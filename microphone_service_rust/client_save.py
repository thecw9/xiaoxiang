import socket
import struct
import numpy as np
import soundfile as sf
import json

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
        SAMPLE_FORMAT = 'f'
        DTYPE = 'float32'
        SUBTYPE = 'FLOAT'
    elif sample_format_str == 'I16':
        SAMPLE_FORMAT = 'h'
        DTYPE = 'int16'
        SUBTYPE = 'PCM_16'
    elif sample_format_str == 'U16':
        SAMPLE_FORMAT = 'H'
        DTYPE = 'uint16'
        SUBTYPE = 'PCM_16'  # WAV 文件不支持 uint16，使用 int16
    else:
        raise ValueError("不支持的采样格式")

    # 创建 WAV 文件
    filename = 'output.wav'
    file = sf.SoundFile(filename, mode='w', samplerate=SAMPLE_RATE, channels=CHANNELS, subtype=SUBTYPE)

    try:
        sample_size = struct.calcsize(SAMPLE_FORMAT)
        buffer_size = 4096  # 每次接收的字节数

        while True:
            # 接收数据
            data = b''
            while len(data) < buffer_size:
                packet = client_socket.recv(buffer_size - len(data))
                if not packet:
                    break
                data += packet

            if not data:
                break

            # 确保数据长度是样本大小的整数倍
            remainder = len(data) % sample_size
            if remainder != 0:
                # 丢弃不完整的样本
                data = data[:-remainder]

            num_samples = len(data) // sample_size
            samples = struct.unpack('<' + SAMPLE_FORMAT * num_samples, data)
            np_samples = np.array(samples, dtype=DTYPE)

            # 如果是多声道，需重塑数组
            if CHANNELS > 1:
                np_samples = np_samples.reshape(-1, CHANNELS)

            # 写入 WAV 文件
            file.write(np_samples)
    finally:
        file.close()
        client_socket.close()
        print(f"音频已保存到 {filename}")

if __name__ == "__main__":
    main()
