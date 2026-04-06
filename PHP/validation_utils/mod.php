<?php
/**
 * AllToolkit - PHP Validation Utilities
 * 
 * 一个全面的验证工具模块，提供各种数据验证功能。
 * 零依赖，仅使用 PHP 标准库。
 * 
 * @package AllToolkit\ValidationUtils
 * @version 1.0.0
 * @license MIT
 */

namespace AllToolkit;

/**
 * ValidationUtils 类 - 提供各种数据验证功能
 * 
 * 包含：基本验证、邮箱验证、手机号验证、IP地址验证、
 * URL验证、身份证号验证、信用卡验证、UUID验证、
 * 密码强度验证等。
 */
class ValidationUtils {
    
    // ==================== 基本验证 ====================
    
    /**
     * 检查字符串是否为空或 null
     * 
     * @param mixed $str 要检查的字符串
     * @return bool 如果为 null、空字符串或仅包含空白字符则返回 true
     */
    public static function isEmpty($str): bool {
        if ($str === null) return true;
        if (!is_string($str)) return empty($str);
        return trim($str) === '';
    }
    
    /**
     * 检查字符串是否不为空
     * 
     * @param mixed $str 要检查的字符串
     * @return bool 如果不为空则返回 true
     */
    public static function isNotEmpty($str): bool {
        return !self::isEmpty($str);
    }
    
    /**
     * 检查字符串是否为空白字符（包括 null）
     * 
     * @param mixed $str 要检查的字符串
     * @return bool 如果为 null、空字符串或仅包含空白字符则返回 true
     */
    public static function isBlank($str): bool {
        return self::isEmpty($str);
    }
    
    /**
     * 检查字符串是否不为空白字符
     * 
     * @param mixed $str 要检查的字符串
     * @return bool 如果不为空白则返回 true
     */
    public static function isNotBlank($str): bool {
        return !self::isBlank($str);
    }
    
    // ==================== 邮箱验证 ====================
    
    /**
     * 验证邮箱格式（符合 RFC 5322）
     * 
     * @param string $email 邮箱地址
     * @return bool 如果格式有效则返回 true
     */
    public static function isEmail(string $email): bool {
        if (self::isEmpty($email)) return false;
        return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
    }
    
    /**
     * 验证邮箱格式（严格模式）
     * 检查常见错误：连续点号、无效域名等
     * 
     * @param string $email 邮箱地址
     * @return bool 如果格式有效则返回 true
     */
    public static function isEmailStrict(string $email): bool {
        if (!self::isEmail($email)) return false;
        
        // 检查连续点号
        if (strpos($email, '..') !== false) return false;
        
        // 检查本地部分和域名
        $parts = explode('@', $email);
        if (count($parts) !== 2) return false;
        
        $local = $parts[0];
        $domain = $parts[1];
        
        // 本地部分不能以点开头或结尾
        if (str_starts_with($local, '.') || str_ends_with($local, '.')) return false;
        
        // 检查域名是否有有效 TLD
        if (!str_contains($domain, '.')) return false;
        
        // 检查域名部分
        $domainParts = explode('.', $domain);
        foreach ($domainParts as $part) {
            if (empty($part)) return false;
            // 域名部分不能以连字符开头或结尾
            if (str_starts_with($part, '-') || str_ends_with($part, '-')) return false;
        }
        
        return true;
    }
    
    // ==================== 手机号验证 ====================
    
    /**
     * 验证中国大陆手机号
     * 11位数字，以 1 开头，第二位为 3-9
     * 
     * @param string $phone 手机号
     * @return bool 如果格式有效则返回 true
     */
    public static function isChinaMobile(string $phone): bool {
        if (self::isEmpty($phone)) return false;
        // 移除所有非数字字符
        $phone = preg_replace('/\D/', '', $phone);
        return preg_match('/^1[3-9]\d{9}$/', $phone) === 1;
    }
    
    /**
     * 验证国际手机号（E.164 格式）
     * 以 + 开头，后跟国家代码和号码
     * 
     * @param string $phone 手机号
     * @return bool 如果格式有效则返回 true
     */
    public static function isInternationalPhone(string $phone): bool {
        if (self::isEmpty($phone)) return false;
        // E.164 格式: +[国家代码][号码]，最多15位
        return preg_match('/^\+[1-9]\d{1,14}$/', $phone) === 1;
    }
    
