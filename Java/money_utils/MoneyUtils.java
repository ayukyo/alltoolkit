/**
 * Money Utilities - 零依赖金额工具库
 * 
 * 功能：
 * - 精确金额计算（避免浮点误差）
 * - 多货币支持
 * - 金额格式化（国际化）
 * - 货币转换（基于预设汇率）
 * - 金额解析
 * - 中文大写金额
 * - 常用金额操作（分摊、折扣、税费等）
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.text.ParseException;
import java.text.ParsePosition;
import java.util.Arrays;
import java.util.Currency;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;

/**
 * 金额类 - 不可变的精确金额表示
 */
final class Money implements Comparable<Money> {
    
    private final BigDecimal amount;
    private final String currencyCode;
    private final int decimalDigits;
    
    // 常用货币的小数位数
    private static final Map<String, Integer> CURRENCY_DECIMALS = new HashMap<>();
    static {
        CURRENCY_DECIMALS.put("JPY", 0);
        CURRENCY_DECIMALS.put("KRW", 0);
        CURRENCY_DECIMALS.put("VND", 0);
        CURRENCY_DECIMALS.put("CNY", 2);
        CURRENCY_DECIMALS.put("USD", 2);
        CURRENCY_DECIMALS.put("EUR", 2);
        CURRENCY_DECIMALS.put("GBP", 2);
        CURRENCY_DECIMALS.put("HKD", 2);
        CURRENCY_DECIMALS.put("TWD", 2);
        CURRENCY_DECIMALS.put("SGD", 2);
        CURRENCY_DECIMALS.put("AUD", 2);
        CURRENCY_DECIMALS.put("CAD", 2);
        CURRENCY_DECIMALS.put("CHF", 2);
        CURRENCY_DECIMALS.put("INR", 2);
        CURRENCY_DECIMALS.put("RUB", 2);
        CURRENCY_DECIMALS.put("BRL", 2);
        CURRENCY_DECIMALS.put("THB", 2);
        CURRENCY_DECIMALS.put("PHP", 2);
        CURRENCY_DECIMALS.put("MYR", 2);
        CURRENCY_DECIMALS.put("IDR", 0);
    }
    
    /**
     * 构造函数
     * @param amount 金额
     * @param currencyCode 货币代码
     */
    public Money(BigDecimal amount, String currencyCode) {
        Objects.requireNonNull(amount, "Amount cannot be null");
        Objects.requireNonNull(currencyCode, "Currency code cannot be null");
        
        this.currencyCode = currencyCode.toUpperCase();
        this.decimalDigits = CURRENCY_DECIMALS.getOrDefault(this.currencyCode, 2);
        this.amount = amount.setScale(this.decimalDigits, RoundingMode.HALF_EVEN);
    }
    
    /**
     * 从字符串创建金额
     * @param amount 金额字符串
     * @param currencyCode 货币代码
     * @return Money 对象
     */
    public static Money of(String amount, String currencyCode) {
        return new Money(new BigDecimal(amount), currencyCode);
    }
    
    /**
     * 从整数创建金额
     * @param amount 金额整数
     * @param currencyCode 货币代码
     * @return Money 对象
     */
    public static Money of(int amount, String currencyCode) {
        return new Money(new BigDecimal(amount), currencyCode);
    }
    
    /**
     * 从 long 创建金额
     * @param amount 金额
     * @param currencyCode 货币代码
     * @return Money 对象
     */
    public static Money of(long amount, String currencyCode) {
        return new Money(new BigDecimal(amount), currencyCode);
    }
    
    /**
     * 从 double 创建金额
     * @param amount 金额
     * @param currencyCode 货币代码
     * @return Money 对象
     */
    public static Money of(double amount, String currencyCode) {
        return new Money(BigDecimal.valueOf(amount), currencyCode);
    }
    
    /**
     * 从最小单位创建金额（如分转元）
     * @param smallestUnit 最小单位数量（如分）
     * @param currencyCode 货币代码
     * @return Money 对象
     */
    public static Money fromSmallestUnit(long smallestUnit, String currencyCode) {
        int decimals = CURRENCY_DECIMALS.getOrDefault(currencyCode.toUpperCase(), 2);
        BigDecimal divisor = BigDecimal.TEN.pow(decimals);
        return new Money(BigDecimal.valueOf(smallestUnit).divide(divisor, decimals, RoundingMode.HALF_EVEN), currencyCode);
    }
    
