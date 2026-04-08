<?php
/**
 * AllToolkit - Encoding Utilities for PHP
 *
 * A comprehensive encoding and charset conversion utility module for PHP
 * providing UTF-8, GBK, GB2312, Big5, ISO-8859-1 conversions, Base64, URL encoding,
 * HTML entities, and various text encoding operations with zero dependencies.
 *
 * @package AllToolkit\EncodingUtils
 * @version 1.0.0
 * @license MIT
 */

namespace AllToolkit;

/**
 * EncodingUtils class providing comprehensive encoding and charset conversion utilities
 */
class EncodingUtils
{
    /** @var array Supported character encodings */
    private static $supportedEncodings = [
        'UTF-8', 'GBK', 'GB2312', 'GB18030', 'BIG5',
        'ISO-8859-1', 'ISO-8859-2', 'ISO-8859-15',
        'WINDOWS-1251', 'WINDOWS-1252', 'ASCII',
        'EUC-JP', 'SJIS', 'EUC-KR',
        'UCS-2', 'UCS-2BE', 'UCS-2LE', 'UCS-4',
    ];

    /** @var string Default encoding */
    private static $defaultEncoding = 'UTF-8';

    /**
     * Convert string encoding
     *
     * @param string $str The string to convert
     * @param string $toEncoding Target encoding
     * @param string|null $fromEncoding Source encoding (auto-detect if null)
     * @return string|false Converted string or false on failure
     */
    public static function convert($str, $toEncoding, $fromEncoding = null)
    {
        if ($str === null || $str === '') {
            return $str;
        }

        $toEncoding = self::normalizeEncoding($toEncoding);

        if ($fromEncoding === null) {
            $fromEncoding = self::detectEncoding($str);
        } else {
            $fromEncoding = self::normalizeEncoding($fromEncoding);
        }

        if (strcasecmp($fromEncoding, $toEncoding) === 0) {
            return $str;
        }

        $result = @mb_convert_encoding($str, $toEncoding, $fromEncoding);

        if ($result === false && function_exists('iconv')) {
            $result = @iconv($fromEncoding, $toEncoding . '//IGNORE', $str);
        }

        return $result !== false ? $result : $str;
    }

    /**
     * Convert string to UTF-8
     *
     * @param string $str The string to convert
     * @param string|null $fromEncoding Source encoding (auto-detect if null)
     * @return string|false Converted string or false on failure
     */
    public static function toUtf8($str, $fromEncoding = null)
    {
        return self::convert($str, 'UTF-8', $fromEncoding);
    }

    /**
     * Convert string from UTF-8 to another encoding
     *
     * @param string $str The string to convert
     * @param string $toEncoding Target encoding
     * @return string|false Converted string or false on failure
     */
    public static function fromUtf8($str, $toEncoding)
    {
        return self::convert($str, $toEncoding, 'UTF-8');
    }

    /**
     * Convert string to GBK encoding
     *
     * @param string $str The string to convert
     * @param string|null $fromEncoding Source encoding (auto-detect if null)
     * @return string|false Converted string or false on failure
     */
    public static function toGbk($str, $fromEncoding = null)
    {
        return self::convert($str, 'GBK', $fromEncoding);
    }

    /**
     * Convert string from GBK to UTF-8
     *
     * @param string $str The string to convert
     * @return string|false Converted string or false on failure
     */
    public static function gbkToUtf8($str)
    {
        return self::convert($str, 'UTF-8', 'GBK');
    }

    /**
     * Convert string to GB2312 encoding
     *
     * @param string $str The string to convert
     * @param string|null $fromEncoding Source encoding (auto-detect if null)
     * @return string|false Converted string or false on failure
     */
    public static function toGb2312($str, $fromEncoding = null)
    {
        return self::convert($str, 'GB2312', $fromEncoding);
    }

    /**
     * Convert string from GB2312 to UTF-8
     *
     * @param string $str The string to convert
     * @return string|false Converted string or false on failure
     */
    public static function gb2312ToUtf8($str)
    {
        return self::convert($str, 'UTF-8', 'GB2312');
    }

