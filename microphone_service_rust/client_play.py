import socket
import struct
import json
import numpy as np
import sounddevice as sd

# 服务器地址和端口
HOST = '127.0.0.1'
PORT = 12345

def main():
    # 创建 TCP 套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # 接收音频配置数据，直到遇到换行符
    config_data = b''
    while not config_data.endswith(b'\n'):
        packet = client_socket.recv(1024)
        if not packet:
            break
        config_data += packet

    # 去掉末尾的换行符
    config_data = config_data.rstrip(b'\n')

    # 解析 JSON 数据
    audio_config = json.loads(config_data.decode('utf-8'))

    SAMPLE_RATE = audio_config['sample_rate']
    CHANNELS = audio_config['channels']
    sample_format_str = audio_config['sample_format']

    if sample_format_str == 'F32':
        dtype = 'float32'
        struct_format = 'f'
    elif sample_format_str == 'I16':
        dtype = 'int16'
        struct_format = 'h'
    elif sample_format_str == 'U16':
        dtype = 'uint16'
        struct_format = 'H'
    else:
        raise ValueError("不支持的采样格式")

    CHUNK_SIZE = 1024  # 每次读取的样本数
    sample_size = struct.calcsize(struct_format)

    def audio_callback(outdata, frames, time, status):
        if status:
            print(status)
        total_bytes = frames * CHANNELS * sample_size
        data = b''
        while len(data) < total_bytes:
            packet = client_socket.recv(total_bytes - len(data))
            if not packet:
                break
            data += packet

        if not data:
            raise sd.CallbackAbort

        num_samples = len(data) // sample_size
        samples = struct.unpack('<' + struct_format * num_samples, data)
        outdata[:] = np.array(samples).reshape(-1, CHANNELS)

    try:
        with sd.OutputStream(samplerate=SAMPLE_RATE,
                             channels=CHANNELS,
                             dtype=dtype,
                             callback=audio_callback):
            print("按下 Ctrl+C 结束")
            while True:
                sd.sleep(1000)
    except KeyboardInterrupt:
        print("用户中断")
    except Exception as e:
        print(f"错误: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
