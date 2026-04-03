package examples;

import uuid_utils.mod;

/**
 * UUID Utilities Example
 *
 * Demonstrates usage of UUID generation and manipulation functions.
 *
 * Compile: javac -cp .. examples/uuid_utils_example.java
 * Run: java -cp .. examples.uuid_utils_example
 */
public class uuid_utils_example {

    public static void main(String[] args) {
        System.out.println("=== UUID Utilities Examples ===\n");

        exampleV4Generation();
        exampleV3V5Generation();
        exampleRandomStrings();
        examplePasswordGeneration();
        exampleValidation();
        exampleFormatConversion();
        exampleAlternativeIds();

        System.out.println("\n=== All examples completed ===");
    }

    private static void exampleV4Generation() {
        System.out.println("1. UUID v4 (Random) Generation");
        System.out.println("------------------------------");

        // Standard format with dashes
        String uuid1 = mod.generateV4();
        System.out.println("Standard v4:  " + uuid1);

        // Compact format without dashes
        String uuid2 = mod.generateV4Compact();
        System.out.println("Compact v4:   " + uuid2);

        // Uppercase format
        String uuid3 = mod.generateV4Upper();
        System.out.println("Uppercase v4: " + uuid3);

        System.out.println();
    }

    private static void exampleV3V5Generation() {
        System.out.println("2. UUID v3/v5 (Name-based) Generation");
        System.out.println("--------------------------------------");

        // v3 uses MD5 - deterministic
        String v3_1 = mod.generateV3(mod.NAMESPACE_DNS, "example.com");
        String v3_2 = mod.generateV3(mod.NAMESPACE_DNS, "example.com");
        System.out.println("v3 for 'example.com' (DNS): " + v3_1);
        System.out.println("v3 again (same):            " + v3_2);
        System.out.println("Same input = same UUID: " + v3_1.equals(v3_2));

        // v5 uses SHA1 - also deterministic, preferred over v3
        String v5_1 = mod.generateV5(mod.NAMESPACE_URL, "https://example.com");
        String v5_2 = mod.generateV5(mod.NAMESPACE_URL, "https://example.com");
        System.out.println("\nv5 for 'https://example.com' (URL): " + v5_1);
        System.out.println("v5 again (same):                    " + v5_2);

        // Different namespaces produce different UUIDs
        String v5_dns = mod.generateV5(mod.NAMESPACE_DNS, "example.com");
        String v5_url = mod.generateV5(mod.NAMESPACE_URL, "example.com");
        System.out.println("\nSame name, different namespaces:");
        System.out.println("  DNS namespace: " + v5_dns);
        System.out.println("  URL namespace: " + v5_url);

        System.out.println();
    }

    private static void exampleRandomStrings() {
        System.out.println("3. Random String Generation");
        System.out.println("----------------------------");

        // Alphanumeric
        String alpha = mod.randomAlphanumeric(16);
        System.out.println("Alphanumeric (16): " + alpha);

        // Numeric only
        String numeric = mod.randomNumeric(10);
        System.out.println("Numeric (10):      " + numeric);

        // Hexadecimal
        String hex = mod.randomHex(32);
        System.out.println("Hex (32):          " + hex);

        // Custom charset
        String custom = mod.randomString(20, "ABCDEF123456");
        System.out.println("Custom charset:    " + custom);

        System.out.println();
    }

    private static void examplePasswordGeneration() {
        System.out.println("4. Secure Password Generation");
        System.out.println("------------------------------");

        // Generate secure passwords
        String pwd1 = mod.randomPassword(12);
        String pwd2 = mod.randomPassword(16);
        String pwd3 = mod.randomPassword(20);

        System.out.println("Password (12 chars): " + pwd1);
        System.out.println("Password (16 chars): " + pwd2);
        System.out.println("Password (20 chars): " + pwd3);

        System.out.println("\nAll passwords contain:");
        System.out.println("  - Uppercase letters");
        System.out.println("  - Lowercase letters");
        System.out.println("  - Digits");
        System.out.println("  - Special characters");

        System.out.println();
    }

    private static void exampleValidation() {
        System.out.println("5. UUID Validation");
        System.out.println("-------------------");

        String validV4 = mod.generateV4();
        String validV5 = mod.generateV5(mod.NAMESPACE_DNS, "test");
        String invalid = "not-a-uuid";

        System.out.println("Valid v4 UUID: " + validV4);
        System.out.println("  isValidUUID: " + mod.isValidUUID(validV4));
        System.out.println("  isValidV4:   " + mod.isValidV4(validV4));
        System.out.println("  Version:     " + mod.getVersion(validV4));

        System.out.println("\nValid v5 UUID: " + validV5);
        System.out.println("  isValidUUID: " + mod.isValidUUID(validV5));
        System.out.println("  isValidV4:   " + mod.isValidV4(validV5));
        System.out.println("  Version:     " + mod.getVersion(validV5));

        System.out.println("\nInvalid: '" + invalid + "'");
        System.out.println("  isValidUUID: " + mod.isValidUUID(invalid));

        System.out.println();
    }

    private static void exampleFormatConversion() {
        System.out.println("6. Format Conversion");
        System.out.println("---------------------");

        String standard = mod.generateV4();
        System.out.println("Original (standard): " + standard);

        // To compact
        String compact = mod.toCompact(standard);
        System.out.println("To compact:          " + compact);

        // Back to standard
        String backToStandard = mod.toStandard(compact);
        System.out.println("Back to standard:    " + backToStandard);

        // To uppercase
        String upper = mod.toUpperCase(standard);
        System.out.println("To uppercase:        " + upper);

        // Parse to UUID object
        java.util.UUID uuid = mod.parse(standard);
        System.out.println("\nParsed to UUID object: " + uuid);

        System.out.println();
    }

    private static void exampleAlternativeIds() {
        System.out.println("7. Alternative ID Formats");
        System.out.println("--------------------------");

        // Short ID (Base32 encoded)
        String shortId = mod.shortId(8);
        System.out.println("Short ID (8 bytes):  " + shortId);

        // Nano ID (URL-safe, 21 chars)
        String nanoId = mod.nanoId();
        System.out.println("Nano ID (default):   " + nanoId);

        // Custom length Nano ID
        String nanoId10 = mod.nanoId(10);
        System.out.println("Nano ID (10 chars):  " + nanoId10);

        // ULID (sortable, 26 chars)
        String ulid1 = mod.ulid();
        String ulid2 = mod.ulid();
        System.out.println("ULID 1:              " + ulid1);
        System.out.println("ULID 2:              " + ulid2);

        System.out.println();
    }
}
