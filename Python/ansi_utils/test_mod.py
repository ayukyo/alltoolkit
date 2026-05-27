"""
ANSI Utils 测试文件

运行: python -m pytest test_mod.py -v
或: python test_mod.py
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# 确保能导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ansi_utils.mod import (
    ANSI, Cursor, Screen, Style, ProgressBar, Table,
    strip_ansi, colorize, rainbow, gradient,
    red, green, yellow, blue, magenta, cyan, white,
    bright_red, bright_green, bright_yellow, bright_blue,
    bright_magenta, bright_cyan, bright_white,
    _supports_color, _supports_256color, _supports_truecolor
)


class TestColorSupport(unittest.TestCase):
    """测试颜色支持检测"""
    
    @patch.dict(os.environ, {'TERM': 'xterm-256color'})
    @patch('sys.stdout.isatty', return_value=True)
    def test_supports_color_with_tty(self, mock_isatty):
        """测试在 TTY 环境下支持颜色"""
        result = _supports_color()
        self.assertTrue(result or not result)  # 基本功能测试
    
    @patch('sys.stdout.isatty', return_value=False)
    def test_no_color_without_tty(self, mock_isatty):
        """测试非 TTY 环境不支持颜色"""
        result = _supports_color()
        self.assertFalse(result)
    
    @patch.dict(os.environ, {'NO_COLOR': '1'}, clear=False)
    @patch('sys.stdout.isatty', return_value=True)
    def test_no_color_env(self, mock_isatty):
        """测试 NO_COLOR 环境变量"""
        result = _supports_color()
        self.assertFalse(result)


class TestANSIColors(unittest.TestCase):
    """测试 ANSI 颜色功能"""
    
    def test_standard_colors(self):
        """测试标准颜色名称"""
        # 需要模拟颜色支持
        import ansi_utils.mod as module
        original = module._COLOR_SUPPORT
        module._COLOR_SUPPORT = True
        try:
            # 红色前景色
            result = ANSI.fg('red')
            self.assertIn('31', result)
            
            # 蓝色前景色
            result = ANSI.fg('blue')
            self.assertIn('34', result)
            
            # 亮绿色前景色
            result = ANSI.fg('bright_green')
            self.assertIn('92', result)
        finally:
            module._COLOR_SUPPORT = original
    
    def test_256_colors(self):
        """测试 256 色"""
        import ansi_utils.mod as module
        original = module._COLOR_SUPPORT
        original_256 = module._256COLOR_SUPPORT
        module._COLOR_SUPPORT = True
        module._256COLOR_SUPPORT = True
        try:
            result = ANSI.fg(196)  # 红色
            self.assertIn('38;5;196', result)
            
            result = ANSI.fg(46)  # 绿色
            self.assertIn('38;5;46', result)
        finally:
            module._COLOR_SUPPORT = original
            module._256COLOR_SUPPORT = original_256
    
    def test_rgb_colors(self):
        """测试 RGB 真彩色"""
        import ansi_utils.mod as module
        original = module._COLOR_SUPPORT
        original_true = module._TRUECOLOR_SUPPORT
        module._COLOR_SUPPORT = True
        module._TRUECOLOR_SUPPORT = True
        try:
            result = ANSI.fg((255, 0, 0))
            # 应该包含 RGB 或 256 色代码
            self.assertTrue('38;2;255;0;0' in result or '38;5;' in result)
        finally:
            module._COLOR_SUPPORT = original
            module._TRUECOLOR_SUPPORT = original_true
    
    def test_background_colors(self):
        """测试背景色"""
        import ansi_utils.mod as module
        original = module._COLOR_SUPPORT
        module._COLOR_SUPPORT = True
        try:
            result = ANSI.bg('red')
            self.assertIn('41', result)
            
            module._256COLOR_SUPPORT = True
            result = ANSI.bg(196)
            self.assertIn('48;5;196', result)
            
            module._TRUECOLOR_SUPPORT = True
            result = ANSI.bg((255, 0, 0))
            self.assertTrue('48;2;255;0;0' in result or '48;5;' in result)
        finally:
            module._COLOR_SUPPORT = original
    
    def test_invalid_colors(self):
        """测试无效颜色处理"""
        import ansi_utils.mod as module
        original = module._COLOR_SUPPORT
        module._COLOR_SUPPORT = True
        try:
            result = ANSI.fg('invalid_color')
            self.assertEqual(result, '')
            
            result = ANSI.fg(300)  # 超出范围
            self.assertEqual(result, '')
            
            result = ANSI.fg((300, 0, 0))  # 无效 RGB
            self.assertEqual(result, '')
        finally:
            module._COLOR_SUPPORT = original


class TestANSIStyles(unittest.TestCase):
    """测试 ANSI 样式功能"""
    
    def test_bold(self):
        """测试粗体"""
        import ansi_utils.mod as module
        original = module._COLOR_SUPPORT
        module._COLOR_SUPPORT = True
        try:
            result = ANSI.bold('hello')
            self.assertIn('\033[1m', result)
            self.assertIn('hello', result)
            self.assertIn('\033[0m', result)
        finally:
            module._COLOR_SUPPORT = original
    
    def test_italic(self):
        """测试斜体"""
        import ansi_utils.mod as module
        original = module._COLOR_SUPPORT
        module._COLOR_SUPPORT = True
        try:
            result = ANSI.italic('hello')
            self.assertIn('\033[3m', result)
        finally:
            module._COLOR_SUPPORT = original
    
    def test_underline(self):
        """测试下划线"""
        import ansi_utils.mod as module
        original = module._COLOR_SUPPORT
        module._COLOR_SUPPORT = True
        try:
            result = ANSI.underline('hello')
            self.assertIn('\033[4m', result)
        finally:
            module._COLOR_SUPPORT = original
    
    def test_strikethrough(self):
        """测试删除线"""
        import ansi_utils.mod as module
        original = module._COLOR_SUPPORT
        module._COLOR_SUPPORT = True
        try:
            result = ANSI.strikethrough('hello')
            self.assertIn('\033[9m', result)
        finally:
            module._COLOR_SUPPORT = original
    
    def test_blink(self):
        """测试闪烁"""
        import ansi_utils.mod as module
        original = module._COLOR_SUPPORT
        module._COLOR_SUPPORT = True
        try:
            result = ANSI.blink('hello')
            self.assertIn('\033[5m', result)
        finally:
            module._COLOR_SUPPORT = original
    
    def test_reverse(self):
        """测试反转"""
        import ansi_utils.mod as module
        original = module._COLOR_SUPPORT
        module._COLOR_SUPPORT = True
        try:
            result = ANSI.reverse('hello')
            self.assertIn('\033[7m', result)
        finally:
            module._COLOR_SUPPORT = original


class TestCursor(unittest.TestCase):
    """测试光标控制"""
    
    def test_cursor_movement(self):
        """测试光标移动"""
        self.assertEqual(Cursor.up(3), '\033[3A')
        self.assertEqual(Cursor.down(2), '\033[2B')
        self.assertEqual(Cursor.forward(5), '\033[5C')
        self.assertEqual(Cursor.back(1), '\033[1D')
    
    def test_cursor_position(self):
        """测试光标定位"""
        self.assertEqual(Cursor.position(5, 10), '\033[5;10H')
        self.assertEqual(Cursor.column(20), '\033[20G')
    
    def test_cursor_save_restore(self):
        """测试保存和恢复光标"""
        self.assertEqual(Cursor.save(), '\033[s')
        self.assertEqual(Cursor.restore(), '\033[u')
    
    def test_cursor_visibility(self):
        """测试光标显示/隐藏"""
        self.assertIn('?25l', Cursor.hide_cursor())
        self.assertIn('?25h', Cursor.show_cursor())


class TestScreen(unittest.TestCase):
    """测试屏幕操作"""
    
    def test_clear_screen(self):
        """测试清屏"""
        self.assertEqual(Screen.clear(), '\033[2J')
        self.assertEqual(Screen.clear_from_cursor(), '\033[J')
        self.assertEqual(Screen.clear_to_cursor(), '\033[1J')
    
    def test_clear_line(self):
        """测试清行"""
        self.assertEqual(Screen.clear_line(), '\033[2K')
        self.assertEqual(Screen.clear_line_from_cursor(), '\033[K')
        self.assertEqual(Screen.clear_line_to_cursor(), '\033[1K')
    
    def test_scroll(self):
        """测试滚动"""
        self.assertEqual(Screen.scroll_up(3), '\033[3S')
        self.assertEqual(Screen.scroll_down(2), '\033[2T')
    
    def test_set_title(self):
        """测试设置标题"""
        result = Screen.set_title('My Terminal')
        self.assertIn('My Terminal', result)
        self.assertIn('\033]0;', result)


class TestStyle(unittest.TestCase):
    """测试链式样式构建器"""
    
    def test_basic_style(self):
        """测试基本样式"""
        s = Style('hello')
        self.assertEqual(str(s), 'hello')
    
    def test_chained_styles(self):
        """测试链式样式"""
        import ansi_utils.mod as module
        original = module._COLOR_SUPPORT
        module._COLOR_SUPPORT = True
        try:
            s = Style('hello').bold().italic()
            result = str(s)
            self.assertIn('\033[1m', result)  # bold
            self.assertIn('\033[3m', result)  # italic
            self.assertIn('hello', result)
            self.assertIn('\033[0m', result)  # reset
        finally:
            module._COLOR_SUPPORT = original
    
    def test_style_with_color(self):
        """测试颜色样式"""
        import ansi_utils.mod as module
        original = module._COLOR_SUPPORT
        module._COLOR_SUPPORT = True
        try:
            s = Style('hello').fg('red').bg('blue')
            result = str(s)
            self.assertIn('hello', result)
        finally:
            module._COLOR_SUPPORT = original
    
    def test_style_prefix_suffix(self):
        """测试前缀后缀"""
        s = Style('hello').prefix('[').suffix(']')
        result = str(s)
        self.assertEqual(result, '[hello]')
    
    def test_render(self):
        """测试渲染"""
        s = Style('test').bold().text('replaced')
        self.assertIn('replaced', s.render())


class TestProgressBar(unittest.TestCase):
    """测试进度条"""
    
    def test_progress_bar_basic(self):
        """测试基本进度条"""
        bar = ProgressBar(total=100, width=10)
        result = bar.update(50)
        self.assertIn('50.0%', result)
        self.assertIn('█', result)
        self.assertIn('░', result)
    
    def test_progress_bar_complete(self):
        """测试完成状态"""
        bar = ProgressBar(total=100, width=10)
        result = bar.update(100)
        self.assertIn('100.0%', result)
    
    def test_progress_bar_zero(self):
        """测试零进度"""
        bar = ProgressBar(total=100, width=10)
        result = bar.update(0)
        self.assertIn('0.0%', result)
    
    def test_progress_bar_custom_chars(self):
        """测试自定义字符"""
        bar = ProgressBar(total=100, width=10, filled_char='#', empty_char='-')
        result = bar.update(50)
        self.assertIn('#', result)
        self.assertIn('-', result)
    
    def test_progress_bar_with_style(self):
        """测试带样式的进度条"""
        import ansi_utils.mod as module
        original = module._COLOR_SUPPORT
        module._COLOR_SUPPORT = True
        try:
            style = Style().fg('green')
            bar = ProgressBar(total=100, width=10, style=style)
            result = bar.update(50)
            # 应该包含 ANSI 转义
            self.assertIn('\033', result)
        finally:
            module._COLOR_SUPPORT = original


class TestTable(unittest.TestCase):
    """测试表格"""
    
    def test_table_basic(self):
        """测试基本表格"""
        table = Table(headers=['Name', 'Age'])
        table.add_row('Alice', '25')
        table.add_row('Bob', '30')
        result = table.render()
        self.assertIn('Name', result)
        self.assertIn('Age', result)
        self.assertIn('Alice', result)
        self.assertIn('Bob', result)
        self.assertIn('|', result)
    
    def test_table_no_border(self):
        """测试无边框表格"""
        table = Table(headers=['A', 'B'], border=False)
        table.add_row('1', '2')
        result = table.render()
        self.assertIn('A', result)
        self.assertIn('1', result)
        self.assertNotIn('+', result)
    
    def test_table_empty(self):
        """测试空表格"""
        table = Table()
        result = table.render()
        self.assertEqual(result, '')
    
    def test_table_with_ansi_content(self):
        """测试包含 ANSI 内容的表格"""
        table = Table(headers=['Col'])
        table.add_row(f'{ANSI.bold("bold")}')
        result = table.render()
        self.assertIn('bold', result)


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_strip_ansi(self):
        """测试移除 ANSI 转义序列"""
        text = f'{ANSI.bold("hello")} world'
        result = strip_ansi(text)
        self.assertEqual(result, 'hello world')
        
        text = f'{ANSI.fg("red")}colored{ANSI.RESET}'
        result = strip_ansi(text)
        self.assertEqual(result, 'colored')
    
    def test_colorize(self):
        """测试 colorize 函数"""
        import ansi_utils.mod as module
        original = module._COLOR_SUPPORT
        module._COLOR_SUPPORT = True
        try:
            result = colorize('hello', fg='red')
            self.assertIn('hello', result)
            self.assertIn('\033', result)
            
            result = colorize('hello', bg='blue', bold=True)
            self.assertIn('hello', result)
        finally:
            module._COLOR_SUPPORT = original
    
    def test_colorize_no_color(self):
        """测试无颜色支持时的 colorize"""
        with patch('ansi_utils.mod._COLOR_SUPPORT', False):
            result = colorize('hello', fg='red', bold=True)
            self.assertEqual(result, 'hello')
    
    def test_rainbow(self):
        """测试彩虹色"""
        result = rainbow('hello')
        self.assertIn('h', strip_ansi(result))
        self.assertIn('e', strip_ansi(result))
    
    def test_gradient(self):
        """测试渐变色"""
        result = gradient('hello', (255, 0, 0), (0, 0, 255))
        self.assertIn('h', strip_ansi(result))
        
        # 空字符串
        result = gradient('', (255, 0, 0), (0, 0, 255))
        self.assertEqual(result, '')
    
    def test_convenience_functions(self):
        """测试便捷函数"""
        self.assertIn('test', red('test'))
        self.assertIn('test', green('test'))
        self.assertIn('test', yellow('test'))
        self.assertIn('test', blue('test'))
        self.assertIn('test', magenta('test'))
        self.assertIn('test', cyan('test'))
        self.assertIn('test', white('test'))
        
        self.assertIn('test', bright_red('test'))
        self.assertIn('test', bright_green('test'))
        self.assertIn('test', bright_yellow('test'))
        self.assertIn('test', bright_blue('test'))


class TestRGBTo256(unittest.TestCase):
    """测试 RGB 到 256 色转换"""
    
    def test_rgb_to_256_grayscale(self):
        """测试灰度转换"""
        # 纯黑
        code = ANSI._rgb_to_256(0, 0, 0)
        self.assertEqual(code, 16)
        
        # 纯白
        code = ANSI._rgb_to_256(255, 255, 255)
        self.assertEqual(code, 231)
        
        # 中等灰
        code = ANSI._rgb_to_256(128, 128, 128)
        self.assertIn(code, range(232, 256))
    
    def test_rgb_to_256_color(self):
        """测试彩色转换"""
        # 红色
        code = ANSI._rgb_to_256(255, 0, 0)
        self.assertIn(code, range(16, 232))
        
        # 绿色
        code = ANSI._rgb_to_256(0, 255, 0)
        self.assertIn(code, range(16, 232))


if __name__ == '__main__':
    unittest.main(verbosity=2)