"""
Gap Buffer Usage Examples

Demonstrates practical usage of the gap buffer data structure
for text editing applications.
"""

import sys
sys.path.insert(0, '..')

from mod import (
    GapBuffer, GapBufferWithHistory, TextEditor,
    create_buffer, create_editor, from_file, to_file
)


def example_basic_operations():
    """Basic gap buffer operations."""
    print("\n=== Basic Operations ===")
    
    # Create an empty buffer
    buf = GapBuffer()
    print(f"Empty buffer: '{buf}' (length: {len(buf)})")
    
    # Insert text
    buf.insert("Hello")
    print(f"After insert 'Hello': '{buf}' (cursor: {buf.cursor})")
    
    # Insert more text
    buf.insert(" World")
    print(f"After insert ' World': '{buf}' (cursor: {buf.cursor})")
    
    # Move cursor and insert
    buf.move_cursor(5)
    buf.insert(",")
    print(f"After insert ',' at position 5: '{buf}' (cursor: {buf.cursor})")


def example_cursor_navigation():
    """Cursor movement examples."""
    print("\n=== Cursor Navigation ===")
    
    buf = GapBuffer(text="Hello World")
    print(f"Initial: '{buf}' (cursor: {buf.cursor})")
    
    # Absolute positioning
    buf.move_cursor(6)
    print(f"After move_cursor(6): cursor={buf.cursor}")
    
    # Relative positioning
    buf.move_cursor_relative(-3)
    print(f"After move_cursor_relative(-3): cursor={buf.cursor}")
    
    # Line-based navigation
    buf.insert("\nNew Line\nAnother Line")
    print(f"\nAfter adding lines:\n{buf}")
    
    buf.goto_line(2)
    line, col, _ = buf.line_info()
    print(f"Line 2: line={line}, col={col}, cursor={buf.cursor}")


def example_editing_operations():
    """Delete and edit operations."""
    print("\n=== Editing Operations ===")
    
    buf = GapBuffer(text="Hello Beautiful World")
    print(f"Initial: '{buf}'")
    
    # Delete forward
    buf.move_cursor(6)
    deleted = buf.delete(9)  # Delete "Beautiful"
    print(f"Deleted: '{deleted}'")
    print(f"After delete: '{buf}'")
    
    # Backspace
    buf.backspace(1)  # Delete space before "World"
    print(f"After backspace: '{buf}'")
    
    # Delete word
    buf = GapBuffer(text="The quick brown fox")
    buf.move_cursor(4)
    deleted = buf.delete_word(forward=True)
    print(f"\nDeleted word: '{deleted}'")
    print(f"After delete word: '{buf}'")


def example_find_and_replace():
    """Search and replace operations."""
    print("\n=== Find and Replace ===")
    
    buf = GapBuffer(text="The quick brown fox jumps over the lazy dog")
    print(f"Text: '{buf}'")
    
    # Find
    pos = buf.find("fox")
    print(f"Found 'fox' at position: {pos}")
    
    # Find next occurrence
    pos = buf.find("the", 5)  # Start from position 5
    print(f"Found 'the' (from pos 5) at position: {pos}")
    
    # Replace
    buf.replace("fox", "cat")
    print(f"After replace 'fox' with 'cat': '{buf}'")
    
    # Replace multiple
    buf = GapBuffer(text="aaa bbb aaa ccc aaa")
    count = buf.replace("aaa", "XXX")
    print(f"\nReplaced {count} occurrences of 'aaa': '{buf}'")


def example_with_undo_redo():
    """Undo/redo functionality."""
    print("\n=== Undo/Redo ===")
    
    buf = GapBufferWithHistory(text="Initial")
    print(f"Initial: '{buf}'")
    
    # Make some edits
    buf.insert(" text")
    print(f"After insert: '{buf}'")
    
    buf.move_cursor(7)
    buf.insert(" edited")
    print(f"After another insert: '{buf}'")
    
    # Undo
    buf.undo()
    print(f"After undo: '{buf}'")
    
    buf.undo()
    print(f"After another undo: '{buf}'")
    
    # Redo
    buf.redo()
    print(f"After redo: '{buf}'")
    
    print(f"\nCan undo: {buf.can_undo()}, Can redo: {buf.can_redo()}")


