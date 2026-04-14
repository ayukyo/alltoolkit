"""
Temperature Utils - 测试套件

测试覆盖：
- 基础转换功能
- 边界值测试
- 错误处理
- 批量操作
- 温度验证
- 比较和运算
- 参考点功能
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from temperature_utils.mod import (
    TemperatureUnit,
    ABSOLUTE_ZERO,
    REFERENCE_POINTS,
    TemperatureError,
    InvalidTemperatureError,
    InvalidUnitError,
    convert,
    convert_all,
    batch_convert,
    celsius_to_fahrenheit,
    celsius_to_kelvin,
    celsius_to_rankine,
    fahrenheit_to_celsius,
    fahrenheit_to_kelvin,
    fahrenheit_to_rankine,
    kelvin_to_celsius,
    kelvin_to_fahrenheit,
    kelvin_to_rankine,
    rankine_to_celsius,
    rankine_to_fahrenheit,
    rankine_to_kelvin,
    is_valid_temperature,
    is_above_freezing,
    is_below_freezing,
    is_fever,
    is_hypothermia,
    get_temperature_category,
    get_temperature_description,
    compare,
    add,
    subtract,
    difference,
    in_range,
    get_reference_point,
    list_reference_points,
    find_nearest_reference,
    format_temperature,
    parse_temperature,
)


class TestResult:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_equal(self, actual, expected, msg="", tolerance=1e-6):
        """带容差的相等比较"""
        if isinstance(actual, float) and isinstance(expected, float):
            if abs(actual - expected) <= tolerance:
                self.passed += 1
                return True
        elif actual == expected:
            self.passed += 1
            return True
        
        self.failed += 1
        error_msg = f"期望 {expected!r}, 得到 {actual!r}"
        if msg:
            error_msg = f"{msg}: {error_msg}"
        self.errors.append(error_msg)
        return False
    
    def assert_true(self, value, msg=""):
        return self.assert_equal(value, True, msg)
    
    def assert_false(self, value, msg=""):
        return self.assert_equal(value, False, msg)
    
    def assert_raises(self, exc_type, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.failed += 1
            self.errors.append(f"期望抛出 {exc_type.__name__}，但没有抛出异常")
            return False
        except exc_type:
            self.passed += 1
            return True
        except Exception as e:
            self.failed += 1
            self.errors.append(f"期望抛出 {exc_type.__name__}，但得到 {type(e).__name__}: {e}")
            return False
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"测试结果: {self.passed}/{total} 通过")
        print(f"{'='*60}")
        if self.errors:
            print("\n失败的测试:")
            for i, err in enumerate(self.errors, 1):
                print(f"  {i}. {err}")
        return self.failed == 0


def test_basic_conversions(r):
    """测试基础转换"""
    print("\n[test_basic_conversions]")
    
    # 摄氏度转华氏度
    r.assert_equal(celsius_to_fahrenheit(0), 32.0, "0°C -> 32°F")
    r.assert_equal(celsius_to_fahrenheit(100), 212.0, "100°C -> 212°F")
    r.assert_equal(celsius_to_fahrenheit(-40), -40.0, "-40°C -> -40°F")
    
    # 摄氏度转开尔文
    r.assert_equal(celsius_to_kelvin(0), 273.15, "0°C -> 273.15K")
    r.assert_equal(celsius_to_kelvin(-273.15), 0.0, "-273.15°C -> 0K")
    r.assert_equal(celsius_to_kelvin(100), 373.15, "100°C -> 373.15K")
    
    # 华氏度转摄氏度
    r.assert_equal(fahrenheit_to_celsius(32), 0.0, "32°F -> 0°C")
    r.assert_equal(fahrenheit_to_celsius(212), 100.0, "212°F -> 100°C")
    r.assert_equal(fahrenheit_to_celsius(-40), -40.0, "-40°F -> -40°C")
    
    # 开尔文转摄氏度
    r.assert_equal(kelvin_to_celsius(0), -273.15, "0K -> -273.15°C")
    r.assert_equal(kelvin_to_celsius(273.15), 0.0, "273.15K -> 0°C")
    r.assert_equal(kelvin_to_celsius(373.15), 100.0, "373.15K -> 100°C")
    
    # 兰氏度转换
    r.assert_equal(rankine_to_celsius(0), -273.15, "0°R -> -273.15°C")
    r.assert_equal(rankine_to_fahrenheit(0), -459.67, "0°R -> -459.67°F")
    r.assert_equal(celsius_to_rankine(0), 491.67, "0°C -> 491.67°R")


def test_convert_function(r):
    """测试通用转换函数"""
    print("\n[test_convert_function]")
    
    # 基本转换
    r.assert_equal(convert(0, 'C', 'F'), 32.0, "convert 0°C to °F")
    r.assert_equal(convert(100, 'C', 'K'), 373.15, "convert 100°C to K")
    r.assert_equal(convert(32, 'F', 'C'), 0.0, "convert 32°F to °C")
    r.assert_equal(convert(273.15, 'K', 'C'), 0.0, "convert 273.15K to °C")
    
    # 使用枚举
    r.assert_equal(convert(0, TemperatureUnit.CELSIUS, TemperatureUnit.FAHRENHEIT), 32.0, 
                   "使用枚举转换")
    
    # 单位别名
    r.assert_equal(convert(0, 'celsius', 'fahrenheit'), 32.0, "使用全名")
    r.assert_equal(convert(0, '摄氏度', '华氏度'), 32.0, "使用中文名")
    
    # 精度控制
    r.assert_equal(convert(0.123456, 'C', 'F', precision=2), 32.22, "精度控制")
    
    # 相同单位
    r.assert_equal(convert(25, 'C', 'C'), 25.0, "相同单位")


def test_convert_all(r):
    """测试转换到所有单位"""
    print("\n[test_convert_all]")
    
    result = convert_all(0, 'C')
    r.assert_equal(result['celsius'], 0.0, "celsius")
    r.assert_equal(result['fahrenheit'], 32.0, "fahrenheit")
    r.assert_equal(result['kelvin'], 273.15, "kelvin")
    r.assert_equal(result['rankine'], 491.67, "rankine")


def test_batch_convert(r):
    """测试批量转换"""
    print("\n[test_batch_convert]")
    
    # 基本批量
    result = batch_convert([0, 100, 200], 'C', 'F')
    r.assert_equal(len(result), 3, "批量数量")
    r.assert_equal(result[0], (0, 32.0, None), "batch 0°C -> 32°F")
    r.assert_equal(result[1], (100, 212.0, None), "batch 100°C -> 212°F")
    
    # 跳过无效值
    result = batch_convert([0, -300, 100], 'C', 'K', skip_invalid=True)
    r.assert_equal(result[0], (0, 273.15, None), "skip_invalid 第一个")
    r.assert_equal(result[1][0], -300, "skip_invalid 无效值")
    r.assert_equal(result[1][1], None, "skip_invalid 结果为None")
    r.assert_equal(result[2], (100, 373.15, None), "skip_invalid 最后一个")


def test_validation(r):
    """测试温度验证"""
    print("\n[test_validation]")
    
    # 有效温度
    r.assert_true(is_valid_temperature(0, 'K'), "0K 有效")
    r.assert_true(is_valid_temperature(273.15, 'K'), "273.15K 有效")
    r.assert_true(is_valid_temperature(-273.15, 'C'), "-273.15°C 有效")
    
    # 无效温度（低于绝对零度）
    r.assert_false(is_valid_temperature(-1, 'K'), "-1K 无效")
    r.assert_false(is_valid_temperature(-274, 'C'), "-274°C 无效")
    r.assert_false(is_valid_temperature(-500, 'F'), "-500°F 无效")


def test_freezing_checks(r):
    """测试冰点检查"""
    print("\n[test_freezing_checks]")
    
    r.assert_true(is_above_freezing(0, 'C'), "0°C 在冰点或以上")
    r.assert_false(is_above_freezing(-1, 'C'), "-1°C 不在冰点以上")
    r.assert_true(is_below_freezing(-1, 'C'), "-1°C 在冰点以下")
    r.assert_false(is_below_freezing(0, 'C'), "0°C 不在冰点以下")


def test_body_temperature(r):
    """测试体温相关功能"""
    print("\n[test_body_temperature]")
    
    r.assert_true(is_fever(38, 'C'), "38°C 是发烧")
    r.assert_false(is_fever(37, 'C'), "37°C 不是发烧")
    r.assert_true(is_fever(100, 'F'), "100°F 是发烧")
    r.assert_false(is_fever(98.6, 'F'), "98.6°F 不是发烧")
    
    r.assert_true(is_hypothermia(34, 'C'), "34°C 体温过低")
    r.assert_false(is_hypothermia(36, 'C'), "36°C 正常")


def test_temperature_category(r):
    """测试温度类别"""
    print("\n[test_temperature_category]")
    
    r.assert_equal(get_temperature_category(-40, 'C'), '极寒', "-40°C 极寒")
    r.assert_equal(get_temperature_category(-20, 'C'), '严寒', "-20°C 严寒")
    r.assert_equal(get_temperature_category(-5, 'C'), '寒冷', "-5°C 寒冷")
    r.assert_equal(get_temperature_category(5, 'C'), '凉爽', "5°C 凉爽")
    r.assert_equal(get_temperature_category(15, 'C'), '温和', "15°C 温和")
    r.assert_equal(get_temperature_category(25, 'C'), '舒适', "25°C 舒适")
    r.assert_equal(get_temperature_category(28, 'C'), '温暖', "28°C 温暖")
    r.assert_equal(get_temperature_category(33, 'C'), '炎热', "33°C 炎热")
    r.assert_equal(get_temperature_category(38, 'C'), '酷热', "38°C 酷热")
    r.assert_equal(get_temperature_category(45, 'C'), '极热', "45°C 极热")


def test_compare(r):
    """测试温度比较"""
    print("\n[test_compare]")
    
    # 相同温度
    r.assert_equal(compare(0, 'C', 32, 'F'), 0, "0°C = 32°F")
    r.assert_equal(compare(100, 'C', 212, 'F'), 0, "100°C = 212°F")
    r.assert_equal(compare(273.15, 'K', 0, 'C'), 0, "273.15K = 0°C")
    
    # 不同温度
    r.assert_equal(compare(0, 'C', 100, 'C'), -1, "0°C < 100°C")
    r.assert_equal(compare(100, 'C', 0, 'C'), 1, "100°C > 0°C")


def test_add_subtract(r):
    """测试温度加减"""
    print("\n[test_add_subtract]")
    
    # 加法
    r.assert_equal(add(0, 'C', 10, 'C'), 10.0, "0°C + 10°C温差")
    r.assert_equal(add(32, 'F', 10, 'C'), 50.0, "32°F + 10°C温差")
    
    # 减法
    r.assert_equal(subtract(10, 'C', 5, 'C'), 5.0, "10°C - 5°C温差")
    r.assert_equal(subtract(50, 'F', 10, 'C'), 32.0, "50°F - 10°C温差")


def test_difference(r):
    """测试温度差值计算"""
    print("\n[test_difference]")
    
    r.assert_equal(difference(100, 'C', 0, 'C'), 100.0, "100°C - 0°C = 100°C温差")
    r.assert_equal(difference(212, 'F', 32, 'F', 'C'), 100.0, "212°F - 32°F = 100°C温差")
    r.assert_equal(difference(0, 'C', 0, 'F', 'F'), 32.0, "0°C - 32°F = 32°F温差")


def test_in_range(r):
    """测试范围检查"""
    print("\n[test_in_range]")
    
    r.assert_true(in_range(25, 'C', 20, 30, 'C'), "25°C 在 20-30°C 范围内")
    r.assert_false(in_range(15, 'C', 20, 30, 'C'), "15°C 不在范围内")
    r.assert_true(in_range(68, 'F', 20, 30, 'C'), "68°F 在 20-30°C 范围内")


def test_reference_points(r):
    """测试参考点功能"""
    print("\n[test_reference_points]")
    
    # 获取参考点
    point = get_reference_point('water_boiling')
    r.assert_equal(point['celsius'], 100.0, "水沸点 100°C")
    r.assert_equal(point['fahrenheit'], 212.0, "水沸点 212°F")
    r.assert_equal(point['kelvin'], 373.15, "水沸点 373.15K")
    
    # 列出参考点
    points = list_reference_points()
    r.assert_true(len(points) > 0, "存在参考点")
    
    # 找到最近参考点
    name, desc, diff = find_nearest_reference(37, 'C')
    r.assert_equal(name, 'human_body', "37°C 最接近人体温度")
    r.assert_equal(diff, 0.0, "温差为0")


def test_format_parse(r):
    """测试格式化和解析"""
    print("\n[test_format_parse]")
    
    # 格式化
    r.assert_equal(format_temperature(36.5, 'C'), '36.5°C', "格式化摄氏度")
    r.assert_equal(format_temperature(100, 'F', precision=0), '100°F', "整数华氏度")
    r.assert_equal(format_temperature(273.15, 'K', precision=2, include_unit=False), '273.15', "无单位精度2")
    
    # 解析
    val, unit = parse_temperature('36.5°C')
    r.assert_equal(val, 36.5, "解析数值")
    r.assert_equal(unit, TemperatureUnit.CELSIUS, "解析单位")
    
    val, unit = parse_temperature('100 F')
    r.assert_equal(val, 100.0, "解析华氏度数值")
    r.assert_equal(unit, TemperatureUnit.FAHRENHEIT, "解析华氏度单位")
    
    val, unit = parse_temperature('273.15K')
    r.assert_equal(val, 273.15, "解析开尔文数值")
    r.assert_equal(unit, TemperatureUnit.KELVIN, "解析开尔文单位")


def test_absolute_zero(r):
    """测试绝对零度"""
    print("\n[test_absolute_zero]")
    
    r.assert_equal(ABSOLUTE_ZERO[TemperatureUnit.CELSIUS], -273.15, "摄氏度绝对零度")
    r.assert_equal(ABSOLUTE_ZERO[TemperatureUnit.FAHRENHEIT], -459.67, "华氏度绝对零度")
    r.assert_equal(ABSOLUTE_ZERO[TemperatureUnit.KELVIN], 0.0, "开尔文绝对零度")
    r.assert_equal(ABSOLUTE_ZERO[TemperatureUnit.RANKINE], 0.0, "兰氏度绝对零度")


def test_errors(r):
    """测试错误处理"""
    print("\n[test_errors]")
    
    # 无效温度
    r.assert_raises(InvalidTemperatureError, convert, -1, 'K', 'C')
    r.assert_raises(InvalidTemperatureError, convert, -274, 'C', 'K')
    r.assert_raises(InvalidTemperatureError, convert, -500, 'F', 'C')
    
    # 无效单位
    r.assert_raises(InvalidUnitError, convert, 0, 'X', 'C')
    r.assert_raises(InvalidUnitError, convert, 0, 'C', 'Y')
    
    # 无效参考点
    r.assert_raises(KeyError, get_reference_point, 'nonexistent')
    
    # 跳过检查时允许无效温度
    result = convert(-1, 'K', 'C', check_valid=False)
    r.assert_equal(result, -274.15, "跳过检查时允许无效温度")


def test_roundtrip(r):
    """测试往返转换"""
    print("\n[test_roundtrip]")
    
    # 测试多个值
    test_values = [0, 20, 100, -40, 37, -273.15]
    
    for val in test_values:
        # C -> F -> C
        f_val = convert(val, 'C', 'F')
        c_back = convert(f_val, 'F', 'C')
        r.assert_equal(c_back, val, f"C->F->C 往返 {val}°C", tolerance=1e-6)
        
        # C -> K -> C
        k_val = convert(val, 'C', 'K')
        c_back = convert(k_val, 'K', 'C')
        r.assert_equal(c_back, val, f"C->K->C 往返 {val}°C", tolerance=1e-6)


def test_temperature_description(r):
    """测试温度描述"""
    print("\n[test_temperature_description]")
    
    desc = get_temperature_description(25, 'C')
    r.assert_true('25°C' in desc or '25.00°C' in desc, "包含摄氏度")
    r.assert_true('77' in desc, "包含华氏度")
    r.assert_true('298' in desc, "包含开尔文")
    r.assert_true('舒适' in desc, "包含类别")


def run_all_tests():
    """运行所有测试"""
    r = TestResult()
    
    print("="*60)
    print("Temperature Utils 测试套件")
    print("="*60)
    
    test_basic_conversions(r)
    test_convert_function(r)
    test_convert_all(r)
    test_batch_convert(r)
    test_validation(r)
    test_freezing_checks(r)
    test_body_temperature(r)
    test_temperature_category(r)
    test_compare(r)
    test_add_subtract(r)
    test_difference(r)
    test_in_range(r)
    test_reference_points(r)
    test_format_parse(r)
    test_absolute_zero(r)
    test_errors(r)
    test_roundtrip(r)
    test_temperature_description(r)
    
    return r.summary()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)