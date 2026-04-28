# Unit Converter

A comprehensive, zero-dependency unit conversion library for Rust.

## Features

This library provides conversions for:

- **Length**: meters, kilometers, miles, feet, inches, yards, nautical miles, light years, astronomical units, etc.
- **Weight/Mass**: kilograms, grams, pounds, ounces, stones, tons, carats, etc.
- **Temperature**: Celsius, Fahrenheit, Kelvin, Rankine, Delisle, Newton, Réaumur, Rømer
- **Area**: square meters, hectares, acres, square feet, square miles, etc.
- **Volume**: liters, gallons, quarts, pints, cups, fluid ounces, cubic meters, etc.
- **Time**: seconds, minutes, hours, days, weeks, months, years, milliseconds, microseconds, nanoseconds
- **Speed**: m/s, km/h, mph, knots, mach, feet per second, etc.
- **Data**: bytes, kilobytes, megabytes, gigabytes, kibibytes, mebibytes, etc.

## Key Features

- **Zero external dependencies** - Uses only Rust standard library
- **Comprehensive coverage** - Supports both metric and imperial units
- **Type-safe conversions** - Each unit type has its own struct
- **Precision handling** - Built-in rounding utilities
- **Human-readable formatting** - Automatic unit selection for display

## Usage

### Basic Conversion

```rust
use unit_converter::{Length, Weight, Temperature};

// Length conversion
let length = Length::from_miles(1.0);
println!("1 mile = {:.2} kilometers", length.to_kilometers());
println!("1 mile = {:.0} meters", length.to_meters());

// Weight conversion
let weight = Weight::from_pounds(150.0);
println!("150 lbs = {:.2} kg", weight.to_kilograms());

// Temperature conversion
let temp = Temperature::from_fahrenheit(98.6);
println!("98.6°F = {:.1}°C", temp.to_celsius());
```

### Human-Readable Formatting

```rust
use unit_converter::{Time, Data};

// Time formatting
let time = Time::from_seconds(3661.0);
println!("Human readable: {}", time.format_human()); // "1h 1m"

// Data formatting
let data = Data::from_megabytes(1024.0);
println!("Binary: {}", data.format_human_binary()); // "1.00 GiB"
println!("Decimal: {}", data.format_human_decimal()); // "1.02 GB"
```

### Utility Functions

```rust
use unit_converter::{Speed, Length};

// Calculate travel time
let speed = Speed::from_kilometers_per_hour(60.0);
let distance = 100_000.0; // 100 km in meters
let time = speed.time_to_travel(distance);
println!("Travel time: {:.0} seconds", time);

// Calculate distance
let distance = speed.distance_traveled(3600.0); // 1 hour
println!("Distance: {:.0} meters", distance);
```

## Unit Types

### Length Units

| Method | Unit |
|--------|------|
| `from_meters` | meters (m) |
| `from_kilometers` | kilometers (km) |
| `from_centimeters` | centimeters (cm) |
| `from_millimeters` | millimeters (mm) |
| `from_miles` | miles (mi) |
| `from_feet` | feet (ft) |
| `from_inches` | inches (in) |
| `from_yards` | yards (yd) |
| `from_nautical_miles` | nautical miles (nmi) |
| `from_light_years` | light years (ly) |
| `from_astronomical_units` | astronomical units (AU) |

### Weight Units

| Method | Unit |
|--------|------|
| `from_kilograms` | kilograms (kg) |
| `from_grams` | grams (g) |
| `from_milligrams` | milligrams (mg) |
| `from_pounds` | pounds (lb) |
| `from_ounces` | ounces (oz) |
| `from_stones` | stones (st) |
| `from_metric_tonnes` | metric tonnes (t) |
| `from_carats` | carats (ct) |

### Temperature Units

| Method | Unit |
|--------|------|
| `from_celsius` | Celsius (°C) |
| `from_fahrenheit` | Fahrenheit (°F) |
| `from_kelvin` | Kelvin (K) |
| `from_rankine` | Rankine (°R) |
| `from_newton` | Newton (°N) |
| `from_reaumur` | Réaumur (°Ré) |

### Data Units

The library supports both binary (1024-based) and decimal (1000-based) prefixes:

| Binary Method | Unit | Decimal Method | Unit |
|---------------|------|----------------|------|
| `from_kibibytes` | KiB | `from_kilobytes` | KB |
| `from_mebibytes` | MiB | `from_megabytes` | MB |
| `from_gibibytes` | GiB | `from_gigabytes` | GB |
| `from_tebibytes` | TiB | `from_terabytes` | TB |

## Running Tests

```bash
cargo test
```

## Running Examples

```bash
cargo run --example demo
```

## License

MIT License - Feel free to use in any project.

## Contributing

Contributions are welcome! Feel free to add more unit types or improve existing functionality.