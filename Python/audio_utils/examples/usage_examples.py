"""
Audio Utilities Usage Examples
音频工具函数使用示例

本文件包含 audio_utils 模块的各种实用示例，
可直接运行或作为参考代码复用。

Author: AllToolkit
Version: 1.0.0
"""

import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    get_audio_info,
    read_audio,
    write_audio,
    adjust_volume,
    fade_in,
    fade_out,
    concatenate_audio,
    extract_segment,
    convert_to_mono,
    reverse_audio,
    generate_sine_wave,
    detect_silence,
    get_peak_amplitude,
    normalize_audio,
    create_tone,
    split_stereo,
)


def example_basic_info():
    """示例 1: 获取音频信息"""
    print("=" * 60)
    print("示例 1: 获取音频信息")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_file = Path(tmp_dir) / "sample.wav"
        
        # 创建测试音频
        create_tone(test_file, frequency=440.0, duration=2.0)
        
        # 获取信息
        info = get_audio_info(test_file)
        
        print(f"文件：{info.filepath}")
        print(f"格式：{info.format}")
        print(f"时长：{info.duration:.2f}秒")
        print(f"采样率：{info.framerate}Hz")
        print(f"声道数：{info.channels}")
        print(f"采样宽度：{info.sample_width}字节")
        print(f"总帧数：{info.frames}")
        print()


def example_create_tones():
    """示例 2: 创建音调"""
    print("=" * 60)
    print("示例 2: 创建音调（C 大调音阶）")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # C 大调音阶频率 (Hz)
        notes = {
            'C4': 261.63,
            'D4': 293.66,
            'E4': 329.63,
            'F4': 349.23,
            'G4': 392.00,
            'A4': 440.00,
            'B4': 493.88,
            'C5': 523.25,
        }
        
        note_files = []
        for note_name, frequency in notes.items():
            note_file = tmp_path / f"{note_name}.wav"
            create_tone(note_file, frequency=frequency, duration=0.5)
            note_files.append(note_file)
            print(f"✓ 创建 {note_name} ({frequency}Hz)")
        
        # 拼接成完整音阶
        scale_file = tmp_path / "scale.wav"
        concatenate_audio(note_files, scale_file)
        
        info = get_audio_info(scale_file)
        print(f"\n✓ 音阶文件已创建：{scale_file}")
        print(f"  总时长：{info.duration:.2f}秒")
        print()


def example_volume_adjustment():
    """示例 3: 音量调整"""
    print("=" * 60)
    print("示例 3: 音量调整")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # 创建原始音频
        original = tmp_path / "original.wav"
        create_tone(original, frequency=440.0, duration=1.0)
        
        original_peak = get_peak_amplitude(original)
        print(f"原始峰值：{original_peak:.2%}")
        
        # 放大 2 倍
        louder = tmp_path / "louder.wav"
        adjust_volume(original, louder, factor=2.0)
        print(f"放大 2 倍后峰值：{get_peak_amplitude(louder):.2%}")
        
        # 衰减到 50%
        quieter = tmp_path / "quieter.wav"
        adjust_volume(original, quieter, factor=0.5)
        print(f"衰减 50% 后峰值：{get_peak_amplitude(quieter):.2%}")
        
        # 静音
        silent = tmp_path / "silent.wav"
        adjust_volume(original, silent, factor=0.0)
        print(f"静音后峰值：{get_peak_amplitude(silent):.2%}")
        print()


def example_fade_effects():
    """示例 4: 淡入淡出效果"""
    print("=" * 60)
    print("示例 4: 淡入淡出效果")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # 创建原始音频
        original = tmp_path / "original.wav"
        create_tone(original, frequency=440.0, duration=5.0)
        
        # 添加淡入
        fade_in_file = tmp_path / "fade_in.wav"
        fade_in(original, fade_in_file, duration=2.0)
        print(f"✓ 添加 2 秒淡入：{fade_in_file}")
        
        # 添加淡出
        fade_out_file = tmp_path / "fade_out.wav"
        fade_out(original, fade_out_file, duration=2.0)
        print(f"✓ 添加 2 秒淡出：{fade_out_file}")
        
        # 同时添加淡入淡出
        both_file = tmp_path / "fade_both.wav"
        fade_in(original, both_file, duration=1.0)
        fade_out(both_file, both_file, duration=1.0)
        print(f"✓ 添加淡入淡出：{both_file}")
        print()


