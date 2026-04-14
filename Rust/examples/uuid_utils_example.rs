/// Example usage of uuid_utils module
///
/// Run with: rustc --edition 2021 uuid_utils_example.rs -L ../uuid_utils && ./uuid_utils_example

mod uuid_utils;

use uuid_utils::{Uuid, UuidGenerator, UuidValidator, UuidFormatter, UuidFormat, UuidVersion, namespaces};

fn main() {
    println!("=== AllToolkit UUID Utilities Demo ===\n");

    // 1. UUID 生成
    println!("1. UUID Generation:");
    let uuid_v4 = Uuid::new_v4();
    println!("   v4 UUID: {}", uuid_v4);
    let uuid_v7 = Uuid::new_v7();
    println!("   v7 UUID: {}", uuid_v7);
    let nil_uuid = Uuid::nil();
    println!("   nil UUID: {}", nil_uuid);
    println!();

    // 2. UUID 解析
    println!("2. UUID Parsing:");
    let parsed = Uuid::parse("f47ac10b-58cc-4372-a567-0e02b2c3d479").unwrap();
    println!("   Parsed: {}", parsed);
    println!("   Version: {:?}", parsed.get_version());
    println!();

    // 3. UUID v3/v5 (命名空间)
    println!("3. UUID v3/v5 with Namespace:");
    let uuid_v5 = Uuid::new_v5(&namespaces::DNS, "example.com");
    println!("   v5 DNS/example.com: {}", uuid_v5);
    let uuid_v3 = Uuid::new_v3(&namespaces::DNS, "example.com");
    println!("   v3 DNS/example.com: {}", uuid_v3);
    println!();

    // 4. UUID 格式化
    println!("4. UUID Formatting:");
    let uuid = Uuid::parse("f47ac10b-58cc-4372-a567-0e02b2c3d479").unwrap();
    println!("   Standard: {}", UuidFormatter::format(&uuid, UuidFormat::Standard));
    println!("   Simple: {}", UuidFormatter::format(&uuid, UuidFormat::Simple));
    println!("   URN: {}", UuidFormatter::format(&uuid, UuidFormat::Urn));
    println!("   Braced: {}", UuidFormatter::format(&uuid, UuidFormat::Braced));
    println!("   Uppercase: {}", UuidFormatter::format(&uuid, UuidFormat::Uppercase));
    println!();

    // 5. UUID 验证
    println!("5. UUID Validation:");
    println!("   Valid: {}", UuidValidator::is_valid("f47ac10b-58cc-4372-a567-0e02b2c3d479"));
    println!("   Invalid: {}", UuidValidator::is_valid("not-a-uuid"));
    println!("   Is nil: {}", UuidValidator::is_nil("00000000-0000-0000-0000-000000000000"));
    println!("   Is v4: {}", UuidValidator::is_v4("f47ac10b-58cc-4372-a567-0e02b2c3d479"));
    println!();

    // 6. 批量生成
    println!("6. Batch Generation:");
    let generator = UuidGenerator::new(UuidVersion::V4);
    let uuids = generator.generate_batch(3);
    println!("   Generated 3 v4 UUIDs:");
    for (i, u) in uuids.iter().enumerate() {
        println!("      {}: {}", i + 1, u);
    }
    println!();

    // 7. 实际使用场景
    println!("7. Practical Usage:");
    println!("   Request ID: {}", Uuid::new_v4());
    println!("   Unique filename: document_{}.txt", Uuid::new_v4().to_simple_string());
    println!("   User ID (v7): {}", Uuid::new_v7());
    println!("   Resource URN: {}", Uuid::new_v4().to_urn());
    println!();

    println!("=== Demo Complete ===");
}