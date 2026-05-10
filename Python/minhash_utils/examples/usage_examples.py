"""
MinHash Utilities - Usage Examples

This module demonstrates how to use MinHash for efficient similarity estimation.
"""

import sys
import os

# Add module directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    MinHash, MinHashSignature, MinHashLSH, MinHashMap,
    estimate_jaccard_similarity, exact_jaccard_similarity,
    text_similarity, create_minhash_from_set, create_minhash_from_text,
    similarity_error_bounds, recommended_num_hash
)


def example_basic_similarity():
    """Example 1: Basic set similarity estimation."""
    print("=" * 60)
    print("Example 1: Basic Set Similarity Estimation")
    print("=" * 60)
    
    # Create a MinHash generator
    mh = MinHash(num_hash=128, seed=42)
    
    # Two sets to compare
    set1 = {'apple', 'banana', 'cherry', 'date', 'elderberry'}
    set2 = {'apple', 'banana', 'cherry', 'fig', 'grape'}
    set3 = {'hello', 'world', 'python', 'code'}
    
    # Compute signatures
    sig1 = mh.compute_signature(set1)
    sig2 = mh.compute_signature(set2)
    sig3 = mh.compute_signature(set3)
    
    # Compare similarities
    sim_1_2 = sig1.jaccard_similarity(sig2)
    sim_1_3 = sig1.jaccard_similarity(sig3)
    
    print(f"Set 1: {set1}")
    print(f"Set 2: {set2}")
    print(f"Set 3: {set3}")
    print()
    print(f"Similarity(Set 1, Set 2): {sim_1_2:.4f} (exact: {exact_jaccard_similarity(set1, set2):.4f})")
    print(f"Similarity(Set 1, Set 3): {sim_1_3:.4f} (exact: {exact_jaccard_similarity(set1, set3):.4f})")
    print()


def example_text_similarity():
    """Example 2: Text similarity using character shingles."""
    print("=" * 60)
    print("Example 2: Text Similarity (Document Comparison)")
    print("=" * 60)
    
    texts = [
        ("doc1", "The quick brown fox jumps over the lazy dog"),
        ("doc2", "The quick brown fox jumps over the lazy cat"),
        ("doc3", "Python is a popular programming language"),
        ("doc4", "The lazy dog sleeps all day long"),
    ]
    
    mh = MinHash(num_hash=256, seed=42)
    
    # Compute signatures for all texts
    signatures = {}
    for name, text in texts:
        sig = mh.compute_signature_from_text(text, ngram_size=3)
        signatures[name] = sig
        print(f"{name}: \"{text[:40]}...\"")
    
    print("\nSimilarity Matrix:")
    print("-" * 50)
    
    names = list(signatures.keys())
    print(f"{'':>8}", end="")
    for name in names:
        print(f"{name:>8}", end="")
    print()
    
    for name1 in names:
        print(f"{name1:>8}", end="")
        for name2 in names:
            sim = signatures[name1].jaccard_similarity(signatures[name2])
            print(f"{sim:>8.3f}", end="")
        print()
    print()


def example_plagiarism_detection():
    """Example 3: Plagiarism detection scenario."""
    print("=" * 60)
    print("Example 3: Plagiarism Detection")
    print("=" * 60)
    
    # Original document
    original = """
    Machine learning is a subset of artificial intelligence that enables
    systems to learn and improve from experience without being explicitly
    programmed. It focuses on developing computer programs that can access
    data and use it to learn for themselves.
    """
    
    # Slightly modified (plagiarized)
    plagiarized = """
    Machine learning is a subfield of AI that allows systems to learn
    and improve from experience without explicit programming. It focuses
    on creating computer programs that can access data and learn for themselves.
    """
    
    # Different topic
    different = """
    The stock market experienced significant volatility today as investors
    reacted to the Federal Reserve's decision to raise interest rates.
    Technology stocks were particularly affected.
    """
    
    mh = MinHash(num_hash=256, seed=42)
    
    sig_orig = mh.compute_signature_from_text(original, ngram_size=4, word_level=False)
    sig_plag = mh.compute_signature_from_text(plagiarized, ngram_size=4, word_level=False)
    sig_diff = mh.compute_signature_from_text(different, ngram_size=4, word_level=False)
    
    sim_orig_plag = sig_orig.jaccard_similarity(sig_plag)
    sim_orig_diff = sig_orig.jaccard_similarity(sig_diff)
    
    print("Original Document:")
    print(f"  {original[:60]}...")
    print()
    print("Potentially Plagiarized:")
    print(f"  {plagiarized[:60]}...")
    print()
    print("Different Topic:")
    print(f"  {different[:60]}...")
    print()
    print(f"Original vs Plagiarized Similarity: {sim_orig_plag:.2%}")
    print(f"Original vs Different Similarity:   {sim_orig_diff:.2%}")
    print()
    
    if sim_orig_plag > 0.5:
        print("⚠️  HIGH SIMILARITY DETECTED - Potential plagiarism!")
    print()


