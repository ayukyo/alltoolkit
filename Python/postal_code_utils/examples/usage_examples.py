"""
Postal Code Utilities - 使用示例

展示邮政编码工具的典型用法和实际应用场景。

作者: AllToolkit
日期: 2026-05-09
"""

import sys
import os

# 添加路径以导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    validate_postal_code,
    format_postal_code,
    normalize_postal_code,
    get_postal_code_info,
    extract_postal_codes,
    detect_country,
    is_valid_postal_code_format,
    get_country_postal_code_info,
    compare_postal_codes,
    get_nearby_postal_codes,
    batch_validate,
    generate_random_postal_code,
    get_supported_countries,
    PostalCodeInfo,
)


def example_basic_validation():
    """示例1：基本验证"""
    print("=" * 60)
    print("示例1：基本验证")
    print("=" * 60)
    
    # 验证中国邮编
    cn_codes = ["100001", "200001", "510000", "invalid", "10000"]
    print("\n中国邮编验证:")
    for code in cn_codes:
        is_valid = validate_postal_code(code, "CN")
        print(f"  {code}: {'有效 ✓' if is_valid else '无效 ✗'}")
    
    # 验证美国ZIP码
    us_codes = ["12345", "90210", "12345-6789", "invalid", "1234"]
    print("\n美国ZIP码验证:")
    for code in us_codes:
        is_valid = validate_postal_code(code, "US")
        print(f"  {code}: {'有效 ✓' if is_valid else '无效 ✗'}")
    
    # 验证英国邮编
    uk_codes = ["SW1A 1AA", "M1 1AA", "invalid", "12345"]
    print("\n英国邮编验证:")
    for code in uk_codes:
        is_valid = validate_postal_code(code, "UK")
        print(f"  {code}: {'有效 ✓' if is_valid else '无效 ✗'}")


def example_formatting():
    """示例2：格式化"""
    print("\n" + "=" * 60)
    print("示例2：格式化")
    print("=" * 60)
    
    # 格式化美国ZIP码
    print("\n美国ZIP码格式化:")
    us_codes = ["12345", "123456789", "12345-6789"]
    for code in us_codes:
        formatted = format_postal_code(code, "US")
        print(f"  {code} → {formatted}")
    
    # 格式化日本邮编
    print("\n日本邮编格式化:")
    jp_codes = ["100-0001", "1000001", "〒100-0001"]
    for code in jp_codes:
        formatted = format_postal_code(code, "JP")
        print(f"  {code} → {formatted}")
    
    # 格式化加拿大邮编
    print("\n加拿大邮编格式化:")
    ca_codes = ["K1A0B1", "k1a 0b1", "K1A 0B1"]
    for code in ca_codes:
        formatted = format_postal_code(code, "CA")
        print(f"  {code} → {formatted}")
    
    # 格式化英国邮编
    print("\n英国邮编格式化:")
    uk_codes = ["SW1A1AA", "sw1a 1aa", "SW1A 1AA"]
    for code in uk_codes:
        formatted = format_postal_code(code, "UK")
        print(f"  {code} → {formatted}")


def example_normalization():
    """示例3：标准化"""
    print("\n" + "=" * 60)
    print("示例3：标准化（去除空格、连字符等）")
    print("=" * 60)
    
    codes_to_normalize = [
        ("12345-6789", "US"),
        ("〒100-0001", "JP"),
        ("K1A 0B1", "CA"),
        ("SW1A 1AA", "UK"),
        ("1011 AB", "NL"),
        ("00-001", "PL"),
    ]
    
    print("\n标准化示例:")
    for code, country in codes_to_normalize:
        normalized = normalize_postal_code(code, country)
        print(f"  {country}: {code} → {normalized}")


def example_get_info():
    """示例4：获取详细信息"""
    print("\n" + "=" * 60)
    print("示例4：获取详细信息")
    print("=" * 60)
    
    codes = [
        ("100001", "CN"),
        ("12345-6789", "US"),
        ("K1A 0B1", "CA"),
        ("SW1A 1AA", "UK"),
    ]
    
    print("\n邮编详细信息:")
    for code, country in codes:
        info = get_postal_code_info(code, country)
        print(f"\n  {country} - {code}:")
        print(f"    有效: {info.is_valid}")
        print(f"    格式化: {info.code}")
        print(f"    标准化: {info.normalized}")
        print(f"    格式类型: {info.format_type}")
        print(f"    原始输入: {info.raw_input}")


