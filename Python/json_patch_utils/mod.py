"""
JSON Patch Utils - RFC 6902 JSON Patch and RFC 6901 JSON Pointer Implementation

A zero-dependency implementation of JSON Patch for applying and creating
patch operations on JSON documents.

Operations supported:
- add: Add a value at a location
- remove: Remove a value at a location
- replace: Replace a value at a location
- move: Move a value from one location to another
- copy: Copy a value from one location to another
- test: Test that a value at a location equals a specified value

Author: AllToolkit
License: MIT
"""

import json
import copy
from typing import Any, List, Dict, Optional, Union, Tuple


class JsonPatchError(Exception):
    """Base exception for JSON Patch errors."""
    pass


class JsonPointerError(JsonPatchError):
    """Exception for JSON Pointer errors."""
    pass


class JsonPatchTestError(JsonPatchError):
    """Exception raised when a test operation fails."""
    def __init__(self, path: str, expected: Any, actual: Any):
        self.path = path
        self.expected = expected
        self.actual = actual
        super().__init__(f"Test failed at '{path}': expected {expected!r}, got {actual!r}")


class JsonPatchOperationError(JsonPatchError):
    """Exception for operation-specific errors."""
    pass


class JsonPointer:
    """
    RFC 6901 JSON Pointer implementation.
    
    JSON Pointer is a string syntax for identifying a specific value
    within a JSON document.
    
    Examples:
        ""      -> entire document
        "/foo"  -> document["foo"]
        "/foo/0" -> document["foo"][0]
        "/foo/bar~0baz" -> document["foo"]["bar~baz"]
    """
    
    def __init__(self, pointer: str = ""):
        """
        Initialize a JSON Pointer.
        
        Args:
            pointer: JSON Pointer string (empty string for root)
        """
        if pointer and not pointer.startswith('/'):
            raise JsonPointerError(f"Invalid JSON Pointer: '{pointer}' (must start with '/' or be empty)")
        self.pointer = pointer
    
    def __repr__(self) -> str:
        return f"JsonPointer('{self.pointer}')"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, JsonPointer):
            return self.pointer == other.pointer
        if isinstance(other, str):
            return self.pointer == other
        return False
    
    @staticmethod
    def unescape(token: str) -> str:
        """
        Unescape a JSON Pointer token.
        
        '~1' -> '/'
        '~0' -> '~'
        
        Args:
            token: Escaped token string
            
        Returns:
            Unescaped token string
        """
        # Order matters: ~0 must be processed after ~1 to avoid double unescaping
        return token.replace('~1', '/').replace('~0', '~')
    
    @staticmethod
    def escape(token: str) -> str:
        """
        Escape a string for use in a JSON Pointer.
        
        '~' -> '~0'
        '/' -> '~1'
        
        Args:
            token: Unescaped token string
            
        Returns:
            Escaped token string
        """
        return token.replace('~', '~0').replace('/', '~1')
    
    def tokens(self) -> List[str]:
        """
        Get the list of unescaped tokens in the pointer.
        
        Returns:
            List of token strings
        """
        if not self.pointer:
            return []
        # Split and unescape each token
        return [self.unescape(t) for t in self.pointer.split('/')[1:]]
    
    def get(self, document: Any) -> Any:
        """
        Get the value at the pointer location.
        
        Args:
            document: JSON document (any valid JSON value)
            
        Returns:
            Value at the pointer location
            
        Raises:
            JsonPointerError: If the path doesn't exist
        """
        tokens = self.tokens()
        value = document
        
        for i, token in enumerate(tokens):
            try:
                if isinstance(value, dict):
                    if token not in value:
                        path = '/' + '/'.join(tokens[:i+1])
                        raise JsonPointerError(f"Key '{token}' not found at '{path}'")
                    value = value[token]
                elif isinstance(value, list):
                    if token == '-':
                        raise JsonPointerError("Array index '-' is only valid for add operations")
                    try:
                        index = int(token)
                        if index < 0 or index >= len(value):
                            path = '/' + '/'.join(tokens[:i+1])
                            raise JsonPointerError(f"Array index {index} out of range at '{path}'")
                        value = value[index]
                    except ValueError:
                        path = '/' + '/'.join(tokens[:i+1])
                        raise JsonPointerError(f"Invalid array index '{token}' at '{path}'")
                else:
                    path = '/' + '/'.join(tokens[:i+1])
                    raise JsonPointerError(f"Cannot traverse non-object/array at '{path}'")
            except JsonPointerError:
                raise
            except Exception as e:
                path = '/' + '/'.join(tokens[:i+1])
                raise JsonPointerError(f"Error accessing '{path}': {e}")
        
        return value
    
    def get_parent_and_key(self, document: Any) -> Tuple[Any, Union[str, int], bool]:
        """
        Get the parent container and key/index for the last token.
        
        Args:
            document: JSON document
            
        Returns:
            Tuple of (parent, key/index, is_new_for_array)
            is_new_for_array is True if key is '-' (append to array)
            
        Raises:
            JsonPointerError: If parent path doesn't exist
        """
        tokens = self.tokens()
        if not tokens:
            raise JsonPointerError("Cannot get parent of root pointer")
        
        parent_tokens = tokens[:-1]
        last_token = tokens[-1]
        
        parent = document
        for token in parent_tokens:
            if isinstance(parent, dict):
                if token not in parent:
                    raise JsonPointerError(f"Key '{token}' not found")
                parent = parent[token]
            elif isinstance(parent, list):
                try:
                    index = int(token)
                    parent = parent[index]
                except (ValueError, IndexError):
                    raise JsonPointerError(f"Invalid array access at '{token}'")
            else:
                raise JsonPointerError(f"Cannot traverse non-object/array")
        
        # Check if appending to array
        is_new_for_array = isinstance(parent, list) and last_token == '-'
        
        if isinstance(parent, list):
            if is_new_for_array:
                return parent, len(parent), True
            try:
                index = int(last_token)
                return parent, index, False
            except ValueError:
                raise JsonPointerError(f"Invalid array index '{last_token}'")
        elif isinstance(parent, dict):
            return parent, last_token, False
        else:
            raise JsonPointerError(f"Parent is not a container")
    
    @classmethod
    def from_tokens(cls, tokens: List[str]) -> 'JsonPointer':
        """
        Create a JSON Pointer from a list of tokens.
        
        Args:
            tokens: List of unescaped tokens
            
        Returns:
            JsonPointer instance
        """
        if not tokens:
            return cls("")
        escaped = [cls.escape(t) for t in tokens]
        return cls('/' + '/'.join(escaped))
    
    def append(self, token: str) -> 'JsonPointer':
        """
        Create a new pointer by appending a token.
        
        Args:
            token: Token to append (will be escaped)
            
        Returns:
            New JsonPointer instance
        """
        if not self.pointer:
            return JsonPointer('/' + self.escape(token))
        return JsonPointer(self.pointer + '/' + self.escape(token))


