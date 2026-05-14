"""
AllToolkit - Python Text Diff Utilities

A zero-dependency, production-ready text comparison and diff utility module.
Supports line-level diff, character-level diff, similarity calculation, and unified diff output.

Author: AllToolkit
License: MIT
"""

from typing import List, Tuple, Optional, NamedTuple
from enum import Enum
import re


class DiffOperation(Enum):
    """Diff operation types."""
    EQUAL = " "
    INSERT = "+"
    DELETE = "-"
    REPLACE = "~"


class DiffBlock(NamedTuple):
    """A single diff block containing operation and text."""
    operation: DiffOperation
    text: str


class TextDiffUtils:
    """
    Text diff and comparison utilities.
    
    Provides functions for:
    - Line-level diff comparison
    - Character-level diff comparison
    - Similarity calculation (Levenshtein distance, ratio)
    - Unified diff format output
    - Diff highlighting
    - Longest Common Subsequence (LCS)
    """

    @staticmethod
    def lcs(text1: str, text2: str) -> str:
        """
        Find the Longest Common Subsequence of two strings.
        
        Args:
            text1: First text string
            text2: Second text string
            
        Returns:
            The longest common subsequence string
            
        Example:
            >>> TextDiffUtils.lcs("ABCBDAB", "BDCABA")
            'BCBA'
        """
        m, n = len(text1), len(text2)
        
        # Build LCS table
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        # Backtrack to find the LCS string
        lcs_chars = []
        i, j = m, n
        while i > 0 and j > 0:
            if text1[i - 1] == text2[j - 1]:
                lcs_chars.append(text1[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1
        
        return ''.join(reversed(lcs_chars))

    @staticmethod
    def lcs_length(text1: str, text2: str) -> int:
        """
        Calculate the length of the Longest Common Subsequence.
        
        Args:
            text1: First text string
            text2: Second text string
            
        Returns:
            Length of the LCS
            
        Example:
            >>> TextDiffUtils.lcs_length("ABCBDAB", "BDCABA")
            4
        """
        m, n = len(text1), len(text2)
        
        # Space-optimized DP - only keep two rows
        prev = [0] * (n + 1)
        curr = [0] * (n + 1)
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    curr[j] = prev[j - 1] + 1
                else:
                    curr[j] = max(prev[j], curr[j - 1])
            prev, curr = curr, prev
        
        return prev[n]

    @staticmethod
    def levenshtein_distance(text1: str, text2: str) -> int:
        """
        Calculate the Levenshtein (edit) distance between two strings.
        
        The minimum number of single-character edits (insertions, deletions,
        or substitutions) required to change one string into another.
        
        Args:
            text1: First text string
            text2: Second text string
            
        Returns:
            The edit distance
            
        Example:
            >>> TextDiffUtils.levenshtein_distance("kitten", "sitting")
            3
        """
        m, n = len(text1), len(text2)
        
        # Edge cases
        if m == 0:
            return n
        if n == 0:
            return m
        
        # Space-optimized DP - only keep two rows
        prev = list(range(n + 1))
        curr = [0] * (n + 1)
        
        for i in range(1, m + 1):
            curr[0] = i
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    curr[j] = prev[j - 1]
                else:
                    curr[j] = 1 + min(
                        prev[j],      # deletion
                        curr[j - 1],  # insertion
                        prev[j - 1]   # substitution
                    )
            prev, curr = curr, prev
        
        return prev[n]

    @staticmethod
    def similarity_ratio(text1: str, text2: str) -> float:
        """
        Calculate the similarity ratio between two strings (0.0 to 1.0).
        
        Based on Levenshtein distance. 1.0 means identical, 0.0 means completely different.
        
        Args:
            text1: First text string
            text2: Second text string
            
        Returns:
            Similarity ratio between 0.0 and 1.0
            
        Example:
            >>> TextDiffUtils.similarity_ratio("hello world", "hello earth")
            0.5454545454545454
        """
        if not text1 and not text2:
            return 1.0
        
        total_len = len(text1) + len(text2)
        if total_len == 0:
            return 1.0
        
        distance = TextDiffUtils.levenshtein_distance(text1, text2)
        return (total_len - distance) / total_len

    @staticmethod
    def jaccard_similarity(text1: str, text2: str, ngram: int = 2) -> float:
        """
        Calculate Jaccard similarity coefficient based on n-grams.
        
        Args:
            text1: First text string
            text2: Second text string
            ngram: N-gram size (default: 2 for bigrams)
            
        Returns:
            Jaccard similarity coefficient between 0.0 and 1.0
            
        Example:
            >>> TextDiffUtils.jaccard_similarity("hello", "hallo")
            0.5
        """
        if ngram < 1:
            raise ValueError("ngram must be at least 1")
        
        def get_ngrams(text: str, n: int) -> set:
            if len(text) < n:
                return {text} if text else set()
            return {text[i:i+n] for i in range(len(text) - n + 1)}
        
        set1 = get_ngrams(text1, ngram)
        set2 = get_ngrams(text2, ngram)
        
        if not set1 and not set2:
            return 1.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0

    @staticmethod
    def diff_chars(text1: str, text2: str) -> List[DiffBlock]:
        """
        Compute character-level diff between two strings.
        
        Uses a modified LCS algorithm to identify insertions, deletions,
        and unchanged characters.
        
        Args:
            text1: Original text
            text2: Modified text
            
        Returns:
            List of DiffBlock objects representing the diff
            
        Example:
            >>> TextDiffUtils.diff_chars("hello", "hallo")
            [DiffBlock(operation=DiffOperation.EQUAL, text='h'),
             DiffBlock(operation=DiffOperation.DELETE, text='e'),
             DiffBlock(operation=DiffOperation.INSERT, text='a'),
             DiffBlock(operation=DiffOperation.EQUAL, text='llo')]
        """
        m, n = len(text1), len(text2)
        
        # Build DP table for LCS
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        # Backtrack to build diff
        diff_blocks = []
        i, j = m, n
        
        while i > 0 or j > 0:
            if i > 0 and j > 0 and text1[i - 1] == text2[j - 1]:
                # Equal character
                diff_blocks.append(DiffBlock(DiffOperation.EQUAL, text1[i - 1]))
                i -= 1
                j -= 1
            elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
                # Insert in text2
                diff_blocks.append(DiffBlock(DiffOperation.INSERT, text2[j - 1]))
                j -= 1
            else:
                # Delete from text1
                diff_blocks.append(DiffBlock(DiffOperation.DELETE, text1[i - 1]))
                i -= 1
        
        # Reverse and merge adjacent blocks with same operation
        diff_blocks.reverse()
        
        merged = []
        for block in diff_blocks:
            if merged and merged[-1].operation == block.operation:
                merged[-1] = DiffBlock(block.operation, merged[-1].text + block.text)
            else:
                merged.append(block)
        
        return merged

    @staticmethod
    def diff_lines(text1: str, text2: str) -> List[DiffBlock]:
        """
        Compute line-level diff between two texts.
        
        Args:
            text1: Original text
            text2: Modified text
            
        Returns:
            List of DiffBlock objects representing line-level changes
            
        Example:
            >>> TextDiffUtils.diff_lines("a\\nb\\nc", "a\\nx\\nc")
            [DiffBlock(operation=DiffOperation.EQUAL, text='a\\n'),
             DiffBlock(operation=DiffOperation.DELETE, text='b\\n'),
             DiffBlock(operation=DiffOperation.INSERT, text='x\\n'),
             DiffBlock(operation=DiffOperation.EQUAL, text='c')]
        """
        lines1 = text1.splitlines(keepends=True)
        lines2 = text2.splitlines(keepends=True)
        
        # Ensure lines end with newline for comparison
        lines1 = [line if line.endswith('\n') else line + '\n' for line in lines1] if lines1 and not text1.endswith('\n') else lines1
        lines2 = [line if line.endswith('\n') else line + '\n' for line in lines2] if lines2 and not text2.endswith('\n') else lines2
        
        m, n = len(lines1), len(lines2)
        
        # Build DP table for LCS
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if lines1[i - 1] == lines2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        # Backtrack to build diff
        diff_blocks = []
        i, j = m, n
        
        while i > 0 or j > 0:
            if i > 0 and j > 0 and lines1[i - 1] == lines2[j - 1]:
                diff_blocks.append(DiffBlock(DiffOperation.EQUAL, lines1[i - 1]))
                i -= 1
                j -= 1
            elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
                diff_blocks.append(DiffBlock(DiffOperation.INSERT, lines2[j - 1]))
                j -= 1
            else:
                diff_blocks.append(DiffBlock(DiffOperation.DELETE, lines1[i - 1]))
                i -= 1
        
        diff_blocks.reverse()
        
        # Merge adjacent blocks with same operation
        merged = []
        for block in diff_blocks:
            if merged and merged[-1].operation == block.operation:
                merged[-1] = DiffBlock(block.operation, merged[-1].text + block.text)
            else:
                merged.append(block)
        
        return merged

    @staticmethod
    def unified_diff(text1: str, text2: str, 
                      filename1: str = "original", 
                      filename2: str = "modified",
                      context_lines: int = 3) -> str:
        """
        Generate unified diff format output.
        
        Args:
            text1: Original text
            text2: Modified text
            filename1: Original filename (default: "original")
            filename2: Modified filename (default: "modified")
            context_lines: Number of context lines around changes (default: 3)
            
        Returns:
            Unified diff string in standard format
            
        Example:
            >>> diff = TextDiffUtils.unified_diff("a\\nb\\nc", "a\\nx\\nc")
            >>> print(diff)
            --- original
            +++ modified
            @@ -1,3 +1,3 @@
             a
            -b
            +x
             c
        """
        lines1 = text1.splitlines()
        lines2 = text2.splitlines()
        
        # Build line diff using LCS
        m, n = len(lines1), len(lines2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if lines1[i - 1] == lines2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        # Build diff sequence
        diff = []
        i, j = m, n
        while i > 0 or j > 0:
            if i > 0 and j > 0 and lines1[i - 1] == lines2[j - 1]:
                diff.append((' ', lines1[i - 1]))
                i -= 1
                j -= 1
            elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
                diff.append(('+', lines2[j - 1]))
                j -= 1
            else:
                diff.append(('-', lines1[i - 1]))
                i -= 1
        
        diff.reverse()
        
        # Build unified diff output
        result = []
        result.append(f"--- {filename1}")
        result.append(f"+++ {filename2}")
        
        # Find change hunks
        if not diff:
            return '\n'.join(result) + '\n'
        
        # Group into hunks
        hunks = []
        hunk_start = None
        hunk_lines = []
        context_before = []
        
        for idx, (op, line) in enumerate(diff):
            if op != ' ':
                # Change detected
                if hunk_start is None:
                    # Find start line number (1-indexed)
                    unchanged_before = sum(1 for i in range(idx) if diff[i][0] == ' ')
                    hunk_start = unchanged_before + 1
                
                # Add context
                context_before_idx = idx - context_lines
                for i in range(max(0, context_before_idx - len(context_before)), idx):
                    if i >= 0 and diff[i][0] == ' ' and (hunk_start is None or i not in [h['idx'] for h in hunks]):
                        context_before.append((i, diff[i]))
                
                hunk_lines.append((op, line))
            elif hunk_start is not None:
                hunk_lines.append((op, line))
        
        # Build hunks from diff
        hunks_data = []
        i = 0
        while i < len(diff):
            if diff[i][0] != ' ':
                # Start of a change
                start = max(0, i - context_lines)
                end = min(len(diff), i + 1)
                
                # Extend to end of change
                while end < len(diff) and diff[end][0] != ' ':
                    end += 1
                # Add context after
                while end < len(diff) and end - i < context_lines + 1:
                    if diff[end][0] != ' ':
                        while end < len(diff) and diff[end][0] != ' ':
                            end += 1
                    else:
                        end += 1
                
                hunk = diff[start:end]
                hunks_data.append((start, hunk))
                i = end
            else:
                i += 1
        
        # Generate output for each hunk
        for hunk_idx, (start_offset, hunk) in enumerate(hunks_data):
            # Calculate line numbers
            orig_start = sum(1 for i in range(start_offset) if diff[i][0] != '+') + 1
            mod_start = sum(1 for i in range(start_offset) if diff[i][0] != '-') + 1
            
            orig_count = sum(1 for op, _ in hunk if op != '+')
            mod_count = sum(1 for op, _ in hunk if op != '-')
            
            result.append(f"@@ -{orig_start},{orig_count} +{mod_start},{mod_count} @@")
            
            for op, line in hunk:
                result.append(f"{op}{line}")
        
        return '\n'.join(result) + '\n'

    @staticmethod
    def highlight_diff(diff_blocks: List[DiffBlock], 
                       color_insert: str = "\033[32m",
                       color_delete: str = "\033[31m",
                       color_equal: str = "\033[0m",
                       color_reset: str = "\033[0m") -> str:
        """
        Highlight diff output with ANSI color codes.
        
        Args:
            diff_blocks: List of DiffBlock objects
            color_insert: ANSI color for insertions (default: green)
            color_delete: ANSI color for deletions (default: red)
            color_equal: ANSI color for unchanged text (default: reset)
            color_reset: ANSI reset code
            
        Returns:
            Colorized string for terminal output
            
        Example:
            >>> diff = TextDiffUtils.diff_chars("hello", "hallo")
            >>> print(TextDiffUtils.highlight_diff(diff))
        """
        colors = {
            DiffOperation.INSERT: color_insert,
            DiffOperation.DELETE: color_delete,
            DiffOperation.EQUAL: color_equal,
        }
        
        result = []
        for block in diff_blocks:
            color = colors.get(block.operation, color_reset)
            result.append(f"{color}{block.text}{color_reset}")
        
        return ''.join(result)

    @staticmethod
    def html_diff(diff_blocks: List[DiffBlock],
                  insert_class: str = "diff-insert",
                  delete_class: str = "diff-delete",
                  equal_class: str = "diff-equal") -> str:
        """
        Generate HTML diff output with CSS classes.
        
        Args:
            diff_blocks: List of DiffBlock objects
            insert_class: CSS class for insertions
            delete_class: CSS class for deletions
            equal_class: CSS class for unchanged text
            
        Returns:
            HTML string with spans for styling
            
        Example:
            >>> diff = TextDiffUtils.diff_chars("hello", "hallo")
            >>> html = TextDiffUtils.html_diff(diff)
        """
        import html
        
        classes = {
            DiffOperation.INSERT: insert_class,
            DiffOperation.DELETE: delete_class,
            DiffOperation.EQUAL: equal_class,
        }
        
        result = []
        for block in diff_blocks:
            css_class = classes.get(block.operation, equal_class)
            escaped_text = html.escape(block.text)
            result.append(f'<span class="{css_class}">{escaped_text}</span>')
        
        return ''.join(result)

    @staticmethod
    def diff_stats(diff_blocks: List[DiffBlock]) -> dict:
        """
        Calculate statistics from diff blocks.
        
        Args:
            diff_blocks: List of DiffBlock objects
            
        Returns:
            Dictionary with counts and statistics
            
        Example:
            >>> diff = TextDiffUtils.diff_chars("hello", "hallo")
            >>> TextDiffUtils.diff_stats(diff)
            {'insertions': 1, 'deletions': 1, 'unchanged': 4, 'total': 6}
        """
        stats = {
            'insertions': 0,
            'deletions': 0,
            'unchanged': 0,
            'total': 0
        }
        
        for block in diff_blocks:
            length = len(block.text)
            stats['total'] += length
            
            if block.operation == DiffOperation.INSERT:
                stats['insertions'] += length
            elif block.operation == DiffOperation.DELETE:
                stats['deletions'] += length
            else:
                stats['unchanged'] += length
        
        return stats

    @staticmethod
    def side_by_side(text1: str, text2: str, 
                     width: int = 50,
                     separator: str = " | ") -> str:
        """
        Generate side-by-side comparison of two texts.
        
        Args:
            text1: Left text
            text2: Right text
            width: Column width for each side (default: 50)
            separator: Separator between columns (default: " | ")
            
        Returns:
            Side-by-side formatted string
            
        Example:
            >>> print(TextDiffUtils.side_by_side("Hello", "World"))
        """
        lines1 = text1.splitlines()
        lines2 = text2.splitlines()
        
        max_lines = max(len(lines1), len(lines2))
        
        result = []
        for i in range(max_lines):
            left = lines1[i] if i < len(lines1) else ""
            right = lines2[i] if i < len(lines2) else ""
            
            # Truncate if too long
            left = left[:width].ljust(width)
            right = right[:width].ljust(width)
            
            result.append(f"{left}{separator}{right}")
        
        return '\n'.join(result)

    @staticmethod
    def find_changes(text1: str, text2: str, 
                     threshold: float = 0.5) -> List[Tuple[int, int, str, str]]:
        """
        Find specific changed regions between two texts.
        
        Args:
            text1: Original text
            text2: Modified text
            threshold: Similarity threshold for grouping changes (default: 0.5)
            
        Returns:
            List of (start_pos, end_pos, deleted_text, inserted_text)
            
        Example:
            >>> TextDiffUtils.find_changes("hello world", "hello there")
            [(6, 11, 'world', 'there')]
        """
        diff_blocks = TextDiffUtils.diff_chars(text1, text2)
        
        changes = []
        current_change = None
        pos = 0
        
        for block in diff_blocks:
            if block.operation == DiffOperation.EQUAL:
                if current_change:
                    start, deleted, inserted = current_change
                    changes.append((start, pos, deleted, inserted))
                    current_change = None
                pos += len(block.text)
            elif block.operation == DiffOperation.DELETE:
                if not current_change:
                    current_change = (pos, "", "")
                deleted, inserted = current_change[1], current_change[2]
                current_change = (current_change[0], deleted + block.text, inserted)
            elif block.operation == DiffOperation.INSERT:
                if not current_change:
                    current_change = (pos, "", "")
                deleted, inserted = current_change[1], current_change[2]
                current_change = (current_change[0], deleted, inserted + block.text)
        
        if current_change:
            start, deleted, inserted = current_change
            changes.append((start, pos, deleted, inserted))
        
        return changes


# Convenience functions for direct import

def lcs(text1: str, text2: str) -> str:
    """Find the Longest Common Subsequence of two strings."""
    return TextDiffUtils.lcs(text1, text2)


def lcs_length(text1: str, text2: str) -> int:
    """Calculate the length of the Longest Common Subsequence."""
    return TextDiffUtils.lcs_length(text1, text2)


def levenshtein_distance(text1: str, text2: str) -> int:
    """Calculate the Levenshtein (edit) distance between two strings."""
    return TextDiffUtils.levenshtein_distance(text1, text2)


def similarity_ratio(text1: str, text2: str) -> float:
    """Calculate the similarity ratio between two strings (0.0 to 1.0)."""
    return TextDiffUtils.similarity_ratio(text1, text2)


def jaccard_similarity(text1: str, text2: str, ngram: int = 2) -> float:
    """Calculate Jaccard similarity coefficient based on n-grams."""
    return TextDiffUtils.jaccard_similarity(text1, text2, ngram)


def diff_chars(text1: str, text2: str) -> List[DiffBlock]:
    """Compute character-level diff between two strings."""
    return TextDiffUtils.diff_chars(text1, text2)


def diff_lines(text1: str, text2: str) -> List[DiffBlock]:
    """Compute line-level diff between two texts."""
    return TextDiffUtils.diff_lines(text1, text2)


def unified_diff(text1: str, text2: str, 
                 filename1: str = "original", 
                 filename2: str = "modified",
                 context_lines: int = 3) -> str:
    """Generate unified diff format output."""
    return TextDiffUtils.unified_diff(text1, text2, filename1, filename2, context_lines)


def highlight_diff(diff_blocks: List[DiffBlock], 
                   color_insert: str = "\033[32m",
                   color_delete: str = "\033[31m",
                   color_equal: str = "\033[0m",
                   color_reset: str = "\033[0m") -> str:
    """Highlight diff output with ANSI color codes."""
    return TextDiffUtils.highlight_diff(diff_blocks, color_insert, color_delete, color_equal, color_reset)


def html_diff(diff_blocks: List[DiffBlock],
              insert_class: str = "diff-insert",
              delete_class: str = "diff-delete",
              equal_class: str = "diff-equal") -> str:
    """Generate HTML diff output with CSS classes."""
    return TextDiffUtils.html_diff(diff_blocks, insert_class, delete_class, equal_class)


def diff_stats(diff_blocks: List[DiffBlock]) -> dict:
    """Calculate statistics from diff blocks."""
    return TextDiffUtils.diff_stats(diff_blocks)


def side_by_side(text1: str, text2: str, width: int = 50, separator: str = " | ") -> str:
    """Generate side-by-side comparison of two texts."""
    return TextDiffUtils.side_by_side(text1, text2, width, separator)


def find_changes(text1: str, text2: str, threshold: float = 0.5) -> List[Tuple[int, int, str, str]]:
    """Find specific changed regions between two texts."""
    return TextDiffUtils.find_changes(text1, text2, threshold)