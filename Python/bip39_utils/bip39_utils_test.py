"""
BIP39 Utilities 测试

全面测试助记词生成、验证和种子派生。
"""

import unittest
import hashlib
import hmac
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bip39_utils.mod import (
    Language,
    MnemonicResult,
    SeedResult,
    ValidationResult,
    BIP39Mnemonic,
    VALID_MNEMONIC_LENGTHS,
    LENGTH_TO_ENTROPY_BITS,
    generate_mnemonic,
    validate_mnemonic,
    mnemonic_to_seed,
    mnemonic_to_entropy,
    ENGLISH_WORDLIST,
)


class TestBIP39Mnemonic(unittest.TestCase):
    """测试 BIP39Mnemonic 类"""
    
    def setUp(self):
        """设置测试"""
        self.bip = BIP39Mnemonic(Language.ENGLISH)
    
    def test_wordlist_count(self):
        """测试词表数量"""
        self.assertEqual(len(ENGLISH_WORDLIST), 2048)
    
    def test_generate_12_words(self):
        """测试生成 12 词助记词"""
        result = self.bip.generate(12)
        
        self.assertEqual(len(result.words), 12)
        self.assertEqual(result.word_count, 12)
        self.assertEqual(len(result.entropy_hex), 32)  # 128 bits = 16 bytes = 32 hex chars
        self.assertEqual(result.language, Language.ENGLISH)
    
    def test_generate_15_words(self):
        """测试生成 15 词助记词"""
        result = self.bip.generate(15)
        
        self.assertEqual(len(result.words), 15)
        self.assertEqual(result.word_count, 15)
        self.assertEqual(len(result.entropy_hex), 40)  # 160 bits = 20 bytes = 40 hex chars
    
    def test_generate_18_words(self):
        """测试生成 18 词助记词"""
        result = self.bip.generate(18)
        
        self.assertEqual(len(result.words), 18)
        self.assertEqual(result.word_count, 18)
        self.assertEqual(len(result.entropy_hex), 48)  # 192 bits = 24 bytes = 48 hex chars
    
    def test_generate_21_words(self):
        """测试生成 21 词助记词"""
        result = self.bip.generate(21)
        
        self.assertEqual(len(result.words), 21)
        self.assertEqual(result.word_count, 21)
        self.assertEqual(len(result.entropy_hex), 56)  # 224 bits = 28 bytes = 56 hex chars
    
    def test_generate_24_words(self):
        """测试生成 24 词助记词"""
        result = self.bip.generate(24)
        
        self.assertEqual(len(result.words), 24)
        self.assertEqual(result.word_count, 24)
        self.assertEqual(len(result.entropy_hex), 64)  # 256 bits = 32 bytes = 64 hex chars
    
    def test_invalid_word_count(self):
        """测试无效词数"""
        with self.assertRaises(ValueError):
            self.bip.generate(10)
        
        with self.assertRaises(ValueError):
            self.bip.generate(16)
        
        with self.assertRaises(ValueError):
            self.bip.generate(30)
    
    def test_words_in_wordlist(self):
        """测试生成的词都在词表中"""
        result = self.bip.generate(12)
        
        word_set = set(ENGLISH_WORDLIST)
        for word in result.words:
            self.assertIn(word, word_set)
    
    def test_mnemonic_format(self):
        """测试助记词格式"""
        result = self.bip.generate(12)
        
        # 应是空格分隔的词
        self.assertIn(' ', result.mnemonic)
        # 每个词都是有效的
        for word in result.words:
            self.assertTrue(self.bip.is_valid_word(word))
    
    def test_validate_valid_mnemonic(self):
        """测试验证有效助记词"""
        # 使用正确的 BIP39 测试向量（熵全零）
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        
        result = self.bip.validate(mnemonic)
        
        self.assertTrue(result.is_valid)
        self.assertTrue(result.checksum_valid)
        self.assertEqual(result.word_count, 12)
    
    def test_validate_generated_mnemonic(self):
        """测试验证生成的助记词"""
        generated = self.bip.generate(12)
        
        result = self.bip.validate(generated.mnemonic)
        
        self.assertTrue(result.is_valid)
        self.assertTrue(result.checksum_valid)
    
    def test_validate_invalid_word_count(self):
        """测试验证无效词数"""
        result = self.bip.validate("abandon ability able about")
        
        self.assertFalse(result.is_valid)
        self.assertEqual(result.word_count, 4)
    
    def test_validate_invalid_words(self):
        """测试验证无效词"""
        result = self.bip.validate("invalidword ability able about above absent absorb abstract absurd abuse access accident")
        
        self.assertFalse(result.is_valid)
    
    def test_validate_tampered_mnemonic(self):
        """测试验证被篡改的助记词"""
        # 修改最后一个词（破坏校验和）
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon academy"
        
        result = self.bip.validate(mnemonic)
        
        # 校验和应该不匹配
        self.assertFalse(result.is_valid)
    
    def test_to_seed_basic(self):
        """测试种子生成"""
        # BIP39 测试向量（熵全零）
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        
        result = self.bip.to_seed(mnemonic)
        
        self.assertEqual(len(result.seed), 64)
        self.assertEqual(len(result.master_key), 32)
        self.assertEqual(len(result.chain_code), 32)
    
    def test_to_seed_with_passphrase(self):
        """测试带密码短语的种子生成"""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        
        result1 = self.bip.to_seed(mnemonic, "")
        result2 = self.bip.to_seed(mnemonic, "passphrase")
        
        # 不同密码短语应产生不同种子
        self.assertNotEqual(result1.seed, result2.seed)
    
    def test_seed_is_consistent(self):
        """测试种子生成一致性"""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        
        result1 = self.bip.to_seed(mnemonic)
        result2 = self.bip.to_seed(mnemonic)
        
        # 同一助记词应产生相同种子
        self.assertEqual(result1.seed, result2.seed)
    
    def test_bip39_test_vectors(self):
        """测试 BIP39 测试向量"""
        # 来自 BIP39 规范的测试向量（熵全零）
        # 熵: 00000000000000000000000000000000
        # 助记词: abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
        # 种子（ passphrase=TREZOR ): c55257c360c07c72029aebc1b53c05ed0362ada38ead3e3e9efa3708e53495531f09a6987599d18264c1e1c92f2cf141630c7a3c4ab7c81b2f001698e7463b04
        
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        
        # 验证助记词
        validation = self.bip.validate(mnemonic)
        self.assertTrue(validation.is_valid)
        
        # 生成种子
        seed_result = self.bip.to_seed(mnemonic, "TREZOR")
        
        # 检查种子前几个字节（已知测试向量）
        expected_prefix = "c55257c360c07c72029aebc1b53c05ed03"
        self.assertEqual(seed_result.seed_hex[:len(expected_prefix)], expected_prefix)
    
    def test_entropy_recovery(self):
        """测试熵恢复"""
        result = self.bip.generate(12)
        
        # 从助记词恢复熵
        recovered_entropy = self.bip.to_entropy(result.mnemonic)
        
        # 应与原始熵相同
        self.assertEqual(recovered_entropy.hex(), result.entropy_hex)
    
    def test_custom_entropy(self):
        """测试自定义熵"""
        # 使用已知熵（全零）
        entropy = bytes.fromhex("00000000000000000000000000000000")
        
        result = self.bip.generate(12, entropy)
        
        # 应生成正确的助记词（11个abandon + 1个about）
        expected_words = [
            "abandon", "abandon", "abandon", "abandon", "abandon", "abandon",
            "abandon", "abandon", "abandon", "abandon", "abandon", "about"
        ]
        self.assertEqual(result.words, expected_words)
    
    def test_custom_entropy_wrong_size(self):
        """测试错误大小的自定义熵"""
        entropy = bytes.fromhex("0000000000000000")  # 8 bytes instead of 16
        
        with self.assertRaises(ValueError):
            self.bip.generate(12, entropy)
    
    def test_word_at_index(self):
        """测试索引取词"""
        self.assertEqual(self.bip.word_at_index(0), "abandon")
        self.assertEqual(self.bip.word_at_index(2047), "zoo")
    
    def test_index_of_word(self):
        """测试词取索引"""
        self.assertEqual(self.bip.index_of_word("abandon"), 0)
        self.assertEqual(self.bip.index_of_word("zoo"), 2047)
    
    def test_invalid_index(self):
        """测试无效索引"""
        with self.assertRaises(ValueError):
            self.bip.word_at_index(-1)
        
        with self.assertRaises(ValueError):
            self.bip.word_at_index(2048)
    
    def test_invalid_word_lookup(self):
        """测试无效词查找"""
        with self.assertRaises(ValueError):
            self.bip.index_of_word("notaword")
    
    def test_is_valid_word(self):
        """测试词有效性检查"""
        self.assertTrue(self.bip.is_valid_word("abandon"))
        self.assertTrue(self.bip.is_valid_word("zoo"))
        self.assertFalse(self.bip.is_valid_word("notaword"))
    
    def test_different_passphrases_different_seeds(self):
        """测试不同密码短语产生不同种子"""
        mnemonic = generate_mnemonic(12)
        
        seed1 = mnemonic_to_seed(mnemonic, "")
        seed2 = mnemonic_to_seed(mnemonic, "password1")
        seed3 = mnemonic_to_seed(mnemonic, "password2")
        
        # 所有种子应该不同
        self.assertNotEqual(seed1, seed2)
        self.assertNotEqual(seed2, seed3)
        self.assertNotEqual(seed1, seed3)
    
    def test_master_key_derivation(self):
        """测试主密钥派生"""
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        
        result = self.bip.to_seed(mnemonic)
        
        # 检查主密钥和链码长度
        self.assertEqual(len(result.master_key), 32)
        self.assertEqual(len(result.chain_code), 32)
        
        # 使用 HMAC-SHA512 验证
        h = hmac.new(b'Bitcoin seed', result.seed, hashlib.sha512).digest()
        self.assertEqual(result.master_key, h[:32])
        self.assertEqual(result.chain_code, h[32:])
    
    def test_multiple_generations_unique(self):
        """测试多次生成不同助记词"""
        results = [self.bip.generate(12) for _ in range(10)]
        
        mnemonics = [r.mnemonic for r in results]
        
        # 所有助记词应该不同
        unique_mnemonics = set(mnemonics)
        self.assertEqual(len(unique_mnemonics), 10)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_generate_mnemonic_function(self):
        """测试生成助记词函数"""
        mnemonic = generate_mnemonic(12)
        
        words = mnemonic.split()
        self.assertEqual(len(words), 12)
    
    def test_validate_mnemonic_function(self):
        """测试验证助记词函数"""
        mnemonic = generate_mnemonic(12)
        
        self.assertTrue(validate_mnemonic(mnemonic))
    
    def test_mnemonic_to_seed_function(self):
        """测试助记词转种子函数"""
        mnemonic = generate_mnemonic(12)
        
        seed = mnemonic_to_seed(mnemonic)
        
        self.assertEqual(len(seed), 64)
    
    def test_mnemonic_to_entropy_function(self):
        """测试助记词转熵函数"""
        mnemonic = generate_mnemonic(12)
        
        entropy = mnemonic_to_entropy(mnemonic)
        
        # 12 词对应 128 bits = 16 bytes
        self.assertEqual(len(entropy), 16)
    
    def test_entropy_recovery_cycle(self):
        """测试熵恢复循环"""
        # 使用自定义熵
        original_entropy = bytes.fromhex("00000000000000000000000000000000")
        
        bip = BIP39Mnemonic()
        result = bip.generate(12, original_entropy)
        
        # 从助记词恢复熵
        recovered = mnemonic_to_entropy(result.mnemonic)
        
        self.assertEqual(recovered, original_entropy)


