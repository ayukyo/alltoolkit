"""
disjoint_set_utils 测试模块

全面测试并查集的各项功能
"""

import unittest
from typing import List, Set, Tuple
from mod import (
    DisjointSet, WeightedDisjointSet,
    connected_components, detect_cycle_undirected,
    minimum_spanning_tree_kruskal,
    create_disjoint_set, create_weighted_disjoint_set
)


class TestDisjointSet(unittest.TestCase):
    """测试 DisjointSet 类"""
    
    def test_init_empty(self):
        """测试空初始化"""
        ds = DisjointSet()
        self.assertEqual(len(ds), 0)
        self.assertEqual(ds.set_count, 0)
        self.assertTrue(ds.is_empty())
    
    def test_init_with_elements(self):
        """测试带元素初始化"""
        ds = DisjointSet([1, 2, 3, 4])
        self.assertEqual(len(ds), 4)
        self.assertEqual(ds.set_count, 4)
        self.assertFalse(ds.is_empty())
    
    def test_make_set(self):
        """测试创建单元素集合"""
        ds = DisjointSet()
        ds.make_set(1)
        self.assertIn(1, ds)
        self.assertEqual(ds.find(1), 1)
        self.assertEqual(ds.set_count, 1)
    
    def test_make_set_duplicate(self):
        """测试重复创建元素"""
        ds = DisjointSet()
        ds.make_set(1)
        with self.assertRaises(ValueError):
            ds.make_set(1)
    
    def test_make_sets(self):
        """测试批量创建集合"""
        ds = DisjointSet()
        ds.make_sets([1, 2, 3])
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds.set_count, 3)
    
    def test_find_basic(self):
        """测试基本查找"""
        ds = DisjointSet([1])
        self.assertEqual(ds.find(1), 1)
    
    def test_find_nonexistent(self):
        """测试查找不存在的元素"""
        ds = DisjointSet()
        with self.assertRaises(KeyError):
            ds.find(999)
    
    def test_union_basic(self):
        """测试基本合并"""
        ds = DisjointSet([1, 2])
        result = ds.union(1, 2)
        self.assertTrue(result)
        self.assertEqual(ds.find(1), ds.find(2))
        self.assertEqual(ds.set_count, 1)
    
    def test_union_same_set(self):
        """测试合并同一集合中的元素"""
        ds = DisjointSet([1, 2])
        ds.union(1, 2)
        result = ds.union(1, 2)
        self.assertFalse(result)
    
    def test_union_multiple(self):
        """测试多次合并"""
        ds = DisjointSet([1, 2, 3, 4, 5])
        ds.union(1, 2)
        ds.union(3, 4)
        ds.union(2, 3)
        ds.union(4, 5)
        self.assertEqual(ds.set_count, 1)
        self.assertTrue(ds.connected(1, 5))
    
    def test_union_all(self):
        """测试批量合并"""
        ds = DisjointSet([1, 2, 3, 4, 5])
        merges = ds.union_all([1, 2, 3, 4, 5])
        self.assertEqual(merges, 4)
        self.assertEqual(ds.set_count, 1)
    
    def test_connected_true(self):
        """测试连通性检测 - 连通"""
        ds = DisjointSet([1, 2, 3])
        ds.union(1, 2)
        ds.union(2, 3)
        self.assertTrue(ds.connected(1, 3))
    
    def test_connected_false(self):
        """测试连通性检测 - 不连通"""
        ds = DisjointSet([1, 2, 3])
        ds.union(1, 2)
        self.assertFalse(ds.connected(1, 3))
    
    def test_connected_nonexistent(self):
        """测试不存在的元素的连通性"""
        ds = DisjointSet([1])
        self.assertFalse(ds.connected(1, 999))
        self.assertFalse(ds.connected(999, 1))
    
    def test_get_set_size(self):
        """测试获取集合大小"""
        ds = DisjointSet([1, 2, 3, 4])
        ds.union(1, 2)
        ds.union(3, 4)
        self.assertEqual(ds.get_set_size(1), 2)
        self.assertEqual(ds.get_set_size(3), 2)
    
    def test_get_sets(self):
        """测试获取所有集合"""
        ds = DisjointSet([1, 2, 3, 4, 5])
        ds.union(1, 2)
        ds.union(3, 4)
        
        sets = ds.get_sets()
        self.assertEqual(len(sets), 3)
        
        # 检查每个集合的内容
        set_sizes = sorted(len(s) for s in sets)
        self.assertEqual(set_sizes, [1, 2, 2])
    
    def test_get_set(self):
        """测试获取特定元素所属集合"""
        ds = DisjointSet([1, 2, 3, 4])
        ds.union(1, 2)
        ds.union(3, 4)
        
        set1 = ds.get_set(1)
        self.assertEqual(set1, {1, 2})
        
        set3 = ds.get_set(3)
        self.assertEqual(set3, {3, 4})
    
    def test_find_path(self):
        """测试查找路径"""
        ds = DisjointSet([1, 2, 3])
        ds.union(1, 2)
        ds.union(2, 3)
        
        path = ds.find_path(3)
        self.assertEqual(path[-1], ds.find(3))  # 路径终点是根
    
    def test_path_compression(self):
        """测试路径压缩"""
        ds = DisjointSet(range(10))
        # 创建一个长链
        for i in range(1, 10):
            ds.union(i-1, i)
        
        # 查找应该压缩路径
        root = ds.find(9)
        # 再次查找时路径应该更短
        path_after = ds.find_path(9)
        self.assertLessEqual(len(path_after), 2)  # 压缩后最多2层
    
    def test_remove_leaf(self):
        """测试移除叶节点"""
        ds = DisjointSet([1, 2, 3])
        ds.union(1, 2)
        ds.union(2, 3)
        
        result = ds.remove(3)
        self.assertTrue(result)
        self.assertNotIn(3, ds)
    
    def test_remove_root(self):
        """测试移除根节点"""
        ds = DisjointSet([1, 2, 3])
        ds.union(1, 2)
        ds.union(2, 3)
        
        result = ds.remove(1)
        self.assertTrue(result)
        self.assertNotIn(1, ds)
        # 其他元素应该仍然连通
        self.assertTrue(ds.connected(2, 3))
    
    def test_remove_nonexistent(self):
        """测试移除不存在的元素"""
        ds = DisjointSet([1])
        result = ds.remove(999)
        self.assertFalse(result)
    
    def test_copy(self):
        """测试深拷贝"""
        ds1 = DisjointSet([1, 2, 3])
        ds1.union(1, 2)
        
        ds2 = ds1.copy()
        ds2.union(2, 3)
        
        # 原并查集不受影响
        self.assertEqual(ds1.set_count, 2)
        self.assertEqual(ds2.set_count, 1)
    
    def test_clear(self):
        """测试清空"""
        ds = DisjointSet([1, 2, 3])
        ds.union(1, 2)
        ds.clear()
        
        self.assertEqual(len(ds), 0)
        self.assertEqual(ds.set_count, 0)
        self.assertTrue(ds.is_empty())
    
    def test_iteration(self):
        """测试迭代"""
        ds = DisjointSet([1, 2, 3])
        elements = list(ds)
        self.assertEqual(sorted(elements), [1, 2, 3])
    
    def test_repr(self):
        """测试字符串表示"""
        ds = DisjointSet([1, 2])
        repr_str = repr(ds)
        self.assertIn("DisjointSet", repr_str)
    
    def test_serialization(self):
        """测试序列化和反序列化"""
        ds1 = DisjointSet([1, 2, 3, 4])
        ds1.union(1, 2)
        ds1.union(3, 4)
        
        data = ds1.to_dict()
        ds2 = DisjointSet.from_dict(data)
        
        self.assertEqual(ds1.set_count, ds2.set_count)
        self.assertEqual(len(ds1), len(ds2))
    
    def test_string_elements(self):
        """测试字符串元素"""
        ds = DisjointSet(['a', 'b', 'c'])
        ds.union('a', 'b')
        self.assertTrue(ds.connected('a', 'b'))
        self.assertFalse(ds.connected('a', 'c'))
    
    def test_tuple_elements(self):
        """测试元组元素"""
        ds = DisjointSet([(1, 2), (3, 4), (5, 6)])
        ds.union((1, 2), (3, 4))
        self.assertTrue(ds.connected((1, 2), (3, 4)))
    
    def test_large_dataset(self):
        """测试大数据集"""
        n = 10000
        ds = DisjointSet(range(n))
        
        # 合并成单个集合
        for i in range(1, n):
            ds.union(0, i)
        
        self.assertEqual(ds.set_count, 1)
        self.assertTrue(ds.connected(0, n-1))


