// Package converter_utils provides comprehensive unit conversion utilities.
// Supports length, weight, temperature, time, data storage, volume, area, speed, and more.
// Zero external dependencies - uses only Go standard library.
package converter_utils

import (
	"errors"
	"fmt"
	"math"
	"strconv"
	"strings"
)

// ============================================================
// Length Conversion
// ============================================================

// LengthUnit represents a unit of length
type LengthUnit string

const (
	Meter      LengthUnit = "m"
	Kilometer  LengthUnit = "km"
	Centimeter LengthUnit = "cm"
	Millimeter LengthUnit = "mm"
	Mile       LengthUnit = "mi"
	Yard       LengthUnit = "yd"
	Foot       LengthUnit = "ft"
	Inch       LengthUnit = "in"
	NauticalMile LengthUnit = "nmi"
)

// lengthToMeter contains conversion factors to meters
var lengthToMeter = map[LengthUnit]float64{
	Meter:        1,
	Kilometer:    1000,
	Centimeter:   0.01,
	Millimeter:   0.001,
	Mile:         1609.344,
	Yard:         0.9144,
	Foot:         0.3048,
	Inch:         0.0254,
	NauticalMile: 1852,
}

// ConvertLength converts a length value from one unit to another
func ConvertLength(value float64, from, to LengthUnit) (float64, error) {
	fromFactor, ok := lengthToMeter[from]
	if !ok {
		return 0, fmt.Errorf("unknown length unit: %s", from)
	}
	toFactor, ok := lengthToMeter[to]
	if !ok {
		return 0, fmt.Errorf("unknown length unit: %s", to)
	}
	return value * fromFactor / toFactor, nil
}

// LengthConverter provides fluent length conversion
type LengthConverter struct {
	value float64
	unit  LengthUnit
}

// Length creates a new LengthConverter
func Length(value float64, unit LengthUnit) *LengthConverter {
	return &LengthConverter{value: value, unit: unit}
}

// To converts to the specified unit
func (lc *LengthConverter) To(unit LengthUnit) (float64, error) {
	return ConvertLength(lc.value, lc.unit, unit)
}

// Meters returns the value in meters
func (lc *LengthConverter) Meters() float64 {
	v, _ := lc.To(Meter)
	return v
}

// Kilometers returns the value in kilometers
func (lc *LengthConverter) Kilometers() float64 {
	v, _ := lc.To(Kilometer)
	return v
}

// Miles returns the value in miles
func (lc *LengthConverter) Miles() float64 {
	v, _ := lc.To(Mile)
	return v
}

// Feet returns the value in feet
func (lc *LengthConverter) Feet() float64 {
	v, _ := lc.To(Foot)
	return v
}

// Inches returns the value in inches
func (lc *LengthConverter) Inches() float64 {
	v, _ := lc.To(Inch)
	return v
}

// ============================================================
// Weight/Mass Conversion
// ============================================================

// WeightUnit represents a unit of weight/mass
type WeightUnit string

const (
	Kilogram    WeightUnit = "kg"
	Gram        WeightUnit = "g"
	Milligram   WeightUnit = "mg"
	MetricTon   WeightUnit = "t"
	Pound       WeightUnit = "lb"
	Ounce       WeightUnit = "oz"
	Stone       WeightUnit = "st"
	CarGram     WeightUnit = "ct" // carat
)

// weightToKilogram contains conversion factors to kilograms
var weightToKilogram = map[WeightUnit]float64{
	Kilogram:  1,
	Gram:      0.001,
	Milligram: 0.000001,
	MetricTon: 1000,
	Pound:     0.45359237,
	Ounce:     0.028349523125,
	Stone:     6.35029318,
	CarGram:   0.0002,
}

// ConvertWeight converts a weight value from one unit to another
func ConvertWeight(value float64, from, to WeightUnit) (float64, error) {
	fromFactor, ok := weightToKilogram[from]
	if !ok {
		return 0, fmt.Errorf("unknown weight unit: %s", from)
	}
	toFactor, ok := weightToKilogram[to]
	if !ok {
		return 0, fmt.Errorf("unknown weight unit: %s", to)
	}
	return value * fromFactor / toFactor, nil
}

// WeightConverter provides fluent weight conversion
type WeightConverter struct {
	value float64
	unit  WeightUnit
}

// Weight creates a new WeightConverter
func Weight(value float64, unit WeightUnit) *WeightConverter {
	return &WeightConverter{value: value, unit: unit}
}

// To converts to the specified unit
func (wc *WeightConverter) To(unit WeightUnit) (float64, error) {
	return ConvertWeight(wc.value, wc.unit, unit)
}

