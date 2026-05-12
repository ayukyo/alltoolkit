"""
Breathing Exercise Utils Tests - 呼吸练习工具测试

测试所有核心功能，确保零外部依赖。
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from breathing_exercise_utils.mod import (
    BreathingTechnique,
    BreathPhase,
    BreathingStep,
    BreathingPattern,
    ExerciseSession,
    BreathingSession,
    
    # 创建函数
    create_478_relaxation,
    create_box_breathing,
    create_ujjayi,
    create_diaphragmatic,
    create_alternate_nostril,
    create_energizing,
    create_meditation,
    create_sleep_breath,
    create_physiological_sigh,
    create_tactical,
    create_coherent,
    create_resonant,
    create_wim_hof,
    create_calming,
    create_focus,
    
    # 核心功能
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
    get_quick_relief_sequence,
    calculate_hrv_estimate,
    
    # 便捷函数
    quick_relax,
    quick_sleep,
    quick_energy,
    print_pattern_info,
)


def test_all_pattern_creators():
    """测试所有呼吸模式创建函数"""
    print("Testing all pattern creators...")
    
    patterns = [
        create_478_relaxation(),
        create_box_breathing(),
        create_ujjayi(),
        create_diaphragmatic(),
        create_alternate_nostril(),
        create_energizing(),
        create_meditation(),
        create_sleep_breath(),
        create_physiological_sigh(),
        create_tactical(),
        create_coherent(),
        create_resonant(),
        create_wim_hof(),
        create_calming(),
        create_focus(),
    ]
    
    assert len(patterns) == 15
    
    for pattern in patterns:
        assert isinstance(pattern, BreathingPattern)
        assert len(pattern.steps) > 0
        assert pattern.total_duration > 0
        assert pattern.name
        assert pattern.technique
        
        # 验证步骤时间总和等于总时长
        total = sum(s.duration for s in pattern.steps)
        assert abs(total - pattern.total_duration) < 0.1
    
    print("  ✓ All pattern creators work correctly")


def test_get_pattern():
    """测试获取呼吸模式"""
    print("Testing get_pattern...")
    
    # 测试每种技巧
    for tech in BreathingTechnique:
        pattern = get_pattern(tech)
        assert isinstance(pattern, BreathingPattern)
        assert pattern.technique == tech
    
    # 测试无效技巧
    try:
        get_pattern("invalid")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("  ✓ get_pattern works correctly")


def test_list_techniques():
    """测试列出技巧"""
    print("Testing list_techniques...")
    
    techniques = list_techniques()
    assert len(techniques) == 15
    assert BreathingTechnique.RELAXATION_478 in techniques
    assert BreathingTechnique.BOX_BREATHING in techniques
    
    print("  ✓ list_techniques returns all 15 techniques")


def test_get_technique_by_name():
    """测试通过名称获取技巧"""
    print("Testing get_technique_by_name...")
    
    # 英文名称
    assert get_technique_by_name("4-7-8") == BreathingTechnique.RELAXATION_478
    assert get_technique_by_name("box") == BreathingTechnique.BOX_BREATHING
    assert get_technique_by_name("ujjayi") == BreathingTechnique.UJJAYI
    assert get_technique_by_name("wim_hof") == BreathingTechnique.WIM_HOF
    
    # 中文名称
    assert get_technique_by_name("放松") == BreathingTechnique.RELAXATION_478
    assert get_technique_by_name("箱式呼吸") == BreathingTechnique.BOX_BREATHING
    assert get_technique_by_name("腹式呼吸") == BreathingTechnique.DIAPHRAGMATIC
    
    # 无效名称
    assert get_technique_by_name("unknown") is None
    
    print("  ✓ get_technique_by_name works for English and Chinese")


def test_calculate_total_duration():
    """测试计算总时长"""
    print("Testing calculate_total_duration...")
    
    pattern = get_pattern(BreathingTechnique.RELAXATION_478)
    
    # 单循环
    duration1 = calculate_total_duration(pattern, 1)
    assert duration1 == pattern.total_duration
    
    # 多循环
    duration4 = calculate_total_duration(pattern, 4)
    assert duration4 == pattern.total_duration * 4
    
    # 验证 4-7-8 呼吸：4+7+8 = 19秒
    assert duration1 == 19.0
    assert duration4 == 76.0
    
    print("  ✓ calculate_total_duration calculates correctly")


def test_calculate_breaths_per_minute():
    """测试计算每分钟呼吸次数"""
    print("Testing calculate_breaths_per_minute...")
    
    # 4-7-8 呼吸：19秒一轮
    pattern_478 = get_pattern(BreathingTechnique.RELAXATION_478)
    bpm_478 = calculate_breaths_per_minute(pattern_478)
    assert abs(bpm_478 - (60/19)) < 0.1
    assert bpm_478 < 4  # 约 3.16 次/分
    
    # 激活呼吸：2秒一轮
    pattern_energy = get_pattern(BreathingTechnique.ENERGIZING)
    bpm_energy = calculate_breaths_per_minute(pattern_energy)
    assert bpm_energy == 30  # 60/2 = 30 次/分
    
    # 连贯呼吸：10秒一轮
    pattern_coherent = get_pattern(BreathingTechnique.COHERENT)
    bpm_coherent = calculate_breaths_per_minute(pattern_coherent)
    assert bpm_coherent == 6  # 60/10 = 6 次/分
    
    print("  ✓ calculate_breaths_per_minute calculates correctly")


def test_generate_session_steps():
    """测试生成会话步骤"""
    print("Testing generate_session_steps...")
    
    pattern = get_pattern(BreathingTechnique.BOX_BREATHING)
    
    # 默认循环次数
    steps = generate_session_steps(pattern)
    assert len(steps) == 4 * pattern.cycles  # 4步 * 循环数
    
    # 自定义循环次数
    steps_custom = generate_session_steps(pattern, 3)
    assert len(steps_custom) == 4 * 3
    
    # 验证循环编号
    for i, (cycle, step) in enumerate(steps_custom):
        expected_cycle = (i // 4) + 1
        assert cycle == expected_cycle
        assert isinstance(step, BreathingStep)
    
    print("  ✓ generate_session_steps generates correct sequence")


def test_create_custom_pattern():
    """测试创建自定义模式"""
    print("Testing create_custom_pattern...")
    
    # 简单模式
    custom = create_custom_pattern(
        name="简单呼吸",
        inhale=4.0,
        exhale=4.0,
        cycles=10,
        benefits=["放松"],
        description="测试模式"
    )
    
    assert custom.name == "简单呼吸"
    assert custom.total_duration == 8.0
    assert len(custom.steps) == 2
    assert custom.cycles == 10
    
    # 复杂模式
    custom_full = create_custom_pattern(
        name="完整模式",
        inhale=4.0,
        hold_in=4.0,
        exhale=8.0,
        hold_out=2.0,
        cycles=5
    )
    
    assert custom_full.total_duration == 18.0
    assert len(custom_full.steps) == 4
    
    # 验证步骤顺序
    phases = [s.phase for s in custom_full.steps]
    assert phases == [
        BreathPhase.INHALE,
        BreathPhase.HOLD_IN,
        BreathPhase.EXHALE,
        BreathPhase.HOLD_OUT
    ]
    
    print("  ✓ create_custom_pattern creates valid patterns")


def test_format_timer_display():
    """测试时间格式化"""
    print("Testing format_timer_display...")
    
    # 秒数显示
    assert format_timer_display(30) == "30s"
    assert format_timer_display(5) == "5s"
    
    # 分钟显示
    assert format_timer_display(60) == "1:00"
    assert format_timer_display(90) == "1:30"
    assert format_timer_display(120) == "2:00"
    assert format_timer_display(125) == "2:05"
    
    print("  ✓ format_timer_display formats correctly")


def test_get_recommended_technique():
    """测试根据目标推荐技巧"""
    print("Testing get_recommended_technique...")
    
    # 测试各种目标
    assert get_recommended_technique("sleep") in [
        BreathingTechnique.SLEEP_BREATH,
        BreathingTechnique.CALMING
    ]
    
    assert get_recommended_technique("relax") in [
        BreathingTechnique.RELAXATION_478,
        BreathingTechnique.CALMING
    ]
    
    assert get_recommended_technique("energy") in [
        BreathingTechnique.ENERGIZING,
        BreathingTechnique.WIM_HOF
    ]
    
    assert get_recommended_technique("focus") in [
        BreathingTechnique.FOCUS,
        BreathingTechnique.BOX_BREATHING
    ]
    
    assert get_recommended_technique("anxiety") in [
        BreathingTechnique.PHYSIOLOGICAL_SIGH,
        BreathingTechnique.CALMING
    ]
    
    # 测试时间限制
    tech_short = get_recommended_technique("relax", time_available=20)
    pattern = get_pattern(tech_short)
    # 确保推荐的技巧能在时间内完成一轮
    assert pattern.total_duration <= 20
    
    print("  ✓ get_recommended_technique recommends appropriate techniques")


def test_get_techniques_by_difficulty():
    """测试按难度获取技巧"""
    print("Testing get_techniques_by_difficulty...")
    
    easy = get_techniques_by_difficulty("easy")
    medium = get_techniques_by_difficulty("medium")
    hard = get_techniques_by_difficulty("hard")
    
    assert len(easy) > 0
    assert len(medium) > 0
    assert len(hard) > 0
    
    # 确保分类正确
    for tech in easy:
        pattern = get_pattern(tech)
        assert pattern.difficulty == "easy"
    
    for tech in medium:
        pattern = get_pattern(tech)
        assert pattern.difficulty == "medium"
    
    for tech in hard:
        pattern = get_pattern(tech)
        assert pattern.difficulty == "hard"
    
    # 确保所有技巧都被分类
    total = len(easy) + len(medium) + len(hard)
    assert total == 15
    
    print("  ✓ get_techniques_by_difficulty categorizes correctly")


def test_get_techniques_by_benefit():
    """测试按益处查找技巧"""
    print("Testing get_techniques_by_benefit...")
    
    # 搜索睡眠相关
    sleep_related = get_techniques_by_benefit("睡眠")
    assert len(sleep_related) > 0
    assert BreathingTechnique.SLEEP_BREATH in sleep_related
    
    # 搜索压力相关
    stress_related = get_techniques_by_benefit("压力")
    assert len(stress_related) > 0
    
    # 搜索专注相关
    focus_related = get_techniques_by_benefit("专注")
    assert len(focus_related) > 0
    
    print("  ✓ get_techniques_by_benefit finds relevant techniques")


def test_calculate_oxygen_efficiency():
    """测试氧气效率计算"""
    print("Testing calculate_oxygen_efficiency...")
    
    # 慢呼吸
    pattern_478 = get_pattern(BreathingTechnique.RELAXATION_478)
    efficiency_478 = calculate_oxygen_efficiency(pattern_478)
    
    assert "breaths_per_minute" in efficiency_478
    assert "minute_volume_liters" in efficiency_478
    assert "inhale_ratio" in efficiency_478
    assert "exhale_ratio" in efficiency_478
    assert "estimated_relaxation_score" in efficiency_478
    
    # 4-7-8 呼吸：吸气4秒，呼气8秒，总19秒
    assert abs(efficiency_478["inhale_ratio"] - (4/19)) < 0.1
    assert abs(efficiency_478["exhale_ratio"] - (8/19)) < 0.1
    # 放松分数 = 呼气比/吸气比 = 8/4 = 2
    assert abs(efficiency_478["estimated_relaxation_score"] - 2.0) < 0.1
    
    print("  ✓ calculate_oxygen_efficiency calculates correctly")


def test_compare_techniques():
    """测试技巧比较"""
    print("Testing compare_techniques...")
    
    comparison = compare_techniques([
        BreathingTechnique.RELAXATION_478,
        BreathingTechnique.BOX_BREATHING,
        BreathingTechnique.COHERENT
    ])
    
    assert len(comparison) == 3
    
    for item in comparison:
        assert "technique" in item
        assert "name" in item
        assert "total_duration" in item
        assert "difficulty" in item
        assert "breaths_per_minute" in item
        assert "relaxation_score" in item
        assert "benefits" in item
    
    # 验证顺序
    assert comparison[0]["technique"] == "relaxation_478"
    assert comparison[1]["technique"] == "box_breathing"
    assert comparison[2]["technique"] == "coherent"
    
    print("  ✓ compare_techniques compares correctly")


def test_generate_breathing_text_guide():
    """测试生成文本指导"""
    print("Testing generate_breathing_text_guide...")
    
    pattern = get_pattern(BreathingTechnique.BOX_BREATHING)
    guide = generate_breathing_text_guide(pattern, 2)
    
    assert "箱式呼吸" in guide
    assert "难度" in guide
    assert "第 1/2 轮" in guide
    assert "第 2/2 轮" in guide
    assert "吸气" in guide
    assert "屏气" in guide
    assert "呼气" in guide
    assert "练习完成" in guide
    
    print("  ✓ generate_breathing_text_guide generates complete guide")


def test_get_quick_relief_sequence():
    """测试快速缓解序列"""
    print("Testing get_quick_relief_sequence...")
    
    sequence = get_quick_relief_sequence()
    
    assert len(sequence) == 3
    assert sequence[0].phase == BreathPhase.INHALE
    assert sequence[1].phase == BreathPhase.INHALE
    assert sequence[2].phase == BreathPhase.EXHALE
    
    # 总时长约 5秒
    total = sum(s.duration for s in sequence)
    assert total == 5.0
    
    print("  ✓ get_quick_relief_sequence returns valid sequence")


def test_calculate_hrv_estimate():
    """测试 HRV 估算"""
    print("Testing calculate_hrv_estimate...")
    
    # 连贯呼吸（6次/分）- 最佳 HRV
    pattern_coherent = get_pattern(BreathingTechnique.COHERENT)
    hrv_coherent = calculate_hrv_estimate(pattern_coherent)
    assert hrv_coherent == 95.0  # 最优
    
    # 4-7-8 呼吸（约3.16次/分）- 在 3-10 次/分范围内
    pattern_478 = get_pattern(BreathingTechnique.RELAXATION_478)
    hrv_478 = calculate_hrv_estimate(pattern_478)
    assert hrv_478 == 70.0  # 在 3-10 次/分范围内
    
    # 共振呼吸（约5.5次/分）- 在 5-7 次/分范围内，最优
    pattern_resonant = get_pattern(BreathingTechnique.RESONANT)
    hrv_resonant = calculate_hrv_estimate(pattern_resonant)
    assert hrv_resonant == 95.0  # 在最优范围内
    
    # 箱式呼吸（约3.75次/分）- 在 3-10 次/分范围内
    pattern_box = get_pattern(BreathingTechnique.BOX_BREATHING)
    hrv_box = calculate_hrv_estimate(pattern_box)
    assert hrv_box == 70.0  # 在 3-10 次/分范围内
    
    # 激活呼吸（30次/分）
    pattern_energy = get_pattern(BreathingTechnique.ENERGIZING)
    hrv_energy = calculate_hrv_estimate(pattern_energy)
    assert hrv_energy < 50  # 较低
    
    print("  ✓ calculate_hrv_estimate estimates correctly")


def test_breathing_session():
    """测试练习会话管理"""
    print("Testing BreathingSession...")
    
    session = BreathingSession(BreathingTechnique.BOX_BREATHING)
    
    # 初始状态
    assert session.technique == BreathingTechnique.BOX_BREATHING
    assert session.cycles_completed == 0
    assert session.is_running == False
    
    # 开始练习
    session.start(cycles=2)
    assert session.is_running == True
    assert session.current_cycle == 1
    
    # 获取当前步骤
    step = session.get_current_step()
    assert step is not None
    assert step.phase == BreathPhase.INHALE
    
    # 获取进度
    progress = session.get_progress()
    assert progress["current_cycle"] == 1
    assert progress["total_cycles"] == 2
    assert progress["cycles_completed"] == 0
    
    # 暂停/恢复
    session.pause()
    assert session.is_paused == True
    
    session.resume()
    assert session.is_paused == False
    
    # 停止
    session.stop()
    assert session.is_running == False
    assert session.end_time is not None
    
    # 获取摘要
    summary = session.get_summary()
    assert isinstance(summary, ExerciseSession)
    assert summary.technique == BreathingTechnique.BOX_BREATHING
    
    print("  ✓ BreathingSession manages sessions correctly")


def test_quick_functions():
    """测试便捷函数"""
    print("Testing quick functions...")
    
    # 快速放松
    relax = quick_relax(cycles=3)
    assert relax.technique == BreathingTechnique.RELAXATION_478
    assert relax.cycles == 3
    
    # 快速睡眠
    sleep = quick_sleep(cycles=10)
    assert sleep.technique == BreathingTechnique.SLEEP_BREATH
    assert sleep.cycles == 10
    
    # 快速激活
    energy = quick_energy(cycles=15)
    assert energy.technique == BreathingTechnique.ENERGIZING
    assert energy.cycles == 15
    
    print("  ✓ Quick functions return correct patterns")


def test_pattern_step_validation():
    """测试步骤结构验证"""
    print("Testing pattern step validation...")
    
    # 测试所有模式的步骤
    for tech in BreathingTechnique:
        pattern = get_pattern(tech)
        
        for step in pattern.steps:
            assert isinstance(step.phase, BreathPhase)
            assert step.duration > 0
            assert step.description
            assert step.instruction
    
    print("  ✓ All pattern steps have valid structure")


def test_box_breathing_specifics():
    """测试箱式呼吸具体数值"""
    print("Testing box breathing specifics...")
    
    pattern = create_box_breathing()
    
    # 箱式呼吸：4-4-4-4
    assert len(pattern.steps) == 4
    assert all(s.duration == 4.0 for s in pattern.steps)
    assert pattern.total_duration == 16.0
    
    # 验证四个阶段
    phases = [s.phase for s in pattern.steps]
    assert phases == [
        BreathPhase.INHALE,
        BreathPhase.HOLD_IN,
        BreathPhase.EXHALE,
        BreathPhase.HOLD_OUT
    ]
    
    print("  ✓ Box breathing has correct 4-4-4-4 pattern")


def test_478_breathing_specifics():
    """测试 4-7-8 呼吸具体数值"""
    print("Testing 4-7-8 breathing specifics...")
    
    pattern = create_478_relaxation()
    
    # 4-7-8 呼吸
    assert len(pattern.steps) == 3
    
    durations = [s.duration for s in pattern.steps]
    assert durations == [4.0, 7.0, 8.0]
    assert pattern.total_duration == 19.0
    
    # 验证阶段
    phases = [s.phase for s in pattern.steps]
    assert phases == [
        BreathPhase.INHALE,
        BreathPhase.HOLD_IN,
        BreathPhase.EXHALE
    ]
    
    print("  ✓ 4-7-8 breathing has correct 4-7-8 pattern")


def test_alternate_nostril_specifics():
    """测试交替鼻孔呼吸具体结构"""
    print("Testing alternate nostril breathing specifics...")
    
    pattern = create_alternate_nostril()
    
    # 交替鼻孔呼吸有特殊的步骤
    assert len(pattern.steps) == 6
    
    # 验证包含左/右鼻孔吸气步骤
    phases = [s.phase for s in pattern.steps]
    assert BreathPhase.INHALE_LEFT in phases
    assert BreathPhase.INHALE_RIGHT in phases
    
    print("  ✓ Alternate nostril has correct structure")


def test_wim_hof_specifics():
    """测试 Wim Hof 呼吸具体结构"""
    print("Testing Wim Hof breathing specifics...")
    
    pattern = create_wim_hof()
    
    # Wim Hof 呼吸难度高
    assert pattern.difficulty == "hard"
    
    # 有大量禁忌
    assert len(pattern.contraindications) > 0
    # 检查包含心脏相关警告
    heart_warning_found = any("心脏" in c or "heart" in c.lower() for c in pattern.contraindications)
    assert heart_warning_found
    
    # 快速呼吸
    assert pattern.total_duration < 3.0
    
    print("  ✓ Wim Hof has correct structure and warnings")


def test_physiological_sigh_specifics():
    """测试生理性叹息具体结构"""
    print("Testing physiological sigh specifics...")
    
    pattern = create_physiological_sigh()
    
    # 生理性叹息：1.5 + 0.5 + 4
    assert len(pattern.steps) == 3
    
    durations = [s.duration for s in pattern.steps]
    assert durations == [1.5, 0.5, 4.0]
    assert pattern.total_duration == 6.0
    
    # 双吸气步骤
    phases = [s.phase for s in pattern.steps]
    assert phases[:2] == [BreathPhase.INHALE, BreathPhase.INHALE]
    
    print("  ✓ Physiological sigh has correct double-inhale structure")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Breathing Exercise Utils Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_all_pattern_creators,
        test_get_pattern,
        test_list_techniques,
        test_get_technique_by_name,
        test_calculate_total_duration,
        test_calculate_breaths_per_minute,
        test_generate_session_steps,
        test_create_custom_pattern,
        test_format_timer_display,
        test_get_recommended_technique,
        test_get_techniques_by_difficulty,
        test_get_techniques_by_benefit,
        test_calculate_oxygen_efficiency,
        test_compare_techniques,
        test_generate_breathing_text_guide,
        test_get_quick_relief_sequence,
        test_calculate_hrv_estimate,
        test_breathing_session,
        test_quick_functions,
        test_pattern_step_validation,
        test_box_breathing_specifics,
        test_478_breathing_specifics,
        test_alternate_nostril_specifics,
        test_wim_hof_specifics,
        test_physiological_sigh_specifics,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  ✗ {test.__name__} failed: {e}")
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)