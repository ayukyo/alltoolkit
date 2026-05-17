/// Snowflake ID Generator Utils
/// 
/// A Twitter Snowflake-like distributed unique ID generator.
/// 
/// ID Structure (64 bits):
/// ```text
/// | 1 bit |    41 bits     |  10 bits  |    12 bits    |
/// | sign  |   timestamp    |  node_id  |  sequence_id  |
/// ```
/// 
/// - Sign bit: Always 0 (positive number)
/// - Timestamp: Milliseconds since custom epoch (default: 2024-01-01)
/// - Node ID: 0-1023 (10 bits, supports 1024 nodes)
/// - Sequence ID: 0-4095 (12 bits, 4096 IDs per millisecond per node)
/// 
/// Features:
/// - Zero external dependencies
/// - Thread-safe ID generation
/// - Clock drift detection and handling
/// - Configurable epoch and node ID

use std::sync::atomic::{AtomicI64, AtomicU64, Ordering};
use std::time::{SystemTime, UNIX_EPOCH};

/// Default custom epoch: 2024-01-01 00:00:00 UTC
pub const DEFAULT_EPOCH: i64 = 1704067200000;

/// Bit lengths for each component
pub const TIMESTAMP_BITS: u64 = 41;
pub const NODE_ID_BITS: u64 = 10;
pub const SEQUENCE_BITS: u64 = 12;

/// Maximum values
pub const MAX_NODE_ID: u64 = (1 << NODE_ID_BITS) - 1; // 1023
pub const MAX_SEQUENCE: u64 = (1 << SEQUENCE_BITS) - 1; // 4095
pub const MAX_TIMESTAMP: i64 = (1i64 << TIMESTAMP_BITS) - 1;

/// Bit shifts
pub const NODE_ID_SHIFT: u64 = SEQUENCE_BITS; // 12
pub const TIMESTAMP_SHIFT: u64 = SEQUENCE_BITS + NODE_ID_BITS; // 22

/// Snowflake ID Generator
/// 
/// # Example
/// 
/// ```
/// use snowflake_utils::{SnowflakeGenerator, DEFAULT_EPOCH};
/// 
/// let generator = SnowflakeGenerator::new(1, DEFAULT_EPOCH);
/// let id = generator.generate();
/// println!("Generated ID: {}", id);
/// ```
pub struct SnowflakeGenerator {
    node_id: u64,
    epoch: i64,
    last_timestamp: AtomicI64,
    sequence: AtomicU64,
}

impl SnowflakeGenerator {
    /// Create a new Snowflake generator
    /// 
    /// # Arguments
    /// 
    /// * `node_id` - Unique node ID (0-1023)
    /// * `epoch` - Custom epoch in milliseconds
    /// 
    /// # Panics
    /// 
    /// Panics if node_id > 1023
    pub fn new(node_id: u64, epoch: i64) -> Self {
        if node_id > MAX_NODE_ID {
            panic!("Node ID must be between 0 and {}", MAX_NODE_ID);
        }
        
        Self {
            node_id,
            epoch,
            last_timestamp: AtomicI64::new(-1),
            sequence: AtomicU64::new(0),
        }
    }
    
    /// Create generator with default epoch (2024-01-01)
    pub fn with_node_id(node_id: u64) -> Self {
        Self::new(node_id, DEFAULT_EPOCH)
    }
    
