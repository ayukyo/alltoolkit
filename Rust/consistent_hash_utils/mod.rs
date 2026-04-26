//! 一致性哈希工具模块
//! 
//! 提供一致性哈希算法的实现，用于分布式系统中的负载均衡和数据分片。
//! 
//! # 特性
//! 
//! - 支持虚拟节点，提高数据分布均匀性
//! - 支持 MD5 和自定义哈希函数
//! - 节点动态添加和删除
//! - 零外部依赖
//! 
//! # 示例
//! 
//! ```
//! use consistent_hash_utils::ConsistentHash;
//! 
//! let mut ch = ConsistentHash::new(150); // 每个节点150个虚拟节点
//! ch.add_node("node1".to_string());
//! ch.add_node("node2".to_string());
//! ch.add_node("node3".to_string());
//! 
//! let node = ch.get_node("user:12345").unwrap();
//! println!("Key 'user:12345' maps to: {}", node);
//! ```

use std::collections::BTreeMap;
use std::collections::HashSet;

/// 一致性哈希结构体
/// 
/// 使用 BTreeMap 存储哈希环，支持高效的节点查找
#[derive(Debug, Clone)]
pub struct ConsistentHash {
    /// 哈希环，key 为哈希值，value 为节点名
    ring: BTreeMap<u64, String>,
    /// 已添加的节点集合
    nodes: HashSet<String>,
    /// 每个节点的虚拟节点数量
    virtual_nodes: usize,
}

impl ConsistentHash {
    /// 创建新的一致性哈希实例
    /// 
    /// # 参数
    /// 
    /// * `virtual_nodes` - 每个物理节点对应的虚拟节点数量，推荐 100-200
    /// 
    /// # 示例
    /// 
    /// ```
    /// use consistent_hash_utils::ConsistentHash;
    /// 
    /// let ch = ConsistentHash::new(150);
    /// ```
    pub fn new(virtual_nodes: usize) -> Self {
        ConsistentHash {
            ring: BTreeMap::new(),
            nodes: HashSet::new(),
            virtual_nodes,
        }
    }
    
    /// 使用默认虚拟节点数量(150)创建实例
    pub fn default_instance() -> Self {
        Self::new(150)
    }
    
    /// 添加节点
    /// 
    /// # 参数
    /// 
    /// * `node` - 节点名称
    /// 
    /// # 返回
    /// 
    /// 如果节点已存在，返回 false；否则返回 true
    /// 
    /// # 示例
    /// 
    /// ```
    /// use consistent_hash_utils::ConsistentHash;
    /// 
    /// let mut ch = ConsistentHash::new(150);
    /// assert!(ch.add_node("server1".to_string()));
    /// assert!(!ch.add_node("server1".to_string())); // 重复添加返回 false
    /// ```
    pub fn add_node(&mut self, node: String) -> bool {
        if self.nodes.contains(&node) {
            return false;
        }
        
        self.nodes.insert(node.clone());
        
        // 为每个物理节点创建虚拟节点
        for i in 0..self.virtual_nodes {
            let virtual_node_key = format!("{}#{}", node, i);
            let hash = Self::hash_md5(&virtual_node_key);
            self.ring.insert(hash, node.clone());
        }
        
        true
    }
    
    /// 批量添加节点
    /// 
    /// # 参数
    /// 
    /// * `nodes` - 节点名称迭代器
    /// 
    /// # 返回
    /// 
    /// 成功添加的节点数量
    pub fn add_nodes<'a, I>(&mut self, nodes: I) -> usize
    where
        I: IntoIterator<Item = &'a str>,
    {
        nodes.into_iter().filter(|n| self.add_node(n.to_string())).count()
    }
    
    /// 移除节点
    /// 
    /// # 参数
    /// 
    /// * `node` - 节点名称
    /// 
    /// # 返回
    /// 
    /// 如果节点存在并被移除，返回 true；否则返回 false
    pub fn remove_node(&mut self, node: &str) -> bool {
        if !self.nodes.remove(node) {
            return false;
        }
        
        // 移除所有相关的虚拟节点
        for i in 0..self.virtual_nodes {
            let virtual_node_key = format!("{}#{}", node, i);
            let hash = Self::hash_md5(&virtual_node_key);
            self.ring.remove(&hash);
        }
        
        true
    }
    
