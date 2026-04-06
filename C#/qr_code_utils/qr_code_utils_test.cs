using System;
using AllToolkit;

namespace AllToolkit.Tests
{
    public class QrCodeUtilsTest
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("Running QR Code Utils Tests...\n");
            int passed = 0, failed = 0;

            try
            {
                var qr = QrCodeUtils.Generate("Hello World");
                Assert(qr != null, "QR code should be generated");
                Assert(qr.Content == "Hello World", "Content should match");
                passed++;
                Console.WriteLine("✓ Basic generation - PASSED");
            }
            catch (Exception ex)
            {
                failed++;
                Console.WriteLine($"✗ Basic generation - FAILED: {ex.Message}");
            }

            try
            {
                var qrL = QrCodeUtils.Generate("Test", QrCodeUtils.ErrorCorrectionLevel.L);
                var qrM = QrCodeUtils.Generate("Test", QrCodeUtils.ErrorCorrectionLevel.M);
                Assert(qrL.ErrorCorrection == QrCodeUtils.ErrorCorrectionLevel.L, "L level");
                Assert(qrM.ErrorCorrection == QrCodeUtils.ErrorCorrectionLevel.M, "M level");
                passed++;
                Console.WriteLine("✓ Error correction levels - PASSED");
            }
            catch (Exception ex)
            {
                failed++;
                Console.WriteLine($"✗ Error correction levels - FAILED: {ex.Message}");
            }

            try
            {
                Assert(QrCodeUtils.IsNumeric("12345"), "12345 numeric");
                Assert(!QrCodeUtils.IsNumeric("123a"), "123a not numeric");
                Assert(QrCodeUtils.IsAlphanumeric("HELLO"), "HELLO alphanumeric");
                passed++;
                Console.WriteLine("✓ Encoding mode detection - PASSED");
            }
            catch (Exception ex)
            {
                failed++;
                Console.WriteLine($"✗ Encoding mode detection - FAILED: {ex.Message}");
            }

            try
            {
                var ascii = QrCodeUtils.GenerateAscii("Test");
                Assert(!string.IsNullOrEmpty(ascii), "ASCII not empty");
                passed++;
                Console.WriteLine("✓ ASCII output - PASSED");
            }
            catch (Exception ex)
            {
                failed++;
                Console.WriteLine($"✗ ASCII output - FAILED: {ex.Message}");
            }

            try
            {
                var svg = QrCodeUtils.GenerateSvg("Test");
                Assert(svg.Contains("<svg"), "SVG tag");
                Assert(svg.Contains("</svg>"), "Closing SVG tag");
                passed++;
                Console.WriteLine("✓ SVG output - PASSED");
            }
            catch (Exception ex)
            {
                failed++;
                Console.WriteLine($"✗ SVG output - FAILED: {ex.Message}");
            }

            try
            {
                var version = QrCodeUtils.GetMinimumVersion("Hello");
                Assert(version != QrCodeUtils.QrVersion.Auto, "Version determined");
                passed++;
                Console.WriteLine("✓ Version calculation - PASSED");
            }
            catch (Exception ex)
            {
                failed++;
                Console.WriteLine($"✗ Version calculation - FAILED: {ex.Message}");
            }

            Console.WriteLine($"\nTotal: {passed} passed, {failed} failed");
            Environment.Exit(failed > 0 ? 1 : 0);
        }

        private static void Assert(bool condition, string message)
        {
            if (!condition)
                throw new Exception($"Assertion failed: {message}");
        }
    }
}
