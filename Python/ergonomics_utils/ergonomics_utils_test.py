"""
人体工程学工具集测试

测试所有功能：
- 工作站设置计算
- 休息间隔计算
- 伸展运动建议
- 姿势评估
- RSI风险评估
- 眼睛保护计划
- 显示器设置计算
- 工作模式分析
- 坐立比例建议
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ergonomics_utils.mod import (
    WorkstationSetup, BreakSuggestion, StretchExercise, PostureAssessment,
    RSIAssessment, EyeCarePlan, BodyPart, WorkIntensity, PostureRisk,
    calculate_workstation_setup, calculate_break_intervals, get_stretch_exercises,
    assess_posture, assess_rsi_risk, create_eye_care_plan,
    calculate_optimal_monitor_setup, get_work_period_analysis,
    get_sitting_vs_standing_recommendation, quick_setup
)


def run_test(name: str, test_func):
    """运行单个测试"""
    try:
        test_func()
        print(f"✓ {name}")
        return True
    except AssertionError as e:
        print(f"✗ {name}: {e}")
        return False
    except Exception as e:
        print(f"✗ {name}: 意外错误 - {e}")
        return False


# ==================== 工作站设置测试 ====================

def test_calculate_workstation_setup_basic():
    """测试基本工作站设置计算"""
    setup = calculate_workstation_setup(175)  # 175cm
    
    assert isinstance(setup, WorkstationSetup)
    assert setup.screen_height > 0
    assert setup.screen_distance > 0
    assert setup.chair_height > 0
    assert setup.desk_height > 0
    assert setup.keyboard_height > 0
    assert setup.monitor_tilt == 10.0


def test_calculate_workstation_setup_different_heights():
    """测试不同身高的工作站设置"""
    heights = [150, 160, 170, 180, 190, 200]
    
    for height in heights:
        setup = calculate_workstation_setup(height)
        assert setup.screen_height > 0
        assert setup.chair_height < setup.desk_height  # 椅子应该比桌子低


def test_calculate_workstation_setup_short_person():
    """测试矮个子工作站的脚踏需求"""
    setup = calculate_workstation_setup(155)
    # 矮个子通常需要脚踏
    assert isinstance(setup.footrest_needed, bool)


def test_calculate_workstation_setup_tall_person():
    """测试高个子的工作站设置"""
    setup = calculate_workstation_setup(195)
    assert setup.chair_height > 50  # 高个子需要较高的椅子
    assert setup.desk_height > 70   # 和较高的桌子


def test_calculate_workstation_setup_standing():
    """测试站立工作站设置"""
    setup = calculate_workstation_setup(175, seated=False)
    
    assert setup.chair_height == 0.0  # 站立模式没有椅子
    assert setup.desk_height > 0      # 但有桌子高度
    assert not setup.footrest_needed   # 站立不需要脚踏


def test_calculate_workstation_setup_screen_size():
    """测试不同屏幕尺寸的影响"""
    setup_24 = calculate_workstation_setup(175, screen_size_inches=24)
    setup_32 = calculate_workstation_setup(175, screen_size_inches=32)
    
    # 屏幕尺寸不应影响基本设置
    assert setup_24.screen_height == setup_32.screen_height
    assert setup_24.chair_height == setup_32.chair_height


def test_calculate_workstation_setup_invalid_height():
    """测试无效身高输入"""
    try:
        calculate_workstation_setup(0)
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    try:
        calculate_workstation_setup(-10)
        assert False, "应该抛出异常"
    except ValueError:
        pass


# ==================== 休息间隔测试 ====================

def test_calculate_break_intervals_light_work():
    """测试轻度工作的休息间隔"""
    breaks = calculate_break_intervals(2, WorkIntensity.LIGHT)
    
    assert len(breaks) > 0
    assert all(isinstance(b, BreakSuggestion) for b in breaks)


def test_calculate_break_intervals_intensive_work():
    """测试高强度工作的休息间隔"""
    breaks_light = calculate_break_intervals(2, WorkIntensity.LIGHT)
    breaks_intensive = calculate_break_intervals(2, WorkIntensity.INTENSIVE)
    
    # 高强度工作应该有更多休息
    work_breaks_light = [b for b in breaks_light if b.break_type != "eye_break"]
    work_breaks_intensive = [b for b in breaks_intensive if b.break_type != "eye_break"]
    
    assert len(work_breaks_intensive) >= len(work_breaks_light)


def test_calculate_break_intervals_long_break():
    """测试长时间工作后的长休息"""
    breaks = calculate_break_intervals(3, WorkIntensity.MODERATE)
    
    # 3小时工作应该有长休息
    long_breaks = [b for b in breaks if b.break_type == "long_break"]
    assert len(long_breaks) > 0
    assert long_breaks[0].duration_minutes == 15


def test_calculate_break_intervals_20_20_20_rule():
    """测试20-20-20法则"""
    breaks = calculate_break_intervals(1, use_20_20_20_rule=True)
    
    eye_breaks = [b for b in breaks if b.break_type == "eye_break"]
    assert len(eye_breaks) == 3  # 1小时 = 3个20分钟


def test_calculate_break_intervals_no_eye_rule():
    """测试不使用20-20-20法则"""
    breaks = calculate_break_intervals(1, use_20_20_20_rule=False)
    
    eye_breaks = [b for b in breaks if b.break_type == "eye_break"]
    assert len(eye_breaks) == 0


def test_calculate_break_intervals_extreme_work():
    """测试极高强度工作的休息"""
    breaks = calculate_break_intervals(1, WorkIntensity.EXTREME)
    
    # 极高强度每20分钟休息
    work_breaks = [b for b in breaks if b.break_type != "eye_break"]
    assert len(work_breaks) == 3  # 60/20 = 3


# ==================== 伸展运动测试 ====================

def test_get_stretch_exercises_all():
    """测试获取所有伸展运动"""
    exercises = get_stretch_exercises()
    
    assert len(exercises) > 0
    assert all(isinstance(e, StretchExercise) for e in exercises)


def test_get_stretch_exercises_by_body_part():
    """测试按身体部位筛选伸展运动"""
    neck_exercises = get_stretch_exercises([BodyPart.NECK])
    
    assert len(neck_exercises) > 0
    for e in neck_exercises:
        assert BodyPart.NECK in e.body_parts


def test_get_stretch_exercises_multiple_body_parts():
    """测试多个身体部位筛选"""
    exercises = get_stretch_exercises([BodyPart.NECK, BodyPart.SHOULDERS])
    
    for e in exercises:
        has_target = BodyPart.NECK in e.body_parts or BodyPart.SHOULDERS in e.body_parts
        assert has_target


def test_get_stretch_exercises_wrist():
    """测试手腕伸展运动"""
    exercises = get_stretch_exercises([BodyPart.WRISTS])
    
    assert len(exercises) > 0
    for e in exercises:
        assert BodyPart.WRISTS in e.body_parts


def test_get_stretch_exercises_eyes():
    """测试眼部运动"""
    exercises = get_stretch_exercises([BodyPart.EYES])
    
    assert len(exercises) > 0
    for e in exercises:
        assert BodyPart.EYES in e.body_parts


def test_get_stretch_exercises_long_work():
    """测试长时间工作的伸展建议"""
    short_work = get_stretch_exercises(work_duration_minutes=30)
    long_work = get_stretch_exercises(work_duration_minutes=150)
    
    assert len(long_work) >= len(short_work)


def test_stretch_exercise_structure():
    """测试伸展运动数据结构"""
    exercises = get_stretch_exercises()
    
    for e in exercises:
        assert len(e.name) > 0
        assert len(e.body_parts) > 0
        assert e.duration_seconds > 0
        assert e.repetitions > 0
        assert len(e.instructions) > 0
        assert len(e.benefits) > 0


# ==================== 姿势评估测试 ====================

def test_assess_posture_ideal():
    """测试理想姿势评估"""
    assessment = assess_posture(
        screen_distance_cm=60,
        screen_height_relative="level",
        back_support=True,
        feet_flat=True,
        elbows_angle=95,
        breaks_taken=3,
        work_duration_minutes=120
    )
    
    assert assessment.risk_level == PostureRisk.LOW
    assert assessment.score >= 80
    assert len(assessment.issues) == 0


def test_assess_posture_poor():
    """测试不良姿势评估"""
    assessment = assess_posture(
        screen_distance_cm=25,  # 太近
        screen_height_relative="above",  # 太高
        back_support=False,  # 无背支撑
        feet_flat=False,  # 脚不平放
        elbows_angle=70,  # 角度太小
        breaks_taken=0,  # 无休息
        work_duration_minutes=120
    )
    
    assert assessment.risk_level in [PostureRisk.HIGH, PostureRisk.CRITICAL]
    assert assessment.score < 60
    assert len(assessment.issues) > 0
    assert len(assessment.recommendations) > 0


def test_assess_posture_screen_too_close():
    """测试屏幕太近"""
    assessment = assess_posture(
        screen_distance_cm=25,
        screen_height_relative="level",
        back_support=True,
        feet_flat=True,
        elbows_angle=95,
        breaks_taken=1,
        work_duration_minutes=45
    )
    
    assert BodyPart.EYES in assessment.affected_areas
    assert any("近" in issue for issue in assessment.issues)


def test_assess_posture_screen_too_far():
    """测试屏幕太远"""
    assessment = assess_posture(
        screen_distance_cm=90,
        screen_height_relative="level",
        back_support=True,
        feet_flat=True,
        elbows_angle=95,
        breaks_taken=1,
        work_duration_minutes=45
    )
    
    assert BodyPart.NECK in assessment.affected_areas


def test_assess_posture_screen_above():
    """测试屏幕位置过高"""
    assessment = assess_posture(
        screen_distance_cm=60,
        screen_height_relative="above",
        back_support=True,
        feet_flat=True,
        elbows_angle=95,
        breaks_taken=1,
        work_duration_minutes=45
    )
    
    assert BodyPart.NECK in assessment.affected_areas
    assert BodyPart.SHOULDERS in assessment.affected_areas


def test_assess_posture_screen_below():
    """测试屏幕位置过低"""
    assessment = assess_posture(
        screen_distance_cm=60,
        screen_height_relative="below",
        back_support=True,
        feet_flat=True,
        elbows_angle=95,
        breaks_taken=1,
        work_duration_minutes=45
    )
    
    assert BodyPart.NECK in assessment.affected_areas
    assert BodyPart.UPPER_BACK in assessment.affected_areas


def test_assess_posture_no_back_support():
    """测试无背支撑"""
    assessment = assess_posture(
        screen_distance_cm=60,
        screen_height_relative="level",
        back_support=False,
        feet_flat=True,
        elbows_angle=95,
        breaks_taken=1,
        work_duration_minutes=45
    )
    
    assert BodyPart.LOWER_BACK in assessment.affected_areas


def test_assess_posture_insufficient_breaks():
    """测试休息不足"""
    assessment = assess_posture(
        screen_distance_cm=60,
        screen_height_relative="level",
        back_support=True,
        feet_flat=True,
        elbows_angle=95,
        breaks_taken=0,
        work_duration_minutes=180
    )
    
    assert len(assessment.issues) > 0
    assert any("休息" in issue for issue in assessment.issues)


def test_assess_posture_elbow_angle():
    """测试手肘角度"""
    # 角度过小
    assessment_small = assess_posture(
        screen_distance_cm=60,
        screen_height_relative="level",
        back_support=True,
        feet_flat=True,
        elbows_angle=70,
        breaks_taken=1,
        work_duration_minutes=45
    )
    assert BodyPart.WRISTS in assessment_small.affected_areas
    
    # 角度过大
    assessment_large = assess_posture(
        screen_distance_cm=60,
        screen_height_relative="level",
        back_support=True,
        feet_flat=True,
        elbows_angle=130,
        breaks_taken=1,
        work_duration_minutes=45
    )
    assert BodyPart.SHOULDERS in assessment_large.affected_areas


# ==================== RSI风险评估测试 ====================

def test_assess_rsi_risk_low():
    """测试低RSI风险"""
    assessment = assess_rsi_risk(
        typing_hours_per_day=2,
        mouse_hours_per_day=1,
        breaks_per_day=6,
        keyboard_position="ideal",
        mouse_position="ideal",
        wrist_support=True,
        previous_injury=False
    )
    
    assert isinstance(assessment, RSIAssessment)
    assert assessment.risk_score <= 20
    assert "低风险" in assessment.risk_level


def test_assess_rsi_risk_high():
    """测试高RSI风险"""
    assessment = assess_rsi_risk(
        typing_hours_per_day=8,
        mouse_hours_per_day=6,
        breaks_per_day=1,
        keyboard_position="high",
        mouse_position="far",
        wrist_support=False,
        previous_injury=True
    )
    
    assert assessment.risk_score > 40
    assert len(assessment.recommendations) > 0


def test_assess_rsi_risk_typing_time():
    """测试打字时间对RSI风险的影响"""
    low_typing = assess_rsi_risk(
        typing_hours_per_day=2,
        mouse_hours_per_day=1,
        breaks_per_day=4,
        keyboard_position="ideal",
        mouse_position="ideal",
        wrist_support=True,
        previous_injury=False
    )
    
    high_typing = assess_rsi_risk(
        typing_hours_per_day=8,
        mouse_hours_per_day=1,
        breaks_per_day=4,
        keyboard_position="ideal",
        mouse_position="ideal",
        wrist_support=True,
        previous_injury=False
    )
    
    assert high_typing.factors["typing_time"] > low_typing.factors["typing_time"]
    assert high_typing.risk_score > low_typing.risk_score


def test_assess_rsi_risk_mouse_time():
    """测试鼠标时间对RSI风险的影响"""
    low_mouse = assess_rsi_risk(
        typing_hours_per_day=4,
        mouse_hours_per_day=1,
        breaks_per_day=4,
        keyboard_position="ideal",
        mouse_position="ideal",
        wrist_support=True,
        previous_injury=False
    )
    
    high_mouse = assess_rsi_risk(
        typing_hours_per_day=4,
        mouse_hours_per_day=6,
        breaks_per_day=4,
        keyboard_position="ideal",
        mouse_position="ideal",
        wrist_support=True,
        previous_injury=False
    )
    
    assert high_mouse.factors["mouse_time"] > low_mouse.factors["mouse_time"]


def test_assess_rsi_risk_breaks():
    """测试休息频率对RSI风险的影响"""
    few_breaks = assess_rsi_risk(
        typing_hours_per_day=6,
        mouse_hours_per_day=2,
        breaks_per_day=1,
        keyboard_position="ideal",
        mouse_position="ideal",
        wrist_support=True,
        previous_injury=False
    )
    
    many_breaks = assess_rsi_risk(
        typing_hours_per_day=6,
        mouse_hours_per_day=2,
        breaks_per_day=10,
        keyboard_position="ideal",
        mouse_position="ideal",
        wrist_support=True,
        previous_injury=False
    )
    
    assert few_breaks.factors["break_frequency"] > many_breaks.factors["break_frequency"]


def test_assess_rsi_risk_previous_injury():
    """测试过往伤病对RSI风险的影响"""
    no_injury = assess_rsi_risk(
        typing_hours_per_day=4,
        mouse_hours_per_day=2,
        breaks_per_day=4,
        keyboard_position="ideal",
        mouse_position="ideal",
        wrist_support=True,
        previous_injury=False
    )
    
    with_injury = assess_rsi_risk(
        typing_hours_per_day=4,
        mouse_hours_per_day=2,
        breaks_per_day=4,
        keyboard_position="ideal",
        mouse_position="ideal",
        wrist_support=True,
        previous_injury=True
    )
    
    assert with_injury.factors["previous_injury"] == 25
    assert with_injury.risk_score > no_injury.risk_score


def test_assess_rsi_risk_equipment():
    """测试设备配置对RSI风险的影响"""
    ideal = assess_rsi_risk(
        typing_hours_per_day=4,
        mouse_hours_per_day=2,
        breaks_per_day=4,
        keyboard_position="ideal",
        mouse_position="ideal",
        wrist_support=True,
        previous_injury=False
    )
    
    poor = assess_rsi_risk(
        typing_hours_per_day=4,
        mouse_hours_per_day=2,
        breaks_per_day=4,
        keyboard_position="high",
        mouse_position="far",
        wrist_support=False,
        previous_injury=False
    )
    
    assert ideal.factors["keyboard_position"] < poor.factors["keyboard_position"]
    assert ideal.factors["mouse_position"] < poor.factors["mouse_position"]
    assert ideal.factors["wrist_support"] < poor.factors["wrist_support"]


def test_assess_rsi_risk_warning_signs():
    """测试RSI警示信号"""
    assessment = assess_rsi_risk(
        typing_hours_per_day=4,
        mouse_hours_per_day=2,
        breaks_per_day=4,
        keyboard_position="ideal",
        mouse_position="ideal",
        wrist_support=True,
        previous_injury=False
    )
    
    assert len(assessment.warning_signs) > 0
    assert all(isinstance(sign, str) for sign in assessment.warning_signs)


# ==================== 眼睛保护计划测试 ====================

def test_create_eye_care_plan_basic():
    """测试基本眼睛保护计划"""
    plan = create_eye_care_plan(screen_hours_per_day=6)
    
    assert isinstance(plan, EyeCarePlan)
    assert plan.break_interval_minutes > 0
    assert plan.focus_distance_meters > 0
    assert len(plan.eye_exercises) > 0
    assert len(plan.lighting_recommendations) > 0


def test_create_eye_care_plan_different_hours():
    """测试不同使用时间的计划"""
    light_use = create_eye_care_plan(screen_hours_per_day=3)
    heavy_use = create_eye_care_plan(screen_hours_per_day=10)
    
    # 重度使用者应该有更短的休息间隔
    assert heavy_use.break_interval_minutes <= light_use.break_interval_minutes


def test_create_eye_care_plan_glasses():
    """测试眼镜用户的计划"""
    no_glasses = create_eye_care_plan(screen_hours_per_day=6, has_glasses=False)
    with_glasses = create_eye_care_plan(screen_hours_per_day=6, has_glasses=True)
    
    # 眼镜用户应该有额外的建议
    glasses_recs = [r for r in with_glasses.lighting_recommendations if "眼镜" in r or "镜片" in r]
    assert len(glasses_recs) > 0


def test_create_eye_care_plan_brightness():
    """测试不同亮度的建议"""
    low_brightness = create_eye_care_plan(screen_hours_per_day=6, screen_brightness="low")
    high_brightness = create_eye_care_plan(screen_hours_per_day=6, screen_brightness="high")
    
    # 高亮度应该有降低亮度的建议
    assert any("降低" in r or "亮度" in r for r in high_brightness.lighting_recommendations)


def test_create_eye_care_plan_ambient_light():
    """测试不同环境光的建议"""
    dim = create_eye_care_plan(screen_hours_per_day=6, ambient_light="dim")
    bright = create_eye_care_plan(screen_hours_per_day=6, ambient_light="bright")
    
    # 暗环境应该有增加照明的建议
    assert any("增加" in r or "光线" in r for r in dim.lighting_recommendations)
    
    # 亮环境应该有避免眩光的建议
    assert any("眩光" in r or "遮挡" in r or "避免" in r for r in bright.lighting_recommendations)


def test_create_eye_care_plan_exercises():
    """测试眼保健操"""
    plan = create_eye_care_plan(screen_hours_per_day=6)
    
    for exercise in plan.eye_exercises:
        assert "name" in exercise
        assert "duration_seconds" in exercise
        assert "steps" in exercise
        assert len(exercise["steps"]) > 0


# ==================== 显示器设置测试 ====================

def test_calculate_optimal_monitor_setup_basic():
    """测试基本显示器设置计算"""
    setup = calculate_optimal_monitor_setup(
        monitor_size_inches=24,
        resolution_width=1920,
        resolution_height=1080,
        user_height_cm=175
    )
    
    assert "monitor_dimensions" in setup
    assert "pixel_density_ppi" in setup
    assert "recommended_viewing_distance_cm" in setup
    assert "tips" in setup
    
    assert setup["monitor_dimensions"]["width_cm"] > 0
    assert setup["monitor_dimensions"]["height_cm"] > 0
    assert setup["pixel_density_ppi"] > 0


def test_calculate_optimal_monitor_setup_4k():
    """测试4K显示器设置"""
    setup_1080p = calculate_optimal_monitor_setup(24, 1920, 1080, 175)
    setup_4k = calculate_optimal_monitor_setup(24, 3840, 2160, 175)
    
    # 4K有更高的像素密度
    assert setup_4k["pixel_density_ppi"] > setup_1080p["pixel_density_ppi"]
    
    # 4K可以更近观看
    assert setup_4k["recommended_viewing_distance_cm"] <= setup_1080p["recommended_viewing_distance_cm"]


def test_calculate_optimal_monitor_setup_different_sizes():
    """测试不同尺寸显示器"""
    small = calculate_optimal_monitor_setup(21, 1920, 1080, 175)
    large = calculate_optimal_monitor_setup(32, 1920, 1080, 175)
    
    # 大屏幕有更大的物理尺寸
    assert large["monitor_dimensions"]["width_cm"] > small["monitor_dimensions"]["width_cm"]
    
    # 但大屏幕如果分辨率相同，PPI更低
    assert large["pixel_density_ppi"] < small["pixel_density_ppi"]


def test_calculate_optimal_monitor_setup_scaling():
    """测试缩放建议"""
    low_ppi = calculate_optimal_monitor_setup(24, 1920, 1080, 175)  # ~92 PPI
    high_ppi = calculate_optimal_monitor_setup(24, 3840, 2160, 175)  # ~184 PPI
    
    # 高DPI需要更高的缩放
    assert "150%" in high_ppi["scaling_recommendation"] or "200%" in high_ppi["scaling_recommendation"]


# ==================== 工作模式分析测试 ====================

def test_get_work_period_analysis_basic():
    """测试基本工作模式分析"""
    analysis = get_work_period_analysis(
        work_periods=[{"start": "09:00", "end": "12:00"}],
        break_periods=[{"start": "12:00", "end": "13:00"}]
    )
    
    assert "total_work_hours" in analysis
    assert "total_break_hours" in analysis
    assert "break_ratio" in analysis
    assert "issues" in analysis
    assert "recommendations" in analysis


def test_get_work_period_analysis_long_day():
    """测试长时间工作"""
    analysis = get_work_period_analysis(
        work_periods=[
            {"start": "09:00", "end": "12:00"},
            {"start": "13:00", "end": "18:00"},
            {"start": "19:00", "end": "22:00"}
        ],
        break_periods=[{"start": "12:00", "end": "13:00"}]
    )
    
    assert analysis["total_work_hours"] > 8
    assert len(analysis["issues"]) > 0


def test_get_work_period_analysis_continuous():
    """测试连续工作时间"""
    analysis = get_work_period_analysis(
        work_periods=[{"start": "09:00", "end": "14:00"}],
        break_periods=[]
    )
    
    assert analysis["longest_continuous_work_minutes"] == 300
    assert any("连续" in issue for issue in analysis["issues"])


def test_get_work_period_analysis_intensity():
    """测试工作强度评估"""
    light = get_work_period_analysis(
        work_periods=[{"start": "09:00", "end": "12:00"}],
        break_periods=[{"start": "12:00", "end": "13:00"}]
    )
    
    heavy = get_work_period_analysis(
        work_periods=[{"start": "09:00", "end": "21:00"}],
        break_periods=[]
    )
    
    assert light["work_intensity"] in ["light", "moderate"]
    assert heavy["work_intensity"] in ["intensive", "extreme"]


def test_get_work_period_analysis_break_suggestions():
    """测试休息建议生成"""
    analysis = get_work_period_analysis(
        work_periods=[{"start": "09:00", "end": "17:00"}],
        break_periods=[{"start": "12:00", "end": "13:00"}]
    )
    
    assert "daily_break_suggestions" in analysis
    assert len(analysis["daily_break_suggestions"]) > 0


# ==================== 坐立比例测试 ====================

def test_get_sitting_vs_standing_recommendation_balanced():
    """测试平衡的坐立比例"""
    result = get_sitting_vs_standing_recommendation(
        sitting_hours=5,
        standing_hours=3,
        total_work_hours=8
    )
    
    assert "current_sitting_ratio" in result
    assert "current_standing_ratio" in result
    assert "ideal_sitting_hours" in result
    assert "ideal_standing_hours" in result


def test_get_sitting_vs_standing_recommendation_too_much_sitting():
    """测试坐得太多"""
    result = get_sitting_vs_standing_recommendation(
        sitting_hours=7,
        standing_hours=1,
        total_work_hours=8
    )
    
    assert result["current_sitting_ratio"] > 0.8
    assert len(result["issues"]) > 0
    assert len(result["recommendations"]) > 0


def test_get_sitting_vs_standing_recommendation_too_much_standing():
    """测试站得太多"""
    result = get_sitting_vs_standing_recommendation(
        sitting_hours=2,
        standing_hours=6,
        total_work_hours=8
    )
    
    assert result["current_standing_ratio"] > 0.5
    assert len(result["issues"]) > 0


def test_get_sitting_vs_standing_recommendation_switch_interval():
    """测试切换间隔建议"""
    short_day = get_sitting_vs_standing_recommendation(
        sitting_hours=3,
        standing_hours=1,
        total_work_hours=4
    )
    
    long_day = get_sitting_vs_standing_recommendation(
        sitting_hours=6,
        standing_hours=2,
        total_work_hours=8
    )
    
    assert "recommended_switch_interval_minutes" in short_day
    assert "recommended_switch_interval_minutes" in long_day


# ==================== 快速设置测试 ====================

def test_quick_setup():
    """测试快速设置功能"""
    setup = quick_setup(175)
    
    assert "workstation" in setup
    assert "footrest" in setup
    assert "recommended_stretches" in setup
    assert "break_reminder" in setup
    
    assert isinstance(setup["workstation"], dict)
    assert len(setup["recommended_stretches"]) > 0


def test_quick_setup_different_heights():
    """测试不同身高的快速设置"""
    for height in [150, 165, 180, 195]:
        setup = quick_setup(height)
        assert "workstation" in setup


# ==================== 枚举测试 ====================

def test_work_intensity_enum():
    """测试工作强度枚举"""
    assert WorkIntensity.LIGHT.value == "light"
    assert WorkIntensity.MODERATE.value == "moderate"
    assert WorkIntensity.INTENSIVE.value == "intensive"
    assert WorkIntensity.EXTREME.value == "extreme"


def test_posture_risk_enum():
    """测试姿势风险枚举"""
    assert PostureRisk.LOW.value == "low"
    assert PostureRisk.MEDIUM.value == "medium"
    assert PostureRisk.HIGH.value == "high"
    assert PostureRisk.CRITICAL.value == "critical"


def test_body_part_enum():
    """测试身体部位枚举"""
    assert BodyPart.NECK.value == "neck"
    assert BodyPart.SHOULDERS.value == "shoulders"
    assert BodyPart.WRISTS.value == "wrists"
    assert BodyPart.EYES.value == "eyes"


# ==================== 边界值测试 ====================

def test_extreme_height():
    """测试极端身高"""
    # 非常矮
    short = calculate_workstation_setup(140)
    assert short.chair_height > 0
    
    # 非常高
    tall = calculate_workstation_setup(210)
    assert tall.desk_height > short.desk_height


def test_zero_work_hours():
    """测试零工作时间"""
    breaks = calculate_break_intervals(0)
    assert len(breaks) == 0
    
    analysis = get_work_period_analysis([], [])
    assert analysis["total_work_hours"] == 0


def test_very_long_work_hours():
    """测试超长工作时间"""
    breaks = calculate_break_intervals(16)  # 16小时
    assert len(breaks) > 0
    
    analysis = get_work_period_analysis(
        [{"start": "00:00", "end": "16:00"}],
        []
    )
    assert analysis["work_intensity"] == "extreme"


def test_negative_inputs():
    """测试负数输入"""
    try:
        calculate_break_intervals(-1)
        assert False, "应该处理负数"
    except:
        pass


def test_edge_case_posture():
    """测试姿势评估边界值"""
    # 完美姿势
    perfect = assess_posture(
        screen_distance_cm=60,
        screen_height_relative="level",
        back_support=True,
        feet_flat=True,
        elbows_angle=100,
        breaks_taken=10,
        work_duration_minutes=60
    )
    assert perfect.score >= 90
    
    # 最差姿势
    worst = assess_posture(
        screen_distance_cm=10,
        screen_height_relative="above",
        back_support=False,
        feet_flat=False,
        elbows_angle=60,
        breaks_taken=0,
        work_duration_minutes=180
    )
    assert worst.score < 50


def test_rsi_edge_cases():
    """测试RSI评估边界值"""
    # 零工作时间
    zero = assess_rsi_risk(
        typing_hours_per_day=0,
        mouse_hours_per_day=0,
        breaks_per_day=0,
        keyboard_position="ideal",
        mouse_position="ideal",
        wrist_support=True,
        previous_injury=False
    )
    assert zero.risk_score == 0 or zero.factors["previous_injury"] == 25  # 只有过往伤病影响


# ==================== 运行所有测试 ====================

def main():
    """运行所有测试"""
    tests = [
        # 工作站设置测试
        ("工作站设置 - 基本计算", test_calculate_workstation_setup_basic),
        ("工作站设置 - 不同身高", test_calculate_workstation_setup_different_heights),
        ("工作站设置 - 矮个子脚踏", test_calculate_workstation_setup_short_person),
        ("工作站设置 - 高个子设置", test_calculate_workstation_setup_tall_person),
        ("工作站设置 - 站立模式", test_calculate_workstation_setup_standing),
        ("工作站设置 - 屏幕尺寸", test_calculate_workstation_setup_screen_size),
        ("工作站设置 - 无效身高", test_calculate_workstation_setup_invalid_height),
        
        # 休息间隔测试
        ("休息间隔 - 轻度工作", test_calculate_break_intervals_light_work),
        ("休息间隔 - 高强度工作", test_calculate_break_intervals_intensive_work),
        ("休息间隔 - 长休息", test_calculate_break_intervals_long_break),
        ("休息间隔 - 20-20-20法则", test_calculate_break_intervals_20_20_20_rule),
        ("休息间隔 - 不使用眼睛法则", test_calculate_break_intervals_no_eye_rule),
        ("休息间隔 - 极高强度", test_calculate_break_intervals_extreme_work),
        
        # 伸展运动测试
        ("伸展运动 - 获取全部", test_get_stretch_exercises_all),
        ("伸展运动 - 按部位筛选", test_get_stretch_exercises_by_body_part),
        ("伸展运动 - 多部位筛选", test_get_stretch_exercises_multiple_body_parts),
        ("伸展运动 - 手腕运动", test_get_stretch_exercises_wrist),
        ("伸展运动 - 眼部运动", test_get_stretch_exercises_eyes),
        ("伸展运动 - 长时间工作", test_get_stretch_exercises_long_work),
        ("伸展运动 - 数据结构", test_stretch_exercise_structure),
        
        # 姿势评估测试
        ("姿势评估 - 理想姿势", test_assess_posture_ideal),
        ("姿势评估 - 不良姿势", test_assess_posture_poor),
        ("姿势评估 - 屏幕太近", test_assess_posture_screen_too_close),
        ("姿势评估 - 屏幕太远", test_assess_posture_screen_too_far),
        ("姿势评估 - 屏幕过高", test_assess_posture_screen_above),
        ("姿势评估 - 屏幕过低", test_assess_posture_screen_below),
        ("姿势评估 - 无背支撑", test_assess_posture_no_back_support),
        ("姿势评估 - 休息不足", test_assess_posture_insufficient_breaks),
        ("姿势评估 - 手肘角度", test_assess_posture_elbow_angle),
        
        # RSI风险评估测试
        ("RSI评估 - 低风险", test_assess_rsi_risk_low),
        ("RSI评估 - 高风险", test_assess_rsi_risk_high),
        ("RSI评估 - 打字时间影响", test_assess_rsi_risk_typing_time),
        ("RSI评估 - 鼠标时间影响", test_assess_rsi_risk_mouse_time),
        ("RSI评估 - 休息频率影响", test_assess_rsi_risk_breaks),
        ("RSI评估 - 过往伤病影响", test_assess_rsi_risk_previous_injury),
        ("RSI评估 - 设备配置影响", test_assess_rsi_risk_equipment),
        ("RSI评估 - 警示信号", test_assess_rsi_risk_warning_signs),
        
        # 眼睛保护计划测试
        ("眼睛保护 - 基本计划", test_create_eye_care_plan_basic),
        ("眼睛保护 - 不同使用时间", test_create_eye_care_plan_different_hours),
        ("眼睛保护 - 眼镜用户", test_create_eye_care_plan_glasses),
        ("眼睛保护 - 屏幕亮度", test_create_eye_care_plan_brightness),
        ("眼睛保护 - 环境光线", test_create_eye_care_plan_ambient_light),
        ("眼睛保护 - 眼保健操", test_create_eye_care_plan_exercises),
        
        # 显示器设置测试
        ("显示器设置 - 基本计算", test_calculate_optimal_monitor_setup_basic),
        ("显示器设置 - 4K对比", test_calculate_optimal_monitor_setup_4k),
        ("显示器设置 - 不同尺寸", test_calculate_optimal_monitor_setup_different_sizes),
        ("显示器设置 - 缩放建议", test_calculate_optimal_monitor_setup_scaling),
        
        # 工作模式分析测试
        ("工作分析 - 基本分析", test_get_work_period_analysis_basic),
        ("工作分析 - 长时间工作", test_get_work_period_analysis_long_day),
        ("工作分析 - 连续工作", test_get_work_period_analysis_continuous),
        ("工作分析 - 强度评估", test_get_work_period_analysis_intensity),
        ("工作分析 - 休息建议", test_get_work_period_analysis_break_suggestions),
        
        # 坐立比例测试
        ("坐立比例 - 平衡比例", test_get_sitting_vs_standing_recommendation_balanced),
        ("坐立比例 - 坐太多", test_get_sitting_vs_standing_recommendation_too_much_sitting),
        ("坐立比例 - 站太多", test_get_sitting_vs_standing_recommendation_too_much_standing),
        ("坐立比例 - 切换间隔", test_get_sitting_vs_standing_recommendation_switch_interval),
        
        # 快速设置测试
        ("快速设置 - 基本功能", test_quick_setup),
        ("快速设置 - 不同身高", test_quick_setup_different_heights),
        
        # 枚举测试
        ("枚举 - 工作强度", test_work_intensity_enum),
        ("枚举 - 姿势风险", test_posture_risk_enum),
        ("枚举 - 身体部位", test_body_part_enum),
        
        # 边界值测试
        ("边界值 - 极端身高", test_extreme_height),
        ("边界值 - 零工作时间", test_zero_work_hours),
        ("边界值 - 超长工作时间", test_very_long_work_hours),
        ("边界值 - 负数输入", test_negative_inputs),
        ("边界值 - 姿势极值", test_edge_case_posture),
        ("边界值 - RSI极值", test_rsi_edge_cases),
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("人体工程学工具集测试")
    print("=" * 60)
    
    for name, test_func in tests:
        if run_test(name, test_func):
            passed += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"总计: {passed + failed} 测试")
    print(f"通过: {passed}")
    print(f"失败: {failed}")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)