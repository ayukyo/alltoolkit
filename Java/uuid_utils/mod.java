package uuid_utils;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Random;
import java.util.UUID;

/**
 * UUID Utilities - Universal Unique Identifier generation and manipulation
 *
 * A comprehensive utility class for generating UUIDs (Universally Unique Identifiers)
 * and related random identifiers. Supports UUID v3, v4, v5, and custom formats.
 *
 * Features:
 * - UUID v4 (random) generation - most common
 * - UUID v3/v5 (name-based) generation using MD5/SHA1
 * - Custom random string generation
 * - UUID validation and parsing
 * - UUID format conversion (with/without dashes, uppercase/lowercase)
 * - GUID/UUID compatibility
 *
 * Zero dependencies - uses only Java standard library (java.util, java.security)
 *
 * @author AllToolkit Contributors
 * @version 1.0.0
 */
public class mod {

    /** Characters used for hexadecimal representation */
    private static final String HEX_CHARS = "0123456789abcdef";

    /** Characters used for Base32 encoding */
    private static final String BASE32_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

    /** Secure random number generator for cryptographic operations */
    private static final SecureRandom SECURE_RANDOM = new SecureRandom();

    /** Regular random for non-cryptographic operations */
    private static final Random RANDOM = new Random();

    // ==================== UUID v4 (Random) Generation ====================

    /**
     * Generate a standard UUID v4 (random UUID) with dashes
     *
     * Format: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
     * where y is 8, 9, a, or b
     *
     * @return String UUID in standard format (36 characters with dashes)
     * @example "550e8400-e29b-41d4-a716-446655440000"
     */
    public static String generateV4() {
        return UUID.randomUUID().toString();
    }

    /**
     * Generate a UUID v4 without dashes (compact format)
     *
     * @return String UUID without dashes (32 characters)
     * @example "550e8400e29b41d4a716446655440000"
     */
    public static String generateV4Compact() {
        return UUID.randomUUID().toString().replace("-", "");
    }

    /**
     * Generate a UUID v4 in uppercase format
     *
     * @return String UUID in uppercase with dashes
     * @example "550E8400-E29B-41D4-A716-446655440000"
     */
    public static String generateV4Upper() {
        return UUID.randomUUID().toString().toUpperCase();
    }

    // ==================== UUID v3/v5 (Name-based) Generation ====================

    /**
     * Generate a UUID v3 (name-based, MD5) from a namespace and name
     *
     * UUID v3 is deterministic - same namespace and name always produce same UUID
     *
     * @param namespace UUID namespace (use NAMESPACE_DNS, NAMESPACE_URL, etc.)
     * @param name      The name to hash
     * @return String UUID v3 in standard format
     */
    public static String generateV3(UUID namespace, String name) {
        return nameBasedUUID(namespace, name, "MD5", 0x30);
    }

    /**
     * Generate a UUID v5 (name-based, SHA1) from a namespace and name
     *
     * UUID v5 is deterministic and preferred over v3 (SHA1 is more secure than MD5)
     *
     * @param namespace UUID namespace (use NAMESPACE_DNS, NAMESPACE_URL, etc.)
     * @param name      The name to hash
     * @return String UUID v5 in standard format
     */
    public static String generateV5(UUID namespace, String name) {
        return nameBasedUUID(namespace, name, "SHA1", 0x50);
    }

    /**
     * Internal method for name-based UUID generation
     *
     * @param namespace The namespace UUID
     * @param name      The name string
     * @param algorithm Hash algorithm (MD5 or SHA1)
     * @param version   Version bits (0x30 for v3, 0x50 for v5)
     * @return String formatted UUID
     */
    private static String nameBasedUUID(UUID namespace, String name, String algorithm, int version) {
        try {
            MessageDigest md = MessageDigest.getInstance(algorithm);

            // Add namespace bytes
            byte[] nsBytes = toBytes(namespace);
            md.update(nsBytes);

            // Add name bytes
            md.update(name.getBytes(java.nio.charset.StandardCharsets.UTF_8));

            // Get hash
            byte[] hash = md.digest();

            // Set version bits
            hash[6] = (byte) ((hash[6] & 0x0F) | version);

            // Set variant bits (RFC 4122 variant)
            hash[8] = (byte) ((hash[8] & 0x3F) | 0x80);

            // Convert to UUID string
            return bytesToUUID(hash);

        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(algorithm + " algorithm not available", e);
        }
    }

