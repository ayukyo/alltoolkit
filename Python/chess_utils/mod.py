"""
chess_utils - 国际象棋工具模块

功能：
- FEN 字符串解析与生成
- 棋盘表示与操作
- 走法生成与验证
- 特殊走法处理（王车易位、吃过路兵、兵升变）
- 棋局状态检测（将军、将死、和棋）
- PGN 格式支持

零外部依赖，纯 Python 实现
"""

from typing import Optional, List, Tuple, Dict, Set, Iterator
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy


class PieceType(Enum):
    """棋子类型"""
    PAWN = 'p'
    KNIGHT = 'n'
    BISHOP = 'b'
    ROOK = 'r'
    QUEEN = 'q'
    KING = 'k'


class Color(Enum):
    """棋子颜色"""
    WHITE = 'w'
    BLACK = 'b'
    
    def opposite(self) -> 'Color':
        return Color.BLACK if self == Color.WHITE else Color.WHITE


@dataclass
class Piece:
    """棋子"""
    type: PieceType
    color: Color
    
    def __repr__(self) -> str:
        symbol = self.type.value
        return symbol.upper() if self.color == Color.WHITE else symbol
    
    @classmethod
    def from_symbol(cls, symbol: str) -> Optional['Piece']:
        """从符号创建棋子"""
        if symbol == ' ' or symbol.isalpha() == False:
            return None
        
        color = Color.WHITE if symbol.isupper() else Color.BLACK
        piece_type = PieceType(symbol.lower())
        return cls(piece_type, color)
    
    def to_symbol(self) -> str:
        """转换为符号"""
        symbol = self.type.value
        return symbol.upper() if self.color == Color.WHITE else symbol


class Square:
    """棋盘位置（0-7, 0-7 对应 a1-h8）"""
    
    def __init__(self, file: int, rank: int):
        if not (0 <= file <= 7 and 0 <= rank <= 7):
            raise ValueError(f"Invalid square: file={file}, rank={rank}")
        self.file = file  # 列 0-7 (a-h)
        self.rank = rank  # 行 0-7 (1-8)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Square):
            return False
        return self.file == other.file and self.rank == other.rank
    
    def __hash__(self) -> int:
        return hash((self.file, self.rank))
    
    def __repr__(self) -> str:
        return self.to_algebraic()
    
    def to_algebraic(self) -> str:
        """转换为代数记号 (e.g., 'e4')"""
        return chr(ord('a') + self.file) + str(self.rank + 1)
    
    @classmethod
    def from_algebraic(cls, notation: str) -> 'Square':
        """从代数记号创建"""
        if len(notation) != 2:
            raise ValueError(f"Invalid algebraic notation: {notation}")
        file = ord(notation[0].lower()) - ord('a')
        rank = int(notation[1]) - 1
        return cls(file, rank)
    
    def offset(self, df: int, dr: int) -> Optional['Square']:
        """偏移位置，返回 None 如果越界"""
        nf, nr = self.file + df, self.rank + dr
        if 0 <= nf <= 7 and 0 <= nr <= 7:
            return Square(nf, nr)
        return None
    
    def is_valid(self) -> bool:
        return 0 <= self.file <= 7 and 0 <= self.rank <= 7


