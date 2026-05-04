"""
AllToolkit - Python Undo/Redo Utilities

A zero-dependency, production-ready undo/redo implementation using the Command Pattern.
Supports command history, transaction batching, state snapshots, and more.

Features:
- Command Pattern implementation
- Unlimited or limited history
- Transaction support (batch multiple commands)
- State snapshot and restore
- Memento pattern for complex states
- Event hooks for UI updates
- Memory-efficient implementation

Author: AllToolkit
License: MIT
"""

from typing import Any, Callable, Dict, List, Optional, Generic, TypeVar
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod
import copy


T = TypeVar('T')
CommandId = str


class UndoRedoError(Exception):
    """Base exception for undo/redo operations."""
    pass


class CannotUndoError(UndoRedoError):
    """Raised when undo is not possible."""
    pass


class CannotRedoError(UndoRedoError):
    """Raised when redo is not possible."""
    pass


class TransactionError(UndoRedoError):
    """Raised when there's an issue with transactions."""
    pass


class CommandType(Enum):
    """Types of commands."""
    NORMAL = "normal"
    TRANSACTION_START = "transaction_start"
    TRANSACTION_END = "transaction_end"
    SNAPSHOT = "snapshot"


@dataclass
class CommandResult:
    """Result of executing a command."""
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None
    timestamp: datetime = field(default_factory=datetime.now)


class Command(ABC):
    """
    Abstract base class for all commands.
    
    Commands encapsulate actions that can be undone and redone.
    Implement do() and undo() methods for your specific actions.
    
    Example:
        >>> class AddTextCommand(Command):
        ...     def __init__(self, editor, text, position):
        ...         self.editor = editor
        ...         self.text = text
        ...         self.position = position
        ...     
        ...     def do(self) -> CommandResult:
        ...         self.editor.insert_text(self.position, self.text)
        ...         return CommandResult(success=True)
        ...     
        ...     def undo(self) -> CommandResult:
        ...         self.editor.delete_text(self.position, len(self.text))
        ...         return CommandResult(success=True)
    """
    
    def __init__(self, description: str = "", id: Optional[CommandId] = None):
        """
        Initialize command.
        
        Args:
            description: Human-readable description of the command
            id: Optional unique identifier for the command
        """
        self.description = description
        self.id = id or self._generate_id()
        self.timestamp = datetime.now()
        self._executed = False
    
    @staticmethod
    def _generate_id() -> str:
        """Generate a unique command ID."""
        import time
        import random
        return f"cmd_{int(time.time() * 1000000)}_{random.randint(1000, 9999)}"
    
    @abstractmethod
    def do(self) -> CommandResult:
        """
        Execute the command.
        
        Returns:
            CommandResult with success status and optional data
        """
        pass
    
    @abstractmethod
    def undo(self) -> CommandResult:
        """
        Undo the command.
        
        Returns:
            CommandResult with success status and optional data
        """
        pass
    
    def redo(self) -> CommandResult:
        """
        Redo the command. Default implementation calls do().
        Override if redo behavior differs from initial execution.
        
        Returns:
            CommandResult with success status and optional data
        """
        return self.do()
    
    def can_merge_with(self, other: 'Command') -> bool:
        """
        Check if this command can be merged with another command.
        Useful for combining consecutive similar commands.
        
        Args:
            other: Another command to potentially merge with
            
        Returns:
            True if commands can be merged
        """
        return False
    
    def merge_with(self, other: 'Command') -> 'Command':
        """
        Merge this command with another command.
        
        Args:
            other: Command to merge with
            
        Returns:
            New merged command
        """
        raise NotImplementedError("merge_with not implemented")
    
    @property
    def is_executed(self) -> bool:
        """Check if command has been executed."""
        return self._executed


