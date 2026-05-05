# wordle_utils

Wordle 游戏辅助工具库，提供单词过滤、字母频率分析、最优猜测建议等功能。

## 功能特性

- **单词过滤**: 根据猜测反馈过滤可能的单词
- **字母频率分析**: 计算全局和位置字母频率
- **智能建议**: 基于评分系统建议最佳猜测
- **反馈验证**: 自动检查猜测结果
- **模式匹配**: 支持通配符模式查找单词

## 安装

```go
import "github.com/ayukyo/alltoolkit/go/wordle_utils"
```

## 快速开始

### 基本使用

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/go/wordle_utils"
)

func main() {
    // 创建求解器（使用默认词库）
    solver := wordle_utils.NewWordleSolver(wordle_utils.DefaultWordList(), 5)
    
    // 获取建议猜测
    guess := solver.SuggestGuess()
    fmt.Printf("建议猜测: %s\n", guess)
    
    // 获取前5个建议
    top5 := solver.TopSuggestions(5)
    fmt.Printf("前5建议: %v\n", top5)
}
```

### 根据反馈过滤

```go
// 猜测 "crane"，反馈: 🟩🟨⬜🟨⬜ (正确/存在/不存在)
feedback := []wordle_utils.Feedback{
    wordle_utils.Correct,  // c 正确
    wordle_utils.Present,  // r 存在但位置错误
    wordle_utils.Absent,   // a 不存在
    wordle_utils.Present,  // n 存在但位置错误
    wordle_utils.Absent,   // e 不存在
}

possibleWords := solver.FilterWords("crane", feedback)
fmt.Printf("剩余可能单词: %v\n", possibleWords)
```

### 检查猜测结果

```go
guess := "crane"
target := "cloud"

feedback := wordle_utils.CheckGuess(guess, target)
fmt.Printf("反馈: %s\n", wordle_utils.FeedbackToString(feedback))
// 输出: 🟩⬜🟨⬜⬜
```

### 从字符串解析反馈

```go
// G = green (正确), Y = yellow (存在), X/? = gray (不存在)
feedback := wordle_utils.FeedbackFromString("GYXYG")
// feedback = [Correct, Present, Absent, Present, Correct]
```

### 模式匹配查找

```go
// 查找匹配模式的单词 (_ 表示未知)
words := solver.WordsWithPattern("__a_e")
// 返回: ["apple", "crate", "plate", ...]
```

### 字母频率分析

```go
// 全局字母频率
freq := solver.LetterFrequency()
fmt.Printf("'e' 出现频率: %.2f%%\n", freq['e']*100)

// 位置字母频率
posFreq := solver.PositionFrequency()
fmt.Printf("位置0的 's' 频率: %.2f%%\n", posFreq[0]['s']*100)

// 最常见字母
common := solver.CommonLetters(5)
fmt.Printf("最常见5个字母: %c\n", common)
```

### 统计信息

```go
stats := solver.Statistics()
fmt.Printf("总单词数: %d\n", stats["total_words"])
fmt.Printf("可能单词数: %d\n", stats["possible_words"])
fmt.Printf("已猜测次数: %d\n", stats["guesses_made"])
fmt.Printf("最佳猜测: %s\n", stats["best_guess"])
```

## API 参考

### 类型

```go
type Feedback int

const (
    Absent  Feedback = iota // 字母不存在 (灰色)
    Present                 // 字母存在但位置错误 (黄色)
    Correct                 // 字母正确 (绿色)
)

