# ID Generator

通用 ID 生成工具包，支持多种 ID 格式，零外部依赖，纯 Go 实现。

## 功能特性

- **UUID v4** - RFC 4122 标准的随机 UUID
- **Snowflake ID** - Twitter 风格的分布式 ID，支持时间戳和节点 ID 提取
- **NanoID** - URL 友好的可配置 ID
- **Short ID** - 短格式 URL 安全 ID
- **Hash ID** - 基于内容的确定性 ID
- **Sequential ID** - 带前缀的顺序 ID
- **Custom Format ID** - 自定义格式的 ID（订单号、发票号等）

## 安装

```bash
go get github.com/ayukyo/alltoolkit/Go/id_generator
```

## 使用示例

### UUID v4

```go
package main

import (
    "fmt"
    idgen "github.com/ayukyo/alltoolkit/Go/id_generator"
)

func main() {
    // 生成 UUID v4
    uuid, err := idgen.NewUUID()
    if err != nil {
        panic(err)
    }
    
    fmt.Println(uuid.String())      // 550e8400-e29b-41d4-a716-446655440000
    fmt.Println(uuid.StringNoDash()) // 550e8400e29b41d4a716446655440000
}
```

### Snowflake ID

```go
package main

import (
    "fmt"
    idgen "github.com/ayukyo/alltoolkit/Go/id_generator"
)

func main() {
    config := idgen.DefaultSnowflakeConfig()
    config.NodeID = 42  // 设置节点 ID (0-1023)
    
    gen, err := idgen.NewSnowflakeGenerator(config)
    if err != nil {
        panic(err)
    }
    
    // 生成 ID
    id, _ := gen.Generate()
    fmt.Printf("ID: %d\n", id)
    
    // 提取组件
    fmt.Printf("Node ID: %d\n", gen.ExtractNodeID(id))
    fmt.Printf("Timestamp: %v\n", gen.ExtractTime(id))
    fmt.Printf("Sequence: %d\n", gen.ExtractSequence(id))
}
```

### NanoID

```go
package main

import (
    "fmt"
    idgen "github.com/ayukyo/alltoolkit/Go/id_generator"
)

func main() {
    // 默认长度 21
    id, _ := idgen.NewNanoID()
    fmt.Println(id) // V1StGXR8_Z5jdHi6B-myT
    
    // 自定义长度
    id, _ = idgen.NewNanoIDWithSize(10)
    fmt.Println(id) // IRFa-VaY2b
    
    // 自定义字母表
    gen, _ := idgen.NewNanoIDGenerator(idgen.AlphabetLower, 16)
    id, _ = gen.Generate()
    fmt.Println(id) // 全小写
}
```

### Short ID

```go
package main

import (
    "fmt"
    idgen "github.com/ayukyo/alltoolkit/Go/id_generator"
)

func main() {
    gen := idgen.NewShortIDGenerator(8)
    id, _ := gen.Generate()
    fmt.Println(id) // x7kP9mN2
}
```

### Hash-based ID

```go
package main

import (
    "fmt"
    idgen "github.com/ayukyo/alltoolkit/Go/id_generator"
)

func main() {
    gen := idgen.NewHashIDGenerator("H-", 8)
    
    // 相同内容生成相同 ID
    id1 := gen.Generate("user@example.com")
    id2 := gen.Generate("user@example.com")
    fmt.Println(id1 == id2) // true
    
    // 不同内容生成不同 ID
    id3 := gen.Generate("other@example.com")
    fmt.Println(id1 != id3) // true
}
```

### Sequential ID

```go
package main

import (
    "fmt"
    idgen "github.com/ayukyo/alltoolkit/Go/id_generator"
)

func main() {
    gen := idgen.NewSequentialGenerator("ORD-", 6, 1)
    
    fmt.Println(gen.Next()) // ORD-000001
    fmt.Println(gen.Next()) // ORD-000002
    fmt.Println(gen.Next()) // ORD-000003
    
    gen.Reset()
    fmt.Println(gen.Next()) // ORD-000001
}
```

### Custom Format ID

```go
package main

import (
    "fmt"
    idgen "github.com/ayukyo/alltoolkit/Go/id_generator"
)

func main() {
    // 订单号格式: ORD-YYYYMMDD-XXXX-NNNN
    config := idgen.FormatSpec{
        Prefix:    "ORD-",
        Separator: "-",
        Parts: []idgen.FormatPart{
            {Type: "timestamp", Format: "20060102"},
            {Type: "random", Length: 4},
            {Type: "sequence", Length: 4},
        },
    }
    
    gen, _ := idgen.NewCustomIDGenerator(config)
    id, _ := gen.Generate()
    fmt.Println(id) // ORD-20260415-7K3M-0001
}
```

## API 参考

### UUID

| 函数 | 描述 |
|------|------|
| `NewUUID() (UUID, error)` | 生成 UUID v4 |
| `UUID.String() string` | 返回带破折号的字符串格式 |
| `UUID.StringNoDash() string` | 返回不带破折号的字符串格式 |
| `ParseUUID(s string) (UUID, error)` | 解析 UUID 字符串 |

### Snowflake ID

| 函数 | 描述 |
|------|------|
| `NewSnowflakeGenerator(config SnowflakeConfig) (*SnowflakeGenerator, error)` | 创建生成器 |
| `Generate() (int64, error)` | 生成 Snowflake ID |
| `ExtractTime(id int64) time.Time` | 提取时间戳 |
| `ExtractNodeID(id int64) int64` | 提取节点 ID |
| `ExtractSequence(id int64) int64` | 提取序列号 |

### NanoID

| 函数 | 描述 |
|------|------|
| `NewNanoID() (string, error)` | 生成默认 NanoID (21字符) |
| `NewNanoIDWithSize(size int) (string, error)` | 生成指定长度的 NanoID |
| `NewNanoIDGenerator(alphabet string, size int) (*NanoIDGenerator, error)` | 创建自定义生成器 |

### 预定义字母表

- `DefaultAlphabet` - 0-9, A-Z, a-z
- `AlphabetLower` - 0-9, a-z
- `AlphabetUpper` - 0-9, A-Z
- `AlphabetNoDups` - 排除易混淆字符 (0/O, 1/l/I)
- `AlphabetHex` - 0-9, a-f
- `AlphabetNumbers` - 0-9

## 性能

基准测试结果 (Go 1.21):

```
BenchmarkUUID-8          5000000    230 ns/op
BenchmarkSnowflake-8    10000000    120 ns/op
BenchmarkNanoID-8        5000000    280 ns/op
BenchmarkShortID-8       8000000    150 ns/op
BenchmarkHashID-8       20000000     60 ns/op
BenchmarkSequentialID-8 50000000     25 ns/op
```

## 许可证

MIT License