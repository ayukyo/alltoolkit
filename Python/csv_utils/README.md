# CSV Utils - CSV 文件处理工具 📊

**零依赖 CSV 处理库 - 读取、写入、过滤、排序、转换、统计**

---

## 📦 功能概览

| 功能类别 | 函数 | 描述 |
|---------|------|------|
| **读取** | `read_csv`, `read_csv_rows` | 读取 CSV 文件 |
| | `parse_csv_string` | 解析 CSV 字符串 |
| | `read_csv_stream` | 流式读取（大文件） |
| **写入** | `write_csv`, `write_csv_rows` | 写入 CSV 文件 |
| | `to_csv_string` | 转换为 CSV 字符串 |
| **过滤** | `filter_rows`, `filter_by_value` | 条件过滤 |
| | `filter_by_contains` | 子字符串匹配 |
| **排序** | `sort_rows` | 按列排序 |
| **列操作** | `select_columns`, `add_column` | 选择/添加列 |
| | `transform_column`, `remove_column` | 转换/删除列 |
| | `rename_column`, `get_column` | 重命名/获取列 |
| **统计** | `count_rows`, `count_by_value` | 计数统计 |
| | `get_numeric_stats` | 数值统计 |
| **转换** | `to_dict_by_key`, `group_by` | 数据结构转换 |
| | `join_tables`, `merge_rows` | 表连接/合并 |
| **文件** | `merge_csv_files`, `split_csv_file` | 合并/分割文件 |
| | `csv_to_json`, `json_to_csv` | 格式转换 |
| **流式** | `process_csv_stream` | 流式处理 |

---

## 🚀 快速开始

### 安装

无需安装！直接复制 `mod.py` 到你的项目：

```bash
cp AllToolkit/Python/csv_utils/mod.py your_project/
```

### 基础使用

```python
from mod import read_csv, write_csv, filter_by_value, sort_rows

# 读取 CSV 文件
data = read_csv('employees.csv')
# [{'name': 'Alice', 'age': '25', 'dept': 'HR'}, ...]

# 过滤数据
hr_employees = filter_by_value(data, 'dept', 'HR')

# 排序
sorted_data = sort_rows(data, 'age', reverse=True)

# 写入 CSV 文件
write_csv('output.csv', sorted_data)
```

---

## 📖 详细文档

### 读取函数

#### `read_csv(filepath, encoding='utf-8')`

读取 CSV 文件为字典列表。

```python
data = read_csv('data.csv')
print(data[0])  # {'name': 'Alice', 'age': '25'}
```

#### `read_csv_rows(filepath, encoding='utf-8')`

读取 CSV 文件为二维列表（包含表头）。

```python
rows = read_csv_rows('data.csv')
print(rows[0])  # ['name', 'age', 'city']
print(rows[1])  # ['Alice', '25', 'NYC']
```

#### `parse_csv_string(csv_string, delimiter=',')`

解析 CSV 格式的字符串。

```python
csv_str = "name,age\nAlice,25\nBob,30"
data = parse_csv_string(csv_str)
# [{'name': 'Alice', 'age': '25'}, {'name': 'Bob', 'age': '30'}]
```

#### `read_csv_stream(filepath, encoding='utf-8')`

流式读取大文件，返回生成器。

```python
for row in read_csv_stream('large_file.csv'):
    process(row)  # 逐行处理，节省内存
```

---

### 写入函数

#### `write_csv(filepath, data, encoding='utf-8')`

将字典列表写入 CSV 文件。

```python
data = [
    {'name': 'Alice', 'age': '25'},
    {'name': 'Bob', 'age': '30'}
]
write_csv('output.csv', data)
```

#### `write_csv_rows(filepath, data, header=None, encoding='utf-8')`

将二维列表写入 CSV 文件。

```python
data = [['Alice', 25], ['Bob', 30]]
write_csv_rows('output.csv', data, header=['name', 'age'])
```

