"""
Mortgage Utils Tests - 房贷计算工具测试

测试所有核心功能，包括等额本息、等额本金、提前还款等计算。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mortgage_utils.mod import (
    calculate_mortgage,
    calculate_equal_principal_interest,
    calculate_equal_principal,
    calculate_prepayment,
    calculate_affordable_loan,
    compare_methods,
    calculate_combined_loan,
    generate_payment_schedule,
    estimate_payoff_time,
    RepaymentMethod,
    PrepaymentType
)
from datetime import date


def test_equal_principal_interest():
    """测试等额本息计算"""
    print("测试等额本息计算...")
    
    # 标准测试用例
    result = calculate_mortgage(1000000, 4.2, 30, RepaymentMethod.EQUAL_PRINCIPAL_INTEREST)
    
    # 验证基本属性
    assert result.principal == 1000000
    assert result.annual_rate == 4.2
    assert result.years == 30
    assert result.total_months == 360
    
    # 验证月供（约 4890 元）
    assert 4850 < result.first_month_payment < 4950
    
    # 验证还款计划
    assert len(result.monthly_payments) == 360
    
    # 验证第一期
    first = result.monthly_payments[0]
    assert first.period == 1
    assert first.payment == result.first_month_payment
    assert first.interest > first.principal  # 前期利息多
    
    # 验证最后一期
    last = result.monthly_payments[-1]
    assert last.period == 360
    assert last.remaining_principal < 100  # 最后一期剩余本金接近 0
    
    # 验证总额（允许浮点数误差）
    expected_total = result.first_month_payment * 360
    assert abs(result.total_payment - expected_total) < 1
    assert abs(result.total_interest - (result.total_payment - result.principal)) < 1
    
    print("  ✓ 等额本息计算正确")


def test_equal_principal():
    """测试等额本金计算"""
    print("测试等额本金计算...")
    
    result = calculate_mortgage(1000000, 4.2, 30, RepaymentMethod.EQUAL_PRINCIPAL)
    
    # 验证基本属性
    assert result.principal == 1000000
    assert result.total_months == 360
    
    # 验证月供递减
    first_payment = result.first_month_payment
    last_payment = result.last_month_payment
    assert first_payment > last_payment
    
    # 验证每月本金固定
    monthly_principal = result.principal / result.total_months
    for p in result.monthly_payments[:12]:
        assert abs(p.principal - monthly_principal) < 0.01
    
    # 验证利息递减
    prev_interest = result.monthly_payments[0].interest
    for p in result.monthly_payments[1:12]:
        assert p.interest < prev_interest
        prev_interest = p.interest
    
    # 验证总额计算
    total_payment = sum(p.payment for p in result.monthly_payments)
    assert abs(total_payment - result.total_payment) < 1
    
    print("  ✓ 等额本金计算正确")


def test_interest_comparison():
    """对比两种方式的总利息"""
    print("测试利息对比...")
    
    equal_pi = calculate_mortgage(1000000, 4.2, 30, RepaymentMethod.EQUAL_PRINCIPAL_INTEREST)
    equal_p = calculate_mortgage(1000000, 4.2, 30, RepaymentMethod.EQUAL_PRINCIPAL)
    
    # 等额本金总利息更少
    assert equal_p.total_interest < equal_pi.total_interest
    
    # 等额本金首月月供更高
    assert equal_p.first_month_payment > equal_pi.first_month_payment
    
    # 使用对比函数验证
    comparison = compare_methods(1000000, 4.2, 30)
    assert comparison["difference"]["total_interest_saved"] > 0
    
    print(f"  等额本息总利息: {equal_pi.total_interest:,.2f}")
    print(f"  等额本金总利息: {equal_p.total_interest:,.2f}")
    print(f"  ✓ 等额本金节省利息: {equal_pi.total_interest - equal_p.total_interest:,.2f}")


def test_prepayment_reduce_term():
    """测试提前还款（缩短年限）"""
    print("测试提前还款（缩短年限）...")
    
    result = calculate_mortgage(1000000, 4.2, 30, RepaymentMethod.EQUAL_PRINCIPAL_INTEREST)
    
    # 第 12 个月提前还款 10 万
    prepay = calculate_prepayment(result, 12, 100000, PrepaymentType.REDUCE_TERM)
    
    assert prepay.prepayment_amount == 100000
    assert prepay.prepayment_month == 12
    assert prepay.new_remaining < prepay.original_remaining
    assert prepay.months_saved > 0
    assert prepay.interest_saved_term > 0
    
    print(f"  原剩余本金: {prepay.original_remaining:,.2f}")
    print(f"  新剩余本金: {prepay.new_remaining:,.2f}")
    print(f"  节省月数: {prepay.months_saved}")
    print(f"  ✓ 节省利息: {prepay.interest_saved_term:,.2f}")


def test_prepayment_reduce_payment():
    """测试提前还款（减少月供）"""
    print("测试提前还款（减少月供）...")
    
    result = calculate_mortgage(1000000, 4.2, 30, RepaymentMethod.EQUAL_PRINCIPAL_INTEREST)
    
    # 第 12 个月提前还款 10 万
    prepay = calculate_prepayment(result, 12, 100000, PrepaymentType.REDUCE_PAYMENT)
    
    assert prepay.prepayment_amount == 100000
    assert prepay.new_monthly_payment < prepay.payment_before
    assert prepay.interest_saved_payment > 0
    
    print(f"  原月供: {prepay.payment_before:,.2f}")
    print(f"  新月供: {prepay.new_monthly_payment:,.2f}")
    print(f"  ✓ 月供减少: {prepay.payment_before - prepay.new_monthly_payment:,.2f}")


def test_affordable_loan():
    """测试反算贷款额度"""
    print("测试反算贷款额度...")
    
    # 月供 5000，利率 4.2%，30 年
    loan = calculate_affordable_loan(5000, 4.2, 30)
    
    assert loan > 0
    
    # 反向验证
    result = calculate_mortgage(loan, 4.2, 30, RepaymentMethod.EQUAL_PRINCIPAL_INTEREST)
    # 月供应该接近 5000
    assert abs(result.first_month_payment - 5000) < 10
    
    print(f"  月供 5000 可贷款: {loan:,.2f}")
    print(f"  ✓ 验证月供: {result.first_month_payment:,.2f}")


def test_combined_loan():
    """测试组合贷款"""
    print("测试组合贷款...")
    
    # 商业贷 70 万(4.2%) + 公积金 30 万(3.1%)，30 年
    combined = calculate_combined_loan(700000, 4.2, 300000, 3.1, 30)
    
    assert combined["commercial"]["principal"] == 700000
    assert combined["fund"]["principal"] == 300000
    assert combined["combined"]["total_principal"] == 1000000
    
    # 验证月供相加
    expected_payment = combined["commercial"]["first_month_payment"] + combined["fund"]["first_month_payment"]
    assert abs(combined["combined"]["first_month_payment"] - expected_payment) < 1
    
    print(f"  商业贷月供: {combined['commercial']['first_month_payment']:,.2f}")
    print(f"  公积金月供: {combined['fund']['first_month_payment']:,.2f}")
    print(f"  ✓ 总月供: {combined['combined']['first_month_payment']:,.2f}")


def test_payment_schedule():
    """测试还款计划生成"""
    print("测试还款计划生成...")
    
    result = calculate_mortgage(1000000, 4.2, 30, RepaymentMethod.EQUAL_PRINCIPAL_INTEREST)
    
    # 文本格式
    text_schedule = generate_payment_schedule(result, "text")
    assert "还款计划表" in text_schedule
    assert "期数" in text_schedule
    
    # CSV 格式
    csv_schedule = generate_payment_schedule(result, "csv")
    assert "期数,月供,本金,利息,剩余本金" in csv_schedule
    
    print("  ✓ 还款计划生成正确")


def test_estimate_payoff_time():
    """测试还清时间估算"""
    print("测试还清时间估算...")
    
    result = estimate_payoff_time(1000000, 4.2, 5000)
    
    assert result["status"] == "可还清"
    assert result["months"] > 0
    assert result["years"] > 0
    
    print(f"  月供 5000 需 {result['months']} 个月 ({result['years']} 年)")
    print(f"  ✓ 总利息: {result['total_interest']:,.2f}")


def test_zero_interest():
    """测试零利率情况"""
    print("测试零利率情况...")
    
    # 零利率等额本息
    result = calculate_mortgage(120000, 0, 10, RepaymentMethod.EQUAL_PRINCIPAL_INTEREST)
    
    assert result.total_interest == 0
    assert result.total_payment == 120000
    assert result.first_month_payment == 1000  # 120000 / 120
    
    # 零利率等额本金
    result2 = calculate_mortgage(120000, 0, 10, RepaymentMethod.EQUAL_PRINCIPAL)
    
    assert result2.total_interest == 0
    assert result2.first_month_payment == 1000
    assert result2.last_month_payment == 1000
    
    print("  ✓ 零利率计算正确")


def test_short_term_loan():
    """测试短期贷款"""
    print("测试短期贷款...")
    
    # 1 年期贷款
    result = calculate_mortgage(100000, 4.2, 1)
    
    assert result.total_months == 12
    assert len(result.monthly_payments) == 12
    
    # 最后一期剩余本金接近 0
    assert result.monthly_payments[-1].remaining_principal < 1
    
    print(f"  ✓ 1 年期贷款计算正确，月供: {result.first_month_payment:,.2f}")


def test_with_start_date():
    """测试带起始日期的计算"""
    print("测试带起始日期的计算...")
    
    start_date = date(2024, 1, 15)
    result = calculate_mortgage(1000000, 4.2, 30, start_date=start_date)
    
    # 验证第一期日期
    assert result.monthly_payments[0].date == start_date
    
    # 验证日期递增
    prev_date = result.monthly_payments[0].date
    for p in result.monthly_payments[1:12]:
        assert p.date > prev_date
        prev_date = p.date
    
    print("  ✓ 日期计算正确")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 小额贷款
    small = calculate_mortgage(10000, 4.2, 1)
    assert small.total_months == 12
    
    # 高利率
    high_rate = calculate_mortgage(100000, 10, 5)
    assert high_rate.total_interest > 0
    
    # 长期贷款
    long_term = calculate_mortgage(1000000, 3.5, 30)
    assert long_term.total_months == 360
    
    print("  ✓ 边界情况处理正确")


def test_error_handling():
    """测试错误处理"""
    print("测试错误处理...")
    
    # 负本金
    try:
        calculate_mortgage(-100000, 4.2, 30)
        assert False, "应该抛出异常"
    except ValueError as e:
        assert "贷款本金" in str(e)
    
    # 零年限
    try:
        calculate_mortgage(100000, 4.2, 0)
        assert False, "应该抛出异常"
    except ValueError as e:
        assert "贷款年限" in str(e)
    
    # 无效提前还款月份
    result = calculate_mortgage(100000, 4.2, 10)
    try:
        calculate_prepayment(result, 500, 10000)  # 超出范围
        assert False, "应该抛出异常"
    except ValueError as e:
        assert "月份" in str(e)
    
    print("  ✓ 错误处理正确")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("房贷计算工具测试套件")
    print("=" * 60 + "\n")
    
    tests = [
        test_equal_principal_interest,
        test_equal_principal,
        test_interest_comparison,
        test_prepayment_reduce_term,
        test_prepayment_reduce_payment,
        test_affordable_loan,
        test_combined_loan,
        test_payment_schedule,
        test_estimate_payoff_time,
        test_zero_interest,
        test_short_term_loan,
        test_with_start_date,
        test_edge_cases,
        test_error_handling
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ 测试失败: {test.__name__}")
            print(f"    错误: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)