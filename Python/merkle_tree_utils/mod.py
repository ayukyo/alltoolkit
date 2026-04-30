#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Python Merkle Tree Utilities
默克尔树工具模块 - 提供默克尔树构建、证明生成与验证功能

@module: merkle_tree_utils
@author: AllToolkit Contributors
@license: MIT
@version: 1.0.0

功能列表:
- 默克尔树构建: 从数据列表构建默克尔树
- 根哈希计算: 计算树的根哈希值
- 成员证明: 生成和验证数据成员资格证明
- 一致性证明: 验证树的一致性
- 增量更新: 添加、删除、更新叶子节点
- 序列化: 树的序列化与反序列化
- 多种哈希算法支持: SHA256, SHA512, MD5 等

使用示例:
    from merkle_tree_utils.mod import MerkleTree, MerkleProof
    
    # 构建默克尔树
    tree = MerkleTree(["data1", "data2", "data3", "data4"])
    root = tree.get_root_hash()
    
    # 生成证明
    proof = tree.generate_proof(0)  # 为第一个叶子生成证明
    
    # 验证证明
    is_valid = MerkleProof.verify("data1", proof, root)
"""

import hashlib
from typing import List, Optional, Union, Tuple, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import json


class HashAlgorithm(Enum):
    """支持的哈希算法"""
    SHA256 = "sha256"
    SHA512 = "sha512"
    SHA384 = "sha384"
    SHA1 = "sha1"
    MD5 = "md5"
    BLAKE2B = "blake2b"
    BLAKE2S = "blake2s"


@dataclass
class MerkleProof:
    """
    默克尔证明数据结构
    
    Attributes:
        leaf_hash: 叶子节点的哈希值
        leaf_index: 叶子在树中的索引
        siblings: 兄弟节点哈希列表（从叶子到根的路径上的兄弟节点）
        direction: 每个兄弟节点的方向（True=右兄弟，False=左兄弟）
        hash_algorithm: 使用的哈希算法
    """
    leaf_hash: str
    leaf_index: int
    siblings: List[str]
    directions: List[bool]  # True = sibling is on right, False = sibling is on left
    hash_algorithm: str = "sha256"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "leaf_hash": self.leaf_hash,
            "leaf_index": self.leaf_index,
            "siblings": self.siblings,
            "directions": self.directions,
            "hash_algorithm": self.hash_algorithm
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MerkleProof':
        """从字典创建"""
        return cls(
            leaf_hash=data["leaf_hash"],
            leaf_index=data["leaf_index"],
            siblings=data["siblings"],
            directions=data["directions"],
            hash_algorithm=data.get("hash_algorithm", "sha256")
        )
    
    def to_json(self) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> 'MerkleProof':
        """从 JSON 字符串创建"""
        return cls.from_dict(json.loads(json_str))
    
    @staticmethod
    def verify(data: Union[str, bytes], proof: 'MerkleProof', 
               root_hash: str) -> bool:
        """
        验证默克尔证明
        
        Args:
            data: 原始数据
            proof: 默克尔证明
            root_hash: 根哈希值
            
        Returns:
            验证是否通过
        """
        # 计算数据的哈希
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        hash_func = MerkleTree._get_hash_function(proof.hash_algorithm)
        current_hash = hash_func(data).hexdigest()
        
        # 验证起始哈希
        if current_hash != proof.leaf_hash:
            return False
        
        # 沿着证明路径计算
        for i, (sibling, is_right) in enumerate(zip(proof.siblings, proof.directions)):
            if is_right:
                # 兄弟在右边，当前节点在左边
                combined = current_hash + sibling
            else:
                # 兄弟在左边，当前节点在右边
                combined = sibling + current_hash
            
            current_hash = hash_func(combined.encode('utf-8')).hexdigest()
        
        return current_hash == root_hash


class MerkleTree:
    """
    默克尔树实现
    
    默克尔树是一种二叉树结构，用于高效验证大量数据的完整性。
    广泛应用于区块链、分布式文件系统、版本控制系统等场景。
    
    Features:
        - 支持多种哈希算法
        - 支持增量更新（添加、删除、修改叶子）
        - 支持成员证明生成与验证
        - 支持序列化与反序列化
        - 支持批量构建
    
    Example:
        >>> tree = MerkleTree(["a", "b", "c", "d"])
        >>> tree.get_root_hash()
        'a8b9c...'
        >>> proof = tree.generate_proof(0)
        >>> MerkleProof.verify("a", proof, tree.get_root_hash())
        True
    """
    
    def __init__(self, data: Optional[List[Union[str, bytes]]] = None,
                 hash_algorithm: Union[str, HashAlgorithm] = HashAlgorithm.SHA256):
        """
        初始化默克尔树
        
        Args:
            data: 初始数据列表（可选）
            hash_algorithm: 哈希算法
        """
        self._leaves: List[str] = []  # 叶子节点哈希
        self._raw_data: List[Union[str, bytes]] = []  # 原始数据
        self._tree: List[List[str]] = []  # 完整树结构
        self._hash_algorithm = self._normalize_algorithm(hash_algorithm)
        
        if data:
            self.build(data)
    
    @staticmethod
    def _normalize_algorithm(algorithm: Union[str, HashAlgorithm]) -> str:
        """规范化哈希算法名称"""
        if isinstance(algorithm, HashAlgorithm):
            return algorithm.value
        algorithm = algorithm.lower().replace('-', '')
        
        # 映射常见名称
        mapping = {
            'sha256': 'sha256',
            'sha512': 'sha512',
            'sha384': 'sha384',
            'sha1': 'sha1',
            'md5': 'md5',
            'blake2b': 'blake2b',
            'blake2s': 'blake2s'
        }
        return mapping.get(algorithm, 'sha256')
    
    @staticmethod
    def _get_hash_function(algorithm: str):
        """获取哈希函数"""
        functions = {
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512,
            'sha384': hashlib.sha384,
            'sha1': hashlib.sha1,
            'md5': hashlib.md5,
            'blake2b': hashlib.blake2b,
            'blake2s': hashlib.blake2s
        }
        return functions.get(algorithm, hashlib.sha256)
    
    def _hash(self, data: Union[str, bytes]) -> str:
        """计算数据的哈希值"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        hash_func = self._get_hash_function(self._hash_algorithm)
        return hash_func(data).hexdigest()
    
    def _hash_pair(self, left: str, right: str) -> str:
        """计算两个节点哈希的组合哈希"""
        combined = left + right
        return self._hash(combined)
    
    def build(self, data: List[Union[str, bytes]]) -> None:
        """
        从数据列表构建默克尔树
        
        Args:
            data: 数据列表
        """
        if not data:
            self._leaves = []
            self._raw_data = []
            self._tree = []
            return
        
        self._raw_data = list(data)
        self._leaves = [self._hash(d) for d in data]
        self._build_tree()
    
    def _build_tree(self) -> None:
        """构建树结构"""
        if not self._leaves:
            self._tree = []
            return
        
        # 树的每一层，从叶子层开始
        self._tree = [self._leaves.copy()]
        
        current_level = self._leaves.copy()
        
        while len(current_level) > 1:
            next_level = []
            
            # 成对处理
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                
                if i + 1 < len(current_level):
                    right = current_level[i + 1]
                else:
                    # 奇数个节点，复制最后一个节点
                    right = left
                
                parent = self._hash_pair(left, right)
                next_level.append(parent)
            
            self._tree.append(next_level)
            current_level = next_level
    
    def get_root_hash(self) -> Optional[str]:
        """
        获取默克尔树的根哈希
        
        Returns:
            根哈希值，空树返回 None
        """
        if not self._tree:
            return None
        return self._tree[-1][0] if self._tree[-1] else None
    
    def get_leaf_count(self) -> int:
        """获取叶子节点数量"""
        return len(self._leaves)
    
    def get_tree_height(self) -> int:
        """获取树的高度"""
        return len(self._tree)
    
    def get_leaf_hash(self, index: int) -> Optional[str]:
        """
        获取指定索引的叶子哈希
        
        Args:
            index: 叶子索引
            
        Returns:
            叶子哈希值
        """
        if 0 <= index < len(self._leaves):
            return self._leaves[index]
        return None
    
    def get_leaf_data(self, index: int) -> Optional[Union[str, bytes]]:
        """
        获取指定索引的原始数据
        
        Args:
            index: 叶子索引
            
        Returns:
            原始数据
        """
        if 0 <= index < len(self._raw_data):
            return self._raw_data[index]
        return None
    
    def generate_proof(self, index: int) -> Optional[MerkleProof]:
        """
        为指定叶子生成默克尔证明
        
        Args:
            index: 叶子索引
            
        Returns:
            默克尔证明对象
        """
        if not (0 <= index < len(self._leaves)):
            return None
        
        siblings = []
        directions = []
        
        current_index = index
        
        # 从叶子层向上遍历
        for level in range(len(self._tree) - 1):
            current_level = self._tree[level]
            
            # 确定兄弟节点
            if current_index % 2 == 0:
                # 当前节点是左节点
                sibling_index = current_index + 1
                if sibling_index < len(current_level):
                    siblings.append(current_level[sibling_index])
                    directions.append(True)  # 兄弟在右边
                else:
                    # 奇数情况，兄弟是自己
                    siblings.append(current_level[current_index])
                    directions.append(True)
            else:
                # 当前节点是右节点
                sibling_index = current_index - 1
                siblings.append(current_level[sibling_index])
                directions.append(False)  # 兄弟在左边
            
            # 移动到父节点
            current_index = current_index // 2
        
        return MerkleProof(
            leaf_hash=self._leaves[index],
            leaf_index=index,
            siblings=siblings,
            directions=directions,
            hash_algorithm=self._hash_algorithm
        )
    
    def verify_proof(self, data: Union[str, bytes], proof: MerkleProof) -> bool:
        """
        验证数据是否在树中
        
        Args:
            data: 原始数据
            proof: 默克尔证明
            
        Returns:
            验证结果
        """
        root_hash = self.get_root_hash()
        if root_hash is None:
            return False
        return MerkleProof.verify(data, proof, root_hash)
    
    def add_leaf(self, data: Union[str, bytes]) -> int:
        """
        添加一个叶子节点
        
        Args:
            data: 要添加的数据
            
        Returns:
            新叶子的索引
        """
        leaf_hash = self._hash(data)
        self._leaves.append(leaf_hash)
        self._raw_data.append(data)
        self._build_tree()
        return len(self._leaves) - 1
    
    def add_leaves(self, data_list: List[Union[str, bytes]]) -> List[int]:
        """
        批量添加叶子节点
        
        Args:
            data_list: 数据列表
            
        Returns:
            新叶子的索引列表
        """
        indices = []
        start_index = len(self._leaves)
        
        for data in data_list:
            leaf_hash = self._hash(data)
            self._leaves.append(leaf_hash)
            self._raw_data.append(data)
            indices.append(len(self._leaves) - 1)
        
        self._build_tree()
        return indices
    
    def update_leaf(self, index: int, new_data: Union[str, bytes]) -> bool:
        """
        更新指定叶子节点的数据
        
        Args:
            index: 叶子索引
            new_data: 新数据
            
        Returns:
            是否更新成功
        """
        if not (0 <= index < len(self._leaves)):
            return False
        
        self._leaves[index] = self._hash(new_data)
        self._raw_data[index] = new_data
        self._build_tree()
        return True
    
    def remove_leaf(self, index: int) -> bool:
        """
        移除指定叶子节点
        
        Args:
            index: 叶子索引
            
        Returns:
            是否移除成功
        """
        if not (0 <= index < len(self._leaves)):
            return False
        
        self._leaves.pop(index)
        self._raw_data.pop(index)
        self._build_tree()
        return True
    
    def find_leaf(self, data: Union[str, bytes]) -> int:
        """
        查找数据对应的叶子索引
        
        Args:
            data: 要查找的数据
            
        Returns:
            叶子索引，未找到返回 -1
        """
        target_hash = self._hash(data)
        for i, leaf_hash in enumerate(self._leaves):
            if leaf_hash == target_hash:
                return i
        return -1
    
    def contains(self, data: Union[str, bytes]) -> bool:
        """
        检查数据是否在树中
        
        Args:
            data: 要检查的数据
            
        Returns:
            是否存在
        """
        return self.find_leaf(data) != -1
    
    def get_proof_for_data(self, data: Union[str, bytes]) -> Optional[MerkleProof]:
        """
        为指定数据生成证明
        
        Args:
            data: 要证明的数据
            
        Returns:
            默克尔证明
        """
        index = self.find_leaf(data)
        if index == -1:
            return None
        return self.generate_proof(index)
    
    def to_dict(self) -> Dict[str, Any]:
        """将树序列化为字典"""
        return {
            "algorithm": self._hash_algorithm,
            "leaves": self._leaves,
            "raw_data": [d.decode('utf-8') if isinstance(d, bytes) else d 
                         for d in self._raw_data],
            "tree": self._tree
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MerkleTree':
        """从字典创建树"""
        tree = cls(hash_algorithm=data.get("algorithm", "sha256"))
        tree._leaves = data["leaves"]
        tree._raw_data = data["raw_data"]
        tree._tree = data["tree"]
        return tree
    
    def to_json(self) -> str:
        """将树序列化为 JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'MerkleTree':
        """从 JSON 字符串创建树"""
        return cls.from_dict(json.loads(json_str))
    
    def get_tree_structure(self) -> List[List[str]]:
        """获取完整树结构（用于调试/可视化）"""
        return self._tree.copy()
    
    def __len__(self) -> int:
        return len(self._leaves)
    
    def __repr__(self) -> str:
        root = self.get_root_hash()
        root_display = root[:16] + "..." if root else "None"
        return f"MerkleTree(leaves={len(self._leaves)}, root={root_display}, algo={self._hash_algorithm})"


class MerkleForest:
    """
    默克尔森林 - 管理多棵默克尔树
    
    用于需要维护多个独立默克尔树的场景，
    如多区块区块链、多文件版本控制等。
    """
    
    def __init__(self, hash_algorithm: Union[str, HashAlgorithm] = HashAlgorithm.SHA256):
        self._trees: Dict[str, MerkleTree] = {}
        self._hash_algorithm = hash_algorithm
    
    def add_tree(self, name: str, data: List[Union[str, bytes]]) -> MerkleTree:
        """
        添加一棵新的默克尔树
        
        Args:
            name: 树名称
            data: 数据列表
            
        Returns:
            创建的默克尔树
        """
        tree = MerkleTree(data, self._hash_algorithm)
        self._trees[name] = tree
        return tree
    
    def get_tree(self, name: str) -> Optional[MerkleTree]:
        """获取指定名称的树"""
        return self._trees.get(name)
    
    def remove_tree(self, name: str) -> bool:
        """移除指定名称的树"""
        if name in self._trees:
            del self._trees[name]
            return True
        return False
    
    def get_all_roots(self) -> Dict[str, Optional[str]]:
        """获取所有树的根哈希"""
        return {name: tree.get_root_hash() for name, tree in self._trees.items()}
    
    def list_trees(self) -> List[str]:
        """列出所有树名称"""
        return list(self._trees.keys())
    
    def __len__(self) -> int:
        return len(self._trees)
    
    def __contains__(self, name: str) -> bool:
        return name in self._trees


class MerkleUtils:
    """默克尔树静态工具方法集合"""
    
    @staticmethod
    def quick_root(data: List[Union[str, bytes]], 
                   algorithm: str = "sha256") -> Optional[str]:
        """
        快速计算数据列表的默克尔根哈希
        
        Args:
            data: 数据列表
            algorithm: 哈希算法
            
        Returns:
            根哈希值
        """
        tree = MerkleTree(data, algorithm)
        return tree.get_root_hash()
    
    @staticmethod
    def verify_inclusion(data: Union[str, bytes], proof: MerkleProof,
                        root_hash: str) -> bool:
        """
        验证数据是否包含在树中（静态方法）
        
        Args:
            data: 原始数据
            proof: 默克尔证明
            root_hash: 根哈希
            
        Returns:
            验证结果
        """
        return MerkleProof.verify(data, proof, root_hash)
    
    @staticmethod
    def compare_trees(tree1: MerkleTree, tree2: MerkleTree) -> bool:
        """
        比较两棵树是否相同
        
        Args:
            tree1: 第一棵树
            tree2: 第二棵树
            
        Returns:
            是否相同
        """
        return tree1.get_root_hash() == tree2.get_root_hash()
    
    @staticmethod
    def find_differences(tree1: MerkleTree, tree2: MerkleTree) -> List[int]:
        """
        找出两棵树之间的差异索引
        
        Args:
            tree1: 第一棵树
            tree2: 第二棵树
            
        Returns:
            差异索引列表
        """
        # 假设两棵树索引对齐
        max_len = max(len(tree1), len(tree2))
        differences = []
        
        for i in range(max_len):
            hash1 = tree1.get_leaf_hash(i)
            hash2 = tree2.get_leaf_hash(i)
            
            if hash1 != hash2:
                differences.append(i)
        
        return differences
    
    @staticmethod
    def merge_trees(tree1: MerkleTree, tree2: MerkleTree) -> MerkleTree:
        """
        合并两棵树
        
        Args:
            tree1: 第一棵树
            tree2: 第二棵树
            
        Returns:
            合并后的新树
        """
        if tree1._hash_algorithm != tree2._hash_algorithm:
            raise ValueError("Cannot merge trees with different hash algorithms")
        
        combined_data = tree1._raw_data + tree2._raw_data
        return MerkleTree(combined_data, tree1._hash_algorithm)
    
    @staticmethod
    def calculate_sibling_path(leaf_index: int, leaf_count: int) -> List[Tuple[int, bool]]:
        """
        计算从叶子到根的兄弟节点路径
        
        Args:
            leaf_index: 叶子索引
            leaf_count: 叶子总数
            
        Returns:
            路径列表，每个元素为 (兄弟索引, 是否在右边)
        """
        path = []
        current_index = leaf_index
        current_count = leaf_count
        
        while current_count > 1:
            if current_index % 2 == 0:
                # 当前是左节点，兄弟在右边
                sibling_index = current_index + 1
                if sibling_index >= current_count:
                    sibling_index = current_index  # 复制自己
                path.append((sibling_index, True))
            else:
                # 当前是右节点，兄弟在左边
                sibling_index = current_index - 1
                path.append((sibling_index, False))
            
            current_index = current_index // 2
            current_count = (current_count + 1) // 2
        
        return path
    
    @staticmethod
    def estimate_proof_size(leaf_count: int) -> int:
        """
        估算证明的大小（兄弟节点数量）
        
        Args:
            leaf_count: 叶子数量
            
        Returns:
            证明中的兄弟节点数量
        """
        if leaf_count <= 1:
            return 0
        
        import math
        return math.ceil(math.log2(leaf_count))


# 便捷函数
def create_tree(data: List[Union[str, bytes]], 
                algorithm: str = "sha256") -> MerkleTree:
    """
    创建默克尔树的便捷函数
    
    Args:
        data: 数据列表
        algorithm: 哈希算法
        
    Returns:
        默克尔树实例
    """
    return MerkleTree(data, algorithm)


def get_root(data: List[Union[str, bytes]], 
             algorithm: str = "sha256") -> Optional[str]:
    """
    快速获取默克尔根哈希的便捷函数
    
    Args:
        data: 数据列表
        algorithm: 哈希算法
        
    Returns:
        根哈希值
    """
    return MerkleUtils.quick_root(data, algorithm)


def verify_proof(data: Union[str, bytes], proof: MerkleProof,
                root_hash: str) -> bool:
    """
    验证默克尔证明的便捷函数
    
    Args:
        data: 原始数据
        proof: 默克尔证明
        root_hash: 根哈希
        
    Returns:
        验证结果
    """
    return MerkleProof.verify(data, proof, root_hash)


if __name__ == "__main__":
    # 简单演示
    print("Merkle Tree Demo")
    print("=" * 50)
    
    # 创建树
    data = ["apple", "banana", "cherry", "date", "elderberry"]
    tree = MerkleTree(data)
    
    print(f"Data: {data}")
    print(f"Leaf count: {tree.get_leaf_count()}")
    print(f"Tree height: {tree.get_tree_height()}")
    print(f"Root hash: {tree.get_root_hash()}")
    print()
    
    # 生成证明
    proof = tree.generate_proof(0)
    print(f"Proof for 'apple':")
    print(f"  Leaf hash: {proof.leaf_hash}")
    print(f"  Siblings: {len(proof.siblings)}")
    print()
    
    # 验证证明
    is_valid = MerkleProof.verify("apple", proof, tree.get_root_hash())
    print(f"Verification: {is_valid}")
    
    # 尝试验证不在树中的数据
    is_invalid = MerkleProof.verify("grape", proof, tree.get_root_hash())
    print(f"Invalid data verification: {is_invalid}")