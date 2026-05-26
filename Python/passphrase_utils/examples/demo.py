"""
密码短语生成工具示例 (Passphrase Utils Examples)
演示各种使用场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    PassphraseGenerator,
    Separator,
    WordCase,
    generate_passphrase,
    generate_diceware,
    passphrase_strength
)


def example_basic():
    """基本用法示例"""
    print("=" * 60)
    print("1. 基本用法")
    print("=" * 60)
    
    # 使用快捷函数
    phrase = generate_passphrase()
    print(f"默认生成: {phrase}")
    
    # 指定单词数量
    phrase = generate_passphrase(word_count=5)
    print(f"5 个单词: {phrase}")
    
    # 指定分隔符
    phrase = generate_passphrase(separator=" ")
    print(f"空格分隔: {phrase}")
    
    phrase = generate_passphrase(separator="_")
    print(f"下划线分隔: {phrase}")
    print()


def example_generator():
    """使用 PassphraseGenerator 类"""
    print("=" * 60)
    print("2. 使用 PassphraseGenerator 类")
    print("=" * 60)
    
    gen = PassphraseGenerator()
    
    # 基本生成
    result = gen.generate()
    print(f"密码短语: {result.passphrase}")
    print(f"单词: {result.words}")
    print(f"熵值: {result.entropy_bits} bits")
    print(f"分隔符: '{result.separator}'")
    print()


def example_separators():
    """分隔符示例"""
    print("=" * 60)
    print("3. 分隔符选项")
    print("=" * 60)
    
    gen = PassphraseGenerator()
    
    separators = [
        (Separator.SPACE, "空格"),
        (Separator.HYPHEN, "连字符"),
        (Separator.UNDERSCORE, "下划线"),
        (Separator.DOT, "点号"),
        (Separator.NONE, "无分隔符"),
        (Separator.RANDOM, "随机"),
    ]
    
    for sep, name in separators:
        result = gen.generate(word_count=3, separator=sep)
        print(f"{name}: {result.passphrase}")
    print()


def example_word_case():
    """单词大小写示例"""
    print("=" * 60)
    print("4. 单词大小写选项")
    print("=" * 60)
    
    gen = PassphraseGenerator()
    
    cases = [
        (WordCase.LOWER, "小写"),
        (WordCase.UPPER, "大写"),
        (WordCase.CAPITALIZE, "首字母大写"),
        (WordCase.RANDOM, "随机大小写"),
        (WordCase.ALTERNATE, "交替大小写"),
    ]
    
    for case, name in cases:
        result = gen.generate(word_count=3, word_case=case)
        print(f"{name}: {result.passphrase}")
    print()


def example_enhanced():
    """增强密码示例"""
    print("=" * 60)
    print("5. 增强密码短语")
    print("=" * 60)
    
    gen = PassphraseGenerator()
    
    # 添加数字
    result = gen.generate(include_numbers=True)
    print(f"带数字: {result.passphrase}")
    
    # 添加特殊字符
    result = gen.generate(include_special=True)
    print(f"带特殊字符: {result.passphrase}")
    
    # 同时添加数字和特殊字符
    result = gen.generate(include_numbers=True, include_special=True)
    print(f"带数字和特殊字符: {result.passphrase}")
    
    # 自定义特殊字符
    result = gen.generate(include_special=True, special_chars="@#$%")
    print(f"自定义特殊字符: {result.passphrase}")
    print()


def example_diceware():
    """Diceware 方法示例"""
    print("=" * 60)
    print("6. Diceware 风格")
    print("=" * 60)
    
    # 使用 Diceware 单词列表
    phrase = generate_diceware()
    print(f"Diceware 默认: {phrase}")
    
    # 指定单词数量
    phrase = generate_diceware(word_count=6)
    print(f"Diceware 6 词: {phrase}")
    
    # 使用连字符分隔
    phrase = generate_diceware(word_count=5, separator="-")
    print(f"Diceware 连字符: {phrase}")
    print()


def example_entropy():
    """熵值计算示例"""
    print("=" * 60)
    print("7. 熵值和安全性")
    print("=" * 60)
    
    gen = PassphraseGenerator()
    
    print("单词数量 vs 熵值:")
    for count in range(3, 9):
        entropy = gen.calculate_entropy(count)
        crack_time = gen.estimate_crack_time(entropy)
        print(f"  {count} 个单词: {entropy:.1f} bits (破解时间: {crack_time})")
    
    print()
    print("不同单词列表大小的影响:")
    for size in [1000, 2000, 5000, 7776, 10000]:
        entropy = gen.calculate_entropy(4, size)
        print(f"  {size} 个单词, 4 词: {entropy:.1f} bits")
    print()


def example_strength_analysis():
    """强度分析示例"""
    print("=" * 60)
    print("8. 密码短语强度分析")
    print("=" * 60)
    
    test_phrases = [
        "correct-horse-battery-staple",
        "apple banana cherry",
        "PASSWORD123!",
        "this-is-a-very-long-passphrase-with-many-words",
        "a-b-c-d",
    ]
    
    for phrase in test_phrases:
        analysis = passphrase_strength(phrase)
        print(f"'{phrase}'")
        print(f"  强度: {analysis['strength']}")
        print(f"  熵值: {analysis['entropy_bits']:.1f} bits")
        print(f"  单词数: {analysis['word_count']}")
        print(f"  预估破解时间: {analysis['estimated_crack_time']}")
        print()
    print()


def example_multiple():
    """批量生成示例"""
    print("=" * 60)
    print("9. 批量生成密码短语")
    print("=" * 60)
    
    gen = PassphraseGenerator()
    results = gen.generate_multiple(10)
    
    print("生成 10 个密码短语候选:")
    for i, r in enumerate(results, 1):
        print(f"  {i:2d}. {r.passphrase} ({r.entropy_bits:.1f} bits)")
    print()


def example_custom_wordlist():
    """自定义单词列表示例"""
    print("=" * 60)
    print("10. 自定义单词列表")
    print("=" * 60)
    
    # 中文单词列表
    chinese_words = [
        "苹果", "香蕉", "樱桃", "葡萄", "橙子",
        "西瓜", "草莓", "蓝莓", "芒果", "柠檬",
        "桃子", "梨子", "荔枝", "龙眼", "榴莲",
        "菠萝", "椰子", "石榴", "柿子", "杏子"
    ]
    
    gen = PassphraseGenerator(wordlist=chinese_words, wordlist_name="fruits_cn")
    result = gen.generate(word_count=4)
    print(f"中文水果: {result.passphrase}")
    
    # 使用 Diceware 单词列表
    from passphrase_utils.mod import DICETIME_WORDLIST
    gen = PassphraseGenerator(wordlist=DICETIME_WORDLIST, wordlist_name="diceware")
    result = gen.generate(word_count=5, separator=Separator.SPACE)
    print(f"Diceware: {result.passphrase}")
    print()


def example_security_recommendations():
    """安全建议示例"""
    print("=" * 60)
    print("11. 安全建议")
    print("=" * 60)
    
    gen = PassphraseGenerator()
    
    print("不同安全级别推荐:")
    print()
    
    # 一般用途
    result = gen.generate(word_count=4)
    print(f"一般用途 (4 词):")
    print(f"  {result.passphrase}")
    print(f"  熵值: {result.entropy_bits:.1f} bits")
    print(f"  适用于: 社交媒体、论坛等普通网站")
    print()
    
    # 重要账户
    result = gen.generate(word_count=5)
    print(f"重要账户 (5 词):")
    print(f"  {result.passphrase}")
    print(f"  熵值: {result.entropy_bits:.1f} bits")
    print(f"  适用于: 邮箱、支付账户")
    print()
    
    # 高安全性
    result = gen.generate(word_count=7, include_numbers=True)
    print(f"高安全性 (7 词 + 数字):")
    print(f"  {result.passphrase}")
    print(f"  熵值: {result.entropy_bits:.1f} bits")
    print(f"  适用于: 加密货币钱包、密码管理器主密码")
    print()


def example_full():
    """完整示例"""
    print("=" * 60)
    print("12. 完整示例")
    print("=" * 60)
    
    gen = PassphraseGenerator()
    
    # 生成一个安全的密码短语
    result = gen.generate(
        word_count=5,
        separator=Separator.HYPHEN,
        word_case=WordCase.CAPITALIZE,
        include_numbers=True,
        include_special=True
    )
    
    print("生成的密码短语:")
    print(f"  密码短语: {result.passphrase}")
    print(f"  组成单词: {', '.join(result.words)}")
    print(f"  熵值: {result.entropy_bits:.1f} bits")
    print(f"  分隔符: '{result.separator}'")
    print(f"  单词数: {result.word_count}")
    print(f"  单词列表: {result.wordlist_name}")
    print(f"  预估破解时间: {gen.estimate_crack_time(result.entropy_bits)}")
    
    # 分析强度
    analysis = gen.analyze_passphrase(result.passphrase)
    print(f"  强度评级: {analysis['strength']}")
    print()


def main():
    """运行所有示例"""
    example_basic()
    example_generator()
    example_separators()
    example_word_case()
    example_enhanced()
    example_diceware()
    example_entropy()
    example_strength_analysis()
    example_multiple()
    example_custom_wordlist()
    example_security_recommendations()
    example_full()
    
    print("=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()