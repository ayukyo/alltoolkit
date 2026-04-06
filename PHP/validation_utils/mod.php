<?php
/**
 * AllToolkit - PHP Validation Utilities
 * 
 * A comprehensive validation utility module providing common validation functions
 * for strings, numbers, emails, URLs, IDs, and more with zero dependencies.
 * 
 * @package AllToolkit\ValidationUtils
 * @version 1.0.0
 * @license MIT
 */

namespace AllToolkit;

/**
 * Validation result class
 */
class ValidationResult
{
    /** @var bool Whether validation passed */
    public $valid;
    
    /** @var string|null Error message if validation failed */
    public $message;
    
    /** @var string|null Field name being validated */
    public $field;
    
    /**
     * Constructor
     * 
     * @param bool $valid Whether validation passed
     * @param string|null $message Error message
     * @param string|null $field Field name
     */
    public function __construct(bool $valid = true, ?string $message = null, ?string $field = null)
    {
        $this->valid = $valid;
        $this->message = $message;
        $this->field = $field;
    }
    
    /**
     * Check if validation passed
     * 
     * @return bool
     */
    public function isValid(): bool
    {
        return $this->valid;
    }
    
    /**
     * Get error message
     * 
     * @return string|null
     */
    public function getMessage(): ?string
    {
        return $this->message;
    }
    
    /**
     * Get field name
     * 
     * @return string|null
     */
    public function getField(): ?string
    {
        return $this->field;
    }
    
    /**
     * Convert to array
     * 
     * @return array
     */
    public function toArray(): array
    {
        return [
            'valid' => $this->valid,
            'message' => $this->message,
            'field' => $this->field
        ];
    }
}

/**
 * Validation utilities class
 */
class ValidationUtils
{
    // Email validation pattern (RFC 5322 compliant, simplified)
    private const EMAIL_PATTERN = '/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/';
    
    // URL validation pattern
    private const URL_PATTERN = '/^https?:\/\/(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?::\d{2,5})?(?:\/[^\s]*)?$/i';
    
    // UUID validation pattern
    private const UUID_PATTERN = '/^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/';
    
    // Hex color validation pattern
    private const HEX_COLOR_PATTERN = '/^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$/';
    
    // MAC address validation pattern
    private const MAC_PATTERN = '/^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$/';
    
    /**
     * Check if value is empty (null, empty string, or empty array)
     * 
     * @param mixed $value Value to check
     * @return bool
     */
    public static function isEmpty($value): bool
    {
        if ($value === null) {
            return true;
        }
        if (is_string($value)) {
            return trim($value) === '';
        }
        if (is_array($value)) {
            return empty($value);
        }
        return false;
    }
    
    /**
     * Check if value is not empty
     * 
     * @param mixed $value Value to check
     * @return bool
     */
    public static function isNotEmpty($value): bool
    {
        return !self::isEmpty($value);
    }
    
    /**
     * Check if string is blank (null, empty, or whitespace only)
     * 
     * @param string|null $str String to check
     * @return bool
     */
    public static function isBlank(?string $str): bool
    {
        return $str === null || trim($str) === '';
    }
    
    /**
     * Check if string is not blank
     * 
     * @param string|null $str String to check
     * @return bool
     */
    public static function isNotBlank(?string $str): bool
    {
        return !self::isBlank($str);
    }
    
    /**
     * Validate email format
     * 
     * @param string|null $email Email to validate
     * @return bool
     */
    public static function isEmail(?string $email): bool
    {
        if ($email === null || trim($email) === '') {
            return false;
        }
        return preg_match(self::EMAIL_PATTERN, $email) === 1;
    }
    
    /**
     * Validate URL format
     * 
     * @param string|null $url URL to validate
     * @param bool $requireHttp Whether to require http/https scheme
     * @return bool
     */
    public static function isUrl(?string $url, bool $requireHttp = true): bool
    {
        if ($url === null || trim($url) === '') {
            return false;
        }
        
        if ($requireHttp) {
            return preg_match(self::URL_PATTERN, $url) === 1;
        }
        
        return filter_var($url, FILTER_VALIDATE_URL) !== false;
    }
    
