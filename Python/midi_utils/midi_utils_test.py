#!/usr/bin/env python3
"""
MIDI Utilities 测试套件

测试所有 MIDI 处理功能：
- 文件读写
- 事件解析
- 音符提取
- 旋律生成
- 音阶和和弦
- 时间转换
"""

import os
import sys
import tempfile
import struct
from pathlib import Path

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # 数据类
    MIDIEvent, NoteEvent, MIDITrack, MIDIFile, MIDIInfo,
    # 异常
    MIDIUtilsError, InvalidMIDIFileError, UnsupportedMIDIFormatError,
    # 枚举
    MIDIMessageType, MetaEventType,
    # 读取函数
    parse_midi_file, read_midi, get_midi_info, extract_notes,
    # 写入函数
    write_midi_file, write_midi,
    # 创建函数
    create_midi_event, create_note_on_event, create_note_off_event,
    create_tempo_event, create_track_name_event, create_end_of_track_event,
    create_simple_melody, create_scale, create_chord,
    # 辅助函数
    midi_note_to_name, name_to_midi_note, ticks_to_seconds, seconds_to_ticks,
    get_instrument_name, transpose_notes, notes_to_text,
    # 底层函数
    read_variable_length, write_variable_length,
)


class TestMIDINoteConversion:
    """测试音符编号和名称转换"""
    
    def test_midi_note_to_name(self):
        """测试 MIDI 音符编号转名称"""
        assert midi_note_to_name(60) == "C4"
        assert midi_note_to_name(61) == "C#4"
        assert midi_note_to_name(69) == "A4"  # 标准 A 音
        assert midi_note_to_name(0) == "C-1"
        assert midi_note_to_name(127) == "G9"
        assert midi_note_to_name(21) == "A0"  # 钢琴最低音
        assert midi_note_to_name(108) == "C8"  # 钢琴最高音附近
    
    def test_name_to_midi_note(self):
        """测试音符名称转 MIDI 编号"""
        assert name_to_midi_note("C4") == 60
        assert name_to_midi_note("C#4") == 61
        assert name_to_midi_note("Db4") == 61  # 降 D 等于升 C
        assert name_to_midi_note("A4") == 69
        assert name_to_midi_note("C-1") == 0
        assert name_to_midi_note("G9") == 127
    
    def test_note_conversion_roundtrip(self):
        """测试往返转换"""
        for note in [0, 21, 60, 69, 100, 127]:
            name = midi_note_to_name(note)
            back = name_to_midi_note(name)
            assert back == note, f"Roundtrip failed for note {note}: {name} -> {back}"
    
    def test_invalid_note_names(self):
        """测试无效音符名称"""
        try:
            name_to_midi_note("H4")
            assert False, "Should raise ValueError for H4"
        except ValueError:
            pass
        
        try:
            name_to_midi_note("C")
            assert False, "Should raise ValueError for missing octave"
        except ValueError:
            pass


class TestTimeConversion:
    """测试时间转换函数"""
    
    def test_ticks_to_seconds(self):
        """测试 tick 转秒"""
        # 120 BPM, 480 PPQN
        # 1 beat = 0.5 秒 = 480 ticks
        # 1 tick = 0.5/480 秒
        
        result = ticks_to_seconds(480, 480, 120)
        expected = 0.5  # 1 beat at 120 BPM
        assert abs(result - expected) < 0.001, f"Expected {expected}, got {result}"
        
        result = ticks_to_seconds(960, 480, 120)
        expected = 1.0  # 2 beats
        assert abs(result - expected) < 0.001
        
        result = ticks_to_seconds(480, 960, 60)
        expected = 0.5  # 1 beat at 60 BPM = 1 second, 480/960 = 0.5 beat
        assert abs(result - expected) < 0.001
    
    def test_seconds_to_ticks(self):
        """测试秒转 tick"""
        # 120 BPM, 480 PPQN
        result = seconds_to_ticks(0.5, 480, 120)
        expected = 480
        assert result == expected, f"Expected {expected}, got {result}"
        
        result = seconds_to_ticks(1.0, 480, 120)
        expected = 960
        assert result == expected
    
    def test_time_conversion_roundtrip(self):
        """测试时间转换往返"""
        for ticks in [0, 100, 480, 960, 1920, 10000]:
            seconds = ticks_to_seconds(ticks, 480, 120)
            back = seconds_to_ticks(seconds, 480, 120)
            assert back == ticks, f"Roundtrip failed for {ticks} ticks"


