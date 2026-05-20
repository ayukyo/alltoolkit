"""
摩尔斯电码工具测试模块

测试覆盖:
- 文本编码
- 电码解码
- 音频生成
- 配置选项
- 边界值和异常处理
"""

import sys
import os
import tempfile
import wave
import struct

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from morse_utils.mod import (
    MorseConfig, MorseEncoder, MorseDecoder, MorseAudioGenerator,
    MorseUtils, MORSE_CODE, MORSE_DECODE, MORSE_ABBREVIATIONS,
    encode, decode, generate_audio, save_audio, get_morse_table, get_abbreviations
)


class TestResult:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_equal(self, actual, expected, msg=""):
        if actual == expected:
            self.passed += 1
            return True
        else:
            self.failed += 1
            error = f"断言失败: {msg}\n  期望: {expected}\n  实际: {actual}"
            self.errors.append(error)
            return False
    
    def assert_true(self, condition, msg=""):
        if condition:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"断言失败 (应为真): {msg}")
            return False
    
    def assert_false(self, condition, msg=""):
        if not condition:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"断言失败 (应为假): {msg}")
            return False
    
    def assert_in(self, item, container, msg=""):
        if item in container:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"断言失败 ({item} 应在容器中): {msg}")
            return False
    
    def assert_greater(self, actual, expected, msg=""):
        if actual > expected:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"断言失败 ({actual} 应大于 {expected}): {msg}")
            return False
    
    def assert_is_instance(self, obj, cls, msg=""):
        if isinstance(obj, cls):
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"断言失败 ({type(obj)} 应是 {cls}): {msg}")
            return False
    
    def assert_raises(self, exception_type, func, msg=""):
        try:
            func()
            self.failed += 1
            self.errors.append(f"断言失败 (应抛出 {exception_type.__name__}): {msg}")
            return False
        except exception_type:
            self.passed += 1
            return True
    
    def print_summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"测试结果: {self.passed} 通过, {self.failed} 失败 (共 {total} 个)")
        if self.errors:
            print(f"\n失败详情:")
            for error in self.errors[:10]:  # 只显示前10个错误
                print(f"  - {error}")
            if len(self.errors) > 10:
                print(f"  ... 还有 {len(self.errors) - 10} 个错误")
        print('='*60)
        return self.failed == 0


result = TestResult()


def test_morse_code_table():
    """测试摩尔斯电码表完整性"""
    print("\n--- 测试摩尔斯电码表完整性 ---")
    
    # 测试字母完整
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for letter in letters:
        result.assert_in(letter, MORSE_CODE, f"字母 {letter} 应在电码表中")
    
    # 测试数字完整
    digits = '0123456789'
    for digit in digits:
        result.assert_in(digit, MORSE_CODE, f"数字 {digit} 应在电码表中")
    
    # 测试常用标点
    punctuation = '.,?\'!/()&:;=+-_"$@'
    for punc in punctuation:
        result.assert_in(punc, MORSE_CODE, f"标点 {punc} 应在电码表中")
    
    # 测试反向映射
    result.assert_greater(len(MORSE_DECODE), 60, "反向映射表应大于 60")
    
    # 测试常用缩写
    result.assert_in('SOS', MORSE_ABBREVIATIONS, "SOS 应在缩写表中")
    result.assert_in('CQ', MORSE_ABBREVIATIONS, "CQ 应在缩写表中")