    /// Generate a unique ID
    /// 
    /// Returns a 64-bit unique ID
    pub fn generate(&self) -> u64 {
        loop {
            let current_ts = self.current_timestamp();
            let last_ts = self.last_timestamp.load(Ordering::SeqCst);
            
            if current_ts < last_ts {
                // Clock moved backwards, wait for clock to catch up
                self.wait_for_clock_sync(last_ts);
                continue;
            }
            
            if current_ts == last_ts {
                // Same millisecond, increment sequence
                let seq = self.sequence.fetch_add(1, Ordering::SeqCst);
                
                if seq > MAX_SEQUENCE {
                    // Sequence overflow, spin wait for next millisecond
                    loop {
                        let now = self.current_timestamp();
                        if now > last_ts {
                            break;
                        }
                        std::thread::yield_now();
                    }
                    continue;
                }
                
                return self.compose_id(current_ts, seq);
            } else {
                // New millisecond, try to update last_timestamp and reset sequence
                match self.last_timestamp.compare_exchange(
                    last_ts,
                    current_ts,
                    Ordering::SeqCst,
                    Ordering::SeqCst,
                ) {
                    Ok(_) => {
                        // Successfully updated timestamp, reset sequence
                        self.sequence.store(1, Ordering::SeqCst);
                        return self.compose_id(current_ts, 0);
                    }
                    Err(_) => {
                        // Another thread updated, retry
                        continue;
                    }
                }
            }
        }
    }
    
    /// Wait for clock to catch up (for clock drift)
    fn wait_for_clock_sync(&self, target_ts: i64) {
        loop {
            let now = self.current_timestamp();
            if now >= target_ts {
                break;
            }
            std::thread::yield_now();
        }
    }
    
    /// Generate multiple IDs at once
    /// 
    /// # Arguments
    /// 
    /// * `count` - Number of IDs to generate
    pub fn generate_batch(&self, count: usize) -> Vec<u64> {
        (0..count).map(|_| self.generate()).collect()
    }
    
    /// Parse an ID into its components
    /// 
    /// # Returns
    /// 
    /// A tuple of (timestamp_ms, node_id, sequence)
    pub fn parse_id(&self, id: u64) -> (i64, u64, u64) {
        let timestamp = ((id >> TIMESTAMP_SHIFT) as i64) + self.epoch;
        let node_id = (id >> NODE_ID_SHIFT) & MAX_NODE_ID;
        let sequence = id & MAX_SEQUENCE;
        
        (timestamp, node_id, sequence)
    }
    
    /// Get the timestamp from an ID
    pub fn get_timestamp(&self, id: u64) -> i64 {
        ((id >> TIMESTAMP_SHIFT) as i64) + self.epoch
    }
    
    /// Get the node ID from an ID
    pub fn get_node_id(id: u64) -> u64 {
        (id >> NODE_ID_SHIFT) & MAX_NODE_ID
    }
    
    /// Get the sequence from an ID
    pub fn get_sequence(id: u64) -> u64 {
        id & MAX_SEQUENCE
    }
    
    /// Get the node ID of this generator
    pub fn node_id(&self) -> u64 {
        self.node_id
    }
    
    /// Get the epoch of this generator
    pub fn epoch(&self) -> i64 {
        self.epoch
    }
    
    /// Get current timestamp in milliseconds since epoch
    fn current_timestamp(&self) -> i64 {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_millis() as i64;
        now - self.epoch
    }
    
    /// Compose an ID from components
    fn compose_id(&self, timestamp: i64, sequence: u64) -> u64 {
        ((timestamp as u64) << TIMESTAMP_SHIFT)
            | (self.node_id << NODE_ID_SHIFT)
            | (sequence & MAX_SEQUENCE)
    }
}

/// Snowflake ID with additional utility methods
pub struct SnowflakeId(pub u64);

impl SnowflakeId {
    /// Create from raw ID
    pub fn new(id: u64) -> Self {
        Self(id)
    }
    
    /// Parse from string
    pub fn from_string(s: &str) -> Option<Self> {
        s.parse::<u64>().ok().map(Self)
    }
    
    /// Get the raw ID
    pub fn id(&self) -> u64 {
        self.0
    }
    
    /// Convert to string
    pub fn to_string(&self) -> String {
        self.0.to_string()
    }
    
    /// Convert to hex string
    pub fn to_hex(&self) -> String {
        format!("{:016x}", self.0)
    }
    
    /// Parse from hex string
    pub fn from_hex(hex: &str) -> Option<Self> {
        u64::from_str_radix(hex.trim_start_matches("0x"), 16).ok().map(Self)
    }
    
