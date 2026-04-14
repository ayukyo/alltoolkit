#!/usr/bin/env python3
"""
Terminal Utilities 使用示例

展示各种终端控制功能的用法
"""

import sys
import os
import time

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from terminal_utils.mod import (
    Color, Style, Ansi, Cursor, ProgressBar, Spinner, Table, Box,
    supports_color, get_terminal_size, clear_screen, clear_line,
    red, green, yellow, blue, magenta, cyan, white,
    bold, dim, underline, italic,
    hidden_cursor, saved_cursor, bell, beep, set_title,
    strip_ansi, visible_length
)


def example_colors():
    """演示颜色功能"""
    print(bold("\n=== 颜色功能演示 ===\n"))
    
    # 使用快速着色函数
    print("快速着色函数:")
    print(f"  {red('红色文本')}")
    print(f"  {green('绿色文本')}")
    print(f"  {yellow('黄色文本')}")
    print(f"  {blue('蓝色文本')}")
    print(f"  {magenta('品红文本')}")
    print(f"  {cyan('青色文本')}")
    print(f"  {white('白色文本')}")
    
    print("\n样式:")
    print(f"  {bold('粗体文本')}")
    print(f"  {dim('暗淡文本')}")
    print(f"  {underline('下划线文本')}")
    print(f"  {italic('斜体文本')}")
    
    # 使用 Ansi 类进行更复杂的着色
    print("\n高级着色:")
    print(f"  {Ansi.color('红色粗体', fg=Color.RED, styles=[Style.BOLD])}")
    print(f"  {Ansi.color('绿色斜体下划线', fg=Color.GREEN, styles=[Style.ITALIC, Style.UNDERLINE])}")
    print(f"  {Ansi.color('黄底蓝字', fg=Color.BLUE, bg=Color.BG_YELLOW)}")
    print(f"  {Ansi.color('高亮红色', fg=Color.BRIGHT_RED)}")
    
    # 测试 ANSI 移除
    print("\nANSI 处理:")
    colored = red("红色文本")
    print(f"  原始: {colored}")
    print(f"  移除后: {strip_ansi(colored)}")
    print(f"  可见长度: {visible_length(colored)} (实际字符: 4)")


def example_terminal_info():
    """演示终端信息获取"""
    print(bold("\n=== 终端信息 ===\n"))
    
    print(f"支持颜色: {supports_color()}")
    
    size = get_terminal_size()
    print(f"终端尺寸: {size.width} x {size.height}")


def example_progress_bar():
    """演示进度条"""
    print(bold("\n=== 进度条演示 ===\n"))
    
    # 基本进度条
    print("基本进度条:")
    with ProgressBar(total=50, prefix="处理中: ") as bar:
        for i in range(50):
            time.sleep(0.02)
            bar.update()
    
    # 带颜色的进度条
    print("\n带颜色的进度条:")
    with ProgressBar(total=30, prefix="下载中: ", color=Color.CYAN) as bar:
        for i in range(30):
            time.sleep(0.03)
            bar.update()
    
    # 自定义样式的进度条
    print("\n自定义样式:")
    with ProgressBar(
        total=20,
        width=30,
        fill='█',
        empty='·',
        prefix="编译: ",
        show_eta=True,
        show_counter=True
    ) as bar:
        for i in range(20):
            time.sleep(0.05)
            bar.update()
    
    print("进度条完成!")


def example_spinner():
    """演示加载动画"""
    print(bold("\n=== 加载动画演示 ===\n"))
    
    styles = ['dots', 'line', 'circle']
    
    for style in styles:
        print(f"\n{style} 样式:")
        with Spinner(message=f"处理中 ({style})...", style=style, color=Color.CYAN) as spinner:
            for _ in range(20):
                time.sleep(0.08)
                spinner.advance()
        print(f"{green('✓')} {style} 完成")


