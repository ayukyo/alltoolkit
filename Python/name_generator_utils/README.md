# name_generator_utils - 名字生成工具

[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](./name_generator_utils_test.py)

零依赖的名字生成工具，支持多种风格和文化背景。

## 特性

- **多种风格**: 现代、古典、奇幻、科幻
- **文化背景**: 中文、英文、日式、欧式等
- **性别支持**: 男名、女名、中性名
- **姓氏生成**: 各文化姓氏库
- **组合生成**: 自动组合姓+名
- **随机化**: 可控的随机参数
- **零依赖**: 纯 Python 实现

## 安装

```python
from name_generator_utils import (
    generate_name,
    generate_first_name,
    generate_last_name,
    generate_chinese_name,
    generate_english_name
)
```

## 快速开始

### 英文名字

```python
from name_generator_utils import generate_english_name

# 生成完整英文名
name = generate_english_name()
print(name)  # "James Wilson"

# 指定性别
male_name = generate_english_name(gender="male")
female_name = generate_english_name(gender="female")

# 只生成名或姓
first = generate_first_name("english", gender="male")
last = generate_last_name("english")
```

### 中文名字

```python
from name_generator_utils import generate_chinese_name

# 生成中文姓名
name = generate_chinese_name()
print(name)  # "张伟"

# 指定性别
male_name = generate_chinese_name(gender="male")
female_name = generate_chinese_name(gender="female")
```

### 通用生成器

```python
from name_generator_utils import generate_name

# 指定文化和风格
name = generate_name(culture="japanese", style="traditional")
name = generate_name(culture="fantasy", style="elven")
name = generate_name(culture="scifi", style="cyberpunk")
```

## API 参考

### 主要函数

| 函数 | 说明 |
|-----|------|
| `generate_name(culture, style, gender)` | 通用名字生成 |
| `generate_first_name(culture, gender)` | 生成名 |
| `generate_last_name(culture)` | 生成姓 |
| `generate_chinese_name(gender)` | 中文姓名 |
| `generate_english_name(gender)` | 英文姓名 |
| `generate_full_name(culture, style, gender)` | 完整姓名 |

### 参数说明

- `culture`: 文化背景（"chinese", "english", "japanese", "fantasy", "scifi"）
- `style`: 名字风格（"modern", "traditional", "fantasy", "cyberpunk"）
- `gender`: 性别（"male", "female", "neutral"）

## 测试

```bash
python -m pytest name_generator_utils_test.py -v
```

## 许可证

MIT License