// Kilograms returns the value in kilograms
func (wc *WeightConverter) Kilograms() float64 {
	v, _ := wc.To(Kilogram)
	return v
}

// Pounds returns the value in pounds
func (wc *WeightConverter) Pounds() float64 {
	v, _ := wc.To(Pound)
	return v
}

// Ounces returns the value in ounces
func (wc *WeightConverter) Ounces() float64 {
	v, _ := wc.To(Ounce)
	return v
}

// Grams returns the value in grams
func (wc *WeightConverter) Grams() float64 {
	v, _ := wc.To(Gram)
	return v
}

// ============================================================
// Temperature Conversion
// ============================================================

// TemperatureUnit represents a temperature scale
type TemperatureUnit string

const (
	Celsius    TemperatureUnit = "C"
	Fahrenheit TemperatureUnit = "F"
	Kelvin     TemperatureUnit = "K"
)

// ConvertTemperature converts temperature between Celsius, Fahrenheit, and Kelvin
func ConvertTemperature(value float64, from, to TemperatureUnit) (float64, error) {
	// First convert to Celsius
	var celsius float64
	switch from {
	case Celsius:
		celsius = value
	case Fahrenheit:
		celsius = (value - 32) * 5 / 9
	case Kelvin:
		celsius = value - 273.15
	default:
		return 0, fmt.Errorf("unknown temperature unit: %s", from)
	}

	// Then convert from Celsius to target
	switch to {
	case Celsius:
		return celsius, nil
	case Fahrenheit:
		return celsius*9/5 + 32, nil
	case Kelvin:
		return celsius + 273.15, nil
	default:
		return 0, fmt.Errorf("unknown temperature unit: %s", to)
	}
}

// TemperatureConverter provides fluent temperature conversion
type TemperatureConverter struct {
	value float64
	unit  TemperatureUnit
}

// Temperature creates a new TemperatureConverter
func Temperature(value float64, unit TemperatureUnit) *TemperatureConverter {
	return &TemperatureConverter{value: value, unit: unit}
}

// To converts to the specified unit
func (tc *TemperatureConverter) To(unit TemperatureUnit) (float64, error) {
	return ConvertTemperature(tc.value, tc.unit, unit)
}

// Celsius returns the value in Celsius
func (tc *TemperatureConverter) Celsius() float64 {
	v, _ := tc.To(Celsius)
	return v
}

// Fahrenheit returns the value in Fahrenheit
func (tc *TemperatureConverter) Fahrenheit() float64 {
	v, _ := tc.To(Fahrenheit)
	return v
}

// Kelvin returns the value in Kelvin
func (tc *TemperatureConverter) Kelvin() float64 {
	v, _ := tc.To(Kelvin)
	return v
}

// ============================================================
// Time Conversion
// ============================================================

// TimeUnit represents a unit of time
type TimeUnit string

const (
	Nanosecond  TimeUnit = "ns"
	Microsecond TimeUnit = "μs"
	Millisecond TimeUnit = "ms"
	Second      TimeUnit = "s"
	Minute      TimeUnit = "min"
	Hour        TimeUnit = "h"
	Day         TimeUnit = "d"
	Week        TimeUnit = "wk"
	Month       TimeUnit = "mo"
	Year        TimeUnit = "yr"
)

// timeToSecond contains conversion factors to seconds
var timeToSecond = map[TimeUnit]float64{
	Nanosecond:  1e-9,
	Microsecond: 1e-6,
	Millisecond: 1e-3,
	Second:      1,
	Minute:      60,
	Hour:        3600,
	Day:         86400,
	Week:        604800,
	Month:       2629746, // Average month (365.2425/12 days)
	Year:        31556952, // Average year (365.2425 days)
}

// ConvertTime converts a time value from one unit to another
func ConvertTime(value float64, from, to TimeUnit) (float64, error) {
	fromFactor, ok := timeToSecond[from]
	if !ok {
		return 0, fmt.Errorf("unknown time unit: %s", from)
	}
	toFactor, ok := timeToSecond[to]
	if !ok {
		return 0, fmt.Errorf("unknown time unit: %s", to)
	}
	return value * fromFactor / toFactor, nil
}

// TimeConverter provides fluent time conversion
type TimeConverter struct {
	value float64
	unit  TimeUnit
}

// Duration creates a new TimeConverter
func Duration(value float64, unit TimeUnit) *TimeConverter {
	return &TimeConverter{value: value, unit: unit}
}

// To converts to the specified unit
func (tc *TimeConverter) To(unit TimeUnit) (float64, error) {
	return ConvertTime(tc.value, tc.unit, unit)
}

