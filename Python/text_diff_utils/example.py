#!/usr/bin/env python3
"""
文本差异比较工具示例

演示如何使用 text_diff_utils 模块进行文本差异比较。
"""

from mod import (
    TextDiffUtils,
    compare_texts,
    get_unified_diff,
    get_similarity,
    format_diff_summary,
    format_side_by_side
)


def demo_basic_comparison():
    """演示基本文本比较"""
    print("=" * 60)
    print("1. 基本文本比较")
    print("=" * 60)
    
    old_text = """def hello():
    print("Hello, World!")
    return True

def goodbye():
    print("Goodbye!")
    return False"""
    
    new_text = """def hello():
    print("Hello, Python!")
    return True

def farewell():
    print("Farewell!")
    return False"""
    
    # 使用便捷函数进行比较
    result = compare_texts(old_text, new_text)
    
    # 打印差异摘要
    print(format_diff_summary(result))
    print()


def demo_unified_diff():
    """演示统一格式差异"""
    print("=" * 60)
    print("2. 统一格式差异 (类似 git diff)")
    print("=" * 60)
    
    old_code = """def calculate(x, y):
    return x + y

def process(data):
    result = []
    for item in data:
        result.append(item)
    return result"""
    
    new_code = """def calculate(x, y, z=0):
    return x + y + z

def process(data, transform=None):
    result = []
    for item in data:
        if transform:
            item = transform(item)
        result.append(item)
    return result

def validate(data):
    return all(item is not None for item in data)"""
    
    # 生成统一格式差异
    diff = get_unified_diff(old_code, new_code, "original.py", "modified.py")
    print(diff)
    print()


def demo_side_by_side():
    """演示并排对比"""
    print("=" * 60)
    print("3. 并排对比视图")
    print("=" * 60)
    
    old_text = """Configuration:
    debug: false
    port: 8080
    host: localhost
    workers: 4"""
    
    new_text = """Configuration:
    debug: true
    port: 3000
    host: 0.0.0.0
    workers: 8
    timeout: 30"""
    
    utils = TextDiffUtils()
    pairs = utils.side_by_side(old_text, new_text, width=30)
    
    print(format_side_by_side(pairs, "配置文件对比"))
    print()


def demo_char_level_diff():
    """演示字符级差异"""
    print("=" * 60)
    print("4. 字符级差异检测")
    print("=" * 60)
    
    old_str = "The quick brown fox jumps over the lazy dog."
    new_str = "The quick brown cat jumps over the lazy dog."
    
    utils = TextDiffUtils()
    diffs = utils.char_diff(old_str, new_str)
    
    print(f"原文本: {old_str}")
    print(f"新文本: {new_str}")
    print("\n字符级差异:")
    
    for diff_type, text in diffs:
        symbol = {
            'equal': ' ',
            'insert': '+',
            'delete': '-',
            'replace': '~'
        }[diff_type.value]
        
        if diff_type.value == 'equal':
            print(f"  {symbol} {text!r}")
        else:
            print(f"  {symbol} \033[91m{text!r}\033[0m")  # 红色高亮
    
    print()


def demo_similarity():
    """演示相似度计算"""
    print("=" * 60)
    print("5. 文本相似度计算")
    print("=" * 60)
    
    texts = [
        ("Hello World", "Hello World", "完全相同"),
        ("Hello World", "Hello Python", "部分相同"),
        ("Hello World", "Goodbye Universe", "完全不同"),
        ("The quick brown fox", "The quick brown dog", "大部分相同"),
    ]
    
    print(f"{'文本 A':<25} {'文本 B':<25} {'相似度':<10} {'说明'}")
    print("-" * 75)
    
    for text_a, text_b, desc in texts:
        sim = get_similarity(text_a, text_b)
        print(f"{text_a:<25} {text_b:<25} {sim:>8.2%}  {desc}")
    
    print()


