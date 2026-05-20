//! Unit Converter Utilities for Rust
//!
//! A comprehensive, zero-dependency unit conversion library supporting
//! multiple measurement categories including length, weight, temperature,
//! area, volume, data storage, time, speed, and pressure.
//!
//! # Features
//!
//! - **Length**: meters, kilometers, miles, feet, inches, yards, centimeters, millimeters
//! - **Weight**: kilograms, grams, pounds, ounces, tons, metric tons
//! - **Temperature**: Celsius, Fahrenheit, Kelvin
//! - **Area**: square meters, square kilometers, hectares, acres, square feet
//! - **Volume**: liters, milliliters, gallons, quarts, pints, cups, fluid ounces
//! - **Data**: bytes, kilobytes, megabytes, gigabytes, terabytes, petabytes
//! - **Time**: seconds, minutes, hours, days, weeks, months, years
//! - **Speed**: m/s, km/h, mph, knots, mach
//! - **Pressure**: pascals, bar, psi, atmospheres
//!
//! Author: AllToolkit
//! License: MIT

use std::fmt;

// ============================================================================
// Error Handling
// ============================================================================

/// Represents errors that can occur during unit conversion
#[derive(Debug, Clone, PartialEq)]
pub enum ConversionError {
    /// Value is invalid (e.g., negative for units that don't support it)
    InvalidValue(String),
    /// Temperature below absolute zero
    BelowAbsoluteZero,
    /// Unsupported conversion between units
    UnsupportedConversion(String),
}

impl fmt::Display for ConversionError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ConversionError::InvalidValue(msg) => write!(f, "Invalid value: {}", msg),
            ConversionError::BelowAbsoluteZero => write!(f, "Temperature below absolute zero"),
            ConversionError::UnsupportedConversion(msg) => write!(f, "Unsupported conversion: {}", msg),
        }
    }
}

impl std::error::Error for ConversionError {}

pub type Result<T> = std::result::Result<T, ConversionError>;

// ============================================================================
// Length Conversion
// ============================================================================

/// Length units supported by the converter
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum LengthUnit {
    Meters,
    Kilometers,
    Miles,
    Feet,
    Inches,
    Yards,
    Centimeters,
    Millimeters,
}

impl LengthUnit {
    /// Get the conversion factor to meters
    fn to_meters_factor(&self) -> f64 {
        match self {
            LengthUnit::Meters => 1.0,
            LengthUnit::Kilometers => 1000.0,
            LengthUnit::Miles => 1609.344,
            LengthUnit::Feet => 0.3048,
            LengthUnit::Inches => 0.0254,
            LengthUnit::Yards => 0.9144,
            LengthUnit::Centimeters => 0.01,
            LengthUnit::Millimeters => 0.001,
        }
    }

    /// Get the unit abbreviation
    pub fn abbreviation(&self) -> &'static str {
        match self {
            LengthUnit::Meters => "m",
            LengthUnit::Kilometers => "km",
            LengthUnit::Miles => "mi",
            LengthUnit::Feet => "ft",
            LengthUnit::Inches => "in",
            LengthUnit::Yards => "yd",
            LengthUnit::Centimeters => "cm",
            LengthUnit::Millimeters => "mm",
        }
    }
}

impl fmt::Display for LengthUnit {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.abbreviation())
    }
}

/// Convert length from one unit to another
///
/// # Example
/// ```
/// use unit_converter_utils::{convert_length, LengthUnit};
///
/// let km = convert_length(1000.0, LengthUnit::Meters, LengthUnit::Kilometers).unwrap();
/// assert!((km - 1.0).abs() < 1e-10);
/// ```
pub fn convert_length(value: f64, from: LengthUnit, to: LengthUnit) -> Result<f64> {
    if value.is_nan() || value.is_infinite() {
        return Err(ConversionError::InvalidValue("Value must be finite".to_string()));
    }
    
    let meters = value * from.to_meters_factor();
    Ok(meters / to.to_meters_factor())
}

// ============================================================================
// Weight/Mass Conversion
// ============================================================================

/// Weight/Mass units supported by the converter
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum WeightUnit {
    Kilograms,
    Grams,
    Pounds,
    Ounces,
    MetricTons,
    ImperialTons,
    Milligrams,
}

