"""
Subtitle Utils 使用示例

演示:
- 解析 SRT/VTT/ASS 字幕
- 时间轴调整
- 格式转换
- 字幕合并与分割
- 统计与验证
"""

from datetime import timedelta
import sys
sys.path.insert(0, '..')
from mod import (
    SubtitleEntry, SRTParser, VTTParser, ASSParser,
    SubtitleUtils, parse_srt, parse_vtt, parse_ass,
    load, save
)


def example_parse_srt():
    """示例：解析 SRT 字幕"""
    print("=" * 50)
    print("1. 解析 SRT 字幕")
    print("=" * 50)
    
    srt_content = """1
00:00:01,000 --> 00:00:04,000
Hello, world!

2
00:00:05,000 --> 00:00:08,000
This is a subtitle example.

3
00:00:09,000 --> 00:00:12,500
字幕支持多行显示
每一行都会被保留
"""
    
    entries = parse_srt(srt_content)
    
    print(f"\n解析到 {len(entries)} 条字幕:\n")
    for entry in entries:
        print(f"  [{entry.index:2d}] {entry.start} --> {entry.end}")
        print(f"       {entry.text.replace(chr(10), ' | ')}")
        print()


def example_parse_vtt():
    """示例：解析 VTT 字幕"""
    print("=" * 50)
    print("2. 解析 WebVTT 字幕")
    print("=" * 50)
    
    vtt_content = """WEBVTT

NOTE This is a comment

STYLE
::cue {
  color: white;
}

00:00:01.000 --> 00:00:04.000 position:50%
Hello from <b>WebVTT</b>!

00:00:05.000 --> 00:00:08.000
This format supports <i>styling</i>.
"""
    
    entries, metadata = parse_vtt(vtt_content)
    
    print(f"\n解析到 {len(entries)} 条字幕")
    print(f"元数据: {metadata if metadata else '无'}\n")
    
    for entry in entries:
        print(f"  [{entry.index}] {entry.text}")


def example_parse_ass():
    """示例：解析 ASS 字幕"""
    print("=" * 50)
    print("3. 解析 ASS 字幕")
    print("=" * 50)
    
    ass_content = """[Script Info]
Title: Example Subtitle
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour
Style: Default,Arial,16,&H00FFFFFF
Style: Title,Arial,24,&H0000FFFF

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:01.00,0:00:04.00,Default,,0,0,0,,Hello from ASS!
Dialogue: 0,0:00:05.00,0:00:08.00,Title,,0,0,0,,{\\b1}Bold Title{\\b0}
Dialogue: 0,0:00:09.00,0:00:12.00,Default,,0,0,0,,Line 1\\NLine 2
"""
    
    entries, metadata = parse_ass(ass_content)
    
    print(f"\n解析到 {len(entries)} 条字幕")
    print(f"脚本信息: {metadata.get('info', {})}")
    print(f"样式数量: {len(metadata.get('styles', {}))}\n")
    
    for entry in entries:
        print(f"  [{entry.index}] {entry.text.replace(chr(10), ' | ')}")


def example_time_shift():
    """示例：时间轴调整"""
    print("=" * 50)
    print("4. 时间轴调整")
    print("=" * 50)
    
    srt_content = """1
00:00:01,000 --> 00:00:04,000
Original timing

2
00:00:05,000 --> 00:00:08,000
Second subtitle
"""
    
    entries = parse_srt(srt_content)
    
    print("\n原始时间:")
    for e in entries:
        print(f"  [{e.index}] {e.start} --> {e.end}")
    
    # 延迟 2.5 秒
    delayed = SubtitleUtils.delay(entries, 2.5)
    print("\n延迟 2.5 秒后:")
    for e in delayed:
        print(f"  [{e.index}] {e.start} --> {e.end}")
    
    # 提前 0.5 秒
    advanced = SubtitleUtils.advance(entries, 0.5)
    print("\n提前 0.5 秒后:")
    for e in advanced:
        print(f"  [{e.index}] {e.start} --> {e.end}")


def example_format_conversion():
    """示例：格式转换"""
    print("=" * 50)
    print("5. 格式转换")
    print("=" * 50)
    
    srt_content = """1
00:00:01,000 --> 00:00:04,000
Hello, world!

2
00:00:05,000 --> 00:00:08,000
格式转换演示
"""
    
    entries = parse_srt(srt_content)
    
    # 转换为 VTT
    vtt_content = SubtitleUtils.convert(entries, 'srt', 'vtt', {'Language': 'zh'})
    print("\n转换为 WebVTT:")
    print("-" * 40)
    print(vtt_content)
    
    # 转换为 ASS (需要通过 metadata 传递 title)
    ass_metadata = {'title': 'Converted Subtitle'}
    ass_content = SubtitleUtils.convert(entries, 'srt', 'ass', metadata=ass_metadata)
    print("\n转换为 ASS:")
    print("-" * 40)
    print(ass_content[:500] + "...")


