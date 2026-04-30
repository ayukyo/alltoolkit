# Merkle Tree Utils

默克尔树工具模块 - 提供默克尔树构建、证明生成与验证功能。

## 功能特性

- **默克尔树构建**: 从数据列表快速构建默克尔树
- **根哈希计算**: 计算并获取树的根哈希值
- **成员证明**: 生成和验证数据成员资格证明
- **增量更新**: 动态添加、删除、更新叶子节点
- **多哈希算法**: 支持 SHA256、SHA512、MD5、BLAKE2 等
- **序列化**: 树和证明的序列化与反序列化
- **零外部依赖**: 仅使用 Python 标准库

## 快速开始

```python
from merkle_tree_utils.mod import MerkleTree, MerkleProof

# 创建默克尔树
transactions = ["tx1", "tx2", "tx3", "tx4"]
tree = MerkleTree(transactions)

# 获取根哈希
root_hash = tree.get_root_hash()
print(f"Root: {root_hash}")

# 为交易生成证明
proof = tree.generate_proof(0)

# 验证证明
is_valid = MerkleProof.verify("tx1", proof, root_hash)
print(f"Valid: {is_valid}")
```

## 核心类

### MerkleTree

默克尔树的主要实现类。

```python
tree = MerkleTree(
    data=["a", "b", "c"],           # 数据列表
    hash_algorithm="sha256"          # 哈希算法
)

# 核心方法
tree.get_root_hash()                 # 获取根哈希
tree.get_leaf_count()                # 获取叶子数量
tree.get_tree_height()               # 获取树高度
tree.generate_proof(index)           # 生成证明
tree.verify_proof(data, proof)       # 验证证明

# 叶子操作
tree.add_leaf(data)                  # 添加叶子
tree.add_leaves([data1, data2])      # 批量添加
tree.update_leaf(index, new_data)    # 更新叶子
tree.remove_leaf(index)              # 删除叶子
tree.find_leaf(data)                 # 查找叶子
tree.contains(data)                  # 检查包含

# 序列化
tree.to_dict()                       # 转为字典
tree.to_json()                       # 转为 JSON
MerkleTree.from_dict(d)              # 从字典创建
MerkleTree.from_json(json_str)       # 从 JSON 创建
```

### MerkleProof

默克尔证明数据结构。

```python
# 从树生成证明
proof = tree.generate_proof(leaf_index)

# 证明属性
proof.leaf_hash                      # 叶子哈希
proof.leaf_index                     # 叶子索引
proof.siblings                       # 兄弟节点列表
proof.directions                     # 方向列表
proof.hash_algorithm                 # 哈希算法

# 验证证明
MerkleProof.verify(data, proof, root_hash)

# 序列化
proof.to_dict()
proof.to_json()
MerkleProof.from_json(json_str)
```

### MerkleForest

管理多棵默克尔树的集合。

```python
forest = MerkleForest()

forest.add_tree("block_1", ["tx1", "tx2"])
forest.get_tree("block_1")
forest.remove_tree("block_1")
forest.list_trees()
forest.get_all_roots()
```

### MerkleUtils

静态工具方法集合。

```python
MerkleUtils.quick_root(data)         # 快速计算根哈希
MerkleUtils.verify_inclusion(data, proof, root)
MerkleUtils.compare_trees(tree1, tree2)
MerkleUtils.find_differences(tree1, tree2)
MerkleUtils.merge_trees(tree1, tree2)
MerkleUtils.estimate_proof_size(leaf_count)
```

## 便捷函数

```python
from merkle_tree_utils.mod import create_tree, get_root, verify_proof

# 快速创建树
tree = create_tree(["a", "b", "c"])

# 快速获取根哈希
root = get_root(["x", "y", "z"])

# 快速验证证明
is_valid = verify_proof(data, proof, root)
```

## 支持的哈希算法

| 算法 | 输出长度 | 说明 |
|------|---------|------|
| SHA256 | 64 字符 | 默认，推荐 |
| SHA512 | 128 字符 | 更安全 |
| SHA384 | 96 字符 | 平衡 |
| SHA1 | 40 字符 | 不推荐 |
| MD5 | 32 字符 | 不推荐 |
| BLAKE2b | 64 字符 | 高性能 |
| BLAKE2s | 64 字符 | 高性能 |

```python
from merkle_tree_utils.mod import HashAlgorithm

tree = MerkleTree(data, HashAlgorithm.SHA512)
tree = MerkleTree(data, "md5")  # 字符串形式
```

## 使用场景

### 1. 区块链交易验证

```python
# 区块交易列表
transactions = ["alice->bob:10", "bob->charlie:5", ...]

# 创建默克尔树
block_tree = MerkleTree(transactions)

# 轻节点只需存储根哈希
block_header = {
    "merkle_root": block_tree.get_root_hash(),
    ...
}

# 验证特定交易
proof = block_tree.generate_proof(tx_index)
is_valid = MerkleProof.verify(transaction, proof, block_header["merkle_root"])
```

### 2. 文件完整性验证

```python
# 将文件分块
file_chunks = split_file_into_chunks(large_file)

# 创建默克尔树
file_tree = MerkleTree(file_chunks)

# 存储根哈希
stored_root = file_tree.get_root_hash()

# 后续验证
received_chunks = receive_file()
received_tree = MerkleTree(received_chunks)

if received_tree.get_root_hash() == stored_root:
    print("文件完整")
```

### 3. Git 类版本控制

```python
# 文件版本的默克尔树
versions = ["v1_content", "v2_content", "v3_content"]
version_tree = MerkleTree(versions)

# 快速比较版本
if version_tree.get_root_hash() == previous_root:
    print("无变化")
else:
    diffs = MerkleUtils.find_differences(version_tree, previous_tree)
```

## 测试

运行测试:

```bash
cd Python/merkle_tree_utils
python merkle_tree_utils_test.py
```

测试覆盖:
- 基础构建 (空树、单叶、多叶、奇数叶)
- 根哈希计算与一致性
- 多哈希算法支持
- 证明生成与验证
- 叶子操作 (增删改查)
- 序列化与反序列化
- 边界值 (Unicode、字节、空串、大数据)
- MerkleForest 多树管理
- MerkleUtils 工具方法

## 实现细节

### 默克尔树结构

默克尔树是一种二叉哈希树:
- 叶子节点存储数据的哈希
- 非叶子节点存储子节点哈希的组合哈希
- 根哈希代表整个数据集的摘要

### 证明验证过程

```
叶子 -> 组合兄弟哈希 -> 向上遍历 -> 达到根
```

对于每个层级:
- 如果当前是左节点，兄弟在右边: hash(current + sibling)
- 如果当前是右节点，兄弟在左边: hash(sibling + current)

### 哈希组合

使用字符串拼接方式组合两个哈希:
```python
combined_hash = hash(left_hash + right_hash)
```

## API 参考

详细 API 文档请参考源代码注释。

## 许可证

MIT License