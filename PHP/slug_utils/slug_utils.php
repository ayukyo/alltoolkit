<?php
/**
 * Slug Utils - URL-friendly slug generation utilities for PHP
 * 
 * A comprehensive library for generating SEO-friendly slugs from strings.
 * Zero external dependencies - uses only PHP standard library.
 * 
 * Features:
 * - Convert strings to URL-friendly slugs
 * - Support for multiple languages (transliteration)
 * - Custom separators and options
 * - Slug validation and sanitization
 * - Unique slug generation with suffixes
 * 
 * @package   SlugUtils
 * @version   1.0.0
 * @license   MIT
 */

namespace SlugUtils;

/**
 * Main SlugGenerator class
 */
class SlugGenerator
{
    /** @var string Default separator between words */
    private string $separator = '-';
    
    /** @var bool Convert to lowercase */
    private bool $lowercase = true;
    
    /** @var int Maximum slug length (0 = unlimited) */
    private int $maxLength = 0;
    
    /** @var array Character transliteration map */
    private array $transliterationMap = [];
    
    /** @var array Reserved words to avoid */
    private array $reservedWords = [];
    
    /**
     * Constructor with optional configuration
     * 
     * @param array $config Configuration options
     */
    public function __construct(array $config = [])
    {
        if (isset($config['separator'])) {
            $this->separator = $config['separator'];
        }
        if (isset($config['lowercase'])) {
            $this->lowercase = $config['lowercase'];
        }
        if (isset($config['max_length'])) {
            $this->maxLength = (int) $config['max_length'];
        }
        if (isset($config['reserved_words'])) {
            $this->reservedWords = $config['reserved_words'];
        }
        
        $this->initializeTransliteration();
    }
    
