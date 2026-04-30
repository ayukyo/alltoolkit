<?php
/**
 * Slug Utils Examples
 * 
 * Demonstrates the usage of SlugGenerator and SlugHelper classes.
 * 
 * Run with: php examples.php
 * 
 * @package SlugUtils\Examples
 */

require_once __DIR__ . '/slug_utils.php';

use SlugUtils\SlugGenerator;
use SlugUtils\SlugHelper;

echo "=====================================\n";
echo "  Slug Utils - Usage Examples\n";
echo "=====================================\n\n";

// ============================================================================
// Example 1: Basic Slug Generation
// ============================================================================
echo "1. Basic Slug Generation\n";
echo str_repeat("-", 40) . "\n";

$generator = new SlugGenerator();

$examples = [
    'Hello World',
    'This is a Test Title!',
    'My Blog Post 2024',
    'PHP & MySQL Tutorial',
    '   Extra   Spaces   Everywhere   ',
    'Special @#$% Characters!!!',
    'CamelCaseString',
    'kebab-case-string',
    'snake_case_string',
];

foreach ($examples as $example) {
    echo "  Input:  '$example'\n";
    echo "  Output: '{$generator->generate($example)}'\n\n";
}

// ============================================================================
// Example 2: Custom Separators
// ============================================================================
echo "2. Custom Separators\n";
echo str_repeat("-", 40) . "\n";

$underscore = new SlugGenerator(['separator' => '_']);
$dot = new SlugGenerator(['separator' => '.']);

$text = 'Hello Beautiful World';
echo "  Input:    '$text'\n";
echo "  Dash:     '{$generator->generate($text)}'\n";
echo "  Underscore: '{$underscore->generate($text)}'\n";
echo "  Dot:      '{$dot->generate($text)}'\n\n";

// ============================================================================
// Example 3: Length Limitation
// ============================================================================
echo "3. Length Limitation\n";
echo str_repeat("-", 40) . "\n";

$short = new SlugGenerator(['max_length' => 30]);
$longText = 'This is a very long blog post title that should be truncated for URL usage';

echo "  Input:   '$longText'\n";
echo "  Full:    '{$generator->generate($longText)}'\n";
echo "  Limited: '{$short->generate($longText)}'\n\n";

// ============================================================================
// Example 4: Unique Slug Generation
// ============================================================================
echo "4. Unique Slug Generation\n";
echo str_repeat("-", 40) . "\n";

$existingSlugs = [
    'my-first-post',
    'my-first-post-1',
    'my-first-post-2',
    'another-article',
];

echo "  Existing slugs: " . implode(', ', $existingSlugs) . "\n\n";

$newSlugs = [
    'My First Post',
    'Another Article',
    'Brand New Content',
];

foreach ($newSlugs as $slug) {
    $unique = $generator->generateUnique($slug, $existingSlugs);
    echo "  '$slug' → '$unique'\n";
    $existingSlugs[] = $unique;
}

echo "\n";

// ============================================================================
// Example 5: International Support
// ============================================================================
echo "5. International Character Support\n";
echo str_repeat("-", 40) . "\n";

$international = [
    'Café au Lait',
    'München ist schön',
    'El niño español',
    'São Paulo, Brasil',
    'Привет мир',
    'Γειά σου κόσμε',
    '東京の天気',
    '你好世界',
];

foreach ($international as $text) {
    echo "  '$text' → '{$generator->generate($text)}'\n";
}

echo "\n";

// ============================================================================
// Example 6: Slug Validation
// ============================================================================
echo "6. Slug Validation\n";
echo str_repeat("-", 40) . "\n";

$testSlugs = [
    'valid-slug',
    'another-valid-slug-123',
    'Invalid Slug',
    'invalid_slug',
    '',
    '123-abc',
];

foreach ($testSlugs as $slug) {
    $isValid = $generator->isValid($slug) ? '✓ Valid' : '✗ Invalid';
    echo "  '$slug' → $isValid\n";
}

echo "\n";

// ============================================================================
// Example 7: Slug Sanitization
// ============================================================================
echo "7. Slug Sanitization\n";
echo str_repeat("-", 40) . "\n";

$dirtySlugs = [
    '--leading-dashes',
    'trailing-dashes--',
    'multiple---dashes',
    'UPPERCASE',
    '  spaces-around  ',
];

foreach ($dirtySlugs as $slug) {
    $clean = $generator->sanitize($slug);
    echo "  '$slug' → '$clean'\n";
}

echo "\n";

// ============================================================================
// Example 8: Slug Conversion Methods
// ============================================================================
echo "8. Slug Conversion Methods\n";
echo str_repeat("-", 40) . "\n";

$testSlug = 'hello-world-example';

echo "  Original:     '$testSlug'\n";
echo "  To Title:    '{$generator->toTitle($testSlug)}'\n";
echo "  To camelCase: '{$generator->toCamelCase($testSlug)}'\n";
echo "  To snake_case: '{$generator->toSnakeCase($testSlug)}'\n";
echo "  Parse:       " . json_encode($generator->parse($testSlug)) . "\n\n";