def example_merge_split():
    """示例：合并与分割"""
    print("=" * 50)
    print("6. 合并与分割")
    print("=" * 50)
    
    # 创建两组字幕
    group1 = [
        SubtitleEntry(1, timedelta(seconds=1), timedelta(seconds=3), "Part 1 - First"),
        SubtitleEntry(2, timedelta(seconds=4), timedelta(seconds=6), "Part 1 - Second")
    ]
    
    group2 = [
        SubtitleEntry(1, timedelta(seconds=2), timedelta(seconds=4), "Part 2 - First"),
        SubtitleEntry(2, timedelta(seconds=7), timedelta(seconds=9), "Part 2 - Second")
    ]
    
    # 合并
    merged = SubtitleUtils.merge(group1, group2)
    print("\n合并后的字幕 (按时间排序):")
    for e in merged:
        print(f"  [{e.index}] {e.start.total_seconds():.0f}s - {e.text}")
    
    # 分割
    before, after = SubtitleUtils.split(merged, timedelta(seconds=5))
    print(f"\n在 5 秒处分割:")
    print(f"  前半部分 ({len(before)} 条):")
    for e in before:
        print(f"    {e.text}")
    print(f"  后半部分 ({len(after)} 条):")
    for e in after:
        print(f"    {e.text}")


def example_filter():
    """示例：过滤"""
    print("=" * 50)
    print("7. 过滤字幕")
    print("=" * 50)
    
    srt_content = """1
00:00:01,000 --> 00:00:04,000
Introduction

2
00:00:05,000 --> 00:00:08,000
Hello everyone

3
00:00:10,000 --> 00:00:14,000
Important announcement

4
00:00:15,000 --> 00:00:18,000
Thank you for watching
"""
    
    entries = parse_srt(srt_content)
    
    # 按时间过滤
    time_filtered = SubtitleUtils.filter_by_time(
        entries,
        start=timedelta(seconds=5),
        end=timedelta(seconds=16)
    )
    print(f"\n时间范围 5-16 秒的字幕 ({len(time_filtered)} 条):")
    for e in time_filtered:
        print(f"  [{e.index}] {e.text}")
    
    # 按文本过滤
    text_filtered = SubtitleUtils.filter_by_text(entries, r"hello|thank")
    print(f"\n包含 'hello' 或 'thank' 的字幕 ({len(text_filtered)} 条):")
    for e in text_filtered:
        print(f"  [{e.index}] {e.text}")


def example_statistics():
    """示例：统计信息"""
    print("=" * 50)
    print("8. 统计信息")
    print("=" * 50)
    
    srt_content = """1
00:00:01,000 --> 00:00:04,000
这是一段测试字幕

2
00:00:05,000 --> 00:00:08,000
The quick brown fox

3
00:00:10,000 --> 00:00:15,000
This is a longer subtitle that spans more time

4
00:00:16,000 --> 00:00:18,000
End
"""
    
    entries = parse_srt(srt_content)
    stats = SubtitleUtils.get_statistics(entries)
    
    print(f"\n字幕统计:")
    print(f"  总条目数: {stats['count']}")
    print(f"  总时长: {stats['total_duration']}")
    print(f"  平均时长: {stats['avg_duration']}")
    print(f"  总字符数: {stats['total_chars']}")
    print(f"  平均字符数: {stats['avg_chars']:.1f}")
    print(f"  最长字幕: [{stats['longest'].index}] '{stats['longest'].text[:30]}...'")
    print(f"  最短字幕: [{stats['shortest'].index}] '{stats['shortest'].text}'")


def example_validation():
    """示例：验证"""
    print("=" * 50)
    print("9. 字幕验证")
    print("=" * 50)
    
    # 正常字幕
    good_entries = [
        SubtitleEntry(1, timedelta(seconds=1), timedelta(seconds=4), "Good"),
        SubtitleEntry(2, timedelta(seconds=5), timedelta(seconds=8), "Also good")
    ]
    
    errors = SubtitleUtils.validate(good_entries)
    print(f"\n正常字幕验证: {len(errors)} 个错误")
    
    # 有问题的字幕
    bad_entries = [
        SubtitleEntry(1, timedelta(seconds=5), timedelta(seconds=1), "Bad: end before start"),
        SubtitleEntry(2, timedelta(seconds=1), timedelta(seconds=4), ""),
        SubtitleEntry(3, timedelta(seconds=2), timedelta(seconds=5), "Overlaps with #2")
    ]
    
    errors = SubtitleUtils.validate(bad_entries)
    print(f"\n问题字幕验证: {len(errors)} 个错误:")
    for err in errors:
        print(f"  - {err}")


def example_deduplicate():
    """示例：去重"""
    print("=" * 50)
    print("10. 去重")
    print("=" * 50)
    
    entries = [
        SubtitleEntry(1, timedelta(seconds=1), timedelta(seconds=4), "Same text"),
        SubtitleEntry(2, timedelta(seconds=3), timedelta(seconds=6), "Same text"),  # 重叠+同文
        SubtitleEntry(3, timedelta(seconds=10), timedelta(seconds=14), "Different text")
    ]
    
    print(f"\n原始字幕 ({len(entries)} 条):")
    for e in entries:
        print(f"  [{e.index}] {e.start.total_seconds():.0f}s-{e.end.total_seconds():.0f}s: {e.text}")
    
    deduped = SubtitleUtils.deduplicate(entries)
    print(f"\n去重后 ({len(deduped)} 条):")
    for e in deduped:
        print(f"  [{e.index}] {e.start.total_seconds():.0f}s-{e.end.total_seconds():.0f}s: {e.text}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 50)
    print("Subtitle Utils 使用示例")
    print("=" * 50)
    
    example_parse_srt()
    example_parse_vtt()
    example_parse_ass()
    example_time_shift()
    example_format_conversion()
    example_merge_split()
    example_filter()
    example_statistics()
    example_validation()
    example_deduplicate()
    
    print("\n" + "=" * 50)
    print("所有示例完成！")
    print("=" * 50)


if __name__ == '__main__':
    main()