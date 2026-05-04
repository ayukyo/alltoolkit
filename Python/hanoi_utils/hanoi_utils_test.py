"""
汉诺塔工具模块测试

测试所有核心功能：
- 递归求解
- 迭代求解
- 状态管理
- 移动验证
- 多柱汉诺塔
"""

import unittest
from mod import (
    HanoiState, Move, MoveError,
    solve_recursive, solve_iterative, solve_generator,
    min_moves, min_moves_frame_stewart, solve_frame_stewart,
    validate_solution, analyze_moves, is_optimal_solution,
    HanoiSolver, hanoi, hanoi_demo,
    get_disk_sequence, visualize_moves
)


class TestHanoiState(unittest.TestCase):
    """测试汉诺塔状态类"""
    
    def test_initial_state(self):
        """测试初始状态"""
        state = HanoiState(3)
        self.assertEqual(state.num_disks, 3)
        self.assertEqual(state.num_pegs, 3)
        self.assertEqual(state.pegs[0], [3, 2, 1])  # 从底到顶
        self.assertEqual(state.pegs[1], [])
        self.assertEqual(state.pegs[2], [])
    
    def test_is_solved(self):
        """测试是否解决"""
        state = HanoiState(3)
        self.assertFalse(state.is_solved())
        
        # 手动移动到解决状态
        state.move(0, 2)  # 盘1: 0->2
        state.move(0, 1)  # 盘2: 0->1
        state.move(2, 1)  # 盘1: 2->1
        state.move(0, 2)  # 盘3: 0->2
        state.move(1, 0)  # 盘1: 1->0
        state.move(1, 2)  # 盘2: 1->2
        state.move(0, 2)  # 盘1: 0->2
        
        self.assertTrue(state.is_solved())
    
    def test_invalid_move_empty_peg(self):
        """测试从空柱移动"""
        state = HanoiState(3)
        self.assertFalse(state.is_valid_move(1, 2))
    
    def test_invalid_move_same_peg(self):
        """测试移动到同一柱子"""
        state = HanoiState(3)
        self.assertFalse(state.is_valid_move(0, 0))
    
    def test_invalid_move_larger_on_smaller(self):
        """测试大盘放小盘上"""
        state = HanoiState(3)
        state.move(0, 2)  # 盘1移到柱2
        state.move(0, 1)  # 盘2移到柱1
        # 尝试把盘2放到盘1上（非法）
        self.assertFalse(state.is_valid_move(1, 2))
    
    def test_valid_move(self):
        """测试合法移动"""
        state = HanoiState(3)
        self.assertTrue(state.is_valid_move(0, 1))
        self.assertTrue(state.is_valid_move(0, 2))
    
    def test_move_execution(self):
        """测试移动执行"""
        state = HanoiState(3)
        move = state.move(0, 2)
        self.assertEqual(move.disk, 1)
        self.assertEqual(move.from_peg, 0)
        self.assertEqual(move.to_peg, 2)
        self.assertEqual(state.pegs[0], [3, 2])
        self.assertEqual(state.pegs[2], [1])
    
    def test_move_error(self):
        """测试非法移动异常"""
        state = HanoiState(3)
        with self.assertRaises(MoveError):
            state.move(1, 2)  # 从空柱移动
    
    def test_copy(self):
        """测试状态复制"""
        state1 = HanoiState(3)
        state1.move(0, 2)
        state2 = state1.copy()
        
        # 独立的状态
        state2.move(0, 1)
        self.assertEqual(state1.pegs[1], [])
        self.assertEqual(state2.pegs[1], [2])
    
    def test_four_pegs(self):
        """测试四柱汉诺塔"""
        state = HanoiState(3, num_pegs=4)
        self.assertEqual(state.num_pegs, 4)
        self.assertEqual(len(state.pegs), 4)
    
    def test_zero_disks(self):
        """测试零个盘子"""
        state = HanoiState(0)
        self.assertTrue(state.is_solved())  # 空状态即为解决
    
    def test_invalid_parameters(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            HanoiState(-1)
        with self.assertRaises(ValueError):
            HanoiState(3, num_pegs=2)


class TestRecursiveSolver(unittest.TestCase):
    """测试递归求解器"""
    
    def test_one_disk(self):
        """测试1个盘子"""
        moves = solve_recursive(1)
        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0].disk, 1)
        self.assertEqual(moves[0].from_peg, 0)
        self.assertEqual(moves[0].to_peg, 2)
    
    def test_two_disks(self):
        """测试2个盘子"""
        moves = solve_recursive(2)
        self.assertEqual(len(moves), 3)
        self.assertTrue(validate_solution(2, moves))
    
    def test_three_disks(self):
        """测试3个盘子"""
        moves = solve_recursive(3)
        self.assertEqual(len(moves), 7)
        self.assertTrue(validate_solution(3, moves))
    
    def test_five_disks(self):
        """测试5个盘子"""
        moves = solve_recursive(5)
        self.assertEqual(len(moves), 31)
        self.assertTrue(validate_solution(5, moves))
    
    def test_zero_disks(self):
        """测试零个盘子"""
        moves = solve_recursive(0)
        self.assertEqual(len(moves), 0)
    
    def test_custom_pegs(self):
        """测试自定义柱子"""
        moves = solve_recursive(3, from_peg=0, to_peg=1, aux_peg=2)
        self.assertTrue(validate_solution(3, moves, target_peg=1))


