import os
import socket
import librosa
import json
import numpy as np
from io import BytesIO
import scipy
from kafka import KafkaProducer
from datetime import datetime
import matplotlib.pyplot as plt
from minio import Minio
from minio.error import S3Error
from features import (
    rms,
    crest_factor,
    zero_crossing_rate,
    kurtosis,
    skewness,
    spectral_centroid,
    spectral_bandwidth,
    spectral_kurtosis,
)

position = "测试地址"

# Kafka 参数设置
KAFKA_SERVER = os.environ["KAFKA_BOOTSTRAP_SERVERS"]  # Kafka 服务器地址
KAFKA_TOPIC = os.environ["KAFKA_REALDATA_TOPIC"]  # Kafka 主题名称

# 创建 Kafka 生产者
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
)

# 网络参数设置
HOST = os.environ["SOUND_SERVICE_HOST"]  # 请替换为服务器的实际 IP 地址
PORT = int(os.environ["SOUND_SERVICE_PORT"])

# 创建 TCP 客户端套接字并连接到服务器
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("已连接到服务器，正在接收数据采集配置...")

# MinIO 参数设置
MINIO_ENDPOINT = os.environ["MINIO_ENDPOINT"]
MINIO_ACCESS_KEY = os.environ["MINIO_ACCESS_KEY"]
MINIO_SECRET_KEY = os.environ["MINIO_SECRET_KEY"]
BUCKET_NAME = os.environ["BUCKET_NAME"]

# 创建MinIO客户端
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)

# 创建MinIO Bucket
bucket_exists = minio_client.bucket_exists(BUCKET_NAME)
if not bucket_exists:
    try:
        minio_client.make_bucket(BUCKET_NAME)
        print(f"Bucket {BUCKET_NAME} is successfully created.")
    except Exception as err:
        print(f"Failed to create bucket: {err}")


def save_to_minio(minio_client, bucket_name, file_name, data, content_type):
    try:
        minio_client.put_object(
            bucket_name,
            file_name,
            data,
            data.getbuffer().nbytes,
            content_type=content_type,
        )
        print(f"File {file_name} is successfully saved to MinIO.")
    except S3Error as err:
        print(f"Failed to save file to MinIO: {err}")


# 接收数据采集配置
def recv_config(sock):
    config_data = b""
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            raise Exception("服务器已关闭连接")
        config_data += chunk
        if b"\n" in chunk:
            break
    # 去掉末尾的换行符，并解析 JSON
    config_str = config_data.decode("utf-8").strip()
    data_config = json.loads(config_str)
    return data_config


try:
    # 接收并解析数据采集配置
    data_config = recv_config(client_socket)
    print(f"接收到的数据采集配置：{data_config}")

    # 从配置中获取参数
    SAMPLE_RATE = data_config["SAMPLE_RATE"]
    CHANNELS = data_config["CHANNELS"]
    FORMAT = data_config["FORMAT"]  # 'int16'
    CHUNK = data_config["CHUNK"]

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
print("开始接收数据并提取特征并发送到Kafka")

