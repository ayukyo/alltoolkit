"""
中国身份证工具使用示例

本文件展示如何使用 chinese_id_utils 模块进行：
- 身份证验证
- 信息提取
- 批量处理
- 测试数据生成

运行方式: cd 到 chinese_id_utils 目录后执行 python examples/usage_examples.py
"""

import sys
import os
# 添加父目录到路径以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
# 直接导入mod模块
import mod


def example_basic_validation():
    """基本验证示例"""
    print("\n" + "=" * 50)
    print("基本验证示例")
    print("=" * 50)
    
    # 格式验证
    test_ids = [
        '11010519491231002X',  # 有效18位
        '110105491231002',     # 有效15位
        '12345',               # 无效长度
        '110105194912310AB',  # 无效字符
    ]
    
    for id_num in test_ids:
        valid, msg = mod.validate_format(id_num)
        status = "有效" if valid else f"无效: {msg}"
        print(f"  {id_num}: {status}")


def example_checksum():
    """校验码示例"""
    print("\n" + "=" * 50)
    print("校验码计算与验证示例")
    print("=" * 50)
    
    # 计算校验码
    id_17 = '11010519491231002'
    checksum = mod.calculate_checksum(id_17)
    print(f"  前17位: {id_17}")
    print(f"  计算校验码: {checksum}")
    
    # 验证校验码
    test_ids = [
        '11010519491231002X',  # 正确
        '11010519491231002A',  # 错误
    ]
    
    for id_num in test_ids:
        valid = mod.validate_checksum(id_num)
        status = "正确" if valid else "错误"
        print(f"  {id_num}: {status}")


def example_15_to_18():
    """15位转18位示例"""
    print("\n" + "=" * 50)
    print("15位转18位示例")
    print("=" * 50)
    
    id_15 = '110105491231002'
    id_18 = mod.convert_15_to_18(id_15)
    
    print(f"  原15位: {id_15}")
    print(f"  转18位: {id_18}")
    
    # 验证转换后的身份证
    valid = mod.is_valid_id(id_18)
    print(f"  转换后有效性: {'有效' if valid else '无效'}")


def example_info_extraction():
    """信息提取示例"""
    print("\n" + "=" * 50)
    print("信息提取示例")
    print("=" * 50)
    
    test_id = '11010519900307888X'
    
    # 提取出生日期
    birth = mod.extract_birth_date(test_id)
    print(f"  身份证: {test_id}")
    print(f"  出生日期: {birth}")
    
    # 提取性别
    gender = mod.extract_gender(test_id)
    print(f"  性别: {gender}")
    
    # 计算年龄
    age = mod.calculate_age(birth, date(2024, 1, 1))
    print(f"  年龄(2024年1月): {age}岁")
    
    # 获取地区
    province = mod.get_province('11')
    city = mod.get_city('1101')
    district = mod.get_district('110105')
    print(f"  地区: {province} {city} {district}")


def example_full_parse():
    """完整解析示例"""
    print("\n" + "=" * 50)
    print("完整解析示例")
    print("=" * 50)
    
    test_ids = [
        '11010519491231002X',  # 北京
        '44030519900101123X',  # 深圳（使用正确校验码）
        '31011519850315012X',  # 上海浦东（使用正确校验码）
    ]
    
    for id_num in test_ids:
        info = mod.parse_id(id_num)
        print(f"\n  身份证: {id_num}")
        if info.valid:
            print(f"    有效: 是")
            print(f"    省份: {info.province}")
            if info.city:
                print(f"    城市: {info.city}")
            if info.district:
                print(f"    区县: {info.district}")
            print(f"    出生日期: {info.birth_date}")
            print(f"    性别: {info.gender}")
            print(f"    年龄: {info.age}岁")
            print(f"    星座: {mod.get_zodiac(info.birth_date)}")
            print(f"    生肖: {mod.get_chinese_zodiac(info.birth_date)}")
            print(f"    校验码: {'正确' if info.checksum_valid else '错误'}")
        else:
            print(f"    有效: 否 ({info.error_message})")


def example_batch_parse():
    """批量解析示例"""
    print("\n" + "=" * 50)
    print("批量解析示例")
    print("=" * 50)
    
    ids = [
        '11010519491231002X',
        '44030519900101123X',
        'invalid_id',
        '51010419850515012X',
    ]
    
    results = mod.batch_parse(ids)
    
    valid_count = sum(1 for r in results if r.valid)
    print(f"  输入: {len(ids)}个身份证")
    print(f"  有效: {valid_count}个")
    print(f"  无效: {len(ids) - valid_count}个")
    
    # 显示无效身份证的错误信息
    for result in results:
        if not result.valid:
            print(f"  {result.id_number}: {result.error_message}")


