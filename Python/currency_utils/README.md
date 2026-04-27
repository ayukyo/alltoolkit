# Currency Utils


Currency Utils - 货币工具库

零依赖的货币处理库，支持：
- ISO 4217 货币代码验证与查询
- 货币格式化（符号、小数位、千位分隔符）
- 精确货币计算（避免浮点误差）
- 多语言本地化支持
- 汇率转换辅助
- 币种信息查询

Author: AllToolkit
License: MIT


## 功能

### 类

- **CurrencyError**: 货币错误基类
- **InvalidCurrencyError**: 无效货币代码错误
- **InvalidAmountError**: 无效金额错误
- **UnsupportedLocaleError**: 不支持的本地化错误
- **Money**: 货币金额类，支持精确计算

使用 Decimal 避免浮点精度问题
  方法: amount, decimals, symbol, name, numeric_code ... (7 个方法)
- **ExchangeRates**: 汇率管理类

存储和管理汇率数据，支持货币转换
  方法: set_rate, set_rates, get_rate, convert, get_supported_currencies

### 函数

- **is_valid_currency(code**) - 验证货币代码是否有效
- **is_valid_numeric_code(code**) - 验证数字代码是否有效
- **get_currency_info(code**) - 获取货币信息
- **get_currencies_by_symbol(symbol**) - 根据符号获取货币代码列表
- **get_all_currencies(**) - 获取所有货币代码
- **get_major_currencies(**) - 获取主要货币代码
- **format_money(amount, currency, locale**, ...) - 格式化货币金额
- **parse_money(money_str, currency, locale**) - 解析货币字符串
- **format_number(number, decimals, locale**) - 格式化数字
- **convert_money(amount, from_currency, to_currency**, ...) - 简单货币转换

... 共 38 个函数

## 使用示例

```python
from mod import is_valid_currency

# 使用 is_valid_currency
result = is_valid_currency()
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
