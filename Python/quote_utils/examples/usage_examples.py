"""
名言警句工具 - 使用示例

展示名言警句工具的各种用法。
"""

from datetime import date, timedelta
import json
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入名言警句模块
from mod import (
    QuoteManager,
    Quote,
    QuoteCategory,
    QuoteStyle,
    QuoteFormatter,
    QuoteUtils,
    get_quote,
    get_daily_quote,
    search_quotes,
    format_quote,
    list_categories,
)


def example_basic_usage():
    """基础用法示例"""
    print("\n=== 基础用法 ===\n")
    
    # 创建管理器
    manager = QuoteManager()
    
    # 获取随机名言
    quote = manager.get_random_quote()
    print("随机名言:")
    print(f"  {quote.format(QuoteStyle.SIMPLE)}")
    
    # 获取每日名言
    daily = manager.get_daily_quote()
    print("\n每日名言:")
    print(f"  {daily.format(QuoteStyle.DECORATED)}")
    
    # 获取统计信息
    stats = manager.get_stats()
    print(f"\n名言库统计:")
    print(f"  总名言数: {stats['total_quotes']}")
    print(f"  中文名言: {stats['language_counts']['zh']}")
    print(f"  英文名言: {stats['language_counts']['en']}")


def example_by_category():
    """按类别获取名言示例"""
    print("\n=== 按类别获取名言 ===\n")
    
    manager = QuoteManager()
    
    # 列出所有类别
    print("可用类别:")
    for cat in list_categories():
        count = len(manager.get_quotes_by_category(QuoteCategory(cat)))
        print(f"  • {cat}: {count} 条")
    
    # 获取特定类别的名言
    print("\n激励类名言 (前5条):")
    quotes = manager.get_quotes_by_category(QuoteCategory.MOTIVATION)[:5]
    for i, q in enumerate(quotes, 1):
        print(f"  {i}. {q.format(QuoteStyle.MINIMAL)}")
    
    # 获取智慧类名言
    print("\n智慧类名言 (前3条):")
    quotes = manager.get_quotes_by_category(QuoteCategory.WISDOM)[:3]
    for q in quotes:
        print(f"  • \"{q.text}\" — {q.author}")


def example_by_author():
    """按作者获取名言示例"""
    print("\n=== 按作者获取名言 ===\n")
    
    manager = QuoteManager()
    
    # 获取孔子的名言
    print("孔子的名言:")
    quotes = manager.get_quotes_by_author("孔子")
    for q in quotes[:5]:
        print(f"  • {q.text}")
    
    # 获取老子的名言
    print("\n老子的名言:")
    quotes = manager.get_quotes_by_author("老子")
    for q in quotes[:3]:
        print(f"  • {q.text}")


def example_search():
    """搜索名言示例"""
    print("\n=== 搜索名言 ===\n")
    
    manager = QuoteManager()
    
    # 搜索关键词
    keywords = ["成功", "人生", "学习"]
    
    for keyword in keywords:
        print(f"\n搜索 '{keyword}':")
        results = manager.search_quotes(keyword)
        for q in results[:3]:
            print(f"  • {q.format(QuoteStyle.SIMPLE)}")


def example_formats():
    """多种格式示例"""
    print("\n=== 多种输出格式 ===\n")
    
    manager = QuoteManager()
    quote = manager.get_random_quote(language="zh")
    
    print(f"原文: {quote.text} — {quote.author}\n")
    
    # 各种格式
    formats = [
        ("简洁格式", QuoteStyle.SIMPLE),
        ("极简格式", QuoteStyle.MINIMAL),
        ("装饰格式", QuoteStyle.DECORATED),
        ("卡片格式", QuoteStyle.CARD),
        ("横幅格式", QuoteStyle.BANNER),
    ]
    
    for name, style in formats:
        print(f"\n{name}:")
        print(quote.format(style))


def example_custom_quote():
    """自定义名言示例"""
    print("\n=== 自定义名言 ===\n")
    
    manager = QuoteManager()
    
    # 添加自定义名言
    custom_quotes = [
        {
            "text": "代码写得优雅，人生才会优雅。",
            "author": "程序员",
            "category": QuoteCategory.WORK,
            "tags": ["编程", "人生"],
        },
        {
            "text": "Bug 是人生的一部分，学会接受它。",
            "author": "开发者",
            "category": QuoteCategory.MOTIVATION,
            "tags": ["调试", "心态"],
            "rating": 4,
        },
        {
            "text": "每一个 commit 都是一次成长。",
            "author": "Git 用户",
            "category": QuoteCategory.LEARNING,
            "tags": ["Git", "成长"],
        },
    ]
    
    for q_data in custom_quotes:
        quote = manager.add_quote(**q_data)
        print(f"添加: {quote.format(QuoteStyle.SIMPLE)}")
    
    # 获取新增的名言
    print("\n编程相关名言:")
    results = manager.search_quotes("代码")
    for q in results:
        print(f"  • {q.text}")


