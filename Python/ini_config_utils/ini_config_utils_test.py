#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - INI Config Utilities Test Suite
INI配置文件工具模块测试

运行方式:
    python ini_config_utils_test.py
    python -m pytest ini_config_utils_test.py -v
"""

import sys
import os
import tempfile
import unittest

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    IniConfig, IniSection, IniConfigError,
    SectionNotFoundError, KeyNotFoundError, ParseError,
    read_ini, write_ini, parse_ini, create_ini
)


class TestIniSection(unittest.TestCase):
    """测试IniSection类"""
    
    def setUp(self):
        self.section = IniSection('test')
        self.section.set('host', 'localhost')
        self.section.set('port', 3306)
        self.section.set('debug', True)
        self.section.set('timeout', 30.5)
    
    def test_basic_operations(self):
        """测试基本操作"""
        self.assertEqual(self.section.get('host'), 'localhost')
        self.assertEqual(self.section.get_int('port'), 3306)
        self.assertTrue(self.section.get_bool('debug'))
        self.assertEqual(self.section.get_float('timeout'), 30.5)
    
    def test_defaults(self):
        """测试默认值"""
        self.assertEqual(self.section.get('missing', 'default'), 'default')
        self.assertEqual(self.section.get_int('missing', 100), 100)
        self.assertEqual(self.section.get_float('missing', 1.5), 1.5)
        self.assertFalse(self.section.get_bool('missing', False))
        self.assertTrue(self.section.get_bool('missing', True))
    
    def test_bool_conversion(self):
        """测试布尔值转换"""
        bool_values = [
            ('true', True), ('True', True), ('TRUE', True),
            ('yes', True), ('Yes', True),
            ('1', True), ('on', True), ('enabled', True),
            ('false', False), ('False', False),
            ('no', False), ('0', False),
            ('off', False), ('disabled', False),
        ]
        for val, expected in bool_values:
            self.section.set('test_bool', val)
            self.assertEqual(self.section.get_bool('test_bool'), expected)
    
    def test_list_operations(self):
        """测试列表操作"""
        self.section.set('items', ['a', 'b', 'c'])
        result = self.section.get_list('items')
        self.assertEqual(result, ['a', 'b', 'c'])
        
        # 自定义分隔符
        self.section.set('paths', '/usr/bin:/usr/local/bin')
        result = self.section.get_list('paths', separator=':')
        self.assertEqual(result, ['/usr/bin', '/usr/local/bin'])
    
    def test_has_and_remove(self):
        """测试存在检查和删除"""
        self.assertTrue(self.section.has('host'))
        self.assertFalse(self.section.has('missing'))
        
        self.assertTrue(self.section.remove('host'))
        self.assertFalse(self.section.has('host'))
        self.assertFalse(self.section.remove('host'))
    
    def test_clear(self):
        """测试清空"""
        self.section.clear()
        self.assertEqual(len(self.section), 0)
        self.assertEqual(self.section.keys(), [])
    
    def test_copy(self):
        """测试拷贝"""
        copy = self.section.copy()
        self.assertEqual(copy.name, self.section.name)
        self.assertEqual(copy.keys(), self.section.keys())
        
        copy.set('new_key', 'new_value')
        self.assertFalse(self.section.has('new_key'))
    
    def test_dict_access(self):
        """测试字典式访问"""
        self.assertEqual(self.section['host'], 'localhost')
        
        self.section['new_key'] = 'new_value'
        self.assertEqual(self.section['new_key'], 'new_value')
        
        self.assertIn('host', self.section)
        self.assertNotIn('missing', self.section)
        
        with self.assertRaises(KeyNotFoundError):
            _ = self.section['missing']
    
    def test_len(self):
        """测试长度"""
        self.assertEqual(len(self.section), 4)
        self.section.set('new', 'value')
        self.assertEqual(len(self.section), 5)


class TestIniConfig(unittest.TestCase):
    """测试IniConfig类"""
    
    def setUp(self):
        self.config = IniConfig()
        self.config.set('database', 'host', 'localhost')
        self.config.set('database', 'port', 3306)
        self.config.set('app', 'name', 'MyApp')
        self.config.set('app', 'debug', True)
    
    def test_section_operations(self):
        """测试节操作"""
        self.assertTrue(self.config.has_section('database'))
        self.assertFalse(self.config.has_section('missing'))
        
        db_section = self.config.section('database')
        self.assertEqual(db_section.get('host'), 'localhost')
        
        new_section = self.config.section('new_section', create=True)
        self.assertTrue(self.config.has_section('new_section'))
        
        self.assertTrue(self.config.remove_section('new_section'))
        self.assertFalse(self.config.has_section('new_section'))
    
    def test_section_not_found(self):
        """测试节不存在异常"""
        with self.assertRaises(SectionNotFoundError):
            self.config.section('missing')
    
    def test_duplicate_section(self):
        """测试重复节"""
        with self.assertRaises(IniConfigError):
            self.config.add_section('database')
    
    def test_get_methods(self):
        """测试获取方法"""
        self.assertEqual(self.config.get('database', 'host'), 'localhost')
        self.assertEqual(self.config.get_int('database', 'port'), 3306)
        self.assertTrue(self.config.get_bool('app', 'debug'))
        
        self.assertEqual(self.config.get('missing', 'key', 'default'), 'default')
        self.assertEqual(self.config.get_int('database', 'missing', 999), 999)
    
    def test_has_and_remove(self):
        """测试存在检查和删除"""
        self.assertTrue(self.config.has('database'))
        self.assertTrue(self.config.has('database', 'host'))
        self.assertFalse(self.config.has('database', 'missing'))
        self.assertFalse(self.config.has('missing'))
        
        self.assertTrue(self.config.remove('database', 'host'))
        self.assertFalse(self.config.has('database', 'host'))
        
        self.assertTrue(self.config.remove('database'))
        self.assertFalse(self.config.has_section('database'))
    
    def test_sections_list(self):
        """测试节列表"""
        sections = self.config.sections()
        self.assertIn('database', sections)
        self.assertIn('app', sections)
        self.assertEqual(len(sections), 2)
    
    def test_to_dict(self):
        """测试转换为字典"""
        data = self.config.to_dict()
        self.assertIn('database', data)
        self.assertIn('app', data)
        self.assertEqual(data['database']['host'], 'localhost')
    
    def test_from_dict(self):
        """测试从字典加载"""
        data = {
            'section1': {'key1': 'value1', 'key2': 'value2'},
            'section2': {'key3': 'value3'}
        }
        config = IniConfig()
        config.from_dict(data)
        
        self.assertEqual(config.get('section1', 'key1'), 'value1')
        self.assertEqual(config.get('section2', 'key3'), 'value3')
    
    def test_copy(self):
        """测试配置拷贝"""
        copy = self.config.copy()
        self.assertEqual(copy.sections(), self.config.sections())
        
        copy.set('new_section', 'key', 'value')
        self.assertFalse(self.config.has_section('new_section'))
    
    def test_clear(self):
        """测试清空"""
        self.config.clear()
        self.assertEqual(self.config.sections(), [])
    
    def test_merge(self):
        """测试合并配置"""
        other = IniConfig()
        other.set('database', 'new_key', 'new_value')
        other.set('new_section', 'key', 'value')
        
        self.config.merge(other)
        
        self.assertEqual(self.config.get('database', 'new_key'), 'new_value')
        self.assertTrue(self.config.has_section('new_section'))
    
    def test_merge_no_overwrite(self):
        """测试合并不覆盖"""
        other = IniConfig()
        other.set('database', 'host', 'new_host')
        other.set('database', 'new_key', 'new_value')
        
        self.config.merge(other, overwrite=False)
        
        self.assertEqual(self.config.get('database', 'host'), 'localhost')
        self.assertEqual(self.config.get('database', 'new_key'), 'new_value')
    
    def test_validate(self):
        """测试验证"""
        schema = {
            'database': ['host', 'port'],
            'app': ['name']
        }
        errors = self.config.validate(schema)
        self.assertEqual(errors, [])
        
        schema = {
            'database': ['host', 'port', 'missing_key'],
            'missing_section': ['key']
        }
        errors = self.config.validate(schema)
        self.assertEqual(len(errors), 2)
    
    def test_dict_access(self):
        """测试字典式访问"""
        section = self.config['database']
        self.assertEqual(section.get('host'), 'localhost')
        
        self.config['new_section'] = {'key': 'value'}
        self.assertTrue(self.config.has_section('new_section'))
        
        self.assertIn('database', self.config)
        self.assertNotIn('missing', self.config)


class TestParsing(unittest.TestCase):
    """测试解析功能"""
    
    def test_parse_string(self):
        """测试解析字符串"""
        content = """# Global comment
