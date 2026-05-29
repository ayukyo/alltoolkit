"""
Batch Rename Utilities Test Suite
批量文件重命名工具库测试

测试覆盖所有重命名功能，包括前缀后缀、序号、正则、大小写转换等。

Author: AllToolkit
Version: 1.0.0
"""

import os
import sys
import tempfile
import shutil
import unittest
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from batch_rename_utils import (
    add_prefix, add_suffix, remove_prefix, remove_suffix,
    replace_text, regex_replace, change_case, sequential_rename,
    datetime_rename, change_extension, custom_rename, undo_rename,
    batch_rename, get_files_by_pattern,
    RenameResult, RenamePreview
)


class TestRenameResult(unittest.TestCase):
    """测试 RenameResult 类"""
    
    def test_success_result(self):
        """测试成功结果"""
        old = Path('old.txt')
        new = Path('new.txt')
        result = RenameResult(True, old, new)
        
        self.assertTrue(result.success)
        self.assertEqual(result.old_path, old)
        self.assertEqual(result.new_path, new)
        self.assertIsNone(result.error)
    
    def test_failure_result(self):
        """测试失败结果"""
        old = Path('old.txt')
        new = Path('new.txt')
        result = RenameResult(False, old, new, "File not found")
        
        self.assertFalse(result.success)
        self.assertEqual(result.error, "File not found")


class TestRenamePreview(unittest.TestCase):
    """测试 RenamePreview 类"""
    
    def test_preview_properties(self):
        """测试预览属性"""
        old = Path('old.txt')
        new = Path('new.txt')
        preview = RenamePreview(old, new)
        
        self.assertEqual(preview.old_name, 'old.txt')
        self.assertEqual(preview.new_name, 'new.txt')
        self.assertEqual(preview.old_path, old)
        self.assertEqual(preview.new_path, new)


class TestAddPrefix(unittest.TestCase):
    """测试添加前缀"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'test.txt'
        self.test_file.write_text('content')
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_add_prefix_preview(self):
        """测试添加前缀预览"""
        results = add_prefix([self.test_file], 'prefix_', preview=True)
        
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], RenamePreview)
        self.assertEqual(results[0].new_name, 'prefix_test.txt')
        # 原文件应保持不变
        self.assertTrue(self.test_file.exists())
    
    def test_add_prefix_execute(self):
        """测试添加前缀执行"""
        results = add_prefix([self.test_file], 'new_')
        
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].success)
        self.assertFalse(self.test_file.exists())
        
        new_file = Path(self.temp_dir) / 'new_test.txt'
        self.assertTrue(new_file.exists())
    
    def test_add_prefix_multiple_files(self):
        """测试多个文件添加前缀"""
        files = []
        for i in range(3):
            f = Path(self.temp_dir) / f'file{i}.txt'
            f.write_text('content')
            files.append(f)
        
        results = add_prefix(files, 'prefix_', preview=True)
        
        self.assertEqual(len(results), 3)
        for i, r in enumerate(results):
            self.assertEqual(r.new_name, f'prefix_file{i}.txt')


class TestAddSuffix(unittest.TestCase):
    """测试添加后缀"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'test.txt'
        self.test_file.write_text('content')
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_add_suffix_before_ext(self):
        """测试在扩展名前添加后缀"""
        results = add_suffix([self.test_file], '_backup', before_ext=True, preview=True)
        
        self.assertEqual(results[0].new_name, 'test_backup.txt')
    
    def test_add_suffix_after_ext(self):
        """测试在扩展名后添加后缀"""
        results = add_suffix([self.test_file], '.bak', before_ext=False, preview=True)
        
        self.assertEqual(results[0].new_name, 'test.txt.bak')
    
    def test_add_suffix_execute(self):
        """测试添加后缀执行"""
        results = add_suffix([self.test_file], '_old')
        
        self.assertTrue(results[0].success)
        new_file = Path(self.temp_dir) / 'test_old.txt'
        self.assertTrue(new_file.exists())


