/**
 * MoneyUtils 测试类
 */

import java.math.BigDecimal;
import java.util.Arrays;
import java.util.Locale;

public class MoneyUtilsTest {
    
    private static int passed = 0;
    private static int failed = 0;
    
    public static void main(String[] args) {
        System.out.println("=== MoneyUtils 测试开始 ===\n");
        
        // 运行所有测试
        testMoneyCreation();
        testMoneyArithmetic();
        testMoneyComparison();
        testMoneyFormatting();
        testMoneyPercentOperations();
        testMoneySplit();
        testMoneyInterest();
        testMoneyTax();
        testCurrencyConverter();
        testMoneyUtilsHelpers();
        testChineseFormat();
        
        // 输出测试结果
        System.out.println("\n=== 测试结果 ===");
        System.out.println("通过: " + passed);
        System.out.println("失败: " + failed);
        System.out.println("总计: " + (passed + failed));
        
        if (failed == 0) {
            System.out.println("\n✅ 所有测试通过！");
        } else {
            System.out.println("\n❌ 有测试失败！");
        }
    }
    
    // ============ 测试方法 ============
    
    private static void testMoneyCreation() {
        System.out.println("--- 测试金额创建 ---");
        
        // 从不同类型创建
        Money m1 = Money.of("100.50", "CNY");
        assertEquals("100.50", m1.toNumberString(), "从字符串创建");
        
        Money m2 = Money.of(100, "USD");
        assertEquals("100.00", m2.toNumberString(), "从整数创建");
        
        Money m3 = Money.of(100.5, "EUR");
        assertEquals("100.50", m3.toNumberString(), "从double创建");
        
        Money m4 = Money.of(100L, "JPY");
        assertEquals("100", m4.toNumberString(), "从long创建（日元无小数）");
        
        // 从最小单位创建
        Money m5 = Money.fromSmallestUnit(10050, "CNY");
        assertEquals("100.50", m5.toNumberString(), "从分创建");
        
        Money m6 = Money.fromSmallestUnit(100, "JPY");
        assertEquals("100", m6.toNumberString(), "日元从最小单位创建");
        
        // 零金额
        Money m7 = Money.zero("USD");
        assertTrue(m7.isZero(), "零金额检查");
        
        System.out.println();
    }
    
    private static void testMoneyArithmetic() {
        System.out.println("--- 测试算术运算 ---");
        
        Money m1 = Money.of("100.00", "CNY");
        Money m2 = Money.of("50.00", "CNY");
        
        // 加法
        Money add = m1.add(m2);
        assertEquals("150.00", add.toNumberString(), "加法");
        
        // 减法
        Money subtract = m1.subtract(m2);
        assertEquals("50.00", subtract.toNumberString(), "减法");
        
        // 乘法
        Money multiply = m1.multiply(2);
        assertEquals("200.00", multiply.toNumberString(), "乘法");
        
        Money multiplyDecimal = m1.multiply(new BigDecimal("1.5"));
        assertEquals("150.00", multiplyDecimal.toNumberString(), "乘法(BigDecimal)");
        
        // 除法
        Money m3 = Money.of("100.00", "CNY");
        Money divide = m3.divide(3);
        assertEquals("33.33", divide.toNumberString(), "除法");
        
        // 取负
        Money negate = m1.negate();
        assertTrue(negate.isNegative(), "取负");
        assertEquals("-100.00", negate.toNumberString(), "取负值");
        
        // 绝对值
        Money abs = negate.abs();
        assertEquals("100.00", abs.toNumberString(), "绝对值");
        
        // 货币不匹配应该抛异常
        try {
            m1.add(Money.of("50.00", "USD"));
            fail("货币不匹配应该抛异常");
        } catch (IllegalArgumentException e) {
            pass("货币不匹配抛异常");
        }
        
        System.out.println();
    }
    
    private static void testMoneyComparison() {
        System.out.println("--- 测试比较运算 ---");
        
        Money m1 = Money.of("100.00", "CNY");
        Money m2 = Money.of("50.00", "CNY");
        Money m3 = Money.of("100.00", "CNY");
        
        assertTrue(m1.greaterThan(m2), "大于");
        assertTrue(m1.greaterThanOrEqual(m3), "大于等于");
        assertTrue(m2.lessThan(m1), "小于");
        assertTrue(m2.lessThanOrEqual(m2), "小于等于");
        assertTrue(m1.equals(m3), "等于");
        assertFalse(m1.equals(m2), "不等于");
        
        System.out.println();
    }
    
