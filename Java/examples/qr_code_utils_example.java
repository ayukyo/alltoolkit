package examples;

import qr_code_utils.mod;
import qr_code_utils.mod.QRCode;
import qr_code_utils.mod.ErrorCorrectionLevel;
import qr_code_utils.mod.Mode;

import java.awt.image.BufferedImage;

/**
 * QR Code Utilities Example
 * 
 * This example demonstrates various ways to generate and use QR codes
 * with the AllToolkit QR Code Utilities module.
 * 
 * @author AllToolkit Contributors
 * @version 1.0.0
 */
public class qr_code_utils_example {
    
    public static void main(String[] args) {
        System.out.println("========================================");
        System.out.println("QR Code Utilities Example");
        System.out.println("========================================\n");
        
        example1_BasicGeneration();
        example2_TextOutput();
        example3_AsciiOutput();
        example4_ImageOutput();
        example5_ErrorCorrectionLevels();
        example6_DifferentDataTypes();
        example7_CapacityPlanning();
        
        System.out.println("\n========================================");
        System.out.println("All examples completed successfully!");
        System.out.println("========================================");
    }
    
    /**
     * Example 1: Basic QR Code Generation
     * Demonstrates the simplest way to generate a QR code
     */
    private static void example1_BasicGeneration() {
        System.out.println("Example 1: Basic QR Code Generation");
        System.out.println("-----------------------------------");
        
        // Generate a QR code with default settings
        QRCode qr = mod.generate("Hello, World!");
        
        System.out.println("Data: " + qr.data);
        System.out.println("Version: " + qr.version);
        System.out.println("Size: " + qr.size + "x" + qr.size + " modules");
        System.out.println("Mode: " + qr.mode);
        System.out.println("Error Correction: " + qr.errorCorrectionLevel);
        System.out.println();
    }
    
    /**
     * Example 2: Text Output
     * Shows how to generate QR codes as text using Unicode block characters
     */
    private static void example2_TextOutput() {
        System.out.println("Example 2: Text Output (Unicode Block Characters)");
        System.out.println("-------------------------------------------------");
        
        // Generate QR code and display as text
        String textQr = mod.generateText("HELLO");
        System.out.println(textQr);
        System.out.println();
    }
    
    /**
     * Example 3: ASCII Output
     * Shows how to generate QR codes using simple ASCII characters
     */
    private static void example3_AsciiOutput() {
        System.out.println("Example 3: ASCII Output");
        System.out.println("-----------------------");
        
        // Generate QR code and display as ASCII art
        String asciiQr = mod.generateAscii("TEST");
        System.out.println(asciiQr);
        System.out.println();
    }
    
    /**
     * Example 4: Image Output
     * Demonstrates generating QR codes as BufferedImage objects
     */
    private static void example4_ImageOutput() {
        System.out.println("Example 4: Image Output");
        System.out.println("-----------------------");
        
        try {
            // Generate QR code as BufferedImage
            BufferedImage image = mod.generateImage("https://example.com");
            
            System.out.println("Generated image: " + image.getWidth() + "x" + image.getHeight() + " pixels");
            
            // Generate with custom module size
            QRCode qr = mod.generate("Custom Size");
            BufferedImage largeImage = qr.toImage(8, 4); // 8 pixels per module, 4 module quiet zone
            System.out.println("Large image: " + largeImage.getWidth() + "x" + largeImage.getHeight() + " pixels");
            
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
        System.out.println();
    }
    
    /**
     * Example 5: Error Correction Levels
     * Shows the different error correction levels available
     */
    private static void example5_ErrorCorrectionLevels() {
        System.out.println("Example 5: Error Correction Levels");
        System.out.println("----------------------------------");
        
        String data = "Important Data";
        
        // Generate with different error correction levels
        QRCode qrL = mod.generate(data, ErrorCorrectionLevel.L);
        QRCode qrM = mod.generate(data, ErrorCorrectionLevel.M);
        QRCode qrQ = mod.generate(data, ErrorCorrectionLevel.Q);
        QRCode qrH = mod.generate(data, ErrorCorrectionLevel.H);
        
        System.out.println("L (Low):    ~7% correction  - Version " + qrL.version + ", Size " + qrL.size + "x" + qrL.size);
        System.out.println("M (Medium): ~15% correction - Version " + qrM.version + ", Size " + qrM.size + "x" + qrM.size);
        System.out.println("Q (Quartile): ~25% correction - Version " + qrQ.version + ", Size " + qrQ.size + "x" + qrQ.size);
        System.out.println("H (High):   ~30% correction - Version " + qrH.version + ", Size " + qrH.size + "x" + qrH.size);
        System.out.println();
        
        System.out.println("Note: Higher error correction requires larger QR codes");
        System.out.println("but can withstand more damage while remaining readable.");
        System.out.println();
    }
    
    /**
     * Example 6: Different Data Types
     * Demonstrates automatic mode selection based on data type
     */
    private static void example6_DifferentDataTypes() {
        System.out.println("Example 6: Different Data Types");
        System.out.println("-------------------------------");
        
        // Numeric mode (most efficient for numbers)
        QRCode numeric = mod.generate("1234567890");
        System.out.println("Numeric '1234567890':");
        System.out.println("  Mode: " + numeric.mode + " (most efficient for numbers)");
        System.out.println("  Version: " + numeric.version);
        System.out.println();
        
        // Alphanumeric mode
        QRCode alphanumeric = mod.generate("HELLO WORLD 123");
        System.out.println("Alphanumeric 'HELLO WORLD 123':");
        System.out.println("  Mode: " + alphanumeric.mode);
        System.out.println("  Version: " + alphanumeric.version);
        System.out.println();
        
        // Byte mode (for mixed or lowercase content)
        QRCode byteMode = mod.generate("Hello, World!");
        System.out.println("Byte 'Hello, World!':");
        System.out.println("  Mode: " + byteMode.mode + " (handles any UTF-8 data)");
        System.out.println("  Version: " + byteMode.version);
        System.out.println();
    }
    
    /**
     * Example 7: Capacity Planning
     * Shows how to plan for data capacity
     */
    private static void example7_CapacityPlanning() {
        System.out.println("Example 7: Capacity Planning");
        System.out.println("----------------------------");
        
        // Get capacity for different versions
        System.out.println("Capacity for different QR versions (Byte mode, M error correction):");
        for (int version : new int[]{1, 5, 10, 20, 40}) {
            int capacity = mod.getCapacity(version, Mode.BYTE, ErrorCorrectionLevel.M);
            int size = mod.getQrSize(version);
            System.out.println("  Version " + version + " (" + size + "x" + size + "): ~" + capacity + " bytes");
        }
        System.out.println();
        
        // Check if data can be encoded
        String longData = "This is a longer piece of text that might need a larger QR code.";
        boolean canEncode = mod.canEncode(longData, ErrorCorrectionLevel.M);
        System.out.println("Can encode \"" + longData.substring(0, 20) + "...\": " + canEncode);
        
        // Get minimum version
        int minVersion = mod.getMinimumVersion(longData, ErrorCorrectionLevel.M);
        System.out.println("Minimum version required: " + minVersion);
        System.out.println();
    }
}
