"""
Breathing Exercise Utils - 使用示例

展示呼吸练习工具的各种使用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from breathing_exercise_utils.mod import (
    BreathingTechnique,
    BreathPhase,
    BreathingSession,
    
    get_pattern,
    list_techniques,
    get_technique_by_name,
    calculate_total_duration,
    calculate_breaths_per_minute,
    generate_session_steps,
    create_custom_pattern,
    format_timer_display,
    get_recommended_technique,
    get_techniques_by_difficulty,
    get_techniques_by_benefit,
    calculate_oxygen_efficiency,
    compare_techniques,
    generate_breathing_text_guide,
    calculate_hrv_estimate,
    
    quick_relax,
    quick_sleep,
    quick_energy,
    print_pattern_info,
)


def example_1_basic_usage():
    """示例 1：基本使用"""
    print("\n" + "=" * 50)
    print("示例 1：基本使用 - 获取呼吸模式")
    print("=" * 50)
    
    # 获取 4-7-8 放松呼吸模式
    pattern = get_pattern(BreathingTechnique.RELAXATION_478)
    
    print(f"\n模式名称: {pattern.name}")
    print(f"难度: {pattern.difficulty}")
    print(f"单循环时长: {pattern.total_duration} 秒")
    print(f"建议循环次数: {pattern.cycles} 次")
    
    print("\n步骤详情:")
    for i, step in enumerate(pattern.steps, 1):
        print(f"  {i}. {step.instruction} ({step.duration}秒) - {step.description}")
    
    print("\n益处:")
    for benefit in pattern.benefits:
        print(f"  • {benefit}")
    
    if pattern.contraindications:
        print("\n注意事项:")
        for contra in pattern.contraindications:
            print(f"  ⚠️ {contra}")


def example_2_list_all_techniques():
    """示例 2：列出所有技巧"""
    print("\n" + "=" * 50)
    print("示例 2：所有可用的呼吸技巧")
    print("=" * 50)
    
    techniques = list_techniques()
    
    print(f"\n共有 {len(techniques)} 种呼吸技巧:\n")
    
    for tech in techniques:
        pattern = get_pattern(tech)
        bpm = calculate_breaths_per_minute(pattern)
        print(f"  {pattern.name}")
        print(f"    难度: {pattern.difficulty} | 呼吸频率: {bpm:.1f} 次/分")


def example_3_find_technique_by_name():
    """示例 3：通过名称查找技巧"""
    print("\n" + "=" * 50)
    print("示例 3：通过名称查找技巧")
    print("=" * 50)
    
    # 英文名称
    names_en = ["4-7-8", "box", "wim_hof", "ujjayi"]
    
    print("\n英文名称搜索:")
    for name in names_en:
        tech = get_technique_by_name(name)
        if tech:
            pattern = get_pattern(tech)
            print(f"  '{name}' → {pattern.name}")
    
    # 中文名称
    names_cn = ["放松", "箱式呼吸", "腹式呼吸", "睡眠", "镇静"]
    
    print("\n中文名称搜索:")
    for name in names_cn:
        tech = get_technique_by_name(name)
        if tech:
            pattern = get_pattern(tech)
            print(f"  '{name}' → {pattern.name}")


def example_4_calculate_timing():
    """示例 4：计算时间"""
    print("\n" + "=" * 50)
    print("示例 4：计算练习时间")
    print("=" * 50)
    
    pattern = get_pattern(BreathingTechnique.BOX_BREATHING)
    
    print(f"\n{pattern.name}:")
    print(f"  单循环时长: {pattern.total_duration} 秒")
    
    for cycles in [1, 4, 10]:
        total = calculate_total_duration(pattern, cycles)
        print(f"  {cycles} 循环: {format_timer_display(total)} ({total:.0f} 秒)")
    
    bpm = calculate_breaths_per_minute(pattern)
    print(f"\n  每分钟呼吸次数: {bpm:.1f} 次")


def example_5_custom_pattern():
    """示例 5：创建自定义模式"""
    print("\n" + "=" * 50)
    print("示例 5：创建自定义呼吸模式")
    print("=" * 50)
    
    # 简单自定义
    custom_simple = create_custom_pattern(
        name="我的简单呼吸",
        inhale=4.0,
        exhale=6.0,
        cycles=12,
        benefits=["放松", "减压"],
        description="简单的吸4呼6模式"
    )
    
    print(f"\n{custom_simple.name}:")
    print(f"  描述: {custom_simple.description}")
    print(f"  单循环: {custom_simple.total_duration} 秒")
    print(f"  建议: {custom_simple.cycles} 循环")
    
    for step in custom_simple.steps:
        print(f"  • {step.instruction}: {step.duration} 秒")
    
    # 复杂自定义
    custom_full = create_custom_pattern(
        name="完整呼吸序列",
        inhale=5.0,
        hold_in=3.0,
        exhale=8.0,
        hold_out=2.0,
        cycles=6
    )
    
    print(f"\n{custom_full.name}:")
    print(f"  时长: {custom_full.total_duration} 秒")
    print(f"  序列: 吸 {custom_full.steps[0].duration}秒 → 屏 {custom_full.steps[1].duration}秒 → 呼 {custom_full.steps[2].duration}秒 → 屏 {custom_full.steps[3].duration}秒")


def example_6_recommendation():
    """示例 6：根据目标推荐"""
    print("\n" + "=" * 50)
    print("示例 6：根据目标推荐技巧")
    print("=" * 50)
    
    goals = ["sleep", "relax", "energy", "focus", "anxiety", "stress"]
    
    print("\n目标推荐:")
    for goal in goals:
        tech = get_recommended_technique(goal)
        pattern = get_pattern(tech)
        total = calculate_total_duration(pattern, pattern.cycles)
        print(f"\n  目标 '{goal}':")
        print(f"    推荐: {pattern.name}")
        print(f"    时长: {format_timer_display(total)}")
    
    # 考虑时间限制
    print("\n\n考虑时间限制:")
    for time_limit in [30, 60, 120]:
        tech = get_recommended_technique("relax", time_available=time_limit)
        pattern = get_pattern(tech)
        print(f"  {time_limit}秒内放松: {pattern.name} (单循环 {pattern.total_duration}秒)")


def example_7_difficulty_filter():
    """示例 7：按难度筛选"""
    print("\n" + "=" * 50)
    print("示例 7：按难度筛选技巧")
    print("=" * 50)
    
    for diff in ["easy", "medium", "hard"]:
        techniques = get_techniques_by_difficulty(diff)
        print(f"\n{diff.upper()} 级技巧 ({len(techniques)} 种):")
        for tech in techniques:
            pattern = get_pattern(tech)
            print(f"  • {pattern.name}")


def example_8_benefit_search():
    """示例 8：按益处搜索"""
    print("\n" + "=" * 50)
    print("示例 8：按益处搜索技巧")
    print("=" * 50)
    
    benefits = ["睡眠", "专注", "压力", "放松", "能量", "焦虑"]
    
    for benefit in benefits:
        techniques = get_techniques_by_benefit(benefit)
        print(f"\n'{benefit}' 相关技巧 ({len(techniques)} 种):")
        for tech in techniques:
            pattern = get_pattern(tech)
            print(f"  • {pattern.name}")


def example_9_oxygen_efficiency():
    """示例 9：氧气效率分析"""
    print("\n" + "=" * 50)
    print("示例 9：氧气效率分析")
    print("=" * 50)
    
    techniques = [
        BreathingTechnique.RELAXATION_478,
        BreathingTechnique.BOX_BREATHING,
        BreathingTechnique.COHERENT,
        BreathingTechnique.ENERGIZING,
    ]
    
    print("\n效率分析:")
    for tech in techniques:
        pattern = get_pattern(tech)
        efficiency = calculate_oxygen_efficiency(pattern)
        
        print(f"\n{pattern.name}:")
        print(f"  呼吸频率: {efficiency['breaths_per_minute']} 次/分")
        print(f"  分钟通气量: {efficiency['minute_volume_liters']} 升/分")
        print(f"  吸气比例: {efficiency['inhale_ratio']:.0%}")
        print(f"  呼气比例: {efficiency['exhale_ratio']:.0%}")
        print(f"  放松分数: {efficiency['estimated_relaxation_score']}")


def example_10_compare_techniques():
    """示例 10：比较技巧"""
    print("\n" + "=" * 50)
    print("示例 10：比较多个技巧")
    print("=" * 50)
    
    comparison = compare_techniques([
        BreathingTechnique.RELAXATION_478,
        BreathingTechnique.BOX_BREATHING,
        BreathingTechnique.COHERENT,
        BreathingTechnique.SLEEP_BREATH,
    ])
    
    print("\n技巧比较表:")
    print("-" * 80)
    
    for item in comparison:
        print(f"\n{item['name']}:")
        print(f"  时长: {item['total_duration']}秒 | 难度: {item['difficulty']}")
        print(f"  呼吸频率: {item['breaths_per_minute']} 次/分")
        print(f"  放松分数: {item['relaxation_score']}")
        print(f"  益处: {', '.join(item['benefits'][:2])}...")


def example_11_text_guide():
    """示例 11：生成文本指导"""
    print("\n" + "=" * 50)
    print("示例 11：生成文本指导")
    print("=" * 50)
    
    # 生理性叹息的指导
    pattern = get_pattern(BreathingTechnique.PHYSIOLOGICAL_SIGH)
    guide = generate_breathing_text_guide(pattern, 3)
    print(guide)


def example_12_hrv_estimate():
    """示例 12：HRV 估算"""
    print("\n" + "=" * 50)
    print("示例 12：心率变异性估算")
    print("=" * 50)
    
    techniques = [
        BreathingTechnique.COHERENT,    # 6 次/分
        BreathingTechnique.RESONANT,    # 5.5 次/分
        BreathingTechnique.BOX_BREATHING,  # 4 次/分
        BreathingTechnique.ENERGIZING,  # 30 次/分
    ]
    
    print("\nHRV 影响分数 (越高越好):")
    for tech in techniques:
        pattern = get_pattern(tech)
        hrv = calculate_hrv_estimate(pattern)
        bpm = calculate_breaths_per_minute(pattern)
        print(f"  {pattern.name}: {hrv:.0f}/100 ({bpm:.1f} 次/分)")
    
    print("\n注意: 5-7 次/分钟的呼吸频率通常对 HRV 最优")


def example_13_quick_functions():
    """示例 13：便捷函数"""
    print("\n" + "=" * 50)
    print("示例 13：便捷函数")
    print("=" * 50)
    
    # 快速放松
    relax = quick_relax(cycles=3)
    print(f"\n快速放松: {relax.name}")
    print(f"  循环: {relax.cycles} 次")
    print(f"  总时长: {calculate_total_duration(relax, relax.cycles):.0f} 秒")
    
    # 快速睡眠
    sleep = quick_sleep(cycles=20)
    print(f"\n快速睡眠: {sleep.name}")
    print(f"  循环: {sleep.cycles} 次")
    print(f"  总时长: {calculate_total_duration(sleep, sleep.cycles):.0f} 秒")
    
    # 快速激活
    energy = quick_energy(cycles=15)
    print(f"\n快速激活: {energy.name}")
    print(f"  循环: {energy.cycles} 次")
    print(f"  注意: {energy.contraindications[0] if energy.contraindications else '无'}")


def example_14_session_steps():
    """示例 14：生成完整练习步骤"""
    print("\n" + "=" * 50)
    print("示例 14：生成完整练习步骤序列")
    print("=" * 50)
    
    pattern = get_pattern(BreathingTechnique.TACTICAL)
    steps = generate_session_steps(pattern, 2)
    
    print(f"\n{pattern.name} - 2 循环:")
    print()
    
    for cycle, step in steps:
        elapsed = sum(s.duration for c, s in steps[:steps.index((cycle, step))])
        print(f"  [{format_timer_display(elapsed)}] 循环{cycle} {step.instruction} ({step.duration}秒)")


def example_15_breathing_session():
    """示例 15：使用练习会话管理器"""
    print("\n" + "=" * 50)
    print("示例 15：练习会话管理器")
    print("=" * 50)
    
    session = BreathingSession(BreathingTechnique.COHERENT)
    
    print(f"\n开始练习: {session.pattern.name}")
    
    session.start(cycles=3)
    
    print(f"  目标循环: {session.target_cycles}")
    print(f"  步骤数: {len(session.pattern.steps)}")
    
    # 模拟查看进度
    progress = session.get_progress()
    print(f"\n当前进度:")
    print(f"  当前循环: {progress['current_cycle']}/{progress['total_cycles']}")
    print(f"  进度: {progress['progress_percent']:.0f}%")
    
    # 模拟几步
    print("\n  模拟练习步骤:")
    current_step = session.get_current_step()
    print(f"    当前: {current_step.instruction} ({current_step.duration}秒)")
    
    session.stop()
    summary = session.get_summary()
    print(f"\n练习结束:")
    print(f"  完成循环: {summary.cycles_completed}")
    print(f"  总时间: {summary.total_time:.1f}秒")


def example_16_practical_scenarios():
    """示例 16：实际场景应用"""
    print("\n" + "=" * 50)
    print("示例 16：实际场景应用")
    print("=" * 50)
    
    # 场景 1：工作压力大
    print("\n场景 1: 工作压力大，需要快速减压")
    tech = get_recommended_technique("stress", time_available=30)
    pattern = get_pattern(tech)
    print(f"  推荐: {pattern.name}")
    print(f"  时间: {pattern.total_duration * pattern.cycles:.0f}秒")
    print(f"  说明: {pattern.description}")
    
    # 场景 2：睡前放松
    print("\n场景 2: 准备睡觉，需要放松")
    tech = get_recommended_technique("sleep")
    pattern = get_pattern(tech)
    print(f"  推荐: {pattern.name}")
    print(f"  时间: {pattern.total_duration * pattern.cycles:.0f}秒")
    print(f"  呼吸频率: {calculate_breaths_per_minute(pattern):.1f} 次/分")
    
    # 场景 3：需要集中注意力
    print("\n场景 3: 考试前需要集中注意力")
    tech = get_recommended_technique("focus")
    pattern = get_pattern(tech)
    print(f"  推荐: {pattern.name}")
    print(f"  益处: {pattern.benefits[0]}")
    
    # 场景 4：突发焦虑
    print("\n场景 4: 突发焦虑，需要快速缓解")
    tech = get_recommended_technique("anxiety")
    pattern = get_pattern(tech)
    print(f"  推荐: {pattern.name}")
    print(f"  单循环: {pattern.total_duration}秒")
    print(f"  快速见效: {pattern.benefits[0]}")


def example_17_special_techniques():
    """示例 17：特殊技巧详解"""
    print("\n" + "=" * 50)
    print("示例 17：特殊技巧详解")
    print("=" * 50)
    
    # Wim Hof 呼吸法
    print("\n1. Wim Hof 呼吸法 (高强度):")
    pattern = get_pattern(BreathingTechnique.WIM_HOF)
    print(f"   难度: {pattern.difficulty}")
    print(f"   呼吸频率: {calculate_breaths_per_minute(pattern):.0f} 次/分")
    print(f"   ⚠️ 禁忌:")
    for contra in pattern.contraindications:
        print(f"      • {contra}")
    
    # 交替鼻孔呼吸
    print("\n2. 交替鼻孔呼吸 (瑜伽技术):")
    pattern = get_pattern(BreathingTechnique.ALTERNATE_NOSTRIL)
    print(f"   步骤数: {len(pattern.steps)}")
    print("   步骤详情:")
    for step in pattern.steps:
        print(f"      • {step.instruction} ({step.duration}秒)")
    
    # 生理性叹息
    print("\n3. 生理性叹息 (斯坦福研究):")
    pattern = get_pattern(BreathingTechnique.PHYSIOLOGICAL_SIGH)
    print(f"   描述: {pattern.description}")
    print(f"   特点: 双吸气后长呼气")
    print("   步骤:")
    for step in pattern.steps:
        print(f"      • {step.phase.value}: {step.duration}秒")


def run_all_examples():
    """运行所有示例"""
    examples = [
        example_1_basic_usage,
        example_2_list_all_techniques,
        example_3_find_technique_by_name,
        example_4_calculate_timing,
        example_5_custom_pattern,
        example_6_recommendation,
        example_7_difficulty_filter,
        example_8_benefit_search,
        example_9_oxygen_efficiency,
        example_10_compare_techniques,
        example_11_text_guide,
        example_12_hrv_estimate,
        example_13_quick_functions,
        example_14_session_steps,
        example_15_breathing_session,
        example_16_practical_scenarios,
        example_17_special_techniques,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n示例 {example.__name__} 出错: {e}")
    
    print("\n" + "=" * 50)
    print("所有示例完成!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_examples()