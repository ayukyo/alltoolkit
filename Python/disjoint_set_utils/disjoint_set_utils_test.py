"""
并查集工具模块测试
"""

import sys
import os
import unittest

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    DisjointSet,
    WeightedDisjointSet,
    UnionFind,
    connected_components,
    detect_cycle_undirected,
    kruskal_mst,
    accounts_merge
)


class TestDisjointSet(unittest.TestCase):
    """DisjointSet 测试"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        ds = DisjointSet[int]()
        
        # 测试初始状态
        self.assertEqual(len(ds), 0)
        self.assertEqual(ds.count_sets(), 0)
        
        # 添加元素
        ds.make_set(1)
        self.assertEqual(len(ds), 1)
        self.assertEqual(ds.count_sets(), 1)
        self.assertIn(1, ds)
        
    def test_union_and_find(self):
        """测试合并和查找"""
        ds = DisjointSet[int]()
        
        ds.union(1, 2)
        self.assertTrue(ds.connected(1, 2))
        self.assertEqual(ds.count_sets(), 1)
        
        ds.union(3, 4)
        self.assertEqual(ds.count_sets(), 2)
        self.assertTrue(ds.connected(3, 4))
        self.assertFalse(ds.connected(1, 3))
        
        ds.union(2, 3)
        self.assertEqual(ds.count_sets(), 1)
        self.assertTrue(ds.connected(1, 4))
        
    def test_set_size(self):
        """测试集合大小"""
        ds = DisjointSet[int]()
        
        ds.union(1, 2)
        self.assertEqual(ds.set_size(1), 2)
        self.assertEqual(ds.set_size(2), 2)
        
        ds.union(3, 4)
        ds.union(2, 3)
        
        self.assertEqual(ds.set_size(1), 4)
        self.assertEqual(ds.set_size(4), 4)
        
    def test_get_sets(self):
        """测试获取所有集合"""
        ds = DisjointSet[int]()
        
        ds.union(1, 2)
        ds.union(3, 4)
        
        sets = ds.get_sets()
        self.assertEqual(len(sets), 2)
        
        # 验证集合内容
        all_elements = set()
        for s in sets.values():
            all_elements.update(s)
        self.assertEqual(all_elements, {1, 2, 3, 4})
        
    def test_string_elements(self):
        """测试字符串元素"""
        ds = DisjointSet[str]()
        
        ds.union("a", "b")
        ds.union("b", "c")
        
        self.assertTrue(ds.connected("a", "c"))
        self.assertFalse(ds.connected("a", "d"))
        
    def test_duplicate_union(self):
        """测试重复合并"""
        ds = DisjointSet[int]()
        
        self.assertTrue(ds.union(1, 2))
        self.assertFalse(ds.union(1, 2))  # 已在同一集合
        self.assertFalse(ds.union(2, 1))  # 反向也一样
        
    def test_repr(self):
        """测试字符串表示"""
        ds = DisjointSet[int]()
        ds.union(1, 2)
        
        repr_str = repr(ds)
        self.assertIn("elements=2", repr_str)
        self.assertIn("sets=1", repr_str)


class TestWeightedDisjointSet(unittest.TestCase):
    """WeightedDisjointSet 测试"""
    
    def test_basic_weight_operations(self):
        """测试基本权重操作"""
        wds = WeightedDisjointSet[str]()
        
        # B = A + 2 (union(A, B, 2) 表示 B 相对于 A 的偏移为 2)
        wds.union_with_weight('A', 'B', 2)
        
        # C = B + 3
        wds.union_with_weight('B', 'C', 3)
        
        # C = A + 5
        weight = wds.get_weight('A', 'C')  # C 相对于 A
        self.assertEqual(weight, 5)
        
    def test_transitive_weight(self):
        """测试传递权重计算"""
        wds = WeightedDisjointSet[int]()
        
        # 2 = 1 + 10 (union(1, 2, 10))
        wds.union_with_weight(1, 2, 10)
        # 3 = 2 + 20
        wds.union_with_weight(2, 3, 20)
        # 4 = 3 + 30
        wds.union_with_weight(3, 4, 30)
        
        # 4 = 1 + 60
        self.assertEqual(wds.get_weight(1, 4), 60)
        self.assertEqual(wds.get_weight(4, 1), -60)
        
    def test_unrelated_elements(self):
        """测试不相关元素"""
        wds = WeightedDisjointSet[int]()
        
        wds.union_with_weight(1, 2, 5)
        wds.union_with_weight(3, 4, 3)
        
        # 1 和 3 不在同一集合
        self.assertIsNone(wds.get_weight(1, 3))


class TestUnionFind(unittest.TestCase):
    """UnionFind 测试"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        uf = UnionFind(5)
        
        self.assertEqual(uf.count_sets(), 5)
        self.assertTrue(uf.connected(0, 0))
        self.assertFalse(uf.connected(0, 1))
        
    def test_union_operations(self):
        """测试合并操作"""
        uf = UnionFind(5)
        
        uf.union(0, 1)
        self.assertTrue(uf.connected(0, 1))
        self.assertEqual(uf.count_sets(), 4)
        
        uf.union(1, 2)
        self.assertTrue(uf.connected(0, 2))
        self.assertEqual(uf.count_sets(), 3)
        
    def test_set_size(self):
        """测试集合大小"""
        uf = UnionFind(5)
        
        uf.union(0, 1)
        uf.union(1, 2)
        
        self.assertEqual(uf.set_size(0), 3)
        self.assertEqual(uf.set_size(3), 1)
        
    def test_reset(self):
        """测试重置"""
        uf = UnionFind(5)
        uf.union(0, 1)
        uf.union(2, 3)
        
        uf.reset()
        
        self.assertEqual(uf.count_sets(), 5)
        self.assertFalse(uf.connected(0, 1))
        
    def test_repr(self):
        """测试字符串表示"""
        uf = UnionFind(5)
        repr_str = repr(uf)
        self.assertIn("elements=5", repr_str)


