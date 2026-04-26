//! 一致性哈希使用示例
//! 
//! 演示如何在分布式系统中使用一致性哈希

use consistent_hash_utils::{ConsistentHash, WeightedConsistentHash};

fn main() {
    println!("=== 一致性哈希工具示例 ===\n");
    
    // 示例 1: 基本使用
    basic_usage();
    
    // 示例 2: 负载分布分析
    distribution_analysis();
    
    // 示例 3: 动态节点管理
    dynamic_nodes();
    
    // 示例 4: 数据复制
    data_replication();
    
    // 示例 5: 加权一致性哈希
    weighted_hash();
    
    // 示例 6: 分布式缓存场景
    distributed_cache_scenario();
}

/// 基本使用示例
fn basic_usage() {
    println!("--- 示例 1: 基本使用 ---");
    
    let mut ch = ConsistentHash::new(150);
    
    // 添加缓存服务器节点
    ch.add_node("cache-server-1".to_string());
    ch.add_node("cache-server-2".to_string());
    ch.add_node("cache-server-3".to_string());
    
    println!("已添加 {} 个节点", ch.node_count());
    println!("虚拟节点总数: {}", ch.virtual_node_count());
    
    // 查找键对应的服务器
    let keys = vec!["user:1001", "user:1002", "product:500", "order:12345"];
    
    for key in keys {
        let node = ch.get_node(key).unwrap();
        println!("键 '{}' -> 节点 '{}'", key, node);
    }
    
    println!();
}

/// 负载分布分析
fn distribution_analysis() {
    println!("--- 示例 2: 负载分布分析 ---");
    
    let mut ch = ConsistentHash::new(200);
    ch.add_node("server-a".to_string());
    ch.add_node("server-b".to_string());
    ch.add_node("server-c".to_string());
    ch.add_node("server-d".to_string());
    
    // 生成 10000 个键
    let keys: Vec<String> = (0..10000).map(|i| format!("key_{:05}", i)).collect();
    let key_refs: Vec<&str> = keys.iter().map(|s| s.as_str()).collect();
    
    let dist = ch.distribution(&key_refs);
    
    println!("负载分布 (10000 个键):");
    let mut total = 0;
    for (node, count) in &dist {
        let percentage = (*count as f64 / 10000.0) * 100.0;
        println!("  {}: {} 个键 ({:.1}%)", node, count, percentage);
        total += count;
    }
    println!("  总计: {} 个键", total);
    
    // 计算标准差
    let values: Vec<f64> = dist.values().map(|&v| v as f64).collect();
    let mean = values.iter().sum::<f64>() / values.len() as f64;
    let variance: f64 = values.iter().map(|v| (v - mean).powi(2)).sum::<f64>() / values.len() as f64;
    let std_dev = variance.sqrt();
    println!("  标准差: {:.2}", std_dev);
    println!("  变异系数: {:.2}%", (std_dev / mean) * 100.0);
    
    println!();
}

/// 动态节点管理
fn dynamic_nodes() {
    println!("--- 示例 3: 动态节点管理 ---");
    
    let mut ch = ConsistentHash::new(150);
    ch.add_node("node-1".to_string());
    ch.add_node("node-2".to_string());
    
    // 记录原始分配
    let test_keys: Vec<String> = (0..100).map(|i| format!("test-key-{}", i)).collect();
    let test_key_refs: Vec<&str> = test_keys.iter().map(|s| s.as_str()).collect();
    
    println!("初始状态 (2 个节点):");
    let dist_initial = ch.distribution(&test_key_refs);
    for (node, count) in &dist_initial {
        println!("  {}: {} 个键", node, count);
    }
    
    // 添加新节点
    println!("\n添加 node-3...");
    ch.add_node("node-3".to_string());
    
    let dist_after_add = ch.distribution(&test_key_refs);
    println!("添加后分布:");
    for (node, count) in &dist_after_add {
        println!("  {}: {} 个键", node, count);
    }
    
    // 移除节点
    println!("\n移除 node-2...");
    ch.remove_node("node-2");
    
    let dist_after_remove = ch.distribution(&test_key_refs);
    println!("移除后分布:");
    for (node, count) in &dist_after_remove {
        println!("  {}: {} 个键", node, count);
    }
    
    println!();
}

