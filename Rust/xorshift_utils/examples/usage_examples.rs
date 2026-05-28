//! Xorshift 工具库使用示例
//!
//! 展示各种随机数生成器的用法

mod xorshift_utils;

use xorshift_utils::*;

fn main() {
    println!("=== Xorshift 工具库使用示例 ===\n");
    
    // ================================
    // 1. 基本随机数生成
    // ================================
    println!("【1. 基本随机数生成】");
    
    let mut rng = Xorshift64::new(42);
    println!("种子: 42");
    println!("随机 u64: {}", rng.next_u64());
    println!("随机 u32: {}", rng.next_u32());
    println!("随机 f64: {:.6}", rng.next_f64());
    println!("随机 f32: {:.6}", rng.next_f32());
    println!("随机布尔: {}", rng.next_bool());
    println!();
    
    // ================================
    // 2. 有界随机数
    // ================================
    println!("【2. 有界随机数】");
    
    println!("5 个 [0, 100) 范围内的随机数:");
    for i in 0..5 {
        println!("  [{:2}] {}", i + 1, rng.next_bounded(100));
    }
    
    println!("\n5 个 [-50, 50] 范围内的随机整数:");
    for i in 0..5 {
        println!("  [{:2}] {}", i + 1, rng.next_range(-50, 50));
    }
    println!();
    
    // ================================
    // 3. 不同生成器对比
    // ================================
    println!("【3. 不同生成器对比】");
    
    let seed = 42;
    let mut xor64 = Xorshift64::new(seed);
    let mut xor128 = Xorshift128::from_u64(seed);
    let mut xor128p = Xorshift128Plus::from_seed(seed);
    let mut xorwow = Xorwow::from_seed(seed);
    let mut split = SplitMix64::new(seed);
    let mut xoshiro = Xoshiro256StarStar::from_seed(seed);
    
    println!("相同种子 ({}) 下各生成器的首个值:", seed);
    println!("  Xorshift64:      {:016x}", xor64.next_u64());
    println!("  Xorshift128:     {:016x}", xor128.next_u64());
    println!("  Xorshift128+:    {:016x}", xor128p.next_u64());
    println!("  Xorwow:          {:016x}", xorwow.next_u64());
    println!("  SplitMix64:      {:016x}", split.next_u64());
    println!("  Xoshiro256**:    {:016x}", xoshiro.next_u64());
    println!();
    
    // ================================
    // 4. 数组随机排序
    // ================================
    println!("【4. 数组随机排序】");
    
    let mut numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    println!("原始数组: {:?}", numbers);
    rng.shuffle(&mut numbers);
    println!("随机排序: {:?}", numbers);
    
    let mut letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
    println!("原始数组: {:?}", letters);
    rng.shuffle(&mut letters);
    println!("随机排序: {:?}", letters);
    println!();
    
    // ================================
    // 5. 随机选择元素
    // ================================
    println!("【5. 随机选择元素】");
    
    let fruits = ["苹果", "香蕉", "樱桃", "枣", "接骨木莓"];
    println!("水果列表: {:?}", fruits);
    println!("随机选取:");
    for i in 0..5 {
        println!("  [{:2}] {}", i + 1, rng.choose(&fruits).unwrap());
    }
    println!();
    
    // ================================
    // 6. 随机字符串与 UUID
    // ================================
    println!("【6. 随机字符串与 UUID】");
    
    println!("随机字母数字字符串:");
    for length in [8, 16, 32] {
        println!("  长度 {}: {}", length, random_string(&mut rng, length));
    }
    
    println!("\n随机 UUID:");
    for i in 0..3 {
        println!("  UUID {}: {}", i + 1, random_uuid(&mut rng));
    }
    println!();
    
    // ================================
    // 7. 加权随机选择
    // ================================
    println!("【7. 加权随机选择】");
    
    let items = ["普通", "罕见", "稀有", "传说"];
    let weights = [50.0, 30.0, 15.0, 5.0]; // 50%, 30%, 15%, 5%
    
    println!("物品及其权重:");
    for (item, weight) in items.iter().zip(weights.iter()) {
        println!("  {} - {:.0}%", item, weight);
    }
    
    // 模拟 100 次抽取
    let mut counts = [0; 4];
    for _ in 0..100 {
        let idx = weighted_choice(&mut rng, &weights);
        counts[idx] += 1;
    }
    
    println!("\n100 次抽取结果:");
    for (item, count) in items.iter().zip(counts.iter()) {
        println!("  {} - {} 次", item, count);
    }
    println!();
    
    // ================================
    // 8. 统计分布
    // ================================
    println!("【8. 统计分布】");
    
    println!("高斯分布 (均值=50, 标准差=10):");
    let gaussians: Vec<f64> = (0..10).map(|_| gaussian(&mut rng, 50.0, 10.0)).collect();
    println!("  {:?}", gaussians);
    
    println!("\n泊松分布 (λ=5):");
    let poissons: Vec<u64> = (0..10).map(|_| poisson(&mut rng, 5.0)).collect();
    println!("  {:?}", poissons);
    
    println!("\n指数分布 (λ=0.5):");
    let exps: Vec<f64> = (0..10).map(|_| exponential(&mut rng, 0.5)).collect();
    println!("  {:?}", exps);
    println!();
    
    // ================================
    // 9. 并行友好的 SplitMix64
    // ================================
    println!("【9. 并行友好的 SplitMix64】");
    
    let mut rng = SplitMix64::new(42);
    
    println!("拆分生成器用于并行计算:");
    let mut child1 = rng.split();
    let mut child2 = rng.split();
    let mut child3 = rng.split();
    
    println!("  主线程: {:016x}", rng.next_u64());
    println!("  子线程1: {:016x}", child1.next_u64());
    println!("  子线程2: {:016x}", child2.next_u64());
    println!("  子线程3: {:016x}", child3.next_u64());
    
    println!("\n各子线程产生独立的随机流:");
    println!("  子线程1: {:016x} {:016x} {:016x}", 
        child1.next_u64(), child1.next_u64(), child1.next_u64());
    println!("  子线程2: {:016x} {:016x} {:016x}", 
        child2.next_u64(), child2.next_u64(), child2.next_u64());
    println!();
    
    // ================================
    // 10. Xoshiro256** 跳跃功能
    // ================================
    println!("【10. Xoshiro256** 跳跃功能】");
    
    let mut rng1 = Xoshiro256StarStar::from_seed(42);
    let mut rng2 = Xoshiro256StarStar::from_seed(42);
    let mut rng3 = Xoshiro256StarStar::from_seed(42);
    
    // jump() 跳跃 2^128 步
    rng2.jump();
    rng3.jump();
    rng3.jump();
    
    println!("同一种子产生的三个并行随机流:");
    println!("  流1 (无跳跃): {:016x}", rng1.next_u64());
    println!("  流2 (跳跃1次): {:016x}", rng2.next_u64());
    println!("  流3 (跳跃2次): {:016x}", rng3.next_u64());
    println!();
    
    // ================================
    // 11. 快速单次随机数
    // ================================
    println!("【11. 快速单次随机数】");
    
    println!("无需创建结构体的单次随机数:");
    println!("  quick_u64(42)   = {}", quick_u64(42));
    println!("  quick_f64(123)  = {:.6}", quick_f64(123));
    println!("  quick_range(999, 0, 100) = {}", quick_range(999, 0, 100));
    
    println!("\n不同种子产生不同值:");
    for seed in [1, 2, 3, 4, 5] {
        println!("  种子 {}: {}", seed, quick_u64(seed));
    }
    println!();
    
    // ================================
    // 12. 骰子模拟
    // ================================
    println!("【12. 骰子模拟】");
    
    println!("掷骰子:");
    for i in 0..10 {
        let d6 = rng.next_bounded(6) + 1;
        let d20 = rng.next_bounded(20) + 1;
        let d100 = rng.next_bounded(100) + 1;
        println!("  第{:2}次: D6={}, D20={}, D100={}", i + 1, d6, d20, d100);
    }
    println!();
    
    // ================================
    // 13. 硬币翻转模拟
    // ================================
    println!("【13. 硬币翻转模拟】");
    
    let flips = 1000;
    let heads = (0..flips).filter(|_| rng.next_bool()).count();
    let tails = flips - heads;
    
    println!("{} 次硬币翻转:", flips);
    println!("  正面: {} ({:.1}%)", heads, heads as f64 / flips as f64 * 100.0);
    println!("  反面: {} ({:.1}%)", tails, tails as f64 / flips as f64 * 100.0);
    println!();
    
    // ================================
    // 14. 随机字节
    // ================================
    println!("【14. 随机字节】");
    
    let mut buf = [0u8; 16];
    rng.fill_bytes(&mut buf);
    
    println!("16 个随机字节: {:02x?}", buf);
    
    // 转换为十六进制字符串
    let hex = buf.iter()
        .map(|b| format!("{:02x}", b))
        .collect::<String>();
    println!("作为十六进制字符串: {}", hex);
    println!();
    
    // ================================
    // 15. 可重复模拟
    // ================================
    println!("【15. 可重复模拟】");
    
    let seed = 2024;
    
    // 运行1
    let mut rng1 = Xorshift64::new(seed);
    let results1: Vec<u64> = (0..5).map(|_| rng1.next_bounded(1000)).collect();
    
    // 运行2 使用相同种子
    let mut rng2 = Xorshift64::new(seed);
    let results2: Vec<u64> = (0..5).map(|_| rng2.next_bounded(1000)).collect();
    
    println!("运行1 (种子 {}): {:?}", seed, results1);
    println!("运行2 (种子 {}): {:?}", seed, results2);
    println!("结果相同: {}", results1 == results2);
    println!();
    
    println!("=== 所有示例完成 ===");
}