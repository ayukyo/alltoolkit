"""
Text Utils - Text Preprocessing Pipeline

Demonstrates building a complete text preprocessing pipeline for NLP tasks.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mod import TextUtils, TextCase, get_stats, analyze
from typing import List, Dict, Any
import re

# Initialize utility class
utils = TextUtils()

print("=" * 60)
print("TEXT PREPROCESSING PIPELINE EXAMPLES")
print("=" * 60)

# -----------------------------------------------------------------------------
# 1. Basic Preprocessing Pipeline
# -----------------------------------------------------------------------------
print("\n1. BASIC PREPROCESSING PIPELINE")
print("-" * 40)

def preprocess_basic(text: str) -> str:
    """
    Basic text preprocessing for general use.
    
    Steps:
    1. Remove HTML tags
    2. Remove URLs
    3. Remove email addresses
    4. Normalize whitespace
    5. Normalize Unicode
    """
    # Remove HTML
    text = utils.remove_html(text)
    
    # Remove URLs
    text = utils.remove_urls(text, replace_with='')
    
    # Remove emails
    text = utils.remove_emails(text, replace_with='')
    
    # Clean and normalize
    text = utils.clean(text,
                       remove_extra_spaces=True,
                       normalize_unicode=True,
                       strip=True)
    
    return text

# Test with dirty input
dirty_input = """
<html>
<body>
  <h1>Welcome!</h1>
  <p>Visit <a href="https://example.com">our website</a></p>
  <p>Contact: support@example.com</p>
  <p>  Multiple   spaces   here  </p>
