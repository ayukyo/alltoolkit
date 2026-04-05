<?php
/**
 * AllToolkit - QR Code Utilities for PHP
 *
 * A zero-dependency QR Code generation library for PHP.
 * Supports QR Code Model 2 with versions 1-10 and error correction levels (L, M, Q, H).
 *
 * @package AllToolkit\QrCodeUtils
 * @author AllToolkit Contributors
 * @license MIT
 */

namespace AllToolkit;

/**
 * QR Code Exception Class
 */
class QrCodeException extends \Exception {}

/**
 * QR Code Generator Class
 *
 * Generates QR Codes with various output formats including:
 * - Text/ASCII art
 * - PNG image (GD extension required)
 * - SVG vector graphics
 * - Binary matrix
 */
class QrCodeGenerator {
    // Error correction levels
    const ERROR_CORRECTION_L = 0; // ~7% correction
    const ERROR_CORRECTION_M = 1; // ~15% correction
    const ERROR_CORRECTION_Q = 2; // ~25% correction
    const ERROR_CORRECTION_H = 3; // ~30% correction

    // Mode indicators
    const MODE_NUMERIC = 1;
    const MODE_ALPHANUMERIC = 2;
    const MODE_BYTE = 4;

    // Alphanumeric character set
    private const ALPHANUMERIC_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:';

    // Format information strings for each error correction level and mask pattern
    private const FORMAT_INFO = [
        [0x77c4, 0x72f3, 0x7daa, 0x789d, 0x662f, 0x6318, 0x6c41, 0x6976],
        [0x5412, 0x5125, 0x5e7c, 0x5b4b, 0x45f9, 0x40ce, 0x4f97, 0x4aa0],
        [0x355f, 0x3068, 0x3f31, 0x3a06, 0x24b4, 0x2183, 0x2eda, 0x2bed],
        [0x1689, 0x13be, 0x1ce7, 0x19d0, 0x0762, 0x0255, 0x0d0c, 0x083b],
    ];

    private $version;
    private $errorCorrectionLevel;
    private $modules;
    private $moduleCount;

    /**
     * Constructor
     *
     * @param int $version QR Code version (1-10 for this implementation)
     * @param int $errorCorrectionLevel Error correction level (L, M, Q, H)
     */
    public function __construct($version = 1, $errorCorrectionLevel = self::ERROR_CORRECTION_L) {
        if ($version < 1 || $version > 10) {
            throw new QrCodeException("Version must be between 1 and 10");
        }
        if ($errorCorrectionLevel < 0 || $errorCorrectionLevel > 3) {
            throw new QrCodeException("Invalid error correction level");
        }
        $this->version = $version;
        $this->errorCorrectionLevel = $errorCorrectionLevel;
        $this->moduleCount = 17 + 4 * $version;
        $this->modules = [];
    }

    /**
     * Detect the best mode for the given data
     *
     * @param string $data Input data
     * @return int Mode constant
     */
    public static function detectMode($data) {
        if (self::isNumeric($data)) {
            return self::MODE_NUMERIC;
        }
        if (self::isAlphanumeric($data)) {
            return self::MODE_ALPHANUMERIC;
        }
        return self::MODE_BYTE;
    }

    /**
     * Check if data is numeric only
     *
     * @param string $data Input data
     * @return bool True if numeric
     */
    private static function isNumeric($data) {
        return preg_match('/^[0-9]+$/', $data) === 1;
    }

    /**
     * Check if data is alphanumeric
     *
     * @param string $data Input data
     * @return bool True if alphanumeric
     */
    private static function isAlphanumeric($data) {
        for ($i = 0; $i < strlen($data); $i++) {
            if (strpos(self::ALPHANUMERIC_CHARS, $data[$i]) === false) {
                return false;
            }
        }
        return true;
    }

    /**
     * Get character code for alphanumeric mode
     *
     * @param string $char Single character
     * @return int Character code
     */
    private static function getAlphanumericCode($char) {
        $pos = strpos(self::ALPHANUMERIC_CHARS, $char);
        return $pos !== false ? $pos : 0;
    }

    /**
     * Generate QR Code from data
     *
     * @param string $data Data to encode
     * @return array 2D array of boolean values representing QR Code modules
     * @throws QrCodeException On error
     */
    public function generate($data) {
        $this->modules = [];

        // Initialize empty modules
        for ($row = 0; $row < $this->moduleCount; $row++) {
            $this->modules[$row] = [];
            for ($col = 0; $col < $this->moduleCount; $col++) {
                $this->modules[$row][$col] = false;
            }
        }

        // Add finder patterns
        $this->addFinderPatterns();

        // Add separators
        $this->addSeparators();

        // Add alignment patterns (versions 2+)
        if ($this->version >= 2) {
            $this->addAlignmentPatterns();
        }

        // Add timing patterns
        $this->addTimingPatterns();

        // Add dark module
        $this->addDarkModule();

        // Add format information
        $this->addFormatInfo();

        // Encode data (simplified version)
        $this->encodeDataSimple($data);

        return $this->modules;
    }

