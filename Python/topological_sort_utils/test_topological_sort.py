"""
Topological Sort Utilities 测试套件

测试覆盖：
- 基本拓扑排序（Kahn's 和 DFS）
- 循环检测
- 并行分层
- 依赖关系分析
- 边界情况
"""

import unittest
from topological_sort import (
    TopologicalSort,
    topological_sort,
    detect_cycle,
    parallel_layers,
    CycleDetectedError
)


class TestBasicOperations(unittest.TestCase):
    """基本操作测试"""
    
    def test_add_node(self):
        """测试添加节点"""
        ts = TopologicalSort()
        ts.add_node('A')
        self.assertIn('A', ts)
        self.assertEqual(ts.node_count, 1)
        self.assertEqual(ts.edge_count, 0)
    
    def test_add_edge(self):
        """测试添加边"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        self.assertIn('A', ts)
        self.assertIn('B', ts)
        self.assertEqual(ts.node_count, 2)
        self.assertEqual(ts.edge_count, 1)
    
    def test_chainable(self):
        """测试链式调用"""
        ts = TopologicalSort()
        result = ts.add_node('A').add_edge('B', 'C').add_node('D')
        self.assertIs(result, ts)
        self.assertEqual(ts.node_count, 4)
    
    def test_remove_edge(self):
        """测试移除边"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        self.assertTrue(ts.remove_edge('A', 'B'))
        self.assertEqual(ts.edge_count, 0)
        self.assertFalse(ts.remove_edge('A', 'B'))
    
    def test_remove_node(self):
        """测试移除节点"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('B', 'C')
        self.assertTrue(ts.remove_node('B'))
        self.assertNotIn('B', ts)
        self.assertEqual(ts.node_count, 2)
        self.assertEqual(ts.edge_count, 0)  # 相关边也被移除


class TestTopologicalSort(unittest.TestCase):
    """拓扑排序测试"""
    
    def test_simple_dag(self):
        """测试简单有向无环图"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')  # A 依赖 B
        ts.add_edge('B', 'C')  # B 依赖 C
        
        result = ts.sort_kahn()
        self.assertEqual(result, ['C', 'B', 'A'])
    
    def test_multiple_dependencies(self):
        """测试多依赖情况"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('A', 'C')
        ts.add_edge('B', 'D')
        ts.add_edge('C', 'D')
        
        result = ts.sort_kahn()
        # D 必须在最前，A 必须在最后
        self.assertEqual(result[0], 'D')
        self.assertEqual(result[-1], 'A')
        self.assertTrue(result.index('B') < result.index('A'))
        self.assertTrue(result.index('C') < result.index('A'))
    
    def test_independent_nodes(self):
        """测试独立节点（无依赖关系）"""
        ts = TopologicalSort()
        ts.add_node('A')
        ts.add_node('B')
        ts.add_node('C')
        
        result = ts.sort_kahn()
        self.assertEqual(set(result), {'A', 'B', 'C'})
    
    def test_dfs_algorithm(self):
        """测试 DFS 算法"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('B', 'C')
        
        result = ts.sort_dfs()
        self.assertEqual(result, ['C', 'B', 'A'])
    
    def test_sort_method_default_kahn(self):
        """测试 sort 方法默认使用 Kahn 算法"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        
        result_kahn = ts.sort_kahn()
        result_default = ts.sort()
        self.assertEqual(result_kahn, result_default)
    
    def test_sort_method_dfs(self):
        """测试 sort 方法使用 DFS 算法"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        
        result = ts.sort(algorithm='dfs')
        self.assertEqual(result, ['B', 'A'])
    
    def test_convenience_function(self):
        """测试便捷函数"""
        nodes = ['A', 'B', 'C']
        edges = [('A', 'B'), ('B', 'C')]
        
        result = topological_sort(nodes, edges)
        self.assertEqual(result, ['C', 'B', 'A'])


