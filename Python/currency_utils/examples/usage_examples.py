"""
Currency Utils 使用示例
"""

from currency_utils import (
    Currency, validate_code, get_currency_info, format_currency,
    parse_currency, convert, exchange, get_rate, round_currency,
    format_multi, compare, calculate_fees, cents_to_amount,
    amount_to_cents, list_currencies, get_supported_currencies
)


def basic_usage():
    """基本用法"""
    print("=" * 50)
    print("基本用法")
    print("=" * 50)
    
    # 创建 Currency 对象
    price = Currency(1234.567, "USD")
    print(f"金额: {price.amount}")
    print(f"符号: {price.symbol}")
    print(f"名称: {price.name}")
    print(f"格式化: {price.formatted()}")
    
    # 算术运算
    price2 = Currency(100, "USD")
    print(f"\n加法: {price + price2}")
    print(f"减法: {price - price2}")
    print(f"乘法: {price * 2}")
    print(f"除法: {price / 2}")
    
    # 比较
    print(f"\nprice > price2: {price > price2}")
    print(f"price == price2: {price == price2}")


def formatting_and_parsing():
    """格式化和解析"""
    print("\n" + "=" * 50)
    print("格式化和解析")
    print("=" * 50)
    
    # 格式化
    amounts = [1234.567, 1000000, 0.99, 12345678.90]
    codes = ["USD", "EUR", "JPY", "CNY"]
    
    for amount in amounts:
        print(f"\n金额 {amount}:")
        for code in codes:
            print(f"  {code}: {format_currency(amount, code)}")
    
    # 解析
    print("\n解析货币字符串:")
    test_strings = [
        "$1,234.56",
        "€1.234,56",
        "¥1234",
        "1234.56 USD",
        "-1,234.56",
        "USD 1000",
        "£1,234.56",
        "1,234,567.89",
    ]
    
    for s in test_strings:
        try:
            amount, code = parse_currency(s)
            print(f"  '{s}' -> {amount} {code}")
        except Exception as e:
            print(f"  '{s}' -> 错误: {e}")


def currency_conversion():
    """货币转换"""
    print("\n" + "=" * 50)
    print("货币转换")
    print("=" * 50)
    
    # 基础转换
    print("\n汇率转换示例 (1000 USD):")
    target_codes = ["EUR", "GBP", "JPY", "CNY", "KRW"]
    for code in target_codes:
        result = convert(1000, "USD", code)
        print(f"  USD -> {code}: {result}")
    
    # 获取汇率
    print("\n当前汇率:")
    print(f"  1 USD = {get_rate('USD', 'EUR'):.4f} EUR")
    print(f"  1 EUR = {get_rate('EUR', 'USD'):.4f} USD")
    print(f"  1 USD = {get_rate('USD', 'JPY'):.2f} JPY")
    print(f"  1 CNY = {get_rate('CNY', 'USD'):.4f} USD")
    
    # 使用 exchange 函数（返回 Currency 对象）
    print("\n使用 exchange 函数:")
    for code in ["EUR", "GBP", "JPY"]:
        result = exchange(1000, "USD", code)
        print(f"  1000 USD -> {result}")


def multi_currency_display():
    """多币种显示"""
    print("\n" + "=" * 50)
    print("多币种显示")
    print("=" * 50)
    
    # 多币种格式化
    print("\n1000 USD 转换为多币种:")
    multi = format_multi(1000, "USD", ["USD", "EUR", "GBP", "CNY", "JPY", "KRW"])
    for code, formatted in multi.items():
        print(f"  {code}: {formatted}")
    
    # 自定义目标货币
    print("\n自定义目标货币列表:")
    multi = format_multi(500, "EUR", ["USD", "CNY", "JPY"])
    for code, formatted in multi.items():
        print(f"  {code}: {formatted}")


