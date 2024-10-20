import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis
from scipy.fft import fft

# 计算均方根
def rms(signal):
    """
    说明：信号的能量水平，反映整体振动能量。
    诊断内容：
        整体振动能量增加：RMS值的提升通常意味着系统整体振动能量增加，可能与多种机械故障（如轴承损坏、齿轮磨损）或电气故障（如绕组短路）相关。
        故障早期检测：RMS作为一个综合能量指标，可以用于早期检测故障的潜在发展。
    """
    return np.sqrt(np.mean(np.square(signal)))

# 计算峰值
def peak(signal):
    return np.max(np.abs(signal))

# 计算偏度
def skewness(signal):
    return skew(signal)

# 计算峰值因子
def crest_factor(signal):
    """
    定义：峰值因子是信号峰峰值与 RMS 值的比值，反映信号中的尖锐脉冲特性。
    诊断意义：
        脉冲特征识别：高峰值因子表示信号中存在尖锐的脉冲，这通常与局部放电或电气击穿等高频故障相关。
        信号非线性检测：峰值因子的增加表明信号的非线性成分增强，提示潜在的电气故障。
    """
    return np.max(np.abs(signal)) / rms(signal)

# 计算脉冲因子
def impulsive_factor(signal):
    return peak(signal) / np.mean(np.abs(signal))

# 计算形状因子
def shape_factor(signal):
    return rms(signal) / np.mean(np.abs(signal))


# 计算过零率
def zero_crossing_rate(signal):
    """
    定义：过零率是信号波形过零点的频率，反映信号中的高频成分。
    诊断意义：
        频率成分变化：过零率的增加通常表明信号中高频成分增加，这可能与机械不平衡或电磁故障相关。
        振动频率检测：过零率可以间接反映振动的频率特性，有助于识别特定频率的异常振动。
    """
    return np.sum(np.abs(np.diff(np.sign(signal)))) / (2 * len(signal))

# 计算频谱质心
def spectral_centroid(signal, sample_rate):
    """
    定义：频谱质心是频谱的重心位置，反映了频谱的“亮度”。
    诊断意义：
        高频成分检测：质心上移表示高频成分增加，可能与局部放电、电气击穿或高频振动相关。
        频谱能量分布分析：通过质心的变化，可以了解频谱能量在不同频率范围的分布情况，有助于识别特定故障类型。
    """
    centroid = librosa.feature.spectral_centroid(y=signal, sr=sample_rate)
    return float(np.mean(centroid))

# 计算频谱带宽
def spectral_bandwidth(signal, sample_rate):
    """
    """
    bandwidth = librosa.feature.spectral_bandwidth(y=signal, sr=sample_rate)
    return float(np.mean(bandwidth))

# 计算频谱峰度
def spectral_kurtosis(signal):
    """
    """
    fft_magnitude = np.abs(np.fft.rfft(signal))
    return kurtosis(fft_magnitude)

# 计算频谱
def compute_fft(signal, sample_rate):
    N = len(signal)
    yf = fft(signal)
    xf = np.fft.fftfreq(N, 1/sample_rate)
    return xf[:N//2], np.abs(yf[:N//2])

# 绘制频谱
def plot_spectrum(signal, sample_rate):
    xf, yf = compute_fft(signal, sample_rate)
    plt.plot(xf, yf)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Spectrum')
    plt.show()

if __name__ == "__main__":
    # 使用示例
    sampling_rate = 1000  # 假设采样率为1000 Hz
    signal = np.random.randn(1000)  # 随机生成模拟信号
    print(f"RMS: {rms(signal)}")
    print(f"Crest Factor: {crest_factor(signal)}")
    print(f"Zero Crossing Rate: {zero_crossing_rate(signal)}")
    print(f"Skewness: {skew(signal)}")
    print(f"Kurtosis: {kurtosis(signal)}")
    print(f"Spectral Centroid: {spectral_centroid(signal, sampling_rate)}")
    print(f"Spectral Bandwidth: {spectral_bandwidth(signal, sampling_rate)}")
    print(f"Spectral Kurtosis: {spectral_kurtosis(signal)}")

    # 使用示例
    # plot_spectrum(signal, sampling_rate)

