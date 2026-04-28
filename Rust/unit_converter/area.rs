//! Area unit conversions
//!
//! Provides conversions between various area units including metric and imperial systems.

use crate::round_to;

/// Represents an area value with conversion methods
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Area {
    /// The area in square meters (base unit)
    square_meters: f64,
}

impl Area {
    // Constructors from various units
    
    /// Creates an Area from square meters
    pub fn from_square_meters(m2: f64) -> Self {
        Self { square_meters: m2 }
    }
    
    /// Creates an Area from square kilometers
    pub fn from_square_kilometers(km2: f64) -> Self {
        Self { square_meters: km2 * 1_000_000.0 }
    }
    
    /// Creates an Area from square centimeters
    pub fn from_square_centimeters(cm2: f64) -> Self {
        Self { square_meters: cm2 / 10_000.0 }
    }
    
    /// Creates an Area from square millimeters
    pub fn from_square_millimeters(mm2: f64) -> Self {
        Self { square_meters: mm2 / 1_000_000.0 }
    }
    
    /// Creates an Area from hectares
    pub fn from_hectares(ha: f64) -> Self {
        Self { square_meters: ha * 10_000.0 }
    }
    
    /// Creates an Area from acres
    pub fn from_acres(ac: f64) -> Self {
        Self { square_meters: ac * 4046.8564224 }
    }
    
    /// Creates an Area from square feet
    pub fn from_square_feet(ft2: f64) -> Self {
        Self { square_meters: ft2 * 0.09290304 }
    }
    
    /// Creates an Area from square yards
    pub fn from_square_yards(yd2: f64) -> Self {
        Self { square_meters: yd2 * 0.83612736 }
    }
    
    /// Creates an Area from square inches
    pub fn from_square_inches(in2: f64) -> Self {
        Self { square_meters: in2 * 0.00064516 }
    }
    
    /// Creates an Area from square miles
    pub fn from_square_miles(mi2: f64) -> Self {
        Self { square_meters: mi2 * 2_589_988.110336 }
    }
    
    /// Creates an Area from ares
    pub fn from_ares(a: f64) -> Self {
        Self { square_meters: a * 100.0 }
    }
    
    /// Creates an Area from barns (nuclear physics unit)
    pub fn from_barns(b: f64) -> Self {
        Self { square_meters: b * 1e-28 }
    }
    
    // Conversion methods to various units
    
    /// Converts to square meters
    pub fn to_square_meters(&self) -> f64 {
        self.square_meters
    }
    
    /// Converts to square kilometers
    pub fn to_square_kilometers(&self) -> f64 {
        self.square_meters / 1_000_000.0
    }
    
    /// Converts to square centimeters
    pub fn to_square_centimeters(&self) -> f64 {
        self.square_meters * 10_000.0
    }
    
    /// Converts to square millimeters
    pub fn to_square_millimeters(&self) -> f64 {
        self.square_meters * 1_000_000.0
    }
    
    /// Converts to hectares
    pub fn to_hectares(&self) -> f64 {
        self.square_meters / 10_000.0
    }
    
    /// Converts to acres
    pub fn to_acres(&self) -> f64 {
        self.square_meters / 4046.8564224
    }
    
    /// Converts to square feet
    pub fn to_square_feet(&self) -> f64 {
        self.square_meters / 0.09290304
    }
    
    /// Converts to square yards
    pub fn to_square_yards(&self) -> f64 {
        self.square_meters / 0.83612736
    }
    
    /// Converts to square inches
    pub fn to_square_inches(&self) -> f64 {
        self.square_meters / 0.00064516
    }
    
    /// Converts to square miles
    pub fn to_square_miles(&self) -> f64 {
        self.square_meters / 2_589_988.110336
    }
    
    /// Converts to ares
    pub fn to_ares(&self) -> f64 {
        self.square_meters / 100.0
    }
    
    /// Converts to barns
    pub fn to_barns(&self) -> f64 {
        self.square_meters / 1e-28
    }
    
    /// Returns the value rounded to the specified decimal places
    pub fn rounded(&self, decimals: u32) -> Self {
        Self {
            square_meters: round_to(self.square_meters, decimals),
        }
    }
}

impl Default for Area {
    fn default() -> Self {
        Self { square_meters: 0.0 }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_square_meters_to_square_kilometers() {
        let area = Area::from_square_meters(1_000_000.0);
        assert!((area.to_square_kilometers() - 1.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_hectares_to_square_meters() {
        let area = Area::from_hectares(1.0);
        assert!((area.to_square_meters() - 10_000.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_acres_to_hectares() {
        let area = Area::from_acres(1.0);
        assert!((area.to_hectares() - 0.404686).abs() < 0.001);
    }
    
    #[test]
    fn test_square_feet_to_square_meters() {
        let area = Area::from_square_feet(1.0);
        assert!((area.to_square_meters() - 0.09290304).abs() < 0.0001);
    }
    
    #[test]
    fn test_square_yards_to_square_feet() {
        let area = Area::from_square_yards(1.0);
        assert!((area.to_square_feet() - 9.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_round_trip() {
        let original = 123.456;
        let area = Area::from_acres(original);
        assert!((area.to_acres() - original).abs() < 0.001);
    }
}