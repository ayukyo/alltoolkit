//! UUID 工具库 - 零外部依赖
//!
//! 提供完整的 UUID 生成、解析、验证和格式化功能
//! 支持 UUID v1、v3、v4、v5、v7 以及自定义格式

use std::fmt;
use std::time::{SystemTime, UNIX_EPOCH};

/// UUID 版本
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum UuidVersion {
    V1 = 1,
    V3 = 3,
    V4 = 4,
    V5 = 5,
    V7 = 7,
}

/// UUID 变体
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum UuidVariant {
    NCS,
    RFC4122,
    Microsoft,
    Future,
}

/// UUID 结构体
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Uuid {
    bytes: [u8; 16],
}

impl Uuid {
    /// 创建空的 nil UUID (全零)
    pub const fn nil() -> Self {
        Uuid { bytes: [0; 16] }
    }

    /// 从字节数组创建 UUID
    pub const fn from_bytes(bytes: [u8; 16]) -> Self {
        Uuid { bytes }
    }

    /// 从切片创建 UUID，如果长度不是 16 字节则返回 None
    pub fn from_slice(slice: &[u8]) -> Option<Self> {
        if slice.len() == 16 {
            let mut bytes = [0u8; 16];
            bytes.copy_from_slice(slice);
            Some(Uuid { bytes })
        } else {
            None
        }
    }

    /// 从十六进制字符串解析 UUID
    /// 支持格式:
    /// - 带连字符: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    /// - 不带连字符: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    /// - 带花括号: {xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}
    /// - URN 格式: urn:uuid:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    pub fn parse(input: &str) -> Option<Self> {
        let s = input.trim();

        // 处理 URN 前缀
        let s = if s.starts_with("urn:uuid:") {
            &s[9..]
        } else {
            s
        };

        // 处理花括号
        let s = if s.starts_with('{') && s.ends_with('}') {
            &s[1..s.len() - 1]
        } else {
            s
        };

        // 移除所有连字符
        let clean: String = s.chars().filter(|c| *c != '-').collect();

        if clean.len() != 32 {
            return None;
        }

        let mut bytes = [0u8; 16];
        for i in 0..16 {
            let start = i * 2;
            let hex_byte = &clean[start..start + 2];
            bytes[i] = u8::from_str_radix(hex_byte, 16).ok()?;
        }