def example_extract():
    """示例5：从文本提取"""
    print("\n" + "=" * 60)
    print("示例5：从文本提取邮编")
    print("=" * 60)
    
    texts = [
        ("请寄往北京市朝阳区 100001", "CN"),
        ("Ship to ZIP code 12345 or 90210-1234", "US"),
        ("Address: 10 Downing Street, SW1A 1AA, London", "UK"),
        ("Destination: K1A 0B1, Ottawa, Canada", "CA"),
    ]
    
    print("\n从文本提取:")
    for text, country in texts:
        codes = extract_postal_codes(text, country)
        print(f"  文本: {text}")
        print(f"  提取: {codes}")
    
    # 多国家提取
    print("\n多国家提取:")
    text = "CN: 100001, US: 12345, UK: SW1A 1AA, CA: K1A 0B1"
    codes = extract_postal_codes(text)
    print(f"  文本: {text}")
    print(f"  提取: {codes}")


def example_detect_country():
    """示例6：自动检测国家"""
    print("\n" + "=" * 60)
    print("示例6：自动检测国家")
    print("=" * 60)
    
    codes = [
        "100001",      # 可能是中国、俄罗斯、印度等
        "12345",       # 可能是美国、德国、法国等
        "K1A 0B1",     # 肯定是加拿大
        "SW1A 1AA",    # 肯定是英国
        "100-0001",    # 肯定是日本
    ]
    
    print("\n自动检测国家:")
    for code in codes:
        countries = detect_country(code)
        print(f"  {code} → 可能的国家: {countries}")


def example_country_info():
    """示例7：获取国家邮编规则"""
    print("\n" + "=" * 60)
    print("示例7：获取国家邮编规则信息")
    print("=" * 60)
    
    countries = ["CN", "US", "JP", "UK", "CA"]
    
    print("\n国家邮编规则:")
    for country in countries:
        info = get_country_postal_code_info(country)
        print(f"\n  {country} - {info['name']}:")
        print(f"    示例邮编: {info['example_codes']}")
        print(f"    格式数量: {len(info['patterns'])}")


def example_compare():
    """示例8：比较邮编"""
    print("\n" + "=" * 60)
    print("示例8：比较邮编")
    print("=" * 60)
    
    pairs = [
        ("100001", "100002", "CN"),
        ("12345", "12346", "US"),
        ("123456789", "12345-6789", "US"),  # 标准化后相同
        ("K1A 0B1", "K1A 0B2", "CA"),
    ]
    
    print("\n比较结果:")
    for code1, code2, country in pairs:
        result = compare_postal_codes(code1, code2, country)
        comparison = "<" if result < 0 else ">" if result > 0 else "="
        print(f"  {country}: {code1} {comparison} {code2}")


def example_nearby():
    """示例9：获取附近邮编"""
    print("\n" + "=" * 60)
    print("示例9：获取附近邮编")
    print("=" * 60)
    
    codes = [
        ("100001", "CN", 3),
        ("12345", "US", 2),
        ("75001", "FR", 5),
    ]
    
    print("\n附近邮编:")
    for code, country, delta in codes:
        nearby = get_nearby_postal_codes(code, country, delta)
        print(f"  {country}: {code} 附近 ({delta}范围):")
        print(f"    {nearby}")


def example_batch_validate():
    """示例10：批量验证"""
    print("\n" + "=" * 60)
    print("示例10：批量验证")
    print("=" * 60)
    
    batch = [
        ("100001", "CN"),
        ("200001", "CN"),
        ("invalid", "CN"),
        ("12345", "US"),
        ("90210", "US"),
        ("invalid", "US"),
        ("K1A 0B1", "CA"),
    ]
    
    print("\n批量验证:")
    result = batch_validate(batch)
    
    print(f"\n  有效邮编 ({len(result['valid'])}):")
    for info in result['valid']:
        print(f"    {info.country}: {info.code}")
    
    print(f"\n  无效邮编 ({len(result['invalid'])}):")
    for info in result['invalid']:
        print(f"    {info.country}: {info.raw_input}")


def example_random_generation():
    """示例11：生成随机邮编"""
    print("\n" + "=" * 60)
    print("示例11：生成随机邮编（用于测试）")
    print("=" * 60)
    
    countries = ["CN", "US", "JP", "UK", "CA", "DE", "FR", "AU", "BR"]
    
    print("\n随机邮编:")
    for country in countries:
        code = generate_random_postal_code(country)
        print(f"  {country}: {code}")


