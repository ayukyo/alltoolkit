"""
房贷计算工具 - 基础用法示例

演示房贷计算工具的基本使用方法。
"""

import sys
import os
# 添加正确的路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mortgage_utils.mod import (
    calculate_mortgage,
    compare_methods,
    RepaymentMethod
)


def example_1_basic_calculation():
    """示例 1: 基本房贷计算"""
    print("\n" + "=" * 60)
    print("示例 1: 基本房贷计算")
    print("=" * 60)
    
    # 贷款 100 万，利率 4.2%，30 年
    principal = 1000000
    annual_rate = 4.2
    years = 30
    
    # 等额本息
    result = calculate_mortgage(principal, annual_rate, years, RepaymentMethod.EQUAL_PRINCIPAL_INTEREST)
    print(result.get_summary())
    
    print("计算结果字典:")
    for key, value in result.to_dict().items():
        print(f"  {key}: {value}")


def example_2_compare_methods():
    """示例 2: 对比等额本息和等额本金"""
    print("\n" + "=" * 60)
    print("示例 2: 对比等额本息和等额本金")
    print("=" * 60)
    
    comparison = compare_methods(1000000, 4.2, 30)
    
    print("\n【等额本息】")
    eq_pi = comparison["equal_principal_interest"]
    print(f"  月供: {eq_pi['monthly_payment']:,.2f} 元")
    print(f"  总利息: {eq_pi['total_interest']:,.2f} 元")
    print(f"  利息占比: {eq_pi['interest_ratio']:.2f}%")
    
    print("\n【等额本金】")
    eq_p = comparison["equal_principal"]
    print(f"  首月月供: {eq_p['first_month_payment']:,.2f} 元")
    print(f"  末月月供: {eq_p['last_month_payment']:,.2f} 元")
    print(f"  月供递减: {eq_p['monthly_decrease']:,.2f} 元/月")
    print(f"  总利息: {eq_p['total_interest']:,.2f} 元")
    print(f"  利息占比: {eq_p['interest_ratio']:.2f}%")
    
    print("\n【差异】")
    diff = comparison["difference"]
    print(f"  等额本金节省利息: {diff['total_interest_saved']:,.2f} 元")
    print(f"  首月月供差额: {diff['first_month_difference']:,.2f} 元")
    print(f"\n  {comparison['recommendation']}")


def example_3_different_terms():
    """示例 3: 不同贷款年限对比"""
    print("\n" + "=" * 60)
    print("示例 3: 不同贷款年限对比")
    print("=" * 60)
    
    principal = 1000000
    annual_rate = 4.2
    
    print(f"\n贷款 {principal:,} 元，利率 {annual_rate}%\n")
    print(f"{'年限':^6} | {'月供':^12} | {'总利息':^14} | {'利息/本金':^10}")
    print("-" * 55)
    
    for years in [10, 15, 20, 25, 30]:
        result = calculate_mortgage(principal, annual_rate, years)
        ratio = result.total_interest / principal * 100
        print(f"{years:^6}年 | {result.first_month_payment:>12,.2f} | {result.total_interest:>14,.2f} | {ratio:>10.2f}%")


def example_4_different_rates():
    """示例 4: 不同利率对比"""
    print("\n" + "=" * 60)
    print("示例 4: 不同利率对比")
    print("=" * 60)
    
    principal = 1000000
    years = 30
    
    print(f"\n贷款 {principal:,} 元，{years} 年\n")
    print(f"{'利率':^8} | {'月供':^12} | {'总利息':^14} | {'利息/本金':^10}")
    print("-" * 55)
    
    for rate in [3.0, 3.5, 4.0, 4.2, 4.5, 5.0]:
        result = calculate_mortgage(principal, rate, years)
        ratio = result.total_interest / principal * 100
        print(f"{rate:^8.1f}% | {result.first_month_payment:>12,.2f} | {result.total_interest:>14,.2f} | {ratio:>10.2f}%")


if __name__ == "__main__":
    example_1_basic_calculation()
    example_2_compare_methods()
    example_3_different_terms()
    example_4_different_rates()
    
    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60)