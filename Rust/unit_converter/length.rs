//! Length unit conversions
//!
//! Provides conversions between various length units including metric and imperial systems.

use crate::round_to;

/// Represents a length value with conversion methods
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Length {
    /// The length in meters (base unit)
    meters: f64,
}

impl Length {
    // Constructors from various units
    
    /// Creates a Length from meters
    pub fn from_meters(m: f64) -> Self {
        Self { meters: m }
    }
    
    /// Creates a Length from kilometers
    pub fn from_kilometers(km: f64) -> Self {
        Self { meters: km * 1000.0 }
    }
    
    /// Creates a Length from centimeters
    pub fn from_centimeters(cm: f64) -> Self {
        Self { meters: cm / 100.0 }
    }
    
    /// Creates a Length from millimeters
    pub fn from_millimeters(mm: f64) -> Self {
        Self { meters: mm / 1000.0 }
    }
    
    /// Creates a Length from micrometers
    pub fn from_micrometers(um: f64) -> Self {
        Self { meters: um / 1_000_000.0 }
    }
    
    /// Creates a Length from nanometers
    pub fn from_nanometers(nm: f64) -> Self {
        Self { meters: nm / 1_000_000_000.0 }
    }
    
    /// Creates a Length from miles
    pub fn from_miles(mi: f64) -> Self {
        Self { meters: mi * 1609.344 }
    }
    
    /// Creates a Length from yards
    pub fn from_yards(yd: f64) -> Self {
        Self { meters: yd * 0.9144 }
    }
    
    /// Creates a Length from feet
    pub fn from_feet(ft: f64) -> Self {
        Self { meters: ft * 0.3048 }
    }
    
    /// Creates a Length from inches
    pub fn from_inches(inch: f64) -> Self {
        Self { meters: inch * 0.0254 }
    }
    
    /// Creates a Length from nautical miles
    pub fn from_nautical_miles(nmi: f64) -> Self {
        Self { meters: nmi * 1852.0 }
    }
    
    /// Creates a Length from light years
    pub fn from_light_years(ly: f64) -> Self {
        Self { meters: ly * 9_460_730_472_580_800.0 }
    }
    
    /// Creates a Length from astronomical units
    pub fn from_astronomical_units(au: f64) -> Self {
        Self { meters: au * 149_597_870_700.0 }
    }
    
    // Conversion methods to various units
    
    /// Converts to meters
    pub fn to_meters(&self) -> f64 {
        self.meters
    }
    
    /// Converts to kilometers
    pub fn to_kilometers(&self) -> f64 {
        self.meters / 1000.0
    }
    
    /// Converts to centimeters
    pub fn to_centimeters(&self) -> f64 {
        self.meters * 100.0
    }
    
    /// Converts to millimeters
    pub fn to_millimeters(&self) -> f64 {
        self.meters * 1000.0
    }
    
    /// Converts to micrometers
    pub fn to_micrometers(&self) -> f64 {
        self.meters * 1_000_000.0
    }
    
    /// Converts to nanometers
    pub fn to_nanometers(&self) -> f64 {
        self.meters * 1_000_000_000.0
    }
    
    /// Converts to miles
    pub fn to_miles(&self) -> f64 {
        self.meters / 1609.344
    }
    
    /// Converts to yards
    pub fn to_yards(&self) -> f64 {
        self.meters / 0.9144
    }
    
    /// Converts to feet
    pub fn to_feet(&self) -> f64 {
        self.meters / 0.3048
    }
    
    /// Converts to inches
    pub fn to_inches(&self) -> f64 {
        self.meters / 0.0254
    }
    
    /// Converts to nautical miles
    pub fn to_nautical_miles(&self) -> f64 {
        self.meters / 1852.0
    }
    
    /// Converts to light years
    pub fn to_light_years(&self) -> f64 {
        self.meters / 9_460_730_472_580_800.0
    }
    
    /// Converts to astronomical units
    pub fn to_astronomical_units(&self) -> f64 {
        self.meters / 149_597_870_700.0
    }
    
    /// Returns the value rounded to the specified decimal places
    pub fn rounded(&self, decimals: u32) -> Self {
        Self {
            meters: round_to(self.meters, decimals),
        }
    }
}

impl Default for Length {
    fn default() -> Self {
        Self { meters: 0.0 }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_meters_to_kilometers() {
        let length = Length::from_meters(1000.0);
        assert!((length.to_kilometers() - 1.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_miles_to_meters() {
        let length = Length::from_miles(1.0);
        assert!((length.to_meters() - 1609.344).abs() < 0.001);
    }
    
    #[test]
    fn test_feet_to_meters() {
        let length = Length::from_feet(1.0);
        assert!((length.to_meters() - 0.3048).abs() < 0.0001);
    }
    
    #[test]
    fn test_inches_to_centimeters() {
        let length = Length::from_inches(1.0);
        assert!((length.to_centimeters() - 2.54).abs() < 0.0001);
    }
    
    #[test]
    fn test_nautical_miles() {
        let length = Length::from_nautical_miles(1.0);
        assert!((length.to_meters() - 1852.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_round_trip() {
        let original = 123.456;
        let length = Length::from_feet(original);
        assert!((length.to_feet() - original).abs() < 0.0001);
    }
}