"""
Classical Cipher Utils Test Suite - 古典密码工具测试集

测试覆盖：
- Caesar Cipher (凯撒密码)
- ROT13
- Atbash Cipher (埃特巴什密码)
- Vigenère Cipher (维吉尼亚密码)
- Affine Cipher (仿射密码)
- Playfair Cipher (普莱费尔密码)
- Rail Fence Cipher (栅栏密码)
- Columnar Transposition Cipher (列置换密码)
- Simple Substitution Cipher (简单替换密码)
- Polybius Square Cipher (波利比乌斯方阵密码)
"""

import sys
import os
import unittest

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    CaesarCipher, ROT13, AtbashCipher, VigenereCipher,
    AffineCipher, PlayfairCipher, RailFenceCipher,
    ColumnarTranspositionCipher, SimpleSubstitutionCipher,
    PolybiusSquareCipher,
    caesar_encrypt, caesar_decrypt, rot13, atbash,
    vigenere_encrypt, vigenere_decrypt,
    affine_encrypt, affine_decrypt,
    rail_fence_encrypt, rail_fence_decrypt,
    playfair_encrypt, playfair_decrypt
)


class TestCaesarCipher(unittest.TestCase):
    """凯撒密码测试"""
    
    def test_encrypt_basic(self):
        """测试基本加密"""
        self.assertEqual(CaesarCipher.encrypt("ABC", 3), "DEF")
        self.assertEqual(CaesarCipher.encrypt("XYZ", 3), "ABC")
        self.assertEqual(CaesarCipher.encrypt("abc", 3), "def")
    
    def test_encrypt_with_spaces(self):
        """测试包含空格的加密"""
        self.assertEqual(CaesarCipher.encrypt("HELLO WORLD", 3), "KHOOR ZRUOG")
    
    def test_encrypt_with_punctuation(self):
        """测试包含标点的加密"""
        self.assertEqual(CaesarCipher.encrypt("Hello, World!", 3), "Khoor, Zruog!")
    
    def test_decrypt(self):
        """测试解密"""
        self.assertEqual(CaesarCipher.decrypt("DEF", 3), "ABC")
        self.assertEqual(CaesarCipher.decrypt("KHOOR ZRUOG", 3), "HELLO WORLD")
    
    def test_encrypt_decrypt_roundtrip(self):
        """测试加密解密往返"""
        text = "The Quick Brown Fox Jumps Over The Lazy Dog"
        encrypted = CaesarCipher.encrypt(text, 5)
        decrypted = CaesarCipher.decrypt(encrypted, 5)
        self.assertEqual(decrypted, text)
    
    def test_shift_0(self):
        """测试0位移"""
        self.assertEqual(CaesarCipher.encrypt("HELLO", 0), "HELLO")
    
    def test_shift_negative(self):
        """测试负位移"""
        self.assertEqual(CaesarCipher.encrypt("DEF", -3), "ABC")
    
    def test_shift_large(self):
        """测试大位移（超过26）"""
        self.assertEqual(CaesarCipher.encrypt("ABC", 29), "DEF")
        self.assertEqual(CaesarCipher.encrypt("ABC", 55), "DEF")
    
    def test_brute_force(self):
        """测试暴力破解"""
        encrypted = "KHOOR"
        results = CaesarCipher.brute_force(encrypted)
        # 位移量为3时应解密为HELLO
        self.assertEqual(results[3][1], "HELLO")
        self.assertEqual(len(results), 26)
    
    def test_convenience_functions(self):
        """测试便捷函数"""
        self.assertEqual(caesar_encrypt("ABC", 3), "DEF")
        self.assertEqual(caesar_decrypt("DEF", 3), "ABC")


class TestROT13(unittest.TestCase):
    """ROT13测试"""
    
    def test_transform(self):
        """测试基本变换"""
        self.assertEqual(ROT13.transform("HELLO"), "URYYB")
        self.assertEqual(ROT13.transform("URYYB"), "HELLO")
    
    def test_roundtrip(self):
        """测试往返变换"""
        text = "Python Programming"
        transformed = ROT13.transform(text)
        back = ROT13.transform(transformed)
        self.assertEqual(back, text)
    
    def test_with_numbers(self):
        """测试包含数字"""
        self.assertEqual(ROT13.transform("ABC123"), "NOP123")
    
    def test_convenience_function(self):
        """测试便捷函数"""
        self.assertEqual(rot13("HELLO"), "URYYB")


