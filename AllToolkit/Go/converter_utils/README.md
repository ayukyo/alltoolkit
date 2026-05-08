# converter_utils

Comprehensive unit conversion utilities for Go. Supports length, weight, temperature, time, data storage, volume, area, speed, pressure, angle, and fuel consumption conversions.

**Zero external dependencies** - uses only Go standard library.

## Features

- **Length**: Meter, Kilometer, Mile, Yard, Foot, Inch, Centimeter, Millimeter, Nautical Mile
- **Weight**: Kilogram, Gram, Milligram, Metric Ton, Pound, Ounce, Stone, Carat
- **Temperature**: Celsius, Fahrenheit, Kelvin
- **Time**: Nanosecond, Microsecond, Millisecond, Second, Minute, Hour, Day, Week, Month, Year
- **Data Storage**: Byte, KB, MB, GB, TB, PB (decimal) and KiB, MiB, GiB, TiB, PiB (binary)
- **Volume**: Liter, Milliliter, Gallon, Quart, Pint, Cup, Fluid Ounce, Tablespoon, Teaspoon
- **Area**: Square Meter, Square Kilometer, Hectare, Acre, Square Mile, Square Foot, Square Inch
- **Speed**: m/s, km/h, mph, ft/s, Knot, Mach
- **Pressure**: Pascal, kPa, MPa, Bar, Millibar, Atmosphere, PSI, Torr, mmHg
- **Angle**: Degrees ↔ Radians
- **Fuel Consumption**: L/100km, km/L, mpg(US), mpg(UK)

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/converter_utils
```

## Quick Start

### Basic Conversion

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/converter_utils"
)

func main() {
    // Convert 1 mile to kilometers
    miles := converter_utils.Length(1, converter_utils.Mile)
    fmt.Printf("1 mile = %.4f km\n", miles.Kilometers())
    
    // Convert 100°C to Fahrenheit
    temp := converter_utils.Temperature(100, converter_utils.Celsius)
    fmt.Printf("100°C = %.1f°F\n", temp.Fahrenheit())
    
    // Convert 1 GB to bytes
    data := converter_utils.Data(1, converter_utils.Gigabyte)
    fmt.Printf("1 GB = %.0f bytes\n", data.Bytes())
}
```

### Fluent API

```go
// Create a converter for a specific value
val := converter_utils.NewConverter(100)

// Use it for different conversions
fmt.Printf("100 m = %.2f km\n", val.AsLength(converter_utils.Meter).Kilometers())
fmt.Printf("100 kg = %.2f lb\n", val.AsWeight(converter_utils.Kilogram).Pounds())
fmt.Printf("100°C = %.1f°F\n", val.AsTemperature(converter_utils.Celsius).Fahrenheit())
```

### Parsing Strings

```go
// Parse unit strings
meters, _ := converter_utils.ParseLength("1.5 mi")
fmt.Printf("1.5 miles = %.2f meters\n", meters)

kg, _ := converter_utils.ParseWeight("100 lb")
fmt.Printf("100 lb = %.4f kg\n", kg)

celsius, _ := converter_utils.ParseTemperature("212 F")
fmt.Printf("212°F = %.2f°C\n", celsius)
```

### Smart Formatting

```go
// Smart data formatting (picks appropriate unit)
fmt.Println(converter_utils.SmartFormatData(1500000))  // "1.43 MB"
fmt.Println(converter_utils.SmartFormatData(1500000000))  // "1.40 GB"

// Smart duration formatting
fmt.Println(converter_utils.SmartFormatDuration(0.001))  // "1.00 ms"
fmt.Println(converter_utils.SmartFormatDuration(3600))  // "1.00 h"
fmt.Println(converter_utils.SmartFormatDuration(86400))  // "1.00 days"

// Number formatting with commas
fmt.Println(converter_utils.FormatWithCommas(1234567.89, 2))  // "1,234,567.88"
```

## API Reference

### Length

```go
// Direct conversion
result, err := converter_utils.ConvertLength(value, fromUnit, toUnit)

// Fluent converter
lc := converter_utils.Length(value, unit)
km := lc.Kilometers()
m := lc.Meters()
mi := lc.Miles()
ft := lc.Feet()
in := lc.Inches()
```

### Weight

```go
result, err := converter_utils.ConvertWeight(value, fromUnit, toUnit)

wc := converter_utils.Weight(value, unit)
kg := wc.Kilograms()
g := wc.Grams()
lb := wc.Pounds()
oz := wc.Ounces()
```

### Temperature

```go
result, err := converter_utils.ConvertTemperature(value, fromUnit, toUnit)

tc := converter_utils.Temperature(value, unit)
c := tc.Celsius()
f := tc.Fahrenheit()
k := tc.Kelvin()
```

### Time

```go
result, err := converter_utils.ConvertTime(value, fromUnit, toUnit)

tc := converter_utils.Duration(value, unit)
s := tc.Seconds()
min := tc.Minutes()
h := tc.Hours()
d := tc.Days()
```

### Data Storage

```go
result, err := converter_utils.ConvertData(value, fromUnit, toUnit)

dc := converter_utils.Data(value, unit)
b := dc.Bytes()
kb := dc.Kilobytes()
mb := dc.Megabytes()
gb := dc.Gigabytes()
```

### Volume

```go
result, err := converter_utils.ConvertVolume(value, fromUnit, toUnit)

vc := converter_utils.Volume(value, unit)
l := vc.Liters()
ml := vc.Milliliters()
gal := vc.Gallons()
```

### Area

```go
result, err := converter_utils.ConvertArea(value, fromUnit, toUnit)

ac := converter_utils.Area(value, unit)
sqm := ac.SquareMeters()
ha := ac.Hectares()
acres := ac.Acres()
```

### Speed

```go
result, err := converter_utils.ConvertSpeed(value, fromUnit, toUnit)

sc := converter_utils.Speed(value, unit)
ms := sc.MetersPerSecond()
kmh := sc.KilometersPerHour()
mph := sc.MilesPerHour()
kn := sc.Knots()
```

### Pressure

```go
result, err := converter_utils.ConvertPressure(value, fromUnit, toUnit)

pc := converter_utils.Pressure(value, unit)
pa := pc.Pascals()
bar := pc.Bars()
psi := pc.PSI()
atm := pc.Atmospheres()
```

### Angle

```go
// Direct conversion
rad := converter_utils.ConvertDegreesToRadians(degrees)
deg := converter_utils.ConvertRadiansToDegrees(radians)

// Fluent converter
ac := converter_utils.Angle(degrees)
rad := ac.Radians()
deg := ac.Degrees()

// From radians
ac := converter_utils.AngleFromRadians(radians)
```

### Fuel Consumption

```go
result, err := converter_utils.ConvertFuelConsumption(value, fromUnit, toUnit)
```

## Testing

```bash
go test -v
```

## Benchmarks

```bash
go test -bench=.
```

## License

MIT License