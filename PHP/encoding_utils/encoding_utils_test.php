<?php
/**
 * AllToolkit - Encoding Utilities Test Suite for PHP
 *
 * Comprehensive test suite for the EncodingUtils module.
 *
 * @package AllToolkit\EncodingUtils
 * @version 1.0.0
 * @license MIT
 */

require_once __DIR__ . '/mod.php';

use AllToolkit\EncodingUtils;

/**
 * Simple test runner
 */
class TestRunner
{
    private static $passed = 0;
    private static $failed = 0;

    public static function test($name, $test)
    {
        try {
            $test();
            self::$passed++;
            echo "✓ {$name}\n";
        } catch (Exception $e) {
            self::$failed++;
            echo "✗ {$name}: {$e->getMessage()}\n";
        }
    }

    public static function assertEquals($expected, $actual, $message = '')
    {
        if ($expected !== $actual) {
            $msg = $message ?: "Expected " . var_export($expected, true) . " but got " . var_export($actual, true);
            throw new Exception($msg);
        }
    }

    public static function assertTrue($condition, $message = '')
    {
        if (!$condition) {
            throw new Exception($message ?: "Expected true but got false");
        }
    }

    public static function assertFalse($condition, $message = '')
    {
        if ($condition) {
            throw new Exception($message ?: "Expected false but got true");
        }
    }

    public static function summary()
    {
        $total = self::$passed + self::$failed;
        echo "\n========================================\n";
        echo "Test Summary: {$total} tests, " . self::$passed . " passed, " . self::$failed . " failed\n";
        echo "========================================\n";
        return self::$failed === 0;
    }
}

echo "========================================\n";
echo "EncodingUtils Test Suite\n";
echo "========================================\n\n";

// Test 1: UTF-8 detection and validation
TestRunner::test('isUtf8 - valid UTF-8', function () {
    TestRunner::assertTrue(EncodingUtils::isUtf8('Hello World'));
    TestRunner::assertTrue(EncodingUtils::isUtf8('你好世界'));
    TestRunner::assertTrue(EncodingUtils::isUtf8('🎉 Emoji test'));
});

TestRunner::test('isUtf8 - empty string', function () {
    TestRunner::assertTrue(EncodingUtils::isUtf8(''));
    TestRunner::assertTrue(EncodingUtils::isUtf8(null));
});

// Test 2: Encoding detection
TestRunner::test('detectEncoding - UTF-8', function () {
    TestRunner::assertEquals('UTF-8', EncodingUtils::detectEncoding('Hello World'));
});

TestRunner::test('detectEncoding - Chinese UTF-8', function () {
    TestRunner::assertEquals('UTF-8', EncodingUtils::detectEncoding('你好世界'));
});

TestRunner::test('detectEncoding - empty string', function () {
    TestRunner::assertEquals('UTF-8', EncodingUtils::detectEncoding(''));
});

// Test 3: UTF-8 conversion
TestRunner::test('toUtf8 - already UTF-8', function () {
    TestRunner::assertEquals('Hello World', EncodingUtils::toUtf8('Hello World'));
});

TestRunner::test('toUtf8 - Chinese', function () {
    TestRunner::assertEquals('你好世界', EncodingUtils::toUtf8('你好世界'));
});

// Test 4: Base64 encoding/decoding
TestRunner::test('base64Encode - basic string', function () {
    TestRunner::assertEquals('SGVsbG8gV29ybGQ=', EncodingUtils::base64Encode('Hello World'));
});

TestRunner::test('base64Encode - Chinese', function () {
    $input = '你好世界';
    $encoded = EncodingUtils::base64Encode($input);
    TestRunner::assertEquals($input, EncodingUtils::base64Decode($encoded));
});

TestRunner::test('base64Decode - valid', function () {
    TestRunner::assertEquals('Hello World', EncodingUtils::base64Decode('SGVsbG8gV29ybGQ='));
});

TestRunner::test('base64Decode - invalid', function () {
    TestRunner::assertFalse(EncodingUtils::base64Decode('Invalid!@#$'));
});

TestRunner::test('base64Encode - empty string', function () {
    TestRunner::assertEquals('', EncodingUtils::base64Encode(''));
    TestRunner::assertEquals('', EncodingUtils::base64Encode(null));
});

