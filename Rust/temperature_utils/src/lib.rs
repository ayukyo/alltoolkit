//! # Temperature Utils
//!
//! A comprehensive temperature conversion utility library.
//! Supports Celsius, Fahrenheit, Kelvin, Rankine, Delisle, Newton, Réaumur, and Rømer scales.
//! Zero external dependencies - uses only Rust standard library.
//!
//! ## Features
//!
//! - Convert between 8 temperature scales
//! - Parse temperature strings like "25°C" or "77F"
//! - Calculate wind chill, heat index, and dew point
//! - Temperature comparison and arithmetic operations
//! - Comfort level and state of matter assessments
//!
//! ## Example
//!
//! ```rust
//! use temperature_utils::{TemperatureUtils, TemperatureUnit};
//!
//! let utils = TemperatureUtils::new();
//! let fahrenheit = utils.celsius_to_fahrenheit(25.0);
//! println!("25°C = {}°F", fahrenheit);
//! ```

use std::fmt;
use std::str::FromStr;

/// Temperature unit enum representing different temperature scales
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum TemperatureUnit {
    Celsius,
    Fahrenheit,
    Kelvin,
    Rankine,
    Delisle,
    Newton,
    Reaumur,
    Romer,
}

impl TemperatureUnit {
    /// Get the symbol for this unit
    pub fn symbol(&self) -> &'static str {
        match self {
            TemperatureUnit::Celsius => "°C",
            TemperatureUnit::Fahrenheit => "°F",
            TemperatureUnit::Kelvin => "K",
            TemperatureUnit::Rankine => "°R",
            TemperatureUnit::Delisle => "°De",
            TemperatureUnit::Newton => "°N",
            TemperatureUnit::Reaumur => "°Ré",
            TemperatureUnit::Romer => "°Rø",
        }
    }

    /// Get the full name for this unit
    pub fn name(&self) -> &'static str {
        match self {
            TemperatureUnit::Celsius => "Celsius",
            TemperatureUnit::Fahrenheit => "Fahrenheit",
            TemperatureUnit::Kelvin => "Kelvin",
            TemperatureUnit::Rankine => "Rankine",
            TemperatureUnit::Delisle => "Delisle",
            TemperatureUnit::Newton => "Newton",
            TemperatureUnit::Reaumur => "Réaumur",
            TemperatureUnit::Romer => "Rømer",
        }
    }

    /// Get water freezing point in this unit
    pub fn freezing_point(&self) -> f64 {
        match self {
            TemperatureUnit::Celsius => 0.0,
            TemperatureUnit::Fahrenheit => 32.0,
            TemperatureUnit::Kelvin => 273.15,
            TemperatureUnit::Rankine => 491.67,
            TemperatureUnit::Delisle => 150.0,
            TemperatureUnit::Newton => 0.0,
            TemperatureUnit::Reaumur => 0.0,
            TemperatureUnit::Romer => 7.5,
        }
    }

    /// Get water boiling point in this unit
    pub fn boiling_point(&self) -> f64 {
        match self {
            TemperatureUnit::Celsius => 100.0,
            TemperatureUnit::Fahrenheit => 212.0,
            TemperatureUnit::Kelvin => 373.15,
            TemperatureUnit::Rankine => 671.641,
            TemperatureUnit::Delisle => 0.0,
            TemperatureUnit::Newton => 33.0,
            TemperatureUnit::Reaumur => 80.0,
            TemperatureUnit::Romer => 60.0,
        }
    }

    /// Get absolute zero in this unit
    pub fn absolute_zero(&self) -> f64 {
        match self {
            TemperatureUnit::Celsius => -273.15,
            TemperatureUnit::Fahrenheit => -459.67,
            TemperatureUnit::Kelvin => 0.0,
            TemperatureUnit::Rankine => 0.0,
            TemperatureUnit::Delisle => 559.725,
            TemperatureUnit::Newton => -90.1395,
            TemperatureUnit::Reaumur => -218.52,
            TemperatureUnit::Romer => -135.90375,
        }
    }

    /// Get all supported units
    pub fn all() -> Vec<TemperatureUnit> {
        vec![
            TemperatureUnit::Celsius,
            TemperatureUnit::Fahrenheit,
            TemperatureUnit::Kelvin,
            TemperatureUnit::Rankine,
            TemperatureUnit::Delisle,
            TemperatureUnit::Newton,
            TemperatureUnit::Reaumur,
            TemperatureUnit::Romer,
        ]
    }
}

