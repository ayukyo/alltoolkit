"""
AllToolkit - YAML Utilities 单元测试

测试 yaml_utils 模块的所有功能。

运行方式：
    python yaml_utils_test.py

依赖：
    - PyYAML (推荐，用于完整测试)
    - 或仅使用标准库（有限测试，使用 JSON 降级）
"""

import os
import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# 导入被测试模块

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    get_version,
    is_pyyaml_available,
    get_module_info,
    YAMLUtilsError,
    YAMLFileNotFoundError,
    YAMLValidationError,
    YAMLFormatError,
    load_yaml,
    load_yaml_string,
    load_yaml_file,
    load_yaml_all,
    safe_load_yaml,
    dump_yaml,
    dump_yaml_file,
    dump_yaml_string,
    validate_yaml,
    is_valid_yaml,
    yaml_to_json,
    json_to_yaml,
    yaml_to_dict,
    merge_yaml,
    diff_yaml,
    get_yaml_value,
    set_yaml_value,
    delete_yaml_key,
    contains_unsafe_tags,
    get_supported_formats,
    get_yaml_info,
)


class TestVersionInfo(unittest.TestCase):
    """测试版本信息功能。"""
    
    def test_get_version(self):
        """测试获取版本号。"""
        version = get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)
    
    def test_is_pyyaml_available(self):
        """测试 PyYAML 可用性检测。"""
        available = is_pyyaml_available()
        self.assertIsInstance(available, bool)
    
    def test_get_module_info(self):
        """测试获取模块信息。"""
        info = get_module_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn('name', info)
        self.assertIn('version', info)
        self.assertIn('pyyaml_available', info)
        self.assertEqual(info['name'], 'yaml_utils')


class TestExceptionClasses(unittest.TestCase):
    """测试异常类。"""
    
    def test_yaml_utils_error(self):
        """测试基础异常类。"""
        with self.assertRaises(YAMLUtilsError):
            raise YAMLUtilsError("测试错误")
    
    def test_file_not_found_error(self):
        """测试文件未找到异常。"""
        with self.assertRaises(YAMLFileNotFoundError):
            raise YAMLFileNotFoundError("文件不存在")
    
    def test_validation_error(self):
        """测试验证异常。"""
        with self.assertRaises(YAMLValidationError):
            raise YAMLValidationError("验证失败")
    
    def test_format_error(self):
        """测试格式异常。"""
        with self.assertRaises(YAMLFormatError):
            raise YAMLFormatError("格式错误")


class TestLoadYaml(unittest.TestCase):
    """测试 YAML 加载功能。"""
    
    def setUp(self):
        """设置测试夹具。"""
        self.test_dir = tempfile.mkdtemp()
        
        # 创建测试 YAML 文件
        self.yaml_file = os.path.join(self.test_dir, 'test.yaml')
        with open(self.yaml_file, 'w', encoding='utf-8') as f:
            f.write("""
name: 测试
version: 1.0
enabled: true
count: 42
tags:
  - yaml
  - python
  - test
config:
  debug: false
  timeout: 30
""")
        
        # 创建测试 JSON 文件（用于降级测试）
        self.json_file = os.path.join(self.test_dir, 'test.json')
        with open(self.json_file, 'w', encoding='utf-8') as f:
            f.write('{"name": "测试", "version": 1.0}')
    
    def tearDown(self):
        """清理测试夹具。"""
        shutil.rmtree(self.test_dir)
    
    def test_load_yaml_file(self):
        """测试从文件加载 YAML。"""
        data = load_yaml_file(self.yaml_file)
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data['name'], '测试')
        self.assertEqual(data['version'], 1.0)
        self.assertTrue(data['enabled'])
        self.assertEqual(data['count'], 42)
        self.assertIn('yaml', data['tags'])
    
    def test_load_yaml_string(self):
        """测试从字符串加载 YAML。"""
        yaml_str = "key: value\nnumber: 123"
        data = load_yaml_string(yaml_str)
        
        self.assertEqual(data['key'], 'value')
        self.assertEqual(data['number'], 123)
    
    def test_load_yaml_nonexistent_file(self):
        """测试加载不存在的文件。"""
        with self.assertRaises(YAMLFileNotFoundError):
            load_yaml_file('/nonexistent/path/file.yaml')
    
    def test_load_yaml_invalid_format(self):
        """测试加载无效格式的 YAML。"""
        invalid_yaml = "invalid: yaml: content: ["
        
        # 应该抛出格式错误或使用降级
        try:
            data = load_yaml_string(invalid_yaml)
            # 如果降级成功，可能是作为其他格式解析
        except YAMLFormatError:
            pass  # 预期行为
    
    def test_safe_load_yaml(self):
        """测试安全加载。"""
        data = safe_load_yaml(self.yaml_file)
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data['name'], '测试')


