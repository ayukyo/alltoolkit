# DiffUtils - Java 文本差异比较工具

[English](#english) | [中文](#中文)

---

## 中文

### 概述

DiffUtils 是一个零外部依赖的 Java 文本差异比较工具库，实现了经典的 Myers 差异算法和 LCS（最长公共子序列）算法，支持多种比较模式。

### 核心功能

| 功能 | 方法 | 说明 |
|------|------|------|
| 文本比较 | `diff(String, String)` | 按行比较两个文本 |
| 字符比较 | `diff(String, String, false)` | 按字符比较两个文本 |
| 数组比较 | `diffArrays(T[], T[])` | 比较两个泛型数组 |
| 编辑距离 | `levenshteinDistance(String, String)` | 计算 Levenshtein 编辑距离 |
| 相似度 | `similarity(String, String)` | 计算文本相似度 (0.0-1.0) |
| 最长公共子串 | `longestCommonSubstring(String, String)` | 查找最长公共子串 |
| 最长公共子序列 | `longestCommonSubsequence(String, String)` | 查找最长公共子序列 |
| 统一格式输出 | `toUnifiedDiff(...)` | 生成 unified diff 格式 |
| 应用差异 | `applyPatch(String, DiffResult)` | 应用差异到原文本 |

### 快速开始

```java
import diff_utils.DiffUtils;
import diff_utils.DiffUtils.DiffResult;
import diff_utils.DiffUtils.DiffItem;
import diff_utils.DiffUtils.DiffType;

public class Example {
    public static void main(String[] args) {
        String oldText = "Hello\nWorld\nJava";
        String newText = "Hello\nJava\nWorld";
        
        // 比较文本
        DiffResult result = DiffUtils.diff(oldText, newText);
        
        // 输出差异
        for (DiffItem item : result.items) {
            System.out.println(item);
        }
        
        // 输出统计
        System.out.println(DiffUtils.getSummary(result));
        // 输出: 变更统计: +1 -1 (相似度: 66.7%)
    }
}
```

### 使用示例

#### 1. 基本文本比较

```java
String oldText = "Line 1\nLine 2\nLine 3";
String newText = "Line 1\nLine 2 modified\nLine 3";

DiffResult result = DiffUtils.diff(oldText, newText);

// 检查是否有变化
if (result.hasChanges()) {
    System.out.println("检测到变化！");
    System.out.println("插入: " + result.insertions);
    System.out.println("删除: " + result.deletions);
    System.out.println("相似度: " + (result.getSimilarity() * 100) + "%");
}
```

#### 2. 字符级别比较

```java
String s1 = "kitten";
String s2 = "sitting";

// 按字符比较
DiffResult result = DiffUtils.diff(s1, s2, false);

for (DiffItem item : result.items) {
    switch (item.type) {
        case INSERT:
            System.out.println("插入: " + item.content);
            break;
        case DELETE:
            System.out.println("删除: " + item.content);
            break;
        case EQUAL:
            System.out.println("相同: " + item.content);
            break;
    }
}
```

#### 3. 数组比较

```java
String[] oldArr = {"apple", "banana", "cherry", "date"};
String[] newArr = {"apple", "blueberry", "cherry", "elderberry"};

DiffResult result = DiffUtils.diffArrays(oldArr, newArr);

// 遍历差异项
for (DiffItem item : result.items) {
    System.out.println(item);  // 使用内置的 toString()
}
```

#### 4. 编辑距离和相似度

```java
String s1 = "kitten";
String s2 = "sitting";

// 计算 Levenshtein 编辑距离
int distance = DiffUtils.levenshteinDistance(s1, s2);
System.out.println("编辑距离: " + distance);  // 输出: 3

// 计算相似度
double sim = DiffUtils.similarity(s1, s2);
System.out.println("相似度: " + sim);  // 输出: 0.5714...
```

#### 5. 最长公共子序列/子串

```java
String s1 = "ABCBDAB";
String s2 = "BDCABA";

// 最长公共子串（连续）
String lcsStr = DiffUtils.longestCommonSubstring(s1, s2);
System.out.println("最长公共子串: " + lcsStr);  // 输出: "AB" 或 "BD" 等

// 最长公共子序列（可非连续）
String lcsSeq = DiffUtils.longestCommonSubsequence(s1, s2);
System.out.println("最长公共子序列: " + lcsSeq);  // 输出: "BCBA" 或 "BDAB" 等
```

#### 6. 生成 Unified Diff

```java
String oldText = "Line 1\nLine 2\nLine 3";
String newText = "Line 1\nLine 2 modified\nLine 3";

String unifiedDiff = DiffUtils.toUnifiedDiff(
    oldText, newText, 
    "original.txt", "modified.txt", 
    3  // 上下文行数
);

System.out.println(unifiedDiff);
// 输出:
// --- original.txt
// +++ modified.txt
// @@ -1,3 +1,3 @@
//  Line 1
// -Line 2
// +Line 2 modified
//  Line 3
```

#### 7. 彩色终端输出

```java
DiffResult result = DiffUtils.diff(oldText, newText);
String colored = DiffUtils.toColoredString(result);
System.out.println(colored);
// 删除的行显示为红色，插入的行显示为绿色
```

#### 8. 应用差异 (Patch)

```java
String original = "Hello\nWorld";
String modified = "Hello\nJava";

// 获取差异
DiffResult diff = DiffUtils.diff(original, modified);

// 应用差异到原始文本
String patched = DiffUtils.applyPatch(original, diff);
System.out.println(patched);  // 输出: Hello\nJava
```

#### 9. 快速比较

```java
// 当只需要知道是否相同时，使用快速比较
if (DiffUtils.quickCompare(text1, text2)) {
    System.out.println("文本相同");
}

// 处理 null 值
if (DiffUtils.isIdentical(text1, text2)) {
    System.out.println("文本相同（包括 null 情况）");
}
```

#### 10. 查找差异位置

```java
String s1 = "Hello World";
String s2 = "Hello Java";

List<int[]> ranges = DiffUtils.findDiffRanges(s1, s2);
for (int[] range : ranges) {
    System.out.println("差异范围: [" + range[0] + ", " + range[1] + ")");
}
```

### DiffResult 结构

```java
DiffResult result = DiffUtils.diff(oldText, newText);

// 差异项列表
List<DiffItem> items = result.items;

// 统计信息
int insertions = result.insertions;  // 插入数量
int deletions = result.deletions;    // 删除数量
int unchanged = result.unchanged;    // 未变数量

// 计算属性
double similarity = result.getSimilarity();  // 相似度 0.0-1.0
double changeRate = result.getChangeRate();  // 变化率 0.0-1.0
boolean hasChanges = result.hasChanges();   // 是否有变化
```

### DiffItem 结构

```java
DiffItem item = result.items.get(0);

DiffType type = item.type;    // EQUAL, INSERT, DELETE
String content = item.content; // 内容

// toString() 输出格式化的差异行
System.out.println(item);  // " content", "+content", "-content"
```

### 编译和运行

```bash
# 编译
javac diff_utils/DiffUtils.java

# 编译测试 (需要 JUnit)
javac -cp .:junit-4.13.2.jar:hamcrest-core-1.3.jar diff_utils/DiffUtilsTest.java

# 运行测试
java -cp .:junit-4.13.2.jar:hamcrest-core-1.3.jar org.junit.runner.JUnitCore diff_utils.DiffUtilsTest
```

### 算法说明

1. **LCS 差异算法**: 基于最长公共子序列，时间复杂度 O(m×n)
2. **Myers 差异算法**: 用于生成更紧凑的差异输出
3. **编辑距离**: 使用动态规划计算 Levenshtein 距离，优化空间复杂度到 O(n)

### 特性

- ✅ 零外部依赖
- ✅ 支持行级别和字符级别比较
- ✅ 支持 Unicode 文本
- ✅ 支持 null 值处理
- ✅ 提供完整统计信息
- ✅ 支持 unified diff 格式输出
- ✅ 支持彩色终端输出

---

## English

### Overview

DiffUtils is a zero-dependency Java library for text diffing, implementing the classic Myers diff algorithm and LCS (Longest Common Subsequence) algorithm with multiple comparison modes.

### Core Features

| Feature | Method | Description |
|---------|--------|-------------|
| Text Diff | `diff(String, String)` | Compare two texts by line |
| Character Diff | `diff(String, String, false)` | Compare two texts by character |
| Array Diff | `diffArrays(T[], T[])` | Compare two generic arrays |
| Edit Distance | `levenshteinDistance(String, String)` | Calculate Levenshtein distance |
| Similarity | `similarity(String, String)` | Calculate text similarity (0.0-1.0) |
| LCS | `longestCommonSubstring(...)` | Find longest common substring |
| LCS | `longestCommonSubsequence(...)` | Find longest common subsequence |
| Unified Diff | `toUnifiedDiff(...)` | Generate unified diff format |
| Apply Patch | `applyPatch(String, DiffResult)` | Apply diff to original text |

### Quick Start

```java
import diff_utils.DiffUtils;
import diff_utils.DiffUtils.DiffResult;

public class Example {
    public static void main(String[] args) {
        String oldText = "Hello\nWorld\nJava";
        String newText = "Hello\nJava\nWorld";
        
        DiffResult result = DiffUtils.diff(oldText, newText);
        
        for (var item : result.items) {
            System.out.println(item);
        }
        
        System.out.println(DiffUtils.getSummary(result));
    }
}
```

### License

MIT License - Part of AllToolkit Project