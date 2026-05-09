// Package temperature_utils provides temperature conversion utilities.
// Supports Celsius, Fahrenheit, Kelvin, Rankine, Delisle, Newton, Réaumur, and Rømer scales.
package temperature_utils

import (
	"fmt"
	"math"
)

// TemperatureUnit represents a temperature scale
type TemperatureUnit string

const (
	Celsius    TemperatureUnit = "Celsius"
	Fahrenheit TemperatureUnit = "Fahrenheit"
	Kelvin     TemperatureUnit = "Kelvin"
	Rankine    TemperatureUnit = "Rankine"
	Delisle    TemperatureUnit = "Delisle"
	Newton     TemperatureUnit = "Newton"
	Reaumur    TemperatureUnit = "Réaumur"
	Romer      TemperatureUnit = "Rømer"
)

// Common temperature constants in Celsius
const (
	AbsoluteZeroC     = -273.15
	AbsoluteZeroF     = -459.67
	AbsoluteZeroK     = 0.0
	WaterFreezingC    = 0.0
	WaterFreezingF    = 32.0
	WaterBoilingC     = 100.0
	WaterBoilingF     = 212.0
	HumanBodyTempC    = 37.0
	HumanBodyTempF    = 98.6
	RoomTemperatureC  = 20.0
	RoomTemperatureF  = 68.0
)

// Temperature represents a temperature value with its unit
type Temperature struct {
	Value float64
	Unit  TemperatureUnit
}

// NewTemperature creates a new Temperature instance
func NewTemperature(value float64, unit TemperatureUnit) Temperature {
	return Temperature{Value: value, Unit: unit}
}

// CelsiusTo converts Celsius to the specified unit
func CelsiusTo(celsius float64, to TemperatureUnit) float64 {
	switch to {
	case Celsius:
		return celsius
	case Fahrenheit:
		return celsius*9/5 + 32
	case Kelvin:
		return celsius + 273.15
	case Rankine:
		return (celsius + 273.15) * 9 / 5
	case Delisle:
		return (100 - celsius) * 3 / 2
	case Newton:
		return celsius * 33 / 100
	case Reaumur:
		return celsius * 4 / 5
	case Romer:
		return celsius * 21/40 + 7.5
	default:
		return celsius
	}
}

// FahrenheitTo converts Fahrenheit to the specified unit
func FahrenheitTo(fahrenheit float64, to TemperatureUnit) float64 {
	celsius := (fahrenheit - 32) * 5 / 9
	return CelsiusTo(celsius, to)
}

// KelvinTo converts Kelvin to the specified unit
func KelvinTo(kelvin float64, to TemperatureUnit) float64 {
	celsius := kelvin - 273.15
	return CelsiusTo(celsius, to)
}

// RankineTo converts Rankine to the specified unit
func RankineTo(rankine float64, to TemperatureUnit) float64 {
	fahrenheit := rankine - 459.67
	return FahrenheitTo(fahrenheit, to)
}

// DelisleTo converts Delisle to the specified unit
func DelisleTo(delisle float64, to TemperatureUnit) float64 {
	celsius := 100 - delisle*2/3
	return CelsiusTo(celsius, to)
}

// NewtonTo converts Newton to the specified unit
func NewtonTo(newton float64, to TemperatureUnit) float64 {
	celsius := newton * 100 / 33
	return CelsiusTo(celsius, to)
}

// ReaumurTo converts Réaumur to the specified unit
func ReaumurTo(reaumur float64, to TemperatureUnit) float64 {
	celsius := reaumur * 5 / 4
	return CelsiusTo(celsius, to)
}

// RomerTo converts Rømer to the specified unit
func RomerTo(romer float64, to TemperatureUnit) float64 {
	celsius := (romer - 7.5) * 40 / 21
	return CelsiusTo(celsius, to)
}

