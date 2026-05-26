"""
密码短语生成工具测试 (Passphrase Utils Test)
测试所有功能以确保正确性和安全性
"""

import sys
import os
import math
import re

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from passphrase_utils.mod import (
    PassphraseGenerator,
    PassphraseResult,
    Separator,
    WordCase,
    generate_passphrase,
    generate_diceware,
    passphrase_strength,
    BUILTIN_WORDLIST,
    DICETIME_WORDLIST
)


def test_wordlist_not_empty():
    """测试单词列表不为空"""
    assert len(BUILTIN_WORDLIST) > 0, "内置单词列表不应为空"
    assert len(DICETIME_WORDLIST) > 0, "Diceware 单词列表不应为空"
    print(f"✓ 内置单词列表: {len(BUILTIN_WORDLIST)} 个单词")
    print(f"✓ Diceware 单词列表: {len(DICETIME_WORDLIST)} 个单词")


def test_generator_initialization():
    """测试生成器初始化"""
    gen = PassphraseGenerator()
    assert gen.wordlist is not None
    assert len(gen.wordlist) > 0
    
    # 测试自定义单词列表（至少 10 个单词）
    custom = ["apple", "banana", "cherry", "date", "elderberry",
              "fig", "grape", "honeydew", "kiwi", "lemon"]
    gen_custom = PassphraseGenerator(wordlist=custom, wordlist_name="custom")
    assert gen_custom.wordlist == custom
    assert gen_custom.wordlist_name == "custom"
    print("✓ 生成器初始化测试通过")


def test_invalid_wordlist():
    """测试无效单词列表"""
    try:
        PassphraseGenerator(wordlist=[])
        assert False, "空列表应该抛出异常"
    except ValueError as e:
        assert "单词列表不能为空" in str(e)
        print("✓ 空单词列表正确抛出异常")
    
    try:
        PassphraseGenerator(wordlist=["a", "b", "c"])  # 太少（少于10）
        assert False, "太少的单词应该抛出异常"
    except ValueError as e:
        assert "单词列表太少" in str(e)
        print("✓ 太少的单词列表正确抛出异常")


def test_generate_basic():
    """测试基本生成功能"""
    gen = PassphraseGenerator()
    result = gen.generate()
    
    assert isinstance(result, PassphraseResult)
    assert result.word_count == 4
    assert len(result.words) == 4
    assert len(result.passphrase) > 0
    assert result.entropy_bits > 0
    print(f"✓ 基本生成: {result.passphrase}")
    print(f"  熵值: {result.entropy_bits} bits")


def test_generate_custom_word_count():
    """测试自定义单词数量"""
    gen = PassphraseGenerator()
    
    for count in [1, 3, 5, 7, 10]:
        result = gen.generate(word_count=count)
        assert result.word_count == count
        assert len(result.words) == count
    print("✓ 自定义单词数量测试通过")


def test_generate_invalid_word_count():
    """测试无效单词数量"""
    gen = PassphraseGenerator()
    
    try:
        gen.generate(word_count=0)
        assert False, "应该抛出异常"
    except ValueError:
        print("✓ 单词数量 0 正确抛出异常")
    
    try:
        gen.generate(word_count=25)
        assert False, "应该抛出异常"
    except ValueError:
        print("✓ 单词数量超过 20 正确抛出异常")


def test_separators():
    """测试各种分隔符"""
    gen = PassphraseGenerator()
    
    # 测试所有分隔符类型
    separators = [
        (Separator.SPACE, " "),
        (Separator.HYPHEN, "-"),
        (Separator.UNDERSCORE, "_"),
        (Separator.DOT, "."),
        (Separator.NONE, ""),
    ]
    
    for sep, expected in separators:
        result = gen.generate(word_count=3, separator=sep)
        if expected:
            assert expected in result.passphrase, f"分隔符 '{expected}' 应该在 '{result.passphrase}' 中"
        else:
            # 无分隔符时，检查单词直接连接
            assert result.separator == expected
        print(f"✓ 分隔符测试 '{expected or '(无)'}' 通过")
    
    # 测试随机分隔符
    result = gen.generate(separator=Separator.RANDOM)
    print(f"✓ 随机分隔符: {result.passphrase}")