    /// Get timestamp component (without epoch offset)
    pub fn timestamp_component(&self) -> u64 {
        self.0 >> TIMESTAMP_SHIFT
    }
    
    /// Get node ID component
    pub fn node_id_component(&self) -> u64 {
        (self.0 >> NODE_ID_SHIFT) & MAX_NODE_ID
    }
    
    /// Get sequence component
    pub fn sequence_component(&self) -> u64 {
        self.0 & MAX_SEQUENCE
    }
    
    /// Parse ID with epoch
    pub fn parse_with_epoch(&self, epoch: i64) -> ParsedSnowflake {
        ParsedSnowflake {
            id: self.0,
            timestamp_ms: ((self.0 >> TIMESTAMP_SHIFT) as i64) + epoch,
            node_id: self.node_id_component(),
            sequence: self.sequence_component(),
        }
    }
}

impl std::fmt::Display for SnowflakeId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl std::fmt::Debug for SnowflakeId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("SnowflakeId")
            .field("id", &self.0)
            .field("hex", &self.to_hex())
            .field("node_id", &self.node_id_component())
            .field("sequence", &self.sequence_component())
            .finish()
    }
}

/// Parsed snowflake ID information
#[derive(Debug, Clone)]
pub struct ParsedSnowflake {
    pub id: u64,
    pub timestamp_ms: i64,
    pub node_id: u64,
    pub sequence: u64,
}

impl ParsedSnowflake {
    /// Get the timestamp as SystemTime
    pub fn as_system_time(&self) -> SystemTime {
        UNIX_EPOCH + std::time::Duration::from_millis(self.timestamp_ms as u64)
    }
    
