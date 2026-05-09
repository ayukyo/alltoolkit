"""
IMEI 工具模块使用示例

演示如何使用 imei_utils 模块处理国际移动设备识别码
"""

import sys
sys.path.insert(0, '..')

from mod import (
    validate_imei,
    parse_imei,
    format_imei,
    generate_random_imei,
    generate_batch_imeis,
    get_imei_type,
    compare_imeis,
    extract_tac_info,
    IMEIValidator,
    TEST_TAC_SAMPLE
)


def example_validation():
    """示例：验证 IMEI"""
    print("=" * 50)
    print("IMEI 验证示例")
    print("=" * 50)
    
    # 生成有效 IMEI 用于演示
    valid_imei = generate_random_imei(tac="35905001")
    valid_formatted = f"{valid_imei[:8]}-{valid_imei[8:14]}-{valid_imei[14]}"
    valid_spaced = f"{valid_imei[:8]} {valid_imei[8:14]} {valid_imei[14]}"
    
    # 创建无效 IMEI（修改校验位）
    wrong_checksum = str((int(valid_imei[14]) + 1) % 10)
    invalid_imei = valid_imei[:14] + wrong_checksum
    
    test_imeis = [
        valid_formatted,       # 有效，标准格式
        valid_imei,            # 有效，无分隔符
        valid_spaced,          # 有效，空格分隔
        invalid_imei,          # 无效，校验位错误
        "12345",               # 无效，长度错误
        "imei123456789",       # 无效，包含字母
    ]
    
    for imei in test_imeis:
        result = "有效 ✓" if validate_imei(imei) else "无效 ✗"
        print(f"  {imei:25s} -> {result}")


def example_parsing():
    """示例：解析 IMEI"""
    print("\n" + "=" * 50)
    print("IMEI 解析示例")
    print("=" * 50)
    
    # 使用动态生成的有效 IMEI
    imei = generate_random_imei(tac="35905001")
    imei_formatted = f"{imei[:8]}-{imei[8:14]}-{imei[14]}"
    parsed = parse_imei(imei_formatted)
    
    if parsed:
        print(f"  原始 IMEI: {imei_formatted}")
        print(f"  清理后:    {parsed['imei']}")
        print(f"  TAC:       {parsed['tac']} (Type Allocation Code)")
        print(f"  SNR:       {parsed['snr']} (Serial Number)")
        print(f"  校验位:    {parsed['checksum']}")
        print(f"  格式化:    {parsed['formatted']}")


def example_formatting():
    """示例：格式化 IMEI"""
    print("\n" + "=" * 50)
    print("IMEI 格式化示例")
    print("=" * 50)
    
    # 使用生成的有效 IMEI
    clean_imei = generate_random_imei()
    
    print(f"  原始:     {clean_imei}")
    print(f"  标准格式: {format_imei(clean_imei)}")
    print(f"  空格分隔: {format_imei(clean_imei, separator=' ')}")
    print(f"  点分隔:   {format_imei(clean_imei, separator='.')}")


def example_generation():
    """示例：生成随机 IMEI"""
    print("\n" + "=" * 50)
    print("随机 IMEI 生成示例")
    print("=" * 50)
    
    # 随机生成
    random_imei = generate_random_imei()
    print(f"  随机 IMEI: {random_imei}")
    print(f"  验证结果: {validate_imei(random_imei)}")
    
    # 使用指定 TAC 生成
    custom_tac = "35905001"
    custom_imei = generate_random_imei(tac=custom_tac)
    print(f"\n  自定义 TAC: {custom_tac}")
    print(f"  生成的 IMEI: {custom_imei}")
    print(f"  以 TAC 开头: {custom_imei.startswith(custom_tac)}")
    
    # 批量生成
    batch = generate_batch_imeis(5, tac=custom_tac)
    print(f"\n  批量生成 5 个:")
    for i, imei in enumerate(batch, 1):
        print(f"    {i}. {imei}")


def example_device_type():
    """示例：获取设备类型"""
    print("\n" + "=" * 50)
    print("设备类型判断示例")
    print("=" * 50)
    
    test_tacs = [
        "00123456",  # 测试/假设备
        "35123456",  # 常见移动设备
        "86123456",  # 中国 TAC
        "99123456",  # 测试/保留范围
    ]
    
    for tac in test_tacs:
        device_type = get_imei_type(tac)
        print(f"  TAC {tac} -> {device_type}")


