"""
Emoji Utils 使用示例
演示各种功能的实际应用场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from Python.emoji_utils.mod import (
    is_emoji,
    extract_emojis,
    remove_emojis,
    count_emojis,
    get_emoji_stats,
    get_emoji_info,
    random_emoji,
    random_emojis,
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


def example_basic_usage():
    """基础用法示例"""
    print("\n" + "="*50)
    print("📌 基础用法示例")
    print("="*50)
    
    text = "Hello 😀 World! 🎉 今天心情 😊 很好! 🚀"
    
    # 1. 判断是否为 Emoji
    print(f"\n1. 判断是否为 Emoji:")
    print(f"   '😀' 是 emoji: {is_emoji('😀')}")
    print(f"   'A' 是 emoji: {is_emoji('A')}")
    
    # 2. 提取文本中的 Emoji
    print(f"\n2. 提取 Emoji:")
    emojis = extract_emojis(text)
    print(f"   原文: {text}")
    print(f"   提取: {emojis}")
    
    # 3. 统计 Emoji 数量
    print(f"\n3. 统计数量:")
    print(f"   Emoji 数量: {count_emojis(text)}")
    
    # 4. 统计频率
    print(f"\n4. 频率统计:")
    stats = get_emoji_stats("😀 👍 😀 🎉 👍 😀")
    print(f"   频率: {stats}")


def example_remove_replace():
    """移除和替换示例"""
    print("\n" + "="*50)
    print("🔧 移除和替换示例")
    print("="*50)
    
    text = "Hello 😀 World 🎉 Test 🌟"
    
    # 移除所有 Emoji
    print(f"\n1. 移除所有 Emoji:")
    print(f"   原文: {text}")
    print(f"   移除后: {remove_emojis(text)}")
    
    # 替换为占位符
    print(f"\n2. 替换为占位符:")
    print(f"   替换后: {remove_emojis(text, '[图片]')}")
    
    # 替换为文本描述
    print(f"\n3. 替换为文本描述:")
    emoji_map = {'😀': '[开心]', '🎉': '[庆祝]', '🌟': '[星星]'}
    print(f"   替换后: {replace_emojis_with_text(text, emoji_map)}")


def example_emoji_info():
    """获取 Emoji 信息示例"""
    print("\n" + "="*50)
    print("ℹ️ Emoji 信息示例")
    print("="*50)
    
    emojis = ['😀', '🎉', '🐱', '🍕']
    
    for emoji in emojis:
        info = get_emoji_info(emoji)
        cat_key, cat_name = categorize_emoji(emoji)
        print(f"\n   {emoji}")
        print(f"   - 码点: {info['hex']} ({info['code_point']})")
        print(f"   - Unicode名称: {info['name']}")
        print(f"   - Emoji分类: {cat_name} ({cat_key})")


def example_random_generation():
    """随机生成示例"""
    print("\n" + "="*50)
    print("🎲 随机生成示例")
    print("="*50)
    
    # 随机单个 Emoji
    print(f"\n1. 随机 Emoji:")
    for _ in range(5):
        print(f"   {random_emoji()}", end=" ")
    print()
    
    # 按分类随机
    print(f"\n2. 表情符号分类随机:")
    for _ in range(5):
        print(f"   {random_emoji('smileys')}", end=" ")
    print()
    
    # 批量随机
    print(f"\n3. 批量随机 (10个):")
    print(f"   {' '.join(random_emojis(10))}")


def example_text_analysis():
    """文本分析示例"""
    print("\n" + "="*50)
    print("📊 文本分析示例")
    print("="*50)
    
    text = "今天的天气真好 🌞 适合出去玩 🎈 和朋友聚会 🎉 真开心 😊"
    
    # 判断是否纯 Emoji
    print(f"\n1. 是否纯 Emoji 文本:")
    print(f"   '{text}'")
    print(f"   纯Emoji: {is_emoji_only(text)}")
    print(f"   '😀 🎉 🌟' 纯Emoji: {is_emoji_only('😀 🎉 🌟')}")
    
    # 找出位置
    print(f"\n2. Emoji 位置:")
    positions = find_emoji_positions(text)
    print(f"   原文: {text}")
    for start, end, emoji in positions:
        print(f"   位置 {start}-{end}: {emoji}")
    
    # 按分类统计
    print(f"\n3. 分类统计:")
    categorized = categorize_text_emojis(text)
    for cat, emojis in categorized.items():
        print(f"   {cat}: {emojis}")


def example_filtering():
    """筛选示例"""
    print("\n" + "="*50)
    print("🔍 筛选示例")
    print("="*50)
    
    # 获取指定分类的 Emoji
    print(f"\n1. 表情符号分类前10个:")
    smileys = get_all_emojis_in_category('smileys', limit=10)
    print(f"   {' '.join(smileys)}")
    
    # 从列表中筛选
    print(f"\n2. 从混合列表中筛选:")
    mixed = ['😀', '🐱', '🍕', '⚽', '😊', '🐶', '🍔', '🏀']
    filtered = filter_by_category(mixed, 'smileys')
    print(f"   原始: {' '.join(mixed)}")
    print(f"   表情符号: {' '.join(filtered)}")


def example_common_emojis():
    """常用 Emoji 示例"""
    print("\n" + "="*50)
    print("⭐ 常用 Emoji 示例")
    print("="*50)
    
    # 使用预定义的常用 Emoji
    print(f"\n1. 预定义常用 Emoji:")
    print(f"   smile: {get_common_emoji('smile')}")
    print(f"   love: {get_common_emoji('love')}")
    print(f"   fire: {get_common_emoji('fire')}")
    print(f"   rocket: {get_common_emoji('rocket')}")
    
    # 打印所有常用 Emoji
    print(f"\n2. 所有常用 Emoji:")
    for name, emoji in list(COMMON_EMOJIS.items())[:10]:
        print(f"   {name}: {emoji}")


def example_practical_scenarios():
    """实际应用场景示例"""
    print("\n" + "="*50)
    print("💼 实际应用场景")
    print("="*50)
    
    # 场景1: 社交媒体评论处理
    print(f"\n场景1: 社交媒体评论处理")
    comments = [
        "这个产品真棒 👍👍👍",
        "差评! 😡👎",
        "一般般吧 😐",
    ]
    
    for comment in comments:
        stats = get_emoji_stats(comment)
        print(f"   评论: {comment}")
        print(f"   Emoji统计: {stats}")
    
    # 场景2: 敏感词过滤（移除 Emoji）
    print(f"\n场景2: 敏感内容处理（移除 Emoji 后检查）")
    text = "😀敏感词😀内容😀"
    clean_text = remove_emojis(text)
    print(f"   原文: {text}")
    print(f"   清理后: {clean_text}")
    
    # 场景3: 消息格式化
    print(f"\n场景3: 消息格式化")
    def format_message(text):
        """将 Emoji 替换为文本描述"""
        emoji_names = {
            '😀': '[开心]',
            '🎉': '[庆祝]',
            '👍': '[点赞]',
            '❤️': '[爱心]',
        }
        return replace_emojis_with_text(text, emoji_names)
    
    msg = "感谢你的帮助 👍 很开心 😀"
    print(f"   原消息: {msg}")
    print(f"   格式化: {format_message(msg)}")


def main():
    """运行所有示例"""
    print("\n" + "="*50)
    print("🎨 Emoji Utils 使用示例集")
    print("="*50)
    
    example_basic_usage()
    example_remove_replace()
    example_emoji_info()
    example_random_generation()
    example_text_analysis()
    example_filtering()
    example_common_emojis()
    example_practical_scenarios()
    
    print("\n" + "="*50)
    print("✅ 所有示例运行完成!")
    print("="*50 + "\n")


if __name__ == '__main__':
    main()