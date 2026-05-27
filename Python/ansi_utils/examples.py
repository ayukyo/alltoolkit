#!/usr/bin/env python3
"""
ANSI Utils 使用示例

运行: python examples.py
"""

import time
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ansi_utils.mod import (
    ANSI, Cursor, Screen, Style, ProgressBar, Table,
    strip_ansi, colorize, rainbow, gradient,
    red, green, yellow, blue, magenta, cyan, white,
    bright_red, bright_green, bright_yellow, bright_blue,
    bright_magenta, bright_cyan, bright_white
)


def print_header(title: str):
    """打印带分隔的标题"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def example_basic_colors():
    """基本颜色示例"""
    print_header("基本颜色")
    
    print("\n标准颜色:")
    print(f"  {red('红色文本')} - danger/error")
    print(f"  {green('绿色文本')} - success/ok")
    print(f"  {yellow('黄色文本')} - warning")
    print(f"  {blue('蓝色文本')} - info")
    print(f"  {magenta('品红文本')} - highlight")
    print(f"  {cyan('青色文本')} - info2")
    print(f"  {white('白色文本')} - normal")
    
    print("\n亮色:")
    print(f"  {bright_red('亮红色')}")
    print(f"  {bright_green('亮绿色')}")
    print(f"  {bright_yellow('亮黄色')}")
    print(f"  {bright_blue('亮蓝色')}")
    print(f"  {bright_magenta('亮品红')}")
    print(f"  {bright_cyan('亮青色')}")
    print(f"  {bright_white('亮白色')}")


def example_256_colors():
    """256 色示例"""
    print_header("256 色")
    
    print("\n颜色条 (0-255):")
    
    # 标准 16 色
    print("标准 16 色:")
    for i in range(16):
        print(f"{ANSI.bg(i)}  {ANSI.RESET}", end='')
        if (i + 1) % 8 == 0:
            print()
    
    # 6x6x6 色立方
    print("\n色立方 (16-231):")
    for i in range(16, 232):
        print(f"{ANSI.bg(i)}  {ANSI.RESET}", end='')
        if (i - 15) % 36 == 0:
            print()
    
    # 灰度
    print("\n灰度 (232-255):")
    for i in range(232, 256):
        print(f"{ANSI.bg(i)}  {ANSI.RESET}", end='')
    print()


def example_true_color():
    """真彩色示例"""
    print_header("真彩色 (RGB)")
    
    print("\n自定义颜色:")
    print(f"  {ANSI.fg((255, 100, 100))}淡红色{ANSI.RESET}")
    print(f"  {ANSI.fg((100, 255, 100))}淡绿色{ANSI.RESET}")
    print(f"  {ANSI.fg((100, 100, 255))}淡蓝色{ANSI.RESET}")
    
    # 渐变示例
    print("\n渐变文本:")
    text = gradient("Hello, World!", (255, 50, 50), (50, 50, 255))
    print(f"  {text}")


def example_styles():
    """文本样式示例"""
    print_header("文本样式")
    
    print(f"\n粗体: {ANSI.bold('这是粗体文本')}")
    print(f"暗淡: {ANSI.dim('这是暗淡文本')}")
    print(f"斜体: {ANSI.italic('这是斜体文本')}")
    print(f"下划线: {ANSI.underline('这是下划线文本')}")
    print(f"删除线: {ANSI.strikethrough('这是删除线文本')}")
    print(f"闪烁: {ANSI.blink('这是闪烁文本')} (可能不支持)")
    print(f"反转: {ANSI.reverse('这是反转文本')}")
    
    print("\n组合样式:")
    s = Style("组合样式").bold().italic().fg('yellow').bg('blue')
    print(f"  {s}")


def example_style_builder():
    """链式样式构建器示例"""
    print_header("链式样式构建器")
    
    print("\n链式调用:")
    s1 = Style("错误消息").bold().fg('red')
    print(f"  {s1}")
    
    s2 = Style("成功消息").bold().fg('green')
    print(f"  {s2}")
    
    s3 = Style("警告消息").bold().fg('yellow')
    print(f"  {s3}")
    
    s4 = Style().bold().underline().fg('cyan').text("带下划线的青色")
    print(f"  {s4}")
    
    print("\n带前后缀:")
    s5 = Style("状态").fg('green').prefix('[OK] ').suffix(' ✓')
    print(f"  {s5}")


def example_rainbow():
    """彩虹色示例"""
    print_header("彩虹色文本")
    
    text = "Hello, Rainbow World! 🌈"
    print(f"\n{rainbow(text)}")
    
    text2 = "这是一个彩虹色的测试文本"
    print(f"\n{rainbow(text2)}")


def example_colorize():
    """colorize 函数示例"""
    print_header("colorize 快捷函数")
    
    print("\n快速着色:")
    print(f"  {colorize('重要', fg='red', bold=True)}")
    print(f"  {colorize('成功', fg='green', bold=True)}")
    print(f"  {colorize('警告', fg='yellow', underline=True)}")
    print(f"  {colorize('信息', fg='blue', italic=True)}")
    
    print("\n带背景色:")
    print(f"  {colorize(' ERROR ', fg='white', bg='red', bold=True)}")
    print(f"  {colorize(' OK ', fg='white', bg='green', bold=True)}")
    print(f"  {colorize(' WARN ', fg='black', bg='yellow', bold=True)}")
    
    print("\nRGB 颜色:")
    print(f"  {colorize('自定义紫色', fg=(128, 0, 255))}")
    print(f"  {colorize('自定义橙色', fg=(255, 128, 0))}")


def example_cursor():
    """光标控制示例"""
    print_header("光标控制")
    
    print("\n光标移动演示 (等待 2 秒):")
    print("正在倒计时: 3")
    time.sleep(0.5)
    
    # 上移一行，清除行，重新打印
    print(f"{Cursor.up(1)}{Cursor.column(1)}正在倒计时: 2", end='', flush=True)
    time.sleep(0.5)
    
    print(f"{Cursor.up(1)}{Cursor.column(1)}正在倒计时: 1", end='', flush=True)
    time.sleep(0.5)
    
    print(f"{Cursor.up(1)}{Cursor.column(1)}正在倒计时: 完成!          ")
    
    print("\n注意: 光标控制在某些终端可能不可见效果")


def example_progress_bar():
    """进度条示例"""
    print_header("进度条")
    
    print("\n基本进度条:")
    bar = ProgressBar(total=100, width=40)
    for i in range(0, 101, 10):
        print(f"\r{bar.update(i)}", end='', flush=True)
        time.sleep(0.1)
    print()
    
    print("\n自定义样式进度条:")
    style = Style().fg('green').bold()
    bar = ProgressBar(total=100, width=30, filled_char='█', empty_char='░', style=style)
    for i in range(0, 101, 5):
        print(f"\r{bar.update(i)}", end='', flush=True)
        time.sleep(0.05)
    print()
    
    print("\nEmoji 进度条:")
    bar = ProgressBar(total=100, width=20, filled_char='🔥', empty_char='💤')
    for i in range(0, 101, 20):
        print(f"\r{bar.update(i)}", end='', flush=True)
        time.sleep(0.15)
    print()


def example_table():
    """表格示例"""
    print_header("表格")
    
    print("\n基本表格:")
    table = Table(headers=['Name', 'Age', 'City'])
    table.add_row('Alice', '25', 'Beijing')
    table.add_row('Bob', '30', 'Shanghai')
    table.add_row('Charlie', '35', 'Guangzhou')
    print(table.render())
    
    print("\n带颜色的表格:")
    table = Table(headers=['Status', 'Count', 'Percentage'])
    table.add_row(colorize('Success', fg='green'), '150', '75%')
    table.add_row(colorize('Warning', fg='yellow'), '30', '15%')
    table.add_row(colorize('Error', fg='red'), '20', '10%')
    print(table.render())
    
    print("\n无边框表格:")
    table = Table(headers=['ID', 'Name', 'Score'], border=False)
    table.add_row('1', 'Alice', '95')
    table.add_row('2', 'Bob', '88')
    table.add_row('3', 'Charlie', '92')
    print(table.render())


def example_screen():
    """屏幕操作示例"""
    print_header("屏幕操作")
    
    print("\n设置终端标题:")
    print(Screen.set_title('ANSI Utils Demo'))
    print("标题已设置为 'ANSI Utils Demo'")
    
    print("\n清屏命令 (不会真正执行):")
    print(f"  清屏: {repr(Screen.clear())}")
    print(f"  清行: {repr(Screen.clear_line())}")
    print(f"  滚动上: {repr(Screen.scroll_up(1))}")


def example_strip_ansi():
    """移除 ANSI 示例"""
    print_header("移除 ANSI 转义序列")
    
    text = f"{ANSI.bold('粗体')} and {ANSI.fg('red')}红色{ANSI.RESET}"
    print(f"\n原始文本: {text}")
    print(f"清除后: {strip_ansi(text)}")
    
    colored = colorize("Hello", fg='green', bg='blue', bold=True)
    print(f"\n着色文本: {colored}")
    print(f"清除后: {strip_ansi(colored)}")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("  ANSI Utils 演示")
    print("=" * 60)
    
    print("\n注意: 某些功能可能需要支持 ANSI 转义的终端")
    
    try:
        example_basic_colors()
        example_styles()
        example_style_builder()
        example_256_colors()
        example_true_color()
        example_rainbow()
        example_colorize()
        example_table()
        example_progress_bar()
        example_cursor()
        example_screen()
        example_strip_ansi()
        
        print_header("演示完成!")
        print("\n感谢使用 ANSI Utils!")
        
    except KeyboardInterrupt:
        print("\n\n演示被中断")
        sys.exit(0)


if __name__ == '__main__':
    main()