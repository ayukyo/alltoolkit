#!/usr/bin/env python3
"""
Terminal Utilities 测试套件
"""

import sys
import os
import time
import unittest
from io import StringIO

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Color, Style, Ansi, Cursor, ProgressBar, Spinner, Table, Box,
    TerminalSize, TerminalMenu, supports_color, get_terminal_size,
    clear_line, strip_ansi, visible_length, hidden_cursor, saved_cursor,
    red, green, yellow, blue, magenta, cyan, white, bold, dim, underline, italic,
    bell, beep, set_title
)


class TestColorEnum(unittest.TestCase):
    """测试颜色枚举"""
    
    def test_foreground_colors(self):
        """测试前景色"""
        self.assertEqual(Color.RED.value, 31)
        self.assertEqual(Color.GREEN.value, 32)
        self.assertEqual(Color.BLUE.value, 34)
        self.assertEqual(Color.WHITE.value, 37)
    
    def test_background_colors(self):
        """测试背景色"""
        self.assertEqual(Color.BG_RED.value, 41)
        self.assertEqual(Color.BG_GREEN.value, 42)
        self.assertEqual(Color.BG_BLUE.value, 44)
    
    def test_bright_colors(self):
        """测试高亮颜色"""
        self.assertEqual(Color.BRIGHT_RED.value, 91)
        self.assertEqual(Color.BRIGHT_GREEN.value, 92)


class TestStyleEnum(unittest.TestCase):
    """测试样式枚举"""
    
    def test_styles(self):
        """测试样式值"""
        self.assertEqual(Style.RESET.value, 0)
        self.assertEqual(Style.BOLD.value, 1)
        self.assertEqual(Style.UNDERLINE.value, 4)
        self.assertEqual(Style.ITALIC.value, 3)


class TestAnsi(unittest.TestCase):
    """测试 ANSI 转义序列处理"""
    
    def test_color_basic(self):
        """测试基本着色"""
        text = "Hello"
        colored = Ansi.color(text, fg=Color.RED)
        # 无论是否支持颜色，原始文本都应该保留
        self.assertIn(text, colored)
        # 如果支持颜色，检查 ANSI 序列
        if supports_color():
            self.assertIn('\033[', colored)
            self.assertIn('\033[0m', colored)
    
    def test_color_with_background(self):
        """测试前景和背景色"""
        text = "Test"
        colored = Ansi.color(text, fg=Color.RED, bg=Color.BG_BLUE)
        self.assertIn(text, colored)
        if supports_color():
            self.assertIn('31', colored)  # RED foreground code
            self.assertIn('44', colored)  # BLUE background code
    
    def test_color_with_styles(self):
        """测试样式"""
        text = "Styled"
        colored = Ansi.color(text, styles=[Style.BOLD, Style.UNDERLINE])
        self.assertIn(text, colored)
        if supports_color():
            self.assertIn('1', colored)  # BOLD code
            self.assertIn('4', colored)  # UNDERLINE code
    
    def test_strip_ansi(self):
        """测试 ANSI 序列移除"""
        colored = '\033[31mRed Text\033[0m'
        stripped = Ansi.strip(colored)
        self.assertEqual(stripped, 'Red Text')
        
        # 复杂的 ANSI 序列
        complex_colored = '\033[1;31;44mBold Red on Blue\033[0m'
        stripped = Ansi.strip(complex_colored)
        self.assertEqual(stripped, 'Bold Red on Blue')
    
    def test_visible_length(self):
        """测试可见长度计算"""
        colored = '\033[31mRed\033[0m'
        length = Ansi.length(colored)
        self.assertEqual(length, 3)
        
        # 多个 ANSI 序列
        complex_text = '\033[1m\033[31mHello\033[0m \033[32mWorld\033[0m'
        length = Ansi.length(complex_text)
        self.assertEqual(length, 11)  # "Hello World"


