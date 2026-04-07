<?php
/**
 * UUID Utilities Module for PHP
 *
 * A comprehensive UUID (Universally Unique Identifier) generation and manipulation
 * utility with zero dependencies. Supports UUID v1, v3, v4, v5, v7 generation, validation,
 * and format conversion.
 *
 * @package AllToolkit\UUIDUtils
 * @author AllToolkit Contributors
 * @license MIT
 */

namespace AllToolkit;

/**
 * UUID Utilities class
 *
 * Provides comprehensive UUID generation, validation, and manipulation functions.
 * All methods are static and stateless for thread-safe usage.
 */
class UUIDUtils {

    // Predefined UUID namespaces for v3/v5 generation
    public const NAMESPACE_DNS = '6ba7b810-9dad-11d1-80b4-00c04fd430c8';
    public const NAMESPACE_URL = '6ba7b811-9dad-11d1-80b4-00c04fd430c8';
    public const NAMESPACE_OID = '6ba7b812-9dad-11d1-80b4-00c04fd430c8';
    public const NAMESPACE_X500 = '6ba7b814-9dad-11d1-80b4-00c04fd430c8';

    /**
     * Generate a UUID version 4 (random)
     *
     * Generates a cryptographically secure random UUID v4.
     *
     * @return string UUID v4 string in standard format (xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx)
     * @throws \Exception If random bytes generation fails
     */
    public static function uuid4(): string {
        // Generate 16 random bytes
        $data = random_bytes(16);

        // Set version (4) in bits 12-15 of time_hi_and_version field
        $data[6] = chr(ord($data[6]) & 0x0f | 0x40);

        // Set variant (10) in bits 6-7 of clock_seq_hi_and_reserved field
        $data[8] = chr(ord($data[8]) & 0x3f | 0x80);

        // Convert to hex and format as UUID
        $hex = bin2hex($data);

        return sprintf(
            '%s-%s-4%s-%s%s-%s',
            substr($hex, 0, 8),
            substr($hex, 8, 4),
            substr($hex, 13, 3),
            substr($hex, 16, 4),
            substr($hex, 20, 12)
        );
    }

    /**
     * Generate a compact UUID v4 (without dashes)
     *
     * @return string Compact UUID v4 string (32 characters)
     * @throws \Exception If random bytes generation fails
     */
    public static function uuid4Compact(): string {
        return str_replace('-', '', self::uuid4());
    }

    /**
     * Generate a UUID version 1 (timestamp-based)
     *
     * Generates a UUID v1 based on current timestamp and node ID.
     * Note: This uses a random node ID for privacy.
     *
     * @return string UUID v1 string in standard format
     * @throws \Exception If random bytes generation fails
     */
    public static function uuid1(): string {
        // Get current timestamp (100-nanosecond intervals since Oct 15, 1582)
        $timestamp = self::getTimestamp100ns();

        // Generate random clock sequence and node
        $clockSeq = random_int(0, 0x3FFF) | 0x8000;
        $node = bin2hex(random_bytes(6));

        // Extract timestamp components
        $timeLow = $timestamp & 0xFFFFFFFF;
        $timeMid = ($timestamp >> 32) & 0xFFFF;
        $timeHi = (($timestamp >> 48) & 0x0FFF) | 0x1000; // Version 1

        return sprintf(
            '%08x-%04x-%04x-%04x-%s',
            $timeLow,
            $timeMid,
            $timeHi,
            $clockSeq,
            $node
        );
    }

    /**
     * Generate a UUID version 3 (MD5-based, name-based)
     *
     * Generates a deterministic UUID v3 based on namespace and name using MD5 hash.
     *
     * @param string $namespace UUID namespace (use NAMESPACE_* constants)
     * @param string $name Name to hash
     * @return string UUID v3 string in standard format
     */
    public static function uuid3(string $namespace, string $name): string {
        $nsBytes = self::uuidToBytes($namespace);
        $hash = md5($nsBytes . $name, true);

        // Set version (3) and variant
        $hash[6] = chr(ord($hash[6]) & 0x0f | 0x30);
        $hash[8] = chr(ord($hash[8]) & 0x3f | 0x80);

        return self::bytesToUuid($hash);
    }