#### `to_csv_string(data, delimiter=',')`

将字典列表转换为 CSV 字符串。

```python
csv_str = to_csv_string(data)
print(csv_str)
# name,age
# Alice,25
# Bob,30
```

---

### 过滤函数

#### `filter_rows(data, condition)`

使用自定义条件过滤。

```python
# 过滤年龄大于 30 的行
adults = filter_rows(data, lambda x: int(x['age']) > 30)
```

#### `filter_by_value(data, column, value)`

精确匹配列值。

```python
hr_staff = filter_by_value(data, 'dept', 'HR')
```

#### `filter_by_contains(data, column, substring)`

子字符串匹配。

```python
# 名字包含 "li" 的人
matches = filter_by_contains(data, 'name', 'li')
```

---

### 排序函数

#### `sort_rows(data, column, reverse=False, key_func=None)`

按列值排序。

```python
# 升序
sorted_data = sort_rows(data, 'age')

# 降序
sorted_data = sort_rows(data, 'age', reverse=True)

# 自定义排序
sorted_data = sort_rows(data, 'name', key_func=lambda x: x.lower())
```

---

### 列操作

#### `select_columns(data, columns)`

选择指定的列。

```python
selected = select_columns(data, ['name', 'age'])
# [{'name': 'Alice', 'age': '25'}, ...]
```

#### `add_column(data, column, value_func)`

添加新列。

```python
# 添加国家列
data = add_column(data, 'country', lambda row: 'USA')
```

#### `transform_column(data, column, transform_func)`

转换列的值。

```python
# 年龄翻倍
data = transform_column(data, 'age', lambda x: int(x) * 2)
```

#### `remove_column(data, column)`

删除列。

```python
data = remove_column(data, 'temp_column')
```

#### `rename_column(data, old_name, new_name)`

重命名列。

```python
data = rename_column(data, 'emp_id', 'id')
```

#### `get_column(data, column)`

获取单列的所有值。

```python
names = get_column(data, 'name')
# ['Alice', 'Bob', 'Charlie']
```

#### `get_unique_values(data, column)`

获取列的唯一值。

```python
cities = get_unique_values(data, 'city')
# ['NYC', 'LA', 'SF']
```

---

### 统计函数

#### `count_rows(data)`

统计行数。

```python
total = count_rows(data)  # 100
```

#### `count_by_value(data, column)`

按列值分组计数。

```python
dept_counts = count_by_value(data, 'dept')
# {'HR': 25, 'IT': 50, 'Sales': 25}
```

#### `get_numeric_stats(data, column)`

获取数值列的统计信息。

```python
stats = get_numeric_stats(data, 'salary')
# {'count': 100, 'sum': 500000, 'min': 3000, 'max': 10000, 'avg': 5000}
```

---

### 转换函数

#### `to_dict_by_key(data, key_column)`

转换为以某列为键的字典。

```python
employees = to_dict_by_key(data, 'id')
# {'1': {'name': 'Alice', ...}, '2': {'name': 'Bob', ...}}
```

#### `group_by(data, column)`

按列值分组。

```python
by_dept = group_by(data, 'dept')
# {'HR': [...], 'IT': [...], 'Sales': [...]}
```

#### `join_tables(left, right, left_key, right_key, join_type='inner')`

连接两个表。

```python
employees = [{'id': '1', 'name': 'Alice'}, {'id': '2', 'name': 'Bob'}]
salaries = [{'emp_id': '1', 'salary': '5000'}, {'emp_id': '2', 'salary': '6000'}]

joined = join_tables(employees, salaries, 'id', 'emp_id', 'inner')
# [{'id': '1', 'name': 'Alice', 'right_salary': '5000'}, ...]
```

---

### 文件操作

#### `merge_csv_files(filepaths, output_path, encoding='utf-8')`

合并多个 CSV 文件。

```python
total = merge_csv_files(
    ['part1.csv', 'part2.csv', 'part3.csv'],
    'merged.csv'
)
print(f"合并了 {total} 行")
```

