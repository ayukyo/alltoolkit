"""
BK-Tree Examples

This file demonstrates various use cases of BK-Tree for:
1. Spell checking
2. Fuzzy string matching
3. Auto-complete
4. Dictionary building
"""

from bk_tree import (
    BKTree,
    SpellChecker,
    levenshtein_distance,
    build_tree_from_words,
    find_similar_words
)


def example_basic_usage():
    """Basic BK-Tree usage example."""
    print("=" * 60)
    print("Example 1: Basic BK-Tree Usage")
    print("=" * 60)
    
    # Create a BK-Tree
    tree = BKTree()
    
    # Insert words
    words = ["apple", "apply", "approach", "apricot", "banana", "bandana"]
    for word in words:
        tree.insert(word)
    
    print(f"Inserted {tree.size()} words into tree")
    print(f"Tree height: {tree.get_height()}")
    print()
    
    # Check if word exists
    print(f"Contains 'apple': {tree.contains('apple')}")
    print(f"Contains 'orange': {tree.contains('orange')}")
    print()
    
    # Search for similar words
    print("Searching for words similar to 'aple':")
    results = tree.search("aple", max_distance=2)
    print(f"  Results: {results}")
    print()
    
    # Find nearest word
    print("Finding nearest word to 'banan':")
    nearest = tree.find_nearest("banan")
    print(f"  Nearest: {nearest}")
    print()


def example_spell_checker():
    """Spell checker example."""
    print("=" * 60)
    print("Example 2: Spell Checker")
    print("=" * 60)
    
    # Create spell checker with dictionary
    dictionary = [
        "python", "programming", "computer", "algorithm",
        "database", "network", "software", "hardware",
        "variable", "function", "class", "object",
        "string", "integer", "boolean", "array"
    ]
    
    checker = SpellChecker(dictionary)
    print(f"Spell checker initialized with {len(dictionary)} words")
    print()
    
    # Test words
    test_words = ["pythn", "progrmming", "computr", "algorthm", "python"]
    
    for word in test_words:
        is_correct = checker.is_correct(word)
        print(f"Word: '{word}'")
        print(f"  Correct: {is_correct}")
        
        if not is_correct:
            suggestions = checker.suggest(word, max_distance=2, max_suggestions=3)
            print(f"  Suggestions: {suggestions}")
        print()


def example_autocomplete():
    """Auto-complete like example."""
    print("=" * 60)
    print("Example 3: Auto-complete / Fuzzy Search")
    print("=" * 60)
    
    # Build dictionary of programming terms
    terms = [
        "function", "functional", "functional programming",
        "function call", "function overloading", "function override",
        "class", "class method", "class variable",
        "object", "object-oriented", "object-oriented programming",
        "variable", "variable assignment", "variable scope"
    ]
    
    tree = build_tree_from_words(terms)
    
    # User typing "func"
    print("User types: 'func'")
    results = tree.search("func", max_distance=5)[:5]
    print(f"  Suggestions: {results}")
    print()
    
    # User types "progrm"
    print("User types: 'progrm'")
    results = tree.search("progrm", max_distance=2)[:5]
    print(f"  Suggestions: {results}")
    print()


def example_levenshtein_distance():
    """Levenshtein distance examples."""
    print("=" * 60)
    print("Example 4: Levenshtein Distance")
    print("=" * 60)
    
    pairs = [
        ("kitten", "sitting"),
        ("saturday", "sunday"),
        ("algorithm", "altruistic"),
        ("python", "python"),
        ("", "abc"),
        ("café", "cafe"),
    ]
    
    for s1, s2 in pairs:
        distance = levenshtein_distance(s1, s2)
        print(f"  '{s1}' ↔ '{s2}': {distance}")
    print()


