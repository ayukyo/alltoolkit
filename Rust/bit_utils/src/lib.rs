//! # Bit Utils
//!
//! A comprehensive collection of bit manipulation utilities for Rust.
//! Zero external dependencies, pure Rust implementation.
//!
//! ## Features
//! - Bit counting (set bits, unset bits)
//! - Bit position finding (first set, last set, etc.)
//! - Bit reversal and rotation
//! - Bit masking utilities
//! - Gray code conversion
//! - Parity checking
//! - Bit field operations
//! - Binary string formatting

#![forbid(unsafe_code)]
#![warn(missing_docs)]

/// Bit manipulation trait for unsigned integers
pub trait BitOps: Copy + Clone {
    /// Count the number of set bits (population count)
    fn count_ones(self) -> u32;
    
    /// Count the number of unset bits
    fn count_zeros(self) -> u32;
    
    /// Get the position of the least significant set bit (0-indexed)
    /// Returns None if no bits are set
    fn first_set_bit(self) -> Option<u32>;
    
    /// Get the position of the most significant set bit (0-indexed)
    /// Returns None if no bits are set
    fn last_set_bit(self) -> Option<u32>;
    
    /// Get the position of the least significant unset bit (0-indexed)
    fn first_unset_bit(self) -> u32;
    
    /// Check if a specific bit is set
    fn is_bit_set(self, pos: u32) -> bool;
    
    /// Set a specific bit
    fn set_bit(self, pos: u32) -> Self;
    
    /// Clear a specific bit
    fn clear_bit(self, pos: u32) -> Self;
    
    /// Toggle a specific bit
    fn toggle_bit(self, pos: u32) -> Self;
    
    /// Reverse all bits
    fn reverse_bits(self) -> Self;
    
    /// Rotate left by n positions
    fn rotate_left_bits(self, n: u32) -> Self;
    
    /// Rotate right by n positions
    fn rotate_right_bits(self, n: u32) -> Self;
    
    /// Get the number of bits
    fn bit_width() -> u32;
    
    /// Create a mask with bits [start, end] set (inclusive)
    fn mask_range(start: u32, end: u32) -> Self;
    
    /// Extract bits [start, end] (inclusive)
    fn extract_bits(self, start: u32, end: u32) -> Self;
    
    /// Count leading zeros
    fn leading_zeros(self) -> u32;
    
    /// Count trailing zeros
    fn trailing_zeros(self) -> u32;
    
    /// Count leading ones
    fn leading_ones(self) -> u32;
    
    /// Count trailing ones
    fn trailing_ones(self) -> u32;
}

/// Implement BitOps for u8
impl BitOps for u8 {
    fn count_ones(self) -> u32 {
        self.count_ones()
    }
    
    fn count_zeros(self) -> u32 {
        self.count_zeros()
    }
    
    fn first_set_bit(self) -> Option<u32> {
        if self == 0 {
            None
        } else {
            Some(self.trailing_zeros())
        }
    }
    
    fn last_set_bit(self) -> Option<u32> {
        if self == 0 {
            None
        } else {
            Some(7 - self.leading_zeros())
        }
    }
    
    fn first_unset_bit(self) -> u32 {
        (!self).trailing_zeros().min(8)
    }
    
    fn is_bit_set(self, pos: u32) -> bool {
        if pos >= 8 {
            return false;
        }
        (self & (1 << pos)) != 0
    }
    
    fn set_bit(self, pos: u32) -> Self {
        if pos >= 8 {
            return self;
        }
        self | (1 << pos)
    }
    
    fn clear_bit(self, pos: u32) -> Self {
        if pos >= 8 {
            return self;
        }
        self & !(1 << pos)
    }
    
    fn toggle_bit(self, pos: u32) -> Self {
        if pos >= 8 {
            return self;
        }
        self ^ (1 << pos)
    }
    
    fn reverse_bits(self) -> Self {
        self.reverse_bits()
    }
    
    fn rotate_left_bits(self, n: u32) -> Self {
        self.rotate_left(n)
    }
    
    fn rotate_right_bits(self, n: u32) -> Self {
        self.rotate_right(n)
    }
    
    fn bit_width() -> u32 {
        8
    }
    
    fn mask_range(start: u32, end: u32) -> Self {
        if start > end || end >= 8 {
            return 0;
        }
        let len = end - start + 1;
        let mask: u8 = ((1u16 << len) - 1) as u8;
        mask << start
    }
    
    fn extract_bits(self, start: u32, end: u32) -> Self {
        let mask = Self::mask_range(start, end);
        (self & mask) >> start
    }
    
