"""
Water Intake Utils 测试
==========================================

测试饮水量计算工具的所有功能。

作者: AllToolkit 自动化生成
日期: 2026-05-23
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    WaterIntakeCalculator,
    ActivityLevel,
    ClimateType,
    HydrationStatus,
    calculate_daily_water,
    get_quick_schedule
)
from datetime import datetime, timedelta


def test_calculate_daily_intake_basic():
    """测试基础每日饮水量计算"""
    calc = WaterIntakeCalculator()
    
    # 70kg 成年人，中度活动，温和气候
    result = calc.calculate_daily_intake(weight_kg=70)
    
    assert result['weight_kg'] == 70
    assert result['base_intake_ml'] == 70 * 30  # 30ml/kg
    assert result['total_intake_ml'] >= 1500  # 最小1500ml
    assert result['total_intake_ml'] <= 4500  # 最大4500ml
    print("✅ test_calculate_daily_intake_basic")


def test_calculate_daily_intake_activity_levels():
    """测试不同活动水平的饮水量"""
    calc = WaterIntakeCalculator()
    
    # 久坐人群
    sedentary = calc.calculate_daily_intake(
        weight_kg=70,
        activity_level=ActivityLevel.SEDENTARY
    )
    
    # 活跃人群
    active = calc.calculate_daily_intake(
        weight_kg=70,
        activity_level=ActivityLevel.ACTIVE
    )
    
    # 非常活跃人群
    very_active = calc.calculate_daily_intake(
        weight_kg=70,
        activity_level=ActivityLevel.VERY_ACTIVE
    )
    
    # 验证活动水平影响
    assert sedentary['total_intake_ml'] < active['total_intake_ml']
    assert active['total_intake_ml'] < very_active['total_intake_ml']
    assert sedentary['activity_multiplier'] == 1.0
    assert very_active['activity_multiplier'] == 1.5
    print("✅ test_calculate_daily_intake_activity_levels")


def test_calculate_daily_intake_climate():
    """测试不同气候的饮水量"""
    calc = WaterIntakeCalculator()
    
    # 寒冷气候
    cold = calc.calculate_daily_intake(
        weight_kg=70,
        climate=ClimateType.COLD
    )
    
    # 炎热气候
    hot = calc.calculate_daily_intake(
        weight_kg=70,
        climate=ClimateType.HOT
    )
    
    # 酷热气候
    very_hot = calc.calculate_daily_intake(
        weight_kg=70,
        climate=ClimateType.VERY_HOT
    )
    
    # 验证气候影响
    assert cold['total_intake_ml'] < hot['total_intake_ml']
    assert hot['total_intake_ml'] < very_hot['total_intake_ml']
    assert cold['climate_multiplier'] == 0.9
    assert very_hot['climate_multiplier'] == 1.4
    print("✅ test_calculate_daily_intake_climate")


def test_calculate_daily_intake_exercise():
    """测试运动对饮水量的影响"""
    calc = WaterIntakeCalculator()
    
    # 无运动
    no_exercise = calc.calculate_daily_intake(
        weight_kg=70,
        exercise_minutes=0
    )
    
    # 30分钟运动
    exercise_30 = calc.calculate_daily_intake(
        weight_kg=70,
        exercise_minutes=30
    )
    
    # 60分钟运动
    exercise_60 = calc.calculate_daily_intake(
        weight_kg=70,
        exercise_minutes=60
    )
    
    # 验证运动影响
    assert no_exercise['exercise_addition_ml'] == 0
    assert exercise_30['exercise_addition_ml'] == 350  # 每30分钟350ml
    assert exercise_60['exercise_addition_ml'] == 700
    assert exercise_30['total_intake_ml'] > no_exercise['total_intake_ml']
    print("✅ test_calculate_daily_intake_exercise")


def test_calculate_daily_intake_special_conditions():
    """测试特殊情况对饮水量的影响"""
    calc = WaterIntakeCalculator()
    
    # 无特殊情况
    normal = calc.calculate_daily_intake(weight_kg=70)
    
    # 孕期
    pregnancy = calc.calculate_daily_intake(
        weight_kg=70,
        special_conditions=['pregnancy']
    )
    
    # 哺乳期
    breastfeeding = calc.calculate_daily_intake(
        weight_kg=70,
        special_conditions=['breastfeeding']
    )
    
    # 发烧
    fever = calc.calculate_daily_intake(
        weight_kg=70,
        special_conditions=['illness_fever']
    )
    
    # 多种特殊情况
    multiple = calc.calculate_daily_intake(
        weight_kg=70,
        special_conditions=['pregnancy', 'altitude_high']
    )
    
    # 验证特殊情况调整
    assert pregnancy['special_addition_ml'] == 300
    assert breastfeeding['special_addition_ml'] == 700
    assert fever['special_addition_ml'] == 500
    assert multiple['special_addition_ml'] == 800  # 300 + 500
    assert pregnancy['total_intake_ml'] > normal['total_intake_ml']
    print("✅ test_calculate_daily_intake_special_conditions")


def test_calculate_daily_intake_age():
    """测试年龄对饮水量的影响"""
    calc = WaterIntakeCalculator()
    
    # 青少年（需要更多水）
    teen = calc.calculate_daily_intake(
        weight_kg=50,
        age=15
    )
    
    # 成年人
    adult = calc.calculate_daily_intake(
        weight_kg=70,
        age=35
    )
    
    # 老年人（可能需要更少）
    elderly = calc.calculate_daily_intake(
        weight_kg=70,
        age=75
    )
    
    # 验证年龄调整
    assert teen['age_adjustment_ml'] > 0
    assert elderly['age_adjustment_ml'] < 0
    print("✅ test_calculate_daily_intake_age")


def test_calculate_daily_intake_bounds():
    """测试饮水量边界值"""
    calc = WaterIntakeCalculator()
    
    # 极轻体重
    very_light = calc.calculate_daily_intake(weight_kg=30)
    assert very_light['total_intake_ml'] >= 1500  # 最小值
    
    # 极重体重
    very_heavy = calc.calculate_daily_intake(weight_kg=150)
    assert very_heavy['total_intake_ml'] <= 4500  # 最大值
    
    # 无效体重
    try:
        calc.calculate_daily_intake(weight_kg=0)
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    try:
        calc.calculate_daily_intake(weight_kg=-10)
        assert False, "应该抛出异常"
    except ValueError:
        pass
    print("✅ test_calculate_daily_intake_bounds")


def test_calculate_hourly_intake():
    """测试每小时饮水量计算"""
    calc = WaterIntakeCalculator()
    
    result = calc.calculate_hourly_intake(
        daily_intake_ml=2000,
        waking_hours=16
    )
    
    assert result['daily_intake_ml'] == 2000
    assert result['waking_hours'] == 16
    assert result['hourly_intake_ml'] == 125  # 2000 / 16
    assert result['sips_per_hour'] == 4  # 125 / 30
    assert result['bottles_500ml'] == 4.0
    
    # 无效输入
    try:
        calc.calculate_hourly_intake(daily_intake_ml=0)
        assert False, "应该抛出异常"
    except ValueError:
        pass
    print("✅ test_calculate_hourly_intake")


def test_generate_drinking_schedule():
    """测试饮水时间表生成"""
    calc = WaterIntakeCalculator()
    
    schedule = calc.generate_drinking_schedule(
        daily_intake_ml=2000,
        wake_time=(7, 0),
        sleep_time=(23, 0),
        num_reminders=8
    )
    
    assert len(schedule) == 8
    
    # 验证累计量
    for i, s in enumerate(schedule):
        assert s['reminder_number'] == i + 1
        assert 'time' in s
        assert s['amount_ml'] > 0
        assert s['cumulative_ml'] >= s['amount_ml']
        assert 0 <= s['percentage'] <= 100
    
    # 验证最后一条记录百分比
    assert schedule[-1]['percentage'] == 100.0
    
    # 验证睡前减少饮水
    late_night = [s for s in schedule if s['hours'] >= 21]
    for s in late_night:
        # 睡前饮水量应该减少
        assert s['amount_ml'] <= 250
    print("✅ test_generate_drinking_schedule")


def test_generate_drinking_schedule_custom_times():
    """测试自定义时间饮水时间表"""
    calc = WaterIntakeCalculator()
    
    # 夜班工作者
    night_schedule = calc.generate_drinking_schedule(
        daily_intake_ml=2000,
        wake_time=(18, 0),  # 傍晚起床
        sleep_time=(8, 0),   # 早上睡觉
        num_reminders=6
    )
    
    assert len(night_schedule) == 6
    
    # 验证时间范围
    for s in night_schedule:
        assert 'time' in s
        assert s['amount_ml'] > 0
    print("✅ test_generate_drinking_schedule_custom_times")


def test_record_intake():
    """测试饮水记录"""
    calc = WaterIntakeCalculator()
    
    # 记录饮水
    record1 = calc.record_intake(
        amount_ml=250,
        beverage_type="water",
        note="早晨"
    )
    
    assert record1['id'] == 1
    assert record1['amount_ml'] == 250
    assert record1['beverage_type'] == "water"
    assert 'timestamp' in record1
    
    # 记录更多
    record2 = calc.record_intake(amount_ml=500, beverage_type="tea")
    record3 = calc.record_intake(amount_ml=300, beverage_type="coffee")
    
    assert record2['id'] == 2
    assert record3['id'] == 3
    assert len(calc.records) == 3
    
    # 无效输入
    try:
        calc.record_intake(amount_ml=0)
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    try:
        calc.record_intake(amount_ml=-100)
        assert False, "应该抛出异常"
    except ValueError:
        pass
    print("✅ test_record_intake")


def test_get_daily_summary():
    """测试每日摘要"""
    calc = WaterIntakeCalculator()
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 记录饮水
    calc.record_intake(amount_ml=250, beverage_type="water")
    calc.record_intake(amount_ml=300, beverage_type="tea")
    calc.record_intake(amount_ml=200, beverage_type="water")
    
    # 获取摘要
    summary = calc.get_daily_summary(target_intake_ml=2000)
    
    assert summary['date'] == today
    assert summary['total_intake_ml'] == 750
    assert summary['record_count'] == 3
    assert 'water' in summary['by_beverage_type']
    assert 'tea' in summary['by_beverage_type']
    assert summary['target_intake_ml'] == 2000
    assert summary['progress_percentage'] == 37.5
    assert summary['remaining_ml'] == 1250
    assert not summary['target_met']
    
    # 无目标的情况
    summary_no_target = calc.get_daily_summary()
    assert 'target_intake_ml' not in summary_no_target
    print("✅ test_get_daily_summary")


def test_assess_hydration():
    """测试补水状态评估"""
    calc = WaterIntakeCalculator()
    
    # 严重脱水
    severe = calc.assess_hydration(
        current_intake_ml=500,
        target_intake_ml=2000
    )
    assert severe['status'] == 'dehydrated_severe'
    assert severe['progress_ratio'] == 0.25
    assert len(severe['recommendations']) > 0
    
    # 脱水
    dehydrated = calc.assess_hydration(
        current_intake_ml=1200,
        target_intake_ml=2000
    )
    assert dehydrated['status'] == 'dehydrated'
    
    # 轻度脱水
    slight = calc.assess_hydration(
        current_intake_ml=1600,
        target_intake_ml=2000
    )
    assert slight['status'] == 'slightly_dehydrated'
    
    # 最佳状态
    optimal = calc.assess_hydration(
        current_intake_ml=2000,
        target_intake_ml=2000
    )
    assert optimal['status'] == 'optimal'
    
    # 补水良好
    well = calc.assess_hydration(
        current_intake_ml=2400,
        target_intake_ml=2000
    )
    assert well['status'] == 'well_hydrated'
    
    # 饮水过量
    over = calc.assess_hydration(
        current_intake_ml=3000,
        target_intake_ml=2000
    )
    assert over['status'] == 'overhydrated'
    print("✅ test_assess_hydration")


def test_assess_hydration_with_urine_color():
    """测试尿液颜色辅助评估"""
    calc = WaterIntakeCalculator()
    
    # 淡黄色 - 正常
    pale = calc.assess_hydration(
        current_intake_ml=2000,
        target_intake_ml=2000,
        urine_color='pale_yellow'
    )
    assert pale['urine_color_assessment']['normal'] == True
    assert pale['urine_color_assessment']['assessment'] == '补水良好'
    
    # 深黄色 - 脱水
    dark = calc.assess_hydration(
        current_intake_ml=2000,
        target_intake_ml=2000,
        urine_color='dark_yellow'
    )
    assert dark['urine_color_assessment']['normal'] == False
    
    # 透明 - 饮水过量
    clear = calc.assess_hydration(
        current_intake_ml=2000,
        target_intake_ml=2000,
        urine_color='clear'
    )
    assert clear['urine_color_assessment']['assessment'] == '饮水过量'
    print("✅ test_assess_hydration_with_urine_color")


def test_calculate_sweat_loss():
    """测试出汗量计算"""
    calc = WaterIntakeCalculator()
    
    result = calc.calculate_sweat_loss(
        weight_before_kg=70,
        weight_after_kg=69.5,
        fluid_intake_ml=500,
        urine_output_ml=0,
        duration_minutes=60
    )
    
    assert result['weight_loss_kg'] == 0.5
    assert result['weight_loss_percent'] > 0
    assert result['sweat_loss_ml'] == 1000  # 0.5kg + 500ml
    assert result['sweat_rate_ml_per_hour'] == 1000
    assert result['rehydration_needed_ml'] > 0
    assert len(result['recommendations']) > 0
    
    # 不同脱水程度
    severe_dehydration = calc.calculate_sweat_loss(
        weight_before_kg=70,
        weight_after_kg=66,  # 4kg 丢失，约5.7%
        fluid_intake_ml=0,
        duration_minutes=120
    )
    assert '严重脱水' in severe_dehydration['dehydration_severity'] or \
           severe_dehydration['weight_loss_percent'] > 4
    print("✅ test_calculate_sweat_loss")


def test_get_beverage_equivalent():
    """测试饮料等效量"""
    calc = WaterIntakeCalculator()
    
    equivalents = calc.get_beverage_equivalent(1000)
    
    # 水的等效量应该等于原量
    assert equivalents['water']['equivalent_ml'] == 1000
    assert equivalents['water']['hydration_factor'] == 1.0
    
    # 咖啡需要更多
    assert equivalents['coffee']['equivalent_ml'] > 1000
    assert equivalents['coffee']['hydration_factor'] == 0.85
    
    # 啤酒需要更多
    assert equivalents['beer']['equivalent_ml'] > equivalents['water']['equivalent_ml']
    assert equivalents['beer']['hydration_factor'] == 0.6
    
    # 验证所有饮料都有备注
    for beverage, info in equivalents.items():
        assert 'equivalent_ml' in info
        assert 'hydration_factor' in info
        assert 'note' in info
    print("✅ test_get_beverage_equivalent")


def test_calculate_for_sport():
    """测试运动补水方案"""
    calc = WaterIntakeCalculator()
    
    # 跑步 - 高强度
    running = calc.calculate_for_sport(
        sport_type='running',
        duration_minutes=60,
        intensity='high',
        weight_kg=70,
        temperature_c=25
    )
    
    assert running['sport_type'] == 'running'
    assert running['duration_minutes'] == 60
    assert running['intensity'] == 'high'
    assert running['estimated_sweat_loss_ml'] > 0
    assert 'hydration_plan' in running
    assert 'before_exercise_ml' in running['hydration_plan']
    assert 'during_exercise' in running['hydration_plan']
    assert 'after_exercise_ml' in running['hydration_plan']
    assert len(running['tips']) > 0
    
    # 游泳 - 出汗较少
    swimming = calc.calculate_for_sport(
        sport_type='swimming',
        duration_minutes=60,
        intensity='moderate',
        weight_kg=70
    )
    
    assert swimming['estimated_sweat_loss_ml'] < running['estimated_sweat_loss_ml']
    
    # 高温环境
    hot_running = calc.calculate_for_sport(
        sport_type='running',
        duration_minutes=60,
        intensity='moderate',
        weight_kg=70,
        temperature_c=35
    )
    
    cool_running = calc.calculate_for_sport(
        sport_type='running',
        duration_minutes=60,
        intensity='moderate',
        weight_kg=70,
        temperature_c=15
    )
    
    assert hot_running['estimated_sweat_loss_ml'] > cool_running['estimated_sweat_loss_ml']
    print("✅ test_calculate_for_sport")


def test_clear_records():
    """测试清除记录"""
    calc = WaterIntakeCalculator()
    
    # 添加记录
    calc.record_intake(amount_ml=250)
    calc.record_intake(amount_ml=300)
    
    assert len(calc.records) == 2
    
    # 清除今天的记录
    today = datetime.now().strftime('%Y-%m-%d')
    calc.clear_records(date=today)
    
    # 如果记录是今天的，应该被清除
    assert len(calc.records) == 0
    
    # 添加记录并清除全部
    calc.record_intake(amount_ml=250)
    calc.record_intake(amount_ml=300)
    calc.clear_records()
    
    assert len(calc.records) == 0
    print("✅ test_clear_records")


def test_export_records():
    """测试导出记录"""
    calc = WaterIntakeCalculator()
    
    calc.record_intake(amount_ml=250, beverage_type="water")
    calc.record_intake(amount_ml=300, beverage_type="tea")
    
    # 导出为字典
    dict_export = calc.export_records(format="dict")
    assert isinstance(dict_export, list)
    assert len(dict_export) == 2
    
    # 导出为JSON
    json_export = calc.export_records(format="json")
    assert isinstance(json_export, str)
    assert "water" in json_export
    assert "tea" in json_export
    print("✅ test_export_records")


def test_convenience_functions():
    """测试便捷函数"""
    # 快速计算每日饮水量
    result = calculate_daily_water(
        weight_kg=70,
        activity_level='active',
        climate='hot',
        exercise_minutes=30
    )
    
    assert 'total_intake_ml' in result
    assert result['weight_kg'] == 70
    assert result['exercise_addition_ml'] == 350
    
    # 快速生成时间表
    schedule = get_quick_schedule(total_ml=2000, wake_hour=6)
    
    assert len(schedule) > 0
    assert all('time' in s for s in schedule)
    assert all('amount_ml' in s for s in schedule)
    print("✅ test_convenience_functions")


def test_comprehensive_scenario():
    """测试综合场景"""
    calc = WaterIntakeCalculator()
    
    # 场景：70kg 活跃成年人，夏天，运动1小时
    daily = calc.calculate_daily_intake(
        weight_kg=70,
        activity_level=ActivityLevel.ACTIVE,
        climate=ClimateType.HOT,
        exercise_minutes=60
    )
    
    # 生成时间表
    schedule = calc.generate_drinking_schedule(
        daily_intake_ml=daily['total_intake_ml'],
        num_reminders=8
    )
    
    # 模拟一天的饮水
    for i, s in enumerate(schedule[:4]):
        calc.record_intake(
            amount_ml=s['amount_ml'],
            beverage_type="water" if i % 2 == 0 else "tea"
        )
    
    # 检查进度
    summary = calc.get_daily_summary(target_intake_ml=daily['total_intake_ml'])
    
    assert summary['progress_percentage'] > 0
    assert summary['total_intake_ml'] > 0
    
    # 评估状态
    hydration = calc.assess_hydration(
        current_intake_ml=summary['total_intake_ml'],
        target_intake_ml=daily['total_intake_ml']
    )
    
    assert 'status' in hydration
    assert 'recommendations' in hydration
    print("✅ test_comprehensive_scenario")


def test_extreme_values():
    """测试极端值"""
    calc = WaterIntakeCalculator()
    
    # 非常小的体重
    tiny = calc.calculate_daily_intake(weight_kg=20)
    assert tiny['total_intake_ml'] >= 1500  # 最小值限制
    
    # 非常大的体重
    huge = calc.calculate_daily_intake(weight_kg=200)
    assert huge['total_intake_ml'] <= 4500  # 最大值限制
    
    # 极端运动量
    extreme_exercise = calc.calculate_daily_intake(
        weight_kg=70,
        exercise_minutes=300  # 5小时
    )
    assert extreme_exercise['exercise_addition_ml'] == 3500  # 10 * 350
    
    # 极端热量
    extreme_heat = calc.calculate_daily_intake(
        weight_kg=70,
        climate=ClimateType.VERY_HOT,
        activity_level=ActivityLevel.VERY_ACTIVE,
        exercise_minutes=120
    )
    assert extreme_heat['total_intake_ml'] >= 1500
    print("✅ test_extreme_values")


def run_all_tests():
    """运行所有测试"""
    tests = [
        test_calculate_daily_intake_basic,
        test_calculate_daily_intake_activity_levels,
        test_calculate_daily_intake_climate,
        test_calculate_daily_intake_exercise,
        test_calculate_daily_intake_special_conditions,
        test_calculate_daily_intake_age,
        test_calculate_daily_intake_bounds,
        test_calculate_hourly_intake,
        test_generate_drinking_schedule,
        test_generate_drinking_schedule_custom_times,
        test_record_intake,
        test_get_daily_summary,
        test_assess_hydration,
        test_assess_hydration_with_urine_color,
        test_calculate_sweat_loss,
        test_get_beverage_equivalent,
        test_calculate_for_sport,
        test_clear_records,
        test_export_records,
        test_convenience_functions,
        test_comprehensive_scenario,
        test_extreme_values
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print(f"{'='*50}")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)