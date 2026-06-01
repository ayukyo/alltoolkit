"""Usage examples for binary_tree_utils."""

from mod import (
    TreeNode, from_list, from_nested_tuple, to_list,
    preorder, inorder, postorder, level_order, zigzag_level_order, morris_inorder,
    find, find_path, lowest_common_ancestor,
    height, count, leaf_count, is_balanced, is_symmetric,
    mirror, clone, map_values,
    insert_level_order, delete_node,
    diameter, all_paths, path_sum, max_path_sum,
    serialize, deserialize, pretty_print
)


def demo_basic_operations():
    print("=== Basic Operations ===")
    
    # Build tree from list
    root = from_list([1, 2, 3, 4, 5, 6, 7])
    print(f"Built tree from list: {to_list(root)}")
    
    # Build tree from nested tuple
    root2 = from_nested_tuple(((None, 4, None), 2, (None, 5, None)))
    print(f"Built tree from tuple: {to_list(root2)}")
    
    # Pretty print
    print("\nPretty print:")
    print(pretty_print(root))


def demo_traversals():
    print("\n=== Traversals ===")
    
    root = from_list([1, 2, 3, 4, 5])
    
    print(f"Preorder (root-left-right): {preorder(root)}")
    print(f"Inorder (left-root-right): {inorder(root)}")
    print(f"Postorder (left-right-root): {postorder(root)}")
    print(f"Level order: {level_order(root)}")
    print(f"Zigzag level order: {zigzag_level_order(root)}")
    print(f"Morris inorder (O(1) space): {morris_inorder(root)}")


def demo_properties():
    print("\n=== Tree Properties ===")
    
    root = from_list([1, 2, 3, 4, 5])
    
    print(f"Height: {height(root)}")
    print(f"Node count: {count(root)}")
    print(f"Leaf count: {leaf_count(root)}")
    print(f"Is balanced: {is_balanced(root)}")
    print(f"Is symmetric: {is_symmetric(root)}")
    
    # Check symmetry
    symmetric_tree = from_nested_tuple(((None, 2, None), 1, (None, 2, None)))
    print(f"Symmetric tree is symmetric: {is_symmetric(symmetric_tree)}")


def demo_queries():
    print("\n=== Query Operations ===")
    
    root = from_list([1, 2, 3, 4, 5])
    
    # Find node
    node = find(root, 4)
    print(f"Found node with value 4: {node}")
    
    # Find path
    path = find_path(root, 5)
    print(f"Path to 5: {[n.val for n in path]}")
    
    # Lowest common ancestor
    lca = lowest_common_ancestor(root, 4, 5)
    print(f"LCA of 4 and 5: {lca.val}")


def demo_modification():
    print("\n=== Modification ===")
    
    root = from_list([1, 2, 3, None, 4])
    print(f"Original level order: {level_order(root)}")
    
    # Mirror
    mirrored = mirror(clone(root))
    print(f"Mirrored level order: {level_order(mirrored)}")
    
    # Map values
    doubled = map_values(root, lambda x: x * 2)
    print(f"Doubled values level order: {level_order(doubled)}")
    
    # Insert
    inserted = insert_level_order(root, 5)
    print(f"After inserting 5: {level_order(inserted)}")
    
    # Delete
    deleted = delete_node(root, 2)
    print(f"After deleting 2: {level_order(deleted)}")


def demo_paths_and_sums():
    print("\n=== Path Operations ===")
    
    root = from_list([1, 2, 3, 4, 5])
    
    print(f"Tree diameter: {diameter(root)}")
    print(f"All root-to-leaf paths: {all_paths(root)}")
    print(f"Path sum to 7 (1->2->4): {path_sum(root, 7)}")
    print(f"Max path sum: {max_path_sum(root)}")


def demo_serialization():
    print("\n=== Serialization ===")
    
    root = from_list([1, 2, 3, None, 4])
    
    serialized = serialize(root)
    print(f"Serialized: {serialized}")
    
    restored = deserialize(serialized)
    print(f"Restored level order: {level_order(restored)}")


def demo_binary_search_tree():
    """Example: Binary Search Tree operations."""
    print("\n=== BST Example ===")
    
    # Build BST from sorted list
    values = [1, 2, 3, 4, 5]
    
    # Manual BST construction for demo
    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(5)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    
    print(f"BST inorder (sorted): {inorder(root)}")
    print(f"Find 3: {find(root, 3)}")
    print(f"LCA of 1 and 3: {lowest_common_ancestor_nodes(root, root.left.left, root.left.right).val}")


if __name__ == "__main__":
    demo_basic_operations()
    demo_traversals()
    demo_properties()
    demo_queries()
    demo_modification()
    demo_paths_and_sums()
    demo_serialization()
    demo_binary_search_tree()