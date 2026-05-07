"""
ISBN Utils 使用示例

本示例展示isbn_utils模块的主要功能：
- ISBN验证
- ISBN-10/ISBN-13转换
- 检验位计算
- 格式化和解析
- 文本提取
- 批量操作

运行方式：从AllToolkit目录运行
cd /home/admin/.openclaw/workspace/AllToolkit
python -c "import sys; sys.path.insert(0, 'Python'); exec(open('Python/isbn_utils/examples/basic_usage.py').read()); run_all_examples()"
"""

import sys
import os

# 添加Python目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
python_dir = os.path.dirname(os.path.dirname(script_dir))
if python_dir not in sys.path:
    sys.path.insert(0, python_dir)

from isbn_utils import (
    ISBN, ISBNType,
    is_valid_isbn10, is_valid_isbn13, is_valid_isbn,
    calculate_isbn10_check_digit, calculate_isbn13_check_digit,
    isbn10_to_isbn13, isbn13_to_isbn10,
    format_isbn, normalize_isbn,
    parse_isbn, extract_isbns, get_isbn_info,
    batch_validate, identify_prefix
)


def example_basic_validation():
    """基础验证示例"""
    print("=" * 50)
    print("基础验证示例")
    print("=" * 50)
    
    # ISBN-10验证
    isbn10_examples = [
        '0306406152',      # 无分隔符
        '0-306-40615-2',   # 带分隔符
        '080442957X',      # X检验位
        '0306406153',      # 无效（错误检验位）
    ]
    
    print("\nISBN-10验证:")
    for isbn in isbn10_examples:
        result = is_valid_isbn10(isbn)
        print(f"  {isbn}: {'有效' if result else '无效'}")
    
    # ISBN-13验证
    isbn13_examples = [
        '9780306406157',        # 无分隔符
        '978-0-306-40615-7',   # 带分隔符
        '9791091146135',       # 979前缀
        '9780306406150',       # 无效（错误检验位）
    ]
    
    print("\nISBN-13验证:")
    for isbn in isbn13_examples:
        result = is_valid_isbn13(isbn)
        print(f"  {isbn}: {'有效' if result else '无效'}")
    
    # 自动检测类型验证
    print("\n自动检测验证:")
    mixed_examples = ['0306406152', '9780306406157', 'invalid']
    for isbn in mixed_examples:
        result = is_valid_isbn(isbn)
        print(f"  {isbn}: {'有效' if result else '无效'}")


def example_check_digit_calculation():
    """检验位计算示例"""
    print("\n" + "=" * 50)
    print("检验位计算示例")
    print("=" * 50)
    
    # ISBN-10检验位
    print("\nISBN-10检验位计算:")
    digits = ['030640615', '047195869', '080442957', '000000000']
    for d in digits:
        check = calculate_isbn10_check_digit(d)
        print(f"  {d} -> 检验位: {check} (完整: {d}{check})")
    
    # ISBN-13检验位
    print("\nISBN-13检验位计算:")
    digits13 = ['978030640615', '978156619909', '979109114613']
    for d in digits13:
        check = calculate_isbn13_check_digit(d)
        print(f"  {d} -> 检验位: {check} (完整: {d}{check})")


def example_conversion():
    """格式转换示例"""
    print("\n" + "=" * 50)
    print("格式转换示例")
    print("=" * 50)
    
    # ISBN-10转ISBN-13
    print("\nISBN-10 → ISBN-13:")
    conversions = [
        ('0-306-40615-2', '9780306406157'),
        ('1-56619-909-3', '9781566199094'),
    ]
    for isbn10, expected13 in conversions:
        result = isbn10_to_isbn13(isbn10)
        print(f"  {isbn10} → {result} (期望: {expected13})")
    
    # ISBN-13转ISBN-10
    print("\nISBN-13 → ISBN-10:")
    conversions = [
        ('978-0-306-40615-7', '0306406152'),
        ('978-1-56619-909-4', '1566199093'),
    ]
    for isbn13, expected10 in conversions:
        result = isbn13_to_isbn10(isbn13)
        print(f"  {isbn13} → {result} (期望: {expected10})")
    
    # 979前缀无法转换
    print("\n979前缀无法转ISBN-10:")
    isbn979 = '9791091146135'
    result = isbn13_to_isbn10(isbn979)
    print(f"  {isbn979} → {result} (无法转换)")


