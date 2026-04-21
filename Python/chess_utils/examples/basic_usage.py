"""
国际象棋工具模块使用示例

展示各种常见用法的示例代码
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Board, Square, Move, Piece, PieceType, Color, Game, PGN,
    create_board, create_game, san_to_uci, uci_to_move
)


def example_basic_board():
    """示例1：基本棋盘操作"""
    print("=" * 50)
    print("示例1：基本棋盘操作")
    print("=" * 50)
    
    # 创建初始局面
    board = Board.starting_position()
    print("\n初始局面：")
    print(board)
    print(f"\nFEN: {board.to_fen()}")
    
    # 从 FEN 创建局面
    fen = "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4"
    board = Board.from_fen(fen)
    print("\n意大利开局：")
    print(board)
    
    # 查找棋子
    white_knights = board.find_pieces(PieceType.KNIGHT, Color.WHITE)
    print(f"\n白方骑士位置: {[str(sq) for sq in white_knights]}")
    
    # 检查将军状态
    print(f"白方是否被将军: {board.is_in_check(Color.WHITE)}")
    print(f"黑方是否被将军: {board.is_in_check(Color.BLACK)}")


def example_legal_moves():
    """示例2：获取合法走法"""
    print("\n" + "=" * 50)
    print("示例2：获取合法走法")
    print("=" * 50)
    
    board = Board.starting_position()
    
    # 获取所有合法走法
    legal_moves = list(board.generate_legal_moves())
    print(f"\n初始局面合法走法数量: {len(legal_moves)}")
    
    # 打印前10个走法
    print("\n前10个合法走法：")
    for i, move in enumerate(legal_moves[:10]):
        san = move.to_san(board)
        uci = move.to_uci()
        print(f"  {i+1}. {san} ({uci})")
    
    # 特定位置的走法
    e2_pawn = Square.from_algebraic("e2")
    pawn_moves = [m for m in legal_moves if m.from_sq == e2_pawn]
    print(f"\ne2兵的走法: {[m.to_uci() for m in pawn_moves]}")


def example_make_moves():
    """示例3：执行走法"""
    print("\n" + "=" * 50)
    print("示例3：执行走法")
    print("=" * 50)
    
    game = create_game()
    
    print("\n开局状态：")
    print(game.board)
    
    # 执行走法
    moves_uci = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"]
    
    for uci in moves_uci:
        move = Move.from_uci(uci)
        san = move.to_san(game.board)
        game.make_move(move)
        print(f"\n执行 {san} ({uci})")
    
    print("\n西班牙开局：")
    print(game.board)
    print(f"\nFEN: {game.board.to_fen()}")


def example_castling():
    """示例4：王车易位"""
    print("\n" + "=" * 50)
    print("示例4：王车易位")
    print("=" * 50)
    
    # 设置一个可以易位的局面
    fen = "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1"
    board = Board.from_fen(fen)
    
    print("\n可以易位的局面：")
    print(board)
    
    # 查找易位走法
    legal_moves = list(board.generate_legal_moves())
    castle_moves = [m for m in legal_moves if m.is_castling]
    
    print(f"\n易位走法: {[m.to_san(board) for m in castle_moves]}")
    
    # 执行王翼易位
    kingside = [m for m in castle_moves if m.to_sq.file == 6][0]
    print(f"\n执行王翼易位: {kingside.to_san(board)}")
    
    new_board = board.make_move(kingside)
    print(new_board)
    
    # 验证王和车的位置
    print(f"\n王的位置: {new_board.find_king(Color.WHITE)}")
    print(f"f1位置棋子: {new_board.get_piece(Square.from_algebraic('f1'))}")


def example_en_passant():
    """示例5：吃过路兵"""
    print("\n" + "=" * 50)
    print("示例5：吃过路兵")
    print("=" * 50)
    
    # 设置过路兵局面
    fen = "rnbqkbnr/ppp1pppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3"
    board = Board.from_fen(fen)
    
    print("\n过路兵局面：")
    print(board)
    print(f"\n过路兵目标: {board.en_passant_target}")
    
    # 找到过路兵走法
    legal_moves = list(board.generate_legal_moves())
    en_passant_moves = [m for m in legal_moves if m.is_en_passant]
    
    print(f"\n过路兵走法: {[m.to_uci() for m in en_passant_moves]}")
    
    # 执行吃子
    if en_passant_moves:
        move = en_passant_moves[0]
        new_board = board.make_move(move)
        print(f"\n执行过路兵: {move.to_uci()}")
        print(new_board)


def example_promotion():
    """示例6：兵升变"""
    print("\n" + "=" * 50)
    print("示例6：兵升变")
    print("=" * 50)
    
    # 白兵即将升变
    fen = "8/P7/8/8/8/8/8/k1K5 w - - 0 1"
    board = Board.from_fen(fen)
    
    print("\n兵即将升变：")
    print(board)
    
    # 获取升变走法
    legal_moves = list(board.generate_legal_moves())
    promotion_moves = [m for m in legal_moves if m.promotion]
    
    print(f"\n升变选择: {[(m.to_uci(), m.promotion.value.upper()) for m in promotion_moves]}")
    
    # 执行升变为皇后
    queen_promo = [m for m in promotion_moves if m.promotion == PieceType.QUEEN][0]
    new_board = board.make_move(queen_promo)
    print(f"\n升变为皇后：")
    print(new_board)


def example_checkmate():
    """示例7：将死检测"""
    print("\n" + "=" * 50)
    print("示例7：将死检测（学者将死）")
    print("=" * 50)
    
    game = create_game()
    
    # 学者将死走法序列
    moves = [
        ("e2e4", "e4"),      # 1. e4
        ("e7e5", "e5"),      # 1... e5
        ("d1h5", "Qh5"),     # 2. Qh5
        ("b8c6", "Nc6"),     # 2... Nc6
        ("f1c4", "Bc4"),     # 3. Bc4
        ("g8f6", "Nf6"),     # 3... Nf6??
        ("h5f7", "Qxf7#"),   # 4. Qxf7#
    ]
    
    print("\n学者将死对局：")
    
    for uci, san in moves:
        move = Move.from_uci(uci)
        actual_san = move.to_san(game.board)
        game.make_move(move)
        print(f"  {actual_san}")
        
        if game.board.is_checkmate():
            print(f"\n{'='*30}")
            print("将死！")
            print(f"{'='*30}")
            print(game.board)
            print(f"\n结果: {game.get_result()}")
            break


def example_pgn_export():
    """示例8：导出 PGN"""
    print("\n" + "=" * 50)
    print("示例8：导出 PGN")
    print("=" * 50)
    
    game = create_game()
    
    # 意大利开局
    moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f8c5"]
    
    for uci in moves:
        move = Move.from_uci(uci)
        game.make_move(move)
    
    # 导出 PGN
    pgn = PGN.export(
        game,
        event="意大利开局示例",
        site="在线对弈",
        date="2026.04.21",
        round_num="1",
        white="Player A",
        black="Player B",
        result="*"
    )
    
    print("\nPGN 输出：")
    print(pgn)


def example_position_analysis():
    """示例9：局面分析"""
    print("\n" + "=" * 50)
    print("示例9：局面分析")
    print("=" * 50)
    
    # 西西里防御开局
    fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
    board = Board.from_fen(fen)
    
    print("\n西西里防御：")
    print(board)
    
    # 分析局面
    print(f"\n当前行动方: {'白方' if board.turn == Color.WHITE else '黑方'}")
    print(f"合法走法数量: {len(list(board.generate_legal_moves()))}")
    print(f"王车易位权: 白方({board.castling_rights[Color.WHITE]}), 黑方({board.castling_rights[Color.BLACK]})")
    print(f"过路兵目标: {board.en_passant_target}")
    
    # 统计棋子
    piece_count = {Color.WHITE: {}, Color.BLACK: {}}
    for rank in range(8):
        for file in range(8):
            piece = board.get_piece(Square(file, rank))
            if piece:
                ptype = piece.type.value
                piece_count[piece.color][ptype] = piece_count[piece.color].get(ptype, 0) + 1
    
    print(f"\n白方棋子: {piece_count[Color.WHITE]}")
    print(f"黑方棋子: {piece_count[Color.BLACK]}")
    
    # 检测攻击
    e4 = Square.from_algebraic("e4")
    print(f"\ne4格是否被黑方攻击: {board.is_square_attacked(e4, Color.BLACK)}")
    
    c5 = Square.from_algebraic("c5")
    print(f"c5格是否被白方攻击: {board.is_square_attacked(c5, Color.WHITE)}")


def example_game_state():
    """示例10：游戏状态管理"""
    print("\n" + "=" * 50)
    print("示例10：游戏状态管理")
    print("=" * 50)
    
    game = create_game()
    
    # 执行一些走法
    moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"]
    
    print("\n执行走法：")
    for uci in moves:
        move = Move.from_uci(uci)
        san = move.to_san(game.board)
        game.make_move(move)
        print(f"  {san}")
    
    print(f"\n当前 FEN: {game.board.to_fen()}")
    print(f"半回合数: {game.board.halfmove_clock}")
    print(f"回合数: {game.board.fullmove_number}")
    
    # 撤销走法
    print("\n撤销最后一步：")
    game.undo_move()
    print(game.board)
    
    print(f"\n撤销后 FEN: {game.board.to_fen()}")


def run_all_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("国际象棋工具模块 - 使用示例")
    print("=" * 60)
    
    example_basic_board()
    example_legal_moves()
    example_make_moves()
    example_castling()
    example_en_passant()
    example_promotion()
    example_checkmate()
    example_pgn_export()
    example_position_analysis()
    example_game_state()
    
    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()