using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace AllToolkit
{
    /// <summary>
    /// Number utilities for formatting, conversion, mathematical operations, and statistical functions.
    /// Zero dependencies - uses only .NET standard library.
    /// </summary>
    public static class NumberUtils
    {
        #region Formatting

        /// <summary>
        /// Formats a number with thousands separator.
        /// </summary>
        /// <param name="number">The number to format</param>
        /// <param name="decimalPlaces">Number of decimal places (null for auto)</param>
        /// <param name="culture">Culture info for formatting (default: current culture)</param>
        /// <returns>Formatted string (e.g., "1,234,567.89")</returns>
        public static string Format(double number, int? decimalPlaces = null, CultureInfo culture = null)
        {
            culture ??= CultureInfo.CurrentCulture;
            var format = decimalPlaces.HasValue
                ? $"N{decimalPlaces.Value}"
                : "N";
            return number.ToString(format, culture);
        }

        /// <summary>
        /// Formats a number as currency.
        /// </summary>
        /// <param name="amount">The amount to format</param>
        /// <param name="symbol">Currency symbol (default: "$")</param>
        /// <param name="decimalPlaces">Number of decimal places (default: 2)</param>
        /// <returns>Formatted currency string (e.g., "$1,234.56")</returns>
        public static string Currency(double amount, string symbol = "$", int decimalPlaces = 2)
        {
            var formatted = Format(amount, decimalPlaces);
            return $"{symbol}{formatted}";
        }

        /// <summary>
        /// Formats a number as percentage.
        /// </summary>
        /// <param name="value">The value to format (0.15 = 15%)</param>
        /// <param name="decimalPlaces">Number of decimal places (default: 0)</param>
        /// <param name="includeSymbol">Whether to include % symbol</param>
        /// <returns>Formatted percentage string (e.g., "15.5%")</returns>
        public static string Percentage(double value, int decimalPlaces = 0, bool includeSymbol = true)
        {
            var percent = value * 100;
            var formatted = Format(percent, decimalPlaces);
            return includeSymbol ? $"{formatted}%" : formatted;
        }

        /// <summary>
        /// Formats a number in compact notation (K, M, B, T).
        /// </summary>
        /// <param name="number">The number to format</param>
        /// <param name="decimalPlaces">Number of decimal places (default: 1)</param>
        /// <returns>Compact notation string (e.g., "1.5M")</returns>
        public static string Compact(double number, int decimalPlaces = 1)
        {
            var abs = Math.Abs(number);
            string suffix;
            double divisor;

            if (abs >= 1_000_000_000_000)
            {
                suffix = "T";
                divisor = 1_000_000_000_000;
            }
            else if (abs >= 1_000_000_000)
            {
                suffix = "B";
                divisor = 1_000_000_000;
            }
            else if (abs >= 1_000_000)
            {
                suffix = "M";
                divisor = 1_000_000;
            }
            else if (abs >= 1_000)
            {
                suffix = "K";
                divisor = 1_000;
            }
            else
            {
                return Format(number, decimalPlaces);
            }

            var result = number / divisor;
            return $"{Format(result, decimalPlaces)}{suffix}";
        }

        /// <summary>
        /// Converts a number to its ordinal representation.
        /// </summary>
        /// <param name="number">The number to convert</param>
        /// <returns>Ordinal string (e.g., "1st", "2nd", "3rd")</returns>
        public static string ToOrdinal(int number)
        {
            if (number < 0) number = -number;

            var lastTwo = number % 100;
            if (lastTwo >= 11 && lastTwo <= 13)
                return $"{number}th";

            return (number % 10) switch
            {
                1 => $"{number}st",
                2 => $"{number}nd",
                3 => $"{number}rd",
                _ => $"{number}th"
            };
        }

        /// <summary>
        /// Converts a number to English words.
        /// </summary>
        /// <param name="number">The number to convert (0-999,999,999,999)</param>
        /// <returns>Number in words (e.g., "one hundred twenty-three")</returns>
        public static string ToWords(long number)
        {
            if (number == 0) return "zero";
            if (number < 0) return "negative " + ToWords(-number);
            if (number > 999_999_999_999) throw new ArgumentOutOfRangeException(nameof(number), "Number too large");

            var parts = new List<string>();

            if (number >= 1_000_000_000)
            {
                parts.Add(ToWords(number / 1_000_000_000) + " billion");
                number %= 1_000_000_000;
            }

            if (number >= 1_000_000)
            {
                parts.Add(ToWords(number / 1_000_000) + " million");
                number %= 1_000_000;
            }

            if (number >= 1_000)
            {
                parts.Add(ToWords(number / 1_000) + " thousand");
                number %= 1_000;
            }

            if (number > 0)
            {
                parts.Add(ToWordsUnderThousand((int)number));
            }

            return string.Join(" ", parts);
        }

        private static string ToWordsUnderThousand(int number)
        {
            var units = new[] { "", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine" };
            var teens = new[] { "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen" };
            var tens = new[] { "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety" };

            var parts = new List<string>();

            if (number >= 100)
            {
                parts.Add(units[number / 100] + " hundred");
                number %= 100;
            }

            if (number >= 20)
            {
                var tenPart = tens[number / 10];
                var unitPart = units[number % 10];
                parts.Add(unitPart == "" ? tenPart : $"{tenPart}-{unitPart}");
            }
            else if (number >= 10)
            {
                parts.Add(teens[number - 10]);
            }
            else if (number > 0)
            {
                parts.Add(units[number]);
            }

            return string.Join(" ", parts);
        }

        #endregion

        #region Number Base Conversion

        /// <summary>
        /// Converts a number to binary string.
        /// </summary>
        /// <param name="number">The number to convert</param>
        /// <param name="minDigits">Minimum number of digits (padded with zeros)</param>
        /// <param name="prefix">Whether to add "0b" prefix</param>
        /// <returns>Binary string (e.g., "0b1010")</returns>
        public static string ToBinary(long number, int minDigits = 0, bool prefix = false)
        {
            var binary = Convert.ToString(number, 2);
            if (binary.Length < minDigits)
                binary = binary.PadLeft(minDigits, '0');
            return prefix ? $"0b{binary}" : binary;
        }

        /// <summary>
        /// Converts a number to hexadecimal string.
        /// </summary>
        /// <param name="number">The number to convert</param>
        /// <param name="minDigits">Minimum number of digits (padded with zeros)</param>
        /// <param name="uppercase">Whether to use uppercase letters</param>
        /// <param name="prefix">Whether to add "0x" prefix</param>
        /// <returns>Hex string (e.g., "0xFF")</returns>
        public static string ToHex(long number, int minDigits = 0, bool uppercase = false, bool prefix = false)
        {
            var format = uppercase ? "X" : "x";
            var hex = number.ToString(format);
            if (hex.Length < minDigits)
                hex = hex.PadLeft(minDigits, '0');
            return prefix ? $"0x{hex}" : hex;
        }

        /// <summary>
        /// Converts a number to octal string.
        /// </summary>
        /// <param name="number">The number to convert</param>
        /// <param name="minDigits">Minimum number of digits (padded with zeros)</param>
        /// <param name="prefix">Whether to add "0o" prefix</param>
        /// <returns>Octal string (e.g., "0o77")</returns>
        public static string ToOctal(long number, int minDigits = 0, bool prefix = false)
        {
            var octal = Convert.ToString(number, 8);
            if (octal.Length < minDigits)
                octal = octal.PadLeft(minDigits, '0');
            return prefix ? $"0o{octal}" : octal;
        }

        /// <summary>
        /// Parses a binary string to number.
        /// </summary>
        /// <param name="binary">Binary string (with or without "0b" prefix)</param>
        /// <returns>Parsed number</returns>
        public static long FromBinary(string binary)
        {
            if (string.IsNullOrWhiteSpace(binary))
                throw new ArgumentException("Binary string cannot be empty", nameof(binary));

            binary = binary.Trim().Replace("0b", "").Replace("0B", "");
            return Convert.ToInt64(binary, 2);
        }

        /// <summary>
        /// Parses a hexadecimal string to number.
        /// </summary>
        /// <param name="hex">Hex string (with or without "0x" prefix)</param>
        /// <returns>Parsed number</returns>
        public static long FromHex(string hex)
        {
            if (string.IsNullOrWhiteSpace(hex))
                throw new ArgumentException("Hex string cannot be empty", nameof(hex));

            hex = hex.Trim().Replace("0x", "").Replace("0X", "");
            return Convert.ToInt64(hex, 16);
        }

        /// <summary>
        /// Parses an octal string to number.
        /// </summary>
        /// <param name="octal">Octal string (with or without "0o" prefix)</param>
        /// <returns>Parsed number</returns>
        public static long FromOctal(string octal)
        {
            if (string.IsNullOrWhiteSpace(octal))
                throw new ArgumentException("Octal string cannot be empty", nameof(octal));

            octal = octal.Trim().Replace("0o", "").Replace("0O", "");
            return Convert.ToInt64(octal, 8);
        }

        #endregion

        #region Roman Numerals

        private static readonly (int value, string symbol)[] RomanMap = new[]
        {
            (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
        };

        /// <summary>
        /// Converts a number to Roman numeral.
        /// </summary>
        /// <param name="number">The number to convert (1-3999)</param>
        /// <returns>Roman numeral string (e.g., "MMXXIV")</returns>
        public static string ToRoman(int number)
        {
            if (number < 1 || number > 3999)
                throw new ArgumentOutOfRangeException(nameof(number), "Roman numerals support 1-3999");

            var result = new StringBuilder();
            var remaining = number;

            foreach (var (value, symbol) in RomanMap)
            {
                while (remaining >= value)
                {
                    result.Append(symbol);
                    remaining -= value;
                }
            }

            return result.ToString();
        }

        /// <summary>
        /// Parses a Roman numeral to number.
        /// </summary>
        /// <param name="roman">Roman numeral string (e.g., "MMXXIV")</param>
        /// <returns>Parsed number</returns>
        public static int FromRoman(string roman)
        {
            if (string.IsNullOrWhiteSpace(roman))
                throw new ArgumentException("Roman numeral cannot be empty", nameof(roman));

            roman = roman.ToUpper().Trim();
            var values = new Dictionary<char, int>
            {
                ['I'] = 1, ['V'] = 5, ['X'] = 10, ['L'] = 50,
                ['C'] = 100, ['D'] = 500, ['M'] = 1000
            };

            var result = 0;
            var prevValue = 0;

            for (int i = roman.Length - 1; i >= 0; i--)
            {
                if (!values.TryGetValue(roman[i], out var value))
                    throw new ArgumentException($"Invalid character in Roman numeral: {roman[i]}", nameof(roman));

                if (value < prevValue)
                    result -= value;
                else
                    result += value;

                prevValue = value;
            }

            return result;
        }

        #endregion

        #region Mathematical Operations

        /// <summary>
        /// Clamps a value between minimum and maximum.
        /// </summary>
        /// <param name="value">The value to clamp</param>
        /// <param name="min">Minimum allowed value</param>
        /// <param name="max">Maximum allowed value</param>
        /// <returns>Clamped value</returns>
        public static double Clamp(double value, double min, double max)
        {
            if (min > max) throw new ArgumentException("Min cannot be greater than max");
            return Math.Max(min, Math.Min(max, value));
        }

        /// <summary>
        /// Linear interpolation between two values.
        /// </summary>
        /// <param name="start">Start value</param>
        /// <param name="end">End value</param>
        /// <param name="t">Interpolation factor (0.0 to 1.0)</param>
        /// <returns>Interpolated value</returns>
        public static double Lerp(double start, double end, double t)
        {
            t = Clamp(t, 0, 1);
            return start + (end - start) * t;
        }

        /// <summary>
        /// Maps a value from one range to another.
        /// </summary>
        /// <param name="value">The value to map</param>
        /// <param name="inMin">Input range minimum</param>
        /// <param name="inMax">Input range maximum</param>
        /// <param name="outMin">Output range minimum</param>
        /// <param name="outMax">Output range maximum</param>
        /// <returns>Mapped value</returns>
        public static double MapRange(double value, double inMin, double inMax, double outMin, double outMax)
        {
            if (inMin == inMax) throw new ArgumentException("Input range cannot be zero");
            var t = (value - inMin) / (inMax - inMin);
            return outMin + t * (outMax - outMin);
        }

        /// <summary>
        /// Checks if two numbers are approximately equal.
        /// </summary>
        /// <param name="a">First number</param>
        /// <param name="b">Second number</param>
        /// <param name="epsilon">Tolerance (default: 1e-9)</param>
        /// <returns>True if approximately equal</returns>
        public static bool ApproxEqual(double a, double b, double epsilon = 1e-9)
        {
            return Math.Abs(a - b) < epsilon;
        }

        /// <summary>
        /// Rounds to the nearest multiple.
        /// </summary>
        /// <param name="value">The value to round</param>
        /// <param name="multiple">The multiple to round to</param>
        /// <returns>Rounded value</returns>
        public static double RoundToMultiple(double value, double multiple)
        {
            if (multiple == 0) throw new ArgumentException("Multiple cannot be zero");
            return Math.Round(value / multiple) * multiple;
        }

        /// <summary>
        /// Rounds to a specific number of significant figures.
        /// </summary>
        /// <param name="value">The value to round</param>
        /// <param name="significantFigures">Number of significant figures</param>
        /// <returns>Rounded value</returns>
        public static double RoundToSignificantFigures(double value, int significantFigures)
        {
            if (significantFigures < 1) throw new ArgumentException("Significant figures must be at least 1");
            if (value == 0) return 0;

            var d = Math.Ceiling(Math.Log10(Math.Abs(value)));
            var power = significantFigures - (int)d;
            var magnitude = Math.Pow(10, power);
            return Math.Round(value * magnitude) / magnitude;
        }

        #endregion

        #region Statistical Functions

        /// <summary>
        /// Calculates the arithmetic mean of a set of numbers.
        /// </summary>
        /// <param name="numbers">The numbers to average</param>
        /// <returns>The mean value</returns>
        public static double Mean(IEnumerable<double> numbers)
        {
            var list = numbers?.ToList() ?? throw new ArgumentNullException(nameof(numbers));
            if (list.Count == 0) throw new ArgumentException("Cannot calculate mean of empty collection");
            return list.Average();
        }

        /// <summary>
        /// Calculates the median of a set of numbers.
        /// </summary>
        /// <param name="numbers">The numbers</param>
        /// <returns>The median value</returns>
        public static double Median(IEnumerable<double> numbers)
        {
            var list = numbers?.ToList() ?? throw new ArgumentNullException(nameof(numbers));
            if (list.Count == 0) throw new ArgumentException("Cannot calculate median of empty collection");

            list.Sort();
            var count = list.Count;

            if (count % 2 == 1)
                return list[count / 2];

            return (list[count / 2 - 1] + list[count / 2]) / 2.0;
        }

        /// <summary>
        /// Calculates the mode (most frequent value) of a set of numbers.
        /// </summary>
        /// <param name="numbers">The numbers</param>
        /// <returns>The mode value, or null if no unique mode</returns>
        public static double? Mode(IEnumerable<double> numbers)
        {
            var list = numbers?.ToList() ?? throw new ArgumentNullException(nameof(numbers));
            if (list.Count == 0) return null;

            var groups = list.GroupBy(x => x).OrderByDescending(g => g.Count()).ToList();
            var maxCount = groups[0].Count();

            // If multiple values have the same max frequency, no unique mode
            if (groups.Count > 1 && groups[1].Count() == maxCount)
                return null;

            return groups[0].Key;
        }

        /// <summary>
        /// Calculates the standard deviation.
        /// </summary>
        /// <param name="numbers">The numbers</param>
        /// <param name="sample">True for sample standard deviation (n-1), false for population (n)</param>
        /// <returns>Standard deviation</returns>
        public static double StdDev(IEnumerable<double> numbers, bool sample = false)
        {
            var list = numbers?.ToList() ?? throw new ArgumentNullException(nameof(numbers));
            if (list.Count < 2) throw new ArgumentException("Need at least 2 values for standard deviation");

            var mean = list.Average();
            var sumSquares = list.Sum(x => (x - mean) * (x - mean));
            var divisor = sample ? list.Count - 1 : list.Count;

            return Math.Sqrt(sumSquares / divisor);
        }

        /// <summary>
        /// Calculates the variance.
        /// </summary>
        /// <param name="numbers">The numbers</param>
        /// <param name="sample">True for sample variance (n-1), false for population (n)</param>
        /// <returns>Variance</returns>
        public static double Variance(IEnumerable<double> numbers, bool sample = false)
        {
            var stdDev = StdDev(numbers, sample);
            return stdDev * stdDev;
        }

        /// <summary>
        /// Calculates the range (max - min).
        /// </summary>
        /// <param name="numbers">The numbers</param>
        /// <returns>Range value</returns>
        public static double Range(IEnumerable<double> numbers)
        {
            var list = numbers?.ToList() ?? throw new ArgumentNullException(nameof(numbers));
            if (list.Count == 0) throw new ArgumentException("Cannot calculate range of empty collection");
            return list.Max() - list.Min();
        }

        /// <summary>
        /// Calculates the sum of squares.
        /// </summary>
        /// <param name="numbers">The numbers</param>
        /// <returns>Sum of squares</returns>
        public static double SumOfSquares(IEnumerable<double> numbers)
        {
            var list = numbers?.ToList() ?? throw new ArgumentNullException(nameof(numbers));
            return list.Sum(x => x * x);
        }

        #endregion

        #region Validation

        /// <summary>
        /// Checks if a value is a valid number (not NaN or Infinity).
        /// </summary>
        /// <param name="value">The value to check</param>
        /// <returns>True if valid number</returns>
        public static bool IsValidNumber(double value)
        {
            return !double.IsNaN(value) && !double.IsInfinity(value);
        }

        /// <summary>
        /// Checks if a number is even.
        /// </summary>
        /// <param name="number">The number to check</param>
        /// <returns>True if even</returns>
        public static bool IsEven(int number) => number % 2 == 0;

        /// <summary>
        /// Checks if a number is odd.
        /// </summary>
        /// <param name="number">The number to check</param>
        /// <returns>True if odd</returns>
        public static bool IsOdd(int number) => number % 2 != 0;

        /// <summary>
        /// Checks if a number is positive.
        /// </summary>
        /// <param name="number">The number to check</param>
        /// <returns>True if positive</returns>
        public static bool IsPositive(double number) => number > 0;

        /// <summary>
        /// Checks if a number is negative.
        /// </summary>
        /// <param name="number">The number to check</param>
        /// <returns>True if negative</returns>
        public static bool IsNegative(double number) => number < 0;

        /// <summary>
        /// Checks if a number is zero.
        /// </summary>
        /// <param name="number">The number to check</param>
        /// <returns>True if zero</returns>
        public static bool IsZero(double number) => number == 0;

        /// <summary>
        /// Checks if a number is within a range (inclusive).
        /// </summary>
        /// <param name="number">The number to check</param>
        /// <param name="min">Minimum value</param>
        /// <param name="max">Maximum value</param>
        /// <returns>True if in range</returns>
        public static bool IsBetween(double number, double min, double max) => number >= min && number <= max;

        /// <summary>
        /// Checks if a number is a prime.
        /// </summary>
        /// <param name="number">The number to check</param>
        /// <returns>True if prime</returns>
        public static bool IsPrime(int number)
        {
            if (number < 2) return false;
            if (number == 2) return true;
            if (number % 2 == 0) return false;

            for (int i = 3; i * i <= number; i += 2)
            {
                if (number % i == 0) return false;
            }

            return true;
        }

        /// <summary>
        /// Checks if a number is a perfect square.
        /// </summary>
        /// <param name="number">The number to check</param>
        /// <returns>True if perfect square</returns>
        public static bool IsPerfectSquare(long number)
        {
            if (number < 0) return false;
            var root = (long)Math.Sqrt(number);
            return root * root == number;
        }

        /// <summary>
        /// Checks if a number is a perfect cube.
        /// </summary>
        /// <param name="number">The number to check</param>
        /// <returns>True if perfect cube</returns>
        public static bool IsPerfectCube(long number)
        {
            var root = (long)Math.Round(Math.Pow(Math.Abs(number), 1.0 / 3.0));
            return root * root * root == Math.Abs(number);
        }

        #endregion

        #region Parsing

        /// <summary>
        /// Parses a string to double with default value on failure.
        /// </summary>
        /// <param name="str">The string to parse</param>
        /// <param name="defaultValue">Default value if parsing fails</param>
        /// <returns>Parsed number or default</returns>
        public static double ParseOrDefault(string str, double defaultValue = 0)
        {
            return double.TryParse(str, NumberStyles.Any, CultureInfo.InvariantCulture, out var result)
                ? result
                : defaultValue;
        }

        /// <summary>
        /// Parses a string to int with default value on failure.
        /// </summary>
        /// <param name="str">The string to parse</param>
        /// <param name="defaultValue">Default value if parsing fails</param>
        /// <returns>Parsed number or default</returns>
        public static int ParseIntOrDefault(string str, int defaultValue = 0)
        {
            return int.TryParse(str, NumberStyles.Any, CultureInfo.InvariantCulture, out var result)
                ? result
                : defaultValue;
        }

        /// <summary>
        /// Parses a string to long with default value on failure.
        /// </summary>
        /// <param name="str">The string to parse</param>
        /// <param name="defaultValue">Default value if parsing fails</param>
        /// <returns>Parsed number or default</returns>
        public static long ParseLongOrDefault(string str, long defaultValue = 0)
        {
            return long.TryParse(str, NumberStyles.Any, CultureInfo.InvariantCulture, out var result)
                ? result
                : defaultValue;
        }

        /// <summary>
        /// Tries to parse a string to double.
        /// </summary>
        /// <param name="str">The string to parse</param>
        /// <param name="result">Parsed value if successful</param>
        /// <returns>True if parsing succeeded</returns>
        public static bool TryParse(string str, out double result)
        {
            return double.TryParse(str, NumberStyles.Any, CultureInfo.InvariantCulture, out result);
        }

        #endregion

        #region Utility Functions

        /// <summary>
        /// Calculates the greatest common divisor.
        /// </summary>
        /// <param name="a">First number</param>
        /// <param name="b">Second number</param>
        /// <returns>GCD</returns>
        public static long Gcd(long a, long b)
        {
            a = Math.Abs(a);
            b = Math.Abs(b);

            while (b != 0)
            {
                var temp = b;
                b = a % b;
                a = temp;
            }

            return a;
        }

        /// <summary>
        /// Calculates the least common multiple.
        /// </summary>
        /// <param name="a">First number</param>
        /// <param name="b">Second number</param>
        /// <returns>LCM</returns>
        public static long Lcm(long a, long b)
        {
            if (a == 0 || b == 0) return 0;
            return Math.Abs(a * b) / Gcd(a, b);
        }

        /// <summary>
        /// Calculates the factorial of a number.
        /// </summary>
        /// <param name="n">The number (0-20)</param>
        /// <returns>Factorial</returns>
        public static long Factorial(int n)
        {
            if (n < 0) throw new ArgumentException("Factorial is undefined for negative numbers");
            if (n > 20) throw new ArgumentOutOfRangeException(nameof(n), "Result would overflow long");

            long result = 1;
            for (int i = 2; i <= n; i++)
                result *= i;

            return result;
        }

        /// <summary>
        /// Calculates the nth Fibonacci number.
        /// </summary>
        /// <param name="n">The index (0-92)</param>
        /// <returns>Fibonacci number</returns>
        public static long Fibonacci(int n)
        {
            if (n < 0) throw new ArgumentException("Fibonacci is undefined for negative indices");
            if (n > 92) throw new ArgumentOutOfRangeException(nameof(n), "Result would overflow long");

            if (n <= 1) return n;

            long prev = 0, curr = 1;
            for (int i = 2; i <= n; i++)
            {
                var temp = curr;
                curr = prev + curr;
                prev = temp;
            }

            return curr;
        }

        /// <summary>
        /// Calculates the sum of digits.
        /// </summary>
        /// <param name="number">The number</param>
        /// <returns>Sum of digits</returns>
        public static int SumOfDigits(long number)
        {
            number = Math.Abs(number);
            var sum = 0;

            while (number > 0)
            {
                sum += (int)(number % 10);
                number /= 10;
            }

            return sum;
        }

        /// <summary>
        /// Reverses the digits of a number.
        /// </summary>
        /// <param name="number">The number</param>
        /// <returns>Number with reversed digits</returns>
        public static long ReverseDigits(long number)
        {
            var isNegative = number < 0;
            number = Math.Abs(number);

            long reversed = 0;
            while (number > 0)
            {
                reversed = reversed * 10 + number % 10;
                number /= 10;
            }

            return isNegative ? -reversed : reversed;
        }

        /// <summary>
        /// Checks if a number is a palindrome.
        /// </summary>
        /// <param name="number">The number to check</param>
        /// <returns>True if palindrome</returns>
        public static bool IsPalindrome(long number)
        {
            return number == ReverseDigits(number);
        }

        /// <summary>
        /// Converts degrees to radians.
        /// </summary>
        /// <param name="degrees">Angle in degrees</param>
        /// <returns>Angle in radians</returns>
        public static double DegreesToRadians(double degrees) => degrees * Math.PI / 180.0;

        /// <summary>
        /// Converts radians to degrees.
        /// </summary>
        /// <param name="radians">Angle in radians</param>
        /// <returns>Angle in degrees</returns>
        public static double RadiansToDegrees(double radians) => radians * 180.0 / Math.PI;

        /// <summary>
        /// Normalizes an angle to 0-360 degrees.
        /// </summary>
        /// <param name="degrees">Angle in degrees</param>
        /// <returns>Normalized angle</returns>
        public static double NormalizeAngle(double degrees)
        {
            degrees = degrees % 360;
            return degrees < 0 ? degrees + 360 : degrees;
        }

        #endregion

        #region Random Generation

        private static readonly Random RandomInstance = new Random();

        /// <summary>
        /// Generates a random double in range [min, max).
        /// </summary>
        /// <param name="min">Minimum value (inclusive)</param>
        /// <param name="max">Maximum value (exclusive)</param>
        /// <returns>Random double</returns>
        public static double Random(double min = 0, double max = 1)
        {
            if (min >= max) throw new ArgumentException("Min must be less than max");
            return min + RandomInstance.NextDouble() * (max - min);
        }

        /// <summary>
        /// Generates a random integer in range [min, max].
        /// </summary>
        /// <param name="min">Minimum value (inclusive)</param>
        /// <param name="max">Maximum value (inclusive)</param>
        /// <returns>Random integer</returns>
        public static int RandomInt(int min, int max)
        {
            if (min > max) throw new ArgumentException("Min must be less than or equal to max");
            return RandomInstance.Next(min, max + 1);
        }

        /// <summary>
        /// Generates a random number from normal distribution.
        /// </summary>
        /// <param name="mean">Mean value</param>
        /// <param name="stdDev">Standard deviation</param>
        /// <returns>Random number from normal distribution</returns>
        public static double RandomNormal(double mean = 0, double stdDev = 1)
        {
            // Box-Muller transform
            var u1 = 1.0 - RandomInstance.NextDouble();
            var u2 = 1.0 - RandomInstance.NextDouble();
            var randStdNormal = Math.Sqrt(-2.0 * Math.Log(u1)) * Math.Sin(2.0 * Math.PI * u2);
            return mean + stdDev * randStdNormal;
        }

        #endregion
    }
}