    /// Get the timestamp in seconds since Unix epoch
    pub fn as_secs(&self) -> f64 {
        self.timestamp_ms as f64 / 1000.0
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashSet;
    use std::sync::Arc;
    use std::thread;
    
    #[test]
    fn test_generate_basic() {
        let generator = SnowflakeGenerator::new(1, DEFAULT_EPOCH);
        let id = generator.generate();
        assert!(id > 0);
        
        let (ts, node, seq) = generator.parse_id(id);
        assert!(ts > 0);
        assert_eq!(node, 1);
        assert!(seq <= MAX_SEQUENCE);
    }
    
    #[test]
    fn test_generate_unique() {
        let generator = SnowflakeGenerator::new(1, DEFAULT_EPOCH);
        let mut ids = HashSet::new();
        
        for _ in 0..10000 {
            let id = generator.generate();
            assert!(ids.insert(id), "Duplicate ID generated: {}", id);
        }
    }
    
    #[test]
    fn test_generate_batch() {
        let generator = SnowflakeGenerator::new(1, DEFAULT_EPOCH);
        let ids = generator.generate_batch(1000);
        
        assert_eq!(ids.len(), 1000);
        
        let unique: HashSet<_> = ids.iter().collect();
        assert_eq!(unique.len(), 1000);
    }
    
    #[test]
    fn test_parse_id() {
        let generator = SnowflakeGenerator::new(42, DEFAULT_EPOCH);
        let id = generator.generate();
        
        let (ts, node, seq) = generator.parse_id(id);
        
        assert_eq!(node, 42);
        assert!(ts > 0);
        assert!(seq <= MAX_SEQUENCE);
        
        // Verify timestamp is recent
        let id_timestamp = generator.get_timestamp(id);
        assert!(id_timestamp > DEFAULT_EPOCH);
    }
    
    #[test]
    fn test_node_id_boundary() {
        // Min node ID
        let gen_min = SnowflakeGenerator::new(0, DEFAULT_EPOCH);
        let id_min = gen_min.generate();
        assert_eq!(SnowflakeGenerator::get_node_id(id_min), 0);
        
        // Max node ID
        let gen_max = SnowflakeGenerator::new(MAX_NODE_ID, DEFAULT_EPOCH);
        let id_max = gen_max.generate();
        assert_eq!(SnowflakeGenerator::get_node_id(id_max), MAX_NODE_ID);
    }
    
    #[test]
    #[should_panic(expected = "Node ID must be between 0 and 1023")]
    fn test_invalid_node_id() {
        SnowflakeGenerator::new(MAX_NODE_ID + 1, DEFAULT_EPOCH);
    }
    
    #[test]
    fn test_snowflake_id_helpers() {
        let generator = SnowflakeGenerator::new(123, DEFAULT_EPOCH);
        let id = generator.generate();
        
        let sf_id = SnowflakeId::new(id);
        
        assert_eq!(sf_id.id(), id);
        assert_eq!(sf_id.node_id_component(), 123);
        assert!(sf_id.sequence_component() <= MAX_SEQUENCE);
        
        // String conversions
        let id_str = sf_id.to_string();
        let parsed = SnowflakeId::from_string(&id_str).unwrap();
        assert_eq!(parsed.id(), id);
        
        // Hex conversions
        let hex = sf_id.to_hex();
        let from_hex = SnowflakeId::from_hex(&hex).unwrap();
        assert_eq!(from_hex.id(), id);
    }
    
    #[test]
    fn test_parsed_snowflake() {
        let generator = SnowflakeGenerator::new(1, DEFAULT_EPOCH);
        let id = generator.generate();
        
        let sf_id = SnowflakeId::new(id);
        let parsed = sf_id.parse_with_epoch(DEFAULT_EPOCH);
        
        assert_eq!(parsed.id, id);
        assert_eq!(parsed.node_id, 1);
        assert!(parsed.timestamp_ms > DEFAULT_EPOCH);
    }
    
    #[test]
    fn test_concurrent_generation() {
        let generator = Arc::new(SnowflakeGenerator::new(1, DEFAULT_EPOCH));
        let mut handles = vec![];
        let mut all_ids = vec![];
        
        for _ in 0..10 {
            let gen = Arc::clone(&generator);
            handles.push(thread::spawn(move || {
                (0..1000).map(|_| gen.generate()).collect::<Vec<_>>()
            }));
        }
        
        for handle in handles {
            all_ids.extend(handle.join().unwrap());
        }
        
        // All IDs should be unique
        let unique: HashSet<_> = all_ids.iter().collect();
        assert_eq!(unique.len(), 10000);
    }
    
    #[test]
    fn test_different_nodes_different_ids() {
        let gen1 = SnowflakeGenerator::new(1, DEFAULT_EPOCH);
        let gen2 = SnowflakeGenerator::new(2, DEFAULT_EPOCH);
        
        let id1 = gen1.generate();
        let id2 = gen2.generate();
        
        // IDs should be different even if generated at the same time
        assert_ne!(id1, id2);
        
        // Node IDs should be correct
        assert_eq!(SnowflakeGenerator::get_node_id(id1), 1);
        assert_eq!(SnowflakeGenerator::get_node_id(id2), 2);
    }
    
    #[test]
    fn test_id_ordering() {
        let generator = SnowflakeGenerator::new(1, DEFAULT_EPOCH);
        
        let mut ids: Vec<u64> = Vec::new();
        for _ in 0..1000 {
            ids.push(generator.generate());
            std::thread::sleep(std::time::Duration::from_micros(1));
        }
        
        // IDs should generally be increasing (monotonic)
        for i in 1..ids.len() {
            assert!(ids[i] >= ids[i - 1], "IDs should be monotonically increasing");
        }
    }
    
    #[test]
    fn test_custom_epoch() {
        // Custom epoch: 2020-01-01
        let custom_epoch = 1577836800000i64;
        let generator = SnowflakeGenerator::new(1, custom_epoch);
        
        let id = generator.generate();
        let (ts, _, _) = generator.parse_id(id);
        
        // Timestamp component should be positive
        assert!(ts > 0);
    }
}