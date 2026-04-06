<?php
/**
 * Number Utilities Test Suite for PHP
 */

require_once __DIR__ . '/mod.php';

use AllToolkit\NumberUtils;

class NumberUtilsTest {
    private $passed = 0;
    private $failed = 0;
    
    public function run() {
        echo "Running NumberUtils Test Suite\n";
        echo str_repeat("=", 50) . "\n\n";
        
        $this->testFormat();
        $this->testCurrency();
        $this->testPercentage();
        $this->testCompact();
        $this->testOrdinal();
        $this->testRoman();
        $this->testBinary();
        $this->testMath();
        $this->testStatistics();
        $this->testValidation();
        $this->testGcdLcm();
        $this->testFactorial();
        $this->testAngleConversion();
        $this->testDigitOperations();
        
        echo "\n" . str_repeat("=", 50) . "\n";
        echo "Results: {$this->passed} passed, {$this->failed} failed\n";
        return $this->failed === 0;
    }
    
    private function assert($condition, $message) {
        if ($condition) {
            echo "  ✓ {$message}\n";
            $this->passed++;
        } else {
            echo "  ✗ {$message}\n";
            $this->failed++;
        }
    }
    
    private function assertEquals($expected, $actual, $message) {
        $this->assert($expected === $actual, "{$message} (expected: {$expected}, got: {$actual})");
    }
    
    private function testFormat() {
        echo "Testing format()...\n";
        $this->assertEquals("1,234", NumberUtils::format(1234), "Format with thousands");
        $this->assertEquals("1,234.56", NumberUtils::format(1234.56, 2), "Format with decimals");
        echo "\n";
    }
    
    private function testCurrency() {
        echo "Testing currency()...\n";
        $this->assertEquals("\$1,234.56", NumberUtils::currency(1234.56), "Currency");
        echo "\n";
    }
    
    private function testPercentage() {
        echo "Testing percentage()...\n";
        $this->assertEquals("50%", NumberUtils::percentage(0.5), "Percentage");
        $this->assertEquals("33.33%", NumberUtils::percentage(0.3333, 2), "Percentage decimals");
        echo "\n";
    }
    
    private function testCompact() {
        echo "Testing compact()...\n";
        $this->assertEquals("1.5K", NumberUtils::compact(1500), "Compact K");
        $this->assertEquals("2.5M", NumberUtils::compact(2500000), "Compact M");
        echo "\n";
    }
    
    private function testOrdinal() {
        echo "Testing ordinal()...\n";
        $this->assertEquals("1st", NumberUtils::ordinal(1), "Ordinal 1st");
        $this->assertEquals("2nd", NumberUtils::ordinal(2), "Ordinal 2nd");
        $this->assertEquals("3rd", NumberUtils::ordinal(3), "Ordinal 3rd");
        $this->assertEquals("4th", NumberUtils::ordinal(4), "Ordinal 4th");
        $this->assertEquals("11th", NumberUtils::ordinal(11), "Ordinal 11th");
        echo "\n";
    }
    
    private function testRoman() {
        echo "Testing Roman numerals...\n";
        $this->assertEquals("I", NumberUtils::toRoman(1), "Roman 1");
        $this->assertEquals("IV", NumberUtils::toRoman(4), "Roman 4");
        $this->assertEquals("XLII", NumberUtils::toRoman(42), "Roman 42");
        $this->assertEquals(42, NumberUtils::fromRoman("XLII"), "From Roman");
        echo "\n";
    }
    
    private function testBinary() {
        echo "Testing binary...\n";
        $this->assertEquals("1010", NumberUtils::toBinary(10), "Binary");
        $this->assertEquals("0b1010", NumberUtils::toBinary(10, true), "Binary prefix");
        echo "\n";
    }
    
    private function testMath() {
        echo "Testing math functions...\n";
        $this->assertEquals(5, NumberUtils::clamp(10, 0, 5), "Clamp");
        $this->assertEquals(50, NumberUtils::lerp(0, 100, 0.5), "Lerp");
        $this->assert(NumberUtils::approxEqual(0.1 + 0.2, 0.3), "Approx equal");
        echo "\n";
    }
    
    private function testStatistics() {
        echo "Testing statistics...\n";
        $this->assertEquals(3, NumberUtils::mean([1, 2, 3, 4, 5]), "Mean");
        $this->assertEquals(3, NumberUtils::median([1, 2, 3, 4, 5]), "Median");
        echo "\n";
    }
    
    private function testValidation() {
        echo "Testing validation...\n";
        $this->assert(NumberUtils::isNumeric("123"), "Is numeric");
        $this->assert(NumberUtils::isEven(4), "Is even");
        $this->assert(NumberUtils::isOdd(3), "Is odd");
        $this->assert(NumberUtils::isPrime(7), "Is prime");
        $this->assert(NumberUtils::isPerfectSquare(16), "Is perfect square");
        echo "\n";
    }
    
    private function testGcdLcm() {
        echo "Testing GCD/LCM...\n";
        $this->assertEquals(12, NumberUtils::gcd(24, 36), "GCD");
        $this->assertEquals(72, NumberUtils::lcm(24, 36), "LCM");
        echo "\n";
    }
    
    private function testFactorial() {
        echo "Testing factorial/fibonacci...\n";
        $this->assertEquals(120, NumberUtils::factorial(5), "Factorial");
        $this->assertEquals(8, NumberUtils::fibonacci(6), "Fibonacci");
        echo "\n";
    }
    
    private function testAngleConversion() {
        echo "Testing angle conversion...\n";
        $this->assertEquals(180.0, NumberUtils::toDegrees(M_PI), "To degrees");
        $this->assertEquals(M_PI, NumberUtils::toRadians(180), "To radians");
        echo "\n";
    }
    
    private function testDigitOperations() {
        echo "Testing digit operations...\n";
        $this->assertEquals(6, NumberUtils::sumOfDigits(123), "Sum of digits");
        $this->assertEquals(321, NumberUtils::reverseDigits(123), "Reverse digits");
        $this->assert(NumberUtils::isPalindrome(121), "Is palindrome");
        echo "\n";
    }
}

$test = new NumberUtilsTest();
$test->run();