def test_basic_encoding():
    """测试基本编码功能"""
    print("\n--- 测试基本编码功能 ---")
    
    encoder = MorseEncoder()
    
    # 测试单个字母
    result.assert_equal(encoder.encode('A'), '.-', "A 应编码为 .-")
    result.assert_equal(encoder.encode('B'), '-...', "B 应编码为 -...")
    result.assert_equal(encoder.encode('E'), '.', "E 应编码为 .")
    result.assert_equal(encoder.encode('T'), '-', "T 应编码为 -")
    
    # 测试单个数字
    result.assert_equal(encoder.encode('0'), '-----', "0 应编码为 -----")
    result.assert_equal(encoder.encode('1'), '.----', "1 应编码为 .----")
    result.assert_equal(encoder.encode('9'), '----.', "9 应编码为 ----.")
    
    # 测试单词
    result.assert_equal(encoder.encode('SOS'), '... --- ...', "SOS 应正确编码")
    result.assert_equal(encoder.encode('HELLO'), '.... . .-.. .-.. ---', "HELLO 应正确编码")
    
    # 测试句子
    result.assert_equal(encoder.encode('HELLO WORLD'), 
                       '.... . .-.. .-.. --- / .-- --- .-. .-.. -..', 
                       "HELLO WORLD 应正确编码")


def test_basic_decoding():
    """测试基本解码功能"""
    print("\n--- 测试基本解码功能 ---")
    
    decoder = MorseDecoder()
    
    # 测试单个字母
    result.assert_equal(decoder.decode('.-'), 'A', ".- 应解码为 A")
    result.assert_equal(decode('-...'), 'B', "-... 应解码为 B")
    
    # 测试单词
    result.assert_equal(decoder.decode('... --- ...'), 'SOS', "... --- ... 应解码为 SOS")
    result.assert_equal(decoder.decode('.... . .-.. .-.. ---'), 'HELLO', 
                       "应解码为 HELLO")
    
    # 测试句子
    result.assert_equal(decoder.decode('.... . .-.. .-.. --- / .-- --- .-. .-.. -..'), 
                       'HELLO WORLD', "应解码为 HELLO WORLD")


def test_round_trip():
    """测试编码解码往返"""
    print("\n--- 测试编码解码往返 ---")
    
    utils = MorseUtils()
    
    test_texts = [
        'SOS',
        'HELLO',
        'WORLD',
        'MORSE CODE',
        'ABC123',
        'TEST 123',
        'HELLO WORLD',
    ]
    
    for text in test_texts:
        morse = utils.encode(text)
        decoded = utils.decode(morse)
        result.assert_equal(decoded, text.upper(), 
                           f"'{text}' 编码解码往返应一致")


def test_case_insensitivity():
    """测试大小写不敏感"""
    print("\n--- 测试大小写不敏感 ---")
    
    encoder = MorseEncoder()
    
    result.assert_equal(encoder.encode('a'), encoder.encode('A'), "a 和 A 应编码相同")
    result.assert_equal(encoder.encode('hello'), encoder.encode('HELLO'), 
                       "hello 和 HELLO 应编码相同")
    result.assert_equal(encoder.encode('Hello World'), encoder.encode('HELLO WORLD'),
                       "Hello World 和 HELLO WORLD 应编码相同")


def test_special_characters():
    """测试特殊字符处理"""
    print("\n--- 测试特殊字符处理 ---")
    
    encoder = MorseEncoder()
    
    # 测试标点符号
    result.assert_equal(encoder.encode('.'), '.-.-.-', ". 应编码为 .-.-.-")
    result.assert_equal(encoder.encode(','), '--..--', ", 应编码为 --..--")
    result.assert_equal(encoder.encode('?'), '..--..', "? 应编码为 ..--..")
    
    # 测试标点解码
    decoder = MorseDecoder()
    result.assert_equal(decoder.decode('.-.-.-'), '.', ".-.-.- 应解码为 .")
    result.assert_equal(decoder.decode('--..--'), ',', "--..-- 应解码为 ,")


def test_unknown_characters():
    """测试未知字符处理"""
    print("\n--- 测试未知字符处理 ---")
    
    # 默认配置 - 替换未知字符
    encoder = MorseEncoder()
    # 两个中文字符会分别替换为两个 ?，用字母分隔符分隔
    result.assert_equal(encoder.encode('HELLO世界'), 
                       '.... . .-.. .-.. --- ? ?', "未知字符应替换为 ?")
    
    # 忽略未知字符
    config = MorseConfig(ignore_unknown=True)
    encoder = MorseEncoder(config)
    result.assert_equal(encoder.encode('HELLO世界'), '.... . .-.. .-.. ---', 
                       "应忽略未知字符")


