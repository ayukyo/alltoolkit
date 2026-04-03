package uuid_utils;

public class uuid_utils_test {
    private static int testsPassed = 0;
    private static int testsFailed = 0;

    public static void main(String[] args) {
        System.out.println("=== UUID Utilities Test Suite ===\n");
        testV4Generation();
        testV4Compact();
        testV4Upper();
        testV3Generation();
        testV5Generation();
        testRandomString();
        testRandomAlphanumeric();
        testRandomNumeric();
        testRandomHex();
        testRandomPassword();
        testValidation();
        testV4Validation();
        testFormatConversion();
        testParsing();
        testVersionAndVariant();
        testShortId();
        testNanoId();
        testUlid();
        System.out.println("\n=== Test Summary ===");
        System.out.println("Passed: " + testsPassed);
        System.out.println("Failed: " + testsFailed);
        System.out.println("Total:  " + (testsPassed + testsFailed));
        if (testsFailed > 0) System.exit(1);
    }

    private static void testV4Generation() {
        System.out.println("Testing UUID v4 generation...");
        String uuid = mod.generateV4();
        assertTrue(uuid != null, "UUID should not be null");
        assertTrue(uuid.length() == 36, "UUID should be 36 characters");
        assertTrue(uuid.matches("^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"),
                "UUID should match v4 format");
        String uuid2 = mod.generateV4();
        assertTrue(!uuid.equals(uuid2), "Two UUIDs should be different");
        System.out.println("  ✓ UUID v4 generation tests passed");
    }

    private static void testV4Compact() {
        System.out.println("Testing UUID v4 compact format...");
        String uuid = mod.generateV4Compact();
        assertTrue(uuid != null, "Compact UUID should not be null");
        assertTrue(uuid.length() == 32, "Compact UUID should be 32 characters");
        assertTrue(!uuid.contains("-"), "Compact UUID should not contain dashes");
        assertTrue(uuid.matches("^[0-9a-f]{32}$"), "Compact UUID should be lowercase hex");
        System.out.println("  ✓ UUID v4 compact tests passed");
    }

    private static void testV4Upper() {
        System.out.println("Testing UUID v4 uppercase format...");
        String uuid = mod.generateV4Upper();
        assertTrue(uuid != null, "Upper UUID should not be null");
        assertTrue(uuid.length() == 36, "Upper UUID should be 36 characters");
        assertTrue(uuid.equals(uuid.toUpperCase()), "Upper UUID should be uppercase");
        System.out.println("  ✓ UUID v4 uppercase tests passed");
    }

    private static void testV3Generation() {
        System.out.println("Testing UUID v3 generation...");
        String uuid1 = mod.generateV3(mod.NAMESPACE_DNS, "example.com");
        String uuid2 = mod.generateV3(mod.NAMESPACE_DNS, "example.com");
        assertTrue(uuid1 != null, "v3 UUID should not be null");
        assertTrue(uuid1.equals(uuid2), "Same namespace+name should produce same v3 UUID");
        assertTrue(mod.getVersion(uuid1) == 3, "Should be version 3");
        String uuid3 = mod.generateV3(mod.NAMESPACE_DNS, "example.org");
        assertTrue(!uuid1.equals(uuid3), "Different names should produce different UUIDs");
        System.out.println("  ✓ UUID v3 generation tests passed");
    }

    private static void testV5Generation() {
        System.out.println("Testing UUID v5 generation...");
        String uuid1 = mod.generateV5(mod.NAMESPACE_URL, "https://example.com");
        String uuid2 = mod.generateV5(mod.NAMESPACE_URL, "https://example.com");
        assertTrue(uuid1 != null, "v5 UUID should not be null");
        assertTrue(uuid1.equals(uuid2), "Same namespace+name should produce same v5 UUID");
        assertTrue(mod.getVersion(uuid1) == 5, "Should be version 5");
        System.out.println("  ✓ UUID v5 generation tests passed");
    }

