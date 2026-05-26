#!/usr/bin/env python3
"""
Meditation Timer Utils 使用示例

本示例展示如何使用冥想计时器工具的各种功能：
1. 基本冥想计时
2. 引导式呼吸练习
3. 会话记录和统计
4. 生成冥想铃声
"""

import time
from meditation_timer import (
    BreathingPattern,
    MeditationTimer,
    BreathingGuide,
    SessionRecorder,
    MeditationAssistant,
    format_duration,
    quick_meditation,
    guided_breathing,
)


def example_basic_timer():
    """示例1: 基本冥想计时"""
    print("\n" + "=" * 60)
    print("示例1: 基本冥想计时器")
    print("=" * 60)
    
    timer = MeditationTimer(duration_minutes=0.1)  # 6秒演示
    
    print("开始冥想...")
    timer.start()
    
    # 模拟进度显示
    for i in range(6):
        time.sleep(1)
        status = timer.get_status()
        elapsed = status["elapsed_seconds"]
        remaining = status["remaining_seconds"]
        progress = status["progress_percent"]
        
        bar = "█" * int(progress / 10) + "░" * (10 - int(progress / 10))
        print(f"  [{bar}] {progress:.0f}% - 剩余 {remaining:.0f}秒")
    
    session = timer.stop(completed=True)
    print(f"\n冥想完成! 时长: {format_duration(session.duration_seconds)}")


def example_breathing_guide():
    """示例2: 引导式呼吸练习"""
    print("\n" + "=" * 60)
    print("示例2: 引导式呼吸练习")
    print("=" * 60)
    
    guide = BreathingGuide()
    
    # 显示可用模式
    print("\n可用的呼吸模式:")
    for pattern in guide.get_available_patterns():
        print(f"  • {pattern['type']}: {pattern['total_duration']:.1f}秒/循环")
    
    # 选择箱式呼吸
    print("\n开始箱式呼吸练习 (2个循环)...")
    guide.set_pattern(BreathingPattern.BOX_BREATHING)
    
    cycle_count = [0]
    
    def on_phase(phase, duration, instruction):
        emoji_map = {
            "inhale": "🌬️ 吸气",
            "hold": "⏸️ 屏息",
            "exhale": "💨 呼气"
        }
        bar = "█" * int(duration) + "░" * (8 - int(duration))
        print(f"  {emoji_map.get(phase, phase)} {instruction} [{duration}s] {bar}")
        
        if phase == "exhale":
            cycle_count[0] += 1
    
    guide.start(0.5, on_phase)  # 30秒
    
    while guide.is_running():
        time.sleep(0.1)
    
    print(f"\n呼吸练习完成! 完成了 {cycle_count[0]} 个循环")


def example_session_recording():
    """示例3: 会话记录和统计"""
    print("\n" + "=" * 60)
    print("示例3: 会话记录和统计")
    print("=" * 60)
    
    # 创建临时存储
    import tempfile
    import os
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    temp_file.close()
    
    try:
        recorder = SessionRecorder(storage_path=temp_file.name)
        
        # 记录几个冥想会话
        print("\n记录冥想会话...")
        
        sessions_data = [
            ("2024-01-01T08:00:00", 600, True, "早晨冥想"),
            ("2024-01-02T08:00:00", 900, True, "深度冥想"),
            ("2024-01-03T20:00:00", 300, False, "晚上尝试"),
            ("2024-01-04T08:00:00", 600, True, "坚持!"),
        ]
        
        for start, duration, completed, notes in sessions_data:
            from meditation_timer import MeditationSession
            session = MeditationSession(
                start_time=start,
                end_time=start.replace(":00:00", f":{duration//60:02d}:00"),
                duration_seconds=duration,
                completed=completed,
                notes=notes
            )
            recorder.record_session(session)
            status = "✅" if completed else "⏹️"
            print(f"  {status} {start[:10]} - {format_duration(duration)} - {notes}")
        
        # 获取统计
        print("\n冥想统计:")
        stats = recorder.get_stats()
        print(f"  总会话数: {stats.total_sessions}")
        print(f"  总时长: {format_duration(stats.total_minutes * 60)}")
        print(f"  完成率: {stats.completed_sessions}/{stats.total_sessions}")
        print(f"  平均时长: {format_duration(stats.average_session_minutes * 60)}")
        print(f"  当前连续: {stats.current_streak} 天")
        print(f"  最长连续: {stats.longest_streak} 天")
        
        # 获取历史记录
        print("\n最近会话:")
        for session in recorder.get_sessions(limit=3):
            status = "✅" if session.completed else "⏹️"
            print(f"  {status} {session.start_time[:16]} - {format_duration(session.duration_seconds)}")
    
    finally:
        os.unlink(temp_file.name)


