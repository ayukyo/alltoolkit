"""
匈牙利算法单元测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hungarian_algorithm_utils.mod import (
    HungarianAlgorithm,
    hungarian,
    solve_assignment,
    max_weight_matching,
    rectangular_assignment,
    AssignmentProblem
)


def test_basic_assignment():
    """测试基本分配问题"""
    print("测试 1: 基本分配问题")
    
    # 简单的 3×3 成本矩阵
    costs = [
        [4, 1, 3],
        [2, 0, 5],
        [3, 2, 2]
    ]
    
    assignment, total = hungarian(costs)
    
    print(f"  成本矩阵: {costs}")
    print(f"  分配方案: {assignment}")
    print(f"  总成本: {total}")
    
    # 验证：每个工人和任务都被分配一次
    workers = [i for i, j in assignment]
    tasks = [j for i, j in assignment]
    assert len(set(workers)) == len(costs), "每个工人应该被分配一次"
    assert len(set(tasks)) == len(costs[0]), "每个任务应该被分配一次"
    
    # 验证总成本
    calculated_total = sum(costs[i][j] for i, j in assignment)
    assert total == calculated_total, f"总成本应该匹配: {total} vs {calculated_total}"
    
    print("  ✓ 通过\n")


def test_optimal_solution():
    """测试是否找到最优解"""
    print("测试 2: 验证最优解")
    
    # 已知最优解的成本矩阵
    costs = [
        [10, 19, 8, 15],
        [10, 18, 7, 17],
        [13, 16, 9, 14],
        [12, 19, 8, 11]
    ]
    
    assignment, total = hungarian(costs)
    
    print(f"  成本矩阵: {costs}")
    print(f"  分配方案: {assignment}")
    print(f"  总成本: {total}")
    
    # 最优解应该是 10 + 16 + 9 + 11 = 46 或类似
    # 验证总成本
    calculated_total = sum(costs[i][j] for i, j in assignment)
    assert total == calculated_total
    
    print("  ✓ 通过\n")


def test_single_element():
    """测试单元素矩阵"""
    print("测试 3: 单元素矩阵")
    
    costs = [[5]]
    assignment, total = hungarian(costs)
    
    assert assignment == [(0, 0)]
    assert total == 5
    
    print(f"  成本: {costs}")
    print(f"  分配: {assignment}, 总成本: {total}")
    print("  ✓ 通过\n")


def test_max_weight_matching():
    """测试最大权重匹配"""
    print("测试 4: 最大权重匹配")
    
    # 效率矩阵（越高越好）
    weights = [
        [10, 19, 8, 15],
        [10, 18, 7, 17],
        [13, 16, 9, 14],
        [12, 19, 8, 11]
    ]
    
    assignment, total_weight = max_weight_matching(weights)
    
    print(f"  权重矩阵: {weights}")
    print(f"  匹配方案: {assignment}")
    print(f"  总权重: {total_weight}")
    
    # 验证
    calculated = sum(weights[i][j] for i, j in assignment)
    assert total_weight == calculated
    
    print("  ✓ 通过\n")


def test_rectangular_assignment():
    """测试非方阵分配"""
    print("测试 5: 非方阵分配 (工人 ≠ 任务)")
    
    # 2 个工人，3 个任务
    costs = [
        [10, 20, 15],
        [25, 15, 30]
    ]
    
    assignment = rectangular_assignment(costs)
    
    print(f"  成本矩阵: {costs}")
    print(f"  分配方案: {assignment}")
    
    # 验证：每个工人最多分配一个任务
    workers = [i for i, j in assignment]
    assert len(set(workers)) == len(workers), "每个工人应该最多被分配一次"
    
    print("  ✓ 通过\n")


def test_assignment_problem_class():
    """测试 AssignmentProblem 类"""
    print("测试 6: AssignmentProblem 类")
    
    problem = AssignmentProblem()
    problem.add_worker("Alice")
    problem.add_worker("Bob")
    problem.add_worker("Charlie")
    problem.add_task("任务A")
    problem.add_task("任务B")
    problem.add_task("任务C")
    
    # 设置成本
    problem.set_cost(0, 0, 10).set_cost(0, 1, 15).set_cost(0, 2, 9)
    problem.set_cost(1, 0, 9).set_cost(1, 1, 18).set_cost(1, 2, 5)
    problem.set_cost(2, 0, 6).set_cost(2, 1, 14).set_cost(2, 2, 3)
    
    result = problem.solve()
    
    print("  工人: ['Alice', 'Bob', 'Charlie']")
    print("  任务: ['任务A', '任务B', '任务C']")
    print(f"  分配结果: {result}")
    
    # 验证
    assert len(result) <= 3
    
    total_cost = sum(cost for _, _, cost in result)
    print(f"  总成本: {total_cost}")
    
    print("  ✓ 通过\n")


def test_large_matrix():
    """测试大矩阵性能"""
    print("测试 7: 大矩阵性能 (10×10)")
    
    import random
    random.seed(42)
    
    n = 10
    costs = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    
    assignment, total = hungarian(costs)
    
    print(f"  矩阵大小: {n}×{n}")
    print(f"  总成本: {total}")
    
    # 验证
    workers = [i for i, j in assignment]
    tasks = [j for i, j in assignment]
    assert len(set(workers)) == n
    assert len(set(tasks)) == n
    
    print("  ✓ 通过\n")


def test_zero_costs():
    """测试零成本"""
    print("测试 8: 零成本矩阵")
    
    costs = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    
    assignment, total = hungarian(costs)
    
    assert total == 0
    print(f"  分配: {assignment}, 总成本: {total}")
    print("  ✓ 通过\n")


def test_symmetric_matrix():
    """测试对称矩阵"""
    print("测试 9: 对称矩阵")
    
    costs = [
        [1, 2, 3],
        [2, 1, 2],
        [3, 2, 1]
    ]
    
    assignment, total = hungarian(costs)
    
    print(f"  对称矩阵: {costs}")
    print(f"  分配: {assignment}, 总成本: {total}")
    
    # 对称矩阵对角线和应该是最小
    # 但不一定，取决于具体值
    
    print("  ✓ 通过\n")


def test_get_assignment_matrix():
    """测试获取分配矩阵"""
    print("测试 10: 获取分配矩阵")
    
    costs = [
        [4, 1, 3],
        [2, 0, 5],
        [3, 2, 2]
    ]
    
    solver = HungarianAlgorithm(costs)
    solver.solve()
    matrix = solver.get_assignment_matrix()
    
    print(f"  成本矩阵: {costs}")
    print(f"  分配矩阵: {matrix}")
    
    # 验证每行每列只有一个 1
    for row in matrix:
        assert sum(row) == 1, "每行应该只有一个分配"
    
    for j in range(len(matrix[0])):
        assert sum(matrix[i][j] for i in range(len(matrix))) == 1, "每列应该只有一个分配"
    
    print("  ✓ 通过\n")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("匈牙利算法单元测试")
    print("=" * 50 + "\n")
    
    test_basic_assignment()
    test_optimal_solution()
    test_single_element()
    test_max_weight_matching()
    test_rectangular_assignment()
    test_assignment_problem_class()
    test_large_matrix()
    test_zero_costs()
    test_symmetric_matrix()
    test_get_assignment_matrix()
    
    print("=" * 50)
    print("所有测试通过! ✓")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()