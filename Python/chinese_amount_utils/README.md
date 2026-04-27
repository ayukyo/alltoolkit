# Chinese Amount Utils


AllToolkit - Chinese Amount Utilities (中文金额大写转换工具)

零依赖的中文金额转换模块，支持：
- 数字金额转中文大写金额（财务标准格式）
- 支持整数和小数金额
- 支持负数金额
- 支持大额金额（亿级以上）
- 提供多种输出格式选项
- 符合中国财务标准

Author: AllToolkit
License: MIT


## 功能

### 类

- **ChineseAmountError**: 中文金额转换异常

### 函数

- **to_chinese_amount(amount**) - 将数字金额转换为中文大写金额。
- **to_chinese_amount_simple(amount**) - 将数字转换为简化的中文大写（不含货币单位）。
- **to_chinese_number(num**) - 将整数转换为中文数字（普通写法）。
- **parse_chinese_amount(chinese_str**) - 将中文大写金额转换为数字金额。
- **format_amount_for_receipt(amount**) - 格式化金额用于收据/发票（标准财务格式）。
- **validate_chinese_amount(chinese_str**) - 验证中文大写金额格式是否正确。
- **amount_in_words(amount**) - 将金额转换为文字描述（多种风格）。
- **rmb(amount**) - 快捷函数：转换为人民币大写金额。
- **cny(amount**) - 快捷函数：转换为人民币大写金额（同 rmb）。
- **parse_section(section**) - 解析中文数字段

## 使用示例

```python
from mod import to_chinese_amount

# 使用 to_chinese_amount
result = to_chinese_amount()
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