class TestVariableLength:
    """测试可变长度编码"""
    
    def test_write_variable_length(self):
        """测试可变长度编码"""
        assert write_variable_length(0) == b'\x00'
        assert write_variable_length(127) == b'\x7F'
        assert write_variable_length(128) == b'\x81\x00'
        assert write_variable_length(255) == b'\x81\x7F'
        # 32767 = 0x7FFF 需要 3 字节编码: 0x81 0xFF 0x7F
        assert write_variable_length(32767) == b'\x81\xFF\x7F'
        # 0x0FFFFFFF 需要 4 字节编码
        assert write_variable_length(0x0FFFFFFF) == b'\xFF\xFF\xFF\x7F'
    
    def test_read_variable_length(self):
        """测试可变长度解码"""
        def read_val(data):
            val, _ = read_variable_length(data, 0)
            return val
        
        assert read_val(b'\x00') == 0
        assert read_val(b'\x7F') == 127
        assert read_val(b'\x81\x00') == 128
        assert read_val(b'\x81\x7F') == 255
        # 32767 的正确编码是 3 字节
        assert read_val(b'\x81\xFF\x7F') == 32767
        assert read_val(b'\xFF\xFF\xFF\x7F') == 0x0FFFFFFF
    
    def test_variable_length_roundtrip(self):
        """测试可变长度编码往返"""
        for value in [0, 1, 127, 128, 255, 1000, 10000, 100000, 1000000]:
            encoded = write_variable_length(value)
            decoded, _ = read_variable_length(encoded, 0)
            assert decoded == value, f"Roundtrip failed for {value}"


class TestMIDIEventCreation:
    """测试 MIDI 事件创建"""
    
    def test_create_note_on_event(self):
        """测试 NOTE_ON 事件创建"""
        event = create_note_on_event(100, 60, 100, channel=0)
        assert event.delta_time == 100
        assert event.event_type == MIDIMessageType.NOTE_ON
        assert event.channel == 0
        assert event.data == bytes([60, 100])
    
    def test_create_note_off_event(self):
        """测试 NOTE_OFF 事件创建"""
        event = create_note_off_event(200, 60, 0, channel=0)
        assert event.delta_time == 200
        assert event.event_type == MIDIMessageType.NOTE_OFF
        assert event.channel == 0
        assert event.data == bytes([60, 0])
    
    def test_create_tempo_event(self):
        """测试速度事件创建"""
        event = create_tempo_event(0, 120.0)
        assert event.event_type == 0xFF
        assert event.meta_type == MetaEventType.TEMPO
        # 120 BPM = 500000 microseconds per beat
        assert len(event.data) == 3
    
    def test_create_track_name_event(self):
        """测试轨道名称事件创建"""
        event = create_track_name_event(0, "Piano")
        assert event.event_type == 0xFF
        assert event.meta_type == MetaEventType.TRACK_NAME
        assert event.data == b"Piano"


class TestMelodyCreation:
    """测试旋律创建"""
    
    def test_create_simple_melody(self):
        """测试简单旋律创建"""
        notes = [
            ("C4", 1.0),
            ("D4", 1.0),
            ("E4", 1.0),
            ("F4", 1.0),
            ("G4", 2.0),
        ]
        
        midi = create_simple_melody(notes, bpm=120, velocity=100)
        
        assert midi.format_type == 0
        assert len(midi.tracks) == 1
        assert midi.bpm == 120.0
    
    def test_create_melody_with_rest(self):
        """测试包含休止符的旋律"""
        notes = [
            ("C4", 1.0),
            ("R", 1.0),  # 休止符
            ("D4", 1.0),
        ]
        
        midi = create_simple_melody(notes)
        assert len(midi.tracks) == 1
    
    def test_write_and_read_melody(self):
        """测试写入和读取旋律"""
        notes = [
            ("C4", 0.5),
            ("D4", 0.5),
            ("E4", 0.5),
            ("F4", 0.5),
            ("G4", 1.0),
        ]
        
        midi = create_simple_melody(notes, bpm=120)
        
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
            temp_path = f.name
        
        try:
            # 写入
            result = write_midi_file(midi, temp_path)
            assert result is True
            assert os.path.exists(temp_path)
            
            # 读取
            loaded_midi = parse_midi_file(temp_path)
            assert loaded_midi.format_type == 0
            assert len(loaded_midi.tracks) == 1
            
            # 提取音符
            read_notes = loaded_midi.get_all_notes()
            assert len(read_notes) == 5
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestScaleCreation:
    """测试音阶创建"""
    
    def test_create_major_scale(self):
        """测试大调音阶"""
        midi = create_scale("major", "C4")
        notes = midi.get_all_notes()
        
        # 大调音阶有 8 个音符
        assert len(notes) == 8
        
        # 检查音符
        note_names = [n.note_name for n in sorted(notes, key=lambda x: x.start_time)]
        assert note_names == ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
    
    def test_create_minor_scale(self):
        """测试小调音阶"""
        midi = create_scale("minor", "A3")
        notes = midi.get_all_notes()
        
        assert len(notes) == 8
        
        note_names = [n.note_name for n in sorted(notes, key=lambda x: x.start_time)]
        assert note_names[0] == "A3"
    
    def test_create_pentatonic_scale(self):
        """测试五声音阶"""
        midi = create_scale("pentatonic", "C4")
        notes = midi.get_all_notes()
        
        # 五声音阶有 6 个音符
        assert len(notes) == 6
    
    def test_create_chromatic_scale(self):
        """测试半音阶"""
        midi = create_scale("chromatic", "C4")
        notes = midi.get_all_notes()
        
        # 半音阶有 13 个音符
        assert len(notes) == 13