class TestAtbashCipher(unittest.TestCase):
    """埃特巴什密码测试"""
    
    def test_encrypt_uppercase(self):
        """测试大写字母加密"""
        self.assertEqual(AtbashCipher.encrypt("ABC"), "ZYX")
        self.assertEqual(AtbashCipher.encrypt("ZYX"), "ABC")
    
    def test_encrypt_lowercase(self):
        """测试小写字母加密"""
        self.assertEqual(AtbashCipher.encrypt("abc"), "zyx")
    
    def test_roundtrip(self):
        """测试往返变换"""
        text = "HELLO WORLD"
        encrypted = AtbashCipher.encrypt(text)
        decrypted = AtbashCipher.decrypt(encrypted)
        self.assertEqual(decrypted, text)
    
    def test_mixed_case(self):
        """测试混合大小写"""
        self.assertEqual(AtbashCipher.encrypt("Hello"), "Svool")
    
    def test_convenience_function(self):
        """测试便捷函数"""
        self.assertEqual(atbash("ABC"), "ZYX")


class TestVigenereCipher(unittest.TestCase):
    """维吉尼亚密码测试"""
    
    def test_encrypt_basic(self):
        """测试基本加密"""
        self.assertEqual(VigenereCipher.encrypt("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR")
    
    def test_decrypt(self):
        """测试解密"""
        self.assertEqual(VigenereCipher.decrypt("LXFOPVEFRNHR", "LEMON"), "ATTACKATDAWN")
    
    def test_roundtrip(self):
        """测试往返变换"""
        text = "HELLO WORLD"
        key = "SECRET"
        encrypted = VigenereCipher.encrypt(text, key)
        decrypted = VigenereCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, text)
    
    def test_case_insensitive_key(self):
        """测试密钥大小写不敏感"""
        self.assertEqual(
            VigenereCipher.encrypt("HELLO", "abc"),
            VigenereCipher.encrypt("HELLO", "ABC")
        )
    
    def test_preserve_non_alpha(self):
        """测试保留非字母字符"""
        text = "HELLO, WORLD! 123"
        key = "KEY"
        encrypted = VigenereCipher.encrypt(text, key)
        decrypted = VigenereCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, text)
    
    def test_empty_key(self):
        """测试空密钥"""
        with self.assertRaises(ValueError):
            VigenereCipher.encrypt("HELLO", "")
    
    def test_convenience_functions(self):
        """测试便捷函数"""
        text = "ATTACK"
        key = "LEMON"
        encrypted = vigenere_encrypt(text, key)
        decrypted = vigenere_decrypt(encrypted, key)
        self.assertEqual(decrypted, text)


class TestAffineCipher(unittest.TestCase):
    """仿射密码测试"""
    
    def test_encrypt_basic(self):
        """测试基本加密"""
        # E(x) = (5x + 8) mod 26
        # A=0 -> (0+8)=8 -> I
        # F=5 -> (25+8)=33 mod 26 = 7 -> H
        self.assertEqual(AffineCipher.encrypt("AFFINE", 5, 8), "IHHWVC")
    
    def test_decrypt(self):
        """测试解密"""
        self.assertEqual(AffineCipher.decrypt("IHHWVC", 5, 8), "AFFINE")
    
    def test_roundtrip(self):
        """测试往返变换"""
        text = "HELLO WORLD"
        for a in AffineCipher.VALID_A_VALUES:
            for b in range(26):
                encrypted = AffineCipher.encrypt(text, a, b)
                decrypted = AffineCipher.decrypt(encrypted, a, b)
                self.assertEqual(decrypted, text)
    
    def test_invalid_a(self):
        """测试无效a值（不与26互质）"""
        with self.assertRaises(ValueError):
            AffineCipher.encrypt("HELLO", 2, 3)
        with self.assertRaises(ValueError):
            AffineCipher.encrypt("HELLO", 13, 3)
    
    def test_valid_a_values(self):
        """测试所有有效a值"""
        text = "TEST"
        for a in AffineCipher.VALID_A_VALUES:
            encrypted = AffineCipher.encrypt(text, a, 0)
            decrypted = AffineCipher.decrypt(encrypted, a, 0)
            self.assertEqual(decrypted, text)
    
    def test_convenience_functions(self):
        """测试便捷函数"""
        text = "TEST"
        encrypted = affine_encrypt(text, 5, 8)
        decrypted = affine_decrypt(encrypted, 5, 8)
        self.assertEqual(decrypted, text)


