# String Utils 🔤

**TypeScript 字符串工具模块 - 零依赖，生产就绪**

---

## 📖 概述

`string_utils` 是一个全面的 TypeScript 字符串操作工具模块，提供常用的字符串转换、格式化、验证、编码等功能。所有实现均使用 TypeScript/JavaScript 标准库，零外部依赖。

### ✨ 特性

- **零依赖** - 仅使用 TypeScript/JavaScript 标准库
- **大小写转换** - camelCase、PascalCase、snake_case、kebab-case 等 9 种格式
- **字符串修剪** - trim、pad、zeroPad 等
- **截断处理** - 按长度或单词数截断
- **模板插值** - 变量替换和格式化
- **转义处理** - HTML、JSON、XML、SQL、RegExp
- **模式提取** - URL、邮箱、电话、标签、提及、数字
- **字符分析** - 统计字母、数字、空格等
- **字符串操作** - 反转、替换、插入、删除、重复
- **编码工具** - Base64、Base64URL、URL 编码
- **相似度计算** - Levenshtein 距离、相似度比率
- **实用工具** - slugify、randomString、capitalize 等
- **类型安全** - 完整的 TypeScript 类型注解
- **生产就绪** - 完整的错误处理和边界检查
- **全面测试** - 100+ 测试用例覆盖所有功能

---

## 📦 安装

无需安装！直接复制 `mod.ts` 到你的项目即可使用。

```bash
# 从 AllToolkit 复制
cp AllToolkit/TypeScript/string_utils/mod.ts your_project/

# 或者克隆整个仓库
git clone https://github.com/ayukyo/alltoolkit.git
```

### 运行环境

- **Deno**: 直接运行，无需配置
- **Bun**: 直接运行，无需配置
- **Node.js 20+**: 使用 `--experimental-strip-types` 或转译后使用
- **浏览器**: 通过打包工具使用

---

## 🚀 快速开始

```typescript
import {
  toCamelCase,
  toSnakeCase,
  truncate,
  escapeHtml,
  extractEmails,
  slugify,
} from './mod.ts';

// 大小写转换
console.log(toCamelCase("hello_world"));  // "helloWorld"
console.log(toSnakeCase("helloWorld"));   // "hello_world"

// 截断
console.log(truncate("Hello World", { length: 8 }));  // "Hello..."

// 转义
console.log(escapeHtml("<script>alert('XSS')</script>"));
// "&lt;script&gt;alert(&#39;XSS&#39;)&lt;/script&gt;"

// 提取
console.log(extractEmails("Contact: test@example.com"));  // ["test@example.com"]

// Slugify
console.log(slugify("Hello World!"));  // "hello-world"
```

---

## 📚 API 参考

### 大小写转换

#### `toCamelCase(str: string): string`

转换为 camelCase。

```typescript
toCamelCase("hello_world");  // "helloWorld"
toCamelCase("Hello-World");  // "helloWorld"
toCamelCase("hello world");  // "helloWorld"
```

#### `toPascalCase(str: string): string`

转换为 PascalCase（UpperCamelCase）。

```typescript
toPascalCase("hello_world");  // "HelloWorld"
toPascalCase("hello-world");  // "HelloWorld"
```

#### `toSnakeCase(str: string): string`

转换为 snake_case。

```typescript
toSnakeCase("helloWorld");  // "hello_world"
toSnakeCase("HelloWorld");  // "hello_world"
```

#### `toScreamingSnake(str: string): string`

转换为 SCREAMING_SNAKE_CASE。

```typescript
toScreamingSnake("helloWorld");  // "HELLO_WORLD"
```

#### `toKebabCase(str: string): string`

转换为 kebab-case。

```typescript
toKebabCase("helloWorld");  // "hello-world"
```

#### `toScreamingKebab(str: string): string`

转换为 SCREAMING-KEBAB-CASE。

```typescript
toScreamingKebab("helloWorld");  // "HELLO-WORLD"
```

#### `toDotCase(str: string): string`

转换为 dot.case。

```typescript
toDotCase("helloWorld");  // "hello.world"
```

#### `toSpaceCase(str: string): string`

转换为 space case。

```typescript
toSpaceCase("helloWorld");  // "hello world"
```

#### `toTitleCase(str: string): string`

转换为 Title Case。

```typescript
toTitleCase("hello world");  // "Hello World"
```

#### `toCase(str: string, style: CaseStyle): string`

转换为指定的大小写格式。

```typescript
toCase("hello_world", "camelCase");   // "helloWorld"
toCase("helloWorld", "snake_case");   // "hello_world"
toCase("helloWorld", "kebab-case");   // "hello-world"
```

---

### 修剪和填充

#### `trim(str: string): string`

修剪两端空白。

```typescript
trim("  hello  ");  // "hello"
```

