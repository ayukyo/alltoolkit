"""
围棋工具使用示例

演示各种使用场景：
1. 创建棋盘和基本操作
2. 落子和提子
3. 打劫规则
4. 领地计算
5. SGF 格式导入导出
6. 死活分析
7. 计分系统
8. 棋形识别
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    GoBoard, Stone, Move, Territory, LifeDeath,
    SGF, ScoreCalculator, Pattern, Handicap,
    create_board, quick_play, coord_to_sgf, sgf_to_coord,
    coord_to_label, label_to_coord
)


def example_basic_board():
    """示例1: 创建棋盘和基本操作"""
    print("\n=== 示例1: 基本棋盘操作 ===\n")
    
    # 创建19路标准棋盘
    board = GoBoard(19)
    print(f"棋盘大小: {board.size}x{board.size}")
    print(f"当前玩家: {'黑方' if board.current_player == Stone.BLACK else '白方'}")
    
    # 在星位落子
    print("\n在星位落子:")
    board.play(3, 3)  # 黑方左上星位
    print(f"黑方落子: {coord_to_label(3, 3)}")
    
    board.play(15, 15)  # 白方右下星位
    print(f"白方落子: {coord_to_label(15, 15)}")
    
    board.play(3, 15)  # 黑方右上星位
    print(f"黑方落子: {coord_to_label(3, 15)}")
    
    board.play(15, 3)  # 白方左下星位
    print(f"白方落子: {coord_to_label(15, 3)}")
    
    print(f"\n历史记录: {len(board.history)} 步")
    
    # 使用9路棋盘展示完整棋盘
    board9 = GoBoard(9)
    board9.play(4, 4)
    board9.play(3, 4)
    board9.play(5, 4)
    board9.play(4, 3)
    print("\n9路棋盘当前状态:")
    print(board9)


def example_capture():
    """示例2: 提子规则"""
    print("\n=== 示例2: 提子规则 ===\n")
    
    board = GoBoard(9)
    
    # 黑方落子
    board.play(4, 4, Stone.BLACK)
    print(f"黑方在 D5 落子")
    
    # 白方包围
    moves = [
        (3, 4, Stone.WHITE),
        (4, 3, Stone.WHITE),
        (5, 4, Stone.WHITE),
    ]
    for row, col, stone in moves:
        board.set(row, col, stone)
        board.current_player = stone.opponent()
    
    print("\n白方包围黑子（三边）")
    print(f"黑子气数: {board.count_liberties(4, 4)}")
    
    # 完成包围
    print("\n白方完成包围:")
    board.current_player = Stone.WHITE
    success, msg, captured = board.play(4, 5, Stone.WHITE)
    print(f"提子数量: {captured}")
    print(f"白方总提子: {board.captured[Stone.WHITE]}")
    print(f"D5 状态: {'空' if board.get(4, 4) == Stone.EMPTY else '有子'}")


def example_ko():
    """示例3: 打劫规则"""
    print("\n=== 示例3: 打劫规则 ===\n")
    
    board = GoBoard(9)
    
    # 设置打劫点
    board.ko_point = (4, 4)
    print(f"打劫点设置: {coord_to_label(4, 4)}")
    
    # 尝试在打劫点落子
    legal, reason = board.is_legal_move(4, 4)
    print(f"在打劫点落子: {'合法' if legal else '不合法'}")
    print(f"原因: {reason}")
    
    # 其他位置合法
    legal, reason = board.is_legal_move(4, 5)
    print(f"\n在其他位置落子: {'合法' if legal else '不合法'}")
    
    # 解除打劫
    board.ko_point = None
    legal, reason = board.is_legal_move(4, 4)
    print(f"\n解除打劫后: {'可以落子' if legal else '不能落子'}")


def example_territory():
    """示例4: 领地计算"""
    print("\n=== 示例4: 领地计算 ===\n")
    
    board = GoBoard(9)
    
    # 黑方占据一角
    black_positions = [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 2),
        (2, 0), (2, 1), (2, 2),
    ]
    for row, col in black_positions:
        board.set(row, col, Stone.BLACK)
    
    # 白方占据一角
    white_positions = [
        (6, 0), (6, 1), (6, 2),
        (7, 0), (7, 2),
        (8, 0), (8, 1), (8, 2),
    ]
    for row, col in white_positions:
        board.set(row, col, Stone.WHITE)
    
    print("黑方占据左上角，白方占据左下角")
    print(board)
    
    # 计算领地
    territory = Territory.calculate(board)
    print(f"\n领地计算:")
    print(f"黑方领地: {territory[Stone.BLACK]} 目")
    print(f"白方领地: {territory[Stone.WHITE]} 目")


def example_sgf():
    """示例5: SGF 格式"""
    print("\n=== 示例5: SGF 格式 ===\n")
    
    board = GoBoard(9)
    
    # 简单对局
    moves = [(4, 4), (3, 4), (5, 4), (3, 3)]
    for i, (row, col) in enumerate(moves):
        board.play(row, col)
    
    print(f"完成 {len(moves)} 步对局")
    
    # 导出 SGF
    sgf = SGF.export(board, black_name="玩家A", white_name="玩家B", result="B+R")
    print("\n导出 SGF 格式:")
    print(sgf)
    
    # 解析 SGF
    sgf_input = "(;SZ[9];B[dd];W[cd];B[ed];W[cc])"
    parsed_board = SGF.parse(sgf_input)
    print(f"\n解析 SGF 棋盘大小: {parsed_board.size}")
    print(f"解析历史步数: {len(parsed_board.history)}")


def example_score():
    """示例6: 计分系统"""
    print("\n=== 示例6: 计分系统 ===\n")
    
    board = GoBoard(9)
    
    # 黑方棋子
    for i in range(3):
        for j in range(3):
            board.set(i, j, Stone.BLACK)
    
    # 白方棋子
    for i in range(6, 9):
        for j in range(6, 9):
            board.set(i, j, Stone.WHITE)
    
    print("简单局面: 黑方左上角，白方右下角")
    
    # 中国规则
    score_chinese = ScoreCalculator.calculate_chinese_score(board, komi=7.5)
    print("\n中国规则计分:")
    print(f"黑方: {score_chinese['black']['stones']} 子 + {score_chinese['black']['territory']} 领地 = {score_chinese['black']['total']} 目")
    print(f"白方: {score_chinese['white']['stones']} 子 + {score_chinese['white']['territory']} 领地 + {score_chinese['komi']} 贴目 = {score_chinese['white']['total']} 目")
    print(f"胜负: {score_chinese['winner']} 方胜 {score_chinese['margin']} 目")
    
    # 日本规则
    score_japanese = ScoreCalculator.calculate_japanese_score(board, komi=6.5)
    print("\n日本规则计分:")
    print(f"黑方: {score_japanese['black']['territory']} 领地 + {score_japanese['black']['captures']} 提子 = {score_japanese['black']['total']} 目")
    print(f"白方: {score_japanese['white']['territory']} 领地 + {score_japanese['white']['captures']} 提子 + {score_japanese['komi']} 贴目 = {score_japanese['white']['total']} 目")


def example_life_death():
    """示例7: 死活分析"""
    print("\n=== 示例7: 死活分析 ===\n")
    
    board = GoBoard(9)
    
    # 单子
    board.play(4, 4)
    print("黑方单子在中央")
    
    analysis = LifeDeath.analyze_group(board, 4, 4)
    print(f"\n棋子组分析:")
    print(f"大小: {analysis['size']} 子")
    print(f"气数: {analysis['liberties']} 气")
    print(f"眼数: {analysis['eyes']} 个")
    print(f"状态: {analysis['status']}")
    
    # 找眼
    board2 = GoBoard(9)
    # 黑方包围一个小区域（简化眼形）
    for pos in [(3, 3), (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4), (5, 5)]:
        board2.set(pos[0], pos[1], Stone.BLACK)
    
    eyes = LifeDeath.get_eyes(board2, Stone.BLACK)
    print(f"\n黑方眼数: {len(eyes)}")


def example_pattern():
    """示例8: 棋形识别"""
    print("\n=== 示例8: 棋形识别 ===\n")
    
    board = GoBoard(9)
    
    # 黑方单子
    board.play(4, 4, Stone.BLACK)
    print("黑方单子在 D5")
    
    # 白方三面包围（形成打吃）
    board.set(3, 4, Stone.WHITE)
    board.set(4, 3, Stone.WHITE)
    board.set(5, 4, Stone.WHITE)
    
    print("\n白方三面包围")
    
    # 打吃检测
    is_atari = Pattern.is_atari(board, 4, 4)
    print(f"黑子是否被打吃: {'是' if is_atari else '否'}")
    print(f"黑子气数: {board.count_liberties(4, 4)}")
    
    # 找打吃组
    atari_groups = Pattern.find_atari_groups(board, Stone.BLACK)
    print(f"打吃组数量: {len(atari_groups)}")
    
    # 劫材
    threats = Pattern.find_ko_threats(board)
    print(f"劫材点数量: {len(threats)}")


def example_handicap():
    """示例9: 让子设置"""
    print("\n=== 示例9: 让子设置 ===\n")
    
    board = GoBoard(19)
    
    # 设置3子让子
    success = Handicap.setup_handicap(board, 3)
    print(f"设置3子让子: {'成功' if success else '失败'}")
    print(f"当前玩家: {'白方' if board.current_player == Stone.WHITE else '黑方'}")
    
    print("\n让子位置:")
    for row in range(19):
        for col in range(19):
            if board.get(row, col) == Stone.BLACK:
                print(f"  {coord_to_label(row, col)}")
    
    # 不同让子数
    print("\n标准让子位置数:")
    for n in range(2, 10):
        board_n = GoBoard(19)
        Handicap.setup_handicap(board_n, n)
        count = sum(1 for r in range(19) for c in range(19) if board_n.get(r, c) == Stone.BLACK)
        print(f"  {n}子: {count} 个星位")


def example_coordinate_system():
    """示例10: 坐标系统"""
    print("\n=== 示例10: 坐标系统 ===\n")
    
    # SGF 坐标
    print("SGF 坐标系统:")
    print(f"  (0, 0) -> {coord_to_sgf(0, 0)}")
    print(f"  (3, 3) -> {coord_to_sgf(3, 3)}")
    print(f"  (8, 8) -> {coord_to_sgf(8, 8)}")
    
    # 棋盘标记（跳过 I）
    print("\n棋盘标记系统（跳过 I）:")
    print(f"  (0, 0) -> {coord_to_label(0, 0)}")
    print(f"  (7, 7) -> {coord_to_label(7, 7)}")
    print(f"  (8, 8) -> {coord_to_label(8, 8)}")
    
    # 逆向转换
    print("\n逆向转换:")
    sgf = "dd"
    print(f"  SGF '{sgf}' -> 坐标 {sgf_to_coord(sgf)}")
    
    label = "J9"
    print(f"  标记 '{label}' -> 坐标 {label_to_coord(label)}")


def example_game_simulation():
    """示例11: 模拟简单对局"""
    print("\n=== 示例11: 模拟简单对局 ===\n")
    
    board = GoBoard(9)
    
    # 模拟对局
    moves = [
        (4, 4, 'B'),  # 黑方中央
        (3, 4, 'W'),  # 白方上方
        (5, 4, 'B'),  # 黑方下方
        (3, 3, 'W'),  # 白方左上
        (4, 5, 'B'),  # 黑方右边
        (2, 4, 'W'),  # 白方更上方
        (6, 4, 'B'),  # 黑方更下方
    ]
    
    for row, col, color in moves:
        stone = Stone.BLACK if color == 'B' else Stone.WHITE
        success, msg, captured = board.play(row, col, stone)
        player = "黑方" if stone == Stone.BLACK else "白方"
        print(f"{player} 落子 {coord_to_label(row, col)}: {msg}")
        if captured > 0:
            print(f"  提子 {captured} 个")
    
    print(f"\n对局结束状态:")
    print(f"步数: {len(board.history)}")
    print(f"黑方提子: {board.captured[Stone.BLACK]}")
    print(f"白方提子: {board.captured[Stone.WHITE]}")
    
    # 计算结果
    score = ScoreCalculator.calculate_chinese_score(board)
    print(f"\n当前计分:")
    print(f"黑方: {score['black']['total']} 目")
    print(f"白方: {score['white']['total']} 目")


def main():
    """运行所有示例"""
    print("="*50)
    print("围棋工具使用示例")
    print("="*50)
    
    examples = [
        example_basic_board,
        example_capture,
        example_ko,
        example_territory,
        example_sgf,
        example_score,
        example_life_death,
        example_pattern,
        example_handicap,
        example_coordinate_system,
        example_game_simulation,
    ]
    
    for example in examples:
        example()
    
    print("\n" + "="*50)
    print("所有示例完成!")
    print("="*50)


if __name__ == "__main__":
    main()