// Seconds returns the value in seconds
func (tc *TimeConverter) Seconds() float64 {
	v, _ := tc.To(Second)
	return v
}

// Minutes returns the value in minutes
func (tc *TimeConverter) Minutes() float64 {
	v, _ := tc.To(Minute)
	return v
}

// Hours returns the value in hours
func (tc *TimeConverter) Hours() float64 {
	v, _ := tc.To(Hour)
	return v
}

// Days returns the value in days
func (tc *TimeConverter) Days() float64 {
	v, _ := tc.To(Day)
	return v
}

// ============================================================
// Data Storage Conversion
// ============================================================

// DataUnit represents a unit of digital storage
type DataUnit string

const (
	Bit       DataUnit = "b"
	Byte      DataUnit = "B"
	Kilobyte  DataUnit = "KB"
	Megabyte  DataUnit = "MB"
	Gigabyte  DataUnit = "GB"
	Terabyte  DataUnit = "TB"
	Petabyte  DataUnit = "PB"
	Kibibyte  DataUnit = "KiB"
	Mebibyte  DataUnit = "MiB"
	Gibibyte  DataUnit = "GiB"
	Tebibyte  DataUnit = "TiB"
	Pebibyte  DataUnit = "PiB"
)

// dataToByte contains conversion factors to bytes
var dataToByte = map[DataUnit]float64{
	Bit:      0.125,
	Byte:     1,
	Kilobyte: 1000,
	Megabyte: 1000 * 1000,
	Gigabyte: 1000 * 1000 * 1000,
	Terabyte: 1000 * 1000 * 1000 * 1000,
	Petabyte: 1000 * 1000 * 1000 * 1000 * 1000,
	Kibibyte: 1024,
	Mebibyte: 1024 * 1024,
	Gibibyte: 1024 * 1024 * 1024,
	Tebibyte: 1024 * 1024 * 1024 * 1024,
	Pebibyte: 1024 * 1024 * 1024 * 1024 * 1024,
}

// ConvertData converts a data storage value from one unit to another
func ConvertData(value float64, from, to DataUnit) (float64, error) {
	fromFactor, ok := dataToByte[from]
	if !ok {
		return 0, fmt.Errorf("unknown data unit: %s", from)
	}
	toFactor, ok := dataToByte[to]
	if !ok {
		return 0, fmt.Errorf("unknown data unit: %s", to)
	}
	return value * fromFactor / toFactor, nil
}

// DataConverter provides fluent data storage conversion
type DataConverter struct {
	value float64
	unit  DataUnit
}

// Data creates a new DataConverter
func Data(value float64, unit DataUnit) *DataConverter {
	return &DataConverter{value: value, unit: unit}
}

// To converts to the specified unit
func (dc *DataConverter) To(unit DataUnit) (float64, error) {
	return ConvertData(dc.value, dc.unit, unit)
}

// Bytes returns the value in bytes
func (dc *DataConverter) Bytes() float64 {
	v, _ := dc.To(Byte)
	return v
}

// Kilobytes returns the value in kilobytes
func (dc *DataConverter) Kilobytes() float64 {
	v, _ := dc.To(Kilobyte)
	return v
}

// Megabytes returns the value in megabytes
func (dc *DataConverter) Megabytes() float64 {
	v, _ := dc.To(Megabyte)
	return v
}

// Gigabytes returns the value in gigabytes
func (dc *DataConverter) Gigabytes() float64 {
	v, _ := dc.To(Gigabyte)
	return v
}

// ============================================================
// Volume Conversion
// ============================================================

// VolumeUnit represents a unit of volume
type VolumeUnit string

const (
	Liter      VolumeUnit = "L"
	Milliliter VolumeUnit = "mL"
	CubicMeter VolumeUnit = "m³"
	CubicInch  VolumeUnit = "in³"
	CubicFoot  VolumeUnit = "ft³"
	Gallon     VolumeUnit = "gal" // US liquid gallon
	Quart      VolumeUnit = "qt"  // US liquid quart
	Pint       VolumeUnit = "pt"  // US liquid pint
	Cup        VolumeUnit = "cup" // US cup
	FluidOunce VolumeUnit = "fl oz"
	Tablespoon VolumeUnit = "tbsp"
	Teaspoon   VolumeUnit = "tsp"
)

// volumeToLiter contains conversion factors to liters
var volumeToLiter = map[VolumeUnit]float64{
	Liter:      1,
	Milliliter: 0.001,
	CubicMeter: 1000,
	CubicInch:  0.016387064,
	CubicFoot:  28.316846592,
	Gallon:     3.785411784,
	Quart:      0.946352946,
	Pint:       0.473176473,
	Cup:        0.2365882365,
	FluidOunce: 0.0295735296,
	Tablespoon: 0.0147867648,
	Teaspoon:   0.00492892159,
}