#### `trimLeft(str: string): string` / `trimRight(str: string): string`

修剪左侧/右侧空白。

```typescript
trimLeft("  hello  ");  // "hello  "
trimRight("  hello  ");  // "  hello"
```

#### `trimChars(str: string, chars: string): string`

修剪指定字符。

```typescript
trimChars("###hello###", "#");  // "hello"
```

#### `pad(str: string, options: PadOptions): string`

填充字符串到指定长度。

```typescript
pad("5", { length: 3, char: "0", position: "left" });   // "005"
pad("5", { length: 3, char: "0", position: "right" });  // "500"
pad("x", { length: 5, char: "*", position: "both" });   // "**x**"
```

#### `padLeft(str: string, length: number, char: string = ' '): string`

左侧填充。

```typescript
padLeft("5", 3, "0");  // "005"
```

#### `padRight(str: string, length: number, char: string = ' '): string`

右侧填充。

```typescript
padRight("5", 3, "0");  // "500"
```

#### `padBoth(str: string, length: number, char: string = ' '): string`

两侧填充。

```typescript
padBoth("x", 5, "*");  // "**x**"
```

#### `zeroPad(num: number | string, length: number): string`

零填充数字。

```typescript
zeroPad(5, 3);    // "005"
zeroPad("42", 4); // "0042"
```

---

### 截断

#### `truncate(str: string, options: TruncateOptions): string`

按长度截断字符串。

```typescript
truncate("Hello World", { length: 8 });  
// "Hello..."

truncate("Hello World", { length: 8, suffix: " [more]" });  
// "Hel [more]"

truncate("Hello World", { length: 8, preserveWords: true });  
// "Hello..."
```

#### `truncateWords(str: string, wordCount: number, suffix: string = '...'): string`

按单词数截断。

```typescript
truncateWords("Hello world this is a test", 3);  
// "Hello world this..."
```

---

### 模板插值

#### `interpolate(template: string, data: Record<string, unknown>, options?: TemplateOptions): string`

模板变量替换。

```typescript
interpolate("Hello, {{name}}!", { name: "World" });  
// "Hello, World!"

interpolate("{{greeting}}, {{name}}!", { greeting: "Hi", name: "Alice" });  
// "Hi, Alice!"

// 自定义定界符
interpolate("Hello, {name}!", { name: "World" }, { prefix: "{", suffix: "}" });  
// "Hello, World!"
```

#### `format(format: string, ...args: unknown[]): string`

格式化字符串（类似 C printf）。

```typescript
format("Hello {0}", "World");  
// "Hello World"

format("{0} is {1} years old", "Alice", 25);  
// "Alice is 25 years old"
```

---

### 转义处理

#### `escapeHtml(str: string): string`

转义 HTML 特殊字符。

```typescript
escapeHtml("<script>alert('XSS')</script>");  
// "&lt;script&gt;alert(&#39;XSS&#39;)&lt;/script&gt;"
```

#### `unescapeHtml(str: string): string`

反转义 HTML 实体。

```typescript
unescapeHtml("&lt;div&gt;");  // "<div>"
```

#### `escapeJson(str: string): string` / `unescapeJson(str: string): string`

转义/反转义 JSON 特殊字符。

```typescript
escapeJson("Hello\nWorld");  // "Hello\\nWorld"
escapeJson('Say "Hi"');      // "Say \\"Hi\\""
```

#### `escapeXml(str: string): string`

转义 XML 特殊字符。

```typescript
escapeXml("<tag>content</tag>");  
// "&lt;tag&gt;content&lt;/tag&gt;"
```

#### `escapeSql(str: string): string`

转义 SQL 字符串（单引号翻倍）。

```typescript
escapeSql("O'Reilly");  // "O''Reilly"
```

#### `escapeRegExp(str: string): string`

转义正则表达式特殊字符。

```typescript
escapeRegExp("hello.world");  // "hello\\.world"
```

---

### 模式提取

#### `extractUrls(str: string): string[]`

提取所有 URL。

```typescript
extractUrls("Visit https://example.com and http://test.org");  
// ["https://example.com", "http://test.org"]
```

#### `extractEmails(str: string): string[]`

提取所有邮箱地址。

```typescript
extractEmails("Contact: test@example.com or support@test.org");  
// ["test@example.com", "support@test.org"]
```

#### `extractPhoneNumbers(str: string): string[]`

提取所有电话号码。

```typescript
extractPhoneNumbers("Call 123-456-7890 or (555) 123-4567");  
// ["123-456-7890", "(555) 123-4567"]
```

#### `extractHashtags(str: string): string[]`

提取所有标签（不含 #）。

```typescript
extractHashtags("Love #typescript and #coding!");  
// ["typescript", "coding"]
```

#### `extractMentions(str: string): string[]`

提取所有提及（不含 @）。

