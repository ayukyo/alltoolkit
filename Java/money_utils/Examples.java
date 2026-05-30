/**
 * MoneyUtils 使用示例
 * 
 * 展示如何使用金额工具库进行精确计算、格式化、转换等操作
 */

import java.math.BigDecimal;
import java.util.Arrays;
import java.util.Locale;

public class Examples {
    
    public static void main(String[] args) {
        System.out.println("========================================");
        System.out.println("   MoneyUtils 使用示例");
        System.out.println("========================================\n");
        
        // 示例1：创建金额
        example1_Creation();
        
        // 示例2：算术运算
        example2_Arithmetic();
        
        // 示例3：格式化
        example3_Formatting();
        
        // 示例4：百分比和折扣
        example4_PercentAndDiscount();
        
        // 示例5：金额分摊
        example5_Split();
        
        // 示例6：货币转换
        example6_CurrencyConversion();
        
        // 示例7：税费计算
        example7_TaxCalculation();
        
        // 示例8：利息计算
        example8_InterestCalculation();
        
        // 示例9：中文大写金额
        example9_ChineseFormat();
        
        // 示例10：实际应用场景
        example10_RealWorldScenarios();
    }
    
    /**
     * 示例1：创建金额的多种方式
     */
    private static void example1_Creation() {
        System.out.println("--- 示例1：创建金额 ---");
        
        // 从不同类型创建
        Money fromString = Money.of("100.50", "CNY");
        Money fromInt = Money.of(100, "USD");
        Money fromDouble = Money.of(100.50, "EUR");
        Money fromLong = Money.of(100L, "JPY");
        
        System.out.println("从字符串创建: " + fromString);
        System.out.println("从整数创建: " + fromInt);
        System.out.println("从double创建: " + fromDouble);
        System.out.println("从long创建: " + fromLong);
        
        // 从最小单位创建（分转元）
        Money fromCents = Money.fromSmallestUnit(10050, "CNY");
        System.out.println("从分创建（10050分）: " + fromCents);
        
        // 快捷方法
        Money cny = MoneyUtils.cny(1000);
        Money usd = MoneyUtils.usd(100);
        Money eur = MoneyUtils.eur(100);
        System.out.println("快捷方法: CNY=" + cny + ", USD=" + usd + ", EUR=" + eur);
        
        // 零金额
        Money zero = Money.zero("USD");
        System.out.println("零金额: " + zero);
        
        System.out.println();
    }
    
    /**
     * 示例2：算术运算
     */
    private static void example2_Arithmetic() {
        System.out.println("--- 示例2：算术运算 ---");
        
        Money price1 = Money.of("100.00", "CNY");
        Money price2 = Money.of("50.00", "CNY");
        
        // 加法
        Money total = price1.add(price2);
        System.out.println("100 + 50 = " + total);
        
        // 减法
        Money diff = price1.subtract(price2);
        System.out.println("100 - 50 = " + diff);
        
        // 乘法
        Money doubled = price1.multiply(2);
        System.out.println("100 × 2 = " + doubled);
        
        Money tripled = price1.multiply(new BigDecimal("3"));
        System.out.println("100 × 3 = " + tripled);
        
        // 除法
        Money divided = price1.divide(4);
        System.out.println("100 ÷ 4 = " + divided);
        
        // 取负
        Money negative = price1.negate();
        System.out.println("取负: " + negative);
        
        // 绝对值
        Money absolute = negative.abs();
        System.out.println("绝对值: " + absolute);
        
        // 求和多个金额
        Money sum = MoneyUtils.sum(
            Money.of("10.00", "CNY"),
            Money.of("20.00", "CNY"),
            Money.of("30.00", "CNY")
        );
        System.out.println("求和 10+20+30 = " + sum);
        
        System.out.println();
    }
    
    /**
     * 示例3：格式化
     */
    private static void example3_Formatting() {
        System.out.println("--- 示例3：格式化 ---");
        
        Money usd = Money.of("1234.56", "USD");
        Money cny = Money.of("1234.56", "CNY");
        Money eur = Money.of("1234.56", "EUR");
        
        // 默认格式化
        System.out.println("USD 默认: " + usd.format());
        System.out.println("CNY 默认: " + cny.format());
        System.out.println("EUR 默认: " + eur.format());
        
        // 指定地区格式化
        System.out.println("USD 美国格式: " + usd.format(Locale.US));
        System.out.println("CNY 中国格式: " + cny.format(Locale.CHINA));
        System.out.println("EUR 德国格式: " + eur.format(Locale.GERMANY));
        
        // 简写格式
        Money large = Money.of("1234567.89", "USD");
        System.out.println("大数简写: " + large.formatCompact());
        
        Money millions = Money.of("12345678.90", "USD");
        System.out.println("百万简写: " + millions.formatCompact());
        
        Money billions = Money.of("1234567890.00", "USD");
        System.out.println("十亿简写: " + billions.formatCompact());
        
        // 带符号格式化
        System.out.println("USD 带符号: " + MoneyUtils.formatWithSymbol(usd));
        System.out.println("CNY 带符号: " + MoneyUtils.formatWithSymbol(cny));
        
        System.out.println();
    }
    
