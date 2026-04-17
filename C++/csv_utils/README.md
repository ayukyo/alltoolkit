# CSV Utils - C++ CSV 读写工具库

零外部依赖的 C++17 CSV 文件读写工具，支持流式处理大数据文件。

## 功能特性

- ✅ **完整的 CSV 解析**：支持引号、转义、多行字段
- ✅ **灵活配置**：自定义分隔符、引号字符、行尾符
- ✅ **头文件支持**：按列名访问数据
- ✅ **流式处理**：处理超大文件不占用内存
- ✅ **类型转换**：int、double、bool 自动转换
- ✅ **数据过滤**：内置 filter_rows 工具函数
- ✅ **纯头文件**：只需包含 `csv_utils.hpp`

## 快速开始

### 基础读取

```cpp
#include "csv_utils.hpp"
using namespace csv_utils;

// 从字符串解析
std::string csv = "name,age,city\nAlice,30,Beijing\nBob,25,Shanghai\n";
auto rows = parse_csv(csv, true);  // true = 有头行

for (const auto& row : rows) {
    std::cout << row[0] << ", " << row[1] << std::endl;
}

// 从文件读取
auto rows = read_csv("data.csv");
```

### 基础写入

```cpp
#include "csv_utils.hpp"
using namespace csv_utils;

std::vector<std::string> header = {"id", "name", "score"};
std::vector<CsvRow> rows;
rows.push_back(CsvRow({"1", "Alice", "95"}));
rows.push_back(CsvRow({"2", "Bob", "87"}));

// 写入文件
write_csv("output.csv", rows, header);

// 或转为字符串
std::string csv = to_csv(rows, header);
```

### 按列名访问

```cpp
CsvReader reader;
auto rows = reader.read_from_string("name,age,city\nAlice,30,Beijing");

for (const auto& row : rows) {
    std::cout << row["name"] << " from " << row["city"] << std::endl;
}
```

### 类型转换

```cpp
CsvRow row({"42", "3.14", "true", "hello"});

int64_t i = row.as_int(0);      // 42
double d = row.as_double(1);    // 3.14
bool b = row.as_bool(2);        // true
```

### 流式处理大文件

```cpp
CsvReader reader;
int total = 0;

reader.stream_from_file("huge_file.csv", [&total](const CsvRow& row) {
    // 每行逐个处理，不加载全部到内存
    total += row.as_int(2);
});

std::cout << "Total: " << total << std::endl;
```

### 自定义配置

```cpp
CsvConfig config;
config.delimiter = ';';       // 使用分号分隔
config.quote = '\'';          // 使用单引号
config.has_header = false;    // 无头行
config.skip_empty_lines = true;
config.trim_whitespace = true;

CsvReader reader(config);
auto rows = reader.read_from_file("data.csv");
```

### 数据过滤

```cpp
#include "csv_utils.hpp"
using namespace csv_utils;

auto rows = parse_csv("product,price\nApple,1.5\nBanana,0.8\nOrange,2.0");

// 过滤价格 > 1.0 的商品
auto expensive = filter_rows(rows, [](const CsvRow& row) {
    return row.as_double(1) > 1.0;
});
```

## API 参考

### CsvConfig 结构体

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| delimiter | char | ',' | 字段分隔符 |
| quote | char | '"' | 引号字符 |
| escape | char | '"' | 转义字符 |
| has_header | bool | true | 是否包含头行 |
| skip_empty_lines | bool | true | 跳过空行 |
| trim_whitespace | bool | false | 去除空白 |
| line_ending | string | "\n" | 行尾符 |

### CsvRow 类

| 方法 | 说明 |
|------|------|
| `operator[](size_t)` | 按索引访问字段 |
| `at(string)` | 按列名访问字段 |
| `size()` | 字段数量 |
| `as_int(index)` | 转为整数 |
| `as_double(index)` | 转为浮点数 |
| `as_bool(index)` | 转为布尔值 |

### CsvReader 类

| 方法 | 说明 |
|------|------|
| `read_from_file(path)` | 从文件读取 |
| `read_from_string(str)` | 从字符串读取 |
| `read_from_stream(is)` | 从流读取 |
| `stream_from_file(path, callback)` | 流式处理文件 |
| `get_header()` | 获取头行 |

### CsvWriter 类

| 方法 | 说明 |
|------|------|
| `write_to_file(path, rows, header)` | 写入文件 |
| `write_to_string(rows, header)` | 转为字符串 |
| `write_to_stream(os, rows, header)` | 写入流 |

### 工具函数

```cpp
// 快捷函数
auto rows = read_csv(filename, has_header);
write_csv(filename, rows, header, has_header);
auto rows = parse_csv(string, has_header);
string csv = to_csv(rows, header, has_header);
size_t n = count_rows(filename, has_header);
auto filtered = filter_rows(rows, predicate);
```

## 编译

```bash
# 编译测试
g++ -std=c++17 -o test csv_utils_test.cpp && ./test

# 编译示例
g++ -std=c++17 -o example example.cpp && ./example
```

## 许可证

MIT License