    /**
     * Convert string to Big5 encoding
     *
     * @param string $str The string to convert
     * @param string|null $fromEncoding Source encoding (auto-detect if null)
     * @return string|false Converted string or false on failure
     */
    public static function toBig5($str, $fromEncoding = null)
    {
        return self::convert($str, 'BIG5', $fromEncoding);
    }

    /**
     * Convert string from Big5 to UTF-8
     *
     * @param string $str The string to convert
     * @return string|false Converted string or false on failure
     */
    public static function big5ToUtf8($str)
    {
        return self::convert($str, 'UTF-8', 'BIG5');
    }

    /**
     * Convert string to ISO-8859-1 encoding
     *
     * @param string $str The string to convert
     * @param string|null $fromEncoding Source encoding (auto-detect if null)
     * @return string|false Converted string or false on failure
     */
    public static function toIso88591($str, $fromEncoding = null)
    {
        return self::convert($str, 'ISO-8859-1', $fromEncoding);
    }

    /**
     * Convert string from ISO-8859-1 to UTF-8
     *
     * @param string $str The string to convert
     * @return string|false Converted string or false on failure
     */
    public static function iso88591ToUtf8($str)
    {
        return self::convert($str, 'UTF-8', 'ISO-8859-1');
    }

    /**
     * Detect string encoding
     *
     * @param string $str The string to detect
     * @param array|null $encodings List of encodings to check (null for all supported)
     * @return string Detected encoding name
     */
    public static function detectEncoding($str, $encodings = null)
    {
        if ($str === null || $str === '') {
            return self::$defaultEncoding;
        }

        if ($encodings === null) {
            $encodings = self::$supportedEncodings;
        }

        $detected = @mb_detect_encoding($str, $encodings, true);

        return $detected !== false ? $detected : self::$defaultEncoding;
    }

    /**
     * Check if string is valid UTF-8
     *
     * @param string $str The string to check
     * @return bool True if valid UTF-8
     */
    public static function isUtf8($str)
    {
        if ($str === null || $str === '') {
            return true;
        }

        return @mb_check_encoding($str, 'UTF-8');
    }

    /**
     * Check if string is valid in specified encoding
     *
     * @param string $str The string to check
     * @param string $encoding The encoding to check against
     * @return bool True if valid
     */
    public static function isValidEncoding($str, $encoding)
    {
        if ($str === null || $str === '') {
            return true;
        }

        $encoding = self::normalizeEncoding($encoding);
        return @mb_check_encoding($str, $encoding);
    }

    /**
     * Get list of supported encodings
     *
     * @return array List of supported encoding names
     */
    public static function getSupportedEncodings()
    {
        return self::$supportedEncodings;
    }

    /**
     * Check if encoding is supported
     *
     * @param string $encoding The encoding to check
     * @return bool True if supported
     */
    public static function isSupportedEncoding($encoding)
    {
        $encoding = self::normalizeEncoding($encoding);
        return in_array($encoding, self::$supportedEncodings, true);
    }

    /**
     * Encode string to Base64
     *
     * @param string $str The string to encode
     * @param string $encoding Character encoding of input string (default: UTF-8)
     * @return string Base64 encoded string
     */
    public static function base64Encode($str, $encoding = 'UTF-8')
    {
        if ($str === null || $str === '') {
            return '';
        }

        $encoding = self::normalizeEncoding($encoding);
        $bytes = $encoding === 'UTF-8' ? $str : self::convert($str, 'UTF-8', $encoding);

        return base64_encode($bytes);
    }

    /**
     * Decode Base64 string
     *
     * @param string $base64 The Base64 string to decode
     * @param string $encoding Character encoding of output string (default: UTF-8)
     * @return string|false Decoded string or false on failure
     */
    public static function base64Decode($base64, $encoding = 'UTF-8')
    {
        if ($base64 === null || $base64 === '') {
            return '';
        }

        $decoded = base64_decode($base64, true);

        if ($decoded === false) {
            return false;
        }

        $encoding = self::normalizeEncoding($encoding);
        if ($encoding !== 'UTF-8') {
            $decoded = self::convert($decoded, $encoding, 'UTF-8');
        }

        return $decoded;
    }