def example_operation_grouping():
    """Group multiple operations for single undo."""
    print("\n=== Operation Grouping ===")
    
    buf = GapBufferWithHistory(text="")
    
    # Group multiple inserts as one operation
    buf.begin_group()
    buf.insert("H")
    buf.insert("e")
    buf.insert("l")
    buf.insert("l")
    buf.insert("o")
    buf.end_group()
    
    print(f"After grouped inserts: '{buf}'")
    
    # Single undo removes all
    buf.undo()
    print(f"After undo (removes all): '{buf}'")


def example_text_editor():
    """Full text editor with selection support."""
    print("\n=== Text Editor ===")
    
    editor = TextEditor(text="Hello World")
    print(f"Text: '{editor.text}'")
    
    # Selection
    editor.move_cursor(6)
    editor.start_selection()
    editor.move_cursor(11, extend_selection=True)
    
    print(f"Selected: '{editor.get_selected_text()}'")
    
    # Replace selection
    editor.type_text("Universe")
    print(f"After replace: '{editor.text}'")
    
    # Select word
    editor.move_cursor(6)
    editor.select_word()
    print(f"Selected word: '{editor.get_selected_text()}'")
    
    # Select line
    editor = TextEditor(text="Line 1\nLine 2\nLine 3")
    editor.move_cursor(10)
    editor.select_line()
    print(f"\nSelected line: '{editor.get_selected_text()}'")


def example_word_navigation():
    """Navigate by words."""
    print("\n=== Word Navigation ===")
    
    editor = TextEditor(text="The quick brown fox jumps over the lazy dog")
    print(f"Text: '{editor.text}'")
    
    editor.move_cursor(0)
    print(f"Starting at cursor: {editor.cursor}")
    
    # Move forward word by word
    for i in range(5):
        editor.move_word_forward()
        word_start, word_end = editor._buffer.word_info()
        word = editor.text[word_start:word_end]
        print(f"  Word {i+1}: '{word}' at position {editor.cursor}")
    
    # Move backward
    print("\nMoving backward:")
    for i in range(3):
        editor.move_word_backward()
        print(f"  Cursor at: {editor.cursor}")


def example_line_operations():
    """Line-based operations."""
    print("\n=== Line Operations ===")
    
    editor = TextEditor(text="First line\nSecond line\nThird line\nFourth line")
    print(f"Text:\n{editor.text}")
    print(f"\nTotal lines: {editor.get_line_count()}")
    
    # Navigate to different lines
    editor.move_to_line(2)
    print(f"\nAt line {editor.get_line_number()}, column {editor.get_column()}")
    
    # Select current line
    editor.select_line()
    print(f"Selected line: '{editor.get_selected_text()}'")
    
    # Line start/end
    editor.move_to_line(3)
    editor.move_line_end()
    print(f"\nEnd of line 3, cursor: {editor.cursor}")
    
    editor.move_line_start()
    print(f"Start of line 3, cursor: {editor.cursor}")


def example_document_navigation():
    """Document-level navigation."""
    print("\n=== Document Navigation ===")
    
    editor = TextEditor(text="Start of document\nMiddle content\nEnd of document")
    print(f"Text:\n{editor.text}")
    
    # Jump to start/end
    editor.move_document_end()
    print(f"\nAt document end, cursor: {editor.cursor}")
    
    editor.move_document_start()
    print(f"At document start, cursor: {editor.cursor}")
    
    # Selection with navigation
    editor.move_document_start()
    editor.move_document_end(extend_selection=True)
    print(f"\nSelected all: '{editor.get_selected_text()}'")


