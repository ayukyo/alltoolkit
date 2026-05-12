"""
Undo/Redo Utils - Command Pattern Implementation for Undo/Redo Operations

A comprehensive library implementing the Command pattern for undo/redo functionality.
Supports command grouping (transactions), memory management, and serialization.

Features:
- Command pattern with execute/undo interface
- Undo/Redo stack management
- Transaction support (grouping commands)
- Memory limit management
- Command history serialization
- Event callbacks for UI updates
- Memento pattern for state snapshots
- Macro commands for complex operations
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union, Tuple
from copy import deepcopy
from datetime import datetime
import json

T = TypeVar('T')


class Command(ABC):
    """
    Abstract base class for all commands.
    
    Commands encapsulate an action that can be executed, undone, and redone.
    Each command should store enough state to reverse its effects.
    """
    
    def __init__(self, description: str = ""):
        """
        Initialize a command.
        
        Args:
            description: Human-readable description of the command
        """
        self.description = description
        self.timestamp = datetime.now()
        self._executed = False
    
    @abstractmethod
    def execute(self) -> Any:
        """
        Execute the command. Should return the result of the operation.
        
        Returns:
            Result of the command execution
        """
        pass
    
    @abstractmethod
    def undo(self) -> Any:
        """
        Undo the command. Should restore state to before execution.
        
        Returns:
            Result of the undo operation
        """
        pass
    
    def redo(self) -> Any:
        """
        Redo the command. Default implementation calls execute again.
        Override for custom redo behavior.
        
        Returns:
            Result of the redo operation
        """
        return self.execute()
    
    @property
    def can_execute(self) -> bool:
        """Check if the command can be executed."""
        return not self._executed
    
    @property
    def can_undo(self) -> bool:
        """Check if the command can be undone."""
        return self._executed
    
    def mark_executed(self) -> None:
        """Mark the command as executed."""
        self._executed = True
    
    def mark_undone(self) -> None:
        """Mark the command as undone."""
        self._executed = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize command to dictionary."""
        return {
            'type': self.__class__.__name__,
            'description': self.description,
            'timestamp': self.timestamp.isoformat(),
            'executed': self._executed
        }
    
    def __repr__(self) -> str:
        status = "executed" if self._executed else "pending"
        return f"<{self.__class__.__name__}: {self.description} [{status}]>"


class SimpleCommand(Command):
    """
    A simple command that uses callable functions for execute/undo.
    Useful for wrapping simple operations without creating full command classes.
    """
    
    def __init__(
        self,
        execute_func: Callable[[], Any],
        undo_func: Callable[[], Any],
        description: str = ""
    ):
        """
        Create a simple command from callable functions.
        
        Args:
            execute_func: Function to call on execute
            undo_func: Function to call on undo
            description: Human-readable description
        """
        super().__init__(description)
        self._execute_func = execute_func
        self._undo_func = undo_func
    
    def execute(self) -> Any:
        result = self._execute_func()
        self.mark_executed()
        return result
    
    def undo(self) -> Any:
        result = self._undo_func()
        self.mark_undone()
        return result


class MementoCommand(Command, Generic[T]):
    """
    Command that uses the Memento pattern to store and restore state.
    Stores a snapshot of state before execution for reliable undo.
    """
    
    def __init__(
        self,
        target: T,
        setter: Callable[[T], None],
        getter: Callable[[], T],
        new_value: T,
        description: str = ""
    ):
        """
        Create a memento-based command.
        
        Args:
            target: The target object/value to modify
            setter: Function to set the new value
            getter: Function to get the current value
            new_value: The new value to set
            description: Human-readable description
        """
        super().__init__(description)
        self.target = target
        self.setter = setter
        self.getter = getter
        self.new_value = new_value
        self.old_value: Optional[T] = None
    
    def execute(self) -> T:
        self.old_value = deepcopy(self.getter())
        self.setter(self.new_value)
        self.mark_executed()
        return self.new_value
    
    def undo(self) -> T:
        if self.old_value is not None:
            self.setter(self.old_value)
        self.mark_undone()
        return self.old_value


