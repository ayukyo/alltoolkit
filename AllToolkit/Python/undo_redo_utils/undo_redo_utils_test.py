#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Undo/Redo Utilities Test Suite

Comprehensive tests for undo/redo functionality.
"""

import unittest
from datetime import datetime
from typing import List, Any, Optional

# Import from mod.py
from mod import (
    Command, CommandResult, SimpleCommand, StateCommand,
    UndoRedoManager, TransactionCommand, Memento, MementoManager,
    UndoRedoError, CannotUndoError, CannotRedoError, TransactionError,
    create_simple_manager, create_memento_manager
)


# ============================================================================
# Test Fixtures - Sample Commands
# ============================================================================

class Counter:
    """Simple counter for testing."""
    def __init__(self, value: int = 0):
        self.value = value
        self.history: List[int] = [value]
    
    def increment(self, amount: int = 1) -> int:
        self.value += amount
        self.history.append(self.value)
        return self.value
    
    def decrement(self, amount: int = 1) -> int:
        self.value -= amount
        self.history.append(self.value)
        return self.value
    
    def set_value(self, value: int) -> int:
        self.value = value
        self.history.append(self.value)
        return self.value


class IncrementCommand(Command):
    """Command to increment a counter."""
    
    def __init__(self, counter: Counter, amount: int = 1, description: str = ""):
        super().__init__(description or f"Increment by {amount}")
        self.counter = counter
        self.amount = amount
    
    def do(self) -> CommandResult:
        new_value = self.counter.increment(self.amount)
        self._executed = True
        return CommandResult(success=True, data=new_value)
    
    def undo(self) -> CommandResult:
        new_value = self.counter.decrement(self.amount)
        self._executed = False
        return CommandResult(success=True, data=new_value)


class SetValueCommand(Command):
    """Command to set a counter value."""
    
    def __init__(self, counter: Counter, new_value: int, description: str = ""):
        super().__init__(description or f"Set value to {new_value}")
        self.counter = counter
        self.new_value = new_value
        self.old_value: Optional[int] = None
    
    def do(self) -> CommandResult:
        self.old_value = self.counter.value
        self.counter.set_value(self.new_value)
        return CommandResult(success=True, data=self.new_value)
    
    def undo(self) -> CommandResult:
        if self.old_value is not None:
            self.counter.set_value(self.old_value)
        return CommandResult(success=True, data=self.old_value)


class MergeableIncrementCommand(Command):
    """Increment command that can merge with similar commands."""
    
    def __init__(self, counter: Counter, amount: int = 1):
        super().__init__(description=f"Increment by {amount}")
        self.counter = counter
        self.amount = amount
    
    def do(self) -> CommandResult:
        new_value = self.counter.increment(self.amount)
        return CommandResult(success=True, data=new_value)
    
    def undo(self) -> CommandResult:
        new_value = self.counter.decrement(self.amount)
        return CommandResult(success=True, data=new_value)
    
    def can_merge_with(self, other: Command) -> bool:
        return isinstance(other, MergeableIncrementCommand) and self.counter is other.counter
    
    def merge_with(self, other: Command) -> Command:
        if not isinstance(other, MergeableIncrementCommand):
            raise ValueError("Cannot merge with non-mergeable command")
        merged = MergeableIncrementCommand(self.counter, self.amount + other.amount)
        merged.description = f"Increment by {merged.amount}"
        return merged


# ============================================================================
# Command Tests
# ============================================================================

class TestCommand(unittest.TestCase):
    """Test base Command class."""
    
    def test_command_id_generation(self):
        """Test that commands get unique IDs."""
        cmd1 = IncrementCommand(Counter())
        cmd2 = IncrementCommand(Counter())
        self.assertNotEqual(cmd1.id, cmd2.id)
    
    def test_command_timestamp(self):
        """Test that commands have timestamps."""
        cmd = IncrementCommand(Counter())
        self.assertIsInstance(cmd.timestamp, datetime)
    
    def test_is_executed_flag(self):
        """Test the is_executed property."""
        counter = Counter()
        cmd = IncrementCommand(counter)
        self.assertFalse(cmd.is_executed)
        cmd.do()
        self.assertTrue(cmd.is_executed)
        cmd.undo()
        self.assertFalse(cmd.is_executed)


class TestSimpleCommand(unittest.TestCase):
    """Test SimpleCommand class."""
    
    def test_simple_command_basic(self):
        """Test basic SimpleCommand functionality."""
        values = []
        
        cmd = SimpleCommand(
            do_func=lambda: values.append(1) or len(values),
            undo_func=lambda: values.pop() or len(values),
            description="Append 1"
        )
        
        result = cmd.do()
        self.assertTrue(result.success)
        self.assertEqual(values, [1])
        
        result = cmd.undo()
        self.assertTrue(result.success)
        self.assertEqual(values, [])


class TestStateCommand(unittest.TestCase):
    """Test StateCommand class."""
    
    def test_state_command(self):
        """Test StateCommand with state capture and restore."""
        class TestStateCmd(StateCommand):
            def __init__(self, obj):
                super().__init__("Test state")
                self.obj = obj
                self.saved_state = None
            
            def capture_state(self):
                return {"value": self.obj.value}
            
            def restore_state(self, state):
                self.obj.value = state["value"]
            
            def do(self):
                if self.saved_state is None:
                    self.saved_state = self.capture_state()
                self.obj.value += 1
                return CommandResult(success=True)
            
            def undo(self):
                if self.saved_state:
                    self.restore_state(self.saved_state)
                return CommandResult(success=True)
        
        class Obj:
            def __init__(self):
                self.value = 0
        
        obj = Obj()
        cmd = TestStateCmd(obj)
        cmd.do()
        self.assertEqual(obj.value, 1)
        cmd.undo()
        self.assertEqual(obj.value, 0)


# ============================================================================
# UndoRedoManager Tests
# ============================================================================

class TestUndoRedoManager(unittest.TestCase):
    """Test UndoRedoManager class."""
    
    def test_basic_undo_redo(self):
        """Test basic undo and redo operations."""
        counter = Counter()
        manager = UndoRedoManager()
        
        # Execute some commands
        manager.execute(IncrementCommand(counter, 5))
        manager.execute(IncrementCommand(counter, 3))
        
        self.assertEqual(counter.value, 8)
        self.assertTrue(manager.can_undo)
        self.assertFalse(manager.can_redo)
        
        # Undo
        manager.undo()
        self.assertEqual(counter.value, 5)
        self.assertTrue(manager.can_undo)
        self.assertTrue(manager.can_redo)
        
        # Redo
        manager.redo()
        self.assertEqual(counter.value, 8)
        self.assertFalse(manager.can_redo)
    
    def test_multiple_undo_steps(self):
        """Test undoing multiple steps at once."""
        counter = Counter()
        manager = UndoRedoManager()
        
        manager.execute(IncrementCommand(counter, 1))
        manager.execute(IncrementCommand(counter, 2))
        manager.execute(IncrementCommand(counter, 3))
        
        self.assertEqual(counter.value, 6)
        
        # Undo 2 steps
        manager.undo(2)
        self.assertEqual(counter.value, 1)
        
        # Redo 1 step
        manager.redo(1)
        self.assertEqual(counter.value, 3)
    
    def test_cannot_undo_when_empty(self):
        """Test that undo raises error when history is empty."""
        manager = UndoRedoManager()
        
        with self.assertRaises(CannotUndoError):
            manager.undo()
    
    def test_cannot_redo_when_empty(self):
        """Test that redo raises error when redo stack is empty."""
        manager = UndoRedoManager()
        
        with self.assertRaises(CannotRedoError):
            manager.redo()
    
    def test_redo_clears_on_new_command(self):
        """Test that redo stack is cleared when new command is executed."""
        counter = Counter()
        manager = UndoRedoManager()
        
        manager.execute(IncrementCommand(counter, 5))
        manager.execute(IncrementCommand(counter, 3))
        manager.undo()
        
        self.assertTrue(manager.can_redo)
        self.assertEqual(manager.redo_count, 1)
        
        # Execute new command
        manager.execute(IncrementCommand(counter, 10))
        
        self.assertFalse(manager.can_redo)
        self.assertEqual(manager.redo_count, 0)
    
    def test_max_history_limit(self):
        """Test that history limit is enforced."""
        counter = Counter()
        manager = UndoRedoManager(max_history=3)
        
        manager.execute(IncrementCommand(counter, 1))  # Value = 1, dropped from history
        manager.execute(IncrementCommand(counter, 2))  # Value = 3
        manager.execute(IncrementCommand(counter, 3))  # Value = 6
        manager.execute(IncrementCommand(counter, 4))  # Value = 10
        
        self.assertEqual(manager.undo_count, 3)  # Only last 3 commands kept
        self.assertEqual(counter.value, 10)
        
        # Undo 3 times - only last 3 commands can be undone
        manager.undo(3)
        # The +1 command was dropped, so we can only undo +2, +3, +4
        # 10 - 4 - 3 - 2 = 1
        self.assertEqual(counter.value, 1)
    
    def test_on_change_callback(self):
        """Test that on_change callback is called."""
        counter = Counter()
        changes = []
        
        def on_change():
            changes.append(len(changes))
        
        manager = UndoRedoManager(on_change=on_change)
        
        manager.execute(IncrementCommand(counter, 1))
        manager.execute(IncrementCommand(counter, 2))
        manager.undo()
        manager.redo()
        
        self.assertEqual(len(changes), 4)
    
    def test_command_merging(self):
        """Test that mergeable commands are combined."""
        counter = Counter()
        manager = UndoRedoManager()
        
        # Execute mergeable commands
        manager.execute(MergeableIncrementCommand(counter, 1))
        manager.execute(MergeableIncrementCommand(counter, 2))
        
        # Should be merged into one command with amount 3
        self.assertEqual(manager.undo_count, 1)
        self.assertEqual(counter.value, 3)
        
        # Single undo should revert all
        manager.undo()
        self.assertEqual(counter.value, 0)


class TestTransactions(unittest.TestCase):
    """Test transaction functionality."""
    
    def test_transaction_commit(self):
        """Test committing a transaction."""
        counter = Counter()
        manager = UndoRedoManager()
        
        manager.begin_transaction("Add 10")
        manager.execute(IncrementCommand(counter, 3))
        manager.execute(IncrementCommand(counter, 3))
        manager.execute(IncrementCommand(counter, 4))
        manager.commit_transaction()
        
        self.assertEqual(counter.value, 10)
        self.assertEqual(manager.undo_count, 1)  # Single transaction command
        
        # Single undo should revert all
        manager.undo()
        self.assertEqual(counter.value, 0)
    
    def test_transaction_rollback(self):
        """Test rolling back a transaction."""
        counter = Counter()
        manager = UndoRedoManager()
        
        manager.execute(IncrementCommand(counter, 5))  # Before transaction
        
        manager.begin_transaction("Add more")
        manager.execute(IncrementCommand(counter, 3))
        manager.execute(IncrementCommand(counter, 2))
        
        self.assertEqual(counter.value, 10)
        
        manager.rollback_transaction()
        
        self.assertEqual(counter.value, 5)  # Only original value remains
    
    def test_cannot_undo_during_transaction(self):
        """Test that undo/redo is blocked during transaction."""
        counter = Counter()
        manager = UndoRedoManager()
        
        manager.execute(IncrementCommand(counter, 5))
        manager.begin_transaction("Test")
        
        with self.assertRaises(TransactionError):
            manager.undo()
        
        with self.assertRaises(TransactionError):
            manager.redo()
        
        manager.rollback_transaction()
    
    def test_nested_transaction_error(self):
        """Test that nested transactions raise error."""
        manager = UndoRedoManager()
        
        manager.begin_transaction("Outer")
        
        with self.assertRaises(TransactionError):
            manager.begin_transaction("Inner")
        
        manager.rollback_transaction()


class TestSavepoints(unittest.TestCase):
    """Test savepoint functionality."""
    
    def test_savepoint_basic(self):
        """Test basic savepoint creation and restore."""
        counter = Counter()
        manager = UndoRedoManager()
        
        manager.execute(IncrementCommand(counter, 1))
        manager.create_savepoint("after_one")
        
        manager.execute(IncrementCommand(counter, 2))
        manager.execute(IncrementCommand(counter, 3))
        
        self.assertEqual(counter.value, 6)
        
        manager.restore_savepoint("after_one")
        self.assertEqual(counter.value, 1)
    
    def test_delete_savepoint(self):
        """Test deleting savepoints."""
        manager = UndoRedoManager()
        
        manager.create_savepoint("test")
        self.assertTrue(manager.delete_savepoint("test"))
        self.assertFalse(manager.delete_savepoint("test"))
    
    def test_restore_nonexistent_savepoint(self):
        """Test restoring a savepoint that doesn't exist."""
        manager = UndoRedoManager()
        
        with self.assertRaises(UndoRedoError):
            manager.restore_savepoint("nonexistent")