    private static void testRandomString() {
        System.out.println("Testing random string generation...");
        String str = mod.randomString(16, null);
        assertTrue(str != null, "Random string should not be null");
        assertTrue(str.length() == 16, "Random string should have correct length");
        String hex = mod.randomString(32, "0123456789ABCDEF");
        assertTrue(hex.matches("^[0-9A-F]+$"), "Should only contain hex characters");
        String str2 = mod.randomString(16, null);
        assertTrue(!str.equals(str2), "Two random strings should likely be different");
        try {
            mod.randomString(-1, null);
            assertTrue(false, "Should throw exception for negative length");
        } catch (IllegalArgumentException e) {
            assertTrue(true, "Should throw exception for negative length");
        }
        System.out.println("  ✓ Random string tests passed");
    }

    private static void testRandomAlphanumeric() {
        System.out.println("Testing random alphanumeric generation...");
        String str = mod.randomAlphanumeric(20);
        assertTrue(str != null, "Alphanumeric should not be null");
        assertTrue(str.length() == 20, "Should have correct length");
        assertTrue(str.matches("^[A-Za-z0-9]+$"), "Should be alphanumeric");
        System.out.println("  ✓ Random alphanumeric tests passed");
    }

    private static void testRandomNumeric() {
        System.out.println("Testing random numeric generation...");
        String str = mod.randomNumeric(10);
        assertTrue(str != null, "Numeric should not be null");
        assertTrue(str.length() == 10, "Should have correct length");
        assertTrue(str.matches("^[0-9]+$"), "Should be numeric only");
        System.out.println("  ✓ Random numeric tests passed");
    }

    private static void testRandomHex() {
        System.out.println("Testing random hex generation...");
        String str = mod.randomHex(32);
        assertTrue(str != null, "Hex should not be null");
        assertTrue(str.length() == 32, "Should have correct length");
        assertTrue(str.matches("^[0-9a-f]+$"), "Should be lowercase hex");
        System.out.println("  ✓ Random hex tests passed");
    }

    private static void testRandomPassword() {
        System.out.println("Testing random password generation...");
        String pwd = mod.randomPassword(16);
        assertTrue(pwd != null, "Password should not be null");
        assertTrue(pwd.length() == 16, "Should have correct length");
        boolean hasUpper = pwd.matches(".*[A-Z].*");
        boolean hasLower = pwd.matches(".*[a-z].*");
        boolean hasDigit = pwd.matches(".*[0-9].*");
        boolean hasSpecial = pwd.matches(".*[!@#$%^&*].*");
        assertTrue(hasUpper, "Password should have uppercase");
        assertTrue(hasLower, "Password should have lowercase");
        assertTrue(hasDigit, "Password should have digit");
        assertTrue(hasSpecial, "Password should have special char");
        System.out.println("  ✓ Random password tests passed");
    }

    private static void testValidation() {
        System.out.println("Testing UUID validation...");
        assertTrue(mod.isValidUUID("550e8400-e29b-41d4-a716-446655440000"), "Valid UUID should be valid");
        assertTrue(mod.isValidUUID("550e8400e29b41d4a716446655440000"), "Compact UUID should be valid");
        assertTrue(mod.isValidUUID("550E8400-E29B-41D4-A716-446655440000"), "Uppercase UUID should be valid");
        assertTrue(!mod.isValidUUID("invalid"), "Invalid string should not be valid");
        assertTrue(!mod.isValidUUID(""), "Empty string should not be valid");
        assertTrue(!mod.isValidUUID(null), "Null should not be valid");
        assertTrue(!mod.isValidUUID("550e8400-e29b-41d4-a716"), "Short UUID should not be valid");
        System.out.println("  ✓ UUID validation tests passed");
    }

