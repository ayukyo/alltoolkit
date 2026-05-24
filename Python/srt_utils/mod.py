#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - SRT Subtitle Utilities Module
===========================================
A comprehensive SRT (SubRip) subtitle file manipulation utility module for Python with zero external dependencies.

Features:
    - SRT file parsing and generation
    - Time format conversion (SRT, VTT, milliseconds)
    - Subtitle manipulation (shift time, merge, split)
    - Subtitle validation and error detection
    - Encoding detection and handling
    - Batch operations on subtitle collections
    - Export to VTT (WebVTT) format
    - Subtitle synchronization tools

Author: AllToolkit Contributors
License: MIT
"""

from typing import Union, List, Optional, Dict, Any, Tuple, Iterator
from dataclasses import dataclass, field
from enum import Enum
import re
from datetime import timedelta


# ============================================================================
# Constants
# ============================================================================

# SRT time format: HH:MM:SS,mmm (comma for milliseconds, NOT dot)
SRT_TIME_PATTERN = re.compile(
    r'(\d{2}):(\d{2}):(\d{2}),(\d{3})'
)

# VTT time format: HH:MM:SS.mmm (dot for milliseconds) or MM:SS.mmm
VTT_TIME_PATTERN = re.compile(
    r'(?:(\d{2}):)?(\d{2}):(\d{2})\.(\d{3})'
)

# Subtitle block pattern - captures multiline text correctly
SUBTITLE_BLOCK_PATTERN = re.compile(
    r'(\d+)\s*\n'
    r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s*\n'
    r'([\s\S]*?)(?=\n\n|\n\d+\s*\n|\n*$)',
    re.MULTILINE
)


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class Subtitle:
    """
    Represents a single subtitle entry.
    
    Attributes:
        index: Subtitle sequence number
        start_time: Start time in milliseconds
        end_time: End time in milliseconds
        text: Subtitle text (may contain multiple lines)
        metadata: Optional metadata dictionary
    """
    index: int
    start_time: int  # milliseconds
    end_time: int    # milliseconds
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def duration(self) -> int:
        """Get subtitle duration in milliseconds."""
        return self.end_time - self.start_time
    
    @property
    def start_timedelta(self) -> timedelta:
        """Get start time as timedelta."""
        return timedelta(milliseconds=self.start_time)
    
    @property
    def end_timedelta(self) -> timedelta:
        """Get end time as timedelta."""
        return timedelta(milliseconds=self.end_time)
    
    def __str__(self) -> str:
        """Return SRT format string."""
        return self.to_srt()
    
    def to_srt(self) -> str:
        """Convert to SRT format string."""
        return (
            f"{self.index}\n"
            f"{milliseconds_to_srt_time(self.start_time)} --> {milliseconds_to_srt_time(self.end_time)}\n"
            f"{self.text}"
        )
    
    def to_vtt(self) -> str:
        """Convert to VTT format string (without 'WEBVTT' header)."""
        return (
            f"{milliseconds_to_vtt_time(self.start_time)} --> {milliseconds_to_vtt_time(self.end_time)}\n"
            f"{self.text}"
        )
    
    def shift(self, milliseconds: int) -> 'Subtitle':
        """
        Shift subtitle timing by given milliseconds.
        
        Args:
            milliseconds: Amount to shift (positive = later, negative = earlier)
            
        Returns:
            New Subtitle with shifted timing
        """
        return Subtitle(
            index=self.index,
            start_time=max(0, self.start_time + milliseconds),
            end_time=max(0, self.end_time + milliseconds),
            text=self.text,
            metadata=self.metadata.copy()
        )
    
    def scale(self, factor: float, origin: int = 0) -> 'Subtitle':
        """
        Scale subtitle timing by a factor.
        
        Args:
            factor: Scaling factor (e.g., 0.9 = 10% faster)
            origin: Origin point in milliseconds for scaling
            
        Returns:
            New Subtitle with scaled timing
        """
        new_start = origin + int((self.start_time - origin) * factor)
        new_end = origin + int((self.end_time - origin) * factor)
        return Subtitle(
            index=self.index,
            start_time=max(0, new_start),
            end_time=max(0, new_end),
            text=self.text,
            metadata=self.metadata.copy()
        )
    
    def overlaps(self, other: 'Subtitle') -> bool:
        """Check if this subtitle overlaps with another."""
        return (
            self.start_time < other.end_time and
            self.end_time > other.start_time
        )
    
    def contains(self, milliseconds: int) -> bool:
        """Check if a time point is within this subtitle's range."""
        return self.start_time <= milliseconds <= self.end_time
    
    def merge_with(self, other: 'Subtitle', separator: str = '\n') -> 'Subtitle':
        """
        Merge this subtitle with another.
        
        Args:
            other: Another subtitle to merge with
            separator: Text separator (default: newline)
            
        Returns:
            New merged subtitle
        """
        return Subtitle(
            index=min(self.index, other.index),
            start_time=min(self.start_time, other.start_time),
            end_time=max(self.end_time, other.end_time),
            text=self.text + separator + other.text,
            metadata={**self.metadata, **other.metadata}
        )
    
    def split_at(self, milliseconds: int, index_offset: int = 0) -> Tuple['Subtitle', 'Subtitle']:
        """
        Split subtitle at a given time point.
        
        Args:
            milliseconds: Split point in milliseconds
            index_offset: Offset for the second subtitle index
            
        Returns:
            Tuple of two new subtitles
        """
        if not self.contains(milliseconds):
            raise ValueError(f"Split point {milliseconds} is not within subtitle range")
        
        return (
            Subtitle(
                index=self.index,
                start_time=self.start_time,
                end_time=milliseconds,
                text=self.text,
                metadata=self.metadata.copy()
            ),
            Subtitle(
                index=self.index + index_offset,
                start_time=milliseconds,
                end_time=self.end_time,
                text=self.text,
                metadata=self.metadata.copy()
            )
        )