    /**
     * Generate a UUID version 5 (SHA1-based, name-based)
     *
     * Generates a deterministic UUID v5 based on namespace and name using SHA1 hash.
     *
     * @param string $namespace UUID namespace (use NAMESPACE_* constants)
     * @param string $name Name to hash
     * @return string UUID v5 string in standard format
     */
    public static function uuid5(string $namespace, string $name): string {
        $nsBytes = self::uuidToBytes($namespace);
        $hash = sha1($nsBytes . $name, true);

        // Set version (5) and variant
        $hash[6] = chr(ord($hash[6]) & 0x0f | 0x50);
        $hash[8] = chr(ord($hash[8]) & 0x3f | 0x80);

        return self::bytesToUuid($hash);
    }

    /**
     * Generate a UUID version 7 (timestamp-ordered, random)
     *
     * Generates a UUID v7 with Unix timestamp prefix for database-friendly ordering.
     * This is the recommended version for new applications.
     *
     * @return string UUID v7 string in standard format
     * @throws \Exception If random bytes generation fails
     */
    public static function uuid7(): string {
        // Get current Unix timestamp in milliseconds
        $timestamp = (int)(microtime(true) * 1000);

        // Generate random bytes
        $rand = random_bytes(10);

        // Build UUID: 48-bit timestamp + 4-bit version + 12-bit random + 2-bit variant + 62-bit random
        $timeHex = sprintf('%012x', $timestamp);
        $randHex = bin2hex($rand);

        // Set version (7) in the appropriate position
        $versionNibble = '7';
        $variantBits = dechex((hexdec(substr($randHex, 4, 1)) & 0x3) | 0x8);

        return sprintf(
            '%s-%s-%s%s%s-%s%s-%s',
            substr($timeHex, 0, 8),
            substr($timeHex, 8, 4),
            $versionNibble,
            substr($randHex, 0, 3),
            $variantBits,
            substr($randHex, 5, 3),
            substr($randHex, 8, 12)
        );
    }

    /**
     * Validate UUID format
     *
     * Checks if a string is a valid UUID (any version).
     *
     * @param string $uuid UUID string to validate
     * @return bool True if valid UUID format
     */
    public static function isValid(string $uuid): bool {
        if (empty($uuid)) {
            return false;
        }

        $pattern = '/^[0-9a-f]{8}-[0-9a-f]{4}-[1-7][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i';
        return (bool) preg_match($pattern, $uuid);
    }

    /**
     * Validate UUID v4 specifically
     *
     * @param string $uuid UUID string to validate
     * @return bool True if valid UUID v4
     */
    public static function isValidV4(string $uuid): bool {
        if (empty($uuid)) {
            return false;
        }

        $pattern = '/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i';
        return (bool) preg_match($pattern, $uuid);
    }

    /**
     * Validate UUID v1 specifically
     *
     * @param string $uuid UUID string to validate
     * @return bool True if valid UUID v1
     */
    public static function isValidV1(string $uuid): bool {
        if (empty($uuid)) {
            return false;
        }

        $pattern = '/^[0-9a-f]{8}-[0-9a-f]{4}-1[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i';
        return (bool) preg_match($pattern, $uuid);
    }

    /**
     * Get UUID version
     *
     * @param string $uuid UUID string
     * @return int|null Version number (1-7) or null if invalid
     */
    public static function getVersion(string $uuid): ?int {
        if (!self::isValid($uuid)) {
            return null;
        }

        $parts = explode('-', $uuid);
        return (int) $parts[2][0];
    }

    /**
     * Convert UUID to compact format (no dashes)
     *
     * @param string $uuid UUID string
     * @return string|null Compact UUID or null if invalid
     */
    public static function toCompact(string $uuid): ?string {
        if (!self::isValid($uuid)) {
            return null;
        }
        return str_replace('-', '', $uuid);
    }