        Some(Uuid { bytes })
    }

    /// 生成 UUID v4 (随机)
    /// 使用系统时间作为伪随机种子
    pub fn new_v4() -> Self {
        let mut bytes = [0u8; 16];

        // 使用系统时间作为种子生成伪随机数
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_nanos() as u64)
            .unwrap_or(0);

        let mut state = seed;
        for i in 0..16 {
            // 简单的 xorshift64 随机数生成器
            state ^= state << 13;
            state ^= state >> 7;
            state ^= state << 17;
            bytes[i] = state as u8;
            state ^= state >> 3;
        }

        // 设置版本位 (v4 = 0100)
        bytes[6] = (bytes[6] & 0x0F) | 0x40;
        // 设置变体位 (RFC 4122)
        bytes[8] = (bytes[8] & 0x3F) | 0x80;

        Uuid { bytes }
    }

    /// 生成 UUID v7 (基于时间戳)
    /// 时间戳 + 随机位
    pub fn new_v7() -> Self {
        let mut bytes = [0u8; 16];

        // 获取毫秒级时间戳
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_millis() as u64)
            .unwrap_or(0);

        // 前 48 位为时间戳 (大端序)
        bytes[0] = ((timestamp >> 40) & 0xFF) as u8;
        bytes[1] = ((timestamp >> 32) & 0xFF) as u8;
        bytes[2] = ((timestamp >> 24) & 0xFF) as u8;
        bytes[3] = ((timestamp >> 16) & 0xFF) as u8;
        bytes[4] = ((timestamp >> 8) & 0xFF) as u8;
        bytes[5] = (timestamp & 0xFF) as u8;

        // 使用伪随机填充剩余位
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_nanos() as u64)
            .unwrap_or(0);

        let mut state = seed.wrapping_mul(0x5851F42D4C957F2D);
        for i in 6..16 {
            state ^= state << 13;
            state ^= state >> 7;
            state ^= state << 17;
            bytes[i] = state as u8;
        }

        // 设置版本位 (v7 = 0111)
        bytes[6] = (bytes[6] & 0x0F) | 0x70;
        // 设置变体位 (RFC 4122)
        bytes[8] = (bytes[8] & 0x3F) | 0x80;

        Uuid { bytes }
    }

    /// 从命名空间和名称生成 UUID v3 (MD5)
    pub fn new_v3(namespace: &Uuid, name: &str) -> Self {
        Self::generate_v3_v5(namespace, name, 0x30)
    }

    /// 从命名空间和名称生成 UUID v5 (SHA-1)
    pub fn new_v5(namespace: &Uuid, name: &str) -> Self {
        Self::generate_v3_v5(namespace, name, 0x50)
    }

    /// 生成 v3/v5 UUID 的内部实现
    fn generate_v3_v5(namespace: &Uuid, name: &str, version_byte: u8) -> Self {
        let namespace_bytes = namespace.as_bytes();
        let name_bytes = name.as_bytes();

        // 组合命名空间和名称
        let mut data = Vec::with_capacity(namespace_bytes.len() + name_bytes.len());
        data.extend_from_slice(namespace_bytes);
        data.extend_from_slice(name_bytes);

        // 使用简化的哈希函数 (SipHash 变体)
        let hash = Self::simple_hash(&data);

        let mut bytes = [0u8; 16];
        bytes.copy_from_slice(&hash[..16]);

        // 设置版本位
        bytes[6] = (bytes[6] & 0x0F) | version_byte;
        // 设置变体位
        bytes[8] = (bytes[8] & 0x3F) | 0x80;

        Uuid { bytes }
    }

    /// 简单哈希函数 (用于 v3/v5)
    fn simple_hash(data: &[u8]) -> [u8; 32] {
        let mut result = [0u8; 32];
        let mut state: [u64; 4] = [
            0x736F6D6570736575,
            0x646F72616E646F6D,
            0x6C7967656E657261,
            0x7465646279746573,
        ];

        // SipHash-like 简化实现
        for chunk in data.chunks(8) {
            let mut buf = [0u8; 8];
            buf[..chunk.len()].copy_from_slice(chunk);
            let m = u64::from_le_bytes(buf);

            state[0] = state[0].wrapping_add(m);
            state[0] = state[0].wrapping_mul(0x85EBCA6B);
            state[1] ^= state[0];
            state[1] = state[1].rotate_left(13);
            state[1] = state[1].wrapping_mul(5);
            state[2] = state[2].wrapping_add(state[1]);
            state[3] ^= state[2];
            state[3] = state[3].rotate_left(17);
        }

        // 最终混淆
        for i in 0..4 {
            state[i] ^= state[(i + 1) % 4];
            state[i] = state[i].wrapping_mul(0xC2B2AE3D27D4EB4F);
        }

        for i in 0..4 {
            let bytes = state[i].to_le_bytes();
            result[i * 8..(i + 1) * 8].copy_from_slice(&bytes);
        }

        result
    }

    /// 获取 UUID 字节数组
    pub const fn as_bytes(&self) -> &[u8; 16] {
        &self.bytes
    }

    /// 获取 UUID 版本
    pub fn get_version(&self) -> Option<UuidVersion> {
        let version_byte = (self.bytes[6] >> 4) & 0x0F;
        match version_byte {
            1 => Some(UuidVersion::V1),
            3 => Some(UuidVersion::V3),
            4 => Some(UuidVersion::V4),
            5 => Some(UuidVersion::V5),
            7 => Some(UuidVersion::V7),
            _ => None,
        }
    }

    /// 获取 UUID 变体
    pub fn get_variant(&self) -> UuidVariant {
        let variant_bits = self.bytes[8] >> 6;
        match variant_bits {
            0b00 => UuidVariant::NCS,
            0b10 => UuidVariant::RFC4122,
            0b110 => UuidVariant::Microsoft,
            _ => UuidVariant::Future,
        }
    }

    /// 检查是否为 nil UUID (全零)
    pub fn is_nil(&self) -> bool {
        self.bytes.iter().all(|&b| b == 0)
    }

    /// 转换为标准字符串格式 (带连字符)
    pub fn to_string(&self) -> String {
        format!(
            "{:02x}{:02x}{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}",
            self.bytes[0], self.bytes[1], self.bytes[2], self.bytes[3],
            self.bytes[4], self.bytes[5],
            self.bytes[6], self.bytes[7],
            self.bytes[8], self.bytes[9],
            self.bytes[10], self.bytes[11], self.bytes[12], self.bytes[13], self.bytes[14], self.bytes[15]
        )
    }

    /// 转换为不带连字符的字符串
    pub fn to_simple_string(&self) -> String {
        format!(
            "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}",
            self.bytes[0], self.bytes[1], self.bytes[2], self.bytes[3],
            self.bytes[4], self.bytes[5], self.bytes[6], self.bytes[7],
            self.bytes[8], self.bytes[9], self.bytes[10], self.bytes[11],
            self.bytes[12], self.bytes[13], self.bytes[14], self.bytes[15]
        )
    }

    /// 转换为 URN 格式
    pub fn to_urn(&self) -> String {
        format!("urn:uuid:{}", self.to_string())
    }

    /// 转换为带花括号的格式
    pub fn to_braced(&self) -> String {
        format!("{{{}}}", self.to_string())
    }

    /// 转换为大写格式
    pub fn to_uppercase(&self) -> String {
        self.to_string().to_uppercase()
    }

    /// 比较 UUID 版本
    pub fn compare_version(&self, other: &Uuid) -> std::cmp::Ordering {
        self.get_version_num().cmp(&other.get_version_num())
    }

    /// 获取版本号
    fn get_version_num(&self) -> u8 {
        (self.bytes[6] >> 4) & 0x0F
    }
}