    /// 获取键对应的节点
    /// 
    /// # 参数
    /// 
    /// * `key` - 要查找的键
    /// 
    /// # 返回
    /// 
    /// 返回负责该键的节点名称，如果没有节点则返回 None
    /// 
    /// # 示例
    /// 
    /// ```
    /// use consistent_hash_utils::ConsistentHash;
    /// 
    /// let mut ch = ConsistentHash::new(150);
    /// ch.add_node("node1".to_string());
    /// 
    /// let node = ch.get_node("user:12345").unwrap();
    /// assert_eq!(node, "node1");
    /// ```
    pub fn get_node(&self, key: &str) -> Option<String> {
        if self.ring.is_empty() {
            return None;
        }
        
        let hash = Self::hash_md5(key);
        
        // 查找第一个哈希值 >= key哈希值的节点
        match self.ring.range(hash..).next() {
            Some((_, node)) => Some(node.clone()),
            None => {
                // 如果没找到，说明应该在环的开头
                self.ring.values().next().map(|s| s.clone())
            }
        }
    }
    
    /// 获取键对应的多个节点（用于数据复制）
    /// 
    /// # 参数
    /// 
    /// * `key` - 要查找的键
    /// * `count` - 需要的节点数量
    /// 
    /// # 返回
    /// 
    /// 返回不同的节点列表，如果节点数量不足则返回尽可能多的节点
    pub fn get_nodes(&self, key: &str, count: usize) -> Vec<String> {
        if self.ring.is_empty() || count == 0 {
            return Vec::new();
        }
        
        let hash = Self::hash_md5(key);
        let mut result = Vec::new();
        let mut seen = HashSet::new();
        
        // 从 hash 位置开始查找
        for (_, node) in self.ring.range(hash..) {
            if seen.insert(node.clone()) {
                result.push(node.clone());
                if result.len() >= count {
                    return result;
                }
            }
        }
        
        // 如果不够，从头开始查找
        for (_, node) in self.ring.iter() {
            if seen.insert(node.clone()) {
                result.push(node.clone());
                if result.len() >= count {
                    return result;
                }
            }
        }
        
        result
    }
    
    /// 获取当前节点数量
    pub fn node_count(&self) -> usize {
        self.nodes.len()
    }
    
    /// 获取虚拟节点数量
    pub fn virtual_node_count(&self) -> usize {
        self.ring.len()
    }
    
    /// 获取所有节点名称
    pub fn get_nodes_list(&self) -> Vec<&str> {
        self.nodes.iter().map(|s| s.as_str()).collect()
    }
    
    /// 检查节点是否存在
    pub fn has_node(&self, node: &str) -> bool {
        self.nodes.contains(node)
    }
    
    /// 清空所有节点
    pub fn clear(&mut self) {
        self.ring.clear();
        self.nodes.clear();
    }
    
    /// 计算键的分布统计
    /// 
    /// # 参数
    /// 
    /// * `keys` - 要分析的键列表
    /// 
    /// # 返回
    /// 
    /// 返回每个节点负责的键数量
    pub fn distribution(&self, keys: &[&str]) -> BTreeMap<String, usize> {
        let mut dist = BTreeMap::new();
        for node in &self.nodes {
            dist.insert(node.clone(), 0);
        }
        
        for key in keys {
            if let Some(node) = self.get_node(key) {
                *dist.get_mut(&node).unwrap() += 1;
            }
        }
        
        dist
    }
    
    /// 计算 MD5 哈希值 (u64)
    /// 
    /// 使用 MD5 算法计算哈希值，取前 8 字节作为 u64
    pub fn hash_md5(key: &str) -> u64 {
        // 内置 MD5 实现（零依赖）
        let bytes = key.as_bytes();
        let hash_bytes = md5(bytes);
        u64::from_be_bytes([
            hash_bytes[0], hash_bytes[1], hash_bytes[2], hash_bytes[3],
            hash_bytes[4], hash_bytes[5], hash_bytes[6], hash_bytes[7],
        ])
    }
}