def example_supported_countries():
    """示例12：获取支持的国家列表"""
    print("\n" + "=" * 60)
    print("示例12：获取支持的国家列表")
    print("=" * 60)
    
    countries = get_supported_countries()
    
    print(f"\n支持的国家数量: {len(countries)}")
    print("\n国家列表:")
    for country in countries:
        print(f"  {country['code']}: {country['name']}")


def example_address_validation():
    """示例13：地址验证应用"""
    print("\n" + "=" * 60)
    print("示例13：地址验证应用场景")
    print("=" * 60)
    
    # 模拟地址输入验证
    addresses = [
        {"address": "北京市朝阳区建国路88号", "postal_code": "100001", "country": "CN"},
        {"address": "123 Main St, New York", "postal_code": "10001", "country": "US"},
        {"address": "10 Downing Street, London", "postal_code": "SW1A 1AA", "country": "UK"},
        {"address": "Invalid Address", "postal_code": "invalid", "country": "CN"},
    ]
    
    print("\n地址验证:")
    for addr in addresses:
        is_valid = validate_postal_code(addr["postal_code"], addr["country"])
        formatted = format_postal_code(addr["postal_code"], addr["country"])
        print(f"\n  地址: {addr['address']}")
        print(f"  邮编: {addr['postal_code']} → {formatted}")
        print(f"  国家: {addr['country']}")
        print(f"  有效: {'✓ 是' if is_valid else '✗ 否'}")


def example_form_integration():
    """示例14：表单集成示例"""
    print("\n" + "=" * 60)
    print("示例14：表单集成示例")
    print("=" * 60)
    
    # 模拟表单数据
    form_data = {
        "name": "张三",
        "country": "CN",
        "postal_code": "100001",
        "city": "北京",
    }
    
    print("\n表单数据处理:")
    print(f"  输入: {form_data}")
    
    # 验证邮编
    is_valid = validate_postal_code(form_data["postal_code"], form_data["country"])
    print(f"  验证结果: {'有效' if is_valid else '无效'}")
    
    if is_valid:
        # 格式化邮编
        formatted = format_postal_code(form_data["postal_code"], form_data["country"])
        print(f"  格式化邮编: {formatted}")
        
        # 标准化邮编（用于存储）
        normalized = normalize_postal_code(form_data["postal_code"], form_data["country"])
        print(f"  标准化邮编: {normalized}")
        
        # 获取详细信息
        info = get_postal_code_info(form_data["postal_code"], form_data["country"])
        print(f"  详细信息:")
        print(f"    格式类型: {info.format_type}")
        print(f"    地区: {info.region if info.region else '未知'}")


def example_api_integration():
    """示例15：API集成示例"""
    print("\n" + "=" * 60)
    print("示例15：API集成示例（批量处理）")
    print("=" * 60)
    
    # 模拟API请求数据
    api_requests = [
        {"id": 1, "postal_code": "100001", "country": "CN"},
        {"id": 2, "postal_code": "12345", "country": "US"},
        {"id": 3, "postal_code": "SW1A 1AA", "country": "UK"},
        {"id": 4, "postal_code": "K1A 0B1", "country": "CA"},
        {"id": 5, "postal_code": "invalid", "country": "CN"},
    ]
    
    print("\nAPI批量处理:")
    
    # 准备批量验证数据
    batch = [(req["postal_code"], req["country"]) for req in api_requests]
    result = batch_validate(batch)
    
    # 返回处理结果
    print(f"\n  有效请求: {len(result['valid'])}")
    print(f"  无效请求: {len(result['invalid'])}")
    
    # 模拟返回数据
    valid_responses = [
        {
            "id": req["id"],
            "postal_code": format_postal_code(req["postal_code"], req["country"]),
            "normalized": normalize_postal_code(req["postal_code"], req["country"]),
            "valid": True,
        }
        for req in api_requests
        if validate_postal_code(req["postal_code"], req["country"])
    ]
    
    print("\n  有效响应:")
    for resp in valid_responses:
        print(f"    ID {resp['id']}: {resp['postal_code']} (normalized: {resp['normalized']})")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Postal Code Utilities - 使用示例")
    print("邮政编码工具库 - 多国邮政编码验证、格式化、提取")
    print("=" * 60)
    
    example_basic_validation()
    example_formatting()
    example_normalization()
    example_get_info()
    example_extract()
    example_detect_country()
    example_country_info()
    example_compare()
    example_nearby()
    example_batch_validate()
    example_random_generation()
    example_supported_countries()
    example_address_validation()
    example_form_integration()
    example_api_integration()
    
    print("\n" + "=" * 60)
    print("示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()