class TestCycleDetection(unittest.TestCase):
    """循环检测测试"""
    
    def test_simple_cycle(self):
        """测试简单循环"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('B', 'C')
        ts.add_edge('C', 'A')  # 形成循环
        
        with self.assertRaises(CycleDetectedError) as context:
            ts.sort_kahn()
        
        self.assertIn('Cycle detected', str(context.exception))
    
    def test_self_loop(self):
        """测试自循环"""
        ts = TopologicalSort()
        ts.add_edge('A', 'A')
        
        with self.assertRaises(CycleDetectedError):
            ts.sort_kahn()
    
    def test_has_cycle_method(self):
        """测试 has_cycle 方法"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('B', 'C')
        
        self.assertFalse(ts.has_cycle())
        
        ts.add_edge('C', 'A')
        self.assertTrue(ts.has_cycle())
    
    def test_get_cycle(self):
        """测试 get_cycle 方法"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('B', 'C')
        ts.add_edge('C', 'A')
        
        cycle = ts.get_cycle()
        self.assertIsNotNone(cycle)
        self.assertEqual(cycle[0], cycle[-1])  # 循环首尾相连
    
    def test_no_cycle_returns_none(self):
        """测试无循环时 get_cycle 返回 None"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('B', 'C')
        
        self.assertIsNone(ts.get_cycle())
    
    def test_detect_cycle_convenience(self):
        """测试 detect_cycle 便捷函数"""
        nodes = ['A', 'B', 'C']
        edges = [('A', 'B'), ('B', 'C'), ('C', 'A')]
        
        cycle = detect_cycle(nodes, edges)
        self.assertIsNotNone(cycle)


class TestParallelLayers(unittest.TestCase):
    """并行分层测试"""
    
    def test_simple_layers(self):
        """测试简单分层"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')  # A 依赖 B
        
        layers = ts.layers()
        self.assertEqual(len(layers), 2)
        self.assertIn('B', layers[0])
        self.assertIn('A', layers[1])
    
    def test_parallel_execution(self):
        """测试可并行执行的节点"""
        ts = TopologicalSort()
        ts.add_node('A')
        ts.add_node('B')
        ts.add_edge('C', 'A')
        ts.add_edge('C', 'B')
        
        layers = ts.layers()
        # 第一层：A, B（可并行）
        # 第二层：C
        self.assertEqual(len(layers), 2)
        self.assertIn('A', layers[0])
        self.assertIn('B', layers[0])
        self.assertIn('C', layers[1])
    
    def test_min_steps(self):
        """测试最少步骤数"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('B', 'C')
        ts.add_edge('C', 'D')
        
        self.assertEqual(ts.min_steps(), 4)
    
    def test_parallel_levels_dict(self):
        """测试节点层级映射"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        
        levels = ts.parallel_levels()
        self.assertEqual(levels['B'], 0)
        self.assertEqual(levels['A'], 1)
    
    def test_layers_with_cycle(self):
        """测试循环时的分层"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('B', 'A')
        
        with self.assertRaises(CycleDetectedError):
            ts.layers()


class TestDependencyAnalysis(unittest.TestCase):
    """依赖分析测试"""
    
    def test_get_dependencies(self):
        """测试获取直接依赖"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('A', 'C')
        
        deps = ts.get_dependencies('A')
        self.assertEqual(deps, {'B', 'C'})
    
    def test_get_dependents(self):
        """测试获取依赖者"""
        ts = TopologicalSort()
        ts.add_edge('A', 'C')
        ts.add_edge('B', 'C')
        
        dependents = ts.get_dependents('C')
        self.assertEqual(dependents, {'A', 'B'})
    
    def test_get_all_dependencies(self):
        """测试获取所有依赖（包括传递依赖）"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('B', 'C')
        
        all_deps = ts.get_all_dependencies('A')
        self.assertEqual(all_deps, {'B', 'C'})
    
    def test_can_reach(self):
        """测试可达性"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('B', 'C')
        
        self.assertTrue(ts.can_reach('A', 'C'))
        self.assertFalse(ts.can_reach('C', 'A'))


class TestCriticalPath(unittest.TestCase):
    """关键路径测试"""
    
    def test_critical_path_single(self):
        """测试单节点关键路径"""
        ts = TopologicalSort()
        ts.add_node('A')
        
        path, length = ts.critical_path()
        self.assertEqual(path, ['A'])
        self.assertEqual(length, 0)
    
    def test_critical_path_chain(self):
        """测试链式关键路径"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('B', 'C')
        ts.add_edge('C', 'D')
        
        path, length = ts.critical_path()
        self.assertEqual(length, 3)
    
    def test_critical_path_diamond(self):
        """测试菱形图的关键路径"""
        ts = TopologicalSort()
        ts.add_edge('D', 'B')
        ts.add_edge('D', 'C')
        ts.add_edge('B', 'A')
        ts.add_edge('C', 'A')
        
        path, length = ts.critical_path()
        self.assertEqual(length, 2)  # D -> B/C -> A