    /**
     * Initialize character transliteration map for international support
     */
    private function initializeTransliteration(): void
    {
        // Common transliterations for international characters
        $this->transliterationMap = [
            // Latin extended
            'À' => 'A', 'Á' => 'A', 'Â' => 'A', 'Ã' => 'A', 'Ä' => 'A', 'Å' => 'A',
            'à' => 'a', 'á' => 'a', 'â' => 'a', 'ã' => 'a', 'ä' => 'a', 'å' => 'a',
            'Æ' => 'AE', 'æ' => 'ae',
            'Ç' => 'C', 'ç' => 'c',
            'Ð' => 'D', 'ð' => 'd',
            'È' => 'E', 'É' => 'E', 'Ê' => 'E', 'Ë' => 'E',
            'è' => 'e', 'é' => 'e', 'ê' => 'e', 'ë' => 'e',
            'Ì' => 'I', 'Í' => 'I', 'Î' => 'I', 'Ï' => 'I',
            'ì' => 'i', 'í' => 'i', 'î' => 'i', 'ï' => 'i',
            'Ñ' => 'N', 'ñ' => 'n',
            'Ò' => 'O', 'Ó' => 'O', 'Ô' => 'O', 'Õ' => 'O', 'Ö' => 'O', 'Ø' => 'O',
            'ò' => 'o', 'ó' => 'o', 'ô' => 'o', 'õ' => 'o', 'ö' => 'o', 'ø' => 'o',
            'Ù' => 'U', 'Ú' => 'U', 'Û' => 'U', 'Ü' => 'U',
            'ù' => 'u', 'ú' => 'u', 'û' => 'u', 'ü' => 'u',
            'Ý' => 'Y', 'ý' => 'y', 'ÿ' => 'y',
            'Þ' => 'TH', 'þ' => 'th',
            'ß' => 'ss',
            
            // Cyrillic (Russian, Ukrainian, etc.)
            'А' => 'A', 'Б' => 'B', 'В' => 'V', 'Г' => 'G', 'Д' => 'D',
            'Е' => 'E', 'Ё' => 'YO', 'Ж' => 'ZH', 'З' => 'Z', 'И' => 'I',
            'Й' => 'Y', 'К' => 'K', 'Л' => 'L', 'М' => 'M', 'Н' => 'N',
            'О' => 'O', 'П' => 'P', 'Р' => 'R', 'С' => 'S', 'Т' => 'T',
            'У' => 'U', 'Ф' => 'F', 'Х' => 'KH', 'Ц' => 'TS', 'Ч' => 'CH',
            'Ш' => 'SH', 'Щ' => 'SCH', 'Ъ' => '', 'Ы' => 'Y', 'Ь' => '',
            'Э' => 'E', 'Ю' => 'YU', 'Я' => 'YA',
            'а' => 'a', 'б' => 'b', 'в' => 'v', 'г' => 'g', 'д' => 'd',
            'е' => 'e', 'ё' => 'yo', 'ж' => 'zh', 'з' => 'z', 'и' => 'i',
            'й' => 'y', 'к' => 'k', 'л' => 'l', 'м' => 'm', 'н' => 'n',
            'о' => 'o', 'п' => 'p', 'р' => 'r', 'с' => 's', 'т' => 't',
            'у' => 'u', 'ф' => 'f', 'х' => 'kh', 'ц' => 'ts', 'ч' => 'ch',
            'ш' => 'sh', 'щ' => 'sch', 'ъ' => '', 'ы' => 'y', 'ь' => '',
            'э' => 'e', 'ю' => 'yu', 'я' => 'ya',
            
            // Greek
            'Α' => 'A', 'Β' => 'B', 'Γ' => 'G', 'Δ' => 'D', 'Ε' => 'E',
            'Ζ' => 'Z', 'Η' => 'H', 'Θ' => 'TH', 'Ι' => 'I', 'Κ' => 'K',
            'Λ' => 'L', 'Μ' => 'M', 'Ν' => 'N', 'Ξ' => 'X', 'Ο' => 'O',
            'Π' => 'P', 'Ρ' => 'R', 'Σ' => 'S', 'Τ' => 'T', 'Υ' => 'Y',
            'Φ' => 'F', 'Χ' => 'CH', 'Ψ' => 'PS', 'Ω' => 'O',
            'α' => 'a', 'β' => 'b', 'γ' => 'g', 'δ' => 'd', 'ε' => 'e',
            'ζ' => 'z', 'η' => 'h', 'θ' => 'th', 'ι' => 'i', 'κ' => 'k',
            'λ' => 'l', 'μ' => 'm', 'ν' => 'n', 'ξ' => 'x', 'ο' => 'o',
            'π' => 'p', 'ρ' => 'r', 'σ' => 's', 'τ' => 't', 'υ' => 'y',
            'φ' => 'f', 'χ' => 'ch', 'ψ' => 'ps', 'ω' => 'o',
            
            // German
            'Ä' => 'AE', 'Ö' => 'OE', 'Ü' => 'UE',
            'ä' => 'ae', 'ö' => 'oe', 'ü' => 'ue',
            
            // Turkish
            'Ğ' => 'G', 'ğ' => 'g', 'Ş' => 'S', 'ş' => 's', 'İ' => 'I', 'ı' => 'i',
            
            // Polish
            'Ą' => 'A', 'ą' => 'a', 'Ć' => 'C', 'ć' => 'c', 'Ę' => 'E', 'ę' => 'e',
            'Ł' => 'L', 'ł' => 'l', 'Ń' => 'N', 'ń' => 'n', 'Ś' => 'S', 'ś' => 's',
            'Ź' => 'Z', 'ź' => 'z', 'Ż' => 'Z', 'ż' => 'z',
            
            // Czech
            'Č' => 'C', 'č' => 'c', 'Ď' => 'D', 'ď' => 'd', 'Ě' => 'E', 'ě' => 'e',
            'Ň' => 'N', 'ň' => 'n', 'Ř' => 'R', 'ř' => 'r', 'Š' => 'S', 'š' => 's',
            'Ť' => 'T', 'ť' => 't', 'Ů' => 'U', 'ů' => 'u', 'Ž' => 'Z', 'ž' => 'z',
            
            // Hungarian
            'Ő' => 'O', 'ő' => 'o', 'Ű' => 'U', 'ű' => 'u',
            
            // Scandinavian
            'Å' => 'A', 'å' => 'a', 'Æ' => 'AE', 'æ' => 'ae', 'Ø' => 'O', 'ø' => 'o',
            
            // Romanian
            'Ă' => 'A', 'ă' => 'a', 'Â' => 'A', 'â' => 'a', 'Î' => 'I', 'î' => 'i',
            'Ț' => 'T', 'ț' => 't', 'Ș' => 'S', 'ș' => 's',
            
            // Japanese (Hiragana/Katakana to romaji - simplified)
            'あ' => 'a', 'い' => 'i', 'う' => 'u', 'え' => 'e', 'お' => 'o',
            'か' => 'ka', 'き' => 'ki', 'く' => 'ku', 'け' => 'ke', 'こ' => 'ko',
            'さ' => 'sa', 'し' => 'shi', 'す' => 'su', 'せ' => 'se', 'そ' => 'so',
            'た' => 'ta', 'ち' => 'chi', 'つ' => 'tsu', 'て' => 'te', 'と' => 'to',
            'な' => 'na', 'に' => 'ni', 'ぬ' => 'nu', 'ね' => 'ne', 'の' => 'no',
            'は' => 'ha', 'ひ' => 'hi', 'ふ' => 'fu', 'へ' => 'he', 'ほ' => 'ho',
            'ま' => 'ma', 'み' => 'mi', 'む' => 'mu', 'め' => 'me', 'も' => 'mo',
            'や' => 'ya', 'ゆ' => 'yu', 'よ' => 'yo',
            'ら' => 'ra', 'り' => 'ri', 'る' => 'ru', 'れ' => 're', 'ろ' => 'ro',
            'わ' => 'wa', 'を' => 'wo', 'ん' => 'n',
            
            // Korean (Hangul to romanization - basic)
            '가' => 'ga', '나' => 'na', '다' => 'da', '라' => 'ra', '마' => 'ma',
            '바' => 'ba', '사' => 'sa', '아' => 'a', '자' => 'ja', '차' => 'cha',
            '카' => 'ka', '타' => 'ta', '파' => 'pa', '하' => 'ha',
            
            // Arabic (basic)
            'ا' => 'a', 'ب' => 'b', 'ت' => 't', 'ث' => 'th', 'ج' => 'j',
            'ح' => 'h', 'خ' => 'kh', 'د' => 'd', 'ذ' => 'dh', 'ر' => 'r',
            'ز' => 'z', 'س' => 's', 'ش' => 'sh', 'ص' => 's', 'ض' => 'd',
            'ط' => 't', 'ظ' => 'z', 'ع' => 'a', 'غ' => 'gh', 'ف' => 'f',
            'ق' => 'q', 'ك' => 'k', 'ل' => 'l', 'م' => 'm', 'ن' => 'n',
            'ه' => 'h', 'و' => 'w', 'ي' => 'y',
            
            // Hebrew (basic)
            'א' => 'a', 'ב' => 'b', 'ג' => 'g', 'ד' => 'd', 'ה' => 'h',
            'ו' => 'v', 'ז' => 'z', 'ח' => 'ch', 'ט' => 't', 'י' => 'y',
            'כ' => 'k', 'ל' => 'l', 'מ' => 'm', 'נ' => 'n', 'ס' => 's',
            'ע' => 'a', 'פ' => 'p', 'צ' => 'tz', 'ק' => 'k', 'ר' => 'r',
            'ש' => 'sh', 'ת' => 't',
            
            // Chinese (Pinyin approximations for common characters)
            '的' => 'de', '一' => 'yi', '是' => 'shi', '不' => 'bu', '了' => 'le',
            '在' => 'zai', '人' => 'ren', '有' => 'you', '我' => 'wo', '他' => 'ta',
            '这' => 'zhe', '个' => 'ge', '中' => 'zhong', '大' => 'da', '来' => 'lai',
            '上' => 'shang', '国' => 'guo', '和' => 'he', '地' => 'di', '到' => 'dao',
            '以' => 'yi', '说' => 'shuo', '时' => 'shi', '要' => 'yao', '就' => 'jiu',
            '出' => 'chu', '会' => 'hui', '可' => 'ke', '也' => 'ye', '自' => 'zi',
            '对' => 'dui', '生' => 'sheng', '能' => 'neng', '而' => 'er', '子' => 'zi',
            '那' => 'na', '得' => 'de', '于' => 'yu', '着' => 'zhe', '下' => 'xia',
        ];
    }
    