class TestHistoryDescriptions(unittest.TestCase):
    """Test history description retrieval."""
    
    def test_undo_descriptions(self):
        """Test getting undo descriptions."""
        counter = Counter()
        manager = UndoRedoManager()
        
        manager.execute(SetValueCommand(counter, 5, "Set to 5"))
        manager.execute(SetValueCommand(counter, 10, "Set to 10"))
        
        descriptions = manager.get_undo_descriptions()
        self.assertEqual(len(descriptions), 2)
        self.assertIn("Set to 10", descriptions[0])
        self.assertIn("Set to 5", descriptions[1])
    
    def test_redo_descriptions(self):
        """Test getting redo descriptions."""
        counter = Counter()
        manager = UndoRedoManager()
        
        manager.execute(SetValueCommand(counter, 5, "Set to 5"))
        manager.execute(SetValueCommand(counter, 10, "Set to 10"))
        manager.undo()
        
        descriptions = manager.get_redo_descriptions()
        self.assertEqual(len(descriptions), 1)
        self.assertIn("Set to 10", descriptions[0])


# ============================================================================
# MementoManager Tests
# ============================================================================

class TestMementoManager(unittest.TestCase):
    """Test MementoManager class."""
    
    def test_basic_memento(self):
        """Test basic memento save/undo/redo."""
        initial = {"value": 0}
        manager = MementoManager(initial)
        
        manager.save("Initial")
        manager.current_state["value"] = 5
        
        self.assertEqual(manager.current_state["value"], 5)
        
        manager.save("Changed to 5")
        manager.current_state["value"] = 10
        
        manager.undo()
        self.assertEqual(manager.current_state["value"], 5)
        
        manager.redo()
        self.assertEqual(manager.current_state["value"], 10)
    
    def test_set_state(self):
        """Test set_state convenience method."""
        manager = MementoManager({"value": 0})
        
        manager.set_state({"value": 10}, "Set to 10")
        manager.set_state({"value": 20}, "Set to 20")
        
        self.assertEqual(manager.current_state["value"], 20)
        
        manager.undo()
        self.assertEqual(manager.current_state["value"], 10)
    
    def test_max_history(self):
        """Test memento history limit."""
        manager = MementoManager({"value": 0}, max_history=2)
        
        for i in range(1, 5):
            manager.save(f"Step {i}")
            manager.current_state["value"] = i
        
        # Only 2 snapshots should be retained
        manager.undo()
        manager.undo()
        
        # Third undo should not be possible
        self.assertFalse(manager.can_undo)
    
    def test_on_change_callback(self):
        """Test on_change callback."""
        changes = []
        
        def on_change(state):
            changes.append(state["value"])
        
        manager = MementoManager({"value": 0}, on_change=on_change)
        
        manager.save("Initial")  # Saves {value: 0}
        manager.current_state["value"] = 5  # Modify
        manager.save("Changed")  # Saves {value: 5}
        manager.current_state["value"] = 10  # Modify
        
        manager.undo()  # Restores to {value: 5} (last saved)
        
        self.assertIn(5, changes)
    
    def test_clear_history(self):
        """Test clearing history."""
        manager = MementoManager({"value": 0})
        
        manager.save("1")
        manager.save("2")
        manager.save("3")
        
        manager.clear()
        
        self.assertFalse(manager.can_undo)
        self.assertFalse(manager.can_redo)


