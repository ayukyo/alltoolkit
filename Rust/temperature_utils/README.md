# Temperature Utils (Rust)

A comprehensive temperature conversion utility library with zero external dependencies.

## Features

- **8 Temperature Scales**: Celsius, Fahrenheit, Kelvin, Rankine, Delisle, Newton, Réaumur, and Rømer
- **Conversion**: Convert between any two scales or convert to all scales at once
- **Parsing**: Parse temperature strings like "25°C" or "77F"
- **Arithmetic**: Add, subtract, scale, and average temperatures
- **Comparison**: Compare temperatures across different units
- **Weather Calculations**: Wind chill, heat index, and dew point
- **Comfort Assessment**: Comfort level and state of matter
- **Descriptions**: Human-readable temperature descriptions

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
temperature_utils = { path = "../temperature_utils" }
```

## Usage

### Basic Conversions

```rust
use temperature_utils::{TemperatureUtils, TemperatureUnit};

let utils = TemperatureUtils::new();

// Convert Celsius to Fahrenheit
let f = utils.celsius_to_fahrenheit(25.0);
println!("25°C = {}°F", f);

// Convert between any units
let k = utils.convert(100.0, TemperatureUnit::Celsius, TemperatureUnit::Kelvin);
println!("100°C = {}K", k);
```

### Temperature Struct

```rust
use temperature_utils::Temperature;

let temp = Temperature::from_celsius(25.0);
println!("{}", temp); // 25.00°C

// Parse from string
let parsed: Temperature = "77°F".parse().unwrap();
println!("{}", parsed); // 77.00°F
```

### Convert to All Units

```rust
let all_temps = utils.convert_all(0.0, TemperatureUnit::Celsius);
for (unit, value) in all_temps {
    println!("{}: {:.2}{}", unit.name(), value, unit.symbol());
}
```

### Arithmetic Operations

```rust
let t1 = Temperature::from_celsius(20.0);
let t2 = Temperature::from_celsius(10.0);

let sum = utils.add(t1, t2);    // 30°C
let diff = utils.subtract(t1, t2); // 10°C
```

### Weather Calculations

```rust
// Wind chill: -5°C with 15 km/h wind
let chill = utils.wind_chill(-5.0, 15.0);

// Heat index: 32°C with 70% humidity
let hi = utils.heat_index(32.0, 70.0);

// Dew point: 25°C with 60% humidity
let dp = utils.dew_point(25.0, 60.0);
```

### Comfort Assessment

```rust
let temp = Temperature::from_celsius(22.0);
println!("Comfort: {}", utils.comfort_level(temp));
println!("State: {}", utils.state_of_matter(temp));
println!("Description: {}", utils.describe(temp));
```

## Supported Units

| Unit      | Symbol | Freezing | Boiling | Absolute Zero |
|-----------|--------|----------|---------|---------------|
| Celsius   | °C     | 0        | 100     | -273.15       |
| Fahrenheit| °F     | 32       | 212     | -459.67       |
| Kelvin    | K      | 273.15   | 373.15  | 0             |
| Rankine   | °R     | 491.67   | 671.64  | 0             |
| Delisle   | °De    | 150      | 0       | 559.73        |
| Newton    | °N     | 0        | 33      | -90.14        |
| Réaumur   | °Ré    | 0        | 80      | -218.52       |
| Rømer     | °Rø    | 7.5      | 60      | -135.90       |

## License

MIT License - Created by AllToolkit