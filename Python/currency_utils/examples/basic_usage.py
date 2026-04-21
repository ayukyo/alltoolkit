#!/usr/bin/env python
"""
Currency Utils 基本使用示例

演示货币工具库的主要功能
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/AllToolkit/Python/currency_utils')

from mod import (
    Money, ExchangeRates,
    format_money, parse_money,
    convert_money,
    add_taxes, apply_discount, split_amount,
    usd, eur, gbp, jpy, cny,
    get_currency_info, get_all_currencies,
)

def main():
    print("="*50)
    print("Currency Utils 基本使用示例")
    print("="*50)
    
    # 1. 创建 Money 对象
    print("\n1. 创建 Money 对象:")
    price = Money(1234.56, 'USD')
    print(f"   price = Money(1234.56, 'USD')")
    print(f"   金额: {price.amount}")
    print(f"   货币: {price.currency}")
    print(f"   符号: {price.symbol}")
    print(f"   名称: {price.name}")
    
    # 2. 便捷函数
    print("\n2. 便捷函数创建货币:")
    print(f"   usd(100) = {usd(100)}")
    print(f"   eur(100) = {eur(100)}")
    print(f"   gbp(100) = {gbp(100)}")
    print(f"   jpy(1000) = {jpy(1000)}")
    print(f"   cny(100) = {cny(100)}")
    
    # 3. 货币运算
    print("\n3. 货币运算:")
    m1 = usd(100)
    m2 = usd(50)
    print(f"   {m1} + {m2} = {m1 + m2}")
    print(f"   {m1} - {m2} = {m1 - m2}")
    print(f"   {m1} * 2 = {m1 * 2}")
    print(f"   {m1} / 2 = {m1 / 2}")
    
    # 4. 格式化
    print("\n4. 货币格式化:")
    amount = 1234567.89
    print(f"   美式格式: {format_money(amount, 'USD')}")
    print(f"   德式格式: {format_money(amount, 'EUR', locale='de_DE')}")
    print(f"   法式格式: {format_money(amount, 'EUR', locale='fr_FR')}")
    print(f"   日元格式: {format_money(1234567, 'JPY')}")
    print(f"   无符号: {format_money(amount, 'USD', include_symbol=False)}")
    
    # 5. 解析货币字符串
    print("\n5. 解析货币字符串:")
    parsed, currency = parse_money('$1,234.56', 'USD')
    print(f"   parse_money('$1,234.56', 'USD') = ({parsed}, '{currency}')")
    
    # 6. 汇率转换
    print("\n6. 汇率转换:")
    rates = ExchangeRates('USD')
    rates.set_rates({
        'EUR': 0.92,
        'GBP': 0.79,
        'JPY': 151.5,
        'CNY': 7.24,
    })
    
    usd_amount = usd(100)
    print(f"   原金额: {usd_amount}")
    print(f"   转欧元: {rates.convert(usd_amount, to_currency='EUR')}")
    print(f"   转英镑: {rates.convert(usd_amount, to_currency='GBP')}")
    print(f"   日元: {rates.convert(usd_amount, to_currency='JPY')}")
    print(f"   转人民币: {rates.convert(usd_amount, to_currency='CNY')}")
    
    # 7. 简单转换
    print("\n7. 简单货币转换:")
    result = convert_money(100, 'USD', 'CNY', 7.2)
    print(f"   convert_money(100, 'USD', 'CNY', 7.2) = {result}")
    
    # 8. 税费和折扣
    print("\n8. 税费和折扣:")
    price = cny(1000)
    with_tax = add_taxes(price, 0.13)  # 13% 税
    discounted = apply_discount(price, 0.1, 'percent')  # 10% 折扣
    print(f"   原价: {price}")
    print(f"   含税(13%): {with_tax}")
    print(f"   折扣后(10%): {discounted}")
    
    # 9. 分割金额
    print("\n9. 分割金额:")
    parts = split_amount(100, 3, 'USD')
    print(f"   split_amount(100, 3, 'USD'):")
    for i, part in enumerate(parts):
        print(f"     第{i+1}份: {part}")
    total = sum(p.amount for p in parts)
    print(f"     总和验证: {total}")
    
    # 10. 货币信息
    print("\n10. 货币信息:")
    info = get_currency_info('JPY')
    print(f"   JPY 信息:")
    print(f"     名称: {info['name']}")
    print(f"     符号: {info['symbol']}")
    print(f"     小数位: {info['decimals']}")
    print(f"     数字代码: {info['numeric_code']}")
    
    # 11. 支持的货币
    print("\n11. 支持的货币数量:")
    all_currencies = get_all_currencies()
    print(f"   共支持 {len(all_currencies)} 种货币")
    print(f"   主要货币: USD, EUR, GBP, JPY, CNY, AUD, CAD, CHF, HKD, SGD")
    
    print("\n" + "="*50)
    print("示例演示完成")
    print("="*50)


if __name__ == '__main__':
    main()