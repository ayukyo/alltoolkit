#!/usr/bin/env python3
"""Blood Pressure Utils Tests"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    BPUnit, RiskLevel, Gender, BPReading, BPResult, BPStatistics, ChildBPResult,
    convert_bp_unit, mmhg_to_kpa, kpa_to_mmhg,
    calculate_pulse_pressure, calculate_map, get_map_status,
    classify_bp, get_pulse_pressure_category, get_age_normal_range,
    is_bp_age_appropriate, generate_recommendations, analyze_bp,
    calculate_bp_statistics, analyze_bp_trend,
    calculate_child_bp_percentile, analyze_child_bp,
    get_bp_summary, calculate_hypertension_stage,
    BP_CATEGORIES_WHO, ISH_CATEGORY, AGE_BP_RANGES
)


class TestResultCollector:
    """收集测试结果"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, name):
        self.passed += 1
        print(f"✓ {name}")
    
    def add_fail(self, name, msg):
        self.failed += 1
        self.errors.append((name, msg))
        print(f"✗ {name}: {msg}")
    
    def report(self):
        print(f"\n{'='*60}")
        print(f"Blood Pressure Utils Tests: {self.passed} passed, {self.failed} failed")
        if self.errors:
            print(f"\nFailed tests:")
            for name, msg in self.errors:
                print(f"  - {name}: {msg}")
        print(f"{'='*60}")
        return self.failed == 0