def example_table():
    """演示表格"""
    print(bold("\n=== 表格演示 ===\n"))
    
    # 基本表格
    print("基本表格 (rounded 样式):")
    table = Table(headers=['名称', '类型', '大小', '状态'])
    table.add_row('document.pdf', 'PDF', '2.5 MB', green('正常'))
    table.add_row('image.png', '图片', '1.2 MB', green('正常'))
    table.add_row('video.mp4', '视频', '150 MB', yellow('处理中'))
    table.add_row('archive.zip', '压缩包', '50 MB', red('错误'))
    table.print()
    
    # 不同样式
    print("\n\n双线边框表格:")
    Table(style='double').add_row('项目A', '完成', '100%').add_row('项目B', '进行中', '60%').print()
    
    print("\n简约边框表格:")
    Table(style='simple').add_row('数据1', '数据2').add_row('数据3', '数据4').print()
    
    print("\nMarkdown 风格表格:")
    Table(headers=['功能', '状态'], style='markdown').add_row('颜色输出', '✓').add_row('进度条', '✓').add_row('表格', '✓').print()


def example_box():
    """演示文本框"""
    print(bold("\n=== 文本框演示 ===\n"))
    
    # 基本文本框
    Box("这是一个简单的文本框").print()
    
    # 带标题的文本框
    print()
    Box(
        "这是一个带标题的文本框\n可以显示多行内容\n非常实用!",
        title="信息",
        style='double'
    ).print()
    
    # 不同边框样式
    print()
    Box("圆角边框样式", title="圆角", style='rounded', border_color=Color.CYAN).print()
    
    print()
    Box("粗边框样式", title="粗边框", style='thick', border_color=Color.GREEN).print()
    
    # 带颜色的文本框
    print()
    Box(
        "重要提示:\n这个文本框有自定义颜色!",
        title="警告",
        style='rounded',
        border_color=Color.YELLOW,
        text_color=Color.RED,
        title_color=Color.BRIGHT_YELLOW
    ).print()


def example_cursor():
    """演示光标控制"""
    print(bold("\n=== 光标控制演示 ===\n"))
    
    print("光标控制方法:")
    print("  Cursor.hide() - 隐藏光标")
    print("  Cursor.show() - 显示光标")
    print("  Cursor.move_to(row, col) - 移动到指定位置")
    print("  Cursor.move_up(n) - 向上移动 n 行")
    print("  Cursor.move_down(n) - 向下移动 n 行")
    print("  Cursor.move_left(n) - 向左移动 n 列")
    print("  Cursor.move_right(n) - 向右移动 n 列")
    print("  Cursor.save_position() - 保存光标位置")
    print("  Cursor.restore_position() - 恢复光标位置")
    
    # 演示上下文管理器
    print("\n使用上下文管理器隐藏光标:")
    with hidden_cursor():
        print("  (光标已隐藏，稍后自动恢复)")


def example_utility_functions():
    """演示工具函数"""
    print(bold("\n=== 工具函数演示 ===\n"))
    
    print("clear_screen() - 清屏")
    print("clear_line() - 清除当前行")
    print("bell() - 发出终端铃声")
    print("set_title(title) - 设置窗口标题")
    print("supports_color() - 检测颜色支持")
    print("get_terminal_size() - 获取终端尺寸")
    print("strip_ansi(text) - 移除 ANSI 序列")
    print("visible_length(text) - 获取可见文本长度")
    
    # 设置窗口标题
    set_title("Terminal Utils Demo")
    print("\n窗口标题已设置为: Terminal Utils Demo")


def example_interactive_elements():
    """演示交互元素（非交互模式）"""
    print(bold("\n=== 交互元素 ===\n"))
    
    print("TerminalMenu - 终端交互菜单")
    print("  支持键盘导航选择")
    print("  示例: menu = TerminalMenu(['选项1', '选项2', '选项3'])")
    print("        selected = menu.select()")


def main():
    """主函数"""
    # 设置标题
    set_title("Terminal Utils Demo")
    
    print(bold("=" * 50))
    print(bold("Terminal Utilities - 终端控制工具集演示"))
    print(bold("=" * 50))
    
    example_terminal_info()
    example_colors()
    example_progress_bar()
    example_spinner()
    example_table()
    example_box()
    example_cursor()
    example_utility_functions()
    example_interactive_elements()
    
    print(bold("\n" + "=" * 50))
    print(green("演示完成!"))
    print(bold("=" * 50))


if __name__ == '__main__':
    main()