"""
Tests for Gap Buffer implementation.
"""

import unittest
from mod import (
    GapBuffer, GapBufferWithHistory, TextEditor,
    create_buffer, create_editor
)


class TestGapBuffer(unittest.TestCase):
    """Test GapBuffer class."""
    
    def test_empty_buffer(self):
        """Test empty buffer initialization."""
        buf = GapBuffer()
        self.assertEqual(buf.length, 0)
        self.assertEqual(buf.cursor, 0)
        self.assertEqual(buf.gap_size, buf.capacity)
        self.assertEqual(buf.get_text(), "")
    
    def test_initial_text(self):
        """Test buffer with initial text."""
        buf = GapBuffer(text="Hello")
        self.assertEqual(buf.length, 5)
        self.assertEqual(buf.cursor, 5)
        self.assertEqual(buf.get_text(), "Hello")
    
    def test_insert_basic(self):
        """Test basic insertion."""
        buf = GapBuffer()
        buf.insert("Hello")
        self.assertEqual(buf.get_text(), "Hello")
        self.assertEqual(buf.cursor, 5)
        self.assertEqual(buf.length, 5)
    
    def test_insert_multiple(self):
        """Test multiple insertions."""
        buf = GapBuffer()
        buf.insert("Hello")
        buf.insert(" ")
        buf.insert("World")
        self.assertEqual(buf.get_text(), "Hello World")
    
    def test_cursor_movement(self):
        """Test cursor movement."""
        buf = GapBuffer(text="Hello World")
        
        buf.move_cursor(5)
        self.assertEqual(buf.cursor, 5)
        
        buf.move_cursor(0)
        self.assertEqual(buf.cursor, 0)
        
        buf.move_cursor(11)
        self.assertEqual(buf.cursor, 11)
    
    def test_cursor_movement_bounds(self):
        """Test cursor movement respects bounds."""
        buf = GapBuffer(text="Hello")
        
        buf.move_cursor(-5)
        self.assertEqual(buf.cursor, 0)
        
        buf.move_cursor(100)
        self.assertEqual(buf.cursor, 5)
    
    def test_cursor_relative(self):
        """Test relative cursor movement."""
        buf = GapBuffer(text="Hello")
        
        # Cursor starts at end (5), move_relative(-3) goes to position 2
        buf.move_cursor_relative(-3)
        self.assertEqual(buf.cursor, 2)
        
        buf.move_cursor_relative(-1)
        self.assertEqual(buf.cursor, 1)
    
    def test_insert_at_position(self):
        """Test insertion at different positions."""
        buf = GapBuffer(text="Hllo")
        buf.move_cursor(1)
        buf.insert("e")
        self.assertEqual(buf.get_text(), "Hello")
        self.assertEqual(buf.cursor, 2)
    
    def test_delete_forward(self):
        """Test forward deletion."""
        buf = GapBuffer(text="Hello")
        buf.move_cursor(1)
        deleted = buf.delete(3)
        self.assertEqual(deleted, "ell")
        self.assertEqual(buf.get_text(), "Ho")
    
    def test_delete_backward(self):
        """Test backward deletion (backspace)."""
        buf = GapBuffer(text="Hello")
        deleted = buf.backspace(2)
        self.assertEqual(deleted, "lo")
        self.assertEqual(buf.get_text(), "Hel")
    
    def test_delete_mixed(self):
        """Test mixed insertions and deletions."""
        buf = GapBuffer(text="Hello")
        buf.move_cursor(2)
        buf.delete(2)  # Delete "ll"
        buf.insert("y")
        self.assertEqual(buf.get_text(), "Heyo")
    
    def test_indexing(self):
        """Test character indexing."""
        buf = GapBuffer(text="Hello")
        self.assertEqual(buf[0], 'H')
        self.assertEqual(buf[4], 'o')
        self.assertEqual(buf[-1], 'o')
        self.assertEqual(buf[-5], 'H')
    
    def test_iteration(self):
        """Test iteration over characters."""
        buf = GapBuffer(text="Hello")
        chars = list(buf)
        self.assertEqual(chars, ['H', 'e', 'l', 'l', 'o'])
    
    def test_contains(self):
        """Test 'in' operator."""
        buf = GapBuffer(text="Hello World")
        self.assertIn("World", buf)
        self.assertIn("Hello", buf)
        self.assertNotIn("Goodbye", buf)
    
    def test_find(self):
        """Test find function."""
        buf = GapBuffer(text="Hello World")
        self.assertEqual(buf.find("World"), 6)
        self.assertEqual(buf.find("o"), 4)
        self.assertEqual(buf.find("xyz"), -1)
    
    def test_rfind(self):
        """Test reverse find."""
        buf = GapBuffer(text="Hello World")
        self.assertEqual(buf.rfind("o"), 7)
        self.assertEqual(buf.rfind("l"), 9)
    
    def test_count(self):
        """Test count function."""
        buf = GapBuffer(text="Hello World")
        self.assertEqual(buf.count("l"), 3)
        self.assertEqual(buf.count("o"), 2)
        self.assertEqual(buf.count("x"), 0)
    
    def test_replace(self):
        """Test replace function."""
        buf = GapBuffer(text="Hello World")
        count = buf.replace("World", "Universe")
        self.assertEqual(count, 1)
        self.assertEqual(buf.get_text(), "Hello Universe")
    
    def test_replace_multiple(self):
        """Test replacing multiple occurrences."""
        buf = GapBuffer(text="aaa aaa aaa")
        count = buf.replace("aaa", "b")
        self.assertEqual(count, 3)
        self.assertEqual(buf.get_text(), "b b b")
    
    def test_replace_limited(self):
        """Test limited replace."""
        buf = GapBuffer(text="aaa aaa aaa")
        count = buf.replace("aaa", "b", 2)
        self.assertEqual(count, 2)
        self.assertEqual(buf.get_text(), "b b aaa")
    
    def test_clear(self):
        """Test clear function."""
        buf = GapBuffer(text="Hello")
        buf.clear()
        self.assertEqual(buf.length, 0)
        self.assertEqual(buf.get_text(), "")
        self.assertEqual(buf.cursor, 0)
    
    def test_line_info(self):
        """Test line information."""
        buf = GapBuffer(text="Line1\nLine2\nLine3")
        buf.move_cursor(0)
        line, col, start = buf.line_info()
        self.assertEqual(line, 1)
        self.assertEqual(col, 0)
        
        buf.move_cursor(6)
        line, col, start = buf.line_info()
        self.assertEqual(line, 2)
        self.assertEqual(col, 0)
        
        buf.move_cursor(8)
        line, col, start = buf.line_info()
        self.assertEqual(line, 2)
        self.assertEqual(col, 2)
    
    def test_get_line(self):
        """Test getting line content."""
        buf = GapBuffer(text="Line1\nLine2\nLine3")
        self.assertEqual(buf.get_line(1), "Line1")
        self.assertEqual(buf.get_line(2), "Line2")
        self.assertEqual(buf.get_line(3), "Line3")
        self.assertEqual(buf.get_line(4), "")
    
    def test_goto_line(self):
        """Test moving to line."""
        buf = GapBuffer(text="Line1\nLine2\nLine3")
        # "Line1\nLine2\nLine3" = 18 chars total
        buf.goto_line(2)
        self.assertEqual(buf.cursor, 6)  # After "Line1\n"
        
        buf.goto_line(1)
        self.assertEqual(buf.cursor, 0)
        
        buf.goto_line(100)  # Beyond last line
        self.assertEqual(buf.cursor, 17)  # At end of text
    
    def test_word_info(self):
        """Test word boundaries."""
        buf = GapBuffer(text="Hello World")
        
        buf.move_cursor(0)
        start, end = buf.word_info()
        self.assertEqual(start, 0)
        self.assertEqual(end, 5)
        
        buf.move_cursor(6)
        start, end = buf.word_info()
        self.assertEqual(start, 6)
        self.assertEqual(end, 11)
    
    def test_delete_word_forward(self):
        """Test deleting word forward."""
        buf = GapBuffer(text="Hello World Test")
        buf.move_cursor(0)
        deleted = buf.delete_word(forward=True)
        # Deletes the word "Hello" (standard Ctrl+Delete behavior)
        self.assertEqual(deleted, "Hello")
        self.assertEqual(buf.get_text(), " World Test")
    
    def test_delete_word_backward(self):
        """Test deleting word backward."""
        buf = GapBuffer(text="Hello World Test")
        # "Hello World Test" has 16 chars
        buf.move_cursor(16)  # At end of text
        deleted = buf.delete_word(forward=False)
        # Deletes the word "Test" (standard Ctrl+Backspace behavior)
        self.assertEqual(deleted, "Test")
        self.assertEqual(buf.get_text(), "Hello World ")
    
    def test_get_slice(self):
        """Test getting slice."""
        buf = GapBuffer(text="Hello World")
        self.assertEqual(buf.get_slice(0, 5), "Hello")
        self.assertEqual(buf.get_slice(6, 11), "World")
        self.assertEqual(buf.get_slice(0), "Hello World")
    
    def test_gap_expansion(self):
        """Test gap expansion when buffer fills."""
        buf = GapBuffer(initial_capacity=32)
        # Insert more text than initial capacity
        large_text = "x" * 100
        buf.insert(large_text)
        self.assertEqual(buf.length, 100)
        self.assertEqual(buf.get_text(), large_text)
        # Gap should have been expanded
        self.assertGreater(buf.capacity, 32)
    
    def test_state_save_restore(self):
        """Test state save and restore."""
        buf1 = GapBuffer(text="Hello")
        buf1.move_cursor(2)
        
        state = buf1.get_state()
        
        buf2 = GapBuffer()
        buf2.set_state(state)
        
        self.assertEqual(buf2.get_text(), "Hello")
        self.assertEqual(buf2.cursor, 2)
    
    def test_copy(self):
        """Test buffer copy."""
        buf1 = GapBuffer(text="Hello World")
        buf1.move_cursor(5)
        
        buf2 = buf1.copy()
        
        # Modify original
        buf1.delete(6)
        
        # Copy should be independent
        self.assertEqual(buf1.get_text(), "Hello")
        self.assertEqual(buf2.get_text(), "Hello World")