    private static void testMoneyFormatting() {
        System.out.println("--- 测试格式化 ---");
        
        Money m1 = Money.of("1234.56", "USD");
        String formatted = m1.format(Locale.US);
        assertTrue(formatted.contains("$") && formatted.contains("1,234.56"), 
                  "美元格式化: " + formatted);
        
        Money m2 = Money.of("1234.56", "CNY");
        String formattedCNY = m2.format(Locale.CHINA);
        assertTrue(formattedCNY.contains("¥") || formattedCNY.contains("￥"), 
                  "人民币格式化: " + formattedCNY);
        
        // 简写格式
        Money m3 = Money.of("1234567.00", "USD");
        String compact = m3.formatCompact();
        assertTrue(compact.contains("1.2M"), "简写格式: " + compact);
        
        Money m4 = Money.of("1234567890.00", "USD");
        assertTrue(m4.formatCompact().contains("1.2B"), "十亿简写");
        
        Money m5 = Money.of("1234567890123.00", "USD");
        assertTrue(m5.formatCompact().contains("1.2T"), "万亿简写");
        
        System.out.println();
    }
    
    private static void testMoneyPercentOperations() {
        System.out.println("--- 测试百分比运算 ---");
        
        Money m = Money.of("100.00", "CNY");
        
        // 百分比
        Money percent = m.percent(15);
        assertEquals("15.00", percent.toNumberString(), "15%计算");
        
        // 折扣
        Money discounted = m.discount(20);
        assertEquals("80.00", discounted.toNumberString(), "20%折扣");
        
        // 含税
        Money withTax = m.withTax(10);
        assertEquals("110.00", withTax.toNumberString(), "含10%税");
        
        // 不含税
        Money m2 = Money.of("110.00", "CNY");
        Money withoutTax = m2.withoutTax(10);
        assertEquals("100.00", withoutTax.toNumberString(), "去10%税");
        
        System.out.println();
    }
    
    private static void testMoneySplit() {
        System.out.println("--- 测试金额分摊 ---");
        
        // 平均分摊
        Money m = Money.of("100.00", "CNY");
        Money[] split1 = MoneyUtils.split(m, 3);
        assertEquals("33.34", split1[0].toNumberString(), "分摊第一份");
        assertEquals("33.33", split1[1].toNumberString(), "分摊第二份");
        assertEquals("33.33", split1[2].toNumberString(), "分摊第三份");
        
        // 验证总和
        Money sum = MoneyUtils.sum(split1);
        assertEquals("100.00", sum.toNumberString(), "分摊总和验证");
        
        // 按比例分摊
        Money[] split2 = MoneyUtils.splitByRatio(m, 1, 2, 3);
        assertEquals("16.67", split2[0].toNumberString(), "1:2:3比例第一份");
        assertEquals("33.33", split2[1].toNumberString(), "1:2:3比例第二份");
        assertEquals("50.00", split2[2].toNumberString(), "1:2:3比例第三份");
        
        System.out.println();
    }
    
    private static void testMoneyInterest() {
        System.out.println("--- 测试利息计算 ---");
        
        Money principal = Money.of("10000.00", "CNY");
        
        // 简单利息
        Money simple = MoneyUtils.simpleInterest(principal, 5, 3);
        assertEquals("1500.00", simple.toNumberString(), "简单利息");
        
        // 复利
        Money compound = MoneyUtils.compoundInterest(principal, 5, 3, 12);
        assertTrue(compound.getAmount().compareTo(new BigDecimal("11600")) > 0, 
                  "复利应该大于简单利息: " + compound.toNumberString());
        
        System.out.println();
    }
    
    private static void testMoneyTax() {
        System.out.println("--- 测试税费计算 ---");
        
        // 不含税金额
        Money m1 = Money.of("100.00", "CNY");
        Money[] tax1 = MoneyUtils.calculateTax(m1, 10, false);
        assertEquals("100.00", tax1[0].toNumberString(), "税前金额");
        assertEquals("10.00", tax1[1].toNumberString(), "税额");
        assertEquals("110.00", tax1[2].toNumberString(), "税后金额");
        
        // 含税金额
        Money m2 = Money.of("110.00", "CNY");
        Money[] tax2 = MoneyUtils.calculateTax(m2, 10, true);
        assertEquals("100.00", tax2[0].toNumberString(), "含税-税前金额");
        assertEquals("10.00", tax2[1].toNumberString(), "含税-税额");
        assertEquals("110.00", tax2[2].toNumberString(), "含税-税后金额");
        
        System.out.println();
    }
    
    private static void testCurrencyConverter() {
        System.out.println("--- 测试货币转换 ---");
        
        DefaultCurrencyConverter converter = new DefaultCurrencyConverter();
        
        // 美元转人民币
        Money usd = Money.of("100.00", "USD");
        Money cny = converter.convert(usd, "CNY");
        assertTrue(cny.getAmount().compareTo(new BigDecimal("700")) > 0, 
                  "USD转CNY: " + cny.toNumberString());
        
        // 人民币转美元
        Money backToUsd = converter.convert(cny, "USD");
        assertEquals("100.00", backToUsd.toNumberString(), "CNY转回USD");
        
        // 欧元转英镑
        Money eur = Money.of("100.00", "EUR");
        Money gbp = converter.convert(eur, "GBP");
        assertTrue(gbp.getAmount().compareTo(BigDecimal.ZERO) > 0, 
                  "EUR转GBP: " + gbp.toNumberString());
        
        System.out.println();
    }
    
