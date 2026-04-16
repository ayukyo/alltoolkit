"""
数据验证工具使用示例
展示各种验证函数的实际用法
"""

import sys
sys.path.insert(0, '..')

from mod import (
    ValidationResult,
    validate_email,
    validate_china_mobile,
    validate_china_id,
    validate_ipv4,
    validate_ipv6,
    validate_ip,
    validate_url,
    validate_json,
    validate_credit_card,
    validate_china_bank_card,
    validate_chinese_name,
    validate_password,
    validate_chinese_phone,
    validate_batch
)


def print_result(result: ValidationResult, label: str = ""):
    """打印验证结果"""
    status = "✓ 有效" if result.is_valid else "✗ 无效"
    print(f"{label}: {status}")
    print(f"  消息: {result.message}")
    if result.details:
        print(f"  详情: {result.details}")
    print()


def example_email_validation():
    """邮箱验证示例"""
    print("=" * 50)
    print("邮箱验证示例")
    print("=" * 50)
    
    emails = [
        'test@gmail.com',
        'user.name@company.co.uk',
        'user+alias@outlook.com',
        'invalid-email',
        '@example.com',
        'test@tempmail.com'
    ]
    
    for email in emails:
        print_result(validate_email(email), f"邮箱 '{email}'")
    
    # 检查域名
    print("检查域名:")
    print_result(
        validate_email('test@tempmail.com', check_domain=True),
        '临时邮箱（不允许）'
    )
    print_result(
        validate_email('test@tempmail.com', check_domain=True, allow_temp=True),
        '临时邮箱（允许）'
    )
    
    # 不允许 + 号别名
    print_result(
        validate_email('user+alias@gmail.com', allow_plus_alias=False),
        '+号别名（不允许）'
    )


def example_mobile_validation():
    """手机号验证示例"""
    print("=" * 50)
    print("中国手机号验证示例")
    print("=" * 50)
    
    phones = [
        '13812345678',
        '18612345678',
        '13312345678',
        '19212345678',  # 中国广电
        '17012345678',  # 虚拟运营商
        '12345678901',  # 无效号段
    ]
    
    for phone in phones:
        print_result(validate_china_mobile(phone), f"手机号 '{phone}'")
    
    # 国际格式
    print_result(validate_china_mobile('+8613812345678'), '国际格式')
    print_result(validate_china_mobile('86 138-1234-5678'), '带分隔符')


def example_id_validation():
    """身份证验证示例"""
    print("=" * 50)
    print("中国身份证验证示例")
    print("=" * 50)
    
    # 示例身份证号（测试用）
    ids = [
        '11010519900307234X',  # 北京，1990年
        '31010119900101001X',  # 上海
        '44010120001231234X',  # 广州，2000年
        'invalid_id',
    ]
    
    for id_num in ids:
        print_result(validate_china_id(id_num), f"身份证 '{id_num}'")
    
    # 年龄检查
    print("年龄检查:")
    print_result(
        validate_china_id('11010519900307234X', check_age=True, min_age=18),
        '检查年龄 >= 18岁'
    )


def example_ip_validation():
    """IP地址验证示例"""
    print("=" * 50)
    print("IP地址验证示例")
    print("=" * 50)
    
    # IPv4
    ipv4_list = [
        '192.168.1.1',
        '10.0.0.1',
        '127.0.0.1',
        '8.8.8.8',
        '192.168.1.256',
        'invalid'
    ]
    
    print("IPv4 验证:")
    for ip in ipv4_list:
        print_result(validate_ipv4(ip), f"'{ip}'")
    
    # IPv6
    ipv6_list = [
        '2001:db8::1',
        '::1',
        '::',
        'fe80::1',
        '2001:db8:85a3::8a2e:370:7334',
        '::ffff:192.168.1.1',
        'invalid::ipv6'
    ]
    
    print("IPv6 验证:")
    for ip in ipv6_list:
        print_result(validate_ipv6(ip), f"'{ip}'")
    
    # 自动检测
    print("自动检测:")
    print_result(validate_ip('192.168.1.1'), 'IPv4 自动检测')
    print_result(validate_ip('2001:db8::1'), 'IPv6 自动检测')


def example_url_validation():
    """URL验证示例"""
    print("=" * 50)
    print("URL验证示例")
    print("=" * 50)
    
    urls = [
        'https://example.com',
        'http://localhost:8080/api',
        'https://sub.domain.com/path?q=value#fragment',
        'ftp://ftp.example.com/files',
        'example.com',
        '://invalid',
    ]
    
    for url in urls:
        print_result(validate_url(url), f"URL '{url}'")
    
    # 自定义协议限制
    print("只允许 HTTPS:")
    print_result(
        validate_url('https://example.com', allowed_schemes=['https']),
        'HTTPS URL'
    )
    print_result(
        validate_url('http://example.com', allowed_schemes=['https']),
        'HTTP URL（不允许）'
    )