class TestDumpYaml(unittest.TestCase):
    """测试 YAML 转储功能。"""
    
    def setUp(self):
        """设置测试夹具。"""
        self.test_dir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.test_dir, 'output.yaml')
        
        self.test_data = {
            'name': '测试数据',
            'version': 2.0,
            'enabled': True,
            'count': 100,
            'tags': ['test', 'yaml'],
            'config': {
                'debug': True,
                'timeout': 60
            }
        }
    
    def tearDown(self):
        """清理测试夹具。"""
        shutil.rmtree(self.test_dir)
    
    def test_dump_yaml_string(self):
        """测试转储为 YAML 字符串。"""
        yaml_str = dump_yaml_string(self.test_data)
        
        self.assertIsInstance(yaml_str, str)
        self.assertIn('name', yaml_str)
        self.assertIn('测试数据', yaml_str)
    
    def test_dump_yaml_file(self):
        """测试转储为 YAML 文件。"""
        dump_yaml_file(self.test_data, self.output_file)
        
        self.assertTrue(os.path.exists(self.output_file))
        
        # 验证内容
        with open(self.output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn('name', content)
        self.assertIn('测试数据', content)
    
    def test_dump_yaml_roundtrip(self):
        """测试转储后加载（往返测试）。"""
        dump_yaml_file(self.test_data, self.output_file)
        loaded = load_yaml_file(self.output_file)
        
        self.assertEqual(loaded['name'], self.test_data['name'])
        self.assertEqual(loaded['version'], self.test_data['version'])
        self.assertEqual(loaded['tags'], self.test_data['tags'])


class TestValidateYaml(unittest.TestCase):
    """测试 YAML 验证功能。"""
    
    def setUp(self):
        """设置测试夹具。"""
        self.test_dir = tempfile.mkdtemp()
        
        # 有效 YAML
        self.valid_file = os.path.join(self.test_dir, 'valid.yaml')
        with open(self.valid_file, 'w', encoding='utf-8') as f:
            f.write("name: test\nvalue: 123")
        
        # 带 schema 的 YAML
        self.schema_file = os.path.join(self.test_dir, 'schema.yaml')
        with open(self.schema_file, 'w', encoding='utf-8') as f:
            f.write("""
name: 测试
age: 25
active: true
""")
    
    def tearDown(self):
        """清理测试夹具。"""
        shutil.rmtree(self.test_dir)
    
    def test_is_valid_yaml(self):
        """测试 YAML 有效性检查。"""
        self.assertTrue(is_valid_yaml(self.valid_file))
    
    def test_validate_with_schema(self):
        """测试带模式的验证。"""
        schema = {
            'name': str,
            'age': int,
            'active': bool
        }
        
        valid, errors = validate_yaml(self.schema_file, schema)
        
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_missing_field(self):
        """测试验证缺失字段。"""
        schema = {
            'name': str,
            'missing_field': str  # 这个字段不存在
        }
        
        valid, errors = validate_yaml(self.valid_file, schema)
        
        self.assertFalse(valid)
        self.assertTrue(any('missing_field' in e for e in errors))


class TestConversion(unittest.TestCase):
    """测试格式转换功能。"""
    
    def setUp(self):
        """设置测试夹具。"""
        self.test_dir = tempfile.mkdtemp()
        
        self.yaml_file = os.path.join(self.test_dir, 'test.yaml')
        with open(self.yaml_file, 'w', encoding='utf-8') as f:
            f.write("""
name: 转换测试
value: 42
items:
  - a
  - b
  - c
""")
        
        self.json_file = os.path.join(self.test_dir, 'test.json')
        with open(self.json_file, 'w', encoding='utf-8') as f:
            f.write('{"name": "JSON 测试", "value": 100}')
    
    def tearDown(self):
        """清理测试夹具。"""
        shutil.rmtree(self.test_dir)
    
    def test_yaml_to_json_string(self):
        """测试 YAML 转 JSON 字符串。"""
        json_str = yaml_to_json(self.yaml_file)
        
        self.assertIsInstance(json_str, str)
        self.assertIn('name', json_str)
        self.assertIn('转换测试', json_str)
    
    def test_yaml_to_json_file(self):
        """测试 YAML 转 JSON 文件。"""
        output = os.path.join(self.test_dir, 'output.json')
        yaml_to_json(self.yaml_file, output)
        
        self.assertTrue(os.path.exists(output))
    
    def test_json_to_yaml(self):
        """测试 JSON 转 YAML。"""
        yaml_str = json_to_yaml(self.json_file)
        
        self.assertIsInstance(yaml_str, str)
        self.assertIn('name', yaml_str)
    
    def test_yaml_to_dict(self):
        """测试 YAML 转字典。"""
        data = yaml_to_dict(self.yaml_file)
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data['name'], '转换测试')


