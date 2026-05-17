#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
约束满足问题工具模块使用示例 (Constraint Satisfaction Utilities Usage Examples)

展示约束满足问题求解器的各种使用场景。
"""

import sys
sys.path.insert(0, '..')

from constraint_satisfaction_utils.mod import (
    CSP, CSPSolver,
    UnaryConstraint, BinaryConstraint,
    AllDifferentConstraint, AllEqualConstraint,
    SumConstraint, MaxValueConstraint,
    create_n_queens_csp, create_sudoku_csp, create_graph_coloring_csp,
    solve_n_queens, solve_sudoku, solve_graph_coloring,
    count_n_queens_solutions,
    print_n_queens_solution, print_sudoku_solution
)


def example_basic_csp():
    """基础 CSP 示例"""
    print("=" * 60)
    print("示例 1: 基础约束满足问题")
    print("=" * 60)
    
    # 定义变量和域
    variables = ['Alice', 'Bob', 'Charlie']
    domains = {v: ['红', '绿', '蓝'] for v in variables}
    
    # 定义约束：所有人颜色不同
    constraints = [AllDifferentConstraint(variables)]
    
    # 创建 CSP
    csp = CSP(variables, domains, constraints)
    
    # 创建求解器
    solver = CSPSolver(csp, var_heuristic='mrv', inference='ac3')
    
    # 求解
    solution = solver.solve()
    
    print(f"解: {solution}")
    print(f"探索节点数: {solver.nodes_explored}")
    print(f"回溯次数: {solver.backtracks}")
    print()


def example_binary_constraints():
    """二元约束示例"""
    print("=" * 60)
    print("示例 2: 二元约束 - 任务调度")
    print("=" * 60)
    
    # 定义任务和时间段
    tasks = ['Task_A', 'Task_B', 'Task_C', 'Task_D']
    time_slots = ['上午', '下午', '晚上']
    
    # 每个任务可选择时间段
    domains = {
        'Task_A': ['上午', '下午'],
        'Task_B': ['上午', '下午', '晚上'],
        'Task_C': ['下午', '晚上'],
        'Task_D': ['上午', '晚上']
    }
    
    # 定义约束：某些任务不能同时进行
    constraints = [
        BinaryConstraint('Task_A', 'Task_B', lambda t1, t2: t1 != t2),
        BinaryConstraint('Task_B', 'Task_C', lambda t1, t2: t1 != t2),
        BinaryConstraint('Task_A', 'Task_C', lambda t1, t2: t1 != t2),
    ]
    
    csp = CSP(tasks, domains, constraints)
    solver = CSPSolver(csp, inference='forward_checking')
    
    solution = solver.solve()
    
    print(f"调度解: {solution}")
    print(f"探索节点数: {solver.nodes_explored}")
    print()


def example_n_queens():
    """N 皇后问题示例"""
    print("=" * 60)
    print("示例 3: N 皇后问题")
    print("=" * 60)
    
    for n in [4, 6, 8]:
        print(f"\n{n} 皇后问题:")
        
        solution = solve_n_queens(n)
        
        if solution:
            print(f"找到一个解:")
            print(print_n_queens_solution(solution, n))
            
            csp = create_n_queens_csp(n)
            solver = CSPSolver(csp, inference='ac3')
            solver.solve()
            print(f"探索节点数: {solver.nodes_explored}")
            print(f"回溯次数: {solver.backtracks}")
        else:
            print(f"无解")
    print()


def example_count_solutions():
    """计算解数量示例"""
    print("=" * 60)
    print("示例 4: 计算 N 皇后解数量")
    print("=" * 60)
    
    for n in [1, 2, 3, 4, 5, 6]:
        count = count_n_queens_solutions(n)
        print(f"{n} 皇后: {count} 个解")
    print()


def example_sudoku():
    """数独问题示例"""
    print("=" * 60)
    print("示例 5: 数独问题")
    print("=" * 60)
    
    # 经典数独谜题
    puzzle = [
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
    
    print("原始数独:")
    print(print_sudoku_solution(puzzle))
    
    solution = solve_sudoku(puzzle)
    
    if solution:
        print("\n解:")
        print(print_sudoku_solution(solution))
    else:
        print("\n无解")
    print()


def example_graph_coloring():
    """图着色问题示例"""
    print("=" * 60)
    print("示例 6: 图着色问题")
    print("=" * 60)
    
    # 定义图
    vertices = ['A', 'B', 'C', 'D', 'E']
    edges = [
        ('A', 'B'), ('A', 'C'),
        ('B', 'C'), ('B', 'D'),
        ('C', 'D'), ('C', 'E'),
        ('D', 'E')
    ]
    colors = ['红', '绿', '蓝', '黄']
    
    solution = solve_graph_coloring(vertices, edges, colors)
    
    print(f"图的顶点: {vertices}")
    print(f"图的边: {edges}")
    print(f"可用颜色: {colors}")
    print(f"着色解: {solution}")
    
    # 验证解
    if solution:
        print("\n验证相邻顶点颜色不同:")
        for v1, v2 in edges:
            print(f"  {v1}({solution[v1]}) - {v2}({solution[v2]}): "
                  f"{solution[v1] != solution[v2]}")
    print()


def example_multiple_constraints():
    """多种约束组合示例"""
    print("=" * 60)
    print("示例 7: 多种约束组合")
    print("=" * 60)
    
    # 定义变量：三个学生的分数
    variables = ['Student_A', 'Student_B', 'Student_C']
    domains = {v: range(60, 101) for v in variables}  # 分数 60-100
    
    # 定义约束
    constraints = [
        # 所有分数不同
        AllDifferentConstraint(variables),
        # 总分至少 240
        SumConstraint(variables, 240),
        # 最高不超过 95
        MaxValueConstraint(variables, 95),
        # 学生 A 分数必须高于学生 B
        BinaryConstraint('Student_A', 'Student_B', lambda a, b: a > b),
    ]
    
    csp = CSP(variables, domains, constraints)
    
    # 注意：SumConstraint 在部分赋值时总是满足，这里简化使用
    # 实际应用中可能需要更精细的处理
    
    solver = CSPSolver(csp, inference='forward_checking')
    solution = solver.solve()
    
    print(f"学生分数解: {solution}")
    
    if solution:
        total = sum(solution.values())
        print(f"总分: {total}")
        print(f"所有分数不同: {len(set(solution.values())) == 3}")
        print(f"最高分不超过 95: {max(solution.values()) <= 95}")
        print(f"A > B: {solution['Student_A'] > solution['Student_B']}")
    print()


def example_all_solutions():
    """查找所有解示例"""
    print("=" * 60)
    print("示例 8: 查找所有解")
    print("=" * 60)
    
    # 简单问题：三个变量，两个值，所有值不同
    variables = ['x', 'y', 'z']
    domains = {v: [1, 2, 3] for v in variables}
    constraints = [AllDifferentConstraint(variables)]
    
    csp = CSP(variables, domains, constraints)
    solver = CSPSolver(csp)
    
    solutions = solver.find_all_solutions(max_solutions=10)
    
    print(f"问题: {variables} 取值 [1,2,3], 所有值不同")
    print(f"找到 {len(solutions)} 个解:")
    
    for i, sol in enumerate(solutions[:5], 1):  # 只显示前 5 个
        print(f"  解 {i}: {sol}")
    print()


def example_heuristics_comparison():
    """启发式比较示例"""
    print("=" * 60)
    print("示例 9: 启发式比较")
    print("=" * 60)
    
    n = 8
    csp = create_n_queens_csp(n)
    
    heuristics = [
        ('none', 'none', 'none'),
        ('mrv', 'none', 'forward_checking'),
        ('mrv_degree', 'lcv', 'ac3'),
    ]
    
    print(f"{n} 皇后问题，不同启发式的性能:")
    
    for var_h, val_h, inf in heuristics:
        solver = CSPSolver(csp, var_heuristic=var_h, value_heuristic=val_h, inference=inf)
        solution = solver.solve()
        
        print(f"\n启发式组合:")
        print(f"  变量选择: {var_h}")
        print(f"  值选择: {val_h}")
        print(f"  推理: {inf}")
        print(f"  探索节点: {solver.nodes_explored}")
        print(f"  回溯次数: {solver.backtracks}")
        print(f"  找到解: {solution is not None}")
    print()


def example_custom_constraint():
    """自定义约束示例"""
    print("=" * 60)
    print("示例 10: 自定义约束")
    print("=" * 60)
    
    # 自定义约束类
    class EvenOddConstraint(Constraint):
        """奇偶约束：x 是偶数时 y 必须是奇数"""
        
        def __init__(self, x, y):
            super().__init__([x, y])
            self.x = x
            self.y = y
        
        def is_satisfied(self, assignment):
            if self.x not in assignment or self.y not in assignment:
                return True
            
            x_val = assignment[self.x]
            y_val = assignment[self.y]
            
            # 如果 x 是偶数，y 必须是奇数
            if x_val % 2 == 0:
                return y_val % 2 == 1
            return True
    
    variables = ['x', 'y']
    domains = {'x': [1, 2, 3, 4], 'y': [1, 2, 3, 4]}
    constraints = [EvenOddConstraint('x', 'y')]
    
    csp = CSP(variables, domains, constraints)
    solver = CSPSolver(csp)
    solution = solver.solve()
    
    print(f"约束: 如果 x 是偶数，y 必须是奇数")
    print(f"解: {solution}")
    
    if solution:
        x, y = solution['x'], solution['y']
        print(f"验证: x={x} ({'偶数' if x % 2 == 0 else '奇数'}), "
              f"y={y} ({'偶数' if y % 2 == 0 else '奇数'})")
        if x % 2 == 0:
            print(f"约束满足: y 是奇数 -> {y % 2 == 1}")
    print()


if __name__ == '__main__':
    example_basic_csp()
    example_binary_constraints()
    example_n_queens()
    example_count_solutions()
    example_sudoku()
    example_graph_coloring()
    example_multiple_constraints()
    example_all_solutions()
    example_heuristics_comparison()
    example_custom_constraint()
    
    print("=" * 60)
    print("所有示例完成!")
    print("=" * 60)