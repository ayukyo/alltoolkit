using System;
using System.Text;
using AllToolkit;

namespace AllToolkit.Examples
{
    /// <summary>
    /// Example usage of Base64Utils class.
    /// </summary>
    class Base64UtilsExample
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Base64Utils Examples");
            Console.WriteLine("====================");
            Console.WriteLine();

            Example1_BasicEncoding();
            Example2_UrlSafeEncoding();
            Example3_BinaryData();
            Example4_Validation();
            Example5_ErrorHandling();
            Example6_LengthCalculations();

            Console.WriteLine();
            Console.WriteLine("All examples completed!");
        }

        static void Example1_BasicEncoding()
        {
            Console.WriteLine("Example 1: Basic Encoding and Decoding");
            Console.WriteLine("--------------------------------------");

            // Basic encoding
            string original = "Hello, World!";
            string encoded = Base64Utils.Encode(original);
            Console.WriteLine($"Original: {original}");
            Console.WriteLine($"Encoded:  {encoded}");

            // Basic decoding
            string decoded = Base64Utils.Decode(encoded);
            Console.WriteLine($"Decoded:  {decoded}");
            Console.WriteLine();

            // Encoding with different text
            string[] texts = { "A", "AB", "ABC", "ABCD" };
            foreach (string text in texts)
            {
                string enc = Base64Utils.Encode(text);
                Console.WriteLine($"'{text}' -> '{enc}'");
            }
            Console.WriteLine();
        }

        static void Example2_UrlSafeEncoding()
        {
            Console.WriteLine("Example 2: URL-Safe Encoding");
            Console.WriteLine("----------------------------");

            // URL-safe encoding is useful for URLs and filenames
            string original = "user+name/file@example.com";
            
            // Standard Base64 (may contain + and /)
            string standard = Base64Utils.Encode(original);
            Console.WriteLine($"Standard Base64: {standard}");

            // URL-safe Base64 (replaces + with - and / with _)
            string urlSafe = Base64Utils.EncodeUrlSafe(original, padding: true);
            Console.WriteLine($"URL-safe Base64: {urlSafe}");

            // URL-safe without padding (shorter, good for tokens)
            string urlSafeNoPad = Base64Utils.EncodeUrlSafe(original, padding: false);
            Console.WriteLine($"URL-safe (no pad): {urlSafeNoPad}");

            // Decoding URL-safe
            string decoded = Base64Utils.DecodeUrlSafe(urlSafe);
            Console.WriteLine($"Decoded: {decoded}");
            Console.WriteLine();
        }

        static void Example3_BinaryData()
        {
            Console.WriteLine("Example 3: Binary Data Encoding");
            Console.WriteLine("-------------------------------");

            // Encode binary data
            byte[] binaryData = new byte[] { 0x00, 0x01, 0x02, 0x03, 0xFF, 0xFE, 0xFD, 0xFC };
            string encoded = Base64Utils.Encode(binaryData);
            Console.WriteLine($"Binary data length: {binaryData.Length} bytes");
            Console.WriteLine($"Encoded: {encoded}");

            // Decode back to bytes
            byte[] decoded = Base64Utils.DecodeToBytes(encoded);
            Console.WriteLine($"Decoded length: {decoded.Length} bytes");
            Console.WriteLine($"Data matches: {BitConverter.ToString(binaryData) == BitConverter.ToString(decoded)}");
            Console.WriteLine();
        }

        static void Example4_Validation()
        {
            Console.WriteLine("Example 4: Validation");
            Console.WriteLine("---------------------");

            // Valid Base64 strings
            string[] validStrings = {
                "SGVsbG8sIFdvcmxkIQ==",
                "",
                "QQ==",
                "SGVsbG8rV29ybGQvVGVzdA"
            };

            Console.WriteLine("Valid strings:");
            foreach (string s in validStrings)
            {
                bool isValid = Base64Utils.IsValid(s);
                Console.WriteLine($"  '{s}' -> {isValid}");
            }

            // Invalid Base64 strings
            string[] invalidStrings = {
                "NotValid!!!",
                "Hello World",
                "===",
                null
            };

            Console.WriteLine("\nInvalid strings:");
            foreach (string s in invalidStrings)
            {
                bool isValid = Base64Utils.IsValid(s);
                Console.WriteLine($"  '{s}' -> {isValid}");
            }
            Console.WriteLine();
        }

        static void Example5_ErrorHandling()
        {
            Console.WriteLine("Example 5: Error Handling");
            Console.WriteLine("-------------------------");

            // Safe decoding with TryDecode
            string result = Base64Utils.TryDecode("SGVsbG8sIFdvcmxkIQ==");
            Console.WriteLine($"TryDecode valid: '{result}'");

            result = Base64Utils.TryDecode("NotValid!!!");
            Console.WriteLine($"TryDecode invalid: '{result ?? "null"}'");

            result = Base64Utils.TryDecode(null);
            Console.WriteLine($"TryDecode null: '{result ?? "null"}'");

            // Exception-based handling
            try
            {
                Base64Utils.Decode("Invalid!!!");
            }
            catch (FormatException e)
            {
                Console.WriteLine($"Caught FormatException: {e.Message}");
            }

            try
            {
                Base64Utils.Encode((string)null);
            }
            catch (ArgumentNullException e)
            {
                Console.WriteLine($"Caught ArgumentNullException: {e.Message}");
            }
            Console.WriteLine();
        }

        static void Example6_LengthCalculations()
        {
            Console.WriteLine("Example 6: Length Calculations");
            Console.WriteLine("------------------------------");

            // Calculate expected encoded length
            int[] inputLengths = { 1, 2, 3, 10, 100, 1000 };
            
            Console.WriteLine("Input Length -> Encoded Length (with padding):");
            foreach (int len in inputLengths)
            {
                int encodedLen = Base64Utils.GetEncodedLength(len, true);
                Console.WriteLine($"  {len,4} bytes -> {encodedLen,4} chars");
            }

            Console.WriteLine("\nInput Length -> Encoded Length (without padding):");
            foreach (int len in inputLengths)
            {
                int encodedLen = Base64Utils.GetEncodedLength(len, false);
                Console.WriteLine($"  {len,4} bytes -> {encodedLen,4} chars");
            }

            // Calculate max decoded length
            int[] encodedLengths = { 4, 8, 12, 100 };
            Console.WriteLine("\nEncoded Length -> Max Decoded Length:");
            foreach (int len in encodedLengths)
            {
                int maxDecoded = Base64Utils.GetDecodedMaxLength(len);
                Console.WriteLine($"  {len,4} chars -> {maxDecoded,4} bytes");
            }
            Console.WriteLine();
        }
    }
}
