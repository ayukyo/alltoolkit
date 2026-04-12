# JSON Utils 📦

**Go 语言高级 JSON 处理工具库**

基于 Go 标准库 `encoding/json` 构建的高级 JSON 操作工具，提供路径访问、合并、验证、转换等丰富功能。

---

## ✨ 特性

- **零依赖** - 仅使用 Go 标准库
- **路径访问** - 使用点号表示法访问/设置/删除 JSON 字段
- **格式转换** - Pretty Print 和 Minify
- **智能合并** - 支持深度合并多个 JSON 对象
- **Schema 验证** - 可选的 JSON Schema 验证
- **差异比较** - 比较两个 JSON 对象的差异
- **键值提取** - 提取所有键或统计值出现次数
- **文件操作** - 直接读写 JSON 文件
- **构建器模式** - 高效的 JSON 构建器
- **并发安全** - 所有函数均可安全并发使用

---

## 📦 安装

```bash
# 克隆 AllToolkit
git clone https://github.com/ayukyo/alltoolkit.git
cd alltoolkit/Go/json_utils

# 或直接复制文件到你的项目
cp json_utils.go your_project/
```

### Go Module

```go
// 在你的 go.mod 中添加
require json_utils v1.0.0

// 或者使用 replace 指向本地路径
replace json_utils => ./json_utils
```

---

## 🚀 快速开始

### 基本使用

```go
package main

import (
    "fmt"
    "json_utils"
)

func main() {
    // 格式化 JSON
    json := `{"name":"John","age":30}`
    formatted, _ := jsonutils.PrettyPrint(json, "  ")
    fmt.Println(formatted)
    
    // 压缩 JSON
    minified, _ := jsonutils.Minify(json)
    fmt.Println(minified)
    
    // 路径访问
    result := jsonutils.Get(json, "name")
    if result.Found {
        fmt.Printf("Name: %v\n", result.Value)
    }
}
```

### 路径操作

```go
json := `{"user": {"name": "John", "address": {"city": "NYC"}}}`

// 获取值
result := jsonutils.Get(json, "user.address.city")
// result.Value = "NYC"

// 设置值
modified, _ := jsonutils.Set(json, "user.age", 30)
// {"user":{"name":"John","address":{"city":"NYC"},"age":30}}

// 删除字段
deleted, _ := jsonutils.Delete(json, "user.address")
// {"user":{"name":"John"}}
```

### 合并 JSON

```go
json1 := `{"a": 1, "b": 2}`
json2 := `{"b": 3, "c": 4}`
json3 := `{"user": {"name": "John"}}`
json4 := `{"user": {"age": 30}}`

// 简单合并（后者覆盖前者）
merged, _ := jsonutils.Merge(json1, json2)
// {"a":1,"b":3,"c":4}

// 深度合并
deepMerged, _ := jsonutils.Merge(json3, json4)
// {"user":{"name":"John","age":30}}
```

---

## 📖 API 参考

### 格式化函数

| 函数 | 描述 | 参数 | 返回 |
|------|------|------|------|
| `PrettyPrint(data, indent)` | 格式化 JSON | data: JSON 数据，indent: 缩进字符串 | (string, error) |
| `Minify(data)` | 压缩 JSON | data: JSON 数据 | (string, error) |

### 路径操作

| 函数 | 描述 | 参数 | 返回 |
|------|------|------|------|
| `Get(data, path)` | 获取路径值 | path: 点号路径 | JSONPathResult |
| `Set(data, path, value)` | 设置路径值 | path: 点号路径，value: 新值 | (string, error) |
| `Delete(data, path)` | 删除路径字段 | path: 点号路径 | (string, error) |

### 数据处理

| 函数 | 描述 | 参数 | 返回 |
|------|------|------|------|
| `Merge(datas...)` | 合并多个 JSON | datas: 可变参数 | (string, error) |
| `Diff(json1, json2)` | 比较差异 | json1, json2: 待比较 JSON | (map, error) |
| `Validate(data, schema)` | 验证 JSON | schema: 可选 Schema | ValidateResult |
| `ExtractKeys(data)` | 提取所有键 | data: JSON 数据 | ([]string, error) |
| `CountValues(data, path)` | 统计值出现次数 | path: 可选路径 | (map[string]int, error) |
| `Transform(data, fn)` | 转换字符串值 | fn: 转换函数 | (string, error) |

### 文件操作

