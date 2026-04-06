<?php
/**
 * ValidationUtils Test Suite
 * 
 * Comprehensive tests for the ValidationUtils class
 */

require_once __DIR__ . '/mod.php';

use AllToolkit\ValidationUtils;
use AllToolkit\ValidationResult;

// Test counter
$passed = 0;
$failed = 0;

function test(string $name, callable $assertion): void {
    global $passed, $failed;
    try {
        $result = $assertion();
        if ($result) {
            echo "✓ {$name}\n";
            $passed++;
        } else {
            echo "✗ {$name} (assertion failed)\n";
            $failed++;
        }
    } catch (Exception $e) {
        echo "✗ {$name} (exception: {$e->getMessage()})\n";
        $failed++;
    }
}

function testGroup(string $name): void {
    echo "\n=== {$name} ===\n";
}

echo "Running ValidationUtils Tests...\n";

// Basic Validation Tests
testGroup("Basic Validation");
test("isEmpty returns true for null", fn() => ValidationUtils::isEmpty(null) === true);
test("isEmpty returns true for empty string", fn() => ValidationUtils::isEmpty('') === true);
test("isEmpty returns true for whitespace string", fn() => ValidationUtils::isEmpty('   ') === true);
test("isEmpty returns true for empty array", fn() => ValidationUtils::isEmpty([]) === true);
test("isEmpty returns false for non-empty string", fn() => ValidationUtils::isEmpty('hello') === false);
test("isNotEmpty is inverse of isEmpty", fn() => ValidationUtils::isNotEmpty('hello') === true && ValidationUtils::isNotEmpty('') === false);
test("isBlank returns true for null", fn() => ValidationUtils::isBlank(null) === true);
test("isBlank returns true for empty string", fn() => ValidationUtils::isBlank('') === true);
test("isBlank returns true for whitespace only", fn() => ValidationUtils::isBlank("  \t\n  ") === true);
test("isBlank returns false for non-blank string", fn() => ValidationUtils::isBlank('hello') === false);

// Email Validation Tests
testGroup("Email Validation");
test("isEmail returns true for valid email", fn() => ValidationUtils::isEmail('test@example.com') === true);
test("isEmail returns true for email with dots", fn() => ValidationUtils::isEmail('user.name@example.co.uk') === true);
test("isEmail returns true for email with plus", fn() => ValidationUtils::isEmail('user+tag@example.com') === true);
test("isEmail returns false for invalid email", fn() => ValidationUtils::isEmail('invalid-email') === false);
test("isEmail returns false for email without @", fn() => ValidationUtils::isEmail('testexample.com') === false);
test("isEmail returns false for null", fn() => ValidationUtils::isEmail(null) === false);
test("isEmail returns false for empty string", fn() => ValidationUtils::isEmail('') === false);

// URL Validation Tests
testGroup("URL Validation");
test("isUrl returns true for valid HTTP URL", fn() => ValidationUtils::isUrl('https://example.com') === true);
test("isUrl returns true for URL with path", fn() => ValidationUtils::isUrl('https://example.com/path/to/page') === true);
test("isUrl returns false for invalid URL", fn() => ValidationUtils::isUrl('not-a-url') === false);
test("isUrl returns false for null", fn() => ValidationUtils::isUrl(null) === false);

// IP Address Tests
testGroup("IP Address Validation");
test("isIpv4 returns true for valid IPv4", fn() => ValidationUtils::isIpv4('192.168.1.1') === true);
test("isIpv4 returns true for localhost", fn() => ValidationUtils::isIpv4('127.0.0.1') === true);
test("isIpv4 returns false for invalid IPv4", fn() => ValidationUtils::isIpv4('256.1.1.1') === false);
test("isIpv6 returns true for valid IPv6", fn() => ValidationUtils::isIpv6('2001:db8::1') === true);
test("isIpv6 returns true for localhost IPv6", fn() => ValidationUtils::isIpv6('::1') === true);
test("isIp returns true for IPv4", fn() => ValidationUtils::isIp('192.168.1.1') === true);
test("isIp returns true for IPv6", fn() => ValidationUtils::isIp('::1') === true);

