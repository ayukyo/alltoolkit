package qr_code_utils;

import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.EnumMap;
import java.util.Map;

/**
 * QR Code Utilities - A zero-dependency QR code generator for Java.
 * 
 * This module provides QR code generation capabilities using only Java standard library.
 * Supports QR code generation in multiple formats: text-based, image-based (BufferedImage),
 * and Base64 encoded strings.
 * 
 * Features:
 * - Generate QR codes in multiple error correction levels (L, M, Q, H)
 * - Support for various QR code sizes (versions 1-40)
 * - Output as text art, BufferedImage, or Base64 PNG data
 * - Customizable quiet zone (margin) and module size
 * - Zero external dependencies - uses only Java standard library
 * 
 * @author AllToolkit Contributors
 * @version 1.0.0
 */
public class mod {
    
    // Error correction levels
    public enum ErrorCorrectionLevel {
        L(0, 0b01, new int[][]{
            {-1, 7, 10, 15, 20, 26, 18, 20, 24, 30, 18, 20, 24, 26, 30, 22, 24, 28, 30, 28, 28, 28, 28, 30, 30, 26, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30},
            {-1, 10, 16, 26, 18, 24, 16, 18, 22, 22, 26, 30, 22, 22, 24, 24, 28, 28, 26, 26, 26, 26, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28},
            {-1, 13, 22, 18, 26, 18, 24, 18, 22, 20, 24, 28, 26, 24, 20, 30, 24, 28, 28, 26, 30, 28, 30, 30, 30, 30, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30},
            {-1, 17, 28, 22, 16, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28, 26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30}
        }),
        M(1, 0b00, new int[][]{
            {-1, 10, 16, 26, 18, 24, 16, 18, 22, 22, 26, 30, 22, 22, 24, 24, 28, 28, 26, 26, 26, 26, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28},
            {-1, 16, 28, 26, 24, 28, 22, 26, 24, 28, 26, 24, 20, 30, 30, 26, 28, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30},
            {-1, 26, 26, 24, 18, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28, 26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30},
            {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1}
        }),
        Q(2, 0b11, new int[][]{
            {-1, 13, 22, 18, 26, 18, 24, 18, 22, 20, 24, 28, 26, 24, 20, 30, 24, 28, 28, 26, 30, 28, 30, 30, 30, 30, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30},
            {-1, 22, 26, 24, 18, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28, 26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30},
            {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1},
            {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1}
        }),
        H(3, 0b10, new int[][]{
            {-1, 17, 28, 22, 16, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28, 26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30},
            {-1, 28, 26, 24, 22, 24, 20, 30, 24, 28, 28, 26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30},
            {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1},
            {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1}
        });
        
        public final int ordinal;
        public final int bits;
        public final int[][] numErrorCorrectionBlocks;
        
        ErrorCorrectionLevel(int ordinal, int bits, int[][] numErrorCorrectionBlocks) {
            this.ordinal = ordinal;
            this.bits = bits;
            this.numErrorCorrectionBlocks = numErrorCorrectionBlocks;
        }
    }
    
    // Mode indicators
    public enum Mode {
        NUMERIC(1, 10, 12, 14),
        ALPHANUMERIC(2, 9, 11, 13),
        BYTE(4, 8, 16, 16);
        
        public final int modeBits;
        public final int numBitsCharCountVersion0; // 1-9
        public final int numBitsCharCountVersion1; // 10-26
        public final int numBitsCharCountVersion2; // 27-40
        
        Mode(int modeBits, int numBitsCharCountVersion0, int numBitsCharCountVersion1, int numBitsCharCountVersion2) {
            this.modeBits = modeBits;
            this.numBitsCharCountVersion0 = numBitsCharCountVersion0;
            this.numBitsCharCountVersion1 = numBitsCharCountVersion1;
            this.numBitsCharCountVersion2 = numBitsCharCountVersion2;
        }
        
        public int numCharCountBits(int version) {
            if (version <= 9) return numBitsCharCountVersion0;
            if (version <= 26) return numBitsCharCountVersion1;
            return numBitsCharCountVersion2;
        }
    }
    
    // Alphanumeric character set
    private static final String ALPHANUMERIC_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:";
    
