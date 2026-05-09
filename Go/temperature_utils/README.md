# Temperature Utils (Go)

A comprehensive temperature conversion utility library for Go with zero external dependencies. Supports 8 temperature scales and provides useful utilities for temperature calculations.

## Features

- **8 Temperature Scales**: Celsius, Fahrenheit, Kelvin, Rankine, Delisle, Newton, Réaumur, and Rømer
- **Type-Safe**: Strong typing with `Temperature` struct and `TemperatureUnit` type
- **Conversion Functions**: Convert between any two temperature scales
- **Utility Functions**: Wind chill, heat index, average, min, max, delta calculations
- **Temperature Ranges**: Built-in ranges for common scenarios
- **Zero Dependencies**: Uses only Go standard library

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/temperature_utils
```

## Quick Start

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/temperature_utils"
)

func main() {
    // Basic conversions
    celsius := 25.0
    fahrenheit := temperature_utils.CelsiusTo(celsius, temperature_utils.Fahrenheit)
    kelvin := temperature_utils.CelsiusTo(celsius, temperature_utils.Kelvin)
    
    fmt.Printf("%.1f°C = %.1f°F = %.2f K\n", celsius, fahrenheit, kelvin)
    
    // Using Temperature type
    temp := temperature_utils.NewTemperature(100, temperature_utils.Celsius)
    fmt.Println(temp.String()) // "100.00° Celsius"
    
    // Convert to different unit
    fahrenheitTemp := temp.ConvertTo(temperature_utils.Fahrenheit)
    fmt.Printf("100°C = %s\n", fahrenheitTemp.String())
    
    // Check if valid (above absolute zero)
    fmt.Printf("Is valid: %v\n", temp.IsValid())
    
    // Compare temperatures
    other := temperature_utils.NewTemperature(32, temperature_utils.Fahrenheit)
    fmt.Printf("100°C equals 32°F: %v\n", temp.Equals(other, 0.01))
}
```

## Supported Temperature Scales

| Scale | Unit | Freezing Point | Boiling Point |
|-------|------|----------------|---------------|
| Celsius | °C | 0 | 100 |
| Fahrenheit | °F | 32 | 212 |
| Kelvin | K | 273.15 | 373.15 |
| Rankine | °R | 491.67 | 671.64 |
| Delisle | °De | 150 | 0 |
| Newton | °N | 0 | 33 |
| Réaumur | °Ré | 0 | 80 |
| Rømer | °Rø | 7.5 | 60 |

## API Reference

### Conversion Functions

```go
// Convert between scales using specific functions
CelsiusTo(celsius float64, to TemperatureUnit) float64
FahrenheitTo(fahrenheit float64, to TemperatureUnit) float64
KelvinTo(kelvin float64, to TemperatureUnit) float64
RankineTo(rankine float64, to TemperatureUnit) float64
DelisleTo(delisle float64, to TemperatureUnit) float64
NewtonTo(newton float64, to TemperatureUnit) float64
ReaumurTo(reaumur float64, to TemperatureUnit) float64
RomerTo(romer float64, to TemperatureUnit) float64

// Generic conversion function
Convert(value float64, from, to TemperatureUnit) float64
```

### Temperature Type

```go
// Create a temperature
temp := NewTemperature(25.0, Celsius)

// Convert to different unit
fahrenheit := temp.ConvertTo(Fahrenheit)

// Check validity
isValid := temp.IsValid()      // Above absolute zero?
isAbove := temp.IsAboveAbsoluteZero()

// Comparisons
temp.Equals(other, 0.01)       // Equal within tolerance
temp.LessThan(other)           // Less than comparison
temp.GreaterThan(other)        // Greater than comparison

// String representation
str := temp.String()           // "25.00° Celsius"
```

### Temperature Range

```go
// Create a temperature range
range := NewRange(0, 100, Celsius)

// Check if temperature is within range
contains := range.Contains(temp)

// String representation
str := range.String()          // "0.00° Celsius to 100.00° Celsius"
```

### Utility Functions

