#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - SRT Utilities Test Suite
=====================================
Comprehensive tests for the SRT subtitle utilities module.
"""

import unittest
import sys
import os
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from srt_utils.mod import (
    Subtitle, ValidationResult,
    srt_time_to_milliseconds, milliseconds_to_srt_time,
    vtt_time_to_milliseconds, milliseconds_to_vtt_time,
    format_duration,
    parse_srt, parse_srt_file, parse_vtt, parse_vtt_file,
    generate_srt, generate_vtt,
    write_srt_file, write_vtt_file,
    shift_subtitles, scale_subtitles,
    merge_overlapping_subtitles, split_long_subtitles,
    remove_empty_subtitles, filter_by_time_range,
    find_subtitle_at_time,
    validate_subtitles, validate_srt_content,
    get_statistics,
    srt_to_vtt, vtt_to_srt,
    create_subtitle, concatenate_subtitles,
)


class TestTimeConversion(unittest.TestCase):
    """Test time conversion functions."""
    
    def test_srt_time_to_milliseconds(self):
        """Test SRT time string to milliseconds conversion."""
        self.assertEqual(srt_time_to_milliseconds("00:00:00,000"), 0)
        self.assertEqual(srt_time_to_milliseconds("00:00:01,000"), 1000)
        self.assertEqual(srt_time_to_milliseconds("00:01:00,000"), 60000)
        self.assertEqual(srt_time_to_milliseconds("01:00:00,000"), 3600000)
        self.assertEqual(srt_time_to_milliseconds("00:00:01,500"), 1500)
        self.assertEqual(srt_time_to_milliseconds("01:02:03,456"), 3723456)
        self.assertEqual(srt_time_to_milliseconds("99:59:59,999"), 359999999)
        
    def test_srt_time_to_milliseconds_invalid(self):
        """Test invalid SRT time format raises error."""
        with self.assertRaises(ValueError):
            srt_time_to_milliseconds("invalid")
        with self.assertRaises(ValueError):
            srt_time_to_milliseconds("00:00:00")
        # Note: Dot format (00:00:00.000) is actually common in some SRT files
        # Our strict parser only accepts comma format
    
    def test_milliseconds_to_srt_time(self):
        """Test milliseconds to SRT time string conversion."""
        self.assertEqual(milliseconds_to_srt_time(0), "00:00:00,000")
        self.assertEqual(milliseconds_to_srt_time(1000), "00:00:01,000")
        self.assertEqual(milliseconds_to_srt_time(60000), "00:01:00,000")
        self.assertEqual(milliseconds_to_srt_time(3600000), "01:00:00,000")
        self.assertEqual(milliseconds_to_srt_time(1500), "00:00:01,500")
        self.assertEqual(milliseconds_to_srt_time(3723456), "01:02:03,456")
        
    def test_milliseconds_to_srt_time_negative(self):
        """Test negative milliseconds is clamped to zero."""
        self.assertEqual(milliseconds_to_srt_time(-1000), "00:00:00,000")
        
    def test_srt_time_roundtrip(self):
        """Test SRT time conversion roundtrip."""
        test_cases = [
            "00:00:00,000",
            "00:00:01,500",
            "00:01:30,750",
            "01:23:45,678",
            "99:59:59,999",
        ]
        for time_str in test_cases:
            with self.subTest(time_str=time_str):
                ms = srt_time_to_milliseconds(time_str)
                result = milliseconds_to_srt_time(ms)
                self.assertEqual(result, time_str)
    
    def test_vtt_time_to_milliseconds(self):
        """Test VTT time string to milliseconds conversion."""
        self.assertEqual(vtt_time_to_milliseconds("00:00:00.000"), 0)
        self.assertEqual(vtt_time_to_milliseconds("00:00:01.000"), 1000)
        self.assertEqual(vtt_time_to_milliseconds("00:01:00.000"), 60000)
        self.assertEqual(vtt_time_to_milliseconds("01:00:00.000"), 3600000)
        self.assertEqual(vtt_time_to_milliseconds("01:30.500"), 90500)  # MM:SS.mmm format
        self.assertEqual(vtt_time_to_milliseconds("01:02:03.456"), 3723456)
        
    def test_milliseconds_to_vtt_time(self):
        """Test milliseconds to VTT time string conversion."""
        self.assertEqual(milliseconds_to_vtt_time(0), "00:00:00.000")
        self.assertEqual(milliseconds_to_vtt_time(1000), "00:00:01.000")
        self.assertEqual(milliseconds_to_vtt_time(60000), "00:01:00.000")
        self.assertEqual(milliseconds_to_vtt_time(3600000), "01:00:00.000")
        
    def test_format_duration(self):
        """Test duration formatting."""
        self.assertEqual(format_duration(1000, 'srt'), "00:00:01,000")
        self.assertEqual(format_duration(90000, 'compact'), "1m30s")
        self.assertEqual(format_duration(90000, 'readable'), "1 minute 30 seconds")
        self.assertEqual(format_duration(3661000, 'readable'), "1 hour 1 minute 1 second")


class TestSubtitle(unittest.TestCase):
    """Test Subtitle data class."""
    
    def test_subtitle_creation(self):
        """Test creating a subtitle."""
        sub = Subtitle(1, 1000, 3000, "Hello world")
        self.assertEqual(sub.index, 1)
        self.assertEqual(sub.start_time, 1000)
        self.assertEqual(sub.end_time, 3000)
        self.assertEqual(sub.text, "Hello world")
        self.assertEqual(sub.duration, 2000)
        
    def test_subtitle_to_srt(self):
        """Test converting subtitle to SRT format."""
        sub = Subtitle(1, 1000, 3000, "Hello world")
        result = sub.to_srt()
        expected = "1\n00:00:01,000 --> 00:00:03,000\nHello world"
        self.assertEqual(result, expected)
        
    def test_subtitle_to_vtt(self):
        """Test converting subtitle to VTT format."""
        sub = Subtitle(1, 1000, 3000, "Hello world")
        result = sub.to_vtt()
        expected = "00:00:01.000 --> 00:00:03.000\nHello world"
        self.assertEqual(result, expected)
        
    def test_subtitle_shift(self):
        """Test shifting subtitle timing."""
        sub = Subtitle(1, 1000, 3000, "Test")
        shifted = sub.shift(5000)
        self.assertEqual(shifted.start_time, 6000)
        self.assertEqual(shifted.end_time, 8000)
        self.assertEqual(shifted.text, "Test")
        
    def test_subtitle_shift_negative(self):
        """Test shifting subtitle timing with negative offset."""
        sub = Subtitle(1, 1000, 3000, "Test")
        shifted = sub.shift(-500)
        self.assertEqual(shifted.start_time, 500)
        self.assertEqual(shifted.end_time, 2500)
        
    def test_subtitle_shift_clamped(self):
        """Test shifting doesn't result in negative times."""
        sub = Subtitle(1, 1000, 3000, "Test")
        shifted = sub.shift(-2000)
        self.assertEqual(shifted.start_time, 0)
        self.assertEqual(shifted.end_time, 1000)
        
    def test_subtitle_scale(self):
        """Test scaling subtitle timing."""
        sub = Subtitle(1, 1000, 5000, "Test")
        scaled = sub.scale(0.9)  # 10% faster
        self.assertEqual(scaled.start_time, 900)
        self.assertEqual(scaled.end_time, 4500)
        
    def test_subtitle_overlaps(self):
        """Test subtitle overlap detection."""
        sub1 = Subtitle(1, 1000, 3000, "First")
        sub2 = Subtitle(2, 2000, 4000, "Second")
        sub3 = Subtitle(3, 4000, 6000, "Third")
        
        self.assertTrue(sub1.overlaps(sub2))
        self.assertFalse(sub1.overlaps(sub3))
        self.assertTrue(sub2.overlaps(sub1))
        
    def test_subtitle_contains(self):
        """Test time point containment."""
        sub = Subtitle(1, 1000, 3000, "Test")
        
        self.assertTrue(sub.contains(1000))
        self.assertTrue(sub.contains(2000))
        self.assertTrue(sub.contains(3000))
        self.assertFalse(sub.contains(500))
        self.assertFalse(sub.contains(4000))
        
    def test_subtitle_merge_with(self):
        """Test merging two subtitles."""
        sub1 = Subtitle(1, 1000, 3000, "Hello")
        sub2 = Subtitle(2, 2000, 5000, "World")
        
        merged = sub1.merge_with(sub2, " ")
        
        self.assertEqual(merged.start_time, 1000)
        self.assertEqual(merged.end_time, 5000)
        self.assertEqual(merged.text, "Hello World")
        
    def test_subtitle_split_at(self):
        """Test splitting subtitle at a time point."""
        sub = Subtitle(1, 1000, 5000, "Hello world")
        
        part1, part2 = sub.split_at(3000, 1)
        
        self.assertEqual(part1.start_time, 1000)
        self.assertEqual(part1.end_time, 3000)
        self.assertEqual(part2.start_time, 3000)
        self.assertEqual(part2.end_time, 5000)
        
    def test_subtitle_split_at_invalid(self):
        """Test splitting at invalid time raises error."""
        sub = Subtitle(1, 1000, 5000, "Test")
        
        with self.assertRaises(ValueError):
            sub.split_at(500)  # Before start
            
        with self.assertRaises(ValueError):
            sub.split_at(6000)  # After end


