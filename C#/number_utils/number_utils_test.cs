using System;
using System.Collections.Generic;
using System.Globalization;
using AllToolkit;

namespace NumberUtilsTest
{
    class Program
    {
        static int passed = 0;
        static int failed = 0;

        static void Main(string[] args)
        {
            Console.WriteLine("=== NumberUtils Test Suite ===\n");

            TestFormatting();
            TestBaseConversion();
            TestRomanNumerals();
            TestMathematicalOperations();
            TestStatisticalFunctions();
            TestValidation();
            TestParsing();
            TestUtilityFunctions();
            TestRandomGeneration();

            Console.WriteLine($"\n=== Results ===");
            Console.WriteLine($"Passed: {passed}");
            Console.WriteLine($"Failed: {failed}");
            Console.WriteLine($"Total: {passed + failed}");

            Environment.Exit(failed > 0 ? 1 : 0);
        }

        static void Assert(bool condition, string testName)
        {
            if (condition)
            {
                Console.WriteLine($"✓ {testName}");
                passed++;
            }
            else
            {
                Console.WriteLine($"✗ {testName}");
                failed++;
            }
        }

        static void AssertEqual<T>(T expected, T actual, string testName)
        {
            if (Equals(expected, actual))
            {
                Console.WriteLine($"✓ {testName}");
                passed++;
            }
            else
            {
                Console.WriteLine($"✗ {testName}: Expected '{expected}', got '{actual}'");
                failed++;
            }
        }

        static void AssertApprox(double expected, double actual, double epsilon, string testName)
        {
            if (Math.Abs(expected - actual) < epsilon)
            {
                Console.WriteLine($"✓ {testName}");
                passed++;
            }
            else
            {
                Console.WriteLine($"✗ {testName}: Expected ~{expected}, got {actual}");
                failed++;
            }
        }

        static void TestFormatting()
        {
            Console.WriteLine("\n--- Formatting Tests ---");

            // Format
            AssertEqual("1,234,567.89", NumberUtils.Format(1234567.89, 2, CultureInfo.InvariantCulture), "Format with 2 decimals");
            AssertEqual("1,234,568", NumberUtils.Format(1234567.89, 0, CultureInfo.InvariantCulture), "Format with 0 decimals");

            // Currency
            AssertEqual("$1,234.56", NumberUtils.Currency(1234.56), "Currency default");
            AssertEqual("€1,234.56", NumberUtils.Currency(1234.56, "€"), "Currency with euro");
            AssertEqual("$1,235", NumberUtils.Currency(1234.56, "$", 0), "Currency no decimals");

            // Percentage
            AssertEqual("15%", NumberUtils.Percentage(0.15), "Percentage default");
            AssertEqual("15.50%", NumberUtils.Percentage(0.155, 2), "Percentage with decimals");
            AssertEqual("15.5", NumberUtils.Percentage(0.155, 1, false), "Percentage without symbol");

            // Compact
            AssertEqual("1.5K", NumberUtils.Compact(1500), "Compact thousands");
            AssertEqual("1.5M", NumberUtils.Compact(1500000), "Compact millions");
            AssertEqual("1.5B", NumberUtils.Compact(1500000000), "Compact billions");
            AssertEqual("1.5T", NumberUtils.Compact(1500000000000L), "Compact trillions");
            AssertEqual("500", NumberUtils.Compact(500), "Compact small number");

            // Ordinal
            AssertEqual("1st", NumberUtils.ToOrdinal(1), "Ordinal 1st");
            AssertEqual("2nd", NumberUtils.ToOrdinal(2), "Ordinal 2nd");
            AssertEqual("3rd", NumberUtils.ToOrdinal(3), "Ordinal 3rd");
            AssertEqual("4th", NumberUtils.ToOrdinal(4), "Ordinal 4th");
            AssertEqual("11th", NumberUtils.ToOrdinal(11), "Ordinal 11th");
            AssertEqual("12th", NumberUtils.ToOrdinal(12), "Ordinal 12th");
            AssertEqual("13th", NumberUtils.ToOrdinal(13), "Ordinal 13th");
            AssertEqual("21st", NumberUtils.ToOrdinal(21), "Ordinal 21st");
            AssertEqual("101st", NumberUtils.ToOrdinal(101), "Ordinal 101st");

            // ToWords
            AssertEqual("zero", NumberUtils.ToWords(0), "Words zero");
            AssertEqual("one", NumberUtils.ToWords(1), "Words one");
            AssertEqual("twenty-one", NumberUtils.ToWords(21), "Words twenty-one");
            AssertEqual("one hundred", NumberUtils.ToWords(100), "Words one hundred");
            AssertEqual("one hundred twenty-three", NumberUtils.ToWords(123), "Words one hundred twenty-three");
            AssertEqual("one thousand", NumberUtils.ToWords(1000), "Words one thousand");
            AssertEqual("one thousand two hundred thirty-four", NumberUtils.ToWords(1234), "Words one thousand two hundred thirty-four");
            AssertEqual("negative five", NumberUtils.ToWords(-5), "Words negative");
        }

