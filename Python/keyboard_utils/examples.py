#!/usr/bin/env python3
"""
Keyboard Utils Examples - 键盘布局工具示例

展示键盘工具的各种用法：
1. 基础布局查询
2. 距离计算
3. 打字分析
4. 效率评分
5. 键盘模式检测
6. 布局比较
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    KeyboardUtils, Finger, Hand,
    distance, total_distance, analyze, get_key_position, get_coordinates,
    get_finger, get_hand, efficiency_score, get_keyboard_patterns,
    suggest_improvements, available_layouts
)


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print('=' * 60)


def example_basic_queries():
    """示例：基础布局查询"""
    print_section("基础布局查询")
    
    ku = KeyboardUtils("qwerty")
    
    # 查询按键位置
    print("\n按键位置信息：")
    for char in ['a', 's', 'd', 'f', 'j', 'k', 'l']:
        pos = ku.layout.get_key_position(char)
        if pos:
            print(f"  '{char}': 行={pos.row}, 列={pos.col}, "
                  f"手指={pos.finger.value}, 手={pos.hand.value}")
    
    # 查询坐标
    print("\n按键坐标：")
    for char in ['a', 'b', 'c']:
        coords = ku.layout.get_coordinates(char)
        if coords:
            print(f"  '{char}': x={coords[0]:.2f}, y={coords[1]:.2f}")
    
    # 获取手指和手
    print("\n手指分配：")
    test_chars = 'asdfjkl;'
    for char in test_chars:
        finger = get_finger(char)
        hand = get_hand(char)
        print(f"  '{char}': {finger.value if finger else 'N/A'} ({hand.value if hand else 'N/A'})")


def example_distance_calculation():
    """示例：距离计算"""
    print_section("距离计算")
    
    ku = KeyboardUtils("qwerty")
    
    # 两键距离
    print("\n两键距离（键宽单位）：")
    pairs = [('a', 's'), ('a', 'f'), ('a', 'j'), ('a', 'p'), ('q', 'p')]
    for c1, c2 in pairs:
        dist = ku.distance(c1, c2)
        print(f"  '{c1}' → '{c2}': {dist:.2f}")
    
    # 总行程距离
    print("\n文本总行程距离：")
    texts = ["hello", "asdf", "the", "qwerty", "python"]
    for text in texts:
        dist = ku.total_distance(text)
        avg = dist / len(text) if text else 0
        print(f"  '{text}': 总距离={dist:.2f}, 平均={avg:.2f}")


def example_typing_analysis():
    """示例：打字分析"""
    print_section("打字分析")
    
    ku = KeyboardUtils("qwerty")
    
    # 分析文本
    text = "the quick brown fox jumps over the lazy dog"
    analysis = ku.analyze(text)
    
    print(f"\n文本: '{text}'")
    print(f"  字符数: {len(text)}")
    print(f"  总距离: {analysis.total_distance:.2f} 键宽")
    print(f"  平均距离: {analysis.average_distance:.2f} 键宽")
    print(f"  手交替次数: {analysis.hand_alternations}")
    print(f"  同手连续次数: {analysis.same_hand_sequences}")
    print(f"  滚动序列数: {analysis.rolling_sequences}")
    
    print("\n行使用分布：")
    print(f"  数字行: {analysis.number_row_usage}")
    print(f"  上行: {analysis.top_row_usage}")
    print(f"  基准行: {analysis.home_row_usage}")
    print(f"  下行: {analysis.bottom_row_usage}")
    
    print("\n手使用分布：")
    print(f"  左手: {analysis.hand_usage.get(Hand.LEFT, 0)}")
    print(f"  右手: {analysis.hand_usage.get(Hand.RIGHT, 0)}")
    
    print("\n手指使用分布：")
    for finger in [Finger.LEFT_PINKY, Finger.LEFT_RING, Finger.LEFT_MIDDLE, Finger.LEFT_INDEX,
                   Finger.RIGHT_INDEX, Finger.RIGHT_MIDDLE, Finger.RIGHT_RING, Finger.RIGHT_PINKY]:
        count = analysis.finger_usage.get(finger, 0)
        print(f"  {finger.value}: {count}")


def example_efficiency_scoring():
    """示例：效率评分"""
    print_section("效率评分")
    
    ku = KeyboardUtils("qwerty")
    
    # 比较不同文本的效率
    texts = [
        ("asdfjkl;", "基准行序列"),
        ("qazwsx", "跳跃序列"),
        ("stressed", "英文单词"),
        ("1234567890", "数字序列"),
        ("the and for", "常用词"),
    ]
    
    print("\n文本效率评分（0-100分）：")
    for text, desc in texts:
        score = ku.get_efficiency_score(text)
        print(f"  '{text}' ({desc}): {score:.1f}分")


def example_pattern_detection():
    """示例：键盘模式检测"""
    print_section("键盘模式检测")
    
    ku = KeyboardUtils("qwerty")
    
    # 检测模式
    texts = ["asd", "aq", "qwer", "zxc"]
    
    for text in texts:
        print(f"\n文本: '{text}'")
        patterns = ku.get_keyboard_patterns(text)
        
        if patterns:
            for p in patterns:
                print(f"  - {p['type']}: '{p['chars']}' (位置 {p['start']}-{p['end']})")
        else:
            print("  无检测到模式")


def example_improvement_suggestions():
    """示例：改进建议"""
    print_section("改进建议")
    
    ku = KeyboardUtils("qwerty")
    
    # 分析并给出建议
    texts = ["password", "qwerty", "azerty"]
    
    for text in texts:
        print(f"\n文本: '{text}'")
        suggestions = ku.suggest_alternatives(text)
        
        if suggestions:
            for s in suggestions[:5]:  # 最多显示5条
                print(f"  - 位置 {s['position']}: {s['message']}")
        else:
            print("  无改进建议")


def example_layout_comparison():
    """示例：布局比较"""
    print_section("布局比较")
    
    layouts = ["qwerty", "dvorak", "colemak"]
    text = "the quick brown fox jumps over the lazy dog"
    
    print(f"\n比较文本: '{text}'")
    print("\n布局对比：")
    
    results = []
    for layout_name in layouts:
        ku = KeyboardUtils(layout_name)
        analysis = ku.analyze(text)
        score = ku.get_efficiency_score(text)
        
        results.append({
            "layout": layout_name,
            "distance": analysis.total_distance,
            "avg_distance": analysis.average_distance,
            "home_row": analysis.home_row_usage,
            "alternations": analysis.hand_alternations,
            "score": score
        })
    
    # 打印结果
    print(f"\n{'布局':<10} {'总距离':<10} {'平均距离':<10} {'基准行':<8} {'交替':<8} {'评分':<8}")
    print("-" * 60)
    for r in results:
        print(f"{r['layout']:<10} {r['distance']:<10.1f} {r['avg_distance']:<10.2f} "
              f"{r['home_row']:<8} {r['alternations']:<8} {r['score']:<8.1f}")
    
    # 找出最佳布局
    best = max(results, key=lambda x: x["score"])
    print(f"\n最高效布局: {best['layout']} (评分: {best['score']:.1f})")


def example_layout_specifics():
    """示例：布局特性"""
    print_section("布局特性")
    
    # QWERTY
    print("\nQWERTY 布局:")
    ku_qwerty = KeyboardUtils("qwerty")
    print(f"  基准行: asdfghjkl;")
    for c in "asdfjkl;":
        finger = ku_qwerty.layout.get_finger(c)
        print(f"    '{c}': {finger.value if finger else 'N/A'}")
    
    # Dvorak
    print("\nDvorak 布局:")
    ku_dvorak = KeyboardUtils("dvorak")
    print(f"  基准行: aoeuidhtns")
    for c in "aoeuidhtns":
        finger = ku_dvorak.layout.get_finger(c)
        print(f"    '{c}': {finger.value if finger else 'N/A'}")
    
    # Colemak
    print("\nColemak 布局:")
    ku_colemak = KeyboardUtils("colemak")
    print(f"  基准行: arstdhneio")
    for c in "arstdhneio":
        finger = ku_colemak.layout.get_finger(c)
        print(f"    '{c}': {finger.value if finger else 'N/A'}")


def example_row_analysis():
    """示例：行使用分析"""
    print_section("行使用分析")
    
    ku = KeyboardUtils("qwerty")
    
    # 分析不同类型的文本
    texts = [
        ("hello world", "英文文本"),
        ("123 + 456 = 579", "数学表达式"),
        ("asdf jkl;", "基准行"),
        ("qwer uiop", "上行"),
        ("zxcv nm,.", "下行"),
    ]
    
    print("\n不同文本的行使用分布：")
    for text, desc in texts:
        analysis = ku.analyze(text)
        total = analysis.number_row_usage + analysis.top_row_usage + \
                analysis.home_row_usage + analysis.bottom_row_usage
        if total > 0:
            print(f"\n  '{text}' ({desc}):")
            print(f"    数字行: {analysis.number_row_usage} ({analysis.number_row_usage/total*100:.1f}%)")
            print(f"    上行: {analysis.top_row_usage} ({analysis.top_row_usage/total*100:.1f}%)")
            print(f"    基准行: {analysis.home_row_usage} ({analysis.home_row_usage/total*100:.1f}%)")
            print(f"    下行: {analysis.bottom_row_usage} ({analysis.bottom_row_usage/total*100:.1f}%)")


def example_finger_workload():
    """示例：手指工作负荷分析"""
    print_section("手指工作负荷分析")
    
    ku = KeyboardUtils("qwerty")
    
    text = "the quick brown fox jumps over the lazy dog"
    analysis = ku.analyze(text)
    
    print(f"\n文本: '{text}'")
    print("\n各手指工作负荷：")
    
    # 左手
    print("\n  左手：")
    left_fingers = [Finger.LEFT_PINKY, Finger.LEFT_RING, Finger.LEFT_MIDDLE, Finger.LEFT_INDEX]
    for finger in left_fingers:
        count = analysis.finger_usage.get(finger, 0)
        bar = "█" * (count // 2)
        print(f"    {finger.value.replace('left_', '').upper():<6}: {count:2d} {bar}")
    
    # 右手
    print("\n  右手：")
    right_fingers = [Finger.RIGHT_INDEX, Finger.RIGHT_MIDDLE, Finger.RIGHT_RING, Finger.RIGHT_PINKY]
    for finger in right_fingers:
        count = analysis.finger_usage.get(finger, 0)
        bar = "█" * (count // 2)
        print(f"    {finger.value.replace('right_', '').upper():<6}: {count:2d} {bar}")
    
    # 左右手对比
    left_total = analysis.hand_usage.get(Hand.LEFT, 0)
    right_total = analysis.hand_usage.get(Hand.RIGHT, 0)
    total = left_total + right_total
    
    print(f"\n  左右手对比：")
    print(f"    左手: {left_total} ({left_total/total*100:.1f}%)")
    print(f"    右手: {right_total} ({right_total/total*100:.1f}%)")


def example_password_analysis():
    """示例：密码键盘分析"""
    print_section("密码键盘分析")
    
    ku = KeyboardUtils("qwerty")
    
    passwords = [
        "password",
        "qwerty123",
        "asdfjkl;",
        "ZaXsCdVf",
        "P@ssw0rd!",
    ]
    
    print("\n密码键盘特征分析：")
    for pwd in passwords:
        analysis = ku.analyze(pwd)
        patterns = ku.get_keyboard_patterns(pwd)
        score = ku.get_efficiency_score(pwd)
        
        consecutive = len([p for p in patterns if p["type"] == "consecutive"])
        same_finger = len([p for p in patterns if p["type"] == "same_finger"])
        
        print(f"\n  '{pwd}':")
        print(f"    效率评分: {score:.1f}")
        print(f"    总距离: {analysis.total_distance:.1f}")
        print(f"    连续键模式: {consecutive}")
        print(f"    同指序列: {same_finger}")
        print(f"    手交替: {analysis.hand_alternations}")


def main():
    """主函数"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         Keyboard Utils - 键盘布局工具示例                 ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    print(f"\n可用布局: {', '.join(available_layouts())}")
    
    example_basic_queries()
    example_distance_calculation()
    example_typing_analysis()
    example_efficiency_scoring()
    example_pattern_detection()
    example_improvement_suggestions()
    example_layout_comparison()
    example_layout_specifics()
    example_row_analysis()
    example_finger_workload()
    example_password_analysis()
    
    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()