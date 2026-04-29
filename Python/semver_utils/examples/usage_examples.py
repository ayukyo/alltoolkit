"""
语义版本工具使用示例

演示如何使用 semver_utils 进行版本号处理
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
    increment_major,
    increment_minor,
    increment_patch,
    increment_prerelease,
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


def example_basic_parsing():
    """基本版本解析示例"""
    print("\n1. 基本版本解析")
    print("-" * 40)
    
    # 解析基本版本
    v = parse("1.2.3")
    print(f"解析 '1.2.3': major={v.major}, minor={v.minor}, patch={v.patch}")
    
    # 解析带预发布的版本
    v = parse("2.0.0-alpha.1")
    print(f"解析 '2.0.0-alpha.1': prerelease={v.prerelease}")
    print(f"是否为预发布版本: {v.is_prerelease()}")
    
    # 解析带构建元数据的版本
    v = parse("1.0.0+20230313144700")
    print(f"解析 '1.0.0+20230313144700': build_metadata={v.build_metadata}")
    
    # 解析完整格式
    v = parse("1.0.0-alpha.1+build.123")
    print(f"解析完整版本: {v}")
    print(f"字符串表示: {str(v)}")


def example_version_comparison():
    """版本比较示例"""
    print("\n2. 版本比较")
    print("-" * 40)
    
    # 使用 compare 函数
    print(f"compare('1.0.0', '2.0.0'): {compare('1.0.0', '2.0.0')} (返回 -1 表示小于)")
    print(f"compare('2.0.0', '1.0.0'): {compare('2.0.0', '1.0.0')} (返回 1 表示大于)")
    print(f"compare('1.0.0', '1.0.0'): {compare('1.0.0', '1.0.0')} (返回 0 表示相等)")
    
    # 使用比较运算符函数
    print(f"\ngt('2.0.0', '1.0.0'): {gt('2.0.0', '1.0.0')}")
    print(f"lt('1.0.0', '2.0.0'): {lt('1.0.0', '2.0.0')}")
    print(f"gte('2.0.0', '2.0.0'): {gte('2.0.0', '2.0.0')}")
    print(f"lte('1.0.0', '1.0.0'): {lte('1.0.0', '1.0.0')}")
    
    # 预发布版本比较
    print("\n预发布版本比较:")
    print(f"正式版本 > 预发布版本: gt('1.0.0', '1.0.0-alpha'): {gt('1.0.0', '1.0.0-alpha')}")
    print(f"alpha < beta: lt('1.0.0-alpha', '1.0.0-beta'): {lt('1.0.0-alpha', '1.0.0-beta')}")


def example_version_increment():
    """版本递增示例"""
    print("\n3. 版本递增")
    print("-" * 40)
    
    version = "1.2.3"
    print(f"当前版本: {version}")
    print(f"递增 major: {increment_major(version)}")
    print(f"递增 minor: {increment_minor(version)}")
    print(f"递增 patch: {increment_patch(version)}")
    print(f"递增 prerelease: {increment_prerelease(version)}")
    
    # 预发布版本递增
    version = "1.0.0-alpha.1"
    print(f"\n预发布版本 {version}")
    print(f"递增 prerelease: {increment_prerelease(version)}")
    print(f"递增 patch (稳定化): {increment_patch(version)}")


def example_version_range():
    """版本范围匹配示例"""
    print("\n4. 版本范围匹配")
    print("-" * 40)
    
    # 插入号范围
    print("插入号范围 (^):")
    print(f"satisfies('1.2.3', '^1.0.0'): {satisfies('1.2.3', '^1.0.0')}")
    print(f"satisfies('2.0.0', '^1.0.0'): {satisfies('2.0.0', '^1.0.0')}")
    print(f"satisfies('0.2.3', '^0.2.0'): {satisfies('0.2.3', '^0.2.0')}")
    print(f"satisfies('0.3.0', '^0.2.0'): {satisfies('0.3.0', '^0.2.0')}")
    
    # 波浪号范围
    print("\n波浪号范围 (~):")
    print(f"satisfies('1.2.5', '~1.2.0'): {satisfies('1.2.5', '~1.2.0')}")
    print(f"satisfies('1.3.0', '~1.2.0'): {satisfies('1.3.0', '~1.2.0')}")
    
    # 比较运算符
    print("\n比较运算符:")
    print(f"satisfies('1.5.0', '>=1.0.0 <2.0.0'): {satisfies('1.5.0', '>=1.0.0 <2.0.0')}")
    print(f"satisfies('2.0.0', '>=1.0.0 <2.0.0'): {satisfies('2.0.0', '>=1.0.0 <2.0.0')}")
    
    # 范围
    print("\n范围匹配:")
    print(f"satisfies('1.5.0', '1.0.0 - 2.0.0'): {satisfies('1.5.0', '1.0.0 - 2.0.0')}")
    
    # 通配符
    print("\n通配符:")
    print(f"satisfies('1.2.5', '1.2.*'): {satisfies('1.2.5', '1.2.*')}")
    print(f"satisfies('1.3.0', '1.2.*'): {satisfies('1.3.0', '1.2.*')}")
    print(f"satisfies('1.5.0', '1.x'): {satisfies('1.5.0', '1.x')}")


def example_find_best_version():
    """查找最佳版本示例"""
    print("\n5. 查找最佳版本")
    print("-" * 40)
    
    versions = ["1.0.0", "1.2.0", "1.2.3", "1.5.0", "2.0.0", "2.1.0"]
    print(f"可用版本: {versions}")
    
    # 查找满足 ^1.0.0 的最大版本
    best = max_satisfying(versions, "^1.0.0")
    print(f"满足 '^1.0.0' 的最大版本: {best}")
    
    # 查找满足 >=1.2.0 的最小版本
    min_v = min_satisfying(versions, ">=1.2.0")
    print(f"满足 '>=1.2.0' 的最小版本: {min_v}")
    
    # 查找满足 ^2.0.0 的版本
    best = max_satisfying(versions, "^2.0.0")
    print(f"满足 '^2.0.0' 的最大版本: {best}")
    
    # 无满足版本
    best = max_satisfying(versions, ">=3.0.0")
    print(f"满足 '>=3.0.0' 的版本: {best} (返回 None)")


def example_version_sorting():
    """版本排序示例"""
    print("\n6. 版本排序")
    print("-" * 40)
    
    versions = ["2.0.0", "1.0.0", "1.2.3", "1.0.0-alpha", "1.0.0-beta", "0.9.0"]
    print(f"原始版本列表: {versions}")
    
    sorted_asc = sort_versions(versions)
    print(f"升序排序: {sorted_asc}")
    
    sorted_desc = sort_versions(versions, reverse=True)
    print(f"降序排序: {sorted_desc}")


def example_version_diff():
    """版本差异检测示例"""
    print("\n7. 版本差异检测")
    print("-" * 40)
    
    pairs = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.1.0"),
        ("1.0.0", "1.0.1"),
        ("1.0.0", "1.0.0"),
        ("1.0.0-alpha", "1.0.0-beta"),
    ]
    
    for v1, v2 in pairs:
        result = diff(v1, v2)
        print(f"diff('{v1}', '{v2}'): {result}")


def example_change_type():
    """版本变更类型示例"""
    print("\n8. 版本变更类型")
    print("-" * 40)
    
    changes = [
        ("1.0.0", "2.0.0", "major"),
        ("1.0.0", "1.1.0", "minor"),
        ("1.0.0", "1.0.1", "patch"),
        ("2.0.0", "1.0.0", "downgrade"),
        ("1.0.0", "1.0.0", "none"),
    ]
    
    for from_v, to_v, expected in changes:
        result = get_change_type(from_v, to_v)
        status = "✓" if result == expected else "✗"
        print(f"{status} get_change_type('{from_v}', '{to_v}'): {result} (期望: {expected})")


def example_coerce():
    """版本强制转换示例"""
    print("\n9. 版本强制转换")
    print("-" * 40)
    
    inputs = [
        "v1.2.3",
        "version-2.0.0",
        "V1.0.0",
        "release-3.0.1",
        "1.2",
        "1",
        "lib-1.2.3",
        "package-v2.1.0-beta",
    ]
    
    for input_str in inputs:
        result = coerce(input_str)
        print(f"coerce('{input_str}'): {result if result else 'None'}")


def example_validation():
    """版本验证示例"""
    print("\n10. 版本验证")
    print("-" * 40)
    
    versions = [
        "1.2.3",      # 有效
        "1.2",        # 无效 - 缺少 patch
        "v1.2.3",     # 无效 - 带前缀
        "01.2.3",     # 无效 - 前导零
        "1.2.3-alpha", # 有效
        "",           # 无效 - 空
    ]
    
    for version in versions:
        valid, err = validate(version)
        status = "✓ 有效" if valid else f"✗ 无效: {err}"
        print(f"validate('{version}'): {status}")


def example_create():
    """创建版本示例"""
    print("\n11. 创建版本")
    print("-" * 40)
    
    # 创建基本版本
    v = create(1, 2, 3)
    print(f"create(1, 2, 3): {v}")
    
    # 创建预发布版本
    v = create(2, 0, 0, ["alpha", 1])
    print(f"create(2, 0, 0, ['alpha', 1]): {v}")
    
    # 创建带构建元数据的版本
    v = create(1, 0, 0, None, "build.123")
    print(f"create(1, 0, 0, None, 'build.123'): {v}")
    
    # 创建完整版本
    v = create(3, 1, 2, ["rc", 1], "exp.sha.5114f85")
    print(f"完整版本: {v}")


def example_next_version():
    """下一个版本示例"""
    print("\n12. 下一个版本")
    print("-" * 40)
    
    version = "1.2.3"
    print(f"当前版本: {version}")
    print(f"下一 major: {next_version(version, 'major')}")
    print(f"下一 minor: {next_version(version, 'minor')}")
    print(f"下一 patch: {next_version(version, 'patch')}")
    print(f"下一 prerelease: {next_version(version, 'prerelease')}")


def example_package_version_handling():
    """包版本处理场景示例"""
    print("\n13. 实际场景：包版本处理")
    print("-" * 40)
    
    # 模拟依赖版本选择
    available_versions = [
        "0.9.0",
        "1.0.0-alpha",
        "1.0.0-beta",
        "1.0.0",
        "1.1.0",
        "1.2.0",
        "1.2.3",
        "1.3.0",
        "2.0.0-rc.1",
        "2.0.0",
    ]
    
    requirement = "^1.0.0"
    print(f"依赖需求: {requirement}")
    print(f"可用版本: {available_versions}")
    
    best = max_satisfying(available_versions, requirement)
    print(f"最佳选择: {best}")
    
    # 检查是否需要升级
    current = "1.1.0"
    if best:
        change = get_change_type(current, best)
        print(f"从 {current} 升级到 {best}: {change}变更")
    
    # 发布新版本流程
    print("\n发布流程示例:")
    dev_version = "1.2.4-alpha.1"
    print(f"开发版本: {dev_version}")
    print(f"测试版本: {increment_prerelease(dev_version, 'beta')}")
    print(f"候选版本: {increment_prerelease(dev_version, 'rc')}")
    print(f"正式版本: {increment_patch(dev_version)}")


def run_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("语义版本工具使用示例")
    print("=" * 60)
    
    examples = [
        example_basic_parsing,
        example_version_comparison,
        example_version_increment,
        example_version_range,
        example_find_best_version,
        example_version_sorting,
        example_version_diff,
        example_change_type,
        example_coerce,
        example_validation,
        example_create,
        example_next_version,
        example_package_version_handling,
    ]
    
    for example in examples:
        example()
    
    print("\n" + "=" * 60)
    print("示例完成")
    print("=" * 60)


if __name__ == "__main__":
    run_examples()