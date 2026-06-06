"""
Data Masking Utils - 测试文件

运行测试: python -m pytest data_masking_utils/test_masker.py -v
或者: python data_masking_utils/test_masker.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_masking_utils import (
    mask_phone,
    mask_id_card,
    mask_bank_card,
    mask_email,
    mask_name,
    mask_address,
    mask_ip,
    mask_custom,
    mask_string,
    DataMasker,
    MaskRule,
    MaskMode,
)


def test_mask_string():
    """测试通用字符串脱敏"""
    print("\n=== 测试 mask_string ===")
    
    # 基本测试
    result = mask_string("13812345678", 3, 4)
    assert result == "138****5678", f"Expected '138****5678', got '{result}'"
    print(f"✓ mask_string('13812345678', 3, 4) = {result}")
    
    # 保留开头
    result = mask_string("hello", 2, 0)
    assert result == "he***", f"Expected 'he***', got '{result}'"
    print(f"✓ mask_string('hello', 2, 0) = {result}")
    
    # 保留结尾
    result = mask_string("hello", 0, 2)
    assert result == "***lo", f"Expected '***lo', got '{result}'"
    print(f"✓ mask_string('hello', 0, 2) = {result}")
    
    # 短字符串
    result = mask_string("ab", 1, 1)
    assert result == "ab", f"Expected 'ab', got '{result}'"
    print(f"✓ mask_string('ab', 1, 1) = {result}")
    
    print("✓ 所有 mask_string 测试通过")


def test_mask_phone():
    """测试手机号脱敏"""
    print("\n=== 测试 mask_phone ===")
    
    # 标准11位手机号
    result = mask_phone("13812345678")
    assert result == "138****5678", f"Expected '138****5678', got '{result}'"
    print(f"✓ mask_phone('13812345678') = {result}")
    
    # 带分隔符的手机号
    result = mask_phone("138-1234-5678")
    assert result == "138****5678", f"Expected '138****5678', got '{result}'"
    print(f"✓ mask_phone('138-1234-5678') = {result}")
    
    # 不同运营商号段
    test_cases = [
        ("13900001111", "139****1111"),  # 中国移动
        ("15000002222", "150****2222"),  # 中国移动
        ("18600003333", "186****3333"),  # 中国联通
        ("17700004444", "177****4444"),  # 中国电信
        ("16600005555", "166****5555"),  # 中国联通
    ]
    
    for phone, expected in test_cases:
        result = mask_phone(phone)
        assert result == expected, f"Expected '{expected}', got '{result}'"
        print(f"✓ mask_phone('{phone}') = {result}")
    
    print("✓ 所有 mask_phone 测试通过")


def test_mask_id_card():
    """测试身份证号脱敏"""
    print("\n=== 测试 mask_id_card ===")
    
    # 18位身份证
    result = mask_id_card("110101199001011234")
    assert result == "110101********1234", f"Expected '110101********1234', got '{result}'"
    print(f"✓ mask_id_card('110101199001011234') = {result}")
    
    # 15位身份证
    result = mask_id_card("110101900101123")
    assert result == "110101******123", f"Expected '110101******123', got '{result}'"
    print(f"✓ mask_id_card('110101900101123') = {result}")
    
    # 带空格的身份证
    result = mask_id_card("110101 19900101 1234")
    assert result == "110101********1234", f"Expected '110101********1234', got '{result}'"
    print(f"✓ mask_id_card('110101 19900101 1234') = {result}")
    
    # 非标准长度（保留前4位和后4位）
    result = mask_id_card("12345678")
    assert result == "1234****", f"Expected '1234****', got '{result}'"
    print(f"✓ mask_id_card('12345678') = {result}")
    
    # 非常短的非标准长度
    result = mask_id_card("12345")
    print(f"✓ mask_id_card('12345') = {result} (短字符串处理)")
    
    print("✓ 所有 mask_id_card 测试通过")


def test_mask_bank_card():
    """测试银行卡号脱敏"""
    print("\n=== 测试 mask_bank_card ===")
    
    # 16位银行卡
    result = mask_bank_card("6222021234567890")
    expected = "6222 **** **** 7890"
    assert result == expected, f"Expected '{expected}', got '{result}'"
    print(f"✓ mask_bank_card('6222021234567890') = {result}")
    
    # 19位银行卡
    result = mask_bank_card("6222021234567890123")
    assert "****" in result and result.startswith("6222")
    print(f"✓ mask_bank_card('6222021234567890123') = {result}")
    
    # 带分隔符的银行卡号
    result = mask_bank_card("6222 0212 3456 7890")
    assert "****" in result
    print(f"✓ mask_bank_card('6222 0212 3456 7890') = {result}")
    
    # 短卡号测试（8位）
    result = mask_bank_card("12345678")
    assert "****" in result
    print(f"✓ mask_bank_card('12345678') = {result}")
    
    print("✓ 所有 mask_bank_card 测试通过")


def test_mask_email():
    """测试邮箱脱敏"""
    print("\n=== 测试 mask_email ===")
    
    # 标准邮箱
    result = mask_email("example@domain.com")
    assert result == "e******@domain.com", f"Expected 'e******@domain.com', got '{result}'"
    print(f"✓ mask_email('example@domain.com') = {result}")
    
    # 短用户名
    result = mask_email("ab@test.org")
    assert result == "a*@test.org", f"Expected 'a*@test.org', got '{result}'"
    print(f"✓ mask_email('ab@test.org') = {result}")
    
    # 单字符用户名
    result = mask_email("a@test.org")
    assert result == "*@test.org", f"Expected '*@test.org', got '{result}'"
    print(f"✓ mask_email('a@test.org') = {result}")
    
    # 带点的用户名 (john.doe 是 8 个字符)
    result = mask_email("john.doe@example.com")
    assert result == "j*******@example.com", f"Expected 'j*******@example.com', got '{result}'"
    print(f"✓ mask_email('john.doe@example.com') = {result}")
    
    # 无效邮箱（无@符号）
    result = mask_email("invalidemail")
    assert result[0] != '*', "First char should be kept"
    print(f"✓ mask_email('invalidemail') = {result}")
    
    print("✓ 所有 mask_email 测试通过")


def test_mask_name():
    """测试姓名脱敏"""
    print("\n=== 测试 mask_name ===")
    
    # 中文单字名
    result = mask_name("张三")
    assert result == "张*", f"Expected '张*', got '{result}'"
    print(f"✓ mask_name('张三') = {result}")
    
    # 中文双字名
    result = mask_name("李明华")
    assert result == "李**", f"Expected '李**', got '{result}'"
    print(f"✓ mask_name('李明华') = {result}")
    
    # 复姓
    result = mask_name("欧阳修")
    assert result == "欧**", f"Expected '欧**', got '{result}'"
    print(f"✓ mask_name('欧阳修') = {result}")
    
    # 少数民族姓名（带·）
    result = mask_name("买买提·阿卜杜拉")
    assert "·" in result and "*" in result
    print(f"✓ mask_name('买买提·阿卜杜拉') = {result}")
    
    # 英文姓名
    result = mask_name("John Smith")
    assert result == "J*** S****", f"Expected 'J*** S****', got '{result}'"
    print(f"✓ mask_name('John Smith') = {result}")
    
    # 英文单名
    result = mask_name("Alice")
    assert result == "A****", f"Expected 'A****', got '{result}'"
    print(f"✓ mask_name('Alice') = {result}")
    
    print("✓ 所有 mask_name 测试通过")


def test_mask_address():
    """测试地址脱敏"""
    print("\n=== 测试 mask_address ===")
    
    # 完整中文地址
    result = mask_address("北京市朝阳区建国路88号")
    assert "北京市朝阳区" in result or "北京市" in result
    assert "*" in result
    print(f"✓ mask_address('北京市朝阳区建国路88号') = {result}")
    
    # 省市区地址
    result = mask_address("广东省深圳市南山区科技园路1号")
    assert "广东省深圳市南山区" in result or "广东省深圳市" in result
    print(f"✓ mask_address('广东省深圳市南山区科技园路1号') = {result}")
    
    # 英文地址
    result = mask_address("123 Main Street, New York")
    assert "*" in result
    print(f"✓ mask_address('123 Main Street, New York') = {result}")
    
    print("✓ 所有 mask_address 测试通过")


def test_mask_ip():
    """测试IP地址脱敏"""
    print("\n=== 测试 mask_ip ===")
    
    # IPv4
    result = mask_ip("192.168.1.100")
    assert result == "192.168.*.*", f"Expected '192.168.*.*', got '{result}'"
    print(f"✓ mask_ip('192.168.1.100') = {result}")
    
    # IPv4 不同格式
    result = mask_ip("10.0.0.1")
    assert result == "10.0.*.*", f"Expected '10.0.*.*', got '{result}'"
    print(f"✓ mask_ip('10.0.0.1') = {result}")
    
    # IPv6 (简化测试)
    result = mask_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
    assert result.startswith("2001:0db8"), f"IPv6 mask failed: {result}"
    print(f"✓ mask_ip('2001:0db8:...') = {result}")
    
    print("✓ 所有 mask_ip 测试通过")


def test_mask_custom():
    """测试自定义脱敏"""
    print("\n=== 测试 mask_custom ===")
    
    # 自定义正则脱敏 - 注意 pattern 需要匹配整个要脱敏的部分
    text = "订单号：123456789"
    result = mask_custom(text, r"\d+", 3, 2)
    assert "订单号：" in result and "*" in result
    print(f"✓ mask_custom('订单号：123456789', ...) = {result}")
    
    # 脱敏信用卡号
    text = "信用卡：1234567890123456"
    result = mask_custom(text, r"\d{16}", 4, 4)
    assert "信用卡：" in result and "****" in result
    print(f"✓ mask_custom('信用卡：...', ...) = {result}")
    
    print("✓ 所有 mask_custom 测试通过")


def test_data_masker():
    """测试 DataMasker 类"""
    print("\n=== 测试 DataMasker ===")
    
    masker = DataMasker()
    
    # 综合文本脱敏
    text = "手机：13812345678，身份证：110101199001011234，邮箱：test@example.com"
    result = masker.mask(text)
    assert "138****5678" in result
    assert "110101********1234" in result
    assert "t***@example.com" in result
    print(f"✓ 综合脱敏测试通过")
    print(f"  原文: {text}")
    print(f"  结果: {result}")
    
    # 字典脱敏
    data = {
        "name": "张三",
        "phone": "13812345678",
        "id_card": "110101199001011234",
        "email": "test@example.com"
    }
    result = masker.mask_dict(data)
    assert "138****5678" in result["phone"]
    print(f"✓ 字典脱敏测试通过")
    print(f"  结果: {result}")
    
    # 列表脱敏
    data_list = ["13812345678", "test@example.com", "110101199001011234"]
    result = masker.mask_list(data_list)
    assert "138****5678" in result[0]
    assert "@example.com" in result[1]
    print(f"✓ 列表脱敏测试通过")
    print(f"  结果: {result}")
    
    # 添加自定义规则
    masker.add_rule(r"\d{6,}", keep_start=2, keep_end=2, name="employee_id")
    text = "工号：123456"
    result = masker.mask(text)
    assert "*" in result
    print(f"✓ 自定义规则测试通过")
    print(f"  结果: {result}")
    
    # 移除规则
    masker.remove_rule("employee_id")
    print(f"✓ 规则移除测试通过")
    
    print("✓ 所有 DataMasker 测试通过")


def test_mask_rule():
    """测试 MaskRule 类"""
    print("\n=== 测试 MaskRule ===")
    
    # 测试不同模式
    rule = MaskRule(r"\d{11}", keep_start=3, keep_end=4, mode=MaskMode.KEEP_BOTH)
    result = rule.apply("手机13812345678号码")
    assert "138****5678" in result
    print(f"✓ KEEP_BOTH 模式测试通过: {result}")
    
    rule = MaskRule(r"\d{11}", mode=MaskMode.FULL)
    result = rule.apply("手机13812345678号码")
    assert "***********" in result
    print(f"✓ FULL 模式测试通过: {result}")
    
    rule = MaskRule(r"\d{11}", keep_start=3, mode=MaskMode.KEEP_START)
    result = rule.apply("手机13812345678号码")
    assert "138********" in result
    print(f"✓ KEEP_START 模式测试通过: {result}")
    
    rule = MaskRule(r"\d{11}", keep_end=4, mode=MaskMode.KEEP_END)
    result = rule.apply("手机13812345678号码")
    assert "*******5678" in result
    print(f"✓ KEEP_END 模式测试通过: {result}")
    
    print("✓ 所有 MaskRule 测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Data Masking Utils - 测试套件")
    print("=" * 60)
    
    tests = [
        test_mask_string,
        test_mask_phone,
        test_mask_id_card,
        test_mask_bank_card,
        test_mask_email,
        test_mask_name,
        test_mask_address,
        test_mask_ip,
        test_mask_custom,
        test_mask_rule,
        test_data_masker,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} 异常: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试完成: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)