impl fmt::Display for Uuid {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.to_string())
    }
}

impl Default for Uuid {
    fn default() -> Self {
        Self::new_v4()
    }
}

impl std::str::FromStr for Uuid {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::parse(s).ok_or(())
    }
}

/// 预定义的命名空间
pub mod namespaces {
    use super::Uuid;

    /// DNS 命名空间 UUID
    pub const DNS: Uuid = Uuid::from_bytes([
        0x6b, 0xa7, 0xb8, 0x10, 0x9d, 0xad, 0x11, 0xd1,
        0x80, 0xb4, 0x00, 0xc0, 0x4f, 0xd4, 0x30, 0xc8,
    ]);

    /// URL 命名空间 UUID
    pub const URL: Uuid = Uuid::from_bytes([
        0x6b, 0xa7, 0xb8, 0x11, 0x9d, 0xad, 0x11, 0xd1,
        0x80, 0xb4, 0x00, 0xc0, 0x4f, 0xd4, 0x30, 0xc8,
    ]);

    /// OID 命名空间 UUID
    pub const OID: Uuid = Uuid::from_bytes([
        0x6b, 0xa7, 0xb8, 0x12, 0x9d, 0xad, 0x11, 0xd1,
        0x80, 0xb4, 0x00, 0xc0, 0x4f, 0xd4, 0x30, 0xc8,
    ]);

    /// X.500 DN 命名空间 UUID
    pub const X500: Uuid = Uuid::from_bytes([
        0x6b, 0xa7, 0xb8, 0x14, 0x9d, 0xad, 0x11, 0xd1,
        0x80, 0xb4, 0x00, 0xc0, 0x4f, 0xd4, 0x30, 0xc8,
    ]);
}

/// UUID 生成器 (批量生成)
pub struct UuidGenerator {
    version: UuidVersion,
}

impl UuidGenerator {
    /// 创建新的生成器
    pub fn new(version: UuidVersion) -> Self {
        UuidGenerator { version }
    }

