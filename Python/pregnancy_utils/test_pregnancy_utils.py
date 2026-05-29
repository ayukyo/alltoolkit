#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Pregnancy Utilities Module Tests
==============================================
Comprehensive tests for the pregnancy utilities module.
"""

import pytest
from datetime import date, timedelta
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    calculate_due_date_from_lmp,
    calculate_due_date_from_conception,
    calculate_due_date_from_ivf,
    calculate_gestational_age,
    get_trimester,
    get_pregnancy_status,
    calculate_progress_percentage,
    calculate_full_pregnancy,
    get_milestones,
    get_next_milestone,
    get_fetal_development,
    get_checkup_schedule,
    get_upcoming_checkups,
    format_gestational_age,
    get_pregnancy_summary,
    estimate_lmp_from_due_date,
    estimate_conception_from_due_date,
    is_high_risk_pregnancy,
    _parse_date,
    Trimester,
    PregnancyStatus,
    CalculationMethod,
    PREGNANCY_DAYS,
    PREGNANCY_WEEKS,
)


class TestParseDate:
    """测试日期解析功能"""
    
    def test_parse_date_object(self):
        """测试 date 对象输入"""
        input_date = date(2024, 1, 1)
        result = _parse_date(input_date)
        assert result == date(2024, 1, 1)
    
    def test_parse_datetime_object(self):
        """测试 datetime 对象输入"""
        from datetime import datetime
        input_datetime = datetime(2024, 1, 1, 12, 0, 0)
        result = _parse_date(input_datetime)
        # 结果应该是 date 对象，值与 datetime 的日期部分相同
        assert isinstance(result, date)
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 1
    
    def test_parse_string_yyyy_mm_dd(self):
        """测试 YYYY-MM-DD 格式字符串"""
        result = _parse_date('2024-01-15')
        assert result == date(2024, 1, 15)
    
    def test_parse_string_yyyy_slash_mm_dd(self):
        """测试 YYYY/MM/DD 格式字符串"""
        result = _parse_date('2024/01/15')
        assert result == date(2024, 1, 15)
    
    def test_parse_invalid_format(self):
        """测试无效格式"""
        with pytest.raises(ValueError):
            _parse_date('invalid-date')


class TestDueDateCalculations:
    """测试预产期计算功能"""
    
    def test_calculate_due_date_from_lmp(self):
        """测试从末次月经计算预产期"""
        # Naegele's rule: +280 days
        lmp = date(2024, 1, 1)
        due_date = calculate_due_date_from_lmp(lmp)
        expected = date(2024, 10, 7)  # 280天 = 2024-10-07
        assert due_date == expected
    
    def test_calculate_due_date_from_lmp_string(self):
        """测试字符串输入"""
        due_date = calculate_due_date_from_lmp('2024-01-01')
        assert due_date == date(2024, 10, 7)  # 280天
    
    def test_calculate_due_date_from_lmp_february(self):
        """测试跨年计算（含闰年）"""
        lmp = date(2024, 2, 15)
        due_date = calculate_due_date_from_lmp(lmp)
        # 2024是闰年，2月有29天
        expected = date(2024, 11, 21)
        assert due_date == expected
    
    def test_calculate_due_date_from_lmp_december(self):
        """测试跨年计算"""
        lmp = date(2024, 12, 1)
        due_date = calculate_due_date_from_lmp(lmp)
        expected = date(2025, 9, 7)
        assert due_date == expected
    
    def test_calculate_due_date_from_conception(self):
        """测试从受孕日期计算预产期"""
        conception = date(2024, 1, 15)
        due_date = calculate_due_date_from_conception(conception)
        expected = date(2024, 10, 7)  # +266 days
        assert due_date == expected
    
    def test_calculate_due_date_from_conception_string(self):
        """测试字符串输入"""
        due_date = calculate_due_date_from_conception('2024-01-15')
        assert due_date == date(2024, 10, 7)  # +266 days
    
    def test_calculate_due_date_from_ivf_day3(self):
        """测试IVF（3天胚胎）"""
        transfer = date(2024, 1, 18)
        due_date = calculate_due_date_from_ivf(transfer, embryo_age_days=3)
        expected = date(2024, 10, 7)
        assert due_date == expected
    
    def test_calculate_due_date_from_ivf_day5(self):
        """测试IVF（5天囊胚）"""
        transfer = date(2024, 1, 20)
        due_date = calculate_due_date_from_ivf(transfer, embryo_age_days=5)
        expected = date(2024, 10, 7)
        assert due_date == expected
    
    def test_calculate_due_date_from_ivf_string(self):
        """测试字符串输入"""
        due_date = calculate_due_date_from_ivf('2024-01-18', 3)
        assert due_date == date(2024, 10, 7)


class TestGestationalAge:
    """测试孕周计算功能"""
    
    def test_calculate_gestational_age_early(self):
        """测试早期孕周"""
        lmp = date(2024, 1, 1)
        current = date(2024, 1, 15)
        weeks, days = calculate_gestational_age(lmp, current)
        assert weeks == 2
        assert days == 0
    
    def test_calculate_gestational_age_mid(self):
        """测试中期孕周"""
        lmp = date(2024, 1, 1)
        current = date(2024, 5, 1)  # 约121天
        weeks, days = calculate_gestational_age(lmp, current)
        assert weeks == 17
        assert days == 2
    
    def test_calculate_gestational_age_late(self):
        """测试晚期孕周"""
        lmp = date(2024, 1, 1)
        current = date(2024, 9, 1)
        weeks, days = calculate_gestational_age(lmp, current)
        assert weeks == 34
        assert days == 6
    
    def test_calculate_gestational_age_full_term(self):
        """测试足月孕周"""
        lmp = date(2024, 1, 1)
        current = date(2024, 10, 7)  # 预产期（280天后）
        weeks, days = calculate_gestational_age(lmp, current)
        assert weeks == 40
        assert days == 0
    
    def test_calculate_gestational_age_from_conception(self):
        """测试从受孕日期计算孕周"""
        conception = date(2024, 1, 15)
        current = date(2024, 5, 1)
        weeks, days = calculate_gestational_age(conception, current, CalculationMethod.CONCEPTION)
        # 应该与从LMP计算结果相近
        assert weeks == 17
        assert days == 2
    
    def test_calculate_gestational_age_today(self):
        """测试使用今天的日期"""
        lmp = date.today() - timedelta(days=140)  # 20周前
        weeks, days = calculate_gestational_age(lmp)
        assert weeks == 20
        assert days == 0


class TestTrimester:
    """测试孕期划分功能"""
    
    def test_first_trimester_early(self):
        """测试早孕期（早期）"""
        trimester, label = get_trimester(4)
        assert trimester == Trimester.FIRST
        assert '第一孕期' in label
    
    def test_first_trimester_late(self):
        """测试早孕期（晚期）"""
        trimester, label = get_trimester(12)
        assert trimester == Trimester.FIRST
    
    def test_second_trimester_early(self):
        """测试中孕期（早期）"""
        trimester, label = get_trimester(13)
        assert trimester == Trimester.SECOND
        assert '第二孕期' in label
    
    def test_second_trimester_mid(self):
        """测试中孕期（中期）"""
        trimester, label = get_trimester(20)
        assert trimester == Trimester.SECOND
    
    def test_second_trimester_late(self):
        """测试中孕期（晚期）"""
        trimester, label = get_trimester(26)
        assert trimester == Trimester.SECOND
    
    def test_third_trimester_early(self):
        """测试晚孕期（早期）"""
        trimester, label = get_trimester(27)
        assert trimester == Trimester.THIRD
        assert '第三孕期' in label
    
    def test_third_trimester_late(self):
        """测试晚孕期（晚期）"""
        trimester, label = get_trimester(38)
        assert trimester == Trimester.THIRD
    
    def test_post_term(self):
        """测试过期妊娠"""
        trimester, label = get_trimester(42)
        assert trimester == Trimester.THIRD


class TestPregnancyStatus:
    """测试妊娠状态功能"""
    
    def test_early_pregnancy(self):
        """测试早孕期"""
        status, label = get_pregnancy_status(8)
        assert status == PregnancyStatus.EARLY
        assert '早孕' in label
    
    def test_normal_pregnancy_early(self):
        """测试正常妊娠（早期）"""
        status, label = get_pregnancy_status(13)
        assert status == PregnancyStatus.NORMAL
        assert '正常' in label
    
    def test_normal_pregnancy_mid(self):
        """测试正常妊娠（中期）"""
        status, label = get_pregnancy_status(25)
        assert status == PregnancyStatus.NORMAL
    
    def test_normal_pregnancy_late(self):
        """测试正常妊娠（晚期）"""
        status, label = get_pregnancy_status(36)
        assert status == PregnancyStatus.NORMAL
    
    def test_full_term_early(self):
        """测试足月（早期）"""
        status, label = get_pregnancy_status(37)
        assert status == PregnancyStatus.FULL_TERM
        assert '足月' in label
    
    def test_full_term_due_date(self):
        """测试足月（预产期）"""
        status, label = get_pregnancy_status(40)
        assert status == PregnancyStatus.FULL_TERM
    
    def test_post_term(self):
        """测试过期妊娠"""
        status, label = get_pregnancy_status(42)
        assert status == PregnancyStatus.POST_TERM
        assert '过期' in label


class TestProgressPercentage:
    """测试进度计算功能"""
    
    def test_progress_zero(self):
        """测试初始进度"""
        progress = calculate_progress_percentage(0)
        assert progress == 0.0
    
    def test_progress_quarter(self):
        """测试25%进度"""
        progress = calculate_progress_percentage(10)
        assert progress == 25.0
    
    def test_progress_half(self):
        """测试50%进度"""
        progress = calculate_progress_percentage(20)
        assert progress == 50.0
    
    def test_progress_three_quarters(self):
        """测试75%进度"""
        progress = calculate_progress_percentage(30)
        assert progress == 75.0
    
    def test_progress_full(self):
        """测试100%进度"""
        progress = calculate_progress_percentage(40)
        assert progress == 100.0
    
    def test_progress_with_days(self):
        """测试带天数的进度"""
        progress = calculate_progress_percentage(20, 3)
        expected = ((20 * 7 + 3) / PREGNANCY_DAYS) * 100
        assert progress == round(expected, 1)
    
    def test_progress_capped(self):
        """测试进度上限"""
        progress = calculate_progress_percentage(45)
        assert progress == 100.0  # 不超过100%


class TestFullPregnancy:
    """测试完整孕期计算功能"""
    
    def test_calculate_full_pregnancy_early(self):
        """测试早期妊娠"""
        result = calculate_full_pregnancy('2024-01-01', '2024-02-01')
        
        assert result.due_date == date(2024, 10, 7)
        assert result.conception_date == date(2024, 1, 15)
        assert result.lmp_date == date(2024, 1, 1)
        assert result.current_week == 4
        assert result.current_day == 3
        assert result.days_remaining == 249
        assert result.trimester == 'first'
        assert result.status == 'early'
    
    def test_calculate_full_pregnancy_mid(self):
        """测试中期妊娠"""
        result = calculate_full_pregnancy('2024-01-01', '2024-05-15')
        
        assert result.due_date == date(2024, 10, 7)
        assert result.current_week == 19
        assert result.current_day == 2
        assert result.trimester == 'second'
        assert result.status == 'normal'
        assert 47 < result.progress_percent < 50
    
    def test_calculate_full_pregnancy_late(self):
        """测试晚期妊娠"""
        result = calculate_full_pregnancy('2024-01-01', '2024-08-15')
        
        assert result.current_week == 32
        assert result.current_day == 3  # 修正天数
        assert result.trimester == 'third'
        assert result.status == 'normal'
        assert 80 < result.progress_percent < 85
    
    def test_calculate_full_pregnancy_full_term(self):
        """测试足月妊娠"""
        result = calculate_full_pregnancy('2024-01-01', '2024-10-07')
        
        assert result.current_week == 40
        assert result.current_day == 0
        assert result.trimester == 'third'
        assert result.status == 'full_term'
        assert result.progress_percent == 100.0
        assert result.days_remaining == 0
    
    def test_calculate_full_pregnancy_post_term(self):
        """测试过期妊娠"""
        result = calculate_full_pregnancy('2024-01-01', '2024-10-22')
        
        assert result.current_week == 42
        assert result.status == 'post_term'
        assert result.days_remaining == 0


class TestMilestones:
    """测试里程碑功能"""
    
    def test_get_milestones(self):
        """测试获取里程碑列表"""
        milestones = get_milestones('2024-01-01', '2024-05-01')
        
        assert len(milestones) > 0
        
        # 检查里程碑结构
        first_milestone = milestones[0]
        assert first_milestone.week == 4
        assert first_milestone.name is not None
        assert first_milestone.date is not None
    
    def test_get_next_milestone_early(self):
        """测试早期妊娠的下一个里程碑"""
        milestone = get_next_milestone('2024-01-01', '2024-02-01')
        
        assert milestone is not None
        assert milestone.week == 6  # 胎心初现
        assert not milestone.is_passed
    
    def test_get_next_milestone_mid(self):
        """测试中期妊娠的下一个里程碑"""
        milestone = get_next_milestone('2024-01-01', '2024-05-15')
        
        assert milestone is not None
        assert milestone.week == 20  # 大排畸
        assert milestone.days_until > 0
    
    def test_get_next_milestone_full_term(self):
        """测试足月妊娠"""
        milestone = get_next_milestone('2024-01-01', '2024-10-15')
        
        # 过了预产期，可能没有下一个里程碑
        assert milestone is None or milestone.week > 40


class TestFetalDevelopment:
    """测试胎儿发育功能"""
    
    def test_get_fetal_development_early(self):
        """测试早期胎儿发育"""
        dev = get_fetal_development(8)
        
        assert dev.week == 8
        assert dev.length_cm > 0
        assert dev.size_reference is not None
        assert len(dev.developments) > 0
    
    def test_get_fetal_development_mid(self):
        """测试中期胎儿发育"""
        dev = get_fetal_development(20)
        
        assert dev.week == 20
        assert dev.length_cm > 10
        assert dev.weight_g > 100
        assert '香蕉' in dev.size_reference
    
    def test_get_fetal_development_late(self):
        """测试晚期胎儿发育"""
        dev = get_fetal_development(36)
        
        assert dev.week == 36
        assert dev.length_cm > 30
        assert dev.weight_g > 2000
    
    def test_get_fetal_development_full_term(self):
        """测试足月胎儿发育"""
        dev = get_fetal_development(40)
        
        assert dev.week == 40
        assert dev.weight_g > 3000
        assert '西瓜' in dev.size_reference


class TestCheckupSchedule:
    """测试产检时间表功能"""
    
    def test_get_checkup_schedule(self):
        """测试获取产检时间表"""
        schedule = get_checkup_schedule('2024-01-01', '2024-05-01')
        
        assert len(schedule) > 0
        
        # 检查产检结构
        first_checkup = schedule[0]
        assert first_checkup.week == 8
        assert first_checkup.name == '首次产检'
        assert len(first_checkup.items) > 0
    
    def test_get_upcoming_checkups(self):
        """测试获取即将到来的产检"""
        checkups = get_upcoming_checkups('2024-01-01', '2024-03-01', limit=2)
        
        assert len(checkups) <= 2
        
        for checkup in checkups:
            assert not checkup.is_past
            assert checkup.date > date(2024, 3, 1)
    
    def test_checkup_past_status(self):
        """测试产检过去状态"""
        schedule = get_checkup_schedule('2024-01-01', '2024-10-01')
        
        # 早期产检应该是已过
        early_checkups = [s for s in schedule if s.week <= 30]
        for checkup in early_checkups:
            assert checkup.is_past
    
    def test_checkup_upcoming_flag(self):
        """测试即将到来标记"""
        schedule = get_checkup_schedule('2024-01-01', '2024-05-01')
        
        # 找到即将到来的产检（14天内）
        upcoming = [s for s in schedule if s.is_upcoming]
        
        for checkup in upcoming:
            assert not checkup.is_past
            days_until = (checkup.date - date(2024, 5, 1)).days
            assert days_until <= 14


class TestFormatGestationalAge:
    """测试格式化孕周功能"""
    
    def test_format_weeks_only(self):
        """测试仅周数"""
        result = format_gestational_age(20)
        assert result == '20周'
    
    def test_format_weeks_and_days(self):
        """测试周数和天数"""
        result = format_gestational_age(20, 4)
        assert result == '20周+4天'
    
    def test_format_zero_days(self):
        """测试零天"""
        result = format_gestational_age(10, 0)
        assert result == '10周'


class TestPregnancySummary:
    """测试孕期摘要功能"""
    
    def test_get_pregnancy_summary(self):
        """测试获取孕期摘要"""
        summary = get_pregnancy_summary('2024-01-01', '2024-05-15')
        
        assert 'weeks' in summary
        assert 'days' in summary
        assert 'due_date' in summary
        assert 'trimester' in summary
        assert 'progress' in summary
        
        assert summary['weeks'] == 19
        assert summary['due_date'] == '2024-10-07'
        assert '第二孕期' in summary['trimester']
    
    def test_pregnancy_summary_fetal_info(self):
        """测试胎儿信息"""
        summary = get_pregnancy_summary('2024-01-01', '2024-05-15')
        
        assert 'fetal_size' in summary
        assert 'fetal_weight' in summary
        assert summary['fetal_size'] is not None


class TestEstimateFromDueDate:
    """测试从预产期推算功能"""
    
    def test_estimate_lmp_from_due_date(self):
        """测试从预产期估算末次月经"""
        due_date = date(2024, 10, 7)
        lmp = estimate_lmp_from_due_date(due_date)
        expected = date(2024, 1, 1)  # 280天倒推
        assert lmp == expected
    
    def test_estimate_conception_from_due_date(self):
        """测试从预产期估算受孕日期"""
        due_date = date(2024, 10, 7)
        conception = estimate_conception_from_due_date(due_date)
        expected = date(2024, 1, 15)  # 266天倒推
        assert conception == expected
    
    def test_roundtrip_lmp(self):
        """测试往返计算"""
        original_lmp = date(2024, 3, 15)
        due_date = calculate_due_date_from_lmp(original_lmp)
        estimated_lmp = estimate_lmp_from_due_date(due_date)
        assert estimated_lmp == original_lmp
    
    def test_roundtrip_string(self):
        """测试字符串输入往返计算"""
        due_date = calculate_due_date_from_lmp('2024-01-01')
        lmp = estimate_lmp_from_due_date(due_date)
        assert lmp == date(2024, 1, 1)


class TestHighRiskPregnancy:
    """测试高危妊娠评估功能"""
    
    def test_normal_pregnancy(self):
        """测试正常妊娠"""
        is_high_risk, factors = is_high_risk_pregnancy(age=28)
        assert is_high_risk == False
        assert len(factors) == 0
    
    def test_advanced_maternal_age(self):
        """测试高龄产妇"""
        is_high_risk, factors = is_high_risk_pregnancy(age=38)
        assert is_high_risk == True
        assert '年龄≥35岁' in factors
    
    def test_very_advanced_maternal_age(self):
        """测试极高龄产妇"""
        is_high_risk, factors = is_high_risk_pregnancy(age=42)
        assert is_high_risk == True
        assert '年龄≥35岁' in factors
        assert '年龄≥40岁' in factors
    
    def test_teenage_pregnancy(self):
        """测试青少年妊娠"""
        is_high_risk, factors = is_high_risk_pregnancy(age=16)
        assert is_high_risk == True
        assert '年龄<18岁' in factors
    
    def test_pre_existing_conditions(self):
        """测试既存疾病"""
        is_high_risk, factors = is_high_risk_pregnancy(
            pre_existing_conditions=['高血压', '糖尿病']
        )
        assert is_high_risk == True
        assert '慢性高血压' in factors
        assert '糖尿病' in factors
    
    def test_pregnancy_complications(self):
        """测试妊娠并发症"""
        is_high_risk, factors = is_high_risk_pregnancy(
            pregnancy_complications=['妊娠高血压', '前置胎盘']
        )
        assert is_high_risk == True
        assert '妊娠期高血压' in factors
        assert '前置胎盘' in factors
    
    def test_multiple_risk_factors(self):
        """测试多风险因素"""
        is_high_risk, factors = is_high_risk_pregnancy(
            age=39,
            pre_existing_conditions=['高血压'],
            pregnancy_complications=['妊娠糖尿病']
        )
        assert is_high_risk == True
        assert len(factors) >= 3
    
    def test_none_parameters(self):
        """测试空参数"""
        is_high_risk, factors = is_high_risk_pregnancy()
        assert is_high_risk == False
        assert len(factors) == 0


class TestConstants:
    """测试常量"""
    
    def test_pregnancy_days(self):
        """测试孕期天数"""
        assert PREGNANCY_DAYS == 280
    
    def test_pregnancy_weeks(self):
        """测试孕期周数"""
        assert PREGNANCY_WEEKS == 40


class TestEdgeCases:
    """测试边界情况"""
    
    def test_very_early_pregnancy(self):
        """测试非常早期的妊娠"""
        lmp = date.today() - timedelta(days=7)
        result = calculate_full_pregnancy(lmp)
        
        assert result.current_week == 1
        assert result.current_day == 0
        assert result.trimester == 'first'
    
    def test_overdue_pregnancy(self):
        """测试过期妊娠"""
        lmp = date(2024, 1, 1)
        current = date(2024, 10, 22)  # 42周+
        result = calculate_full_pregnancy(lmp, current)
        
        assert result.current_week == 42
        assert result.status == 'post_term'
    
    def test_exact_due_date(self):
        """测试预产期当天"""
        lmp = date(2024, 1, 1)
        due = date(2024, 10, 8)
        result = calculate_full_pregnancy(lmp, due)
        
        assert result.days_remaining == 0
        assert result.progress_percent == 100.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])