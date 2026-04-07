using System;
using AllToolkit;

namespace QRCodeUtilsExample
{
    /// <summary>
    /// Example usage of QRCodeUtils
    /// </summary>
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== QR Code Utils Examples ===\n");

            Example1_BasicGeneration();
            Example2_TextOutput();
            Example3_SvgOutput();
            Example4_ErrorLevels();
            Example5_ModeDetection();
            Example6_CapacityInfo();
            Example7_CustomCharacters();
            Example8_Validation();
            Example9_VersionInfo();
            Example10_LongerText();
        }

        static void Example1_BasicGeneration()
        {
            Console.WriteLine("Example 1: Basic QR Code Generation");
            Console.WriteLine("-----------------------------------");

            var qr = QRCodeUtils.Generate("HELLO WORLD");
            Console.WriteLine($"Data: {qr.Data}");
            Console.WriteLine($"Version: {qr.Version}");
            Console.WriteLine($"Size: {qr.Width}x{qr.Width} modules");
            Console.WriteLine($"Mode: {qr.Mode}");
            Console.WriteLine($"Error Level: {QRCodeUtils.ErrorLevelToString(qr.ErrorCorrectionLevel)}");
            Console.WriteLine();
        }

        static void Example2_TextOutput()
        {
            Console.WriteLine("Example 2: Text Output");
            Console.WriteLine("----------------------");

            string text = QRCodeUtils.GenerateText("TEST", "██", "  ");
            Console.WriteLine("QR Code (TEST):");
            Console.WriteLine(text);
        }

        static void Example3_SvgOutput()
        {
            Console.WriteLine("Example 3: SVG Output");
            Console.WriteLine("---------------------");

            string svg = QRCodeUtils.GenerateSvg("https://example.com", 4);
            Console.WriteLine("SVG output (first 200 chars):");
            Console.WriteLine(svg.Substring(0, Math.Min(200, svg.Length)) + "...");
            Console.WriteLine();
        }

        static void Example4_ErrorLevels()
        {
            Console.WriteLine("Example 4: Different Error Correction Levels");
            Console.WriteLine("--------------------------------------------");

            string data = "SAME DATA";
            
            foreach (QRErrorCorrectionLevel level in Enum.GetValues(typeof(QRErrorCorrectionLevel)))
            {
                var qr = QRCodeUtils.Generate(data, level);
                Console.WriteLine($"Level {QRCodeUtils.ErrorLevelToString(level)}: Version {qr.Version}");
            }
            Console.WriteLine();
        }

        static void Example5_ModeDetection()
        {
            Console.WriteLine("Example 5: Mode Detection");
            Console.WriteLine("-------------------------");

            string[] testCases = new[] { "12345", "HELLO", "hello", "Test123!", "HELLO WORLD 123" };
            
            foreach (var test in testCases)
            {
                var mode = QRCodeUtils.GetMode(test);
                Console.WriteLine($"'{test}' -> {mode} mode");
            }
            Console.WriteLine();
        }

        static void Example6_CapacityInfo()
        {
            Console.WriteLine("Example 6: Capacity Information");
            Console.WriteLine("-------------------------------");

            string[] testData = new[] { "A", "HELLO", "HELLO WORLD THIS IS A TEST" };
            
            foreach (var data in testData)
            {
                var info = QRCodeUtils.GetCapacityInfo(data);
                Console.WriteLine($"Data: '{data}' ({info.DataLength} chars)");
                Console.WriteLine($"  {info}");
            }
            Console.WriteLine();
        }

        static void Example7_CustomCharacters()
        {
            Console.WriteLine("Example 7: Custom Characters");
            Console.WriteLine("----------------------------");

            // Using different characters for dark/light modules
            string text1 = QRCodeUtils.GenerateText("HI", "##", "  ");
            Console.WriteLine("Using '##' and '  ':");
            Console.WriteLine(text1);

            string text2 = QRCodeUtils.GenerateText("HI", "++", "--");
            Console.WriteLine("Using '++' and '--':");
            Console.WriteLine(text2);
        }

        static void Example8_Validation()
        {
            Console.WriteLine("Example 8: Data Validation");
            Console.WriteLine("--------------------------");

            string[] testCases = new[] { "VALID", "123", "", null };
            
            foreach (var test in testCases)
            {
                bool isValid = QRCodeUtils.ValidateData(test);
                Console.WriteLine($"ValidateData('{test}'): {isValid}");
            }
            Console.WriteLine();
        }

        static void Example9_VersionInfo()
        {
            Console.WriteLine("Example 9: Version Information");
            Console.WriteLine("------------------------------");

            for (int v = 1; v <= 5; v++)
            {
                int size = QRCodeUtils.GetQRCodeSize(v);
                int capNumeric = QRCodeUtils.GetMaxCapacity(v, QRMode.Numeric, QRErrorCorrectionLevel.M);
                int capAlpha = QRCodeUtils.GetMaxCapacity(v, QRMode.Alphanumeric, QRErrorCorrectionLevel.M);
                int capByte = QRCodeUtils.GetMaxCapacity(v, QRMode.Byte, QRErrorCorrectionLevel.M);
                
                Console.WriteLine($"Version {v} ({size}x{size}): Numeric={capNumeric}, Alpha={capAlpha}, Byte={capByte}");
            }
            Console.WriteLine();
        }

        static void Example10_LongerText()
        {
            Console.WriteLine("Example 10: Longer Text");
            Console.WriteLine("-----------------------");

            string url = "https://github.com/ayukyo/alltoolkit";
            var qr = QRCodeUtils.Generate(url, QRErrorCorrectionLevel.M);
            
            Console.WriteLine($"URL: {url}");
            Console.WriteLine($"Length: {url.Length} characters");
            Console.WriteLine($"QR Version: {qr.Version}");
            Console.WriteLine($"QR Size: {qr.Width}x{qr.Width}");
            Console.WriteLine($"Mode: {qr.Mode}");
            Console.WriteLine();

            // Show text representation (smaller)
            string text = QRCodeUtils.GenerateText(url, "█", " ");
            Console.WriteLine("Text representation:");
            Console.WriteLine(text);
        }
    }
}
