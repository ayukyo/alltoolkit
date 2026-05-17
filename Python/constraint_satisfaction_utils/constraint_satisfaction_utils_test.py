#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
约束满足问题工具模块测试 (Constraint Satisfaction Utilities Test)

测试约束满足问题求解器的各项功能。
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constraint_satisfaction_utils.mod import (
    CSP, CSPSolver, Constraint, UnaryConstraint, BinaryConstraint,
    AllDifferentConstraint, AllEqualConstraint, SumConstraint,
    MaxValueConstraint,
    create_n_queens_csp, create_sudoku_csp, create_graph_coloring_csp,
    create_scheduling_csp,
    solve_n_queens, solve_sudoku, solve_graph_coloring,
    count_n_queens_solutions,
    print_n_queens_solution, print_sudoku_solution
)


class TestConstraints(unittest.TestCase):
    """测试约束类"""
    
    def test_unary_constraint(self):
        """测试一元约束"""
        # 值必须大于 0
        constraint = UnaryConstraint('x', lambda v: v > 0)
        
        self.assertTrue(constraint.is_satisfied({'x': 1}))
        self.assertTrue(constraint.is_satisfied({'x': 10}))
        self.assertFalse(constraint.is_satisfied({'x': 0}))
        self.assertFalse(constraint.is_satisfied({'x': -1}))
        self.assertTrue(constraint.is_satisfied({'y': 1}))  # 变量未赋值
    
    def test_binary_constraint(self):
        """测试二元约束"""
        # x != y
        constraint = BinaryConstraint('x', 'y', lambda v1, v2: v1 != v2)
        
        self.assertTrue(constraint.is_satisfied({'x': 1, 'y': 2}))
        self.assertFalse(constraint.is_satisfied({'x': 1, 'y': 1}))
        self.assertTrue(constraint.is_satisfied({'x': 1}))  # y 未赋值
        self.assertTrue(constraint.is_satisfied({'y': 2}))  # x 未赋值
    
    def test_all_different_constraint(self):
        """测试所有不同约束"""
        constraint = AllDifferentConstraint(['x', 'y', 'z'])
        
        self.assertTrue(constraint.is_satisfied({'x': 1, 'y': 2, 'z': 3}))
        self.assertFalse(constraint.is_satisfied({'x': 1, 'y': 1, 'z': 3}))
        self.assertTrue(constraint.is_satisfied({'x': 1, 'y': 2}))  # z 未赋值
    
    def test_all_equal_constraint(self):
        """测试所有相等约束"""
        constraint = AllEqualConstraint(['x', 'y', 'z'])
        
        self.assertTrue(constraint.is_satisfied({'x': 1, 'y': 1, 'z': 1}))
        self.assertFalse(constraint.is_satisfied({'x': 1, 'y': 2, 'z': 1}))
        self.assertTrue(constraint.is_satisfied({'x': 1}))  # y, z 未赋值
    
    def test_sum_constraint(self):
        """测试求和约束"""
        constraint = SumConstraint(['x', 'y', 'z'], 10)
        
        self.assertTrue(constraint.is_satisfied({'x': 3, 'y': 3, 'z': 4}))
        self.assertFalse(constraint.is_satisfied({'x': 3, 'y': 3, 'z': 5}))
        self.assertTrue(constraint.is_satisfied({'x': 3, 'y': 3}))  # z 未赋值
    
    def test_max_value_constraint(self):
        """测试最大值约束"""
        constraint = MaxValueConstraint(['x', 'y', 'z'], 10)
        
        self.assertTrue(constraint.is_satisfied({'x': 5, 'y': 8, 'z': 10}))
        self.assertFalse(constraint.is_satisfied({'x': 11}))
        self.assertTrue(constraint.is_satisfied({}))  # 全未赋值


class TestCSP(unittest.TestCase):
    """测试 CSP 类"""
    
    def test_csp_creation(self):
        """测试 CSP 创建"""
        variables = ['x', 'y', 'z']
        domains = {'x': [1, 2], 'y': [1, 2], 'z': [1, 2]}
        constraints = [AllDifferentConstraint(variables)]
        
        csp = CSP(variables, domains, constraints)
        
        self.assertEqual(len(csp.variables), 3)
        self.assertEqual(len(csp.constraints), 1)
    
    def test_csp_add_constraint(self):
        """测试添加约束"""
        variables = ['x', 'y']
        domains = {'x': [1, 2], 'y': [1, 2]}
        
        csp = CSP(variables, domains, [])
        csp.add_constraint(BinaryConstraint('x', 'y', lambda v1, v2: v1 != v2))
        
        self.assertEqual(len(csp.constraints), 1)
    
    def test_csp_is_consistent(self):
        """测试一致性检查"""
        variables = ['x', 'y']
        domains = {'x': [1, 2], 'y': [1, 2]}
        constraints = [BinaryConstraint('x', 'y', lambda v1, v2: v1 != v2)]
        
        csp = CSP(variables, domains, constraints)
        
        self.assertTrue(csp.is_consistent('x', 1, {}))
        self.assertTrue(csp.is_consistent('y', 2, {'x': 1}))
        self.assertFalse(csp.is_consistent('y', 1, {'x': 1}))
    
    def test_csp_get_conflicts(self):
        """测试获取冲突"""
        variables = ['x', 'y']
        domains = {'x': [1, 2], 'y': [1, 2]}
        constraints = [BinaryConstraint('x', 'y', lambda v1, v2: v1 != v2)]
        
        csp = CSP(variables, domains, constraints)
        
        conflicts = csp.get_conflicts({'x': 1, 'y': 1})
        self.assertEqual(len(conflicts), 1)
        
        conflicts = csp.get_conflicts({'x': 1, 'y': 2})
        self.assertEqual(len(conflicts), 0)