    /**
     * Convert compact UUID to standard format
     *
     * @param string $compact Compact UUID string (32 characters)
     * @return string|null Standard UUID or null if invalid
     */
    public static function fromCompact(string $compact): ?string {
        if (strlen($compact) !== 32 || !ctype_xdigit($compact)) {
            return null;
        }

        return sprintf(
            '%s-%s-%s-%s-%s',
            substr($compact, 0, 8),
            substr($compact, 8, 4),
            substr($compact, 12, 4),
            substr($compact, 16, 4),
            substr($compact, 20, 12)
        );
    }

    /**
     * Convert UUID to uppercase
     *
     * @param string $uuid UUID string
     * @return string|null Uppercase UUID or null if invalid
     */
    public static function toUpper(string $uuid): ?string {
        if (!self::isValid($uuid)) {
            return null;
        }
        return strtoupper($uuid);
    }

    /**
     * Convert UUID to lowercase
     *
     * @param string $uuid UUID string
     * @return string|null Lowercase UUID or null if invalid
     */
    public static function toLower(string $uuid): ?string {
        if (!self::isValid($uuid)) {
            return null;
        }
        return strtolower($uuid);
    }

    /**
     * Generate multiple UUIDs at once
     *
     * @param int $count Number of UUIDs to generate
     * @param string $version UUID version ('1', '3', '4', '5', '7')
     * @param string|null $namespace Namespace for v3/v5 (required for those versions)
     * @param string|null $name Name for v3/v5 (required for those versions)
     * @return array Array of UUID strings
     * @throws \Exception If random bytes generation fails
     * @throws \InvalidArgumentException If invalid version or missing params
     */
    public static function generateMultiple(int $count, string $version = '4', ?string $namespace = null, ?string $name = null): array {
        if ($count < 1) {
            throw new \InvalidArgumentException('Count must be at least 1');
        }

        $uuids = [];
        for ($i = 0; $i < $count; $i++) {
            switch ($version) {
                case '1':
                    $uuids[] = self::uuid1();
                    break;
                case '3':
                    if ($namespace === null || $name === null) {
                        throw new \InvalidArgumentException('Namespace and name required for v3');
                    }
                    $uuids[] = self::uuid3($namespace, $name . $i);
                    break;
                case '4':
                    $uuids[] = self::uuid4();
                    break;
                case '5':
                    if ($namespace === null || $name === null) {
                        throw new \InvalidArgumentException('Namespace and name required for v5');
                    }
                    $uuids[] = self::uuid5($namespace, $name . $i);
                    break;
                case '7':
                    $uuids[] = self::uuid7();
                    break;
                default:
                    throw new \InvalidArgumentException('Invalid UUID version: ' . $version);
            }
        }
        return $uuids;
    }

    /**
     * Check if two UUIDs are equal (case-insensitive)
     *
     * @param string $uuid1 First UUID
     * @param string $uuid2 Second UUID
     * @return bool True if equal
     */
    public static function equals(string $uuid1, string $uuid2): bool {
        return strtolower($uuid1) === strtolower($uuid2);
    }

    /**
     * Get UUID info array
     *
     * @param string $uuid UUID string
     * @return array|null Array with version, variant, and other info, or null if invalid
     */
    public static function getInfo(string $uuid): ?array {
        if (!self::isValid($uuid)) {
            return null;
        }

        $version = self::getVersion($uuid);
        $parts = explode('-', $uuid);

        // Determine variant from the first character of the 4th part
        $variantChar = $parts[3][0];
        $variantCode = hexdec($variantChar);
        if (($variantCode & 0x8) === 0) {
            $variant = 'NCS';
        } elseif (($variantCode & 0xC) === 0x8) {
            $variant = 'RFC4122';
        } elseif (($variantCode & 0xE) === 0xC) {
            $variant = 'Microsoft';
        } else {
            $variant = 'Future';
        }

        return [
            'uuid' => $uuid,
            'version' => $version,
            'variant' => $variant,
            'compact' => self::toCompact($uuid),
            'time_low' => $parts[0],
            'time_mid' => $parts[1],
            'time_high_and_version' => $parts[2],
            'clock_seq' => $parts[3],
            'node' => $parts[4]
        ];
    }