class SimpleCommand(Command):
    """
    A simple command that wraps functions for do and undo operations.
    Useful for quick, one-off commands without creating a full class.
    
    Example:
        >>> cmd = SimpleCommand(
        ...     do_func=lambda: set_value(10),
        ...     undo_func=lambda: set_value(0),
        ...     description="Set value to 10"
        ... )
    """
    
    def __init__(
        self,
        do_func: Callable[[], Any],
        undo_func: Callable[[], Any],
        description: str = "",
        id: Optional[CommandId] = None
    ):
        super().__init__(description, id)
        self._do_func = do_func
        self._undo_func = undo_func
    
    def do(self) -> CommandResult:
        result = self._do_func()
        self._executed = True
        return CommandResult(success=True, data=result)
    
    def undo(self) -> CommandResult:
        result = self._undo_func()
        self._executed = False
        return CommandResult(success=True, data=result)


class StateCommand(Command):
    """
    A command that stores and restores state using snapshots.
    Useful for complex objects where full state capture is easier
    than incremental changes.
    
    Example:
        >>> class EditorStateCommand(StateCommand):
        ...     def __init__(self, editor):
        ...         super().__init__("Editor change")
        ...         self.editor = editor
        ...         self.old_state = None
        ...     
        ...     def do(self):
        ...         if self.old_state is None:
        ...             self.old_state = self.capture_state()
        ...         # Make changes...
        ...         return CommandResult(success=True)
        ...     
        ...     def undo(self):
        ...         self.restore_state(self.old_state)
        ...         return CommandResult(success=True)
    """
    
    @abstractmethod
    def capture_state(self) -> Any:
        """Capture current state."""
        pass
    
    @abstractmethod
    def restore_state(self, state: Any) -> None:
        """Restore to a previous state."""
        pass


@dataclass
class HistoryEntry:
    """Entry in the command history."""
    command: Command
    timestamp: datetime
    result: Optional[CommandResult] = None