    private static void testMoneyUtilsHelpers() {
        System.out.println("--- 测试 MoneyUtils 工具方法 ---");
        
        // 快捷创建方法
        Money cny1 = MoneyUtils.cny(100.50);
        assertEquals("100.50", cny1.toNumberString(), "cny快捷方法");
        
        Money usd1 = MoneyUtils.usd(100);
        assertEquals("100.00", usd1.toNumberString(), "usd快捷方法");
        
        Money eur1 = MoneyUtils.eur(100);
        assertEquals("100.00", eur1.toNumberString(), "eur快捷方法");
        
        Money jpy1 = MoneyUtils.jpy(100);
        assertEquals("100", jpy1.toNumberString(), "jpy快捷方法");
        
        // 求和
        Money sum = MoneyUtils.sum(
            Money.of("10.00", "CNY"),
            Money.of("20.00", "CNY"),
            Money.of("30.00", "CNY")
        );
        assertEquals("60.00", sum.toNumberString(), "求和");
        
        // 平均值
        Money avg = MoneyUtils.average(
            Money.of("100.00", "CNY"),
            Money.of("200.00", "CNY"),
            Money.of("300.00", "CNY")
        );
        assertEquals("200.00", avg.toNumberString(), "平均值");
        
        // 最大最小
        Money max = MoneyUtils.max(Money.of("100", "CNY"), Money.of("200", "CNY"));
        assertEquals("200.00", max.toNumberString(), "最大值");
        
        Money min = MoneyUtils.min(Money.of("100", "CNY"), Money.of("200", "CNY"));
        assertEquals("100.00", min.toNumberString(), "最小值");
        
        // 解析
        Money parsed = MoneyUtils.parse("¥1,234.56", "CNY");
        assertEquals("1234.56", parsed.toNumberString(), "解析人民币");
        
        Money parsed2 = MoneyUtils.parse("$1,234.56", "USD");
        assertEquals("1234.56", parsed2.toNumberString(), "解析美元");
        
        // 获取符号
        assertEquals("¥", MoneyUtils.getSymbol("CNY"), "获取人民币符号");
        assertEquals("$", MoneyUtils.getSymbol("USD"), "获取美元符号");
        assertEquals("€", MoneyUtils.getSymbol("EUR"), "获取欧元符号");
        
        System.out.println();
    }
    
    private static void testChineseFormat() {
        System.out.println("--- 测试中文大写金额 ---");
        
        Money m1 = Money.of("123.45", "CNY");
        String chinese1 = m1.formatChinese();
        assertTrue(chinese1.contains("壹佰") && chinese1.contains("贰拾") && 
                  chinese1.contains("叁元") && chinese1.contains("肆角") && 
                  chinese1.contains("伍分"), 
                  "123.45中文: " + chinese1);
        
        Money m2 = Money.of("100.00", "CNY");
        String chinese2 = m2.formatChinese();
        assertTrue(chinese2.contains("壹佰元"), "100元整中文: " + chinese2);
        
        Money m3 = Money.of("0", "CNY");
        assertEquals("零元整", m3.formatChinese(), "零元整");
        
        Money m4 = Money.of("-100.50", "CNY");
        String chinese4 = m4.formatChinese();
        assertTrue(chinese4.startsWith("负"), "负数中文: " + chinese4);
        
        Money m5 = Money.of("1234567.89", "CNY");
        String chinese5 = m5.formatChinese();
        assertTrue(chinese5.contains("壹佰") && chinese5.contains("贰拾") && 
                  chinese5.contains("叁万") && chinese5.contains("肆仟") && 
                  chinese5.contains("伍佰") && chinese5.contains("陆拾") && 
                  chinese5.contains("柒元"), 
                  "大数中文: " + chinese5);
        
        System.out.println();
    }
    
    // ============ 辅助方法 ============
    
    private static void assertEquals(String expected, String actual, String message) {
        if (expected.equals(actual)) {
            pass(message);
        } else {
            fail(message + " - 期望: " + expected + ", 实际: " + actual);
        }
    }
    
    private static void assertTrue(boolean condition, String message) {
        if (condition) {
            pass(message);
        } else {
            fail(message);
        }
    }
    
    private static void assertFalse(boolean condition, String message) {
        if (!condition) {
            pass(message);
        } else {
            fail(message);
        }
    }
    
    private static void pass(String message) {
        System.out.println("✅ " + message);
        passed++;
    }
    
    private static void fail(String message) {
        System.out.println("❌ " + message);
        failed++;
    }
}