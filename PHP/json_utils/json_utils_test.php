<?php
/**
 * AllToolkit - JSON Utilities Test Suite
 *
 * Comprehensive test suite for JsonUtils class
 *
 * @author AllToolkit Contributors
 * @license MIT
 */

require_once __DIR__ . '/mod.php';

use AllToolkit\JsonUtils;

// Test counter
$passed = 0;
$failed = 0;

function test($name, $condition) {
    global $passed, $failed;
    if ($condition) {
        echo "✓ $name\n";
        $passed++;
    } else {
        echo "✗ $name\n";
        $failed++;
    }
}

function test_group($name) {
    echo "\n=== $name ===\n";
}

echo "AllToolkit - JSON Utilities Test Suite\n";
echo "=======================================\n";

// Parse Tests
test_group("Parse Tests");

$json = '{"name":"John","age":30}';
$result = JsonUtils::parse($json);
test("Parse valid JSON", $result !== null && $result['name'] === 'John');

test("Parse invalid JSON returns null", JsonUtils::parse('invalid') === null);
test("Parse empty string returns null", JsonUtils::parse('') === null);

// Parse with object return
$obj = JsonUtils::parse($json, false);
test("Parse as object", is_object($obj) && $obj->name === 'John');

// Parse or throw
try {
    JsonUtils::parseOrThrow('invalid');
    test("Parse or throw throws exception", false);
} catch (\RuntimeException $e) {
    test("Parse or throw throws exception", true);
}

// Validation Tests
test_group("Validation Tests");

test("IsValid returns true for valid JSON", JsonUtils::isValid('{"a":1}'));
test("IsValid returns false for invalid JSON", !JsonUtils::isValid('invalid'));
test("IsValid returns false for empty string", !JsonUtils::isValid(''));

$error = JsonUtils::getError('invalid');
test("GetError returns error message", $error !== null && strlen($error) > 0);

$error = JsonUtils::getError('{"a":1}');
test("GetError returns null for valid JSON", $error === null);

// Stringify Tests
test_group("Stringify Tests");

$data = ['name' => 'John', 'age' => 30];
$json = JsonUtils::stringify($data);
test("Stringify array", is_string($json) && strlen($json) > 0);

$pretty = JsonUtils::stringify($data, true);
test("Stringify with pretty print", strpos($pretty, "\n") !== false);

$nullResult = JsonUtils::tryStringify("\x80\x81"); // Invalid UTF-8
test("TryStringify returns null on error", $nullResult === null);

// Pretty Print Tests
test_group("Pretty Print Tests");

$minified = '{"name":"John","age":30}';
$pretty = JsonUtils::prettyPrint($minified);
test("Pretty print adds formatting", strpos($pretty, "\n") !== false);

test("Pretty print invalid JSON returns null", JsonUtils::prettyPrint('invalid') === null);

// Minify Tests
test_group("Minify Tests");

$pretty = "{\n  \"name\": \"John\",\n  \"age\": 30\n}";
$minified = JsonUtils::minify($pretty);
test("Minify removes whitespace", strpos($minified, "\n") === false);

// Get/Set/Has Tests
test_group("Get/Set/Has Tests");

$data = [
    'user' => [
        'name' => 'John',
        'address' => [
            'city' => 'New York'
        ]
    ]
];

test("Get nested value", JsonUtils::get($data, 'user.name') === 'John');
test("Get deeply nested value", JsonUtils::get($data, 'user.address.city') === 'New York');
test("Get with default", JsonUtils::get($data, 'user.nonexistent', 'default') === 'default');
test("Get returns null for missing path", JsonUtils::get($data, 'nonexistent') === null);

test("Has returns true for existing path", JsonUtils::has($data, 'user.name'));
test("Has returns false for missing path", !JsonUtils::has($data, 'user.nonexistent'));

// Set tests
$arr = [];
JsonUtils::set($arr, 'user.name', 'John');
test("Set nested value", $arr['user']['name'] === 'John');

JsonUtils::set($arr, 'user.address.city', 'NYC');
test("Set deeply nested value", $arr['user']['address']['city'] === 'NYC');

// Remove Tests
test_group("Remove Tests");

$arr = ['a' => ['b' => ['c' => 'value']]];
$removed = JsonUtils::remove($arr, 'a.b.c');
test("Remove returns true on success", $removed);
test("Remove actually removes value", !isset($arr['a']['b']['c']));

$notRemoved = JsonUtils::remove($arr, 'nonexistent.path');
test("Remove returns false for missing path", !$notRemoved);

// Merge Tests
test_group("Merge Tests");

$base = ['a' => 1, 'b' => ['c' => 2]];
$overlay = ['b' => ['d' => 3], 'e' => 4];
$merged = JsonUtils::merge($base, $overlay);
test("Merge combines arrays", $merged['a'] === 1 && $merged['e'] === 4);
test("Merge recursively merges nested arrays", $merged['b']['c'] === 2 && $merged['b']['d'] === 3);