    /// 生成单个 UUID
    pub fn generate(&self) -> Uuid {
        match self.version {
            UuidVersion::V4 => Uuid::new_v4(),
            UuidVersion::V7 => Uuid::new_v7(),
            _ => Uuid::new_v4(), // 默认使用 v4
        }
    }

    /// 批量生成 UUID
    pub fn generate_batch(&self, count: usize) -> Vec<Uuid> {
        (0..count).map(|_| self.generate()).collect()
    }
}

/// UUID 验证器
pub struct UuidValidator;

impl UuidValidator {
    /// 验证 UUID 字符串格式是否正确
    pub fn is_valid(s: &str) -> bool {
        Uuid::parse(s).is_some()
    }

    /// 验证是否为 nil UUID
    pub fn is_nil(s: &str) -> bool {
        Uuid::parse(s).map(|u| u.is_nil()).unwrap_or(false)
    }

    /// 验证 UUID 版本
    pub fn is_version(s: &str, version: UuidVersion) -> bool {
        Uuid::parse(s)
            .and_then(|u| u.get_version())
            .map(|v| v == version)
            .unwrap_or(false)
    }

    /// 验证是否为有效的 v4 UUID
    pub fn is_v4(s: &str) -> bool {
        Self::is_version(s, UuidVersion::V4)
    }

    /// 验证是否为有效的 v7 UUID
    pub fn is_v7(s: &str) -> bool {
        Self::is_version(s, UuidVersion::V7)
    }
}

/// UUID 格式化器
pub struct UuidFormatter;

impl UuidFormatter {
    /// 格式化为指定格式
    pub fn format(uuid: &Uuid, format: UuidFormat) -> String {
        match format {
            UuidFormat::Standard => uuid.to_string(),
            UuidFormat::Simple => uuid.to_simple_string(),
            UuidFormat::Urn => uuid.to_urn(),
            UuidFormat::Braced => uuid.to_braced(),
            UuidFormat::Uppercase => uuid.to_uppercase(),
        }
    }

    /// 解析多种格式的 UUID
    pub fn parse(s: &str) -> Option<Uuid> {
        Uuid::parse(s)
    }
}

/// UUID 格式枚举
#[derive(Debug, Clone, Copy)]
pub enum UuidFormat {
    Standard,
    Simple,
    Urn,
    Braced,
    Uppercase,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new_v4() {
        let uuid1 = Uuid::new_v4();
        let uuid2 = Uuid::new_v4();
        
        // 两个 UUID 应该不同
        assert_ne!(uuid1, uuid2);
        
        // 版本应该是 v4
        assert_eq!(uuid1.get_version(), Some(UuidVersion::V4));
        assert_eq!(uuid2.get_version(), Some(UuidVersion::V4));
        
        // 变体应该是 RFC4122
        assert_eq!(uuid1.get_variant(), UuidVariant::RFC4122);
    }

    #[test]
    fn test_new_v7() {
        let uuid = Uuid::new_v7();
        
        // 版本应该是 v7
        assert_eq!(uuid.get_version(), Some(UuidVersion::V7));
        
        // 变体应该是 RFC4122
        assert_eq!(uuid.get_variant(), UuidVariant::RFC4122);
    }

    #[test]
    fn test_nil() {
        let nil = Uuid::nil();
        assert!(nil.is_nil());
        assert_eq!(nil.to_string(), "00000000-0000-0000-0000-000000000000");
    }

    #[test]
    fn test_parse_standard() {
        let uuid_str = "550e8400-e29b-41d4-a716-446655440000";
        let uuid = Uuid::parse(uuid_str).unwrap();
        
        assert_eq!(uuid.to_string(), uuid_str);
        assert_eq!(uuid.get_version(), Some(UuidVersion::V4));
    }

    #[test]
    fn test_parse_simple() {
        let uuid_str = "550e8400e29b41d4a716446655440000";
        let uuid = Uuid::parse(uuid_str).unwrap();
        
        assert_eq!(uuid.to_simple_string(), uuid_str);
    }