    /**
     * Encode string to URL-safe Base64 (RFC 4648)
     *
     * @param string $str The string to encode
     * @param bool $padding Include padding (default: true)
     * @param string $encoding Character encoding of input string (default: UTF-8)
     * @return string URL-safe Base64 encoded string
     */
    public static function base64UrlEncode($str, $padding = true, $encoding = 'UTF-8')
    {
        $base64 = self::base64Encode($str, $encoding);
        $base64 = strtr($base64, '+/', '-_');

        if (!$padding) {
            $base64 = rtrim($base64, '=');
        }

        return $base64;
    }

    /**
     * Decode URL-safe Base64 string
     *
     * @param string $base64Url The URL-safe Base64 string to decode
     * @param string $encoding Character encoding of output string (default: UTF-8)
     * @return string|false Decoded string or false on failure
     */
    public static function base64UrlDecode($base64Url, $encoding = 'UTF-8')
    {
        if ($base64Url === null || $base64Url === '') {
            return '';
        }

        $base64 = strtr($base64Url, '-_', '+/');

        $padding = 4 - (strlen($base64) % 4);
        if ($padding !== 4) {
            $base64 .= str_repeat('=', $padding);
        }

        return self::base64Decode($base64, $encoding);
    }

    /**
     * URL encode a string
     *
     * @param string $str The string to encode
     * @param string $encoding Character encoding (default: UTF-8)
     * @return string URL encoded string
     */
    public static function urlEncode($str, $encoding = 'UTF-8')
    {
        if ($str === null || $str === '') {
            return '';
        }

        $encoding = self::normalizeEncoding($encoding);
        if ($encoding !== 'UTF-8') {
            $str = self::toUtf8($str, $encoding);
        }

        return urlencode($str);
    }

    /**
     * URL decode a string
     *
     * @param string $str The URL encoded string to decode
     * @param string $encoding Character encoding of output string (default: UTF-8)
     * @return string URL decoded string
     */
    public static function urlDecode($str, $encoding = 'UTF-8')
    {
        if ($str === null || $str === '') {
            return '';
        }

        $decoded = urldecode($str);

        $encoding = self::normalizeEncoding($encoding);
        if ($encoding !== 'UTF-8') {
            $decoded = self::convert($decoded, $encoding, 'UTF-8');
        }

        return $decoded;
    }

    /**
     * Raw URL encode (RFC 3986)
     *
     * @param string $str The string to encode
     * @param string $encoding Character encoding (default: UTF-8)
     * @return string Raw URL encoded string
     */
    public static function rawUrlEncode($str, $encoding = 'UTF-8')
    {
        if ($str === null || $str === '') {
            return '';
        }

        $encoding = self::normalizeEncoding($encoding);
        if ($encoding !== 'UTF-8') {
            $str = self::toUtf8($str, $encoding);
        }

        return rawurlencode($str);
    }

    /**
     * Raw URL decode (RFC 3986)
     *
     * @param string $str The raw URL encoded string to decode
     * @param string $encoding Character encoding of output string (default: UTF-8)
     * @return string Raw URL decoded string
     */
    public static function rawUrlDecode($str, $encoding = 'UTF-8')
    {
        if ($str === null || $str === '') {
            return '';
        }

        $decoded = rawurldecode($str);

        $encoding = self::normalizeEncoding($encoding);
        if ($encoding !== 'UTF-8') {
            $decoded = self::convert($decoded, $encoding, 'UTF-8');
        }

        return $decoded;
    }

    /**
     * Encode special characters to HTML entities
     *
     * @param string $str The string to encode
     * @param int $flags HTML entities flags (default: ENT_QUOTES | ENT_HTML5)
     * @param string $encoding Character encoding (default: UTF-8)
     * @return string HTML encoded string
     */
    public static function htmlEncode($str, $flags = null, $encoding = 'UTF-8')
    {
        if ($str === null || $str === '') {
            return '';
        }

        if ($flags === null) {
            $flags = ENT_QUOTES | ENT_HTML5;
        }

        $encoding = self::normalizeEncoding($encoding);

        return htmlentities($str, $flags, $encoding);
    }

