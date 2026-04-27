#!/usr/bin/env python
"""
Currency Utils 测试文件

测试货币工具库的所有功能
"""

import sys
import os
sys.path.insert(0, '/home/admin/.openclaw/workspace/AllToolkit/Python/currency_utils')

from decimal import Decimal
from mod import (
    # 类
    Money, ExchangeRates,
    # 异常
    CurrencyError, InvalidCurrencyError, InvalidAmountError,
    # 验证函数
    is_valid_currency, is_valid_numeric_code, get_currency_info,
    get_currencies_by_symbol, get_all_currencies, get_major_currencies,
    # 格式化函数
    format_money, parse_money, format_number,
    # 转换函数
    convert_money,
    # 计算函数
    add_taxes, apply_discount, split_amount, compare_amounts,
    percentage_of, is_zero, is_negative, is_positive,
    # 便捷函数
    money, usd, eur, gbp, jpy, cny,
    # 数据
    CURRENCIES, LOCALE_FORMATS,
)

def test_money_creation():
    """测试 Money 创建"""
    print("测试 Money 创建...")
    
    # 整数
    m1 = Money(100, 'USD')
    assert m1.amount == Decimal('100')
    assert m1.currency == 'USD'
    
    # 浮点数
    m2 = Money(123.45, 'EUR')
    assert m2.amount == Decimal('123.45')
    
    # 字符串
    m3 = Money('1000.50', 'GBP')
    assert m3.amount == Decimal('1000.50')
    
    # Decimal
    m4 = Money(Decimal('99.99'), 'JPY')
    assert m4.amount == Decimal('99.99')
    
    # 货币信息
    assert m1.symbol == '$'
    assert m1.name == 'US Dollar'
    assert m1.decimals == 2
    assert m1.numeric_code == '840'
    
    # 日元小数位为 0
    jpy_money = Money(1000, 'JPY')
    assert jpy_money.decimals == 0
    
    print("  ✓ Money 创建测试通过")


def test_money_invalid():
    """测试无效 Money 创建"""
    print("测试无效 Money 创建...")
    
    # 无效货币代码
    try:
        Money(100, 'XXX')
        assert False, "应该抛出异常"
    except InvalidCurrencyError:
        pass
    
    # 无效金额
    try:
        Money('abc', 'USD')
        assert False, "应该抛出异常"
    except InvalidAmountError:
        pass
    
    print("  ✓ 无效 Money 创建测试通过")