    /**
     * Generate a short ID (Base32 encoded, URL-safe)
     *
     * Generates a shorter alternative to UUID for URL-friendly identifiers.
     *
     * @param int $length Length of the short ID (default 22)
     * @return string Short ID string
     * @throws \Exception If random bytes generation fails
     */
    public static function shortId(int $length = 22): string {
        $bytes = random_bytes((int) ceil($length * 5 / 8));
        return self::base32Encode($bytes, $length);
    }

    /**
     * Generate a ULID (Universally Unique Lexicographically Sortable Identifier)
     *
     * @return string ULID string (26 characters)
     * @throws \Exception If random bytes generation fails
     */
    public static function ulid(): string {
        $timestamp = (int)(microtime(true) * 1000);
        $rand = random_bytes(10);

        // Crockford's Base32 encoding
        $ Crockford = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';

        $result = '';

        // Encode 48-bit timestamp (10 characters)
        for ($i = 9; $i >= 0; $i--) {
            $result = $Crockford[$timestamp & 0x1F] . $result;
            $timestamp >>= 5;
        }

        // Encode 80-bit randomness (16 characters)
        $randHex = bin2hex($rand);
        $randValue = hexdec(substr($randHex, 0, 16)) | (hexdec(substr($randHex, 16)) << 64);

        for ($i = 15; $i >= 0; $i--) {
            $result .= $Crockford[$randValue & 0x1F];
            $randValue >>= 5;
        }

        return $result;
    }

    // ==================== Private Helper Methods ====================

    /**
     * Convert UUID string to bytes
     *
     * @param string $uuid UUID string
     * @return string Binary bytes
     */
    private static function uuidToBytes(string $uuid): string {
        $hex = str_replace('-', '', $uuid);
        return hex2bin($hex);
    }

    /**
     * Convert bytes to UUID string
     *
     * @param string $bytes Binary bytes (16 bytes)
     * @return string UUID string
     */
    private static function bytesToUuid(string $bytes): string {
        $hex = bin2hex($bytes);
        return sprintf(
            '%s-%s-%s-%s-%s',
            substr($hex, 0, 8),
            substr($hex, 8, 4),
            substr($hex, 12, 4),
            substr($hex, 16, 4),
            substr($hex, 20, 12)
        );
    }

    /**
     * Get current timestamp in 100-nanosecond intervals since Oct 15, 1582
     *
     * @return int Timestamp in 100-nanosecond intervals
     */
    private static function getTimestamp100ns(): int {
        // UUID epoch (Oct 15, 1582) to Unix epoch (Jan 1, 1970) difference
        // 12219292800 seconds = 0x01B21DD213814000 * 100-nanoseconds
        $uuidEpochOffset = 0x01B21DD213814000;

        // Current time in 100-nanosecond intervals since Unix epoch
        $now = (int)(microtime(true) * 10000000);

        return $uuidEpochOffset + $now;
    }

    /**
     * Base32 encode bytes (Crockford's Base32)
     *
     * @param string $bytes Binary bytes
     * @param int $length Desired output length
     * @return string Base32 encoded string
     */
    private static function base32Encode(string $bytes, int $length): string {
        $Crockford = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';
        $result = '';
        $byteIndex = 0;
        $bitBuffer = 0;
        $bitsInBuffer = 0;

        while (strlen($result) < $length) {
            if ($bitsInBuffer < 5) {
                if ($byteIndex < strlen($bytes)) {
                    $bitBuffer = ($bitBuffer << 8) | ord($bytes[$byteIndex++]);
                    $bitsInBuffer += 8;
                } else {
                    break;
                }
            }

            $bitsInBuffer -= 5;
            $value = ($bitBuffer >> $bitsInBuffer) & 0x1F;
            $result .= $Crockford[$value];
        }

        // Pad if necessary
        while (strlen($result) < $length) {
            $result .= '0';
        }

        return substr($result, 0, $length);
    }
}