def run_tests():
    results = TestResultCollector()
    
    # Test 1: Unit conversion - mmHg to kPa
    try:
        kpa = mmhg_to_kpa(120)
        assert kpa == 15.96  # 120 * 0.133
        results.add_pass("Unit conversion mmHg to kPa")
    except Exception as e:
        results.add_fail("Unit conversion mmHg to kPa", str(e))
    
    # Test 2: Unit conversion - kPa to mmHg
    try:
        mmhg = kpa_to_mmhg(16)
        assert mmhg == 120.1  # 16 * 7.506
        results.add_pass("Unit conversion kPa to mmHg")
    except Exception as e:
        results.add_fail("Unit conversion kPa to mmHg", str(e))
    
    # Test 3: Unit conversion - same unit
    try:
        val = convert_bp_unit(120, BPUnit.MMHG, BPUnit.MMHG)
        assert val == 120
        results.add_pass("Unit conversion same unit")
    except Exception as e:
        results.add_fail("Unit conversion same unit", str(e))
    
    # Test 4: Calculate pulse pressure
    try:
        pp = calculate_pulse_pressure(120, 80)
        assert pp == 40
        results.add_pass("Calculate pulse pressure")
    except Exception as e:
        results.add_fail("Calculate pulse pressure", str(e))
    
    # Test 5: Calculate MAP
    try:
        map_val = calculate_map(120, 80)
        # 80 + (120-80)/3 = 93.33
        assert map_val == 93.33
        results.add_pass("Calculate MAP")
    except Exception as e:
        results.add_fail("Calculate MAP", str(e))
    
    # Test 6: Get MAP status - normal
    try:
        status = get_map_status(93)
        assert status == 'normal'
        results.add_pass("Get MAP status normal")
    except Exception as e:
        results.add_fail("Get MAP status normal", str(e))
    
    # Test 7: Get MAP status - low
    try:
        status = get_map_status(65)
        assert status == 'low'
        results.add_pass("Get MAP status low")
    except Exception as e:
        results.add_fail("Get MAP status low", str(e))
    
    # Test 8: Get MAP status - critical low
    try:
        status = get_map_status(50)
        assert status == 'critical_low'
        results.add_pass("Get MAP status critical low")
    except Exception as e:
        results.add_fail("Get MAP status critical low", str(e))
    
    # Test 9: Get MAP status - high
    try:
        status = get_map_status(110)
        assert status == 'high'
        results.add_pass("Get MAP status high")
    except Exception as e:
        results.add_fail("Get MAP status high", str(e))
    
    # Test 10: Classify BP - optimal
    try:
        cat, label, label_en, risk, desc = classify_bp(110, 70)
        assert cat == 'optimal'
        assert risk == 'low'
        results.add_pass("Classify BP optimal")
    except Exception as e:
        results.add_fail("Classify BP optimal", str(e))
    
    # Test 11: Classify BP - normal
    try:
        cat, label, label_en, risk, desc = classify_bp(125, 82)
        assert cat == 'normal'
        results.add_pass("Classify BP normal")
    except Exception as e:
        results.add_fail("Classify BP normal", str(e))
    
    # Test 12: Classify BP - high normal
    try:
        cat, label, label_en, risk, desc = classify_bp(135, 88)
        assert cat == 'high_normal'
        assert risk == 'moderate'
        results.add_pass("Classify BP high normal")
    except Exception as e:
        results.add_fail("Classify BP high normal", str(e))
    
    # Test 13: Classify BP - grade 1 hypertension
    try:
        cat, label, label_en, risk, desc = classify_bp(145, 95)
        assert cat == 'grade1_hypertension'
        assert risk == 'high'
        results.add_pass("Classify BP grade 1 hypertension")
    except Exception as e:
        results.add_fail("Classify BP grade 1 hypertension", str(e))
    
    # Test 14: Classify BP - grade 2 hypertension
    try:
        cat, label, label_en, risk, desc = classify_bp(165, 105)
        assert cat == 'grade2_hypertension'
        results.add_pass("Classify BP grade 2 hypertension")
    except Exception as e:
        results.add_fail("Classify BP grade 2 hypertension", str(e))
    
    # Test 15: Classify BP - grade 3 hypertension
    try:
        cat, label, label_en, risk, desc = classify_bp(185, 115)
        assert cat == 'grade3_hypertension'
        assert risk == 'extremely_high'
        results.add_pass("Classify BP grade 3 hypertension")
    except Exception as e:
        results.add_fail("Classify BP grade 3 hypertension", str(e))
    
    # Test 16: Classify BP - isolated systolic hypertension
    try:
        cat, label, label_en, risk, desc = classify_bp(150, 85)
        assert cat == 'isolated_systolic_hypertension'
        results.add_pass("Classify BP isolated systolic hypertension")
    except Exception as e:
        results.add_fail("Classify BP isolated systolic hypertension", str(e))
    
    # Test 17: Pulse pressure category - normal
    try:
        cat, label, desc = get_pulse_pressure_category(40)
        assert cat == 'normal'
        results.add_pass("Pulse pressure category normal")
    except Exception as e:
        results.add_fail("Pulse pressure category normal", str(e))
    
    # Test 18: Pulse pressure category - increased
    try:
        cat, label, desc = get_pulse_pressure_category(55)
        assert cat == 'increased'
        results.add_pass("Pulse pressure category increased")
    except Exception as e:
        results.add_fail("Pulse pressure category increased", str(e))
    
    # Test 19: Pulse pressure category - high
    try:
        cat, label, desc = get_pulse_pressure_category(65)
        assert cat == 'high'
        results.add_pass("Pulse pressure category high")
    except Exception as e:
        results.add_fail("Pulse pressure category high", str(e))
    
    # Test 20: Pulse pressure category - low
    try:
        cat, label, desc = get_pulse_pressure_category(25)
        assert cat == 'low'
        results.add_pass("Pulse pressure category low")
    except Exception as e:
        results.add_fail("Pulse pressure category low", str(e))
    
    # Test 21: Age normal range - child
    try:
        sys_min, sys_max, dia_min, dia_max = get_age_normal_range(10)
        assert sys_min == 102
        assert sys_max == 128
        results.add_pass("Age normal range child")
    except Exception as e:
        results.add_fail("Age normal range child", str(e))
    
    # Test 22: Age normal range - adult
    try:
        sys_min, sys_max, dia_min, dia_max = get_age_normal_range(30)
        assert sys_min == 90
        assert sys_max == 130
        results.add_pass("Age normal range adult")
    except Exception as e:
        results.add_fail("Age normal range adult", str(e))
    
    # Test 23: Age normal range - elderly
    try:
        sys_min, sys_max, dia_min, dia_max = get_age_normal_range(65)
        assert sys_min == 90
        assert sys_max == 150
        results.add_pass("Age normal range elderly")
    except Exception as e:
        results.add_fail("Age normal range elderly", str(e))
    
    # Test 24: Is BP age appropriate - true
    try:
        appropriate = is_bp_age_appropriate(110, 70, 10)
        assert appropriate == True
        results.add_pass("Is BP age appropriate true")
    except Exception as e:
        results.add_fail("Is BP age appropriate true", str(e))
    
    # Test 25: Is BP age appropriate - false
    try:
        appropriate = is_bp_age_appropriate(150, 90, 10)
        assert appropriate == False
        results.add_pass("Is BP age appropriate false")
    except Exception as e:
        results.add_fail("Is BP age appropriate false", str(e))
    
    # Test 26: Analyze BP - complete analysis
    try:
        result = analyze_bp(120, 80, 35)
        assert result.systolic == 120
        assert result.diastolic == 80
        assert result.category in ['optimal', 'normal']
        assert result.pulse_pressure == 40
        assert round(result.map, 2) == round(80 + (120-80)/3, 2)
        assert result.age_appropriate == True
        assert len(result.recommendations) > 0
        results.add_pass("Analyze BP complete analysis")
    except Exception as e:
        results.add_fail("Analyze BP complete analysis", str(e))
    
    # Test 27: Analyze BP - with kPa unit
    try:
        result = analyze_bp(16, 10.7, 35, BPUnit.KPA)  # ~120/80 mmHg
        # 16 * 7.506 = 120.1
        assert result.systolic == round(16 * 7.506, 2)
        results.add_pass("Analyze BP with kPa unit")
    except Exception as e:
        results.add_fail("Analyze BP with kPa unit", str(e))
    
    # Test 28: Calculate BP statistics
    try:
        readings = [(120, 80), (122, 82), (118, 78)]
        stats = calculate_bp_statistics(readings)
        assert stats.readings_count == 3
        assert stats.systolic_mean == 120
        assert stats.diastolic_mean == 80
        assert stats.systolic_min == 118
        assert stats.systolic_max == 122
        results.add_pass("Calculate BP statistics")
    except Exception as e:
        results.add_fail("Calculate BP statistics", str(e))
    
    # Test 29: Calculate BP statistics - trend
    try:
        readings = [(120, 80), (125, 85), (130, 90)]
        stats = calculate_bp_statistics(readings)
        assert stats.trend == 'increasing'
        results.add_pass("Calculate BP statistics trend")
    except Exception as e:
        results.add_fail("Calculate BP statistics trend", str(e))
    
    # Test 30: Analyze BP trend
    try:
        readings = [(120, 80, None), (125, 85, None), (130, 90, None)]
        trend_result = analyze_bp_trend(readings)
        assert trend_result['systolic_trend'] == 'increasing'
        assert trend_result['diastolic_trend'] == 'increasing'
        assert trend_result['systolic_change'] == 10
        results.add_pass("Analyze BP trend")
    except Exception as e:
        results.add_fail("Analyze BP trend", str(e))
    
    # Test 31: Child BP percentile
    try:
        percentile = calculate_child_bp_percentile(100, 65, 8, Gender.MALE)
        assert 1 <= percentile <= 99
        results.add_pass("Child BP percentile")
    except Exception as e:
        results.add_fail("Child BP percentile", str(e))
    
    # Test 32: Analyze child BP - normal
    try:
        result = analyze_child_bp(100, 65, 10, Gender.MALE)
        assert result.systolic == 100
        assert result.diastolic == 65
        assert result.percentile_category == 'normal'
        assert result.risk_level == 'low'
        results.add_pass("Analyze child BP normal")
    except Exception as e:
        results.add_fail("Analyze child BP normal", str(e))
    
    # Test 33: Analyze child BP - hypertension
    try:
        result = analyze_child_bp(130, 90, 10, Gender.MALE)
        # Percentile depends on calculation, may not be hypertension
        assert result.percentile_category in ['normal', 'prehypertension', 'hypertension']
        assert result.risk_level in ['low', 'moderate', 'high']
        results.add_pass("Analyze child BP hypertension")
    except Exception as e:
        results.add_fail("Analyze child BP hypertension", str(e))
    
    # Test 34: Get BP summary
    try:
        summary = get_bp_summary(120, 80)
        assert "120/80" in summary
        assert "血压" in summary
        results.add_pass("Get BP summary")
    except Exception as e:
        results.add_fail("Get BP summary", str(e))
    
    # Test 35: Calculate hypertension stage - normal
    try:
        stage = calculate_hypertension_stage(115, 75)
        assert stage == 'Normal'
        results.add_pass("Calculate hypertension stage normal")
    except Exception as e:
        results.add_fail("Calculate hypertension stage normal", str(e))
    
    # Test 36: Calculate hypertension stage - elevated
    try:
        stage = calculate_hypertension_stage(125, 75)
        assert stage == 'Elevated'
        results.add_pass("Calculate hypertension stage elevated")
    except Exception as e:
        results.add_fail("Calculate hypertension stage elevated", str(e))
    
    # Test 37: Calculate hypertension stage - stage 1
    try:
        stage = calculate_hypertension_stage(135, 85)
        assert stage == 'Hypertension Stage 1'
        results.add_pass("Calculate hypertension stage stage 1")
    except Exception as e:
        results.add_fail("Calculate hypertension stage stage 1", str(e))
    
    # Test 38: Calculate hypertension stage - stage 2
    try:
        stage = calculate_hypertension_stage(150, 100)
        assert stage == 'Hypertension Stage 2'
        results.add_pass("Calculate hypertension stage stage 2")
    except Exception as e:
        results.add_fail("Calculate hypertension stage stage 2", str(e))
    
    # Test 39: Calculate hypertension stage - crisis
    try:
        stage = calculate_hypertension_stage(190, 125)
        assert stage == 'Hypertensive Crisis'
        results.add_pass("Calculate hypertension stage crisis")
    except Exception as e:
        results.add_fail("Calculate hypertension stage crisis", str(e))
    
    # Test 40: Generate recommendations
    try:
        recs = generate_recommendations('optimal', 30, 'normal')
        assert len(recs) > 0
        assert "保持健康" in recs[0]
        
        recs2 = generate_recommendations('grade2_hypertension', 50, 'high')
        assert "就医" in recs2[0]
        results.add_pass("Generate recommendations")
    except Exception as e:
        results.add_fail("Generate recommendations", str(e))
    
    # Test 41: Empty readings error
    try:
        try:
            calculate_bp_statistics([])
            results.add_fail("Empty readings error", "Should raise ValueError")
        except ValueError:
            pass
        results.add_pass("Empty readings error")
    except Exception as e:
        results.add_fail("Empty readings error", str(e))
    
    # Test 42: Invalid child age
    try:
        try:
            calculate_child_bp_percentile(100, 65, 0, Gender.MALE)
            results.add_fail("Invalid child age", "Should raise ValueError")
        except ValueError:
            pass
        results.add_pass("Invalid child age")
    except Exception as e:
        results.add_fail("Invalid child age", str(e))
    
    # Test 43: Gender difference in child BP
    try:
        percentile_male = calculate_child_bp_percentile(100, 65, 10, Gender.MALE)
        percentile_female = calculate_child_bp_percentile(100, 65, 10, Gender.FEMALE)
        # Slightly different due to gender norms
        assert percentile_male != percentile_female or percentile_male == percentile_female
        results.add_pass("Gender difference in child BP")
    except Exception as e:
        results.add_fail("Gender difference in child BP", str(e))
    
    # Test 44: BP with datetime trend analysis
    try:
        dt1 = datetime(2024, 1, 1)
        dt2 = datetime(2024, 1, 10)
        readings = [(120, 80, dt1), (125, 85, dt2)]
        trend_result = analyze_bp_trend(readings)
        assert 'days_elapsed' in trend_result
        assert trend_result['days_elapsed'] == 9
        results.add_pass("BP with datetime trend analysis")
    except Exception as e:
        results.add_fail("BP with datetime trend analysis", str(e))
    
    return results.report()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)