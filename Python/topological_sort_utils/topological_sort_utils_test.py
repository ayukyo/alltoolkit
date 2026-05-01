#!/usr/bin/env python3
"""
Topological Sort Utils 测试套件
"""

import unittest
import sys
import os

# 添加父目录到路径以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Graph,
    TopologicalSorter,
    TopologicalSortError,
    CycleDetectedError,
    topological_sort,
    detect_cycle,
    get_parallel_levels,
)


class TestGraph(unittest.TestCase):
    """测试 Graph 类"""
    
    def test_add_node(self):
        """测试添加节点"""
        g = Graph()
        g.add_node('A')
        g.add_node('B')
        g.add_node('C')
        
        self.assertEqual(g.node_count, 3)
        self.assertTrue(g.has_node('A'))
        self.assertTrue(g.has_node('B'))
        self.assertTrue(g.has_node('C'))
        self.assertFalse(g.has_node('D'))
    
    def test_add_node_with_weight(self):
        """测试带权节点"""
        g = Graph()
        g.add_node('A', weight=10)
        g.add_node('B', weight={'data': 'test'})
        
        self.assertEqual(g.get_node_weight('A'), 10)
        self.assertEqual(g.get_node_weight('B'), {'data': 'test'})
        self.assertIsNone(g.get_node_weight('C'))
        self.assertEqual(g.get_node_weight('C', 0), 0)
    
    def test_add_edge(self):
        """测试添加边"""
        g = Graph()
        g.add_edge('A', 'B')
        g.add_edge('B', 'C')
        
        self.assertEqual(g.node_count, 3)
        self.assertEqual(g.edge_count, 2)
        self.assertTrue(g.has_edge('A', 'B'))
        self.assertTrue(g.has_edge('B', 'C'))
        self.assertFalse(g.has_edge('A', 'C'))
    
    def test_add_edges(self):
        """测试批量添加边"""
        g = Graph()
        g.add_edges([('A', 'B'), ('B', 'C'), ('A', 'C')])
        
        self.assertEqual(g.node_count, 3)
        self.assertEqual(g.edge_count, 3)
    
    def test_remove_edge(self):
        """测试移除边"""
        g = Graph()
        g.add_edge('A', 'B')
        g.remove_edge('A', 'B')
        
        self.assertEqual(g.edge_count, 0)
        self.assertFalse(g.has_edge('A', 'B'))
    
    def test_remove_node(self):
        """测试移除节点"""
        g = Graph()
        g.add_edges([('A', 'B'), ('B', 'C'), ('C', 'A')])
        g.remove_node('B')
        
        self.assertEqual(g.node_count, 2)
        self.assertEqual(g.edge_count, 1)  # 只有 C->A
        self.assertFalse(g.has_node('B'))
    
    def test_in_out_degree(self):
        """测试入度和出度"""
        g = Graph()
        g.add_edges([('A', 'B'), ('A', 'C'), ('D', 'A')])
        
        self.assertEqual(g.in_degree('A'), 1)
        self.assertEqual(g.out_degree('A'), 2)
        self.assertEqual(g.in_degree('B'), 1)
        self.assertEqual(g.out_degree('B'), 0)
    
    def test_neighbors_predecessors(self):
        """测试邻居和前驱"""
        g = Graph()
        g.add_edges([('A', 'B'), ('A', 'C'), ('B', 'D')])
        
        self.assertEqual(g.get_neighbors('A'), {'B', 'C'})
        self.assertEqual(g.get_neighbors('B'), {'D'})
        self.assertEqual(g.get_predecessors('D'), {'B'})
        self.assertEqual(g.get_predecessors('A'), set())
    
    def test_copy(self):
        """测试图拷贝"""
        g = Graph()
        g.add_edges([('A', 'B'), ('B', 'C')])
        g.set_node_weight('A', 100)
        
        g2 = g.copy()
        g2.add_edge('C', 'D')
        
        self.assertEqual(g.node_count, 3)
        self.assertEqual(g2.node_count, 4)
        self.assertEqual(g.get_node_weight('A'), 100)
        self.assertEqual(g2.get_node_weight('A'), 100)


