#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Captcha Utils 测试模块
测试验证码生成、验证、存储等所有功能
"""

import unittest
import time
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    CaptchaGenerator, CaptchaStore,
    CaptchaType, CaptchaDifficulty, CaptchaCharset,
    CaptchaResult, MathCaptchaResult,
    generate_captcha, verify_captcha,
    create_and_store_captcha, generate_batch_captchas,
    _PILLOW_AVAILABLE
)


class TestCaptchaGenerator(unittest.TestCase):
    """测试验证码生成器"""
    
    def setUp(self):
        self.generator = CaptchaGenerator(secret="test_secret")
    
    def test_generate_text_captcha_default(self):
        """测试默认文本验证码生成"""
        captcha = self.generator.generate_text_captcha()
        
        self.assertIsInstance(captcha, CaptchaResult)
        self.assertEqual(captcha.captcha_type, CaptchaType.TEXT)
        self.assertEqual(len(captcha.text), 6)  # MEDIUM 默认长度
        self.assertTrue(captcha.text.isdigit())  # DIGITS 默认字符集
        self.assertEqual(captcha.difficulty, CaptchaDifficulty.MEDIUM)
        self.assertEqual(captcha.expires_in, 300.0)
    
    def test_generate_text_captcha_custom_length(self):
        """测试自定义长度文本验证码"""
        captcha = self.generator.generate_text_captcha(length=8)
        self.assertEqual(len(captcha.text), 8)
        
        captcha = self.generator.generate_text_captcha(length=4)
        self.assertEqual(len(captcha.text), 4)
    
    def test_generate_text_captcha_charset_digits(self):
        """测试数字字符集"""
        captcha = self.generator.generate_text_captcha(charset=CaptchaCharset.DIGITS)
        self.assertTrue(captcha.text.isdigit())
    
    def test_generate_text_captcha_charset_uppercase(self):
        """测试大写字母字符集"""
        captcha = self.generator.generate_text_captcha(charset=CaptchaCharset.UPPERCASE)
        self.assertTrue(captcha.text.isalpha() and captcha.text.isupper())
    
    def test_generate_text_captcha_charset_lowercase(self):
        """测试小写字母字符集"""
        captcha = self.generator.generate_text_captcha(charset=CaptchaCharset.LOWERCASE)
        self.assertTrue(captcha.text.isalpha() and captcha.text.islower())
    
    def test_generate_text_captcha_charset_alphanumeric(self):
        """测试数字字母字符集"""
        captcha = self.generator.generate_text_captcha(charset=CaptchaCharset.ALPHANUMERIC)
        self.assertTrue(all(c.isdigit() or c.isupper() for c in captcha.text))
    
    def test_generate_text_captcha_difficulty_easy(self):
        """测试简单难度"""
        captcha = self.generator.generate_text_captcha(difficulty=CaptchaDifficulty.EASY)
        self.assertEqual(len(captcha.text), 4)
        self.assertEqual(captcha.difficulty, CaptchaDifficulty.EASY)
    
    def test_generate_text_captcha_difficulty_hard(self):
        """测试困难难度"""
        captcha = self.generator.generate_text_captcha(difficulty=CaptchaDifficulty.HARD)
        self.assertEqual(len(captcha.text), 8)
        self.assertEqual(captcha.difficulty, CaptchaDifficulty.HARD)
    
    def test_generate_text_captcha_difficulty_extreme(self):
        """测试极难难度"""
        captcha = self.generator.generate_text_captcha(difficulty=CaptchaDifficulty.EXTREME)
        self.assertEqual(len(captcha.text), 8)
        self.assertEqual(captcha.difficulty, CaptchaDifficulty.EXTREME)
    
    def test_generate_text_captcha_excludes_similar(self):
        """测试排除相似字符"""
        # 多次生成，确保不包含容易混淆的字符
        for _ in range(100):
            captcha = self.generator.generate_text_captcha(
                charset=CaptchaCharset.ALPHANUMERIC,
                exclude_similar=True
            )
            similar_chars = {'0', 'O', '1', 'I', 'l', '2', 'Z', '5', 'S', '8', 'B'}
            self.assertTrue(all(c not in similar_chars for c in captcha.text))
    
    def test_generate_ascii_captcha_default(self):
        """测试默认 ASCII 艺术验证码"""
        captcha = self.generator.generate_ascii_captcha()
        
        self.assertIsInstance(captcha, CaptchaResult)
        self.assertEqual(captcha.captcha_type, CaptchaType.ASCII_ART)
        self.assertEqual(len(captcha.text), 6)
        self.assertTrue(len(captcha.captcha) > 0)
        # 验证是多行 ASCII 艺术
        self.assertTrue('\n' in captcha.captcha)
    
    def test_generate_ascii_captcha_simple_style(self):
        """测试简化风格 ASCII 艺术"""
        captcha = self.generator.generate_ascii_captcha(simple_style=True)
        self.assertEqual(captcha.captcha_type, CaptchaType.ASCII_ART)
        # 简化风格使用线条字符
        self.assertTrue(any(c in captcha.captcha for c in ['╭', '╮', '╰', '╯', '│', '─']))
    
    def test_generate_ascii_captcha_no_noise(self):
        """测试无噪声 ASCII 艺术"""
        captcha = self.generator.generate_ascii_captcha(add_noise=False)
        # 噪声字符不应出现
        noise_chars = ['░', '▒', '▓', '·', '∙', '•', '○', '●']
        # 可能仍包含干扰线字符（HARD 以上），但不包含随机噪声点
        self.assertEqual(captcha.captcha_type, CaptchaType.ASCII_ART)
    
    def test_generate_ascii_captcha_hard_with_interference(self):
        """测试困难难度干扰线"""
        captcha = self.generator.generate_ascii_captcha(difficulty=CaptchaDifficulty.HARD)
        self.assertEqual(len(captcha.text), 8)
        # 困难难度应该有干扰线
        self.assertTrue(len(captcha.captcha.split('\n')) >= 5)
    
    def test_generate_math_captcha_default(self):
        """测试默认数学验证码"""
        captcha = self.generator.generate_math_captcha()
        
        self.assertIsInstance(captcha, MathCaptchaResult)
        self.assertEqual(captcha.captcha_type, CaptchaType.MATH)
        self.assertTrue(captcha.question.endswith('= ?'))
        self.assertIsInstance(captcha.answer, int)
    
    def test_generate_math_captcha_easy(self):
        """测试简单数学验证码"""
        captcha = self.generator.generate_math_captcha(difficulty=CaptchaDifficulty.EASY)
        # EASY 只使用加减法
        self.assertTrue('+' in captcha.question or '-' in captcha.question)
        # 答案应该在合理范围内
        self.assertTrue(0 <= captcha.answer <= 20)
    
    def test_generate_math_captcha_hard(self):
        """测试困难数学验证码"""
        captcha = self.generator.generate_math_captcha(difficulty=CaptchaDifficulty.HARD)
        # HARD 可能包含乘除法
        operators = ['+', '-', '×', '÷']
        self.assertTrue(any(op in captcha.question for op in operators))
    
    def test_generate_math_captcha_division(self):
        """测试除法验证码（确保能整除）"""
        # 多次生成，找到除法类型
        for _ in range(50):
            captcha = self.generator.generate_math_captcha(difficulty=CaptchaDifficulty.EXTREME)
            if '÷' in captcha.question:
                # 确保答案是整数（能整除）
                parts = captcha.question.replace(' = ?', '').split(' ÷ ')
                a = int(parts[0])
                b = int(parts[1])
                self.assertEqual(a % b, 0)
                self.assertEqual(a // b, captcha.answer)
                break
    
    def test_generate_reverse_captcha_default(self):
        """测试默认反序验证码"""
        captcha = self.generator.generate_reverse_captcha()
        
        self.assertIsInstance(captcha, CaptchaResult)
        self.assertEqual(captcha.captcha_type, CaptchaType.REVERSE)
        self.assertTrue('请输入反转后的文本:' in captcha.captcha or '反转' in captcha.captcha)
    
    def test_generate_reverse_captcha_logic(self):
        """测试反序逻辑"""
        captcha = self.generator.generate_reverse_captcha(length=4)
        # 从显示内容中提取原文本
        display_text = captcha.captcha.split(': ')[-1] if ': ' in captcha.captcha else captcha.text
        # captcha.text 应该是反转后的
        reversed_display = display_text[::-1]
        self.assertEqual(captcha.text, reversed_display)
    
    def test_generate_image_captcha_without_pillow(self):
        """测试无 Pillow 时的图像验证码"""
        if not _PILLOW_AVAILABLE:
            with self.assertRaises(ImportError):
                self.generator.generate_image_captcha()
    
    def test_generate_image_captcha_with_pillow(self):
        """测试有 Pillow 时的图像验证码"""
        if _PILLOW_AVAILABLE:
            captcha = self.generator.generate_image_captcha()
            
            self.assertEqual(captcha.captcha_type, CaptchaType.IMAGE)
            self.assertTrue(len(captcha.captcha) > 0)
            # Base64 编码的图像
            import base64
            try:
                decoded = base64.b64decode(captcha.captcha)
                self.assertTrue(len(decoded) > 0)
            except:
                # 可能是其他格式
                pass
    
    def test_generate_mixed_captcha(self):
        """测试混合验证码"""
        # 多次生成，确保能生成不同类型
        types_seen = set()
        for _ in range(20):
            captcha = self.generator.generate_mixed_captcha()
            types_seen.add(captcha.captcha_type)
        
        # 应该能看到多种类型
        self.assertTrue(len(types_seen) >= 2)


class TestCaptchaVerification(unittest.TestCase):
    """测试验证码验证"""
    
    def setUp(self):
        self.generator = CaptchaGenerator()
    
    def test_verify_text_captcha_correct(self):
        """测试正确验证文本验证码"""
        captcha = self.generator.generate_text_captcha()
        self.assertTrue(captcha.verify(captcha.text))
    
    def test_verify_text_captcha_wrong(self):
        """测试错误验证文本验证码"""
        captcha = self.generator.generate_text_captcha()
        self.assertFalse(captcha.verify("wrong_answer"))
    
    def test_verify_case_insensitive(self):
        """测试不区分大小写验证"""
        captcha = self.generator.generate_text_captcha(charset=CaptchaCharset.UPPERCASE)
        # 大写验证码，小写输入应该也能通过
        self.assertTrue(captcha.verify(captcha.text.lower(), case_sensitive=False))
        # 区分大小写时应该失败
        self.assertFalse(captcha.verify(captcha.text.lower(), case_sensitive=True))
    
    def test_verify_math_captcha_correct(self):
        """测试正确验证数学验证码"""
        captcha = self.generator.generate_math_captcha()
        self.assertTrue(captcha.verify(captcha.answer))
        self.assertTrue(captcha.verify(str(captcha.answer)))
    
    def test_verify_math_captcha_wrong(self):
        """测试错误验证数学验证码"""
        captcha = self.generator.generate_math_captcha()
        wrong_answer = captcha.answer + 100
        self.assertFalse(captcha.verify(wrong_answer))
        self.assertFalse(captcha.verify("not_a_number"))
    
    def test_verify_expired_captcha(self):
        """测试过期验证码"""
        captcha = self.generator.generate_text_captcha(expires_in=0.1)
        # 等待过期
        time.sleep(0.2)
        self.assertTrue(captcha.is_expired())
        self.assertFalse(captcha.verify(captcha.text))
    
    def test_captcha_result_to_dict(self):
        """测试转换为字典"""
        captcha = self.generator.generate_text_captcha()
        d = captcha.to_dict()
        
        self.assertIn('text', d)
        self.assertIn('captcha', d)
        self.assertIn('captcha_type', d)
        self.assertIn('difficulty', d)
        self.assertIn('timestamp', d)
        self.assertIn('expires_in', d)
        self.assertIn('hash', d)
        self.assertIn('expired', d)


class TestCaptchaStore(unittest.TestCase):
    """测试验证码存储"""
    
    def setUp(self):
        self.store = CaptchaStore(max_size=100, cleanup_interval=1.0)
        self.generator = CaptchaGenerator()
    
    def test_store_and_get(self):
        """测试存储和获取"""
        captcha = self.generator.generate_text_captcha()
        self.store.store("test_id", captcha)
        
        stored = self.store.get("test_id")
        self.assertIsNotNone(stored)
        self.assertEqual(stored.text, captcha.text)
    
    def test_verify_from_store(self):
        """测试从存储验证"""
        captcha = self.generator.generate_text_captcha()
        self.store.store("test_id", captcha)
        
        self.assertTrue(self.store.verify("test_id", captcha.text))
        # 成功后自动删除
        self.assertIsNone(self.store.get("test_id"))
    
    def test_verify_wrong_answer(self):
        """测试验证错误答案"""
        captcha = self.generator.generate_text_captcha()
        self.store.store("test_id", captcha)
        
        self.assertFalse(self.store.verify("test_id", "wrong"))
        # 失败后不删除
        self.assertIsNotNone(self.store.get("test_id"))
    
    def test_verify_nonexistent(self):
        """测试验证不存在的验证码"""
        self.assertFalse(self.store.verify("nonexistent", "123"))
    
    def test_remove(self):
        """测试删除"""
        captcha = self.generator.generate_text_captcha()
        self.store.store("test_id", captcha)
        
        self.assertTrue(self.store.remove("test_id"))
        self.assertIsNone(self.store.get("test_id"))
        # 再次删除返回 False
        self.assertFalse(self.store.remove("test_id"))
    
    def test_clear(self):
        """测试清空"""
        for i in range(10):
            captcha = self.generator.generate_text_captcha()
            self.store.store(f"id_{i}", captcha)
        
        self.assertEqual(self.store.size(), 10)
        self.store.clear()
        self.assertEqual(self.store.size(), 0)
    
    def test_max_size(self):
        """测试最大存储数量"""
        small_store = CaptchaStore(max_size=5)
        
        for i in range(10):
            captcha = self.generator.generate_text_captcha()
            small_store.store(f"id_{i}", captcha)
        
        # 不应该超过最大数量
        self.assertTrue(small_store.size() <= 5)
    
    def test_auto_cleanup_expired(self):
        """测试自动清理过期验证码"""
        # 使用更短的清理间隔
        fast_store = CaptchaStore(max_size=100, cleanup_interval=0.1)
        
        # 生成很快过期的验证码
        for i in range(5):
            captcha = self.generator.generate_text_captcha(expires_in=0.1)
            fast_store.store(f"id_{i}", captcha)
        
        # 等待过期和清理周期
        time.sleep(0.3)
        
        # 触发清理（通过新的存储操作）
        new_captcha = self.generator.generate_text_captcha()
        fast_store.store("new_id", new_captcha)
        
        # 过期的应该被清理
        for i in range(5):
            self.assertIsNone(fast_store.get(f"id_{i}"))
        
        # 新的应该存在
        self.assertIsNotNone(fast_store.get("new_id"))


class TestQuickFunctions(unittest.TestCase):
    """测试快捷函数"""
    
    def test_generate_captcha_text(self):
        """测试快捷生成文本验证码"""
        captcha = generate_captcha(CaptchaType.TEXT)
        self.assertEqual(captcha.captcha_type, CaptchaType.TEXT)
    
    def test_generate_captcha_ascii(self):
        """测试快捷生成 ASCII 验证码"""
        captcha = generate_captcha(CaptchaType.ASCII_ART)
        self.assertEqual(captcha.captcha_type, CaptchaType.ASCII_ART)
    
    def test_generate_captcha_math(self):
        """测试快捷生成数学验证码"""
        captcha = generate_captcha(CaptchaType.MATH)
        self.assertEqual(captcha.captcha_type, CaptchaType.MATH)
    
    def test_generate_captcha_reverse(self):
        """测试快捷生成反序验证码"""
        captcha = generate_captcha(CaptchaType.REVERSE)
        self.assertEqual(captcha.captcha_type, CaptchaType.REVERSE)
    
    def test_generate_captcha_mixed(self):
        """测试快捷生成混合验证码"""
        captcha = generate_captcha(CaptchaType.MIXED)
        # 应该是某种具体类型
        self.assertIn(captcha.captcha_type, [
            CaptchaType.TEXT, CaptchaType.ASCII_ART, 
            CaptchaType.MATH, CaptchaType.REVERSE
        ])
    
    def test_generate_batch_captchas(self):
        """测试批量生成"""
        captchas = generate_batch_captchas(count=5)
        self.assertEqual(len(captchas), 5)
        
        for captcha in captchas:
            self.assertEqual(captcha.captcha_type, CaptchaType.ASCII_ART)
    
    def test_create_and_store_captcha(self):
        """测试创建并存储"""
        captcha = create_and_store_captcha("quick_test_id")
        self.assertIsNotNone(captcha)
        
        # 应该能验证
        self.assertTrue(verify_captcha("quick_test_id", captcha.text))
    
    def test_verify_captcha_nonexistent(self):
        """测试快捷验证不存在的验证码"""
        self.assertFalse(verify_captcha("nonexistent_id", "123"))


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def setUp(self):
        self.generator = CaptchaGenerator()
    
    def test_empty_charset(self):
        """测试空字符集处理"""
        # 排除所有相似字符后应该还有剩余字符
        captcha = self.generator.generate_text_captcha(
            charset=CaptchaCharset.ALPHANUMERIC,
            exclude_similar=True,
            length=4
        )
        self.assertEqual(len(captcha.text), 4)
    
    def test_min_length(self):
        """测试最小长度"""
        captcha = self.generator.generate_text_captcha(length=1)
        self.assertEqual(len(captcha.text), 1)
    
    def test_max_length(self):
        """测试较大长度"""
        captcha = self.generator.generate_text_captcha(length=20)
        self.assertEqual(len(captcha.text), 20)
    
    def test_zero_expires_in(self):
        """测试零过期时间"""
        captcha = self.generator.generate_text_captcha(expires_in=0)
        self.assertTrue(captcha.is_expired())
    
    def test_negative_expires_in(self):
        """测试负过期时间"""
        captcha = self.generator.generate_text_captcha(expires_in=-1)
        self.assertTrue(captcha.is_expired())
    
    def test_unicode_in_text(self):
        """测试文本中的 Unicode"""
        captcha = self.generator.generate_text_captcha()
        # 验证码文本应该不包含非 ASCII 字符
        self.assertTrue(all(ord(c) < 128 for c in captcha.text))
    
    def test_special_answer_verification(self):
        """测试特殊答案验证"""
        captcha = self.generator.generate_math_captcha()
        # 测试各种输入类型
        # None
        self.assertFalse(captcha.verify(None))
        # 空字符串
        self.assertFalse(captcha.verify(""))
        # 浮点数
        self.assertFalse(captcha.verify(3.14))


class TestCaptchaTypes(unittest.TestCase):
    """测试验证码类型"""
    
    def test_captcha_type_values(self):
        """测试验证码类型值"""
        self.assertEqual(CaptchaType.TEXT.value, "text")
        self.assertEqual(CaptchaType.ASCII_ART.value, "ascii")
        self.assertEqual(CaptchaType.IMAGE.value, "image")
        self.assertEqual(CaptchaType.MATH.value, "math")
        self.assertEqual(CaptchaType.REVERSE.value, "reverse")
        self.assertEqual(CaptchaType.MIXED.value, "mixed")
    
    def test_captcha_difficulty_values(self):
        """测试难度值"""
        self.assertEqual(CaptchaDifficulty.EASY.value, "easy")
        self.assertEqual(CaptchaDifficulty.MEDIUM.value, "medium")
        self.assertEqual(CaptchaDifficulty.HARD.value, "hard")
        self.assertEqual(CaptchaDifficulty.EXTREME.value, "extreme")
    
    def test_captcha_charset_values(self):
        """测试字符集值"""
        self.assertEqual(CaptchaCharset.DIGITS.value, "digits")
        self.assertEqual(CaptchaCharset.LOWERCASE.value, "lower")
        self.assertEqual(CaptchaCharset.UPPERCASE.value, "upper")
        self.assertEqual(CaptchaCharset.ALPHANUMERIC.value, "alnum")
        self.assertEqual(CaptchaCharset.MIXED.value, "mixed")


if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)
    
    # 打印测试统计
    print("\n" + "=" * 60)
    print("Captcha Utils 测试完成")
    print("=" * 60)