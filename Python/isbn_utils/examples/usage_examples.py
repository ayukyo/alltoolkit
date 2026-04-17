"""
ISBN Utils 使用示例

演示 ISBN 工具的各种功能：
- 验证 ISBN
- 格式转换
- 解析和提取
- 随机生成
"""

from mod import (
    ISBNUtils,
    validate, validate_strict, convert_to_13, convert_to_10,
    format_isbn, parse, generate_random, extract_from_text
)


def example_basic_validation():
    """基本验证示例"""
    print("=" * 50)
    print("基本验证示例")
    print("=" * 50)
    
    # 各种格式的 ISBN
    test_isbns = [
        "978-7-115-46985-5",  # 人民邮电出版社
        "7-302-11756-7",      # 清华大学出版社
        "978-0-13-235088-4",  # 《代码整洁之道》
        "0-201-63361-2",      # 《设计模式》
    ]
    
    for isbn in test_isbns:
        is_valid = validate(isbn)
        version = ISBNUtils.detect_version(isbn)
        formatted = format_isbn(isbn)
        group = ISBNUtils.get_registration_group(isbn)
        
        print(f"\nISBN: {isbn}")
        print(f"  有效: {is_valid}")
        print(f"  版本: ISBN-{version}")
        print(f"  格式化: {formatted}")
        print(f"  注册组: {group}")


def example_strict_validation():
    """严格验证示例"""
    print("\n" + "=" * 50)
    print("严格验证示例")
    print("=" * 50)
    
    isbns = [
        "978-7-115-46985-5",  # 有效
        "978-7-115-46985-6",  # 无效（校验位错误）
    ]
    
    for isbn in isbns:
        try:
            result = validate_strict(isbn)
            print(f"\n✓ {isbn} 是有效的")
            print(f"  版本: ISBN-{result['version']}")
            print(f"  校验位: {result['check_digit']}")
            if 'prefix' in result:
                print(f"  前缀: {result['prefix']}")
        except Exception as e:
            print(f"\n✗ {isbn} 是无效的: {e}")


def example_conversion():
    """格式转换示例"""
    print("\n" + "=" * 50)
    print("格式转换示例")
    print("=" * 50)
    
    # ISBN-10 转 ISBN-13
    isbn10 = "7-302-11756-7"
    isbn13 = convert_to_13(isbn10)
    print(f"\nISBN-10 → ISBN-13:")
    print(f"  {isbn10} → {isbn13}")
    print(f"  格式化: {format_isbn(isbn13)}")
    
    # ISBN-13 转 ISBN-10
    isbn13 = "978-7-115-46985-5"
    isbn10 = convert_to_10(isbn13)
    print(f"\nISBN-13 → ISBN-10:")
    print(f"  {isbn13} → {isbn10}")
    print(f"  格式化: {format_isbn(isbn10)}")
    
    # 979 前缀的 ISBN-13 无法转换为 ISBN-10
    print(f"\n979 前缀的 ISBN-13 无法转换为 ISBN-10:")
    isbn_979 = "979-10-90636-07-0"
    try:
        convert_to_10(isbn_979)
    except Exception as e:
        print(f"  {isbn_979} → 错误: {e}")


def example_parse():
    """解析示例"""
    print("\n" + "=" * 50)
    print("解析示例")
    print("=" * 50)
    
    isbns = [
        "978-7-115-46985-5",
        "7-302-11756-7",
        "0-201-63361-2",
    ]
    
    for isbn in isbns:
        result = parse(isbn)
        print(f"\n解析: {isbn}")
        print(f"  清理后: {result['cleaned']}")
        print(f"  版本: ISBN-{result['version']}")
        print(f"  有效: {result['valid']}")
        print(f"  格式化: {result.get('isbn_formatted', 'N/A')}")
        if 'isbn13' in result:
            print(f"  ISBN-13: {result['isbn13']}")
        if 'isbn10' in result:
            print(f"  ISBN-10: {result['isbn10']}")