def example_favorites():
    """收藏管理示例"""
    print("\n=== 收藏管理 ===\n")
    
    manager = QuoteManager()
    
    # 获取几条名言并收藏
    quotes = [
        manager.get_quotes_by_category(QuoteCategory.WISDOM)[0],
        manager.get_quotes_by_category(QuoteCategory.MOTIVATION)[0],
    ]
    
    print("添加收藏:")
    for quote in quotes:
        manager.add_to_favorites(quote.get_id())
        print(f"  ✓ {quote.format(QuoteStyle.MINIMAL)}")
    
    # 获取收藏列表
    print("\n收藏列表:")
    favorites = manager.get_favorites()
    for i, q in enumerate(favorites, 1):
        emoji = "⭐" if q.is_favorite else "☆"
        print(f"  {emoji} {i}. {q.format(QuoteStyle.SIMPLE)}")
    
    # 取消收藏
    if favorites:
        removed = manager.remove_from_favorites(favorites[0].get_id())
        print(f"\n取消收藏: {favorites[0].text[:20]}...")
    
    # 验证
    print(f"当前收藏数: {len(manager.get_favorites())}")


def example_daily_quote():
    """每日名言示例"""
    print("\n=== 每日名言功能 ===\n")
    
    manager = QuoteManager()
    
    # 获取今天的每日名言
    today_quote = manager.get_daily_quote()
    print("今日名言:")
    print(today_quote.format(QuoteStyle.CARD))
    
    # 再次获取，应该是同一条
    quote2 = manager.get_daily_quote()
    print(f"\n再次获取（验证同一条）:")
    print(f"  ID匹配: {today_quote.get_id() == quote2.get_id()}")
    
    # 按类别获取每日名言
    print("\n按类别的每日名言:")
    categories = ["success", "motivation", "wisdom"]
    
    for cat in categories:
        daily = manager.get_daily_quote(category=QuoteCategory(cat))
        print(f"\n[{cat}]")
        print(f"  {daily.format(QuoteStyle.DECORATED)}")
    
    # 中英文每日名言
    print("\n中文每日名言:")
    zh_quote = manager.get_daily_quote(language="zh")
    print(f"  {zh_quote.format(QuoteStyle.SIMPLE)}")
    
    print("\n英文每日名言:")
    en_quote = manager.get_daily_quote(language="en")
    print(f"  {en_quote.format(QuoteStyle.SIMPLE)}")


def example_formatter():
    """格式化工具示例"""
    print("\n=== 格式化工具 ===\n")
    
    manager = QuoteManager()
    quote = manager.get_random_quote(language="zh")
    
    # 简洁格式
    print("简洁格式:")
    print(QuoteFormatter.format_simple(quote))
    
    # Twitter格式
    print("\nTwitter格式:")
    print(QuoteFormatter.format_twitter(quote))
    
    # Markdown格式
    print("\nMarkdown格式:")
    print(QuoteFormatter.format_markdown(quote))
    
    # HTML格式
    print("\nHTML格式:")
    print(QuoteFormatter.format_html(quote))
    
    # 带翻译格式
    print("\n带翻译格式:")
    if quote.language == "zh":
        translation = "Life is like a cup of tea..."
    else:
        translation = "人生就像一杯茶..."
    print(QuoteFormatter.format_with_translation(quote, translation))
    
    # 名言列表格式
    print("\n名言列表格式:")
    quotes = manager.get_quotes_by_category(QuoteCategory.LIFE)[:3]
    print(QuoteFormatter.format_list(quotes))


def example_stats():
    """统计信息示例"""
    print("\n=== 统计信息 ===\n")
    
    manager = QuoteManager()
    stats = manager.get_stats()
    
    print("名言库统计:")
    print(f"  总名言数: {stats['total_quotes']}")
    print(f"  收藏数: {stats['favorites_count']}")
    
    print("\n语言分布:")
    for lang, count in stats['language_counts'].items():
        print(f"  • {lang}: {count} 条")
    
    print("\n类别分布 (前10):")
    sorted_cats = sorted(stats['category_counts'].items(), key=lambda x: x[1], reverse=True)
    for cat, count in sorted_cats[:10]:
        if count > 0:
            print(f"  • {cat}: {count} 条")
    
    # 高评分名言
    print("\n高评分名言:")
    top_quotes = manager.get_top_quotes(n=5)
    for i, q in enumerate(top_quotes, 1):
        print(f"  {i}. [{q.rating}★] {q.text[:30]}...")


