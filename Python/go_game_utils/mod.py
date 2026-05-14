"""
围棋游戏工具模块 (Go Game Utilities)

提供围棋游戏的完整实现，包括：
- 棋盘管理（9x9, 13x13, 19x19）
- 落子规则（禁入点、打劫）
- 提子规则
- 死活判断
- 眼的识别
- 领地计算
- SGF 格式支持

零外部依赖，仅使用 Python 标准库。
"""

from typing import Optional, List, Tuple, Set, Dict, FrozenSet
from enum import Enum
from dataclasses import dataclass
from copy import deepcopy
import re


class Stone(Enum):
    """棋子枚举"""
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    
    def opponent(self) -> 'Stone':
        """获取对手颜色"""
        if self == Stone.BLACK:
            return Stone.WHITE
        elif self == Stone.WHITE:
            return Stone.BLACK
        return Stone.EMPTY
    
    def to_sgf(self) -> str:
        """转换为 SGF 格式字符"""
        if self == Stone.BLACK:
            return 'B'
        elif self == Stone.WHITE:
            return 'W'
        return ''


class BoardSize(Enum):
    """棋盘大小枚举"""
    SMALL = 9    # 小棋盘
    MEDIUM = 13  # 中棋盘
    STANDARD = 19  # 标准棋盘


@dataclass(frozen=True)
class Move:
    """落子记录"""
    row: int
    col: int
    stone: Stone
    captured: Tuple[Tuple[int, int], ...] = ()
    
    def to_sgf(self) -> str:
        """转换为 SGF 坐标"""
        if self.row < 0 or self.col < 0:
            return ''
        return chr(ord('a') + self.col) + chr(ord('a') + self.row)
    
    @staticmethod
    def from_sgf(sgf_coord: str, stone: Stone) -> 'Move':
        """从 SGF 坐标创建"""
        if len(sgf_coord) != 2:
            raise ValueError(f"无效的 SGF 坐标: {sgf_coord}")
        col = ord(sgf_coord[0]) - ord('a')
        row = ord(sgf_coord[1]) - ord('a')
        return Move(row=row, col=col, stone=stone)
    
    def __str__(self) -> str:
        col_label = chr(ord('A') + self.col) if self.col < 8 else chr(ord('A') + self.col + 1)
        row_label = self.row + 1
        return f"{col_label}{row_label}"


