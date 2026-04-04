using System;
using System.Linq;
using AllToolkit.StringUtils;

namespace AllToolkit.Tests
{
    /// <summary>
    /// StringUtils 单元测试
    /// </summary>
    class StringUtilsTest
    {
        private static int passed = 0;
        private static int failed = 0;

        static void Main(string[] args)
        {
            Console.WriteLine("Running StringUtils tests...\n");

            TestTrim();
            TestSplit();
            TestReplace();
            TestSearch();
            TestCaseConversion();
            TestValidation();
            TestSubstring();
            TestRepeatAndJoin();
            TestCleanup();
            TestTruncate();
            TestPadAndCenter();
            TestReverse();
            TestComparison();

            Console.WriteLine("\n========================================");
            Console.WriteLine($"Results: {passed} passed, {failed} failed");
            Console.WriteLine("========================================");

            Environment.Exit(failed > 0 ? 1 : 0);
        }

        static void Assert(bool condition, string testName)
        {
            if (condition)
            {
                Console.WriteLine($"  ✓ {testName}");
                passed++;
            }
            else
            {
                Console.WriteLine($"  ✗ {testName}");
                failed++;
            }
        }

        static void TestTrim()
        {
            Console.WriteLine("\nTrim Tests:");
            Assert(StringUtils.Trim("  hello  ") == "hello", "Trim whitespace");
            Assert(StringUtils.TrimLeft("  hello  ") == "hello  ", "TrimLeft");
            Assert(StringUtils.TrimRight("  hello  ") == "  hello", "TrimRight");
            Assert(StringUtils.TrimChars("...hello...", new[] { '.' }) == "hello", "TrimChars");
            Assert(StringUtils.Trim(null) == null, "Trim null");
            Assert(StringUtils.Trim("") == "", "Trim empty");
        }

        static void TestSplit()
        {
            Console.WriteLine("\nSplit Tests:");
            var parts = StringUtils.Split("a,b,c", ",");
            Assert(parts.Length == 3 && parts[0] == "a" && parts[1] == "b" && parts[2] == "c", "Split by string");
            
            parts = StringUtils.Split("a,b,c", ",", 2);
            Assert(parts.Length == 2, "Split with maxSplits");
            
            parts = StringUtils.SplitChar("a,b,c", ',');
            Assert(parts.Length == 3, "Split by char");
            
            Assert(StringUtils.Split("", ",").Length == 0, "Split empty string");
            Assert(StringUtils.Split(null, ",").Length == 0, "Split null");
        }

        static void TestReplace()
        {
            Console.WriteLine("\nReplace Tests:");
            Assert(StringUtils.Replace("hello world", "world", "C#") == "hello C#", "Replace all");
            Assert(StringUtils.ReplaceFirst("aaa", "a", "b") == "baa", "ReplaceFirst");
            Assert(StringUtils.ReplaceN("aaa", "a", "b", 2) == "bba", "ReplaceN");
            Assert(StringUtils.Replace("hello", "xyz", "abc") == "hello", "Replace not found");
        }

        static void TestSearch()
        {
            Console.WriteLine("\nSearch Tests:");
            Assert(StringUtils.Count("aaa", "a") == 3, "Count");
            Assert(StringUtils.Count("hello world", "l") == 3, "Count multiple");
            Assert(StringUtils.StartsWith("hello", "he"), "StartsWith");
            Assert(StringUtils.EndsWith("hello", "lo"), "EndsWith");
            Assert(StringUtils.Contains("hello", "ell"), "Contains");
            Assert(!StringUtils.StartsWith("hello", "xyz"), "StartsWith false");
        }

        static void TestCaseConversion()
        {
            Console.WriteLine("\nCase Conversion Tests:");
            Assert(StringUtils.ToUpper("hello") == "HELLO", "ToUpper");
            Assert(StringUtils.ToLower("HELLO") == "hello", "ToLower");
            Assert(StringUtils.ToTitleCase("hello world") == "Hello World", "ToTitleCase");
            Assert(StringUtils.ToSnakeCase("HelloWorld") == "hello_world", "ToSnakeCase");
            Assert(StringUtils.ToCamelCase("hello_world") == "helloWorld", "ToCamelCase");
            Assert(StringUtils.ToCamelCase("hello world") == "helloWorld", "ToCamelCase with space");
        }