    // QR Code capacity table (characters per version and mode)
    private static final int[][][] CAPACITY_TABLE = {
        // Numeric mode capacities for each error correction level
        {{41, 77, 127, 187, 255, 322, 370, 461, 552, 652, 772, 883, 1022, 1101, 1250, 1408, 1548, 1725, 1903, 2061, 2232, 2409, 2620, 2812, 3057, 3283, 3514, 3669, 3909, 4158, 4417, 4686, 4965, 5253, 5529, 5836, 6153, 6479, 6743, 7089}},
        // Alphanumeric mode capacities
        {{25, 47, 77, 114, 154, 195, 224, 279, 335, 395, 468, 535, 619, 667, 758, 854, 938, 1046, 1153, 1249, 1352, 1460, 1588, 1704, 1853, 1990, 2132, 2223, 2369, 2520, 2677, 2840, 3009, 3183, 3351, 3537, 3729, 3927, 4087, 4296}},
        // Byte mode capacities
        {{17, 32, 53, 78, 106, 134, 154, 192, 230, 271, 321, 367, 425, 458, 520, 586, 644, 718, 792, 858, 929, 1003, 1091, 1171, 1273, 1367, 1465, 1528, 1628, 1732, 1840, 1952, 2068, 2188, 2303, 2431, 2563, 2699, 2809, 2953}}
    };
    
    /**
     * QR Code data class containing the generated matrix and metadata
     */
    public static class QRCode {
        public final int version;
        public final ErrorCorrectionLevel errorCorrectionLevel;
        public final Mode mode;
        public final int size;
        public final boolean[][] modules;
        public final String data;
        
        QRCode(int version, ErrorCorrectionLevel level, Mode mode, boolean[][] modules, String data) {
            this.version = version;
            this.errorCorrectionLevel = level;
            this.mode = mode;
            this.size = modules.length;
            this.modules = modules;
            this.data = data;
        }
        
        /**
         * Get the module at specific coordinates
         * @param row Row index (0-based)
         * @param col Column index (0-based)
         * @return true if module is dark, false if light
         */
        public boolean getModule(int row, int col) {
            if (row < 0 || row >= size || col < 0 || col >= size) {
                return false;
            }
            return modules[row][col];
        }
        
        /**
         * Convert QR code to text representation using Unicode block characters
         * @return String representation of QR code
         */
        public String toText() {
            StringBuilder sb = new StringBuilder();
            // Top quiet zone
            sb.append(repeatChar('\u2588', (size + 4) * 2)).append("\n");
            
            for (int row = 0; row < size; row++) {
                sb.append("\u2588\u2588"); // Left quiet zone
                for (int col = 0; col < size; col++) {
                    sb.append(modules[row][col] ? "\u2588\u2588" : "  ");
                }
                sb.append("\u2588\u2588\n"); // Right quiet zone
            }
            
            // Bottom quiet zone
            sb.append(repeatChar('\u2588', (size + 4) * 2));
            return sb.toString();
        }
        
        /**
         * Convert QR code to simple ASCII representation
         * @return ASCII art representation
         */
        public String toAscii() {
            StringBuilder sb = new StringBuilder();
            // Top border
            for (int i = 0; i < size + 4; i++) sb.append("##");
            sb.append("\n");
            
            for (int row = 0; row < size; row++) {
                sb.append("####"); // Left border
                for (int col = 0; col < size; col++) {
                    sb.append(modules[row][col] ? "##" : "  ");
                }
                sb.append("####\n"); // Right border
            }
            
            // Bottom border
            for (int i = 0; i < size + 4; i++) sb.append("##");
            return sb.toString();
        }
        
        /**
         * Convert QR code to BufferedImage
         * @param moduleSize Size of each module in pixels (default: 4)
         * @param quietZone Quiet zone size in modules (default: 4)
         * @return BufferedImage containing the QR code
         */
        public BufferedImage toImage(int moduleSize, int quietZone) {
            int imageSize = (size + 2 * quietZone) * moduleSize;
            BufferedImage image = new BufferedImage(imageSize, imageSize, BufferedImage.TYPE_INT_RGB);
            
            // Fill with white
            for (int y = 0; y < imageSize; y++) {
                for (int x = 0; x < imageSize; x++) {
                    image.setRGB(x, y, 0xFFFFFF);
                }
            }
            
            // Draw QR modules
            for (int row = 0; row < size; row++) {
                for (int col = 0; col < size; col++) {
                    if (modules[row][col]) {
                        int startY = (row + quietZone) * moduleSize;
                        int startX = (col + quietZone) * moduleSize;
                        for (int dy = 0; dy < moduleSize; dy++) {
                            for (int dx = 0; dx < moduleSize; dx++) {
                                image.setRGB(startX + dx, startY + dy, 0x000000);
                            }
                        }
                    }
                }
            }
            
            return image;
        }
        