class TestRemovePrefix(unittest.TestCase):
    """测试移除前缀"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'prefix_test.txt'
        self.test_file.write_text('content')
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_remove_prefix(self):
        """测试移除前缀"""
        results = remove_prefix([self.test_file], 'prefix_', preview=True)
        
        self.assertEqual(results[0].new_name, 'test.txt')
    
    def test_remove_prefix_no_match(self):
        """测试移除不存在的前缀"""
        results = remove_prefix([self.test_file], 'other_', preview=True)
        
        # 无变化
        self.assertEqual(results[0].new_name, 'prefix_test.txt')
    
    def test_remove_prefix_execute(self):
        """测试移除前缀执行"""
        results = remove_prefix([self.test_file], 'prefix_')
        
        self.assertTrue(results[0].success)
        new_file = Path(self.temp_dir) / 'test.txt'
        self.assertTrue(new_file.exists())


class TestRemoveSuffix(unittest.TestCase):
    """测试移除后缀"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'test_backup.txt'
        self.test_file.write_text('content')
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_remove_suffix_before_ext(self):
        """测试移除扩展名前的后缀"""
        results = remove_suffix([self.test_file], '_backup', before_ext=True, preview=True)
        
        self.assertEqual(results[0].new_name, 'test.txt')
    
    def test_remove_suffix_no_match(self):
        """测试移除不存在的后缀"""
        results = remove_suffix([self.test_file], '_other', preview=True)
        
        self.assertEqual(results[0].new_name, 'test_backup.txt')


class TestReplaceText(unittest.TestCase):
    """测试文本替换"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'old_file.txt'
        self.test_file.write_text('content')
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_replace_text(self):
        """测试文本替换"""
        results = replace_text([self.test_file], 'old', 'new', preview=True)
        
        self.assertEqual(results[0].new_name, 'new_file.txt')
    
    def test_replace_text_multiple(self):
        """测试多次替换"""
        f = Path(self.temp_dir) / 'test_test_test.txt'
        f.write_text('content')
        
        results = replace_text([f], 'test', 'demo', preview=True)
        
        self.assertEqual(results[0].new_name, 'demo_demo_demo.txt')
    
    def test_replace_text_execute(self):
        """测试文本替换执行"""
        results = replace_text([self.test_file], 'old', 'new')
        
        self.assertTrue(results[0].success)
        new_file = Path(self.temp_dir) / 'new_file.txt'
        self.assertTrue(new_file.exists())


class TestRegexReplace(unittest.TestCase):
    """测试正则表达式替换"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_regex_replace_digits(self):
        """测试替换数字"""
        f = Path(self.temp_dir) / 'IMG_1234.jpg'
        f.write_text('content')
        
        results = regex_replace([f], r'\d+', '0000', preview=True)
        
        self.assertEqual(results[0].new_name, 'IMG_0000.jpg')
    
    def test_regex_replace_with_group(self):
        """测试正则分组替换"""
        f = Path(self.temp_dir) / 'photo_2023_05_29.jpg'
        f.write_text('content')
        
        results = regex_replace([f], r'photo_(\d{4})_(\d{2})_(\d{2})', r'IMG_\1\2\3', preview=True)
        
        self.assertEqual(results[0].new_name, 'IMG_20230529.jpg')
    
    def test_regex_replace_extension(self):
        """测试替换扩展名"""
        f = Path(self.temp_dir) / 'document.txt'
        f.write_text('content')
        
        results = regex_replace([f], r'\.txt$', '.md', preview=True)
        
        self.assertEqual(results[0].new_name, 'document.md')
    
    def test_regex_replace_case_insensitive(self):
        """测试大小写不敏感替换"""
        f = Path(self.temp_dir) / 'TEST_FILE.txt'
        f.write_text('content')
        
        results = regex_replace([f], r'test', 'demo', flags=0, preview=True)
        self.assertEqual(results[0].new_name, 'TEST_FILE.txt')
        
        results = regex_replace([f], r'test', 'demo', flags=2, preview=True)  # re.IGNORECASE = 2
        self.assertEqual(results[0].new_name, 'demo_FILE.txt')
    
    def test_regex_invalid_pattern(self):
        """测试无效正则模式"""
        f = Path(self.temp_dir) / 'test.txt'
        f.write_text('content')
        
        results = regex_replace([f], r'[invalid', 'new')
        
        self.assertFalse(results[0].success)
        self.assertIn('Invalid regex', results[0].error)


