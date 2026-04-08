<?php
/**
 * AllToolkit - PHP Array Utilities
 *
 * A comprehensive array manipulation utility module providing common array operations
 * including filtering, sorting, searching, transformation, and utility functions.
 *
 * @package    AllToolkit
 * @subpackage ArrayUtils
 * @author     AllToolkit Team
 * @license    MIT
 * @version    1.0.0
 */

namespace AllToolkit;

/**
 * Array utility class providing static methods for array manipulation
 */
class ArrayUtils
{
    /**
     * Check if array is empty or null
     *
     * @param array|null $arr The array to check
     * @return bool True if array is null or empty
     */
    public static function isEmpty(?array $arr): bool
    {
        return $arr === null || empty($arr);
    }

    /**
     * Check if array is not empty
     *
     * @param array|null $arr The array to check
     * @return bool True if array is not null and not empty
     */
    public static function isNotEmpty(?array $arr): bool
    {
        return $arr !== null && !empty($arr);
    }

    /**
     * Get array length
     *
     * @param array|null $arr The array
     * @return int Number of elements (0 if null)
     */
    public static function length(?array $arr): int
    {
        return $arr === null ? 0 : count($arr);
    }

    /**
     * Get first element of array
     *
     * @param array|null $arr The array
     * @param mixed|null $default Default value if array is empty
     * @return mixed|null First element or default
     */
    public static function first(?array $arr, $default = null)
    {
        if ($arr === null || empty($arr)) {
            return $default;
        }
        return reset($arr);
    }

    /**
     * Get last element of array
     *
     * @param array|null $arr The array
     * @param mixed|null $default Default value if array is empty
     * @return mixed|null Last element or default
     */
    public static function last(?array $arr, $default = null)
    {
        if ($arr === null || empty($arr)) {
            return $default;
        }
        return end($arr);
    }

    /**
     * Get element at index (supports negative indices)
     *
     * @param array|null $arr The array
     * @param int $index Index (negative for from end)
     * @param mixed|null $default Default value if index out of bounds
     * @return mixed|null Element at index or default
     */
    public static function get(?array $arr, int $index, $default = null)
    {
        if ($arr === null) {
            return $default;
        }

        $length = count($arr);
        if ($length === 0) {
            return $default;
        }

        // Handle negative index
        if ($index < 0) {
            $index = $length + $index;
        }

        if ($index < 0 || $index >= $length) {
            return $default;
        }

        $values = array_values($arr);
        return $values[$index];
    }

    /**
     * Check if array contains a value
     *
     * @param array|null $arr The array
     * @param mixed $value Value to search for
     * @param bool $strict Use strict comparison
     * @return bool True if value exists in array
     */
    public static function contains(?array $arr, $value, bool $strict = false): bool
    {
        if ($arr === null) {
            return false;
        }
        return in_array($value, $arr, $strict);
    }

    /**
     * Check if array contains a key
     *
     * @param array|null $arr The array
     * @param string|int $key Key to check
     * @return bool True if key exists
     */
    public static function hasKey(?array $arr, $key): bool
    {
        if ($arr === null) {
            return false;
        }
        return array_key_exists($key, $arr);
    }

    /**
     * Find index of a value
     *
     * @param array|null $arr The array
     * @param mixed $value Value to find
     * @param bool $strict Use strict comparison
     * @return int|false Index of value or false if not found
     */
    public static function indexOf(?array $arr, $value, bool $strict = false)
    {
        if ($arr === null) {
            return false;
        }
        return array_search($value, $arr, $strict);
    }

    /**
     * Find all indices of a value
     *
     * @param array|null $arr The array
     * @param mixed $value Value to find
     * @param bool $strict Use strict comparison
     * @return array Array of indices
     */
    public static function indicesOf(?array $arr, $value, bool $strict = false): array
    {
        if ($arr === null) {
            return [];
        }

        $indices = [];
        foreach ($arr as $key => $item) {
            if ($strict ? $item === $value : $item == $value) {
                $indices[] = $key;
            }
        }
        return $indices;
    }

    /**
     * Filter array using callback function
     *
     * @param array|null $arr The array
     * @param callable $callback Function($value, $key) returning bool
     * @return array Filtered array
     */
    public static function filter(?array $arr, callable $callback): array
    {
        if ($arr === null) {
            return [];
        }

        $result = [];
        foreach ($arr as $key => $value) {
            if ($callback($value, $key)) {
                $result[$key] = $value;
            }
        }
        return $result;
    }

    /**
     * Map array values using callback function
     *
     * @param array|null $arr The array
     * @param callable $callback Function($value, $key) returning new value
     * @return array Mapped array
     */
    public static function map(?array $arr, callable $callback): array
    {
        if ($arr === null) {
            return [];
        }

        $result = [];
        foreach ($arr as $key => $value) {
            $result[$key] = $callback($value, $key);
        }
        return $result;
    }

    /**
     * Reduce array to single value
     *
     * @param array|null $arr The array
     * @param callable $callback Function($carry, $value, $key) returning new carry
     * @param mixed|null $initial Initial value
     * @return mixed|null Reduced value
     */
    public static function reduce(?array $arr, callable $callback, $initial = null)
    {
        if ($arr === null) {
            return $initial;
        }

        $carry = $initial;
        foreach ($arr as $key => $value) {
            $carry = $callback($carry, $value, $key);
        }
        return $carry;
    }

    /**
     * Find first element matching predicate
     *
     * @param array|null $arr The array
     * @param callable $predicate Function($value, $key) returning bool
     * @param mixed|null $default Default value if not found
     * @return mixed|null Found element or default
     */
    public static function find(?array $arr, callable $predicate, $default = null)
    {
        if ($arr === null) {
            return $default;
        }

        foreach ($arr as $key => $value) {
            if ($predicate($value, $key)) {
                return $value;
            }
        }
        return $default;
    }

    /**
     * Find all elements matching predicate
     *
     * @param array|null $arr The array
     * @param callable $predicate Function($value, $key) returning bool
     * @return array Array of matching elements
     */
    public static function findAll(?array $arr, callable $predicate): array
    {
        if ($arr === null) {
            return [];
        }

        $result = [];
        foreach ($arr as $key => $value) {
            if ($predicate($value, $key)) {
                $result[$key] = $value;
            }
        }
        return $result;
    }

    /**
     * Check if any element matches predicate
     *
     * @param array|null $arr