    /**
     * 示例4：百分比和折扣
     */
    private static void example4_PercentAndDiscount() {
        System.out.println("--- 示例4：百分比和折扣 ---");
        
        Money price = Money.of("200.00", "CNY");
        
        // 计算百分比
        Money tenPercent = price.percent(10);
        System.out.println("200的10% = " + tenPercent);
        
        Money fifteenPercent = price.percent(15);
        System.out.println("200的15% = " + fifteenPercent);
        
        // 应用折扣
        Money discounted = price.discount(20);  // 20%折扣
        System.out.println("200打8折 = " + discounted);
        
        Money halfPrice = price.discount(50);
        System.out.println("200半价 = " + halfPrice);
        
        // 含税和不含税
        Money withTax = price.withTax(10);
        System.out.println("200含10%税 = " + withTax);
        
        Money withoutTax = withTax.withoutTax(10);
        System.out.println("220去10%税 = " + withoutTax);
        
        System.out.println();
    }
    
    /**
     * 示例5：金额分摊
     */
    private static void example5_Split() {
        System.out.println("--- 示例5：金额分摊 ---");
        
        Money total = Money.of("100.00", "CNY");
        
        // 平均分摊
        Money[] split3 = MoneyUtils.split(total, 3);
        System.out.println("100元分3份: " + Arrays.toString(formatArray(split3)));
        
        Money[] split7 = MoneyUtils.split(total, 7);
        System.out.println("100元分7份: " + Arrays.toString(formatArray(split7)));
        
        // 按比例分摊
        Money[] byRatio = MoneyUtils.splitByRatio(total, 1, 2, 3);
        System.out.println("100元按1:2:3分摊: " + Arrays.toString(formatArray(byRatio)));
        
        Money[] byRatio2 = MoneyUtils.splitByRatio(total, 10, 20, 30, 40);
        System.out.println("100元按10:20:30:40分摊: " + Arrays.toString(formatArray(byRatio2)));
        
        System.out.println();
    }
    
    /**
     * 示例6：货币转换
     */
    private static void example6_CurrencyConversion() {
        System.out.println("--- 示例6：货币转换 ---");
        
        DefaultCurrencyConverter converter = new DefaultCurrencyConverter();
        
        // 美元转人民币
        Money usd100 = Money.of("100.00", "USD");
        Money cnyConverted = converter.convert(usd100, "CNY");
        System.out.println("$100 ≈ ¥" + cnyConverted.toNumberString());
        
        // 人民币转美元
        Money cny724 = Money.of("724.00", "CNY");
        Money usdConverted = converter.convert(cny724, "USD");
        System.out.println("¥724 ≈ $" + usdConverted.toNumberString());
        
        // 美元转欧元
        Money eurConverted = converter.convert(usd100, "EUR");
        System.out.println("$100 ≈ €" + eurConverted.toNumberString());
        
        // 美元转日元
        Money jpyConverted = converter.convert(usd100, "JPY");
        System.out.println("$100 ≈ ¥" + jpyConverted.toNumberString() + "（日元）");
        
        // 自定义汇率转换器
        CurrencyConverter custom = new CurrencyConverter("CNY");
        custom.setRate("USD", 0.138);  // 1 CNY ≈ 0.138 USD
        custom.setRate("EUR", 0.127);
        
        Money cny1000 = Money.of("1000.00", "CNY");
        System.out.println("¥1000 (自定义汇率) ≈ $" + custom.convert(cny1000, "USD").toNumberString());
        
        System.out.println();
    }
    
    /**
     * 示例7：税费计算
     */
    private static void example7_TaxCalculation() {
        System.out.println("--- 示例7：税费计算 ---");
        
        // 不含税价格计算
        Money priceWithoutTax = Money.of("100.00", "CNY");
        Money[] taxAdded = MoneyUtils.calculateTax(priceWithoutTax, 13, false);
        System.out.println("不含税价格: ¥100");
        System.out.println("税率: 13%");
        System.out.println("税前金额: ¥" + taxAdded[0].toNumberString());
        System.out.println("税额: ¥" + taxAdded[1].toNumberString());
        System.out.println("税后金额: ¥" + taxAdded[2].toNumberString());
        
        // 含税价格反算
        Money priceWithTax = Money.of("113.00", "CNY");
        Money[] taxIncluded = MoneyUtils.calculateTax(priceWithTax, 13, true);
        System.out.println("\n含税价格: ¥113");
        System.out.println("税前金额: ¥" + taxIncluded[0].toNumberString());
        System.out.println("税额: ¥" + taxIncluded[1].toNumberString());
        
        System.out.println();
    }
    
