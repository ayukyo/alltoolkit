<?php
/**
 * Tests for SlugUtils
 * 
 * Run with: php slug_utils_test.php
 * 
 * @package SlugUtils\Tests
 */

require_once __DIR__ . '/slug_utils.php';

use SlugUtils\SlugGenerator;
use SlugUtils\SlugHelper;

class SlugUtilsTest
{
    private int $passed = 0;
    private int $failed = 0;
    private array $errors = [];
    
    /**
     * Assert that two values are equal
     */
    private function assertEquals($expected, $actual, string $message = ''): void
    {
        if ($expected === $actual) {
            $this->passed++;
        } else {
            $this->failed++;
            $this->errors[] = "FAILED: $message\n  Expected: '$expected'\n  Actual: '$actual'";
        }
    }
    
    /**
     * Assert that a condition is true
     */
    private function assertTrue(bool $condition, string $message = ''): void
    {
        if ($condition) {
            $this->passed++;
        } else {
            $this->failed++;
            $this->errors[] = "FAILED: $message (expected true, got false)";
        }
    }
    
    /**
     * Run all tests
     */
    public function run(): void
    {
        echo "===================================\n";
        echo "  SlugUtils Test Suite\n";
        echo "===================================\n\n";
        
        $this->testBasicSlugGeneration();
        $this->testTransliteration();
        $this->testCustomSeparator();
        $this->testMaxLength();
        $this->testUniqueSlugGeneration();
        $this->testSlugValidation();
        $this->testSlugSanitization();
        $this->testSlugConversion();
        $this->testHelperFunctions();
        $this->testEdgeCases();
        $this->testInternationalCharacters();
        
        $this->printResults();
    }
    
    /**
     * Test basic slug generation
     */
    private function testBasicSlugGeneration(): void
    {
        echo "Testing basic slug generation...\n";
        
        $generator = new SlugGenerator();
        
        $this->assertEquals(
            'hello-world',
            $generator->generate('Hello World'),
            'Simple space to dash'
        );
        
        $this->assertEquals(
            'this-is-a-test',
            $generator->generate('This is a test'),
            'Multiple spaces'
        );
        
        $this->assertEquals(
            'hello-world',
            $generator->generate('Hello World!!!'),
            'Remove special characters'
        );
        
        $this->assertEquals(
            'hello-world',
            $generator->generate('  Hello  World  '),
            'Trim spaces'
        );
        
        $this->assertEquals(
            'test-123',
            $generator->generate('Test 123'),
            'Preserve numbers'
        );
        
        $this->assertEquals(
            'test-123-abc',
            $generator->generate('Test 123 ABC'),
            'Mix of letters and numbers'
        );
        
        echo "  Basic tests completed\n\n";
    }
    
    /**
     * Test transliteration
     */
    private function testTransliteration(): void
    {
        echo "Testing transliteration...\n";
        
        $generator = new SlugGenerator();
        
        // French
        $this->assertEquals(
            'cafe-francais',
            $generator->generate('Café Français'),
            'French accents'
        );
        
        // German
        $this->assertEquals(
            'gruße-aus-deutschland',
            $generator->generate('Grüße aus Deutschland'),
            'German umlauts'
        );
        
        // Spanish
        $this->assertEquals(
            'nino-espanol',
            $generator->generate('Niño Español'),
            'Spanish tilde'
        );
        
        // Portuguese
        $this->assertEquals(
            'coracao-do-brasil',
            $generator->generate('Coração do Brasil'),
            'Portuguese accents'
        );
        
        echo "  Transliteration tests completed\n\n";
    }
    
    /**
     * Test custom separator
     */
    private function testCustomSeparator(): void
    {
        echo "Testing custom separator...\n";
        
        $generator = new SlugGenerator(['separator' => '_']);
        
        $this->assertEquals(
            'hello_world',
            $generator->generate('Hello World'),
            'Underscore separator'
        );
        
        $this->assertEquals(
            'this_is_a_test',
            $generator->generate('This is a test'),
            'Multiple words with underscore'
        );
        
        $generator2 = new SlugGenerator(['separator' => '.']);
        $this->assertEquals(
            'hello.world',
            $generator2->generate('Hello World'),
            'Dot separator'
        );
        
        echo "  Custom separator tests completed\n\n";
    }
    