class TestWeightedDisjointSet(unittest.TestCase):
    """测试带权并查集"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        wds = WeightedDisjointSet([1, 2, 3])
        wds.union(1, 2, weight=5)
        
        self.assertTrue(wds.connected(1, 2))
        self.assertEqual(wds.get_weight(1, 2), 5)
    
    def test_transitive_weight(self):
        """测试权重传递"""
        wds = WeightedDisjointSet([1, 2, 3])
        wds.union(1, 2, weight=3)
        wds.union(2, 3, weight=2)
        
        self.assertTrue(wds.connected(1, 3))
        # 1 -> 2 -> 3: 3 + 2 = 5
        self.assertEqual(wds.get_weight(1, 3), 5)
    
    def test_negative_weight(self):
        """测试负权重"""
        wds = WeightedDisjointSet([1, 2])
        wds.union(1, 2, weight=-10)
        self.assertEqual(wds.get_weight(1, 2), -10)
    
    def test_zero_weight(self):
        """测试零权重"""
        wds = WeightedDisjointSet([1, 2])
        wds.union(1, 2, weight=0)
        self.assertEqual(wds.get_weight(1, 2), 0)
    
    def test_different_components(self):
        """测试不同集合的权重"""
        wds = WeightedDisjointSet([1, 2, 3])
        wds.union(1, 2, weight=5)
        
        # 1 和 3 不连通
        self.assertIsNone(wds.get_weight(1, 3))


class TestConnectedComponents(unittest.TestCase):
    """测试连通分量计算"""
    
    def test_empty(self):
        """测试空图"""
        result = connected_components([])
        self.assertEqual(result, [])
    
    def test_single_component(self):
        """测试单一连通分量"""
        edges = [(1, 2), (2, 3), (3, 4)]
        result = connected_components(edges)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], {1, 2, 3, 4})
    
    def test_multiple_components(self):
        """测试多个连通分量"""
        edges = [(1, 2), (2, 3), (4, 5), (6, 7), (7, 8)]
        result = connected_components(edges)
        self.assertEqual(len(result), 3)
        
        sizes = sorted(len(c) for c in result)
        self.assertEqual(sizes, [2, 3, 3])
    
    def test_no_edges(self):
        """测试无边的图"""
        # 无边的情况，每个节点自成一个分量
        # 但函数从边推导节点，无边则为空
        result = connected_components([])
        self.assertEqual(result, [])


class TestCycleDetection(unittest.TestCase):
    """测试环检测"""
    
    def test_no_cycle(self):
        """测试无环图"""
        edges = [(1, 2), (2, 3), (3, 4)]
        self.assertFalse(detect_cycle_undirected(edges))
    
    def test_simple_cycle(self):
        """测试简单环"""
        edges = [(1, 2), (2, 3), (3, 1)]
        self.assertTrue(detect_cycle_undirected(edges))
    
    def test_complex_cycle(self):
        """测试复杂环"""
        edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 2)]
        self.assertTrue(detect_cycle_undirected(edges))
    
    def test_multiple_cycles(self):
        """测试多个环"""
        edges = [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)]
        self.assertTrue(detect_cycle_undirected(edges))
    
    def test_empty_graph(self):
        """测试空图"""
        self.assertFalse(detect_cycle_undirected([]))
    
    def test_single_edge(self):
        """测试单边"""
        self.assertFalse(detect_cycle_undirected([(1, 2)]))


class TestMinimumSpanningTree(unittest.TestCase):
    """测试最小生成树"""
    
    def test_simple_graph(self):
        """测试简单图"""
        nodes = [1, 2, 3]
        edges = [(1, 2, 1), (2, 3, 2), (1, 3, 3)]
        
        mst, total = minimum_spanning_tree_kruskal(nodes, edges)
        self.assertEqual(len(mst), 2)
        self.assertEqual(total, 3)  # 1 + 2
    
    def test_complex_graph(self):
        """测试复杂图"""
        nodes = ['A', 'B', 'C', 'D']
        edges = [
            ('A', 'B', 4),
            ('A', 'C', 2),
            ('B', 'C', 1),
            ('B', 'D', 3),
            ('C', 'D', 5)
        ]
        
        mst, total = minimum_spanning_tree_kruskal(nodes, edges)
        self.assertEqual(len(mst), 3)  # n-1 edges
        self.assertEqual(total, 6)  # 2 + 1 + 3
    
    def test_empty_graph(self):
        """测试空图"""
        mst, total = minimum_spanning_tree_kruskal([], [])
        self.assertEqual(mst, [])
        self.assertEqual(total, 0)
    
    def test_single_node(self):
        """测试单节点"""
        mst, total = minimum_spanning_tree_kruskal([1], [])
        self.assertEqual(mst, [])
        self.assertEqual(total, 0)
    
    def test_disconnected_graph(self):
        """测试不连通图"""
        nodes = [1, 2, 3, 4]
        edges = [(1, 2, 1), (3, 4, 2)]  # 两个不连通部分
        
        mst, total = minimum_spanning_tree_kruskal(nodes, edges)
        self.assertEqual(len(mst), 2)
        self.assertEqual(total, 3)
    
    def test_equal_weights(self):
        """测试等权重边"""
        nodes = [1, 2, 3]
        edges = [(1, 2, 1), (2, 3, 1), (1, 3, 1)]
        
        mst, total = minimum_spanning_tree_kruskal(nodes, edges)
        self.assertEqual(len(mst), 2)
        self.assertEqual(total, 2)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_create_disjoint_set(self):
        """测试创建并查集函数"""
        ds = create_disjoint_set([1, 2, 3])
        self.assertEqual(len(ds), 3)
        self.assertEqual(ds.set_count, 3)
    
    def test_create_weighted_disjoint_set(self):
        """测试创建带权并查集函数"""
        wds = create_weighted_disjoint_set([1, 2, 3])
        self.assertEqual(len(wds), 3)
    
    def test_create_empty(self):
        """测试创建空并查集"""
        ds = create_disjoint_set()
        self.assertTrue(ds.is_empty())


if __name__ == '__main__':
    unittest.main(verbosity=2)