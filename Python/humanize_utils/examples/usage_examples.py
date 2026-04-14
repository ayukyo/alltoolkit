"""
humanize_utils 使用示例
展示人性化格式工具的各种用法
"""

import sys
import os

# 添加父目录到路径以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    format_bytes, parse_size,
    format_number, format_percentage, format_with_commas,
    format_duration, format_relative_time, format_time_ago,
    format_list,
    format_phone, format_card_number, truncate_text, format_ordinal,
    format_json
)


def print_section(title):
    """打印分隔线"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)


def demo_file_size():
    """演示文件大小格式化"""
    print_section("文件大小格式化")
    
    sizes = [0, 100, 1024, 1536, 1048576, 1572864, 1073741824, 1099511627776]
    
    print("\n十进制单位 (KB, MB, GB):")
    for size in sizes:
        print(f"  {size:>15} bytes = {format_bytes(size)}")
    
    print("\n二进制单位 (KiB, MiB, GiB):")
    for size in [1024, 1048576, 1073741824]:
        print(f"  {size:>15} bytes = {format_bytes(size, binary=True)}")
    
    print("\n解析大小字符串:")
    size_strings = ["1KB", "1.5MB", "2GB", "1KiB", "1MiB"]
    for s in size_strings:
        print(f"  {s:>6} = {parse_size(s):,} bytes")


def demo_numbers():
    """演示数字格式化"""
    print_section("数字格式化")
    
    numbers = [100, 999, 1000, 1500, 10000, 15000, 100000, 1000000, 1500000, 1000000000]
    
    print("\n数字缩写:")
    for n in numbers:
        print(f"  {n:>15,} = {format_number(n)}")
    
    print("\n中文单位:")
    chinese_numbers = [100, 1000, 10000, 15000, 100000, 1000000, 100000000, 1000000000000]
    for n in chinese_numbers:
        print(f"  {n:>15,} = {format_number(n, use_chinese=True)}")
    
    print("\n千分位格式化:")
    for n in [1000, 12345, 1234567, 1234567890]:
        print(f"  {n:>15,} = {format_with_commas(n)}")
    
    print("\n百分比格式化:")
    values = [0.5, 0.256, 0.75, 50, 75.5]
    for v in values:
        print(f"  {v} = {format_percentage(v, precision=1)}")


def demo_time():
    """演示时间格式化"""
    print_section("时间格式化")
    
    durations = [0, 5, 60, 65, 3600, 3665, 86400, 90061]
    
    print("\n持续时间格式化:")
    for d in durations:
        print(f"  {d:>6} 秒 = {format_duration(d, format_type='full')} | "
              f"{format_duration(d, format_type='compact')} | "
              f"{format_duration(d, format_type='text', use_chinese=True)}")
    
    print("\n相对时间 (假设当前时间):")
    import time
    now = time.time()
    offsets = [-30, -300, -3600, -86400, -2592000, -31536000, 3600]
    for offset in offsets:
        timestamp = now + offset
        result = format_relative_time(timestamp, reference=now)
        if offset > 0:
            print(f"  {offset:>8} 秒后 = {result}")
        else:
            print(f"  {abs(offset):>8} 秒前 = {result}")


def demo_list():
    """演示列表格式化"""
    print_section("列表格式化")
    
    lists = [
        ["苹果"],
        ["苹果", "香蕉"],
        ["苹果", "香蕉", "橙子"],
        ["苹果", "香蕉", "橙子", "葡萄", "西瓜", "草莓"],
    ]
    
    print("\n中文格式:")
    for lst in lists:
        print(f"  {lst} -> {format_list(lst)}")
    
    print("\n英文格式:")
    for lst in lists:
        print(f"  {lst} -> {format_list(lst, use_chinese=False)}")
    
    print("\n带限制:")
    long_list = ["项目" + str(i) for i in range(1, 11)]
    print(f"  {long_list[:3]}...")
    print(f"  限制显示3项: {format_list(long_list, limit=3)}")


def demo_phone_card():
    """演示电话和银行卡格式化"""
    print_section("电话和银行卡格式化")
    
    print("\n电话号码格式化:")
    phones = ["13800000000", "15912345678"]
    formats = ["standard", "hyphen", "international"]
    for phone in phones:
        for fmt in formats:
            print(f"  {phone} ({fmt}): {format_phone(phone, format_type=fmt)}")
    
    print("\n银行卡号格式化:")
    cards = ["6222021234567890123", "6217001234567891234"]
    for card in cards:
        print(f"  {card}")
        print(f"    普通格式: {format_card_number(card)}")
        print(f"    遮盖格式: {format_card_number(card, mask=True)}")


def demo_text():
    """演示文本处理"""
    print_section("文本处理")
    
    print("\n文本截断:")
    texts = [
        ("这是一段很短的文本", 20),
        ("这是一段比较长的文本需要被截断处理才能正常显示", 20),
        ("Hello world this is a long sentence that needs to be truncated", 30),
    ]
    for text, max_len in texts:
        result = truncate_text(text, max_length=max_len)
        print(f"  原文: {text[:30]}...")
        print(f"  截断: {result}")
        print()
    
    print("序数词:")
    for n in [1, 2, 3, 4, 11, 21, 22, 23, 100]:
        print(f"  {n} -> {format_ordinal(n)} (英文) / {format_ordinal(n, use_chinese=True)} (中文)")


def demo_json():
    """演示 JSON 格式化"""
    print_section("JSON 格式化")
    
    data = {
        "name": "张三",
        "age": 25,
        "hobbies": ["阅读", "游泳", "编程"],
        "address": {
            "city": "北京",
            "street": "朝阳区xxx路xxx号"
        }
    }
    
    print("\n格式化输出:")
    print(format_json(data))


def main():
    """主函数"""
    print("\n" + "="*60)
    print("       humanize_utils 人性化格式工具 - 使用示例")
    print("="*60)
    
    demo_file_size()
    demo_numbers()
    demo_time()
    demo_list()
    demo_phone_card()
    demo_text()
    demo_json()
    
    print("\n" + "="*60)
    print("  示例演示完成！")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()