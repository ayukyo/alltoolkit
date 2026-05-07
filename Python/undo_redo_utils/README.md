# Undo/Redo Utilities

A zero-dependency, production-ready undo/redo implementation using the Command Pattern.

## Features

- **Command Pattern Implementation**: Full implementation of the Command design pattern for reversible operations
- **Unlimited or Limited History**: Configure maximum history size or use unlimited history
- **Transaction Support**: Batch multiple commands into a single undoable transaction
- **State Snapshots**: Memento pattern for simple state-based undo/redo
- **Savepoints**: Create and restore to named savepoints in history
- **Command Merging**: Automatically merge consecutive similar commands
- **Event Hooks**: Callback support for UI updates on history changes
- **Memory Efficient**: Only stores executed commands, not intermediate states
- **Thread-Safe**: Can be extended for multi-threaded applications

## Installation

No external dependencies required. Just copy the `mod.py` file to your project.

## Quick Start

### Basic Usage

```python
from undo_redo_utils import (
    Command, CommandResult, UndoRedoManager, SimpleCommand
)

# Define a simple counter
counter = {"value": 0}

# Create simple commands
def increment():
    counter["value"] += 1
    return counter["value"]

def decrement():
    counter["value"] -= 1
    return counter["value"]

# Create manager
manager = UndoRedoManager()

# Execute commands
cmd1 = SimpleCommand(increment, decrement, "Increment")
manager.execute(cmd1)

cmd2 = SimpleCommand(increment, decrement, "Increment")
manager.execute(cmd2)

print(counter["value"])  # 2

# Undo
manager.undo()
print(counter["value"])  # 1

# Redo
manager.redo()
print(counter["value"])  # 2
```

### Custom Command Class

```python
from undo_redo_utils import Command, CommandResult, UndoRedoManager

class AddTextCommand(Command):
    """Command to add text to a document."""
    
    def __init__(self, document, text, position):
        super().__init__(f"Add '{text}' at position {position}")
        self.document = document
        self.text = text
        self.position = position
    
    def do(self) -> CommandResult:
        self.document.insert(self.position, self.text)
        return CommandResult(success=True)
    
    def undo(self) -> CommandResult:
        self.document.delete(self.position, len(self.text))
        return CommandResult(success=True)

# Usage
doc = Document()  # Your document class
manager = UndoRedoManager()

manager.execute(AddTextCommand(doc, "Hello", 0))
manager.execute(AddTextCommand(doc, " World", 5))

manager.undo()  # Removes " World"
```

### Transactions

Group multiple commands into a single undoable unit:

```python
manager = UndoRedoManager()

# Begin transaction
manager.begin_transaction("Apply formatting")

manager.execute(BoldCommand(text, 0, 5))
manager.execute(ItalicCommand(text, 6, 10))
manager.execute(UnderlineCommand(text, 0, 15))

# Commit - all commands are now one undoable unit
manager.commit_transaction()

# Single undo reverts all three commands
manager.undo()

# Or rollback during transaction
manager.begin_transaction("Multiple changes")
manager.execute(cmd1)
manager.execute(cmd2)
manager.rollback_transaction()  # Undoes cmd1 and cmd2
```

### Savepoints

Create named restore points:

```python
manager = UndoRedoManager()

manager.execute(InitialSetupCommand())
manager.create_savepoint("after_setup")

manager.execute(MoreChangesCommand())
manager.execute(EvenMoreChangesCommand())

# Restore to savepoint
manager.restore_savepoint("after_setup")  # Undoes to after initial setup

# Clean up savepoint
manager.delete_savepoint("after_setup")
```

### Memento Pattern (State-Based)

For simple state objects, use the MementoManager:

```python
from undo_redo_utils import MementoManager

# Initialize with state
state = {
    "text": "",
    "cursor": 0,
    "selection": None
}

manager = MementoManager(state)

# Make changes and save snapshots
state["text"] = "Hello"
manager.save("Typed 'Hello'")

state["text"] += " World"
manager.save("Typed ' World'")

# Undo
manager.undo()
print(manager.current_state["text"])  # "Hello"

# Redo
manager.redo()
print(manager.current_state["text"])  # "Hello World"
```

### Command Merging

Merge consecutive similar commands automatically:

```python
class IncrementCommand(Command):
    def __init__(self, counter, amount=1):
        super().__init__(f"Add {amount}")
        self.counter = counter
        self.amount = amount
    
    def do(self):
        self.counter.value += self.amount
        return CommandResult(success=True)
    
    def undo(self):
        self.counter.value -= self.amount
        return CommandResult(success=True)
    
    def can_merge_with(self, other):
        # Can merge with another increment for same counter
        return isinstance(other, IncrementCommand)
    
    def merge_with(self, other):
        # Create combined command
        return IncrementCommand(self.counter, self.amount + other.amount)

manager = UndoRedoManager()
counter = Counter()

manager.execute(IncrementCommand(counter, 1))
manager.execute(IncrementCommand(counter, 1))
manager.execute(IncrementCommand(counter, 1))

# Only one undo needed!
manager.undo()  # Reverts all three increments
```

### UI Integration

```python
def on_history_change():
    update_undo_button(manager.can_undo)
    update_redo_button(manager.can_redo)
    update_undo_menu(manager.get_undo_descriptions(10))
    update_redo_menu(manager.get_redo_descriptions(10))

manager = UndoRedoManager(on_change=on_history_change)

# Now every execute/undo/redo triggers UI update
```

## API Reference

### Command (Abstract Base Class)

- `do() -> CommandResult`: Execute the command
- `undo() -> CommandResult`: Undo the command
- `redo() -> CommandResult`: Redo the command (default: calls do())
- `can_merge_with(other) -> bool`: Check if mergeable with another command
- `merge_with(other) -> Command`: Merge with another command
- `is_executed -> bool`: Whether command has been executed

### SimpleCommand

Convenience class for wrapping functions:

```python
cmd = SimpleCommand(
    do_func=lambda: action(),
    undo_func=lambda: reverse(),
    description="My action"
)
```

### UndoRedoManager

Main manager class:

- `execute(command) -> CommandResult`: Execute and track a command
- `undo(steps=1) -> List[CommandResult]`: Undo commands
- `redo(steps=1) -> List[CommandResult]`: Redo commands
- `begin_transaction(name="")`: Start a transaction
- `commit_transaction() -> CommandResult`: Commit current transaction
- `rollback_transaction()`: Rollback current transaction
- `create_savepoint(name)`: Create a named savepoint
- `restore_savepoint(name)`: Restore to a savepoint
- `clear()`: Clear all history
- `can_undo -> bool`: Whether undo is possible
- `can_redo -> bool`: Whether redo is possible
- `undo_count -> int`: Number of undoable commands
- `redo_count -> int`: Number of redoable commands

### MementoManager

State-based manager:

- `save(description="")`: Save current state to history
- `undo() -> Optional[T]`: Restore previous state
- `redo() -> Optional[T]`: Restore next state
- `set_state(state, description="")`: Set new state and save
- `clear()`: Clear all history
- `current_state -> T`: Current state object

### CommandResult

Result object:

- `success: bool`: Whether operation succeeded
- `message: Optional[str]`: Optional message
- `data: Optional[Any]`: Optional result data

## Use Cases

- **Text Editors**: Document editing with undo/redo
- **Drawing Applications**: Canvas operations with reversible actions
- **Form State Management**: Form field changes with undo capability
- **Game State**: Turn-based games with move history
- **Configuration Management**: Settings changes with rollback
- **Data Transformation**: Reversible data operations

## License

MIT License - Part of AllToolkit