impl WeightUnit {
    /// Get the conversion factor to kilograms
    fn to_kilograms_factor(&self) -> f64 {
        match self {
            WeightUnit::Kilograms => 1.0,
            WeightUnit::Grams => 0.001,
            WeightUnit::Pounds => 0.45359237,
            WeightUnit::Ounces => 0.028349523125,
            WeightUnit::MetricTons => 1000.0,
            WeightUnit::ImperialTons => 1016.0469088,
            WeightUnit::Milligrams => 0.000001,
        }
    }

    /// Get the unit abbreviation
    pub fn abbreviation(&self) -> &'static str {
        match self {
            WeightUnit::Kilograms => "kg",
            WeightUnit::Grams => "g",
            WeightUnit::Pounds => "lb",
            WeightUnit::Ounces => "oz",
            WeightUnit::MetricTons => "t",
            WeightUnit::ImperialTons => "ton",
            WeightUnit::Milligrams => "mg",
        }
    }
}

impl fmt::Display for WeightUnit {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.abbreviation())
    }
}

/// Convert weight from one unit to another
///
/// # Example
/// ```
/// use unit_converter_utils::{convert_weight, WeightUnit};
///
/// let kg = convert_weight(1000.0, WeightUnit::Grams, WeightUnit::Kilograms).unwrap();
/// assert!((kg - 1.0).abs() < 1e-10);
/// ```
pub fn convert_weight(value: f64, from: WeightUnit, to: WeightUnit) -> Result<f64> {
    if value.is_nan() || value.is_infinite() {
        return Err(ConversionError::InvalidValue("Value must be finite".to_string()));
    }
    
    let kg = value * from.to_kilograms_factor();
    Ok(kg / to.to_kilograms_factor())
}

// ============================================================================
// Temperature Conversion
// ============================================================================

/// Temperature units supported by the converter
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum TemperatureUnit {
    Celsius,
    Fahrenheit,
    Kelvin,
}

impl TemperatureUnit {
    /// Get the unit abbreviation
    pub fn abbreviation(&self) -> &'static str {
        match self {
            TemperatureUnit::Celsius => "°C",
            TemperatureUnit::Fahrenheit => "°F",
            TemperatureUnit::Kelvin => "K",
        }
    }
}

impl fmt::Display for TemperatureUnit {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.abbreviation())
    }
}

/// Convert temperature from one unit to another
///
/// # Example
/// ```
/// use unit_converter_utils::{convert_temperature, TemperatureUnit};
///
/// let f = convert_temperature(0.0, TemperatureUnit::Celsius, TemperatureUnit::Fahrenheit).unwrap();
/// assert!((f - 32.0).abs() < 1e-10);
/// ```
pub fn convert_temperature(value: f64, from: TemperatureUnit, to: TemperatureUnit) -> Result<f64> {
    if value.is_nan() || value.is_infinite() {
        return Err(ConversionError::InvalidValue("Value must be finite".to_string()));
    }
    
    // First convert to Kelvin
    let kelvin = match from {
        TemperatureUnit::Kelvin => value,
        TemperatureUnit::Celsius => value + 273.15,
        TemperatureUnit::Fahrenheit => (value - 32.0) * 5.0 / 9.0 + 273.15,
    };
    
    // Check for below absolute zero
    if kelvin < 0.0 {
        return Err(ConversionError::BelowAbsoluteZero);
    }
    
    // Then convert from Kelvin to target unit
    let result = match to {
        TemperatureUnit::Kelvin => kelvin,
        TemperatureUnit::Celsius => kelvin - 273.15,
        TemperatureUnit::Fahrenheit => (kelvin - 273.15) * 9.0 / 5.0 + 32.0,
    };
    
    Ok(result)
}

// ============================================================================
// Area Conversion
// ============================================================================

/// Area units supported by the converter
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum AreaUnit {
    SquareMeters,
    SquareKilometers,
    Hectares,
    Acres,
    SquareFeet,
    SquareYards,
    SquareMiles,
    SquareInches,
}

impl AreaUnit {
    /// Get the conversion factor to square meters
    fn to_square_meters_factor(&self) -> f64 {
        match self {
            AreaUnit::SquareMeters => 1.0,
            AreaUnit::SquareKilometers => 1_000_000.0,
            AreaUnit::Hectares => 10_000.0,
            AreaUnit::Acres => 4046.8564224,
            AreaUnit::SquareFeet => 0.09290304,
            AreaUnit::SquareYards => 0.83612736,
            AreaUnit::SquareMiles => 2_589_988.110336,
            AreaUnit::SquareInches => 0.00064516,
        }
    }

