"""
Text Utils - Basic Usage Examples

Demonstrates common text processing operations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mod import TextUtils, TextCase, get_stats, clean, analyze

# Initialize utility class
utils = TextUtils()

print("=" * 60)
print("TEXT UTILS - BASIC USAGE EXAMPLES")
print("=" * 60)

# -----------------------------------------------------------------------------
# 1. Text Cleaning
# -----------------------------------------------------------------------------
print("\n1. TEXT CLEANING")
print("-" * 40)

dirty_text = """
  <p>Hello   World!</p>  
Visit https://example.com for more info.
Contact: test@example.com
"""

print(f"Original:\n{repr(dirty_text)}")

cleaned = utils.clean(dirty_text, 
                      remove_extra_spaces=True,
                      normalize_unicode=True)
print(f"\nCleaned (extra spaces):\n{repr(cleaned)}")

no_html = utils.remove_html(dirty_text)
print(f"\nNo HTML:\n{repr(no_html)}")

no_urls = utils.remove_urls(dirty_text)
print(f"\nNo URLs:\n{repr(no_urls)}")

no_emails = utils.remove_emails(dirty_text)
print(f"\nNo Emails:\n{repr(no_emails)}")

# -----------------------------------------------------------------------------
# 2. Case Conversion
# -----------------------------------------------------------------------------
print("\n2. CASE CONVERSION")
print("-" * 40)

text = "hello world"

print(f"Original: {text}")
print(f"UPPER:    {utils.to_case(text, TextCase.UPPER)}")
print(f"lower:    {utils.to_case(text, TextCase.LOWER)}")
print(f"Title:    {utils.to_case(text, TextCase.TITLE)}")
print(f"Sentence: {utils.to_case(text, TextCase.SENTENCE)}")
print(f"camelCase: {utils.to_case(text, TextCase.CAMEL)}")
print(f"PascalCase: {utils.to_case(text, TextCase.PASCAL)}")
print(f"snake_case: {utils.to_case(text, TextCase.SNAKE)}")
print(f"kebab-case: {utils.to_case(text, TextCase.KEBAB)}")
print(f"CONSTANT_CASE: {utils.to_case(text, TextCase.CONSTANT)}")

# -----------------------------------------------------------------------------
# 3. Text Statistics
# -----------------------------------------------------------------------------
print("\n3. TEXT STATISTICS")
print("-" * 40)

sample = """
The quick brown fox jumps over the lazy dog. 
This pangram contains every letter of the alphabet at least once.
It's commonly used for typing practice and font demonstrations.
"""

stats = utils.get_stats(sample)

print(f"Text: {repr(sample[:50])}...")
print(f"\nStatistics:")
print(f"  Characters:        {stats.char_count}")
print(f"  Characters (no space): {stats.char_count_no_spaces}")
print(f"  Words:             {stats.word_count}")
print(f"  Sentences:         {stats.sentence_count}")
print(f"  Paragraphs:        {stats.paragraph_count}")
print(f"  Lines:             {stats.line_count}")
print(f"  Avg word length:   {stats.avg_word_length:.2f}")
print(f"  Avg sentence length: {stats.avg_sentence_length:.2f}")
print(f"  Unique words:      {stats.unique_words}")
print(f"  Readability score: {stats.readability_score:.1f}")

# -----------------------------------------------------------------------------
# 4. Text Transformation
# -----------------------------------------------------------------------------
print("\n4. TEXT TRANSFORMATION")
print("-" * 40)

text = "hello world"

print(f"Original: {text}")
print(f"Reverse (chars):  {utils.reverse(text)}")
print(f"Reverse (words):  {utils.reverse('hello world test', preserve_words=True)}")
print(f"Rotate (2):       {utils.rotate(text, 2)}")
print(f"Alternate case:   {utils.alternate_case(text)}")
print(f"Mirror:           {utils.mirror(text)}")
print(f"Truncate (8):     {utils.truncate('hello world', 8)}")
print(f"Abbreviate:       {utils.abbreviate('Portable Network Graphics')}")

# -----------------------------------------------------------------------------
# 5. Padding and Wrapping
# -----------------------------------------------------------------------------
print("\n5. PADDING AND WRAPPING")
print("-" * 40)

text = "test"
print(f"Original: '{text}'")
print(f"Pad left (10):   '{utils.pad(text, 10, side='left')}'")
print(f"Pad right (10):  '{utils.pad(text, 10, side='right')}'")
print(f"Pad center (10): '{utils.pad(text, 10, side='center')}'")

long_text = "This is a long sentence that should be wrapped to multiple lines."
wrapped = utils.wrap(long_text, width=20)
print(f"\nWrapped text (width=20):")
for i, line in enumerate(wrapped, 1):
    print(f"  Line {i}: '{line}'")

# -----------------------------------------------------------------------------
# 6. Module-level Functions
# -----------------------------------------------------------------------------
print("\n6. MODULE-LEVEL FUNCTIONS")
print("-" * 40)

text = "<p>Hello World!</p>"
print(f"remove_html: {clean(text)}")

text = "Hello world. Test sentence."
stats = get_stats(text)
print(f"get_stats: {stats.word_count} words, {stats.sentence_count} sentences")

text = "The quick brown fox"
analysis = analyze(text, top_n=3)
print(f"analyze: keywords = {analysis.keywords}")

print("\n" + "=" * 60)
print("Examples completed!")
print("=" * 60)
