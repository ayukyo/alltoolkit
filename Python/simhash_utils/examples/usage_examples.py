#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - SimHash Utilities Examples
========================================
Practical examples demonstrating SimHash usage for various scenarios.

Run with: python usage_examples.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from simhash_utils.mod import (
    compute_simhash, compute_simhash_text,
    hamming_distance, similarity, are_similar,
    tokenize_words, tokenize_ngrams, tokenize_chinese,
    fingerprint_to_hex, fingerprint_to_binary,
    SimHashIndex,
    batch_compute_simhash, find_near_duplicates,
    compute_simhash_chinese, compare_documents,
    compute_distance_matrix
)


def example_basic_usage():
    """Example 1: Basic SimHash usage."""
    print("=" * 60)
    print("Example 1: Basic SimHash Usage")
    print("=" * 60)
    
    # Generate fingerprints for two texts
    text1 = "The quick brown fox jumps over the lazy dog"
    text2 = "The quick brown fox jumped over the lazy dog"
    
    fp1 = compute_simhash_text(text1)
    fp2 = compute_simhash_text(text2)
    
    print(f"Text 1: '{text1}'")
    print(f"Text 2: '{text2}'")
    print(f"\nFingerprint 1 (hex): {fingerprint_to_hex(fp1)}")
    print(f"Fingerprint 2 (hex): {fingerprint_to_hex(fp2)}")
    print(f"Fingerprint 1 (binary): {fingerprint_to_binary(fp1)[:32]}...")
    
    # Compare fingerprints
    dist = hamming_distance(fp1, fp2)
    sim = similarity(fp1, fp2)
    
    print(f"\nHamming distance: {dist} bits")
    print(f"Similarity: {sim:.2%}")
    print(f"Are similar (threshold=5): {are_similar(fp1, fp2, threshold=5)}")


def example_near_duplicate_detection():
    """Example 2: Near-duplicate document detection."""
    print("\n" + "=" * 60)
    print("Example 2: Near-Duplicate Document Detection")
    print("=" * 60)
    
    # Simulate a collection of documents
    documents = [
        "Python is a popular programming language created by Guido van Rossum",
        "Python is a well-known programming language developed by Guido van Rossum",
        "JavaScript is a scripting language commonly used in web browsers",
        "JavaScript is widely used for creating interactive web pages",
        "Machine learning uses algorithms to learn from data",
        "Machine learning applies algorithms to learn patterns from data",
        "The weather forecast predicts rain tomorrow",
        "Weather predictions suggest rain for tomorrow"
    ]
    
    # Compute fingerprints
    fingerprints = batch_compute_simhash(documents)
    
    # Find near-duplicates
    duplicates = find_near_duplicates(fingerprints, threshold=10)
    
    print(f"Total documents: {len(documents)}")
    print(f"Near-duplicate pairs found: {len(duplicates)}")
    print("\nDuplicate pairs:")
    
    for i, j, dist in duplicates:
        print(f"\n  Pair: documents[{i}] and documents[{j}]")
        print(f"    Distance: {dist} bits")
        print(f"    Similarity: {similarity(fingerprints[i], fingerprints[j]):.2%}")
        print(f"    Doc 1: '{documents[i][:50]}...'")
        print(f"    Doc 2: '{documents[j][:50]}...'")


def example_similarity_index():
    """Example 3: Building a similarity search index."""
    print("\n" + "=" * 60)
    print("Example 3: Similarity Search Index")
    print("=" * 60)
    
    # Create index
    index = SimHashIndex()
    
    # Add documents (simulating a document database)
    docs = {
        "web1": "Welcome to our Python programming tutorial",
        "web2": "Learn Python programming with our comprehensive guide",
        "web3": "JavaScript for beginners - complete tutorial",
        "web4": "Introduction to JavaScript programming",
        "web5": "Data science with Python and machine learning",
        "web6": "Python data science and ML fundamentals",
        "web7": "Cooking recipes for Italian cuisine",
        "web8": "Best Italian cooking recipes and tips"
    }
    
    print("Adding documents to index...")
    fps = index.add_batch(docs)
    print(f"Indexed {len(index)} documents")
    
    # Query for similar documents
    queries = [
        "Python programming guide",
        "JavaScript tutorial",
        "Data science tutorial",
        "Italian food recipes"
    ]
    
    print("\nSearching for similar documents...")
    for query in queries:
        print(f"\n  Query: '{query}'")
        results = index.query(query, threshold=15)
        
        if results:
            print("  Results:")
            for doc_id, dist, sim in results[:3]:  # Top 3
                print(f"    - {doc_id}: similarity={sim:.2%}, distance={dist}")
        else:
            print("  No similar documents found")
    
    # Find all duplicate groups
    print("\n\nDuplicate groups (threshold=10):")
    groups = index.get_duplicates(threshold=10)
    for group in groups:
        print(f"  Group: {group}")