    /**
     * 零金额
     * @param currencyCode 货币代码
     * @return 零金额 Money 对象
     */
    public static Money zero(String currencyCode) {
        return new Money(BigDecimal.ZERO, currencyCode);
    }
    
    // ============ 基本属性 ============
    
    /**
     * 获取金额
     * @return 金额 BigDecimal
     */
    public BigDecimal getAmount() {
        return amount;
    }
    
    /**
     * 获取货币代码
     * @return 货币代码
     */
    public String getCurrencyCode() {
        return currencyCode;
    }
    
    /**
     * 获取小数位数
     * @return 小数位数
     */
    public int getDecimalDigits() {
        return decimalDigits;
    }
    
    /**
     * 获取最小单位值（如元转分）
     * @return 最小单位值
     */
    public long toSmallestUnit() {
        BigDecimal multiplier = BigDecimal.TEN.pow(decimalDigits);
        return amount.multiply(multiplier).longValue();
    }
    
    /**
     * 是否为零
     * @return 如果为零返回 true
     */
    public boolean isZero() {
        return amount.compareTo(BigDecimal.ZERO) == 0;
    }
    
    /**
     * 是否为正数
     * @return 如果为正数返回 true
     */
    public boolean isPositive() {
        return amount.compareTo(BigDecimal.ZERO) > 0;
    }
    
    /**
     * 是否为负数
     * @return 如果为负数返回 true
     */
    public boolean isNegative() {
        return amount.compareTo(BigDecimal.ZERO) < 0;
    }
    
    // ============ 算术运算 ============
    
    /**
     * 加法
     * @param other 另一个金额
     * @return 结果
     * @throws IllegalArgumentException 货币不匹配时抛出
     */
    public Money add(Money other) {
        checkCurrency(other);
        return new Money(amount.add(other.amount), currencyCode);
    }
    
    /**
     * 加上一个数值
     * @param value 数值
     * @return 结果
     */
    public Money add(BigDecimal value) {
        return new Money(amount.add(value), currencyCode);
    }
    
    /**
     * 减法
     * @param other 另一个金额
     * @return 结果
     * @throws IllegalArgumentException 货币不匹配时抛出
     */
    public Money subtract(Money other) {
        checkCurrency(other);
        return new Money(amount.subtract(other.amount), currencyCode);
    }
    
    /**
     * 减去一个数值
     * @param value 数值
     * @return 结果
     */
    public Money subtract(BigDecimal value) {
        return new Money(amount.subtract(value), currencyCode);
    }
    
    /**
     * 乘法
     * @param multiplier 乘数
     * @return 结果
     */
    public Money multiply(BigDecimal multiplier) {
        return new Money(amount.multiply(multiplier), currencyCode);
    }
    
    /**
     * 乘法
     * @param multiplier 乘数
     * @return 结果
     */
    public Money multiply(int multiplier) {
        return multiply(BigDecimal.valueOf(multiplier));
    }
    
    /**
     * 乘法
     * @param multiplier 乘数
     * @return 结果
     */
    public Money multiply(double multiplier) {
        return multiply(BigDecimal.valueOf(multiplier));
    }
    
    /**
     * 除法
     * @param divisor 除数
     * @return 结果
     */
    public Money divide(BigDecimal divisor) {
        return new Money(amount.divide(divisor, decimalDigits, RoundingMode.HALF_EVEN), currencyCode);
    }
    
    /**
     * 除法
     * @param divisor 除数
     * @return 结果
     */
    public Money divide(int divisor) {
        return divide(BigDecimal.valueOf(divisor));
    }
    
    /**
     * 除法
     * @param divisor 除数
     * @return 结果
     */
    public Money divide(double divisor) {
        return divide(BigDecimal.valueOf(divisor));
    }
    
    /**
     * 取模
     * @param divisor 除数
     * @return 余数
     */
    public Money remainder(BigDecimal divisor) {
        return new Money(amount.remainder(divisor), currencyCode);
    }
    
    /**
     * 取负
     * @return 负金额
     */
    public Money negate() {
        return new Money(amount.negate(), currencyCode);
    }
    
    /**
     * 取绝对值
     * @return 绝对值金额
     */
    public Money abs() {
        return new Money(amount.abs(), currencyCode);
    }
    
    // ============ 百分比运算 ============
    