class TestChordCreation:
    """测试和弦创建"""
    
    def test_create_major_chord(self):
        """测试大三和弦"""
        midi = create_chord("C4:major", duration=1.0)
        notes = midi.get_all_notes()
        
        # 大三和弦有 3 个音符
        assert len(notes) == 3
        
        # 检查音符是 C, E, G
        note_names = sorted(set(n.note_name for n in notes))
        assert "C4" in note_names
        assert "E4" in note_names
        assert "G4" in note_names
    
    def test_create_minor_chord(self):
        """测试小三和弦"""
        midi = create_chord("A4:minor")
        notes = midi.get_all_notes()
        
        assert len(notes) == 3
    
    def test_create_seventh_chord(self):
        """测试七和弦"""
        midi = create_chord("C4:maj7")
        notes = midi.get_all_notes()
        
        # 七和弦有 4 个音符
        assert len(notes) == 4
    
    def test_create_diminished_seventh(self):
        """测试减七和弦"""
        midi = create_chord("C4:dim7")
        notes = midi.get_all_notes()
        
        # 减七和弦有 4 个音符
        assert len(notes) == 4


class TestNoteExtraction:
    """测试音符提取"""
    
    def test_extract_notes_from_melody(self):
        """测试从旋律提取音符"""
        notes = [
            ("C4", 1.0),
            ("E4", 1.0),
            ("G4", 1.0),
        ]
        
        midi = create_simple_melody(notes, bpm=120)
        
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
            temp_path = f.name
        
        try:
            write_midi_file(midi, temp_path)
            extracted = extract_notes(temp_path)
            
            assert len(extracted) == 3
            
            # 检查音符名称
            note_names = sorted(set(n.note_name for n in extracted))
            assert "C4" in note_names
            assert "E4" in note_names
            assert "G4" in note_names
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_extract_notes_duration(self):
        """测试音符持续时间"""
        notes = [("C4", 0.5), ("D4", 1.0), ("E4", 2.0)]
        midi = create_simple_melody(notes, bpm=120)
        
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
            temp_path = f.name
        
        try:
            write_midi_file(midi, temp_path)
            extracted = extract_notes(temp_path)
            
            # 按开始时间排序
            extracted.sort(key=lambda n: n.start_time)
            
            # 检查持续时间（0.5 beat at 120 BPM = 0.25s）
            assert abs(extracted[0].duration - 0.25) < 0.01
            assert abs(extracted[1].duration - 0.5) < 0.01
            assert abs(extracted[2].duration - 1.0) < 0.01
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestTranspose:
    """测试移调"""
    
    def test_transpose_up(self):
        """测试向上移调"""
        notes = [
            NoteEvent(note=60, note_name="C4", start_time=0, duration=1.0, velocity=100, channel=0),
        ]
        
        transposed = transpose_notes(notes, 12)  # 升高一个八度
        
        assert len(transposed) == 1
        assert transposed[0].note == 72
        assert transposed[0].note_name == "C5"
    
    def test_transpose_down(self):
        """测试向下移调"""
        notes = [
            NoteEvent(note=60, note_name="C4", start_time=0, duration=1.0, velocity=100, channel=0),
        ]
        
        transposed = transpose_notes(notes, -12)  # 降低一个八度
        
        assert len(transposed) == 1
        assert transposed[0].note == 48
        assert transposed[0].note_name == "C3"
    
    def test_transpose_semitones(self):
        """测试半音移调"""
        notes = [
            NoteEvent(note=60, note_name="C4", start_time=0, duration=1.0, velocity=100, channel=0),
        ]
        
        transposed = transpose_notes(notes, 7)  # 升高 7 个半音（纯五度）
        
        assert transposed[0].note == 67
        assert transposed[0].note_name == "G4"
    
    def test_transpose_out_of_range(self):
        """测试移调超出范围"""
        # 音符 0 无法再降低
        notes = [
            NoteEvent(note=0, note_name="C-1", start_time=0, duration=1.0, velocity=100, channel=0),
        ]
        
        transposed = transpose_notes(notes, -1)
        
        # 应该被过滤掉
        assert len(transposed) == 0