def test_empty_input():
    """测试空输入"""
    print("\n--- 测试空输入 ---")
    
    encoder = MorseEncoder()
    decoder = MorseDecoder()
    
    result.assert_equal(encoder.encode(''), '', "空字符串应返回空")
    result.assert_equal(encoder.encode('   '), '', "纯空格应返回空")
    result.assert_equal(decoder.decode(''), '', "空摩尔斯码应返回空")
    result.assert_equal(decoder.decode('   '), '', "纯空格应返回空")


def test_alternative_symbols():
    """测试替代符号"""
    print("\n--- 测试替代符号 ---")
    
    decoder = MorseDecoder()
    
    # 使用圆点和长划
    result.assert_equal(decoder.decode('•—'), 'A', "圆点符号应被识别")
    result.assert_equal(decoder.decode('••• ——— •••'), 'SOS', "替代符号应正确解码")


def test_config_options():
    """测试配置选项"""
    print("\n--- 测试配置选项 ---")
    
    # 自定义符号
    config = MorseConfig(dot_symbol='*', dash_symbol='_')
    encoder = MorseEncoder(config)
    
    result.assert_equal(encoder.encode('A'), '*_', "应使用自定义符号")
    result.assert_equal(encoder.encode('SOS'), '*** ___ ***', "应使用自定义符号")
    
    # 自定义分隔符
    config2 = MorseConfig(letter_separator=' | ', word_separator=' / ')
    encoder2 = MorseEncoder(config2)
    result.assert_equal(encoder2.encode('AB'), '.- | -...', "应使用自定义字母分隔符")


def test_config_validation():
    """测试配置验证"""
    print("\n--- 测试配置验证 ---")
    
    # 频率必须为正
    result.assert_raises(ValueError, lambda: MorseConfig(frequency=0))
    result.assert_raises(ValueError, lambda: MorseConfig(frequency=-100))
    
    # 采样率必须为正
    result.assert_raises(ValueError, lambda: MorseConfig(sample_rate=0))
    result.assert_raises(ValueError, lambda: MorseConfig(sample_rate=-44100))
    
    # 点持续时间必须为正
    result.assert_raises(ValueError, lambda: MorseConfig(dot_duration=0))
    result.assert_raises(ValueError, lambda: MorseConfig(dot_duration=-0.1))


def test_audio_generation():
    """测试音频生成"""
    print("\n--- 测试音频生成 ---")
    
    generator = MorseAudioGenerator()
    
    # 生成音频数据
    audio = generator.generate_audio('SOS')
    result.assert_is_instance(audio, bytes, "音频数据应为 bytes 类型")
    result.assert_greater(len(audio), 44, "音频数据应包含 WAV 头 (至少 44 字节)")
    
    # 验证 WAV 格式
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        filepath = f.name
    
    try:
        generator.save_audio('SOS', filepath)
        
        # 验证文件
        with wave.open(filepath, 'rb') as wav:
            result.assert_equal(wav.getnchannels(), 1, "应为单声道")
            result.assert_equal(wav.getsampwidth(), 2, "应为 16 位")
            result.assert_equal(wav.getframerate(), 44100, "采样率应为 44100")
        
        # 验证文件大小
        file_size = os.path.getsize(filepath)
        result.assert_greater(file_size, 44, "文件应有数据")
    finally:
        os.unlink(filepath)


