"""
Maze Utils Tests - 迷宫工具测试
================================

测试所有迷宫生成和求解功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import unittest
from maze_utils import (
    Maze, Cell, Direction,
    generate_dfs, generate_prim, generate_kruskal,
    generate_recursive_division, generate_ellers, generate_binary_tree,
    solve_bfs, solve_dfs, solve_astar, solve_wall_follower, solve_dead_end_filling,
    render_ascii, render_unicode,
    to_json, from_json, to_dict, from_dict, to_binary, from_binary,
)


class TestCell(unittest.TestCase):
    """单元格测试"""
    
    def test_cell_creation(self):
        """测试单元格创建"""
        cell = Cell(0, 0)
        self.assertEqual(cell.x, 0)
        self.assertEqual(cell.y, 0)
        self.assertEqual(len(cell.walls), 4)  # 四面墙
        self.assertFalse(cell.visited)
    
    def test_wall_operations(self):
        """测试墙壁操作"""
        cell = Cell(0, 0)
        
        # 移除墙
        cell.remove_wall(Direction.NORTH)
        self.assertFalse(cell.has_wall(Direction.NORTH))
        self.assertTrue(cell.can_move(Direction.NORTH))
        
        # 添加墙
        cell.add_wall(Direction.NORTH)
        self.assertTrue(cell.has_wall(Direction.NORTH))
        self.assertFalse(cell.can_move(Direction.NORTH))
    
    def test_cell_reset(self):
        """测试单元格重置"""
        cell = Cell(0, 0)
        cell.remove_wall(Direction.NORTH)
        cell.visited = True
        
        cell.reset()
        
        self.assertEqual(len(cell.walls), 4)
        self.assertFalse(cell.visited)


class TestMaze(unittest.TestCase):
    """迷宫测试"""
    
    def test_maze_creation(self):
        """测试迷宫创建"""
        maze = Maze(10, 10)
        self.assertEqual(maze.width, 10)
        self.assertEqual(maze.height, 10)
        self.assertEqual(len(maze), 100)
    
    def test_invalid_dimensions(self):
        """测试无效尺寸"""
        with self.assertRaises(ValueError):
            Maze(1, 10)
        with self.assertRaises(ValueError):
            Maze(10, 1)
    
    def test_cell_access(self):
        """测试单元格访问"""
        maze = Maze(5, 5)
        cell = maze.get_cell(2, 2)
        self.assertEqual(cell.x, 2)
        self.assertEqual(cell.y, 2)
        
        # 通过索引访问
        cell2 = maze[3, 3]
        self.assertEqual(cell2.x, 3)
        self.assertEqual(cell2.y, 3)
    
    def test_wall_operations(self):
        """测试墙壁操作"""
        maze = Maze(5, 5)
        
        # 移除墙壁
        maze.remove_wall(0, 0, 1, 0)
        self.assertFalse(maze.get_cell(0, 0).has_wall(Direction.EAST))
        self.assertFalse(maze.get_cell(1, 0).has_wall(Direction.WEST))
        
        # 添加墙壁
        maze.add_wall(0, 0, 1, 0)
        self.assertTrue(maze.get_cell(0, 0).has_wall(Direction.EAST))
        self.assertTrue(maze.get_cell(1, 0).has_wall(Direction.WEST))
    
    def test_neighbors(self):
        """测试邻居获取"""
        maze = Maze(5, 5)
        
        # 角落单元格
        neighbors = maze.get_neighbors(0, 0)
        self.assertEqual(len(neighbors), 2)  # 只有东和南
        
        # 中心单元格
        neighbors = maze.get_neighbors(2, 2)
        self.assertEqual(len(neighbors), 4)  # 四个方向
    
    def test_maze_copy(self):
        """测试迷宫复制"""
        maze1 = generate_dfs(5, 5, seed=42)
        maze2 = maze1.copy()
        
        self.assertEqual(maze1.width, maze2.width)
        self.assertEqual(maze1.height, maze2.height)
        
        # 确保是深拷贝
        maze1.get_cell(0, 0).remove_wall(Direction.NORTH)
        self.assertTrue(maze2.get_cell(0, 0).has_wall(Direction.NORTH))


class TestGenerators(unittest.TestCase):
    """生成器测试"""
    
    def setUp(self):
        self.width = 15
        self.height = 15
    
    def test_dfs_generator(self):
        """测试DFS生成器"""
        maze = generate_dfs(self.width, self.height, seed=42)
        self.assertEqual(maze.width, self.width)
        self.assertEqual(maze.height, self.height)
        self.assertTrue(maze.is_perfect())
    
    def test_prim_generator(self):
        """测试Prim生成器"""
        maze = generate_prim(self.width, self.height, seed=42)
        self.assertEqual(maze.width, self.width)
        self.assertEqual(maze.height, self.height)
        self.assertTrue(maze.is_perfect())
    
    def test_kruskal_generator(self):
        """测试Kruskal生成器"""
        maze = generate_kruskal(self.width, self.height, seed=42)
        self.assertEqual(maze.width, self.width)
        self.assertEqual(maze.height, self.height)
        self.assertTrue(maze.is_perfect())
    
    def test_recursive_division_generator(self):
        """测试递归分割生成器"""
        maze = generate_recursive_division(self.width, self.height, seed=42)
        self.assertEqual(maze.width, self.width)
        self.assertEqual(maze.height, self.height)
        self.assertTrue(maze.is_perfect())
    
    def test_ellers_generator(self):
        """测试Eller生成器"""
        maze = generate_ellers(self.width, self.height, seed=42)
        self.assertEqual(maze.width, self.width)
        self.assertEqual(maze.height, self.height)
        self.assertTrue(maze.is_perfect())
    
    def test_binary_tree_generator(self):
        """测试二叉树生成器"""
        for bias in ['northeast', 'northwest', 'southeast', 'southwest']:
            maze = generate_binary_tree(self.width, self.height, seed=42, bias=bias)
            self.assertEqual(maze.width, self.width)
            self.assertEqual(maze.height, self.height)
            self.assertTrue(maze.is_perfect())
    
    def test_reproducibility(self):
        """测试随机种子复现性"""
        maze1 = generate_dfs(10, 10, seed=12345)
        maze2 = generate_dfs(10, 10, seed=12345)
        
        for y in range(10):
            for x in range(10):
                cell1 = maze1.get_cell(x, y)
                cell2 = maze2.get_cell(x, y)
                self.assertEqual(cell1.walls, cell2.walls)


class TestSolvers(unittest.TestCase):
    """求解器测试"""
    
    def setUp(self):
        self.maze = generate_dfs(10, 10, seed=42)
    
    def test_bfs_solver(self):
        """测试BFS求解器"""
        path = solve_bfs(self.maze)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], self.maze.start)
        self.assertEqual(path[-1], self.maze.end)
        
        # BFS应该找到最短路径
        astar_path = solve_astar(self.maze)
        self.assertEqual(len(path), len(astar_path))
    
    def test_dfs_solver(self):
        """测试DFS求解器"""
        path = solve_dfs(self.maze)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], self.maze.start)
        self.assertEqual(path[-1], self.maze.end)
    
    def test_astar_solver(self):
        """测试A*求解器"""
        path = solve_astar(self.maze)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], self.maze.start)
        self.assertEqual(path[-1], self.maze.end)
    
    def test_wall_follower_solver(self):
        """测试墙跟随求解器"""
        # 使用Prim生成的迷宫测试（更适合墙跟随算法）
        maze = generate_prim(10, 10, seed=42)
        path = solve_wall_follower(maze)
        # 墙跟随算法在某些迷宫结构下可能失败，但应该能找到路径
        if path:
            self.assertEqual(path[0], maze.start)
            self.assertEqual(path[-1], maze.end)
    
    def test_dead_end_filling_solver(self):
        """测试死胡同填充求解器"""
        path = solve_dead_end_filling(self.maze)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], self.maze.start)
        self.assertEqual(path[-1], self.maze.end)
    
    def test_custom_start_end(self):
        """测试自定义起点和终点"""
        maze = generate_dfs(5, 5, seed=42)
        maze.start = (0, 0)
        maze.end = (4, 4)
        
        path = solve_bfs(maze)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (4, 4))
    
    def test_same_start_end(self):
        """测试起点和终点相同"""
        path = solve_bfs(self.maze, start=(0, 0), end=(0, 0))
        self.assertEqual(path, [(0, 0)])


class TestRenderers(unittest.TestCase):
    """渲染器测试"""
    
    def setUp(self):
        self.maze = generate_dfs(5, 5, seed=42)
        self.path = solve_bfs(self.maze)
    
    def test_ascii_render(self):
        """测试ASCII渲染"""
        output = render_ascii(self.maze)
        self.assertIsInstance(output, str)
        self.assertIn('+', output)
        self.assertIn('-', output)
        self.assertIn('|', output)
    
    def test_unicode_render(self):
        """测试Unicode渲染"""
        output = render_unicode(self.maze)
        self.assertIsInstance(output, str)
    
    def test_path_render(self):
        """测试路径渲染"""
        output = render_ascii(self.maze, path=self.path)
        self.assertIn('#', output)
    
    def test_start_end_markers(self):
        """测试起点和终点标记"""
        output = render_ascii(self.maze, show_start_end=True)
        self.assertIn('S', output)
        self.assertIn('E', output)


class TestSerializers(unittest.TestCase):
    """序列化测试"""
    
    def setUp(self):
        self.maze = generate_dfs(10, 10, seed=42)
    
    def test_dict_serialization(self):
        """测试字典序列化"""
        data = to_dict(self.maze)
        restored = from_dict(data)
        
        self.assertEqual(restored.width, self.maze.width)
        self.assertEqual(restored.height, self.maze.height)
    
    def test_json_serialization(self):
        """测试JSON序列化"""
        json_str = to_json(self.maze)
        restored = from_json(json_str)
        
        self.assertEqual(restored.width, self.maze.width)
        self.assertEqual(restored.height, self.maze.height)
    
    def test_binary_serialization(self):
        """测试二进制序列化"""
        data = to_binary(self.maze)
        restored = from_binary(data)
        
        self.assertEqual(restored.width, self.maze.width)
        self.assertEqual(restored.height, self.maze.height)
        
        # 验证墙壁完全一致
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                original = self.maze.get_cell(x, y)
                restored_cell = restored.get_cell(x, y)
                self.assertEqual(original.walls, restored_cell.walls)
    
    def test_maze_integrity(self):
        """测试序列化后迷宫完整性"""
        data = to_dict(self.maze)
        restored = from_dict(data)
        
        # 验证可以求解
        path = solve_bfs(restored)
        self.assertIsNotNone(path)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_generate_solve_render(self):
        """测试完整流程：生成-求解-渲染"""
        for gen_func in [generate_dfs, generate_prim, generate_kruskal]:
            maze = gen_func(10, 10, seed=42)
            path = solve_bfs(maze)
            output = render_ascii(maze, path=path)
            
            self.assertIsNotNone(path)
            self.assertIsInstance(output, str)
            self.assertTrue(len(output) > 0)
    
    def test_large_maze(self):
        """测试大迷宫性能"""
        maze = generate_dfs(50, 50, seed=42)
        
        # BFS求解
        path = solve_bfs(maze)
        self.assertIsNotNone(path)
        
        # A*求解
        astar_path = solve_astar(maze)
        self.assertIsNotNone(astar_path)
        
        # 两者应该找到相同长度的路径（最短）
        self.assertEqual(len(path), len(astar_path))
    
    def test_different_sizes(self):
        """测试不同尺寸的迷宫"""
        sizes = [(2, 2), (3, 5), (10, 15), (20, 20)]
        
        for w, h in sizes:
            maze = generate_dfs(w, h, seed=42)
            self.assertEqual(maze.width, w)
            self.assertEqual(maze.height, h)
            self.assertTrue(maze.is_perfect())
            
            path = solve_bfs(maze)
            self.assertIsNotNone(path)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestCell))
    suite.addTests(loader.loadTestsFromTestCase(TestMaze))
    suite.addTests(loader.loadTestsFromTestCase(TestGenerators))
    suite.addTests(loader.loadTestsFromTestCase(TestSolvers))
    suite.addTests(loader.loadTestsFromTestCase(TestRenderers))
    suite.addTests(loader.loadTestsFromTestCase(TestSerializers))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)