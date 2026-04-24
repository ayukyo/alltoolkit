#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - SimHash Utilities Tests
=====================================
Comprehensive test suite for the SimHash utilities module.

Run with: python -m pytest simhash_utils_test.py -v
Or: python simhash_utils_test.py
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simhash_utils.mod import (
    # Core functions
    compute_simhash, compute_simhash_text,
    hamming_distance, hamming_distance_normalized, similarity, are_similar,
    
    # Tokenization
    tokenize_words, tokenize_chars, tokenize_ngrams, tokenize_chinese,
    
    # Hash functions
    hash_token,
    
    # Fingerprint utilities
    fingerprint_to_binary, fingerprint_to_hex, hex_to_fingerprint,
    fingerprint_chunks, is_valid_fingerprint,
    
    # Index
    SimHashIndex,
    
    # Advanced
    compute_weighted_simhash, compute_simhash_with_features,
    batch_compute_simhash, find_near_duplicates,
    compute_distance_matrix, compute_similarity_matrix,
    compute_simhash_chinese, compare_documents,
    
    # Constants
    DEFAULT_FINGERPRINT_SIZE, DEFAULT_TOKENIZER, DEFAULT_NGRAM_SIZE
)


class TestTokenization(unittest.TestCase):
    """Test tokenization functions."""
    
    def test_tokenize_words_basic(self):
        """Test basic word tokenization."""
        tokens = tokenize_words("Hello World")
        self.assertEqual(tokens, ['hello', 'world'])
    
    def test_tokenize_words_punctuation(self):
        """Test punctuation removal."""
        tokens = tokenize_words("Hello, World! How are you?", remove_punctuation=True)
        self.assertEqual(tokens, ['hello', 'world', 'how', 'are', 'you'])
    
    def test_tokenize_words_min_length(self):
        """Test minimum length filter."""
        tokens = tokenize_words("a an the hello", min_length=3)
        self.assertEqual(tokens, ['the', 'hello'])
    
    def test_tokenize_chars_basic(self):
        """Test character tokenization."""
        tokens = tokenize_chars("Hi!")
        self.assertEqual(tokens, ['h', 'i', '!'])
    
    def test_tokenize_chars_remove_whitespace(self):
        """Test whitespace removal."""
        tokens = tokenize_chars("Hi!", remove_whitespace=True)
        self.assertEqual(tokens, ['h', 'i', '!'])
    
    def test_tokenize_ngrams_char(self):
        """Test character n-grams."""
        tokens = tokenize_ngrams("hello", n=2)
        self.assertEqual(tokens, ['he', 'el', 'll', 'lo'])
    
    def test_tokenize_ngrams_word(self):
        """Test word n-grams."""
        tokens = tokenize_ngrams("hello world", n=2, word_level=True)
        self.assertEqual(tokens, ['hello world'])
    
    def test_tokenize_ngrams_longer(self):
        """Test longer n-grams."""
        tokens = tokenize_ngrams("hello world", n=3)
        self.assertEqual(tokens, ['hel', 'ell', 'llo', 'lo ', 'o w', ' wo', 'wor', 'orl', 'rld'])
    
    def test_tokenize_chinese_char(self):
        """Test Chinese character tokenization."""
        tokens = tokenize_chinese("你好世界")
        self.assertEqual(tokens, ['你', '好', '世', '界'])
    
    def test_tokenize_chinese_ngram(self):
        """Test Chinese n-gram tokenization."""
        tokens = tokenize_chinese("你好世界", mode='ngram', ngram_size=2)
        self.assertEqual(tokens, ['你好', '好世', '世界'])


class TestHashFunctions(unittest.TestCase):
    """Test hash functions."""
    
    def test_hash_token_sha256(self):
        """Test SHA256 hashing."""
        h1 = hash_token("test", algorithm='sha256', size=64)
        h2 = hash_token("test", algorithm='sha256', size=64)
        self.assertEqual(h1, h2)  # Same input, same output
        self.assertTrue(0 <= h1 < (1 << 64))
    
    def test_hash_token_different_inputs(self):
        """Test different inputs produce different hashes."""
        h1 = hash_token("hello", algorithm='sha256', size=64)
        h2 = hash_token("world", algorithm='sha256', size=64)
        self.assertNotEqual(h1, h2)
    
    def test_hash_token_fnv1a(self):
        """Test FNV-1a hashing."""
        h = hash_token("test", algorithm='fnv1a', size=64)
        self.assertTrue(0 <= h < (1 << 64))
    
    def test_hash_token_consistency(self):
        """Test hash consistency across algorithms."""
        for algo in ['sha256', 'md5', 'fnv1a', 'murmur']:
            h1 = hash_token("consistent", algorithm=algo, size=64)
            h2 = hash_token("consistent", algorithm=algo, size=64)
            self.assertEqual(h1, h2)


