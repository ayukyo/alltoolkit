//! Volume unit conversions
//!
//! Provides conversions between various volume units including metric and imperial systems.

use crate::round_to;

/// Represents a volume value with conversion methods
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Volume {
    /// The volume in liters (base unit)
    liters: f64,
}

impl Volume {
    // Constructors from various units
    
    /// Creates a Volume from liters
    pub fn from_liters(l: f64) -> Self {
        Self { liters: l }
    }
    
    /// Creates a Volume from milliliters
    pub fn from_milliliters(ml: f64) -> Self {
        Self { liters: ml / 1000.0 }
    }
    
    /// Creates a Volume from cubic centimeters (same as milliliters)
    pub fn from_cubic_centimeters(cm3: f64) -> Self {
        Self { liters: cm3 / 1000.0 }
    }
    
    /// Creates a Volume from cubic meters
    pub fn from_cubic_meters(m3: f64) -> Self {
        Self { liters: m3 * 1000.0 }
    }
    
    /// Creates a Volume from cubic decimeters (same as liters)
    pub fn from_cubic_decimeters(dm3: f64) -> Self {
        Self { liters: dm3 }
    }
    
    /// Creates a Volume from cubic millimeters
    pub fn from_cubic_millimeters(mm3: f64) -> Self {
        Self { liters: mm3 / 1_000_000.0 }
    }
    
    /// Creates a Volume from cubic kilometers
    pub fn from_cubic_kilometers(km3: f64) -> Self {
        Self { liters: km3 * 1_000_000_000_000.0 }
    }
    
    /// Creates a Volume from US gallons
    pub fn from_us_gallons(gal: f64) -> Self {
        Self { liters: gal * 3.785411784 }
    }
    
    /// Creates a Volume from UK/imperial gallons
    pub fn from_imperial_gallons(gal: f64) -> Self {
        Self { liters: gal * 4.54609 }
    }
    
    /// Creates a Volume from US quarts
    pub fn from_us_quarts(qt: f64) -> Self {
        Self { liters: qt * 0.946352946 }
    }
    
    /// Creates a Volume from US pints
    pub fn from_us_pints(pt: f64) -> Self {
        Self { liters: pt * 0.473176473 }
    }
    
    /// Creates a Volume from US cups
    pub fn from_us_cups(cup: f64) -> Self {
        Self { liters: cup * 0.2365882365 }
    }
    
    /// Creates a Volume from US fluid ounces
    pub fn from_us_fluid_ounces(floz: f64) -> Self {
        Self { liters: floz * 0.0295735295625 }
    }
    
    /// Creates a Volume from US tablespoons
    pub fn from_us_tablespoons(tbsp: f64) -> Self {
        Self { liters: tbsp * 0.01478676478125 }
    }
    
    /// Creates a Volume from US teaspoons
    pub fn from_us_teaspoons(tsp: f64) -> Self {
        Self { liters: tsp * 0.00492892159375 }
    }
    
    /// Creates a Volume from cubic feet
    pub fn from_cubic_feet(ft3: f64) -> Self {
        Self { liters: ft3 * 28.316846592 }
    }
    
    /// Creates a Volume from cubic inches
    pub fn from_cubic_inches(in3: f64) -> Self {
        Self { liters: in3 * 0.016387064 }
    }
    
    /// Creates a Volume from cubic yards
    pub fn from_cubic_yards(yd3: f64) -> Self {
        Self { liters: yd3 * 764.554857984 }
    }
    
    /// Creates a Volume from barrels (oil)
    pub fn from_barrels_oil(bbl: f64) -> Self {
        Self { liters: bbl * 158.987294928 }
    }
    
    // Conversion methods to various units
    
    /// Converts to liters
    pub fn to_liters(&self) -> f64 {
        self.liters
    }
    
    /// Converts to milliliters
    pub fn to_milliliters(&self) -> f64 {
        self.liters * 1000.0
    }
    
