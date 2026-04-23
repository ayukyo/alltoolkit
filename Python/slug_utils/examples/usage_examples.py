#!/usr/bin/env python3
"""
slug_utils 使用示例
===================

展示 slug_utils 库的各种使用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    slugify,
    slugify_unique,
    generate_slug,
    is_valid_slug,
    unslugify,
    slug_range,
    smart_slugify,
    count_slug_words,
    truncate_slug,
    compare_slugs,
    batch_slugify,
)


def example_basic_usage():
    """基本用法示例"""
    print("\n" + "=" * 50)
    print("基本用法示例")
    print("=" * 50)
    
    texts = [
        "Hello World!",
        "The Quick Brown Fox Jumps Over The Lazy Dog",
        "Python 3.12 新特性",
        "Café & Restaurant",
        "100% Natural Product",
    ]
    
    for text in texts:
        slug = slugify(text)
        print(f"  '{text}' -> '{slug}'")


def example_custom_separator():
    """自定义分隔符示例"""
    print("\n" + "=" * 50)
    print("自定义分隔符示例")
    print("=" * 50)
    
    text = "Hello World From Python"
    
    print(f"  原文: '{text}'")
    print(f"  默认(连字符): '{slugify(text)}'")
    print(f"  下划线: '{slugify(text, separator='_')}'")
    print(f"  点号: '{slugify(text, separator='.')}'")
    print(f"  无分隔符: '{slugify(text, separator='')}'")


def example_case_handling():
    """大小写处理示例"""
    print("\n" + "=" * 50)
    print("大小写处理示例")
    print("=" * 50)
    
    text = "HELLO World"
    
    print(f"  原文: '{text}'")
    print(f"  小写(默认): '{slugify(text, lowercase=True)}'")
    print(f"  保留原样: '{slugify(text, lowercase=False)}'")


def example_chinese_japanese():
    """中日文处理示例"""
    print("\n" + "=" * 50)
    print("中日文处理示例")
    print("=" * 50)
    
    texts = [
        "你好世界",
        "中国人工智能发展",
        "こんにちは世界",  # 日文
        "テストページ",  # 日文片假名
        "한국",  # 韩文
        "Hello世界Mixed",  # 混合
    ]
    
    for text in texts:
        slug = slugify(text)
        print(f"  '{text}' -> '{slug}'")


def example_unique_slug():
    """唯一slug生成示例"""
    print("\n" + "=" * 50)
    print("唯一slug生成示例")
    print("=" * 50)
    
    existing = ["hello-world", "my-post", "hello-world-2"]
    
    titles = ["Hello World", "My New Post", "Hello World"]
    
    for title in titles:
        slug = slugify_unique(title, existing=existing)
        existing.append(slug)
        print(f"  '{title}' -> '{slug}'")


def example_prefix_suffix():
    """前缀后缀示例"""
    print("\n" + "=" * 50)
    print("前缀后缀示例")
    print("=" * 50)
    
    title = "My Blog Post"
    
    print(f"  原文: '{title}'")
    with_prefix = generate_slug(title, prefix="blog")
    print(f"  带分类前缀: '{with_prefix}'")
    with_suffix = generate_slug(title, suffix="2024-01-15")
    print(f"  带日期后缀: '{with_suffix}'")
    with_both = generate_slug(title, prefix="blog", suffix="2024")
    print(f"  同时添加: '{with_both}'")


def example_validation():
    """验证示例"""
    print("\n" + "=" * 50)
    print("验证示例")
    print("=" * 50)
    
    test_slugs = [
        "hello-world",
        "Hello-World",  # 大写
        "hello_world",  # 下划线
        "hello world",  # 空格
        "-hello",  # 开头分隔符
        "hello-",  # 结尾分隔符
        "",  # 空字符串
    ]
    
    for slug in test_slugs:
        valid = is_valid_slug(slug)
        valid_upper = is_valid_slug(slug, allow_uppercase=True)
        valid_underscore = is_valid_slug(slug, separator="_")
        
        print(f"  '{slug}':")
        print(f"    默认: {'✅' if valid else '❌'}")
        print(f"    允许大写: {'✅' if valid_upper else '❌'}")


def example_unslugify():
    """slug还原示例"""
    print("\n" + "=" * 50)
    print("slug还原示例")
    print("=" * 50)
    
    slugs = [
        "hello-world",
        "my-blog-post-2024",
        "product_review",
    ]
    
    for slug in slugs:
        normal = unslugify(slug)
        title = unslugify(slug, title_case=True)
        underscore = unslugify(slug, separator="_", space_replacement="_")
        
        print(f"  '{slug}':")
        print(f"    普通还原: '{normal}'")
        print(f"    标题格式: '{title}'")


def example_smart_slug():
    """智能slug示例"""
    print("\n" + "=" * 50)
    print("智能slug示例")
    print("=" * 50)
    
    texts = [
        "What's the Best Way?",
        "Price: $100 + Tax",
        "100% Natural™ Product",
        "α + β = γ",
        "user@email.com",
        "Café & Restaurant",
    ]
    
    for text in texts:
        slug = smart_slugify(text)
        print(f"  '{text}' -> '{slug}'")


def example_slug_range():
    """slug范围生成示例"""
    print("\n" + "=" * 50)
    print("slug范围生成示例")
    print("=" * 50)
    
    # 生成章节编号
    chapters = slug_range("Chapter", 1, 5)
    print(f"  章节: {chapters}")
    
    # 生成页码
    pages = slug_range("Page", 0, 10, separator="_")
    print(f"  页码: {pages}")
    
    # 生成版本号
    versions = slug_range("v", 1, 3)
    print(f"  版本: {versions}")


def example_truncate():
    """截断示例"""
    print("\n" + "=" * 50)
    print("截断示例")
    print("=" * 50)
    
    slug = "this-is-a-very-long-blog-post-title-that-needs-to-be-truncated"
    
    print(f"  原始: '{slug}'")
    print(f"  保留单词边界 (max=40): '{truncate_slug(slug, 40)}'")
    print(f"  硬截断 (max=40): '{truncate_slug(slug, 40, preserve_words=False)}'")
    print(f"  短截断 (max=20): '{truncate_slug(slug, 20)}'")


def example_compare():
    """比较示例"""
    print("\n" + "=" * 50)
    print("比较示例")
    print("=" * 50)
    
    pairs = [
        ("hello-world", "hello-world"),
        ("hello-world", "hello-python"),
        ("my-blog-post", "your-blog-post"),
        ("product-123", "product-456"),
    ]
    
    for slug1, slug2 in pairs:
        result = compare_slugs(slug1, slug2)
        print(f"\n  比较 '{slug1}' vs '{slug2}':")
        print(f"    完全匹配: {'是' if result['exact_match'] else '否'}")
        print(f"    相似度: {result['similarity'] * 100:.1f}%")
        print(f"    共同词: {result['common_words']}")


def example_batch():
    """批量处理示例"""
    print("\n" + "=" * 50)
    print("批量处理示例")
    print("=" * 50)
    
    titles = [
        "Introduction to Python",
        "Introduction to Python",  # 重复
        "Advanced Python Techniques",
        "Python for Data Science",
    ]
    
    # 不保证唯一
    slugs = batch_slugify(titles)
    print(f"  普通批量生成: {slugs}")
    
    # 保证唯一
    unique_slugs = batch_slugify(titles, unique=True)
    print(f"  唯一批量生成: {unique_slugs}")


def example_real_world():
    """真实场景示例"""
    print("\n" + "=" * 50)
    print("真实场景示例")
    print("=" * 50)
    
    # 博客系统
    print("\n  📝 博客系统:")
    blog_title = "10 Tips for Writing Clean Python Code"
    blog_slug = slugify(blog_title, max_length=50)
    print(f"    标题: '{blog_title}'")
    print(f"    Slug: '{blog_slug}'")
    
    # 电商产品
    print("\n  🛒 电商产品:")
    product = "iPhone 15 Pro Max 256GB 紫色"
    product_slug = slugify(product)
    print(f"    产品: '{product}'")
    print(f"    Slug: '{product_slug}'")
    
    # 用户名生成
    print("\n  👤 用户名生成:")
    email = "john.doe@example.com"
    username = slugify(email.split('@')[0])
    print(f"    邮箱: '{email}'")
    print(f"    用户名: '{username}'")
    
    # URL路径
    print("\n  🌐 URL路径:")
    category = "电子产品 > 手机 > 智能手机"
    path_slug = slugify(category)
    print(f"    分类: '{category}'")
    print(f"    路径: '/products/{path_slug}'")
    
    # 文件名
    print("\n  📄 文件名转换:")
    filename = "My Document (Final Version).docx"
    file_slug = slugify(filename)
    print(f"    原文件名: '{filename}'")
    print(f"    安全文件名: '{file_slug}.docx'")


def example_max_length():
    """最大长度限制示例"""
    print("\n" + "=" * 50)
    print("最大长度限制示例")
    print("=" * 50)
    
    long_title = "This is an extremely long blog post title that definitely needs to be truncated for SEO purposes"
    
    print(f"  原标题: '{long_title}'")
    print(f"  长度: {len(long_title)}")
    
    for max_len in [30, 50, 80]:
        truncated = slugify(long_title, max_length=max_len)
        print(f"  max={max_len}: '{truncated}' ({len(truncated)} 字符)")


def example_word_count():
    """单词计数示例"""
    print("\n" + "=" * 50)
    print("单词计数示例")
    print("=" * 50)
    
    slugs = [
        "hello-world",
        "the-quick-brown-fox",
        "single",
        "",
    ]
    
    for slug in slugs:
        count = count_slug_words(slug)
        print(f"  '{slug}': {count} 个单词")


def run_all_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("slug_utils 使用示例演示")
    print("=" * 60)
    
    example_basic_usage()
    example_custom_separator()
    example_case_handling()
    example_chinese_japanese()
    example_unique_slug()
    example_prefix_suffix()
    example_validation()
    example_unslugify()
    example_smart_slug()
    example_slug_range()
    example_truncate()
    example_compare()
    example_batch()
    example_real_world()
    example_max_length()
    example_word_count()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all_examples()