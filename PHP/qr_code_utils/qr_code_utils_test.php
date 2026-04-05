<?php
/**
 * AllToolkit - QR Code Utilities Test Suite
 *
 * Comprehensive test suite for QR Code generation functionality.
 *
 * @package AllToolkit\QrCodeUtils
 */

require_once __DIR__ . '/mod.php';

use AllToolkit\QrCodeGenerator;
use AllToolkit\QrCodeUtils;
use AllToolkit\QrCodeException;

/**
 * Simple test runner
 */
class TestRunner {
    private $tests = 0;
    private $passed = 0;
    private $failed = 0;
    private $errors = [];

    public function assert($condition, $message) {
        $this->tests++;
        if ($condition) {
            $this->passed++;
            echo "  ✓ {$message}\n";
        } else {
            $this->failed++;
            $this->errors[] = $message;
            echo "  ✗ {$message}\n";
        }
    }

    public function assertEquals($expected, $actual, $message) {
        $this->assert($expected === $actual, $message . " (expected: {$expected}, got: {$actual})");
    }

    public function assertTrue($condition, $message) {
        $this->assert($condition, $message);
    }

    public function assertFalse($condition, $message) {
        $this->assert(!$condition, $message);
    }

    public function assertException($callback, $expectedMessage = null, $message = 'Should throw exception') {
        $this->tests++;
        try {
            $callback();
            $this->failed++;
            $this->errors[] = $message;
            echo "  ✗ {$message} (no exception thrown)\n";
        } catch (QrCodeException $e) {
            if ($expectedMessage === null || strpos($e->getMessage(), $expectedMessage) !== false) {
                $this->passed++;
                echo "  ✓ {$message}\n";
            } else {
                $this->failed++;
                $this->errors[] = $message;
                echo "  ✗ {$message} (wrong message: {$e->getMessage()})\n";
            }
        }
    }

    public function summary() {
        echo "\n";
        echo "========================================\n";
        echo "Test Results: {$this->passed}/{$this->tests} passed\n";
        echo "========================================\n";

        if ($this->failed > 0) {
            echo "\nFailed tests:\n";
            foreach ($this->errors as $error) {
                echo "  - {$error}\n";
            }
        }

        return $this->failed === 0;
    }
}

// Run tests
$runner = new TestRunner();

echo "========================================\n";
echo "QR Code Utils Test Suite\n";
echo "========================================\n\n";

// Test 1: Constructor validation
echo "Test Group: Constructor Validation\n";
echo "------------------------------------\n";

try {
    $qr = new QrCodeGenerator(1, QrCodeGenerator::ERROR_CORRECTION_L);
    $runner->assertTrue($qr instanceof QrCodeGenerator, "Create QR Code generator v1, level L");
} catch (Exception $e) {
    $runner->assertFalse(true, "Create QR Code generator v1, level L: " . $e->getMessage());
}

$runner->assertException(function() {
    new QrCodeGenerator(0, QrCodeGenerator::ERROR_CORRECTION_L);
}, "Version must be between", "Invalid version (0) should throw exception");

$runner->assertException(function() {
    new QrCodeGenerator(11, QrCodeGenerator::ERROR_CORRECTION_L);
}, "Version must be between", "Invalid version (11) should throw exception");

$runner->assertException(function() {
    new QrCodeGenerator(1, -1);
}, "Invalid error correction level", "Invalid error correction level (-1) should throw exception");

$runner->assertException(function() {
    new QrCodeGenerator(1, 4);
}, "Invalid error correction level", "Invalid error correction level (4) should throw exception");

echo "\n";

// Test 2: Mode detection
echo "Test Group: Mode Detection\n";
echo "------------------------------------\n";

$runner->assertEquals(QrCodeGenerator::MODE_NUMERIC, QrCodeGenerator::detectMode("1234567890"), "Detect numeric mode");
$runner->assertEquals(QrCodeGenerator::MODE_NUMERIC, QrCodeGenerator::detectMode("0"), "Detect numeric mode (single digit)");
$runner->assertEquals(QrCodeGenerator::MODE_ALPHANUMERIC, QrCodeGenerator::detectMode("HELLO WORLD"), "Detect alphanumeric mode");
$runner->assertEquals(QrCodeGenerator::MODE_ALPHANUMERIC, QrCodeGenerator::detectMode("ABC123"), "Detect alphanumeric mode (mixed)");
$runner->assertEquals(QrCodeGenerator::MODE_BYTE, QrCodeGenerator::detectMode("Hello World"), "Detect byte mode (lowercase)");
$runner->assertEquals(QrCodeGenerator::MODE_BYTE, QrCodeGenerator::detectMode("Hello, World!"), "Detect byte mode (punctuation)");
$runner->assertEquals(QrCodeGenerator::MODE_BYTE, QrCodeGenerator::detectMode("你好世界"), "Detect byte mode (Unicode)");