# ============================================================================
# TransactionCommand Tests
# ============================================================================

class TestTransactionCommand(unittest.TestCase):
    """Test TransactionCommand class."""
    
    def test_transaction_command_execute(self):
        """Test executing transaction command."""
        counter = Counter()
        
        commands = [
            IncrementCommand(counter, 1),
            IncrementCommand(counter, 2),
            IncrementCommand(counter, 3)
        ]
        
        # Use execute_commands=True for standalone execution
        transaction = TransactionCommand(commands, "Add 6", execute_commands=True)
        result = transaction.do()
        
        self.assertTrue(result.success)
        self.assertEqual(counter.value, 6)
    
    def test_transaction_command_undo(self):
        """Test undoing transaction command."""
        counter = Counter()
        
        commands = [
            IncrementCommand(counter, 1),
            IncrementCommand(counter, 2)
        ]
        
        # Use execute_commands=True for standalone execution
        transaction = TransactionCommand(commands, "Add 3", execute_commands=True)
        transaction.do()
        transaction.undo()
        
        self.assertEqual(counter.value, 0)


# ============================================================================
# Convenience Function Tests
# ============================================================================

class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_create_simple_manager(self):
        """Test create_simple_manager function."""
        manager = create_simple_manager(max_history=10)
        self.assertIsInstance(manager, UndoRedoManager)
        self.assertEqual(manager._max_history, 10)
    
    def test_create_memento_manager(self):
        """Test create_memento_manager function."""
        manager = create_memento_manager({"value": 0}, max_history=5)
        self.assertIsInstance(manager, MementoManager)
        self.assertEqual(manager.current_state, {"value": 0})