    /**
     * Test max length
     */
    private function testMaxLength(): void
    {
        echo "Testing max length...\n";
        
        $generator = new SlugGenerator(['max_length' => 20]);
        
        $this->assertEquals(
            'this-is-a-very',
            $generator->generate('This is a very long string that should be truncated'),
            'Truncate to max length'
        );
        
        $this->assertEquals(
            'short-string',
            $generator->generate('Short String'),
            'Keep short strings'
        );
        
        echo "  Max length tests completed\n\n";
    }
    
    /**
     * Test unique slug generation
     */
    private function testUniqueSlugGeneration(): void
    {
        echo "Testing unique slug generation...\n";
        
        $generator = new SlugGenerator();
        $existing = ['hello-world', 'hello-world-1', 'hello-world-2'];
        
        $this->assertEquals(
            'hello-world',
            $generator->generateUnique('Hello World', []),
            'First occurrence'
        );
        
        $this->assertEquals(
            'hello-world-3',
            $generator->generateUnique('Hello World', $existing),
            'Skip existing slugs'
        );
        
        $this->assertEquals(
            'new-slug',
            $generator->generateUnique('New Slug', $existing),
            'New unique slug'
        );
        
        echo "  Unique slug tests completed\n\n";
    }
    
    /**
     * Test slug validation
     */
    private function testSlugValidation(): void
    {
        echo "Testing slug validation...\n";
        
        $generator = new SlugGenerator();
        
        $this->assertTrue(
            $generator->isValid('hello-world'),
            'Valid slug with dash'
        );
        
        $this->assertTrue(
            $generator->isValid('test123'),
            'Valid alphanumeric slug'
        );
        
        $this->assertTrue(
            $generator->isValid('a-b-c-d'),
            'Valid multi-part slug'
        );
        
        $this->assertTrue(
            !$generator->isValid(''),
            'Empty slug is invalid'
        );
        
        $this->assertTrue(
            !$generator->isValid('Hello World'),
            'Slug with spaces is invalid'
        );
        
        $this->assertTrue(
            !$generator->isValid('hello_world'),
            'Slug with underscore is invalid (wrong separator)'
        );
        
        echo "  Validation tests completed\n\n";
    }
    
    /**
     * Test slug sanitization
     */
    private function testSlugSanitization(): void
    {
        echo "Testing slug sanitization...\n";
        
        $generator = new SlugGenerator();
        
        $this->assertEquals(
            'hello-world',
            $generator->sanitize('--hello--world--'),
            'Remove extra dashes'
        );
        
        $this->assertEquals(
            'hello-world',
            $generator->sanitize('hello---world'),
            'Replace multiple dashes'
        );
        
        $this->assertEquals(
            'test',
            $generator->sanitize('TEST'),
            'Convert to lowercase'
        );
        
        echo "  Sanitization tests completed\n\n";
    }
    
    /**
     * Test slug conversion methods
     */
    private function testSlugConversion(): void
    {
        echo "Testing slug conversion methods...\n";
        
        $generator = new SlugGenerator();
        
        $this->assertEquals(
            'Hello World',
            $generator->toTitle('hello-world'),
            'Convert to title'
        );
        
        $this->assertEquals(
            'helloWorld',
            $generator->toCamelCase('hello-world'),
            'Convert to camelCase'
        );
        
        $this->assertEquals(
            'hello_world',
            $generator->toSnakeCase('hello-world'),
            'Convert to snake_case'
        );
        
        $this->assertEquals(
            ['hello', 'world'],
            $generator->parse('hello-world'),
            'Parse slug into words'
        );
        
        echo "  Conversion tests completed\n\n";
    }
    
