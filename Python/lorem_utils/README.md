# Lorem Ipsum Generator

A zero-dependency Lorem Ipsum text generator for creating placeholder content.

## Features

- Generate words, sentences, and paragraphs
- Generate titles and headlines
- HTML output support
- List generation (ordered/unordered)
- Fake data generation (names, emails, URLs, addresses, etc.)
- Reproducible output with seeds
- Extended word pool option
- No external dependencies

## Installation

No installation required. Simply copy the `lorem_utils.py` file to your project.

## Quick Start

```python
from lorem_utils import words, sentence, paragraph, paragraphs

# Generate words
print(words(10))  # "Lorem ipsum dolor sit amet consectetur adipiscing elit..."

# Generate a sentence
print(sentence())

# Generate a paragraph
print(paragraph())

# Generate multiple paragraphs
print(paragraphs(3))
```

## API Reference

### Convenience Functions

```python
# Words
words(count=5, as_list=False, capitalize_first=True, seed=None)

# Sentences
sentence(min_words=8, max_words=15, seed=None)
sentences(count=3, min_words=8, max_words=15, as_list=False, seed=None)

# Paragraphs
paragraph(min_sentences=4, max_sentences=7, min_words=8, max_words=15, seed=None)
paragraphs(count=2, min_sentences=4, max_sentences=7, min_words=8, max_words=15, 
           as_list=False, separator='\n\n', seed=None)

# Titles
title(min_words=3, max_words=6, seed=None)
headline(min_words=4, max_words=8, seed=None)

# HTML
html_paragraphs(count=2, min_sentences=4, max_sentences=7, wrap_tag='p', seed=None)

# Lists
list_items(count=5, min_words=3, max_words=8, ordered=False, seed=None)

# Fake Data
buzzword(seed=None)
buzzwords(count=5, seed=None)
email(domain='example.com', seed=None)
username(seed=None)
url(domain='example.com', seed=None)
phone(seed=None)
address(seed=None)
name(seed=None)
company(seed=None)

# Generic generator
generate(content_type, count=1, seed=None, **kwargs)
```

### LoremGenerator Class

```python
from lorem_utils import LoremGenerator

# Create generator with seed for reproducibility
gen = LoremGenerator(seed=42)

# Use extended word pool for more variety
gen = LoremGenerator(seed=42, use_extended=True)

# Available methods
gen.words(count, as_list=False, capitalize_first=True)
gen.sentence(min_words=8, max_words=15)
gen.sentences(count, min_words=8, max_words=15, as_list=False)
gen.paragraph(min_sentences=4, max_sentences=7, min_words=8, max_words=15)
gen.paragraphs(count, min_sentences=4, max_sentences=7, min_words=8, max_words=15, 
               as_list=False, separator='\n\n')
gen.title(min_words=3, max_words=6)
gen.headline(min_words=4, max_words=8)
gen.html_paragraphs(count, min_sentences=4, max_sentences=7, wrap_tag='p')
gen.list_items(count, min_words=3, max_words=8, ordered=False)
gen.buzzword()
gen.buzzwords(count=5)
gen.email(domain='example.com')
gen.username()
gen.url(domain='example.com')
gen.phone()
gen.address()
gen.name()
gen.company()
gen.reset_seed(seed=None)
```

## Examples

### Basic Usage

```python
from lorem_utils import words, sentence, paragraph, paragraphs

# Generate 10 words
print(words(10))

# Generate a sentence (8-15 words by default)
print(sentence())

# Generate a paragraph (4-7 sentences by default)
print(paragraph())

# Generate 3 paragraphs
print(paragraphs(3))
```

### Reproducible Output

```python
from lorem_utils import LoremGenerator

# Same seed = same output
gen1 = LoremGenerator(seed=42)
gen2 = LoremGenerator(seed=42)

print(gen1.paragraph() == gen2.paragraph())  # True
```

### Fake Data Generation

```python
from lorem_utils import LoremGenerator

gen = LoremGenerator(seed=123)

# Personal info
print(gen.name())       # "Lorem Ipsum"
print(gen.email())      # "lorem123@example.com"
print(gen.phone())      # "(123) 456-7890"
print(gen.address())    # "123 Dolor St, IpsumCity, IC 12345"

# Company info
print(gen.company())    # "Lorem Ipsum Inc"
print(gen.url())        # "https://example.com/lorem/ipsum"
```

### HTML Output

```python
from lorem_utils import html_paragraphs

# Generate HTML paragraphs
html = html_paragraphs(3, wrap_tag='p')
print(html)
# <p>Lorem ipsum dolor sit amet...</p>
# <p>Consectetur adipiscing elit...</p>
# <p>Sed do eiusmod tempor...</p>
```

### Lists

```python
from lorem_utils import list_items

# Unordered list
print(list_items(5, ordered=False))

# Ordered list
print(list_items(5, ordered=True))
```

### Extended Word Pool

```python
from lorem_utils import LoremGenerator

# Use extended word pool for more variety
gen = LoremGenerator(use_extended=True)
print(gen.paragraph())
```

### Generic Generate Function

```python
from lorem_utils import generate

# Generate any type
print(generate('words', 5, seed=42))
print(generate('sentence', seed=42))
print(generate('paragraphs', 2, seed=42))
print(generate('email', domain='test.com'))
print(generate('name'))
```

## Use Cases

- **Mock Data**: Generate realistic test data for development
- **Placeholder Content**: Fill UI templates with sample text
- **Documentation**: Create example content in documentation
- **Testing**: Generate various text lengths for testing
- **UI Mockups**: Populate design prototypes with content

## Running Tests

```bash
# Run with pytest
python -m pytest lorem_utils_test.py -v

# Run directly
python lorem_utils_test.py
```

## Running Examples

```bash
python examples.py
```

## License

MIT License - Part of the AllToolkit project.