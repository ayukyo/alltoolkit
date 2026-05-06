"""
Gap Buffer - Text Editor Data Structure

A gap buffer is a dynamic array with a "gap" (empty space) that allows
efficient insertions and deletions at the cursor position. This makes it
ideal for text editors where most edits occur near the cursor.

Time Complexity:
- Insert at cursor: O(1) amortized
- Delete at cursor: O(1)
- Move cursor: O(k) where k is distance moved
- Random access: O(1)

Space Complexity: O(n) where n is buffer size including gap
"""

from typing import Optional, List, Tuple, Iterator
from copy import deepcopy


class GapBuffer:
    """
    A gap buffer implementation optimized for text editing operations.
    
    The buffer consists of:
    - Pre-gap content: characters before the cursor
    - Gap: empty space for insertions
    - Post-gap content: characters after the cursor
    
    Example:
        "Hello|World" with cursor at position 5
        
        Buffer: ['H','e','l','l','o','_','_','_','W','o','r','l','d']
                        pre-gap      gap      post-gap
    """
    
    def __init__(self, initial_capacity: int = 256, text: str = ""):
        """
        Initialize a gap buffer.
        
        Args:
            initial_capacity: Initial size of the buffer (default 256)
            text: Initial text content
        """
        if initial_capacity < 16:
            initial_capacity = 16
        
        self._buffer: List[str] = [''] * initial_capacity
        self._gap_start = 0
        self._gap_end = initial_capacity
        self._cursor = 0  # Cursor position (same as gap_start)
        self._length = 0  # Length of actual content
        
        if text:
            self.insert(text)
    
    @property
    def cursor(self) -> int:
        """Current cursor position (0-indexed)."""
        return self._cursor
    
    @property
    def length(self) -> int:
        """Length of actual text content."""
        return self._length
    
    @property
    def capacity(self) -> int:
        """Total buffer capacity including gap."""
        return len(self._buffer)
    
    @property
    def gap_size(self) -> int:
        """Current size of the gap."""
        return self._gap_end - self._gap_start
    
    def _ensure_gap_size(self, required: int) -> None:
        """Ensure gap is large enough, expanding if necessary."""
        if self.gap_size >= required:
            return
        
        # Calculate new capacity
        new_capacity = max(self.capacity * 2, self._length + required + 256)
        new_buffer = [''] * new_capacity
        new_gap_size = new_capacity - self._length
        
        # Copy pre-gap content
        new_buffer[0:self._gap_start] = self._buffer[0:self._gap_start]
        
        # Copy post-gap content to new position
        post_start = self._gap_end
        post_end = self.capacity
        new_post_start = self._gap_start + new_gap_size
        new_buffer[new_post_start:new_post_start + (post_end - post_start)] = \
            self._buffer[post_start:post_end]
        
        self._buffer = new_buffer
        self._gap_end = new_post_start
    
    def _move_gap_to_cursor(self, position: int) -> None:
        """Move gap to the specified position."""
        if position < 0:
            position = 0
        elif position > self._length:
            position = self._length
        
        if position == self._gap_start:
            return
        
        gap_len = self.gap_size
        
        if position < self._gap_start:
            # Move gap left: copy characters from left of gap to right of gap
            # [AAA][gap][BBB] -> cursor at 1 -> [A][gap][AABBB]
            chars_to_move = self._gap_start - position
            self._buffer[self._gap_end - chars_to_move:self._gap_end] = \
                self._buffer[position:self._gap_start]
            self._gap_start = position
            self._gap_end = self._gap_start + gap_len
        else:
            # Move gap right: copy characters from right of gap to left of gap
            # [AAA][gap][BBB] -> cursor at 5 -> [AAABB][gap][B]
            chars_to_move = position - self._gap_start
            self._buffer[self._gap_start:self._gap_start + chars_to_move] = \
                self._buffer[self._gap_end:self._gap_end + chars_to_move]
            self._gap_start = position
            self._gap_end = self._gap_start + gap_len
        
        self._cursor = self._gap_start
    
    def move_cursor(self, position: int) -> None:
        """
        Move cursor to specified position.
        
        Args:
            position: Target position (0-indexed)
        """
        self._move_gap_to_cursor(position)
    
    def move_cursor_relative(self, offset: int) -> int:
        """
        Move cursor relative to current position.
        
        Args:
            offset: Number of characters to move (positive = right, negative = left)
            
        Returns:
            New cursor position
        """
        new_pos = self._cursor + offset
        self.move_cursor(new_pos)
        return self._cursor
    
    def insert(self, text: str) -> None:
        """
        Insert text at cursor position.
        
        Args:
            text: Text to insert
        """
        if not text:
            return
        
        text_len = len(text)
        self._ensure_gap_size(text_len)
        
        # Insert characters into gap
        for i, char in enumerate(text):
            self._buffer[self._gap_start + i] = char
        
        self._gap_start += text_len
        self._cursor = self._gap_start
        self._length += text_len
    
    def delete(self, count: int = 1) -> str:
        """
        Delete characters at cursor position.
        
        Args:
            count: Number of characters to delete (positive = forward, negative = backward)
            
        Returns:
            Deleted text
        """
        if count == 0:
            return ""
        
        if count > 0:
            # Delete forward (characters after cursor)
            if self._gap_end >= self.capacity:
                return ""
            
            actual_count = min(count, self.capacity - self._gap_end)
            deleted = ''.join(self._buffer[self._gap_end:self._gap_end + actual_count])
            self._gap_end += actual_count
            self._length -= actual_count
            return deleted
        else:
            # Delete backward (characters before cursor)
            actual_count = min(-count, self._gap_start)
            start_pos = self._gap_start - actual_count
            deleted = ''.join(self._buffer[start_pos:self._gap_start])
            self._gap_start = start_pos
            self._cursor = self._gap_start
            self._length -= actual_count
            return deleted
    
    def backspace(self, count: int = 1) -> str:
        """
        Delete characters before cursor (backspace).
        
        Args:
            count: Number of characters to delete
            
        Returns:
            Deleted text
        """
        return self.delete(-count)
    
    def get_text(self) -> str:
        """Get the full text content."""
        pre_gap = ''.join(self._buffer[0:self._gap_start])
        post_gap = ''.join(self._buffer[self._gap_end:self.capacity])
        return pre_gap + post_gap
    
    def __str__(self) -> str:
        return self.get_text()
    
    def __repr__(self) -> str:
        return f"GapBuffer(length={self._length}, cursor={self._cursor}, gap_size={self.gap_size})"
    
    def __len__(self) -> int:
        return self._length
    
    def __getitem__(self, index: int) -> str:
        """Get character at index."""
        if index < 0:
            index += self._length
        if index < 0 or index >= self._length:
            raise IndexError(f"Index {index} out of range")
        
        if index < self._gap_start:
            return self._buffer[index]
        else:
            return self._buffer[self._gap_end + (index - self._gap_start)]
    
    def __contains__(self, text: str) -> bool:
        """Check if text is contained in buffer."""
        return text in self.get_text()
    
    def __iter__(self) -> Iterator[str]:
        """Iterate over characters."""
        for i in range(self._length):
            yield self[i]
    
    def get_slice(self, start: int = 0, end: Optional[int] = None) -> str:
        """
        Get a slice of text.
        
        Args:
            start: Start index
            end: End index (exclusive)
            
        Returns:
            Text slice
        """
        if end is None:
            end = self._length
        return ''.join(self[i] for i in range(start, min(end, self._length)))
    
    def find(self, text: str, start: int = 0) -> int:
        """
        Find text in buffer.
        
        Args:
            text: Text to find
            start: Start position for search
            
        Returns:
            Index of first occurrence, or -1 if not found
        """
        content = self.get_text()
        return content.find(text, start)
    
    def rfind(self, text: str, end: Optional[int] = None) -> int:
        """
        Find text in buffer (reverse search).
        
        Args:
            text: Text to find
            end: End position for search
            
        Returns:
            Index of last occurrence, or -1 if not found
        """
        content = self.get_text()
        if end is not None:
            return content.rfind(text, 0, end)
        return content.rfind(text)
    
    def count(self, text: str) -> int:
        """Count occurrences of text."""
        return self.get_text().count(text)
    
    def replace(self, old: str, new: str, count: int = -1) -> int:
        """
        Replace occurrences of text.
        
        Args:
            old: Text to replace
            new: Replacement text
            count: Maximum replacements (-1 for all)
            
        Returns:
            Number of replacements made
        """
        text = self.get_text()
        if count == -1:
            new_text = text.replace(old, new)
        else:
            new_text = text.replace(old, new, count)
        
        if new_text == text:
            return 0
        
        replacements = text.count(old) if count == -1 else min(count, text.count(old))
        
        # Clear and reinsert
        self._buffer = [''] * self.capacity
        self._gap_start = 0
        self._gap_end = self.capacity
        self._cursor = 0
        self._length = 0
        self.insert(new_text)
        
        return replacements
    
    def clear(self) -> None:
        """Clear all content."""
        self._gap_start = 0
        self._gap_end = self.capacity
        self._cursor = 0
        self._length = 0
    
    def line_info(self) -> Tuple[int, int, int]:
        """
        Get line information at cursor.
        
        Returns:
            Tuple of (line_number, column, line_start_index)
        """
        text = self.get_text()
        lines_before = text[:self._cursor]
        line_num = lines_before.count('\n') + 1
        
        last_newline = lines_before.rfind('\n')
        if last_newline == -1:
            col = self._cursor
            line_start = 0
        else:
            col = self._cursor - last_newline - 1
            line_start = last_newline + 1
        
        return line_num, col, line_start
    
    def get_line(self, line_number: int) -> str:
        """
        Get content of a specific line.
        
        Args:
            line_number: 1-indexed line number
            
        Returns:
            Line content (without newline)
        """
        lines = self.get_text().split('\n')
        if 1 <= line_number <= len(lines):
            return lines[line_number - 1]
        return ""
    
    def goto_line(self, line_number: int) -> None:
        """
        Move cursor to start of specified line.
        
        Args:
            line_number: 1-indexed line number
        """
        if line_number < 1:
            line_number = 1
        
        text = self.get_text()
        lines = text.split('\n')
        
        if line_number > len(lines):
            self.move_cursor(len(text))
            return
        
        pos = 0
        for i in range(line_number - 1):
            pos += len(lines[i]) + 1  # +1 for newline
        
        self.move_cursor(pos)
    
    def word_info(self) -> Tuple[int, int]:
        """
        Get current word boundaries.
        
        Returns:
            Tuple of (word_start, word_end) indices
        """
        text = self.get_text()
        cursor = self._cursor
        
        if not text:
            return 0, 0
        
        # Find word start
        start = cursor
        while start > 0 and text[start - 1].isalnum():
            start -= 1
        
        # Find word end
        end = cursor
        while end < len(text) and text[end].isalnum():
            end += 1
        
        return start, end
    
    def delete_word(self, forward: bool = True) -> str:
        """
        Delete word at cursor.
        
        Args:
            forward: Delete forward if True, backward if False
            
        Returns:
            Deleted text
        """
        text = self.get_text()
        cursor = self._cursor
        
        if not text:
            return ""
        
        if forward:
            # Find end of word
            end = cursor
            # Skip whitespace
            while end < len(text) and text[end].isspace():
                end += 1
            # Skip word characters
            while end < len(text) and text[end].isalnum():
                end += 1
            
            # Move gap to cursor and delete
            self.move_cursor(cursor)
            return self.delete(end - cursor)
        else:
            # Find start of previous word
            start = cursor
            # Skip whitespace backwards
            while start > 0 and text[start - 1].isspace():
                start -= 1
            # Skip word characters backwards
            while start > 0 and text[start - 1].isalnum():
                start -= 1
            
            # Move gap and delete
            self.move_cursor(start)
            return self.delete(cursor - start)
    
    def get_state(self) -> dict:
        """Get current state for serialization."""
        return {
            'text': self.get_text(),
            'cursor': self._cursor,
            'capacity': self.capacity
        }
    
    def set_state(self, state: dict) -> None:
        """Restore state from serialization."""
        self.clear()
        if 'text' in state:
            self.insert(state['text'])
        if 'cursor' in state:
            self.move_cursor(state['cursor'])
    
    def copy(self) -> 'GapBuffer':
        """Create a deep copy of this buffer."""
        new_buffer = GapBuffer(self.capacity)
        new_buffer._buffer = self._buffer.copy()
        new_buffer._gap_start = self._gap_start
        new_buffer._gap_end = self._gap_end
        new_buffer._cursor = self._cursor
        new_buffer._length = self._length
        return new_buffer