    /**
     * 计算百分比
     * @param percent 百分比（如 15 表示 15%）
     * @return 百分比金额
     */
    public Money percent(BigDecimal percent) {
        return multiply(percent.divide(BigDecimal.valueOf(100), 10, RoundingMode.HALF_EVEN));
    }
    
    /**
     * 计算百分比
     * @param percent 百分比
     * @return 百分比金额
     */
    public Money percent(double percent) {
        return percent(BigDecimal.valueOf(percent));
    }
    
    /**
     * 应用折扣
     * @param discountPercent 折扣百分比
     * @return 折后金额
     */
    public Money discount(double discountPercent) {
        return multiply(BigDecimal.valueOf(1 - discountPercent / 100));
    }
    
    /**
     * 应用税率
     * @param taxRatePercent 税率百分比
     * @return 含税金额
     */
    public Money withTax(double taxRatePercent) {
        return multiply(BigDecimal.valueOf(1 + taxRatePercent / 100));
    }
    
    /**
     * 去除税率
     * @param taxRatePercent 税率百分比
     * @return 不含税金额
     */
    public Money withoutTax(double taxRatePercent) {
        return divide(BigDecimal.valueOf(1 + taxRatePercent / 100));
    }
    
    // ============ 比较运算 ============
    
    @Override
    public int compareTo(Money other) {
        checkCurrency(other);
        return amount.compareTo(other.amount);
    }
    
    /**
     * 大于
     */
    public boolean greaterThan(Money other) {
        return compareTo(other) > 0;
    }
    
    /**
     * 大于等于
     */
    public boolean greaterThanOrEqual(Money other) {
        return compareTo(other) >= 0;
    }
    
    /**
     * 小于
     */
    public boolean lessThan(Money other) {
        return compareTo(other) < 0;
    }
    
    /**
     * 小于等于
     */
    public boolean lessThanOrEqual(Money other) {
        return compareTo(other) <= 0;
    }
    
    // ============ 格式化 ============
    
    /**
     * 格式化为字符串
     * @return 格式化字符串
     */
    public String format() {
        return format(Locale.getDefault());
    }
    
    /**
     * 格式化为字符串
     * @param locale 地区
     * @return 格式化字符串
     */
    public String format(Locale locale) {
        try {
            Currency currency = Currency.getInstance(currencyCode);
            java.text.NumberFormat format = java.text.NumberFormat.getCurrencyInstance(locale);
            format.setCurrency(currency);
            return format.format(amount);
        } catch (IllegalArgumentException e) {
            // 货币不支持时使用简单格式
            DecimalFormatSymbols symbols = new DecimalFormatSymbols(locale);
            DecimalFormat format = new DecimalFormat("#,##0.00", symbols);
            return format.format(amount) + " " + currencyCode;
        }
    }
    
    /**
     * 格式化为简写形式（K, M, B, T）
     * @return 简写形式
     */
    public String formatCompact() {
        BigDecimal absAmount = amount.abs();
        String prefix = amount.compareTo(BigDecimal.ZERO) < 0 ? "-" : "";
        
        if (absAmount.compareTo(BigDecimal.valueOf(1_000_000_000_000L)) >= 0) {
            return prefix + absAmount.divide(BigDecimal.valueOf(1_000_000_000_000L), 1, RoundingMode.HALF_EVEN) + "T";
        } else if (absAmount.compareTo(BigDecimal.valueOf(1_000_000_000L)) >= 0) {
            return prefix + absAmount.divide(BigDecimal.valueOf(1_000_000_000L), 1, RoundingMode.HALF_EVEN) + "B";
        } else if (absAmount.compareTo(BigDecimal.valueOf(1_000_000L)) >= 0) {
            return prefix + absAmount.divide(BigDecimal.valueOf(1_000_000L), 1, RoundingMode.HALF_EVEN) + "M";
        } else if (absAmount.compareTo(BigDecimal.valueOf(1_000L)) >= 0) {
            return prefix + absAmount.divide(BigDecimal.valueOf(1_000L), 1, RoundingMode.HALF_EVEN) + "K";
        } else {
            return prefix + absAmount.setScale(decimalDigits, RoundingMode.HALF_EVEN).toPlainString();
        }
    }
    