    fn leading_zeros(self) -> u32 {
        self.leading_zeros()
    }
    
    fn trailing_zeros(self) -> u32 {
        self.trailing_zeros()
    }
    
    fn leading_ones(self) -> u32 {
        self.leading_ones()
    }
    
    fn trailing_ones(self) -> u32 {
        self.trailing_ones()
    }
}

/// Implement BitOps for u16
impl BitOps for u16 {
    fn count_ones(self) -> u32 {
        self.count_ones()
    }
    
    fn count_zeros(self) -> u32 {
        self.count_zeros()
    }
    
    fn first_set_bit(self) -> Option<u32> {
        if self == 0 {
            None
        } else {
            Some(self.trailing_zeros())
        }
    }
    
    fn last_set_bit(self) -> Option<u32> {
        if self == 0 {
            None
        } else {
            Some(15 - self.leading_zeros())
        }
    }
    
    fn first_unset_bit(self) -> u32 {
        (!self).trailing_zeros().min(16)
    }
    
    fn is_bit_set(self, pos: u32) -> bool {
        if pos >= 16 {
            return false;
        }
        (self & (1 << pos)) != 0
    }
    
    fn set_bit(self, pos: u32) -> Self {
        if pos >= 16 {
            return self;
        }
        self | (1 << pos)
    }
    
    fn clear_bit(self, pos: u32) -> Self {
        if pos >= 16 {
            return self;
        }
        self & !(1 << pos)
    }
    
    fn toggle_bit(self, pos: u32) -> Self {
        if pos >= 16 {
            return self;
        }
        self ^ (1 << pos)
    }
    
    fn reverse_bits(self) -> Self {
        self.reverse_bits()
    }
    
    fn rotate_left_bits(self, n: u32) -> Self {
        self.rotate_left(n)
    }
    
    fn rotate_right_bits(self, n: u32) -> Self {
        self.rotate_right(n)
    }
    
    fn bit_width() -> u32 {
        16
    }
    
    fn mask_range(start: u32, end: u32) -> Self {
        if start > end || end >= 16 {
            return 0;
        }
        let len = end - start + 1;
        let mask: u16 = ((1u32 << len) - 1) as u16;
        mask << start
    }
    
    fn extract_bits(self, start: u32, end: u32) -> Self {
        let mask = Self::mask_range(start, end);
        (self & mask) >> start
    }
    
    fn leading_zeros(self) -> u32 {
        self.leading_zeros()
    }
    
    fn trailing_zeros(self) -> u32 {
        self.trailing_zeros()
    }
    
    fn leading_ones(self) -> u32 {
        self.leading_ones()
    }
    
    fn trailing_ones(self) -> u32 {
        self.trailing_ones()
    }
}

/// Implement BitOps for u32
impl BitOps for u32 {
    fn count_ones(self) -> u32 {
        self.count_ones()
    }
    
    fn count_zeros(self) -> u32 {
        self.count_zeros()
    }
    
    fn first_set_bit(self) -> Option<u32> {
        if self == 0 {
            None
        } else {
            Some(self.trailing_zeros())
        }
    }
    
    fn last_set_bit(self) -> Option<u32> {
        if self == 0 {
            None
        } else {
            Some(31 - self.leading_zeros())
        }
    }
    
    fn first_unset_bit(self) -> u32 {
        (!self).trailing_zeros().min(32)
    }
    
    fn is_bit_set(self, pos: u32) -> bool {
        if pos >= 32 {
            return false;
        }
        (self & (1 << pos)) != 0
    }
    
    fn set_bit(self, pos: u32) -> Self {
        if pos >= 32 {
            return self;
        }
        self | (1 << pos)
    }
    
    fn clear_bit(self, pos: u32) -> Self {
        if pos >= 32 {
            return self;
        }
        self & !(1 << pos)
    }
    
    fn toggle_bit(self, pos: u32) -> Self {
        if pos >= 32 {
            return self;
        }
        self ^ (1 << pos)
    }
    
    fn reverse_bits(self) -> Self {
        self.reverse_bits()
    }
    
    fn rotate_left_bits(self, n: u32) -> Self {
        self.rotate_left(n)
    }
    
    fn rotate_right_bits(self, n: u32) -> Self {
        self.rotate_right(n)
    }
    
    fn bit_width() -> u32 {
        32
    }
    
