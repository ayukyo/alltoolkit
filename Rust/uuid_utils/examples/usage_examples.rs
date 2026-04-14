//! UUID 工具库使用示例
//!
//! 展示 UUID 生成、解析、验证和格式化的各种用法

use uuid_utils::{Uuid, UuidGenerator, UuidValidator, UuidFormatter, UuidFormat, UuidVersion, namespaces};

fn main() {
    println!("=== UUID 工具库使用示例 ===\n");

    // ================================
    // 1. UUID 生成
    // ================================
    println!("【1. UUID 生成】");
    
    // 生成 v4 UUID (随机)
    let uuid_v4 = Uuid::new_v4();
    println!("v4 UUID: {}", uuid_v4);
    
    // 生成 v7 UUID (基于时间戳)
    let uuid_v7 = Uuid::new_v7();
    println!("v7 UUID: {}", uuid_v7);
    
    // nil UUID
    let nil_uuid = Uuid::nil();
    println!("nil UUID: {}", nil_uuid);
    
    println!();

    // ================================
    // 2. UUID 解析
    // ================================
    println!("【2. UUID 解析】");
    
    // 标准格式
    let uuid1 = Uuid::parse("550e8400-e29b-41d4-a716-446655440000").unwrap();
    println!("标准格式: {}", uuid1);
    
    // 无连字符格式
    let uuid2 = Uuid::parse("550e8400e29b41d4a716446655440000").unwrap();
    println!("无连字符: {}", uuid2.to_string());
    
    // URN 格式
    let uuid3 = Uuid::parse("urn:uuid:550e8400-e29b-41d4-a716-446655440000").unwrap();
    println!("URN 格式: {}", uuid3.to_string());
    
    // 带花括号格式
    let uuid4 = Uuid::parse("{550e8400-e29b-41d4-a716-446655440000}").unwrap();
    println!("花括号格式: {}", uuid4.to_string());
    
    println!();

    // ================================
    // 3. UUID v3/v5 (命名空间 + 名称)
    // ================================
    println!("【3. UUID v3/v5 (确定性 UUID)】");
    
    // 使用预定义命名空间
    let uuid_v5_dns = Uuid::new_v5(&namespaces::DNS, "example.com");
    println!("v5 DNS: {}", uuid_v5_dns);
    
    let uuid_v5_url = Uuid::new_v5(&namespaces::URL, "https://example.com");
    println!("v5 URL: {}", uuid_v5_url);
    
    let uuid_v3_dns = Uuid::new_v3(&namespaces::DNS, "example.com");
    println!("v3 DNS: {}", uuid_v3_dns);
    
    // 相同输入总是产生相同 UUID
    let uuid_v5_repeat = Uuid::new_v5(&namespaces::DNS, "example.com");
    println!("v5 重复: {} (相同: {})", uuid_v5_repeat, uuid_v5_dns == uuid_v5_repeat);
    
    println!();

    // ================================
    // 4. UUID 格式化
    // ================================
    println!("【4. UUID 格式化】");
    
    let uuid = Uuid::parse("f47ac10b-58cc-4372-a567-0e02b2c3d479").unwrap();
    
    println!("标准格式: {}", UuidFormatter::format(&uuid, UuidFormat::Standard));
    println!("简单格式: {}", UuidFormatter::format(&uuid, UuidFormat::Simple));
    println!("URN 格式: {}", UuidFormatter::format(&uuid, UuidFormat::Urn));
    println!("花括号格式: {}", UuidFormatter::format(&uuid, UuidFormat::Braced));
    println!("大写格式: {}", UuidFormatter::format(&uuid, UuidFormat::Uppercase));
    
    println!();

    // ================================
    // 5. UUID 验证
    // ================================
    println!("【5. UUID 验证】");
    
    let valid_uuid = "f47ac10b-58cc-4372-a567-0e02b2c3d479";
    let invalid_uuid = "not-a-uuid";
    
    println!("验证 '{}': {}", valid_uuid, UuidValidator::is_valid(valid_uuid));
    println!("验证 '{}': {}", invalid_uuid, UuidValidator::is_valid(invalid_uuid));
    println!("是否为 nil UUID: {}", UuidValidator::is_nil("00000000-0000-0000-0000-000000000000"));
    println!("是否为 v4 UUID: {}", UuidValidator::is_v4(valid_uuid));
    
    println!();

    // ================================
    // 6. UUID 属性
    // ================================
    println!("【6. UUID 属性】");
    
    let uuid_v4 = Uuid::new_v4();
    let uuid_v7 = Uuid::new_v7();
    
    println!("v4 UUID 版本: {:?}", uuid_v4.get_version());
    println!("v7 UUID 版本: {:?}", uuid_v7.get_version());
    println!("v4 UUID 变体: {:?}", uuid_v4.get_variant());
    println!("是否为 nil: {}", uuid_v4.is_nil());
    
    // 获取原始字节
    let bytes = uuid_v4.as_bytes();
    println!("原始字节: {:?}", bytes);
    
    println!();

    // ================================
    // 7. 批量生成
    // ================================
    println!("【7. 批量生成 UUID】");
    
    let generator = UuidGenerator::new(UuidVersion::V4);
    let uuids = generator.generate_batch(5);
    
    println!("生成 5 个 v4 UUID:");
    for (i, uuid) in uuids.iter().enumerate() {
        println!("  {}: {}", i + 1, uuid);
    }
    
    // 使用 v7 生成器
    let v7_generator = UuidGenerator::new(UuidVersion::V7);
    let v7_uuids = v7_generator.generate_batch(3);
    
    println!("生成 3 个 v7 UUID:");
    for (i, uuid) in v7_uuids.iter().enumerate() {
        println!("  {}: {}", i + 1, uuid);
    }
    
    println!();

    // ================================
    // 8. 从字节创建
    // ================================
    println!("【8. 从字节创建 UUID】");
    
    let bytes: [u8; 16] = [
        0xf4, 0x7a, 0xc1, 0x0b, 0x58, 0xcc, 0x43, 0x72,
        0xa5, 0x67, 0x0e, 0x02, 0xb2, 0xc3, 0xd4, 0x79,
    ];
    
    let uuid_from_bytes = Uuid::from_bytes(bytes);
    println!("从字节创建: {}", uuid_from_bytes);
    
    let uuid_from_slice = Uuid::from_slice(&bytes).unwrap();
    println!("从切片创建: {}", uuid_from_slice);
    
    println!();

    // ================================
    // 9. 使用场景示例
    // ================================
    println!("【9. 实际使用场景】");
    
    // 场景1: 生成唯一请求 ID
    let request_id = Uuid::new_v4();
    println!("请求 ID: {}", request_id);
    
    // 场景2: 生成唯一文件名
    let filename = format!("document_{}.txt", Uuid::new_v4().to_simple_string());
    println!("唯一文件名: {}", filename);
    
    // 场景3: 数据库主键
    let user_id = Uuid::new_v7();  // v7 更适合作为主键（时间有序）
    println!("用户 ID: {}", user_id);
    
    // 场景4: URL 短链接
    let short_code = &Uuid::new_v4().to_string()[..8];
    println!("短链接代码: {}", short_code);
    
    // 场景5: 资源 URN
    let resource_urn = Uuid::new_v4().to_urn();
    println!("资源 URN: {}", resource_urn);
    
    println!();

    // ================================
    // 10. 性能测试
    // ================================
    println!("【10. 性能测试】");
    
    use std::time::Instant;
    
    // 生成 10000 个 v4 UUID
    let start = Instant::now();
    for _ in 0..10000 {
        let _ = Uuid::new_v4();
    }
    let v4_duration = start.elapsed();
    println!("生成 10000 个 v4 UUID: {:?}", v4_duration);
    
    // 生成 10000 个 v7 UUID
    let start = Instant::now();
    for _ in 0..10000 {
        let _ = Uuid::new_v7();
    }
    let v7_duration = start.elapsed();
    println!("生成 10000 个 v7 UUID: {:?}", v7_duration);
    
    // 解析 10000 个 UUID
    let uuid_str = "f47ac10b-58cc-4372-a567-0e02b2c3d479";
    let start = Instant::now();
    for _ in 0..10000 {
        let _ = Uuid::parse(uuid_str);
    }
    let parse_duration = start.elapsed();
    println!("解析 10000 个 UUID: {:?}", parse_duration);
    
    println!();
    println!("=== 示例完成 ===");
}