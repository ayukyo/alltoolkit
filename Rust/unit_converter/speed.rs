//! Speed/Velocity unit conversions
//!
//! Provides conversions between various speed/velocity units.

use crate::round_to;

/// Represents a speed/velocity value with conversion methods
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Speed {
    /// The speed in meters per second (base unit)
    meters_per_second: f64,
}

impl Speed {
    // Constructors from various units
    
    /// Creates a Speed from meters per second
    pub fn from_meters_per_second(mps: f64) -> Self {
        Self { meters_per_second: mps }
    }
    
    /// Creates a Speed from kilometers per hour
    pub fn from_kilometers_per_hour(kmph: f64) -> Self {
        Self { meters_per_second: kmph / 3.6 }
    }
    
    /// Creates a Speed from miles per hour
    pub fn from_miles_per_hour(mph: f64) -> Self {
        Self { meters_per_second: mph * 0.44704 }
    }
    
    /// Creates a Speed from feet per second
    pub fn from_feet_per_second(fps: f64) -> Self {
        Self { meters_per_second: fps * 0.3048 }
    }
    
    /// Creates a Speed from knots (nautical miles per hour)
    pub fn from_knots(kn: f64) -> Self {
        Self { meters_per_second: kn * 0.514444 }
    }
    
    /// Creates a Speed from mach number (at sea level, 15°C)
    pub fn from_mach(m: f64) -> Self {
        Self { meters_per_second: m * 340.29 }
    }
    
    /// Creates a Speed from centimeters per second
    pub fn from_centimeters_per_second(cmps: f64) -> Self {
        Self { meters_per_second: cmps / 100.0 }
    }
    
    /// Creates a Speed from centimeters per minute
    pub fn from_centimeters_per_minute(cmpm: f64) -> Self {
        Self { meters_per_second: cmpm / 6000.0 }
    }
    
    /// Creates a Speed from meters per minute
    pub fn from_meters_per_minute(mpm: f64) -> Self {
        Self { meters_per_second: mpm / 60.0 }
    }
    
    /// Creates a Speed from kilometers per second
    pub fn from_kilometers_per_second(kmps: f64) -> Self {
        Self { meters_per_second: kmps * 1000.0 }
    }
    
    /// Creates a Speed from miles per minute
    pub fn from_miles_per_minute(mpm: f64) -> Self {
        Self { meters_per_second: mpm * 26.8224 }
    }
    
    /// Creates a Speed from miles per second
    pub fn from_miles_per_second(mps: f64) -> Self {
        Self { meters_per_second: mps * 1609.344 }
    }
    
    // Conversion methods to various units
    
    /// Converts to meters per second
    pub fn to_meters_per_second(&self) -> f64 {
        self.meters_per_second
    }
    
    /// Converts to kilometers per hour
    pub fn to_kilometers_per_hour(&self) -> f64 {
        self.meters_per_second * 3.6
    }
    
    /// Converts to miles per hour
    pub fn to_miles_per_hour(&self) -> f64 {
        self.meters_per_second / 0.44704
    }
    
    /// Converts to feet per second
    pub fn to_feet_per_second(&self) -> f64 {
        self.meters_per_second / 0.3048
    }
    
    /// Converts to knots
    pub fn to_knots(&self) -> f64 {
        self.meters_per_second / 0.514444
    }
    
    /// Converts to mach number
    pub fn to_mach(&self) -> f64 {
        self.meters_per_second / 340.29
    }
    
    /// Converts to centimeters per second
    pub fn to_centimeters_per_second(&self) -> f64 {
        self.meters_per_second * 100.0
    }
    
    /// Converts to centimeters per minute
    pub fn to_centimeters_per_minute(&self) -> f64 {
        self.meters_per_second * 6000.0
    }
    
    /// Converts to meters per minute
    pub fn to_meters_per_minute(&self) -> f64 {
        self.meters_per_second * 60.0
    }
    
    /// Converts to kilometers per second
    pub fn to_kilometers_per_second(&self) -> f64 {
        self.meters_per_second / 1000.0
    }
    
    /// Converts to miles per minute
    pub fn to_miles_per_minute(&self) -> f64 {
        self.meters_per_second / 26.8224
    }
    
    /// Converts to miles per second
    pub fn to_miles_per_second(&self) -> f64 {
        self.meters_per_second / 1609.344
    }
    
    /// Returns the value rounded to the specified decimal places
    pub fn rounded(&self, decimals: u32) -> Self {
        Self {
            meters_per_second: round_to(self.meters_per_second, decimals),
        }
    }
    
    /// Calculates the time to travel a given distance
    /// Returns the time in seconds
    pub fn time_to_travel(&self, distance_meters: f64) -> f64 {
        if self.meters_per_second == 0.0 {
            f64::INFINITY
        } else {
            distance_meters / self.meters_per_second
        }
    }
    
    /// Calculates the distance traveled in a given time
    /// Returns the distance in meters
    pub fn distance_traveled(&self, time_seconds: f64) -> f64 {
        self.meters_per_second * time_seconds
    }
}

impl Default for Speed {
    fn default() -> Self {
        Self { meters_per_second: 0.0 }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mps_to_kmph() {
        let speed = Speed::from_meters_per_second(1.0);
        assert!((speed.to_kilometers_per_hour() - 3.6).abs() < 0.0001);
    }
    
    #[test]
    fn test_kmph_to_mps() {
        let speed = Speed::from_kilometers_per_hour(3.6);
        assert!((speed.to_meters_per_second() - 1.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_mph_to_kmph() {
        let speed = Speed::from_miles_per_hour(60.0);
        let kmph = speed.to_kilometers_per_hour();
        assert!((kmph - 96.56).abs() < 0.1);
    }
    
    #[test]
    fn test_knots_to_mph() {
        let speed = Speed::from_knots(1.0);
        let mph = speed.to_miles_per_hour();
        assert!((mph - 1.15).abs() < 0.01);
    }
    
    #[test]
    fn test_mach_to_kmph() {
        let speed = Speed::from_mach(1.0);
        let kmph = speed.to_kilometers_per_hour();
        assert!((kmph - 1225.0).abs() < 1.0);
    }
    
    #[test]
    fn test_feet_per_second_to_mps() {
        let speed = Speed::from_feet_per_second(1.0);
        assert!((speed.to_meters_per_second() - 0.3048).abs() < 0.0001);
    }
    
    #[test]
    fn test_round_trip() {
        let original = 100.0;
        let speed = Speed::from_kilometers_per_hour(original);
        assert!((speed.to_kilometers_per_hour() - original).abs() < 0.0001);
    }
    
    #[test]
    fn test_time_to_travel() {
        let speed = Speed::from_meters_per_second(10.0);
        let time = speed.time_to_travel(100.0);
        assert!((time - 10.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_distance_traveled() {
        let speed = Speed::from_meters_per_second(10.0);
        let distance = speed.distance_traveled(5.0);
        assert!((distance - 50.0).abs() < 0.0001);
    }
}