    /**
     * 示例8：利息计算
     */
    private static void example8_InterestCalculation() {
        System.out.println("--- 示例8：利息计算 ---");
        
        Money principal = Money.of("10000.00", "CNY");
        double rate = 5;  // 5%年利率
        double years = 3;
        
        // 简单利息
        Money simpleInterest = MoneyUtils.simpleInterest(principal, rate, years);
        System.out.println("本金: ¥" + principal.toNumberString());
        System.out.println("年利率: " + rate + "%");
        System.out.println("期限: " + years + "年");
        System.out.println("简单利息: ¥" + simpleInterest.toNumberString());
        
        // 复利
        Money compound = MoneyUtils.compoundInterest(principal, rate, years, 12);
        System.out.println("复利（月复利）本息合计: ¥" + compound.toNumberString());
        
        // 日复利
        Money dailyCompound = MoneyUtils.compoundInterest(principal, rate, years, 365);
        System.out.println("复利（日复利）本息合计: ¥" + dailyCompound.toNumberString());
        
        System.out.println();
    }
    
    /**
     * 示例9：中文大写金额
     */
    private static void example9_ChineseFormat() {
        System.out.println("--- 示例9：中文大写金额 ---");
        
        // 常见金额
        Money[] amounts = {
            Money.of("0", "CNY"),
            Money.of("1", "CNY"),
            Money.of("10", "CNY"),
            Money.of("100", "CNY"),
            Money.of("1000", "CNY"),
            Money.of("1234.56", "CNY"),
            Money.of("10000", "CNY"),
            Money.of("123456.78", "CNY"),
            Money.of("1000000", "CNY"),
            Money.of("-100.50", "CNY")
        };
        
        for (Money m : amounts) {
            System.out.println("¥" + m.toNumberString() + " → " + m.formatChinese());
        }
        
        System.out.println();
    }
    
    /**
     * 示例10：实际应用场景
     */
    private static void example10_RealWorldScenarios() {
        System.out.println("--- 示例10：实际应用场景 ---");
        
        // 场景1：购物计算
        System.out.println("\n【场景1：购物计算】");
        Money item1 = Money.of("199.00", "CNY");
        Money item2 = Money.of("59.00", "CNY");
        Money item3 = Money.of("299.00", "CNY");
        
        Money subtotal = MoneyUtils.sum(item1, item2, item3);
        Money discount = subtotal.percent(5);  // 5%折扣
        Money finalPrice = subtotal.subtract(discount);
        
        System.out.println("商品1: ¥" + item1.toNumberString());
        System.out.println("商品2: ¥" + item2.toNumberString());
        System.out.println("商品3: ¥" + item3.toNumberString());
        System.out.println("小计: ¥" + subtotal.toNumberString());
        System.out.println("会员折扣(5%): ¥-" + discount.toNumberString());
        System.out.println("实付: ¥" + finalPrice.toNumberString());
        
        // 场景2：工资计算
        System.out.println("\n【场景2：工资计算】");
        Money baseSalary = Money.of("8000.00", "CNY");
        Money bonus = Money.of("2000.00", "CNY");
        Money totalIncome = baseSalary.add(bonus);
        
        Money[] taxResult = MoneyUtils.calculateTax(totalIncome, 10, false);
        Money insurance = totalIncome.percent(8);  // 社保8%
        Money netSalary = taxResult[2].subtract(insurance);
        
        System.out.println("基本工资: ¥" + baseSalary.toNumberString());
        System.out.println("奖金: ¥" + bonus.toNumberString());
        System.out.println("总收入: ¥" + totalIncome.toNumberString());
        System.out.println("个人所得税(10%): ¥" + taxResult[1].toNumberString());
        System.out.println("社保(8%): ¥" + insurance.toNumberString());
        System.out.println("实发工资: ¥" + netSalary.toNumberString());
        
        // 场景3：国际购物
        System.out.println("\n【场景3：国际购物】");
        DefaultCurrencyConverter converter = new DefaultCurrencyConverter();
        
        Money usdPrice = Money.of("99.99", "USD");
        Money shipping = Money.of("15.00", "USD");
        Money totalUSD = usdPrice.add(shipping);
        Money totalCNY = converter.convert(totalUSD, "CNY");
        
        System.out.println("商品价格: $" + usdPrice.toNumberString());
        System.out.println("运费: $" + shipping.toNumberString());
        System.out.println("美元合计: $" + totalUSD.toNumberString());
        System.out.println("折合人民币: ¥" + totalCNY.toNumberString());
        
        // 场景4：发票金额
        System.out.println("\n【场景4：发票金额】");
        Money invoiceAmount = Money.of("123456.78", "CNY");
        System.out.println("发票金额数字: ¥" + invoiceAmount.toNumberString());
        System.out.println("发票金额大写: " + invoiceAmount.formatChinese());
        
        System.out.println("\n========================================");
        System.out.println("   示例演示完成");
        System.out.println("========================================");
    }
    
    // 辅助方法
    private static String[] formatArray(Money[] monies) {
        String[] result = new String[monies.length];
        for (int i = 0; i < monies.length; i++) {
            result[i] = monies[i].toNumberString();
        }
        return result;
    }
}