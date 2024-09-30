import socket
import numpy as np
import threading
import sounddevice as sd
import json

# 网络参数设置
HOST = '10.126.233.202'  # 请替换为服务器的实际 IP 地址
PORT = 50007

# 创建 TCP 客户端套接字并连接到服务器
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("已连接到服务器，正在接收数据采集配置...")

# 接收数据采集配置
def recv_config(sock):
    config_data = b''
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            raise Exception("服务器已关闭连接")
        config_data += chunk
        if b'\n' in chunk:
            break
    # 去掉末尾的换行符，并解析 JSON
    config_str = config_data.decode('utf-8').strip()
    data_config = json.loads(config_str)
    return data_config

try:
    # 接收并解析数据采集配置
    data_config = recv_config(client_socket)
    print(f"接收到的数据采集配置：{data_config}")

    # 从配置中获取参数
    SAMPLE_RATE = data_config['SAMPLE_RATE']
    CHANNELS = data_config['CHANNELS']
    FORMAT = data_config['FORMAT']  # 'int16'
    CHUNK = data_config['CHUNK']

except Exception as e:
    print(f"接收数据采集配置时发生错误：{e}")
    client_socket.close()
    exit(1)

# 选择要播放的通道
if CHANNELS > 1:
    print(f"检测到 {CHANNELS} 个通道。")
    while True:
        try:
            selected_channel = int(input(f"请选择要播放的通道（0 到 {CHANNELS-1}）：")) 
            if 0 <= selected_channel < CHANNELS:
                break
            else:
                print("无效的通道编号，请重新输入。")
        except ValueError:
            print("请输入有效的数字。")
    print(f"已选择播放通道：{selected_channel}")
else:
    selected_channel = 0  # 只有一个通道，默认选择

print("开始接收数据并实时播放...")

def audio_callback(outdata, frames, time, status):
    if status:
        print(status)
    try:
        # 计算需要接收的字节数
        bytes_needed = CHUNK * CHANNELS * 2  # int16 类型，每个样本2字节
        data_bytes = b''
        while len(data_bytes) < bytes_needed:
            packet = client_socket.recv(bytes_needed - len(data_bytes))
            if not packet:
                print("服务器已关闭连接")
                raise sd.CallbackAbort()
            data_bytes += packet
        # 将字节数据转换为 numpy 数组
        data_int16 = np.frombuffer(data_bytes, dtype=np.int16).reshape(-1, CHANNELS)
        # 将 int16 数据转换为 float32，范围从 -1.0 到 1.0
        data_float32 = data_int16.astype(np.float32) / 32767
        # 从多通道数据中提取所需通道
        data_channel = data_float32[:, selected_channel]
        # 将数据写入输出缓冲区
        outdata[:] = data_channel[:, None]
    except Exception as e:
        print(f"错误：{e}")
        raise sd.CallbackAbort()

try:
    with sd.OutputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, blocksize=CHUNK,
                         dtype='float32', callback=audio_callback):
        threading.Event().wait()
except KeyboardInterrupt:
    print("客户端正在关闭...")
finally:
    client_socket.close()

