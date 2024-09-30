import nidaqmx
from nidaqmx.constants import AcquisitionType
import threading
import socket
import numpy as np
import json

# 数据采集参数设置
SAMPLE_RATE = 10000  # 采样率（根据您的需求设置）
SAMPLES_PER_CHUNK = 1024  # 每个数据块的样本数
CHANNEL_NAMES = ["cDAQ1Mod1/ai0",
                 "cDAQ1Mod1/ai1"]  # 您的 NI DAQ 设备和通道名称，请根据实际情况修改

# 网络参数设置
HOST = '0.0.0.0'  # 监听所有可用的网络接口
PORT = 50007  # 监听的端口号

# 创建 TCP 服务端 Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = []  # 存储客户端连接的列表，包含 (conn, addr) 元组
clients_lock = threading.Lock()  # 线程锁，用于同步访问 clients 列表


def accept_clients():
    """接受新的客户端连接"""
    while True:
        conn, addr = server_socket.accept()
        # 向客户端发送数据采集配置
        data_config = {
            'SAMPLE_RATE': SAMPLE_RATE,
            'CHANNELS': len(CHANNEL_NAMES),
            'FORMAT': 'int16',  # 修改为 'int16'
            'CHUNK': SAMPLES_PER_CHUNK
        }
        config_str = json.dumps(data_config) + '\n'
        conn.sendall(config_str.encode('utf-8'))
        with clients_lock:
            clients.append((conn, addr))
        print(f"客户端已连接：{addr}，已发送数据采集配置：{data_config}")


# 启动线程来接受客户端连接
accept_thread = threading.Thread(target=accept_clients, daemon=True)
accept_thread.start()

print("服务器已启动，等待客户端连接...")

# 创建一个任务，从 NI DAQ 采集数据
with nidaqmx.Task() as task:
    # 配置模拟输入通道
    for channel_name in CHANNEL_NAMES:
        task.ai_channels.add_ai_voltage_chan(channel_name)

    # 配置采样时钟
    task.timing.cfg_samp_clk_timing(rate=SAMPLE_RATE,
                                    sample_mode=AcquisitionType.CONTINUOUS,
                                    samps_per_chan=SAMPLES_PER_CHUNK)

    # 开始数据采集
    task.start()
    print("开始从 NI 数据采集卡采集数据，按 Ctrl+C 退出。")

    try:
        while True:
            # 从 NI DAQ 读取数据（float64 类型）
            data = task.read(number_of_samples_per_channel=SAMPLES_PER_CHUNK)
            # 如果通道数为1，则 data 的形状为 (SAMPLES_PER_CHUNK,)，需要转换为 (1, SAMPLES_PER_CHUNK)
            if len(CHANNEL_NAMES) == 1:
                data = np.expand_dims(data, axis=0)
            data_array = np.array(
                data, dtype=np.float64)  # 形状为 (CHANNELS, SAMPLES_PER_CHUNK)
            data_array = data_array - np.mean(data_array,
                                              axis=1)[:, np.newaxis]  # 消除直流偏移
            # 将数据从 float64 转换为 int16
            # 假设输入电压范围为 -5V 到 +5V，需要根据实际情况调整
            max_voltage = 5.0  # 最大电压值
            data_int16 = np.int16((data_array / max_voltage) * 32767)
            # 将数据转换为字节形式
            data_bytes = data_int16.tobytes(order='F')  # 使用列优先顺序
            # 向所有已连接的客户端发送数据
            with clients_lock:
                for c, addr in clients[:]:
                    try:
                        c.sendall(data_bytes)
                    except Exception as e:
                        print(f"客户端已断开连接：{addr}")
                        clients.remove((c, addr))
                        c.close()
    except KeyboardInterrupt:
        print("服务器正在关闭...")
    finally:
        server_socket.close()