def example_lsh_index():
    """Example 4: LSH index for finding similar documents efficiently."""
    print("=" * 60)
    print("Example 4: LSH Index for Efficient Similarity Search")
    print("=" * 60)
    
    # Sample documents
    documents = {
        'doc1': "machine learning algorithms neural networks deep learning",
        'doc2': "machine learning algorithms decision trees random forest",
        'doc3': "web development javascript html css frameworks",
        'doc4': "database systems sql nosql data modeling",
        'doc5': "deep learning neural networks backpropagation training",
        'doc6': "javascript frameworks react angular vue components",
    }
    
    # Create MinHash generator with matching parameters
    num_hash = 128
    mh = MinHash(num_hash=num_hash, seed=42)
    
    # Create LSH index
    # num_bands * rows_per_band should equal num_hash
    lsh = MinHashLSH(num_hash=num_hash, num_bands=32, rows_per_band=4)
    
    # Insert all documents
    for doc_id, text in documents.items():
        sig = mh.compute_signature_from_text(text, ngram_size=3, word_level=True)
        lsh.insert(doc_id, sig)
        print(f"Inserted: {doc_id}")
    
    print(f"\nLSH Index Statistics:")
    stats = lsh.stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Query for similar documents
    print("\nQuery: 'machine learning neural networks'")
    query_sig = mh.compute_signature_from_text(
        "machine learning neural networks", ngram_size=3, word_level=True
    )
    candidates = lsh.query(query_sig)
    
    print(f"Candidates found: {candidates}")
    
    # Calculate actual similarities for candidates
    print("\nActual similarities:")
    for doc_id in candidates:
        doc_sig = lsh.get_signature(doc_id)
        sim = query_sig.jaccard_similarity(doc_sig)
        print(f"  {doc_id}: {sim:.4f} - \"{documents[doc_id][:40]}...\"")
    print()


def example_minhash_map():
    """Example 5: Using MinHashMap for collection management."""
    print("=" * 60)
    print("Example 5: MinHashMap for Document Collection")
    print("=" * 60)
    
    # Create a MinHashMap collection
    collection = MinHashMap(num_hash=128, seed=42)
    
    # Add documents
    collection.add_text('intro', "Introduction to Python programming language basics")
    collection.add_text('advanced', "Advanced Python concepts decorators generators")
    collection.add_text('web', "Web development with Django Flask frameworks")
    collection.add_text('data', "Data analysis pandas numpy visualization")
    collection.add_text('ml', "Machine learning scikit-learn neural networks")
    
    print(f"Collection size: {collection.count} documents")
    print(f"Keys: {collection.keys()}")
    
    # Find similar documents
    print("\nFinding documents similar to 'intro':")
    similar = collection.find_similar('intro', threshold=0.1)
    for doc_id, sim in similar:
        print(f"  {doc_id}: {sim:.4f}")
    
    # Find all similar pairs
    print("\nFinding all similar pairs (threshold: 0.1):")
    pairs = collection.find_all_similar_pairs(threshold=0.1)
    for key1, key2, sim in pairs:
        print(f"  ({key1}, {key2}): {sim:.4f}")
    print()


def example_serialization():
    """Example 6: Serialization and persistence."""
    print("=" * 60)
    print("Example 6: Serialization and Persistence")
    print("=" * 60)
    
    # Create MinHashMap and add data
    collection1 = MinHashMap(num_hash=64, seed=42)
    collection1.add('set1', {'apple', 'banana', 'cherry'})
    collection1.add('set2', {'apple', 'banana', 'date'})
    collection1.add('set3', {'x', 'y', 'z'})
    
    # Serialize to JSON
    json_data = collection1.to_json()
    print(f"Serialized size: {len(json_data)} bytes")
    
    # Deserialize
    collection2 = MinHashMap.from_json(json_data)
    
    # Verify
    print(f"Restored collection size: {collection2.count}")
    print(f"Keys match: {set(collection1.keys()) == set(collection2.keys())}")
    
    # Compare similarities
    sim1 = collection1.similarity('set1', 'set2')
    sim2 = collection2.similarity('set1', 'set2')
    print(f"Similarity preserved: {sim1:.4f} == {sim2:.4f}")
    print()