class TestParseSRT(unittest.TestCase):
    """Test SRT parsing functions."""
    
    def test_parse_simple_srt(self):
        """Test parsing a simple SRT string."""
        srt_content = """1
00:00:01,000 --> 00:00:03,000
Hello world!

2
00:00:04,000 --> 00:00:06,000
Second subtitle"""
        
        subs = parse_srt(srt_content)
        
        self.assertEqual(len(subs), 2)
        self.assertEqual(subs[0].index, 1)
        self.assertEqual(subs[0].start_time, 1000)
        self.assertEqual(subs[0].end_time, 3000)
        self.assertEqual(subs[0].text, "Hello world!")
        self.assertEqual(subs[1].index, 2)
        
    def test_parse_multiline_text(self):
        """Test parsing subtitles with multiple lines."""
        srt_content = """1
00:00:01,000 --> 00:00:03,000
First line
Second line"""
        
        subs = parse_srt(srt_content)
        
        self.assertEqual(len(subs), 1)
        self.assertIn("First line", subs[0].text)
        self.assertIn("Second line", subs[0].text)
        
    def test_parse_with_bom(self):
        """Test parsing SRT with BOM."""
        srt_content = "\ufeff1\n00:00:01,000 --> 00:00:03,000\nTest"
        
        subs = parse_srt(srt_content)
        
        self.assertEqual(len(subs), 1)
        
    def test_parse_empty_content(self):
        """Test parsing empty content."""
        subs = parse_srt("")
        self.assertEqual(len(subs), 0)
        
    def test_parse_srt_file(self):
        """Test parsing SRT file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', 
                                          encoding='utf-8', delete=False) as f:
            f.write("1\n00:00:01,000 --> 00:00:03,000\nTest subtitle")
            temp_path = f.name
        
        try:
            subs = parse_srt_file(temp_path)
            self.assertEqual(len(subs), 1)
            self.assertEqual(subs[0].text, "Test subtitle")
        finally:
            os.unlink(temp_path)


class TestParseVTT(unittest.TestCase):
    """Test WebVTT parsing functions."""
    
    def test_parse_simple_vtt(self):
        """Test parsing a simple VTT string."""
        vtt_content = """WEBVTT

