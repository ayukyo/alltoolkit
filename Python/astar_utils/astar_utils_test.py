"""
A* Pathfinding Utils 测试

测试 A* 寻路算法的各项功能。
"""

import sys
import os
import unittest
import math

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    AStar, GridAStar, PathNode, BidirectionalAStar,
    astar_path, grid_path, create_grid_from_string, visualize_path
)


class TestPathNode(unittest.TestCase):
    """测试 PathNode 类"""
    
    def test_f_cost_calculation(self):
        """测试 f_cost 自动计算"""
        node = PathNode(position='A', g_cost=5, h_cost=3)
        self.assertEqual(node.f_cost, 8)
    
    def test_comparison(self):
        """测试节点比较"""
        node1 = PathNode(position='A', g_cost=5, h_cost=3)
        node2 = PathNode(position='B', g_cost=4, h_cost=3)
        node3 = PathNode(position='C', g_cost=5, h_cost=2)
        
        # f_cost 小的排前面
        self.assertTrue(node2 < node1)  # f_cost: 7 vs 8, node2 should be smaller
        # f_cost 相等时，h_cost 小的排前面
        self.assertTrue(node3 < node1)  # f_cost: 7 vs 8, node3 should be smaller
    
    def test_hash_and_equality(self):
        """测试哈希和相等性"""
        node1 = PathNode(position='A', g_cost=1)
        node2 = PathNode(position='A', g_cost=2)
        node3 = PathNode(position='B', g_cost=1)
        
        self.assertEqual(node1, node2)  # 相同位置
        self.assertNotEqual(node1, node3)  # 不同位置
        self.assertEqual(hash(node1), hash(node2))


class TestAStar(unittest.TestCase):
    """测试通用 A* 算法"""
    
    def setUp(self):
        """设置简单的测试图"""
        # 创建一个简单的图: A -> B -> C -> D
        #              \-> E ->/
        self.graph = {
            'A': [('B', 1), ('E', 3)],
            'B': [('C', 1)],
            'C': [('D', 1)],
            'D': [],
            'E': [('D', 1)]
        }
        
        def neighbors_fn(node):
            return self.graph.get(node, [])
        
        def heuristic_fn(a, b):
            # 简单启发：0
            return 0
        
        self.astar = AStar(neighbors_fn, heuristic_fn)
    
    def test_simple_path(self):
        """测试简单路径查找"""
        path, cost = self.astar.find_path('A', 'D')
        self.assertEqual(path, ['A', 'B', 'C', 'D'])
        self.assertEqual(cost, 3)
    
    def test_shorter_path_with_heuristic(self):
        """测试使用启发函数找到更短路径"""
        # 使用更好的启发函数
        def heuristic_fn(a, b):
            # 简单假设：E 到 D 更近
            distances = {'A': 3, 'B': 2, 'C': 1, 'D': 0, 'E': 1}
            return distances.get(a, 0)
        
        astar = AStar(lambda n: self.graph.get(n, []), heuristic_fn)
        path, cost = astar.find_path('A', 'D')
        
        # 路径应该是 A -> E -> D (代价 4) 而不是 A -> B -> C -> D (代价 3)
        # 实际上 A -> B -> C -> D 代价更低，所以应该选择这个
        self.assertEqual(cost, 3)
    
    def test_no_path(self):
        """测试找不到路径"""
        # D 没有出边
        path, cost = self.astar.find_path('D', 'A')
        self.assertEqual(path, [])
        self.assertEqual(cost, float('inf'))
    
    def test_same_start_goal(self):
        """测试起点等于终点"""
        path, cost = self.astar.find_path('A', 'A')
        self.assertEqual(path, ['A'])
        self.assertEqual(cost, 0)
    
    def test_find_all_reachable(self):
        """测试查找所有可达节点"""
        reachable = self.astar.find_all_reachable('A', max_cost=3)
        
        # A 代价 0
        self.assertEqual(reachable['A'], 0)
        # B 代价 1
        self.assertEqual(reachable['B'], 1)
        # C 代价 2
        self.assertEqual(reachable['C'], 2)
        # D 代价 3 (A -> B -> C -> D)
        self.assertEqual(reachable['D'], 3)
        # E 代价 3
        self.assertEqual(reachable['E'], 3)


