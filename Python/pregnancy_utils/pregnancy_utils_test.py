#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Pregnancy Utilities Tests

Tests for the pregnancy_utils module.
"""

import pytest
import sys
import os
from datetime import date, datetime, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pregnancy_utils import (
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
    Trimester,
    PregnancyStatus,
    CalculationMethod,
    DueDateResult,
    PregnancyMilestone,
    FetalDevelopment,
    CheckupSchedule,
    PREGNANCY_DAYS,
    PREGNANCY_WEEKS,
)


class TestCalculateDueDate:
    """Tests for due date calculation functions."""

    def test_due_date_from_lmp(self):
        """Test due date calculation from LMP."""
        due = calculate_due_date_from_lmp('2024-01-01')
        assert due == date(2024, 10, 7)

    def test_due_date_from_lmp_date_object(self):
        """Test due date from LMP with date object."""
        due = calculate_due_date_from_lmp(date(2024, 1, 1))
        assert due == date(2024, 10, 7)

    def test_due_date_from_conception(self):
        """Test due date from conception date."""
        due = calculate_due_date_from_conception('2024-01-15')
        assert due == date(2024, 10, 7)

    def test_due_date_from_ivf_day3(self):
        """Test due date from IVF transfer (day 3 embryo)."""
        due = calculate_due_date_from_ivf('2024-01-20', 3)
        assert due == date(2024, 10, 9)

    def test_due_date_from_ivf_day5(self):
        """Test due date from IVF transfer (day 5 blastocyst)."""
        due = calculate_due_date_from_ivf('2024-01-22', 5)
        assert due == date(2024, 10, 9)


class TestGestationalAge:
    """Tests for gestational age calculation."""

    def test_gestational_age_basic(self):
        """Test basic gestational age calculation."""
        weeks, days = calculate_gestational_age('2024-01-01', '2024-03-01')
        assert weeks == 8
        assert days == 4

    def test_gestational_age_20_weeks(self):
        """Test gestational age at 20 weeks."""
        weeks, days = calculate_gestational_age('2024-01-01', '2024-05-15')
        assert weeks == 19
        assert days == 2

    def test_gestational_age_from_conception(self):
        """Test gestational age from conception date."""
        # Conception date is ~14 days after LMP
        weeks, days = calculate_gestational_age('2024-01-15', '2024-03-01', CalculationMethod.CONCEPTION)
        assert weeks >= 6

    def test_gestational_age_today(self):
        """Test gestational age with today (None)."""
        # Should not raise an error
        weeks, days = calculate_gestational_age('2024-01-01')
        assert weeks >= 0


class TestTrimester:
    """Tests for trimester determination."""

    def test_first_trimester(self):
        """Test first trimester (weeks 0-12)."""
        trimester, label = get_trimester(8)
        assert trimester == Trimester.FIRST
        assert '第一孕期' in label or 'first' in label.lower()

    def test_second_trimester(self):
        """Test second trimester (weeks 13-26)."""
        trimester, label = get_trimester(20)
        assert trimester == Trimester.SECOND

    def test_third_trimester(self):
        """Test third trimester (weeks 27+)."""
        trimester, label = get_trimester(32)
        assert trimester == Trimester.THIRD

    def test_trimester_boundary_week13(self):
        """Test trimester at boundary week 13."""
        trimester, _ = get_trimester(13)
        assert trimester == Trimester.SECOND


class TestPregnancyStatus:
    """Tests for pregnancy status."""

    def test_status_early(self):
        """Test early pregnancy status."""
        status, label = get_pregnancy_status(10)
        assert status == PregnancyStatus.EARLY

    def test_status_normal(self):
        """Test normal pregnancy status."""
        status, label = get_pregnancy_status(25)
        assert status == PregnancyStatus.NORMAL

    def test_status_full_term(self):
        """Test full term pregnancy status."""
        status, label = get_pregnancy_status(38)
        assert status == PregnancyStatus.FULL_TERM

    def test_status_post_term(self):
        """Test post term pregnancy status."""
        status, label = get_pregnancy_status(42)
        assert status == PregnancyStatus.POST_TERM


class TestProgressPercentage:
    """Tests for progress percentage calculation."""

    def test_progress_at_20_weeks(self):
        """Test progress at 20 weeks."""
        progress = calculate_progress_percentage(20)
        assert progress == 50.0

    def test_progress_at_40_weeks(self):
        """Test progress at 40 weeks."""
        progress = calculate_progress_percentage(40)
        assert progress == 100.0

    def test_progress_at_10_weeks(self):
        """Test progress at 10 weeks."""
        progress = calculate_progress_percentage(10)
        expected = (10 * 7) / PREGNANCY_DAYS * 100
        assert abs(progress - expected) < 0.1

    def test_progress_capped_at_100(self):
        """Test that progress is capped at 100%."""
        progress = calculate_progress_percentage(45, days=5)
        assert progress <= 100.0


class TestFullPregnancy:
    """Tests for full pregnancy calculation."""

    def test_full_pregnancy_result(self):
        """Test full pregnancy calculation result structure."""
        result = calculate_full_pregnancy('2024-01-01', '2024-05-15')
        assert isinstance(result, DueDateResult)
        assert result.due_date == date(2024, 10, 7)
        assert result.lmp_date == date(2024, 1, 1)
        assert result.current_week >= 18

    def test_full_pregnancy_conception_date(self):
        """Test that conception date is approximately 14 days after LMP."""
        result = calculate_full_pregnancy('2024-01-01')
        assert result.conception_date == date(2024, 1, 15)

    def test_full_pregnancy_days_remaining(self):
        """Test days remaining calculation."""
        result = calculate_full_pregnancy('2024-01-01', '2024-05-15')
        assert result.days_remaining >= 0


class TestMilestones:
    """Tests for pregnancy milestones."""

    def test_get_milestones(self):
        """Test getting milestones list."""
        milestones = get_milestones('2024-01-01', '2024-03-01')
        assert isinstance(milestones, list)
        assert len(milestones) > 0
        assert all(isinstance(m, PregnancyMilestone) for m in milestones)

    def test_next_milestone(self):
        """Test getting next milestone."""
        milestone = get_next_milestone('2024-01-01', '2024-03-01')
        if milestone:
            assert milestone.is_passed is False

    def test_next_milestone_none_when_all_passed(self):
        """Test that next milestone is None when all milestones have passed."""
        # Use a date far past the due date
        milestone = get_next_milestone('2023-01-01', '2024-10-15')
        assert milestone is None or milestone.is_passed is True


class TestFetalDevelopment:
    """Tests for fetal development information."""

    def test_fetal_development_20_weeks(self):
        """Test fetal development at 20 weeks."""
        fetal = get_fetal_development(20)
        assert isinstance(fetal, FetalDevelopment)
        assert fetal.week == 20
        assert fetal.size_reference == '香蕉'
        assert fetal.length_cm > 0
        assert fetal.weight_g > 0

    def test_fetal_development_8_weeks(self):
        """Test fetal development at 8 weeks."""
        fetal = get_fetal_development(8)
        assert fetal.size_reference == '覆盆子'

    def test_fetal_development_size_reference(self):
        """Test that size reference changes based on week."""
        fetal_16 = get_fetal_development(16)
        fetal_20 = get_fetal_development(20)
        assert fetal_20.weight_g > fetal_16.weight_g


class TestCheckupSchedule:
    """Tests for prenatal checkup schedule."""

    def test_get_checkup_schedule(self):
        """Test getting checkup schedule."""
        schedule = get_checkup_schedule('2024-01-01')
        assert isinstance(schedule, list)
        assert len(schedule) > 0
        assert all(isinstance(c, CheckupSchedule) for c in schedule)

    def test_get_upcoming_checkups(self):
        """Test getting upcoming checkups."""
        checkups = get_upcoming_checkups('2024-01-01', '2024-05-15', limit=2)
        assert isinstance(checkups, list)
        assert len(checkups) <= 2

    def test_checkup_schedule_items(self):
        """Test that checkup items are present."""
        schedule = get_checkup_schedule('2024-01-01')
        first_checkup = schedule[0]
        assert len(first_checkup.items) > 0


class TestFormatGestationalAge:
    """Tests for gestational age formatting."""

    def test_format_without_days(self):
        """Test formatting without extra days."""
        result = format_gestational_age(20)
        assert '20' in result
        assert '周' in result

    def test_format_with_days(self):
        """Test formatting with extra days."""
        result = format_gestational_age(20, 4)
        assert '20' in result
        assert '4' in result


class TestPregnancySummary:
    """Tests for pregnancy summary."""

    def test_pregnancy_summary(self):
        """Test pregnancy summary structure."""
        summary = get_pregnancy_summary('2024-01-01', '2024-05-15')
        assert isinstance(summary, dict)
        assert 'weeks' in summary
        assert 'days' in summary
        assert 'due_date' in summary
        assert 'trimester' in summary
        assert 'progress' in summary

    def test_pregnancy_summary_values(self):
        """Test pregnancy summary values."""
        summary = get_pregnancy_summary('2024-01-01', '2024-05-15')
        assert summary['weeks'] >= 18
        assert '%' in summary['progress']


class TestEstimateFromDueDate:
    """Tests for estimation functions."""

    def test_estimate_lmp_from_due_date(self):
        """Test estimating LMP from due date."""
        lmp = estimate_lmp_from_due_date('2024-10-07')
        assert lmp == date(2024, 1, 1)

    def test_estimate_conception_from_due_date(self):
        """Test estimating conception date from due date."""
        conception = estimate_conception_from_due_date('2024-10-07')
        assert conception == date(2024, 1, 15)


class TestHighRiskPregnancy:
    """Tests for high risk pregnancy assessment."""

    def test_high_risk_age_high(self):
        """Test high risk due to age."""
        is_high_risk, factors = is_high_risk_pregnancy(age=38)
        assert is_high_risk is True
        assert len(factors) > 0

    def test_high_risk_age_too_young(self):
        """Test high risk due to young age."""
        is_high_risk, factors = is_high_risk_pregnancy(age=16)
        assert is_high_risk is True

    def test_not_high_risk_normal_age(self):
        """Test not high risk for normal age."""
        is_high_risk, factors = is_high_risk_pregnancy(age=25)
        assert is_high_risk is False

    def test_high_risk_conditions(self):
        """Test high risk due to pre-existing conditions."""
        is_high_risk, factors = is_high_risk_pregnancy(pre_existing_conditions=['高血压'])
        assert is_high_risk is True

    def test_high_risk_complications(self):
        """Test high risk due to pregnancy complications."""
        is_high_risk, factors = is_high_risk_pregnancy(
            pregnancy_complications=['妊娠糖尿病']
        )
        assert is_high_risk is True


class TestEdgeCases:
    """Tests for edge cases."""

    def test_due_date_invalid_format(self):
        """Test that invalid date format raises ValueError."""
        with pytest.raises(ValueError):
            calculate_due_date_from_lmp('invalid-date')

    def test_gestational_age_future_date(self):
        """Test gestational age with future reference date."""
        weeks, days = calculate_gestational_age('2025-01-01', '2024-01-01')
        assert weeks < 0  # Future LMP means negative gestational age

    def test_full_pregnancy_without_current_date(self):
        """Test full pregnancy calculation without current date (uses today)."""
        result = calculate_full_pregnancy('2024-01-01')
        assert result.current_week >= 0


class TestConstants:
    """Tests for module constants."""

    def test_pregnancy_days(self):
        """Test pregnancy days constant."""
        assert PREGNANCY_DAYS == 280

    def test_pregnancy_weeks(self):
        """Test pregnancy weeks constant."""
        assert PREGNANCY_WEEKS == 40


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