        static void TestBaseConversion()
        {
            Console.WriteLine("\n--- Base Conversion Tests ---");

            // ToBinary
            AssertEqual("1010", NumberUtils.ToBinary(10), "ToBinary 10");
            AssertEqual("0b1010", NumberUtils.ToBinary(10, 0, true), "ToBinary with prefix");
            AssertEqual("00001010", NumberUtils.ToBinary(10, 8), "ToBinary with padding");

            // ToHex
            AssertEqual("ff", NumberUtils.ToHex(255), "ToHex 255");
            AssertEqual("FF", NumberUtils.ToHex(255, 0, true), "ToHex uppercase");
            AssertEqual("0x00ff", NumberUtils.ToHex(255, 4, false, true), "ToHex with prefix");

            // ToOctal
            AssertEqual("77", NumberUtils.ToOctal(63), "ToOctal 63");
            AssertEqual("0o77", NumberUtils.ToOctal(63, 0, true), "ToOctal with prefix");

            // FromBinary
            AssertEqual(10L, NumberUtils.FromBinary("1010"), "FromBinary 1010");
            AssertEqual(10L, NumberUtils.FromBinary("0b1010"), "FromBinary with prefix");
            AssertEqual(10L, NumberUtils.FromBinary(" 1010 "), "FromBinary with whitespace");

            // FromHex
            AssertEqual(255L, NumberUtils.FromHex("ff"), "FromHex ff");
            AssertEqual(255L, NumberUtils.FromHex("FF"), "FromHex FF");
            AssertEqual(255L, NumberUtils.FromHex("0xFF"), "FromHex with prefix");

            // FromOctal
            AssertEqual(63L, NumberUtils.FromOctal("77"), "FromOctal 77");
            AssertEqual(63L, NumberUtils.FromOctal("0o77"), "FromOctal with prefix");
        }

        static void TestRomanNumerals()
        {
            Console.WriteLine("\n--- Roman Numeral Tests ---");

            // ToRoman
            AssertEqual("I", NumberUtils.ToRoman(1), "Roman 1");
            AssertEqual("IV", NumberUtils.ToRoman(4), "Roman 4");
            AssertEqual("V", NumberUtils.ToRoman(5), "Roman 5");
            AssertEqual("IX", NumberUtils.ToRoman(9), "Roman 9");
            AssertEqual("X", NumberUtils.ToRoman(10), "Roman 10");
            AssertEqual("XL", NumberUtils.ToRoman(40), "Roman 40");
            AssertEqual("L", NumberUtils.ToRoman(50), "Roman 50");
            AssertEqual("XC", NumberUtils.ToRoman(90), "Roman 90");
            AssertEqual("C", NumberUtils.ToRoman(100), "Roman 100");
            AssertEqual("CD", NumberUtils.ToRoman(400), "Roman 400");
            AssertEqual("D", NumberUtils.ToRoman(500), "Roman 500");
            AssertEqual("CM", NumberUtils.ToRoman(900), "Roman 900");
            AssertEqual("M", NumberUtils.ToRoman(1000), "Roman 1000");
            AssertEqual("MMXXIV", NumberUtils.ToRoman(2024), "Roman 2024");

            // FromRoman
            AssertEqual(1, NumberUtils.FromRoman("I"), "FromRoman I");
            AssertEqual(4, NumberUtils.FromRoman("IV"), "FromRoman IV");
            AssertEqual(5, NumberUtils.FromRoman("V"), "FromRoman V");
            AssertEqual(9, NumberUtils.FromRoman("IX"), "FromRoman IX");
            AssertEqual(10, NumberUtils.FromRoman("X"), "FromRoman X");
            AssertEqual(2024, NumberUtils.FromRoman("MMXXIV"), "FromRoman MMXXIV");
            AssertEqual(2024, NumberUtils.FromRoman("mmxxiv"), "FromRoman lowercase");
        }

