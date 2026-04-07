<?php
/**
 * UUID Utils Test Suite
 *
 * Comprehensive test coverage for UUID generation, validation, and manipulation.
 */

require_once __DIR__ . '/mod.php';

use AllToolkit\UUIDUtils;

class UUIDUtilsTest {
    private $passed = 0;
    private $failed = 0;

    public function run(): void {
        echo "========================================\n";
        echo "UUID Utils Test Suite\n";
        echo "========================================\n\n";

        $this->testUUID4Generation();
        $this->testUUID1Generation();
        $this->testUUID3Generation();
        $this->testUUID5Generation();
        $this->testUUID7Generation();
        $this->testValidation();
        $this->testFormatConversion();
        $this->testMultipleGeneration();
        $this->testEquality();
        $this->testInfo();
        $this->testShortId();
        $this->testULID();

        $this->printSummary();
    }

    private function testUUID4Generation(): void {
        echo "Testing UUID v4 Generation...\n";

        $uuid = UUIDUtils::uuid4();
        $this->assertTrue(UUIDUtils::isValid($uuid), 'Generated UUID v4 should be valid');
        $this->assertTrue(UUIDUtils::isValidV4($uuid), 'Generated UUID should be valid v4');
        $this->assertTrue(strlen($uuid) === 36, 'UUID v4 should be 36 characters');

        // Test uniqueness
        $uuids = [];
        for ($i = 0; $i < 100; $i++) {
            $uuids[] = UUIDUtils::uuid4();
        }
        $this->assertTrue(count(array_unique($uuids)) === 100, 'Generated UUIDs should be unique');

        // Test compact generation
        $compact = UUIDUtils::uuid4Compact();
        $this->assertTrue(strlen($compact) === 32, 'Compact UUID should be 32 characters');

        echo "  ✓ UUID v4 generation tests passed\n\n";
    }

    private function testUUID1Generation(): void {
        echo "Testing UUID v1 Generation...\n";

        $uuid = UUIDUtils::uuid1();
        $this->assertTrue(UUIDUtils::isValid($uuid), 'Generated UUID v1 should be valid');
        $this->assertTrue(UUIDUtils::isValidV1($uuid), 'Generated UUID should be valid v1');

        $uuid2 = UUIDUtils::uuid1();
        $this->assertTrue($uuid !== $uuid2, 'Consecutive UUID v1 should be different');

        echo "  ✓ UUID v1 generation tests passed\n\n";
    }

    private function testUUID3Generation(): void {
        echo "Testing UUID v3 Generation...\n";

        $uuid1 = UUIDUtils::uuid3(UUIDUtils::NAMESPACE_DNS, 'example.com');
        $uuid2 = UUIDUtils::uuid3(UUIDUtils::NAMESPACE_DNS, 'example.com');
        $this->assertTrue($uuid1 === $uuid2, 'UUID v3 should be deterministic');

        $uuid3 = UUIDUtils::uuid3(UUIDUtils::NAMESPACE_DNS, 'example.org');
        $this->assertTrue($uuid1 !== $uuid3, 'Different names should produce different UUIDs');
        $this->assertTrue(UUIDUtils::isValid($uuid1), 'Generated UUID v3 should be valid');

        echo "  ✓ UUID v3 generation tests passed\n\n";
    }

    private function testUUID5Generation(): void {
        echo "Testing UUID v5 Generation...\n";

        $uuid1 = UUIDUtils::uuid5(UUIDUtils::NAMESPACE_DNS, 'example.com');
        $uuid2 = UUIDUtils::uuid5(UUIDUtils::NAMESPACE_DNS, 'example.com');
        $this->assertTrue($uuid1 === $uuid2, 'UUID v5 should be deterministic');
        $this->assertTrue(UUIDUtils::isValid($uuid1), 'Generated UUID v5 should be valid');

        echo "  ✓ UUID v5 generation tests passed\n\n";
    }

    private function testUUID7Generation(): void {
        echo "Testing UUID v7 Generation...\n";

        $uuid = UUIDUtils::uuid7();
        $this->assertTrue(UUIDUtils::isValid($uuid), 'Generated UUID v7 should be valid');

        // Test ordering
        $uuids = [];
        for ($i = 0; $i < 5; $i++) {
            $uuids[] = UUIDUtils::uuid7();
            usleep(1000);
        }
        $sorted = $uuids;
        sort($sorted);
        $this->assertTrue($uuids === $sorted, 'UUID v7 should be ordered by timestamp');

        echo "  ✓ UUID v7 generation tests passed\n\n";
    }

