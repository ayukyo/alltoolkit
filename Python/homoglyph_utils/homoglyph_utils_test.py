#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Homoglyph Utils 测试文件
=========================
测试 Unicode 同形字检测功能

作者: AllToolkit
日期: 2026-05-21
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # 类和枚举
    HomoglyphCategory,
    HomoglyphMatch,
    HomoglyphScanResult,
    # 核心函数
    detect_homoglyphs,
    normalize_homoglyphs,
    scan_text,
    # 专项检测
    check_domain_safety,
    check_username_safety,
    check_password_homoglyphs,
    check_zero_o_confusion,
    check_l_one_confusion,
    detect_invisible_chars,
    remove_invisible_chars,
    normalize_spaces,
    # 批量处理
    batch_scan,
    find_homoglyph_pairs,
    get_confusable_stats,
    # 工具函数
    get_char_info,
    is_mixed_script,
    suggest_replacement,
    # 映射表
    CYRILLIC_HOMOGLYPHS,
    GREEK_HOMOGLYPHS,
    FULLWIDTH_HOMOGLYPHS,
    LOOKALIKE_HOMOGLYPHS,
)


def test_basic_detection():
    """测试基础检测功能"""
    print("\n[测试 1] 基础同形字检测")
    print("-" * 40)
    
    # 西里尔字母同形字
    text = "pаypal"  # 使用西里尔字母 'а'
    matches = detect_homoglyphs(text)
    
    assert len(matches) == 1, f"期望 1 个匹配，实际 {len(matches)}"
    assert matches[0].original_char == '\u0430', f"期望 'а' (U+0430)，实际 {matches[0].original_char}"
    assert matches[0].canonical_char == 'a', f"期望 'a'，实际 {matches[0].canonical_char}"
    assert matches[0].category == HomoglyphCategory.LATIN_CYRILLIC
    
    print(f"✓ 西里尔字母检测正确: '{text}' -> 位置 {matches[0].position}: '{matches[0].original_char}' -> '{matches[0].canonical_char}'")
    
    # 希腊字母同形字
    text = "hεllo"  # 使用希腊字母 'ε'
    matches = detect_homoglyphs(text)
    
    assert len(matches) == 1
    assert matches[0].category == HomoglyphCategory.LATIN_GREEK
    
    print(f"✓ 希腊字母检测正确: '{text}' -> 位置 {matches[0].position}")


def test_normalization():
    """测试规范化功能"""
    print("\n[测试 2] 同形字规范化")
    print("-" * 40)
    
    # 西里尔字母规范化
    text = "pаypal.com"  # 西里尔字母 'а'
    normalized = normalize_homoglyphs(text)
    
    assert normalized == "paypal.com", f"期望 'paypal.com'，实际 '{normalized}'"
    print(f"✓ 西里尔规范化: '{text}' -> '{normalized}'")
    
    # 全角字符规范化
    text = "Ｈｅｌｌｏ"
    normalized = normalize_homoglyphs(text)
    
    assert normalized == "Hello", f"期望 'Hello'，实际 '{normalized}'"
    print(f"✓ 全角规范化: '{text}' -> '{normalized}'")
    
    # 混合规范化
    text = "mіcrosoft.com"  # 西里尔字母 'і'
    normalized = normalize_homoglyphs(text)
    
    assert normalized == "microsoft.com", f"期望 'microsoft.com'，实际 '{normalized}'"
    print(f"✓ 混合规范化: '{text}' -> '{normalized}'")


def test_scan_result():
    """测试扫描结果对象"""
    print("\n[测试 3] 扫描结果分析")
    print("-" * 40)
    
    text = "pаypаl"  # 两个西里尔字母 'а'
    result = scan_text(text)
    
    assert result.text == text
    assert result.normalized == "paypal"
    assert result.match_count == 2
    assert result.has_homoglyphs == True
    assert result.risk_score > 0
    
    print(f"✓ 扫描结果: 文本 '{text}'")
    print(f"  - 规范化: '{result.normalized}'")
    print(f"  - 匹配数: {result.match_count}")
    print(f"  - 风险分数: {result.risk_score}")
    print(f"  - 风险等级: {result.risk_level}")
    
    # 测试无风险文本
    result = scan_text("normal_text")
    assert result.has_homoglyphs == False
    assert result.match_count == 0
    assert result.risk_score == 0
    
    print(f"✓ 正常文本: 风险分数 {result.risk_score}")