def example_static_utils():
    """静态工具方法示例"""
    print("\n=== 静态工具方法 ===\n")
    
    # 随机名言
    print("随机名言:")
    quote = QuoteUtils.random_quote()
    print(f"  {quote.format(QuoteStyle.SIMPLE)}")
    
    # 每日名言
    print("\n每日名言:")
    daily = QuoteUtils.daily_quote()
    print(f"  {daily.format(QuoteStyle.SIMPLE)}")
    
    # 搜索
    print("\n搜索 '勇气':")
    results = QuoteUtils.search("勇气")
    for q in results[:2]:
        print(f"  • {q.text}")
    
    # 按类别
    print("\n学习类名言:")
    quotes = QuoteUtils.by_category("learning")
    for q in quotes[:3]:
        print(f"  • {q.text}")
    
    # 所有类别
    print("\n所有类别:")
    categories = QuoteUtils.categories()
    print(f"  {', '.join(categories[:8])}...")
    
    # 格式化
    print("\n格式化样式:")
    quote = QuoteUtils.random_quote()
    for style in ["simple", "card", "decorated"]:
        formatted = QuoteUtils.format(quote, style)
        print(f"\n  [{style}]")
        print(f"  {formatted[:50]}...")


def example_export_import():
    """数据导出导入示例"""
    print("\n=== 数据导出导入 ===\n")
    
    manager = QuoteManager()
    
    # 添加一些自定义名言
    manager.add_quote("导出测试名言1", "作者A", category=QuoteCategory.LIFE)
    manager.add_quote("导出测试名言2", "作者B", category=QuoteCategory.SUCCESS)
    
    # 导出数据
    json_data = manager.export_data()
    
    print("导出的JSON数据 (前500字符):")
    print(json_data[:500])
    print(f"\n总长度: {len(json_data)} 字符")
    
    # 导入到新管理器
    new_manager = QuoteManager()
    count = new_manager.import_data(json_data)
    
    print(f"\n成功导入 {count} 条新增名言")
    
    # 验证
    for q in new_manager.search_quotes("导出测试"):
        print(f"  ✓ {q.text}")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n=== 便捷函数 ===\n")
    
    # get_quote - 随机名言
    print("随机名言:")
    quote = get_quote()
    print(f"  {format_quote(quote)}")
    
    # 带类别
    print("\n成功类名言:")
    quote = get_quote(category="success")
    if quote:
        print(f"  {format_quote(quote)}")
    
    # 每日名言
    print("\n每日名言:")
    daily = get_daily_quote()
    print(f"  {format_quote(daily, style='decorated')}")
    
    # 搜索
    print("\n搜索 '时间':")
    results = search_quotes("时间")
    for q in results[:3]:
        print(f"  • {q.text}")
    
    # 类别列表
    print("\n所有类别:")
    cats = list_categories()
    print(f"  {cats}")


def example_full_demo():
    """完整演示"""
    print("\n=== 完整演示 ===\n")
    
    manager = QuoteManager()
    
    # 1. 显示今日名言
    print("✨ 今日名言 ✨")
    daily = manager.get_daily_quote()
    print(daily.format(QuoteStyle.CARD))
    
    # 2. 显示各类别名言数
    print("\n名言库概览:")
    stats = manager.get_stats()
    print(f"  总计: {stats['total_quotes']} 条名言")
    
    # 3. 推荐名言（按类别）
    print("\n今日推荐 (各类别精选):")
    recommend_categories = ["motivation", "wisdom", "success", "learning"]
    
    for cat in recommend_categories:
        quote = manager.get_random_quote(category=QuoteCategory(cat))
        if quote:
            print(f"\n[{cat.upper()}]")
            print(f"  {quote.format(QuoteStyle.DECORATED)}")
    
    # 4. 搜索热门关键词
    print("\n热门关键词搜索结果:")
    hot_keywords = ["人生", "成功", "学习"]
    
    for keyword in hot_keywords:
        results = manager.search_quotes(keyword)
        print(f"\n'{keyword}' ({len(results)} 条):")
        if results:
            print(f"  示例: {results[0].text[:30]}...")
    
    # 5. 高评分名言
    print("\n⭐ 高评分名言 ⭐")
    top_quotes = manager.get_top_quotes(n=5)
    for i, q in enumerate(top_quotes, 1):
        stars = "★" * q.rating
        print(f"  {i}. [{stars}] {q.text[:25]}...")
    
    # 6. 英文名言
    print("\n英文每日名言:")
    en_quote = manager.get_daily_quote(language="en")
    print(f"  {en_quote.format(QuoteStyle.SIMPLE)}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("名言警句工具 - 使用示例")
    print("=" * 60)
    
    example_basic_usage()
    example_by_category()
    example_by_author()
    example_search()
    example_formats()
    example_custom_quote()
    example_favorites()
    example_daily_quote()
    example_formatter()
    example_stats()
    example_static_utils()
    example_export_import()
    example_convenience_functions()
    example_full_demo()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()