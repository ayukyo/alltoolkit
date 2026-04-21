"""
chess_utils 测试文件

测试国际象棋工具模块的所有核心功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Board, Square, Move, Piece, PieceType, Color, Game, PGN,
    create_board, create_game, san_to_uci, uci_to_move
)


def test_square():
    """测试棋盘位置"""
    print("测试 Square...")
    
    # 代数记号转换
    sq = Square.from_algebraic("e4")
    assert sq.file == 4
    assert sq.rank == 3
    assert sq.to_algebraic() == "e4"
    
    sq = Square.from_algebraic("a1")
    assert sq.file == 0
    assert sq.rank == 0
    
    sq = Square.from_algebraic("h8")
    assert sq.file == 7
    assert sq.rank == 7
    
    # 偏移
    sq = Square(4, 3)  # e4
    assert sq.offset(1, 1) == Square(5, 4)  # f5
    assert sq.offset(-1, -1) == Square(3, 2)  # d3
    assert sq.offset(10, 0) is None  # 越界
    
    print("  ✓ Square 测试通过")


def test_piece():
    """测试棋子"""
    print("测试 Piece...")
    
    # 从符号创建
    p = Piece.from_symbol('P')
    assert p.type == PieceType.PAWN
    assert p.color == Color.WHITE
    
    p = Piece.from_symbol('k')
    assert p.type == PieceType.KING
    assert p.color == Color.BLACK
    
    # 转换为符号
    assert Piece(PieceType.QUEEN, Color.WHITE).to_symbol() == 'Q'
    assert Piece(PieceType.ROOK, Color.BLACK).to_symbol() == 'r'
    
    print("  ✓ Piece 测试通过")


def test_move():
    """测试走法"""
    print("测试 Move...")
    
    # UCI 格式
    move = Move.from_uci("e2e4")
    assert move.from_sq.to_algebraic() == "e2"
    assert move.to_sq.to_algebraic() == "e4"
    
    # 带升变
    move = Move.from_uci("e7e8q")
    assert move.promotion == PieceType.QUEEN
    
    # 输出 UCI
    move = Move(Square.from_algebraic("e2"), Square.from_algebraic("e4"))
    assert move.to_uci() == "e2e4"
    
    print("  ✓ Move 测试通过")


def test_board_initial():
    """测试初始局面"""
    print("测试初始局面...")
    
    board = Board.starting_position()
    
    # 检查 FEN
    expected_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    assert board.to_fen() == expected_fen
    
    # 检查棋子位置
    assert board.get_piece(Square.from_algebraic("a1")).type == PieceType.ROOK
    assert board.get_piece(Square.from_algebraic("a1")).color == Color.WHITE
    assert board.get_piece(Square.from_algebraic("e1")).type == PieceType.KING
    assert board.get_piece(Square.from_algebraic("e8")).type == PieceType.KING
    assert board.get_piece(Square.from_algebraic("d8")).type == PieceType.QUEEN
    
    # 检查空格
    assert board.get_piece(Square.from_algebraic("e4")) is None
    
    # 检查行动方
    assert board.turn == Color.WHITE
    
    print("  ✓ 初始局面测试通过")


def test_board_fen():
    """测试 FEN 解析"""
    print("测试 FEN 解析...")
    
    # 意大利开局后
    fen = "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3"
    board = Board.from_fen(fen)
    
    assert board.turn == Color.BLACK
    assert board.get_piece(Square.from_algebraic("c4")).type == PieceType.BISHOP
    assert board.get_piece(Square.from_algebraic("f3")).type == PieceType.KNIGHT
    
    # 重新生成 FEN
    assert board.to_fen() == fen
    
    print("  ✓ FEN 解析测试通过")


def test_pseudo_legal_moves():
    """测试伪合法走法生成"""
    print("测试伪合法走法生成...")
    
    board = Board.starting_position()
    
    # 初始局面白方有 20 个合法走法
    legal_moves = list(board.generate_legal_moves())
    assert len(legal_moves) == 20
    
    # 检查一些特定走法
    uci_moves = [m.to_uci() for m in legal_moves]
    assert "e2e4" in uci_moves
    assert "d2d4" in uci_moves
    assert "g1f3" in uci_moves
    
    print("  ✓ 伪合法走法测试通过")


def test_make_move():
    """测试执行走法"""
    print("测试执行走法...")
    
    board = Board.starting_position()
    
    # 执行 e4
    move = Move.from_uci("e2e4")
    new_board = board.make_move(move)
    
    assert new_board.get_piece(Square.from_algebraic("e4")).type == PieceType.PAWN
    assert new_board.get_piece(Square.from_algebraic("e2")) is None
    assert new_board.turn == Color.BLACK
    assert new_board.en_passant_target.to_algebraic() == "e3"
    
    print("  ✓ 执行走法测试通过")


def test_castling():
    """测试王车易位"""
    print("测试王车易位...")
    
    # 白方王翼易位局面
    fen = "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1"
    board = Board.from_fen(fen)
    
    # 检查易位权
    assert board.castling_rights[Color.WHITE]['K'] == True
    assert board.castling_rights[Color.WHITE]['Q'] == True
    
    # 执行王翼易位
    legal_moves = list(board.generate_legal_moves())
    castle_moves = [m for m in legal_moves if m.is_castling]
    assert len(castle_moves) >= 2  # 王翼和后翼
    
    # 执行王翼易位
    kingside = [m for m in castle_moves if m.to_sq.file == 6][0]
    new_board = board.make_move(kingside)
    
    # 检查王和车的位置
    assert new_board.get_piece(Square.from_algebraic("g1")).type == PieceType.KING
    assert new_board.get_piece(Square.from_algebraic("f1")).type == PieceType.ROOK
    
    print("  ✓ 王车易位测试通过")


def test_en_passant():
    """测试吃过路兵"""
    print("测试吃过路兵...")
    
    # 设置过路兵局面
    fen = "rnbqkbnr/ppp1pppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3"
    board = Board.from_fen(fen)
    
    # 检查过路兵目标
    assert board.en_passant_target.to_algebraic() == "d6"
    
    # 执行吃子
    legal_moves = list(board.generate_legal_moves())
    en_passant_moves = [m for m in legal_moves if m.is_en_passant]
    assert len(en_passant_moves) == 1
    
    move = en_passant_moves[0]
    assert move.to_uci() == "e5d6"
    
    new_board = board.make_move(move)
    # 检查被吃的兵
    assert new_board.get_piece(Square.from_algebraic("d5")) is None
    
    print("  ✓ 吃过路兵测试通过")


def test_promotion():
    """测试兵升变"""
    print("测试兵升变...")
    
    # 白兵即将升变
    fen = "8/P7/8/8/8/8/8/4K2k w - - 0 1"
    board = Board.from_fen(fen)
    
    legal_moves = list(board.generate_legal_moves())
    promotion_moves = [m for m in legal_moves if m.promotion]
    
    # 应该有4种升变选择
    assert len(promotion_moves) == 4
    promotions = {m.promotion for m in promotion_moves}
    assert PieceType.QUEEN in promotions
    assert PieceType.ROOK in promotions
    assert PieceType.BISHOP in promotions
    assert PieceType.KNIGHT in promotions
    
    # 执行升变
    queen_promo = [m for m in promotion_moves if m.promotion == PieceType.QUEEN][0]
    new_board = board.make_move(queen_promo)
    assert new_board.get_piece(Square.from_algebraic("a8")).type == PieceType.QUEEN
    
    print("  ✓ 兵升变测试通过")


def test_check_detection():
    """测试将军检测"""
    print("测试将军检测...")
    
    # 被将军的局面
    fen = "rnb1kbnr/pppp1ppp/4p3/8/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
    board = Board.from_fen(fen)
    
    assert board.is_in_check(Color.WHITE)
    
    # 不被将军的局面
    board2 = Board.starting_position()
    assert not board2.is_in_check(Color.WHITE)
    assert not board2.is_in_check(Color.BLACK)
    
    print("  ✓ 将军检测测试通过")


def test_checkmate():
    """测试将死检测"""
    print("测试将死检测...")
    
    # 学者将死
    fen = "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4"
    board = Board.from_fen(fen)
    
    # 执行 Qxf7#
    move = Move.from_uci("h5f7")
    new_board = board.make_move(move)
    
    assert new_board.is_checkmate()
    
    print("  ✓ 将死检测测试通过")


def test_stalemate():
    """测试逼和检测"""
    print("测试逼和检测...")
    
    # 逼和局面
    fen = "k7/8/1K6/8/8/8/8/8 w - - 0 1"
    board = Board.from_fen(fen)
    
    # 移动王到逼和位置
    stalemate_fen = "k7/8/2K5/8/8/8/8/8 w - - 0 1"
    board = Board.from_fen(stalemate_fen)
    
    # 这不是逼和（白方可以移动）
    # 让我们用一个更明确的逼和局面
    stalemate_fen2 = "k7/2K5/8/8/8/8/8/8 w - - 0 1"
    board2 = Board.from_fen(stalemate_fen2)
    
    # 黑方被逼和（无法移动且未被将军）
    board3 = Board.from_fen("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1")
    assert board3.is_stalemate()
    
    print("  ✓ 逼和检测测试通过")


def test_game():
    """测试游戏状态管理"""
    print("测试游戏状态管理...")
    
    game = create_game()
    
    # 执行走法
    assert game.make_move(Move.from_uci("e2e4"))
    assert game.make_move(Move.from_uci("e7e5"))
    assert game.make_move(Move.from_uci("g1f3"))
    
    # 检查历史
    assert len(game.move_history) == 3
    
    # 撤销
    game.undo_move()
    assert len(game.move_history) == 2
    
    print("  ✓ 游戏状态管理测试通过")


def test_san_conversion():
    """测试 SAN 转换"""
    print("测试 SAN 转换...")
    
    board = Board.starting_position()
    
    # SAN 转 UCI
    uci = san_to_uci(board, "e4")
    assert uci == "e2e4"
    
    uci = san_to_uci(board, "Nf3")
    assert uci == "g1f3"
    
    # UCI 转 Move
    move = uci_to_move(board, "e2e4")
    assert move is not None
    assert move.to_uci() == "e2e4"
    
    print("  ✓ SAN 转换测试通过")


def test_pgn_export():
    """测试 PGN 导出"""
    print("测试 PGN 导出...")
    
    game = create_game()
    game.make_move(Move.from_uci("e2e4"))
    game.make_move(Move.from_uci("e7e5"))
    game.make_move(Move.from_uci("g1f3"))
    game.make_move(Move.from_uci("b8c6"))
    
    pgn = PGN.export(game, white="Player1", black="Player2", result="*")
    
    assert '[White "Player1"]' in pgn
    assert '[Black "Player2"]' in pgn
    assert "1. e4 e5" in pgn
    assert "2. Nf3 Nc6" in pgn
    
    print("  ✓ PGN 导出测试通过")


def test_special_positions():
    """测试特殊局面"""
    print("测试特殊局面...")
    
    # 测试材料不足和棋
    fen = "k7/8/1K6/8/8/8/8/8 w - - 0 1"
    board = Board.from_fen(fen)
    assert board._is_insufficient_material()
    
    # 测试复杂局面
    fen = "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4"
    board = Board.from_fen(fen)
    legal_moves = list(board.generate_legal_moves())
    assert len(legal_moves) > 0
    
    print("  ✓ 特殊局面测试通过")


def test_full_game():
    """测试完整对局（学者将死）"""
    print("测试完整对局...")
    
    game = create_game()
    
    # 学者将死
    moves = ["e2e4", "e7e5", "d1h5", "b8c6", "f1c4", "g8f6", "h5f7"]
    
    for uci in moves:
        move = Move.from_uci(uci)
        success = game.make_move(move)
        assert success, f"走法 {uci} 执行失败"
        
        result = game.get_result()
        if result:
            break
    
    # 检查将死
    assert game.board.is_checkmate()
    assert "Checkmate" in game.get_result()
    
    print("  ✓ 完整对局测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("国际象棋工具模块测试")
    print("=" * 50)
    print()
    
    test_square()
    test_piece()
    test_move()
    test_board_initial()
    test_board_fen()
    test_pseudo_legal_moves()
    test_make_move()
    test_castling()
    test_en_passant()
    test_promotion()
    test_check_detection()
    test_checkmate()
    test_stalemate()
    test_game()
    test_san_conversion()
    test_pgn_export()
    test_special_positions()
    test_full_game()
    
    print()
    print("=" * 50)
    print("✅ 所有测试通过！")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()