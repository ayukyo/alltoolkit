"""
物流追踪号码工具使用示例

本示例演示如何使用 tracking_number_utils 模块：
1. 验证追踪号码
2. 识别承运商
3. 获取追踪链接
4. 批量处理
5. 从文本中提取追踪号码
"""

import sys
sys.path.insert(0, '..')

from mod import (
    TrackingNumberUtils,
    Carrier,
    validate,
    identify_carrier,
    get_tracking_url,
    extract_from_text
)


def example_basic_validation():
    """基础验证示例"""
    print("=" * 60)
    print("1. 基础验证示例")
    print("=" * 60)

    # UPS 追踪号码
    result = validate("1Z999AA10123456784")
    print(f"\nUPS追踪号码: 1Z999AA10123456784")
    print(f"  有效: {result.is_valid}")
    print(f"  承运商: {result.carrier.value}")
    print(f"  标准化: {result.normalized}")
    print(f"  追踪链接: {result.tracking_url}")

    # 顺丰追踪号码
    result = validate("SF1234567890123")
    print(f"\n顺丰追踪号码: SF1234567890123")
    print(f"  有效: {result.is_valid}")
    print(f"  承运商: {result.carrier.value}")
    print(f"  标准化: {result.normalized}")
    print(f"  追踪链接: {result.tracking_url}")


def example_carrier_identification():
    """承运商识别示例"""
    print("\n" + "=" * 60)
    print("2. 承运商识别示例")
    print("=" * 60)

    test_numbers = [
        ("1Z999AA10123456784", "UPS"),
        ("123456789012", "FedEx"),
        ("9400111899223336117112", "USPS"),
        ("1234567890", "DHL"),
        ("SF1234567890123", "顺丰"),
        ("EA123456789CN", "中国邮政EMS"),
        ("JD123456789012", "京东物流"),
        ("712345678901", "中通快递"),
        ("JT1234567890123", "极兔速递"),
    ]

    print("\n识别结果:")
    for number, description in test_numbers:
        carrier = identify_carrier(number)
        print(f"  {description:15} -> {carrier.value}")


def example_tracking_urls():
    """获取追踪链接示例"""
    print("\n" + "=" * 60)
    print("3. 获取追踪链接示例")
    print("=" * 60)

    tracking_numbers = [
        "1Z999AA10123456784",  # UPS
        "SF1234567890123",    # 顺丰
        "EA123456789CN",      # 中国邮政
        "JD123456789012",     # 京东
    ]

    print("\n追踪链接:")
    for number in tracking_numbers:
        url = get_tracking_url(number)
        carrier = identify_carrier(number)
        if url:
            print(f"  {carrier.value:15} -> {url}")


def example_batch_validation():
    """批量验证示例"""
    print("\n" + "=" * 60)
    print("4. 批量验证示例")
    print("=" * 60)

    tracking_numbers = [
        "1Z999AA10123456784",  # UPS
        "SF1234567890123",     # 顺丰
        "EA123456789CN",       # 中国邮政EMS
        "INVALID_NUMBER",      # 无效
        "JD123456789012",      # 京东
        "",                    # 空
    ]

    print("\n批量验证结果:")
    results = TrackingNumberUtils.batch_validate(tracking_numbers)
    for num, result in zip(tracking_numbers, results):
        status = "✓ 有效" if result.is_valid else "✗ 无效"
        carrier_name = result.carrier.value if result.is_valid else "-"
        print(f"  {num or '(空)':25} {status:10} {carrier_name}")


def example_extract_from_text():
    """从文本提取追踪号码示例"""
    print("\n" + "=" * 60)
    print("5. 从文本提取追踪号码示例")
    print("=" * 60)

    email_text = """
    尊敬的客户：

    您的订单已发货，请注意查收。

    物流信息：
    - UPS国际件：1Z999AA10123456784
    - 顺丰快递：SF1234567890123
    - 京东物流：JD123456789012

    如有问题请联系客服。
    """

    print("\n原始文本:")
    print(email_text)

    results = extract_from_text(email_text)
    print("提取到的追踪号码:")
    for tracking_num, carrier in results:
        print(f"  {tracking_num:25} ({carrier.value})")


def example_format_normalization():
    """格式标准化示例"""
    print("\n" + "=" * 60)
    print("6. 格式标准化示例")
    print("=" * 60)

    raw_numbers = [
        "1z 999 aa 10 1234 5678 90",  # 带空格
        "SF-1234567890-123",          # 带连字符
        "sf1234567890123",            # 小写
        "  EA123456789CN  ",          # 带前后空格
    ]

    print("\n标准化结果:")
    for raw in raw_numbers:
        normalized = TrackingNumberUtils.normalize(raw)
        carrier = identify_carrier(normalized)
        print(f"  '{raw:30}' -> '{normalized}' ({carrier.value})")


def example_detailed_validation():
    """详细验证结果示例"""
    print("\n" + "=" * 60)
    print("7. 详细验证结果示例")
    print("=" * 60)

    test_numbers = [
        "SF1234567890123",    # 有效顺丰
        "EA123456789CN",      # 有效EMS
        "INVALID",            # 无效格式
    ]

    print("\n详细验证信息:")
    for number in test_numbers:
        result = validate(number)
        print(f"\n追踪号码: {number}")
        print(f"  是否有效: {result.is_valid}")
        print(f"  承运商: {result.carrier.value}")
        print(f"  标准化号码: {result.normalized}")
        print(f"  校验位有效: {result.checksum_valid}")
        print(f"  追踪链接: {result.tracking_url or '无'}")
        print(f"  消息: {result.message}")


def example_china_couriers():
    """中国快递公司示例"""
    print("\n" + "=" * 60)
    print("8. 中国快递公司识别示例")
    print("=" * 60)

    china_tracking_numbers = [
        ("SF1234567890123", "顺丰速运"),
        ("EA123456789CN", "中国邮政"),
        ("PA123456789012", "中国邮政"),  # PA+12位数字=14位
        ("JD123456789012", "京东物流"),
        ("JDX123456789012", "京东物流"),
        ("YT12345678901", "圆通速递"),
        ("712345678901", "中通快递"),
        ("ZT12345678901", "中通快递"),
        ("7123456789012", "申通快递"),
        ("ST12345678901", "申通快递"),
        ("1123456789012", "韵达快递"),
        ("YD12345678901", "韵达快递"),
        ("JT1234567890123", "极兔速递"),
    ]

    print("\n中国快递识别结果:")
    for number, expected in china_tracking_numbers:
        carrier = identify_carrier(number)
        match = "✓" if carrier.value == expected else "✗"
        print(f"  {number:20} -> {carrier.value:15} {match}")


def main():
    """运行所有示例"""
    example_basic_validation()
    example_carrier_identification()
    example_tracking_urls()
    example_batch_validation()
    example_extract_from_text()
    example_format_normalization()
    example_detailed_validation()
    example_china_couriers()

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()