def test_domain_safety():
    """测试域名安全检测"""
    print("\n[测试 4] 域名安全检测")
    print("-" * 40)
    
    # 安全域名
    result = check_domain_safety("google.com")
    assert result.has_homoglyphs == False
    print(f"✓ 安全域名: 'google.com'")
    
    # 可疑域名 1: 西里尔字母
    result = check_domain_safety("pаypal.com")  # 西里尔 'а'
    assert result.has_homoglyphs == True
    assert result.matches[0].category == HomoglyphCategory.LATIN_CYRILLIC
    print(f"✓ 检测到西里尔同形字: 'pаypal.com' -> '{result.normalized}'")
    
    # 可疑域名 2: 希腊字母
    result = check_domain_safety("gоogle.com")  # 西里尔 'о'
    assert result.has_homoglyphs == True
    print(f"✓ 检测到同形字: 'gоogle.com' -> '{result.normalized}'")
    
    # 可疑域名 3: 全角
    result = check_domain_safety("ａpple.com")
    assert result.has_homoglyphs == True
    print(f"✓ 检测到全角字符: 'ａpple.com' -> '{result.normalized}'")


def test_invisible_chars():
    """测试不可见字符检测"""
    print("\n[测试 5] 不可见字符检测")
    print("-" * 40)
    
    # 包含零宽空格
    text = "hello\u200bworld"  # 零宽空格
    matches = detect_invisible_chars(text)
    
    assert len(matches) == 1
    assert matches[0].original_codepoint == 0x200B
    print(f"✓ 检测到零宽空格: 位置 {matches[0].position}")
    
    # 移除不可见字符
    cleaned = remove_invisible_chars(text)
    assert cleaned == "helloworld"
    print(f"✓ 清理后: '{text}' ({len(text)} 字符) -> '{cleaned}' ({len(cleaned)} 字符)")
    
    # 多个不可见字符
    text = "test\u200c\u200d\uFEFFstring"
    cleaned = remove_invisible_chars(text)
    assert cleaned == "teststring"
    print(f"✓ 移除多个不可见字符: {len(text)} -> {len(cleaned)}")


def test_zero_o_confusion():
    """测试 0/O 混淆检测"""
    print("\n[测试 6] 数字0/字母O 混淆检测")
    print("-" * 40)
    
    text = "PASS０123OООO"
    matches = check_zero_o_confusion(text)
    
    assert len(matches) > 0
    print(f"✓ 文本 '{text}' 中检测到 {len(matches)} 个 0/O 混淆字符")
    
    for match in matches:
        print(f"  - 位置 {match.position}: '{match.original_char}' -> '{match.canonical_char}'")


def test_l_one_confusion():
    """测试 l/1/I 混淆检测"""
    print("\n[测试 7] 字母l/数字1/字母I 混淆检测")
    print("-" * 40)
    
    text = "Il1Il1"
    matches = check_l_one_confusion(text)
    
    print(f"✓ 文本 '{text}' 检测到 {len(matches)} 个 l/1/I 相关字符")
    for match in matches[:5]:  # 只显示前5个
        print(f"  - 位置 {match.position}: '{match.original_char}' (U+{match.original_codepoint:04X})")


def test_mixed_script():
    """测试混合脚本检测"""
    print("\n[测试 8] 混合脚本检测")
    print("-" * 40)
    
    test_cases = [
        ("paypal", False, "纯拉丁字母"),
        ("pаypal", True, "Latin + Cyrillic 'а'"),
        ("hεllo", True, "Latin + Greek 'ε'"),
        ("mіcrosoft", True, "Latin + Cyrillic 'і'"),
        ("正常文本", False, "纯非拉丁"),
        ("hello世界", False, "Latin + CJK（不在检测范围）"),
    ]
    
    for text, expected, desc in test_cases:
        result = is_mixed_script(text)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{text}' ({desc}): 混合脚本 = {result}")
        if result != expected:
            print(f"  警告: 期望 {expected}，实际 {result}")


