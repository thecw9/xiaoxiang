import sounddevice as sd
import threading
import socket
import numpy as np
import json

# 音频参数设置
CHUNK = 1024              # 每个缓冲区的帧数
CHANNELS = 1              # 声道数

# 列出所有可用的音频输入设备
print("可用的音频输入设备列表：")
input_devices = []
devices = sd.query_devices()
for idx, device in enumerate(devices):
    if device['max_input_channels'] > 0:
        input_devices.append(idx)
        print(f"设备索引：{idx}, 设备名称：{device['name']}")

# 让用户选择设备索引
while True:
    try:
        DEVICE_INDEX = int(input("请选择要使用的设备索引："))
        if DEVICE_INDEX in input_devices:
            break
        else:
            print("无效的设备索引，请重新输入。")
    except ValueError:
        print("请输入有效的数字索引。")

# 获取所选设备的详细信息
device_info = sd.query_devices(DEVICE_INDEX, 'input')
SUPPORTED_RATES = [8000, 16000, 32000, 44100, 48000, 96000]

# 检查设备支持的采样率
supported_rates = []
for rate in SUPPORTED_RATES:
    try:
        sd.check_input_settings(device=DEVICE_INDEX, channels=CHANNELS, samplerate=rate)
        supported_rates.append(rate)
    except Exception:
        continue

print(f"所选设备支持的采样率：{supported_rates}")

# 设置默认采样率为支持的第一个采样率
default_rate = supported_rates[0]

# 让用户选择采样率，提供默认值
while True:
    try:
        rate_input = input(f"请选择采样率 {supported_rates} 中的一个（按回车选择默认值 {default_rate}）：")
        if not rate_input.strip():
            RATE = default_rate
            print(f"已选择默认采样率：{RATE}")
            break
        RATE = int(rate_input)
        if RATE in supported_rates:
            break
        else:
            print("无效的采样率，请重新输入。")
    except ValueError:
        print("请输入有效的采样率。")

# 网络参数设置
HOST = '0.0.0.0'  # 监听所有可用的网络接口
PORT = 50007      # 监听的端口号

# 创建 TCP 服务端 Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = []                # 存储客户端连接的列表，包含 (conn, addr) 元组
clients_lock = threading.Lock()  # 线程锁，用于同步访问 clients 列表

def accept_clients():
    """接受新的客户端连接"""
    while True:
        conn, addr = server_socket.accept()
        # 向客户端发送音频配置
        audio_config = {
            'RATE': RATE,
            'CHANNELS': CHANNELS,
            'FORMAT': 'int16',
            'CHUNK': CHUNK
        }
        config_str = json.dumps(audio_config) + '\n'
        conn.sendall(config_str.encode('utf-8'))
        with clients_lock:
            clients.append((conn, addr))
        print(f"客户端已连接：{addr}，已发送音频配置：{audio_config}")

# 启动线程来接受客户端连接
accept_thread = threading.Thread(target=accept_clients, daemon=True)
accept_thread.start()

print("服务器已启动，等待客户端连接...")

def callback(indata, frames, time, status):
    """这是音频输入流的回调函数，用于处理实时音频数据"""
    if status:
        print(status)
    # 使用 numpy 进行数据转换
    data_int16 = np.int16(indata * 32767)
    # 将数据转换为字节形式
    data_bytes = data_int16.tobytes()
    # 向所有已连接的客户端发送数据
    with clients_lock:
        for c, addr in clients[:]:
            try:
                c.sendall(data_bytes)
            except Exception as e:
                print(f"客户端已断开连接：{addr}")
                clients.remove((c, addr))
                c.close()

# 打开输入流并开始采集音频数据
try:
    with sd.InputStream(samplerate=RATE, channels=CHANNELS, device=DEVICE_INDEX,
                        blocksize=CHUNK, callback=callback):
        print("开始采集音频数据，按 Ctrl+C 退出。")
        threading.Event().wait()  # 保持主线程运行
except KeyboardInterrupt:
    print("服务器正在关闭...")
finally:
    server_socket.close()