[database]
host = localhost
port = 3306

[app]
name = MyApp
debug = true
"""
        config = IniConfig()
        config.read_string(content)
        
        self.assertEqual(config.get('database', 'host'), 'localhost')
        self.assertEqual(config.get_int('database', 'port'), 3306)
        self.assertEqual(config.get('app', 'name'), 'MyApp')
        self.assertTrue(config.get_bool('app', 'debug'))
    
    def test_parse_with_comments(self):
        """测试带注释的解析"""
        content = """# Global comment
# Another global comment

[database]
# Database settings
host = localhost
port = 3306

[app]
name = MyApp
"""
        config = IniConfig()
        config.read_string(content)
        
        self.assertEqual(len(config._global_comments), 2)
        # 节后的注释被解析为第一个键的注释
        db_section = config.section('database')
        self.assertEqual(db_section._comments.get('host'), 'Database settings')
    
    def test_parse_quoted_values(self):
        """测试带引号的值"""
        content = """[section]
key1 = "value with spaces"
key2 = 'single quoted'
key3 = normal_value
"""
        config = IniConfig()
        config.read_string(content)
        
        self.assertEqual(config.get('section', 'key1'), 'value with spaces')
        self.assertEqual(config.get('section', 'key2'), 'single quoted')
        self.assertEqual(config.get('section', 'key3'), 'normal_value')
    
    def test_parse_special_values(self):
        """测试特殊值"""
        content = """[section]
