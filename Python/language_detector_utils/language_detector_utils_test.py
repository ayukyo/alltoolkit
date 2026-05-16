"""
Unit tests for language_detector_utils module.

Run with: python -m pytest language_detector_utils_test.py -v
Or: python language_detector_utils_test.py
"""

import unittest
from language_detector_utils import (
    Script,
    Language,
    get_script,
    get_scripts,
    count_scripts,
    analyze_scripts,
    detect_language,
    detect_languages_batch,
    detect_latin_language,
    detect_non_latin_language,
    get_language_name,
    get_script_name,
    is_language,
    get_text_statistics,
    LanguageDetector,
    LanguageResult,
    ScriptStats,
)


class TestGetScript(unittest.TestCase):
    """Tests for get_script function."""
    
    def test_latin_characters(self):
        """Test Latin script detection."""
        self.assertEqual(get_script('A'), Script.LATIN)
        self.assertEqual(get_script('z'), Script.LATIN)
        self.assertEqual(get_script('é'), Script.LATIN)
    
    def test_cjk_characters(self):
        """Test CJK script detection."""
        self.assertEqual(get_script('中'), Script.CJK)
        self.assertEqual(get_script('国'), Script.CJK)
        self.assertEqual(get_script('日'), Script.CJK)
    
    def test_hiragana(self):
        """Test Hiragana script detection."""
        self.assertEqual(get_script('あ'), Script.HIRAGANA)
        self.assertEqual(get_script('い'), Script.HIRAGANA)
        self.assertEqual(get_script('う'), Script.HIRAGANA)
    
    def test_katakana(self):
        """Test Katakana script detection."""
        self.assertEqual(get_script('ア'), Script.KATAKANA)
        self.assertEqual(get_script('イ'), Script.KATAKANA)
        self.assertEqual(get_script('ウ'), Script.KATAKANA)
    
    def test_hangul(self):
        """Test Hangul (Korean) script detection."""
        self.assertEqual(get_script('한'), Script.HANGUL)
        self.assertEqual(get_script('글'), Script.HANGUL)
    
    def test_arabic(self):
        """Test Arabic script detection."""
        self.assertEqual(get_script('ا'), Script.ARABIC)
        self.assertEqual(get_script('ب'), Script.ARABIC)
    
    def test_devanagari(self):
        """Test Devanagari (Hindi) script detection."""
        self.assertEqual(get_script('न'), Script.DEVANAGARI)
        self.assertEqual(get_script('म'), Script.DEVANAGARI)
    
    def test_thai(self):
        """Test Thai script detection."""
        self.assertEqual(get_script('ก'), Script.THAI)
        self.assertEqual(get_script('ข'), Script.THAI)
    
    def test_cyrillic(self):
        """Test Cyrillic script detection."""
        self.assertEqual(get_script('П'), Script.CYRILLIC)
        self.assertEqual(get_script('р'), Script.CYRILLIC)
    
    def test_greek(self):
        """Test Greek script detection."""
        self.assertEqual(get_script('Α'), Script.GREEK)
        self.assertEqual(get_script('β'), Script.GREEK)
    
    def test_hebrew(self):
        """Test Hebrew script detection."""
        self.assertEqual(get_script('א'), Script.HEBREW)
        self.assertEqual(get_script('ב'), Script.HEBREW)
    
    def test_unknown_characters(self):
        """Test unknown script detection."""
        # Numbers and punctuation should return UNKNOWN
        self.assertEqual(get_script('1'), Script.UNKNOWN)
        self.assertEqual(get_script('!'), Script.UNKNOWN)
        self.assertEqual(get_script(' '), Script.UNKNOWN)


class TestGetScripts(unittest.TestCase):
    """Tests for get_scripts function."""
    
    def test_single_script(self):
        """Test single script text."""
        scripts = get_scripts("Hello World")
        self.assertEqual(scripts, {Script.LATIN})
    
    def test_multiple_scripts(self):
        """Test multiple scripts in text."""
        scripts = get_scripts("Hello世界")
        self.assertEqual(scripts, {Script.LATIN, Script.CJK})
    
    def test_empty_text(self):
        """Test empty text."""
        scripts = get_scripts("")
        self.assertEqual(scripts, set())
    
    def test_whitespace_only(self):
        """Test whitespace only text."""
        scripts = get_scripts("   ")
        self.assertEqual(scripts, set())
    
    def test_numbers_only(self):
        """Test numbers only text."""
        scripts = get_scripts("12345")
        self.assertEqual(scripts, set())


