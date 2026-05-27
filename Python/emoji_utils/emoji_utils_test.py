"""
Emoji Utils 测试文件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Python.emoji_utils.mod import (
    is_emoji,
    extract_emojis,
    remove_emojis,
    count_emojis,
    get_emoji_stats,
    get_emoji_info,
    random_emoji,
    random_emojis,
    emoji_to_code_points,
    code_points_to_emoji,
    categorize_emoji,
    categorize_text_emojis,
    is_emoji_only,
    find_emoji_positions,
    replace_emojis_with_text,
    filter_by_category,
    get_all_emojis_in_category,
    get_common_emoji,
    COMMON_EMOJIS,
)


def test_is_emoji():
    """测试 is_emoji 函数"""
    print("测试 is_emoji...")
    
    # 正向测试
    assert is_emoji('😀') == True, "😀 应该是 emoji"
    assert is_emoji('🎉') == True, "🎉 应该是 emoji"
    assert is_emoji('❤️') == True, "❤️ 应该是 emoji"
    assert is_emoji('👍') == True, "👍 应该是 emoji"
    assert is_emoji('🔥') == True, "🔥 应该是 emoji"
    
    # 反向测试
    assert is_emoji('A') == False, "A 不是 emoji"
    assert is_emoji('1') == False, "1 不是 emoji"
    assert is_emoji('!') == False, "! 不是 emoji"
    assert is_emoji(' ') == False, "空格不是 emoji"
    assert is_emoji('') == False, "空字符串不是 emoji"
    
    print("✅ is_emoji 测试通过")


def test_extract_emojis():
    """测试 extract_emojis 函数"""
    print("测试 extract_emojis...")
    
    # 基础测试
    result = extract_emojis('Hello 😀 World 🎉')
    assert '😀' in result, "应该包含 😀"
    assert '🎉' in result, "应该包含 🎉"
    assert len(result) == 2, f"应该有 2 个 emoji，实际: {len(result)}"
    
    # 无 emoji 测试
    result = extract_emojis('Hello World')
    assert len(result) == 0, "无 emoji 文本应该返回空列表"
    
    # 连续 emoji 测试
    result = extract_emojis('😀😃😄')
    assert len(result) == 3, f"应该有 3 个 emoji，实际: {len(result)}"
    
    # 混合测试
    result = extract_emojis('Test 🚀 Launch! 🎉 Party 🎊')
    assert len(result) == 3, f"应该有 3 个 emoji"
    
    print("✅ extract_emojis 测试通过")


def test_remove_emojis():
    """测试 remove_emojis 函数"""
    print("测试 remove_emojis...")
    
    # 基础移除
    result = remove_emojis('Hello 😀 World 🎉')
    assert '😀' not in result, "应该移除 😀"
    assert '🎉' not in result, "应该移除 🎉"
    
    # 替换测试
    result = remove_emojis('Hello 😀', '[emoji]')
    assert result == 'Hello [emoji]', f"替换失败: {result}"
    
    # 无 emoji
    result = remove_emojis('Hello World')
    assert result == 'Hello World', "无 emoji 文本应该不变"
    
    print("✅ remove_emojis 测试通过")


def test_count_emojis():
    """测试 count_emojis 函数"""
    print("测试 count_emojis...")
    
    assert count_emojis('😀 🎉 🌟') == 3, "应该有 3 个 emoji"
    assert count_emojis('No emoji here') == 0, "应该有 0 个 emoji"
    assert count_emojis('😀😀😀') == 3, "连续 emoji 应该正确计数"
    
    print("✅ count_emojis 测试通过")


def test_get_emoji_stats():
    """测试 get_emoji_stats 函数"""
    print("测试 get_emoji_stats...")
    
    result = get_emoji_stats('😀 👍 😀 👍 🎉')
    assert result.get('😀') == 2, "😀 应该出现 2 次"
    assert result.get('👍') == 2, "👍 应该出现 2 次"
    assert result.get('🎉') == 1, "🎉 应该出现 1 次"
    
    print("✅ get_emoji_stats 测试通过")


def test_get_emoji_info():
    """测试 get_emoji_info 函数"""
    print("测试 get_emoji_info...")
    
    info = get_emoji_info('😀')
    assert info['is_emoji'] == True, "应该是 emoji"
    assert info['code_point'] is not None, "应该有码点"
    assert info['hex'] is not None, "应该有十六进制表示"
    assert 'GRINNING' in info['name'].upper() or 'FACE' in info['name'].upper(), f"名称应包含相关词: {info['name']}"
    
    # 非 emoji 测试
    info = get_emoji_info('A')
    assert info['is_emoji'] == False, "A 不是 emoji"
    
    print("✅ get_emoji_info 测试通过")


def test_random_emoji():
    """测试 random_emoji 函数"""
    print("测试 random_emoji...")
    
    # 随机生成测试
    for _ in range(10):
        emoji = random_emoji()
        assert is_emoji(emoji), f"生成的应该是有效 emoji: {emoji}"
    
    # 分类随机测试
    emoji = random_emoji('smileys')
    assert is_emoji(emoji), f"表情符号应该是有效 emoji: {emoji}"
    
    print("✅ random_emoji 测试通过")


def test_random_emojis():
    """测试 random_emojis 函数"""
    print("测试 random_emojis...")
    
    result = random_emojis(5)
    assert len(result) == 5, f"应该生成 5 个 emoji，实际: {len(result)}"
    
    for emoji in result:
        assert is_emoji(emoji), f"所有生成的都应该是有效 emoji: {emoji}"
    
    print("✅ random_emojis 测试通过")


def test_emoji_to_code_points():
    """测试 emoji_to_code_points 函数"""
    print("测试 emoji_to_code_points...")
    
    result = emoji_to_code_points('😀')
    assert result[0] == 128512, f"😀 的码点应该是 128512，实际: {result[0]}"
    
    # 转换回来
    restored = code_points_to_emoji(result)
    assert restored == '😀', f"转换回来应该是 😀，实际: {restored}"
    
    print("✅ emoji_to_code_points 测试通过")


def test_categorize_emoji():
    """测试 categorize_emoji 函数"""
    print("测试 categorize_emoji...")
    
    cat_key, cat_name = categorize_emoji('😀')
    assert cat_key == 'smileys', f"😀 应该是 smileys 分类，实际: {cat_key}"
    assert '表情' in cat_name, f"分类名称应包含'表情': {cat_name}"
    
    print("✅ categorize_emoji 测试通过")


def test_categorize_text_emojis():
    """测试 categorize_text_emojis 函数"""
    print("测试 categorize_text_emojis...")
    
    result = categorize_text_emojis('😀 🐱 🍕')
    
    # 检查分类存在
    assert len(result) > 0, "应该有分类结果"
    
    print("✅ categorize_text_emojis 测试通过")


def test_is_emoji_only():
    """测试 is_emoji_only 函数"""
    print("测试 is_emoji_only...")
    
    assert is_emoji_only('😀 🎉 🌟') == True, "纯 emoji 文本应该返回 True"
    assert is_emoji_only('😀🎉🌟') == True, "无空格纯 emoji 应该返回 True"
    assert is_emoji_only('Hello 😀') == False, "混合文本应该返回 False"
    assert is_emoji_only('Hello World') == False, "纯文本应该返回 False"
    
    print("✅ is_emoji_only 测试通过")


def test_find_emoji_positions():
    """测试 find_emoji_positions 函数"""
    print("测试 find_emoji_positions...")
    
    result = find_emoji_positions('Hello 😀 World 🎉')
    
    assert len(result) == 2, f"应该找到 2 个位置，实际: {len(result)}"
    
    # 检查位置正确性
    start1, end1, emoji1 = result[0]
    assert emoji1 == '😀', f"第一个 emoji 应该是 😀，实际: {emoji1}"
    
    print("✅ find_emoji_positions 测试通过")


def test_replace_emojis_with_text():
    """测试 replace_emojis_with_text 函数"""
    print("测试 replace_emojis_with_text...")
    
    # 自定义映射
    result = replace_emojis_with_text('Hello 😀', {'😀': '[开心]'})
    assert '[开心]' in result, f"应该包含 '[开心]'，实际: {result}"
    
    # 自动使用 Unicode 名称
    result = replace_emojis_with_text('Test 😀')
    assert 'Test' in result, "应该保留原文本"
    
    print("✅ replace_emojis_with_text 测试通过")


def test_filter_by_category():
    """测试 filter_by_category 函数"""
    print("测试 filter_by_category...")
    
    emojis = ['😀', '🐱', '🍕', '⚽']
    result = filter_by_category(emojis, 'smileys')
    
    assert '😀' in result, "应该包含 😀"
    assert '🐱' not in result, "不应该包含 🐱"
    
    print("✅ filter_by_category 测试通过")


def test_get_all_emojis_in_category():
    """测试 get_all_emojis_in_category 函数"""
    print("测试 get_all_emojis_in_category...")
    
    result = get_all_emojis_in_category('smileys', limit=10)
    
    assert len(result) > 0, "应该返回一些 emoji"
    assert len(result) <= 10, "应该不超过限制"
    
    for emoji in result:
        assert is_emoji(emoji), f"所有返回的都应该是有效 emoji: {emoji}"
    
    print("✅ get_all_emojis_in_category 测试通过")


def test_get_common_emoji():
    """测试 get_common_emoji 函数"""
    print("测试 get_common_emoji...")
    
    assert get_common_emoji('smile') == '😊', "smile 应该返回 😊"
    assert get_common_emoji('love') == '❤️', "love 应该返回 ❤️"
    assert get_common_emoji('fire') == '🔥', "fire 应该返回 🔥"
    assert get_common_emoji('nonexistent') is None, "不存在的名称应该返回 None"
    
    print("✅ get_common_emoji 测试通过")


def test_common_emojis_constant():
    """测试 COMMON_EMOJIS 常量"""
    print("测试 COMMON_EMOJIS...")
    
    assert len(COMMON_EMOJIS) > 0, "COMMON_EMOJIS 应该有内容"
    
    for name, emoji in COMMON_EMOJIS.items():
        assert is_emoji(emoji), f"{name} 的值应该是有效 emoji: {emoji}"
    
    print("✅ COMMON_EMOJIS 测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("🧪 Emoji Utils 测试套件")
    print("="*50 + "\n")
    
    tests = [
        test_is_emoji,
        test_extract_emojis,
        test_remove_emojis,
        test_count_emojis,
        test_get_emoji_stats,
        test_get_emoji_info,
        test_random_emoji,
        test_random_emojis,
        test_emoji_to_code_points,
        test_categorize_emoji,
        test_categorize_text_emojis,
        test_is_emoji_only,
        test_find_emoji_positions,
        test_replace_emojis_with_text,
        test_filter_by_category,
        test_get_all_emojis_in_category,
        test_get_common_emoji,
        test_common_emojis_constant,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} 异常: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"📊 测试结果: {passed} 通过, {failed} 失败")
    print("="*50 + "\n")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)