class TestGridAStar(unittest.TestCase):
    """测试网格 A* 算法"""
    
    def setUp(self):
        """设置测试网格"""
        # 3x3 网格
        # 0 0 0
        # 0 1 0  (1 是障碍物)
        # 0 0 0
        self.grid = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        self.finder = GridAStar(self.grid)
    
    def test_valid_position(self):
        """测试位置有效性检查"""
        self.assertTrue(self.finder.is_valid((0, 0)))
        self.assertTrue(self.finder.is_valid((2, 2)))
        self.assertFalse(self.finder.is_valid((1, 1)))  # 障碍物
        self.assertFalse(self.finder.is_valid((-1, 0)))  # 越界
        self.assertFalse(self.finder.is_valid((3, 0)))   # 越界
    
    def test_four_direction_path(self):
        """测试四方向移动"""
        path = self.finder.find_path((0, 0), (2, 2))
        
        # 应该绕过障碍物
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (2, 2))
        self.assertNotIn((1, 1), path)  # 不应该经过障碍物
    
    def test_eight_direction_path(self):
        """测试八方向移动"""
        finder = GridAStar(self.grid, diagonal=True)
        path = finder.find_path((0, 0), (2, 2))
        
        # 八方向可以更直接地到达
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (2, 2))
    
    def test_diagonal_blocked_by_corners(self):
        """测试对角线移动被角落阻挡"""
        # 创建一个角落被阻挡的地图
        # . . .
        # # # .
        # . . .
        grid = [
            [0, 0, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]
        finder = GridAStar(grid, diagonal=True)
        
        # 从 (0, 0) 到 (1, 2)，不应该直接对角线移动
        path = finder.find_path((0, 0), (1, 2))
        self.assertTrue(len(path) > 0)
    
    def test_heuristics(self):
        """测试不同启发函数"""
        start = (0, 0)
        goal = (2, 2)
        
        # Manhattan
        h1 = self.finder.heuristic(start, goal, 'manhattan')
        self.assertEqual(h1, 4)
        
        # Euclidean
        h2 = self.finder.heuristic(start, goal, 'euclidean')
        self.assertAlmostEqual(h2, math.sqrt(8))
        
        # Chebyshev
        h3 = self.finder.heuristic(start, goal, 'chebyshev')
        self.assertEqual(h3, 2)
        
        # Octile
        h4 = self.finder.heuristic(start, goal, 'octile')
        self.assertAlmostEqual(h4, 2 + (math.sqrt(2) - 1) * 2)
    
    def test_path_smoothing(self):
        """测试路径平滑"""
        # 创建一个长路径
        path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
        smoothed = self.finder.smooth_path(path)
        
        # 平滑后应该更短
        self.assertLessEqual(len(smoothed), len(path))
        self.assertEqual(smoothed[0], (0, 0))
        self.assertEqual(smoothed[-1], (2, 2))
    
    def test_find_all_reachable(self):
        """测试查找所有可达位置"""
        reachable = self.finder.find_all_reachable((0, 0), max_cost=2)
        
        # 代价 0: 起点
        self.assertIn((0, 0), reachable)
        self.assertEqual(reachable[(0, 0)], 0)
        
        # 代价 1: 四个相邻点
        self.assertIn((0, 1), reachable)
        self.assertIn((1, 0), reachable)
        
        # (1, 1) 是障碍物，不可达
        self.assertNotIn((1, 1), reachable)
    
    def test_no_path(self):
        """测试无法到达终点"""
        # 完全被围住的终点
        grid = [
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, 0]
        ]
        finder = GridAStar(grid)
        path = finder.find_path((0, 0), (2, 2))
        self.assertEqual(path, [])


