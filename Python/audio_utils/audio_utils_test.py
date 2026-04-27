"""
Audio Utilities Test Suite
音频工具函数测试套件

覆盖场景:
- WAV/AIFF/AU 文件读写
- 音频信息提取
- 音量调整
- 淡入淡出效果
- 音频拼接
- 片段提取
- 声道转换
- 正弦波生成
- 静音检测
- 音频标准化

Author: AllToolkit
Version: 1.0.0
"""

import os
import sys
import tempfile
import shutil
import math
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    AudioInfo,
    AudioUtilsError,
    UnsupportedFormatError,
    InvalidAudioError,
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


def create_test_wav(filepath: str, duration: float = 1.0, frequency: float = 440.0,
                    channels: int = 1, framerate: int = 44100) -> str:
    """创建测试 WAV 文件"""
    data = generate_sine_wave(frequency, duration, framerate, channels=channels)
    write_audio(filepath, data, channels=channels, sample_width=2, framerate=framerate)
    return filepath


class TestAudioInfo:
    """音频信息测试"""
    
    def test_get_audio_info_wav(self, tmp_path):
        """测试获取 WAV 文件信息"""
        test_file = tmp_path / "test.wav"
        create_test_wav(str(test_file), duration=2.0, framerate=44100)
        
        info = get_audio_info(test_file)
        
        assert info.format == 'WAV'
        assert info.channels == 1
        assert info.sample_width == 2
        assert info.framerate == 44100
        assert abs(info.duration - 2.0) < 0.01
        assert info.frames == int(2.0 * 44100)
    
    def test_get_audio_info_nonexistent(self, tmp_path):
        """测试获取不存在文件的信息"""
        test_file = tmp_path / "nonexistent.wav"
        
        try:
            get_audio_info(test_file)
            assert False, "Should raise FileNotFoundError"
        except FileNotFoundError:
            pass
    
    def test_get_audio_info_unsupported_format(self, tmp_path):
        """测试不支持的格式"""
        test_file = tmp_path / "test.mp3"
        test_file.write_bytes(b"fake mp3")
        
        try:
            get_audio_info(test_file)
            assert False, "Should raise UnsupportedFormatError"
        except UnsupportedFormatError:
            pass


class TestReadWrite:
    """读写测试"""
    
    def test_write_and_read_wav(self, tmp_path):
        """测试 WAV 文件写入和读取"""
        test_file = tmp_path / "test.wav"
        
        # 生成测试数据
        original_data = generate_sine_wave(440.0, 1.0, 44100)
        
        # 写入
        success = write_audio(test_file, original_data, 
                             channels=1, sample_width=2, framerate=44100)
        assert success is True
        
        # 读取
        read_data, ch, sw, fr = read_audio(test_file)
        
        assert ch == 1
        assert sw == 2
        assert fr == 44100
        assert len(read_data) == len(original_data)
    
    def test_write_auto_create_dirs(self, tmp_path):
        """测试自动创建目录"""
        test_file = tmp_path / "subdir" / "nested" / "test.wav"
        
        data = generate_sine_wave(440.0, 0.5)
        success = write_audio(test_file, data, channels=1, sample_width=2, framerate=44100)
        
        assert success is True
        assert test_file.exists()
    
    def test_read_stereo_audio(self, tmp_path):
        """测试读取立体声音频"""
        test_file = tmp_path / "stereo.wav"
        
        data = generate_sine_wave(440.0, 1.0, channels=2)
        write_audio(test_file, data, channels=2, sample_width=2, framerate=44100)
        
        read_data, ch, sw, fr = read_audio(test_file)
        
        assert ch == 2
        assert len(read_data) == len(data)


class TestVolumeAdjustment:
    """音量调整测试"""
    
    def test_adjust_volume_increase(self, tmp_path):
        """测试音量放大"""
        input_file = tmp_path / "input.wav"
        output_file = tmp_path / "output.wav"
        
        create_test_wav(input_file, duration=1.0)
        
        original_peak = get_peak_amplitude(input_file)
        
        success = adjust_volume(input_file, output_file, factor=2.0)
        assert success is True
        
        new_peak = get_peak_amplitude(output_file)
        # 峰值应该接近原来的 2 倍（可能因为削波而略低）
        assert new_peak > original_peak
    
    def test_adjust_volume_decrease(self, tmp_path):
        """测试音量衰减"""
        input_file = tmp_path / "input.wav"
        output_file = tmp_path / "output.wav"
        
        create_test_wav(input_file, duration=1.0)
        
        original_peak = get_peak_amplitude(input_file)
        
        success = adjust_volume(input_file, output_file, factor=0.5)
        assert success is True
        
        new_peak = get_peak_amplitude(output_file)
        assert abs(new_peak - original_peak * 0.5) < 0.01
    
    def test_adjust_volume_silence(self, tmp_path):
        """测试静音（因子=0）"""
        input_file = tmp_path / "input.wav"
        output_file = tmp_path / "output.wav"
        
        create_test_wav(input_file, duration=1.0)
        
        success = adjust_volume(input_file, output_file, factor=0.0)
        assert success is True
        
        new_peak = get_peak_amplitude(output_file)
        assert new_peak == 0.0