```typescript
extractMentions("Hey @alice and @bob!");  
// ["alice", "bob"]
```

#### `extractNumbers(str: string, asFloat: boolean = false): number[]`

提取所有数字。

```typescript
extractNumbers("I have 3 apples and 5 oranges");  
// [3, 5]

extractNumbers("Price: 19.99 and 29.50", true);  
// [19.99, 29.5]
```

#### `extractBetween(str: string, start: string, end: string, includeDelimiters: boolean = false): string[]`

提取定界符之间的文本。

```typescript
extractBetween("Hello [World] and [Universe]", "[", "]");  
// ["World", "Universe"]

extractBetween("<tag>content</tag>", "<tag>", "</tag>");  
// ["content"]
```

---

### 字符分析

#### `analyzeChars(str: string): CharAnalysis`

分析字符组成。

```typescript
analyzeChars("Hello 123!");  
// {
//   total: 10,
//   letters: 5,
//   digits: 3,
//   spaces: 1,
//   punctuation: 1,
//   uppercase: 1,
//   lowercase: 4,
//   special: 0,
//   unicode: 0
// }
```

#### `countOccurrences(str: string, substring: string, caseSensitive: boolean = true): number`

计算子串出现次数。

```typescript
countOccurrences("hello hello hello", "hello");  // 3
countOccurrences("Hello HELLO hello", "hello", false);  // 3
```

#### `isAlpha(str: string): boolean`

检查是否全为字母。

```typescript
isAlpha("Hello");   // true
isAlpha("Hello123"); // false
```

#### `isAlphanumeric(str: string): boolean`

检查是否全为字母数字。

```typescript
isAlphanumeric("Hello123");  // true
isAlphanumeric("Hello 123"); // false
```

#### `isNumeric(str: string): boolean`

检查是否全为数字。

```typescript
isNumeric("123");   // true
isNumeric("12.3");  // false
```

#### `isInteger(str: string): boolean` / `isFloat(str: string): boolean`

检查是否为整数/浮点数。

```typescript
isInteger("123");    // true
isInteger("-123");   // true
isInteger("12.3");   // false

isFloat("12.34");    // true
isFloat("123");      // true
```

---

### 字符串操作

#### `reverse(str: string): string`

反转字符串。

```typescript
reverse("hello");  // "olleh"
reverse("你好");   // "好你"
```

#### `removeWhitespace(str: string): string`

移除所有空白。

```typescript
removeWhitespace("hello world");  // "helloworld"
```

#### `removeDigits(str: string): string`

移除所有数字。

```typescript
removeDigits("abc123def");  // "abcdef"
```

#### `removeSpecialChars(str: string): string`

移除所有特殊字符。

```typescript
removeSpecialChars("Hello! World@123");  // "HelloWorld123"
```

#### `replaceAll(str: string, search: string, replace: string, caseSensitive: boolean = true): string`

替换所有出现。

```typescript
replaceAll("hello hello", "hello", "hi");  
// "hi hi"

replaceAll("Hello HELLO", "hello", "hi", false);  
// "hi hi"
```

#### `insertAt(str: string, substring: string, position: number): string`

在指定位置插入。

```typescript
insertAt("Helo", "l", 2);  // "Hello"
```

#### `removeAt(str: string, start: number, length: number = 1): string`

删除指定位置的字符。

```typescript
removeAt("Hello", 1, 1);  // "Hllo"
```

#### `repeat(str: string, count: number, separator?: string): string`

重复字符串。

```typescript
repeat("ab", 3);       // "ababab"
repeat("ab", 3, "-");  // "ab-ab-ab"
```

---

### 分割和连接

#### `split(str: string, options?: SplitOptions): string[]`

分割字符串。

```typescript
split("a,b,c", { separator: "," });  
// ["a", "b", "c"]

split("a, b, c", { separator: ",", trim: true });  
// ["a", "b", "c"]

split("a,,b,,c", { separator: ",", removeEmpty: true });  
// ["a", "b", "c"]
```

#### `chunk(str: string, chunkSize: number): string[]`

分割为固定大小的块。

```typescript
chunk("abcdefgh", 3);  // ["abc", "def", "gh"]
```

#### `joinGrammar(items: string[], options?: { conjunction?: string; oxfordComma?: boolean }): string`

符合语法的连接。

```typescript
joinGrammar(["apple"]);  
// "apple"

joinGrammar(["apple", "banana"]);  
// "apple and banana"

joinGrammar(["apple", "banana", "cherry"]);  
// "apple, banana, and cherry"

joinGrammar(["apple", "banana", "cherry"], { oxfordComma: false });  
// "apple, banana and cherry"
```

---

### 编码工具

#### `toBase64(str: string): string` / `fromBase64(str: string): string`

Base64 编码/解码。

