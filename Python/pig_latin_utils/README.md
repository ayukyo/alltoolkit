# Pig Latin Utilities 🐷

**Pig Latin Translation Toolkit - Encode and decode Pig Latin with ease!**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/)

---

## 📖 Overview

Pig Latin is a language game where words are altered according to simple rules. This toolkit provides complete encoding and decoding functionality with:

- **Word and sentence translation**
- **Encoding and decoding support**
- **Punctuation and capitalization preservation**
- **Customizable rules**
- **Detection utilities**

---

## 🎯 Features

- ✅ Zero dependencies (pure Python standard library)
- ✅ Complete encode/decode support
- ✅ Preserves punctuation and capitalization
- ✅ Handles consonant clusters correctly
- ✅ Customizable suffixes and vowel definitions
- ✅ Sentence-level translation
- ✅ Pig Latin detection
- ✅ Comprehensive test coverage (50+ test cases)

---

## 🚀 Quick Start

### Installation

```bash
# No installation needed - just import the module
from pig_latin_utils import translate_word, decode_word
```

### Basic Usage

```python
from mod import PigLatinTranslator, translate_word, decode_word

# Simple word translation
print(translate_word("hello"))    # "ellohay"
print(translate_word("apple"))    # "appleway"
print(translate_word("string"))   # "ingstray"

# Decode back to English
print(decode_word("ellohay"))     # "hello"
print(decode_word("appleway"))    # "apple"

# Sentence translation
from mod import translate_sentence

print(translate_sentence("Hello, world!"))
# "Ellohay, orldway!"
```

---

## 📚 Pig Latin Rules

### Vowel Rule
Words starting with a vowel: add "way" to the end
```
apple  → appleway
egg    → eggway
orange → orangeway
```

### Consonant Rule
Words starting with consonant(s): move consonant cluster to end and add "ay"
```
hello  → ellohay
string → ingstray
world  → orldway
pig    → igpay
```

### Special Cases
- **Capitalization preserved**: "Hello" → "Ellohay"
- **Punctuation preserved**: "Hello!" → "Ellohay!"
- **Consonant clusters handled**: "string" → "ingstray" (not "tringsay")

---

## 📋 API Reference

### PigLatinTranslator Class

```python
translator = PigLatinTranslator(
    vowel_suffix="way",      # Suffix for vowel-starting words
    consonant_suffix="ay",    # Suffix for consonant-starting words
    vowels="aeiou"            # Vowel characters
)
```

#### Methods

| Method | Description | Example |
|--------|-------------|---------|
| `translate_word(word)` | Translate a single word to Pig Latin | `"hello"` → `"ellohay"` |
| `decode_word(word)` | Decode a Pig Latin word to English | `"ellohay"` → `"hello"` |
| `translate_sentence(sentence)` | Translate a full sentence | `"Hello world"` → `"Ellohay orldway"` |
| `decode_sentence(sentence)` | Decode a Pig Latin sentence | `"Ellohay orldway"` → `"Hello world"` |
| `is_pig_latin(word)` | Check if word is Pig Latin format | `"ellohay"` → `True` |

### Convenience Functions

```python
from mod import (
    translate_word,      # Single word translation
    decode_word,         # Single word decoding
    translate_sentence,  # Sentence translation
    decode_sentence,     # Sentence decoding
    translate_words,      # List of words translation
    decode_words,         # List of words decoding
    get_pig_latin_rules   # Get rule descriptions
)
```

---

## 💡 Examples

### Word Translation

```python
translator = PigLatinTranslator()

# Vowel-starting words
print(translator.translate_word("apple"))     # appleway
print(translator.translate_word("elephant"))  # elephantway

# Consonant-starting words
print(translator.translate_word("hello"))     # ellohay
print(translator.translate_word("world"))     # orldway

# Consonant clusters
print(translator.translate_word("string"))    # ingstray
print(translator.translate_word("quiet"))     # ietquay
```

### Sentence Translation

```python
translator = PigLatinTranslator()

sentence = "The quick brown fox jumps over the lazy dog."
translated = translator.translate_sentence(sentence)
print(translated)
# Ethay ickquay ownbray oxfay umpsjay overay ethay azylay ogday.

decoded = translator.decode_sentence(translated)
print(decoded)
# The quick brown fox jumps over the lazy dog.
```

### Pig Latin Detection

```python
translator = PigLatinTranslator()

print(translator.is_pig_latin("ellohay"))   # True
print(translator.is_pig_latin("hello"))     # False
```

### Custom Settings

```python
# Different dialect with "yay" suffix
translator = PigLatinTranslator(
    vowel_suffix="yay",
    consonant_suffix="yay"
)

print(translator.translate_word("apple"))  # appleyay
print(translator.translate_word("hello"))  # ellohay

# Treat 'y' as vowel
translator = PigLatinTranslator(vowels="aeiouy")
print(translator.translate_word("yellow"))  # ellowyay
```

---

## 🧪 Testing

Run the test suite:

```bash
python pig_latin_utils_test.py
```

### Test Coverage

- ✅ Basic vowel word translation
- ✅ Basic consonant word translation
- ✅ Consonant clusters
- ✅ Capitalization preservation
- ✅ Punctuation handling
- ✅ Sentence translation
- ✅ Decoding (vowel and consonant words)
- ✅ Roundtrip verification
- ✅ Pig Latin detection
- ✅ Empty and special cases
- ✅ Custom settings
- ✅ Edge cases (no vowels, numbers, mixed content)

**Total: 50+ test cases**

---

## 🎮 Fun Examples

### Secret Messages

```python
translator = PigLatinTranslator()

secret = translator.translate_sentence("Meet me at the park")
print(secret)  # Eetmay emay atway ethay arkpay

# Decode
original = translator.decode_sentence(secret)
print(original)  # Meet me at the park
```

### Classic Phrases

```python
phrases = [
    "Happy birthday!",
    "I love you",
    "Good morning",
    "Have a nice day"
]

for phrase in phrases:
    print(translator.translate_sentence(phrase))
```

---

## 📊 Performance

- **Translation**: O(n) where n is word length
- **Sentence**: O(m × n) where m is number of words
- **Memory**: O(1) for translation, O(m) for sentences

---

## 🤝 Contributing

Contributions welcome! Please ensure:
1. All tests pass
2. New features include tests
3. Code follows existing style

---

## 📄 License

MIT License - See [LICENSE](../../LICENSE) for details.

---

## 🔗 Related Modules

- `morse_utils` - Morse code translation
- `nato_phonetic_utils` - NATO phonetic alphabet
- `braille_utils` - Braille encoding/decoding
- `leet_speak_utils` - Leet speak transformation

---

## 📝 Changelog

### v1.0.0 (2026-05-05)
- Initial release
- Full encode/decode support
- Sentence translation
- Customizable settings
- Comprehensive test suite (50+ tests)
- Complete documentation

---

**Made with ❤️ for the AllToolkit project**