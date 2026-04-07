using System;
using AllToolkit;

namespace QRCodeUtilsTest
{
    /// <summary>
    /// Test suite for QRCodeUtils
    /// </summary>
    class Program
    {
        static int testsPassed = 0;
        static int testsFailed = 0;

        static void Main(string[] args)
        {
            Console.WriteLine("=== QR Code Utils Test Suite ===\n");

            TestBasicGeneration();
            TestTextGeneration();
            TestSvgGeneration();
            TestModeDetection();
            TestCapacityCalculation();
            TestErrorLevels();
            TestValidation();
            TestCapacityInfo();
            TestErrorLevelConversion();
            TestQRCodeSize();

            Console.WriteLine("\n=== Test Summary ===");
            Console.WriteLine($"Passed: {testsPassed}");
            Console.WriteLine($"Failed: {testsFailed}");
            Console.WriteLine($"Total: {testsPassed + testsFailed}");

            Environment.Exit(testsFailed > 0 ? 1 : 0);
        }

        static void TestBasicGeneration()
        {
            Console.WriteLine("Test: Basic Generation");
            try
            {
                var qr = QRCodeUtils.Generate("HELLO");
                Assert(qr != null, "QR Code should not be null");
                Assert(qr.Version >= 1 && qr.Version <= 10, "Version should be between 1 and 10");
                Assert(qr.Width == 17 + 4 * qr.Version, "Width should match version formula");
                Assert(qr.Matrix != null, "Matrix should not be null");
                Assert(qr.Matrix.GetLength(0) == qr.Width, "Matrix height should match width");
                Assert(qr.Matrix.GetLength(1) == qr.Width, "Matrix width should match width");
                Assert(qr.Data == "HELLO", "Data should match input");
                Console.WriteLine("  PASSED");
                testsPassed++;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  FAILED: {ex.Message}");
                testsFailed++;
            }
        }

        static void TestTextGeneration()
        {
            Console.WriteLine("Test: Text Generation");
            try
            {
                string text = QRCodeUtils.GenerateText("TEST", "##", "  ");
                Assert(!string.IsNullOrEmpty(text), "Text should not be empty");
                Assert(text.Contains("##"), "Text should contain dark modules");
                Assert(text.Contains("  "), "Text should contain light modules");
                Console.WriteLine("  PASSED");
                testsPassed++;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  FAILED: {ex.Message}");
                testsFailed++;
            }
        }

        static void TestSvgGeneration()
        {
            Console.WriteLine("Test: SVG Generation");
            try
            {
                string svg = QRCodeUtils.GenerateSvg("SVG TEST", 4);
                Assert(!string.IsNullOrEmpty(svg), "SVG should not be empty");
                Assert(svg.Contains("<?xml"), "SVG should contain XML declaration");
                Assert(svg.Contains("<svg"), "SVG should contain svg element");
                Assert(svg.Contains("</svg>"), "SVG should contain closing svg tag");
                Assert(svg.Contains("rect"), "SVG should contain rect elements");
                Console.WriteLine("  PASSED");
                testsPassed++;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  FAILED: {ex.Message}");
                testsFailed++;
            }
        }

        static void TestModeDetection()
        {
            Console.WriteLine("Test: Mode Detection");
            try
            {
                // Numeric mode
                var mode = QRCodeUtils.GetMode("12345");
                Assert(mode == QRMode.Numeric, "12345 should be Numeric mode");

                // Alphanumeric mode
                mode = QRCodeUtils.GetMode("HELLO");
                Assert(mode == QRMode.Alphanumeric, "HELLO should be Alphanumeric mode");

                // Byte mode
                mode = QRCodeUtils.GetMode("hello");
                Assert(mode == QRMode.Byte, "hello should be Byte mode");

                mode = QRCodeUtils.GetMode("Test123!");
                Assert(mode == QRMode.Byte, "Test123! should be Byte mode");

                Console.WriteLine("  PASSED");
                testsPassed++;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  FAILED: {ex.Message}");
                testsFailed++;
            }
        }

        static void TestCapacityCalculation()
        {
            Console.WriteLine("Test: Capacity Calculation");
            try
            {
                // Numeric capacity
                int capacity = QRCodeUtils.GetMaxCapacity(1, QRMode.Numeric, QRErrorCorrectionLevel.L);
                Assert(capacity > 0, "Numeric capacity should be positive");

                // Alphanumeric capacity
                capacity = QRCodeUtils.GetMaxCapacity(1, QRMode.Alphanumeric, QRErrorCorrectionLevel.L);
                Assert(capacity > 0, "Alphanumeric capacity should be positive");

                // Byte capacity
                capacity = QRCodeUtils.GetMaxCapacity(1, QRMode.Byte, QRErrorCorrectionLevel.L);
                Assert(capacity > 0, "Byte capacity should be positive");

                // Error level affects capacity
                int capL = QRCodeUtils.GetMaxCapacity(2, QRMode.Byte, QRErrorCorrectionLevel.L);
                int capH = QRCodeUtils.GetMaxCapacity(2, QRMode.Byte, QRErrorCorrectionLevel.H);
                Assert(capL > capH, "L level should have higher capacity than H level");

                Console.WriteLine("  PASSED");
                testsPassed++;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  FAILED: {ex.Message}");
                testsFailed++;
            }
        }

