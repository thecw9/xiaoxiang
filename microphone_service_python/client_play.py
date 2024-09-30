import socket
import sounddevice as sd
import numpy as np
import threading
import json

# 网络参数设置
HOST = '127.0.0.1'  # 请替换为服务器的实际 IP 地址
PORT = 50007

# 创建 TCP 客户端套接字并连接到服务器
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("已连接到服务器，正在接收音频配置...")

# 接收音频配置
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
    audio_config = json.loads(config_str)
    return audio_config

try:
    # 接收并解析音频配置
    audio_config = recv_config(client_socket)
    print(f"接收到的音频配置：{audio_config}")

    # 从配置中获取音频参数
    RATE = audio_config['RATE']
    CHANNELS = audio_config['CHANNELS']
    FORMAT = audio_config['FORMAT']  # 本例中未使用，因为我们固定为 int16
    CHUNK = audio_config['CHUNK']

except Exception as e:
    print(f"接收音频配置时发生错误：{e}")
    client_socket.close()
    exit(1)

print("开始接收并播放音频数据...")

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
                raise Exception("服务器已关闭连接")
            data_bytes += packet
        # 将字节数据转换为 numpy 数组
        data_int16 = np.frombuffer(data_bytes, dtype=np.int16)
        # 将 int16 数据转换为 float32，范围从 -1.0 到 1.0
        data_float32 = data_int16.astype(np.float32) / 32767
        outdata[:] = data_float32.reshape(-1, CHANNELS)
    except Exception as e:
        print(f"错误：{e}")
        raise sd.CallbackAbort

try:
    with sd.OutputStream(samplerate=RATE, channels=CHANNELS, blocksize=CHUNK,
                         dtype='float32', callback=audio_callback):
        threading.Event().wait()
except KeyboardInterrupt:
    print("客户端正在关闭...")
finally:
    client_socket.close()