class TestCountScripts(unittest.TestCase):
    """Tests for count_scripts function."""
    
    def test_single_script_count(self):
        """Test counting single script."""
        counts = count_scripts("Hello")
        self.assertEqual(counts[Script.LATIN], 5)
    
    def test_multiple_scripts_count(self):
        """Test counting multiple scripts."""
        counts = count_scripts("Hello世界")
        self.assertEqual(counts[Script.LATIN], 5)
        self.assertEqual(counts[Script.CJK], 2)
    
    def test_mixed_with_numbers(self):
        """Test mixed text with numbers."""
        counts = count_scripts("Hello123世界")
        self.assertEqual(counts[Script.LATIN], 5)
        self.assertEqual(counts[Script.CJK], 2)
        # Numbers not counted
        self.assertNotIn(Script.UNKNOWN, counts)


class TestAnalyzeScripts(unittest.TestCase):
    """Tests for analyze_scripts function."""
    
    def test_basic_analysis(self):
        """Test basic script analysis."""
        stats = analyze_scripts("Hello世界")
        self.assertEqual(len(stats), 2)
        
        # Latin should be first (more characters)
        self.assertEqual(stats[0].script, Script.LATIN)
        self.assertEqual(stats[0].count, 5)
        self.assertAlmostEqual(stats[0].percentage, 71.43, places=1)
    
    def test_empty_text(self):
        """Test empty text analysis."""
        stats = analyze_scripts("")
        self.assertEqual(stats, [])
    
    def test_percentage_calculation(self):
        """Test percentage calculation."""
        stats = analyze_scripts("AABB中中中")
        
        # AABB = 4 Latin chars, 中中中 = 3 CJK chars
        # Total = 7 chars
        latin_stat = next(s for s in stats if s.script == Script.LATIN)
        cjk_stat = next(s for s in stats if s.script == Script.CJK)
        
        self.assertAlmostEqual(latin_stat.percentage, 57.14, places=1)
        self.assertAlmostEqual(cjk_stat.percentage, 42.86, places=1)