        static void TestMathematicalOperations()
        {
            Console.WriteLine("\n--- Mathematical Operations Tests ---");

            // Clamp
            AssertEqual(5.0, NumberUtils.Clamp(5, 0, 10), "Clamp within range");
            AssertEqual(0.0, NumberUtils.Clamp(-5, 0, 10), "Clamp below min");
            AssertEqual(10.0, NumberUtils.Clamp(15, 0, 10), "Clamp above max");

            // Lerp
            AssertEqual(50.0, NumberUtils.Lerp(0, 100, 0.5), "Lerp middle");
            AssertEqual(0.0, NumberUtils.Lerp(0, 100, 0), "Lerp start");
            AssertEqual(100.0, NumberUtils.Lerp(0, 100, 1), "Lerp end");
            AssertEqual(25.0, NumberUtils.Lerp(0, 100, 0.25), "Lerp quarter");

            // MapRange
            AssertEqual(50.0, NumberUtils.MapRange(5, 0, 10, 0, 100), "MapRange simple");
            AssertEqual(0.0, NumberUtils.MapRange(0, 0, 10, 0, 100), "MapRange start");
            AssertEqual(100.0, NumberUtils.MapRange(10, 0, 10, 0, 100), "MapRange end");
            AssertEqual(-40.0, NumberUtils.MapRange(0, 32, 212, 0, 100), "MapRange Fahrenheit to Celsius");

            // ApproxEqual
            Assert(NumberUtils.ApproxEqual(0.1 + 0.2, 0.3), "ApproxEqual floating point");
            Assert(!NumberUtils.ApproxEqual(1.0, 2.0), "ApproxEqual different");
            Assert(NumberUtils.ApproxEqual(1.0, 1.000000001, 1e-6), "ApproxEqual with tolerance");

            // RoundToMultiple
            AssertEqual(10.0, NumberUtils.RoundToMultiple(8, 5), "RoundToMultiple 8 to 5");
            AssertEqual(15.0, NumberUtils.RoundToMultiple(13, 5), "RoundToMultiple 13 to 5");
            AssertEqual(100.0, NumberUtils.RoundToMultiple(97, 25), "RoundToMultiple 97 to 25");

            // RoundToSignificantFigures
            AssertEqual(1230.0, NumberUtils.RoundToSignificantFigures(1234, 3), "RoundToSigFig 1234 to 3");
            AssertEqual(0.00123, NumberUtils.RoundToSignificantFigures(0.001234, 3), "RoundToSigFig small");
        }

        static void TestStatisticalFunctions()
        {
            Console.WriteLine("\n--- Statistical Functions Tests ---");

            var data = new List<double> { 1, 2, 3, 4, 5 };
            var data2 = new List<double> { 1, 2, 2, 3, 4 };

            // Mean
            AssertEqual(3.0, NumberUtils.Mean(data), "Mean of 1-5");

            // Median
            AssertEqual(3.0, NumberUtils.Median(data), "Median of 1-5 (odd)");
            AssertEqual(2.5, NumberUtils.Median(new List<double> { 1, 2, 3, 4 }), "Median of 1-4 (even)");

            // Mode
            AssertEqual(null, NumberUtils.Mode(data), "Mode of 1-5 (no unique)");
            AssertEqual(2.0, NumberUtils.Mode(data2), "Mode of data2");

            // StdDev
            AssertApprox(1.414, NumberUtils.StdDev(data), 0.01, "StdDev population");
            AssertApprox(1.581, NumberUtils.StdDev(data, true), 0.01, "StdDev sample");

            // Variance
            AssertApprox(2.0, NumberUtils.Variance(data), 0.01, "Variance population");

            // Range
            AssertEqual(4.0, NumberUtils.Range(data), "Range of 1-5");

            // SumOfSquares
            AssertEqual(55.0, NumberUtils.SumOfSquares(data), "SumOfSquares of 1-5");
        }

