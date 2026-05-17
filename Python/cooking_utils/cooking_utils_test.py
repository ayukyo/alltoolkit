#!/usr/bin/env python3
"""
Cooking Utils 测试套件

测试覆盖：
- 温度单位转换
- 重量单位转换
- 容积单位转换
- 烘焙时间计算
- 食物保存指南
- 食材替代建议
- 烹饪术语词典
- 火候控制指南
- 边界值和异常处理
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    TemperatureUnit,
    WeightUnit,
    VolumeUnit,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    convert_temperature,
    get_common_temperatures,
    grams_to_ounces,
    ounces_to_grams,
    grams_to_pounds,
    pounds_to_grams,
    kilograms_to_pounds,
    pounds_to_kilograms,
    convert_weight,
    milliliters_to_cups,
    cups_to_milliliters,
    milliliters_to_tablespoons,
    tablespoons_to_milliliters,
    milliliters_to_teaspoons,
    teaspoons_to_milliliters,
    convert_volume,
    calculate_baking_time,
    get_oven_preheat_time,
    get_food_storage_info,
    get_ingredient_substitutes,
    get_cooking_term_definition,
    get_all_cooking_terms,
    get_heat_level_guide,
    recommend_heat_level,
    quick_convert,
    recipe_scale,
    calculate_cooking_water_ratio,
)


class TestResultCollector:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_equal(self, actual, expected, msg="", tolerance=None):
        # 默认容差
        if tolerance is None:
            tolerance = 0.01
        # 如果 tolerance 是字符串，说明参数顺序错了，重新解析
        if isinstance(tolerance, str):
            # 实际调用形式是 assert_equal(actual, expected, tolerance, msg)
            msg = tolerance
            tolerance = 0.01
        
        if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
            if abs(actual - expected) <= tolerance:
                self.passed += 1
            else:
                self.failed += 1
                self.errors.append(f"断言失败: {msg}\n  期望: {expected}±{tolerance}\n  实际: {actual}")
        else:
            if actual == expected:
                self.passed += 1
            else:
                self.failed += 1
                self.errors.append(f"断言失败: {msg}\n  期望: {expected}\n  实际: {actual}")
    
    def assert_true(self, condition, msg=""):
        if condition:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"断言失败: {msg}")
    
    def assert_false(self, condition, msg=""):
        self.assert_true(not condition, msg)
    
    def assert_raises(self, exception_class, func, msg=""):
        try:
            func()
            self.failed += 1
            self.errors.append(f"断言失败: {msg}\n  期望抛出 {exception_class.__name__}")
        except exception_class:
            self.passed += 1
        except Exception as e:
            self.failed += 1
            self.errors.append(f"断言失败: {msg}\n  期望 {exception_class.__name__}，实际抛出 {type(e).__name__}")
    
    def assert_in(self, item, container, msg=""):
        if item in container:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"断言失败: {msg}\n  {item} 不在容器中")
    
    def assert_not_empty(self, container, msg=""):
        if len(container) > 0:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"断言失败: {msg}\n  容器为空")
    
    def report(self, test_name):
        status = "✅" if self.failed == 0 else "❌"
        print(f"{status} {test_name}: {self.passed} passed, {self.failed} failed")
        for error in self.errors:
            print(f"  - {error}")
        return self.failed == 0


# ============ 温度转换测试 ============

def test_celsius_to_fahrenheit():
    """测试摄氏转华氏"""
    t = TestResultCollector()
    
    t.assert_equal(celsius_to_fahrenheit(0), 32, "冰点")
    t.assert_equal(celsius_to_fahrenheit(100), 212, "沸点")
    t.assert_equal(celsius_to_fahrenheit(180), 356, "烘焙温度")
    t.assert_equal(celsius_to_fahrenheit(-40), -40, "等温点")
    t.assert_equal(celsius_to_fahrenheit(20), 68, "室温")
    
    return t.report("test_celsius_to_fahrenheit")


def test_fahrenheit_to_celsius():
    """测试华氏转摄氏"""
    t = TestResultCollector()
    
    t.assert_equal(fahrenheit_to_celsius(32), 0, "冰点")
    t.assert_equal(fahrenheit_to_celsius(212), 100, "沸点")
    t.assert_equal(fahrenheit_to_celsius(350), 177, "烘焙温度", tolerance=1)  # 增加容差
    t.assert_equal(fahrenheit_to_celsius(-40), -40, "等温点")
    
    return t.report("test_fahrenheit_to_celsius")


def test_convert_temperature():
    """测试温度单位转换"""
    t = TestResultCollector()
    
    # 同单位转换
    t.assert_equal(convert_temperature(100, TemperatureUnit.CELSIUS, TemperatureUnit.CELSIUS), 100, "同单位")
    
    # 跨单位转换
    t.assert_equal(convert_temperature(100, TemperatureUnit.CELSIUS, TemperatureUnit.FAHRENHEIT), 212, "C转F")
    t.assert_equal(convert_temperature(212, TemperatureUnit.FAHRENHEIT, TemperatureUnit.CELSIUS), 100, "F转C")
    
    return t.report("test_convert_temperature")


def test_get_common_temperatures():
    """测试常见温度参考"""
    t = TestResultCollector()
    
    temps = get_common_temperatures()
    
    t.assert_not_empty(temps, "温度表不为空")
    t.assert_in("水沸腾", temps, "包含水沸腾")
    t.assert_in("中温烘烤", temps, "包含中温烘烤")
    
    # 验证格式
    t.assert_true(len(temps["水沸腾"]) == 2, "温度格式正确")
    t.assert_equal(temps["水沸腾"][0], 100, "水沸腾摄氏")
    t.assert_equal(temps["水沸腾"][1], 212, "水沸腾华氏")
    
    return t.report("test_get_common_temperatures")


# ============ 重量转换测试 ============

def test_grams_to_ounces():
    """测试克转盎司"""
    t = TestResultCollector()
    
    t.assert_equal(grams_to_ounces(28.35), 1, "标准盎司")
    t.assert_equal(grams_to_ounces(100), 3.53, 0.1, "100克")
    t.assert_equal(grams_to_ounces(500), 17.64, 0.1, "500克")
    t.assert_equal(grams_to_ounces(0), 0, "零值")
    
    return t.report("test_grams_to_ounces")


def test_ounces_to_grams():
    """测试盎司转克"""
    t = TestResultCollector()
    
    t.assert_equal(ounces_to_grams(1), 28.35, 0.1, "1盎司")
    t.assert_equal(ounces_to_grams(8), 226.8, 0.5, "8盎司")
    t.assert_equal(ounces_to_grams(0), 0, "零值")
    
    return t.report("test_ounces_to_grams")


def test_grams_to_pounds():
    """测试克转磅"""
    t = TestResultCollector()
    
    t.assert_equal(grams_to_pounds(453.6), 1, 0.01, "标准磅")
    t.assert_equal(grams_to_pounds(1000), 2.2, 0.1, "1000克")
    
    return t.report("test_grams_to_pounds")


def test_pounds_to_grams():
    """测试磅转克"""
    t = TestResultCollector()
    
    t.assert_equal(pounds_to_grams(1), 453.6, "1磅", tolerance=1)
    t.assert_equal(pounds_to_grams(2), 907.2, "2磅", tolerance=1)
    
    return t.report("test_pounds_to_grams")


def test_kilograms_pounds():
    """测试千克和磅转换"""
    t = TestResultCollector()
    
    t.assert_equal(kilograms_to_pounds(1), 2.2, 0.1, "1千克转磅")
    t.assert_equal(pounds_to_kilograms(2.2), 1, 0.1, "2.2磅转千克")
    
    return t.report("test_kilograms_pounds")


def test_convert_weight():
    """测试重量单位转换"""
    t = TestResultCollector()
    
    # 同单位
    t.assert_equal(convert_weight(100, WeightUnit.GRAM, WeightUnit.GRAM), 100, "同单位")
    
    # 跨单位
    t.assert_equal(convert_weight(1000, WeightUnit.GRAM, WeightUnit.KILOGRAM), 1, "克转千克")
    t.assert_equal(convert_weight(1, WeightUnit.KILOGRAM, WeightUnit.GRAM), 1000, "千克转克")
    t.assert_equal(convert_weight(1000, WeightUnit.GRAM, WeightUnit.POUND), 2.2, 0.1, "克转磅")
    
    return t.report("test_convert_weight")


# ============ 容积转换测试 ============

def test_ml_to_cups():
    """测试毫升转杯"""
    t = TestResultCollector()
    
    t.assert_equal(milliliters_to_cups(240), 1, "标准杯", tolerance=0.1)
    t.assert_equal(milliliters_to_cups(480), 2, "2杯", tolerance=0.1)
    t.assert_equal(milliliters_to_cups(0), 0, "零值")
    
    return t.report("test_ml_to_cups")


def test_cups_to_ml():
    """测试杯转毫升"""
    t = TestResultCollector()
    
    t.assert_equal(cups_to_milliliters(1), 240, "1杯")
    t.assert_equal(cups_to_milliliters(0.5), 120, "半杯")
    
    return t.report("test_cups_to_ml")


def test_ml_to_tablespoons():
    """测试毫升转汤匙"""
    t = TestResultCollector()
    
    t.assert_equal(milliliters_to_tablespoons(15), 1, "1汤匙", tolerance=0.1)
    t.assert_equal(milliliters_to_tablespoons(30), 2, "2汤匙", tolerance=0.1)
    
    return t.report("test_ml_to_tablespoons")


def test_tablespoons_to_ml():
    """测试汤匙转毫升"""
    t = TestResultCollector()
    
    t.assert_equal(tablespoons_to_milliliters(1), 15, "1汤匙")
    t.assert_equal(tablespoons_to_milliliters(2), 30, "2汤匙")
    
    return t.report("test_tablespoons_to_ml")


def test_ml_to_teaspoons():
    """测试毫升转茶匙"""
    t = TestResultCollector()
    
    t.assert_equal(milliliters_to_teaspoons(5), 1, "1茶匙", tolerance=0.1)
    t.assert_equal(milliliters_to_teaspoons(15), 3, "3茶匙", tolerance=0.1)
    
    return t.report("test_ml_to_teaspoons")


def test_teaspoons_to_ml():
    """测试茶匙转毫升"""
    t = TestResultCollector()
    
    t.assert_equal(teaspoons_to_milliliters(1), 5, "1茶匙")
    t.assert_equal(teaspoons_to_milliliters(3), 15, "3茶匙")
    
    return t.report("test_teaspoons_to_ml")


def test_convert_volume():
    """测试容积单位转换"""
    t = TestResultCollector()
    
    # 同单位
    t.assert_equal(convert_volume(100, VolumeUnit.MILLILITER, VolumeUnit.MILLILITER), 100, "同单位")
    
    # 跨单位
    t.assert_equal(convert_volume(1000, VolumeUnit.MILLILITER, VolumeUnit.LITER), 1, "毫升转升")
    t.assert_equal(convert_volume(1, VolumeUnit.LITER, VolumeUnit.MILLILITER), 1000, "升转毫升")
    
    return t.report("test_convert_volume")


# ============ 烘焙计算测试 ============

def test_calculate_baking_time():
    """测试烘焙时间计算"""
    t = TestResultCollector()
    
    # 基础计算
    result = calculate_baking_time(180, TemperatureUnit.CELSIUS, "蛋糕")
    t.assert_in("min_time_minutes", result, "包含最小时间")
    t.assert_in("max_time_minutes", result, "包含最大时间")
    t.assert_true(result["min_time_minutes"] <= result["max_time_minutes"], "时间范围有效")
    
    # 温度转换验证（增加容差）
    result_f = calculate_baking_time(350, TemperatureUnit.FAHRENHEIT, "蛋糕")
    t.assert_equal(result_f["oven_temp_celsius"], 177, "F转C正确", tolerance=1)
    
    return t.report("test_calculate_baking_time")


def test_get_oven_preheat_time():
    """测试烤箱预热时间"""
    t = TestResultCollector()
    
    t.assert_equal(get_oven_preheat_time(100), 5, "低温预热")
    t.assert_equal(get_oven_preheat_time(175), 10, "中温预热")
    t.assert_equal(get_oven_preheat_time(220), 15, "高温预热")
    t.assert_equal(get_oven_preheat_time(280), 20, "极高预热")
    
    return t.report("test_get_oven_preheat_time")


# ============ 食物保存测试 ============

def test_get_food_storage_info():
    """测试食物保存信息"""
    t = TestResultCollector()
    
    info = get_food_storage_info("鸡蛋")
    t.assert_in("冷藏", info, "包含冷藏信息")
    t.assert_in("冷冻", info, "包含冷冻信息")
    
    info2 = get_food_storage_info("生肉")
    t.assert_in("冷藏", info2, "生肉包含冷藏")
    
    # 未知食物
    info_unknown = get_food_storage_info("未知食物")
    t.assert_in("提示", info_unknown, "未知食物返回提示")
    
    return t.report("test_get_food_storage_info")


# ============ 食材替代测试 ============

def test_get_ingredient_substitutes():
    """测试食材替代建议"""
    t = TestResultCollector()
    
    subs = get_ingredient_substitutes("鸡蛋")
    t.assert_not_empty(subs, "鸡蛋有替代方案")
    t.assert_true(len(subs) >= 1, "至少一个替代方案")
    
    # 检查替代方案格式
    first_sub = subs[0]
    t.assert_in("替代", first_sub, "包含替代名称")
    
    # 未知食材
    unknown_subs = get_ingredient_substitutes("未知食材")
    t.assert_in("提示", unknown_subs[0], "未知食材返回提示")
    
    return t.report("test_get_ingredient_substitutes")


# ============ 烹饪术语测试 ============

def test_get_cooking_term_definition():
    """测试烹饪术语定义"""
    t = TestResultCollector()
    
    def1 = get_cooking_term_definition("焯水")
    t.assert_in("术语", def1, "包含术语")
    t.assert_in("定义", def1, "包含定义")
    t.assert_true(len(def1["定义"]) > 10, "定义有内容")
    
    # 未知术语
    def_unknown = get_cooking_term_definition("未知术语")
    t.assert_equal(def_unknown["定义"], "未找到该术语的定义", "未知术语提示")
    
    return t.report("test_get_cooking_term_definition")


def test_get_all_cooking_terms():
    """测试获取所有烹饪术语"""
    t = TestResultCollector()
    
    terms = get_all_cooking_terms()
    t.assert_not_empty(terms, "术语表不为空")
    t.assert_in("煎", terms, "包含煎")
    t.assert_in("炒", terms, "包含炒")
    
    return t.report("test_get_all_cooking_terms")


# ============ 火候控制测试 ============

def test_get_heat_level_guide():
    """测试火候控制指南"""
    t = TestResultCollector()
    
    guide = get_heat_level_guide()
    t.assert_not_empty(guide, "火候指南不为空")
    t.assert_in("大火", guide, "包含大火")
    t.assert_in("小火", guide, "包含小火")
    
    # 检查格式
    fire_info = guide["大火"]
    t.assert_in("温度", fire_info, "包含温度")
    t.assert_in("适用", fire_info, "包含适用")
    
    return t.report("test_get_heat_level_guide")


def test_recommend_heat_level():
    """测试火候推荐"""
    t = TestResultCollector()
    
    rec = recommend_heat_level("炒菜")
    t.assert_in("火候", rec, "包含火候")
    t.assert_in("说明", rec, "包含说明")
    
    rec2 = recommend_heat_level("炖汤")
    t.assert_true("小火" in rec2["火候"], "炖汤推荐小火")
    
    # 未知菜肴
    unknown_rec = recommend_heat_level("未知菜肴")
    t.assert_in("提示", unknown_rec, "未知菜肴返回提示")
    
    return t.report("test_recommend_heat_level")


# ============ 便捷函数测试 ============

def test_quick_convert():
    """测试快速转换"""
    t = TestResultCollector()
    
    # 温度
    t.assert_equal(quick_convert(100, "temperature", "celsius", "fahrenheit"), 212, "温度转换")
    
    # 重量
    t.assert_equal(quick_convert(1000, "weight", "gram", "kilogram"), 1, "重量转换")
    
    # 容积 - 注意 cup 转 ml 的方向
    result = quick_convert(1, "volume", "cup", "milliliter")
    t.assert_true(result > 200, f"容积转换: 1杯应该约240ml，实际{result}")
    
    return t.report("test_quick_convert")


def test_recipe_scale():
    """测试食谱缩放"""
    t = TestResultCollector()
    
    # 2人份到4人份
    t.assert_equal(recipe_scale(100, 2, 4), 200, "翻倍")
    
    # 4人份到2人份
    t.assert_equal(recipe_scale(100, 4, 2), 50, "减半")
    
    # 3人份到5人份
    t.assert_equal(recipe_scale(300, 3, 5), 500, "不规则缩放")
    
    # 异常
    t.assert_raises(ValueError, lambda: recipe_scale(100, 0, 4), "零人数")
    
    return t.report("test_recipe_scale")


def test_calculate_cooking_water_ratio():
    """测试米水比例"""
    t = TestResultCollector()
    
    ratio = calculate_cooking_water_ratio("普通米")
    t.assert_in("比例", ratio, "包含比例")
    t.assert_equal(ratio["比例"], 1.5, "普通米比例")
    
    ratio2 = calculate_cooking_water_ratio("糙米")
    t.assert_equal(ratio2["比例"], 2.0, "糙米比例")
    
    # 未知类型
    unknown_ratio = calculate_cooking_water_ratio("未知米")
    t.assert_equal(unknown_ratio["比例"], 1.5, "默认比例")
    
    return t.report("test_calculate_cooking_water_ratio")


# ============ 边界值测试 ============

def test_boundary_values():
    """测试边界值"""
    t = TestResultCollector()
    
    # 零值
    t.assert_equal(celsius_to_fahrenheit(0), 32, "零摄氏度")
    t.assert_equal(grams_to_ounces(0), 0, "零克")
    t.assert_equal(cups_to_milliliters(0), 0, "零杯")
    
    # 负值
    t.assert_equal(celsius_to_fahrenheit(-40), -40, "负摄氏度")
    t.assert_equal(grams_to_ounces(-100), -3.53, 0.1, "负克")
    
    # 极大值
    t.assert_equal(celsius_to_fahrenheit(1000), 1832, "极大摄氏度")
    
    return t.report("test_boundary_values")


# ============ 综合测试 ============

def test_integration():
    """测试综合场景"""
    t = TestResultCollector()
    
    # 模拟烘焙场景
    # 1. 预热烤箱
    preheat_time = get_oven_preheat_time(180)
    t.assert_true(preheat_time >= 5, "预热时间合理")
    
    # 2. 计算烘焙时间
    baking = calculate_baking_time(180, TemperatureUnit.CELSIUS, "蛋糕")
    t.assert_true(baking["min_time_minutes"] > 0, "烘焙时间合理")
    
    # 3. 食材替代
    subs = get_ingredient_substitutes("黄油")
    t.assert_not_empty(subs, "黄油替代方案")
    
    # 4. 火候推荐
    heat = recommend_heat_level("炒青菜")
    t.assert_in("大火", heat["火候"], "炒青菜用大火")
    
    return t.report("test_integration")


# ============ 运行所有测试 ============

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Cooking Utils 测试套件")
    print("=" * 60)
    
    tests = [
        # 温度转换测试
        test_celsius_to_fahrenheit,
        test_fahrenheit_to_celsius,
        test_convert_temperature,
        test_get_common_temperatures,
        
        # 重量转换测试
        test_grams_to_ounces,
        test_ounces_to_grams,
        test_grams_to_pounds,
        test_pounds_to_grams,
        test_kilograms_pounds,
        test_convert_weight,
        
        # 容积转换测试
        test_ml_to_cups,
        test_cups_to_ml,
        test_ml_to_tablespoons,
        test_tablespoons_to_ml,
        test_ml_to_teaspoons,
        test_teaspoons_to_ml,
        test_convert_volume,
        
        # 烘焙计算测试
        test_calculate_baking_time,
        test_get_oven_preheat_time,
        
        # 食物保存测试
        test_get_food_storage_info,
        
        # 食材替代测试
        test_get_ingredient_substitutes,
        
        # 烹饪术语测试
        test_get_cooking_term_definition,
        test_get_all_cooking_terms,
        
        # 火候控制测试
        test_get_heat_level_guide,
        test_recommend_heat_level,
        
        # 便捷函数测试
        test_quick_convert,
        test_recipe_scale,
        test_calculate_cooking_water_ratio,
        
        # 边界值测试
        test_boundary_values,
        
        # 综合测试
        test_integration,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: 异常 - {e}")
            failed += 1
    
    print("=" * 60)
    print(f"总计: {passed + failed} 测试, {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)