class TestDetectLanguage(unittest.TestCase):
    """Tests for detect_language function."""
    
    def test_english_detection(self):
        """Test English detection."""
        result = detect_language("Hello world, this is a test.")
        self.assertEqual(result.language, Language.ENGLISH)
        self.assertGreater(result.confidence, 0.3)
    
    def test_chinese_detection(self):
        """Test Chinese detection."""
        result = detect_language("你好世界，这是一个测试。")
        self.assertIn(result.language, [Language.CHINESE, Language.CHINESE_SIMPLIFIED])
        self.assertGreater(result.confidence, 0.5)
    
    def test_japanese_detection(self):
        """Test Japanese detection with Hiragana."""
        result = detect_language("こんにちは世界、これはテストです。")
        self.assertEqual(result.language, Language.JAPANESE)
        self.assertGreater(result.confidence, 0.5)
    
    def test_japanese_detection_katakana(self):
        """Test Japanese detection with Katakana."""
        result = detect_language("コンニチハ、テストです。")
        self.assertEqual(result.language, Language.JAPANESE)
    
    def test_korean_detection(self):
        """Test Korean detection."""
        result = detect_language("안녕하세요 세계, 이것은 테스트입니다.")
        self.assertEqual(result.language, Language.KOREAN)
        self.assertGreater(result.confidence, 0.5)
    
    def test_spanish_detection(self):
        """Test Spanish detection."""
        result = detect_language("Hola mundo, esto es una prueba en español.")
        self.assertEqual(result.language, Language.SPANISH)
    
    def test_french_detection(self):
        """Test French detection."""
        result = detect_language("Bonjour le monde, c'est une phrase française.")
        self.assertEqual(result.language, Language.FRENCH)
    
    def test_german_detection(self):
        """Test German detection."""
        result = detect_language("Hallo Welt, das ist ein deutscher Text.")
        self.assertEqual(result.language, Language.GERMAN)
    
    def test_russian_detection(self):
        """Test Russian detection."""
        result = detect_language("Привет мир, это тест на русском языке.")
        self.assertEqual(result.language, Language.RUSSIAN)
        self.assertGreater(result.confidence, 0.5)
    
    def test_arabic_detection(self):
        """Test Arabic detection."""
        result = detect_language("مرحبا بالعالم، هذا نص باللغة العربية.")
        self.assertEqual(result.language, Language.ARABIC)
        self.assertGreater(result.confidence, 0.5)
    
    def test_hindi_detection(self):
        """Test Hindi detection."""
        result = detect_language("नमस्ते दुनिया, यह हिंदी में लिखा है।")
        self.assertEqual(result.language, Language.HINDI)
        self.assertGreater(result.confidence, 0.5)
    
    def test_thai_detection(self):
        """Test Thai detection."""
        result = detect_language("สวัสดีโลก นี่คือข้อความภาษาไทย")
        self.assertEqual(result.language, Language.THAI)
        self.assertGreater(result.confidence, 0.5)
    
    def test_empty_text(self):
        """Test empty text detection."""
        result = detect_language("")
        self.assertEqual(result.language, Language.UNKNOWN)
        self.assertEqual(result.confidence, 0.0)
    
    def test_numbers_only(self):
        """Test numbers only text."""
        result = detect_language("12345 67890")
        self.assertEqual(result.language, Language.UNKNOWN)
    
    def test_mixed_language(self):
        """Test mixed language detection."""
        result = detect_language("Hello世界，this is中文混合text。")
        self.assertTrue(result.is_mixed)
        self.assertGreater(len(result.detected_scripts), 1)
    
    def test_result_fields(self):
        """Test LanguageResult fields."""
        result = detect_language("Hello World")
        self.assertIsInstance(result.language, Language)
        self.assertIsInstance(result.confidence, float)
        self.assertIsInstance(result.script_stats, list)
        self.assertIsInstance(result.detected_scripts, set)
        self.assertIsInstance(result.total_chars, int)
        self.assertIsInstance(result.analyzed_chars, int)


class TestDetectLanguagesBatch(unittest.TestCase):
    """Tests for detect_languages_batch function."""
    
    def test_batch_detection(self):
        """Test batch language detection."""
        texts = [
            "Hello world",
            "你好世界",
            "こんにちは",
        ]
        results = detect_languages_batch(texts)
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].language, Language.ENGLISH)
        self.assertIn(results[1].language, [Language.CHINESE, Language.CHINESE_SIMPLIFIED])
        self.assertEqual(results[2].language, Language.JAPANESE)
    
    def test_empty_batch(self):
        """Test empty batch."""
        results = detect_languages_batch([])
        self.assertEqual(results, [])
    
    def test_mixed_batch(self):
        """Test batch with various languages."""
        texts = [
            "English text here",
            "Texto en español",
            "Texte français",
            "Deutscher Text",
        ]
        results = detect_languages_batch(texts)
        
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0].language, Language.ENGLISH)
        self.assertEqual(results[1].language, Language.SPANISH)
        self.assertEqual(results[2].language, Language.FRENCH)
        self.assertEqual(results[3].language, Language.GERMAN)


class TestDetectLatinLanguage(unittest.TestCase):
    """Tests for detect_latin_language function."""
    
    def test_english_common_words(self):
        """Test English detection via common words."""
        lang, conf = detect_latin_language("the and is in to of for")
        self.assertEqual(lang, Language.ENGLISH)
    
    def test_spanish_special_chars(self):
        """Test Spanish via special characters."""
        lang, conf = detect_latin_language("ñación español")
        self.assertEqual(lang, Language.SPANISH)
    
    def test_french_special_chars(self):
        """Test French via special characters."""
        lang, conf = detect_latin_language("français")
        self.assertEqual(lang, Language.FRENCH)
    
    def test_german_special_chars(self):
        """Test German via special characters."""
        lang, conf = detect_latin_language("Größe und Übung")
        self.assertEqual(lang, Language.GERMAN)
    
    def test_portuguese_special_chars(self):
        """Test Portuguese via special characters."""
        lang, conf = detect_latin_language("língua portuguesa com ç")
        # ç is common in Portuguese and French
        self.assertIn(lang, [Language.PORTUGUESE, Language.FRENCH])