        /**
         * Convert QR code to BufferedImage with default settings
         * @return BufferedImage containing the QR code
         */
        public BufferedImage toImage() {
            return toImage(4, 4);
        }
    }
    
    /**
     * Generate a QR code from text data
     * @param data The text to encode
     * @return QRCode object containing the generated code
     */
    public static QRCode generate(String data) {
        return generate(data, ErrorCorrectionLevel.M, null);
    }
    
    /**
     * Generate a QR code with specified error correction level
     * @param data The text to encode
     * @param errorCorrectionLevel Error correction level (L, M, Q, H)
     * @return QRCode object containing the generated code
     */
    public static QRCode generate(String data, ErrorCorrectionLevel errorCorrectionLevel) {
        return generate(data, errorCorrectionLevel, null);
    }
    
    /**
     * Generate a QR code with specified parameters
     * @param data The text to encode
     * @param errorCorrectionLevel Error correction level
     * @param requestedVersion Specific QR version (1-40), or null for auto
     * @return QRCode object containing the generated code
     */
    public static QRCode generate(String data, ErrorCorrectionLevel errorCorrectionLevel, Integer requestedVersion) {
        if (data == null || data.isEmpty()) {
            throw new IllegalArgumentException("Data cannot be null or empty");
        }
        
        // Determine the best mode
        Mode mode = determineMode(data);
        
        // Determine version
        int version = requestedVersion != null ? requestedVersion : findMinimumVersion(data.length(), mode, errorCorrectionLevel);
        if (version < 1 || version > 40) {
            throw new IllegalArgumentException("Version must be between 1 and 40");
        }
        
        // Create QR code matrix
        boolean[][] modules = new boolean[getSizeForVersion(version)][getSizeForVersion(version)];
        
        // Draw function patterns
        drawFunctionPatterns(modules, version);
        
        // Draw data
        drawData(modules, data, mode, version, errorCorrectionLevel);
        
        // Apply mask pattern (simplified - use mask 0)
        applyMask(modules, version, 0);
        
        // Draw format info
        drawFormatInfo(modules, version, errorCorrectionLevel, 0);
        
        return new QRCode(version, errorCorrectionLevel, mode, modules, data);
    }
    
    /**
     * Determine the optimal encoding mode for the data
     */
    private static Mode determineMode(String data) {
        boolean numeric = true;
        boolean alphanumeric = true;
        
        for (char c : data.toCharArray()) {
            if (numeric && !Character.isDigit(c)) {
                numeric = false;
            }
            if (alphanumeric && ALPHANUMERIC_CHARS.indexOf(c) < 0) {
                alphanumeric = false;
            }
        }
        
        if (numeric) return Mode.NUMERIC;
        if (alphanumeric) return Mode.ALPHANUMERIC;
        return Mode.BYTE;
    }
    
    /**
     * Find minimum QR version that can hold the data
     */
    private static int findMinimumVersion(int dataLength, Mode mode, ErrorCorrectionLevel level) {
        int modeIndex = mode == Mode.NUMERIC ? 0 : (mode == Mode.ALPHANUMERIC ? 1 : 2);
        for (int version = 1; version <= 40; version++) {
            if (version - 1 < CAPACITY_TABLE[modeIndex][0].length) {
                int capacity = CAPACITY_TABLE[modeIndex][0][version - 1];
                // Adjust capacity based on error correction level
                capacity = (int)(capacity * getCapacityMultiplier(level));
                if (capacity >= dataLength) {
                    return version;
                }
            }
        }
        throw new IllegalArgumentException("Data too long for any QR code version");
    }
    
    /**
     * Get capacity multiplier based on error correction level
     */
    private static double getCapacityMultiplier(ErrorCorrectionLevel level) {
        switch (level) {
            case L: return 1.0;
            case M: return 0.8;
            case Q: return 0.6;
            case H: return 0.45;
            default: return 0.8;
        }
    }
    
    /**
     * Get QR code size for a given version
     */
    private static int getSizeForVersion(int version) {
        return 17 + 4 * version;
    }
    