impl fmt::Display for TemperatureUnit {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.symbol())
    }
}

impl FromStr for TemperatureUnit {
    type Err = TemperatureError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let normalized = normalize_unit_string(s);
        match normalized {
            "C" => Ok(TemperatureUnit::Celsius),
            "F" => Ok(TemperatureUnit::Fahrenheit),
            "K" => Ok(TemperatureUnit::Kelvin),
            "R" => Ok(TemperatureUnit::Rankine),
            "De" => Ok(TemperatureUnit::Delisle),
            "N" => Ok(TemperatureUnit::Newton),
            "Ré" => Ok(TemperatureUnit::Reaumur),
            "Rø" => Ok(TemperatureUnit::Romer),
            _ => Err(TemperatureError::InvalidUnit(s.to_string())),
        }
    }
}

/// Normalize unit string variations
fn normalize_unit_string(s: &str) -> &str {
    let s = s.trim();
    match s {
        "°C" | "C" | "c" | "℃" => "C",
        "°F" | "F" | "f" | "℉" => "F",
        "K" | "k" => "K",
        "°R" | "R" | "r" => "R",
        "°De" | "De" | "de" | "D" | "d" => "De",
        "°N" | "N" | "n" => "N",
        "°Ré" | "Ré" | "ré" | "Re" | "re" => "Ré",
        "°Rø" | "Rø" | "rø" | "Ro" | "ro" => "Rø",
        _ => s,
    }
}

/// Temperature value with unit
#[derive(Debug, Clone, Copy)]
pub struct Temperature {
    pub value: f64,
    pub unit: TemperatureUnit,
}

impl Temperature {
    /// Create a new temperature
    pub fn new(value: f64, unit: TemperatureUnit) -> Self {
        Self { value, unit }
    }

    /// Create temperature from Celsius
    pub fn from_celsius(value: f64) -> Self {
        Self::new(value, TemperatureUnit::Celsius)
    }

    /// Create temperature from Fahrenheit
    pub fn from_fahrenheit(value: f64) -> Self {
        Self::new(value, TemperatureUnit::Fahrenheit)
    }

    /// Create temperature from Kelvin
    pub fn from_kelvin(value: f64) -> Self {
        Self::new(value, TemperatureUnit::Kelvin)
    }

    /// Convert to another unit
    pub fn convert_to(&self, target: TemperatureUnit, utils: &TemperatureUtils) -> Self {
        utils.convert_temperature(*self, target)
    }
}

impl fmt::Display for Temperature {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:.2}{}", self.value, self.unit.symbol())
    }
}

impl FromStr for Temperature {
    type Err = TemperatureError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        parse_temperature(s)
    }
}

/// Error types for temperature operations
#[derive(Debug, Clone)]
pub enum TemperatureError {
    InvalidUnit(String),
    ParseError(String),
    InvalidValue(String),
}

impl fmt::Display for TemperatureError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            TemperatureError::InvalidUnit(s) => write!(f, "Invalid temperature unit: {}", s),
            TemperatureError::ParseError(s) => write!(f, "Failed to parse temperature: {}", s),
            TemperatureError::InvalidValue(s) => write!(f, "Invalid temperature value: {}", s),
        }
    }
}

impl std::error::Error for TemperatureError {}

/// Parse temperature string like "25°C" or "77F"
pub fn parse_temperature(s: &str) -> Result<Temperature, TemperatureError> {
    let s = s.trim();
    
    // Try to find number and unit
    let mut number_end = 0;
    for (i, c) in s.char_indices() {
        if c.is_ascii_digit() || c == '.' || c == '-' || c == '+' {
            number_end = i + c.len_utf8();
        } else {
            break;
        }
    }
    
    if number_end == 0 {
        return Err(TemperatureError::ParseError(s.to_string()));
    }
    
    let number_str = &s[..number_end];
    let unit_str = &s[number_end..];
    
    let value: f64 = number_str.parse()
        .map_err(|_| TemperatureError::ParseError(s.to_string()))?;
    
    let unit: TemperatureUnit = unit_str.parse()
        .map_err(|_| TemperatureError::ParseError(s.to_string()))?;
    
    Ok(Temperature::new(value, unit))
}

