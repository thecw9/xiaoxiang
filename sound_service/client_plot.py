import socket
import numpy as np
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
print("开始接收数据并绘制波形...")

# 定义缓冲区，长度为 CHUNK * 10
BUFFER_SIZE = CHUNK * 10
data_buffer = np.zeros(BUFFER_SIZE, dtype=np.int16)

# 定义一个线程锁，用于同步访问 data_buffer
buffer_lock = threading.Lock()

# 定义一个事件，用于控制线程的运行
exit_event = threading.Event()

def receive_data():
    """从服务器接收数据的线程函数"""
    try:
        while not exit_event.is_set():
            # 计算需要接收的字节数
            bytes_needed = CHUNK * CHANNELS * 2  # int16 类型，每个样本2字节
            data_bytes = b''
            while len(data_bytes) < bytes_needed:
                packet = client_socket.recv(bytes_needed - len(data_bytes))
                if not packet:
                    print("服务器已关闭连接")
                    exit_event.set()
                    break
                data_bytes += packet
            if data_bytes:
                # 将字节数据转换为 numpy 数组
                data_array = np.frombuffer(data_bytes, dtype=np.int16).reshape(-1, CHANNELS)
                # 从多通道数据中提取所需通道
                data_channel = data_array[:, selected_channel]
                # 使用线程锁，安全地更新 data_buffer
                with buffer_lock:
                    # 将新的数据追加到缓冲区末尾，并移除开头的旧数据
                    data_buffer[:-CHUNK] = data_buffer[CHUNK:]
                    data_buffer[-CHUNK:] = data_channel
    except Exception as e:
        print(f"接收数据时发生错误：{e}")
        exit_event.set()

# 启动数据接收线程
receive_thread = threading.Thread(target=receive_data)
receive_thread.start()

# 初始化绘图
fig, ax = plt.subplots()
x = np.arange(0, BUFFER_SIZE)
line, = ax.plot(x, np.zeros(BUFFER_SIZE))
ax.set_ylim([-32768, 32767])  # int16 的取值范围
ax.set_xlim([0, BUFFER_SIZE])
plt.xlabel('样本点')
plt.ylabel('幅度')
plt.title('实时数据波形（滚动显示）')

def update_waveform(frame):
    """更新波形的函数"""
    if exit_event.is_set():
        plt.close(fig)
        return line,
    # 使用线程锁，安全地读取 data_buffer
    with buffer_lock:
        # 更新波形图
        line.set_ydata(data_buffer)
    return line,

# 使用 FuncAnimation 实现实时更新
ani = animation.FuncAnimation(fig, update_waveform, interval=50, blit=True)

# 显示图形
try:
    plt.show()
except KeyboardInterrupt:
    print("用户中断，正在关闭...")

# 程序结束，设置退出事件
exit_event.set()
receive_thread.join()
client_socket.close()