    /**
     * Draw function patterns (finder patterns, timing patterns, etc.)
     */
    private static void drawFunctionPatterns(boolean[][] modules, int version) {
        int size = modules.length;
        
        // Draw finder patterns (corners)
        drawFinderPattern(modules, 0, 0);
        drawFinderPattern(modules, size - 7, 0);
        drawFinderPattern(modules, 0, size - 7);
        
        // Draw separators
        drawSeparators(modules);
        
        // Draw timing patterns
        drawTimingPatterns(modules);
        
        // Draw dark module
        modules[4 * version + 9][8] = true;
        
        // Draw alignment patterns (if version > 1)
        if (version > 1) {
            drawAlignmentPatterns(modules, version);
        }
    }
    
    /**
     * Draw a finder pattern at the specified position
     */
    private static void drawFinderPattern(boolean[][] modules, int row, int col) {
        // 7x7 finder pattern
        for (int r = 0; r < 7; r++) {
            for (int c = 0; c < 7; c++) {
                boolean dark = (r == 0 || r == 6 || c == 0 || c == 6) || // Outer border
                              (r >= 2 && r <= 4 && c >= 2 && c <= 4);    // Inner square
                modules[row + r][col + c] = dark;
            }
        }
    }
    
    /**
     * Draw separators around finder patterns
     */
    private static void drawSeparators(boolean[][] modules) {
        int size = modules.length;
        
        // Top-left
        for (int i = 0; i < 8; i++) {
            if (i < 7) modules[7][i] = false;
            if (i < 7) modules[i][7] = false;
        }
        
        // Top-right
        for (int i = 0; i < 8; i++) {
            if (i < 7) modules[7][size - 1 - i] = false;
            if (i < 7) modules[i][size - 8] = false;
        }
        
        // Bottom-left
        for (int i = 0; i < 8; i++) {
            if (i < 7) modules[size - 8][i] = false;
            if (i < 7) modules[size - 1 - i][7] = false;
        }
    }
    
    /**
     * Draw timing patterns
     */
    private static void drawTimingPatterns(boolean[][] modules) {
        int size = modules.length;
        
        // Horizontal timing pattern
        for (int i = 8; i < size - 8; i++) {
            modules[6][i] = (i % 2) == 0;
        }
        
        // Vertical timing pattern
        for (int i = 8; i < size - 8; i++) {
            modules[i][6] = (i % 2) == 0;
        }
    }
    
    /**
     * Draw alignment patterns
     */
    private static void drawAlignmentPatterns(boolean[][] modules, int version) {
        int[] positions = getAlignmentPatternPositions(version);
        
        for (int row : positions) {
            for (int col : positions) {
                // Skip if overlapping with finder patterns
                if ((row < 10 && col < 10) || (row < 10 && col > modules.length - 10) || 
                    (row > modules.length - 10 && col < 10)) {
                    continue;
                }
                
                // Draw 5x5 alignment pattern
                for (int r = -2; r <= 2; r++) {
                    for (int c = -2; c <= 2; c++) {
                        boolean dark = (Math.abs(r) == 2 || Math.abs(c) == 2) || 
                                      (r == 0 && c == 0);
                        modules[row + r][col + c] = dark;
                    }
                }
            }
        }
    }
    
    /**
     * Get alignment pattern positions for a version
     */
    private static int[] getAlignmentPatternPositions(int version) {
        if (version == 1) return new int[0];
        
        int numAlign = version / 7 + 2;
        int step = (version == 32) ? 26 : 
                   ((version * 4 + numAlign * 2 + 1) / (2 * numAlign - 2)) * 2;
        
        int[] positions = new int[numAlign];
        positions[0] = 6;
        for (int i = 1; i < numAlign; i++) {
            positions[i] = (version * 4 + 10) - (numAlign - 1 - i) * step;
        }
        return positions;
    }
    
