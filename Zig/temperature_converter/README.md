# Temperature Converter - Zig

A comprehensive temperature conversion utility for Zig, supporting Celsius, Fahrenheit, and Kelvin with validation, classification, and advanced features.

## Features

### Core Conversion
- Celsius ↔ Fahrenheit ↔ Kelvin conversions
- Single function for any unit to any unit conversion
- Safe conversion with absolute zero validation
- NaN/Infinity input detection

### Temperature Parsing
- Parse temperature strings like "25°C", "77°F", "300K"
- Case-insensitive unit parsing
- Support for degree symbol and unit abbreviations

### Temperature Range
- Define temperature ranges with min/max values
- Convert ranges to different units
- Check if a temperature falls within a range
- Calculate midpoint and size

### Temperature Classification
- Human comfort-based classification system
- 8 categories: Freezing, Cold, Cool, Comfortable, Warm, Hot, VeryHot, ExtremeHeat
- Descriptive messages for each category

### Advanced Features
- Wind chill calculation (Fahrenheit and Celsius)
- Heat index calculation (Fahrenheit and Celsius)
- Temperature arithmetic (add, subtract, average)
- Multiple temperature conversion (convertAll)
- Temperature comparison and equality checking
- String formatting with precision control

### Constants
- Absolute zero values for all units
- Water freezing/boiling points
- Human body temperature
- Room temperature

## Installation

Add to your `build.zig.zon`:

```zig
.dependencies = .{
    .temperature_converter = .{
        .path = "path/to/temperature_converter",
    },
},
```

Then in your `build.zig`:

```zig
const temp_conv = b.dependency("temperature_converter", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.addImport("temperature_converter", temp_conv.module("temperature_converter"));
```

## Usage

### Basic Conversion

```zig
const std = @import("std");
const temp_conv = @import("temperature_converter");

pub fn main() !void {
    // Direct conversion functions
    const fahrenheit = temp_conv.celsiusToFahrenheit(25.0);  // 77°F
    const kelvin = temp_conv.celsiusToKelvin(25.0);           // 298.15 K

    // Universal convert function
    const temp = temp_conv.convert(100.0, .Celsius, .Fahrenheit);  // 212°F
}
```

### Safe Conversion with Validation

```zig
const result = temp_conv.convertSafe(-300.0, .Celsius, .Fahrenheit);
if (result) |temp| {
    std.debug.print("Converted: {d}\n", .{temp});
} else |err| {
    switch (err) {
        .AbsoluteZeroViolation => std.debug.print("Below absolute zero!\n", .{}),
        .InvalidTemperature => std.debug.print("Invalid temperature value\n", .{}),
        else => {},
    }
}
```

### Parsing Temperatures

```zig
const parsed = temp_conv.parseTemperature("25°C").?;
std.debug.print("Value: {d}, Unit: {s}\n", .{
    parsed.value,
    parsed.unit.name(),
});
```

### Temperature Classification

```zig
const category = temp_conv.classifyCelsius(35.0);
std.debug.print("Category: {s}\n", .{category.description()});
// Output: "Hot, stay hydrated"
```

### Wind Chill and Heat Index

```zig
// Wind chill (Fahrenheit, valid for temp <= 50°F and wind >= 3 mph)
const wc = temp_conv.windChillFahrenheit(30.0, 15.0);
if (wc) |value| {
    std.debug.print("Wind chill: {d}°F\n", .{value});
}

// Heat index (Fahrenheit, valid for temp >= 80°F and humidity >= 40%)
const hi = temp_conv.heatIndexFahrenheit(90.0, 70.0);
if (hi) |value| {
    std.debug.print("Heat index: {d}°F\n", .{value});
}
```

### Temperature Range

```zig
const range = temp_conv.TemperatureRange.init(18.0, 26.0, .Celsius);

if (range.contains(22.0)) {
    std.debug.print("Comfortable temperature!\n", .{}); // true
}

const f_range = range.toUnit(.Fahrenheit);
// f_range.min ≈ 64.4°F, f_range.max ≈ 78.8°F
```

### Temperature Arithmetic

```zig
const avg = temp_conv.average(&[_]f64{20.0, 22.0, 24.0}, .Celsius);
std.debug.print("Average: {d}°C\n", .{avg});

const sum = temp_conv.add(10.0, .Celsius, 5.0, .Celsius);
std.debug.print("Sum: {d}°C\n", .{sum});
```

