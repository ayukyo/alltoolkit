#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - SRT Utilities Usage Examples
==========================================
Comprehensive examples demonstrating all features of the SRT utilities module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from srt_utils.mod import (
    Subtitle,
    srt_time_to_milliseconds, milliseconds_to_srt_time,
    vtt_time_to_milliseconds, milliseconds_to_vtt_time,
    format_duration,
    parse_srt, parse_vtt,
    generate_srt, generate_vtt,
    shift_subtitles, scale_subtitles,
    merge_overlapping_subtitles, split_long_subtitles,
    remove_empty_subtitles, filter_by_time_range,
    find_subtitle_at_time,
    validate_subtitles, validate_srt_content,
    get_statistics,
    srt_to_vtt, vtt_to_srt,
    create_subtitle, concatenate_subtitles,
    write_srt_file, write_vtt_file,
)


def example_basic_usage():
    """Example 1: Basic SRT parsing and generation."""
    print("=" * 60)
    print("Example 1: Basic SRT Parsing and Generation")
    print("=" * 60)
    
    # Sample SRT content
    srt_content = """1
00:00:01,000 --> 00:00:04,000
Hello, welcome to our tutorial!

2
00:00:05,000 --> 00:00:08,500
Today we'll learn about subtitle files.

3
00:00:09,000 --> 00:00:13,000
SRT is the most common subtitle format."""
    
    # Parse SRT content
    subtitles = parse_srt(srt_content)
    
    print(f"\nParsed {len(subtitles)} subtitles:")
    for sub in subtitles:
        print(f"  [{sub.index}] {milliseconds_to_srt_time(sub.start_time)} --> {milliseconds_to_srt_time(sub.end_time)}")
        print(f"      Text: {sub.text}")
        print(f"      Duration: {sub.duration}ms ({format_duration(sub.duration, 'compact')})")
    
    # Generate SRT output
    print("\nGenerated SRT:")
    print(generate_srt(subtitles))


def example_time_conversion():
    """Example 2: Time format conversions."""
    print("\n" + "=" * 60)
    print("Example 2: Time Format Conversions")
    print("=" * 60)
    
    # SRT time format conversions
    srt_time = "01:23:45,678"
    ms = srt_time_to_milliseconds(srt_time)
    print(f"\nSRT time '{srt_time}' = {ms} milliseconds")
    print(f"Back to SRT: {milliseconds_to_srt_time(ms)}")
    
    # VTT time format conversions
    vtt_time = "01:23:45.678"
    ms = vtt_time_to_milliseconds(vtt_time)
    print(f"\nVTT time '{vtt_time}' = {ms} milliseconds")
    print(f"Back to VTT: {milliseconds_to_vtt_time(ms)}")
    
    # Human-readable duration
    print("\nDuration formatting:")
    test_ms = [1000, 90000, 3661000, 7323000]
    for ms in test_ms:
        print(f"  {ms}ms = {format_duration(ms, 'readable')}")
        print(f"  {ms}ms = {format_duration(ms, 'compact')}")
        print(f"  {ms}ms = {format_duration(ms, 'srt')}")
        print()


def example_subtitle_shift():
    """Example 3: Shifting subtitle timing."""
    print("=" * 60)
    print("Example 3: Shifting Subtitle Timing")
    print("=" * 60)
    
    # Create subtitles
    subtitles = [
        create_subtitle(1, "00:00:01,000", "00:00:03,000", "Original timing"),
        create_subtitle(2, "00:00:05,000", "00:00:08,000", "Second subtitle"),
    ]
    
    print("\nOriginal subtitles:")
    print(generate_srt(subtitles))
    
    # Shift forward by 5 seconds
    shifted_forward = shift_subtitles(subtitles, 5000)
    print("\nShifted forward by 5 seconds:")
    print(generate_srt(shifted_forward))
    
    # Shift backward by 2 seconds
    shifted_backward = shift_subtitles(subtitles, -2000)
    print("\nShifted backward by 2 seconds:")
    print(generate_srt(shifted_backward))


def example_subtitle_scaling():
    """Example 4: Scaling subtitle timing (speed adjustment)."""
    print("\n" + "=" * 60)
    print("Example 4: Scaling Subtitle Timing")
    print("=" * 60)
    
    subtitles = [
        create_subtitle(1, "00:00:10,000", "00:00:15,000", "Original"),
        create_subtitle(2, "00:00:20,000", "00:00:25,000", "Second"),
    ]
    
    print("\nOriginal subtitles (10-15s, 20-25s):")
    print(generate_srt(subtitles))
    
    # Scale to 90% (make video appear 10% faster)
    scaled = scale_subtitles(subtitles, 0.9)
    print("\nScaled to 90% (10% faster):")
    print(generate_srt(scaled))
    print(f"New durations: {scaled[0].duration}ms, {scaled[1].duration}ms")
    
    # Scale to 110% (make video appear 10% slower)
    scaled_slow = scale_subtitles(subtitles, 1.1)
    print("\nScaled to 110% (10% slower):")
    print(generate_srt(scaled_slow))
    print(f"New durations: {scaled_slow[0].duration}ms, {scaled_slow[1].duration}ms")


