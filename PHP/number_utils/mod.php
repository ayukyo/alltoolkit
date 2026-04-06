<?php
/**
 * Number Utilities for PHP
 * 
 * A comprehensive number utility module providing formatting, conversion,
 * mathematical operations, and statistical functions with zero dependencies.
 * 
 * @package AllToolkit\NumberUtils
 * @author AllToolkit Contributors
 * @license MIT
 */

namespace AllToolkit;

/**
 * Number utility class providing comprehensive number operations
 */
class NumberUtils
{
    /**
     * Format a number with thousands separator
     */
    public static function format($number, int $decimals = 0, string $decimalSeparator = '.', string $thousandsSeparator = ','): string {
        return number_format((float)$number, $decimals, $decimalSeparator, $thousandsSeparator);
    }

    /**
     * Format a number as currency
     */
    public static function currency($amount, string $symbol = '$', int $decimals = 2): string {
        return $symbol . self::format($amount, $decimals);
    }

    /**
     * Format a number as percentage
     */
    public static function percentage($number, int $decimals = 0, bool $includeSymbol = true): string {
        $value = self::format($number * 100, $decimals);
        return $includeSymbol ? $value . '%' : $value;
    }

    /**
     * Format a number in compact notation (K, M, B, T)
     */
    public static function compact($number, int $precision = 1): string {
        $number = (float)$number;
        $suffixes = ['', 'K', 'M', 'B', 'T', 'Q'];
        $suffixIndex = 0;
        while (abs($number) >= 1000 && $suffixIndex < count($suffixes) - 1) {
            $number /= 1000;
            $suffixIndex++;
        }
        return self::format($number, $precision) . $suffixes[$suffixIndex];
    }

    /**
     * Convert a number to ordinal string (1st, 2nd, 3rd, etc.)
     */
    public static function ordinal(int $number): string {
        if (!in_array($number % 100, [11, 12, 13], true)) {
            switch ($number % 10) {
                case 1: return $number . 'st';
                case 2: return $number . 'nd';
                case 3: return $number . 'rd';
            }
        }
        return $number . 'th';
    }

    /**
     * Convert a number to English words
     */
    public static function toWords(int $number): string {
        if ($number === 0) return 'zero';
        if ($number < 0) return 'negative ' . self::toWords(abs($number));
        $words = [];
        $scales = ['', 'thousand', 'million', 'billion'];
        $scaleIndex = 0;
        while ($number > 0) {
            $chunk = $number % 1000;
            if ($chunk > 0) {
                $chunkWords = self::convertChunk($chunk);
                if ($scaleIndex > 0) $chunkWords .= ' ' . $scales[$scaleIndex];
                array_unshift($words, $chunkWords);
            }
            $number = (int)($number / 1000);
            $scaleIndex++;
        }
        return implode(' ', $words);
    }