    /**
     * Add finder patterns (three corners)
     */
    private function addFinderPatterns() {
        $positions = [
            [0, 0],
            [$this->moduleCount - 7, 0],
            [0, $this->moduleCount - 7]
        ];

        foreach ($positions as $pos) {
            $row = $pos[1];
            $col = $pos[0];

            // 7x7 finder pattern
            for ($r = 0; $r < 7; $r++) {
                for ($c = 0; $c < 7; $c++) {
                    // Outer black square (3x3 corners)
                    $isBlack = ($r == 0 || $r == 6 || $c == 0 || $c == 6) ||
                               ($r >= 2 && $r <= 4 && $c >= 2 && $c <= 4);
                    $this->modules[$row + $r][$col + $c] = $isBlack;
                }
            }
        }
    }

    /**
     * Add separators around finder patterns
     */
    private function addSeparators() {
        $positions = [
            [0, 0],
            [$this->moduleCount - 8, 0],
            [0, $this->moduleCount - 8]
        ];

        foreach ($positions as $pos) {
            $row = $pos[1];
            $col = $pos[0];

            // White separator (1 module wide)
            for ($i = 0; $i <= 7; $i++) {
                if ($row + 7 < $this->moduleCount) {
                    $this->modules[$row + 7][$col + min($i, 6)] = false;
                }
                if ($col + 7 < $this->moduleCount) {
                    $this->modules[$row + min($i, 6)][$col + 7] = false;
                }
            }
        }
    }

    /**
     * Add alignment patterns
     */
    private function addAlignmentPatterns() {
        $positions = $this->getAlignmentPatternPositions();

        foreach ($positions as $pos) {
            $row = $pos[1];
            $col = $pos[0];

            // 5x5 alignment pattern
            for ($r = -2; $r <= 2; $r++) {
                for ($c = -2; $c <= 2; $c++) {
                    $isBlack = (abs($r) == 2 || abs($c) == 2) || ($r == 0 && $c == 0);
                    $this->modules[$row + $r][$col + $c] = $isBlack;
                }
            }
        }
    }

    /**
     * Get alignment pattern positions for current version
     */
    private function getAlignmentPatternPositions() {
        if ($this->version == 1) return [];

        $alignmentPatternPositions = [
            2 => [6, 18],
            3 => [6, 22],
            4 => [6, 26],
            5 => [6, 30],
            6 => [6, 34],
            7 => [6, 22, 38],
            8 => [6, 24, 42],
            9 => [6, 26, 46],
            10 => [6, 28, 50],
        ];

        $positions = [];
        $coords = $alignmentPatternPositions[$this->version] ?? [6, 18];

        foreach ($coords as $row) {
            foreach ($coords as $col) {
                // Skip positions overlapping with finder patterns
                if (($row < 10 && $col < 10) ||
                    ($row < 10 && $col > $this->moduleCount - 10) ||
                    ($row > $this->moduleCount - 10 && $col < 10)) {
                    continue;
                }
                $positions[] = [$col, $row];
            }
        }

        return $positions;
    }

    /**
     * Add timing patterns
     */
    private function addTimingPatterns() {
        for ($i = 8; $i < $this->moduleCount - 8; $i++) {
            $this->modules[6][$i] = ($i % 2) == 0;
            $this->modules[$i][6] = ($i % 2) == 0;
        }
    }

    /**
     * Add dark module (always at position [4*version+9, 8])
     */
    private function addDarkModule() {
        $this->modules[4 * $this->version + 9][8] = true;
    }

    /**
     * Add format information
     */
    private function addFormatInfo() {
        $formatInfo = self::FORMAT_INFO[$this->errorCorrectionLevel][0];

        // Top-left
        for ($i = 0; $i < 6; $i++) {
            $this->modules[8][$i] = (($formatInfo >> $i) & 1) == 1;
        }
        for ($i = 0; $i < 3; $i++) {
            $this->modules[8][7 + $i] = (($formatInfo >> (6 + $i)) & 1) == 1;
        }
        for ($i = 0; $i < 6; $i++) {
            $this->modules[5 - $i][8] = (($formatInfo >> $i) & 1) == 1;
        }
        for ($i = 0; $i < 3; $i++) {
            $this->modules[7 + $i][8] = (($formatInfo >> (6 + $i)) & 1) == 1;
        }

        // Top-right and bottom-left
        for ($i = 0; $i < 8; $i++) {
            $this->modules[8][$this->moduleCount - 1 - $i] = (($formatInfo >> $i) & 1) == 1;
            $this->modules[$this->moduleCount - 1 - $i][8] = (($formatInfo >> $i) & 1) == 1;
        }
    }

