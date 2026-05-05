"""
Pig Latin Utilities Test Suite

Comprehensive tests for Pig Latin translation and decoding.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    PigLatinTranslator,
    translate_word,
    decode_word,
    translate_sentence,
    decode_sentence,
    translate_words,
    decode_words,
    get_pig_latin_rules
)


class TestResult:
    """Simple test result collector."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_equal(self, actual, expected, message=""):
        if actual == expected:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"  ✗ {message}: expected {expected!r}, got {actual!r}")
            return False
    
    def assert_true(self, condition, message=""):
        if condition:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"  ✗ {message}: expected True, got False")
            return False
    
    def assert_false(self, condition, message=""):
        if not condition:
            self.passed += 1
            return True
        else:
            self.failed += 1
            self.errors.append(f"  ✗ {message}: expected False, got True")
            return False
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Tests: {total} total, {self.passed} passed, {self.failed} failed")
        if self.errors:
            print("\nFailures:")
            for error in self.errors:
                print(error)
        print('='*60)
        return self.failed == 0


def test_basic_vowel_words():
    """Test translation of vowel-starting words."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    result.assert_equal(translator.translate_word("apple"), "appleway", "apple -> appleway")
    result.assert_equal(translator.translate_word("egg"), "eggway", "egg -> eggway")
    result.assert_equal(translator.translate_word("orange"), "orangeway", "orange -> orangeway")
    result.assert_equal(translator.translate_word("elephant"), "elephantway", "elephant -> elephantway")
    result.assert_equal(translator.translate_word("ice"), "iceway", "ice -> iceway")
    result.assert_equal(translator.translate_word("umbrella"), "umbrellaway", "umbrella -> umbrellaway")
    
    return result


def test_basic_consonant_words():
    """Test translation of consonant-starting words."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    result.assert_equal(translator.translate_word("hello"), "ellohay", "hello -> ellohay")
    result.assert_equal(translator.translate_word("world"), "orldway", "world -> orldway")
    result.assert_equal(translator.translate_word("pig"), "igpay", "pig -> igpay")
    result.assert_equal(translator.translate_word("latin"), "atinlay", "latin -> atinlay")
    result.assert_equal(translator.translate_word("dog"), "ogday", "dog -> ogday")
    result.assert_equal(translator.translate_word("cat"), "atcay", "cat -> atcay")
    
    return result


def test_consonant_clusters():
    """Test words with consonant clusters."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    result.assert_equal(translator.translate_word("string"), "ingstray", "string -> ingstray")
    result.assert_equal(translator.translate_word("smile"), "ilesmay", "smile -> ilesmay")
    result.assert_equal(translator.translate_word("chair"), "airchay", "chair -> airchay")
    result.assert_equal(translator.translate_word("three"), "eethray", "three -> eethray")
    result.assert_equal(translator.translate_word("school"), "oolschay", "school -> oolschay")
    result.assert_equal(translator.translate_word("quiet"), "ietquay", "quiet -> ietquay")
    
    return result


def test_capitalization():
    """Test capitalization preservation."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    result.assert_equal(translator.translate_word("Hello"), "Ellohay", "Hello -> Ellohay")
    result.assert_equal(translator.translate_word("APPLE"), "Appleway", "APPLE -> Appleway")  # Converts to title case
    result.assert_equal(translator.translate_word("World"), "Orldway", "World -> Orldway")
    result.assert_equal(translator.translate_word("String"), "Ingstray", "String -> Ingstray")
    
    return result


def test_punctuation():
    """Test punctuation handling."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    result.assert_equal(translator.translate_word("hello!"), "ellohay!", "hello! -> ellohay!")
    result.assert_equal(translator.translate_word("world."), "orldway.", "world. -> orldway.")
    result.assert_equal(translator.translate_word("apple,"), "appleway,", "apple, -> appleway,")
    result.assert_equal(translator.translate_word("'hello'"), "'ellohay'", "'hello' -> 'ellohay'")
    result.assert_equal(translator.translate_word("(test)"), "(esttay)", "(test) -> (esttay)")
    
    return result


def test_sentences():
    """Test sentence translation."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    result.assert_equal(
        translator.translate_sentence("Hello world"),
        "Ellohay orldway",
        "Hello world -> Ellohay orldway"
    )
    result.assert_equal(
        translator.translate_sentence("The quick brown fox"),
        "Ethay ickquay ownbray oxfay",
        "The quick brown fox translation"
    )
    result.assert_equal(
        translator.translate_sentence("Hello, world!"),
        "Ellohay, orldway!",
        "Hello, world! -> Ellohay, orldway!"
    )
    
    return result