/// Main temperature utilities struct
#[derive(Debug, Clone)]
pub struct TemperatureUtils {
    precision: usize,
}

impl Default for TemperatureUtils {
    fn default() -> Self {
        Self::new()
    }
}

impl TemperatureUtils {
    /// Create a new TemperatureUtils with default precision (2 decimal places)
    pub fn new() -> Self {
        Self { precision: 2 }
    }

    /// Create with custom precision
    pub fn with_precision(precision: usize) -> Self {
        Self { precision }
    }

    /// Set precision for rounding
    pub fn set_precision(&mut self, precision: usize) {
        self.precision = precision;
    }

    /// Round value to configured precision
    fn round(&self, value: f64) -> f64 {
        let factor = 10_f64.powi(self.precision as i32);
        (value * factor).round() / factor
    }

    /// Convert temperature from one unit to another
    pub fn convert(&self, value: f64, from: TemperatureUnit, to: TemperatureUnit) -> f64 {
        let celsius = self.to_celsius(value, from);
        self.round(self.from_celsius(celsius, to))
    }

    /// Convert a Temperature struct to another unit
    pub fn convert_temperature(&self, temp: Temperature, to: TemperatureUnit) -> Temperature {
        Temperature::new(self.convert(temp.value, temp.unit, to), to)
    }

    /// Convert any temperature to Celsius
    fn to_celsius(&self, value: f64, from: TemperatureUnit) -> f64 {
        match from {
            TemperatureUnit::Celsius => value,
            TemperatureUnit::Fahrenheit => (value - 32.0) * 5.0 / 9.0,
            TemperatureUnit::Kelvin => value - 273.15,
            TemperatureUnit::Rankine => (value - 491.67) * 5.0 / 9.0,
            TemperatureUnit::Delisle => 100.0 - value * 2.0 / 3.0,
            TemperatureUnit::Newton => value * 100.0 / 33.0,
            TemperatureUnit::Reaumur => value * 5.0 / 4.0,
            TemperatureUnit::Romer => (value - 7.5) * 40.0 / 21.0,
        }
    }

    /// Convert Celsius to any temperature unit
    fn from_celsius(&self, celsius: f64, to: TemperatureUnit) -> f64 {
        match to {
            TemperatureUnit::Celsius => celsius,
            TemperatureUnit::Fahrenheit => celsius * 9.0 / 5.0 + 32.0,
            TemperatureUnit::Kelvin => celsius + 273.15,
            TemperatureUnit::Rankine => (celsius + 273.15) * 9.0 / 5.0,
            TemperatureUnit::Delisle => (100.0 - celsius) * 3.0 / 2.0,
            TemperatureUnit::Newton => celsius * 33.0 / 100.0,
            TemperatureUnit::Reaumur => celsius * 4.0 / 5.0,
            TemperatureUnit::Romer => celsius * 21.0 / 40.0 + 7.5,
        }
    }

    /// Convert Celsius to Fahrenheit
    pub fn celsius_to_fahrenheit(&self, celsius: f64) -> f64 {
        self.convert(celsius, TemperatureUnit::Celsius, TemperatureUnit::Fahrenheit)
    }

    /// Convert Fahrenheit to Celsius
    pub fn fahrenheit_to_celsius(&self, fahrenheit: f64) -> f64 {
        self.convert(fahrenheit, TemperatureUnit::Fahrenheit, TemperatureUnit::Celsius)
    }

    /// Convert Celsius to Kelvin
    pub fn celsius_to_kelvin(&self, celsius: f64) -> f64 {
        self.convert(celsius, TemperatureUnit::Celsius, TemperatureUnit::Kelvin)
    }

    /// Convert Kelvin to Celsius
    pub fn kelvin_to_celsius(&self, kelvin: f64) -> f64 {
        self.convert(kelvin, TemperatureUnit::Kelvin, TemperatureUnit::Celsius)
    }

    /// Convert Fahrenheit to Kelvin
    pub fn fahrenheit_to_kelvin(&self, fahrenheit: f64) -> f64 {
        self.convert(fahrenheit, TemperatureUnit::Fahrenheit, TemperatureUnit::Kelvin)
    }

    /// Convert Kelvin to Fahrenheit
    pub fn kelvin_to_fahrenheit(&self, kelvin: f64) -> f64 {
        self.convert(kelvin, TemperatureUnit::Kelvin, TemperatureUnit::Fahrenheit)
    }

