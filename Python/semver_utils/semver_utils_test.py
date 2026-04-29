"""
语义版本工具测试

测试覆盖:
- 版本解析：各种格式、边界值、错误处理
- 版本比较：>、<、>=、<=、==、!=
- 版本验证：有效/无效格式
- 版本递增：major、minor、patch、prerelease
- 版本范围：^、~、通配符、比较运算符
- 边界值：空值、极值、Unicode、特殊格式
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    SemanticVersion,
    parse,
    is_valid,
    compare,
    gt,
    gte,
    lt,
    lte,
    eq,
    neq,
    increment_major,
    increment_minor,
    increment_patch,
    increment_prerelease,
    major,
    minor,
    patch,
    prerelease,
    build_metadata,
    diff,
    satisfies,
    max_satisfying,
    min_satisfying,
    coerce,
    sort_versions,
    get_change_type,
    create,
    validate,
    next_version,
)


def test_parse():
    """测试版本解析"""
    print("测试 parse...")
    
    # 基本版本
    v = parse("1.2.3")
    assert v.major == 1
    assert v.minor == 2
    assert v.patch == 3
    assert v.prerelease is None
    assert v.build_metadata is None
    
    # 带预发布
    v = parse("1.0.0-alpha")
    assert v.major == 1
    assert v.minor == 0
    assert v.patch == 0
    assert v.prerelease == ["alpha"]
    
    # 带数字预发布
    v = parse("1.0.0-alpha.1")
    assert v.prerelease == ["alpha", 1]
    
    # 带构建元数据
    v = parse("1.0.0+build.123")
    assert v.build_metadata == "build.123"
    
    # 完整格式
    v = parse("1.0.0-alpha.1+build.123")
    assert v.major == 1
    assert v.minor == 0
    assert v.patch == 0
    assert v.prerelease == ["alpha", 1]
    assert v.build_metadata == "build.123"
    
    # 复杂预发布
    v = parse("2.0.0-rc.1.beta.2")
    assert v.prerelease == ["rc", 1, "beta", 2]
    
    # 零版本
    v = parse("0.0.0")
    assert v.major == 0
    assert v.minor == 0
    assert v.patch == 0
    
    # 大版本号
    v = parse("999.888.777")
    assert v.major == 999
    assert v.minor == 888
    assert v.patch == 777
    
    print("  ✓ parse 基本测试通过")


def test_parse_errors():
    """测试解析错误处理"""
    print("测试 parse 错误处理...")
    
    invalid_versions = [
        "",                 # 空字符串
        "1",                # 只有一个版本号
        "1.2",              # 只有两个版本号
        "1.2.3.4",          # 四个版本号
        "v1.2.3",           # 带前缀
        "1.2.3a",           # 无效格式
        "1.2.-3",           # 负号
        "01.2.3",           # 前导零
        "1.02.3",           # 前导零
        "1.2.03",           # 前导零
        "a.b.c",            # 非数字
        "1.2.3-",           # 空预发布
        "1.2.3+",           # 空构建元数据
    ]
    
    for version in invalid_versions:
        try:
            parse(version)
            assert False, f"应该抛出异常: {version}"
        except ValueError:
            pass  # 正确抛出异常
    
    print("  ✓ parse 错误处理测试通过")


def test_is_valid():
    """测试版本验证"""
    print("测试 is_valid...")
    
    # 有效版本
    valid_versions = [
        "1.0.0",
        "0.0.0",
        "10.20.30",
        "1.0.0-alpha",
        "1.0.0-alpha.1",
        "1.0.0-0.3.7",
        "1.0.0-x.7.z.92",
        "1.0.0-alpha+001",
        "1.0.0+20130313144700",
        "1.0.0-beta+exp.sha.5114f85",
    ]
    
    for version in valid_versions:
        assert is_valid(version), f"应该有效: {version}"
    
    # 无效版本
    invalid_versions = [
        "",
        "1",
        "1.2",
        "1.2.3.4",
        "v1.2.3",
        "01.2.3",
        "1.02.3",
        "1.2.03",
    ]
    
    for version in invalid_versions:
        assert not is_valid(version), f"应该无效: {version}"
    
    print("  ✓ is_valid 测试通过")


def test_compare():
    """测试版本比较"""
    print("测试 compare...")
    
    # 基本比较
    assert compare("1.0.0", "2.0.0") == -1
    assert compare("2.0.0", "1.0.0") == 1
    assert compare("1.0.0", "1.0.0") == 0
    
    # 次版本比较
    assert compare("1.0.0", "1.1.0") == -1
    assert compare("1.1.0", "1.0.0") == 1
    
    # 修订版本比较
    assert compare("1.0.0", "1.0.1") == -1
    assert compare("1.0.1", "1.0.0") == 1
    
    # 预发布版本比较
    assert compare("1.0.0-alpha", "1.0.0-beta") == -1
    assert compare("1.0.0-alpha.1", "1.0.0-alpha.2") == -1
    assert compare("1.0.0-alpha", "1.0.0") == -1  # 预发布 < 正式
    
    # 正式版本 > 预发布版本
    assert compare("1.0.0", "1.0.0-alpha") == 1
    assert compare("1.0.0", "1.0.0-beta.2") == 1
    
    # 数字标识符 vs 字符串标识符
    assert compare("1.0.0-1", "1.0.0-alpha") == -1  # 数字 < 字符串
    
    print("  ✓ compare 测试通过")


def test_comparison_operators():
    """测试比较运算符函数"""
    print("测试比较运算符函数...")
    
    # gt
    assert gt("2.0.0", "1.0.0") is True
    assert gt("1.0.0", "2.0.0") is False
    assert gt("1.0.0", "1.0.0") is False
    
    # gte
    assert gte("2.0.0", "1.0.0") is True
    assert gte("1.0.0", "1.0.0") is True
    assert gte("1.0.0", "2.0.0") is False
    
    # lt
    assert lt("1.0.0", "2.0.0") is True
    assert lt("2.0.0", "1.0.0") is False
    assert lt("1.0.0", "1.0.0") is False
    
    # lte
    assert lte("1.0.0", "2.0.0") is True
    assert lte("1.0.0", "1.0.0") is True
    assert lte("2.0.0", "1.0.0") is False
    
    # eq
    assert eq("1.0.0", "1.0.0") is True
    assert eq("1.0.0+build1", "1.0.0+build2") is True  # 构建元数据不影响比较
    assert eq("1.0.0", "2.0.0") is False
    
    # neq
    assert neq("1.0.0", "2.0.0") is True
    assert neq("1.0.0", "1.0.0") is False
    
    print("  ✓ 比较运算符函数测试通过")


def test_increment():
    """测试版本递增"""
    print("测试 increment...")
    
    # increment_major
    assert increment_major("1.2.3") == "2.0.0"
    assert increment_major("0.1.0") == "1.0.0"
    assert increment_major("1.2.3-alpha") == "2.0.0"  # 移除预发布
    
    # increment_minor
    assert increment_minor("1.2.3") == "1.3.0"
    assert increment_minor("0.1.0") == "0.2.0"
    assert increment_minor("1.2.3-alpha") == "1.3.0"  # 移除预发布
    
    # increment_patch
    assert increment_patch("1.2.3") == "1.2.4"
    assert increment_patch("0.0.1") == "0.0.2"
    assert increment_patch("1.2.3-alpha") == "1.2.4"  # 移除预发布并递增 patch
    
    # increment_prerelease
    assert increment_prerelease("1.2.3") == "1.2.4-rc.1"
    assert increment_prerelease("1.2.3-rc.1") == "1.2.3-rc.2"
    assert increment_prerelease("1.2.3-alpha.1") == "1.2.3-alpha.2"
    assert increment_prerelease("1.2.3-alpha") == "1.2.3-alpha.1"
    assert increment_prerelease("1.2.3", "beta") == "1.2.4-beta.1"
    
    print("  ✓ increment 测试通过")


def test_getters():
    """测试版本组件获取"""
    print("测试 getters...")
    
    assert major("1.2.3") == 1
    assert minor("1.2.3") == 2
    assert patch("1.2.3") == 3
    assert prerelease("1.0.0-alpha.1") == ["alpha", 1]
    assert prerelease("1.0.0") is None
    assert build_metadata("1.0.0+build.123") == "build.123"
    assert build_metadata("1.0.0") is None
    
    print("  ✓ getters 测试通过")


def test_diff():
    """测试版本差异检测"""
    print("测试 diff...")
    
    assert diff("1.0.0", "2.0.0") == "major"
    assert diff("1.0.0", "1.1.0") == "minor"
    assert diff("1.0.0", "1.0.1") == "patch"
    assert diff("1.0.0-alpha", "1.0.0-beta") == "prerelease"
    assert diff("1.0.0", "1.0.0") is None
    
    print("  ✓ diff 测试通过")


def test_satisfies():
    """测试版本范围匹配"""
    print("测试 satisfies...")
    
    # 精确匹配
    assert satisfies("1.2.3", "1.2.3") is True
    assert satisfies("1.2.3", "1.2.4") is False
    
    # 比较运算符
    assert satisfies("1.2.3", ">=1.0.0") is True
    assert satisfies("1.2.3", ">=1.2.3") is True
    assert satisfies("1.2.3", ">1.0.0") is True
    assert satisfies("1.2.3", "<2.0.0") is True
    assert satisfies("1.2.3", "<=1.2.3") is True
    
    # 插入号范围 ^
    assert satisfies("1.2.3", "^1.0.0") is True
    assert satisfies("1.2.3", "^1.2.0") is True
    assert satisfies("2.0.0", "^1.0.0") is False
    assert satisfies("0.2.3", "^0.2.0") is True
    assert satisfies("0.3.0", "^0.2.0") is False
    assert satisfies("0.0.3", "^0.0.3") is True
    assert satisfies("0.0.4", "^0.0.3") is False
    
    # 波浪号范围 ~
    assert satisfies("1.2.3", "~1.2.0") is True
    assert satisfies("1.2.5", "~1.2.0") is True
    assert satisfies("1.3.0", "~1.2.0") is False
    
    # 通配符
    assert satisfies("1.2.3", "1.2.*") is True
    assert satisfies("1.3.0", "1.2.*") is False
    assert satisfies("1.2.3", "1.x") is True
    assert satisfies("2.0.0", "1.x") is False
    assert satisfies("1.0.0", "*") is True
    
    # 范围
    assert satisfies("1.5.0", "1.0.0 - 2.0.0") is True
    assert satisfies("3.0.0", "1.0.0 - 2.0.0") is False
    
    # 复合条件
    assert satisfies("1.2.3", ">=1.0.0 <2.0.0") is True
    assert satisfies("2.0.0", ">=1.0.0 <2.0.0") is False
    
    print("  ✓ satisfies 测试通过")


def test_max_min_satisfying():
    """测试最大/最小满足版本"""
    print("测试 max_satisfying / min_satisfying...")
    
    versions = ["1.0.0", "1.2.3", "1.5.0", "2.0.0", "2.1.0"]
    
    # max_satisfying
    assert max_satisfying(versions, "^1.0.0") == "1.5.0"
    assert max_satisfying(versions, "^2.0.0") == "2.1.0"
    assert max_satisfying(versions, ">=3.0.0") is None
    
    # min_satisfying
    assert min_satisfying(versions, ">=1.2.0") == "1.2.3"
    assert min_satisfying(versions, ">=2.0.0") == "2.0.0"
    assert min_satisfying(versions, ">=3.0.0") is None
    
    print("  ✓ max_satisfying / min_satisfying 测试通过")


def test_coerce():
    """测试版本强制转换"""
    print("测试 coerce...")
    
    # 带前缀
    v = coerce("v1.2.3")
    assert v is not None
    assert str(v) == "1.2.3"
    
    v = coerce("version-2.0.0")
    assert v is not None
    assert str(v) == "2.0.0"
    
    # 短版本
    v = coerce("1.2")
    assert v is not None
    assert str(v) == "1.2.0"
    
    v = coerce("1")
    assert v is not None
    assert str(v) == "1.0.0"
    
    # 无效版本
    assert coerce("not-a-version") is None
    assert coerce("") is None
    
    print("  ✓ coerce 测试通过")


def test_sort_versions():
    """测试版本排序"""
    print("测试 sort_versions...")
    
    versions = ["2.0.0", "1.0.0-alpha", "1.0.0", "1.2.3", "1.0.0-beta"]
    
    # 升序
    sorted_asc = sort_versions(versions)
    assert sorted_asc[0] == "1.0.0-alpha"
    assert sorted_asc[-1] == "2.0.0"
    
    # 降序
    sorted_desc = sort_versions(versions, reverse=True)
    assert sorted_desc[0] == "2.0.0"
    assert sorted_desc[-1] == "1.0.0-alpha"
    
    print("  ✓ sort_versions 测试通过")


def test_get_change_type():
    """测试版本变更类型"""
    print("测试 get_change_type...")
    
    assert get_change_type("1.0.0", "2.0.0") == "major"
    assert get_change_type("1.0.0", "1.1.0") == "minor"
    assert get_change_type("1.0.0", "1.0.1") == "patch"
    assert get_change_type("1.0.0-alpha", "1.0.0-beta") == "prerelease"
    assert get_change_type("1.0.0", "1.0.0") == "none"
    assert get_change_type("2.0.0", "1.0.0") == "downgrade"
    
    print("  ✓ get_change_type 测试通过")


def test_create():
    """测试创建版本"""
    print("测试 create...")
    
    v = create(1, 2, 3)
    assert str(v) == "1.2.3"
    
    v = create(1, 0, 0, ["alpha", 1])
    assert str(v) == "1.0.0-alpha.1"
    
    v = create(1, 0, 0, None, "build.123")
    assert str(v) == "1.0.0+build.123"
    
    v = create(1, 0, 0, ["rc", 1], "build.456")
    assert str(v) == "1.0.0-rc.1+build.456"
    
    print("  ✓ create 测试通过")


def test_validate():
    """测试详细验证"""
    print("测试 validate...")
    
    # 有效版本
    valid, err = validate("1.2.3")
    assert valid is True
    assert err is None
    
    # 无效版本
    valid, err = validate("")
    assert valid is False
    assert err is not None
    
    valid, err = validate("1.2")
    assert valid is False
    assert "patch" in err.lower()
    
    valid, err = validate("01.2.3")
    assert valid is False
    assert "leading zero" in err.lower() or "前导零" in err
    
    print("  ✓ validate 测试通过")


def test_next_version():
    """测试下一个版本"""
    print("测试 next_version...")
    
    assert next_version("1.2.3", "major") == "2.0.0"
    assert next_version("1.2.3", "minor") == "1.3.0"
    assert next_version("1.2.3", "patch") == "1.2.4"
    assert next_version("1.2.3", "prerelease") == "1.2.4-rc.1"
    
    # 无效发布类型
    try:
        next_version("1.2.3", "invalid")
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    print("  ✓ next_version 测试通过")


def test_semantic_version_class():
    """测试 SemanticVersion 类"""
    print("测试 SemanticVersion 类...")
    
    v1 = SemanticVersion(1, 2, 3)
    v2 = SemanticVersion(1, 2, 3)
    v3 = SemanticVersion(1, 2, 4)
    
    # 相等性
    assert v1 == v2
    assert v1 != v3
    
    # 比较
    assert v1 < v3
    assert v3 > v1
    assert v1 <= v2
    assert v1 >= v2
    
    # 字符串转换
    assert str(v1) == "1.2.3"
    
    # 元组转换
    assert v1.to_tuple() == (1, 2, 3)
    
    # 预发布检查
    v_alpha = SemanticVersion(1, 0, 0, ["alpha"])
    assert v_alpha.is_prerelease() is True
    assert v_alpha.is_stable() is False
    
    v_stable = SemanticVersion(1, 0, 0)
    assert v_stable.is_prerelease() is False
    assert v_stable.is_stable() is True
    
    v0 = SemanticVersion(0, 1, 0)
    assert v0.is_stable() is False  # major = 0
    
    # 哈希（可用于 set/dict）
    version_set = {v1, v2, v3}
    assert len(version_set) == 2
    
    print("  ✓ SemanticVersion 类测试通过")


def test_prerelease_comparison():
    """测试预发布版本比较规则"""
    print("测试预发布版本比较规则...")
    
    # 正式版本 > 预发布版本
    assert gt("1.0.0", "1.0.0-alpha") is True
    
    # 预发布版本比较
    assert lt("1.0.0-alpha", "1.0.0-beta") is True
    assert lt("1.0.0-alpha.1", "1.0.0-alpha.2") is True
    assert lt("1.0.0-alpha", "1.0.0-alpha.1") is True
    
    # 数字 < 字符串
    assert lt("1.0.0-1", "1.0.0-alpha") is True
    
    # 相同前缀，长度不同
    assert lt("1.0.0-alpha", "1.0.0-alpha.1") is True
    
    print("  ✓ 预发布版本比较测试通过")


def test_edge_cases():
    """测试边界值"""
    print("测试边界值...")
    
    # 零版本
    v = parse("0.0.0")
    assert v.major == 0
    assert v.minor == 0
    assert v.patch == 0
    
    # 大版本号
    v = parse("999999.999999.999999")
    assert v.major == 999999
    assert v.minor == 999999
    assert v.patch == 999999
    
    # 长预发布标识符
    v = parse("1.0.0-abcdefghijklmnopqrstuvwxyz0123456789")
    assert v.prerelease == ["abcdefghijklmnopqrstuvwxyz0123456789"]
    
    # 长构建元数据
    v = parse("1.0.0+" + "a" * 1000)
    assert len(v.build_metadata) == 1000
    
    # 多个预发布标识符
    v = parse("1.0.0-a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p")
    assert len(v.prerelease) == 16
    
    # 排序大量版本
    versions = [f"1.{i}.{j}" for i in range(10) for j in range(10)]
    sorted_versions = sort_versions(versions)
    assert sorted_versions[0] == "1.0.0"
    assert sorted_versions[-1] == "1.9.9"
    
    print("  ✓ 边界值测试通过")


def test_unicode_and_special():
    """测试 Unicode 和特殊字符"""
    print("测试 Unicode 和特殊字符...")
    
    # Unicode 不允许在版本号中
    try:
        parse("1.0.0-αβγ")
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    # 特殊字符（允许的：字母数字和连字符）
    v = parse("1.0.0-alpha-beta")
    assert v.prerelease == ["alpha-beta"]
    
    # 构建元数据中的特殊字符
    v = parse("1.0.0+build-123.test")
    assert v.build_metadata == "build-123.test"
    
    print("  ✓ Unicode 和特殊字符测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("语义版本工具测试")
    print("=" * 60 + "\n")
    
    tests = [
        test_parse,
        test_parse_errors,
        test_is_valid,
        test_compare,
        test_comparison_operators,
        test_increment,
        test_getters,
        test_diff,
        test_satisfies,
        test_max_min_satisfying,
        test_coerce,
        test_sort_versions,
        test_get_change_type,
        test_create,
        test_validate,
        test_next_version,
        test_semantic_version_class,
        test_prerelease_comparison,
        test_edge_cases,
        test_unicode_and_special,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} 异常: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)