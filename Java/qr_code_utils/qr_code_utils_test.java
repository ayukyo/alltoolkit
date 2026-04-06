package qr_code_utils;

import java.awt.image.BufferedImage;

import static qr_code_utils.mod.*;

/**
 * QR Code Utilities Test Suite
 * 
 * Comprehensive tests for QR code generation functionality.
 * Tests cover all encoding modes, error correction levels, and output formats.
 * 
 * @author AllToolkit Contributors
 * @version 1.0.0
 */
public class qr_code_utils_test {
    
    private static int testsPassed = 0;
    private static int testsFailed = 0;
    
    public static void main(String[] args) {
        System.out.println("========================================");
        System.out.println("QR Code Utilities Test Suite");
        System.out.println("========================================\n");
        
        // Basic generation tests
        testBasicGeneration();
        testNumericMode();
        testAlphanumericMode();
        testByteMode();
        testErrorCorrectionLevels();
        testTextOutput();
        testAsciiOutput();
        testImageOutput();
        testDifferentSizes();
        testCapacity();
        testEdgeCases();
        
        // Summary
        System.out.println("\n========================================");
        System.out.println("Test Summary:");
        System.out.println("  Passed: " + testsPassed);
        System.out.println("  Failed: " + testsFailed);
        System.out.println("  Total:  " + (testsPassed + testsFailed));
        System.out.println("========================================");
        
        if (testsFailed > 0) {
            System.exit(1);
        }
    }
    
    private static void testBasicGeneration() {
        System.out.println("Testing basic QR code generation...");
        
        try {
            // Test basic generation
            mod.QRCode qr = mod.generate("Hello, World!");
            assertNotNull("QR code should not be null", qr);
            assertTrue("QR code size should be positive", qr.size > 0);
            assertNotNull("QR code modules should not be null", qr.modules);
            assertEquals("QR code data should match input", "Hello, World!", qr.data);
            assertNotNull("QR code error correction level should not be null", qr.errorCorrectionLevel);
            assertNotNull("QR code mode should not be null", qr.mode);
            
            // Test that modules array has correct dimensions
            assertEquals("Modules array height should match size", qr.size, qr.modules.length);
            assertEquals("Modules array width should match size", qr.size, qr.modules[0].length);
            
            pass("Basic generation test");
        } catch (Exception e) {
            fail("Basic generation test", e.getMessage());
        }
    }
    
    private static void testNumericMode() {
        System.out.println("Testing numeric mode encoding...");
        
        try {
            // Test pure numeric data
            mod.QRCode qr = mod.generate("1234567890");
            assertEquals("Numeric data should use numeric mode", mod.Mode.NUMERIC, qr.mode);
            
            // Test longer numeric string
            qr = mod.generate("12345678901234567890");
            assertEquals("Long numeric data should use numeric mode", mod.Mode.NUMERIC, qr.mode);
            
            pass("Numeric mode test");
        } catch (Exception e) {
            fail("Numeric mode test", e.getMessage());
        }
    }
    
    private static void testAlphanumericMode() {
        System.out.println("Testing alphanumeric mode encoding...");
        
        try {
            // Test alphanumeric data
            mod.QRCode qr = mod.generate("HELLO WORLD");
            assertEquals("Alphanumeric data should use alphanumeric mode", mod.Mode.ALPHANUMERIC, qr.mode);
            
            // Test with special characters
            qr = mod.generate("ABC123 $%*+-./:");
            assertEquals("Alphanumeric with special chars should use alphanumeric mode", mod.Mode.ALPHANUMERIC, qr.mode);
            
            pass("Alphanumeric mode test");
        } catch (Exception e) {
            fail("Alphanumeric mode test", e.getMessage());
        }
    }
    