    /// Convert a temperature to all supported units
    pub fn convert_all(&self, value: f64, from: TemperatureUnit) -> Vec<(TemperatureUnit, f64)> {
        TemperatureUnit::all()
            .into_iter()
            .map(|unit| (unit, self.convert(value, from, unit)))
            .collect()
    }

    /// Compare two temperatures
    pub fn compare(&self, t1: Temperature, t2: Temperature) -> std::cmp::Ordering {
        let c1 = self.to_celsius(t1.value, t1.unit);
        let c2 = self.to_celsius(t2.value, t2.unit);
        c1.partial_cmp(&c2).unwrap_or(std::cmp::Ordering::Equal)
    }

    /// Check if two temperatures are equal
    pub fn equal(&self, t1: Temperature, t2: Temperature) -> bool {
        self.compare(t1, t2) == std::cmp::Ordering::Equal
    }

    /// Check if t1 is less than t2
    pub fn less_than(&self, t1: Temperature, t2: Temperature) -> bool {
        self.compare(t1, t2) == std::cmp::Ordering::Less
    }

    /// Check if t1 is greater than t2
    pub fn greater_than(&self, t1: Temperature, t2: Temperature) -> bool {
        self.compare(t1, t2) == std::cmp::Ordering::Greater
    }

    /// Add two temperatures (result in t1's unit)
    pub fn add(&self, t1: Temperature, t2: Temperature) -> Temperature {
        let c1 = self.to_celsius(t1.value, t1.unit);
        let c2 = self.to_celsius(t2.value, t2.unit);
        let result = self.from_celsius(c1 + c2, t1.unit);
        Temperature::new(self.round(result), t1.unit)
    }

    /// Subtract t2 from t1 (result in t1's unit)
    pub fn subtract(&self, t1: Temperature, t2: Temperature) -> Temperature {
        let c1 = self.to_celsius(t1.value, t1.unit);
        let c2 = self.to_celsius(t2.value, t2.unit);
        let result = self.from_celsius(c1 - c2, t1.unit);
        Temperature::new(self.round(result), t1.unit)
    }

    /// Scale a temperature by a factor
    pub fn scale(&self, temp: Temperature, factor: f64) -> Temperature {
        Temperature::new(self.round(temp.value * factor), temp.unit)
    }

    /// Calculate average of multiple temperatures
    pub fn average(&self, temps: &[Temperature], result_unit: TemperatureUnit) -> Temperature {
        if temps.is_empty() {
            return Temperature::new(0.0, result_unit);
        }

        let sum: f64 = temps.iter()
            .map(|t| self.to_celsius(t.value, t.unit))
            .sum();
        
        let avg_celsius = sum / temps.len() as f64;
        let result = self.from_celsius(avg_celsius, result_unit);
        Temperature::new(self.round(result), result_unit)
    }

    /// Check if temperature is below water freezing point
    pub fn is_below_freezing(&self, temp: Temperature) -> bool {
        let celsius = self.to_celsius(temp.value, temp.unit);
        celsius < 0.0
    }

    /// Check if temperature is above water boiling point
    pub fn is_above_boiling(&self, temp: Temperature) -> bool {
        let celsius = self.to_celsius(temp.value, temp.unit);
        celsius > 100.0
    }

    /// Check if temperature is at or below absolute zero
    pub fn is_absolute_zero(&self, temp: Temperature) -> bool {
        let celsius = self.to_celsius(temp.value, temp.unit);
        celsius <= -273.15
    }

    /// Get state of matter for water at this temperature
    pub fn state_of_matter(&self, temp: Temperature) -> &'static str {
        let celsius = self.to_celsius(temp.value, temp.unit);
        
