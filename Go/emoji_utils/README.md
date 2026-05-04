# Emoji Utils - Go 语言 Emoji 工具集

零外部依赖的 Emoji 处理工具库，提供 Emoji 检测、提取、转换、分类等完整功能。

## 功能特性

### 核心功能
- **Emoji 检测** - 判断字符是否为 Emoji
- **包含检查** - 判断字符串是否包含 Emoji
- **Emoji 计数** - 统计字符串中的 Emoji 数量
- **Emoji 提取** - 提取字符串中的所有 Emoji
- **Emoji 移除** - 移除字符串中的所有 Emoji
- **Emoji 替换** - 将 Emoji 替换为指定文本

### 分类与信息
- **Emoji 分类** - 自动分类（表情、人物、动物、食物等）
- **详细信息** - 获取 Emoji 名称、码点、是否复合等
- **分类查询** - 按分类获取 Emoji 列表

### 转换功能
- **Emoticon 转 Emoji** - 文本表情符号转 Emoji (`:)` → `😊`)
- **码点转换** - Emoji 与 Unicode 码点双向转换
- **修饰符处理** - 移除肤色修饰符、变体选择器

### 辅助功能
- **显示长度计算** - 计算 Emoji 显示长度（每个 Emoji 计为 1）
- **文本分割** - 按 Emoji/non-Emoji 分割文本
- **Emoji 验证** - 验证字符串是否为有效 Emoji

## 安装使用

```go
import emoji_utils "github.com/ayukyo/alltoolkit/Go/emoji_utils"
```

## 快速示例

```go
// 检测 Emoji
emoji_utils.IsEmoji('😀') // true

// 检查是否包含 Emoji
emoji_utils.ContainsEmoji("Hello 😀 World") // true

// 统计 Emoji 数量
emoji_utils.CountEmoji("🎉🎉🎉") // 3

// 提取所有 Emoji
emoji_utils.ExtractEmoji("Hello 😀 World 🎉") // ["😀", "🎉"]

// 移除 Emoji
emoji_utils.RemoveEmoji("Hello 😀 World") // "Hello  World"

// 获取 Emoji 分类
emoji_utils.GetEmojiCategory("😀") // CategoryFaces

// Emoticon 转 Emoji
emoji_utils.EmoticonToEmoji(":)") // "😊"

// Emoji 转 Unicode 码点
emoji_utils.EmojiToCodePoints("😀") // ["U+1F600"]
```

## API 参考

### 检测函数
| 函数 | 说明 |
|------|------|
| `IsEmoji(r rune)` | 判断 rune 是否为 Emoji |
| `ContainsEmoji(s string)` | 判断字符串是否包含 Emoji |
| `ValidateEmoji(s string)` | 验证是否为有效 Emoji 序列 |
| `IsEmojiOnly(s string)` | 判断是否仅包含 Emoji |

### 计数与提取
| 函数 | 说明 |
|------|------|
| `CountEmoji(s string)` | 统计 Emoji 数量 |
| `ExtractEmoji(s string)` | 提取所有 Emoji |
| `EmojiLength(s string)` | 计算显示长度 |

### 处理函数
| 函数 | 说明 |
|------|------|
| `RemoveEmoji(s string)` | 移除所有 Emoji |
| `ReplaceEmoji(s, replacement)` | 替换所有 Emoji |
| `StripSkinToneModifiers(emoji)` | 移除肤色修饰符 |
| `StripVariationSelectors(emoji)` | 移除变体选择器 |
| `NormalizeEmoji(emoji)` | 标准化 Emoji |

### 分类与信息
| 函数 | 说明 |
|------|------|
| `GetEmojiCategory(emoji)` | 获取 Emoji 分类 |
| `GetEmojiInfo(emoji)` | 获取详细信息 |
| `GetEmojisByCategory(category)` | 按分类获取 Emoji |

### 转换函数
| 函数 | 说明 |
|------|------|
| `EmoticonToEmoji(text)` | 文本表情转 Emoji |
| `EmojiToCodePoints(emoji)` | Emoji 转 Unicode 码点 |
| `CodePointsToEmoji(codePoints)` | Unicode 码点转 Emoji |
| `SplitByEmoji(s string)` | 按 Emoji 分割文本 |

## Emoji 分类

| 分类 | 说明 |
|------|------|
| `CategoryFaces` | 表情符号 |
| `CategoryPeople` | 人物与手势 |
| `CategoryAnimals` | 动物 |
| `CategoryFood` | 食物 |
| `CategoryTravel` | 交通与旅行 |
| `CategoryActivities` | 活动与运动 |
| `CategoryObjects` | 物品 |
| `CategorySymbols` | 符号 |
| `CategoryFlags` | 旗帜 |

## 支持的 Emoticon 转换

| Emoticon | Emoji |
|----------|-------|
| `:)` | 😊 |
| `:(` | 😢 |
| `:D` | 😀 |
| `;)` | 😉 |
| `:P` | 😛 |
| `<3` | ❤️ |
| `:O` | 😮 |
| `:*` | 😘 |

## 性能

- ContainsEmoji: ~1100 ns/op, 0 allocs
- ExtractEmoji: ~2400 ns/op, ~352 B/op, 18 allocs
- EmojiLength: ~1300 ns/op, 0 allocs

## 许可证

MIT License