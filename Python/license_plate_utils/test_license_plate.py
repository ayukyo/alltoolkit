"""
AllToolkit - Python License Plate Utilities Tests

全面测试车牌工具模块功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    validate, parse, validate_format,
    generate, generate_batch, generate_nice_number,
    get_province, get_province_short, get_city_code, get_number, get_type,
    is_special, is_police, is_learner, is_embassy, is_temporary, is_electric,
    encode_number, decode_number,
    compare, match_pattern,
    analyze_batch,
    format_plate, format_with_province,
    list_provinces, list_province_names, list_special_types,
    is_valid_char, get_char_type,
    LicensePlate, LicensePlateSet,
    PROVINCES, PROVINCE_MAP, VALID_LETTERS, SPECIAL_TYPES
)

# ============================================================================
# 测试框架
# ============================================================================

tests_passed = 0
tests_failed = 0

def test(name: str, condition: bool):
    global tests_passed, tests_failed
    if condition:
        print(f"✅ {name}")
        tests_passed += 1
    else:
        print(f"❌ {name}")
        tests_failed += 1

def test_equal(name: str, expected, actual):
    global tests_passed, tests_failed
    if expected == actual:
        print(f"✅ {name}: {expected} == {actual}")
        tests_passed += 1
    else:
        print(f"❌ {name}: expected {expected}, got {actual}")
        tests_failed += 1

# ============================================================================
# 测试开始
# ============================================================================

print("=" * 60)
print("Python License Plate Utilities Tests")
print("=" * 60)
print()

# MARK: - 常量测试
print("📦 常量测试")
print("-" * 40)

test("PROVINCES 数量", len(PROVINCES) == 34)
test("PROVINCE_MAP 数量", len(PROVINCE_MAP) == 34)
test("VALID_LETTERS 不含 I", 'I' not in VALID_LETTERS)
test("VALID_LETTERS 不含 O", 'O' not in VALID_LETTERS)
test("SPECIAL_TYPES 存在", len(SPECIAL_TYPES) > 0)

print()

# MARK: - 验证测试
print("🔍 验证测试")
print("-" * 40)

test("京A12345 有效", validate("京A12345"))
test("粤B12345 有效", validate("粤B12345"))
test("沪C·12345 有效", validate("沪C12345"))
test("京A12345警 有效", validate("京A12345警"))
test("鲁B12345学 有效", validate("鲁B12345学"))

test("京I12345 无效(I)", not validate("京I12345"))
test("京O12345 无效(O)", not validate("京O12345"))
test("1A12345 无效", not validate("1A12345"))
test("空字符串 无效", not validate(""))
test("None 无效", not validate(None))
test("短车牌 无效", not validate("京A"))
test("包含无效字符 无效", not validate("京A12I45"))

print()

# MARK: - 解析测试
print("📋 解析测试")
print("-" * 40)

info = parse("京A12345")
test_equal("parse 省份简称", "京", info.province)
test_equal("parse 省份名称", "北京市", info.province_name)
test_equal("parse 城市代码", "A", info.city_code)
test_equal("parse 号码", "12345", info.number)
test_equal("parse 特殊类型", None, info.special_type)
test_equal("parse 完整车牌", "京A12345", info.full_plate)

info_special = parse("粤B12345警")
test_equal("parse 警车牌特殊类型", "警", info_special.special_type)
test("parse 警车牌 is_special()", info_special.is_special())
test_equal("parse 警车牌类型描述", "警用车辆", info_special.get_type_description())

print()

# MARK: - validate_format 测试
print("📝 validate_format 测试")
print("-" * 40)

result = validate_format("京A12345")
test_equal("validate_format 有效车牌", (True, "车牌格式有效"), result)

result = validate_format("京I12345")
test("validate_format 无效省份", result[0] == False and "无效" in result[1])

result = validate_format("")
test_equal("validate_format 空车牌", (False, "车牌号为空"), result)

print()

# MARK: - 生成测试
print("🚗 生成测试")
print("-" * 40)

plate = generate()
test("generate 默认生成有效", validate(plate))
test("generate 默认长度为7或8", len(plate) in (7, 8))

plate_jing = generate(province="京")
test("generate 指定省份京", plate_jing.startswith("京"))

plate_a = generate(province="粤", city_code="A")
test("generate 指定粤A", plate_a.startswith("粤A"))

plate_jingcha = generate(province="京", special_type="警")
test("generate 警用车牌有效", validate(plate_jingcha))
test("generate 警用车牌含警", plate_jingcha.endswith("警"))

batch = generate_batch(10)
test_equal("generate_batch 数量", 10, len(batch))
test("generate_batch 全部有效", all(validate(p) for p in batch))

print()

# MARK: - 靓号生成测试
print("✨ 靓号生成测试")
print("-" * 40)

nice_seq = generate_nice_number(pattern='sequential')
test("generate_nice_number 连号有效", validate(nice_seq))

nice_repeat = generate_nice_number(pattern='repeat')
test("generate_nice_number 重复号有效", validate(nice_repeat))

nice_palindrome = generate_nice_number(pattern='palindrome')
test("generate_nice_number 回文号有效", validate(nice_palindrome))

print()

# MARK: - 获取信息测试
print("📖 获取信息测试")
print("-" * 40)

test_equal("get_province", "广东省", get_province("粤A12345"))
test_equal("get_province_short", "粤", get_province_short("粤A12345"))
test_equal("get_city_code", "A", get_city_code("粤A12345"))
test_equal("get_number", "12345", get_number("粤A12345"))
test_equal("get_type", "普通车牌", get_type("粤A12345"))
test_equal("get_type 警用", "警用车辆", get_type("京A12345警"))

print()

# MARK: - 类型判断测试
print("🏷️ 类型判断测试")
print("-" * 40)

test("is_special 警车", is_special("京A12345警"))
test("!is_special 普通车", not is_special("京A12345"))

test("is_police", is_police("京A12345警"))
test("!is_police 普通车", not is_police("京A12345"))

test("is_learner", is_learner("鲁B12345学"))
test("!is_learner 普通车", not is_learner("鲁B12345"))

test("is_embassy 使车", is_embassy("京A12345使"))
test("is_embassy 领车", is_embassy("沪A12345领"))
test("!is_embassy 普通车", not is_embassy("京A12345"))

test("is_temporary", is_temporary("京A12345临"))
test("!is_temporary 普通车", not is_temporary("京A12345"))

test("is_electric 电车", is_electric("京A12345电"))
test("is_electric D牌", is_electric("粤AD1234"))
test("is_electric F牌", is_electric("粤AF1234"))
test("!is_electric 普通车", not is_electric("京A12345"))

print()

# MARK: - 编码测试
print("🔢 编码测试")
print("-" * 40)

code = encode_number("京A12345")
test("encode_number 返回数值", isinstance(code, int))

decoded = decode_number(code)
test_equal("decode_number 还原", "12345", decoded)

code_letters = encode_number("京AAB123")
test("encode_number 含字母有效", code_letters is not None)

# 测试无效车牌
test_equal("encode_number 无效车牌", None, encode_number("无效车牌"))

print()

# MARK: - 比较测试
print("⚖️ 比较测试")
print("-" * 40)

result = compare("京A12345", "京A12345")
test_equal("compare 相同车牌", (True, "完全相同"), result)

result = compare("京A12345", "京A12346")
test("compare 不同车牌", result[0] == False)

result = compare("京A12345", "京A12345 ")
test("compare 忽略空格", result[0] == True)

result = compare("京a12345", "京A12345")
test("compare 忽略大小写", result[0] == True)

print()

# MARK: - 模式匹配测试
print("🎯 模式匹配测试")
print("-" * 40)

test("!match_pattern 京?", not match_pattern("京A12345", "京?"))  # 京?只匹配京+单字符
test("match_pattern 京A*", match_pattern("京A12345", "京A*"))
test("match_pattern 京A?????", match_pattern("京A12345", "京A?????"))
test("match_pattern [京津沪]A*", match_pattern("京A12345", "[京津沪]A*"))  # 以京津沪开头+A+任意
test("!match_pattern 不匹配", not match_pattern("粤A12345", "京A*"))

print()

# MARK: - 批量分析测试
print("📊 批量分析测试")
print("-" * 40)

plates = ["京A12345", "粤B12345", "沪C12345", "京A12345警", "无效车牌"]
result = analyze_batch(plates)

test_equal("analyze_batch 总数", 5, result['total'])
test_equal("analyze_batch 有效数", 4, result['valid'])
test_equal("analyze_batch 无效数", 1, result['invalid'])
test("analyze_batch 有效率", result['valid_rate'] == 0.8)
test("analyze_batch 省份分布", '京' in result['province_distribution'])

print()

# MARK: - 格式化测试
print("✏️ 格式化测试")
print("-" * 40)

test_equal("format_plate 无分隔符", "京A12345", format_plate("京A12345"))
test_equal("format_plate 空格分隔", "京 A 12345", format_plate("京A12345", separator=" "))
test_equal("format_with_province", "京A12345 (北京市)", format_with_province("京A12345"))
test_equal("format_with_province 无效", "无效车牌 (无效)", format_with_province("无效车牌"))

print()

# MARK: - 辅助函数测试
print("🔧 辅助函数测试")
print("-" * 40)

test("list_provinces 非空", len(list_provinces()) > 0)
test("list_province_names 非空", len(list_province_names()) > 0)
test("list_special_types 非空", len(list_special_types()) > 0)

test("is_valid_char A", is_valid_char('A'))
test("is_valid_char 5", is_valid_char('5'))
test("!is_valid_char I", not is_valid_char('I'))
test("!is_valid_char O", not is_valid_char('O'))

test_equal("get_char_type 数字", "digit", get_char_type('5'))
test_equal("get_char_type 字母", "letter", get_char_type('A'))
test_equal("get_char_type 无效", "invalid", get_char_type('I'))

print()

# MARK: - LicensePlate 类测试
print("🏛️ LicensePlate 类测试")
print("-" * 40)

plate_obj = LicensePlate(
    province="粤",
    province_name="广东省",
    city_code="A",
    number="12345"
)
test_equal("LicensePlate full_plate", "粤A12345", plate_obj.full_plate)
test_equal("LicensePlate str", "粤A12345", str(plate_obj))
test("!LicensePlate is_special", not plate_obj.is_special())
test_equal("LicensePlate get_type_description", "普通车牌", plate_obj.get_type_description())

print()

# MARK: - LicensePlateSet 类测试
print("📚 LicensePlateSet 类测试")
print("-" * 40)

plate_set = LicensePlateSet()
test("LicensePlateSet 初始为空", plate_set.count() == 0)

plate_set.add("京A12345")
plate_set.add("粤B12345")
test_equal("LicensePlateSet 添加后数量", 2, plate_set.count())

test("LicensePlateSet contains", plate_set.contains("京A12345"))
test("!LicensePlateSet contains 不存在", not plate_set.contains("沪C12345"))

test("LicensePlateSet remove", plate_set.remove("京A12345"))
test_equal("LicensePlateSet remove后数量", 1, plate_set.count())

plate_set.add("京A12345警")
result = plate_set.filter_by_special_type("警")
test_equal("LicensePlateSet filter_by_special_type", ["京A12345警"], result)

plate_set.add("京B12345")
result = plate_set.filter_by_province("京")
test_equal("LicensePlateSet filter_by_province 数量", 2, len(result))

test("LicensePlateSet __len__", len(plate_set) == plate_set.count())
test("LicensePlateSet __contains__", "粤B12345" in plate_set)

analysis = plate_set.analyze()
test("LicensePlateSet analyze", 'total' in analysis)

plate_set.clear()
test("LicensePlateSet clear", plate_set.count() == 0)

print()

# MARK: - 边界值测试
print("🧪 边界值测试")
print("-" * 40)

# 空输入
test_equal("parse 空", None, parse(""))
test_equal("validate 空", False, validate(""))
test_equal("get_province 空", None, get_province(""))
test_equal("encode_number 空", None, encode_number(""))

# 最短车牌
test("!validate 最短", not validate("京A"))

# 最长车牌（8位含特殊类型）
test("validate 最长8位", validate("京A12345警"))

# 各省份测试
all_valid = True
for province in PROVINCES:
    plate = f"{province}A12345"
    if not validate(plate):
        all_valid = False
        print(f"省份 {province} 测试失败")
test("所有省份简称有效", all_valid)

# 所有字母测试
all_letters_valid = True
for letter in VALID_LETTERS:
    plate = f"京{letter}12345"
    if not validate(plate):
        all_letters_valid = False
        print(f"字母 {letter} 测试失败")
test("所有有效字母可用", all_letters_valid)

print()

# MARK: - 特殊字符测试
print("🔤 特殊字符测试")
print("-" * 40)

# 大小写混合
test("validate 大小写混合", validate("京a12345"))

# 包含空格
test("validate 包含空格", validate(" 京 A 12345 "))
test("validate 包含中空格", validate("京A 12345"))

# 包含点号分隔符
test("validate 包含点号", validate("京A·12345"))

print()

# ============================================================================
# 测试结果
# ============================================================================

print("=" * 60)
print(f"测试结果: ✅ {tests_passed} 通过, ❌ {tests_failed} 失败")
print("=" * 60)

if tests_failed == 0:
    print("\n🎉 所有测试通过！")
else:
    print(f"\n⚠️ 有 {tests_failed} 个测试失败")