    /**
     * Decode HTML entities to characters
     *
     * @param string $str The HTML encoded string to decode
     * @param int $flags HTML entities flags (default: ENT_QUOTES | ENT_HTML5)
     * @param string $encoding Character encoding (default: UTF-8)
     * @return string HTML decoded string
     */
    public static function htmlDecode($str, $flags = null, $encoding = 'UTF-8')
    {
        if ($str === null || $str === '') {
            return '';
        }

        if ($flags === null) {
            $flags = ENT_QUOTES | ENT_HTML5;
        }

        $encoding = self::normalizeEncoding($encoding);

        return html_entity_decode($str, $flags, $encoding);
    }

    /**
     * Encode special characters to HTML special chars
     *
     * @param string $str The string to encode
     * @param int $flags HTML special chars flags (default: ENT_QUOTES | ENT_HTML5)
     * @param string $encoding Character encoding (default: UTF-8)
     * @return string HTML special chars encoded string
     */
    public static function htmlSpecialCharsEncode($str, $flags = null, $encoding = 'UTF-8')
    {
        if ($str === null || $str === '') {
            return '';
        }

        if ($flags === null) {
            $flags = ENT_QUOTES | ENT_HTML5;
        }

        $encoding = self::normalizeEncoding($encoding);

        return htmlspecialchars($str, $flags, $encoding);
    }

    /**
     * Decode HTML special chars
     *
     * @param string $str The HTML special chars encoded string to decode
     * @param int $flags HTML special chars flags (default: ENT_QUOTES | ENT_HTML5)
     * @param string $encoding Character encoding (default: UTF-8)
     * @return string HTML special chars decoded string
     */
    public static function htmlSpecialCharsDecode($str, $flags = null, $encoding = 'UTF-8')
    {
        if ($str === null || $str === '') {
            return '';
        }

        if ($flags === null) {
            $flags = ENT_QUOTES | ENT_HTML5;
        }

        $encoding = self::normalizeEncoding($encoding);

        return htmlspecialchars_decode($str, $flags);
    }

    /**
     * Convert string to hexadecimal representation
     *
     * @param string $str The string to convert
     * @param string $encoding Character encoding (default: UTF-8)
     * @param bool $upperCase Use uppercase letters (default: false)
     * @return string Hexadecimal string
     */
    public static function toHex($str, $encoding = 'UTF-8', $upperCase = false)
    {
        if ($str === null || $str === '') {
            return '';
        }

        $encoding = self::normalizeEncoding($encoding);
        if ($encoding !== 'UTF-8') {
            $str = self::toUtf8($str, $encoding);
        }

        $hex = bin2hex($str);

        return $upperCase ? strtoupper($hex) : $hex;
    }

    /**
     * Convert hexadecimal string to regular string
     *
     * @param string $hex The hexadecimal string to convert
     * @param string $encoding Character encoding of output string (default: UTF-8)
     * @return string|false Converted string or false on failure
     */
    public static function fromHex($hex, $encoding = 'UTF-8')
    {
        if ($hex === null || $hex === '') {
            return '';
        }

        if (!self::isValidHex($hex)) {
            return false;
        }

        $str = @hex2bin($hex);

        if ($str === false) {
            return false;
        }

        $encoding = self::normalizeEncoding($encoding);
        if ($encoding !== 'UTF-8') {
            $str = self::convert($str, $encoding, 'UTF-8');
        }

        return $str;
    }

    /**
     * Check if string is valid hexadecimal
     *
     * @param string $str The string to check
     * @return bool True if valid hexadecimal
     */
    public static function isValidHex($str)
    {
        if ($str === null || $str === '') {
            return true;
        }

        return preg_match('/^[0-9a-fA-F]*$/', $str) === 1;
    }

    /**
     * Convert binary data to binary string representation
     *
     * @param string $str The string to convert
     * @param string $encoding Character encoding (default: UTF-8)
     * @param string $separator Separator between bytes (default: space)
     * @return string Binary string representation
     */
    public static function toBinary($str, $encoding = 'UTF-8', $separator = ' ')
    {
        if ($str === null || $str === '') {
            return '';
        }

        $encoding = self::normalizeEncoding($encoding);
        if ($encoding !== 'UTF-8') {
            $str = self::toUtf8($str, $encoding);
        }

        $binary = '';
        $length = strlen($str);

        for ($i = 0; $i < $length; $i++) {
            if ($i > 0) {
                $binary .= $separator;
            }
            $binary .= sprintf('%08b', ord($str[$i]));
        }

        return $binary;
    }

