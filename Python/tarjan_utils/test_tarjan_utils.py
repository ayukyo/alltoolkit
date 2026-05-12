"""
Tarjan Utils Tests
"""

import unittest
import sys
sys.path.insert(0, '.')

from tarjan_utils import (
    tarjan, tarjan_with_info, is_strongly_connected, count_scc,
    largest_scc, smallest_scc, find_cycles, has_cycle,
    condensation_graph, scc_sizes, scc_distribution,
    get_scc_for_node, is_in_cycle, build_scc_adjacency,
    sort_nodes_by_scc, from_edge_list, from_adjacency_matrix,
    TarjanResult
)


class TestBasicOperations(unittest.TestCase):
    """基本操作测试"""
    
    def test_simple_scc(self):
        """测试简单的 SCC"""
        # 0->1->2->0 形成一个 SCC
        graph = {
            0: [1],
            1: [2],
            2: [0]
        }
        sccs = tarjan(graph)
        self.assertEqual(len(sccs), 1)
        self.assertEqual(set(sccs[0]), {0, 1, 2})
    
    def test_two_sccs(self):
        """测试两个 SCC"""
        # SCC 1: 0->1->2->0
        # SCC 2: 3->4->3
        graph = {
            0: [1],
            1: [2],
            2: [0, 3],
            3: [4],
            4: [3]
        }
        sccs = tarjan(graph)
        self.assertEqual(len(sccs), 2)
        
        # 检查 SCC 内容（顺序可能不同）
        scc_sets = [set(scc) for scc in sccs]
        self.assertIn({0, 1, 2}, scc_sets)
        self.assertIn({3, 4}, scc_sets)
    
    def test_dag(self):
        """测试 DAG（无环图）"""
        graph = {
            0: [1, 2],
            1: [3],
            2: [3],
            3: []
        }
        sccs = tarjan(graph)
        self.assertEqual(len(sccs), 4)  # 每个节点都是独立的 SCC
        
        result = tarjan_with_info(graph)
        self.assertTrue(result.is_dag)
    
    def test_isolated_nodes(self):
        """测试孤立节点"""
        graph = {
            0: [],
            1: [],
            2: []
        }
        sccs = tarjan(graph)
        self.assertEqual(len(sccs), 3)
        
        for scc in sccs:
            self.assertEqual(len(scc), 1)
    
    def test_self_loop(self):
        """测试自环"""
        graph = {
            0: [0]  # 自环
        }
        sccs = tarjan(graph)
        self.assertEqual(len(sccs), 1)
        self.assertEqual(sccs[0], [0])
        
        self.assertTrue(has_cycle(graph))


class TestStrongConnectivity(unittest.TestCase):
    """强连通性测试"""
    
    def test_strongly_connected(self):
        """测试强连通图"""
        graph = {
            0: [1],
            1: [2],
            2: [3],
            3: [0]
        }
        self.assertTrue(is_strongly_connected(graph))
    
    def test_not_strongly_connected(self):
        """测试非强连通图"""
        graph = {
            0: [1],
            1: [2],
            2: []  # 不能回到起点
        }
        self.assertFalse(is_strongly_connected(graph))
    
    def test_single_node(self):
        """测试单个节点"""
        graph = {0: []}
        self.assertTrue(is_strongly_connected(graph))


class TestSCCCount(unittest.TestCase):
    """SCC 数量测试"""
    
    def test_count(self):
        """测试 SCC 数量"""
        graph = {
            0: [1], 1: [2], 2: [0],  # SCC 1
            3: [4], 4: [3],          # SCC 2
            5: []                     # SCC 3
        }
        self.assertEqual(count_scc(graph), 3)


