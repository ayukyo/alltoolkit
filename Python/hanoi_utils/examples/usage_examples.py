"""
汉诺塔工具使用示例

演示各种功能和用法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    HanoiState, solve_recursive, solve_iterative, solve_generator,
    min_moves, min_moves_frame_stewart, solve_frame_stewart,
    validate_solution, analyze_moves, is_optimal_solution,
    HanoiSolver, hanoi, hanoi_demo, visualize_moves
)


def example_basic_solve():
    """基本求解示例"""
    print("=" * 60)
    print("示例1: 基本求解")
    print("=" * 60)
    
    # 使用递归方法求解
    moves = solve_recursive(3)
    print(f"\n3个盘子的汉诺塔解法（递归）:")
    for i, move in enumerate(moves, 1):
        print(f"  第{i}步: {move}")
    
    # 使用迭代方法
    moves = solve_iterative(3)
    print(f"\n3个盘子的汉诺塔解法（迭代）:")
    for i, move in enumerate(moves, 1):
        print(f"  第{i}步: {move}")


def example_generator():
    """生成器示例"""
    print("\n" + "=" * 60)
    print("示例2: 使用生成器（内存高效）")
    print("=" * 60)
    
    print("\n使用生成器逐步获取移动:")
    for i, move in enumerate(solve_generator(4), 1):
        print(f"  第{i}步: {move}")


def example_state_management():
    """状态管理示例"""
    print("\n" + "=" * 60)
    print("示例3: 状态管理")
    print("=" * 60)
    
    # 创建初始状态
    state = HanoiState(4)
    print(f"\n初始状态:")
    print(state)
    
    # 执行移动
    moves = solve_recursive(4)
    print(f"\n执行前3步移动:")
    for move in moves[:3]:
        state.move(move.from_peg, move.to_peg)
        print(f"\n{move}")
        print(state)


def example_min_moves():
    """最少移动次数示例"""
    print("\n" + "=" * 60)
    print("示例4: 最少移动次数")
    print("=" * 60)
    
    print("\n3柱汉诺塔最少移动次数 (公式: 2^n - 1):")
    for n in range(1, 11):
        print(f"  {n}个盘子: {min_moves(n)} 次移动")
    
    print("\n4柱汉诺塔最少移动次数 (Frame-Stewart算法):")
    for n in range(1, 11):
        moves_3 = min_moves(n)
        moves_4 = min_moves_frame_stewart(n, 4)
        savings = moves_3 - moves_4
        print(f"  {n}个盘子: {moves_4} 次 (比3柱少 {savings} 次)")


def example_multi_peg():
    """多柱汉诺塔示例"""
    print("\n" + "=" * 60)
    print("示例5: 多柱汉诺塔（4柱及以上）")
    print("=" * 60)
    
    print("\n4个盘子，使用不同柱子数量:")
    for pegs in [3, 4, 5]:
        moves = solve_frame_stewart(4, num_pegs=pegs)
        print(f"  {pegs}根柱子: {len(moves)} 次移动")
    
    print("\n验证4柱解法:")
    moves = solve_frame_stewart(4, num_pegs=4)
    print(f"  移动序列: {len(moves)} 步")
    for i, move in enumerate(moves, 1):
        print(f"    第{i}步: {move}")
    print(f"  验证结果: {'正确' if validate_solution(4, moves, num_pegs=4) else '错误'}")


def example_solution_analysis():
    """解分析示例"""
    print("\n" + "=" * 60)
    print("示例6: 解分析")
    print("=" * 60)
    
    moves = solve_recursive(5)
    analysis = analyze_moves(moves)
    
    print(f"\n5个盘子汉诺塔解分析:")
    print(f"  总移动次数: {analysis['total_moves']}")
    print(f"  涉及盘子数: {analysis['unique_disks']}")
    print(f"  最小盘子: {analysis['min_disk']}")
    print(f"  最大盘子: {analysis['max_disk']}")
    print(f"\n  各盘子移动次数:")
    for disk in sorted(analysis['moves_per_disk'].keys()):
        count = analysis['moves_per_disk'][disk]
        bar = '█' * count
        print(f"    盘子{disk}: {count}次 {bar}")
    
    print(f"\n  柱子使用频率:")
    for peg in sorted(analysis['peg_usage'].keys()):
        count = analysis['peg_usage'][peg]
        print(f"    柱{peg}: {count}次")


def example_solver_class():
    """求解器类示例"""
    print("\n" + "=" * 60)
    print("示例7: HanoiSolver 类")
    print("=" * 60)
    
    # 创建求解器
    solver = HanoiSolver(4)
    
    print(f"\n求解器信息:")
    print(f"  盘子数: {solver.num_disks}")
    print(f"  柱子数: {solver.num_pegs}")
    print(f"  最少移动次数: {min_moves(solver.num_disks)}")
    
    # 求解
    solver.solve('recursive')
    print(f"  实际移动次数: {solver.move_count}")
    print(f"  是否最优解: {solver.is_optimal()}")


def example_visualization():
    """可视化示例"""
    print("\n" + "=" * 60)
    print("示例8: 步骤可视化")
    print("=" * 60)
    
    print("\n2个盘子的完整移动过程:")
    moves = solve_recursive(2)
    
    for step_text in visualize_moves(2, moves):
        print(step_text)


def example_demo():
    """完整演示"""
    print("\n" + "=" * 60)
    print("示例9: 完整演示")
    print("=" * 60)
    
    print(hanoi_demo(3))


def example_performance():
    """性能测试"""
    print("\n" + "=" * 60)
    print("示例10: 性能测试")
    print("=" * 60)
    
    import time
    
    # 测试递归 vs 迭代
    for n in [10, 15, 20]:
        print(f"\n{n}个盘子:")
        
        start = time.time()
        moves_rec = solve_recursive(n)
        time_rec = time.time() - start
        
        start = time.time()
        moves_iter = solve_iterative(n)
        time_iter = time.time() - start
        
        print(f"  递归: {len(moves_rec)} 步, 耗时 {time_rec:.4f}s")
        print(f"  迭代: {len(moves_iter)} 步, 耗时 {time_iter:.4f}s")


def example_quick_usage():
    """快速使用示例"""
    print("\n" + "=" * 60)
    print("示例11: 快速使用")
    print("=" * 60)
    
    # 使用hanoi快捷函数
    moves = hanoi(3)
    print(f"\n使用hanoi()快捷函数:")
    print(f"  移动次数: {len(moves)}")
    print(f"  是否最优: {is_optimal_solution(3, moves)}")


def example_validation():
    """验证示例"""
    print("\n" + "=" * 60)
    print("示例12: 解验证")
    print("=" * 60)
    
    # 正确的解
    correct_moves = solve_recursive(3)
    print(f"\n验证正确解: {validate_solution(3, correct_moves)}")
    
    # 错误的解（移动不够）
    wrong_moves = correct_moves[:3]
    print(f"验证不完整解: {validate_solution(3, wrong_moves)}")
    
    # 错误的解（非法移动）
    from mod import Move
    invalid_moves = [Move(3, 0, 2), Move(2, 0, 2)]  # 大盘放小盘上
    print(f"验证非法解: {validate_solution(3, invalid_moves)}")


def main():
    """运行所有示例"""
    example_basic_solve()
    example_generator()
    example_state_management()
    example_min_moves()
    example_multi_peg()
    example_solution_analysis()
    example_solver_class()
    example_visualization()
    example_demo()
    example_performance()
    example_quick_usage()
    example_validation()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()