def test_audio_timing():
    """测试音频时序"""
    print("\n--- 测试音频时序 ---")
    
    config = MorseConfig(dot_duration=0.05)  # 50ms 点
    generator = MorseAudioGenerator(config)
    
    # 'E' 只有一个点
    audio_e = generator.generate_audio('E')
    # 'T' 只有一个划 (3倍点长度)
    audio_t = generator.generate_audio('T')
    
    # 划应该比点长
    result.assert_greater(len(audio_t), len(audio_e), "划应比点长")


def test_duration_calculation():
    """测试持续时间计算"""
    print("\n--- 测试持续时间计算 ---")
    
    utils = MorseUtils()
    
    # E = 一个点
    duration_e = utils.calculate_duration('E')
    result.assert_greater(duration_e, 0, "E 的持续时间应大于 0")
    
    # T = 一个划，应该比 E 长
    duration_t = utils.calculate_duration('T')
    result.assert_greater(duration_t, duration_e, "T 应比 E 长")
    
    # 单词比字母长
    duration_sos = utils.calculate_duration('SOS')
    result.assert_greater(duration_sos, duration_e, "SOS 应比单个字母长")


def test_statistics():
    """测试统计功能"""
    print("\n--- 测试统计功能 ---")
    
    utils = MorseUtils()
    
    stats = utils.get_statistics('SOS')
    
    result.assert_equal(stats['original_text'], 'SOS', "原始文本应为 SOS")
    result.assert_equal(stats['morse_code'], '... --- ...', "电码应正确")
    result.assert_equal(stats['dot_count'], 6, "应有 6 个点")
    result.assert_equal(stats['dash_count'], 3, "应有 3 个划")
    result.assert_equal(stats['total_symbols'], 9, "共 9 个符号")
    result.assert_equal(stats['character_count'], 3, "3 个字符")
    result.assert_equal(stats['word_count'], 1, "1 个单词")
    result.assert_greater(stats['duration_seconds'], 0, "持续时间应大于 0")


def test_visualization():
    """测试可视化功能"""
    print("\n--- 测试可视化功能 ---")
    
    utils = MorseUtils()
    
    # 标准格式
    result.assert_equal(utils.visualize('SOS', style='standard'), '... --- ...',
                       "标准格式应正确")
    
    # 圆点格式
    dots = utils.visualize('SOS', style='dots')
    result.assert_in('•', dots, "圆点格式应包含 •")
    result.assert_in('—', dots, "圆点格式应包含 —")
    
    # 音效拟声
    sound = utils.visualize('SOS', style='sound')
    result.assert_in('di', sound, "音效格式应包含 di")
    result.assert_in('da', sound, "音效格式应包含 da")


def test_practice():
    """测试练习功能"""
    print("\n--- 测试练习功能 ---")
    
    utils = MorseUtils()
    
    # 指定字符练习
    practice = utils.practice('A')
    result.assert_equal(practice['character'], 'A', "字符应为 A")
    result.assert_equal(practice['morse_code'], '.-', "电码应为 .-")
    result.assert_in('description', practice, "应包含描述")
    
    # 随机字符练习
    practice_random = utils.practice()
    result.assert_in('character', practice_random, "应包含字符")
    result.assert_in('morse_code', practice_random, "应包含电码")
    result.assert_greater(len(practice_random['morse_code']), 0, "电码应非空")


def test_is_valid_morse():
    """测试摩尔斯电码验证"""
    print("\n--- 测试摩尔斯电码验证 ---")
    
    decoder = MorseDecoder()
    
    # 有效电码
    result.assert_true(decoder.is_valid_morse('... --- ...'), "SOS 是有效电码")
    result.assert_true(decoder.is_valid_morse('.-'), ".- 是有效电码")
    result.assert_true(decoder.is_valid_morse('.... . .-.. .-.. ---'), "HELLO 是有效电码")
    
    # 无效电码
    result.assert_false(decoder.is_valid_morse(''), "空字符串无效")
    result.assert_false(decoder.is_valid_morse('abc'), "包含无效字符")
    result.assert_false(decoder.is_valid_morse('...abc...'), "包含无效字符")


