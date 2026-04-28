//! Weight/Mass unit conversions
//!
//! Provides conversions between various mass/weight units including metric and imperial systems.

use crate::round_to;

/// Represents a weight/mass value with conversion methods
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Weight {
    /// The weight in kilograms (base unit)
    kilograms: f64,
}

impl Weight {
    // Constructors from various units
    
    /// Creates a Weight from kilograms
    pub fn from_kilograms(kg: f64) -> Self {
        Self { kilograms: kg }
    }
    
    /// Creates a Weight from grams
    pub fn from_grams(g: f64) -> Self {
        Self { kilograms: g / 1000.0 }
    }
    
    /// Creates a Weight from milligrams
    pub fn from_milligrams(mg: f64) -> Self {
        Self { kilograms: mg / 1_000_000.0 }
    }
    
    /// Creates a Weight from micrograms
    pub fn from_micrograms(ug: f64) -> Self {
        Self { kilograms: ug / 1_000_000_000.0 }
    }
    
    /// Creates a Weight from metric tons
    pub fn from_metric_tonnes(t: f64) -> Self {
        Self { kilograms: t * 1000.0 }
    }
    
    /// Creates a Weight from pounds (avoirdupois)
    pub fn from_pounds(lb: f64) -> Self {
        Self { kilograms: lb * 0.45359237 }
    }
    
    /// Creates a Weight from ounces (avoirdupois)
    pub fn from_ounces(oz: f64) -> Self {
        Self { kilograms: oz * 0.028349523125 }
    }
    
    /// Creates a Weight from stones
    pub fn from_stones(st: f64) -> Self {
        Self { kilograms: st * 6.35029318 }
    }
    
    /// Creates a Weight from short tons (US)
    pub fn from_short_tons(t: f64) -> Self {
        Self { kilograms: t * 907.18474 }
    }
    
    /// Creates a Weight from long tons (UK)
    pub fn from_long_tons(t: f64) -> Self {
        Self { kilograms: t * 1016.0469088 }
    }
    
    /// Creates a Weight from carats (metric)
    pub fn from_carats(ct: f64) -> Self {
        Self { kilograms: ct * 0.0002 }
    }
    
    // Conversion methods to various units
    
    /// Converts to kilograms
    pub fn to_kilograms(&self) -> f64 {
        self.kilograms
    }
    
    /// Converts to grams
    pub fn to_grams(&self) -> f64 {
        self.kilograms * 1000.0
    }
    
    /// Converts to milligrams
    pub fn to_milligrams(&self) -> f64 {
        self.kilograms * 1_000_000.0
    }
    
    /// Converts to micrograms
    pub fn to_micrograms(&self) -> f64 {
        self.kilograms * 1_000_000_000.0
    }
    
    /// Converts to metric tonnes
    pub fn to_metric_tonnes(&self) -> f64 {
        self.kilograms / 1000.0
    }
    
    /// Converts to pounds
    pub fn to_pounds(&self) -> f64 {
        self.kilograms / 0.45359237
    }
    
    /// Converts to ounces
    pub fn to_ounces(&self) -> f64 {
        self.kilograms / 0.028349523125
    }
    
    /// Converts to stones
    pub fn to_stones(&self) -> f64 {
        self.kilograms / 6.35029318
    }
    
    /// Converts to short tons (US)
    pub fn to_short_tons(&self) -> f64 {
        self.kilograms / 907.18474
    }
    
    /// Converts to long tons (UK)
    pub fn to_long_tons(&self) -> f64 {
        self.kilograms / 1016.0469088
    }
    
    /// Converts to carats
    pub fn to_carats(&self) -> f64 {
        self.kilograms / 0.0002
    }
    
    /// Returns the value rounded to the specified decimal places
    pub fn rounded(&self, decimals: u32) -> Self {
        Self {
            kilograms: round_to(self.kilograms, decimals),
        }
    }
}

impl Default for Weight {
    fn default() -> Self {
        Self { kilograms: 0.0 }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kilograms_to_grams() {
        let weight = Weight::from_kilograms(1.0);
        assert!((weight.to_grams() - 1000.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_pounds_to_kilograms() {
        let weight = Weight::from_pounds(1.0);
        assert!((weight.to_kilograms() - 0.45359237).abs() < 0.0001);
    }
    
    #[test]
    fn test_ounces_to_grams() {
        let weight = Weight::from_ounces(1.0);
        assert!((weight.to_grams() - 28.349523125).abs() < 0.0001);
    }
    
    #[test]
    fn test_stones_to_kilograms() {
        let weight = Weight::from_stones(1.0);
        assert!((weight.to_kilograms() - 6.35029318).abs() < 0.0001);
    }
    
    #[test]
    fn test_carats_to_grams() {
        let weight = Weight::from_carats(5.0); // 1 carat = 0.2g
        assert!((weight.to_grams() - 1.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_metric_tonnes() {
        let weight = Weight::from_metric_tonnes(1.0);
        assert!((weight.to_kilograms() - 1000.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_round_trip() {
        let original = 150.5;
        let weight = Weight::from_pounds(original);
        assert!((weight.to_pounds() - original).abs() < 0.0001);
    }
}