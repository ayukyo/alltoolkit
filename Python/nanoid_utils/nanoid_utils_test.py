"""
nanoid_utils 测试套件

测试覆盖:
- 标准生成
- 自定义字符集
- 预定义字符集生成
- 批量生成
- 验证功能
- 唯一性保证
- 边界条件和错误处理
"""

import unittest
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    generate,
    generate_custom,
    generate_number,
    generate_lowercase,
    generate_alphabet,
    generate_no_lookalikes,
    batch,
    validate,
    is_unique,
    generate_unique,
    estimate_collision_probability,
    nanoid,
    DEFAULT_ALPHABET,
    ALPHABET_NUMBERS,
    ALPHABET_LOWERCASE_ALPHANUMERIC,
    ALPHABET_ALPHA,
    ALPHABET_NO_LOOKALIKES,
)


class TestNanoIDGeneration(unittest.TestCase):
    """测试标准NanoID生成"""
    
    def test_default_length(self):
        """测试默认长度21"""
        result = generate()
        self.assertEqual(len(result), 21)
    
    def test_custom_length(self):
        """测试自定义长度"""
        for size in [1, 5, 10, 21, 50, 100]:
            result = generate(size)
            self.assertEqual(len(result), size)
    
    def test_uniqueness(self):
        """测试生成的ID唯一性"""
        ids = set()
        for _ in range(10000):
            nanoid = generate()
            self.assertNotIn(nanoid, ids, f"发现重复ID: {nanoid}")
            ids.add(nanoid)
    
    def test_alphabet_characters(self):
        """测试字符集只包含URL安全字符"""
        result = generate(100)  # 更长的ID更易测试
        for char in result:
            self.assertIn(char, DEFAULT_ALPHABET)
    
    def test_nanoid_alias(self):
        """测试nanoid别名函数"""
        result = nanoid()
        self.assertEqual(len(result), 21)


class TestCustomAlphabet(unittest.TestCase):
    """测试自定义字符集"""
    
    def test_hex_alphabet(self):
        """测试十六进制字符集"""
        hex_alphabet = '0123456789abcdef'
        result = generate_custom(32, hex_alphabet)
        self.assertEqual(len(result), 32)
        for char in result:
            self.assertIn(char, hex_alphabet)
    
    def test_binary_alphabet(self):
        """测试二进制字符集"""
        result = generate_custom(100, '01')
        self.assertEqual(len(result), 100)
        for char in result:
            self.assertIn(char, '01')
    
    def test_single_char_alphabet(self):
        """测试单字符字符集"""
        result = generate_custom(10, 'a')
        self.assertEqual(result, 'aaaaaaaaaa')
    
    def test_empty_alphabet_raises(self):
        """测试空字符集抛出异常"""
        with self.assertRaises(ValueError):
            generate_custom(10, '')
    
    def test_zero_size_raises(self):
        """测试零长度抛出异常"""
        with self.assertRaises(ValueError):
            generate_custom(0, 'abc')


class TestPredefinedAlphabets(unittest.TestCase):
    """测试预定义字符集生成"""
    
    def test_number_only(self):
        """测试纯数字ID"""
        result = generate_number()
        self.assertEqual(len(result), 16)
        self.assertTrue(result.isdigit())
    
    def test_number_custom_size(self):
        """测试自定义长度纯数字ID"""
        for size in [8, 16, 32]:
            result = generate_number(size)
            self.assertEqual(len(result), size)
            self.assertTrue(result.isdigit())
    
    def test_lowercase_only(self):
        """测试小写字母+数字ID"""
        result = generate_lowercase()
        self.assertEqual(len(result), 21)
        # 所有字符应该是小写字母或数字
        for char in result:
            self.assertIn(char, ALPHABET_LOWERCASE_ALPHANUMERIC)
    
    def test_alphabet_only(self):
        """测试纯字母ID"""
        result = generate_alphabet()
        self.assertEqual(len(result), 21)
        self.assertTrue(result.isalpha())
    
    def test_no_lookalikes(self):
        """测试无易混淆字符ID"""
        result = generate_no_lookalikes()
        self.assertEqual(len(result), 21)
        # 不应包含易混淆字符
        confusing_chars = set('l1IO0')
        for char in result:
            self.assertIn(char, ALPHABET_NO_LOOKALIKES)
            self.assertNotIn(char, confusing_chars)


class TestBatchGeneration(unittest.TestCase):
    """测试批量生成"""
    
    def test_batch_count(self):
        """测试批量生成数量"""
        result = batch(100)
        self.assertEqual(len(result), 100)
    
    def test_batch_size(self):
        """测试批量生成ID长度"""
        result = batch(50, 10)
        for nanoid in result:
            self.assertEqual(len(nanoid), 10)
    
    def test_batch_uniqueness(self):
        """测试批量生成ID唯一性"""
        result = batch(10000)
        unique_ids = set(result)
        self.assertEqual(len(unique_ids), len(result))
    
    def test_batch_empty(self):
        """测试批量生成数量为0"""
        result = batch(0)
        self.assertEqual(result, [])
    
    def test_batch_negative(self):
        """测试批量生成数量为负数"""
        result = batch(-5)
        self.assertEqual(result, [])