    private static void testV4Validation() {
        System.out.println("Testing UUID v4 validation...");
        String v4 = mod.generateV4();
        assertTrue(mod.isValidV4(v4), "Generated v4 should be valid v4");
        String v5 = mod.generateV5(mod.NAMESPACE_DNS, "test");
        assertTrue(!mod.isValidV4(v5), "v5 UUID should not be valid v4");
        assertTrue(!mod.isValidV4("invalid"), "Invalid string should not be valid v4");
        System.out.println("  ✓ UUID v4 validation tests passed");
    }

    private static void testFormatConversion() {
        System.out.println("Testing format conversion...");
        String standard = "550e8400-e29b-41d4-a716-446655440000";
        String compact = "550e8400e29b41d4a716446655440000";
        assertTrue(mod.toCompact(standard).equals(compact), "toCompact should remove dashes");
        assertTrue(mod.toStandard(compact).equals(standard), "toStandard should add dashes");
        assertTrue(mod.toUpperCase(standard).equals("550E8400-E29B-41D4-A716-446655440000"), "toUpperCase should uppercase");
        assertTrue(mod.toCompact("invalid") == null, "Invalid UUID should return null");
        System.out.println("  ✓ Format conversion tests passed");
    }

    private static void testParsing() {
        System.out.println("Testing UUID parsing...");
        String uuidStr = mod.generateV4();
        java.util.UUID uuid = mod.parse(uuidStr);
        assertTrue(uuid != null, "Parsed UUID should not be null");
        assertTrue(uuid.toString().equals(uuidStr), "Parsed UUID should match original");
        assertTrue(mod.parse("invalid") == null, "Invalid UUID should return null");
        System.out.println("  ✓ UUID parsing tests passed");
    }

    private static void testVersionAndVariant() {
        System.out.println("Testing version and variant...");
        String v4 = mod.generateV4();
        assertTrue(mod.getVersion(v4) == 4, "v4 should have version 4");
        String v3 = mod.generateV3(mod.NAMESPACE_DNS, "test");
        assertTrue(mod.getVersion(v3) == 3, "v3 should have version 3");
        String v5 = mod.generateV5(mod.NAMESPACE_DNS, "test");
        assertTrue(mod.getVersion(v5) == 5, "v5 should have version 5");
        assertTrue(mod.getVariant(v4) == 1, "RFC4122 variant should be 1");
        assertTrue(mod.getVersion("invalid") == -1, "Invalid UUID should return -1");
        System.out.println("  ✓ Version and variant tests passed");
    }

    private static void testShortId() {
        System.out.println("Testing short ID generation...");
        String id = mod.shortId(8);
        assertTrue(id != null, "Short ID should not be null");
        assertTrue(id.length() > 0, "Short ID should not be empty");
        String id2 = mod.shortId(8);
        assertTrue(!id.equals(id2), "Two short IDs should be different");
        System.out.println("  ✓ Short ID tests passed");
    }

    private static void testNanoId() {
        System.out.println("Testing Nano ID generation...");
        String nano = mod.nanoId();
        assertTrue(nano != null, "Nano ID should not be null");
        assertTrue(nano.length() == 21, "Default Nano ID should be 21 characters");
        String nano10 = mod.nanoId(10);
        assertTrue(nano10.length() == 10, "Custom Nano ID should have correct length");
        System.out.println("  ✓ Nano ID tests passed");
    }

    private static void testUlid() {
        System.out.println("Testing ULID generation...");
        String ulid1 = mod.ulid();
        String ulid2 = mod.ulid();
        assertTrue(ulid1 != null, "ULID should not be null");
        assertTrue(ulid1.length() == 26, "ULID should be 26 characters");
        assertTrue(!ulid1.equals(ulid2), "Two ULIDs should be different");
        System.out.println("  ✓ ULID tests passed");
    }

    private static void assertTrue(boolean condition, String message) {
        if (condition) {
            testsPassed++;
        } else {
            testsFailed++;
            System.out.println("    ✗ FAILED: " + message);
        }
    }
}