    /**
     * Generate a slug from a string
     * 
     * @param string $text Input text to convert to slug
     * @return string Generated slug
     */
    public function generate(string $text): string
    {
        // Step 1: Apply transliteration
        $slug = strtr($text, $this->transliterationMap);
        
        // Step 2: Convert to lowercase if enabled
        if ($this->lowercase) {
            $slug = strtolower($slug);
        }
        
        // Step 3: Replace non-alphanumeric characters
        $slug = preg_replace('/[^a-z0-9]+/i', $this->separator, $slug);
        
        // Step 4: Remove separator from beginning and end
        $slug = trim($slug, $this->separator);
        
        // Step 5: Apply max length if set
        if ($this->maxLength > 0 && strlen($slug) > $this->maxLength) {
            $slug = substr($slug, 0, $this->maxLength);
            // Remove partial word at the end
            $lastSepPos = strrpos($slug, $this->separator);
            if ($lastSepPos !== false) {
                $slug = substr($slug, 0, $lastSepPos);
            }
        }
        
        // Step 6: Handle reserved words
        if (in_array($slug, $this->reservedWords, true)) {
            $slug .= $this->separator . '1';
        }
        
        return $slug;
    }
    
    /**
     * Generate a unique slug with numeric suffix
     * 
     * @param string $text Input text
     * @param array $existingSlugs Array of existing slugs to avoid
     * @return string Unique slug
     */
    public function generateUnique(string $text, array $existingSlugs = []): string
    {
        $baseSlug = $this->generate($text);
        $slug = $baseSlug;
        $counter = 1;
        
        while (in_array($slug, $existingSlugs, true)) {
            $slug = $baseSlug . $this->separator . $counter;
            $counter++;
        }
        
        return $slug;
    }
    
