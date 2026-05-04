"""
permission_utils 测试套件

测试权限解析、转换、比较等功能。
"""

import unittest
import os
import stat
import tempfile
import sys

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from permission_utils.mod import (
    PermissionUtils, PermissionInfo, PermissionBit,
    parse, to_symbolic, to_octal, compare, recommend
)


class TestPermissionParsing(unittest.TestCase):
    """测试权限解析功能"""
    
    def test_parse_octal_number(self):
        """测试解析八进制数字"""
        info = parse(0o755)
        self.assertEqual(info.mode, 0o755)
        self.assertTrue(info.owner_read)
        self.assertTrue(info.owner_write)
        self.assertTrue(info.owner_execute)
        self.assertTrue(info.group_read)
        self.assertFalse(info.group_write)
        self.assertTrue(info.group_execute)
        self.assertTrue(info.other_read)
        self.assertFalse(info.other_write)
        self.assertTrue(info.other_execute)
    
    def test_parse_decimal_number(self):
        """测试解析十进制数字"""
        info = parse(493)  # 0o755 = 493
        self.assertEqual(info.mode, 0o755)
    
    def test_parse_octal_string(self):
        """测试解析八进制字符串"""
        info = parse("755")
        self.assertEqual(info.mode, 0o755)
        
        info = parse("0755")
        self.assertEqual(info.mode, 0o755)
    
    def test_parse_symbolic(self):
        """测试解析符号权限"""
        info = parse("rwxr-xr-x")
        self.assertEqual(info.mode, 0o755)
        
        info = parse("rw-r--r--")
        self.assertEqual(info.mode, 0o644)
        
        info = parse("rwx------")
        self.assertEqual(info.mode, 0o700)
    
    def test_parse_with_special_bits(self):
        """测试解析带特殊位的权限"""
        # setuid
        info = parse("rwsr-xr-x")
        self.assertEqual(info.mode, 0o4755)
        self.assertTrue(info.setuid)
        self.assertTrue(info.owner_execute)
        
        # setgid
        info = parse("rwxr-sr-x")
        self.assertEqual(info.mode, 0o2755)
        self.assertTrue(info.setgid)
        
        # sticky
        info = parse("rwxr-xr-t")
        self.assertEqual(info.mode, 0o1755)
        self.assertTrue(info.sticky)
    
    def test_parse_invalid_symbolic(self):
        """测试解析无效符号权限"""
        with self.assertRaises(ValueError):
            PermissionUtils.from_symbolic("rwxr-x")  # 长度不够


class TestPermissionConversion(unittest.TestCase):
    """测试权限转换功能"""
    
    def test_to_symbolic(self):
        """测试转换为符号表示"""
        self.assertEqual(to_symbolic(0o755), "rwxr-xr-x")
        self.assertEqual(to_symbolic(0o644), "rw-r--r--")
        self.assertEqual(to_symbolic(0o777), "rwxrwxrwx")
        self.assertEqual(to_symbolic(0o000), "---------")
    
    def test_to_symbolic_with_special_bits(self):
        """测试带特殊位的符号转换"""
        # setuid
        self.assertIn('s', to_symbolic(0o4755))
        
        # setgid
        self.assertIn('s', to_symbolic(0o2755))
        
        # sticky
        self.assertIn('t', to_symbolic(0o1755))
    
    def test_to_octal(self):
        """测试转换为八进制"""
        self.assertEqual(to_octal(0o755), "0755")
        self.assertEqual(to_octal(0o644), "0644")
        self.assertEqual(to_octal(0o755, include_special=False), "755")