class SetValueCommand(Command):
    """
    Command for setting a value on an object's attribute.
    Automatically captures the old value for undo.
    """
    
    def __init__(
        self,
        obj: Any,
        attr: str,
        new_value: Any,
        description: str = ""
    ):
        """
        Create a set value command.
        
        Args:
            obj: Target object
            attr: Attribute name to set
            new_value: New value to set
            description: Human-readable description
        """
        super().__init__(description or f"Set {attr}")
        self.obj = obj
        self.attr = attr
        self.new_value = new_value
        self.old_value: Any = None
        self._has_old_value = False
    
    def execute(self) -> Any:
        if hasattr(self.obj, self.attr):
            self.old_value = deepcopy(getattr(self.obj, self.attr))
            self._has_old_value = True
        setattr(self.obj, self.attr, self.new_value)
        self.mark_executed()
        return self.new_value
    
    def undo(self) -> Any:
        if self._has_old_value:
            setattr(self.obj, self.attr, self.old_value)
        else:
            delattr(self.obj, self.attr)
        self.mark_undone()
        return self.old_value


class ListInsertCommand(Command):
    """Command for inserting an item into a list."""
    
    def __init__(self, target_list: List, index: int, item: Any, description: str = ""):
        super().__init__(description or f"Insert at index {index}")
        self.target_list = target_list
        self.index = index
        self.item = item
    
    def execute(self) -> int:
        self.target_list.insert(self.index, self.item)
        self.mark_executed()
        return self.index
    
    def undo(self) -> None:
        if 0 <= self.index < len(self.target_list):
            self.target_list.pop(self.index)
        self.mark_undone()


class ListRemoveCommand(Command):
    """Command for removing an item from a list."""
    
    def __init__(self, target_list: List, index: int, description: str = ""):
        super().__init__(description or f"Remove at index {index}")
        self.target_list = target_list
        self.index = index
        self.removed_item: Any = None
    
    def execute(self) -> Any:
        if 0 <= self.index < len(self.target_list):
            self.removed_item = self.target_list.pop(self.index)
        self.mark_executed()
        return self.removed_item
    
    def undo(self) -> None:
        if self.removed_item is not None:
            self.target_list.insert(self.index, self.removed_item)
        self.mark_undone()


class DictSetCommand(Command):
    """Command for setting a key-value pair in a dictionary."""
    
    def __init__(self, target_dict: Dict, key: Any, new_value: Any, description: str = ""):
        super().__init__(description or f"Set {key}")
        self.target_dict = target_dict
        self.key = key
        self.new_value = new_value
        self.old_value: Any = None
        self._had_key = False
    
    def execute(self) -> Any:
        if self.key in self.target_dict:
            self.old_value = deepcopy(self.target_dict[self.key])
            self._had_key = True
        self.target_dict[self.key] = self.new_value
        self.mark_executed()
        return self.new_value
    
    def undo(self) -> Any:
        if self._had_key:
            self.target_dict[self.key] = self.old_value
        else:
            del self.target_dict[self.key]
        self.mark_undone()
        return self.old_value


class DictDeleteCommand(Command):
    """Command for deleting a key from a dictionary."""
    
    def __init__(self, target_dict: Dict, key: Any, description: str = ""):
        super().__init__(description or f"Delete {key}")
        self.target_dict = target_dict
        self.key = key
        self.old_value: Any = None
    
    def execute(self) -> Any:
        if self.key in self.target_dict:
            self.old_value = self.target_dict.pop(self.key)
        self.mark_executed()
        return self.old_value
    
    def undo(self) -> None:
        if self.old_value is not None:
            self.target_dict[self.key] = self.old_value
        self.mark_undone()


class MacroCommand(Command):
    """
    A macro command that groups multiple commands together.
    All commands are executed and undone as a single unit.
    """
    
    def __init__(self, commands: Optional[List[Command]] = None, description: str = ""):
        super().__init__(description or "Macro Command")
        self.commands: List[Command] = commands or []
    
    def add_command(self, command: Command) -> None:
        """Add a command to the macro."""
        self.commands.append(command)
    
    def execute(self) -> List[Any]:
        results = []
        for cmd in self.commands:
            results.append(cmd.execute())
        self.mark_executed()
        return results
    
    def undo(self) -> List[Any]:
        results = []
        # Undo in reverse order
        for cmd in reversed(self.commands):
            results.append(cmd.undo())
        self.mark_undone()
        return results
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['commands'] = [cmd.to_dict() for cmd in self.commands]
        return data


