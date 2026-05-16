"""
节拍器工具模块使用示例

展示 metronome_utils 模块的主要功能，
包括 BPM 计算、节拍生成、练习计划等。

作者: AllToolkit
日期: 2026-05-17
"""

import time
import sys
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from mod import (
    Metronome,
    TimeSignature,
    TempoMarking,
    Subdivision,
    bpm_to_ms,
    bpm_to_seconds,
    get_tempo_marking,
    get_bpm_range_for_tempo,
    calculate_measures,
    calculate_duration,
    adjust_bpm_for_exercise,
    get_subdivision_name,
    calculate_delay_time,
    time_signature_to_string,
    parse_time_signature,
    get_time_signature_info,
    generate_rhythm_pattern,
    suggest_bpm_for_genre,
    create_practice_routine,
    calculate_polymetric_bpm,
    get_metronome_exercise
)


def example_bpm_conversion():
    """示例：BPM 转换"""
    print("=" * 50)
    print("【BPM 转换示例】")
    print("=" * 50)
    
    bpm_values = [40, 60, 90, 120, 150, 200]
    
    print("\nBPM 与毫秒/秒转换:")
    print("-" * 40)
    for bpm in bpm_values:
        ms = bpm_to_ms(bpm)
        sec = bpm_to_seconds(bpm)
        print(f"  {bpm} BPM → {ms:.1f}ms/拍 → {sec:.3f}s/拍")
    
    print("\n速度标记对照:")
    print("-" * 40)
    for bpm in [25, 45, 60, 80, 100, 120, 150, 180, 210]:
        italian, chinese = get_tempo_marking(bpm)
        print(f"  {bpm} BPM → {italian} ({chinese})")


def example_time_signature():
    """示例：拍号处理"""
    print("\n" + "=" * 50)
    print("【拍号处理示例】")
    print("=" * 50)
    
    signatures = ['2/4', '3/4', '4/4', '6/8', '12/8', '5/4', '7/8']
    
    print("\n拍号信息:")
    print("-" * 40)
    for sig in signatures:
        beats, unit = parse_time_signature(sig)
        info = get_time_signature_info(beats, unit)
        
        print(f"  {sig}:")
        print(f"    名称: {info['name']}")
        print(f"    类型: {info['type']}")
        print(f"    强拍位置: {info['downbeats']}")
        print(f"    是否复合拍号: {info['is_compound']}")


def example_duration_calculation():
    """示例：时长计算"""
    print("\n" + "=" * 50)
    print("【时长计算示例】")
    print("=" * 50)
    
    # 计算练习时长
    print("\n练习时长计算:")
    print("-" * 40)
    
    bpm = 120
    measures = 16
    beats_per_measure = 4
    
    duration = calculate_duration(bpm, measures, beats_per_measure)
    print(f"  {bpm} BPM，{measures}小节(4/4拍) → {duration:.1f}秒")
    
    # 反向计算小节数
    duration_seconds = 180  # 3分钟
    measures = calculate_measures(bpm, duration_seconds, beats_per_measure)
    print(f"  {bpm} BPM，{duration_seconds}秒 → {measures:.1f}小节")


def example_rhythm_pattern():
    """示例：节奏模式"""
    print("\n" + "=" * 50)
    print("【节奏模式示例】")
    print("=" * 50)
    
    patterns = {
        '基础四拍': [1, 1, 1, 1],
        '切分节奏': [1, 0, 1, 0],
        '摇摆节奏': [1, 0, 1, 0, 1, 0, 1, 0],
        '三连音': [1, 1, 1]
    }
    
    bpm = 120
    
    print(f"\nBPM: {bpm}")
    print("-" * 40)
    
    for name, pattern in patterns.items():
        result = generate_rhythm_pattern(bpm, pattern, 1)
        times = [r['time_ms'] for r in result]
        
        # 创建可视化
        visual = ' '.join(['●' if p else '○' for p in pattern])
        
        print(f"  {name}: {visual}")
        print(f"    时间点: {[f'{t:.0f}ms' for t in times]}")


def example_genre_bpm():
    """示例：音乐风格 BPM"""
    print("\n" + "=" * 50)
    print("【音乐风格 BPM 推荐】")
    print("=" * 50)
    
    genres = ['ballad', 'rock', 'pop', 'hip_hop', 'jazz', 'house', 'waltz', 'metal']
    
    print("\n各风格 BPM 范围:")
    print("-" * 40)
    
    for genre in genres:
        info = suggest_bpm_for_genre(genre)
        print(f"  {info['genre']}:")
        print(f"    BPM范围: {info['min_bpm']} - {info['max_bpm']}")
        print(f"    推荐BPM: {info['suggested_bpm']}")
        print(f"    速度标记: {info['tempo_marking']}")