def example_dictionary_builder():
    """Build dictionary from file-like data."""
    print("=" * 60)
    print("Example 5: Building Dictionary from Data")
    print("=" * 60)
    
    # Simulate reading from a file
    word_data = """
    apple
    banana
    cherry
    date
    elderberry
    fig
    grape
    honeydew
    """
    
    # Parse and clean
    words = [w.strip() for w in word_data.strip().split('\n')]
    
    # Build tree
    tree = build_tree_from_words(words)
    
    print(f"Built tree with {tree.size()} words")
    print(f"All words: {tree.get_all_words()}")
    print()
    
    # Query
    print("Finding similar words to 'appl':")
    similar = tree.search("appl", max_distance=1)
    print(f"  Results: {similar}")
    print()


def example_typo_correction():
    """Real-world typo correction example."""
    print("=" * 60)
    print("Example 6: Typo Correction System")
    print("=" * 60)
    
    # Common English words (small sample)
    common_words = [
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
        "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
        "hello", "world", "help", "held", "hell"
    ]
    
    checker = SpellChecker(common_words)
    
    # Sample text with typos
    text = "Helo world! I hav a queston about the queston."
    words = text.split()
    
    print(f"Original text: {text}")
    print()
    print("Analyzing words:")
    
    corrected_text = []
    for word in words:
        # Clean punctuation
        clean_word = word.lower().rstrip('.,!?;:')
        punct = word[len(clean_word):]
        
        if not checker.is_correct(clean_word):
            suggestions = checker.suggest(clean_word, max_distance=2, max_suggestions=1)
            if suggestions:
                corrected = suggestions[0] + punct
                print(f"  '{word}' → '{corrected}' (suggested)")
                corrected_text.append(corrected)
            else:
                print(f"  '{word}' (no suggestion)")
                corrected_text.append(word)
        else:
            corrected_text.append(word)
    
    print()
    print(f"Corrected text: {' '.join(corrected_text)}")
    print()


def example_performance():
    """Performance comparison example."""
    print("=" * 60)
    print("Example 7: Performance Comparison")
    print("=" * 60)
    
    import time
    
    # Generate dictionary
    words = [f"word{i:05d}" for i in range(10000)]
    
    # Build tree
    start = time.time()
    tree = build_tree_from_words(words)
    build_time = time.time() - start
    print(f"Built BK-Tree with {tree.size()} words in {build_time:.3f}s")
    
    # Search using BK-Tree
    search_word = "word00500"
    start = time.time()
    for _ in range(100):
        results = tree.search(search_word, max_distance=1)
    bk_search_time = time.time() - start
    print(f"BK-Tree search (100 queries): {bk_search_time:.3f}s")
    
    # Brute force search
    start = time.time()
    for _ in range(100):
        results = find_similar_words(search_word, words, max_distance=1)
    brute_time = time.time() - start
    print(f"Brute force search (100 queries): {brute_time:.3f}s")
    
    speedup = brute_time / bk_search_time if bk_search_time > 0 else float('inf')
    print(f"Speedup: {speedup:.1f}x")
    print()


def example_custom_distance():
    """Custom distance function example."""
    print("=" * 60)
    print("Example 8: Custom Distance Function")
    print("=" * 60)
    
    # Hamming distance (only works for strings of equal length)
    def hamming_distance(s1, s2):
        if len(s1) != len(s2):
            return float('inf')
        return sum(c1 != c2 for c1, c2 in zip(s1, s2))
    
    tree = BKTree(distance_func=hamming_distance)
    
    # Binary strings
    binaries = ["0000", "0001", "0010", "0100", "1000", "1111"]
    for b in binaries:
        tree.insert(b)
    
    print(f"Inserted {tree.size()} binary strings")
    print()
    
    # Search for similar patterns
    print("Searching for patterns similar to '0000' (Hamming distance ≤ 1):")
    results = tree.search("0000", max_distance=1)
    print(f"  Results: {results}")
    print()


if __name__ == "__main__":
    example_basic_usage()
    example_spell_checker()
    example_autocomplete()
    example_levenshtein_distance()
    example_dictionary_builder()
    example_typo_correction()
    example_performance()
    example_custom_distance()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)