00:00:01.000 --> 00:00:03.000
Hello world!

00:00:04.000 --> 00:00:06.000
Second subtitle"""
        
        subs = parse_vtt(vtt_content)
        
        self.assertEqual(len(subs), 2)
        self.assertEqual(subs[0].start_time, 1000)
        self.assertEqual(subs[0].end_time, 3000)
        self.assertEqual(subs[0].text, "Hello world!")
        
    def test_parse_vtt_with_indices(self):
        """Test parsing VTT with subtitle indices."""
        vtt_content = """WEBVTT

1
00:00:01.000 --> 00:00:03.000
First

2
00:00:04.000 --> 00:00:06.000
Second"""
        
        subs = parse_vtt(vtt_content)
        
        self.assertEqual(len(subs), 2)
        
    def test_parse_vtt_short_time_format(self):
        """Test parsing VTT with MM:SS.mmm format."""
        vtt_content = """WEBVTT

00:01.000 --> 00:03.000
Short format time"""
        
        subs = parse_vtt(vtt_content)
        
        self.assertEqual(len(subs), 1)
        self.assertEqual(subs[0].start_time, 1000)
        self.assertEqual(subs[0].end_time, 3000)


class TestGenerateSRT(unittest.TestCase):
    """Test SRT generation functions."""
    
    def test_generate_simple_srt(self):
        """Test generating simple SRT content."""
        subs = [
            Subtitle(1, 1000, 3000, "Hello"),
            Subtitle(2, 4000, 6000, "World"),
        ]
        
        result = generate_srt(subs)
        
        self.assertIn("1\n00:00:01,000 --> 00:00:03,000\nHello", result)
        self.assertIn("2\n00:00:04,000 --> 00:00:06,000\nWorld", result)
        
    def test_generate_empty_subtitles(self):
        """Test generating SRT from empty list."""
        result = generate_srt([])
        self.assertEqual(result, "")
        
    def test_generate_reindexes(self):
        """Test that generation reindexes subtitles."""
        subs = [
            Subtitle(5, 1000, 3000, "First"),
            Subtitle(3, 4000, 6000, "Second"),
        ]
        
        result = generate_srt(subs, reindex=True)
        
        self.assertIn("1\n", result)
        self.assertIn("2\n", result)
        
    def test_generate_no_reindex(self):
        """Test generation without reindexing."""
        subs = [
            Subtitle(5, 1000, 3000, "First"),
        ]
        
        result = generate_srt(subs, reindex=False)
        
        self.assertIn("5\n", result)
        
    def test_generate_sorts_by_time(self):
        """Test that generation sorts by start time."""
        subs = [
            Subtitle(2, 5000, 7000, "Second"),
            Subtitle(1, 1000, 3000, "First"),
        ]
        
        result = generate_srt(subs)
        
        # First subtitle should appear before second
        first_idx = result.find("First")
        second_idx = result.find("Second")
        self.assertLess(first_idx, second_idx)


class TestGenerateVTT(unittest.TestCase):
    """Test VTT generation functions."""
    
    def test_generate_simple_vtt(self):
        """Test generating simple VTT content."""
        subs = [
            Subtitle(1, 1000, 3000, "Hello"),
        ]
        
        result = generate_vtt(subs)
        
        self.assertTrue(result.startswith("WEBVTT"))
        self.assertIn("00:00:01.000 --> 00:00:03.000", result)
        self.assertIn("Hello", result)
        
    def test_generate_vtt_with_header(self):
        """Test generating VTT with custom header."""
        subs = [Subtitle(1, 1000, 3000, "Test")]
        
        result = generate_vtt(subs, header="This is a test")
        
        self.assertIn("WEBVTT", result)
        self.assertIn("This is a test", result)


class TestWriteFiles(unittest.TestCase):
    """Test file writing functions."""
    
    def test_write_srt_file(self):
        """Test writing SRT file."""
        subs = [
            Subtitle(1, 1000, 3000, "Test subtitle"),
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', 
                                          delete=False) as f:
            temp_path = f.name
        
        try:
            write_srt_file(subs, temp_path)
            
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertIn("Test subtitle", content)
            self.assertIn("00:00:01,000 --> 00:00:03,000", content)
        finally:
            os.unlink(temp_path)
            
    def test_write_vtt_file(self):
        """Test writing VTT file."""
        subs = [
            Subtitle(1, 1000, 3000, "Test subtitle"),
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vtt', 
                                          delete=False) as f:
            temp_path = f.name
        
        try:
            write_vtt_file(subs, temp_path)
            
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertIn("WEBVTT", content)
            self.assertIn("00:00:01.000 --> 00:00:03.000", content)
        finally:
            os.unlink(temp_path)


class TestShiftSubtitles(unittest.TestCase):
    """Test subtitle shifting functions."""
    
    def test_shift_subtitles_positive(self):
        """Test positive shift."""
        subs = [
            Subtitle(1, 1000, 3000, "A"),
            Subtitle(2, 4000, 6000, "B"),
        ]
        
        shifted = shift_subtitles(subs, 5000)
        
        self.assertEqual(shifted[0].start_time, 6000)
        self.assertEqual(shifted[0].end_time, 8000)
        self.assertEqual(shifted[1].start_time, 9000)
        self.assertEqual(shifted[1].end_time, 11000)
        
    def test_shift_subtitles_negative(self):
        """Test negative shift."""
        subs = [
            Subtitle(1, 10000, 12000, "A"),
        ]
        
        shifted = shift_subtitles(subs, -5000)
        
        self.assertEqual(shifted[0].start_time, 5000)
        self.assertEqual(shifted[0].end_time, 7000)


class TestScaleSubtitles(unittest.TestCase):
    """Test subtitle scaling functions."""
    
    def test_scale_subtitles(self):
        """Test scaling subtitles."""
        subs = [
            Subtitle(1, 0, 10000, "A"),  # 0-10s
            Subtitle(2, 10000, 20000, "B"),  # 10-20s
        ]
        
        scaled = scale_subtitles(subs, 0.9)  # 10% faster
        
        self.assertEqual(scaled[0].start_time, 0)
        self.assertEqual(scaled[0].end_time, 9000)
        self.assertEqual(scaled[1].start_time, 9000)
        self.assertEqual(scaled[1].end_time, 18000)


class TestMergeOverlapping(unittest.TestCase):
    """Test subtitle merging functions."""
    
    def test_merge_overlapping(self):
        """Test merging overlapping subtitles."""
        subs = [
            Subtitle(1, 1000, 3000, "First"),
            Subtitle(2, 2000, 4000, "Second"),  # Overlaps
            Subtitle(3, 5000, 7000, "Third"),  # No overlap
        ]
        
        merged = merge_overlapping_subtitles(subs)
        
        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0].start_time, 1000)
        self.assertEqual(merged[0].end_time, 4000)
        self.assertIn("First", merged[0].text)
        self.assertIn("Second", merged[0].text)
        
    def test_merge_no_overlapping(self):
        """Test merging when no overlaps exist."""
        subs = [
            Subtitle(1, 1000, 3000, "A"),
            Subtitle(2, 5000, 7000, "B"),
        ]
        
        merged = merge_overlapping_subtitles(subs)
        
        self.assertEqual(len(merged), 2)


class TestSplitLongSubtitles(unittest.TestCase):
    """Test subtitle splitting functions."""
    
    def test_split_long_subtitle(self):
        """Test splitting long subtitles."""
        subs = [
            Subtitle(1, 0, 10000, "This is a very long subtitle"),  # 10 seconds
        ]
        
        split = split_long_subtitles(subs, max_duration_ms=5000)
        
        self.assertEqual(len(split), 2)
        self.assertEqual(split[0].duration, 5000)
        self.assertEqual(split[1].duration, 5000)
        
    def test_no_split_short_subtitle(self):
        """Test that short subtitles are not split."""
        subs = [
            Subtitle(1, 0, 3000, "Short"),  # 3 seconds
        ]
        
        split = split_long_subtitles(subs, max_duration_ms=5000)
        
        self.assertEqual(len(split), 1)


class TestRemoveEmptySubtitles(unittest.TestCase):
    """Test empty subtitle removal."""
    
    def test_remove_empty(self):
        """Test removing empty subtitles."""
        subs = [
            Subtitle(1, 0, 1000, "Text"),
            Subtitle(2, 2000, 3000, ""),  # Empty
            Subtitle(3, 4000, 5000, "   "),  # Whitespace
            Subtitle(4, 6000, 7000, "More text"),
        ]
        
        result = remove_empty_subtitles(subs)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Text")
        self.assertEqual(result[1].text, "More text")


class TestFilterByTimeRange(unittest.TestCase):
    """Test time range filtering."""
    
    def test_filter_by_time_range(self):
        """Test filtering subtitles within time range."""
        subs = [
            Subtitle(1, 0, 2000, "A"),
            Subtitle(2, 3000, 5000, "B"),
            Subtitle(3, 6000, 8000, "C"),
        ]
        
        result = filter_by_time_range(subs, 2500, 5500)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "B")


class TestFindSubtitleAtTime(unittest.TestCase):
    """Test finding subtitle at specific time."""
    
    def test_find_subtitle_at_time(self):
        """Test finding subtitle containing a time point."""
        subs = [
            Subtitle(1, 1000, 3000, "First"),
            Subtitle(2, 4000, 6000, "Second"),
        ]
        
        self.assertEqual(find_subtitle_at_time(subs, 1500).text, "First")
        self.assertEqual(find_subtitle_at_time(subs, 5000).text, "Second")
        self.assertIsNone(find_subtitle_at_time(subs, 3500))


class TestValidation(unittest.TestCase):
    """Test validation functions."""
    
    def test_validate_valid_subtitles(self):
        """Test validating valid subtitles."""
        subs = [
            Subtitle(1, 1000, 3000, "First"),
            Subtitle(2, 4000, 6000, "Second"),
        ]
        
        result = validate_subtitles(subs)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
        
    def test_validate_negative_time(self):
        """Test validating negative time."""
        subs = [
            Subtitle(1, -1000, 3000, "Test"),
        ]
        
        result = validate_subtitles(subs)
        
        self.assertFalse(result.is_valid)
        self.assertIn("Negative start time", str(result.errors))
        
    def test_validate_start_after_end(self):
        """Test validating start time after end time."""
        subs = [
            Subtitle(1, 5000, 3000, "Test"),
        ]
        
        result = validate_subtitles(subs)
        
        self.assertFalse(result.is_valid)
        self.assertIn("Start time >= end time", str(result.errors))
        
    def test_validate_duplicate_index(self):
        """Test validating duplicate indices."""
        subs = [
            Subtitle(1, 1000, 3000, "First"),
            Subtitle(1, 4000, 6000, "Second"),
        ]
        
        result = validate_subtitles(subs)
        
        self.assertFalse(result.is_valid)
        self.assertIn("Duplicate index", str(result.errors))
        
    def test_validate_empty_subtitles(self):
        """Test validating empty subtitle list."""
        result = validate_subtitles([])
        
        self.assertFalse(result.is_valid)
        self.assertIn("No subtitles", str(result.errors))
        
    def test_validate_srt_content(self):
        """Test validating SRT content string."""
        content = """1