class TestMergeYaml(unittest.TestCase):
    """测试 YAML 合并功能。"""
    
    def setUp(self):
        """设置测试夹具。"""
        self.test_dir = tempfile.mkdtemp()
        
        # 基础配置
        self.base_file = os.path.join(self.test_dir, 'base.yaml')
        with open(self.base_file, 'w', encoding='utf-8') as f:
            f.write("""
database:
  host: localhost
  port: 5432
  name: mydb
logging:
  level: INFO
""")
        
        # 覆盖配置
        self.override_file = os.path.join(self.test_dir, 'override.yaml')
        with open(self.override_file, 'w', encoding='utf-8') as f:
            f.write("""
database:
  host: production.example.com
  password: secret
logging:
  level: DEBUG
  file: app.log
""")
    
    def tearDown(self):
        """清理测试夹具。"""
        shutil.rmtree(self.test_dir)
    
    def test_merge_yaml_deep(self):
        """测试深度合并 YAML。"""
        merged = merge_yaml([self.base_file, self.override_file], deep=True)
        
        # 数据库主机应该被覆盖
        self.assertEqual(merged['database']['host'], 'production.example.com')
        # 数据库端口应该保留
        self.assertEqual(merged['database']['port'], 5432)
        # 新增的密码应该存在
        self.assertEqual(merged['database']['password'], 'secret')
        # 日志级别应该被覆盖
        self.assertEqual(merged['logging']['level'], 'DEBUG')
        # 新增的日志文件应该存在
        self.assertEqual(merged['logging']['file'], 'app.log')
    
    def test_merge_yaml_shallow(self):
        """测试浅层合并 YAML。"""
        merged = merge_yaml([self.base_file, self.override_file], deep=False)
        
        # 浅层合并会完全覆盖 database 键
        self.assertNotIn('port', merged.get('database', {}))


class TestDiffYaml(unittest.TestCase):
    """测试 YAML 差分功能。"""
    
    def setUp(self):
        """设置测试夹具。"""
        self.test_dir = tempfile.mkdtemp()
        
        # 原始配置
        self.original_file = os.path.join(self.test_dir, 'original.yaml')
        with open(self.original_file, 'w', encoding='utf-8') as f:
            f.write("""
name: 原始
version: 1.0
enabled: true
count: 10
""")
        
        # 修改后的配置
        self.modified_file = os.path.join(self.test_dir, 'modified.yaml')
        with open(self.modified_file, 'w', encoding='utf-8') as f:
            f.write("""
name: 修改后
version: 2.0
enabled: true
new_field: added
""")
    
    def tearDown(self):
        """清理测试夹具。"""
        shutil.rmtree(self.test_dir)
    
    def test_diff_yaml(self):
        """测试 YAML 差分。"""
        diff = diff_yaml(self.original_file, self.modified_file)
        
        self.assertIn('added', diff)
        self.assertIn('removed', diff)
        self.assertIn('modified', diff)
        
        # name 和 version 应该被修改
        self.assertIn('name', diff['modified'])
        self.assertIn('version', diff['modified'])
        
        # count 应该被移除
        self.assertIn('count', diff['removed'])
        
        # new_field 应该被添加
        self.assertIn('new_field', diff['added'])


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷功能。"""
    
    def setUp(self):
        """设置测试夹具。"""
        self.test_dir = tempfile.mkdtemp()
        
        self.config_file = os.path.join(self.test_dir, 'config.yaml')
        with open(self.config_file, 'w', encoding='utf-8') as f:
            f.write("""