/// MD5 哈希实现
/// 
/// 纯 Rust 实现，零外部依赖
fn md5(input: &[u8]) -> [u8; 16] {
    // 初始化
    let mut a0: u32 = 0x67452301;
    let mut b0: u32 = 0xefcdab89;
    let mut c0: u32 = 0x98badcfe;
    let mut d0: u32 = 0x10325476;
    
    // 预处理：添加填充
    let mut msg = input.to_vec();
    let original_len = msg.len() as u64;
    msg.push(0x80);
    
    // 填充到 56 mod 64 字节
    while msg.len() % 64 != 56 {
        msg.push(0);
    }
    
    // 追加原始长度（小端序，以位为单位，所以乘以8）
    let bit_len = (original_len * 8) as u64;
    msg.extend_from_slice(&bit_len.to_le_bytes());
    
    // 确保消息长度是 64 字节的倍数
    assert!(msg.len() % 64 == 0, "Message length must be multiple of 64 bytes");
    
    // 处理每个 512 位块
    for chunk in msg.chunks(64) {
        let mut m = [0u32; 16];
        for i in 0..16 {
            m[i] = u32::from_le_bytes([
                chunk[i * 4],
                chunk[i * 4 + 1],
                chunk[i * 4 + 2],
                chunk[i * 4 + 3],
            ]);
        }
        
        let mut a = a0;
        let mut b = b0;
        let mut c = c0;
        let mut d = d0;
        
        // 主循环
        for i in 0..64 {
            let (f, g) = match i {
                0..=15 => ((b & c) | ((!b) & d), i),
                16..=31 => ((d & b) | ((!d) & c), (5 * i + 1) % 16),
                32..=47 => (b ^ c ^ d, (3 * i + 5) % 16),
                _ => (c ^ (b | (!d)), (7 * i) % 16),
            };
            
            let f = f.wrapping_add(a).wrapping_add(K[i]).wrapping_add(m[g]);
            a = d;
            d = c;
            c = b;
            b = b.wrapping_add(left_rotate(f, S[i]));
        }
        
        a0 = a0.wrapping_add(a);
        b0 = b0.wrapping_add(b);
        c0 = c0.wrapping_add(c);
        d0 = d0.wrapping_add(d);
    }
    
    // 输出结果
    let mut result = [0u8; 16];
    result[..4].copy_from_slice(&a0.to_le_bytes());
    result[4..8].copy_from_slice(&b0.to_le_bytes());
    result[8..12].copy_from_slice(&c0.to_le_bytes());
    result[12..].copy_from_slice(&d0.to_le_bytes());
    
    result
}

/// 左循环移位
fn left_rotate(x: u32, c: u32) -> u32 {
    (x << c) | (x >> (32 - c))
}

/// MD5 常量表
const K: [u32; 64] = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
    0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
    0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
    0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
    0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,
];

/// MD5 每轮的位移量
const S: [u32; 64] = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21,
];

/// 带权重的一致性哈希
/// 
/// 允许为不同节点分配不同的权重，权重越高的节点承担更多的负载
#[derive(Debug, Clone)]
pub struct WeightedConsistentHash {
    ring: BTreeMap<u64, String>,
    nodes: HashSet<String>,
    weights: std::collections::HashMap<String, usize>,
    base_virtual_nodes: usize,
}

impl WeightedConsistentHash {
    /// 创建新的加权一致性哈希实例
    /// 
    /// # 参数
    /// 
    /// * `base_virtual_nodes` - 基础虚拟节点数量（权重为1时的虚拟节点数）
    pub fn new(base_virtual_nodes: usize) -> Self {
        WeightedConsistentHash {
            ring: BTreeMap::new(),
            nodes: HashSet::new(),
            weights: std::collections::HashMap::new(),
            base_virtual_nodes,
        }
    }
    
    /// 添加带权重的节点
    /// 
    /// # 参数
    /// 
    /// * `node` - 节点名称
    /// * `weight` - 节点权重（>= 1）
    pub fn add_node(&mut self, node: String, weight: usize) -> bool {
        if weight == 0 || self.nodes.contains(&node) {
            return false;
        }
        
        self.nodes.insert(node.clone());
        self.weights.insert(node.clone(), weight);
        
        // 根据权重计算虚拟节点数量
        let virtual_nodes = self.base_virtual_nodes * weight;
        
        for i in 0..virtual_nodes {
            let virtual_node_key = format!("{}#{}", node, i);
            let hash = ConsistentHash::hash_md5(&virtual_node_key);
            self.ring.insert(hash, node.clone());
        }
        
        true
    }
    
    /// 移除节点
    pub fn remove_node(&mut self, node: &str) -> bool {
        if !self.nodes.remove(node) {
            return false;
        }
        
        let weight = self.weights.remove(node).unwrap_or(1);
        let virtual_nodes = self.base_virtual_nodes * weight;
        
        for i in 0..virtual_nodes {
            let virtual_node_key = format!("{}#{}", node, i);
            let hash = ConsistentHash::hash_md5(&virtual_node_key);
            self.ring.remove(&hash);
        }
        
        true
    }
    
    /// 获取键对应的节点
    pub fn get_node(&self, key: &str) -> Option<String> {
        if self.ring.is_empty() {
            return None;
        }
        
        let hash = ConsistentHash::hash_md5(key);
        
        match self.ring.range(hash..).next() {
            Some((_, node)) => Some(node.clone()),
            None => self.ring.values().next().map(|s| s.clone()),
        }
    }
    
    /// 获取节点权重
    pub fn get_weight(&self, node: &str) -> Option<usize> {
        self.weights.get(node).copied()
    }
    
