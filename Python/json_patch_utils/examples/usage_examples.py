"""
JSON Patch Utils - Usage Examples

This file demonstrates the key features of json_patch_utils:
1. JSON Pointer - RFC 6901 (pointing to locations in JSON)
2. JSON Patch - RFC 6902 (applying changes to JSON)
3. Diff generation (creating patches from document differences)
4. Utility functions for building patches
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from json_patch_utils.mod import (
    JsonPatch, JsonPointer,
    diff, patch_document, create_patch, merge_patches,
    op_add, op_remove, op_replace, op_move, op_copy, op_test
)
import json


def example_json_pointer():
    """Example 1: JSON Pointer - RFC 6901"""
    print("=" * 60)
    print("Example 1: JSON Pointer (RFC 6901)")
    print("=" * 60)
    
    # Sample document
    document = {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ],
        "config": {
            "theme": "dark",
            "notifications": {
                "email": True,
                "push": False
            }
        }
    }
    
    print("\nDocument:")
    print(json.dumps(document, indent=2))
    
    # Navigate using JSON Pointer
    print("\n--- JSON Pointer Navigation ---")
    
    # Get first user's name
    ptr = JsonPointer("/users/0/name")
    print(f"\nPointer: {ptr.pointer}")
    print(f"Value: {ptr.get(document)}")
    
    # Get nested config value
    ptr = JsonPointer("/config/notifications/email")
    print(f"\nPointer: {ptr.pointer}")
    print(f"Value: {ptr.get(document)}")
    
    # Build pointer from tokens
    ptr = JsonPointer.from_tokens(["users", "1", "email"])
    print(f"\nBuilt from tokens: {ptr.pointer}")
    print(f"Value: {ptr.get(document)}")
    
    # Handle special characters in keys
    document_with_special = {
        "api/v1": "version 1",
        "data~backup": "backup data"
    }
    
    # Escape special characters
    ptr = JsonPointer("/api~1v1")  # ~1 escapes /
    print(f"\nPointer with escaped /: {ptr.pointer}")
    print(f"Value: {ptr.get(document_with_special)}")
    
    ptr = JsonPointer("/data~0backup")  # ~0 escapes ~
    print(f"\nPointer with escaped ~: {ptr.pointer}")
    print(f"Value: {ptr.get(document_with_special)}")


def example_basic_patch_operations():
    """Example 2: Basic JSON Patch Operations"""
    print("\n" + "=" * 60)
    print("Example 2: Basic JSON Patch Operations")
    print("=" * 60)
    
    # ADD operation
    print("\n--- ADD Operation ---")
    doc = {"name": "Alice"}
    print(f"Before: {doc}")
    
    patch = JsonPatch([
        {"op": "add", "path": "/age", "value": 30},
        {"op": "add", "path": "/hobbies", "value": ["reading", "coding"]}
    ])
    result = patch.apply(doc)
    print(f"After: {result}")
    
    # REMOVE operation
    print("\n--- REMOVE Operation ---")
    doc = {"name": "Alice", "temp": "delete me"}
    print(f"Before: {doc}")
    
    patch = JsonPatch([{"op": "remove", "path": "/temp"}])
    result = patch.apply(doc)
    print(f"After: {result}")
    
    # REPLACE operation
    print("\n--- REPLACE Operation ---")
    doc = {"name": "Alice", "age": 30}
    print(f"Before: {doc}")
    
    patch = JsonPatch([{"op": "replace", "path": "/age", "value": 31}])
    result = patch.apply(doc)
    print(f"After: {result}")
    
    # Array operations
    print("\n--- Array Operations ---")
    doc = {"items": [1, 2, 3]}
    print(f"Before: {doc}")
    
    patch = JsonPatch([
        {"op": "add", "path": "/items/0", "value": 0},      # Insert at index 0
        {"op": "add", "path": "/items/-", "value": 4},      # Append to end
        {"op": "remove", "path": "/items/2"},               # Remove at index
    ])
    result = patch.apply(doc)
    print(f"After: {result}")


def example_move_copy_operations():
    """Example 3: Move and Copy Operations"""
    print("\n" + "=" * 60)
    print("Example 3: Move and Copy Operations")
    print("=" * 60)
    
    # MOVE operation
    print("\n--- MOVE Operation ---")
    doc = {
        "old_location": {"data": "important"},
        "new_location": {}
    }
    print(f"Before: {json.dumps(doc, indent=2)}")
    
    patch = JsonPatch([
        {"op": "move", "from": "/old_location/data", "path": "/new_location/data"},
        {"op": "remove", "path": "/old_location"}
    ])
    result = patch.apply(doc)
    print(f"After: {json.dumps(result, indent=2)}")
    
    # COPY operation
    print("\n--- COPY Operation ---")
    doc = {
        "template": {"name": "John", "role": "user"},
        "users": []
    }
    print(f"Before: {json.dumps(doc, indent=2)}")
    
    patch = JsonPatch([
        {"op": "copy", "from": "/template", "path": "/users/-"}
    ])
    result = patch.apply(doc)
    print(f"After: {json.dumps(result, indent=2)}")


def example_test_operation():
    """Example 4: Test Operation for Validation"""
    print("\n" + "=" * 60)
    print("Example 4: Test Operation for Validation")
    print("=" * 60)
    
    doc = {
        "user": {
            "id": 123,
            "role": "admin"
        }
    }
    
    print(f"Document: {json.dumps(doc, indent=2)}")
    
    # Test before making changes
    patch = JsonPatch([
        {"op": "test", "path": "/user/role", "value": "admin"},
        {"op": "replace", "path": "/user/role", "value": "superadmin"}
    ])
    
    print("\nPatch with test (should succeed):")
    result = patch.apply(doc)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Test that fails
    print("\n--- Test Failure Example ---")
    doc = {"status": "pending"}
    patch = JsonPatch([
        {"op": "test", "path": "/status", "value": "approved"},
        {"op": "add", "path": "/approved_at", "value": "2024-01-01"}
    ])
    
    try:
        patch.apply(doc)
    except Exception as e:
        print(f"Test failed as expected: {e}")


def example_diff_generation():
    """Example 5: Generating Patches from Document Differences"""
    print("\n" + "=" * 60)
    print("Example 5: Diff Generation")
    print("=" * 60)
    
    source = {
        "name": "Alice",
        "age": 30,
        "hobbies": ["reading", "coding"],
        "address": {
            "city": "New York",
            "zip": "10001"
        }
    }
    
    target = {
        "name": "Alice",
        "age": 31,  # Changed
        "hobbies": ["reading", "coding", "gaming"],  # Changed
        "address": {
            "city": "Boston",  # Changed
            "zip": "02101"     # Changed
        },
        "email": "alice@example.com"  # Added
    }
    
    print("Source:")
    print(json.dumps(source, indent=2))
    print("\nTarget:")
    print(json.dumps(target, indent=2))
    
    # Generate patch
    operations = diff(source, target)
    print(f"\nGenerated Patch ({len(operations)} operations):")
    for i, op in enumerate(operations, 1):
        print(f"  {i}. {op['op']}: {op.get('path', op.get('from', 'N/A'))}")
    
    # Apply patch
    patch = JsonPatch(operations)
    result = patch.apply(source)
    print(f"\nPatch application successful: {result == target}")


def example_api_versioning():
    """Example 6: API Version Migration"""
    print("\n" + "=" * 60)
    print("Example 6: API Version Migration")
    print("=" * 60)
    
    # Version 1 of user data
    v1_user = {
        "name": "John Doe",
        "email": "john@example.com",
        "active": True
    }
    
    # Migration to Version 2
    # Changes: 
    # - 'name' split into 'first_name' and 'last_name'
    # - 'active' renamed to 'status'
    # - 'created_at' timestamp added
    
    def migrate_v1_to_v2(user):
        name_parts = user["name"].split(" ", 1)
        
        patch = JsonPatch([
            {"op": "add", "path": "/first_name", "value": name_parts[0]},
            {"op": "add", "path": "/last_name", "value": name_parts[1] if len(name_parts) > 1 else ""},
            {"op": "remove", "path": "/name"},
            {"op": "add", "path": "/status", "value": "active" if user["active"] else "inactive"},
            {"op": "remove", "path": "/active"},
            {"op": "add", "path": "/created_at", "value": "2024-01-15T10:30:00Z"}
        ])
        
        return patch.apply(user)
    
    print("V1 User:")
    print(json.dumps(v1_user, indent=2))
    
    v2_user = migrate_v1_to_v2(v1_user)
    print("\nV2 User:")
    print(json.dumps(v2_user, indent=2))


def example_conditional_updates():
    """Example 7: Conditional Updates with Test"""
    print("\n" + "=" * 60)
    print("Example 7: Conditional Updates")
    print("=" * 60)
    
    inventory = {
        "products": [
            {"id": 1, "name": "Widget", "stock": 10, "price": 9.99},
            {"id": 2, "name": "Gadget", "stock": 5, "price": 19.99}
        ]
    }
    
    print("Current Inventory:")
    print(json.dumps(inventory, indent=2))
    
    # Only update if stock is sufficient
    def purchase_product(inventory, product_id, quantity):
        """Try to purchase a product, only if enough stock exists."""
        product_idx = next(
            (i for i, p in enumerate(inventory["products"]) if p["id"] == product_id),
            None
        )
        if product_idx is None:
            raise ValueError("Product not found")
        
        path = f"/products/{product_idx}/stock"
        current_stock = inventory["products"][product_idx]["stock"]
        new_stock = current_stock - quantity
        
        patch = JsonPatch([
            {"op": "test", "path": path, "value": current_stock},
            {"op": "replace", "path": path, "value": new_stock}
        ])
        
        return patch.apply(inventory)
    
    # Successful purchase
    print("\n--- Successful Purchase (3 Widgets) ---")
    result = purchase_product(inventory, 1, 3)
    print(json.dumps(result, indent=2))
    
    # Failed purchase (not enough stock)
    print("\n--- Failed Purchase (10 Gadgets, only 5 in stock) ---")
    try:
        result = purchase_product(result, 2, 10)
    except Exception as e:
        print(f"Purchase failed: {e}")


def example_builder_pattern():
    """Example 8: Building Patches with Helper Functions"""
    print("\n" + "=" * 60)
    print("Example 8: Building Patches with Helpers")
    print("=" * 60)
    
    # Build patch step by step
    operations = [
        op_add("/version", 2),
        op_add("/features/-", "new_feature"),
        op_replace("/status", "updated"),
        op_remove("/deprecated_field"),
        op_test("/checksum", "abc123"),
    ]
    
    print("Operations built with helpers:")
    for op in operations:
        print(f"  {op}")
    
    doc = {
        "version": 1,
        "status": "old",
        "deprecated_field": "remove me",
        "features": ["feature1"],
        "checksum": "abc123"
    }
    
    print("\nBefore:")
    print(json.dumps(doc, indent=2))
    
    patch = JsonPatch(operations)
    result = patch.apply(doc)
    
    print("\nAfter:")
    print(json.dumps(result, indent=2))


def example_merge_patches():
    """Example 9: Merging Multiple Patches"""
    print("\n" + "=" * 60)
    print("Example 9: Merging Multiple Patches")
    print("=" * 60)
    
    # Create multiple patches
    schema_patch = JsonPatch([
        {"op": "add", "path": "/$schema", "value": "https://example.com/schema/v2"}
    ])
    
    data_patch = JsonPatch([
        {"op": "add", "path": "/data/new_field", "value": "new_value"},
        {"op": "replace", "path": "/data/updated_field", "value": "updated"}
    ])
    
    cleanup_patch = JsonPatch([
        {"op": "remove", "path": "/deprecated"}
    ])
    
    # Merge all patches
    combined = merge_patches(schema_patch, data_patch, cleanup_patch)
    print(f"Combined patch has {len(combined)} operations")
    
    doc = {
        "data": {
            "updated_field": "old"
        },
        "deprecated": "old field"
    }
    
    result = combined.apply(doc)
    print("\nResult:")
    print(json.dumps(result, indent=2))


def example_document_comparison():
    """Example 10: Document Comparison Tool"""
    print("\n" + "=" * 60)
    print("Example 10: Document Comparison Tool")
    print("=" * 60)
    
    def compare_documents(doc1, doc2, name1="Document 1", name2="Document 2"):
        """Compare two documents and show changes."""
        operations = diff(doc1, doc2)
        
        if not operations:
            print("Documents are identical!")
            return
        
        print(f"Changes from {name1} to {name2}:")
        print("-" * 40)
        
        for op in operations:
            if op["op"] == "add":
                print(f"  + {op['path']}: {op['value']}")
            elif op["op"] == "remove":
                print(f"  - {op['path']}")
            elif op["op"] == "replace":
                print(f"  ~ {op['path']}: new value = {op['value']}")
    
    config_v1 = {
        "app_name": "MyApp",
        "version": "1.0",
        "debug": False,
        "database": {
            "host": "localhost",
            "port": 5432
        }
    }
    
    config_v2 = {
        "app_name": "MyApp",
        "version": "2.0",
        "debug": True,
        "database": {
            "host": "db.example.com",
            "port": 5432,
            "ssl": True
        },
        "cache": {
            "enabled": True
        }
    }
    
    print("Config V1:")
    print(json.dumps(config_v1, indent=2))
    print("\nConfig V2:")
    print(json.dumps(config_v2, indent=2))
    print()
    
    compare_documents(config_v1, config_v2, "Config V1", "Config V2")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("JSON PATCH UTILS - USAGE EXAMPLES")
    print("=" * 60)
    
    example_json_pointer()
    example_basic_patch_operations()
    example_move_copy_operations()
    example_test_operation()
    example_diff_generation()
    example_api_versioning()
    example_conditional_updates()
    example_builder_pattern()
    example_merge_patches()
    example_document_comparison()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()