class TestChangeCase(unittest.TestCase):
    """测试大小写转换"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_to_lower(self):
        """测试转小写"""
        f = Path(self.temp_dir) / 'HELLO.txt'
        f.write_text('content')
        
        results = change_case([f], 'lower', preview=True)
        
        self.assertEqual(results[0].new_name, 'hello.txt')
    
    def test_to_upper(self):
        """测试转大写"""
        f = Path(self.temp_dir) / 'hello.txt'
        f.write_text('content')
        
        results = change_case([f], 'upper', preview=True)
        
        self.assertEqual(results[0].new_name, 'HELLO.TXT')
    
    def test_to_title(self):
        """测试标题化"""
        f = Path(self.temp_dir) / 'hello world.txt'
        f.write_text('content')
        
        results = change_case([f], 'title', preview=True)
        
        self.assertEqual(results[0].new_name, 'Hello World.Txt')
    
    def test_to_capitalize(self):
        """测试首字母大写"""
        f = Path(self.temp_dir) / 'hello world.txt'
        f.write_text('content')
        
        results = change_case([f], 'capitalize', preview=True)
        
        self.assertEqual(results[0].new_name, 'Hello world.txt')
    
    def test_swap_case(self):
        """测试大小写互换"""
        f = Path(self.temp_dir) / 'HeLLo.txt'
        f.write_text('content')
        
        results = change_case([f], 'swap', preview=True)
        
        self.assertEqual(results[0].new_name, 'hEllO.TXT')
    
    def test_invalid_case_mode(self):
        """测试无效大小写模式"""
        f = Path(self.temp_dir) / 'test.txt'
        f.write_text('content')
        
        results = change_case([f], 'invalid')
        
        self.assertFalse(results[0].success)


class TestSequentialRename(unittest.TestCase):
    """测试序号重命名"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.files = []
        for name in ['a.txt', 'b.txt', 'c.txt']:
            f = Path(self.temp_dir) / name
            f.write_text('content')
            self.files.append(f)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_sequential_rename_preview(self):
        """测试序号重命名预览"""
        results = sequential_rename(self.files, 'photo', start=1, preview=True)
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].new_name, 'photo_001.txt')
        self.assertEqual(results[1].new_name, 'photo_002.txt')
        self.assertEqual(results[2].new_name, 'photo_003.txt')
    
    def test_sequential_rename_custom_digits(self):
        """测试自定义位数"""
        results = sequential_rename(self.files, 'img', start=1, digits=4, preview=True)
        
        self.assertEqual(results[0].new_name, 'img_0001.txt')
    
    def test_sequential_rename_custom_separator(self):
        """测试自定义分隔符"""
        results = sequential_rename(self.files, 'file', separator='-', preview=True)
        
        self.assertEqual(results[0].new_name, 'file-001.txt')
    
    def test_sequential_rename_start_value(self):
        """测试起始值"""
        results = sequential_rename(self.files, 'doc', start=10, preview=True)
        
        self.assertEqual(results[0].new_name, 'doc_010.txt')
        self.assertEqual(results[1].new_name, 'doc_011.txt')
    
    def test_sequential_rename_execute(self):
        """测试序号重命名执行"""
        results = sequential_rename(self.files, 'test')
        
        self.assertTrue(all(r.success for r in results))
        
        # 验证新文件存在
        self.assertTrue((Path(self.temp_dir) / 'test_001.txt').exists())
        self.assertTrue((Path(self.temp_dir) / 'test_002.txt').exists())
        self.assertTrue((Path(self.temp_dir) / 'test_003.txt').exists())
    
    def test_sequential_rename_no_extension(self):
        """测试不保留扩展名"""
        results = sequential_rename(self.files, 'data', keep_ext=False, preview=True)
        
        self.assertEqual(results[0].new_name, 'data_001')


class TestDatetimeRename(unittest.TestCase):
    """测试日期时间重命名"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'photo.jpg'
        self.test_file.write_text('content')
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_datetime_rename_default_format(self):
        """测试默认日期时间格式"""
        results = datetime_rename([self.test_file], preview=True)
        
        # 默认格式 %Y%m%d_%H%M%S
        import re
        pattern = r'^\d{8}_\d{6}\.jpg$'
        self.assertTrue(re.match(pattern, results[0].new_name))
    
    def test_datetime_rename_custom_format(self):
        """测试自定义日期时间格式"""
        results = datetime_rename([self.test_file], format_str='%Y-%m-%d', preview=True)
        
        import re
        pattern = r'^\d{4}-\d{2}-\d{2}\.jpg$'
        self.assertTrue(re.match(pattern, results[0].new_name))
    
    def test_datetime_rename_with_prefix_suffix(self):
        """测试带前缀后缀"""
        results = datetime_rename([self.test_file], prefix='IMG_', suffix='_backup', preview=True)
        
        self.assertTrue(results[0].new_name.startswith('IMG_'))
        self.assertTrue(results[0].new_name.endswith('_backup.jpg'))
    
    def test_datetime_rename_no_extension(self):
        """测试不保留扩展名"""
        results = datetime_rename([self.test_file], keep_ext=False, preview=True)
        
        # 无扩展名
        self.assertFalse(results[0].new_name.endswith('.jpg'))


class TestChangeExtension(unittest.TestCase):
    """测试更改扩展名"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'data.txt'
        self.test_file.write_text('content')
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_change_extension_with_dot(self):
        """测试带点的扩展名"""
        results = change_extension([self.test_file], '.md', preview=True)
        
        self.assertEqual(results[0].new_name, 'data.md')
    
    def test_change_extension_without_dot(self):
        """测试不带点的扩展名"""
        results = change_extension([self.test_file], 'md', preview=True)
        
        self.assertEqual(results[0].new_name, 'data.md')
    
    def test_change_extension_execute(self):
        """测试更改扩展名执行"""
        results = change_extension([self.test_file], '.md')
        
        self.assertTrue(results[0].success)
        new_file = Path(self.temp_dir) / 'data.md'
        self.assertTrue(new_file.exists())


