#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Maze Utilities Test Suite
=======================================
Comprehensive tests for the maze_utils module.

Run with: python maze_utils_test.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maze_utils.mod import (
    Maze, MazeCell, MazeSolution, MazeMetrics,
    Cell, Direction,
    create_maze, solve_maze, maze_from_string,
    compare_solvers, get_path_directions,
    generate_maze_collection,
    print_maze_with_solution
)

import unittest


class TestMazeCreation(unittest.TestCase):
    """Test maze creation and initialization."""
    
    def test_maze_creation(self):
        """Test basic maze creation."""
        maze = Maze(10, 10)
        self.assertEqual(maze.width, 11)  # Adjusted to odd
        self.assertEqual(maze.height, 11)  # Adjusted to odd
    
    def test_maze_creation_odd_dimensions(self):
        """Test maze creation with odd dimensions."""
        maze = Maze(11, 15)
        self.assertEqual(maze.width, 11)
        self.assertEqual(maze.height, 15)
    
    def test_maze_creation_with_seed(self):
        """Test maze creation with seed for reproducibility."""
        maze1 = Maze(11, 11, seed=42)
        maze2 = Maze(11, 11, seed=42)
        self.assertEqual(maze1.width, maze2.width)
        self.assertEqual(maze1.height, maze2.height)
    
    def test_maze_grid_initialization(self):
        """Test that maze grid is initialized with walls."""
        maze = Maze(11, 11)
        for y in range(maze.height):
            for x in range(maze.width):
                self.assertEqual(maze.get_cell(x, y), Cell.WALL.value)
    
    def test_maze_start_end_positions(self):
        """Test default start and end positions."""
        maze = Maze(11, 11)
        self.assertEqual(maze.start, (1, 1))
        self.assertEqual(maze.end, (9, 9))


class TestMazeGeneration(unittest.TestCase):
    """Test maze generation algorithms."""
    
    def test_generate_dfs(self):
        """Test DFS maze generation."""
        maze = create_maze(11, 11, 'dfs', seed=42)
        
        # Check that paths exist
        self.assertTrue(maze.is_path(maze.start[0], maze.start[1]))
        self.assertTrue(maze.is_path(maze.end[0], maze.end[1]))
        
        # Check that maze is solvable
        solution = maze.solve_bfs()
        self.assertIsNotNone(solution)
    
    def test_generate_prim(self):
        """Test Prim's algorithm maze generation."""
        maze = create_maze(11, 11, 'prim', seed=42)
        
        self.assertTrue(maze.is_path(maze.start[0], maze.start[1]))
        solution = maze.solve_bfs()
        self.assertIsNotNone(solution)
    
    def test_generate_kruskal(self):
        """Test Kruskal's algorithm maze generation."""
        maze = create_maze(11, 11, 'kruskal', seed=42)
        
        self.assertTrue(maze.is_path(maze.start[0], maze.start[1]))
        solution = maze.solve_bfs()
        self.assertIsNotNone(solution)
    
    def test_generate_eller(self):
        """Test Eller's algorithm maze generation."""
        maze = create_maze(11, 11, 'eller', seed=42)
        
        self.assertTrue(maze.is_path(maze.start[0], maze.start[1]))
        solution = maze.solve_bfs()
        self.assertIsNotNone(solution)
    
    def test_invalid_algorithm(self):
        """Test invalid algorithm raises error."""
        with self.assertRaises(ValueError):
            create_maze(11, 11, 'invalid')
    
    def test_maze_has_boundary_walls(self):
        """Test that maze has boundary walls."""
        maze = create_maze(11, 11, 'dfs')
        
        # Check boundary walls
        for x in range(maze.width):
            self.assertTrue(maze.is_wall(x, 0))
            self.assertTrue(maze.is_wall(x, maze.height - 1))
        
        for y in range(maze.height):
            self.assertTrue(maze.is_wall(0, y))
            self.assertTrue(maze.is_wall(maze.width - 1, y))