class TestLargestSmallestSCC(unittest.TestCase):
    """最大/最小 SCC 测试"""
    
    def test_largest_scc(self):
        """测试最大 SCC"""
        graph = {
            0: [1], 1: [2], 2: [0, 3], 3: [4, 5], 4: [5], 5: [4]
        }
        largest = largest_scc(graph)
        # 最大的 SCC 是 {0, 1, 2} 或 {4, 5}
        self.assertTrue(len(largest) >= 2)
    
    def test_smallest_scc(self):
        """测试最小 SCC"""
        graph = {
            0: [1], 1: [0],  # SCC with 2 nodes
            2: []             # SCC with 1 node
        }
        smallest = smallest_scc(graph)
        # 应该返回最小的多节点 SCC 或单节点 SCC
        self.assertTrue(len(smallest) >= 1)
    
    def test_empty_graph(self):
        """测试空图"""
        graph = {}
        self.assertEqual(largest_scc(graph), [])
        self.assertEqual(smallest_scc(graph), [])


class TestCycles(unittest.TestCase):
    """环检测测试"""
    
    def test_find_cycles(self):
        """测试查找环"""
        graph = {
            0: [1], 1: [2], 2: [0],  # Cycle 1
            3: [4], 4: [3],          # Cycle 2
            5: []                     # No cycle
        }
        cycles = find_cycles(graph)
        self.assertEqual(len(cycles), 2)
    
    def test_has_cycle(self):
        """测试环检测"""
        graph_with_cycle = {0: [1], 1: [0]}
        self.assertTrue(has_cycle(graph_with_cycle))
        
        graph_no_cycle = {0: [1], 1: []}
        self.assertFalse(has_cycle(graph_no_cycle))
    
    def test_is_in_cycle(self):
        """测试节点是否在环中"""
        graph = {
            0: [1], 1: [0],  # Cycle
            2: []             # Not in cycle
        }
        self.assertTrue(is_in_cycle(graph, 0))
        self.assertTrue(is_in_cycle(graph, 1))
        self.assertFalse(is_in_cycle(graph, 2))


class TestCondensationGraph(unittest.TestCase):
    """缩点图测试"""
    
    def test_condensation(self):
        """测试缩点图构建"""
        graph = {
            0: [1], 1: [2], 2: [0, 3],  # SCC 0: {0,1,2}
            3: [4], 4: [3]              # SCC 1: {3,4}
        }
        condensed = condensation_graph(graph)
        
        # 缩点图应该有 2 个节点（代表 2 个 SCC）
        self.assertEqual(len(condensed), 1)  # SCC 0 -> SCC 1
        
        result = tarjan_with_info(graph)
        # 验证缩点图是 DAG
        condensed_result = tarjan_with_info(condensed)
        self.assertTrue(condensed_result.is_dag)
    
    def test_dag_condensation(self):
        """测试 DAG 的缩点图"""
        graph = {0: [1], 1: [2], 2: []}
        condensed = condensation_graph(graph)
        
        # DAG 的缩点图是自身
        self.assertEqual(len(condensed), 2)  # 0->1, 1->2


class TestSCCSizes(unittest.TestCase):
    """SCC 大小测试"""
    
    def test_scc_sizes(self):
        """测试 SCC 大小"""
        graph = {
            0: [1], 1: [2], 2: [0],  # Size 3
            3: [],                     # Size 1
            4: []                      # Size 1
        }
        sizes = scc_sizes(graph)
        self.assertEqual(sorted(sizes), [1, 1, 3])
    
    def test_scc_distribution(self):
        """测试 SCC 分布"""
        graph = {
            0: [1], 1: [0],  # Size 2
            2: [3], 3: [2],  # Size 2
            4: []            # Size 1
        }
        distribution = scc_distribution(graph)
        self.assertEqual(distribution[1], 1)
        self.assertEqual(distribution[2], 2)


class TestNodeOperations(unittest.TestCase):
    """节点操作测试"""
    
    def test_get_scc_for_node(self):
        """测试获取节点的 SCC"""
        graph = {
            0: [1], 1: [0],  # SCC
            2: []             # Isolated
        }
        scc_0 = get_scc_for_node(graph, 0)
        self.assertEqual(set(scc_0), {0, 1})
        
        scc_2 = get_scc_for_node(graph, 2)
        self.assertEqual(scc_2, [2])
    
    def test_missing_node(self):
        """测试不在图中的节点"""
        graph = {0: [1]}
        scc = get_scc_for_node(graph, 5)
        self.assertEqual(scc, [5])


