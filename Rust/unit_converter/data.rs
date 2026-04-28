//! Data size unit conversions
//!
//! Provides conversions between various digital data size units.
//! Supports both binary (1024-based) and decimal (1000-based) prefixes.

use crate::round_to;

/// Represents a data size value with conversion methods
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Data {
    /// The data size in bytes (base unit)
    bytes: f64,
}

impl Data {
    // Constructors from various units (binary, 1024-based)
    
    /// Creates a Data from bytes
    pub fn from_bytes(b: f64) -> Self {
        Self { bytes: b }
    }
    
    /// Creates a Data from kibibytes (KiB, 1024 bytes)
    pub fn from_kibibytes(kib: f64) -> Self {
        Self { bytes: kib * 1024.0 }
    }
    
    /// Creates a Data from mebibytes (MiB, 1024² bytes)
    pub fn from_mebibytes(mib: f64) -> Self {
        Self { bytes: mib * 1_048_576.0 }
    }
    
    /// Creates a Data from gibibytes (GiB, 1024³ bytes)
    pub fn from_gibibytes(gib: f64) -> Self {
        Self { bytes: gib * 1_073_741_824.0 }
    }
    
    /// Creates a Data from tebibytes (TiB, 1024⁴ bytes)
    pub fn from_tebibytes(tib: f64) -> Self {
        Self { bytes: tib * 1_099_511_627_776.0 }
    }
    
    /// Creates a Data from pebibytes (PiB, 1024⁵ bytes)
    pub fn from_pebibytes(pib: f64) -> Self {
        Self { bytes: pib * 1_125_899_906_842_624.0 }
    }
    
    /// Creates a Data from exbibytes (EiB, 1024⁶ bytes)
    pub fn from_exbibytes(eib: f64) -> Self {
        Self { bytes: eib * 1_152_921_504_606_846_976.0 }
    }
    
    // Constructors from various units (decimal, 1000-based)
    
    /// Creates a Data from kilobytes (KB, 1000 bytes)
    pub fn from_kilobytes(kb: f64) -> Self {
        Self { bytes: kb * 1000.0 }
    }
    
    /// Creates a Data from megabytes (MB, 1000² bytes)
    pub fn from_megabytes(mb: f64) -> Self {
        Self { bytes: mb * 1_000_000.0 }
    }
    
    /// Creates a Data from gigabytes (GB, 1000³ bytes)
    pub fn from_gigabytes(gb: f64) -> Self {
        Self { bytes: gb * 1_000_000_000.0 }
    }
    
    /// Creates a Data from terabytes (TB, 1000⁴ bytes)
    pub fn from_terabytes(tb: f64) -> Self {
        Self { bytes: tb * 1_000_000_000_000.0 }
    }
    
    /// Creates a Data from petabytes (PB, 1000⁵ bytes)
    pub fn from_petabytes(pb: f64) -> Self {
        Self { bytes: pb * 1_000_000_000_000_000.0 }
    }
    
    /// Creates a Data from exabytes (EB, 1000⁶ bytes)
    pub fn from_exabytes(eb: f64) -> Self {
        Self { bytes: eb * 1_000_000_000_000_000_000.0 }
    }
    
    // Bit-based constructors
    
    /// Creates a Data from bits
    pub fn from_bits(bits: f64) -> Self {
        Self { bytes: bits / 8.0 }
    }
    
    /// Creates a Data from kilobits (Kb, 1000 bits)
    pub fn from_kilobits(kb: f64) -> Self {
        Self { bytes: kb * 125.0 }
    }
    
    /// Creates a Data from megabits (Mb, 10⁶ bits)
    pub fn from_megabits(mb: f64) -> Self {
        Self { bytes: mb * 125_000.0 }
    }
    
    /// Creates a Data from gigabits (Gb, 10⁹ bits)
    pub fn from_gigabits(gb: f64) -> Self {
        Self { bytes: gb * 125_000_000.0 }
    }
    
    // Conversion methods to various units (binary, 1024-based)
    
    /// Converts to bytes
    pub fn to_bytes(&self) -> f64 {
        self.bytes
    }
    
    /// Converts to kibibytes (KiB)
    pub fn to_kibibytes(&self) -> f64 {
        self.bytes / 1024.0
    }
    
    /// Converts to mebibytes (MiB)
    pub fn to_mebibytes(&self) -> f64 {
        self.bytes / 1_048_576.0
    }
    
    /// Converts to gibibytes (GiB)
    pub fn to_gibibytes(&self) -> f64 {
        self.bytes / 1_073_741_824.0
    }
    
    /// Converts to tebibytes (TiB)
    pub fn to_tebibytes(&self) -> f64 {
        self.bytes / 1_099_511_627_776.0
    }
    
    /// Converts to pebibytes (PiB)
    pub fn to_pebibytes(&self) -> f64 {
        self.bytes / 1_125_899_906_842_624.0
    }
    
    /// Converts to exbibytes (EiB)
    pub fn to_exbibytes(&self) -> f64 {
        self.bytes / 1_152_921_504_606_846_976.0
    }
    
    // Conversion methods to various units (decimal, 1000-based)
    
    /// Converts to kilobytes (KB)
    pub fn to_kilobytes(&self) -> f64 {
        self.bytes / 1000.0
    }
    
    /// Converts to megabytes (MB)
    pub fn to_megabytes(&self) -> f64 {
        self.bytes / 1_000_000.0
    }
    