    /// Get the unit abbreviation
    pub fn abbreviation(&self) -> &'static str {
        match self {
            AreaUnit::SquareMeters => "m²",
            AreaUnit::SquareKilometers => "km²",
            AreaUnit::Hectares => "ha",
            AreaUnit::Acres => "ac",
            AreaUnit::SquareFeet => "ft²",
            AreaUnit::SquareYards => "yd²",
            AreaUnit::SquareMiles => "mi²",
            AreaUnit::SquareInches => "in²",
        }
    }
}

impl fmt::Display for AreaUnit {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.abbreviation())
    }
}

/// Convert area from one unit to another
///
/// # Example
/// ```
/// use unit_converter_utils::{convert_area, AreaUnit};
///
/// let km2 = convert_area(1_000_000.0, AreaUnit::SquareMeters, AreaUnit::SquareKilometers).unwrap();
/// assert!((km2 - 1.0).abs() < 1e-10);
/// ```
pub fn convert_area(value: f64, from: AreaUnit, to: AreaUnit) -> Result<f64> {
    if value.is_nan() || value.is_infinite() {
        return Err(ConversionError::InvalidValue("Value must be finite".to_string()));
    }
    
    let sq_meters = value * from.to_square_meters_factor();
    Ok(sq_meters / to.to_square_meters_factor())
}

// ============================================================================
// Volume Conversion
// ============================================================================

/// Volume units supported by the converter
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum VolumeUnit {
    Liters,
    Milliliters,
    GallonsUS,
    GallonsUK,
    Quarts,
    Pints,
    Cups,
    FluidOuncesUS,
    CubicMeters,
    CubicCentimeters,
}

impl VolumeUnit {
    /// Get the conversion factor to liters
    fn to_liters_factor(&self) -> f64 {
        match self {
            VolumeUnit::Liters => 1.0,
            VolumeUnit::Milliliters => 0.001,
            VolumeUnit::GallonsUS => 3.785411784,
            VolumeUnit::GallonsUK => 4.54609,
            VolumeUnit::Quarts => 0.946352946,
            VolumeUnit::Pints => 0.473176473,
            VolumeUnit::Cups => 0.2365882365,
            VolumeUnit::FluidOuncesUS => 0.0295735295625,
            VolumeUnit::CubicMeters => 1000.0,
            VolumeUnit::CubicCentimeters => 0.001,
        }
    }

    /// Get the unit abbreviation
    pub fn abbreviation(&self) -> &'static str {
        match self {
            VolumeUnit::Liters => "L",
            VolumeUnit::Milliliters => "mL",
            VolumeUnit::GallonsUS => "gal (US)",
            VolumeUnit::GallonsUK => "gal (UK)",
            VolumeUnit::Quarts => "qt",
            VolumeUnit::Pints => "pt",
            VolumeUnit::Cups => "cup",
            VolumeUnit::FluidOuncesUS => "fl oz",
            VolumeUnit::CubicMeters => "m³",
            VolumeUnit::CubicCentimeters => "cm³",
        }
    }
}

impl fmt::Display for VolumeUnit {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.abbreviation())
    }
}

/// Convert volume from one unit to another
///
/// # Example
/// ```
/// use unit_converter_utils::{convert_volume, VolumeUnit};
///
/// let ml = convert_volume(1.0, VolumeUnit::Liters, VolumeUnit::Milliliters).unwrap();
/// assert!((ml - 1000.0).abs() < 1e-10);
/// ```
pub fn convert_volume(value: f64, from: VolumeUnit, to: VolumeUnit) -> Result<f64> {
    if value.is_nan() || value.is_infinite() {
        return Err(ConversionError::InvalidValue("Value must be finite".to_string()));
    }
    
    let liters = value * from.to_liters_factor();
    Ok(liters / to.to_liters_factor())
}

// ============================================================================
// Data Storage Conversion
// ============================================================================

/// Data storage units supported by the converter
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum DataUnit {
    Bytes,
    Kilobytes,
    Megabytes,
    Gigabytes,
    Terabytes,
    Petabytes,
    Kibibytes,
    Mebibytes,
    Gibibytes,
    Tebibytes,
    Pebibytes,
    Bits,
    Kilobits,
    Megabits,
    Gigabits,
}

