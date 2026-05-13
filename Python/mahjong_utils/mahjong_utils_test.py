"""
Mahjong Utils 测试
==================

测试麻将工具库的所有功能
"""

import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mahjong_utils.mod import (
    Tile, TileType, Wind, Dragon, YakuType,
    Hand, Meld, WinDetector, YakuDetector,
    ScoreCalculator, TileEfficiency, Wall, MahjongGame,
    create_all_tiles, parse_hand, create_tile, can_win,
    calculate_shanten, get_waiting_tiles, detect_yaku, calculate_score
)


def test_result(name: str, passed: bool):
    """打印测试结果"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} {name}")


# ==================== Tile 测试 ====================

def test_tile_creation():
    """测试牌创建"""
    print("\n=== 测试牌创建 ===")
    
    # 数牌
    t1 = Tile(TileType.MAN, 1)
    test_result("创建万子1", t1.tile_type == TileType.MAN and t1.number == 1)
    
    t2 = Tile(TileType.PIN, 5)
    test_result("创建筒子5", t2.tile_type == TileType.PIN and t2.number == 5)
    
    t3 = Tile(TileType.SOU, 9)
    test_result("创建索子9", t3.tile_type == TileType.SOU and t3.number == 9)
    
    # 风牌
    t4 = Tile(TileType.WIND, 1)  # 东
    test_result("创建东风", t4.tile_type == TileType.WIND and t4.number == 1)
    
    # 三元牌
    t5 = Tile(TileType.DRAGON, 2)  # 发
    test_result("创建发财", t5.tile_type == TileType.DRAGON and t5.number == 2)
    
    # 字牌检测
    test_result("字牌检测 - 东风", t4.is_honor == True)
    test_result("字牌检测 - 万子1", t1.is_honor == False)
    
    # 幺九牌检测
    t6 = Tile(TileType.MAN, 1)  # 一万 - 幺九
    t7 = Tile(TileType.PIN, 2)  # 二筒 - 中张
    test_result("幺九牌检测 - 一万", t6.is_terminal == True)
    test_result("幺九牌检测 - 东风", t4.is_terminal_or_honor == True)
    test_result("中张牌检测 - 二筒", t7.is_simple == True)
    
    # 绿牌检测
    t8 = Tile(TileType.SOU, 2)  # 二索 - 绿
    t9 = Tile(TileType.SOU, 5)  # 五索 - 非绿
    test_result("绿牌检测 - 二索", t8.is_green == True)
    test_result("绿牌检测 - 五索", t9.is_green == False)


def test_tile_string():
    """测试牌字符串表示"""
    print("\n=== 测试牌字符串表示 ===")
    
    t1 = Tile(TileType.MAN, 3)
    test_result("字符串表示 3m", str(t1) == "3m")
    
    t2 = Tile(TileType.WIND, 1)
    test_result("中文表示 东风", t2.to_chinese() == "东风")
    
    t3 = Tile(TileType.DRAGON, 3)
    test_result("中文表示 红中", t3.to_chinese() == "红中")
    
    # 从字符串解析
    t4 = Tile.from_string("5p")
    test_result("从字符串解析 5p", t4.tile_type == TileType.PIN and t4.number == 5)
    
    t5 = Tile.from_string("东")
    test_result("从字符串解析 东", t5.tile_type == TileType.WIND and t5.number == 1)
    
    t6 = Tile.from_string("发")
    test_result("从字符串解析 发", t6.tile_type == TileType.DRAGON and t6.number == 2)


def test_tile_validation():
    """测试牌验证"""
    print("\n=== 测试牌验证 ===")
    
    # 有效牌
    try:
        Tile(TileType.MAN, 1)
        test_result("有效牌 万子1", True)
    except ValueError:
        test_result("有效牌 万子1", False)
    
    # 无效牌
    try:
        Tile(TileType.MAN, 10)
        test_result("无效牌 万子10 应报错", False)
    except ValueError:
        test_result("无效牌 万子10 应报错", True)
    
    try:
        Tile(TileType.DRAGON, 5)
        test_result("无效牌 三元牌5 应报错", False)
    except ValueError:
        test_result("无效牌 三元牌5 应报错", True)


# ==================== Hand 测试 ====================

def test_hand_creation():
    """测试手牌创建"""
    print("\n=== 测试手牌创建 ===")
    
    tiles = [Tile(TileType.MAN, 1), Tile(TileType.MAN, 2), Tile(TileType.PIN, 3)]
    hand = Hand(tiles)
    
    test_result("手牌长度", len(hand) == 3)
    test_result("手牌计数", hand.count_tile(Tile(TileType.MAN, 1)) == 1)
    
    # 添加牌
    hand.add_tile(Tile(TileType.SOU, 5))
    test_result("添加牌后长度", len(hand) == 4)
    
    # 移除牌
    hand.remove_tile(Tile(TileType.PIN, 3))
    test_result("移除牌后长度", len(hand) == 3)


def test_hand_string():
    """测试手牌字符串"""
    print("\n=== 测试手牌字符串 ===")
    
    # 从字符串解析
    hand = parse_hand("123m 456p 789s")
    test_result("解析 123m456p789s", len(hand) == 9)
    
    # 转换为字符串
    tiles = [
        Tile(TileType.MAN, 1), Tile(TileType.MAN, 2), Tile(TileType.MAN, 3),
        Tile(TileType.PIN, 4), Tile(TileType.PIN, 5), Tile(TileType.PIN, 6),
    ]
    hand = Hand(tiles)
    hand_str = hand.to_tile_string()
    test_result("手牌字符串转换", "123m" in hand_str and "456p" in hand_str)
    
    # 字牌解析
    hand2 = parse_hand("1234z 567z")
    test_result("解析字牌", len(hand2) == 7)
    
    # 验证风牌
    has_wind = any(t.tile_type == TileType.WIND for t in hand2.tiles)
    test_result("包含风牌", has_wind)
    
    # 验证三元牌
    has_dragon = any(t.tile_type == TileType.DRAGON for t in hand2.tiles)
    test_result("包含三元牌", has_dragon)


def test_hand_sort():
    """测试手牌排序"""
    print("\n=== 测试手牌排序 ===")
    
    tiles = [
        Tile(TileType.SOU, 9), Tile(TileType.MAN, 1), Tile(TileType.PIN, 5),
        Tile(TileType.WIND, 2), Tile(TileType.MAN, 3)
    ]
    hand = Hand(tiles)
    hand.sort()
    
    sorted_tiles = hand.tiles
    test_result("排序正确", sorted_tiles[0].tile_type == TileType.MAN)


# ==================== WinDetector 测试 ====================

def test_standard_win():
    """测试标准形和牌"""
    print("\n=== 测试标准形和牌 ===")
    
    # 四面子一雀头 - 简单形
    hand = parse_hand("123m 456m 789m 123p 11s")
    detector = WinDetector(hand)
    test_result("标准形和牌检测 123456789m123p11s", detector.is_standard_win())
    
    # 四刻子一雀头
    hand2 = parse_hand("111m 222m 333m 444m 55s")
    detector2 = WinDetector(hand2)
    test_result("刻子形和牌检测 111222333444m55s", detector2.is_standard_win())
    
    # 不和牌
    hand3 = parse_hand("123m 456m 789p 12s 34s")
    detector3 = WinDetector(hand3)
    test_result("不和牌检测", not detector3.can_win())


def test_seven_pairs():
    """测试七对子"""
    print("\n=== 测试七对子 ===")
    
    # 七对子
    hand = parse_hand("11223344556677m")
    detector = WinDetector(hand)
    test_result("七对子检测 11223344556677m", detector.is_seven_pairs())
    test_result("七对子可以和牌", detector.can_win())
    
    # 不是七对子
    hand2 = parse_hand("11223344556678m")
    detector2 = WinDetector(hand2)
    test_result("非七对子检测", not detector2.is_seven_pairs())


def test_thirteen_orphans():
    """测试国士无双"""
    print("\n=== 测试国士无双 ===")
    
    # 国士无双十三面
    hand = parse_hand("19m 19p 19s 1234z 567z 5z")  # 所有幺九牌 + 白重复
    detector = WinDetector(hand)
    print(f"  国士无双手牌数: {len(hand)}张 (应为14张)")
    test_result("国士无双检测", len(hand) == 14 and detector.is_thirteen_orphans())
    
    # 不是国士无双
    hand2 = parse_hand("123456789m 123p")
    detector2 = WinDetector(hand2)
    test_result("非国士无双检测", not detector2.is_thirteen_orphans())


def test_win_decomposition():
    """测试和牌分解"""
    print("\n=== 测试和牌分解 ===")
    
    hand = parse_hand("123m 456m 789m 123p 11s")
    detector = WinDetector(hand)
    decomp = detector.get_win_decomposition()
    
    test_result("分解存在", decomp is not None)
    test_result("分解为5组", len(decomp) == 5)
    
    # 检查雀头
    pairs = [m for m in decomp if m.meld_type == 'pair']
    test_result("有雀头", len(pairs) == 1)
    
    # 检查面子
    melds = [m for m in decomp if m.meld_type != 'pair']
    test_result("有4面子", len(melds) == 4)


# ==================== TileEfficiency 测试 ====================

def test_shanten():
    """测试向听数计算"""
    print("\n=== 测试向听数计算 ===")
    
    # 和牌形（向听数-1）
    hand = parse_hand("123m 456m 789m 123p 11s")
    efficiency = TileEfficiency(hand)
    test_result("和牌向听数为-1", efficiency.get_shanten() == -1)
    
    # 听牌形（向听数0）
    hand2 = parse_hand("123m 456m 789m 123p 1s")  # 缺一张一索
    efficiency2 = TileEfficiency(hand2)
    test_result("听牌向听数为0", efficiency2.get_shanten() == 0)
    
    # 一向听
    hand3 = parse_hand("123m 456m 789m 12p 1s")
    efficiency3 = TileEfficiency(hand3)
    test_result("一向听检测", efficiency3.get_shanten() == 1)


def test_waiting_tiles():
    """测试等待牌"""
    print("\n=== 测试等待牌 ===")
    
    # 听牌形
    hand = parse_hand("123m 456m 789m 12p 11s")  # 二筒三筒可成顺子
    efficiency = TileEfficiency(hand)
    
    waiting = efficiency.get_waiting_tiles()
    test_result("听牌时有等待牌", len(waiting) > 0)
    
    # 多面听
    hand2 = parse_hand("23456m 234p 234s 22z")  # 清一色两面听
    efficiency2 = TileEfficiency(hand2)
    
    if efficiency2.get_shanten() == 0:
        waiting2 = efficiency2.get_waiting_tiles()
        test_result("多面听检测", len(waiting2) >= 2)


def test_best_discard():
    """测试最佳切牌"""
    print("\n=== 测试最佳切牌 ===")
    
    # 向听手牌
    hand = parse_hand("123m 456m 789m 12p 135s")
    efficiency = TileEfficiency(hand)
    
    best = efficiency.find_best_discard()
    test_result("能找到最佳切牌", best is not None)


# ==================== YakuDetector 测试 ====================

def test_tanyao():
    """测试断幺九"""
    print("\n=== 测试断幺九 ===")
    
    hand = parse_hand("234m 345m 456m 234p 2s")  # 12张 + win_tile = 断幺九
    win_tile = Tile(TileType.SOU, 2)
    
    yaku_detector = YakuDetector(hand, win_tile)
    yaku_list = yaku_detector.detect_yaku()
    
    print(f"  手牌数: {len(hand)}张, 和牌: {win_tile}")
    print(f"  役种: {[(yt.value, han) for yt, han in yaku_list]}")
    has_tanyao = any(yt == YakuType.TANYAO for yt, _ in yaku_list)
    test_result("断幺九检测", has_tanyao)


def test_pinfu():
    """测试平和"""
    print("\n=== 测试平和 ===")
    
    hand = parse_hand("123m 456m 789p 12s 55p")  # 12张 + win_tile = 平和
    win_tile = Tile(TileType.SOU, 3)  # 两面听（1s或3s）
    
    yaku_detector = YakuDetector(hand, win_tile, is_tsumo=True)
    yaku_list = yaku_detector.detect_yaku()
    
    print(f"  手牌数: {len(hand)}张, 和牌: {win_tile}")
    print(f"  役种: {[(yt.value, han) for yt, han in yaku_list]}")
    has_pinfu = any(yt == YakuType.PINFU for yt, _ in yaku_list)
    test_result("平和检测", has_pinfu)


def test_chiitou():
    """测试七对子"""
    print("\n=== 测试七对子役 ===")
    
    # 七对子（不复合其他役）
    tiles = [
        Tile(TileType.MAN, 2), Tile(TileType.MAN, 2),
        Tile(TileType.MAN, 3), Tile(TileType.MAN, 3),
        Tile(TileType.MAN, 4), Tile(TileType.MAN, 4),
        Tile(TileType.MAN, 5), Tile(TileType.MAN, 5),
        Tile(TileType.MAN, 6), Tile(TileType.MAN, 6),
        Tile(TileType.MAN, 7), Tile(TileType.MAN, 7),
        Tile(TileType.PIN, 2),  # 听牌
    ]
    hand = Hand(tiles)
    win_tile = Tile(TileType.PIN, 2)
    
    yaku_detector = YakuDetector(hand, win_tile)
    yaku_list = yaku_detector.detect_yaku()
    
    print(f"  手牌数: {len(hand)}张, 和牌: {win_tile}")
    print(f"  役种: {[(yt.value, han) for yt, han in yaku_list]}")
    has_chiitou = any(yt == YakuType.CHIITOU for yt, _ in yaku_list)
    test_result("七对子役检测", has_chiitou)
    
    han = yaku_detector.calculate_han()
    test_result("七对子至少2番", han >= 2)


def test_honitsu():
    """测试混一色"""
    print("\n=== 测试混一色 ===")
    
    # 混一色：万子 + 字牌
    tiles = [
        Tile(TileType.MAN, 1), Tile(TileType.MAN, 2), Tile(TileType.MAN, 3),
        Tile(TileType.MAN, 4), Tile(TileType.MAN, 5), Tile(TileType.MAN, 6),
        Tile(TileType.MAN, 7), Tile(TileType.MAN, 8),
        Tile(TileType.DRAGON, 1), Tile(TileType.DRAGON, 1),
        Tile(TileType.WIND, 1), Tile(TileType.WIND, 1), Tile(TileType.WIND, 1),
    ]
    hand = Hand(tiles)
    win_tile = Tile(TileType.MAN, 9)
    
    yaku_detector = YakuDetector(hand, win_tile)
    yaku_list = yaku_detector.detect_yaku()
    
    print(f"  手牌数: {len(hand)}张, 和牌: {win_tile}")
    print(f"  役种: {[(yt.value, han) for yt, han in yaku_list]}")
    has_honitsu = any(yt == YakuType.HONITSU for yt, _ in yaku_list)
    test_result("混一色检测", has_honitsu)
    
    han = yaku_detector.calculate_han()
    test_result("门前混一色至少3番", han >= 3)


def test_chinitsu():
    """测试清一色"""
    print("\n=== 测试清一色 ===")
    
    # 清一色：纯万子
    tiles = [
        Tile(TileType.MAN, 1), Tile(TileType.MAN, 1), Tile(TileType.MAN, 1),
        Tile(TileType.MAN, 2), Tile(TileType.MAN, 3), Tile(TileType.MAN, 4),
        Tile(TileType.MAN, 5), Tile(TileType.MAN, 6), Tile(TileType.MAN, 7),
        Tile(TileType.MAN, 8), Tile(TileType.MAN, 8), Tile(TileType.MAN, 9), Tile(TileType.MAN, 9),
    ]
    hand = Hand(tiles)
    win_tile = Tile(TileType.MAN, 2)
    
    yaku_detector = YakuDetector(hand, win_tile)
    yaku_list = yaku_detector.detect_yaku()
    
    print(f"  手牌数: {len(hand)}张, 和牌: {win_tile}")
    print(f"  役种: {[(yt.value, han) for yt, han in yaku_list]}")
    has_chinitsu = any(yt == YakuType.CHINITSU for yt, _ in yaku_list)
    test_result("清一色检测", has_chinitsu)
    
    han = yaku_detector.calculate_han()
    test_result("门前清一色至少6番", han >= 6)


def test_toitoi():
    """测试对对和"""
    print("\n=== 测试对对和 ===")
    
    # 对对和：4刻子+1雀头
    tiles = [
        Tile(TileType.MAN, 1), Tile(TileType.MAN, 1), Tile(TileType.MAN, 1),
        Tile(TileType.MAN, 2), Tile(TileType.MAN, 2), Tile(TileType.MAN, 2),
        Tile(TileType.MAN, 3), Tile(TileType.MAN, 3), Tile(TileType.MAN, 3),
        Tile(TileType.MAN, 4), Tile(TileType.MAN, 4), Tile(TileType.MAN, 4),
        Tile(TileType.SOU, 5),  # 听牌
    ]
    hand = Hand(tiles)
    win_tile = Tile(TileType.SOU, 5)
    
    yaku_detector = YakuDetector(hand, win_tile)
    yaku_list = yaku_detector.detect_yaku()
    
    print(f"  手牌数: {len(hand)}张, 和牌: {win_tile}")
    print(f"  役种: {[(yt.value, han) for yt, han in yaku_list]}")
    has_toitoi = any(yt == YakuType.TOITOI for yt, _ in yaku_list)
    test_result("对对和检测", has_toitoi)


def test_yakuman():
    """测试役满"""
    print("\n=== 测试役满 ===")
    
    # 字一色 - 13张 + win_tile
    tiles = [
        Tile(TileType.WIND, 1), Tile(TileType.WIND, 1),  # 东东
        Tile(TileType.WIND, 2), Tile(TileType.WIND, 2),  # 南南
        Tile(TileType.WIND, 3), Tile(TileType.WIND, 3),  # 西西
        Tile(TileType.WIND, 4), Tile(TileType.WIND, 4),  # 北北
        Tile(TileType.DRAGON, 1), Tile(TileType.DRAGON, 1),  # 白白
        Tile(TileType.DRAGON, 2), Tile(TileType.DRAGON, 2),  # 发发
        Tile(TileType.DRAGON, 3),  # 中（听牌）
    ]
    hand = Hand(tiles)
    win_tile = Tile(TileType.DRAGON, 3)  # 红中
    
    yaku_detector = YakuDetector(hand, win_tile)
    test_result("字一色是役满", yaku_detector.is_yakuman())
    
    # 四暗刻 - 13张 + win_tile
    tiles2 = [
        Tile(TileType.MAN, 1), Tile(TileType.MAN, 1), Tile(TileType.MAN, 1),
        Tile(TileType.MAN, 2), Tile(TileType.MAN, 2), Tile(TileType.MAN, 2),
        Tile(TileType.MAN, 3), Tile(TileType.MAN, 3), Tile(TileType.MAN, 3),
        Tile(TileType.MAN, 4), Tile(TileType.MAN, 4), Tile(TileType.MAN, 4),
        Tile(TileType.SOU, 5),  # 听牌
    ]
    hand2 = Hand(tiles2)
    win_tile2 = Tile(TileType.SOU, 5)
    
    yaku_detector2 = YakuDetector(hand2, win_tile2, is_tsumo=True)
    yaku_list2 = yaku_detector2.detect_yaku()
    
    has_suuankou = any(yt == YakuType.SUUANKOU for yt, _ in yaku_list2)
    test_result("四暗刻检测（自摸）", has_suuankou)


# ==================== ScoreCalculator 测试 ====================

def test_score_calculation():
    """测试得分计算"""
    print("\n=== 测试得分计算 ===")
    
    # 简单得分 - 断幺九
    tiles = [
        Tile(TileType.MAN, 2), Tile(TileType.MAN, 3), Tile(TileType.MAN, 4),
        Tile(TileType.MAN, 3), Tile(TileType.MAN, 4), Tile(TileType.MAN, 5),
        Tile(TileType.MAN, 4), Tile(TileType.MAN, 5), Tile(TileType.MAN, 6),
        Tile(TileType.PIN, 2), Tile(TileType.PIN, 3), Tile(TileType.PIN, 4),
        Tile(TileType.SOU, 2),  # 听牌
    ]
    hand = Hand(tiles)
    win_tile = Tile(TileType.SOU, 2)
    
    yaku_detector = YakuDetector(hand, win_tile, is_tsumo=True)
    calculator = ScoreCalculator(hand, win_tile, is_tsumo=True, is_dealer=False, yaku_detector=yaku_detector)
    
    score = calculator.calculate_score()
    test_result("得分计算返回结果", score is not None and "total" in score)
    
    # 符数计算
    fu = calculator.calculate_fu()
    test_result("符数计算", fu > 0)


def test_yakuman_score():
    """测试役满得分"""
    print("\n=== 测试役满得分 ===")
    
    # 字一色 - 13张 + win_tile
    tiles = [
        Tile(TileType.WIND, 1), Tile(TileType.WIND, 1),  # 东东
        Tile(TileType.WIND, 2), Tile(TileType.WIND, 2),  # 南南
        Tile(TileType.WIND, 3), Tile(TileType.WIND, 3),  # 西西
        Tile(TileType.WIND, 4), Tile(TileType.WIND, 4),  # 北北
        Tile(TileType.DRAGON, 1), Tile(TileType.DRAGON, 1),  # 白白
        Tile(TileType.DRAGON, 2), Tile(TileType.DRAGON, 2),  # 发发
        Tile(TileType.DRAGON, 3),  # 中（听牌）
    ]
    hand = Hand(tiles)
    win_tile = Tile(TileType.DRAGON, 3)  # 红中
    
    yaku_detector = YakuDetector(hand, win_tile)
    calculator = ScoreCalculator(hand, win_tile, yaku_detector=yaku_detector)
    
    score = calculator.calculate_score()
    test_result("役满得分32000", score.get("total", 0) >= 32000)


# ==================== Wall 测试 ====================

def test_wall():
    """测试牌山"""
    print("\n=== 测试牌山 ===")
    
    wall = Wall(seed=42)
    
    test_result("牌山初始牌数", wall.remaining_count == 136)
    
    tile = wall.draw()
    test_result("摸牌成功", tile is not None)
    test_result("摸牌后剩余135张", wall.remaining_count == 135)
    
    tiles = wall.draw_multiple(13)
    test_result("摸13张牌", len(tiles) == 13)
    test_result("摸牌后剩余122张", wall.remaining_count == 122)


def test_wall_shuffle():
    """测试牌山洗牌"""
    print("\n=== 测试牌山洗牌 ===")
    
    # 不同种子应该产生不同顺序
    wall1 = Wall(seed=1)
    wall2 = Wall(seed=2)
    
    tile1 = wall1.draw()
    tile2 = wall2.draw()
    
    # 大多数情况下应该不同
    test_result("不同种子产生不同顺序", tile1 != tile2)


# ==================== MahjongGame 测试 ====================

def test_game():
    """测试游戏"""
    print("\n=== 测试游戏 ===")
    
    game = MahjongGame(4)
    game.start_game(seed=42)
    
    test_result("游戏初始化成功", game.remaining_tiles > 0)
    
    # 玩家手牌
    hand = game.get_player_hand(0)
    test_result("玩家0有手牌", hand is not None and len(hand) == 13)
    
    # 摸牌
    tile = game.draw_tile(0)
    test_result("玩家摸牌成功", tile is not None)
    test_result("摸牌后14张", len(game.get_player_hand(0)) == 14)
    
    # 打牌
    success = game.discard_tile(0, tile)
    test_result("打牌成功", success)
    test_result("打牌后13张", len(game.get_player_hand(0)) == 13)


def test_dora():
    """测试宝牌"""
    print("\n=== 测试宝牌 ===")
    
    game = MahjongGame(4)
    game.start_game(seed=42)
    
    dora = game.get_dora_tiles()
    test_result("有宝牌", len(dora) >= 1)


# ==================== 便捷函数测试 ====================

def test_convenience_functions():
    """测试便捷函数"""
    print("\n=== 测试便捷函数 ===")
    
    # create_tile
    tile = create_tile("5m")
    test_result("create_tile 创建5m", tile.tile_type == TileType.MAN and tile.number == 5)
    
    # parse_hand
    hand = parse_hand("123m 456p")
    test_result("parse_hand 创建手牌", len(hand) == 6)
    
    # can_win
    tiles = parse_hand("123m 456m 789m 123p 11s").tiles
    test_result("can_win 检测和牌", can_win(tiles))
    
    # calculate_shanten
    tiles2 = parse_hand("123m 456m 789m 12p 1s").tiles
    shanten = calculate_shanten(tiles2)
    test_result("calculate_shanten 检测向听数", shanten >= 0)
    
    # get_waiting_tiles
    tiles3 = parse_hand("123m 456m 789m 12p 11s").tiles
    waiting = get_waiting_tiles(tiles3)
    test_result("get_waiting_tiles 返回等待牌", len(waiting) >= 1)


# ==================== 边界测试 ====================

def test_edge_cases():
    """边界测试"""
    print("\n=== 边界测试 ===")
    
    # 空手牌
    hand_empty = Hand([])
    test_result("空手牌长度为0", len(hand_empty) == 0)
    
    # 单张牌
    hand_single = Hand([Tile(TileType.MAN, 1)])
    test_result("单张牌长度为1", len(hand_single) == 1)
    
    # 最大牌数（完整手牌+和牌）
    tiles_full = [Tile(TileType.MAN, 1)] * 4 + [Tile(TileType.MAN, 9)] * 4
    hand_full = Hand(tiles_full)
    test_result("满牌手牌长度", len(hand_full) == 8)
    
    # 重复牌处理
    tiles_dup = [Tile(TileType.MAN, 5)] * 5  # 5张相同牌（超过4张）
    try:
        hand_dup = Hand(tiles_dup)
        test_result("重复牌超过4张可创建", True)
    except:
        test_result("重复牌超过4张可创建", False)


def test_invalid_inputs():
    """无效输入测试"""
    print("\n=== 无效输入测试 ===")
    
    # 无效牌号
    try:
        Tile(TileType.MAN, 0)
        test_result("无效牌号0应报错", False)
    except ValueError:
        test_result("无效牌号0应报错", True)
    
    try:
        Tile(TileType.MAN, 15)
        test_result("无效牌号15应报错", False)
    except ValueError:
        test_result("无效牌号15应报错", True)
    
    # 无效字符串
    try:
        Tile.from_string("xm")
        test_result("无效字符串解析应报错", False)
    except ValueError:
        test_result("无效字符串解析应报错", True)


# ==================== 主测试运行 ====================

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("麻将工具库测试")
    print("=" * 50)
    
    # 牌测试
    test_tile_creation()
    test_tile_string()
    test_tile_validation()
    
    # 手牌测试
    test_hand_creation()
    test_hand_string()
    test_hand_sort()
    
    # 和牌检测测试
    test_standard_win()
    test_seven_pairs()
    test_thirteen_orphans()
    test_win_decomposition()
    
    # 效率测试
    test_shanten()
    test_waiting_tiles()
    test_best_discard()
    
    # 役种测试
    test_tanyao()
    test_pinfu()
    test_chiitou()
    test_honitsu()
    test_chinitsu()
    test_toitoi()
    test_yakuman()
    
    # 得分测试
    test_score_calculation()
    test_yakuman_score()
    
    # 牌山测试
    test_wall()
    test_wall_shuffle()
    
    # 游戏测试
    test_game()
    test_dora()
    
    # 便捷函数测试
    test_convenience_functions()
    
    # 边界测试
    test_edge_cases()
    test_invalid_inputs()
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()