    // ==================== IP 地址验证 ====================
    
    /**
     * 验证 IPv4 地址
     * 
     * @param string $ip IP 地址
     * @return bool 如果格式有效则返回 true
     */
    public static function isIpv4(string $ip): bool {
        if (self::isEmpty($ip)) return false;
        return filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4) !== false;
    }
    
    /**
     * 验证 IPv6 地址
     * 
     * @param string $ip IP 地址
     * @return bool 如果格式有效则返回 true
     */
    public static function isIpv6(string $ip): bool {
        if (self::isEmpty($ip)) return false;
        return filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6) !== false;
    }
    
    /**
     * 验证 IP 地址（IPv4 或 IPv6）
     * 
     * @param string $ip IP 地址
     * @return bool 如果格式有效则返回 true
     */
    public static function isIp(string $ip): bool {
        if (self::isEmpty($ip)) return false;
        return filter_var($ip, FILTER_VALIDATE_IP) !== false;
    }
    
    /**
     * 验证是否为私有 IP 地址
     * 
     * @param string $ip IP 地址
     * @return bool 如果是私有 IP 则返回 true
     */
    public static function isPrivateIp(string $ip): bool {
        if (!self::isIp($ip)) return false;
        return filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE) === false;
    }
    
    // ==================== URL 验证 ====================
    
    /**
     * 验证 URL 格式
     * 
     * @param string $url URL 字符串
     * @return bool 如果格式有效则返回 true
     */
    public static function isUrl(string $url): bool {
        if (self::isEmpty($url)) return false;
        return filter_var($url, FILTER_VALIDATE_URL) !== false;
    }
    
    /**
     * 验证 HTTP/HTTPS URL
     * 
     * @param string $url URL 字符串
     * @return bool 如果是有效的 HTTP(S) URL 则返回 true
     */
    public static function isHttpUrl(string $url): bool {
        if (!self::isUrl($url)) return false;
        $scheme = parse_url($url, PHP_URL_SCHEME);
        return in_array($scheme, ['http', 'https'], true);
    }
    
    // ==================== 身份证号验证 ====================
    
    /**
     * 验证中国大陆身份证号（15位或18位）
     * 18位身份证包含校验码验证
     * 
     * @param string $idCard 身份证号
     * @return bool 如果格式有效则返回 true
     */
    public static function isChinaIdCard(string $idCard): bool {
        if (self::isEmpty($idCard)) return false;
        
        $idCard = strtoupper(trim($idCard));
        $len = strlen($idCard);
        
        if ($len === 15) {
            // 15位身份证：纯数字
            return preg_match('/^\d{15}$/', $idCard) === 1;
        } elseif ($len === 18) {
            // 18位身份证：前17位数字，最后一位数字或X
            if (!preg_match('/^\d{17}[\dX]$/', $idCard)) return false;
            
            // 校验码验证
            $weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
            $checkCodes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'];
            
            $sum = 0;
            for ($i = 0; $i < 17; $i++) {
                $sum += intval($idCard[$i]) * $weights[$i];
            }
            
            $checkCode = $checkCodes[$sum % 11];
            return $idCard[17] === $checkCode;
        }
        
        return false;
    }
    
    // ==================== 信用卡验证 ====================
    
    /**
     * 验证信用卡号（使用 Luhn 算法）
     * 
     * @param string $cardNumber 信用卡号
     * @return bool 如果格式有效则返回 true
     */
    public static function isCreditCard(string $cardNumber): bool {
        if (self::isEmpty($cardNumber)) return false;
        
        // 移除空格和连字符
        $cardNumber = preg_replace('/[\s-]/', '', $cardNumber);
        
        // 必须是13-19位数字
        if (!preg_match('/^\d{13,19}$/', $cardNumber)) return false;
        
        // Luhn 算法
        $sum = 0;
        $alternate = false;
        
        for ($i = strlen($cardNumber) - 1; $i >= 0; $i--) {
            $n = intval($cardNumber[$i]);
            if ($alternate) {
                $n *= 2;
                if ($n > 9) $n -= 9;
            }
            $sum += $n;
            $alternate = !$alternate;
        }
        
        return $sum % 10 === 0;
    }
    
    // ==================== UUID 验证 ====================
    
    /**
     * 验证 UUID 格式
     * 支持标准格式：8-4-4-4-12
     * 
     * @param string $uuid UUID 字符串
     * @return bool 如果格式有效则返回 true
     */
    public static function isUuid(string $uuid): bool {
        if (self::isEmpty($uuid)) return false;
        return preg_match('/^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/', $uuid) === 1;
    }
    
    /**
     * 验证 UUID v4 格式
     * 
     * @param string $uuid UUID 字符串
     * @return bool 如果是有效的 UUID v4 则返回 true
     */
    public static function isUuidV4(string $uuid): bool {
        if (!self::isUuid($uuid)) return false;
        // UUID v4: 第3部分的第一个字符必须是 4
        $parts = explode('-', $uuid);
        return strlen($parts[2]) === 4 && $parts[2][0] === '4';
    }
    
    /**
     * 验证简化 UUID（无连字符）
     * 
     * @param string $uuid UUID 字符串
     * @return bool 如果格式有效则返回 true
     */
    public static function isUuidSimple(string $uuid): bool {
        if (self::isEmpty($uuid)) return false;
        return preg_match('/^[0-9a-fA-F]{32}$/', $uuid) === 1;
    }
    
    // ==================== 密码强度验证 ====================
    
    /**
     * 验证强密码
     * 要求：至少8位，包含大写字母、小写字母、数字和特殊字符
     * 
     * @param string $password 密码
     * @param int $minLength 最小长度（默认8）
     * @return bool 如果符合要求则返回 true
     */
    public static function isStrongPassword(string $password, int $minLength = 8): bool {
        if (strlen($password) < $minLength) return false;
        
        // 包含小写字母
        if (!preg_match('/[a-z]/', $password)) return false;
        // 包含大写字母
        if (!preg_match('/[A-Z]/', $password)) return false;
        // 包含数字
        if (!preg_match('/\d/', $password)) return false;
        // 包含特殊字符
        if (!preg_match('/[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]/', $password)) return false;
        
        return true;
    }
    
    /**
     * 验证中等强度密码
     * 要求：至少6位，包含字母和数字
     * 
     * @param string $password 密码
     * @param int $minLength 最小长度（默认6）
     * @return bool 如果符合要求则返回 true
     */
    public static function isMediumPassword(string $password, int $minLength = 6): bool {
        if (strlen($password) < $minLength) return false;
        
        // 包含字母
        if (!preg_match('/[a-zA-Z]/', $password)) return false;
        // 包含数字
        if (!preg_match('/\d/', $password)) return false;
        
        return true;
    }
    
    /**
     * 获取密码强度评分（0-100）
     * 
     * @param string $password 密码
     * @return int 强度评分
     */
    public static function getPasswordStrength(string $password): int {
        $score = 0;
        $length = strlen($password);
        
        // 长度评分
        if ($length >= 8) $score += 20;
        if ($length >= 12) $score += 10;
        if ($length >= 16) $score += 10;
        
        // 包含小写字母
        if (preg_match('/[a-z]/', $password)) $score += 10;
        // 包含大写字母
        if (preg_match('/[A-Z]/', $password)) $score += 10;
        // 包含数字
        if (preg_match('/\d/', $password)) $score += 10;
        // 包含特殊字符
        if (preg_match('/[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]/', $password)) $score += 20;
        // 包含多种字符类型
        $types = 0;
        if (preg_match('/[a-z]/', $password)) $types++;
        if (preg_match('/[A-Z]/', $password)) $types++;
        if (preg_match('/\d/', $password)) $types++;
        if (preg_match('/[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]/', $password)) $types++;
        if ($types >= 4) $score += 10;
        
        return min($score, 100);
    }
    
    // ==================== 用户名验证 ====================
    
    /**
     * 验证用户名
     * 要求：字母开头，3-20位，只允许字母、数字、下划线
     * 
     * @param string $username 用户名
     * @param int $minLength 最小长度（默认3）
     * @param int $maxLength 最大长度（默认20）
     * @return bool 如果格式有效则返回 true
     */
    public static function isUsername(string $username, int $minLength = 3, int $maxLength = 20): bool {
        if (self::isEmpty($username)) return false;
        $len = strlen($username);
        if ($len < $minLength || $len > $maxLength) return false;
        return preg_match('/^[a-zA-Z][a-zA-Z0-9_]*$/', $username) === 1;
    }
    
    // ==================== 颜色验证 ====================
    
    /**
     * 验证十六进制颜色代码
     * 支持 #RGB 和 #RRGGBB 格式
     * 
     * @param string $color 颜色代码
     * @return bool 如果格式有效则返回 true
     */
    public static function isHexColor(string $color): bool {
        if (self::isEmpty($color)) return false;
        return preg_match('/^#([0-9a-fA-F]{3}){1,2}$/', $color) === 1;
    }
    
    /**
     * 验证 RGB 颜色值
     * 
     * @param int $r 红色值 (0-255)
     * @param int $g 绿色值 (0-255)
     * @param int $b 蓝色值 (0-255)
     * @return bool 如果值有效则返回 true
     */
    public static function isRgbColor(int $r, int $g, int $b): bool {
        return $r >= 0 && $r <= 255 && $g >= 0 && $g <= 255 && $b >= 0 && $b <= 255;
    }
    
    // ==================== 日期时间验证 ====================
    
    /**
     * 验证日期格式
     * 
     * @param string $date 日期字符串
     * @param string $format 日期格式（默认 Y-m-d）
     * @return bool 如果格式有效则返回 true
     */
    public static function isDate(string $date, string $format = 'Y-m-d'): bool {
        if (self::isEmpty($date)) return false;
        $d = \DateTime::createFromFormat($format, $date);
        return $d && $d->format($format) === $date;
    }
    
    /**
     * 验证时间格式
     * 
     * @param string $time 时间字符串
     * @param string $format 时间格式（默认 H:i:s）
     * @return bool 如果格式有效则返回 true
     */
    public static function isTime(string $time, string $format = 'H:i:s'): bool {
        return self::isDate($time, $format);
    }
    
    /**
     * 验证日期时间格式
     * 
     * @param string $datetime 日期时间字符串
     * @param string $format 格式（默认 Y-m-d H:i:s）
     * @return bool 如果格式有效则返回 true
     */
    public static function isDateTime(string $datetime, string $format = 'Y-m-d H:i:s'): bool {
        return self::isDate($datetime, $format);
    }
    
    // ==================== 数字验证 ====================
    
    /**
     * 检查是否为数字（整数或浮点数）
     * 
     * @param mixed $value 要检查的值
     * @return bool 如果是数字则返回 true
     */
    public static function isNumeric($value): bool {
        return is_numeric($value);
    }
    
    /**
     * 检查是否为整数
     * 
     * @param mixed $value 要检查的值
     * @return bool 如果是整数则返回 true
     */
    public static function isInteger($value): bool {
        return is_int($value) || (is_string($value) && preg_match('/^-?\d+$/', $value) === 1);
    }
    
    /**
     * 检查是否为正整数
     * 
     * @param mixed $value 要检查的值
     * @return bool 如果是正整数则返回 true
     */
    public static function isPositiveInteger($value): bool {
        return self::isInteger($value) && intval($value) > 0;
    }
    
    /**
     * 检查值是否在范围内
     * 
     * @param int|float $value 要检查的值
     * @param int|float $min 最小值
     * @param int|float $max 最大值
     * @return bool 如果在范围内则返回 true
     */
    public static function inRange($value, $min, $max): bool {
        return $value >= $min && $value <= $max;
    }
    
    // ==================== 字符串验证 ====================
    
    /**
     * 检查字符串长度是否在范围内
     * 
     * @param string $str 字符串
     * @param int $min 最小长度
     * @param int|null $max 最大长度（null表示无限制）
     * @return bool 如果长度在范围内则返回 true
     */
    public static function lengthBetween(string $str, int $min, ?int $max = null): bool {
        $len = strlen($str);
        if ($len < $min) return false;
        if ($max !== null && $len > $max) return false;
        return true;
    }
    
    /**
     * 检查字符串是否只包含字母
     * 
     * @param string $str 字符串
     * @return