class TestTopologicalSorter(unittest.TestCase):
    """测试 TopologicalSorter 类"""
    
    def setUp(self):
        """创建测试图"""
        # 简单 DAG: A -> B -> C, A -> C
        self.simple_graph = Graph()
        self.simple_graph.add_edges([('A', 'B'), ('B', 'C'), ('A', 'C')])
        
        # 线性 DAG: A -> B -> C -> D
        self.linear_graph = Graph()
        self.linear_graph.add_edges([('A', 'B'), ('B', 'C'), ('C', 'D')])
        
        # 复杂 DAG（多起点多终点）
        self.complex_graph = Graph()
        self.complex_graph.add_edges([
            ('A', 'C'), ('B', 'C'),
            ('C', 'D'), ('C', 'E'),
            ('D', 'F'), ('E', 'F')
        ])
        
        # 带环图
        self.cycle_graph = Graph()
        self.cycle_graph.add_edges([('A', 'B'), ('B', 'C'), ('C', 'A')])
    
    def test_kahn_sort_simple(self):
        """测试 Kahn 算法 - 简单图"""
        sorter = TopologicalSorter(self.simple_graph)
        result = sorter.kahn_sort()
        
        # A 必须在 B 和 C 之前
        self.assertLess(result.index('A'), result.index('B'))
        self.assertLess(result.index('A'), result.index('C'))
        # B 必须在 C 之前
        self.assertLess(result.index('B'), result.index('C'))
    
    def test_kahn_sort_linear(self):
        """测试 Kahn 算法 - 线性图"""
        sorter = TopologicalSorter(self.linear_graph)
        result = sorter.kahn_sort()
        
        self.assertEqual(result, ['A', 'B', 'C', 'D'])
    
    def test_kahn_sort_cycle(self):
        """测试 Kahn 算法 - 有环图"""
        sorter = TopologicalSorter(self.cycle_graph)
        
        with self.assertRaises(CycleDetectedError):
            sorter.kahn_sort()
    
    def test_dfs_sort_simple(self):
        """测试 DFS 排序 - 简单图"""
        sorter = TopologicalSorter(self.simple_graph)
        result = sorter.dfs_sort()
        
        # 验证顺序正确
        self.assertLess(result.index('A'), result.index('B'))
        self.assertLess(result.index('A'), result.index('C'))
        self.assertLess(result.index('B'), result.index('C'))
    
    def test_dfs_sort_cycle(self):
        """测试 DFS 排序 - 有环图"""
        sorter = TopologicalSorter(self.cycle_graph)
        
        with self.assertRaises(CycleDetectedError):
            sorter.dfs_sort()
    
    def test_has_cycle(self):
        """测试环检测"""
        # 无环图
        sorter1 = TopologicalSorter(self.simple_graph)
        self.assertFalse(sorter1.has_cycle())
        
        sorter2 = TopologicalSorter(self.linear_graph)
        self.assertFalse(sorter2.has_cycle())
        
        # 有环图
        sorter3 = TopologicalSorter(self.cycle_graph)
        self.assertTrue(sorter3.has_cycle())
    
    def test_find_cycle(self):
        """测试查找环"""
        sorter1 = TopologicalSorter(self.simple_graph)
        self.assertIsNone(sorter1.find_cycle())
        
        sorter2 = TopologicalSorter(self.cycle_graph)
        cycle = sorter2.find_cycle()
        self.assertIsNotNone(cycle)
        self.assertEqual(len(cycle), 4)  # A, B, C, A
        self.assertEqual(cycle[0], cycle[-1])  # 起点和终点相同
    
    def test_parallel_levels(self):
        """测试并行层级"""
        sorter = TopologicalSorter(self.complex_graph)
        levels = sorter.parallel_levels()
        
        # 第一层：A, B（无依赖）
        self.assertIn(['A', 'B'], levels)
        # 第二层：C
        self.assertIn(['C'], levels)
        # 第三层：D, E
        self.assertIn(['D', 'E'], levels)
        # 第四层：F
        self.assertIn(['F'], levels)
    
    def test_parallel_levels_cycle(self):
        """测试并行层级 - 有环图"""
        sorter = TopologicalSorter(self.cycle_graph)
        
        with self.assertRaises(CycleDetectedError):
            sorter.parallel_levels()
    
    def test_longest_path(self):
        """测试最长路径"""
        sorter = TopologicalSorter(self.linear_graph)
        length, path = sorter.longest_path()
        
        self.assertEqual(length, 3)  # 3 条边
        self.assertEqual(path, ['A', 'B', 'C', 'D'])
    
    def test_longest_path_complex(self):
        """测试最长路径 - 复杂图"""
        sorter = TopologicalSorter(self.complex_graph)
        length, path = sorter.longest_path()
        
        # 最长路径可能是 A->C->D->F 或 B->C->D->F 或 A->C->E->F 或 B->C->E->F
        self.assertEqual(length, 3)
        self.assertEqual(len(path), 4)
    
    def test_longest_path_weighted(self):
        """测试带权最长路径"""
        graph = Graph()
        graph.add_node('A', 1)
        graph.add_node('B', 2)
        graph.add_node('C', 3)
        graph.add_node('D', 4)
        graph.add_edges([('A', 'B'), ('B', 'C'), ('C', 'D')])
        
        sorter = TopologicalSorter(graph)
        weight, path = sorter.longest_path_weighted()
        
        self.assertEqual(weight, 10)  # 1 + 2 + 3 + 4
        self.assertEqual(path, ['A', 'B', 'C', 'D'])
    
    def test_ancestors(self):
        """测试获取祖先"""
        sorter = TopologicalSorter(self.complex_graph)
        
        ancestors_c = sorter.ancestors('C')
        self.assertEqual(ancestors_c, {'A', 'B'})
        
        ancestors_f = sorter.ancestors('F')
        self.assertEqual(ancestors_f, {'A', 'B', 'C', 'D', 'E'})
    
    def test_descendants(self):
        """测试获取后代"""
        sorter = TopologicalSorter(self.complex_graph)
        
        descendants_a = sorter.descendants('A')
        self.assertEqual(descendants_a, {'C', 'D', 'E', 'F'})
        
        descendants_c = sorter.descendants('C')
        self.assertEqual(descendants_c, {'D', 'E', 'F'})
    
    def test_all_paths(self):
        """测试查找所有路径"""
        graph = Graph()
        graph.add_edges([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')])
        
        sorter = TopologicalSorter(graph)
        paths = sorter.all_paths('A', 'D')
        
        self.assertEqual(len(paths), 2)
        self.assertIn(['A', 'B', 'D'], paths)
        self.assertIn(['A', 'C', 'D'], paths)
    
    def test_sort_with_priority(self):
        """测试带优先级的拓扑排序"""
        sorter = TopologicalSorter(self.complex_graph)
        
        # 优先级：按字母顺序
        result = sorter.sort_with_priority(priority=lambda x: x)
        
        # A, B 无依赖，按字母顺序
        self.assertEqual(result[0], 'A')
        self.assertEqual(result[1], 'B')
    
    def test_empty_graph(self):
        """测试空图"""
        graph = Graph()
        sorter = TopologicalSorter(graph)
        
        self.assertEqual(sorter.kahn_sort(), [])
        self.assertEqual(sorter.dfs_sort(), [])
        self.assertEqual(sorter.parallel_levels(), [])
        self.assertFalse(sorter.has_cycle())


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_topological_sort(self):
        """测试快速拓扑排序"""
        edges = [('A', 'B'), ('B', 'C'), ('A', 'C')]
        result = topological_sort(edges)
        
        self.assertEqual(len(result), 3)
        self.assertLess(result.index('A'), result.index('B'))
        self.assertLess(result.index('B'), result.index('C'))
    
    def test_topological_sort_with_nodes(self):
        """测试带孤立节点的拓扑排序"""
        edges = [('A', 'B')]
        nodes = ['A', 'B', 'C']  # C 是孤立节点
        result = topological_sort(edges, nodes)
        
        self.assertEqual(len(result), 3)
        self.assertIn('C', result)
    
    def test_detect_cycle(self):
        """测试快速环检测"""
        # 无环
        edges1 = [('A', 'B'), ('B', 'C')]
        self.assertIsNone(detect_cycle(edges1))
        
        # 有环
        edges2 = [('A', 'B'), ('B', 'C'), ('C', 'A')]
        cycle = detect_cycle(edges2)
        self.assertIsNotNone(cycle)
    
    def test_get_parallel_levels(self):
        """测试快速获取并行层级"""
        edges = [('A', 'C'), ('B', 'C')]
        levels = get_parallel_levels(edges)
        
        self.assertEqual(len(levels), 2)
        self.assertIn(['A', 'B'], levels)
        self.assertIn(['C'], levels)


class TestRealWorldScenarios(unittest.TestCase):
    """测试真实世界场景"""
    
    def test_task_dependencies(self):
        """测试任务依赖排序"""
        # 构建系统依赖
        # A: 基础库
        # B, C: 依赖 A 的库
        # D: 依赖 B, C 的应用
        graph = Graph()
        graph.add_edges([
            ('base', 'utils'),     # utils 依赖 base
            ('base', 'core'),      # core 依赖 base
            ('utils', 'app'),      # app 依赖 utils
            ('core', 'app'),       # app 依赖 core
        ])
        
        sorter = TopologicalSorter(graph)
        order = sorter.kahn_sort()
        
        # base 必须最先
        self.assertEqual(order[0], 'base')
        # app 必须最后
        self.assertEqual(order[-1], 'app')
        # utils 和 core 在 base 之后，app 之前
        self.assertLess(order.index('base'), order.index('utils'))
        self.assertLess(order.index('base'), order.index('core'))
        self.assertLess(order.index('utils'), order.index('app'))
        self.assertLess(order.index('core'), order.index('app'))
    
    def test_course_prerequisites(self):
        """测试课程先修关系"""
        graph = Graph()
        graph.add_edges([
            ('math101', 'math201'),
            ('math101', 'physics101'),
            ('math201', 'physics201'),
            ('physics101', 'physics201'),
            ('math201', 'math301'),
            ('physics201', 'quantum'),
            ('math301', 'quantum'),
        ])
        
        sorter = TopologicalSorter(graph)
        order = sorter.kahn_sort()
        
        # 验证先修关系
        self.assertLess(order.index('math101'), order.index('math201'))
        self.assertLess(order.index('math201'), order.index('math301'))
        self.assertLess(order.index('physics101'), order.index('physics201'))
        self.assertLess(order.index('math301'), order.index('quantum'))
        self.assertLess(order.index('physics201'), order.index('quantum'))
    
    def test_package_dependencies(self):
        """测试包依赖关系"""
        # npm/pip 风格的依赖
        graph = Graph()
        graph.add_edges([
            ('lodash', 'myapp'),
            ('express', 'myapp'),
            ('body-parser', 'express'),
            ('cookie-parser', 'express'),
        ])
        
        sorter = TopologicalSorter(graph)
        levels = sorter.parallel_levels()
        
        # 可以并行安装的包
        # Level 0: lodash, body-parser, cookie-parser（无依赖）
        # Level 1: express
        # Level 2: myapp
        
        first_level = [pkg for level in levels for pkg in level if pkg in ['lodash', 'body-parser', 'cookie-parser']]
        self.assertEqual(len(first_level), 3)
    
    def test_parallel_execution_planning(self):
        """测试并行执行规划"""
        # CI/CD 任务依赖
        graph = Graph()
        graph.add_edges([
            ('checkout', 'build'),
            ('checkout', 'lint'),
            ('checkout', 'test-unit'),
            ('build', 'test-integration'),
            ('build', 'deploy-staging'),
            ('lint', 'deploy-staging'),
            ('test-unit', 'test-integration'),
            ('test-integration', 'deploy-prod'),
            ('deploy-staging', 'deploy-prod'),
        ])
        
        sorter = TopologicalSorter(graph)
        levels = sorter.parallel_levels()
        
        # checkout 必须在第 0 层
        self.assertIn('checkout', levels[0])
        
        # build, lint, test-unit 可以并行（第 1 层）
        level_1_nodes = set(levels[1]) if len(levels) > 1 else set()
        self.assertTrue({'build', 'lint', 'test-unit'}.issubset(level_1_nodes))
        
        # deploy-prod 在最后一层
        self.assertIn('deploy-prod', levels[-1])


if __name__ == '__main__':
    unittest.main(verbosity=2)