// UUID Tests
testGroup("UUID Validation");
test("isUuid returns true for valid UUID", fn() => ValidationUtils::isUuid('550e8400-e29b-41d4-a716-446655440000') === true);
test("isUuid returns false for invalid UUID", fn() => ValidationUtils::isUuid('not-a-uuid') === false);
test("isUuid returns false for UUID without dashes", fn() => ValidationUtils::isUuid('550e8400e29b41d4a716446655440000') === false);

// Color and MAC Tests
testGroup("Color and MAC Validation");
test("isHexColor returns true for 6-digit hex", fn() => ValidationUtils::isHexColor('#FF5733') === true);
test("isHexColor returns true for 3-digit hex", fn() => ValidationUtils::isHexColor('#F53') === true);
test("isHexColor returns false for invalid hex", fn() => ValidationUtils::isHexColor('#GGGGGG') === false);
test("isMacAddress returns true for valid MAC", fn() => ValidationUtils::isMacAddress('00:1A:2B:3C:4D:5E') === true);
test("isMacAddress returns true for MAC with dashes", fn() => ValidationUtils::isMacAddress('00-1A-2B-3C-4D-5E') === true);

// Character Type Tests
testGroup("Character Type Validation");
test("isAlpha returns true for alphabetic", fn() => ValidationUtils::isAlpha('HelloWorld') === true);
test("isAlpha returns false for alphanumeric", fn() => ValidationUtils::isAlpha('Hello123') === false);
test("isAlphanumeric returns true for alphanumeric", fn() => ValidationUtils::isAlphanumeric('Hello123') === true);
test("isNumeric returns true for digits only", fn() => ValidationUtils::isNumeric('123456') === true);
test("isInteger returns true for positive integer", fn() => ValidationUtils::isInteger('123') === true);
test("isInteger returns true for negative integer", fn() => ValidationUtils::isInteger('-123') === true);
test("isFloat returns true for float", fn() => ValidationUtils::isFloat('123.45') === true);

// Range Tests
testGroup("Range Validation");
test("between returns true for value in range", fn() => ValidationUtils::between(5, 1, 10) === true);
test("between returns false for value below range", fn() => ValidationUtils::between(0, 1, 10) === false);
test("between returns false for value above range", fn() => ValidationUtils::between(11, 1, 10) === false);
test("between handles null min/max", fn() => ValidationUtils::between(100, null, null) === true);
test("lengthBetween returns true for valid length", fn() => ValidationUtils::lengthBetween('hello', 3, 10) === true);
test("lengthBetween returns false for too short", fn() => ValidationUtils::lengthBetween('hi', 3, 10) === false);

// Number Tests
testGroup("Number Validation");
test("isPositive returns true for positive number", fn() => ValidationUtils::isPositive(5) === true);
test("isPositive returns false for negative number", fn() => ValidationUtils::isPositive(-5) === false);
test("isNegative returns true for negative number", fn() => ValidationUtils::isNegative(-5) === true);
test("isNegative returns false for positive number", fn() => ValidationUtils::isNegative(5) === false);
test("isZero returns true for zero", fn() => ValidationUtils::isZero(0) === true);
test("isZero returns false for non-zero", fn() => ValidationUtils::isZero(5) === false);

// Credit Card Tests
testGroup("Credit Card Validation");
test("isCreditCard returns true for valid Visa", fn() => ValidationUtils::isCreditCard('4532015112830366') === true);
test("isCreditCard returns true for valid Mastercard", fn() => ValidationUtils::isCreditCard('5555555555554444') === true);
test("isCreditCard returns false for invalid number", fn() => ValidationUtils::isCreditCard('1234567890123456') === false);
test("isCreditCard handles spaces and dashes", fn() => ValidationUtils::isCreditCard('4532 0151 1283 0366') === true);

// Password Tests
testGroup("Password Validation");
test("isStrongPassword returns true for strong password", fn() => ValidationUtils::isStrongPassword('MyP@ssw0rd!') === true);
test("isStrongPassword returns false for weak password", fn() => ValidationUtils::isStrongPassword('password') === false);
test("isStrongPassword returns false for too short", fn() => ValidationUtils::isStrongPassword('A1!') === false);

