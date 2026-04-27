# Nanoid Utils


nanoid_utils - 轻量级唯一ID生成工具

NanoID 是一个小巧、安全、URL友好的唯一字符串ID生成器。
- 默认长度21字符
- 使用加密安全的随机数生成器
- URL安全字符集: A-Za-z0-9_-
- 零外部依赖，纯Python实现

特性:
- generate(): 生成标准NanoID
- generate_custom(): 自定义长度和字符集
- generate_number(): 纯数字ID
- generate_lowercase(): 小写字母+数字ID
- generate_alphabet(): 纯字母ID
- validate(): 验证ID格式
- batch(): 批量生成ID


## 功能

### 函数

- **generate(size**) - 生成标准NanoID
- **generate_custom(size, alphabet**) - 使用自定义字符集生成ID
- **generate_number(size**) - 生成纯数字ID
- **generate_lowercase(size**) - 生成小写字母+数字ID
- **generate_alphabet(size**) - 生成纯字母ID (大小写混合)
- **generate_no_lookalikes(size**) - 生成无易混淆字符的ID
- **batch(count, size**) - 批量生成NanoID
- **validate(nanoid, size, alphabet**) - 验证NanoID格式
- **is_unique(nanoid, existing_ids**) - 检查ID在现有集合中是否唯一
- **generate_unique(size, existing_ids, max_attempts**) - 生成确保唯一的NanoID (在给定集合中不重复)

... 共 11 个函数

## 使用示例

```python
from mod import generate

# 使用 generate
result = generate()
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
