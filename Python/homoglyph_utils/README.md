# Homoglyph Utils - Unicode 同形字检测工具

Unicode 同形字（Homoglyph）检测、转换和分析工具模块。零外部依赖，仅使用 Python 标准库。

## 功能特性

- ✅ 同形字检测（西里尔、希腊、全角等混淆字符）
- ✅ 字符正规化（统一到标准形式）
- ✅ 同形字攻击风险评估
- ✅ 字符串相似度分析（视觉相似性）
- ✅ 同形字映射查询
- ✅ 批量文本扫描
- ✅ 域名安全检查
- ✅ 不可见字符检测与移除
- ✅ 混合脚本检测

## 应用场景

- **IDN 同形字攻击检测**: 检测钓鱼域名如 `pаypal.com`（使用西里尔字母 'а'）
- **用户名安全验证**: 防止用户使用混淆字符冒充他人
- **密码安全检查**: 确保密码不包含可能导致输入问题的混淆字符
- **文本欺诈检测**: 检测文档中的隐藏字符或混淆字符
- **域名安全分析**: 批量扫描域名库中的可疑域名

## 安装使用

```python
from homoglyph_utils.mod import (
    detect_homoglyphs,
    normalize_homoglyphs,
    scan_text,
    check_domain_safety,
)

# 基础检测
text = "pаypal.com"  # 包含西里尔字母 'а'
matches = detect_homoglyphs(text)

# 规范化
normalized = normalize_homoglyphs(text)  # "paypal.com"

# 域名安全检查
result = check_domain_safety("pаypal.com")
print(result.has_homoglyphs)  # True
print(result.normalized)       # "paypal.com"
print(result.risk_level)       # "高风险"
```

## API 参考

### 核心函数

#### `detect_homoglyphs(text, categories=None, include_invisible=True)`
检测文本中的同形字，返回匹配列表。

```python
matches = detect_homoglyphs("pаypal.com")
for match in matches:
    print(f"位置 {match.position}: '{match.original_char}' -> '{match.canonical_char}'")
```

#### `normalize_homoglyphs(text, categories=None)`
将同形字转换为规范形式。

```python
normalize_homoglyphs("Ｈｅｌｌｏ")  # "Hello"
normalize_homoglyphs("pаypal.com") # "paypal.com"
```

#### `scan_text(text, categories=None, include_invisible=True)`
扫描文本并返回详细结果对象。

```python
result = scan_text("pаypal.com")
print(result.has_homoglyphs)    # True
print(result.match_count)       # 1
print(result.normalized)        # "paypal.com"
print(result.risk_score)        # 80
print(result.risk_level)        # "高风险"
```

### 专项检测

#### `check_domain_safety(domain)`
检查域名安全性，重点关注 IDN 同形字攻击。

```python
result = check_domain_safety("pаypal.com")
if result.has_homoglyphs:
    print(f"可疑域名: {domain}")
    print(f"规范形式: {result.normalized}")
```

#### `detect_invisible_chars(text)`
检测不可见字符（零宽空格、零宽连接符等）。

```python
text = "hello\u200bworld"  # 包含零宽空格
matches = detect_invisible_chars(text)
```

#### `remove_invisible_chars(text)`
移除不可见字符。

```python
cleaned = remove_invisible_chars("hello\u200bworld")  # "helloworld"
```

#### `check_zero_o_confusion(text)`
专门检测数字 0 和字母 O 的混淆。

```python
matches = check_zero_o_confusion("PASS０123OООO")
```

#### `check_l_one_confusion(text)`
专门检测字母 l、数字 1、字母 I 的混淆。

```python
matches = check_l_one_confusion("Il1Il1")
```

#### `is_mixed_script(text, scripts=None)`
检测文本是否混合了多种书写系统。

```python
is_mixed_script("pаypal")   # True (Latin + Cyrillic)
is_mixed_script("paypal")   # False
```

### 批量处理

#### `batch_scan(texts, categories=None)`
批量扫描多个文本。

```python
domains = ["google.com", "gоogle.com", "аpple.com"]
results = batch_scan(domains)
for result in results:
    if result.has_homoglyphs:
        print(f"可疑: {result.text}")
```

### 工具函数

#### `get_char_info(char)`
获取字符的详细信息。

```python
info = get_char_info('\u0430')
print(info['is_homoglyph'])   # True
print(info['canonical_char']) # 'a'
print(info['name'])           # CYRILLIC SMALL LETTER A
```

#### `suggest_replacement(text)`
建议字符替换方案。

```python
suggestions = suggest_replacement("pаypal")
# [(1, 'а', 'a')]
```

## 同形字类别

| 类别 | 描述 | 示例 |
|------|------|------|
| LATIN_CYRILLIC | 西里尔字母混淆拉丁字母 | `а` → `a`, `о` → `o` |
| LATIN_GREEK | 希腊字母混淆拉丁字母 | `α` → `a`, `ε` → `e` |
| FULLWIDTH | 全角字符混淆半角字符 | `Ａ` → `A`, `０` → `0` |
| LOOKALIKE | 其他视觉相似字符 | 零宽空格、各种空格字符 |

## 真实攻击示例

以下是一些常见的同形字攻击示例：

| 假域名 | 规范形式 | 使用的混淆字符 |
|--------|----------|----------------|
| pаypal.com | paypal.com | 西里尔字母 `а` |
| gоogle.com | google.com | 西里尔字母 `о` |
| аpple.com | apple.com | 西里尔字母 `а` |
| mіcrosoft.com | microsoft.com | 西里尔字母 `і` |
| netflіx.com | netflix.com | 西里尔字母 `і` |

## 风险等级

风险分数范围 0-100，对应以下等级：

- **无风险** (0): 文本不包含同形字
- **低风险** (1-19): 可能是误用或无害的全角字符
- **中低风险** (20-39): 存在少量混淆字符
- **中风险** (40-59): 混淆字符较多或为中等危险类型
- **中高风险** (60-79): 高危险类型混淆字符（如西里尔字母）
- **高风险** (80-100): 多个高危险类型混淆字符，极可能是攻击

## 测试

运行测试文件：

```bash
python homoglyph_utils_test.py
```

测试覆盖：
- 基础同形字检测
- 规范化功能
- 扫描结果分析
- 域名安全检测
- 不可见字符检测
- 0/O 混淆检测
- l/1/I 混淆检测
- 混合脚本检测
- 批量扫描
- 风险等级计算
- 真实世界攻击示例

## 注意事项

1. 此工具主要针对拉丁字母系统的同形字，CJK（中日韩）字符不在检测范围
2. 零宽字符和特殊空格字符在默认情况下会被检测
3. 建议对高风险域名进行人工复核后再采取行动

## 许可证

MIT License

## 作者

AllToolkit
日期: 2026-05-21