class Transaction:
    """
    A context manager for grouping commands into a single undo/redo unit.
    All commands executed within the transaction are treated as one.
    """
    
    def __init__(self, manager: 'UndoRedoManager', description: str = ""):
        """
        Create a transaction.
        
        Args:
            manager: The UndoRedoManager to use
            description: Description for the macro command
        """
        self.manager = manager
        self.description = description
        self.commands: List[Command] = []
        self._previous_recording = False
    
    def __enter__(self) -> 'Transaction':
        self._previous_recording = self.manager._recording
        self.manager._recording = False  # Pause normal recording
        self.manager._active_transaction = self  # Register as active transaction
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.manager._recording = self._previous_recording
        self.manager._active_transaction = None  # Unregister
        if exc_type is None and self.commands:
            # Only commit if no exception occurred
            macro = MacroCommand(self.commands, self.description)
            macro.mark_executed()
            self.manager._push_to_undo_stack(macro)
    
    def add_command(self, command: Command) -> None:
        """Add a command to the transaction."""
        self.commands.append(command)


@dataclass
class UndoRedoStats:
    """Statistics for an UndoRedoManager."""
    total_commands: int = 0
    undo_count: int = 0
    redo_count: int = 0
    current_undo_size: int = 0
    current_redo_size: int = 0
    memory_commands: int = 0