    /**
     * Validate IPv4 address
     * 
     * @param string|null $ip IP address to validate
     * @return bool
     */
    public static function isIpv4(?string $ip): bool
    {
        if ($ip === null || trim($ip) === '') {
            return false;
        }
        return filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4) !== false;
    }
    
    /**
     * Validate IPv6 address
     * 
     * @param string|null $ip IP address to validate
     * @return bool
     */
    public static function isIpv6(?string $ip): bool
    {
        if ($ip === null || trim($ip) === '') {
            return false;
        }
        return filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6) !== false;
    }
    
    /**
     * Validate IP address (IPv4 or IPv6)
     * 
     * @param string|null $ip IP address to validate
     * @return bool
     */
    public static function isIp(?string $ip): bool
    {
        if ($ip === null || trim($ip) === '') {
            return false;
        }
        return filter_var($ip, FILTER_VALIDATE_IP) !== false;
    }
    
    /**
     * Validate UUID format
     * 
     * @param string|null $uuid UUID to validate
     * @param int|null $version Specific version to validate (1, 4, etc.)
     * @return bool
     */
    public static function isUuid(?string $uuid, ?int $version = null): bool
    {
        if ($uuid === null || trim($uuid) === '') {
            return false;
        }
        
        if (!preg_match(self::UUID_PATTERN, $uuid)) {
            return false;
        }
        
        if ($version !== null) {
            // Check version nibble at position 14
            $uuidVersion = hexdec(substr(str_replace('-', '', $uuid), 12, 1));
            return $uuidVersion === $version;
        }
        
        return true;
    }
    
    /**
     * Validate hex color code
     * 
     * @param string|null $color Color code to validate
     * @return bool
     */
    public static function isHexColor(?string $color): bool
    {
        if ($color === null || trim($color) === '') {
            return false;
        }
        return preg_match(self::HEX_COLOR_PATTERN, $color) === 1;
    }
    
    /**
     * Validate MAC address
     * 
     * @param string|null $mac MAC address to validate
     * @return bool
     */
    public static function isMacAddress(?string $mac): bool
    {
        if ($mac === null || trim($mac) === '') {
            return false;
        }
        return preg_match(self::MAC_PATTERN, $mac) === 1;
    }
    
    /**
     * Check if string contains only alphabetic characters
     * 
     * @param string|null $str String to check
     * @return bool
     */
    public static function isAlpha(?string $str): bool
    {
        if ($str === null || $str === '') {
            return false;
        }
        return ctype_alpha($str);
    }
    
    /**
     * Check if string contains only alphanumeric characters
     * 
     * @param string|null $str String to check
     * @return bool
     */
    public static function isAlphanumeric(?string $str): bool
    {
        if ($str === null || $str === '') {
            return false;
        }
        return ctype_alnum($str);
    }
    
    /**
     * Check if string contains only digits
     * 
     * @param string|null $str String to check
     * @return bool
     */
    public static function isNumeric(?string $str): bool
    {
        if ($str === null || $str === '') {
            return false;
        }
        return ctype_digit($str);
    }
    
    /**
     * Check if string is a valid integer (including negative)
     * 
     * @param string|null $str String to check
     * @return bool
     */
    public static function isInteger(?string $str): bool
    {
        if ($str === null || $str === '') {
            return false;
        }
        return filter_var($str, FILTER_VALIDATE_INT) !== false;
    }
    
    /**
     * Check if string is a valid float number
     * 
     * @param string|null $str String to check
     * @return bool
     */
    public static function isFloat(?string $str): bool
    {
        if ($str === null || $str === '') {
            return false;
        }
        return filter_var($str, FILTER_VALIDATE_FLOAT) !== false;
    }
    
    /**
     * Check if value is a valid number (int or float)
     * 
     * @param mixed $value Value to check
     * @return bool
     */
    public static function isNumber($value): bool
    {
        if ($value === null) {
            return false;
        }
        if (is_int($value) || is_float($value)) {
            return true;
        }
        if (is_string($value)) {
            return self::isInteger($value) || self::isFloat($value);
        }
        return false;
    }
    
    /**
     * Check if string matches regex pattern
     * 
     * @param string|null $str String to check
     * @param string $pattern Regex pattern
     * @return bool
     */
    public static function matches(?string $str, string $pattern): bool
    {
        if ($str === null) {
            return false;
        }
        return preg_match($pattern, $str) === 1;
    }
    
    /**
     * Check if string length is within range
     * 
     * @param string|null $str String to check
     * @param int|null $min Minimum length (null for no minimum)
     * @param int|null $max Maximum length (null for no maximum)
     * @return bool
     */
    public static function lengthBetween(?string $str, ?int $min = null, ?int $max = null): bool
    {
        if ($str === null) {
            return false;
        }
        $len = strlen($str);
        if ($min !== null && $len < $min) {
            return false;
        }
        if ($max !== null && $len > $max) {
            return false;
        }
        return true;
    }
    
    /**
     * Check if numeric value is within range
     * 
     * @param float|int|string|null $value Value to check
     * @param float|int|null $min Minimum value (null for no minimum)
     * @param float|int|null $max Maximum value (null for no maximum)
     * @return bool
     */
    public static function between($value, $min = null, $max = null): bool
    {
        if ($value === null) {
            return false;
        }
        
        $num = is_numeric($value) ? (float)$value : null;
        if ($num === null) {
            return false;
        }
        
        if ($min !== null && $num < (float)$min) {
            return false;
        }
        if ($max !== null && $num > (float)$max) {
            return false;
        }
        return true;
    }
    
    /**
     * Check if value is positive
     * 
     * @param float|int|string|null $value Value to check
     * @return bool
     */
    public static function isPositive($value): bool
    {
        if ($value === null) {
            return false;
        }
        return is_numeric($value) && (float)$value > 0;
    }
    
    /**
     * Check if value is negative
     * 
     * @param float|int|string|null $value Value to check
     * @return bool
     */
    public static function isNegative($value): bool
    {
        if ($value === null) {
            return false;
        }
        return is_numeric($value) && (float)$value < 0;
    }
    
    /**
     * Check if value is zero
     * 
     * @param float|int|string|null $value Value to check
     * @return bool
     */
    public static function isZero($value): bool
    {
        if ($value === null) {
            return false;
        }
        return is_numeric($value) && (float)$value === 0.0;
    }
    
    /**
     * Validate credit card number using Luhn algorithm
     * 
     * @param string|null $cardNumber Credit card number to validate
     * @return bool
     */
    public static function isCreditCard(?string $cardNumber): bool
    {
        if ($cardNumber === null || trim($cardNumber) === '') {
            return false;
        }
        
        // Remove spaces and dashes
        $cardNumber = preg_replace('/[\s-]/', '', $cardNumber);
        
        // Must be numeric and 13-19 digits
        if (!ctype_digit($cardNumber) || strlen($cardNumber) < 13 || strlen($cardNumber) > 19) {
            return false;
        }
        
        // Luhn algorithm
        $sum = 0;
        $alternate = false;
        for ($i = strlen($cardNumber) - 1; $i >= 0; $i--) {
            $digit = (int)$cardNumber[$i];
            if ($alternate) {
                $digit *= 2;
                if ($digit > 9) {
                    $digit -= 9;
                }
            }
            $sum += $digit;
            $alternate = !$alternate;
        }
        
        return $sum % 10 === 0;
    }
    
    /**
     * Validate Chinese mobile phone number
     * 
     * @param string|null $phone Phone number to validate
     * @return bool
     */
    public static function isChinaMobile(?string $phone): bool
    {
        if ($phone === null || trim($phone) === '') {
            return false;
        }
        // Remove spaces and dashes
        $phone = preg_replace('/[\s-]/', '', $phone);
        // China mobile: 11 digits, starts with 1
        return preg_match('/^1[3-9]\d{9}$/', $phone) === 1;
    }
    
    /**
     * Validate Chinese ID card number
     * 
     * @param string|null $idCard ID card number to validate
     * @return bool
     */
    public static function isChinaIdCard(?string $idCard): bool
    {
        if ($idCard === null || trim($idCard) === '') {
            return false;
        }
        
        $idCard = strtoupper(trim($idCard));
        
        // 18-digit ID card
        if (strlen($idCard) !== 18) {
            return false;
        }
        
        // Check first 17 digits are numeric
        if (!ctype_digit(substr($idCard, 0, 17))) {
            return false;
        }
        
        // Check last character (checksum or X)
        $lastChar = substr($idCard, 17, 1);
        if (!ctype_digit($lastChar) && $lastChar !== 'X') {
            return false;
        }
        
        // Calculate checksum
        $weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
        $checkCodes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'];
        
        $sum = 0;
        for ($i = 0; $i < 17; $i++) {
            $sum += (int)$idCard[$i] * $weights[$i];
        }
        
        $expectedCheckCode = $checkCodes[$sum % 11];
        return $lastChar === $expectedCheckCode;
    }
    
    /**
     * Validate strong password
     * 
     * @param string|null $password Password to validate
     * @param int $minLength Minimum length (default: 8)
     * @param bool $requireUpper Require uppercase letter
     * @param bool $requireLower Require lowercase letter
     * @param bool $requireDigit Require digit
     * @param bool $requireSpecial Require special character
     * @return bool
     */
    public static function isStrongPassword(
        ?string $password,
        int $minLength = 8,
        bool $requireUpper = true,
        bool $requireLower = true,
        bool $requireDigit = true,
        bool $requireSpecial = true
    ): bool {
        if ($password === null || strlen($password) < $minLength) {
            return false;
        }
        
        if ($requireUpper && !preg_match('/[A-Z]/', $password)) {
            return false;
        }
        if ($requireLower && !preg_match('/[a-z]/', $password)) {
            return false;
        }
        if ($requireDigit && !preg_match('/\d/', $password)) {
            return false;
        }
        if ($requireSpecial && !preg_match('/[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]/', $password)) {
            return false;
        }
        
        return true;
    }
    
    /**
     * Validate username
     * 
     * @param string|null $username Username to validate
     * @param int $minLength Minimum length (default: 3)
     * @param int $maxLength Maximum length (default: 20)
     * @return bool
     */
    public static function isUsername(?string $username, int $minLength = 3, int $maxLength = 20): bool
    {
        if ($username === null || trim($username) === '') {
            return false;
        }
        $len = strlen($username);
        if ($len < $minLength || $len > $maxLength) {
            return false;
        }
        // Must start with letter, contain only letters, digits, underscores
        return preg_match('/^[a-zA-Z][a-zA-Z0-9_]*$/', $username) === 1;
    }
    
    /**
     * Validate date format
     * 
     * @param string|null $date Date string to validate
     * @param string $format Date format (default: Y-m-d)
     * @return bool
     */
    public static function isDate(?string $date, string $format = 'Y-m-d'): bool
    {
        if ($date === null || trim($date) === '') {
            return false;
        }
        $d = \DateTime::createFromFormat($format, $date);
        return $d && $d->format($format) === $date;
    }
    
    /**
     * Validate JSON string
     * 
     * @param string|null $json JSON string to validate
     * @return bool
     */
    public static function isJson(?string $json): bool
    {
        if ($json === null || trim($json) === '') {
            return false;
        }
        json_decode($json);
        return json_last_error() === JSON_ERROR_NONE;
    }
    
    /**
     * Check if value is in array (enum validation)
     * 
     * @param mixed $value Value to check
     * @param array $allowed Array of allowed values
     * @param bool $strict Strict type checking
     * @return bool
     */
    public static function isIn($value, array $allowed, bool $strict = false): bool
    {
        return in_array($value, $allowed, $strict);
    }
    
    /**
     * Check if array has required keys
     * 
     * @param array|null $array Array to check
     * @param array $required Required keys
     * @return bool
     */
    public static function hasRequiredKeys(?array $array, array $required): bool
    {
        if ($array === null) {
            return false;
        }
        foreach ($required as $key) {
            if (!array_key_exists($key, $array) || self::isEmpty($array[$key])) {
                return false;
            }
        }
        return true;
    }
    
    /**
     * Validate with custom rule and return result object
     * 
     * @param mixed $value Value to validate
     * @param callable $rule Validation function
     * @param string $field Field name
     * @param string $errorMessage Error message
     * @return ValidationResult
     */
    public static function validate($value, callable $rule, string $field = '', string $errorMessage = ''): ValidationResult
    {
        $isValid = $rule($value);
        if ($isValid) {
            return new ValidationResult(true, null, $field);
        }
        return new ValidationResult(false, $errorMessage ?: "Validation failed for {$field}", $field);
    }
    
    /**
     * Run multiple validations and return all results
     * 
     * @param array $validations Array of ['field' => name, 'value' => value, 'rule' => callable, 'message' => msg]
     * @return array Array of ValidationResult objects
     */
    public static function validateMultiple(array $validations): array
    {
        $results = [];
        foreach ($validations as $v) {
            $field = $v['field'] ?? '';
            $value = $v['value'] ?? null;
            $rule = $v['rule'];
            $message = $v['message'] ?? "Validation failed for {$field}";
            $results[] = self::validate($value, $rule, $field, $message);
        }
        return $results;
    }
    
    /**
     * Check if all validations passed
     * 
     * @param array $results Array of ValidationResult objects
     * @return bool
     */
    public static function allValid(array $results): bool
    {
        foreach ($results as $result) {
            if (!$result->isValid()) {
                return false;
            }
        }
        return true;
    }
    
    /**
     * Get first error from validation results
     * 
     * @param array $results Array of ValidationResult objects
     * @return string|null
     */
    public static function firstError(array $results): ?string
    {
        foreach ($results as $result) {
            if (!$result->isValid()) {
                return $result->getMessage();
            }
        }
        return null;
    }
    
    /**
     * Get all errors from validation results
     * 
     * @param array $results Array of ValidationResult objects
     * @return array
     */
    public static function allErrors(array $results): array
    {
        $errors = [];
        foreach ($results as $result) {
            if (!$result->isValid()) {
                $errors[] = [
                    'field' => $result->getField(),
                    'message' => $result->getMessage()
                ];
            }
        }
        return $errors;
    }
}
