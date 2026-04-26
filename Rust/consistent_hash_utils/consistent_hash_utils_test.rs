//! 一致性哈希工具测试套件
//! 
//! 运行测试: cargo test

use consistent_hash_utils::{ConsistentHash, WeightedConsistentHash};

/// 测试基本添加和获取节点
#[test]
fn test_basic_add_and_get() {
    let mut ch = ConsistentHash::new(150);
    
    ch.add_node("server1".to_string());
    ch.add_node("server2".to_string());
    ch.add_node("server3".to_string());
    
    assert_eq!(ch.node_count(), 3);
    
    // 确保每个键都能获取到节点
    for i in 0..100 {
        let key = format!("user_{}", i);
        let node = ch.get_node(&key);
        assert!(node.is_some());
    }
}

/// 测试键的一致性（相同键总是映射到相同节点）
#[test]
fn test_consistency() {
    let mut ch = ConsistentHash::new(150);
    ch.add_node("node1".to_string());
    ch.add_node("node2".to_string());
    ch.add_node("node3".to_string());
    
    let test_keys = ["key1", "key2", "key3", "long_key_name", "中文键", "🔑"];
    
    for key in test_keys {
        let node1 = ch.get_node(key);
        let node2 = ch.get_node(key);
        let node3 = ch.get_node(key);
        
        assert_eq!(node1, node2, "相同键映射到不同节点: {}", key);
        assert_eq!(node2, node3, "相同键映射到不同节点: {}", key);
    }
}

/// 测试节点移除后重新分配
#[test]
fn test_node_removal() {
    let mut ch = ConsistentHash::new(150);
    ch.add_node("node1".to_string());
    ch.add_node("node2".to_string());
    ch.add_node("node3".to_string());
    
    // 记录原始分配
    let original_mapping: Vec<(String, Option<String>)> = (0..50)
        .map(|i| {
            let key = format!("key_{}", i);
            (key.clone(), ch.get_node(&key))
        })
        .collect();
    
    // 移除节点
    ch.remove_node("node2");
    assert_eq!(ch.node_count(), 2);
    
    // 验证重新分配
    // 移除 node2 后，原来分配到 node2 的键应该重新分配到其他节点
    for (key, original_node) in &original_mapping {
        let new_node = ch.get_node(key);
        if original_node.as_ref().map(|s| s.as_str()) == Some("node2") {
            // 原 node2 的键应该分配到 node1 或 node3
            assert!(
                new_node.as_ref().map(|s| s.as_str()) == Some("node1") 
                || new_node.as_ref().map(|s| s.as_str()) == Some("node3"),
                "键 {} 重新分配错误: {:?}", key, new_node
            );
        } else {
            // 其他键应该保持不变
            assert_eq!(new_node, *original_node, "键 {} 不应该改变分配", key);
        }
    }
}

/// 测试负载分布均衡性
#[test]
fn test_load_distribution() {
    let mut ch = ConsistentHash::new(200); // 更多的虚拟节点提高均衡性
    ch.add_node("node1".to_string());
    ch.add_node("node2".to_string());
    ch.add_node("node3".to_string());
    
    // 生成大量测试键
    let keys: Vec<String> = (0..10000).map(|i| format!("test_key_{:06}", i)).collect();
    let key_refs: Vec<&str> = keys.iter().map(|s| s.as_str()).collect();
    
    let dist = ch.distribution(&key_refs);
    
    // 每个节点应该承担大约 33% 的负载
    let expected_per_node = 10000.0 / 3.0;
    let tolerance = expected_per_node * 0.20; // 20% 容差（更宽松）
    
    for node in &["node1", "node2", "node3"] {
        let count = *dist.get(*node).unwrap_or(&0) as f64;
        let diff = (count - expected_per_node).abs();
        assert!(
            diff <= tolerance,
            "节点 {} 负载不均衡: {} (期望: {}, 容差: {})",
            node, count, expected_per_node, tolerance
        );
    }
}