def example_comparison():
    """示例：比较 IMEI"""
    print("\n" + "=" * 50)
    print("IMEI 比较示例")
    print("=" * 50)
    
    # 使用动态生成的 IMEI
    imei = generate_random_imei(tac="35905001")
    imei1 = f"{imei[:8]}-{imei[8:14]}-{imei[14]}"  # 相同 IMEI，不同格式
    imei2 = imei  # 无分隔符格式
    
    imei4 = generate_random_imei(tac="35905001")
    imei5 = generate_random_imei(tac="35905001")
    
    result = compare_imeis(imei1, imei2)
    print(f"  比较 '{imei1}' 和 '{imei2}':")
    print(f"    相同: {result['are_equal']}")
    print(f"    相同 TAC: {result['same_tac']}")
    
    result = compare_imeis(imei4, imei5)
    print(f"\n  比较 '{imei4}' 和 '{imei5}':")
    print(f"    相同: {result['are_equal']}")
    print(f"    相同 TAC: {result['same_tac']}")
    print(f"    同批次: {result['same_manufacturer_batch']}")


def example_tac_info():
    """示例：提取 TAC 信息"""
    print("\n" + "=" * 50)
    print("TAC 信息提取示例")
    print("=" * 50)
    
    test_tacs = ["35209009", "86123456", "01123456"]
    
    for tac in test_tacs:
        info = extract_tac_info(tac)
        print(f"  TAC: {tac}")
        print(f"    RBI: {info.get('rbi', 'N/A')}")
        print(f"    报告体: {info.get('reporting_body', 'N/A')}")
        print(f"    设备类型: {info.get('device_type', 'N/A')}")
        print()


def example_validator_class():
    """示例：使用 IMEIValidator 类"""
    print("=" * 50)
    print("IMEIValidator 类示例")
    print("=" * 50)
    
    # 使用动态生成的有效 IMEI
    imei = generate_random_imei(tac="35905001")
    valid_imei = f"{imei[:8]}-{imei[8:14]}-{imei[14]}"
    validator = IMEIValidator(valid_imei)
    
    print(f"  输入: {valid_imei}")
    print(f"  是否有效: {validator.is_valid}")
    print(f"  TAC: {validator.tac}")
    print(f"  SNR: {validator.snr}")
    print(f"  校验位: {validator.checksum}")
    print(f"  格式化: {validator.formatted}")
    print(f"  字符串: {str(validator)}")
    print(f"  repr: {repr(validator)}")
    
    print("\n  无效 IMEI 示例:")
    invalid_validator = IMEIValidator("invalid-imei")
    print(f"  输入: invalid-imei")
    print(f"  是否有效: {invalid_validator.is_valid}")
    print(f"  repr: {repr(invalid_validator)}")


def example_real_world_scenario():
    """示例：实际应用场景"""
    print("\n" + "=" * 50)
    print("实际应用场景")
    print("=" * 50)
    
    print("\n场景 1: 设备注册验证")
    print("-" * 40)
    # 使用动态生成的有效 IMEI
    imei = generate_random_imei(tac="35905001")
    user_input = f"{imei[:8]}-{imei[8:14]}-{imei[14]}"
    if validate_imei(user_input):
        parsed = parse_imei(user_input)
        print(f"  IMEI 有效！设备信息:")
        print(f"    TAC (型号): {parsed['tac']}")
        print(f"    SNR (序列): {parsed['snr']}")
    else:
        print("  IMEI 无效，请检查输入")
    
    print("\n场景 2: 测试数据生成")
    print("-" * 40)
    test_tac = "35905001"
    test_imeis = generate_batch_imeis(3, tac=test_tac)
    print(f"  生成 {len(test_imeis)} 个测试用 IMEI:")
    for imei in test_imeis:
        print(f"    {imei}")
    
    print("\n场景 3: 批量验证")
    print("-" * 40)
    # 生成混合批次
    valid1 = generate_random_imei()
    valid2 = generate_random_imei()
    invalid1 = valid1[:14] + str((int(valid1[14]) + 1) % 10)  # 错误校验位
    
    batch = [
        valid1,       # 有效
        invalid1,     # 无效（校验位错误）
        valid2,       # 有效
        "invalid",    # 无效
    ]
    
    valid_count = sum(1 for imei in batch if validate_imei(imei))
    print(f"  总数: {len(batch)}")
    print(f"  有效: {valid_count}")
    print(f"  无效: {len(batch) - valid_count}")
    
    print("\n场景 4: 设备溯源")
    print("-" * 40)
    device_imei = generate_random_imei(tac="86123456")
    info = extract_tac_info(device_imei[:8])
    print(f"  IMEI: {device_imei}")
    print(f"  来源: {info.get('reporting_body', '未知')}")


def main():
    """主函数"""
    example_validation()
    example_parsing()
    example_formatting()
    example_generation()
    example_device_type()
    example_comparison()
    example_tac_info()
    example_validator_class()
    example_real_world_scenario()
    
    print("\n" + "=" * 50)
    print("示例完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()