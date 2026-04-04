<?php
/**
 * AllToolkit - JSON Utilities Example
 *
 * Demonstrates various use cases for JsonUtils
 *
 * @author AllToolkit Contributors
 * @license MIT
 */

require_once __DIR__ . '/../json_utils/mod.php';

use AllToolkit\JsonUtils;

echo "AllToolkit - JSON Utilities Examples\n";
echo "====================================\n\n";

// Example 1: Basic parsing and stringification
echo "1. Basic Parsing and Stringification\n";
echo "------------------------------------\n";

$jsonString = '{"name":"John","age":30,"city":"New York"}';
$data = JsonUtils::parse($jsonString);

echo "Input JSON: $jsonString\n";
echo "Parsed name: " . $data['name'] . "\n";
echo "Parsed age: " . $data['age'] . "\n\n";

// Convert back to JSON
$backToJson = JsonUtils::stringify($data);
echo "Stringified: $backToJson\n\n";

// Example 2: Pretty printing
echo "2. Pretty Printing\n";
echo "------------------\n";

$minified = '{"users":[{"name":"Alice"},{"name":"Bob"}]}';
$pretty = JsonUtils::prettyPrint($minified);
echo "Minified:\n$minified\n\n";
echo "Pretty printed:\n$pretty\n\n";

// Example 3: Nested data access with dot notation
echo "3. Nested Data Access (Dot Notation)\n";
echo "------------------------------------\n";

$nestedData = [
    'company' => [
        'name' => 'Acme Corp',
        'address' => [
            'street' => '123 Main St',
            'city' => 'Boston',
            'zip' => '02101'
        ],
        'employees' => [
            ['name' => 'Alice', 'role' => 'Developer'],
            ['name' => 'Bob', 'role' => 'Designer']
        ]
    ]
];

echo "Company name: " . JsonUtils::get($nestedData, 'company.name') . "\n";
echo "City: " . JsonUtils::get($nestedData, 'company.address.city') . "\n";
echo "First employee: " . JsonUtils::get($nestedData, 'company.employees.0.name') . "\n";
echo "Missing path with default: " . JsonUtils::get($nestedData, 'company.phone', 'N/A') . "\n\n";

// Example 4: Setting nested values
echo "4. Setting Nested Values\n";
echo "------------------------\n";

$config = [];
JsonUtils::set($config, 'database.host', 'localhost');
JsonUtils::set($config, 'database.port', 3306);
JsonUtils::set($config, 'database.credentials.username', 'admin');
JsonUtils::set($config, 'database.credentials.password', 'secret');

echo "Config after setting values:\n";
echo JsonUtils::stringify($config, true) . "\n\n";

// Example 5: Checking if path exists
echo "5. Checking Path Existence\n";
echo "--------------------------\n";

$hasHost = JsonUtils::has($config, 'database.host');
$hasSsl = JsonUtils::has($config, 'database.ssl');

echo "Has database.host: " . ($hasHost ? 'Yes' : 'No') . "\n";
echo "Has database.ssl: " . ($hasSsl ? 'Yes' : 'No') . "\n\n";

// Example 6: Merging JSON data
echo "6. Merging JSON Data\n";
echo "--------------------\n";

$defaults = [
    'theme' => 'light',
    'language' => 'en',
    'notifications' => [
        'email' => true,
        'push' => false
    ]
];

$userSettings = [
    'theme' => 'dark',
    'notifications' => [
        'push' => true
    ]
];

$merged = JsonUtils::merge($defaults, $userSettings);
echo "Merged settings:\n";
echo JsonUtils::stringify($merged, true) . "\n\n";

// Example 7: Flatten and unflatten
echo "7. Flatten and Unflatten\n";
echo "------------------------\n";

$nested = [
    'user' => [
        'profile' => [
            'name' => 'John',
            'settings' => [
                'theme' => 'dark',
                'notifications' => true
            ]
        ]
    ]
];

$flat = JsonUtils::flatten($nested);
echo "Flattened:\n";
print_r($flat);

$unflattened = JsonUtils::unflatten($flat);
echo "\nUnflattened:\n";
echo JsonUtils::stringify($unflattened, true) . "\n\n";

// Example 8: Type-safe getters
echo "8. Type-safe Getters\n";
echo "--------------------\n";

$apiResponse = [
    'status' => 'success',
    'code' => '200',
    'data' => [
        'count' => '42',
        'average' => '85.5',
        'items' => ['a', 'b', 'c']
    ]
];

echo "Status (string): " . JsonUtils::getString($apiResponse, 'status') . "\n";
echo "Code (int): " . JsonUtils::getInt($apiResponse, 'code') . "\n";
echo "Count (int): " . JsonUtils::getInt($apiResponse, 'data.count') . "\n";
echo "Average (float): " . JsonUtils::getFloat($apiResponse, 'data.average') . "\n";
echo "Items count: " . count(JsonUtils::getArray($apiResponse, 'data.items')) . "\n\n";

// Example 9: Validation
echo "9. JSON Validation\n";
echo "------------------\n";

$validJson = '{"name":"test","value":123}';
$invalidJson = '{"name":"test",}';

echo "Is valid JSON: " . (JsonUtils::isValid($validJson) ? 'Yes' : 'No') . "\n";
echo "Is invalid JSON: " . (JsonUtils::isValid($invalidJson) ? 'Yes' : 'No') . "\n";

$error = JsonUtils::getError($invalidJson);
echo "Error message: $error\n\n";

// Example 10: Working with arrays
echo "10. Working with Arrays\n";
echo "-----------------------\n";

$users = [
    ['id' => 1, 'name' => 'Alice', 'active' => true],
    ['id' => 2, 'name' => 'Bob', 'active' => false],
    ['id' => 3, 'name' => 'Charlie', 'active' => true]
];

$keys = JsonUtils::keys($users[0]);
echo "User object keys: " . implode(', ', $keys) . "\n";

$names = array_map(function($user) {
    return $user['name'];
}, $users);
echo "All names: " . implode(', ', $names) . "\n\n";

// Example 11: Minification
echo "11. Minification\n";
echo "----------------\n";

$prettyJson = JsonUtils::stringify(['a' => 1, 'b' => 2], true);
echo "Pretty:\n$prettyJson\n";

$minified = JsonUtils::minify($prettyJson);
echo "\nMinified: $minified\n\n";

// Example 12: Cloning
echo "12. Deep Cloning\n";
echo "----------------\n";

$original = [
    'user' => [
        'name' => 'John',
        'preferences' => ['theme' => 'dark']
    ]
];

$clone = JsonUtils::clone($original);
$clone['user']['name'] = 'Jane';
$clone['user']['preferences']['theme'] = 'light';

echo "Original name: " . $original['user']['name'] . "\n";
echo "Clone name: " . $clone['user']['name'] . "\n";
echo "Original theme: " . $original['user']['preferences']['theme'] . "\n";
echo "Clone theme: " . $clone['user']['preferences']['theme'] . "\n\n";

// Example 13: Comparing JSON
echo "13. Comparing JSON\n";
echo "------------------\n";

$obj1 = ['a' => 1, 'b' => ['c' => 2]];
$obj2 = ['b' => ['c' => 2], 'a' => 1];
$obj3 = ['a' => 1, 'b' => ['c' => 3]];

echo "obj1 equals obj2: " . (JsonUtils::equals($obj1, $obj2) ? 'Yes' : 'No') . "\n";
echo "obj1 equals obj3: " . (JsonUtils::equals($obj1, $obj3) ? 'Yes' : 'No') . "\n\n";

echo "====================================\n";
echo "Examples completed!\n";