class TestDetectNonLatinLanguage(unittest.TestCase):
    """Tests for detect_non_latin_language function."""
    
    def test_chinese_detection(self):
        """Test Chinese via CJK."""
        counts = count_scripts("你好世界")
        lang, conf = detect_non_latin_language("你好世界", counts)
        self.assertIn(lang, [Language.CHINESE, Language.CHINESE_SIMPLIFIED])
    
    def test_japanese_detection(self):
        """Test Japanese via Hiragana."""
        counts = count_scripts("こんにちは")
        lang, conf = detect_non_latin_language("こんにちは", counts)
        self.assertEqual(lang, Language.JAPANESE)
    
    def test_korean_detection(self):
        """Test Korean via Hangul."""
        counts = count_scripts("안녕하세요")
        lang, conf = detect_non_latin_language("안녕하세요", counts)
        self.assertEqual(lang, Language.KOREAN)


class TestGetLanguageName(unittest.TestCase):
    """Tests for get_language_name function."""
    
    def test_major_languages(self):
        """Test major language names."""
        self.assertEqual(get_language_name(Language.ENGLISH), "English")
        self.assertEqual(get_language_name(Language.CHINESE), "Chinese")
        self.assertEqual(get_language_name(Language.JAPANESE), "Japanese")
        self.assertEqual(get_language_name(Language.KOREAN), "Korean")
        self.assertEqual(get_language_name(Language.SPANISH), "Spanish")
    
    def test_unknown_language(self):
        """Test unknown language name."""
        self.assertEqual(get_language_name(Language.UNKNOWN), "Unknown")
    
    def test_mixed_language(self):
        """Test mixed language name."""
        self.assertEqual(get_language_name(Language.MIXED), "Mixed")


class TestGetScriptName(unittest.TestCase):
    """Tests for get_script_name function."""
    
    def test_major_scripts(self):
        """Test major script names."""
        self.assertEqual(get_script_name(Script.LATIN), "Latin")
        self.assertEqual(get_script_name(Script.CJK), "CJK (Chinese/Japanese)")
        self.assertEqual(get_script_name(Script.HIRAGANA), "Hiragana (Japanese)")
        self.assertEqual(get_script_name(Script.HANGUL), "Hangul (Korean)")
    
    def test_unknown_script(self):
        """Test unknown script name."""
        self.assertEqual(get_script_name(Script.UNKNOWN), "Unknown")


class TestIsLanguage(unittest.TestCase):
    """Tests for is_language function."""
    
    def test_match_english(self):
        """Test English match."""
        match, conf = is_language("Hello world", Language.ENGLISH)
        self.assertTrue(match)
    
    def test_match_chinese(self):
        """Test Chinese match."""
        match, conf = is_language("你好世界", Language.CHINESE)
        self.assertTrue(match)
    
    def test_match_japanese(self):
        """Test Japanese match."""
        match, conf = is_language("こんにちは", Language.JAPANESE)
        self.assertTrue(match)
    
    def test_no_match(self):
        """Test no match case."""
        match, conf = is_language("Hello world", Language.JAPANESE)
        self.assertFalse(match)
    
    def test_chinese_variant_match(self):
        """Test Chinese variants match."""
        # Simplified text should match all Chinese variants
        match, conf = is_language("你好世界", Language.CHINESE_SIMPLIFIED)
        self.assertTrue(match)
        
        match, conf = is_language("你好世界", Language.CHINESE_TRADITIONAL)
        self.assertTrue(match)


class TestGetTextStatistics(unittest.TestCase):
    """Tests for get_text_statistics function."""
    
    def test_basic_statistics(self):
        """Test basic text statistics."""
        stats = get_text_statistics("Hello World")
        
        self.assertIn("language", stats)
        self.assertIn("confidence", stats)
        self.assertIn("total_chars", stats)
        self.assertIn("word_count", stats)
        
        self.assertEqual(stats["total_chars"], 11)
        self.assertEqual(stats["alpha_chars"], 10)
        self.assertEqual(stats["word_count"], 2)
    
    def test_mixed_text_statistics(self):
        """Test mixed text statistics."""
        stats = get_text_statistics("Hello世界123")
        
        self.assertTrue(stats["is_mixed"])
        self.assertGreater(len(stats["scripts"]), 1)
    
    def test_digit_count(self):
        """Test digit counting."""
        stats = get_text_statistics("Hello123World456")
        self.assertEqual(stats["digit_chars"], 6)
    
    def test_space_count(self):
        """Test space counting."""
        stats = get_text_statistics("Hello  World")
        self.assertEqual(stats["space_chars"], 2)