        if celsius <= 0.0 {
            "solid (ice)"
        } else if celsius < 100.0 {
            "liquid (water)"
        } else {
            "gas (steam)"
        }
    }

    /// Get comfort level assessment
    pub fn comfort_level(&self, temp: Temperature) -> &'static str {
        let celsius = self.to_celsius(temp.value, temp.unit);
        
        match celsius {
            c if c < 18.0 => "Too cold",
            c if c <= 24.0 => "Comfortable",
            c if c <= 26.0 => "Slightly warm",
            c if c <= 30.0 => "Warm",
            _ => "Too hot",
        }
    }

    /// Get human-readable description of temperature
    pub fn describe(&self, temp: Temperature) -> String {
        let celsius = self.to_celsius(temp.value, temp.unit);
        
        let desc = match celsius {
            c if c <= -273.15 => "Absolute zero - the lowest possible temperature",
            c if c < -100.0 => "Extremely cold - far below freezing",
            c if c < -40.0 => "Very cold - extreme arctic conditions",
            c if c < -20.0 => "Very cold - severe winter weather",
            c if c < 0.0 => "Below freezing - icy conditions",
            c if c < 10.0 => "Cold - winter-like temperature",
            c if c < 20.0 => "Cool - mild weather",
            c if c < 25.0 => "Comfortable - room temperature",
            c if c < 30.0 => "Warm - pleasant weather",
            c if c < 35.0 => "Warm - hot summer day",
            c if c < 40.0 => "Hot - heat wave conditions",
            c if c < 50.0 => "Very hot - dangerous heat",
            c if c < 100.0 => "Extremely hot - dangerous temperatures",
            c if c < 200.0 => "Boiling water temperature range",
            c if c < 500.0 => "High temperature - cooking range",
            c if c < 1000.0 => "Very high temperature - industrial processes",
            _ => "Extreme temperature",
        };
        
        format!("{} {}", temp, desc)
    }

    /// Calculate wind chill temperature
    /// Formula: Wind Chill = 13.12 + 0.6215×T - 11.37×V^0.16 + 0.3965×T×V^0.16
    pub fn wind_chill(&self, temp_celsius: f64, wind_speed_kmh: f64) -> f64 {
        if temp_celsius > 10.0 || wind_speed_kmh < 4.8 {
            return temp_celsius; // Formula not applicable
        }
        
        let wind_pow = wind_speed_kmh.powf(0.16);
        let chill = 13.12 + 0.6215 * temp_celsius - 
                    11.37 * wind_pow + 
                    0.3965 * temp_celsius * wind_pow;
        
        self.round(chill)
    }

    /// Calculate heat index temperature
    pub fn heat_index(&self, temp_celsius: f64, relative_humidity: f64) -> f64 {
        if temp_celsius < 27.0 {
            return temp_celsius; // Formula not applicable below 27°C
        }
        
        // Convert to Fahrenheit for standard formula
        let temp_f = temp_celsius * 9.0 / 5.0 + 32.0;
        
        let hi = -42.379 + 
                 2.04901523 * temp_f + 
                 10.14333127 * relative_humidity -
                 0.22475541 * temp_f * relative_humidity -
                 0.00683783 * temp_f * temp_f -
                 0.05481717 * relative_humidity * relative_humidity +
                 0.00122874 * temp_f * temp_f * relative_humidity +
                 0.00085282 * temp_f * relative_humidity * relative_humidity -
                 0.00000199 * temp_f * temp_f * relative_humidity * relative_humidity;
        
        // Convert back to Celsius
        self.round((hi - 32.0) * 5.0 / 9.0)
    }

    /// Calculate dew point temperature (Magnus formula)
    pub fn dew_point(&self, temp_celsius: f64, relative_humidity: f64) -> f64 {
        const A: f64 = 17.27;
        const B: f64 = 237.7;
        
        let alpha = (A * temp_celsius) / (B + temp_celsius) + 
                    (relative_humidity / 100.0).ln();
        let dew_point = (B * alpha) / (A - alpha);
        
        self.round(dew_point)
    }
}

/// Check if a string is a valid temperature unit
pub fn is_valid_unit(s: &str) -> bool {
    TemperatureUnit::from_str(s).is_ok()
}

/// Format temperature value with unit symbol
pub fn format_temperature(value: f64, unit: TemperatureUnit, precision: usize) -> String {
    format!("{:.p$}{}", value, unit.symbol(), p = precision)
}

#[cfg(test)]
mod tests {
    use super::*;
    const EPSILON: f64 = 0.01;

    fn approx_eq(a: f64, b: f64) -> bool {
        (a - b).abs() < EPSILON
    }

    #[test]
    fn test_celsius_to_fahrenheit() {
        let utils = TemperatureUtils::new();
        
        assert!(approx_eq(utils.celsius_to_fahrenheit(0.0), 32.0));
        assert!(approx_eq(utils.celsius_to_fahrenheit(100.0), 212.0));
        assert!(approx_eq(utils.celsius_to_fahrenheit(-40.0), -40.0));
        assert!(approx_eq(utils.celsius_to_fahrenheit(37.0), 98.6));
    }