def example_merge_overlapping():
    """Example 5: Merging overlapping subtitles."""
    print("=" * 60)
    print("Example 5: Merging Overlapping Subtitles")
    print("=" * 60)
    
    # Subtitles that overlap
    subtitles = [
        create_subtitle(1, "00:00:01,000", "00:00:05,000", "Hello"),
        create_subtitle(2, "00:00:03,000", "00:00:07,000", "World"),  # Overlaps!
        create_subtitle(3, "00:00:10,000", "00:00:12,000", "Non-overlapping"),
    ]
    
    print("\nOriginal subtitles (with overlap):")
    for sub in subtitles:
        print(f"  [{sub.index}] {milliseconds_to_srt_time(sub.start_time)} --> {milliseconds_to_srt_time(sub.end_time)}: {sub.text}")
    
    # Merge overlapping
    merged = merge_overlapping_subtitles(subtitles, separator=" ")
    
    print(f"\nAfter merging ({len(merged)} subtitles):")
    for sub in merged:
        print(f"  [{sub.index}] {milliseconds_to_srt_time(sub.start_time)} --> {milliseconds_to_srt_time(sub.end_time)}: {sub.text}")


def example_split_long():
    """Example 6: Splitting long subtitles."""
    print("\n" + "=" * 60)
    print("Example 6: Splitting Long Subtitles")
    print("=" * 60)
    
    # Long subtitle (8 seconds)
    subtitles = [
        create_subtitle(1, "00:00:00,000", "00:00:08,000", 
                        "This is a very long subtitle that exceeds the maximum duration"),
    ]
    
    print("\nOriginal subtitle (8 seconds):")
    print(generate_srt(subtitles))
    
    # Split into chunks of max 4 seconds
    split = split_long_subtitles(subtitles, max_duration_ms=4000)
    
    print(f"\nSplit into {len(split)} parts (max 4s each):")
    print(generate_srt(split))


def example_validation():
    """Example 7: Validating subtitles."""
    print("=" * 60)
    print("Example 7: Subtitle Validation")
    print("=" * 60)
    
    # Valid subtitles
    valid_subs = [
        create_subtitle(1, "00:00:01,000", "00:00:04,000", "Good subtitle"),
        create_subtitle(2, "00:00:05,000", "00:00:08,000", "Another good one"),
    ]
    
    result = validate_subtitles(valid_subs)
    print(f"\nValid subtitles: is_valid={result.is_valid}")
    print(f"  Errors: {len(result.errors)}, Warnings: {len(result.warnings)}")
    
    # Invalid subtitles with various issues
    invalid_subs = [
        create_subtitle(1, "00:00:05,000", "00:00:02,000", "Start after end!"),
        create_subtitle(2, "00:00:10,000", "00:00:12,000", "Good"),
        create_subtitle(2, "00:00:13,000", "00:00:15,000", "Duplicate index"),
    ]
    
    result = validate_subtitles(invalid_subs)
    print(f"\nInvalid subtitles: is_valid={result.is_valid}")
    print(f"  Errors: {result.errors}")
    print(f"  Warnings: {result.warnings}")


def example_statistics():
    """Example 8: Getting subtitle statistics."""
    print("\n" + "=" * 60)
    print("Example 8: Subtitle Statistics")
    print("=" * 60)
    
    subtitles = [
        create_subtitle(1, "00:00:01,000", "00:00:03,000", "Short"),
        create_subtitle(2, "00:00:05,000", "00:00:08,000", "Medium length"),
        create_subtitle(3, "00:00:10,000", "00:00:15,000", "Longer subtitle here"),
    ]
    
    stats = get_statistics(subtitles)
    
    print("\nSubtitle Statistics:")
    print(f"  Total count: {stats['count']}")
    print(f"  Total duration: {format_duration(stats['total_duration_ms'], 'readable')}")
    print(f"  Average duration: {stats['average_duration_ms']}ms")
    print(f"  Min duration: {stats['min_duration_ms']}ms")
    print(f"  Max duration: {stats['max_duration_ms']}ms")
    print(f"  Total text length: {stats['total_text_length']} characters")
    print(f"  Average text length: {stats['average_text_length']} characters")
    print(f"  Time coverage: {stats['coverage_seconds']} seconds")


def example_format_conversion():
    """Example 9: Converting between SRT and VTT."""
    print("=" * 60)
    print("Example 9: Format Conversion (SRT <-> VTT)")
    print("=" * 60)
    
    srt_content = """1
00:00:01,000 --> 00:00:04,000
Hello world!

2
00:00:05,000 --> 00:00:08,000
Second subtitle"""
    
    print("\nOriginal SRT:")
    print(srt_content)
    
    # Convert to VTT
    vtt_output = srt_to_vtt(srt_content)
    print("\nConverted to VTT:")
    print(vtt_output)
    
    # Convert back to SRT
    srt_back = vtt_to_srt(vtt_output)
    print("\nConverted back to SRT:")
    print(srt_back)


