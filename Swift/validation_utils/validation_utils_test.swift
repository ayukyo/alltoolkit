import Foundation

// Simple test framework
struct TestRunner {
    private var passed = 0
    private var failed = 0
    
    mutating func suite(_ name: String, _ tests: () -> Void) {
        print("\n=== \(name) ===")
        tests()
    }
    
    mutating func test(_ name: String, _ assertion: Bool) {
        if assertion {
            passed += 1
            print("  ✓ \(name)")
        } else {
            failed += 1
            print("  ✗ \(name)")
        }
    }
    
    func summary() {
        print("\n=== Test Summary ===")
        print("Passed: \(passed)")
        print("Failed: \(failed)")
        print("Total:  \(passed + failed)")
    }
}

var runner = TestRunner()

// String Validation Tests
runner.suite("String Validation") {
    runner.test("isBlank nil", ValidationUtils.isBlank(nil) == true)
    runner.test("isBlank empty", ValidationUtils.isBlank("") == true)
    runner.test("isBlank whitespace", ValidationUtils.isBlank("   ") == true)
    runner.test("isBlank content", ValidationUtils.isBlank("hello") == false)
    runner.test("isNotBlank empty", ValidationUtils.isNotBlank("") == false)
    runner.test("isNotBlank content", ValidationUtils.isNotBlank("hello") == true)
    runner.test("lengthBetween valid", ValidationUtils.lengthBetween("hello", min: 3, max: 10) == true)
    runner.test("lengthBetween too short", ValidationUtils.lengthBetween("hi", min: 3, max: 10) == false)
    runner.test("isAlpha letters", ValidationUtils.isAlpha("Hello") == true)
    runner.test("isAlpha with digits", ValidationUtils.isAlpha("Hello123") == false)
    runner.test("isNumeric digits", ValidationUtils.isNumeric("12345") == true)
    runner.test("isAlphanumeric mixed", ValidationUtils.isAlphanumeric("Hello123") == true)
}

// Email Validation Tests
runner.suite("Email Validation") {
    runner.test("valid email", ValidationUtils.isValidEmail("test@example.com") == true)
    runner.test("valid email with dots", ValidationUtils.isValidEmail("test.user@example.com") == true)
    runner.test("invalid email no at", ValidationUtils.isValidEmail("testexample.com") == false)
    runner.test("invalid email nil", ValidationUtils.isValidEmail(nil) == false)
}

// URL Validation Tests
runner.suite("URL Validation") {
    runner.test("valid HTTP", ValidationUtils.isValidURL("http://example.com") == true)
    runner.test("valid HTTPS", ValidationUtils.isValidURL("https://example.com") == true)
    runner.test("invalid no scheme", ValidationUtils.isValidURL("example.com", requireScheme: true) == false)
    runner.test("valid HTTPS only", ValidationUtils.isValidHTTPS("https://example.com") == true)
}

// Phone Validation Tests
runner.suite("Phone Validation") {
    runner.test("valid phone", ValidationUtils.isValidPhone("1234567890") == true)
    runner.test("valid US phone", ValidationUtils.isValidUSPhone("1234567890") == true)
    runner.test("valid China mobile", ValidationUtils.isValidChinaMobile("13800138000") == true)
    runner.test("invalid China prefix", ValidationUtils.isValidChinaMobile("12123456789") == false)
}

// IP Address Tests
runner.suite("IP Address Validation") {
    runner.test("valid IPv4", ValidationUtils.isValidIPv4("192.168.1.1") == true)
    runner.test("invalid IPv4 out of range", ValidationUtils.isValidIPv4("256.1.1.1") == false)
    runner.test("valid IPv6", ValidationUtils.isValidIPv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334") == true)
    runner.test("valid IP v4", ValidationUtils.isValidIP("192.168.1.1") == true)
}

// Credit Card Tests
runner.suite("Credit Card Validation") {
    runner.test("valid Visa", ValidationUtils.isValidCreditCard("4532015112830366") == true)
    runner.test("invalid checksum", ValidationUtils.isValidCreditCard("4532015112830367") == false)
    runner.test("invalid nil", ValidationUtils.isValidCreditCard(nil) == false)
}

// UUID Tests
runner.suite("UUID Validation") {
    runner.test("valid UUID v4", ValidationUtils.isValidUUID("550e8400-e29b-41d4-a716-446655440000") == true)
    runner.test("valid UUID simple", ValidationUtils.isValidUUIDSimple("550e8400e29b41d4a716446655440000") == true)
    runner.test("invalid UUID nil", ValidationUtils.isValidUUID(nil) == false)
}

// Hex Color Tests
runner.suite("Hex Color Validation") {
    runner.test("valid hex 6 char", ValidationUtils.isValidHexColor("#FF5733") == true)
    runner.test("valid hex 3 char", ValidationUtils.isValidHexColor("#F53") == true)
    runner.test("invalid hex no hash", ValidationUtils.isValidHexColor("FF5733") == false)
    runner.test("valid hex with alpha", ValidationUtils.isValidHexColorWithAlpha("#FF5733FF") == true)
}

// MAC Address Tests
runner.suite("MAC Address Validation") {
    runner.test("valid MAC colon", ValidationUtils.isValidMACAddress("00:1A:2B:3C:4D:5E") == true)
    runner.test("valid MAC hyphen", ValidationUtils.isValidMACAddress("00-1A-2B-3C-4D-5E") == true)
    runner.test("invalid MAC too short", ValidationUtils.isValidMACAddress("00:1A:2B:3C:4D") == false)
}

// Password Tests
runner.suite("Password Validation") {
    runner.test("strong password valid", ValidationUtils.isStrongPassword("StrongP@ss123") == true)
    runner.test("weak password too short", ValidationUtils.isStrongPassword("weak") == false)
    runner.test("weak password no uppercase", ValidationUtils.isStrongPassword("nouppercase123!") == false)
    runner.test("weak password no lowercase", ValidationUtils.isStrongPassword("NOLOWERCASE123!") == false)
    runner.test("weak password no digit", ValidationUtils.isStrongPassword("NoDigitPass!") == false)
    runner.test("weak password no special", ValidationUtils.isStrongPassword("NoSpecial123") == false)
}

// Date Validation Tests
runner.suite("Date Validation") {
    runner.test("valid date", ValidationUtils.isValidDate("2024-03-15") == true)
    runner.test("invalid date", ValidationUtils.isValidDate("2024-13-15") == false)
    runner.test("valid date format", ValidationUtils.isValidDate("15/03/2024", format: "dd/MM/yyyy") == true)
}

// Regex Validation Tests
runner.suite("Regex Validation") {
    runner.test("matches pattern", ValidationUtils.matches("hello123", pattern: "^[a-z]+[0-9]+$") == true)
    runner.test("contains pattern", ValidationUtils.contains("hello world", pattern: "world") == true)
}

// Numeric Validation Tests
runner.suite("Numeric Validation") {
    runner.test("between range", ValidationUtils.between(5, min: 1, max: 10) == true)
    runner.test("outside range", ValidationUtils.between(15, min: 1, max: 10) == false)
    runner.test("valid integer", ValidationUtils.isValidInteger("123") == true)
    runner.test("invalid integer", ValidationUtils.isValidInteger("abc") == false)
    runner.test("valid float", ValidationUtils.isValidFloat("3.14") == true)
    runner.test("is positive", ValidationUtils.isPositive("5") == true)
    runner.test("is negative", ValidationUtils.isNegative("-5") == true)
}

runner.summary()
