"""
Tests for JSON Patch Utils
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    JsonPatch, JsonPointer, JsonPatchError, JsonPatchTestError,
    JsonPointerError, diff, patch_document, create_patch, merge_patches,
    op_add, op_remove, op_replace, op_move, op_copy, op_test
)


def test_json_pointer_basic():
    """Test basic JSON Pointer functionality."""
    print("Testing JsonPointer basic operations...")
    
    # Root pointer
    ptr = JsonPointer("")
    doc = {"foo": "bar"}
    assert ptr.get(doc) == doc
    
    # Simple path
    ptr = JsonPointer("/foo")
    assert ptr.get(doc) == "bar"
    
    # Nested path
    doc = {"foo": {"bar": {"baz": 42}}}
    ptr = JsonPointer("/foo/bar/baz")
    assert ptr.get(doc) == 42
    
    # Array access
    doc = {"items": [10, 20, 30]}
    ptr = JsonPointer("/items/1")
    assert ptr.get(doc) == 20
    
    print("  ✓ Basic JSON Pointer operations work")


def test_json_pointer_escaping():
    """Test JSON Pointer escaping/unescaping."""
    print("Testing JsonPointer escaping...")
    
    # Slash in key
    doc = {"a/b": "slash"}
    ptr = JsonPointer("/a~1b")
    assert ptr.get(doc) == "slash"
    
    # Tilde in key
    doc = {"a~b": "tilde"}
    ptr = JsonPointer("/a~0b")
    assert ptr.get(doc) == "tilde"
    
    # Combined
    doc = {"a~/b": "both"}
    ptr = JsonPointer("/a~0~1b")
    assert ptr.get(doc) == "both"
    
    # Escape function
    assert JsonPointer.escape("a/b") == "a~1b"
    assert JsonPointer.escape("a~b") == "a~0b"
    assert JsonPointer.escape("a~/b") == "a~0~1b"
    
    # Unescape function
    assert JsonPointer.unescape("a~1b") == "a/b"
    assert JsonPointer.unescape("a~0b") == "a~b"
    
    # from_tokens
    ptr = JsonPointer.from_tokens(["foo", "bar/baz", "~test"])
    assert ptr.pointer == "/foo/bar~1baz/~0test"
    
    print("  ✓ JSON Pointer escaping works")


def test_json_pointer_append():
    """Test JSON Pointer append functionality."""
    print("Testing JsonPointer append...")
    
    ptr = JsonPointer("/foo")
    new_ptr = ptr.append("bar")
    assert new_ptr.pointer == "/foo/bar"
    
    # Append with special chars
    ptr = JsonPointer("/foo")
    new_ptr = ptr.append("a/b")
    assert new_ptr.pointer == "/foo/a~1b"
    
    print("  ✓ JSON Pointer append works")


def test_json_patch_add():
    """Test add operation."""
    print("Testing JSON Patch add operation...")
    
    # Add to object
    doc = {"foo": "bar"}
    patch = JsonPatch([{"op": "add", "path": "/baz", "value": "qux"}])
    result = patch.apply(doc)
    assert result == {"foo": "bar", "baz": "qux"}
    assert doc == {"foo": "bar"}  # Original unchanged
    
    # Add to array at index
    doc = {"items": [1, 2, 3]}
    patch = JsonPatch([{"op": "add", "path": "/items/1", "value": 99}])
    result = patch.apply(doc)
    assert result == {"items": [1, 99, 2, 3]}
    
    # Add to array at end
    doc = {"items": [1, 2, 3]}
    patch = JsonPatch([{"op": "add", "path": "/items/-", "value": 4}])
    result = patch.apply(doc)
    assert result == {"items": [1, 2, 3, 4]}
    
    # Add at root
    doc = {"old": "data"}
    patch = JsonPatch([{"op": "add", "path": "", "value": {"new": "data"}}])
    result = patch.apply(doc)
    assert result == {"new": "data"}
    
    print("  ✓ Add operation works")


def test_json_patch_remove():
    """Test remove operation."""
    print("Testing JSON Patch remove operation...")
    
    # Remove from object
    doc = {"foo": "bar", "baz": "qux"}
    patch = JsonPatch([{"op": "remove", "path": "/baz"}])
    result = patch.apply(doc)
    assert result == {"foo": "bar"}
    
    # Remove from array
    doc = {"items": [1, 2, 3]}
    patch = JsonPatch([{"op": "remove", "path": "/items/1"}])
    result = patch.apply(doc)
    assert result == {"items": [1, 3]}
    
    print("  ✓ Remove operation works")


def test_json_patch_replace():
    """Test replace operation."""
    print("Testing JSON Patch replace operation...")
    
    # Replace in object
    doc = {"foo": "bar"}
    patch = JsonPatch([{"op": "replace", "path": "/foo", "value": "baz"}])
    result = patch.apply(doc)
    assert result == {"foo": "baz"}
    
    # Replace in array
    doc = {"items": [1, 2, 3]}
    patch = JsonPatch([{"op": "replace", "path": "/items/1", "value": 99}])
    result = patch.apply(doc)
    assert result == {"items": [1, 99, 3]}
    
    # Replace at root
    doc = {"old": "data"}
    patch = JsonPatch([{"op": "replace", "path": "", "value": "simple"}])
    result = patch.apply(doc)
    assert result == "simple"
    
    print("  ✓ Replace operation works")


def test_json_patch_move():
    """Test move operation."""
    print("Testing JSON Patch move operation...")
    
    # Move between object keys
    doc = {"foo": "bar"}
    patch = JsonPatch([{"op": "move", "from": "/foo", "path": "/baz"}])
    result = patch.apply(doc)
    assert result == {"baz": "bar"}
    
    # Move array element
    doc = {"items": [1, 2, 3]}
    patch = JsonPatch([{"op": "move", "from": "/items/0", "path": "/items/2"}])
    result = patch.apply(doc)
    assert result == {"items": [2, 3, 1]}
    
    print("  ✓ Move operation works")


def test_json_patch_copy():
    """Test copy operation."""
    print("Testing JSON Patch copy operation...")
    
    # Copy between keys
    doc = {"foo": {"bar": "baz"}}
    patch = JsonPatch([{"op": "copy", "from": "/foo", "path": "/qux"}])
    result = patch.apply(doc)
    assert result["qux"] == {"bar": "baz"}
    assert result["foo"] == {"bar": "baz"}  # Original intact
    
    print("  ✓ Copy operation works")


def test_json_patch_test():
    """Test test operation."""
    print("Testing JSON Patch test operation...")
    
    # Successful test
    doc = {"foo": "bar"}
    patch = JsonPatch([{"op": "test", "path": "/foo", "value": "bar"}])
    result = patch.apply(doc)
    assert result == {"foo": "bar"}
    
    # Failed test
    doc = {"foo": "bar"}
    patch = JsonPatch([{"op": "test", "path": "/foo", "value": "wrong"}])
    try:
        patch.apply(doc)
        assert False, "Should have raised JsonPatchTestError"
    except JsonPatchTestError as e:
        assert e.path == "/foo"
        assert e.expected == "wrong"
        assert e.actual == "bar"
    
    # Deep equality test
    doc = {"nested": {"a": [1, 2, 3]}}
    patch = JsonPatch([{"op": "test", "path": "/nested", "value": {"a": [1, 2, 3]}}])
    result = patch.apply(doc)
    assert result == {"nested": {"a": [1, 2, 3]}}
    
    print("  ✓ Test operation works")


def test_json_patch_multiple_operations():
    """Test multiple operations in sequence."""
    print("Testing multiple operations...")
    
    doc = {"foo": "bar"}
    patch = JsonPatch([
        {"op": "add", "path": "/baz", "value": "qux"},
        {"op": "remove", "path": "/foo"},
        {"op": "add", "path": "/new", "value": "value"}
    ])
    result = patch.apply(doc)
    assert result == {"baz": "qux", "new": "value"}
    
    print("  ✓ Multiple operations work")


def test_json_patch_in_place():
    """Test in-place modification."""
    print("Testing in-place modification...")
    
    doc = {"foo": "bar"}
    patch = JsonPatch([{"op": "add", "path": "/baz", "value": "qux"}])
    result = patch.apply(doc, in_place=True)
    assert result == {"foo": "bar", "baz": "qux"}
    assert doc == {"foo": "bar", "baz": "qux"}  # Original modified
    
    print("  ✓ In-place modification works")


def test_diff():
    """Test diff generation."""
    print("Testing diff generation...")
    
    # Add key
    source = {"foo": "bar"}
    target = {"foo": "bar", "baz": "qux"}
    ops = diff(source, target)
    assert len(ops) == 1
    assert ops[0]["op"] == "add"
    assert ops[0]["path"] == "/baz"
    
    # Remove key
    source = {"foo": "bar", "old": "value"}
    target = {"foo": "bar"}
    ops = diff(source, target)
    assert len(ops) == 1
    assert ops[0]["op"] == "remove"
    
    # Replace value
    source = {"foo": "bar"}
    target = {"foo": "baz"}
    ops = diff(source, target)
    assert len(ops) == 1
    assert ops[0]["op"] == "replace"
    
    # Complex diff
    source = {"a": 1, "b": 2, "c": [1, 2, 3]}
    target = {"a": 1, "b": 99, "d": 4, "c": [1, 2, 3, 4]}
    ops = diff(source, target)
    result = JsonPatch(ops).apply(source)
    assert result == target
    
    print("  ✓ Diff generation works")


def test_create_patch():
    """Test create_patch convenience function."""
    print("Testing create_patch...")
    
    source = {"foo": "bar"}
    target = {"foo": "baz", "new": "value"}
    
    patch = create_patch(source, target)
    result = patch.apply(source)
    assert result == target
    
    print("  ✓ create_patch works")


def test_patch_document():
    """Test patch_document convenience function."""
    print("Testing patch_document...")
    
    doc = {"foo": "bar"}
    ops = [{"op": "add", "path": "/baz", "value": "qux"}]
    
    result = patch_document(doc, ops)
    assert result == {"foo": "bar", "baz": "qux"}
    
    # With JSON string
    result = patch_document(doc, '[{"op": "add", "path": "/new", "value": 42}]')
    assert result == {"foo": "bar", "new": 42}
    
    print("  ✓ patch_document works")


def test_merge_patches():
    """Test merge_patches function."""
    print("Testing merge_patches...")
    
    p1 = JsonPatch([{"op": "add", "path": "/a", "value": 1}])
    p2 = [{"op": "add", "path": "/b", "value": 2}]
    p3 = '[{"op": "add", "path": "/c", "value": 3}]'
    
    merged = merge_patches(p1, p2, p3)
    assert len(merged) == 3
    
    doc = {}
    result = merged.apply(doc)
    assert result == {"a": 1, "b": 2, "c": 3}
    
    print("  ✓ merge_patches works")


def test_op_helpers():
    """Test operation helper functions."""
    print("Testing operation helpers...")
    
    # op_add
    op = op_add("/foo", "bar")
    assert op == {"op": "add", "path": "/foo", "value": "bar"}
    
    # op_remove
    op = op_remove("/foo")
    assert op == {"op": "remove", "path": "/foo"}
    
    # op_replace
    op = op_replace("/foo", "new")
    assert op == {"op": "replace", "path": "/foo", "value": "new"}
    
    # op_move
    op = op_move("/dest", "/src")
    assert op == {"op": "move", "path": "/dest", "from": "/src"}
    
    # op_copy
    op = op_copy("/dest", "/src")
    assert op == {"op": "copy", "path": "/dest", "from": "/src"}
    
    # op_test
    op = op_test("/foo", "expected")
    assert op == {"op": "test", "path": "/foo", "value": "expected"}
    
    print("  ✓ Operation helpers work")


def test_json_serialization():
    """Test JSON serialization."""
    print("Testing JSON serialization...")
    
    patch = JsonPatch([
        {"op": "add", "path": "/foo", "value": "bar"},
        {"op": "remove", "path": "/old"}
    ])
    
    json_str = patch.to_json()
    assert '"op": "add"' in json_str
    
    # Round trip
    new_patch = JsonPatch.from_json(json_str)
    assert len(new_patch) == 2
    
    print("  ✓ JSON serialization works")


def test_error_handling():
    """Test error handling."""
    print("Testing error handling...")
    
    # Invalid pointer
    try:
        JsonPointer("invalid")
        assert False, "Should raise JsonPointerError"
    except JsonPointerError:
        pass
    
    # Missing key in pointer
    doc = {"foo": "bar"}
    ptr = JsonPointer("/missing")
    try:
        ptr.get(doc)
        assert False, "Should raise JsonPointerError"
    except JsonPointerError:
        pass
    
    # Out of range array index
    doc = {"items": [1, 2, 3]}
    ptr = JsonPointer("/items/10")
    try:
        ptr.get(doc)
        assert False, "Should raise JsonPointerError"
    except JsonPointerError:
        pass
    
    # Invalid operation type
    try:
        JsonPatch([{"op": "invalid"}])
        assert False, "Should raise JsonPatchError"
    except JsonPatchError:
        pass
    
    # Missing required field
    try:
        JsonPatch([{"op": "add", "path": "/foo"}])  # Missing value
        assert False, "Should raise JsonPatchError"
    except JsonPatchError:
        pass
    
    print("  ✓ Error handling works")


def test_rfc_examples():
    """Test examples from RFC 6902."""
    print("Testing RFC 6902 examples...")
    
    # Example 1: Add
    doc = {"foo": "bar"}
    patch = JsonPatch([{"op": "add", "path": "/baz", "value": "qux"}])
    assert patch.apply(doc) == {"foo": "bar", "baz": "qux"}
    
    # Example 2: Remove
    doc = {"foo": "bar", "baz": "qux"}
    patch = JsonPatch([{"op": "remove", "path": "/baz"}])
    assert patch.apply(doc) == {"foo": "bar"}
    
    # Example 3: Replace
    doc = {"foo": "bar", "baz": "qux"}
    patch = JsonPatch([{"op": "replace", "path": "/baz", "value": "boo"}])
    assert patch.apply(doc) == {"foo": "bar", "baz": "boo"}
    
    # Example 4: Move
    doc = {"foo": {"bar": "baz", "waldo": "fred"}, "qux": {"corge": "grault"}}
    patch = JsonPatch([{"op": "move", "from": "/foo/waldo", "path": "/qux/thud"}])
    result = patch.apply(doc)
    assert "waldo" not in result["foo"]
    assert result["qux"]["thud"] == "fred"
    
    # Example 5: Copy
    doc = {"foo": {"bar": "baz"}}
    patch = JsonPatch([{"op": "copy", "from": "/foo/bar", "path": "/foo/qux"}])
    assert patch.apply(doc) == {"foo": {"bar": "baz", "qux": "baz"}}
    
    # Example 6: Test
    doc = {"foo": {"bar": "baz"}}
    patch = JsonPatch([{"op": "test", "path": "/foo/bar", "value": "baz"}])
    result = patch.apply(doc)  # Should not raise
    
    print("  ✓ RFC 6902 examples pass")


def run_all_tests():
    """Run all tests."""
    print("\n=== JSON Patch Utils Tests ===\n")
    
    test_json_pointer_basic()
    test_json_pointer_escaping()
    test_json_pointer_append()
    test_json_patch_add()
    test_json_patch_remove()
    test_json_patch_replace()
    test_json_patch_move()
    test_json_patch_copy()
    test_json_patch_test()
    test_json_patch_multiple_operations()
    test_json_patch_in_place()
    test_diff()
    test_create_patch()
    test_patch_document()
    test_merge_patches()
    test_op_helpers()
    test_json_serialization()
    test_error_handling()
    test_rfc_examples()
    
    print("\n=== All tests passed! ===\n")


if __name__ == "__main__":
    run_all_tests()