class TestChmodParsing(unittest.TestCase):
    """测试 chmod 风格解析"""
    
    def test_absolute_mode(self):
        """测试绝对模式"""
        self.assertEqual(PermissionUtils.parse_chmod_mode("755"), 0o755)
        self.assertEqual(PermissionUtils.parse_chmod_mode("644"), 0o644)
        self.assertEqual(PermissionUtils.parse_chmod_mode("700"), 0o700)
    
    def test_add_permission(self):
        """测试添加权限"""
        # u+x
        result = PermissionUtils.parse_chmod_mode("u+x", 0o644)
        self.assertEqual(result, 0o744)
        
        # g+w
        result = PermissionUtils.parse_chmod_mode("g+w", 0o644)
        self.assertEqual(result, 0o664)
        
        # o+x
        result = PermissionUtils.parse_chmod_mode("o+x", 0o644)
        self.assertEqual(result, 0o645)
    
    def test_remove_permission(self):
        """测试移除权限"""
        # u-x
        result = PermissionUtils.parse_chmod_mode("u-x", 0o755)
        self.assertEqual(result, 0o655)
        
        # go-w
        result = PermissionUtils.parse_chmod_mode("go-w", 0o777)
        self.assertEqual(result, 0o755)
    
    def test_set_permission(self):
        """测试设置权限"""
        # u=rwx
        result = PermissionUtils.parse_chmod_mode("u=rwx", 0o000)
        self.assertEqual(result, 0o700)
        
        # go=rx
        result = PermissionUtils.parse_chmod_mode("go=rx", 0o000)
        self.assertEqual(result, 0o055)
    
    def test_all_users(self):
        """测试所有用户操作"""
        # a+x
        result = PermissionUtils.parse_chmod_mode("a+x", 0o644)
        self.assertEqual(result, 0o755)
        
        # +x (默认对所有用户)
        result = PermissionUtils.parse_chmod_mode("+x", 0o644)
        self.assertEqual(result, 0o755)
    
    def test_compound_mode(self):
        """测试复合模式"""
        # u=rwx,go=rx
        result = PermissionUtils.parse_chmod_mode("u=rwx,go=rx", 0o000)
        self.assertEqual(result, 0o755)
        
        # u+rwx,g+rx,o-w
        result = PermissionUtils.parse_chmod_mode("u+rwx,g+rx,o-w", 0o000)
        self.assertEqual(result, 0o750)


class TestPermissionComparison(unittest.TestCase):
    """测试权限比较功能"""
    
    def test_compare_equal(self):
        """测试相等权限比较"""
        result = compare(0o755, 0o755)
        self.assertTrue(result['equal'])
        self.assertEqual(result['difference'], 0)
    
    def test_compare_different(self):
        """测试不同权限比较"""
        result = compare(0o644, 0o755)
        self.assertFalse(result['equal'])
        self.assertTrue(result['added'] > 0)
    
    def test_is_more_restrictive(self):
        """测试权限严格性判断"""
        self.assertTrue(PermissionUtils.is_more_restrictive(0o644, 0o755))
        self.assertFalse(PermissionUtils.is_more_restrictive(0o755, 0o644))
        self.assertFalse(PermissionUtils.is_more_restrictive(0o755, 0o755))
    
    def test_least_privilege(self):
        """测试最小权限计算"""
        result = PermissionUtils.get_least_privilege([0o755, 0o644, 0o750])
        self.assertEqual(result, 0o640)
    
    def test_most_privilege(self):
        """测试最大权限计算"""
        result = PermissionUtils.get_most_privilege([0o644, 0o755, 0o750])
        self.assertEqual(result, 0o755)


class TestUmask(unittest.TestCase):
    """测试 umask 功能"""
    
    def test_apply_umask_explicit(self):
        """测试显式应用 umask"""
        result = PermissionUtils.apply_umask(0o777, 0o022)
        self.assertEqual(result, 0o755)
        
        result = PermissionUtils.apply_umask(0o666, 0o022)
        self.assertEqual(result, 0o644)
    
    def test_get_umask(self):
        """测试获取 umask"""
        umask = PermissionUtils.get_umask()
        self.assertIsInstance(umask, int)
        self.assertGreaterEqual(umask, 0)
        self.assertLessEqual(umask, 0o777)


class TestRecommendedPermissions(unittest.TestCase):
    """测试推荐权限"""
    
    def test_recommend_file(self):
        """测试文件推荐权限"""
        self.assertEqual(recommend('file'), 0o644)
    
    def test_recommend_executable(self):
        """测试可执行文件推荐权限"""
        self.assertEqual(recommend('executable'), 0o755)
        self.assertEqual(recommend('file', is_executable=True), 0o755)
    
    def test_recommend_directory(self):
        """测试目录推荐权限"""
        self.assertEqual(recommend('dir'), 0o755)
    
    def test_recommend_private(self):
        """测试私有文件推荐权限"""
        self.assertEqual(recommend('file', is_private=True), 0o600)
        self.assertEqual(recommend('dir', is_private=True), 0o700)
    
    def test_recommend_shared(self):
        """测试共享文件推荐权限"""
        self.assertEqual(recommend('file', is_shared=True), 0o664)
        self.assertEqual(recommend('dir', is_shared=True), 0o2775)
    
    def test_recommend_config(self):
        """测试配置文件推荐权限"""
        self.assertEqual(recommend('config'), 0o600)
    
    def test_recommend_secret(self):
        """测试敏感文件推荐权限"""
        self.assertEqual(recommend('secret'), 0o600)


