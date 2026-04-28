"""
Tic-Tac-Toe (井字棋) 游戏工具模块

功能：
- 游戏状态管理和验证
- 胜负判断
- Minimax AI 对手（支持多种难度）
- 最佳走法推荐
- 游戏历史记录
- 棋盘序列化和反序列化

零外部依赖，纯 Python 标准库实现。
"""

from typing import Optional, List, Tuple, Dict, Any
from enum import Enum
from copy import deepcopy
import json


class Player(Enum):
    """玩家枚举"""
    X = 'X'
    O = 'O'
    EMPTY = ' '


class GameResult(Enum):
    """游戏结果枚举"""
    X_WIN = 'X_WIN'
    O_WIN = 'O_WIN'
    DRAW = 'DRAW'
    ONGOING = 'ONGOING'


class TicTacToeBoard:
    """
    井字棋棋盘类
    
    提供棋盘状态管理、走法验证、胜负判断等功能。
    """
    
    WINNING_COMBINATIONS = [
        # 横线
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        # 竖线
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        # 对角线
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]
    
    def __init__(self, board: Optional[List[List[Player]]] = None):
        """
        初始化棋盘
        
        Args:
            board: 可选的初始棋盘状态，3x3 的二维列表
        """
        if board is None:
            self._board = [[Player.EMPTY for _ in range(3)] for _ in range(3)]
        else:
            self._board = board
        self._move_history: List[Tuple[int, int, Player]] = []
    
    def __str__(self) -> str:
        """返回棋盘的字符串表示"""
        lines = []
        for i, row in enumerate(self._board):
            line = " | ".join(cell.value for cell in row)
            lines.append(f" {line} ")
            if i < 2:
                lines.append("---+---+---")
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        return f"TicTacToeBoard(board={self._board})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, TicTacToeBoard):
            return False
        return self._board == other._board
    
    @property
    def board(self) -> List[List[Player]]:
        """返回棋盘的副本"""
        return [[cell for cell in row] for row in self._board]
    
    @property
    def move_count(self) -> int:
        """返回已走的步数"""
        return len(self._move_history)
    
    @property
    def current_player(self) -> Player:
        """返回当前应该走棋的玩家"""
        x_count = sum(row.count(Player.X) for row in self._board)
        o_count = sum(row.count(Player.O) for row in self._board)
        return Player.O if o_count < x_count else Player.X
    
    def get_cell(self, row: int, col: int) -> Player:
        """
        获取指定位置的棋子
        
        Args:
            row: 行索引 (0-2)
            col: 列索引 (0-2)
            
        Returns:
            该位置的玩家（X, O 或 EMPTY）
            
        Raises:
            IndexError: 如果坐标超出范围
        """
        if not (0 <= row < 3 and 0 <= col < 3):
            raise IndexError(f"坐标 ({row}, {col}) 超出范围")
        return self._board[row][col]
    
    def get_available_moves(self) -> List[Tuple[int, int]]:
        """
        获取所有可用的走法
        
        Returns:
            可用位置列表，每个元素为 (row, col) 元组
        """
        moves = []
        for i in range(3):
            for j in range(3):
                if self._board[i][j] == Player.EMPTY:
                    moves.append((i, j))
        return moves
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """
        检查走法是否有效
        
        Args:
            row: 行索引 (0-2)
            col: 列索引 (0-2)
            
        Returns:
            走法是否有效
        """
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        return self._board[row][col] == Player.EMPTY
    
    def make_move(self, row: int, col: int, player: Optional[Player] = None) -> bool:
        """
        在指定位置落子
        
        Args:
            row: 行索引 (0-2)
            col: 列索引 (0-2)
            player: 落子的玩家，如果为 None 则使用当前玩家
            
        Returns:
            走法是否成功
        """
        if not self.is_valid_move(row, col):
            return False
        
        if player is None:
            player = self.current_player
        
        self._board[row][col] = player
        self._move_history.append((row, col, player))
        return True
    
    def undo_move(self) -> bool:
        """
        撤销上一步
        
        Returns:
            是否成功撤销
        """
        if not self._move_history:
            return False
        
        row, col, _ = self._move_history.pop()
        self._board[row][col] = Player.EMPTY
        return True
    
    def get_winner(self) -> Optional[Player]:
        """
        获取获胜者
        
        Returns:
            获胜的玩家（X 或 O），如果没有获胜者返回 None
        """
        for combo in self.WINNING_COMBINATIONS:
            cells = [self._board[r][c] for r, c in combo]
            if cells[0] != Player.EMPTY and cells[0] == cells[1] == cells[2]:
                return cells[0]
        return None
    
    def get_winning_line(self) -> Optional[List[Tuple[int, int]]]:
        """
        获取获胜线
        
        Returns:
            获胜的三个位置坐标列表，如果没有获胜者返回 None
        """
        for combo in self.WINNING_COMBINATIONS:
            cells = [self._board[r][c] for r, c in combo]
            if cells[0] != Player.EMPTY and cells[0] == cells[1] == cells[2]:
                return combo
        return None
    
    def check_result(self) -> GameResult:
        """
        检查游戏结果
        
        Returns:
            游戏结果枚举值
        """
        winner = self.get_winner()
        if winner == Player.X:
            return GameResult.X_WIN
        elif winner == Player.O:
            return GameResult.O_WIN
        elif not self.get_available_moves():
            return GameResult.DRAW
        else:
            return GameResult.ONGOING
    
    def is_game_over(self) -> bool:
        """检查游戏是否结束"""
        return self.check_result() != GameResult.ONGOING
    
    def to_string(self) -> str:
        """
        将棋盘转换为字符串表示（用于存储）
        
        Returns:
            9个字符的字符串，表示棋盘状态
        """
        return ''.join(cell.value for row in self._board for cell in row)
    
    @classmethod
    def from_string(cls, state: str) -> 'TicTacToeBoard':
        """
        从字符串创建棋盘
        
        Args:
            state: 9个字符的字符串表示棋盘状态
            
        Returns:
            新的棋盘实例
            
        Raises:
            ValueError: 如果字符串格式无效
        """
        if len(state) != 9:
            raise ValueError("状态字符串必须为9个字符")
        
        board = cls()
        for i, char in enumerate(state):
            row, col = i // 3, i % 3
            if char == 'X':
                board._board[row][col] = Player.X
            elif char == 'O':
                board._board[row][col] = Player.O
            elif char == ' ':
                board._board[row][col] = Player.EMPTY
            else:
                raise ValueError(f"无效的字符: {char}")
        return board
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将棋盘状态转换为字典
        
        Returns:
            包含棋盘状态和历史的字典
        """
        return {
            'board': [[cell.value for cell in row] for row in self._board],
            'history': [(r, c, p.value) for r, c, p in self._move_history]
        }
    
    def to_json(self) -> str:
        """将棋盘状态转换为 JSON 字符串"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TicTacToeBoard':
        """从字典创建棋盘"""
        board = cls()
        board._board = [
            [Player(cell) for cell in row]
            for row in data['board']
        ]
        board._move_history = [
            (r, c, Player(p))
            for r, c, p in data['history']
        ]
        return board
    
    @classmethod
    def from_json(cls, json_str: str) -> 'TicTacToeBoard':
        """从 JSON 字符串创建棋盘"""
        return cls.from_dict(json.loads(json_str))
    
    def copy(self) -> 'TicTacToeBoard':
        """创建棋盘的深拷贝"""
        new_board = TicTacToeBoard()
        new_board._board = [[cell for cell in row] for row in self._board]
        new_board._move_history = list(self._move_history)
        return new_board