def test_word_case():
    """测试单词大小写"""
    gen = PassphraseGenerator()
    
    # 小写
    result = gen.generate(word_count=3, word_case=WordCase.LOWER)
    assert all(w.islower() for w in result.words), "所有单词应为小写"
    print(f"✓ 小写测试: {result.passphrase}")
    
    # 大写
    result = gen.generate(word_count=3, word_case=WordCase.UPPER)
    assert all(w.isupper() for w in result.words), "所有单词应为大写"
    print(f"✓ 大写测试: {result.passphrase}")
    
    # 首字母大写
    result = gen.generate(word_count=3, word_case=WordCase.CAPITALIZE)
    assert all(w[0].isupper() for w in result.words), "所有单词应首字母大写"
    print(f"✓ 首字母大写测试: {result.passphrase}")


def test_include_numbers():
    """测试包含数字"""
    gen = PassphraseGenerator()
    result = gen.generate(include_numbers=True)
    
    # 检查末尾是否有数字
    assert re.search(r'\d+$', result.passphrase), "密码短语末尾应包含数字"
    print(f"✓ 包含数字测试: {result.passphrase}")


def test_include_special():
    """测试包含特殊字符"""
    gen = PassphraseGenerator()
    special_chars = "!@#$%^&*"
    result = gen.generate(include_special=True, special_chars=special_chars)
    
    # 检查末尾是否有特殊字符
    assert result.passphrase[-1] in special_chars, "密码短语末尾应有特殊字符"
    print(f"✓ 包含特殊字符测试: {result.passphrase}")


def test_word_length_filter():
    """测试单词长度过滤"""
    gen = PassphraseGenerator()
    result = gen.generate(
        word_count=10,
        min_word_length=4,
        max_word_length=6
    )
    
    for word in result.words:
        # 注意：转换大小写后检查原始长度
        assert 4 <= len(word) <= 6, f"单词 '{word}' 长度应为 4-6，实际为 {len(word)}"
    print(f"✓ 单词长度过滤测试: {result.passphrase}")


def test_entropy_calculation():
    """测试熵值计算"""
    gen = PassphraseGenerator()
    
    # 4 个单词，使用默认单词列表
    entropy = gen.calculate_entropy(4)
    expected = 4 * math.log2(len(gen.wordlist))
    assert abs(entropy - round(expected, 2)) < 0.1
    
    # 更多的单词应该有更高的熵值
    entropy_5 = gen.calculate_entropy(5)
    assert entropy_5 > entropy
    
    print(f"✓ 熵值计算测试: 4 词 = {entropy} bits, 5 词 = {entropy_5} bits")


def test_generate_multiple():
    """测试批量生成"""
    gen = PassphraseGenerator()
    results = gen.generate_multiple(10)
    
    assert len(results) == 10
    
    # 检查所有结果都是唯一的
    passphrases = [r.passphrase for r in results]
    unique_count = len(set(passphrases))
    # 由于随机性，大多数应该是唯一的
    assert unique_count >= 8, f"应该有至少 8 个唯一的密码短语，实际 {unique_count}"
    
    print(f"✓ 批量生成 10 个密码短语，{unique_count} 个唯一")


def test_crack_time_estimation():
    """测试破解时间估算"""
    gen = PassphraseGenerator()
    
    # 低熵值
    time1 = gen.estimate_crack_time(20)
    assert "秒" in time1 or "分钟" in time1 or "瞬间" in time1
    print(f"  20 bits: {time1}")
    
    # 中等熵值
    time2 = gen.estimate_crack_time(50)
    print(f"  50 bits: {time2}")
    
    # 高熵值
    time3 = gen.estimate_crack_time(80)
    assert "年" in time3 or "亿" in time3
    print(f"  80 bits: {time3}")
    
    # 极高熵值
    time4 = gen.estimate_crack_time(120)
    print(f"  120 bits: {time4}")
    
    print("✓ 破解时间估算测试通过")