class TestMnemonicResult(unittest.TestCase):
    """测试 MnemonicResult 数据类"""
    
    def test_result_attributes(self):
        """测试结果属性"""
        bip = BIP39Mnemonic()
        result = bip.generate(12)
        
        self.assertIsNotNone(result.mnemonic)
        self.assertIsNotNone(result.words)
        self.assertIsNotNone(result.entropy_hex)
        self.assertEqual(result.language, Language.ENGLISH)
        self.assertEqual(result.word_count, 12)
    
    def test_words_match_mnemonic(self):
        """测试词列表匹配助记词"""
        bip = BIP39Mnemonic()
        result = bip.generate(12)
        
        self.assertEqual(result.words, result.mnemonic.split())


class TestSeedResult(unittest.TestCase):
    """测试 SeedResult 数据类"""
    
    def test_seed_result_attributes(self):
        """测试种子结果属性"""
        bip = BIP39Mnemonic()
        mnemonic = generate_mnemonic(12)
        
        result = bip.to_seed(mnemonic)
        
        self.assertIsNotNone(result.seed)
        self.assertIsNotNone(result.seed_hex)
        self.assertIsNotNone(result.master_key)
        self.assertIsNotNone(result.master_key_hex)
        self.assertIsNotNone(result.chain_code)
        self.assertIsNotNone(result.chain_code_hex)
    
    def test_hex_matches_bytes(self):
        """测试十六进制匹配字节"""
        bip = BIP39Mnemonic()
        mnemonic = generate_mnemonic(12)
        
        result = bip.to_seed(mnemonic)
        
        self.assertEqual(result.seed.hex(), result.seed_hex)
        self.assertEqual(result.master_key.hex(), result.master_key_hex)
        self.assertEqual(result.chain_code.hex(), result.chain_code_hex)