    fn mask_range(start: u32, end: u32) -> Self {
        if start > end || end >= 32 {
            return 0;
        }
        let len = end - start + 1;
        let mask: u32 = ((1u64 << len) - 1) as u32;
        mask << start
    }
    
    fn extract_bits(self, start: u32, end: u32) -> Self {
        let mask = Self::mask_range(start, end);
        (self & mask) >> start
    }
    
    fn leading_zeros(self) -> u32 {
        self.leading_zeros()
    }
    
    fn trailing_zeros(self) -> u32 {
        self.trailing_zeros()
    }
    
    fn leading_ones(self) -> u32 {
        self.leading_ones()
    }
    
    fn trailing_ones(self) -> u32 {
        self.trailing_ones()
    }
}

/// Implement BitOps for u64
impl BitOps for u64 {
    fn count_ones(self) -> u32 {
        self.count_ones()
    }
    
    fn count_zeros(self) -> u32 {
        self.count_zeros()
    }
    
    fn first_set_bit(self) -> Option<u32> {
        if self == 0 {
            None
        } else {
            Some(self.trailing_zeros())
        }
    }
    
    fn last_set_bit(self) -> Option<u32> {
        if self == 0 {
            None
        } else {
            Some(63 - self.leading_zeros())
        }
    }
    
    fn first_unset_bit(self) -> u32 {
        (!self).trailing_zeros().min(64)
    }
    
    fn is_bit_set(self, pos: u32) -> bool {
        if pos >= 64 {
            return false;
        }
        (self & (1 << pos)) != 0
    }
    
    fn set_bit(self, pos: u32) -> Self {
        if pos >= 64 {
            return self;
        }
        self | (1 << pos)
    }
    
    fn clear_bit(self, pos: u32) -> Self {
        if pos >= 64 {
            return self;
        }
        self & !(1 << pos)
    }
    
    fn toggle_bit(self, pos: u32) -> Self {
        if pos >= 64 {
            return self;
        }
        self ^ (1 << pos)
    }
    
    fn reverse_bits(self) -> Self {
        self.reverse_bits()
    }
    
    fn rotate_left_bits(self, n: u32) -> Self {
        self.rotate_left(n)
    }
    
    fn rotate_right_bits(self, n: u32) -> Self {
        self.rotate_right(n)
    }
    
    fn bit_width() -> u32 {
        64
    }
    
    fn mask_range(start: u32, end: u32) -> Self {
        if start > end || end >= 64 {
            return 0;
        }
        let len = end - start + 1;
        let mask: u64 = ((1u128 << len) - 1) as u64;
        mask << start
    }
    
    fn extract_bits(self, start: u32, end: u32) -> Self {
        let mask = Self::mask_range(start, end);
        (self & mask) >> start
    }
    
    fn leading_zeros(self) -> u32 {
        self.leading_zeros()
    }
    
    fn trailing_zeros(self) -> u32 {
        self.trailing_zeros()
    }
    
    fn leading_ones(self) -> u32 {
        self.leading_ones()
    }
    
    fn trailing_ones(self) -> u32 {
        self.trailing_ones()
    }
}

/// Implement BitOps for u128
impl BitOps for u128 {
    fn count_ones(self) -> u32 {
        self.count_ones()
    }
    
    fn count_zeros(self) -> u32 {
        self.count_zeros()
    }
    
    fn first_set_bit(self) -> Option<u32> {
        if self == 0 {
            None
        } else {
            Some(self.trailing_zeros())
        }
    }
    
    fn last_set_bit(self) -> Option<u32> {
        if self == 0 {
            None
        } else {
            Some(127 - self.leading_zeros())
        }
    }
    
    fn first_unset_bit(self) -> u32 {
        (!self).trailing_zeros().min(128)
    }
    
    fn is_bit_set(self, pos: u32) -> bool {
        if pos >= 128 {
            return false;
        }
        (self & (1 << pos)) != 0
    }
    
    fn set_bit(self, pos: u32) -> Self {
        if pos >= 128 {
            return self;
        }
        self | (1 << pos)
    }
    
    fn clear_bit(self, pos: u32) -> Self {
        if pos >= 128 {
            return self;
        }
        self & !(1 << pos)
    }
    
    fn toggle_bit(self, pos: u32) -> Self {
        if pos >= 128 {
            return self;
        }
        self ^ (1 << pos)
    }
    
    fn reverse_bits(self) -> Self {
        self.reverse_bits()
    }
    
    fn rotate_left_bits(self, n: u32) -> Self {
        self.rotate_left(n)
    }
    
    fn rotate_right_bits(self, n: u32) -> Self {
        self.rotate_right(n)
    }
    