type WordleSolver struct { ... }
```

### WordleSolver 方法

| 方法 | 说明 |
|------|------|
| `NewWordleSolver(wordList []string, wordLength int)` | 创建新求解器 |
| `FilterWords(guess string, feedback []Feedback) []string` | 根据反馈过滤单词 |
| `GetPossibleWords() []string` | 获取当前可能的单词 |
| `SuggestGuess() string` | 建议最佳猜测 |
| `SuggestGuessFromAll() string` | 从全部单词中建议 |
| `TopSuggestions(n int) []string` | 返回前N个建议 |
| `ScoreWord(word string) float64` | 计算单词得分 |
| `LetterFrequency() map[rune]float64` | 计算字母频率 |
| `PositionFrequency() []map[rune]float64` | 计算位置频率 |
| `CommonLetters(n int) []rune` | 获取最常见字母 |
| `WordsContaining(letter rune) []string` | 包含某字母的单词 |
| `WordsWithPattern(pattern string) []string` | 匹配模式的单词 |
| `Statistics() map[string]interface{}` | 获取统计信息 |
| `Reset()` | 重置求解器 |

### 辅助函数

| 函数 | 说明 |
|------|------|
| `CheckGuess(guess, target string) []Feedback` | 检查猜测结果 |
| `FeedbackToString(feedback []Feedback) string` | 反馈转Emoji字符串 |
| `FeedbackFromString(s string) []Feedback` | 字符串转反馈 |
| `IsWinningFeedback(feedback []Feedback) bool` | 是否获胜 |
| `DefaultWordList() []string` | 默认5字母词库 |

## 使用示例

### 完整游戏流程

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/go/wordle_utils"
)

func main() {
    // 创建求解器
    solver := wordle_utils.NewWordleSolver(wordle_utils.DefaultWordList(), 5)
    
    fmt.Println("=== Wordle 求解器 ===")
    fmt.Printf("词库大小: %d 个单词\n\n", len(solver.GetPossibleWords()))
    
    // 第一轮猜测
    guess := solver.SuggestGuess()
    fmt.Printf("第1轮建议: %s\n", guess)
    fmt.Println("输入反馈 (G=正确, Y=存在, X=不存在): GYXYG")
    
    // 模拟反馈
    feedback := wordle_utils.FeedbackFromString("GYXYG")
    
    // 过滤
    remaining := solver.FilterWords(guess, feedback)
    fmt.Printf("剩余可能: %d 个单词\n", len(remaining))
    
    if wordle_utils.IsWinningFeedback(feedback) {
        fmt.Println("🎉 恭喜猜中！")
        return
    }
    
    // 继续下一轮
    guess2 := solver.SuggestGuess()
    fmt.Printf("\n第2轮建议: %s\n", guess2)
    
    // 查看统计
    stats := solver.Statistics()
    fmt.Printf("\n统计信息:\n")
    fmt.Printf("  剩余单词: %d\n", stats["remaining_words"])
    fmt.Printf("  最常见字母: %c\n", stats["top_letters"])
}
```

### 自定义词库

```go
// 使用自定义词库
words := []string{"apple", "bread", "crane", "dream", "flame", "grape", "house", "juice"}
solver := wordle_utils.NewWordleSolver(words, 5)

// 或加载文件
// data, _ := os.ReadFile("words.txt")
// words := strings.Split(string(data), "\n")
```

## 测试

```bash
# 运行所有测试
go test -v ./...

# 运行特定测试
go test -v -run TestCheckGuess

# 查看覆盖率
go test -cover ./...
```

## 测试覆盖

- ✅ 单词过滤（正确/存在/不存在）
- ✅ 字母频率分析
- ✅ 位置频率分析
- ✅ 猜测建议
- ✅ 反馈验证
- ✅ 双字母处理
- ✅ 模式匹配
- ✅ 边界条件
- ✅ 空词库处理
- ✅ 重置功能

## 算法说明

### 评分系统

单词评分基于两个因素：

1. **字母频率**: 单词中不重复字母的全局出现频率
2. **位置频率**: 字符在特定位置的频率

```go
score = Σ(字母频率 × 10) + Σ(位置频率 × 5)
```

不重复字母获得更高权重，鼓励猜测能快速排除更多字母的单词。

### 过滤逻辑

过滤考虑以下情况：

1. **正确 (绿色)**: 候选词必须在对应位置有相同字母
2. **存在 (黄色)**: 候选词必须包含该字母，但不能在该位置
3. **不存在 (灰色)**: 字母在候选词中的数量不能超过已确认的数量

## 许可证

MIT License