        static void TestValidation()
        {
            Console.WriteLine("\nValidation Tests:");
            Assert(StringUtils.IsNullOrEmpty(null), "IsNullOrEmpty null");
            Assert(StringUtils.IsNullOrEmpty(""), "IsNullOrEmpty empty");
            Assert(!StringUtils.IsNullOrEmpty("hello"), "IsNullOrEmpty false");
            Assert(StringUtils.IsBlank("   "), "IsBlank whitespace");
            Assert(StringUtils.IsNotBlank("hello"), "IsNotBlank");
            Assert(StringUtils.IsNumeric("123.45"), "IsNumeric");
            Assert(StringUtils.IsInteger("-123"), "IsInteger");
            Assert(StringUtils.IsFloat("3.14"), "IsFloat");
            Assert(StringUtils.IsAlpha("hello"), "IsAlpha");
            Assert(StringUtils.IsAlphanumeric("hello123"), "IsAlphanumeric");
            Assert(StringUtils.IsEmail("test@example.com"), "IsEmail");
            Assert(!StringUtils.IsEmail("invalid"), "IsEmail false");
        }

        static void TestSubstring()
        {
            Console.WriteLine("\nSubstring Tests:");
            Assert(StringUtils.Left("hello", 3) == "hel", "Left");
            Assert(StringUtils.Right("hello", 3) == "llo", "Right");
            Assert(StringUtils.DropLeft("hello", 2) == "llo", "DropLeft");
            Assert(StringUtils.DropRight("hello", 2) == "hel", "DropRight");
            Assert(StringUtils.Substring("hello", 1, 3) == "ell", "Substring");
            Assert(StringUtils.Left("hi", 10) == "hi", "Left longer than string");
        }

        static void TestRepeatAndJoin()
        {
            Console.WriteLine("\nRepeat and Join Tests:");
            Assert(StringUtils.Repeat("ab", 3) == "ababab", "Repeat");
            Assert(StringUtils.Repeat("x", 0) == "", "Repeat zero");
            Assert(StringUtils.Join(",", "a", "b", "c") == "a,b,c", "Join params");
            Assert(StringUtils.Join("-", new[] { "a", "b" }) == "a-b", "Join array");
        }

        static void TestCleanup()
        {
            Console.WriteLine("\nCleanup Tests:");
            Assert(StringUtils.RemoveWhitespace("h e l l o") == "hello", "RemoveWhitespace");
            Assert(StringUtils.RemoveChars("hello123", new[] { '1', '2', '3' }) == "hello", "RemoveChars");
            Assert(StringUtils.NormalizeWhitespace("hello   world") == "hello world", "NormalizeWhitespace");
            Assert(StringUtils.NormalizeWhitespace("  hello  world  ") == "hello world", "NormalizeWhitespace trim");
        }

        static void TestTruncate()
        {
            Console.WriteLine("\nTruncate Tests:");
            Assert(StringUtils.Truncate("hello world", 5) == "hello", "Truncate");
            Assert(StringUtils.TruncateWithEllipsis("hello world", 8) == "hello...", "TruncateWithEllipsis");
            Assert(StringUtils.Truncate("hi", 10) == "hi", "Truncate shorter than max");
        }

        static void TestPadAndCenter()
        {
            Console.WriteLine("\nPad and Center Tests:");
            Assert(StringUtils.PadLeft("hi", 5) == "   hi", "PadLeft");
            Assert(StringUtils.PadRight("hi", 5) == "hi   ", "PadRight");
            Assert            Assert(StringUtils.Center("hi", 6) == "  hi  ", "Center even");
            Assert(StringUtils.Center("hi", 5) == " hi  ", "Center odd");
            Assert(StringUtils.PadLeft("hi", 5, '0') == "000hi", "PadLeft with char");
        }

        static void TestReverse()
        {
            Console.WriteLine("\nReverse Tests:");
            Assert(StringUtils.Reverse("hello") == "olleh", "Reverse");
            Assert(StringUtils.Reverse("") == "", "Reverse empty");
            Assert(StringUtils.Reverse("a") == "a", "Reverse single char");
        }

        static void TestComparison()
        {
            Console.WriteLine("\nComparison Tests:");
            Assert(StringUtils.EqualsIgnoreCase("Hello", "hello"), "EqualsIgnoreCase");
            Assert(!StringUtils.EqualsIgnoreCase("Hello", "world"), "EqualsIgnoreCase false");
            Assert(StringUtils.Compare("a", "b") < 0, "Compare");
            Assert(StringUtils.CompareIgnoreCase("A", "a") == 0, "CompareIgnoreCase");
        }
    }
}
