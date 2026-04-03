<?php
/**
 * AllToolkit - PHP HTTP Utilities Test Suite
 *
 * @package AllToolkit\PHP\HttpUtils
 * @license MIT
 */

require_once __DIR__ . '/mod.php';

use AllToolkit\HttpResponse;
use AllToolkit\HttpOptions;
use AllToolkit\HttpUtils;

class TestRunner
{
    private static int $passed = 0;
    private static int $failed = 0;

    public static function run(string $name, callable $test): void
    {
        try {
            $test();
            self::$passed++;
            echo "✓ {$name}\n";
        } catch (Exception $e) {
            self::$failed++;
            echo "✗ {$name}: " . $e->getMessage() . "\n";
        }
    }

    public static function assert(bool $condition, string $message = 'Assertion failed'): void
    {
        if (!$condition) {
            throw new Exception($message);
        }
    }

    public static function assertEquals($expected, $actual): void
    {
        if ($expected !== $actual) {
            throw new Exception("Expected: " . var_export($expected, true) . ", Got: " . var_export($actual, true));
        }
    }

    public static function summary(): void
    {
        $total = self::$passed + self::$failed;
        echo "\n========================================\n";
        echo "Total: {$total}, Passed: " . self::$passed . ", Failed: " . self::$failed . "\n";
        exit(self::$failed > 0 ? 1 : 0);
    }
}

echo "=== URL Utilities Tests ===\n";

TestRunner::run('buildUrl with no params', function () {
    $url = HttpUtils::buildUrl('https://example.com/path', []);
    TestRunner::assertEquals('https://example.com/path', $url);
});

TestRunner::run('buildUrl with params', function () {
    $url = HttpUtils::buildUrl('https://example.com/path', ['foo' => 'bar']);
    TestRunner::assert(strpos($url, 'foo=bar') !== false);
});

TestRunner::run('urlEncode', function () {
    $encoded = HttpUtils::urlEncode('hello world');
    TestRunner::assertEquals('hello+world', $encoded);
});

TestRunner::run('urlDecode', function () {
    $decoded = HttpUtils::urlDecode('hello%20world');
    TestRunner::assertEquals('hello world', $decoded);
});

TestRunner::run('parseUrl', function () {
    $parts = HttpUtils::parseUrl('https://example.com:8080/path?query=1');
    TestRunner::assertEquals('https', $parts['scheme']);
    TestRunner::assertEquals('example.com', $parts['host']);
    TestRunner::assertEquals(8080, $parts['port']);
});

TestRunner::run('parseQueryString', function () {
    $params = HttpUtils::parseQueryString('foo=bar&baz=qux');
    TestRunner::assertEquals('bar', $params['foo']);
    TestRunner::assertEquals('qux', $params['baz']);
});

TestRunner::run('isValidUrl valid', function () {
    TestRunner::assert(HttpUtils::isValidUrl('https://example.com'));
});

TestRunner::run('isValidUrl invalid', function () {
    TestRunner::assert(!HttpUtils::isValidUrl('not a url'));
});

TestRunner::run('getDomain', function () {
    TestRunner::assertEquals('example.com', HttpUtils::getDomain('https://example.com/path'));
});

TestRunner::run('getPath', function () {
    TestRunner::assertEquals('/path/to/resource', HttpUtils::getPath('https://example.com/path/to/resource'));
});

echo "\n=== HttpResponse Tests ===\n";

TestRunner::run('HttpResponse success for 200', function () {
    $response = new HttpResponse(200, 'OK', [], 'body', 'url', 0.5, null);
    TestRunner::assert($response->success);
});

TestRunner::run('HttpResponse not success for 404', function () {
    $response = new HttpResponse(404, 'Not Found', [], 'body', 'url', 0.5, null);
    TestRunner::assert(!$response->success);
});

TestRunner::run('HttpResponse json parsing', function () {
    $response = new HttpResponse(200, 'OK', [], '{"key":"value"}', 'url', 0.5, null);
    $data = $response->json();
    TestRunner::assertEquals('value', $data['key']);
});

TestRunner::run('HttpResponse isJson', function () {
    $response = new HttpResponse(200, 'OK', [], '{"key":"value"}', 'url', 0.5, null);
    TestRunner::assert($response->isJson());
});

echo "\n=== HttpOptions Tests ===\n";

TestRunner::run('HttpOptions fromArray', function () {
    $opts = HttpOptions::fromArray(['timeout' => 60]);
    TestRunner::assertEquals(60, $opts->timeout);
});

TestRunner::run('HttpOptions default values', function () {
    $opts = new HttpOptions();
    TestRunner::assertEquals(30, $opts->timeout);
});

echo "\n=== Live HTTP Tests ===\n";

try {
    $response = HttpUtils::get('https://httpbin.org/get', ['timeout' => 10]);
    if ($response->success) {
        TestRunner::run('GET request to httpbin', function () use ($response) {
            TestRunner::assert($response->success);
            TestRunner::assert($response->isJson());
        });
    }
} catch (Exception $e) {
    echo "Skipping live HTTP tests (offline)\n";
}

TestRunner::summary();