class TestMazeSolving(unittest.TestCase):
    """Test maze solving algorithms."""
    
    def setUp(self):
        """Create a maze for testing."""
        self.maze = create_maze(15, 15, 'dfs', seed=42)
    
    def test_solve_dfs(self):
        """Test DFS maze solving."""
        solution = self.maze.solve_dfs()
        self.assertIsNotNone(solution)
        self.assertEqual(solution.algorithm, 'DFS')
        self.assertTrue(len(solution.path) > 0)
    
    def test_solve_bfs(self):
        """Test BFS maze solving."""
        solution = self.maze.solve_bfs()
        self.assertIsNotNone(solution)
        self.assertEqual(solution.algorithm, 'BFS')
        self.assertTrue(len(solution.path) > 0)
    
    def test_solve_a_star(self):
        """Test A* maze solving."""
        solution = self.maze.solve_a_star()
        self.assertIsNotNone(solution)
        self.assertEqual(solution.algorithm, 'A*')
        self.assertTrue(len(solution.path) > 0)
    
    def test_solve_dead_end_filling(self):
        """Test dead-end filling maze solving."""
        solution = self.maze.solve_dead_end_filling()
        self.assertIsNotNone(solution)
        self.assertEqual(solution.algorithm, 'Dead-End Filling')
        self.assertTrue(len(solution.path) > 0)
    
    def test_bfs_finds_shortest_path(self):
        """Test that BFS finds the shortest path."""
        bfs_solution = self.maze.solve_bfs()
        dfs_solution = self.maze.solve_dfs()
        
        self.assertTrue(bfs_solution.steps <= dfs_solution.steps)
    
    def test_path_starts_at_start(self):
        """Test that solution path starts at start position."""
        solution = self.maze.solve_bfs()
        self.assertEqual(solution.path[0], self.maze.start)
    
    def test_path_ends_at_end(self):
        """Test that solution path ends at end position."""
        solution = self.maze.solve_bfs()
        self.assertEqual(solution.path[-1], self.maze.end)
    
    def test_solve_maze_function(self):
        """Test solve_maze function."""
        solution = solve_maze(self.maze, 'bfs')
        self.assertIsNotNone(solution)
        self.assertEqual(solution.algorithm, 'BFS')
    
    def test_invalid_solver(self):
        """Test invalid solver raises error."""
        with self.assertRaises(ValueError):
            solve_maze(self.maze, 'invalid')


class TestMazeSolution(unittest.TestCase):
    """Test MazeSolution data class."""
    
    def setUp(self):
        """Create a maze and solution for testing."""
        self.maze = create_maze(11, 11, 'dfs', seed=42)
        self.solution = self.maze.solve_bfs()
    
    def test_to_directions(self):
        """Test direction conversion."""
        directions = self.solution.to_directions()
        
        # All directions should be valid
        valid = {'N', 'S', 'E', 'W'}
        for d in directions:
            self.assertIn(d, valid)
    
    def test_get_path_directions(self):
        """Test get_path_directions function."""
        directions = get_path_directions(self.solution)
        self.assertEqual(len(directions), self.solution.steps)


class TestMazeAnalysis(unittest.TestCase):
    """Test maze analysis functions."""
    
    def setUp(self):
        """Create a maze for analysis."""
        self.maze = create_maze(21, 21, 'dfs', seed=42)
    
    def test_analyze(self):
        """Test maze analysis."""
        metrics = self.maze.analyze()
        
        self.assertEqual(metrics.width, self.maze.width)
        self.assertEqual(metrics.height, self.maze.height)
        self.assertTrue(metrics.path_cells > 0)
        self.assertTrue(metrics.wall_cells > 0)
        self.assertTrue(metrics.dead_ends >= 0)
        self.assertTrue(metrics.branching_points >= 0)
        self.assertTrue(0 <= metrics.difficulty_score <= 100)
    
    def test_find_dead_ends(self):
        """Test dead end finding."""
        dead_ends = self.maze.find_dead_ends()
        self.assertTrue(len(dead_ends) >= 0)
        
        metrics = self.maze.analyze()
        self.assertEqual(len(dead_ends), metrics.dead_ends)
    
    def test_find_branching_points(self):
        """Test branching point finding."""
        branches = self.maze.find_branching_points()
        self.assertTrue(len(branches) >= 0)
        
        metrics = self.maze.analyze()
        self.assertEqual(len(branches), metrics.branching_points)