impl DataUnit {
    /// Get the conversion factor to bytes (or bits for bit units)
    fn to_base_factor(&self) -> f64 {
        match self {
            DataUnit::Bytes => 1.0,
            DataUnit::Kilobytes => 1000.0,
            DataUnit::Megabytes => 1_000_000.0,
            DataUnit::Gigabytes => 1_000_000_000.0,
            DataUnit::Terabytes => 1_000_000_000_000.0,
            DataUnit::Petabytes => 1_000_000_000_000_000.0,
            DataUnit::Kibibytes => 1024.0,
            DataUnit::Mebibytes => 1048576.0,
            DataUnit::Gibibytes => 1073741824.0,
            DataUnit::Tebibytes => 1099511627776.0,
            DataUnit::Pebibytes => 1125899906842624.0,
            DataUnit::Bits => 0.125,
            DataUnit::Kilobits => 125.0,
            DataUnit::Megabits => 125000.0,
            DataUnit::Gigabits => 125000000.0,
        }
    }

    /// Check if unit is a bit-based unit
    fn is_bits(&self) -> bool {
        matches!(self, DataUnit::Bits | DataUnit::Kilobits | DataUnit::Megabits | DataUnit::Gigabits)
    }

    /// Get the unit abbreviation
    pub fn abbreviation(&self) -> &'static str {
        match self {
            DataUnit::Bytes => "B",
            DataUnit::Kilobytes => "KB",
            DataUnit::Megabytes => "MB",
            DataUnit::Gigabytes => "GB",
            DataUnit::Terabytes => "TB",
            DataUnit::Petabytes => "PB",
            DataUnit::Kibibytes => "KiB",
            DataUnit::Mebibytes => "MiB",
            DataUnit::Gibibytes => "GiB",
            DataUnit::Tebibytes => "TiB",
            DataUnit::Pebibytes => "PiB",
            DataUnit::Bits => "b",
            DataUnit::Kilobits => "Kb",
            DataUnit::Megabits => "Mb",
            DataUnit::Gigabits => "Gb",
        }
    }
}

impl fmt::Display for DataUnit {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.abbreviation())
    }
}

/// Convert data storage from one unit to another
///
/// # Example
/// ```
/// use unit_converter_utils::{convert_data, DataUnit};
///
/// let kb = convert_data(1024.0, DataUnit::Bytes, DataUnit::Kilobytes).unwrap();
/// assert!((kb - 1.024).abs() < 1e-10);
/// ```
pub fn convert_data(value: f64, from: DataUnit, to: DataUnit) -> Result<f64> {
    if value.is_nan() || value.is_infinite() {
        return Err(ConversionError::InvalidValue("Value must be finite".to_string()));
    }
    
    let bytes = value * from.to_base_factor();
    Ok(bytes / to.to_base_factor())
}

// ============================================================================
// Time Conversion
// ============================================================================

/// Time units supported by the converter
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum TimeUnit {
    Seconds,
    Minutes,
    Hours,
    Days,
    Weeks,
    Months,    // Average month (30.44 days)
    Years,     // Average year (365.25 days)
    Milliseconds,
    Microseconds,
    Nanoseconds,
}

impl TimeUnit {
    /// Get the conversion factor to seconds
    fn to_seconds_factor(&self) -> f64 {
        match self {
            TimeUnit::Seconds => 1.0,
            TimeUnit::Minutes => 60.0,
            TimeUnit::Hours => 3600.0,
            TimeUnit::Days => 86400.0,
            TimeUnit::Weeks => 604800.0,
            TimeUnit::Months => 2629746.0, // 30.44 days average
            TimeUnit::Years => 31556952.0, // 365.25 days average
            TimeUnit::Milliseconds => 0.001,
            TimeUnit::Microseconds => 0.000001,
            TimeUnit::Nanoseconds => 0.000000001,
        }
    }

    /// Get the unit abbreviation
    pub fn abbreviation(&self) -> &'static str {
        match self {
            TimeUnit::Seconds => "s",
            TimeUnit::Minutes => "min",
            TimeUnit::Hours => "h",
            TimeUnit::Days => "d",
            TimeUnit::Weeks => "wk",
            TimeUnit::Months => "mo",
            TimeUnit::Years => "yr",
            TimeUnit::Milliseconds => "ms",
            TimeUnit::Microseconds => "μs",
            TimeUnit::Nanoseconds => "ns",
        }
    }
}

impl fmt::Display for TimeUnit {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.abbreviation())
    }
}