def example_accuracy_vs_speed():
    """Example 7: Accuracy vs Speed trade-off."""
    print("=" * 60)
    print("Example 7: Accuracy vs Speed Trade-off")
    print("=" * 60)
    
    import time
    
    test_sets = [
        ({f'item{i}' for i in range(100)}, {f'item{i}' for i in range(50, 150)}),
    ]
    set1, set2 = test_sets[0]
    exact_sim = exact_jaccard_similarity(set1, set2)
    
    print(f"Set sizes: {len(set1)} and {len(set2)}")
    print(f"Exact similarity: {exact_sim:.4f}")
    print()
    
    hash_counts = [32, 64, 128, 256, 512, 1024]
    
    print(f"{'Hashes':>8} {'Time (ms)':>12} {'Estimated':>12} {'Error':>10}")
    print("-" * 45)
    
    for num_hash in hash_counts:
        mh = MinHash(num_hash=num_hash, seed=42)
        
        start = time.perf_counter()
        for _ in range(100):
            sig1 = mh.compute_signature(set1)
            sig2 = mh.compute_signature(set2)
            estimated = sig1.jaccard_similarity(sig2)
        elapsed = (time.perf_counter() - start) * 10  # ms per operation
        
        error = abs(estimated - exact_sim)
        print(f"{num_hash:>8} {elapsed:>12.3f} {estimated:>12.4f} {error:>10.4f}")
    
    print()
    
    # Show error bounds
    print("Theoretical error bounds:")
    for num_hash in [64, 128, 256]:
        expected_error, ci = similarity_error_bounds(num_hash)
        print(f"  {num_hash} hashes: expected error ≈ {expected_error:.4f}, 95% CI ≈ ±{ci:.4f}")
    print()


def example_recommended_settings():
    """Example 8: Getting recommended settings."""
    print("=" * 60)
    print("Example 8: Recommended Settings")
    print("=" * 60)
    
    target_errors = [0.05, 0.1, 0.15, 0.2]
    
    print("Recommended number of hash functions:")
    print("-" * 45)
    print(f"{'Target Error':>15} {'Recommended Hashes':>20}")
    
    for target_error in target_errors:
        num_hash = recommended_num_hash(target_error)
        print(f"{target_error:>15.2f} {num_hash:>20}")
    
    print()
    
    # LSH bands recommendation
    print("LSH band configuration (for 128 hashes):")
    print("-" * 45)
    
    num_hash = 128
    for num_bands in [8, 16, 32, 64]:
        rows_per_band = num_hash // num_bands
        # Approximate threshold for 50% probability of being a candidate
        threshold = (1.0 / num_bands) ** (1.0 / rows_per_band)
        print(f"  {num_bands} bands × {rows_per_band} rows: threshold ≈ {threshold:.2%}")
    
    print()


def example_duplicate_detection():
    """Example 9: Near-duplicate document detection."""
    print("=" * 60)
    print("Example 9: Near-Duplicate Document Detection")
    print("=" * 60)
    
    documents = {
        'original': """
            The quick brown fox jumps over the lazy dog. This sentence contains
            every letter of the alphabet and is commonly used for testing.
            """,
        'typo': """
            The quick brown fox jumps over the lazy dog. This sentence contains
            every letter of the alphabet and is commonly used for testing!
            """,
        'rewritten': """
            A fast brown fox leaps over a sleepy dog. This phrase includes all
            letters of the alphabet and is often used for testing purposes.
            """,
        'different': """
            Machine learning is transforming industries worldwide. From healthcare
            to finance, AI applications are becoming increasingly prevalent.
            """,
    }
    
    # Clean documents
    documents = {k: ' '.join(v.split()) for k, v in documents.items()}
    
    mh = MinHashMap(num_hash=256, seed=42)
    
    # Add all documents
    for doc_id, text in documents.items():
        mh.add_text(doc_id, text, ngram_size=4)
    
    print("Document preview:")
    for doc_id, text in documents.items():
        print(f"  {doc_id}: \"{text[:50]}...\"")
    
    # Find all similar pairs
    print("\nSimilar document pairs (threshold: 0.3):")
    pairs = mh.find_all_similar_pairs(threshold=0.3)
    
    for doc1, doc2, sim in pairs:
        print(f"  ({doc1}, {doc2}): {sim:.2%}")
        if sim > 0.8:
            print(f"    → Near-duplicate detected!")
        elif sim > 0.5:
            print(f"    → Similar content")
    
    print()


def main():
    """Run all examples."""
    example_basic_similarity()
    example_text_similarity()
    example_plagiarism_detection()
    example_lsh_index()
    example_minhash_map()
    example_serialization()
    example_accuracy_vs_speed()
    example_recommended_settings()
    example_duplicate_detection()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()