class TestIterativeSolver(unittest.TestCase):
    """测试迭代求解器"""
    
    def test_matches_recursive(self):
        """测试迭代与递归结果一致"""
        for n in range(1, 7):
            rec_moves = solve_recursive(n)
            iter_moves = solve_iterative(n)
            self.assertEqual(len(rec_moves), len(iter_moves))
            # 移动序列可能不同，但都应该正确
            self.assertTrue(validate_solution(n, rec_moves))
            self.assertTrue(validate_solution(n, iter_moves))
    
    def test_zero_disks(self):
        """测试零个盘子"""
        moves = solve_iterative(0)
        self.assertEqual(len(moves), 0)


class TestGeneratorSolver(unittest.TestCase):
    """测试生成器求解器"""
    
    def test_generator(self):
        """测试生成器功能"""
        moves_list = list(solve_generator(3))
        self.assertEqual(len(moves_list), 7)
        self.assertTrue(validate_solution(3, moves_list))
    
    def test_memory_efficiency(self):
        """测试内存效率（生成器不应预先计算所有移动）"""
        gen = solve_generator(10)
        first_move = next(gen)
        self.assertEqual(first_move.disk, 1)


class TestMinMoves(unittest.TestCase):
    """测试最少移动次数计算"""
    
    def test_formula(self):
        """测试公式 2^n - 1"""
        for n in range(10):
            self.assertEqual(min_moves(n), (1 << n) - 1)
    
    def test_known_values(self):
        """测试已知值"""
        self.assertEqual(min_moves(0), 0)
        self.assertEqual(min_moves(1), 1)
        self.assertEqual(min_moves(2), 3)
        self.assertEqual(min_moves(3), 7)
        self.assertEqual(min_moves(4), 15)
        self.assertEqual(min_moves(5), 31)
        self.assertEqual(min_moves(10), 1023)
    
    def test_negative_disks(self):
        """测试负数盘子"""
        with self.assertRaises(ValueError):
            min_moves(-1)


class TestFrameStewart(unittest.TestCase):
    """测试多柱汉诺塔（Frame-Stewart算法）"""
    
    def test_three_pegs_matches_standard(self):
        """测试3柱情况与标准解一致"""
        for n in range(1, 6):
            fs_moves = min_moves_frame_stewart(n, 3)
            std_moves = min_moves(n)
            self.assertEqual(fs_moves, std_moves)
    
    def test_four_pegs_fewer_moves(self):
        """测试4柱比3柱移动次数少"""
        for n in [3, 4, 5, 6]:
            moves_3 = min_moves_frame_stewart(n, 3)
            moves_4 = min_moves_frame_stewart(n, 4)
            self.assertLess(moves_4, moves_3)
    
    def test_four_pegs_solution(self):
        """测试4柱求解"""
        for n in [1, 2, 3, 4]:
            moves = solve_frame_stewart(n, num_pegs=4)
            self.assertTrue(validate_solution(n, moves, num_pegs=4))
    
    def test_known_values(self):
        """测试已知的最少移动次数（4柱）"""
        # 4柱汉诺塔已知最优解
        self.assertEqual(min_moves_frame_stewart(1, 4), 1)
        self.assertEqual(min_moves_frame_stewart(2, 4), 3)
        self.assertEqual(min_moves_frame_stewart(3, 4), 5)
        self.assertEqual(min_moves_frame_stewart(4, 4), 9)
    
    def test_zero_disks(self):
        """测试零个盘子"""
        self.assertEqual(min_moves_frame_stewart(0, 4), 0)