class TestValidation(unittest.TestCase):
    """验证测试"""
    
    def test_valid_order(self):
        """测试验证有效顺序"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('B', 'C')
        
        self.assertTrue(ts.is_valid_order(['C', 'B', 'A']))
        self.assertFalse(ts.is_valid_order(['A', 'B', 'C']))
    
    def test_valid_order_missing_nodes(self):
        """测试验证缺少节点的顺序"""
        ts = TopologicalSort()
        ts.add_node('A')
        ts.add_node('B')
        
        self.assertFalse(ts.is_valid_order(['A']))
    
    def test_valid_order_extra_nodes(self):
        """测试验证多余节点的顺序"""
        ts = TopologicalSort()
        ts.add_node('A')
        
        self.assertFalse(ts.is_valid_order(['A', 'B']))


class TestGraphOperations(unittest.TestCase):
    """图操作测试"""
    
    def test_reverse(self):
        """测试反向图"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('B', 'C')
        
        reversed_ts = ts.reverse()
        self.assertEqual(reversed_ts.get_dependencies('B'), {'A'})
        self.assertEqual(reversed_ts.get_dependencies('C'), {'B'})
    
    def test_copy(self):
        """测试深拷贝"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        
        copied = ts.copy()
        copied.add_edge('B', 'C')
        
        self.assertEqual(ts.edge_count, 1)
        self.assertEqual(copied.edge_count, 2)
    
    def test_merge(self):
        """测试合并图"""
        ts1 = TopologicalSort()
        ts1.add_edge('A', 'B')
        
        ts2 = TopologicalSort()
        ts2.add_edge('C', 'D')
        
        merged = ts1.merge(ts2)
        self.assertEqual(merged.node_count, 4)
        self.assertEqual(merged.edge_count, 2)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_empty_graph(self):
        """测试空图"""
        ts = TopologicalSort()
        self.assertEqual(ts.sort_kahn(), [])
        self.assertEqual(ts.layers(), [])
    
    def test_single_node(self):
        """测试单节点"""
        ts = TopologicalSort()
        ts.add_node('A')
        self.assertEqual(ts.sort_kahn(), ['A'])
        self.assertEqual(ts.layers(), [['A']])
    
    def test_duplicate_edges(self):
        """测试重复边"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        ts.add_edge('A', 'B')  # 重复添加
        
        self.assertEqual(ts.edge_count, 1)  # 边只存储一次
        self.assertEqual(ts.sort_kahn(), ['B', 'A'])
    
    def test_numeric_nodes(self):
        """测试数字节点"""
        ts = TopologicalSort()
        ts.add_edge(1, 2)
        ts.add_edge(2, 3)
        
        result = ts.sort_kahn()
        self.assertEqual(result, [3, 2, 1])
    
    def test_tuple_nodes(self):
        """测试元组节点"""
        ts = TopologicalSort()
        ts.add_edge(('task', 1), ('task', 0))
        
        result = ts.sort_kahn()
        self.assertEqual(result, [('task', 0), ('task', 1)])


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_topological_sort_function(self):
        """测试 topological_sort 函数"""
        nodes = ['A', 'B', 'C', 'D']
        edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')]
        
        result = topological_sort(nodes, edges)
        self.assertEqual(result[0], 'D')
        self.assertEqual(result[-1], 'A')
    
    def test_parallel_layers_function(self):
        """测试 parallel_layers 函数"""
        nodes = ['A', 'B', 'C']
        edges = [('C', 'A'), ('C', 'B')]
        
        layers = parallel_layers(nodes, edges)
        self.assertIn('A', layers[0])
        self.assertIn('B', layers[0])
        self.assertIn('C', layers[1])