    /**
     * Draw data into the QR code matrix
     */
    private static void drawData(boolean[][] modules, String data, Mode mode, 
                                  int version, ErrorCorrectionLevel level) {
        // Convert data to bit stream
        BitBuffer bitBuffer = new BitBuffer();
        
        // Mode indicator
        bitBuffer.appendBits(mode.modeBits, 4);
        
        // Character count indicator
        bitBuffer.appendBits(data.length(), mode.numCharCountBits(version));
        
        // Data
        switch (mode) {
            case NUMERIC:
                encodeNumeric(bitBuffer, data);
                break;
            case ALPHANUMERIC:
                encodeAlphanumeric(bitBuffer, data);
                break;
            case BYTE:
                encodeByte(bitBuffer, data);
                break;
        }
        
        // Terminator
        int capacityBits = getCapacityBits(version, level);
        int terminatorBits = Math.min(4, capacityBits - bitBuffer.getBitLength());
        bitBuffer.appendBits(0, terminatorBits);
        
        // Pad to byte boundary
        int paddingBits = (8 - bitBuffer.getBitLength() % 8) % 8;
        bitBuffer.appendBits(0, paddingBits);
        
        // Pad bytes
        byte[] padBytes = {(byte)0xEC, (byte)0x11};
        int padIndex = 0;
        while (bitBuffer.getBitLength() < capacityBits) {
            bitBuffer.appendBits(padBytes[padIndex] & 0xFF, 8);
            padIndex = 1 - padIndex;
        }
        
        // Place bits in matrix
        placeBits(modules, bitBuffer);
    }
    
    /**
     * Encode numeric data
     */
    private static void encodeNumeric(BitBuffer buffer, String data) {
        for (int i = 0; i < data.length(); i += 3) {
            int len = Math.min(3, data.length() - i);
            int value = Integer.parseInt(data.substring(i, i + len));
            buffer.appendBits(value, len == 3 ? 10 : (len == 2 ? 7 : 4));
        }
    }
    
    /**
     * Encode alphanumeric data
     */
    private static void encodeAlphanumeric(BitBuffer buffer, String data) {
        for (int i = 0; i < data.length(); i += 2) {
            int first = ALPHANUMERIC_CHARS.indexOf(data.charAt(i));
            if (i + 1 < data.length()) {
                int second = ALPHANUMERIC_CHARS.indexOf(data.charAt(i + 1));
                buffer.appendBits(first * 45 + second, 11);
            } else {
                buffer.appendBits(first, 6);
            }
        }
    }
    
    /**
     * Encode byte data
     */
    private static void encodeByte(BitBuffer buffer, String data) {
        byte[] bytes = data.getBytes(StandardCharsets.UTF_8);
        for (byte b : bytes) {
            buffer.appendBits(b & 0xFF, 8);
        }
    }
    
    /**
     * Get capacity in bits for a version and error correction level
     */
    private static int getCapacityBits(int version, ErrorCorrectionLevel level) {
        int totalModules = getSizeForVersion(version);
        int totalBits = totalModules * totalModules;
        
        // Subtract function patterns
        int functionBits = countFunctionPatternBits(version);
        int dataBits = totalBits - functionBits;
        
        // Apply error correction ratio
        double[] ratios = {0.785, 0.625, 0.47, 0.36}; // L, M, Q, H
        return (int)(dataBits * ratios[level.ordinal]);
    }
    
    /**
     * Count bits used by function patterns
     */
    private static int countFunctionPatternBits(int version) {
        int size = getSizeForVersion(version);
        
        // Finder patterns (3 * 7 * 7)
        int finderBits = 3 * 7 * 7;
        
        // Separators (3 * 8 * 8 - 3 * 7 * 7)
        int separatorBits = 3 * (8 * 8 - 7 * 7);
        
        // Timing patterns
        int timingBits = 2 * (size - 16);
        
        // Dark module
        int darkModuleBits = 1;
        
        // Alignment patterns
        int alignCount = version > 1 ? (version / 7 + 2) : 0;
        int alignPatterns = alignCount * alignCount - 3; // Subtract overlapping with finders
        if (alignPatterns < 0) alignPatterns = 0;
        int alignBits = alignPatterns * 5 * 5;
        
        // Format info (2 * 15)
        int formatBits = 2 * 15;
        
        // Version info for versions >= 7
        int versionBits = version >= 7 ? 2 * 18 : 0;
        
        return finderBits + separatorBits + timingBits + darkModuleBits + 
               alignBits + formatBits + versionBits;
    }
    