class TestSimHashCore(unittest.TestCase):
    """Test core SimHash functions."""
    
    def test_compute_simhash_empty(self):
        """Test empty input."""
        fp = compute_simhash([])
        self.assertEqual(fp, 0)
    
    def test_compute_simhash_single_token(self):
        """Test single token."""
        fp = compute_simhash(["hello"])
        self.assertTrue(is_valid_fingerprint(fp))
    
    def test_compute_simhash_multiple_tokens(self):
        """Test multiple tokens."""
        fp = compute_simhash(["hello", "world"])
        self.assertTrue(is_valid_fingerprint(fp))
    
    def test_compute_simhash_text_basic(self):
        """Test basic text hashing."""
        fp = compute_simhash_text("hello world")
        self.assertTrue(is_valid_fingerprint(fp))
    
    def test_compute_simhash_text_different_tokenizers(self):
        """Test different tokenizers."""
        fp_word = compute_simhash_text("hello world", tokenizer='word')
        fp_char = compute_simhash_text("hello world", tokenizer='char')
        fp_ngram = compute_simhash_text("hello world", tokenizer='ngram')
        
        # All should be valid but likely different
        self.assertTrue(is_valid_fingerprint(fp_word))
        self.assertTrue(is_valid_fingerprint(fp_char))
        self.assertTrue(is_valid_fingerprint(fp_ngram))
    
    def test_similar_texts_low_distance(self):
        """Test similar texts have low Hamming distance."""
        fp1 = compute_simhash_text("The quick brown fox jumps over the lazy dog")
        fp2 = compute_simhash_text("The quick brown fox jumped over the lazy dog")
        
        dist = hamming_distance(fp1, fp2)
        self.assertLess(dist, 10)  # Should be similar
    
    def test_different_texts_high_distance(self):
        """Test different texts have higher Hamming distance."""
        fp1 = compute_simhash_text("Python is a programming language")
        fp2 = compute_simhash_text("The weather is nice today")
        
        dist = hamming_distance(fp1, fp2)
        self.assertGreater(dist, 5)  # Should be different
    
    def test_identical_texts_zero_distance(self):
        """Test identical texts have zero distance."""
        fp1 = compute_simhash_text("hello world")
        fp2 = compute_simhash_text("hello world")
        
        self.assertEqual(fp1, fp2)
        self.assertEqual(hamming_distance(fp1, fp2), 0)


class TestHammingDistance(unittest.TestCase):
    """Test Hamming distance functions."""
    
    def test_hamming_distance_basic(self):
        """Test basic Hamming distance."""
        self.assertEqual(hamming_distance(0b1111, 0b1100, size=4), 2)
        self.assertEqual(hamming_distance(0b1010, 0b0101, size=4), 4)
    
    def test_hamming_distance_identical(self):
        """Test identical values."""
        self.assertEqual(hamming_distance(0b1111, 0b1111, size=4), 0)
    
    def test_hamming_distance_normalized(self):
        """Test normalized distance."""
        self.assertEqual(hamming_distance_normalized(0b1111, 0b1100, size=4), 0.5)
        self.assertEqual(hamming_distance_normalized(0b1111, 0b1111, size=4), 0.0)
    
    def test_similarity(self):
        """Test similarity calculation."""
        self.assertEqual(similarity(0b1111, 0b1100, size=4), 0.5)
        self.assertEqual(similarity(0b1111, 0b1111, size=4), 1.0)
    
    def test_are_similar(self):
        """Test similarity threshold."""
        fp1 = compute_simhash_text("hello world")
        fp2 = compute_simhash_text("hello world!")
        
        # These should be similar
        self.assertTrue(are_similar(fp1, fp2, threshold=10))