class TestPlayfairCipher(unittest.TestCase):
    """普莱费尔密码测试"""
    
    def test_encrypt_basic(self):
        """测试基本加密"""
        encrypted = PlayfairCipher.encrypt("HELLO", "PLAYFAIR")
        # HELLO -> HE LX LO -> 密文
        self.assertEqual(len(encrypted), 6)  # 3个字母对
    
    def test_decrypt(self):
        """测试解密"""
        text = "HELLO WORLD"
        key = "SECRET"
        encrypted = PlayfairCipher.encrypt(text, key)
        decrypted = PlayfairCipher.decrypt(encrypted, key)
        # 解密结果可能包含填充的X
        self.assertTrue(decrypted.startswith("HELXLO"))
    
    def test_key_with_duplicates(self):
        """测试包含重复字符的密钥"""
        encrypted = PlayfairCipher.encrypt("TEST", "SECRETKEY")
        self.assertEqual(len(encrypted), 4)
    
    def test_roundtrip(self):
        """测试往返变换"""
        text = "ATTACKATDAWN"
        key = "FORTIFICATION"
        encrypted = PlayfairCipher.encrypt(text, key)
        decrypted = PlayfairCipher.decrypt(encrypted, key)
        self.assertTrue(decrypted.startswith("AT"))
    
    def test_ij_merge(self):
        """测试I/J合并处理"""
        # J应该被当作I处理
        encrypted = PlayfairCipher.encrypt("JUMP", "KEY")
        decrypted = PlayfairCipher.decrypt(encrypted, "KEY")
        self.assertTrue("I" in decrypted or "J" in decrypted)
    
    def test_convenience_functions(self):
        """测试便捷函数"""
        text = "HELLO"
        key = "WORLD"
        encrypted = playfair_encrypt(text, key)
        decrypted = playfair_decrypt(encrypted, key)
        self.assertTrue(decrypted.startswith("HEL"))


class TestRailFenceCipher(unittest.TestCase):
    """栅栏密码测试"""
    
    def test_encrypt_2_rails(self):
        """测试2栏加密"""
        # 2栏栅栏密码：
        # 第一栏：W A E I C V R D L E T N E
        # 第二栏：. E A R D S O E E F E A O C .
        # 结果：WAEICVRDLETN EERDSOEEFEAOC
        text = "WEAREDISCOVEREDFLEEATONCE"
        encrypted = RailFenceCipher.encrypt(text, 2)
        # 验证长度正确
        self.assertEqual(len(encrypted), len(text))
        # 验证往返正确
        decrypted = RailFenceCipher.decrypt(encrypted, 2)
        self.assertEqual(decrypted, text)
    
    def test_encrypt_3_rails(self):
        """测试3栏加密"""
        text = "HELLO WORLD"
        encrypted = RailFenceCipher.encrypt(text, 3)
        # 栅栏密码保留所有字符（包括空格）
        self.assertEqual(len(encrypted), len(text))
    
    def test_decrypt(self):
        """测试解密"""
        text = "WEAREDISCOVEREDFLEEATONCE"
        encrypted = RailFenceCipher.encrypt(text, 3)
        decrypted = RailFenceCipher.decrypt(encrypted, 3)
        self.assertEqual(decrypted, text)
    
    def test_roundtrip(self):
        """测试往返变换"""
        text = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
        for rails in range(2, 6):
            encrypted = RailFenceCipher.encrypt(text, rails)
            decrypted = RailFenceCipher.decrypt(encrypted, rails)
            self.assertEqual(decrypted, text)
    
    def test_invalid_rails(self):
        """测试无效栏数"""
        with self.assertRaises(ValueError):
            RailFenceCipher.encrypt("HELLO", 1)
        with self.assertRaises(ValueError):
            RailFenceCipher.decrypt("HELLO", 0)
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(RailFenceCipher.encrypt("", 2), "")
        self.assertEqual(RailFenceCipher.decrypt("", 2), "")
    
    def test_single_char(self):
        """测试单字符"""
        self.assertEqual(RailFenceCipher.encrypt("A", 2), "A")
        self.assertEqual(RailFenceCipher.decrypt("A", 2), "A")
    
    def test_convenience_functions(self):
        """测试便捷函数"""
        text = "HELLO"
        encrypted = rail_fence_encrypt(text, 3)
        decrypted = rail_fence_decrypt(encrypted, 3)
        self.assertEqual(decrypted, text)