    fn bit_width() -> u32 {
        128
    }
    
    fn mask_range(start: u32, end: u32) -> Self {
        if start > end || end >= 128 {
            return 0;
        }
        let len = end - start + 1;
        // Handle the full 128-bit case
        let mask = if len >= 128 {
            !0u128
        } else {
            (1u128 << len) - 1
        };
        mask << start
    }
    
    fn extract_bits(self, start: u32, end: u32) -> Self {
        let mask = Self::mask_range(start, end);
        (self & mask) >> start
    }
    
    fn leading_zeros(self) -> u32 {
        self.leading_zeros()
    }
    
    fn trailing_zeros(self) -> u32 {
        self.trailing_zeros()
    }
    
    fn leading_ones(self) -> u32 {
        self.leading_ones()
    }
    
    fn trailing_ones(self) -> u32 {
        self.trailing_ones()
    }
}

/// Implement BitOps for usize
impl BitOps for usize {
    fn count_ones(self) -> u32 {
        self.count_ones()
    }
    
    fn count_zeros(self) -> u32 {
        self.count_zeros()
    }
    
    fn first_set_bit(self) -> Option<u32> {
        if self == 0 {
            None
        } else {
            Some(self.trailing_zeros())
        }
    }
    
    fn last_set_bit(self) -> Option<u32> {
        if self == 0 {
            None
        } else {
            Some((std::mem::size_of::<usize>() * 8 - 1) as u32 - self.leading_zeros())
        }
    }
    
    fn first_unset_bit(self) -> u32 {
        (!self).trailing_zeros().min(std::mem::size_of::<usize>() as u32 * 8)
    }
    
    fn is_bit_set(self, pos: u32) -> bool {
        let width = std::mem::size_of::<usize>() as u32 * 8;
        if pos >= width {
            return false;
        }
        (self & (1 << pos)) != 0
    }
    
    fn set_bit(self, pos: u32) -> Self {
        let width = std::mem::size_of::<usize>() as u32 * 8;
        if pos >= width {
            return self;
        }
        self | (1 << pos)
    }
    
    fn clear_bit(self, pos: u32) -> Self {
        let width = std::mem::size_of::<usize>() as u32 * 8;
        if pos >= width {
            return self;
        }
        self & !(1 << pos)
    }
    
    fn toggle_bit(self, pos: u32) -> Self {
        let width = std::mem::size_of::<usize>() as u32 * 8;
        if pos >= width {
            return self;
        }
        self ^ (1 << pos)
    }
    
    fn reverse_bits(self) -> Self {
        self.reverse_bits()
    }
    
    fn rotate_left_bits(self, n: u32) -> Self {
        self.rotate_left(n)
    }
    
    fn rotate_right_bits(self, n: u32) -> Self {
        self.rotate_right(n)
    }
    
    fn bit_width() -> u32 {
        std::mem::size_of::<usize>() as u32 * 8
    }
    
    fn mask_range(start: u32, end: u32) -> Self {
        let width = std::mem::size_of::<usize>() as u32 * 8;
        if start > end || end >= width {
            return 0;
        }
        let len = end - start + 1;
        let mask: usize = ((1u128 << len) - 1) as usize;
        mask << start
    }
    
    fn extract_bits(self, start: u32, end: u32) -> Self {
        let mask = Self::mask_range(start, end);
        (self & mask) >> start
    }
    
    fn leading_zeros(self) -> u32 {
        self.leading_zeros()
    }
    
    fn trailing_zeros(self) -> u32 {
        self.trailing_zeros()
    }
    
    fn leading_ones(self) -> u32 {
        self.leading_ones()
    }
    
    fn trailing_ones(self) -> u32 {
        self.trailing_ones()
    }
}

/// Convert a number to its binary representation as a string
/// 
/// # Example
/// ```
/// use bit_utils::to_binary_string;
/// assert_eq!(to_binary_string(5u8), "00000101");
/// ```
pub fn to_binary_string<T: BitOps>(value: T) -> String {
    let width = T::bit_width() as usize;
    let mut result = String::with_capacity(width);
    for i in (0..width).rev() {
        result.push(if value.is_bit_set(i as u32) { '1' } else { '0' });
    }
    result
}

/// Convert a number to its hexadecimal representation as a string
/// 
/// # Example
/// ```
/// use bit_utils::to_hex_string;
/// assert_eq!(to_hex_string(255u8), "FF");
/// ```
pub fn to_hex_string<T: std::fmt::UpperHex>(value: T) -> String {
    format!("{:X}", value)
}