class TestFadeEffects:
    """淡入淡出效果测试"""
    
    def test_fade_in(self, tmp_path):
        """测试淡入效果"""
        input_file = tmp_path / "input.wav"
        output_file = tmp_path / "output.wav"
        
        create_test_wav(input_file, duration=2.0)
        
        success = fade_in(input_file, output_file, duration=1.0)
        assert success is True
        
        # 淡入后开头应该更安静
        info = get_audio_info(output_file)
        assert abs(info.duration - 2.0) < 0.01
    
    def test_fade_out(self, tmp_path):
        """测试淡出效果"""
        input_file = tmp_path / "input.wav"
        output_file = tmp_path / "output.wav"
        
        create_test_wav(input_file, duration=2.0)
        
        success = fade_out(input_file, output_file, duration=1.0)
        assert success is True
        
        info = get_audio_info(output_file)
        assert abs(info.duration - 2.0) < 0.01


class TestConcatenation:
    """音频拼接测试"""
    
    def test_concatenate_two_files(self, tmp_path):
        """测试拼接两个文件"""
        file1 = tmp_path / "part1.wav"
        file2 = tmp_path / "part2.wav"
        output = tmp_path / "combined.wav"
        
        create_test_wav(file1, duration=1.0, frequency=440.0)
        create_test_wav(file2, duration=1.0, frequency=880.0)
        
        success = concatenate_audio([file1, file2], output)
        assert success is True
        
        info = get_audio_info(output)
        assert abs(info.duration - 2.0) < 0.01
    
    def test_concatenate_multiple_files(self, tmp_path):
        """测试拼接多个文件"""
        files = []
        for i in range(5):
            f = tmp_path / f"part{i}.wav"
            create_test_wav(f, duration=0.5)
            files.append(f)
        
        output = tmp_path / "combined.wav"
        success = concatenate_audio(files, output)
        assert success is True
        
        info = get_audio_info(output)
        assert abs(info.duration - 2.5) < 0.01
    
    def test_concatenate_empty_list(self, tmp_path):
        """测试空列表"""
        output = tmp_path / "output.wav"
        success = concatenate_audio([], output)
        assert success is False
    
    def test_concatenate_mismatched_params(self, tmp_path):
        """测试参数不匹配"""
        file1 = tmp_path / "file1.wav"
        file2 = tmp_path / "file2.wav"
        output = tmp_path / "output.wav"
        
        create_test_wav(file1, duration=1.0, framerate=44100)
        create_test_wav(file2, duration=1.0, framerate=22050)  # 不同采样率
        
        success = concatenate_audio([file1, file2], output)
        assert success is False


class TestSegmentExtraction:
    """片段提取测试"""
    
    def test_extract_middle_segment(self, tmp_path):
        """测试提取中间片段"""
        input_file = tmp_path / "input.wav"
        output_file = tmp_path / "output.wav"
        
        create_test_wav(input_file, duration=10.0)
        
        success = extract_segment(input_file, output_file, 
                                  start_time=3.0, end_time=5.0)
        assert success is True
        
        info = get_audio_info(output_file)
        assert abs(info.duration - 2.0) < 0.01
    
    def test_extract_full_segment(self, tmp_path):
        """测试提取完整片段"""
        input_file = tmp_path / "input.wav"
        output_file = tmp_path / "output.wav"
        
        create_test_wav(input_file, duration=5.0)
        
        success = extract_segment(input_file, output_file, 
                                  start_time=0.0, end_time=5.0)
        assert success is True
        
        info1 = get_audio_info(input_file)
        info2 = get_audio_info(output_file)
        assert abs(info1.duration - info2.duration) < 0.01
    
    def test_extract_invalid_range(self, tmp_path):
        """测试无效范围"""
        input_file = tmp_path / "input.wav"
        output_file = tmp_path / "output.wav"
        
        create_test_wav(input_file, duration=5.0)
        
        # start > end
        success = extract_segment(input_file, output_file, 
                                  start_time=5.0, end_time=3.0)
        assert success is False