    // ==================== Predefined Namespaces (RFC 4122) ====================

    /** DNS namespace UUID: 6ba7b810-9dad-11d1-80b4-00c04fd430c8 */
    public static final UUID NAMESPACE_DNS = UUID.fromString("6ba7b810-9dad-11d1-80b4-00c04fd430c8");

    /** URL namespace UUID: 6ba7b811-9dad-11d1-80b4-00c04fd430c8 */
    public static final UUID NAMESPACE_URL = UUID.fromString("6ba7b811-9dad-11d1-80b4-00c04fd430c8");

    /** OID namespace UUID: 6ba7b812-9dad-11d1-80b4-00c04fd430c8 */
    public static final UUID NAMESPACE_OID = UUID.fromString("6ba7b812-9dad-11d1-80b4-00c04fd430c8");

    /** X500 namespace UUID: 6ba7b814-9dad-11d1-80b4-00c04fd430c8 */
    public static final UUID NAMESPACE_X500 = UUID.fromString("6ba7b814-9dad-11d1-80b4-00c04fd430c8");

    // ==================== Custom Random String Generation ====================

    /**
     * Generate a cryptographically secure random string
     *
     * @param length Length of the string to generate
     * @param chars  Characters to use (if null/empty, uses alphanumeric)
     * @return String random string
     * @throws IllegalArgumentException if length is negative
     */
    public static String randomString(int length, String chars) {
        if (length < 0) {
            throw new IllegalArgumentException("Length must be non-negative");
        }
        if (chars == null || chars.isEmpty()) {
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        }

        StringBuilder sb = new StringBuilder(length);
        byte[] randomBytes = new byte[length];
        SECURE_RANDOM.nextBytes(randomBytes);

        for (int i = 0; i < length; i++) {
            int index = Math.abs(randomBytes[i]) % chars.length();
            sb.append(chars.charAt(index));
        }

        return sb.toString();
    }

