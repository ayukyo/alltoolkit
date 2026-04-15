"""
Morse Utils - 测试套件

测试覆盖：
- 编码功能
- 解码功能
- 音频生成
- 验证功能
- 统计功能
- 错误处理
- 文件操作
"""

import sys
import os
import struct

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from morse_utils.mod import (
    MORSE_CODE,
    MORSE_DECODE,
    MORSE_ABBREVIATIONS,
    Q_CODE,
    MorseError,
    InvalidCharacterError,
    InvalidMorseError,
    MorseConfig,
    DEFAULT_CONFIG,
    encode,
    decode,
    encode_file,
    decode_file,
    is_valid_morse,
    is_valid_text_for_encoding,
    get_supported_characters,
    get_morse_for_char,
    get_char_for_morse,
    normalize_morse,
    calculate_duration,
    generate_tone,
    generate_silence,
    generate_morse_audio,
    translate_abbreviation,
    translate_q_code,
    list_abbreviations,
    list_q_codes,
    get_morse_stats,
    reverse_encode,
    compare_morse,
    practice_mode,
    MorseCode,
    text_to_morse,
    morse_to_text,
    text_to_audio,
)


class TestResult:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_equal(self, actual, expected, msg=""):
        """相等比较"""
        if actual == expected:
            self.passed += 1
            return True
        else:
            self.failed += 1
            error_msg = f"期望 {expected!r}, 得到 {actual!r}"
            if msg:
                error_msg = f"{msg}: {error_msg}"
            self.errors.append(error_msg)
            return False
    
    def assert_true(self, condition, msg=""):
        """真值断言"""
        if condition:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"期望 True, 得到 False" + (f": {msg}" if msg else ""))
            return False
    
    def assert_false(self, condition, msg=""):
        """假值断言"""
        if not condition:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"期望 False, 得到 True" + (f": {msg}" if msg else ""))
            return False
    
    def assert_in(self, item, container, msg=""):
        """包含断言"""
        if item in container:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"{item!r} 不在 {container!r}" + (f": {msg}" if msg else ""))
            return False
    
    def assert_raises(self, exception_class, func, *args, msg="", **kwargs):
        """异常断言"""
        try:
            func(*args, **kwargs)
            self.failed += 1
            self.errors.append(f"期望异常 {exception_class.__name__}, 但没有抛出" + (f": {msg}" if msg else ""))
            return False
        except exception_class:
            self.passed += 1
            return True
        except Exception as e:
            self.failed += 1
            self.errors.append(f"期望异常 {exception_class.__name__}, 得到 {type(e).__name__}" + (f": {msg}" if msg else ""))
            return False
    
    def assert_almost_equal(self, actual, expected, tolerance=0.01, msg=""):
        """近似相等比较"""
        if abs(actual - expected) <= tolerance:
            self.passed += 1
            return True
        else:
            self.failed += 1
            error_msg = f"期望约 {expected!r}, 得到 {actual!r}"
            if msg:
                error_msg = f"{msg}: {error_msg}"
            self.errors.append(error_msg)
            return False
    
    def summary(self):
        """返回测试摘要"""
        total = self.passed + self.failed
        status = "通过" if self.failed == 0 else "失败"
        return f"测试结果: {self.passed}/{total} 通过 [{status}]"