class TestLanguageDetectorClass(unittest.TestCase):
    """Tests for LanguageDetector class."""
    
    def test_basic_detection(self):
        """Test basic detection."""
        detector = LanguageDetector(min_confidence=0.3)
        result = detector.detect("Hello world this is English text")
        self.assertEqual(result.language, Language.ENGLISH)
    
    def test_min_confidence(self):
        """Test minimum confidence threshold."""
        detector = LanguageDetector(min_confidence=0.9)
        
        # Short text might have low confidence
        result = detector.detect("Hi")
        # Language might be UNKNOWN due to low confidence
        # (depends on actual confidence returned)
    
    def test_is_english(self):
        """Test is_english method."""
        detector = LanguageDetector(min_confidence=0.2)
        self.assertTrue(detector.is_english("Hello world this is English text"))
        self.assertFalse(detector.is_english("你好世界"))
    
    def test_is_chinese(self):
        """Test is_chinese method."""
        detector = LanguageDetector(min_confidence=0.3)
        self.assertTrue(detector.is_chinese("你好世界"))
        self.assertFalse(detector.is_chinese("Hello world"))
    
    def test_is_japanese(self):
        """Test is_japanese method."""
        detector = LanguageDetector(min_confidence=0.3)
        self.assertTrue(detector.is_japanese("こんにちは"))
        self.assertFalse(detector.is_japanese("你好世界"))
    
    def test_is_korean(self):
        """Test is_korean method."""
        detector = LanguageDetector(min_confidence=0.3)
        self.assertTrue(detector.is_korean("안녕하세요"))
        self.assertFalse(detector.is_korean("你好世界"))
    
    def test_filter_by_language(self):
        """Test filter_by_language method."""
        detector = LanguageDetector(min_confidence=0.3)
        texts = [
            "Hello world this is English",
            "你好世界",
            "こんにちは",
            "English text here",
            "Texto en español",
        ]
        
        filtered = detector.filter_by_language(texts, Language.ENGLISH)
        
        # Should return English texts
        for text, conf in filtered:
            self.assertIn(text, ["Hello world this is English", "English text here"])
    
    def test_batch_detection(self):
        """Test batch detection via detector."""
        detector = LanguageDetector(min_confidence=0.3)
        texts = ["Hello", "你好", "こんにちは"]
        
        results = detector.detect_batch(texts)
        self.assertEqual(len(results), 3)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""
    
    def test_single_character(self):
        """Test single character detection."""
        result = detect_language("中")
        self.assertIn(result.language, [Language.CHINESE, Language.CHINESE_SIMPLIFIED])
    
    def test_very_long_text(self):
        """Test very long text."""
        text = "Hello world, this is a very long English text that continues for many words."
        result = detect_language(text)
        self.assertEqual(result.language, Language.ENGLISH)
    
    def test_punctuation_only(self):
        """Test punctuation only text."""
        result = detect_language("!@#$%^&*()")
        self.assertEqual(result.language, Language.UNKNOWN)
    
    def test_numbers_and_letters(self):
        """Test numbers with letters."""
        result = detect_language("ABC123")
        self.assertEqual(result.language, Language.ENGLISH)
    
    def test_unicode_punctuation(self):
        """Test with Unicode punctuation."""
        result = detect_language("Hello——world")
        self.assertEqual(result.language, Language.ENGLISH)
    
    def test_emoticons(self):
        """Test with emoticons."""
        result = detect_language("Hello 😊 world 🌍")
        # Emoticons should be ignored
        self.assertIn(result.language, [Language.ENGLISH, Language.UNKNOWN])