        static void TestErrorLevels()
        {
            Console.WriteLine("Test: Error Levels");
            try
            {
                var qrL = QRCodeUtils.Generate("TEST", QRErrorCorrectionLevel.L);
                Assert(qrL.ErrorCorrectionLevel == QRErrorCorrectionLevel.L, "Should use L level");

                var qrM = QRCodeUtils.Generate("TEST", QRErrorCorrectionLevel.M);
                Assert(qrM.ErrorCorrectionLevel == QRErrorCorrectionLevel.M, "Should use M level");

                var qrQ = QRCodeUtils.Generate("TEST", QRErrorCorrectionLevel.Q);
                Assert(qrQ.ErrorCorrectionLevel == QRErrorCorrectionLevel.Q, "Should use Q level");

                var qrH = QRCodeUtils.Generate("TEST", QRErrorCorrectionLevel.H);
                Assert(qrH.ErrorCorrectionLevel == QRErrorCorrectionLevel.H, "Should use H level");

                Console.WriteLine("  PASSED");
                testsPassed++;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  FAILED: {ex.Message}");
                testsFailed++;
            }
        }

        static void TestValidation()
        {
            Console.WriteLine("Test: Validation");
            try
            {
                // Valid data
                Assert(QRCodeUtils.ValidateData("TEST"), "TEST should be valid");
                Assert(QRCodeUtils.ValidateData("A"), "Single char should be valid");

                // Empty/null data should throw
                try
                {
                    QRCodeUtils.Generate("");
                    Assert(false, "Empty string should throw exception");
                }
                catch (ArgumentException)
                {
                    // Expected
                }

                try
                {
                    QRCodeUtils.Generate(null);
                    Assert(false, "Null should throw exception");
                }
                catch (ArgumentException)
                {
                    // Expected
                }

                Console.WriteLine("  PASSED");
                testsPassed++;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  FAILED: {ex.Message}");
                testsFailed++;
            }
        }

        static void TestCapacityInfo()
        {
            Console.WriteLine("Test: Capacity Info");
            try
            {
                var info = QRCodeUtils.GetCapacityInfo("HELLO WORLD");
                Assert(info != null, "Capacity info should not be null");
                Assert(info.DataLength == 11, "Data length should be 11");
                Assert(info.Mode == QRMode.Alphanumeric, "Mode should be Alphanumeric");
                Assert(info.Version >= 1, "Version should be at least 1");
                Assert(info.MaxCapacity > 0, "Max capacity should be positive");
                Assert(info.CanEncode, "Should be able to encode");

                // Test ToString
                string str = info.ToString();
                Assert(str.Contains("Mode:"), "ToString should contain Mode");
                Assert(str.Contains("Version:"), "ToString should contain Version");

                Console.WriteLine("  PASSED");
                testsPassed++;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  FAILED: {ex.Message}");
                testsFailed++;
            }
        }

        static void TestErrorLevelConversion()
        {
            Console.WriteLine("Test: Error Level Conversion");
            try
            {
                // To string
                Assert(QRCodeUtils.ErrorLevelToString(QRErrorCorrectionLevel.L) == "L", "L should convert to 'L'");
                Assert(QRCodeUtils.ErrorLevelToString(QRErrorCorrectionLevel.M) == "M", "M should convert to 'M'");
                Assert(QRCodeUtils.ErrorLevelToString(QRErrorCorrectionLevel.Q) == "Q", "Q should convert to 'Q'");
                Assert(QRCodeUtils.ErrorLevelToString(QRErrorCorrectionLevel.H) == "H", "H should convert to 'H'");

                // From string
                Assert(QRCodeUtils.StringToErrorLevel("L") == QRErrorCorrectionLevel.L, "'L' should parse to L");
                Assert(QRCodeUtils.StringToErrorLevel("M") == QRErrorCorrectionLevel.M, "'M' should parse to M");
                Assert(QRCodeUtils.StringToErrorLevel("Q") == QRErrorCorrectionLevel.Q, "'Q' should parse to Q");
                Assert(QRCodeUtils.StringToErrorLevel("H") == QRErrorCorrectionLevel.H, "'H' should parse to H");
                Assert(QRCodeUtils.StringToErrorLevel("invalid") == QRErrorCorrectionLevel.M, "Invalid should default to M");
                Assert(QRCodeUtils.StringToErrorLevel(null) == QRErrorCorrectionLevel.M, "Null should default to M");

                // Case insensitive
                Assert(QRCodeUtils.StringToErrorLevel("l") == QRErrorCorrectionLevel.L, "'l' should parse to L");
                Assert(QRCodeUtils.StringToErrorLevel("m") == QRErrorCorrectionLevel.M, "'m' should parse to M");

                Console.WriteLine("  PASSED");
                testsPassed++;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  FAILED: {ex.Message}");
                testsFailed++;
            }
        }

        static void TestQRCodeSize()
        {
            Console.WriteLine("Test: QR Code Size");
            try
            {
                Assert(QRCodeUtils.GetQRCodeSize(1) == 21, "Version 1 should be 21x21");
                Assert(QRCodeUtils.GetQRCodeSize(2) == 25, "Version 2 should be 25x25");
                Assert(QRCodeUtils.GetQRCodeSize(5) == 37, "Version 5 should be 37x37");
                Assert(QRCodeUtils.GetQRCodeSize(10) == 57, "Version 10 should be 57x57");

                try
                {
                    QRCodeUtils.GetQRCodeSize(0);
                    Assert(false, "Version 0 should throw");
                }
                catch (ArgumentException)
                {
                    // Expected
                }

                try
                {
                    QRCodeUtils.GetQRCodeSize(41);
                    Assert(false, "Version 41 should throw");
                }
                catch (ArgumentException)
                {
                    // Expected
                }

                Console.WriteLine("  PASSED");
                testsPassed++;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  FAILED: {ex.Message}");
                testsFailed++;
            }
        }

        static void Assert(bool condition, string message)
        {
            if (!condition)
            {
                throw new Exception($"Assertion failed: {message}");
            }
        }
    }
}