class TestQuickColorFunctions(unittest.TestCase):
    """测试快速着色函数"""
    
    def test_red(self):
        result = red("test")
        self.assertIn("test", result)
        if supports_color():
            self.assertIn('\033[31m', result)
    
    def test_green(self):
        result = green("test")
        self.assertIn("test", result)
        if supports_color():
            self.assertIn('\033[32m', result)
    
    def test_blue(self):
        result = blue("test")
        self.assertIn("test", result)
        if supports_color():
            self.assertIn('\033[34m', result)
    
    def test_bold(self):
        result = bold("test")
        self.assertIn("test", result)
        if supports_color():
            self.assertIn('\033[1m', result)
    
    def test_underline(self):
        result = underline("test")
        self.assertIn("test", result)
        if supports_color():
            self.assertIn('\033[4m', result)


class TestTerminalSize(unittest.TestCase):
    """测试终端尺寸"""
    
    def test_terminal_size_dataclass(self):
        """测试终端尺寸数据类"""
        size = TerminalSize(width=100, height=30)
        self.assertEqual(size.width, 100)
        self.assertEqual(size.height, 30)
    
    def test_get_terminal_size(self):
        """测试获取终端尺寸"""
        size = get_terminal_size()
        self.assertIsInstance(size, TerminalSize)
        self.assertGreater(size.width, 0)
        self.assertGreater(size.height, 0)


class TestProgressBar(unittest.TestCase):
    """测试进度条"""
    
    def test_progress_bar_creation(self):
        """测试进度条创建"""
        bar = ProgressBar(total=100)
        self.assertEqual(bar.total, 100)
        self.assertEqual(bar.current, 0)
    
    def test_progress_bar_update(self):
        """测试进度条更新"""
        bar = ProgressBar(total=100)
        bar.update(10)
        self.assertEqual(bar.current, 10)
        
        bar.update(20)
        self.assertEqual(bar.current, 30)
    
    def test_progress_bar_set_progress(self):
        """测试直接设置进度"""
        bar = ProgressBar(total=100)
        bar.set_progress(50)
        self.assertEqual(bar.current, 50)
        
        # 测试上限
        bar.set_progress(150)
        self.assertEqual(bar.current, 100)
        
        # 新建一个进度条测试下限
        bar2 = ProgressBar(total=100)
        bar2.set_progress(-10)
        self.assertEqual(bar2.current, 0)
    
    def test_progress_bar_context_manager(self):
        """测试上下文管理器"""
        with ProgressBar(total=10) as bar:
            self.assertEqual(bar.current, 0)
            bar.update(10)


class TestSpinner(unittest.TestCase):
    """测试加载动画"""
    
    def test_spinner_creation(self):
        """测试动画创建"""
        spinner = Spinner(message="Loading...", style="dots")
        self.assertEqual(spinner.message, "Loading...")
        self.assertIn('dots', Spinner.STYLES)
    
    def test_spinner_styles(self):
        """测试各种动画样式"""
        for style in ['dots', 'line', 'arrow', 'circle']:
            spinner = Spinner(style=style)
            self.assertGreater(len(spinner.frames), 0)
    
    def test_spinner_update(self):
        """测试消息更新"""
        spinner = Spinner(message="Initial")
        spinner.update("Updated")
        self.assertEqual(spinner.message, "Updated")


class TestTable(unittest.TestCase):
    """测试表格"""
    
    def test_table_creation(self):
        """测试表格创建"""
        table = Table(headers=['A', 'B', 'C'])
        self.assertEqual(table.headers, ['A', 'B', 'C'])
    
    def test_table_add_row(self):
        """测试添加行"""
        table = Table()
        table.add_row('x', 'y', 'z')
        self.assertEqual(len(table.rows), 1)
        self.assertEqual(table.rows[0], ['x', 'y', 'z'])
    
    def test_table_render(self):
        """测试表格渲染"""
        table = Table(headers=['Name', 'Value'])
        table.add_row('Test', '123')
        rendered = table.render()
        self.assertIn('Name', rendered)
        self.assertIn('Value', rendered)
        self.assertIn('Test', rendered)
        self.assertIn('123', rendered)
    
    def test_table_styles(self):
        """测试表格样式"""
        styles = ['simple', 'double', 'rounded', 'minimal', 'markdown']
        for style in styles:
            table = Table(headers=['A', 'B'], style=style)
            table.add_row('1', '2')
            rendered = table.render()
            self.assertIn('A', rendered)
            self.assertIn('B', rendered)
    
    def test_table_empty(self):
        """测试空表格"""
        table = Table()
        rendered = table.render()
        self.assertEqual(rendered, '')