/// Convert time from one unit to another
///
/// # Example
/// ```
/// use unit_converter_utils::{convert_time, TimeUnit};
///
/// let min = convert_time(60.0, TimeUnit::Seconds, TimeUnit::Minutes).unwrap();
/// assert!((min - 1.0).abs() < 1e-10);
/// ```
pub fn convert_time(value: f64, from: TimeUnit, to: TimeUnit) -> Result<f64> {
    if value.is_nan() || value.is_infinite() {
        return Err(ConversionError::InvalidValue("Value must be finite".to_string()));
    }
    
    let seconds = value * from.to_seconds_factor();
    Ok(seconds / to.to_seconds_factor())
}

// ============================================================================
// Speed Conversion
// ============================================================================

/// Speed units supported by the converter
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum SpeedUnit {
    MetersPerSecond,
    KilometersPerHour,
    MilesPerHour,
    Knots,
    FeetPerSecond,
    Mach, // At sea level, 15°C
}

impl SpeedUnit {
    /// Get the conversion factor to meters per second
    fn to_mps_factor(&self) -> f64 {
        match self {
            SpeedUnit::MetersPerSecond => 1.0,
            SpeedUnit::KilometersPerHour => 0.277777778,
            SpeedUnit::MilesPerHour => 0.44704,
            SpeedUnit::Knots => 0.514444,
            SpeedUnit::FeetPerSecond => 0.3048,
            SpeedUnit::Mach => 340.29, // Speed of sound at sea level, 15°C
        }
    }

    /// Get the unit abbreviation
    pub fn abbreviation(&self) -> &'static str {
        match self {
            SpeedUnit::MetersPerSecond => "m/s",
            SpeedUnit::KilometersPerHour => "km/h",
            SpeedUnit::MilesPerHour => "mph",
            SpeedUnit::Knots => "kn",
            SpeedUnit::FeetPerSecond => "ft/s",
            SpeedUnit::Mach => "Mach",
        }
    }
}

impl fmt::Display for SpeedUnit {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.abbreviation())
    }
}

/// Convert speed from one unit to another
///
/// # Example
/// ```
/// use unit_converter_utils::{convert_speed, SpeedUnit};
///
/// let kmh = convert_speed(1.0, SpeedUnit::MetersPerSecond, SpeedUnit::KilometersPerHour).unwrap();
/// assert!((kmh - 3.6).abs() < 1e-6);
/// ```
pub fn convert_speed(value: f64, from: SpeedUnit, to: SpeedUnit) -> Result<f64> {
    if value.is_nan() || value.is_infinite() {
        return Err(ConversionError::InvalidValue("Value must be finite".to_string()));
    }
    
    let mps = value * from.to_mps_factor();
    Ok(mps / to.to_mps_factor())
}

// ============================================================================
// Pressure Conversion
// ============================================================================

/// Pressure units supported by the converter
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum PressureUnit {
    Pascals,
    Kilopascals,
    Bar,
    Psi,
    Atmospheres,
    MillimetersOfMercury,
    InchesOfMercury,
}

impl PressureUnit {
    /// Get the conversion factor to pascals
    fn to_pascals_factor(&self) -> f64 {
        match self {
            PressureUnit::Pascals => 1.0,
            PressureUnit::Kilopascals => 1000.0,
            PressureUnit::Bar => 100000.0,
            PressureUnit::Psi => 6894.757293168,
            PressureUnit::Atmospheres => 101325.0,
            PressureUnit::MillimetersOfMercury => 133.322,
            PressureUnit::InchesOfMercury => 3386.389,
        }
    }

    /// Get the unit abbreviation
    pub fn abbreviation(&self) -> &'static str {
        match self {
            PressureUnit::Pascals => "Pa",
            PressureUnit::Kilopascals => "kPa",
            PressureUnit::Bar => "bar",
            PressureUnit::Psi => "psi",
            PressureUnit::Atmospheres => "atm",
            PressureUnit::MillimetersOfMercury => "mmHg",
            PressureUnit::InchesOfMercury => "inHg",
        }
    }
}

impl fmt::Display for PressureUnit {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.abbreviation())
    }
}

/// Convert pressure from one unit to another
///
/// # Example
/// ```
/// use unit_converter_utils::{convert_pressure, PressureUnit};
///
/// let kpa = convert_pressure(1000.0, PressureUnit::Pascals, PressureUnit::Kilopascals).unwrap();
/// assert!((kpa - 1.0).abs() < 1e-10);
/// ```
pub fn convert_pressure(value: f64, from: PressureUnit, to: PressureUnit) -> Result<f64> {
    if value.is_nan() || value.is_infinite() {
        return Err(ConversionError::InvalidValue("Value must be finite".to_string()));
    }
    
    let pascals = value * from.to_pascals_factor();
    Ok(pascals / to.to_pascals_factor())
}

