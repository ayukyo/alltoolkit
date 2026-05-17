"""
语义化版本工具测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    SemVer, parse, try_parse, is_valid, compare, equals,
    greater_than, less_than, gte, lte, sort, rsort,
    min_version, max_version, VersionRange, parse_range,
    satisfies, filter_versions, find_best_match,
    VersionDiff, diff, format, to_tuple, from_tuple,
    unique, next_versions, ZERO, ONE,
    major, minor, patch, prerelease, build
)


class TestSemVer:
    """SemVer 类测试"""
    
    def test_create_basic(self):
        """测试基本版本创建"""
        v = SemVer(1, 2, 3)
        assert str(v) == "1.2.3"
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 3
        assert v.prerelease is None
        assert v.build is None
        print("✅ test_create_basic")
    
    def test_create_with_prerelease(self):
        """测试带预发布标识的版本"""
        v = SemVer(1, 0, 0, "alpha.1")
        assert str(v) == "1.0.0-alpha.1"
        assert v.is_prerelease == True
        assert v.is_stable == False
        print("✅ test_create_with_prerelease")
    
    def test_create_with_build(self):
        """测试带构建元数据的版本"""
        v = SemVer(1, 0, 0, None, "build.123")
        assert str(v) == "1.0.0+build.123"
        print("✅ test_create_with_build")
    
    def test_create_full(self):
        """测试完整版本"""
        v = SemVer(2, 1, 0, "beta.2", "exp.sha.5114f85")
        assert str(v) == "2.1.0-beta.2+exp.sha.5114f85"
        print("✅ test_create_full")
    
    def test_equality(self):
        """测试相等比较"""
        v1 = SemVer(1, 2, 3)
        v2 = SemVer(1, 2, 3)
        v3 = SemVer(1, 2, 4)
        assert v1 == v2
        assert v1 != v3
        print("✅ test_equality")
    
    def test_equality_with_prerelease(self):
        """测试预发布版本相等"""
        v1 = SemVer(1, 0, 0, "alpha")
        v2 = SemVer(1, 0, 0, "alpha")
        v3 = SemVer(1, 0, 0, "beta")
        assert v1 == v2
        assert v1 != v3
        print("✅ test_equality_with_prerelease")
    
    def test_equality_ignores_build(self):
        """测试构建元数据不影响相等"""
        v1 = SemVer(1, 0, 0, None, "build.1")
        v2 = SemVer(1, 0, 0, None, "build.2")
        assert v1 == v2
        print("✅ test_equality_ignores_build")
    
    def test_comparison_basic(self):
        """测试基本比较"""
        v1 = SemVer(1, 0, 0)
        v2 = SemVer(2, 0, 0)
        v3 = SemVer(1, 1, 0)
        v4 = SemVer(1, 0, 1)
        
        assert v1 < v2
        assert v1 < v3
        assert v1 < v4
        assert v2 > v3
        assert v3 > v4
        print("✅ test_comparison_basic")
    
    def test_comparison_prerelease(self):
        """测试预发布版本比较"""
        # 预发布版本 < 正式版本
        v1 = SemVer(1, 0, 0, "alpha")
        v2 = SemVer(1, 0, 0)
        assert v1 < v2
        
        # 预发布版本内部比较
        v3 = SemVer(1, 0, 0, "alpha.1")
        v4 = SemVer(1, 0, 0, "alpha.2")
        assert v3 < v4
        
        # 数字标识符 < 字母标识符
        v5 = SemVer(1, 0, 0, "alpha.1")
        v6 = SemVer(1, 0, 0, "alpha.beta")
        assert v5 < v6
        print("✅ test_comparison_prerelease")
    
    def test_bump_major(self):
        """测试主版本递增"""
        v = SemVer(1, 2, 3, "alpha")
        new_v = v.bump_major()
        assert str(new_v) == "2.0.0"
        print("✅ test_bump_major")
    
    def test_bump_minor(self):
        """测试次版本递增"""
        v = SemVer(1, 2, 3, "beta")
        new_v = v.bump_minor()
        assert str(new_v) == "1.3.0"
        print("✅ test_bump_minor")
    
    def test_bump_patch(self):
        """测试修订版本递增"""
        v = SemVer(1, 2, 3, "rc.1")
        new_v = v.bump_patch()
        assert str(new_v) == "1.2.4"
        print("✅ test_bump_patch")
    
    def test_bump_prerelease(self):
        """测试预发布版本递增"""
        v = SemVer(1, 0, 0)
        
        # 创建新预发布
        v1 = v.bump_prerelease("alpha")
        assert str(v1) == "1.0.0-alpha.1"
        
        # 递增预发布
        v2 = v1.bump_prerelease("alpha")
        assert str(v2) == "1.0.0-alpha.2"
        
        # 切换预发布类型
        v3 = v2.bump_prerelease("beta")
        assert str(v3) == "1.0.0-beta.1"
        print("✅ test_bump_prerelease")
    
    def test_with_prerelease(self):
        """测试设置预发布标识"""
        v = SemVer(1, 2, 3)
        new_v = v.with_prerelease("rc.1")
        assert str(new_v) == "1.2.3-rc.1"
        print("✅ test_with_prerelease")
    
    def test_with_build(self):
        """测试设置构建元数据"""
        v = SemVer(1, 2, 3)
        new_v = v.with_build("20240101")
        assert str(new_v) == "1.2.3+20240101"
        print("✅ test_with_build")
    
    def test_release(self):
        """测试移除预发布标识"""
        v = SemVer(1, 2, 3, "alpha.1", "build.1")
        released = v.release()
        assert str(released) == "1.2.3+build.1"
        print("✅ test_release")
    
    def test_is_stable(self):
        """测试稳定版本判断"""
        v1 = SemVer(0, 1, 0)
        v2 = SemVer(1, 0, 0)
        v3 = SemVer(1, 0, 0, "alpha")
        v4 = SemVer(2, 0, 0)
        
        assert v1.is_stable == False  # 主版本为 0
        assert v2.is_stable == True
        assert v3.is_stable == False  # 预发布版本
        assert v4.is_stable == True
        print("✅ test_is_stable")


class TestParse:
    """解析测试"""
    
    def test_parse_basic(self):
        """测试基本解析"""
        v = parse("1.2.3")
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 3
        print("✅ test_parse_basic")
    
    def test_parse_with_prerelease(self):
        """测试预发布解析"""
        v = parse("1.0.0-alpha.1")
        assert v.prerelease == "alpha.1"
        print("✅ test_parse_with_prerelease")
    
    def test_parse_with_build(self):
        """测试构建元数据解析"""
        v = parse("1.0.0+build.123")
        assert v.build == "build.123"
        print("✅ test_parse_with_build")
    
    def test_parse_full(self):
        """测试完整解析"""
        v = parse("1.0.0-beta.2+exp.sha.5114f85")
        assert v.major == 1
        assert v.minor == 0
        assert v.patch == 0
        assert v.prerelease == "beta.2"
        assert v.build == "exp.sha.5114f85"
        print("✅ test_parse_full")
    
    def test_parse_invalid(self):
        """测试无效版本"""
        invalid = ["1", "1.2", "v1.0.0", "1.0.0.", "1.0.0-", ""]
        for v in invalid:
            try:
                parse(v)
                assert False, f"Should fail: {v}"
            except ValueError:
                pass
        print("✅ test_parse_invalid")
    
    def test_try_parse(self):
        """测试安全解析"""
        v = try_parse("1.0.0")
        assert v is not None
        assert str(v) == "1.0.0"
        
        v = try_parse("invalid")
        assert v is None
        print("✅ test_try_parse")
    
    def test_is_valid(self):
        """测试有效性验证"""
        assert is_valid("1.0.0") == True
        assert is_valid("1.0.0-alpha") == True
        assert is_valid("1.0.0+build") == True
        assert is_valid("1.0.0-alpha+build") == True
        assert is_valid("invalid") == False
        assert is_valid("v1.0.0") == False
        print("✅ test_is_valid")


class TestComparison:
    """比较测试"""
    
    def test_compare(self):
        """测试版本比较"""
        assert compare("1.0.0", "2.0.0") < 0
        assert compare("2.0.0", "1.0.0") > 0
        assert compare("1.0.0", "1.0.0") == 0
        assert compare("1.0.0", "1.0.1") < 0
        assert compare("1.1.0", "1.0.9") > 0
        print("✅ test_compare")
    
    def test_equals(self):
        """测试相等"""
        assert equals("1.0.0", "1.0.0") == True
        assert equals("1.0.0", "1.0.1") == False
        assert equals("1.0.0+build1", "1.0.0+build2") == True
        print("✅ test_equals")
    
    def test_greater_than(self):
        """测试大于"""
        assert greater_than("2.0.0", "1.0.0") == True
        assert greater_than("1.0.0", "2.0.0") == False
        assert greater_than("1.0.0", "1.0.0") == False
        print("✅ test_greater_than")
    
    def test_less_than(self):
        """测试小于"""
        assert less_than("1.0.0", "2.0.0") == True
        assert less_than("2.0.0", "1.0.0") == False
        assert less_than("1.0.0", "1.0.0") == False
        print("✅ test_less_than")
    
    def test_gte_lte(self):
        """测试大于等于和小于等于"""
        assert gte("1.0.0", "1.0.0") == True
        assert gte("2.0.0", "1.0.0") == True
        assert gte("1.0.0", "2.0.0") == False
        
        assert lte("1.0.0", "1.0.0") == True
        assert lte("1.0.0", "2.0.0") == True
        assert lte("2.0.0", "1.0.0") == False
        print("✅ test_gte_lte")


class TestSorting:
    """排序测试"""
    
    def test_sort_ascending(self):
        """测试升序排序"""
        versions = ["2.0.0", "1.0.0", "1.1.0", "1.0.1"]
        sorted_v = sort(versions)
        assert [str(v) for v in sorted_v] == ["1.0.0", "1.0.1", "1.1.0", "2.0.0"]
        print("✅ test_sort_ascending")
    
    def test_sort_descending(self):
        """测试降序排序"""
        versions = ["1.0.0", "2.0.0", "1.5.0"]
        sorted_v = rsort(versions)
        assert [str(v) for v in sorted_v] == ["2.0.0", "1.5.0", "1.0.0"]
        print("✅ test_sort_descending")
    
    def test_sort_with_prerelease(self):
        """测试预发布版本排序"""
        versions = ["1.0.0", "1.0.0-alpha", "1.0.0-beta", "1.0.0-alpha.2", "1.0.0-alpha.1"]
        sorted_v = sort(versions)
        expected = ["1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-alpha.2", "1.0.0-beta", "1.0.0"]
        assert [str(v) for v in sorted_v] == expected
        print("✅ test_sort_with_prerelease")
    
    def test_min_max(self):
        """测试最小最大版本"""
        versions = ["1.0.0", "2.0.0", "0.5.0", "1.5.0"]
        assert str(min_version(versions)) == "0.5.0"
        assert str(max_version(versions)) == "2.0.0"
        print("✅ test_min_max")
    
    def test_min_max_empty(self):
        """测试空列表"""
        assert min_version([]) is None
        assert max_version([]) is None
        print("✅ test_min_max_empty")


class TestRange:
    """版本范围测试"""
    
    def test_parse_range_star(self):
        """测试通配符范围"""
        r = parse_range("*")
        assert r.contains("1.0.0") == True
        assert r.contains("100.0.0") == True
        print("✅ test_parse_range_star")
    
    def test_parse_range_exact(self):
        """测试精确版本"""
        r = parse_range("1.2.3")
        assert r.contains("1.2.3") == True
        assert r.contains("1.2.4") == False
        assert r.contains("1.3.0") == False
        print("✅ test_parse_range_exact")
    
    def test_parse_range_gte(self):
        """测试大于等于"""
        r = parse_range(">=1.0.0")
        assert r.contains("1.0.0") == True
        assert r.contains("2.0.0") == True
        assert r.contains("0.9.9") == False
        print("✅ test_parse_range_gte")
    
    def test_parse_range_gt(self):
        """测试大于"""
        r = parse_range(">1.0.0")
        assert r.contains("1.0.0") == False
        assert r.contains("1.0.1") == True
        assert r.contains("2.0.0") == True
        print("✅ test_parse_range_gt")
    
    def test_parse_range_lte(self):
        """测试小于等于"""
        r = parse_range("<=2.0.0")
        assert r.contains("2.0.0") == True
        assert r.contains("1.9.9") == True
        assert r.contains("2.0.1") == False
        print("✅ test_parse_range_lte")
    
    def test_parse_range_lt(self):
        """测试小于"""
        r = parse_range("<2.0.0")
        assert r.contains("2.0.0") == False
        assert r.contains("1.9.9") == True
        assert r.contains("1.0.0") == True
        print("✅ test_parse_range_lt")
    
    def test_parse_range_combination(self):
        """测试组合范围"""
        r = parse_range(">=1.0.0 <2.0.0")
        assert r.contains("1.0.0") == True
        assert r.contains("1.9.9") == True
        assert r.contains("2.0.0") == False
        assert r.contains("0.9.9") == False
        print("✅ test_parse_range_combination")
    
    def test_parse_range_caret(self):
        """测试插入符范围"""
        # ^1.2.3 := >=1.2.3 <2.0.0
        r = parse_range("^1.2.3")
        assert r.contains("1.2.3") == True
        assert r.contains("1.9.9") == True
        assert r.contains("2.0.0") == False
        assert r.contains("1.2.2") == False
        print("✅ test_parse_range_caret")
    
    def test_parse_range_caret_zero(self):
        """测试插入符范围（零版本）"""
        # ^0.2.3 := >=0.2.3 <0.3.0
        r = parse_range("^0.2.3")
        assert r.contains("0.2.3") == True
        assert r.contains("0.2.9") == True
        assert r.contains("0.3.0") == False
        
        # ^0.0.3 := >=0.0.3 <0.0.4
        r = parse_range("^0.0.3")
        assert r.contains("0.0.3") == True
        assert r.contains("0.0.4") == False
        print("✅ test_parse_range_caret_zero")
    
    def test_parse_range_tilde(self):
        """测试波浪号范围"""
        # ~1.2.3 := >=1.2.3 <1.3.0
        r = parse_range("~1.2.3")
        assert r.contains("1.2.3") == True
        assert r.contains("1.2.9") == True
        assert r.contains("1.3.0") == False
        assert r.contains("1.2.2") == False
        print("✅ test_parse_range_tilde")
    
    def test_parse_range_tilde_short(self):
        """测试短波浪号范围"""
        # ~1.2 := >=1.2.0 <1.3.0
        r = parse_range("~1.2")
        assert r.contains("1.2.0") == True
        assert r.contains("1.2.9") == True
        assert r.contains("1.3.0") == False
        
        # ~1 := >=1.0.0 <2.0.0
        r = parse_range("~1")
        assert r.contains("1.0.0") == True
        assert r.contains("1.9.9") == True
        assert r.contains("2.0.0") == False
        print("✅ test_parse_range_tilde_short")
    
    def test_parse_range_x_wildcard(self):
        """测试 x 通配符"""
        # 1.2.x
        r = parse_range("1.2.x")
        assert r.contains("1.2.0") == True
        assert r.contains("1.2.9") == True
        assert r.contains("1.3.0") == False
        
        # 1.x
        r = parse_range("1.x")
        assert r.contains("1.0.0") == True
        assert r.contains("1.9.9") == True
        assert r.contains("2.0.0") == False
        print("✅ test_parse_range_x_wildcard")
    
    def test_satisfies(self):
        """测试满足约束"""
        assert satisfies("1.2.3", "^1.0.0") == True
        assert satisfies("2.0.0", "^1.0.0") == False
        assert satisfies("1.2.3", "~1.2.0") == True
        assert satisfies("1.3.0", "~1.2.0") == False
        print("✅ test_satisfies")
    
    def test_filter_versions(self):
        """测试过滤版本"""
        versions = ["1.0.0", "1.1.0", "1.2.0", "2.0.0", "2.1.0"]
        filtered = filter_versions(versions, ">=1.0.0 <2.0.0")
        assert [str(v) for v in filtered] == ["1.0.0", "1.1.0", "1.2.0"]
        print("✅ test_filter_versions")
    
    def test_find_best_match(self):
        """测试最佳匹配"""
        versions = ["1.0.0", "1.1.0", "1.2.0", "1.3.0-alpha", "2.0.0"]
        
        # 排除预发布
        best = find_best_match(versions, "^1.0.0")
        assert str(best) == "1.2.0"
        
        # 包含预发布
        best = find_best_match(versions, "^1.0.0", prefer_prerelease=True)
        assert str(best) == "1.3.0-alpha"
        
        # 无匹配
        best = find_best_match(versions, "^3.0.0")
        assert best is None
        print("✅ test_find_best_match")


class TestDiff:
    """版本差异测试"""
    
    def test_diff_upgrade_patch(self):
        """测试修订版本升级"""
        d = diff("1.0.0", "1.0.1")
        assert d.major_diff == 0
        assert d.minor_diff == 0
        assert d.patch_diff == 1
        assert d.is_upgrade == True
        assert d.is_downgrade == False
        assert d.is_patch_change == True
        print("✅ test_diff_upgrade_patch")
    
    def test_diff_upgrade_minor(self):
        """测试次版本升级"""
        d = diff("1.0.0", "1.1.0")
        assert d.minor_diff == 1
        assert d.is_minor_change == True
        assert d.is_upgrade == True
        print("✅ test_diff_upgrade_minor")
    
    def test_diff_upgrade_major(self):
        """测试主版本升级"""
        d = diff("1.0.0", "2.0.0")
        assert d.major_diff == 1
        assert d.is_major_change == True
        assert d.is_upgrade == True
        print("✅ test_diff_upgrade_major")
    
    def test_diff_downgrade(self):
        """测试降级"""
        d = diff("2.0.0", "1.0.0")
        assert d.major_diff == -1
        assert d.is_downgrade == True
        assert d.is_upgrade == False
        print("✅ test_diff_downgrade")
    
    def test_diff_no_change(self):
        """测试无变化"""
        d = diff("1.0.0", "1.0.0")
        assert d.major_diff == 0
        assert d.minor_diff == 0
        assert d.patch_diff == 0
        assert d.is_upgrade == False
        assert d.is_downgrade == False
        print("✅ test_diff_no_change")
    
    def test_diff_prerelease(self):
        """测试预发布变化"""
        d = diff("1.0.0-alpha", "1.0.0-beta")
        assert d.prerelease_change == ("alpha", "beta")
        print("✅ test_diff_prerelease")
    
    def test_diff_build(self):
        """测试构建元数据变化"""
        d = diff("1.0.0+build.1", "1.0.0+build.2")
        assert d.build_change == ("build.1", "build.2")
        print("✅ test_diff_build")


class TestFormat:
    """格式化测试"""
    
    def test_format_full(self):
        """测试完整格式化"""
        v = SemVer(1, 2, 3, "alpha.1", "build.123")
        assert format(v) == "1.2.3-alpha.1+build.123"
        assert format(v, include_prerelease=False) == "1.2.3+build.123"
        assert format(v, include_build=False) == "1.2.3-alpha.1"
        assert format(v, include_prerelease=False, include_build=False) == "1.2.3"
        print("✅ test_format_full")
    
    def test_to_tuple(self):
        """测试元组转换"""
        assert to_tuple("1.2.3") == (1, 2, 3)
        assert to_tuple(SemVer(2, 0, 0)) == (2, 0, 0)
        print("✅ test_to_tuple")
    
    def test_from_tuple(self):
        """测试从元组创建"""
        v = from_tuple((1, 2, 3))
        assert str(v) == "1.2.3"
        
        v = from_tuple((1, 2, 3), "alpha", "build")
        assert str(v) == "1.2.3-alpha+build"
        print("✅ test_from_tuple")


class TestUtilities:
    """工具函数测试"""
    
    def test_accessors(self):
        """测试访问器"""
        v = SemVer(1, 2, 3, "alpha", "build")
        assert major(v) == 1
        assert minor(v) == 2
        assert patch(v) == 3
        assert prerelease(v) == "alpha"
        assert build(v) == "build"
        
        # 字符串版本
        assert major("1.2.3") == 1
        assert minor("1.2.3") == 2
        assert patch("1.2.3") == 3
        print("✅ test_accessors")
    
    def test_unique(self):
        """测试去重"""
        versions = ["1.0.0", "1.0.0", "2.0.0", "1.0.0+build"]
        unique_v = unique(versions)
        # 1.0.0 和 1.0.0+build 相等（构建元数据不参与比较）
        assert len(unique_v) == 2
        print("✅ test_unique")
    
    def test_next_versions(self):
        """测试下一个版本列表"""
        v = SemVer(1, 2, 3)
        next_v = next_versions(v)
        
        versions_str = [str(nv) for nv in next_v]
        assert "1.2.4" in versions_str  # patch
        assert "1.3.0" in versions_str  # minor
        assert "2.0.0" in versions_str  # major
        print("✅ test_next_versions")
    
    def test_next_versions_with_prerelease(self):
        """测试下一个版本列表（包含预发布）"""
        v = SemVer(1, 2, 3)
        next_v = next_versions(v, include_prerelease=True)
        
        versions_str = [str(nv) for nv in next_v]
        assert "1.2.3-alpha.1" in versions_str
        assert "1.2.3-beta.1" in versions_str
        assert "1.2.3-rc.1" in versions_str
        print("✅ test_next_versions_with_prerelease")
    
    def test_constants(self):
        """测试常量"""
        assert str(ZERO) == "0.0.0"
        assert str(ONE) == "1.0.0"
        print("✅ test_constants")


class TestEdgeCases:
    """边界值测试"""
    
    def test_zero_versions(self):
        """测试零版本"""
        v = SemVer(0, 0, 0)
        assert str(v) == "0.0.0"
        assert v.is_stable == False
        print("✅ test_zero_versions")
    
    def test_large_versions(self):
        """测试大版本号"""
        v = SemVer(999, 999, 999)
        assert str(v) == "999.999.999"
        print("✅ test_large_versions")
    
    def test_complex_prerelease(self):
        """测试复杂预发布标识"""
        v = parse("1.0.0-alpha.1.beta.2.build.3")
        assert v.prerelease == "alpha.1.beta.2.build.3"
        print("✅ test_complex_prerelease")
    
    def test_complex_build(self):
        """测试复杂构建元数据"""
        v = parse("1.0.0+exp.sha.5114f85.2024-01-01")
        assert v.build == "exp.sha.5114f85.2024-01-01"
        print("✅ test_complex_build")
    
    def test_prerelease_ordering(self):
        """测试预发布排序顺序"""
        versions = [
            "1.0.0-beta",
            "1.0.0-alpha.beta",
            "1.0.0-alpha",
            "1.0.0-alpha.1",
            "1.0.0-alpha.0",
            "1.0.0-0",
        ]
        sorted_v = sort(versions)
        expected = [
            "1.0.0-0",
            "1.0.0-alpha",
            "1.0.0-alpha.0",
            "1.0.0-alpha.1",
            "1.0.0-alpha.beta",
            "1.0.0-beta",
        ]
        assert [str(v) for v in sorted_v] == expected
        print("✅ test_prerelease_ordering")
    
    def test_hash_consistency(self):
        """测试哈希一致性"""
        v1 = SemVer(1, 0, 0)
        v2 = SemVer(1, 0, 0)
        assert hash(v1) == hash(v2)
        
        # 构建元数据不影响哈希
        v3 = SemVer(1, 0, 0, None, "build.1")
        v4 = SemVer(1, 0, 0, None, "build.2")
        assert hash(v3) == hash(v4)
        print("✅ test_hash_consistency")
    
    def test_repr(self):
        """测试字符串表示"""
        v = SemVer(1, 2, 3)
        assert repr(v) == "SemVer(1.2.3)"
        print("✅ test_repr")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("语义化版本工具测试")
    print("=" * 60)
    
    test_classes = [
        TestSemVer,
        TestParse,
        TestComparison,
        TestSorting,
        TestRange,
        TestDiff,
        TestFormat,
        TestUtilities,
        TestEdgeCases,
    ]
    
    total_tests = 0
    
    for test_class in test_classes:
        print(f"\n{test_class.__name__}:")
        print("-" * 40)
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                method = getattr(instance, method_name)
                method()
                total_tests += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 所有测试通过! 共 {total_tests} 个测试")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()