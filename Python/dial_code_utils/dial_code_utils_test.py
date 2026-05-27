"""
国际电话区号工具测试模块
"""

import sys
import os

# 添加正确的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from mod import (
    get_country_by_dial_code,
    get_dial_code_by_country,
    get_all_countries,
    get_countries_by_continent,
    format_phone_number,
    validate_phone_number,
    extract_dial_code,
    get_country_name,
    is_valid_dial_code,
    search_countries,
    compare_dial_codes,
    DialCodeUtils
)


def test_get_country_by_dial_code():
    """测试根据区号查询国家"""
    # 测试中国区号
    china = get_country_by_dial_code("86")
    assert china is not None
    assert china["name"] == "中国"
    assert china["code"] == "CN"
    assert china["continent"] == "亚洲"
    
    # 测试带+前缀
    china2 = get_country_by_dial_code("+86")
    assert china2 is not None
    assert china2["name"] == "中国"
    
    # 测试美国区号
    us = get_country_by_dial_code("1")
    assert us is not None
    assert "美国" in us["name"]
    
    # 测试无效区号
    invalid = get_country_by_dial_code("999")
    assert invalid is None
    
    # 测试日本区号
    japan = get_country_by_dial_code("81")
    assert japan is not None
    assert japan["name"] == "日本"
    
    print("test_get_country_by_dial_code: PASSED")


def test_get_dial_code_by_country():
    """测试根据国家查询区号"""
    # 测试中文名称
    assert get_dial_code_by_country("中国") == "86"
    
    # 测试ISO代码
    assert get_dial_code_by_country("CN") == "86"
    assert get_dial_code_by_country("JP") == "81"
    assert get_dial_code_by_country("US") == "1"
    
    # 测试alpha3代码
    assert get_dial_code_by_country("CHN") == "86"
    assert get_dial_code_by_country("JPN") == "81"
    
    # 测试小写输入
    assert get_dial_code_by_country("cn") == "86"
    
    # 测试无效国家
    assert get_dial_code_by_country("不存在") is None
    
    print("test_get_dial_code_by_country: PASSED")


def test_get_all_countries():
    """测试获取所有国家"""
    countries = get_all_countries()
    assert len(countries) > 200
    
    # 检查数据结构
    first = countries[0]
    assert "dial_code" in first
    assert "name" in first
    assert "code" in first
    assert "continent" in first
    
    # 检查包含主要国家
    china_found = any(c["name"] == "中国" for c in countries)
    assert china_found
    
    print("test_get_all_countries: PASSED")


def test_get_countries_by_continent():
    """测试按大洲获取国家"""
    asia = get_countries_by_continent("亚洲")
    assert len(asia) > 20
    assert any(c["name"] == "中国" for c in asia)
    assert any(c["name"] == "日本" for c in asia)
    
    europe = get_countries_by_continent("欧洲")
    assert len(europe) > 30
    assert any(c["name"] == "德国" for c in europe)
    
    africa = get_countries_by_continent("非洲")
    assert len(africa) > 30
    
    print("test_get_countries_by_continent: PASSED")


def test_format_phone_number():
    """测试电话号码格式化"""
    # 国际格式
    intl = format_phone_number("13800138000", "86", "international")
    assert intl == "+86 138 0013 8000"
    
    # E.164格式
    e164 = format_phone_number("13800138000", "86", "e164")
    assert e164 == "+8613800138000"
    
    # 本地格式
    local = format_phone_number("13800138000", "86", "local")
    assert local == "138-0013-8000"
    
    # 易读格式
    readable = format_phone_number("13800138000", "86", "readable")
    assert readable == "+86 138-0013-8000"
    
    # 测试带分隔符的输入
    formatted = format_phone_number("138-0013-8000", "86", "international")
    assert formatted == "+86 138 0013 8000"
    
    # 测试美国号码
    us_intl = format_phone_number("2125551234", "1", "international")
    assert us_intl == "+1 212 555 1234"
    
    print("test_format_phone_number: PASSED")


def test_validate_phone_number():
    """测试电话号码验证"""
    # 有效号码
    valid, msg = validate_phone_number("13800138000", "86")
    assert valid is True
    
    # 号码过短
    valid, msg = validate_phone_number("123", "86")
    assert valid is False
    assert "长度不足" in msg
    
    # 号码过长
    valid, msg = validate_phone_number("12345678901234567890", "86")
    assert valid is False
    assert "过长" in msg
    
    # 空号码
    valid, msg = validate_phone_number("", "86")
    assert valid is False
    
    # 中国手机号验证
    valid, msg = validate_phone_number("22345678901", "86")
    assert valid is False  # 不是以1开头的11位
    
    print("test_validate_phone_number: PASSED")