class Move:
    """走法"""
    
    def __init__(self, from_sq: Square, to_sq: Square, 
                 promotion: Optional[PieceType] = None,
                 is_castling: bool = False,
                 is_en_passant: bool = False):
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.promotion = promotion  # 兵升变的目标棋子
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant
        self.captured_piece: Optional[Piece] = None  # 被吃的棋子
    
    def __repr__(self) -> str:
        return self.to_uci()
    
    def to_uci(self) -> str:
        """转换为 UCI 格式 (e.g., 'e2e4' or 'e7e8q')"""
        uci = self.from_sq.to_algebraic() + self.to_sq.to_algebraic()
        if self.promotion:
            uci += self.promotion.value
        return uci
    
    @classmethod
    def from_uci(cls, uci: str) -> 'Move':
        """从 UCI 格式创建"""
        if len(uci) < 4:
            raise ValueError(f"Invalid UCI move: {uci}")
        
        from_sq = Square.from_algebraic(uci[:2])
        to_sq = Square.from_algebraic(uci[2:4])
        promotion = None
        if len(uci) == 5:
            promotion = PieceType(uci[4].lower())
        
        return cls(from_sq, to_sq, promotion)
    
    def to_san(self, board: 'Board') -> str:
        """转换为标准代数记号 (SAN)"""
        piece = board.get_piece(self.from_sq)
        if not piece:
            return ""
        
        # 王车易位
        if self.is_castling:
            return "O-O" if self.to_sq.file > self.from_sq.file else "O-O-O"
        
        san = ""
        
        # 棋子类型（兵不需要）
        if piece.type != PieceType.PAWN:
            san += piece.type.value.upper()
        
        # 歧义消解（多个相同棋子可以移动到同一位置）
        if piece.type != PieceType.PAWN:
            ambiguous_squares = []
            for sq in board.find_pieces(piece.type, piece.color):
                if sq != self.from_sq:
                    for move in board._generate_pseudo_legal_moves_from(sq):
                        if move.to_sq == self.to_sq:
                            ambiguous_squares.append(sq)
                            break
            
            if ambiguous_squares:
                same_file = any(sq.file == self.from_sq.file for sq in ambiguous_squares)
                same_rank = any(sq.rank == self.from_sq.rank for sq in ambiguous_squares)
                
                if not same_file:
                    san += chr(ord('a') + self.from_sq.file)
                elif not same_rank:
                    san += str(self.from_sq.rank + 1)
                else:
                    san += chr(ord('a') + self.from_sq.file) + str(self.from_sq.rank + 1)
        
        # 吃子
        is_capture = self.captured_piece is not None or self.is_en_passant
        if is_capture:
            if piece.type == PieceType.PAWN:
                san += chr(ord('a') + self.from_sq.file)
            san += "x"
        
        # 目标位置
        san += self.to_sq.to_algebraic()
        
        # 升变
        if self.promotion:
            san += "=" + self.promotion.value.upper()
        
        # 将军/将死标记会在外部添加
        return san