class TestBuildSCCAdjacency(unittest.TestCase):
    """SCC 内部邻接测试"""
    
    def test_scc_adjacency(self):
        """测试 SCC 内部邻接"""
        graph = {
            0: [1], 1: [2], 2: [0, 3],  # SCC
            3: []                         # Outside SCC
        }
        scc_adj = build_scc_adjacency(graph)
        
        result = tarjan_with_info(graph)
        scc_index = result.node_to_scc[0]
        
        # SCC 内部应该有边 0->1, 1->2, 2->0
        self.assertIn(scc_index, scc_adj)


class TestSortNodesBySCC(unittest.TestCase):
    """按 SCC 排序测试"""
    
    def test_sort_by_scc(self):
        """测试按 SCC 排序"""
        graph = {
            0: [1], 1: [2], 2: [0],  # SCC 1
            3: [4], 4: [3]           # SCC 2
        }
        sorted_nodes = sort_nodes_by_scc(graph)
        
        # 所有节点都应该在结果中
        self.assertEqual(set(sorted_nodes), {0, 1, 2, 3, 4})


class TestGraphBuilders(unittest.TestCase):
    """图构建器测试"""
    
    def test_from_edge_list(self):
        """测试从边列表构建"""
        edges = [(0, 1), (1, 2), (2, 0)]
        graph = from_edge_list(edges)
        
        self.assertEqual(set(graph.keys()), {0, 1, 2})
        self.assertEqual(graph[0], [1])
        self.assertEqual(graph[1], [2])
        self.assertEqual(graph[2], [0])
    
    def test_from_adjacency_matrix(self):
        """测试从邻接矩阵构建"""
        matrix = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 0]
        ]
        graph = from_adjacency_matrix(matrix)
        
        self.assertEqual(graph[0], [1])
        self.assertEqual(graph[1], [2])
        self.assertEqual(graph[2], [0])


class TestTarjanResult(unittest.TestCase):
    """TarjanResult 测试"""
    
    def test_result_structure(self):
        """测试结果结构"""
        graph = {0: [1], 1: [0]}
        result = tarjan_with_info(graph)
        
        self.assertEqual(result.scc_count, 1)
        self.assertEqual(len(result.sccs), 1)
        self.assertEqual(set(result.sccs[0]), {0, 1})
        self.assertEqual(result.node_to_scc[0], 0)
        self.assertEqual(result.node_to_scc[1], 0)
        self.assertFalse(result.is_dag)


class TestComplexGraphs(unittest.TestCase):
    """复杂图测试"""
    
    def test_large_cycle(self):
        """测试大环"""
        # 创建一个大环
        n = 100
        graph = {i: [(i + 1) % n] for i in range(n)}
        
        sccs = tarjan(graph)
        self.assertEqual(len(sccs), 1)
        self.assertEqual(len(sccs[0]), n)
        self.assertTrue(is_strongly_connected(graph))
    
    def test_multiple_interconnected_sccs(self):
        """测试多个互联的 SCC"""
        graph = {
            # SCC 1: {0, 1}
            0: [1, 2],
            1: [0],
            # SCC 2: {2, 3}
            2: [3],
            3: [2, 4],
            # SCC 3: {4}
            4: []
        }
        
        sccs = tarjan(graph)
        self.assertEqual(len(sccs), 3)
        
        cycles = find_cycles(graph)
        self.assertEqual(len(cycles), 2)  # {0,1} and {2,3}


class TestStringNodes(unittest.TestCase):
    """字符串节点测试"""
    
    def test_string_keys(self):
        """测试字符串作为节点"""
        graph = {
            "A": ["B"],
            "B": ["C"],
            "C": ["A"]
        }
        sccs = tarjan(graph)
        self.assertEqual(len(sccs), 1)
        self.assertEqual(set(sccs[0]), {"A", "B", "C"})


class TestEmptyGraph(unittest.TestCase):
    """空图测试"""
    
    def test_empty(self):
        """测试空图"""
        graph = {}
        sccs = tarjan(graph)
        self.assertEqual(sccs, [])
        
        self.assertEqual(count_scc(graph), 0)
        self.assertEqual(largest_scc(graph), [])


if __name__ == "__main__":
    unittest.main()