    private static function convertChunk(int $number): string {
        $ones = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'];
        $teens = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'];
        $tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];
        $words = [];
        if ($number >= 100) {
            $words[] = $ones[(int)($number / 100)] . ' hundred';
            $number %= 100;
        }
        if ($number >= 20) {
            $tenWord = $tens[(int)($number / 10)];
            $number %= 10;
            if ($number > 0) $tenWord .= '-' . $ones[$number];
            $words[] = $tenWord;
        } elseif ($number >= 10) {
            $words[] = $teens[$number - 10];
        } elseif ($number > 0) {
            $words[] = $ones[$number];
        }
        return implode(' ', $words);
    }

    /**
     * Convert integer to Roman numeral (1-3999)
     */
    public static function toRoman(int $number): string {
        if ($number < 1 || $number > 3999) throw new \InvalidArgumentException('Number must be between 1 and 3999');
        $map = ['M' => 1000, 'CM' => 900, 'D' => 500, 'CD' => 400, 'C' => 100, 'XC' => 90, 'L' => 50, 'XL' => 40, 'X' => 10, 'IX' => 9, 'V' => 5, 'IV' => 4, 'I' => 1];
        $result = '';
        foreach ($map as $roman => $value) {
            while ($number >= $value) {
                $result .= $roman;
                $number -= $value;
            }
        }
        return $result;
    }

    /**
     * Convert Roman numeral to integer
     */
    public static function fromRoman(string $roman): int {
        $map = ['I' => 1, 'V' => 5, 'X' => 10, 'L' => 50, 'C' => 100, 'D' => 500, 'M' => 1000];
        $roman = strtoupper($roman);
        $result = 0;
        $prev = 0;
        for ($i = strlen($roman) - 1; $i >= 0; $i--) {
            $current = $map[$roman[$i]] ?? 0;
            if ($current < $prev) $result -= $current;
            else $result += $current;
            $prev = $current;
        }
        return $result;
    }

    /**
     * Convert number to binary string
     */
    public static function toBinary(int $number, bool $prefix = false, ?int $minWidth = null): string {
        $binary = decbin($number);
        if ($minWidth !== null) $binary = str_pad($binary, $minWidth, '0', STR_PAD_LEFT);
        return $prefix ? '0b' . $binary : $binary;
    }

    /**
     * Convert number to hexadecimal string
     */
    public static function toHex(int $number, bool $prefix = false, bool $uppercase = false, ?int $minWidth = null): string {
        $hex = dechex($number);
        if ($minWidth !== null) $hex = str_pad($hex, $minWidth, '0', STR_PAD_LEFT);
        if ($uppercase) $hex = strtoupper($hex);
        return $prefix ? '0x' . $hex : $hex;
    }

    /**
     * Convert number to octal string
     */
    public static function toOctal(int $number, bool $prefix = false): string {
        return $prefix ? '0' . decoct($number) : decoct($number);
    }

    /**
     * Clamp a value between min and max
     */
    public static function clamp($value, $min, $max) {
        return max($min, min($max, $value));
    }

    /**
     * Linear interpolation between start and end
     */
    public static function lerp(float $start, float $end, float $t): float {
        return $start + ($end - $start) * self::clamp($t, 0, 1);
    }

    /**
     * Map a value from one range to another
     */
    public static function mapRange($value, $inMin, $inMax, $outMin, $outMax) {
        return $outMin + ($value - $inMin) * ($outMax - $outMin) / ($inMax - $inMin);
    }

    /**
     * Check if two floats are approximately equal
     */
    public static function approxEqual(float $a, float $b, float $epsilon = 1e-9): bool {
        return abs($a - $b) < $epsilon;
    }

    /**
     * Round to nearest multiple
     */
    public static function roundToMultiple($number, $multiple) {
        return round($number / $multiple) * $multiple;
    }

    /**
     * Round to specific decimal places
     */
    public static function roundToPlaces(float $number, int $places): float {
        $factor = pow(10, $places);
        return round($number * $factor) / $factor;
    }

    /**
     * Calculate arithmetic mean
     */
    public static function mean(array $numbers): float {
        if (empty($numbers)) return 0.0;
        return array_sum($numbers) / count($numbers);
    }

    /**
     * Calculate median
     */
    public static function median(array $numbers): float {
        if (empty($numbers)) return 0.0;
        sort($numbers);
        $count = count($numbers);
        $middle = (int)($count / 2);
        if ($count % 2 === 0) return ($numbers[$middle - 1] + $numbers[$middle]) / 2;
        return $numbers[$middle];
    }

    /**
     * Calculate mode (most frequent value)
     */
    public static function mode(array $numbers): ?float {
        if (empty($numbers)) return null;
        $counts = array_count_values(array_map('strval', $numbers));
        arsort($counts);
        $maxCount = reset($counts);
        $modes = array_filter($counts, function($v) use ($maxCount) { return $v === $maxCount; });
        $firstMode = array_key_first($modes);
        return is_numeric($firstMode) ? (float)$firstMode : null;
    }

    /**
     * Calculate standard deviation
     */
    public static function stdDev(array $numbers, bool $sample = false): float {
        if (count($numbers) < 2) return 0.0;
        $mean = self::mean($numbers);
        $variance = 0.0;
        foreach ($numbers as $num) $variance += pow($num - $mean, 2);
        $variance /= count($numbers) - ($sample ? 1 : 0);
        return sqrt($variance);
    }

    /**
     * Calculate sum of squares
     */
    public static function sumOfSquares(array $numbers): float {
        return array_sum(array_map(function($n) { return $n * $n; }, $numbers));
    }

    /**
     * Calculate range (max - min)
     */
    public static function range(array $numbers): float {
        if (empty($numbers)) return 0.0;
        return max($numbers) - min($numbers);
    }

    /**
     * Check if value is numeric
     */
    public static function isNumeric($value): bool {
        return is_numeric($value);
    }

    /**
     * Check if value is an integer
     */
    public static function isInteger($value): bool {
        if (!is_numeric($value)) return false;
        return (float)$value == (int)$value;
    }

    /**
     * Check if number is even
     */
    public static function isEven(int $number): bool {
        return $number % 2 === 0;
    }

    /**
     * Check if number is odd
     */
    public static function isOdd(int $number): bool {
        return $number % 2 !== 0;
    }

    /**
     * Check if number is positive
     */
    public static function isPositive($number): bool {
        return $number > 0;
    }

    /**
     * Check if number is negative
     */
    public static function isNegative($number): bool {
        return $number < 0;
    }

    /**
     * Check if number is zero
     */
    public static function isZero($number): bool {
        return $number == 0;
    }

    /**
     * Check if number is between min and max
     */
    public static function between($number, $min, $max, bool $inclusive = true): bool {
        if ($inclusive) return $number >= $min && $number <= $max;
        return $number > $min && $number < $max;
    }

    /**
     * Check if number is prime
     */
    public static function isPrime(int $number): bool {
        if ($number < 2) return false;
        if ($number === 2) return true;
        if (self::isEven($number)) return false;
        $sqrt = (int)sqrt($number);
        for ($i = 3; $i <= $sqrt; $i += 2) {
            if ($number % $i === 0) return false;
        }
        return true;
    }

    /**
     * Check if number is a perfect square
     */
    public static function isPerfectSquare(int $number): bool {
        if ($number < 0) return false;
        $sqrt = (int)sqrt($number);
        return $sqrt * $sqrt === $number;
    }

    /**
     * Parse a string to number
     */
    public static function parse($str, $default = null) {
        if (!is_string($str)) return $default;
        $str = trim($str);
        $str = str_replace([',', '$', '%', ' '], '', $str);
        if (is_numeric($str)) return (float)$str;
        return $default;
    }

    /**
     * Parse a string to integer
     */
    public static function parseInt($str, ?int $default = null, int $base = 10): ?int {
        $result = self::parse($str);
        if ($result === null) return $default;
        return (int)$result;
    }

    /**
     * Parse a string to float
     */
    public static function parseFloat($str, ?float $default = null): ?float {
        return self::parse($str, $default);
    }

    /**
     * Calculate greatest common divisor
     */
    public static function gcd(int $a, int $b): int {
        $a = abs($a);
        $b = abs($b);
        while ($b !== 0) {
            $temp = $b;
            $b = $a % $b;
            $a = $temp;
        }
        return $a;
    }

    /**
     * Calculate least common multiple
     */
    public static function lcm(int $a, int $b): int {
        if ($a === 0 || $b === 0) return 0;
        return abs($a * $b) / self::gcd($a, $b);
    }

    /**
     * Calculate factorial
     */
    public static function factorial(int $n): int {
        if ($n < 0) throw new \InvalidArgumentException('Factorial is not defined for negative numbers');
        if ($n === 0 || $n === 1) return 1;
        $result = 1;
        for ($i = 2; $i <= $n; $i++) $result *= $i;
        return $result;
    }

    /**
     * Calculate Fibonacci number
     */
    public static function fibonacci(int $n): int {
        if ($n < 0) throw new \InvalidArgumentException('Fibonacci is not defined for negative numbers');
        if ($n === 0) return 0;
        if ($n === 1) return 1;
        $a = 0;
        $b = 1;
        for ($i = 2; $i <= $n; $i++) {
            $temp = $a + $b;
            $a = $b;
            $b = $temp;
        }
        return $b;
    }

    /**
     * Calculate square root
     */
    public static function sqrt(float $number): float {
        return sqrt($number);
    }

    /**
     * Calculate nth root
     */
    public static function nthRoot(float $number, int $n): float {
        if ($n === 0) throw new \InvalidArgumentException('Root cannot be zero');
        return pow($number, 1 / $n);
    }

    /**
     * Convert degrees to radians
     */
    public static function toRadians(float $degrees): float {
        return $degrees * M_PI / 180;
    }

    /**
     * Convert radians to degrees
     */
    public static function toDegrees(float $radians): float {
        return $radians * 180 / M_PI;
    }

    /**
     * Normalize angle to 0-360 range
     */
    public static function normalizeAngle(float $degrees): float {
        $angle = fmod($degrees, 360);
        if ($angle < 0) $angle += 360;
        return $angle;
    }

    /**
     * Calculate sum of digits
     */
    public static function sumOfDigits(int $number): int {
        $number = abs($number);
        $sum = 0;
        while ($number > 0) {
            $sum += $number % 10;
            $number = (int)($number / 10);
        }
        return $sum;
    }

    /**
     * Reverse digits of a number
     */
    public static function reverseDigits(int $number): int {
        $negative = $number < 0;
        $number = abs($number);
        $reversed = 0;
        while ($number > 0) {
            $reversed = $reversed * 10 + $number % 10;
            $number = (int)($number / 10);
        }
        return $negative ? -$reversed : $reversed;
    }

    /**
     * Check if number is a palindrome
     */
    public static function isPalindrome(int $number): bool {
        return $number === self::reverseDigits($number);
    }

    /**
     * Generate random float
     */
    public static function random(float $min = 0, float $max = 1): float {
        return $min + mt_rand() / mt_getrandmax() * ($max - $min);
    }

    /**
     * Generate random integer
     */
    public static function randomInt(int $min, int $max): int {
        return mt_rand($min, $max);
    }

    /**
     * Generate random number from normal distribution
     */
    public static function randomNormal(float $mean = 0, float $stdDev = 1): float {
        $u1 = mt_rand() / mt_getrandmax();
        $u2 = mt_rand() / mt_getrandmax();
        $z = sqrt(-2 * log($u1)) * cos(2 * M_PI * $u2);
        return $mean + $z * $stdDev;
    }
}
