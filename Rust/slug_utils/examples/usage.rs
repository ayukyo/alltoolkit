//! Slug Utils 使用示例
//!
//! 运行方式: cargo run --example usage

use slug_utils::{slugify, slugify_with_separator, slugify_with_max_length, 
                 slugify_filename, slugify_batch, SlugGenerator, SlugOptions};

fn main() {
    println!("=== Slug Utils 使用示例 ===\n");
    
    // 1. 基本用法
    println!("1. 基本 slug 生成:");
    println!("   'Hello World' -> '{}'", slugify("Hello World"));
    println!("   'This is a Test' -> '{}'", slugify("This is a Test"));
    println!("   'Multiple   Spaces' -> '{}'", slugify("Multiple   Spaces"));
    println!();
    
    // 2. 特殊字符处理
    println!("2. 特殊字符处理:");
    println!("   'Hello@World!' -> '{}'", slugify("Hello@World!"));
    println!("   'Test#123$%%^' -> '{}'", slugify("Test#123$%^"));
    println!("   'Under_Score-Text' -> '{}'", slugify("Under_Score-Text"));
    println!();
    
    // 3. 中文支持
    println!("3. 中文支持:");
    println!("   '中文标题' -> '{}'", slugify("中文标题"));
    println!("   '测试开发环境' -> '{}'", slugify("测试开发环境"));
    println!("   '欢迎使用Rust' -> '{}'", slugify("欢迎使用Rust"));
    println!("   '程序设计与算法' -> '{}'", slugify("程序设计与算法"));
    println!();
    
    // 4. 自定义分隔符
    println!("4. 自定义分隔符:");
    println!("   'Hello World' (下划线) -> '{}'", 
             slugify_with_separator("Hello World", "_"));
    println!("   'Test Case' (点号) -> '{}'", 
             slugify_with_separator("Test Case", "."));
    println!();
    
    // 5. 最大长度限制
    println!("5. 最大长度限制:");
    println!("   'This is a very long string' (限制10字符) -> '{}'", 
             slugify_with_max_length("This is a very long string", 10));
    println!("   'Hello World Example' (限制15字符) -> '{}'", 
             slugify_with_max_length("Hello World Example", 15));
    println!();
    
    // 6. 保留大小写
    println!("6. 保留大小写:");
    let options = SlugOptions {
        lowercase: false,
        ..Default::default()
    };
    let gen = SlugGenerator::new(options);
    println!("   'Hello World' -> '{}'", gen.slugify("Hello World"));
    println!("   'Test CASE Example' -> '{}'", gen.slugify("Test CASE Example"));
    println!();
    
    // 7. 去除停用词
    println!("7. 去除停用词:");
    let options = SlugOptions {
        remove_stop_words: true,
        ..Default::default()
    };
    let gen = SlugGenerator::new(options);
    println!("   'The Quick Brown Fox' -> '{}'", gen.slugify("The Quick Brown Fox"));
    println!("   'A Day in the Life' -> '{}'", gen.slugify("A Day in the Life"));
    println!();
    
    // 8. 不保留数字
    println!("8. 不保留数字:");
    let options = SlugOptions {
        keep_numbers: false,
        ..Default::default()
    };
    let gen = SlugGenerator::new(options);
    println!("   'Test123Case456' -> '{}'", gen.slugify("Test123Case456"));
    println!("   '2024 Year Report' -> '{}'", gen.slugify("2024 Year Report"));
    println!();
    
    // 9. 文件名处理
    println!("9. 文件名处理:");
    println!("   'My Document.pdf' -> '{}'", slugify_filename("My Document.pdf"));
    println!("   'report_2024.xlsx' -> '{}'", slugify_filename("report_2024.xlsx"));
    println!("   'image (1).png' -> '{}'", slugify_filename("image (1).png"));
    println!();
    
    // 10. 批量处理
    println!("10. 批量处理:");
    let inputs = vec!["First Article", "Second Post", "Third Entry"];
    let results = slugify_batch(&inputs);
    for (input, output) in inputs.iter().zip(results.iter()) {
        println!("    '{}' -> '{}'", input, output);
    }
    println!();
    
    // 11. 唯一 Slug 生成
    println!("11. 唯一 Slug 生成:");
    let gen = SlugGenerator::default();
    let existing: Vec<String> = vec!["hello-world".to_string()];
    println!("   已存在: {:?}", existing);
    println!("   新 'Hello World' -> '{}'", gen.unique_slug("Hello World", &existing));
    
    let existing2: Vec<String> = vec!["hello-world".to_string(), "hello-world-1".to_string()];
    println!("   已存在: {:?}", existing2);
    println!("   新 'Hello World' -> '{}'", gen.unique_slug("Hello World", &existing2));
    println!();
    
    // 12. 组合配置
    println!("12. 组合配置示例:");
    let options = SlugOptions {
        separator: "_".to_string(),
        lowercase: true,
        max_length: 20,
        remove_stop_words: true,
        keep_numbers: true,
    };
    let gen = SlugGenerator::new(options);
    println!("   'The Quick Brown 2024' -> '{}'", gen.slugify("The Quick Brown 2024"));
    println!("   'A Long Title For An Article' -> '{}'", 
             gen.slugify("A Long Title For An Article"));
    println!();
    
    // 13. 实际应用场景
    println!("13. 实际应用场景:");
    
    // 博客文章 URL
    println!("   博客文章: '如何学习Rust编程' -> '{}'", slugify("如何学习Rust编程"));
    
    // 产品名称
    println!("   产品名称: 'iPhone 15 Pro Max' -> '{}'", slugify("iPhone 15 Pro Max"));
    
    // 用户名
    println!("   用户名: 'John.Doe@Example' -> '{}'", slugify("John.Doe@Example"));
    
    // 标签
    println!("   标签: 'Rust Programming' -> '{}'", slugify("Rust Programming"));
    
    // 分类
    println!("   分类: '技术文章/编程/Rust' -> '{}'", slugify("技术文章/编程/Rust"));
    println!();
    
    // 14. 边缘情况处理
    println!("14. 边缘情况处理:");
    println!("   空字符串 -> '{}'", slugify(""));
    println!("   只有特殊字符 '@#$%%^' -> '{}'", slugify("@#$%^"));
    println!("   连续分隔符 'a---b' -> '{}'", slugify("a---b"));
    println!("   首尾分隔符 '---hello---' -> '{}'", slugify("---hello---"));
    println!();
    
    println!("=== 示例完成 ===");
}