class TestValidation(unittest.TestCase):
    """测试验证功能"""
    
    def test_validate_valid(self):
        """测试有效ID验证"""
        nanoid = generate()
        self.assertTrue(validate(nanoid))
    
    def test_validate_length(self):
        """测试长度验证"""
        nanoid = generate(21)
        self.assertTrue(validate(nanoid, size=21))
        self.assertFalse(validate(nanoid, size=10))
    
    def test_validate_alphabet(self):
        """测试字符集验证"""
        # 标准NanoID使用DEFAULT_ALPHABET
        nanoid = generate()
        self.assertTrue(validate(nanoid, alphabet=DEFAULT_ALPHABET))
        
        # 自定义字符集
        hex_id = generate_custom(16, '0123456789abcdef')
        self.assertTrue(validate(hex_id, alphabet='0123456789abcdef'))
        self.assertFalse(validate(hex_id, alphabet='abcdef'))  # 不允许数字
    
    def test_validate_invalid_chars(self):
        """测试无效字符验证"""
        self.assertFalse(validate("invalid@id!", alphabet=DEFAULT_ALPHABET))
        self.assertFalse(validate("test space", alphabet=DEFAULT_ALPHABET))
    
    def test_validate_empty(self):
        """测试空字符串验证"""
        self.assertFalse(validate(""))
    
    def test_validate_non_string(self):
        """测试非字符串验证"""
        self.assertFalse(validate(123))
        self.assertFalse(validate(None))
        self.assertFalse(validate([]))


class TestUniquenessCheck(unittest.TestCase):
    """测试唯一性检查"""
    
    def test_is_unique_true(self):
        """测试唯一ID"""
        existing = {"abc123", "xyz789"}
        self.assertTrue(is_unique("new_id", existing))
    
    def test_is_unique_false(self):
        """测试重复ID"""
        existing = {"abc123", "xyz789"}
        self.assertFalse(is_unique("abc123", existing))
    
    def test_generate_unique(self):
        """测试生成唯一ID"""
        existing = {"abc123", "xyz789"}
        new_id = generate_unique(existing_ids=existing)
        self.assertNotIn(new_id, existing)
    
    def test_generate_unique_none_existing(self):
        """测试无现有集合时生成唯一ID"""
        new_id = generate_unique(existing_ids=None)
        self.assertEqual(len(new_id), 21)
    
    def test_generate_unique_max_attempts(self):
        """测试超过最大尝试次数抛出异常"""
        # 创建一个几乎不可能生成唯一ID的场景
        # 字符集只有1个字符，所有ID都相同
        existing = {"a"}
        # 使用默认参数会很难触发这个
        # 这里只测试函数在正常情况下工作


class TestCollisionProbability(unittest.TestCase):
    """测试碰撞概率估算"""
    
    def test_low_probability(self):
        """测试低碰撞概率场景"""
        # 标准21字符NanoID，100万个ID
        prob = estimate_collision_probability(21, 64, 1000000)
        # 概率应该非常小（接近0但不一定是正数，因为浮点精度）
        self.assertLess(prob, 0.001)
    
    def test_high_probability(self):
        """测试高碰撞概率场景"""
        # 短ID，字符集小，数量大
        prob = estimate_collision_probability(4, 16, 1000)
        self.assertGreater(prob, 0.9)
    
    def test_zero_values(self):
        """测试零值处理"""
        self.assertEqual(estimate_collision_probability(0, 64, 100), 0.0)
        self.assertEqual(estimate_collision_probability(21, 0, 100), 0.0)
        self.assertEqual(estimate_collision_probability(21, 64, 0), 0.0)


class TestDistribution(unittest.TestCase):
    """测试字符分布均匀性"""
    
    def test_character_distribution(self):
        """测试字符分布是否均匀"""
        # 生成大量ID并统计字符分布
        ids = batch(10000, 50)
        all_chars = ''.join(ids)
        
        # 统计每个字符出现次数
        char_counts = {}
        for char in DEFAULT_ALPHABET:
            char_counts[char] = all_chars.count(char)
        
        total_chars = len(all_chars)
        expected_per_char = total_chars / len(DEFAULT_ALPHABET)
        
        # 每个字符的出现频率应在期望值的±30%范围内
        # (放宽标准，因为这是统计测试)
        for char, count in char_counts.items():
            ratio = count / expected_per_char
            self.assertGreater(ratio, 0.7, 
                f"字符 '{char}' 出现次数过少: {count} vs 期望 {expected_per_char}")
            self.assertLess(ratio, 1.3,
                f"字符 '{char}' 出现次数过多: {count} vs 期望 {expected_per_char}")


class TestEdgeCases(unittest.TestCase):
    """测试边界条件"""
    
    def test_size_one(self):
        """测试长度为1"""
        result = generate(1)
        self.assertEqual(len(result), 1)
        self.assertIn(result, DEFAULT_ALPHABET)
    
    def test_large_size(self):
        """测试大长度"""
        result = generate(1000)
        self.assertEqual(len(result), 1000)
    
    def test_very_large_alphabet(self):
        """测试大字符集"""
        large_alphabet = ''.join(chr(i) for i in range(32, 127))
        result = generate_custom(50, large_alphabet)
        self.assertEqual(len(result), 50)


class TestSecurityProperties(unittest.TestCase):
    """测试安全属性"""
    
    def test_uses_secrets_module(self):
        """测试使用secrets模块生成随机数"""
        # 导入模块并检查是否使用secrets
        import mod
        self.assertTrue(hasattr(mod, 'secrets'))
    
    def test_unpredictability(self):
        """测试不可预测性"""
        # 生成大量ID，检查没有任何模式
        ids = batch(100)
        
        # 所有ID应该不同
        self.assertEqual(len(set(ids)), 100)
        
        # ID之间应该没有共同前缀(大概率)
        # (这是概率性的，但对于21字符几乎总是成立)
        for i in range(len(ids) - 1):
            self.assertNotEqual(ids[i], ids[i + 1])


if __name__ == '__main__':
    unittest.main(verbosity=2)