    /**
     * Convert binary string representation to regular string
     *
     * @param string $binary The binary string to convert
     * @param string $encoding Character encoding of output string (default: UTF-8)
     * @param string $separator Separator between bytes (default: space)
     * @return string|false Converted string or false on failure
     */
    public static function fromBinary($binary, $encoding = 'UTF-8', $separator = ' ')
    {
        if ($binary === null || $binary === '') {
            return '';
        }

        $bytes = explode($separator, $binary);
        $str = '';

        foreach ($bytes as $byte) {
            $byte = trim($byte);
            if ($byte === '') {
                continue;
            }

            if (!preg_match('/^[01]{1,8}$/', $byte)) {
                return false;
            }

            $str .= chr(bindec($byte));
        }

        $encoding = self::normalizeEncoding($encoding);
        if ($encoding !== 'UTF-8') {
            $str = self::convert($str, $encoding, 'UTF-8');
        }

        return $str;
    }

    /**
     * Convert string to quoted-printable encoding
     *
     * @param string $str The string to encode
     * @param string $encoding Character encoding (default: UTF-8)
     * @return string Quoted-printable encoded string
     */
    public static function quotedPrintableEncode($str, $encoding = 'UTF-8')
    {
        if ($str === null || $str === '') {
            return '';
        }

        $encoding = self::normalizeEncoding($encoding);
        if ($encoding !== 'UTF-8') {
            $str = self::toUtf8($str, $encoding);
        }

        return quoted_printable_encode($str);
    }

    /**
     * Decode quoted-printable string
     *
     * @param string $str The quoted-printable string to decode
     * @param string $encoding Character encoding of output string (default: UTF-8)
     * @return string Quoted-printable decoded string
     */
    public static function quotedPrintableDecode($str, $encoding = 'UTF-8')
    {
        if ($str === null || $str === '') {
            return '';
        }

        $decoded = quoted_printable_decode($str);

        $encoding = self::normalizeEncoding($encoding);
        if ($encoding !== 'UTF-8') {
            $decoded = self::convert($decoded, $encoding, 'UTF-8');
        }

        return $decoded;
    }

    /**
     * Convert string to Unicode escape sequences
     *
     * @param string $str The string to convert
     * @param string $encoding Character encoding (default: UTF-8)
     * @param string $format Escape format: 'json' (\uXXXX) or 'xml' (&#xXXXX;) or 'html' (&#XXXX;) (default: 'json')
     * @return string Unicode escaped string
     */
    public static function toUnicodeEscape($str, $encoding = 'UTF-8', $format = 'json')
    {
        if ($str === null || $str === '') {
            return '';
        }

        $encoding = self::normalizeEncoding($encoding);
        if ($encoding !== 'UTF-8') {
            $str = self::toUtf8($str, $encoding);
        }

        $result = '';
        $length = mb_strlen($str, 'UTF-8');

        for ($i = 0; $i < $length; $i++) {
            $char = mb_substr($str, $i, 1, 'UTF-8');
            $codePoint = self::getCodePoint($char);

            if ($codePoint === false) {
                continue;
            }

            if ($format === 'json') {
                if ($codePoint > 0xFFFF) {
                    $result .= sprintf('\\u{%X}', $codePoint);
                } else {
                    $result .= sprintf('\\u%04X', $codePoint);
                }
            } elseif ($format === 'xml' || $format === 'html') {
                $result .= sprintf('&#x%X;', $codePoint);
            } else {
                $result .= sprintf('\\u%04X', $codePoint);
            }
        }

        return $result;
    }

