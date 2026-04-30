# Pagination Utilities - 分页工具

提供完整的分页实现，支持多种分页策略，适用于 Web 应用、API 设计和数据展示场景。

## 功能特性

- ✅ **偏移量分页 (Offset Pagination)** - 传统分页，支持页码跳转
- ✅ **游标分页 (Cursor Pagination)** - API 友好，适合大数据集
- ✅ **键集分页 (Keyset Pagination)** - 最高效的数据库分页
- ✅ **无限滚动分页 (Infinite Scroll)** - 社交媒体风格
- ✅ 分页元数据生成
- ✅ 分页链接生成 (REST API Link Header)
- ✅ 页码范围计算 (UI 显示优化)
- ✅ 预加载阈值检测

## 零外部依赖

纯 Python 实现，无需安装任何第三方包。

## 快速开始

### 基础用法

```python
from pagination_utils import Pagination, paginate_offset

# 准备数据
items = [{'id': i, 'name': f'Item-{i}'} for i in range(100)]

# 偏移量分页
result = paginate_offset(items, page=3, per_page=20)

print(f"当前页: {result.metadata.current_page}")
print(f"数据: {result.items}")
print(f"总页数: {result.metadata.total_pages}")
```

### 偏移量分页 (Offset)

适用于小数据集、后台管理系统。

```python
from pagination_utils import OffsetPaginator

paginator = OffsetPaginator(items_per_page=20)
result = paginator.paginate(items, page=5)

# 获取 SQL 参数
offset, limit = paginator.get_offset_limit(page=5)
# SQL: SELECT * FROM table LIMIT 20 OFFSET 80
```

### 游标分页 (Cursor)

适用于 API、大数据集。

```python
from pagination_utils import CursorPaginator

paginator = CursorPaginator(limit=20)

# 第一页
result = paginator.paginate(items)
cursor = result.metadata.next_cursor

# 下一页
result = paginator.paginate(items, cursor=cursor)
```

### 键集分页 (Keyset)

适用于百万级数据的高效分页。

```python
from pagination_utils import KeysetPaginator

# 数据应已按 key_field 排序
paginator = KeysetPaginator(limit=20, key_field='id')
result = paginator.paginate(sorted_items)

# 下一页
result = paginator.paginate(sorted_items, cursor=result.metadata.next_cursor)
```

### 无限滚动分页

适用于移动端、社交媒体。

```python
from pagination_utils import InfiniteScrollPaginator

paginator = InfiniteScrollPaginator(batch_size=20, preload_threshold=5)

result = paginator.paginate(items, loaded_count=0)

# 检查加载状态
state = paginator.get_load_state(total_items=1000, loaded_count=200)
print(f"进度: {state['progress']}%")
print(f"需要预加载: {state['should_preload']}")
```

## 高级功能

### API 响应构建

```python
# 构建 JSON 响应
response = result.to_dict()
# {
#   'items': [...],
#   'pagination': {
#     'current_page': 3,
#     'total_pages': 10,
#     ...
#   },
#   'type': 'offset'
# }

# 生成 REST API Link Header
header = Pagination.generate_header_links('/api/items', 3, 10)
# Link: <api/items?page=1>; rel="first", <api/items?page=10>; rel="last", ...
```

### 页码范围计算 (UI)

```python
# 计算要显示的页码
pages = Pagination.calculate_page_range(
    current_page=5, 
    total_pages=20, 
    max_display=7
)
# [2, 3, 4, 5, 6, 7, 8] - 当前页居中
```

### 分页链接生成

```python
links = Pagination.generate_links('/api/products', 5, 10)
# {
#   'first': '/api/products?page=1',
#   'last': '/api/products?page=10',
#   'prev': '/api/products?page=4',
#   'next': '/api/products?page=6',
#   'self': '/api/products?page=5'
# }
```

## 分页方式对比

| 类型 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| 偏移量 | 小数据集、后台 | 简单、可跳转 | 大数据性能差 |
| 游标 | API、大数据 | 性能稳定 | 无法跳转任意页 |
| 键集 | 百万级数据 | 最高效 | 只能单向翻页 |
| 无限滚动 | 移动端 | 体验好 | 无法定位 |

## API 参考

### OffsetPaginator

- `paginate(items, page, per_page)` - 分页
- `get_offset_limit(page)` - 获取 SQL 参数
- `calculate_pages(total_items)` - 计算总页数

### CursorPaginator

- `paginate(items, cursor, limit)` - 分页
- `encode_cursor(index)` - 编码游标
- `decode_cursor(cursor)` - 解码游标
- `get_first_page(items)` - 获取第一页

### KeysetPaginator

- `paginate(items, cursor, limit, descending)` - 分页
- `encode_cursor(key)` - 编码游标
- `decode_cursor(cursor)` - 解码游标

### InfiniteScrollPaginator

- `paginate(items, loaded_count, batch_size)` - 分页
- `get_load_state(total_items, loaded_count)` - 获取状态

### Pagination (静态方法)

- `offset(items, page, per_page)` - 偏移量分页
- `cursor(items, cursor, limit)` - 游标分页
- `keyset(items, cursor, limit, key_field)` - 键集分页
- `infinite(items, loaded_count, batch_size)` - 无限滚动
- `calculate_page_range(current, total, max_display)` - 页码范围
- `generate_links(base_url, current, total)` - 生成链接
- `generate_header_links(base_url, current, total)` - Link Header

## 文件结构

```
pagination_utils/
├── mod.py              # 核心实现
├── pagination_utils_test.py  # 单元测试
├── README.md           # 说明文档
└── examples/
    └── usage_examples.py  # 使用示例
```

## 运行测试

```bash
python pagination_utils_test.py
```

## 运行示例

```bash
python examples/usage_examples.py
```

## 作者

AllToolkit 自动化开发助手

## 日期

2026-04-30