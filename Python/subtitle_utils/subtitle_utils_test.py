"""
Subtitle Utils 单元测试
"""

import unittest
from datetime import timedelta
from mod import (
    SubtitleEntry, SRTParser, VTTParser, ASSParser,
    SubtitleUtils, parse_srt, parse_vtt, parse_ass
)


class TestSubtitleEntry(unittest.TestCase):
    """测试 SubtitleEntry"""
    
    def test_create_entry(self):
        """测试创建字幕条目"""
        entry = SubtitleEntry(
            index=1,
            start=timedelta(seconds=1),
            end=timedelta(seconds=4),
            text="Hello"
        )
        self.assertEqual(entry.index, 1)
        self.assertEqual(entry.duration, timedelta(seconds=3))
        self.assertTrue(entry.is_valid())
    
    def test_invalid_entry(self):
        """测试无效字幕条目"""
        # 结束时间早于开始时间
        entry = SubtitleEntry(
            index=1,
            start=timedelta(seconds=5),
            end=timedelta(seconds=1),
            text="Invalid"
        )
        self.assertFalse(entry.is_valid())
        
        # 空文本
        entry2 = SubtitleEntry(
            index=2,
            start=timedelta(seconds=1),
            end=timedelta(seconds=5),
            text=""
        )
        self.assertFalse(entry2.is_valid())
    
    def test_shift(self):
        """测试时间偏移"""
        entry = SubtitleEntry(
            index=1,
            start=timedelta(seconds=1),
            end=timedelta(seconds=4),
            text="Test"
        )
        shifted = entry.shift(timedelta(seconds=2))
        self.assertEqual(shifted.start, timedelta(seconds=3))
        self.assertEqual(shifted.end, timedelta(seconds=6))


class TestSRTParser(unittest.TestCase):
    """测试 SRT 解析器"""
    
    SRT_CONTENT = """1
00:00:01,000 --> 00:00:04,000
Hello, world!

2
00:00:05,000 --> 00:00:08,000
This is a test.

3
00:00:09,000 --> 00:00:12,500
Multiple lines
are supported!
"""
    
    def test_parse_time(self):
        """测试时间解析"""
        td = SRTParser.parse_time("00:01:23,456")
        self.assertEqual(td, timedelta(hours=0, minutes=1, seconds=23, milliseconds=456))
    
    def test_format_time(self):
        """测试时间格式化"""
        td = timedelta(hours=1, minutes=23, seconds=45, milliseconds=678)
        self.assertEqual(SRTParser.format_time(td), "01:23:45,678")
    
    def test_parse_content(self):
        """测试解析 SRT 内容"""
        entries = SRTParser.parse(self.SRT_CONTENT)
        self.assertEqual(len(entries), 3)
        
        self.assertEqual(entries[0].index, 1)
        self.assertEqual(entries[0].start, timedelta(hours=0, minutes=0, seconds=1, milliseconds=0))
        self.assertEqual(entries[0].end, timedelta(hours=0, minutes=0, seconds=4, milliseconds=0))
        self.assertEqual(entries[0].text, "Hello, world!")
        
        self.assertEqual(entries[2].text, "Multiple lines\nare supported!")
    
    def test_generate(self):
        """测试生成 SRT 内容"""
        entries = [
            SubtitleEntry(1, timedelta(seconds=1), timedelta(seconds=4), "Test"),
            SubtitleEntry(2, timedelta(seconds=5), timedelta(seconds=8), "Another")
        ]
        content = SRTParser.generate(entries)
        
        self.assertIn("00:00:01,000 --> 00:00:04,000", content)
        self.assertIn("Test", content)
        self.assertIn("00:00:05,000 --> 00:00:08,000", content)
        self.assertIn("Another", content)
    
    def test_roundtrip(self):
        """测试解析和生成的往返"""
        entries = SRTParser.parse(self.SRT_CONTENT)
        regenerated = SRTParser.generate(entries)
        reparsed = SRTParser.parse(regenerated)
        
        self.assertEqual(len(entries), len(reparsed))
        for original, reparsed_entry in zip(entries, reparsed):
            self.assertEqual(original.index, reparsed_entry.index)
            self.assertEqual(original.start, reparsed_entry.start)
            self.assertEqual(original.end, reparsed_entry.end)
            self.assertEqual(original.text, reparsed_entry.text)