    /**
     * 格式化为中文大写金额
     * @return 中文大写金额
     */
    public String formatChinese() {
        if (amount.compareTo(BigDecimal.ZERO) == 0) {
            return "零元整";
        }
        
        String[] digits = {"零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖"};
        String[] units = {"", "拾", "佰", "仟"};
        String[] bigUnits = {"", "万", "亿", "兆"};
        String[] decimalUnits = {"角", "分"};
        
        boolean isNegative = amount.compareTo(BigDecimal.ZERO) < 0;
        BigDecimal absAmount = amount.abs();
        
        long integerPart = absAmount.longValue();
        int decimalPart = absAmount.subtract(BigDecimal.valueOf(integerPart))
                .multiply(BigDecimal.valueOf(100))
                .intValue();
        
        StringBuilder result = new StringBuilder();
        
        if (integerPart > 0) {
            int groupIndex = 0;
            while (integerPart > 0) {
                int group = (int) (integerPart % 10000);
                if (group > 0) {
                    StringBuilder groupStr = new StringBuilder();
                    boolean hasZero = false;
                    
                    for (int i = 0; i < 4; i++) {
                        int digit = (group / (int) Math.pow(10, i)) % 10;
                        if (digit == 0) {
                            hasZero = true;
                        } else {
                            if (hasZero && groupStr.length() > 0) {
                                groupStr.insert(0, "零");
                            }
                            hasZero = false;
                            groupStr.insert(0, digits[digit] + units[i]);
                        }
                    }
                    
                    result.insert(0, groupStr + bigUnits[groupIndex]);
                }
                integerPart /= 10000;
                groupIndex++;
            }
            result.append("元");
        }
        
        if (decimalPart > 0) {
            int jiao = decimalPart / 10;
            int fen = decimalPart % 10;
            
            if (jiao > 0) {
                result.append(digits[jiao]).append(decimalUnits[0]);
            }
            if (fen > 0) {
                result.append(digits[fen]).append(decimalUnits[1]);
            }
        } else if (integerPart > 0) {
            result.append("整");
        }
        
        return (isNegative ? "负" : "") + result.toString();
    }
    
    /**
     * 格式化为不带货币符号的数字字符串
     * @return 数字字符串
     */
    public String toNumberString() {
        return amount.setScale(decimalDigits, RoundingMode.HALF_EVEN).toPlainString();
    }
    
    @Override
    public String toString() {
        return format();
    }
    
    // ============ Object 方法 ============
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof Money)) return false;
        Money other = (Money) obj;
        return amount.compareTo(other.amount) == 0 && currencyCode.equals(other.currencyCode);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(amount, currencyCode);
    }
    
    private void checkCurrency(Money other) {
        if (!currencyCode.equals(other.currencyCode)) {
            throw new IllegalArgumentException(
                "Currency mismatch: " + currencyCode + " vs " + other.currencyCode);
        }
    }
}

/**
 * 货币转换器
 */
class CurrencyConverter {
    
    private final Map<String, BigDecimal> rates;
    private final String baseCurrency;
    
    /**
     * 创建货币转换器
     * @param baseCurrency 基准货币
     */
    public CurrencyConverter(String baseCurrency) {
        this.baseCurrency = baseCurrency.toUpperCase();
        this.rates = new HashMap<>();
        this.rates.put(this.baseCurrency, BigDecimal.ONE);
    }
    
    /**
     * 设置汇率
     * @param currency 货币代码
     * @param rate 相对于基准货币的汇率
     */
    public void setRate(String currency, BigDecimal rate) {
        rates.put(currency.toUpperCase(), rate);
    }
    
    /**
     * 设置汇率
     * @param currency 货币代码
     * @param rate 相对于基准货币的汇率
     */
    public void setRate(String currency, double rate) {
        setRate(currency, BigDecimal.valueOf(rate));
    }
    
    /**
     * 批量设置汇率
     * @param newRates 汇率映射
     */
    public void setRates(Map<String, BigDecimal> newRates) {
        rates.putAll(newRates);
    }
    
    /**
     * 获取汇率
     * @param currency 货币代码
     * @return 汇率
     */
    public BigDecimal getRate(String currency) {
        return rates.get(currency.toUpperCase());
    }
    
    /**
     * 检查是否支持某货币
     * @param currency 货币代码
     * @return 是否支持
     */
    public boolean supports(String currency) {
        return rates.containsKey(currency.toUpperCase());
    }
    