class UndoRedoManager:
    """
    Main manager for undo/redo operations.
    
    Manages a stack of executed commands and provides undo/redo functionality.
    Supports transactions, history limits, and event hooks.
    
    Example:
        >>> manager = UndoRedoManager(max_history=100)
        >>> manager.execute(AddTextCommand(editor, "Hello", 0))
        >>> manager.undo()  # Undoes the add text command
        >>> manager.redo()  # Redoes the add text command
        >>> manager.can_undo  # False
    """
    
    def __init__(
        self,
        max_history: Optional[int] = None,
        on_change: Optional[Callable[[], None]] = None
    ):
        """
        Initialize the undo/redo manager.
        
        Args:
            max_history: Maximum number of commands to keep (None = unlimited)
            on_change: Callback to call when history changes
        """
        self._undo_stack: List[HistoryEntry] = []
        self._redo_stack: List[HistoryEntry] = []
        self._max_history = max_history
        self._on_change = on_change
        self._in_transaction = False
        self._transaction_commands: List[Command] = []
        self._transaction_name = ""
        self._savepoints: Dict[str, int] = {}
    
    @property
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return len(self._undo_stack) > 0 and not self._in_transaction
    
    @property
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return len(self._redo_stack) > 0 and not self._in_transaction
    
    @property
    def undo_count(self) -> int:
        """Get number of undoable commands."""
        return len(self._undo_stack)
    
    @property
    def redo_count(self) -> int:
        """Get number of redoable commands."""
        return len(self._redo_stack)
    
    @property
    def history(self) -> List[HistoryEntry]:
        """Get a copy of the undo history."""
        return self._undo_stack.copy()
    
    @property
    def in_transaction(self) -> bool:
        """Check if currently in a transaction."""
        return self._in_transaction
    
    def execute(self, command: Command) -> CommandResult:
        """
        Execute a command and add it to the history.
        
        Args:
            command: Command to execute
            
        Returns:
            CommandResult from the execution
        """
        if self._in_transaction:
            self._transaction_commands.append(command)
            result = command.do()
            return result
        
        # Execute the command
        result = command.do()
        command._executed = True
        
        # Check for merge with last command
        if self._undo_stack and self._undo_stack[-1].command.can_merge_with(command):
            merged = self._undo_stack[-1].command.merge_with(command)
            self._undo_stack[-1] = HistoryEntry(
                command=merged,
                timestamp=datetime.now(),
                result=result
            )
        else:
            # Add to undo stack
            entry = HistoryEntry(
                command=command,
                timestamp=datetime.now(),
                result=result
            )
            self._undo_stack.append(entry)
        
        # Clear redo stack when new command is executed
        self._redo_stack.clear()
        
        # Enforce history limit
        self._enforce_limit()
        
        # Notify listeners
        self._notify_change()
        
        return result
    
    def undo(self, steps: int = 1) -> List[CommandResult]:
        """
        Undo the last command(s).
        
        Args:
            steps: Number of commands to undo (default: 1)
            
        Returns:
            List of CommandResults from undo operations
            
        Raises:
            CannotUndoError: If undo is not possible
        """
        if self._in_transaction:
            raise TransactionError("Cannot undo during a transaction")
        
        if not self.can_undo:
            raise CannotUndoError("No commands to undo")
        
        steps = min(steps, len(self._undo_stack))
        results = []
        
        for _ in range(steps):
            entry = self._undo_stack.pop()
            result = entry.command.undo()
            entry.command._executed = False
            entry.result = result
            self._redo_stack.append(entry)
            results.append(result)
        
        self._notify_change()
        return results
    
    def redo(self, steps: int = 1) -> List[CommandResult]:
        """
        Redo previously undone command(s).
        
        Args:
            steps: Number of commands to redo (default: 1)
            
        Returns:
            List of CommandResults from redo operations
            
        Raises:
            CannotRedoError: If redo is not possible
        """
        if self._in_transaction:
            raise TransactionError("Cannot redo during a transaction")
        
        if not self.can_redo:
            raise CannotRedoError("No commands to redo")
        
        steps = min(steps, len(self._redo_stack))
        results = []
        
        for _ in range(steps):
            entry = self._redo_stack.pop()
            result = entry.command.redo()
            entry.command._executed = True
            entry.result = result
            self._undo_stack.append(entry)
            results.append(result)
        
        self._enforce_limit()
        self._notify_change()
        return results
    
    def begin_transaction(self, name: str = "") -> None:
        """
        Begin a transaction. All subsequent commands will be grouped.
        
        Args:
            name: Optional name for the transaction
            
        Raises:
            TransactionError: If already in a transaction
        """
        if self._in_transaction:
            raise TransactionError("Already in a transaction")
        
        self._in_transaction = True
        self._transaction_commands = []
        self._transaction_name = name
    
    def commit_transaction(self) -> CommandResult:
        """
        Commit the current transaction.
        
        Returns:
            CommandResult for the transaction
            
        Raises:
            TransactionError: If not in a transaction
        """
        if not self._in_transaction:
            raise TransactionError("Not in a transaction")
        
        commands = self._transaction_commands
        name = self._transaction_name
        self._in_transaction = False
        self._transaction_commands = []
        self._transaction_name = ""
        
        if not commands:
            return CommandResult(success=True, message="Empty transaction")
        
        # Create a transaction command (commands already executed)
        transaction_cmd = TransactionCommand(commands, name, execute_commands=False)
        
        # Add directly to undo stack without re-executing
        entry = HistoryEntry(
            command=transaction_cmd,
            timestamp=datetime.now(),
            result=CommandResult(success=True)
        )
        self._undo_stack.append(entry)
        transaction_cmd._executed = True
        
        # Clear redo stack
        self._redo_stack.clear()
        
        # Enforce history limit
        self._enforce_limit()
        
        # Notify listeners
        self._notify_change()
        
        return CommandResult(success=True, message=f"Transaction committed: {name or f'{len(commands)} commands'}")
    
    def rollback_transaction(self) -> None:
        """
        Rollback the current transaction by undoing all commands.
        
        Raises:
            TransactionError: If not in a transaction
        """
        if not self._in_transaction:
            raise TransactionError("Not in a transaction")
        
        # Undo all transaction commands in reverse order
        for cmd in reversed(self._transaction_commands):
            if cmd.is_executed:
                cmd.undo()
        
        self._in_transaction = False
        self._transaction_commands = []
        self._transaction_name = ""
        self._notify_change()
    
    def create_savepoint(self, name: str) -> None:
        """
        Create a savepoint at the current position in history.
        
        Args:
            name: Name for the savepoint
        """
        self._savepoints[name] = len(self._undo_stack)
    
    def restore_savepoint(self, name: str) -> None:
        """
        Restore to a previously created savepoint.
        
        Args:
            name: Name of the savepoint
            
        Raises:
            UndoRedoError: If savepoint doesn't exist
        """
        if name not in self._savepoints:
            raise UndoRedoError(f"Savepoint '{name}' does not exist")
        
        target = self._savepoints[name]
        current = len(self._undo_stack)
        
        if target < current:
            # Undo to reach savepoint
            self.undo(current - target)
        elif target > current:
            # Redo to reach savepoint (if possible)
            raise UndoRedoError("Cannot redo to savepoint - history was modified")
    
    def delete_savepoint(self, name: str) -> bool:
        """
        Delete a savepoint.
        
        Args:
            name: Name of the savepoint
            
        Returns:
            True if savepoint was deleted
        """
        if name in self._savepoints:
            del self._savepoints[name]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all history."""
        self._undo_stack.clear()
        self._redo_stack.clear()
        self._savepoints.clear()
        self._notify_change()
    
    def get_undo_descriptions(self, count: Optional[int] = None) -> List[str]:
        """
        Get descriptions of undoable commands.
        
        Args:
            count: Maximum number to return (None = all)
            
        Returns:
            List of command descriptions
        """
        if count is None:
            count = len(self._undo_stack)
        
        entries = self._undo_stack[-count:]
        return [
            f"{e.command.description or e.command.id}"
            for e in reversed(entries)
        ]
    
    def get_redo_descriptions(self, count: Optional[int] = None) -> List[str]:
        """
        Get descriptions of redoable commands.
        
        Args:
            count: Maximum number to return (None = all)
            
        Returns:
            List of command descriptions
        """
        if count is None:
            count = len(self._redo_stack)
        
        entries = self._redo_stack[-count:]
        return [
            f"{e.command.description or e.command.id}"
            for e in reversed(entries)
        ]
    
    def _enforce_limit(self) -> None:
        """Enforce the history limit by removing oldest entries."""
        if self._max_history is None:
            return
        
        while len(self._undo_stack) > self._max_history:
            self._undo_stack.pop(0)
    
    def _notify_change(self) -> None:
        """Notify listeners of history changes."""
        if self._on_change:
            self._on_change()


class TransactionCommand(Command):
    """
    A command that groups multiple commands into a single transaction.
    All commands are executed and undone together.
    
    Note: Commands passed to this class are assumed to have been
    already executed (if coming from UndoRedoManager.commit_transaction).
    Use execute_commands=True to execute them during do().
    """
    
    def __init__(self, commands: List[Command], description: str = "", execute_commands: bool = False):
        super().__init__(description or f"Transaction ({len(commands)} commands)")
        self._commands = commands
        self._execute_commands = execute_commands
    
    def do(self) -> CommandResult:
        """Execute all commands in order (if execute_commands=True)."""
        if self._execute_commands:
            executed = []
            for cmd in self._commands:
                result = cmd.do()
                if not result.success:
                    # Rollback executed commands on failure
                    for executed_cmd in reversed(executed):
                        executed_cmd.undo()
                    return CommandResult(
                        success=False,
                        message=f"Transaction failed at command: {cmd.description}"
                    )
                executed.append(cmd)
        
        self._executed = True
        return CommandResult(
            success=True,
            message=f"Transaction with {len(self._commands)} commands"
        )
    
    def undo(self) -> CommandResult:
        """Undo all commands in reverse order."""
        for cmd in reversed(self._commands):
            cmd.undo()
        
        self._executed = False
        return CommandResult(
            success=True,
            message=f"Undid {len(self._commands)} commands"
        )
    
    def get_commands(self) -> List[Command]:
        """Get the list of commands in this transaction."""
        return self._commands.copy()


class Memento(Generic[T]):
    """
    A memento object that stores state.
    Used with MementoManager for full state snapshots.
    """
    
    def __init__(self, state: T, description: str = ""):
        self.state = copy.deepcopy(state)
        self.description = description
        self.timestamp = datetime.now()


class MementoManager(Generic[T]):
    """
    A simpler undo/redo manager that works with full state snapshots.
    Useful when state is small and cheap to copy.
    
    Example:
        >>> manager = MementoManager(initial_state={"text": ""})
        >>> manager.save("Added 'Hello'")
        >>> manager.current_state["text"] = "Hello"
        >>> manager.undo()  # Returns previous state
    """
    
    def __init__(
        self,
        initial_state: T,
        max_history: Optional[int] = None,
        on_change: Optional[Callable[[T], None]] = None
    ):
        """
        Initialize the memento manager.
        
        Args:
            initial_state: Initial state object
            max_history: Maximum snapshots to keep (None = unlimited)
            on_change: Callback when state changes
        """
        self._current_state = copy.deepcopy(initial_state)
        self._undo_stack: List[Memento[T]] = []
        self._redo_stack: List[Memento[T]] = []
        self._max_history = max_history
        self._on_change = on_change
    
    @property
    def current_state(self) -> T:
        """Get the current state."""
        return self._current_state
    
    @property
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return len(self._undo_stack) > 0
    
    @property
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return len(self._redo_stack) > 0
    
    def save(self, description: str = "") -> None:
        """
        Save current state to history, creating a checkpoint.
        
        After calling save(), the current state becomes the state to UNDO TO.
        
        Args:
            description: Description of this state
        """
        # Save the current state as a point to return to when undoing
        memento = Memento(copy.deepcopy(self._current_state), description)
        self._undo_stack.append(memento)
        self._redo_stack.clear()
        self._enforce_limit()
    
    def undo(self) -> Optional[T]:
        """
        Undo to previous state.
        
        Returns:
            The previous state, or None if cannot undo
        """
        if not self.can_undo:
            return None
        
        # Save current state to redo stack
        current = Memento(self._current_state)
        self._redo_stack.append(current)
        
        # Restore previous state
        memento = self._undo_stack.pop()
        self._current_state = copy.deepcopy(memento.state)
        
        self._notify_change()
        return self._current_state
    
    def redo(self) -> Optional[T]:
        """
        Redo to next state.
        
        Returns:
            The next state, or None if cannot redo
        """
        if not self.can_redo:
            return None
        
        # Save current state to undo stack
        current = Memento(self._current_state)
        self._undo_stack.append(current)
        
        # Restore next state
        memento = self._redo_stack.pop()
        self._current_state = copy.deepcopy(memento.state)
        
        self._enforce_limit()
        self._notify_change()
        return self._current_state
    
    def set_state(self, state: T, description: str = "") -> None:
        """
        Set a new state and save to history.
        
        Args:
            state: New state
            description: Description of the change
        """
        self.save(description)
        self._current_state = copy.deepcopy(state)
        self._notify_change()
    
    def clear(self) -> None:
        """Clear all history."""
        self._undo_stack.clear()
        self._redo_stack.clear()
    
    def _enforce_limit(self) -> None:
        """Enforce history limit."""
        if self._max_history is None:
            return
        
        while len(self._undo_stack) > self._max_history:
            self._undo_stack.pop(0)
    
    def _notify_change(self) -> None:
        """Notify listeners of state change."""
        if self._on_change:
            self._on_change(self._current_state)


# Convenience functions

def create_simple_manager(max_history: Optional[int] = None) -> UndoRedoManager:
    """
    Create a new UndoRedoManager instance.
    
    Args:
        max_history: Maximum commands to keep (None = unlimited)
        
    Returns:
        New UndoRedoManager instance
    """
    return UndoRedoManager(max_history=max_history)


def create_memento_manager(
    initial_state: T,
    max_history: Optional[int] = None
) -> MementoManager[T]:
    """
    Create a new MementoManager instance.
    
    Args:
        initial_state: Initial state object
        max_history: Maximum snapshots to keep (None = unlimited)
        
    Returns:
        New MementoManager instance
    """
    return MementoManager(initial_state=initial_state, max_history=max_history)