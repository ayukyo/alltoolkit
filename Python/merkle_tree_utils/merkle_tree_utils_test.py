#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Python Merkle Tree Utils Test Suite
默克尔树工具模块单元测试

运行测试:
    cd Python/merkle_tree_utils
    python merkle_tree_utils_test.py
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    MerkleTree, MerkleProof, MerkleForest, MerkleUtils,
    HashAlgorithm, create_tree, get_root, verify_proof
)


class TestMerkleTree:
    """MerkleTree 测试类"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def assert_equal(self, actual, expected, test_name):
        """断言相等"""
        if actual == expected:
            print(f"  ✓ {test_name}")
            self.passed += 1
            return True
        else:
            print(f"  ✗ {test_name}")
            print(f"    Expected: {expected}")
            print(f"    Actual: {actual}")
            self.failed += 1
            return False
    
    def assert_true(self, condition, test_name):
        """断言为真"""
        if condition:
            print(f"  ✓ {test_name}")
            self.passed += 1
            return True
        else:
            print(f"  ✗ {test_name}")
            self.failed += 1
            return False
    
    def assert_false(self, condition, test_name):
        """断言为假"""
        return self.assert_true(not condition, test_name)
    
    def assert_is_none(self, value, test_name):
        """断言为 None"""
        return self.assert_true(value is None, test_name)
    
    def assert_is_not_none(self, value, test_name):
        """断言不为 None"""
        return self.assert_true(value is not None, test_name)
    
    def assert_length(self, data, length, test_name):
        """断言长度"""
        return self.assert_equal(len(data), length, test_name)
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "=" * 60)
        print("MerkleTree 测试套件")
        print("=" * 60)
        
        # 基础构建测试
        self.test_empty_tree()
        self.test_single_leaf()
        self.test_two_leaves()
        self.test_four_leaves()
        self.test_odd_leaves()
        self.test_large_tree()
        
        # 根哈希测试
        self.test_root_hash_consistency()
        self.test_root_hash_different_data()
        
        # 哈希算法测试
        self.test_sha256_algorithm()
        self.test_sha512_algorithm()
        self.test_md5_algorithm()
        self.test_blake2b_algorithm()
        
        # 证明生成测试
        self.test_generate_proof()
        self.test_proof_structure()
        self.test_proof_for_missing_index()
        
        # 证明验证测试
        self.test_verify_valid_proof()
        self.test_verify_invalid_data()
        self.test_verify_tampered_root()
        
        # 叶子操作测试
        self.test_add_leaf()
        self.test_add_leaves_batch()
        self.test_update_leaf()
        self.test_remove_leaf()
        self.test_find_leaf()
        self.test_contains()
        
        # 序列化测试
        self.test_to_dict()
        self.test_from_dict()
        self.test_to_json()
        self.test_from_json()
        
        # 边界值测试
        self.test_bytes_data()
        self.test_mixed_string_bytes()
        self.test_unicode_data()
        self.test_empty_string()
        self.test_long_data()
        self.test_duplicate_data()
        
        # MerkleForest 测试
        self.test_forest_add_tree()
        self.test_forest_get_tree()
        self.test_forest_remove_tree()
        self.test_forest_list_trees()
        
        # MerkleUtils 测试
        self.test_quick_root()
        self.test_compare_trees()
        self.test_find_differences()
        self.test_merge_trees()
        self.test_estimate_proof_size()
        
        # 便捷函数测试
        self.test_create_tree_function()
        self.test_get_root_function()
        self.test_verify_proof_function()
        
        # 打印结果
        print("\n" + "=" * 60)
        print(f"测试结果: {self.passed} 通过, {self.failed} 失败")
        print("=" * 60)
        
        return self.failed == 0
    
    def test_empty_tree(self):
        """测试空树"""
        print("\n[Test: Empty Tree]")
        tree = MerkleTree()
        self.assert_equal(tree.get_leaf_count(), 0, "Empty tree has 0 leaves")
        self.assert_equal(tree.get_tree_height(), 0, "Empty tree height is 0")
        self.assert_is_none(tree.get_root_hash(), "Empty tree root is None")
        self.assert_equal(len(tree), 0, "len() returns 0")
    
    def test_single_leaf(self):
        """测试单叶树"""
        print("\n[Test: Single Leaf]")
        tree = MerkleTree(["hello"])
        self.assert_equal(tree.get_leaf_count(), 1, "Single leaf count")
        self.assert_equal(tree.get_tree_height(), 1, "Single leaf height")
        self.assert_is_not_none(tree.get_root_hash(), "Root hash exists")
        self.assert_equal(tree.get_root_hash(), tree.get_leaf_hash(0), 
                         "Root equals leaf hash")
    
    def test_two_leaves(self):
        """测试两个叶子"""
        print("\n[Test: Two Leaves]")
        tree = MerkleTree(["a", "b"])
        self.assert_equal(tree.get_leaf_count(), 2, "Two leaves count")
        self.assert_equal(tree.get_tree_height(), 2, "Two leaves height")
        
        # 根哈希应该是两个叶子哈希的组合哈希
        left = tree.get_leaf_hash(0)
        right = tree.get_leaf_hash(1)
        expected_root = tree._hash_pair(left, right)
        self.assert_equal(tree.get_root_hash(), expected_root, "Correct root hash")
    
    def test_four_leaves(self):
        """测试四个叶子"""
        print("\n[Test: Four Leaves]")
        tree = MerkleTree(["a", "b", "c", "d"])
        self.assert_equal(tree.get_leaf_count(), 4, "Four leaves count")
        self.assert_equal(tree.get_tree_height(), 3, "Four leaves height")
        self.assert_is_not_none(tree.get_root_hash(), "Root hash exists")
    
    def test_odd_leaves(self):
        """测试奇数个叶子"""
        print("\n[Test: Odd Leaves]")
        tree = MerkleTree(["a", "b", "c"])
        self.assert_equal(tree.get_leaf_count(), 3, "Three leaves count")
        self.assert_equal(tree.get_tree_height(), 3, "Three leaves height")
        self.assert_is_not_none(tree.get_root_hash(), "Root hash exists for odd leaves")
    
    def test_large_tree(self):
        """测试大树"""
        print("\n[Test: Large Tree]")
        data = [f"item_{i}" for i in range(100)]
        tree = MerkleTree(data)
        self.assert_equal(tree.get_leaf_count(), 100, "100 leaves count")
        self.assert_true(tree.get_tree_height() >= 7, "Tree height >= 7")
        self.assert_is_not_none(tree.get_root_hash(), "Root hash exists")
    
    def test_root_hash_consistency(self):
        """测试根哈希一致性"""
        print("\n[Test: Root Hash Consistency]")
        data = ["apple", "banana", "cherry"]
        tree1 = MerkleTree(data)
        tree2 = MerkleTree(data)
        self.assert_equal(tree1.get_root_hash(), tree2.get_root_hash(), 
                         "Same data produces same root")
        
        # 多次获取应该返回相同的值
        root1 = tree1.get_root_hash()
        root2 = tree1.get_root_hash()
        self.assert_equal(root1, root2, "Multiple calls return same root")
    
    def test_root_hash_different_data(self):
        """测试不同数据产生不同根哈希"""
        print("\n[Test: Root Hash Different Data]")
        tree1 = MerkleTree(["a", "b", "c"])
        tree2 = MerkleTree(["a", "b", "d"])
        self.assert_true(tree1.get_root_hash() != tree2.get_root_hash(), 
                        "Different data produces different root")
    
    def test_sha256_algorithm(self):
        """测试 SHA256 算法"""
        print("\n[Test: SHA256 Algorithm]")
        tree = MerkleTree(["test"], HashAlgorithm.SHA256)
        self.assert_equal(tree._hash_algorithm, "sha256", "Algorithm is sha256")
        
        # SHA256 哈希应该是 64 个字符
        root = tree.get_root_hash()
        self.assert_equal(len(root), 64, "SHA256 hash is 64 chars")
    
    def test_sha512_algorithm(self):
        """测试 SHA512 算法"""
        print("\n[Test: SHA512 Algorithm]")
        tree = MerkleTree(["test"], HashAlgorithm.SHA512)
        self.assert_equal(tree._hash_algorithm, "sha512", "Algorithm is sha512")
        
        root = tree.get_root_hash()
        self.assert_equal(len(root), 128, "SHA512 hash is 128 chars")
    
    def test_md5_algorithm(self):
        """测试 MD5 算法"""
        print("\n[Test: MD5 Algorithm]")
        tree = MerkleTree(["test"], "md5")
        self.assert_equal(tree._hash_algorithm, "md5", "Algorithm is md5")
        
        root = tree.get_root_hash()
        self.assert_equal(len(root), 32, "MD5 hash is 32 chars")
    
    def test_blake2b_algorithm(self):
        """测试 BLAKE2b 算法"""
        print("\n[Test: BLAKE2b Algorithm]")
        tree = MerkleTree(["test"], HashAlgorithm.BLAKE2B)
        self.assert_equal(tree._hash_algorithm, "blake2b", "Algorithm is blake2b")
        self.assert_is_not_none(tree.get_root_hash(), "BLAKE2b produces hash")
    
    def test_generate_proof(self):
        """测试证明生成"""
        print("\n[Test: Generate Proof]")
        tree = MerkleTree(["a", "b", "c", "d"])
        
        proof = tree.generate_proof(0)
        self.assert_is_not_none(proof, "Proof generated")
        self.assert_equal(proof.leaf_index, 0, "Correct leaf index")
        self.assert_equal(proof.leaf_hash, tree.get_leaf_hash(0), "Correct leaf hash")
        self.assert_true(len(proof.siblings) > 0, "Has siblings")
        self.assert_true(len(proof.siblings) == len(proof.directions), 
                        "Siblings and directions have same length")
    
    def test_proof_structure(self):
        """测试证明结构"""
        print("\n[Test: Proof Structure]")
        tree = MerkleTree(["a", "b", "c", "d", "e", "f", "g", "h"])
        
        for i in range(8):
            proof = tree.generate_proof(i)
            self.assert_is_not_none(proof, f"Proof {i} exists")
            self.assert_equal(proof.leaf_index, i, f"Correct index {i}")
    
    def test_proof_for_missing_index(self):
        """测试不存在索引的证明"""
        print("\n[Test: Proof for Missing Index]")
        tree = MerkleTree(["a", "b"])
        proof = tree.generate_proof(10)
        self.assert_is_none(proof, "Proof for invalid index is None")
        
        proof_neg = tree.generate_proof(-1)
        self.assert_is_none(proof_neg, "Proof for negative index is None")
    
    def test_verify_valid_proof(self):
        """测试验证有效证明"""
        print("\n[Test: Verify Valid Proof]")
        tree = MerkleTree(["apple", "banana", "cherry", "date"])
        root = tree.get_root_hash()
        
        for i, fruit in enumerate(["apple", "banana", "cherry", "date"]):
            proof = tree.generate_proof(i)
            is_valid = MerkleProof.verify(fruit, proof, root)
            self.assert_true(is_valid, f"Valid proof for {fruit}")
    
    def test_verify_invalid_data(self):
        """测试验证无效数据"""
        print("\n[Test: Verify Invalid Data]")
        tree = MerkleTree(["apple", "banana", "cherry"])
        root = tree.get_root_hash()
        
        proof = tree.generate_proof(0)
        is_valid = MerkleProof.verify("grape", proof, root)
        self.assert_false(is_valid, "Invalid data fails verification")
    
    def test_verify_tampered_root(self):
        """测试篡改的根哈希"""
        print("\n[Test: Verify Tampered Root]")
        tree = MerkleTree(["apple", "banana", "cherry"])
        root = tree.get_root_hash()
        
        proof = tree.generate_proof(0)
        
        # 使用错误的根哈希
        fake_root = "0" * 64
        is_valid = MerkleProof.verify("apple", proof, fake_root)
        self.assert_false(is_valid, "Tampered root fails verification")
    
    def test_add_leaf(self):
        """测试添加叶子"""
        print("\n[Test: Add Leaf]")
        tree = MerkleTree(["a", "b"])
        original_root = tree.get_root_hash()
        
        index = tree.add_leaf("c")
        self.assert_equal(index, 2, "Returns correct index")
        self.assert_equal(tree.get_leaf_count(), 3, "Leaf count increased")
        self.assert_true(tree.get_root_hash() != original_root, "Root changed")
        self.assert_true(tree.contains("c"), "New leaf is in tree")
    
    def test_add_leaves_batch(self):
        """测试批量添加叶子"""
        print("\n[Test: Add Leaves Batch]")
        tree = MerkleTree(["a"])
        
        indices = tree.add_leaves(["b", "c", "d"])
        self.assert_equal(len(indices), 3, "Returns 3 indices")
        self.assert_equal(tree.get_leaf_count(), 4, "Leaf count is 4")
    
    def test_update_leaf(self):
        """测试更新叶子"""
        print("\n[Test: Update Leaf]")
        tree = MerkleTree(["apple", "banana", "cherry"])
        original_root = tree.get_root_hash()
        
        result = tree.update_leaf(1, "blueberry")
        self.assert_true(result, "Update successful")
        self.assert_equal(tree.get_leaf_data(1), "blueberry", "Data updated")
        self.assert_true(tree.get_root_hash() != original_root, "Root changed")
        
        # 更新不存在的索引
        result = tree.update_leaf(10, "date")
        self.assert_false(result, "Update invalid index fails")
    
    def test_remove_leaf(self):
        """测试删除叶子"""
        print("\n[Test: Remove Leaf]")
        tree = MerkleTree(["a", "b", "c", "d"])
        original_root = tree.get_root_hash()
        
        result = tree.remove_leaf(1)
        self.assert_true(result, "Remove successful")
        self.assert_equal(tree.get_leaf_count(), 3, "Leaf count decreased")
        self.assert_true(tree.get_root_hash() != original_root, "Root changed")
        
        # 删除不存在的索引
        result = tree.remove_leaf(10)
        self.assert_false(result, "Remove invalid index fails")
    
    def test_find_leaf(self):
        """测试查找叶子"""
        print("\n[Test: Find Leaf]")
        tree = MerkleTree(["apple", "banana", "cherry"])
        
        index = tree.find_leaf("banana")
        self.assert_equal(index, 1, "Found at correct index")
        
        index = tree.find_leaf("grape")
        self.assert_equal(index, -1, "Not found returns -1")
    
    def test_contains(self):
        """测试包含检查"""
        print("\n[Test: Contains]")
        tree = MerkleTree(["apple", "banana", "cherry"])
        
        self.assert_true(tree.contains("banana"), "Contains banana")
        self.assert_false(tree.contains("grape"), "Does not contain grape")
    
    def test_to_dict(self):
        """测试序列化到字典"""
        print("\n[Test: To Dict]")
        tree = MerkleTree(["a", "b", "c"])
        d = tree.to_dict()
        
        self.assert_true("algorithm" in d, "Has algorithm")
        self.assert_true("leaves" in d, "Has leaves")
        self.assert_true("raw_data" in d, "Has raw_data")
        self.assert_true("tree" in d, "Has tree")
        self.assert_equal(d["algorithm"], "sha256", "Correct algorithm")
        self.assert_equal(len(d["leaves"]), 3, "3 leaves")
        self.assert_equal(d["raw_data"], ["a", "b", "c"], "Correct raw data")
    
    def test_from_dict(self):
        """测试从字典创建"""
        print("\n[Test: From Dict]")
        original = MerkleTree(["a", "b", "c"])
        d = original.to_dict()
        
        restored = MerkleTree.from_dict(d)
        self.assert_equal(restored.get_root_hash(), original.get_root_hash(),
                         "Same root hash")
        self.assert_equal(restored.get_leaf_count(), 3, "Same leaf count")
    
    def test_to_json(self):
        """测试序列化到 JSON"""
        print("\n[Test: To JSON]")
        tree = MerkleTree(["a", "b"])
        json_str = tree.to_json()
        
        self.assert_true(isinstance(json_str, str), "Returns string")
        self.assert_true("algorithm" in json_str, "Has algorithm")
        self.assert_true("leaves" in json_str, "Has leaves")
    
    def test_from_json(self):
        """测试从 JSON 创建"""
        print("\n[Test: From JSON]")
        original = MerkleTree(["x", "y", "z"])
        json_str = original.to_json()
        
        restored = MerkleTree.from_json(json_str)
        self.assert_equal(restored.get_root_hash(), original.get_root_hash(),
                         "Same root from JSON")
    
    def test_bytes_data(self):
        """测试字节数据"""
        print("\n[Test: Bytes Data]")
        tree = MerkleTree([b"hello", b"world"])
        self.assert_equal(tree.get_leaf_count(), 2, "Works with bytes")
        self.assert_is_not_none(tree.get_root_hash(), "Root hash exists")
    
    def test_mixed_string_bytes(self):
        """测试混合字符串和字节"""
        print("\n[Test: Mixed String and Bytes]")
        tree = MerkleTree(["hello", b"world", "test"])
        self.assert_equal(tree.get_leaf_count(), 3, "Works with mixed types")
        self.assert_is_not_none(tree.get_root_hash(), "Root hash exists")
    
    def test_unicode_data(self):
        """测试 Unicode 数据"""
        print("\n[Test: Unicode Data]")
        tree = MerkleTree(["你好", "世界", "🎉", "日本語"])
        self.assert_equal(tree.get_leaf_count(), 4, "Works with Unicode")
        self.assert_is_not_none(tree.get_root_hash(), "Root hash exists")
        
        # 验证证明也能正常工作
        proof = tree.generate_proof(0)
        is_valid = MerkleProof.verify("你好", proof, tree.get_root_hash())
        self.assert_true(is_valid, "Unicode proof verification works")
    
    def test_empty_string(self):
        """测试空字符串"""
        print("\n[Test: Empty String]")
        tree = MerkleTree(["", "a", ""])
        self.assert_equal(tree.get_leaf_count(), 3, "Handles empty strings")
        self.assert_is_not_none(tree.get_root_hash(), "Root hash exists")
    
    def test_long_data(self):
        """测试长数据"""
        print("\n[Test: Long Data]")
        long_data = "x" * 10000
        tree = MerkleTree([long_data, long_data + "y"])
        self.assert_equal(tree.get_leaf_count(), 2, "Handles long data")
        self.assert_is_not_none(tree.get_root_hash(), "Root hash exists")
    
    def test_duplicate_data(self):
        """测试重复数据"""
        print("\n[Test: Duplicate Data]")
        tree = MerkleTree(["a", "b", "a", "a", "b"])
        self.assert_equal(tree.get_leaf_count(), 5, "Handles duplicates")
        
        # 找到第一个 a
        index = tree.find_leaf("a")
        self.assert_equal(index, 0, "find_leaf returns first occurrence")
    
    def test_forest_add_tree(self):
        """测试 MerkleForest 添加树"""
        print("\n[Test: Forest Add Tree]")
        forest = MerkleForest()
        
        tree = forest.add_tree("tree1", ["a", "b", "c"])
        self.assert_is_not_none(tree, "Tree created")
        self.assert_true("tree1" in forest, "Tree in forest")
        self.assert_equal(len(forest), 1, "Forest has 1 tree")
    
    def test_forest_get_tree(self):
        """测试 MerkleForest 获取树"""
        print("\n[Test: Forest Get Tree]")
        forest = MerkleForest()
        forest.add_tree("tree1", ["a", "b"])
        forest.add_tree("tree2", ["c", "d"])
        
        tree1 = forest.get_tree("tree1")
        self.assert_is_not_none(tree1, "Can get tree1")
        
        tree3 = forest.get_tree("tree3")
        self.assert_is_none(tree3, "Non-existent tree is None")
    
    def test_forest_remove_tree(self):
        """测试 MerkleForest 移除树"""
        print("\n[Test: Forest Remove Tree]")
        forest = MerkleForest()
        forest.add_tree("tree1", ["a", "b"])
        
        result = forest.remove_tree("tree1")
        self.assert_true(result, "Remove successful")
        self.assert_true("tree1" not in forest, "Tree removed")
        
        result = forest.remove_tree("nonexistent")
        self.assert_false(result, "Remove non-existent fails")
    
    def test_forest_list_trees(self):
        """测试 MerkleForest 列出树"""
        print("\n[Test: Forest List Trees]")
        forest = MerkleForest()
        forest.add_tree("tree1", ["a"])
        forest.add_tree("tree2", ["b"])
        forest.add_tree("tree3", ["c"])
        
        names = forest.list_trees()
        self.assert_equal(len(names), 3, "3 trees listed")
        self.assert_true("tree1" in names, "tree1 in list")
    
    def test_quick_root(self):
        """测试快速根哈希计算"""
        print("\n[Test: Quick Root]")
        root = MerkleUtils.quick_root(["a", "b", "c"])
        self.assert_is_not_none(root, "Returns root hash")
        self.assert_equal(len(root), 64, "SHA256 hash length")
        
        # 空列表
        empty_root = MerkleUtils.quick_root([])
        self.assert_is_none(empty_root, "Empty list returns None")
    
    def test_compare_trees(self):
        """测试比较树"""
        print("\n[Test: Compare Trees]")
        tree1 = MerkleTree(["a", "b", "c"])
        tree2 = MerkleTree(["a", "b", "c"])
        tree3 = MerkleTree(["a", "b", "d"])
        
        self.assert_true(MerkleUtils.compare_trees(tree1, tree2), 
                        "Same trees compare equal")
        self.assert_false(MerkleUtils.compare_trees(tree1, tree3),
                         "Different trees compare unequal")
    
    def test_find_differences(self):
        """测试查找差异"""
        print("\n[Test: Find Differences]")
        tree1 = MerkleTree(["a", "b", "c", "d"])
        tree2 = MerkleTree(["a", "x", "c", "y"])
        
        diffs = MerkleUtils.find_differences(tree1, tree2)
        self.assert_true(1 in diffs, "Index 1 is different")
        self.assert_true(3 in diffs, "Index 3 is different")
    
    def test_merge_trees(self):
        """测试合并树"""
        print("\n[Test: Merge Trees]")
        tree1 = MerkleTree(["a", "b"])
        tree2 = MerkleTree(["c", "d"])
        
        merged = MerkleUtils.merge_trees(tree1, tree2)
        self.assert_equal(merged.get_leaf_count(), 4, "Merged has 4 leaves")
        self.assert_true(merged.contains("a"), "Contains a")
        self.assert_true(merged.contains("d"), "Contains d")
    
    def test_estimate_proof_size(self):
        """测试证明大小估算"""
        print("\n[Test: Estimate Proof Size]")
        size_1 = MerkleUtils.estimate_proof_size(1)
        self.assert_equal(size_1, 0, "1 leaf: 0 siblings")
        
        size_2 = MerkleUtils.estimate_proof_size(2)
        self.assert_equal(size_2, 1, "2 leaves: 1 sibling")
        
        size_4 = MerkleUtils.estimate_proof_size(4)
        self.assert_equal(size_4, 2, "4 leaves: 2 siblings")
        
        size_8 = MerkleUtils.estimate_proof_size(8)
        self.assert_equal(size_8, 3, "8 leaves: 3 siblings")
        
        size_100 = MerkleUtils.estimate_proof_size(100)
        self.assert_true(size_100 >= 6, "100 leaves: >= 6 siblings")
    
    def test_create_tree_function(self):
        """测试 create_tree 便捷函数"""
        print("\n[Test: create_tree Function]")
        tree = create_tree(["a", "b", "c"])
        self.assert_is_not_none(tree, "Tree created")
        self.assert_equal(tree.get_leaf_count(), 3, "3 leaves")
    
    def test_get_root_function(self):
        """测试 get_root 便捷函数"""
        print("\n[Test: get_root Function]")
        root = get_root(["a", "b", "c"])
        self.assert_is_not_none(root, "Root returned")
        self.assert_equal(len(root), 64, "SHA256 hash length")
    
    def test_verify_proof_function(self):
        """测试 verify_proof 便捷函数"""
        print("\n[Test: verify_proof Function]")
        tree = MerkleTree(["apple", "banana"])
        proof = tree.generate_proof(0)
        root = tree.get_root_hash()
        
        is_valid = verify_proof("apple", proof, root)
        self.assert_true(is_valid, "Convenience function works")


class TestMerkleProof:
    """MerkleProof 测试类"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def assert_equal(self, actual, expected, test_name):
        if actual == expected:
            print(f"  ✓ {test_name}")
            self.passed += 1
        else:
            print(f"  ✗ {test_name}")
            print(f"    Expected: {expected}")
            print(f"    Actual: {actual}")
            self.failed += 1
    
    def assert_true(self, condition, test_name):
        if condition:
            print(f"  ✓ {test_name}")
            self.passed += 1
        else:
            print(f"  ✗ {test_name}")
            self.failed += 1
    
    def run_all_tests(self):
        print("\n" + "=" * 60)
        print("MerkleProof 测试套件")
        print("=" * 60)
        
        self.test_proof_serialization()
        self.test_proof_json()
        self.test_proof_immutable()
        self.test_proof_directions()
        
        print("\n" + "=" * 60)
        print(f"测试结果: {self.passed} 通过, {self.failed} 失败")
        print("=" * 60)
        
        return self.failed == 0
    
    def test_proof_serialization(self):
        """测试证明序列化"""
        print("\n[Test: Proof Serialization]")
        tree = MerkleTree(["a", "b", "c"])
        proof = tree.generate_proof(0)
        
        d = proof.to_dict()
        self.assert_true("leaf_hash" in d, "Dict has leaf_hash")
        self.assert_true("leaf_index" in d, "Dict has leaf_index")
        self.assert_true("siblings" in d, "Dict has siblings")
        self.assert_true("directions" in d, "Dict has directions")
        self.assert_true("hash_algorithm" in d, "Dict has hash_algorithm")
    
    def test_proof_json(self):
        """测试证明 JSON 序列化"""
        print("\n[Test: Proof JSON]")
        tree = MerkleTree(["test"])
        proof = tree.generate_proof(0)
        
        json_str = proof.to_json()
        self.assert_true(isinstance(json_str, str), "to_json returns string")
        
        restored = MerkleProof.from_json(json_str)
        self.assert_equal(restored.leaf_hash, proof.leaf_hash, "Same leaf_hash")
        self.assert_equal(restored.leaf_index, proof.leaf_index, "Same leaf_index")
    
    def test_proof_immutable(self):
        """测试证明数据不可变性（概念）"""
        print("\n[Test: Proof Data]")
        tree = MerkleTree(["x", "y", "z"])
        proof = tree.generate_proof(1)
        
        self.assert_equal(proof.leaf_index, 1, "Correct index")
        self.assert_equal(proof.hash_algorithm, "sha256", "Correct algorithm")
        self.assert_true(len(proof.siblings) == len(proof.directions),
                        "Siblings and directions match")
    
    def test_proof_directions(self):
        """测试证明方向"""
        print("\n[Test: Proof Directions]")
        tree = MerkleTree(["a", "b", "c", "d"])
        
        # 索引 0 的证明：第一个叶子，兄弟应该在右边
        proof_0 = tree.generate_proof(0)
        self.assert_true(len(proof_0.directions) > 0, "Has directions")
        
        # 索引 1 的证明：第二个叶子，兄弟应该在左边
        proof_1 = tree.generate_proof(1)
        self.assert_true(len(proof_1.directions) > 0, "Has directions")


def main():
    """运行所有测试"""
    tree_tests = TestMerkleTree()
    tree_success = tree_tests.run_all_tests()
    
    proof_tests = TestMerkleProof()
    proof_success = proof_tests.run_all_tests()
    
    total_passed = tree_tests.passed + proof_tests.passed
    total_failed = tree_tests.failed + proof_tests.failed
    
    print("\n" + "=" * 60)
    print(f"总计: {total_passed} 通过, {total_failed} 失败")
    print("=" * 60)
    
    if total_failed == 0:
        print("\n✅ 所有测试通过!")
        return 0
    else:
        print(f"\n❌ {total_failed} 个测试失败")
        return 1


if __name__ == "__main__":
    exit(main())