    #[test]
    fn test_fahrenheit_to_celsius() {
        let utils = TemperatureUtils::new();
        
        assert!(approx_eq(utils.fahrenheit_to_celsius(32.0), 0.0));
        assert!(approx_eq(utils.fahrenheit_to_celsius(212.0), 100.0));
        assert!(approx_eq(utils.fahrenheit_to_celsius(-40.0), -40.0));
        assert!(approx_eq(utils.fahrenheit_to_celsius(98.6), 37.0));
    }

    #[test]
    fn test_celsius_to_kelvin() {
        let utils = TemperatureUtils::new();
        
        assert!(approx_eq(utils.celsius_to_kelvin(0.0), 273.15));
        assert!(approx_eq(utils.celsius_to_kelvin(100.0), 373.15));
        assert!(approx_eq(utils.celsius_to_kelvin(-273.15), 0.0));
    }

    #[test]
    fn test_kelvin_to_celsius() {
        let utils = TemperatureUtils::new();
        
        assert!(approx_eq(utils.kelvin_to_celsius(273.15), 0.0));
        assert!(approx_eq(utils.kelvin_to_celsius(373.15), 100.0));
        assert!(approx_eq(utils.kelvin_to_celsius(0.0), -273.15));
    }

    #[test]
    fn test_convert() {
        let utils = TemperatureUtils::new();
        
        // Celsius to Fahrenheit
        assert!(approx_eq(utils.convert(0.0, TemperatureUnit::Celsius, TemperatureUnit::Fahrenheit), 32.0));
        
        // Fahrenheit to Kelvin
        assert!(approx_eq(utils.convert(32.0, TemperatureUnit::Fahrenheit, TemperatureUnit::Kelvin), 273.15));
        
        // Celsius to Rankine
        assert!(approx_eq(utils.convert(0.0, TemperatureUnit::Celsius, TemperatureUnit::Rankine), 491.67));
    }

    #[test]
    fn test_convert_all() {
        let utils = TemperatureUtils::new();
        let results = utils.convert_all(0.0, TemperatureUnit::Celsius);
        
        assert_eq!(results.len(), 8);
        
        // Find Fahrenheit result
        let f_result = results.iter()
            .find(|(u, _)| *u == TemperatureUnit::Fahrenheit)
            .map(|(_, v)| v);
        assert!(approx_eq(*f_result.unwrap(), 32.0));
    }

    #[test]
    fn test_parse_temperature() {
        let temp: Temperature = "25°C".parse().unwrap();
        assert_eq!(temp.value, 25.0);
        assert_eq!(temp.unit, TemperatureUnit::Celsius);
        
        let temp: Temperature = "77F".parse().unwrap();
        assert_eq!(temp.value, 77.0);
        assert_eq!(temp.unit, TemperatureUnit::Fahrenheit);
        
        let temp: Temperature = "300K".parse().unwrap();
        assert_eq!(temp.value, 300.0);
        assert_eq!(temp.unit, TemperatureUnit::Kelvin);
    }

    #[test]
    fn test_temperature_display() {
        let temp = Temperature::from_celsius(25.0);
        assert!(temp.to_string().contains("25"));
        assert!(temp.to_string().contains("°C"));
    }

    #[test]
    fn test_unit_properties() {
        assert_eq!(TemperatureUnit::Celsius.symbol(), "°C");
        assert_eq!(TemperatureUnit::Celsius.name(), "Celsius");
        assert_eq!(TemperatureUnit::Celsius.freezing_point(), 0.0);
        assert_eq!(TemperatureUnit::Celsius.boiling_point(), 100.0);
    }

    #[test]
    fn test_temperature_arithmetic() {
        let utils = TemperatureUtils::new();
        
        let t1 = Temperature::from_celsius(20.0);
        let t2 = Temperature::from_celsius(10.0);
        
        let sum = utils.add(t1, t2);
        assert!(approx_eq(sum.value, 30.0));
        
        let diff = utils.subtract(t1, t2);
        assert!(approx_eq(diff.value, 10.0));
    }

    #[test]
    fn test_temperature_comparison() {
        let utils = TemperatureUtils::new();
        
        let t1 = Temperature::from_celsius(20.0);
        let t2 = Temperature::from_celsius(30.0);
        let t3 = Temperature::from_fahrenheit(68.0); // ≈ 20°C
        
        assert!(utils.less_than(t1, t2));
        assert!(utils.greater_than(t2, t1));
        assert!(utils.equal(t1, t3));
    }

