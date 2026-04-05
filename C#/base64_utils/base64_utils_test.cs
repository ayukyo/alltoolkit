using System;
using System.Text;
using AllToolkit;

namespace AllToolkit.Tests
{
    /// <summary>
    /// Unit tests for Base64Utils class.
    /// </summary>
    public static class Base64UtilsTest
    {
        private static int testsPassed = 0;
        private static int testsFailed = 0;

        public static void Main()
        {
            Console.WriteLine("Running Base64Utils Tests...");
            Console.WriteLine("===========================");

            TestBasicEncoding();
            TestBasicDecoding();
            TestUrlSafeEncoding();
            TestUrlSafeDecoding();
            TestByteArrayEncoding();
            TestTryDecode();
            TestValidation();
            TestLengthCalculations();
            TestEdgeCases();
            TestUnicodeSupport();

            Console.WriteLine();
            Console.WriteLine("===========================");
            Console.WriteLine($"Tests Passed: {testsPassed}");
            Console.WriteLine($"Tests Failed: {testsFailed}");
            Console.WriteLine($"Total Tests: {testsPassed + testsFailed}");

            if (testsFailed > 0)
                Environment.Exit(1);
        }

        private static void AssertEqual<T>(T expected, T actual, string testName)
        {
            if (expected.Equals(actual))
            {
                Console.WriteLine($"[PASS] {testName}");
                testsPassed++;
            }
            else
            {
                Console.WriteLine($"[FAIL] {testName}: Expected '{expected}', got '{actual}'");
                testsFailed++;
            }
        }

        private static void AssertTrue(bool condition, string testName)
        {
            if (condition)
            {
                Console.WriteLine($"[PASS] {testName}");
                testsPassed++;
            }
            else
            {
                Console.WriteLine($"[FAIL] {testName}");
                testsFailed++;
            }
        }

        private static void AssertFalse(bool condition, string testName)
        {
            AssertTrue(!condition, testName);
        }

        private static void TestBasicEncoding()
        {
            Console.WriteLine();
            Console.WriteLine("--- Basic Encoding Tests ---");

            string encoded = Base64Utils.Encode("Hello, World!");
            AssertEqual("SGVsbG8sIFdvcmxkIQ==", encoded, "Encode 'Hello, World!'");

            encoded = Base64Utils.Encode("");
            AssertEqual("", encoded, "Encode empty string");

            encoded = Base64Utils.Encode("A");
            AssertEqual("QQ==", encoded, "Encode single char 'A'");
        }

        private static void TestBasicDecoding()
        {
            Console.WriteLine();
            Console.WriteLine("--- Basic Decoding Tests ---");

            string decoded = Base64Utils.Decode("SGVsbG8sIFdvcmxkIQ==");
            AssertEqual("Hello, World!", decoded, "Decode 'SGVsbG8sIFdvcmxkIQ=='");

            decoded = Base64Utils.Decode("");
            AssertEqual("", decoded, "Decode empty string");

            decoded = Base64Utils.Decode("QQ==");
            AssertEqual("A", decoded, "Decode 'QQ=='");
        }

        private static void TestUrlSafeEncoding()
        {
            Console.WriteLine();
            Console.WriteLine("--- URL-Safe Encoding Tests ---");

            string encoded = Base64Utils.EncodeUrlSafe("Hello+World/Test", padding: true);
            AssertEqual("SGVsbG8rV29ybGQvVGVzdA==", encoded, "URL-safe encode with padding");

            encoded = Base64Utils.EncodeUrlSafe("Hello+World/Test", padding: false);
            AssertEqual("SGVsbG8rV29ybGQvVGVzdA", encoded, "URL-safe encode without padding");

            string original = ">>>???";
            encoded = Base64Utils.EncodeUrlSafe(original, padding: false);
            AssertFalse(encoded.Contains("+"), "URL-safe should not contain '+'");
            AssertFalse(encoded.Contains("/"), "URL-safe should not contain '/'");
        }

        private static void TestUrlSafeDecoding()
        {
            Console.WriteLine();
            Console.WriteLine("--- URL-Safe Decoding Tests ---");

            string decoded = Base64Utils.DecodeUrlSafe("SGVsbG8rV29ybGQvVGVzdA==");
            AssertEqual("Hello+World/Test", decoded, "URL-safe decode");

            decoded = Base64Utils.DecodeUrlSafe("SGVsbG8rV29ybGQvVGVzdA");
            AssertEqual("Hello+World/Test", decoded, "URL-safe decode without padding");
        }