        static void TestValidation()
        {
            Console.WriteLine("\n--- Validation Tests ---");

            // IsValidNumber
            Assert(NumberUtils.IsValidNumber(123), "IsValidNumber 123");
            Assert(!NumberUtils.IsValidNumber(double.NaN), "IsValidNumber NaN");
            Assert(!NumberUtils.IsValidNumber(double.PositiveInfinity), "IsValidNumber Infinity");

            // IsEven/IsOdd
            Assert(NumberUtils.IsEven(4), "IsEven 4");
            Assert(!NumberUtils.IsEven(5), "IsEven 5");
            Assert(NumberUtils.IsOdd(5), "IsOdd 5");
            Assert(!NumberUtils.IsOdd(4), "IsOdd 4");

            // IsPositive/IsNegative/IsZero
            Assert(NumberUtils.IsPositive(5), "IsPositive 5");
            Assert(NumberUtils.IsNegative(-5), "IsNegative -5");
            Assert(NumberUtils.IsZero(0), "IsZero 0");

            // IsBetween
            Assert(NumberUtils.IsBetween(5, 0, 10), "IsBetween 5 in 0-10");
            Assert(NumberUtils.IsBetween(0, 0, 10), "IsBetween 0 in 0-10 (inclusive)");
            Assert(NumberUtils.IsBetween(10, 0, 10), "IsBetween 10 in 0-10 (inclusive)");
            Assert(!NumberUtils.IsBetween(-1, 0, 10), "IsBetween -1 not in 0-10");

            // IsPrime
            Assert(!NumberUtils.IsPrime(0), "IsPrime 0");
            Assert(!NumberUtils.IsPrime(1), "IsPrime 1");
            Assert(NumberUtils.IsPrime(2), "IsPrime 2");
            Assert(NumberUtils.IsPrime(3), "IsPrime 3");
            Assert(!NumberUtils.IsPrime(4), "IsPrime 4");
            Assert(NumberUtils.IsPrime(7), "IsPrime 7");
            Assert(NumberUtils.IsPrime(97), "IsPrime 97");

            // IsPerfectSquare
            Assert(NumberUtils.IsPerfectSquare(0), "IsPerfectSquare 0");
            Assert(NumberUtils.IsPerfectSquare(1), "IsPerfectSquare 1");
            Assert(NumberUtils.IsPerfectSquare(4), "IsPerfectSquare 4");
            Assert(NumberUtils.IsPerfectSquare(16), "IsPerfectSquare 16");
            Assert(!NumberUtils.IsPerfectSquare(15), "IsPerfectSquare 15");

            // IsPerfectCube
            Assert(NumberUtils.IsPerfectCube(0), "IsPerfectCube 0");
            Assert(NumberUtils.IsPerfectCube(1), "IsPerfectCube 1");
            Assert(NumberUtils.IsPerfectCube(8), "IsPerfectCube 8");
            Assert(NumberUtils.IsPerfectCube(27), "IsPerfectCube 27");
            Assert(!NumberUtils.IsPerfectCube(9), "IsPerfectCube 9");
        }

        static void TestParsing()
        {
            Console.WriteLine("\n--- Parsing Tests ---");

            // ParseOrDefault
            AssertEqual(123.45, NumberUtils.ParseOrDefault("123.45"), "ParseOrDefault valid");
            AssertEqual(0.0, NumberUtils.ParseOrDefault("invalid"), "ParseOrDefault invalid");
            AssertEqual(42.0, NumberUtils.ParseOrDefault("invalid", 42), "ParseOrDefault with default");

            // ParseIntOrDefault
            AssertEqual(123, NumberUtils.ParseIntOrDefault("123"), "ParseIntOrDefault valid");
            AssertEqual(0, NumberUtils.ParseIntOrDefault("invalid"), "ParseIntOrDefault invalid");

            // ParseLongOrDefault
            AssertEqual(123456789012L, NumberUtils.ParseLongOrDefault("123456789012"), "ParseLongOrDefault valid");
            AssertEqual(0L, NumberUtils.ParseLongOrDefault("invalid"), "ParseLongOrDefault invalid");

            // TryParse
            double result;
            Assert(NumberUtils.TryParse("123.45", out result), "TryParse valid");
            AssertEqual(123.45, result, "TryParse result");
            Assert(!NumberUtils.TryParse("invalid", out result), "TryParse invalid");
        }