    /// Converts to gigabytes (GB)
    pub fn to_gigabytes(&self) -> f64 {
        self.bytes / 1_000_000_000.0
    }
    
    /// Converts to terabytes (TB)
    pub fn to_terabytes(&self) -> f64 {
        self.bytes / 1_000_000_000_000.0
    }
    
    /// Converts to petabytes (PB)
    pub fn to_petabytes(&self) -> f64 {
        self.bytes / 1_000_000_000_000_000.0
    }
    
    /// Converts to exabytes (EB)
    pub fn to_exabytes(&self) -> f64 {
        self.bytes / 1_000_000_000_000_000_000.0
    }
    
    // Bit-based conversions
    
    /// Converts to bits
    pub fn to_bits(&self) -> f64 {
        self.bytes * 8.0
    }
    
    /// Converts to kilobits (Kb)
    pub fn to_kilobits(&self) -> f64 {
        self.bytes / 125.0
    }
    
    /// Converts to megabits (Mb)
    pub fn to_megabits(&self) -> f64 {
        self.bytes / 125_000.0
    }
    
    /// Converts to gigabits (Gb)
    pub fn to_gigabits(&self) -> f64 {
        self.bytes / 125_000_000.0
    }
    
    /// Returns the value rounded to the specified decimal places
    pub fn rounded(&self, decimals: u32) -> Self {
        Self {
            bytes: round_to(self.bytes, decimals),
        }
    }
    
    /// Formats the data size as a human-readable string (binary units)
    pub fn format_human_binary(&self) -> String {
        if self.bytes < 1024.0 {
            format!("{:.0} B", self.bytes)
        } else if self.bytes < 1_048_576.0 {
            format!("{:.2} KiB", self.to_kibibytes())
        } else if self.bytes < 1_073_741_824.0 {
            format!("{:.2} MiB", self.to_mebibytes())
        } else if self.bytes < 1_099_511_627_776.0 {
            format!("{:.2} GiB", self.to_gibibytes())
        } else if self.bytes < 1_125_899_906_842_624.0 {
            format!("{:.2} TiB", self.to_tebibytes())
        } else if self.bytes < 1_152_921_504_606_846_976.0 {
            format!("{:.2} PiB", self.to_pebibytes())
        } else {
            format!("{:.2} EiB", self.to_exbibytes())
        }
    }
    
    /// Formats the data size as a human-readable string (decimal units)
    pub fn format_human_decimal(&self) -> String {
        if self.bytes < 1000.0 {
            format!("{:.0} B", self.bytes)
        } else if self.bytes < 1_000_000.0 {
            format!("{:.2} KB", self.to_kilobytes())
        } else if self.bytes < 1_000_000_000.0 {
            format!("{:.2} MB", self.to_megabytes())
        } else if self.bytes < 1_000_000_000_000.0 {
            format!("{:.2} GB", self.to_gigabytes())
        } else if self.bytes < 1_000_000_000_000_000.0 {
            format!("{:.2} TB", self.to_terabytes())
        } else if self.bytes < 1_000_000_000_000_000_000.0 {
            format!("{:.2} PB", self.to_petabytes())
        } else {
            format!("{:.2} EB", self.to_exabytes())
        }
    }
}

impl Default for Data {
    fn default() -> Self {
        Self { bytes: 0.0 }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bytes_to_kibibytes() {
        let data = Data::from_bytes(1024.0);
        assert!((data.to_kibibytes() - 1.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_kilobytes_vs_kibibytes() {
        let kb = Data::from_kilobytes(1.0);
        let kib = Data::from_kibibytes(1.0);
        
        // 1 KB = 1000 bytes, 1 KiB = 1024 bytes
        assert!((kb.to_bytes() - 1000.0).abs() < 0.0001);
        assert!((kib.to_bytes() - 1024.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_gigabytes_to_megabytes() {
        let data = Data::from_gigabytes(1.0);
        assert!((data.to_megabytes() - 1000.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_gibibytes_to_mebibytes() {
        let data = Data::from_gibibytes(1.0);
        assert!((data.to_mebibytes() - 1024.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_bits_to_bytes() {
        let data = Data::from_bits(8.0);
        assert!((data.to_bytes() - 1.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_megabits_to_megabytes() {
        // 1 Mb = 1,000,000 bits = 125,000 bytes
        let data = Data::from_megabits(8.0);
        // 8 Mb = 1,000,000 bytes = 1 MB
        assert!((data.to_megabytes() - 1.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_round_trip() {
        let original = 5.5;
        let data = Data::from_gibibytes(original);
        assert!((data.to_gibibytes() - original).abs() < 0.0001);
    }
    
    #[test]
    fn test_format_human_binary() {
        assert_eq!(Data::from_bytes(512.0).format_human_binary(), "512 B");
        assert_eq!(Data::from_kibibytes(1.0).format_human_binary(), "1.00 KiB");
        assert_eq!(Data::from_mebibytes(1.5).format_human_binary(), "1.50 MiB");
    }
    
    #[test]
    fn test_format_human_decimal() {
        assert_eq!(Data::from_bytes(500.0).format_human_decimal(), "500 B");
        assert_eq!(Data::from_kilobytes(1.0).format_human_decimal(), "1.00 KB");
        assert_eq!(Data::from_megabytes(1.5).format_human_decimal(), "1.50 MB");
    }
}