// ConvertVolume converts a volume value from one unit to another
func ConvertVolume(value float64, from, to VolumeUnit) (float64, error) {
	fromFactor, ok := volumeToLiter[from]
	if !ok {
		return 0, fmt.Errorf("unknown volume unit: %s", from)
	}
	toFactor, ok := volumeToLiter[to]
	if !ok {
		return 0, fmt.Errorf("unknown volume unit: %s", to)
	}
	return value * fromFactor / toFactor, nil
}

// VolumeConverter provides fluent volume conversion
type VolumeConverter struct {
	value float64
	unit  VolumeUnit
}

// Volume creates a new VolumeConverter
func Volume(value float64, unit VolumeUnit) *VolumeConverter {
	return &VolumeConverter{value: value, unit: unit}
}

// To converts to the specified unit
func (vc *VolumeConverter) To(unit VolumeUnit) (float64, error) {
	return ConvertVolume(vc.value, vc.unit, unit)
}

// Liters returns the value in liters
func (vc *VolumeConverter) Liters() float64 {
	v, _ := vc.To(Liter)
	return v
}

// Milliliters returns the value in milliliters
func (vc *VolumeConverter) Milliliters() float64 {
	v, _ := vc.To(Milliliter)
	return v
}

// Gallons returns the value in US gallons
func (vc *VolumeConverter) Gallons() float64 {
	v, _ := vc.To(Gallon)
	return v
}

// ============================================================
// Area Conversion
// ============================================================

// AreaUnit represents a unit of area
type AreaUnit string

const (
	SquareMeter      AreaUnit = "m²"
	SquareKilometer  AreaUnit = "km²"
	SquareCentimeter AreaUnit = "cm²"
	SquareMillimeter AreaUnit = "mm²"
	Hectare          AreaUnit = "ha"
	Are              AreaUnit = "a"
	SquareMile       AreaUnit = "mi²"
	SquareYard       AreaUnit = "yd²"
	SquareFoot       AreaUnit = "ft²"
	SquareInch       AreaUnit = "in²"
	Acre             AreaUnit = "ac"
)

// areaToSquareMeter contains conversion factors to square meters
var areaToSquareMeter = map[AreaUnit]float64{
	SquareMeter:      1,
	SquareKilometer:  1000000,
	SquareCentimeter: 0.0001,
	SquareMillimeter: 0.000001,
	Hectare:          10000,
	Are:              100,
	SquareMile:       2589988.110336,
	SquareYard:       0.83612736,
	SquareFoot:       0.09290304,
	SquareInch:       0.00064516,
	Acre:             4046.8564224,
}

// ConvertArea converts an area value from one unit to another
func ConvertArea(value float64, from, to AreaUnit) (float64, error) {
	fromFactor, ok := areaToSquareMeter[from]
	if !ok {
		return 0, fmt.Errorf("unknown area unit: %s", from)
	}
	toFactor, ok := areaToSquareMeter[to]
	if !ok {
		return 0, fmt.Errorf("unknown area unit: %s", to)
	}
	return value * fromFactor / toFactor, nil
}

// AreaConverter provides fluent area conversion
type AreaConverter struct {
	value float64
	unit  AreaUnit
}

// Area creates a new AreaConverter
func Area(value float64, unit AreaUnit) *AreaConverter {
	return &AreaConverter{value: value, unit: unit}
}

// To converts to the specified unit
func (ac *AreaConverter) To(unit AreaUnit) (float64, error) {
	return ConvertArea(ac.value, ac.unit, unit)
}

// SquareMeters returns the value in square meters
func (ac *AreaConverter) SquareMeters() float64 {
	v, _ := ac.To(SquareMeter)
	return v
}

// Hectares returns the value in hectares
func (ac *AreaConverter) Hectares() float64 {
	v, _ := ac.To(Hectare)
	return v
}

// Acres returns the value in acres
func (ac *AreaConverter) Acres() float64 {
	v, _ := ac.To(Acre)
	return v
}

// ============================================================
// Speed Conversion
// ============================================================

// SpeedUnit represents a unit of speed
type SpeedUnit string

const (
	MeterPerSecond     SpeedUnit = "m/s"
	KilometerPerHour   SpeedUnit = "km/h"
	MilePerHour        SpeedUnit = "mph"
	FootPerSecond      SpeedUnit = "ft/s"
	Knot               SpeedUnit = "kn"
	Mach               SpeedUnit = "Ma"
)