    /// 获取节点数量
    pub fn node_count(&self) -> usize {
        self.nodes.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_basic_operations() {
        let mut ch = ConsistentHash::new(150);
        
        // 添加节点
        assert!(ch.add_node("node1".to_string()));
        assert!(ch.add_node("node2".to_string()));
        assert!(ch.add_node("node3".to_string()));
        
        // 重复添加
        assert!(!ch.add_node("node1".to_string()));
        
        // 检查节点数量
        assert_eq!(ch.node_count(), 3);
        assert_eq!(ch.virtual_node_count(), 450);
        
        // 检查节点存在
        assert!(ch.has_node("node1"));
        assert!(!ch.has_node("node4"));
    }
    
    #[test]
    fn test_get_node() {
        let mut ch = ConsistentHash::new(150);
        ch.add_node("node1".to_string());
        
        // 单节点情况
        let node = ch.get_node("any_key").unwrap();
        assert_eq!(node, "node1");
        
        // 多节点
        ch.add_node("node2".to_string());
        ch.add_node("node3".to_string());
        
        // 相同键总是映射到相同节点
        let key = "test_key_12345";
        let node1 = ch.get_node(key);
        let node2 = ch.get_node(key);
        assert_eq!(node1, node2);
    }
    
    #[test]
    fn test_distribution() {
        let mut ch = ConsistentHash::new(150);
        ch.add_node("node1".to_string());
        ch.add_node("node2".to_string());
        ch.add_node("node3".to_string());
        
        // 生成测试键
        let keys: Vec<String> = (0..1000).map(|i| format!("key_{}", i)).collect();
        let key_refs: Vec<&str> = keys.iter().map(|s| s.as_str()).collect();
        
        let dist = ch.distribution(&key_refs);
        
        // 每个节点都应该分配到一些键
        for node in &["node1", "node2", "node3"] {
            let count = dist.get(*node).unwrap_or(&0);
            assert!(*count > 200, "节点 {} 只分配了 {} 个键", node, count);
        }
    }
    
    #[test]
    fn test_remove_node() {
        let mut ch = ConsistentHash::new(150);
        ch.add_node("node1".to_string());
        ch.add_node("node2".to_string());
        
        // 移除节点
        assert!(ch.remove_node("node1"));
        assert!(!ch.has_node("node1"));
        assert_eq!(ch.node_count(), 1);
        assert_eq!(ch.virtual_node_count(), 150);
        
        // 移除不存在的节点
        assert!(!ch.remove_node("node3"));
    }
    
    #[test]
    fn test_get_nodes_replication() {
        let mut ch = ConsistentHash::new(150);
        ch.add_node("node1".to_string());
        ch.add_node("node2".to_string());
        ch.add_node("node3".to_string());
        ch.add_node("node4".to_string());
        
        // 获取3个节点用于复制
        let nodes = ch.get_nodes("key1", 3);
        assert_eq!(nodes.len(), 3);
        
        // 确保节点不重复
        let unique: std::collections::HashSet<_> = nodes.iter().collect();
        assert_eq!(unique.len(), 3);
    }
    
    #[test]
    fn test_add_nodes_batch() {
        let mut ch = ConsistentHash::new(100);
        let count = ch.add_nodes(vec!["a", "b", "c", "d"].into_iter());
        assert_eq!(count, 4);
        assert_eq!(ch.node_count(), 4);
    }
    
    #[test]
    fn test_clear() {
        let mut ch = ConsistentHash::new(150);
        ch.add_node("node1".to_string());
        ch.add_node("node2".to_string());
        
        ch.clear();
        assert_eq!(ch.node_count(), 0);
        assert_eq!(ch.virtual_node_count(), 0);
    }
    
    #[test]
    fn test_empty_ring() {
        let ch = ConsistentHash::new(150);
        assert!(ch.get_node("key").is_none());
        assert!(ch.get_nodes("key", 3).is_empty());
    }
    
    #[test]
    fn test_weighted_consistent_hash() {
        let mut wch = WeightedConsistentHash::new(100);
        
        wch.add_node("small".to_string(), 1);
        wch.add_node("medium".to_string(), 2);
        wch.add_node("large".to_string(), 3);
        
        assert_eq!(wch.node_count(), 3);
        assert_eq!(wch.get_weight("small"), Some(1));
        assert_eq!(wch.get_weight("medium"), Some(2));
        assert_eq!(wch.get_weight("large"), Some(3));
        
        // 测试键分配
        let node = wch.get_node("test_key");
        assert!(node.is_some());
    }
    
    #[test]
    fn test_md5_implementation() {
        // 测试已知值
        let hash1 = md5(b"");
        assert_eq!(hex_encode(&hash1), "d41d8cd98f00b204e9800998ecf8427e");
        
        let hash2 = md5(b"hello");
        assert_eq!(hex_encode(&hash2), "5d41402abc4b2a76b9719d911017c592");
        
        let hash3 = md5(b"The quick brown fox jumps over the lazy dog");
        assert_eq!(hex_encode(&hash3), "9e107d9d372bb6826bd81d3542a419d6");
    }
    
    fn hex_encode(bytes: &[u8]) -> String {
        bytes.iter().map(|b| format!("{:02x}", b)).collect()
    }
}