00:00:01,000 --> 00:00:03,000
Valid subtitle"""
        
        result = validate_srt_content(content)
        
        self.assertTrue(result.is_valid)


class TestStatistics(unittest.TestCase):
    """Test statistics functions."""
    
    def test_statistics_empty(self):
        """Test statistics on empty list."""
        stats = get_statistics([])
        
        self.assertEqual(stats['count'], 0)
        self.assertEqual(stats['total_duration_ms'], 0)
        
    def test_statistics_single(self):
        """Test statistics on single subtitle."""
        subs = [Subtitle(1, 1000, 5000, "Test")]
        
        stats = get_statistics(subs)
        
        self.assertEqual(stats['count'], 1)
        self.assertEqual(stats['total_duration_ms'], 4000)
        self.assertEqual(stats['average_duration_ms'], 4000)
        self.assertEqual(stats['min_duration_ms'], 4000)
        self.assertEqual(stats['max_duration_ms'], 4000)
        
    def test_statistics_multiple(self):
        """Test statistics on multiple subtitles."""
        subs = [
            Subtitle(1, 0, 2000, "A"),    # 2000ms
            Subtitle(2, 3000, 8000, "B"),  # 5000ms
        ]
        
        stats = get_statistics(subs)
        
        self.assertEqual(stats['count'], 2)
        self.assertEqual(stats['total_duration_ms'], 7000)
        self.assertEqual(stats['average_duration_ms'], 3500)
        self.assertEqual(stats['min_duration_ms'], 2000)
        self.assertEqual(stats['max_duration_ms'], 5000)
        self.assertEqual(stats['total_text_length'], 2)  # "A" + "B"


class TestConversion(unittest.TestCase):
    """Test format conversion functions."""
    
    def test_srt_to_vtt(self):
        """Test SRT to VTT conversion."""
        srt_content = """1