echo "\n";

// Test 3: QR Code generation
echo "Test Group: QR Code Generation\n";
echo "------------------------------------\n";

$qr = new QrCodeGenerator(1, QrCodeGenerator::ERROR_CORRECTION_L);
$modules = $qr->generate("HELLO");

$runner->assertTrue(is_array($modules), "Generate returns array");
$runner->assertEquals(21, count($modules), "Version 1 has 21x21 modules");
$runner->assertEquals(21, count($modules[0]), "Each row has 21 modules");
$runner->assertEquals(1, $qr->getVersion(), "Get version returns 1");
$runner->assertEquals(21, $qr->getModuleCount(), "Get module count returns 21");
$runner->assertEquals('L', $qr->getErrorCorrectionLevelName(), "Get error correction level name returns L");

echo "\n";

// Test 4: ASCII output
echo "Test Group: ASCII Output\n";
echo "------------------------------------\n";

$qr = new QrCodeGenerator(1, QrCodeGenerator::ERROR_CORRECTION_L);
$ascii = $qr->toAscii("TEST");

$runner->assertTrue(strpos($ascii, '██') !== false, "ASCII output contains dark modules");
$runner->assertTrue(strpos($ascii, '  ') !== false, "ASCII output contains light modules");
$runner->assertTrue(strpos($ascii, "\n") !== false, "ASCII output contains newlines");

echo "\n";

// Test 5: SVG output
echo "Test Group: SVG Output\n";
echo "------------------------------------\n";

$qr = new QrCodeGenerator(1, QrCodeGenerator::ERROR_CORRECTION_L);
$svg = $qr->toSvg("TEST");

$runner->assertTrue(strpos($svg, '<?xml') !== false, "SVG starts with XML declaration");
$runner->assertTrue(strpos($svg, '<svg') !== false, "SVG contains svg element");
$runner->assertTrue(strpos($svg, '</svg>') !== false, "SVG ends with closing svg tag");
$runner->assertTrue(strpos($svg, 'rect') !== false, "SVG contains rect elements");
$runner->assertTrue(strpos($svg, 'width="') !== false, "SVG has width attribute");
$runner->assertTrue(strpos($svg, 'height="') !== false, "SVG has height attribute");

echo "\n";

// Test 6: Matrix output
echo "Test Group: Matrix Output\n";
echo "------------------------------------\n";

$qr = new QrCodeGenerator(1, QrCodeGenerator::ERROR_CORRECTION_L);
$matrix = $qr->toMatrix("TEST");

$runner->assertTrue(is_array($matrix), "Matrix is array");
$runner->assertEquals(21, count($matrix), "Matrix has 21 rows");
$runner->assertEquals(21, count($matrix[0]), "Matrix has 21 columns");

// Check that matrix contains only 0s and 1s
$validValues = true;
for ($i = 0; $i < 21; $i++) {
    for ($j = 0; $j < 21; $j++) {
        if ($matrix[$i][$j] !== 0 && $matrix[$i][$j] !== 1) {
            $validValues = false;
            break 2;
        }
    }
}
$runner->assertTrue($validValues, "Matrix contains only 0s and 1s");

echo "\n";

// Test 7: Utility functions
echo "Test Group: Utility Functions\n";
echo "------------------------------------\n";

$ascii = QrCodeUtils::toAscii("HELLO");
$runner->assertTrue(strpos($ascii, '██') !== false, "QrCodeUtils::toAscii generates output");

$svg = QrCodeUtils::toSvg("WORLD");
$runner->assertTrue(strpos($svg, '<svg') !== false, "QrCodeUtils::toSvg generates SVG");

$matrix = QrCodeUtils::toMatrix("TEST123");
$runner->assertTrue(is_array($matrix), "QrCodeUtils::toMatrix returns array");

