# Text Analyzer Utils - 文本分析工具集

零外部依赖的 JavaScript 文本分析工具库，支持中英文混合文本。

## 安装

```javascript
const textAnalyzer = require('./text_analyzer_utils/mod.js');
```

## 功能列表

### 📊 基础统计

| 函数 | 说明 |
|------|------|
| `countCharacters(text, options)` | 统计字符数，可选是否包含空格/标点 |
| `countWords(text)` | 统计单词数（支持中英文混合） |
| `countSentences(text)` | 统计句子数 |
| `countParagraphs(text)` | 统计段落数 |
| `getTextStatistics(text)` | 获取完整统计信息 |

### ⏱️ 阅读时间

| 函数 | 说明 |
|------|------|
| `estimateReadingTime(text, options)` | 估算阅读时间 |

### 📈 词汇频率

| 函数 | 说明 |
|------|------|
| `analyzeWordFrequency(text, options)` | 分析词汇频率 |

### 📖 可读性指标

| 函数 | 说明 |
|------|------|
| `calculateFleschKincaid(text)` | 计算 Flesch-Kincaid 可读性（英文） |
| `calculateChineseReadability(text)` | 计算中文可读性评分 |
| `countSyllables(word)` | 计算英文单词音节数 |

### 🔑 关键词提取

| 函数 | 说明 |
|------|------|
| `extractKeywords(text, options)` | 提取关键词 |

### 🧩 句子复杂度

| 函数 | 说明 |
|------|------|
| `analyzeSentenceComplexity(text)` | 分析句子复杂度 |

### 📋 综合分析

| 函数 | 说明 |
|------|------|
| `getFullAnalysis(text)` | 获取完整分析报告 |

## 使用示例

### 基础统计

```javascript
const text = `Hello world! 你好世界。
This is a sample text.`;

// 字符数
console.log(textAnalyzer.countCharacters(text)); // 43

// 单词数（中英文混合）
console.log(textAnalyzer.countWords(text)); // 10

// 句子数
console.log(textAnalyzer.countSentences(text)); // 3

// 完整统计
console.log(textAnalyzer.getTextStatistics(text));
// {
//   characters: 43,
//   charactersNoSpaces: 36,
//   words: 10,
//   sentences: 3,
//   paragraphs: 2,
//   avgWordsPerSentence: "3.33",
//   avgCharsPerWord: "3.60"
// }
```

### 阅读时间估算

```javascript
const longText = `很长的文章内容...`;

const readingTime = textAnalyzer.estimateReadingTime(longText);
console.log(readingTime.formatted); // "2分30秒"
console.log(readingTime.details);
// {
//   englishWords: 100,
//   chineseChars: 500,
//   englishTime: 0.5,
//   chineseTime: 1.67
// }
```

### 词汇频率分析

```javascript
const text = `JavaScript is a programming language. 
JavaScript is versatile and popular.`;

const freq = textAnalyzer.analyzeWordFrequency(text, {
  removeStopWords: true,
  topN: 10,
  caseSensitive: false,
});

console.log(freq.words);
// [
//   { word: "javascript", count: 2, percentage: "28.57" },
//   { word: "programming", count: 1, percentage: "14.29" },
//   { word: "language", count: 1, percentage: "14.29" },
//   ...
// ]
```

### 可读性分析

```javascript
const englishText = `The quick brown fox jumps over the lazy dog...`;
const flesch = textAnalyzer.calculateFleschKincaid(englishText);
console.log(flesch);
// {
//   score: "72.50",
//   gradeLevel: "7.2",
//   grade: "高中",
//   description: "较易阅读",
//   details: { words: 100, sentences: 8, ... }
// }

const chineseText = `自然语言处理是人工智能的重要分支...`;
const chinese = textAnalyzer.calculateChineseReadability(chineseText);
console.log(chinese);
// {
//   score: "85.00",
//   level: "通俗易懂",
//   description: "适合大众阅读，语言流畅",
//   details: { chineseChars: 50, sentences: 3, ... }
// }
```

