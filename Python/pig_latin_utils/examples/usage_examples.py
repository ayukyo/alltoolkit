"""
Pig Latin Utilities - Usage Examples

This file demonstrates various ways to use the Pig Latin translation utilities.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


def example_basic_translation():
    """Basic word translation examples."""
    print("\n" + "="*60)
    print("Example 1: Basic Word Translation")
    print("="*60)
    
    translator = PigLatinTranslator()
    
    # Vowel-starting words
    vowel_words = ["apple", "egg", "orange", "elephant", "ice", "umbrella"]
    print("\nVowel-starting words (add 'way'):")
    for word in vowel_words:
        translated = translator.translate_word(word)
        print(f"  {word:>10} -> {translated}")
    
    # Consonant-starting words
    consonant_words = ["hello", "world", "pig", "latin", "dog", "cat"]
    print("\nConsonant-starting words (move cluster + add 'ay'):")
    for word in consonant_words:
        translated = translator.translate_word(word)
        print(f"  {word:>10} -> {translated}")
    
    # Consonant clusters
    cluster_words = ["string", "smile", "chair", "three", "school", "quiet"]
    print("\nWords with consonant clusters:")
    for word in cluster_words:
        translated = translator.translate_word(word)
        print(f"  {word:>10} -> {translated}")


def example_decoding():
    """Decoding Pig Latin back to English."""
    print("\n" + "="*60)
    print("Example 2: Decoding Pig Latin")
    print("="*60)
    
    translator = PigLatinTranslator()
    
    pig_latin_words = ["ellohay", "appleway", "ingstray", "igpay", "atinlay"]
    print("\nDecoding Pig Latin to English:")
    for word in pig_latin_words:
        decoded = translator.decode_word(word)
        print(f"  {word:>10} -> {decoded}")


def example_sentences():
    """Sentence translation examples."""
    print("\n" + "="*60)
    print("Example 3: Sentence Translation")
    print("="*60)
    
    translator = PigLatinTranslator()
    
    sentences = [
        "Hello, world!",
        "The quick brown fox jumps over the lazy dog.",
        "Pig Latin is fun!",
        "I love programming.",
        "What time is it?"
    ]
    
    for sentence in sentences:
        translated = translator.translate_sentence(sentence)
        decoded = translator.decode_sentence(translated)
        print(f"\nOriginal:  {sentence}")
        print(f"Pig Latin: {translated}")
        print(f"Decoded:   {decoded}")


def example_convenience_functions():
    """Using convenience functions."""
    print("\n" + "="*60)
    print("Example 4: Convenience Functions")
    print("="*60)
    
    # Using module-level functions
    print("\nUsing translate_word():")
    print(f"  hello -> {translate_word('hello')}")
    print(f"  apple -> {translate_word('apple')}")
    
    print("\nUsing decode_word():")
    print(f"  ellohay -> {decode_word('ellohay')}")
    print(f"  appleway -> {decode_word('appleway')}")
    
    print("\nUsing translate_sentence():")
    sentence = "Hello world"
    translated = translate_sentence(sentence)
    print(f"  {sentence} -> {translated}")
    
    print("\nUsing translate_words() for lists:")
    words = ["hello", "apple", "string"]
    translated_list = translate_words(words)
    print(f"  {words} -> {translated_list}")


def example_custom_settings():
    """Custom translator settings."""
    print("\n" + "="*60)
    print("Example 5: Custom Settings")
    print("="*60)
    
    # Custom suffixes (different dialect)
    print("\nCustom suffixes ('yay' for both):")
    translator_yay = PigLatinTranslator(vowel_suffix="yay", consonant_suffix="yay")
    print(f"  apple -> {translator_yay.translate_word('apple')}")
    print(f"  hello -> {translator_yay.translate_word('hello')}")
    
    # Treat 'y' as vowel
    print("\nTreating 'y' as vowel:")
    translator_y_vowel = PigLatinTranslator(vowels="aeiouy")
    print(f"  yellow -> {translator_y_vowel.translate_word('yellow')}")
    print(f"  rhythm -> {translator_y_vowel.translate_word('rhythm')}")


def example_pig_latin_detection():
    """Detecting Pig Latin words."""
    print("\n" + "="*60)
    print("Example 6: Pig Latin Detection")
    print("="*60)
    
    translator = PigLatinTranslator()
    
    test_words = [
        "hello",      # English
        "ellohay",    # Pig Latin
        "apple",      # English
        "appleway",   # Pig Latin
        "string",     # English
        "ingstray",   # Pig Latin
    ]
    
    print("\nDetecting Pig Latin:")
    for word in test_words:
        is_pl = translator.is_pig_latin(word)
        status = "✓ Pig Latin" if is_pl else "✗ English"
        print(f"  {word:>10} -> {status}")


def example_rules():
    """Displaying Pig Latin rules."""
    print("\n" + "="*60)
    print("Example 7: Pig Latin Rules")
    print("="*60)
    
    rules = get_pig_latin_rules()
    
    print(f"\nVowel rule: {rules['vowel_rule']}")
    print(f"Consonant rule: {rules['consonant_rule']}")
    
    print("\nExamples:")
    for category, examples in rules['examples'].items():
        print(f"\n  {category}:")
        for original, translated in examples.items():
            print(f"    {original} -> {translated}")


def example_roundtrip():
    """Roundtrip translation verification."""
    print("\n" + "="*60)
    print("Example 8: Roundtrip Translation")
    print("="*60)
    
    translator = PigLatinTranslator()
    
    words = ["hello", "apple", "string", "quiet", "smile", "world"]
    
    print("\nVerifying encode -> decode returns original:")
    for word in words:
        encoded = translator.translate_word(word)
        decoded = translator.decode_word(encoded)
        status = "✓" if decoded == word else "✗"
        print(f"  {status} {word} -> {encoded} -> {decoded}")


def example_fun_phrases():
    """Fun Pig Latin phrases."""
    print("\n" + "="*60)
    print("Example 9: Fun Pig Latin Phrases")
    print("="*60)
    
    translator = PigLatinTranslator()
    
    phrases = [
        "Happy birthday!",
        "I love you",
        "Good morning",
        "See you later",
        "Have a nice day",
        "Welcome to the club",
        "Secret message"
    ]
    
    print("\nFun translations:")
    for phrase in phrases:
        translated = translator.translate_sentence(phrase)
        print(f"\n  {phrase}")
        print(f"  {translated}")


def example_game():
    """Simple Pig Latin game."""
    print("\n" + "="*60)
    print("Example 10: Pig Latin Guessing Game")
    print("="*60)
    
    translator = PigLatinTranslator()
    
    # Game: guess the original word
    quiz = [
        ("igpay", "pig"),
        ("appleway", "apple"),
        ("ellohay", "hello"),
        ("ingstray", "string"),
        ("eletay", "television"),  # This might vary
    ]
    
    print("\nGuess the original English word!")
    print("(Answers shown below)")
    
    for pig_latin, answer in quiz:
        print(f"\n  Pig Latin: {pig_latin}")
        print(f"  Answer: {answer}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("🐷 Pig Latin Utilities - Usage Examples")
    print("="*60)
    
    example_basic_translation()
    example_decoding()
    example_sentences()
    example_convenience_functions()
    example_custom_settings()
    example_pig_latin_detection()
    example_rules()
    example_roundtrip()
    example_fun_phrases()
    example_game()
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()