class TestCSPSolver(unittest.TestCase):
    """测试 CSP 求解器"""
    
    def test_simple_csp(self):
        """测试简单 CSP"""
        variables = ['x', 'y']
        domains = {'x': [1, 2], 'y': [1, 2]}
        constraints = [BinaryConstraint('x', 'y', lambda v1, v2: v1 != v2)]
        
        csp = CSP(variables, domains, constraints)
        solver = CSPSolver(csp)
        solution = solver.solve()
        
        self.assertIsNotNone(solution)
        self.assertNotEqual(solution['x'], solution['y'])
    
    def test_unsolvable_csp(self):
        """测试无解 CSP"""
        variables = ['x', 'y']
        domains = {'x': [1], 'y': [1]}  # 只有相同值
        constraints = [BinaryConstraint('x', 'y', lambda v1, v2: v1 != v2)]
        
        csp = CSP(variables, domains, constraints)
        solver = CSPSolver(csp)
        solution = solver.solve()
        
        self.assertIsNone(solution)
    
    def test_all_different_csp(self):
        """测试 AllDifferent 约束"""
        variables = ['a', 'b', 'c']
        domains = {v: [1, 2, 3] for v in variables}
        constraints = [AllDifferentConstraint(variables)]
        
        csp = CSP(variables, domains, constraints)
        solver = CSPSolver(csp)
        solution = solver.solve()
        
        self.assertIsNotNone(solution)
        values = [solution[v] for v in variables]
        self.assertEqual(len(values), len(set(values)))  # 所有值不同
    
    def test_heuristics(self):
        """测试启发式"""
        variables = ['x', 'y', 'z']
        domains = {'x': [1, 2], 'y': [1, 2, 3], 'z': [1]}  # z 最小
        constraints = [AllDifferentConstraint(variables)]
        
        csp = CSP(variables, domains, constraints)
        
        # 测试 MRV 启发式
        solver = CSPSolver(csp, var_heuristic='mrv')
        solution = solver.solve()
        
        self.assertIsNotNone(solution)
        self.assertEqual(solution['z'], 1)  # z 应该被优先选择
    
    def test_inference_methods(self):
        """测试推理方法"""
        variables = ['x', 'y', 'z', 'w']
        domains = {v: [1, 2, 3, 4] for v in variables}
        constraints = [
            BinaryConstraint('x', 'y', lambda v1, v2: v1 != v2),
            BinaryConstraint('y', 'z', lambda v1, v2: v1 != v2),
            BinaryConstraint('z', 'w', lambda v1, v2: v1 != v2),
        ]
        
        csp = CSP(variables, domains, constraints)
        
        # 测试不同推理方法
        for inference in ['none', 'forward_checking', 'ac3']:
            solver = CSPSolver(csp, inference=inference)
            solution = solver.solve()
            self.assertIsNotNone(solution)
    
    def test_find_all_solutions(self):
        """测试查找所有解"""
        variables = ['x', 'y']
        domains = {'x': [1, 2, 3], 'y': [1, 2, 3]}
        constraints = [BinaryConstraint('x', 'y', lambda v1, v2: v1 < v2)]
        
        csp = CSP(variables, domains, constraints)
        solver = CSPSolver(csp)
        solutions = solver.find_all_solutions()
        
        # x < y 的组合：3 种
        self.assertEqual(len(solutions), 3)