    /**
     * 转换货币
     * @param money 原金额
     * @param toCurrency 目标货币
     * @return 转换后的金额
     */
    public Money convert(Money money, String toCurrency) {
        String to = toCurrency.toUpperCase();
        
        if (money.getCurrencyCode().equals(to)) {
            return money;
        }
        
        BigDecimal fromRate = rates.get(money.getCurrencyCode());
        BigDecimal toRate = rates.get(to);
        
        if (fromRate == null) {
            throw new IllegalArgumentException("Unsupported currency: " + money.getCurrencyCode());
        }
        if (toRate == null) {
            throw new IllegalArgumentException("Unsupported currency: " + to);
        }
        
        // 先转换为基准货币，再转换为目标货币
        BigDecimal baseAmount = money.getAmount().divide(fromRate, 10, RoundingMode.HALF_EVEN);
        BigDecimal converted = baseAmount.multiply(toRate);
        
        return new Money(converted, to);
    }
    
    /**
     * 获取基准货币
     * @return 基准货币代码
     */
    public String getBaseCurrency() {
        return baseCurrency;
    }
}

/**
 * 金额工具类
 */
class MoneyUtils {
    
    // 常用货币符号
    private static final Map<String, String> CURRENCY_SYMBOLS = new HashMap<>();
    static {
        CURRENCY_SYMBOLS.put("CNY", "¥");
        CURRENCY_SYMBOLS.put("USD", "$");
        CURRENCY_SYMBOLS.put("EUR", "€");
        CURRENCY_SYMBOLS.put("GBP", "£");
        CURRENCY_SYMBOLS.put("JPY", "¥");
        CURRENCY_SYMBOLS.put("KRW", "₩");
        CURRENCY_SYMBOLS.put("HKD", "HK$");
        CURRENCY_SYMBOLS.put("TWD", "NT$");
        CURRENCY_SYMBOLS.put("SGD", "S$");
        CURRENCY_SYMBOLS.put("AUD", "A$");
        CURRENCY_SYMBOLS.put("CAD", "C$");
        CURRENCY_SYMBOLS.put("CHF", "Fr");
        CURRENCY_SYMBOLS.put("INR", "₹");
        CURRENCY_SYMBOLS.put("RUB", "₽");
        CURRENCY_SYMBOLS.put("BRL", "R$");
        CURRENCY_SYMBOLS.put("THB", "฿");
        CURRENCY_SYMBOLS.put("VND", "₫");
        CURRENCY_SYMBOLS.put("PHP", "₱");
        CURRENCY_SYMBOLS.put("MYR", "RM");
        CURRENCY_SYMBOLS.put("IDR", "Rp");
    }
    
    private MoneyUtils() {}
    
    // ============ 创建金额 ============
    
    /**
     * 创建金额
     */
    public static Money money(BigDecimal amount, String currencyCode) {
        return new Money(amount, currencyCode);
    }
    
    /**
     * 创建金额
     */
    public static Money money(String amount, String currencyCode) {
        return Money.of(amount, currencyCode);
    }
    
    /**
     * 创建金额
     */
    public static Money money(int amount, String currencyCode) {
        return Money.of(amount, currencyCode);
    }
    
    /**
     * 创建金额
     */
    public static Money money(long amount, String currencyCode) {
        return Money.of(amount, currencyCode);
    }
    
    /**
     * 创建金额
     */
    public static Money money(double amount, String currencyCode) {
        return Money.of(amount, currencyCode);
    }
    
    /**
     * 创建人民币金额
     */
    public static Money cny(BigDecimal amount) {
        return new Money(amount, "CNY");
    }
    
    /**
     * 创建人民币金额
     */
    public static Money cny(double amount) {
        return Money.of(amount, "CNY");
    }
    
    /**
     * 创建美元金额
     */
    public static Money usd(BigDecimal amount) {
        return new Money(amount, "USD");
    }
    
    /**
     * 创建美元金额
     */
    public static Money usd(double amount) {
        return Money.of(amount, "USD");
    }
    
    /**
     * 创建欧元金额
     */
    public static Money eur(BigDecimal amount) {
        return new Money(amount, "EUR");
    }
    
    /**
     * 创建欧元金额
     */
    public static Money eur(double amount) {
        return Money.of(amount, "EUR");
    }
    
    /**
     * 创建日元金额
     */
    public static Money jpy(BigDecimal amount) {
        return new Money(amount, "JPY");
    }
    
    /**
     * 创建日元金额
     */
    public static Money jpy(double amount) {
        return Money.of(amount, "JPY");
    }
    
    // ============ 解析 ============
    
