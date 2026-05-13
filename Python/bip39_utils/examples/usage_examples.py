"""
BIP39 Utilities 使用示例

演示助记词生成、验证和种子派生的各种用法。
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bip39_utils.mod import (
    BIP39Mnemonic,
    Language,
    generate_mnemonic,
    validate_mnemonic,
    mnemonic_to_seed,
    mnemonic_to_entropy,
    VALID_MNEMONIC_LENGTHS,
)


def example_1_basic_generation():
    """示例 1: 基本助记词生成"""
    print("=" * 60)
    print("示例 1: 基本助记词生成")
    print("=" * 60)
    
    # 创建 BIP39 工具实例
    bip = BIP39Mnemonic()
    
    # 生成不同长度的助记词
    for word_count in [12, 15, 18, 21, 24]:
        result = bip.generate(word_count)
        print(f"\n{word_count} 词助记词:")
        print(f"  助记词: {result.mnemonic}")
        print(f"  熵 (hex): {result.entropy_hex}")
    
    print("\n提示: 12 词提供 128 位安全强度，24 词提供 256 位。")


def example_2_validation():
    """示例 2: 助记词验证"""
    print("\n" + "=" * 60)
    print("示例 2: 助记词验证")
    print("=" * 60)
    
    bip = BIP39Mnemonic()
    
    # 有效助记词（来自 BIP39 测试向量）
    valid_mnemonic = "abandon ability able about above absent absorb abstract absurd abuse access accident"
    
    print(f"\n验证有效助记词:")
    print(f"  助记词: {valid_mnemonic}")
    
    result = bip.validate(valid_mnemonic)
    print(f"  结果:")
    print(f"    - 有效: {result.is_valid}")
    print(f"    - 校验和正确: {result.checksum_valid}")
    print(f"    - 词数: {result.word_count}")
    print(f"    - 语言: {result.detected_language}")
    
    # 无效助记词
    invalid_mnemonic = "abandon ability able about above absent absorb abstract absurd abuse access academy"
    
    print(f"\n验证无效助记词（最后一个词被修改）:")
    print(f"  助记词: {invalid_mnemonic}")
    
    result = bip.validate(invalid_mnemonic)
    print(f"  结果:")
    print(f"    - 有效: {result.is_valid}")
    print(f"    - 错误: {result.error}")
    
    # 错误词数的助记词
    wrong_count = "abandon ability able about above"
    
    print(f"\n验证错误词数的助记词:")
    print(f"  助记词: {wrong_count}")
    
    result = bip.validate(wrong_count)
    print(f"  结果:")
    print(f"    - 有效: {result.is_valid}")
    print(f"    - 错误: {result.error}")


def example_3_seed_generation():
    """示例 3: 种子生成"""
    print("\n" + "=" * 60)
    print("示例 3: 种子生成")
    print("=" * 60)
    
    bip = BIP39Mnemonic()
    
    # BIP39 测试向量中的助记词
    mnemonic = "abandon ability able about above absent absorb abstract absurd abuse access accident"
    
    print(f"\n从助记词生成种子:")
    print(f"  助记词: {mnemonic}")
    
    # 无密码短语
    result = bip.to_seed(mnemonic, "")
    print(f"\n  无密码短语:")
    print(f"    - 种子 (前 32 字节): {result.seed_hex[:64]}")
    print(f"    - 主密钥 (前 16 字节): {result.master_key_hex[:32]}")
    print(f"    - 链码 (前 16 字节): {result.chain_code_hex[:32]}")
    
    # 带密码短语
    result_with_passphrase = bip.to_seed(mnemonic, "TREZOR")
    print(f"\n  密码短语 'TREZOR':")
    print(f"    - 种子 (前 32 字节): {result_with_passphrase.seed_hex[:64]}")
    
    # 对比不同密码短语
    print(f"\n  注意: 不同密码短语产生完全不同的种子!")
    print(f"    无密码短语种子前 8 字节: {result.seed_hex[:16]}")
    print(f"    TREZOR 密码短语种子前 8 字节: {result_with_passphrase.seed_hex[:16]}")


def example_4_custom_entropy():
    """示例 4: 使用自定义熵"""
    print("\n" + "=" * 60)
    print("示例 4: 使用自定义熵")
    print("=" * 60)
    
    bip = BIP39Mnemonic()
    
    # 自定义熵（用于恢复或测试）
    entropy_hex = "00000000000000000000000000000000"
    entropy = bytes.fromhex(entropy_hex)
    
    print(f"\n使用自定义熵生成助记词:")
    print(f"  熵 (hex): {entropy_hex}")
    
    result = bip.generate(12, entropy)
    print(f"  生成的助记词: {result.mnemonic}")
    print(f"  这是著名的测试向量！")
    
    # 另一个熵
    entropy_hex2 = "7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f"
    entropy2 = bytes.fromhex(entropy_hex2)
    
    print(f"\n使用另一个熵:")
    print(f"  熵 (hex): {entropy_hex2}")
    
    result2 = bip.generate(12, entropy2)
    print(f"  生成的助记词: {result2.mnemonic}")


def example_5_entropy_recovery():
    """示例 5: 从助记词恢复熵"""
    print("\n" + "=" * 60)
    print("示例 5: 从助记词恢复熵")
    print("=" * 60)
    
    bip = BIP39Mnemonic()
    
    # 先生成助记词
    result = bip.generate(12)
    mnemonic = result.mnemonic
    original_entropy = result.entropy_hex
    
    print(f"\n原始生成:")
    print(f"  助记词: {mnemonic}")
    print(f"  熵 (hex): {original_entropy}")
    
    # 从助记词恢复熵
    recovered_entropy = bip.to_entropy(mnemonic)
    
    print(f"\n恢复的熵:")
    print(f"  熵 (hex): {recovered_entropy.hex()}")
    
    # 验证熵相同
    if recovered_entropy.hex() == original_entropy:
        print(f"\n  ✓ 熵恢复成功！熵完全匹配。")
    else:
        print(f"\n  ✗ 熵不匹配！")


def example_6_convenience_functions():
    """示例 6: 便捷函数"""
    print("\n" + "=" * 60)
    print("示例 6: 便捷函数")
    print("=" * 60)
    
    # 使用便捷函数快速生成助记词
    mnemonic = generate_mnemonic(12)
    
    print(f"\n快速生成助记词:")
    print(f"  generate_mnemonic(12) -> {mnemonic}")
    
    # 快速验证
    is_valid = validate_mnemonic(mnemonic)
    
    print(f"\n快速验证:")
    print(f"  validate_mnemonic(mnemonic) -> {is_valid}")
    
    # 快速转种子
    seed = mnemonic_to_seed(mnemonic)
    
    print(f"\n快速转种子:")
    print(f"  mnemonic_to_seed(mnemonic) -> {seed.hex()[:32]}...")
    
    # 快速转熵
    entropy = mnemonic_to_entropy(mnemonic)
    
    print(f"\n快速转熵:")
    print(f"  mnemonic_to_entropy(mnemonic) -> {entropy.hex()}")


def example_7_wallet_workflow():
    """示例 7: 完整钱包工作流程"""
    print("\n" + "=" * 60)
    print("示例 7: 完整钱包工作流程")
    print("=" * 60)
    
    bip = BIP39Mnemonic()
    
    print("\n--- 步骤 1: 生成助记词 ---")
    result = bip.generate(24)  # 使用最高安全级别
    mnemonic = result.mnemonic
    
    print(f"  生成的 24 词助记词:")
    print(f"  {mnemonic}")
    
    print("\n  ⚠️  请妥善保存此助记词！这是恢复钱包的唯一方式！")
    
    print("\n--- 步骤 2: 验证助记词 ---")
    validation = bip.validate(mnemonic)
    
    print(f"  验证结果: {validation.is_valid}")
    print(f"  校验和: {validation.checksum_valid}")
    
    print("\n--- 步骤 3: 生成种子 ---")
    seed_result = bip.to_seed(mnemonic)
    
    print(f"  种子 (hex): {seed_result.seed_hex}")
    
    print("\n--- 步骤 4: 获取主密钥 ---")
    print(f"  主密钥: {seed_result.master_key_hex}")
    print(f"  链码: {seed_result.chain_code_hex}")
    
    print("\n  ✓ 钱包初始化完成！")
    print("\n  接下来可以使用主密钥和链码派生各种账户地址。")


def example_8_security_levels():
    """示例 8: 不同安全级别对比"""
    print("\n" + "=" * 60)
    print("示例 8: 不同安全级别对比")
    print("=" * 60)
    
    bip = BIP39Mnemonic()
    
    print("\n不同词数对应不同的安全强度:")
    print("-" * 50)
    
    for word_count in VALID_MNEMONIC_LENGTHS:
        entropy_bits = {
            12: 128,
            15: 160,
            18: 192,
            21: 224,
            24: 256,
        }
        
        result = bip.generate(word_count)
        
        print(f"\n{word_count} 词助记词:")
        print(f"  熵位数: {entropy_bits[word_count]} bits")
        print(f"  示例: {result.mnemonic[:50]}...")
        
        # 计算可能的组合数
        combinations = 2 ** entropy_bits[word_count]
        print(f"  可能组合: ~{combinations:.2e}")


def example_9_passphrase_security():
    """示例 9: 密码短语的安全性"""
    print("\n" + "=" * 60)
    print("示例 9: 密码短语的安全性")
    print("=" * 60)
    
    bip = BIP39Mnemonic()
    
    # 固定的助记词
    mnemonic = generate_mnemonic(12)
    
    print(f"\n使用同一助记词，不同密码短语:")
    print(f"  助记词: {mnemonic}")
    
    # 不同密码短语
    passphrases = ["", "password", "my_secret_passphrase", "密码短语"]
    
    for passphrase in passphrases:
        seed = bip.to_seed(mnemonic, passphrase)
        
        display_passphrase = passphrase if passphrase else "(空)"
        print(f"\n  密码短语 '{display_passphrase}':")
        print(f"    种子前 16 字节: {seed.seed_hex[:32]}")
    
    print("\n  ⚠️  注意: 即使助记词泄露，不知道密码短语也无法恢复钱包！")
    print("  密码短语提供了额外的安全层。")


def example_10_wordlist_operations():
    """示例 10: 词表操作"""
    print("\n" + "=" * 60)
    print("示例 10: 词表操作")
    print("=" * 60)
    
    bip = BIP39Mnemonic()
    
    print("\n词表基本信息:")
    print(f"  总词数: 2048")
    print(f"  第一个词 (index 0): {bip.word_at_index(0)}")
    print(f"  最后一个词 (index 2047): {bip.word_at_index(2047)}")
    
    # 查找词的索引
    words_to_find = ["abandon", "bitcoin", "wallet", "zoo"]
    
    print("\n查找词的索引:")
    for word in words_to_find:
        if bip.is_valid_word(word):
            index = bip.index_of_word(word)
            print(f"  '{word}' -> index {index}")
        else:
            print(f"  '{word}' -> 不在词表中")
    
    # 验证随机词
    print("\n验证词是否在词表中:")
    test_words = ["abandon", "ability", "invalidword", "crypto"]
    for word in test_words:
        is_valid = bip.is_valid_word(word)
        print(f"  '{word}': {is_valid}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("BIP39 Utilities 使用示例")
    print("=" * 60)
    
    example_1_basic_generation()
    example_2_validation()
    example_3_seed_generation()
    example_4_custom_entropy()
    example_5_entropy_recovery()
    example_6_convenience_functions()
    example_7_wallet_workflow()
    example_8_security_levels()
    example_9_passphrase_security()
    example_10_wordlist_operations()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)
    
    print("\n安全提示:")
    print("  1. 助记词是钱包的备份，请妥善保存")
    print("  2. 不要在不安全的地方存储助记词")
    print("  3. 使用密码短语可以增加额外安全层")
    print("  4. 24 词助记词提供最高安全级别 (256 bits)")
    print("  5. 测试时不要使用真实的助记词")


if __name__ == "__main__":
    main()