class GoBoard:
    """围棋棋盘类"""
    
    # 星位坐标
    STAR_POINTS = {
        9: [(2, 2), (2, 6), (4, 4), (6, 2), (6, 6)],
        13: [(3, 3), (3, 9), (6, 6), (9, 3), (9, 9),
             (3, 6), (6, 3), (6, 9), (9, 6)],
        19: [(3, 3), (3, 9), (3, 15),
             (9, 3), (9, 9), (9, 15),
             (15, 3), (15, 9), (15, 15)]
    }
    
    def __init__(self, size: int = 19):
        """
        初始化棋盘
        
        Args:
            size: 棋盘大小（9, 13, 19）
        """
        if size not in (9, 13, 19):
            raise ValueError(f"不支持的棋盘大小: {size}，支持: 9, 13, 19")
        self.size = size
        self.board: List[List[Stone]] = [[Stone.EMPTY] * size for _ in range(size)]
        self.history: List[Move] = []
        self.captured: Dict[Stone, int] = {Stone.BLACK: 0, Stone.WHITE: 0}
        self.current_player = Stone.BLACK
        self.ko_point: Optional[Tuple[int, int]] = None
        self.last_move: Optional[Tuple[int, int]] = None
        self.passes: int = 0  # 连续虚手次数
        
    def copy(self) -> 'GoBoard':
        """创建棋盘副本"""
        new_board = GoBoard(self.size)
        new_board.board = [row[:] for row in self.board]
        new_board.history = self.history[:]
        new_board.captured = self.captured.copy()
        new_board.current_player = self.current_player
        new_board.ko_point = self.ko_point
        new_board.last_move = self.last_move
        new_board.passes = self.passes
        return new_board
    
    def get(self, row: int, col: int) -> Stone:
        """获取指定位置的棋子"""
        if not self.is_valid_position(row, col):
            return Stone.EMPTY
        return self.board[row][col]
    
    def set(self, row: int, col: int, stone: Stone) -> None:
        """设置指定位置的棋子（不检查规则）"""
        if self.is_valid_position(row, col):
            self.board[row][col] = stone
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """检查位置是否在棋盘内"""
        return 0 <= row < self.size and 0 <= col < self.size
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """获取相邻位置"""
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if self.is_valid_position(nr, nc):
                neighbors.append((nr, nc))
        return neighbors
    
    def get_group(self, row: int, col: int) -> Set[Tuple[int, int]]:
        """获取连通棋子组"""
        stone = self.get(row, col)
        if stone == Stone.EMPTY:
            return set()
        
        group = set()
        stack = [(row, col)]
        
        while stack:
            r, c = stack.pop()
            if (r, c) in group:
                continue
            if self.get(r, c) != stone:
                continue
            group.add((r, c))
            stack.extend(self.get_neighbors(r, c))
        
        return group
    
    def get_liberties(self, group: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        """获取棋子组的气"""
        liberties = set()
        for row, col in group:
            for nr, nc in self.get_neighbors(row, col):
                if self.get(nr, nc) == Stone.EMPTY:
                    liberties.add((nr, nc))
        return liberties
    
    def count_liberties(self, row: int, col: int) -> int:
        """计算指定位置棋子的气数"""
        group = self.get_group(row, col)
        if not group:
            return 0
        return len(self.get_liberties(group))
    
    def is_captured(self, group: Set[Tuple[int, int]]) -> bool:
        """检查棋子组是否被提"""
        return len(self.get_liberties(group)) == 0
    
    def remove_group(self, group: Set[Tuple[int, int]]) -> int:
        """移除棋子组，返回移除的数量"""
        for row, col in group:
            self.board[row][col] = Stone.EMPTY
        return len(group)
    
    def would_be_suicide(self, row: int, col: int, stone: Stone) -> bool:
        """检查落子是否为自杀"""
        if self.get(row, col) != Stone.EMPTY:
            return False
        
        # 临时放置棋子
        self.board[row][col] = stone
        
        # 检查是否能提对方的子
        opponent = stone.opponent()
        can_capture = False
        for nr, nc in self.get_neighbors(row, col):
            if self.get(nr, nc) == opponent:
                group = self.get_group(nr, nc)
                if self.is_captured(group):
                    can_capture = True
                    break
        
        # 检查自己是否有气
        own_group = self.get_group(row, col)
        own_liberties = self.get_liberties(own_group)
        
        # 恢复
        self.board[row][col] = Stone.EMPTY
        
        # 如果能提子或者自己有气，则不是自杀
        return not can_capture and len(own_liberties) == 0
    
    def is_ko(self, row: int, col: int) -> bool:
        """检查是否为打劫点"""
        return self.ko_point == (row, col)
    
    def is_legal_move(self, row: int, col: int, stone: Stone = None) -> Tuple[bool, str]:
        """
        检查落子是否合法
        
        Returns:
            (是否合法, 原因)
        """
        if stone is None:
            stone = self.current_player
        
        # 检查位置是否在棋盘内
        if not self.is_valid_position(row, col):
            return False, "位置超出棋盘范围"
        
        # 检查位置是否为空
        if self.get(row, col) != Stone.EMPTY:
            return False, "该位置已有棋子"
        
        # 检查是否为打劫点
        if self.is_ko(row, col):
            return False, "打劫点，不能立即落子"
        
        # 检查是否为自杀
        if self.would_be_suicide(row, col, stone):
            return False, "自杀点，不能落子"
        
        return True, "合法落子"
    
    def play(self, row: int, col: int, stone: Stone = None) -> Tuple[bool, str, int]:
        """
        落子
        
        Returns:
            (是否成功, 原因, 提子数量)
        """
        if stone is None:
            stone = self.current_player
        
        legal, reason = self.is_legal_move(row, col, stone)
        if not legal:
            return False, reason, 0
        
        # 放置棋子
        self.board[row][col] = stone
        
        # 提子
        captured = []
        opponent = stone.opponent()
        for nr, nc in self.get_neighbors(row, col):
            if self.get(nr, nc) == opponent:
                group = self.get_group(nr, nc)
                if self.is_captured(group):
                    captured.extend(group)
        
        # 移除被提的子
        captured_set = set(captured)
        num_captured = 0
        for r, c in captured_set:
            self.board[r][c] = Stone.EMPTY
            num_captured += 1
        
        self.captured[stone] += num_captured
        
        # 记录历史
        move = Move(row=row, col=col, stone=stone, captured=tuple(captured_set))
        self.history.append(move)
        
        # 更新打劫点
        if num_captured == 1 and len(captured_set) == 1:
            # 检查是否形成打劫
            own_group = self.get_group(row, col)
            if len(own_group) == 1 and len(self.get_liberties(own_group)) == 1:
                self.ko_point = captured[0]
            else:
                self.ko_point = None
        else:
            self.ko_point = None
        
        # 更新状态
        self.last_move = (row, col)
        self.current_player = opponent
        self.passes = 0
        
        return True, "落子成功", num_captured
    
    def pass_turn(self) -> None:
        """虚手"""
        self.history.append(Move(-1, -1, self.current_player))
        self.current_player = self.current_player.opponent()
        self.ko_point = None
        self.passes += 1
    
    def is_game_over(self) -> bool:
        """检查游戏是否结束（双方连续虚手）"""
        return self.passes >= 2
    
    def reset(self) -> None:
        """重置棋盘"""
        self.board = [[Stone.EMPTY] * self.size for _ in range(self.size)]
        self.history = []
        self.captured = {Stone.BLACK: 0, Stone.WHITE: 0}
        self.current_player = Stone.BLACK
        self.ko_point = None
        self.last_move = None
        self.passes = 0
    
    def get_empty_points(self) -> List[Tuple[int, int]]:
        """获取所有空点"""
        points = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == Stone.EMPTY:
                    points.append((row, col))
        return points
    
    def get_legal_moves(self) -> List[Tuple[int, int]]:
        """获取所有合法落子点"""
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_legal_move(row, col)[0]:
                    moves.append((row, col))
        return moves
    
    def is_star_point(self, row: int, col: int) -> bool:
        """检查是否为星位"""
        return (row, col) in self.STAR_POINTS.get(self.size, [])
    
    def get_corner_points(self) -> List[Tuple[int, int]]:
        """获取四个角的位置"""
        return [
            (0, 0), (0, self.size - 1),
            (self.size - 1, 0), (self.size - 1, self.size - 1)
        ]
    
    def get_edge_points(self) -> List[Tuple[int, int]]:
        """获取所有边上的位置"""
        points = []
        for i in range(self.size):
            points.extend([(0, i), (self.size - 1, i), (i, 0), (i, self.size - 1)])
        return list(set(points))
    
    def __str__(self) -> str:
        """转换为字符串表示"""
        result = []
        
        # 列标记
        header = "   "
        for col in range(self.size):
            label = chr(ord('A') + col) if col < 8 else chr(ord('A') + col + 1)
            header += f" {label}"
        result.append(header)
        
        # 棋盘
        for row in range(self.size - 1, -1, -1):
            line = f"{row + 1:2d} "
            for col in range(self.size):
                stone = self.board[row][col]
                if stone == Stone.EMPTY:
                    if self.is_star_point(row, col):
                        line += " +"
                    else:
                        line += " ."
                elif stone == Stone.BLACK:
                    line += " X"
                else:
                    line += " O"
            line += f" {row + 1:2d}"
            result.append(line)
        
        result.append(header)
        result.append(f"当前玩家: {'黑' if self.current_player == Stone.BLACK else '白'}")
        result.append(f"提子: 黑 {self.captured[Stone.BLACK]} | 白 {self.captured[Stone.WHITE]}")
        
        return "\n".join(result)


class Territory:
    """领地计算类"""
    
    @staticmethod
    def calculate(board: GoBoard) -> Dict[Stone, int]:
        """
        计算各方的领地
        
        Returns:
            {黑方领地, 白方领地}
        """
        territory = {Stone.BLACK: 0, Stone.WHITE: 0}
        visited = set()
        
        for row in range(board.size):
            for col in range(board.size):
                if (row, col) in visited:
                    continue
                if board.get(row, col) != Stone.EMPTY:
                    continue
                
                # 找到连通的空点区域
                region = set()
                borders: Set[Stone] = set()
                stack = [(row, col)]
                
                while stack:
                    r, c = stack.pop()
                    if (r, c) in region:
                        continue
                    
                    stone = board.get(r, c)
                    if stone != Stone.EMPTY:
                        borders.add(stone)
                        continue
                    
                    region.add((r, c))
                    visited.add((r, c))
                    stack.extend(board.get_neighbors(r, c))
                
                # 如果区域只被一种颜色包围，则归属该方
                if len(borders) == 1:
                    owner = list(borders)[0]
                    territory[owner] += len(region)
        
        return territory
    
    @staticmethod
    def get_territory_map(board: GoBoard) -> Dict[Tuple[int, int], Optional[Stone]]:
        """
        获取每个空点的归属
        
        Returns:
            {(row, col): 归属颜色} None 表示无归属
        """
        result = {}
        visited = set()
        
        for row in range(board.size):
            for col in range(board.size):
                if (row, col) in visited:
                    continue
                if board.get(row, col) != Stone.EMPTY:
                    continue
                
                region = set()
                borders: Set[Stone] = set()
                stack = [(row, col)]
                
                while stack:
                    r, c = stack.pop()
                    if (r, c) in region:
                        continue
                    
                    stone = board.get(r, c)
                    if stone != Stone.EMPTY:
                        borders.add(stone)
                        continue
                    
                    region.add((r, c))
                    visited.add((r, c))
                    stack.extend(board.get_neighbors(r, c))
                
                owner = list(borders)[0] if len(borders) == 1 else None
                for pos in region:
                    result[pos] = owner
        
        return result


class LifeDeath:
    """死活判断类"""
    
    @staticmethod
    def get_eyes(board: GoBoard, stone: Stone) -> List[Set[Tuple[int, int]]]:
        """
        找到指定颜色的所有眼
        
        眼的定义：被同色棋子完全包围的空点区域
        """
        eyes = []
        visited = set()
        
        for row in range(board.size):
            for col in range(board.size):
                if (row, col) in visited:
                    continue
                if board.get(row, col) != Stone.EMPTY:
                    continue
                
                # 找连通的空点区域
                region = set()
                borders: Set[Stone] = set()
                stack = [(row, col)]
                
                while stack:
                    r, c = stack.pop()
                    if (r, c) in region:
                        continue
                    
                    s = board.get(r, c)
                    if s != Stone.EMPTY:
                        borders.add(s)
                        continue
                    
                    region.add((r, c))
                    visited.add((r, c))
                    stack.extend(board.get_neighbors(r, c))
                
                # 如果只被指定颜色包围，则是眼
                if borders == {stone}:
                    eyes.append(region)
        
        return eyes
    
    @staticmethod
    def is_alive(board: GoBoard, group: Set[Tuple[int, int]], stone: Stone) -> bool:
        """
        判断棋子组是否活棋
        
        简化规则：有两个或以上的真眼则活
        """
        if not group:
            return False
        
        # 找到与该组相邻的眼
        adjacent_eyes = set()
        for r, c in group:
            for nr, nc in board.get_neighbors(r, c):
                if board.get(nr, nc) == Stone.EMPTY:
                    # 检查这个空点是否属于眼
                    for eye in LifeDeath.get_eyes(board, stone):
                        if (nr, nc) in eye:
                            adjacent_eyes.add(frozenset(eye))
        
        # 两个或以上的眼则活
        return len(adjacent_eyes) >= 2
    
    @staticmethod
    def is_dead(board: GoBoard, group: Set[Tuple[int, int]], stone: Stone) -> bool:
        """
        判断棋子组是否死棋
        
        简化规则：没有气且没有眼
        """
        if not group:
            return True
        
        liberties = board.get_liberties(group)
        if not liberties:
            # 检查是否有眼
            eyes = LifeDeath.get_eyes(board, stone)
            for eye in eyes:
                if eye & liberties:
                    return False
            return True
        
        return False
    
    @staticmethod
    def analyze_group(board: GoBoard, row: int, col: int) -> Dict:
        """
        分析棋子组的状态
        
        Returns:
            {
                'size': 大小,
                'liberties': 气数,
                'eyes': 眼数,
                'is_alive': 是否活棋,
                'status': 'alive' | 'dead' | 'uncertain'
            }
        """
        stone = board.get(row, col)
        if stone == Stone.EMPTY:
            return {'size': 0, 'liberties': 0, 'eyes': 0, 'is_alive': False, 'status': 'empty'}
        
        group = board.get_group(row, col)
        liberties = board.get_liberties(group)
        
        # 找眼
        eyes = LifeDeath.get_eyes(board, stone)
        eye_count = sum(1 for eye in eyes if any((r, c) in liberties for r, c in eye))
        
        is_alive = LifeDeath.is_alive(board, group, stone)
        is_dead = LifeDeath.is_dead(board, group, stone)
        
        if is_alive:
            status = 'alive'
        elif is_dead:
            status = 'dead'
        else:
            status = 'uncertain'
        
        return {
            'size': len(group),
            'liberties': len(liberties),
            'eyes': eye_count,
            'is_alive': is_alive,
            'status': status
        }


class SGF:
    """SGF (Smart Game Format) 格式支持"""
    
    @staticmethod
    def export(board: GoBoard, 
               black_name: str = "Black",
               white_name: str = "White",
               result: str = "",
               date: str = "") -> str:
        """
        导出棋局为 SGF 格式
        """
        lines = [
            "(;",
            f"GM[1]",  # 游戏: 围棋
            f"FF[4]",  # SGF 格式版本
            f"SZ[{board.size}]",
            f"PW[{white_name}]",
            f"PB[{black_name}]",
        ]
        
        if result:
            lines.append(f"RE[{result}]")
        if date:
            lines.append(f"DT[{date}]")
        
        # 添加落子记录
        for move in board.history:
            if move.row < 0:  # 虚手
                lines.append(f"{move.stone.to_sgf()}[]")
            else:
                sgf_coord = move.to_sgf()
                lines.append(f"{move.stone.to_sgf()}[{sgf_coord}]")
        
        lines.append(")")
        return "\n".join(lines)
    
    @staticmethod
    def parse(sgf_content: str) -> GoBoard:
        """
        解析 SGF 格式内容
        """
        # 提取棋盘大小
        size_match = re.search(r'SZ\[(\d+)\]', sgf_content)
        size = int(size_match.group(1)) if size_match else 19
        
        board = GoBoard(size)
        
        # 提取落子记录
        move_pattern = re.compile(r'([BW])\[([a-z]{0,2})\]')
        
        for match in move_pattern.finditer(sgf_content):
            color = Stone.BLACK if match.group(1) == 'B' else Stone.WHITE
            coord = match.group(2)
            
            if not coord:  # 虚手
                board.pass_turn()
            else:
                move = Move.from_sgf(coord, color)
                board.play(move.row, move.col, color)
        
        return board


class ScoreCalculator:
    """计分器"""
    
    @staticmethod
    def calculate_chinese_score(board: GoBoard, komi: float = 7.5) -> Dict:
        """
        中国规则计分
        
        计算公式：棋子数 + 领地
        """
        territory = Territory.calculate(board)
        
        black_stones = 0
        white_stones = 0
        
        for row in range(board.size):
            for col in range(board.size):
                stone = board.get(row, col)
                if stone == Stone.BLACK:
                    black_stones += 1
                elif stone == Stone.WHITE:
                    white_stones += 1
        
        black_score = black_stones + territory[Stone.BLACK]
        white_score = white_stones + territory[Stone.WHITE] + komi
        
        return {
            'black': {
                'stones': black_stones,
                'territory': territory[Stone.BLACK],
                'total': black_score
            },
            'white': {
                'stones': white_stones,
                'territory': territory[Stone.WHITE],
                'total': white_score
            },
            'komi': komi,
            'winner': 'black' if black_score > white_score else 'white',
            'margin': abs(black_score - white_score)
        }
    
    @staticmethod
    def calculate_japanese_score(board: GoBoard, komi: float = 6.5) -> Dict:
        """
        日本规则计分
        
        计算公式：领地 + 提子
        """
        territory = Territory.calculate(board)
        
        black_score = territory[Stone.BLACK] + board.captured[Stone.BLACK]
        white_score = territory[Stone.WHITE] + board.captured[Stone.WHITE] + komi
        
        return {
            'black': {
                'territory': territory[Stone.BLACK],
                'captures': board.captured[Stone.BLACK],
                'total': black_score
            },
            'white': {
                'territory': territory[Stone.WHITE],
                'captures': board.captured[Stone.WHITE],
                'total': white_score
            },
            'komi': komi,
            'winner': 'black' if black_score > white_score else 'white',
            'margin': abs(black_score - white_score)
        }


class Pattern:
    """棋形识别"""
    
    @staticmethod
    def is_atari(board: GoBoard, row: int, col: int) -> bool:
        """检查是否处于打吃状态（只剩一气）"""
        stone = board.get(row, col)
        if stone == Stone.EMPTY:
            return False
        return board.count_liberties(row, col) == 1
    
    @staticmethod
    def find_atari_groups(board: GoBoard, stone: Stone) -> List[Set[Tuple[int, int]]]:
        """找出处于打吃状态的所有棋子组"""
        atari_groups = []
        visited = set()
        
        for row in range(board.size):
            for col in range(board.size):
                if (row, col) in visited:
                    continue
                if board.get(row, col) != stone:
                    continue
                
                group = board.get_group(row, col)
                visited.update(group)
                
                if board.count_liberties(row, col) == 1:
                    atari_groups.append(group)
        
        return atari_groups
    
    @staticmethod
    def is_eye_point(board: GoBoard, row: int, col: int, stone: Stone) -> bool:
        """
        检查是否可能成为眼位
        
        简化判断：周围都是同色棋子或边角
        """
        if board.get(row, col) != Stone.EMPTY:
            return False
        
        neighbors = board.get_neighbors(row, col)
        
        for nr, nc in neighbors:
            neighbor_stone = board.get(nr, nc)
            if neighbor_stone != stone and neighbor_stone != Stone.EMPTY:
                return False
        
        # 检查对角线（斜向）
        diagonals = []
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nr, nc = row + dr, col + dc
            if board.is_valid_position(nr, nc):
                diagonals.append((nr, nc))
        
        # 如果在边角，对角线有更多要求
        if len(neighbors) < 4:  # 边或角
            same_color_diags = sum(1 for r, c in diagonals if board.get(r, c) == stone)
            return same_color_diags >= len(diagonals) - 1
        
        # 中央需要更多对角线是同色
        same_color_diags = sum(1 for r, c in diagonals if board.get(r, c) == stone)
        return same_color_diags >= 3
    
    @staticmethod
    def find_ko_threats(board: GoBoard) -> List[Tuple[int, int]]:
        """
        找出可能的劫材点
        
        劫材：威胁对方必须应的地方
        """
        threats = []
        opponent = board.current_player.opponent()
        
        for row in range(board.size):
            for col in range(board.size):
                if board.get(row, col) != Stone.EMPTY:
                    continue
                
                # 检查是否能威胁对方的棋子组
                for nr, nc in board.get_neighbors(row, col):
                    if board.get(nr, nc) == opponent:
                        group = board.get_group(nr, nc)
                        if len(group) <= 3 and board.count_liberties(nr, nc) == 2:
                            threats.append((row, col))
                            break
        
        return list(set(threats))


class Handicap:
    """让子设置"""
    
    # 标准让子位置（19路棋盘）
    HANDICAP_19 = {
        2: [(3, 15), (15, 3)],
        3: [(3, 15), (15, 3), (15, 15)],
        4: [(3, 3), (3, 15), (15, 3), (15, 15)],
        5: [(3, 3), (3, 15), (15, 3), (15, 15), (9, 9)],
        6: [(3, 3), (3, 15), (15, 3), (15, 15), (3, 9), (15, 9)],
        7: [(3, 3), (3, 15), (15, 3), (15, 15), (3, 9), (15, 9), (9, 9)],
        8: [(3, 3), (3, 15), (15, 3), (15, 15), (3, 9), (15, 9), (9, 3), (9, 15)],
        9: [(3, 3), (3, 15), (15, 3), (15, 15), (3, 9), (15, 9), (9, 3), (9, 15), (9, 9)],
    }
    
    @staticmethod
    def setup_handicap(board: GoBoard, handicap: int) -> bool:
        """
        设置让子
        
        Args:
            board: 棋盘
            handicap: 让子数（2-9）
        
        Returns:
            是否成功
        """
        if board.size != 19:
            return False
        
        if handicap < 2 or handicap > 9:
            return False
        
        positions = Handicap.HANDICAP_19.get(handicap, [])
        if not positions:
            return False
        
        for row, col in positions:
            board.set(row, col, Stone.BLACK)
        
        # 让子后白方先行
        board.current_player = Stone.WHITE
        
        return True


# 便捷函数
def create_board(size: int = 19) -> GoBoard:
    """创建棋盘"""
    return GoBoard(size)


def quick_play(board: GoBoard, moves: List[Tuple[int, int, str]]) -> GoBoard:
    """
    快速落子
    
    Args:
        board: 棋盘
        moves: 落子列表 [(row, col, 'B'/'W'), ...]
    
    Returns:
        落子后的棋盘副本
    """
    new_board = board.copy()
    for row, col, color in moves:
        stone = Stone.BLACK if color.upper() == 'B' else Stone.WHITE
        new_board.play(row, col, stone)
    return new_board


def coord_to_sgf(row: int, col: int) -> str:
    """坐标转 SGF 格式"""
    return chr(ord('a') + col) + chr(ord('a') + row)


def sgf_to_coord(sgf: str) -> Tuple[int, int]:
    """SGF 格式转坐标"""
    if len(sgf) != 2:
        raise ValueError(f"无效的 SGF 坐标: {sgf}")
    return (ord(sgf[1]) - ord('a'), ord(sgf[0]) - ord('a'))


def coord_to_label(row: int, col: int) -> str:
    """坐标转棋盘标记（如 A1, B2 等，跳过 I）"""
    col_label = chr(ord('A') + col) if col < 8 else chr(ord('A') + col + 1)
    return f"{col_label}{row + 1}"


def label_to_coord(label: str) -> Tuple[int, int]:
    """棋盘标记转坐标"""
    if len(label) < 2:
        raise ValueError(f"无效的坐标标记: {label}")
    
    col_char = label[0].upper()
    col = ord(col_char) - ord('A')
    if col > 7:  # 跳过 I
        col -= 1
    
    row = int(label[1:]) - 1
    return (row, col)


if __name__ == "__main__":
    # 简单测试
    board = GoBoard(19)
    print("=== 围棋工具测试 ===\n")
    print(board)
    print()
    
    # 落子测试
    board.play(3, 3)  # 黑方星位
    board.play(15, 15)  # 白方星位
    board.play(3, 15)  # 黑方星位
    board.play(15, 3)  # 白方星位
    
    print("=== 落子后 ===\n")
    print(board)
    
    print("\n=== 计分测试 ===")
    score = ScoreCalculator.calculate_chinese_score(board)
    print(f"黑方: {score['black']['total']} 目")
    print(f"白方: {score['white']['total']} 目 (含贴目 {score['komi']})")