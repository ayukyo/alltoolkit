//! Sparse Set 使用示例
//!
//! 展示稀疏集合的各种用法

use sparse_set_utils::SparseSet;

fn main() {
    println!("=== Sparse Set 稀疏集合示例 ===\n");

    // 1. 基本操作
    println!("1. 基本操作");
    let mut set = SparseSet::new(100);
    println!("   创建容量为 100 的空集合");
    
    set.insert(5);
    set.insert(10);
    set.insert(42);
    println!("   插入元素: 5, 10, 42");
    println!("   集合大小: {}", set.len());
    println!("   包含 5? {}", set.contains(&5));
    println!("   包含 99? {}", set.contains(&99));
    
    set.remove(&10);
    println!("   删除 10 后，大小: {}", set.len());
    println!();

    // 2. 遍历元素
    println!("2. 遍历元素");
    let mut set2 = SparseSet::new(100);
    for i in 1..=5 {
        set2.insert(i);
    }
    println!("   集合内容: {:?}", set2.to_vec());
    println!("   元素和: {}", set2.iter().sum::<usize>());
    println!();

    // 3. 条件过滤
    println!("3. 条件过滤 (保留偶数)");
    let mut set3 = SparseSet::new(100);
    for i in 1..=10 {
        set3.insert(i);
    }
    println!("   过滤前: {:?}", set3.to_vec());
    set3.retain(|&x| x % 2 == 0);
    println!("   过滤后: {:?}", set3.to_vec());
    println!();

    // 4. 集合运算
    println!("4. 集合运算");
    let mut a = SparseSet::new(100);
    let mut b = SparseSet::new(100);
    
    a.insert(1);
    a.insert(2);
    a.insert(3);
    
    b.insert(2);
    b.insert(3);
    b.insert(4);
    
    println!("   集合 A: {:?}", a.to_vec());
    println!("   集合 B: {:?}", b.to_vec());
    println!("   A ∩ B (交集): {:?}", a.intersection(&b).to_vec());
    println!("   A ∪ B (并集): {:?}", a.union(&b).to_vec());
    println!("   A - B (差集): {:?}", a.difference(&b).to_vec());
    println!("   A △ B (对称差): {:?}", a.symmetric_difference(&b).to_vec());
    println!();

    // 5. 子集判断
    println!("5. 子集判断");
    let mut subset = SparseSet::new(100);
    subset.insert(2);
    subset.insert(3);
    println!("   子集 {:?} 是 A 的子集? {}", subset.to_vec(), subset.is_subset(&a));
    println!();

    // 6. 从迭代器创建
    println!("6. 从迭代器创建");
    let set4: SparseSet = vec![10, 20, 30, 40, 50].into_iter().collect();
    println!("   从 vec 创建: {:?}", set4.to_vec());
    println!();

    // 7. 自动扩展容量
    println!("7. 自动扩展容量");
    let mut small_set = SparseSet::new(10);
    println!("   初始容量: {}", small_set.capacity());
    small_set.insert(100); // 超出初始容量
    println!("   插入 100 后容量: {}", small_set.capacity());
    println!("   包含 100? {}", small_set.contains(&100));
    println!();

    // 8. 性能测试
    println!("8. 性能演示 (10000 个元素)");
    use std::time::Instant;
    
    let mut perf_set = SparseSet::new(20000);
    
    let start = Instant::now();
    for i in 0..10000 {
        perf_set.insert(i);
    }
    let insert_time = start.elapsed();
    
    let start = Instant::now();
    for i in 0..10000 {
        assert!(perf_set.contains(&i));
    }
    let lookup_time = start.elapsed();
    
    let start = Instant::now();
    for i in 0..10000 {
        perf_set.remove(&i);
    }
    let remove_time = start.elapsed();
    
    println!("   插入 10000 元素: {:?}", insert_time);
    println!("   查找 10000 元素: {:?}", lookup_time);
    println!("   删除 10000 元素: {:?}", remove_time);
    println!();

    println!("=== 示例完成 ===");
}