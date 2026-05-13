"""
Mahjong Utils 使用示例
=====================

展示麻将工具库的主要功能
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mahjong_utils.mod import (
    Tile, TileType, Wind, Dragon, YakuType,
    Hand, WinDetector, YakuDetector, ScoreCalculator,
    TileEfficiency, Wall, MahjongGame,
    parse_hand, create_tile, can_win, calculate_shanten,
    get_waiting_tiles, detect_yaku, calculate_score
)


def example_basic_tiles():
    """示例：基本牌操作"""
    print("\n=== 基本牌操作 ===")
    
    # 创建牌
    man1 = create_tile("1m")  # 一万
    pin5 = create_tile("5p")  # 五筒
    sou9 = create_tile("9s")  # 九索
    
    print(f"万子1: {man1} -> {man1.to_chinese()}")
    print(f"筒子5: {pin5} -> {pin5.to_chinese()}")
    print(f"索子9: {sou9} -> {sou9.to_chinese()}")
    
    # 字牌
    east = create_tile("东")
    green = create_tile("发")
    red = create_tile("中")
    
    print(f"东风: {east} -> {east.to_chinese()}")
    print(f"发财: {green} -> {green.to_chinese()}")
    print(f"红中: {red} -> {red.to_chinese()}")
    
    # 牌属性检查
    print(f"万子1是幺九牌: {man1.is_terminal}")
    print(f"筒子5是中张牌: {pin5.is_simple}")
    print(f"东风是字牌: {east.is_honor}")
    
    # 绿牌检测
    sou2 = create_tile("2s")
    print(f"索子2是绿牌: {sou2.is_green} (可用于绿一色)")


def example_hand_operations():
    """示例：手牌操作"""
    print("\n=== 手牌操作 ===")
    
    # 从字符串创建手牌
    hand = parse_hand("123m 456p 789s 123p 11z")
    print(f"手牌: {hand}")
    print(f"手牌数: {len(hand)}张")
    
    # 排序手牌
    hand.sort()
    print(f"排序后: {hand}")
    
    # 添加和移除牌
    hand.add_tile(create_tile("5m"))
    print(f"添加5m后: {len(hand)}张")
    
    hand.remove_tile(create_tile("5m"))
    print(f"移除5m后: {len(hand)}张")
    
    # 按类型分组
    counts = hand.get_tile_types()
    print(f"万子数: {sum(counts[TileType.MAN].values())}")
    print(f"筒子数: {sum(counts[TileType.PIN].values())}")
    print(f"索子数: {sum(counts[TileType.SOU].values())}")


def example_win_detection():
    """示例：和牌检测"""
    print("\n=== 和牌检测 ===")
    
    # 标准形和牌
    hand1 = parse_hand("123m 456m 789m 123p 11s")
    detector1 = WinDetector(hand1)
    
    print(f"手牌 {hand1}:")
    print(f"  可以和牌: {detector1.can_win()}")
    print(f"  标准形: {detector1.is_standard_win()}")
    
    # 获取分解
    if detector1.can_win():
        decomp = detector1.get_win_decomposition()
        print(f"  分解:")
        for meld in decomp:
            print(f"    {meld.meld_type}: {[str(t) for t in meld.tiles]}")
    
    # 七对子
    hand2 = parse_hand("11223344556677m")
    detector2 = WinDetector(hand2)
    
    print(f"\n手牌 {hand2}:")
    print(f"  七对子: {detector2.is_seven_pairs()}")
    print(f"  可以和牌: {detector2.can_win()}")
    
    # 国士无双
    hand3 = parse_hand("19m19p19s1234z56z7z")
    detector3 = WinDetector(hand3)
    
    print(f"\n手牌 {hand3}:")
    print(f"  国士无双: {detector3.is_thirteen_orphans()}")


def example_shanten_calculation():
    """示例：向听数计算"""
    print("\n=== 向听数计算 ===")
    
    # 和牌形
    hand1 = parse_hand("123m 456m 789m 123p 11s")
    eff1 = TileEfficiency(hand1)
    print(f"手牌 {hand1}: 向听数 = {eff1.get_shanten()} (和牌)")
    
    # 听牌形
    hand2 = parse_hand("123m 456m 789m 123p 1s")
    eff2 = TileEfficiency(hand2)
    print(f"手牌 {hand2}: 向听数 = {eff2.get_shanten()} (听牌)")
    
    # 获取等待牌
    if eff2.get_shanten() == 0:
        waiting = eff2.get_waiting_tiles()
        print(f"  等待牌: {[str(t) for t in waiting]}")
    
    # 一向听
    hand3 = parse_hand("123m 456m 789m 12p 135s")
    eff3 = TileEfficiency(hand3)
    print(f"手牌 {hand3}: 向听数 = {eff3.get_shanten()}")
    
    # 最佳切牌
    best = eff3.find_best_discard()
    if best:
        print(f"  最佳切牌: {best}")
    
    # 进张计算
    ukeire = eff3.calculate_ukeire()
    total_ukeire = sum(ukeire.values())
    print(f"  进张数: {total_ukeire}张")


def example_yaku_detection():
    """示例：役种检测"""
    print("\n=== 役种检测 ===")
    
    # 断幺九
    hand1 = parse_hand("234567m 23456p 234s 22s")
    win_tile1 = create_tile("2s")
    yaku1 = YakuDetector(hand1, win_tile1)
    
    print(f"手牌 {hand1} 和牌 {win_tile1}:")
    for yt, han in yaku1.detect_yaku():
        print(f"  {yt.value}: {han}番")
    
    # 混一色
    hand2 = parse_hand("123456789m 11m 22z")
    win_tile2 = create_tile("2m")
    yaku2 = YakuDetector(hand2, win_tile2)
    
    print(f"\n手牌 {hand2} 和牌 {win_tile2}:")
    for yt, han in yaku2.detect_yaku():
        print(f"  {yt.value}: {han}番")
    print(f"  总番数: {yaku2.calculate_han()}番")
    
    # 立直 + 一发
    hand3 = parse_hand("123m 456m 789m 234p 22s")
    win_tile3 = create_tile("2s")
    yaku3 = YakuDetector(hand3, win_tile3, is_riichi=True, is_ippatsu=True, is_tsumo=True)
    
    print(f"\n手牌 {hand3} 和牌 {win_tile3} (立直+一发+自摸):")
    for yt, han in yaku3.detect_yaku():
        print(f"  {yt.value}: {han}番")
    
    # 役满 - 字一色
    hand4 = parse_hand("11223344556677z")
    win_tile4 = create_tile("7z")  # 北
    yaku4 = YakuDetector(hand4, win_tile4)
    
    print(f"\n手牌 {hand4} 和牌 {win_tile4}:")
    print(f"  是否役满: {yaku4.is_yakuman()}")
    for yt, han in yaku4.detect_yaku():
        print(f"  {yt.value}: 役满×{han}")


def example_score_calculation():
    """示例：得分计算"""
    print("\n=== 得分计算 ===")
    
    # 闲家荣和
    hand1 = parse_hand("123m 456m 789m 234p 22s")
    win_tile1 = create_tile("2s")
    yaku1 = YakuDetector(hand1, win_tile1)
    score1 = ScoreCalculator(hand1, win_tile1, yaku_detector=yaku1, is_dealer=False)
    
    print(f"闲家荣和:")
    print(f"  符数: {score1.calculate_fu()}")
    print(f"  得分: {score1.calculate_score()}")
    
    # 庄家自摸
    hand2 = parse_hand("11223344556677m")
    win_tile2 = create_tile("7m")
    yaku2 = YakuDetector(hand2, win_tile2, is_tsumo=True)
    score2 = ScoreCalculator(hand2, win_tile2, is_tsumo=True, is_dealer=True, yaku_detector=yaku2)
    
    print(f"\n庄家自摸七对子:")
    print(f"  得分: {score2.calculate_score()}")
    
    # 役满得分
    hand3 = parse_hand("11223344556677z")
    win_tile3 = create_tile("7z")
    yaku3 = YakuDetector(hand3, win_tile3)
    score3 = ScoreCalculator(hand3, win_tile3, yaku_detector=yaku3)
    
    print(f"\n字一色役满:")
    print(f"  得分: {score3.calculate_score()}")


def example_wall_and_game():
    """示例：牌山和游戏"""
    print("\n=== 牌山和游戏 ===")
    
    # 创建牌山
    wall = Wall(seed=42)
    print(f"牌山初始牌数: {wall.remaining_count}")
    
    # 模拟摸牌
    tiles = wall.draw_multiple(13)
    print(f"摸13张牌: {[str(t) for t in tiles]}")
    print(f"剩余牌数: {wall.remaining_count}")
    
    # 创建游戏
    game = MahjongGame(4)
    game.start_game(seed=42)
    
    print(f"\n游戏状态:")
    print(f"  剩余牌数: {game.remaining_tiles}")
    
    for i in range(4):
        hand = game.get_player_hand(i)
        print(f"  玩家{i}手牌: {hand}")
    
    # 宝牌
    dora = game.get_dora_tiles()
    print(f"  宝牌: {[str(t) for t in dora]}")


def example_special_cases():
    """示例：特殊情况"""
    print("\n=== 特殊情况 ===")
    
    # 九莲宝灯（清一色的特殊形）
    hand1 = parse_hand("1112345678999m")
    detector1 = WinDetector(hand1)
    print(f"九莲宝灯形 {hand1}:")
    print(f"  可以和牌: {detector1.can_win()}")
    
    # 绿一色
    hand2 = parse_hand("222333444666888s 2d")
    detector2 = WinDetector(hand2)
    yaku2 = YakuDetector(hand2, create_tile("2d"))
    print(f"\n绿一色 {hand2}:")
    print(f"  可以和牌: {detector2.can_win()}")
    print(f"  是否役满: {yaku2.is_yakuman()}")


def example_convenience_functions():
    """示例：便捷函数"""
    print("\n=== 便捷函数 ===")
    
    # 快速和牌检测
    tiles = parse_hand("123m 456m 789m 123p 11s").tiles
    print(f"can_win: {can_win(tiles)}")
    
    # 快速向听数计算
    tiles2 = parse_hand("123m 456m 789m 12p 1s").tiles
    print(f"calculate_shanten: {calculate_shanten(tiles2)}")
    
    # 快速等待牌获取
    tiles3 = parse_hand("123m 456m 789m 12p 11s").tiles
    waiting = get_waiting_tiles(tiles3)
    print(f"get_waiting_tiles: {[str(t) for t in waiting]}")
    
    # 快速役种检测
    tiles4 = parse_hand("234567m 23456p 234s 22s").tiles
    win_tile = create_tile("2s")
    yaku = detect_yaku(tiles4, win_tile)
    print(f"detect_yaku: {[yt.value for yt, _ in yaku]}")
    
    # 快速得分计算
    score = calculate_score(tiles4, win_tile)
    print(f"calculate_score: {score}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("麻将工具库使用示例")
    print("=" * 60)
    
    example_basic_tiles()
    example_hand_operations()
    example_win_detection()
    example_shanten_calculation()
    example_yaku_detection()
    example_score_calculation()
    example_wall_and_game()
    example_special_cases()
    example_convenience_functions()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()