def test_money_operations():
    """测试 Money 运算"""
    print("测试 Money 运算...")
    
    m1 = Money(100, 'USD')
    m2 = Money(50, 'USD')
    
    # 加法
    assert (m1 + m2).amount == Decimal('150')
    
    # 减法
    assert (m1 - m2).amount == Decimal('50')
    
    # 乘法
    assert (m1 * 2).amount == Decimal('200')
    assert (2 * m1).amount == Decimal('200')
    assert (m1 * 1.5).amount == Decimal('150')
    
    # 除法
    assert (m1 / 2).amount == Decimal('50')
    assert (m1 // 3).amount == Decimal('33')
    
    # 取模
    assert (m1 % 30).amount == Decimal('10')
    
    # 负数
    neg = -m1
    assert neg.amount == Decimal('-100')
    
    # 绝对值
    neg_money = Money(-50, 'USD')
    assert abs(neg_money).amount == Decimal('50')
    
    # 比较
    assert m1 > m2
    assert m1 >= m2
    assert m2 < m1
    assert m2 <= m1
    assert m1 == Money(100, 'USD')
    assert m1 != m2
    
    # 布尔值
    assert bool(m1) is True
    assert bool(Money(0, 'USD')) is False
    
    print("  ✓ Money 运算测试通过")


def test_money_mismatch():
    """测试货币不匹配"""
    print("测试货币不匹配...")
    
    m1 = Money(100, 'USD')
    m2 = Money(50, 'EUR')
    
    # 不同货币不能相加
    try:
        m1 + m2
        assert False, "应该抛出异常"
    except CurrencyError:
        pass
    
    # 不同货币不能比较
    try:
        m1 > m2
        assert False, "应该抛出异常"
    except CurrencyError:
        pass
    
    print("  ✓ 货币不匹配测试通过")


def test_money_rounding():
    """测试 Money 舍入"""
    print("测试 Money 舍入...")
    
    # USD 精度为 2
    m1 = Money(123.456, 'USD')
    rounded = m1.round()
    assert rounded.amount == Decimal('123.46')
    
    # JPY 精度为 0
    m2 = Money(123.4, 'JPY')
    rounded = m2.round()
    assert rounded.amount == Decimal('123')
    
    # BTC 精度为 8
    m3 = Money('0.123456789', 'BTC')
    rounded = m3.round()
    assert rounded.amount == Decimal('0.12345679')
    
    print("  ✓ Money 舍入测试通过")


def test_format_money():
    """测试货币格式化"""
    print("测试货币格式化...")
    
    # 美式格式
    assert format_money(1234.56, 'USD') == '$1,234.56'
    assert format_money(1234, 'USD') == '$1,234.00'
    
    # 无符号格式
    assert format_money(1234.56, 'USD', include_symbol=False) == '1,234.56'
    
    # 含代码格式
    assert format_money(1234.56, 'USD', include_code=True) == '$1,234.56 USD'
    
    # 德式格式
    assert format_money(1234.56, 'EUR', locale='de_DE') == '1.234,56 €'
    
    # 法式格式
    assert format_money(1234.56, 'EUR', locale='fr_FR') == '1 234,56 €'
    
    # 日元（无小数）
    assert format_money(1234, 'JPY') == '¥1,234'
    
    # 大数字
    assert format_money(1234567.89, 'USD') == '$1,234,567.89'
    
    # 负数
    assert format_money(-1234.56, 'USD') == '-$1,234.56'
    
    # 韩元（无小数）
    assert format_money(1234567, 'KRW') == '₩1,234,567'
    
    print("  ✓ 货币格式化测试通过")


def test_parse_money():
    """测试货币解析"""
    print("测试货币解析...")
    
    # 带符号的字符串
    amount, currency = parse_money('$1,234.56', 'USD')
    assert amount == Decimal('1234.56')
    assert currency == 'USD'
    
    # 无符号的字符串
    amount, currency = parse_money('1,234.56', 'USD')
    assert amount == Decimal('1234.56')
    
    # 德式格式
    amount, currency = parse_money('1.234,56 €', locale='de_DE')
    assert amount == Decimal('1234.56')
    assert currency == 'EUR'
    
    # 日元
    amount, currency = parse_money('¥1,234', 'JPY')
    assert amount == Decimal('1234')
    
    print("  ✓ 货币解析测试通过")


def test_format_number():
    """测试数字格式化"""
    print("测试数字格式化...")
    
    # 美式格式
    assert format_number(1234.5678, 2) == '1,234.57'
    
    # 德式格式
    assert format_number(1234.5678, 2, 'de_DE') == '1.234,57'
    
    # 无小数
    assert format_number(1234.5, 0) == '1,235'
    
    # 负数
    assert format_number(-1234.56, 2) == '-1,234.56'
    
    print("  ✓ 数字格式化测试通过")


def test_currency_validation():
    """测试货币验证"""
    print("测试货币验证...")
    
    # 有效货币
    assert is_valid_currency('USD') is True
    assert is_valid_currency('EUR') is True
    assert is_valid_currency('JPY') is True
    assert is_valid_currency('CNY') is True
    
    # 无效货币
    assert is_valid_currency('XXX') is False
    assert is_valid_currency('ABC') is False
    
    # 数字代码
    assert is_valid_numeric_code('840') is True  # USD
    assert is_valid_numeric_code('978') is True  # EUR
    assert is_valid_numeric_code('000') is False
    
    print("  ✓ 货币验证测试通过")


def test_currency_info():
    """测试货币信息"""
    print("测试货币信息...")
    
    # USD 信息
    info = get_currency_info('USD')
    assert info['code'] == 'USD'
    assert info['name'] == 'US Dollar'
    assert info['symbol'] == '$'
    assert info['decimals'] == 2
    assert info['numeric_code'] == '840'
    
    # EUR 信息
    info = get_currency_info('EUR')
    assert info['symbol'] == '€'
    
    # JPY 信息
    info = get_currency_info('JPY')
    assert info['decimals'] == 0
    
    # 无效货币
    try:
        get_currency_info('XXX')
        assert False, "应该抛出异常"
    except InvalidCurrencyError:
        pass
    
    print("  ✓ 货币信息测试通过")


def test_symbol_mapping():
    """测试符号映射"""
    print("测试符号映射...")
    
    # $ 符号
    dollar_currencies = get_currencies_by_symbol('$')
    assert 'USD' in dollar_currencies
    assert 'AUD' in dollar_currencies
    assert 'CAD' in dollar_currencies
    
    # € 符号（只有 EUR）
    euro_currencies = get_currencies_by_symbol('€')
    assert 'EUR' in euro_currencies
    
    # ¥ 符号（JPY 和 CNY）
    yen_currencies = get_currencies_by_symbol('¥')
    assert 'JPY' in yen_currencies
    assert 'CNY' in yen_currencies
    
    # 无效符号
    empty = get_currencies_by_symbol('X')
    assert empty == []
    
    print("  ✓ 符号映射测试通过")


def test_currency_lists():
    """测试货币列表"""
    print("测试货币列表...")
    
    # 所有货币
    all_currencies = get_all_currencies()
    assert len(all_currencies) > 50
    assert 'USD' in all_currencies
    assert 'EUR' in all_currencies
    
    # 主要货币
    major = get_major_currencies()
    assert len(major) == 10
    assert 'USD' in major
    assert 'EUR' in major
    
    print("  ✓ 货币列表测试通过")


def test_exchange_rates():
    """测试汇率转换"""
    print("测试汇率转换...")
    
    rates = ExchangeRates('USD')
    
    # 设置汇率
    rates.set_rate('EUR', Decimal('0.92'))
    rates.set_rate('GBP', Decimal('0.79'))
    rates.set_rate('JPY', Decimal('151.5'))
    rates.set_rate('CNY', Decimal('7.24'))
    
    # USD -> EUR
    usd = Money(100, 'USD')
    eur = rates.convert(usd, to_currency='EUR')
    assert eur.amount == Decimal('92')
    assert eur.currency == 'EUR'
    
    # USD -> JPY
    jpy = rates.convert(usd, to_currency='JPY')
    assert jpy.amount == Decimal('15150')
    
    # 数值转换
    converted = rates.convert(100, 'USD', 'EUR')
    assert converted.amount == Decimal('92')
    
    # 批量设置
    rates2 = ExchangeRates('EUR')
    rates2.set_rates({
        'USD': Decimal('1.09'),
        'GBP': Decimal('0.86'),
    })
    result = rates2.convert(100, 'EUR', 'USD')
    assert result.amount == Decimal('109')
    
    # 相同货币
    same = rates.convert(100, 'USD', 'USD')
    assert same.amount == Decimal('100')
    
    print("  ✓ 汇率转换测试通过")


def test_convert_money():
    """测试简单货币转换"""
    print("测试简单货币转换...")
    
    # USD -> CNY
    result = convert_money(100, 'USD', 'CNY', 7.2)
    assert result.amount == Decimal('720')
    assert result.currency == 'CNY'
    
    # EUR -> USD
    result = convert_money(100, 'EUR', 'USD', 1.1)
    assert result.amount == Decimal('110')
    
    # Money 对象
    usd = Money(50, 'USD')
    result = convert_money(usd, None, 'CNY', 7.2)
    assert result.amount == Decimal('360')
    
    print("  ✓ 简单货币转换测试通过")


def test_add_taxes():
    """测试添加税费"""
    print("测试添加税费...")
    
    # 10% 税
    result = add_taxes(100, 0.1, 'USD')
    assert result.amount == Decimal('110')
    
    # 20% 税
    result = add_taxes(100, 0.2, 'USD')
    assert result.amount == Decimal('120')
    
    # Money 对象
    price = Money(50, 'EUR')
    result = add_taxes(price, 0.19)
    assert result.amount == Decimal('59.5')
    assert result.currency == 'EUR'
    
    print("  ✓ 添加税费测试通过")


def test_apply_discount():
    """测试应用折扣"""
    print("测试应用折扣...")
    
    # 百分比折扣
    result = apply_discount(100, 0.1, 'percent', 'USD')
    assert result.amount == Decimal('90')
    
    # 固定折扣
    result = apply_discount(100, 10, 'fixed', 'USD')
    assert result.amount == Decimal('90')
    
    # Money 对象
    price = Money(200, 'GBP')
    result = apply_discount(price, 0.25, 'percent')
    assert result.amount == Decimal('150')
    
    print("  ✓ 应用折扣测试通过")


def test_split_amount():
    """测试分割金额"""
    print("测试分割金额...")
    
    # 分成 3份
    parts = split_amount(100, 3, 'USD')
    assert len(parts) == 3
    # 验证总和等于原金额
    total = sum(p.amount for p in parts)
    assert total == Decimal('100')
    
    # 分成 7份
    parts = split_amount(100, 7, 'USD')
    assert len(parts) == 7
    total = sum(p.amount for p in parts)
    assert total == Decimal('100')
    
    # Money 对象
    money = Money(1000, 'JPY')
    parts = split_amount(money, 4)
    total = sum(p.amount for p in parts)
    assert total == Decimal('1000')
    
    print("  ✓ 分割金额测试通过")


def test_compare_amounts():
    """测试金额比较"""
    print("测试金额比较...")
    
    # 比较
    assert compare_amounts(100, 200, 'USD') == -1
    assert compare_amounts(200, 100, 'USD') == 1
    assert compare_amounts(100, 100, 'USD') == 0
    
    # Money 对象
    assert compare_amounts(Money(100, 'USD'), Money(200, 'USD')) == -1
    
    print("  ✓ 金额比较测试通过")


def test_percentage_of():
    """测试百分比计算"""
    print("测试百分比计算...")
    
    # 基本计算
    result = percentage_of(25, 100)
    assert result == Decimal('0.25')
    
    result = percentage_of(50, 200)
    assert result == Decimal('0.25')
    
    # Money 对象
    result = percentage_of(Money(25, 'USD'), Money(100, 'USD'))
    assert result == Decimal('0.25')
    
    # 零除
    try:
        percentage_of(25, 0)
        assert False, "应该抛出异常"
    except ZeroDivisionError:
        pass
    
    print("  ✓ 百分比计算测试通过")


def test_amount_checks():
    """测试金额检查"""
    print("测试金额检查...")
    
    # 零检查
    assert is_zero(0) is True
    assert is_zero(Money(0, 'USD')) is True
    assert is_zero(100) is False
    
    # 负数检查
    assert is_negative(-100) is True
    assert is_negative(Money(-50, 'EUR')) is True
    assert is_negative(100) is False
    
    # 正数检查
    assert is_positive(100) is True
    assert is_positive(Money(50, 'GBP')) is True
    assert is_positive(0) is False
    assert is_positive(-100) is False
    
    print("  ✓ 金额检查测试通过")


def test_convenience_functions():
    """测试便捷函数"""
    print("测试便捷函数...")
    
    # money()
    m = money(100, 'USD')
    assert m.amount == Decimal('100')
    assert m.currency == 'USD'
    
    # usd()
    m = usd(100)
    assert m.currency == 'USD'
    
    # eur()
    m = eur(100)
    assert m.currency == 'EUR'
    
    # gbp()
    m = gbp(100)
    assert m.currency == 'GBP'
    
    # jpy()
    m = jpy(100)
    assert m.currency == 'JPY'
    
    # cny()
    m = cny(100)
    assert m.currency == 'CNY'
    
    print("  ✓ 便捷函数测试通过")


def test_localization():
    """测试本地化格式"""
    print("测试本地化格式...")
    
    # 不同地区的格式
    amount = 1234.56
    
    # 美国格式
    us = format_money(amount, 'USD', 'en_US')
    assert '$' in us
    assert ',' in us
    assert '.' in us.split('$')[1]  # 小数点
    
    # 德国格式
    de = format_money(amount, 'EUR', 'de_DE')
    assert '€' in de
    assert '.' in de.replace('€', '')  # 千位分隔符
    assert ',' in de  # 小数分隔符
    
    # 法国格式
    fr = format_money(amount, 'EUR', 'fr_FR')
    assert ' ' in fr  # 千位分隔符是空格
    
    # 巴西格式
    br = format_money(amount, 'BRL', 'pt_BR')
    assert 'R$' in br
    
    print("  ✓ 本地化格式测试通过")


def test_decimal_precision():
    """测试 Decimal 精度"""
    print("测试 Decimal 精度...")
    
    # 大数字
    m1 = Money('999999999999.99', 'USD')
    assert m1.amount == Decimal('999999999999.99')
    
    # 小数字
    m2 = Money('0.00000001', 'BTC')
    assert m2.amount == Decimal('0.00000001')
    
    # 精确计算
    m3 = Money('0.1', 'USD')
    m4 = Money('0.2', 'USD')
    m5 = m3 + m4
    # 避免浮点精度问题
    assert m5.amount == Decimal('0.3')
    
    # 乘法精度
    m6 = Money('0.1', 'USD')
    m7 = m6 * 3
    assert m7.amount == Decimal('0.3')
    
    print("  ✓ Decimal 精度测试通过")


def test_crypto_currencies():
    """测试加密货币"""
    print("测试加密货币...")
    
    # BTC
    btc = Money('0.12345678', 'BTC')
    assert btc.decimals == 8
    assert btc.symbol == '₿'
    
    # ETH
    eth = Money('1.5', 'ETH')
    assert eth.decimals == 18
    
    # 格式化
    formatted = format_money('0.12345678', 'BTC')
    assert '₿' in formatted
    
    print("  ✓ 加密货币测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("Currency Utils 测试套件")
    print("="*50 + "\n")
    
    tests = [
        test_money_creation,
        test_money_invalid,
        test_money_operations,
        test_money_mismatch,
        test_money_rounding,
        test_format_money,
        test_parse_money,
        test_format_number,
        test_currency_validation,
        test_currency_info,
        test_symbol_mapping,
        test_currency_lists,
        test_exchange_rates,
        test_convert_money,
        test_add_taxes,
        test_apply_discount,
        test_split_amount,
        test_compare_amounts,
        test_percentage_of,
        test_amount_checks,
        test_convenience_functions,
        test_localization,
        test_decimal_precision,
        test_crypto_currencies,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} 失败: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("="*50 + "\n")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)