def test_analyze_passphrase():
    """测试密码短语分析"""
    gen = PassphraseGenerator()
    
    # 测试有效的密码短语（使用内置单词列表中存在的单词）
    analysis = gen.analyze_passphrase("like-work-time-food")
    # 注意：analyze_passphrase 的识别可能不完全，因为需要单词存在于列表中
    assert analysis["passphrase"] == "like-work-time-food"
    assert analysis["has_number"] == False
    print(f"✓ 分析 'like-work-time-food': {analysis['strength']}")
    
    # 测试带数字的
    analysis = gen.analyze_passphrase("like-work-1234")
    assert analysis["has_number"] == True
    print(f"✓ 分析带数字的密码短语")
    
    # 测试带特殊字符的
    analysis = gen.analyze_passphrase("like-work!")
    assert analysis["has_special"] == True
    print(f"✓ 分析带特殊字符的密码短语")
    
    # 测试未知格式的密码（无法识别分隔符时返回 word_count=0）
    analysis = gen.analyze_passphrase("unknownformatpassword")
    # 无论是否能识别，都应该返回分析结果
    assert analysis["passphrase"] == "unknownformatpassword"
    assert analysis["strength"] in ["非常弱", "弱", "中等", "强", "非常强"]
    print(f"✓ 分析未知格式密码: {analysis['strength']}")


def test_quick_functions():
    """测试快捷函数"""
    # generate_passphrase
    phrase = generate_passphrase()
    assert len(phrase) > 0
    assert "-" in phrase
    print(f"✓ generate_passphrase(): {phrase}")
    
    # generate_passphrase with custom separator
    phrase = generate_passphrase(separator=" ")
    assert " " in phrase
    print(f"✓ generate_passphrase(separator=' '): {phrase}")
    
    # generate_diceware
    phrase = generate_diceware()
    assert len(phrase) > 0
    print(f"✓ generate_diceware(): {phrase}")
    
    # passphrase_strength
    strength = passphrase_strength("correct-horse-battery-staple")
    assert "strength" in strength
    assert "entropy_bits" in strength
    print(f"✓ passphrase_strength(): {strength['strength']}")


def test_diceware_generator():
    """测试 Diceware 生成器"""
    gen = PassphraseGenerator(wordlist=DICETIME_WORDLIST, wordlist_name="diceware")
    result = gen.generate(word_count=5)
    
    assert result.word_count == 5
    assert result.wordlist_name == "diceware"
    print(f"✓ Diceware 生成: {result.passphrase}")


def test_custom_wordlist():
    """测试自定义单词列表"""
    # 使用至少 10 个单词的自定义列表
    custom_words = ["apple", "banana", "cherry", "date", "elderberry",
                    "fig", "grape", "honeydew", "kiwi", "lemon",
                    "mango", "nectarine", "orange", "papaya", "quince"]
    gen = PassphraseGenerator(wordlist=custom_words, wordlist_name="fruits")
    
    result = gen.generate(word_count=3)
    for word in result.words:
        assert word.lower() in [w.lower() for w in custom_words]
    
    print(f"✓ 自定义单词列表: {result.passphrase}")


def test_randomness():
    """测试随机性（生成多个密码短语，验证不会完全相同）"""
    gen = PassphraseGenerator()
    results = gen.generate_multiple(100)
    
    passphrases = [r.passphrase for r in results]
    unique = len(set(passphrases))
    
    # 100 个密码短语中，至少应该有 90 个是唯一的
    assert unique >= 90, f"随机性不足：100 个密码短语只有 {unique} 个唯一"
    print(f"✓ 随机性测试：100 个密码短语中 {unique} 个唯一")


def test_security():
    """测试安全性（使用 secrets 模块而非 random）"""
    # 这个测试确保我们使用的是密码学安全的随机数生成器
    import passphrase_utils.mod as module
    import inspect
    
    source = inspect.getsource(module.PassphraseGenerator.generate)
    assert "secrets.choice" in source or "secrets.randbelow" in source, \
        "应该使用 secrets 模块而非 random 模块"
    assert "random.choice" not in source.lower(), \
        "不应使用 random.choice（不安全）"
    
    print("✓ 安全性测试：使用密码学安全的随机数生成器")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("密码短语生成工具测试")
    print("=" * 60)
    print()
    
    tests = [
        test_wordlist_not_empty,
        test_generator_initialization,
        test_invalid_wordlist,
        test_generate_basic,
        test_generate_custom_word_count,
        test_generate_invalid_word_count,
        test_separators,
        test_word_case,
        test_include_numbers,
        test_include_special,
        test_word_length_filter,
        test_entropy_calculation,
        test_generate_multiple,
        test_crack_time_estimation,
        test_analyze_passphrase,
        test_quick_functions,
        test_diceware_generator,
        test_custom_wordlist,
        test_randomness,
        test_security,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} 失败: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)