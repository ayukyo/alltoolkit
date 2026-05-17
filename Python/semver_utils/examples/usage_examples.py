"""
语义化版本工具使用示例

展示 semver_utils 的主要功能：
- 版本解析与验证
- 版本比较
- 版本递增
- 版本范围匹配
- 版本排序
- 版本差异分析
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    SemVer, parse, is_valid, try_parse,
    compare, equals, greater_than, less_than, gte, lte,
    sort, rsort, min_version, max_version,
    parse_range, satisfies, filter_versions, find_best_match,
    diff, format, to_tuple, from_tuple,
    unique, next_versions, VersionRange
)


def print_section(title):
    """打印分隔线"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print("=" * 60)


def main():
    print_section("语义化版本工具示例")
    
    # ============================================
    # 1. 版本解析与验证
    # ============================================
    print_section("1. 版本解析与验证")
    
    # 解析基本版本
    v1 = parse("1.2.3")
    print(f"解析 '1.2.3': {v1}")
    print(f"  major: {v1.major}, minor: {v1.minor}, patch: {v1.patch}")
    
    # 解析预发布版本
    v2 = parse("2.0.0-alpha.1")
    print(f"\n解析 '2.0.0-alpha.1': {v2}")
    print(f"  是否预发布: {v2.is_prerelease}")
    print(f"  是否稳定: {v2.is_stable}")
    
    # 解析完整版本
    v3 = parse("3.0.0-beta.2+exp.sha.5114f85")
    print(f"\n解析完整版本: {v3}")
    print(f"  版本号: {v3.major}.{v3.minor}.{v3.patch}")
    print(f"  预发布: {v3.prerelease}")
    print(f"  构建: {v3.build}")
    
    # 验证版本
    print(f"\n验证版本:")
    print(f"  '1.0.0' 有效: {is_valid('1.0.0')}")
    print(f"  'invalid' 有效: {is_valid('invalid')}")
    
    # 安全解析
    result = try_parse("2.0.0")
    print(f"\n安全解析 '2.0.0': {result}")
    result = try_parse("invalid")
    print(f"安全解析 'invalid': {result}")
    
    # ============================================
    # 2. 版本比较
    # ============================================
    print_section("2. 版本比较")
    
    versions = ["1.0.0", "1.0.1", "1.1.0", "2.0.0"]
    v_a = SemVer(1, 0, 0)
    v_b = SemVer(2, 0, 0)
    
    print(f"比较 {v_a} 和 {v_b}:")
    print(f"  v_a < v_b: {v_a < v_b}")
    print(f"  v_a == v_b: {v_a == v_b}")
    print(f"  v_a > v_b: {v_a > v_b}")
    
    print(f"\n比较函数:")
    print(f"  compare('1.0.0', '2.0.0'): {compare('1.0.0', '2.0.0')}")
    print(f"  equals('1.0.0', '1.0.0'): {equals('1.0.0', '1.0.0')}")
    print(f"  greater_than('2.0.0', '1.0.0'): {greater_than('2.0.0', '1.0.0')}")
    print(f"  less_than('1.0.0', '2.0.0'): {less_than('1.0.0', '2.0.0')}")
    print(f"  gte('1.0.0', '1.0.0'): {gte('1.0.0', '1.0.0')}")
    print(f"  lte('1.0.0', '2.0.0'): {lte('1.0.0', '2.0.0')}")
    
    # 预发布版本比较
    print(f"\n预发布版本比较:")
    v_pre = SemVer(1, 0, 0, "alpha")
    v_release = SemVer(1, 0, 0)
    print(f"  {v_pre} < {v_release}: {v_pre < v_release}")
    
    # ============================================
    # 3. 版本递增
    # ============================================
    print_section("3. 版本递增")
    
    v = SemVer(1, 2, 3, "alpha.1")
    print(f"当前版本: {v}")
    print(f"递增主版本: {v.bump_major()}")
    print(f"递增次版本: {v.bump_minor()}")
    print(f"递增修订版本: {v.bump_patch()}")
    print(f"递增预发布(alpha): {v.bump_prerelease('alpha')}")
    print(f"递增预发布(beta): {v.bump_prerelease('beta')}")
    
    # 保留预发布标识的递增
    v2 = SemVer(1, 0, 0, "rc.1")
    print(f"\n当前版本: {v2}")
    print(f"递增主版本(保留预发布): {v2.bump_major(reset_prerelease=False)}")
    
    # 移除预发布标识
    print(f"\n发布正式版本: {v.release()}")
    
    # ============================================
    # 4. 版本排序
    # ============================================
    print_section("4. 版本排序")
    
    versions = ["2.0.0", "1.0.0", "1.1.0", "1.0.1", "1.0.0-alpha", "1.0.0-beta"]
    print(f"原始列表: {versions}")
    
    sorted_v = sort(versions)
    print(f"升序排序: {[str(v) for v in sorted_v]}")
    
    rsorted_v = rsort(versions)
    print(f"降序排序: {[str(v) for v in rsorted_v]}")
    
    print(f"\n最小版本: {min_version(versions)}")
    print(f"最大版本: {max_version(versions)}")
    
    # ============================================
    # 5. 版本范围匹配
    # ============================================
    print_section("5. 版本范围匹配")
    
    # 各种范围语法
    ranges = [
        ("*", "所有版本"),
        ("1.2.3", "精确版本"),
        (">=1.0.0", "大于等于"),
        (">1.0.0", "大于"),
        ("<=2.0.0", "小于等于"),
        ("<2.0.0", "小于"),
        (">=1.0.0 <2.0.0", "范围"),
        ("^1.2.3", "插入符(兼容)"),
        ("~1.2.3", "波浪号(补丁)"),
        ("~1.2", "波浪号(次版本)"),
        ("1.2.x", "通配符"),
    ]
    
    print("范围语法示例:")
    for range_str, desc in ranges:
        r = parse_range(range_str)
        print(f"  {range_str:20s} ({desc}): {r}")
    
    # 检查版本是否满足约束
    print(f"\n检查版本是否满足约束:")
    print(f"  '1.2.3' 满足 '^1.0.0': {satisfies('1.2.3', '^1.0.0')}")
    print(f"  '2.0.0' 满足 '^1.0.0': {satisfies('2.0.0', '^1.0.0')}")
    print(f"  '1.2.5' 满足 '~1.2.0': {satisfies('1.2.5', '~1.2.0')}")
    print(f"  '1.3.0' 满足 '~1.2.0': {satisfies('1.3.0', '~1.2.0')}")
    
    # 过滤版本列表
    versions = ["1.0.0", "1.1.0", "1.2.0", "2.0.0", "2.1.0", "3.0.0"]
    print(f"\n版本列表: {versions}")
    filtered = filter_versions(versions, ">=1.0.0 <2.0.0")
    print(f"满足 '>=1.0.0 <2.0.0': {[str(v) for v in filtered]}")
    
    # 查找最佳匹配
    versions = ["1.0.0", "1.1.0", "1.2.0", "1.3.0-alpha", "2.0.0"]
    print(f"\n版本列表: {versions}")
    best = find_best_match(versions, "^1.0.0")
    print(f"'^1.0.0' 最佳匹配: {best}")
    
    # ============================================
    # 6. 版本差异分析
    # ============================================
    print_section("6. 版本差异分析")
    
    diffs = [
        ("1.0.0", "1.0.1"),
        ("1.0.0", "1.1.0"),
        ("1.0.0", "2.0.0"),
        ("2.0.0", "1.0.0"),
        ("1.0.0-alpha", "1.0.0-beta"),
        ("1.0.0", "1.0.0+build"),
    ]
    
    print("版本差异:")
    for v1, v2 in diffs:
        d = diff(v1, v2)
        print(f"  {v1} → {v2}: {d}")
        if d.is_upgrade:
            print(f"    ↗ 升级")
        elif d.is_downgrade:
            print(f"    ↘ 降级")
        if d.is_major_change:
            print(f"    ⚠️  主版本变更")
    
    # ============================================
    # 7. 实用工具函数
    # ============================================
    print_section("7. 实用工具函数")
    
    # 访问器
    v = parse("2.1.3-alpha+build.123")
    print(f"版本: {v}")
    print(f"  主版本: {v.major}")
    print(f"  次版本: {v.minor}")
    print(f"  修订: {v.patch}")
    print(f"  预发布: {v.prerelease}")
    print(f"  构建: {v.build}")
    
    # 元组转换
    t = to_tuple("1.2.3")
    print(f"\n元组: {t}")
    v = from_tuple((2, 0, 0), "beta", "123")
    print(f"从元组创建: {v}")
    
    # 格式化
    v = SemVer(1, 2, 3, "alpha.1", "build.123")
    print(f"\n完整版本: {format(v)}")
    print(f"不含预发布: {format(v, include_prerelease=False)}")
    print(f"不含构建: {format(v, include_build=False)}")
    print(f"仅版本号: {format(v, include_prerelease=False, include_build=False)}")
    
    # 下一个版本
    v = SemVer(1, 2, 3)
    print(f"\n当前版本: {v}")
    print(f"可能的下一个版本:")
    for nv in next_versions(v):
        print(f"  - {nv}")
    
    # 包含预发布版本
    print(f"\n包含预发布版本:")
    for nv in next_versions(v, include_prerelease=True):
        print(f"  - {nv}")
    
    # 去重
    versions = ["1.0.0", "1.0.0", "1.0.0+build", "2.0.0"]
    print(f"\n原始: {versions}")
    print(f"去重: {[str(v) for v in unique(versions)]}")
    
    # ============================================
    # 8. 实际应用场景
    # ============================================
    print_section("8. 实际应用场景")
    
    # 场景1: 依赖版本检查
    print("场景1: 依赖版本检查")
    dependencies = {
        "react": "18.2.0",
        "vue": "3.2.0",
        "angular": "15.0.0",
    }
    constraints = {
        "react": "^18.0.0",
        "vue": "^3.0.0",
        "angular": ">=14.0.0 <16.0.0",
    }
    
    print(f"\n检查依赖版本:")
    for pkg, version in dependencies.items():
        constraint = constraints[pkg]
        ok = satisfies(version, constraint)
        status = "✅" if ok else "❌"
        print(f"  {pkg}: {version} 满足 '{constraint}': {status}")
    
    # 场景2: 版本发布建议
    print(f"\n场景2: 版本发布建议")
    current = parse("1.2.3")
    print(f"当前版本: {current}")
    print(f"建议发布版本:")
    print(f"  - 修复 bug: {current.bump_patch()}")
    print(f"  - 新功能: {current.bump_minor()}")
    print(f"  - 破坏性变更: {current.bump_major()}")
    print(f"  - 预发布 alpha: {current.bump_prerelease('alpha')}")
    print(f"  - 预发布 beta: {current.bump_prerelease('beta')}")
    print(f"  - 预发布 rc: {current.bump_prerelease('rc')}")
    
    # 场景3: 查找兼容版本
    print(f"\n场景3: 查找兼容版本")
    available = ["1.0.0", "1.1.0", "1.2.0", "2.0.0", "2.1.0", "3.0.0-beta"]
    print(f"可用版本: {available}")
    print(f"兼容 '^1.0.0':")
    compatible = filter_versions(available, "^1.0.0")
    for v in compatible:
        print(f"  - {v}")
    
    # 场景4: 版本升级分析
    print(f"\n场景4: 版本升级分析")
    old = "1.2.3"
    new = "2.0.0"
    d = diff(old, new)
    print(f"从 {old} 升级到 {new}:")
    if d.is_major_change:
        print(f"  ⚠️  主版本升级，可能包含破坏性变更！")
    elif d.is_minor_change:
        print(f"  ✅ 次版本升级，新增功能，向后兼容")
    elif d.is_patch_change:
        print(f"  ✅ 补丁更新，bug 修复")
    
    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()