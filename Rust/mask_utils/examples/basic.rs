//! # Mask Utils 基本使用示例
//! 
//! 演示如何使用 mask_utils 进行各种数据脱敏操作

use mask_utils::*;

fn main() {
    println!("=== Mask Utils 示例 ===\n");
    
    // 1. 手机号脱敏
    println!("📱 手机号脱敏:");
    println!("  13812345678 -> {}", mask_phone("13812345678"));
    println!("  15987654321 -> {}", mask_phone("15987654321"));
    println!("  国际号码 +8613812345678 -> {}", mask_phone("+8613812345678"));
    
    // 2. 邮箱脱敏
    println!("\n📧 邮箱脱敏:");
    println!("  example@domain.com -> {}", mask_email("example@domain.com"));
    println!("  test@gmail.com -> {}", mask_email("test@gmail.com"));
    println!("  a@b.com -> {}", mask_email("a@b.com"));
    
    // 3. 身份证号脱敏
    println!("\n🪪 身份证号脱敏:");
    println!("  11010519900307888X -> {}", mask_id_card("11010519900307888X"));
    println!("  110105199003078 -> {}", mask_id_card("110105199003078"));
    
    // 4. 银行卡号脱敏
    println!("\n💳 银行卡号脱敏:");
    println!("  6222021234567890123 -> {}", mask_bank_card("6222021234567890123"));
    println!("  6222 0212 3456 7890 -> {}", mask_bank_card("6222 0212 3456 7890"));
    
    // 5. 姓名脱敏
    println!("\n👤 姓名脱敏:");
    println!("  张三 -> {}", mask_name("张三"));
    println!("  王小明 -> {}", mask_name("王小明"));
    println!("  欧阳修 -> {}", mask_name("欧阳修"));
    println!("  John -> {}", mask_name("John"));
    println!("  Alice -> {}", mask_name("Alice"));
    
    // 6. IP地址脱敏
    println!("\n🌐 IP地址脱敏:");
    println!("  192.168.1.100 -> {}", mask_ip("192.168.1.100"));
    println!("  10.0.0.1 -> {}", mask_ip("10.0.0.1"));
    println!("  2001:0db8:85a3::8a2e:0370:7334 -> {}", mask_ip("2001:0db8:85a3::8a2e:0370:7334"));
    
    // 7. 自定义脱敏规则
    println!("\n🔧 自定义脱敏规则:");
    println!("  abcdef123456 (前3后4) -> {}", mask_custom("abcdef123456", 3, 4));
    println!("  abcdef123456 (前2后2) -> {}", mask_custom("abcdef123456", 2, 2));
    
    // 8. 按长度智能脱敏
    println!("\n📏 按长度智能脱敏:");
    println!("  a (长度1) -> {}", mask_by_length("a"));
    println!("  ab (长度2) -> {}", mask_by_length("ab"));
    println!("  abc (长度3) -> {}", mask_by_length("abc"));
    println!("  abcdef (长度6) -> {}", mask_by_length("abcdef"));
    println!("  abcdefghijk (长度11) -> {}", mask_by_length("abcdefghijk"));
    
    // 9. 完全脱敏
    println!("\n🔒 完全脱敏:");
    println!("  password123 -> {}", mask_all("password123"));
    println!("  secret -> {}", mask_all_with_char("secret", '#'));
    
    // 10. 批量脱敏
    println!("\n📦 批量脱敏:");
    let phones = vec!["13812345678", "15987654321", "18611112222"];
    let masked = batch_mask(&phones, MaskType::Phone);
    println!("  原始: {:?}", phones);
    println!("  脱敏: {:?}", masked);
    
    // 11. 使用 MaskMapper 进行映射脱敏
    println!("\n🗺️ MaskMapper 映射脱敏:");
    let mut mapper = MaskMapper::new();
    mapper
        .add("phone", MaskType::Phone)
        .add("email", MaskType::Email)
        .add("id_card", MaskType::IdCard)
        .add("bank_card", MaskType::BankCard)
        .add("name", MaskType::Name);
    
    let mut data = std::collections::HashMap::new();
    data.insert("phone".to_string(), "13812345678".to_string());
    data.insert("email".to_string(), "user@example.com".to_string());
    data.insert("id_card".to_string(), "11010519900307888X".to_string());
    data.insert("bank_card".to_string(), "6222021234567890123".to_string());
    data.insert("name".to_string(), "张三".to_string());
    
    let masked_data = mapper.mask_map(&data);
    println!("  原始数据:");
    for (k, v) in &data {
        println!("    {}: {}", k, v);
    }
    println!("  脱敏数据:");
    for (k, v) in &masked_data {
        println!("    {}: {}", k, v);
    }
    
    // 12. JSON字段脱敏
    println!("\n📄 JSON字段脱敏:");
    let json = r#"{
    "name": "张三",
    "phone": "13812345678",
    "email": "zhangsan@example.com",
    "id_card": "11010519900307888X"
}"#;
    
    let config = JsonMaskConfig::new()
        .with_field("phone")
        .with_field("email")
        .with_mask_type(MaskType::Phone);
    
    let masked_json = mask_json(json, &config);
    println!("  原始: {}", json.replace('\n', "").replace("    ", ""));
    println!("  脱敏: {}", masked_json.replace('\n', "").replace("    ", ""));
    
    println!("\n✅ 示例演示完成!");
}