// speedToMeterPerSecond contains conversion factors to meters per second
var speedToMeterPerSecond = map[SpeedUnit]float64{
	MeterPerSecond:   1,
	KilometerPerHour: 1000.0 / 3600.0,
	MilePerHour:      0.44704,
	FootPerSecond:    0.3048,
	Knot:             0.514444444,
	Mach:             340.29, // Speed of sound at sea level, 15°C
}

// ConvertSpeed converts a speed value from one unit to another
func ConvertSpeed(value float64, from, to SpeedUnit) (float64, error) {
	fromFactor, ok := speedToMeterPerSecond[from]
	if !ok {
		return 0, fmt.Errorf("unknown speed unit: %s", from)
	}
	toFactor, ok := speedToMeterPerSecond[to]
	if !ok {
		return 0, fmt.Errorf("unknown speed unit: %s", to)
	}
	return value * fromFactor / toFactor, nil
}

// SpeedConverter provides fluent speed conversion
type SpeedConverter struct {
	value float64
	unit  SpeedUnit
}

// Speed creates a new SpeedConverter
func Speed(value float64, unit SpeedUnit) *SpeedConverter {
	return &SpeedConverter{value: value, unit: unit}
}

// To converts to the specified unit
func (sc *SpeedConverter) To(unit SpeedUnit) (float64, error) {
	return ConvertSpeed(sc.value, sc.unit, unit)
}

// MetersPerSecond returns the value in m/s
func (sc *SpeedConverter) MetersPerSecond() float64 {
	v, _ := sc.To(MeterPerSecond)
	return v
}

// KilometersPerHour returns the value in km/h
func (sc *SpeedConverter) KilometersPerHour() float64 {
	v, _ := sc.To(KilometerPerHour)
	return v
}

// MilesPerHour returns the value in mph
func (sc *SpeedConverter) MilesPerHour() float64 {
	v, _ := sc.To(MilePerHour)
	return v
}

// Knots returns the value in knots
func (sc *SpeedConverter) Knots() float64 {
	v, _ := sc.To(Knot)
	return v
}

// ============================================================
// Pressure Conversion
// ============================================================

// PressureUnit represents a unit of pressure
type PressureUnit string

const (
	Pascal       PressureUnit = "Pa"
	Kilopascal   PressureUnit = "kPa"
	Megapascal   PressureUnit = "MPa"
	Bar          PressureUnit = "bar"
	Millibar     PressureUnit = "mbar"
	Atmosphere   PressureUnit = "atm"
	PSI          PressureUnit = "psi" // Pounds per square inch
	Torr         PressureUnit = "Torr"
	MmHg         PressureUnit = "mmHg" // Millimeters of mercury
)

// pressureToPascal contains conversion factors to Pascals
var pressureToPascal = map[PressureUnit]float64{
	Pascal:     1,
	Kilopascal: 1000,
	Megapascal: 1000000,
	Bar:        100000,
	Millibar:   100,
	Atmosphere: 101325,
	PSI:        6894.757293168,
	Torr:       133.3223684211,
	MmHg:       133.3223684211,
}

// ConvertPressure converts a pressure value from one unit to another
func ConvertPressure(value float64, from, to PressureUnit) (float64, error) {
	fromFactor, ok := pressureToPascal[from]
	if !ok {
		return 0, fmt.Errorf("unknown pressure unit: %s", from)
	}
	toFactor, ok := pressureToPascal[to]
	if !ok {
		return 0, fmt.Errorf("unknown pressure unit: %s", to)
	}
	return value * fromFactor / toFactor, nil
}

// PressureConverter provides fluent pressure conversion
type PressureConverter struct {
	value float64
	unit  PressureUnit
}

// Pressure creates a new PressureConverter
func Pressure(value float64, unit PressureUnit) *PressureConverter {
	return &PressureConverter{value: value, unit: unit}
}

// To converts to the specified unit
func (pc *PressureConverter) To(unit PressureUnit) (float64, error) {
	return ConvertPressure(pc.value, pc.unit, unit)
}

// Pascals returns the value in Pascals
func (pc *PressureConverter) Pascals() float64 {
	v, _ := pc.To(Pascal)
	return v
}

// Bars returns the value in bars
func (pc *PressureConverter) Bars() float64 {
	v, _ := pc.To(Bar)
	return v
}

// PSI returns the value in PSI
func (pc *PressureConverter) PSI() float64 {
	v, _ := pc.To(PSI)
	return v
}

// Atmospheres returns the value in atmospheres
func (pc *PressureConverter) Atmospheres() float64 {
	v, _ := pc.To(Atmosphere)
	return v
}

// ============================================================
// Angle Conversion
// ============================================================

