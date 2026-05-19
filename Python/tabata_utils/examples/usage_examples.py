"""
Tabata Utilities 使用示例

展示 Tabata 高强度间歇训练工具的各种用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from typing import List, Tuple

# 导入模块
from mod import (
    PhaseType,
    TabataSession,
    TabataTimer,
    TabataPresets,
    TabataBuilder,
    TabataFormatter,
    TabataCalculator,
    SessionStats,
    create_tabata,
    get_preset,
    list_presets,
)


def example_01_basic_usage():
    """
    示例1：基本使用
    
    展示如何创建和使用基本的 Tabata 训练会话。
    """
    print("\n" + "=" * 50)
    print("示例1：基本使用")
    print("=" * 50)
    
    # 创建标准 Tabata 训练
    session = create_tabata()
    
    # 显示训练信息
    print(TabataFormatter.format_session(session))
    
    # 显示总时长
    print(f"\n总时长: {TabataFormatter.format_duration(session.total_duration)}")
    print(f"总运动时间: {TabataFormatter.format_duration(session.total_work_time)}")
    print(f"总休息时间: {TabataFormatter.format_duration(session.total_rest_time)}")


def example_02_presets():
    """
    示例2：使用预设
    
    展示如何使用预设训练方案。
    """
    print("\n" + "=" * 50)
    print("示例2：使用预设")
    print("=" * 50)
    
    # 列出所有可用预设
    print("可用预设方案:")
    for name in list_presets():
        preset = get_preset(name)
        if preset:
            print(f"  • {name}: {preset.rounds}轮 × {preset.work_duration}s运动 + {preset.rest_duration}s休息")
    
    # 使用核心训练预设
    print("\n核心训练预设详情:")
    core = TabataPresets.CORE
    print(TabataFormatter.format_session(core))


def example_03_custom_session():
    """
    示例3：创建自定义训练
    
    展示如何使用 Builder 创建自定义训练方案。
    """
    print("\n" + "=" * 50)
    print("示例3：创建自定义训练")
    print("=" * 50)
    
    # 使用 Builder 创建自定义训练
    custom = (TabataBuilder()
              .name("我的健身计划")
              .rounds(6)
              .work(25)
              .rest(15)
              .prepare(8)
              .exercises(
                  "俯卧撑",
                  "深蹲",
                  "波比跳",
                  "平板支撑",
                  "跳跃深蹲",
                  "登山跑"
              )
              .build())
    
    print(TabataFormatter.format_session(custom))
    
    # 查看每轮运动
    print("\n每轮运动安排:")
    for i in range(1, custom.rounds + 1):
        print(f"  第{i}轮: {custom.get_exercise(i)}")


def example_04_calculations():
    """
    示例4：训练计算
    
    展示各种训练相关的计算功能。
    """
    print("\n" + "=" * 50)
    print("示例4：训练计算")
    print("=" * 50)
    
    session = TabataPresets.STANDARD
    
    # 卡路里计算
    print("卡路里消耗估算:")
    for weight in [50, 60, 70, 80, 90]:
        calories = TabataCalculator.calories_burned(session, weight_kg=weight)
        print(f"  {weight}kg: {calories:.0f} kcal")
    
    # 心率区间
    print("\n30岁心率区间:")
    zones = TabataCalculator.heart_rate_zones(30)
    for zone_name, (low, high) in zones.items():
        print(f"  {zone_name}: {low}-{high} bpm")
    
    # 推荐轮数
    print("\n根据健身水平推荐轮数:")
    for level in ["beginner", "intermediate", "advanced", "elite"]:
        rounds = TabataCalculator.recommended_rounds(level)
        print(f"  {level}: {rounds}轮")
    
    # 运动休息比
    print(f"\n运动休息比:")
    print(f"  标准 Tabata: {TabataCalculator.work_rest_ratio(session):.1f}:1")
    extended = TabataPresets.EXTENDED
    print(f"  延长 Tabata: {TabataCalculator.work_rest_ratio(extended):.1f}:1")


def example_05_formatter():
    """
    示例5：格式化显示
    
    展示各种格式化输出功能。
    """
    print("\n" + "=" * 50)
    print("示例5：格式化显示")
    print("=" * 50)
    
    # 时长格式化
    print("时长格式化:")
    durations = [30, 60, 90, 120, 180, 240, 300]
    for d in durations:
        print(f"  {d}秒 -> {TabataFormatter.format_duration(d)}")
    
    # 倒计时格式化
    print("\n倒计时格式化:")
    countdowns = [0, 10.5, 20.7, 59.9, 60, 90, 120.5]
    for c in countdowns:
        print(f"  {c}秒 -> {TabataFormatter.format_countdown(c)}")
    
    # 进度条
    print("\n进度条:")
    for progress in [0, 25, 50, 75, 100]:
        print(f"  {progress}%: {TabataFormatter.format_progress(progress, 100, width=20)}")


def example_06_timer_simulation():
    """
    示例6：计时器模拟
    
    模拟计时器运行（不实际等待）。
    """
    print("\n" + "=" * 50)
    print("示例6：计时器模拟")
    print("=" * 50)
    
    # 创建短训练用于演示
    session = TabataSession(
        rounds=2,
        work_duration=20,
        rest_duration=10,
        prepare_duration=5,
        name="短训练演示"
    )
    
    timer = TabataTimer(session)
    
    # 记录回调事件
    phase_changes: List[Tuple[PhaseType, int]] = []
    
    def on_phase_change(phase: PhaseType, round_num: int):
        phase_changes.append((phase, round_num))
        phase_name = {
            PhaseType.PREPARE: "准备",
            PhaseType.WORK: "运动",
            PhaseType.REST: "休息",
            PhaseType.COMPLETE: "完成"
        }
        if phase == PhaseType.WORK:
            exercise = session.get_exercise(round_num)
            print(f"  [{phase_name[phase]}] 第{round_num}轮: {exercise}")
        elif phase == PhaseType.REST:
            print(f"  [{phase_name[phase]}] 第{round_num}轮休息")
        else:
            print(f"  [{phase_name[phase]}]")
    
    timer.set_callbacks(on_phase_change=on_phase_change)
    
    # 模拟阶段推进（不实际等待时间）
    print("模拟计时器事件:")
    timer._notify_phase_change()  # 准备阶段
    
    # 手动推进模拟
    timer._current_phase = PhaseType.WORK
    timer._current_round = 1
    timer._notify_phase_change()
    
    timer._current_phase = PhaseType.REST
    timer._notify_phase_change()
    
    timer._current_phase = PhaseType.WORK
    timer._current_round = 2
    timer._notify_phase_change()
    
    timer._current_phase = PhaseType.REST
    timer._notify_phase_change()
    
    timer._current_phase = PhaseType.COMPLETE
    print("  [完成] 训练结束！")


def example_07_different_workouts():
    """
    示例7：不同类型的训练
    
    展示各种预设训练方案的特点。
    """
    print("\n" + "=" * 50)
    print("示例7：不同类型的训练")
    print("=" * 50)
    
    # 比较不同训练
    presets = [
        TabataPresets.STANDARD,
        TabataPresets.HIIT_BASIC,
        TabataPresets.CARDIO,
        TabataPresets.STRENGTH,
        TabataPresets.EMOM,
    ]
    
    print("不同训练方案对比:")
    print(f"{'名称':<20} {'轮数':<6} {'运动':<8} {'休息':<8} {'总时长':<10} {'运动/休息比'}")
    print("-" * 70)
    
    for preset in presets:
        total = TabataFormatter.format_duration(preset.total_duration)
        ratio = TabataCalculator.work_rest_ratio(preset)
        ratio_str = f"{ratio:.1f}:1" if ratio != float('inf') else "无休息"
        print(f"{preset.name:<20} {preset.rounds:<6} {preset.work_duration}s{'':<5} {preset.rest_duration}s{'':<5} {total:<10} {ratio_str}")


def example_08_stats():
    """
    示例8：训练统计
    
    展示训练完成后的统计信息。
    """
    print("\n" + "=" * 50)
    print("示例8：训练统计")
    print("=" * 50)
    
    session = TabataPresets.STANDARD
    
    # 创建模拟完成的统计
    stats = SessionStats(
        session=session,
        start_time=time.time() - 250,
        end_time=time.time(),
        completed_rounds=8,
        total_paused_time=0,
        calories_burned_estimate=TabataCalculator.calories_burned(session, 70)
    )
    
    print("训练完成统计:")
    print(TabataFormatter.format_stats(stats))
    
    # 转换为字典
    print("\n统计数据字典:")
    for key, value in stats.to_dict().items():
        print(f"  {key}: {value}")


def example_09_body_part_workouts():
    """
    示例9：部位训练
    
    展示针对特定部位的训练预设。
    """
    print("\n" + "=" * 50)
    print("示例9：部位训练预设")
    print("=" * 50)
    
    body_presets = [
        ("核心", TabataPresets.CORE),
        ("下肢", TabataPresets.LOWER_BODY),
        ("上肢", TabataPresets.UPPER_BODY),
    ]
    
    for part_name, preset in body_presets:
        print(f"\n{part_name}训练:")
        print(f"  训练名称: {preset.name}")
        print(f"  运动列表:")
        for i, exercise in enumerate(preset.exercises, 1):
            print(f"    {i}. {exercise}")


def example_10_advanced_custom():
    """
    示例10：高级自定义
    
    展示更复杂的自定义训练配置。
    """
    print("\n" + "=" * 50)
    print("示例10：高级自定义")
    print("=" * 50)
    
    # 创建一个混合训练
    # 第一阶段：热身（较低强度）
    warmup = (TabataBuilder()
              .name("热身阶段")
              .rounds(2)
              .work(30)
              .rest(30)
              .exercises("开合跳", "原地慢跑")
              .build())
    
    # 第二阶段：高强度
    high_intensity = (TabataBuilder()
                      .name("高强度阶段")
                      .rounds(6)
                      .work(20)
                      .rest(10)
                      .exercises(
                          "波比跳",
                          "俯卧撑",
                          "深蹲跳",
                          "平板支撑",
                          "登山跑",
                          "箭步蹲"
                      )
                      .build())
    
    # 第三阶段：放松
    cooldown = (TabataBuilder()
                .name("放松阶段")
                .rounds(2)
                .work(20)
                .rest(40)
                .exercises("静态拉伸", "深呼吸")
                .build())
    
    print("三阶段训练计划:")
    phases = [("热身", warmup), ("高强度", high_intensity), ("放松", cooldown)]
    
    total_time = 0
    for phase_name, session in phases:
        phase_time = session.total_duration
        total_time += phase_time
        print(f"\n{phase_name}阶段:")
        print(f"  时长: {TabataFormatter.format_duration(phase_time)}")
        print(f"  内容: {', '.join(session.exercises)}")
    
    print(f"\n总训练时长: {TabataFormatter.format_duration(total_time)}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("Tabata Utilities 使用示例集合")
    print("=" * 60)
    
    example_01_basic_usage()
    example_02_presets()
    example_03_custom_session()
    example_04_calculations()
    example_05_formatter()
    example_06_timer_simulation()
    example_07_different_workouts()
    example_08_stats()
    example_09_body_part_workouts()
    example_10_advanced_custom()
    
    print("\n" + "=" * 60)
    print("所有示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()