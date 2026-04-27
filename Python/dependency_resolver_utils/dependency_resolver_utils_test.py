"""
Dependency Resolver Utils 测试模块

测试依赖解析工具的所有核心功能。
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    DependencyGraph,
    ResolutionResult,
    NodeInfo,
    ResolutionError,
    CyclicDependencyError,
    topological_sort,
    resolve_dependencies,
    find_cycles,
)


class TestDependencyGraph(unittest.TestCase):
    """DependencyGraph 测试类"""
    
    def test_add_node(self):
        """测试添加节点"""
        graph = DependencyGraph()
        graph.add_node("A")
        
        self.assertIn("A", graph)
        self.assertEqual(len(graph), 1)
    
    def test_add_node_with_dependencies(self):
        """测试添加带依赖的节点"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        
        self.assertIn("B", graph)
        self.assertEqual(graph.get_dependencies("B"), {"A"})
        self.assertEqual(graph.get_dependents("A"), {"B"})
    
    def test_chain_add(self):
        """测试链式调用"""
        graph = (DependencyGraph()
            .add_node("A")
            .add_node("B", dependencies=["A"])
            .add_node("C", dependencies=["B"]))
        
        self.assertEqual(len(graph), 3)
    
    def test_auto_create_dependency_node(self):
        """测试自动创建依赖节点"""
        graph = DependencyGraph()
        graph.add_node("B")
        graph.add_dependency("B", "A")  # A 不存在，应自动创建
        
        self.assertIn("A", graph)
        self.assertIn("B", graph)
    
    def test_remove_node(self):
        """测试移除节点"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        graph.remove_node("A")
        
        self.assertNotIn("A", graph)
        self.assertEqual(graph.get_dependencies("B"), set())
    
    def test_remove_dependency(self):
        """测试移除依赖"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        graph.remove_dependency("B", "A")
        
        self.assertEqual(graph.get_dependencies("B"), set())
    
    def test_get_roots(self):
        """测试获取根节点"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        graph.add_node("C")
        
        roots = graph.get_roots()
        self.assertIn("A", roots)
        self.assertIn("C", roots)
        self.assertNotIn("B", roots)
    
    def test_get_leaves(self):
        """测试获取叶节点"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        graph.add_node("C", dependencies=["B"])
        
        leaves = graph.get_leaves()
        self.assertEqual(leaves, ["C"])
    
    def test_get_all_dependencies(self):
        """测试获取所有传递依赖"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        graph.add_node("C", dependencies=["B"])
        graph.add_node("D", dependencies=["C"])
        
        all_deps = graph.get_all_dependencies("D")
        self.assertEqual(all_deps, {"A", "B", "C"})
    
    def test_get_all_dependents(self):
        """测试获取所有传递被依赖"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        graph.add_node("C", dependencies=["B"])
        graph.add_node("D", dependencies=["C"])
        
        all_dependents = graph.get_all_dependents("A")
        self.assertEqual(all_dependents, {"B", "C", "D"})