    /**
     * Generate slug from multiple parts
     * 
     * @param array $parts Array of strings to combine
     * @return string Combined slug
     */
    public function generateFromParts(array $parts): string
    {
        $combined = implode(' ', array_filter($parts));
        return $this->generate($combined);
    }
    
    /**
     * Generate slug with timestamp suffix
     * 
     * @param string $text Input text
     * @param string|null $timestamp Custom timestamp (defaults to now)
     * @return string Slug with timestamp
     */
    public function generateWithTimestamp(string $text, ?string $timestamp = null): string
    {
        $slug = $this->generate($text);
        $ts = $timestamp ?? date('Y-m-d');
        return $slug . $this->separator . $ts;
    }
    
    /**
     * Generate slug with random suffix
     * 
     * @param string $text Input text
     * @param int $length Length of random suffix (default: 4)
     * @return string Slug with random suffix
     */
    public function generateWithRandomSuffix(string $text, int $length = 4): string
    {
        $slug = $this->generate($text);
        $suffix = $this->generateRandomString($length);
        return $slug . $this->separator . $suffix;
    }
    
    /**
     * Generate random alphanumeric string
     * 
     * @param int $length String length
     * @return string Random string
     */
    private function generateRandomString(int $length): string
    {
        $chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
        $result = '';
        for ($i = 0; $i < $length; $i++) {
            $result .= $chars[random_int(0, strlen($chars) - 1)];
        }
        return $result;
    }
    
    /**
     * Validate if a string is a valid slug
     * 
     * @param string $slug Slug to validate
     * @return bool True if valid
     */
    public function isValid(string $slug): bool
    {
        // Empty is not valid
        if (empty($slug)) {
            return false;
        }
        
        // Check pattern: only alphanumeric and separator
        $pattern = '/^[a-z0-9]+(' . preg_quote($this->separator, '/') . '[a-z0-9]+)*$/';
        if ($this->lowercase) {
            return preg_match($pattern, $slug) === 1;
        }
        
        // Case-insensitive pattern
        $pattern = '/^[a-z0-9]+(' . preg_quote($this->separator, '/') . '[a-z0-9]+)*$/i';
        return preg_match($pattern, $slug) === 1;
    }
    
    /**
     * Sanitize an existing slug
     * 
     * @param string $slug Slug to sanitize
     * @return string Sanitized slug
     */
    public function sanitize(string $slug): string
    {
        // Remove leading/trailing separators
        $slug = trim($slug, $this->separator);
        
        // Replace multiple consecutive separators with one
        $pattern = '/' . preg_quote($this->separator, '/') . '+/';
        $slug = preg_replace($pattern, $this->separator, $slug);
        
        // Convert to lowercase if enabled
        if ($this->lowercase) {
            $slug = strtolower($slug);
        }
        
        return $slug;
    }
    
    /**
     * Convert slug back to title case
     * 
     * @param string $slug Slug to convert
     * @return string Title case string
     */
    public function toTitle(string $slug): string
    {
        $words = explode($this->separator, $slug);
        $words = array_map('ucfirst', $words);
        return implode(' ', $words);
    }
    
    /**
     * Convert slug to camelCase
     * 
     * @param string $slug Slug to convert
     * @return string camelCase string
     */
    public function toCamelCase(string $slug): string
    {
        $words = explode($this->separator, $slug);
        $first = array_shift($words);
        $words = array_map('ucfirst', $words);
        return $first . implode('', $words);
    }
    
    /**
     * Convert slug to snake_case
     * 
     * @param string $slug Slug to convert
     * @return string snake_case string
     */
    public function toSnakeCase(string $slug): string
    {
        return str_replace($this->separator, '_', $slug);
    }
    