    /**
     * Generate a random alphanumeric string (secure)
     *
     * @param length Length of the string
     * @return String random alphanumeric string
     */
    public static String randomAlphanumeric(int length) {
        return randomString(length, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789");
    }

    /**
     * Generate a random numeric string (secure)
     *
     * @param length Length of the string
     * @return String random numeric string
     */
    public static String randomNumeric(int length) {
        return randomString(length, "0123456789");
    }

    /**
     * Generate a random hexadecimal string (secure)
     *
     * @param length Length of the string
     * @return String random hex string
     */
    public static String randomHex(int length) {
        return randomString(length, HEX_CHARS);
    }

    /**
     * Generate a secure password with mixed character types
     *
     * @param length Minimum length (will use at least 4)
     * @return String secure password
     */
    public static String randomPassword(int length) {
        if (length < 4) length = 4;

        String upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        String lower = "abcdefghijklmnopqrstuvwxyz";
        String digits = "0123456789";
        String special = "!@#$%^&*";

        StringBuilder sb = new StringBuilder(length);

        // Ensure at least one of each type
        sb.append(randomString(1, upper));
        sb.append(randomString(1, lower));
        sb.append(randomString(1, digits));
        sb.append(randomString(1, special));

        // Fill remaining with mixed
        String all = upper + lower + digits + special;
        sb.append(randomString(length - 4, all));

        // Shuffle
        char[] chars = sb.toString().toCharArray();
        for (int i = chars.length - 1; i > 0; i--) {
            int j = RANDOM.nextInt(i + 1);
            char temp = chars[i];
            chars[i] = chars[j];
            chars[j] = temp;
        }

        return new String(chars);
    }

    // ==================== UUID Validation ====================

    /**
     * Check if a string is a valid UUID
     *
     * @param uuid String to validate
     * @return boolean true if valid UUID format
     */
    public static boolean isValidUUID(String uuid) {
        if (uuid == null || uuid.isEmpty()) {
            return false;
        }

        // Remove dashes for compact format check
        String compact = uuid.replace("-", "");

        // Check length
        if (compact.length() != 32) {
            return false;
        }

        // Check hex characters
        return compact.matches("^[0-9a-fA-F]+$");
    }

    /**
     * Check if a string is a valid UUID v4
     *
     * @param uuid String to validate
     * @return boolean true if valid UUID v4
     */
    public static boolean isValidV4(String uuid) {
        if (!isValidUUID(uuid)) {
            return false;
        }

        String normalized = uuid.replace("-", "").toLowerCase();

        // Check version (13th character should be '4')
        char version = normalized.charAt(12);
        if (version != '4') {
            return false;
        }

        // Check variant (17th character should be 8, 9, a, or b)
        char variant = normalized.charAt(16);
        return variant == '8' || variant == '9' || variant == 'a' || variant == 'b';
    }

    // ==================== UUID Format Conversion ====================

    /**
     * Convert UUID to compact format (no dashes)
     *
     * @param uuid UUID string
     * @return String compact UUID or null if invalid
     */
    public static String toCompact(String uuid) {
        if (!isValidUUID(uuid)) {
            return null;
        }
        return uuid.replace("-", "").toLowerCase();
    }

    /**
     * Convert UUID to standard format (with dashes)
     *
     * @param uuid UUID string (can be compact)
     * @return String standard UUID or null if invalid
     */
    public static String toStandard(String uuid) {
        if (!isValidUUID(uuid)) {
            return null;
        }

        String compact = uuid.replace("-", "").toLowerCase();
        return String.format("%s-%s-%s-%s-%s",
                compact.substring(0, 8),
                compact.substring(8, 12),
                compact.substring(12, 16),
                compact.substring(16, 20),
                compact.substring(20));
    }

    /**
     * Convert UUID to uppercase format
     *
     * @param uuid UUID string
     * @return String uppercase UUID or null if invalid
     */
    public static String toUpperCase(String uuid) {
        if (!isValidUUID(uuid)) {
            return null;
        }
        return toStandard(uuid).toUpperCase();
    }

    // ==================== UUID Parsing ====================

    /**
     * Parse a UUID string to java.util.UUID object
     *
     * @param uuid UUID string
     * @return UUID object or null if invalid
     */
    public static UUID parse(String uuid) {
        if (!isValidUUID(uuid)) {
            return null;
        }
        try {
            return UUID.fromString(toStandard(uuid));
        } catch (IllegalArgumentException e) {
            return null;
        }
    }

    /**
     * Get UUID version
     *
     * @param uuid UUID string
     * @return int version (3, 4, 5) or -1 if invalid
     */
    public static int getVersion(String uuid) {
        if (!isValidUUID(uuid)) {
            return -1;
        }
        String compact = uuid.replace("-", "").toLowerCase();
        char versionChar = compact.charAt(12);
        return Character.digit(versionChar, 16);
    }

    /**
     * Get UUID variant
     *
     * @param uuid UUID string
     * @return int variant (0=reserved, 1=RFC4122, 2=reserved, 3=reserved) or -1 if invalid
     */
    public static int getVariant(String uuid) {
        if (!isValidUUID(uuid)) {
            return -1;
        }
        String compact = uuid.replace("-", "").toLowerCase();
        int variantBits = Character.digit(compact.charAt(16), 16);
        if ((variantBits & 0x8) == 0) return 0;
        if ((variantBits & 0xC) == 0x8) return 1;
        if ((variantBits & 0xE) == 0xC) return 2;
        return 3;
    }

    // ==================== Utility Functions ====================

    /**
     * Generate a short unique ID (Base32 encoded, URL-safe)
     *
     * @param length Length in bytes (output will be longer due to encoding)
     * @return String short unique ID
     */
    public static String shortId(int length) {
        byte[] bytes = new byte[length];
        SECURE_RANDOM.nextBytes(bytes);
        return base32Encode(bytes);
    }

    /**
     * Generate a Nano ID (21 characters, URL-safe)
     *
     * Similar to nanoid npm package
     *
     * @return String 21-character Nano ID
     */
    public static String nanoId() {
        return randomString(21, "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz-");
    }

    /**
     * Generate a Nano ID with custom length
     *
     * @param length Desired length
     * @return String Nano ID of specified length
     */
    public static String nanoId(int length) {
        return randomString(length, "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz-");
    }

    /**
     * Generate a ULID (Universally Unique Lexicographically Sortable Identifier)
     *
     * 26 characters: 10 timestamp + 16 random
     *
     * @return String ULID
     */
    public static String ulid() {
        StringBuilder sb = new StringBuilder(26);

        // Timestamp part (10 chars, base32 encoded milliseconds)
        long timestamp = System.currentTimeMillis();
        sb.append(encodeBase32Timestamp(timestamp));

        // Randomness part (16 chars)
        sb.append(randomString(16, "0123456789ABCDEFGHJKMNPQRSTVWXYZ"));

        return sb.toString();
    }

    // ==================== Private Helper Methods ====================

    /**
     * Convert UUID to byte array
     *
     * @param uuid UUID object
     * @return byte[] 16-byte array
     */
    private static byte[] toBytes(UUID uuid) {
        byte[] bytes = new byte[16];
        long msb = uuid.getMostSignificantBits();
        long lsb = uuid.getLeastSignificantBits();

        for (int i = 0; i < 8; i++) {
            bytes[i] = (byte) (msb >>> (8 * (7 - i)));
            bytes[8 + i] = (byte) (lsb >>> (8 * (7 - i)));
        }

        return bytes;
    }

    /**
     * Convert byte array to UUID string
     *
     * @param bytes 16-byte array
     * @return String formatted UUID
     */
    private static String bytesToUUID(byte[] bytes) {
        StringBuilder sb = new StringBuilder(36);

        for (int i = 0; i < 16; i++) {
            if (i == 4 || i == 6 || i == 8 || i == 10) {
                sb.append('-');
            }
            sb.append(String.format("%02x", bytes[i]));
        }

        return sb.toString();
    }

    /**
     * Base32 encode byte array
     *
     * @param data Byte array to encode
     * @return String Base32 encoded string
     */
    private static String base32Encode(byte[] data) {
        StringBuilder sb = new StringBuilder();
        int buffer = 0;
        int bitsLeft = 0;

        for (byte b : data) {
            buffer = (buffer << 8) | (b & 0xFF);
            bitsLeft += 8;

            while (bitsLeft >= 5) {
                sb.append(BASE32_CHARS.charAt((buffer >>> (bitsLeft - 5)) & 0x1F));
                bitsLeft -= 5;
            }
        }

        if (bitsLeft > 0) {
            sb.append(BASE32_CHARS.charAt((buffer << (5 - bitsLeft)) & 0x1F));
        }

        return sb.toString();
    }

    /**
     * Encode timestamp to Base32 (Crockford's Base32)
     *
     * @param timestamp Milliseconds since epoch
     * @return String 10-character Base32 string
     */
    private static String encodeBase32Timestamp(long timestamp) {
        String chars = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";
        StringBuilder sb = new StringBuilder(10);

        for (int i = 9; i >= 0; i--) {
            sb.append(chars.charAt((int) (timestamp & 0x1F)));
            timestamp >>= 5;
        }

        return sb.reverse().toString();
    }
}