class TestChannelConversion:
    """声道转换测试"""
    
    def test_stereo_to_mono(self, tmp_path):
        """测试立体声转单声道"""
        input_file = tmp_path / "stereo.wav"
        output_file = tmp_path / "mono.wav"
        
        data = generate_sine_wave(440.0, 1.0, channels=2)
        write_audio(input_file, data, channels=2, sample_width=2, framerate=44100)
        
        success = convert_to_mono(input_file, output_file)
        assert success is True
        
        info = get_audio_info(output_file)
        assert info.channels == 1
    
    def test_mono_to_mono(self, tmp_path):
        """测试单声道转单声道（应该直接复制）"""
        input_file = tmp_path / "mono.wav"
        output_file = tmp_path / "mono2.wav"
        
        create_test_wav(input_file, duration=1.0)
        
        success = convert_to_mono(input_file, output_file)
        assert success is True
        
        info1 = get_audio_info(input_file)
        info2 = get_audio_info(output_file)
        assert info1.channels == info2.channels == 1


class TestReverse:
    """反转测试"""
    
    def test_reverse_audio(self, tmp_path):
        """测试音频反转"""
        input_file = tmp_path / "input.wav"
        output_file = tmp_path / "reversed.wav"
        
        create_test_wav(input_file, duration=2.0)
        
        success = reverse_audio(input_file, output_file)
        assert success is True
        
        info1 = get_audio_info(input_file)
        info2 = get_audio_info(output_file)
        assert abs(info1.duration - info2.duration) < 0.01


class TestSineWaveGeneration:
    """正弦波生成测试"""
    
    def test_generate_440hz(self):
        """测试生成 440Hz 正弦波"""
        data = generate_sine_wave(440.0, 1.0, framerate=44100)
        
        # 1 秒 44100Hz 16-bit 单声道 = 44100 * 2 = 88200 bytes
        assert len(data) == 88200
    
    def test_generate_stereo(self):
        """测试生成立体声"""
        data = generate_sine_wave(440.0, 1.0, channels=2)
        
        # 立体声数据应该是单声道的 2 倍
        mono_data = generate_sine_wave(440.0, 1.0, channels=1)
        assert len(data) == len(mono_data) * 2
    
    def test_generate_different_sample_widths(self):
        """测试不同采样宽度"""
        for sw in [1, 2, 4]:
            data = generate_sine_wave(440.0, 0.1, sample_width=sw)
            expected_len = int(0.1 * 44100) * sw
            assert len(data) == expected_len, f"Failed for sample_width={sw}"
    
    def test_generate_invalid_sample_width(self):
        """测试无效采样宽度"""
        try:
            generate_sine_wave(440.0, 1.0, sample_width=3)
            assert False, "Should raise ValueError"
        except ValueError:
            pass


class TestSilenceDetection:
    """静音检测测试"""
    
    def test_detect_silence_in_tone(self, tmp_path):
        """测试在纯音中检测静音（应该没有）"""
        test_file = tmp_path / "tone.wav"
        create_test_wav(test_file, duration=2.0, frequency=440.0)
        
        # 使用较低的阈值，避免检测到正弦波的过零点
        silences = detect_silence(test_file, threshold=10)
        
        # 纯音不应该被检测为静音（或者只有极短的过零点）
        # 允许极短的"静音"（过零点），但总时长应该小于 10ms
        total_silence = sum(end - start for start, end in silences)
        assert total_silence < 0.01  # 小于 10ms
    
    def test_detect_silence_in_silent_file(self, tmp_path):
        """测试在静音文件中检测静音"""
        test_file = tmp_path / "silent.wav"
        
        # 创建完全静音的文件
        data = b'\x00' * 88200  # 1 秒静音
        write_audio(test_file, data, channels=1, sample_width=2, framerate=44100)
        
        silences = detect_silence(test_file, threshold=100)
        
        # 应该检测到静音
        assert len(silences) > 0