class TestSolutionValidation(unittest.TestCase):
    """测试解验证"""
    
    def test_valid_solution(self):
        """测试有效解"""
        moves = solve_recursive(3)
        self.assertTrue(validate_solution(3, moves))
    
    def test_invalid_solution_wrong_move(self):
        """测试无效移动的解"""
        moves = [Move(1, 0, 2)]  # 只移动一个盘子
        self.assertFalse(validate_solution(3, moves))
    
    def test_invalid_solution_wrong_order(self):
        """测试顺序错误的解"""
        moves = [Move(2, 0, 2), Move(1, 0, 2)]  # 大盘放小盘上
        self.assertFalse(validate_solution(2, moves))
    
    def test_empty_solution(self):
        """测试空解"""
        self.assertTrue(validate_solution(0, []))
        self.assertFalse(validate_solution(1, []))


class TestAnalyzeMoves(unittest.TestCase):
    """测试移动分析"""
    
    def test_analysis(self):
        """测试分析结果"""
        moves = solve_recursive(3)
        analysis = analyze_moves(moves)
        
        self.assertEqual(analysis['total_moves'], 7)
        self.assertEqual(analysis['unique_disks'], 3)
        self.assertEqual(analysis['min_disk'], 1)
        self.assertEqual(analysis['max_disk'], 3)
        
        # 每个盘子的移动次数
        # 盘1移动最多，盘3移动最少
        self.assertEqual(analysis['moves_per_disk'][1], 4)
        self.assertEqual(analysis['moves_per_disk'][2], 2)
        self.assertEqual(analysis['moves_per_disk'][3], 1)
    
    def test_empty_moves(self):
        """测试空移动序列"""
        analysis = analyze_moves([])
        self.assertEqual(analysis['total_moves'], 0)
        self.assertEqual(analysis['unique_disks'], 0)


class TestIsOptimal(unittest.TestCase):
    """测试最优解判断"""
    
    def test_optimal_solution(self):
        """测试最优解"""
        moves = solve_recursive(5)
        self.assertTrue(is_optimal_solution(5, moves))
    
    def test_non_optimal_solution(self):
        """测试非最优解"""
        moves = [Move(1, 0, 1), Move(1, 1, 2)]  # 冗余移动
        self.assertFalse(is_optimal_solution(1, moves))


class TestHanoiSolver(unittest.TestCase):
    """测试求解器类"""
    
    def test_recursive(self):
        """测试递归方法"""
        solver = HanoiSolver(3)
        moves = solver.solve('recursive')
        self.assertEqual(len(moves), 7)
        self.assertTrue(solver.is_optimal())
    
    def test_iterative(self):
        """测试迭代方法"""
        solver = HanoiSolver(3)
        moves = solver.solve('iterative')
        self.assertEqual(len(moves), 7)
    
    def test_properties(self):
        """测试属性"""
        solver = HanoiSolver(4)
        self.assertEqual(solver.move_count, 15)
    
    def test_four_pegs(self):
        """测试4柱"""
        solver = HanoiSolver(4, num_pegs=4)
        moves = solver.moves
        self.assertTrue(validate_solution(4, moves, num_pegs=4))
    
    def test_simulate(self):
        """测试模拟"""
        solver = HanoiSolver(2)
        states = list(solver.simulate())
        self.assertEqual(len(states), 4)  # 初始状态 + 3次移动


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_hanoi_function(self):
        """测试hanoi函数"""
        moves_rec = hanoi(3, 'recursive')
        moves_iter = hanoi(3, 'iterative')
        
        self.assertEqual(len(moves_rec), 7)
        self.assertEqual(len(moves_iter), 7)
    
    def test_hanoi_demo(self):
        """测试演示函数"""
        demo = hanoi_demo(2)
        self.assertIn('汉诺塔演示', demo)
        self.assertIn('最少移动次数', demo)
    
    def test_get_disk_sequence(self):
        """测试获取盘子序列"""
        moves = solve_recursive(3)
        sequence = get_disk_sequence(moves)
        self.assertEqual(len(sequence), 7)
        self.assertTrue(all(1 <= d <= 3 for d in sequence))


class TestMove(unittest.TestCase):
    """测试Move类"""
    
    def test_str(self):
        """测试字符串表示"""
        move = Move(3, 0, 2)
        self.assertEqual(str(move), "移动盘子 3 从柱 0 到柱 2")
    
    def test_to_tuple(self):
        """测试元组转换"""
        move = Move(2, 1, 0)
        self.assertEqual(move.to_tuple(), (2, 1, 0))


class TestVisualizeMoves(unittest.TestCase):
    """测试可视化"""
    
    def test_visualize(self):
        """测试可视化生成"""
        moves = solve_recursive(2)
        visualizations = list(visualize_moves(2, moves))
        self.assertEqual(len(visualizations), 4)  # 初始 + 3次移动


if __name__ == '__main__':
    unittest.main()