class Board:
    """棋盘"""
    
    def __init__(self):
        self.squares: List[List[Optional[Piece]]] = [[None] * 8 for _ in range(8)]
        self.turn: Color = Color.WHITE
        self.castling_rights: Dict[Color, Dict[str, bool]] = {
            Color.WHITE: {'K': True, 'Q': True},
            Color.BLACK: {'K': True, 'Q': True}
        }
        self.en_passant_target: Optional[Square] = None
        self.halfmove_clock: int = 0  # 用于50回合规则
        self.fullmove_number: int = 1
        
        # 内部状态
        self._king_positions: Dict[Color, Optional[Square]] = {
            Color.WHITE: None,
            Color.BLACK: None
        }
    
    def copy(self) -> 'Board':
        """深拷贝棋盘"""
        new_board = Board()
        for rank in range(8):
            for file in range(8):
                piece = self.squares[rank][file]
                new_board.squares[rank][file] = Piece(piece.type, piece.color) if piece else None
        
        new_board.turn = self.turn
        new_board.castling_rights = deepcopy(self.castling_rights)
        new_board.en_passant_target = self.en_passant_target
        new_board.halfmove_clock = self.halfmove_clock
        new_board.fullmove_number = self.fullmove_number
        new_board._king_positions = deepcopy(self._king_positions)
        
        return new_board
    
    @classmethod
    def from_fen(cls, fen: str) -> 'Board':
        """从 FEN 字符串创建棋盘"""
        parts = fen.split()
        if len(parts) < 4:
            raise ValueError(f"Invalid FEN: {fen}")
        
        board = cls()
        
        # 棋子位置
        ranks = parts[0].split('/')
        for rank_idx, rank_data in enumerate(ranks):
            file_idx = 0
            actual_rank = 7 - rank_idx  # FEN 从第8行开始
            
            for char in rank_data:
                if char.isdigit():
                    file_idx += int(char)
                else:
                    piece = Piece.from_symbol(char)
                    if piece:
                        board.squares[actual_rank][file_idx] = piece
                        if piece.type == PieceType.KING:
                            board._king_positions[piece.color] = Square(file_idx, actual_rank)
                    file_idx += 1
        
        # 行动方
        board.turn = Color.WHITE if parts[1] == 'w' else Color.BLACK
        
        # 王车易位权
        castling = parts[2]
        board.castling_rights = {
            Color.WHITE: {'K': 'K' in castling, 'Q': 'Q' in castling},
            Color.BLACK: {'K': 'k' in castling, 'Q': 'q' in castling}
        }
        
        # 过路兵目标
        if parts[3] != '-':
            board.en_passant_target = Square.from_algebraic(parts[3])
        else:
            board.en_passant_target = None
        
        # 半回合数和回合数
        if len(parts) >= 5:
            board.halfmove_clock = int(parts[4])
        if len(parts) >= 6:
            board.fullmove_number = int(parts[5])
        
        return board
    
    def to_fen(self) -> str:
        """转换为 FEN 字符串"""
        # 棋子位置
        fen_rows = []
        for rank in range(7, -1, -1):
            empty = 0
            row = ""
            for file in range(8):
                piece = self.squares[rank][file]
                if piece:
                    if empty > 0:
                        row += str(empty)
                        empty = 0
                    row += piece.to_symbol()
                else:
                    empty += 1
            if empty > 0:
                row += str(empty)
            fen_rows.append(row)
        
        position = '/'.join(fen_rows)
        
        # 行动方
        turn = 'w' if self.turn == Color.WHITE else 'b'
        
        # 王车易位权
        castling = ""
        if self.castling_rights[Color.WHITE]['K']:
            castling += 'K'
        if self.castling_rights[Color.WHITE]['Q']:
            castling += 'Q'
        if self.castling_rights[Color.BLACK]['K']:
            castling += 'k'
        if self.castling_rights[Color.BLACK]['Q']:
            castling += 'q'
        castling = castling if castling else '-'
        
        # 过路兵目标
        en_passant = self.en_passant_target.to_algebraic() if self.en_passant_target else '-'
        
        return f"{position} {turn} {castling} {en_passant} {self.halfmove_clock} {self.fullmove_number}"
    
    @classmethod
    def starting_position(cls) -> 'Board':
        """创建初始局面"""
        return cls.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    
    def get_piece(self, sq: Square) -> Optional[Piece]:
        """获取指定位置的棋子"""
        return self.squares[sq.rank][sq.file]
    
    def set_piece(self, sq: Square, piece: Optional[Piece]) -> None:
        """设置指定位置的棋子"""
        self.squares[sq.rank][sq.file] = piece
        if piece and piece.type == PieceType.KING:
            self._king_positions[piece.color] = sq
    
    def find_pieces(self, piece_type: PieceType, color: Color) -> List[Square]:
        """找到所有指定类型和颜色的棋子"""
        result = []
        for rank in range(8):
            for file in range(8):
                piece = self.squares[rank][file]
                if piece and piece.type == piece_type and piece.color == color:
                    result.append(Square(file, rank))
        return result
    
    def find_king(self, color: Color) -> Optional[Square]:
        """找到指定颜色的王"""
        return self._king_positions.get(color)
    
    def is_square_attacked(self, sq: Square, by_color: Color) -> bool:
        """检查某位置是否被攻击"""
        # 检查骑士攻击
        knight_offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                         (1, -2), (1, 2), (2, -1), (2, 1)]
        for df, dr in knight_offsets:
            attacker_sq = sq.offset(df, dr)
            if attacker_sq:
                piece = self.get_piece(attacker_sq)
                if piece and piece.type == PieceType.KNIGHT and piece.color == by_color:
                    return True
        
        # 检查王攻击
        king_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                        (0, 1), (1, -1), (1, 0), (1, 1)]
        for df, dr in king_offsets:
            attacker_sq = sq.offset(df, dr)
            if attacker_sq:
                piece = self.get_piece(attacker_sq)
                if piece and piece.type == PieceType.KING and piece.color == by_color:
                    return True
        
        # 检查兵攻击
        pawn_dir = -1 if by_color == Color.WHITE else 1
        for df in [-1, 1]:
            attacker_sq = sq.offset(df, pawn_dir)
            if attacker_sq:
                piece = self.get_piece(attacker_sq)
                if piece and piece.type == PieceType.PAWN and piece.color == by_color:
                    return True
        
        # 检查直线攻击（车、后）
        for df, dr in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            curr = sq.offset(df, dr)
            while curr:
                piece = self.get_piece(curr)
                if piece:
                    if piece.color == by_color and piece.type in [PieceType.ROOK, PieceType.QUEEN]:
                        return True
                    break
                curr = curr.offset(df, dr)
        
        # 检查斜线攻击（象、后）
        for df, dr in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            curr = sq.offset(df, dr)
            while curr:
                piece = self.get_piece(curr)
                if piece:
                    if piece.color == by_color and piece.type in [PieceType.BISHOP, PieceType.QUEEN]:
                        return True
                    break
                curr = curr.offset(df, dr)
        
        return False
    
    def is_in_check(self, color: Color) -> bool:
        """检查指定颜色是否被将军"""
        king_sq = self.find_king(color)
        if not king_sq:
            return False
        return self.is_square_attacked(king_sq, color.opposite())
    
    def _generate_pseudo_legal_moves_from(self, from_sq: Square) -> Iterator[Move]:
        """从指定位置生成所有伪合法走法（不考虑是否被将军）"""
        piece = self.get_piece(from_sq)
        if not piece:
            return
        
        if piece.type == PieceType.PAWN:
            yield from self._generate_pawn_moves(from_sq, piece)
        elif piece.type == PieceType.KNIGHT:
            yield from self._generate_knight_moves(from_sq, piece)
        elif piece.type == PieceType.BISHOP:
            yield from self._generate_sliding_moves(from_sq, piece, [(1, 1), (1, -1), (-1, 1), (-1, -1)])
        elif piece.type == PieceType.ROOK:
            yield from self._generate_sliding_moves(from_sq, piece, [(0, 1), (0, -1), (1, 0), (-1, 0)])
        elif piece.type == PieceType.QUEEN:
            yield from self._generate_sliding_moves(from_sq, piece, 
                [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)])
        elif piece.type == PieceType.KING:
            yield from self._generate_king_moves(from_sq, piece)
    
    def _generate_pawn_moves(self, from_sq: Square, piece: Piece) -> Iterator[Move]:
        """生成兵的走法"""
        direction = 1 if piece.color == Color.WHITE else -1
        start_rank = 1 if piece.color == Color.WHITE else 6
        promotion_rank = 7 if piece.color == Color.WHITE else 0
        
        # 前进一格
        to_sq = from_sq.offset(0, direction)
        if to_sq and not self.get_piece(to_sq):
            if to_sq.rank == promotion_rank:
                for promo in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
                    yield Move(from_sq, to_sq, promotion=promo)
            else:
                yield Move(from_sq, to_sq)
            
            # 初始位置前进两格
            if from_sq.rank == start_rank:
                to_sq2 = from_sq.offset(0, 2 * direction)
                if to_sq2 and not self.get_piece(to_sq2):
                    move = Move(from_sq, to_sq2)
                    yield move
        
        # 吃子
        for df in [-1, 1]:
            to_sq = from_sq.offset(df, direction)
            if to_sq:
                target = self.get_piece(to_sq)
                if target and target.color != piece.color:
                    if to_sq.rank == promotion_rank:
                        for promo in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
                            move = Move(from_sq, to_sq, promotion=promo)
                            move.captured_piece = target
                            yield move
                    else:
                        move = Move(from_sq, to_sq)
                        move.captured_piece = target
                        yield move
                
                # 吃过路兵
                if self.en_passant_target and to_sq == self.en_passant_target:
                    move = Move(from_sq, to_sq, is_en_passant=True)
                    captured_sq = to_sq.offset(0, -direction)
                    move.captured_piece = self.get_piece(captured_sq) if captured_sq else None
                    yield move
    
    def _generate_knight_moves(self, from_sq: Square, piece: Piece) -> Iterator[Move]:
        """生成骑士的走法"""
        offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                   (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for df, dr in offsets:
            to_sq = from_sq.offset(df, dr)
            if to_sq:
                target = self.get_piece(to_sq)
                if not target or target.color != piece.color:
                    move = Move(from_sq, to_sq)
                    move.captured_piece = target
                    yield move
    
    def _generate_sliding_moves(self, from_sq: Square, piece: Piece, 
                                 directions: List[Tuple[int, int]]) -> Iterator[Move]:
        """生成滑动棋子（象、车、后）的走法"""
        for df, dr in directions:
            curr = from_sq.offset(df, dr)
            while curr:
                target = self.get_piece(curr)
                if target:
                    if target.color != piece.color:
                        move = Move(from_sq, curr)
                        move.captured_piece = target
                        yield move
                    break
                yield Move(from_sq, curr)
                curr = curr.offset(df, dr)
    
    def _generate_king_moves(self, from_sq: Square, piece: Piece) -> Iterator[Move]:
        """生成王的走法"""
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                   (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for df, dr in offsets:
            to_sq = from_sq.offset(df, dr)
            if to_sq:
                target = self.get_piece(to_sq)
                if not target or target.color != piece.color:
                    move = Move(from_sq, to_sq)
                    move.captured_piece = target
                    yield move
        
        # 王车易位
        if not self.is_in_check(piece.color):
            # 王翼易位
            if self.castling_rights[piece.color]['K']:
                if self._can_castle_kingside(piece.color):
                    yield Move(from_sq, Square(6, from_sq.rank), is_castling=True)
            
            # 后翼易位
            if self.castling_rights[piece.color]['Q']:
                if self._can_castle_queenside(piece.color):
                    yield Move(from_sq, Square(2, from_sq.rank), is_castling=True)
    
    def _can_castle_kingside(self, color: Color) -> bool:
        """检查是否可以进行王翼易位"""
        rank = 0 if color == Color.WHITE else 7
        king_sq = Square(4, rank)
        
        # 检查王和车是否在正确位置
        king = self.get_piece(king_sq)
        rook = self.get_piece(Square(7, rank))
        
        if not king or king.type != PieceType.KING or king.color != color:
            return False
        if not rook or rook.type != PieceType.ROOK or rook.color != color:
            return False
        
        # 检查中间是否有棋子
        if self.get_piece(Square(5, rank)) or self.get_piece(Square(6, rank)):
            return False
        
        # 检查王经过的位置是否被攻击
        enemy = color.opposite()
        if self.is_square_attacked(king_sq, enemy):
            return False
        if self.is_square_attacked(Square(5, rank), enemy):
            return False
        if self.is_square_attacked(Square(6, rank), enemy):
            return False
        
        return True
    
    def _can_castle_queenside(self, color: Color) -> bool:
        """检查是否可以进行后翼易位"""
        rank = 0 if color == Color.WHITE else 7
        king_sq = Square(4, rank)
        
        # 检查王和车是否在正确位置
        king = self.get_piece(king_sq)
        rook = self.get_piece(Square(0, rank))
        
        if not king or king.type != PieceType.KING or king.color != color:
            return False
        if not rook or rook.type != PieceType.ROOK or rook.color != color:
            return False
        
        # 检查中间是否有棋子
        if self.get_piece(Square(1, rank)) or self.get_piece(Square(2, rank)) or self.get_piece(Square(3, rank)):
            return False
        
        # 检查王经过的位置是否被攻击
        enemy = color.opposite()
        if self.is_square_attacked(king_sq, enemy):
            return False
        if self.is_square_attacked(Square(3, rank), enemy):
            return False
        if self.is_square_attacked(Square(2, rank), enemy):
            return False
        
        return True
    
    def generate_legal_moves(self) -> Iterator[Move]:
        """生成所有合法走法"""
        for rank in range(8):
            for file in range(8):
                piece = self.squares[rank][file]
                if piece and piece.color == self.turn:
                    for move in self._generate_pseudo_legal_moves_from(Square(file, rank)):
                        # 检查走法是否会导致自己被将军
                        new_board = self.make_move(move)
                        if not new_board.is_in_check(self.turn):
                            yield move
    
    def make_move(self, move: Move) -> 'Board':
        """执行走法，返回新棋盘"""
        new_board = self.copy()
        piece = new_board.get_piece(move.from_sq)
        
        if not piece:
            return new_board
        
        # 记录被吃的棋子
        move.captured_piece = new_board.get_piece(move.to_sq)
        
        # 移动棋子
        new_board.set_piece(move.from_sq, None)
        
        # 处理兵升变
        if move.promotion:
            new_board.set_piece(move.to_sq, Piece(move.promotion, piece.color))
        else:
            new_board.set_piece(move.to_sq, piece)
        
        # 处理王车易位
        if move.is_castling:
            rank = move.from_sq.rank
            if move.to_sq.file == 6:  # 王翼
                rook = new_board.get_piece(Square(7, rank))
                new_board.set_piece(Square(7, rank), None)
                new_board.set_piece(Square(5, rank), rook)
            else:  # 后翼
                rook = new_board.get_piece(Square(0, rank))
                new_board.set_piece(Square(0, rank), None)
                new_board.set_piece(Square(3, rank), rook)
        
        # 处理吃过路兵
        if move.is_en_passant:
            direction = 1 if piece.color == Color.WHITE else -1
            captured_sq = move.to_sq.offset(0, -direction)
            if captured_sq:
                move.captured_piece = new_board.get_piece(captured_sq)
                new_board.set_piece(captured_sq, None)
        
        # 更新王的位置
        if piece.type == PieceType.KING:
            new_board._king_positions[piece.color] = move.to_sq
        
        # 更新易位权
        if piece.type == PieceType.KING:
            new_board.castling_rights[piece.color]['K'] = False
            new_board.castling_rights[piece.color]['Q'] = False
        
        if piece.type == PieceType.ROOK:
            if move.from_sq.file == 0:
                new_board.castling_rights[piece.color]['Q'] = False
            elif move.from_sq.file == 7:
                new_board.castling_rights[piece.color]['K'] = False
        
        # 更新过路兵目标
        if piece.type == PieceType.PAWN and abs(move.to_sq.rank - move.from_sq.rank) == 2:
            direction = 1 if piece.color == Color.WHITE else -1
            new_board.en_passant_target = move.from_sq.offset(0, direction)
        else:
            new_board.en_passant_target = None
        
        # 更新半回合数
        if piece.type == PieceType.PAWN or move.captured_piece:
            new_board.halfmove_clock = 0
        else:
            new_board.halfmove_clock += 1
        
        # 更新回合数
        if piece.color == Color.BLACK:
            new_board.fullmove_number += 1
        
        # 切换行动方
        new_board.turn = self.turn.opposite()
        
        return new_board
    
    def is_checkmate(self) -> bool:
        """检查是否将死"""
        if not self.is_in_check(self.turn):
            return False
        return not any(self.generate_legal_moves())
    
    def is_stalemate(self) -> bool:
        """检查是否逼和"""
        if self.is_in_check(self.turn):
            return False
        return not any(self.generate_legal_moves())
    
    def is_draw(self) -> bool:
        """检查是否和棋"""
        # 50回合规则
        if self.halfmove_clock >= 100:
            return True
        
        # 逼和
        if self.is_stalemate():
            return True
        
        # 重复局面（简化实现）
        if self._is_insufficient_material():
            return True
        
        return False
    
    def _is_insufficient_material(self) -> bool:
        """检查是否双方棋子不足以将死"""
        pieces = {'w': [], 'b': []}
        for rank in range(8):
            for file in range(8):
                piece = self.squares[rank][file]
                if piece:
                    pieces[piece.color.value].append(piece.type.value)
        
        # 王对王
        if len(pieces['w']) == 1 and len(pieces['b']) == 1:
            return True
        
        # 王对王+象或王+马
        if len(pieces['w']) == 1 and len(pieces['b']) == 2:
            if 'b' in pieces['b'] or 'n' in pieces['b']:
                return True
        if len(pieces['b']) == 1 and len(pieces['w']) == 2:
            if 'b' in pieces['w'] or 'n' in pieces['w']:
                return True
        
        return False
    
    def get_game_result(self) -> Optional[str]:
        """获取游戏结果"""
        if self.is_checkmate():
            winner = "Black" if self.turn == Color.WHITE else "White"
            return f"Checkmate! {winner} wins!"
        if self.is_stalemate():
            return "Stalemate! Draw!"
        if self.halfmove_clock >= 100:
            return "Draw by 50-move rule!"
        if self._is_insufficient_material():
            return "Draw by insufficient material!"
        return None
    
    def __str__(self) -> str:
        """打印棋盘"""
        lines = []
        lines.append("  +-----------------+")
        for rank in range(7, -1, -1):
            row = f"{rank + 1} | "
            for file in range(8):
                piece = self.squares[rank][file]
                row += (piece.to_symbol() if piece else '.') + " "
            row += "|"
            lines.append(row)
        lines.append("  +-----------------+")
        lines.append("    a b c d e f g h")
        return "\n".join(lines)


class Game:
    """游戏状态管理"""
    
    def __init__(self, board: Optional[Board] = None):
        self.board = board or Board.starting_position()
        self.move_history: List[Tuple[Move, Optional[Piece]]] = []  # (move, captured_piece)
        self.position_history: List[str] = [self.board.to_fen()]
    
    def make_move(self, move: Move) -> bool:
        """执行走法"""
        # 验证走法
        legal_moves = list(self.board.generate_legal_moves())
        if move not in legal_moves:
            # 尝试 UCI 匹配
            for m in legal_moves:
                if m.to_uci() == move.to_uci():
                    move = m
                    break
            else:
                return False
        
        # 执行走法
        captured = self.board.get_piece(move.to_sq)
        self.board = self.board.make_move(move)
        self.move_history.append((move, captured))
        self.position_history.append(self.board.to_fen())
        
        return True
    
    def undo_move(self) -> bool:
        """撤销走法"""
        if len(self.move_history) == 0:
            return False
        
        self.move_history.pop()
        self.position_history.pop()
        self.board = Board.from_fen(self.position_history[-1])
        
        return True
    
    def get_result(self) -> Optional[str]:
        """获取游戏结果"""
        return self.board.get_game_result()
    
    def is_game_over(self) -> bool:
        """检查游戏是否结束"""
        return self.get_result() is not None


class PGN:
    """PGN 格式支持"""
    
    @staticmethod
    def export(game: Game, event: str = "?", site: str = "?", 
               date: str = "?", round_num: str = "?",
               white: str = "?", black: str = "?",
               result: str = "*") -> str:
        """导出游戏为 PGN 格式"""
        lines = [
            f'[Event "{event}"]',
            f'[Site "{site}"]',
            f'[Date "{date}"]',
            f'[Round "{round_num}"]',
            f'[White "{white}"]',
            f'[Black "{black}"]',
            f'[Result "{result}"]',
            ""
        ]
        
        # 移动记录
        moves = []
        board = Board.starting_position()
        
        for i, (move, _) in enumerate(game.move_history):
            move_num = (i // 2) + 1
            san = move.to_san(board)
            
            if i % 2 == 0:
                moves.append(f"{move_num}. {san}")
            else:
                moves.append(san)
            
            board = board.make_move(move)
        
        # 添加结果
        moves.append(result)
        
        # 组合移动记录（每行最多80字符）
        moves_text = " ".join(moves)
        lines.append(moves_text)
        
        return "\n".join(lines)


# 便捷函数
def create_board(fen: Optional[str] = None) -> Board:
    """创建棋盘"""
    if fen:
        return Board.from_fen(fen)
    return Board.starting_position()


def create_game(fen: Optional[str] = None) -> Game:
    """创建游戏"""
    if fen:
        return Game(Board.from_fen(fen))
    return Game()


def san_to_uci(board: Board, san: str) -> Optional[str]:
    """将 SAN 转换为 UCI"""
    # 尝试匹配所有合法走法
    for move in board.generate_legal_moves():
        if move.to_san(board) == san:
            return move.to_uci()
    return None


def uci_to_move(board: Board, uci: str) -> Optional[Move]:
    """将 UCI 转换为 Move 对象"""
    try:
        move = Move.from_uci(uci)
        for legal_move in board.generate_legal_moves():
            if legal_move.to_uci() == uci:
                return legal_move
    except:
        pass
    return None


if __name__ == "__main__":
    # 示例用法
    print("=== 国际象棋工具模块 ===\n")
    
    # 创建初始局面
    board = Board.starting_position()
    print("初始局面：")
    print(board)
    print(f"\nFEN: {board.to_fen()}")
    
    # 执行一些走法
    print("\n执行走法：e2e4")
    game = create_game()
    game.make_move(Move.from_uci("e2e4"))
    print(game.board)
    
    print("\n执行走法：e7e5")
    game.make_move(Move.from_uci("e7e5"))
    print(game.board)
    
    # 检查合法走法
    print("\n白方合法走法（前10个）：")
    for i, move in enumerate(game.board.generate_legal_moves()):
        if i >= 10:
            break
        print(f"  {move.to_san(game.board)} ({move.to_uci()})")
    
    # 导出 PGN
    print("\nPGN 导出：")
    print(PGN.export(game, white="Player1", black="Player2", result="*"))