// ConvertDegreesToRadians converts degrees to radians
func ConvertDegreesToRadians(degrees float64) float64 {
	return degrees * math.Pi / 180
}

// ConvertRadiansToDegrees converts radians to degrees
func ConvertRadiansToDegrees(radians float64) float64 {
	return radians * 180 / math.Pi
}

// AngleConverter provides fluent angle conversion
type AngleConverter struct {
	degrees float64
}

// Angle creates a new AngleConverter from degrees
func Angle(degrees float64) *AngleConverter {
	return &AngleConverter{degrees: degrees}
}

// AngleFromRadians creates a new AngleConverter from radians
func AngleFromRadians(radians float64) *AngleConverter {
	return &AngleConverter{degrees: ConvertRadiansToDegrees(radians)}
}

// Degrees returns the angle in degrees
func (ac *AngleConverter) Degrees() float64 {
	return ac.degrees
}

// Radians returns the angle in radians
func (ac *AngleConverter) Radians() float64 {
	return ConvertDegreesToRadians(ac.degrees)
}

// ============================================================
// Fuel Consumption Conversion
// ============================================================

// FuelUnit represents a unit of fuel consumption
type FuelUnit string

const (
	LitersPer100km   FuelUnit = "L/100km"
	KilometersPerLiter FuelUnit = "km/L"
	MilesPerGallonUS  FuelUnit = "mpg(US)"
	MilesPerGallonUK  FuelUnit = "mpg(UK)"
)

// ConvertFuelConsumption converts fuel consumption between different units
func ConvertFuelConsumption(value float64, from, to FuelUnit) (float64, error) {
	// Convert to km/L first
	var kmPerLiter float64
	
	switch from {
	case LitersPer100km:
		if value == 0 {
			return 0, nil
		}
		kmPerLiter = 100 / value
	case KilometersPerLiter:
		kmPerLiter = value
	case MilesPerGallonUS:
		kmPerLiter = value * 0.425143707
	case MilesPerGallonUK:
		kmPerLiter = value * 0.354006
	default:
		return 0, fmt.Errorf("unknown fuel consumption unit: %s", from)
	}
	
	// Convert from km/L to target unit
	switch to {
	case LitersPer100km:
		if kmPerLiter == 0 {
			return 0, nil
		}
		return 100 / kmPerLiter, nil
	case KilometersPerLiter:
		return kmPerLiter, nil
	case MilesPerGallonUS:
		return kmPerLiter / 0.425143707, nil
	case MilesPerGallonUK:
		return kmPerLiter / 0.354006, nil
	default:
		return 0, fmt.Errorf("unknown fuel consumption unit: %s", to)
	}
}

// ============================================================
// Generic Converter
// ============================================================

// Converter provides a generic conversion interface
type Converter struct {
	value float64
}

// NewConverter creates a new Converter with a value
func NewConverter(value float64) *Converter {
	return &Converter{value: value}
}

// AsLength creates a LengthConverter
func (c *Converter) AsLength(unit LengthUnit) *LengthConverter {
	return Length(c.value, unit)
}

// AsWeight creates a WeightConverter
func (c *Converter) AsWeight(unit WeightUnit) *WeightConverter {
	return Weight(c.value, unit)
}

// AsTemperature creates a TemperatureConverter
func (c *Converter) AsTemperature(unit TemperatureUnit) *TemperatureConverter {
	return Temperature(c.value, unit)
}

// AsDuration creates a TimeConverter
func (c *Converter) AsDuration(unit TimeUnit) *TimeConverter {
	return Duration(c.value, unit)
}

// AsData creates a DataConverter
func (c *Converter) AsData(unit DataUnit) *DataConverter {
	return Data(c.value, unit)
}

// AsVolume creates a VolumeConverter
func (c *Converter) AsVolume(unit VolumeUnit) *VolumeConverter {
	return Volume(c.value, unit)
}

// AsArea creates an AreaConverter
func (c *Converter) AsArea(unit AreaUnit) *AreaConverter {
	return Area(c.value, unit)
}

// AsSpeed creates a SpeedConverter
func (c *Converter) AsSpeed(unit SpeedUnit) *SpeedConverter {
	return Speed(c.value, unit)
}

// AsPressure creates a PressureConverter
func (c *Converter) AsPressure(unit PressureUnit) *PressureConverter {
	return Pressure(c.value, unit)
}

// AsAngle creates an AngleConverter
func (c *Converter) AsAngle() *AngleConverter {
	return Angle(c.value)
}

// ============================================================
// Parsing Utilities
// ============================================================

var (
	ErrInvalidFormat = errors.New("invalid format")
	ErrUnknownUnit   = errors.New("unknown unit")
)

