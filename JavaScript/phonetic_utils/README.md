# Phonetic Utils - 语音匹配算法工具集

[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Zero Dependencies](https://img.shields.io/badge/Zero-Dependencies-green.svg)](https://www.npmjs.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

JavaScript 语音匹配算法工具集，零外部依赖，纯 JavaScript 实现。用于姓名匹配、模糊搜索、拼写检查等场景。

## ✨ 功能特性

- 🔤 **Soundex** - 美国档案标准语音编码
- 🎯 **Metaphone** - 改进的英语语音编码
- 🌍 **Double Metaphone** - 支持多语言发音变体
- 🏛️ **NYSIIS** - 纽约州识别信息系统编码
- 🇳🇿 **Caverphone** - 新西兰地名匹配算法
- 📊 **相似度计算** - 多算法语音相似度对比
- 🔍 **模糊搜索** - 在列表中查找语音相似单词

## 📦 安装

```bash
# 直接复制使用，无需安装
cp -r phonetic_utils/ your_project/
```

## 🚀 快速开始

```javascript
const {
  soundex,
  metaphone,
  doubleMetaphone,
  nysiis,
  caverphone,
  phoneticSimilarity,
  findPhoneticMatches
} = require('./phonetic_utils');

// Soundex 编码
soundex('Robert');  // 'R163'
soundex('Rupert');  // 'R163' - 相同编码！

// Metaphone 编码
metaphone('phone');   // 'FN'
metaphone('know');    // 'N'

// Double Metaphone
doubleMetaphone('Catherine');
// { primary: 'K0RN', alternate: 'KTRN' }

// 计算语音相似度
phoneticSimilarity('Smith', 'Smythe', 'metaphone');  // 1
phoneticSimilarity('Robert', 'Rupert', 'soundex');    // 1

// 查找相似单词
const words = ['Smith', 'Smythe', 'Schmidt', 'Johnson'];
findPhoneticMatches('Smith', words, { algorithm: 'soundex' });
// [{ word: 'Smith', similarity: 1 }, { word: 'Smythe', similarity: 1 }]
```

## 📚 API 文档

### Soundex

```javascript
soundex(word: string): string
```

将单词转换为 4 字符 Soundex 编码。

**示例：**
```javascript
soundex('Robert');   // 'R163'
soundex('Rupert');   // 'R163'
soundex('Smith');    // 'S530'
soundex('Ashcraft'); // 'A261'
```

### Metaphone

```javascript
metaphone(word: string, maxLength: number = 4): string
```

改进的语音编码算法，更适合英语发音。

**示例：**
```javascript
metaphone('phone');     // 'FN'
metaphone('know');      // 'N'
metaphone('psychic');   // 'SKSK'
metaphone('bright');    // 'BRT'
```

### Double Metaphone

```javascript
doubleMetaphone(word: string): { primary: string, alternate: string }
```

为主词返回主编码和备用编码，支持多语言发音。

**示例：**
```javascript
doubleMetaphone('Smith');
// { primary: 'SM0', alternate: 'XMT' }

doubleMetaphone('Schmidt');
// { primary: 'SKMT', alternate: 'SKMT' }
```

### NYSIIS

```javascript
nysiis(word: string): string
```

纽约州识别信息系统编码，比 Soundex 更精确。

**示例：**
```javascript
nysiis('Smith');     // 'SNAT'
nysiis('Schmidt');   // 'SNAT' - 相同编码
nysiis('MacDonald'); // 'MCNA'
```

### Caverphone

```javascript
caverphone(word: string): string
```

10 字符编码，专为新西兰地名设计。

**示例：**
```javascript
caverphone('Thompson');  // 'TMPSN111'
caverphone('Katherine'); // 'K0RYN111'
```

### 相似度计算

```javascript
phoneticSimilarity(word1: string, word2: string, algorithm: string): number
```

计算两个单词的语音相似度（0-1）。

**支持算法：**
- `'soundex'` - Soundex 编码比较
- `'metaphone'` - Metaphone 编码比较
- `'doubleMetaphone'` - Double Metaphone 编码比较
- `'nysiis'` - NYSIIS 编码比较
- `'caverphone'` - Caverphone 编码比较

**示例：**
```javascript
phoneticSimilarity('Smith', 'Smythe', 'metaphone');     // 1
phoneticSimilarity('Robert', 'Rupert', 'soundex');      // 1
phoneticSimilarity('Catherine', 'Katherine', 'nysiis'); // 约 0.9
```

### 模糊搜索

```javascript
findPhoneticMatches(target: string, words: string[], options: object): Array
```

在单词列表中查找语音相似的单词。

**选项：**
- `algorithm` - 算法名称（默认 `'metaphone'`）
- `threshold` - 相似度阈值（默认 `0.7`）
- `limit` - 返回结果数量限制（默认 `10`）

**示例：**
```javascript
const words = ['Smith', 'Smythe', 'Schmidt', 'Johnson', 'Williams'];
findPhoneticMatches('Smith', words, {
  algorithm: 'soundex',
  threshold: 0.8
});
// [{ word: 'Smith', similarity: 1 }, { word: 'Smythe', similarity: 1 }]
```

## 🎯 应用场景

### 1. 姓名去重

```javascript
const names = ['Smith', 'Smythe', 'Johnson', 'Johnsen'];
const groups = {};

for (const name of names) {
  const code = soundex(name);
  if (!groups[code]) groups[code] = [];
  groups[code].push(name);
}
// { 'S530': ['Smith', 'Smythe'], 'J525': ['Johnson', 'Johnsen'] }
```

### 2. 模糊搜索

```javascript
const database = ['Robert Johnson', 'Rupert Johnsen', 'William Smith'];
const query = 'Robart Jonson';

const results = database.map(name => ({
  name,
  similarity: phoneticSimilarity(query, name, 'metaphone')
})).sort((a, b) => b.similarity - a.similarity);
```

### 3. 拼写检查

```javascript
const dictionary = ['through', 'though', 'thought', 'thorough'];
const misspelled = 'thru';

const suggestions = findPhoneticMatches(misspelled, dictionary, {
  algorithm: 'metaphone',
  threshold: 0.5
});
// [{ word: 'through', similarity: 0.75 }]
```

### 4. 姓名匹配系统

```javascript
function findMatchingNames(query, names) {
  const dmQuery = doubleMetaphone(query);
  
  return names.filter(name => {
    const dmName = doubleMetaphone(name);
    return dmQuery.primary === dmName.primary ||
           dmQuery.primary === dmName.alternate ||
           dmQuery.alternate === dmName.primary;
  });
}
```

## 📊 算法对比

| 算法 | 编码长度 | 特点 | 适用场景 |
|------|---------|------|---------|
| Soundex | 4 字符 | 简单快速，美国标准 | 英文姓名、档案索引 |
| Metaphone | 可变 | 更精确的英语匹配 | 英文姓名、搜索建议 |
| Double Metaphone | 4 字符×2 | 支持多种语言 | 多语言姓名、国际化应用 |
| NYSIIS | 可变 | 精确度高于 Soundex | 法律文件、身份验证 |
| Caverphone | 10 字符 | 针对地名优化 | 地名匹配、新西兰应用 |

## 🧪 运行测试

```bash
node phonetic_utils/index.test.js
```

## 📖 运行示例

```bash
node phonetic_utils/examples.js
```

## 📄 许可证

MIT License - 自由使用、修改和分发。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**注意：** 这些算法主要针对英语姓名设计，对于其他语言（如中文、日文等）效果有限。