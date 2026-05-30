# MoneyUtils - 金额工具库

零依赖的 Java 金额计算工具库，支持精确计算、多货币、格式化、转换等功能。

## 功能特性

- ✅ **精确计算** - 使用 BigDecimal 避免浮点误差
- ✅ **多货币支持** - 支持 20+ 种常用货币
- ✅ **金额格式化** - 国际化格式、简写、中文大写
- ✅ **货币转换** - 内置汇率转换器
- ✅ **百分比运算** - 折扣、含税、不含税计算
- ✅ **金额分摊** - 平均分摊、按比例分摊
- ✅ **利息计算** - 简单利息、复利
- ✅ **税费计算** - 含税/不含税价格互算
- ✅ **零外部依赖** - 纯 Java 标准库实现

## 快速开始

### 创建金额

```java
// 多种创建方式
Money m1 = Money.of("100.50", "CNY");   // 从字符串
Money m2 = Money.of(100, "USD");         // 从整数
Money m3 = Money.of(100.5, "EUR");       // 从 double
Money m4 = Money.fromSmallestUnit(10050, "CNY");  // 从分转元

// 快捷方法
Money cny = MoneyUtils.cny(1000);
Money usd = MoneyUtils.usd(100);
Money eur = MoneyUtils.eur(100);
Money jpy = MoneyUtils.jpy(100);
```

### 算术运算

```java
Money price = Money.of("100.00", "CNY");

Money total = price.add(Money.of("50.00", "CNY"));   // 加法
Money diff = price.subtract(Money.of("30.00", "CNY")); // 减法
Money doubled = price.multiply(2);                    // 乘法
Money divided = price.divide(4);                      // 除法
Money negated = price.negate();                       // 取负
Money absolute = negated.abs();                       // 绝对值
```

### 格式化

```java
Money m = Money.of("1234.56", "USD");

String formatted = m.format();              // 默认格式
String usFormat = m.format(Locale.US);      // 美国格式
String compact = m.formatCompact();         // 简写: 1.2K
String chinese = m.formatChinese();         // 中文大写金额
String withSymbol = MoneyUtils.formatWithSymbol(m);  // $1,234.56
```

### 百分比和折扣

```java
Money price = Money.of("200.00", "CNY");

Money percent = price.percent(10);      // 10% = ¥20
Money discounted = price.discount(20);   // 20%折扣 = ¥160
Money withTax = price.withTax(10);       // 含10%税 = ¥220
Money withoutTax = withTax.withoutTax(10); // 去10%税 = ¥200
```

### 金额分摊

```java
Money total = Money.of("100.00", "CNY");

// 平均分摊
Money[] split = MoneyUtils.split(total, 3);
// [¥33.34, ¥33.33, ¥33.33]

// 按比例分摊
Money[] byRatio = MoneyUtils.splitByRatio(total, 1, 2, 3);
// [¥16.67, ¥33.33, ¥50.00]
```

### 货币转换

```java
DefaultCurrencyConverter converter = new DefaultCurrencyConverter();

Money usd = Money.of("100.00", "USD");
Money cny = converter.convert(usd, "CNY");
// ≈ ¥724

// 自定义汇率
CurrencyConverter custom = new CurrencyConverter("CNY");
custom.setRate("USD", 0.138);
```

### 税费计算

```java
Money price = Money.of("100.00", "CNY");

// 不含税价格，计算含税
Money[] result = MoneyUtils.calculateTax(price, 13, false);
// [税前¥100, 税额¥13, 税后¥113]

// 含税价格，反算税前
Money[] result2 = MoneyUtils.calculateTax(Money.of("113", "CNY"), 13, true);
// [税前¥100, 税额¥13, 税后¥113]
```

### 利息计算

```java
Money principal = Money.of("10000.00", "CNY");

// 简单利息
Money interest = MoneyUtils.simpleInterest(principal, 5, 3);
// ¥1500

// 复利（月复利）
Money compound = MoneyUtils.compoundInterest(principal, 5, 3, 12);
// ≈ ¥11614.72
```

## 支持的货币