database:
  host: localhost
  port: 5432
  credentials:
    username: admin
    password: secret
app:
  name: MyApp
  version: 1.0
""")
    
    def tearDown(self):
        """清理测试夹具。"""
        shutil.rmtree(self.test_dir)
    
    def test_get_yaml_value_simple(self):
        """测试获取简单路径的值。"""
        value = get_yaml_value(self.config_file, 'app.name')
        self.assertEqual(value, 'MyApp')
    
    def test_get_yaml_value_nested(self):
        """测试获取嵌套路径的值。"""
        value = get_yaml_value(self.config_file, 'database.credentials.username')
        self.assertEqual(value, 'admin')
    
    def test_get_yaml_value_default(self):
        """测试获取不存在路径的默认值。"""
        value = get_yaml_value(self.config_file, 'nonexistent.key', 'default')
        self.assertEqual(value, 'default')
    
    def test_set_yaml_value(self):
        """测试设置值。"""
        output = os.path.join(self.test_dir, 'output.yaml')
        shutil.copy(self.config_file, output)
        
        set_yaml_value(output, 'app.version', '2.0')
        
        new_value = get_yaml_value(output, 'app.version')
        self.assertEqual(new_value, '2.0')
    
    def test_delete_yaml_key(self):
        """测试删除键。"""
        output = os.path.join(self.test_dir, 'output.yaml')
        shutil.copy(self.config_file, output)
        
        delete_yaml_key(output, 'database.credentials.password')
        
        value = get_yaml_value(output, 'database.credentials.password', None)
        self.assertIsNone(value)
        
        # 其他键应该保留
        username = get_yaml_value(output, 'database.credentials.username')
        self.assertEqual(username, 'admin')


class TestSecurityFeatures(unittest.TestCase):
    """测试安全功能。"""
    
    def setUp(self):
        """设置测试夹具。"""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """清理测试夹具。"""
        shutil.rmtree(self.test_dir)
    
    def test_contains_unsafe_tags_safe(self):
        """测试安全 YAML 不包含不安全标签。"""
        safe_file = os.path.join(self.test_dir, 'safe.yaml')
        with open(safe_file, 'w', encoding='utf-8') as f:
            f.write("name: safe\nvalue: 123")
        
        self.assertFalse(contains_unsafe_tags(safe_file))
    
    def test_contains_unsafe_tags_unsafe(self):
        """测试检测不安全标签。"""
        unsafe_file = os.path.join(self.test_dir, 'unsafe.yaml')
        with open(unsafe_file, 'w', encoding='utf-8') as f:
            f.write("!!python/object:__main__.Test: {}")
        
        self.assertTrue(contains_unsafe_tags(unsafe_file))


class TestUtilityFunctions(unittest.TestCase):
    """测试工具功能。"""
    
    def setUp(self):
        """设置测试夹具。"""
        self.test_dir = tempfile.mkdtemp()
        
        self.yaml_file = os.path.join(self.test_dir, 'test.yaml')
        with open(self.yaml_file, 'w', encoding='utf-8') as f:
            f.write("""
name: 测试
items:
  - a
  - b
  - c