class TestBox(unittest.TestCase):
    """测试文本框"""
    
    def test_box_creation(self):
        """测试文本框创建"""
        box = Box("Hello World")
        self.assertEqual(box.text, "Hello World")
    
    def test_box_render(self):
        """测试文本框渲染"""
        box = Box("Test Content")
        rendered = box.render()
        self.assertIn('Test Content', rendered)
    
    def test_box_with_title(self):
        """测试带标题的文本框"""
        box = Box("Content", title="Title")
        rendered = box.render()
        self.assertIn('Content', rendered)
        self.assertIn('Title', rendered)
    
    def test_box_styles(self):
        """测试文本框样式"""
        styles = ['single', 'double', 'rounded', 'thick']
        for style in styles:
            box = Box("Test", style=style)
            rendered = box.render()
            self.assertIn('Test', rendered)
    
    def test_box_multiline(self):
        """测试多行文本"""
        box = Box("Line 1\nLine 2\nLine 3")
        rendered = box.render()
        self.assertIn('Line 1', rendered)
        self.assertIn('Line 2', rendered)
        self.assertIn('Line 3', rendered)
    
    def test_box_alignment(self):
        """测试对齐"""
        box = Box("Test", align='center')
        rendered = box.render()
        self.assertIn('Test', rendered)


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_supports_color(self):
        """测试颜色支持检测"""
        result = supports_color()
        self.assertIsInstance(result, bool)
    
    def test_strip_ansi_function(self):
        """测试 ANSI 移除函数"""
        result = strip_ansi('\033[31mRed\033[0m')
        self.assertEqual(result, 'Red')
    
    def test_visible_length_function(self):
        """测试可见长度函数"""
        result = visible_length('\033[31mHello\033[0m')
        self.assertEqual(result, 5)


class TestCursor(unittest.TestCase):
    """测试光标控制"""
    
    def test_cursor_has_methods(self):
        """测试光标方法存在"""
        self.assertTrue(hasattr(Cursor, 'hide'))
        self.assertTrue(hasattr(Cursor, 'show'))
        self.assertTrue(hasattr(Cursor, 'move_to'))
        self.assertTrue(hasattr(Cursor, 'move_up'))
        self.assertTrue(hasattr(Cursor, 'move_down'))
        self.assertTrue(hasattr(Cursor, 'move_left'))
        self.assertTrue(hasattr(Cursor, 'move_right'))
        self.assertTrue(hasattr(Cursor, 'save_position'))
        self.assertTrue(hasattr(Cursor, 'restore_position'))


class TestContextManagers(unittest.TestCase):
    """测试上下文管理器"""
    
    def test_hidden_cursor_context(self):
        """测试隐藏光标上下文"""
        with hidden_cursor():
            pass  # 只是测试不会抛出异常
    
    def test_saved_cursor_context(self):
        """测试保存光标上下文"""
        with saved_cursor():
            pass  # 只是测试不会抛出异常


class TestBellAndBeep(unittest.TestCase):
    """测试铃声功能"""
    
    def test_bell(self):
        """测试铃声"""
        # 只测试不会抛出异常
        bell()
    
    def test_set_title(self):
        """测试设置标题"""
        set_title("Test Title")


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestColorEnum,
        TestStyleEnum,
        TestAnsi,
        TestQuickColorFunctions,
        TestTerminalSize,
        TestProgressBar,
        TestSpinner,
        TestTable,
        TestBox,
        TestUtilityFunctions,
        TestCursor,
        TestContextManagers,
        TestBellAndBeep,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)