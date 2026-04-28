# Roman Numeral Utils

罗马数字转换工具库，支持整数与罗马数字之间的双向转换，以及算术运算。

## 功能特性

- **双向转换**: 整数 ↔ 罗马数字
- **验证**: 检查字符串是否为有效的罗马数字
- **算术运算**: 加、减、乘、除
- **比较**: 比较两个罗马数字的大小
- **范围生成**: 生成指定范围内的所有罗马数字
- **扩展支持**: 支持 vinculum 记法（用于大于 3999 的数字）
- **零外部依赖**: 仅使用 Go 标准库

## 安装

```bash
go get github.com/ayukyo/alltoolkit/Go/roman_numeral_utils
```

## 使用示例

### 基本转换

```go
package main

import (
    "fmt"
    roman "github.com/ayukyo/alltoolkit/Go/roman_numeral_utils"
)

func main() {
    // 罗马数字转整数
    num, err := roman.ToInt("MCMXCIV")
    if err != nil {
        fmt.Println("Error:", err)
    }
    fmt.Println(num) // 输出: 1994

    // 整数转罗马数字
    r, err := roman.ToRoman(2024)
    if err != nil {
        fmt.Println("Error:", err)
    }
    fmt.Println(r) // 输出: MMXXIV

    // 大小写不敏感
    roman.ToInt("xiv") // 返回 14
}
```

### 验证

```go
roman.IsValid("XIV")    // true
roman.IsValid("IIII")    // false (无效格式)
roman.IsValid("ABC")     // false
```

### 算术运算

```go
// 加法
result, _ := roman.Add("X", "V")    // "XV" (15)

// 减法
result, _ = roman.Subtract("X", "I") // "IX" (9)

// 乘法
result, _ = roman.Multiply("V", "II") // "X" (10)

// 除法 (整数除法)
result, _ = roman.Divide("X", "II")  // "V" (5)
```

### 比较

```go
cmp, _ := roman.Compare("V", "I")   // 1 (V > I)
cmp, _ = roman.Compare("I", "V")     // -1 (I < V)
cmp, _ = roman.Compare("X", "X")     // 0 (相等)
```

### 范围生成

```go
// 生成 1-10 的罗马数字
range, _ := roman.GenerateRange(1, 10)
// ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
```

### 扩展记法 (Vinculum)

对于大于 3999 的数字，使用下划线表示横线记法：
- `_V_` 表示 V 上方有横线 = 5 × 1000 = 5000
- `_X_` 表示 X 上方有横线 = 10 × 1000 = 10000

```go
// 标准罗马数字 (最大 3999)
num, _ := roman.ParseWithAlternative("MCMXCIV") // 1994

// 使用 vinculum 记法 (支持更大数字)
num, _ = roman.ParseWithAlternative("_V_")  // 5000
num, _ = roman.ParseWithAlternative("M_V_") // 6000 (1000 + 5000)
```

### Must 函数

如果确定输入有效，可以使用 Must 系列函数（无效时会 panic）：

```go
num := roman.MustToInt("XIV")     // 14
r := roman.MustToRoman(14)        // "XIV"
```

## 支持范围

- **标准罗马数字**: 1 - 3999
- **扩展记法**: 可支持更大的数字（通过 vinculum）

## 错误处理

```go
// 返回的错误类型
roman.ErrEmptyString      // 空字符串
roman.ErrInvalidRoman     // 无效的罗马数字格式
roman.ErrOutOfRange       // 超出范围 (> 3999)
roman.ErrNegativeNumber   // 负数
roman.ErrZeroNotAllowed   // 零不允许
```

## 运行测试

```bash
go test -v
```

## 运行示例

```bash
cd examples
go run main.go
```

## 许可证

MIT License