def example_generate():
    """随机生成示例"""
    print("\n" + "=" * 50)
    print("随机生成示例")
    print("=" * 50)
    
    print("\n生成 5 个随机 ISBN-13:")
    for _ in range(5):
        isbn = generate_random(version=13)
        print(f"  {isbn} (格式化: {format_isbn(isbn)})")
    
    print("\n生成 5 个随机 ISBN-10:")
    for _ in range(5):
        isbn = generate_random(version=10)
        print(f"  {isbn} (格式化: {format_isbn(isbn)})")
    
    print("\n生成指定前缀的 ISBN-13:")
    print(f"  978 前缀: {generate_random(13, prefix='978')}")
    print(f"  979 前缀: {generate_random(13, prefix='979')}")
    
    print("\n批量生成:")
    batch = ISBNUtils.generate_batch(5, version=13)
    for isbn in batch:
        print(f"  {isbn}")


def example_extract():
    """文本提取示例"""
    print("\n" + "=" * 50)
    print("文本提取示例")
    print("=" * 50)
    
    text = """
    推荐阅读书籍：
    
    1. 《代码整洁之道》ISBN: 978-0-13-235088-4
    2. 《设计模式》ISBN: 0-201-63361-2
    3. 《Python编程》ISBN: 978-7-115-46985-5
    4. 《算法导论》ISBN: 7-302-11756-7
    
    注意：以下 ISBN 无效：
    - 978-7-115-46985-6（校验位错误）
    - 12345（长度错误）
    """
    
    found = extract_from_text(text)
    print(f"\n从文本中找到 {len(found)} 个有效的 ISBN:")
    for isbn in found:
        formatted = format_isbn(isbn)
        group = ISBNUtils.get_registration_group(isbn)
        print(f"  {isbn} ({formatted}) - {group}")


def example_check_digit():
    """校验位计算示例"""
    print("\n" + "=" * 50)
    print("校验位计算示例")
    print("=" * 50)
    
    # ISBN-10 校验位计算
    isbn9 = "730211756"
    check = ISBNUtils.calculate_check_digit_10(isbn9)
    print(f"\nISBN-10 校验位计算:")
    print(f"  前9位: {isbn9}")
    print(f"  校验位: {check}")
    print(f"  完整 ISBN-10: {isbn9}{check}")
    
    # ISBN-13 校验位计算
    isbn12 = "978711546985"
    check = ISBNUtils.calculate_check_digit_12(isbn12)
    print(f"\nISBN-13 校验位计算:")
    print(f"  前12位: {isbn12}")
    print(f"  校验位: {check}")
    print(f"  完整 ISBN-13: {isbn12}{check}")


def example_registration_groups():
    """注册组识别示例"""
    print("\n" + "=" * 50)
    print("注册组识别示例")
    print("=" * 50)
    
    # 不同国家/地区的 ISBN
    examples = [
        ("978-7-115-46985-5", "中国"),
        ("0-201-63361-2", "英语区"),
        ("2-1234-5678-9", "法语区"),
        ("3-1234-5678-9", "德语区"),
        ("4-1234-5678-9", "日本"),
        ("5-1234-5678-9", "俄语区"),
        ("81-1234-5678-9", "印度"),
        ("89-1234-5678-9", "韩国"),
    ]
    
    print("\n识别不同国家/地区的 ISBN:")
    for isbn, expected in examples:
        group = ISBNUtils.get_registration_group(isbn)
        status = "✓" if group == expected else "✗"
        print(f"  {status} {isbn} → {group} (期望: {expected})")


def main():
    """运行所有示例"""
    example_basic_validation()
    example_strict_validation()
    example_conversion()
    example_parse()
    example_generate()
    example_extract()
    example_check_digit()
    example_registration_groups()
    
    print("\n" + "=" * 50)
    print("示例完成！")
    print("=" * 50)


if __name__ == '__main__':
    main()