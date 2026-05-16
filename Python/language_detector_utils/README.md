# Language Detector Utils

Lightweight language detection based on Unicode character ranges. Zero external dependencies - pure Python implementation.

## Features

- **20+ Languages**: Chinese, Japanese, Korean, English, Spanish, French, German, Russian, Arabic, Hindi, Thai, Vietnamese, Portuguese, Italian, Dutch, Turkish, Polish, Greek, Hebrew, and more
- **Unicode Script-Based Detection**: Fast identification via character ranges
- **Latin Script Language Detection**: Pattern-based detection for European languages
- **Mixed Language Support**: Detect multiple languages in same text
- **Confidence Scoring**: Know how certain the detection is
- **Text Statistics**: Comprehensive analysis of text composition
- **Zero Dependencies**: Pure Python standard library

## Installation

```python
from language_detector_utils import (
    detect_language,
    LanguageDetector,
    get_text_statistics,
    is_language,
    Language,
    Script,
)
```

## Quick Start

### Basic Detection

```python
from language_detector_utils import detect_language, get_language_name

# Detect single language
result = detect_language("Hello world, this is English.")
print(f"Language: {get_language_name(result.language)}")
print(f"Confidence: {result.confidence:.2f}")

# Detect Chinese
result = detect_language("你好世界，这是中文。")
print(f"Language: {get_language_name(result.language)}")  # Chinese

# Detect Japanese
result = detect_language("こんにちは世界")
print(f"Language: {get_language_name(result.language)}")  # Japanese
```

### LanguageDetector Class

```python
from language_detector_utils import LanguageDetector

detector = LanguageDetector(min_confidence=0.5)

# Detect language
result = detector.detect("Hello world")
print(result.language)  # Language.ENGLISH

# Quick checks
print(detector.is_english("Hello world"))  # True
print(detector.is_chinese("你好世界"))      # True
print(detector.is_japanese("こんにちは"))   # True
print(detector.is_korean("안녕하세요"))     # True

# Filter texts by language
texts = ["Hello", "你好", "こんにちは", "World", "Texto en español"]
english_texts = detector.filter_by_language(texts, Language.ENGLISH)
# [("Hello", 0.8), ("World", 0.7)]
```

### Text Statistics

```python
from language_detector_utils import get_text_statistics

stats = get_text_statistics("Hello世界，这是混合文本！")
print(stats)
# {
#   "language": "Chinese",
#   "confidence": 0.75,
#   "is_mixed": True,
#   "scripts": {"Latin": 5, "CJK": 8},
#   "total_chars": 18,
#   "alpha_chars": 13,
#   "word_count": 3,
#   ...
# }
```

### Mixed Language Detection

```python
from language_detector_utils import detect_language

result = detect_language("Hello世界，this is中文混合text。")

print(f"Is Mixed: {result.is_mixed}")
print(f"Detected Scripts: {result.detected_scripts}")
print(f"Mixed Languages: {result.mixed_languages}")
# Mixed Languages: [(Language.CHINESE, 0.6), (Language.ENGLISH, 0.3)]
```

### Batch Detection

```python
from language_detector_utils import detect_languages_batch

texts = [
    "Hello world",
    "你好世界",
    "こんにちは",
    "안녕하세요",
]

results = detect_languages_batch(texts)
for i, result in enumerate(results):
    print(f"{texts[i][:10]}: {result.language.value}")
```

### Script Analysis

```python
from language_detector_utils import get_script, get_scripts, analyze_scripts

# Get script for single character
print(get_script('中'))  # Script.CJK
print(get_script('あ'))  # Script.HIRAGANA
print(get_script('A'))  # Script.LATIN

# Get all scripts in text
scripts = get_scripts("Hello世界こんにちは")
print(scripts)  # {Script.LATIN, Script.CJK, Script.HIRAGANA}

# Detailed script analysis
stats = analyze_scripts("Hello世界こんにちは")
for stat in stats:
    print(f"{stat.script}: {stat.count} chars ({stat.percentage:.1f}%)")
```

### Language Verification

```python
from language_detector_utils import is_language

# Check if text is in specific language
match, confidence = is_language("Hello world", Language.ENGLISH)
print(f"Is English: {match}, Confidence: {confidence}")

match, confidence = is_language("你好世界", Language.CHINESE)
print(f"Is Chinese: {match}, Confidence: {confidence}")
```