def example_formatting():
    """格式化示例"""
    print("\n" + "=" * 50)
    print("格式化示例")
    print("=" * 50)
    
    # 标准化（移除分隔符）
    print("\n标准化（移除分隔符）:")
    examples = ['978-0-306-40615-7', '0 306 40615 2', '0-80442-957-X']
    for isbn in examples:
        result = normalize_isbn(isbn)
        print(f"  {isbn} → {result}")
    
    # 格式化（添加分隔符）
    print("\n格式化（添加分隔符）:")
    examples = ['9780306406157', '0306406152']
    for isbn in examples:
        result = format_isbn(isbn)
        print(f"  {isbn} → {result}")
    
    # 自定义分隔符
    print("\n自定义分隔符:")
    isbn = '9780306406157'
    print(f"  默认: {format_isbn(isbn)}")
    print(f"  空格: {format_isbn(isbn, ' ')}")
    print(f"  无分隔: {format_isbn(isbn, '')}")


def example_isbn_class():
    """ISBN类使用示例"""
    print("\n" + "=" * 50)
    print("ISBN类使用示例")
    print("=" * 50)
    
    # 创建ISBN对象
    isbn = ISBN('978-0-306-40615-7')
    
    print(f"\n原始输入: {isbn._raw}")
    print(f"是否有效: {isbn.is_valid()}")
    print(f"类型: {isbn.get_type()}")
    print(f"标准化: {isbn.normalize()}")
    print(f"格式化: {isbn.format()}")
    
    # 转换
    print(f"\n转ISBN-13: {isbn.to_isbn13()}")
    print(f"转ISBN-10: {isbn.to_isbn10()}")
    
    # 获取详细信息
    info = isbn.get_info()
    print(f"\n详细信息:")
    print(f"  检验位: {info.check_digit}")
    print(f"  前缀: {info.prefix}")


def example_extract_isbns():
    """文本提取ISBN示例"""
    print("\n" + "=" * 50)
    print("从文本提取ISBN示例")
    print("=" * 50)
    
    texts = [
        "这本书的ISBN是978-0-306-40615-7",
        "ISBN: 0-306-40615-2，另一本9781566199094",
        "书单：ISBN-13 9780306406157, ISBN-10 080442957X",
        "普通文本没有ISBN",
    ]
    
    for text in texts:
        isbns = extract_isbns(text)
        print(f"\n文本: \"{text}\"")
        print(f"提取: {isbns if isbns else '无'}")


def example_batch_validate():
    """批量验证示例"""
    print("\n" + "=" * 50)
    print("批量验证示例")
    print("=" * 50)
    
    isbns = [
        '978-0-306-40615-7',
        '0-306-40615-2',
        '9781566199094',
        'invalid-isbn',
        '1234567890',
        '080442957X',
    ]
    
    result = batch_validate(isbns)
    
    print(f"\n输入列表: {isbns}")
    print(f"\n统计:")
    print(f"  总数: {result['stats']['total']}")
    print(f"  有效: {result['stats']['valid_count']}")
    print(f"  无效: {result['stats']['invalid_count']}")
    print(f"  ISBN-10: {result['stats']['isbn10_count']}")
    print(f"  ISBN-13: {result['stats']['isbn13_count']}")
    
    print(f"\n有效ISBN:")
    for isbn in result['valid']:
        print(f"  {isbn}")
    
    print(f"\n无效ISBN:")
    for isbn in result['invalid']:
        print(f"  {isbn}")


def example_identify_prefix():
    """分组识别示例"""
    print("\n" + "=" * 50)
    print("分组前缀识别示例")
    print("=" * 50)
    
    prefixes = ['0', '1', '7', '4', '3', '2', '957', '962']
    
    for prefix in prefixes:
        group = identify_prefix(prefix)
        print(f"  前缀 {prefix}: {group if group else '未知'}")


def example_parsing():
    """详细解析示例"""
    print("\n" + "=" * 50)
    print("详细解析示例")
    print("=" * 50)
    
    examples = ['978-0-306-40615-7', '0-306-40615-2', '080442957X']
    
    for isbn in examples:
        info = parse_isbn(isbn)
        print(f"\nISBN: {isbn}")
        print(f"  类型: {info.isbn_type.value}")
        print(f"  有效: {info.is_valid}")
        print(f"  标准化: {info.normalized}")
        print(f"  格式化: {info.formatted}")
        print(f"  检验位: {info.check_digit}")
        if info.isbn_type == ISBNType.ISBN13:
            print(f"  前缀: {info.prefix}")
            print(f"  ISBN-10: {info.isbn10}")
        else:
            print(f"  ISBN-13: {info.isbn13}")


def run_all_examples():
    """运行所有示例"""
    example_basic_validation()
    example_check_digit_calculation()
    example_conversion()
    example_formatting()
    example_isbn_class()
    example_extract_isbns()
    example_batch_validate()
    example_identify_prefix()
    example_parsing()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成")
    print("=" * 50)


if __name__ == '__main__':
    run_all_examples()