def example_segment_extraction():
    """示例 5: 提取音频片段"""
    print("=" * 60)
    print("示例 5: 提取音频片段")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # 创建 10 秒音频
        original = tmp_path / "original.wav"
        create_tone(original, frequency=440.0, duration=10.0)
        
        info = get_audio_info(original)
        print(f"原始音频时长：{info.duration:.2f}秒")
        
        # 提取中间 3 秒片段
        segment = tmp_path / "segment.wav"
        extract_segment(original, segment, start_time=3.0, end_time=6.0)
        
        seg_info = get_audio_info(segment)
        print(f"提取片段时长：{seg_info.duration:.2f}秒 (3.0s - 6.0s)")
        
        # 提取开头 2 秒
        intro = tmp_path / "intro.wav"
        extract_segment(original, intro, start_time=0.0, end_time=2.0)
        print(f"提取开头：{get_audio_info(intro).duration:.2f}秒")
        
        # 提取结尾 2 秒
        outro = tmp_path / "outro.wav"
        extract_segment(original, outro, start_time=8.0, end_time=10.0)
        print(f"提取结尾：{get_audio_info(outro).duration:.2f}秒")
        print()


def example_channel_conversion():
    """示例 6: 声道转换"""
    print("=" * 60)
    print("示例 6: 声道转换")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # 创建立体声音频
        stereo_data = generate_sine_wave(440.0, 2.0, channels=2)
        stereo_file = tmp_path / "stereo.wav"
        write_audio(stereo_file, stereo_data, channels=2, sample_width=2, framerate=44100)
        
        stereo_info = get_audio_info(stereo_file)
        print(f"立体声：{stereo_info.channels}声道，{stereo_info.duration:.2f}秒")
        
        # 转换为单声道
        mono_file = tmp_path / "mono.wav"
        convert_to_mono(stereo_file, mono_file)
        
        mono_info = get_audio_info(mono_file)
        print(f"单声道：{mono_info.channels}声道，{mono_info.duration:.2f}秒")
        
        # 分离左右声道
        left_file = tmp_path / "left.wav"
        right_file = tmp_path / "right.wav"
        split_stereo(stereo_file, left_file, right_file)
        
        print(f"左声道：{get_audio_info(left_file).channels}声道")
        print(f"右声道：{get_audio_info(right_file).channels}声道")
        print()


def example_audio_reversal():
    """示例 7: 音频反转"""
    print("=" * 60)
    print("示例 7: 音频反转（倒放效果）")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # 创建 ascending tone（频率递增的音调序列）
        original = tmp_path / "ascending.wav"
        files = []
        for freq in [440, 554, 659, 784]:  # A4, C#5, E5, G5
            f = tmp_path / f"tone_{freq}.wav"
            create_tone(f, frequency=freq, duration=0.5)
            files.append(f)
        
        concatenate_audio(files, original)
        print(f"原始音频：{get_audio_info(original).duration:.2f}秒（频率递增）")
        
        # 反转
        reversed_file = tmp_path / "reversed.wav"
        reverse_audio(original, reversed_file)
        print(f"反转音频：{get_audio_info(reversed_file).duration:.2f}秒（频率递减）")
        print()


def example_silence_detection():
    """示例 8: 静音检测"""
    print("=" * 60)
    print("示例 8: 静音检测")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # 创建带静音的音频：有声 - 静音 - 有声
        part1 = tmp_path / "part1.wav"
        silence = tmp_path / "silence.wav"
        part2 = tmp_path / "part2.wav"
        
        create_tone(part1, frequency=440.0, duration=2.0)
        
        # 创建静音片段
        silence_data = b'\x00' * 44100 * 2  # 1 秒静音
        write_audio(silence, silence_data, channels=1, sample_width=2, framerate=44100)
        
        create_tone(part2, frequency=880.0, duration=2.0)
        
        # 拼接
        combined = tmp_path / "combined.wav"
        concatenate_audio([part1, silence, part2], combined)
        
        # 检测静音
        silences = detect_silence(combined, threshold=100)
        
        print(f"检测到 {len(silences)} 个静音片段:")
        for i, (start, end) in enumerate(silences):
            duration = end - start
            print(f"  片段 {i+1}: {start:.2f}s - {end:.2f}s (时长：{duration:.2f}秒)")
        print()


def example_normalization():
    """示例 9: 音频标准化"""
    print("=" * 60)
    print("示例 9: 音频标准化")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # 创建低振幅音频
        original = tmp_path / "quiet.wav"
        quiet_data = generate_sine_wave(440.0, 2.0, amplitude=0.1)
        write_audio(original, quiet_data, channels=1, sample_width=2, framerate=44100)
        
        original_peak = get_peak_amplitude(original)
        print(f"原始峰值：{original_peak:.2%}")
        
        # 标准化到 90%
        normalized = tmp_path / "normalized.wav"
        normalize_audio(original, normalized, target_peak=0.9)
        
        new_peak = get_peak_amplitude(normalized)
        print(f"标准化后峰值：{new_peak:.2%}")
        print(f"增益：{new_peak/original_peak:.1f}x")
        print()