class TestNQueens(unittest.TestCase):
    """测试 N 皇后问题"""
    
    def test_n_queens_4(self):
        """测试 4 皇后"""
        solution = solve_n_queens(4)
        
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution), 4)
        
        # 检查约束
        for col1, row1 in solution.items():
            for col2, row2 in solution.items():
                if col1 != col2:
                    # 不同行
                    self.assertNotEqual(row1, row2)
                    # 不同对角线
                    self.assertNotEqual(abs(row1 - row2), abs(col1 - col2))
    
    def test_n_queens_8(self):
        """测试 8 皇后"""
        solution = solve_n_queens(8)
        
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution), 8)
        
        # 检查约束
        for col1, row1 in solution.items():
            for col2, row2 in solution.items():
                if col1 != col2:
                    self.assertNotEqual(row1, row2)
                    self.assertNotEqual(abs(row1 - row2), abs(col1 - col2))
    
    def test_n_queens_1(self):
        """测试 1 皇后"""
        solution = solve_n_queens(1)
        self.assertIsNotNone(solution)
        self.assertEqual(solution, {0: 0})
    
    def test_n_queens_2(self):
        """测试 2 皇后（无解）"""
        solution = solve_n_queens(2)
        self.assertIsNone(solution)
    
    def test_n_queens_3(self):
        """测试 3 皇后（无解）"""
        solution = solve_n_queens(3)
        self.assertIsNone(solution)
    
    def test_count_n_queens_solutions(self):
        """测试计算解数量"""
        # 4 皇后有 2 个解
        self.assertEqual(count_n_queens_solutions(4), 2)
        
        # 1 皇后有 1 个解
        self.assertEqual(count_n_queens_solutions(1), 1)
    
    def test_print_n_queens_solution(self):
        """测试打印解"""
        solution = solve_n_queens(4)
        output = print_n_queens_solution(solution, 4)
        
        self.assertIn('Q', output)
        self.assertIn('.', output)
        lines = output.split('\n')
        self.assertEqual(len(lines), 4)


class TestSudoku(unittest.TestCase):
    """测试数独问题"""
    
    def test_simple_sudoku(self):
        """测试简单数独"""
        grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        
        solution = solve_sudoku(grid)
        
        self.assertIsNotNone(solution)
        
        # 检查行
        for i in range(9):
            self.assertEqual(len(set(solution[i])), 9)
        
        # 检查列
        for j in range(9):
            col = [solution[i][j] for i in range(9)]
            self.assertEqual(len(set(col)), 9)
        
        # 检查 3x3 宫格
        for bi in range(3):
            for bj in range(3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(solution[bi * 3 + i][bj * 3 + j])
                self.assertEqual(len(set(box)), 9)
    
    def test_complete_sudoku(self):
        """测试完整数独"""
        grid = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        
        solution = solve_sudoku(grid)
        
        self.assertIsNotNone(solution)
        self.assertEqual(solution, grid)
    
    def test_print_sudoku_solution(self):
        """测试打印数独解"""
        grid = [[i + 1 for i in range(9)] for _ in range(9)]  # 不合法，仅测试格式
        output = print_sudoku_solution(grid)
        
        lines = output.split('\n')
        self.assertEqual(len(lines), 11)  # 包含分隔线


class TestGraphColoring(unittest.TestCase):
    """测试图着色问题"""
    
    def test_simple_graph(self):
        """测试简单图"""
        vertices = ['A', 'B', 'C']
        edges = [('A', 'B'), ('B', 'C')]
        colors = ['红', '绿']
        
        solution = solve_graph_coloring(vertices, edges, colors)
        
        self.assertIsNotNone(solution)
        
        # 检查相邻顶点颜色不同
        for v1, v2 in edges:
            self.assertNotEqual(solution[v1], solution[v2])
    
    def test_triangle_graph(self):
        """测试三角形图"""
        vertices = ['A', 'B', 'C']
        edges = [('A', 'B'), ('B', 'C'), ('A', 'C')]
        colors = ['红', '绿', '蓝']
        
        solution = solve_graph_coloring(vertices, edges, colors)
        
        self.assertIsNotNone(solution)
        
        for v1, v2 in edges:
            self.assertNotEqual(solution[v1], solution[v2])
    
    def test_unsolvable_graph(self):
        """测试无解图"""
        vertices = ['A', 'B', 'C']
        edges = [('A', 'B'), ('B', 'C'), ('A', 'C')]  # 三角形
        colors = ['红', '绿']  # 只有两个颜色
        
        solution = solve_graph_coloring(vertices, edges, colors)
        
        self.assertIsNone(solution)  # 三角形需要至少 3 个颜色


class TestScheduling(unittest.TestCase):
    """测试调度问题"""
    
    def test_simple_scheduling(self):
        """测试简单调度"""
        tasks = ['Task1', 'Task2', 'Task3']
        resources = ['R1', 'R2']
        # Task1 和 Task2 不能同时执行
        constraints = [('Task1', 'Task2')]
        
        csp = create_scheduling_csp(tasks, resources, constraints)
        solver = CSPSolver(csp)
        solution = solver.solve()
        
        self.assertIsNotNone(solution)
        
        # Task1 和 Task2 应分配不同资源
        if 'Task1' in solution and 'Task2' in solution:
            self.assertNotEqual(solution['Task1'], solution['Task2'])


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_solver_stats(self):
        """测试求解器统计"""
        variables = ['x', 'y', 'z']
        domains = {v: [1, 2, 3] for v in variables}
        constraints = [AllDifferentConstraint(variables)]
        
        csp = CSP(variables, domains, constraints)
        solver = CSPSolver(csp)
        solution = solver.solve()
        
        self.assertIsNotNone(solution)
        self.assertGreater(solver.nodes_explored, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)