def test_decode_vowel_words():
    """Test decoding of vowel-starting words."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    result.assert_equal(translator.decode_word("appleway"), "apple", "appleway -> apple")
    result.assert_equal(translator.decode_word("eggway"), "egg", "eggway -> egg")
    result.assert_equal(translator.decode_word("orangeway"), "orange", "orangeway -> orange")
    result.assert_equal(translator.decode_word("elephantway"), "elephant", "elephantway -> elephant")
    
    return result


def test_decode_consonant_words():
    """Test decoding of consonant-starting words."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    result.assert_equal(translator.decode_word("ellohay"), "hello", "ellohay -> hello")
    result.assert_equal(translator.decode_word("orldway"), "world", "orldway -> world")
    result.assert_equal(translator.decode_word("igpay"), "pig", "igpay -> pig")
    result.assert_equal(translator.decode_word("atinlay"), "latin", "atinlay -> latin")
    result.assert_equal(translator.decode_word("ingstray"), "string", "ingstray -> string")
    result.assert_equal(translator.decode_word("ietquay"), "quiet", "ietquay -> quiet")
    
    return result


def test_decode_capitalization():
    """Test decoding with capitalization."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    result.assert_equal(translator.decode_word("Ellohay"), "Hello", "Ellohay -> Hello")
    result.assert_equal(translator.decode_word("Orldway"), "World", "Orldway -> World")
    result.assert_equal(translator.decode_word("Ingstray"), "String", "Ingstray -> String")
    
    return result


def test_decode_punctuation():
    """Test decoding with punctuation."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    result.assert_equal(translator.decode_word("ellohay!"), "hello!", "ellohay! -> hello!")
    result.assert_equal(translator.decode_word("orldway."), "world.", "orldway. -> world.")
    result.assert_equal(translator.decode_word("'ellohay'"), "'hello'", "'ellohay' -> 'hello'")
    
    return result


def test_decode_sentences():
    """Test sentence decoding."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    result.assert_equal(
        translator.decode_sentence("Ellohay orldway"),
        "Hello world",
        "Ellohay orldway -> Hello world"
    )
    result.assert_equal(
        translator.decode_sentence("Ellohay, orldway!"),
        "Hello, world!",
        "Ellohay, orldway! -> Hello, world!"
    )
    
    return result


def test_roundtrip():
    """Test encoding then decoding returns original."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    test_words = ["hello", "apple", "string", "quiet", "smile", "chair", "school", "world"]
    
    for word in test_words:
        encoded = translator.translate_word(word)
        decoded = translator.decode_word(encoded)
        result.assert_equal(decoded, word, f"Roundtrip for '{word}'")
    
    return result


def test_is_pig_latin():
    """Test Pig Latin detection."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    # Should be detected as Pig Latin
    result.assert_true(translator.is_pig_latin("ellohay"), "ellohay is Pig Latin")
    result.assert_true(translator.is_pig_latin("appleway"), "appleway is Pig Latin")
    result.assert_true(translator.is_pig_latin("ingstray"), "ingstray is Pig Latin")
    
    # Should NOT be detected as Pig Latin
    result.assert_false(translator.is_pig_latin("hello"), "hello is not Pig Latin")
    result.assert_false(translator.is_pig_latin("apple"), "apple is not Pig Latin")
    result.assert_false(translator.is_pig_latin("string"), "string is not Pig Latin")
    
    return result


def test_empty_and_special():
    """Test empty strings and special cases."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    result.assert_equal(translator.translate_word(""), "", "Empty string")
    result.assert_equal(translator.decode_word(""), "", "Empty string decode")
    result.assert_equal(translator.translate_word("123"), "123", "Numbers unchanged")
    result.assert_equal(translator.translate_word("!@#"), "!@#", "Symbols unchanged")
    result.assert_equal(translator.translate_word("a"), "away", "Single vowel")
    result.assert_equal(translator.translate_word("i"), "iway", "Single vowel 'i'")
    
    return result


def test_convenience_functions():
    """Test convenience functions."""
    result = TestResult()
    
    result.assert_equal(translate_word("hello"), "ellohay", "translate_word function")
    result.assert_equal(decode_word("ellohay"), "hello", "decode_word function")
    result.assert_equal(
        translate_sentence("Hello world"),
        "Ellohay orldway",
        "translate_sentence function"
    )
    result.assert_equal(
        decode_sentence("Ellohay orldway"),
        "Hello world",
        "decode_sentence function"
    )
    
    return result


def test_list_functions():
    """Test list translation functions."""
    result = TestResult()
    
    words = ["hello", "apple", "string"]
    expected = ["ellohay", "appleway", "ingstray"]
    result.assert_equal(translate_words(words), expected, "translate_words")
    
    result.assert_equal(decode_words(expected), words, "decode_words")
    
    return result


