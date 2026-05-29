#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANSI Terminal Utilities Test Module
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ansi_utils.mod import (
    ANSI, Cursor, Screen, Style, ProgressBar, Table,
    strip_ansi, colorize, rainbow, gradient,
    red, green, yellow, blue, magenta, cyan, white,
    bright_red, bright_green, bright_yellow, bright_blue,
    bright_magenta, bright_cyan, bright_white
)


class TestANSI(unittest.TestCase):
    """测试 ANSI 类"""
    
    def test_reset(self):
        """测试重置序列"""
        reset = ANSI.reset()
        self.assertEqual(reset, '\033[0m')
    
    def test_bold(self):
        """测试粗体"""
        bold_seq = ANSI.bold()
        # 在非TTY环境可能返回空，检查格式正确或返回空
        if bold_seq:
            self.assertIn('\033[1m', bold_seq)
        
        bold_text = ANSI.bold('test')
        self.assertIn('test', bold_text)
    
    def test_italic(self):
        """测试斜体"""
        italic_seq = ANSI.italic()
        if italic_seq:
            self.assertIn('\033[3m', italic_seq)
    
    def test_underline(self):
        """测试下划线"""
        underline_seq = ANSI.underline()
        if underline_seq:
            self.assertIn('\033[4m', underline_seq)
    
    def test_fg_with_color_name(self):
        """测试前景色 - 颜色名称"""
        red_fg = ANSI.fg('red')
        if red_fg:  # 仅在支持颜色的终端测试
            self.assertIn('31m', red_fg)
        
        green_fg = ANSI.fg('green')
        if green_fg:
            self.assertIn('32m', green_fg)
        
        bright_red_fg = ANSI.fg('bright_red')
        if bright_red_fg:
            self.assertIn('91m', bright_red_fg)
    
    def test_fg_with_256_color(self):
        """测试前景色 - 256色"""
        # 在支持颜色的终端中测试
        color_100 = ANSI.fg(100)
        if color_100:  # 如果支持颜色
            self.assertIn('38;5;100', color_100)
    
    def test_fg_with_rgb(self):
        """测试前景色 - RGB"""
        rgb_color = ANSI.fg((255, 128, 64))
        # 如果支持真彩色
        if rgb_color:
            self.assertIn('38;2', rgb_color)
    
    def test_bg_with_color_name(self):
        """测试背景色 - 颜色名称"""
        red_bg = ANSI.bg('red')
        if red_bg:  # 仅在支持颜色的终端测试
            self.assertIn('41m', red_bg)
        
        green_bg = ANSI.bg('green')
        if green_bg:
            self.assertIn('42m', green_bg)
    
    def test_rgb_to_256(self):
        """测试 RGB 到 256 转换"""
        # 灰度转换 - 灰度色系在 232-255 范围内
        gray_128 = ANSI._rgb_to_256(128, 128, 128)
        self.assertTrue(232 <= gray_128 <= 255)
        
        # 彩色转换 - 彩色在 16-231 范围内
        color = ANSI._rgb_to_256(255, 0, 0)
        self.assertTrue(16 <= color <= 231)


class TestCursor(unittest.TestCase):
    """测试光标控制"""
    
    def test_up(self):
        """测试向上移动"""
        up = Cursor.up(5)
        self.assertEqual(up, '\033[5A')
    
    def test_down(self):
        """测试向下移动"""
        down = Cursor.down(3)
        self.assertEqual(down, '\033[3B')
    
    def test_forward(self):
        """测试向前移动"""
        forward = Cursor.forward(10)
        self.assertEqual(forward, '\033[10C')
    
    def test_back(self):
        """测试向后移动"""
        back = Cursor.back(2)
        self.assertEqual(back, '\033[2D')
    
    def test_position(self):
        """测试定位"""
        pos = Cursor.position(10, 20)
        self.assertEqual(pos, '\033[10;20H')
    
    def test_save_restore(self):
        """测试保存和恢复"""
        save = Cursor.save()
        restore = Cursor.restore()
        # Cursor.save 使用 CSI 格式 '\033[s'
        self.assertIn('[s', save)
        self.assertIn('[u', restore)
    
    def test_hide_show(self):
        """测试隐藏和显示"""
        hide = Cursor.hide_cursor()
        show = Cursor.show_cursor()
        self.assertIn('?25l', hide)
        self.assertIn('?25h', show)


class TestScreen(unittest.TestCase):
    """测试屏幕操作"""
    
    def test_clear(self):
        """测试清屏"""
        clear = Screen.clear()
        self.assertEqual(clear, '\033[2J')
    
    def test_clear_line(self):
        """测试清除行"""
        clear_line = Screen.clear_line()
        self.assertEqual(clear_line, '\033[2K')
    
    def test_scroll(self):
        """测试滚动"""
        scroll_up = Screen.scroll_up(5)
        scroll_down = Screen.scroll_down(3)
        self.assertEqual(scroll_up, '\033[5S')
        self.assertEqual(scroll_down, '\033[3T')
    
    def test_set_title(self):
        """测试设置标题"""
        title = Screen.set_title('My Terminal')
        self.assertIn('My Terminal', title)
        self.assertIn('\033]0;', title)


