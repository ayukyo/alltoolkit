"""
Width Utilities 使用示例

演示字符串显示宽度计算工具的各种用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    char_width, width, is_wide, is_combining, is_zero_width,
    truncate, pad_left, pad_right, center, align_columns,
    strip_ansi, width_with_ansi, split_by_width, wrap_text,
    chars_with_width, visualize_width
)


def example_basic_width():
    """基础宽度计算示例"""
    print("=" * 50)
    print("基础宽度计算")
    print("=" * 50)
    
    # ASCII 字符
    print(f"\nASCII 字符:")
    print(f"  'A' 的宽度: {char_width('A')}")
    print(f"  'Hello' 的宽度: {width('Hello')}")
    
    # CJK 字符
    print(f"\nCJK 字符:")
    print(f"  '中' 的宽度: {char_width('中')}")
    print(f"  '你好世界' 的宽度: {width('你好世界')}")
    
    # 混合字符串
    print(f"\n混合字符串:")
    print(f"  'Hello, 世界!' 的宽度: {width('Hello, 世界!')}")
    
    # 控制字符
    newline = '\n'
    hello_newline_world = 'Hello\nWorld'
    print(f"\n控制字符:")
    print(f"  newline 字符的宽度: {char_width(newline)}")
    print(f"  'Hello + newline + World' 的宽度: {width(hello_newline_world)}")
    
    # 组合字符
    combining_acute = '\u0301'
    cafe_combined = 'ca\u0301fe'
    print(f"\n组合字符:")
    print(f"  'é' (预组合) 的宽度: {char_width('é')}")
    print(f"  组合重音符号 (U+0301) 的宽度: {char_width(combining_acute)}")
    print(f"  'café' 的宽度: {width('café')}")
    print(f"  cafe + 组合符 的宽度: {width(cafe_combined)}")


def example_character_detection():
    """字符检测示例"""
    print("\n" + "=" * 50)
    print("字符类型检测")
    print("=" * 50)
    
    print(f"\n宽字符检测:")
    print(f"  'A' 是否为宽字符: {is_wide('A')}")
    print(f"  '中' 是否为宽字符: {is_wide('中')}")
    print(f"  'あ' 是否为宽字符: {is_wide('あ')}")
    print(f"  'Ａ' (全角) 是否为宽字符: {is_wide('Ａ')}")
    
    print(f"\n组合字符检测:")
    print(f"  'A' 是否为组合字符: {is_combining('A')}")
    combining_acute = '\u0301'
    print(f"  组合重音符号 (U+0301) 是否为组合字符: {is_combining(combining_acute)}")
    
    zero_width_space = '\u200B'
    newline = '\n'
    print(f"\n零宽度字符检测:")
    print(f"  'A' 是否为零宽度: {is_zero_width('A')}")
    print(f"  newline 字符是否为零宽度: {is_zero_width(newline)}")
    print(f"  零宽空格 (U+200B) 是否为零宽度: {is_zero_width(zero_width_space)}")


def example_truncate():
    """字符串截断示例"""
    print("\n" + "=" * 50)
    print("字符串截断")
    print("=" * 50)
    
    texts = [
        "Hello, World! This is a test.",
        "你好，世界！这是一个测试。",
        "Hello, 世界! Mixed content.",
    ]
    
    for text in texts:
        print(f"\n原文本: '{text}' (宽度: {width(text)})")
        for max_w in [10, 15, 20]:
            result = truncate(text, max_w)
            print(f"  截断到 {max_w}: '{result}' (宽度: {width(result)})")
    
    # 自定义省略号
    print(f"\n自定义省略号:")
    text = "Hello, World!"
    print(f"  原文本: '{text}'")
    print(f"  截断到 10 (ellipsis='...'): '{truncate(text, 10)}'")
    print(f"  截断到 10 (ellipsis='…'): '{truncate(text, 10, ellipsis='…')}'")
    print(f"  截断到 10 (ellipsis='[MORE]'): '{truncate(text, 10, ellipsis='[MORE]')}'")


def example_alignment():
    """字符串对齐示例"""
    print("\n" + "=" * 50)
    print("字符串对齐")
    print("=" * 50)
    
    texts = [
        "Hello",
        "你好",
        "Hello世界",
    ]
    
    target_width = 12
    
    print(f"\n目标宽度: {target_width}")
    for text in texts:
        print(f"\n原文本: '{text}' (宽度: {width(text)})")
        print(f"  左填充: |{pad_left(text, target_width)}|")
        print(f"  右填充: |{pad_right(text, target_width)}|")
        print(f"  居中:   |{center(text, target_width)}|")
    
    # 自定义填充字符
    print(f"\n自定义填充字符:")
    print(f"  左填充 '-': |{pad_left('你好', 10, fill_char='-')}|")
    print(f"  右填充 '_': |{pad_right('Hello', 10, fill_char='_')}|")
    print(f"  居中 '=': |{center('Test', 10, fill_char='=')}|")


def example_table():
    """表格对齐示例"""
    print("\n" + "=" * 50)
    print("表格对齐")
    print("=" * 50)
    
    # 简单 ASCII 表格
    rows = [
        ['Name', 'Age', 'City'],
        ['Alice', '25', 'New York'],
        ['Bob', '30', 'Los Angeles'],
        ['Charlie', '35', 'Chicago'],
    ]
    
    print("\nASCII 表格:")
    for row in align_columns(rows):
        print(f"  {row}")
    
    # 混合 CJK 表格
    rows = [
        ['姓名', '年龄', '城市'],
        ['张三', '25', '北京'],
        ['李四', '30', '上海'],
        ['王五', '35', '广州'],
    ]
    
    print("\nCJK 表格:")
    for row in align_columns(rows):
        print(f"  {row}")
    
    # 混合表格
    rows = [
        ['Name', '年龄', 'Location'],
        ['Alice', '25', '北京'],
        ['Bob张', '30', 'New York'],
    ]
    
    print("\n混合表格:")
    for row in align_columns(rows):
        print(f"  {row}")
    
    # 自定义分隔符
    rows = [['A', 'B'], ['C', 'D']]
    print("\n自定义分隔符 (separator=' || '):")
    for row in align_columns(rows, separator=' || '):
        print(f"  {row}")


def example_ansi():
    """ANSI 转义序列示例"""
    print("\n" + "=" * 50)
    print("ANSI 转义序列处理")
    print("=" * 50)
    
    # ANSI 彩色文本
    colored_text = "\x1b[31mHello\x1b[0m \x1b[32mWorld\x1b[0m"
    print(f"\n彩色文本 (实际显示为红绿): '{colored_text}'")
    print(f"  移除 ANSI 后: '{strip_ansi(colored_text)}'")
    print(f"  带 ANSI 的宽度: {width_with_ansi(colored_text)}")
    print(f"  移除 ANSI 后的宽度: {width(strip_ansi(colored_text))}")
    
    # ANSI + CJK
    colored_cjk = "\x1b[31m你好\x1b[0m"
    print(f"\n彩色 CJK 文本: '{colored_cjk}'")
    print(f"  移除 ANSI 后: '{strip_ansi(colored_cjk)}'")
    print(f"  带 ANSI 的宽度: {width_with_ansi(colored_cjk)}")


def example_split():
    """按宽度分割示例"""
    print("\n" + "=" * 50)
    print("按宽度分割")
    print("=" * 50)
    
    texts = [
        "HelloWorld",
        "你好世界测试",
        "Hello你好World世界",
    ]
    
    for text in texts:
        print(f"\n原文本: '{text}' (宽度: {width(text)})")
        for max_w in [5, 10]:
            result = split_by_width(text, max_w)
            print(f"  按宽度 {max_w} 分割: {result}")
            for part in result:
                print(f"    '{part}' (宽度: {width(part)})")


def example_wrap():
    """文本换行示例"""
    print("\n" + "=" * 50)
    print("文本换行")
    print("=" * 50)
    
    texts = [
        "Hello World This is a test of wrapping functionality.",
        "你好世界这是一个测试文本换行功能演示。",
        "Hello 世界 Mixed content 测试换行功能。",
    ]
    
    width_limits = [15, 20]
    
    for text in texts:
        print(f"\n原文本: '{text}'")
        for limit in width_limits:
            lines = wrap_text(text, limit)
            print(f"  换行宽度 {limit}:")
            for line in lines:
                print(f"    '{line}' (宽度: {width(line)})")


def example_visualize():
    """宽度可视化示例"""
    print("\n" + "=" * 50)
    print("宽度可视化")
    print("=" * 50)
    
    texts = [
        "Hello",
        "你好",
        "Hello你好",
        "café",
        "\x1b[31mText\x1b[0m",
    ]
    
    for text in texts:
        clean = strip_ansi(text)
        print(f"\n文本: '{text}'")
        print(f"  清理后: '{clean}'")
        print(f"  宽度可视化: {visualize_width(clean)}")
        print(f"  自定义可视化: {visualize_width(clean, narrow_char='-', wide_char='##')}")
    
    # 显示字符宽度详情
    print(f"\n字符宽度详情:")
    text = "Hello你好ABC"
    print(f"  文本: '{text}'")
    for char, w in chars_with_width(text):
        print(f"    '{char}' -> 宽度 {w}")


def example_terminal_ui():
    """终端 UI 应用示例"""
    print("\n" + "=" * 50)
    print("终端 UI 应用")
    print("=" * 50)
    
    # 模拟进度条
    def simulate_progress_bar(percent, width=50):
        filled = int(width * percent)
        bar = '█' * filled + '░' * (width - filled)
        label = truncate(f"{percent*100:.1f}%", 10, ellipsis='')
        return f"[{bar}] {pad_left(label, 8)}"
    
    print("\n进度条示例:")
    for p in [0.0, 0.25, 0.5, 0.75, 1.0]:
        print(f"  {simulate_progress_bar(p)}")
    
    # 模拟状态行
    def status_line(status, message, width=60):
        truncated_msg = truncate(message, width - width(status) - 3)
        return pad_right(f"{status}: {truncated_msg}", width)
    
    print("\n状态行示例:")
    statuses = [
        ("OK", "Operation completed successfully"),
        ("WARN", "Warning: 缓存空间不足，请及时清理"),
        ("ERROR", "Error: 连接失败 Connection timeout"),
    ]
    for status, msg in statuses:
        print(f"  |{status_line(status, msg)}|")
    
    # 模拟菜单
    def menu_header(title, width=40):
        return center(f"=== {title} ===", width, fill_char='-')
    
    def menu_item(index, text, width=40):
        num = f"{index}."
        content = truncate(text, width - 4)
        return pad_right(f"  {num} {content}", width)
    
    print("\n菜单示例:")
    print(menu_header("系统菜单", 30))
    items = ["用户管理", "系统设置 Settings", "数据备份 Backup", "退出系统 Exit"]
    for i, item in enumerate(items, 1):
        print(menu_item(i, item, 30))
    print(center("", 30, fill_char='-'))


def example_cli_output():
    """命令行输出格式化示例"""
    print("\n" + "=" * 50)
    print("命令行输出格式化")
    print("=" * 50)
    
    # 日志格式化
    def format_log(level, message, width=80):
        level_str = pad_right(f"[{level}]", 8)
        msg = truncate(message, width - 10)
        return level_str + msg
    
    print("\n日志格式化:")
    logs = [
        ("INFO", "Application started successfully"),
        ("WARN", "配置文件缺失 Missing config file"),
        ("ERROR", "数据库连接失败 Database connection failed after 3 retries"),
    ]
    for level, msg in logs:
        print(format_log(level, msg))
    
    # 列表格式化
    def format_list(items, indent=2, width=40):
        result = []
        for item in items:
            line = " " * indent + truncate(item, width - indent)
            result.append(pad_right(line, width))
        return result
    
    print("\n列表格式化:")
    items = ["First item 第一项", "Second item 第二项", "Third item 第三项"]
    for line in format_list(items):
        print(line)


def main():
    """运行所有示例"""
    example_basic_width()
    example_character_detection()
    example_truncate()
    example_alignment()
    example_table()
    example_ansi()
    example_split()
    example_wrap()
    example_visualize()
    example_terminal_ui()
    example_cli_output()
    
    print("\n" + "=" * 50)
    print("所有示例完成!")
    print("=" * 50)


if __name__ == '__main__':
    main()