#### `split_csv_file(filepath, chunk_size, output_dir, prefix='chunk')`

分割 CSV 文件。

```python
chunks = split_csv_file('large.csv', 1000, 'output/', prefix='part')
# [Path('output/part_0.csv'), Path('output/part_1.csv'), ...]
```

#### `csv_to_json(filepath, encoding='utf-8')`

转换为 JSON 字符串。

```python
json_str = csv_to_json('data.csv')
```

#### `json_to_csv(json_string, output_path, encoding='utf-8')`

JSON 转 CSV。

```python
json_to_csv('[{"name": "Alice"}]', 'output.csv')
```

---

### 流式处理

#### `process_csv_stream(filepath, process_func, output_path=None, encoding='utf-8')`

流式处理大文件。

```python
# 处理并输出到新文件
process_csv_stream(
    'input.csv',
    lambda row: {'id': row['id'], 'processed': 'yes'},
    'output.csv'
)

# 处理并返回结果
results = process_csv_stream(
    'input.csv',
    lambda row: {'id': row['id'], 'value': int(row['value']) * 2}
)
```

---

## 🧪 运行测试

```bash
cd csv_utils
python csv_utils_test.py
```

### 测试覆盖

- ✅ 基本读写操作
- ✅ 过滤和排序
- ✅ 列操作（选择、添加、转换、删除、重命名）
- ✅ 统计函数
- ✅ 数据结构转换
- ✅ 文件合并和分割
- ✅ 格式转换（CSV ↔ JSON）
- ✅ 流式处理
- ✅ 边界情况（空数据、特殊字符、Unicode）
- ✅ 错误处理（文件不存在等）

---

## 🔧 命令行工具

模块包含简单的命令行接口：

```bash
# 读取并显示前 20 行
python mod.py read data.csv

# 统计行数
python mod.py count data.csv

# 显示列名
python mod.py columns data.csv

# 显示前 10 行
python mod.py head data.csv 10
```

---

## 📝 使用示例

### 示例 1：数据清洗

```python
from mod import read_csv, write_csv, filter_rows, transform_column

# 读取数据
data = read_csv('raw_data.csv')

# 过滤无效数据
clean_data = filter_rows(data, lambda x: x['age'] and x['name'])

# 转换年龄为整数
clean_data = transform_column(clean_data, 'age', int)

# 保存
write_csv('clean_data.csv', clean_data)
```

### 示例 2：数据分析

```python
from mod import read_csv, group_by, get_numeric_stats, count_by_value

data = read_csv('sales.csv')

# 按地区分组
by_region = group_by(data, 'region')

# 计算每个地区的销售统计
for region, rows in by_region.items():
    stats = get_numeric_stats(rows, 'amount')
    print(f"{region}: 平均销售额 = {stats['avg']:.2f}")

# 产品计数
product_counts = count_by_value(data, 'product')
```

### 示例 3：大文件处理

```python
from mod import process_csv_stream

# 处理 1GB 的 CSV 文件
process_csv_stream(
    'huge_file.csv',
    lambda row: {
        'id': row['id'],
        'category': row['category'].upper(),
        'amount': float(row['amount']) * 1.1  # 加 10%
    },
    'processed.csv'
)
```

### 示例 4：表连接

```python
from mod import read_csv, join_tables, write_csv

employees = read_csv('employees.csv')
departments = read_csv('departments.csv')

# 内连接
result = join_tables(
    employees, departments,
    'dept_id', 'id',
    'inner'
)

write_csv('employees_with_dept.csv', result)
```

---

## ⚠️ 注意事项

1. **编码问题**：默认使用 UTF-8，处理其他编码请指定 `encoding` 参数
2. **大文件**：使用流式函数 `read_csv_stream` / `process_csv_stream`
3. **特殊字符**：自动处理包含逗号、引号的字段
4. **空值处理**：空单元格读取为空字符串 `''`

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