def example_filter_and_find():
    """Example 10: Filtering and finding subtitles."""
    print("\n" + "=" * 60)
    print("Example 10: Filtering and Finding Subtitles")
    print("=" * 60)
    
    subtitles = [
        create_subtitle(1, "00:00:01,000", "00:00:04,000", "Intro"),
        create_subtitle(2, "00:00:05,000", "00:00:08,000", "Middle part"),
        create_subtitle(3, "00:00:10,000", "00:00:13,000", "More content"),
        create_subtitle(4, "00:00:15,000", "00:00:18,000", "Conclusion"),
    ]
    
    # Filter by time range (extract middle portion)
    filtered = filter_by_time_range(subtitles, 5000, 13000)
    print(f"\nFiltered subtitles (5s-13s range): {len(filtered)} found")
    for sub in filtered:
        print(f"  [{sub.index}] {sub.text}")
    
    # Find subtitle at specific time
    time_point = 6000  # 6 seconds
    found = find_subtitle_at_time(subtitles, time_point)
    print(f"\nSubtitle at 6 seconds: {found.text if found else 'None'}")
    
    time_point = 9000  # 9 seconds (gap)
    found = find_subtitle_at_time(subtitles, time_point)
    print(f"Subtitle at 9 seconds: {found.text if found else 'None'}")


def example_concatenate():
    """Example 11: Concatenating multiple subtitle tracks."""
    print("=" * 60)
    print("Example 11: Concatenating Subtitle Tracks")
    print("=" * 60)
    
    # Two separate subtitle tracks
    track1 = [
        create_subtitle(1, "00:00:00,000", "00:00:02,000", "Part 1 intro"),
        create_subtitle(2, "00:00:03,000", "00:00:05,000", "Part 1 content"),
    ]
    
    track2 = [
        create_subtitle(1, "00:00:00,000", "00:00:02,500", "Part 2 intro"),
        create_subtitle(2, "00:00:03,000", "00:00:06,000", "Part 2 content"),
    ]
    
    print("\nTrack 1:")
    print(generate_srt(track1))
    print("\nTrack 2:")
    print(generate_srt(track2))
    
    # Concatenate with 1 second gap between tracks
    combined = concatenate_subtitles([track1, track2], gap_ms=1000)
    
    print(f"\nCombined ({len(combined)} subtitles):")
    print(generate_srt(combined))


def example_practical_workflow():
    """Example 12: Practical subtitle editing workflow."""
    print("\n" + "=" * 60)
    print("Example 12: Practical Subtitle Editing Workflow")
    print("=" * 60)
    
    # Simulate a typical subtitle editing scenario
    print("\nScenario: You have subtitles that are 2 seconds too early,")
    print("          some overlapping subtitles, and one very long subtitle.")
    
    # Problem subtitles
    raw_subtitles = [
        create_subtitle(1, "00:00:01,000", "00:00:04,000", "Welcome"),
        create_subtitle(2, "00:00:03,500", "00:00:06,000", "To our show"),  # Overlaps
        create_subtitle(3, "00:00:08,000", "00:00:20,000", "This is a very long subtitle..."),  # Too long
        create_subtitle(4, "00:00:22,000", "00:00:25,000", "Goodbye"),
    ]
    
    print("\nStep 1: Original subtitles")
    stats = get_statistics(raw_subtitles)
    print(f"  Count: {stats['count']}, Duration range: {stats['min_duration_ms']}-{stats['max_duration_ms']}ms")
    
    # Step 2: Shift timing
    print("\nStep 2: Shift all subtitles forward by 2 seconds")
    shifted = shift_subtitles(raw_subtitles, 2000)
    
    # Step 3: Merge overlapping
    print("\nStep 3: Merge overlapping subtitles")
    merged = merge_overlapping_subtitles(shifted)
    
    # Step 4: Split long subtitles
    print("\nStep 4: Split long subtitles (max 5 seconds)")
    split = split_long_subtitles(merged, max_duration_ms=5000)
    
    # Step 5: Validate
    print("\nStep 5: Validate final result")
    result = validate_subtitles(split)
    print(f"  is_valid: {result.is_valid}")
    if result.warnings:
        print(f"  Warnings: {result.warnings}")
    
    # Final output
    print("\nFinal processed subtitles:")
    stats = get_statistics(split)
    print(f"  Count: {stats['count']}, Total duration: {format_duration(stats['total_duration_ms'], 'readable')}")
    print(generate_srt(split))


def main():
    """Run all examples."""
    example_basic_usage()
    example_time_conversion()
    example_subtitle_shift()
    example_subtitle_scaling()
    example_merge_overlapping()
    example_split_long()
    example_validation()
    example_statistics()
    example_format_conversion()
    example_filter_and_find()
    example_concatenate()
    example_practical_workflow()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()