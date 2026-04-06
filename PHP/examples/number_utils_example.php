<?php
/**
 * Number Utilities Example for PHP
 * 
 * Demonstrates the usage of NumberUtils class
 */

require_once __DIR__ . '/../number_utils/mod.php';

use AllToolkit\NumberUtils;

echo "Number Utilities Examples\n";
echo str_repeat("=", 50) . "\n\n";

// Formatting
echo "1. Number Formatting\n";
echo "--------------------\n";
echo "format(1234567.89): " . NumberUtils::format(1234567.89) . "\n";
echo "format(1234567.89, 2): " . NumberUtils::format(1234567.89, 2) . "\n";
echo "currency(1234.5): " . NumberUtils::currency(1234.5) . "\n";
echo "currency(1234.5, '€'): " . NumberUtils::currency(1234.5, '€') . "\n";
echo "percentage(0.1567): " . NumberUtils::percentage(0.1567) . "\n";
echo "percentage(0.1567, 2): " . NumberUtils::percentage(0.1567, 2) . "\n";
echo "compact(1500000): " . NumberUtils::compact(1500000) . "\n";
echo "compact(2500000000): " . NumberUtils::compact(2500000000) . "\n\n";

// Ordinal and Words
echo "2. Ordinal and Words\n";
echo "--------------------\n";
echo "ordinal(1): " . NumberUtils::ordinal(1) . "\n";
echo "ordinal(21): " . NumberUtils::ordinal(21) . "\n";
echo "toWords(123): " . NumberUtils::toWords(123) . "\n";
echo "toWords(1234): " . NumberUtils::toWords(1234) . "\n\n";

// Roman Numerals
echo "3. Roman Numerals\n";
echo "-----------------\n";
echo "toRoman(2024): " . NumberUtils::toRoman(2024) . "\n";
echo "fromRoman('MMXXIV'): " . NumberUtils::fromRoman('MMXXIV') . "\n";
echo "toRoman(42): " . NumberUtils::toRoman(42) . "\n\n";

// Base Conversions
echo "4. Base Conversions\n";
echo "-------------------\n";
echo "toBinary(255): " . NumberUtils::toBinary(255) . "\n";
echo "toBinary(255, true): " . NumberUtils::toBinary(255, true) . "\n";
echo "toHex(255): " . NumberUtils::toHex(255) . "\n";
echo "toHex(255, true, true): " . NumberUtils::toHex(255, true, true) . "\n";
echo "toOctal(8): " . NumberUtils::toOctal(8) . "\n\n";

// Math Operations
echo "5. Math Operations\n";
echo "------------------\n";
echo "clamp(15, 0, 10): " . NumberUtils::clamp(15, 0, 10) . "\n";
echo "lerp(0, 100, 0.5): " . NumberUtils::lerp(0, 100, 0.5) . "\n";
echo "mapRange(5, 0, 10, 0, 100): " . NumberUtils::mapRange(5, 0, 10, 0, 100) . "\n";
echo "roundToMultiple(14, 5): " . NumberUtils::roundToMultiple(14, 5) . "\n";
echo "roundToPlaces(3.14159, 2): " . NumberUtils::roundToPlaces(3.14159, 2) . "\n\n";

// Statistics
echo "6. Statistics\n";
echo "-------------\n";
$data = [1, 2, 3, 4, 5];
echo "Data: " . implode(", ", $data) . "\n";
echo "mean: " . NumberUtils::mean($data) . "\n";
echo "median: " . NumberUtils::median($data) . "\n";
echo "range: " . NumberUtils::range($data) . "\n\n";

// Validation
echo "7. Validation\n";
echo "-------------\n";
echo "isNumeric('123'): " . (NumberUtils::isNumeric('123') ? 'true' : 'false') . "\n";
echo "isEven(4): " . (NumberUtils::isEven(4) ? 'true' : 'false') . "\n";
echo "isOdd(3): " . (NumberUtils::isOdd(3) ? 'true' : 'false') . "\n";
echo "isPrime(7): " . (NumberUtils::isPrime(7) ? 'true' : 'false') . "\n";
echo "isPerfectSquare(16): " . (NumberUtils::isPerfectSquare(16) ? 'true' : 'false') . "\n";
echo "between(5, 1, 10): " . (NumberUtils::between(5, 1, 10) ? 'true' : 'false') . "\n\n";

// GCD and LCM
echo "8. GCD and LCM\n";
echo "--------------\n";
echo "gcd(24, 36): " . NumberUtils::gcd(24, 36) . "\n";
echo "lcm(24, 36): " . NumberUtils::lcm(24, 36) . "\n\n";

// Factorial and Fibonacci
echo "9. Factorial and Fibonacci\n";
echo "--------------------------\n";
echo "factorial(5): " . NumberUtils::factorial(5) . "\n";
echo "fibonacci(10): " . NumberUtils::fibonacci(10) . "\n\n";

// Angle Conversion
echo "10. Angle Conversion\n";
echo "--------------------\n";
echo "toRadians(180): " . NumberUtils::toRadians(180) . "\n";
echo "toDegrees(PI): " . NumberUtils::toDegrees(M_PI) . "\n";
echo "normalizeAngle(450): " . NumberUtils::normalizeAngle(450) . "\n\n";

// Digit Operations
echo "11. Digit Operations\n";
echo "--------------------\n";
echo "sumOfDigits(123): " . NumberUtils::sumOfDigits(123) . "\n";
echo "reverseDigits(123): " . NumberUtils::reverseDigits(123) . "\n";
echo "isPalindrome(121): " . (NumberUtils::isPalindrome(121) ? 'true' : 'false') . "\n\n";

echo "All examples completed!\n";