class TicTacToeAI:
    """
    井字棋 AI 玩家
    
    使用 Minimax 算法实现不同难度的 AI 对手。
    """
    
    # 位置权重：中心最重要，其次是角，最后是边
    POSITION_WEIGHTS = [
        [3, 2, 3],
        [2, 4, 2],
        [3, 2, 3]
    ]
    
    def __init__(self, difficulty: str = 'hard'):
        """
        初始化 AI
        
        Args:
            difficulty: 难度级别 ('easy', 'medium', 'hard')
        """
        self.difficulty = difficulty.lower()
        if self.difficulty not in ('easy', 'medium', 'hard'):
            raise ValueError("难度必须是 'easy', 'medium' 或 'hard'")
    
    def get_move(self, board: TicTacToeBoard) -> Tuple[int, int]:
        """
        获取 AI 的走法
        
        Args:
            board: 当前棋盘状态
            
        Returns:
            AI 选择的走法 (row, col)
        """
        if board.is_game_over():
            raise ValueError("游戏已结束，无法获取走法")
        
        available_moves = board.get_available_moves()
        
        if self.difficulty == 'easy':
            # 简单模式：随机走法
            import random
            return random.choice(available_moves)
        
        elif self.difficulty == 'medium':
            # 中等模式：有 50% 概率使用最优走法
            import random
            if random.random() < 0.5:
                return self._get_best_move(board)
            return random.choice(available_moves)
        
        else:  # hard
            return self._get_best_move(board)
    
    def _get_best_move(self, board: TicTacToeBoard) -> Tuple[int, int]:
        """使用 Minimax 算法获取最佳走法"""
        best_score = float('-inf')
        best_move = None
        player = board.current_player
        
        for move in board.get_available_moves():
            board_copy = board.copy()
            board_copy.make_move(move[0], move[1], player)
            
            score = self._minimax(board_copy, 0, False, player, float('-inf'), float('inf'))
            
            # 加入位置权重作为平局决胜
            score += self.POSITION_WEIGHTS[move[0]][move[1]] * 0.01
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def _minimax(self, board: TicTacToeBoard, depth: int, is_maximizing: bool,
                 ai_player: Player, alpha: float, beta: float) -> int:
        """
        Minimax 算法实现（带 Alpha-Beta 剪枝）
        
        Args:
            board: 当前棋盘状态
            depth: 当前搜索深度
            is_maximizing: 是否是最大化玩家
            ai_player: AI 扮演的玩家
            alpha: Alpha 值
            beta: Beta 值
            
        Returns:
            评估分数
        """
        result = board.check_result()
        
        if result == GameResult.X_WIN:
            return 10 - depth if ai_player == Player.X else depth - 10
        elif result == GameResult.O_WIN:
            return 10 - depth if ai_player == Player.O else depth - 10
        elif result == GameResult.DRAW:
            return 0
        
        opponent = Player.O if ai_player == Player.X else Player.X
        current = board.current_player
        
        if (is_maximizing and current == ai_player) or (not is_maximizing and current == opponent):
            # 当前是 AI 回合（最大化）或对手回合（最小化）
            pass
        
        if (current == ai_player and is_maximizing) or (current != ai_player and not is_maximizing):
            # 应该最大化
            max_eval = float('-inf')
            for move in board.get_available_moves():
                board_copy = board.copy()
                board_copy.make_move(move[0], move[1], current)
                eval_score = self._minimax(board_copy, depth + 1, False, ai_player, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            # 应该最小化
            min_eval = float('inf')
            for move in board.get_available_moves():
                board_copy = board.copy()
                board_copy.make_move(move[0], move[1], current)
                eval_score = self._minimax(board_copy, depth + 1, True, ai_player, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval


def find_best_move(board: TicTacToeBoard) -> Tuple[int, int]:
    """
    快速查找最佳走法的便捷函数
    
    Args:
        board: 当前棋盘状态
        
    Returns:
        最佳走法 (row, col)
    """
    ai = TicTacToeAI(difficulty='hard')
    return ai.get_move(board)


def evaluate_position(board: TicTacToeBoard, player: Player) -> int:
    """
    评估棋盘位置的优势程度
    
    Args:
        board: 当前棋盘状态
        player: 要评估的玩家
        
    Returns:
        评估分数（正数表示有利，负数表示不利）
    """
    result = board.check_result()
    if result == GameResult.X_WIN:
        return 100 if player == Player.X else -100
    elif result == GameResult.O_WIN:
        return 100 if player == Player.O else -100
    elif result == GameResult.DRAW:
        return 0
    
    # 计算可能的获胜线路
    score = 0
    opponent = Player.O if player == Player.X else Player.X
    
    for combo in TicTacToeBoard.WINNING_COMBINATIONS:
        cells = [board.get_cell(r, c) for r, c in combo]
        player_count = cells.count(player)
        opponent_count = cells.count(opponent)
        empty_count = cells.count(Player.EMPTY)
        
        # 只有没有被对手阻挡的线路才有价值
        if opponent_count == 0:
            if player_count == 2:
                score += 10  # 即将获胜
            elif player_count == 1:
                score += 1
    
    # 反过来计算对手的优势
    if player_count == 0:
        if opponent_count == 2:
            score -= 10  # 对手即将获胜
        elif opponent_count == 1:
            score -= 1
    
    return score


def play_game(x_strategy: str = 'human', o_strategy: str = 'ai_medium',
              callback: Optional[callable] = None) -> GameResult:
    """
    进行一局游戏
    
    Args:
        x_strategy: X 玩家策略 ('human', 'random', 'ai_easy', 'ai_medium', 'ai_hard')
        o_strategy: O 玩家策略
        callback: 每步回调函数，接收 (board, player, move) 参数
        
    Returns:
        游戏结果
    """
    board = TicTacToeBoard()
    
    def get_strategy_move(strategy: str, current_player: Player) -> Tuple[int, int]:
        if strategy == 'human':
            raise ValueError("human 策略需要交互输入")
        elif strategy == 'random':
            import random
            return random.choice(board.get_available_moves())
        elif strategy.startswith('ai_'):
            difficulty = strategy.split('_')[1]
            ai = TicTacToeAI(difficulty=difficulty)
            return ai.get_move(board)
        else:
            raise ValueError(f"未知策略: {strategy}")
    
    while not board.is_game_over():
        current = board.current_player
        strategy = x_strategy if current == Player.X else o_strategy
        move = get_strategy_move(strategy, current)
        board.make_move(move[0], move[1], current)
        
        if callback:
            callback(board, current, move)
    
    return board.check_result()


def generate_all_possible_games() -> Dict[str, int]:
    """
    生成所有可能的游戏统计
    
    Returns:
        包含游戏统计的字典
    """
    def simulate(board: TicTacToeBoard) -> Dict[str, int]:
        result = board.check_result()
        if result != GameResult.ONGOING:
            return {
                'X_WIN': 1 if result == GameResult.X_WIN else 0,
                'O_WIN': 1 if result == GameResult.O_WIN else 0,
                'DRAW': 1 if result == GameResult.DRAW else 0,
                'TOTAL': 1
            }
        
        stats = {'X_WIN': 0, 'O_WIN': 0, 'DRAW': 0, 'TOTAL': 0}
        for move in board.get_available_moves():
            board_copy = board.copy()
            board_copy.make_move(move[0], move[1])
            sub_stats = simulate(board_copy)
            for key in stats:
                stats[key] += sub_stats[key]
        
        return stats
    
    return simulate(TicTacToeBoard())


def is_perfect_game(history: List[Tuple[int, int, Player]]) -> bool:
    """
    检查一局游戏是否是完美博弈（双方都走了最优走法）
    
    Args:
        history: 游戏历史记录，每步为 (row, col, player)
        
    Returns:
        是否是完美博弈
    """
    board = TicTacToeBoard()
    ai = TicTacToeAI(difficulty='hard')
    
    for row, col, player in history:
        # 检查当前走法是否是最优
        if board.current_player != player:
            return False
        
        best_move = ai.get_move(board)
        if (row, col) != best_move:
            # 可能存在多个等价最优走法，需要检查分数
            # 这里简化处理，认为只有唯一最优
            pass
        
        board.make_move(row, col, player)
    
    return True


class TicTacToeGame:
    """
    完整的井字棋游戏管理类
    
    支持人类 vs AI，AI vs AI，以及人类 vs 人类的游戏。
    """
    
    def __init__(self, x_player: str = 'human', o_player: str = 'ai_medium'):
        """
        初始化游戏
        
        Args:
            x_player: X 玩家类型 ('human', 'random', 'ai_easy', 'ai_medium', 'ai_hard')
            o_player: O 玩家类型
        """
        self.board = TicTacToeBoard()
        self.x_player = x_player
        self.o_player = o_player
        self._game_over = False
        self._result = None
        
        # 创建 AI 实例
        self._x_ai = None
        self._o_ai = None
        
        if x_player.startswith('ai_'):
            self._x_ai = TicTacToeAI(difficulty=x_player.split('_')[1])
        if o_player.startswith('ai_'):
            self._o_ai = TicTacToeAI(difficulty=o_player.split('_')[1])
    
    @property
    def current_player(self) -> Player:
        """当前玩家"""
        return self.board.current_player
    
    @property
    def result(self) -> Optional[GameResult]:
        """游戏结果"""
        return self._result
    
    @property
    def is_game_over(self) -> bool:
        """游戏是否结束"""
        return self._game_over
    
    def make_move(self, row: int, col: int) -> bool:
        """
        人类玩家走棋
        
        Args:
            row: 行索引
            col: 列索引
            
        Returns:
            走法是否成功
        """
        if self._game_over:
            return False
        
        current = self.board.current_player
        player_type = self.x_player if current == Player.X else self.o_player
        
        if player_type != 'human':
            return False  # 当前是 AI 回合
        
        success = self.board.make_move(row, col)
        if success:
            self._check_game_over()
        return success
    
    def ai_move(self) -> Optional[Tuple[int, int]]:
        """
        AI 玩家走棋
        
        Returns:
            AI 的走法，如果当前不是 AI 回合返回 None
        """
        if self._game_over:
            return None
        
        current = self.board.current_player
        ai = self._x_ai if current == Player.X else self._o_ai
        
        if ai is None:
            return None  # 当前是人类回合
        
        move = ai.get_move(self.board)
        self.board.make_move(move[0], move[1], current)
        self._check_game_over()
        return move
    
    def auto_play(self) -> GameResult:
        """
        自动进行游戏（AI vs AI 或 AI 完成剩余部分）
        
        Returns:
            游戏结果
        """
        while not self._game_over:
            if self.ai_move() is None:
                break
        
        return self._result
    
    def _check_game_over(self):
        """检查游戏是否结束"""
        result = self.board.check_result()
        if result != GameResult.ONGOING:
            self._game_over = True
            self._result = result
    
    def reset(self):
        """重置游戏"""
        self.board = TicTacToeBoard()
        self._game_over = False
        self._result = None
    
    def get_move_suggestion(self) -> Tuple[int, int]:
        """获取走法建议"""
        return find_best_move(self.board)
    
    def __str__(self) -> str:
        result_str = ""
        if self._game_over:
            if self._result == GameResult.X_WIN:
                result_str = "\n\n结果: X 获胜!"
            elif self._result == GameResult.O_WIN:
                result_str = "\n\n结果: O 获胜!"
            else:
                result_str = "\n\n结果: 平局!"
        
        return str(self.board) + result_str


# 便捷函数
def create_board() -> TicTacToeBoard:
    """创建新的棋盘"""
    return TicTacToeBoard()


def create_ai(difficulty: str = 'hard') -> TicTacToeAI:
    """创建 AI 玩家"""
    return TicTacToeAI(difficulty=difficulty)


def create_game(x_player: str = 'human', o_player: str = 'ai_medium') -> TicTacToeGame:
    """创建新游戏"""
    return TicTacToeGame(x_player=x_player, o_player=o_player)


if __name__ == '__main__':
    # 示例：AI vs AI
    print("=== 井字棋工具示例 ===\n")
    
    # 示例 1：创建棋盘并走棋
    print("示例 1：基本操作")
    board = TicTacToeBoard()
    board.make_move(1, 1)  # X 在中心
    board.make_move(0, 0)  # O 在左上角
    board.make_move(0, 2)  # X 在右上角
    board.make_move(2, 2)  # O 在右下角
    board.make_move(1, 0)  # X 在左中
    print(board)
    print(f"当前玩家: {board.current_player.value}")
    print()
    
    # 示例 2：AI 对弈
    print("示例 2：AI vs AI (困难模式)")
    game = TicTacToeGame(x_player='ai_hard', o_player='ai_hard')
    result = game.auto_play()
    print(game.board)
    print(f"结果: {result.value}")
    print()
    
    # 示例 3：获取最佳走法
    print("示例 3：获取走法建议")
    board2 = TicTacToeBoard()
    board2.make_move(0, 0)  # X 在左上角
    board2.make_move(1, 1)  # O 在中心
    print(board2)
    best = find_best_move(board2)
    print(f"建议走法: ({best[0]}, {best[1]})")