def example_meditation_assistant():
    """示例4: 综合冥想助手"""
    print("\n" + "=" * 60)
    print("示例4: 综合冥想助手")
    print("=" * 60)
    
    import tempfile
    import os
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    temp_file.close()
    
    try:
        assistant = MeditationAssistant(storage_path=temp_file.name)
        
        # 设置冥想参数
        duration_minutes = 0.1  # 6秒演示
        assistant.set_timer_duration(duration_minutes)
        
        print(f"\n设置 {duration_minutes * 60:.0f} 秒冥想会话")
        print("使用呼吸模式: 箱式呼吸")
        
        # 设置回调
        def on_tick(elapsed, remaining):
            progress = (elapsed / (duration_minutes * 60)) * 100
            bar = "█" * int(progress / 10) + "░" * (10 - int(progress / 10))
            print(f"\r  [{bar}] {progress:.0f}%", end="", flush=True)
        
        def on_complete():
            print("\n\n  ✨ 冥想完成!")
        
        assistant.timer.set_callbacks(on_tick=on_tick, on_complete=on_complete)
        
        # 开始冥想
        session = assistant.start_meditation(
            breathing_pattern=BreathingPattern.BOX_BREATHING
        )
        
        # 同时启动呼吸指导
        phase_count = [0]
        
        def on_breath(phase, duration, instruction):
            phase_count[0] += 1
        
        assistant.start_breathing_guide(
            BreathingPattern.BOX_BREATHING,
            duration_minutes=duration_minutes,
            callback=on_breath
        )
        
        # 等待完成
        while assistant.timer.is_running():
            time.sleep(0.1)
        
        # 结束呼吸指导
        assistant.stop_breathing_guide()
        
        # 显示统计
        stats = assistant.get_stats()
        print(f"\n冥想统计:")
        print(f"  总会话: {stats.total_sessions}")
        print(f"  总时长: {format_duration(stats.total_minutes * 60)}")
    
    finally:
        os.unlink(temp_file.name)


def example_bell_generation():
    """示例5: 生成冥想铃声"""
    print("\n" + "=" * 60)
    print("示例5: 生成冥想铃声")
    print("=" * 60)
    
    # 生成不同频率的铃声
    frequencies = [
        (432, "治愈频率"),
        (528, "爱的频率"),
        (639, "关系和谐"),
        (741, "觉醒/清理"),
    ]
    
    print("\n生成冥想铃声:")
    for freq, desc in frequencies:
        wav_data = MeditationAssistant.generate_bell_wav(frequency=freq, duration=1.0)
        print(f"  {freq}Hz ({desc}): {len(wav_data)} 字节")
    
    # 保存铃声文件示例
    import tempfile
    import os
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_file.close()
    
    try:
        wav_data = MeditationAssistant.generate_bell_wav(frequency=432.0, duration=2.0)
        with open(temp_file.name, 'wb') as f:
            f.write(wav_data)
        print(f"\n铃声已保存到: {temp_file.name}")
        print(f"文件大小: {os.path.getsize(temp_file.name)} 字节")
    finally:
        os.unlink(temp_file.name)


def example_quick_meditation():
    """示例6: 快速冥想"""
    print("\n" + "=" * 60)
    print("示例6: 快速冥想函数")
    print("=" * 60)
    
    print("\nquick_meditation() 提供简单的阻塞式冥想体验:")
    print("  - 自动计时和进度显示")
    print("  - 支持 Ctrl+C 中断")
    print("  - 返回会话结果")
    
    # 注释掉实际执行，因为这会阻塞
    # result = quick_meditation(minutes=0.1)
    # print(f"结果: {result}")


def example_guided_breathing():
    """示例7: 引导式呼吸函数"""
    print("\n" + "=" * 60)
    print("示例7: 引导式呼吸函数")
    print("=" * 60)
    
    print("\nguided_breathing() 提供阻塞式呼吸指导:")
    print("  - 实时显示呼吸阶段")
    print("  - 支持 Ctrl+C 中断")
    print("  - 返回练习统计")
    
    # 注释掉实际执行
    # result = guided_breathing(BreathingPattern.BOX_BREATHING, cycles=3)
    # print(f"结果: {result}")


def example_breathing_patterns():
    """示例8: 所有呼吸模式详解"""
    print("\n" + "=" * 60)
    print("示例8: 所有呼吸模式详解")
    print("=" * 60)
    
    patterns = [
        (BreathingPattern.RELAXING_4_7_8, "放松/助眠", "吸4秒-屏7秒-呼8秒，有效缓解焦虑"),
        (BreathingPattern.BOX_BREATHING, "专注/平静", "吸4秒-屏4秒-呼4秒-屏4秒，提升专注力"),
        (BreathingPattern.CALMING_4_6, "镇静", "吸4秒-呼6秒，快速平复情绪"),
        (BreathingPattern.ENERGIZING, "激发", "快速吸呼，提升能量"),
        (BreathingPattern.DEEP_RELAXATION, "深度放松", "吸6秒-屏2秒-呼7秒-屏2秒，深度放松"),
        (BreathingPattern.EQUAL_BREATHING, "平衡", "吸5秒-呼5秒，身心平衡"),
    ]
    
    print("\n推荐呼吸模式:\n")
    for pattern, purpose, description in patterns:
        guide = BreathingGuide(pattern)
        cycle_time = guide.cycle.get_total_duration() if guide.cycle else 0
        print(f"  {pattern.value}")
        print(f"    用途: {purpose}")
        print(f"    说明: {description}")
        print(f"    周期: {cycle_time:.0f}秒/循环")
        print()


def main():
    """运行所有示例"""
    print("=" * 60)
    print("🧘 冥想计时器工具 - 使用示例")
    print("=" * 60)
    
    # 运行非阻塞示例
    example_basic_timer()
    example_breathing_guide()
    example_session_recording()
    example_meditation_assistant()
    example_bell_generation()
    example_quick_meditation()
    example_guided_breathing()
    example_breathing_patterns()
    
    print("\n" + "=" * 60)
    print("✨ 所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()