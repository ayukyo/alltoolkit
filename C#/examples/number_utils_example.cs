using System;
using System.Collections.Generic;
using System.Globalization;
using AllToolkit;

namespace NumberUtilsExample
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== NumberUtils Examples ===\n");

            FormattingExamples();
            BaseConversionExamples();
            RomanNumeralExamples();
            MathematicalExamples();
            StatisticalExamples();
            ValidationExamples();
            ParsingExamples();
            UtilityExamples();
            RandomExamples();

            Console.WriteLine("\n=== All examples completed ===");
        }

        static void FormattingExamples()
        {
            Console.WriteLine("--- Formatting Examples ---");

            // Basic formatting
            Console.WriteLine($"Format: {NumberUtils.Format(1234567.89, 2)}");
            Console.WriteLine($"Format (no decimals): {NumberUtils.Format(1234567.89, 0)}");

            // Currency
            Console.WriteLine($"Currency (USD): {NumberUtils.Currency(1234.56)}");
            Console.WriteLine($"Currency (EUR): {NumberUtils.Currency(1234.56, "€")}");
            Console.WriteLine($"Currency (JPY): {NumberUtils.Currency(1234, "¥", 0)}");

            // Percentage
            Console.WriteLine($"Percentage: {NumberUtils.Percentage(0.1567, 2)}");
            Console.WriteLine($"Percentage (no symbol): {NumberUtils.Percentage(0.1567, 1, false)}");

            // Compact notation
            Console.WriteLine($"Compact 1,500: {NumberUtils.Compact(1500)}");
            Console.WriteLine($"Compact 1,500,000: {NumberUtils.Compact(1500000)}");
            Console.WriteLine($"Compact 1,500,000,000: {NumberUtils.Compact(1500000000)}");

            // Ordinal
            Console.WriteLine($"Ordinal 1: {NumberUtils.ToOrdinal(1)}");
            Console.WriteLine($"Ordinal 22: {NumberUtils.ToOrdinal(22)}");
            Console.WriteLine($"Ordinal 103: {NumberUtils.ToOrdinal(103)}");

            // Words
            Console.WriteLine($"Words 42: {NumberUtils.ToWords(42)}");
            Console.WriteLine($"Words 1234: {NumberUtils.ToWords(1234)}");
            Console.WriteLine($"Words 1000000: {NumberUtils.ToWords(1000000)}");

            Console.WriteLine();
        }

        static void BaseConversionExamples()
        {
            Console.WriteLine("--- Base Conversion Examples ---");

            // To different bases
            Console.WriteLine($"Decimal 255 to Binary: {NumberUtils.ToBinary(255, 8, true)}");
            Console.WriteLine($"Decimal 255 to Hex: {NumberUtils.ToHex(255, 2, true, true)}");
            Console.WriteLine($"Decimal 63 to Octal: {NumberUtils.ToOctal(63, 0, true)}");

            // From different bases
            Console.WriteLine($"Binary 0b11111111 to Decimal: {NumberUtils.FromBinary("0b11111111")}");
            Console.WriteLine($"Hex 0xFF to Decimal: {NumberUtils.FromHex("0xFF")}");
            Console.WriteLine($"Octal 0o77 to Decimal: {NumberUtils.FromOctal("0o77")}");

            Console.WriteLine();
        }

        static void RomanNumeralExamples()
        {
            Console.WriteLine("--- Roman Numeral Examples ---");

            // To Roman
            Console.WriteLine($"2024 to Roman: {NumberUtils.ToRoman(2024)}");
            Console.WriteLine($"1999 to Roman: {NumberUtils.ToRoman(1999)}");
            Console.WriteLine($"44 to Roman: {NumberUtils.ToRoman(44)}");

            // From Roman
            Console.WriteLine($"MMXXIV from Roman: {NumberUtils.FromRoman("MMXXIV")}");
            Console.WriteLine($"MCMXCIX from Roman: {NumberUtils.FromRoman("MCMXCIX")}");
            Console.WriteLine($"XLIV from Roman: {NumberUtils.FromRoman("XLIV")}");

            Console.WriteLine();
        }

        static void MathematicalExamples()
        {
            Console.WriteLine("--- Mathematical Examples ---");

            // Clamp
            Console.WriteLine($"Clamp 15 to [0, 10]: {NumberUtils.Clamp(15, 0, 10)}");
            Console.WriteLine($"Clamp -5 to [0, 10]: {NumberUtils.Clamp(-5, 0, 10)}");

            // Lerp
            Console.WriteLine($"Lerp 0 to 100 at 0.5: {NumberUtils.Lerp(0, 100, 0.5)}");
            Console.WriteLine($"Lerp 0 to 100 at 0.25: {NumberUtils.Lerp(0, 100, 0.25)}");

            // MapRange (Fahrenheit to Celsius)
            Console.WriteLine($"Map 32°F to Celsius: {NumberUtils.MapRange(32, 32, 212, 0, 100):F1}°C");
            Console.WriteLine($"Map 212°F to Celsius: {NumberUtils.MapRange(212, 32, 212, 0, 100):F1}°C");

            // ApproxEqual
            Console.WriteLine($"ApproxEqual(0.1 + 0.2, 0.3): {NumberUtils.ApproxEqual(0.1 + 0.2, 0.3)}");

            // RoundToMultiple
            Console.WriteLine($"Round 13 to nearest 5: {NumberUtils.RoundToMultiple(13, 5)}");
            Console.WriteLine($"Round 97 to nearest 25: {NumberUtils.RoundToMultiple(97, 25)}");

            Console.WriteLine();
        }

        static void StatisticalExamples()
        {
            Console.WriteLine("--- Statistical Examples ---");

            var data = new List<double> { 23, 45, 67, 89, 12, 34, 56, 78, 90, 11 };

            Console.WriteLine($"Data: {string.Join(", ", data)}");
            Console.WriteLine($"Mean: {NumberUtils.Mean(data):F2}");
            Console.WriteLine($"Median: {NumberUtils.Median(data):F2}");

            var mode = NumberUtils.Mode(data);
            Console.WriteLine($"Mode: {(mode.HasValue ? mode.Value.ToString() : "No unique mode")}");

            Console.WriteLine($"Standard Deviation: {NumberUtils.StdDev(data):F2}");
            Console.WriteLine($"Variance: {NumberUtils.Variance(data):F2}");
            Console.WriteLine($"Range: {NumberUtils.Range(data)}");
            Console.WriteLine($"Sum of Squares: {NumberUtils.SumOfSquares(data):F2}");

            Console.WriteLine();
        }

        static void ValidationExamples()
        {
            Console.WriteLine("--- Validation Examples ---");

            // Number validation
            Console.WriteLine($"IsValidNumber(123): {NumberUtils.IsValidNumber(123)}");
            Console.WriteLine($"IsValidNumber(NaN): {NumberUtils.IsValidNumber(double.NaN)}");

            // Even/Odd
            Console.WriteLine($"IsEven(42): {NumberUtils.IsEven(42)}");
            Console.WriteLine($"IsOdd(42): {NumberUtils.IsOdd(42)}");

            // Prime
            Console.WriteLine($"IsPrime(7): {NumberUtils.IsPrime(7)}");
            Console.WriteLine($"IsPrime(100): {NumberUtils.IsPrime(100)}");

            // Perfect square/cube
            Console.WriteLine($"IsPerfectSquare(144): {NumberUtils.IsPerfectSquare(144)}");
            Console.WriteLine($"IsPerfectCube(27): {NumberUtils.IsPerfectCube(27)}");

            // Range
            Console.WriteLine($"IsBetween(5, 0, 10): {NumberUtils.IsBetween(5, 0, 10)}");

            Console.WriteLine();
        }

        static void ParsingExamples()
        {
            Console.WriteLine("--- Parsing Examples ---");

            // Parse with default
            Console.WriteLine($"Parse '123.45': {NumberUtils.ParseOrDefault("123.45")}");
            Console.WriteLine($"Parse 'invalid': {NumberUtils.ParseOrDefault("invalid", -1)}");

            // Parse int
            Console.WriteLine($"ParseInt '42': {NumberUtils.ParseIntOrDefault("42")}");
            Console.WriteLine($"ParseInt 'abc': {NumberUtils.ParseIntOrDefault("abc", 0)}");

            // TryParse
            double result;
            if (NumberUtils.TryParse("3.14159", out result))
            {
                Console.WriteLine($"TryParse '3.14159': {result}");
            }

            Console.WriteLine();
        }

        static void UtilityExamples()
        {
            Console.WriteLine("--- Utility Examples ---");

            // GCD and LCM
            Console.WriteLine($"GCD(24, 36): {NumberUtils.Gcd(24, 36)}");
            Console.WriteLine($"LCM(24, 36): {NumberUtils.Lcm(24, 36)}");

            // Factorial
            Console.WriteLine($"Factorial(5): {NumberUtils.Factorial(5)}");
            Console.WriteLine($"Factorial(10): {NumberUtils.Factorial(10)}");

            // Fibonacci
            Console.WriteLine($"Fibonacci(10): {NumberUtils.Fibonacci(10)}");
            Console.WriteLine($"Fibonacci(20): {NumberUtils.Fibonacci(20)}");

            // Digit operations
            Console.WriteLine($"SumOfDigits(12345): {NumberUtils.SumOfDigits(12345)}");
            Console.WriteLine($"ReverseDigits(12345): {NumberUtils.ReverseDigits(12345)}");
            Console.WriteLine($"IsPalindrome(12321): {NumberUtils.IsPalindrome(12321)}");

            // Angle conversions
            Console.WriteLine($"DegreesToRadians(180): {NumberUtils.DegreesToRadians(180):F4}");
            Console.WriteLine($"RadiansToDegrees(PI): {NumberUtils.RadiansToDegrees(Math.PI):F2}");
            Console.WriteLine($"NormalizeAngle(450): {NumberUtils.NormalizeAngle(450)}");

            Console.WriteLine();
        }

        static void RandomExamples()
        {
            Console.WriteLine("--- Random Examples ---");

            // Random double
            Console.WriteLine($"Random [0,1): {NumberUtils.Random():F4}");
            Console.WriteLine($"Random [5,10): {NumberUtils.Random(5, 10):F2}");

            // Random int
            Console.WriteLine($"RandomInt [1,6]: {NumberUtils.RandomInt(1, 6)}");
            Console.WriteLine($"RandomInt [1,6]: {NumberUtils.RandomInt(1, 6)}");

            // Random normal
            Console.WriteLine($"RandomNormal(0,1): {NumberUtils.RandomNormal(0, 1):F4}");
            Console.WriteLine($"RandomNormal(100,15): {NumberUtils.RandomNormal(100, 15):F2}");

            Console.WriteLine();
        }
    }
}