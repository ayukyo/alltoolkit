"""
围棋工具模块测试

测试覆盖：
- 棋盘基础操作
- 落子规则（合法落子、禁入点、自杀）
- 打劫规则
- 提子规则
- 气的计算
- 死活判断
- 领地计算
- SGF 格式
- 计分系统
- 棋形识别
- 让子设置
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    GoBoard, Stone, BoardSize, Move, Territory, LifeDeath,
    SGF, ScoreCalculator, Pattern, Handicap,
    create_board, quick_play, coord_to_sgf, sgf_to_coord,
    coord_to_label, label_to_coord
)


class ResultCollector:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_true(self, condition: bool, message: str):
        if condition:
            self.passed += 1
            print(f"  ✓ {message}")
        else:
            self.failed += 1
            self.errors.append(message)
            print(f"  ✗ {message}")
    
    def assert_equal(self, expected, actual, message: str):
        if expected == actual:
            self.passed += 1
            print(f"  ✓ {message}")
        else:
            self.failed += 1
            self.errors.append(f"{message}: 期望 {expected}, 实际 {actual}")
            print(f"  ✗ {message}: 期望 {expected}, 实际 {actual}")
    
    def assert_raises(self, exception_type, func, message: str):
        try:
            func()
            self.failed += 1
            self.errors.append(f"{message}: 未抛出异常")
            print(f"  ✗ {message}: 未抛出异常")
        except exception_type:
            self.passed += 1
            print(f"  ✓ {message}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*50}")
        print(f"测试结果: {self.passed}/{total} 通过")
        if self.errors:
            print(f"\n失败测试:")
            for error in self.errors:
                print(f"  - {error}")
        print(f"{'='*50}")
        return self.failed == 0


def test_board_creation():
    """测试棋盘创建"""
    print("\n[测试] 棋盘创建")
    rc = ResultCollector()
    
    # 测试标准棋盘
    board = GoBoard(19)
    rc.assert_equal(19, board.size, "19路棋盘大小")
    rc.assert_equal(Stone.BLACK, board.current_player, "黑方先行")
    
    # 测试中棋盘
    board13 = GoBoard(13)
    rc.assert_equal(13, board13.size, "13路棋盘大小")
    
    # 测试小棋盘
    board9 = GoBoard(9)
    rc.assert_equal(9, board9.size, "9路棋盘大小")
    
    # 测试无效大小
    rc.assert_raises(ValueError, lambda: GoBoard(10), "拒绝无效棋盘大小")
    
    # 测试初始状态
    board = GoBoard(19)
    rc.assert_equal(Stone.EMPTY, board.get(0, 0), "初始棋盘为空")
    rc.assert_equal(0, board.captured[Stone.BLACK], "初始提子数为0")
    rc.assert_equal(0, len(board.history), "初始历史为空")
    
    return rc.summary()


def test_board_operations():
    """测试棋盘操作"""
    print("\n[测试] 棋盘操作")
    rc = ResultCollector()
    
    board = GoBoard(9)
    
    # 位置验证
    rc.assert_true(board.is_valid_position(0, 0), "左上角位置有效")
    rc.assert_true(board.is_valid_position(8, 8), "右下角位置有效")
    rc.assert_true(not board.is_valid_position(-1, 0), "负行无效")
    rc.assert_true(not board.is_valid_position(9, 0), "超出行无效")
    
    # 设置和获取
    board.set(4, 4, Stone.BLACK)
    rc.assert_equal(Stone.BLACK, board.get(4, 4), "设置黑子")
    board.set(4, 4, Stone.WHITE)
    rc.assert_equal(Stone.WHITE, board.get(4, 4), "设置白子")
    
    # 邻点
    neighbors = board.get_neighbors(4, 4)
    rc.assert_equal(4, len(neighbors), "中央点有4个邻点")
    
    neighbors_corner = board.get_neighbors(0, 0)
    rc.assert_equal(2, len(neighbors_corner), "角点有2个邻点")
    
    neighbors_edge = board.get_neighbors(0, 4)
    rc.assert_equal(3, len(neighbors_edge), "边点有3个邻点")
    
    # 星位
    rc.assert_true(board.is_star_point(4, 4), "9路棋盘中央为星位")
    board19 = GoBoard(19)
    rc.assert_true(board19.is_star_point(3, 3), "19路棋盘左上星位")
    
    # 副本
    board.set(1, 1, Stone.BLACK)
    board_copy = board.copy()
    rc.assert_equal(Stone.BLACK, board_copy.get(1, 1), "副本保持棋子")
    board_copy.set(1, 1, Stone.WHITE)
    rc.assert_equal(Stone.BLACK, board.get(1, 1), "副本修改不影响原棋盘")
    
    return rc.summary()


def test_play_moves():
    """测试落子"""
    print("\n[测试] 落子操作")
    rc = ResultCollector()
    
    board = GoBoard(9)
    
    # 正常落子
    success, msg, captured = board.play(4, 4)
    rc.assert_true(success, "合法落子成功")
    rc.assert_equal(Stone.BLACK, board.get(4, 4), "落子位置有黑子")
    rc.assert_equal(Stone.WHITE, board.current_player, "轮换到白方")
    rc.assert_equal(1, len(board.history), "历史记录增加")
    rc.assert_equal(0, captured, "无提子")
    
    # 白方落子
    success, msg, captured = board.play(3, 4)
    rc.assert_true(success, "白方落子成功")
    rc.assert_equal(Stone.WHITE, board.get(3, 4), "白子位置")
    rc.assert_equal(Stone.BLACK, board.current_player, "轮换到黑方")
    
    # 非法落子 - 已有棋子
    success, msg, captured = board.play(4, 4)
    rc.assert_true(not success, "不能在已有棋子处落子")
    rc.assert_equal("该位置已有棋子", msg, "错误信息正确")
    
    # 非法落子 - 超出范围
    success, msg, captured = board.play(10, 10)
    rc.assert_true(not success, "不能超出棋盘范围")
    
    # 落子验证
    legal, reason = board.is_legal_move(5, 5)
    rc.assert_true(legal, "空位合法")
    
    legal, reason = board.is_legal_move(4, 4)
    rc.assert_true(not legal, "有子位置不合法")
    
    # 获取合法落子点
    legal_moves = board.get_legal_moves()
    rc.assert_true((5, 5) in legal_moves, "空位在合法落子列表")
    rc.assert_true((4, 4) not in legal_moves, "有子位置不在合法列表")
    
    return rc.summary()


def test_capture():
    """测试提子"""
    print("\n[测试] 提子规则")
    rc = ResultCollector()
    
    board = GoBoard(9)
    
    # 简单提子 - 单子
    # 黑方在中心落子，白方包围
    board.play(4, 4)  # 黑
    board.play(3, 4)  # 白
    board.play(5, 4)  # 黑
    board.play(4, 3)  # 白
    board.play(4, 5)  # 黑
    # 此时黑子在(4,4)和(5,4)连接
    
    # 继续包围
    board.play(5, 3)  # 白
    board.play(6, 4)  # 黑
    board.play(5, 5)  # 白
    board.play(3, 5)  # 黑
    board.play(6, 3)  # 白
    
    # 提子测试 - 完全包围一个子
    board2 = GoBoard(9)
    board2.play(4, 4, Stone.BLACK)
    board2.play(3, 4, Stone.WHITE)
    board2.play(4, 3, Stone.WHITE)
    board2.play(5, 4, Stone.WHITE)
    success, msg, captured = board2.play(4, 5, Stone.WHITE)
    rc.assert_equal(1, captured, "包围提子")
    rc.assert_equal(Stone.EMPTY, board2.get(4, 4), "被提位置为空")
    rc.assert_equal(1, board2.captured[Stone.WHITE], "提子计数")
    
    # 气的计算
    board3 = GoBoard(9)
    board3.play(4, 4, Stone.BLACK)
    liberties = board3.count_liberties(4, 4)
    rc.assert_equal(4, liberties, "单子有4气")
    
    board3.play(4, 3, Stone.BLACK)
    liberties = board3.count_liberties(4, 4)
    rc.assert_equal(6, liberties, "双子连接有6气")
    
    # 连通组
    board4 = GoBoard(9)
    board4.play(4, 4, Stone.BLACK)
    board4.play(4, 3, Stone.BLACK)
    board4.play(3, 4, Stone.BLACK)
    group = board4.get_group(4, 4)
    rc.assert_equal(3, len(group), "连通组大小")
    rc.assert_true((4, 3) in group, "邻子属于同组")
    
    return rc.summary()


def test_ko():
    """测试打劫规则"""
    print("\n[测试] 打劫规则")
    rc = ResultCollector()
    
    # 创建打劫形状
    #  ⚫ ⚪ ⚫
    #  ⚪ ⚫ ⚪
    #  ⚫ ⚪ ⚫
    board = GoBoard(9)
    
    # 设置打劫形状（简化）
    board.play(4, 4, Stone.BLACK)
    board.play(3, 4, Stone.WHITE)
    board.play(4, 3, Stone.WHITE)
    board.play(5, 4, Stone.WHITE)
    board.play(4, 5, Stone.WHITE)
    
    # 这不是经典打劫形状，需要更精确的设置
    # 经典打劫测试
    board2 = GoBoard(9)
    
    # 黑子
    board2.set(1, 2, Stone.BLACK)
    board2.set(2, 1, Stone.BLACK)
    board2.set(2, 3, Stone.BLACK)
    board2.set(3, 2, Stone.BLACK)
    
    # 白子包围
    board2.set(0, 2, Stone.WHITE)
    board2.set(1, 1, Stone.WHITE)
    board2.set(1, 3, Stone.WHITE)
    board2.set(3, 1, Stone.WHITE)
    board2.set(3, 3, Stone.WHITE)
    board2.set(2, 2, Stone.WHITE)
    
    board2.current_player = Stone.BLACK
    
    # 验证打劫点设置
    board3 = GoBoard(9)
    board3.play(2, 2, Stone.BLACK)
    board3.play(2, 1, Stone.WHITE)
    board3.play(1, 2, Stone.BLACK)
    board3.play(1, 1, Stone.WHITE)
    board3.play(3, 2, Stone.BLACK)
    board3.play(2, 3, Stone.WHITE)
    board3.play(3, 1, Stone.WHITE)
    board3.play(3, 3, Stone.WHITE)
    
    # 测试打劫检测
    board4 = GoBoard(9)
    board4.ko_point = (4, 4)
    legal, reason = board4.is_legal_move(4, 4)
    rc.assert_true(not legal, "打劫点不能立即落子")
    rc.assert_equal("打劫点，不能立即落子", reason, "打劫错误信息")
    
    board4.ko_point = None
    legal, reason = board4.is_legal_move(4, 4)
    rc.assert_true(legal, "取消打劫后可落子")
    
    return rc.summary()


def test_suicide():
    """测试自杀规则"""
    print("\n[测试] 自杀规则")
    rc = ResultCollector()
    
    board = GoBoard(9)
    
    # 创建包围形状
    board.set(3, 4, Stone.WHITE)
    board.set(4, 3, Stone.WHITE)
    board.set(5, 4, Stone.WHITE)
    board.set(4, 5, Stone.WHITE)
    
    # 检查自杀检测
    board.current_player = Stone.BLACK
    is_suicide = board.would_be_suicide(4, 4, Stone.BLACK)
    rc.assert_true(is_suicide, "被包围的空点是自杀点")
    
    # 非自杀 - 有气
    board2 = GoBoard(9)
    is_suicide = board2.would_be_suicide(4, 4, Stone.BLACK)
    rc.assert_true(not is_suicide, "有气的点不是自杀点")
    
    # 非自杀 - 能提子
    board3 = GoBoard(9)
    board3.set(3, 4, Stone.WHITE)
    board3.set(4, 3, Stone.WHITE)
    board3.set(5, 4, Stone.WHITE)
    # (4, 5) 空着，所以有气
    
    board4 = GoBoard(9)
    board4.set(4, 4, Stone.WHITE)
    board4.set(3, 4, Stone.BLACK)
    board4.set(5, 4, Stone.BLACK)
    board4.set(4, 3, Stone.BLACK)
    # 黑方在(4, 5)落子可以提白子
    is_suicide = board4.would_be_suicide(4, 5, Stone.BLACK)
    rc.assert_true(not is_suicide, "能提子的点不是自杀点")
    
    return rc.summary()


def test_pass_and_game_end():
    """测试虚手和游戏结束"""
    print("\n[测试] 虚手和游戏结束")
    rc = ResultCollector()
    
    board = GoBoard(9)
    
    # 虚手
    board.pass_turn()
    rc.assert_equal(Stone.WHITE, board.current_player, "虚手后换手")
    rc.assert_equal(1, board.passes, "虚手计数")
    rc.assert_equal(1, len(board.history), "虚手记录历史")
    
    board.pass_turn()
    rc.assert_equal(2, board.passes, "第二次虚手")
    rc.assert_true(board.is_game_over(), "连续虚手游戏结束")
    
    # 落子后重置虚手计数
    board2 = GoBoard(9)
    board2.pass_turn()
    board2.play(4, 4)
    rc.assert_equal(0, board2.passes, "落子后重置虚手计数")
    
    return rc.summary()


def test_territory():
    """测试领地计算"""
    print("\n[测试] 领地计算")
    rc = ResultCollector()
    
    board = GoBoard(9)
    
    # 完全由黑方包围的区域
    for i in range(3):
        board.set(i, 0, Stone.BLACK)
        board.set(i, 2, Stone.BLACK)
    board.set(0, 1, Stone.BLACK)
    board.set(2, 1, Stone.BLACK)
    
    # 完全由白方包围的区域
    for i in range(6, 9):
        board.set(i, 0, Stone.WHITE)
        board.set(i, 2, Stone.WHITE)
    board.set(6, 1, Stone.WHITE)
    board.set(8, 1, Stone.WHITE)
    
    territory = Territory.calculate(board)
    rc.assert_equal(1, territory[Stone.BLACK], "黑方领地(1个空点)")
    rc.assert_equal(1, territory[Stone.WHITE], "白方领地(1个空点)")
    
    # 领地地图
    territory_map = Territory.get_territory_map(board)
    rc.assert_true((1, 1) in territory_map, "空点在领地地图")
    rc.assert_equal(Stone.BLACK, territory_map.get((1, 1)), "黑方区域归属")
    
    # 空棋盘无领地
    board_empty = GoBoard(9)
    territory_empty = Territory.calculate(board_empty)
    rc.assert_equal(0, territory_empty[Stone.BLACK], "空棋盘无黑方领地")
    rc.assert_equal(0, territory_empty[Stone.WHITE], "空棋盘无白方领地")
    
    return rc.summary()


def test_life_death():
    """测试死活判断"""
    print("\n[测试] 死活判断")
    rc = ResultCollector()
    
    board = GoBoard(9)
    
    # 眼的形成 - 简化测试
    # 黑子完全包围一个空点 (创建真正的眼形)
    for pos in [(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)]:
        board.set(pos[0], pos[1], Stone.BLACK)
    
    # 现在 (3, 3) 是一个被黑子包围的空点，应该是黑方的眼
    eyes = LifeDeath.get_eyes(board, Stone.BLACK)
    rc.assert_true(len(eyes) >= 1, "黑子包围区域形成眼")
    # 检查是否有眼包含中心点
    has_center_eye = any((3, 3) in eye for eye in eyes)
    rc.assert_true(has_center_eye, "眼包含中心空点")
    
    # 测试空棋盘无眼
    board2 = GoBoard(9)
    eyes = LifeDeath.get_eyes(board2, Stone.BLACK)
    rc.assert_equal(0, len(eyes), "空棋盘无眼")
    
    # 分析棋子组
    board3 = GoBoard(9)
    board3.play(4, 4, Stone.BLACK)
    analysis = LifeDeath.analyze_group(board3, 4, 4)
    rc.assert_equal(1, analysis['size'], "棋子组大小")
    rc.assert_equal(4, analysis['liberties'], "单子有4气")
    rc.assert_equal('uncertain', analysis['status'], "单子状态不确定")
    
    # 分析空点
    analysis_empty = LifeDeath.analyze_group(board3, 0, 0)
    rc.assert_equal('empty', analysis_empty['status'], "空点状态")
    
    return rc.summary()


def test_sgf():
    """测试 SGF 格式"""
    print("\n[测试] SGF 格式")
    rc = ResultCollector()
    
    board = GoBoard(9)
    board.play(4, 4)  # 黑方在 row=4, col=4 -> SGF: "ee"
    board.play(3, 4)  # 白方在 row=3, col=4 -> SGF: "ed"
    
    # 导出
    sgf = SGF.export(board, black_name="黑方", white_name="白方")
    rc.assert_true("SZ[9]" in sgf, "SGF包含棋盘大小")
    rc.assert_true("PB[黑方]" in sgf, "SGF包含黑方名称")
    rc.assert_true("B[ee]" in sgf, "SGF包含黑方落子 (ee)")
    rc.assert_true("W[ed]" in sgf, "SGF包含白方落子 (ed)")
    
    # 解析
    sgf_content = "(;SZ[9];B[ee];W[ed];B[dd])"  # B[ee]=row=4,col=4, W[ed]=row=3,col=4, B[dd]=row=3,col=3
    parsed_board = SGF.parse(sgf_content)
    rc.assert_equal(9, parsed_board.size, "解析棋盘大小")
    rc.assert_equal(Stone.BLACK, parsed_board.get(4, 4), "解析黑子位置 (ee -> 4,4)")
    rc.assert_equal(Stone.WHITE, parsed_board.get(3, 4), "解析白子位置 (ed -> 3,4)")
    rc.assert_equal(Stone.BLACK, parsed_board.get(3, 3), "解析第三步 (dd -> 3,3)")
    
    # Move 的 SGF 方法
    # SGF 格式: 列字母 + 行字母, (3,3) -> col=3='d', row=3='d' -> "dd"
    move = Move(row=3, col=3, stone=Stone.BLACK)
    rc.assert_equal("dd", move.to_sgf(), "坐标转SGF (row=3,col=3)")
    
    move_parsed = Move.from_sgf("dd", Stone.BLACK)
    rc.assert_equal(3, move_parsed.row, "SGF转坐标-行")
    rc.assert_equal(3, move_parsed.col, "SGF转坐标-列")
    
    # 坐标转换函数
    rc.assert_equal("dd", coord_to_sgf(3, 3), "coord_to_sgf函数 (row=3,col=3)")
    rc.assert_equal((3, 3), sgf_to_coord("dd"), "sgf_to_coord函数")
    
    return rc.summary()


def test_score():
    """测试计分"""
    print("\n[测试] 计分系统")
    rc = ResultCollector()
    
    board = GoBoard(9)
    
    # 简单局面 - 黑方占据一角
    for i in range(3):
        board.set(i, 0, Stone.BLACK)
        board.set(i, 1, Stone.BLACK)
        board.set(i, 2, Stone.BLACK)
    
    # 中国规则
    score_chinese = ScoreCalculator.calculate_chinese_score(board, komi=7.5)
    rc.assert_true('black' in score_chinese, "中国规则包含黑方")
    rc.assert_true('white' in score_chinese, "中国规则包含白方")
    rc.assert_equal(7.5, score_chinese['komi'], "贴目值")
    
    # 日本规则
    score_japanese = ScoreCalculator.calculate_japanese_score(board, komi=6.5)
    rc.assert_equal(6.5, score_japanese['komi'], "日本规则贴目")
    
    # 空棋盘计分
    board_empty = GoBoard(9)
    score_empty = ScoreCalculator.calculate_chinese_score(board_empty)
    rc.assert_equal(7.5, score_empty['white']['total'], "空棋盘白方只有贴目")
    rc.assert_equal('white', score_empty['winner'], "空棋盘白方胜")
    
    return rc.summary()


def test_pattern():
    """测试棋形识别"""
    print("\n[测试] 棋形识别")
    rc = ResultCollector()
    
    board = GoBoard(9)
    
    # 打吃检测
    board.play(4, 4, Stone.BLACK)
    board.play(3, 4, Stone.WHITE)
    board.play(5, 4, Stone.WHITE)
    board.play(4, 3, Stone.WHITE)
    # 黑子只剩一气
    is_atari = Pattern.is_atari(board, 4, 4)
    rc.assert_true(is_atari, "打吃检测")
    
    # 找打吃组
    atari_groups = Pattern.find_atari_groups(board, Stone.BLACK)
    rc.assert_equal(1, len(atari_groups), "找到1个打吃组")
    
    # 眼位检测
    board2 = GoBoard(9)
    # 黑子包围一个点
    board2.set(4, 4, Stone.BLACK)
    board2.set(3, 4, Stone.BLACK)
    board2.set(5, 4, Stone.BLACK)
    board2.set(4, 3, Stone.BLACK)
    board2.set(4, 5, Stone.BLACK)
    
    # 检查对角线是否可能成为眼
    is_eye = Pattern.is_eye_point(board2, 4, 4, Stone.BLACK)
    rc.assert_true(not is_eye, "有子位置不是眼位")
    
    # 劫材
    board3 = GoBoard(9)
    threats = Pattern.find_ko_threats(board3)
    rc.assert_equal(0, len(threats), "空棋盘无劫材")
    
    return rc.summary()


def test_handicap():
    """测试让子"""
    print("\n[测试] 让子设置")
    rc = ResultCollector()
    
    board = GoBoard(19)
    
    # 2子让子
    success = Handicap.setup_handicap(board, 2)
    rc.assert_true(success, "设置2子让子")
    rc.assert_equal(Stone.BLACK, board.get(3, 15), "2子让子位置1")
    rc.assert_equal(Stone.BLACK, board.get(15, 3), "2子让子位置2")
    rc.assert_equal(Stone.WHITE, board.current_player, "让子后白方先行")
    
    # 9子让子
    board2 = GoBoard(19)
    success = Handicap.setup_handicap(board2, 9)
    rc.assert_true(success, "设置9子让子")
    rc.assert_equal(Stone.WHITE, board2.current_player, "9子让子白方先行")
    
    # 无效让子数
    board3 = GoBoard(19)
    success = Handicap.setup_handicap(board3, 10)
    rc.assert_true(not success, "拒绝无效让子数")
    
    # 非19路棋盘不支持标准让子
    board9 = GoBoard(9)
    success = Handicap.setup_handicap(board9, 2)
    rc.assert_true(not success, "9路棋盘不支持标准让子")
    
    return rc.summary()


def test_coordinate_functions():
    """测试坐标函数"""
    print("\n[测试] 坐标函数")
    rc = ResultCollector()
    
    # SGF 转换
    rc.assert_equal("aa", coord_to_sgf(0, 0), "(0,0) -> aa")
    rc.assert_equal("dd", coord_to_sgf(3, 3), "(3,3) -> dd")
    rc.assert_equal((0, 0), sgf_to_coord("aa"), "aa -> (0,0)")
    rc.assert_equal((3, 3), sgf_to_coord("dd"), "dd -> (3,3)")
    
    # 棋盘标记（跳过I）
    rc.assert_equal("A1", coord_to_label(0, 0), "(0,0) -> A1")
    rc.assert_equal("J9", coord_to_label(8, 8), "(8,8) -> J9 (跳过I)")
    rc.assert_equal((0, 0), label_to_coord("A1"), "A1 -> (0,0)")
    rc.assert_equal((8, 8), label_to_coord("J9"), "J9 -> (8,8)")
    
    # 无效坐标
    rc.assert_raises(ValueError, lambda: sgf_to_coord("a"), "拒绝无效SGF长度")
    rc.assert_raises(ValueError, lambda: label_to_coord("A"), "拒绝无效标记长度")
    
    return rc.summary()


def test_utility_functions():
    """测试便捷函数"""
    print("\n[测试] 便捷函数")
    rc = ResultCollector()
    
    # 创建棋盘
    board = create_board(13)
    rc.assert_equal(13, board.size, "create_board函数")
    
    # 快速落子
    board = create_board(9)
    moves = [(4, 4, 'B'), (3, 4, 'W'), (5, 4, 'B')]
    new_board = quick_play(board, moves)
    rc.assert_equal(Stone.BLACK, new_board.get(4, 4), "quick_play黑子")
    rc.assert_equal(Stone.WHITE, new_board.get(3, 4), "quick_play白子")
    rc.assert_equal(Stone.BLACK, new_board.get(5, 4), "quick_play黑子")
    rc.assert_equal(Stone.EMPTY, board.get(4, 4), "原棋盘不变")
    
    return rc.summary()


def test_reset():
    """测试重置"""
    print("\n[测试] 棋盘重置")
    rc = ResultCollector()
    
    board = GoBoard(9)
    board.play(4, 4)
    board.play(3, 4)
    board.play(5, 4)
    
    board.reset()
    rc.assert_equal(Stone.EMPTY, board.get(4, 4), "重置后棋盘为空")
    rc.assert_equal(Stone.BLACK, board.current_player, "重置后黑方先行")
    rc.assert_equal(0, len(board.history), "重置后历史清空")
    rc.assert_equal(0, board.captured[Stone.BLACK], "重置后提子清零")
    
    return rc.summary()


def test_move_string():
    """测试 Move 字符串表示"""
    print("\n[测试] Move 字符串")
    rc = ResultCollector()
    
    move = Move(row=0, col=0, stone=Stone.BLACK)
    rc.assert_equal("A1", str(move), "Move字符串表示 A1")
    
    move = Move(row=8, col=8, stone=Stone.WHITE)
    rc.assert_equal("J9", str(move), "Move字符串表示 J9 (跳过I)")
    
    move = Move(row=4, col=7, stone=Stone.BLACK)
    rc.assert_equal("H5", str(move), "Move字符串表示 H5")
    
    return rc.summary()


def test_edge_cases():
    """测试边界情况"""
    print("\n[测试] 边界情况")
    rc = ResultCollector()
    
    # 角落点
    board = GoBoard(9)
    board.play(0, 0)  # 左上角
    liberties = board.count_liberties(0, 0)
    rc.assert_equal(2, liberties, "角点有2气")
    
    # 边点
    board.play(0, 4)  # 上边
    liberties = board.count_liberties(0, 4)
    rc.assert_equal(3, liberties, "边点有3气")
    
    # 大棋盘边界
    board19 = GoBoard(19)
    board19.play(18, 18)
    rc.assert_true(board19.is_valid_position(18, 18), "19路棋盘右下角")
    rc.assert_true(not board19.is_valid_position(19, 19), "19路棋盘超出边界")
    
    # 空棋盘合法落子数
    board_empty = GoBoard(9)
    legal_moves = board_empty.get_legal_moves()
    rc.assert_equal(81, len(legal_moves), "空棋盘81个合法落子点")
    
    return rc.summary()


def test_stone_enum():
    """测试 Stone 枚举"""
    print("\n[测试] Stone 枚举")
    rc = ResultCollector()
    
    # 对手
    rc.assert_equal(Stone.WHITE, Stone.BLACK.opponent(), "黑方对手是白方")
    rc.assert_equal(Stone.BLACK, Stone.WHITE.opponent(), "白方对手是黑方")
    rc.assert_equal(Stone.EMPTY, Stone.EMPTY.opponent(), "空对手是空")
    
    # SGF 转换
    rc.assert_equal('B', Stone.BLACK.to_sgf(), "黑方SGF代码")
    rc.assert_equal('W', Stone.WHITE.to_sgf(), "白方SGF代码")
    rc.assert_equal('', Stone.EMPTY.to_sgf(), "空SGF代码")
    
    return rc.summary()


def test_board_string():
    """测试棋盘字符串输出"""
    print("\n[测试] 棋盘字符串")
    rc = ResultCollector()
    
    board = GoBoard(9)
    board.play(4, 4)
    board_str = str(board)
    
    rc.assert_true("当前玩家: 白" in board_str, "字符串包含当前玩家")
    rc.assert_true("提子:" in board_str, "字符串包含提子信息")
    rc.assert_true("A" in board_str, "字符串包含列标记")
    rc.assert_true("1" in board_str, "字符串包含行标记")
    
    return rc.summary()


def main():
    """运行所有测试"""
    print("="*50)
    print("围棋工具模块测试")
    print("="*50)
    
    tests = [
        test_board_creation,
        test_board_operations,
        test_play_moves,
        test_capture,
        test_ko,
        test_suicide,
        test_pass_and_game_end,
        test_territory,
        test_life_death,
        test_sgf,
        test_score,
        test_pattern,
        test_handicap,
        test_coordinate_functions,
        test_utility_functions,
        test_reset,
        test_move_string,
        test_edge_cases,
        test_stone_enum,
        test_board_string,
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("所有测试通过! ✅")
    else:
        print("部分测试失败! ❌")
    print("="*50)
    
    return all_passed


if __name__ == "__main__":
    main()