class TestGapBufferWithHistory(unittest.TestCase):
    """Test GapBufferWithHistory class."""
    
    def test_undo_insert(self):
        """Test undoing insertion."""
        buf = GapBufferWithHistory(text="Hello")
        buf.insert(" World")
        self.assertEqual(buf.get_text(), "Hello World")
        
        buf.undo()
        self.assertEqual(buf.get_text(), "Hello")
    
    def test_undo_delete(self):
        """Test undoing deletion."""
        buf = GapBufferWithHistory(text="Hello World")
        # Move cursor to position 5 (before " World")
        buf.move_cursor(5)
        buf.delete(6)  # Delete " World"
        self.assertEqual(buf.get_text(), "Hello")
        
        buf.undo()
        self.assertEqual(buf.get_text(), "Hello World")
        
        # Can undo further to empty state
        buf.undo()
        self.assertEqual(buf.get_text(), "")
    
    def test_redo(self):
        """Test redo functionality."""
        buf = GapBufferWithHistory(text="Hello")
        buf.insert(" World")
        self.assertEqual(buf.get_text(), "Hello World")
        
        buf.undo()  # Undo " World" -> "Hello"
        self.assertEqual(buf.get_text(), "Hello")
        
        buf.undo()  # Undo "Hello" -> ""
        self.assertEqual(buf.get_text(), "")
        
        buf.redo()  # Redo "Hello"
        self.assertEqual(buf.get_text(), "Hello")
        
        buf.redo()  # Redo " World"
        self.assertEqual(buf.get_text(), "Hello World")
    
    def test_multiple_undo_redo(self):
        """Test multiple undo/redo operations."""
        buf = GapBufferWithHistory(text="A")
        buf.insert("B")
        buf.insert("C")
        buf.insert("D")
        self.assertEqual(buf.get_text(), "ABCD")
        
        # Undo "D" -> "ABC"
        buf.undo()
        self.assertEqual(buf.get_text(), "ABC")
        
        # Undo "C" -> "AB"
        buf.undo()
        self.assertEqual(buf.get_text(), "AB")
        
        # Undo "B" -> "A"
        buf.undo()
        self.assertEqual(buf.get_text(), "A")
        
        # Undo "A" -> ""
        buf.undo()
        self.assertEqual(buf.get_text(), "")
        
        # Can't undo further
        self.assertFalse(buf.can_undo())
        
        # Redo "A"
        buf.redo()
        self.assertEqual(buf.get_text(), "A")
        
        # Redo "B"
        buf.redo()
        self.assertEqual(buf.get_text(), "AB")
        
        # Redo "C"
        buf.redo()
        self.assertEqual(buf.get_text(), "ABC")
        
        # Redo "D"
        buf.redo()
        self.assertEqual(buf.get_text(), "ABCD")
    
    def test_can_undo_redo(self):
        """Test undo/redo availability check."""
        buf = GapBufferWithHistory(text="Hello")
        
        # Initially can undo to empty state (the initial state)
        self.assertTrue(buf.can_undo())  # Can undo to empty state
        self.assertFalse(buf.can_redo())
        
        buf.insert(" World")
        self.assertTrue(buf.can_undo())
        self.assertFalse(buf.can_redo())
        
        buf.undo()  # Undo " World"
        self.assertTrue(buf.can_undo())  # Can still undo to empty
        self.assertTrue(buf.can_redo())
        
        buf.undo()  # Undo "Hello" -> empty
        self.assertFalse(buf.can_undo())
        self.assertTrue(buf.can_redo())
        
        buf.redo()
        self.assertTrue(buf.can_undo())
        self.assertTrue(buf.can_redo())
    
    def test_operation_grouping(self):
        """Test grouping operations."""
        buf = GapBufferWithHistory(text="")
        
        buf.begin_group()
        buf.insert("H")
        buf.insert("e")
        buf.insert("l")
        buf.insert("l")
        buf.insert("o")
        buf.end_group()
        
        # Grouped operations should be undone together
        buf.undo()
        self.assertEqual(buf.get_text(), "")
    
    def test_clear_history(self):
        """Test clearing history."""
        buf = GapBufferWithHistory(text="Hello")
        buf.insert(" World")
        buf.clear_history()
        
        self.assertFalse(buf.can_undo())
        self.assertFalse(buf.can_redo())


