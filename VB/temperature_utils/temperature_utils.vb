' TemperatureUtils - Complete Temperature Conversion and Calculation Library
' Zero external dependencies - Pure VB.NET implementation
' Supports Celsius, Fahrenheit, Kelvin, Rankine conversion and thermal indices

Imports System

Namespace TemperatureUtils

    ''' <summary>
    ''' Temperature unit enumeration
    ''' </summary>
    Public Enum TemperatureUnit
        Celsius
        Fahrenheit
        Kelvin
        Rankine
    End Enum

    ''' <summary>
    ''' Temperature value with unit
    ''' </summary>
    Public Structure Temperature
        Public ReadOnly Value As Double
        Public ReadOnly Unit As TemperatureUnit

        Public Sub New(value As Double, unit As TemperatureUnit)
            Me.Value = value
            Me.Unit = unit
        End Sub

        ''' <summary>
        ''' Create temperature in Celsius
        ''' </summary>
        Public Shared Function FromCelsius(value As Double) As Temperature
            Return New Temperature(value, TemperatureUnit.Celsius)
        End Function

        ''' <summary>
        ''' Create temperature in Fahrenheit
        ''' </summary>
        Public Shared Function FromFahrenheit(value As Double) As Temperature
            Return New Temperature(value, TemperatureUnit.Fahrenheit)
        End Function

        ''' <summary>
        ''' Create temperature in Kelvin
        ''' </summary>
        Public Shared Function FromKelvin(value As Double) As Temperature
            Return New Temperature(value, TemperatureUnit.Kelvin)
        End Function

        ''' <summary>
        ''' Create temperature in Rankine
        ''' </summary>
        Public Shared Function FromRankine(value As Double) As Temperature
            Return New Temperature(value, TemperatureUnit.Rankine)
        End Function

        ''' <summary>
        ''' Convert to Celsius
        ''' </summary>
        Public Function ToCelsius() As Double
            Return TemperatureConverter.Convert(Value, Unit, TemperatureUnit.Celsius)
        End Function

        ''' <summary>
        ''' Convert to Fahrenheit
        ''' </summary>
        Public Function ToFahrenheit() As Double
            Return TemperatureConverter.Convert(Value, Unit, TemperatureUnit.Fahrenheit)
        End Function

        ''' <summary>
        ''' Convert to Kelvin
        ''' </summary>
        Public Function ToKelvin() As Double
            Return TemperatureConverter.Convert(Value, Unit, TemperatureUnit.Kelvin)
        End Function

        ''' <summary>
        ''' Convert to Rankine
        ''' </summary>
        Public Function ToRankine() As Double
            Return TemperatureConverter.Convert(Value, Unit, TemperatureUnit.Rankine)
        End Function

        ''' <summary>
        ''' Convert to specified unit
        ''' </summary>
        Public Function ConvertTo(targetUnit As TemperatureUnit) As Temperature
            Dim convertedValue = TemperatureConverter.Convert(Value, Unit, targetUnit)
            Return New Temperature(convertedValue, targetUnit)
        End Function

        ''' <summary>
        ''' Check if temperature is below absolute zero
        ''' </summary>
        Public Function IsValid() As Boolean
            Return TemperatureValidator.IsValidTemperature(Value, Unit)
        End Function

        ''' <summary>
        ''' Get temperature in human-readable format
        ''' </summary>
        Public Function Format(Optional decimals As Integer = 1) As String
            Return TemperatureFormatter.Format(Value, Unit, decimals)
        End Function

        ''' <summary>
        ''' Get temperature category
        ''' </summary>
        Public Function GetCategory() As String
            Dim celsius = ToCelsius()
            Return TemperatureCategories.GetCategory(celsius)
        End Function

        ''' <summary>
        ''' Check if temperature is freezing
        ''' </summary>
        Public Function IsFreezing() As Boolean
            Return ToCelsius() <= 0
        End Function

        ''' <summary>
        ''' Check if temperature is boiling
        ''' </summary>
        Public Function IsBoiling() As Boolean
            Return ToCelsius() >= 100
        End Function

        ''' <summary>
        ''' Check if temperature is comfortable for humans
        ''' </summary>
        Public Function IsComfortable() As Boolean
            Dim celsius = ToCelsius()
            Return celsius >= 18 AndAlso celsius <= 24
        End Function

        Public Overrides Function ToString() As String
            Return Format()
        End Function

        ' Operator overloads
        Public Shared Operator +(t1 As Temperature, t2 As Temperature) As Temperature
            If t1.Unit <> t2.Unit Then
                t2 = t2.ConvertTo(t1.Unit)
            End If
            Return New Temperature(t1.Value + t2.Value, t1.Unit)
        End Operator

        Public Shared Operator -(t1 As Temperature, t2 As Temperature) As Temperature
            If t1.Unit <> t2.Unit Then
                t2 = t2.ConvertTo(t1.Unit)
            End If
            Return New Temperature(t1.Value - t2.Value, t1.Unit)
        End Operator

        Public Shared Operator *(t As Temperature, factor As Double) As Temperature
            Return New Temperature(t.Value * factor, t.Unit)
        End Operator

        Public Shared Operator /(t As Temperature, divisor As Double) As Temperature
            Return New Temperature(t.Value / divisor, t.Unit)
        End Operator

        Public Shared Operator =(t1 As Temperature, t2 As Temperature) As Boolean
            Return Math.Abs(t1.ToKelvin() - t2.ToKelvin()) < 0.0001
        End Operator

        Public Shared Operator <>(t1 As Temperature, t2 As Temperature) As Boolean
            Return Not (t1 = t2)
        End Operator

        Public Shared Operator <(t1 As Temperature, t2 As Temperature) As Boolean
            Return t1.ToKelvin() < t2.ToKelvin()
        End Operator

        Public Shared Operator >(t1 As Temperature, t2 As Temperature) As Boolean
            Return t1.ToKelvin() > t2.ToKelvin()
        End Operator

        Public Shared Operator <=(t1 As Temperature, t2 As Temperature) As Boolean
            Return t1.ToKelvin() <= t2.ToKelvin()
        End Operator

        Public Shared Operator >=(t1 As Temperature, t2 As Temperature) As Boolean
            Return t1.ToKelvin() >= t2.ToKelvin()
        End Operator
    End Structure

    ''' <summary>
    ''' Temperature conversion utilities
    ''' </summary>
    Public Class TemperatureConverter

        ' Conversion constants
        Private Const CelsiusToFahrenheitFactor As Double = 9.0 / 5.0
        Private Const FahrenheitToCelsiusFactor As Double = 5.0 / 9.0
        Private Const CelsiusOffset As Double = 32.0
        Private Const AbsoluteZeroCelsius As Double = -273.15
        Private Const AbsoluteZeroFahrenheit As Double = -459.67

        ''' <summary>
        ''' Convert temperature between units
        ''' </summary>
        Public Shared Function Convert(value As Double, fromUnit As TemperatureUnit, toUnit As TemperatureUnit) As Double
            If fromUnit = toUnit Then Return value

            ' First convert to Celsius as intermediate
            Dim celsius As Double
            Select Case fromUnit
                Case TemperatureUnit.Celsius
                    celsius = value
                Case TemperatureUnit.Fahrenheit
                    celsius = FahrenheitToCelsius(value)
                Case TemperatureUnit.Kelvin
                    celsius = KelvinToCelsius(value)
                Case TemperatureUnit.Rankine
                    celsius = RankineToCelsius(value)
                Case Else
                    Throw New ArgumentException($"Unknown unit: {fromUnit}")
            End Select

            ' Then convert from Celsius to target unit
            Select Case toUnit
                Case TemperatureUnit.Celsius
                    Return celsius
                Case TemperatureUnit.Fahrenheit
                    Return CelsiusToFahrenheit(celsius)
                Case TemperatureUnit.Kelvin
                    Return CelsiusToKelvin(celsius)
                Case TemperatureUnit.Rankine
                    Return CelsiusToRankine(celsius)
                Case Else
                    Throw New ArgumentException($"Unknown unit: {toUnit}")
            End Select
        End Function

        ''' <summary>
        ''' Convert Celsius to Fahrenheit
        ''' </summary>
        Public Shared Function CelsiusToFahrenheit(celsius As Double) As Double
            Return celsius * CelsiusToFahrenheitFactor + CelsiusOffset
        End Function

        ''' <summary>
        ''' Convert Fahrenheit to Celsius
        ''' </summary>
        Public Shared Function FahrenheitToCelsius(fahrenheit As Double) As Double
            Return (fahrenheit - CelsiusOffset) * FahrenheitToCelsiusFactor
        End Function

        ''' <summary>
        ''' Convert Celsius to Kelvin
        ''' </summary>
        Public Shared Function CelsiusToKelvin(celsius As Double) As Double
            Return celsius - AbsoluteZeroCelsius
        End Function

        ''' <summary>
        ''' Convert Kelvin to Celsius
        ''' </summary>
        Public Shared Function KelvinToCelsius(kelvin As Double) As Double
            Return kelvin + AbsoluteZeroCelsius
        End Function

        ''' <summary>
        ''' Convert Fahrenheit to Kelvin
        ''' </summary>
        Public Shared Function FahrenheitToKelvin(fahrenheit As Double) As Double
            Return CelsiusToKelvin(FahrenheitToCelsius(fahrenheit))
        End Function

        ''' <summary>
        ''' Convert Kelvin to Fahrenheit
        ''' </summary>
        Public Shared Function KelvinToFahrenheit(kelvin As Double) As Double
            Return CelsiusToFahrenheit(KelvinToCelsius(kelvin))
        End Function

        ''' <summary>
        ''' Convert Fahrenheit to Rankine
        ''' </summary>
        Public Shared Function FahrenheitToRankine(fahrenheit As Double) As Double
            Return fahrenheit - AbsoluteZeroFahrenheit
        End Function

        ''' <summary>
        ''' Convert Rankine to Fahrenheit
        ''' </summary>
        Public Shared Function RankineToFahrenheit(rankine As Double) As Double
            Return rankine + AbsoluteZeroFahrenheit
        End Function

        ''' <summary>
        ''' Convert Celsius to Rankine
        ''' </summary>
        Public Shared Function CelsiusToRankine(celsius As Double) As Double
            Return FahrenheitToRankine(CelsiusToFahrenheit(celsius))
        End Function

        ''' <summary>
        ''' Convert Rankine to Celsius
        ''' </summary>
        Public Shared Function RankineToCelsius(rankine As Double) As Double
            Return FahrenheitToCelsius(RankineToFahrenheit(rankine))
        End Function

        ''' <summary>
        ''' Convert Kelvin to Rankine
        ''' </summary>
        Public Shared Function KelvinToRankine(kelvin As Double) As Double
            Return kelvin * CelsiusToFahrenheitFactor
        End Function

        ''' <summary>
        ''' Convert Rankine to Kelvin
        ''' </summary>
        Public Shared Function RankineToKelvin(rankine As Double) As Double
            Return rankine * FahrenheitToCelsiusFactor
        End Function

        ''' <summary>
        ''' Batch convert multiple values
        ''' </summary>
        Public Shared Function ConvertBatch(values As Double(), fromUnit As TemperatureUnit, toUnit As TemperatureUnit) As Double()
            Dim results(values.Length - 1) As Double
            For i As Integer = 0 To values.Length - 1
                results(i) = Convert(values(i), fromUnit, toUnit)
            Next
            Return results
        End Function

        ''' <summary>
        ''' Parse temperature string (e.g., "25°C", "77°F", "300K")
        ''' </summary>
        Public Shared Function Parse(tempString As String) As Temperature
            Dim trimmed = tempString.Trim()
            Dim value As Double
            Dim unit As TemperatureUnit

            If trimmed.EndsWith("°C") OrElse trimmed.EndsWith("C") Then
                value = Double.Parse(trimmed.Replace("°C", "").Replace("C", "").Trim())
                unit = TemperatureUnit.Celsius
            ElseIf trimmed.EndsWith("°F") OrElse trimmed.EndsWith("F") Then
                value = Double.Parse(trimmed.Replace("°F", "").Replace("F", "").Trim())
                unit = TemperatureUnit.Fahrenheit
            ElseIf trimmed.EndsWith("K") Then
                value = Double.Parse(trimmed.Replace("K", "").Trim())
                unit = TemperatureUnit.Kelvin
            ElseIf trimmed.EndsWith("°R") OrElse trimmed.EndsWith("R") Then
                value = Double.Parse(trimmed.Replace("°R", "").Replace("R", "").Trim())
                unit = TemperatureUnit.Rankine
            Else
                Throw New FormatException($"Cannot parse temperature: {tempString}")
            End If

            Return New Temperature(value, unit)
        End Function

        ''' <summary>
        ''' Try to parse temperature string
        ''' </summary>
        Public Shared Function TryParse(tempString As String, ByRef result As Temperature) As Boolean
            Try
                result = Parse(tempString)
                Return True
            Catch
                result = Nothing
                Return False
            End Try
        End Function
    End Class

    ''' <summary>
    ''' Temperature validation utilities
    ''' </summary>
    Public Class TemperatureValidator

        ' Absolute zero values
        Public Shared ReadOnly AbsoluteZeroCelsius As Double = -273.15
        Public Shared ReadOnly AbsoluteZeroFahrenheit As Double = -459.67
        Public Shared ReadOnly AbsoluteZeroKelvin As Double = 0.0
        Public Shared ReadOnly AbsoluteZeroRankine As Double = 0.0

        ''' <summary>
        ''' Check if temperature is above absolute zero
        ''' </summary>
        Public Shared Function IsValidTemperature(value As Double, unit As TemperatureUnit) As Boolean
            Select Case unit
                Case TemperatureUnit.Celsius
                    Return value >= AbsoluteZeroCelsius
                Case TemperatureUnit.Fahrenheit
                    Return value >= AbsoluteZeroFahrenheit
                Case TemperatureUnit.Kelvin
                    Return value >= AbsoluteZeroKelvin
                Case TemperatureUnit.Rankine
                    Return value >= AbsoluteZeroRankine
                Case Else
                    Return False
            End Select
        End Function

        ''' <summary>
        ''' Validate temperature and throw exception if invalid
        ''' </summary>
        Public Shared Sub ValidateTemperature(value As Double, unit As TemperatureUnit)
            If Not IsValidTemperature(value, unit) Then
                Throw New ArgumentOutOfRangeException(
                    $"Temperature {value} {unit} is below absolute zero")
            End If
        End Sub

        ''' <summary>
        ''' Get absolute zero for a unit
        ''' </summary>
        Public Shared Function GetAbsoluteZero(unit As TemperatureUnit) As Double
            Select Case unit
                Case TemperatureUnit.Celsius
                    Return AbsoluteZeroCelsius
                Case TemperatureUnit.Fahrenheit
                    Return AbsoluteZeroFahrenheit
                Case TemperatureUnit.Kelvin
                    Return AbsoluteZeroKelvin
                Case TemperatureUnit.Rankine
                    Return AbsoluteZeroRankine
                Case Else
                    Throw New ArgumentException($"Unknown unit: {unit}")
            End Select
        End Function

        ''' <summary>
        ''' Check if temperature is within a range
        ''' </summary>
        Public Shared Function IsInRange(value As Double, unit As TemperatureUnit, min As Double, max As Double) As Boolean
            Dim kelvin = TemperatureConverter.Convert(value, unit, TemperatureUnit.Kelvin)
            Dim minKelvin = TemperatureConverter.Convert(min, unit, TemperatureUnit.Kelvin)
            Dim maxKelvin = TemperatureConverter.Convert(max, unit, TemperatureUnit.Kelvin)
            Return kelvin >= minKelvin AndAlso kelvin <= maxKelvin
        End Function
    End Class

    ''' <summary>
    ''' Temperature formatting utilities
    ''' </summary>
    Public Class TemperatureFormatter

        Private Shared ReadOnly UnitSymbols As New Dictionary(Of TemperatureUnit, String) From
        {
            {TemperatureUnit.Celsius, "°C"},
            {TemperatureUnit.Fahrenheit, "°F"},
            {TemperatureUnit.Kelvin, "K"},
            {TemperatureUnit.Rankine, "°R"}
        }

        ''' <summary>
        ''' Format temperature with default decimal places
        ''' </summary>
        Public Shared Function Format(value As Double, unit As TemperatureUnit, Optional decimals As Integer = 1) As String
            Dim formatted = Math.Round(value, decimals)
            Return $"{formatted}{UnitSymbols(unit)}"
        End Function

        ''' <summary>
        ''' Format temperature with all units
        ''' </summary>
        Public Shared Function FormatAll(value As Double, unit As TemperatureUnit, Optional decimals As Integer = 1) As String
            Dim parts As New List(Of String)()
            For Each u As TemperatureUnit In [Enum].GetValues(GetType(TemperatureUnit))
                Dim converted = TemperatureConverter.Convert(value, unit, u)
                parts.Add(Format(converted, u, decimals))
            Next
            Return String.Join(" | ", parts)
        End Function

        ''' <summary>
        ''' Format temperature range
        ''' </summary>
        Public Shared Function FormatRange(min As Double, max As Double, unit As TemperatureUnit, Optional decimals As Integer = 1) As String
            Return $"{Format(min, unit, decimals)} - {Format(max, unit, decimals)}"
        End Function

        ''' <summary>
        ''' Format temperature difference
        ''' </summary>
        Public Shared Function FormatDifference(diff As Double, unit As TemperatureUnit, Optional decimals As Integer = 1) As String
            Dim symbol = If(unit = TemperatureUnit.Kelvin, "K", $"°{UnitSymbols(unit).Substring(1)}")
            Return $"{Math.Round(diff, decimals)} {symbol}"
        End Function
    End Class

    ''' <summary>
    ''' Temperature categories and classifications
    ''' </summary>
    Public Class TemperatureCategories

        ''' <summary>
        ''' Get temperature category description
        ''' </summary>
        Public Shared Function GetCategory(celsius As Double) As String
            If celsius < -50 Then Return "Extreme Cold"
            If celsius < -20 Then Return "Severe Cold"
            If celsius < 0 Then Return "Freezing"
            If celsius < 10 Then Return "Cold"
            If celsius < 18 Then Return "Cool"
            If celsius < 24 Then Return "Comfortable"
            If celsius < 30 Then Return "Warm"
            If celsius < 35 Then Return "Hot"
            If celsius < 40 Then Return "Very Hot"
            If celsius < 50 Then Return "Extreme Heat"
            Return "Extreme Danger"
        End Function

        ''' <summary>
        ''' Get clothing recommendation based on temperature
        ''' </summary>
        Public Shared Function GetClothingRecommendation(celsius As Double) As String
            If celsius < -20 Then Return "Heavy winter coat, multiple layers, face protection required"
            If celsius < 0 Then Return "Winter coat, hat, gloves, scarf"
            If celsius < 10 Then Return "Jacket or sweater, long pants"
            If celsius < 18 Then Return "Light jacket or sweater"
            If celsius < 24 Then Return "Comfortable with light clothing"
            If celsius < 30 Then Return "Light, breathable clothing"
            If celsius < 35 Then Return "Very light clothing, sun protection"
            Return "Minimal clothing, stay hydrated, avoid prolonged exposure"
        End Function

        ''' <summary>
        ''' Get activity recommendation based on temperature
        ''' </summary>
        Public Shared Function GetActivityRecommendation(celsius As Double) As String
            If celsius < -20 Then Return "Avoid outdoor activities; dangerous cold conditions"
            If celsius < 0 Then Return "Limit outdoor exposure; indoor activities recommended"
            If celsius < 10 Then Return "Suitable for outdoor activities with warm clothing"
            If celsius < 24 Then Return "Ideal for all outdoor activities"
            If celsius < 30 Then Return "Good for outdoor activities; stay hydrated"
            If celsius < 35 Then Return "Limit strenuous outdoor activities"
            Return "Avoid outdoor activities; heat advisory conditions"
        End Function

        ''' <summary>
        ''' Get risk level for temperature exposure
        ''' </summary>
        Public Shared Function GetRiskLevel(celsius As Double) As String
            If celsius < -40 OrElse celsius > 50 Then Return "Extreme"
            If celsius < -20 OrElse celsius > 40 Then Return "High"
            If celsius < -10 OrElse celsius > 35 Then Return "Moderate"
            If celsius < 0 OrElse celsius > 30 Then Return "Low"
            Return "Minimal"
        End Function
    End Class

    ''' <summary>
    ''' Thermal index calculations (heat index, wind chill, etc.)
    ''' </summary>
    Public Class ThermalIndices

        ''' <summary>
        ''' Calculate heat index (feels-like temperature in hot weather)
        ''' Uses the Rothfusz regression equation
        ''' </summary>
        Public Shared Function CalculateHeatIndex(temperatureF As Double, relativeHumidity As Double) As Double
            ' Heat index is only valid for temps >= 80°F and humidity >= 40%
            If temperatureF < 80 OrElse relativeHumidity < 40 Then
                Return temperatureF
            End If

            Dim T = temperatureF
            Dim R = relativeHumidity

            ' Rothfusz regression equation
            Dim HI = -42.379 +
                     2.04901523 * T +
                     10.14333127 * R -
                     0.22475541 * T * R -
                     0.00683783 * T * T -
                     0.05481717 * R * R +
                     0.00122874 * T * T * R +
                     0.00085282 * T * R * R -
                     0.00000199 * T * T * R * R

            Return HI
        End Function

        ''' <summary>
        ''' Calculate heat index from Celsius
        ''' </summary>
        Public Shared Function CalculateHeatIndexCelsius(temperatureC As Double, relativeHumidity As Double) As Double
            Dim tempF = TemperatureConverter.CelsiusToFahrenheit(temperatureC)
            Dim heatIndexF = CalculateHeatIndex(tempF, relativeHumidity)
            Return TemperatureConverter.FahrenheitToCelsius(heatIndexF)
        End Function

        ''' <summary>
        ''' Calculate wind chill (feels-like temperature in cold weather)
        ''' Uses the NWS Wind Chill Formula
        ''' </summary>
        Public Shared Function CalculateWindChill(temperatureF As Double, windSpeedMph As Double) As Double
            ' Wind chill is only valid for temps <= 50°F and wind >= 3 mph
            If temperatureF > 50 OrElse windSpeedMph < 3 Then
                Return temperatureF
            End If

            ' NWS Wind Chill Formula
            Dim windChill = 35.74 +
                           0.6215 * temperatureF -
                           35.75 * Math.Pow(windSpeedMph, 0.16) +
                           0.4275 * temperatureF * Math.Pow(windSpeedMph, 0.16)

            Return windChill
        End Function

        ''' <summary>
        ''' Calculate wind chill from Celsius and km/h
        ''' </summary>
        Public Shared Function CalculateWindChillCelsius(temperatureC As Double, windSpeedKmh As Double) As Double
            Dim tempF = TemperatureConverter.CelsiusToFahrenheit(temperatureC)
            Dim windMph = windSpeedKmh / 1.60934
            Dim windChillF = CalculateWindChill(tempF, windMph)
            Return TemperatureConverter.FahrenheitToCelsius(windChillF)
        End Function

        ''' <summary>
        ''' Calculate dew point temperature
        ''' Magnus formula approximation
        ''' </summary>
        Public Shared Function CalculateDewPoint(temperatureC As Double, relativeHumidity As Double) As Double
            Dim a = 17.27
            Dim b = 237.7
            Dim alpha = (a * temperatureC) / (b + temperatureC) + Math.Log(relativeHumidity / 100.0)
            Return (b * alpha) / (a - alpha)
        End Function

        ''' <summary>
        ''' Calculate apparent temperature (Australian Bureau of Meteorology formula)
        ''' </summary>
        Public Shared Function CalculateApparentTemperature(temperatureC As Double, relativeHumidity As Double, windSpeedMps As Double) As Double
            ' Vapor pressure
            Dim e = (relativeHumidity / 100.0) * 6.105 * Math.Exp((17.27 * temperatureC) / (237.7 + temperatureC))

            ' Apparent temperature
            Dim AT = temperatureC + 0.33 * e - 0.7 * windSpeedMps - 4.0
            Return AT
        End Function

        ''' <summary>
        ''' Calculate humidex (Canadian heat index)
        ''' </summary>
        Public Shared Function CalculateHumidex(temperatureC As Double, dewPointC As Double) As Double
            ' Calculate vapor pressure
            Dim e = 6.11 * Math.Exp(5417.7530 * ((1 / 273.16) - (1 / (dewPointC + 273.15))))

            ' Calculate humidex
            Dim h = temperatureC + 0.5555 * (e - 10.0)
            Return Math.Max(h, temperatureC)
        End Function

        ''' <summary>
        ''' Calculate wet bulb globe temperature (simplified)
        ''' For outdoor heat stress assessment
        ''' </summary>
        Public Shared Function CalculateWetBulbGlobeTemperature(temperatureC As Double, relativeHumidity As Double, Optional solarRadiation As Double = 0.5) As Double
            ' Simplified WBGT calculation
            Dim wetBulb = CalculateWetBulbTemperature(temperatureC, relativeHumidity)

            ' WBGT = 0.7 * Tw + 0.2 * Tg + 0.1 * Td
            ' Simplified: assume globe temp ≈ air temp + solar effect
            Dim globeTemp = temperatureC + solarRadiation * 10
            Dim wbgt = 0.7 * wetBulb + 0.2 * globeTemp + 0.1 * temperatureC

            Return wbgt
        End Function

        ''' <summary>
        ''' Calculate wet bulb temperature (approximation)
        ''' </summary>
        Public Shared Function CalculateWetBulbTemperature(temperatureC As Double, relativeHumidity As Double) As Double
            Dim dewPoint = CalculateDewPoint(temperatureC, relativeHumidity)
            Return dewPoint + (temperatureC - dewPoint) / 3
        End Function

        ''' <summary>
        ''' Get heat stress category based on WBGT
        ''' </summary>
        Public Shared Function GetHeatStressCategory(wbgtC As Double) As String
            If wbgtC < 25 Then Return "Normal"
            If wbgtC < 28 Then Return "Caution: Fatigue possible"
            If wbgtC < 30 Then Return "Extreme Caution: Heat cramps/exhaustion possible"
            If wbgtC < 33 Then Return "Danger: Heat exhaustion likely"
            Return "Extreme Danger: Heat stroke imminent"
        End Function
    End Class

    ''' <summary>
    ''' Temperature statistics and analysis
    ''' </summary>
    Public Class TemperatureStatistics

        ''' <summary>
        ''' Calculate average temperature
        ''' </summary>
        Public Shared Function Average(temperatures As Temperature()) As Temperature
            If temperatures.Length = 0 Then
                Throw New ArgumentException("Cannot calculate average of empty array")
            End If

            Dim unit = temperatures(0).Unit
            Dim sum = temperatures.Sum(Function(t) t.ConvertTo(unit).Value)
            Return New Temperature(sum / temperatures.Length, unit)
        End Function

        ''' <summary>
        ''' Calculate median temperature
        ''' </summary>
        Public Shared Function Median(temperatures As Temperature()) As Temperature
            If temperatures.Length = 0 Then
                Throw New ArgumentException("Cannot calculate median of empty array")
            End If

            Dim unit = temperatures(0).Unit
            Dim values = temperatures.Select(Function(t) t.ConvertTo(unit).Value).OrderBy(Function(v) v).ToArray()

            If values.Length Mod 2 = 0 Then
                Return New Temperature((values(values.Length \ 2 - 1) + values(values.Length \ 2)) / 2, unit)
            Else
                Return New Temperature(values(values.Length \ 2), unit)
            End If
        End Function

        ''' <summary>
        ''' Find minimum temperature
        ''' </summary>
        Public Shared Function Minimum(temperatures As Temperature()) As Temperature
            If temperatures.Length = 0 Then
                Throw New ArgumentException("Cannot find minimum of empty array")
            End If

            Return temperatures.OrderBy(Function(t) t.ToKelvin()).First()
        End Function

        ''' <summary>
        ''' Find maximum temperature
        ''' </summary>
        Public Shared Function Maximum(temperatures As Temperature()) As Temperature
            If temperatures.Length = 0 Then
                Throw New ArgumentException("Cannot find maximum of empty array")
            End If

            Return temperatures.OrderBy(Function(t) t.ToKelvin()).Last()
        End Function

        ''' <summary>
        ''' Calculate temperature range
        ''' </summary>
        Public Shared Function Range(temperatures As Temperature()) As (min As Temperature, max As Temperature)
            Return (Minimum(temperatures), Maximum(temperatures))
        End Function

        ''' <summary>
        ''' Calculate standard deviation
        ''' </summary>
        Public Shared Function StandardDeviation(temperatures As Temperature()) As Double
            If temperatures.Length < 2 Then Return 0

            Dim unit = temperatures(0).Unit
            Dim values = temperatures.Select(Function(t) t.ConvertTo(unit).Value).ToArray()
            Dim avg = values.Average()
            Dim sumSquares = values.Sum(Function(v) Math.Pow(v - avg, 2))

            Return Math.Sqrt(sumSquares / (values.Length - 1))
        End Function

        ''' <summary>
        ''' Count temperatures in range
        ''' </summary>
        Public Shared Function CountInRange(temperatures As Temperature(), minCelsius As Double, maxCelsius As Double) As Integer
            Return temperatures.Count(Function(t)
                                         Dim celsius = t.ToCelsius()
                                         Return celsius >= minCelsius AndAlso celsius <= maxCelsius
                                     End Function)
        End Function
    End Class

    ''' <summary>
    ''' Temperature conversion lookup table for quick reference
    ''' </summary>
    Public Class TemperatureLookupTable

        ''' <summary>
        ''' Generate a lookup table for temperature conversion
        ''' </summary>
        Public Shared Function GenerateTable(fromUnit As TemperatureUnit, toUnit As TemperatureUnit, startValue As Double, endValue As Double, step As Double) As Dictionary(Of Double, Double)
            Dim table As New Dictionary(Of Double, Double)()

            For value = startValue To endValue Step step
                table(value) = Math.Round(TemperatureConverter.Convert(value, fromUnit, toUnit), 2)
            Next

            Return table
        End Function

        ''' <summary>
        ''' Get common temperature reference points
        ''' </summary>
        Public Shared Function GetReferencePoints() As Dictionary(Of String, Temperature)
            Return New Dictionary(Of String, Temperature) From
            {
                {"Absolute Zero", Temperature.FromCelsius(-273.15)},
                {"Liquid Nitrogen", Temperature.FromCelsius(-196)},
                {"Dry Ice", Temperature.FromCelsius(-78.5)},
                {"Water Freezing", Temperature.FromCelsius(0)},
                {"Refrigerator", Temperature.FromCelsius(4)},
                {"Room Temperature", Temperature.FromCelsius(20)},
                {"Body Temperature", Temperature.FromCelsius(37)},
                {"Water Boiling", Temperature.FromCelsius(100)},
                {"Oven (Moderate)", Temperature.FromCelsius(180)},
                {"Bread Baking", Temperature.FromCelsius(200)},
                {"Pizza Oven", Temperature.FromCelsius(250)},
                {"Surface of Sun", Temperature.FromCelsius(5500)}
            }
        End Function
    End Class

End Namespace