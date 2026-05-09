# Phonetic Encoding Utilities

A comprehensive phonetic encoding utility module for Python with zero external dependencies.

## Features

### Algorithms

| Algorithm | Description | Best For |
|-----------|-------------|----------|
| **Soundex** | Classic American Soundex | Basic homophone matching |
| **Metaphone** | Improved pronunciation encoding | English names |
| **Double Metaphone** | Primary + alternate codes | Multi-origin names |
| **NYSIIS** | New York State system | Law enforcement records |
| **Caverphone** | New Zealand electoral | Australian/NZ names |
| **Match Rating Codex** | Ontario Police system | Criminal justice |

### Functions

```python
# Encoding functions
soundex("Smith")          # "S530"
metaphone("Smith")        # "SM0T"
double_metaphone("Smith") # DoubleMetaphoneResult(primary="SMT0", alternate="XMT0")
nysiis("Smith")           # "SNAT"
caverphone("Smith")       # "SMT1111111"
match_rating_codex("Smith") # "SMTH"

# Matching functions
soundex_match("Smith", "Schmidt")     # True
metaphone_match("Catherine", "Katherine") # True
double_metaphone_match("Smith", "Schmidt") # True

# Similarity
phonetic_similarity("Smith", "Schmidt") # 0.833...

# Batch operations
batch_encode(["Smith", "Schmidt"], PhoneticAlgorithm.SOUNDEX)
find_phonetic_matches("Smith", ["Smith", "Schmidt", "Jones"])
```

## Applications

- **Name deduplication** - Find duplicate entries with spelling variations
- **Search tolerance** - Enable fuzzy name search
- **Genealogy** - Match surname variations in historical records
- **Customer databases** - Merge contact lists without duplicates
- **Record linkage** - Connect records across databases

## Quick Start

```python
from phonetic_utils import soundex, metaphone, double_metaphone

# Basic encoding
print(soundex("Robert"))     # R163
print(soundex("Rupert"))     # R163 (same!)

# Double Metaphone for better accuracy
result = double_metaphone("Smith")
print(result.primary)        # SMT0
print(result.alternate)      # XMT0

# Find similar names
from phonetic_utils import find_phonetic_matches
matches = find_phonetic_matches("Smith", ["Smith", "Schmidt", "Smythe"])
for name, score in matches:
    print(f"{name}: {score:.1%}")
```

## Algorithm Comparison

| Name Pair | Soundex | Metaphone | Double Metaphone |
|-----------|---------|-----------|------------------|
| Smith/Schmidt | ✓ | ✗ | ✓ |
| Catherine/Katherine | ✗ | ✓ | ✓ |
| Brian/Bryan | ✓ | ✓ | ✓ |
| Gene/Jean | ✗ | ✓ | ✓ |

**Recommendation**: Use Double Metaphone for best overall accuracy.

## Testing

Run tests with:
```bash
python phonetic_utils_test.py
```

## License

MIT License - Part of AllToolkit