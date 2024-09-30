use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use serde::{Deserialize, Serialize};
use tokio::io::AsyncWriteExt;
use tokio::net::TcpListener;
use tokio::sync::broadcast;

#[derive(Serialize, Deserialize, Debug)]
struct AudioConfig {
    sample_rate: u32,
    channels: u16,
    sample_format: String,
}

#[tokio::main]
async fn main() {
    // 创建一个广播通道，容量为16
    let (tx, _) = broadcast::channel::<Vec<u8>>(16);

    // 获取音频输入设备和配置
    let host = cpal::default_host();
    let device = host.default_input_device().expect("没有可用的输入设备");
    let config = device.default_input_config().unwrap();

    println!("输入设备: {}", device.name().unwrap());
    println!("默认输入配置: {:?}", config);

    let sample_format = config.sample_format();
    let config_clone = config.clone();

    // 启动音频采集任务
    let tx_clone = tx.clone();
    tokio::spawn(async move {
        capture_audio(tx_clone, device, config, sample_format);
    });

    // 启动 TCP 服务器
    let listener = TcpListener::bind("0.0.0.0:12345").await.unwrap();

    loop {
        let (mut socket, _) = listener.accept().await.unwrap();
        let mut rx = tx.subscribe();

        // 在客户端连接后，发送音频配置
        let audio_config = AudioConfig {
            sample_rate: config_clone.sample_rate().0,
            channels: config_clone.channels(),
            sample_format: format!("{:?}", sample_format),
        };

        // 序列化音频配置为 JSON，并添加换行符作为结束标志
        let config_data = serde_json::to_string(&audio_config).unwrap() + "\n";

        // 发送配置数据给客户端
        if let Err(e) = socket.write_all(config_data.as_bytes()).await {
            eprintln!("发送音频配置失败: {}", e);
            continue;
        }

        // 为每个客户端连接启动一个异步任务
        tokio::spawn(async move {
            loop {
                match rx.recv().await {
                    Ok(data) => {
                        if let Err(e) = socket.write_all(&data).await {
                            eprintln!("发送数据失败: {}", e);
                            break;
                        }
                    }
                    Err(broadcast::error::RecvError::Lagged(_)) => {
                        eprintln!("客户端处理速度过慢，跳过一些数据");
                    }
                    Err(broadcast::error::RecvError::Closed) => {
                        eprintln!("通道已关闭");
                        break;
                    }
                }
            }
        });
    }
}

fn capture_audio(
    tx: broadcast::Sender<Vec<u8>>,
    device: cpal::Device,
    config: cpal::SupportedStreamConfig,
    sample_format: cpal::SampleFormat,
) {
    let err_fn = |err| eprintln!("音频输入流发生错误: {}", err);

    // 根据采样格式构建输入流
    let stream = match sample_format {
        cpal::SampleFormat::F32 => device.build_input_stream(
            &config.config(),
            move |data: &[f32], _: &cpal::InputCallbackInfo| {
                send_input_data::<f32>(data, &tx)
            },
            err_fn,
        ),
        cpal::SampleFormat::I16 => device.build_input_stream(
            &config.config(),
            move |data: &[i16], _: &cpal::InputCallbackInfo| {
                send_input_data::<i16>(data, &tx)
            },
            err_fn,
        ),
        cpal::SampleFormat::U16 => device.build_input_stream(
            &config.config(),
            move |data: &[u16], _: &cpal::InputCallbackInfo| {
                send_input_data::<u16>(data, &tx)
            },
            err_fn,
        ),
    }
    .unwrap();

    stream.play().unwrap();

    // 保持流运行
    std::thread::sleep(std::time::Duration::from_secs(u64::MAX));
}

fn send_input_data<T>(input: &[T], tx: &broadcast::Sender<Vec<u8>>)
where
    T: cpal::Sample + bytemuck::Pod,
{
    // 将采样数据转换为字节切片
    let bytes: &[u8] = bytemuck::cast_slice(input);
    let data = bytes.to_vec();
    // 发送数据到所有订阅者
    let _ = tx.send(data);
}