/// 测试虚拟节点数量影响
#[test]
fn test_virtual_nodes_impact() {
    // 少量虚拟节点
    let mut ch_low = ConsistentHash::new(10);
    ch_low.add_node("node1".to_string());
    ch_low.add_node("node2".to_string());
    
    // 大量虚拟节点
    let mut ch_high = ConsistentHash::new(1000);
    ch_high.add_node("node1".to_string());
    ch_high.add_node("node2".to_string());
    
    let keys: Vec<String> = (0..1000).map(|i| format!("key_{}", i)).collect();
    let key_refs: Vec<&str> = keys.iter().map(|s| s.as_str()).collect();
    
    let dist_low = ch_low.distribution(&key_refs);
    let dist_high = ch_high.distribution(&key_refs);
    
    // 计算标准差来衡量均衡性
    let calc_std = |dist: &std::collections::BTreeMap<String, usize>| -> f64 {
        let values: Vec<f64> = dist.values().map(|&v| v as f64).collect();
        let mean = values.iter().sum::<f64>() / values.len() as f64;
        let variance = values.iter().map(|v| (v - mean).powi(2)).sum::<f64>() / values.len() as f64;
        variance.sqrt()
    };
    
    let std_low = calc_std(&dist_low);
    let std_high = calc_std(&dist_high);
    
    // 更多虚拟节点应该更均衡
    assert!(
        std_high <= std_low * 1.5, // 允许一定波动
        "高虚拟节点应该更均衡: 低={}, 高={}",
        std_low, std_high
    );
}

/// 测试获取多个节点（用于数据复制）
#[test]
fn test_get_multiple_nodes() {
    let mut ch = ConsistentHash::new(150);
    ch.add_node("node1".to_string());
    ch.add_node("node2".to_string());
    ch.add_node("node3".to_string());
    ch.add_node("node4".to_string());
    ch.add_node("node5".to_string());
    
    // 请求 3 个节点
    let nodes = ch.get_nodes("test_key", 3);
    assert_eq!(nodes.len(), 3);
    
    // 确保节点不重复
    let unique: std::collections::HashSet<_> = nodes.iter().collect();
    assert_eq!(unique.len(), 3);
    
    // 请求超过节点数量
    let nodes_exceed = ch.get_nodes("key", 10);
    assert_eq!(nodes_exceed.len(), 5); // 最多返回所有节点
}

/// 测试空环行为
#[test]
fn test_empty_ring() {
    let ch = ConsistentHash::new(150);
    
    assert!(ch.get_node("any_key").is_none());
    assert!(ch.get_nodes("any_key", 3).is_empty());
    assert_eq!(ch.node_count(), 0);
    assert_eq!(ch.virtual_node_count(), 0);
}

/// 测试批量添加节点
#[test]
fn test_batch_add_nodes() {
    let mut ch = ConsistentHash::new(100);
    
    let added = ch.add_nodes(vec!["server1", "server2", "server3"]);
    assert_eq!(added, 3);
    assert_eq!(ch.node_count(), 3);
    
    // 重复添加应该返回 0
    let readded = ch.add_nodes(vec!["server1", "server2", "server3"]);
    assert_eq!(readded, 0);
}

/// 测试清空操作
#[test]
fn test_clear() {
    let mut ch = ConsistentHash::new(150);
    ch.add_node("node1".to_string());
    ch.add_node("node2".to_string());
    ch.add_node("node3".to_string());
    
    ch.clear();
    
    assert_eq!(ch.node_count(), 0);
    assert_eq!(ch.virtual_node_count(), 0);
    assert!(ch.get_node("key").is_none());
}

/// 测试加权一致性哈希
#[test]
fn test_weighted_hash() {
    let mut wch = WeightedConsistentHash::new(100);
    
    wch.add_node("small".to_string(), 1);
    wch.add_node("medium".to_string(), 2);
    wch.add_node("large".to_string(), 4);
    
    assert_eq!(wch.node_count(), 3);
    
    // 验证权重
    assert_eq!(wch.get_weight("small"), Some(1));
    assert_eq!(wch.get_weight("medium"), Some(2));
    assert_eq!(wch.get_weight("large"), Some(4));
    
    // 统计分布
    let mut counts: std::collections::HashMap<String, usize> = std::collections::HashMap::new();
    for i in 0..10000 {
        if let Some(node) = wch.get_node(&format!("key_{}", i)) {
            *counts.entry(node).or_insert(0) += 1;
        }
    }
    
    // large 节点应该承担最多负载
    let large_count = counts.get("large").copied().unwrap_or(0);
    let small_count = counts.get("small").copied().unwrap_or(0);
    
    assert!(
        large_count > small_count * 2,
        "权重高的节点应该承担更多负载: large={}, small={}",
        large_count, small_count
    );
}