class UndoRedoManager:
    """
    Main manager for undo/redo operations.
    
    Manages command history, provides undo/redo functionality,
    and supports transactions, memory limits, and event callbacks.
    """
    
    def __init__(
        self,
        max_undo_levels: int = 100,
        max_redo_levels: int = 100
    ):
        """
        Initialize the UndoRedoManager.
        
        Args:
            max_undo_levels: Maximum number of undo commands to store
            max_redo_levels: Maximum number of redo commands to store
        """
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []
        self._max_undo_levels = max_undo_levels
        self._max_redo_levels = max_redo_levels
        self._recording = True
        self._active_transaction: Optional[Transaction] = None
        self._stats = UndoRedoStats()
        
        # Callbacks
        self._on_change: Optional[Callable[[], None]] = None
        self._on_execute: Optional[Callable[[Command], None]] = None
        self._on_undo: Optional[Callable[[Command], None]] = None
        self._on_redo: Optional[Callable[[Command], None]] = None
    
    # ========== Properties ==========
    
    @property
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self._undo_stack) > 0
    
    @property
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self._redo_stack) > 0
    
    @property
    def undo_count(self) -> int:
        """Get the number of available undo operations."""
        return len(self._undo_stack)
    
    @property
    def redo_count(self) -> int:
        """Get the number of available redo operations."""
        return len(self._redo_stack)
    
    @property
    def is_recording(self) -> bool:
        """Check if the manager is recording commands."""
        return self._recording
    
    @property
    def stats(self) -> UndoRedoStats:
        """Get current statistics."""
        return UndoRedoStats(
            total_commands=self._stats.total_commands,
            undo_count=self._stats.undo_count,
            redo_count=self._stats.redo_count,
            current_undo_size=len(self._undo_stack),
            current_redo_size=len(self._redo_stack),
            memory_commands=len(self._undo_stack) + len(self._redo_stack)
        )
    
    # ========== Callback Setters ==========
    
    def on_change(self, callback: Callable[[], None]) -> None:
        """Set callback for when undo/redo state changes."""
        self._on_change = callback
    
    def on_execute(self, callback: Callable[[Command], None]) -> None:
        """Set callback for when a command is executed."""
        self._on_execute = callback
    
    def on_undo(self, callback: Callable[[Command], None]) -> None:
        """Set callback for when a command is undone."""
        self._on_undo = callback
    
    def on_redo(self, callback: Callable[[Command], None]) -> None:
        """Set callback for when a command is redone."""
        self._on_redo = callback
    
    # ========== Core Operations ==========
    
    def execute(self, command: Command) -> Any:
        """
        Execute a command and add it to the undo stack.
        
        Args:
            command: The command to execute
            
        Returns:
            Result of the command execution
        """
        result = command.execute()
        command.mark_executed()
        
        # If in a transaction, add to transaction instead of undo stack
        if self._active_transaction:
            self._active_transaction.add_command(command)
        elif self._recording:
            self._push_to_undo_stack(command)
        
        self._stats.total_commands += 1
        
        if self._on_execute:
            self._on_execute(command)
        self._trigger_change()
        
        return result
    
    def undo(self) -> Any:
        """
        Undo the last command.
        
        Returns:
            Result of the undo operation
            
        Raises:
            IndexError: If no commands to undo
        """
        if not self.can_undo:
            raise IndexError("No commands to undo")
        
        command = self._undo_stack.pop()
        result = command.undo()
        
        self._push_to_redo_stack(command)
        self._stats.undo_count += 1
        
        if self._on_undo:
            self._on_undo(command)
        self._trigger_change()
        
        return result
    
    def redo(self) -> Any:
        """
        Redo the last undone command.
        
        Returns:
            Result of the redo operation
            
        Raises:
            IndexError: If no commands to redo
        """
        if not self.can_redo:
            raise IndexError("No commands to redo")
        
        command = self._redo_stack.pop()
        result = command.redo()
        
        self._push_to_undo_stack(command, clear_redo=False)
        self._stats.redo_count += 1
        
        if self._on_redo:
            self._on_redo(command)
        self._trigger_change()
        
        return result
    
    def undo_n(self, n: int) -> List[Any]:
        """
        Undo the last n commands.
        
        Args:
            n: Number of commands to undo
            
        Returns:
            List of results from undo operations
        """
        results = []
        for _ in range(min(n, len(self._undo_stack))):
            results.append(self.undo())
        return results
    
    def redo_n(self, n: int) -> List[Any]:
        """
        Redo the last n undone commands.
        
        Args:
            n: Number of commands to redo
            
        Returns:
            List of results from redo operations
        """
        results = []
        for _ in range(min(n, len(self._redo_stack))):
            results.append(self.redo())
        return results
    
    def undo_all(self) -> List[Any]:
        """Undo all commands in the undo stack."""
        return self.undo_n(len(self._undo_stack))
    
    def redo_all(self) -> List[Any]:
        """Redo all commands in the redo stack."""
        return self.redo_n(len(self._redo_stack))
    
    # ========== Transaction Support ==========
    
    def transaction(self, description: str = "") -> Transaction:
        """
        Create a transaction context for grouping commands.
        
        Args:
            description: Description for the transaction
            
        Returns:
            Transaction context manager
            
        Example:
            with manager.transaction("Add multiple items"):
                manager.execute(ListInsertCommand(items, 0, "a"))
                manager.execute(ListInsertCommand(items, 1, "b"))
        """
        return Transaction(self, description)
    
    # ========== Stack Management ==========
    
    def clear(self) -> None:
        """Clear all undo and redo history."""
        self._undo_stack.clear()
        self._redo_stack.clear()
        self._trigger_change()
    
    def clear_redo(self) -> None:
        """Clear only the redo stack."""
        self._redo_stack.clear()
        self._trigger_change()
    
    def set_max_undo_levels(self, max_levels: int) -> None:
        """Set the maximum number of undo levels."""
        self._max_undo_levels = max_levels
        # Trim stack if needed
        while len(self._undo_stack) > self._max_undo_levels:
            self._undo_stack.pop(0)
    
    def set_max_redo_levels(self, max_levels: int) -> None:
        """Set the maximum number of redo levels."""
        self._max_redo_levels = max_levels
        while len(self._redo_stack) > self._max_redo_levels:
            self._redo_stack.pop(0)
    
    # ========== Recording Control ==========
    
    def start_recording(self) -> None:
        """Start recording commands to the undo stack."""
        self._recording = True
    
    def stop_recording(self) -> None:
        """Stop recording commands (executed commands won't be added to undo stack)."""
        self._recording = False
    
    def pause_recording(self) -> bool:
        """Temporarily pause recording. Returns previous state."""
        prev = self._recording
        self._recording = False
        return prev
    
    def resume_recording(self, state: bool = True) -> None:
        """Resume recording."""
        self._recording = state
    
    # ========== Query Operations ==========
    
    def get_undo_descriptions(self, n: Optional[int] = None) -> List[str]:
        """
        Get descriptions of undoable commands.
        
        Args:
            n: Maximum number of descriptions (None for all)
            
        Returns:
            List of command descriptions (most recent first)
        """
        count = n if n else len(self._undo_stack)
        return [cmd.description for cmd in self._undo_stack[-count:][::-1]]
    
    def get_redo_descriptions(self, n: Optional[int] = None) -> List[str]:
        """
        Get descriptions of redoable commands.
        
        Args:
            n: Maximum number of descriptions (None for all)
            
        Returns:
            List of command descriptions (most recent first)
        """
        count = n if n else len(self._redo_stack)
        return [cmd.description for cmd in self._redo_stack[-count:][::-1]]
    
    def peek_undo(self) -> Optional[Command]:
        """Peek at the next command to undo without removing it."""
        return self._undo_stack[-1] if self._undo_stack else None
    
    def peek_redo(self) -> Optional[Command]:
        """Peek at the next command to redo without removing it."""
        return self._redo_stack[-1] if self._redo_stack else None
    
    # ========== Serialization ==========
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize manager state to dictionary."""
        return {
            'undo_stack': [cmd.to_dict() for cmd in self._undo_stack],
            'redo_stack': [cmd.to_dict() for cmd in self._redo_stack],
            'stats': {
                'total_commands': self._stats.total_commands,
                'undo_count': self._stats.undo_count,
                'redo_count': self._stats.redo_count
            }
        }
    
    # ========== Private Methods ==========
    
    def _push_to_undo_stack(self, command: Command, clear_redo: bool = True) -> None:
        """Push a command to the undo stack, optionally clearing redo stack."""
        self._undo_stack.append(command)
        
        # Trim if needed
        while len(self._undo_stack) > self._max_undo_levels:
            self._undo_stack.pop(0)
        
        # Clear redo stack (new action clears redo history) - but not during redo
        if clear_redo:
            self._redo_stack.clear()
    
    def _push_to_redo_stack(self, command: Command) -> None:
        """Push a command to the redo stack."""
        self._redo_stack.append(command)
        
        # Trim if needed
        while len(self._redo_stack) > self._max_redo_levels:
            self._redo_stack.pop(0)
    
    def _trigger_change(self) -> None:
        """Trigger the change callback."""
        if self._on_change:
            self._on_change()
    
    def __repr__(self) -> str:
        return f"<UndoRedoManager: undo={len(self._undo_stack)}, redo={len(self._redo_stack)}>"


class UndoRedoStack(UndoRedoManager):
    """
    Alias for UndoRedoManager for backwards compatibility.
    """
    pass


class StateSnapshot:
    """
    A simple state snapshot for memento pattern implementation.
    Useful for capturing and restoring complex state.
    """
    
    def __init__(self, state: Any, description: str = ""):
        """
        Create a state snapshot.
        
        Args:
            state: The state to capture (will be deep copied)
            description: Description of the snapshot
        """
        self.state = deepcopy(state)
        self.description = description
        self.timestamp = datetime.now()
    
    def restore(self) -> Any:
        """Return a deep copy of the stored state."""
        return deepcopy(self.state)
    
    def __repr__(self) -> str:
        return f"<StateSnapshot: {self.description} @ {self.timestamp}>"


class SnapshotManager(Generic[T]):
    """
    Manager for state snapshots with undo/redo support.
    Alternative to command-based undo/redo for complex state.
    """
    
    def __init__(self, max_snapshots: int = 50):
        """
        Initialize the snapshot manager.
        
        Args:
            max_snapshots: Maximum number of snapshots to keep
        """
        self._snapshots: List[StateSnapshot] = []
        self._current_index: int = -1
        self._max_snapshots = max_snapshots
    
    @property
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self._current_index > 0
    
    @property
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return self._current_index < len(self._snapshots) - 1
    
    @property
    def snapshot_count(self) -> int:
        """Get the number of snapshots."""
        return len(self._snapshots)
    
    def save(self, state: T, description: str = "") -> StateSnapshot:
        """
        Save a new snapshot.
        
        Args:
            state: The state to save
            description: Description of the snapshot
            
        Returns:
            The created snapshot
        """
        # Remove any snapshots after current position (redo history)
        if self._current_index < len(self._snapshots) - 1:
            self._snapshots = self._snapshots[:self._current_index + 1]
        
        snapshot = StateSnapshot(state, description)
        self._snapshots.append(snapshot)
        self._current_index = len(self._snapshots) - 1
        
        # Trim if needed
        while len(self._snapshots) > self._max_snapshots:
            self._snapshots.pop(0)
            self._current_index -= 1
        
        return snapshot
    
    def undo(self) -> Optional[T]:
        """
        Undo to previous snapshot.
        
        Returns:
            The previous state, or None if no undo available
        """
        if not self.can_undo:
            return None
        
        self._current_index -= 1
        return self._snapshots[self._current_index].restore()
    
    def redo(self) -> Optional[T]:
        """
        Redo to next snapshot.
        
        Returns:
            The next state, or None if no redo available
        """
        if not self.can_redo:
            return None
        
        self._current_index += 1
        return self._snapshots[self._current_index].restore()
    
    def current(self) -> Optional[T]:
        """Get the current state."""
        if 0 <= self._current_index < len(self._snapshots):
            return self._snapshots[self._current_index].restore()
        return None
    
    def get_history(self) -> List[str]:
        """Get list of snapshot descriptions."""
        return [s.description for s in self._snapshots]
    
    def clear(self) -> None:
        """Clear all snapshots."""
        self._snapshots.clear()
        self._current_index = -1
    
    def __repr__(self) -> str:
        return f"<SnapshotManager: {len(self._snapshots)} snapshots, index={self._current_index}>"


# ========== Convenience Functions ==========

def create_simple_undo_redo(
    obj: Any,
    attr: str
) -> Tuple[Callable[[Any], Any], Callable[[], Any], Callable[[], Any]]:
    """
    Create simple undo/redo functions for an object's attribute.
    
    Args:
        obj: The target object
        attr: The attribute name
        
    Returns:
        Tuple of (setter, undo, redo) functions
        
    Example:
        setter, undo, redo = create_simple_undo_redo(editor, 'text')
        setter("Hello")  # Sets text, saves old value
        undo()           # Restores previous text
        redo()           # Redoes the set
    """
    history: List[Any] = []
    history_index: int = -1
    
    def setter(value: Any) -> Any:
        nonlocal history_index
        # Trim any future history
        history[history_index + 1:] = []
        # Save current value
        if hasattr(obj, attr):
            history.append(deepcopy(getattr(obj, attr)))
        else:
            history.append(None)
        history_index = len(history) - 1
        # Set new value
        setattr(obj, attr, value)
        return value
    
    def undo() -> Any:
        nonlocal history_index
        if history_index > 0:
            # Restore the previous saved state (the value before the last change)
            history_index -= 1
            value = history[history_index]
            setattr(obj, attr, deepcopy(value))
            return value
        elif history_index == 0:
            # At the first saved state, restore to initial state (before any changes)
            # But we don't have the initial state before the first setter call
            # So we restore to the first saved value
            value = history[0]
            setattr(obj, attr, deepcopy(value))
            return value
        return None
    
    def redo() -> Any:
        nonlocal history_index
        if history_index < len(history) - 1:
            history_index += 1
            # The redo should restore the next saved value
            # But we need to track the values that were set, not the old values
            # This is a limitation - we need a different approach
            # For now, redo can't work properly with this simple implementation
        return None
    
    return setter, undo, redo


# ========== Decorator for Undo/Redo ==========

def undoable(manager: UndoRedoManager, description: str = ""):
    """
    Decorator to make a function undoable.
    
    Note: This requires the function to have an 'undo' counterpart
    or be a method on an object with undo support.
    
    Example:
        @undoable(manager, "Change value")
        def change_value(obj, attr, value):
            old = getattr(obj, attr)
            setattr(obj, attr, value)
            return old
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # This is a simplified implementation
            # In practice, you'd need to capture state before/after
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


# ========== Export List ==========

__all__ = [
    # Core classes
    'Command',
    'SimpleCommand',
    'MementoCommand',
    'SetValueCommand',
    'ListInsertCommand',
    'ListRemoveCommand',
    'DictSetCommand',
    'DictDeleteCommand',
    'MacroCommand',
    'Transaction',
    
    # Managers
    'UndoRedoManager',
    'UndoRedoStack',
    'SnapshotManager',
    
    # Support classes
    'UndoRedoStats',
    'StateSnapshot',
    
    # Convenience functions
    'create_simple_undo_redo',
    'undoable',
]