```go
// Wind chill (temperature in Celsius, wind speed in km/h)
// Only valid for temp <= 10°C and wind > 4.8 km/h
windChill := WindChill(0, 15)  // Apparent temperature

// Heat index (temperature in Celsius, humidity 0-100%)
// Only valid for temp >= 27°C
heatIndex := HeatIndex(30, 50) // Apparent temperature

// Average of multiple temperatures
avg := Average(temp1, temp2, temp3)

// Min/Max from slice
min := Min(temp1, temp2, temp3)
max := Max(temp1, temp2, temp3)

// Delta between two temperatures
delta := Delta(temp1, temp2)
```

### Parsing and Formatting

```go
// Parse unit from string
unit, err := ParseUnit("C")       // Celsius
unit, err := ParseUnit("Fahrenheit") // Fahrenheit
unit, err := ParseUnit("K")       // Kelvin

// Format with standard symbol
formatted := FormatWithSymbol(25.5, Celsius) // "25.50°C"
```

### Pre-defined Constants

```go
// Temperature constants (in Celsius and Fahrenheit)
AbsoluteZeroC     = -273.15
AbsoluteZeroF     = -459.67
WaterFreezingC    = 0.0
WaterFreezingF    = 32.0
WaterBoilingC     = 100.0
WaterBoilingF     = 212.0
HumanBodyTempC    = 37.0
HumanBodyTempF    = 98.6
RoomTemperatureC  = 20.0
RoomTemperatureF  = 68.0

// Common temperature ranges
CommonRanges.AbsoluteZeroToWaterFreezing  // -273.15°C to 0°C
CommonRanges.WaterFreezingToBoiling       // 0°C to 100°C
CommonRanges.HumanComfortRange            // 18°C to 24°C
CommonRanges.ColdWeatherRange             // -20°C to 0°C
CommonRanges.HotWeatherRange              // 30°C to 45°C
```

## Examples

### Weather Application

```go
package main

import (
    "fmt"
    "temperature_utils"
)

func main() {
    // Convert weather data from different sources
    celsiusReport := NewTemperature(22, Celsius)
    fahrenheitReport := NewTemperature(75, Fahrenheit)
    
    // Normalize to Celsius for comparison
    fInCelsius := fahrenheitReport.ConvertTo(Celsius)
    fmt.Printf("Report 1: %s\n", celsiusReport)
    fmt.Printf("Report 2: %s (converted to Celsius: %.1f°C)\n", 
        fahrenheitReport, fInCelsius.Value)
    
    // Calculate average temperature
    avg := Average(celsiusReport, fahrenheitReport)
    fmt.Printf("Average: %s\n", avg.String())
    
    // Check if comfortable
    if CommonRanges.HumanComfortRange.Contains(avg) {
        fmt.Println("Temperature is comfortable for humans!")
    }
    
    // Calculate wind chill
    windChill := WindChill(5, 20) // 5°C with 20 km/h wind
    fmt.Printf("Wind chill: %.1f°C\n", windChill)
    
    // Calculate heat index
    heatIndex := HeatIndex(32, 60) // 32°C with 60% humidity
    fmt.Printf("Heat index: %.1f°C\n", heatIndex)
}
```

### Scientific Computing

```go
package main

import (
    "fmt"
    "temperature_utils"
)

func main() {
    // Temperature in Kelvin (standard scientific unit)
    roomTemp := NewTemperature(293.15, Kelvin) // ~20°C
    
    // Check absolute zero constraint
    sampleTemp := NewTemperature(4.2, Kelvin) // Liquid helium
    fmt.Printf("Sample temperature: %s\n", sampleTemp.String())
    fmt.Printf("Is above absolute zero: %v\n", sampleTemp.IsAboveAbsoluteZero())
    
    // Compare temperatures across different scales
    freezing := NewTemperature(273.15, Kelvin)
    boiling := NewTemperature(373.15, Kelvin)
    
    fmt.Printf("Delta: %s\n", Delta(freezing, boiling).String())
    
    // Temperature range validation
    labRange := NewRange(273, 373, Kelvin) // 0°C to 100°C
    experiment := NewTemperature(350, Kelvin)
    
    if labRange.Contains(experiment) {
        fmt.Println("Experiment temperature within acceptable range")
    }
}
```

## Testing

Run the test suite:

```bash
go test -v
```

Run benchmarks:

```bash
go test -bench=.
```

## License

MIT License