### Comparison

```zig
// Compare two temperatures (returns -1, 0, or 1)
const cmp = temp_conv.compare(0.0, .Celsius, 32.0, .Fahrenheit);  // 0 (equal)

// Check equality with tolerance
const equal = temp_conv.equal(0.0, .Celsius, 32.0, .Fahrenheit, 0.01);  // true
```

## API Reference

### Units

```zig
pub const TemperatureUnit = enum {
    Celsius,
    Fahrenheit,
    Kelvin,
    
    pub fn symbol(self: TemperatureUnit) []const u8;  // "°C", "°F", "K"
    pub fn name(self: TemperatureUnit) []const u8;   // "Celsius", "Fahrenheit", "Kelvin"
    pub fn parse(str: []const u8) ?TemperatureUnit;  // Parse from string
};
```

### Conversion Functions

```zig
pub fn celsiusToFahrenheit(celsius: f64) f64;
pub fn celsiusToKelvin(celsius: f64) f64;
pub fn fahrenheitToCelsius(fahrenheit: f64) f64;
pub fn fahrenheitToKelvin(fahrenheit: f64) f64;
pub fn kelvinToCelsius(kelvin: f64) f64;
pub fn kelvinToFahrenheit(kelvin: f64) f64;
pub fn convert(value: f64, from: TemperatureUnit, to: TemperatureUnit) f64;
pub fn convertSafe(value: f64, from: TemperatureUnit, to: TemperatureUnit) TemperatureError!f64;
```

### Classification

```zig
pub fn classifyCelsius(celsius: f64) TemperatureCategory;
pub fn classifyFahrenheit(fahrenheit: f64) TemperatureCategory;
pub fn classifyKelvin(kelvin: f64) TemperatureCategory;
```

### Parsing & Formatting

```zig
pub fn parseTemperature(str: []const u8) ?struct { value: f64, unit: TemperatureUnit };
pub fn formatTemperature(allocator: Allocator, value: f64, unit: TemperatureUnit, precision: usize) ![]u8;
```

### Arithmetic

```zig
pub fn add(temp1: f64, unit1: TemperatureUnit, temp2: f64, unit2: TemperatureUnit) f64;
pub fn subtract(temp1: f64, unit1: TemperatureUnit, temp2: f64, unit2: TemperatureUnit) f64;
pub fn average(temps: []const f64, unit: TemperatureUnit) f64;
pub fn convertAll(allocator: Allocator, temps: []const f64, from: TemperatureUnit, to: TemperatureUnit) ![]f64;
```

### Wind Chill & Heat Index

```zig
pub fn windChillCelsius(temp_celsius: f64, wind_speed_kmh: f64) ?f64;
pub fn windChillFahrenheit(temp_fahrenheit: f64, wind_speed_mph: f64) ?f64;
pub fn heatIndexCelsius(temp_celsius: f64, relative_humidity: f64) ?f64;
pub fn heatIndexFahrenheit(temp_fahrenheit: f64, relative_humidity: f64) ?f64;
```

### Constants

```zig
pub const temperatures = struct {
    pub const absolute_zero_celsius: f64;       // -273.15
    pub const absolute_zero_fahrenheit: f64;    // -459.67
    pub const absolute_zero_kelvin: f64;        // 0.0
    pub const water_freezing_celsius: f64;      // 0.0
    pub const water_freezing_fahrenheit: f64;   // 32.0
    pub const water_freezing_kelvin: f64;       // 273.15
    pub const water_boiling_celsius: f64;       // 100.0
    pub const water_boiling_fahrenheit: f64;    // 212.0
    pub const water_boiling_kelvin: f64;        // 373.15
    pub const human_body_celsius: f64;          // 37.0
    pub const human_body_fahrenheit: f64;       // 98.6
    pub const human_body_kelvin: f64;           // 310.15
    pub const room_temp_celsius: f64;           // 20.0
    pub const room_temp_fahrenheit: f64;        // 68.0
    pub const room_temp_kelvin: f64;            // 293.15
};
```

## Running Tests

```bash
zig build test
```

## Running Examples

```bash
zig build example
```

## License

MIT License - Part of the AllToolkit project.