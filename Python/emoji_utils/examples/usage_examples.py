"""
emoji_utils 使用示例

展示各种功能的使用方法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


def example_basic_detection():
    """基础检测示例"""
    print("\n" + "=" * 50)
    print("示例 1: 基础 Emoji 检测")
    print("=" * 50)
    
    text = "今天天气真好 😊☀️ 适合出去玩 🎉"
    
    print(f"文本: {text}")
    print(f"检测到的 emoji: {detect_emojis(text)}")
    
    # 统计
    counts = count_emojis(text)
    print(f"emoji 统计: {counts}")


def example_remove_replace():
    """移除和替换示例"""
    print("\n" + "=" * 50)
    print("示例 2: 移除和替换 Emoji")
    print("=" * 50)
    
    text = "你好 👋 世界 🌍 开心 😊"
    
    # 移除
    cleaned = remove_emojis(text)
    print(f"原文: {text}")
    print(f"移除后: {cleaned}")
    
    # 替换为占位符
    replaced = remove_emojis(text, replacement='[表情]')
    print(f"替换后: {replaced}")
    
    # 使用映射替换
    mapping = {'👋': '你好', '🌍': '地球', '😊': '开心'}
    mapped = EmojiUtils.replace_emojis(text, mapping, default='[?]')
    print(f"映射替换: {mapped}")


def example_emoji_info():
    """获取 emoji 信息"""
    print("\n" + "=" * 50)
    print("示例 3: 获取 Emoji 详细信息")
    print("=" * 50)
    
    emojis = ['😊', '❤️', '🐱', '🍕', '🎉']
    
    for emoji in emojis:
        info = get_emoji_info(emoji)
        print(f"\nEmoji: {info['emoji']}")
        print(f"  Unicode: {info['unicode']}")
        print(f"  名称: {info['name']}")
        print(f"  分类: {info['category']}")


def example_separate():
    """分离文本和 emoji"""
    print("\n" + "=" * 50)
    print("示例 4: 分离文本和 Emoji")
    print("=" * 50)
    
    text = "今天心情 😊 很好，想去 🏖️ 玩，然后吃 🍕"
    
    pure_text, emojis = separate_text_emoji(text)
    
    print(f"原文: {text}")
    print(f"纯文本: {pure_text}")
    print(f"Emoji 列表: {emojis}")


def example_categorize():
    """emoji 分类示例"""
    print("\n" + "=" * 50)
    print("示例 5: Emoji 分类")
    print("=" * 50)
    
    emojis = ['😊', '😢', '🐱', '🐶', '🍕', '🍔', '⚽', '🎮', '❤️', '👍']
    
    print(f"Emoji 列表: {emojis}")
    
    categories = EmojiUtils.categorize_emojis(emojis)
    print("\n分类结果:")
    for category, emoji_list in categories.items():
        print(f"  {category}: {emoji_list}")


def example_text_to_emoji():
    """文本转 emoji"""
    print("\n" + "=" * 50)
    print("示例 6: 文本转 Emoji")
    print("=" * 50)
    
    texts = [
        "I am happy today",
        "I love cats and dogs",
        "The weather is sunny and I want coffee",
        "Good job! Keep going!",
    ]
    
    for text in texts:
        converted = text_to_emoji(text)
        print(f"{text}")
        print(f"  → {converted}")


def example_density():
    """emoji 密度分析"""
    print("\n" + "=" * 50)
    print("示例 7: Emoji 密度分析")
    print("=" * 50)
    
    texts = [
        "今天心情很好",
        "😊🎉🌟✨🎊🎈",
        "你好 👋 世界 🌍 很开心 😊",
        "这是一个包含一些 emoji 的普通文本段落 📝",
    ]
    
    for text in texts:
        density = emoji_density(text)
        print(f"密度 {density:.2%}: {text}")


def example_positions():
    """位置提取示例"""
    print("\n" + "=" * 50)
    print("示例 8: Emoji 位置提取")
    print("=" * 50)
    
    text = "你好😊世界🎉开心🌟"
    
    print(f"文本: {text}")
    positions = EmojiUtils.extract_emoji_positions(text)
    
    for emoji, start, end in positions:
        print(f"  '{emoji}' 位于 [{start}:{end}]")


def example_only_emojis():
    """检查是否只包含 emoji"""
    print("\n" + "=" * 50)
    print("示例 9: 检查是否仅包含 Emoji")
    print("=" * 50)
    
    texts = [
        "🎉🎊🎈",
        "你好 😊",
        "这是一段纯文本",
        "👍🏻👍🏼👍🏽",
    ]
    
    for text in texts:
        result = is_only_emojis(text)
        print(f"{result}: '{text}'")


def example_practical_use():
    """实际应用示例"""
    print("\n" + "=" * 50)
    print("示例 10: 实际应用 - 社交媒体文本分析")
    print("=" * 50)
    
    # 模拟社交媒体帖子
    posts = [
        "今天去公园玩了 🎉 遇到了一只可爱的 🐱 真开心 😊",
        "工作好累 😫 需要咖啡 ☕ 和休息 😴",
        "美食时刻 🍕🍔🍟 和朋友聚餐真开心 👫",
    ]
    
    print("社交媒体帖子分析:\n")
    
    for i, post in enumerate(posts, 1):
        print(f"帖子 {i}: {post}")
        
        # 分析
        emojis = detect_emojis(post)
        density = emoji_density(post)
        counts = count_emojis(post)
        
        print(f"  Emoji 种类: {len(emojis)}")
        print(f"  Emoji 数量: {sum(counts.values())}")
        print(f"  Emoji 密度: {density:.1%}")
        print(f"  分类: {EmojiUtils.categorize_emojis(emojis)}")
        print()


def main():
    """运行所有示例"""
    example_basic_detection()
    example_remove_replace()
    example_emoji_info()
    example_separate()
    example_categorize()
    example_text_to_emoji()
    example_density()
    example_positions()
    example_only_emojis()
    example_practical_use()
    
    print("\n" + "=" * 50)
    print("所有示例演示完成！")
    print("=" * 50)


if __name__ == '__main__':
    main()