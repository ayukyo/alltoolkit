"""
盲文工具使用示例

演示：
1. 基本文本与盲文互转
2. BrailleCell 类的使用
3. 点位与 Unicode 转换
4. 盲文矩阵可视化
5. Grade 2 缩写
6. 音乐盲文
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from braille_utils.mod import (
    BrailleCell, BrailleEncoder, BrailleUtils, BrailleGrade,
    text_to_braille, braille_to_text, dots_to_unicode, unicode_to_dots,
    display_braille, ENGLISH_LETTERS, NUMBERS, PUNCTUATION,
    GRADE2_ABBREVIATIONS, MUSIC_BRAILLE, NUMBER_SIGN, CAPITAL_SIGN
)


def example_basic_conversion():
    """示例1: 基本文本与盲文互转"""
    print("\n" + "=" * 60)
    print("示例1: 基本文本与盲文互转")
    print("=" * 60)
    
    # 简单文本转盲文
    text = "hello"
    braille = text_to_braille(text)
    print(f"\n'{text}' -> '{braille}'")
    
    # 盲文转文本
    decoded = braille_to_text(braille)
    print(f"'{braille}' -> '{decoded}'")
    
    # 包含大写字母
    text2 = "Hello World"
    braille2 = text_to_braille(text2)
    print(f"\n'{text2}' -> '{braille2}'")
    
    # 包含数字
    text3 = "Room 123"
    braille3 = text_to_braille(text3)
    print(f"\n'{text3}' -> '{braille3}'")
    
    # 包含标点
    text4 = "Hello, World!"
    braille4 = text_to_braille(text4)
    print(f"\n'{text4}' -> '{braille4}'")


def example_braille_cell():
    """示例2: BrailleCell 类的使用"""
    print("\n" + "=" * 60)
    print("示例2: BrailleCell 类的使用")
    print("=" * 60)
    
    # 创建盲文单元格
    cell1 = BrailleCell({1, 2, 5})  # 点位 1, 2, 5 -> 'h'
    print(f"\n点位 {{1, 2, 5}} -> {cell1.to_unicode()} (字符 'h')")
    
    # 从 Unicode 创建
    cell2 = BrailleCell.from_unicode('⠁')
    print(f"Unicode '⠁' -> 点位 {cell2.dots} (点位模式: {cell2.to_dots_pattern()})")
    
    # 从点位模式创建
    cell3 = BrailleCell.from_dots_pattern('135')
    print(f"点位模式 '135' -> {cell3.to_unicode()}")
    
    # 获取二进制矩阵
    matrix = cell1.to_binary_matrix()
    print(f"\n点位 {{1, 2, 5}} 的矩阵表示:")
    for row in matrix:
        print(f"  {row}")


def example_dots_unicode_conversion():
    """示例3: 点位与 Unicode 转换"""
    print("\n" + "=" * 60)
    print("示例3: 点位与 Unicode 转换")
    print("=" * 60)
    
    # 点位模式 -> Unicode
    dots_patterns = ['1', '12', '14', '145', '15', '124', '1245', '125']
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    print("\n点位模式转 Unicode:")
    for dots, letter in zip(dots_patterns, letters):
        char = dots_to_unicode(dots)
        print(f"  点位 '{dots}' -> '{char}' (字母 '{letter}')")
    
    # Unicode -> 点位模式
    print("\nUnicode 转点位模式:")
    braille_chars = ['⠁', '⠃', '⠉', '⠙', '⠑', '⠋', '⠛', '⠓']
    for char in braille_chars:
        dots = unicode_to_dots(char)
        print(f"  Unicode '{char}' -> 点位 '{dots}'")


def example_visualization():
    """示例4: 盲文矩阵可视化"""
    print("\n" + "=" * 60)
    print("示例4: 盲文矩阵可视化")
    print("=" * 60)
    
    # 可视化字母 A-H
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    for letter in letters:
        braille = ENGLISH_LETTERS[letter]
        display = display_braille(braille)
        print(f"\n字母 '{letter.upper()}' ({braille}):")
        print(display)
    
    # 空白单元格
    empty = BrailleUtils.create_empty_cell()
    print(f"\n空白单元格 ({empty.to_unicode()}):")
    print(display_braille(empty.to_unicode()))
    
    # 满点单元格
    full = BrailleUtils.create_full_cell()
    print(f"\n满点单元格 ({full.to_unicode()}):")
    print(display_braille(full.to_unicode()))


def example_grade2():
    """示例5: Grade 2 缩写"""
    print("\n" + "=" * 60)
    print("示例5: Grade 2 缩写")
    print("=" * 60)
    
    encoder_g1 = BrailleEncoder(BrailleGrade.GRADE_1)
    encoder_g2 = BrailleEncoder(BrailleGrade.GRADE_2)
    
    words = ['the', 'and', 'for', 'with', 'ing']
    
    print("\nGrade 1 vs Grade 2 编码对比:")
    for word in words:
        g1 = encoder_g1.encode(word)
        g2 = encoder_g2.encode(word)
        print(f"  '{word}': Grade 1 -> '{g1}', Grade 2 -> '{g2}'")


def example_encoder_class():
    """示例6: 使用 BrailleEncoder 类"""
    print("\n" + "=" * 60)
    print("示例6: 使用 BrailleEncoder 类")
    print("=" * 60)
    
    encoder = BrailleEncoder(BrailleGrade.GRADE_1)
    
    # 编码句子
    sentences = [
        "Hello World",
        "The quick brown fox jumps over the lazy dog",
        "2024",
        "Email: test@example.com"
    ]
    
    print("\n句子编码:")
    for sentence in sentences:
        braille = encoder.encode(sentence)
        print(f"\n原文: '{sentence}'")
        print(f"盲文: '{braille}'")
    
    # 解码
    print("\n句子解码:")
    braille_texts = [
        "⠓⠑⠇⠇⠕",
        "⠼⠁⠃⠉",
        "⠠⠺⠕⠗⠇⠙"
    ]
    
    for braille in braille_texts:
        text = encoder.decode(braille)
        print(f"盲文 '{braille}' -> 文本 '{text}'")


def example_special_features():
    """示例7: 特殊功能"""
    print("\n" + "=" * 60)
    print("示例7: 特殊功能")
    print("=" * 60)
    
    # 检测盲文字符
    print("\n检测盲文字符:")
    test_chars = ['⠁', 'a', '⠿', '1']
    for char in test_chars:
        is_braille = BrailleUtils.is_braille_char(char)
        print(f"  '{char}' 是盲文字符: {is_braille}")
    
    # 统计点数
    print("\n统计盲文字符点数:")
    test_brailles = ['⠁', '⠃', '⠓', '⠿', '⠀']
    for braille in test_brailles:
        count = BrailleUtils.count_braille_dots(braille)
        print(f"  '{braille}' 点数: {count}")
    
    # 反转盲文
    print("\n反转盲文:")
    test_cases = ['⠁', '⠃', '⠓', '⠿']
    for braille in test_cases:
        inverted = BrailleUtils.invert_braille(braille)
        print(f"  '{braille}' -> '{inverted}'")
        print(f"    原始: {display_braille(braille)}")
        print(f"    反转: {display_braille(inverted)}")


def example_all_alphabet():
    """示例8: 完整字母表"""
    print("\n" + "=" * 60)
    print("示例8: 完整英文字母表")
    print("=" * 60)
    
    print("\n小写字母:")
    for letter, braille in sorted(ENGLISH_LETTERS.items()):
        dots = unicode_to_dots(braille)
        display = display_braille(braille).replace('●', '●').replace('○', '○')
        print(f"  {letter} -> {braille} (点位 {dots})")
    
    print("\n数字:")
    for digit, braille in sorted(NUMBERS.items()):
        dots = unicode_to_dots(braille)
        print(f"  {digit} -> {NUMBER_SIGN}{braille} (点位 {dots})")


def example_music_braille():
    """示例9: 音乐盲文"""
    print("\n" + "=" * 60)
    print("示例9: 音乐盲文")
    print("=" * 60)
    
    print("\n音符:")
    for note, braille in MUSIC_BRAILLE.items():
        if len(note) == 1:
            print(f"  {note} -> {braille}")
    
    print("\n音符时值:")
    durations = ['whole', 'half', 'quarter', 'eighth', 'rest']
    for duration in durations:
        if duration in MUSIC_BRAILLE:
            print(f"  {duration} -> {MUSIC_BRAILLE[duration]}")


def example_batch_conversion():
    """示例10: 批量转换"""
    print("\n" + "=" * 60)
    print("示例10: 批量转换")
    print("=" * 60)
    
    # 批量文本转盲文
    texts = [
        "Welcome to Braille World!",
        "Learn braille today.",
        "123 Main Street",
        "Call: 555-1234"
    ]
    
    print("\n批量文本转盲文:")
    for text in texts:
        braille = text_to_braille(text)
        print(f"\n原文: {text}")
        print(f"盲文: {braille}")
    
    # 批量盲文转文本
    brailles = [
        "⠓⠑⠇⠇⠕",
        "⠺⠕⠗⠇⠙",
        "⠼⠁⠃⠉⠙⠑"
    ]
    
    print("\n批量盲文转文本:")
    for braille in brailles:
        text = braille_to_text(braille)
        print(f"盲文: {braille} -> 文本: {text}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("      盲文工具使用示例")
    print("=" * 60)
    
    example_basic_conversion()
    example_braille_cell()
    example_dots_unicode_conversion()
    example_visualization()
    example_grade2()
    example_encoder_class()
    example_special_features()
    example_all_alphabet()
    example_music_braille()
    example_batch_conversion()
    
    print("\n" + "=" * 60)
    print("      示例演示完成！")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()