def test_extract_dial_code():
    """测试提取区号"""
    # 带+前缀
    code, local = extract_dial_code("+8613800138000")
    assert code == "86"
    assert local == "13800138000"
    
    # 带00前缀
    code, local = extract_dial_code("008613800138000")
    assert code == "86"
    assert local == "13800138000"
    
    # 无前缀
    code, local = extract_dial_code("8613800138000")
    assert code == "86"
    assert local == "13800138000"
    
    # 美国号码
    code, local = extract_dial_code("+12125551234")
    assert code == "1"
    assert local == "2125551234"
    
    # 无法识别的号码（以非区号数字开头）
    code, local = extract_dial_code("99912345678")
    assert code is None
    assert local == "99912345678"
    
    print("test_extract_dial_code: PASSED")


def test_get_country_name():
    """测试获取国家名称"""
    assert get_country_name("86") == "中国"
    assert get_country_name("86", "zh") == "中国"
    
    print("test_get_country_name: PASSED")


def test_is_valid_dial_code():
    """测试区号有效性检查"""
    assert is_valid_dial_code("86") is True
    assert is_valid_dial_code("+86") is True
    assert is_valid_dial_code("81") is True
    assert is_valid_dial_code("1") is True
    assert is_valid_dial_code("999") is False
    assert is_valid_dial_code("12345") is False
    
    print("test_is_valid_dial_code: PASSED")


def test_search_countries():
    """测试搜索国家"""
    # 搜索中文名称
    results = search_countries("中国")
    assert len(results) >= 1
    assert results[0]["name"] == "中国"
    
    # 搜索区号
    results = search_countries("86")
    assert len(results) >= 1
    
    # 搜索ISO代码
    results = search_countries("CN")
    assert len(results) >= 1
    
    # 搜索日本
    results = search_countries("日本")
    assert len(results) >= 1
    assert results[0]["name"] == "日本"
    
    print("test_search_countries: PASSED")


def test_compare_dial_codes():
    """测试比较区号"""
    result = compare_dial_codes("86", "81")
    assert result["valid"] is True
    assert result["same_continent"] is True  # 都在亚洲
    
    result = compare_dial_codes("86", "1")
    assert result["valid"] is True
    assert result["same_continent"] is False
    
    result = compare_dial_codes("999", "86")
    assert result["valid"] is False
    
    print("test_compare_dial_codes: PASSED")


def test_dial_code_utils_class():
    """测试工具类"""
    # 验证类方法与独立函数结果一致
    assert DialCodeUtils.get_country("86") == get_country_by_dial_code("86")
    assert DialCodeUtils.get_dial_code("中国") == get_dial_code_by_country("中国")
    assert DialCodeUtils.get_all() == get_all_countries()
    assert DialCodeUtils.is_valid("86") == is_valid_dial_code("86")
    
    # 验证搜索
    results = DialCodeUtils.search("中国")
    assert len(results) >= 1
    
    # 验证格式化
    formatted = DialCodeUtils.format_phone("13800138000", "86", "international")
    assert formatted == "+86 138 0013 8000"
    
    # 验证提取
    code, local = DialCodeUtils.extract("+8613800138000")
    assert code == "86"
    
    print("test_dial_code_utils_class: PASSED")


def test_edge_cases():
    """测试边界情况"""
    # 空输入
    assert get_country_by_dial_code("") is None
    assert get_dial_code_by_country("") is None
    
    # 空格处理
    assert get_country_by_dial_code(" 86 ")["name"] == "中国"
    
    # 特殊字符处理
    formatted = format_phone_number("(138) 0013-8000", "86")
    assert "13800138000" in formatted.replace(" ", "").replace("-", "").replace("+", "")
    
    print("test_edge_cases: PASSED")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("国际电话区号工具测试")
    print("=" * 50)
    
    tests = [
        test_get_country_by_dial_code,
        test_get_dial_code_by_country,
        test_get_all_countries,
        test_get_countries_by_continent,
        test_format_phone_number,
        test_validate_phone_number,
        test_extract_dial_code,
        test_get_country_name,
        test_is_valid_dial_code,
        test_search_countries,
        test_compare_dial_codes,
        test_dial_code_utils_class,
        test_edge_cases
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"{test.__name__}: FAILED - {e}")
            failed += 1
        except Exception as e:
            print(f"{test.__name__}: ERROR - {e}")
            failed += 1
    
    print()
    print("=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)