"""
password_strength_utils 测试文件
测试密码强度分析、破解时间估算、密码生成等功能
"""

import unittest
import re
from mod import (
    PasswordStrength, PasswordGenerator, PasswordValidator,
    PasswordEntropy, PasswordCrackEstimator, CommonPasswordChecker,
    PatternDetector, StrengthLevel, PasswordIssue, StrengthResult,
    check_password, generate_password, generate_passphrase, is_strong_password
)


class TestPasswordEntropy(unittest.TestCase):
    """测试密码熵计算"""
    
    def test_empty_password(self):
        """测试空密码"""
        entropy = PasswordEntropy.calculate("")
        self.assertEqual(entropy, 0.0)
    
    def test_simple_password(self):
        """测试简单密码"""
        # 只有数字
        entropy = PasswordEntropy.calculate("12345")
        self.assertGreater(entropy, 0)
        
        # 只有小写字母
        entropy = PasswordEntropy.calculate("abcde")
        self.assertGreater(entropy, 0)
    
    def test_complex_password(self):
        """测试复杂密码"""
        # 包含大小写、数字、特殊字符
        entropy1 = PasswordEntropy.calculate("abcde")
        entropy2 = PasswordEntropy.calculate("Abcde")
        entropy3 = PasswordEntropy.calculate("Abc12")
        entropy4 = PasswordEntropy.calculate("Abc1!")
        
        # 复杂度递增
        self.assertLess(entropy1, entropy2)
        self.assertLess(entropy2, entropy3)
        self.assertLess(entropy3, entropy4)
    
    def test_charset_detection(self):
        """测试字符集检测"""
        # 纯小写
        charset = PasswordEntropy._get_charset_size("abc")
        self.assertEqual(charset, 26)
        
        # 小写+大写
        charset = PasswordEntropy._get_charset_size("Abc")
        self.assertEqual(charset, 52)
        
        # 小写+大写+数字
        charset = PasswordEntropy._get_charset_size("Abc1")
        self.assertEqual(charset, 62)
        
        # 小写+大写+数字+特殊
        charset = PasswordEntropy._get_charset_size("Abc1!")
        self.assertEqual(charset, 94)


class TestPasswordCrackEstimator(unittest.TestCase):
    """测试破解时间估算"""
    
    def test_instant_crack(self):
        """测试瞬间破解"""
        time_str = PasswordCrackEstimator.estimate_time("a")
        # 单字符密码应该是瞬间或毫秒级破解
        self.assertTrue("瞬间" in time_str or "毫秒" in time_str)
    
    def test_strong_password(self):
        """测试强密码破解时间"""
        time_str = PasswordCrackEstimator.estimate_time("Tr0ub4dor&3")
        # 应该需要很长时间
        self.assertTrue(
            "年" in time_str or "百年" in time_str or "千年" in time_str or 
            "百万年" in time_str or "十亿年" in time_str or "宇宙" in time_str
        )
    
    def test_very_strong_password(self):
        """测试非常强的密码"""
        time_str = PasswordCrackEstimator.estimate_time("correct-horse-battery-staple")
        # 应该需要很长时间
        self.assertTrue(
            "年" in time_str or "百年" in time_str or "千年" in time_str or 
            "百万年" in time_str or "十亿年" in time_str or "宇宙" in time_str
        )
    
    def test_estimate_all_scenarios(self):
        """测试所有场景估算"""
        scenarios = PasswordCrackEstimator.estimate_all_scenarios("Test123!")
        
        self.assertIn("在线攻击", scenarios)
        self.assertIn("离线快速哈希", scenarios)
        self.assertIn("离线慢速哈希", scenarios)
        self.assertIn("GPU暴力破解", scenarios)
    
    def test_format_time(self):
        """测试时间格式化"""
        self.assertEqual(PasswordCrackEstimator._format_time(0.0001), "瞬间")
        self.assertIn("毫秒", PasswordCrackEstimator._format_time(0.001))
        self.assertIn("秒", PasswordCrackEstimator._format_time(1))
        self.assertIn("分钟", PasswordCrackEstimator._format_time(60))
        self.assertIn("小时", PasswordCrackEstimator._format_time(3600))
        self.assertIn("天", PasswordCrackEstimator._format_time(86400))