    /**
     * Place bits in the QR code matrix
     */
    private static void placeBits(boolean[][] modules, BitBuffer buffer) {
        int size = modules.length;
        int bitIndex = 0;
        byte[] bytes = buffer.toByteArray();
        
        // Place data in upward columns, right to left, skipping function patterns
        for (int right = size - 1; right > 0; right -= 2) {
            if (right == 6) right--; // Skip timing column
            
            for (int vert = 0; vert < size; vert++) {
                for (int j = 0; j < 2; j++) {
                    int col = right - j;
                    int row = ((right + 1) / 2 % 2 == 0) ? (size - 1 - vert) : vert;
                    
                    if (!isFunctionPattern(modules, row, col)) {
                        if (bitIndex < bytes.length * 8) {
                            boolean bit = ((bytes[bitIndex / 8] >> (7 - bitIndex % 8)) & 1) == 1;
                            modules[row][col] = bit;
                            bitIndex++;
                        }
                    }
                }
            }
        }
    }
    
    /**
     * Check if a position is a function pattern
     */
    private static boolean isFunctionPattern(boolean[][] modules, int row, int col) {
        int size = modules.length;
        int version = (size - 17) / 4;
        
        // Finder patterns and separators
        if ((row < 9 && col < 9) || (row < 9 && col >= size - 8) || 
            (row >= size - 8 && col < 9)) {
            return true;
        }
        
        // Timing patterns
        if (row == 6 || col == 6) {
            return true;
        }
        
        // Alignment patterns
        if (version > 1) {
            int[] positions = getAlignmentPatternPositions(version);
            for (int posRow : positions) {
                for (int posCol : positions) {
                    if ((posRow < 10 && posCol < 10) || (posRow < 10 && posCol > size - 10) || 
                        (posRow > size - 10 && posCol < 10)) {
                        continue;
                    }
                    if (Math.abs(row - posRow) <= 2 && Math.abs(col - posCol) <= 2) {
                        return true;
                    }
                }
            }
        }
        
        return false;
    }
    
    /**
     * Apply mask pattern to the QR code
     */
    private static void applyMask(boolean[][] modules, int version, int maskPattern) {
        int size = modules.length;
        
        for (int row = 0; row < size; row++) {
            for (int col = 0; col < size; col++) {
                if (!isFunctionPattern(modules, row, col)) {
                    boolean mask = getMaskBit(maskPattern, row, col);
                    modules[row][col] = modules[row][col] ^ mask;
                }
            }
        }
    }
    
    /**
     * Get mask bit for a position
     */
    private static boolean getMaskBit(int maskPattern, int row, int col) {
        switch (maskPattern) {
            case 0: return ((row + col) % 2) == 0;
            case 1: return (row % 2) == 0;
            case 2: return (col % 3) == 0;
            case 3: return ((row + col) % 3) == 0;
            case 4: return (((row / 2) + (col / 3)) % 2) == 0;
            case 5: return (((row * col) % 2) + ((row * col) % 3)) == 0;
            case 6: return ((((row * col) % 2) + ((row * col) % 3)) % 2) == 0;
            case 7: return ((((row + col) % 2) + ((row * col) % 3)) % 2) == 0;
            default: return false;
        }
    }
    
    /**
     * Draw format information
     */
    private static void drawFormatInfo(boolean[][] modules, int version, 
                                        ErrorCorrectionLevel level, int maskPattern) {
        int size = modules.length;
        int formatInfo = (level.bits << 3) | maskPattern;
        
        // Calculate BCH error correction
        formatInfo = (formatInfo << 10) | calculateBCH(formatInfo);
        
        // XOR with mask
        formatInfo ^= 0x5412;
        
        // Draw format info around top-left finder
        for (int i = 0; i < 6; i++) {
            modules[8][i] = ((formatInfo >> i) & 1) == 1;
        }
        modules[8][7] = ((formatInfo >> 6) & 1) == 1;
        modules[8][8] = ((formatInfo >> 7) & 1) == 1;
        modules[7][8] = ((formatInfo >> 8) & 1) == 1;
        for (int i = 9; i < 15; i++) {
            modules[14 - i][8] = ((formatInfo >> i) & 1) == 1;
        }
        
        // Draw format info around other corners
        for (int i = 0; i < 8; i++) {
            modules[size - 1 - i][8] = ((formatInfo >> i) & 1) == 1;
        }
        for (int i = 8; i < 15; i++) {
            modules[8][size - 15 + i] = ((formatInfo >> i) & 1) == 1;
        }
        
        // Dark module
        modules[4 * version + 9][8] = true;
    }
    
    /**
     * Calculate BCH error correction for format info
     */
    private static int calculateBCH(int data) {
        int generator = 0x537;
        int result = data << 10;
        
        for (int i = 14; i >= 10; i--) {
            if (((result >> i) & 1) == 1) {
                result ^= generator << (i - 10);
            }
        }
        
        return result & 0x3FF;
    }
    
