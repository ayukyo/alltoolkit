# String Utils 🔤

**Java 字符串工具类 - 零依赖，生产就绪**

---

## 📖 概述

`StringUtils` 是一个全面的 Java 字符串操作工具类，提供常用的字符串转换、格式化、验证、编码等功能。所有实现均使用 Java 标准库，零外部依赖。

### ✨ 特性

- **零依赖** - 仅使用 Java 标准库（Java 8+）
- **大小写转换** - camelCase、PascalCase、snake_case、kebab-case 等 9 种格式
- **字符串修剪** - trim、pad、zeroPad、center 等
- **截断处理** - 按长度或单词数截断
- **模板插值** - 变量替换和格式化
- **转义处理** - HTML、JSON、XML、SQL、RegExp、URL
- **模式提取** - URL、邮箱、电话、标签、提及、数字
- **字符分析** - 统计字母、数字、空格等
- **字符串操作** - 反转、替换、插入、删除、重复
- **编码工具** - Base64、Base64URL 编码解码
- **相似度计算** - Levenshtein 距离、相似度比率
- **实用工具** - slugify、randomString、capitalize 等
- **中文支持** - 中文字符检测、提取、回文判断
- **生产就绪** - 完整的错误处理和边界检查
- **全面测试** - 100+ 测试用例覆盖所有功能

---

## 📦 安装

无需安装！直接复制 `StringUtils.java` 到你的项目即可使用。

```bash
# 从 AllToolkit 复制
cp AllToolkit/Java/string_utils/StringUtils.java your_project/

# 或者克隆整个仓库
git clone https://github.com/ayukyo/alltoolkit.git
```

### 运行环境

- **Java 8+** - 完全兼容
- **Android** - 兼容（使用标准库部分）
- **无需任何外部依赖**

---

## 🚀 快速开始

```java
import string_utils.StringUtils;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        // 大小写转换
        System.out.println(StringUtils.toCamelCase("hello_world"));  // "helloWorld"
        System.out.println(StringUtils.toSnakeCase("helloWorld"));   // "hello_world"
        System.out.println(StringUtils.toKebabCase("Hello World"));  // "hello-world"
        
        // 截断
        System.out.println(StringUtils.truncate("Hello World", 8));  // "Hello..."
        
        // HTML 转义
        System.out.println(StringUtils.escapeHtml("<script>alert('XSS')</script>"));
        // "&lt;script&gt;alert(&#39;XSS&#39;)&lt;/script&gt;"
        
        // 提取
        System.out.println(StringUtils.extractEmails("Contact: test@example.com"));
        // ["test@example.com"]
        
        // Slugify
        System.out.println(StringUtils.slugify("Hello World!"));  // "hello-world"
        
        // Base64
        String encoded = StringUtils.base64Encode("Hello");
        System.out.println(encoded);  // "SGVsbG8="
        System.out.println(StringUtils.base64Decode(encoded));  // "Hello"
        
        // 相似度
        System.out.println(StringUtils.similarityRatio("hello", "helo"));  // 0.8
    }
}
```

---

## 📚 API 文档

### 大小写转换

| 方法 | 描述 | 示例 |
|------|------|------|
| `toCamelCase(String)` | 驼峰命名 | `"hello_world"` → `"helloWorld"` |
| `toPascalCase(String)` | 大驼峰命名 | `"hello_world"` → `"HelloWorld"` |
| `toSnakeCase(String)` | 蛇形命名 | `"helloWorld"` → `"hello_world"` |
| `toKebabCase(String)` | 短横线命名 | `"helloWorld"` → `"hello-world"` |
| `toConstantCase(String)` | 常量命名 | `"helloWorld"` → `"HELLO_WORLD"` |
| `toDotCase(String)` | 点分隔命名 | `"helloWorld"` → `"hello.world"` |
| `toPathCase(String)` | 路径命名 | `"helloWorld"` → `"hello/world"` |
| `toSpaceCase(String)` | 空格分隔 | `"helloWorld"` → `"hello world"` |
| `toSentenceCase(String)` | 句子大小写 | `"hello WORLD"` → `"Hello world"` |

### 字符串修剪和填充