00:00:01,000 --> 00:00:03,000
Hello world!"""
        
        vtt_result = srt_to_vtt(srt_content)
        
        self.assertIn("WEBVTT", vtt_result)
        self.assertIn("00:00:01.000 --> 00:00:03.000", vtt_result)  # Dot, not comma
        self.assertIn("Hello world!", vtt_result)
        
    def test_vtt_to_srt(self):
        """Test VTT to SRT conversion."""
        vtt_content = """WEBVTT

00:00:01.000 --> 00:00:03.000
Hello world!"""
        
        srt_result = vtt_to_srt(vtt_content)
        
        self.assertIn("1\n", srt_result)
        self.assertIn("00:00:01,000 --> 00:00:03,000", srt_result)  # Comma, not dot
        self.assertIn("Hello world!", srt_result)


class TestCreateSubtitle(unittest.TestCase):
    """Test subtitle creation helper."""
    
    def test_create_with_strings(self):
        """Test creating subtitle with time strings."""
        sub = create_subtitle(1, "00:00:01,000", "00:00:03,000", "Test")
        
        self.assertEqual(sub.index, 1)
        self.assertEqual(sub.start_time, 1000)
        self.assertEqual(sub.end_time, 3000)
        self.assertEqual(sub.text, "Test")
        
    def test_create_with_integers(self):
        """Test creating subtitle with integer times."""
        sub = create_subtitle(1, 1000, 3000, "Test")
        
        self.assertEqual(sub.start_time, 1000)
        self.assertEqual(sub.end_time, 3000)


class TestConcatenateSubtitles(unittest.TestCase):
    """Test subtitle concatenation."""
    
    def test_concatenate(self):
        """Test concatenating subtitle lists."""
        list1 = [Subtitle(1, 0, 2000, "First")]
        list2 = [Subtitle(1, 0, 3000, "Second")]
        
        result = concatenate_subtitles([list1, list2], gap_ms=1000)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].start_time, 0)
        self.assertEqual(result[0].end_time, 2000)
        self.assertEqual(result[1].start_time, 3000)  # 2000 + 1000 gap
        self.assertEqual(result[1].end_time, 6000)  # 3000 + 3000 shift
        
    def test_concatenate_empty(self):
        """Test concatenating with empty lists."""
        list1 = [Subtitle(1, 0, 2000, "First")]
        
        result = concatenate_subtitles([list1, [], list1], gap_ms=500)
        
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)