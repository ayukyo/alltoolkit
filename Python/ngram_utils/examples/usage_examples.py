"""
N-gram Utilities - Usage Examples

This file demonstrates various use cases for the N-gram utilities module.

N-grams are contiguous sequences of n items (characters, words, or tokens) from a given text.
They are fundamental building blocks for many NLP and text processing tasks.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ngram_utils.mod import (
    char_ngrams, word_ngrams, token_ngrams, ngram_frequencies,
    all_ngrams, jaccard_similarity, dice_similarity, cosine_similarity,
    ngram_profile, language_distance, build_language_profiles,
    detect_language, ngram_frequency_analysis, most_common_ngrams,
    build_ngram_model, predict_next, text_similarity, ngram_overlap,
    unique_ngrams, ngram_positions, sentence_ngrams, NGramAnalyzer,
    get_common_language_profiles, bigrams, trigrams, quadgrams
)


def example_basic_ngrams():
    """Basic N-gram generation examples."""
    print("=" * 60)
    print("Example 1: Basic N-gram Generation")
    print("=" * 60)
    
    text = "Hello World"
    
    # Character N-grams
    print(f"\nText: '{text}'")
    print(f"Character bigrams (n=2): {char_ngrams(text, 2)}")
    print(f"Character trigrams (n=3): {char_ngrams(text, 3)}")
    
    # Word N-grams
    sentence = "The quick brown fox jumps over the lazy dog"
    print(f"\nSentence: '{sentence}'")
    print(f"Word bigrams: {word_ngrams(sentence, 2)[:5]}...")
    print(f"Word trigrams: {word_ngrams(sentence, 3)[:3]}...")
    
    # Token N-grams (from pre-tokenized list)
    tokens = ['The', 'quick', 'brown', 'fox']
    print(f"\nTokens: {tokens}")
    print(f"Token bigrams: {token_ngrams(tokens, 2)}")
    
    # Using convenience functions
    print(f"\nUsing convenience functions:")
    print(f"bigrams('hello'): {bigrams('hello', mode='char')}")
    print(f"trigrams('hello'): {trigrams('hello', mode='char')}")


def example_frequency_analysis():
    """N-gram frequency analysis examples."""
    print("\n" + "=" * 60)
    print("Example 2: N-gram Frequency Analysis")
    print("=" * 60)
    
    text = "the cat sat on the mat the cat was fat"
    
    print(f"\nText: '{text}'")
    
    # Word frequency
    word_freq = ngram_frequencies(word_ngrams(text, 1))
    print(f"\nWord frequencies: {word_freq}")
    
    # Word bigram frequencies
    bigram_freq = ngram_frequencies(word_ngrams(text, 2))
    print(f"\nWord bigram frequencies: {bigram_freq}")
    
    # Normalized frequencies
    normalized = ngram_frequencies(word_ngrams(text, 1), normalize=True)
    print(f"\nNormalized word frequencies: {normalized}")
    print(f"Sum: {sum(normalized.values()):.2f}")
    
    # Most common N-grams
    print(f"\nMost common words: {most_common_ngrams(text, 1, 'word', 3)}")
    print(f"Most common word bigrams: {most_common_ngrams(text, 2, 'word', 3)}")
    
    # Comprehensive analysis
    print("\nComprehensive analysis (character N-grams 1-3):")
    analysis = ngram_frequency_analysis("mississippi", 1, 3, 'char', top_k=3)
    for n, freqs in analysis.items():
        print(f"  {n}-grams: {freqs}")


def example_text_similarity():
    """Text similarity examples using N-grams."""
    print("\n" + "=" * 60)
    print("Example 3: Text Similarity with N-grams")
    print("=" * 60)
    
    pairs = [
        ("hello world", "hello there"),
        ("the quick brown fox", "the quick brown dog"),
        ("completely different", "totally unrelated"),
        ("same text", "same text"),
    ]
    
    print("\nText Similarity Comparison (using character trigrams):\n")
    print(f"{'Text 1':<25} {'Text 2':<25} {'Jaccard':>8} {'Dice':>8} {'Cosine':>8}")
    print("-" * 75)
    
    for text1, text2 in pairs:
        jaccard = text_similarity(text1, text2, 3, 'jaccard')
        dice = text_similarity(text1, text2, 3, 'dice')
        cosine = text_similarity(text1, text2, 3, 'cosine')
        print(f"{text1:<25} {text2:<25} {jaccard:>8.3f} {dice:>8.3f} {cosine:>8.3f}")
    
    # N-gram overlap details
    print("\nDetailed N-gram overlap:")
    overlap = ngram_overlap("hello world", "hello there", 2, 'word')
    print(f"  Text 1: 'hello world'")
    print(f"  Text 2: 'hello there'")
    print(f"  Intersection: {overlap['intersection']}")
    print(f"  Intersection size: {overlap['intersection_size']}")
    print(f"  Union size: {overlap['union_size']}")
    print(f"  Jaccard similarity: {overlap['jaccard']:.3f}")


def example_language_detection():
    """Language detection using N-gram profiles."""
    print("\n" + "=" * 60)
    print("Example 4: Language Detection")
    print("=" * 60)
    
    # Get pre-built language profiles
    profiles = get_common_language_profiles(n=3, top_k=200)
    
    test_texts = [
        ("English", "This is a sample English text for testing language detection capabilities."),
        ("Spanish", "Este es un texto de muestra en español para probar la detección de idioma."),
        ("French", "Ceci est un exemple de texte en français pour tester la détection de langue."),
        ("German", "Dies ist ein Beispieltext auf Deutsch zum Testen der Spracherkennung."),
        ("Italian", "Questo è un testo di esempio in italiano per testare il rilevamento della lingua."),
        ("Portuguese", "Este é um texto de exemplo em português para testar a detecção de idioma."),
        ("Chinese", "这是一个中文示例文本用于语言检测测试。"),
        ("Japanese", "これは言語検出テスト用の日本語サンプルテキストです。"),
        ("Korean", "이것은 언어 감지 테스트를 위한 한국어 샘플 텍스트입니다."),
        ("Russian", "Это пример текста на русском языке для тестирования определения языка."),
    ]
    
    print("\nLanguage Detection Results:\n")
    print(f"{'Actual':<12} {'Detected':<12} {'Distance':>10}")
    print("-" * 35)
    
    for actual_lang, text in test_texts:
        detected, distance = detect_language(text, profiles, n=3, top_k=200)
        status = "✓" if detected == actual_lang.lower()[:2] or actual_lang.lower()[:2] in detected else "?"
        print(f"{actual_lang:<12} {detected:<12} {distance:>10} {status}")


def example_text_prediction():
    """Text prediction using N-gram models."""
    print("\n" + "=" * 60)
    print("Example 5: Text Prediction with N-gram Models")
    print("=" * 60)
    
    # Training corpus
    corpus = """
    the cat sat on the mat
    the cat was very happy
    the cat liked to sleep
    the dog ran in the park
    the dog was very friendly
    the dog liked to play
    the bird flew in the sky
    the bird was very small
    """
    
    # Build trigram model (context of 2 words to predict 3rd)
    model = build_ngram_model(corpus, n=3, mode='word')
    
    print("Training corpus: stories about cat, dog, and bird")
    print("\nPrediction results (trigram model):\n")
    
    contexts = [
        ['the', 'cat'],
        ['the', 'dog'],
        ['cat', 'was'],
        ['dog', 'was'],
        ['the', 'bird'],
    ]
    
    for context in contexts:
        predictions = predict_next(model, context, top_k=3)
        context_str = ' '.join(context)
        if predictions:
            preds_str = ', '.join(f"{word} ({prob:.2f})" for word, prob in predictions)
            print(f"  '{context_str} ...' -> {preds_str}")
        else:
            print(f"  '{context_str} ...' -> (no predictions)")


def example_analyzer_class():
    """Using the NGramAnalyzer class for comprehensive analysis."""
    print("\n" + "=" * 60)
    print("Example 6: NGramAnalyzer Class")
    print("=" * 60)
    
    text = "The quick brown fox jumps over the lazy dog. The dog was not amused."
    analyzer = NGramAnalyzer(text)
    
    print(f"\nAnalyzing: '{text}'")
    print(f"\n{analyzer}")
    
    # Character N-grams
    print(f"\nCharacter trigrams (first 10): {analyzer.char_ngrams(3)[:10]}")
    
    # Word N-grams
    print(f"\nWord bigrams: {analyzer.word_ngrams(2)}")
    
    # Most common
    print(f"\nMost common character bigrams: {analyzer.most_common(2, 'char', 5)}")
    print(f"Most common word unigrams: {analyzer.most_common(1, 'word', 5)}")
    
    # Unique N-grams
    print(f"\nUnique character bigrams: {len(analyzer.unique(2, 'char'))}")
    
    # Similarity
    similar_text = "The quick brown cat jumps over the lazy dog"
    similarity = analyzer.similarity_to(similar_text, n=3)
    print(f"\nSimilarity to '{similar_text[:40]}...': {similarity:.3f}")
    
    # Profile
    profile = analyzer.profile(n=3, top_k=10)
    print(f"\nTop 10 trigram profile: {list(profile.keys())}")


def example_sentence_ngrams():
    """Sentence-level N-grams."""
    print("\n" + "=" * 60)
    print("Example 7: Sentence N-grams")
    print("=" * 60)
    
    text = "First sentence. Second sentence here. Third one. Fourth and final."
    
    print(f"\nText: '{text}'")
    print(f"\nSentence bigrams:")
    for i, sg in enumerate(sentence_ngrams(text, 2), 1):
        print(f"  {i}. {sg}")


def example_unique_and_positions():
    """Finding unique N-grams and their positions."""
    print("\n" + "=" * 60)
    print("Example 8: Unique N-grams and Positions")
    print("=" * 60)
    
    text = "ababab"
    
    print(f"\nText: '{text}'")
    
    # Unique character bigrams
    unique = unique_ngrams(text, 2, 'char')
    print(f"Unique character bigrams: {unique}")
    
    # Positions of each N-gram
    positions = ngram_positions(text, 2, 'char')
    print(f"\nPositions of each bigram:")
    for ngram, pos in sorted(positions.items()):
        print(f"  '{ngram}': {pos}")


def example_plagiarism_detection():
    """Simple plagiarism detection using N-gram similarity."""
    print("\n" + "=" * 60)
    print("Example 9: Simple Plagiarism Detection")
    print("=" * 60)
    
    original = """
    The development of artificial intelligence has revolutionized many industries.
    Machine learning algorithms can now process vast amounts of data in real-time.
    Natural language processing enables computers to understand human language.
    """
    
    # Different versions
    versions = {
        "Original": original,
        "Slightly Modified": """
            AI development has changed many sectors significantly.
            Machine learning systems now handle huge data volumes instantly.
            NLP allows machines to comprehend human speech.
        """,
        "Plagiarized": """
            The development of artificial intelligence has revolutionized many industries.
            Machine learning algorithms can process large data amounts.
            Natural language processing helps computers understand language.
        """,
        "Original Work": """
            Quantum computing represents a paradigm shift in computational capability.
            Unlike classical computers, quantum machines leverage superposition.
            This technology promises breakthroughs in cryptography and simulation.
        """,
    }
    
    print("\nComparing documents to original using character trigrams:\n")
    print(f"{'Document':<20} {'Similarity':>10}")
    print("-" * 32)
    
    for name, text in versions.items():
        if name != "Original":
            similarity = text_similarity(original, text, 3, 'jaccard')
            print(f"{name:<20} {similarity:>10.3f}")


def example_spell_check_assistant():
    """Simple spell check assistance using N-gram similarity."""
    print("\n" + "=" * 60)
    print("Example 10: Spell Check Assistance")
    print("=" * 60)
    
    # Dictionary of words
    dictionary = [
        "hello", "help", "held", "helmet", "helper",
        "world", "word", "work", "worn", "worth",
        "computer", "compute", "commute", "compact",
        "programming", "program", "progress", "project",
    ]
    
    misspelled = ["helo", "wrld", "computr", "progam"]
    
    print("\nFinding similar words for potential misspellings:\n")
    
    for word in misspelled:
        # Calculate similarity with all dictionary words
        similarities = []
        for dict_word in dictionary:
            sim = text_similarity(word, dict_word, 2, 'jaccard')
            similarities.append((dict_word, sim))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        print(f"'{word}' -> suggestions:")
        for dict_word, sim in similarities[:3]:
            print(f"  {dict_word:<15} (similarity: {sim:.3f})")


def example_keyword_extraction():
    """Simple keyword extraction using N-gram frequencies."""
    print("\n" + "=" * 60)
    print("Example 10: Simple Keyword Extraction")
    print("=" * 60)
    
    document = """
    Machine learning is a subset of artificial intelligence.
    Machine learning algorithms learn from data and improve over time.
    Deep learning is a type of machine learning using neural networks.
    Neural networks are inspired by the human brain.
    Artificial intelligence and machine learning are transforming technology.
    """
    
    print(f"\nDocument: '{document[:100]}...'")
    
    # Get word frequencies
    words = word_ngrams(document.lower(), 1)
    freq = ngram_frequencies(words)
    
    # Remove common stop words (simplified)
    stop_words = {'a', 'an', 'the', 'is', 'are', 'of', 'and', 'to', 'from', 'by', 'in', 'for', 'over', 'with'}
    keywords = [(word, count) for word, count in freq.items() 
                if word not in stop_words and len(word) > 2]
    keywords.sort(key=lambda x: x[1], reverse=True)
    
    print("\nTop keywords (excluding stop words):")
    for word, count in keywords[:10]:
        print(f"  {word:<15} {count:>3}")


def main():
    """Run all examples."""
    example_basic_ngrams()
    example_frequency_analysis()
    example_text_similarity()
    example_language_detection()
    example_text_prediction()
    example_analyzer_class()
    example_sentence_ngrams()
    example_unique_and_positions()
    example_plagiarism_detection()
    example_spell_check_assistant()
    example_keyword_extraction()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()