class TestTopologicalSort(unittest.TestCase):
    """拓扑排序测试"""
    
    def test_simple_sort(self):
        """测试简单排序"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        graph.add_node("C", dependencies=["B"])
        
        order = graph.get_execution_order()
        self.assertEqual(order, ["A", "B", "C"])
    
    def test_complex_sort(self):
        """测试复杂排序"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        graph.add_node("C", dependencies=["A"])
        graph.add_node("D", dependencies=["B", "C"])
        graph.add_node("E", dependencies=["D"])
        
        order = graph.get_execution_order()
        
        # A 必须在 B, C 之前
        self.assertLess(order.index("A"), order.index("B"))
        self.assertLess(order.index("A"), order.index("C"))
        # B, C 必须在 D 之前
        self.assertLess(order.index("B"), order.index("D"))
        self.assertLess(order.index("C"), order.index("D"))
        # D 必须在 E 之前
        self.assertLess(order.index("D"), order.index("E"))
    
    def test_multiple_roots(self):
        """测试多个根节点"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B")
        graph.add_node("C", dependencies=["A", "B"])
        
        order = graph.get_execution_order()
        
        # A 和 B 都在 C 之前
        self.assertLess(order.index("A"), order.index("C"))
        self.assertLess(order.index("B"), order.index("C"))
    
    def test_empty_graph(self):
        """测试空图"""
        graph = DependencyGraph()
        order = graph.get_execution_order()
        self.assertEqual(order, [])


class TestCycleDetection(unittest.TestCase):
    """循环检测测试"""
    
    def test_simple_cycle(self):
        """测试简单循环"""
        graph = DependencyGraph()
        graph.add_node("A", dependencies=["B"])
        graph.add_node("B", dependencies=["C"])
        graph.add_node("C", dependencies=["A"])
        
        cycles = graph.detect_cycles()
        self.assertTrue(len(cycles) > 0)
    
    def test_self_cycle(self):
        """测试自循环"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_dependency("A", "A")
        
        cycles = graph.detect_cycles()
        self.assertTrue(len(cycles) > 0)
    
    def test_no_cycle(self):
        """测试无循环"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        graph.add_node("C", dependencies=["B"])
        
        cycles = graph.detect_cycles()
        self.assertEqual(cycles, [])
    
    def test_cycle_error(self):
        """测试循环错误抛出"""
        graph = DependencyGraph()
        graph.add_node("A", dependencies=["B"])
        graph.add_node("B", dependencies=["A"])
        
        with self.assertRaises(CyclicDependencyError):
            graph.resolve()
    
    def test_allow_cycles(self):
        """测试允许循环"""
        graph = DependencyGraph()
        graph.add_node("A", dependencies=["B"])
        graph.add_node("B", dependencies=["A"])
        graph.add_node("C")
        
        result = graph.resolve(allow_cycles=True)
        
        self.assertTrue(result.has_cycles)
        self.assertIn("C", result.order)


class TestParallelLevels(unittest.TestCase):
    """并行层级测试"""
    
    def test_simple_levels(self):
        """测试简单层级"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        graph.add_node("C", dependencies=["A"])
        graph.add_node("D", dependencies=["B", "C"])
        
        levels = graph.get_parallel_levels()
        
        self.assertEqual(len(levels), 3)
        self.assertEqual(levels[0], ["A"])  # 第1层
        self.assertIn("B", levels[1])       # 第2层可并行
        self.assertIn("C", levels[1])
        self.assertEqual(levels[2], ["D"])  # 第3层
    
    def test_max_parallel(self):
        """测试最大并行"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B")
        graph.add_node("C")
        graph.add_node("D", dependencies=["A", "B", "C"])
        
        levels = graph.get_parallel_levels()
        
        # A, B, C 应该在同一层
        self.assertEqual(len(levels[0]), 3)
        self.assertIn("A", levels[0])
        self.assertIn("B", levels[0])
        self.assertIn("C", levels[0])


class TestSerialization(unittest.TestCase):
    """序列化测试"""
    
    def test_to_dict(self):
        """测试转换为字典"""
        graph = DependencyGraph(name="TestGraph")
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        
        data = graph.to_dict()
        
        self.assertEqual(data["name"], "TestGraph")
        self.assertIn("A", data["nodes"])
        self.assertIn("B", data["nodes"])
        self.assertEqual(data["nodes"]["B"]["dependencies"], ["A"])
    
    def test_from_dict(self):
        """测试从字典创建"""
        data = {
            "name": "TestGraph",
            "nodes": {
                "A": {"dependencies": [], "dependents": ["B"], "metadata": {}},
                "B": {"dependencies": ["A"], "dependents": [], "metadata": {}}
            }
        }
        
        graph = DependencyGraph.from_dict(data)
        
        self.assertEqual(graph.name, "TestGraph")
        self.assertIn("A", graph)
        self.assertIn("B", graph)
        self.assertEqual(graph.get_dependencies("B"), {"A"})
    
    def test_to_json_from_json(self):
        """测试JSON序列化循环"""
        graph = DependencyGraph(name="TestGraph")
        graph.add_node("A", metadata={"version": "1.0"})
        graph.add_node("B", dependencies=["A"])
        
        json_str = graph.to_json()
        graph2 = DependencyGraph.from_json(json_str)
        
        self.assertEqual(graph2.name, "TestGraph")
        self.assertIn("A", graph2)
        self.assertEqual(graph2.get_dependencies("B"), {"A"})
    
    def test_copy(self):
        """测试复制"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        
        graph2 = graph.copy()
        
        # 修改原图不影响副本
        graph.remove_node("A")
        self.assertIn("A", graph2)
        self.assertNotIn("A", graph)