| 方法 | 描述 | 示例 |
|------|------|------|
| `trim(String)` | 修剪两端空白 | `"  hi  "` → `"hi"` |
| `trimLeft(String)` | 修剪左端空白 | `"  hi  "` → `"hi  "` |
| `trimRight(String)` | 修剪右端空白 | `"  hi  "` → `"  hi"` |
| `padLeft(String, int, char)` | 左侧填充 | `padLeft("123", 5, '0')` → `"00123"` |
| `padRight(String, int, char)` | 右侧填充 | `padRight("123", 5, ' ')` → `"123  "` |
| `zeroPad(String, int)` | 左侧补零 | `zeroPad("42", 4)` → `"0042"` |
| `center(String, int, char)` | 居中 | `center("hi", 5, '*')` → `"**hi*"` |

### 截断处理

| 方法 | 描述 | 示例 |
|------|------|------|
| `truncate(String, int)` | 按长度截断（默认后缀 "..."） | `truncate("Hello World", 8)` → `"Hello..."` |
| `truncate(String, int, String)` | 按长度截断（自定义后缀） | `truncate("Hello", 3, "!")` → `"He!"` |
| `truncateWords(String, int)` | 按单词数截断 | `truncateWords("Hello World Test", 2)` → `"Hello World..."` |

### 模板插值

| 方法 | 描述 | 示例 |
|------|------|------|
| `interpolate(String, Map)` | 模板变量替换（${var}语法） | `interpolate("Hi ${name}", {name:"Bob"})` → `"Hi Bob"` |
| `format(String, Object...)` | 格式化字符串（{0}语法） | `format("Hello {0}", "World")` → `"Hello World"` |

### 转义处理

| 方法 | 描述 | 示例 |
|------|------|------|
| `escapeHtml(String)` | HTML 转义 | `"<div>"` → `"&lt;div&gt;"` |
| `unescapeHtml(String)` | HTML 反转义 | `"&lt;div&gt;"` → `"<div>"` |
| `escapeXml(String)` | XML 转义 | `"'test'"` → `"&apos;test&apos;"` |
| `escapeJson(String)` | JSON 转义 | `"\n"` → `"\\n"` |
| `escapeSql(String)` | SQL 转义 | `"O'Brien"` → `"O''Brien"` |
| `escapeRegex(String)` | 正则转义 | `".test"` → `"\\Q.test\\E"` |
| `urlEncode(String)` | URL 编码 | `"a b"` → `"a+b"` |
| `urlDecode(String)` | URL 解码 | `"a+b"` → `"a b"` |

### 模式提取

| 方法 | 描述 | 返回类型 |
|------|------|----------|
| `extractEmails(String)` | 提取所有邮箱 | `List<String>` |
| `extractUrls(String)` | 提取所有 URL | `List<String>` |
| `extractPhoneNumbers(String)` | 提取所有电话号码 | `List<String>` |
| `extractHashtags(String)` | 提取所有标签 | `List<String>` |
| `extractMentions(String)` | 提取所有提及 | `List<String>` |
| `extractNumbers(String)` | 提取所有数字 | `List<String>` |

### 字符统计分析

| 方法 | 描述 | 示例 |
|------|------|------|
| `countLetters(String)` | 统计字母数量 | `countLetters("Hello123")` → `5` |
| `countDigits(String)` | 统计数字数量 | `countDigits("Hello123")` → `3` |
| `countWhitespace(String)` | 统计空白字符 | `countWhitespace("a b")` → `1` |
| `countSpecialChars(String)` | 统计特殊字符 | `countSpecialChars("a!b")` → `1` |
| `getCharStats(String)` | 获取完整统计 | `Map<String, Integer>` |

### 字符串操作

| 方法 | 描述 | 示例 |
|------|------|------|
| `reverse(String)` | 反转字符串 | `reverse("hello")` → `"olleh"` |
| `replace(String, String, String, int)` | 替换子串 | `replace("aaa", "a", "b", 2)` → `"bba"` |
| `insert(String, String, int)` | 插入字符串 | `insert("Hello", "X", 3)` → `"HelXlo"` |
| `delete(String, int, int)` | 删除子串 | `delete("Hello", 2, 3)` → `"Helo"` |
| `repeat(String, int)` | 重复字符串 | `repeat("ab", 3)` → `"ababab"` |
| `capitalize(String)` | 首字母大写 | `capitalize("hello")` → `"Hello"` |
| `uncapitalize(String)` | 首字母小写 | `uncapitalize("Hello")` → `"hello"` |
| `swapCase(String)` | 交换大小写 | `swapCase("Hello")` → `"hELLO"` |
| `isPalindrome(String)` | 回文检查 | `isPalindrome("上海自来水来自海上")` → `true` |
| `join(String, String...)` | 连接字符串 | `join(",", "a","b","c")` → `"a,b,c"` |
| `split(String, String)` | 分割字符串 | `split("a,b,c", ",")` → `["a","b","c"]` |

