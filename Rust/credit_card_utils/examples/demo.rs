//! 信用卡工具库使用示例
//!
//! 演示如何使用 credit_card_utils 进行信用卡验证和处理

use credit_card_utils::*;

fn main() {
    println!("=== 信用卡工具库演示 ===\n");

    // 1. 基本验证
    println!("1. 基本卡号验证");
    println!("{}", "-".repeat(40));
    
    let cards = vec![
        ("4111111111111111", "Visa 测试卡"),
        ("5555555555554444", "MasterCard 测试卡"),
        ("378282246310005", "American Express 测试卡"),
        ("6011111111111117", "Discover 测试卡"),
        ("3530111333300000", "JCB 测试卡"),
    ];

    for (number, desc) in cards {
        let card = CreditCard::new(number);
        println!("{} ({})", desc, number);
        println!("  品牌: {}", card.brand());
        println!("  有效: {}", if card.is_valid() { "✓" } else { "✗" });
        println!("  格式化: {}", card.format());
        println!("  掩码 (后4位): {}", card.mask_last4());
        println!("  掩码 (中间): {}", card.mask_middle());
        println!("  BIN: {}", card.bin().unwrap_or("N/A"));
        println!("  测试卡: {}", if card.is_test_card() { "是" } else { "否" });
        println!();
    }

    // 2. 使用验证器
    println!("2. 详细验证结果");
    println!("{}", "-".repeat(40));
    
    let test_numbers = vec![
        "4111111111111111",
        "4111111111111112", // 错误的校验位
        "1234567890123456", // 无效卡号
        "5555555555554444",
    ];

    for number in test_numbers {
        let result = CreditCardValidator::validate(number);
        println!("卡号: {}", number);
        println!("  有效: {}", if result.valid { "✓" } else { "✗" });
        println!("  品牌: {}", result.brand);
        println!("  格式化: {}", result.formatted);
        if !result.errors.is_empty() {
            println!("  错误: {:?}", result.errors);
        }
        if !result.warnings.is_empty() {
            println!("  警告: {:?}", result.warnings);
        }
        println!();
    }

    // 3. 有效期和 CVV 验证
    println!("3. 有效期和 CVV 验证");
    println!("{}", "-".repeat(40));
    
    let expiries = vec!["12/25", "01/30", "13/25", "00/25"];
    for exp in expiries {
        let valid = CreditCardValidator::validate_expiry(exp);
        println!("有效期 {}: {}", exp, if valid { "有效" } else { "无效" });
    }
    println!();

    let cvvs = vec![
        ("123", CardBrand::Visa),
        ("1234", CardBrand::Visa),
        ("1234", CardBrand::Amex),
        ("12", CardBrand::Visa),
    ];
    for (cvv, brand) in cvvs {
        let valid = CreditCardValidator::validate_cvv(cvv, brand);
        println!("CVV {} ({}): {}", cvv, brand, if valid { "有效" } else { "无效" });
    }
    println!();

    // 4. 生成测试卡号
    println!("4. 生成测试卡号");
    println!("{}", "-".repeat(40));
    
    println!("Visa:       {}", CreditCardGenerator::generate_visa());
    println!("MasterCard: {}", CreditCardGenerator::generate_mastercard());
    println!("Amex:       {}", CreditCardGenerator::generate_amex());
    println!("Discover:   {}", CreditCardGenerator::generate_discover());
    println!();

    // 5. 卡品牌检测
    println!("5. 卡品牌检测");
    println!("{}", "-".repeat(40));
    
    let test_prefixes = vec![
        "4111111111111111", // Visa
        "5500000000000004", // MasterCard
        "340000000000009", // Amex
        "6011000000000004", // Discover
        "6225881234567890", // UnionPay
        "2200123456789012", // Mir
    ];

    for number in test_prefixes {
        let brand = CreditCardValidator::detect_brand(number);
        println!("{} → {}", number, brand);
    }
    println!();

    // 6. Luhn 算法演示
    println!("6. Luhn 算法验证");
    println!("{}", "-".repeat(40));
    
    let numbers = vec![
        "4111111111111111", // 有效
        "49927398716",      // 有效
        "49927398717",      // 无效
        "1234567812345670", // 有效
    ];

    for number in numbers {
        let valid = CreditCardValidator::check_luhn(number);
        println!("{} → {}", number, if valid { "✓ 有效" } else { "✗ 无效" });
    }
}