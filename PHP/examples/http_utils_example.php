<?php
/**
 * AllToolkit - PHP HTTP Utilities Example
 *
 * 展示 HTTP 工具类的各种使用场景。
 *
 * @package AllToolkit\PHP\HttpUtils
 * @license MIT
 */

require_once __DIR__ . '/../http_utils/mod.php';

use AllToolkit\HttpUtils;
use AllToolkit\HttpOptions;

echo "=== PHP HTTP Utilities Example ===\n\n";

// ============ URL 操作示例 ============

echo "1. URL Building:\n";
$url = HttpUtils::buildUrl('https://api.example.com/users', [
    'page' => 1,
    'limit' => 10,
    'sort' => 'name'
]);
echo "   Built URL: {$url}\n\n";

echo "2. URL Parsing:\n";
$parts = HttpUtils::parseUrl('https://user:pass@api.example.com:8080/v1/users?page=1#section');
echo "   Scheme: {$parts['scheme']}\n";
echo "   Host: {$parts['host']}\n";
echo "   Port: {$parts['port']}\n";
echo "   Path: {$parts['path']}\n";
echo "   Query: {$parts['query']}\n\n";

echo "3. Query String Operations:\n";
$params = HttpUtils::parseQueryString('foo=bar&baz=qux&num=123');
echo "   Parsed params: " . json_encode($params) . "\n";
$qs = HttpUtils::buildQueryString(['search' => 'hello world', 'page' => 2]);
echo "   Built query string: {$qs}\n\n";

echo "4. URL Validation:\n";
$urls = [
    'https://example.com',
    'not a url',
    'ftp://files.example.com',
    '/relative/path'
];
foreach ($urls as $u) {
    $valid = HttpUtils::isValidUrl($u) ? 'valid' : 'invalid';
    echo "   '{$u}' is {$valid}\n";
}
echo "\n";

echo "5. Domain and Path Extraction:\n";
echo "   Domain of 'https://api.example.com/v1': " . HttpUtils::getDomain('https://api.example.com/v1') . "\n";
echo "   Path of 'https://example.com/api/users': " . HttpUtils::getPath('https://example.com/api/users') . "\n\n";

// ============ HTTP 请求示例 ============

echo "6. HTTP GET Request (using httpbin.org):\n";
try {
    $response = HttpUtils::get('https://httpbin.org/get', ['timeout' => 10]);
    echo "   Status: {$response->statusCode} {$response->statusText}\n";
    echo "   Success: " . ($response->success ? 'true' : 'false') . "\n";
    echo "   Response Time: " . round($response->responseTime * 1000, 2) . "ms\n";
    if ($response->isJson()) {
        $data = $response->json();
        echo "   Origin: {$data['origin']}\n";
    }
} catch (Exception $e) {
    echo "   Error: " . $e->getMessage() . "\n";
}
echo "\n";

echo "7. HTTP POST JSON Request:\n";
try {
    $response = HttpUtils::postJson('https://httpbin.org/post', [
        'name' => 'John Doe',
        'email' => 'john@example.com',
        'age' => 30
    ]);
    echo "   Status: {$response->statusCode}\n";
    if ($response->isJson()) {
        $data = $response->json();
        echo "   Posted Data: " . json_encode($data['json']) . "\n";
    }
} catch (Exception $e) {
    echo "   Error: " . $e->getMessage() . "\n";
}
echo "\n";

echo "8. HTTP POST Form Request:\n";
try {
    $response = HttpUtils::postForm('https://httpbin.org/post', [
        'username' => 'admin',
        'password' => 'secret123'
    ]);
    echo "   Status: {$response->statusCode}\n";
    if ($response->isJson()) {
        $data = $response->json();
        echo "   Form Data: " . json_encode($data['form']) . "\n";
    }
} catch (Exception $e) {
    echo "   Error: " . $e->getMessage() . "\n";
}
echo "\n";

echo "9. HTTP PUT Request:\n";
try {
    $response = HttpUtils::putJson('https://httpbin.org/put', [
        'id' => 123,
        'status' => 'updated'
    ]);
    echo "   Status: {$response->statusCode}\n";
} catch (Exception $e) {
    echo "   Error: " . $e->getMessage() . "\n";
}
echo "\n";

echo "10. HTTP DELETE Request:\n";
try {
    $response = HttpUtils::delete('https://httpbin.org/delete');
    echo "    Status: {$response->statusCode}\n";
} catch (Exception $e) {
    echo "    Error: " . $e->getMessage() . "\n";
}
echo "\n";

echo "11. HTTP HEAD Request:\n";
try {
    $response = HttpUtils::head('https://httpbin.org/get');
    echo "    Status: {$response->statusCode}\n";
    echo "    Headers: " . json_encode($response->headers, JSON_PRETTY_PRINT) . "\n";
} catch (Exception $e) {
    echo "    Error: " . $e->getMessage() . "\n";
}
echo "\n";

echo "12. Custom Headers and Options:\n";
try {
    $options = new HttpOptions();
    $options->headers = [
        'X-Custom-Header' => 'MyValue',
        'Authorization' => 'Bearer token123'
    ];
    $options->timeout = 15;
    
    $response = HttpUtils::get('https://httpbin.org/headers', $options);
    echo "    Status: {$response->statusCode}\n";
    if ($response->isJson()) {
        $data = $response->json();
        echo "    Sent Headers: " . json_encode($data['headers']) . "\n";
    }
} catch (Exception $e) {
    echo "    Error: " . $e->getMessage() . "\n";
}
echo "\n";

echo "=== Example completed! ===\n";