### Base64 编码解码

| 方法 | 描述 | 示例 |
|------|------|------|
| `base64Encode(String)` | Base64 编码 | `base64Encode("Hello")` → `"SGVsbG8="` |
| `base64Decode(String)` | Base64 解码 | `base64Decode("SGVsbG8=")` → `"Hello"` |
| `base64UrlEncode(String)` | Base64URL 编码 | URL 安全的 Base64 |
| `base64UrlDecode(String)` | Base64URL 解码 | URL 安全的 Base64 |

### 相似度计算

| 方法 | 描述 | 示例 |
|------|------|------|
| `levenshteinDistance(String, String)` | 编辑距离 | `levenshteinDistance("kitten", "sitting")` → `3` |
| `similarityRatio(String, String)` | 相似度比率 (0-1) | `similarityRatio("hello", "helo")` → `0.8` |

### 实用工具

| 方法 | 描述 | 示例 |
|------|------|------|
| `slugify(String)` | 生成 URL 友好字符串 | `slugify("Hello World!")` → `"hello-world"` |
| `randomString(int, String)` | 生成随机字符串 | `randomString(8, "abc")` → `"bacbcaba"` |
| `randomAlphanumeric(int)` | 生成随机字母数字 | `randomAlphanumeric(16)` → `"aB3dE5fG7hI9jK1L"` |
| `randomHex(int)` | 生成随机十六进制 | `randomHex(8)` → `"A3F5C7E9"` |
| `containsChinese(String)` | 检测中文字符 | `containsChinese("你好")` → `true` |
| `extractChinese(String)` | 提取中文字符 | `extractChinese("Hello 世界")` → `"世界"` |

---

## 💡 使用场景

### 1. Web 开发 - 防止 XSS 攻击

```java
String userInput = request.getParameter("comment");
String safeOutput = StringUtils.escapeHtml(userInput);
response.getWriter().write("<p>" + safeOutput + "</p>");
```

### 2. API 开发 - 字段命名转换

```java
// JSON (camelCase) → 数据库 (snake_case)
String jsonField = "userName";
String dbColumn = StringUtils.toSnakeCase(jsonField);  // "user_name"

// 数据库 (snake_case) → Java 变量 (camelCase)
String dbField = "user_first_name";
String javaVar = StringUtils.toCamelCase(dbField);  // "userFirstName"
```

### 3. 内容处理 - 提取关键信息

```java
String content = getEmailContent();
List<String> emails = StringUtils.extractEmails(content);
List<String> urls = StringUtils.extractUrls(content);
List<String> phones = StringUtils.extractPhoneNumbers(content);
```

### 4. 搜索 - 拼写纠错

```java
String input = "helo";
List<String> dictionary = Arrays.asList("hello", "help", "held");

String bestMatch = null;
double bestScore = 0;

for (String word : dictionary) {
    double score = StringUtils.similarityRatio(input, word);
    if (score > bestScore) {
        bestScore = score;
        bestMatch = word;
    }
}

if (bestScore > 0.8) {
    System.out.println("Did you mean: " + bestMatch);
}
```

### 5. URL 生成 - Slugify

```java
String articleTitle = "Java 编程入门教程";
String slug = StringUtils.slugify(articleTitle);
String url = "https://example.com/articles/" + slug;
// https://example.com/articles/java-bian-cheng-ru-men-jiao-cheng
```

### 6. 数据脱敏 - Base64 编码

```java
String sensitiveData = "password123";
String encoded = StringUtils.base64Encode(sensitiveData);
// 存储或传输 encoded
String decoded = StringUtils.base64Decode(encoded);
```

---

## 🧪 测试

运行测试套件：

```bash
cd AllToolkit/Java/string_utils
javac *.java
java string_utils.StringUtilsTest
```

运行示例：

```bash
cd AllToolkit/Java/string_utils/examples
javac -cp .. StringUtilsExamples.java
java -cp ..:./ string_utils.examples.StringUtilsExamples
```

---

## 📝 注意事项

1. **空值处理**：所有方法都安全处理 `null` 输入，返回 `null` 或空集合
2. **性能**：使用 `StringBuilder` 和缓存优化性能
3. **线程安全**：所有方法都是线程安全的（无状态）
4. **中文支持**：完整支持中文字符的处理和分析
5. **SQL 注入**：`escapeSql` 提供基本保护，但推荐使用预编译语句

---

## 📄 许可证

MIT License - 自由使用、修改和分发

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**AllToolkit** - 一站式工具集合，让开发更简单 🚀