def example_practice_routine():
    """示例：练习计划"""
    print("\n" + "=" * 50)
    print("【练习计划示例】")
    print("=" * 50)
    
    # 创建从60到120的练习计划
    target_bpm = 120
    current_bpm = 60
    
    print(f"\n目标: 从 {current_bpm} BPM 提升至 {target_bpm} BPM")
    print("-" * 40)
    
    for difficulty in ['easy', 'medium', 'hard']:
        routine = create_practice_routine(target_bpm, current_bpm, 5, difficulty)
        
        print(f"\n难度: {difficulty}")
        print(f"  步骤: {len(routine)}步")
        
        for step in routine[:5]:  # 只显示前5步
            is_target = ' [目标]' if step['is_target'] else ''
            is_start = ' [起点]' if step['is_start'] else ''
            print(f"    步骤{step['step']}: {step['bpm']} BPM ({step['tempo_marking']}){is_target}{is_start}")


def example_delay_calculation():
    """示例：延迟时间计算"""
    print("\n" + "=" * 50)
    print("【延迟效果器时间计算】")
    print("=" * 50)
    
    bpm = 120
    note_types = ['quarter', 'eighth', 'sixteenth', 'dotted_quarter', 'triplet_eighth']
    
    print(f"\nBPM: {bpm}")
    print("-" * 40)
    
    quarter_delay = calculate_delay_time(bpm, 'quarter')
    print(f"  四分音符基准延迟: {quarter_delay:.0f}ms")
    
    for note_type in note_types:
        delay = calculate_delay_time(bpm, note_type)
        print(f"  {note_type}: {delay:.0f}ms")


def example_metronome_class():
    """示例：节拍器类"""
    print("\n" + "=" * 50)
    print("【节拍器类使用】")
    print("=" * 50)
    
    # 创建节拍器
    metronome = Metronome(
        bpm=100,
        time_signature=TimeSignature.FOUR_FOUR,
        subdivision=Subdivision.QUARTER
    )
    
    print(f"\n节拍器设置:")
    print(f"  BPM: {metronome.bpm}")
    print(f"  拍号: {time_signature_to_string(metronome.beats_per_measure, metronome.beat_unit)}")
    print(f"  每小节拍数: {metronome.beats_per_measure}")
    print(f"  细分: {metronome.subdivision.name}")
    
    print(f"\n时间计算:")
    print(f"  每拍时长: {metronome.get_beat_duration_ms():.0f}ms")
    print(f"  每小节时长: {metronome.get_measure_duration_ms():.0f}ms")
    
    print(f"\n强拍位置: {metronome.get_downbeats()}")
    
    # 生成节拍
    beats = metronome.generate_beats(2)
    print(f"\n生成2小节的节拍:")
    for beat in beats:
        beat_type_str = '强' if beat.is_downbeat else '弱'
        print(f"  拍{beat.position}: {beat_type_str}拍, 时间: {beat.time_ms:.0f}ms")


def example_polymetric():
    """示例：多节奏"""
    print("\n" + "=" * 50)
    print("【多节奏同步计算】")
    print("=" * 50)
    
    # 常见多节奏组合
    combinations = [(60, 90), (90, 120), (100, 150)]
    
    for bpm1, bpm2 in combinations:
        result = calculate_polymetric_bpm(bpm1, bpm2)
        
        print(f"\n{bpm1} BPM vs {bpm2} BPM:")
        print(f"  同步间隔: {result['sync_interval_seconds']:.3f}秒")
        print(f"  各节奏拍数: {result['sync_interval_beats']}")


def example_exercises():
    """示例：练习类型"""
    print("\n" + "=" * 50)
    print("【节拍器练习类型】")
    print("=" * 50)
    
    exercise_types = ['basic', 'subdivision', 'accent', 'polyrhythm', 'mixed']
    
    for exercise_type in exercise_types:
        exercise = get_metronome_exercise(exercise_type)
        
        print(f"\n{exercise['name']}:")
        print(f"  难度: {exercise['difficulty']}")
        print(f"  描述: {exercise['description']}")
        print(f"  推荐BPM范围: {exercise['recommended_bpm_range']}")
        
        print(f"  指导:")
        for instruction in exercise['instructions'][:3]:
            print(f"    - {instruction}")


def example_bpm_progression():
    """示例：BPM 递进"""
    print("\n" + "=" * 50)
    print("【BPM 递进练习】")
    print("=" * 50)
    
    # 不同难度的递进
    for difficulty, step in [('easy', 5), ('medium', 10), ('hard', 15)]:
        progression = adjust_bpm_for_exercise(60, 120, difficulty)
        
        print(f"\n难度 {difficulty} (每次+{step} BPM):")
        print(f"  递进序列: {progression}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("     Metronome Utils - 节拍器工具模块示例")
    print("=" * 60)
    
    example_bpm_conversion()
    example_time_signature()
    example_duration_calculation()
    example_rhythm_pattern()
    example_genre_bpm()
    example_practice_routine()
    example_delay_calculation()
    example_metronome_class()
    example_polymetric()
    example_exercises()
    example_bpm_progression()
    
    print("\n" + "=" * 60)
    print("     示例演示完成")
    print("=" * 60)


if __name__ == '__main__':
    main()