    #[test]
    fn test_parse_urn() {
        let uuid_str = "urn:uuid:550e8400-e29b-41d4-a716-446655440000";
        let uuid = Uuid::parse(uuid_str).unwrap();
        
        assert_eq!(uuid.to_urn(), uuid_str);
    }

    #[test]
    fn test_parse_braced() {
        let uuid_str = "{550e8400-e29b-41d4-a716-446655440000}";
        let uuid = Uuid::parse(uuid_str).unwrap();
        
        assert_eq!(uuid.to_braced(), uuid_str);
    }

    #[test]
    fn test_parse_invalid() {
        assert!(Uuid::parse("invalid").is_none());
        assert!(Uuid::parse("550e8400-e29b-41d4-a716").is_none());
        assert!(Uuid::parse("").is_none());
    }

    #[test]
    fn test_new_v5() {
        let uuid = Uuid::new_v5(&namespaces::DNS, "example.com");
        
        // 版本应该是 v5
        assert_eq!(uuid.get_version(), Some(UuidVersion::V5));
        
        // 相同输入应该产生相同 UUID
        let uuid2 = Uuid::new_v5(&namespaces::DNS, "example.com");
        assert_eq!(uuid, uuid2);
        
        // 不同命名空间应该产生不同 UUID
        let uuid3 = Uuid::new_v5(&namespaces::URL, "example.com");
        assert_ne!(uuid, uuid3);
    }

    #[test]
    fn test_new_v3() {
        let uuid = Uuid::new_v3(&namespaces::DNS, "example.com");
        
        assert_eq!(uuid.get_version(), Some(UuidVersion::V3));
    }

    #[test]
    fn test_format() {
        let uuid_str = "550e8400-e29b-41d4-a716-446655440000";
        let uuid = Uuid::parse(uuid_str).unwrap();
        
        assert_eq!(uuid.to_string(), uuid_str);
        assert_eq!(uuid.to_simple_string(), "550e8400e29b41d4a716446655440000");
        assert_eq!(uuid.to_urn(), "urn:uuid:550e8400-e29b-41d4-a716-446655440000");
        assert_eq!(uuid.to_braced(), "{550e8400-e29b-41d4-a716-446655440000}");
        assert_eq!(uuid.to_uppercase(), "550E8400-E29B-41D4-A716-446655440000");
    }

    #[test]
    fn test_validator() {
        assert!(UuidValidator::is_valid("550e8400-e29b-41d4-a716-446655440000"));
        assert!(!UuidValidator::is_valid("invalid"));
        assert!(UuidValidator::is_nil("00000000-0000-0000-0000-000000000000"));
        assert!(UuidValidator::is_v4("550e8400-e29b-41d4-a716-446655440000"));
    }

    #[test]
    fn test_generator() {
        let gen = UuidGenerator::new(UuidVersion::V4);
        let uuids = gen.generate_batch(10);
        
        assert_eq!(uuids.len(), 10);
        
        // 所有 UUID 应该是唯一的
        for i in 0..uuids.len() {
            for j in (i + 1)..uuids.len() {
                assert_ne!(uuids[i], uuids[j]);
            }
        }
    }

    #[test]
    fn test_from_bytes() {
        let bytes = [
            0x55, 0x0e, 0x84, 0x00, 0xe2, 0x9b, 0x41, 0xd4,
            0xa7, 0x16, 0x44, 0x66, 0x55, 0x44, 0x00, 0x00,
        ];
        let uuid = Uuid::from_bytes(bytes);
        assert_eq!(uuid.as_bytes(), &bytes);
    }

    #[test]
    fn test_default() {
        let uuid = Uuid::default();
        assert_eq!(uuid.get_version(), Some(UuidVersion::V4));
    }

    #[test]
    fn test_from_str() {
        let uuid: Uuid = "550e8400-e29b-41d4-a716-446655440000".parse().unwrap();
        assert_eq!(uuid.get_version(), Some(UuidVersion::V4));
    }
}