    /**
     * 解析金额字符串
     * @param str 金额字符串
     * @param currencyCode 货币代码
     * @return Money 对象
     */
    public static Money parse(String str, String currencyCode) {
        // 移除货币符号和空格
        String cleaned = str.replaceAll("[^\\d.,\\-()]", "")
                           .replace("(", "-")
                           .replace(")", "");
        
        // 处理不同的数字格式
        int lastComma = cleaned.lastIndexOf(',');
        int lastDot = cleaned.lastIndexOf('.');
        
        if (lastComma > lastDot) {
            // 欧洲格式：逗号是小数点
            cleaned = cleaned.replace(".", "").replace(",", ".");
        } else {
            // 英美格式：点是小数点
            cleaned = cleaned.replace(",", "");
        }
        
        try {
            return new Money(new BigDecimal(cleaned), currencyCode);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("Invalid money format: " + str);
        }
    }
    
    // ============ 计算 ============
    
    /**
     * 求和
     * @param monies 金额数组
     * @return 总和
     */
    public static Money sum(Money... monies) {
        if (monies == null || monies.length == 0) {
            throw new IllegalArgumentException("Money array cannot be null or empty");
        }
        
        Money result = monies[0];
        for (int i = 1; i < monies.length; i++) {
            result = result.add(monies[i]);
        }
        return result;
    }
    
    /**
     * 求和
     * @param monies 金额列表
     * @return 总和
     */
    public static Money sum(Iterable<Money> monies) {
        Money result = null;
        for (Money money : monies) {
            if (result == null) {
                result = money;
            } else {
                result = result.add(money);
            }
        }
        if (result == null) {
            throw new IllegalArgumentException("Money iterable cannot be empty");
        }
        return result;
    }
    
    /**
     * 求平均值
     * @param monies 金额数组
     * @return 平均值
     */
    public static Money average(Money... monies) {
        if (monies == null || monies.length == 0) {
            throw new IllegalArgumentException("Money array cannot be null or empty");
        }
        return sum(monies).divide(monies.length);
    }
    
    /**
     * 求最大值
     */
    public static Money max(Money a, Money b) {
        return a.greaterThan(b) ? a : b;
    }
    
    /**
     * 求最小值
     */
    public static Money min(Money a, Money b) {
        return a.lessThan(b) ? a : b;
    }
    
    /**
     * 分摊金额
     * @param amount 总金额
     * @param parts 分成几份
     * @return 分摊后的金额数组
     */
    public static Money[] split(Money amount, int parts) {
        if (parts <= 0) {
            throw new IllegalArgumentException("Parts must be positive");
        }
        
        Money[] result = new Money[parts];
        BigDecimal[] shares = split(amount.getAmount(), parts, amount.getDecimalDigits());
        
        for (int i = 0; i < parts; i++) {
            result[i] = new Money(shares[i], amount.getCurrencyCode());
        }
        
        return result;
    }
    
    /**
     * 按比例分摊金额
     * @param amount 总金额
     * @param ratios 比例数组
     * @return 分摊后的金额数组
     */
    public static Money[] splitByRatio(Money amount, int... ratios) {
        if (ratios == null || ratios.length == 0) {
            throw new IllegalArgumentException("Ratios cannot be null or empty");
        }
        
        int totalRatio = 0;
        for (int ratio : ratios) {
            if (ratio < 0) {
                throw new IllegalArgumentException("Ratios must be non-negative");
            }
            totalRatio += ratio;
        }
        
        if (totalRatio == 0) {
            throw new IllegalArgumentException("Total ratio must be positive");
        }
        
        Money[] result = new Money[ratios.length];
        BigDecimal remaining = amount.getAmount();
        
        for (int i = 0; i < ratios.length; i++) {
            if (i == ratios.length - 1) {
                // 最后一部分取剩余，避免精度损失
                result[i] = new Money(remaining, amount.getCurrencyCode());
            } else {
                BigDecimal share = amount.getAmount()
                        .multiply(BigDecimal.valueOf(ratios[i]))
                        .divide(BigDecimal.valueOf(totalRatio), amount.getDecimalDigits(), RoundingMode.HALF_EVEN);
                result[i] = new Money(share, amount.getCurrencyCode());
                remaining = remaining.subtract(share);
            }
        }
        
        return result;
    }
    
