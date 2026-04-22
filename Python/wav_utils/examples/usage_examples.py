"""
WAV 工具集使用示例
==================

演示 wav_utils 模块的主要功能。
"""

import os
import sys
import tempfile

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from wav_utils.mod import (
    WavReader, WavWriter, WavProcessor,
    read_wav, write_wav, get_wav_info, create_sine_wav
)


def example_basic_read_write():
    """基本读写示例"""
    print("\n=== 基本读写示例 ===\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, 'basic.wav')
        
        # 创建简单的音频样本
        samples = [int(10000 * (i % 100) / 100) for i in range(4410)]
        
        # 写入 WAV 文件
        info = write_wav(filepath, samples, sample_rate=44100)
        print(f"写入文件: {filepath}")
        print(f"  通道数: {info.channels}")
        print(f"  采样率: {info.sample_rate} Hz")
        print(f"  位深: {info.bits_per_sample} bits")
        print(f"  时长: {info.duration:.3f} 秒")
        
        # 读取 WAV 文件
        read_info, read_samples = read_wav(filepath)
        print(f"\n读取文件:")
        print(f"  样本数: {len(read_samples[0])}")
        print(f"  前5个样本: {read_samples[0][:5]}")


def example_sine_wave():
    """正弦波生成示例"""
    print("\n=== 正弦波生成示例 ===\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, 'sine_440hz.wav')
        
        # 生成 440Hz (A4音符) 正弦波，持续 1 秒
        info = create_sine_wav(
            filepath,
            frequency=440,      # A4 音符
            duration_ms=1000,   # 1 秒
            sample_rate=44100,
            amplitude=0.5       # 50% 振幅
        )
        
        print(f"生成正弦波文件: {filepath}")
        print(f"  频率: 440 Hz (A4 音符)")
        print(f"  时长: {info.duration:.2f} 秒")
        print(f"  文件大小: {os.path.getsize(filepath)} 字节")
        
        # 验证波形
        info, samples = read_wav(filepath)
        max_amplitude = max(abs(s) for s in samples[0])
        print(f"  最大振幅: {max_amplitude}")


def example_stereo_audio():
    """立体声音频示例"""
    print("\n=== 立体声音频示例 ===\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, 'stereo.wav')
        
        # 创建立体声音频（左右声道不同）
        num_samples = 4410  # 0.1 秒
        
        # 左声道：低频
        left_channel = [int(16000 * (i % 100) / 100) for i in range(num_samples)]
        
        # 右声道：高频
        right_channel = [int(16000 * (i % 20) / 20) for i in range(num_samples)]
        
        writer = WavWriter(filepath, sample_rate=44100, channels=2, bits_per_sample=16)
        writer.add_samples([left_channel, right_channel])
        info = writer.write()
        
        print(f"生成立体声文件:")
        print(f"  通道数: {info.channels}")
        print(f"  块对齐: {info.block_align} 字节")
        
        # 读取并验证
        read_info, channels = read_wav(filepath)
        print(f"  左声道样本: {channels[0][:5]}...")
        print(f"  右声道样本: {channels[1][:5]}...")


def example_audio_processing():
    """音频处理示例"""
    print("\n=== 音频处理示例 ===\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, 'process.wav')
        
        # 生成测试音频
        create_sine_wav(filepath, frequency=440, duration_ms=500, amplitude=0.3)
        
        # 读取音频
        info, channels = read_wav(filepath)
        samples = channels[0]
        
        print("原始音频:")
        print(f"  样本数: {len(samples)}")
        print(f"  最大值: {max(samples)}")
        print(f"  最小值: {min(samples)}")
        
        # 1. 归一化
        normalized = WavProcessor.normalize(samples, target_peak=0.9)
        print(f"\n归一化后:")
        print(f"  最大值: {max(normalized)}")
        print(f"  最小值: {min(normalized)}")
        
        # 2. 增益调整
        amplified = WavProcessor.amplify(samples, gain_db=6)
        print(f"\n+6dB 增益后:")
        print(f"  最大值: {max(amplified)}")
        
        # 3. 反转
        reversed_samples = WavProcessor.reverse(samples)
        print(f"\n反转音频:")
        print(f"  原始前5个: {samples[:5]}")
        print(f"  反转后前5个: {reversed_samples[:5]}")


def example_fade_effects():
    """淡入淡出效果示例"""
    print("\n=== 淡入淡出效果示例 ===\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, 'fade.wav')
        
        # 创建恒定振幅的音频
        samples = [10000] * 1000
        
        # 淡入
        fade_in = WavProcessor.fade_in(samples.copy(), duration_ms=50, sample_rate=10000)
        print(f"淡入效果:")
        print(f"  开头样本: {fade_in[:5]}")
        print(f"  结尾样本: {fade_in[-5:]}")
        
        # 淡出
        fade_out = WavProcessor.fade_out(samples.copy(), duration_ms=50, sample_rate=10000)
        print(f"\n淡出效果:")
        print(f"  开头样本: {fade_out[:5]}")
        print(f"  结尾样本: {fade_out[-5:]}")
        
        # 写入带淡入淡出的音频
        filepath_in = os.path.join(temp_dir, 'with_fade.wav')
        writer = WavWriter(filepath_in, sample_rate=44100)
        writer.add_sine_wave(440, 1000, 0.5)
        info = writer.write()
        
        # 读取并应用淡入淡出
        _, channels = read_wav(filepath_in)
        samples = channels[0]
        
        # 应用淡入淡出
        processed = WavProcessor.fade_in(samples, duration_ms=100, sample_rate=44100)
        processed = WavProcessor.fade_out(processed, duration_ms=100, sample_rate=44100)
        
        # 保存处理后的音频
        out_path = os.path.join(temp_dir, 'processed.wav')
        write_wav(out_path, processed, sample_rate=44100)
        
        print(f"\n保存处理后的音频: {out_path}")


def example_silence_detection():
    """静音检测示例"""
    print("\n=== 静音检测示例 ===\n")
    
    # 创建包含静音的测试音频
    samples = (
        [0, 0, 0, 0, 0] +           # 开头静音
        [1000, 2000, 3000, 4000] +   # 有声音
        [0, 0, 0, 0, 0, 0] +         # 中间静音
        [2000, 3000, 4000, 5000] +   # 有声音
        [0, 0, 0, 0]                 # 结尾静音
    )
    
    print(f"测试样本: 共 {len(samples)} 个")
    
    # 检测静音区间
    silence_regions = WavProcessor.find_silence(
        samples,
        threshold=500,
        min_duration_ms=1,
        sample_rate=1000
    )
    
    print(f"\n检测到的静音区间:")
    for i, (start, end) in enumerate(silence_regions):
        print(f"  区间 {i+1}: [{start}, {end}) - 时长: {end - start} 样本")
    
    # 去除首尾静音
    trimmed = WavProcessor.trim_silence(samples, threshold=500)
    print(f"\n去除首尾静音后:")
    print(f"  原始长度: {len(samples)}")
    print(f"  处理后长度: {len(trimmed)}")
    print(f"  处理后样本: {trimmed}")


def example_audio_mixing():
    """音频混合示例"""
    print("\n=== 音频混合示例 ===\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建两个音频源
        # 源1：低频正弦波
        file1 = os.path.join(temp_dir, 'low.wav')
        writer1 = WavWriter(file1, sample_rate=44100)
        writer1.add_sine_wave(220, 500, 0.5)  # A3
        writer1.write()
        
        # 源2：高频正弦波
        file2 = os.path.join(temp_dir, 'high.wav')
        writer2 = WavWriter(file2, sample_rate=44100)
        writer2.add_sine_wave(880, 500, 0.5)  # A5
        writer2.write()
        
        # 读取两个音频
        _, ch1 = read_wav(file1)
        _, ch2 = read_wav(file2)
        
        # 混合
        mixed = WavProcessor.mix([ch1[0], ch2[0]], weights=[0.5, 0.5])
        
        # 保存混合结果
        mixed_file = os.path.join(temp_dir, 'mixed.wav')
        write_wav(mixed_file, mixed, sample_rate=44100)
        
        print(f"混合两个音频源:")
        print(f"  源1: 220 Hz (A3)")
        print(f"  源2: 880 Hz (A5)")
        print(f"  混合后样本数: {len(mixed)}")
        print(f"  保存到: {mixed_file}")


def example_resampling():
    """重采样示例"""
    print("\n=== 重采样示例 ===\n")
    
    # 创建测试样本
    samples = [int(10000 * (i % 50) / 50) for i in range(4410)]
    
    print(f"原始样本数: {len(samples)} (采样率 44100 Hz)")
    
    # 下采样到 22050 Hz
    downsampled = WavProcessor.resample(samples, from_rate=44100, to_rate=22050)
    print(f"下采样到 22050 Hz: {len(downsampled)} 样本")
    
    # 上采样到 88200 Hz
    upsampled = WavProcessor.resample(samples, from_rate=44100, to_rate=88200)
    print(f"上采样到 88200 Hz: {len(upsampled)} 样本")
    
    # 验证插值质量
    print(f"\n插值质量:")
    print(f"  原始样本[100]: {samples[100]}")
    print(f"  上采样后[200]: {upsampled[200]}")


def example_bit_depths():
    """不同位深示例"""
    print("\n=== 不同位深示例 ===\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for bits in [8, 16, 24, 32]:
            filepath = os.path.join(temp_dir, f'{bits}bit.wav')
            
            writer = WavWriter(filepath, sample_rate=44100, bits_per_sample=bits)
            writer.add_sine_wave(440, 100, 0.5)
            info = writer.write()
            
            file_size = os.path.getsize(filepath)
            print(f"{bits}-bit WAV:")
            print(f"  文件大小: {file_size} 字节")
            print(f"  每样本字节数: {bits // 8}")


def example_chained_operations():
    """链式操作示例"""
    print("\n=== 链式操作示例 ===\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, 'chained.wav')
        
        # 使用链式调用创建复杂音频
        info = (WavWriter(filepath, sample_rate=44100)
                .add_sine_wave(440, 200, 0.5)  # A4
                .add_silence(100)              # 静音
                .add_sine_wave(880, 200, 0.5)  # A5
                .add_silence(100)              # 静音
                .add_sine_wave(660, 200, 0.5)  # E5
                .write())
        
        print(f"创建多段音频:")
        print(f"  总时长: {info.duration:.3f} 秒")
        print(f"  样本数: {info.num_samples}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("WAV 工具集使用示例")
    print("=" * 60)
    
    example_basic_read_write()
    example_sine_wave()
    example_stereo_audio()
    example_audio_processing()
    example_fade_effects()
    example_silence_detection()
    example_audio_mixing()
    example_resampling()
    example_bit_depths()
    example_chained_operations()
    
    print("\n" + "=" * 60)
    print("所有示例完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()