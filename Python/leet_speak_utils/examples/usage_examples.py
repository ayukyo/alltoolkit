"""
Leet Speak Utils 使用示例

展示如何使用 leet_speak_utils 模块进行各种编码、解码和生成操作。
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from leet_speak_utils.mod import (
    LeetSpeakEncoder,
    LeetSpeakDecoder,
    LeetSpeakGenerator,
    encode,
    decode,
    is_leet,
    detect_level,
    to_leet,
    from_leet,
    create_custom_encoder,
)


def example_basic_usage():
    """基础用法示例"""
    print("=" * 50)
    print("1. 基础用法")
    print("=" * 50)
    
    text = "Hello World"
    
    print(f"\n原文: {text}")
    print(f"基础转换: {encode(text, 'basic')}")
    print(f"标准转换: {encode(text, 'standard')}")
    print(f"高级转换: {encode(text, 'advanced')}")
    
    # 解码
    leet_text = "H3ll0 W0rld"
    print(f"\nLeet 文本: {leet_text}")
    print(f"解码结果: {decode(leet_text, 'basic')}")


def example_different_levels():
    """不同级别对比示例"""
    print("\n" + "=" * 50)
    print("2. 不同级别对比")
    print("=" * 50)
    
    words = ["hacker", "elite", "skills", "password"]
    
    for word in words:
        print(f"\n{word}:")
        print(f"  Basic:    {encode(word, 'basic')}")
        print(f"  Standard: {encode(word, 'standard')}")
        print(f"  Advanced: {encode(word, 'advanced')}")


def example_random_encoding():
    """随机编码示例"""
    print("\n" + "=" * 50)
    print("3. 随机编码（可重现）")
    print("=" * 50)
    
    text = "elite hacker"
    
    print(f"\n原文: {text}")
    print("\n随机编码（固定种子）:")
    
    encoder = LeetSpeakEncoder(level='standard')
    for seed in range(5):
        result = encoder.encode(text, randomize=True, seed=seed)
        print(f"  Seed {seed}: {result}")


def example_custom_mapping():
    """自定义映射示例"""
    print("\n" + "=" * 50)
    print("4. 自定义映射")
    print("=" * 50)
    
    # 自定义映射：只替换特定字符
    custom_map = {
        'a': ['@'],
        'e': ['3'],
        'i': ['!'],
        'o': ['0'],
        'u': ['_'],
    }
    
    encoder = create_custom_encoder(custom_map, base_level='basic')
    
    text = "authentication"
    print(f"\n原文: {text}")
    print(f"自定义编码: {encoder.encode(text)}")


def example_word_variants():
    """单词变体生成示例"""
    print("\n" + "=" * 50)
    print("5. 单词变体生成")
    print("=" * 50)
    
    encoder = LeetSpeakEncoder(level='standard')
    
    words = ["leet", "hacker", "admin"]
    
    for word in words:
        variants = encoder.encode_word_variants(word, max_variants=8)
        print(f"\n{word} 的变体:")
        for i, v in enumerate(variants, 1):
            print(f"  {i}. {v}")


def example_detection():
    """Leet 检测示例"""
    print("\n" + "=" * 50)
    print("6. Leet Speak 检测")
    print("=" * 50)
    
    test_texts = [
        "Hello World",
        "H3ll0 W0rld",
        "l33t h4ck3r",
        "n00b pwn3d",
        "|-|4x0r",
        "Th1s 1s 4 t3st",
    ]
    
    print("\n文本检测结果:")
    for text in test_texts:
        is_leet_text = is_leet(text)
        level = detect_level(text)
        print(f"  '{text}'")
        print(f"    是Leet: {is_leet_text}, 级别: {level}")


def example_username_generator():
    """用户名生成器示例"""
    print("\n" + "=" * 50)
    print("7. 用户名变体生成")
    print("=" * 50)
    
    generator = LeetSpeakGenerator()
    
    usernames = ["shadow", "ninja", "cyber"]
    
    for name in usernames:
        variants = generator.generate_username_variants(name, count=5)
        print(f"\n'{name}' 的用户名变体:")
        for i, v in enumerate(variants, 1):
            print(f"  {i}. {v}")


def example_password_hints():
    """密码提示生成示例"""
    print("\n" + "=" * 50)
    print("8. 密码提示生成")
    print("=" * 50)
    
    generator = LeetSpeakGenerator()
    
    words = ["secret", "password", "admin"]
    
    for word in words:
        hints = generator.generate_password_hints(word)
        print(f"\n'{word}' 的密码提示:")
        for variant, desc in hints:
            print(f"  {variant} ({desc})")


def example_decoder():
    """解码器详细示例"""
    print("\n" + "=" * 50)
    print("9. 解码器高级用法")
    print("=" * 50)
    
    decoder = LeetSpeakDecoder(level='standard')
    
    leet_texts = [
        "l33t",
        "h4ck3r",
        "n00b",
        "pwn3d",
        "pr0",
    ]
    
    print("\n解码示例:")
    for text in leet_texts:
        decoded = decoder.decode(text)
        print(f"  {text} -> {decoded}")
    
    # 所有可能的解码
    print("\n所有可能的解码 (l33t):")
    all_possible = decoder.decode_all_possible("l33t")
    for i, result in enumerate(all_possible[:5], 1):
        print(f"  {i}. {result}")


def example_encoder_class():
    """编码器类详细示例"""
    print("\n" + "=" * 50)
    print("10. 编码器类高级用法")
    print("=" * 50)
    
    # 创建不同级别的编码器
    basic_encoder = LeetSpeakEncoder(level='basic')
    standard_encoder = LeetSpeakEncoder(level='standard')
    advanced_encoder = LeetSpeakEncoder(level='advanced')
    
    text = "The quick brown fox"
    
    print(f"\n原文: {text}")
    print(f"基础: {basic_encoder.encode(text)}")
    print(f"标准: {standard_encoder.encode(text)}")
    print(f"高级: {advanced_encoder.encode(text)}")


def example_practical_use():
    """实际应用示例"""
    print("\n" + "=" * 50)
    print("11. 实际应用场景")
    print("=" * 50)
    
    # 场景1: 生成安全的密码变体
    print("\n场景1: 密码变体生成")
    base_word = "secure123"
    encoder = LeetSpeakEncoder(level='standard')
    for i in range(3):
        variant = encoder.encode(base_word, randomize=True, seed=i)
        print(f"  变体 {i+1}: {variant}")
    
    # 场景2: 用户名可用性检查
    print("\n场景2: 用户名变体建议")
    generator = LeetSpeakGenerator()
    base_name = "gamer"
    variants = generator.generate_username_variants(base_name, count=6)
    print(f"  如果 '{base_name}' 已被占用，可以尝试:")
    for v in variants:
        print(f"    - {v}")
    
    # 场景3: 识别混淆文本
    print("\n场景3: 识别混淆文本")
    suspicious_texts = [
        "fr33 m0n3y",
        "cl1ck h3r3",
        "normal message",
        "pr1z3 w1nn3r",
    ]
    print("  检测潜在混淆文本:")
    for text in suspicious_texts:
        if is_leet(text, threshold=0.2):
            decoded = decode(text)
            print(f"    '{text}' -> 可能是 '{decoded}'")


def main():
    """运行所有示例"""
    example_basic_usage()
    example_different_levels()
    example_random_encoding()
    example_custom_mapping()
    example_word_variants()
    example_detection()
    example_username_generator()
    example_password_hints()
    example_decoder()
    example_encoder_class()
    example_practical_use()
    
    print("\n" + "=" * 50)
    print("示例完成!")
    print("=" * 50)


if __name__ == '__main__':
    main()