def rounding_and_cents():
    """舍入和最小单位转换"""
    print("\n" + "=" * 50)
    print("舍入和最小单位转换")
    print("=" * 50)
    
    # 货币规则舍入
    print("\n货币规则舍入示例:")
    amounts = [100.555, 100.554, 100.556]
    codes = ["USD", "EUR", "JPY"]
    
    for code in codes:
        print(f"\n  {code}:")
        for amount in amounts:
            rounded = round_currency(amount, code, "HALF_UP")
            print(f"    {amount} -> {rounded}")
    
    # 最小单位转换
    print("\n最小单位转换 (分/元):")
    test_cases = [
        (10050, "USD"),
        (123456, "JPY"),
        (999990, "KRW"),
    ]
    
    for cents, code in test_cases:
        amount = cents_to_amount(cents, code)
        back = amount_to_cents(amount, code)
        print(f"  {cents} cents ({code}) = {amount} = {back} cents")


def fee_calculation():
    """手续费计算"""
    print("\n" + "=" * 50)
    print("手续费计算")
    print("=" * 50)
    
    # 基础手续费
    print("\n基础手续费计算:")
    result = calculate_fees(1000, "USD", fee_percent=0.0325, fee_fixed=1.50)
    print(f"  订单金额: ${result['gross_amount']}")
    print(f"  百分比费 (3.25%): ${result['fee_percent']}")
    print(f"  固定费: ${result['fee_fixed']}")
    print(f"  总手续费: ${result['total_fee']}")
    print(f"  净额: ${result['net_amount']}")
    
    # 带最小/最大限制
    print("\n带限制的手续费:")
    cases = [
        {"amount": 50, "fee_percent": 0.03, "min_fee": 2},
        {"amount": 5000, "fee_percent": 0.03, "max_fee": 100},
        {"amount": 100, "fee_percent": 0.01, "fee_fixed": 5, "min_fee": 10, "max_fee": 50},
    ]
    
    for case in cases:
        result = calculate_fees(
            case["amount"],
            "USD",
            fee_percent=case["fee_percent"],
            fee_fixed=case.get("fee_fixed", 0),
            min_fee=case.get("min_fee", 0),
            max_fee=case.get("max_fee")
        )
        print(f"  金额 ${case['amount']}: 手续费 ${result['total_fee']} (净额 ${result['net_amount']})")


def currency_comparison():
    """货币比较"""
    print("\n" + "=" * 50)
    print("货币比较")
    print("=" * 50)
    
    cases = [
        (Currency(100, "USD"), Currency(100, "USD")),
        (Currency(100, "USD"), Currency(92, "EUR")),
        ("$150", Currency(120, "USD")),
        (1000, "€900 EUR"),
    ]
    
    print("\n货币比较示例:")
    for a, b in cases:
        result = compare(a, b)
        relation = {1: ">", 0: "==", -1: "<"}[result]
        print(f"  {a} vs {b}: {relation}")


def currency_validation():
    """货币验证和信息查询"""
    print("\n" + "=" * 50)
    print("货币验证和信息查询")
    print("=" * 50)
    
    # 验证代码
    print("\n代码验证:")
    test_codes = ["USD", "eur", "ABC", "CNY", "INVALID"]
    for code in test_codes:
        valid = validate_code(code)
        print(f"  {code}: {'有效' if valid else '无效'}")
    
    # 获取货币信息
    print("\n货币信息:")
    for code in ["USD", "EUR", "JPY", "CNY"]:
        info = get_currency_info(code)
        if info:
            print(f"  {code}: {info['name']}, 符号: {info['symbol']}, 小数位: {info['decimals']}")
    
    # 列出所有支持的货币
    print(f"\n所有支持的货币 ({len(list_currencies())} 种):")
    currencies = list_currencies()
    for i in range(0, len(currencies), 6):
        row = currencies[i:i+6]
        print("  " + ", ".join(row))


def main():
    """运行所有示例"""
    basic_usage()
    formatting_and_parsing()
    currency_conversion()
    multi_currency_display()
    rounding_and_cents()
    fee_calculation()
    currency_comparison()
    currency_validation()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()