def test_encode_single_letter():
    """测试单字母编码"""
    print("\n--- 测试单字母编码 ---")
    
    encoder = MorseEncoder()
    
    # 有效字符
    result.assert_equal(encoder.encode_letter('A'), '.-', "A 应返回 .-")
    result.assert_equal(encoder.encode_letter('a'), '.-', "a 应返回 .-")
    result.assert_equal(encoder.encode_letter('1'), '.----', "1 应返回 .----")
    
    # 无效字符
    result.assert_equal(encoder.encode_letter('中'), None, "中文字符应返回 None")
    
    # 多字符应报错
    result.assert_raises(ValueError, lambda: encoder.encode_letter('AB'))


def test_decode_single_letter():
    """测试单字母解码"""
    print("\n--- 测试单字母解码 ---")
    
    decoder = MorseDecoder()
    
    result.assert_equal(decoder.decode_letter('.-'), 'A', ".- 应返回 A")
    result.assert_equal(decoder.decode_letter('... --- ...'), None, 
                       "多字母电码应返回 None")
    result.assert_equal(decoder.decode_letter('invalid'), None, 
                       "无效电码应返回 None")


def test_convenience_functions():
    """测试便捷函数"""
    print("\n--- 测试便捷函数 ---")
    
    # 编码函数
    result.assert_equal(encode('HELLO'), '.... . .-.. .-.. ---', 
                       "encode 函数应正常工作")
    
    # 解码函数
    result.assert_equal(decode('.... . .-.. .-.. ---'), 'HELLO',
                       "decode 函数应正常工作")
    
    # 音频函数
    audio = generate_audio('SOS')
    result.assert_is_instance(audio, bytes, "generate_audio 应返回 bytes")
    
    # 表获取函数
    table = get_morse_table()
    result.assert_is_instance(table, dict, "get_morse_table 应返回 dict")
    result.assert_in('A', table, "表应包含 A")
    
    abbreviations = get_abbreviations()
    result.assert_is_instance(abbreviations, dict, "get_abbreviations 应返回 dict")
    result.assert_in('SOS', abbreviations, "缩写表应包含 SOS")


def test_unicode_handling():
    """测试 Unicode 处理"""
    print("\n--- 测试 Unicode 处理 ---")
    
    encoder = MorseEncoder()
    
    # Unicode 字符应被替换或忽略
    result.assert_equal(encoder.encode('HELLO你好'), 
                       '.... . .-.. .-.. --- ? ?', 
                       "中文字符应替换为 ?")
    
    # 忽略 Unicode
    config = MorseConfig(ignore_unknown=True)
    encoder2 = MorseEncoder(config)
    result.assert_equal(encoder2.encode('HELLO你好世界'), 
                       '.... . .-.. .-.. ---', 
                       "应忽略未知字符")


def test_whitespace_handling():
    """测试空白处理"""
    print("\n--- 测试空白处理 ---")
    
    encoder = MorseEncoder()
    decoder = MorseDecoder()
    
    # 多个空格应合并
    result.assert_equal(encoder.encode('HELLO   WORLD'), 
                       '.... . .-.. .-.. --- / .-- --- .-. .-.. -..',
                       "多个空格应合并为一个单词分隔")
    
    # 前后空格
    result.assert_equal(encoder.encode('  HELLO  '), 
                       '.... . .-.. .-.. ---',
                       "前后空格应被忽略")


def test_long_text():
    """测试长文本"""
    print("\n--- 测试长文本 ---")
    
    encoder = MorseEncoder()
    decoder = MorseDecoder()
    
    # 长文本
    long_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG 1234567890"
    morse = encoder.encode(long_text)
    decoded = decoder.decode(morse)
    
    result.assert_equal(decoded, long_text, "长文本应正确往返")
    result.assert_greater(len(morse), 100, "长文本电码应较长")