class TestVTTParser(unittest.TestCase):
    """测试 VTT 解析器"""
    
    VTT_CONTENT = """WEBVTT

NOTE This is a test file

00:00:01.000 --> 00:00:04.000
Hello, world!

00:00:05.000 --> 00:00:08.000
This is a <b>test</b> subtitle.
"""
    
    def test_parse_time(self):
        """测试时间解析"""
        td = VTTParser.parse_time("00:01:23.456")
        self.assertEqual(td, timedelta(minutes=1, seconds=23, milliseconds=456))
        
        # 不带小时的格式
        td2 = VTTParser.parse_time("01:23.456")
        self.assertEqual(td2, timedelta(minutes=1, seconds=23, milliseconds=456))
    
    def test_format_time(self):
        """测试时间格式化"""
        td = timedelta(hours=1, minutes=23, seconds=45, milliseconds=678)
        self.assertEqual(VTTParser.format_time(td), "01:23:45.678")
    
    def test_parse_content(self):
        """测试解析 VTT 内容"""
        entries, metadata = VTTParser.parse(self.VTT_CONTENT)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].text, "Hello, world!")
        # VTT 标签应该被移除
        self.assertIn("test", entries[1].text)
        self.assertNotIn("<b>", entries[1].text)
    
    def test_generate(self):
        """测试生成 VTT 内容"""
        entries = [
            SubtitleEntry(1, timedelta(seconds=1), timedelta(seconds=4), "Test")
        ]
        content = VTTParser.generate(entries, {"Language": "en"})
        
        self.assertIn("WEBVTT", content)
        self.assertIn("Language: en", content)
        self.assertIn("00:00:01.000 --> 00:00:04.000", content)


class TestASSParser(unittest.TestCase):
    """测试 ASS 解析器"""
    
    ASS_CONTENT = """[Script Info]
Title: Test Subtitle
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour
Style: Default,Arial,16,&H00FFFFFF

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:01.00,0:00:04.00,Default,,0,0,0,,Hello, world!
Dialogue: 0,0:00:05.00,0:00:08.00,Default,,0,0,0,,{\\b1}Bold text{\\b0}
"""
    
    def test_parse_time(self):
        """测试时间解析"""
        td = ASSParser.parse_time("0:01:23.45")
        self.assertEqual(td, timedelta(minutes=1, seconds=23, milliseconds=450))
    
    def test_format_time(self):
        """测试时间格式化"""
        td = timedelta(hours=1, minutes=23, seconds=45, milliseconds=670)
        self.assertEqual(ASSParser.format_time(td), "1:23:45.67")
    
    def test_parse_content(self):
        """测试解析 ASS 内容"""
        entries, metadata = ASSParser.parse(self.ASS_CONTENT)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].text, "Hello, world!")
        # ASS 标签应该被移除
        self.assertNotIn("{\\b1}", entries[1].text)
        self.assertIn("Bold text", entries[1].text)
    
    def test_generate(self):
        """测试生成 ASS 内容"""
        entries = [
            SubtitleEntry(1, timedelta(seconds=1), timedelta(seconds=4), "Test")
        ]
        content = ASSParser.generate(entries, title="My Subtitle")
        
        self.assertIn("[Script Info]", content)
        self.assertIn("My Subtitle", content)
        self.assertIn("[Events]", content)


