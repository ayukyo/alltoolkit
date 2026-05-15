Imports System
Imports Microsoft.VisualStudio.TestTools.UnitTesting
Imports TemperatureUtils

<TestClass>
Public Class TemperatureConverterTests

    <TestMethod>
    Public Sub CelsiusToFahrenheit_FreezingPoint()
        Dim result = TemperatureConverter.CelsiusToFahrenheit(0)
        Assert.AreEqual(32.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub CelsiusToFahrenheit_BoilingPoint()
        Dim result = TemperatureConverter.CelsiusToFahrenheit(100)
        Assert.AreEqual(212.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub CelsiusToFahrenheit_RoomTemperature()
        Dim result = TemperatureConverter.CelsiusToFahrenheit(20)
        Assert.AreEqual(68.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub FahrenheitToCelsius_FreezingPoint()
        Dim result = TemperatureConverter.FahrenheitToCelsius(32)
        Assert.AreEqual(0.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub FahrenheitToCelsius_BoilingPoint()
        Dim result = TemperatureConverter.FahrenheitToCelsius(212)
        Assert.AreEqual(100.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub CelsiusToKelvin_FreezingPoint()
        Dim result = TemperatureConverter.CelsiusToKelvin(0)
        Assert.AreEqual(273.15, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub CelsiusToKelvin_AbsoluteZero()
        Dim result = TemperatureConverter.CelsiusToKelvin(-273.15)
        Assert.AreEqual(0.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub KelvinToCelsius_FreezingPoint()
        Dim result = TemperatureConverter.KelvinToCelsius(273.15)
        Assert.AreEqual(0.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub FahrenheitToKelvin_Standard()
        Dim result = TemperatureConverter.FahrenheitToKelvin(32)
        Assert.AreEqual(273.15, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub KelvinToFahrenheit_Standard()
        Dim result = TemperatureConverter.KelvinToFahrenheit(273.15)
        Assert.AreEqual(32.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub FahrenheitToRankine_Freezing()
        Dim result = TemperatureConverter.FahrenheitToRankine(32)
        Assert.AreEqual(491.67, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub RankineToFahrenheit_Standard()
        Dim result = TemperatureConverter.RankineToFahrenheit(491.67)
        Assert.AreEqual(32.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub CelsiusToRankine_Freezing()
        Dim result = TemperatureConverter.CelsiusToRankine(0)
        Assert.AreEqual(491.67, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub RankineToCelsius_Standard()
        Dim result = TemperatureConverter.RankineToCelsius(491.67)
        Assert.AreEqual(0.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub KelvinToRankine_Freezing()
        Dim result = TemperatureConverter.KelvinToRankine(273.15)
        Assert.AreEqual(491.67, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub RankineToKelvin_Standard()
        Dim result = TemperatureConverter.RankineToKelvin(491.67)
        Assert.AreEqual(273.15, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub Convert_CelsiusToFahrenheit()
        Dim result = TemperatureConverter.Convert(0, TemperatureUnit.Celsius, TemperatureUnit.Fahrenheit)
        Assert.AreEqual(32.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub Convert_FahrenheitToKelvin()
        Dim result = TemperatureConverter.Convert(32, TemperatureUnit.Fahrenheit, TemperatureUnit.Kelvin)
        Assert.AreEqual(273.15, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub Convert_KelvinToCelsius()
        Dim result = TemperatureConverter.Convert(373.15, TemperatureUnit.Kelvin, TemperatureUnit.Celsius)
        Assert.AreEqual(100.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub Convert_SameUnit_ReturnsSame()
        Dim result = TemperatureConverter.Convert(25.5, TemperatureUnit.Celsius, TemperatureUnit.Celsius)
        Assert.AreEqual(25.5, result, 0.001)
    End Sub

    <TestMethod>
    Public Sub ConvertBatch_MultipleValues()
        Dim values = {0.0, 100.0, -40.0}
        Dim result = TemperatureConverter.ConvertBatch(values, TemperatureUnit.Celsius, TemperatureUnit.Fahrenheit)
        
        Assert.AreEqual(32.0, result(0), 0.01)
        Assert.AreEqual(212.0, result(1), 0.01)
        Assert.AreEqual(-40.0, result(2), 0.01)
    End Sub

    <TestMethod>
    Public Sub Parse_CelsiusWithSymbol()
        Dim result = TemperatureConverter.Parse("25°C")
        Assert.AreEqual(25.0, result.Value, 0.01)
        Assert.AreEqual(TemperatureUnit.Celsius, result.Unit)
    End Sub

    <TestMethod>
    Public Sub Parse_FahrenheitWithSymbol()
        Dim result = TemperatureConverter.Parse("77°F")
        Assert.AreEqual(77.0, result.Value, 0.01)
        Assert.AreEqual(TemperatureUnit.Fahrenheit, result.Unit)
    End Sub

    <TestMethod>
    Public Sub Parse_KelvinNoSymbol()
        Dim result = TemperatureConverter.Parse("300K")
        Assert.AreEqual(300.0, result.Value, 0.01)
        Assert.AreEqual(TemperatureUnit.Kelvin, result.Unit)
    End Sub

    <TestMethod>
    Public Sub Parse_RankineWithSymbol()
        Dim result = TemperatureConverter.Parse("491.67°R")
        Assert.AreEqual(491.67, result.Value, 0.01)
        Assert.AreEqual(TemperatureUnit.Rankine, result.Unit)
    End Sub

    <TestMethod>
    Public Sub TryParse_ValidInput_ReturnsTrue()
        Dim result As Temperature
        Dim success = TemperatureConverter.TryParse("25°C", result)
        
        Assert.IsTrue(success)
        Assert.AreEqual(25.0, result.Value, 0.01)
    End Sub

    <TestMethod>
    Public Sub TryParse_InvalidInput_ReturnsFalse()
        Dim result As Temperature
        Dim success = TemperatureConverter.TryParse("invalid", result)
        
        Assert.IsFalse(success)
    End Sub

End Class

<TestClass>
Public Class TemperatureTests

    <TestMethod>
    Public Sub FromCelsius_CreatesCorrectTemperature()
        Dim temp = Temperature.FromCelsius(25)
        Assert.AreEqual(25.0, temp.Value, 0.01)
        Assert.AreEqual(TemperatureUnit.Celsius, temp.Unit)
    End Sub

    <TestMethod>
    Public Sub FromFahrenheit_CreatesCorrectTemperature()
        Dim temp = Temperature.FromFahrenheit(77)
        Assert.AreEqual(77.0, temp.Value, 0.01)
        Assert.AreEqual(TemperatureUnit.Fahrenheit, temp.Unit)
    End Sub

    <TestMethod>
    Public Sub FromKelvin_CreatesCorrectTemperature()
        Dim temp = Temperature.FromKelvin(300)
        Assert.AreEqual(300.0, temp.Value, 0.01)
        Assert.AreEqual(TemperatureUnit.Kelvin, temp.Unit)
    End Sub

    <TestMethod>
    Public Sub ToCelsius_ConvertsCorrectly()
        Dim temp = Temperature.FromFahrenheit(32)
        Dim result = temp.ToCelsius()
        Assert.AreEqual(0.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub ToFahrenheit_ConvertsCorrectly()
        Dim temp = Temperature.FromCelsius(0)
        Dim result = temp.ToFahrenheit()
        Assert.AreEqual(32.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub ToKelvin_ConvertsCorrectly()
        Dim temp = Temperature.FromCelsius(0)
        Dim result = temp.ToKelvin()
        Assert.AreEqual(273.15, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub ToRankine_ConvertsCorrectly()
        Dim temp = Temperature.FromCelsius(0)
        Dim result = temp.ToRankine()
        Assert.AreEqual(491.67, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub ConvertTo_ChangesUnit()
        Dim temp = Temperature.FromCelsius(100)
        Dim result = temp.ConvertTo(TemperatureUnit.Fahrenheit)
        
        Assert.AreEqual(TemperatureUnit.Fahrenheit, result.Unit)
        Assert.AreEqual(212.0, result.Value, 0.01)
    End Sub

    <TestMethod>
    Public Sub IsValid_AboveAbsoluteZero_ReturnsTrue()
        Dim temp = Temperature.FromCelsius(0)
        Assert.IsTrue(temp.IsValid())
    End Sub

    <TestMethod>
    Public Sub IsValid_BelowAbsoluteZero_ReturnsFalse()
        Dim temp = Temperature.FromCelsius(-300)
        Assert.IsFalse(temp.IsValid())
    End Sub

    <TestMethod>
    Public Sub IsFreezing_BelowZero_ReturnsTrue()
        Dim temp = Temperature.FromCelsius(-5)
        Assert.IsTrue(temp.IsFreezing())
    End Sub

    <TestMethod>
    Public Sub IsFreezing_AboveZero_ReturnsFalse()
        Dim temp = Temperature.FromCelsius(20)
        Assert.IsFalse(temp.IsFreezing())
    End Sub

    <TestMethod>
    Public Sub IsBoiling_AtOrAbove100_ReturnsTrue()
        Dim temp = Temperature.FromCelsius(100)
        Assert.IsTrue(temp.IsBoiling())
    End Sub

    <TestMethod>
    Public Sub IsBoiling_Below100_ReturnsFalse()
        Dim temp = Temperature.FromCelsius(99)
        Assert.IsFalse(temp.IsBoiling())
    End Sub

    <TestMethod>
    Public Sub IsComfortable_InRange_ReturnsTrue()
        Dim temp = Temperature.FromCelsius(20)
        Assert.IsTrue(temp.IsComfortable())
    End Sub

    <TestMethod>
    Public Sub IsComfortable_OutOfRange_ReturnsFalse()
        Dim temp = Temperature.FromCelsius(30)
        Assert.IsFalse(temp.IsComfortable())
    End Sub

    <TestMethod>
    Public Sub Format_ReturnsCorrectString()
        Dim temp = Temperature.FromCelsius(25.5)
        Dim result = temp.Format(1)
        Assert.AreEqual("25.5°C", result)
    End Sub

    <TestMethod>
    Public Sub GetCategory_ReturnsCorrectCategory()
        Dim freezing = Temperature.FromCelsius(-10)
        Dim comfortable = Temperature.FromCelsius(22)
        Dim hot = Temperature.FromCelsius(38)
        
        Assert.AreEqual("Freezing", freezing.GetCategory())
        Assert.AreEqual("Comfortable", comfortable.GetCategory())
        Assert.AreEqual("Very Hot", hot.GetCategory())
    End Sub

    <TestMethod>
    Public Sub Operator_Add_SameUnits()
        Dim t1 = Temperature.FromCelsius(10)
        Dim t2 = Temperature.FromCelsius(15)
        Dim result = t1 + t2
        
        Assert.AreEqual(25.0, result.Value, 0.01)
        Assert.AreEqual(TemperatureUnit.Celsius, result.Unit)
    End Sub

    <TestMethod>
    Public Sub Operator_Add_DifferentUnits()
        Dim t1 = Temperature.FromCelsius(0)
        Dim t2 = Temperature.FromFahrenheit(32)
        Dim result = t1 + t2
        
        Assert.AreEqual(0.0, result.Value, 0.01)
    End Sub

    <TestMethod>
    Public Sub Operator_Subtract_SameUnits()
        Dim t1 = Temperature.FromCelsius(20)
        Dim t2 = Temperature.FromCelsius(10)
        Dim result = t1 - t2
        
        Assert.AreEqual(10.0, result.Value, 0.01)
    End Sub

    <TestMethod>
    Public Sub Operator_Multiply()
        Dim temp = Temperature.FromCelsius(10)
        Dim result = temp * 2
        
        Assert.AreEqual(20.0, result.Value, 0.01)
    End Sub

    <TestMethod>
    Public Sub Operator_Divide()
        Dim temp = Temperature.FromCelsius(20)
        Dim result = temp / 2
        
        Assert.AreEqual(10.0, result.Value, 0.01)
    End Sub

    <TestMethod>
    Public Sub Operator_Equal()
        Dim t1 = Temperature.FromCelsius(0)
        Dim t2 = Temperature.FromFahrenheit(32)
        
        Assert.IsTrue(t1 = t2)
    End Sub

    <TestMethod>
    Public Sub Operator_NotEqual()
        Dim t1 = Temperature.FromCelsius(0)
        Dim t2 = Temperature.FromFahrenheit(100)
        
        Assert.IsTrue(t1 <> t2)
    End Sub

    <TestMethod>
    Public Sub Operator_LessThan()
        Dim t1 = Temperature.FromCelsius(0)
        Dim t2 = Temperature.FromCelsius(100)
        
        Assert.IsTrue(t1 < t2)
    End Sub

    <TestMethod>
    Public Sub Operator_GreaterThan()
        Dim t1 = Temperature.FromCelsius(100)
        Dim t2 = Temperature.FromCelsius(0)
        
        Assert.IsTrue(t1 > t2)
    End Sub

End Class

<TestClass>
Public Class TemperatureValidatorTests

    <TestMethod>
    Public Sub IsValidTemperature_CelsiusAboveAbsoluteZero()
        Dim result = TemperatureValidator.IsValidTemperature(0, TemperatureUnit.Celsius)
        Assert.IsTrue(result)
    End Sub

    <TestMethod>
    Public Sub IsValidTemperature_CelsiusBelowAbsoluteZero()
        Dim result = TemperatureValidator.IsValidTemperature(-300, TemperatureUnit.Celsius)
        Assert.IsFalse(result)
    End Sub

    <TestMethod>
    Public Sub IsValidTemperature_KelvinAboveAbsoluteZero()
        Dim result = TemperatureValidator.IsValidTemperature(1, TemperatureUnit.Kelvin)
        Assert.IsTrue(result)
    End Sub

    <TestMethod>
    Public Sub IsValidTemperature_KelvinAtAbsoluteZero()
        Dim result = TemperatureValidator.IsValidTemperature(0, TemperatureUnit.Kelvin)
        Assert.IsTrue(result)
    End Sub

    <TestMethod>
    Public Sub IsValidTemperature_KelvinBelowAbsoluteZero()
        Dim result = TemperatureValidator.IsValidTemperature(-1, TemperatureUnit.Kelvin)
        Assert.IsFalse(result)
    End Sub

    <TestMethod>
    Public Sub GetAbsoluteZero_Celsius()
        Dim result = TemperatureValidator.GetAbsoluteZero(TemperatureUnit.Celsius)
        Assert.AreEqual(-273.15, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub GetAbsoluteZero_Fahrenheit()
        Dim result = TemperatureValidator.GetAbsoluteZero(TemperatureUnit.Fahrenheit)
        Assert.AreEqual(-459.67, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub GetAbsoluteZero_Kelvin()
        Dim result = TemperatureValidator.GetAbsoluteZero(TemperatureUnit.Kelvin)
        Assert.AreEqual(0.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub IsInRange_WithinRange()
        Dim result = TemperatureValidator.IsInRange(25, TemperatureUnit.Celsius, 0, 100)
        Assert.IsTrue(result)
    End Sub

    <TestMethod>
    Public Sub IsInRange_OutsideRange()
        Dim result = TemperatureValidator.IsInRange(150, TemperatureUnit.Celsius, 0, 100)
        Assert.IsFalse(result)
    End Sub

End Class

<TestClass>
Public Class TemperatureFormatterTests

    <TestMethod>
    Public Sub Format_Celsius()
        Dim result = TemperatureFormatter.Format(25.5, TemperatureUnit.Celsius, 1)
        Assert.AreEqual("25.5°C", result)
    End Sub

    <TestMethod>
    Public Sub Format_Fahrenheit()
        Dim result = TemperatureFormatter.Format(77.3, TemperatureUnit.Fahrenheit, 1)
        Assert.AreEqual("77.3°F", result)
    End Sub

    <TestMethod>
    Public Sub Format_Kelvin()
        Dim result = TemperatureFormatter.Format(300.15, TemperatureUnit.Kelvin, 2)
        Assert.AreEqual("300.15K", result)
    End Sub

    <TestMethod>
    Public Sub Format_Rankine()
        Dim result = TemperatureFormatter.Format(491.67, TemperatureUnit.Rankine, 2)
        Assert.AreEqual("491.67°R", result)
    End Sub

    <TestMethod>
    Public Sub FormatAll_ReturnsAllFormats()
        Dim result = TemperatureFormatter.FormatAll(0, TemperatureUnit.Celsius, 1)
        Assert.IsTrue(result.Contains("0°C"))
        Assert.IsTrue(result.Contains("32°F"))
        Assert.IsTrue(result.Contains("273.1K"))
    End Sub

    <TestMethod>
    Public Sub FormatRange_ReturnsCorrectString()
        Dim result = TemperatureFormatter.FormatRange(20, 25, TemperatureUnit.Celsius, 1)
        Assert.AreEqual("20°C - 25°C", result)
    End Sub

End Class

<TestClass>
Public Class TemperatureCategoriesTests

    <TestMethod>
    Public Sub GetCategory_ExtremeCold()
        Assert.AreEqual("Extreme Cold", TemperatureCategories.GetCategory(-60))
    End Sub

    <TestMethod>
    Public Sub GetCategory_SevereCold()
        Assert.AreEqual("Severe Cold", TemperatureCategories.GetCategory(-30))
    End Sub

    <TestMethod>
    Public Sub GetCategory_Freezing()
        Assert.AreEqual("Freezing", TemperatureCategories.GetCategory(-5))
    End Sub

    <TestMethod>
    Public Sub GetCategory_Cold()
        Assert.AreEqual("Cold", TemperatureCategories.GetCategory(5))
    End Sub

    <TestMethod>
    Public Sub GetCategory_Cool()
        Assert.AreEqual("Cool", TemperatureCategories.GetCategory(15))
    End Sub

    <TestMethod>
    Public Sub GetCategory_Comfortable()
        Assert.AreEqual("Comfortable", TemperatureCategories.GetCategory(22))
    End Sub

    <TestMethod>
    Public Sub GetCategory_Warm()
        Assert.AreEqual("Warm", TemperatureCategories.GetCategory(27))
    End Sub

    <TestMethod>
    Public Sub GetCategory_Hot()
        Assert.AreEqual("Hot", TemperatureCategories.GetCategory(33))
    End Sub

    <TestMethod>
    Public Sub GetCategory_VeryHot()
        Assert.AreEqual("Very Hot", TemperatureCategories.GetCategory(38))
    End Sub

    <TestMethod>
    Public Sub GetCategory_ExtremeHeat()
        Assert.AreEqual("Extreme Heat", TemperatureCategories.GetCategory(45))
    End Sub

    <TestMethod>
    Public Sub GetCategory_ExtremeDanger()
        Assert.AreEqual("Extreme Danger", TemperatureCategories.GetCategory(55))
    End Sub

    <TestMethod>
    Public Sub GetClothingRecommendation_WinterCoat()
        Dim result = TemperatureCategories.GetClothingRecommendation(-10)
        Assert.IsTrue(result.Contains("Winter coat"))
    End Sub

    <TestMethod>
    Public Sub GetClothingRecommendation_LightClothing()
        Dim result = TemperatureCategories.GetClothingRecommendation(28)
        Assert.IsTrue(result.Contains("Light"))
    End Sub

    <TestMethod>
    Public Sub GetActivityRecommendation_IdealWeather()
        Dim result = TemperatureCategories.GetActivityRecommendation(22)
        Assert.IsTrue(result.Contains("Ideal"))
    End Sub

    <TestMethod>
    Public Sub GetRiskLevel_Extreme()
        Assert.AreEqual("Extreme", TemperatureCategories.GetRiskLevel(-50))
        Assert.AreEqual("Extreme", TemperatureCategories.GetRiskLevel(55))
    End Sub

    <TestMethod>
    Public Sub GetRiskLevel_Minimal()
        Assert.AreEqual("Minimal", TemperatureCategories.GetRiskLevel(20))
    End Sub

End Class

<TestClass>
Public Class ThermalIndicesTests

    <TestMethod>
    Public Sub CalculateHeatIndex_HighTempHighHumidity()
        ' 90°F at 80% humidity should give heat index > 100°F
        Dim result = ThermalIndices.CalculateHeatIndex(90, 80)
        Assert.IsTrue(result > 100)
    End Sub

    <TestMethod>
    Public Sub CalculateHeatIndex_BelowThreshold_ReturnsTemp()
        ' Below 80°F, should return original temp
        Dim result = ThermalIndices.CalculateHeatIndex(70, 50)
        Assert.AreEqual(70.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub CalculateHeatIndex_LowHumidity_ReturnsTemp()
        ' Below 40% humidity, should return original temp
        Dim result = ThermalIndices.CalculateHeatIndex(85, 30)
        Assert.AreEqual(85.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub CalculateHeatIndexCelsius_Standard()
        Dim result = ThermalIndices.CalculateHeatIndexCelsius(35, 70)
        ' 35°C at 70% humidity should give elevated heat index
        Assert.IsTrue(result > 35)
    End Sub

    <TestMethod>
    Public Sub CalculateWindChill_BelowFreezing()
        ' 30°F with 10 mph wind
        Dim result = ThermalIndices.CalculateWindChill(30, 10)
        Assert.IsTrue(result < 30)
    End Sub

    <TestMethod>
    Public Sub CalculateWindChill_Above50_ReturnsTemp()
        ' Above 50°F, should return original temp
        Dim result = ThermalIndices.CalculateWindChill(60, 10)
        Assert.AreEqual(60.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub CalculateWindChill_LowWind_ReturnsTemp()
        ' Below 3 mph wind, should return original temp
        Dim result = ThermalIndices.CalculateWindChill(30, 2)
        Assert.AreEqual(30.0, result, 0.01)
    End Sub

    <TestMethod>
    Public Sub CalculateWindChillCelsius_Standard()
        ' 0°C with 20 km/h wind
        Dim result = ThermalIndices.CalculateWindChillCelsius(0, 20)
        Assert.IsTrue(result < 0)
    End Sub

    <TestMethod>
    Public Sub CalculateDewPoint_Standard()
        ' At 20°C with 50% humidity, dew point should be around 9.3°C
        Dim result = ThermalIndices.CalculateDewPoint(20, 50)
        Assert.IsTrue(result > 8 AndAlso result < 11)
    End Sub

    <TestMethod>
    Public Sub CalculateDewPoint_HighHumidity()
        ' At 30°C with 90% humidity, dew point should be close to 30°C
        Dim result = ThermalIndices.CalculateDewPoint(30, 90)
        Assert.IsTrue(result > 27)
    End Sub

    <TestMethod>
    Public Sub CalculateApparentTemperature_Standard()
        Dim result = ThermalIndices.CalculateApparentTemperature(25, 50, 2)
        ' Should be somewhat close to actual temperature
        Assert.IsTrue(Math.Abs(result - 25) < 10)
    End Sub

    <TestMethod>
    Public Sub CalculateHumidex_HighHumidity()
        ' 30°C with high dew point
        Dim result = ThermalIndices.CalculateHumidex(30, 25)
        Assert.IsTrue(result > 30)
    End Sub

    <TestMethod>
    Public Sub CalculateWetBulbTemperature_Standard()
        Dim result = ThermalIndices.CalculateWetBulbTemperature(25, 50)
        ' Wet bulb should be between dew point and dry bulb
        Dim dewPoint = ThermalIndices.CalculateDewPoint(25, 50)
        Assert.IsTrue(result >= dewPoint AndAlso result <= 25)
    End Sub

    <TestMethod>
    Public Sub GetHeatStressCategory_Normal()
        Assert.AreEqual("Normal", ThermalIndices.GetHeatStressCategory(20))
    End Sub

    <TestMethod>
    Public Sub GetHeatStressCategory_Caution()
        Assert.AreEqual("Caution: Fatigue possible", ThermalIndices.GetHeatStressCategory(26))
    End Sub

    <TestMethod>
    Public Sub GetHeatStressCategory_ExtremeDanger()
        Assert.AreEqual("Extreme Danger: Heat stroke imminent", ThermalIndices.GetHeatStressCategory(35))
    End Sub

End Class

<TestClass>
Public Class TemperatureStatisticsTests

    <TestMethod>
    Public Sub Average_SameUnits()
        Dim temps = {
            Temperature.FromCelsius(10),
            Temperature.FromCelsius(20),
            Temperature.FromCelsius(30)
        }
        Dim result = TemperatureStatistics.Average(temps)
        Assert.AreEqual(20.0, result.Value, 0.01)
    End Sub

    <TestMethod>
    Public Sub Average_MixedUnits()
        Dim temps = {
            Temperature.FromCelsius(0),
            Temperature.FromFahrenheit(32) ' Also 0°C
        }
        Dim result = TemperatureStatistics.Average(temps)
        Assert.AreEqual(0.0, result.ToCelsius(), 0.01)
    End Sub

    <TestMethod>
    Public Sub Median_OddCount()
        Dim temps = {
            Temperature.FromCelsius(10),
            Temperature.FromCelsius(20),
            Temperature.FromCelsius(30)
        }
        Dim result = TemperatureStatistics.Median(temps)
        Assert.AreEqual(20.0, result.Value, 0.01)
    End Sub

    <TestMethod>
    Public Sub Median_EvenCount()
        Dim temps = {
            Temperature.FromCelsius(10),
            Temperature.FromCelsius(20),
            Temperature.FromCelsius(30),
            Temperature.FromCelsius(40)
        }
        Dim result = TemperatureStatistics.Median(temps)
        Assert.AreEqual(25.0, result.Value, 0.01)
    End Sub

    <TestMethod>
    Public Sub Minimum_FindsColdest()
        Dim temps = {
            Temperature.FromCelsius(30),
            Temperature.FromCelsius(-10),
            Temperature.FromCelsius(20)
        }
        Dim result = TemperatureStatistics.Minimum(temps)
        Assert.AreEqual(-10.0, result.Value, 0.01)
    End Sub

    <TestMethod>
    Public Sub Maximum_FindsHottest()
        Dim temps = {
            Temperature.FromCelsius(30),
            Temperature.FromCelsius(-10),
            Temperature.FromCelsius(20)
        }
        Dim result = TemperatureStatistics.Maximum(temps)
        Assert.AreEqual(30.0, result.Value, 0.01)
    End Sub

    <TestMethod>
    Public Sub Range_ReturnsMinMax()
        Dim temps = {
            Temperature.FromCelsius(30),
            Temperature.FromCelsius(-10),
            Temperature.FromCelsius(20)
        }
        Dim result = TemperatureStatistics.Range(temps)
        Assert.AreEqual(-10.0, result.min.Value, 0.01)
        Assert.AreEqual(30.0, result.max.Value, 0.01)
    End Sub

    <TestMethod>
    Public Sub StandardDeviation_SmallVariance()
        Dim temps = {
            Temperature.FromCelsius(20),
            Temperature.FromCelsius(21),
            Temperature.FromCelsius(19),
            Temperature.FromCelsius(20)
        }
        Dim result = TemperatureStatistics.StandardDeviation(temps)
        Assert.IsTrue(result < 1)
    End Sub

    <TestMethod>
    Public Sub StandardDeviation_LargeVariance()
        Dim temps = {
            Temperature.FromCelsius(0),
            Temperature.FromCelsius(100)
        }
        Dim result = TemperatureStatistics.StandardDeviation(temps)
        Assert.IsTrue(result > 50)
    End Sub

    <TestMethod>
    Public Sub CountInRange_WithinRange()
        Dim temps = {
            Temperature.FromCelsius(10),
            Temperature.FromCelsius(20),
            Temperature.FromCelsius(30),
            Temperature.FromCelsius(40)
        }
        Dim result = TemperatureStatistics.CountInRange(temps, 15, 35)
        Assert.AreEqual(2, result)
    End Sub

End Class

<TestClass>
Public Class TemperatureLookupTableTests

    <TestMethod>
    Public Sub GenerateTable_CelsiusToFahrenheit()
        Dim table = TemperatureLookupTable.GenerateTable(
            TemperatureUnit.Celsius, 
            TemperatureUnit.Fahrenheit, 
            0, 10, 5)
        
        Assert.AreEqual(3, table.Count)
        Assert.AreEqual(32.0, table(0), 0.01)
        Assert.AreEqual(41.0, table(5), 0.01)
        Assert.AreEqual(50.0, table(10), 0.01)
    End Sub

    <TestMethod>
    Public Sub GetReferencePoints_ContainsExpectedValues()
        Dim refs = TemperatureLookupTable.GetReferencePoints()
        
        Assert.IsTrue(refs.ContainsKey("Absolute Zero"))
        Assert.IsTrue(refs.ContainsKey("Water Freezing"))
        Assert.IsTrue(refs.ContainsKey("Water Boiling"))
        Assert.IsTrue(refs.ContainsKey("Body Temperature"))
    End Sub

    <TestMethod>
    Public Sub GetReferencePoints_WaterFreezingIsCorrect()
        Dim refs = TemperatureLookupTable.GetReferencePoints()
        Dim freezing = refs("Water Freezing")
        
        Assert.AreEqual(0.0, freezing.ToCelsius(), 0.01)
    End Sub

    <TestMethod>
    Public Sub GetReferencePoints_WaterBoilingIsCorrect()
        Dim refs = TemperatureLookupTable.GetReferencePoints()
        Dim boiling = refs("Water Boiling")
        
        Assert.AreEqual(100.0, boiling.ToCelsius(), 0.01)
    End Sub

    <TestMethod>
    Public Sub GetReferencePoints_BodyTempIsCorrect()
        Dim refs = TemperatureLookupTable.GetReferencePoints()
        Dim body = refs("Body Temperature")
        
        Assert.AreEqual(37.0, body.ToCelsius(), 0.01)
    End Sub

End Class