def example_json_validation():
    """JSON验证示例"""
    print("=" * 50)
    print("JSON验证示例")
    print("=" * 50)
    
    jsons = [
        '{"name": "张三", "age": 25}',
        '[1, 2, 3, 4]',
        '{"nested": {"key": "value"}}',
        '{invalid json}',
        '{"missing": "quote}',
    ]
    
    for j in jsons:
        print_result(validate_json(j), f"JSON '{j[:30]}...'")
    
    # Schema 验证
    print("Schema 验证:")
    schema = {
        'type': 'object',
        'required': ['name'],
        'properties': {
            'name': {'type': 'string', 'minLength': 2},
            'age': {'type': 'number', 'minimum': 0, 'maximum': 120},
            'email': {'type': 'string', 'pattern': r'^[^@]+@[^@]+$'}
        }
    }
    
    print_result(
        validate_json('{"name": "张三", "age": 25}', schema=schema),
        '符合 schema'
    )
    print_result(
        validate_json('{"age": 25}', schema=schema),
        '缺少必需字段'
    )
    print_result(
        validate_json('{"name": "张三", "age": 150}', schema=schema),
        '超过最大值'
    )


def example_credit_card_validation():
    """信用卡验证示例"""
    print("=" * 50)
    print("信用卡验证示例")
    print("=" * 50)
    
    # 测试卡号（非真实卡号，仅用于测试）
    cards = [
        '4111111111111111',  # Visa 测试卡
        '5500000000000004',  # MasterCard 测试卡
        '378282246310005',   # Amex 测试卡
        '4111-1111-1111-111',  # 格式化
        'invalid',
    ]
    
    for card in cards:
        print_result(validate_credit_card(card), f"卡号 '{card}'")
    
    print("银行卡验证:")
    bank_cards = [
        '6222021234567890',
        '6217234567890123',
    ]
    
    for card in bank_cards:
        print_result(validate_china_bank_card(card), f"银行卡 '{card}'")


def example_name_validation():
    """姓名验证示例"""
    print("=" * 50)
    print("中文姓名验证示例")
    print("=" * 50)
    
    names = [
        '张三',
        '王小明',
        '李四·王五',
        '欧阳修',
        'John',
        '张123',
        ''
    ]
    
    for name in names:
        print_result(validate_chinese_name(name), f"姓名 '{name}'")


def example_password_validation():
    """密码验证示例"""
    print("=" * 50)
    print("密码验证示例")
    print("=" * 50)
    
    passwords = [
        'Password123',
        'VeryStrongPassword2024!',
        'short',
        'nocaps123',
        'NOLOWER123',
        'NoDigitsHere',
    ]
    
    for pwd in passwords:
        result = validate_password(pwd)
        print(f"密码 '{pwd}': {result.message}")
        print(f"  强度: {result.details.get('strength', 'N/A')}")
        print(f"  分数: {result.details.get('score', 'N/A')}")
        print()
    
    # 自定义规则
    print("自定义规则（要求特殊字符）:")
    print_result(
        validate_password('Password123!', require_special=True),
        '包含特殊字符'
    )
    print_result(
        validate_password('Password123', require_special=True),
        '无特殊字符'
    )


def example_phone_validation():
    """电话验证示例"""
    print("=" * 50)
    print("电话号码验证示例")
    print("=" * 50)
    
    phones = [
        '13812345678',      # 手机
        '01012345678',      # 北京座机
        '02112345678',      # 上海座机
        '07551234567',      # 深圳座机
        '4001234567',       # 400客服
        '8001234567',       # 800客服
        'invalid',
    ]
    
    for phone in phones:
        print_result(validate_chinese_phone(phone), f"电话 '{phone}'")


def example_batch_validation():
    """批量验证示例"""
    print("=" * 50)
    print("批量验证示例")
    print("=" * 50)
    
    # 批量验证邮箱
    emails = [
        'test@example.com',
        'invalid-email',
        'user@gmail.com',
        '@missing.com',
        'valid@company.cn'
    ]
    
    print("批量邮箱验证:")
    result = validate_batch(emails, 'email')
    print(f"总数: {result['total']}")
    print(f"有效: {result['valid']}")
    print(f"无效: {result['invalid']}")
    
    for item in result['items']:
        status = "✓" if item['is_valid'] else "✗"
        print(f"  {status} {item['input']}: {item['message']}")
    print()
    
    # 批量验证手机号
    phones = [
        '13812345678',
        'invalid',
        '18612345678',
        '12345678901',
    ]
    
    print("批量手机号验证:")
    result = validate_batch(phones, 'mobile')
    print(f"总数: {result['total']}")
    print(f"有效: {result['valid']}")
    print(f"无效: {result['invalid']}")
    
    for item in result['items']:
        status = "✓" if item['is_valid'] else "✗"
        print(f"  {status} {item['input']}: {item['message']}")
    print()


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("数据验证工具集 (Data Validator) 使用示例")
    print("=" * 60 + "\n")
    
    example_email_validation()
    example_mobile_validation()
    example_id_validation()
    example_ip_validation()
    example_url_validation()
    example_json_validation()
    example_credit_card_validation()
    example_name_validation()
    example_password_validation()
    example_phone_validation()
    example_batch_validation()
    
    print("=" * 60)
    print("示例完成")
    print("=" * 60)


if __name__ == '__main__':
    main()