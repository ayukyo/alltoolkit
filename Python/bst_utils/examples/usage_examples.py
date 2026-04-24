"""
BST Utilities - Usage Examples
================================
Comprehensive examples demonstrating all features of the BST utilities.
"""

import sys
sys.path.insert(0, '..')

from mod import (
    BST, create_bst, create_balanced_bst, 
    merge_bsts, are_identical, lowest_common_ancestor
)


def basic_operations():
    """Demonstrate basic BST operations."""
    print("=" * 60)
    print("Basic Operations")
    print("=" * 60)
    
    # Create a BST
    bst = BST[int]()
    
    # Insert values
    print("\n1. Inserting values: 50, 30, 70, 20, 40, 60, 80")
    for val in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(val)
    
    print(f"   Tree size: {bst.size}")
    print(f"   Tree height: {bst.height()}")
    
    # Search
    print("\n2. Searching:")
    print(f"   Contains 30? {bst.contains(30)}")
    print(f"   Contains 100? {bst.contains(100)}")
    
    # Min/Max
    print("\n3. Min/Max values:")
    print(f"   Min: {bst.find_min()}")
    print(f"   Max: {bst.find_max()}")
    
    # Delete
    print("\n4. Deleting 30:")
    bst.delete(30)
    print(f"   Tree size after deletion: {bst.size}")
    print(f"   Contains 30? {bst.contains(30)}")


def traversal_examples():
    """Demonstrate all traversal methods."""
    print("\n" + "=" * 60)
    print("Traversal Examples")
    print("=" * 60)
    
    bst = create_bst([50, 30, 70, 20, 40, 60, 80])
    
    print("\nTree structure:")
    print("        50")
    print("       /  \\")
    print("      30   70")
    print("     / \\   / \\")
    print("    20 40 60 80")
    
    print("\n1. In-order (sorted):")
    print(f"   {list(bst.inorder())}")
    
    print("\n2. Pre-order (root first):")
    print(f"   {list(bst.preorder())}")
    
    print("\n3. Post-order (root last):")
    print(f"   {list(bst.postorder())}")
    
    print("\n4. Level-order (BFS):")
    print(f"   {list(bst.levelorder())}")
    
    print("\n5. Reverse in-order (descending):")
    print(f"   {list(bst.reverse_inorder())}")
    
    print("\n6. Iteration (default is in-order):")
    print(f"   {list(bst)}")


def successor_predecessor_examples():
    """Demonstrate successor and predecessor finding."""
    print("\n" + "=" * 60)
    print("Successor & Predecessor")
    print("=" * 60)
    
    bst = create_bst([50, 30, 70, 20, 40, 60, 80])
    
    print("\nTree: [20, 30, 40, 50, 60, 70, 80]")
    
    print("\n1. Successors:")
    for val in [20, 40, 50, 70]:
        succ = bst.find_successor(val)
        print(f"   Successor of {val}: {succ}")
    
    print("\n2. Predecessors:")
    for val in [30, 50, 60, 80]:
        pred = bst.find_predecessor(val)
        print(f"   Predecessor of {val}: {pred}")


def range_query_examples():
    """Demonstrate range query operations."""
    print("\n" + "=" * 60)
    print("Range Queries")
    print("=" * 60)
    
    bst = create_bst([50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45])
    
    print(f"\nAll values: {sorted(list(bst))}")
    
    print("\n1. Range [30, 60]:")
    print(f"   Values: {bst.range_query(30, 60)}")
    print(f"   Count: {bst.count_range(30, 60)}")
    
    print("\n2. Range [1, 25]:")
    print(f"   Values: {bst.range_query(1, 25)}")
    
    print("\n3. Range [70, 100]:")
    print(f"   Values: {bst.range_query(70, 100)}")


def kth_element_examples():
    """Demonstrate k-th element finding."""
    print("\n" + "=" * 60)
    print("K-th Element Finding")
    print("=" * 60)
    
    bst = create_bst([50, 30, 70, 20, 40, 60, 80])
    
    print(f"\nAll values: {sorted(list(bst))}")
    
    print("\n1. K-th smallest:")
    for k in [1, 3, 5, 7]:
        print(f"   {k}-th smallest: {bst.kth_smallest(k)}")
    
    print("\n2. K-th largest:")
    for k in [1, 3, 5, 7]:
        print(f"   {k}-th largest: {bst.kth_largest(k)}")


def balancing_examples():
    """Demonstrate tree balancing."""
    print("\n" + "=" * 60)
    print("Tree Balancing")
    print("=" * 60)
    
    # Unbalanced tree (inserted in sorted order)
    print("\n1. Creating unbalanced tree (inserting 1-7 in order):")
    bst = BST[int]()
    for val in [1, 2, 3, 4, 5, 6, 7]:
        bst.insert(val)
    
    print(f"   Height: {bst.height()}")
    print(f"   Is balanced? {bst.is_balanced()}")
    
    print("\n2. Balancing the tree:")
    bst.balance()
    print(f"   Height after balance: {bst.height()}")
    print(f"   Is balanced? {bst.is_balanced()}")
    print(f"   Root value: {bst.root.value}")
    
    print("\n3. Creating balanced BST directly from sorted list:")
    balanced = create_balanced_bst([1, 2, 3, 4, 5, 6, 7])
    print(f"   Height: {balanced.height()}")
    print(f"   Is balanced? {balanced.is_balanced()}")


