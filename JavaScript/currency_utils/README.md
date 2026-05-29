# Currency Utils - 货币工具库

零依赖的 JavaScript 货币处理工具库，支持格式化、转换、精确计算等功能。

## 功能特性

- ✅ **货币格式化** - 支持国际化格式，自定义符号、分隔符
- ✅ **简写格式** - K/M/B/T 简写形式
- ✅ **中文大写金额** - 支持转换为财务用的中文大写
- ✅ **精确计算** - 避免浮点数误差
- ✅ **货币转换** - 基于汇率的货币转换
- ✅ **税费计算** - 支持含税/不含税计算
- ✅ **利息计算** - 简单利息和复利
- ✅ **金额分摊** - 公平分摊金额

## 安装

```javascript
const currency = require('./currency_utils/mod.js');
```

## 快速开始

### 格式化

```javascript
const { format } = require('./mod.js');

// 基本格式化
format(1234.56, { currency: 'USD' });  // '$1,234.56'
format(1234.56, { currency: 'CNY' });  // '¥1,234.56'
format(1234.56, { currency: 'EUR' });  // '€1,234.56'

// 日元无小数
format(12345, { currency: 'JPY' });  // '¥12,345'

// 不显示符号
format(1234.56, { showSymbol: false });  // '1,234.56'

// 显示货币代码
format(1234.56, { currency: 'CNY', showCode: true });  // '¥1,234.56 CNY'
```

### 简写格式

```javascript
const { formatCompact } = require('./mod.js');

formatCompact(1500, { currency: 'USD' });        // '$1.5K'
formatCompact(1500000, { currency: 'USD' });     // '$1.5M'
formatCompact(1500000000, { currency: 'USD' });  // '$1.5B'
```

### 中文大写金额

```javascript
const { formatChinese } = require('./mod.js');

formatChinese(100);      // '壹佰元整'
formatChinese(123.45);   // '壹佰贰拾叁元肆角伍分'
formatChinese(-100);     // '负壹佰元整'
```

### 解析

```javascript
const { parse } = require('./mod.js');

parse('$1,234.56');    // 1234.56
parse('¥100.50');      // 100.5
parse('(500)');        // -500 (括号表示负数)
parse('1.234,56');     // 1234.56 (欧洲格式)
```

### 货币转换

```javascript
const { convert, convertAndFormat, setRates } = require('./mod.js');

// 使用默认汇率转换
convert(100, 'USD', 'CNY');  // 724.00 (基于默认汇率)

// 转换并格式化
convertAndFormat(100, 'USD', 'EUR');  // '€92.00'

// 设置自定义汇率
setRates({ CNY: 7.20, EUR: 0.90 });
convert(100, 'USD', 'CNY');  // 720.00
```

### 精确计算

```javascript
const { preciseAdd, preciseSubtract, preciseMultiply, preciseDivide } = require('./mod.js');

// 避免 JavaScript 浮点数误差
preciseAdd(0.1, 0.2);      // 0.3 (不是 0.30000000000000004)
preciseSubtract(0.3, 0.1);  // 0.2 (不是 0.19999999999999998)
preciseMultiply(0.1, 0.2);  // 0.02
preciseDivide(0.3, 3);      // 0.1
```

### 百分比和折扣

```javascript
const { calculatePercent, calculateDiscount } = require('./mod.js');

// 计算百分比
calculatePercent(100, 10);  // 10 (100的10%)

// 计算折扣
const { discounted, saved } = calculateDiscount(200, 25);
// discounted: 150, saved: 50
```

### 税费计算

```javascript
const { calculateTax } = require('./mod.js');

// 不含税 -> 含税
const result1 = calculateTax(100, 10, false);
// { subtotal: 100, tax: 10, total: 110 }

// 含税 -> 不含税
const result2 = calculateTax(110, 10, true);
// { subtotal: 100, tax: 10, total: 110 }
```

### 金额分摊

```javascript
const { split } = require('./mod.js');

// 100元分给3人
split(100, 3);  // [33.34, 33.33, 33.33] (总和为100)
```

### 利息计算

```javascript
const { simpleInterest, compoundInterest } = require('./mod.js');

// 简单利息
simpleInterest(10000, 5, 3);  // { interest: 1500, total: 11500 }

// 复利 (月复利)
compoundInterest(10000, 5, 3, 12);  // { interest: 1614.72, total: 11614.72 }
```

## 支持的货币

| 代码 | 名称 | 符号 |
|------|------|------|
| CNY | Chinese Yuan | ¥ |
| USD | US Dollar | $ |
| EUR | Euro | € |
| GBP | British Pound | £ |
| JPY | Japanese Yen | ¥ |
| KRW | South Korean Won | ₩ |
| HKD | Hong Kong Dollar | HK$ |
| TWD | New Taiwan Dollar | NT$ |
| SGD | Singapore Dollar | S$ |
| AUD | Australian Dollar | A$ |
| CAD | Canadian Dollar | C$ |
| CHF | Swiss Franc | Fr |
| INR | Indian Rupee | ₹ |
| RUB | Russian Ruble | ₽ |
| BRL | Brazilian Real | R$ |
| THB | Thai Baht | ฿ |
| VND | Vietnamese Dong | ₫ |
| PHP | Philippine Peso | ₱ |
| MYR | Malaysian Ringgit | RM |
| IDR | Indonesian Rupiah | Rp |

## API 文档

### 格式化

- `format(amount, options)` - 格式化货币金额
- `formatCompact(amount, options)` - 格式化为简写形式
- `formatChinese(amount)` - 格式化为中文大写金额

### 解析

- `parse(currencyString, options)` - 解析货币字符串为数字
- `extractCurrencyCode(str)` - 从字符串中提取货币代码

### 转换

- `convert(amount, from, to, decimals)` - 货币转换
- `convertAndFormat(amount, from, to, formatOptions)` - 转换并格式化
- `setRates(rates, baseCurrency)` - 设置汇率
- `getRates()` - 获取当前汇率

### 计算

- `preciseAdd(a, b, decimals)` - 精确加法
- `preciseSubtract(a, b, decimals)` - 精确减法
- `preciseMultiply(a, b, decimals)` - 精确乘法
- `preciseDivide(a, b, decimals)` - 精确除法
- `calculatePercent(amount, percent, decimals)` - 计算百分比
- `calculateDiscount(amount, discountPercent, decimals)` - 计算折扣
- `calculateTax(amount, taxRate, inclusive, decimals)` - 计算税费
- `split(amount, parts, decimals)` - 分摊金额
- `simpleInterest(principal, rate, years)` - 简单利息
- `compoundInterest(principal, rate, years, compoundsPerYear)` - 复利

### 信息

- `getCurrencyInfo(code)` - 获取货币信息
- `getSupportedCurrencies()` - 获取支持的货币列表
- `getSymbol(code)` - 获取货币符号
- `isSupported(code)` - 检查货币是否支持

## 运行测试

```bash
node test.js
```

## 运行示例

```bash
node examples.js
```

## 注意事项

1. **汇率** - 默认汇率仅供参考，实际使用时应从可靠的汇率 API 获取实时数据
2. **精度** - 内部使用整数运算避免浮点误差，但复杂运算仍需注意精度问题
3. **货币支持** - 目前支持 20 种常用货币，可根据需要扩展

## License

MIT