// ParseLength parses a string like "100 km" or "50.5 mi" into meters
func ParseLength(s string) (float64, error) {
	value, unit, err := parseValueUnit(s)
	if err != nil {
		return 0, err
	}
	
	lu := parseLengthUnit(unit)
	if lu == "" {
		return 0, fmt.Errorf("%w: %s", ErrUnknownUnit, unit)
	}
	
	return Length(value, lu).Meters(), nil
}

// ParseWeight parses a string like "100 kg" or "50.5 lb" into kilograms
func ParseWeight(s string) (float64, error) {
	value, unit, err := parseValueUnit(s)
	if err != nil {
		return 0, err
	}
	
	wu := parseWeightUnit(unit)
	if wu == "" {
		return 0, fmt.Errorf("%w: %s", ErrUnknownUnit, unit)
	}
	
	return Weight(value, wu).Kilograms(), nil
}

// ParseTemperature parses a string like "100 C" or "50.5 F" into Celsius
func ParseTemperature(s string) (float64, error) {
	value, unit, err := parseValueUnit(s)
	if err != nil {
		return 0, err
	}
	
	tu := parseTemperatureUnit(unit)
	if tu == "" {
		return 0, fmt.Errorf("%w: %s", ErrUnknownUnit, unit)
	}
	
	return Temperature(value, tu).Celsius(), nil
}

// ParseDuration parses a string like "100 s" or "1.5 h" into seconds
func ParseDuration(s string) (float64, error) {
	value, unit, err := parseValueUnit(s)
	if err != nil {
		return 0, err
	}
	
	tu := parseTimeUnit(unit)
	if tu == "" {
		return 0, fmt.Errorf("%w: %s", ErrUnknownUnit, unit)
	}
	
	return Duration(value, tu).Seconds(), nil
}

// ParseData parses a string like "100 MB" or "1.5 GB" into bytes
func ParseData(s string) (float64, error) {
	value, unit, err := parseValueUnit(s)
	if err != nil {
		return 0, err
	}
	
	du := parseDataUnit(unit)
	if du == "" {
		return 0, fmt.Errorf("%w: %s", ErrUnknownUnit, unit)
	}
	
	return Data(value, du).Bytes(), nil
}

// parseValueUnit extracts numeric value and unit from a string
func parseValueUnit(s string) (float64, string, error) {
	s = strings.TrimSpace(s)
	
	// Find the split point between number and unit
	var i int
	for i = 0; i < len(s); i++ {
		c := s[i]
		if !((c >= '0' && c <= '9') || c == '.' || c == '-' || c == '+' || c == 'e' || c == 'E') {
			break
		}
	}
	
	if i == 0 {
		return 0, "", ErrInvalidFormat
	}
	
	value, err := strconv.ParseFloat(strings.TrimSpace(s[:i]), 64)
	if err != nil {
		return 0, "", fmt.Errorf("%w: %v", ErrInvalidFormat, err)
	}
	
	unit := strings.TrimSpace(s[i:])
	if unit == "" {
		return 0, "", ErrInvalidFormat
	}
	
	return value, unit, nil
}

func parseLengthUnit(s string) LengthUnit {
	switch strings.ToLower(s) {
	case "m", "meter", "meters":
		return Meter
	case "km", "kilometer", "kilometers":
		return Kilometer
	case "cm", "centimeter", "centimeters":
		return Centimeter
	case "mm", "millimeter", "millimeters":
		return Millimeter
	case "mi", "mile", "miles":
		return Mile
	case "yd", "yard", "yards":
		return Yard
	case "ft", "foot", "feet":
		return Foot
	case "in", "inch", "inches":
		return Inch
	case "nmi", "nauticalmile", "nauticalmiles":
		return NauticalMile
	default:
		return ""
	}
}

func parseWeightUnit(s string) WeightUnit {
	switch strings.ToLower(s) {
	case "kg", "kilogram", "kilograms":
		return Kilogram
	case "g", "gram", "grams":
		return Gram
	case "mg", "milligram", "milligrams":
		return Milligram
	case "t", "ton", "metricton", "tonne":
		return MetricTon
	case "lb", "lbs", "pound", "pounds":
		return Pound
	case "oz", "ounce", "ounces":
		return Ounce
	case "st", "stone", "stones":
		return Stone
	case "ct", "carat", "carats":
		return CarGram
	default:
		return ""
	}
}

func parseTemperatureUnit(s string) TemperatureUnit {
	switch strings.ToUpper(s) {
	case "C", "CELSIUS":
		return Celsius
	case "F", "FAHRENHEIT":
		return Fahrenheit
	case "K", "KELVIN":
		return Kelvin
	default:
		return ""
	}
}