def example_ringtone_creation():
    """示例 10: 制作铃声"""
    print("=" * 60)
    print("示例 10: 制作铃声（完整流程）")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # 模拟"歌曲"：创建 30 秒音频
        song = tmp_path / "song.wav"
        files = []
        for i in range(30):
            f = tmp_path / f"sec_{i}.wav"
            freq = 440 + (i * 10)  # 频率递增
            create_tone(f, frequency=freq, duration=1.0)
            files.append(f)
        
        concatenate_audio(files, song)
        print(f"✓ 创建模拟歌曲：{get_audio_info(song).duration:.2f}秒")
        
        # 提取"副歌"部分（10-25 秒）
        chorus = tmp_path / "chorus.wav"
        extract_segment(song, chorus, start_time=10.0, end_time=25.0)
        print(f"✓ 提取副歌：{get_audio_info(chorus).duration:.2f}秒")
        
        # 标准化音量
        chorus_norm = tmp_path / "chorus_normalized.wav"
        normalize_audio(chorus, chorus_norm, target_peak=0.9)
        print(f"✓ 标准化音量：{get_peak_amplitude(chorus_norm):.2%}")
        
        # 添加淡入淡出
        ringtone = tmp_path / "ringtone.wav"
        fade_in(chorus_norm, ringtone, duration=1.0)
        fade_out(ringtone, ringtone, duration=2.0)
        print(f"✓ 添加淡入淡出：{get_audio_info(ringtone).duration:.2f}秒")
        
        print(f"\n🎵 铃声制作完成：{ringtone}")
        print()


def example_batch_processing():
    """示例 11: 批量处理"""
    print("=" * 60)
    print("示例 11: 批量处理音频文件")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # 创建多个测试文件
        for i in range(5):
            f = tmp_path / f"track_{i}.wav"
            # 不同振幅
            data = generate_sine_wave(440 + i*100, 1.0, amplitude=0.3 + i*0.1)
            write_audio(f, data, channels=1, sample_width=2, framerate=44100)
        
        print("批量处理前:")
        for f in sorted(tmp_path.glob("track_*.wav")):
            peak = get_peak_amplitude(f)
            print(f"  {f.name}: 峰值 {peak:.2%}")
        
        # 批量标准化
        print("\n批量标准化到 85%...")
        for f in sorted(tmp_path.glob("track_*.wav")):
            output = tmp_path / (f.stem + "_normalized.wav")
            normalize_audio(f, output, target_peak=0.85)
        
        print("\n批量处理后:")
        for f in sorted(tmp_path.glob("track_*_normalized.wav")):
            peak = get_peak_amplitude(f)
            print(f"  {f.name}: 峰值 {peak:.2%}")
        print()


def example_custom_waveform():
    """示例 12: 自定义波形生成"""
    print("=" * 60)
    print("示例 12: 自定义波形生成")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        import math
        
        # 生成方波
        def generate_square_wave(frequency, duration, framerate=44100, amplitude=0.5):
            """生成方波"""
            total_samples = int(duration * framerate)
            data = b''
            for i in range(total_samples):
                # 方波：正半周为 +amplitude，负半周为 -amplitude
                period = framerate / frequency
                value = amplitude if (i % period) < (period / 2) else -amplitude
                sample = int(value * 32767)
                data += sample.to_bytes(2, 'little', signed=True)
            return data
        
        # 生成锯齿波
        def generate_sawtooth_wave(frequency, duration, framerate=44100, amplitude=0.5):
            """生成锯齿波"""
            total_samples = int(duration * framerate)
            data = b''
            period = framerate / frequency
            for i in range(total_samples):
                # 锯齿波：线性从 -amplitude 上升到 +amplitude
                value = -amplitude + 2 * amplitude * ((i % period) / period)
                sample = int(value * 32767)
                data += sample.to_bytes(2, 'little', signed=True)
            return data
        
        # 生成方波
        square_data = generate_square_wave(440.0, 1.0)
        square_file = tmp_path / "square.wav"
        write_audio(square_file, square_data, channels=1, sample_width=2, framerate=44100)
        print(f"✓ 方波：{square_file}")
        
        # 生成锯齿波
        sawtooth_data = generate_sawtooth_wave(440.0, 1.0)
        sawtooth_file = tmp_path / "sawtooth.wav"
        write_audio(sawtooth_file, sawtooth_data, channels=1, sample_width=2, framerate=44100)
        print(f"✓ 锯齿波：{sawtooth_file}")
        
        # 生成三角波
        triangle_data = generate_sine_wave(440.0, 1.0)  # 用正弦波近似
        triangle_file = tmp_path / "sine.wav"
        write_audio(triangle_file, triangle_data, channels=1, sample_width=2, framerate=44100)
        print(f"✓ 正弦波：{triangle_file}")
        print()


def run_all_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Audio Utilities 使用示例")
    print("=" * 60 + "\n")
    
    examples = [
        example_basic_info,
        example_create_tones,
        example_volume_adjustment,
        example_fade_effects,
        example_segment_extraction,
        example_channel_conversion,
        example_audio_reversal,
        example_silence_detection,
        example_normalization,
        example_ringtone_creation,
        example_batch_processing,
        example_custom_waveform,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"示例出错：{e}")
            import traceback
            traceback.print_exc()
    
    print("=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()