class TestColumnarTranspositionCipher(unittest.TestCase):
    """列置换密码测试"""
    
    def test_encrypt_basic(self):
        """测试基本加密"""
        text = "WEAREDISCOVEREDFLEEATONCE"
        key = "ZEBRAS"
        encrypted = ColumnarTranspositionCipher.encrypt(text, key)
        # 密钥长度为6，文本长度26，需要填充
        self.assertEqual(len(encrypted), len(text) + (6 - len(text) % 6) % 6)
    
    def test_decrypt(self):
        """测试解密"""
        text = "WEAREDISCOVEREDFLEEATONCE"
        key = "ZEBRAS"
        encrypted = ColumnarTranspositionCipher.encrypt(text, key)
        decrypted = ColumnarTranspositionCipher.decrypt(encrypted, key)
        # 解密结果可能包含填充的X
        self.assertTrue(decrypted.startswith(text))
    
    def test_roundtrip(self):
        """测试往返变换"""
        text = "HELLOWORLDTHISISATEST"
        key = "SECRET"
        encrypted = ColumnarTranspositionCipher.encrypt(text, key)
        decrypted = ColumnarTranspositionCipher.decrypt(encrypted, key)
        # 列置换密码会对文本进行填充，所以解密结果可能包含X
        self.assertTrue(decrypted.startswith(text))
    
    def test_empty_key(self):
        """测试空密钥"""
        with self.assertRaises(ValueError):
            ColumnarTranspositionCipher.encrypt("HELLO", "")
    
    def test_key_with_duplicates(self):
        """测试包含重复字符的密钥"""
        text = "TESTMESSAGE"
        key = "BANANA"
        encrypted = ColumnarTranspositionCipher.encrypt(text, key)
        decrypted = ColumnarTranspositionCipher.decrypt(encrypted, key)
        self.assertTrue(decrypted.startswith("TESTMESSAGE"))


class TestSimpleSubstitutionCipher(unittest.TestCase):
    """简单替换密码测试"""
    
    def test_encrypt_basic(self):
        """测试基本加密"""
        text = "HELLO"
        key = "QWERTYUIOPASDFGHJKLZXCVBNM"
        encrypted = SimpleSubstitutionCipher.encrypt(text, key)
        self.assertEqual(len(encrypted), len(text))
        self.assertNotEqual(encrypted, text)
    
    def test_decrypt(self):
        """测试解密"""
        text = "HELLO WORLD"
        key = "QWERTYUIOPASDFGHJKLZXCVBNM"
        encrypted = SimpleSubstitutionCipher.encrypt(text, key)
        decrypted = SimpleSubstitutionCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, text)
    
    def test_roundtrip(self):
        """测试往返变换"""
        text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        key = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
        encrypted = SimpleSubstitutionCipher.encrypt(text, key)
        decrypted = SimpleSubstitutionCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, text)
    
    def test_partial_key(self):
        """测试部分密钥（自动补充）"""
        text = "HELLO"
        key = "ZYX"  # 只提供部分密钥
        encrypted = SimpleSubstitutionCipher.encrypt(text, key)
        # 应该能正常工作
        self.assertEqual(len(encrypted), len(text))