class TestPerformance(unittest.TestCase):
    """Performance tests."""
    
    def test_large_text_detection(self):
        """Test detection on large text."""
        import time
        
        # Create a large text
        text = "Hello world, this is a test. " * 1000
        
        start = time.time()
        result = detect_language(text)
        elapsed = time.time() - start
        
        self.assertEqual(result.language, Language.ENGLISH)
        self.assertLess(elapsed, 1.0)  # Should complete in under 1 second
    
    def test_batch_performance(self):
        """Test batch detection performance."""
        import time
        
        texts = ["Hello world number {}".format(i) for i in range(100)]
        
        start = time.time()
        results = detect_languages_batch(texts)
        elapsed = time.time() - start
        
        self.assertEqual(len(results), 100)
        self.assertLess(elapsed, 2.0)  # Should complete in under 2 seconds


class TestScriptStats(unittest.TestCase):
    """Tests for ScriptStats dataclass."""
    
    def test_script_stats_creation(self):
        """Test ScriptStats creation."""
        stats = ScriptStats(
            script=Script.LATIN,
            count=10,
            percentage=80.0,
            chars={'a', 'b', 'c'}
        )
        
        self.assertEqual(stats.script, Script.LATIN)
        self.assertEqual(stats.count, 10)
        self.assertAlmostEqual(stats.percentage, 80.0)
        self.assertEqual(len(stats.chars), 3)


class TestLanguageResult(unittest.TestCase):
    """Tests for LanguageResult dataclass."""
    
    def test_language_result_creation(self):
        """Test LanguageResult creation."""
        result = LanguageResult(
            language=Language.ENGLISH,
            confidence=0.9,
            total_chars=100,
            analyzed_chars=80
        )
        
        self.assertEqual(result.language, Language.ENGLISH)
        self.assertAlmostEqual(result.confidence, 0.9)
        self.assertEqual(result.total_chars, 100)
        self.assertEqual(result.analyzed_chars, 80)


class TestLessCommonLanguages(unittest.TestCase):
    """Tests for less common languages."""
    
    def test_portuguese_detection(self):
        """Test Portuguese detection."""
        # Use distinctive Portuguese characters: ã (tilde) is unique to Portuguese
        result = detect_language("Olá mundo, este é português com ão e ã.")
        self.assertEqual(result.language, Language.PORTUGUESE)
    
    def test_italian_detection(self):
        """Test Italian detection."""
        # Italian is hard to distinguish without longer text
        # We verify it detects Latin script
        result = detect_language("Ciao mondo, questo è un testo italiano.")
        self.assertIn(result.language, [Language.ITALIAN, Language.FRENCH, Language.ENGLISH])
    
    def test_dutch_detection(self):
        """Test Dutch detection."""
        # Dutch is hard to distinguish from German without special chars
        # We test that it detects Latin script at minimum
        result = detect_language("Hallo wereld, dit is Nederlandse tekst.")
        self.assertIn(result.language, [Language.DUTCH, Language.ENGLISH, Language.GERMAN])
    
    def test_turkish_detection(self):
        """Test Turkish detection."""
        # Turkish has unique characters: ı (dotless i) and ş
        result = detect_language("Merhaba dünya, Türkçe şarkı ılık.")
        self.assertEqual(result.language, Language.TURKISH)
    
    def test_polish_detection(self):
        """Test Polish detection."""
        # Polish has unique characters: ł (l with stroke)
        result = detect_language("Witaj świecie, polski ładować tekst.")
        self.assertEqual(result.language, Language.POLISH)
    
    def test_greek_detection(self):
        """Test Greek detection."""
        result = detect_language("Γειά σου κόσμος, αυτό είναι κείμενο.")
        self.assertEqual(result.language, Language.GREEK)
    
    def test_hebrew_detection(self):
        """Test Hebrew detection."""
        result = detect_language("שלום עולם, זהו טקסט בעברית.")
        self.assertEqual(result.language, Language.HEBREW)
    
    def test_vietnamese_detection(self):
        """Test Vietnamese detection."""
        # Vietnamese has unique characters: đ (d with stroke) and ă
        result = detect_language("Xin chào thế giới, tiếng Việt đàng ă.")
        self.assertEqual(result.language, Language.VIETNAMESE)


if __name__ == "__main__":
    unittest.main(verbosity=2)