/// 数据复制场景
fn data_replication() {
    println!("--- 示例 4: 数据复制 ---");
    
    let mut ch = ConsistentHash::new(150);
    ch.add_node("replica-1".to_string());
    ch.add_node("replica-2".to_string());
    ch.add_node("replica-3".to_string());
    ch.add_node("replica-4".to_string());
    ch.add_node("replica-5".to_string());
    
    // 获取数据的主副本和从副本
    let key = "important-data:12345";
    let replicas = ch.get_nodes(key, 3); // 3 个副本
    
    println!("键 '{}' 的副本分布:", key);
    for (i, node) in replicas.iter().enumerate() {
        match i {
            0 => println!("  主副本: {}", node),
            _ => println!("  从副本 {}: {}", i, node),
        }
    }
    
    // 确保副本在不同节点上
    println!("\n多个键的副本分布:");
    for key in &["data:a", "data:b", "data:c"] {
        let nodes = ch.get_nodes(*key, 3);
        println!("  {}: {:?}", key, nodes);
    }
    
    println!();
}

/// 加权一致性哈希
fn weighted_hash() {
    println!("--- 示例 5: 加权一致性哈希 ---");
    
    let mut wch = WeightedConsistentHash::new(100);
    
    // 不同配置的服务器
    wch.add_node("small-server".to_string(), 1);   // 1x 权重
    wch.add_node("medium-server".to_string(), 2);  // 2x 权重
    wch.add_node("large-server".to_string(), 4);   // 4x 权重
    
    println!("服务器权重配置:");
    println!("  small-server: 权重 1 (2核 4GB)");
    println!("  medium-server: 权重 2 (4核 8GB)");
    println!("  large-server: 权重 4 (8核 16GB)");
    
    // 统计分布
    let mut counts: std::collections::HashMap<String, usize> = std::collections::HashMap::new();
    for i in 0..10000 {
        if let Some(node) = wch.get_node(&format!("request-{}", i)) {
            *counts.entry(node).or_insert(0) += 1;
        }
    }
    
    println!("\n请求分布 (10000 次请求):");
    let total = counts.values().sum::<usize>();
    for node in &["small-server", "medium-server", "large-server"] {
        let count = counts.get(*node).copied().unwrap_or(0);
        let percentage = (count as f64 / total as f64) * 100.0;
        println!("  {}: {} ({:.1}%)", node, count, percentage);
    }
    
    println!();
}

/// 分布式缓存场景
fn distributed_cache_scenario() {
    println!("--- 示例 6: 分布式缓存场景 ---");
    
    // 模拟一个分布式缓存系统
    let mut cache_cluster = ConsistentHash::new(200);
    
    // 初始集群配置
    cache_cluster.add_nodes(vec![
        "redis-01",
        "redis-02", 
        "redis-03",
    ]);
    
    println!("缓存集群初始化完成，节点: {:?}", cache_cluster.get_nodes_list());
    
    // 用户数据分布
    let user_ids: Vec<String> = (1000..1100).map(|i| format!("user:{}", i)).collect();
    let user_id_refs: Vec<&str> = user_ids.iter().map(|s| s.as_str()).collect();
    
    println!("\n用户数据分布:");
    let user_dist = cache_cluster.distribution(&user_id_refs);
    for (node, count) in &user_dist {
        println!("  {}: {} 个用户", node, count);
    }
    
    // 扩容场景
    println!("\n>>> 扩容: 添加 redis-04");
    cache_cluster.add_node("redis-04".to_string());
    
    let user_dist_after = cache_cluster.distribution(&user_id_refs);
    println!("扩容后分布:");
    for (node, count) in &user_dist_after {
        println!("  {}: {} 个用户", node, count);
    }
    
    // 计算数据迁移量
    let mut migrated = 0;
    for key in &user_id_refs {
        let before = get_node_before(&user_dist, key);
        let after = cache_cluster.get_node(key);
        if before != after {
            migrated += 1;
        }
    }
    println!("\n数据迁移统计:");
    println!("  总用户数: {}", user_ids.len());
    println!("  需迁移用户: {} ({:.1}%)", migrated, (migrated as f64 / user_ids.len() as f64) * 100.0);
    
    // 缩容场景
    println!("\n>>> 缩容: 移除 redis-02");
    cache_cluster.remove_node("redis-02");
    
    let user_dist_final = cache_cluster.distribution(&user_id_refs);
    println!("缩容后分布:");
    for (node, count) in &user_dist_final {
        println!("  {}: {} 个用户", node, count);
    }
    
    println!();
    println!("=== 示例结束 ===");
}

// 辅助函数：获取之前分布中的节点
fn get_node_before(dist: &std::collections::BTreeMap<String, usize>, _key: &str) -> Option<String> {
    // 简化实现：根据分布推断
    for (node, &count) in dist {
        if count > 0 {
            return Some(node.clone());
        }
    }
    None
}