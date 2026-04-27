# Json Patch Utils


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


## 功能

### 类

- **JsonPatchError**: Base exception for JSON Patch errors
- **JsonPointerError**: Exception for JSON Pointer errors
- **JsonPatchTestError**: Exception raised when a test operation fails
- **JsonPatchOperationError**: Exception for operation-specific errors
- **JsonPointer**: RFC 6901 JSON Pointer implementation
  方法: unescape, escape, tokens, get, get_parent_and_key ... (7 个方法)
- **JsonPatch**: RFC 6902 JSON Patch implementation
  方法: apply, to_json, from_json

### 函数

- **diff(source, target, path**) - Generate a JSON Patch to transform source into target.
- **patch_document(document, operations, in_place**) - Convenience function to apply a JSON Patch to a document.
- **create_patch(source, target**) - Convenience function to create a JSON Patch from source to target.
- **merge_patches(**) - Merge multiple patches into a single patch.
- **op_add(path, value**) - Create an add operation.
- **op_remove(path**) - Create a remove operation.
- **op_replace(path, value**) - Create a replace operation.
- **op_move(path, from_path**) - Create a move operation.
- **op_copy(path, from_path**) - Create a copy operation.
- **op_test(path, value**) - Create a test operation.

... 共 20 个函数

## 使用示例

```python
from mod import diff

# 使用 diff
result = diff()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
