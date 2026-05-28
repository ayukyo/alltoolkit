//! Count-Min Sketch 使用示例
//! 
//! 运行方式: rustc --edition 2021 main.rs mod.rs -o cms_demo && ./cms_demo

use std::hash::Hash;
use std::collections::hash_map::DefaultHasher;
use std::hash::Hasher;
use std::cmp::Reverse;

// 重新导出 mod.rs 中的结构（需要手动复制 mod.rs 内容或使用 cargo）

fn main() {
    println!("=== Count-Min Sketch 示例 ===\n");
    println!("请使用 cargo 运行此示例:");
    println!("  cd Rust/count_min_sketch_utils");
    println!("  cargo init --name count_min_sketch");
    println!("  cargo run --example demo");
    println!();
    println!("或直接测试:");
    println!("  rustc --test mod.rs -o test_binary && ./test_binary");
    println!();
    println!("模块已实现以下功能:");
    println!("  - CountMinSketch: 频率估计数据结构");
    println!("  - HeavyHitters: 高频元素追踪器");
    println!("  - FrequencyCounter: 频率计数器");
    println!("  - SketchStats: 统计信息");
}