$runner->assertEquals('Numeric', QrCodeUtils::getModeName(QrCodeGenerator::MODE_NUMERIC), "Get mode name for numeric");
$runner->assertEquals('Alphanumeric', QrCodeUtils::getModeName(QrCodeGenerator::MODE_ALPHANUMERIC), "Get mode name for alphanumeric");
$runner->assertEquals('Byte', QrCodeUtils::getModeName(QrCodeGenerator::MODE_BYTE), "Get mode name for byte");

$runner->assertEquals('L', QrCodeUtils::getErrorCorrectionLevelName(QrCodeGenerator::ERROR_CORRECTION_L), "Get EC level name L");
$runner->assertEquals('M', QrCodeUtils::getErrorCorrectionLevelName(QrCodeGenerator::ERROR_CORRECTION_M), "Get EC level name M");
$runner->assertEquals('Q', QrCodeUtils::getErrorCorrectionLevelName(QrCodeGenerator::ERROR_CORRECTION_Q), "Get EC level name Q");
$runner->assertEquals('H', QrCodeUtils::getErrorCorrectionLevelName(QrCodeGenerator::ERROR_CORRECTION_H), "Get EC level name H");

echo "\n";

// Test 8: Different versions
echo "Test Group: Different Versions\n";
echo "------------------------------------\n";

for ($v = 1; $v <= 5; $v++) {
    $qr = new QrCodeGenerator($v, QrCodeGenerator::ERROR_CORRECTION_L);
    $modules = $qr->generate("TEST");
    $expectedSize = 17 + 4 * $v;
    $runner->assertEquals($expectedSize, count($modules), "Version {$v} has {$expectedSize}x{$expectedSize} modules");
}

echo "\n";

// Test 9: Different error correction levels
echo "Test Group: Error Correction Levels\n";
echo "------------------------------------\n";

$levels = [
    QrCodeGenerator::ERROR_CORRECTION_L => 'L',
    QrCodeGenerator::ERROR_CORRECTION_M => 'M',
    QrCodeGenerator::ERROR_CORRECTION_Q => 'Q',
    QrCodeGenerator::ERROR_CORRECTION_H => 'H',
];

foreach ($levels as $level => $name) {
    $qr = new QrCodeGenerator(1, $level);
    $modules = $qr->generate("HELLO");
    $runner->assertTrue(is_array($modules), "Generate with error correction level {$name}");
    $runner->assertEquals($name, $qr->getErrorCorrectionLevelName(), "Get EC level name {$name}");
}

echo "\n";

// Test 10: Various data types
echo "Test Group: Various Data Types\n";
echo "------------------------------------\n";

$testData = [
    "1234567890" => "Numeric data",
    "HELLO WORLD" => "Alphanumeric data",
    "Hello, World!" => "Byte data with punctuation",
    "test@example.com" => "Email address",
    "https://example.com" => "URL",
    "Test123" => "Mixed alphanumeric",
];

foreach ($testData as $data => $description) {
    $qr = new QrCodeGenerator(2, QrCodeGenerator::ERROR_CORRECTION_L);
    $modules = $qr->generate($data);
    $runner->assertTrue(is_array($modules), "Generate QR for {$description}");
}

echo "\n";

// Test 11: Custom ASCII characters
echo "Test Group: Custom ASCII Characters\n";
echo "------------------------------------\n";

$qr = new QrCodeGenerator(1, QrCodeGenerator::ERROR_CORRECTION_L);
$ascii = $qr->toAscii("TEST", "##", "..");
$runner->assertTrue(strpos($ascii, '##') !== false, "Custom dark character works");
$runner->assertTrue(strpos($ascii, '..') !== false, "Custom light character works");

echo "\n";

// Test 12: Custom SVG colors
echo "Test Group: Custom SVG Colors\n";
echo "------------------------------------\n";

$qr = new QrCodeGenerator(1, QrCodeGenerator::ERROR_CORRECTION_L);
$svg = $qr->toSvg("TEST", 4, '#ff0000', '#ffffff');
$runner->assertTrue(strpos($svg, '#ff0000') !== false, "Custom dark color in SVG");
$runner->assertTrue(strpos($svg, '#ffffff') !== false, "Custom light color in SVG");

echo "\n";

// Print summary
$success = $runner->summary();

exit($success ? 0 : 1);