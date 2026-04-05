<?php
/**
 * AllToolkit - PHP Cache Utilities Test Suite
 *
 * Comprehensive test suite for the Cache utilities module.
 *
 * @package AllToolkit
 * @author AllToolkit Team
 * @license MIT
 */

require_once __DIR__ . '/mod.php';

use AllToolkit\Cache;
use AllToolkit\CacheOptions;
use AllToolkit\CacheEntry;
use AllToolkit\CacheStats;

class CacheUtilsTest {
    private $testCount = 0;
    private $passCount = 0;
    private $failCount = 0;
    private $cacheDir;

    public function __construct() {
        $this->cacheDir = sys_get_temp_dir() . '/alltoolkit_cache_test_' . uniqid();
    }

    public function run(): void {
        echo "Running Cache Utilities Test Suite...\n\n";

        $this->testBasicOperations();
        $this->testTtlOperations();
        $this->testTagOperations();
        $this->testAdvancedOperations();
        $this->testStatistics();
        $this->testEviction();
        $this->testEdgeCases();

        echo "\n";
        echo "========================================\n";
        echo "Test Results:\n";
        echo "  Total:  {$this->testCount}\n";
        echo "  Passed: {$this->passCount}\n";
        echo "  Failed: {$this->failCount}\n";
        echo "========================================\n";

        // Cleanup
        $this->cleanup();

        exit($this->failCount > 0 ? 1 : 0);
    }

    private function cleanup(): void {
        if (is_dir($this->cacheDir)) {
            $files = glob($this->cacheDir . '/*');
            if ($files) {
                foreach ($files as $file) {
                    @unlink($file);
                }
            }
            @rmdir($this->cacheDir);
        }
    }

    private function assert(string $testName, bool $condition, string $message = ''): void {
        $this->testCount++;
        if ($condition) {
            $this->passCount++;
            echo "  [PASS] {$testName}\n";
        } else {
            $this->failCount++;
            echo "  [FAIL] {$testName}";
            if ($message) {
                echo " - {$message}";
            }
            echo "\n";
        }
    }

    private function testBasicOperations(): void {
        echo "Testing Basic Operations:\n";

        $cache = new Cache(['directory' => $this->cacheDir]);

        // Test set and get
        $cache->set('key1', 'value1');
        $this->assert('Set and get string value', $cache->get('key1') === 'value1');

        // Test integer
        $cache->set('int_key', 42);
        $this->assert('Set and get integer', $cache->get('int_key') === 42);

        // Test array
        $cache->set('array_key', ['a', 'b', 'c']);
        $this->assert('Set and get array', $cache->get('array_key') === ['a', 'b', 'c']);

        // Test object
        $obj = new stdClass();
        $obj->name = 'test';
        $cache->set('obj_key', $obj);
        $retrieved = $cache->get('obj_key');
        $this->assert('Set and get object', $retrieved instanceof stdClass && $retrieved->name === 'test');

        // Test has
        $this->assert('Has existing key', $cache->has('key1') === true);
        $this->assert('Has non-existing key', $cache->has('nonexistent') === false);

        // Test delete
        $cache->delete('key1');
        $this->assert('Delete removes key', $cache->has('key1') === false);
        $this->assert('Delete returns null', $cache->get('key1') === null);

        // Test default value
        $this->assert('Default value for missing key', $cache->get('missing', 'default') === 'default');

        // Test flush
        $cache->set('key2', 'value2');
        $cache->flush();
        $this->assert('Flush removes all keys', $cache->has('key2') === false);

        $this->cleanup();
    }

    private function testTtlOperations(): void {
        echo "\nTesting TTL Operations:\n";

        $cache = new Cache(['directory' => $this->cacheDir]);

        // Test immediate expiration
        $cache->set('expired_key', 'value', 0);
        $this->assert('TTL 0 means no expiration', $cache->has('expired_key') === true);

        // Test short TTL
        $cache->set('short_ttl', 'value', 1);
        $this->assert('Key exists before expiration', $cache->has('short_ttl') === true);
        sleep(2);
        $this->assert('Key expires after TTL', $cache->has('short_ttl') === false);

        // Test forever
        $cache->forever('forever_key', 'value');
        $this->assert('Forever key exists', $cache->has('forever_key') === true);
        $entry = $cache->getEntry('forever_key');
        $this->assert('Forever key has no expiration', $entry->expires === 0);

        // Test ttl() method
        $cache->set('ttl_test', 'value', 3600);
        $ttl = $cache->ttl('ttl_test');
        $this->assert('TTL returns positive value', $ttl !== null && $ttl > 0);

        // Test expiresAt
        $expiresAt = $cache->expiresAt('ttl_test');
        $this->assert('ExpiresAt returns timestamp', $expiresAt !== null && $expiresAt > time());

        $this->cleanup();
    }

    private function testTagOperations(): void {
        echo "\nTesting Tag Operations:\n";

        $cache = new Cache(['directory' => $this->cacheDir]);

        // Test set with tags
        $cache->set('tagged1', 'value1', null, ['tag1', 'tag2']);
        $cache->set('tagged2', 'value2', null, ['tag1', 'tag3']);
        $cache->set('tagged3', 'value3', null, ['tag2', 'tag3']);

        // Test getKeysByTag
        $keys1 = $cache->getKeysByTag('tag1');
        $this->assert('Get keys by tag1', count($keys1) === 2 && in_array('tagged1', $keys1) && in_array('tagged2', $keys1));

        // Test getTags
        $tags = $cache->getTags();
        $this->assert('Get all tags', count($tags) === 3);

        // Test flushByTag
        $cache->flushByTag('tag1');
        $this->assert('Flush by tag removes tagged entries', $cache->has('tagged1') === false && $cache->has('tagged2') === false);
        $this->assert('Flush by tag keeps other entries', $cache->has('tagged3') === true);

        // Test flushByTags
        $cache->set('multi1', 'value', null, ['a', 'b']);
        $cache->set('multi2', 'value', null, ['b', 'c']);
        $cache->set('multi3', 'value', null, ['c', 'd']);
        $cache->flushByTags(['a', 'c']);
        $this->assert('Flush by multiple tags', $cache->has('multi1') === false && $cache->has('multi2') === false);
        $this->assert('Flush by multiple tags keeps others', $cache->has('multi3') === true);

        $this->cleanup();
    }

    private function testAdvancedOperations(): void {
        echo "\nTesting Advanced Operations:\n";

        $cache = new Cache(['directory' => $this->cacheDir]);

        // Test increment
        $cache->set('counter', 10);
        $result = $cache->increment('counter', 5);
        $this->assert('Increment returns new value', $result === 15);
        $this->assert('Increment stores new value', $cache->get('counter') === 15);

        // Test decrement
        $result = $cache->decrement('counter', 3);
        $this->assert('Decrement returns new value', $result === 12);

        // Test increment on non-existent key
        $result = $cache->increment('new_counter', 1);
        $this->assert('Increment on new key starts from 0', $result === 1);

        // Test getOrSet
        $callCount = 0;
        $value = $cache->getOrSet('computed', function() use (&$callCount) {
            $callCount++;
            return 'computed_value';
        });
        $this->assert('getOrSet returns computed value', $value === 'computed_value');
        $this->assert('getOrSet stores value', $cache->get('computed') === 'computed_value');

        // Second call should not execute callback
        $cache->getOrSet('computed', function() use (&$callCount)