"""
Cuckoo Filter usage examples.

Demonstrates:
- Basic operations (insert, contains, delete)
- URL deduplication
- Spam detection
- Serialization
"""

import sys
import os

# Add the Python directory (parent of cuckoo_filter_utils) to path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent_dir)

from cuckoo_filter_utils import CuckooFilter, create_optimal_filter


def basic_example():
    """Basic usage example."""
    print("\n=== Basic Usage ===")
    
    # Create a filter with capacity of 10000 items
    cf = CuckooFilter(10000)
    
    # Insert items
    items = ["apple", "banana", "cherry", "date", "elderberry"]
    for item in items:
        cf.insert_string(item)
        print(f"Inserted: {item}")
    
    print()
    
    # Check membership
    print("Checking membership:")
    print(f"  Contains 'apple': {cf.contains_string('apple')}")
    print(f"  Contains 'grape': {cf.contains_string('grape')}")
    
    # Delete an item
    print()
    cf.delete_string("banana")
    print(f"After deleting 'banana', contains 'banana': {cf.contains_string('banana')}")
    
    # Show stats
    print()
    print(f"Stats: {cf}")
    print(f"Items in filter: {len(cf)}")


def url_dedup_example():
    """URL deduplication example (web crawler use case)."""
    print("\n=== URL Deduplication ===")
    
    # Create filter optimized for 100K URLs with low FP rate
    cf = create_optimal_filter(100000, fp_rate=0.001)
    
    # URLs already crawled
    crawled_urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3",
        "https://test.com/article",
        "https://blog.example.com/post",
    ]
    
    for url in crawled_urls:
        cf.insert_string(url)
    
    # Simulate checking URLs during crawling
    new_urls = [
        "https://example.com/page1",    # Already seen - will be skipped
        "https://example.com/page4",    # New - will be crawled
        "https://test.com/article",     # Already seen - will be skipped
        "https://newsite.com/page",     # New - will be crawled
    ]
    
    print("Checking if URLs have been visited:")
    for url in new_urls:
        if cf.contains_string(url):
            print(f"  [SKIP] {url} (already visited)")
        else:
            print(f"  [NEW]  {url}")
            cf.insert_string(url)  # Add to filter
    
    print()
    print(f"Total URLs tracked: {cf.count}")


def spam_detection_example():
    """Spam detection example."""
    print("\n=== Spam Detection ===")
    
    cf = CuckooFilter(50000)
    
    # Known spam keywords
    spam_keywords = [
        "FREE MONEY",
        "WINNER",
        "URGENT",
        "LOTTERY",
        "CLICK HERE NOW",
        "CONGRATULATIONS",
        "ACT IMMEDIATELY",
    ]
    
    for keyword in spam_keywords:
        cf.insert_string(keyword)
    
    # Test messages
    messages = [
        "FREE MONEY just for you!",
        "Meeting scheduled for tomorrow",
        "CONGRATULATIONS! You won the LOTTERY!",
        "Can you review the document?",
        "URGENT: Your account needs verification",
    ]
    
    print("Spam detection results:")
    for msg in messages:
        is_spam = any(cf.contains_string(kw) and kw in msg.upper() 
                      for kw in spam_keywords)
        status = "[SPAM]" if is_spam else "[CLEAN]"
        print(f"  {status:10s} {msg}")


def serialization_example():
    """Serialization example."""
    print("\n=== Serialization ===")
    
    # Create and populate filter
    cf1 = CuckooFilter(1000)
    items = ["red", "green", "blue", "yellow", "purple"]
    
    for item in items:
        cf1.insert_string(item)
    
    # Serialize
    json_data = cf1.to_json()
    print(f"Serialized size: {len(json_data)} bytes")
    
    # Deserialize
    cf2 = CuckooFilter.from_json(json_data)
    
    # Verify all items found
    print("After deserialization:")
    for item in items:
        found = cf2.contains_string(item)
        status = "✓" if found else "✗"
        print(f"  {status} {item} found")
    
    # Clone example
    cf3 = cf1.clone()
    print(f"\nCloned filter has same count: {cf3.count == cf1.count}")


def performance_example():
    """Performance demonstration."""
    print("\n=== Performance Demo ===")
    
    import time
    
    cf = create_optimal_filter(100000, fp_rate=0.01)
    
    # Insert performance
    start = time.time()
    for i in range(50000):
        cf.insert_string(f"user-{i}")
    insert_time = time.time() - start
    
    # Lookup performance
    start = time.time()
    for i in range(50000):
        cf.contains_string(f"user-{i}")
    lookup_time = time.time() - start
    
    # Stats
    stats = cf.stats()
    
    print(f"Items inserted: 50000")
    print(f"Insert time: {insert_time:.3f}s")
    print(f"Lookup time: {lookup_time:.3f}s")
    print(f"Memory usage: {stats['memory_bytes']:,} bytes")
    print(f"Load factor: {stats['load_factor']:.1%}")
    print(f"Expected FP rate: {stats['expected_fp_rate']:.2%}")


def comparison_with_bloom():
    """Comparison with Bloom filter."""
    print("\n=== Cuckoo vs Bloom Filter Comparison ===")
    
    print("Cuckoo Filter Advantages:")
    print("  ✓ Supports deletion")
    print("  ✓ Better space efficiency (~4-5 bits/item vs ~10 bits/item)")
    print("  ✓ Lower false positive rates")
    print("  ✓ Constant time operations (O(1) average)")
    
    print()
    print("Use Cases:")
    print("  - URL deduplication (web crawling)")
    print("  - Spam/blacklist filtering")
    print("  - Cache filtering")
    print("  - Duplicate detection in streams")


def run_all_examples():
    """Run all examples."""
    basic_example()
    url_dedup_example()
    spam_detection_example()
    serialization_example()
    performance_example()
    comparison_with_bloom()


if __name__ == "__main__":
    run_all_examples()