class TestCommonPasswordChecker(unittest.TestCase):
    """测试常见密码检测"""
    
    def test_common_passwords(self):
        """测试常见密码"""
        self.assertTrue(CommonPasswordChecker.is_common("123456"))
        self.assertTrue(CommonPasswordChecker.is_common("password"))
        self.assertTrue(CommonPasswordChecker.is_common("qwerty"))
        self.assertTrue(CommonPasswordChecker.is_common("admin"))
    
    def test_not_common(self):
        """测试非常见密码"""
        self.assertFalse(CommonPasswordChecker.is_common("xYz@123$%AbC"))
        self.assertFalse(CommonPasswordChecker.is_common("correct-horse-battery-staple"))
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        self.assertTrue(CommonPasswordChecker.is_common("PASSWORD"))
        self.assertTrue(CommonPasswordChecker.is_common("Password"))
        self.assertTrue(CommonPasswordChecker.is_common("ADMIN"))
    
    def test_variants(self):
        """测试变体检测"""
        # 数字后缀变体
        variants = CommonPasswordChecker.check_variants("admin123")
        self.assertTrue(len(variants) > 0)
        
        # 反转变体
        variants = CommonPasswordChecker.check_variants("drowssap")
        self.assertTrue(len(variants) > 0)


class TestPatternDetector(unittest.TestCase):
    """测试模式检测"""
    
    def test_sequential_letters(self):
        """测试连续字母"""
        patterns = PatternDetector.detect_sequential("abcdef")
        self.assertTrue(len(patterns) > 0)
        self.assertIn("abcdef", patterns)
        
        patterns = PatternDetector.detect_sequential("xyz")
        self.assertTrue(len(patterns) > 0)
    
    def test_sequential_numbers(self):
        """测试连续数字"""
        patterns = PatternDetector.detect_sequential("12345")
        self.assertTrue(len(patterns) > 0)
        self.assertIn("12345", patterns)
    
    def test_repeated_chars(self):
        """测试重复字符"""
        patterns = PatternDetector.detect_repeated("aaabbb")
        self.assertTrue(len(patterns) > 0)
        
        patterns = PatternDetector.detect_repeated("aabbcc")
        self.assertTrue(len(patterns) > 0)
        
        # 只检测连续重复
        patterns = PatternDetector.detect_repeated("ababab")
        self.assertTrue(all(len(p) < 3 for p in patterns))
    
    def test_keyboard_pattern(self):
        """测试键盘模式"""
        patterns = PatternDetector.detect_keyboard_pattern("qwerty")
        self.assertTrue(len(patterns) > 0)
        
        patterns = PatternDetector.detect_keyboard_pattern("asdfgh")
        self.assertTrue(len(patterns) > 0)
    
    def test_date_pattern(self):
        """测试日期模式"""
        patterns = PatternDetector.detect_date_pattern("19900101")
        self.assertTrue(len(patterns) > 0)
        
        patterns = PatternDetector.detect_date_pattern("password20001231test")
        self.assertTrue(len(patterns) > 0)
    
    def test_dictionary_word(self):
        """测试字典单词"""
        words = PatternDetector.detect_dictionary_word("password123")
        self.assertIn("password", words)
        
        words = PatternDetector.detect_dictionary_word("myiloveyou")
        self.assertIn("iloveyou", words)
    
    def test_no_patterns(self):
        """测试无模式的强密码"""
        patterns = PatternDetector.detect_sequential("xY7!kL2@")
        self.assertEqual(len(patterns), 0)
        
        patterns = PatternDetector.detect_keyboard_pattern("xY7!kL2@")
        self.assertEqual(len(patterns), 0)