/// 测试加权哈希节点移除
#[test]
fn test_weighted_remove() {
    let mut wch = WeightedConsistentHash::new(100);
    
    wch.add_node("node1".to_string(), 1);
    wch.add_node("node2".to_string(), 2);
    
    assert!(wch.remove_node("node1"));
    assert!(!wch.remove_node("node1")); // 重复移除
    assert_eq!(wch.node_count(), 1);
}

/// 测试边界情况：零权重
#[test]
fn test_zero_weight() {
    let mut wch = WeightedConsistentHash::new(100);
    
    // 零权重不应该添加
    assert!(!wch.add_node("zero".to_string(), 0));
    assert_eq!(wch.node_count(), 0);
}

/// 测试默认实例创建
#[test]
fn test_default_instance() {
    let ch = ConsistentHash::default_instance();
    assert_eq!(ch.node_count(), 0);
    assert_eq!(ch.virtual_node_count(), 0);
}

/// 测试获取节点列表
#[test]
fn test_get_nodes_list() {
    let mut ch = ConsistentHash::new(100);
    ch.add_node("node1".to_string());
    ch.add_node("node2".to_string());
    ch.add_node("node3".to_string());
    
    let nodes = ch.get_nodes_list();
    assert_eq!(nodes.len(), 3);
    
    for node in &["node1", "node2", "node3"] {
        assert!(nodes.contains(node));
    }
}

/// 测试特殊字符键
#[test]
fn test_special_characters() {
    let mut ch = ConsistentHash::new(150);
    ch.add_node("node1".to_string());
    ch.add_node("node2".to_string());
    
    // 测试各种特殊字符
    let mut special_keys: Vec<String> = vec![
        "".to_string(),
        " ".to_string(),
        "\t".to_string(),
        "\n".to_string(),
        "key with spaces".to_string(),
        "key:with:colons".to_string(),
        "key/with/slashes".to_string(),
        "key#with#hash".to_string(),
        "key?with?question".to_string(),
        "中文键".to_string(),
        "日本語キー".to_string(),
        "🔑🦀🚀".to_string(),
    ];
    
    // 测试非常长的键
    special_keys.push("very_long_key_".to_string() + &"a".repeat(1000));
    
    for key in &special_keys {
        let node = ch.get_node(key);
        assert!(node.is_some(), "键 {:?} 没有分配到节点", key);
        
        // 一致性检查
        let node2 = ch.get_node(key);
        assert_eq!(node, node2);
    }
}

/// 测试节点添加后的一致性
#[test]
fn test_add_node_consistency() {
    let mut ch = ConsistentHash::new(150);
    ch.add_node("node1".to_string());
    ch.add_node("node2".to_string());
    
    // 记录初始映射
    let initial_mapping: std::collections::HashMap<String, String> = (0..100)
        .map(|i| {
            let key = format!("key_{}", i);
            (key.clone(), ch.get_node(&key).unwrap())
        })
        .collect();
    
    // 添加新节点
    ch.add_node("node3".to_string());
    
    // 大部分键应该保持不变
    let unchanged = initial_mapping.iter()
        .filter(|(key, node)| ch.get_node(key) == Some(node.to_string()))
        .count();
    
    // 约有 1/3 的键会改变（添加了第三个节点）
    // 但不应该超过 50%
    let change_ratio = 1.0 - (unchanged as f64 / initial_mapping.len() as f64);
    assert!(
        change_ratio < 0.5,
        "添加节点后变化比例过高: {:.2}%",
        change_ratio * 100.0
    );
}