// Test 5: URL-safe Base64
TestRunner::test('base64UrlEncode - no special chars', function () {
    $input = 'Hello+World/Test';
    $encoded = EncodingUtils::base64UrlEncode($input);
    TestRunner::assertFalse(strpos($encoded, '+') !== false);
    TestRunner::assertFalse(strpos($encoded, '/') !== false);
});

TestRunner::test('base64UrlEncode - without padding', function () {
    $encoded = EncodingUtils::base64UrlEncode('Hello World', false);
    TestRunner::assertFalse(strpos($encoded, '=') !== false);
});

TestRunner::test('base64UrlDecode - roundtrip', function () {
    $input = 'Hello+World/Test';
    $encoded = EncodingUtils::base64UrlEncode($input);
    TestRunner::assertEquals($input, EncodingUtils::base64UrlDecode($encoded));
});

// Test 6: URL encoding
TestRunner::test('urlEncode - basic', function () {
    TestRunner::assertEquals('Hello+World', EncodingUtils::urlEncode('Hello World'));
});

TestRunner::test('urlEncode - special chars', function () {
    TestRunner::assertEquals('Hello%40World%23Test', EncodingUtils::urlEncode('Hello@World#Test'));
});

TestRunner::test('urlDecode - basic', function () {
    TestRunner::assertEquals('Hello World', EncodingUtils::urlDecode('Hello+World'));
});

TestRunner::test('urlDecode - special chars', function () {
    TestRunner::assertEquals('Hello@World#Test', EncodingUtils::urlDecode('Hello%40World%23Test'));
});

// Test 7: Raw URL encoding
TestRunner::test('rawUrlEncode - basic', function () {
    TestRunner::assertEquals('Hello%20World', EncodingUtils::rawUrlEncode('Hello World'));
});

TestRunner::test('rawUrlDecode - basic', function () {
    TestRunner::assertEquals('Hello World', EncodingUtils::rawUrlDecode('Hello%20World'));
});

// Test 8: HTML encoding
TestRunner::test('htmlEncode - special chars', function () {
    $encoded = EncodingUtils::htmlEncode('<script>alert("test")</script>');
    TestRunner::assertFalse(strpos($encoded, '<script>') !== false);
    TestRunner::assertTrue(strpos($encoded, '&lt;') !== false);
});

TestRunner::test('htmlDecode - special chars', function () {
    $input = '&lt;script&gt;alert(&quot;test&quot;)&lt;/script&gt;';
    TestRunner::assertEquals('<script>alert("test")</script>', EncodingUtils::htmlDecode($input));
});

// Test 9: Hex encoding
TestRunner::test('toHex - basic', function () {
    TestRunner::assertEquals('48656c6c6f', EncodingUtils::toHex('Hello'));
});

TestRunner::test('toHex - uppercase', function () {
    TestRunner::assertEquals('48656C6C6F', EncodingUtils::toHex('Hello', 'UTF-8', true));
});

TestRunner::test('fromHex - basic', function () {
    TestRunner::assertEquals('Hello', EncodingUtils::fromHex('48656c6c6f'));
});

TestRunner::test('fromHex - invalid', function () {
    TestRunner::assertFalse(EncodingUtils::fromHex('Invalid!'));
});

// Test 10: Binary encoding
TestRunner::test('toBinary - basic', function () {
    TestRunner::assertEquals('01000001 01000010', EncodingUtils::toBinary('AB'));
});

TestRunner::test('fromBinary - basic', function () {
    TestRunner::assertEquals('AB', EncodingUtils::fromBinary('01000001 01000010'));
});

// Test 11: Quoted-printable
TestRunner::test('quotedPrintableEncode - roundtrip', function () {
    $input = 'Hello World! 你好';
    $encoded = EncodingUtils::quotedPrintableEncode($input);
    TestRunner::assertEquals($input, EncodingUtils::quotedPrintableDecode($encoded));
});

// Test 12: Unicode escape
TestRunner::test('toUnicodeEscape - json format', function () {
    $result = EncodingUtils::toUnicodeEscape('A', 'UTF-8', 'json');
    TestRunner::assertEquals('\\u0041', $result);
});

TestRunner::test('fromUnicodeEscape - json format', function () {
    TestRunner::assertEquals('A', EncodingUtils::fromUnicodeEscape('\\u0041', 'json'))