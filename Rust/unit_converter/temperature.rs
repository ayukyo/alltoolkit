//! Temperature unit conversions
//!
//! Provides conversions between Celsius, Fahrenheit, and Kelvin temperature scales.

use crate::round_to;

/// Represents a temperature value with conversion methods
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Temperature {
    /// The temperature in Kelvin (base unit)
    kelvin: f64,
}

impl Temperature {
    // Constructors from various temperature scales
    
    /// Creates a Temperature from Celsius
    pub fn from_celsius(c: f64) -> Self {
        Self { kelvin: c + 273.15 }
    }
    
    /// Creates a Temperature from Fahrenheit
    pub fn from_fahrenheit(f: f64) -> Self {
        Self {
            kelvin: (f - 32.0) * 5.0 / 9.0 + 273.15,
        }
    }
    
    /// Creates a Temperature from Kelvin
    pub fn from_kelvin(k: f64) -> Self {
        Self { kelvin: k }
    }
    
    /// Creates a Temperature from Rankine
    pub fn from_rankine(r: f64) -> Self {
        Self { kelvin: r * 5.0 / 9.0 }
    }
    
    /// Creates a Temperature from Delisle
    pub fn from_delisle(d: f64) -> Self {
        Self { kelvin: 373.15 - d * 2.0 / 3.0 }
    }
    
    /// Creates a Temperature from Newton
    pub fn from_newton(n: f64) -> Self {
        Self { kelvin: n * 100.0 / 33.0 + 273.15 }
    }
    
    /// Creates a Temperature from Réaumur
    pub fn from_reaumur(r: f64) -> Self {
        Self { kelvin: r * 5.0 / 4.0 + 273.15 }
    }
    
    /// Creates a Temperature from Rømer
    pub fn from_romer(r: f64) -> Self {
        Self {
            kelvin: (r - 7.5) * 40.0 / 21.0 + 273.15,
        }
    }
    
    // Conversion methods to various temperature scales
    
    /// Converts to Celsius
    pub fn to_celsius(&self) -> f64 {
        self.kelvin - 273.15
    }
    
    /// Converts to Fahrenheit
    pub fn to_fahrenheit(&self) -> f64 {
        (self.kelvin - 273.15) * 9.0 / 5.0 + 32.0
    }
    
    /// Converts to Kelvin
    pub fn to_kelvin(&self) -> f64 {
        self.kelvin
    }
    
    /// Converts to Rankine
    pub fn to_rankine(&self) -> f64 {
        self.kelvin * 9.0 / 5.0
    }
    
    /// Converts to Delisle
    pub fn to_delisle(&self) -> f64 {
        (373.15 - self.kelvin) * 3.0 / 2.0
    }
    
    /// Converts to Newton
    pub fn to_newton(&self) -> f64 {
        (self.kelvin - 273.15) * 33.0 / 100.0
    }
    
    /// Converts to Réaumur
    pub fn to_reaumur(&self) -> f64 {
        (self.kelvin - 273.15) * 4.0 / 5.0
    }
    
    /// Converts to Rømer
    pub fn to_romer(&self) -> f64 {
        (self.kelvin - 273.15) * 21.0 / 40.0 + 7.5
    }
    
    /// Returns the value rounded to the specified decimal places
    pub fn rounded(&self, decimals: u32) -> Self {
        Self {
            kelvin: round_to(self.kelvin, decimals),
        }
    }
    
    /// Checks if the temperature is below absolute zero
    pub fn is_valid(&self) -> bool {
        self.kelvin >= 0.0
    }
}

impl Default for Temperature {
    fn default() -> Self {
        Self { kelvin: 273.15 } // 0°C
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_celsius_to_fahrenheit() {
        let temp = Temperature::from_celsius(0.0);
        assert!((temp.to_fahrenheit() - 32.0).abs() < 0.001);
        
        let temp = Temperature::from_celsius(100.0);
        assert!((temp.to_fahrenheit() - 212.0).abs() < 0.001);
    }
    
    #[test]
    fn test_fahrenheit_to_celsius() {
        let temp = Temperature::from_fahrenheit(32.0);
        assert!((temp.to_celsius() - 0.0).abs() < 0.001);
        
        let temp = Temperature::from_fahrenheit(212.0);
        assert!((temp.to_celsius() - 100.0).abs() < 0.001);
    }
    
    #[test]
    fn test_kelvin_conversions() {
        let temp = Temperature::from_kelvin(0.0);
        assert!((temp.to_celsius() - (-273.15)).abs() < 0.001);
        
        let temp = Temperature::from_celsius(0.0);
        assert!((temp.to_kelvin() - 273.15).abs() < 0.001);
    }
    
    #[test]
    fn test_round_trip() {
        let original = 25.5;
        let temp = Temperature::from_celsius(original);
        assert!((temp.to_celsius() - original).abs() < 0.001);
    }
    
    #[test]
    fn test_body_temperature() {
        // Normal human body temperature: 98.6°F = 37°C
        let temp = Temperature::from_fahrenheit(98.6);
        assert!((temp.to_celsius() - 37.0).abs() < 0.01);
    }
    
    #[test]
    fn test_absolute_zero() {
        let temp = Temperature::from_kelvin(0.0);
        assert!((temp.to_celsius() - (-273.15)).abs() < 0.001);
        assert!((temp.to_fahrenheit() - (-459.67)).abs() < 0.01);
        assert!(temp.is_valid());
    }
    
    #[test]
    fn test_invalid_temperature() {
        let temp = Temperature::from_celsius(-300.0);
        assert!(!temp.is_valid());
    }
}