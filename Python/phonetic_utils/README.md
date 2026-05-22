# Phonetic Algorithm Utilities

Phonetic algorithms encode words based on their pronunciation rather than spelling, enabling matching of similar-sounding names and words. Useful for deduplication, search, spelling correction, and genealogical research.

## Supported Algorithms

### Soundex
US Census standard encoding. Groups similar-sounding letters:
- Robert, Rupert → R163
- Smith, Schmidt → S530

### Metaphone
Improved Soundex using English pronunciation rules. More accurate for English names.

### Double Metaphone
Handles multiple possible pronunciations. Returns both primary and alternate codes.
- Catherine → K0RN / KTRN

### Caverphone
Designed for New Zealand electoral rolls. Handles Maori-influenced pronunciations.
- Returns 10-character codes.

### NYSIIS
New York State Identification and Intelligence System. Designed for law enforcement name matching.

### Match Rating Codex
Simplified encoding with built-in comparison algorithm.

### Refined Soundex
Extended version with separate codes for letter groups.

## Usage Examples

### Basic Encoding

```python
from phonetic_utils.mod import soundex

# Encode a name
result = soundex("Robert")
print(result.primary)  # 'R163'
```

### Multiple Algorithms

```python
from phonetic_utils.mod import encode_all

# Encode with all algorithms
results = encode_all("Smith")
for algo, result in results.items():
    print(f"{algo}: {result}")
```

### Phonetic Matching

```python
from phonetic_utils.mod import phonetic_match

# Check if two names match phonetically
matches, similarity = phonetic_match("Robert", "Rupert")
print(f"Match: {matches}, Similarity: {similarity}")
```

### Phonetic Search

```python
from phonetic_utils.mod import phonetic_search

candidates = ["Smith", "Smyth", "Schmidt", "John", "Johnson"]
results = phonetic_search("Smith", candidates)
for name, similarity in results:
    print(f"{name}: {similarity:.2f}")
```

### Grouping Names

```python
from phonetic_utils.mod import group_by_phonetic

names = ["Robert", "Rupert", "Smith", "Schmidt", "John"]
groups = group_by_phonetic(names)
for code, names in groups.items():
    print(f"{code}: {', '.join(names)}")
```

### Finding Duplicates

```python
from phonetic_utils.mod import find_duplicates

names = ["Robert", "Rupert", "Smith", "Schmidt"]
duplicates = find_duplicates(names)
for group in duplicates:
    print(f"Similar: {', '.join(group)}")
```

## Algorithm Comparison

| Algorithm | Code Length | Primary Use | Language |
|-----------|-------------|-------------|----------|
| Soundex | 4 chars | Census, genealogy | English |
| Metaphone | 4 chars | Search, dedup | English |
| Double Metaphone | Variable | Multi-origin names | English |
| Caverphone | 10 chars | Electoral rolls | English/NZ |
| NYSIIS | Variable | Law enforcement | English |
| Match Rating | Variable | Name matching | English |

## Common Use Cases

1. **Name deduplication**: Find duplicate entries with different spellings
2. **Search enhancement**: Match phonetically similar terms
3. **Genealogy research**: Link records with variant spellings
4. **Data cleansing**: Standardize name representations
5. **Spelling correction**: Suggest phonetically similar alternatives

## Implementation Notes

- Pure Python implementation with zero external dependencies
- All algorithms support Unicode input (ASCII normalization applied)
- Double Metaphone returns both primary and alternate encodings
- Comparison functions return similarity scores

## References

- [Soundex Wikipedia](https://en.wikipedia.org/wiki/Soundex)
- [Metaphone Algorithm](https://en.wikipedia.org/wiki/Metaphone)
- [Double Metaphone](https://en.wikipedia.org/wiki/Metaphone#Double_Metaphone)
- [NYSIIS Specification](https://en.wikipedia.org/wiki/New_York_State_Identification_and_Intelligence_System)