class TestPolybiusSquareCipher(unittest.TestCase):
    """波利比乌斯方阵密码测试"""
    
    def test_encrypt_basic(self):
        """测试基本加密"""
        # H=2,3  E=1,5  L=3,1  L=3,1  O=3,4
        encrypted = PolybiusSquareCipher.encrypt("HELLO")
        self.assertEqual(encrypted, "2315313134")
    
    def test_encrypt_with_j(self):
        """测试J被当作I处理"""
        # J应该映射到I的位置(2,4)
        encrypted = PolybiusSquareCipher.encrypt("JUMP")
        self.assertTrue(encrypted.startswith("24"))  # J -> I的位置
    
    def test_decrypt(self):
        """测试解密"""
        encrypted = "2315313134"
        decrypted = PolybiusSquareCipher.decrypt(encrypted)
        self.assertEqual(decrypted, "HELLO")
    
    def test_roundtrip(self):
        """测试往返变换"""
        text = "THEQUICKBROWNFXJMP SVLAZYDG"  # 包含所有字母的测试
        encrypted = PolybiusSquareCipher.encrypt(text)
        decrypted = PolybiusSquareCipher.decrypt(encrypted)
        # J会被转为I
        self.assertEqual(decrypted, text.replace('J', 'I').replace(' ', ''))
    
    def test_ignore_non_alpha(self):
        """测试忽略非字母字符"""
        encrypted = PolybiusSquareCipher.encrypt("A1B2C3")
        # 只加密字母
        self.assertEqual(encrypted, "111213")
    
    def test_odd_digits(self):
        """测试奇数个数字的密文"""
        with self.assertRaises(ValueError):
            PolybiusSquareCipher.decrypt("123")
    
    def test_custom_square(self):
        """测试自定义方阵"""
        # 自定义方阵必须包含所有字母A-Z（I/J合并时为25个字母）
        custom = [
            ['K', 'E', 'Y', 'W', 'O'],
            ['R', 'D', 'A', 'B', 'C'],
            ['F', 'G', 'H', 'I', 'L'],
            ['M', 'N', 'P', 'Q', 'S'],
            ['T', 'U', 'V', 'X', 'Z']
        ]
        # 测试几个字母的加密解密
        encrypted = PolybiusSquareCipher.encrypt("KEY", custom)
        decrypted = PolybiusSquareCipher.decrypt(encrypted, custom)
        self.assertEqual(decrypted, "KEY")


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_multiple_ciphers_chain(self):
        """测试多重加密"""
        text = "HELLO WORLD"
        
        # 凯撒加密
        caesar = CaesarCipher.encrypt(text, 5)
        # 栅栏加密
        rail = RailFenceCipher.encrypt(caesar, 3)
        # 栅栏解密
        rail_dec = RailFenceCipher.decrypt(rail, 3)
        # 凯撒解密
        final = CaesarCipher.decrypt(rail_dec, 5)
        
        self.assertEqual(final, text)
    
    def test_all_ciphers_available(self):
        """测试所有密码类都可用"""
        text = "TEST"
        
        # 简单测试所有密码
        self.assertIsNotNone(CaesarCipher.encrypt(text, 3))
        self.assertIsNotNone(ROT13.transform(text))
        self.assertIsNotNone(AtbashCipher.encrypt(text))
        self.assertIsNotNone(VigenereCipher.encrypt(text, "KEY"))
        self.assertIsNotNone(AffineCipher.encrypt(text, 5, 8))
        self.assertIsNotNone(PlayfairCipher.encrypt(text, "KEY"))
        self.assertIsNotNone(RailFenceCipher.encrypt(text, 2))
        self.assertIsNotNone(ColumnarTranspositionCipher.encrypt(text, "KEY"))
        self.assertIsNotNone(SimpleSubstitutionCipher.encrypt(text, "ZYX"))
        self.assertIsNotNone(PolybiusSquareCipher.encrypt(text))


if __name__ == "__main__":
    unittest.main(verbosity=2)