        private static void TestByteArrayEncoding()
        {
            Console.WriteLine();
            Console.WriteLine("--- Byte Array Tests ---");

            byte[] data = new byte[] { 0x00, 0x01, 0x02, 0xFF };
            string encoded = Base64Utils.Encode(data);
            AssertEqual("AAEC/w==", encoded, "Encode byte array");

            byte[] decoded = Base64Utils.DecodeToBytes("AAEC/w==");
            AssertTrue(decoded.Length == 4 && decoded[0] == 0x00 && decoded[3] == 0xFF,
                "Decode to byte array");

            encoded = Base64Utils.EncodeUrlSafe(data, padding: false);
            AssertEqual("AAEC_w", encoded, "URL-safe encode byte array");
        }

        private static void TestTryDecode()
        {
            Console.WriteLine();
            Console.WriteLine("--- TryDecode Tests ---");

            string result = Base64Utils.TryDecode("SGVsbG8sIFdvcmxkIQ==");
            AssertEqual("Hello, World!", result, "TryDecode valid Base64");

            result = Base64Utils.TryDecode("NotValid!!!");
            AssertEqual(null, result, "TryDecode invalid Base64 returns null");

            result = Base64Utils.TryDecode(null);
            AssertEqual(null, result, "TryDecode null returns null");
        }

        private static void TestValidation()
        {
            Console.WriteLine();
            Console.WriteLine("--- Validation Tests ---");

            AssertTrue(Base64Utils.IsValid("SGVsbG8sIFdvcmxkIQ=="), "IsValid valid Base64");
            AssertTrue(Base64Utils.IsValid(""), "IsValid empty string");

            AssertFalse(Base64Utils.IsValid("NotValid!!!"), "IsValid invalid Base64");
            AssertFalse(Base64Utils.IsValid(null), "IsValid null");

            AssertTrue(Base64Utils.IsValidUrlSafe("SGVsbG8rV29ybGQvVGVzdA"), "IsValidUrlSafe valid");
            AssertFalse(Base64Utils.IsValidUrlSafe("NotValid"), "IsValidUrlSafe invalid");
        }

        private static void TestLengthCalculations()
        {
            Console.WriteLine();
            Console.WriteLine("--- Length Calculation Tests ---");

            int length = Base64Utils.GetEncodedLength(3, true);
            AssertEqual(4, length, "GetEncodedLength(3, true)");

            length = Base64Utils.GetEncodedLength(3, false);
            AssertEqual(4, length, "GetEncodedLength(3, false)");

            int maxDecoded = Base64Utils.GetDecodedMaxLength(4);
            AssertEqual(3, maxDecoded, "GetDecodedMaxLength(4)");
        }

        private static void TestEdgeCases()
        {
            Console.WriteLine();
            Console.WriteLine("--- Edge Case Tests ---");

            try
            {
                Base64Utils.Encode((string)null);
                AssertFalse(true, "Encode null should throw exception");
            }
            catch (ArgumentNullException)
            {
                AssertTrue(true, "Encode null throws ArgumentNullException");
            }

            try
            {
                Base64Utils.Decode((string)null);
                AssertFalse(true, "Decode null should throw exception");
            }
            catch (ArgumentNullException)
            {
                AssertTrue(true, "Decode null throws ArgumentNullException");
            }

            string roundTrip = Base64Utils.Decode(Base64Utils.Encode("Test123"));
            AssertEqual("Test123", roundTrip, "Round-trip encoding/decoding");
        }

        private static void TestUnicodeSupport()
        {
            Console.WriteLine();
            Console.WriteLine("--- Unicode Support Tests ---");

            string unicode = "Hello, 世界!";
            string encoded = Base64Utils.Encode(unicode);
            string decoded = Base64Utils.Decode(encoded);
            AssertEqual(unicode, decoded, "Unicode round-trip");

            string emoji = "Hello";
            encoded = Base64Utils.Encode(emoji);
            decoded = Base64Utils.Decode(encoded);
            AssertEqual(emoji, decoded, "Emoji round-trip");

            string chinese = "你好世界";
            encoded = Base64Utils.EncodeUrlSafe(chinese, padding: false);
            decoded = Base64Utils.DecodeUrlSafe(encoded);
            AssertEqual(chinese, decoded, "Chinese URL-safe round-trip");
        }
    }
}