class TestSubtitleUtils(unittest.TestCase):
    """测试 SubtitleUtils 工具集"""
    
    def setUp(self):
        self.entries = [
            SubtitleEntry(1, timedelta(seconds=1), timedelta(seconds=4), "First"),
            SubtitleEntry(2, timedelta(seconds=5), timedelta(seconds=8), "Second"),
            SubtitleEntry(3, timedelta(seconds=10), timedelta(seconds=14), "Third")
        ]
    
    def test_shift_delay(self):
        """测试延迟"""
        shifted = SubtitleUtils.delay(self.entries, 2)
        self.assertEqual(shifted[0].start, timedelta(seconds=3))
        self.assertEqual(shifted[0].end, timedelta(seconds=6))
    
    def test_shift_advance(self):
        """测试提前"""
        shifted = SubtitleUtils.advance(self.entries, 0.5)
        self.assertEqual(shifted[0].start, timedelta(seconds=0.5))
    
    def test_merge(self):
        """测试合并"""
        other = [
            SubtitleEntry(4, timedelta(seconds=2), timedelta(seconds=3), "Middle")
        ]
        merged = SubtitleUtils.merge(self.entries, other)
        self.assertEqual(len(merged), 4)
        # 应该按时间排序
        self.assertEqual(merged[0].text, "First")
        self.assertEqual(merged[1].text, "Middle")
    
    def test_split(self):
        """测试分割"""
        before, after = SubtitleUtils.split(self.entries, timedelta(seconds=6))
        self.assertEqual(len(before), 2)  # 第一条和第二条
        self.assertEqual(len(after), 1)   # 第三条
    
    def test_filter_by_time(self):
        """测试时间过滤"""
        filtered = SubtitleUtils.filter_by_time(
            self.entries,
            start=timedelta(seconds=4),
            end=timedelta(seconds=11)
        )
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0].text, "Second")
        self.assertEqual(filtered[1].text, "Third")
    
    def test_filter_by_text(self):
        """测试文本过滤"""
        filtered = SubtitleUtils.filter_by_text(self.entries, "First|Third")
        self.assertEqual(len(filtered), 2)
    
    def test_reindex(self):
        """测试重新编号"""
        entries = [
            SubtitleEntry(100, timedelta(seconds=1), timedelta(seconds=4), "Test")
        ]
        reindexed = SubtitleUtils.reindex(entries, start=1)
        self.assertEqual(reindexed[0].index, 1)
    
    def test_deduplicate(self):
        """测试去重"""
        entries = [
            SubtitleEntry(1, timedelta(seconds=1), timedelta(seconds=4), "Same"),
            SubtitleEntry(2, timedelta(seconds=3), timedelta(seconds=6), "Same"),
            SubtitleEntry(3, timedelta(seconds=10), timedelta(seconds=12), "Different")
        ]
        deduped = SubtitleUtils.deduplicate(entries)
        self.assertEqual(len(deduped), 2)
    
    def test_get_statistics(self):
        """测试统计信息"""
        stats = SubtitleUtils.get_statistics(self.entries)
        self.assertEqual(stats['count'], 3)
        self.assertEqual(stats['total_chars'], 16)  # First (5) + Second (6) + Third (5)
        self.assertEqual(stats['longest'].text, "Third")  # 4秒最长
    
    def test_validate(self):
        """测试验证"""
        # 正常情况
        errors = SubtitleUtils.validate(self.entries)
        self.assertEqual(len(errors), 0)
        
        # 有问题的情况
        bad_entries = [
            SubtitleEntry(1, timedelta(seconds=5), timedelta(seconds=1), "Bad time")
        ]
        errors = SubtitleUtils.validate(bad_entries)
        self.assertGreater(len(errors), 0)


class TestAutoDetectFormat(unittest.TestCase):
    """测试自动格式检测"""
    
    def test_detect_srt(self):
        """测试检测 SRT 格式"""
        srt = "1\n00:00:01,000 --> 00:00:04,000\nTest\n"
        entries, fmt, _ = SubtitleUtils.parse(srt)
        self.assertEqual(fmt, 'srt')
    
    def test_detect_vtt(self):
        """测试检测 VTT 格式"""
        vtt = "WEBVTT\n\n00:00:01.000 --> 00:00:04.000\nTest\n"
        entries, fmt, _ = SubtitleUtils.parse(vtt)
        self.assertEqual(fmt, 'vtt')
    
    def test_detect_ass(self):
        """测试检测 ASS 格式"""
        ass = "[Script Info]\nTitle: Test\n\n[Events]\n"
        entries, fmt, _ = SubtitleUtils.parse(ass)
        self.assertEqual(fmt, 'ass')


class TestConvert(unittest.TestCase):
    """测试格式转换"""
    
    def test_srt_to_vtt(self):
        """测试 SRT 转 VTT"""
        srt_content = """1
00:00:01,000 --> 00:00:04,000
Hello

"""
        entries = parse_srt(srt_content)
        vtt_content = SubtitleUtils.convert(entries, 'srt', 'vtt')
        
        self.assertIn("WEBVTT", vtt_content)
        self.assertIn("00:00:01.000 --> 00:00:04.000", vtt_content)  # VTT 用 . 不是 ,
    
    def test_srt_to_ass(self):
        """测试 SRT 转 ASS"""
        srt_content = """1
00:00:01,000 --> 00:00:04,000
Hello

"""
        entries = parse_srt(srt_content)
        ass_content = SubtitleUtils.convert(entries, 'srt', 'ass')
        
        self.assertIn("[Script Info]", ass_content)
        self.assertIn("[Events]", ass_content)


if __name__ == '__main__':
    unittest.main()