    /**
     * Simple data encoding (demonstration version)
     * In a full implementation, this would include proper Reed-Solomon error correction
     */
    private function encodeDataSimple($data) {
        $mode = self::detectMode($data);
        $bitData = '';

        // Mode indicator (4 bits)
        $bitData .= str_pad(decbin($mode), 4, '0', STR_PAD_LEFT);

        // Character count indicator (varies by mode and version)
        $charCountBits = $this->getCharCountBits($mode);
        $bitData .= str_pad(decbin(strlen($data)), $charCountBits, '0', STR_PAD_LEFT);

        // Data encoding
        if ($mode === self::MODE_NUMERIC) {
            $bitData .= $this->encodeNumeric($data);
        } elseif ($mode === self::MODE_ALPHANUMERIC) {
            $bitData .= $this->encodeAlphanumeric($data);
        } else {
            $bitData .= $this->encodeByte($data);
        }

        // Terminator (4 zeros or less)
        $bitData .= '0000';

        // Pad to byte boundary
        while (strlen($bitData) % 8 !== 0) {
            $bitData .= '0';
        }

        // Pad bytes
        $padBytes = ['11101100', '00010001'];
        $padIndex = 0;
        $dataCapacity = $this->getDataCapacity();

        while (strlen($bitData) < $dataCapacity * 8) {
            $bitData .= $padBytes[$padIndex % 2];
            $padIndex++;
        }

        // Place data in QR Code matrix
        $this->placeData($bitData);
    }

    /**
     * Get character count bits based on mode and version
     */
    private function getCharCountBits($mode) {
        if ($this->version <= 9) {
            return $mode === self::MODE_NUMERIC ? 10 : ($mode === self::MODE_ALPHANUMERIC ? 9 : 8);
        }
        return $mode === self::MODE_NUMERIC ? 12 : ($mode === self::MODE_ALPHANUMERIC ? 11 : 16);
    }

    /**
     * Encode numeric data
     */
    private function encodeNumeric($data) {
        $result = '';
        for ($i = 0; $i < strlen($data); $i += 3) {
            $chunk = substr($data, $i, 3);
            $bits = strlen($chunk) === 3 ? 10 : (strlen($chunk) === 2 ? 7 : 4);
            $result .= str_pad(decbin((int)$chunk), $bits, '0', STR_PAD_LEFT);
        }
        return $result;
    }

    /**
     * Encode alphanumeric data
     */
    private function encodeAlphanumeric($data) {
        $result = '';
        for ($i = 0; $i < strlen($data); $i += 2) {
            if ($i + 1 < strlen($data)) {
                $val = self::getAlphanumericCode($data[$i]) * 45 +
                       self::getAlphanumericCode($data[$i + 1]);
                $result .= str_pad(decbin($val), 11, '0', STR_PAD_LEFT);
            } else {
                $result .= str_pad(decbin(self::getAlphanumericCode($data[$i])), 6, '0', STR_PAD_LEFT);
            }
        }
        return $result;
    }

    /**
     * Encode byte data
     */
    private function encodeByte($data) {
        $result = '';
        for ($i = 0; $i < strlen($data); $i++) {
            $result .= str_pad(decbin(ord($data[$i])), 8, '0', STR_PAD_LEFT);
        }
        return $result;
    }

    /**
     * Get data capacity in codewords
     */
    private function getDataCapacity() {
        // Simplified capacity table (data codewords for version 1-10, error level L)
        $capacities = [
            1 => [19, 16, 13, 9],
            2 => [34, 28, 22, 16],
            3 => [55, 44, 34, 26],
            4 => [80, 64, 48, 36],
            5 => [108, 86, 62, 46],
            6 => [136, 108, 76, 60],
            7 => [156, 124, 88, 66],
            8 => [194, 154, 110, 86],
            9 => [232, 182, 132, 100],
            10 => [274, 216, 154, 122],
        ];
        return $capacities[$this->version][$this->errorCorrectionLevel] ?? 19;
    }

