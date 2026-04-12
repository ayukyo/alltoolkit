"""
Text Utils - Text Analysis Examples

Demonstrates comprehensive text analysis capabilities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mod import TextUtils, TextCase, analyze, get_stats
import json

utils = TextUtils()

print("=" * 60)
print("TEXT ANALYSIS EXAMPLES")
print("=" * 60)

# -----------------------------------------------------------------------------
# Sample Texts
# -----------------------------------------------------------------------------
sample_texts = {
    "news": """
    Breaking News: Technology Company Announces Revolutionary Product.
    The innovative device combines artificial intelligence with sustainable design.
    Industry experts predict significant market impact. Stock prices surged following the announcement.
    """,
    
    "technical": """
    The algorithm implements a binary search tree with O(log n) complexity.
    Data structures include nodes, pointers, and recursive traversal methods.
    Memory management requires careful handling of references and garbage collection.
    """,
    
    "creative": """
    The moonlight danced across the shimmering lake, casting ethereal patterns on the water.
    Silent stars watched from above as the night unfolded its mysterious beauty.
    A gentle breeze whispered secrets through the ancient trees.
    """,
}

# -----------------------------------------------------------------------------
# 1. Comprehensive Analysis
# -----------------------------------------------------------------------------
print("\n1. COMPREHENSIVE TEXT ANALYSIS")
print("-" * 40)

for name, text in sample_texts.items():
    print(f"\n📄 {name.upper()} TEXT:")
    analysis = utils.analyze(text, top_n=5)
    
    print(f"  Words: {analysis.stats.word_count}")
    print(f"  Sentences: {analysis.stats.sentence_count}")
    print(f"  Unique words: {analysis.stats.unique_words}")
    print(f"  Readability: {analysis.stats.readability_score:.1f}/100")
    print(f"  Top keywords: {', '.join(analysis.keywords[:5])}")
    print(f"  Top word frequencies:")
    for word, count in list(analysis.word_frequencies.items())[:3]:
        print(f"    - {word}: {count}")

# -----------------------------------------------------------------------------
# 2. Keyword Density Analysis
# -----------------------------------------------------------------------------
print("\n2. KEYWORD DENSITY ANALYSIS")
print("-" * 40)

text = sample_texts["news"]
density = utils.keyword_density(text)

print(f"Text: {text.strip()[:80]}...")
print(f"\nKeyword Density (top 10):")
for keyword, percentage in density[:10]:
    bar = '█' * int(percentage * 2)
    print(f"  {keyword:15} {percentage:5.1f}% {bar}")

# -----------------------------------------------------------------------------
# 3. N-gram Analysis
# -----------------------------------------------------------------------------
print("\n3. N-GRAM ANALYSIS")
print("-" * 40)

text = sample_texts["technical"]
words = utils.extract_words(text)

for n in [1, 2, 3]:
    ngrams = utils.get_ngrams(words, n)
    print(f"\n{n}-grams (top 5):")
    for ngram in ngrams[:5]:
        print(f"  {' '.join(ngram)}")

# -----------------------------------------------------------------------------
# 4. Sentence Analysis
# -----------------------------------------------------------------------------
print("\n4. SENTENCE ANALYSIS")
print("-" * 40)

text = sample_texts["creative"]
sentences = utils.split_sentences(text)

print(f"Total sentences: {len(sentences)}\n")

for i, sentence in enumerate(sentences, 1):
    stats = utils.get_stats(sentence)
    print(f"Sentence {i}:")
    print(f"  Text: {sentence[:60]}...")
    print(f"  Words: {stats.word_count}, Avg word length: {stats.avg_word_length:.1f}")

# -----------------------------------------------------------------------------
# 5. Text Comparison
# -----------------------------------------------------------------------------
print("\n5. TEXT SIMILARITY COMPARISON")
print("-" * 40)

text1 = "The quick brown fox jumps over the lazy dog"
text2 = "A quick brown dog jumps over the lazy fox"
text3 = "Completely different content about something else"

print(f"Text 1: {text1}")
print(f"Text 2: {text2}")
print(f"Text 3: {text3}")

sim_12 = utils.similarity(text1, text2)
sim_13 = utils.similarity(text1, text3)
sim_23 = utils.similarity(text2, text3)

print(f"\nSimilarity scores:")
print(f"  Text 1 ↔ Text 2: {sim_12:.2%}")
print(f"  Text 1 ↔ Text 3: {sim_13:.2%}")
print(f"  Text 2 ↔ Text 3: {sim_23:.2%}")

# -----------------------------------------------------------------------------
# 6. Levenshtein Distance
# -----------------------------------------------------------------------------
print("\n6. LEVENSHTEIN DISTANCE (Edit Distance)")
print("-" * 40)

pairs = [
    ("kitten", "sitting"),
    ("hello", "hallo"),
    ("algorithm", "altruistic"),
    ("python", "jython"),
]

for s1, s2 in pairs:
    distance = utils.levenshtein_distance(s1, s2)
    print(f"  '{s1}' → '{s2}': {distance} edits")

# -----------------------------------------------------------------------------
# 7. Content Detection
# -----------------------------------------------------------------------------
print("\n7. CONTENT DETECTION")
print("-" * 40)

text = """
Visit https://example.com for more information.
Contact support@company.org for help.
<p>This is <b>HTML</b> content.</p>
"""

print(f"Text: {text.strip()}")
print(f"\nDetection results:")
print(f"  Contains URL: {utils.contains_any(text, ['https://', 'http://'])}")
print(f"  Contains email: {'@' in text}")
print(f"  Contains HTML: {'<' in text and '>' in text}")

# After cleaning:
cleaned = utils.remove_html(utils.remove_urls(utils.remove_emails(text)))
print(f"\nAfter cleaning: {cleaned.strip()}")

# -----------------------------------------------------------------------------
# 8. Readability Assessment
# -----------------------------------------------------------------------------
print("\n8. READABILITY ASSESSMENT")
print("-" * 40)

texts_by_level = {
    "Simple": "The cat sat. It was happy.",
    "Medium": "The quick brown fox jumps over the lazy dog repeatedly.",
    "Complex": "Notwithstanding the aforementioned complexities, the aforementioned phenomenon demonstrates significant correlation with previously established theoretical frameworks.",
}

def get_readability_level(score: float) -> str:
    if score >= 90:
        return "Very Easy (Elementary)"
    elif score >= 80:
        return "Easy (Middle School)"
    elif score >= 70:
        return "Fairly Easy (High School)"
    elif score >= 60:
        return "Standard (College)"
    elif score >= 50:
        return "Fairly Difficult (Graduate)"
    else:
        return "Difficult (Expert)"

for level, text in texts_by_level.items():
    stats = utils.get_stats(text)
    print(f"\n{level}:")
    print(f"  Text: {text}")
    print(f"  Score: {stats.readability_score:.1f}")
    print(f"  Level: {get_readability_level(stats.readability_score)}")

# -----------------------------------------------------------------------------
# 9. Export Analysis as JSON
# -----------------------------------------------------------------------------
print("\n9. EXPORT ANALYSIS AS JSON")
print("-" * 40)

text = sample_texts["news"]
analysis = utils.analyze(text, top_n=5)

json_output = analysis.to_dict()
print(json.dumps(json_output, indent=2, ensure_ascii=False)[:500] + "...")

print("\n" + "=" * 60)
print("Analysis examples completed!")
print("=" * 60)