class TestFingerprintUtilities(unittest.TestCase):
    """Test fingerprint utility functions."""
    
    def test_fingerprint_to_binary(self):
        """Test binary conversion."""
        self.assertEqual(fingerprint_to_binary(0b1100, size=4), '1100')
        self.assertEqual(fingerprint_to_binary(0b0001, size=4), '0001')
    
    def test_fingerprint_to_hex(self):
        """Test hex conversion."""
        self.assertEqual(fingerprint_to_hex(255, size=8), 'ff')
        self.assertEqual(fingerprint_to_hex(16, size=8), '10')
    
    def test_hex_to_fingerprint(self):
        """Test hex to fingerprint conversion."""
        self.assertEqual(hex_to_fingerprint('ff'), 255)
        self.assertEqual(hex_to_fingerprint('10'), 16)
    
    def test_fingerprint_roundtrip(self):
        """Test hex roundtrip conversion."""
        fp = compute_simhash_text("test")
        hex_str = fingerprint_to_hex(fp)
        restored = hex_to_fingerprint(hex_str)
        self.assertEqual(fp, restored)
    
    def test_fingerprint_chunks(self):
        """Test fingerprint chunking."""
        fp = 0xDEADBEEF
        chunks = fingerprint_chunks(fp, chunk_size=8, total_size=32)
        self.assertEqual(len(chunks), 4)
        self.assertEqual(chunks[0], 239)  # 0xEF
    
    def test_is_valid_fingerprint(self):
        """Test fingerprint validation."""
        self.assertTrue(is_valid_fingerprint(0, size=64))
        self.assertTrue(is_valid_fingerprint(0xFFFFFFFFFFFFFFFF, size=64))
        self.assertFalse(is_valid_fingerprint(-1, size=64))
        self.assertFalse(is_valid_fingerprint(0xFFFFFFFFFFFFFFFF + 1, size=64))


class TestSimHashIndex(unittest.TestCase):
    """Test SimHash index."""
    
    def test_index_add(self):
        """Test adding documents."""
        index = SimHashIndex()
        fp = index.add("doc1", "hello world")
        self.assertTrue(is_valid_fingerprint(fp))
        self.assertEqual(len(index), 1)
    
    def test_index_add_batch(self):
        """Test batch adding."""
        index = SimHashIndex()
        docs = {"doc1": "hello", "doc2": "world", "doc3": "test"}
        fps = index.add_batch(docs)
        self.assertEqual(len(index), 3)
        self.assertEqual(len(fps), 3)
    
    def test_index_remove(self):
        """Test removing documents."""
        index = SimHashIndex()
        index.add("doc1", "hello")
        self.assertEqual(len(index), 1)
        self.assertTrue(index.remove("doc1"))
        self.assertEqual(len(index), 0)
    
    def test_index_query(self):
        """Test querying for similar documents."""
        index = SimHashIndex()
        index.add("doc1", "Python is a programming language")
        index.add("doc2", "Python is a popular programming language")
        index.add("doc3", "The weather is nice")
        
        # Use a more lenient threshold for short texts
        results = index.query("Python programming guide", threshold=20)
        self.assertGreater(len(results), 0)
        
        # doc1 and doc2 should appear (they're about Python)
        doc_ids = [r[0] for r in results]
        self.assertIn("doc1", doc_ids)
    
    def test_index_contains(self):
        """Test contains check."""
        index = SimHashIndex()
        index.add("doc1", "hello")
        self.assertIn("doc1", index)
        self.assertNotIn("doc2", index)
    
    def test_index_get_fingerprint(self):
        """Test getting fingerprint."""
        index = SimHashIndex()
        index.add("doc1", "hello")
        fp = index.get_fingerprint("doc1")
        self.assertTrue(is_valid_fingerprint(fp))
    
    def test_index_get_document(self):
        """Test getting document."""
        index = SimHashIndex()
        index.add("doc1", "hello world")
        text = index.get_document("doc1")
        self.assertEqual(text, "hello world")


class TestBatchFunctions(unittest.TestCase):
    """Test batch processing functions."""
    
    def test_batch_compute_simhash(self):
        """Test batch computation."""
        texts = ["hello", "world", "test"]
        fps = batch_compute_simhash(texts)
        self.assertEqual(len(fps), 3)
        for fp in fps:
            self.assertTrue(is_valid_fingerprint(fp))
    
    def test_find_near_duplicates(self):
        """Test finding duplicates."""
        texts = ["hello world", "hello world!", "goodbye world"]
        fps = batch_compute_simhash(texts)
        dups = find_near_duplicates(fps, threshold=10)
        
        # Should find at least one pair (hello world and hello world!)
        self.assertGreater(len(dups), 0)
    
    def test_compute_distance_matrix(self):
        """Test distance matrix."""
        fps = [0b1111, 0b1100, 0b0000]
        matrix = compute_distance_matrix(fps, size=4)
        
        self.assertEqual(len(matrix), 3)
        self.assertEqual(matrix[0][0], 0)  # Self-distance is 0
        self.assertEqual(matrix[0][1], 2)  # 1111 vs 1100
    
    def test_compute_similarity_matrix(self):
        """Test similarity matrix."""
        fps = [0b1111, 0b1111, 0b0000]
        matrix = compute_similarity_matrix(fps, size=4)
        
        self.assertEqual(matrix[0][1], 1.0)  # Identical
        self.assertEqual(matrix[0][2], 0.0)  # Completely different


