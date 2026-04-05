<?php
/**
 * AllToolkit - QR Code Utilities Example
 *
 * Demonstrates various QR Code generation features and output formats.
 *
 * @package AllToolkit\QrCodeUtils
 */

require_once __DIR__ . '/../qr_code_utils/mod.php';

use AllToolkit\QrCodeGenerator;
use AllToolkit\QrCodeUtils;

echo "========================================\n";
echo "QR Code Utilities Example\n";
echo "========================================\n\n";

// Example 1: Basic ASCII QR Code
echo "Example 1: Basic ASCII QR Code\n";
echo "--------------------------------\n";
echo "Data: 'HELLO WORLD'\n\n";

$qr = new QrCodeGenerator(1, QrCodeGenerator::ERROR_CORRECTION_L);
echo $qr->toAscii("HELLO WORLD");
echo "\n";

// Example 2: Custom ASCII characters
echo "Example 2: Custom ASCII Characters\n";
echo "-----------------------------------\n";
echo "Data: 'TEST' with custom characters\n\n";

echo $qr->toAscii("TEST", "##", "..");
echo "\n";

// Example 3: Numeric data (most compact)
echo "Example 3: Numeric Data (Most Compact)\n";
echo "---------------------------------------\n";
echo "Data: '1234567890'\n\n";

echo $qr->toAscii("1234567890");
echo "\n";

// Example 4: Different versions
echo "Example 4: Different Versions\n";
echo "------------------------------\n";
echo "Data: 'VERSION TEST' with versions 1, 2, 3\n\n";

for ($v = 1; $v <= 3; $v++) {
    $qrV = new QrCodeGenerator($v, QrCodeGenerator::ERROR_CORRECTION_L);
    echo "Version {$v} ({$qrV->getModuleCount()}x{$qrV->getModuleCount()} modules):\n";
    echo $qrV->toAscii("VERSION TEST");
    echo "\n";
}

// Example 5: Different error correction levels
echo "Example 5: Error Correction Levels\n";
echo "-----------------------------------\n";
echo "Data: 'ERROR CORRECTION' with levels L, M, Q, H\n\n";

$levels = [
    QrCodeGenerator::ERROR_CORRECTION_L => 'L (~7%)',
    QrCodeGenerator::ERROR_CORRECTION_M => 'M (~15%)',
    QrCodeGenerator::ERROR_CORRECTION_Q => 'Q (~25%)',
    QrCodeGenerator::ERROR_CORRECTION_H => 'H (~30%)',
];

foreach ($levels as $level => $desc) {
    $qrE = new QrCodeGenerator(2, $level);
    echo "Level {$desc}:\n";
    echo $qrE->toAscii("ERROR CORRECTION");
    echo "\n";
}

// Example 6: Generate SVG output
echo "Example 6: SVG Output\n";
echo "----------------------\n";
echo "Data: 'SVG TEST'\n\n";

$svg = $qr->toSvg("SVG TEST", 4, '#000000', '#ffffff');
echo "SVG generated (length: " . strlen($svg) . " chars)\n";
echo "First 200 characters:\n";
echo substr($svg, 0, 200) . "...\n\n";

// Example 7: Custom colored SVG
echo "Example 7: Custom Colored SVG\n";
echo "------------------------------\n";
echo "Data: 'COLORED' with red on white\n\n";

$svgColored = $qr->toSvg("COLORED", 4, '#ff0000', '#ffffff');
echo "SVG with custom colors generated (length: " . strlen($svgColored) . " chars)\n\n";

// Example 8: Binary matrix output
echo "Example 8: Binary Matrix Output\n";
echo "--------------------------------\n";
echo "Data: 'MATRIX'\n\n";

$matrix = $qr->toMatrix("MATRIX");
echo "Matrix size: " . count($matrix) . "x" . count($matrix[0]) . "\n";
echo "First 5 rows:\n";
for ($i = 0; $i < min(5, count($matrix)); $i++) {
    for ($j = 0; $j < min(10, count($matrix[$i])); $j++) {
        echo $matrix[$i][$j];
    }
    echo "...\n";
}
echo "\n";

// Example 9: Mode detection
echo "Example 9: Mode Detection\n";
echo "--------------------------\n";

$testStrings = [
    "1234567890" => "Numeric",
    "HELLO WORLD" => "Alphanumeric",
    "Hello, World!" => "Byte",
    "test@example.com" => "Byte (email)",
];

foreach ($testStrings as $data => $desc) {
    $mode = QrCodeGenerator::detectMode($data);
    $modeName = QrCodeUtils::getModeName($mode);
    echo "'{$data}' => {$modeName} mode ({$desc})\n";
}
echo "\n";

// Example 10: Utility functions
echo "Example 10: Utility Functions\n";
echo "------------------------------\n";

// Quick ASCII generation
$ascii = QrCodeUtils::toAscii("QUICK", 2, QrCodeGenerator::ERROR_CORRECTION_M);
echo "Quick ASCII generation:\n";
echo $ascii;
echo "\n";

// Quick SVG generation
$svg = QrCodeUtils::toSvg("QUICK SVG", 2, QrCodeGenerator::ERROR_CORRECTION_M, 4, '#0000ff', '#ffffff');
echo "Quick SVG generation (length: " . strlen($svg) . " chars)\n\n";

// Example 11: Save SVG to file
echo "Example 11: Save SVG to File\n";
echo "-----------------------------\n";

$tempFile = sys_get_temp_dir() . '/qrcode_test.svg';
if (QrCodeUtils::saveSvg("SAVE TEST", $tempFile)) {
    echo "SVG saved to: {$tempFile}\n";
    echo "File size: " . filesize($tempFile) . " bytes\n";
    // Clean up
    unlink($tempFile);
} else {
    echo "Failed to save SVG\n";
}
echo "\n";

// Example 12: URL QR Code
echo "Example 12: URL QR Code\n";
echo "------------------------\n";
echo "Data: 'https://github.com/ayukyo/alltoolkit'\n\n";

$qrUrl = new QrCodeGenerator(3, QrCodeGenerator::ERROR_CORRECTION_M);
echo $qrUrl->toAscii("https://github.com/ayukyo/alltoolkit");
echo "\n";

// Example 13: WiFi QR Code (common use case)
echo "Example 13: WiFi QR Code\n";
echo "-------------------------\n";
echo "Data: 'WIFI:T:WPA;S:MyNetwork;P:MyPassword;;'\n\n";

$qrWifi = new QrCodeGenerator(2, QrCodeGenerator::ERROR_CORRECTION_H);
echo $qrWifi->toAscii("WIFI:T:WPA;S:MyNetwork;P:MyPassword;;");
echo "\n";

// Example 14: Email QR Code
echo "Example 14: Email QR Code\n";
echo "--------------------------\n";
echo "Data: 'mailto:test@example.com?subject=Hello'\n\n";

$qrEmail = new QrCodeGenerator(2, QrCodeGenerator::ERROR_CORRECTION_M);
echo $qrEmail->toAscii("mailto:test@example.com?subject=Hello");
echo "\n";

// Example 15: Large data with higher version
echo "Example 15: Large Data (Version 4)\n";
echo "------------------------------------\n";
echo "Data: 'THIS IS A LONGER TEXT THAT REQUIRES A LARGER QR CODE VERSION'\n\n";

$qrLarge = new QrCodeGenerator(4, QrCodeGenerator::ERROR_CORRECTION_L);
echo $qrLarge->toAscii("THIS IS A LONGER TEXT THAT REQUIRES A LARGER QR CODE VERSION");
echo "\n";

echo "========================================\n";
echo "Example Complete!\n";
echo "========================================\n";
