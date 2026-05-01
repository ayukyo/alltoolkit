# Fortune Utilities

A zero-dependency fortune cookie and inspirational quote generator for Python.

## Features

- **Multiple Categories**: Unix fortunes, inspirational quotes, programming quotes, wisdom quotes, humor, Chinese proverbs, riddles, and motivational quotes
- **Daily Fortune**: Get the same fortune for an entire day (deterministic)
- **Search**: Search for fortunes containing specific keywords
- **Custom Fortunes**: Add your own fortunes to the database
- **Multiple Formats**: Simple, quote, card, JSON, and full display formats
- **Unix Compatible**: Export/import in traditional fortune cookie file format
- **Zero Dependencies**: Uses only Python standard library

## Installation

```python
# Just import the module - no dependencies needed
from fortune_utils.mod import fortune, inspirational_quote, riddle
```

## Quick Usage

```python
# Get a random fortune
text = fortune()
print(text)

# Get fortune from specific category
text = fortune('programming')
print(text)

# Get inspirational quote
quote = inspirational_quote()
print(quote)

# Get a riddle with answer
question, answer = riddle()
print(f"Q: {question}")
print(f"A: {answer}")

# Get daily fortune (same all day)
result = daily_fortune()
print(result.fortune.text)
```

## Categories

| Category | Description | Count |
|----------|-------------|-------|
| `unix` | Classic Unix-style fortune cookies | 55 |
| `inspirational` | Inspirational quotes with authors | 30 |
| `programming` | Programming/developer quotes | 20 |
| `wisdom` | Philosophy and wisdom quotes | 20 |
| `humor` | Funny and humorous quotes | 20 |
| `chinese` | Chinese proverbs | 61 |
| `riddle` | Riddles with answers | 25 |
| `motivational` | Motivational success quotes | 20 |

## API Reference

### Convenience Functions

```python
fortune(category=None)               # Get random fortune text
fortune_result(category=None)        # Get FortuneResult with details
daily_fortune(category=None, seed=None)  # Get daily fortune
inspirational_quote()                # Random inspirational quote
programming_quote()                  # Random programming quote
wisdom_quote()                       # Random wisdom quote
humor_quote()                        # Random humor quote
chinese_proverb()                    # Random Chinese proverb
motivational_quote()                 # Random motivational quote
riddle()                             # Get (question, answer) tuple
riddle_question()                    # Get riddle question only
unix_fortune()                       # Classic Unix fortune
search_fortunes(query, category=None)  # Search for fortunes
categories()                         # List all categories
fortune_count(category=None)         # Count fortunes
```

### FortuneDatabase Class

```python
db = FortuneDatabase()

db.random(category=None)             # Get random FortuneResult
db.random_daily(category, seed)      # Get daily FortuneResult
db.get(index, category)              # Get specific fortune
db.search(query, category)           # Search fortunes
db.get_categories()                  # List categories
db.count(category)                   # Count fortunes
db.get_all(category)                 # Get all in category
db.add_fortune(fortune)              # Add custom fortune
db.get_riddle_answer(question)       # Get riddle answer
```

### FortuneGenerator Class

```python
gen = FortuneGenerator(seed=42)      # With reproducible seed

gen.random(category)                 # Get random fortune
gen.add_fortune(text, category, author, tags)
gen.add_fortunes_from_list(list, category)
gen.search(query)                    # Search fortunes
gen.count(category)                  # Count fortunes
```

### Formatting

```python
format_fortune(fortune, style)       # Format Fortune object
format_fortune_result(result, style) # Format FortuneResult

# Styles: 'simple', 'quote', 'card', 'json', 'full'
```

### Cookie Format

```python
to_cookie_format(fortunes, delimiter='%')  # Export to Unix format
from_cookie_format(content, delimiter='%') # Import from Unix format
```

## Examples

### Basic Usage

```python
from fortune_utils.mod import fortune, inspirational_quote, riddle

# Random fortune
print(fortune())

# Programming quote
print(fortune('programming'))

# Inspirational quote with formatting
result = fortune_result('inspirational')
print(f"\"{result.fortune.text}\"")
print(f"    — {result.fortune.author}")
```

### Daily Fortune

```python
from fortune_utils.mod import daily_fortune, format_fortune_result

# Same fortune for entire day
result = daily_fortune()
print(format_fortune_result(result, 'full'))
```

### Custom Fortune Database

```python
from fortune_utils.mod import FortuneGenerator

gen = FortuneGenerator()

# Add custom fortunes
gen.add_fortune(
    "My company motto",
    category="company",
    author="CEO",
    tags=["motto", "inspiration"]
)

gen.add_fortunes_from_list([
    "Teamwork makes the dream work",
    "Innovation starts here",
], category="company")

# Get random custom fortune
result = gen.random('company')
print(result.fortune.text)
```

### Search and Display

```python
from fortune_utils.mod import search_fortunes, format_fortune

# Search for "success"
results = search_fortunes("success")
for f in results[:5]:
    print(format_fortune(f, 'quote'))
    print()
```

### Export to Unix Fortune Format

```python
from fortune_utils.mod import to_cookie_format, fortune

# Generate multiple fortunes
fortunes = [fortune() for _ in range(10)]

# Export to Unix fortune file format
cookie_content = to_cookie_format(fortunes)
print(cookie_content)
```

## Data Classes

### Fortune

```python
Fortune(
    text: str,              # The fortune text
    category: str = "general",  # Category name
    author: Optional[str] = None,  # Author name (if applicable)
    source: Optional[str] = None,  # Source reference
    tags: List[str] = [],   # Tags for search/filtering
    difficulty: int = 1     # Difficulty rating (1-5)
)
```

### FortuneResult

```python
FortuneResult(
    fortune: Fortune,       # The Fortune object
    index: int,             # Index in category
    total_in_category: int, # Total fortunes in category
    timestamp: datetime     # When generated
)
```

## Author

AllToolkit

## License

MIT