def test_abbreviations():
    """测试常用缩写"""
    print("\n--- 测试常用缩写 ---")
    
    abbreviations = get_abbreviations()
    
    # 验证缩写
    result.assert_equal(abbreviations['SOS'], '... --- ...', "SOS 电码正确")
    result.assert_equal(abbreviations['CQ'], '-.-. --.-', "CQ 电码正确")
    result.assert_equal(abbreviations['73'], '--... ...--', "73 电码正确")
    
    # 验证缩写是有效摩尔斯电码
    decoder = MorseDecoder()
    for name, morse in abbreviations.items():
        result.assert_true(decoder.is_valid_morse(morse), 
                         f"{name} 应是有效电码")


def test_numbers():
    """测试数字编码解码"""
    print("\n--- 测试数字编码解码 ---")
    
    encoder = MorseEncoder()
    decoder = MorseDecoder()
    
    for i in range(10):
        digit = str(i)
        morse = encoder.encode(digit)
        decoded = decoder.decode(morse)
        result.assert_equal(decoded, digit, f"数字 {digit} 应正确往返")


def test_punctuation():
    """测试标点符号编码解码"""
    print("\n--- 测试标点符号编码解码 ---")
    
    encoder = MorseEncoder()
    decoder = MorseDecoder()
    
    punctuation_tests = [
        ('.', '.-.-.-'),
        (',', '--..--'),
        ('?', '..--..'),
        ('!', '-.-.--'),
        ('/', '-..-.'),
        ('(', '-.--.'),
        (')', '-.--.-'),
        ('&', '.-...'),
        (':', '---...'),
        (';', '-.-.-.'),
        ('=', '-...-'),
        ('+', '.-.-.'),
        ('-', '-....-'),
        ('_', '..--.-'),
        ('"', '.-..-.'),
        ('$', '...-..-'),
        ('@', '.--.-.'),
    ]
    
    for char, expected_morse in punctuation_tests:
        morse = encoder.encode(char)
        result.assert_equal(morse, expected_morse, f"'{char}' 应编码为 {expected_morse}")
        
        decoded = decoder.decode(morse)
        result.assert_equal(decoded, char, f"'{morse}' 应解码为 '{char}'")


def test_morse_utils_class():
    """测试 MorseUtils 类"""
    print("\n--- 测试 MorseUtils 类 ---")
    
    utils = MorseUtils()
    
    # 测试所有方法
    result.assert_equal(utils.encode('TEST'), '- . ... -', "encode 方法")
    result.assert_equal(utils.decode('- . ... -'), 'TEST', "decode 方法")
    
    stats = utils.get_statistics('TEST')
    result.assert_is_instance(stats, dict, "get_statistics 应返回 dict")
    
    duration = utils.calculate_duration('TEST')
    result.assert_greater(duration, 0, "calculate_duration 应返回正数")
    
    result.assert_true(utils.is_valid_morse('.-'), "is_valid_morse 应返回 True")


def run_all_tests():
    """运行所有测试"""
    print("="*60)
    print("摩尔斯电码工具测试")
    print("="*60)
    
    # 运行所有测试
    test_morse_code_table()
    test_basic_encoding()
    test_basic_decoding()
    test_round_trip()
    test_case_insensitivity()
    test_special_characters()
    test_unknown_characters()
    test_empty_input()
    test_alternative_symbols()
    test_config_options()
    test_config_validation()
    test_audio_generation()
    test_audio_timing()
    test_duration_calculation()
    test_statistics()
    test_visualization()
    test_practice()
    test_is_valid_morse()
    test_encode_single_letter()
    test_decode_single_letter()
    test_convenience_functions()
    test_unicode_handling()
    test_whitespace_handling()
    test_long_text()
    test_abbreviations()
    test_numbers()
    test_punctuation()
    test_morse_utils_class()
    
    # 打印结果
    success = result.print_summary()
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(run_all_tests())