def example_different_tokenizers():
    """Example 4: Using different tokenization strategies."""
    print("\n" + "=" * 60)
    print("Example 4: Different Tokenization Strategies")
    print("=" * 60)
    
    text = "The quick brown fox jumps over the lazy dog"
    
    tokenizers = ['word', 'char', 'ngram']
    ngram_sizes = [2, 3, 4]
    
    print(f"Text: '{text}'")
    print("\nFingerprints with different tokenizers:")
    
    for tokenizer in tokenizers:
        if tokenizer == 'ngram':
            for n in ngram_sizes:
                fp = compute_simhash_text(text, tokenizer='ngram', ngram_size=n)
                print(f"  ngram-{n}: {fingerprint_to_hex(fp)}")
        else:
            fp = compute_simhash_text(text, tokenizer=tokenizer)
            print(f"  {tokenizer}: {fingerprint_to_hex(fp)}")
    
    # Show that n-grams can be more robust to small changes
    print("\nRobustness test - comparing 'jumps' vs 'jumped':")
    text1 = "The quick brown fox jumps over the lazy dog"
    text2 = "The quick brown fox jumped over the lazy dog"
    
    for tokenizer in ['word', 'ngram']:
        fp1 = compute_simhash_text(text1, tokenizer=tokenizer, ngram_size=3)
        fp2 = compute_simhash_text(text2, tokenizer=tokenizer, ngram_size=3)
        dist = hamming_distance(fp1, fp2)
        sim = similarity(fp1, fp2)
        print(f"  {tokenizer}: distance={dist}, similarity={sim:.2%}")


def example_chinese_text():
    """Example 5: Processing Chinese text."""
    print("\n" + "=" * 60)
    print("Example 5: Chinese Text Processing")
    print("=" * 60)
    
    chinese_texts = [
        "今天天气很好，适合外出散步",
        "今天天气真好，适合外出散步",
        "明天天气预报说会下雨",
        "天气预报显示明天有雨",
        "机器学习是人工智能的重要分支",
        "人工智能包括机器学习技术"
    ]
    
    print("Computing fingerprints for Chinese texts:")
    
    # Compute fingerprints using Chinese n-gram tokenization
    fingerprints = [compute_simhash_chinese(t, ngram_size=2) for t in chinese_texts]
    
    for i, text in enumerate(chinese_texts):
        print(f"  [{i}] '{text}' -> {fingerprint_to_hex(fingerprints[i])}")
    
    # Find similar pairs
    print("\nSimilar pairs analysis:")
    for i in range(len(chinese_texts)):
        for j in range(i + 1, len(chinese_texts)):
            sim = similarity(fingerprints[i], fingerprints[j])
            if sim > 0.8:  # Only show highly similar
                print(f"  [{i}] vs [{j}]: similarity={sim:.2%}")
    
    # Distance matrix visualization
    print("\nDistance matrix (showing first 4 texts):")
    matrix = compute_distance_matrix(fingerprints[:4])
    
    print("     ", end="")
    for i in range(4):
        print(f"[{i}]  ", end="")
    print()
    
    for i, row in enumerate(matrix):
        print(f"[{i}] ", end="")
        for val in row:
            print(f"{val:3} ", end="")
        print()


def example_document_comparison():
    """Example 6: Comprehensive document comparison."""
    print("\n" + "=" * 60)
    print("Example 6: Document Comparison")
    print("=" * 60)
    
    comparisons = [
        ("Machine learning is a subset of AI", 
         "Machine learning is part of artificial intelligence"),
        ("Python is great for data science",
         "Python excels in data science applications"),
        ("The stock market crashed yesterday",
         "I love eating pizza on weekends"),
    ]
    
    for text1, text2 in comparisons:
        result = compare_documents(text1, text2)
        
        print(f"\nComparing:")
        print(f"  Text 1: '{text1}'")
        print(f"  Text 2: '{text2}'")
        print(f"\n  Results:")
        print(f"    Fingerprints: {result['fingerprint1_hex']} vs {result['fingerprint2_hex']}")
        print(f"    Hamming distance: {result['hamming_distance']} bits")
        print(f"    Similarity: {result['similarity']:.2%}")
        print(f"    Interpretation: {result['interpretation']}")
        print(f"    Near duplicate: {result['is_near_duplicate']}")