/// Check if a number has even parity (even number of set bits)
pub fn has_even_parity<T: BitOps>(value: T) -> bool {
    value.count_ones() % 2 == 0
}

/// Check if a number has odd parity (odd number of set bits)
pub fn has_odd_parity<T: BitOps>(value: T) -> bool {
    value.count_ones() % 2 == 1
}

/// Compute parity bit (0 for even parity, 1 for odd parity)
pub fn parity_bit<T: BitOps>(value: T) -> u32 {
    value.count_ones() % 2
}

/// Convert binary number to Gray code
/// 
/// # Example
/// ```
/// use bit_utils::binary_to_gray;
/// assert_eq!(binary_to_gray(4u8), 6);
/// ```
pub fn binary_to_gray<T: BitOps + std::ops::Shr<i32, Output = T> + std::ops::BitXor<Output = T>>(value: T) -> T {
    value ^ (value >> 1)
}

/// Convert Gray code back to binary (for u8)
pub fn gray_to_binary_u8(gray: u8) -> u8 {
    let mut binary = gray;
    let mut mask = gray >> 1;
    while mask != 0 {
        binary ^= mask;
        mask >>= 1;
    }
    binary
}

/// Convert Gray code back to binary (for u16)
pub fn gray_to_binary_u16(gray: u16) -> u16 {
    let mut binary = gray;
    let mut mask = gray >> 1;
    while mask != 0 {
        binary ^= mask;
        mask >>= 1;
    }
    binary
}

/// Convert Gray code back to binary (for u32)
pub fn gray_to_binary_u32(gray: u32) -> u32 {
    let mut binary = gray;
    let mut mask = gray >> 1;
    while mask != 0 {
        binary ^= mask;
        mask >>= 1;
    }
    binary
}

/// Convert Gray code back to binary (for u64)
pub fn gray_to_binary_u64(gray: u64) -> u64 {
    let mut binary = gray;
    let mut mask = gray >> 1;
    while mask != 0 {
        binary ^= mask;
        mask >>= 1;
    }
    binary
}

/// Convert Gray code back to binary (for u128)
pub fn gray_to_binary_u128(gray: u128) -> u128 {
    let mut binary = gray;
    let mut mask = gray >> 1;
    while mask != 0 {
        binary ^= mask;
        mask >>= 1;
    }
    binary
}

/// Convert Gray code back to binary (for usize)
pub fn gray_to_binary_usize(gray: usize) -> usize {
    let mut binary = gray;
    let mut mask = gray >> 1;
    while mask != 0 {
        binary ^= mask;
        mask >>= 1;
    }
    binary
}

/// Convert Gray code back to binary
/// 
/// # Example
/// ```
/// use bit_utils::gray_to_binary;
/// assert_eq!(gray_to_binary(6u8), 4);
/// ```
pub fn gray_to_binary<T: BitOps>(gray: T) -> T
where
    T: std::ops::Shr<i32, Output = T> + std::ops::BitXor<Output = T> + Default + PartialEq + Copy
{
    let zero: T = Default::default();
    let mut binary = gray;
    let mut mask: T = gray >> 1;
    while mask != zero {
        binary = binary ^ mask;
        mask = mask >> 1;
    }
    binary
}

/// Swap the two halves of a number
/// 
/// # Example
/// ```
/// use bit_utils::swap_halves;
/// assert_eq!(swap_halves(0x12345678u32), 0x56781234);
/// ```
pub fn swap_halves<T: BitOps + std::ops::Shl<u32, Output = T> + std::ops::BitOr<Output = T>>(value: T) -> T {
    let half = T::bit_width() / 2;
    let upper = value.extract_bits(half, T::bit_width() - 1);
    let lower = value.extract_bits(0, half - 1);
    (lower << half) | upper
}

/// Interleave bits from two numbers (Morton/Z-order curve)
/// Returns a number with interleaved bits (up to 64 bits total)
pub fn interleave_bits(a: u32, b: u32) -> u64 {
    let mut result: u64 = 0;
    for i in 0..32 {
        result |= (((a >> i) & 1) as u64) << (2 * i);
        result |= (((b >> i) & 1) as u64) << (2 * i + 1);
    }
    result
}

/// Deinterleave bits into two numbers (reverse of interleave_bits)
pub fn deinterleave_bits(z: u64) -> (u32, u32) {
    let mut a: u32 = 0;
    let mut b: u32 = 0;
    for i in 0..32 {
        a |= (((z >> (2 * i)) & 1) as u32) << i;
        b |= (((z >> (2 * i + 1)) & 1) as u32) << i;
    }
    (a, b)
}

