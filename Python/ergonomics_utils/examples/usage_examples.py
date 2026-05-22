"""
人体工程学工具集使用示例

展示所有主要功能的实际使用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ergonomics_utils.mod import (
    BodyPart, WorkIntensity, PostureRisk,
    calculate_workstation_setup, calculate_break_intervals, get_stretch_exercises,
    assess_posture, assess_rsi_risk, create_eye_care_plan,
    calculate_optimal_monitor_setup, get_work_period_analysis,
    get_sitting_vs_standing_recommendation, quick_setup
)


def example_workstation_setup():
    """示例：工作站设置计算"""
    print("=" * 60)
    print("示例 1: 工作站设置计算")
    print("=" * 60)
    
    # 根据身高计算理想工作站设置
    height = 175  # cm
    setup = calculate_workstation_setup(height)
    
    print(f"\n身高 {height}cm 的理想工作站设置：")
    print(f"  屏幕顶部高度: {setup.screen_height} cm")
    print(f"  眼睛到屏幕距离: {setup.screen_distance} cm")
    print(f"  椅子高度: {setup.chair_height} cm")
    print(f"  桌子高度: {setup.desk_height} cm")
    print(f"  键盘高度: {setup.keyboard_height} cm")
    print(f"  显示器倾斜角度: {setup.monitor_tilt}°")
    print(f"  扶手高度: {setup.armrest_height} cm")
    print(f"  是否需要脚踏: {'是' if setup.footrest_needed else '否'}")
    if setup.footrest_needed:
        print(f"  脚踏高度: {setup.footrest_height} cm")
    
    print("\n站立工作站设置：")
    standing_setup = calculate_workstation_setup(height, seated=False)
    print(f"  桌子高度: {standing_setup.desk_height} cm")
    print(f"  屏幕顶部高度: {standing_setup.screen_height} cm")


def example_break_intervals():
    """示例：休息间隔计算"""
    print("\n" + "=" * 60)
    print("示例 2: 休息间隔计算")
    print("=" * 60)
    
    # 不同工作强度的休息建议
    work_hours = 4
    
    print(f"\n{work_hours}小时工作的休息建议：")
    
    for intensity in [WorkIntensity.LIGHT, WorkIntensity.MODERATE, 
                       WorkIntensity.INTENSIVE, WorkIntensity.EXTREME]:
        breaks = calculate_break_intervals(work_hours, intensity, use_20_20_20_rule=False)
        work_breaks = [b for b in breaks if b.break_type != "eye_break"]
        
        print(f"\n{intensity.value}强度工作：")
        print(f"  休息次数: {len(work_breaks)}")
        if len(work_breaks) > 0:
            print(f"  首次休息: 工作{work_breaks[0].reason.split(' ')[2]}分钟后")
            print(f"  休息时长: {work_breaks[0].duration_minutes}分钟")
    
    # 20-20-20法则
    print("\n20-20-20法则（眼睛保护）：")
    breaks = calculate_break_intervals(1, use_20_20_20_rule=True)
    eye_breaks = [b for b in breaks if b.break_type == "eye_break"]
    print(f"  每20分钟远眺20秒，看向6米外")
    print(f"  1小时内需要 {len(eye_breaks)} 次眼睛休息")


def example_stretch_exercises():
    """示例：伸展运动建议"""
    print("\n" + "=" * 60)
    print("示例 3: 伸展运动建议")
    print("=" * 60)
    
    # 获取所有伸展运动
    all_exercises = get_stretch_exercises()
    print(f"\n共有 {len(all_exercises)} 种伸展运动")
    
    # 针特定部位的伸展
    print("\n针对颈部的伸展运动：")
    neck_exercises = get_stretch_exercises([BodyPart.NECK])
    for e in neck_exercises[:2]:
        print(f"\n  【{e.name}】")
        print(f"    时长: {e.duration_seconds}秒 × {e.repetitions}次")
        print(f"    步骤:")
        for i, step in enumerate(e.instructions[:3], 1):
            print(f"      {i}. {step}")
        print(f"    好处: {', '.join(e.benefits[:2])}")
    
    # 针对手腕的伸展（适合程序员）
    print("\n针对手腕的伸展运动（预防腕管综合症）：")
    wrist_exercises = get_stretch_exercises([BodyPart.WRISTS])
    for e in wrist_exercises:
        print(f"  【{e.name}】 - {e.duration_seconds}秒 × {e.repetitions}次")
    
    # 针对眼睛的伸展
    print("\n眼部放松运动：")
    eye_exercises = get_stretch_exercises([BodyPart.EYES])
    for e in eye_exercises:
        print(f"  【{e.name}】")


def example_posture_assessment():
    """示例：姿势评估"""
    print("\n" + "=" * 60)
    print("示例 4: 姿势风险评估")
    print("=" * 60)
    
    # 理想姿势
    print("\n场景A：理想工作姿势")
    good_posture = assess_posture(
        screen_distance_cm=60,
        screen_height_relative="level",
        back_support=True,
        feet_flat=True,
        elbows_angle=95,
        breaks_taken=3,
        work_duration_minutes=120
    )
    print(f"  风险等级: {good_posture.risk_level.value}")
    print(f"  评分: {good_posture.score}/100")
    if good_posture.issues:
        print(f"  问题: {', '.join(good_posture.issues)}")
    else:
        print(f"  问题: 无明显问题 ✓")
    
    # 不良姿势
    print("\n场景B：常见不良姿势")
    bad_posture = assess_posture(
        screen_distance_cm=35,  # 屏幕太近
        screen_height_relative="below",  # 屏幕太低
        back_support=False,  # 无背支撑
        feet_flat=False,  # 脚不平放
        elbows_angle=85,  # 手肘角度小
        breaks_taken=1,  # 休息太少
        work_duration_minutes=180  # 工作时间长
    )
    print(f"  风险等级: {bad_posture.risk_level.value}")
    print(f"  评分: {bad_posture.score}/100")
    print(f"  受影响部位: {', '.join([bp.value for bp in bad_posture.affected_areas])}")
    print(f"  问题:")
    for issue in bad_posture.issues[:5]:
        print(f"    - {issue}")
    print(f"  建议改进:")
    for rec in bad_posture.recommendations[:3]:
        print(f"    - {rec}")


def example_rsi_assessment():
    """示例：RSI风险评估"""
    print("\n" + "=" * 60)
    print("示例 5: RSI（重复性劳损）风险评估")
    print("=" * 60)
    
    # 程序员典型情况
    print("\n程序员A（低风险）：")
    programmer_low = assess_rsi_risk(
        typing_hours_per_day=4,
        mouse_hours_per_day=2,
        breaks_per_day=6,
        keyboard_position="ideal",
        mouse_position="ideal",
        wrist_support=True,
        previous_injury=False
    )
    print(f"  总风险分数: {programmer_low.risk_score}")
    print(f"  风险等级: {programmer_low.risk_level}")
    print(f"  各因素分数:")
    for factor, score in programmer_low.factors.items():
        if score > 0:
            print(f"    - {factor}: {score}")
    
    # 高风险情况
    print("\n程序员B（高风险）：")
    programmer_high = assess_rsi_risk(
        typing_hours_per_day=8,
        mouse_hours_per_day=5,
        breaks_per_day=2,
        keyboard_position="high",
        mouse_position="far",
        wrist_support=False,
        previous_injury=True
    )
    print(f"  总风险分数: {programmer_high.risk_score}")
    print(f"  风险等级: {programmer_high.risk_level}")
    print(f"  改进建议:")
    for rec in programmer_high.recommendations[:5]:
        print(f"    - {rec}")
    
    print("\n⚠️ 警示信号（如有以下症状请就医）：")
    for sign in programmer_high.warning_signs[:3]:
        print(f"    - {sign}")


def example_eye_care():
    """示例：眼睛保护计划"""
    print("\n" + "=" * 60)
    print("示例 6: 眼睛保护计划")
    print("=" * 60)
    
    # 轻度使用
    print("\n轻度屏幕使用者（4小时/天）：")
    light_plan = create_eye_care_plan(screen_hours_per_day=4)
    print(f"  建议休息间隔: 每{light_plan.break_interval_minutes}分钟")
    print(f"  远眺距离: {light_plan.focus_distance_meters}米")
    
    # 重度使用
    print("\n重度屏幕使用者（10小时/天）：")
    heavy_plan = create_eye_care_plan(
        screen_hours_per_day=10,
        has_glasses=True,
        screen_brightness="high",
        ambient_light="dim"
    )
    print(f"  建议休息间隔: 每{heavy_plan.break_interval_minutes}分钟")
    print(f"  照明建议:")
    for rec in heavy_plan.lighting_recommendations[:4]:
        print(f"    - {rec}")
    
    print("\n眼保健操推荐：")
    for exercise in heavy_plan.eye_exercises[:2]:
        print(f"\n  【{exercise['name']}】({exercise['duration_seconds']}秒)")
        for step in exercise['steps']:
            print(f"    - {step}")


def example_monitor_setup():
    """示例：显示器设置"""
    print("\n" + "=" * 60)
    print("示例 7: 显示器设置计算")
    print("=" * 60)
    
    # 24寸 1080p
    print("\n24寸 1080p显示器设置：")
    setup_1080p = calculate_optimal_monitor_setup(
        monitor_size_inches=24,
        resolution_width=1920,
        resolution_height=1080,
        user_height_cm=175
    )
    print(f"  显示器尺寸: {setup_1080p['monitor_dimensions']['width_cm']}×{setup_1080p['monitor_dimensions']['height_cm']} cm")
    print(f"  像素密度: {setup_1080p['pixel_density_ppi']} PPI")
    print(f"  推荐观看距离: {setup_1080p['recommended_viewing_distance_cm']} cm")
    print(f"  缩放建议: {setup_1080p['scaling_recommendation']}")
    print(f"  字体大小建议: {setup_1080p['font_size_recommendation']}")
    
    # 27寸 4K
    print("\n27寸 4K显示器设置：")
    setup_4k = calculate_optimal_monitor_setup(
        monitor_size_inches=27,
        resolution_width=3840,
        resolution_height=2160,
        user_height_cm=175
    )
    print(f"  显示器尺寸: {setup_4k['monitor_dimensions']['width_cm']}×{setup_4k['monitor_dimensions']['height_cm']} cm")
    print(f"  像素密度: {setup_4k['pixel_density_ppi']} PPI")
    print(f"  推荐观看距离: {setup_4k['recommended_viewing_distance_cm']} cm")
    print(f"  缩放建议: {setup_4k['scaling_recommendation']}")
    
    print("\n显示器使用提示：")
    for tip in setup_1080p['tips']:
        print(f"  - {tip}")


def example_work_analysis():
    """示例：工作模式分析"""
    print("\n" + "=" * 60)
    print("示例 8: 工作模式分析")
    print("=" * 60)
    
    # 典型工作日
    print("\n典型8小时工作日分析：")
    analysis = get_work_period_analysis(
        work_periods=[
            {"start": "09:00", "end": "12:00"},
            {"start": "13:00", "end": "17:00"},
            {"start": "18:00", "end": "20:00"}
        ],
        break_periods=[
            {"start": "12:00", "end": "13:00"},
            {"start": "17:00", "end": "18:00"}
        ]
    )
    
    print(f"  总工作时间: {analysis['total_work_hours']}小时")
    print(f"  总休息时间: {analysis['total_break_hours']}小时")
    print(f"  休息比例: {analysis['break_ratio'] * 100:.1f}%")
    print(f"  最长连续工作: {analysis['longest_continuous_work_minutes']}分钟")
    print(f"  工作强度: {analysis['work_intensity']}")
    
    if analysis['issues']:
        print(f"  ⚠️ 发现问题:")
        for issue in analysis['issues']:
            print(f"    - {issue}")
    
    print(f"\n  休息建议:")
    suggestions = analysis['daily_break_suggestions']
    for s in suggestions[:3]:
        print(f"    - {s.break_type}: {s.activity}")


def example_sitting_standing():
    """示例：坐立比例建议"""
    print("\n" + "=" * 60)
    print("示例 9: 坐立比例建议")
    print("=" * 60)
    
    # 使用升降桌的情况
    print("\n使用升降桌的8小时工作日：")
    result = get_sitting_vs_standing_recommendation(
        sitting_hours=5,
        standing_hours=3,
        total_work_hours=8
    )
    
    print(f"  当前坐姿比例: {result['current_sitting_ratio'] * 100:.0f}%")
    print(f"  当前站姿比例: {result['current_standing_ratio'] * 100:.0f}%")
    print(f"  理想坐姿时间: {result['ideal_sitting_hours']}小时")
    print(f"  理想站姿时间: {result['ideal_standing_hours']}小时")
    print(f"  建议切换间隔: {result['recommended_switch_interval_minutes']}分钟")
    
    if result['issues']:
        print(f"  ⚠️ 问题:")
        for issue in result['issues']:
            print(f"    - {issue}")
    
    print(f"\n  使用提示:")
    for tip in result['tips']:
        print(f"    - {tip}")


def example_quick_setup():
    """示例：快速设置"""
    print("\n" + "=" * 60)
    print("示例 10: 快速工作站设置")
    print("=" * 60)
    
    # 快速获取所有建议
    height = 175
    setup = quick_setup(height)
    
    print(f"\n身高 {height}cm 的快速设置指南：")
    print("\n工作站设置：")
    for key, value in setup['workstation'].items():
        print(f"  - {value}")
    
    print(f"\n脚踏需求: {setup['footrest']}")
    
    print(f"\n推荐伸展运动（前5项）：")
    for stretch in setup['recommended_stretches']:
        print(f"  - {stretch}")
    
    print(f"\n休息提醒: {setup['break_reminder']}")


def example_complete_scenario():
    """完整场景：程序员的一天"""
    print("\n" + "=" * 60)
    print("示例 11: 程序员完整健康工作指南")
    print("=" * 60)
    
    height = 178  # cm
    work_hours = 8
    
    print(f"\n程序员（身高{height}cm，工作{work_hours}小时）的完整健康指南：")
    
    # 1. 工作站设置
    print("\n【1. 工作站设置】")
    workstation = calculate_workstation_setup(height)
    print(f"  椅子高度: {workstation.chair_height} cm")
    print(f"  桌子高度: {workstation.desk_height} cm")
    print(f"  屏幕距离: {workstation.screen_distance} cm")
    
    # 2. 休息计划
    print("\n【2. 休息计划】")
    breaks = calculate_break_intervals(work_hours, WorkIntensity.INTENSIVE)
    work_breaks = [b for b in breaks if b.break_type == "short_break" or b.break_type == "long_break"]
    print(f"  建议休息次数: {len(work_breaks)}")
    print(f"  休息类型:")
    for b in work_breaks[:4]:
        print(f"    - {b.break_type}: {b.duration_minutes}分钟 ({b.activity})")
    
    # 3. 伸展运动
    print("\n【3. 重点伸展运动】")
    stretches = get_stretch_exercises([BodyPart.NECK, BodyPart.WRISTS, BodyPart.EYES])
    print(f"  针对程序员重点部位:")
    for s in stretches[:4]:
        print(f"    - {s.name}: {s.duration_seconds}秒 × {s.repetitions}次")
    
    # 4. 眼睛保护
    print("\n【4. 眼睛保护】")
    eye_plan = create_eye_care_plan(work_hours)
    print(f"  休息间隔: 每{eye_plan.break_interval_minutes}分钟")
    print(f"  远眺距离: {eye_plan.focus_distance_meters}米")
    
    # 5. RSI预防
    print("\n【5. RSI预防检查】")
    rsi = assess_rsi_risk(
        typing_hours_per_day=6,
        mouse_hours_per_day=3,
        breaks_per_day=6,
        keyboard_position="ideal",
        mouse_position="ideal",
        wrist_support=True,
        previous_injury=False
    )
    print(f"  风险分数: {rsi.risk_score}")
    print(f"  风险等级: {rsi.risk_level}")
    
    print("\n" + "=" * 60)
    print("✅ 保持健康的工作习惯！")
    print("=" * 60)


def main():
    """运行所有示例"""
    example_workstation_setup()
    example_break_intervals()
    example_stretch_exercises()
    example_posture_assessment()
    example_rsi_assessment()
    example_eye_care()
    example_monitor_setup()
    example_work_analysis()
    example_sitting_standing()
    example_quick_setup()
    example_complete_scenario()


if __name__ == "__main__":
    main()