class GapBufferWithHistory(GapBuffer):
    """
    Gap Buffer with undo/redo support.
    """
    
    def __init__(self, initial_capacity: int = 256, text: str = "", max_history: int = 100):
        # Initialize history attributes FIRST
        self._history: List[dict] = []
        self._history_index: int = -1
        self._max_history: int = max_history
        self._grouping: bool = False
        self._in_undo_redo: bool = False  # Flag to prevent saving during undo/redo
        
        # Initialize buffer (without text)
        super().__init__(initial_capacity, "")
        
        # Save empty state
        self._save_state()
        
        # Insert initial text if provided
        if text:
            self.insert(text)
    
    def _save_state(self) -> None:
        """Save current state to history."""
        if self._in_undo_redo:
            return
        
        # Remove any future states
        self._history = self._history[:self._history_index + 1]
        
        # Add current state
        self._history.append(self.get_state())
        
        # Limit history size
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]
        
        self._history_index = len(self._history) - 1
    
    def begin_group(self) -> None:
        """Start grouping operations (will be undone/redone together)."""
        self._grouping = True
    
    def end_group(self) -> None:
        """End grouping and save state."""
        self._grouping = False
        self._save_state()
    
    def insert(self, text: str) -> None:
        super().insert(text)
        if not self._grouping:
            self._save_state()
    
    def delete(self, count: int = 1) -> str:
        result = super().delete(count)
        if not self._grouping:
            self._save_state()
        return result
    
    def undo(self) -> bool:
        """
        Undo last operation.
        
        Returns:
            True if undone, False if no more history
        """
        if self._history_index <= 0:
            return False
        
        self._in_undo_redo = True
        self._history_index -= 1
        state = self._history[self._history_index]
        super().set_state(state)
        self._in_undo_redo = False
        return True
    
    def redo(self) -> bool:
        """
        Redo last undone operation.
        
        Returns:
            True if redone, False if no more future
        """
        if self._history_index >= len(self._history) - 1:
            return False
        
        self._in_undo_redo = True
        self._history_index += 1
        state = self._history[self._history_index]
        super().set_state(state)
        self._in_undo_redo = False
        return True
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self._history_index > 0
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return self._history_index < len(self._history) - 1
    
    def clear_history(self) -> None:
        """Clear undo history."""
        self._history = [self.get_state()]
        self._history_index = 0