@dataclass
class ValidationResult:
    """Result of subtitle file validation."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def __bool__(self) -> bool:
        return self.is_valid


# ============================================================================
# Time Conversion Functions
# ============================================================================

def srt_time_to_milliseconds(time_str: str) -> int:
    """
    Convert SRT time format (HH:MM:SS,mmm) to milliseconds.
    
    Args:
        time_str: Time string in SRT format
        
    Returns:
        Time in milliseconds
        
    Examples:
        >>> srt_time_to_milliseconds("00:01:30,500")
        90500
        >>> srt_time_to_milliseconds("01:02:03,456")
        3723456
    """
    match = SRT_TIME_PATTERN.match(time_str.strip())
    if not match:
        raise ValueError(f"Invalid SRT time format: {time_str}")
    
    hours, minutes, seconds, millis = match.groups()
    return (
        int(hours) * 3600000 +
        int(minutes) * 60000 +
        int(seconds) * 1000 +
        int(millis)
    )


def milliseconds_to_srt_time(ms: int) -> str:
    """
    Convert milliseconds to SRT time format (HH:MM:SS,mmm).
    
    Args:
        ms: Time in milliseconds
        
    Returns:
        Time string in SRT format
        
    Examples:
        >>> milliseconds_to_srt_time(90500)
        '00:01:30,500'
        >>> milliseconds_to_srt_time(3723456)
        '01:02:03,456'
    """
    if ms < 0:
        ms = 0
    
    hours = ms // 3600000
    ms %= 3600000
    minutes = ms // 60000
    ms %= 60000
    seconds = ms // 1000
    milliseconds = ms % 1000
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def vtt_time_to_milliseconds(time_str: str) -> int:
    """
    Convert VTT time format (HH:MM:SS.mmm or MM:SS.mmm) to milliseconds.
    
    Args:
        time_str: Time string in VTT format
        
    Returns:
        Time in milliseconds
        
    Examples:
        >>> vtt_time_to_milliseconds("00:01:30.500")
        90500
        >>> vtt_time_to_milliseconds("01:30.500")
        90500
    """
    match = VTT_TIME_PATTERN.match(time_str.strip())
    if not match:
        raise ValueError(f"Invalid VTT time format: {time_str}")
    
    hours, minutes, seconds, millis = match.groups()
    hours = int(hours) if hours else 0
    
    return (
        hours * 3600000 +
        int(minutes) * 60000 +
        int(seconds) * 1000 +
        int(millis)
    )


def milliseconds_to_vtt_time(ms: int) -> str:
    """
    Convert milliseconds to VTT time format (HH:MM:SS.mmm).
    
    Args:
        ms: Time in milliseconds
        
    Returns:
        Time string in VTT format
    """
    if ms < 0:
        ms = 0
    
    hours = ms // 3600000
    ms %= 3600000
    minutes = ms // 60000
    ms %= 60000
    seconds = ms // 1000
    milliseconds = ms % 1000
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def format_duration(ms: int, format_type: str = 'readable') -> str:
    """
    Format duration in a human-readable way.
    
    Args:
        ms: Duration in milliseconds
        format_type: 'readable', 'compact', or 'srt'
        
    Returns:
        Formatted duration string
    """
    if format_type == 'srt':
        return milliseconds_to_srt_time(ms)
    
    total_seconds = ms // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = ms % 1000
    
    if format_type == 'compact':
        if hours > 0:
            return f"{hours}h{minutes}m{seconds}s"
        elif minutes > 0:
            return f"{minutes}m{seconds}s"
        else:
            return f"{seconds}s"
    
    # readable
    parts = []
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    
    return ' '.join(parts)


# ============================================================================
# Parsing Functions
# ============================================================================

def parse_srt(content: str, encoding: str = 'utf-8') -> List[Subtitle]:
    """
    Parse SRT content into a list of Subtitle objects.
    
    Args:
        content: SRT file content
        encoding: Text encoding (for error messages)
        
    Returns:
        List of Subtitle objects
        
    Examples:
        >>> srt_content = '''1
        ... 00:00:01,000 --> 00:00:04,000
        ... Hello world!
        ...
        ... 2
        ... 00:00:05,000 --> 00:00:08,000
        ... Second subtitle'''
        >>> subtitles = parse_srt(srt_content)
        >>> len(subtitles)
        2
        >>> subtitles[0].text
        'Hello world!'
    """
    # Normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove BOM if present
    if content.startswith('\ufeff'):
        content = content[1:]
    
    subtitles = []
    
    # Split by double newlines (subtitle blocks)
    blocks = content.strip().split('\n\n')
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        
        lines = block.split('\n')
        if len(lines) < 3:
            continue
        
        # First line is index
        try:
            index = int(lines[0].strip())
        except ValueError:
            continue
        
        # Second line is timestamp
        timestamp_line = lines[1].strip()
        ts_match = re.match(
            r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})',
            timestamp_line
        )
        if not ts_match:
            # Try with dot separator (some non-standard SRT files use this)
            ts_match = re.match(
                r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})',
                timestamp_line
            )
            if ts_match:
                # Convert dot to comma format
                start_str = ts_match.group(1).replace('.', ',')
                end_str = ts_match.group(2).replace('.', ',')
            else:
                continue
        else:
            start_str = ts_match.group(1)
            end_str = ts_match.group(2)
        
        start_time = srt_time_to_milliseconds(start_str)
        end_time = srt_time_to_milliseconds(end_str)
        
        # Remaining lines are text (may be multiple lines)
        text = '\n'.join(lines[2:])
        
        subtitles.append(Subtitle(
            index=index,
            start_time=start_time,
            end_time=end_time,
            text=text
        ))
    
    return subtitles


def parse_srt_file(filepath: str, encoding: str = 'utf-8') -> List[Subtitle]:
    """
    Parse an SRT file into a list of Subtitle objects.
    
    Args:
        filepath: Path to the SRT file
        encoding: File encoding (default: utf-8)
        
    Returns:
        List of Subtitle objects
    """
    with open(filepath, 'r', encoding=encoding) as f:
        content = f.read()
    
    return parse_srt(content, encoding)


def parse_vtt(content: str) -> List[Subtitle]:
    """
    Parse WebVTT content into a list of Subtitle objects.
    
    Args:
        content: VTT file content
        
    Returns:
        List of Subtitle objects
    """
    # Normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove BOM if present
    if content.startswith('\ufeff'):
        content = content[1:]
    
    # Skip WEBVTT header and any header metadata
    lines = content.split('\n')
    start_idx = 0
    
    for i, line in enumerate(lines):
        if '-->' in line:
            start_idx = i - 1 if i > 0 and lines[i-1].isdigit() else i
            break
        if line.strip() and not line.startswith('WEBVTT') and not line.startswith('NOTE') and ':' not in line:
            start_idx = i
            break
    
    content = '\n'.join(lines[start_idx:])
    
    # Parse blocks
    subtitles = []
    current_index = 1
    
    # VTT block pattern (index is optional in VTT)
    vtt_block_pattern = re.compile(
        r'(?:^|\n)(?:(\d+)\s*\n)?'
        r'(\d{2}:)?(\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:)?(\d{2}:\d{2}\.\d{3})'
        r'(?:[ \t]+(.*?))?\s*\n'
        r'([\s\S]*?)(?=\n\n|\n*$|\Z)',
        re.MULTILINE
    )
    
    # Simpler approach: split by double newlines
    blocks = re.split(r'\n\n+', content.strip())
    
    for block in blocks:
        block = block.strip()
        if not block or block.startswith('WEBVTT') or block.startswith('NOTE'):
            continue
        
        # Find timestamp line
        ts_match = re.search(
            r'((?:\d{2}:)?\d{2}:\d{2}[.,]\d{3})\s*-->\s*((?:\d{2}:)?\d{2}:\d{2}[.,]\d{3})',
            block
        )
        
        if not ts_match:
            continue
        
        start_time = vtt_time_to_milliseconds(ts_match.group(1).replace(',', '.'))
        end_time = vtt_time_to_milliseconds(ts_match.group(2).replace(',', '.'))
        
        # Get text (everything after timestamp line)
        text_start = ts_match.end()
        text = block[text_start:].strip()
        
        # Check for index number before timestamp
        lines_before = block[:ts_match.start()].strip().split('\n')
        index = current_index
        if lines_before and lines_before[-1].isdigit():
            index = int(lines_before[-1])
        
        subtitles.append(Subtitle(
            index=index,
            start_time=start_time,
            end_time=end_time,
            text=text
        ))
        current_index += 1
    
    return subtitles


def parse_vtt_file(filepath: str, encoding: str = 'utf-8') -> List[Subtitle]:
    """
    Parse a WebVTT file into a list of Subtitle objects.
    
    Args:
        filepath: Path to the VTT file
        encoding: File encoding (default: utf-8)
        
    Returns:
        List of Subtitle objects
    """
    with open(filepath, 'r', encoding=encoding) as f:
        content = f.read()
    
    return parse_vtt(content)


# ============================================================================
# Generation Functions
# ============================================================================

def generate_srt(subtitles: List[Subtitle], reindex: bool = True) -> str:
    """
    Generate SRT content from a list of Subtitle objects.
    
    Args:
        subtitles: List of Subtitle objects
        reindex: Whether to renumber subtitles starting from 1
        
    Returns:
        SRT formatted string
    """
    if not subtitles:
        return ""
    
    # Sort by start time
    sorted_subs = sorted(subtitles, key=lambda s: s.start_time)
    
    if reindex:
        sorted_subs = [
            Subtitle(
                index=i + 1,
                start_time=s.start_time,
                end_time=s.end_time,
                text=s.text,
                metadata=s.metadata
            )
            for i, s in enumerate(sorted_subs)
        ]
    
    return '\n\n'.join(s.to_srt() for s in sorted_subs)


def generate_vtt(subtitles: List[Subtitle], header: str = "", reindex: bool = False) -> str:
    """
    Generate WebVTT content from a list of Subtitle objects.
    
    Args:
        subtitles: List of Subtitle objects
        header: Optional header comment (after WEBVTT)
        reindex: Whether to renumber subtitles
        
    Returns:
        VTT formatted string
    """
    lines = ["WEBVTT"]
    
    if header:
        lines.append(header)
    
    lines.append("")  # Empty line after header
    
    if not subtitles:
        return '\n'.join(lines)
    
    # Sort by start time
    sorted_subs = sorted(subtitles, key=lambda s: s.start_time)
    
    for i, sub in enumerate(sorted_subs, 1):
        if reindex:
            lines.append(f"{i}")
        elif sub.index > 0:
            lines.append(f"{sub.index}")
        
        lines.append(f"{milliseconds_to_vtt_time(sub.start_time)} --> {milliseconds_to_vtt_time(sub.end_time)}")
        lines.append(sub.text)
        lines.append("")
    
    return '\n'.join(lines)


def write_srt_file(subtitles: List[Subtitle], filepath: str, 
                   encoding: str = 'utf-8', reindex: bool = True) -> None:
    """
    Write subtitles to an SRT file.
    
    Args:
        subtitles: List of Subtitle objects
        filepath: Output file path
        encoding: File encoding (default: utf-8)
        reindex: Whether to renumber subtitles
    """
    content = generate_srt(subtitles, reindex=reindex)
    with open(filepath, 'w', encoding=encoding) as f:
        f.write(content)


def write_vtt_file(subtitles: List[Subtitle], filepath: str,
                   encoding: str = 'utf-8', header: str = "") -> None:
    """
    Write subtitles to a WebVTT file.
    
    Args:
        subtitles: List of Subtitle objects
        filepath: Output file path
        encoding: File encoding (default: utf-8)
        header: Optional header comment
    """
    content = generate_vtt(subtitles, header=header)
    with open(filepath, 'w', encoding=encoding) as f:
        f.write(content)


# ============================================================================
# Manipulation Functions
# ============================================================================

def shift_subtitles(subtitles: List[Subtitle], milliseconds: int) -> List[Subtitle]:
    """
    Shift all subtitles by a given time offset.
    
    Args:
        subtitles: List of Subtitle objects
        milliseconds: Time offset in milliseconds (positive = later)
        
    Returns:
        New list of shifted Subtitle objects
    """
    return [s.shift(milliseconds) for s in subtitles]


def scale_subtitles(subtitles: List[Subtitle], factor: float, 
                    origin: int = 0) -> List[Subtitle]:
    """
    Scale all subtitle timings by a factor.
    
    Args:
        subtitles: List of Subtitle objects
        factor: Scaling factor (e.g., 0.9 = 10% faster)
        origin: Origin point for scaling (default: 0)
        
    Returns:
        New list of scaled Subtitle objects
    """
    return [s.scale(factor, origin) for s in subtitles]


def merge_overlapping_subtitles(subtitles: List[Subtitle], 
                                separator: str = ' ') -> List[Subtitle]:
    """
    Merge overlapping subtitles into single subtitles.
    
    Args:
        subtitles: List of Subtitle objects
        separator: Text separator for merged text
        
    Returns:
        New list with overlapping subtitles merged
    """
    if not subtitles:
        return []
    
    # Sort by start time
    sorted_subs = sorted(subtitles, key=lambda s: s.start_time)
    
    result = [sorted_subs[0]]
    
    for current in sorted_subs[1:]:
        previous = result[-1]
        
        if previous.overlaps(current):
            # Merge with previous
            result[-1] = previous.merge_with(current, separator)
        else:
            result.append(current)
    
    # Reindex
    return [
        Subtitle(index=i+1, start_time=s.start_time, end_time=s.end_time,
                  text=s.text, metadata=s.metadata)
        for i, s in enumerate(result)
    ]


def split_long_subtitles(subtitles: List[Subtitle], 
                         max_duration_ms: int = 5000,
                         min_duration_ms: int = 1000) -> List[Subtitle]:
    """
    Split subtitles that exceed maximum duration.
    
    Args:
        subtitles: List of Subtitle objects
        max_duration_ms: Maximum allowed duration in milliseconds
        min_duration_ms: Minimum duration for each split part
        
    Returns:
        New list with long subtitles split
    """
    result = []
    
    for sub in subtitles:
        if sub.duration <= max_duration_ms:
            result.append(sub)
        else:
            # Calculate how many parts we need
            num_parts = (sub.duration + max_duration_ms - 1) // max_duration_ms
            part_duration = sub.duration // num_parts
            
            if part_duration < min_duration_ms:
                # Can't split evenly, just keep original
                result.append(sub)
                continue
            
            # Create split parts
            for i in range(num_parts):
                start = sub.start_time + i * part_duration
                end = sub.start_time + (i + 1) * part_duration if i < num_parts - 1 else sub.end_time
                
                result.append(Subtitle(
                    index=len(result) + 1,
                    start_time=start,
                    end_time=end,
                    text=sub.text,
                    metadata=sub.metadata.copy()
                ))
    
    # Reindex
    return [
        Subtitle(index=i+1, start_time=s.start_time, end_time=s.end_time,
                  text=s.text, metadata=s.metadata)
        for i, s in enumerate(result)
    ]


def remove_empty_subtitles(subtitles: List[Subtitle]) -> List[Subtitle]:
    """
    Remove subtitles with empty or whitespace-only text.
    
    Args:
        subtitles: List of Subtitle objects
        
    Returns:
        New list without empty subtitles
    """
    return [
        Subtitle(index=i+1, start_time=s.start_time, end_time=s.end_time,
                  text=s.text, metadata=s.metadata)
        for i, s in enumerate(s for s in subtitles if s.text.strip())
    ]


def filter_by_time_range(subtitles: List[Subtitle], 
                         start_ms: int, end_ms: int) -> List[Subtitle]:
    """
    Filter subtitles within a time range.
    
    Args:
        subtitles: List of Subtitle objects
        start_ms: Start time in milliseconds
        end_ms: End time in milliseconds
        
    Returns:
        New list with filtered subtitles
    """
    return [
        Subtitle(index=i+1, start_time=s.start_time, end_time=s.end_time,
                  text=s.text, metadata=s.metadata)
        for i, s in enumerate(
            s for s in subtitles
            if s.start_time >= start_ms and s.end_time <= end_ms
        )
    ]


def find_subtitle_at_time(subtitles: List[Subtitle], 
                          time_ms: int) -> Optional[Subtitle]:
    """
    Find subtitle that contains a given time point.
    
    Args:
        subtitles: List of Subtitle objects
        time_ms: Time point in milliseconds
        
    Returns:
        Subtitle at that time, or None
    """
    for sub in subtitles:
        if sub.contains(time_ms):
            return sub
    return None


# ============================================================================
# Validation Functions
# ============================================================================

def validate_subtitles(subtitles: List[Subtitle]) -> ValidationResult:
    """
    Validate a list of subtitles for common issues.
    
    Args:
        subtitles: List of Subtitle objects
        
    Returns:
        ValidationResult with errors and warnings
    """
    errors = []
    warnings = []
    
    if not subtitles:
        errors.append("No subtitles found")
        return ValidationResult(False, errors, warnings)
    
    # Check for issues
    seen_indices = set()
    prev_end_time = -1
    
    for i, sub in enumerate(subtitles):
        # Check index
        if sub.index in seen_indices:
            errors.append(f"Duplicate index: {sub.index}")
        seen_indices.add(sub.index)
        
        # Check timing
        if sub.start_time < 0:
            errors.append(f"Subtitle {sub.index}: Negative start time")
        
        if sub.end_time < 0:
            errors.append(f"Subtitle {sub.index}: Negative end time")
        
        if sub.start_time >= sub.end_time:
            errors.append(f"Subtitle {sub.index}: Start time >= end time")
        
        if sub.duration < 100:
            warnings.append(f"Subtitle {sub.index}: Very short duration ({sub.duration}ms)")
        
        if sub.duration > 10000:
            warnings.append(f"Subtitle {sub.index}: Very long duration ({sub.duration}ms)")
        
        # Check ordering
        if sub.start_time < prev_end_time:
            warnings.append(f"Subtitle {sub.index}: Overlaps with previous subtitle")
        prev_end_time = sub.end_time
        
        # Check text
        if not sub.text.strip():
            warnings.append(f"Subtitle {sub.index}: Empty text")
    
    return ValidationResult(len(errors) == 0, errors, warnings)


def validate_srt_content(content: str) -> ValidationResult:
    """
    Validate SRT content for format issues.
    
    Args:
        content: SRT file content
        
    Returns:
        ValidationResult with errors and warnings
    """
    errors = []
    warnings = []
    
    # Check for common format issues
    if not content.strip():
        errors.append("Empty content")
        return ValidationResult(False, errors, warnings)
    
    # Try to parse
    try:
        subtitles = parse_srt(content)
        return validate_subtitles(subtitles)
    except Exception as e:
        errors.append(f"Parse error: {str(e)}")
        return ValidationResult(False, errors, warnings)


# ============================================================================
# Statistics Functions
# ============================================================================

def get_statistics(subtitles: List[Subtitle]) -> Dict[str, Any]:
    """
    Get statistics about a subtitle collection.
    
    Args:
        subtitles: List of Subtitle objects
        
    Returns:
        Dictionary with statistics
    """
    if not subtitles:
        return {
            'count': 0,
            'total_duration_ms': 0,
            'total_text_length': 0,
            'average_duration_ms': 0,
            'average_text_length': 0,
            'min_duration_ms': 0,
            'max_duration_ms': 0,
            'first_start_ms': 0,
            'last_end_ms': 0,
            'coverage_seconds': 0
        }
    
    durations = [s.duration for s in subtitles]
    text_lengths = [len(s.text) for s in subtitles]
    
    total_duration = sum(durations)
    total_text = sum(text_lengths)
    
    return {
        'count': len(subtitles),
        'total_duration_ms': total_duration,
        'total_text_length': total_text,
        'average_duration_ms': total_duration // len(subtitles),
        'average_text_length': total_text // len(subtitles),
        'min_duration_ms': min(durations),
        'max_duration_ms': max(durations),
        'first_start_ms': subtitles[0].start_time,
        'last_end_ms': subtitles[-1].end_time,
        'coverage_seconds': (subtitles[-1].end_time - subtitles[0].start_time) // 1000
    }


# ============================================================================
# Conversion Functions
# ============================================================================

def srt_to_vtt(srt_content: str) -> str:
    """
    Convert SRT content to WebVTT format.
    
    Args:
        srt_content: SRT formatted string
        
    Returns:
        VTT formatted string
    """
    subtitles = parse_srt(srt_content)
    return generate_vtt(subtitles)


def vtt_to_srt(vtt_content: str) -> str:
    """
    Convert WebVTT content to SRT format.
    
    Args:
        vtt_content: VTT formatted string
        
    Returns:
        SRT formatted string
    """
    subtitles = parse_vtt(vtt_content)
    return generate_srt(subtitles)


# ============================================================================
# Utility Functions
# ============================================================================

def create_subtitle(index: int, start_time: Union[str, int], 
                    end_time: Union[str, int], text: str) -> Subtitle:
    """
    Create a Subtitle object with flexible time input.
    
    Args:
        index: Subtitle sequence number
        start_time: Start time (SRT string or milliseconds)
        end_time: End time (SRT string or milliseconds)
        text: Subtitle text
        
    Returns:
        New Subtitle object
    """
    start_ms = (
        srt_time_to_milliseconds(start_time) 
        if isinstance(start_time, str) 
        else start_time
    )
    end_ms = (
        srt_time_to_milliseconds(end_time) 
        if isinstance(end_time, str) 
        else end_time
    )
    
    return Subtitle(index=index, start_time=start_ms, end_time=end_ms, text=text)


def concatenate_subtitles(subtitle_lists: List[List[Subtitle]], 
                         gap_ms: int = 1000) -> List[Subtitle]:
    """
    Concatenate multiple subtitle lists with a gap between them.
    
    Args:
        subtitle_lists: List of subtitle lists to concatenate
        gap_ms: Gap between subtitle lists in milliseconds
        
    Returns:
        Single concatenated list of subtitles
    """
    result = []
    current_offset = 0
    
    for subs in subtitle_lists:
        if not subs:
            continue
        
        # Shift all subtitles to current offset
        for sub in subs:
            result.append(Subtitle(
                index=len(result) + 1,
                start_time=sub.start_time + current_offset,
                end_time=sub.end_time + current_offset,
                text=sub.text,
                metadata=sub.metadata
            ))
        
        # Update offset for next list
        if result:
            current_offset = result[-1].end_time + gap_ms
    
    return result


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Demo usage
    print("=" * 60)
    print("SRT Utilities Demo")
    print("=" * 60)
    
    # Create some subtitles
    subs = [
        create_subtitle(1, "00:00:01,000", "00:00:03,000", "Hello, welcome to the show!"),
        create_subtitle(2, "00:00:04,000", "00:00:07,500", "Today we'll learn about subtitles."),
        create_subtitle(3, "00:00:08,000", "00:00:12,000", "SRT is a popular subtitle format."),
    ]
    
    # Generate SRT
    print("\nSRT Output:")
    print("-" * 40)
    srt_output = generate_srt(subs)
    print(srt_output)
    
    # Generate VTT
    print("\nVTT Output:")
    print("-" * 40)
    vtt_output = generate_vtt(subs)
    print(vtt_output)
    
    # Statistics
    print("\nStatistics:")
    print("-" * 40)
    stats = get_statistics(subs)
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Time conversion demo
    print("\nTime Conversion Demo:")
    print("-" * 40)
    ms = 90500
    print(f"  {ms}ms = {milliseconds_to_srt_time(ms)} (SRT)")
    print(f"  {ms}ms = {milliseconds_to_vtt_time(ms)} (VTT)")
    print(f"  {ms}ms = {format_duration(ms)} (readable)")
    print(f"  {ms}ms = {format_duration(ms, 'compact')} (compact)")
    
    # Validation demo
    print("\nValidation:")
    print("-" * 40)
    result = validate_subtitles(subs)
    print(f"  Valid: {result.is_valid}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Warnings: {len(result.warnings)}")