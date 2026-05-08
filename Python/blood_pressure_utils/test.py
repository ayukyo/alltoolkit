#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Blood Pressure Utilities Test Suite
==================================================
Comprehensive tests for blood_pressure_utils module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Python.blood_pressure_utils.mod import (
    # Unit conversion
    convert_bp_unit, mmhg_to_kpa, kpa_to_mmhg, BPUnit,
    
    # Core functions
    calculate_pulse_pressure, calculate_map, get_map_status,
    classify_bp, get_pulse_pressure_category,
    get_age_normal_range, is_bp_age_appropriate,
    generate_recommendations, analyze_bp,
    
    # Statistics
    calculate_bp_statistics, analyze_bp_trend,
    
    # Pediatric
    calculate_child_bp_percentile, analyze_child_bp, PED_BP_DATA,
    
    # Utility
    get_bp_summary, calculate_hypertension_stage,
    
    # Enums and data classes
    Gender, BPResult, BPStatistics, ChildBPResult,
)


def test_unit_conversion():
    """测试血压单位转换"""
    print("Testing unit conversion...")
    
    # mmHg to kPa
    assert mmhg_to_kpa(120) == 15.96
    assert mmhg_to_kpa(80) == 10.64
    assert mmhg_to_kpa(100) == 13.3
    
    # kPa to mmHg
    assert kpa_to_mmhg(16) == 120.1
    assert kpa_to_mmhg(10.64) == 79.86
    
    # Generic conversion
    assert convert_bp_unit(120, BPUnit.MMHG, BPUnit.KPA) == 15.96
    assert convert_bp_unit(16, BPUnit.KPA, BPUnit.MMHG) == 120.1
    assert convert_bp_unit(120, BPUnit.MMHG, BPUnit.MMHG) == 120
    
    print("  ✓ Unit conversion tests passed")


def test_pulse_pressure():
    """测试脉压差计算"""
    print("Testing pulse pressure calculation...")
    
    # Normal pulse pressure
    pp = calculate_pulse_pressure(120, 80)
    assert pp == 40
    
    # High pulse pressure
    pp = calculate_pulse_pressure(160, 70)
    assert pp == 90
    
    # Low pulse pressure
    pp = calculate_pulse_pressure(100, 85)
    assert pp == 15
    
    print("  ✓ Pulse pressure tests passed")


def test_map():
    """测试平均动脉压计算"""
    print("Testing MAP calculation...")
    
    # Normal MAP
    map_val = calculate_map(120, 80)
    assert map_val == 93.33  # 80 + (120-80)/3 = 80 + 13.33
    
    # High MAP
    map_val = calculate_map(150, 95)
    assert map_val == 113.33  # 95 + (150-95)/3
    
    # Low MAP
    map_val = calculate_map(90, 60)
    assert map_val == 70
    
    print("  ✓ MAP tests passed")


def test_map_status():
    """测试 MAP 状态评估"""
    print("Testing MAP status...")
    
    assert get_map_status(93) == 'normal'
    assert get_map_status(70) == 'normal'
    assert get_map_status(105) == 'normal'
    assert get_map_status(65) == 'low'
    assert get_map_status(55) == 'critical_low'
    assert get_map_status(110) == 'high'
    assert get_map_status(125) == 'critical_high'
    
    print("  ✓ MAP status tests passed")


def test_bp_classification():
    """测试血压分类"""
    print("Testing BP classification...")
    
    # Optimal
    cat, label, label_en, risk, desc = classify_bp(115, 75)
    assert cat == 'optimal'
    assert risk == 'low'
    
    # Normal
    cat, label, label_en, risk, desc = classify_bp(125, 82)
    assert cat == 'normal'
    
    # High normal
    cat, label, label_en, risk, desc = classify_bp(135, 88)
    assert cat == 'high_normal'
    
    # Grade 1 hypertension
    cat, label, label_en, risk, desc = classify_bp(145, 95)
    assert cat == 'grade1_hypertension'
    assert risk == 'high'
    
    # Grade 2 hypertension
    cat, label, label_en, risk, desc = classify_bp(170, 105)
    assert cat == 'grade2_hypertension'
    
    # Grade 3 hypertension
    cat, label, label_en, risk, desc = classify_bp(185, 115)
    assert cat == 'grade3_hypertension'
    
    # Isolated systolic hypertension
    cat, label, label_en, risk, desc = classify_bp(150, 85)
    assert cat == 'isolated_systolic_hypertension'
    
    print("  ✓ BP classification tests passed")


def test_pulse_pressure_category():
    """测试脉压差分类"""
    print("Testing pulse pressure category...")
    
    # Normal
    cat, label, desc = get_pulse_pressure_category(40)
    assert cat == 'normal'
    
    # Low
    cat, label, desc = get_pulse_pressure_category(25)
    assert cat == 'low'
    
    # Increased
    cat, label, desc = get_pulse_pressure_category(55)
    assert cat == 'increased'
    
    # High
    cat, label, desc = get_pulse_pressure_category(70)
    assert cat == 'high'
    
    print("  ✓ Pulse pressure category tests passed")