// ============================================================================
// Example 9: Similarity Comparison
// ============================================================================
echo "9. Slug Similarity Comparison\n";
echo str_repeat("-", 40) . "\n";

$pairs = [
    ['hello-world', 'hello-world'],
    ['hello-world', 'hello-world-2'],
    ['my-blog-post', 'my-blog-article'],
    ['product-review', 'review-product'],
    ['test-123', 'completely-different'],
];

foreach ($pairs as $pair) {
    $similarity = $generator->similarity($pair[0], $pair[1]);
    echo "  '{$pair[0]}' vs '{$pair[1]}'\n";
    echo "    Similarity: " . round($similarity * 100, 1) . "%\n";
}

echo "\n";

// ============================================================================
// Example 10: Helper Functions
// ============================================================================
echo "10. Quick Helper Functions\n";
echo str_repeat("-", 40) . "\n";

echo "  SlugHelper::slug('Hello World!'):\n";
echo "    → '" . SlugHelper::slug('Hello World!') . "'\n\n";

echo "  SlugHelper::underscore('My Variable Name'):\n";
echo "    → '" . SlugHelper::underscore('My Variable Name') . "'\n\n";

echo "  SlugHelper::filename('My Document!!!', 'pdf'):\n";
echo "    → '" . SlugHelper::filename('My Document!!!', 'pdf') . "'\n\n";

echo "  SlugHelper::titleSlug('A Very Long Blog Post Title That Should Be Truncated'):\n";
echo "    → '" . SlugHelper::titleSlug('A Very Long Blog Post Title That Should Be Truncated') . "'\n\n";

echo "  SlugHelper::productSlug('Amazing Gadget 3000!', 'SKU-123'):\n";
echo "    → '" . SlugHelper::productSlug('Amazing Gadget 3000!', 'SKU-123') . "'\n\n";

echo "  SlugHelper::usernameSlug('John Doe'):\n";
echo "    → '" . SlugHelper::usernameSlug('John Doe') . "'\n\n";

echo "  SlugHelper::usernameSlug('Admin') (reserved word):\n";
echo "    → '" . SlugHelper::usernameSlug('Admin') . "'\n\n";

echo "  SlugHelper::id('user'):\n";
echo "    → '" . SlugHelper::id('user') . "'\n\n";

// ============================================================================
// Example 11: Real-World Use Cases
// ============================================================================
echo "11. Real-World Use Cases\n";
echo str_repeat("-", 40) . "\n";

// Blog post URL generation
echo "  Blog Post URL:\n";
$title = '10 Tips for Writing Clean PHP Code in 2024!';
$blogSlug = SlugHelper::titleSlug($title);
echo "    Title: '$title'\n";
echo "    URL:   '/blog/{$blogSlug}'\n\n";

// Product URL generation
echo "  E-commerce Product URL:\n";
$productName = 'Wireless Bluetooth Earbuds Pro - Noise Cancelling';
$sku = 'WBE-PRO-2024';
$productSlug = SlugHelper::productSlug($productName, $sku);
echo "    Product: '$productName'\n";
echo "    SKU:     '$sku'\n";
echo "    URL:     '/products/{$productSlug}'\n\n";

// User profile URL
echo "  User Profile URL:\n";
$fullName = 'John P. MacGyver Jr.';
$username = SlugHelper::usernameSlug($fullName);
echo "    Name:     '$fullName'\n";
echo "    Username: '$username'\n";
echo "    URL:      '/profile/{$username}'\n\n";

// File naming
echo "  Safe Filename Generation:\n";
$documentTitle = 'Project Proposal: Q4 2024 Budget.pdf';
$filename = SlugHelper::filename($documentTitle, 'pdf');
echo "    Original: '$documentTitle'\n";
echo "    Safe:     '$filename'\n\n";

// Unique slug with existing check
echo "  Unique Slug with Database Check:\n";
$title = 'Breaking News';
$existingInDb = ['breaking-news', 'breaking-news-1', 'breaking-news-2'];
$uniqueSlug = $generator->generateUnique($title, $existingInDb);
echo "    Title:    '$title'\n";
echo "    Existing: " . implode(', ', $existingInDb) . "\n";
echo "    New:      '$uniqueSlug'\n\n";

// Timestamp-based slug
echo "  Timestamp-based Slug:\n";
$event = 'Annual Conference 2024';
$timestampSlug = $generator->generateWithTimestamp($event);
echo "    Event: '$event'\n";
echo "    Slug:  '$timestampSlug'\n\n";

// Random suffix slug
echo "  Random Suffix Slug (for unique IDs):\n";
$baseTitle = 'Draft Document';
$randomSlug = $generator->generateWithRandomSuffix($baseTitle, 6);
echo "    Title: '$baseTitle'\n";
echo "    Slug:  '$randomSlug'\n\n";

echo "=====================================\n";
echo "  Examples Complete!\n";
echo "=====================================\n";