def example_generate_test_ids():
    """生成测试身份证示例"""
    print("\n" + "=" * 50)
    print("生成测试身份证示例")
    print("=" * 50)
    
    # 生成各种测试身份证
    print("\n  生成不同地区的身份证:")
    provinces = [('11', '北京'), ('44', '广东'), ('31', '上海'), ('51', '四川')]
    for code, name in provinces:
        id_num = mod.generate_random_id(province_code=code, birth_date=date(1990, 1, 1))
        print(f"    {name}: {id_num}")
    
    print("\n  生成不同性别的身份证:")
    male_id = mod.generate_random_id(gender='男', birth_date=date(1995, 6, 15))
    female_id = mod.generate_random_id(gender='女', birth_date=date(1995, 6, 15))
    print(f"    男性: {male_id}")
    print(f"    女性: {female_id}")
    
    print("\n  生成不同年龄的身份证:")
    ages = [18, 25, 40, 60, 80]
    today = date.today()
    for age in ages:
        birth_year = today.year - age
        birth = date(birth_year, 1, 1)
        id_num = mod.generate_random_id(birth_date=birth)
        print(f"    {age}岁: {id_num} (出生于{birth_year}年)")
    
    print("\n  验证所有生成的身份证:")
    test_ids = [mod.generate_random_id() for _ in range(10)]
    valid_count = sum(1 for id_num in test_ids if mod.is_valid_id(id_num))
    print(f"    生成10个，全部有效: {'是' if valid_count == 10 else '否'}")


def example_format_output():
    """格式化输出示例"""
    print("\n" + "=" * 50)
    print("格式化输出示例")
    print("=" * 50)
    
    test_id = '11010519900307888X'
    info = mod.parse_id(test_id)
    
    formatted = mod.format_id_info(info)
    print(formatted)


def example_zodiac_calculation():
    """星座和生肖计算示例"""
    print("\n" + "=" * 50)
    print("星座和生肖计算示例")
    print("=" * 50)
    
    # 星座示例
    print("\n  星座计算:")
    test_dates = [
        (date(2000, 1, 15), '摩羯座'),
        (date(2000, 2, 15), '水瓶座'),
        (date(2000, 3, 21), '白羊座'),
        (date(2000, 7, 23), '狮子座'),
    ]
    for birth, expected in test_dates:
        zodiac = mod.get_zodiac(birth)
        match = '匹配' if zodiac == expected else '不匹配'
        print(f"    {birth.strftime('%Y-%m-%d')}: {zodiac} ({match})")
    
    # 生肖示例
    print("\n  生肖计算:")
    test_years = [
        (2000, '龙'),
        (2008, '鼠'),
        (2024, '龙'),
        (2025, '蛇'),
    ]
    for year, expected in test_years:
        zodiac = mod.get_chinese_zodiac(date(year, 1, 1))
        match = '匹配' if zodiac == expected else '不匹配'
        print(f"    {year}年: {zodiac} ({match})")


def example_error_cases():
    """错误处理示例"""
    print("\n" + "=" * 50)
    print("错误处理示例")
    print("=" * 50)
    
    error_cases = [
        ('', '空值'),
        ('12345', '长度错误'),
        ('11010519999999999X', '无效日期'),
        ('99999919491231002X', '无效地区码'),
        ('11010519491231002A', '校验码错误'),
        (f'110105{date.today().year + 1}0101' + '1234', '未来出生日期'),
    ]
    
    for id_num, desc in error_cases:
        info = mod.parse_id(id_num)
        print(f"  {desc}:")
        print(f"    输入: '{id_num}'")
        print(f"    结果: {info.error_message}")


def main():
    """运行所有示例"""
    print("\n")
    print("=" * 60)
    print("中国身份证工具 (chinese_id_utils) 使用示例")
    print("=" * 60)
    
    example_basic_validation()
    example_checksum()
    example_15_to_18()
    example_info_extraction()
    example_full_parse()
    example_batch_parse()
    example_generate_test_ids()
    example_format_output()
    example_zodiac_calculation()
    example_error_cases()
    
    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()