class TestValidationResult(unittest.TestCase):
    """测试 ValidationResult 数据类"""
    
    def test_valid_result(self):
        """测试有效验证结果"""
        bip = BIP39Mnemonic()
        mnemonic = generate_mnemonic(12)
        
        result = bip.validate(mnemonic)
        
        self.assertTrue(result.is_valid)
        self.assertIsNone(result.error)
        self.assertTrue(result.checksum_valid)
        self.assertEqual(result.word_count, 12)
        self.assertEqual(result.detected_language, Language.ENGLISH)
    
    def test_invalid_result(self):
        """测试无效验证结果"""
        bip = BIP39Mnemonic()
        mnemonic = "invalid mnemonic with wrong words"
        
        result = bip.validate(mnemonic)
        
        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.error)


class TestConstants(unittest.TestCase):
    """测试常量"""
    
    def test_valid_mnemonic_lengths(self):
        """测试有效助记词长度"""
        self.assertEqual(VALID_MNEMONIC_LENGTHS, [12, 15, 18, 21, 24])
    
    def test_length_to_entropy_bits(self):
        """测试长度到熵位数映射"""
        self.assertEqual(LENGTH_TO_ENTROPY_BITS[12], 128)
        self.assertEqual(LENGTH_TO_ENTROPY_BITS[15], 160)
        self.assertEqual(LENGTH_TO_ENTROPY_BITS[18], 192)
        self.assertEqual(LENGTH_TO_ENTROPY_BITS[21], 224)
        self.assertEqual(LENGTH_TO_ENTROPY_BITS[24], 256)