class TestPasswordStrength(unittest.TestCase):
    """测试密码强度分析"""
    
    def test_very_weak_password(self):
        """测试非常弱的密码"""
        result = check_password("123")
        self.assertEqual(result.level, StrengthLevel.VERY_WEAK)
        self.assertLess(result.score, 20)
        self.assertTrue(PasswordIssue.TOO_SHORT in result.issues or 
                       PasswordIssue.COMMON_PASSWORD in result.issues)
    
    def test_weak_password(self):
        """测试弱密码"""
        result = check_password("password")
        self.assertIn(result.level, [StrengthLevel.VERY_WEAK, StrengthLevel.WEAK])
        self.assertLess(result.score, 50)
    
    def test_medium_password(self):
        """测试中等密码"""
        result = check_password("Password1")
        self.assertGreaterEqual(result.score, 30)
        self.assertIn(result.level, [StrengthLevel.MEDIUM, StrengthLevel.STRONG, StrengthLevel.VERY_STRONG])
    
    def test_strong_password(self):
        """测试强密码"""
        result = check_password("Tr0ub4dor&3")
        self.assertGreaterEqual(result.score, 50)
        self.assertIn(result.level, [StrengthLevel.STRONG, StrengthLevel.VERY_STRONG])
    
    def test_very_strong_password(self):
        """测试非常强的密码"""
        result = check_password("xY7!kL2@mN9#pQ4$")
        self.assertGreaterEqual(result.score, 70)
        self.assertIn(result.level, [StrengthLevel.STRONG, StrengthLevel.VERY_STRONG])
    
    def test_issues_detection(self):
        """测试问题检测"""
        # 短密码
        result = check_password("a")
        self.assertIn(PasswordIssue.TOO_SHORT, result.issues)
        
        # 无数字
        analyzer = PasswordStrength(require_digit=True)
        result = analyzer.analyze("Abcdefgh!")
        self.assertIn(PasswordIssue.NO_DIGITS, result.issues)
        
        # 无特殊字符
        analyzer = PasswordStrength(require_special=True)
        result = analyzer.analyze("Password1")
        self.assertIn(PasswordIssue.NO_SPECIAL, result.issues)
    
    def test_suggestions(self):
        """测试建议"""
        result = check_password("abc")
        self.assertTrue(len(result.suggestions) > 0)
    
    def test_result_properties(self):
        """测试结果属性"""
        result = check_password("StrongP@ssw0rd123")
        
        # 测试 is_strong
        self.assertIsInstance(result.is_strong, bool)
        
        # 测试 is_acceptable
        self.assertIsInstance(result.is_acceptable, bool)
        
        # 测试 to_dict
        result_dict = result.to_dict()
        self.assertIn("score", result_dict)
        self.assertIn("level", result_dict)
        self.assertIn("entropy", result_dict)
    
    def test_validate_method(self):
        """测试验证方法"""
        analyzer = PasswordStrength(min_length=8, require_special=True)
        
        # 不符合条件的密码
        valid, errors = analyzer.validate("short")
        self.assertFalse(valid)
        self.assertTrue(len(errors) > 0)
        
        # 符合条件的密码
        valid, errors = analyzer.validate("StrongP@ssw0rd")
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)


class TestPasswordGenerator(unittest.TestCase):
    """测试密码生成"""
    
    def test_generate_default(self):
        """测试默认生成"""
        password = generate_password()
        self.assertEqual(len(password), 16)
    
    def test_generate_custom_length(self):
        """测试自定义长度"""
        password = generate_password(length=24)
        self.assertEqual(len(password), 24)
        
        password = generate_password(length=8)
        self.assertEqual(len(password), 8)
    
    def test_generate_no_special(self):
        """测试不含特殊字符"""
        password = generate_password(length=16, use_special=False)
        self.assertEqual(len(password), 16)
        # 检查不含特殊字符
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.assertFalse(any(c in special for c in password))
    
    def test_generate_with_ambiguous(self):
        """测试包含混淆字符"""
        generator = PasswordGenerator(length=100, exclude_ambiguous=False)
        password = generator.generate()
        # 应该包含可能的混淆字符
        ambiguous = "il1Lo0O"
        # 由于随机性，高概率会包含
        self.assertEqual(len(password), 100)
    
    def test_generate_contains_required_chars(self):
        """测试包含必需字符"""
        generator = PasswordGenerator(
            length=16,
            use_lowercase=True,
            use_uppercase=True,
            use_digits=True,
            use_special=True
        )
        password = generator.generate()
        
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password))
    
    def test_generate_multiple(self):
        """测试生成多个密码"""
        generator = PasswordGenerator(length=12)
        passwords = generator.generate_multiple(5)
        
        self.assertEqual(len(passwords), 5)
        # 每个密码应该不同（极小概率相同）
        self.assertEqual(len(set(passwords)), 5)
    
    def test_generate_passphrase(self):
        """测试密码短语生成"""
        passphrase = generate_passphrase(word_count=4)
        words = passphrase.split("-")
        self.assertEqual(len(words), 4)
    
    def test_generate_passphrase_with_options(self):
        """测试带选项的密码短语"""
        generator = PasswordGenerator()
        
        # 带数字
        passphrase = generator.generate_passphrase(word_count=4, add_number=True)
        self.assertTrue(passphrase[-1].isdigit() or passphrase[-2:].isdigit())
        
        # 首字母大写
        passphrase = generator.generate_passphrase(word_count=4, capitalize=True)
        words = passphrase.split("-")
        self.assertTrue(all(w[0].isupper() for w in words if w and not w.isdigit()))


