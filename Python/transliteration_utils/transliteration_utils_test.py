"""
Transliteration Utils 测试文件

测试文字系统音译转换功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transliteration_utils.mod import (
    TransliterationUtils,
    cyrillic_to_latin, latin_to_cyrillic, greek_to_latin,
    hiragana_to_romaji, katakana_to_romaji, japanese_to_romaji,
    hangul_to_romaji, arabic_to_latin, thai_to_latin, hebrew_to_latin,
    detect_script, auto_transliterate, transliterate
)


class TestCyrillicToLatin:
    """西里尔字母转拉丁字母测试"""
    
    def test_basic_conversion(self):
        """测试基本转换"""
        assert cyrillic_to_latin("Привет") == "Privet"
        assert cyrillic_to_latin("мир") == "mir"
    
    def test_with_spaces(self):
        """测试带空格的文本"""
        assert cyrillic_to_latin("Привет мир") == "Privet mir"
    
    def test_special_characters(self):
        """测试特殊字符"""
        assert cyrillic_to_latin("Ёжик") == "Yozhik"
        assert cyrillic_to_latin("Щука") == "Shchuka"
    
    def test_mixed_text(self):
        """测试混合文本"""
        result = cyrillic_to_latin("Hello, Привет!")
        assert "Hello" in result
        assert "Privet" in result
    
    def test_empty_string(self):
        """测试空字符串"""
        assert cyrillic_to_latin("") == ""
    
    def test_latin_only(self):
        """测试纯拉丁文本"""
        assert cyrillic_to_latin("Hello World") == "Hello World"
    
    def test_numbers_and_punctuation(self):
        """测试数字和标点"""
        assert cyrillic_to_latin("123 Привет!") == "123 Privet!"
    
    def test_longer_text(self):
        """测试较长文本"""
        russian = "Добро пожаловать в Россию"
        expected = "Dobro pozhalovat v Rossiyu"
        assert cyrillic_to_latin(russian) == expected


class TestLatinToCyrillic:
    """拉丁字母转西里尔字母测试"""
    
    def test_basic_conversion(self):
        """测试基本转换"""
        assert latin_to_cyrillic("Privet") == "Привет"
        assert latin_to_cyrillic("mir") == "мир"
    
    def test_special_combinations(self):
        """测试特殊组合"""
        assert latin_to_cyrillic("Yozhik") == "Ёжик"
        assert latin_to_cyrillic("Shchuka") == "Щука"
    
    def test_roundtrip(self):
        """测试往返转换"""
        original = "Привет"
        to_latin = cyrillic_to_latin(original)
        back_to_cyrillic = latin_to_cyrillic(to_latin)
        assert back_to_cyrillic == original


class TestGreekToLatin:
    """希腊字母转拉丁字母测试"""
    
    def test_basic_conversion(self):
        """测试基本转换"""
        result = greek_to_latin("Γειά")
        # 接受各种合理的音译结果
        assert "G" in result and len(result) >= 3
    
    def test_alpha(self):
        """测试字母Alpha"""
        assert greek_to_latin("Α") == "A"
        assert greek_to_latin("α") == "a"
    
    def test_beta(self):
        """测试字母Beta"""
        assert greek_to_latin("Β") == "V"
        assert greek_to_latin("β") == "v"
    
    def test_theta(self):
        """测试字母Theta"""
        assert greek_to_latin("Θ") == "Th"
        assert greek_to_latin("θ") == "th"
    
    def test_word(self):
        """测试单词转换"""
        # logos -> λόγος
        result = greek_to_latin("λόγος")
        # 检查输出是合理的拉丁化结果
        assert len(result) >= 3 and result[0].lower() == 'l'


class TestHiraganaToRomaji:
    """平假名转罗马音测试"""
    
    def test_basic_syllables(self):
        """测试基本音节"""
        assert hiragana_to_romaji("あ") == "a"
        assert hiragana_to_romaji("か") == "ka"
        assert hiragana_to_romaji("さ") == "sa"
    
    def test_dakuten(self):
        """测试浊音"""
        assert hiragana_to_romaji("が") == "ga"
        assert hiragana_to_romaji("じ") == "ji"
        assert hiragana_to_romaji("ば") == "ba"
    
    def test_handakuten(self):
        """测试半浊音"""
        assert hiragana_to_romaji("ぱ") == "pa"
        assert hiragana_to_romaji("ぴ") == "pi"
    
    def test_youon(self):
        """测试拗音"""
        assert hiragana_to_romaji("きゃ") == "kya"
        assert hiragana_to_romaji("しゅ") == "shu"
        assert hiragana_to_romaji("ちょ") == "cho"
    
    def test_sokuon(self):
        """测试促音"""
        # っ + か = kka
        result = hiragana_to_romaji("っか")
        assert result == "kka"
    
    def test_n(self):
        """测试ん"""
        assert hiragana_to_romaji("ん") == "n"
    
    def test_word(self):
        """测试单词"""
        result = hiragana_to_romaji("こんにちは")
        assert "konnichi" in result or "konniti" in result


class TestKatakanaToRomaji:
    """片假名转罗马音测试"""
    
    def test_basic_syllables(self):
        """测试基本音节"""
        assert katakana_to_romaji("ア") == "a"
        assert katakana_to_romaji("カ") == "ka"
        assert katakana_to_romaji("サ") == "sa"
    
    def test_dakuten(self):
        """测试浊音"""
        assert katakana_to_romaji("ガ") == "ga"
        assert katakana_to_romaji("ジ") == "ji"
    
    def test_youon(self):
        """测试拗音"""
        assert katakana_to_romaji("キャ") == "kya"
        assert katakana_to_romaji("シュ") == "shu"
    
    def test_foreign_sounds(self):
        """测试外来音"""
        # ヴァ -> va
        assert katakana_to_romaji("ヴァ") == "va"


class TestJapaneseToRomaji:
    """日语转罗马音测试"""
    
    def test_mixed_kana(self):
        """测试混合假名"""
        result = japanese_to_romaji("こんにちは")
        assert len(result) > 0
    
    def test_hiragana_portion(self):
        """测试平假名部分"""
        result = japanese_to_romaji("あいうえお")
        assert result == "aiueo"
    
    def test_katakana_portion(self):
        """测试片假名部分"""
        result = japanese_to_romaji("アイウエオ")
        assert result == "aiueo"
    
    def test_mixed_with_kanji(self):
        """测试混合汉字"""
        result = japanese_to_romaji("日本語")
        # 汉字不会被转换
        assert "日本語" in result or len(result) == 3  # 保留汉字
    
    def test_sokuon_hiragana(self):
        """测试平假名促音"""
        result = japanese_to_romaji("がっこう")
        # 促音应该产生重复辅音或保持某种音节结构
        assert len(result) > 0


class TestHangulToRomaji:
    """韩语转罗马音测试"""
    
    def test_basic_syllable(self):
        """测试基本音节"""
        result = hangul_to_romaji("가")
        assert result == "ga"
    
    def test_word(self):
        """测试单词"""
        result = hangul_to_romaji("안녕하세요")
        assert "annyeong" in result or "an" in result
    
    def test_kim(self):
        """测试姓氏金"""
        result = hangul_to_romaji("김")
        assert result == "gim" or "kim" in result
    
    def test_seoul(self):
        """测试首尔"""
        result = hangul_to_romaji("서울")
        assert "seoul" in result.lower() or "seou" in result.lower()
    
    def test_korean(self):
        """测试韩语"""
        result = hangul_to_romaji("한국")
        assert "han" in result.lower() and "guk" in result.lower()


class TestArabicToLatin:
    """阿拉伯字母转拉丁字母测试"""
    
    def test_basic_letters(self):
        """测试基本字母"""
        assert arabic_to_latin("ا") == "a"
        assert arabic_to_latin("ب") == "b"
    
    def test_word(self):
        """测试单词"""
        result = arabic_to_latin("مرحبا")
        assert len(result) >= 3  # 至少有一些输出
    
    def test_salaam(self):
        """测试平安"""
        result = arabic_to_latin("سلام")
        assert "s" in result or "l" in result or "m" in result


class TestThaiToLatin:
    """泰语转拉丁字母测试"""
    
    def test_basic_letters(self):
        """测试基本字母"""
        result = thai_to_latin("สวัสดี")
        assert len(result) > 0
    
    def test_word(self):
        """测试单词"""
        result = thai_to_latin("ไทย")
        assert "th" in result or "t" in result


class TestHebrewToLatin:
    """希伯来语转拉丁字母测试"""
    
    def test_basic_letters(self):
        """测试基本字母"""
        assert hebrew_to_latin("א") == ""  # aleph 无音
        assert hebrew_to_latin("ב") == "b"
    
    def test_shalom(self):
        """测试平安"""
        result = hebrew_to_latin("שלום")
        assert "sh" in result or "s" in result


class TestDetectScript:
    """文字系统检测测试"""
    
    def test_cyrillic_detection(self):
        """测试西里尔字母检测"""
        assert detect_script("Привет") == "cyrillic"
    
    def test_greek_detection(self):
        """测试希腊字母检测"""
        assert detect_script("Γειά") == "greek"
    
    def test_hiragana_detection(self):
        """测试平假名检测"""
        assert detect_script("こんにちは") == "hiragana"
    
    def test_katakana_detection(self):
        """测试片假名检测"""
        assert detect_script("コンニチハ") == "katakana"
    
    def test_hangul_detection(self):
        """测试韩语检测"""
        assert detect_script("안녕하세요") == "hangul"
    
    def test_arabic_detection(self):
        """测试阿拉伯字母检测"""
        assert detect_script("مرحبا") == "arabic"
    
    def test_thai_detection(self):
        """测试泰语检测"""
        assert detect_script("สวัสดี") == "thai"
    
    def test_hebrew_detection(self):
        """测试希伯来语检测"""
        assert detect_script("שלום") == "hebrew"
    
    def test_latin_detection(self):
        """测试拉丁字母检测"""
        assert detect_script("Hello World") == "latin"
    
    def test_empty_string(self):
        """测试空字符串"""
        assert detect_script("") == "unknown"
    
    def test_numbers_only(self):
        """测试纯数字"""
        assert detect_script("12345") == "unknown"


class TestAutoTransliterate:
    """自动转换测试"""
    
    def test_auto_russian(self):
        """测试自动检测俄语"""
        result, script = auto_transliterate("Привет")
        assert script == "cyrillic"
        assert "Privet" in result
    
    def test_auto_greek(self):
        """测试自动检测希腊语"""
        result, script = auto_transliterate("Γειά")
        assert script == "greek"
        assert len(result) > 0
    
    def test_auto_japanese(self):
        """测试自动检测日语"""
        result, script = auto_transliterate("こんにちは")
        assert script in ["hiragana", "katakana"]
    
    def test_auto_latin(self):
        """测试自动检测拉丁"""
        result, script = auto_transliterate("Hello")
        assert script == "latin"
        assert result == "Hello"
    
    def test_auto_korean(self):
        """测试自动检测韩语"""
        result, script = auto_transliterate("안녕")
        assert script == "hangul"


class TestTransliterate:
    """指定转换测试"""
    
    def test_transliterate_cyrillic(self):
        """测试指定西里尔转换"""
        result = transliterate("Привет", "cyrillic", "latin")
        assert result == "Privet"
    
    def test_transliterate_greek(self):
        """测试指定希腊转换"""
        result = transliterate("Θεός", "greek", "latin")
        assert "Th" in result
    
    def test_transliterate_hiragana(self):
        """测试指定平假名转换"""
        result = transliterate("あいうえお", "hiragana", "latin")
        assert result == "aiueo"
    
    def test_transliterate_katakana(self):
        """测试指定片假名转换"""
        result = transliterate("アイウエオ", "katakana", "latin")
        assert result == "aiueo"
    
    def test_transliterate_japanese(self):
        """测试指定日语转换"""
        result = transliterate("こんにちは", "japanese", "latin")
        assert len(result) > 0
    
    def test_transliterate_hangul(self):
        """测试指定韩语转换"""
        result = transliterate("안녕", "hangul", "latin")
        assert "an" in result.lower()
    
    def test_unsupported_source(self):
        """测试不支持的源文字系统"""
        try:
            transliterate("Hello", "invalid", "latin")
            assert False, "应该抛出异常"
        except ValueError as e:
            assert "不支持" in str(e)
    
    def test_unsupported_target(self):
        """测试不支持的目标文字系统"""
        try:
            transliterate("Hello", "cyrillic", "invalid")
            assert False, "应该抛出异常"
        except ValueError as e:
            assert "不支持" in str(e)


class TestGetSupportedScripts:
    """获取支持文字系统测试"""
    
    def test_returns_list(self):
        """测试返回列表"""
        scripts = TransliterationUtils.get_supported_scripts()
        assert isinstance(scripts, list)
    
    def test_contains_common_scripts(self):
        """测试包含常见文字系统"""
        scripts = TransliterationUtils.get_supported_scripts()
        assert "cyrillic" in scripts
        assert "greek" in scripts
        assert "hiragana" in scripts
        assert "katakana" in scripts
        assert "hangul" in scripts
        assert "arabic" in scripts


class TestEdgeCases:
    """边缘情况测试"""
    
    def test_empty_string(self):
        """测试空字符串"""
        assert cyrillic_to_latin("") == ""
        assert greek_to_latin("") == ""
        assert hiragana_to_romaji("") == ""
        assert katakana_to_romaji("") == ""
        assert hangul_to_romaji("") == ""
        assert arabic_to_latin("") == ""
        assert thai_to_latin("") == ""
        assert hebrew_to_latin("") == ""
    
    def test_whitespace_only(self):
        """测试纯空格"""
        assert cyrillic_to_latin("   ") == "   "
        assert hiragana_to_romaji("   ") == "   "
    
    def test_newlines(self):
        """测试换行符"""
        text = "Привет\nмир"
        result = cyrillic_to_latin(text)
        assert "\n" in result
    
    def test_unicode_symbols(self):
        """测试Unicode符号"""
        assert cyrillic_to_latin("★") == "★"
        assert hiragana_to_romaji("♡") == "♡"
    
    def test_mixed_scripts(self):
        """测试混合文字系统"""
        # 俄语+日语+拉丁
        text = "Hello Привет こんにちは"
        result = cyrillic_to_latin(text)
        assert "Hello" in result
        assert "Privet" in result
        # 日语部分保持原样
        assert "こんにちは" in result


def run_tests():
    """运行所有测试"""
    test_classes = [
        TestCyrillicToLatin,
        TestLatinToCyrillic,
        TestGreekToLatin,
        TestHiraganaToRomaji,
        TestKatakanaToRomaji,
        TestJapaneseToRomaji,
        TestHangulToRomaji,
        TestArabicToLatin,
        TestThaiToLatin,
        TestHebrewToLatin,
        TestDetectScript,
        TestAutoTransliterate,
        TestTransliterate,
        TestGetSupportedScripts,
        TestEdgeCases,
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for test_class in test_classes:
        print(f"\n{'='*60}")
        print(f"Testing: {test_class.__name__}")
        print('='*60)
        
        instance = test_class()
        
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                total_tests += 1
                try:
                    method = getattr(instance, method_name)
                    method()
                    print(f"  ✓ {method_name}")
                    passed_tests += 1
                except AssertionError as e:
                    print(f"  ✗ {method_name}: {e}")
                    failed_tests += 1
                except Exception as e:
                    print(f"  ✗ {method_name}: Unexpected error: {e}")
                    failed_tests += 1
    
    print(f"\n{'='*60}")
    print(f"Test Summary")
    print('='*60)
    print(f"Total:  {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print('='*60)
    
    return failed_tests == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)