def demo_ignore_options():
    """演示忽略选项"""
    print("=" * 60)
    print("6. 忽略选项演示")
    print("=" * 60)
    
    text1 = "HELLO WORLD\nSecond Line"
    text2 = "hello world\nSecond Line"
    
    # 不忽略大小写
    utils_normal = TextDiffUtils()
    sim_normal = utils_normal.similarity(text1, text2)
    
    # 忽略大小写
    utils_ignore_case = TextDiffUtils(ignore_case=True)
    sim_ignore_case = utils_ignore_case.similarity(text1, text2)
    
    print(f"文本 A: {text1!r}")
    print(f"文本 B: {text2!r}")
    print()
    print(f"不忽略大小写: {sim_normal:.2%}")
    print(f"忽略大小写:   {sim_ignore_case:.2%}")
    print()
    
    # 忽略空白字符
    text3 = "Hello   World"
    text4 = "Hello World"
    
    utils_ignore_ws = TextDiffUtils(ignore_whitespace=True)
    sim_ignore_ws = utils_ignore_ws.similarity(text3, text4)
    
    print(f"文本 A: {text3!r}")
    print(f"文本 B: {text4!r}")
    print(f"忽略空白字符: {sim_ignore_ws:.2%}")
    print()


def demo_find_matches():
    """演示查找公共子串"""
    print("=" * 60)
    print("7. 查找公共子串")
    print("=" * 60)
    
    text1 = "The quick brown fox jumps over the lazy dog"
    text2 = "A quick brown cat runs over the lazy mouse"
    
    utils = TextDiffUtils()
    matches = utils.find_matches(text1, text2, min_length=5)
    
    print(f"文本 A: {text1}")
    print(f"文本 B: {text2}")
    print("\n公共子串 (长度 >= 5):")
    
    for substring, pos_a, pos_b in matches:
        print(f"  '{substring}' (A: {pos_a}, B: {pos_b})")
    
    print()


def demo_diff_stats():
    """演示差异统计"""
    print("=" * 60)
    print("8. 差异统计信息")
    print("=" * 60)
    
    old_text = """class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b"""
    
    new_text = """class Calculator:
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def subtract(self, a, b):
        return a - b"""
    
    utils = TextDiffUtils()
    stats = utils.diff_stats(old_text, new_text)
    
    print("差异统计:")
    print(f"  原文本行数: {stats['old_lines']}")
    print(f"  新文本行数: {stats['new_lines']}")
    print(f"  新增行数:   {stats['added_lines']}")
    print(f"  删除行数:   {stats['deleted_lines']}")
    print(f"  修改行数:   {stats['changed_lines']}")
    print(f"  相似度:     {stats['similarity']}%")
    print(f"  差异比例:   {stats['diff_percentage']}%")
    print(f"  是否相同:   {'是' if stats['is_identical'] else '否'}")
    print()


def demo_practical_use_case():
    """演示实际应用场景"""
    print("=" * 60)
    print("9. 实际应用：配置文件变更检测")
    print("=" * 60)
    
    old_config = """[database]
host = localhost
port = 5432
name = mydb
user = admin
password = secret123

[server]
host = 0.0.0.0
port = 8080
debug = false"""
    
    new_config = """[database]
host = db.example.com
port = 5432
name = production_db
user = app_user
password = ${DB_PASSWORD}

[server]
host = 0.0.0.0
port = 443
ssl = true
debug = false"""
    
    print("原配置:")
    print("-" * 40)
    print(old_config)
    print()
    
    print("新配置:")
    print("-" * 40)
    print(new_config)
    print()
    
    # 生成差异报告
    diff = get_unified_diff(old_config, new_config, "config.old", "config.new")
    
    print("差异报告:")
    print("-" * 40)
    print(diff)
    print()
    
    # 统计信息
    stats = TextDiffUtils().diff_stats(old_config, new_config)
    print(f"变更统计: 新增 {stats['added_lines']} 行, 删除 {stats['deleted_lines']} 行, 相似度 {stats['similarity']}%")
    print()


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("文本差异比较工具 (text_diff_utils) 示例")
    print("=" * 60 + "\n")
    
    demo_basic_comparison()
    demo_unified_diff()
    demo_side_by_side()
    demo_char_level_diff()
    demo_similarity()
    demo_ignore_options()
    demo_find_matches()
    demo_diff_stats()
    demo_practical_use_case()
    
    print("=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()