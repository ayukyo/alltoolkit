// Example program demonstrating converter_utils usage
package main

import (
	"fmt"
	
	"github.com/ayukyo/alltoolkit/Go/converter_utils"
)

func main() {
	fmt.Println("=== Converter Utils Examples ===")
	fmt.Println()
	
	// ============================================================
	// Length Conversion Examples
	// ============================================================
	fmt.Println("--- Length Conversion ---")
	
	// Convert 1 mile to kilometers
	miles := converter_utils.Length(1, converter_utils.Mile)
	fmt.Printf("1 mile = %.4f km\n", miles.Kilometers())
	
	// Convert 100 meters to feet
	meters := converter_utils.Length(100, converter_utils.Meter)
	fmt.Printf("100 meters = %.2f ft\n", meters.Feet())
	
	// Convert 1 nautical mile to kilometers
	nmi := converter_utils.Length(1, converter_utils.NauticalMile)
	fmt.Printf("1 nautical mile = %.3f km\n", nmi.Kilometers())
	
	fmt.Println()
	
	// ============================================================
	// Weight Conversion Examples
	// ============================================================
	fmt.Println("--- Weight Conversion ---")
	
	// Convert 1 pound to kilograms
	pounds := converter_utils.Weight(1, converter_utils.Pound)
	fmt.Printf("1 lb = %.6f kg\n", pounds.Kilograms())
	
	// Convert 100 kilograms to pounds
	kilograms := converter_utils.Weight(100, converter_utils.Kilogram)
	fmt.Printf("100 kg = %.2f lb\n", kilograms.Pounds())
	
	// Convert 1 ounce to grams
	ounces := converter_utils.Weight(1, converter_utils.Ounce)
	fmt.Printf("1 oz = %.4f g\n", ounces.Grams())
	
	fmt.Println()
	
	// ============================================================
	// Temperature Conversion Examples
	// ============================================================
	fmt.Println("--- Temperature Conversion ---")
	
	// Convert 0°C to Fahrenheit and Kelvin
	celsius := converter_utils.Temperature(0, converter_utils.Celsius)
	fmt.Printf("0°C = %.1f°F = %.2f K\n", celsius.Fahrenheit(), celsius.Kelvin())
	
	// Convert 100°C to Fahrenheit
	hundredC := converter_utils.Temperature(100, converter_utils.Celsius)
	fmt.Printf("100°C = %.1f°F\n", hundredC.Fahrenheit())
	
	// Convert -40°F to Celsius (special case where C = F)
	minus40F := converter_utils.Temperature(-40, converter_utils.Fahrenheit)
	fmt.Printf("-40°F = %.1f°C\n", minus40F.Celsius())
	
	fmt.Println()
	
	// ============================================================
	// Time Conversion Examples
	// ============================================================
	fmt.Println("--- Time Conversion ---")
	
	// Convert 1 hour to various units
	hour := converter_utils.Duration(1, converter_utils.Hour)
	fmt.Printf("1 hour = %.0f minutes = %.0f seconds = %.4f days\n", 
		hour.Minutes(), hour.Seconds(), hour.Days())
	
	// Convert 1000 milliseconds to seconds
	ms := converter_utils.Duration(1000, converter_utils.Millisecond)
	fmt.Printf("1000 ms = %.1f s\n", ms.Seconds())
	
	// Convert 1 year to days
	year := converter_utils.Duration(1, converter_utils.Year)
	fmt.Printf("1 year ≈ %.2f days\n", year.Days())
	
	fmt.Println()
	
	// ============================================================
	// Data Storage Conversion Examples
	// ============================================================
	fmt.Println("--- Data Storage Conversion ---")
	
	// Convert 1 GB to MB and bytes
	gb := converter_utils.Data(1, converter_utils.Gigabyte)
	fmt.Printf("1 GB = %.0f MB = %.0f bytes\n", gb.Megabytes(), gb.Bytes())
	
	// Convert 1 GiB to GB (binary vs decimal)
	gib := converter_utils.Data(1, converter_utils.Gibibyte)
	fmt.Printf("1 GiB = %.4f GB\n", gib.Gigabytes())
	
	// Smart format for various sizes
	fmt.Println("Smart formatting:")
	fmt.Printf("500 bytes: %s\n", converter_utils.SmartFormatData(500))
	fmt.Printf("1,500 bytes: %s\n", converter_utils.SmartFormatData(1500))
	fmt.Printf("1,500,000 bytes: %s\n", converter_utils.SmartFormatData(1500000))
	fmt.Printf("1.5 billion bytes: %s\n", converter_utils.SmartFormatData(1500000000))
	fmt.Printf("1.5 trillion bytes: %s\n", converter_utils.SmartFormatData(1500000000000))
	
	fmt.Println()
	
	// ============================================================
	// Volume Conversion Examples
	// ============================================================
	fmt.Println("--- Volume Conversion ---")
	
	// Convert 1 gallon to liters
	gallon := converter_utils.Volume(1, converter_utils.Gallon)
	fmt.Printf("1 US gallon = %.4f L\n", gallon.Liters())
	
	// Convert 1 liter to milliliters
	liter := converter_utils.Volume(1, converter_utils.Liter)
	fmt.Printf("1 L = %.0f mL\n", liter.Milliliters())
	
	// Convert 1 cup to fluid ounces
	cup := converter_utils.Volume(1, converter_utils.Cup)
	oz, _ := cup.To(converter_utils.FluidOunce)
	fmt.Printf("1 cup = %.1f fl oz\n", oz)
	
	fmt.Println()
	
	// ============================================================
	// Area Conversion Examples
	// ============================================================
	fmt.Println("--- Area Conversion ---")
	
	// Convert 1 acre to square meters and hectares
	acre := converter_utils.Area(1, converter_utils.Acre)
	fmt.Printf("1 acre = %.2f m² = %.4f hectares\n", acre.SquareMeters(), acre.Hectares())
	
	// Convert 1 square mile to acres
	sqMile := converter_utils.Area(1, converter_utils.SquareMile)
	acres, _ := sqMile.To(converter_utils.Acre)
	fmt.Printf("1 sq mile = %.0f acres\n", acres)
	
	fmt.Println()
	
	// ============================================================
	// Speed Conversion Examples
	// ============================================================
	fmt.Println("--- Speed Conversion ---")
	
	// Convert 100 km/h to mph
	speedKmh := converter_utils.Speed(100, converter_utils.KilometerPerHour)
	fmt.Printf("100 km/h = %.2f mph = %.2f m/s\n", speedKmh.MilesPerHour(), speedKmh.MetersPerSecond())
	
	// Convert 60 mph to km/h
	speedMph := converter_utils.Speed(60, converter_utils.MilePerHour)
	kmh, _ := speedMph.To(converter_utils.KilometerPerHour)
	fmt.Printf("60 mph = %.2f km/h\n", kmh)
	
	// Convert Mach 1 to km/h
	mach := converter_utils.Speed(1, converter_utils.Mach)
	machKmh, _ := mach.To(converter_utils.KilometerPerHour)
	fmt.Printf("Mach 1 ≈ %.2f km/h\n", machKmh)
	
	fmt.Println()
	
	// ============================================================
	// Pressure Conversion Examples
	// ============================================================
	fmt.Println("--- Pressure Conversion ---")
	
	// Convert 1 atmosphere to PSI and bars
	atm := converter_utils.Pressure(1, converter_utils.Atmosphere)
	fmt.Printf("1 atm = %.2f PSI = %.5f bar\n", atm.PSI(), atm.Bars())
	
	// Convert 1 PSI to kPa
	psi := converter_utils.Pressure(1, converter_utils.PSI)
	kpa, _ := psi.To(converter_utils.Kilopascal)
	fmt.Printf("1 PSI = %.4f kPa\n", kpa)
	
	fmt.Println()
	
	// ============================================================
	// Angle Conversion Examples
	// ============================================================
	fmt.Println("--- Angle Conversion ---")
	
	// Convert 90° to radians
	angle90 := converter_utils.Angle(90)
	fmt.Printf("90° = %.6f rad (π/2 ≈ %.6f)\n", angle90.Radians(), 3.14159265/2)
	
	// Convert π radians to degrees
	anglePi := converter_utils.AngleFromRadians(3.14159265358979)
	fmt.Printf("π rad = %.2f°\n", anglePi.Degrees())
	
	fmt.Println()
	
	// ============================================================
	// Fuel Consumption Examples
	// ============================================================
	fmt.Println("--- Fuel Consumption ---")
	
	// Convert 10 L/100km to mpg
	l100km := 10.0
	mpg, _ := converter_utils.ConvertFuelConsumption(l100km, 
		converter_utils.LitersPer100km, converter_utils.MilesPerGallonUS)
	fmt.Printf("10 L/100km ≈ %.2f mpg (US)\n", mpg)
	
	// Convert 30 mpg to L/100km
	mpg30 := 30.0
	l100, _ := converter_utils.ConvertFuelConsumption(mpg30, 
		converter_utils.MilesPerGallonUS, converter_utils.LitersPer100km)
	fmt.Printf("30 mpg (US) ≈ %.2f L/100km\n", l100)
	
	fmt.Println()
	
	// ============================================================
	// Parsing Examples
	// ============================================================
	fmt.Println("--- Parsing ---")
	
	// Parse length string
	m, _ := converter_utils.ParseLength("1.5 mi")
	fmt.Printf("ParseLength(\"1.5 mi\") = %.2f meters\n", m)
	
	// Parse weight string
	kg, _ := converter_utils.ParseWeight("100 lb")
	fmt.Printf("ParseWeight(\"100 lb\") = %.4f kg\n", kg)
	
	// Parse temperature string
	c, _ := converter_utils.ParseTemperature("212 F")
	fmt.Printf("ParseTemperature(\"212 F\") = %.2f°C\n", c)
	
	// Parse duration string
	s, _ := converter_utils.ParseDuration("2.5 h")
	fmt.Printf("ParseDuration(\"2.5 h\") = %.0f seconds\n", s)
	
	// Parse data string
	b, _ := converter_utils.ParseData("10 MB")
	fmt.Printf("ParseData(\"10 MB\") = %.0f bytes\n", b)
	
	fmt.Println()
	
	// ============================================================
	// Smart Formatting Examples
	// ============================================================
	fmt.Println("--- Smart Formatting ---")
	
	// Smart duration formatting
	fmt.Println("Smart duration formatting:")
	fmt.Printf("0.000001 seconds: %s\n", converter_utils.SmartFormatDuration(0.000001))
	fmt.Printf("0.5 seconds: %s\n", converter_utils.SmartFormatDuration(0.5))
	fmt.Printf("30 seconds: %s\n", converter_utils.SmartFormatDuration(30))
	fmt.Printf("90 seconds: %s\n", converter_utils.SmartFormatDuration(90))
	fmt.Printf("3600 seconds: %s\n", converter_utils.SmartFormatDuration(3600))
	fmt.Printf("86400 seconds: %s\n", converter_utils.SmartFormatDuration(86400))
	
	fmt.Println()
	
	// Number formatting with commas
	fmt.Println("Number formatting:")
	fmt.Printf("1000: %s\n", converter_utils.FormatWithCommas(1000, 0))
	fmt.Printf("1234567.89: %s\n", converter_utils.FormatWithCommas(1234567.89, 2))
	fmt.Printf("-1234567.89: %s\n", converter_utils.FormatWithCommas(-1234567.89, 2))
	
	fmt.Println()
	
	// ============================================================
	// Generic Converter Examples
	// ============================================================
	fmt.Println("--- Generic Converter ---")
	
	// Using NewConverter for fluent conversions
	val := converter_utils.NewConverter(100)
	
	fmt.Printf("100 meters = %.2f km\n", val.AsLength(converter_utils.Meter).Kilometers())
	fmt.Printf("100 kg = %.2f lb\n", val.AsWeight(converter_utils.Kilogram).Pounds())
	fmt.Printf("100°C = %.1f°F\n", val.AsTemperature(converter_utils.Celsius).Fahrenheit())
	fmt.Printf("100 MB = %.2f GB\n", val.AsData(converter_utils.Megabyte).Gigabytes())
	
	fmt.Println()
	fmt.Println("=== All Examples Completed ===")
}