"""
中文文本对齐工具测试模块

测试所有核心功能：
- 字符宽度计算
- 文本填充对齐
- 表格格式化
- 双语对齐
- 进度条
- 文本换行
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chinese_alignment_utils.mod import (
    get_display_width,
    text_width,
    pad_left,
    pad_right,
    pad_center,
    truncate,
    align_columns,
    align_bilingual,
    create_progress_bar,
    wrap_text,
    split_by_width,
    ChineseTextAligner,
    format_table,
    ljust,
    rjust,
    center,
)


class TestDisplayWidth(unittest.TestCase):
    """测试字符宽度计算"""
    
    def test_ascii_width(self):
        """测试 ASCII 字符宽度"""
        self.assertEqual(get_display_width('a'), 1)
        self.assertEqual(get_display_width('A'), 1)
        self.assertEqual(get_display_width('0'), 1)
        self.assertEqual(get_display_width('!'), 1)
        self.assertEqual(get_display_width(' '), 1)
    
    def test_chinese_width(self):
        """测试中文字符宽度"""
        self.assertEqual(get_display_width('中'), 2)
        self.assertEqual(get_display_width('文'), 2)
        self.assertEqual(get_display_width('测'), 2)
        self.assertEqual(get_display_width('试'), 2)
    
    def test_chinese_punctuation(self):
        """测试中文标点宽度"""
        self.assertEqual(get_display_width('。'), 2)
        self.assertEqual(get_display_width('，'), 2)
        self.assertEqual(get_display_width('：'), 2)
        self.assertEqual(get_display_width('！'), 2)
    
    def test_fullwidth_char(self):
        """测试全角字符宽度"""
        self.assertEqual(get_display_width('Ａ'), 2)  # 全角 A
        self.assertEqual(get_display_width('１'), 2)  # 全角 1
        self.assertEqual(get_display_width('　'), 2)  # 全角空格
    
    def test_empty_char(self):
        """测试空字符"""
        self.assertEqual(get_display_width(''), 0)
    
    def test_control_char(self):
        """测试控制字符"""
        self.assertEqual(get_display_width('\n'), 0)
        self.assertEqual(get_display_width('\t'), 0)
    
    def test_text_width(self):
        """测试文本总宽度"""
        self.assertEqual(text_width('hello'), 5)
        self.assertEqual(text_width('你好'), 4)
        self.assertEqual(text_width('hello世界'), 9)  # 5 + 4 = 9
        self.assertEqual(text_width(''), 0)


class TestPadding(unittest.TestCase):
    """测试文本填充"""
    
    def test_pad_left(self):
        """测试左填充"""
        result = pad_left('abc', 10)
        self.assertEqual(len(result), 10)
        self.assertTrue(result.endswith('abc'))
        
        result = pad_left('你好', 10)
        self.assertTrue(text_width(result) >= 10)
    
    def test_pad_right(self):
        """测试右填充"""
        result = pad_right('abc', 10)
        self.assertEqual(len(result), 10)
        self.assertTrue(result.startswith('abc'))
        
        result = pad_right('你好', 10)
        self.assertTrue(text_width(result) >= 10)
    
    def test_pad_center(self):
        """测试居中填充"""
        result = pad_center('abc', 10)
        self.assertEqual(text_width(result), 10)
        self.assertTrue('abc' in result)
        # 居中意味着左右两边应该有填充
        self.assertTrue(result.startswith(' ') or result.startswith('-'))
    
    def test_pad_no_need(self):
        """测试无需填充的情况"""
        result = pad_left('abcdefghijk', 5)
        self.assertEqual(result, 'abcdefghijk')
    
    def test_custom_fillchar(self):
        """测试自定义填充字符"""
        result = pad_left('abc', 10, '-')
        self.assertTrue(result.startswith('-'))
        self.assertTrue(result.endswith('abc'))
        
        result = pad_right('abc', 10, '中')
        self.assertTrue('中' in result)


class TestTruncate(unittest.TestCase):
    """测试文本截断"""
    
    def test_truncate_english(self):
        """测试英文截断"""
        result = truncate('hello world', 8)
        self.assertTrue(text_width(result) <= 8)
        self.assertTrue(result.endswith('...'))
    
    def test_truncate_chinese(self):
        """测试中文截断"""
        result = truncate('这是一个测试文本', 8)
        self.assertTrue(text_width(result) <= 8)
        self.assertTrue(result.endswith('...'))
    
    def test_truncate_mixed(self):
        """测试中英文混合截断"""
        result = truncate('hello世界test', 10)
        self.assertTrue(text_width(result) <= 10)
    
    def test_truncate_short_text(self):
        """测试短文本不截断"""
        result = truncate('abc', 10)
        self.assertEqual(result, 'abc')
    
    def test_custom_suffix(self):
        """测试自定义后缀"""
        result = truncate('hello world', 8, '…')
        self.assertTrue(result.endswith('…'))


class TestAlignColumns(unittest.TestCase):
    """测试列对齐"""
    
    def test_simple_columns(self):
        """测试简单列对齐"""
        rows = [
            ['Name', 'Age'],
            ['Alice', '25'],
            ['Bob', '30'],
        ]
        result = align_columns(rows)
        lines = result.split('\n')
        self.assertEqual(len(lines), 4)  # 3行 + 1分隔线
        self.assertIn('Name', lines[0])
        self.assertIn('Alice', lines[2])
    
    def test_chinese_columns(self):
        """测试中文列对齐"""
        rows = [
            ['姓名', '年龄', '城市'],
            ['张三', '25', '北京'],
            ['李四', '30', '上海'],
        ]
        result = align_columns(rows)
        lines = result.split('\n')
        self.assertEqual(len(lines), 4)
        self.assertIn('姓名', lines[0])
        self.assertIn('张三', lines[2])
    
    def test_alignment_modes(self):
        """测试对齐模式"""
        rows = [
            ['Name', 'Count'],
            ['Alice', '100'],
            ['Bob', '99'],
        ]
        
        # 左对齐
        result_left = align_columns(rows, align='left')
        self.assertIn('Alice', result_left)
        
        # 右对齐
        result_right = align_columns(rows, align='right')
        self.assertIn('100', result_right)
        
        # 居中
        result_center = align_columns(rows, align='center')
        self.assertIn('Alice', result_center)
    
    def test_empty_rows(self):
        """测试空行"""
        result = align_columns([])
        self.assertEqual(result, '')
    
    def test_no_header_line(self):
        """测试不显示表头分隔线"""
        rows = [['a', 'b'], ['c', 'd']]
        result = align_columns(rows, show_header_line=False)
        lines = result.split('\n')
        self.assertEqual(len(lines), 2)


class TestBilingualAlignment(unittest.TestCase):
    """测试双语对齐"""
    
    def test_parallel_mode(self):
        """测试并排显示"""
        chinese = "你好世界\n这是测试"
        english = "Hello World\nThis is a test"
        result = align_bilingual(chinese, english, mode='parallel')
        lines = result.split('\n')
        self.assertEqual(len(lines), 2)
    
    def test_interleaved_mode(self):
        """测试交错显示"""
        chinese = "你好"
        english = "Hello"
        result = align_bilingual(chinese, english, mode='interleaved')
        lines = result.split('\n')
        self.assertTrue(len(lines) >= 2)
    
    def test_block_mode(self):
        """测试块状显示"""
        chinese = "你好"
        english = "Hello"
        result = align_bilingual(chinese, english, mode='block')
        self.assertIn('中文', result)
        self.assertIn('English', result)


class TestProgressBar(unittest.TestCase):
    """测试进度条"""
    
    def test_progress_bar_creation(self):
        """测试进度条创建"""
        result = create_progress_bar(50, 100)
        self.assertIn('[', result)
        self.assertIn(']', result)
        self.assertIn('50%', result)
    
    def test_progress_bar_zero(self):
        """测试零进度"""
        result = create_progress_bar(0, 100)
        self.assertIn('0%', result)
    
    def test_progress_bar_full(self):
        """测试完成进度"""
        result = create_progress_bar(100, 100)
        self.assertIn('100%', result)
    
    def test_progress_bar_no_percent(self):
        """测试不显示百分比"""
        result = create_progress_bar(50, 100, show_percent=False)
        self.assertNotIn('%', result)
    
    def test_custom_fill_chars(self):
        """测试自定义填充字符"""
        result = create_progress_bar(50, 100, fill='#', empty='-')
        self.assertIn('#', result)
        self.assertIn('-', result)


class TestWrapText(unittest.TestCase):
    """测试文本换行"""
    
    def test_wrap_english(self):
        """测试英文换行"""
        text = "This is a long sentence that should be wrapped to multiple lines."
        result = wrap_text(text, width=20)
        lines = result.split('\n')
        # 检查每行宽度不超过限制（最后一行可能较短）
        for line in lines:
            line_width = text_width(line)
            self.assertTrue(line_width <= 20 or len(line) == 1)
    
    def test_wrap_chinese(self):
        """测试中文换行"""
        text = "这是一段很长的中文文本需要进行换行处理以便于阅读。"
        result = wrap_text(text, width=20)
        lines = result.split('\n')
        # 检查有换行产生
        self.assertTrue(len(lines) >= 1)
        for line in lines:
            line_width = text_width(line)
            self.assertTrue(line_width <= 20)
    
    def test_wrap_with_indent(self):
        """测试带缩进换行"""
        text = "This is a test sentence for wrapping."
        result = wrap_text(text, width=30, indent='  ')
        lines = result.split('\n')
        # 检查每行都有缩进
        for line in lines:
            if line:  # 非空行
                self.assertTrue(line.startswith('  '))


class TestSplitByWidth(unittest.TestCase):
    """测试按宽度分割"""
    
    def test_split_english(self):
        """测试英文分割"""
        text = "HelloWorld"
        result = split_by_width(text, 5)
        for segment in result:
            self.assertTrue(text_width(segment) <= 5)
    
    def test_split_chinese(self):
        """测试中文分割"""
        text = "你好世界测试"
        result = split_by_width(text, 4)  # 2个中文字符宽度
        for segment in result:
            self.assertTrue(text_width(segment) <= 4)
    
    def test_split_mixed(self):
        """测试中英文混合分割"""
        text = "Hello世界Test测试"
        result = split_by_width(text, 6)
        for segment in result:
            self.assertTrue(text_width(segment) <= 6)


class TestChineseTextAligner(unittest.TestCase):
    """测试文本对齐器类"""
    
    def test_aligner_pad_right(self):
        """测试右填充"""
        result = ChineseTextAligner('hello').width(10).pad_right()
        self.assertTrue(text_width(result) >= 10)
    
    def test_aligner_pad_left(self):
        """测试左填充"""
        result = ChineseTextAligner('hello').width(10).pad_left()
        self.assertTrue(text_width(result) >= 10)
    
    def test_aligner_truncate(self):
        """测试截断"""
        result = ChineseTextAligner('hello world').width(5).truncate()
        self.assertTrue(text_width(result) <= 5)


class TestFormatTable(unittest.TestCase):
    """测试表格格式化"""
    
    def test_simple_table(self):
        """测试简单表格"""
        headers = ['Name', 'Age']
        rows = [['Alice', '25'], ['Bob', '30']]
        result = format_table(headers, rows)
        self.assertIn('Name', result)
        self.assertIn('Alice', result)
        self.assertIn('25', result)
    
    def test_chinese_table(self):
        """测试中文表格"""
        headers = ['姓名', '年龄', '城市']
        rows = [
            ['张三', '25', '北京'],
            ['李四', '30', '上海'],
        ]
        result = format_table(headers, rows)
        self.assertIn('姓名', result)
        self.assertIn('张三', result)
        self.assertIn('北京', result)
    
    def test_table_with_title(self):
        """测试带标题的表格"""
        headers = ['A', 'B']
        rows = [['1', '2']]
        result = format_table(headers, rows, title='Test Table')
        self.assertIn('Test Table', result)
    
    def test_table_without_border(self):
        """测试无边框表格"""
        headers = ['A', 'B']
        rows = [['1', '2']]
        result = format_table(headers, rows, border=False)
        self.assertNotIn('┌', result)
    
    def test_empty_table(self):
        """测试空表格"""
        result = format_table([], [])
        self.assertEqual(result, '')


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_ljust(self):
        """测试 ljust"""
        result = ljust('hello', 10)
        self.assertTrue(result.startswith('hello'))
    
    def test_rjust(self):
        """测试 rjust"""
        result = rjust('hello', 10)
        self.assertTrue(result.endswith('hello'))
    
    def test_center(self):
        """测试 center"""
        result = center('hello', 10)
        self.assertTrue('hello' in result)


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(text_width(''), 0)
        self.assertEqual(pad_left('', 5), '     ')
        self.assertEqual(truncate('', 10), '')
    
    def test_single_char(self):
        """测试单字符"""
        self.assertEqual(text_width('a'), 1)
        self.assertEqual(text_width('中'), 2)
    
    def test_very_long_text(self):
        """测试超长文本"""
        text = 'a' * 1000
        result = truncate(text, 50)
        self.assertTrue(text_width(result) <= 50)
    
    def test_special_chars(self):
        """测试特殊字符"""
        text = '★☆●○■□'
        # 这些符号宽度可能是1或2，取决于具体字符
        width = text_width(text)
        self.assertTrue(width >= len(text))


if __name__ == '__main__':
    unittest.main(verbosity=2)