class TestSubgraph(unittest.TestCase):
    """子图测试"""
    
    def test_subgraph(self):
        """测试创建子图"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        graph.add_node("C", dependencies=["B"])
        graph.add_node("D")  # 不相关的节点
        
        sub = graph.subgraph(["C"])
        
        # 子图应该包含 C 及其所有依赖 (A, B)
        self.assertIn("A", sub)
        self.assertIn("B", sub)
        self.assertIn("C", sub)
        self.assertNotIn("D", sub)


class TestVisualization(unittest.TestCase):
    """可视化测试"""
    
    def test_visualize(self):
        """测试可视化输出"""
        graph = DependencyGraph(name="TestGraph")
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        graph.add_node("C", dependencies=["A"])
        
        viz = graph.visualize()
        
        self.assertIn("TestGraph", viz)
        self.assertIn("A", viz)
        self.assertIn("节点总数: 3", viz)
        self.assertIn("根节点数: 1", viz)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_topological_sort(self):
        """测试拓扑排序便捷函数"""
        deps = {"C": ["A", "B"], "B": ["A"], "A": []}
        order = topological_sort(deps)
        
        self.assertEqual(order, ["A", "B", "C"])
    
    def test_resolve_dependencies(self):
        """测试依赖解析便捷函数"""
        deps = {"C": ["A", "B"], "B": ["A"], "A": []}
        result = resolve_dependencies(deps)
        
        self.assertEqual(result.order, ["A", "B", "C"])
        self.assertEqual(len(result.levels), 3)
        self.assertFalse(result.has_cycles)
    
    def test_find_cycles(self):
        """测试循环检测便捷函数"""
        deps = {"A": ["B"], "B": ["C"], "C": ["A"]}
        cycles = find_cycles(deps)
        
        self.assertTrue(len(cycles) > 0)
    
    def test_find_cycles_none(self):
        """测试无循环便捷函数"""
        deps = {"C": ["A", "B"], "B": ["A"], "A": []}
        cycles = find_cycles(deps)
        
        self.assertEqual(cycles, [])


class TestNodeInfo(unittest.TestCase):
    """节点信息测试"""
    
    def test_node_properties(self):
        """测试节点属性"""
        info = NodeInfo(name="Test", dependencies={"A", "B"}, dependents={"C"})
        
        self.assertEqual(info.in_degree, 2)
        self.assertEqual(info.out_degree, 1)
        self.assertFalse(info.is_root)
        self.assertFalse(info.is_leaf)
    
    def test_root_leaf(self):
        """测试根节点和叶节点判断"""
        root = NodeInfo(name="Root")
        self.assertTrue(root.is_root)
        
        leaf = NodeInfo(name="Leaf", dependencies={"X"})
        self.assertTrue(leaf.is_leaf)


class TestResolutionResult(unittest.TestCase):
    """解析结果测试"""
    
    def test_to_dict(self):
        """测试结果转字典"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        
        result = graph.resolve()
        data = result.to_dict()
        
        self.assertIn("order", data)
        self.assertIn("levels", data)
        self.assertEqual(data["order"], ["A", "B"])
    
    def test_to_json(self):
        """测试结果转JSON"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        
        result = graph.resolve()
        json_str = result.to_json()
        
        self.assertIn('"order"', json_str)
        self.assertIn("A", json_str)
        self.assertIn("B", json_str)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_empty_node_name(self):
        """测试空节点名称"""
        graph = DependencyGraph()
        
        with self.assertRaises(ValueError):
            graph.add_node("")
        
        with self.assertRaises(ValueError):
            graph.add_node("   ")
    
    def test_nonexistent_node(self):
        """测试不存在的节点"""
        graph = DependencyGraph()
        
        with self.assertRaises(ValueError):
            graph.get_dependencies("NonExistent")
        
        with self.assertRaises(ValueError):
            graph.get_all_dependencies("NonExistent")
    
    def test_large_graph(self):
        """测试大图"""
        graph = DependencyGraph()
        
        # 创建链式依赖 A -> B -> C -> ... -> Z
        nodes = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        for i, node in enumerate(nodes):
            if i == 0:
                graph.add_node(node)
            else:
                graph.add_node(node, dependencies=[nodes[i-1]])
        
        order = graph.get_execution_order()
        self.assertEqual(order, nodes)
    
    def test_diamond_dependency(self):
        """测试菱形依赖"""
        graph = DependencyGraph()
        graph.add_node("A")
        graph.add_node("B", dependencies=["A"])
        graph.add_node("C", dependencies=["A"])
        graph.add_node("D", dependencies=["B", "C"])
        
        order = graph.get_execution_order()
        
        # A 在 B, C 之前
        self.assertLess(order.index("A"), order.index("B"))
        self.assertLess(order.index("A"), order.index("C"))
        # B, C 在 D 之前
        self.assertLess(order.index("B"), order.index("D"))
        self.assertLess(order.index("C"), order.index("D"))


if __name__ == "__main__":
    unittest.main(verbosity=2)