// Convert converts a temperature from one unit to another
func Convert(value float64, from, to TemperatureUnit) float64 {
	switch from {
	case Celsius:
		return CelsiusTo(value, to)
	case Fahrenheit:
		return FahrenheitTo(value, to)
	case Kelvin:
		return KelvinTo(value, to)
	case Rankine:
		return RankineTo(value, to)
	case Delisle:
		return DelisleTo(value, to)
	case Newton:
		return NewtonTo(value, to)
	case Reaumur:
		return ReaumurTo(value, to)
	case Romer:
		return RomerTo(value, to)
	default:
		return value
	}
}

// ConvertTo converts a Temperature to a different unit
func (t Temperature) ConvertTo(to TemperatureUnit) Temperature {
	return Temperature{
		Value: Convert(t.Value, t.Unit, to),
		Unit:  to,
	}
}

// String returns a formatted string representation
func (t Temperature) String() string {
	return fmt.Sprintf("%.2f° %s", t.Value, t.Unit)
}

// IsAboveAbsoluteZero checks if the temperature is above absolute zero
func (t Temperature) IsAboveAbsoluteZero() bool {
	kelvin := t.ConvertTo(Kelvin)
	return kelvin.Value > AbsoluteZeroK
}

// IsValid checks if the temperature is physically valid (above absolute zero)
func (t Temperature) IsValid() bool {
	return t.IsAboveAbsoluteZero()
}

// Equals checks if two temperatures are equal (with tolerance)
func (t Temperature) Equals(other Temperature, tolerance float64) bool {
	otherInSameUnit := other.ConvertTo(t.Unit)
	return math.Abs(t.Value-otherInSameUnit.Value) <= tolerance
}

// LessThan checks if this temperature is less than another
func (t Temperature) LessThan(other Temperature) bool {
	otherInSameUnit := other.ConvertTo(t.Unit)
	return t.Value < otherInSameUnit.Value
}

// GreaterThan checks if this temperature is greater than another
func (t Temperature) GreaterThan(other Temperature) bool {
	otherInSameUnit := other.ConvertTo(t.Unit)
	return t.Value > otherInSameUnit.Value
}

// Range represents a temperature range
type Range struct {
	Min Temperature
	Max Temperature
}

// NewRange creates a new temperature range
func NewRange(min, max float64, unit TemperatureUnit) Range {
	return Range{
		Min: NewTemperature(min, unit),
		Max: NewTemperature(max, unit),
	}
}

// Contains checks if a temperature is within the range
func (r Range) Contains(t Temperature) bool {
	minInUnit := r.Min.ConvertTo(t.Unit)
	maxInUnit := r.Max.ConvertTo(t.Unit)
	return t.Value >= minInUnit.Value && t.Value <= maxInUnit.Value
}

// String returns a formatted string representation of the range
func (r Range) String() string {
	return fmt.Sprintf("%s to %s", r.Min, r.Max)
}

// CommonRanges provides commonly used temperature ranges
var CommonRanges = struct {
	AbsoluteZeroToWaterFreezing Range
	WaterFreezingToBoiling      Range
	HumanComfortRange           Range
	ColdWeatherRange            Range
	HotWeatherRange             Range
}{
	AbsoluteZeroToWaterFreezing: NewRange(-273.15, 0, Celsius),
	WaterFreezingToBoiling:      NewRange(0, 100, Celsius),
	HumanComfortRange:           NewRange(18, 24, Celsius),
	ColdWeatherRange:            NewRange(-20, 0, Celsius),
	HotWeatherRange:             NewRange(30, 45, Celsius),
}

// WindChill calculates the wind chill temperature (apparent temperature)
// Uses the North American wind chill formula (temperature in Celsius, wind speed in km/h)
// Only valid for temperatures at or below 10°C and wind speeds above 4.8 km/h
func WindChill(tempC, windSpeedKmh float64) float64 {
	if tempC > 10 || windSpeedKmh <= 4.8 {
		return tempC
	}
	return 13.12 + 0.6215*tempC - 11.37*math.Pow(windSpeedKmh, 0.16) + 0.3965*tempC*math.Pow(windSpeedKmh, 0.16)
}

