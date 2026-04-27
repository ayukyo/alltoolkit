# Paginator Utils


AllToolkit - Python Paginator Utilities

A zero-dependency, production-ready pagination utility module.
Supports offset pagination, cursor pagination, and infinite scroll helpers.
Works with any iterable and provides rich metadata.

Author: AllToolkit
License: MIT


## 功能

### 类

- **PageMetadata**: Pagination metadata for a page
  方法: to_dict
- **PageResult**: Result of a paginated query
  方法: to_dict
- **CursorMetadata**: Cursor pagination metadata
  方法: to_dict
- **CursorResult**: Result of a cursor-based paginated query
  方法: to_dict
- **Paginator**: Offset-based paginator for any iterable
  方法: total, total_pages, per_page, page, first ... (6 个方法)
- **CursorPaginator**: Cursor-based paginator for efficient pagination
  方法: per_page, first, after, before
- **InfinitePaginator**: Paginator for infinite/unknown-length iterables
  方法: per_page, exhausted, batch_count, total_yielded, next_batch
- **Chunker**: Split iterables into chunks of a specific size
  方法: chunk_size, to_list
- **PaginatedResponse**: Helper for building paginated API responses
  方法: total_pages, has_next, has_previous, to_dict, to_json

### 函数

- **paginate(items, page, per_page**, ...) - Convenience function for one-off pagination.
- **chunk(items, chunk_size**) - Convenience function for chunking an iterable.
- **slice_iterable(items, start, length**) - Slice an iterable with start and length.
- **calculate_offset(page, per_page**) - Calculate offset for database queries.
- **calculate_total_pages(total, per_page**) - Calculate total number of pages.
- **validate_page(page, total_pages**) - Validate and clamp page number to valid range.
- **page_range(current_page, total_pages, window**) - Calculate page range with ellipsis support.
- **ellipsis_pages(current_page, total_pages, window**) - Generate page list with ellipsis markers.
- **to_dict(self**) - Convert to dictionary.
- **to_dict(self, item_serializer**) - Convert to dictionary with optional item serialization.

... 共 35 个函数

## 使用示例

```python
from mod import paginate

# 使用 paginate
result = paginate()
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