class TestPermissionCheck(unittest.TestCase):
    """测试权限检查功能"""
    
    def test_check_permission_existing_file(self):
        """测试检查现有文件权限"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('test')
            temp_path = f.name
        
        try:
            os.chmod(temp_path, 0o644)
            result = PermissionUtils.check_permission(temp_path, 0o644)
            self.assertTrue(result['exists'])
            self.assertTrue(result['is_file'])
            self.assertEqual(result['actual_mode'], 0o644)
            self.assertTrue(result['match'])
            self.assertTrue(result['can_read'])
            self.assertTrue(result['can_write'])
        finally:
            os.unlink(temp_path)
    
    def test_check_permission_nonexistent(self):
        """测试检查不存在的文件"""
        result = PermissionUtils.check_permission('/nonexistent/path', 0o644)
        self.assertFalse(result['exists'])
        self.assertFalse(result['match'])
    
    def test_check_permission_directory(self):
        """测试检查目录权限"""
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chmod(temp_dir, 0o755)
            result = PermissionUtils.check_permission(temp_dir, 0o755)
            self.assertTrue(result['exists'])
            self.assertTrue(result['is_dir'])
            self.assertEqual(result['actual_mode'], 0o755)


class TestPermissionExplain(unittest.TestCase):
    """测试权限解释功能"""
    
    def test_explain_basic(self):
        """测试基本权限解释"""
        explanation = PermissionUtils.explain(0o755)
        self.assertIn("755", explanation)
        self.assertIn("rwxr-xr-x", explanation)
        self.assertIn("所有者", explanation)
    
    def test_explain_with_special_bits(self):
        """测试带特殊位的权限解释"""
        # setuid
        explanation = PermissionUtils.explain(0o4755)
        self.assertIn("setuid", explanation.lower())
        
        # sticky
        explanation = PermissionUtils.explain(0o1755)
        self.assertIn("sticky", explanation.lower())


class TestPermissionInfo(unittest.TestCase):
    """测试 PermissionInfo 数据类"""
    
    def test_info_properties(self):
        """测试 PermissionInfo 属性"""
        info = parse(0o755)
        self.assertEqual(info.octal, "0755")
        self.assertEqual(info.octal_short, "755")
        self.assertEqual(info.symbolic, "rwxr-xr-x")
    
    def test_info_with_special_bits(self):
        """测试带特殊位的 PermissionInfo"""
        info = parse(0o4755)
        self.assertEqual(info.octal, "4755")
        self.assertTrue(info.setuid)
        self.assertFalse(info.setgid)
        self.assertFalse(info.sticky)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_zero_permission(self):
        """测试零权限"""
        info = parse(0)
        self.assertEqual(info.mode, 0)
        self.assertEqual(info.symbolic, "---------")
        self.assertFalse(info.owner_read)
        self.assertFalse(info.owner_write)
        self.assertFalse(info.owner_execute)
    
    def test_full_permission(self):
        """测试完全权限"""
        info = parse(0o777)
        self.assertEqual(info.mode, 0o777)
        self.assertEqual(info.symbolic, "rwxrwxrwx")
        self.assertTrue(info.owner_read)
        self.assertTrue(info.owner_write)
        self.assertTrue(info.owner_execute)
    
    def test_all_special_bits(self):
        """测试所有特殊位"""
        info = parse(0o7777)
        self.assertTrue(info.setuid)
        self.assertTrue(info.setgid)
        self.assertTrue(info.sticky)
    
    def test_chmod_empty(self):
        """测试空的 chmod 操作"""
        # 空操作应该不改变权限
        result = PermissionUtils.parse_chmod_mode("", 0o644)
        self.assertEqual(result, 0o644)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_parse_function(self):
        """测试 parse 便捷函数"""
        info = parse("755")
        self.assertEqual(info.mode, 0o755)
    
    def test_to_symbolic_function(self):
        """测试 to_symbolic 便捷函数"""
        self.assertEqual(to_symbolic(0o755), "rwxr-xr-x")
    
    def test_to_octal_function(self):
        """测试 to_octal 便捷函数"""
        self.assertEqual(to_octal(0o755), "0755")
    
    def test_compare_function(self):
        """测试 compare 便捷函数"""
        result = compare(0o644, 0o755)
        self.assertFalse(result['equal'])
    
    def test_recommend_function(self):
        """测试 recommend 便捷函数"""
        self.assertEqual(recommend('file'), 0o644)


if __name__ == '__main__':
    unittest.main(verbosity=2)