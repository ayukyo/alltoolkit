' TemperatureUtils Examples - Complete Usage Demonstration
' This file shows all features of the TemperatureUtils library

Imports System
Imports TemperatureUtils

Module TemperatureUtilsExamples

    Sub Main()
        Console.WriteLine("=" & New String("="c, 60))
        Console.WriteLine("TemperatureUtils - Complete Usage Examples")
        Console.WriteLine("=" & New String("="c, 60))
        Console.WriteLine()

        ' Example 1: Basic Temperature Conversion
        Console.WriteLine("--- Example 1: Basic Temperature Conversion ---")
        BasicConversionExample()
        Console.WriteLine()

        ' Example 2: Temperature Struct Operations
        Console.WriteLine("--- Example 2: Temperature Struct Operations ---")
        TemperatureStructExample()
        Console.WriteLine()

        ' Example 3: Parsing Temperature Strings
        Console.WriteLine("--- Example 3: Parsing Temperature Strings ---")
        ParseExample()
        Console.WriteLine()

        ' Example 4: Temperature Validation
        Console.WriteLine("--- Example 4: Temperature Validation ---")
        ValidationExample()
        Console.WriteLine()

        ' Example 5: Temperature Categories
        Console.WriteLine("--- Example 5: Temperature Categories ---")
        CategoriesExample()
        Console.WriteLine()

        ' Example 6: Heat Index Calculation
        Console.WriteLine("--- Example 6: Heat Index Calculation ---")
        HeatIndexExample()
        Console.WriteLine()

        ' Example 7: Wind Chill Calculation
        Console.WriteLine("--- Example 7: Wind Chill Calculation ---")
        WindChillExample()
        Console.WriteLine()

        ' Example 8: Dew Point and Humidity
        Console.WriteLine("--- Example 8: Dew Point and Humidity ---")
        DewPointExample()
        Console.WriteLine()

        ' Example 9: Temperature Statistics
        Console.WriteLine("--- Example 9: Temperature Statistics ---")
        StatisticsExample()
        Console.WriteLine()

        ' Example 10: Temperature Lookup Tables
        Console.WriteLine("--- Example 10: Temperature Lookup Tables ---")
        LookupTableExample()
        Console.WriteLine()

        ' Example 11: Practical Weather Application
        Console.WriteLine("--- Example 11: Practical Weather Application ---")
        WeatherAppExample()
        Console.WriteLine()

        ' Example 12: Cooking Temperature Guide
        Console.WriteLine("--- Example 12: Cooking Temperature Guide ---")
        CookingExample()
        Console.WriteLine()

        Console.WriteLine("All examples completed!")
    End Sub

    Sub BasicConversionExample()
        ' Convert between temperature scales
        Dim celsius = 25.0
        Dim fahrenheit = TemperatureConverter.CelsiusToFahrenheit(celsius)
        Dim kelvin = TemperatureConverter.CelsiusToKelvin(celsius)
        Dim rankine = TemperatureConverter.CelsiusToRankine(celsius)

        Console.WriteLine($"  {celsius}°C is:")
        Console.WriteLine($"    {fahrenheit:F2}°F (Fahrenheit)")
        Console.WriteLine($"    {kelvin:F2}K (Kelvin)")
        Console.WriteLine($"    {rankine:F2}°R (Rankine)")
        Console.WriteLine()

        ' Convert back
        Console.WriteLine($"  {fahrenheit}°F is {TemperatureConverter.FahrenheitToCelsius(fahrenheit):F2}°C")
        Console.WriteLine($"  {kelvin}K is {TemperatureConverter.KelvinToCelsius(kelvin):F2}°C")
        Console.WriteLine()

        ' Use generic Convert method
        Dim boilingF = TemperatureConverter.Convert(100, TemperatureUnit.Celsius, TemperatureUnit.Fahrenheit)
        Console.WriteLine($"  100°C = {boilingF:F2}°F (using Convert method)")
        Console.WriteLine()

        ' Batch conversion
        Dim temps = {0.0, 20.0, 37.0, 100.0}
        Dim converted = TemperatureConverter.ConvertBatch(temps, TemperatureUnit.Celsius, TemperatureUnit.Fahrenheit)
        Console.WriteLine("  Batch conversion (Celsius to Fahrenheit):")
        For i As Integer = 0 To temps.Length - 1
            Console.WriteLine($"    {temps(i)}°C = {converted(i):F2}°F")
        Next
    End Sub

    Sub TemperatureStructExample()
        ' Create temperatures using factory methods
        Dim freezing = Temperature.FromCelsius(0)
        Dim bodyTemp = Temperature.FromFahrenheit(98.6)
        Dim roomTemp = Temperature.FromKelvin(293.15)

        Console.WriteLine($"  Freezing: {freezing.Format()}")
        Console.WriteLine($"  Body temp: {bodyTemp.Format()}")
        Console.WriteLine($"  Room temp: {roomTemp.Format()}")
        Console.WriteLine()

        ' Convert to other units
        Console.WriteLine($"  Freezing in all units: {freezing.FormatAll()}")
        Console.WriteLine()

        ' Temperature arithmetic
        Dim warm = Temperature.FromCelsius(10)
        Dim hot = warm + Temperature.FromCelsius(30)
        Dim diff = hot - warm
        Dim doubled = warm * 2
        Dim half = hot / 2

        Console.WriteLine($"  {warm.Format()} + 30°C = {hot.Format()}")
        Console.WriteLine($"  {hot.Format()} - {warm.Format()} = {diff.Format()}")
        Console.WriteLine($"  {warm.Format()} × 2 = {doubled.Format()}")
        Console.WriteLine($"  {hot.Format()} ÷ 2 = {half.Format()}")
        Console.WriteLine()

        ' Comparison operators
        Dim t1 = Temperature.FromCelsius(20)
        Dim t2 = Temperature.FromFahrenheit(68) ' Same as 20°C

        Console.WriteLine($"  {t1.Format()} = {t2.Format()}: {t1 = t2}")
        Console.WriteLine($"  {t1.Format()} < {Temperature.FromCelsius(30).Format()}: {t1 < Temperature.FromCelsius(30)}")
        Console.WriteLine($"  {t1.Format()} > {Temperature.FromCelsius(10).Format()}: {t1 > Temperature.FromCelsius(10)}")
        Console.WriteLine()

        ' Built-in checks
        Dim cold = Temperature.FromCelsius(-5)
        Dim boiling = Temperature.FromCelsius(100)
        Dim comfy = Temperature.FromCelsius(22)

        Console.WriteLine($"  {cold.Format()} is freezing: {cold.IsFreezing()}")
        Console.WriteLine($"  {boiling.Format()} is boiling: {boiling.IsBoiling()}")
        Console.WriteLine($"  {comfy.Format()} is comfortable: {comfy.IsComfortable()}")
        Console.WriteLine($"  {cold.Format()} is valid (above absolute zero): {cold.IsValid()}")
        Console.WriteLine($"  {Temperature.FromCelsius(-300).Format()} is valid: {Temperature.FromCelsius(-300).IsValid()}")
    End Sub

    Sub ParseExample()
        ' Parse temperature strings
        Dim temps = {"25°C", "77°F", "300K", "491.67°R", "-40C", "100F"}

        Console.WriteLine("  Parsing temperature strings:")
        For Each tempStr In temps
            Dim temp = TemperatureConverter.Parse(tempStr)
            Console.WriteLine($"    ""{tempStr}"" → {temp.Format()} ({temp.ToCelsius():F2}°C)")
        Next
        Console.WriteLine()

        ' TryParse for safe parsing
        Dim inputs = {"25°C", "invalid", "100F"}
        Console.WriteLine("  Using TryParse:")
        For Each input In inputs
            Dim temp As Temperature
            If TemperatureConverter.TryParse(input, temp) Then
                Console.WriteLine($"    ""{input}"" → {temp.Format()}")
            Else
                Console.WriteLine($"    ""{input}"" → Invalid format")
            End If
        Next
    End Sub

    Sub ValidationExample()
        ' Absolute zero values
        Console.WriteLine("  Absolute zero values:")
        Console.WriteLine($"    Celsius: {TemperatureValidator.AbsoluteZeroCelsius}°C")
        Console.WriteLine($"    Fahrenheit: {TemperatureValidator.AbsoluteZeroFahrenheit}°F")
        Console.WriteLine($"    Kelvin: {TemperatureValidator.AbsoluteZeroKelvin}K")
        Console.WriteLine($"    Rankine: {TemperatureValidator.AbsoluteZeroRankine}°R")
        Console.WriteLine()

        ' Validate temperatures
        Dim temps = {
            (0, TemperatureUnit.Celsius),
            (-273.15, TemperatureUnit.Celsius),
            (-300, TemperatureUnit.Celsius),
            (0, TemperatureUnit.Kelvin),
            (-1, TemperatureUnit.Kelvin)
        }

        Console.WriteLine("  Temperature validation:")
        For Each t In temps
            Dim isValid = TemperatureValidator.IsValidTemperature(t.Item1, t.Item2)
            Console.WriteLine($"    {t.Item1} {t.Item2}: {(If(isValid, "Valid", "Below absolute zero!"))}")
        Next
        Console.WriteLine()

        ' Check if temperature is in range
        Console.WriteLine("  Range checking (15-25°C):")
        Dim testTemps = {10, 20, 30}
        For Each t In testTemps
            Dim inRange = TemperatureValidator.IsInRange(t, TemperatureUnit.Celsius, 15, 25)
            Console.WriteLine($"    {t}°C: {(If(inRange, "In range", "Out of range"))}")
        Next
    End Sub

    Sub CategoriesExample()
        ' Get temperature categories
        Dim temps = {-60, -30, -10, 5, 15, 22, 28, 33, 38, 45, 55}

        Console.WriteLine("  Temperature categories:")
        Console.WriteLine("  " & "Temp".PadLeft(8) & " | Category")
        Console.WriteLine("  " & New String("-"c, 8) & "-+-" & New String("-"c, 25))
        For Each t In temps
            Dim category = TemperatureCategories.GetCategory(t)
            Console.WriteLine($"  {t,8}°C | {category}")
        Next
        Console.WriteLine()

        ' Clothing recommendations
        Console.WriteLine("  Clothing recommendations:")
        Dim clothingTemps = {-25, -5, 8, 15, 22, 30, 40}
        For Each t In clothingTemps
            Console.WriteLine($"    {t}°C: {TemperatureCategories.GetClothingRecommendation(t)}")
        Next
        Console.WriteLine()

        ' Activity recommendations
        Console.WriteLine("  Activity recommendations:")
        Dim activityTemps = {-30, -5, 15, 22, 32, 40}
        For Each t In activityTemps
            Console.WriteLine($"    {t}°C: {TemperatureCategories.GetActivityRecommendation(t)}")
        Next
        Console.WriteLine()

        ' Risk levels
        Console.WriteLine("  Risk levels:")
        Dim riskTemps = {-50, -25, -5, 10, 25, 38, 55}
        For Each t In riskTemps
            Console.WriteLine($"    {t}°C: {TemperatureCategories.GetRiskLevel(t)} risk")
        Next
    End Sub

    Sub HeatIndexExample()
        Console.WriteLine("  Heat Index (feels-like temperature in hot weather):")
        Console.WriteLine("  " & "Temp".PadLeft(8) & " | " & "Humidity".PadLeft(8) & " | " & "Heat Index".PadLeft(12))
        Console.WriteLine("  " & New String("-"c, 8) & "-+-" & New String("-"c, 8) & "-+-" & New String("-"c, 12))

        Dim conditions = {
            (80, 40),
            (85, 50),
            (90, 60),
            (95, 70),
            (100, 80)
        }

        For Each c In conditions
            Dim heatIndex = ThermalIndices.CalculateHeatIndex(c.Item1, c.Item2)
            Console.WriteLine($"  {c.Item1,8}°F | {c.Item2,8}% | {heatIndex,12:F1}°F")
        Next
        Console.WriteLine()

        ' Heat index in Celsius
        Console.WriteLine("  Heat Index (Celsius):")
        Dim celsiusConditions = {
            (30, 50),
            (35, 60),
            (40, 70)
        }

        For Each c In celsiusConditions
            Dim heatIndex = ThermalIndices.CalculateHeatIndexCelsius(c.Item1, c.Item2)
            Console.WriteLine($"    {c.Item1}°C at {c.Item2}% humidity feels like {heatIndex:F1}°C")
        Next
    End Sub

    Sub WindChillExample()
        Console.WriteLine("  Wind Chill (feels-like temperature in cold weather):")
        Console.WriteLine("  " & "Temp".PadLeft(8) & " | " & "Wind".PadLeft(8) & " | " & "Wind Chill".PadLeft(12))
        Console.WriteLine("  " & New String("-"c, 8) & "-+-" & New String("-"c, 8) & "-+-" & New String("-"c, 12))

        Dim conditions = {
            (30, 5),
            (20, 10),
            (10, 15),
            (0, 20),
            (-10, 25)
        }

        For Each c In conditions
            Dim windChill = ThermalIndices.CalculateWindChill(c.Item1, c.Item2)
            Console.WriteLine($"  {c.Item1,8}°F | {c.Item2,8} mph | {windChill,12:F1}°F")
        Next
        Console.WriteLine()

        ' Wind chill in metric
        Console.WriteLine("  Wind Chill (Metric):")
        Dim metricConditions = {
            (0, 10),
            (-10, 20),
            (-20, 30)
        }

        For Each c In metricConditions
            Dim windChill = ThermalIndices.CalculateWindChillCelsius(c.Item1, c.Item2)
            Console.WriteLine($"    {c.Item1}°C with {c.Item2} km/h wind feels like {windChill:F1}°C")
        Next
    End Sub

    Sub DewPointExample()
        ' Dew point calculation
        Console.WriteLine("  Dew Point (temperature where air becomes saturated):")
        Console.WriteLine("  " & "Temp".PadLeft(8) & " | " & "Humidity".PadLeft(8) & " | " & "Dew Point".PadLeft(10))
        Console.WriteLine("  " & New String("-"c, 8) & "-+-" & New String("-"c, 8) & "-+-" & New String("-"c, 10))

        Dim conditions = {
            (20, 30),
            (20, 50),
            (20, 70),
            (30, 50),
            (30, 90)
        }

        For Each c In conditions
            Dim dewPoint = ThermalIndices.CalculateDewPoint(c.Item1, c.Item2)
            Console.WriteLine($"  {c.Item1,8}°C | {c.Item2,8}% | {dewPoint,10:F1}°C")
        Next
        Console.WriteLine()

        ' Wet bulb temperature
        Console.WriteLine("  Wet Bulb Temperature:")
        Dim wbConditions = {
            (25, 30),
            (25, 50),
            (25, 70),
            (30, 60)
        }

        For Each c In wbConditions
            Dim wetBulb = ThermalIndices.CalculateWetBulbTemperature(c.Item1, c.Item2)
            Console.WriteLine($"    {c.Item1}°C at {c.Item2}% humidity: {wetBulb:F1}°C wet bulb")
        Next
        Console.WriteLine()

        ' Humidex
        Console.WriteLine("  Humidex (Canadian heat index):")
        Dim humidexConditions = {
            (30, 20),
            (30, 25),
            (35, 25)
        }

        For Each c In humidexConditions
            Dim humidex = ThermalIndices.CalculateHumidex(c.Item1, c.Item2)
            Console.WriteLine($"    {c.Item1}°C with {c.Item2}°C dew point: humidex {humidex:F1}")
        Next
        Console.WriteLine()

        ' Heat stress categories
        Console.WriteLine("  Heat Stress Categories (WBGT):")
        Dim wbgtValues = {20, 26, 29, 31, 34}
        For Each wbgt In wbgtValues
            Console.WriteLine($"    WBGT {wbgt}°C: {ThermalIndices.GetHeatStressCategory(wbgt)}")
        Next
    End Sub

    Sub StatisticsExample()
        ' Create sample temperature data
        Dim hourlyTemps = {
            Temperature.FromCelsius(15),
            Temperature.FromCelsius(14),
            Temperature.FromCelsius(13),
            Temperature.FromCelsius(12),
            Temperature.FromCelsius(13),
            Temperature.FromCelsius(15),
            Temperature.FromCelsius(18),
            Temperature.FromCelsius(22),
            Temperature.FromCelsius(25),
            Temperature.FromCelsius(27),
            Temperature.FromCelsius(28),
            Temperature.FromCelsius(27)
        }

        Console.WriteLine("  Temperature statistics (hourly data):")
        Console.WriteLine($"    Average: {TemperatureStatistics.Average(hourlyTemps).Format()}")
        Console.WriteLine($"    Median: {TemperatureStatistics.Median(hourlyTemps).Format()}")
        Console.WriteLine($"    Minimum: {TemperatureStatistics.Minimum(hourlyTemps).Format()}")
        Console.WriteLine($"    Maximum: {TemperatureStatistics.Maximum(hourlyTemps).Format()}")
        Console.WriteLine($"    Std Dev: {TemperatureStatistics.StandardDeviation(hourlyTemps):F2}°C")
        Console.WriteLine()

        ' Temperature range
        Dim range = TemperatureStatistics.Range(hourlyTemps)
        Console.WriteLine($"    Range: {range.min.Format()} to {range.max.Format()}")
        Console.WriteLine()

        ' Count temperatures in range
        Dim comfortableCount = TemperatureStatistics.CountInRange(hourlyTemps, 18, 24)
        Console.WriteLine($"    Hours in comfort zone (18-24°C): {comfortableCount}")
    End Sub

    Sub LookupTableExample()
        ' Generate conversion table
        Console.WriteLine("  Celsius to Fahrenheit conversion table:")
        Dim table = TemperatureLookupTable.GenerateTable(
            TemperatureUnit.Celsius,
            TemperatureUnit.Fahrenheit,
            0, 100, 10)

        For Each kvp In table
            Console.WriteLine($"    {kvp.Key}°C = {kvp.Value}°F")
        Next
        Console.WriteLine()

        ' Reference points
        Console.WriteLine("  Temperature Reference Points:")
        Dim refs = TemperatureLookupTable.GetReferencePoints()
        For Each kvp In refs
            Console.WriteLine($"    {kvp.Key}: {kvp.Value.FormatAll(1)}")
        Next
    End Sub

    Sub WeatherAppExample()
        ' Simulate a weather app scenario
        Console.WriteLine("  Weather Report for Example City:")
        Console.WriteLine()

        Dim currentTemp = Temperature.FromCelsius(28)
        Dim feelsLike = Temperature.FromCelsius(32)
        Dim humidity = 65
        Dim windSpeed = 15 ' km/h

        Console.WriteLine($"  Current Temperature: {currentTemp.Format()}")
        Console.WriteLine($"  Feels Like: {feelsLike.Format()}")
        Console.WriteLine($"  Humidity: {humidity}%")
        Console.WriteLine($"  Wind: {windSpeed} km/h")
        Console.WriteLine()

        ' Calculate thermal indices
        Dim heatIndex = ThermalIndices.CalculateHeatIndexCelsius(currentTemp.ToCelsius(), humidity)
        Dim windChill = ThermalIndices.CalculateWindChillCelsius(currentTemp.ToCelsius(), windSpeed)
        Dim dewPoint = ThermalIndices.CalculateDewPoint(currentTemp.ToCelsius(), humidity)
        Dim wetBulb = ThermalIndices.CalculateWetBulbTemperature(currentTemp.ToCelsius(), humidity)

        Console.WriteLine("  Thermal Indices:")
        Console.WriteLine($"    Heat Index: {heatIndex:F1}°C")
        Console.WriteLine($"    Dew Point: {dewPoint:F1}°C")
        Console.WriteLine($"    Wet Bulb: {wetBulb:F1}°C")
        Console.WriteLine()

        ' Get category and recommendations
        Console.WriteLine($"  Category: {currentTemp.GetCategory()}")
        Console.WriteLine($"  Risk Level: {TemperatureCategories.GetRiskLevel(currentTemp.ToCelsius())}")
        Console.WriteLine($"  Clothing: {TemperatureCategories.GetClothingRecommendation(currentTemp.ToCelsius())}")
        Console.WriteLine($"  Activity: {TemperatureCategories.GetActivityRecommendation(currentTemp.ToCelsius())}")
    End Sub

    Sub CookingExample()
        ' Cooking temperature reference
        Console.WriteLine("  Cooking Temperature Guide:")
        Console.WriteLine()

        Dim cookingTemps = {
            ("Rare Beef", Temperature.FromCelsius(52)),
            ("Medium Rare Beef", Temperature.FromCelsius(57)),
            ("Medium Beef", Temperature.FromCelsius(63)),
            ("Well Done Beef", Temperature.FromCelsius(71)),
            ("Poultry (Safe)", Temperature.FromCelsius(74)),
            ("Pork (Safe)", Temperature.FromCelsius(71)),
            ("Fish (Safe)", Temperature.FromCelsius(63)),
            ("Bread (Internal)", Temperature.FromCelsius(93)),
            ("Candy - Soft Ball", Temperature.FromCelsius(112)),
            ("Candy - Hard Crack", Temperature.FromCelsius(149))
        }

        Console.WriteLine("  " & "Item".PadRight(20) & " | Celsius | Fahrenheit | Kelvin")
        Console.WriteLine("  " & New String("-"c, 20) & "-+---------+------------+--------")

        For Each item In cookingTemps
            Console.WriteLine($"  {item.Item1.PadRight(20)} | {item.Item2.ToCelsius(),7:F0}°C | {item.Item2.ToFahrenheit(),10:F0}°F | {item.Item2.ToKelvin(),7:F0}K")
        Next
        Console.WriteLine()

        ' Oven temperature conversion
        Console.WriteLine("  Common Oven Temperatures:")
        Dim ovenTemps = {
            ("Very Slow", Temperature.FromCelsius(120)),
            ("Slow", Temperature.FromCelsius(150)),
            ("Moderate", Temperature.FromCelsius(180)),
            ("Hot", Temperature.FromCelsius(200)),
            ("Very Hot", Temperature.FromCelsius(220))
        }

        For Each oven In ovenTemps
            Console.WriteLine($"    {oven.Item1}: {oven.Item2.Format(0)} ({oven.Item2.ToFahrenheit():F0}°F)")
        Next
    End Sub

End Module