# ============================================================================
# Edge Cases
# ============================================================================

class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_empty_transaction(self):
        """Test committing empty transaction."""
        manager = UndoRedoManager()
        
        manager.begin_transaction("Empty")
        result = manager.commit_transaction()
        
        self.assertTrue(result.success)
        self.assertIn("Empty", result.message)
    
    def test_multiple_undos_than_redos(self):
        """Test undoing more than available."""
        counter = Counter()
        manager = UndoRedoManager()
        
        manager.execute(IncrementCommand(counter, 1))
        manager.execute(IncrementCommand(counter, 2))
        
        # Undo more than available
        manager.undo(5)
        self.assertEqual(counter.value, 0)
    
    def test_redo_more_than_available(self):
        """Test redoing more than available."""
        counter = Counter()
        manager = UndoRedoManager()
        
        manager.execute(IncrementCommand(counter, 1))
        manager.execute(IncrementCommand(counter, 2))
        manager.undo(2)
        
        # Redo more than available
        manager.redo(5)
        self.assertEqual(counter.value, 3)
    
    def test_clear_during_transaction(self):
        """Test that rollback_transaction properly undoes in-progress commands."""
        counter = Counter()
        manager = UndoRedoManager()
        
        manager.execute(IncrementCommand(counter, 5))  # Before transaction
        
        manager.begin_transaction("Test")
        manager.execute(IncrementCommand(counter, 3))  # Executed during transaction
        
        self.assertEqual(counter.value, 8)
        
        # Rollback should undo the transaction commands
        manager.rollback_transaction()
        
        # Only the pre-transaction command remains
        self.assertEqual(counter.value, 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)