| 函数 | 描述 | 参数 | 返回 |
|------|------|------|------|
| `ReadFile(filename)` | 读取 JSON 文件 | filename: 文件路径 | (interface{}, error) |
| `WriteFile(filename, data, indent)` | 写入 JSON 文件 | indent: 可选缩进 | error |

### 类型转换

| 函数 | 描述 | 参数 | 返回 |
|------|------|------|------|
| `ToMap(data)` | 转换为 map | data: 任意 JSON 数据 | (map[string]interface{}, error) |
| `FromMap(m, target)` | 从 map 转换到结构体 | target: 结构体指针 | error |

### 构建器

```go
// JSON 对象构建器
buf := jsonutils.NewBuffer()
result := buf.StartObject().
    Key("name").String("John").
    Key("age").Number(30).
    Key("active").Bool(true).
    Key("data").Null().
    EndObject().
    String()

// JSON 数组构建器
ab := jsonutils.NewArrayBuilder()
result := ab.
    Add("first").
    Add(42).
    Add(true).
    Add(map[string]interface{}{"key": "value"}).
    String()
// ["first",42,true,{"key":"value"}]
```

---

## 📝 示例

### 配置文件处理

```go
package main

import (
    "fmt"
    "json_utils"
    "strings"
)

func main() {
    config := `{
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "mydb"
        },
        "features": ["auth", "api", "admin"]
    }`
    
    // 获取配置值
    host := jsonutils.Get(config, "database.host")
    fmt.Printf("DB Host: %v\n", host.Value)
    
    // 更新配置
    updated, _ := jsonutils.Set(config, "database.port", 5433)
    
    // 添加新配置
    updated, _ = jsonutils.Set(updated, "cache.enabled", true)
    
    // 格式化输出
    pretty, _ := jsonutils.PrettyPrint(updated, "  ")
    fmt.Println(pretty)
}
```

### API 响应处理

```go
func processAPIResponse(response string) {
    // 验证响应
    result := jsonutils.Validate(response, nil)
    if !result.Valid {
        fmt.Printf("Invalid response: %v\n", result.Errors)
        return
    }
    
    // 提取数据
    data := jsonutils.Get(response, "data.items")
    
    // 统计类型分布
    counts, _ := jsonutils.CountValues(response, "data.items.type")
    fmt.Printf("Type distribution: %v\n", counts)
    
    // 转换字段名
    normalized, _ := jsonutils.Transform(response, strings.ToLower)
}
```

### 配置差异比较

```go
func compareConfigs(old, new string) {
    diff, err := jsonutils.Diff(old, new)
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }
    
    added := diff["added"].(map[string]interface{})
    removed := diff["removed"].(map[string]interface{})
    changed := diff["changed"].(map[string]interface{})
    
    fmt.Printf("Added: %d fields\n", len(added))
    fmt.Printf("Removed: %d fields\n", len(removed))
    fmt.Printf("Changed: %d fields\n", len(changed))
    
    for key, val := range changed {
        change := val.(map[string]interface{})
        fmt.Printf("  %s: %v -> %v\n", key, change["old"], change["new"])
    }
}
```

---

## 🔧 数据结构

### JSONPathResult

```go
type JSONPathResult struct {
    Found   bool        // 是否找到
    Value   interface{} // 找到的值
    Path    string      // 查询路径
    Matches int         // 匹配数量
}
```

### ValidateResult

```go
type ValidateResult struct {
    Valid    bool     // 是否有效
    Errors   []string // 错误列表
    Warnings []string // 警告列表
}
```

### JSONSchema

```go
type JSONSchema struct {
    Name        string        // Schema 名称
    Description string        // 描述
    Fields      []SchemaField // 字段定义
}

type SchemaField struct {
    Name     string      // 字段名
    Type     string      // 类型 (string/number/boolean/array/object)
    Required bool        // 是否必填
    Default  interface{} // 默认值
}
```

---

## ⚡ 性能

基准测试结果（Go 1.21）：

```
BenchmarkPrettyPrint-8      156432      7654 ns/op
BenchmarkMinify-8           234567      5123 ns/op
BenchmarkGet-8             1234567       987 ns/op
BenchmarkMerge-8             89012     13456 ns/op
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📚 相关工具

- [string_utils](../string_utils) - 字符串处理工具
- [crypto_utils](../crypto_utils) - 加密工具
- [csv_utils](../csv_utils) - CSV 处理工具
- [xml_utils](../xml_utils) - XML 处理工具