class TestTextEditor(unittest.TestCase):
    """Test TextEditor class."""
    
    def test_basic_editing(self):
        """Test basic editing operations."""
        editor = TextEditor()
        editor.type_text("Hello")
        self.assertEqual(editor.text, "Hello")
        self.assertEqual(editor.cursor, 5)
    
    def test_cursor_movement(self):
        """Test cursor movement."""
        editor = TextEditor(text="Hello World")
        
        editor.move_cursor(5)
        self.assertEqual(editor.cursor, 5)
        
        editor.move_relative(-2)
        self.assertEqual(editor.cursor, 3)
    
    def test_selection(self):
        """Test selection operations."""
        editor = TextEditor(text="Hello World")
        
        editor.move_cursor(0)
        editor.start_selection()
        editor.move_cursor(5, extend_selection=True)
        
        self.assertTrue(editor.has_selection())
        self.assertEqual(editor.get_selected_text(), "Hello")
    
    def test_select_all(self):
        """Test select all."""
        editor = TextEditor(text="Hello World")
        editor.select_all()
        
        self.assertTrue(editor.has_selection())
        self.assertEqual(editor.get_selected_text(), "Hello World")
    
    def test_select_word(self):
        """Test word selection."""
        editor = TextEditor(text="Hello World")
        editor.move_cursor(7)  # In "World"
        editor.select_word()
        
        self.assertEqual(editor.get_selected_text(), "World")
    
    def test_select_line(self):
        """Test line selection."""
        editor = TextEditor(text="Line1\nLine2\nLine3")
        editor.move_cursor(8)  # In "Line2"
        editor.select_line()
        
        self.assertEqual(editor.get_selected_text(), "Line2")
    
    def test_delete_selection(self):
        """Test deleting selection."""
        editor = TextEditor(text="Hello World")
        editor.move_cursor(6)
        editor.start_selection()
        editor.move_cursor(11, extend_selection=True)
        
        deleted = editor.delete_selection()
        self.assertEqual(deleted, "World")
        self.assertEqual(editor.text, "Hello ")
    
    def test_type_replaces_selection(self):
        """Test typing replaces selection."""
        editor = TextEditor(text="Hello World")
        editor.move_cursor(6)
        editor.start_selection()
        editor.move_cursor(11, extend_selection=True)
        
        editor.type_text("Universe")
        self.assertEqual(editor.text, "Hello Universe")
    
    def test_delete_character(self):
        """Test character deletion."""
        editor = TextEditor(text="Hello")
        
        editor.move_cursor(1)
        editor.delete(forward=True)  # Delete 'e'
        self.assertEqual(editor.text, "Hllo")
        
        editor.delete(forward=False)  # Backspace at position 1
        self.assertEqual(editor.text, "llo")
    
    def test_delete_word(self):
        """Test word deletion."""
        editor = TextEditor(text="Hello World Test")
        
        editor.move_cursor(0)
        editor.delete_word(forward=True)
        # Deletes "Hello", leaving " World Test"
        self.assertEqual(editor.text, " World Test")
    
    def test_word_navigation(self):
        """Test word-by-word navigation."""
        editor = TextEditor(text="Hello World Test")
        
        editor.move_cursor(0)
        editor.move_word_forward()
        self.assertEqual(editor.cursor, 6)
        
        editor.move_word_forward()
        self.assertEqual(editor.cursor, 12)
        
        editor.move_word_backward()
        self.assertEqual(editor.cursor, 6)
    
    def test_line_navigation(self):
        """Test line navigation."""
        editor = TextEditor(text="Line1\nLine2\nLine3")
        
        editor.move_cursor(0)
        editor.move_line_end()
        self.assertEqual(editor.cursor, 5)
        
        editor.move_line_start()
        self.assertEqual(editor.cursor, 0)
        
        editor.move_to_line(2)
        self.assertEqual(editor.cursor, 6)
    
    def test_document_navigation(self):
        """Test document start/end navigation."""
        editor = TextEditor(text="Hello")
        
        editor.move_cursor(3)
        editor.move_document_end()
        self.assertEqual(editor.cursor, 5)
        
        editor.move_document_start()
        self.assertEqual(editor.cursor, 0)
    
    def test_find(self):
        """Test find operations."""
        editor = TextEditor(text="Hello World")
        
        self.assertEqual(editor.find("World"), 6)
        self.assertEqual(editor.find("xyz"), -1)
        
        editor.move_cursor(0)
        self.assertEqual(editor.find_next("o"), 4)
        
        editor.move_cursor(11)
        self.assertEqual(editor.find_previous("o"), 7)
    
    def test_replace(self):
        """Test replace operation."""
        editor = TextEditor(text="Hello World")
        count = editor.replace("World", "Universe")
        self.assertEqual(count, 1)
        self.assertEqual(editor.text, "Hello Universe")
    
    def test_line_column_info(self):
        """Test line and column info."""
        editor = TextEditor(text="Line1\nLine2\nLine3")
        
        editor.move_cursor(0)
        self.assertEqual(editor.get_line_number(), 1)
        self.assertEqual(editor.get_column(), 0)
        
        editor.move_cursor(7)
        self.assertEqual(editor.get_line_number(), 2)
        self.assertEqual(editor.get_column(), 1)
        
        self.assertEqual(editor.get_line_count(), 3)
    
    def test_undo_redo(self):
        """Test editor undo/redo."""
        editor = TextEditor(text="Hello")
        
        editor.type_text(" World")
        self.assertEqual(editor.text, "Hello World")
        
        # First undo: " World" is removed -> "Hello"
        editor.undo()
        self.assertEqual(editor.text, "Hello")
        
        # Second undo: "Hello" is removed -> ""
        editor.undo()
        self.assertEqual(editor.text, "")
        
        # First redo: "Hello" is restored
        editor.redo()
        self.assertEqual(editor.text, "Hello")
        
        # Second redo: " World" is restored
        editor.redo()
        self.assertEqual(editor.text, "Hello World")
    
    def test_selection_with_navigation(self):
        """Test selection with shift+navigation."""
        editor = TextEditor(text="Hello World")
        
        editor.move_cursor(0)
        editor.move_relative(5, extend_selection=True)
        
        self.assertTrue(editor.has_selection())
        self.assertEqual(editor.get_selected_text(), "Hello")


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_create_buffer(self):
        """Test create_buffer function."""
        buf = create_buffer("Hello")
        self.assertEqual(buf.get_text(), "Hello")
    
    def test_create_editor(self):
        """Test create_editor function."""
        editor = create_editor("Hello")
        self.assertEqual(editor.text, "Hello")
    
    def test_file_operations(self):
        """Test file read/write operations."""
        import tempfile
        import os
        
        buf = GapBuffer(text="Hello World")
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            filepath = f.name
        
        try:
            # Write to file
            from mod import to_file
            to_file(buf, filepath)
            
            # Read from file
            from mod import from_file
            buf2 = from_file(filepath)
            
            self.assertEqual(buf2.get_text(), "Hello World")
        finally:
            os.unlink(filepath)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_empty_string_operations(self):
        """Test operations on empty buffer."""
        buf = GapBuffer()
        
        self.assertEqual(buf.delete(10), "")
        self.assertEqual(buf.backspace(10), "")
        self.assertEqual(buf.get_text(), "")
    
    def test_unicode_text(self):
        """Test Unicode text handling."""
        buf = GapBuffer(text="你好世界")
        self.assertEqual(buf.length, 4)
        self.assertEqual(buf[0], "你")
        
        buf.move_cursor(2)
        buf.insert("中间")
        self.assertEqual(buf.get_text(), "你好中间世界")
    
    def test_emoji_text(self):
        """Test emoji handling."""
        buf = GapBuffer(text="Hello 👋 World")
        self.assertEqual(buf.length, 13)  # Emoji is 1 character in Python 3
        self.assertIn("👋", buf)
    
    def test_large_insert(self):
        """Test inserting large text."""
        buf = GapBuffer(initial_capacity=64)
        large_text = "x" * 10000
        buf.insert(large_text)
        self.assertEqual(buf.length, 10000)
        self.assertEqual(buf.get_text(), large_text)
    
    def test_rapid_cursor_movement(self):
        """Test rapid cursor movement."""
        buf = GapBuffer(text="Hello World")
        
        for _ in range(100):
            buf.move_cursor(5)
            buf.move_cursor(0)
            buf.move_cursor(11)
        
        self.assertEqual(buf.cursor, 11)
    
    def test_rapid_editing(self):
        """Test rapid editing."""
        buf = GapBuffer()
        
        for i in range(100):
            buf.insert(f"word{i} ")
        
        # word0-9: 6 chars each (60 chars)
        # word10-99: 7 chars each (630 chars)
        # Total: 690 chars
        self.assertEqual(buf.length, 690)
    
    def test_repr(self):
        """Test string representation."""
        buf = GapBuffer(text="Hello")
        repr_str = repr(buf)
        self.assertIn("length=5", repr_str)
        self.assertIn("cursor=5", repr_str)
        
        editor = TextEditor(text="Hello")
        repr_str = repr(editor)
        self.assertIn("length=5", repr_str)


if __name__ == '__main__':
    unittest.main()