def example_file_operations():
    """Reading from and writing to files."""
    print("\n=== File Operations ===")
    
    import tempfile
    import os
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        filepath = f.name
        f.write("File content here")
    
    try:
        # Read from file
        buf = from_file(filepath)
        print(f"Read from file: '{buf}'")
        
        # Modify
        buf.move_cursor(0)
        buf.insert("Modified ")
        print(f"After modification: '{buf}'")
        
        # Write to file
        to_file(buf, filepath)
        
        # Read back
        buf2 = from_file(filepath)
        print(f"Read back: '{buf2}'")
    finally:
        os.unlink(filepath)


def example_text_processing():
    """Common text processing patterns."""
    print("\n=== Text Processing Patterns ===")
    
    # Pattern 1: Process each character
    buf = GapBuffer(text="Hello")
    uppercase = ''.join(c.upper() for c in buf)
    print(f"Uppercase: '{uppercase}'")
    
    # Pattern 2: Count occurrences
    buf = GapBuffer(text="The quick brown fox jumps over the lazy dog")
    print(f"\nCount 'o': {buf.count('o')}")
    print(f"Count 'the': {buf.count('the')}")
    
    # Pattern 3: Find all positions
    text = buf.get_text()
    positions = []
    pos = 0
    while True:
        pos = buf.find('o', pos)
        if pos == -1:
            break
        positions.append(pos)
        pos += 1
    print(f"Positions of 'o': {positions}")
    
    # Pattern 4: Extract words
    editor = TextEditor(text=buf.get_text())
    words = []
    editor.move_cursor(0)
    while editor.cursor < editor.length:
        start, end = editor._buffer.word_info()
        if start < end:
            words.append(editor.text[start:end])
        editor.move_cursor(end + 1)
        if editor.cursor <= start:
            break
    print(f"Words: {words[:5]}...")


def example_state_management():
    """Save and restore state."""
    print("\n=== State Management ===")
    
    buf1 = GapBuffer(text="Original text")
    buf1.move_cursor(9)
    
    # Save state
    state = buf1.get_state()
    print(f"State: {state}")
    
    # Modify buffer
    buf1.insert("modified ")
    print(f"Modified: '{buf1}'")
    
    # Restore state
    buf2 = GapBuffer()
    buf2.set_state(state)
    print(f"Restored: '{buf2}' (cursor: {buf2.cursor})")
    
    # Create copy
    buf3 = buf1.copy()
    buf3.delete(100)
    print(f"Copy (after delete): '{buf3}'")
    print(f"Original (unchanged): '{buf1}'")


def example_performance():
    """Performance characteristics demonstration."""
    print("\n=== Performance Characteristics ===")
    
    import time
    
    # Insert at beginning vs end
    buf = GapBuffer()
    
    # Insert at end (gap is at end) - O(1) amortized
    start = time.time()
    for _ in range(10000):
        buf.insert("x")
    end_insert = time.time() - start
    print(f"Insert 10000 chars at end: {end_insert:.4f}s")
    
    # Insert at beginning (requires gap move)
    buf.move_cursor(0)
    start = time.time()
    for _ in range(100):
        buf.move_cursor(0)
        buf.insert("y")
    end_insert_beginning = time.time() - start
    print(f"Insert 100 chars at beginning: {end_insert_beginning:.4f}s")
    
    # Random access
    start = time.time()
    chars = [buf[i] for i in range(0, len(buf), 100)]
    random_access_time = time.time() - start
    print(f"Random access 100 chars: {random_access_time:.6f}s")
    
    print(f"\nFinal buffer size: {len(buf)} chars")


if __name__ == '__main__':
    print("Gap Buffer Examples")
    print("=" * 50)
    
    example_basic_operations()
    example_cursor_navigation()
    example_editing_operations()
    example_find_and_replace()
    example_with_undo_redo()
    example_operation_grouping()
    example_text_editor()
    example_word_navigation()
    example_line_operations()
    example_document_navigation()
    example_file_operations()
    example_text_processing()
    example_state_management()
    example_performance()
    
    print("\n" + "=" * 50)
    print("Examples completed!")