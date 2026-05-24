"""
name_parser_utils 使用示例

演示如何使用 name_parser_utils 解析、格式化和比较人名。

Author: AllToolkit
Date: 2026-05-24
"""

import sys
sys.path.insert(0, '..')

from mod import (
    NameParser, parse_name, parse_names, 
    format_name, compare_names, get_initials
)


def example_basic_parsing():
    """基础解析示例"""
    print("=" * 50)
    print("基础解析示例")
    print("=" * 50)
    
    parser = NameParser()
    
    # 简单英文名
    result = parser.parse("John Doe")
    print(f"\n解析 'John Doe':")
    print(f"  名: {result.first_name}")
    print(f"  姓: {result.last_name}")
    print(f"  格式类型: {result.format_type}")
    
    # 带中间名
    result = parser.parse("John William Doe")
    print(f"\n解析 'John William Doe':")
    print(f"  名: {result.first_name}")
    print(f"  中间名: {result.middle_name}")
    print(f"  姓: {result.last_name}")
    
    # 带前缀和后缀
    result = parser.parse("Dr. Jane Smith PhD")
    print(f"\n解析 'Dr. Jane Smith PhD':")
    print(f"  前缀: {result.prefix}")
    print(f"  名: {result.first_name}")
    print(f"  姓: {result.last_name}")
    print(f"  后缀: {result.suffix}")
    
    # 姓在前的格式
    result = parser.parse("Doe, John William")
    print(f"\n解析 'Doe, John William':")
    print(f"  名: {result.first_name}")
    print(f"  中间名: {result.middle_name}")
    print(f"  姓: {result.last_name}")


def example_chinese_parsing():
    """中文名称解析示例"""
    print("\n" + "=" * 50)
    print("中文名称解析示例")
    print("=" * 50)
    
    parser = NameParser()
    
    # 简单中文名
    result = parser.parse("张三")
    print(f"\n解析 '张三':")
    print(f"  姓: {result.chinese_surname}")
    print(f"  名: {result.chinese_given_name}")
    print(f"  格式类型: {result.format_type}")
    
    # 复姓
    result = parser.parse("欧阳锋")
    print(f"\n解析 '欧阳锋':")
    print(f"  姓: {result.chinese_surname}")
    print(f"  名: {result.chinese_given_name}")
    
    # 复姓加双字名
    result = parser.parse("司马相如")
    print(f"\n解析 '司马相如':")
    print(f"  姓: {result.chinese_surname}")
    print(f"  名: {result.chinese_given_name}")
    
    # 常见姓氏
    names = ["王伟", "李明", "刘洋", "陈晓", "赵云"]
    print(f"\n批量解析中文姓名:")
    for name in names:
        result = parser.parse(name)
        print(f"  {name}: 姓='{result.chinese_surname}', 名='{result.chinese_given_name}'")


def example_formatting():
    """名称格式化示例"""
    print("\n" + "=" * 50)
    print("名称格式化示例")
    print("=" * 50)
    
    parser = NameParser()
    
    # 不同格式
    names = [
        "John William Doe",
        "Dr. Jane Smith PhD",
        "张三",
        "欧阳锋"
    ]
    
    for name in names:
        parsed = parser.parse(name)
        print(f"\n原始: {name}")
        print(f"  西方格式: {parser.format_name(parsed, 'western')}")
        print(f"  姓在先: {parser.format_name(parsed, 'last_first')}")
        print(f"  首字母: {parser.format_name(parsed, 'initials')}")
        print(f"  带前缀后缀: {parser.format_name(parsed, 'western', include_prefix=True, include_suffix=True)}")


def example_comparison():
    """名称比较示例"""
    print("\n" + "=" * 50)
    print("名称比较示例")
    print("=" * 50)
    
    parser = NameParser()
    
    pairs = [
        ("John Doe", "John Doe"),
        ("John Doe", "JOHN DOE"),
        ("John Doe", "Jane Doe"),
        ("John Doe", "John Smith"),
        ("J. Doe", "John Doe"),
        ("张三", "张三"),
        ("张三", "李四"),
    ]
    
    print("\n比较结果:")
    for name1, name2 in pairs:
        match, score = parser.compare_names(name1, name2)
        status = "✓ 匹配" if match else "✗ 不匹配"
        print(f"  '{name1}' vs '{name2}': {status} (相似度: {score:.2f})")


def example_batch_parsing():
    """批量解析示例"""
    print("\n" + "=" * 50)
    print("批量解析示例")
    print("=" * 50)
    
    names = [
        "Mr. John William Doe Jr.",
        "Dr. Jane Smith",
        "Madonna",
        "张三",
        "欧阳锋",
        "Doe, John",
        'Alice "Ali" Johnson'
    ]
    
    print(f"\n批量解析 {len(names)} 个名称:")
    results = parse_names(names)
    
    for name, result in zip(names, results):
        print(f"\n  '{name}':")
        print(f"    前缀: {result.prefix or '-'}")
        print(f"    名: {result.first_name or '-'}")
        print(f"    中间名: {result.middle_name or '-'}")
        print(f"    姓: {result.last_name or '-'}")
        print(f"    后缀: {result.suffix or '-'}")
        if result.chinese_surname:
            print(f"    中文姓: {result.chinese_surname}")
            print(f"    中文名: {result.chinese_given_name}")
        if result.nickname:
            print(f"    昵称: {result.nickname}")


def example_initials():
    """首字母提取示例"""
    print("\n" + "=" * 50)
    print("首字母提取示例")
    print("=" * 50)
    
    parser = NameParser()
    
    names = [
        "John Doe",
        "John William Doe",
        "Mary Jane Watson",
        "张三",
        "欧阳锋",
    ]
    
    print("\n首字母提取:")
    for name in names:
        initials = parser.get_initials(name)
        initials_with_middle = parser.get_initials(name, include_middle=True)
        print(f"  '{name}': {initials} (含中间名: {initials_with_middle})")


def example_to_dict():
    """字典转换示例"""
    print("\n" + "=" * 50)
    print("字典转换示例")
    print("=" * 50)
    
    result = parse_name("Dr. John William Doe Jr.")
    data = result.to_dict()
    
    print("\n解析 'Dr. John William Doe Jr.' 转换为字典:")
    for key, value in data.items():
        print(f"  {key}: {value!r}")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 50)
    print("便捷函数示例")
    print("=" * 50)
    
    # parse_name
    result = parse_name("John Doe")
    print(f"\nparse_name('John Doe'): first={result.first_name}, last={result.last_name}")
    
    # format_name
    formatted = format_name("John William Doe", "initials")
    print(f"format_name('John William Doe', 'initials'): {formatted}")
    
    # compare_names
    match, score = compare_names("John Doe", "John Doe")
    print(f"compare_names('John Doe', 'John Doe'): match={match}, score={score:.2f}")
    
    # get_initials
    initials = get_initials("John William Doe")
    print(f"get_initials('John William Doe'): {initials}")


def main():
    """运行所有示例"""
    example_basic_parsing()
    example_chinese_parsing()
    example_formatting()
    example_comparison()
    example_batch_parsing()
    example_initials()
    example_to_dict()
    example_convenience_functions()
    
    print("\n" + "=" * 50)
    print("示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()