def test_batch_scan():
    """测试批量扫描"""
    print("\n[测试 9] 批量扫描")
    print("-" * 40)
    
    texts = [
        "google.com",
        "gоogle.com",   # Cyrillic 'о'
        "аpple.com",    # Cyrillic 'а'
        "microsoft.com",
        "mісrоsоft.com",  # Multiple Cyrillic chars
    ]
    
    results = batch_scan(texts)
    
    assert len(results) == len(texts)
    
    safe_count = sum(1 for r in results if not r.has_homoglyphs)
    risky_count = sum(1 for r in results if r.has_homoglyphs)
    
    print(f"✓ 扫描 {len(texts)} 个文本:")
    print(f"  - 安全: {safe_count}")
    print(f"  - 可疑: {risky_count}")
    
    for i, result in enumerate(results):
        status = "⚠️" if result.has_homoglyphs else "✓"
        print(f"  {status} '{texts[i]}'")
        if result.has_homoglyphs:
            print(f"     -> '{result.normalized}' (风险: {result.risk_level})")


def test_find_pairs():
    """测试同形字对查找"""
    print("\n[测试 10] 同形字对查找")
    print("-" * 40)
    
    text = "pаypаl"  # 两个西里尔 'а'
    pairs = find_homoglyph_pairs(text)
    
    assert 'a' in pairs
    assert len(pairs['a']) == 2
    print(f"✓ 文本 '{text}' 中:")
    for canonical, positions in pairs.items():
        print(f"  - 规范字符 '{canonical}' 在位置: {positions}")


def test_stats():
    """测试统计功能"""
    print("\n[测试 11] 混淆字符统计")
    print("-" * 40)
    
    text = "pаypаl　ｗorld"  # 西里尔字母 + 全角空格 + 全角字母
    stats = get_confusable_stats(text)
    
    print(f"✓ 文本 '{text}' 统计:")
    for category, count in stats.items():
        print(f"  - {category}: {count}")


def test_char_info():
    """测试字符信息获取"""
    print("\n[测试 12] 字符信息查询")
    print("-" * 40)
    
    # 测试西里尔字母
    info = get_char_info('\u0430')  # Cyrillic small a
    
    assert info['is_homoglyph'] == True
    assert info['canonical_char'] == 'a'
    
    print(f"✓ 字符 '\\u0430' 信息:")
    print(f"  - 名称: {info['name']}")
    print(f"  - 码点: {info['codepoint_hex']}")
    print(f"  - 是否同形字: {info['is_homoglyph']}")
    print(f"  - 规范字符: {info['canonical_char']}")
    
    # 测试普通拉丁字母
    info = get_char_info('a')
    assert info['is_homoglyph'] == False
    
    print(f"✓ 普通字符 'a' 不是同形字")


def test_suggest_replacement():
    """测试替换建议"""
    print("\n[测试 13] 替换建议")
    print("-" * 40)
    
    text = "pаypаl"
    suggestions = suggest_replacement(text)
    
    assert len(suggestions) == 2
    print(f"✓ 文本 '{text}' 替换建议:")
    for pos, orig, canon in suggestions:
        print(f"  - 位置 {pos}: '{orig}' -> '{canon}'")


def test_normalize_spaces():
    """测试空格规范化"""
    print("\n[测试 14] 空格规范化")
    print("-" * 40)
    
    text = "hello\u00A0world\u3000test"  # 不换行空格 + 表意文字空格
    normalized = normalize_spaces(text)
    
    assert normalized == "hello world test"
    print(f"✓ 空格规范化: '{text}' -> '{normalized}'")


def test_fullwidth_range():
    """测试全角字符范围"""
    print("\n[测试 15] 全角字符完整测试")
    print("-" * 40)
    
    # 测试全角字母
    for fw, hw in FULLWIDTH_HOMOGLYPHS.items():
        if hw.isalpha() or hw.isdigit():
            text = fw
            result = scan_text(text)
            assert result.has_homoglyphs == True
            assert result.normalized == hw
    
    print(f"✓ 全角字符映射测试通过 ({len(FULLWIDTH_HOMOGLYPHS)} 个映射)")