| 货币代码 | 名称 | 符号 | 小数位数 |
|---------|------|------|---------|
| CNY | 人民币 | ¥ | 2 |
| USD | 美元 | $ | 2 |
| EUR | 欧元 | € | 2 |
| GBP | 英镑 | £ | 2 |
| JPY | 日元 | ¥ | 0 |
| KRW | 韩元 | ₩ | 0 |
| HKD | 港币 | HK$ | 2 |
| TWD | 台币 | NT$ | 2 |
| SGD | 新加坡元 | S$ | 2 |
| AUD | 澳元 | A$ | 2 |
| CAD | 加元 | C$ | 2 |
| CHF | 瑞士法郎 | Fr | 2 |
| INR | 卢比 | ₹ | 2 |
| RUB | 卢布 | ₽ | 2 |
| BRL | 巴西雷亚尔 | R$ | 2 |
| THB | 泰铢 | ฿ | 2 |
| VND | 越南盾 | ₫ | 0 |
| PHP | 比索 | ₱ | 2 |
| MYR | 马币 | RM | 2 |
| IDR | 印尼盾 | Rp | 0 |

## API 参考

### Money 类

| 方法 | 描述 |
|-----|------|
| `of(String, String)` | 从字符串创建 |
| `of(int, String)` | 从整数创建 |
| `of(double, String)` | 从 double 创建 |
| `of(long, String)` | 从 long 创建 |
| `fromSmallestUnit(long, String)` | 从最小单位创建 |
| `zero(String)` | 创建零金额 |
| `add(Money)` | 加法 |
| `subtract(Money)` | 减法 |
| `multiply(BigDecimal/int/double)` | 乘法 |
| `divide(BigDecimal/int/double)` | 除法 |
| `negate()` | 取负 |
| `abs()` | 绝对值 |
| `percent(BigDecimal/double)` | 计算百分比 |
| `discount(double)` | 应用折扣 |
| `withTax(double)` | 含税金额 |
| `withoutTax(double)` | 不含税金额 |
| `format()` | 默认格式化 |
| `format(Locale)` | 指定地区格式化 |
| `formatCompact()` | 简写格式 |
| `formatChinese()` | 中文大写金额 |
| `isZero/Positive/Negative()` | 状态检查 |
| `greaterThan/LessThan/equals(Money)` | 比较运算 |

### MoneyUtils 工具类

| 方法 | 描述 |
|-----|------|
| `money(...)` | 创建金额 |
| `cny/usd/eur/jpy(...)` | 快捷创建 |
| `parse(String, String)` | 解析金额字符串 |
| `sum(Money...)` | 求和 |
| `average(Money...)` | 平均值 |
| `max/min(Money, Money)` | 最大最小值 |
| `split(Money, int)` | 平均分摊 |
| `splitByRatio(Money, int...)` | 按比例分摊 |
| `simpleInterest(...)` | 简单利息 |
| `compoundInterest(...)` | 复利 |
| `calculateTax(...)` | 税费计算 |
| `getSymbol(String)` | 获取货币符号 |
| `formatWithSymbol(Money)` | 带符号格式化 |

### CurrencyConverter 类

| 方法 | 描述 |
|-----|------|
| `setRate(String, BigDecimal/double)` | 设置汇率 |
| `setRates(Map)` | 批量设置汇率 |
| `getRate(String)` | 获取汇率 |
| `supports(String)` | 检查是否支持 |
| `convert(Money, String)` | 货币转换 |
| `getBaseCurrency()` | 获取基准货币 |

## 中文大写金额示例

```
¥0       → 零元整
¥1       → 壹元整
¥100     → 壹佰元整
¥1234.56 → 壹仟贰佰叁拾肆元伍角陆分
¥123456.78 → 壹拾贰万叁仟肆佰伍拾陆元柒角捌分
¥-100.50 → 壹佰元伍角
```

## 设计原则

1. **不可变设计** - Money 类是不可变的，所有运算返回新对象
2. **类型安全** - 货币不匹配时会抛出 IllegalArgumentException
3. **精度保证** - 所有计算使用 BigDecimal，避免浮点误差
4. **国际化** - 支持多种地区的格式化输出

## 编译和运行

```bash
# 编译
javac MoneyUtils.java MoneyUtilsTest.java Examples.java

# 运行测试
java MoneyUtilsTest

# 运行示例
java Examples
```

## 许可证

MIT License