// HeatIndex calculates the heat index (apparent temperature)
// Uses temperature in Celsius and relative humidity (0-100)
// Only valid for temperatures above 27°C
func HeatIndex(tempC, relativeHumidity float64) float64 {
	if tempC < 27 {
		return tempC
	}
	
	// Convert to Fahrenheit for the standard formula
	tempF := CelsiusTo(tempC, Fahrenheit)
	
	// Simple heat index formula
	hi := -42.379 + 2.04901523*tempF + 10.14333127*relativeHumidity
	hi -= 0.22475541*tempF*relativeHumidity
	hi -= 0.00683783*tempF*tempF
	hi -= 0.05481717*relativeHumidity*relativeHumidity
	hi += 0.00122874*tempF*tempF*relativeHumidity
	hi += 0.00085282*tempF*relativeHumidity*relativeHumidity
	hi -= 0.00000199*tempF*tempF*relativeHumidity*relativeHumidity
	
	// Convert back to Celsius
	return FahrenheitTo(hi, Celsius)
}

// Average calculates the average of multiple temperatures
func Average(temperatures ...Temperature) Temperature {
	if len(temperatures) == 0 {
		return NewTemperature(0, Celsius)
	}
	
	var sum float64
	unit := temperatures[0].Unit
	
	for _, t := range temperatures {
		sum += t.ConvertTo(unit).Value
	}
	
	return NewTemperature(sum/float64(len(temperatures)), unit)
}

// Min returns the minimum temperature from a slice
func Min(temperatures ...Temperature) Temperature {
	if len(temperatures) == 0 {
		return NewTemperature(0, Celsius)
	}
	
	min := temperatures[0]
	for _, t := range temperatures[1:] {
		if t.LessThan(min) {
			min = t
		}
	}
	return min
}

// Max returns the maximum temperature from a slice
func Max(temperatures ...Temperature) Temperature {
	if len(temperatures) == 0 {
		return NewTemperature(0, Celsius)
	}
	
	max := temperatures[0]
	for _, t := range temperatures[1:] {
		if t.GreaterThan(max) {
			max = t
		}
	}
	return max
}

// Delta calculates the difference between two temperatures
func Delta(t1, t2 Temperature) Temperature {
	t2InUnit1 := t2.ConvertTo(t1.Unit)
	return NewTemperature(math.Abs(t1.Value-t2InUnit1.Value), t1.Unit)
}

// ParseUnit parses a string to a TemperatureUnit
func ParseUnit(s string) (TemperatureUnit, error) {
	switch s {
	case "C", "c", "Celsius", "celsius":
		return Celsius, nil
	case "F", "f", "Fahrenheit", "fahrenheit":
		return Fahrenheit, nil
	case "K", "k", "Kelvin", "kelvin":
		return Kelvin, nil
	case "R", "r", "Ra", "ra", "Rankine", "rankine":
		return Rankine, nil
	case "D", "d", "De", "de", "Delisle", "delisle":
		return Delisle, nil
	case "N", "n", "Newton", "newton":
		return Newton, nil
	case "Re", "re", "Réaumur", "reaumur", "Reaumur":
		return Reaumur, nil
	case "Ro", "ro", "Rømer", "romer", "Romer":
		return Romer, nil
	default:
		return "", fmt.Errorf("unknown temperature unit: %s", s)
	}
}

// FormatWithSymbol formats a temperature with the standard unit symbol
func FormatWithSymbol(value float64, unit TemperatureUnit) string {
	switch unit {
	case Celsius:
		return fmt.Sprintf("%.2f°C", value)
	case Fahrenheit:
		return fmt.Sprintf("%.2f°F", value)
	case Kelvin:
		return fmt.Sprintf("%.2f K", value)
	case Rankine:
		return fmt.Sprintf("%.2f°R", value)
	case Delisle:
		return fmt.Sprintf("%.2f°De", value)
	case Newton:
		return fmt.Sprintf("%.2f°N", value)
	case Reaumur:
		return fmt.Sprintf("%.2f°Ré", value)
	case Romer:
		return fmt.Sprintf("%.2f°Rø", value)
	default:
		return fmt.Sprintf("%.2f", value)
	}
}