class TestCustomRename(unittest.TestCase):
    """测试自定义重命名"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'test_file.txt'
        self.test_file.write_text('content')
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_custom_rename_uppercase(self):
        """测试自定义大写重命名"""
        def uppercase_rename(path):
            return path.stem.upper() + path.suffix
        
        results = custom_rename([self.test_file], uppercase_rename, preview=True)
        
        self.assertEqual(results[0].new_name, 'TEST_FILE.txt')
    
    def test_custom_rename_complex(self):
        """测试复杂自定义重命名"""
        def complex_rename(path):
            import hashlib
            h = hashlib.md5(path.stem.encode()).hexdigest()[:8]
            return f"{path.stem}_{h}{path.suffix}"
        
        results = custom_rename([self.test_file], complex_rename, preview=True)
        
        self.assertTrue(results[0].new_name.startswith('test_file_'))
        self.assertTrue(results[0].new_name.endswith('.txt'))
    
    def test_custom_rename_execute(self):
        """测试自定义重命名执行"""
        def add_date(path):
            from datetime import datetime
            return f"{path.stem}_{datetime.now().strftime('%Y%m%d')}{path.suffix}"
        
        results = custom_rename([self.test_file], add_date)
        
        self.assertTrue(results[0].success)


class TestUndoRename(unittest.TestCase):
    """测试撤销重命名"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'original.txt'
        self.test_file.write_text('content')
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_undo_prefix(self):
        """测试撤销添加前缀"""
        # 添加前缀
        results = add_prefix([self.test_file], 'new_')
        self.assertTrue(results[0].success)
        
        new_file = Path(self.temp_dir) / 'new_original.txt'
        self.assertTrue(new_file.exists())
        
        # 撤销
        undo_results = undo_rename(results)
        self.assertTrue(undo_results[0].success)
        self.assertTrue(self.test_file.exists())
    
    def test_undo_sequential(self):
        """测试撤销序号重命名"""
        files = []
        for name in ['a.txt', 'b.txt']:
            f = Path(self.temp_dir) / name
            f.write_text('content')
            files.append(f)
        
        results = sequential_rename(files, 'file')
        self.assertTrue(all(r.success for r in results))
        
        # 撤销
        undo_results = undo_rename(results)
        self.assertTrue(all(r.success for r in undo_results))
    
    def test_undo_no_change(self):
        """测试撤销无变化的结果"""
        results = [RenameResult(True, self.test_file, self.test_file)]
        undo_results = undo_rename(results)
        
        self.assertTrue(undo_results[0].success)