class TestInstrumentNames:
    """测试乐器名称"""
    
    def test_piano_names(self):
        """测试钢琴乐器名称"""
        assert "Piano" in get_instrument_name(0)
        assert "Piano" in get_instrument_name(1)
    
    def test_drum_names(self):
        """测试打击乐器名称"""
        # 打击乐在通道 9
        drum_name = get_instrument_name(36, channel=9)
        assert "Drum" in drum_name or "Bass" in drum_name
    
    def test_unknown_instrument(self):
        """测试未知乐器"""
        name = get_instrument_name(200)  # 超出范围
        assert "Instrument" in name or "200" in name


class TestMIDIFileFormat:
    """测试 MIDI 文件格式"""
    
    def test_file_header(self):
        """测试文件头"""
        midi = create_simple_melody([("C4", 1.0)])
        
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
            temp_path = f.name
        
        try:
            write_midi_file(midi, temp_path)
            
            with open(temp_path, 'rb') as f:
                header = f.read(4)
            
            assert header == b'MThd'
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_track_header(self):
        """测试轨道头"""
        midi = create_simple_melody([("C4", 1.0)])
        
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
            temp_path = f.name
        
        try:
            write_midi_file(midi, temp_path)
            
            with open(temp_path, 'rb') as f:
                data = f.read()
            
            # 应该包含 MTrk
            assert b'MTrk' in data
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestErrorHandling:
    """测试错误处理"""
    
    def test_invalid_file(self):
        """测试无效文件"""
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
            temp_path = f.name
            f.write(b'Not a MIDI file')
        
        try:
            try:
                parse_midi_file(temp_path)
                assert False, "Should raise InvalidMIDIFileError"
            except InvalidMIDIFileError:
                pass
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_nonexistent_file(self):
        """测试不存在的文件"""
        try:
            parse_midi_file("/nonexistent/path/file.mid")
            assert False, "Should raise FileNotFoundError"
        except FileNotFoundError:
            pass
    
    def test_invalid_scale_type(self):
        """测试无效音阶类型"""
        try:
            create_scale("invalid_scale", "C4")
            assert False, "Should raise ValueError"
        except ValueError:
            pass
    
    def test_invalid_chord_type(self):
        """测试无效和弦类型"""
        try:
            create_chord("C4:invalid_chord")
            assert False, "Should raise ValueError"
        except ValueError:
            pass


class TestNotesToText:
    """测试音符转文本"""
    
    def test_notes_to_text_output(self):
        """测试输出格式"""
        notes = [
            NoteEvent(note=60, note_name="C4", start_time=0.0, duration=0.5, velocity=100, channel=0),
            NoteEvent(note=64, note_name="E4", start_time=0.5, duration=0.5, velocity=100, channel=0),
        ]
        
        text = notes_to_text(notes)
        
        assert "C4" in text
        assert "E4" in text
        assert "Note" in text
        assert "Start" in text
        assert "Duration" in text


class TestMIDIInfo:
    """测试 MIDI 信息"""
    
    def test_get_midi_info(self):
        """测试获取 MIDI 信息"""
        midi = create_simple_melody([
            ("C4", 1.0),
            ("D4", 1.0),
            ("E4", 1.0),
        ], bpm=120)
        
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
            temp_path = f.name
        
        try:
            write_midi_file(midi, temp_path)
            info = get_midi_info(temp_path)
            
            assert info.format_type == 0
            assert info.num_tracks == 1
            assert info.bpm == 120.0
            assert info.num_notes == 3
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


def run_tests():
    """运行所有测试"""
    test_classes = [
        TestMIDINoteConversion,
        TestTimeConversion,
        TestVariableLength,
        TestMIDIEventCreation,
        TestMelodyCreation,
        TestScaleCreation,
        TestChordCreation,
        TestNoteExtraction,
        TestTranspose,
        TestInstrumentNames,
        TestMIDIFileFormat,
        TestErrorHandling,
        TestNotesToText,
        TestMIDIInfo,
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("MIDI Utilities Test Suite")
    print("=" * 60)
    
    for test_class in test_classes:
        instance = test_class()
        
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                method = getattr(instance, method_name)
                try:
                    method()
                    print(f"✓ {test_class.__name__}.{method_name}")
                    passed += 1
                except AssertionError as e:
                    print(f"✗ {test_class.__name__}.{method_name}")
                    print(f"  AssertionError: {e}")
                    failed += 1
                except Exception as e:
                    print(f"✗ {test_class.__name__}.{method_name}")
                    print(f"  {type(e).__name__}: {e}")
                    failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)