    /**
     * 计算简单利息
     * @param principal 本金
     * @param rate 年利率百分比
     * @param years 年数
     * @return 利息
     */
    public static Money simpleInterest(Money principal, double rate, double years) {
        BigDecimal interest = principal.getAmount()
                .multiply(BigDecimal.valueOf(rate / 100 * years));
        return new Money(interest, principal.getCurrencyCode());
    }
    
    /**
     * 计算复利
     * @param principal 本金
     * @param rate 年利率百分比
     * @param years 年数
     * @param compoundsPerYear 每年复利次数
     * @return 本息合计
     */
    public static Money compoundInterest(Money principal, double rate, double years, int compoundsPerYear) {
        double r = rate / 100;
        double factor = Math.pow(1 + r / compoundsPerYear, compoundsPerYear * years);
        BigDecimal total = principal.getAmount().multiply(BigDecimal.valueOf(factor));
        return new Money(total, principal.getCurrencyCode());
    }
    
    /**
     * 计算税费
     * @param amount 金额
     * @param taxRate 税率百分比
     * @param inclusive 是否含税
     * @return [税前金额, 税额, 税后金额]
     */
    public static Money[] calculateTax(Money amount, double taxRate, boolean inclusive) {
        Money[] result = new Money[3];
        
        if (inclusive) {
            // 含税金额：求税前
            Money subtotal = amount.withoutTax(taxRate);
            Money tax = amount.subtract(subtotal);
            result[0] = subtotal;
            result[1] = tax;
            result[2] = amount;
        } else {
            // 不含税金额：求税后
            Money tax = amount.percent(taxRate);
            Money total = amount.add(tax);
            result[0] = amount;
            result[1] = tax;
            result[2] = total;
        }
        
        return result;
    }
    
    // ============ 货币信息 ============
    
    /**
     * 获取货币符号
     * @param currencyCode 货币代码
     * @return 货币符号
     */
    public static String getSymbol(String currencyCode) {
        return CURRENCY_SYMBOLS.getOrDefault(currencyCode.toUpperCase(), currencyCode);
    }
    
    /**
     * 格式化金额（带符号）
     * @param money 金额
     * @return 格式化字符串
     */
    public static String formatWithSymbol(Money money) {
        String symbol = getSymbol(money.getCurrencyCode());
        return symbol + money.toNumberString();
    }
    
    /**
     * 比较两个金额是否相等（允许不同货币）
     */
    public static boolean equals(Money a, Money b) {
        if (!a.getCurrencyCode().equals(b.getCurrencyCode())) {
            return false;
        }
        return a.equals(b);
    }
    
    // ============ 私有方法 ============
    
    private static BigDecimal[] split(BigDecimal amount, int parts, int scale) {
        BigDecimal[] result = new BigDecimal[parts];
        BigDecimal baseShare = amount.divide(BigDecimal.valueOf(parts), scale, RoundingMode.DOWN);
        BigDecimal totalAllocated = baseShare.multiply(BigDecimal.valueOf(parts));
        BigDecimal remainder = amount.subtract(totalAllocated);
        
        for (int i = 0; i < parts; i++) {
            result[i] = baseShare;
        }
        
        // 将余数分配给前几个部分
        BigDecimal unit = BigDecimal.ONE.divide(BigDecimal.TEN.pow(scale), scale, RoundingMode.HALF_EVEN);
        int remainderUnits = remainder.multiply(BigDecimal.TEN.pow(scale)).intValue();
        
        for (int i = 0; i < remainderUnits; i++) {
            result[i] = result[i].add(unit);
        }
        
        return result;
    }
}

/**
 * 默认货币转换器（带预设汇率）
 */
class DefaultCurrencyConverter extends CurrencyConverter {
    
    public DefaultCurrencyConverter() {
        super("USD");
        
        // 设置常用货币汇率（相对于 USD，仅作示例）
        setRate("CNY", 7.24);
        setRate("EUR", 0.92);
        setRate("GBP", 0.79);
        setRate("JPY", 154.50);
        setRate("KRW", 1360);
        setRate("HKD", 7.82);
        setRate("TWD", 32.10);
        setRate("SGD", 1.35);
        setRate("AUD", 1.53);
        setRate("CAD", 1.36);
        setRate("CHF", 0.90);
        setRate("INR", 83.12);
        setRate("RUB", 89.50);
        setRate("BRL", 5.05);
        setRate("THB", 36.20);
        setRate("VND", 25400);
        setRate("PHP", 58.50);
        setRate("MYR", 4.72);
        setRate("IDR", 16200);
    }
}