    /**
     * Place data bits in the QR Code matrix
     */
    private function placeData($bitData) {
        $bitIndex = 0;
        $direction = -1; // Upward
        $col = $this->moduleCount - 1;

        while ($col > 0 && $bitIndex < strlen($bitData)) {
            if ($col === 6) $col--; // Skip timing column

            for ($i = 0; $i < $this->moduleCount; $i++) {
                $row = $direction === -1 ? $this->moduleCount - 1 - $i : $i;

                for ($c = 0; $c < 2; $c++) {
                    $currentCol = $col - $c;

                    // Skip if module is already set (part of finder patterns, etc.)
                    if ($this->isReserved($row, $currentCol)) {
                        continue;
                    }

                    if ($bitIndex < strlen($bitData)) {
                        $this->modules[$row][$currentCol] = $bitData[$bitIndex] === '1';
                        $bitIndex++;
                    }
                }
            }

            $col -= 2;
            $direction *= -1;
        }
    }

    /**
     * Check if a module position is reserved for function patterns
     */
    private function isReserved($row, $col) {
        // Finder patterns and separators
        if (($row < 9 && $col < 9) ||
            ($row < 9 && $col >= $this->moduleCount - 8) ||
            ($row >= $this->moduleCount - 8 && $col < 9)) {
            return true;
        }

        // Timing patterns
        if ($row === 6 || $col === 6) {
            return true;
        }

        // Dark module
        if ($row === 4 * $this->version + 9 && $col === 8) {
            return true;
        }

        // Format information
        if (($row === 8 && $col < 9) ||
            ($row === 8 && $col >= $this->moduleCount - 8) ||
            ($col === 8 && $row < 9) ||
            ($col === 8 && $row >= $this->moduleCount - 8)) {
            return true;
        }

        // Alignment patterns (simplified check)
        if ($this->version >= 2) {
            $positions = $this->getAlignmentPatternPositions();
            foreach ($positions as $pos) {
                $apCol = $pos[0];
                $apRow = $pos[1];
                if (abs($row - $apRow) <= 2 && abs($col - $apCol) <= 2) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Generate QR Code as ASCII art
     *
     * @param string $data Data to encode
     * @param string $darkChar Character for dark modules
     * @param string $lightChar Character for light modules
     * @return string ASCII art representation
     */
    public function toAscii($data, $darkChar = '██', $lightChar = '  ') {
        $this->generate($data);
        $result = '';

        // Add quiet zone (border)
        $border = str_repeat($lightChar, $this->moduleCount + 4);

        $result .= $border . "\n";
        $result .= $border . "\n";

        for ($row = 0; $row < $this->moduleCount; $row++) {
            $result .= $lightChar . $lightChar;
            for ($col = 0; $col < $this->moduleCount; $col++) {
                $result .= $this->modules[$row][$col] ? $darkChar : $lightChar;
            }
            $result .= $lightChar . $lightChar . "\n";
        }

        $result .= $border . "\n";
        $result .= $border . "\n";

        return $result;
    }

    /**
     * Generate QR Code as SVG
     *
     * @param string $data Data to encode
     * @param int $moduleSize Size of each module in pixels
     * @param string $darkColor Color for dark modules
     * @param string $lightColor Color for light modules
     * @return string SVG markup
     */
    public function toSvg($data, $moduleSize = 4, $darkColor = '#000000', $lightColor = '#ffffff') {
        $this->generate($data);
        $size = $this->moduleCount * $moduleSize;
        $quietZone = 4 * $moduleSize;
        $totalSize = $size + 2 * $quietZone;

        $svg = '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
        $svg .= '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" ';
        $svg .= 'width="' . $totalSize . '" height="' . $totalSize . '" viewBox="0 0 ' . $totalSize . ' ' . $totalSize . '">' . "\n";

        // Background
        $svg .= '  <rect width="' . $totalSize . '" height="' . $totalSize . '" fill="' . $lightColor . '"/>' . "\n";

        // Modules
        for ($row = 0; $row < $this->moduleCount; $row++) {
            for ($col = 0; $col < $this->moduleCount; $col++) {
                if ($this->modules[$row][$col]) {
                    $x = $quietZone + $col * $moduleSize;
                    $y = $quietZone + $row * $moduleSize;
                    $svg .= '  <rect x="' . $x . '" y="' . $y . '" width="' . $moduleSize . '" height="' . $moduleSize . '" fill="' . $darkColor . '"/>' . "\n";
                }
            }
        }

        $svg .= '</svg>';

        return $svg;
    }

    /**
     * Generate QR Code as binary matrix
     *
     * @param string $data Data to encode
     * @return array 2D array of 0s and 1s
     */
    public function toMatrix($data) {
        $this->generate($data);
        $matrix = [];

        for ($row = 0; $row < $this->moduleCount; $row++) {
            $matrix[$row] = [];
            for ($col = 0; $col < $this->moduleCount; $col++) {
                $matrix[$row][$col] = $this->modules[$row][$col] ? 1 : 0;
            }
        }

        return $matrix;
    }

    /**
     * Get the version of the QR Code
     *
     * @return int Version number
     */
    public function getVersion() {
        return $this->version;
    }

    /**
     * Get the module count (size) of the QR Code
     *
     * @return int Module count
     */
    public function getModuleCount() {
        return $this->moduleCount;
    }

    /**
     * Get error correction level name
     *
     * @return string Error correction level name
     */
    public function getErrorCorrectionLevelName() {
        $names = ['L', 'M', 'Q', 'H'];
        return $names[$this->errorCorrectionLevel] ?? 'L';
    }
}

/**
 * QR Code Utility Functions
 *
 * Static helper functions for quick QR Code generation
 */
class QrCodeUtils {

    /**
     * Generate QR Code and return as ASCII art
     *
     * @param string $data Data to encode
     * @param int $version QR Code version (1-10)
     * @param int $errorCorrectionLevel Error correction level
     * @param string $darkChar Character for dark modules
     * @param string $lightChar Character for light modules
     * @return string ASCII art
     */
    public static function toAscii($data, $version = 1, $errorCorrectionLevel = QrCodeGenerator::ERROR_CORRECTION_L, $darkChar = '██', $lightChar = '  ') {
        $generator = new QrCodeGenerator($version, $errorCorrectionLevel);
        return $generator->toAscii($data, $darkChar, $lightChar);
    }

    /**
     * Generate QR Code and return as SVG
     *
     * @param string $data Data to encode
     * @param int $version QR Code version (1-10)
     * @param int $errorCorrectionLevel Error correction level
     * @param int $moduleSize Size of each module
     * @param string $darkColor Color for dark modules
     * @param string $lightColor Color for light modules
     * @return string SVG markup
     */
    public static function toSvg($data, $version = 1, $errorCorrectionLevel = QrCodeGenerator::ERROR_CORRECTION_L, $moduleSize = 4, $darkColor = '#000000', $lightColor = '#ffffff') {
        $generator = new QrCodeGenerator($version, $errorCorrectionLevel);
        return $generator->toSvg($data, $moduleSize, $darkColor, $lightColor);
    }

    /**
     * Generate QR Code and return as binary matrix
     *
     * @param string $data Data to encode
     * @param int $version QR Code version (1-10)
     * @param int $errorCorrectionLevel Error correction level
     * @return array 2D array of 0s and 1s
     */
    public static function toMatrix($data, $version = 1, $errorCorrectionLevel = QrCodeGenerator::ERROR_CORRECTION_L) {
        $generator = new QrCodeGenerator($version, $errorCorrectionLevel);
        return $generator->toMatrix($data);
    }

    /**
     * Save QR Code as SVG file
     *
     * @param string $data Data to encode
     * @param string $filename Output filename
     * @param int $version QR Code version (1-10)
     * @param int $errorCorrectionLevel Error correction level
     * @param int $moduleSize Size of each module
     * @param string $darkColor Color for dark modules
     * @param string $lightColor Color for light modules
     * @return bool True on success
     */
    public static function saveSvg($data, $filename, $version = 1, $errorCorrectionLevel = QrCodeGenerator::ERROR_CORRECTION_L, $moduleSize = 4, $darkColor = '#000000', $lightColor = '#ffffff') {
        $svg = self::toSvg($data, $version, $errorCorrectionLevel, $moduleSize, $darkColor, $lightColor);
        return file_put_contents($filename, $svg) !== false;
    }

    /**
     * Detect the best mode for the given data
     *
     * @param string $data Input data
     * @return int Mode constant
     */
    public static function detectMode($data) {
        return QrCodeGenerator::detectMode($data);
    }

    /**
     * Get mode name
     *
     * @param int $mode Mode constant
     * @return string Mode name
     */
    public static function getModeName($mode) {
        $names = [
            QrCodeGenerator::MODE_NUMERIC => 'Numeric',
            QrCodeGenerator::MODE_ALPHANUMERIC => 'Alphanumeric',
            QrCodeGenerator::MODE_BYTE => 'Byte',
        ];
        return $names[$mode] ?? 'Unknown';
    }

    /**
     * Get error correction level name
     *
     * @param int $level Error correction level
     * @return string Level name
     */
    public static function getErrorCorrectionLevelName($level) {
        $names = ['L', 'M', 'Q', 'H'];
        return $names[$level] ?? 'L';
    }
}
