#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Table Utilities Test Suite
========================================
Comprehensive tests for the table_utils module.
"""

import unittest
import sys
import os

# Add module path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Table, Column, Cell, TableConfig,
    Align, Style, BOX_CHARS, ANSI_COLORS,
    create_table, format_table, format_simple_table,
    format_grid_table, format_markdown_table, format_html_table,
    format_csv, format_columns, format_list, format_key_value,
    align_columns, column_widths, pad_columns,
    colorize, strip_colors, colored_table
)


class TestEnums(unittest.TestCase):
    """Test enum definitions."""
    
    def test_align_values(self):
        """Test Align enum values."""
        self.assertEqual(Align.LEFT.value, 'left')
        self.assertEqual(Align.CENTER.value, 'center')
        self.assertEqual(Align.RIGHT.value, 'right')
    
    def test_style_values(self):
        """Test Style enum values."""
        self.assertEqual(Style.SIMPLE.value, 'simple')
        self.assertEqual(Style.GRID.value, 'grid')
        self.assertEqual(Style.BOX.value, 'box')
        self.assertEqual(Style.MARKDOWN.value, 'markdown')
        self.assertEqual(Style.HTML.value, 'html')
        self.assertEqual(Style.CSV.value, 'csv')


class TestBoxChars(unittest.TestCase):
    """Test box drawing characters."""
    
    def test_light_chars(self):
        """Test light style characters."""
        chars = BOX_CHARS['light']
        self.assertEqual(chars['horizontal'], '─')
        self.assertEqual(chars['vertical'], '│')
    
    def test_heavy_chars(self):
        """Test heavy style characters."""
        chars = BOX_CHARS['heavy']
        self.assertEqual(chars['horizontal'], '━')
        self.assertEqual(chars['vertical'], '┃')
    
    def test_double_chars(self):
        """Test double style characters."""
        chars = BOX_CHARS['double']
        self.assertEqual(chars['horizontal'], '═')
        self.assertEqual(chars['vertical'], '║')
    
    def test_all_styles_exist(self):
        """Test all styles have required characters."""
        required_keys = ['horizontal', 'vertical', 'top_left', 'top_right',
                        'bottom_left', 'bottom_right', 'left_tee', 'right_tee',
                        'top_tee', 'bottom_tee', 'cross']
        
        for style_name, chars in BOX_CHARS.items():
            for key in required_keys:
                self.assertIn(key, chars, f"{style_name} missing {key}")


class TestColumn(unittest.TestCase):
    """Test Column dataclass."""
    
    def test_basic_column(self):
        """Test basic column creation."""
        col = Column(name='Test')
        self.assertEqual(col.name, 'Test')
        self.assertEqual(col.align, Align.LEFT)
        self.assertIsNone(col.width)
    
    def test_column_with_options(self):
        """Test column with options."""
        col = Column(name='Test', align=Align.RIGHT, width=10)
        self.assertEqual(col.align, Align.RIGHT)
        self.assertEqual(col.width, 10)
    
    def test_column_validation(self):
        """Test column validation."""
        col = Column(name='Test', min_width=-5)
        self.assertEqual(col.min_width, 1)  # Corrected to minimum
        
        col2 = Column(name='Test', min_width=5, max_width=3)
        self.assertEqual(col2.max_width, 5)  # Corrected to min_width


class TestCell(unittest.TestCase):
    """Test Cell dataclass."""
    
    def test_basic_cell(self):
        """Test basic cell creation."""
        cell = Cell(value='test')
        self.assertEqual(cell.value, 'test')
    
    def test_formatted_value(self):
        """Test cell formatting."""
        cell = Cell(value=123, format='{:.2f}')
        self.assertEqual(cell.formatted_value(), '123.00')
    
    def test_none_value(self):
        """Test None value handling."""
        cell = Cell(value=None)
        self.assertEqual(cell.formatted_value(), '')
    
    def test_format_fallback(self):
        """Test format fallback."""
        cell = Cell(value='test')
        formatted = cell.formatted_value(default_format='{}')
        self.assertEqual(formatted, 'test')


class TestTable(unittest.TestCase):
    """Test Table class."""
    
    def test_basic_table(self):
        """Test basic table creation."""
        table = Table(headers=['A', 'B', 'C'])
        self.assertEqual(table.num_columns, 3)
        self.assertEqual(table.num_rows, 0)
    
    def test_add_row(self):
        """Test adding rows."""
        table = Table(headers=['A', 'B'])
        table.add_row([1, 2])
        self.assertEqual(table.num_rows, 1)
        self.assertEqual(table.get_cell(0, 0).value, 1)
    
    def test_add_rows(self):
        """Test adding multiple rows."""
        table = Table(headers=['A', 'B'])
        table.add_rows([[1, 2], [3, 4]])
        self.assertEqual(table.num_rows, 2)
    
    def test_set_cell(self):
        """Test setting cell value."""
        table = Table(headers=['A', 'B'])
        table.add_row([1, 2])
        table.set_cell(0, 0, 'new')
        self.assertEqual(table.get_cell(0, 0).value, 'new')
    
    def test_clear_rows(self):
        """Test clearing rows."""
        table = Table(headers=['A', 'B'])
        table.add_rows([[1, 2], [3, 4]])
        table.clear_rows()
        self.assertEqual(table.num_rows, 0)
    
    def test_iteration(self):
        """Test table iteration."""
        table = Table(headers=['A', 'B'])
        table.add_rows([[1, 2], [3, 4]])
        count = 0
        for row in table:
            count += 1
        self.assertEqual(count, 2)
    
    def test_len(self):
        """Test table length."""
        table = Table(headers=['A', 'B'])
        table.add_rows([[1, 2], [3, 4]])
        self.assertEqual(len(table), 2)
    
    def test_getitem(self):
        """Test table indexing."""
        table = Table(headers=['A', 'B'])
        table.add_row([1, 2])
        row = table[0]
        self.assertEqual(len(row), 2)


class TestTableSorting(unittest.TestCase):
    """Test table sorting."""
    
    def test_sort_numeric(self):
        """Test numeric sorting."""
        table = Table(headers=['Name', 'Score'])
        table.add_rows([['Alice', 85], ['Bob', 90], ['Charlie', 80]])
        table.sort(1, reverse=True)
        
        self.assertEqual(table[0][1].value, 90)
        self.assertEqual(table[1][1].value, 85)
        self.assertEqual(table[2][1].value, 80)
    
    def test_sort_string(self):
        """Test string sorting."""
        table = Table(headers=['Name', 'Value'])
        table.add_rows([['Charlie', 1], ['Alice', 2], ['Bob', 3]])
        table.sort(0)
        
        self.assertEqual(table[0][0].value, 'Alice')
        self.assertEqual(table[1][0].value, 'Bob')
        self.assertEqual(table[2][0].value, 'Charlie')


class TestTableFilter(unittest.TestCase):
    """Test table filtering."""
    
    def test_filter_rows(self):
        """Test filtering rows."""
        table = Table(headers=['ID', 'Value'])
        table.add_rows([[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd']])
        
        filtered = table.filter(lambda row: row[0].value > 2)
        self.assertEqual(filtered.num_rows, 2)
        self.assertEqual(filtered[0][0].value, 3)


class TestTableRender(unittest.TestCase):
    """Test table rendering."""
    
    def test_render_simple(self):
        """Test simple style rendering."""
        table = Table(headers=['A', 'B'])
        table.add_row([1, 2])
        result = table.render(Style.SIMPLE)
        
        self.assertIn('A', result)
        self.assertIn('B', result)
        self.assertIn('1', result)
        self.assertIn('2', result)
    
    def test_render_grid(self):
        """Test grid style rendering."""
        table = Table(headers=['A', 'B'])
        table.add_row([1, 2])
        result = table.render(Style.GRID)
        
        self.assertIn('┌', result)
        self.assertIn('└', result)
        self.assertIn('│', result)
    
    def test_render_markdown(self):
        """Test markdown style rendering."""
        table = Table(headers=['A', 'B'])
        table.add_row([1, 2])
        result = table.render(Style.MARKDOWN)
        
        self.assertIn('|A|B|', result)
        self.assertIn('|1|2|', result)
    
    def test_render_html(self):
        """Test HTML style rendering."""
        table = Table(headers=['A', 'B'])
        table.add_row([1, 2])
        result = table.render(Style.HTML)
        
        self.assertIn('<table>', result)
        self.assertIn('<thead>', result)
        self.assertIn('<td>', result)
    
    def test_render_csv(self):
        """Test CSV style rendering."""
        table = Table(headers=['A', 'B'])
        table.add_row([1, 2])
        result = table.render(Style.CSV)
        
        self.assertIn('A,B', result)
        self.assertIn('1,2', result)
    
    def test_str_method(self):
        """Test __str__ method."""
        table = Table(headers=['A', 'B'])
        table.add_row([1, 2])
        result = str(table)
        
        self.assertIn('A', result)
        self.assertIn('1', result)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_create_table(self):
        """Test create_table function."""
        table = create_table(['A', 'B'], [[1, 2]])
        self.assertEqual(table.num_rows, 1)
    
    def test_format_table(self):
        """Test format_table function."""
        result = format_table(['A', 'B'], [[1, 2]])
        self.assertIn('A', result)
        self.assertIn('1', result)
    
    def test_format_simple_table(self):
        """Test format_simple_table function."""
        result = format_simple_table(['A', 'B'], [[1, 2]])
        self.assertIn('A', result)
        self.assertIn('B', result)
        self.assertIn('1', result)
        self.assertIn('2', result)
    
    def test_format_grid_table(self):
        """Test format_grid_table function."""
        result = format_grid_table(['A', 'B'], [[1, 2]])
        self.assertIn('│', result)
    
    def test_format_markdown_table(self):
        """Test format_markdown_table function."""
        result = format_markdown_table(['A', 'B'], [[1, 2]])
        self.assertTrue(result.startswith('|'))
    
    def test_format_html_table(self):
        """Test format_html_table function."""
        result = format_html_table(['A', 'B'], [[1, 2]])
        self.assertIn('<table>', result)
    
    def test_format_csv(self):
        """Test format_csv function."""
        result = format_csv(['A', 'B'], [[1, 2]])
        self.assertEqual(result, 'A,B\n1,2')
    
    def test_format_columns(self):
        """Test format_columns function."""
        data = [{'name': 'Alice', 'age': 25}]
        result = format_columns(data)
        self.assertIn('name', result)
        self.assertIn('Alice', result)
    
    def test_format_list(self):
        """Test format_list function."""
        result = format_list(['a', 'b', 'c'])
        self.assertIn('Value', result)
        self.assertIn('a', result)
    
    def test_format_key_value(self):
        """Test format_key_value function."""
        result = format_key_value({'a': 1, 'b': 2})
        self.assertIn('Key', result)
        self.assertIn('Value', result)
        self.assertIn('a', result)
    
    def test_align_columns(self):
        """Test align_columns function."""
        result = align_columns([['A', 'B'], ['1', '2']])
        self.assertIn('A', result)
        self.assertIn('1', result)
    
    def test_column_widths(self):
        """Test column_widths function."""
        widths = column_widths([['abc', 'd'], ['e', 'fghi']])
        self.assertEqual(widths, [3, 4])
    
    def test_pad_columns(self):
        """Test pad_columns function."""
        padded = pad_columns([['a', 'bb']], widths=[2, 3])
        self.assertEqual(padded[0][0], 'a ')
        self.assertEqual(padded[0][1], 'bb ')


class TestColorFunctions(unittest.TestCase):
    """Test color functions."""
    
    def test_colorize(self):
        """Test colorize function."""
        result = colorize('test', 'red')
        self.assertIn('test', result)
        self.assertIn('\033[31m', result)
        self.assertIn('\033[0m', result)
    
    def test_strip_colors(self):
        """Test strip_colors function."""
        colored = colorize('test', 'red')
        stripped = strip_colors(colored)
        self.assertEqual(stripped, 'test')
    
    def test_colored_table(self):
        """Test colored_table function."""
        result = colored_table(['A', 'B'], [[1, 2]], header_color='cyan')
        self.assertIn('A', result)
        self.assertIn('\033[36m', result)


class TestCSV(unittest.TestCase):
    """Test CSV handling."""
    
    def test_csv_escape_simple(self):
        """Test CSV escape for simple values."""
        table = Table(headers=['A', 'B'])
        result = table._csv_escape('simple')
        self.assertEqual(result, 'simple')
    
    def test_csv_escape_comma(self):
        """Test CSV escape for values with comma."""
        table = Table(headers=['A', 'B'])
        result = table._csv_escape('a,b')
        self.assertEqual(result, '"a,b"')
    
    def test_csv_escape_quote(self):
        """Test CSV escape for values with quote."""
        table = Table(headers=['A', 'B'])
        result = table._csv_escape('a"b')
        self.assertEqual(result, '"a""b"')
    
    def test_csv_escape_newline(self):
        """Test CSV escape for values with newline."""
        table = Table(headers=['A', 'B'])
        result = table._csv_escape('a\nb')
        self.assertEqual(result, '"a\nb"')


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_empty_table(self):
        """Test empty table."""
        table = Table(headers=['A', 'B'])
        result = table.render()
        self.assertIn('A', result)
    
    def test_empty_rows(self):
        """Test format_columns with empty data."""
        result = format_columns([])
        self.assertEqual(result, '')
    
    def test_single_column(self):
        """Test single column table."""
        table = Table(headers=['A'])
        table.add_row([1])
        result = table.render(Style.SIMPLE)
        self.assertIn('A', result)
        self.assertIn('1', result)
    
    def test_missing_cell_values(self):
        """Test row with fewer values than columns."""
        table = Table(headers=['A', 'B', 'C'])
        table.add_row([1, 2])  # Missing C
        result = table.render()
        self.assertIn('A', result)
        self.assertIn('1', result)
    
    def test_special_characters(self):
        """Test table with special characters."""
        table = Table(headers=['A', 'B'])
        table.add_row(['emoji 🎉', 'unicode 中文'])
        result = table.render()
        self.assertIn('emoji', result)
        self.assertIn('unicode', result)


class TestTableConfig(unittest.TestCase):
    """Test TableConfig."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = TableConfig()
        self.assertEqual(config.style, Style.GRID)
        self.assertEqual(config.padding, 1)
        self.assertTrue(config.show_header)
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = TableConfig(
            style=Style.SIMPLE,
            padding=2,
            show_header=False
        )
        self.assertEqual(config.style, Style.SIMPLE)
        self.assertEqual(config.padding, 2)
        self.assertFalse(config.show_header)
    
    def test_no_header(self):
        """Test table without header."""
        config = TableConfig(show_header=False)
        table = Table(headers=['A', 'B'], config=config)
        table.add_row([1, 2])
        result = table.render(Style.SIMPLE)
        self.assertNotIn('A', result.split('\n')[0])
    
    def test_footer(self):
        """Test table with footer."""
        config = TableConfig(show_footer=True)
        table = Table(headers=['A', 'B'], config=config)
        table.add_row([1, 2])
        table.set_footer(['Total', 3])
        result = table.render()
        self.assertIn('Total', result)


class TestVisibility(unittest.TestCase):
    """Test column visibility."""
    
    def test_hidden_column(self):
        """Test hidden column."""
        table = Table(columns=[
            Column(name='A'),
            Column(name='B', visible=False),
            Column(name='C'),
        ])
        table.add_row([1, 2, 3])
        result = table.render()
        
        self.assertIn('A', result)
        self.assertIn('C', result)
        # Column B should not be visible


class TestRepr(unittest.TestCase):
    """Test repr methods."""
    
    def test_table_repr(self):
        """Test table repr."""
        table = Table(headers=['A', 'B'])
        table.add_rows([[1, 2], [3, 4]])
        repr_str = repr(table)
        self.assertIn('columns=2', repr_str)
        self.assertIn('rows=2', repr_str)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)