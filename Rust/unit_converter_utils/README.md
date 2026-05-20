# Unit Converter Utilities

A comprehensive, zero-dependency unit conversion library for Rust.

## Features

Supports **9 measurement categories** with **50+ unit types**:

### Length
- Meters, Kilometers, Miles, Feet, Inches, Yards, Centimeters, Millimeters

### Weight/Mass
- Kilograms, Grams, Pounds, Ounces, Metric Tons, Imperial Tons, Milligrams

### Temperature
- Celsius, Fahrenheit, Kelvin (with absolute zero validation)

### Area
- Square Meters, Square Kilometers, Hectares, Acres, Square Feet, Square Yards, Square Miles, Square Inches

### Volume
- Liters, Milliliters, US Gallons, UK Gallons, Quarts, Pints, Cups, Fluid Ounces, Cubic Meters, Cubic Centimeters

### Data Storage
- Bytes, KB, MB, GB, TB, PB (decimal)
- KiB, MiB, GiB, TiB, PiB (binary)
- Bits, Kb, Mb, Gb

### Time
- Seconds, Minutes, Hours, Days, Weeks, Months, Years, Milliseconds, Microseconds, Nanoseconds

### Speed
- m/s, km/h, mph, Knots, ft/s, Mach

### Pressure
- Pascals, Kilopascals, Bar, PSI, Atmospheres, mmHg, inHg

## Usage

### Basic Conversion

```rust
use unit_converter_utils::{convert_length, LengthUnit};

// Convert 1000 meters to kilometers
let km = convert_length(1000.0, LengthUnit::Meters, LengthUnit::Kilometers).unwrap();
println!("1000 m = {} km", km); // 1000 m = 1 km

// Convert 1 mile to kilometers
let km = convert_length(1.0, LengthUnit::Miles, LengthUnit::Kilometers).unwrap();
println!("1 mile = {} km", km); // 1 mile = 1.609344 km
```

### Temperature Conversion

```rust
use unit_converter_utils::{convert_temperature, TemperatureUnit, celsius_to_fahrenheit};

// Using the general function
let f = convert_temperature(0.0, TemperatureUnit::Celsius, TemperatureUnit::Fahrenheit).unwrap();
println!("0°C = {}°F", f); // 0°C = 32°F

// Using convenience functions
let f = celsius_to_fahrenheit(100.0).unwrap();
println!("100°C = {}°F", f); // 100°C = 212°F

// Absolute zero validation
let result = convert_temperature(-274.0, TemperatureUnit::Celsius, TemperatureUnit::Kelvin);
assert!(result.is_err()); // Error: BelowAbsoluteZero
```

### Data Storage Conversion

```rust
use unit_converter_utils::{convert_data, DataUnit};

// Decimal (1000-based)
let mb = convert_data(1.0, DataUnit::Gigabytes, DataUnit::Megabytes).unwrap();
println!("1 GB = {} MB", mb); // 1 GB = 1000 MB

// Binary (1024-based)
let mib = convert_data(1024.0, DataUnit::Bytes, DataUnit::Kibibytes).unwrap();
println!("1024 B = {} KiB", mib); // 1024 B = 1 KiB

// Bits to bytes
let mb = convert_data(8.0, DataUnit::Megabits, DataUnit::Megabytes).unwrap();
println!("8 Mb = {} MB", mb); // 8 Mb = 1 MB
```

### Speed Conversion

```rust
use unit_converter_utils::{convert_speed, SpeedUnit};

let kmh = convert_speed(1.0, SpeedUnit::MetersPerSecond, SpeedUnit::KilometersPerHour).unwrap();
println!("1 m/s = {} km/h", kmh); // 1 m/s = 3.6 km/h

let mach = convert_speed(340.29, SpeedUnit::MetersPerSecond, SpeedUnit::Mach).unwrap();
println!("340.29 m/s = Mach {}", mach); // 340.29 m/s = Mach 1.0
```

### Pressure Conversion

```rust
use unit_converter_utils::{convert_pressure, PressureUnit};

let psi = convert_pressure(1.0, PressureUnit::Bar, PressureUnit::Psi).unwrap();
println!("1 bar = {} psi", psi); // 1 bar = 14.5038 psi

let atm = convert_pressure(101325.0, PressureUnit::Pascals, PressureUnit::Atmospheres).unwrap();
println!("101325 Pa = {} atm", atm); // 101325 Pa = 1 atm
```

## Error Handling

```rust
use unit_converter_utils::{convert_length, LengthUnit, ConversionError};

// Invalid values (NaN, Infinity)
let result = convert_length(f64::NAN, LengthUnit::Meters, LengthUnit::Kilometers);
match result {
    Err(ConversionError::InvalidValue(msg)) => println!("Error: {}", msg),
    Err(ConversionError::BelowAbsoluteZero) => println!("Temperature below absolute zero"),
    _ => {}
}
```

## Convenience Functions

```rust
use unit_converter_utils::{
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    miles_to_km,
    km_to_miles,
    lbs_to_kg,
    kg_to_lbs,
};

let f = celsius_to_fahrenheit(25.0).unwrap();
let c = fahrenheit_to_celsius(77.0).unwrap();
let km = miles_to_km(1.0).unwrap();
let mi = km_to_miles(1.0).unwrap();
let kg = lbs_to_kg(1.0).unwrap();
let lb = kg_to_lbs(1.0).unwrap();
```

## Unit Abbreviations

All units provide their standard abbreviations:

```rust
use unit_converter_utils::{LengthUnit, WeightUnit, TemperatureUnit};

assert_eq!(LengthUnit::Kilometers.abbreviation(), "km");
assert_eq!(WeightUnit::Pounds.abbreviation(), "lb");
assert_eq!(TemperatureUnit::Celsius.abbreviation(), "°C");
```

## API Reference

### Conversion Functions

| Function | Description |
|----------|-------------|
| `convert_length(value, from, to)` | Length conversion |
| `convert_weight(value, from, to)` | Weight/mass conversion |
| `convert_temperature(value, from, to)` | Temperature conversion |
| `convert_area(value, from, to)` | Area conversion |
| `convert_volume(value, from, to)` | Volume conversion |
| `convert_data(value, from, to)` | Data storage conversion |
| `convert_time(value, from, to)` | Time conversion |
| `convert_speed(value, from, to)` | Speed conversion |
| `convert_pressure(value, from, to)` | Pressure conversion |

### Types

- `LengthUnit` - Length measurement units
- `WeightUnit` - Weight/mass measurement units
- `TemperatureUnit` - Temperature measurement units
- `AreaUnit` - Area measurement units
- `VolumeUnit` - Volume measurement units
- `DataUnit` - Data storage units
- `TimeUnit` - Time measurement units
- `SpeedUnit` - Speed measurement units
- `PressureUnit` - Pressure measurement units
- `ConversionError` - Error types for invalid conversions
- `UnitValue` - Generic unit value wrapper

## Testing

Run tests with:

```bash
cargo test
```

The module includes comprehensive test coverage with 40+ unit tests covering:
- All unit type conversions
- Round-trip conversions
- Error handling (NaN, Infinity, absolute zero)
- Unit abbreviations
- Convenience functions

## License

MIT License - Part of AllToolkit

## Author

AllToolkit