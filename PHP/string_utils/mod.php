<?php
/**
 * StringUtils - PHP 字符串处理工具类
 * 
 * 提供常用字符串操作函数，无外部依赖，可直接复用
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

class StringUtils
{
    /**
     * 检查字符串是否为空或仅包含空白字符
     *
     * @param string|null $str 待检查的字符串
     * @return bool 如果字符串为null、空字符串或仅包含空白字符则返回true
     */
    public static function isBlank(?string $str): bool
    {
        return $str === null || trim($str) === '';
    }

    /**
     * 检查字符串是否非空
     *
     * @param string|null $str 待检查的字符串
     * @return bool 如果字符串不为null且trim后不为空则返回true
     */
    public static function isNotBlank(?string $str): bool
    {
        return !self::isBlank($str);
    }

    /**
     * 安全地截取字符串（支持多字节字符）
     *
     * @param string|null $str 原字符串
     * @param int $start 起始位置（从0开始）
     * @param int|null $length 截取长度，null表示截取到末尾
     * @param string $encoding 字符编码，默认UTF-8
     * @return string 截取后的字符串
     */
    public static function substring(?string $str, int $start, ?int $length = null, string $encoding = 'UTF-8'): string
    {
        if ($str === null) {
            return '';
        }
        
        if ($length === null) {
            return mb_substr($str, $start, null, $encoding);
        }
        
        return mb_substr($str, $start, $length, $encoding);
    }

    /**
     * 截取字符串并添加省略号（支持多字节字符）
     *
     * @param string|null $str 原字符串
     * @param int $maxLength 最大长度
     * @param string $suffix 截断后缀，默认"..."
     * @param string $encoding 字符编码，默认UTF-8
     * @return string 截取后的字符串
     */
    public static function truncate(?string $str, int $maxLength, string $suffix = '...', string $encoding = 'UTF-8'): string
    {
        if ($str === null || $maxLength <= 0) {
            return '';
        }
        
        $strLength = mb_strlen($str, $encoding);
        
        if ($strLength <= $maxLength) {
            return $str;
        }
        
        $suffixLength = mb_strlen($suffix, $encoding);
        $cutLength = max(0, $maxLength - $suffixLength);
        
        return mb_substr($str, 0, $cutLength, $encoding) . $suffix;
    }

    /**
     * 驼峰命名转下划线命名（snake_case）
     *
     * @param string|null $str 驼峰命名字符串
     * @return string 下划线命名字符串
     */
    public static function camelToSnake(?string $str): string
    {
        if ($str === null || $str === '') {
            return '';
        }
        
        return strtolower(preg_replace('/([a-z])([A-Z])/', '$1_$2', $str));
    }

    /**
     * 下划线命名转驼峰命名（camelCase）
     *
     * @param string|null $str 下划线命名字符串
     * @param bool $capitalizeFirst 是否首字母大写（PascalCase），默认false
     * @return string 驼峰命名字符串
     */
    public static function snakeToCamel(?string $str, bool $capitalizeFirst = false): string
    {
        if ($str === null || $str === '') {
            return '';
        }
        
        $str = str_replace('_', ' ', $str);
        $str = ucwords($str);
        $str = str_replace(' ', '', $str);
        
        if (!$capitalizeFirst) {
            $str = lcfirst($str);
        }
        
        return $str;
    }

    /**
     * 生成随机字符串
     *
     * Optimized: Validates charset, uses array for string building (faster concatenation).
     *
     * @param int $length 字符串长度
     * @param string $chars 可用字符集，默认包含大小写字母和数字
     * @return string 随机字符串
     */
    public static function random(int $length = 16, string $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'): string
    {
        if ($length <= 0) {
            return '';
        }
        
        $charsLength = strlen($chars);
        if ($charsLength === 0) {
            return '';
        }
        
        // Use array for efficient string building
        $result = [];
        $maxIndex = $charsLength - 1;
        
        for ($i = 0; $i < $length; $i++) {
            $result[] = $chars[random_int(0, $maxIndex)];
        }
        
        return implode('', $result);
    }

    /**
     * 检查字符串是否以指定前缀开头
     *
     * @param string|null $str 待检查的字符串
     * @param string $prefix 前缀
     * @param bool $ignoreCase 是否忽略大小写，默认false
     * @return bool 如果字符串以指定前缀开头则返回true
     */
    public static function startsWith(?string $str, string $prefix, bool $ignoreCase = false): bool
    {
        if ($str === null || $prefix === '') {
            return $prefix === '';
        }
        
        if ($ignoreCase) {
            return stripos($str, $prefix) === 0;
        }
        
        return strpos($str, $prefix) === 0;
    }

    /**
     * 检查字符串是否以指定后缀结尾
     *
     * @param string|null $str 待检查的字符串
     * @param string $suffix 后缀
     * @param bool $ignoreCase 是否忽略大小写，默认false
     * @return bool 如果字符串以指定后缀结尾则返回true
     */
    public static function endsWith(?string $str, string $suffix, bool $ignoreCase = false): bool
    {
        if ($str === null || $suffix === '') {
            return $suffix === '';
        }
        
        $suffixLength = strlen($suffix);
        $strLength = strlen($str);
        
        if ($suffixLength > $strLength) {
            return false;
        }
        
        if ($ignoreCase) {
            return strcasecmp(substr($str, -$suffixLength), $suffix) === 0;
        }
        
        return substr($str, -$suffixLength) === $suffix;
    }

    /**
     * 移除字符串前缀（如果存在）
     *
     * @param string|null $str 原字符串
     * @param string $prefix 要移除的前缀
     * @return string 处理后的字符串
     */
    public static function removePrefix(?string $str, string $prefix): string
    {
        if ($str === null || $prefix === '') {
            return $str ?? '';
        }
        
        if (strpos($str, $prefix) === 0) {
            return substr($str, strlen($prefix));
        }
        
        return $str;
    }

    /**
     * 移除字符串后缀（如果存在）
     *
     * @param string|null $str 原字符串
     * @param string $suffix 要移除的后缀
     * @return string 处理后的字符串
     */
    public static function removeSuffix(?string $str, string $suffix): string
    {
        if ($str === null || $suffix === '') {
            return $str ?? '';
        }
        
        $suffixLength = strlen($suffix);
        $strLength = strlen($str);
        
        if ($suffixLength > $strLength) {
            return $str;
        }
        
        if (substr($str, -$suffixLength) === $suffix) {
            return substr($str, 0, $strLength - $suffixLength);
        }
        
        return $str;
    }

    /**
     * 将字符串按行分割为数组
     *
     * @param string|null $str 原字符串
     * @param bool $trimEmpty 是否去除空行，默认true
     * @return array 字符串数组
     */
    public static function lines(?string $str, bool $trimEmpty = true): array
    {
        if ($str === null || $str === '') {
            return [];
        }
        
        $lines = preg_split('/\r\n|\r|\n/', $str);
        
        if ($trimEmpty) {
            $lines = array_filter($lines, function ($line) {
                return trim($line) !== '';
            });
        }
        
        return array_values($lines);
    }

    /**
     * 重复字符串指定次数
     *
     * @param string $str 原字符串
     * @param int $count 重复次数
     * @return string 重复后的字符串
     */
    public static function repeat(string $str, int $count): string
    {
        if ($count <= 0) {
            return '';
        }
        
        return str_repeat($str, $count);
    }

    /**
     * 填充字符串到指定长度
     *
     * @param string|null $str 原字符串
     * @param int $length 目标长度
     * @param string $padStr 填充字符，默认空格
     * @param int $padType 填充位置：STR_PAD_RIGHT(默认), STR_PAD_LEFT, STR_PAD_BOTH
     * @return string 填充后的字符串
     */
    public static function pad(?string $str, int $length, string $padStr = ' ', int $padType = STR_PAD_RIGHT): string
    {
        if ($str === null) {
            $str = '';
        }
        
        if ($length <= 0 || strlen($padStr) === 0) {
            return $str;
        }
        
        return str_pad($str, $length, $padStr, $padType);
    }

    /**
     * 反转字符串（支持多字节字符）
     *
     * Optimized: Uses mb_substr loop for better memory efficiency with large strings.
     *
     * @param string|null $str 原字符串
     * @param string $encoding 字符编码，默认UTF-8
     * @return string 反转后的字符串
     */
    public static function reverse(?string $str, string $encoding = 'UTF-8'): string
    {
        if ($str === null || $str === '') {
            return '';
        }
        
        // Use mb_str_split if available (PHP 7.4+), fallback to manual iteration
        if (function_exists('mb_str_split')) {
            $chars = mb_str_split($str, 1, $encoding);
            return implode('', array_reverse($chars));
        }
        
        // Fallback for older PHP versions
        $length = mb_strlen($str, $encoding);
        $result = '';
        for ($i = $length - 1; $i >= 0; $i--) {
            $result .= mb_substr($str, $i, 1, $encoding);
        }
        return $result;
    }

    /**
     * 计算字符串在终端显示宽度（处理中英文混排）
     *
     * Optimized: Uses cached regex pattern and single-pass calculation.
     * CJK characters (East Asian Wide) count as 2, others as 1.
     *
     * @param string|null $str 原字符串
     * @param string $encoding 字符编码，默认UTF-8
     * @return int 显示宽度（ASCII字符计1，中文等宽字符计2）
     */
    public static function displayWidth(?string $str, string $encoding = 'UTF-8'): int
    {
        if ($str === null || $str === '') {
            return 0;
        }
        
        // Use static cache for regex pattern to avoid recompilation
        static $cjkPattern = null;
        if ($cjkPattern === null) {
            // CJK Unified Ideographs + Extensions + Fullwidth forms
            $cjkPattern = '/[' .
                '\x{4e00}-\x{9fff}' .      // CJK Unified Ideographs
                '\x{3400}-\x{4dbf}' .      // CJK Extension A
                '\x{20000}-\x{2a6df}' .    // CJK Extension B
                '\x{2a700}-\x{2b73f}' .    // CJK Extension C
                '\x{2b740}-\x{2b81f}' .    // CJK Extension D
                '\x{2b820}-\x{2ceaf}' .    // CJK Extension E
                '\x{3000}-\x{303f}' .      // CJK Symbols and Punctuation
                '\x{ff00}-\x{ffef}' .      // Halfwidth/Fullwidth Forms
                '\x{ac00}-\x{d7af}' .      // Hangul Syllables
                '\x{3040}-\x{309f}' .      // Hiragana
                '\x{30a0}-\x{30ff}' .      // Katakana
                ']/u';
        }
        
        $width = 0;
        $length = mb_strlen($str, $encoding);
        
        // Single-pass calculation with early termination for ASCII-only strings
        $isAsciiOnly = true;
        for ($i = 0; $i < $length; $i++) {
            $char = mb_substr($str, $i, 1, $encoding);
            $ord = mb_ord($char, $encoding);
            
            // Fast path: ASCII characters (0x00-0x7F) are always width 1
            if ($ord !== false && $ord < 0x80) {
                $width += 1;
                continue;
            }
            
            $isAsciiOnly = false;
            
            // Check for CJK and fullwidth characters using cached pattern
            if (preg_match($cjkPattern, $char)) {
                $width += 2;
            } else {
                $width += 1;
            }
        }
        
        return $width;
    }

    /**
     * 将字符串首字母大写（支持多字节字符）
     *
     * @param string|null $str 原字符串
     * @param string $encoding 字符编码，默认UTF-8
     * @return string 首字母大写的字符串
     */
    public static function capitalize(?string $str, string $encoding = 'UTF-8'): string
    {
        if ($str === null || $str === '') {
            return '';
        }
        
        $firstChar = mb_substr($str, 0, 1, $encoding);
        $rest = mb_substr($str, 1, null, $encoding);
        
        return mb_strtoupper($firstChar, $encoding) . $rest;
    }

    /**
     * 将字符串首字母小写（支持多字节字符）
     *
     * @param string|null $str 原字符串
     * @param string $encoding 字符编码，默认UTF-8
     * @return string 首字母小写的字符串
     */
    public static function uncapitalize(?string $str, string $encoding = 'UTF-8'): string
    {
        if ($str === null || $str === '') {
            return '';
        }
        
        $firstChar = mb_substr($str, 0, 1, $encoding);
        $rest = mb_substr($str, 1, null, $encoding);
        
        return mb_strtolower($firstChar, $encoding) . $rest;
    }

    /**
     * 计算子字符串出现次数
     *
     * @param string|null $str 原字符串
     * @param string $sub 子字符串
     * @param bool $ignoreCase 是否忽略大小写，默认false
     * @return int 出现次数
     */
    public static function count(?string $str, string $sub, bool $ignoreCase = false): int
    {
        if ($str === null || $sub === '') {
            return 0;
        }
        
        if ($ignoreCase) {
            $str = strtolower($str);
            $sub = strtolower($sub);
        }
        
        return substr_count($str, $sub);
    }

    /**
     * 安全地比较两个字符串
     *
     * @param string|null $str1 第一个字符串
     * @param string|null $str2 第二个字符串
     * @param bool $ignoreCase 是否忽略大小写，默认false
     * @return bool 如果相等则返回true
     */
    public static function equals(?string $str1, ?string $str2, bool $ignoreCase = false): bool
    {
        if ($str1 === null || $str2 === null) {
            return $str1 === $str2;
        }
        
        if ($ignoreCase) {
            return strcasecmp($str1, $str2) === 0;
        }
        
        return strcmp($str1, $str2) === 0;
    }

    /**
     * 将字符串转换为URL友好的slug
     *
     * @param string|null $str 原字符串
     * @param string $separator 分隔符，默认"-"
     * @return string slug字符串
     */
    public static function slug(?string $str, string $separator = '-'): string
    {
        if ($str === null || $str === '') {
            return '';
        }
        
        // 转换为小写
        $str = strtolower($str);
        
        // 替换非字母数字字符为分隔符
        $str = preg_replace('/[^a-z0-9]+/', $separator, $str);
        
        // 移除首尾分隔符
        $str = trim($str, $separator);
        
        // 合并连续的分隔符
        $str = preg_replace('/' . preg_quote($separator, '/') . '+/', $separator, $str);
        
        return $str;
    }
}