class TestMazeFromString(unittest.TestCase):
    """Test creating maze from string."""
    
    def test_maze_from_string(self):
        """Test creating maze from ASCII string."""
        text = """
#####
#S  #
# # #
#  E#
#####
"""
        maze = maze_from_string(text)
        
        self.assertEqual(maze.width, 5)
        self.assertEqual(maze.height, 5)
        self.assertEqual(maze.start, (1, 1))
        self.assertEqual(maze.end, (3, 3))
    
    def test_maze_from_string_solvable(self):
        """Test that maze from string is solvable."""
        text = """
#######
#S    #
# ### #
# #   #
#   # #
#####E#
#######
"""
        maze = maze_from_string(text)
        solution = maze.solve_bfs()
        self.assertIsNotNone(solution)
    
    def test_maze_from_empty_string(self):
        """Test that empty string raises error."""
        with self.assertRaises(ValueError):
            maze_from_string("")
    
    def test_maze_from_string_preserves_structure(self):
        """Test that maze from string preserves original structure."""
        text = """
#####
#S E#
#####
"""
        maze = maze_from_string(text)
        
        # Should be a 1-row path
        self.assertTrue(maze.is_path(1, 1))
        self.assertTrue(maze.is_path(2, 1))
        self.assertTrue(maze.is_path(3, 1))


class TestMazeOutput(unittest.TestCase):
    """Test maze output functions."""
    
    def test_to_ascii(self):
        """Test ASCII output."""
        maze = create_maze(7, 7, 'dfs', seed=42)
        ascii_str = maze.to_ascii()
        
        # Should have correct number of lines
        lines = ascii_str.split('\n')
        self.assertEqual(len(lines), maze.height)
        
        # Each line should have correct width
        for line in lines:
            self.assertEqual(len(line), maze.width)
    
    def test_to_ascii_with_solution(self):
        """Test ASCII output with solution."""
        maze = create_maze(7, 7, 'dfs', seed=42)
        maze.solve_bfs()
        ascii_str = maze.to_ascii(show_solution=True)
        
        self.assertTrue(len(ascii_str) > 0)
    
    def test_str_representation(self):
        """Test string representation."""
        maze = create_maze(7, 7, 'dfs')
        str_repr = str(maze)
        
        self.assertTrue(len(str_repr) > 0)
    
    def test_repr(self):
        """Test repr representation."""
        maze = Maze(11, 11)
        repr_str = repr(maze)
        
        self.assertIn('Maze', repr_str)
        self.assertIn('width', repr_str)
        self.assertIn('height', repr_str)
    
    def test_to_dict(self):
        """Test dictionary representation."""
        maze = create_maze(7, 7, 'dfs')
        data = maze.to_dict()
        
        self.assertIn('width', data)
        self.assertIn('height', data)
        self.assertIn('grid', data)
        self.assertIn('start', data)
        self.assertIn('end', data)


class TestCompareSolvers(unittest.TestCase):
    """Test solver comparison."""
    
    def test_compare_solvers(self):
        """Test comparing all solvers."""
        maze = create_maze(15, 15, 'dfs', seed=42)
        results = compare_solvers(maze)
        
        # Should have results for all algorithms
        self.assertIn('dfs', results)
        self.assertIn('bfs', results)
        self.assertIn('a_star', results)
        self.assertIn('dead_end_filling', results)
        
        # BFS should be shortest or equal
        for name, sol in results.items():
            if name != 'bfs':
                self.assertTrue(results['bfs'].steps <= sol.steps)


class TestMazeCollection(unittest.TestCase):
    """Test maze collection generation."""
    
    def test_generate_collection(self):
        """Test generating multiple mazes."""
        mazes = generate_maze_collection(5)
        self.assertEqual(len(mazes), 5)
        
        for maze in mazes:
            self.assertIsInstance(maze, Maze)
    
    def test_collection_sizes(self):
        """Test that collection has varying sizes."""
        mazes = generate_maze_collection(10, min_size=7, max_size=21)
        
        sizes = set()
        for maze in mazes:
            sizes.add(maze.width)
        
        self.assertTrue(len(sizes) > 1)  # Should have different sizes
    
    def test_collection_solvability(self):
        """Test that all mazes in collection are solvable."""
        mazes = generate_maze_collection(5)
        
        for maze in mazes:
            solution = maze.solve_bfs()
            self.assertIsNotNone(solution)


