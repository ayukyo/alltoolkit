//! Unit Converter - A zero-dependency unit conversion library for Rust
//!
//! This module provides comprehensive unit conversion utilities including:
//! - Length conversions (meters, kilometers, miles, feet, inches, etc.)
//! - Weight/Mass conversions (kilograms, grams, pounds, ounces, etc.)
//! - Temperature conversions (Celsius, Fahrenheit, Kelvin)
//! - Area conversions (square meters, square feet, acres, hectares, etc.)
//! - Volume conversions (liters, gallons, cubic meters, etc.)
//! - Time conversions (seconds, minutes, hours, days, etc.)
//! - Speed conversions (m/s, km/h, mph, knots, etc.)
//! - Data conversions (bytes, KB, MB, GB, TB, etc.)
//!
//! # Example
//! ```
//! use unit_converter::{Length, Weight, Temperature, Area, Volume, Time, Speed, Data};
//!
//! // Length conversion
//! let meters = Length::from_miles(1.0).to_meters();
//! println!("1 mile = {} meters", meters);
//!
//! // Temperature conversion
//! let celsius = Temperature::from_fahrenheit(98.6).to_celsius();
//! println!("98.6°F = {}°C", celsius);
//! ```

pub mod length;
pub mod weight;
pub mod temperature;
pub mod area;
pub mod volume;
pub mod time;
pub mod speed;
pub mod data;

pub use length::Length;
pub use weight::Weight;
pub use temperature::Temperature;
pub use area::Area;
pub use volume::Volume;
pub use time::Time;
pub use speed::Speed;
pub use data::Data;

/// A trait for unit types that support conversion
pub trait UnitConversions {
    /// Returns the value in the base unit
    fn to_base(&self) -> f64;
    
    /// Creates a new instance from a base unit value
    fn from_base(value: f64) -> Self;
}

/// Helper function to round to a specified number of decimal places
pub fn round_to(value: f64, decimals: u32) -> f64 {
    let factor = 10_f64.powi(decimals as i32);
    (value * factor).round() / factor
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_length_conversions() {
        // 1 mile = 1609.344 meters
        let length = Length::from_miles(1.0);
        assert!((length.to_meters() - 1609.344).abs() < 0.001);
    }

    #[test]
    fn test_weight_conversions() {
        // 1 kg = 2.20462 lbs
        let weight = Weight::from_kilograms(1.0);
        assert!((weight.to_pounds() - 2.20462).abs() < 0.001);
    }

    #[test]
    fn test_temperature_conversions() {
        // 0°C = 32°F
        let temp = Temperature::from_celsius(0.0);
        assert!((temp.to_fahrenheit() - 32.0).abs() < 0.001);
        
        // 100°C = 212°F
        let temp = Temperature::from_celsius(100.0);
        assert!((temp.to_fahrenheit() - 212.0).abs() < 0.001);
    }

    #[test]
    fn test_area_conversions() {
        // 1 hectare = 10000 square meters
        let area = Area::from_hectares(1.0);
        assert!((area.to_square_meters() - 10000.0).abs() < 0.001);
    }

    #[test]
    fn test_volume_conversions() {
        // 1 liter = 1000 milliliters
        let volume = Volume::from_liters(1.0);
        assert!((volume.to_milliliters() - 1000.0).abs() < 0.001);
    }

    #[test]
    fn test_time_conversions() {
        // 1 hour = 3600 seconds
        let time = Time::from_hours(1.0);
        assert!((time.to_seconds() - 3600.0).abs() < 0.001);
    }

    #[test]
    fn test_speed_conversions() {
        // 1 m/s = 3.6 km/h
        let speed = Speed::from_meters_per_second(1.0);
        assert!((speed.to_kilometers_per_hour() - 3.6).abs() < 0.001);
    }

    #[test]
    fn test_data_conversions() {
        // 1 KB = 1000 bytes (decimal), 1 KiB = 1024 bytes (binary)
        let data_kb = Data::from_kilobytes(1.0);
        assert!((data_kb.to_bytes() - 1000.0).abs() < 0.001);
        
        let data_kib = Data::from_kibibytes(1.0);
        assert!((data_kib.to_bytes() - 1024.0).abs() < 0.001);
    }
}