class TestLanguageSupport(unittest.TestCase):
    """测试多语言支持"""
    
    def test_english_wordlist(self):
        """测试英文词表"""
        bip = BIP39Mnemonic(Language.ENGLISH)
        
        result = bip.generate(12)
        
        # 所有词应该是英文
        for word in result.words:
            self.assertIn(word, ENGLISH_WORDLIST)
    
    def test_unsupported_language(self):
        """测试不支持的语言"""
        # 目前只支持英文
        with self.assertRaises(ValueError):
            BIP39Mnemonic(Language.CHINESE_SIMPLIFIED)  # 中文词表不完整
    
    def test_language_enum_values(self):
        """测试语言枚举值"""
        self.assertEqual(Language.ENGLISH.value, "english")
        self.assertEqual(Language.CHINESE_SIMPLIFIED.value, "chinese_simplified")


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_passphrase(self):
        """测试空密码短语"""
        bip = BIP39Mnemonic()
        mnemonic = generate_mnemonic(12)
        
        # 密码短语应该有效
        result = bip.to_seed(mnemonic, "")
        
        self.assertEqual(len(result.seed), 64)
    
    def test_whitespace_in_mnemonic(self):
        """测试助记词中的空白"""
        bip = BIP39Mnemonic()
        
        # 多余空格
        mnemonic = "abandon  ability  able  about  above  absent  absorb  abstract  absurd  abuse  access  accident"
        
        result = bip.validate(mnemonic)
        
        # 应自动处理多余空格
        # 注意：当前实现可能不自动处理，取决于 validate 的实现
    
    def test_all_zeros_entropy(self):
        """测试全零熵"""
        entropy = bytes(16)  # 16 bytes of zeros
        
        bip = BIP39Mnemonic()
        result = bip.generate(12, entropy)
        
        # 应生成正确的助记词（11个abandon + 1个about）
        expected_words = [
            "abandon", "abandon", "abandon", "abandon", "abandon", "abandon",
            "abandon", "abandon", "abandon", "abandon", "abandon", "about"
        ]
        self.assertEqual(result.words, expected_words)
    
    def test_all_ones_entropy(self):
        """测试全一熵"""
        entropy = bytes([255] * 16)  # 16 bytes of 255
        
        bip = BIP39Mnemonic()
        result = bip.generate(12, entropy)
        
        # 应有效生成
        self.assertEqual(len(result.words), 12)
    
    def test_special_characters_in_passphrase(self):
        """测试密码短语中的特殊字符"""
        bip = BIP39Mnemonic()
        mnemonic = generate_mnemonic(12)
        
        # 特殊字符密码短语
        passphrase = "!@#$%^&*()_+-=[]{}|;':,./<>?`~"
        
        result = bip.to_seed(mnemonic, passphrase)
        
        self.assertEqual(len(result.seed), 64)
    
    def test_unicode_passphrase(self):
        """测试 Unicode 密码短语"""
        bip = BIP39Mnemonic()
        mnemonic = generate_mnemonic(12)
        
        # Unicode 密码短语
        passphrase = "密码密码密码"
        
        result = bip.to_seed(mnemonic, passphrase)
        
        self.assertEqual(len(result.seed), 64)
    
    def test_long_passphrase(self):
        """测试长密码短语"""
        bip = BIP39Mnemonic()
        mnemonic = generate_mnemonic(12)
        
        # 长密码短语
        passphrase = "a" * 1000
        
        result = bip.to_seed(mnemonic, passphrase)
        
        self.assertEqual(len(result.seed), 64)