    private static void testByteMode() {
        System.out.println("Testing byte mode encoding...");
        
        try {
            // Test byte data (lowercase letters)
            mod.QRCode qr = mod.generate("hello world");
            assertEquals("Lowercase data should use byte mode", mod.Mode.BYTE, qr.mode);
            
            // Test with Unicode
            qr = mod.generate("Hello, World!");
            assertEquals("ASCII with punctuation should use byte mode", mod.Mode.BYTE, qr.mode);
            
            // Test with mixed content
            qr = mod.generate("Test123!@#");
            assertEquals("Mixed content should use byte mode", mod.Mode.BYTE, qr.mode);
            
            pass("Byte mode test");
        } catch (Exception e) {
            fail("Byte mode test", e.getMessage());
        }
    }
    
    private static void testErrorCorrectionLevels() {
        System.out.println("Testing error correction levels...");
        
        try {
            String data = "Hello, World!";
            
            // Test all error correction levels
            mod.QRCode qrL = mod.generate(data, mod.ErrorCorrectionLevel.L);
            assertEquals("Should use L error correction", mod.ErrorCorrectionLevel.L, qrL.errorCorrectionLevel);
            
            mod.QRCode qrM = mod.generate(data, mod.ErrorCorrectionLevel.M);
            assertEquals("Should use M error correction", mod.ErrorCorrectionLevel.M, qrM.errorCorrectionLevel);
            
            mod.QRCode qrQ = mod.generate(data, mod.ErrorCorrectionLevel.Q);
            assertEquals("Should use Q error correction", mod.ErrorCorrectionLevel.Q, qrQ.errorCorrectionLevel);
            
            mod.QRCode qrH = mod.generate(data, mod.ErrorCorrectionLevel.H);
            assertEquals("Should use H error correction", mod.ErrorCorrectionLevel.H, qrH.errorCorrectionLevel);
            
            pass("Error correction levels test");
        } catch (Exception e) {
            fail("Error correction levels test", e.getMessage());
        }
    }
    
    private static void testTextOutput() {
        System.out.println("Testing text output...");
        
        try {
            mod.QRCode qr = mod.generate("TEST");
            String text = qr.toText();
            
            assertNotNull("Text output should not be null", text);
            assertTrue("Text output should not be empty", text.length() > 0);
            assertTrue("Text output should contain block characters", text.contains("\u2588"));
            
            // Test generateText convenience method
            String directText = mod.generateText("TEST");
            assertNotNull("generateText should return non-null", directText);
            assertTrue("generateText should return non-empty", directText.length() > 0);
            
            pass("Text output test");
        } catch (Exception e) {
            fail("Text output test", e.getMessage());
        }
    }
    
    private static void testAsciiOutput() {
        System.out.println("Testing ASCII output...");
        
        try {
            mod.QRCode qr = mod.generate("TEST");
            String ascii = qr.toAscii();
            
            assertNotNull("ASCII output should not be null", ascii);
            assertTrue("ASCII output should not be empty", ascii.length() > 0);
            assertTrue("ASCII output should contain # characters", ascii.contains("#"));
            
            // Test generateAscii convenience method
            String directAscii = mod.generateAscii("TEST");
            assertNotNull("generateAscii should return non-null", directAscii);
            assertTrue("generateAscii should return non-empty", directAscii.length() > 0);
            
            pass("ASCII output test");
        } catch (Exception e) {
            fail("ASCII output test", e.getMessage());
        }
    }
    
    private static void testImageOutput() {
        System.out.println("Testing image output...");
        
        try {
            mod.QRCode qr = mod.generate("TEST");
            BufferedImage image = qr.toImage();
            
            assertNotNull("Image should not be null", image);
            assertTrue("Image width should be positive", image.getWidth() > 0);
            assertTrue("Image height should be positive", image.getHeight() > 0);
            assertEquals("Image should be square", image.getWidth(), image.getHeight());
            
            // Test with custom module size
            BufferedImage largeImage = qr.toImage(8, 4);
            assertTrue("Large image should be bigger", largeImage.getWidth() > image.getWidth());
            
            // Test generateImage convenience method
            BufferedImage directImage = mod.generateImage("TEST");
            assertNotNull("generateImage should return non-null", directImage);
            
            pass("Image output test");
        } catch (Exception e) {
            fail("Image output test", e.getMessage());
        }
    }
    