// ============================================================================
// Convenience Conversion Functions
// ============================================================================

/// Convert temperature from Celsius to Fahrenheit
pub fn celsius_to_fahrenheit(celsius: f64) -> Result<f64> {
    convert_temperature(celsius, TemperatureUnit::Celsius, TemperatureUnit::Fahrenheit)
}

/// Convert temperature from Fahrenheit to Celsius
pub fn fahrenheit_to_celsius(fahrenheit: f64) -> Result<f64> {
    convert_temperature(fahrenheit, TemperatureUnit::Fahrenheit, TemperatureUnit::Celsius)
}

/// Convert length from miles to kilometers
pub fn miles_to_km(miles: f64) -> Result<f64> {
    convert_length(miles, LengthUnit::Miles, LengthUnit::Kilometers)
}

/// Convert length from kilometers to miles
pub fn km_to_miles(km: f64) -> Result<f64> {
    convert_length(km, LengthUnit::Kilometers, LengthUnit::Miles)
}

/// Convert weight from pounds to kilograms
pub fn lbs_to_kg(lbs: f64) -> Result<f64> {
    convert_weight(lbs, WeightUnit::Pounds, WeightUnit::Kilograms)
}

/// Convert weight from kilograms to pounds
pub fn kg_to_lbs(kg: f64) -> Result<f64> {
    convert_weight(kg, WeightUnit::Kilograms, WeightUnit::Pounds)
}

// ============================================================================
// Unit Value Struct
// ============================================================================

/// A generic unit value that can be converted
#[derive(Debug, Clone)]
pub struct UnitValue {
    pub value: f64,
    pub unit: String,
}

impl UnitValue {
    /// Create a new unit value
    pub fn new(value: f64, unit: &str) -> Self {
        UnitValue {
            value,
            unit: unit.to_string(),
        }
    }
}

impl fmt::Display for UnitValue {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{} {}", self.value, self.unit)
    }
}

