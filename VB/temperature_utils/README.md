# temperature_utils - Temperature Conversion and Calculation Library

A comprehensive VB.NET library for temperature conversion, thermal index calculations, and temperature-related utilities.

## Features

### Temperature Conversion
- Convert between Celsius, Fahrenheit, Kelvin, and Rankine
- Batch conversion support
- String parsing for temperature formats ("25°C", "77°F", "300K")
- Temperature struct with operator overloads

### Temperature Validation
- Check if temperature is above absolute zero
- Range validation
- Absolute zero constants for all units

### Temperature Categories
- Temperature classification (Freezing, Cold, Comfortable, Hot, etc.)
- Clothing recommendations based on temperature
- Activity recommendations
- Risk level assessment

### Thermal Indices
- **Heat Index**: Calculate "feels-like" temperature in hot weather
- **Wind Chill**: Calculate "feels-like" temperature in cold weather
- **Dew Point**: Temperature where air becomes saturated
- **Wet Bulb Temperature**: Important for heat stress assessment
- **Humidex**: Canadian heat index formula
- **WBGT**: Wet Bulb Globe Temperature for heat stress

### Temperature Statistics
- Calculate average, median, minimum, maximum
- Standard deviation
- Range calculation
- Count temperatures in specific range

### Lookup Tables
- Generate conversion tables
- Reference points (Freezing, Boiling, Body Temp, etc.)

## Usage Examples

### Basic Conversion

```vb
' Convert Celsius to Fahrenheit
Dim fahrenheit = TemperatureConverter.CelsiusToFahrenheit(25)
' Result: 77°F

' Convert using generic method
Dim kelvin = TemperatureConverter.Convert(100, TemperatureUnit.Celsius, TemperatureUnit.Kelvin)
' Result: 373.15K

' Batch conversion
Dim temps = {0.0, 20.0, 37.0, 100.0}
Dim converted = TemperatureConverter.ConvertBatch(temps, TemperatureUnit.Celsius, TemperatureUnit.Fahrenheit)
```

### Temperature Struct

```vb
' Create temperatures
Dim freezing = Temperature.FromCelsius(0)
Dim bodyTemp = Temperature.FromFahrenheit(98.6)
Dim roomTemp = Temperature.FromKelvin(293.15)

' Convert to other units
Console.WriteLine(freezing.FormatAll())  ' 0°C | 32°F | 273.2K | 491.7°R

' Arithmetic operations
Dim hot = Temperature.FromCelsius(10) + Temperature.FromCelsius(30)
' Result: 40°C

' Comparison (works across units!)
Dim t1 = Temperature.FromCelsius(20)
Dim t2 = Temperature.FromFahrenheit(68)  ' Same temperature
Console.WriteLine(t1 = t2)  ' True

' Built-in checks
Console.WriteLine(freezing.IsFreezing())      ' True
Console.WriteLine(bodyTemp.IsComfortable())   ' False
```

### Parsing

```vb
Dim temp = TemperatureConverter.Parse("25°C")
Console.WriteLine(temp.ToFahrenheit())  ' 77

' Safe parsing
Dim result As Temperature
If TemperatureConverter.TryParse("77°F", result) Then
    Console.WriteLine(result.ToCelsius())  ' 25
End If
```

### Heat Index

```vb
' Calculate heat index (hot weather "feels-like" temperature)
Dim heatIndex = ThermalIndices.CalculateHeatIndex(95, 80)
' 95°F at 80% humidity feels like ~126°F

' Using Celsius
Dim heatIndexC = ThermalIndices.CalculateHeatIndexCelsius(35, 70)
' 35°C at 70% humidity
```

### Wind Chill

```vb
' Calculate wind chill (cold weather "feels-like" temperature)
Dim windChill = ThermalIndices.CalculateWindChill(20, 15)
' 20°F with 15 mph wind feels like ~6°F

' Using Celsius and km/h
Dim windChillC = ThermalIndices.CalculateWindChillCelsius(0, 20)
' 0°C with 20 km/h wind
```

### Dew Point

```vb
' Calculate dew point
Dim dewPoint = ThermalIndices.CalculateDewPoint(25, 50)
' 25°C at 50% humidity → dew point ~14°C
```

### Temperature Categories

```vb
' Get category
Dim category = TemperatureCategories.GetCategory(22)  ' "Comfortable"

' Clothing recommendation
Dim clothing = TemperatureCategories.GetClothingRecommendation(-10)
' "Winter coat, hat, gloves, scarf"

' Activity recommendation
Dim activity = TemperatureCategories.GetActivityRecommendation(22)
' "Ideal for all outdoor activities"

' Risk level
Dim risk = TemperatureCategories.GetRiskLevel(-50)  ' "Extreme"
```

### Statistics

```vb
Dim temps = {
    Temperature.FromCelsius(15),
    Temperature.FromCelsius(20),
    Temperature.FromCelsius(25)
}

Console.WriteLine(TemperatureStatistics.Average(temps).Format())  ' 20°C
Console.WriteLine(TemperatureStatistics.Median(temps).Format())   ' 20°C
Console.WriteLine(TemperatureStatistics.Maximum(temps).Format())  ' 25°C
```

## Files

- `temperature_utils.vb` - Main library implementation
- `temperature_utils_tests.vb` - Unit tests (100+ tests)
- `examples.vb` - Complete usage examples
- `README.md` - This documentation

## Supported Temperature Units

| Unit      | Symbol | Absolute Zero |
|-----------|--------|---------------|
| Celsius   | °C     | -273.15       |
| Fahrenheit| °F     | -459.67       |
| Kelvin    | K      | 0             |
| Rankine   | °R     | 0             |

## Thermal Index Formulas

- **Heat Index**: Rothfusz regression equation (NWS)
- **Wind Chill**: NWS Wind Chill Formula (2001)
- **Dew Point**: Magnus formula approximation
- **Humidex**: Canadian Meteorological Service formula
- **WBGT**: Simplified wet bulb globe temperature

## Applications

- Weather applications
- HVAC systems
- Cooking and food safety
- Industrial processes
- Scientific calculations
- Health and safety monitoring
- Sports and outdoor activities

## Notes

- Zero external dependencies
- Pure VB.NET implementation
- All formulas use standard meteorological equations
- Temperature struct supports operator overloads (+, -, *, /, comparisons)
- Valid temperature range enforcement (above absolute zero)