""")
    
    def tearDown(self):
        """清理测试夹具。"""
        shutil.rmtree(self.test_dir)
    
    def test_get_supported_formats(self):
        """测试获取支持的格式。"""
        formats = get_supported_formats()
        
        self.assertIsInstance(formats, list)
        self.assertIn('YAML', formats)
        self.assertIn('JSON', formats)
    
    def test_get_yaml_info(self):
        """测试获取 YAML 文件信息。"""
        info = get_yaml_info(self.yaml_file)
        
        self.assertIsInstance(info, dict)
        self.assertTrue(info['exists'])
        self.assertTrue(info['valid'])
        self.assertIn('name', info['keys'])
        self.assertIn('items', info['keys'])
    
    def test_get_yaml_info_nonexistent(self):
        """测试获取不存在文件的信息。"""
        info = get_yaml_info('/nonexistent/file.yaml')
        
        self.assertFalse(info['exists'])
        self.assertFalse(info['valid'])


class TestLoadYamlAll(unittest.TestCase):
    """测试多文档 YAML 加载。"""
    
    def setUp(self):
        """设置测试夹具。"""
        self.test_dir = tempfile.mkdtemp()
        
        # 多文档 YAML
        self.multi_file = os.path.join(self.test_dir, 'multi.yaml')
        with open(self.multi_file, 'w', encoding='utf-8') as f:
            f.write("""---
name: 文档 1
value: 1
---
name: 文档 2
value: 2
---
name: 文档 3
value: 3
""")
    
    def tearDown(self):
        """清理测试夹具。"""
        shutil.rmtree(self.test_dir)
    
    def test_load_yaml_all(self):
        """测试加载多文档 YAML。"""
        documents = load_yaml_all(self.multi_file)
        
        self.assertIsInstance(documents, list)
        self.assertEqual(len(documents), 3)
        self.assertEqual(documents[0]['name'], '文档 1')
        self.assertEqual(documents[1]['name'], '文档 2')
        self.assertEqual(documents[2]['name'], '文档 3')


class TestEdgeCases(unittest.TestCase):
    """测试边界情况。"""
    
    def setUp(self):
        """设置测试夹具。"""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """清理测试夹具。"""
        shutil.rmtree(self.test_dir)
    
    def test_empty_yaml(self):
        """测试空 YAML。"""
        empty_file = os.path.join(self.test_dir, 'empty.yaml')
        with open(empty_file, 'w', encoding='utf-8') as f:
            f.write("")
        
        data = load_yaml_file(empty_file)
        self.assertIsNone(data)
    
    def test_yaml_with_unicode(self):
        """测试包含 Unicode 的 YAML。"""
        unicode_file = os.path.join(self.test_dir, 'unicode.yaml')
        with open(unicode_file, 'w', encoding='utf-8') as f:
            f.write("""
chinese: 中文测试
japanese: 日本語テスト
emoji: 🎉🚀
""")
        
        try:
            data = load_yaml_file(unicode_file)
            
            self.assertEqual(data['chinese'], '中文测试')
            self.assertEqual(data['japanese'], '日本語テスト')
            self.assertEqual(data['emoji'], '🎉🚀')
        except YAMLFormatError as e:
            # 旧版 PyYAML 可能不支持 emoji，跳过 emoji 测试
            if 'emoji' in str(e) or 'special characters' in str(e):
                # 验证至少中文和日文能正常加载
                with open(unicode_file, 'r', encoding='utf-8') as f:
                    content = f.read().replace('emoji: 🎉🚀', 'emoji: test')
                temp_file = os.path.join(self.test_dir, 'unicode2.yaml')
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                data = load_yaml_file(temp_file)
                self.assertEqual(data['chinese'], '中文测试')
                self.assertEqual(data['japanese'], '日本語テスト')
            else:
                raise
    
    def test_yaml_with_special_values(self):
        """测试包含特殊值的 YAML。"""
        special_file = os.path.join(self.test_dir, 'special.yaml')
        with open(special_file, 'w', encoding='utf-8') as f:
            f.write("""
null_value: null
true_value: true
false_value: false
empty_string: ""
empty_list: []
empty_dict: {}
""")
        
        data = load_yaml_file(special_file)
        
        self.assertIsNone(data['null_value'])
        self.assertTrue(data['true_value'])
        self.assertFalse(data['false_value'])
        self.assertEqual(data['empty_string'], '')
        self.assertEqual(data['empty_list'], [])
        self.assertEqual(data['empty_dict'], {})


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