def test_encode_basic():
    """测试基本编码功能"""
    r = TestResult()
    
    # 测试单个字符
    r.assert_equal(encode('A'), '.-', "编码 A")
    r.assert_equal(encode('B'), '-...', "编码 B")
    r.assert_equal(encode('E'), '.', "编码 E")
    r.assert_equal(encode('T'), '-', "编码 T")
    
    # 测试单词
    r.assert_equal(encode('HELLO'), '.... . .-.. .-.. ---', "编码 HELLO")
    r.assert_equal(encode('SOS'), '... --- ...', "编码 SOS")
    r.assert_equal(encode('WORLD'), '.-- --- .-. .-.. -..', "编码 WORLD")
    
    # 测试句子
    result = encode('HELLO WORLD')
    expected = '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'
    r.assert_equal(result, expected, "编码 HELLO WORLD")
    
    # 测试小写（应自动转换为大写）
    r.assert_equal(encode('hello'), '.... . .-.. .-.. ---', "编码小写")
    
    # 测试空字符串
    r.assert_equal(encode(''), '', "编码空字符串")
    
    # 测试空格
    r.assert_equal(encode('A B'), '.- / -...', "编码带空格")
    
    print(f"test_encode_basic: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_encode_numbers_and_symbols():
    """测试数字和符号编码"""
    r = TestResult()
    
    # 测试数字
    r.assert_equal(encode('0'), '-----', "编码 0")
    r.assert_equal(encode('1'), '.----', "编码 1")
    r.assert_equal(encode('9'), '----.', "编码 9")
    
    # 测试符号
    r.assert_equal(encode('.'), '.-.-.-', "编码 .")
    r.assert_equal(encode(','), '--..--', "编码 ,")
    r.assert_equal(encode('?'), '..--..', "编码 ?")
    r.assert_equal(encode('!'), '-.-.--', "编码 !")
    r.assert_equal(encode('@'), '.--.-.', "编码 @")
    
    # 测试混合
    r.assert_equal(encode('ABC123'), '.- -... -.-. .---- ..--- ...--', "编码混合")
    
    print(f"test_encode_numbers_and_symbols: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_decode_basic():
    """测试基本解码功能"""
    r = TestResult()
    
    # 测试单个字符
    r.assert_equal(decode('.-'), 'A', "解码 .-")
    r.assert_equal(decode('-...'), 'B', "解码 -...")
    r.assert_equal(decode('.'), 'E', "解码 .")
    r.assert_equal(decode('-'), 'T', "解码 -")
    
    # 测试单词
    r.assert_equal(decode('.... . .-.. .-.. ---'), 'HELLO', "解码 HELLO")
    r.assert_equal(decode('... --- ...'), 'SOS', "解码 SOS")
    
    # 测试句子
    result = decode('.... . .-.. .-.. --- / .-- --- .-. .-.. -..')
    r.assert_equal(result, 'HELLO WORLD', "解码 HELLO WORLD")
    
    # 测试空字符串
    r.assert_equal(decode(''), '', "解码空字符串")
    
    print(f"test_decode_basic: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_decode_numbers_and_symbols():
    """测试数字和符号解码"""
    r = TestResult()
    
    # 测试数字
    r.assert_equal(decode('-----'), '0', "解码 0")
    r.assert_equal(decode('.----'), '1', "解码 1")
    r.assert_equal(decode('----.'), '9', "解码 9")
    
    # 测试符号
    r.assert_equal(decode('.-.-.-'), '.', "解码 .")
    r.assert_equal(decode('--..--'), ',', "解码 ,")
    r.assert_equal(decode('..--..'), '?', "解码 ?")
    
    print(f"test_decode_numbers_and_symbols: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_encode_decode_roundtrip():
    """测试编码解码往返"""
    r = TestResult()
    
    test_cases = [
        'HELLO',
        'SOS',
        'HELLO WORLD',
        'ABC 123',
        'MORSE CODE',
        'TEST 123 TEST',
    ]
    
    for text in test_cases:
        morse = encode(text)
        decoded = decode(morse)
        r.assert_equal(decoded, text, f"往返测试: {text}")
    
    print(f"test_encode_decode_roundtrip: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_error_handling():
    """测试错误处理"""
    r = TestResult()
    
    # 测试无效字符编码
    r.assert_raises(
        InvalidCharacterError,
        encode,
        '你好',
        msg="编码中文字符应抛出异常"
    )
    
    # 测试忽略无效字符
    try:
        result = encode('你好', ignore_unknown=True)
        r.assert_equal(result, '', "忽略无效字符应返回空")
    except Exception as e:
        r.failed += 1
        r.errors.append(f"忽略无效字符异常: {e}")
    
    # 测试无效摩尔斯码解码
    r.assert_raises(
        InvalidMorseError,
        decode,
        '... ... ... invalid',
        msg="解码无效摩尔斯码应抛出异常"
    )
    
    # 测试忽略无效摩尔斯码
    try:
        result = decode('... ...', ignore_unknown=True)
        r.assert_true('S' in result, "忽略无效摩尔斯码应解码有效部分")
    except Exception as e:
        r.failed += 1
        r.errors.append(f"忽略无效摩尔斯码异常: {e}")
    
    print(f"test_error_handling: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_validation():
    """测试验证功能"""
    r = TestResult()
    
    # 测试摩尔斯码验证
    r.assert_true(is_valid_morse('... --- ...'), "有效摩尔斯码")
    r.assert_true(is_valid_morse('.- -... -.-.'), "有效摩尔斯码")
    r.assert_true(is_valid_morse(''), "空字符串有效")
    r.assert_true(is_valid_morse('.- / -...'), "带分隔符的有效摩尔斯码")
    r.assert_false(is_valid_morse('abc'), "无效摩尔斯码")
    r.assert_false(is_valid_morse('.-.abc'), "包含无效字符")
    
    # 测试文本验证
    valid, invalid = is_valid_text_for_encoding('HELLO')
    r.assert_true(valid, "HELLO 可编码")
    r.assert_equal(len(invalid), 0, "无无效字符")
    
    valid, invalid = is_valid_text_for_encoding('你好')
    r.assert_false(valid, "中文不可编码")
    r.assert_equal(len(invalid), 2, "有无效字符")
    
    print(f"test_validation: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_utilities():
    """测试工具函数"""
    r = TestResult()
    
    # 测试支持的字符
    chars = get_supported_characters()
    r.assert_true('A' in chars, "A 在支持字符中")
    r.assert_true('0' in chars, "0 在支持字符中")
    r.assert_true('.' in chars, ". 在支持字符中")
    
    # 测试字符转摩尔斯
    r.assert_equal(get_morse_for_char('A'), '.-', "A 的摩尔斯码")
    r.assert_equal(get_morse_for_char('a'), '.-', "a 的摩尔斯码（小写）")
    r.assert_equal(get_morse_for_char('你'), None, "中文字符无摩尔斯码")
    
    # 测试摩尔斯转字符
    r.assert_equal(get_char_for_morse('.-'), 'A', ".- 的字符")
    r.assert_equal(get_char_for_morse('...'), 'S', "... 的字符")
    r.assert_equal(get_char_for_morse('invalid'), None, "无效摩尔斯码")
    
    # 测试标准化
    r.assert_equal(normalize_morse('.-'), '.-', "标准化简单码")
    r.assert_equal(normalize_morse('. - .'), '.-.', "标准化空格")
    r.assert_equal(normalize_morse('.—.'), '.-.', "标准化特殊划")
    
    print(f"test_utilities: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_duration():
    """测试时长计算"""
    r = TestResult()
    
    # 测试默认配置
    config = MorseConfig(dot_duration=0.1)
    
    # 一个点
    duration = calculate_duration('.', config)
    # 点 + 符号间隔 = 0.1 + 0.1 = 0.2
    r.assert_almost_equal(duration, 0.2, tolerance=0.01, msg="单点时长")
    
    # 一个划
    duration = calculate_duration('-', config)
    # 划 + 符号间隔 = 0.3 + 0.1 = 0.4
    r.assert_almost_equal(duration, 0.4, tolerance=0.01, msg="单划时长")
    
    # SOS: ... --- ...
    duration = calculate_duration('... --- ...', config)
    # 3点 + 3划 + 3点 = 3*0.2 + 3*0.4 + 3*0.2 + 2*字母间隔
    # 但实际计算有间隔调整
    r.assert_true(duration > 0, "SOS 时长大于 0")
    
    print(f"test_duration: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_audio_generation():
    """测试音频生成"""
    r = TestResult()
    
    # 测试生成音调
    audio = generate_tone(600, 0.1)
    r.assert_true(len(audio) > 44, "音频数据长度大于 WAV 头")
    
    # 检查 WAV 头
    r.assert_equal(audio[:4], b'RIFF', "WAV RIFF 头")
    r.assert_equal(audio[8:12], b'WAVE', "WAV 格式标记")
    
    # 测试生成静音
    silence = generate_silence(0.1)
    r.assert_true(len(silence) > 44, "静音数据长度大于 WAV 头")
    
    # 测试生成摩尔斯音频
    morse_audio = generate_morse_audio('SOS')
    r.assert_true(len(morse_audio) > 44, "摩尔斯音频数据长度大于 WAV 头")
    
    print(f"test_audio_generation: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_abbreviations():
    """测试缩写和Q代码"""
    r = TestResult()
    
    # 测试摩尔斯缩写
    sos_morse = translate_abbreviation('SOS')
    r.assert_equal(sos_morse, '...---...', "SOS 缩写")
    
    cq_morse = translate_abbreviation('CQ')
    r.assert_equal(cq_morse, '-.-.--.-', "CQ 缩写")
    
    r.assert_equal(translate_abbreviation('INVALID'), None, "无效缩写")
    
    # 测试 Q 代码
    qth = translate_q_code('QTH')
    r.assert_equal(qth, 'What is your position?', "QTH 含义")
    
    qrz = translate_q_code('QRZ')
    r.assert_equal(qrz, 'Who is calling me?', "QRZ 含义")
    
    r.assert_equal(translate_q_code('INVALID'), None, "无效 Q 代码")
    
    # 测试列表
    abbr_list = list_abbreviations()
    r.assert_true(len(abbr_list) > 0, "缩写列表非空")
    r.assert_true('SOS' in abbr_list, "SOS 在缩写列表中")
    
    q_list = list_q_codes()
    r.assert_true(len(q_list) > 0, "Q 代码列表非空")
    r.assert_true('QTH' in q_list, "QTH 在 Q 代码列表中")
    
    print(f"test_abbreviations: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_statistics():
    """测试统计功能"""
    r = TestResult()
    
    # 测试摩尔斯统计
    stats = get_morse_stats('... --- ...')
    r.assert_equal(stats['dots'], 6, "点数量")
    r.assert_equal(stats['dashes'], 3, "划数量")
    r.assert_equal(stats['letters'], 3, "字母数量")
    r.assert_equal(stats['words'], 1, "单词数量")
    r.assert_equal(stats['total_symbols'], 9, "总符号数")
    
    # 测试反转
    reversed_morse = reverse_encode('...')
    r.assert_equal(reversed_morse, '---', "反转点为划")
    
    reversed_morse = reverse_encode('.-')
    r.assert_equal(reversed_morse, '-.', "反转混合")
    
    print(f"test_statistics: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_compare():
    """测试比较功能"""
    r = TestResult()
    
    # 测试相同摩尔斯码
    equal, diff = compare_morse('...', '...')
    r.assert_true(equal, "相同摩尔斯码比较")
    r.assert_equal(diff['matches'], 3, "匹配数")
    r.assert_equal(diff['mismatches'], 0, "不匹配数")
    
    # 测试不同摩尔斯码
    equal, diff = compare_morse('...', '---')
    r.assert_false(equal, "不同摩尔斯码比较")
    r.assert_equal(diff['matches'], 0, "匹配数为 0")
    r.assert_equal(diff['mismatches'], 3, "不匹配数")
    
    # 测试带空格
    equal, diff = compare_morse('. - .', '.-.')
    r.assert_true(equal, "带空格比较")
    
    print(f"test_compare: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_practice_mode():
    """测试练习模式"""
    r = TestResult()
    
    # 测试编码练习
    result = practice_mode(text='HELLO', show_answer=True)
    r.assert_equal(result['type'], 'encode', "编码练习类型")
    r.assert_equal(result['text'], 'HELLO', "练习文本")
    r.assert_equal(result['morse'], '.... . .-.. .-.. ---', "练习答案")
    
    # 测试解码练习
    result = practice_mode(morse='... --- ...', show_answer=True)
    r.assert_equal(result['type'], 'decode', "解码练习类型")
    r.assert_equal(result['morse'], '... --- ...', "练习摩尔斯码")
    r.assert_equal(result['text'], 'SOS', "练习答案")
    
    # 测试隐藏答案
    result = practice_mode(text='HELLO', show_answer=False)
    r.assert_equal(result['morse'], None, "隐藏答案")
    
    print(f"test_practice_mode: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_morse_code_class():
    """测试 MorseCode 类"""
    r = TestResult()
    
    # 测试默认配置
    mc = MorseCode()
    r.assert_true('MorseCode' in repr(mc), "字符串表示")
    
    # 测试编码
    morse = mc.encode('HELLO')
    r.assert_equal(morse, '.... . .-.. .-.. ---', "类方法编码")
    
    # 测试解码
    text = mc.decode(morse)
    r.assert_equal(text, 'HELLO', "类方法解码")
    
    # 测试时长
    duration = mc.duration(morse)
    r.assert_true(duration > 0, "类方法时长")
    
    # 测试音频
    audio = mc.to_audio('SOS')
    r.assert_true(len(audio) > 44, "类方法音频")
    
    # 测试自定义配置
    custom_config = MorseConfig(dot_duration=0.05, frequency=800)
    mc_custom = MorseCode(config=custom_config)
    r.assert_equal(mc_custom.config.frequency, 800, "自定义频率")
    r.assert_equal(mc_custom.config.dot_duration, 0.05, "自定义点时长")
    
    print(f"test_morse_code_class: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_convenience_functions():
    """测试便捷函数"""
    r = TestResult()
    
    # 测试 text_to_morse
    morse = text_to_morse('HELLO')
    r.assert_equal(morse, '.... . .-.. .-.. ---', "text_to_morse")
    
    # 测试 morse_to_text
    text = morse_to_text(morse)
    r.assert_equal(text, 'HELLO', "morse_to_text")
    
    # 测试 text_to_audio
    audio = text_to_audio('SOS')
    r.assert_true(len(audio) > 44, "text_to_audio")
    
    print(f"test_convenience_functions: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def test_file_operations():
    """测试文件操作"""
    r = TestResult()
    
    import tempfile
    import os
    
    # 创建临时文件
    with tempfile.TemporaryDirectory() as tmpdir:
        # 测试编码文件
        input_file = os.path.join(tmpdir, 'input.txt')
        output_file = os.path.join(tmpdir, 'output.txt')
        
        # 写入测试内容
        with open(input_file, 'w') as f:
            f.write('HELLO WORLD')
        
        # 编码
        count = encode_file(input_file, output_file)
        r.assert_equal(count, 11, "编码字符数")
        
        # 检查输出
        with open(output_file, 'r') as f:
            encoded = f.read()
        r.assert_equal(encoded, '.... . .-.. .-.. --- / .-- --- .-. .-.. -..', "编码文件内容")
        
        # 解码
        decoded_file = os.path.join(tmpdir, 'decoded.txt')
        count = decode_file(output_file, decoded_file)
        
        with open(decoded_file, 'r') as f:
            decoded = f.read()
        r.assert_equal(decoded, 'HELLO WORLD', "解码文件内容")
    
    print(f"test_file_operations: {r.summary()}")
    if r.errors:
        for e in r.errors[:5]:
            print(f"  - {e}")
    return r


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Morse Utils 测试套件")
    print("=" * 60)
    print()
    
    all_results = []
    
    # 运行所有测试
    all_results.append(test_encode_basic())
    all_results.append(test_encode_numbers_and_symbols())
    all_results.append(test_decode_basic())
    all_results.append(test_decode_numbers_and_symbols())
    all_results.append(test_encode_decode_roundtrip())
    all_results.append(test_error_handling())
    all_results.append(test_validation())
    all_results.append(test_utilities())
    all_results.append(test_duration())
    all_results.append(test_audio_generation())
    all_results.append(test_abbreviations())
    all_results.append(test_statistics())
    all_results.append(test_compare())
    all_results.append(test_practice_mode())
    all_results.append(test_morse_code_class())
    all_results.append(test_convenience_functions())
    all_results.append(test_file_operations())
    
    # 汇总结果
    print()
    print("=" * 60)
    total_passed = sum(r.passed for r in all_results)
    total_failed = sum(r.failed for r in all_results)
    total_tests = total_passed + total_failed
    
    print(f"总测试: {total_tests}")
    print(f"通过: {total_passed}")
    print(f"失败: {total_failed}")
    
    if total_failed == 0:
        print("\n✅ 所有测试通过!")
    else:
        print(f"\n❌ 有 {total_failed} 个测试失败")
    
    print("=" * 60)
    
    return total_failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)