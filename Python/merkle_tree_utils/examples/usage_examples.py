#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Merkle Tree Utils 使用示例
默克尔树工具模块使用示例

运行示例:
    cd Python/merkle_tree_utils/examples
    python usage_examples.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    MerkleTree, MerkleProof, MerkleForest, MerkleUtils,
    HashAlgorithm, create_tree, get_root, verify_proof
)


def print_section(title: str):
    """打印分节标题"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def example_basic_usage():
    """基础用法示例"""
    print_section("1. 基础用法 - 创建和验证默克尔树")
    
    # 创建默克尔树
    transactions = [
        "alice -> bob: 10 BTC",
        "bob -> charlie: 5 BTC",
        "charlie -> dave: 2 BTC",
        "dave -> eve: 1 BTC"
    ]
    
    tree = MerkleTree(transactions)
    
    print(f"交易数量: {tree.get_leaf_count()}")
    print(f"树高度: {tree.get_tree_height()}")
    print(f"根哈希: {tree.get_root_hash()}")
    print()
    
    # 为第一笔交易生成证明
    proof = tree.generate_proof(0)
    print(f"交易 #0 的证明:")
    print(f"  叶子哈希: {proof.leaf_hash[:32]}...")
    print(f"  兄弟节点数: {len(proof.siblings)}")
    
    # 验证证明
    is_valid = MerkleProof.verify(transactions[0], proof, tree.get_root_hash())
    print(f"\n验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")


def example_different_algorithms():
    """不同哈希算法示例"""
    print_section("2. 不同哈希算法")
    
    data = ["block1", "block2", "block3"]
    
    algorithms = [
        HashAlgorithm.SHA256,
        HashAlgorithm.SHA512,
        HashAlgorithm.MD5,
        HashAlgorithm.BLAKE2B
    ]
    
    print(f"数据: {data}")
    print()
    
    for algo in algorithms:
        tree = MerkleTree(data, algo)
        root = tree.get_root_hash()
        hash_len = len(root) if root else 0
        print(f"{algo.value:10} -> 根哈希 (长度 {hash_len}): {root[:40]}...")


def example_membership_proof():
    """成员证明示例"""
    print_section("3. 成员证明 - 验证数据是否在树中")
    
    # 模拟文件系统
    files = [
        "document.pdf",
        "image.png",
        "video.mp4",
        "audio.mp3",
        "archive.zip"
    ]
    
    tree = MerkleTree(files)
    root = tree.get_root_hash()
    
    print("文件列表:", files)
    print(f"默克尔根: {root[:40]}...")
    print()
    
    # 验证文件存在
    test_file = "image.png"
    proof = tree.get_proof_for_data(test_file)
    
    if proof:
        print(f"验证 '{test_file}':")
        is_valid = verify_proof(test_file, proof, root)
        print(f"  结果: {'✅ 存在' if is_valid else '❌ 不存在'}")
    
    # 验证不存在的文件
    fake_file = "nonexistent.txt"
    fake_proof = tree.get_proof_for_data(fake_file)
    print(f"\n验证 '{fake_file}':")
    print(f"  结果: {'❌ 不存在' if fake_proof is None else '✅ 存在'}")


def example_data_integrity():
    """数据完整性验证示例"""
    print_section("4. 数据完整性验证")
    
    # 模拟数据块
    original_data = ["chunk1", "chunk2", "chunk3", "chunk4", "chunk5"]
    tree = MerkleTree(original_data)
    original_root = tree.get_root_hash()
    
    print("原始数据:", original_data)
    print(f"原始根哈希: {original_root[:40]}...")
    print()
    
    # 模拟数据传输后的验证
    received_data = ["chunk1", "chunk2", "chunk3", "chunk4", "chunk5"]
    
    # 方法1: 重建树比较根哈希
    received_tree = MerkleTree(received_data)
    received_root = received_tree.get_root_hash()
    
    print("方法1: 重建树比较")
    print(f"  收到的根哈希: {received_root[:40]}...")
    print(f"  根哈希匹配: {'✅ 是' if original_root == received_root else '❌ 否'}")
    
    # 方法2: 使用单独的证明验证
    print("\n方法2: 使用证明验证每个块")
    for i, chunk in enumerate(received_data):
        proof = tree.generate_proof(i)
        is_valid = verify_proof(chunk, proof, original_root)
        print(f"  块 {i} ({chunk}): {'✅ 有效' if is_valid else '❌ 无效'}")
    
    # 模拟数据篡改
    print("\n模拟数据篡改:")
    tampered_data = ["chunk1", "chunk2", "TAMPERED!", "chunk4", "chunk5"]
    tampered_tree = MerkleTree(tampered_data)
    tampered_root = tampered_tree.get_root_hash()
    
    print(f"  篡改后的根哈希: {tampered_root[:40]}...")
    print(f"  根哈希匹配: {'✅ 是' if original_root == tampered_root else '❌ 否'}")


def example_incremental_updates():
    """增量更新示例"""
    print_section("5. 增量更新 - 动态修改树")
    
    # 初始数据
    data = ["entry1", "entry2", "entry3"]
    tree = MerkleTree(data)
    
    print("初始状态:")
    print(f"  数据: {data}")
    print(f"  叶子数: {tree.get_leaf_count()}")
    print(f"  根哈希: {tree.get_root_hash()[:40]}...")
    
    # 添加新叶子
    print("\n添加 'entry4':")
    index = tree.add_leaf("entry4")
    print(f"  新索引: {index}")
    print(f"  叶子数: {tree.get_leaf_count()}")
    print(f"  根哈希: {tree.get_root_hash()[:40]}...")
    
    # 批量添加
    print("\n批量添加 ['entry5', 'entry6']:")
    indices = tree.add_leaves(["entry5", "entry6"])
    print(f"  新索引: {indices}")
    print(f"  叶子数: {tree.get_leaf_count()}")
    
    # 更新叶子
    print("\n更新索引 1 为 'updated_entry':")
    tree.update_leaf(1, "updated_entry")
    print(f"  数据[1]: {tree.get_leaf_data(1)}")
    print(f"  根哈希: {tree.get_root_hash()[:40]}...")
    
    # 删除叶子
    print("\n删除索引 2:")
    tree.remove_leaf(2)
    print(f"  叶子数: {tree.get_leaf_count()}")
    print(f"  根哈希: {tree.get_root_hash()[:40]}...")


def example_serialization():
    """序列化示例"""
    print_section("6. 序列化 - 保存和恢复树")
    
    # 创建树
    data = ["block_a", "block_b", "block_c", "block_d"]
    original_tree = MerkleTree(data)
    
    print("原始树:")
    print(f"  数据: {data}")
    print(f"  根哈希: {original_tree.get_root_hash()[:40]}...")
    
    # 序列化为字典
    tree_dict = original_tree.to_dict()
    print(f"\n序列化为字典 (键: {list(tree_dict.keys())})")
    
    # 序列化为 JSON
    json_str = original_tree.to_json()
    print(f"序列化为 JSON (长度: {len(json_str)} 字符)")
    
    # 从字典恢复
    restored_from_dict = MerkleTree.from_dict(tree_dict)
    print(f"\n从字典恢复:")
    print(f"  根哈希: {restored_from_dict.get_root_hash()[:40]}...")
    print(f"  根哈希匹配: {'✅ 是' if original_tree.get_root_hash() == restored_from_dict.get_root_hash() else '❌ 否'}")
    
    # 从 JSON 恢复
    restored_from_json = MerkleTree.from_json(json_str)
    print(f"\n从 JSON 恢复:")
    print(f"  根哈希: {restored_from_json.get_root_hash()[:40]}...")
    print(f"  根哈希匹配: {'✅ 是' if original_tree.get_root_hash() == restored_from_json.get_root_hash() else '❌ 否'}")


def example_proof_serialization():
    """证明序列化示例"""
    print_section("7. 证明序列化 - 导出和导入证明")
    
    # 创建树并生成证明
    data = ["transaction_001", "transaction_002", "transaction_003"]
    tree = MerkleTree(data)
    proof = tree.generate_proof(0)
    
    print("原始证明:")
    print(f"  叶子索引: {proof.leaf_index}")
    print(f"  叶子哈希: {proof.leaf_hash[:32]}...")
    print(f"  兄弟节点数: {len(proof.siblings)}")
    
    # 序列化
    proof_dict = proof.to_dict()
    print(f"\n序列化为字典 (键: {list(proof_dict.keys())})")
    
    json_str = proof.to_json()
    print(f"序列化为 JSON:")
    print(f"  {json_str[:100]}...")
    
    # 反序列化
    restored_proof = MerkleProof.from_json(json_str)
    print(f"\n从 JSON 恢复:")
    print(f"  叶子索引: {restored_proof.leaf_index}")
    print(f"  叶子哈希: {restored_proof.leaf_hash[:32]}...")
    
    # 验证恢复的证明
    is_valid = verify_proof(data[0], restored_proof, tree.get_root_hash())
    print(f"  验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")


def example_merkle_forest():
    """MerkleForest 示例"""
    print_section("8. MerkleForest - 管理多棵树")
    
    # 创建森林
    forest = MerkleForest()
    
    # 添加不同的树
    forest.add_tree("blockchain_block_1", ["tx1", "tx2", "tx3"])
    forest.add_tree("blockchain_block_2", ["tx4", "tx5", "tx6", "tx7"])
    forest.add_tree("file_versions", ["v1", "v2", "v3", "v4", "v5"])
    
    print("森林中的树:")
    for name in forest.list_trees():
        tree = forest.get_tree(name)
        print(f"  {name}: {tree.get_leaf_count()} 个叶子, 根哈希: {tree.get_root_hash()[:32]}...")
    
    # 获取所有根
    print("\n所有树的根哈希:")
    roots = forest.get_all_roots()
    for name, root in roots.items():
        print(f"  {name}: {root[:32]}...")
    
    # 从树中获取证明
    block1 = forest.get_tree("blockchain_block_1")
    proof = block1.generate_proof(0)
    print(f"\nblockchain_block_1 交易 #0 的证明:")
    print(f"  叶子哈希: {proof.leaf_hash[:32]}...")


def example_convenience_functions():
    """便捷函数示例"""
    print_section("9. 便捷函数")
    
    # create_tree - 快速创建
    tree = create_tree(["a", "b", "c"])
    print(f"create_tree(['a', 'b', 'c'])")
    print(f"  叶子数: {tree.get_leaf_count()}")
    print(f"  根哈希: {tree.get_root_hash()[:40]}...")
    
    # get_root - 快速获取根哈希
    root = get_root(["x", "y", "z"])
    print(f"\nget_root(['x', 'y', 'z'])")
    print(f"  结果: {root[:40]}...")
    
    # verify_proof - 快速验证
    tree = MerkleTree(["hello", "world"])
    proof = tree.generate_proof(0)
    is_valid = verify_proof("hello", proof, tree.get_root_hash())
    print(f"\nverify_proof('hello', proof, root)")
    print(f"  结果: {'✅ 有效' if is_valid else '❌ 无效'}")


def example_blockchain_simulation():
    """区块链模拟示例"""
    print_section("10. 区块链模拟 - 简化的区块验证")
    
    class SimpleBlock:
        def __init__(self, index, transactions, prev_root=None):
            self.index = index
            self.transactions = transactions
            self.merkle_tree = MerkleTree(transactions)
            self.merkle_root = self.merkle_tree.get_root_hash()
            self.prev_root = prev_root
        
        def __repr__(self):
            return f"Block #{self.index} (root: {self.merkle_root[:16]}...)"
    
    # 创建区块链
    print("创建简单的区块链:")
    blocks = []
    
    # 创世区块
    genesis = SimpleBlock(0, ["genesis_tx"])
    blocks.append(genesis)
    print(f"  创世区块: {genesis}")
    
    # 后续区块
    for i in range(1, 4):
        transactions = [f"tx_{i}_1", f"tx_{i}_2", f"tx_{i}_3"]
        block = SimpleBlock(i, transactions, blocks[-1].merkle_root)
        blocks.append(block)
        print(f"  区块 #{i}: {block}")
    
    print("\n验证交易:")
    # 验证区块 2 的第二笔交易
    block_2 = blocks[2]
    tx_index = 1
    tx = block_2.transactions[tx_index]
    
    proof = block_2.merkle_tree.generate_proof(tx_index)
    is_valid = verify_proof(tx, proof, block_2.merkle_root)
    
    print(f"  区块 #2 交易 #{tx_index}: '{tx}'")
    print(f"  默克尔根: {block_2.merkle_root[:32]}...")
    print(f"  验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")


def example_file_integrity():
    """文件完整性检查示例"""
    print_section("11. 文件完整性检查 - 模拟")
    
    # 模拟文件块
    files = {
        "readme.txt": "This is the readme file content.",
        "config.json": '{"version": "1.0", "debug": false}',
        "data.csv": "id,name,value\n1,test,100\n2,demo,200"
    }
    
    # 为每个文件创建默克尔树
    print("文件完整性记录:")
    file_trees = {}
    
    for filename, content in files.items():
        # 将文件内容分块
        chunks = [content[i:i+10] for i in range(0, len(content), 10)]
        tree = MerkleTree(chunks)
        file_trees[filename] = tree
        
        print(f"\n  {filename}:")
        print(f"    块数: {len(chunks)}")
        print(f"    根哈希: {tree.get_root_hash()[:32]}...")
    
    # 验证文件完整性
    print("\n\n验证文件完整性:")
    test_file = "config.json"
    test_content = files[test_file]
    
    tree = file_trees[test_file]
    original_root = tree.get_root_hash()
    
    # 正常文件
    chunks = [test_content[i:i+10] for i in range(0, len(test_content), 10)]
    new_tree = MerkleTree(chunks)
    
    print(f"  {test_file} (原始):")
    print(f"    根哈希匹配: {'✅ 是' if new_tree.get_root_hash() == original_root else '❌ 否'}")
    
    # 篡改的文件
    tampered_content = test_content.replace("1.0", "9.9")
    tampered_chunks = [tampered_content[i:i+10] for i in range(0, len(tampered_content), 10)]
    tampered_tree = MerkleTree(tampered_chunks)
    
    print(f"  {test_file} (篡改):")
    print(f"    根哈希匹配: {'✅ 是' if tampered_tree.get_root_hash() == original_root else '❌ 否'}")


def example_performance():
    """性能示例"""
    print_section("12. 性能测试 - 大规模数据")
    
    import time
    
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        data = [f"item_{i}" for i in range(size)]
        
        # 构建树
        start = time.time()
        tree = MerkleTree(data)
        build_time = time.time() - start
        
        # 生成证明
        start = time.time()
        proof = tree.generate_proof(size // 2)
        proof_time = time.time() - start
        
        # 验证证明
        start = time.time()
        is_valid = verify_proof(data[size // 2], proof, tree.get_root_hash())
        verify_time = time.time() - start
        
        print(f"\n{size} 个叶子:")
        print(f"  构建时间: {build_time*1000:.2f} ms")
        print(f"  证明生成时间: {proof_time*1000:.4f} ms")
        print(f"  证明验证时间: {verify_time*1000:.4f} ms")
        print(f"  树高度: {tree.get_tree_height()}")
        print(f"  证明大小: {len(proof.siblings)} 个兄弟节点")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("  Merkle Tree Utils 使用示例")
    print("=" * 60)
    
    example_basic_usage()
    example_different_algorithms()
    example_membership_proof()
    example_data_integrity()
    example_incremental_updates()
    example_serialization()
    example_proof_serialization()
    example_merkle_forest()
    example_convenience_functions()
    example_blockchain_simulation()
    example_file_integrity()
    example_performance()
    
    print("\n" + "=" * 60)
    print("  示例演示完成!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()