def test_custom_suffixes():
    """Test custom suffix configuration."""
    result = TestResult()
    
    # Custom suffixes
    translator = PigLatinTranslator(vowel_suffix="yay", consonant_suffix="yay")
    
    result.assert_equal(translator.translate_word("apple"), "appleyay", "Custom vowel suffix")
    result.assert_equal(translator.translate_word("hello"), "ellohay", "Custom consonant suffix")
    
    # Note: With same suffix, decoding might be ambiguous
    
    return result


def test_custom_vowels():
    """Test custom vowel configuration."""
    result = TestResult()
    
    # Treat 'y' as vowel
    translator = PigLatinTranslator(vowels="aeiouy")
    
    result.assert_equal(translator.translate_word("yellow"), "ellowyay", "y as vowel: yellow")
    result.assert_equal(translator.translate_word("rhythm"), "rhythmay", "y as vowel: rhythm")
    
    return result


def test_get_pig_latin_rules():
    """Test rules retrieval."""
    result = TestResult()
    
    rules = get_pig_latin_rules()
    
    result.assert_true("vowel_rule" in rules, "Rules contain vowel_rule")
    result.assert_true("consonant_rule" in rules, "Rules contain consonant_rule")
    result.assert_true("examples" in rules, "Rules contain examples")
    
    return result


def test_no_vowel_words():
    """Test words without vowels."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    # Words like "nth", "tsk" (rare cases)
    result.assert_equal(translator.translate_word("nth"), "nthay", "Word with no vowels")
    result.assert_equal(translator.translate_word("shh"), "shhay", "Interjection with no vowels")
    
    return result


def test_complex_sentences():
    """Test complex sentence structures."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    sentence = "The quick brown fox jumps over the lazy dog."
    translated = translator.translate_sentence(sentence)
    decoded = translator.decode_sentence(translated)
    
    # Should preserve structure
    result.assert_true(decoded.endswith("."), "Preserves ending period")
    result.assert_true("fox" in decoded.lower(), "Contains 'fox'")
    
    return result


def test_numbers_and_mixed():
    """Test words with numbers and mixed content."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    result.assert_equal(translator.translate_word("hello123"), "ellohay123", "Word with numbers")
    result.assert_equal(translator.translate_word("test!@#"), "esttay!@#", "Word with symbols")
    
    return result


def test_single_consonant():
    """Test single consonant words."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    result.assert_equal(translator.translate_word("be"), "ebay", "be -> ebay")
    result.assert_equal(translator.translate_word("do"), "oday", "do -> oday")
    result.assert_equal(translator.translate_word("go"), "ogay", "go -> ogay")
    
    return result


def test_y_handling():
    """Test handling of 'y' (sometimes vowel, sometimes consonant)."""
    result = TestResult()
    translator = PigLatinTranslator()
    
    # 'y' at start is consonant
    result.assert_equal(translator.translate_word("yes"), "esyay", "yes -> esyay")
    result.assert_equal(translator.translate_word("yellow"), "ellowyay", "yellow -> ellowyay")
    
    # 'y' in middle is vowel (handled by standard rules)
    result.assert_equal(translator.translate_word("style"), "ylestay", "style -> ylestay")
    
    return result


def run_all_tests():
    """Run all test functions."""
    print("\n" + "="*60)
    print("Pig Latin Utilities Test Suite")
    print("="*60)
    
    test_functions = [
        ("Basic Vowel Words", test_basic_vowel_words),
        ("Basic Consonant Words", test_basic_consonant_words),
        ("Consonant Clusters", test_consonant_clusters),
        ("Capitalization", test_capitalization),
        ("Punctuation", test_punctuation),
        ("Sentences", test_sentences),
        ("Decode Vowel Words", test_decode_vowel_words),
        ("Decode Consonant Words", test_decode_consonant_words),
        ("Decode Capitalization", test_decode_capitalization),
        ("Decode Punctuation", test_decode_punctuation),
        ("Decode Sentences", test_decode_sentences),
        ("Roundtrip", test_roundtrip),
        ("Is Pig Latin", test_is_pig_latin),
        ("Empty and Special", test_empty_and_special),
        ("Convenience Functions", test_convenience_functions),
        ("List Functions", test_list_functions),
        ("Custom Suffixes", test_custom_suffixes),
        ("Custom Vowels", test_custom_vowels),
        ("Get Rules", test_get_pig_latin_rules),
        ("No Vowel Words", test_no_vowel_words),
        ("Complex Sentences", test_complex_sentences),
        ("Numbers and Mixed", test_numbers_and_mixed),
        ("Single Consonant", test_single_consonant),
        ("Y Handling", test_y_handling),
    ]
    
    all_passed = True
    
    for name, test_func in test_functions:
        print(f"\n{name}:")
        result = test_func()
        status = "✓ PASSED" if result.failed == 0 else f"✗ FAILED ({result.failed})"
        print(f"  {status}")
        all_passed = all_passed and (result.failed == 0)
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    print("="*60)
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)