    /**
     * Test helper functions
     */
    private function testHelperFunctions(): void
    {
        echo "Testing helper functions...\n";
        
        $this->assertEquals(
            'quick-slug-test',
            SlugHelper::slug('Quick Slug Test!'),
            'SlugHelper::slug()'
        );
        
        $this->assertEquals(
            'quick_slug_test',
            SlugHelper::underscore('Quick Slug Test!'),
            'SlugHelper::underscore()'
        );
        
        $this->assertEquals(
            'my-file.txt',
            SlugHelper::filename('My File!!!', 'txt'),
            'SlugHelper::filename()'
        );
        
        $this->assertEquals(
            'this-is-a-blog-post-title',
            SlugHelper::titleSlug('This is a Blog Post Title That is Too Long for SEO'),
            'SlugHelper::titleSlug() with max length'
        );
        
        $this->assertEquals(
            'awesome-product-sku123',
            SlugHelper::productSlug('Awesome Product!!!', 'SKU123'),
            'SlugHelper::productSlug()'
        );
        
        $username = SlugHelper::usernameSlug('Admin');
        $this->assertTrue(
            $username !== 'admin',
            'SlugHelper::usernameSlug() avoids reserved words'
        );
        
        $id = SlugHelper::id('user');
        $this->assertTrue(
            strpos($id, 'user-') === 0,
            'SlugHelper::id() with prefix'
        );
        
        echo "  Helper function tests completed\n\n";
    }
    
    /**
     * Test edge cases
     */
    private function testEdgeCases(): void
    {
        echo "Testing edge cases...\n";
        
        $generator = new SlugGenerator();
        
        $this->assertEquals(
            '',
            $generator->generate('!!!'),
            'Only special characters'
        );
        
        $this->assertEquals(
            '123',
            $generator->generate('123'),
            'Only numbers'
        );
        
        $this->assertEquals(
            'a-b-c',
            $generator->generate('a"b"c'),
            'Quotes as separators'
        );
        
        $this->assertEquals(
            'test-2024',
            $generator->generate('test-2024'),
            'Already has dashes'
        );
        
        $this->assertEquals(
            'test',
            $generator->generate('test    test'),
            'Multiple spaces become single dash'
        );
        
        echo "  Edge case tests completed\n\n";
    }
    
    /**
     * Test international characters
     */
    private function testInternationalCharacters(): void
    {
        echo "Testing international characters...\n";
        
        $generator = new SlugGenerator();
        
        // Cyrillic (Russian)
        $this->assertEquals(
            'privet-mir',
            $generator->generate('Привет мир'),
            'Russian Cyrillic'
        );
        
        // Greek
        $this->assertEquals(
            'geia-sou-kosme',
            $generator->generate('Γειά σου κόσμε'),
            'Greek'
        );
        
        // Japanese (basic)
        $slug = $generator->generate('こんにちは');
        $this->assertTrue(
            !empty($slug),
            'Japanese Hiragana transliterates'
        );
        
        // Chinese
        $slug = $generator->generate('你好世界');
        $this->assertTrue(
            !empty($slug),
            'Chinese characters transliterate'
        );
        
        // Arabic
        $slug = $generator->generate('مرحبا');
        $this->assertTrue(
            !empty($slug),
            'Arabic characters transliterate'
        );
        
        echo "  International character tests completed\n\n";
    }
    
    /**
     * Print test results
     */
    private function printResults(): void
    {
        echo "===================================\n";
        echo "  Test Results\n";
        echo "===================================\n";
        echo "  Passed: {$this->passed}\n";
        echo "  Failed: {$this->failed}\n";
        echo "  Total:  " . ($this->passed + $this->failed) . "\n";
        
        if ($this->failed > 0) {
            echo "\n  Errors:\n";
            foreach ($this->errors as $error) {
                echo "  - $error\n";
            }
        }
        
        echo "===================================\n";
        
        if ($this->failed === 0) {
            echo "\n✅ All tests passed!\n";
        } else {
            echo "\n❌ Some tests failed.\n";
        }
    }
}

// Run tests
$test = new SlugUtilsTest();
$test->run();