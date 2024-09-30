import socket
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
    print(audio_config)

    SAMPLE_RATE = audio_config['sample_rate']
    CHANNELS = audio_config['channels']
    sample_format_str = audio_config['sample_format']

    if sample_format_str == 'F32':
        SAMPLE_FORMAT = 'f'
        y_limit = [-1.0, 1.0]
    elif sample_format_str == 'I16':
        SAMPLE_FORMAT = 'h'
        y_limit = [-32768, 32767]
    elif sample_format_str == 'U16':
        SAMPLE_FORMAT = 'H'
        y_limit = [0, 65535]
    else:
        raise ValueError("不支持的采样格式")

    CHUNK_SIZE = 1024  # 每次读取的样本数
    WINDOW_SIZE = CHUNK_SIZE * 10  # 窗口大小，共显示 1024 * 10 个样本

    # 初始化数据缓冲区
    data_buffer = np.zeros(WINDOW_SIZE)

    # 设置 matplotlib 图形
    fig, ax = plt.subplots()
    xdata = np.arange(0, WINDOW_SIZE)
    line, = ax.plot(xdata, data_buffer)
    ax.set_ylim(y_limit)
    ax.set_xlim(0, WINDOW_SIZE - 1)
    ax.set_xlabel('样本')
    ax.set_ylabel('幅值')
    ax.set_title('实时音频波形')

    def init():
        line.set_ydata(np.zeros(WINDOW_SIZE))
        return line,

    def update(frame):
        sample_size = struct.calcsize(SAMPLE_FORMAT)
        total_bytes = CHUNK_SIZE * sample_size
        data = b''
        while len(data) < total_bytes:
            packet = client_socket.recv(total_bytes - len(data))
            if not packet:
                break
            data += packet

        if not data:
            return line,

        num_samples = len(data) // sample_size
        samples = struct.unpack('<' + SAMPLE_FORMAT * num_samples, data[:num_samples * sample_size])
        new_data = np.array(samples)

        # 更新数据缓冲区，移除最旧的样本，添加新样本
        data_buffer[:-CHUNK_SIZE] = data_buffer[CHUNK_SIZE:]
        data_buffer[-CHUNK_SIZE:] = new_data

        # 更新波形数据
        line.set_ydata(data_buffer)
        return line,

    ani = animation.FuncAnimation(fig, update, init_func=init, interval=10, blit=True)
    plt.show()

    client_socket.close()

if __name__ == "__main__":
    main()
