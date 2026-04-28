"""
Tic-Tac-Toe 工具模块测试

测试覆盖：
- 棋盘基本操作
- 胜负判断
- Minimax AI
- 游戏管理
- 序列化/反序列化
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    TicTacToeBoard, TicTacToeAI, TicTacToeGame, Player, GameResult,
    find_best_move, evaluate_position, play_game, is_perfect_game,
    create_board, create_ai, create_game
)


class TestTicTacToeBoard(unittest.TestCase):
    """测试棋盘类"""
    
    def test_create_empty_board(self):
        """测试创建空棋盘"""
        board = TicTacToeBoard()
        self.assertEqual(board.move_count, 0)
        self.assertEqual(board.current_player, Player.X)
        self.assertEqual(board.check_result(), GameResult.ONGOING)
        self.assertFalse(board.is_game_over())
    
    def test_make_move(self):
        """测试走棋"""
        board = TicTacToeBoard()
        
        # 有效走法
        self.assertTrue(board.make_move(1, 1))
        self.assertEqual(board.get_cell(1, 1), Player.X)
        self.assertEqual(board.current_player, Player.O)
        self.assertEqual(board.move_count, 1)
        
        # 无效走法（位置已占用）
        self.assertFalse(board.make_move(1, 1))
        self.assertEqual(board.move_count, 1)
        
        # 无效走法（超出范围）
        self.assertFalse(board.make_move(3, 0))
        self.assertFalse(board.make_move(-1, 0))
    
    def test_get_available_moves(self):
        """测试获取可用走法"""
        board = TicTacToeBoard()
        moves = board.get_available_moves()
        self.assertEqual(len(moves), 9)
        
        board.make_move(1, 1)
        moves = board.get_available_moves()
        self.assertEqual(len(moves), 8)
        self.assertNotIn((1, 1), moves)
    
    def test_undo_move(self):
        """测试撤销走法"""
        board = TicTacToeBoard()
        board.make_move(0, 0)
        board.make_move(1, 1)
        self.assertEqual(board.move_count, 2)
        
        self.assertTrue(board.undo_move())
        self.assertEqual(board.move_count, 1)
        self.assertEqual(board.get_cell(1, 1), Player.EMPTY)
        self.assertEqual(board.current_player, Player.O)
        
        # 撤销空棋盘
        board = TicTacToeBoard()
        self.assertFalse(board.undo_move())
    
    def test_x_win_horizontal(self):
        """测试 X 横向获胜"""
        board = TicTacToeBoard()
        # X: 0,0  0,1  0,2
        # O: 1,0  1,1
        board.make_move(0, 0)  # X
        board.make_move(1, 0)  # O
        board.make_move(0, 1)  # X
        board.make_move(1, 1)  # O
        board.make_move(0, 2)  # X 获胜
        
        self.assertEqual(board.get_winner(), Player.X)
        self.assertEqual(board.check_result(), GameResult.X_WIN)
        self.assertTrue(board.is_game_over())
        self.assertEqual(board.get_winning_line(), [(0, 0), (0, 1), (0, 2)])
    
    def test_o_win_vertical(self):
        """测试 O 纵向获胜"""
        board = TicTacToeBoard()
        # O: 0,0  1,0  2,0
        # X: 0,1  1,1
        board.make_move(0, 1)  # X
        board.make_move(0, 0)  # O
        board.make_move(1, 1)  # X
        board.make_move(1, 0)  # O
        board.make_move(2, 2)  # X
        board.make_move(2, 0)  # O 获胜
        
        self.assertEqual(board.get_winner(), Player.O)
        self.assertEqual(board.check_result(), GameResult.O_WIN)
    
    def test_x_win_diagonal(self):
        """测试 X 对角线获胜"""
        board = TicTacToeBoard()
        # X: 0,0  1,1  2,2 (对角线)
        board.make_move(0, 0)  # X
        board.make_move(0, 1)  # O
        board.make_move(1, 1)  # X
        board.make_move(0, 2)  # O
        board.make_move(2, 2)  # X 获胜
        
        self.assertEqual(board.get_winner(), Player.X)
        self.assertEqual(board.get_winning_line(), [(0, 0), (1, 1), (2, 2)])
    
    def test_o_win_anti_diagonal(self):
        """测试 O 反对角线获胜"""
        board = TicTacToeBoard()
        # O: 0,2  1,1  2,0 (反对角线)
        board.make_move(0, 0)  # X
        board.make_move(0, 2)  # O
        board.make_move(2, 2)  # X
        board.make_move(1, 1)  # O
        board.make_move(1, 0)  # X
        board.make_move(2, 0)  # O 获胜
        
        self.assertEqual(board.get_winner(), Player.O)
        self.assertEqual(board.get_winning_line(), [(0, 2), (1, 1), (2, 0)])
    
    def test_draw(self):
        """测试平局"""
        board = TicTacToeBoard()
        # 构造一个平局
        # X O X
        # O X O
        # O X O  -- 这个不可能，重新构造
        # X O X
        # X X O
        # O X O
        board.make_move(0, 0)  # X
        board.make_move(0, 1)  # O
        board.make_move(0, 2)  # X
        board.make_move(1, 2)  # O
        board.make_move(1, 0)  # X
        board.make_move(2, 0)  # O
        board.make_move(1, 1)  # X
        board.make_move(2, 2)  # O
        board.make_move(2, 1)  # X
        
        self.assertIsNone(board.get_winner())
        self.assertEqual(board.check_result(), GameResult.DRAW)
        self.assertTrue(board.is_game_over())
    
    def test_serialization(self):
        """测试序列化"""
        board = TicTacToeBoard()
        board.make_move(1, 1)
        board.make_move(0, 0)
        
        # 字符串序列化
        state = board.to_string()
        self.assertEqual(len(state), 9)
        
        board2 = TicTacToeBoard.from_string(state)
        self.assertEqual(board.get_cell(1, 1), board2.get_cell(1, 1))
        self.assertEqual(board.get_cell(0, 0), board2.get_cell(0, 0))
        
        # JSON 序列化
        json_str = board.to_json()
        board3 = TicTacToeBoard.from_json(json_str)
        self.assertEqual(board.get_cell(1, 1), board3.get_cell(1, 1))
    
    def test_copy(self):
        """测试深拷贝"""
        board = TicTacToeBoard()
        board.make_move(1, 1)  # X 在中心
        
        board_copy = board.copy()
        # 复制后，当前玩家应该是 O
        self.assertEqual(board_copy.current_player, Player.O)
        board_copy.make_move(0, 0)  # O 在左上角
        
        # 原棋盘不受影响
        self.assertEqual(board.get_cell(0, 0), Player.EMPTY)
        self.assertEqual(board_copy.get_cell(0, 0), Player.O)
    
    def test_string_representation(self):
        """测试字符串表示"""
        board = TicTacToeBoard()
        s = str(board)
        self.assertIn("|", s)
        self.assertIn("---", s)


class TestTicTacToeAI(unittest.TestCase):
    """测试 AI 类"""
    
    def test_create_ai(self):
        """测试创建 AI"""
        ai = TicTacToeAI(difficulty='easy')
        self.assertEqual(ai.difficulty, 'easy')
        
        ai = TicTacToeAI(difficulty='hard')
        self.assertEqual(ai.difficulty, 'hard')
        
        with self.assertRaises(ValueError):
            TicTacToeAI(difficulty='invalid')
    
    def test_ai_winning_move(self):
        """测试 AI 能识别获胜走法"""
        board = TicTacToeBoard()
        # X 有两个，再下一步就赢
        board.make_move(0, 0)  # X
        board.make_move(1, 0)  # O
        board.make_move(0, 1)  # X
        board.make_move(1, 1)  # O
        # X 应该走 0,2 获胜
        
        ai = TicTacToeAI(difficulty='hard')
        move = ai.get_move(board)
        self.assertEqual(move, (0, 2))
    
    def test_ai_blocks_opponent(self):
        """测试 AI 能阻止对手获胜"""
        board = TicTacToeBoard()
        # O 有两个，X 需要阻止
        board.make_move(1, 1)  # X
        board.make_move(0, 0)  # O
        board.make_move(2, 2)  # X
        board.make_move(0, 1)  # O
        # X 应该走 0,2 阻止 O 获胜
        
        ai = TicTacToeAI(difficulty='hard')
        move = ai.get_move(board)
        self.assertEqual(move, (0, 2))
    
    def test_ai_takes_center(self):
        """测试 AI 会抢占中心"""
        board = TicTacToeBoard()
        ai = TicTacToeAI(difficulty='hard')
        move = ai.get_move(board)
        self.assertEqual(move, (1, 1))  # 中心是最优开局
    
    def test_ai_easy_makes_valid_move(self):
        """测试简单 AI 返回有效走法"""
        board = TicTacToeBoard()
        ai = TicTacToeAI(difficulty='easy')
        
        for _ in range(5):
            board_copy = board.copy()
            move = ai.get_move(board_copy)
            self.assertIn(move, board_copy.get_available_moves())
    
    def test_ai_game_over_error(self):
        """测试游戏结束后调用 AI 抛出异常"""
        board = TicTacToeBoard()
        # 快速结束游戏
        board.make_move(0, 0)
        board.make_move(1, 0)
        board.make_move(0, 1)
        board.make_move(1, 1)
        board.make_move(0, 2)  # X 获胜
        
        ai = TicTacToeAI(difficulty='hard')
        with self.assertRaises(ValueError):
            ai.get_move(board)


class TestTicTacToeGame(unittest.TestCase):
    """测试游戏管理类"""
    
    def test_create_game(self):
        """测试创建游戏"""
        game = TicTacToeGame()
        self.assertEqual(game.current_player, Player.X)
        self.assertFalse(game.is_game_over)
        self.assertIsNone(game.result)
    
    def test_human_move(self):
        """测试人类走棋"""
        game = TicTacToeGame(x_player='human', o_player='ai_easy')
        
        # X 是人类
        self.assertTrue(game.make_move(1, 1))
        self.assertEqual(game.current_player, Player.O)
        
        # O 是 AI，人类不能走
        self.assertFalse(game.make_move(0, 0))
    
    def test_ai_move(self):
        """测试 AI 走棋"""
        game = TicTacToeGame(x_player='ai_hard', o_player='human')
        
        # X 是 AI
        move = game.ai_move()
        self.assertIsNotNone(move)
        self.assertEqual(game.current_player, Player.O)
        
        # O 是人类，AI 不能走
        self.assertIsNone(game.ai_move())
    
    def test_auto_play(self):
        """测试自动对弈"""
        game = TicTacToeGame(x_player='ai_hard', o_player='ai_hard')
        result = game.auto_play()
        
        self.assertTrue(game.is_game_over)
        self.assertIn(result, [GameResult.X_WIN, GameResult.O_WIN, GameResult.DRAW])
    
    def test_reset_game(self):
        """测试重置游戏"""
        game = TicTacToeGame(x_player='ai_hard', o_player='ai_hard')
        game.auto_play()
        
        self.assertTrue(game.is_game_over)
        game.reset()
        
        self.assertFalse(game.is_game_over)
        self.assertEqual(game.move_count if hasattr(game, 'move_count') else 0, 0)
    
    def test_get_move_suggestion(self):
        """测试获取走法建议"""
        game = TicTacToeGame(x_player='human', o_player='human')
        suggestion = game.get_move_suggestion()
        self.assertEqual(suggestion, (1, 1))  # 中心是最优开局


class TestUtilityFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_find_best_move(self):
        """测试查找最佳走法"""
        board = TicTacToeBoard()
        move = find_best_move(board)
        self.assertEqual(move, (1, 1))
    
    def test_evaluate_position(self):
        """测试位置评估"""
        board = TicTacToeBoard()
        score = evaluate_position(board, Player.X)
        self.assertEqual(score, 0)  # 空棋盘，均势
        
        # X 占中心，有利
        board.make_move(1, 1)
        score = evaluate_position(board, Player.X)
        self.assertGreater(score, 0)
    
    def test_create_board(self):
        """测试创建棋盘函数"""
        board = create_board()
        self.assertIsInstance(board, TicTacToeBoard)
    
    def test_create_ai(self):
        """测试创建 AI 函数"""
        ai = create_ai('easy')
        self.assertIsInstance(ai, TicTacToeAI)
        self.assertEqual(ai.difficulty, 'easy')
    
    def test_create_game(self):
        """测试创建游戏函数"""
        game = create_game()
        self.assertIsInstance(game, TicTacToeGame)


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""
    
    def test_full_board_no_winner(self):
        """测试满盘无胜者"""
        # X X O
        # O O X
        # X O X
        board = TicTacToeBoard()
        moves = [(0, 0), (0, 2), (0, 1), (1, 0), (1, 2), (1, 1), (2, 0), (2, 1), (2, 2)]
        for i, (r, c) in enumerate(moves):
            player = Player.X if i % 2 == 0 else Player.O
            board.make_move(r, c, player)
        
        self.assertTrue(board.is_game_over())
        self.assertEqual(board.check_result(), GameResult.DRAW)
    
    def test_invalid_string_deserialization(self):
        """测试无效字符串反序列化"""
        with self.assertRaises(ValueError):
            TicTacToeBoard.from_string("too short")
        
        with self.assertRaises(ValueError):
            TicTacToeBoard.from_string("invalid!!")
    
    def test_board_equality(self):
        """测试棋盘相等性"""
        board1 = TicTacToeBoard()
        board2 = TicTacToeBoard()
        
        self.assertEqual(board1, board2)
        
        board1.make_move(1, 1)
        self.assertNotEqual(board1, board2)
    
    def test_consecutive_undo(self):
        """测试连续撤销"""
        board = TicTacToeBoard()
        board.make_move(0, 0)
        board.make_move(1, 1)
        board.make_move(2, 2)
        
        board.undo_move()
        self.assertEqual(board.move_count, 2)
        
        board.undo_move()
        self.assertEqual(board.move_count, 1)
        
        board.undo_move()
        self.assertEqual(board.move_count, 0)
        self.assertEqual(board.current_player, Player.X)


class TestPerformance(unittest.TestCase):
    """测试性能"""
    
    def test_ai_response_time(self):
        """测试 AI 响应时间"""
        import time
        
        ai = TicTacToeAI(difficulty='hard')
        
        # 测试多个场景的响应时间
        total_time = 0
        for _ in range(10):
            board = TicTacToeBoard()
            # 随机走几步
            import random
            for _ in range(random.randint(0, 4)):
                moves = board.get_available_moves()
                if moves:
                    m = random.choice(moves)
                    board.make_move(m[0], m[1])
            
            start = time.time()
            ai.get_move(board)
            total_time += time.time() - start
        
        # 平均响应时间应该很短
        avg_time = total_time / 10
        self.assertLess(avg_time, 0.5)  # 平均小于 500ms（考虑不同运行环境）


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)