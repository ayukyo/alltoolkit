"""
国际电话区号工具使用示例

演示如何使用 dial_code_utils 模块的各种功能
"""

import sys
import os

# 添加正确的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from mod import (
    get_country_by_dial_code,
    get_dial_code_by_country,
    get_all_countries,
    get_countries_by_continent,
    format_phone_number,
    validate_phone_number,
    extract_dial_code,
    search_countries,
    DialCodeUtils
)


def example_query_by_dial_code():
    """示例：根据区号查询国家"""
    print("\n=== 根据区号查询国家 ===\n")
    
    # 常见区号
    common_codes = ["86", "1", "44", "81", "82", "33", "49", "61"]
    
    for code in common_codes:
        country = get_country_by_dial_code(code)
        if country:
            print(f"区号 {code}: {country['name']} ({country['code']}) - {country['continent']}")
    
    # 带+前缀也支持
    print(f"\n区号 +86: {get_country_by_dial_code('+86')['name']}")


def example_query_by_country():
    """示例：根据国家查询区号"""
    print("\n=== 根据国家查询区号 ===\n")
    
    countries = ["中国", "美国", "日本", "英国", "法国", "德国", "韩国", "加拿大"]
    
    for name in countries:
        code = get_dial_code_by_country(name)
        print(f"{name}: 区号 {code}")
    
    # 使用ISO代码查询
    print(f"\nISO代码 CN: 区号 {get_dial_code_by_country('CN')}")
    print(f"ISO代码 US: 区号 {get_dial_code_by_country('US')}")
    print(f"alpha3代码 CHN: 区号 {get_dial_code_by_country('CHN')}")


def example_format_phone_numbers():
    """示例：格式化电话号码"""
    print("\n=== 格式化电话号码 ===\n")
    
    phone = "13800138000"
    dial_code = "86"
    
    print(f"原始号码: {phone}")
    print(f"国际格式: {format_phone_number(phone, dial_code, 'international')}")
    print(f"E.164格式: {format_phone_number(phone, dial_code, 'e164')}")
    print(f"本地格式: {format_phone_number(phone, dial_code, 'local')}")
    print(f"易读格式: {format_phone_number(phone, dial_code, 'readable')}")
    
    # 美国号码
    print("\n美国号码示例:")
    us_phone = "2125551234"
    print(f"原始: {us_phone}")
    print(f"国际格式: {format_phone_number(us_phone, '1', 'international')}")
    
    # 日本号码
    print("\n日本号码示例:")
    jp_phone = "9012345678"
    print(f"原始: {jp_phone}")
    print(f"国际格式: {format_phone_number(jp_phone, '81', 'international')}")


def example_validate_phone_numbers():
    """示例：验证电话号码"""
    print("\n=== 验证电话号码 ===\n")
    
    test_numbers = [
        ("13800138000", "86"),  # 有效中国号码
        ("12345", "86"),        # 过短
        ("12345678901234567890", "86"),  # 过长
        ("2125551234", "1"),    # 有效美国号码
    ]
    
    for phone, code in test_numbers:
        valid, msg = validate_phone_number(phone, code)
        status = "有效" if valid else "无效"
        print(f"{phone} (区号{code}): {status} - {msg}")


def example_extract_dial_code():
    """示例：提取区号和本地号码"""
    print("\n=== 提取区号和本地号码 ===\n")
    
    phones = [
        "+8613800138000",
        "008613800138000",
        "+12125551234",
        "+819012345678",
        "86-138-0013-8000",
    ]
    
    for phone in phones:
        code, local = extract_dial_code(phone)
        country = get_country_by_dial_code(code) if code else None
        country_name = country["name"] if country else "未知"
        print(f"{phone} -> 区号: {code}, 本地号码: {local}, 国家: {country_name}")


def example_search_countries():
    """示例：搜索国家"""
    print("\n=== 搜索国家 ===\n")
    
    # 搜索关键词
    keywords = ["中国", "日本", "86", "Asia", "CN", "非洲"]
    
    for keyword in keywords:
        results = search_countries(keyword)
        print(f"\n搜索 '{keyword}' 找到 {len(results)} 个结果:")
        for r in results[:5]:  # 只显示前5个
            print(f"  - {r['name']} ({r['dial_code']})")


def example_by_continent():
    """示例：按大洲获取国家"""
    print("\n=== 按大洲获取国家 ===\n")
    
    continents = ["亚洲", "欧洲", "北美", "南美", "非洲", "大洋洲"]
    
    for continent in continents:
        countries = get_countries_by_continent(continent)
        print(f"{continent}: {len(countries)} 个国家")
        # 显示前5个
        for c in countries[:5]:
            print(f"  - {c['name']} (+{c['dial_code']})")


def example_using_class():
    """示例：使用 DialCodeUtils 类"""
    print("\n=== 使用 DialCodeUtils 类 ===\n")
    
    utils = DialCodeUtils()
    
    # 查询
    print(f"区号86对应: {utils.get_country('86')['name']}")
    print(f"中国区号: {utils.get_dial_code('中国')}")
    
    # 格式化
    print(f"格式化号码: {utils.format_phone('13800138000', '86')}")
    
    # 验证
    valid, msg = utils.validate("13800138000", "86")
    print(f"号码验证: {valid}")
    
    # 提取
    code, local = utils.extract("+8613800138000")
    print(f"提取区号: {code}, 本地号码: {local}")
    
    # 检查有效性
    print(f"区号86有效: {utils.is_valid('86')}")
    print(f"区号999有效: {utils.is_valid('999')}")


def example_all_countries():
    """示例：获取所有国家"""
    print("\n=== 所有国家统计 ===\n")
    
    countries = get_all_countries()
    print(f"总计: {len(countries)} 个国家/地区")
    
    # 按大洲统计
    continents_count = {}
    for c in countries:
        continent = c.get("continent", "未知")
        continents_count[continent] = continents_count.get(continent, 0) + 1
    
    print("\n按大洲分布:")
    for continent, count in sorted(continents_count.items(), key=lambda x: -x[1]):
        print(f"  {continent}: {count} 个")


def example_common_use_cases():
    """示例：常见使用场景"""
    print("\n=== 常见使用场景 ===\n")
    
    # 场景1：用户输入电话号码，自动识别国家
    user_input = "+8613800138000"
    code, local = extract_dial_code(user_input)
    country = get_country_by_dial_code(code)
    print(f"用户输入: {user_input}")
    print(f"识别为国家: {country['name']}")
    print(f"本地号码: {local}")
    
    # 场景2：验证并格式化号码
    phone = "13800138000"
    valid, msg = validate_phone_number(phone, "86")
    if valid:
        formatted = format_phone_number(phone, "86", "international")
        print(f"\n验证成功，格式化后: {formatted}")
    
    # 场景3：查找特定国家的区号
    country_name = "德国"
    code = get_dial_code_by_country(country_name)
    print(f"\n{country_name}的国际区号是: +{code}")
    
    # 场景4：检查号码是否来自特定国家
    phone = "+442071234567"
    code, local = extract_dial_code(phone)
    is_uk = code == "44"
    print(f"\n{phone} 是英国号码吗? {is_uk}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("国际电话区号工具使用示例")
    print("=" * 60)
    
    example_query_by_dial_code()
    example_query_by_country()
    example_format_phone_numbers()
    example_validate_phone_numbers()
    example_extract_dial_code()
    example_search_countries()
    example_by_continent()
    example_using_class()
    example_all_countries()
    example_common_use_cases()
    
    print("\n" + "=" * 60)
    print("示例演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()