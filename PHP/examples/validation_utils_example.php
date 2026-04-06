<?php
/**
 * ValidationUtils Example
 * 
 * Demonstrates usage of the ValidationUtils class
 */

require_once __DIR__ . '/../validation_utils/mod.php';

use AllToolkit\ValidationUtils;
use AllToolkit\ValidationResult;

echo "=== PHP ValidationUtils Examples ===\n\n";

// Basic Validation
echo "1. Basic Validation\n";
echo "-------------------\n";

$email = 'user@example.com';
echo "Email '{$email}' is valid: " . (ValidationUtils::isEmail($email) ? 'Yes' : 'No') . "\n";

$empty = '';
echo "Is empty string blank: " . (ValidationUtils::isBlank($empty) ? 'Yes' : 'No') . "\n";

$value = 'Hello World';
echo "Is '{$value}' not empty: " . (ValidationUtils::isNotEmpty($value) ? 'Yes' : 'No') . "\n";

echo "\n";

// Email Validation
echo "2. Email Validation\n";
echo "-------------------\n";

$emails = [
    'test@example.com',
    'user.name@example.co.uk',
    'user+tag@example.com',
    'invalid-email',
    'test@',
    '@example.com'
];

foreach ($emails as $email) {
    $valid = ValidationUtils::isEmail($email) ? '✓ Valid' : '✗ Invalid';
    echo "  {$email}: {$valid}\n";
}

echo "\n";

// URL Validation
echo "3. URL Validation\n";
echo "-----------------\n";

$urls = [
    'https://example.com',
    'https://example.com/path/to/page',
    'https://example.com?foo=bar&baz=qux',
    'not-a-url',
    'ftp://files.example.com'
];

foreach ($urls as $url) {
    $valid = ValidationUtils::isUrl($url) ? '✓ Valid' : '✗ Invalid';
    echo "  {$url}: {$valid}\n";
}

echo "\n";

// IP Address Validation
echo "4. IP Address Validation\n";
echo "------------------------\n";

$ips = [
    '192.168.1.1',
    '127.0.0.1',
    '256.1.1.1',
    '2001:db8::1',
    '::1',
    'not-an-ip'
];

foreach ($ips as $ip) {
    $ipv4 = ValidationUtils::isIpv4($ip) ? 'IPv4' : '';
    $ipv6 = ValidationUtils::isIpv6($ip) ? 'IPv6' : '';
    $type = $ipv4 ?: ($ipv6 ?: 'Invalid');
    echo "  {$ip}: {$type}\n";
}

echo "\n";

// UUID Validation
echo "5. UUID Validation\n";
echo "------------------\n";

$uuids = [
    '550e8400-e29b-41d4-a716-446655440000',
    '6ba7b810-9dad-11d1-80b4-00c04fd430c8',
    'not-a-uuid',
    '550e8400e29b41d4a716446655440000'
];

foreach ($uuids as $uuid) {
    $valid = ValidationUtils::isUuid($uuid) ? '✓ Valid' : '✗ Invalid';
    echo "  {$uuid}: {$valid}\n";
}

echo "\n";

// Credit Card Validation
echo "6. Credit Card Validation (Luhn Algorithm)\n";
echo "-------------------------------------------\n";

$cards = [
    '4532015112830366',  // Valid Visa
    '5555555555554444',  // Valid Mastercard
    '378282246310005',   // Valid Amex
    '1234567890123456',  // Invalid
    '4532 0151 1283 0366' // With spaces
];

foreach ($cards as $card) {
    $valid = ValidationUtils::isCreditCard($card) ? '✓ Valid' : '✗ Invalid';
    echo "  {$card}: {$valid}\n";
}

echo "\n";

// Password Validation
echo "7. Strong Password Validation\n";
echo "-----------------------------\n";

$passwords = [
    'MyP@ssw0rd!',
    'password',
    'Password1',
    'short1!',
    'NoSpecial123'
];

foreach ($passwords as $password) {
    $valid = ValidationUtils::isStrongPassword($password) ? '✓ Strong' : '✗ Weak';
    echo "  {$password}: {$valid}\n";
}

echo "\n";

// Range Validation
echo "8. Range Validation\n";
echo "-------------------\n";

$age = 25;
echo "Age {$age} is between 18 and 65: " . (ValidationUtils::between($age, 18, 65) ? 'Yes' : 'No') . "\n";

$score = 95;
echo "Score {$score} is between 0 and 100: " . (ValidationUtils::between($score, 0, 100) ? 'Yes' : 'No') . "\n";

$username = 'john_doe';
echo "Username length (" . strlen($username) . ") is between 3 and 20: " . 
    (ValidationUtils::lengthBetween($username, 3, 20) ? 'Yes' : 'No') . "\n";

echo "\n";

// JSON Validation
echo "9. JSON Validation\n";
echo "------------------\n";

$jsonStrings = [
    '{"name":"John","age":30}',
    '[1,2,3,4,5]',
    'not valid json',
    '{"incomplete":'
];

foreach ($jsonStrings as $json) {
    $valid = ValidationUtils::isJson($json) ? '✓ Valid' : '✗ Invalid';
    echo "  {$json}: {$valid}\n";
}

echo "\n";

// China Mobile Validation
echo "10. China Mobile Phone Validation\n";
echo "---------------------------------\n";

$phones = [
    '13800138000',
    '15912345678',
    '138-0013-8000',
    '1380013800',
    '23800138000'
];

foreach ($phones as $phone) {
    $valid = ValidationUtils::isChinaMobile($phone) ? '✓ Valid' : '✗ Invalid';
    echo "  {$phone}: {$valid}\n";
}

echo "\n";

// Multiple Validation
echo "11. Multiple Validation\n";
echo "-----------------------\n";

$userData = [
    ['field' => 'email', 'value' => 'test@example.com', 'rule' => fn($v) => ValidationUtils::isEmail($v), 'message' => 'Invalid email'],
    ['field' => 'age', 'value' => 25, 'rule' => fn($v) => ValidationUtils::between($v, 18, 120), 'message' => 'Age must be between 18 and 120'],
    ['field' => 'username', 'value' => 'john_doe', 'rule' => fn($v) => ValidationUtils::isUsername($v), 'message' => 'Invalid username']
];

$results = ValidationUtils::validateMultiple($userData);

echo "Validation results:\n";
foreach ($results as $result) {
    $status = $result->isValid() ? '✓' : '✗';
    $field = $result->getField();
    echo "  {$status} {$field}";
    if (!$result->isValid()) {
        echo ": {$result->getMessage()}";
    }
    echo "\n";
}

$allValid = ValidationUtils::allValid($results);
echo "\nAll validations passed: " . ($allValid ? 'Yes' : 'No') . "\n";

echo "\n";

// Custom Validation
echo "12. Custom Validation\n";
echo "---------------------\n";

$customValidator = function($value) {
    return is_string($value) && strlen($value) >= 5 && strlen($value) <= 10;
};

$customResult = ValidationUtils::validate('Hello', $customValidator, 'custom_field', 'Value must be 5-10 characters');
echo "Custom validation result: " . ($customResult->isValid() ? 'Valid' : 'Invalid') . "\n";

$customResult2 = ValidationUtils::validate('Hi', $customValidator, 'custom_field', 'Value must be 5-10 characters');
echo "Custom validation result: " . ($customResult2->isValid() ? 'Valid' : 'Invalid');
if (!$customResult2->isValid()) {
    echo " - " . $customResult2->getMessage();
}
echo "\n";

echo "\n=== Examples completed ===\n";