class TestBatchRename(unittest.TestCase):
    """测试批量重命名"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'TEST.txt'
        self.test_file.write_text('content')
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_batch_single_operation(self):
        """测试单操作批量重命名"""
        ops = [{'type': 'case', 'mode': 'lower'}]
        results = batch_rename([self.test_file], ops, preview=True)
        
        self.assertEqual(results[0].new_name, 'test.txt')
    
    def test_batch_multiple_operations(self):
        """测试多操作批量重命名"""
        ops = [
            {'type': 'prefix', 'value': 'new_'},
            {'type': 'case', 'mode': 'lower'}
        ]
        results = batch_rename([self.test_file], ops, preview=True)
        
        self.assertEqual(results[0].new_name, 'new_test.txt')
    
    def test_batch_replace_and_extension(self):
        """测试替换和扩展名操作"""
        ops = [
            {'type': 'replace', 'old': 'TEST', 'new': 'DATA'},
            {'type': 'extension', 'value': '.md'}
        ]
        results = batch_rename([self.test_file], ops, preview=True)
        
        self.assertEqual(results[0].new_name, 'DATA.md')
    
    def test_batch_regex_operation(self):
        """测试正则操作"""
        f = Path(self.temp_dir) / 'file_123.txt'
        f.write_text('content')
        
        ops = [{'type': 'regex', 'pattern': r'\d+', 'replacement': 'XXX'}]
        results = batch_rename([f], ops, preview=True)
        
        self.assertEqual(results[0].new_name, 'file_XXX.txt')
    
    def test_batch_execute(self):
        """测试批量重命名执行"""
        ops = [
            {'type': 'prefix', 'value': 'final_'},
            {'type': 'case', 'mode': 'lower'}
        ]
        results = batch_rename([self.test_file], ops)
        
        # 批量操作返回最后一步的结果
        self.assertTrue(all(r.success for r in results))


class TestGetFilesByPattern(unittest.TestCase):
    """测试按模式获取文件"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建测试文件结构
        Path(self.temp_dir, 'file1.txt').write_text('content')
        Path(self.temp_dir, 'file2.txt').write_text('content')
        Path(self.temp_dir, 'image.jpg').write_text('content')
        
        subdir = Path(self.temp_dir) / 'subdir'
        subdir.mkdir()
        Path(subdir, 'file3.txt').write_text('content')
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_get_files_non_recursive(self):
        """测试非递归获取文件"""
        files = get_files_by_pattern(self.temp_dir, '*.txt')
        
        self.assertEqual(len(files), 2)
    
    def test_get_files_recursive(self):
        """测试递归获取文件"""
        files = get_files_by_pattern(self.temp_dir, '*.txt', recursive=True)
        
        self.assertEqual(len(files), 3)
    
    def test_get_files_all(self):
        """测试获取所有文件"""
        files = get_files_by_pattern(self.temp_dir, '*')
        
        # 包括 file1.txt, file2.txt, image.jpg, subdir (目录)
        self.assertGreaterEqual(len(files), 3)
    
    def test_get_files_invalid_directory(self):
        """测试无效目录"""
        files = get_files_by_pattern('/nonexistent', '*.txt')
        
        self.assertEqual(len(files), 0)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_empty_file_list(self):
        """测试空文件列表"""
        results = add_prefix([], 'prefix_', preview=True)
        self.assertEqual(len(results), 0)
    
    def test_unicode_filename(self):
        """测试 Unicode 文件名"""
        f = Path(self.temp_dir) / '测试文件.txt'
        f.write_text('content')
        
        results = add_prefix([f], '前缀_', preview=True)
        self.assertEqual(results[0].new_name, '前缀_测试文件.txt')
    
    def test_special_characters(self):
        """测试特殊字符"""
        f = Path(self.temp_dir) / 'file (1).txt'
        f.write_text('content')
        
        results = add_suffix([f], '_backup', preview=True)
        self.assertEqual(results[0].new_name, 'file (1)_backup.txt')
    
    def test_no_extension(self):
        """测试无扩展名文件"""
        f = Path(self.temp_dir) / 'README'
        f.write_text('content')
        
        results = add_suffix([f], '_v1', preview=True)
        self.assertEqual(results[0].new_name, 'README_v1')
    
    def test_multiple_dots_in_name(self):
        """测试多个点的文件名"""
        f = Path(self.temp_dir) / 'file.name.with.dots.txt'
        f.write_text('content')
        
        results = add_suffix([f], '_bak', preview=True)
        self.assertEqual(results[0].new_name, 'file.name.with.dots_bak.txt')
    
    def test_hidden_file(self):
        """测试隐藏文件"""
        f = Path(self.temp_dir) / '.hidden'
        f.write_text('content')
        
        results = add_prefix([f], 'prefix_', preview=True)
        self.assertEqual(results[0].new_name, 'prefix_.hidden')
    
    def test_very_long_filename(self):
        """测试长文件名"""
        long_name = 'a' * 200 + '.txt'
        f = Path(self.temp_dir) / long_name
        f.write_text('content')
        
        results = add_prefix([f], 'prefix_', preview=True)
        self.assertTrue(results[0].new_name.startswith('prefix_'))


if __name__ == '__main__':
    unittest.main(verbosity=2)