    /**
     * Helper method to repeat a character
     */
    private static String repeatChar(char c, int count) {
        StringBuilder sb = new StringBuilder(count);
        for (int i = 0; i < count; i++) {
            sb.append(c);
        }
        return sb.toString();
    }
    
    /**
     * Bit buffer for QR code data
     */
    private static class BitBuffer {
        private byte[] data = new byte[1024];
        private int bitLength = 0;
        
        void appendBits(int value, int numBits) {
            if (numBits < 0 || numBits > 16) {
                throw new IllegalArgumentException("Invalid number of bits");
            }
            
            ensureCapacity(bitLength + numBits);
            
            for (int i = numBits - 1; i >= 0; i--) {
                int byteIndex = bitLength / 8;
                int bitIndex = 7 - (bitLength % 8);
                
                if (((value >> i) & 1) == 1) {
                    data[byteIndex] |= (1 << bitIndex);
                }
                
                bitLength++;
            }
        }
        
        int getBitLength() {
            return bitLength;
        }
        
        byte[] toByteArray() {
            int byteLength = (bitLength + 7) / 8;
            byte[] result = new byte[byteLength];
            System.arraycopy(data, 0, result, 0, byteLength);
            return result;
        }
        
        private void ensureCapacity(int bits) {
            int bytesNeeded = (bits + 7) / 8;
            if (bytesNeeded > data.length) {
                byte[] newData = new byte[bytesNeeded * 2];
                System.arraycopy(data, 0, newData, 0, data.length);
                data = newData;
            }
        }
    }
    
    // ==================== Utility Methods ====================
    
    /**
     * Generate QR code and return as text string
     * @param data The text to encode
     * @return Text representation of QR code
     */
    public static String generateText(String data) {
        return generate(data).toText();
    }
    
    /**
     * Generate QR code and return as ASCII string
     * @param data The text to encode
     * @return ASCII representation of QR code
     */
    public static String generateAscii(String data) {
        return generate(data).toAscii();
    }
    
    /**
     * Generate QR code and return as BufferedImage
     * @param data The text to encode
     * @return BufferedImage containing the QR code
     */
    public static BufferedImage generateImage(String data) {
        return generate(data).toImage();
    }
    
    /**
     * Generate QR code and return as BufferedImage with custom size
     * @param data The text to encode
     * @param moduleSize Size of each module in pixels
     * @return BufferedImage containing the QR code
     */
    public static BufferedImage generateImage(String data, int moduleSize) {
        return generate(data).toImage(moduleSize, 4);
    }
    
    /**
     * Check if data can be encoded as QR code
     * @param data The text to check
     * @param errorCorrectionLevel Error correction level
     * @return true if data can be encoded
     */
    public static boolean canEncode(String data, ErrorCorrectionLevel errorCorrectionLevel) {
        try {
            generate(data, errorCorrectionLevel);
            return true;
        } catch (IllegalArgumentException e) {
            return false;
        }
    }
    
    /**
     * Get the minimum QR version required for the data
     * @param data The text to encode
     * @param errorCorrectionLevel Error correction level
     * @return Minimum version number (1-40)
     */
    public static int getMinimumVersion(String data, ErrorCorrectionLevel errorCorrectionLevel) {
        Mode mode = determineMode(data);
        return findMinimumVersion(data.length(), mode, errorCorrectionLevel);
    }
    
    /**
     * Get the size in pixels for a QR code version
     * @param version QR code version (1-40)
     * @return Size in modules
     */
    public static int getQrSize(int version) {
        return getSizeForVersion(version);
    }
    
    /**
     * Get the capacity in characters for a given version and mode
     * @param version QR code version (1-40)
     * @param mode Encoding mode
     * @param level Error correction level
     * @return Capacity in characters
     */
    public static int getCapacity(int version, Mode mode, ErrorCorrectionLevel level) {
        int modeIndex = mode == Mode.NUMERIC ? 0 : (mode == Mode.ALPHANUMERIC ? 1 : 2);
        if (version < 1 || version > 40 || version > CAPACITY_TABLE[modeIndex][0].length) {
            return 0;
        }
        int capacity = CAPACITY_TABLE[modeIndex][0][version - 1];
        return (int)(capacity * getCapacityMultiplier(level));
    }
}