    #[test]
    fn test_average() {
        let utils = TemperatureUtils::new();
        
        let temps = [
            Temperature::from_celsius(10.0),
            Temperature::from_celsius(20.0),
            Temperature::from_celsius(30.0),
        ];
        
        let avg = utils.average(&temps, TemperatureUnit::Celsius);
        assert!(approx_eq(avg.value, 20.0));
    }

    #[test]
    fn test_state_of_matter() {
        let utils = TemperatureUtils::new();
        
        assert_eq!(utils.state_of_matter(Temperature::from_celsius(-10.0)), "solid (ice)");
        assert_eq!(utils.state_of_matter(Temperature::from_celsius(25.0)), "liquid (water)");
        assert_eq!(utils.state_of_matter(Temperature::from_celsius(110.0)), "gas (steam)");
    }

    #[test]
    fn test_comfort_level() {
        let utils = TemperatureUtils::new();
        
        assert_eq!(utils.comfort_level(Temperature::from_celsius(15.0)), "Too cold");
        assert_eq!(utils.comfort_level(Temperature::from_celsius(22.0)), "Comfortable");
        assert_eq!(utils.comfort_level(Temperature::from_celsius(28.0)), "Warm");
        assert_eq!(utils.comfort_level(Temperature::from_celsius(32.0)), "Too hot");
    }

    #[test]
    fn test_wind_chill() {
        let utils = TemperatureUtils::new();
        
        // Wind chill should be colder than actual
        let chill = utils.wind_chill(-10.0, 15.0);
        assert!(chill < -10.0);
        
        // Not applicable above 10°C
        let chill2 = utils.wind_chill(15.0, 15.0);
        assert_eq!(chill2, 15.0);
    }

    #[test]
    fn test_heat_index() {
        let utils = TemperatureUtils::new();
        
        // Heat index should be warmer than actual
        let hi = utils.heat_index(32.0, 70.0);
        assert!(hi > 32.0);
        
        // Not applicable below 27°C
        let hi2 = utils.heat_index(20.0, 70.0);
        assert_eq!(hi2, 20.0);
    }

    #[test]
    fn test_dew_point() {
        let utils = TemperatureUtils::new();
        
        // Dew point should be lower than temperature
        let dp = utils.dew_point(25.0, 50.0);
        assert!(dp < 25.0);
        
        // At 100% humidity, dew point ≈ temperature
        let dp2 = utils.dew_point(25.0, 100.0);
        assert!(approx_eq(dp2, 25.0));
    }

    #[test]
    fn test_is_below_freezing() {
        let utils = TemperatureUtils::new();
        
        assert!(utils.is_below_freezing(Temperature::from_celsius(-5.0)));
        assert!(!utils.is_below_freezing(Temperature::from_celsius(5.0)));
    }

    #[test]
    fn test_is_above_boiling() {
        let utils = TemperatureUtils::new();
        
        assert!(utils.is_above_boiling(Temperature::from_celsius(105.0)));
        assert!(!utils.is_above_boiling(Temperature::from_celsius(50.0)));
    }

    #[test]
    fn test_precision() {
        let utils = TemperatureUtils::with_precision(4);
        let result = utils.celsius_to_fahrenheit(37.0);
        // Should round to 4 decimal places
        assert!(approx_eq(result, 98.6));
    }

    #[test]
    fn test_historical_scales() {
        let utils = TemperatureUtils::new();
        
        // Water freezing point in Delisle: 150
        assert!(approx_eq(utils.convert(0.0, TemperatureUnit::Celsius, TemperatureUnit::Delisle), 150.0));
        
        // Water freezing point in Newton: 0
        assert!(approx_eq(utils.convert(0.0, TemperatureUnit::Celsius, TemperatureUnit::Newton), 0.0));
        
        // Water freezing point in Réaumur: 0
        assert!(approx_eq(utils.convert(0.0, TemperatureUnit::Celsius, TemperatureUnit::Reaumur), 0.0));
        
        // Water freezing point in Rømer: 7.5
        assert!(approx_eq(utils.convert(0.0, TemperatureUnit::Celsius, TemperatureUnit::Romer), 7.5));
    }
}