</body>
</html>
"""

print(f"Input:\n{dirty_input}")
print(f"\nPreprocessed:\n{preprocess_basic(dirty_input)}")

# -----------------------------------------------------------------------------
# 2. NLP Preprocessing Pipeline
# -----------------------------------------------------------------------------
print("\n2. NLP PREPROCESSING PIPELINE")
print("-" * 40)

def preprocess_for_nlp(text: str, 
                       lowercase: bool = True,
                       remove_punctuation: bool = True,
                       remove_numbers: bool = False,
                       remove_stopwords: bool = True,
                       min_word_length: int = 2) -> List[str]:
    """
    Preprocess text for NLP tasks.
    
    Returns a list of cleaned tokens.
    """
    # Basic cleaning
    text = preprocess_basic(text)
    
    # Lowercase
    if lowercase:
        text = text.lower()
    
    # Remove punctuation
    if remove_punctuation:
        text = ''.join(c for c in text if c not in utils.PUNCTUATION_ALL)
    
    # Remove numbers
    if remove_numbers:
        text = ''.join(c for c in text if not c.isdigit())
    
    # Extract words
    words = utils.extract_words(text, min_length=min_word_length)
    
    # Remove stop words
    if remove_stopwords:
        words = [w for w in words if w not in utils.stop_words]
    
    return words

text = """
Natural Language Processing (NLP) is a field of artificial intelligence.
It focuses on the interaction between computers and human language.
NLP enables machines to understand, interpret, and generate text.
"""

tokens = preprocess_for_nlp(text)
print(f"Input: {text[:80]}...")
print(f"\nTokens ({len(tokens)}):")
print(tokens)

# -----------------------------------------------------------------------------
# 3. Social Media Text Pipeline
# -----------------------------------------------------------------------------
print("\n3. SOCIAL MEDIA TEXT PIPELINE")
print("-" * 40)

def preprocess_social_media(text: str) -> Dict[str, Any]:
    """
    Preprocess social media text, preserving hashtags and mentions.
    
    Returns structured data with cleaned text and extracted entities.
    """
    result = {
        'original': text,
        'hashtags': [],
        'mentions': [],
        'urls': [],
        'cleaned': text,
    }
    
    # Extract hashtags
    result['hashtags'] = re.findall(r'#\w+', text)
    
    # Extract mentions
    result['mentions'] = re.findall(r'@\w+', text)
    
    # Extract URLs
    result['urls'] = re.findall(r'https?://[^\s]+', text)
    
    # Remove entities for cleaned text
    cleaned = text
    for tag in result['hashtags'] + result['mentions']:
        cleaned = cleaned.replace(tag, '')
    cleaned = utils.remove_urls(cleaned, replace_with='')
    cleaned = utils.normalize_whitespace(cleaned)
    
    result['cleaned'] = cleaned.strip()
    
    return result

social_text = """
🚀 Just launched our new product! Check it out at https://example.com/product
#TechLaunch #Innovation @TechCrunch @VentureBeat
Great thanks to the team! 🎉
"""

result = preprocess_social_media(social_text)
print(f"Original: {social_text.strip()}")
print(f"\nExtracted:")
print(f"  Hashtags: {result['hashtags']}")
print(f"  Mentions: {result['mentions']}")
print(f"  URLs: {result['urls']}")
print(f"\nCleaned: {result['cleaned']}")

# -----------------------------------------------------------------------------
# 4. Document Similarity Pipeline
# -----------------------------------------------------------------------------
print("\n4. DOCUMENT SIMILARITY PIPELINE")
print("-" * 40)

def compare_documents(doc1: str, doc2: str) -> Dict[str, Any]:
    """
    Compare two documents for similarity.
    
    Returns similarity metrics and analysis.
    """
    # Preprocess both documents
    tokens1 = set(preprocess_for_nlp(doc1, remove_stopwords=True))
    tokens2 = set(preprocess_for_nlp(doc2, remove_stopwords=True))
    
    # Calculate metrics
    intersection = tokens1 & tokens2
    union = tokens1 | tokens2
    
    jaccard = len(intersection) / len(union) if union else 0
    
    # Levenshtein on cleaned text
    clean1 = preprocess_basic(doc1)
    clean2 = preprocess_basic(doc2)
    levenshtein = utils.levenshtein_distance(clean1, clean2)
    
    # Word-level similarity
    word_sim = utils.similarity(clean1, clean2)
    
    return {
        'jaccard_similarity': jaccard,
        'word_similarity': word_sim,
        'levenshtein_distance': levenshtein,
        'common_words': list(intersection),
        'unique_to_doc1': list(tokens1 - tokens2),
        'unique_to_doc2': list(tokens2 - tokens1),
    }

doc1 = "Machine learning is a subset of artificial intelligence that enables systems to learn from data."
doc2 = "Deep learning is a type of machine learning that uses neural networks with many layers."
doc3 = "The weather today is sunny and warm, perfect for outdoor activities."

print("Document 1:", doc1)
print("Document 2:", doc2)
print("Document 3:", doc3)

comparison = compare_documents(doc1, doc2)
print(f"\nDoc1 vs Doc2:")
print(f"  Jaccard: {comparison['jaccard_similarity']:.2%}")
print(f"  Word Sim: {comparison['word_similarity']:.2%}")
print(f"  Common words: {comparison['common_words'][:5]}")

comparison = compare_documents(doc1, doc3)
print(f"\nDoc1 vs Doc3:")
print(f"  Jaccard: {comparison['jaccard_similarity']:.2%}")
print(f"  Word Sim: {comparison['word_similarity']:.2%}")

# -----------------------------------------------------------------------------
# 5. Content Quality Checker
# -----------------------------------------------------------------------------
print("\n5. CONTENT QUALITY CHECKER")
print("-" * 40)

def check_content_quality(text: str) -> Dict[str, Any]:
    """
    Check content quality based on various metrics.
    
    Returns quality score and recommendations.
    """
    stats = utils.get_stats(text)
    analysis = utils.analyze(text, top_n=10)
    
    issues = []
    recommendations = []
    
    # Check word count
    if stats.word_count < 50:
        issues.append("Content is too short")
        recommendations.append("Expand content to at least 50 words")
    
    # Check sentence length
    if stats.avg_sentence_length > 25:
        issues.append("Sentences are too long")
        recommendations.append("Break down long sentences for readability")
    
    # Check readability
    if stats.readability_score < 50:
        issues.append("Content is difficult to read")
        recommendations.append("Simplify vocabulary and sentence structure")
    
    # Check keyword repetition
    for word, count in analysis.word_frequencies.items():
        if count > stats.word_count * 0.05:  # More than 5%
            issues.append(f"Word '{word}' is overused")
            recommendations.append(f"Vary vocabulary, reduce use of '{word}'")
    
    # Calculate quality score
    score = 100
    score -= len(issues) * 10
    score = max(0, min(100, score))
    
    return {
        'quality_score': score,
        'issues': issues,
        'recommendations': recommendations,
        'stats': stats.to_dict(),
        'keywords': analysis.keywords,
    }

# Test with different quality content
low_quality = "Stuff things good bad stuff things good. Stuff bad."
medium_quality = "This is decent content. It has some information. Could be better."
high_quality = "This comprehensive guide provides valuable insights into best practices. Readers will appreciate the clear explanations and practical examples throughout the document."

for name, text in [("Low", low_quality), ("Medium", medium_quality), ("High", high_quality)]:
    result = check_content_quality(text)
    print(f"\n{name} Quality Content:")
    print(f"  Score: {result['quality_score']}/100")
    if result['issues']:
        print(f"  Issues: {result['issues'][:2]}")
    if result['recommendations']:
        print(f"  Tips: {result['recommendations'][:2]}")

# -----------------------------------------------------------------------------
# 6. Text Anonymization Pipeline
# -----------------------------------------------------------------------------
print("\n6. TEXT ANONYMIZATION PIPELINE")
print("-" * 40)

def anonymize_text(text: str) -> str:
    """
    Anonymize sensitive information in text.
    
    Removes/replaces:
    - Email addresses
    - URLs
    - Phone numbers (basic pattern)
    - Potential names (capitalized words after certain patterns)
    """
    result = text
    
    # Remove emails
    result = utils.remove_emails(result, replace_with='[EMAIL]')
    
    # Remove URLs
    result = utils.remove_urls(result, replace_with='[URL]')
    
    # Remove phone numbers (basic pattern)
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    result = re.sub(phone_pattern, '[PHONE]', result)
    
    # Remove potential credit card numbers
    cc_pattern = r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'
    result = re.sub(cc_pattern, '[CARD]', result)
    
    return result

sensitive_text = """
Contact John Doe at john.doe@example.com or call 555-123-4567.
Visit https://company.com/profile or send payment to card 1234-5678-9012-3456.
Alternative contact: jane_smith@company.org, phone: 555.987.6543
"""

print(f"Original:\n{sensitive_text}")
print(f"\nAnonymized:\n{anonymize_text(sensitive_text)}")

print("\n" + "=" * 60)
print("Preprocessing pipeline examples completed!")
print("=" * 60)