// ============================================================================
// Tests
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    // Length conversion tests
    #[test]
    fn test_length_meters_to_kilometers() {
        let result = convert_length(1000.0, LengthUnit::Meters, LengthUnit::Kilometers).unwrap();
        assert!((result - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_length_miles_to_km() {
        let result = convert_length(1.0, LengthUnit::Miles, LengthUnit::Kilometers).unwrap();
        assert!((result - 1.609344).abs() < 1e-6);
    }

    #[test]
    fn test_length_feet_to_inches() {
        let result = convert_length(1.0, LengthUnit::Feet, LengthUnit::Inches).unwrap();
        assert!((result - 12.0).abs() < 1e-10);
    }

    #[test]
    fn test_length_cm_to_inches() {
        let result = convert_length(2.54, LengthUnit::Centimeters, LengthUnit::Inches).unwrap();
        assert!((result - 1.0).abs() < 1e-6);
    }

    // Weight conversion tests
    #[test]
    fn test_weight_kg_to_lbs() {
        let result = convert_weight(1.0, WeightUnit::Kilograms, WeightUnit::Pounds).unwrap();
        assert!((result - 2.20462).abs() < 1e-4);
    }

    #[test]
    fn test_weight_grams_to_kg() {
        let result = convert_weight(1000.0, WeightUnit::Grams, WeightUnit::Kilograms).unwrap();
        assert!((result - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_weight_ounces_to_grams() {
        let result = convert_weight(1.0, WeightUnit::Ounces, WeightUnit::Grams).unwrap();
        assert!((result - 28.3495).abs() < 1e-3);
    }

    // Temperature conversion tests
    #[test]
    fn test_celsius_to_fahrenheit() {
        let result = convert_temperature(0.0, TemperatureUnit::Celsius, TemperatureUnit::Fahrenheit).unwrap();
        assert!((result - 32.0).abs() < 1e-10);
        
        let result2 = convert_temperature(100.0, TemperatureUnit::Celsius, TemperatureUnit::Fahrenheit).unwrap();
        assert!((result2 - 212.0).abs() < 1e-10);
    }

    #[test]
    fn test_fahrenheit_to_celsius() {
        let result = convert_temperature(32.0, TemperatureUnit::Fahrenheit, TemperatureUnit::Celsius).unwrap();
        assert!((result - 0.0).abs() < 1e-10);
        
        let result2 = convert_temperature(212.0, TemperatureUnit::Fahrenheit, TemperatureUnit::Celsius).unwrap();
        assert!((result2 - 100.0).abs() < 1e-10);
    }

    #[test]
    fn test_celsius_to_kelvin() {
        let result = convert_temperature(0.0, TemperatureUnit::Celsius, TemperatureUnit::Kelvin).unwrap();
        assert!((result - 273.15).abs() < 1e-10);
    }

    #[test]
    fn test_kelvin_to_celsius() {
        let result = convert_temperature(273.15, TemperatureUnit::Kelvin, TemperatureUnit::Celsius).unwrap();
        assert!((result - 0.0).abs() < 1e-10);
    }

    #[test]
    fn test_below_absolute_zero() {
        let result = convert_temperature(-274.0, TemperatureUnit::Celsius, TemperatureUnit::Kelvin);
        assert_eq!(result, Err(ConversionError::BelowAbsoluteZero));
    }

    // Area conversion tests
    #[test]
    fn test_area_sqm_to_sqkm() {
        let result = convert_area(1_000_000.0, AreaUnit::SquareMeters, AreaUnit::SquareKilometers).unwrap();
        assert!((result - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_area_hectares_to_acres() {
        let result = convert_area(1.0, AreaUnit::Hectares, AreaUnit::Acres).unwrap();
        assert!((result - 2.47105).abs() < 1e-4);
    }

    // Volume conversion tests
    #[test]
    fn test_volume_liters_to_ml() {
        let result = convert_volume(1.0, VolumeUnit::Liters, VolumeUnit::Milliliters).unwrap();
        assert!((result - 1000.0).abs() < 1e-10);
    }

    #[test]
    fn test_volume_gallons_to_liters() {
        let result = convert_volume(1.0, VolumeUnit::GallonsUS, VolumeUnit::Liters).unwrap();
        assert!((result - 3.78541).abs() < 1e-4);
    }

    #[test]
    fn test_volume_cups_to_ml() {
        let result = convert_volume(1.0, VolumeUnit::Cups, VolumeUnit::Milliliters).unwrap();
        assert!((result - 236.588).abs() < 1e-2);
    }

    // Data conversion tests
    #[test]
    fn test_data_bytes_to_kb() {
        let result = convert_data(1000.0, DataUnit::Bytes, DataUnit::Kilobytes).unwrap();
        assert!((result - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_data_bytes_to_kib() {
        let result = convert_data(1024.0, DataUnit::Bytes, DataUnit::Kibibytes).unwrap();
        assert!((result - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_data_gb_to_mb() {
        let result = convert_data(1.0, DataUnit::Gigabytes, DataUnit::Megabytes).unwrap();
        assert!((result - 1000.0).abs() < 1e-10);
    }

    #[test]
    fn test_data_megabits_to_megabytes() {
        let result = convert_data(8.0, DataUnit::Megabits, DataUnit::Megabytes).unwrap();
        assert!((result - 1.0).abs() < 1e-10);
    }

    // Time conversion tests
    #[test]
    fn test_time_seconds_to_minutes() {
        let result = convert_time(60.0, TimeUnit::Seconds, TimeUnit::Minutes).unwrap();
        assert!((result - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_time_hours_to_seconds() {
        let result = convert_time(1.0, TimeUnit::Hours, TimeUnit::Seconds).unwrap();
        assert!((result - 3600.0).abs() < 1e-10);
    }

    #[test]
    fn test_time_days_to_hours() {
        let result = convert_time(1.0, TimeUnit::Days, TimeUnit::Hours).unwrap();
        assert!((result - 24.0).abs() < 1e-10);
    }

    #[test]
    fn test_time_weeks_to_days() {
        let result = convert_time(1.0, TimeUnit::Weeks, TimeUnit::Days).unwrap();
        assert!((result - 7.0).abs() < 1e-10);
    }

    // Speed conversion tests
    #[test]
    fn test_speed_mps_to_kmh() {
        let result = convert_speed(1.0, SpeedUnit::MetersPerSecond, SpeedUnit::KilometersPerHour).unwrap();
        assert!((result - 3.6).abs() < 1e-6);
    }

    #[test]
    fn test_speed_mph_to_kmh() {
        let result = convert_speed(1.0, SpeedUnit::MilesPerHour, SpeedUnit::KilometersPerHour).unwrap();
        assert!((result - 1.60934).abs() < 1e-4);
    }

    #[test]
    fn test_speed_knots_to_mps() {
        let result = convert_speed(1.0, SpeedUnit::Knots, SpeedUnit::MetersPerSecond).unwrap();
        assert!((result - 0.514444).abs() < 1e-4);
    }

    // Pressure conversion tests
    #[test]
    fn test_pressure_pascal_to_kpa() {
        let result = convert_pressure(1000.0, PressureUnit::Pascals, PressureUnit::Kilopascals).unwrap();
        assert!((result - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_pressure_bar_to_psi() {
        let result = convert_pressure(1.0, PressureUnit::Bar, PressureUnit::Psi).unwrap();
        assert!((result - 14.5038).abs() < 1e-3);
    }

    #[test]
    fn test_pressure_atm_to_pa() {
        let result = convert_pressure(1.0, PressureUnit::Atmospheres, PressureUnit::Pascals).unwrap();
        assert!((result - 101325.0).abs() < 1.0);
    }

    // Convenience function tests
    #[test]
    fn test_convenience_celsius_to_fahrenheit() {
        let result = celsius_to_fahrenheit(0.0).unwrap();
        assert!((result - 32.0).abs() < 1e-10);
    }

    #[test]
    fn test_convenience_miles_to_km() {
        let result = miles_to_km(1.0).unwrap();
        assert!((result - 1.609344).abs() < 1e-6);
    }

    #[test]
    fn test_convenience_kg_to_lbs() {
        let result = kg_to_lbs(1.0).unwrap();
        assert!((result - 2.20462).abs() < 1e-4);
    }

    // Error handling tests
    #[test]
    fn test_nan_input() {
        let result = convert_length(f64::NAN, LengthUnit::Meters, LengthUnit::Kilometers);
        assert!(matches!(result, Err(ConversionError::InvalidValue(_))));
    }

    #[test]
    fn test_infinite_input() {
        let result = convert_length(f64::INFINITY, LengthUnit::Meters, LengthUnit::Kilometers);
        assert!(matches!(result, Err(ConversionError::InvalidValue(_))));
    }

    // Unit abbreviations
    #[test]
    fn test_unit_abbreviations() {
        assert_eq!(LengthUnit::Meters.abbreviation(), "m");
        assert_eq!(LengthUnit::Kilometers.abbreviation(), "km");
        assert_eq!(WeightUnit::Kilograms.abbreviation(), "kg");
        assert_eq!(WeightUnit::Pounds.abbreviation(), "lb");
        assert_eq!(TemperatureUnit::Celsius.abbreviation(), "°C");
        assert_eq!(TemperatureUnit::Fahrenheit.abbreviation(), "°F");
        assert_eq!(DataUnit::Megabytes.abbreviation(), "MB");
        assert_eq!(DataUnit::Mebibytes.abbreviation(), "MiB");
        assert_eq!(SpeedUnit::MetersPerSecond.abbreviation(), "m/s");
        assert_eq!(PressureUnit::Atmospheres.abbreviation(), "atm");
    }

    // Unit value display
    #[test]
    fn test_unit_value_display() {
        let uv = UnitValue::new(100.0, "km/h");
        assert_eq!(format!("{}", uv), "100 km/h");
    }

    // Round-trip conversion tests
    #[test]
    fn test_round_trip_length() {
        let original = 123.456;
        let converted = convert_length(original, LengthUnit::Miles, LengthUnit::Kilometers).unwrap();
        let back = convert_length(converted, LengthUnit::Kilometers, LengthUnit::Miles).unwrap();
        assert!((original - back).abs() < 1e-9);
    }

    #[test]
    fn test_round_trip_weight() {
        let original = 789.012;
        let converted = convert_weight(original, WeightUnit::Pounds, WeightUnit::Kilograms).unwrap();
        let back = convert_weight(converted, WeightUnit::Kilograms, WeightUnit::Pounds).unwrap();
        assert!((original - back).abs() < 1e-9);
    }

    #[test]
    fn test_round_trip_temperature() {
        let original = 23.5;
        let converted = convert_temperature(original, TemperatureUnit::Celsius, TemperatureUnit::Fahrenheit).unwrap();
        let back = convert_temperature(converted, TemperatureUnit::Fahrenheit, TemperatureUnit::Celsius).unwrap();
        assert!((original - back).abs() < 1e-9);
    }
}