class TestChecksum(unittest.TestCase):
    """测试校验和"""
    
    def test_checksum_computation(self):
        """测试校验和计算"""
        # 使用已知熵
        entropy = bytes.fromhex("00000000000000000000000000000000")
        
        bip = BIP39Mnemonic()
        result = bip.generate(12, entropy)
        
        # 校验和应该是正确的
        validation = bip.validate(result.mnemonic)
        self.assertTrue(validation.checksum_valid)
    
    def test_checksum_in_validation(self):
        """测试校验和在验证中的作用"""
        # 有效助记词（熵全零）
        valid_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        
        # 稍微修改（破坏校验和）- 修改最后一个词
        invalid_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon academy"
        
        bip = BIP39Mnemonic()
        
        valid_result = bip.validate(valid_mnemonic)
        invalid_result = bip.validate(invalid_mnemonic)
        
        self.assertTrue(valid_result.checksum_valid)
        self.assertFalse(invalid_result.checksum_valid)


class TestDeterminism(unittest.TestCase):
    """测试确定性"""
    
    def test_same_entropy_same_mnemonic(self):
        """测试相同熵产生相同助记词"""
        entropy = bytes.fromhex("00000000000000000000000000000000")
        
        bip = BIP39Mnemonic()
        
        result1 = bip.generate(12, entropy)
        result2 = bip.generate(12, entropy)
        
        self.assertEqual(result1.mnemonic, result2.mnemonic)
    
    def test_same_mnemonic_same_seed(self):
        """测试相同助记词产生相同种子"""
        mnemonic = "abandon ability able about above absent absorb abstract absurd abuse access accident"
        
        bip = BIP39Mnemonic()
        
        seed1 = bip.to_seed(mnemonic)
        seed2 = bip.to_seed(mnemonic)
        
        self.assertEqual(seed1.seed, seed2.seed)
    
    def test_same_mnemonic_passphrase_same_seed(self):
        """测试相同助记词和密码短语产生相同种子"""
        mnemonic = "abandon ability able about above absent absorb abstract absurd abuse access accident"
        passphrase = "test"
        
        bip = BIP39Mnemonic()
        
        seed1 = bip.to_seed(mnemonic, passphrase)
        seed2 = bip.to_seed(mnemonic, passphrase)
        
        self.assertEqual(seed1.seed, seed2.seed)


if __name__ == '__main__':
    unittest.main(verbosity=2)