class TestConnectedComponents(unittest.TestCase):
    """connected_components 测试"""
    
    def test_single_component(self):
        """测试单个连通分量"""
        n = 4
        edges = [(0, 1), (1, 2), (2, 3)]
        components = connected_components(n, edges)
        
        self.assertEqual(len(components), 1)
        self.assertEqual(set(components[0]), {0, 1, 2, 3})
        
    def test_multiple_components(self):
        """测试多个连通分量"""
        n = 6
        edges = [(0, 1), (2, 3), (4, 5)]
        components = connected_components(n, edges)
        
        self.assertEqual(len(components), 3)
        
        # 验证每个分量
        all_nodes = set()
        for comp in components:
            self.assertEqual(len(comp), 2)
            all_nodes.update(comp)
        self.assertEqual(all_nodes, {0, 1, 2, 3, 4, 5})
        
    def test_isolated_nodes(self):
        """测试孤立节点"""
        n = 5
        edges = [(0, 1)]
        components = connected_components(n, edges)
        
        self.assertEqual(len(components), 4)  # {0,1}, {2}, {3}, {4}


class TestDetectCycleUndirected(unittest.TestCase):
    """detect_cycle_undirected 测试"""
    
    def test_no_cycle(self):
        """测试无环图"""
        n = 4
        edges = [(0, 1), (1, 2), (2, 3)]
        self.assertFalse(detect_cycle_undirected(n, edges))
        
    def test_with_cycle(self):
        """测试有环图"""
        n = 3
        edges = [(0, 1), (1, 2), (2, 0)]
        self.assertTrue(detect_cycle_undirected(n, edges))
        
    def test_triangle_cycle(self):
        """测试三角形环"""
        n = 3
        edges = [(0, 1), (1, 2), (0, 2)]
        self.assertTrue(detect_cycle_undirected(n, edges))
        
    def test_empty_graph(self):
        """测试空图"""
        self.assertFalse(detect_cycle_undirected(3, []))


class TestKruskalMST(unittest.TestCase):
    """kruskal_mst 测试"""
    
    def test_simple_mst(self):
        """测试简单最小生成树"""
        n = 4
        edges = [
            (0, 1, 1),
            (1, 2, 2),
            (2, 3, 3),
            (0, 3, 4)
        ]
        weight, mst = kruskal_mst(n, edges)
        
        self.assertEqual(weight, 6.0)  # 1 + 2 + 3
        self.assertEqual(len(mst), 3)  # n-1 条边
        
    def test_disconnected_graph(self):
        """测试不连通图"""
        n = 4
        edges = [(0, 1, 1), (2, 3, 2)]
        weight, mst = kruskal_mst(n, edges)
        
        self.assertEqual(weight, float('inf'))
        self.assertEqual(len(mst), 0)
        
    def test_triangle_graph(self):
        """测试三角形图"""
        n = 3
        edges = [
            (0, 1, 1),
            (1, 2, 2),
            (0, 2, 3)
        ]
        weight, mst = kruskal_mst(n, edges)
        
        self.assertEqual(weight, 3.0)  # 1 + 2
        self.assertEqual(len(mst), 2)


class TestAccountsMerge(unittest.TestCase):
    """accounts_merge 测试"""
    
    def test_simple_merge(self):
        """测试简单合并"""
        accounts = [
            ("John", ["john@email.com", "john.smith@email.com"]),
            ("John", ["john.smith@email.com", "john.doe@email.com"]),
            ("Mary", ["mary@email.com"])
        ]
        merged = accounts_merge(accounts)
        
        self.assertEqual(len(merged), 2)
        
        # 查找 John 的合并账户
        john_account = next((a for a in merged if a[0] == "John"), None)
        self.assertIsNotNone(john_account)
        self.assertEqual(len(john_account[1]), 3)
        
    def test_no_merge_needed(self):
        """测试无需合并"""
        accounts = [
            ("Alice", ["alice@email.com"]),
            ("Bob", ["bob@email.com"])
        ]
        merged = accounts_merge(accounts)
        
        self.assertEqual(len(merged), 2)
        
    def test_multiple_shared_emails(self):
        """测试多个共享邮箱"""
        accounts = [
            ("User1", ["a@email.com", "b@email.com"]),
            ("User1", ["b@email.com", "c@email.com"]),
            ("User1", ["c@email.com", "d@email.com"])
        ]
        merged = accounts_merge(accounts)
        
        self.assertEqual(len(merged), 1)
        self.assertEqual(len(merged[0][1]), 4)


if __name__ == '__main__':
    unittest.main()