class TestStringRepr(unittest.TestCase):
    """字符串表示测试"""
    
    def test_repr(self):
        """测试 __repr__"""
        ts = TopologicalSort()
        ts.add_edge('A', 'B')
        
        repr_str = repr(ts)
        self.assertIn('nodes=2', repr_str)
        self.assertIn('edges=1', repr_str)
    
    def test_len(self):
        """测试 __len__"""
        ts = TopologicalSort()
        ts.add_node('A')
        ts.add_node('B')
        
        self.assertEqual(len(ts), 2)
    
    def test_iter(self):
        """测试 __iter__"""
        ts = TopologicalSort()
        ts.add_node('A')
        ts.add_node('B')
        
        nodes = set(ts)
        self.assertEqual(nodes, {'A', 'B'})


class TestRealWorldScenarios(unittest.TestCase):
    """真实场景测试"""
    
    def test_task_scheduling(self):
        """测试任务调度场景"""
        ts = TopologicalSort()
        # 任务依赖：编译前需要先写代码和测试
        ts.add_edge('compile', 'write_code')
        ts.add_edge('compile', 'write_tests')
        ts.add_edge('deploy', 'compile')
        ts.add_edge('deploy', 'security_review')
        
        order = ts.sort_kahn()
        self.assertTrue(order.index('write_code') < order.index('compile'))
        self.assertTrue(order.index('write_tests') < order.index('compile'))
        self.assertTrue(order.index('compile') < order.index('deploy'))
    
    def test_course_prerequisites(self):
        """测试课程先修关系"""
        ts = TopologicalSort()
        # 课程依赖链
        ts.add_edge('calculus_ii', 'calculus_i')
        ts.add_edge('linear_algebra', 'calculus_i')
        ts.add_edge('machine_learning', 'linear_algebra')
        ts.add_edge('machine_learning', 'calculus_ii')
        ts.add_edge('deep_learning', 'machine_learning')
        
        order = ts.sort_kahn()
        self.assertTrue(order.index('calculus_i') < order.index('calculus_ii'))
        self.assertTrue(order.index('machine_learning') < order.index('deep_learning'))
    
    def test_package_dependencies(self):
        """测试包依赖关系"""
        ts = TopologicalSort()
        # npm/pip 风格的包依赖
        ts.add_edge('myapp', 'react')
        ts.add_edge('myapp', 'lodash')
        ts.add_edge('react', 'react-dom')
        
        order = ts.sort_kahn()
        # react 和 lodash 应该在 myapp 之前
        self.assertTrue(order.index('react') < order.index('myapp'))
        self.assertTrue(order.index('lodash') < order.index('myapp'))
    
    def test_build_system(self):
        """测试构建系统依赖"""
        ts = TopologicalSort()
        # Makefile 风格的依赖
        ts.add_edge('main.o', 'main.c')
        ts.add_edge('utils.o', 'utils.c')
        ts.add_edge('app', 'main.o')
        ts.add_edge('app', 'utils.o')
        
        layers = ts.layers()
        # 第一层：源文件
        source_layer = layers[0]
        self.assertIn('main.c', source_layer)
        self.assertIn('utils.c', source_layer)
        # 最后一层：最终目标
        self.assertIn('app', layers[-1])


if __name__ == '__main__':
    unittest.main()