def test_age_normal_range():
    """测试年龄正常血压范围"""
    print("Testing age normal range...")
    
    # Child age 10
    sys_min, sys_max, dia_min, dia_max = get_age_normal_range(10)
    assert sys_min == 102
    assert sys_max == 128
    assert dia_min == 70
    assert dia_max == 92
    
    # Adult 30
    sys_min, sys_max, dia_min, dia_max = get_age_normal_range(30)
    assert sys_min == 90
    assert sys_max == 130
    
    # Elderly 70
    sys_min, sys_max, dia_min, dia_max = get_age_normal_range(70)
    assert sys_max == 150
    
    print("  ✓ Age normal range tests passed")


def test_bp_age_appropriate():
    """测试血压年龄适宜性"""
    print("Testing BP age appropriateness...")
    
    # Normal for age
    assert is_bp_age_appropriate(110, 70, 10) == True
    assert is_bp_age_appropriate(120, 80, 35) == True
    
    # Abnormal for age
    assert is_bp_age_appropriate(150, 100, 10) == False
    
    print("  ✓ BP age appropriateness tests passed")


def test_full_analysis():
    """测试完整血压分析"""
    print("Testing full BP analysis...")
    
    result = analyze_bp(115, 75, 35)  # 使用更低的血压值
    
    assert result.systolic == 115
    assert result.diastolic == 75
    assert result.category == 'optimal'
    assert result.pulse_pressure == 40
    assert result.map == 88.33
    assert result.map_status == 'normal'
    assert result.age_appropriate == True
    assert len(result.recommendations) > 0
    
    # Test with high BP
    result2 = analyze_bp(155, 95, 50)
    assert result2.category in ['grade1_hypertension', 'grade2_hypertension']
    assert result2.risk_level == 'high'
    
    print("  ✓ Full analysis tests passed")


def test_statistics():
    """测试血压统计"""
    print("Testing BP statistics...")
    
    readings = [(120, 80), (122, 82), (118, 78), (125, 83), (119, 79)]
    stats = calculate_bp_statistics(readings)
    
    assert stats.readings_count == 5
    assert stats.systolic_mean == 120.8
    assert stats.systolic_min == 118
    assert stats.systolic_max == 125
    assert stats.diastolic_mean == 80.4
    assert stats.pulse_pressure_mean == 40.4
    assert stats.dominant_category == 'normal'
    
    print("  ✓ Statistics tests passed")


def test_trend_analysis():
    """测试趋势分析"""
    print("Testing trend analysis...")
    
    readings = [(120, 80, None), (125, 85, None), (130, 90, None)]
    trend = analyze_bp_trend(readings)
    
    assert trend['systolic_trend'] == 'increasing'
    assert trend['diastolic_trend'] == 'increasing'
    assert trend['systolic_change'] == 10
    assert trend['diastolic_change'] == 10
    
    print("  ✓ Trend analysis tests passed")


def test_child_bp():
    """测试儿童血压分析"""
    print("Testing child BP analysis...")
    
    result = analyze_child_bp(105, 70, 10, Gender.MALE)
    
    assert result.systolic == 105
    assert result.diastolic == 70
    assert result.age == 10
    assert result.percentile >= 1 and result.percentile <= 99
    assert result.risk_level in ['low', 'moderate', 'high']
    assert len(result.recommendations) > 0
    
    print("  ✓ Child BP tests passed")


def test_hypertension_stage():
    """测试高血压分期"""
    print("Testing hypertension stage...")
    
    assert calculate_hypertension_stage(118, 76) == 'Normal'
    assert calculate_hypertension_stage(125, 75) == 'Elevated'
    assert calculate_hypertension_stage(135, 85) == 'Hypertension Stage 1'
    assert calculate_hypertension_stage(138, 88) == 'Hypertension Stage 1'
    assert calculate_hypertension_stage(145, 92) == 'Hypertension Stage 2'
    assert calculate_hypertension_stage(165, 105) == 'Hypertension Stage 2'
    assert calculate_hypertension_stage(185, 120) == 'Hypertensive Crisis'
    
    print("  ✓ Hypertension stage tests passed")


def test_summary():
    """测试简要说明"""
    print("Testing BP summary...")
    
    summary = get_bp_summary(115, 75)
    assert '115/75' in summary
    assert '理想血压' in summary
    
    summary = get_bp_summary(145, 95)
    assert '145/95' in summary
    assert '高血压' in summary
    
    print("  ✓ Summary tests passed")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("Blood Pressure Utilities - Test Suite")
    print("=" * 60 + "\n")
    
    test_unit_conversion()
    test_pulse_pressure()
    test_map()
    test_map_status()
    test_bp_classification()
    test_pulse_pressure_category()
    test_age_normal_range()
    test_bp_age_appropriate()
    test_full_analysis()
    test_statistics()
    test_trend_analysis()
    test_child_bp()
    test_hypertension_stage()
    test_summary()
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()