### 关键词提取

```javascript
const article = `人工智能正在改变世界。
机器学习和深度学习是人工智能的核心技术。
这些技术已应用于医疗、金融、教育等领域。`;

const keywords = textAnalyzer.extractKeywords(article, {
  topN: 5,
  minLength: 2,
});

console.log(keywords.keywords);
// [
//   { word: "人工智能", count: 2, score: "4.80", inFirstParagraph: true },
//   { word: "学习", count: 2, score: "4.00", inFirstParagraph: false },
//   ...
// ]
```

### 句子复杂度分析

```javascript
const text = `This is a simple sentence. 
However, this is a more complex sentence, which contains multiple clauses, 
and it demonstrates how sentence complexity can vary significantly.`;

const complexity = textAnalyzer.analyzeSentenceComplexity(text);
console.log(complexity);
// {
//   overallScore: "35.00",
//   level: "中等",
//   totalSentences: 2,
//   sentences: [
//     { sentence: "This is a simple sentence", complexity: 10, level: "简单", ... },
//     { sentence: "However, this is a more complex...", complexity: 60, level: "复杂", ... }
//   ],
//   summary: { simple: 1, moderate: 0, complex: 1 }
// }
```

### 综合分析

```javascript
const article = `你的文章内容...`;

const analysis = textAnalyzer.getFullAnalysis(article);
console.log(analysis);
// {
//   statistics: { characters: 500, words: 200, ... },
//   readingTime: { minutes: 1, seconds: 30, formatted: "1分30秒" },
//   wordFrequency: { words: [...], total: 200, unique: 80 },
//   readability: {
//     english: { score: "65.00", ... },
//     chinese: { score: "78.00", ... }
//   },
//   keywords: { keywords: [...], totalCandidates: 50 },
//   sentenceComplexity: { overallScore: "42.00", level: "中等", ... }
// }
```

## API 详细说明

### countCharacters(text, options)

统计文本中的字符数。

**参数：**
- `text` (string): 输入文本
- `options` (Object): 选项
  - `includeSpaces` (boolean): 是否包含空格，默认 true
  - `includePunctuation` (boolean): 是否包含标点，默认 true

**返回：** number - 字符数

---

### countWords(text)

统计文本中的单词数，支持中英文混合。

**参数：**
- `text` (string): 输入文本

**返回：** number - 单词数

---

### estimateReadingTime(text, options)

估算阅读时间。

**参数：**
- `text` (string): 输入文本
- `options` (Object): 选项
  - `wordsPerMinute` (number): 英文阅读速度，默认 200 词/分钟
  - `chineseCharsPerMinute` (number): 中文阅读速度，默认 300 字/分钟

**返回：** Object - 包含 minutes, seconds, formatted, details

---

### analyzeWordFrequency(text, options)

分析词汇频率。

**参数：**
- `text` (string): 输入文本
- `options` (Object): 选项
  - `removeStopWords` (boolean): 是否移除停用词，默认 true
  - `topN` (number): 返回前 N 个高频词，默认 20
  - `caseSensitive` (boolean): 是否区分大小写，默认 false

**返回：** Object - 包含 words, total, unique, averageFrequency

---

### extractKeywords(text, options)

提取关键词。

**参数：**
- `text` (string): 输入文本
- `options` (Object): 选项
  - `topN` (number): 返回前 N 个关键词，默认 10
  - `minLength` (number): 最小词长，默认 2

**返回：** Object - 包含 keywords, totalCandidates

## 常量

```javascript
// 英文停用词
textAnalyzer.STOP_WORDS_EN // Set { 'a', 'an', 'the', ... }

// 中文停用词
textAnalyzer.STOP_WORDS_ZH // Set { '的', '了', '和', ... }
```

## 运行测试

```bash
node text_analyzer_utils/test.js
```

## 特性

- ✅ 零外部依赖
- ✅ 支持中英文混合文本
- ✅ 完整的单元测试
- ✅ 多种分析维度
- ✅ 灵活的配置选项

## License

MIT