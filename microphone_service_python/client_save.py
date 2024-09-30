import socket
import numpy as np
import threading
import json
import wave
import time

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
    FORMAT = audio_config['FORMAT']  # 本例中为 'int16'
    CHUNK = audio_config['CHUNK']

except Exception as e:
    print(f"接收音频配置时发生错误：{e}")
    client_socket.close()
    exit(1)

print("开始接收音频数据并保存到文件...")

# 根据 FORMAT 确定采样宽度（bytes）
if FORMAT == 'int16':
    sampwidth = 2
elif FORMAT == 'int32':
    sampwidth = 4
elif FORMAT == 'float32':
    sampwidth = 4
else:
    raise ValueError(f"不支持的音频格式：{FORMAT}")

# 打开 WAV 文件进行写入
timestamp = time.strftime("%Y%m%d-%H%M%S")
filename = f"recorded_audio_{timestamp}.wav"
wf = wave.open(filename, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(sampwidth)
wf.setframerate(RATE)

# 定义一个事件，用于控制线程的运行
exit_event = threading.Event()

def receive_and_save():
    """接收音频数据并保存到文件"""
    try:
        while not exit_event.is_set():
            # 计算需要接收的字节数
            bytes_needed = CHUNK * CHANNELS * sampwidth
            data_bytes = b''
            while len(data_bytes) < bytes_needed:
                packet = client_socket.recv(bytes_needed - len(data_bytes))
                if not packet:
                    print("服务器已关闭连接")
                    exit_event.set()
                    break
                data_bytes += packet
            if data_bytes:
                # 直接将字节数据写入 WAV 文件
                wf.writeframes(data_bytes)
    except Exception as e:
        print(f"接收数据时发生错误：{e}")
        exit_event.set()

# 启动接收和保存数据的线程
receive_thread = threading.Thread(target=receive_and_save)
receive_thread.start()

print("正在录制音频，按 Ctrl+C 停止并保存文件。")

try:
    while not exit_event.is_set():
        time.sleep(1)
except KeyboardInterrupt:
    print("停止录制。")
    exit_event.set()

# 等待线程结束
receive_thread.join()
# 关闭文件和套接字
wf.close()
client_socket.close()
print(f"音频已保存到文件：{filename}")