func parseTimeUnit(s string) TimeUnit {
	switch strings.ToLower(s) {
	case "ns", "nanosecond", "nanoseconds":
		return Nanosecond
	case "μs", "us", "microsecond", "microseconds":
		return Microsecond
	case "ms", "millisecond", "milliseconds":
		return Millisecond
	case "s", "sec", "second", "seconds":
		return Second
	case "min", "minute", "minutes":
		return Minute
	case "h", "hr", "hour", "hours":
		return Hour
	case "d", "day", "days":
		return Day
	case "wk", "week", "weeks":
		return Week
	case "mo", "month", "months":
		return Month
	case "yr", "y", "year", "years":
		return Year
	default:
		return ""
	}
}

func parseDataUnit(s string) DataUnit {
	switch strings.ToUpper(s) {
	case "B", "BYTE", "BYTES":
		return Byte
	case "KB", "KILOBYTE", "KILOBYTES":
		return Kilobyte
	case "MB", "MEGABYTE", "MEGABYTES":
		return Megabyte
	case "GB", "GIGABYTE", "GIGABYTES":
		return Gigabyte
	case "TB", "TERABYTE", "TERABYTES":
		return Terabyte
	case "PB", "PETABYTE", "PETABYTES":
		return Petabyte
	case "KIB", "KIBIBYTE", "KIBIBYTES":
		return Kibibyte
	case "MIB", "MEBIBYTE", "MEBIBYTES":
		return Mebibyte
	case "GIB", "GIBIBYTE", "GIBIBYTES":
		return Gibibyte
	case "TIB", "TEBIBYTE", "TEBIBYTES":
		return Tebibyte
	case "PIB", "PEBIBYTE", "PEBIBYTES":
		return Pebibyte
	default:
		return ""
	}
}

// ============================================================
// Formatting Utilities
// ============================================================

// FormatNumber formats a number with specified decimal places
func FormatNumber(value float64, decimals int) string {
	format := fmt.Sprintf("%%.%df", decimals)
	return fmt.Sprintf(format, value)
}

// FormatWithCommas formats a number with thousand separators
func FormatWithCommas(value float64, decimals int) string {
	// Round to specified decimals
	multiplier := math.Pow(10, float64(decimals))
	rounded := math.Round(value*multiplier) / multiplier
	
	// Split into integer and decimal parts
	str := fmt.Sprintf("%.10f", rounded)
	parts := strings.Split(str, ".")
	
	intPart := parts[0]
	var result []rune
	
	// Add commas to integer part
	neg := false
	if len(intPart) > 0 && intPart[0] == '-' {
		neg = true
		intPart = intPart[1:]
	}
	
	for i, c := range intPart {
		if i > 0 && (len(intPart)-i)%3 == 0 {
			result = append(result, ',')
		}
		result = append(result, c)
	}
	
	// Reconstruct
	intResult := string(result)
	if neg {
		intResult = "-" + intResult
	}
	
	if decimals > 0 && len(parts) > 1 {
		decimalPart := parts[1]
		if len(decimalPart) > decimals {
			decimalPart = decimalPart[:decimals]
		}
		// Remove trailing zeros
		decimalPart = strings.TrimRight(decimalPart, "0")
		if decimalPart != "" {
			return intResult + "." + decimalPart
		}
	}
	
	return intResult
}

// SmartFormatData formats data size in the most appropriate unit
func SmartFormatData(bytes float64) string {
	units := []DataUnit{Byte, Kilobyte, Megabyte, Gigabyte, Terabyte, Petabyte}
	
	var i int
	value := bytes
	for i = 0; i < len(units)-1 && value >= 1024; i++ {
		value /= 1024
	}
	
	if i == 0 {
		return fmt.Sprintf("%.0f %s", value, units[i])
	}
	return fmt.Sprintf("%.2f %s", value, units[i])
}

// SmartFormatDuration formats duration in a human-readable way
func SmartFormatDuration(seconds float64) string {
	if seconds < 0.001 {
		ns := seconds * 1e9
		return fmt.Sprintf("%.0f ns", ns)
	} else if seconds < 1 {
		ms := seconds * 1000
		return fmt.Sprintf("%.2f ms", ms)
	} else if seconds < 60 {
		return fmt.Sprintf("%.2f s", seconds)
	} else if seconds < 3600 {
		minutes := seconds / 60
		return fmt.Sprintf("%.2f min", minutes)
	} else if seconds < 86400 {
		hours := seconds / 3600
		return fmt.Sprintf("%.2f h", hours)
	} else {
		days := seconds / 86400
		return fmt.Sprintf("%.2f days", days)
	}
}