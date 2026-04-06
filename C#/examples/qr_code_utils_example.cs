using System;
using AllToolkit;

namespace AllToolkit.Examples
{
    /// <summary>
    /// Example usage of QR Code utilities.
    /// </summary>
    public class QrCodeUtilsExample
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("=== QR Code Utilities Example ===\n");

            // Example 1: Basic QR code generation
            Console.WriteLine("1. Basic QR Code Generation");
            Console.WriteLine("---------------------------");
            var qr = QrCodeUtils.Generate("Hello, World!");
            Console.WriteLine($"Content: {qr.Content}");
            Console.WriteLine($"Size: {qr.Size}x{qr.Size} modules");
            Console.WriteLine($"Version: {qr.Version}");
            Console.WriteLine($"Error Correction: {qr.ErrorCorrection}\n");

            // Example 2: ASCII output
            Console.WriteLine("2. ASCII QR Code Output");
            Console.WriteLine("-----------------------");
            var ascii = QrCodeUtils.GenerateAscii("HELLO");
            Console.WriteLine(ascii);

            // Example 3: Compact ASCII output
            Console.WriteLine("3. Compact ASCII Output");
            Console.WriteLine("-----------------------");
            var compact = QrCodeUtils.GenerateAscii("HI", compact: true);
            Console.WriteLine(compact);

            // Example 4: SVG output
            Console.WriteLine("4. SVG QR Code");
            Console.WriteLine("--------------");
            var svg = QrCodeUtils.GenerateSvg("https://example.com", moduleSize: 4);
            Console.WriteLine("SVG generated (first 200 chars):");
            Console.WriteLine(svg.Substring(0, Math.Min(200, svg.Length)) + "...\n");

            // Example 5: Custom colors SVG
            Console.WriteLine("5. Custom Colored QR Code");
            Console.WriteLine("-------------------------");
            var coloredSvg = QrCodeUtils.GenerateSvg("COLOR", foreground: "#FF0000", background: "#FFFF00");
            Console.WriteLine("Colored SVG generated with red foreground and yellow background\n");

            // Example 6: Error correction levels
            Console.WriteLine("6. Error Correction Levels");
            Console.WriteLine("--------------------------");
            foreach (QrCodeUtils.ErrorCorrectionLevel level in Enum.GetValues(typeof(QrCodeUtils.ErrorCorrectionLevel)))
            {
                var qrLevel = QrCodeUtils.Generate("TEST", level);
                Console.WriteLine($"Level {level}: {qrLevel.Size}x{qrLevel.Size}");
            }
            Console.WriteLine();

            // Example 7: Encoding mode detection
            Console.WriteLine("7. Encoding Mode Detection");
            Console.WriteLine("--------------------------");
            string[] testStrings = { "12345", "HELLO WORLD", "Hello World!" };
            foreach (var s in testStrings)
            {
                var mode = QrCodeUtils.GetEncodingMode(s);
                string modeName = mode == 1 ? "Numeric" : mode == 2 ? "Alphanumeric" : "Byte";
                Console.WriteLine($"'{s}' -> {modeName} mode");
            }
            Console.WriteLine();

            // Example 8: Version calculation
            Console.WriteLine("8. QR Version Calculation");
            Console.WriteLine("-------------------------");
            string[] testContent = { "A", "Hello World", "This is a longer text" };
            foreach (var content in testContent)
            {
                var version = QrCodeUtils.GetMinimumVersion(content);
                Console.WriteLine($"'{content}' requires version {version}");
            }
            Console.WriteLine();

            // Example 9: Capacity information
            Console.WriteLine("9. QR Code Capacity");
            Console.WriteLine("-------------------");
            foreach (QrCodeUtils.QrVersion version in new[] { QrCodeUtils.QrVersion.V1, QrCodeUtils.QrVersion.V5, QrCodeUtils.QrVersion.V10 })
            {
                var capacity = QrCodeUtils.GetCapacity(version);
                Console.WriteLine($"Version {version}: ~{capacity} characters");
            }
            Console.WriteLine();

            // Example 10: Unicode output
            Console.WriteLine("10. Unicode Block Output");
            Console.WriteLine("------------------------");
            var unicode = QrCodeUtils.GenerateUnicode("TEST");
            Console.WriteLine(unicode);

            Console.WriteLine("=== End of Examples ===");
        }
    }
}
