# pluralize_utils

Go 语言实现的英文单词单复数转换工具。零外部依赖，纯 Go 实现。

## 功能

- **单数转复数** (`SingularToPlural`) - 将单数形式转换为复数形式
- **复数转单数** (`PluralToSingular`) - 将复数形式转换为单数形式
- **判断是否为复数** (`IsPlural`) - 检查单词是否为复数形式
- **根据数量获取正确形式** (`GetPluralForm`) - 根据计数返回单数或复数形式
- **批量转换** (`BatchPluralize`, `BatchSingularize`) - 批量处理多个单词
- **冠词处理** (`GetArticle`) - 返回正确的冠词 ("a" 或 "an")
- **格式化数量** (`FormatCount`) - 格式化数量和单词的组合

## 安装

```go
import pluralize "github.com/ayukyo/alltoolkit/Go/pluralize_utils"
```

## 使用示例

### 基本转换

```go
package main

import (
    "fmt"
    pluralize "github.com/ayukyo/alltoolkit/Go/pluralize_utils"
)

func main() {
    // 单数转复数
    fmt.Println(pluralize.SingularToPlural("cat"))      // cats
    fmt.Println(pluralize.SingularToPlural("box"))      // boxes
    fmt.Println(pluralize.SingularToPlural("city"))     // cities
    fmt.Println(pluralize.SingularToPlural("knife"))    // knives
    fmt.Println(pluralize.SingularToPlural("child"))    // children
    fmt.Println(pluralize.SingularToPlural("man"))      // men
    
    // 复数转单数
    fmt.Println(pluralize.PluralToSingular("cats"))     // cat
    fmt.Println(pluralize.PluralToSingular("boxes"))    // box
    fmt.Println(pluralize.PluralToSingular("cities"))   // city
    fmt.Println(pluralize.PluralToSingular("children")) // child
}
```

### 带计数参数

```go
// count=1 时返回单数形式
fmt.Println(pluralize.SingularToPlural("cat", 1))  // cat
fmt.Println(pluralize.SingularToPlural("cat", 2))  // cats
fmt.Println(pluralize.SingularToPlural("cat", 0))  // cats

// GetPluralForm 根据计数返回正确形式
fmt.Println(pluralize.GetPluralForm("cat", 1))     // cat
fmt.Println(pluralize.GetPluralForm("cat", 5))     // cats
fmt.Println(pluralize.GetPluralForm("cats", 1))    // cat
```

### 判断是否为复数

```go
fmt.Println(pluralize.IsPlural("cats"))     // true
fmt.Println(pluralize.IsPlural("cat"))      // false
fmt.Println(pluralize.IsPlural("men"))      // true
fmt.Println(pluralize.IsPlural("news"))     // false (以 s 结尾但为单数)
fmt.Println(pluralize.IsPlural("sheep"))    // false (不可数名词)
```

### 批量操作

```go
// 批量转复数
words := []string{"cat", "dog", "box", "city"}
plurals := pluralize.BatchPluralize(words)
fmt.Println(plurals)  // [cats, dogs, boxes, cities]

// 批量转单数
plurals := []string{"cats", "dogs", "boxes", "cities"}
singulars := pluralize.BatchSingularize(plurals)
fmt.Println(singulars)  // [cat, dog, box, city]
```

### 冠词处理

```go
fmt.Println(pluralize.GetArticle("cat"))     // a
fmt.Println(pluralize.GetArticle("apple"))   // an
fmt.Println(pluralize.GetArticle("orange"))  // an
fmt.Println(pluralize.GetArticle("cat", 2))  // "" (空字符串，因为 count != 1)
```

### 格式化数量

```go
fmt.Println(pluralize.FormatCount("cat", 1))   // a cat
fmt.Println(pluralize.FormatCount("apple", 1)) // an apple
fmt.Println(pluralize.FormatCount("cat", 2))   // 2 cats
fmt.Println(pluralize.FormatCount("box", 5))   // 5 boxes
fmt.Println(pluralize.FormatCount("child", 10)) // 10 children
```

## 支持的规则

### 规则变化

| 类型 | 规则 | 示例 |
|------|------|------|
| 基本规则 | +s | cat → cats, dog → dogs |
| -s/-x/-z/-ch/-sh | +es | box → boxes, bus → buses, church → churches |
| 辅音+y | y→ies | city → cities, baby → babies |
| 元音+y | +s | day → days, boy → boys |
| -f/-fe | f/fe→ves | knife → knives, leaf → leaves |
| -o (部分) | +es | potato → potatoes, tomato → tomatoes |
| -o (其他) | +s | photo → photos, piano → pianos |

### 不规则变化

| 单数 | 复数 | 类型 |
|------|------|------|
| man | men | 不规则变化 |
| woman | women | 不规则变化 |
| child | children | 不规则变化 |
| person | people | 不规则变化 |
| foot | feet | 不规则变化 |
| tooth | teeth | 不规则变化 |
| goose | geese | 不规则变化 |
| mouse | mice | 不规则变化 |
| ox | oxen | 不规则变化 |

### 拉丁/希腊源词

| 单数 | 复数 |
|------|------|
| analysis | analyses |
| phenomenon | phenomena |
| criterion | criteria |
| datum | data |
| medium | media |
| focus | foci |
| nucleus | nuclei |
| stimulus | stimuli |

### 不可数名词（单复数同形）

- sheep, deer, fish, species, series, moose
- information, news, knowledge, advice
- mathematics, physics, economics, politics

### 连字符复合词

只变化主要名词：
- brother-in-law → brothers-in-law
- mother-in-law → mothers-in-law
- passer-by → passers-by

### 代词

- he → they
- she → they
- it → they
- this → these
- that → those

## 大小写保持

工具会自动保持原始大小写：

```go
fmt.Println(pluralize.SingularToPlural("Cat"))    // Cats
fmt.Println(pluralize.SingularToPlural("CAT"))    // CATS
fmt.Println(pluralize.SingularToPlural("Child"))  // Children
```

## 运行测试

```bash
cd Go/pluralize_utils
go test -v
```

## 运行示例

```bash
cd Go/pluralize_utils/examples
go run main.go
```

## 注意事项

- `SingularToPlural` 函数假设输入是单数形式。如果输入已经是复数形式（如 "cats"），会按规则处理（"cats" → "catses"，因为以 -s 结尾会加 -es）
- 不可数名词返回原词不变
- 以 -s 结尾的单数词（如 news, politics）会被正确识别为单数

## 许可证

MIT License