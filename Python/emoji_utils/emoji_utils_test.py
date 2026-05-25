"""
emoji_utils 测试模块

测试所有核心功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    EmojiUtils,
    detect_emojis,
    remove_emojis,
    count_emojis,
    get_emoji_info,
    separate_text_emoji,
    text_to_emoji,
    emoji_density,
    is_only_emojis
)


def test_is_emoji():
    """测试单个字符是否为 emoji"""
    print("测试 is_emoji...")
    
    # 正向测试
    assert EmojiUtils.is_emoji('😊') == True, "笑脸 emoji 应该被识别"
    assert EmojiUtils.is_emoji('❤') == True, "心形 emoji 应该被识别"
    assert EmojiUtils.is_emoji('⭐') == True, "星星 emoji 应该被识别"
    assert EmojiUtils.is_emoji('🎉') == True, "庆祝 emoji 应该被识别"
    assert EmojiUtils.is_emoji('🐱') == True, "猫 emoji 应该被识别"
    assert EmojiUtils.is_emoji('🍕') == True, "披萨 emoji 应该被识别"
    
    # 负向测试
    assert EmojiUtils.is_emoji('a') == False, "字母 a 不是 emoji"
    assert EmojiUtils.is_emoji('中') == False, "汉字不是 emoji"
    assert EmojiUtils.is_emoji('1') == False, "数字不是 emoji"
    assert EmojiUtils.is_emoji(' ') == False, "空格不是 emoji"
    
    print("✓ is_emoji 测试通过")


def test_detect_emojis():
    """测试检测文本中的 emoji"""
    print("\n测试 detect_emojis...")
    
    # 基础测试
    text1 = "你好 😊 今天天气很好 ☀️"
    emojis1 = detect_emojis(text1)
    assert '😊' in emojis1, "应该检测到笑脸"
    assert '☀️' in emojis1 or '☀' in emojis1, "应该检测到太阳"
    
    # 多个 emoji
    text2 = "🎉🎊🎈🎂🎁"
    emojis2 = detect_emojis(text2)
    assert len(emojis2) >= 4, f"应该检测到至少 4 个 emoji，实际检测到 {len(emojis2)}"
    
    # 无 emoji
    text3 = "这是一段没有表情的普通文本"
    emojis3 = detect_emojis(text3)
    assert len(emojis3) == 0, "普通文本不应检测到 emoji"
    
    # 组合 emoji（如肤色修饰）
    text4 = "👍🏻👍🏼👍🏽👍🏾👍🏿"
    emojis4 = detect_emojis(text4)
    assert len(emojis4) >= 1, "应该检测到手势 emoji"
    
    print("✓ detect_emojis 测试通过")


def test_remove_emojis():
    """测试移除 emoji"""
    print("\n测试 remove_emojis...")
    
    # 基础移除
    text1 = "你好 😊 世界"
    result1 = remove_emojis(text1)
    assert '😊' not in result1, "emoji 应该被移除"
    assert '你好' in result1 and '世界' in result1, "文本应该保留"
    
    # 替换为其他字符
    text2 = "开心 😊"
    result2 = remove_emojis(text2, replacement='[表情]')
    assert '[表情]' in result2, "应该使用替换文本"
    
    # 只有 emoji
    text3 = "🎉🎊🎈"
    result3 = remove_emojis(text3)
    assert result3.strip() == '', "只有 emoji 时应该得到空字符串"
    
    print("✓ remove_emojis 测试通过")


def test_count_emojis():
    """测试统计 emoji"""
    print("\n测试 count_emojis...")
    
    text = "😊 你好 😊 世界 😊 🎉🎉"
    counts = count_emojis(text)
    
    assert counts.get('😊', 0) == 3, f"笑脸应该出现 3 次，实际 {counts.get('😊', 0)}"
    assert counts.get('🎉', 0) == 2, f"庆祝应该出现 2 次，实际 {counts.get('🎉', 0)}"
    
    print("✓ count_emojis 测试通过")


def test_get_emoji_info():
    """测试获取 emoji 信息"""
    print("\n测试 get_emoji_info...")
    
    info = get_emoji_info('😊')
    assert info['emoji'] == '😊', "应该返回正确的 emoji"
    assert 'unicode' in info, "应该包含 unicode 信息"
    assert 'name' in info, "应该包含名称"
    assert 'category' in info, "应该包含分类"
    
    # 检查分类
    assert info['category'] in EmojiUtils.EMOJI_CATEGORIES.keys() or info['category'] == 'unknown', \
        "分类应该是有效的"
    
    print("✓ get_emoji_info 测试通过")


def test_separate_text_emoji():
    """测试分离文本和 emoji"""
    print("\n测试 separate_text_emoji...")
    
    text = "今天天气真好 😊☀️ 去公园玩吧 🎉"
    pure_text, emojis = separate_text_emoji(text)
    
    assert '😊' not in pure_text, "纯文本不应包含 emoji"
    assert '☀️' not in pure_text and '☀' not in pure_text, "纯文本不应包含 emoji"
    assert '🎉' not in pure_text, "纯文本不应包含 emoji"
    assert '今天天气真好' in pure_text, "应该保留文本内容"
    assert '去公园玩吧' in pure_text, "应该保留文本内容"
    
    assert len(emojis) >= 2, f"应该检测到至少 2 个不同的 emoji，实际 {len(emojis)}"
    
    print("✓ separate_text_emoji 测试通过")


def test_text_to_emoji():
    """测试文本转 emoji"""
    print("\n测试 text_to_emoji...")
    
    # 基础转换
    result1 = text_to_emoji("I am happy and love you")
    assert '😊' in result1 or 'happy' in result1.lower(), "应该转换 happy"
    assert '❤️' in result1 or 'love' in result1.lower() or '❤' in result1, "应该转换 love"
    
    # 保留未匹配
    result2 = text_to_emoji("hello world", keep_unmatched=True)
    assert 'hello' in result2 or 'world' in result2, "应该保留未匹配的文本"
    
    print("✓ text_to_emoji 测试通过")


def test_emoji_density():
    """测试 emoji 密度计算"""
    print("\n测试 emoji_density...")
    
    # 高密度
    text1 = "🎉🎉🎉🎉"
    density1 = emoji_density(text1)
    assert density1 > 0, "应该有正密度"
    
    # 低密度
    text2 = "这是一段很长的文本内容"
    density2 = emoji_density(text2)
    assert density2 == 0, "没有 emoji 应该密度为 0"
    
    # 混合
    text3 = "😊ab"
    density3 = emoji_density(text3)
    assert 0 < density3 < 1, "混合文本密度应在 0-1 之间"
    
    print("✓ emoji_density 测试通过")


def test_is_only_emojis():
    """测试是否仅包含 emoji"""
    print("\n测试 is_only_emojis...")
    
    # 只有 emoji
    assert is_only_emojis("😊🎉🌟") == True, "只有 emoji 应该返回 True"
    
    # emoji 和文本
    assert is_only_emojis("你好 😊") == False, "包含文本应该返回 False"
    
    # 纯文本
    assert is_only_emojis("这是纯文本") == False, "纯文本应该返回 False"
    
    # 空字符串
    assert is_only_emojis("") == True, "空字符串视为只包含 emoji（无其他内容）"
    
    print("✓ is_only_emojis 测试通过")


def test_extract_emoji_positions():
    """测试提取 emoji 位置"""
    print("\n测试 extract_emoji_positions...")
    
    text = "a😊b🎉c"
    positions = EmojiUtils.extract_emoji_positions(text)
    
    assert len(positions) == 2, f"应该检测到 2 个 emoji，实际 {len(positions)}"
    
    # 检查第一个 emoji 位置
    emoji1, start1, end1 = positions[0]
    assert emoji1 == '😊', f"第一个 emoji 应该是 😊，实际 {emoji1}"
    assert start1 == 1, f"开始位置应该是 1，实际 {start1}"
    assert end1 == 2, f"结束位置应该是 2，实际 {end1}"
    
    print("✓ extract_emoji_positions 测试通过")


def test_categorize_emojis():
    """测试 emoji 分类"""
    print("\n测试 categorize_emojis...")
    
    emojis = ['😊', '🐱', '🍕', '⚽', '❤️', '🚗']
    categories = EmojiUtils.categorize_emojis(emojis)
    
    # 至少应该能分类出一些
    assert len(categories) > 0, "应该能分类出一些 emoji"
    
    print("✓ categorize_emojis 测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("emoji_utils 测试套件")
    print("=" * 50)
    
    try:
        test_is_emoji()
        test_detect_emojis()
        test_remove_emojis()
        test_count_emojis()
        test_get_emoji_info()
        test_separate_text_emoji()
        test_text_to_emoji()
        test_emoji_density()
        test_is_only_emojis()
        test_extract_emoji_positions()
        test_categorize_emojis()
        
        print("\n" + "=" * 50)
        print("✅ 所有测试通过！")
        print("=" * 50)
        return True
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)