def example_practical_dedup():
    """Example 7: Practical web page deduplication."""
    print("\n" + "=" * 60)
    print("Example 7: Web Page Deduplication (Practical)")
    print("=" * 60)
    
    # Simulate crawled web pages
    pages = {
        "page1": """
            Python Programming Tutorial
            Welcome to our comprehensive Python tutorial.
            This guide covers basics, data types, functions, and more.
            Perfect for beginners and intermediate programmers.
        """.strip(),
        
        "page2": """
            Python Programming Guide
            Welcome to this Python programming tutorial.
            Our guide covers basics, types, functions and advanced topics.
            Great for beginners and intermediate developers.
        """.strip(),
        
        "page3": """
            JavaScript Tutorial
            Learn JavaScript programming from scratch.
            Covers DOM manipulation, events, and modern ES6 features.
            Suitable for web developers.
        """.strip(),
        
        "page4": """
            About Us
            We are a technology company focused on education.
            Our mission is to provide high-quality programming tutorials.
            Contact us for more information.
        """.strip(),
        
        "page5": """
            Python Programming Tutorial - Extended Edition
            Welcome to our comprehensive Python tutorial.
            This guide covers basics, data types, functions, and more.
            Perfect for beginners and intermediate programmers.
            Now includes bonus chapters on web development!
        """.strip()
    }
    
    # Build index
    index = SimHashIndex()
    index.add_batch(pages)
    
    print(f"Indexed {len(index)} web pages")
    
    # Find duplicate groups
    print("\nDuplicate detection (threshold=10):")
    duplicates = index.get_duplicates(threshold=10)
    
    if duplicates:
        for i, group in enumerate(duplicates):
            print(f"\n  Duplicate group {i + 1}:")
            for doc_id in group:
                fp = index.get_fingerprint(doc_id)
                print(f"    - {doc_id}: {fingerprint_to_hex(fp)}")
    else:
        print("  No duplicates found")
    
    # More detailed comparison of page1 and page2
    print("\nDetailed comparison of page1 vs page2:")
    result = compare_documents(pages["page1"], pages["page2"])
    print(f"  Similarity: {result['similarity']:.2%}")
    print(f"  Interpretation: {result['interpretation']}")


def example_code_similarity():
    """Example 8: Code similarity detection."""
    print("\n" + "=" * 60)
    print("Example 8: Code Similarity Detection")
    print("=" * 60)
    
    # Simulate code snippets
    code_snippets = {
        "code1": """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
        """.strip(),
        
        "code2": """
def calculate_sum(arr):
    result = 0
    for n in arr:
        result = result + n
    return result
        """.strip(),
        
        "code3": """
def calculate_average(numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)
        """.strip(),
        
        "code4": """
def greet_user(name):
    print(f"Hello, {name}!")
    return True
        """.strip()
    }
    
    # Compare code snippets
    print("Comparing code snippets:")
    
    fingerprints = batch_compute_simhash(list(code_snippets.values()))
    
    # Show similarity matrix
    print("\nSimilarity matrix:")
    ids = list(code_snippets.keys())
    
    print("        ", end="")
    for id in ids:
        print(f"{id:8}", end="")
    print()
    
    for i, id1 in enumerate(ids):
        print(f"{id1:8}", end="")
        for j, id2 in enumerate(ids):
            if i == j:
                print(f"  100%  ", end="")
            else:
                sim = similarity(fingerprints[i], fingerprints[j])
                print(f"  {sim:.0%}  ", end="")
        print()
    
    # Interpret results
    print("\nAnalysis:")
    print("  code1 vs code2: Very similar (both are sum functions)")
    print("  code1 vs code3: Different (sum vs average)")
    print("  code1 vs code4: Very different (math vs greeting)")


def main():
    """Run all examples."""
    examples = [
        example_basic_usage,
        example_near_duplicate_detection,
        example_similarity_index,
        example_different_tokenizers,
        example_chinese_text,
        example_document_comparison,
        example_practical_dedup,
        example_code_similarity
    ]
    
    for example in examples:
        example()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()