def serialization_examples():
    """Demonstrate serialization and deserialization."""
    print("\n" + "=" * 60)
    print("Serialization")
    print("=" * 60)
    
    bst = create_bst([50, 30, 70, 20, 40, 60, 80])
    
    print("\n1. To list (level-order):")
    serialized = bst.to_list()
    print(f"   {serialized}")
    
    print("\n2. To sorted list:")
    sorted_list = bst.to_sorted_list()
    print(f"   {sorted_list}")
    
    print("\n3. From list (reconstruct):")
    bst2 = BST.from_list(serialized)
    print(f"   Reconstructed: {list(bst2)}")
    print(f"   Identical? {are_identical(bst, bst2)}")


def utility_functions():
    """Demonstrate utility functions."""
    print("\n" + "=" * 60)
    print("Utility Functions")
    print("=" * 60)
    
    print("\n1. create_bst() - Create BST from list:")
    bst = create_bst([5, 3, 7, 1, 9, 4, 6])
    print(f"   Created: {list(bst)}")
    
    print("\n2. merge_bsts() - Merge two BSTs:")
    bst1 = create_bst([1, 3, 5, 7])
    bst2 = create_bst([2, 4, 6, 8])
    merged = merge_bsts(bst1, bst2)
    print(f"   BST1: {list(bst1)}")
    print(f"   BST2: {list(bst2)}")
    print(f"   Merged: {list(merged)}")
    
    print("\n3. lowest_common_ancestor():")
    bst = create_bst([50, 30, 70, 20, 40, 60, 80])
    print(f"   Tree: {list(bst)}")
    print(f"   LCA(20, 40): {lowest_common_ancestor(bst, 20, 40)}")
    print(f"   LCA(20, 80): {lowest_common_ancestor(bst, 20, 80)}")
    print(f"   LCA(60, 80): {lowest_common_ancestor(bst, 60, 80)}")


def tree_validation():
    """Demonstrate tree validation."""
    print("\n" + "=" * 60)
    print("Tree Validation")
    print("=" * 60)
    
    bst = create_bst([50, 30, 70, 20, 40])
    
    print("\n1. Valid BST:")
    print(f"   Is valid BST? {bst.is_valid_bst()}")
    
    print("\n2. Tree properties:")
    print(f"   Size: {bst.size}")
    print(f"   Height: {bst.height()}")
    print(f"   Is balanced? {bst.is_balanced()}")
    print(f"   Is empty? {bst.is_empty}")
    
    print("\n3. Depth of values:")
    for val in [50, 30, 20]:
        print(f"   Depth of {val}: {bst.depth(val)}")


def string_example():
    """Demonstrate BST with string values."""
    print("\n" + "=" * 60)
    print("String Values Example")
    print("=" * 60)
    
    bst = BST[str]()
    words = ["banana", "apple", "cherry", "date", "elderberry", "fig", "grape"]
    
    print(f"\n1. Inserting words: {words}")
    for word in words:
        bst.insert(word)
    
    print(f"\n2. In-order (alphabetically):")
    print(f"   {list(bst)}")
    
    print(f"\n3. Min/Max:")
    print(f"   First alphabetically: {bst.find_min()}")
    print(f"   Last alphabetically: {bst.find_max()}")
    
    print(f"\n4. Search:")
    print(f"   Contains 'apple'? {bst.contains('apple')}")
    print(f"   Contains 'orange'? {bst.contains('orange')}")


def custom_objects_example():
    """Demonstrate BST with custom objects using comparator."""
    print("\n" + "=" * 60)
    print("Custom Objects Example (Tuples)")
    print("=" * 60)
    
    # BST with tuples (comparing by first element)
    bst = BST[tuple]()
    data = [(50, "Alice"), (30, "Bob"), (70, "Charlie"), (20, "David"), (40, "Eve")]
    
    print(f"\n1. Inserting (score, name) tuples:")
    for item in data:
        bst.insert(item)
    
    print(f"\n2. In-order (by score):")
    for item in bst:
        print(f"   {item}")
    
    print(f"\n3. Find by score:")
    # Create a search tuple with same key
    result = bst.search((30, ""))
    print(f"   Search for (30, ''): {result.value if result else 'Not found'}")


def visualization_example():
    """Demonstrate tree visualization."""
    print("\n" + "=" * 60)
    print("Tree Visualization")
    print("=" * 60)
    
    bst = create_bst([50, 30, 70, 20, 40, 60, 80])
    
    print("\nString representation:")
    print(bst)


def main():
    """Run all examples."""
    basic_operations()
    traversal_examples()
    successor_predecessor_examples()
    range_query_examples()
    kth_element_examples()
    balancing_examples()
    serialization_examples()
    utility_functions()
    tree_validation()
    string_example()
    custom_objects_example()
    visualization_example()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()