class TextEditor:
    """
    A simple text editor interface built on GapBuffer.
    Provides common editor operations.
    """
    
    def __init__(self, text: str = ""):
        """Initialize editor with optional text."""
        self._buffer = GapBufferWithHistory(text=text)
        self._selection_start: Optional[int] = None
        self._selection_end: Optional[int] = None
    
    @property
    def cursor(self) -> int:
        """Current cursor position."""
        return self._buffer.cursor
    
    @property
    def length(self) -> int:
        """Text length."""
        return self._buffer.length
    
    @property
    def text(self) -> str:
        """Full text content."""
        return self._buffer.get_text()
    
    def start_selection(self) -> None:
        """Start selection at current cursor."""
        self._selection_start = self._buffer.cursor
        self._selection_end = self._buffer.cursor
    
    def extend_selection(self) -> None:
        """Extend selection to current cursor."""
        if self._selection_start is None:
            self.start_selection()
        self._selection_end = self._buffer.cursor
    
    def end_selection(self) -> None:
        """End selection."""
        pass
    
    def clear_selection(self) -> None:
        """Clear selection."""
        self._selection_start = None
        self._selection_end = None
    
    def has_selection(self) -> bool:
        """Check if there is an active selection."""
        if self._selection_start is None or self._selection_end is None:
            return False
        return self._selection_start != self._selection_end
    
    def get_selection(self) -> Tuple[int, int]:
        """Get selection range (start, end) in document order."""
        if not self.has_selection():
            return self._buffer.cursor, self._buffer.cursor
        return (min(self._selection_start, self._selection_end),
                max(self._selection_start, self._selection_end))
    
    def get_selected_text(self) -> str:
        """Get currently selected text."""
        if not self.has_selection():
            return ""
        start, end = self.get_selection()
        return self._buffer.get_slice(start, end)
    
    def select_all(self) -> None:
        """Select all text."""
        self._selection_start = 0
        self._selection_end = self._buffer.length
    
    def select_word(self) -> None:
        """Select word at cursor."""
        start, end = self._buffer.word_info()
        self._selection_start = start
        self._selection_end = end
    
    def select_line(self) -> None:
        """Select current line."""
        line_num, _, line_start = self._buffer.line_info()
        text = self._buffer.get_text()
        next_newline = text.find('\n', self._buffer.cursor)
        if next_newline == -1:
            next_newline = self._buffer.length
        self._selection_start = line_start
        self._selection_end = next_newline
    
    def type_text(self, text: str) -> None:
        """Type text at cursor, replacing selection if any."""
        if self.has_selection():
            self.delete_selection()
        self._buffer.insert(text)
    
    def delete_selection(self) -> str:
        """Delete selected text."""
        if not self.has_selection():
            return ""
        
        start, end = self.get_selection()
        self._buffer.move_cursor(start)
        deleted = self._buffer.delete(end - start)
        self.clear_selection()
        return deleted
    
    def delete(self, forward: bool = True) -> str:
        """Delete character or selection."""
        if self.has_selection():
            return self.delete_selection()
        
        if forward:
            return self._buffer.delete(1)
        else:
            return self._buffer.backspace(1)
    
    def delete_word(self, forward: bool = True) -> str:
        """Delete word."""
        if self.has_selection():
            return self.delete_selection()
        return self._buffer.delete_word(forward)
    
    def move_cursor(self, position: int, extend_selection: bool = False) -> None:
        """Move cursor to position."""
        # If extending selection and no selection exists, save current position as start
        if extend_selection and not self.has_selection():
            self._selection_start = self._buffer.cursor
        
        self._buffer.move_cursor(position)
        
        if extend_selection:
            self._selection_end = self._buffer.cursor
        elif self.has_selection():
            self.clear_selection()
    
    def move_relative(self, offset: int, extend_selection: bool = False) -> None:
        """Move cursor relative to current position."""
        self.move_cursor(self._buffer.cursor + offset, extend_selection)
    
    def move_to_line(self, line_number: int, extend_selection: bool = False) -> None:
        """Move cursor to line."""
        self._buffer.goto_line(line_number)
        if extend_selection:
            self.extend_selection()
        elif self.has_selection():
            self.clear_selection()
    
    def move_word_forward(self, extend_selection: bool = False) -> None:
        """Move cursor to start of next word."""
        text = self._buffer.get_text()
        cursor = self._buffer.cursor
        
        # Skip current word
        while cursor < len(text) and text[cursor].isalnum():
            cursor += 1
        # Skip whitespace
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
        
        self.move_cursor(cursor, extend_selection)
    
    def move_word_backward(self, extend_selection: bool = False) -> None:
        """Move cursor to start of previous word."""
        text = self._buffer.get_text()
        cursor = self._buffer.cursor
        
        # Skip whitespace backwards
        while cursor > 0 and text[cursor - 1].isspace():
            cursor -= 1
        # Skip word backwards
        while cursor > 0 and text[cursor - 1].isalnum():
            cursor -= 1
        
        self.move_cursor(cursor, extend_selection)
    
    def move_line_start(self, extend_selection: bool = False) -> None:
        """Move cursor to start of line."""
        _, _, line_start = self._buffer.line_info()
        self.move_cursor(line_start, extend_selection)
    
    def move_line_end(self, extend_selection: bool = False) -> None:
        """Move cursor to end of line."""
        text = self._buffer.get_text()
        next_newline = text.find('\n', self._buffer.cursor)
        if next_newline == -1:
            next_newline = self._buffer.length
        self.move_cursor(next_newline, extend_selection)
    
    def move_document_start(self, extend_selection: bool = False) -> None:
        """Move cursor to start of document."""
        self.move_cursor(0, extend_selection)
    
    def move_document_end(self, extend_selection: bool = False) -> None:
        """Move cursor to end of document."""
        self.move_cursor(self._buffer.length, extend_selection)
    
    def undo(self) -> bool:
        """Undo last operation."""
        self.clear_selection()
        return self._buffer.undo()
    
    def redo(self) -> bool:
        """Redo last undone operation."""
        self.clear_selection()
        return self._buffer.redo()
    
    def find(self, text: str, start: int = 0) -> int:
        """Find text, returns -1 if not found."""
        return self._buffer.find(text, start)
    
    def find_next(self, text: str) -> int:
        """Find next occurrence from cursor."""
        return self._buffer.find(text, self._buffer.cursor)
    
    def find_previous(self, text: str) -> int:
        """Find previous occurrence before cursor."""
        return self._buffer.rfind(text, self._buffer.cursor)
    
    def replace(self, old: str, new: str, count: int = -1) -> int:
        """Replace text."""
        self.clear_selection()
        return self._buffer.replace(old, new, count)
    
    def get_line_number(self) -> int:
        """Get current line number (1-indexed)."""
        line_num, _, _ = self._buffer.line_info()
        return line_num
    
    def get_column(self) -> int:
        """Get current column (0-indexed)."""
        _, col, _ = self._buffer.line_info()
        return col
    
    def get_line_count(self) -> int:
        """Get total number of lines."""
        return self._buffer.get_text().count('\n') + 1
    
    def __str__(self) -> str:
        return self._buffer.get_text()
    
    def __repr__(self) -> str:
        return f"TextEditor(length={self.length}, cursor={self.cursor})"


# Convenience functions
def create_buffer(text: str = "", capacity: int = 256) -> GapBuffer:
    """Create a gap buffer with optional initial text."""
    return GapBuffer(capacity, text)


def create_editor(text: str = "") -> TextEditor:
    """Create a text editor with optional initial text."""
    return TextEditor(text)


def from_file(filepath: str) -> GapBuffer:
    """Create a gap buffer from file contents."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return GapBuffer(text=f.read())


def to_file(buffer: GapBuffer, filepath: str) -> None:
    """Write gap buffer contents to file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(buffer.get_text())