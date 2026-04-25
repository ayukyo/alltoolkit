"""
Emoji Utils 使用示例

演示 emoji_utils 模块的主要功能
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    detect_emoji,
    extract_emoji,
    remove_emoji,
    replace_emoji,
    count_emoji,
    get_emoji_frequency,
    get_emoji_description,
    categorize_emoji,
    group_emoji_by_category,
    extract_unique_emoji,
    is_only_emoji,
    get_text_emoji_ratio,
    sanitize_text,
    analyze,
    EmojiUtils,
    EmojiCategory,
)


def print_separator(title: str):
    """打印分隔线"""
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print(f"{'=' * 50}\n")


def example_detect():
    """示例：检测 emoji"""
    print_separator("检测 emoji")
    
    texts = [
        "Hello! 👋",
        "I'm feeling 😊 today!",
        "No emojis here!",
        "🚀🎉❤️🔥💯",
    ]
    
    for text in texts:
        has_emoji = detect_emoji(text)
        print(f"'{text}' -> 包含 emoji: {has_emoji}")


def example_extract():
    """示例：提取 emoji"""
    print_separator("提取 emoji")
    
    text = "Hello! 👋 I'm feeling 😊 today! 🌍🚀❤️"
    
    emojis = extract_emoji(text)
    print(f"原文: {text}")
    print(f"提取的 emoji: {emojis}")
    print(f"数量: {len(emojis)}")


def example_remove():
    """示例：移除 emoji"""
    print_separator("移除 emoji")
    
    text = "Hello! 👋😊 World! 🌍🚀"
    
    # 默认移除
    result1 = remove_emoji(text)
    print(f"原文: {text}")
    print(f"移除后: '{result1}'")
    
    # 使用空格替换
    result2 = remove_emoji(text, replacement=" ")
    print(f"替换为空格: '{result2}'")
    
    # 使用标记替换
    result3 = remove_emoji(text, replacement="[EMOJI]")
    print(f"替换为标记: '{result3}'")


def example_replace():
    """示例：替换 emoji 为描述"""
    print_separator("替换 emoji 为描述")
    
    text = "Hello! 👋 I ❤️ Python! 🐍🚀"
    
    result = replace_emoji(text)
    print(f"原文: {text}")
    print(f"替换后: {result}")
    
    # 自定义替换
    custom_map = {
        "👋": "HI",
        "❤️": "LOVE",
        "🐍": "PYTHON",
        "🚀": "ROCKET"
    }
    result2 = replace_emoji(text, replacement_map=custom_map)
    print(f"自定义替换: {result2}")


def example_count():
    """示例：统计 emoji"""
    print_separator("统计 emoji")
    
    text = "Hello! 👋😊👋🌍🚀👋"
    
    count = count_emoji(text)
    frequency = get_emoji_frequency(text)
    
    print(f"原文: {text}")
    print(f"总数: {count}")
    print(f"频率统计: {frequency}")


def example_description():
    """示例：获取 emoji 描述"""
    print_separator("获取 emoji 描述")
    
    emojis = ["👋", "❤️", "😊", "🚀", "🌍"]
    
    for emoji in emojis:
        desc = get_emoji_description(emoji)
        print(f"{emoji} -> {desc}")


def example_categorize():
    """示例：emoji 分类"""
    print_separator("emoji 分类")
    
    emojis = ["😊", "😂", "🐶", "🐱", "🍎", "🍕", "🚗", "🚀", "❤️", "👍"]
    
    print("单个 emoji 分类:")
    for emoji in emojis:
        category = categorize_emoji(emoji)
        print(f"  {emoji} -> {category.value}")
    
    print("\n批量分组:")
    grouped = group_emoji_by_category(emojis)
    for category, emoji_list in grouped.items():
        print(f"  {category.value}: {emoji_list}")


def example_unique():
    """示例：唯一 emoji"""
    print_separator("唯一 emoji")
    
    text = "Hello! 👋😊👋🌍🚀👋"
    
    unique = extract_unique_emoji(text)
    all_emojis = extract_emoji(text)
    
    print(f"原文: {text}")
    print(f"所有 emoji: {all_emojis}")
    print(f"唯一 emoji: {unique}")
    print(f"总数: {len(all_emojis)}, 唯一数: {len(unique)}")


def example_only_emoji():
    """示例：检测是否只有 emoji"""
    print_separator("检测是否只有 emoji")
    
    texts = [
        "👋😊🌍🚀",
        "Hello 👋",
        "   ",  # 只有空格
        "😊😊😊",
        "Test 123",
    ]
    
    for text in texts:
        result = is_only_emoji(text)
        print(f"'{text}' -> 只有 emoji: {result}")


def example_ratio():
    """示例：emoji 比例"""
    print_separator("emoji 比例")
    
    texts = [
        "Hello 👋",          # 50%
        "Hi! 👋😊",          # 50%
        "👋😊🌍",            # 100%
        "Hello World",       # 0%
        "Test 👋 Test Test", # 25%
    ]
    
    for text in texts:
        ratio = get_text_emoji_ratio(text)
        print(f"'{text}' -> 比例: {ratio:.2%}")


def example_sanitize():
    """示例：清理过多 emoji"""
    print_separator("清理过多 emoji")
    
    texts = [
        ("Hello! 👋", 0.3),           # 正常，在限制内
        ("👋👋👋👋👋", 0.3),            # 超过限制
        ("Test 👋 Test 👋 Test", 0.3), # 正常
        ("👋🎉❤️🔥💯👋", 0.2),          # 超过限制
    ]
    
    for text, max_ratio in texts:
        result = sanitize_text(text, max_emoji_ratio=max_ratio)
        ratio = get_text_emoji_ratio(text)
        print(f"原文: '{text}' (比例: {ratio:.0%})")
        print(f"  限制: {max_ratio:.0%}, 结果: '{result}'\n")


def example_analyze():
    """示例：完整分析"""
    print_separator("完整分析")
    
    text = "Hello! 👋😊👋 I ❤️ Python! 🐍🚀🌍"
    
    result = analyze(text)
    
    print(f"原文: {text}")
    print(f"\n分析结果:")
    print(f"  包含 emoji: {result['has_emoji']}")
    print(f"  emoji 数量: {result['emoji_count']}")
    print(f"  唯一 emoji 数量: {result['unique_count']}")
    print(f"  emoji 列表: {result['emojis']}")
    print(f"  唯一 emoji: {result['unique_emojis']}")
    print(f"  频率统计: {result['frequency']}")
    print(f"  emoji 比例: {result['ratio']:.2%}")
    print(f"  是否只有 emoji: {result['is_only_emoji']}")
    print(f"  类别分布: {result['categories']}")


def example_class():
    """示例：使用 EmojiUtils 类"""
    print_separator("使用 EmojiUtils 类")
    
    text = "Hello! 👋😊❤️ Python! 🐍🚀"
    utils = EmojiUtils(text)
    
    print(f"原文: {text}")
    print(f"\n属性:")
    print(f"  包含 emoji: {utils.has_emoji}")
    print(f"  emoji 数量: {utils.emoji_count}")
    print(f"  emoji 列表: {utils.emojis}")
    print(f"  唯一 emoji: {utils.unique_emojis}")
    print(f"  emoji 频率: {utils.emoji_frequency}")
    print(f"  emoji 比例: {utils.emoji_ratio():.2%}")
    
    print(f"\n方法:")
    print(f"  移除 emoji: '{utils.remove_emoji()}'")
    print(f"  替换 emoji: '{utils.replace_emoji()}'")
    print(f"  只有 emoji: {utils.is_only_emoji()}")
    print(f"  类别分组: {utils.categorize()}")
    
    # 更新文本
    print(f"\n更新文本:")
    utils.text = "Hi! 🚀🎉🔥"
    print(f"  新文本: {utils.text}")
    print(f"  emoji 数量: {utils.emoji_count}")
    print(f"  emoji 列表: {utils.emojis}")


def example_practical():
    """示例：实际应用场景"""
    print_separator("实际应用场景")
    
    # 场景1：社交媒体文本清理
    print("场景1：社交媒体文本清理")
    user_input = "OMG!!! 😂😂😂😂😂😂😂😂😂😂 SO FUNNY!!! 😂😂😂"
    clean_text = sanitize_text(user_input, max_emoji_ratio=0.2)
    print(f"  原文: {user_input}")
    print(f"  清理后: {clean_text}")
    
    # 场景2：评论 emoji 分析
    print("\n场景2：评论 emoji 分析")
    comments = [
        "Great product! ❤️❤️❤️",
        "Not bad 👍",
        "Terrible experience 👎👎👎",
        "Love it! 😍🥰💖💕",
    ]
    
    for comment in comments:
        emojis = extract_emoji(comment)
        freq = get_emoji_frequency(comment)
        print(f"  '{comment}' -> emoji: {emojis}, 频率: {freq}")
    
    # 场景3：生成 emoji 报告
    print("\n场景3：emoji 分析报告")
    text = "Today was amazing! 😊 I met so many cool people 👋❤️ " \
           "We had great food 🍕🍔 and the weather was perfect 🌞 " \
           "Can't wait for tomorrow! 🚀🎉"
    
    report = analyze(text)
    print(f"  文本: {text[:50]}...")
    print(f"  共 {report['emoji_count']} 个 emoji")
    print(f"  {report['unique_count']} 种不同的 emoji")
    print(f"  emoji 比例: {report['ratio']:.1%}")
    print(f"  类别分布:")
    for cat, emojis in report['categories'].items():
        print(f"    - {cat}: {emojis}")


def main():
    """运行所有示例"""
    example_detect()
    example_extract()
    example_remove()
    example_replace()
    example_count()
    example_description()
    example_categorize()
    example_unique()
    example_only_emoji()
    example_ratio()
    example_sanitize()
    example_analyze()
    example_class()
    example_practical()
    
    print_separator("示例运行完成!")


if __name__ == "__main__":
    main()