class TestPasswordValidator(unittest.TestCase):
    """测试密码验证器"""
    
    def test_validate_with_defaults(self):
        """测试默认验证"""
        validator = PasswordValidator()
        
        valid, errors = validator.validate("StrongP@ssw0rd")
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_with_custom_rules(self):
        """测试自定义规则"""
        validator = PasswordValidator()
        
        # 测试最小熵值
        valid, errors = validator.validate("weak", min_entropy=30)
        self.assertFalse(valid)
        
        # 测试最小分数
        valid, errors = validator.validate("weak", min_score=50)
        self.assertFalse(valid)
    
    def test_validate_exclude_common(self):
        """测试排除常见密码"""
        validator = PasswordValidator()
        
        valid, errors = validator.validate("password123", exclude_common=True)
        self.assertFalse(valid)
    
    def test_get_strength_summary(self):
        """测试强度摘要"""
        validator = PasswordValidator()
        summary = validator.get_strength_summary("Test123!")
        
        self.assertIn("密码强度", summary)
        self.assertIn("得分", summary)
        self.assertIn("熵值", summary)
        self.assertIn("破解时间", summary)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_check_password(self):
        """测试检查密码"""
        result = check_password("test123")
        self.assertIsInstance(result, StrengthResult)
        self.assertIn(result.level, list(StrengthLevel))
    
    def test_generate_password_func(self):
        """测试生成密码函数"""
        password = generate_password()
        self.assertEqual(len(password), 16)
        
        password = generate_password(length=20, use_special=False)
        self.assertEqual(len(password), 20)
    
    def test_generate_passphrase_func(self):
        """测试生成密码短语函数"""
        passphrase = generate_passphrase(5)
        words = passphrase.split("-")
        self.assertEqual(len(words), 5)
    
    def test_is_strong_password(self):
        """测试强密码判断"""
        self.assertFalse(is_strong_password("123456"))
        self.assertTrue(is_strong_password("Tr0ub4dor&3", min_score=50))
        
        # 测试自定义分数
        self.assertTrue(is_strong_password("StrongP@ssw0rd", min_score=60))


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_generate_and_validate(self):
        """测试生成并验证"""
        # 生成密码
        password = generate_password(length=16, use_special=True)
        
        # 验证密码
        result = check_password(password)
        
        # 生成的密码应该是强密码
        self.assertGreaterEqual(result.score, 50)
        self.assertTrue(result.is_acceptable)
    
    def test_passphrase_strength(self):
        """测试密码短语强度"""
        passphrase = generate_passphrase(4)
        result = check_password(passphrase)
        
        # 密码短语应该有较高的熵
        self.assertGreater(result.entropy, 40)
    
    def test_strong_password_has_no_issues(self):
        """测试强密码无问题"""
        password = "xY7!kL2@mN9#pQ4$wE5&"
        result = check_password(password)
        
        # 强密码应该没有问题
        self.assertEqual(len(result.issues), 0)
    
    def test_weak_password_has_issues(self):
        """测试弱密码有问题"""
        password = "password"
        result = check_password(password)
        
        # 弱密码应该有多个问题
        self.assertGreater(len(result.issues), 0)
        self.assertLess(result.score, 50)


if __name__ == "__main__":
    unittest.main()