/// Find the next power of 2 greater than or equal to the given value
/// Returns None if the value is 0 or if the result would overflow
/// 
/// # Example
/// ```
/// use bit_utils::next_power_of_two;
/// assert_eq!(next_power_of_two(5u32), Some(8));
/// assert_eq!(next_power_of_two(8u32), Some(8));
/// ```
pub fn next_power_of_two<T: BitOps + TryFrom<u64> + Into<u64>>(value: T) -> Option<T> {
    let v: u64 = value.into();
    if v == 0 {
        return Some(1.try_into().ok()?);
    }
    if v.is_power_of_two() {
        return Some(value);
    }
    let next = 1u64 << (64 - v.leading_zeros());
    next.try_into().ok()
}

/// Check if a number is a power of 2
pub fn is_power_of_two<T: BitOps + Into<u64>>(value: T) -> bool {
    let v: u64 = value.into();
    v > 0 && (v & (v - 1)) == 0
}

/// Set all bits in the given positions
pub fn set_bits<T: BitOps>(value: T, positions: &[u32]) -> T {
    let mut result = value;
    for &pos in positions {
        result = result.set_bit(pos);
    }
    result
}

/// Clear all bits in the given positions
pub fn clear_bits<T: BitOps>(value: T, positions: &[u32]) -> T {
    let mut result = value;
    for &pos in positions {
        result = result.clear_bit(pos);
    }
    result
}

/// Toggle all bits in the given positions
pub fn toggle_bits<T: BitOps>(value: T, positions: &[u32]) -> T {
    let mut result = value;
    for &pos in positions {
        result = result.toggle_bit(pos);
    }
    result
}

/// Create a bitmask with the lowest n bits set
/// 
/// # Example
/// ```
/// use bit_utils::low_mask;
/// assert_eq!(low_mask::<u8>(4), 0b00001111);
/// ```
pub fn low_mask<T: BitOps + std::ops::Not<Output = T>>(n: u32) -> T {
    if n == 0 {
        return T::mask_range(0, 0).clear_bit(0);
    }
    if n >= T::bit_width() {
        return !T::mask_range(0, 0).clear_bit(0); // All bits set
    }
    T::mask_range(0, n - 1)
}

/// Create a bitmask with the highest n bits set
/// 
/// # Example
/// ```
/// use bit_utils::high_mask;
/// assert_eq!(high_mask::<u8>(4), 0b11110000);
/// ```
pub fn high_mask<T: BitOps + std::ops::Not<Output = T>>(n: u32) -> T {
    let width = T::bit_width();
    if n >= width {
        return !T::mask_range(0, 0).clear_bit(0); // All bits set
    }
    if n == 0 {
        return T::mask_range(0, 0).clear_bit(0); // 0
    }
    T::mask_range(width - n, width - 1)
}

/// Align value up to the given alignment (must be power of 2)
pub fn align_up<T>(value: T, alignment: T) -> Option<T>
where
    T: BitOps + std::ops::Add<Output = T> + std::ops::Sub<Output = T> + std::ops::BitAnd<Output = T> + std::ops::Not<Output = T> + Copy + Into<u64>
{
    let v: u64 = alignment.into();
    if v == 0 || (v & (v - 1)) != 0 {
        return None;
    }
    let one = T::mask_range(0, 0).set_bit(0);
    let mask = alignment - one;
    Some((value + alignment - one) & !mask)
}