key_with_equals = value=with=equals
key_with_hash = value # not a comment
key_with_semicolon = value;not a comment
"""
        config = IniConfig()
        config.read_string(content)
        
        self.assertEqual(config.get('section', 'key_with_equals'), 'value=with=equals')
        self.assertEqual(config.get('section', 'key_with_hash'), 'value # not a comment')
        self.assertEqual(config.get('section', 'key_with_semicolon'), 'value;not a comment')
    
    def test_parse_error_outside_section(self):
        """测试节外键错误"""
        content = "key = value\n[section]\nother = value"
        config = IniConfig()
        
        with self.assertRaises(ParseError):
            config.read_string(content)
    
    def test_parse_error_invalid_line(self):
        """测试无效行错误"""
        content = "[section]\ninvalid line without equals"
        config = IniConfig()
        
        with self.assertRaises(ParseError):
            config.read_string(content)


class TestWriting(unittest.TestCase):
    """测试写入功能"""
    
    def test_write_string(self):
        """测试生成字符串"""
        config = IniConfig()
        config.set('database', 'host', 'localhost')
        config.set('database', 'port', 3306)
        config.set('app', 'name', 'MyApp')
        
        content = config.write_string()
        
        self.assertIn('[database]', content)
        self.assertIn('host = localhost', content)
        self.assertIn('[app]', content)
        self.assertIn('name = MyApp', content)
    
    def test_write_with_comments(self):
        """测试带注释的写入"""
        config = IniConfig()
        config._global_comments = ['Global comment']
        config.add_section('database', 'Database settings')
        config.set('database', 'host', 'localhost', 'Server host')
        
        content = config.write_string()
        
        self.assertIn('# Global comment', content)
        self.assertIn('# Database settings', content)
        self.assertIn('# Server host', content)
    
    def test_write_quoted_values(self):
        """测试带引号的值写入"""
        config = IniConfig()
        config.set('section', 'key', 'value with spaces')
        
        content = config.write_string()
        
        self.assertIn('key = "value with spaces"', content)
    
    def test_write_file(self):
        """测试写入文件"""
        config = IniConfig()
        config.set('section', 'key', 'value')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            temp_path = f.name
        
        try:
            config.write_file(temp_path)
            
            with open(temp_path, 'r') as f:
                content = f.read()
            
            self.assertIn('[section]', content)
            self.assertIn('key = value', content)
        finally:
            os.unlink(temp_path)
    
    def test_read_file(self):
        """测试读取文件"""
        content = "[section]\nkey = value\n"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            config = IniConfig()
            config.read_file(temp_path)
            
            self.assertEqual(config.get('section', 'key'), 'value')
        finally:
            os.unlink(temp_path)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_read_ini(self):
        """测试read_ini函数"""
        content = "[section]\nkey = value\n"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            config = read_ini(temp_path)
            self.assertEqual(config.get('section', 'key'), 'value')
        finally:
            os.unlink(temp_path)
    
    def test_write_ini(self):
        """测试write_ini函数"""
        config = IniConfig()
        config.set('section', 'key', 'value')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            temp_path = f.name
        
        try:
            write_ini(config, temp_path)
            
            with open(temp_path, 'r') as f:
                content = f.read()
            
            self.assertIn('[section]', content)
        finally:
            os.unlink(temp_path)
    
    def test_parse_ini(self):
        """测试parse_ini函数"""
        content = "[section]\nkey = value\n"
        config = parse_ini(content)
        
        self.assertEqual(config.get('section', 'key'), 'value')
    
    def test_create_ini(self):
        """测试create_ini函数"""
        data = {'section': {'key': 'value'}}
        config = create_ini(data)
        
        self.assertEqual(config.get('section', 'key'), 'value')


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_config(self):
        """测试空配置"""
        config = IniConfig()
        self.assertEqual(config.sections(), [])
        self.assertEqual(config.write_string(), '')
    
    def test_empty_section(self):
        """测试空节"""
        config = IniConfig()
        config.add_section('empty_section')
        
        content = config.write_string()
        self.assertIn('[empty_section]', content)
    
    def test_empty_values(self):
        """测试空值"""
        config = IniConfig()
        config.set('section', 'empty', '')
        config.set('section', 'spaces', '   ')
        
        self.assertEqual(config.get('section', 'empty'), '')
        self.assertEqual(config.get('section', 'spaces'), '   ')
    
    def test_unicode_values(self):
        """测试Unicode值"""
        config = IniConfig()
        config.set('section', 'chinese', '中文测试')
        config.set('section', 'emoji', '🎉🎊')
        config.set('section', 'japanese', 'こんにちは')
        
        content = config.write_string()
        config2 = IniConfig()
        config2.read_string(content)
        
        self.assertEqual(config2.get('section', 'chinese'), '中文测试')
        self.assertEqual(config2.get('section', 'emoji'), '🎉🎊')
        self.assertEqual(config2.get('section', 'japanese'), 'こんにちは')
    
    def test_special_characters_in_keys(self):
        """测试特殊字符键名"""
        config = IniConfig()
        config.set('section', 'key_with_underscore', 'value1')
        config.set('section', 'key-with-dash', 'value2')
        config.set('section', 'Key.With.Dots', 'value3')
        
        self.assertEqual(config.get('section', 'key_with_underscore'), 'value1')
        self.assertEqual(config.get('section', 'key-with-dash'), 'value2')
        self.assertEqual(config.get('section', 'Key.With.Dots'), 'value3')
    
    def test_case_sensitivity(self):
        """测试大小写敏感"""
        config = IniConfig()
        config.set('Section', 'Key', 'value')
        
        self.assertTrue(config.has('Section'))
        self.assertFalse(config.has('section'))
        self.assertTrue(config.has('Section', 'Key'))
        self.assertFalse(config.has('Section', 'key'))


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestIniSection))
    suite.addTests(loader.loadTestsFromTestCase(TestIniConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestParsing))
    suite.addTests(loader.loadTestsFromTestCase(TestWriting))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
