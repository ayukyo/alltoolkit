# Case Utils


Case Utils - 命名风格转换工具

支持多种命名风格之间的相互转换：
- camelCase (小驼峰)
- PascalCase (大驼峰)
- snake_case (蛇形)
- SCREAMING_SNAKE_CASE (尖叫蛇形)
- kebab-case (短横线)
- Title Case (标题格式)
- sentence case (句子格式)
- dot.case (点分隔)

零外部依赖，纯Python实现。


## 功能

### 类

- **CaseUtils**: 命名风格转换工具类
  方法: split_words, to_camel_case, to_pascal_case, to_snake_case, to_screaming_snake_case ... (18 个方法)

### 函数

- **to_camel_case(text**) - 转换为 camelCase
- **to_pascal_case(text**) - 转换为 PascalCase
- **to_snake_case(text**) - 转换为 snake_case
- **to_kebab_case(text**) - 转换为 kebab-case
- **detect_case(text**) - 检测命名风格
- **convert_case(text, target_case**) - 转换为指定命名风格
- **split_words(text**) - 将任意格式的字符串拆分为单词列表
- **to_camel_case(text**) - 转换为 camelCase (小驼峰)
- **to_pascal_case(text**) - 转换为 PascalCase (大驼峰/帕斯卡命名)
- **to_snake_case(text**) - 转换为 snake_case (蛇形命名)

... 共 24 个函数

## 使用示例

```python
from mod import to_camel_case

# 使用 to_camel_case
result = to_camel_case()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