## Supported Languages

| Language | Code | Detection Method |
|----------|------|-----------------|
| Chinese | zh | CJK script |
| Japanese | ja | Hiragana/Katakana + CJK |
| Korean | ko | Hangul script |
| English | en | Latin + word patterns |
| Spanish | es | Latin + special chars (ñ, á, é) |
| French | fr | Latin + special chars (é, è, ê) |
| German | de | Latin + special chars (ä, ö, ü, ß) |
| Russian | ru | Cyrillic script |
| Arabic | ar | Arabic script |
| Hindi | hi | Devanagari script |
| Thai | th | Thai script |
| Vietnamese | vi | Latin + special chars (ă, đ, ư) |
| Portuguese | pt | Latin + special chars (ã, ç) |
| Italian | it | Latin + word patterns |
| Dutch | nl | Latin + word patterns |
| Turkish | tr | Latin + special chars (ç, ğ, ı, ş, ü) |
| Polish | pl | Latin + special chars (ą, ć, ę, ł, ń) |
| Hebrew | he | Hebrew script |
| Greek | el | Greek script |
| Bengali | bn | Bengali script |
| Punjabi | pa | Gurmukhi script |
| Tamil | ta | Tamil script |
| Telugu | te | Telugu script |
| Kannada | kn | Kannada script |
| Malayalam | ml | Malayalam script |
| Sinhala | si | Sinhala script |
| Myanmar | my | Myanmar script |
| Khmer | km | Khmer script |
| Lao | lo | Lao script |
| Tibetan | bo | Tibetan script |
| Georgian | ka | Georgian script |
| Armenian | hy | Armenian script |

## API Reference

### Functions

- `detect_language(text)` - Detect primary language
- `detect_languages_batch(texts)` - Batch detection
- `get_script(char)` - Get Unicode script for character
- `get_scripts(text)` - Get all scripts in text
- `count_scripts(text)` - Count characters per script
- `analyze_scripts(text)` - Detailed script statistics
- `is_language(text, lang)` - Check if text is specific language
- `get_text_statistics(text)` - Comprehensive text analysis
- `get_language_name(lang)` - Human-readable language name
- `get_script_name(script)` - Human-readable script name

### Classes

- `LanguageDetector(min_confidence)` - Reusable detector class
- `LanguageResult` - Detection result container
- `ScriptStats` - Script statistics container

### Enums

- `Language` - Language identifiers (Language.ENGLISH, Language.CHINESE, etc.)
- `Script` - Script identifiers (Script.LATIN, Script.CJK, etc.)

## LanguageDetector Methods

```python
detector = LanguageDetector()

# Detection
detector.detect(text)              # Detect language
detector.detect_batch(texts)       # Batch detection

# Quick checks
detector.is_english(text)          # Check English
detector.is_chinese(text)          # Check Chinese
detector.is_japanese(text)         # Check Japanese
detector.is_korean(text)           # Check Korean
detector.is_language(text, lang)   # Check specific language

# Analysis
detector.get_statistics(text)      # Get text statistics
detector.filter_by_language(texts, lang)  # Filter by language
```

## Running Tests

```bash
python -m pytest language_detector_utils_test.py -v
# Or
python language_detector_utils_test.py
```

## Use Cases

1. **Content Analysis**: Detect language of user posts, comments, reviews
2. **Multilingual Apps**: Auto-select UI language based on content
3. **Translation Routing**: Route text to appropriate translation service
4. **Search Filtering**: Filter search results by language
5. **Data Processing**: Classify text datasets by language
6. **Chatbots**: Detect user language for appropriate responses
7. **SEO Analysis**: Analyze language distribution of website content
8. **Document Processing**: Auto-tag documents by language

## Performance

- Fast detection: Most texts analyzed in <50ms
- Batch processing: 100 texts in <2 seconds
- Memory efficient: No large language models required
- Pure Python: Works without external dependencies

## Limitations

- Short texts (<10 chars) may have low confidence
- Very similar languages (e.g., Spanish/Portuguese) may be confused
- Language variants (Simplified/Traditional Chinese) approximated
- Mixed language confidence depends on character distribution

## License

MIT License - Part of AllToolkit collection.