class TestPeakAmplitude:
    """峰值振幅测试"""
    
    def test_peak_amplitude_sine_wave(self, tmp_path):
        """测试正弦波峰值"""
        test_file = tmp_path / "sine.wav"
        
        # 生成振幅为 0.5 的正弦波
        data = generate_sine_wave(440.0, 1.0, amplitude=0.5)
        write_audio(test_file, data, channels=1, sample_width=2, framerate=44100)
        
        peak = get_peak_amplitude(test_file)
        
        # 峰值应该接近 0.5
        assert 0.45 < peak < 0.55
    
    def test_peak_amplitude_silence(self, tmp_path):
        """测试静音峰值"""
        test_file = tmp_path / "silent.wav"
        
        data = b'\x00' * 88200
        write_audio(test_file, data, channels=1, sample_width=2, framerate=44100)
        
        peak = get_peak_amplitude(test_file)
        assert peak == 0.0


class TestNormalization:
    """标准化测试"""
    
    def test_normalize_audio(self, tmp_path):
        """测试音频标准化"""
        input_file = tmp_path / "input.wav"
        output_file = tmp_path / "normalized.wav"
        
        # 生成低振幅音频
        data = generate_sine_wave(440.0, 1.0, amplitude=0.1)
        write_audio(input_file, data, channels=1, sample_width=2, framerate=44100)
        
        original_peak = get_peak_amplitude(input_file)
        assert original_peak < 0.2  # 确认原始峰值较低
        
        success = normalize_audio(input_file, output_file, target_peak=0.9)
        assert success is True
        
        new_peak = get_peak_amplitude(output_file)
        # 标准化后峰值应该接近 0.9
        assert 0.85 < new_peak < 0.95


class TestCreateTone:
    """音调创建测试"""
    
    def test_create_tone(self, tmp_path):
        """测试创建音调"""
        output_file = tmp_path / "tone.wav"
        
        success = create_tone(output_file, frequency=1000.0, duration=0.5)
        assert success is True
        
        info = get_audio_info(output_file)
        assert info.format == 'WAV'
        assert abs(info.duration - 0.5) < 0.01


class TestSplitStereo:
    """立体声分离测试"""
    
    def test_split_stereo(self, tmp_path):
        """测试分离立体声"""
        input_file = tmp_path / "stereo.wav"
        left_file = tmp_path / "left.wav"
        right_file = tmp_path / "right.wav"
        
        # 创建左右声道不同的立体声
        data = generate_sine_wave(440.0, 1.0, channels=2)
        write_audio(input_file, data, channels=2, sample_width=2, framerate=44100)
        
        success = split_stereo(input_file, left_file, right_file)
        assert success is True
        
        # 验证输出都是单声道
        left_info = get_audio_info(left_file)
        right_info = get_audio_info(right_file)
        
        assert left_info.channels == 1
        assert right_info.channels == 1
        assert abs(left_info.duration - 1.0) < 0.01
        assert abs(right_info.duration - 1.0) < 0.01
    
    def test_split_mono_fails(self, tmp_path):
        """测试分离单声道应该失败"""
        input_file = tmp_path / "mono.wav"
        left_file = tmp_path / "left.wav"
        right_file = tmp_path / "right.wav"
        
        create_test_wav(input_file, duration=1.0)
        
        success = split_stereo(input_file, left_file, right_file)
        assert success is False


def run_all_tests():
    """运行所有测试"""
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        test_classes = [
            TestAudioInfo,
            TestReadWrite,
            TestVolumeAdjustment,
            TestFadeEffects,
            TestConcatenation,
            TestSegmentExtraction,
            TestChannelConversion,
            TestReverse,
            TestSineWaveGeneration,
            TestSilenceDetection,
            TestPeakAmplitude,
            TestNormalization,
            TestCreateTone,
            TestSplitStereo,
        ]
        
        total_tests = 0
        passed_tests = 0
        failed_tests = []
        
        for test_class in test_classes:
            instance = test_class()
            for method_name in dir(instance):
                if method_name.startswith('test_'):
                    total_tests += 1
                    try:
                        method = getattr(instance, method_name)
                        # 检查方法是否需要 tmp_path 参数
                        import inspect
                        sig = inspect.signature(method)
                        if 'tmp_path' in sig.parameters:
                            method(tmp_path)
                        else:
                            method()
                        passed_tests += 1
                        print(f"✓ {test_class.__name__}.{method_name}")
                    except Exception as e:
                        failed_tests.append((f"{test_class.__name__}.{method_name}", str(e)))
                        print(f"✗ {test_class.__name__}.{method_name}: {e}")
        
        print(f"\n{'='*60}")
        print(f"测试结果：{passed_tests}/{total_tests} 通过")
        if failed_tests:
            print(f"\n失败的测试:")
            for name, error in failed_tests:
                print(f"  - {name}: {error}")
        else:
            print("所有测试通过！✓")
        
        return len(failed_tests) == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