# 定义缓冲区，长度为 CHUNK * 10
BUFFER_SIZE = CHUNK * (SAMPLE_RATE // CHUNK) * 60

try:
    while True:
        # 计算需要接收的字节数
        bytes_needed = BUFFER_SIZE * CHANNELS * 2  # int16 类型，每个样本2字节
        data_bytes = b""
        while len(data_bytes) < bytes_needed:
            packet = client_socket.recv(bytes_needed - len(data_bytes))
            if not packet:
                print("服务器已关闭连接")
                break
            data_bytes += packet
        if data_bytes:
            # 将字节数据转换为 numpy 数组
            data_int16 = np.frombuffer(data_bytes, dtype=np.int16).reshape(-1, CHANNELS)
            # 将 int16 数据转换为 float32，范围从 -1.0 到 1.0
            data_float32 = data_int16.astype(np.float32) / 32767
            # 从多通道数据中提取所需通道
            data_channel = data_float32[:, selected_channel]

            now = datetime.now().isoformat()
            current_key = 900000000
            # 计算 RMS 值
            current_key += 1
            message = {
                "value": float(rms(data_channel)),
                "fresh_time": now,
                "time": now,
                "path": f"/潇湘站数字特高压IV区/声纹监测/{position}/时域指标_RMS",
                "name": f"{position}_RMS",
                "unit": "",
                "quality": 0,
                "key": str(current_key),
            }
            # 发送 RMS 值到 Kafka
            producer.send(KAFKA_TOPIC, message)

            # 计算峰值因子
            current_key += 1
            message = {
                "value": float(crest_factor(data_channel)),
                "fresh_time": now,
                "time": now,
                "path": f"/潇湘站数字特高压IV区/声纹监测/{position}/时域指标_峰值因子",
                "name": f"{position}_crest_factor",
                "unit": "",
                "quality": 0,
                "key": str(current_key),
            }
            # 发送峰值因子到 Kafka
            producer.send(KAFKA_TOPIC, message)

            # 计算零交叉率
            current_key += 1
            message = {
                "value": float(zero_crossing_rate(data_channel)),
                "fresh_time": now,
                "time": now,
                "path": f"/潇湘站数字特高压IV区/声纹监测/{position}/时域指标_跨零率",
                "name": f"{position}_zero_crossing_rate",
                "unit": "",
                "quality": 0,
                "key": str(current_key),
            }
            # 发送零交叉率到 Kafka
            producer.send(KAFKA_TOPIC, message)

            # 计算峰度
            current_key += 1
            message = {
                "value": float(kurtosis(data_channel)),
                "fresh_time": now,
                "time": now,
                "path": f"/潇湘站数字特高压IV区/声纹监测/{position}/时域指标_峰度",
                "name": f"{position}_kurtosis",
                "unit": "",
                "quality": 0,
                "key": str(current_key),
            }
            # 发送峰度到 Kafka
            producer.send(KAFKA_TOPIC, message)

            # 计算偏度
            current_key += 1
            message = {
                "value": float(skewness(data_channel)),
                "fresh_time": now,
                "time": now,
                "path": f"/潇湘站数字特高压IV区/声纹监测/{position}/时域指标_偏度",
                "name": f"{position}_skewness",
                "unit": "",
                "quality": 0,
                "key": str(current_key),
            }
            producer.send(KAFKA_TOPIC, message)

            # 计算频谱中心
            current_key += 1
            message = {
                "value": float(spectral_centroid(data_channel, SAMPLE_RATE)),
                "fresh_time": now,
                "time": now,
                "path": f"/潇湘站数字特高压IV区/声纹监测/{position}/频域指标_频谱质心",
                "name": f"{position}_spectral_centroid",
                "unit": "",
                "quality": 0,
                "key": str(current_key),
            }
            # 发送频谱中心到 Kafka
            producer.send(KAFKA_TOPIC, message)

            # 计算频谱带宽
            current_key += 1
            message = {
                "value": float(spectral_bandwidth(data_channel, SAMPLE_RATE)),
                "fresh_time": now,
                "time": now,
                "path": f"/潇湘站数字特高压IV区/声纹监测/{position}/频域指标_频谱带宽",
                "name": f"{position}_spectral_bandwidth",
                "unit": "",
                "quality": 0,
                "key": str(current_key),
            }
            producer.send(KAFKA_TOPIC, message)

            # 计算频谱
            current_key += 1
            message = {
                "value": float(spectral_kurtosis(data_channel)),
                "fresh_time": now,
                "time": now,
                "path": f"/潇湘站数字特高压IV区/声纹监测/{position}/频域指标_频谱峰度",
                "name": f"{position}_spectral_kurtosis",
                "unit": "",
                "quality": 0,
                "key": str(current_key),
            }
            # 发送频谱峰度到 Kafka
            producer.send(KAFKA_TOPIC, message)

            producer.flush()
            print("数据已发送到Kafka")

            # 存储音频文件
            wav_io = BytesIO()
            sound_data = (data_channel * 32767).astype(np.int16)
            scipy.io.wavfile.write(wav_io, SAMPLE_RATE, sound_data)
            wav_io.seek(0)
            object_name = (
                f"audio/{datetime.now().strftime('%Y-%m-%d/%H-%M')}_{position}.wav"
            )
            save_to_minio(
                minio_client=minio_client,
                bucket_name=BUCKET_NAME,
                file_name=object_name,
                data=wav_io,
                content_type="audio/wav",
            )

            # 存储波形图
            fig, ax = plt.subplots(figsize=(8, 4))
            # 隐藏顶部和右侧的轴线
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            # 隐藏底部和左侧的轴线
            ax.spines["bottom"].set_visible(False)
            ax.spines["left"].set_visible(False)
            # 隐藏X轴刻度
            ax.xaxis.set_ticks([])
            # 设置Y轴刻度和刻度标签的颜色为白色（可根据背景颜色调整）
            ax.tick_params(axis="y", colors="white")
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            # plt.ylim(-0.01, 0.01)
            plt.plot(data_channel)
            plt.tight_layout()

            wave_img_io = BytesIO()
            plt.savefig(wave_img_io, transparent=True, format="png")
            wave_img_io.seek(0)
            plt.close()
            waveform_object_name = (
                f"waveform/{datetime.now().strftime('%Y-%m-%d/%H-%M')}_{position}.png"
            )
            save_to_minio(
                minio_client=minio_client,
                bucket_name=BUCKET_NAME,
                file_name=waveform_object_name,
                data=wave_img_io,
                content_type="image/png",
            )

            # FFT图
            fft = np.fft.rfft(data_channel)
            freqs = np.fft.rfftfreq(len(data_channel), 1 / SAMPLE_RATE)
            fig, ax = plt.subplots(figsize=(8, 4))
            # 隐藏顶部和右侧的轴线
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)

            # 隐藏底部和左侧的轴线，但保留刻度
            ax.spines["bottom"].set_visible(False)
            ax.spines["left"].set_visible(False)

            # 保留刻度和刻度标签
            ax.xaxis.set_ticks_position("bottom")
            ax.yaxis.set_ticks_position("left")

            # 设置刻度线和刻度标签的颜色为白色
            ax.tick_params(axis="x", colors="white")
            ax.tick_params(axis="y", colors="white")
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            # plt.ylim(0, 1000)
            freq_lenght = len(freqs)
            plt.plot(
                freqs[10 : int(freq_lenght / 4)],
                np.abs(fft[10 : int(freq_lenght / 4)]),
            )
            plt.tight_layout()

            fft_img_io = BytesIO()
            plt.savefig(fft_img_io, transparent=True, format="png")
            fft_img_io.seek(0)
            plt.close()

            fft_object_name = (
                f"fft/{datetime.now().strftime('%Y-%m-%d/%H-%M')}_{position}.png"
            )
            save_to_minio(
                minio_client=minio_client,
                bucket_name=BUCKET_NAME,
                file_name=fft_object_name,
                data=fft_img_io,
                content_type="image/png",
            )

            # 梅尔频谱
            mel_spectrogram = librosa.feature.melspectrogram(
                y=data_channel, sr=SAMPLE_RATE, n_mels=128
            )
            mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            plt.imshow(mel_spectrogram, cmap="viridis", aspect="auto")

            mel_img_io = BytesIO()
            plt.savefig(mel_img_io, transparent=True, format="png")
            mel_img_io.seek(0)
            plt.close()

            img_object_name = (
                f"mel/{datetime.now().strftime('%Y-%m-%d/%H-%M')}_{position}.png"
            )
            save_to_minio(
                minio_client=minio_client,
                bucket_name=BUCKET_NAME,
                file_name=img_object_name,
                data=mel_img_io,
                content_type="image/png",
            )
except Exception as e:
    client_socket.close()
    print(f"接收数据时发生错误：{e}")