    private function testValidation(): void {
        echo "Testing Validation...\n";

        $this->assertTrue(UUIDUtils::isValid('550e8400-e29b-41d4-a716-446655440000'), 'Valid UUID should pass');
        $this->assertFalse(UUIDUtils::isValid(''), 'Empty string should be invalid');
        $this->assertFalse(UUIDUtils::isValid('not-a-uuid'), 'Invalid format should fail');
        $this->assertFalse(UUIDUtils::isValid('550e8400e29b41d4a716446655440000'), 'Missing dashes should fail');

        echo "  ✓ Validation tests passed\n\n";
    }

    private function testFormatConversion(): void {
        echo "Testing Format Conversion...\n";

        $uuid = '550e8400-e29b-41d4-a716-446655440000';
        $compact = UUIDUtils::toCompact($uuid);
        $this->assertTrue(strlen($compact) === 32, 'Compact should be 32 chars');

        $back = UUIDUtils::fromCompact($compact);
        $this->assertTrue(strtolower($back) === strtolower($uuid), 'Round-trip conversion should work');

        $upper = UUIDUtils::toUpper($uuid);
        $this->assertTrue($upper === strtoupper($uuid), 'toUpper should work');

        echo "  ✓ Format conversion tests passed\n\n";
    }

    private function testMultipleGeneration(): void {
        echo "Testing Multiple Generation...\n";

        $uuids = UUIDUtils::generateMultiple(5, '4');
        $this->assertTrue(count($uuids) === 5, 'Should generate 5 UUIDs');

        foreach ($uuids as $uuid) {
            $this->assertTrue(UUIDUtils::isValid($uuid), 'All generated UUIDs should be valid');
        }

        echo "  ✓ Multiple generation tests passed\n\n";
    }

    private function testEquality(): void {
        echo "Testing Equality...\n";

        $uuid1 = '550e8400-e29b-41d4-a716-446655440000';
        $uuid2 = '550E8400-E29B-41D4-A716-446655440000';
        $this->assertTrue(UUIDUtils::equals($uuid1, $uuid2), 'Case-insensitive equality should work');

        echo "  ✓ Equality tests passed\n\n";
    }

    private function testInfo(): void {
        echo "Testing Info...\n";

        $uuid = '550e8400-e29b-41d4-a716-446655440000';
        $info = UUIDUtils::getInfo($uuid);
        $this->assertTrue(is_array($info), 'getInfo should return array');
        $this->assertTrue(isset($info['version']), 'Info should have version');

        echo "  ✓ Info tests passed\n\n";
    }

    private function testShortId(): void {
        echo "Testing Short ID...\n";

        $shortId = UUIDUtils::shortId();
        $this->assertTrue(strlen($shortId) === 22, 'Default short ID should be 22 chars');

        $shortId10 = UUIDUtils::shortId(10);
        $this->assertTrue(strlen($shortId10) === 10, 'Custom length short ID should work');

        echo "  ✓ Short ID tests passed\n\n";
    }

    private function testULID(): void {
        echo "Testing ULID...\n";

        $ulid = UUIDUtils::ulid();
        $this->assertTrue(strlen($ulid) === 26, 'ULID should be 26 characters');
        $this->assertTrue(ctype_upper($ulid), 'ULID should be uppercase');

        echo "  ✓ ULID tests passed\n\n";
    }

    private function assertTrue($condition, $message): void {
        if ($condition) {
            $this->passed++;
        } else {
            $this->failed++;
            echo "    ✗ FAILED: $message\n";
        }
    }

    private function printSummary(): void {
        echo "========================================\n";
        echo "Test Summary\n";
        echo "========================================\n";
        echo "Passed: {$this->passed}\n";
        echo "Failed: {$this->failed}\n";
        echo "Total:  " . ($this->passed + $this->failed) . "\n
        if ($this->failed === 0) {
            echo "\n✓ All tests passed!\n";
        } else {
            echo "\n✗ Some tests failed!\n";
            exit(1);
        }
    }
}

// Run tests
$test = new UUIDUtilsTest();
$test->run();