    private static void testDifferentSizes() {
        System.out.println("Testing different data sizes...");
        
        try {
            // Small data
            mod.QRCode qrSmall = mod.generate("A");
            assertTrue("Small data should generate valid QR", qrSmall.size > 0);
            
            // Medium data
            mod.QRCode qrMedium = mod.generate("Hello, World! This is a test.");
            assertTrue("Medium data should generate valid QR", qrMedium.size > 0);
            
            // Larger data
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < 100; i++) {
                sb.append("TEST");
            }
            mod.QRCode qrLarge = mod.generate(sb.toString());
            assertTrue("Large data should generate valid QR", qrLarge.size > 0);
            
            pass("Different sizes test");
        } catch (Exception e) {
            fail("Different sizes test", e.getMessage());
        }
    }
    
    private static void testCapacity() {
        System.out.println("Testing capacity functions...");
        
        try {
            // Test getQrSize
            int size1 = mod.getQrSize(1);
            assertEquals("Version 1 should be 21x21", 21, size1);
            
            int size2 = mod.getQrSize(2);
            assertEquals("Version 2 should be 25x25", 25, size2);
            
            int size40 = mod.getQrSize(40);
            assertEquals("Version 40 should be 177x177", 177, size40);
            
            // Test getCapacity
            int capacity = mod.getCapacity(1, mod.Mode.BYTE, mod.ErrorCorrectionLevel.M);
            assertTrue("Capacity should be positive", capacity > 0);
            
            // Test getMinimumVersion
            int minVersion = mod.getMinimumVersion("HELLO", mod.ErrorCorrectionLevel.M);
            assertTrue("Minimum version should be at least 1", minVersion >= 1);
            assertTrue("Minimum version should be at most 40", minVersion <= 40);
            
            pass("Capacity test");
        } catch (Exception e) {
            fail("Capacity test", e.getMessage());
        }
    }
    
    private static void testEdgeCases() {
        System.out.println("Testing edge cases...");
        
        try {
            // Test empty string (should throw exception)
            try {
                mod.generate("");
                fail("Empty string test", "Should throw exception for empty string");
            } catch (IllegalArgumentException e) {
                // Expected
            }
            
            // Test null (should throw exception)
            try {
                mod.generate(null);
                fail("Null test", "Should throw exception for null");
            } catch (IllegalArgumentException e) {
                // Expected
            }
            
            // Test canEncode
            assertTrue("canEncode should return true for valid data", 
                      mod.canEncode("TEST", mod.ErrorCorrectionLevel.M));
            
            // Test module access
            mod.QRCode qr = mod.generate("TEST");
            boolean module = qr.getModule(0, 0);
            // Just verify it doesn't throw
            
            // Test out of bounds access
            boolean outOfBounds = qr.getModule(-1, -1);
            assertFalse("Out of bounds should return false", outOfBounds);
            
            pass("Edge cases test");
        } catch (Exception e) {
            fail("Edge cases test", e.getMessage());
        }
    }
    
    // ==================== Assertion Helpers ====================
    
    private static void assertTrue(String message, boolean condition) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
    
    private static void assertFalse(String message, boolean condition) {
        if (condition) {
            throw new AssertionError(message);
        }
    }
    
    private static void assertEquals(String message, Object expected, Object actual) {
        if (expected == null ? actual != null : !expected.equals(actual)) {
            throw new AssertionError(message + " - Expected: " + expected + ", Actual: " + actual);
        }
    }
    
    private static void assertNotNull(String message, Object object) {
        if (object == null) {
            throw new AssertionError(message);
        }
    }
    
    private static void pass(String testName) {
        testsPassed++;
        System.out.println("  [PASS] " + testName);
    }
    
    private static void fail(String testName, String reason) {
        testsFailed++;
        System.out.println("  [FAIL] " + testName + ": " + reason);
    }
}
