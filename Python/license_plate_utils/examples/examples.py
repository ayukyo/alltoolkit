#!/usr/bin/env python3
"""
AllToolkit - Python License Plate Utilities Examples

使用示例演示
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    validate, parse, validate_format,
    generate, generate_batch, generate_nice_number,
    get_province, get_province_short, get_city_code, get_number, get_type,
    is_special, is_police, is_learner, is_embassy, is_temporary, is_electric,
    compare, match_pattern,
    analyze_batch,
    format_plate, format_with_province,
    list_provinces, list_special_types,
    LicensePlateSet
)

print("=" * 60)
print("Python License Plate Utilities - 使用示例")
print("=" * 60)
print()

# ============================================================
# 基本验证
# ============================================================
print("📦 基本验证")
print("-" * 40)

test_plates = [
    "京A12345",
    "粤B12345",
    "沪C12345",
    "京A12345警",
    "粤AD1234",      # 新能源纯电
    "粤AF1234",      # 新能源插混
    "京I12345",      # 无效（含I）
    "12345",         # 无效（无省份）
]

for plate in test_plates:
    valid = validate(plate)
    status = "✅ 有效" if valid else "❌ 无效"
    print(f"{plate}: {status}")

print()

# ============================================================
# 详细解析
# ============================================================
print("📋 详细解析")
print("-" * 40)

plates_to_parse = ["京A12345", "粤B12345警", "粤AD1234", "鲁C12345学"]

for plate in plates_to_parse:
    info = parse(plate)
    if info:
        print(f"车牌: {info.full_plate}")
        print(f"  省份: {info.province_name} ({info.province})")
        print(f"  城市: {info.city_code}")
        print(f"  号码: {info.number}")
        print(f"  类型: {info.get_type_description()}")
        print(f"  特殊: {info.is_special()}")
    else:
        print(f"{plate}: 无效车牌")
    print()

# ============================================================
# 车牌生成
# ============================================================
print("🚗 车牌生成")
print("-" * 40)

# 随机生成
print("随机生成:")
for _ in range(5):
    print(f"  {generate()}")

print()

# 指定省份
print("指定省份生成 (北京):")
for _ in range(3):
    print(f"  {generate(province='京')}")

print()

# 特殊类型
print("特殊车牌生成:")
print(f"  警车: {generate(province='京', special_type='警')}")
print(f"  教练车: {generate(province='鲁', special_type='学')}")
print(f"  临时车: {generate(province='沪', special_type='临')}")

print()

# 批量生成
print("批量生成 (10个上海车牌):")
shanghai_plates = generate_batch(10, province='沪')
for plate in shanghai_plates:
    print(f"  {plate}")

print()

# ============================================================
# 靓号生成
# ============================================================
print("✨ 靓号生成")
print("-" * 40)

print("连号:")
print(f"  {generate_nice_number(pattern='sequential')}")

print("重复号:")
print(f"  {generate_nice_number(pattern='repeat')}")

print("回文号:")
print(f"  {generate_nice_number(pattern='palindrome')}")

print("混合重复:")
print(f"  {generate_nice_number(pattern='mixed_repeat')}")

print()

# ============================================================
# 类型判断
# ============================================================
print("🏷️ 类型判断")
print("-" * 40)

type_test_plates = [
    ("京A12345警", "警车"),
    ("鲁B12345学", "教练车"),
    ("京A12345使", "使馆车"),
    ("沪A12345临", "临时车"),
    ("粤AD1234", "纯电动车"),
    ("粤AF1234", "插电混动"),
    ("京A12345电", "电动车"),
]

for plate, desc in type_test_plates:
    if desc == "警车":
        result = is_police(plate)
    elif desc == "教练车":
        result = is_learner(plate)
    elif desc == "使馆车":
        result = is_embassy(plate)
    elif desc == "临时车":
        result = is_temporary(plate)
    elif desc in ("纯电动车", "插电混动", "电动车"):
        result = is_electric(plate)
    
    print(f"{plate} ({desc}): {result}")

print()

# ============================================================
# 信息获取
# ============================================================
print("📖 信息获取")
print("-" * 40)

info_plate = "粤B12345"
print(f"车牌: {info_plate}")
print(f"  省份名称: {get_province(info_plate)}")
print(f"  省份简称: {get_province_short(info_plate)}")
print(f"  城市代码: {get_city_code(info_plate)}")
print(f"  号码: {get_number(info_plate)}")
print(f"  类型: {get_type(info_plate)}")

print()

# ============================================================
# 模式匹配
# ============================================================
print("🎯 模式匹配")
print("-" * 40)

patterns = [
    ("京A12345", "[京津沪]A*", "京津沪开头"),
    ("京A12345警", "*警", "警车"),
    ("京A88888", "京A?????", "5位号码"),
    ("粤AD1234", "粤D*", "粤D开头"),
]

for plate, pattern, desc in patterns:
    result = match_pattern(plate, pattern)
    print(f"{plate} 匹配 {pattern} ({desc}): {result}")

print()

# ============================================================
# 格式化输出
# ============================================================
print("✏️ 格式化输出")
print("-" * 40)

format_test = "京A12345"
print(f"原车牌: {format_test}")
print(f"空格分隔: {format_plate(format_test, separator=' ')}")
print(f"点号分隔: {format_plate(format_test, separator='·')}")
print(f"带省份: {format_with_province(format_test)}")

print()

# ============================================================
# 批量分析
# ============================================================
print("📊 批量分析")
print("-" * 40)

batch_plates = [
    "京A12345",
    "京B12345",
    "粤A12345",
    "沪A12345",
    "京A12345警",
    "无效车牌",
]

result = analyze_batch(batch_plates)
print(f"总数: {result['total']}")
print(f"有效: {result['valid']}")
print(f"无效: {result['invalid']}")
print(f"有效率: {result['valid_rate']:.2%}")
print(f"省份分布: {result['province_distribution']}")
print(f"特殊类型分布: {result['special_type_distribution']}")

print()

# ============================================================
# 车牌集合管理
# ============================================================
print("📚 车牌集合管理")
print("-" * 40)

# 创建集合
plate_set = LicensePlateSet()

# 添加车牌
plate_set.add("京A12345")
plate_set.add("京B12345")
plate_set.add("粤A12345")
plate_set.add("京A12345警")

print(f"集合大小: {plate_set.count()}")
print(f"所有车牌: {plate_set.list_all()}")

# 筛选
print(f"北京车牌: {plate_set.filter_by_province('京')}")
print(f"警车: {plate_set.filter_by_special_type('警')}")

# 包含检查
print(f"包含京A12345: {plate_set.contains('京A12345')}")
print(f"包含沪A12345: {'沪A12345' in plate_set}")

print()

# ============================================================
# 比较车牌
# ============================================================
print("⚖️ 比较车牌")
print("-" * 40)

compare_cases = [
    ("京A12345", "京A12345"),
    ("京A12345", "京A12346"),
    ("京A12345", "京A12345 "),  # 含空格
    ("京a12345", "京A12345"),   # 小写
]

for p1, p2 in compare_cases:
    result, msg = compare(p1, p2)
    print(f"{p1} vs {p2}: {result} ({msg})")

print()

# ============================================================
# 辅助信息
# ============================================================
print("🔧 辅助信息")
print("-" * 40)

print(f"所有省份简称: {list_provinces()}")
print(f"特殊车牌类型: {list_special_types()}")

print()

print("=" * 60)
print("示例演示完成！")
print("=" * 60)