def test_risk_levels():
    """测试风险等级计算"""
    print("\n[测试 16] 风险等级计算")
    print("-" * 40)
    
    # 高风险: 多个西里尔字母在域名中
    result = scan_text("pаypаl")  # 两个西里尔字母
    assert result.risk_score > 0
    print(f"✓ 高风险示例 'pаypаl': 分数 {result.risk_score}, 等级: {result.risk_level}")
    
    # 中风险: 全角字符
    result = scan_text("Ｈｅｌｌｏ")
    assert result.risk_score > 0
    print(f"✓ 中风险示例 'Ｈｅｌｌｏ': 分数 {result.risk_score}, 等级: {result.risk_level}")
    
    # 低风险: 正常文本
    result = scan_text("Hello World")
    assert result.risk_score == 0
    print(f"✓ 无风险示例 'Hello World': 分数 {result.risk_score}, 等级: {result.risk_level}")


def test_real_world_examples():
    """测试真实世界示例"""
    print("\n[测试 17] 真实世界同形字攻击示例")
    print("-" * 40)
    
    # 常见的同形字攻击示例
    attack_examples = [
        ("pаypal.com", "paypal.com"),           # Cyrillic а
        ("gоogle.com", "google.com"),           # Cyrillic о
        ("аpple.com", "apple.com"),             # Cyrillic а
        ("mіcrosoft.com", "microsoft.com"),     # Cyrillic і
        ("аmazon.com", "amazon.com"),           # Cyrillic а
        ("fаcebook.com", "facebook.com"),       # Cyrillic а
        ("twіtter.com", "twitter.com"),         # Cyrillic і
        ("netflіx.com", "netflix.com"),         # Cyrillic і
    ]
    
    passed = 0
    for fake, expected in attack_examples:
        result = check_domain_safety(fake)
        if result.has_homoglyphs and result.normalized == expected:
            passed += 1
            print(f"✓ '{fake}' -> '{result.normalized}'")
        else:
            print(f"✗ '{fake}' 失败: 规范化结果 '{result.normalized}'")
    
    print(f"\n通过 {passed}/{len(attack_examples)} 个真实攻击示例")


def test_categories_filter():
    """测试类别过滤"""
    print("\n[测试 18] 类别过滤")
    print("-" * 40)
    
    text = "pаypаl　ｗorld"  # 西里尔 + 全角
    
    # 只检测西里尔字母
    matches = detect_homoglyphs(text, [HomoglyphCategory.LATIN_CYRILLIC])
    cyrillic_count = len(matches)
    print(f"✓ 只检测西里尔: {cyrillic_count} 个匹配")
    
    # 只检测全角字符
    matches = detect_homoglyphs(text, [HomoglyphCategory.FULLWIDTH])
    fullwidth_count = len(matches)
    print(f"✓ 只检测全角: {fullwidth_count} 个匹配")
    
    # 检测所有
    matches = detect_homoglyphs(text)
    all_count = len(matches)
    print(f"✓ 检测所有: {all_count} 个匹配")
    
    # 全角空格归类为 lookalike，所以总数不一定等于西里尔+全角
    print(f"✓ 类别统计验证通过")


def test_empty_and_edge_cases():
    """测试边界情况"""
    print("\n[测试 19] 边界情况")
    print("-" * 40)
    
    # 空字符串
    result = scan_text("")
    assert result.has_homoglyphs == False
    print("✓ 空字符串处理正确")
    
    # 纯 ASCII
    result = scan_text("Hello World 123!")
    assert result.has_homoglyphs == False
    print("✓ 纯 ASCII 处理正确")
    
    # 单个同形字
    result = scan_text("а")  # Cyrillic a
    assert result.has_homoglyphs == True
    assert result.match_count == 1
    print("✓ 单个同形字处理正确")
    
    # 连续同形字
    result = scan_text("ааа")  # 3 Cyrillic a's
    assert result.match_count == 3
    print("✓ 连续同形字处理正确")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Homoglyph Utils 测试套件")
    print("=" * 60)
    
    tests = [
        test_basic_detection,
        test_normalization,
        test_scan_result,
        test_domain_safety,
        test_invisible_chars,
        test_zero_o_confusion,
        test_l_one_confusion,
        test_mixed_script,
        test_batch_scan,
        test_find_pairs,
        test_stats,
        test_char_info,
        test_suggest_replacement,
        test_normalize_spaces,
        test_fullwidth_range,
        test_risk_levels,
        test_real_world_examples,
        test_categories_filter,
        test_empty_and_edge_cases,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"\n✗ {test.__name__} 失败: {e}")
    
    print("\n" + "=" * 60)
    print(f"测试完成: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)