/// Align value down to the given alignment (must be power of 2)
pub fn align_down<T>(value: T, alignment: T) -> Option<T>
where
    T: BitOps + std::ops::Sub<Output = T> + std::ops::BitAnd<Output = T> + std::ops::Not<Output = T> + Copy + Into<u64>
{
    let v: u64 = alignment.into();
    if v == 0 || (v & (v - 1)) != 0 {
        return None;
    }
    let one = T::mask_range(0, 0).set_bit(0);
    let mask = alignment - one;
    Some(value & !mask)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_count_ones() {
        assert_eq!(0b10101010u8.count_ones(), 4);
        assert_eq!(0b11111111u8.count_ones(), 8);
        assert_eq!(0u8.count_ones(), 0);
    }

    #[test]
    fn test_count_zeros() {
        assert_eq!(0b10101010u8.count_zeros(), 4);
        assert_eq!(0b11111111u8.count_zeros(), 0);
        assert_eq!(0u8.count_zeros(), 8);
    }

    #[test]
    fn test_first_set_bit() {
        assert_eq!(0b10000000u8.first_set_bit(), Some(7));
        assert_eq!(0b00000001u8.first_set_bit(), Some(0));
        assert_eq!(0b00010000u8.first_set_bit(), Some(4));
        assert_eq!(0u8.first_set_bit(), None);
    }

    #[test]
    fn test_last_set_bit() {
        assert_eq!(0b10000001u8.last_set_bit(), Some(7));
        assert_eq!(0b00000001u8.last_set_bit(), Some(0));
        assert_eq!(0b00010000u8.last_set_bit(), Some(4));
        assert_eq!(0u8.last_set_bit(), None);
    }

    #[test]
    fn test_bit_manipulation() {
        let val: u8 = 0b00000000;
        assert_eq!(val.set_bit(3), 0b00001000);
        assert_eq!(val.set_bit(7), 0b10000000);
        
        let val: u8 = 0b11111111;
        assert_eq!(val.clear_bit(3), 0b11110111);
        assert_eq!(val.clear_bit(0), 0b11111110);
        
        let val: u8 = 0b00001000;
        assert_eq!(val.toggle_bit(3), 0b00000000);
        assert_eq!(val.toggle_bit(0), 0b00001001);
    }

    #[test]
    fn test_is_bit_set() {
        let val: u8 = 0b10101010;
        assert!(val.is_bit_set(1));
        assert!(!val.is_bit_set(0));
        assert!(val.is_bit_set(7));
        assert!(!val.is_bit_set(6));
    }

    #[test]
    fn test_reverse_bits() {
        assert_eq!(0b11110000u8.reverse_bits(), 0b00001111);
        assert_eq!(0b10101010u8.reverse_bits(), 0b01010101);
    }

    #[test]
    fn test_rotate() {
        let val: u8 = 0b11010010;
        // rotate_left(2): high 2 bits (11) move to low, result = 0b01001011
        assert_eq!(val.rotate_left_bits(2), 0b01001011);
        // rotate_right(2): low 2 bits (10) move to high, result = 0b10110100
        assert_eq!(val.rotate_right_bits(2), 0b10110100);
    }

    #[test]
    fn test_mask_range() {
        assert_eq!(u8::mask_range(0, 3), 0b00001111);
        assert_eq!(u8::mask_range(4, 7), 0b11110000);
        assert_eq!(u8::mask_range(2, 5), 0b00111100);
    }

    #[test]
    fn test_extract_bits() {
        let val: u8 = 0b11011010;
        assert_eq!(val.extract_bits(0, 3), 0b1010);
        assert_eq!(val.extract_bits(4, 7), 0b1101);
    }

    #[test]
    fn test_to_binary_string() {
        assert_eq!(to_binary_string(5u8), "00000101");
        assert_eq!(to_binary_string(255u8), "11111111");
    }

    #[test]
    fn test_to_hex_string() {
        assert_eq!(to_hex_string(255u8), "FF");
        assert_eq!(to_hex_string(16u8), "10");
    }

    #[test]
    fn test_parity() {
        assert!(has_even_parity(0b10101010u8));
        assert!(!has_odd_parity(0b10101010u8));
        assert!(has_odd_parity(0b10101011u8));
        assert_eq!(parity_bit(0b10101010u8), 0);
        assert_eq!(parity_bit(0b10101011u8), 1);
    }

    #[test]
    fn test_gray_code() {
        // Test binary_to_gray
        assert_eq!(binary_to_gray(0u8), 0);
        assert_eq!(binary_to_gray(1u8), 1);
        assert_eq!(binary_to_gray(2u8), 3);
        assert_eq!(binary_to_gray(3u8), 2);
        assert_eq!(binary_to_gray(4u8), 6);
        
        // Test gray_to_binary_u8
        assert_eq!(gray_to_binary_u8(0), 0);
        assert_eq!(gray_to_binary_u8(1), 1);
        assert_eq!(gray_to_binary_u8(3), 2);
        assert_eq!(gray_to_binary_u8(2), 3);
        assert_eq!(gray_to_binary_u8(6), 4);
        
        // Test generic gray_to_binary
        assert_eq!(gray_to_binary(0u8), 0);
        assert_eq!(gray_to_binary(1u8), 1);
        assert_eq!(gray_to_binary(3u32), 2);
        assert_eq!(gray_to_binary(2u64), 3);
        assert_eq!(gray_to_binary(6u128), 4);
    }

    #[test]
    fn test_swap_halves() {
        assert_eq!(swap_halves(0x12345678u32), 0x56781234);
        assert_eq!(swap_halves(0x00FF00FFu32), 0x00FF00FF);
    }

    #[test]
    fn test_interleave_bits() {
        assert_eq!(interleave_bits(0, 0), 0);
        assert_eq!(interleave_bits(1, 0), 1);
        assert_eq!(interleave_bits(0, 1), 2);
        assert_eq!(interleave_bits(1, 1), 3);
        // interleave_bits(3, 5): 3=0b11, 5=0b101
        // bit positions: a[0]=1 at pos0, b[0]=1 at pos1, a[1]=1 at pos2, b[1]=0 at pos3, b[2]=1 at pos5
        // result = 0b100111 = 39
        assert_eq!(interleave_bits(3, 5), 0b100111);
    }

    #[test]
    fn test_deinterleave_bits() {
        assert_eq!(deinterleave_bits(0), (0, 0));
        assert_eq!(deinterleave_bits(1), (1, 0));
        assert_eq!(deinterleave_bits(2), (0, 1));
        assert_eq!(deinterleave_bits(3), (1, 1));
    }

    #[test]
    fn test_next_power_of_two() {
        assert_eq!(next_power_of_two(0u32), Some(1));
        assert_eq!(next_power_of_two(1u32), Some(1));
        assert_eq!(next_power_of_two(2u32), Some(2));
        assert_eq!(next_power_of_two(3u32), Some(4));
        assert_eq!(next_power_of_two(5u32), Some(8));
        assert_eq!(next_power_of_two(8u32), Some(8));
        assert_eq!(next_power_of_two(9u32), Some(16));
    }

    #[test]
    fn test_is_power_of_two() {
        assert!(!is_power_of_two(0u8));
        assert!(is_power_of_two(1u8));
        assert!(is_power_of_two(2u8));
        assert!(is_power_of_two(4u8));
        assert!(is_power_of_two(128u8));
        assert!(!is_power_of_two(3u8));
        assert!(!is_power_of_two(5u8));
    }

    #[test]
    fn test_low_mask() {
        assert_eq!(low_mask::<u8>(0), 0);
        assert_eq!(low_mask::<u8>(4), 0b00001111);
        assert_eq!(low_mask::<u8>(8), 0b11111111);
    }

    #[test]
    fn test_high_mask() {
        assert_eq!(high_mask::<u8>(0), 0);
        assert_eq!(high_mask::<u8>(4), 0b11110000);
        assert_eq!(high_mask::<u8>(8), 0b11111111);
    }

    #[test]
    fn test_set_clear_toggle_bits() {
        let val: u8 = 0;
        assert_eq!(set_bits(val, &[0, 2, 4]), 0b00010101);
        assert_eq!(clear_bits(0b11111111u8, &[0, 2, 4]), 0b11101010);
        // toggle bits 0, 2, 4 on 0b00001010 (bits 1 and 3 are set)
        // toggle bit 0: 0->1, toggle bit 2: 0->1, toggle bit 4: 0->1
        // result: 0b00011111 = 31
        assert_eq!(toggle_bits(0b00001010u8, &[0, 2, 4]), 0b00011111);
    }

    #[test]
    fn test_trailing_leading() {
        assert_eq!(0b00110000u8.trailing_zeros(), 4);
        assert_eq!(0b00110000u8.leading_zeros(), 2);
        assert_eq!(0b00001111u8.trailing_ones(), 4);
        assert_eq!(0b11110000u8.leading_ones(), 4);
    }

    #[test]
    fn test_u32_operations() {
        let val: u32 = 0x12345678;
        assert_eq!(val.count_ones(), 13);
        assert_eq!(val.first_set_bit(), Some(3));
        assert_eq!(val.last_set_bit(), Some(28));
        assert!(val.is_bit_set(3));
        assert!(!val.is_bit_set(0));
    }

    #[test]
    fn test_u64_operations() {
        let val: u64 = 0x123456789ABCDEF0;
        assert_eq!(val.count_ones(), 32);
        assert_eq!(val.first_set_bit(), Some(4));
        assert_eq!(val.last_set_bit(), Some(60));
    }

    #[test]
    fn test_u128_operations() {
        let val: u128 = u128::MAX;
        assert_eq!(val.count_ones(), 128);
        assert_eq!(val.count_zeros(), 0);
        assert_eq!(val.first_set_bit(), Some(0));
        assert_eq!(val.last_set_bit(), Some(127));
    }
}