class TestMazeCellMethods(unittest.TestCase):
    """Test maze cell methods."""
    
    def test_is_path(self):
        """Test is_path method."""
        maze = create_maze(11, 11, 'dfs')
        
        self.assertTrue(maze.is_path(maze.start[0], maze.start[1]))
        self.assertTrue(maze.is_path(maze.end[0], maze.end[1]))
        self.assertTrue(maze.is_wall(0, 0))  # Boundary wall
    
    def test_is_wall(self):
        """Test is_wall method."""
        maze = create_maze(11, 11, 'dfs')
        
        self.assertTrue(maze.is_wall(0, 0))
        self.assertTrue(maze.is_wall(maze.width - 1, maze.height - 1))
    
    def test_get_cell(self):
        """Test get_cell method."""
        maze = Maze(11, 11)
        
        self.assertEqual(maze.get_cell(0, 0), Cell.WALL.value)
        self.assertEqual(maze.get_cell(-1, 0), Cell.WALL.value)  # Out of bounds
    
    def test_set_cell(self):
        """Test set_cell method."""
        maze = Maze(11, 11)
        
        maze.set_cell(1, 1, Cell.PATH.value)
        self.assertEqual(maze.get_cell(1, 1), Cell.PATH.value)
    
    def test_get_neighbors(self):
        """Test get_neighbors method."""
        maze = Maze(11, 11)
        
        neighbors = maze.get_neighbors(5, 5)
        self.assertEqual(len(neighbors), 4)
        
        # Should include all four directions
        coords = set(neighbors)
        expected = {(5, 4), (5, 6), (4, 5), (6, 5)}
        self.assertEqual(coords, expected)


class TestMazeDataClasses(unittest.TestCase):
    """Test maze data classes."""
    
    def test_maze_cell(self):
        """Test MazeCell class."""
        cell = MazeCell(5, 10)
        self.assertEqual(cell.x, 5)
        self.assertEqual(cell.y, 10)
        self.assertTrue(cell.is_wall)
    
    def test_maze_cell_hash(self):
        """Test MazeCell hash."""
        cell1 = MazeCell(5, 10)
        cell2 = MazeCell(5, 10)
        
        self.assertEqual(hash(cell1), hash(cell2))
    
    def test_maze_cell_equality(self):
        """Test MazeCell equality."""
        cell1 = MazeCell(5, 10)
        cell2 = MazeCell(5, 10)
        cell3 = MazeCell(5, 11)
        
        self.assertEqual(cell1, cell2)
        self.assertNotEqual(cell1, cell3)
    
    def test_maze_metrics(self):
        """Test MazeMetrics class."""
        metrics = MazeMetrics(
            width=11, height=11,
            total_cells=121,
            path_cells=40, wall_cells=81,
            dead_ends=5, branching_points=3,
            longest_path=20, shortest_path=15,
            difficulty_score=45.0
        )
        
        self.assertEqual(metrics.width, 11)
        self.assertEqual(metrics.difficulty_score, 45.0)


class TestDirectionEnum(unittest.TestCase):
    """Test Direction enum."""
    
    def test_direction_values(self):
        """Test direction coordinate values."""
        self.assertEqual(Direction.NORTH.value, (0, -1))
        self.assertEqual(Direction.SOUTH.value, (0, 1))
        self.assertEqual(Direction.EAST.value, (1, 0))
        self.assertEqual(Direction.WEST.value, (-1, 0))
    
    def test_direction_count(self):
        """Test that we have exactly four directions."""
        self.assertEqual(len(list(Direction)), 4)


class TestCellEnum(unittest.TestCase):
    """Test Cell enum."""
    
    def test_cell_values(self):
        """Test cell character values."""
        self.assertEqual(Cell.WALL.value, '#')
        self.assertEqual(Cell.PATH.value, ' ')
        self.assertEqual(Cell.START.value, 'S')
        self.assertEqual(Cell.END.value, 'E')
        self.assertEqual(Cell.VISITED.value, '.')
        self.assertEqual(Cell.SOLUTION.value, '*')


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestMazeCreation))
    suite.addTests(loader.loadTestsFromTestCase(TestMazeGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestMazeSolving))
    suite.addTests(loader.loadTestsFromTestCase(TestMazeSolution))
    suite.addTests(loader.loadTestsFromTestCase(TestMazeAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestMazeFromString))
    suite.addTests(loader.loadTestsFromTestCase(TestMazeOutput))
    suite.addTests(loader.loadTestsFromTestCase(TestCompareSolvers))
    suite.addTests(loader.loadTestsFromTestCase(TestMazeCollection))
    suite.addTests(loader.loadTestsFromTestCase(TestMazeCellMethods))
    suite.addTests(loader.loadTestsFromTestCase(TestMazeDataClasses))
    suite.addTests(loader.loadTestsFromTestCase(TestDirectionEnum))
    suite.addTests(loader.loadTestsFromTestCase(TestCellEnum))
    
    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)