```typescript
const encoded = toBase64("Hello, World!");  
// "SGVsbG8sIFdvcmxkIQ=="

fromBase64(encoded);  // "Hello, World!"
```

#### `toBase64Url(str: string): string` / `fromBase64Url(str: string): string`

URL 安全的 Base64 编码/解码。

```typescript
toBase64Url("Hello+World/Test");  
// "SGVsbG8rV29ybGQvVGVzdA" (无 + / =)
```

#### `encodeUrl(str: string): string` / `decodeUrl(str: string): string`

URL 编码/解码。

```typescript
encodeUrl("Hello World!");  // "Hello%20World!"
decodeUrl("Hello%20World!"); // "Hello World!"
```

---

### 比较和相似度

#### `equals(str1: string, str2: string, caseSensitive: boolean = false): boolean`

比较字符串是否相等。

```typescript
equals("Hello", "Hello");  // true
equals("Hello", "hello");  // true (默认不区分大小写)
equals("Hello", "hello", true);  // false
```

#### `startsWith(str: string, prefix: string, caseSensitive: boolean = true): boolean`

检查是否以指定前缀开头。

```typescript
startsWith("Hello World", "Hello");  // true
startsWith("Hello World", "hello", false);  // true
```

#### `endsWith(str: string, suffix: string, caseSensitive: boolean = true): boolean`

检查是否以指定后缀结尾。

```typescript
endsWith("Hello World", "World");  // true
```

#### `contains(str: string, substring: string, caseSensitive: boolean = true): boolean`

检查是否包含子串。

```typescript
contains("Hello World", "lo Wo");  // true
contains("Hello World", "hello", false);  // true
```

#### `levenshtein(str1: string, str2: string): number`

计算 Levenshtein 编辑距离。

```typescript
levenshtein("kitten", "sitting");  // 3
levenshtein("abc", "abc");  // 0
```

#### `similarity(str1: string, str2: string): number`

计算相似度比率（0-1）。

```typescript
similarity("abc", "abc");  // 1.0
similarity("abc", "def");  // 0.0
similarity("kitten", "sitting");  // ~0.57
```

#### `longestCommonSubstring(str1: string, str2: string): string`

查找最长公共子串。

```typescript
longestCommonSubstring("abcdef", "zcdgh");  // "cd"
```

---

### 实用工具

#### `randomString(length: number, charset?: string): string`

生成随机字符串。

```typescript
randomString(10);  // "aB3xK9pL2m"
randomString(8, "0123456789");  // "48291057"
```

#### `slugify(str: string, options?: { lowercase?: boolean; separator?: string; removeSpecial?: boolean }): string`

创建 URL 友好的 slug。

```typescript
slugify("Hello World!");  // "hello-world"
slugify("Café & Restaurant");  // "cafe-restaurant"
```

#### `isEmpty(str: string): boolean` / `isNotEmpty(str: string): boolean`

检查字符串是否为空。

```typescript
isEmpty("");       // true
isEmpty("   ");    // true
isEmpty("hello");  // false
```

#### `capitalize(str: string): string`

首字母大写。

```typescript
capitalize("hello");  // "Hello"
```

#### `capitalizeWords(str: string): string`

每个单词首字母大写。

```typescript
capitalizeWords("hello world");  // "Hello World"
```

#### `decapitalize(str: string): string`

首字母小写。

```typescript
decapitalize("Hello");  // "hello"
```

---

## 📝 示例

查看 `examples/` 目录获取更多使用示例：

- `basic_usage.ts` - 基本用法示例
- `text_processing.ts` - 文本处理示例
- `validation.ts` - 输入验证示例
- `encoding.ts` - 编码转换示例

---

## 🧪 运行测试

```bash
cd string_utils

# Deno
deno test string_utils_test.ts

# Bun
bun test string_utils_test.ts

# Node.js 20+
node --test string_utils_test.ts
```

测试覆盖：
- 大小写转换
- 修剪和填充
- 截断处理
- 模板插值
- 转义处理
- 模式提取
- 字符分析
- 字符串操作
- 分割和连接
- 编码工具
- 比较和相似度
- 实用工具

---

## 🔒 安全注意事项

1. **XSS 防护**：使用 `escapeHtml` 转义用户输入后再插入 HTML。

2. **SQL 注入**：`escapeSql` 仅提供基本保护，生产环境请使用参数化查询。

3. **路径遍历**：处理文件路径时，不要仅依赖字符串操作，应使用路径规范化库。

4. **敏感数据**：不要使用 `randomString` 生成加密密钥，应使用 `crypto` 模块。

---

## 📊 性能提示

- 对于大量字符串操作，考虑使用数组连接而非多次字符串拼接
- `replaceAll` 比正则表达式替换更快（对于简单字符串）
- `levenshtein` 和 `similarity` 对长字符串较慢，慎用

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License
