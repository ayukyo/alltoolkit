#!/usr/bin/env python3
"""
MIDI Utilities 基础使用示例

演示：
1. 读取 MIDI 文件并获取信息
2. 提取音符列表
3. 创建简单旋律
4. 生成音阶和和弦
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    read_midi,
    write_midi,
    get_midi_info,
    extract_notes,
    create_simple_melody,
    create_scale,
    create_chord,
    midi_note_to_name,
    name_to_midi_note,
    notes_to_text,
    transpose_notes,
)


def example_create_melody():
    """示例：创建简单旋律"""
    print("\n=== 创建简单旋律 ===")
    
    # 创建《小星星》旋律
    twinkle = [
        ("C4", 0.5), ("C4", 0.5),  # 一闪一闪
        ("G4", 0.5), ("G4", 0.5),  # 亮晶晶
        ("A4", 0.5), ("A4", 0.5),  # 漫天都是
        ("G4", 1.0),               # 小星星
        ("F4", 0.5), ("F4", 0.5),  # 挂在天上
        ("E4", 0.5), ("E4", 0.5),  # 放光明
        ("D4", 0.5), ("D4", 0.5),  # 好像许多
        ("C4", 1.0),               # 小眼睛
    ]
    
    midi = create_simple_melody(twinkle, bpm=120, program=0)
    write_midi(midi, "examples/output/twinkle.mid")
    
    print("✓ 创建 twinkle.mid (小星星)")
    print(f"  轨道数: {len(midi.tracks)}")
    print(f"  BPM: {midi.bpm}")
    
    # 提取音符并显示
    notes = midi.get_all_notes()
    print(f"  音符数: {len(notes)}")


def example_create_scale():
    """示例：创建音阶"""
    print("\n=== 创建音阶 ===")
    
    # 创建 C 大调音阶
    midi = create_scale("major", "C4", bpm=100, velocity=80)
    write_midi(midi, "examples/output/c_major_scale.mid")
    
    notes = midi.get_all_notes()
    note_names = [n.note_name for n in sorted(notes, key=lambda x: x.start_time)]
    
    print("✓ 创建 c_major_scale.mid")
    print(f"  音阶: {', '.join(note_names)}")
    
    # 创建 A 小调音阶
    midi = create_scale("minor", "A3")
    write_midi(midi, "examples/output/a_minor_scale.mid")
    print("✓ 创建 a_minor_scale.mid")


def example_create_chord():
    """示例：创建和弦"""
    print("\n=== 创建和弦 ===")
    
    # 创建大三和弦
    chords = [
        ("C4:major", "C 大三和弦"),
        ("F4:maj7", "F 大七和弦"),
        ("G4:dom7", "G 属七和弦"),
        ("A4:min7", "A 小七和弦"),  # 使用 A4 而不是 Am
    ]
    
    for chord_name, description in chords:
        midi = create_chord(chord_name, duration=1.0, bpm=120)
        filename = chord_name.replace(':', '_').replace('#', 's')
        write_midi(midi, f"examples/output/chord_{filename}.mid")
        
        notes = midi.get_all_notes()
        note_names = sorted(set(n.note_name for n in notes))
        
        print(f"✓ 创建 {description}: {', '.join(note_names)}")


def example_note_conversion():
    """示例：音符转换"""
    print("\n=== 音符转换 ===")
    
    # MIDI 编号转名称
    test_notes = [0, 21, 60, 69, 108, 127]
    print("MIDI 编号 → 名称:")
    for note in test_notes:
        print(f"  {note} → {midi_note_to_name(note)}")
    
    # 名称转 MIDI 编号
    test_names = ["C-1", "A0", "C4", "A4", "C8", "G9"]
    print("\n名称 → MIDI 编号:")
    for name in test_names:
        print(f"  {name} → {name_to_midi_note(name)}")


def example_transpose():
    """示例：移调"""
    print("\n=== 移调示例 ===")
    
    # 创建原旋律
    melody = [("C4", 1.0), ("D4", 1.0), ("E4", 1.0), ("F4", 1.0), ("G4", 2.0)]
    midi = create_simple_melody(melody, bpm=120)
    
    notes = midi.get_all_notes()
    original_names = [n.note_name for n in sorted(notes, key=lambda x: x.start_time)]
    print(f"原旋律: {', '.join(original_names)}")
    
    # 升高 2 个半音
    transposed_up = transpose_notes(notes, 2)
    up_names = [n.note_name for n in sorted(transposed_up, key=lambda x: x.start_time)]
    print(f"升 2 半音: {', '.join(up_names)}")
    
    # 降低 3 个半音
    transposed_down = transpose_notes(notes, -3)
    down_names = [n.note_name for n in sorted(transposed_down, key=lambda x: x.start_time)]
    print(f"降 3 半音: {', '.join(down_names)}")


def example_melody_with_velocity():
    """示例：自定义力度的旋律"""
    print("\n=== 自定义力度旋律 ===")
    
    # 每个音符指定力度
    melody = [
        ("C4", 1.0, 50),   # 弱
        ("D4", 1.0, 80),   # 中
        ("E4", 1.0, 100),  # 强
        ("F4", 1.0, 127),  # 最强
        ("G4", 2.0, 60),   # 中弱
    ]
    
    midi = create_simple_melody(melody, bpm=120)
    write_midi(midi, "examples/output/dynamic_melody.mid")
    
    print("✓ 创建 dynamic_melody.mid (渐强效果)")
    
    notes = midi.get_all_notes()
    for note in sorted(notes, key=lambda x: x.start_time):
        print(f"  {note.note_name}: 力度 {note.velocity}")


def main():
    """运行所有示例"""
    print("=" * 50)
    print("MIDI Utilities 基础使用示例")
    print("=" * 50)
    
    # 创建输出目录
    os.makedirs("examples/output", exist_ok=True)
    
    example_note_conversion()
    example_create_melody()
    example_create_scale()
    example_create_chord()
    example_transpose()
    example_melody_with_velocity()
    
    print("\n" + "=" * 50)
    print("所有示例完成！")
    print("输出文件在 examples/output/ 目录")
    print("=" * 50)


if __name__ == "__main__":
    main()