class JsonPatch:
    """
    RFC 6902 JSON Patch implementation.
    
    JSON Patch is a format for describing changes to a JSON document.
    A JSON Patch document is a list of operations to apply.
    
    Operations:
        - add: {"op": "add", "path": "/foo", "value": "bar"}
        - remove: {"op": "remove", "path": "/foo"}
        - replace: {"op": "replace", "path": "/foo", "value": "bar"}
        - move: {"op": "move", "from": "/foo", "path": "/bar"}
        - copy: {"op": "copy", "from": "/foo", "path": "/bar"}
        - test: {"op": "test", "path": "/foo", "value": "bar"}
    
    Example:
        >>> doc = {"foo": "bar"}
        >>> patch = JsonPatch([{"op": "add", "path": "/baz", "value": "qux"}])
        >>> result = patch.apply(doc)
        >>> result
        {'foo': 'bar', 'baz': 'qux'}
    """
    
    def __init__(self, operations: Union[List[Dict], str]):
        """
        Initialize a JSON Patch.
        
        Args:
            operations: List of operation dicts or JSON string
        """
        if isinstance(operations, str):
            operations = json.loads(operations)
        
        if not isinstance(operations, list):
            raise JsonPatchError("JSON Patch must be a list of operations")
        
        self.operations = operations
        self._validate_operations()
    
    def _validate_operations(self) -> None:
        """Validate all operations in the patch."""
        valid_ops = {'add', 'remove', 'replace', 'move', 'copy', 'test'}
        
        for i, op in enumerate(self.operations):
            if not isinstance(op, dict):
                raise JsonPatchError(f"Operation {i} must be an object")
            
            if 'op' not in op:
                raise JsonPatchError(f"Operation {i} missing 'op' field")
            
            if op['op'] not in valid_ops:
                raise JsonPatchError(f"Operation {i} has invalid op: {op['op']}")
            
            if 'path' not in op:
                raise JsonPatchError(f"Operation {i} missing 'path' field")
            
            if op['op'] in {'add', 'replace', 'test'}:
                if 'value' not in op:
                    raise JsonPatchError(f"Operation {i} ({op['op']}) missing 'value' field")
            
            if op['op'] in {'move', 'copy'}:
                if 'from' not in op:
                    raise JsonPatchError(f"Operation {i} ({op['op']}) missing 'from' field")
    
    def apply(self, document: Any, in_place: bool = False) -> Any:
        """
        Apply the patch to a document.
        
        Args:
            document: JSON document to patch
            in_place: If True, modify the original document; otherwise, create a copy
            
        Returns:
            Patched document
            
        Raises:
            JsonPatchTestError: If a test operation fails
            JsonPatchError: If an operation cannot be applied
        """
        if not in_place:
            document = copy.deepcopy(document)
        
        for op in self.operations:
            document = self._apply_operation(document, op)
        
        return document
    
    def _apply_operation(self, document: Any, op: Dict) -> Any:
        """Apply a single operation to the document."""
        op_type = op['op']
        path = JsonPointer(op['path'])
        tokens = path.tokens()
        
        if op_type == 'add':
            return self._op_add(document, tokens, op['value'])
        elif op_type == 'remove':
            return self._op_remove(document, tokens)
        elif op_type == 'replace':
            return self._op_replace(document, tokens, op['value'])
        elif op_type == 'move':
            return self._op_move(document, tokens, JsonPointer(op['from']))
        elif op_type == 'copy':
            return self._op_copy(document, tokens, JsonPointer(op['from']))
        elif op_type == 'test':
            return self._op_test(document, path, op['value'])
        else:
            raise JsonPatchOperationError(f"Unknown operation: {op_type}")
    
    def _op_add(self, document: Any, tokens: List[str], value: Any) -> Any:
        """Add a value at the specified path."""
        if not tokens:
            # Adding at root replaces entire document
            return copy.deepcopy(value)
        
        # Navigate to parent
        parent = document
        path_stack = [document]
        
        for i, token in enumerate(tokens[:-1]):
            if isinstance(parent, dict):
                parent = parent[token]
            elif isinstance(parent, list):
                parent = parent[int(token)]
            path_stack.append(parent)
        
        last_token = tokens[-1]
        
        if isinstance(parent, dict):
            parent[last_token] = copy.deepcopy(value)
        elif isinstance(parent, list):
            if last_token == '-':
                parent.append(copy.deepcopy(value))
            else:
                index = int(last_token)
                if index < 0 or index > len(parent):
                    raise JsonPatchOperationError(f"Array index {index} out of range")
                parent.insert(index, copy.deepcopy(value))
        else:
            raise JsonPatchOperationError(f"Cannot add to non-container")
        
        return document
    
    def _op_remove(self, document: Any, tokens: List[str]) -> Any:
        """Remove the value at the specified path."""
        if not tokens:
            raise JsonPatchOperationError("Cannot remove root")
        
        # Navigate to parent
        parent = document
        
        for token in tokens[:-1]:
            if isinstance(parent, dict):
                parent = parent[token]
            elif isinstance(parent, list):
                parent = parent[int(token)]
        
        last_token = tokens[-1]
        
        if isinstance(parent, dict):
            if last_token not in parent:
                raise JsonPatchOperationError(f"Key '{last_token}' not found")
            del parent[last_token]
        elif isinstance(parent, list):
            index = int(last_token)
            if index < 0 or index >= len(parent):
                raise JsonPatchOperationError(f"Array index {index} out of range")
            del parent[index]
        else:
            raise JsonPatchOperationError(f"Cannot remove from non-container")
        
        return document
    
    def _op_replace(self, document: Any, tokens: List[str], value: Any) -> Any:
        """Replace the value at the specified path."""
        if not tokens:
            return copy.deepcopy(value)
        
        # Navigate to parent
        parent = document
        
        for token in tokens[:-1]:
            if isinstance(parent, dict):
                parent = parent[token]
            elif isinstance(parent, list):
                parent = parent[int(token)]
        
        last_token = tokens[-1]
        
        if isinstance(parent, dict):
            if last_token not in parent:
                raise JsonPatchOperationError(f"Key '{last_token}' not found")
            parent[last_token] = copy.deepcopy(value)
        elif isinstance(parent, list):
            index = int(last_token)
            if index < 0 or index >= len(parent):
                raise JsonPatchOperationError(f"Array index {index} out of range")
            parent[index] = copy.deepcopy(value)
        else:
            raise JsonPatchOperationError(f"Cannot replace in non-container")
        
        return document
    
    def _op_move(self, document: Any, path_tokens: List[str], from_ptr: JsonPointer) -> Any:
        """Move a value from one location to another."""
        from_tokens = from_ptr.tokens()
        
        # Check for moving into descendant
        if len(from_tokens) <= len(path_tokens):
            if path_tokens[:len(from_tokens)] == from_tokens:
                raise JsonPatchOperationError("Cannot move into a descendant of the source")
        
        # Get the value to move
        value = self._get_value(document, from_tokens)
        
        # Remove from source
        document = self._op_remove(document, from_tokens)
        
        # Add to destination (need to recompute path after removal)
        document = self._op_add(document, path_tokens, value)
        
        return document
    
    def _op_copy(self, document: Any, path_tokens: List[str], from_ptr: JsonPointer) -> Any:
        """Copy a value from one location to another."""
        from_tokens = from_ptr.tokens()
        value = self._get_value(document, from_tokens)
        return self._op_add(document, path_tokens, value)
    
    def _op_test(self, document: Any, path: JsonPointer, expected: Any) -> Any:
        """Test that a value equals the expected value."""
        actual = path.get(document)
        
        # Deep comparison
        if not self._deep_equals(actual, expected):
            raise JsonPatchTestError(path.pointer, expected, actual)
        
        return document
    
    def _get_value(self, document: Any, tokens: List[str]) -> Any:
        """Get value at path, returning a deep copy."""
        value = document
        for token in tokens:
            if isinstance(value, dict):
                value = value[token]
            elif isinstance(value, list):
                value = value[int(token)]
        return copy.deepcopy(value)
    
    @staticmethod
    def _deep_equals(a: Any, b: Any) -> bool:
        """Deep equality check for JSON values."""
        if type(a) != type(b):
            # Special case: int and float comparison
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return a == b
            return False
        
        if isinstance(a, dict):
            if set(a.keys()) != set(b.keys()):
                return False
            return all(JsonPatch._deep_equals(a[k], b[k]) for k in a)
        
        if isinstance(a, list):
            if len(a) != len(b):
                return False
            return all(JsonPatch._deep_equals(x, y) for x, y in zip(a, b))
        
        return a == b
    
    def to_json(self) -> str:
        """Convert the patch to JSON string."""
        return json.dumps(self.operations, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'JsonPatch':
        """Create a patch from JSON string."""
        return cls(json_str)
    
    def __repr__(self) -> str:
        return f"JsonPatch({self.operations!r})"
    
    def __len__(self) -> int:
        return len(self.operations)
    
    def __iter__(self):
        return iter(self.operations)


def diff(source: Any, target: Any, path: str = "") -> List[Dict]:
    """
    Generate a JSON Patch to transform source into target.
    
    This creates a minimal set of operations to transform the source
    document into the target document.
    
    Args:
        source: Original JSON document
        target: Target JSON document
        path: Current path (used internally for recursion)
        
    Returns:
        List of JSON Patch operations
    
    Example:
        >>> source = {"foo": "bar", "old": 1}
        >>> target = {"foo": "bar", "new": 2}
        >>> diff(source, target)
        [{'op': 'remove', 'path': '/old'}, {'op': 'add', 'path': '/new', 'value': 2}]
    """
    operations = []
    _diff_recursive(source, target, path or "", operations)
    return operations


def _diff_recursive(source: Any, target: Any, path: str, ops: List[Dict]) -> None:
    """Recursive diff helper."""
    # Both None or same type
    if source is None and target is None:
        return
    
    if source is None:
        ops.append({"op": "add", "path": path or "/", "value": copy.deepcopy(target)})
        return
    
    if target is None:
        if path:
            ops.append({"op": "remove", "path": path})
        return
    
    # Type mismatch - replace
    if type(source) != type(target):
        ops.append({"op": "replace", "path": path or "/", "value": copy.deepcopy(target)})
        return
    
    # Both are dicts
    if isinstance(source, dict):
        all_keys = set(source.keys()) | set(target.keys())
        
        for key in sorted(all_keys):
            escaped_key = JsonPointer.escape(key)
            child_path = f"{path}/{escaped_key}" if path else f"/{escaped_key}"
            
            if key not in source:
                # Added key
                ops.append({"op": "add", "path": child_path, "value": copy.deepcopy(target[key])})
            elif key not in target:
                # Removed key
                ops.append({"op": "remove", "path": child_path})
            else:
                # Both have key, recurse
                _diff_recursive(source[key], target[key], child_path, ops)
    
    # Both are lists
    elif isinstance(source, list):
        # Simple diff: if lengths differ or elements differ, use replace for simplicity
        # A more sophisticated algorithm would use LCS diff
        if len(source) != len(target):
            ops.append({"op": "replace", "path": path or "/", "value": copy.deepcopy(target)})
        else:
            for i, (s, t) in enumerate(zip(source, target)):
                child_path = f"{path}/{i}" if path else f"/{i}"
                _diff_recursive(s, t, child_path, ops)
    
    # Primitive values
    else:
        if source != target:
            ops.append({"op": "replace", "path": path or "/", "value": copy.deepcopy(target)})


def patch_document(document: Any, operations: Union[List[Dict], str], in_place: bool = False) -> Any:
    """
    Convenience function to apply a JSON Patch to a document.
    
    Args:
        document: JSON document to patch
        operations: List of operations or JSON string
        in_place: Whether to modify the original document
        
    Returns:
        Patched document
    """
    p = JsonPatch(operations)
    return p.apply(document, in_place)


def create_patch(source: Any, target: Any) -> JsonPatch:
    """
    Convenience function to create a JSON Patch from source to target.
    
    Args:
        source: Source document
        target: Target document
        
    Returns:
        JsonPatch instance
    """
    return JsonPatch(diff(source, target))


def merge_patches(*patches: Union[JsonPatch, List[Dict], str]) -> JsonPatch:
    """
    Merge multiple patches into a single patch.
    
    Args:
        *patches: JsonPatch instances, operation lists, or JSON strings
        
    Returns:
        Combined JsonPatch
    """
    combined_ops = []
    
    for p in patches:
        if isinstance(p, JsonPatch):
            combined_ops.extend(p.operations)
        elif isinstance(p, str):
            combined_ops.extend(json.loads(p))
        else:
            combined_ops.extend(p)
    
    return JsonPatch(combined_ops)


# Utility functions for common operations

def op_add(path: str, value: Any) -> Dict:
    """Create an add operation."""
    return {"op": "add", "path": path, "value": value}


def op_remove(path: str) -> Dict:
    """Create a remove operation."""
    return {"op": "remove", "path": path}


def op_replace(path: str, value: Any) -> Dict:
    """Create a replace operation."""
    return {"op": "replace", "path": path, "value": value}


def op_move(path: str, from_path: str) -> Dict:
    """Create a move operation."""
    return {"op": "move", "path": path, "from": from_path}


def op_copy(path: str, from_path: str) -> Dict:
    """Create a copy operation."""
    return {"op": "copy", "path": path, "from": from_path}


def op_test(path: str, value: Any) -> Dict:
    """Create a test operation."""
    return {"op": "test", "path": path, "value": value}


__all__ = [
    'JsonPatch',
    'JsonPatchError',
    'JsonPatchTestError',
    'JsonPatchOperationError',
    'JsonPointer',
    'JsonPointerError',
    'diff',
    'patch_document',
    'create_patch',
    'merge_patches',
    'op_add',
    'op_remove',
    'op_replace',
    'op_move',
    'op_copy',
    'op_test',
]