        static void TestUtilityFunctions()
        {
            Console.WriteLine("\n--- Utility Functions Tests ---");

            // Gcd
            AssertEqual(12L, NumberUtils.Gcd(24, 36), "Gcd 24, 36");
            AssertEqual(1L, NumberUtils.Gcd(17, 5), "Gcd 17, 5");
            AssertEqual(5L, NumberUtils.Gcd(0, 5), "Gcd 0, 5");
            AssertEqual(12L, NumberUtils.Gcd(-24, 36), "Gcd -24, 36");

            // Lcm
            AssertEqual(72L, NumberUtils.Lcm(24, 36), "Lcm 24, 36");
            AssertEqual(85L, NumberUtils.Lcm(17, 5), "Lcm 17, 5");
            AssertEqual(0L, NumberUtils.Lcm(0, 5), "Lcm 0, 5");

            // Factorial
            AssertEqual(1L, NumberUtils.Factorial(0), "Factorial 0");
            AssertEqual(1L, NumberUtils.Factorial(1), "Factorial 1");
            AssertEqual(120L, NumberUtils.Factorial(5), "Factorial 5");
            AssertEqual(3628800L, NumberUtils.Factorial(10), "Factorial 10");

            // Fibonacci
            AssertEqual(0L, NumberUtils.Fibonacci(0), "Fibonacci 0");
            AssertEqual(1L, NumberUtils.Fibonacci(1), "Fibonacci 1");
            AssertEqual(1L, NumberUtils.Fibonacci(2), "Fibonacci 2");
            AssertEqual(55L, NumberUtils.Fibonacci(10), "Fibonacci 10");
            AssertEqual(6765L, NumberUtils.Fibonacci(20), "Fibonacci 20");

            // SumOfDigits
            AssertEqual(6, NumberUtils.SumOfDigits(123), "SumOfDigits 123");
            AssertEqual(1, NumberUtils.SumOfDigits(1000), "SumOfDigits 1000");
            AssertEqual(6, NumberUtils.SumOfDigits(-123), "SumOfDigits -123");

            // ReverseDigits
            AssertEqual(321L, NumberUtils.ReverseDigits(123), "ReverseDigits 123");
            AssertEqual(1L, NumberUtils.ReverseDigits(1000), "ReverseDigits 1000");
            AssertEqual(-321L, NumberUtils.ReverseDigits(-123), "ReverseDigits -123");

            // IsPalindrome
            Assert(NumberUtils.IsPalindrome(121), "IsPalindrome 121");
            Assert(NumberUtils.IsPalindrome(1), "IsPalindrome 1");
            Assert(!NumberUtils.IsPalindrome(123), "IsPalindrome 123");

            // DegreesToRadians/RadiansToDegrees
            AssertApprox(Math.PI, NumberUtils.DegreesToRadians(180), 0.0001, "DegreesToRadians 180");
            AssertApprox(180.0, NumberUtils.RadiansToDegrees(Math.PI), 0.0001, "RadiansToDegrees PI");

            // NormalizeAngle
            AssertEqual(90.0, NumberUtils.NormalizeAngle(90), "NormalizeAngle 90");
            AssertEqual(90.0, NumberUtils.NormalizeAngle(450), "NormalizeAngle 450");
            AssertEqual(270.0, NumberUtils.NormalizeAngle(-90), "NormalizeAngle -90");
        }

        static void TestRandomGeneration()
        {
            Console.WriteLine("\n--- Random Generation Tests ---");

            // Random (double)
            for (int i = 0; i < 10; i++)
            {
                var r = NumberUtils.Random(0, 1);
                Assert(r >= 0 && r < 1, $"Random in range [0,1): {r}");
            }

            var r5to10 = NumberUtils.Random(5, 10);
            Assert(r5to10 >= 5 && r5to10 < 10, "Random in range [5,10)");

            // RandomInt
            for (int i = 0; i < 10; i++)
            {
                var r = NumberUtils.RandomInt(1, 6);
                Assert(r >= 1 && r <= 6, $"RandomInt in range [1,6]: {r}");
            }

            // RandomNormal
            for (int i = 0; i < 10; i++)
            {
                var r = NumberUtils.RandomNormal(0, 1);
                Assert(!double.IsNaN(r) && !double.IsInfinity(r), $"RandomNormal valid: {r}");
            }
        }
    }
}
