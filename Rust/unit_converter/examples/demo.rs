//! Unit Converter Examples
//!
//! This example demonstrates the usage of all unit conversion types.

use unit_converter::{Length, Weight, Temperature, Area, Volume, Time, Speed, Data};

fn main() {
    println!("=== Unit Converter Demo ===\n");

    // Length conversions
    println!("--- Length Conversions ---");
    let length = Length::from_miles(26.2); // Marathon distance
    println!("Marathon distance:");
    println!("  {:.2} miles", 26.2);
    println!("  {:.2} kilometers", length.to_kilometers());
    println!("  {:.0} meters", length.to_meters());
    println!("  {:.0} feet", length.to_feet());
    println!();

    // Weight conversions
    println!("--- Weight Conversions ---");
    let weight = Weight::from_pounds(150.0);
    println!("150 pounds:");
    println!("  {:.2} kilograms", weight.to_kilograms());
    println!("  {:.0} grams", weight.to_grams());
    println!("  {:.2} ounces", weight.to_ounces());
    println!("  {:.2} stones", weight.to_stones());
    println!();

    // Temperature conversions
    println!("--- Temperature Conversions ---");
    let temp = Temperature::from_fahrenheit(98.6);
    println!("Body temperature (98.6°F):");
    println!("  {:.2}°C", temp.to_celsius());
    println!("  {:.2} K", temp.to_kelvin());
    
    let boiling = Temperature::from_celsius(100.0);
    println!("Boiling point of water (100°C):");
    println!("  {:.2}°F", boiling.to_fahrenheit());
    println!("  {:.2} K", boiling.to_kelvin());
    println!();

    // Area conversions
    println!("--- Area Conversions ---");
    let area = Area::from_acres(1.0);
    println!("1 acre:");
    println!("  {:.2} square meters", area.to_square_meters());
    println!("  {:.4} hectares", area.to_hectares());
    println!("  {:.2} square feet", area.to_square_feet());
    println!("  {:.6} square kilometers", area.to_square_kilometers());
    println!();

    // Volume conversions
    println!("--- Volume Conversions ---");
    let volume = Volume::from_us_gallons(5.0);
    println!("5 US gallons:");
    println!("  {:.2} liters", volume.to_liters());
    println!("  {:.0} milliliters", volume.to_milliliters());
    println!("  {:.2} imperial gallons", volume.to_imperial_gallons());
    println!("  {:.2} US quarts", volume.to_us_quarts());
    println!("  {:.2} US cups", volume.to_us_cups());
    println!();

    // Time conversions
    println!("--- Time Conversions ---");
    let time = Time::from_days(1.0);
    println!("1 day:");
    println!("  {:.0} hours", time.to_hours());
    println!("  {:.0} minutes", time.to_minutes());
    println!("  {:.0} seconds", time.to_seconds());
    println!("  {:.0} milliseconds", time.to_milliseconds());
    println!("  Human readable: {}", time.format_human());
    
    let speed_time = Speed::from_kilometers_per_hour(50.0).time_to_travel(100_000.0);
    println!("  Time to travel 100km at 50km/h: {}", Time::from_seconds(speed_time).format_human());
    println!();

    // Speed conversions
    println!("--- Speed Conversions ---");
    let speed = Speed::from_kilometers_per_hour(100.0);
    println!("100 km/h:");
    println!("  {:.2} m/s", speed.to_meters_per_second());
    println!("  {:.2} mph", speed.to_miles_per_hour());
    println!("  {:.2} knots", speed.to_knots());
    println!("  Mach {:.4}", speed.to_mach());
    println!("  Distance in 1 hour: {:.2} km", speed.distance_traveled(3600.0) / 1000.0);
    println!();

    // Data conversions
    println!("--- Data Conversions ---");
    let data = Data::from_gigabytes(4.7); // DVD capacity
    println!("4.7 GB (DVD capacity):");
    println!("  {} (binary)", data.format_human_binary());
    println!("  {} (decimal)", data.format_human_decimal());
    println!("  {:.2} Mb", data.to_megabits());
    
    let file_size = Data::from_mebibytes(10.0);
    println!("10 MiB file:");
    println!("  {} (decimal)", file_size.format_human_decimal());
    println!("  {:.0} bytes", file_size.to_bytes());
    println!();

    println!("=== Demo Complete ===");
}