class TestAdvancedFunctions(unittest.TestCase):
    """Test advanced functions."""
    
    def test_compute_weighted_simhash(self):
        """Test weighted SimHash."""
        tokens = ["hello", "world"]
        weights = {"hello": 2.0}
        fp = compute_weighted_simhash(tokens, weights)
        self.assertTrue(is_valid_fingerprint(fp))
    
    def test_compute_simhash_with_features(self):
        """Test feature-based SimHash."""
        features = {"keyword:python": 3.0, "keyword:code": 1.5}
        fp = compute_simhash_with_features(features)
        self.assertTrue(is_valid_fingerprint(fp))
    
    def test_compute_simhash_chinese(self):
        """Test Chinese text SimHash."""
        fp = compute_simhash_chinese("你好世界")
        self.assertTrue(is_valid_fingerprint(fp))
    
    def test_compare_documents(self):
        """Test document comparison."""
        result = compare_documents("hello world", "hello world!")
        
        self.assertIn('similarity', result)
        self.assertIn('hamming_distance', result)
        self.assertIn('interpretation', result)
        
        self.assertGreater(result['similarity'], 0.9)
        self.assertLess(result['hamming_distance'], 10)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_empty_text(self):
        """Test empty text."""
        fp = compute_simhash_text("")
        self.assertEqual(fp, 0)
    
    def test_single_char(self):
        """Test single character."""
        fp = compute_simhash_text("a")
        self.assertTrue(is_valid_fingerprint(fp))
    
    def test_whitespace_only(self):
        """Test whitespace only."""
        fp = compute_simhash_text("   ")
        self.assertEqual(fp, 0)
    
    def test_repeated_text(self):
        """Test repeated text."""
        fp1 = compute_simhash_text("hello hello hello")
        fp2 = compute_simhash_text("hello")
        
        # Repeated words should be similar to single word
        dist = hamming_distance(fp1, fp2)
        self.assertLess(dist, 20)
    
    def test_case_sensitivity(self):
        """Test case sensitivity."""
        fp1 = compute_simhash_text("Hello World", lowercase=True)
        fp2 = compute_simhash_text("hello world", lowercase=True)
        
        # Lowercase should produce same fingerprint
        self.assertEqual(fp1, fp2)
    
    def test_large_text(self):
        """Test large text."""
        large_text = " ".join(["word"] * 1000)
        fp = compute_simhash_text(large_text)
        self.assertTrue(is_valid_fingerprint(fp))
    
    def test_different_fingerprint_sizes(self):
        """Test different fingerprint sizes."""
        for size in [32, 64, 128]:
            fp = compute_simhash_text("test", fingerprint_size=size)
            max_val = (1 << size) - 1
            self.assertTrue(0 <= fp <= max_val)


class TestIntegration(unittest.TestCase):
    """Integration tests."""
    
    def test_full_workflow(self):
        """Test full workflow from text to comparison."""
        # Create index
        index = SimHashIndex()
        
        # Add documents
        docs = {
            "doc1": "Python is great for web development",
            "doc2": "Python is excellent for web apps",
            "doc3": "JavaScript is also good for web development",
            "doc4": "I love pizza"
        }
        index.add_batch(docs)
        
        # Query - use lenient threshold for short texts
        results = index.query("Python web development", threshold=25)
        
        # Should find doc1, doc2, and possibly doc3
        self.assertGreater(len(results), 0)
        
        # Find duplicates - use brute_force for small datasets
        duplicates = index.get_duplicates(threshold=25, brute_force=True)
        self.assertGreater(len(duplicates), 0)
    
    def test_chinese_workflow(self):
        """Test Chinese text workflow."""
        texts = [
            "今天天气很好",
            "今天天气真好",
            "明天天气也不错"
        ]
        
        fps = [compute_simhash_chinese(t) for t in texts]
        
        # First two should be very similar
        dist1 = hamming_distance(fps[0], fps[1])
        self.assertLess(dist1, 20)
        
        # Find duplicates
        dups = find_near_duplicates(fps, threshold=20)
        self.assertGreater(len(dups), 0)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTokenization))
    suite.addTests(loader.loadTestsFromTestCase(TestHashFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestSimHashCore))
    suite.addTests(loader.loadTestsFromTestCase(TestHammingDistance))
    suite.addTests(loader.loadTestsFromTestCase(TestFingerprintUtilities))
    suite.addTests(loader.loadTestsFromTestCase(TestSimHashIndex))
    suite.addTests(loader.loadTestsFromTestCase(TestBatchFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestAdvancedFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)