class TestStyle(unittest.TestCase):
    """测试链式样式"""
    
    def test_chain_styles(self):
        """测试链式样式组合"""
        style = Style('Hello').bold().underline()
        result = style.render()
        self.assertIn('Hello', result)
    
    def test_color_chain(self):
        """测试颜色链式调用"""
        style = Style('Colored').fg('red').bg('blue')
        result = style.render()
        self.assertIn('Colored', result)
    
    def test_prefix_suffix(self):
        """测试前缀和后缀"""
        style = Style('Text').prefix('[]').suffix('!')
        result = style.render()
        self.assertIn('[', result)
        self.assertIn('!', result)
    
    def test_text_method(self):
        """测试 text 方法"""
        style = Style().text('New Text')
        self.assertEqual(style.render(), 'New Text')
    
    def test_on_alias(self):
        """测试 on 方法（bg 别名）"""
        style = Style('Test').on('red')
        result = style.render()
        self.assertIn('Test', result)
    
    def test_color_alias(self):
        """测试 color 方法（fg 别名）"""
        style = Style('Test').color('green')
        result = style.render()
        self.assertIn('Test', result)


class TestProgressBar(unittest.TestCase):
    """测试进度条"""
    
    def test_progress_bar_creation(self):
        """测试进度条创建"""
        bar = ProgressBar(100)
        result = bar.update(50)
        self.assertIn('50.0%', result)
    
    def test_progress_bar_complete(self):
        """测试进度完成"""
        bar = ProgressBar(100)
        result = bar.update(100)
        self.assertIn('100.0%', result)
    
    def test_progress_bar_zero(self):
        """测试零进度"""
        bar = ProgressBar(100)
        result = bar.update(0)
        self.assertIn('0.0%', result)
    
    def test_progress_bar_custom_chars(self):
        """测试自定义字符"""
        bar = ProgressBar(100, filled_char='=', empty_char='-')
        result = bar.update(50)
        self.assertIn('=', result)
        self.assertIn('-', result)
    
    def test_progress_bar_with_style(self):
        """测试带样式的进度条"""
        style = Style().fg('green')
        bar = ProgressBar(100, style=style)
        result = bar.update(50)
        self.assertIn('50.0%', result)


class TestTable(unittest.TestCase):
    """测试表格"""
    
    def test_table_with_headers(self):
        """测试带表头的表格"""
        table = Table(headers=['Name', 'Value'])
        table.add_row('Item1', '100')
        table.add_row('Item2', '200')
        result = table.render()
        self.assertIn('Name', result)
        self.assertIn('Value', result)
        self.assertIn('Item1', result)
        self.assertIn('Item2', result)
    
    def test_table_without_border(self):
        """测试无边框表格"""
        table = Table(headers=['A', 'B'], border=False)
        table.add_row('1', '2')
        result = table.render()
        self.assertNotIn('+', result)
    
    def test_table_strip_ansi(self):
        """测试 ANSI 序列移除"""
        table = Table()
        clean = table._strip_ansi('\033[31mRed\033[0m')
        self.assertEqual(clean, 'Red')
    
    def test_table_empty(self):
        """测试空表格"""
        table = Table()
        result = table.render()
        self.assertEqual(result, '')
    
    def test_table_with_styles(self):
        """测试带样式的表格"""
        header_style = Style().bold()
        table = Table(headers=['Col1', 'Col2'], header_style=header_style)
        table.add_row('Data1', 'Data2')
        result = table.render()
        self.assertIn('Col1', result)
        self.assertIn('Data1', result)


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_strip_ansi(self):
        """测试 ANSI 序列移除"""
        text = '\033[31mRed Text\033[0m'
        clean = strip_ansi(text)
        self.assertEqual(clean, 'Red Text')
    
    def test_strip_ansi_complex(self):
        """测试复杂的 ANSI 序列移除"""
        text = '\033[1;31;42mStyled\033[0m Normal'
        clean = strip_ansi(text)
        self.assertEqual(clean, 'Styled Normal')
    
    def test_colorize(self):
        """测试快速着色"""
        colored = colorize('Hello', fg='red', bg='blue', bold=True)
        self.assertIn('Hello', colored)
    
    def test_rainbow(self):
        """测试彩虹色"""
        rainbow_text = rainbow('Test')
        self.assertIn('T', rainbow_text)
        self.assertIn('e', rainbow_text)
        self.assertIn('s', rainbow_text)
        self.assertIn('t', rainbow_text)
    
    def test_gradient(self):
        """测试渐变色"""
        gradient_text = gradient('Gradient', (255, 0, 0), (0, 255, 0))
        self.assertIn('G', gradient_text)
        # 在支持颜色的终端，包含 ANSI 序列
        # 否则只是原始文本
        self.assertIn('Gradient', gradient_text)
    
    def test_color_shortcuts(self):
        """测试颜色快捷函数"""
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
        self.assertIn('test', bright_magenta('test'))
        self.assertIn('test', bright_cyan('test'))
        self.assertIn('test', bright_white('test'))


class TestStyleStrRepr(unittest.TestCase):
    """测试 Style 的字符串表示"""
    
    def test_str_method(self):
        """测试 __str__"""
        style = Style('Text').bold()
        self.assertIn('Text', str(style))
    
    def test_repr_method(self):
        """测试 __repr__"""
        style = Style('Text').italic()
        self.assertIn('Text', repr(style))


if __name__ == '__main__':
    unittest.main(verbosity=2)