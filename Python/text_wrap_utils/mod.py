#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Text Wrap Utilities Module
=======================================
A comprehensive text wrapping, justification and alignment utility module 
for Python with zero external dependencies.

Features:
    - Word wrapping with customizable width
    - Text justification (left, right, center, justify)
    - Paragraph formatting
    - Smart hyphenation support
    - Unicode-aware text processing
    - Indentation support
    - Hanging indentation
    - Preserve whitespace options
    - CJK (Chinese/Japanese/Korean) text support
    - ANSI color code aware wrapping

Author: AllToolkit Contributors
License: MIT
"""

import re
import unicodedata
from typing import List, Optional, Tuple, Callable
from enum import Enum


class Alignment(Enum):
    """Text alignment options."""
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    JUSTIFY = "justify"


class WrapMode(Enum):
    """Text wrapping mode."""
    SOFT = "soft"       # Wrap at word boundaries when possible
    HARD = "hard"       # Wrap exactly at width, breaking words if needed
    FILL = "fill"       # Fill each line as much as possible


# ============================================================================
# Character Classification Utilities
# ============================================================================

def is_cjk_char(char: str) -> bool:
    """
    Check if a character is a CJK (Chinese, Japanese, Korean) character.
    
    Args:
        char: Single character to check
    
    Returns:
        True if character is CJK, False otherwise
    """
    if len(char) != 1:
        return False
    
    code_point = ord(char)
    
    # CJK Unified Ideographs
    if 0x4E00 <= code_point <= 0x9FFF:
        return True
    # CJK Unified Ideographs Extension A
    if 0x3400 <= code_point <= 0x4DBF:
        return True
    # CJK Unified Ideographs Extension B-F
    if 0x20000 <= code_point <= 0x2CEAF:
        return True
    # CJK Compatibility Ideographs
    if 0xF900 <= code_point <= 0xFAFF:
        return True
    # Japanese Hiragana
    if 0x3040 <= code_point <= 0x309F:
        return True
    # Japanese Katakana
    if 0x30A0 <= code_point <= 0x30FF:
        return True
    # Korean Hangul Syllables
    if 0xAC00 <= code_point <= 0xD7AF:
        return True
    # Korean Hangul Jamo
    if 0x1100 <= code_point <= 0x11FF:
        return True
    
    return False


def is_wide_char(char: str) -> bool:
    """
    Check if a character is fullwidth/wide (takes 2 character cells).
    
    Args:
        char: Single character to check
    
    Returns:
        True if character is wide, False otherwise
    """
    if len(char) != 1:
        return False
    
    # CJK characters are wide
    if is_cjk_char(char):
        return True
    
    # Check East Asian Width property
    try:
        width = unicodedata.east_asian_width(char)
        return width in ('F', 'W')  # Fullwidth or Wide
    except Exception:
        return False


def display_width(text: str) -> int:
    """
    Calculate the display width of a string (accounting for wide characters).
    
    Args:
        text: Input string
    
    Returns:
        Display width in character cells
    """
    width = 0
    for char in text:
        if is_wide_char(char):
            width += 2
        elif char == '\t':
            width += 4  # Default tab width
        elif unicodedata.category(char)[0] != 'C':  # Not a control character
            width += 1
    return width


def strip_ansi(text: str) -> str:
    """
    Remove ANSI escape codes from text.
    
    Args:
        text: Text with possible ANSI codes
    
    Returns:
        Text with ANSI codes removed
    """
    ansi_pattern = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]|\x1b\][^\x07]*\x07|\x1b[()][AB012]')
    return ansi_pattern.sub('', text)


def display_width_ansi(text: str) -> int:
    """
    Calculate display width of text, ignoring ANSI escape codes.
    
    Args:
        text: Input text (may contain ANSI codes)
    
    Returns:
        Display width in character cells
    """
    return display_width(strip_ansi(text))


# ============================================================================
# Core Wrapping Functions
# ============================================================================

def _split_words(text: str) -> List[Tuple[str, bool]]:
    """
    Split text into words with their breakability status.
    
    Args:
        text: Input text
    
    Returns:
        List of (word, is_breakable) tuples
    """
    words = []
    current_word = ""
    prev_is_cjk = False
    
    for char in text:
        is_cjk = is_cjk_char(char)
        
        if char.isspace():
            if current_word:
                words.append((current_word, True))
                current_word = ""
            words.append((char, True))
            prev_is_cjk = False
        elif is_cjk:
            # CJK characters can break after them
            if current_word and not prev_is_cjk:
                words.append((current_word, True))
                current_word = ""
            current_word += char
            words.append((current_word, True))
            current_word = ""
            prev_is_cjk = True
        else:
            current_word += char
            prev_is_cjk = False
    
    if current_word:
        words.append((current_word, True))
    
    return words


def wrap_text(
    text: str,
    width: int = 80,
    mode: WrapMode = WrapMode.SOFT,
    break_long_words: bool = True,
    break_on_hyphens: bool = True,
    drop_whitespace: bool = True,
    replace_whitespace: bool = True,
    initial_indent: str = "",
    subsequent_indent: str = "",
    max_lines: Optional[int] = None,
    placeholder: str = "..."
) -> List[str]:
    """
    Wrap text to a specified width.
    
    Args:
        text: Input text to wrap
        width: Maximum line width (default: 80)
        mode: Wrapping mode (soft, hard, fill)
        break_long_words: Break words longer than width
        break_on_hyphens: Break on hyphens
        drop_whitespace: Drop leading/trailing whitespace
        replace_whitespace: Replace tabs/newlines with spaces
        initial_indent: String to indent first line
        subsequent_indent: String to indent subsequent lines
        max_lines: Maximum number of lines (truncate with placeholder if exceeded)
        placeholder: String to append if text is truncated
    
    Returns:
        List of wrapped lines
    """
    if not text:
        return []
    
    # Handle whitespace replacement
    if replace_whitespace:
        text = re.sub(r'\s+', ' ', text)
    
    # Handle initial whitespace
    if drop_whitespace:
        text = text.strip()
    
    # Get display width of indentation
    initial_indent_width = display_width(initial_indent)
    subsequent_indent_width = display_width(subsequent_indent)
    
    # Split text into chunks
    words = _split_words(text)
    
    lines = []
    current_line = ""
    current_width = initial_indent_width
    first_line = True
    
    for word, is_breakable in words:
        # Skip empty words
        if not word:
            continue
        
        word_width = display_width(word)
        
        # Calculate effective width for current line
        indent = initial_indent if first_line else subsequent_indent
        indent_width = initial_indent_width if first_line else subsequent_indent_width
        effective_width = width - indent_width
        
        # Check if word fits on current line
        if not current_line:
            # Starting a new line
            if word_width > effective_width and break_long_words:
                # Word is too long, need to break it
                broken = _break_word(word, effective_width)
                for part in broken:
                    if lines or current_line:
                        lines.append(indent + current_line)
                        current_line = ""
                        current_width = indent_width
                        first_line = False
                        indent = subsequent_indent
                        indent_width = subsequent_indent_width
                        effective_width = width - indent_width
                    current_line = part
                    current_width = indent_width + display_width(part)
            else:
                current_line = word
                current_width = indent_width + word_width
                first_line = True
        elif current_width + 1 + word_width <= effective_width or not is_breakable:
            # Word fits on current line
            if mode != WrapMode.HARD or not current_line.endswith(' '):
                current_line += word if is_cjk_char(word[0]) else (" " if not current_line.endswith(' ') and not is_cjk_char(word[0]) else "") + word
                current_width = indent_width + display_width(current_line)
        else:
            # Word doesn't fit, start new line
            if drop_whitespace:
                current_line = current_line.rstrip()
            
            lines.append(indent + current_line)
            current_line = word
            current_width = subsequent_indent_width + word_width
            first_line = False
            
            # Check max_lines
            if max_lines and len(lines) >= max_lines - 1:
                break
    
    # Add last line
    if current_line and (not max_lines or len(lines) < max_lines):
        indent = initial_indent if first_line else subsequent_indent
        lines.append(indent + current_line)
    
    # Handle max_lines truncation
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        if lines:
            last_line = lines[-1]
            # Truncate and add placeholder
            available_width = width - subsequent_indent_width - display_width(placeholder)
            if available_width > 0:
                truncated = _truncate_to_width(last_line, available_width)
                lines[-1] = truncated + placeholder
    
    return lines


def _break_word(word: str, width: int) -> List[str]:
    """
    Break a word into parts that fit within the given width.
    
    Args:
        word: Word to break
        width: Maximum width for each part
    
    Returns:
        List of word parts
    """
    if width <= 0:
        return [word]
    
    parts = []
    current = ""
    current_width = 0
    
    for char in word:
        char_width = display_width(char)
        if current_width + char_width > width:
            if current:
                parts.append(current)
            current = char
            current_width = char_width
        else:
            current += char
            current_width += char_width
    
    if current:
        parts.append(current)
    
    return parts if parts else [word]


def _truncate_to_width(text: str, width: int) -> str:
    """
    Truncate text to fit within the given display width.
    
    Args:
        text: Text to truncate
        width: Maximum display width
    
    Returns:
        Truncated text
    """
    result = ""
    current_width = 0
    
    for char in text:
        char_width = display_width(char)
        if current_width + char_width > width:
            break
        result += char
        current_width += char_width
    
    return result


# ============================================================================
# Text Alignment Functions
# ============================================================================

def align_text(
    text: str,
    width: int,
    alignment: Alignment = Alignment.LEFT,
    fill_char: str = " "
) -> str:
    """
    Align a single line of text within the given width.
    
    Args:
        text: Text to align
        width: Target width
        alignment: Alignment type (left, right, center, justify)
        fill_char: Character to use for padding
    
    Returns:
        Aligned text
    """
    if not text:
        return fill_char * width
    
    text_width = display_width_ansi(text)
    padding = width - text_width
    
    if padding <= 0:
        return text
    
    if alignment == Alignment.LEFT:
        return text + fill_char * padding
    elif alignment == Alignment.RIGHT:
        return fill_char * padding + text
    elif alignment == Alignment.CENTER:
        left_pad = padding // 2
        right_pad = padding - left_pad
        return fill_char * left_pad + text + fill_char * right_pad
    else:  # JUSTIFY
        return text  # Justification needs multi-line context


def justify_text(
    text: str,
    width: int,
    last_line_align: Alignment = Alignment.LEFT
) -> str:
    """
    Justify text by distributing spaces between words.
    
    Args:
        text: Text to justify
        width: Target width
        last_line_align: How to align the last line
    
    Returns:
        Justified text
    """
    # Strip ANSI for processing but preserve positions
    clean_text = strip_ansi(text)
    
    if display_width(clean_text) >= width:
        return text
    
    # Split into words
    words = clean_text.split()
    
    if len(words) <= 1:
        return align_text(text, width, last_line_align)
    
    # Calculate spaces needed
    total_word_width = sum(display_width(w) for w in words)
    total_spaces = width - total_word_width
    gaps = len(words) - 1
    
    if gaps == 0:
        return align_text(text, width, last_line_align)
    
    # Distribute spaces
    space_per_gap = total_spaces // gaps
    extra_spaces = total_spaces % gaps
    
    result = ""
    for i, word in enumerate(words):
        result += word
        if i < gaps:
            spaces = space_per_gap
            if i < extra_spaces:
                spaces += 1
            result += " " * spaces
    
    # Preserve ANSI codes by re-inserting them
    if text != clean_text:
        # Simple approach: return original if it has ANSI
        return _justify_with_ansi(text, width)
    
    return result


def _justify_with_ansi(text: str, width: int) -> str:
    """
    Justify text that contains ANSI codes.
    
    Args:
        text: Text with ANSI codes
        width: Target width
    
    Returns:
        Justified text
    """
    # Remove ANSI for width calculation
    clean_text = strip_ansi(text)
    
    # Find ANSI code positions and content
    ansi_codes = []
    result = ""
    clean_idx = 0
    i = 0
    
    while i < len(text):
        if text[i] == '\x1b':
            # Start of ANSI sequence
            j = i
            while j < len(text) and text[j] not in 'mABCDEFGHJKSTfilsu':
                j += 1
            if j < len(text):
                j += 1  # Include the final letter
            ansi_codes.append((i, text[i:j]))
            i = j
        else:
            clean_idx += 1
            i += 1
    
    # Justify the clean text
    justified_clean = justify_text(clean_text, width)
    
    # Re-insert ANSI codes
    if not ansi_codes:
        return justified_clean
    
    # Simple approach: prepend ANSI codes to result
    # A more sophisticated approach would track exact positions
    all_codes = "".join(code for _, code in ansi_codes)
    return all_codes + strip_ansi(justified_clean)


# ============================================================================
# High-Level Formatting Functions
# ============================================================================

def wrap_and_align(
    text: str,
    width: int = 80,
    alignment: Alignment = Alignment.LEFT,
    mode: WrapMode = WrapMode.SOFT,
    initial_indent: str = "",
    subsequent_indent: str = "",
    justify_last: bool = False
) -> List[str]:
    """
    Wrap text and align each line.
    
    Args:
        text: Input text
        width: Line width
        alignment: Text alignment
        mode: Wrapping mode
        initial_indent: First line indent
        subsequent_indent: Subsequent lines indent
        justify_last: Justify last line (only when alignment is JUSTIFY)
    
    Returns:
        List of aligned lines
    """
    # Wrap text first
    lines = wrap_text(
        text,
        width=width,
        mode=mode,
        initial_indent=initial_indent,
        subsequent_indent=subsequent_indent
    )
    
    if not lines:
        return []
    
    # Align each line
    aligned_lines = []
    for i, line in enumerate(lines):
        if alignment == Alignment.JUSTIFY:
            is_last = (i == len(lines) - 1)
            if is_last and not justify_last:
                aligned_lines.append(align_text(line, width, Alignment.LEFT))
            else:
                aligned_lines.append(justify_text(line, width))
        else:
            aligned_lines.append(align_text(line, width, alignment))
    
    return aligned_lines


def format_paragraph(
    text: str,
    width: int = 80,
    alignment: Alignment = Alignment.JUSTIFY,
    first_line_indent: int = 0,
    hanging_indent: int = 0,
    line_spacing: int = 1
) -> str:
    """
    Format a paragraph of text.
    
    Args:
        text: Input text
        width: Line width
        alignment: Text alignment
        first_line_indent: Indent for first line (in spaces)
        hanging_indent: Hanging indent for subsequent lines (in spaces)
        line_spacing: Number of blank lines between text lines
    
    Returns:
        Formatted paragraph
    """
    initial_indent = " " * first_line_indent
    subsequent_indent = " " * hanging_indent
    
    lines = wrap_and_align(
        text,
        width=width,
        alignment=alignment,
        initial_indent=initial_indent,
        subsequent_indent=subsequent_indent,
        justify_last=(alignment == Alignment.JUSTIFY)
    )
    
    # Add line spacing
    if line_spacing > 1:
        spacing = "\n" * line_spacing
        lines = spacing.join(lines)
    else:
        lines = "\n".join(lines)
    
    return lines


def dedent_text(text: str) -> str:
    """
    Remove common leading whitespace from all lines.
    
    Args:
        text: Input text
    
    Returns:
        Dedented text
    """
    lines = text.splitlines()
    
    if not lines:
        return ""
    
    # Find minimum indentation
    min_indent = float('inf')
    for line in lines:
        if line.strip():  # Ignore empty lines
            indent = len(line) - len(line.lstrip())
            min_indent = min(min_indent, indent)
    
    if min_indent == float('inf'):
        min_indent = 0
    
    # Remove common indentation
    dedented_lines = []
    for line in lines:
        if len(line) >= min_indent:
            dedented_lines.append(line[min_indent:])
        else:
            dedented_lines.append(line)
    
    return "\n".join(dedented_lines)


def indent_text(
    text: str,
    prefix: str = "    ",
    skip_empty: bool = True,
    skip_first: bool = False
) -> str:
    """
    Add indentation prefix to all lines.
    
    Args:
        text: Input text
        prefix: Indentation string
        skip_empty: Skip empty lines
        skip_first: Skip first line
    
    Returns:
        Indented text
    """
    lines = text.splitlines()
    result = []
    
    for i, line in enumerate(lines):
        if skip_first and i == 0:
            result.append(line)
        elif skip_empty and not line.strip():
            result.append(line)
        else:
            result.append(prefix + line)
    
    return "\n".join(result)


def center_block(
    text: str,
    width: int = 80,
    fill_char: str = " "
) -> str:
    """
    Center a block of text.
    
    Args:
        text: Input text (may contain multiple lines)
        width: Target width
        fill_char: Character for padding
    
    Returns:
        Centered text block
    """
    lines = text.splitlines()
    max_line_width = max(display_width_ansi(line) for line in lines) if lines else 0
    
    result = []
    for line in lines:
        line_width = display_width_ansi(line)
        if line_width < width:
            left_pad = (width - line_width) // 2
            right_pad = width - line_width - left_pad
            centered = fill_char * left_pad + line + fill_char * right_pad
            result.append(centered)
        else:
            result.append(line)
    
    return "\n".join(result)


def fill_text(
    text: str,
    width: int = 80,
    initial_indent: str = "",
    subsequent_indent: str = "",
    preserve_paragraphs: bool = True,
    paragraph_separator: str = "\n\n"
) -> str:
    """
    Fill and wrap text, optionally preserving paragraph breaks.
    
    Args:
        text: Input text
        width: Maximum line width
        initial_indent: String for first line indent
        subsequent_indent: String for subsequent line indent
        preserve_paragraphs: Preserve paragraph breaks
        paragraph_separator: String that separates paragraphs
    
    Returns:
        Filled text
    """
    if preserve_paragraphs:
        paragraphs = text.split(paragraph_separator)
        filled_paragraphs = []
        
        for para in paragraphs:
            para = para.strip()
            if para:
                lines = wrap_text(
                    para,
                    width=width,
                    initial_indent=initial_indent,
                    subsequent_indent=subsequent_indent
                )
                filled_paragraphs.append("\n".join(lines))
        
        return paragraph_separator.join(filled_paragraphs)
    else:
        lines = wrap_text(
            text,
            width=width,
            initial_indent=initial_indent,
            subsequent_indent=subsequent_indent
        )
        return "\n".join(lines)


def shorten_text(
    text: str,
    width: int,
    placeholder: str = "...",
    break_word: bool = False
) -> str:
    """
    Shorten text to fit within a given width.
    
    Args:
        text: Input text
        width: Maximum width
        placeholder: String to append when truncated
        break_word: Break words if necessary
    
    Returns:
        Shortened text
    """
    if display_width_ansi(text) <= width:
        return text
    
    placeholder_width = display_width(placeholder)
    available = width - placeholder_width
    
    if available <= 0:
        return placeholder[:width] if break_word else placeholder
    
    # Truncate text
    result = _truncate_to_width(text, available)
    
    return result + placeholder


def split_lines_aware(text: str, width: int) -> List[str]:
    """
    Split text into lines that fit within the given width,
    preserving existing line breaks when possible.
    
    Args:
        text: Input text
        width: Maximum line width
    
    Returns:
        List of lines
    """
    result = []
    
    # Split by existing line breaks
    paragraphs = text.split('\n')
    
    for para in paragraphs:
        if display_width_ansi(para) <= width:
            result.append(para)
        else:
            # Wrap the paragraph
            wrapped = wrap_text(para, width=width)
            result.extend(wrapped)
    
    return result


# ============================================================================
# Utility Classes
# ============================================================================

class TextWrapper:
    """
    A configurable text wrapper with object-oriented interface.
    """
    
    def __init__(
        self,
        width: int = 80,
        alignment: Alignment = Alignment.LEFT,
        mode: WrapMode = WrapMode.SOFT,
        initial_indent: str = "",
        subsequent_indent: str = "",
        break_long_words: bool = True,
        break_on_hyphens: bool = True,
        drop_whitespace: bool = True,
        replace_whitespace: bool = True,
        max_lines: Optional[int] = None,
        placeholder: str = "..."
    ):
        """
        Initialize the text wrapper.
        
        Args:
            width: Maximum line width
            alignment: Text alignment
            mode: Wrapping mode
            initial_indent: First line indent
            subsequent_indent: Subsequent line indent
            break_long_words: Break words longer than width
            break_on_hyphens: Break on hyphens
            drop_whitespace: Drop leading/trailing whitespace
            replace_whitespace: Replace tabs/newlines with spaces
            max_lines: Maximum number of lines
            placeholder: Placeholder for truncated text
        """
        self.width = width
        self.alignment = alignment
        self.mode = mode
        self.initial_indent = initial_indent
        self.subsequent_indent = subsequent_indent
        self.break_long_words = break_long_words
        self.break_on_hyphens = break_on_hyphens
        self.drop_whitespace = drop_whitespace
        self.replace_whitespace = replace_whitespace
        self.max_lines = max_lines
        self.placeholder = placeholder
    
    def wrap(self, text: str) -> List[str]:
        """
        Wrap text to lines.
        
        Args:
            text: Input text
        
        Returns:
            List of wrapped lines
        """
        return wrap_text(
            text,
            width=self.width,
            mode=self.mode,
            break_long_words=self.break_long_words,
            break_on_hyphens=self.break_on_hyphens,
            drop_whitespace=self.drop_whitespace,
            replace_whitespace=self.replace_whitespace,
            initial_indent=self.initial_indent,
            subsequent_indent=self.subsequent_indent,
            max_lines=self.max_lines,
            placeholder=self.placeholder
        )
    
    def fill(self, text: str) -> str:
        """
        Wrap text and return as a single string.
        
        Args:
            text: Input text
        
        Returns:
            Wrapped text as string
        """
        return "\n".join(self.wrap(text))
    
    def wrap_and_align(self, text: str) -> List[str]:
        """
        Wrap and align text.
        
        Args:
            text: Input text
        
        Returns:
            List of aligned lines
        """
        return wrap_and_align(
            text,
            width=self.width,
            alignment=self.alignment,
            mode=self.mode,
            initial_indent=self.initial_indent,
            subsequent_indent=self.subsequent_indent
        )


# ============================================================================
# Convenience Functions
# ============================================================================

def wrap(text: str, width: int = 80) -> List[str]:
    """Convenience function for basic text wrapping."""
    return wrap_text(text, width=width)


def fill(text: str, width: int = 80) -> str:
    """Convenience function for text filling."""
    return fill_text(text, width=width)


def center(text: str, width: int = 80) -> str:
    """Convenience function for centering text."""
    return align_text(text, width, Alignment.CENTER)


def left_align(text: str, width: int = 80) -> str:
    """Convenience function for left alignment."""
    return align_text(text, width, Alignment.LEFT)


def right_align(text: str, width: int = 80) -> str:
    """Convenience function for right alignment."""
    return align_text(text, width, Alignment.RIGHT)


def justify(text: str, width: int = 80) -> str:
    """Convenience function for text justification."""
    return justify_text(text, width)


def shorten(text: str, width: int, placeholder: str = "...") -> str:
    """Convenience function for text shortening."""
    return shorten_text(text, width, placeholder)


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    # Demo
    print("=" * 60)
    print("Text Wrap Utilities Demo")
    print("=" * 60)
    
    # Test text wrapping
    sample_text = (
        "This is a sample text that demonstrates the text wrapping "
        "capabilities of this utility module. It handles long words "
        "like 'supercalifragilisticexpialidocious' and various "
        "formatting options."
    )
    
    print("\n1. Basic Text Wrapping (width=40):")
    print("-" * 40)
    lines = wrap_text(sample_text, width=40)
    for line in lines:
        print(line)
    
    print("\n2. Justified Text:")
    print("-" * 40)
    lines = wrap_and_align(sample_text, width=40, alignment=Alignment.JUSTIFY)
    for line in lines:
        print(line)
    
    print("\n3. Centered Text:")
    print("-" * 40)
    for line in wrap_text(sample_text[:50], width=40):
        print(center(line, 40))
    
    print("\n4. Right-Aligned Text:")
    print("-" * 40)
    for line in wrap_text(sample_text[:50], width=40):
        print(right_align(line, 40))
    
    print("\n5. Indented Paragraph:")
    print("-" * 40)
    para = format_paragraph(
        sample_text,
        width=50,
        alignment=Alignment.JUSTIFY,
        first_line_indent=4,
        hanging_indent=2
    )
    print(para)
    
    print("\n6. Text Shortening:")
    print("-" * 40)
    print(f"Original: {sample_text[:60]}...")
    print(f"Shortened: {shorten_text(sample_text, 50)}")
    
    print("\n7. CJK Text Support:")
    print("-" * 40)
    cjk_text = "这是一个测试文本，用于演示中文字符的处理能力。文字会自动换行，并且正确计算字符宽度。"
    lines = wrap_text(cjk_text, width=30)
    for line in lines:
        print(f"|{line}|")
    
    print("\n8. TextWrapper Class:")
    print("-" * 40)
    wrapper = TextWrapper(width=35, initial_indent="> ", subsequent_indent="  ")
    filled = wrapper.fill(sample_text)
    print(filled)
    
    print("\n" + "=" * 60)
    print("Demo Complete!")