// Clone Tests
test_group("Clone Tests");

$original = ['a' => ['b' => 'c']];
$clone = JsonUtils::clone($original);
test("Clone creates equal copy", JsonUtils::equals($original, $clone));
$clone['a']['b'] = 'modified';
test("Clone is independent of original", $original['a']['b'] === 'c');

// Keys/Values Tests
test_group("Keys/Values Tests");

$data = ['a' => 1, 'b' => 2, 'c' => 3];
$keys = JsonUtils::keys($data);
test("Keys returns all keys", count($keys) === 3 && in_array('a', $keys));

$values = JsonUtils::values($data);
test("Values returns all values", count($values) === 3 && in_array(2, $values));

// Flatten/Unflatten Tests
test_group("Flatten/Unflatten Tests");

$nested = ['a' => ['b' => ['c' => 'value']]];
$flat = JsonUtils::flatten($nested);
test("Flatten creates dot notation keys", isset($flat['a.b.c']));
test("Flatten preserves values", $flat['a.b.c'] === 'value');

$unflattened = JsonUtils::unflatten($flat);
test("Unflatten restores structure", $unflattened['a']['b']['c'] === 'value');

// Type-safe Getters Tests
test_group("Type-safe Getters Tests");

$data = [
    'str' => 'hello',
    'int' => '42',
    'float' => '3.14',
    'bool' => 'true',
    'arr' => [1, 2, 3]
];

test("GetString returns string", JsonUtils::getString($data, 'str') === 'hello');
test("GetInt returns integer", JsonUtils::getInt($data, 'int') === 42);
test("GetFloat returns float", JsonUtils::getFloat($data, 'float') === 3.14);
test("GetBool returns boolean", JsonUtils::getBool($data, 'bool') === true);
test("GetArray returns array", is_array(JsonUtils::getArray($data, 'arr')));

// Default values
test("GetString with default", JsonUtils::getString($data, 'missing', 'default') === 'default');
test("GetInt with default", JsonUtils::getInt($data, 'missing', 100) === 100);

// Equals Tests
test_group("Equals Tests");

$a = ['name' => 'John', 'age' => 30];
$b = ['age' => 30, 'name' => 'John'];
$c = ['name' => 'Jane', 'age' => 30];

test("Equals returns true for equal objects", JsonUtils::equals($a, $b));
test("Equals returns false for different objects", !JsonUtils::equals($a, $c));

// Complex JSON Tests
test_group("Complex JSON Tests");

$complex = [
    'users' => [
        ['id' => 1, 'name' => 'Alice', 'active' => true],
        ['id' => 2, 'name' => 'Bob', 'active' => false],
        ['id' => 3, 'name' => 'Charlie', 'active' => true]
    ],
    'meta' => [
        'total' => 3,
        'page' => 1
    ]
];

test("Complex nested access", JsonUtils::get($complex, 'users.0.name') === 'Alice');
test("Complex array access", JsonUtils::get($complex, 'users.1.id') === 2);

$json = JsonUtils::stringify($complex);
$parsed = JsonUtils::parse($json);
test("Round-trip stringify/parse preserves data", 
    $parsed['users'][0]['name'] === 'Alice' && 
    $parsed['meta']['total'] === 3
);

// Edge Cases
test_group("Edge Cases");

test("Empty array stringify", JsonUtils::stringify([]) === '[]');
test("Empty object stringify", JsonUtils::stringify(new \stdClass()) === '{}');
test("Null value", JsonUtils::parse('null') === null);
test("Boolean true", JsonUtils::parse('true') === true);
test("Boolean false", JsonUtils::parse('false') === false);
test("Number zero", JsonUtils::parse('0') === 0);
test("Empty string value", JsonUtils::parse('""') === '');

// Unicode Tests
test_group("Unicode Tests");

$unicode = ['name' => '你好世界', 'emoji' => '🎉'];
$json = JsonUtils::stringify($unicode);
$parsed = JsonUtils::parse($json);
test("Unicode preserved in stringify/parse", $parsed['name'] === '你好世界' && $parsed['emoji'] === '🎉');

// Special Characters Tests
test_group("Special Characters Tests");

$special = ['path' => '/usr/local/bin', 'url' => 'https://example.com/path?query=value'];
$json = JsonUtils::stringify($special);
$parsed = JsonUtils::parse($json);
test("Special characters preserved", 
    $parsed['path'] === '/usr/local/bin' && 
    strpos($parsed['url'], 'https://') === 0
);

// Summary
echo "\n=======================================\n";
echo "Test Summary\n";
echo "=======================================\n";
echo "Passed: $passed\n";
echo "Failed: $failed\n";
echo "Total: " . ($passed + $failed) . "\n";

if ($failed === 0) {
    echo "\n✓ All tests passed!\n";
    exit(0);
} else {
    echo "\n✗ Some tests failed!\n";
    exit(1);
}