    /// Converts to cubic centimeters
    pub fn to_cubic_centimeters(&self) -> f64 {
        self.liters * 1000.0
    }
    
    /// Converts to cubic meters
    pub fn to_cubic_meters(&self) -> f64 {
        self.liters / 1000.0
    }
    
    /// Converts to cubic decimeters
    pub fn to_cubic_decimeters(&self) -> f64 {
        self.liters
    }
    
    /// Converts to cubic millimeters
    pub fn to_cubic_millimeters(&self) -> f64 {
        self.liters * 1_000_000.0
    }
    
    /// Converts to cubic kilometers
    pub fn to_cubic_kilometers(&self) -> f64 {
        self.liters / 1_000_000_000_000.0
    }
    
    /// Converts to US gallons
    pub fn to_us_gallons(&self) -> f64 {
        self.liters / 3.785411784
    }
    
    /// Converts to UK/imperial gallons
    pub fn to_imperial_gallons(&self) -> f64 {
        self.liters / 4.54609
    }
    
    /// Converts to US quarts
    pub fn to_us_quarts(&self) -> f64 {
        self.liters / 0.946352946
    }
    
    /// Converts to US pints
    pub fn to_us_pints(&self) -> f64 {
        self.liters / 0.473176473
    }
    
    /// Converts to US cups
    pub fn to_us_cups(&self) -> f64 {
        self.liters / 0.2365882365
    }
    
    /// Converts to US fluid ounces
    pub fn to_us_fluid_ounces(&self) -> f64 {
        self.liters / 0.0295735295625
    }
    
    /// Converts to US tablespoons
    pub fn to_us_tablespoons(&self) -> f64 {
        self.liters / 0.01478676478125
    }
    
    /// Converts to US teaspoons
    pub fn to_us_teaspoons(&self) -> f64 {
        self.liters / 0.00492892159375
    }
    
    /// Converts to cubic feet
    pub fn to_cubic_feet(&self) -> f64 {
        self.liters / 28.316846592
    }
    
    /// Converts to cubic inches
    pub fn to_cubic_inches(&self) -> f64 {
        self.liters / 0.016387064
    }
    
    /// Converts to cubic yards
    pub fn to_cubic_yards(&self) -> f64 {
        self.liters / 764.554857984
    }
    
    /// Converts to barrels (oil)
    pub fn to_barrels_oil(&self) -> f64 {
        self.liters / 158.987294928
    }
    
    /// Returns the value rounded to the specified decimal places
    pub fn rounded(&self, decimals: u32) -> Self {
        Self {
            liters: round_to(self.liters, decimals),
        }
    }
}

impl Default for Volume {
    fn default() -> Self {
        Self { liters: 0.0 }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_liters_to_milliliters() {
        let volume = Volume::from_liters(1.0);
        assert!((volume.to_milliliters() - 1000.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_us_gallons_to_liters() {
        let volume = Volume::from_us_gallons(1.0);
        assert!((volume.to_liters() - 3.785411784).abs() < 0.0001);
    }
    
    #[test]
    fn test_imperial_gallons_to_liters() {
        let volume = Volume::from_imperial_gallons(1.0);
        assert!((volume.to_liters() - 4.54609).abs() < 0.0001);
    }
    
    #[test]
    fn test_cubic_meters_to_liters() {
        let volume = Volume::from_cubic_meters(1.0);
        assert!((volume.to_liters() - 1000.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_cubic_feet_to_liters() {
        let volume = Volume::from_cubic_feet(1.0);
        assert!((volume.to_liters() - 28.316846592).abs() < 0.0001);
    }
    
    #[test]
    fn test_barrels_oil_to_liters() {
        let volume = Volume::from_barrels_oil(1.0);
        assert!((volume.to_liters() - 158.987294928).abs() < 0.0001);
    }
    
    #[test]
    fn test_round_trip() {
        let original = 5.5;
        let volume = Volume::from_us_gallons(original);
        assert!((volume.to_us_gallons() - original).abs() < 0.0001);
    }
}