    /**
     * Parse slug into array of words
     * 
     * @param string $slug Slug to parse
     * @return array Array of words
     */
    public function parse(string $slug): array
    {
        return explode($this->separator, $slug);
    }
    
    /**
     * Compare two slugs for similarity
     * 
     * @param string $slug1 First slug
     * @param string $slug2 Second slug
     * @return float Similarity score (0.0 to 1.0)
     */
    public function similarity(string $slug1, string $slug2): float
    {
        $words1 = $this->parse($slug1);
        $words2 = $this->parse($slug2);
        
        $commonWords = array_intersect($words1, $words2);
        $totalWords = array_unique(array_merge($words1, $words2));
        
        if (empty($totalWords)) {
            return 1.0;
        }
        
        return count($commonWords) / count($totalWords);
    }
    
    /**
     * Get current separator
     * 
     * @return string Current separator
     */
    public function getSeparator(): string
    {
        return $this->separator;
    }
    
    /**
     * Set separator
     * 
     * @param string $separator New separator
     * @return self
     */
    public function setSeparator(string $separator): self
    {
        $this->separator = $separator;
        return $this;
    }
}

/**
 * Convenience functions for quick slug generation
 */
class SlugHelper
{
    /**
     * Quick slug generation with default settings
     * 
     * @param string $text Input text
     * @return string Generated slug
     */
    public static function slug(string $text): string
    {
        $generator = new SlugGenerator();
        return $generator->generate($text);
    }
    
    /**
     * Generate slug with underscore separator
     * 
     * @param string $text Input text
     * @return string Generated slug with underscores
     */
    public static function underscore(string $text): string
    {
        $generator = new SlugGenerator(['separator' => '_']);
        return $generator->generate($text);
    }
    
    /**
     * Generate URL-safe filename from text
     * 
     * @param string $text Input text
     * @param string $extension File extension (without dot)
     * @return string Safe filename
     */
    public static function filename(string $text, string $extension = ''): string
    {
        $generator = new SlugGenerator(['separator' => '-']);
        $slug = $generator->generate($text);
        
        if (!empty($extension)) {
            $slug .= '.' . preg_replace('/[^a-z0-9]+/i', '', strtolower($extension));
        }
        
        return $slug;
    }
    
    /**
     * Generate URL-safe ID
     * 
     * @param string $prefix Optional prefix
     * @param int $length Length of random part
     * @return string Unique ID
     */
    public static function id(string $prefix = '', int $length = 8): string
    {
        $chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
        $random = '';
        for ($i = 0; $i < $length; $i++) {
            $random .= $chars[random_int(0, strlen($chars) - 1)];
        }
        
        return $prefix . ($prefix !== '' ? '-' : '') . $random;
    }
    
    /**
     * Generate slug from a title (optimized for blog posts, articles)
     * 
     * @param string $title Article title
     * @param int $maxLength Maximum length (default: 60 for SEO)
     * @return string SEO-friendly slug
     */
    public static function titleSlug(string $title, int $maxLength = 60): string
    {
        $generator = new SlugGenerator(['max_length' => $maxLength]);
        return $generator->generate($title);
    }
    
    /**
     * Generate slug for a product (optimized for e-commerce)
     * 
     * @param string $name Product name
     * @param string|null $sku Optional SKU to append
     * @return string Product slug
     */
    public static function productSlug(string $name, ?string $sku = null): string
    {
        $generator = new SlugGenerator(['max_length' => 50]);
        $slug = $generator->generate($name);
        
        if ($sku !== null) {
            $skuSlug = preg_replace('/[^a-z0-9-]+/i', '-', $sku);
            $slug .= '-' . strtolower($skuSlug);
        }
        
        return $slug;
    }
    
    /**
     * Generate slug for a username (strict rules)
     * 
     * @param string $name Desired username
     * @return string Safe username
     */
    public static function usernameSlug(string $name): string
    {
        // Reserved usernames to avoid
        $reserved = ['admin', 'root', 'system', 'api', 'www', 'ftp', 'mail', 
                     'support', 'help', 'administrator', 'moderator', 'mod'];
        
        $generator = new SlugGenerator([
            'separator' => '',
            'reserved_words' => $reserved
        ]);
        
        $slug = $generator->generate($name);
        
        // Ensure minimum length
        if (strlen($slug) < 3) {
            $slug .= self::id('', 3);
        }
        
        return $slug;
    }
}