    /**
     * Convert Unicode escape sequences to string
     *
     * @param string $str The Unicode escaped string to convert
     * @param string $format Escape format: 'json' (\uXXXX) or 'xml' (&#xXXXX;) or 'html' (&#XXXX;) (default: 'json')
     * @param string $encoding Character encoding of output string (default: UTF-8)
     * @return string Converted string
     */
    public static function fromUnicodeEscape($str, $format = 'json', $encoding = 'UTF-8')
    {
        if ($str === null || $str === '') {
            return '';
        }

        $result = '';

        if ($format === 'json') {
            $result = preg_replace_callback('/\\\\u([0-9a-fA-F]{4})/', function ($matches) {
                return self::codePointToChar(hexdec($matches[1]));
            }, $str);
        } elseif ($format === 'xml' || $format === 'html') {
            $result = preg_replace_callback('/&#x([0-9a-fA-F]+);/', function ($matches) {
                return self::codePointToChar(hexdec($matches[1]));
            }, $str);
            $result = preg_replace_callback('/&#([0-9]+);/', function ($matches) {
                return self::codePointToChar((int)$matches[1]);
            }, $result);
        }

        $encoding = self::normalizeEncoding($encoding);
        if ($encoding !== 'UTF-8') {
            $result = self::convert($result, $encoding, 'UTF-8');
        }

        return $result;
    }

    /**
     * Get Unicode code point of a character
     *
     * @param string $char The character
     * @return int|false Code point or false on failure
     */
    private static function getCodePoint($char)
    {
        $length = strlen($char);

        if ($length === 1) {
            return ord($char);
        }

        $ord = ord($char[0]);

        if ($ord >= 0xF0) {
            return (($ord - 0xF0) << 18) +
                   ((ord($char[1]) - 0x80) << 12) +
                   ((ord($char[2]) - 0x80) << 6) +
                   (ord($char[3]) - 0x80);
        } elseif ($ord >= 0xE0) {
            return (($ord - 0xE0) << 12) +
                   ((ord($char[1]) - 0x80) << 6) +
                   (ord($char[2]) - 0x80);
        } elseif ($ord >= 0xC0) {
            return (($ord - 0xC0) << 6) +
                   (ord($char[1]) - 0x80);
        }

        return $ord;
    }

    /**
     * Convert Unicode code point to UTF-8 character
     *
     * @param int $codePoint The Unicode code point
     * @return string UTF-8 character
     */
    private static function codePointToChar($codePoint)
    {
        if ($codePoint < 0x80) {
            return chr($codePoint);
        } elseif ($codePoint < 0x800) {
            return chr(0xC0 | ($codePoint >> 6)) .
                   chr(0x80 | ($codePoint & 0x3F));
        } elseif ($codePoint < 0x10000) {
            return chr(0xE0 | ($codePoint >> 12)) .
                   chr(0x80 | (($codePoint >> 6) & 0x3F)) .
                   chr(0x80 | ($codePoint & 0x3F));
        } else {
            return chr(0xF0 | ($codePoint >> 18)) .
                   chr(0x80 | (($codePoint >> 12) & 0x3F)) .
                   chr(0x80 | (($codePoint >> 6) & 0x3F)) .
                   chr(0x80 | ($codePoint & 0x3F));
        }
    }

    /**
     * Normalize encoding name
     *
     * @param string $encoding The encoding name to normalize
     * @return string Normalized encoding name
     */
    private static function normalizeEncoding($encoding)
    {
        if ($encoding === null) {
            return self::$defaultEncoding;
        }

        $encoding = strtoupper(trim($encoding));

        $aliases = [
            'UTF8' => 'UTF-8',
            'UTF-8' => 'UTF-8',
            'GB18030' => 'GB18030',
            'BIG5' => 'BIG5',
            'BIG-5' => 'BIG5',
            'BIG5-HKSCS' => 'BIG5',
            'ISO-8859-1' => 'ISO-8859-1',
            'ISO8859-1' => 'ISO-8859-1',
            'LATIN1' => 'ISO-8859-1',
            'LATIN-1' => 'ISO-8859-1',
            'WINDOWS-1251' => 'WINDOWS-1251',
            'CP1251' => 'WINDOWS-1251',
            'WINDOWS-1252' => 'WINDOWS-1252',
            'CP1252' => 'WINDOWS-1252',
            'ASCII' => 'ASCII',
            'US-ASCII' => 'ASCII',
            'EUC-JP' => 'EUC-JP',
            'EUCJP' => 'EUC-JP',
            'SJIS' => 'SJIS',
            'SHIFT_JIS' => 'SJIS',
            'EUC-KR' => 'EUC-KR',
            'EUCKR' => 'EUC-KR',
        ];

        return isset($aliases[$encoding]) ? $aliases[$encoding] : $encoding;
    }
}
