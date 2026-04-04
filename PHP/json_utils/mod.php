<?php
/**
 * AllToolkit - JSON Utilities for PHP
 *
 * A zero-dependency JSON manipulation toolkit providing:
 * - JSON parsing with error handling
 * - JSON validation
 * - Pretty printing and minification
 * - JSON Path-like querying
 * - JSON merging and patching
 * - Type-safe accessors
 *
 * @author AllToolkit Contributors
 * @license MIT
 */

namespace AllToolkit;

/**
 * JSON parsing and manipulation utilities
 */
class JsonUtils
{
    /**
     * Parse JSON string with detailed error handling
     *
     * @param string $json JSON string to parse
     * @param bool $assoc Return associative array instead of object (default: true)
     * @return array|object|null Parsed data or null on error
     */
    /**
     * @return array|object|null
     */
    public static function parse(string $json, bool $assoc = true): array|object|null
    {
        if (empty($json)) {
            return null;
        }

        $data = json_decode($json, $assoc);
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            return null;
        }
        
        return $data;
    }

    /**
     * Parse JSON string with exception on error
     *
     * @param string $json JSON string to parse
     * @param bool $assoc Return associative array instead of object
     * @return array|object
     * @throws \RuntimeException On parse error
     */
    public static function parseOrThrow(string $json, bool $assoc = true): array|object
    {
        if (empty($json)) {
            throw new \RuntimeException('JSON string is empty');
        }

        $data = json_decode($json, $assoc);
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            throw new \RuntimeException('JSON parse error: ' . json_last_error_msg());
        }
        return $data;
    }

    /**
     * Check if string is valid JSON
     *
     * @param string $json String to validate
     * @return bool True if valid JSON
     */
    public static function isValid(string $json): bool
    {
        if (empty($json)) {
            return false;
        }

        json_decode($json);
        return json_last_error() === JSON_ERROR_NONE;
    }

    /**
     * Get JSON parse error message
     *
     * @param string $json JSON string that failed to parse
     * @return string|null Error message or null if valid
     */
    public static function getError(string $json): ?string
    {
        json_decode($json);
        $error = json_last_error();
        
        if ($error === JSON_ERROR_NONE) {
            return null;
        }
        
        return json_last_error_msg();
    }

    /**
     * Encode data to JSON string
     *
     * @param mixed $data Data to encode
     * @param bool $pretty Pretty print output
     * @param int $flags Additional JSON flags
     * @return string JSON string
     * @throws \RuntimeException On encode error
     */
    public static function stringify(mixed $data, bool $pretty = false, int $flags = 0): string
    {
        $jsonFlags = $flags | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES;
        
        if ($pretty) {
            $jsonFlags |= JSON_PRETTY_PRINT;
        }
        
        $result = json_encode($data, $jsonFlags);
        
        if ($result === false) {
            throw new \RuntimeException('JSON encode error: ' . json_last_error_msg());
        }
        
        return $result;
    }

    /**
     * Encode data to JSON string, return null on error
     *
     * @param mixed $data Data to encode
     * @param bool $pretty Pretty print output
     * @return string|null JSON string or null on error
     */
    public static function tryStringify(mixed $data, bool $pretty = false): ?string
    {
        try {
            return self::stringify($data, $pretty);
        } catch (\RuntimeException $e) {
            return null;
        }
    }

    /**
     * Pretty print JSON string
     *
     * @param string $json JSON string to format
     * @param int $indent Indentation spaces (default: 2)
     * @return string|null Pretty printed JSON or null on error
     */
    public static function prettyPrint(string $json, int $indent = 2): ?string
    {
        $data = self::parse($json);
        
        if ($data === null) {
            return null;
        }
        
        $result = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        
        if ($result === false) {
            return null;
        }
        
        // Adjust indentation if needed
        if ($indent !== 2) {
            $result = preg_replace_callback('/^( +)/m', function($matches) use ($indent) {
            $spaces = strlen($matches[1]);
                $levels = $spaces / 2;
                return str_repeat(' ', (int)($levels * $indent));
            }, $result);
        }
        
        return $result;
    }

    /**
     * Minify JSON string (remove whitespace)
     * @param string $json JSON string to minify
     * @return string|null Minified JSON or null on error
     */
    public static function minify(string $json): ?string
    {
        $data = self::parse($json);
        
        if ($data === null) {
            return null;
        }
        
        $result = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        
        return $result !== false ? $result : null;
    }

    /**
     * Get value from nested JSON using dot notation path
     *
     * @param array|object $data JSON data
     * @param string $path Dot notation path (e.g., "user.address.city")
     * @param mixed $default Default value if path not found
     */
    public static function get(array|object $data, string $path, mixed $default = null): mixed
    {
        if (empty($path)) {
            return $data;
        }

        $keys = explode('.', $path);
        $current = $data;
        // (optional: stop services if running
        //
        foreach ($keys as $key) {
            if (is_array($current) && array_key_exists($key, $current)) {
                $current = $current[$key];
            } elseif (is_object($current) && property_exists($current, $key)) {
                $current = $current->$key;
            } else {
                return $default;
            }
        }

        return $current;
    }

    /**
     * Set value at nested path using dot notation
     *
     * @param array $data Reference to array data
     * @param string $path Dot notation path
     * @param mixed $value Value to set
     * @return bool True if successful
     */
    public static function set(array &$data, string $path, mixed $value): bool
    {
        if (empty($path)) {
            return false;
        }

        $keys = explode('.', $path);
        $current = &$data;

        foreach ($keys as $i => $key) {
            if ($i === count($keys) - 1) {
                $current[$key] = $value;
                return true;
            }

            if (!isset($current[$key]) || !is_array($current[$key])) {
                $current[$key] = [];
            }

            $current = &$current[$key];
        }

        return true;
    }

    /**
     * Check if path exists in JSON data
     *
     * @param array|object $data JSON data
     * @param string $path Dot notation path
     * @return bool True if path exists
     */
    public static function has(array|object $data, string $path): bool
    {
        if (empty($path)) {
            return true;
        }

        $keys = explode('.', $path);
        $current = $data;

        foreach ($keys as $key) {
            if (is_array($current) && array_key_exists($key, $current)) {
                $current = $current[$key];
            } elseif (is_object($current) && property_exists($current, $key))            {
                $current = $current->$key;
            } else {
                return false;
            }
        }

        return true;
    }

    /**
     * Remove value at nested path
     *
     * @param array $data Reference to array data
     * @param string $path Dot notation path
     * @return bool True if removed, false if not found
     */
    public static function remove(array &$data, string $path): bool
    {
        if (empty($path)) {
            return false;
        }

        $keys = explode('.', $path);
        $lastKey = array_pop($keys);
        $current = &$data;

        foreach ($keys as $key) {
            if (!isset($current[$key]) || !is_array($current[$key])) {
                return false;
            }
            $current = &$current[$key];
        }

        if (array_key_exists($lastKey, $current)) {
            unset($current[$lastKey]);
            return true;
        }

        return false;
    }

    /**
     * Merge two JSON objects/arrays recursively
     *
     * @param array|object $base Base data
     * @param array|object $overlay Data to merge into base
     * @return array Merged data
     */
    public static function merge(array|object $base, array|object $overlay): array
    {
        $baseArray = is_object($base) ? (array) $base : $base;
        $overlayArray = is_object($overlay) ? (array) $overlay : $overlay;

        $result = $baseArray;

        foreach ($overlayArray as $key => $value) {
            if (is_array($value) && isset($result[$key]) && is_array($result[$key])) {
                $result[$key] = self::merge($result[$key], $value);
            } else {
                $result[$key] = $value;
            }
        }

        return $result;
    }

    /**
     * Deep clone JSON data
     *
     * @param mixed $data Data to clone
     * @return mixed Cloned data
     */
    public static function clone(mixed $data): mixed
    {
        return self::parse(self::stringify($data));
    }

    /**
     * Get all keys at a given path
     *
     * @param array|object $data JSON data
     * @param string $path Dot notation path to object
     * @return array List of keys
     */
    public static function keys(array|object $data, string $path = ''): array
    {
        $target = empty($path) ? $data : self::get($data, $path);

        if (is_array($target)) {
            return array_keys($target);
        } elseif (is_object($target)) {
            return array_keys(get_object_vars($target));
        }

        return [];
    }

    /**
     * Get all values at a given path
     *
     * @param array|object $data JSON data
     * @param string $path Dot notation path
     * @return array List of values
     */
    public static function values(array|object $data, string $path = ''): array
    {
        $target = empty($path) ? $data : self::get($data, $path);

        if (is_array($target)) {
            return array_values($target);
        } elseif (is_object($target)) {
            return array_values(get_object_vars($target));
        }

        return [];
    }

    /**
     * Flatten nested array to single level
     *
     * @param array $data Nested array
     * @param string $separator Key separator (default: '.')
     * @return array Flattened array
     */
    public static function flatten(array $data, string $separator = '.'): array
    {
        $result = [];

        foreach ($data as $key => $value) {
            if (is_array($value)) {
                $flattened = self::flatten($value, $separator);
                foreach ($flattened as $subKey => $subValue) {
                    $result[$key . $separator . $subKey] = $subValue;
                }
            } else {
                $result[$key] = $value;
            }
        }

        return $result;
    }

    /**
     * Unflatten single level array to nested
     *
     * @param array $data Flattened array
     * @param string $separator Key separator (default: '.')
     * @return array Nested array
     */
    public static function unflatten(array $data, string $separator = '.'): array
    {
        $result = [];

        foreach ($data as $key => $value) {
            self::set($result, $key, $value);
        }

        return $result;
    }

    /**
     * Get string value safely
     *
     * @param array|object $data JSON data
     * @param string $path Dot notation path
     * @param string $default Default value
     * @return string String value
     */
    public static function getString(array|object $data, string $path, string $default = ''): string
    {
        $value = self::get($data, $path, $default);
        return is_scalar($value) ? (string) $value : $default;
    }

    /**
     * Get integer value safely
     *
     * @param array|object $data JSON data
     * @param string $path Dot notation path
     * @param int $default Default value
     * @return int Integer value
     */
    public static function getInt(array|object $data, string $path, int $default = 0): int
    {
        $value = self::get($data, $path, $default);
        return is_numeric($value) ? (int) $value : $default;
    }

    /**
     * Get float value safely
     *
     * @param array|object $data JSON data
     * @param string $path Dot notation path
     * @param float $default Default value
     * @return float Float value
     */
    public static function getFloat(array|object $data, string $path, float $default = 0.0): float
    {
        $value = self::get($data, $path, $default);
        return is_numeric($value) ? (float) $value : $default;
    }

    /**
     * Get boolean value safely
     *
     * @param array|object $data JSON data
     * @param string $path Dot notation path
     * @param bool $default Default value
     * @return bool Boolean value
     */
    public static function getBool(array|object $data, string $path, bool $default = false): bool
    {
        $value = self::get($data, $path, $default);
        return (bool) $value;
    }

    /**
     * Get array value safely
     *
     * @param array|object $data JSON data
     * @param string $path Dot notation path
     * @param array $default Default value
     * @return array Array value
     */
    public static function getArray(array|object $data, string $path, array $default = []): array
    {
        $value = self::get($data, $path, $default);
        return is_array($value) ? $value : $default;
    }

    /**
     * Compare two JSON structures for equality
     *
     * @param mixed $a First value
     * @param mixed $b Second value
     * @return bool True if equal
     */
    public static function equals(mixed $a, mixed $b): bool
    {
        return self::stringify($a) === self::stringify($b);
    }
}