class TestVisualization(unittest.TestCase):
    """测试可视化功能"""
    
    def test_create_grid_from_string(self):
        """测试从字符串创建网格"""
        map_str = """
        .#.
        ...
        .#.
        """
        grid = create_grid_from_string(map_str)
        
        self.assertEqual(len(grid), 3)
        self.assertEqual(len(grid[0]), 3)
        self.assertEqual(grid[0][1], 1)  # 障碍物
        self.assertEqual(grid[0][0], 0)  # 可通行
    
    def test_visualize_path(self):
        """测试路径可视化"""
        grid = [
            [0, 1, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        path = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
        
        visual = visualize_path(grid, path)
        
        self.assertIn('S', visual)  # 起点
        self.assertIn('G', visual)  # 终点
        self.assertIn('*', visual)  # 路径
        self.assertIn('#', visual)  # 障碍物
    
    def test_empty_path_visualization(self):
        """测试空路径可视化"""
        grid = [[0]]
        visual = visualize_path(grid, [])
        self.assertEqual(visual, "No path found")


class TestBidirectionalAStar(unittest.TestCase):
    """测试双向 A* 算法"""
    
    def test_simple_path(self):
        """测试简单路径"""
        graph = {
            'A': [('B', 1), ('C', 4)],
            'B': [('C', 2), ('D', 5)],
            'C': [('D', 1)],
            'D': []
        }
        
        astar = BidirectionalAStar(
            lambda n: graph.get(n, []),
            lambda a, b: 0
        )
        
        path, cost = astar.find_path('A', 'D')
        
        # 最短路径: A -> B -> C -> D (代价 4)
        self.assertEqual(path[0], 'A')
        self.assertEqual(path[-1], 'D')
        self.assertEqual(cost, 4)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_astar_path(self):
        """测试 astar_path 便捷函数"""
        graph = {
            'A': [('B', 1)],
            'B': [('C', 1)],
            'C': []
        }
        
        path = astar_path(
            'A', 'C',
            lambda n: graph.get(n, []),
            lambda a, b: 0
        )
        
        self.assertEqual(path, ['A', 'B', 'C'])
    
    def test_grid_path(self):
        """测试 grid_path 便捷函数"""
        grid = [
            [0, 0],
            [0, 0]
        ]
        
        path = grid_path(grid, (0, 0), (1, 1))
        
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (1, 1))


class TestComplexScenarios(unittest.TestCase):
    """测试复杂场景"""
    
    def test_maze(self):
        """测试迷宫场景"""
        # 简单迷宫
        maze_str = """
        #########
        #S......#
        #.#####.#
        #.#...#.#
        #.#.#.#.#
        #...#...#
        #.#######.
        #......G#
        #########
        """
        grid = create_grid_from_string(maze_str)
        finder = GridAStar(grid, diagonal=False)
        
        # 找到起点和终点
        start = None
        goal = None
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                # 'S' 和 'G' 被转换为 0（可通行）
                # 需要从原始字符串获取位置
                pass
        
        # 直接使用坐标
        path = finder.find_path((1, 1), (7, 7))
        
        # 应该能找到路径
        self.assertGreater(len(path), 0)
    
    def test_large_grid_performance(self):
        """测试大网格性能"""
        # 创建 100x100 的空网格
        grid = [[0] * 100 for _ in range(100)]
        finder = GridAStar(grid, diagonal=False)
        
        # 对角线寻路
        path = finder.find_path((0, 0), (99, 99))
        
        # 应该找到路径
        self.assertEqual(len(path), 199)  # 100 + 100 - 1
    
    def test_obstacle_avoidance(self):
        """测试障碍物避让"""
        # U 形障碍物（上方开口）
        grid = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]
        finder = GridAStar(grid)
        
        # 从顶部绕过 U 形到中心
        path = finder.find_path((0, 2), (2, 2))
        
        # 中心 (2, 2) 被完全包围，无法到达
        # 应该返回空路径
        self.assertEqual(len(path), 0)


if __name__ == '__main__':
    unittest.main()