// Username Tests
testGroup("Username Validation");
test("isUsername returns true for valid username", fn() => ValidationUtils::isUsername('john_doe123') === true);
test("isUsername returns false for starting with number", fn() => ValidationUtils::isUsername('123user') === false);
test("isUsername returns false for too short", fn() => ValidationUtils::isUsername('ab') === false);

// JSON Tests
testGroup("JSON Validation");
test("isJson returns true for valid JSON", fn() => ValidationUtils::isJson('{"key":"value"}') === true);
test("isJson returns true for JSON array", fn() => ValidationUtils::isJson('[1,2,3]') === true);
test("isJson returns false for invalid JSON", fn() => ValidationUtils::isJson('not json') === false);

// Date Tests
testGroup("Date Validation");
test("isDate returns true for valid date", fn() => ValidationUtils::isDate('2024-03-15') === true);
test("isDate returns false for invalid date", fn() => ValidationUtils::isDate('2024-13-45') === false);
test("isDate returns false for wrong format", fn() => ValidationUtils::isDate('15/03/2024') === false);

// Array Tests
testGroup("Array Validation");
test("isIn returns true for value in array", fn() => ValidationUtils::isIn('apple', ['apple', 'banana', 'orange']) === true);
test("isIn returns false for value not in array", fn() => ValidationUtils::isIn('grape', ['apple', 'banana', 'orange']) === false);
test("hasRequiredKeys returns true when all keys present", fn() => ValidationUtils::hasRequiredKeys(['name' => 'John', 'email' => 'john@example.com'], ['name', 'email']) === true);
test("hasRequiredKeys returns false when key missing", fn() => ValidationUtils::hasRequiredKeys(['name' => 'John'], ['name', 'email']) === false);

// Validation Result Tests
testGroup("Validation Result");
test("ValidationResult isValid returns true", fn() => (new ValidationResult(true))->isValid() === true);
test("ValidationResult isValid returns false", fn() => (new ValidationResult(false, 'error'))->isValid() === false);
test("ValidationResult getMessage returns message", fn() => (new ValidationResult(false, 'error message'))->getMessage() === 'error message');

// Multiple Validation Tests
testGroup("Multiple Validation");
test("allValid returns true when all valid", function() {
    $results = [
        new ValidationResult(true),
        new ValidationResult(true),
        new ValidationResult(true)
    ];
    return ValidationUtils::allValid($results) === true;
});
test("allValid returns false when one invalid", function() {
    $results = [
        new ValidationResult(true),
        new ValidationResult(false, 'error'),
        new ValidationResult(true)
    ];
    return ValidationUtils::allValid($results) === false;
});
test("firstError returns null when all valid", function() {
    $results = [new ValidationResult(true), new ValidationResult(true)];
    return ValidationUtils::firstError($results) === null;
});
test("firstError returns first error message", function() {
    $results = [
        new ValidationResult(false, 'first error', 'field1'),
        new ValidationResult(false, 'second error', 'field2')
    ];
    return ValidationUtils::firstError($results) === 'first error';
});

// China Mobile Tests
testGroup("China Mobile Validation");
test("isChinaMobile returns true for valid mobile", fn() => ValidationUtils::isChinaMobile('13800138000') === true);
test("isChinaMobile returns false for invalid mobile", fn() => ValidationUtils::isChinaMobile('1380013800') === false);
test("isChinaMobile handles spaces and dashes", fn() => ValidationUtils::isChinaMobile('138-0013-8000') === true);

// China ID Card Tests
testGroup("China ID Card Validation");
test("isChinaIdCard returns true for valid ID", fn() => ValidationUtils::isChinaIdCard('110101199001011234') === true);
test("isChinaIdCard returns false for invalid length", fn() => ValidationUtils::isChinaIdCard('11010119900101123') === false);
test("isChinaIdCard returns false for invalid format", fn() => ValidationUtils::isChinaIdCard('11010119900101123X') === false);

// Summary
echo "\n" . str_repeat("=", 50) . "\n";
echo "Tests completed: " . ($passed + $failed) . "\n";
echo "Passed: {$passed}\n";
echo "Failed: {$failed}\n";

exit($failed > 0 ? 1 : 0);
