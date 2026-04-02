<?php
/**
 * StringUtils 使用示例
 * 
 * 演示 StringUtils 工具类的各种用法
 * 
 * 运行方式: php ExampleStringUtils.php
 */

require_once 'StringUtils.php';

echo "=== StringUtils 使用示例 ===\n\n";

// 1. 空值检查
echo "【1. 空值检查】\n";
echo "isBlank(''): " . (StringUtils::isBlank('') ? 'true' : 'false') . "\n";
echo "isBlank('   '): " . (StringUtils::isBlank('   ') ? 'true' : 'false') . "\n";
echo "isBlank(null): " . (StringUtils::isBlank(null) ? 'true' : 'false') . "\n";
echo "isBlank('hello'): " . (StringUtils::isBlank('hello') ? 'true' : 'false') . "\n";
echo "isNotBlank('hello'): " . (StringUtils::isNotBlank('hello') ? 'true' : 'false') . "\n\n";

// 2. 字符串截取
echo "【2. 字符串截取】\n";
$text = "Hello, World!";
echo "substring('$text', 0, 5): " . StringUtils::substring($text, 0, 5) . "\n";
echo "substring('$text', 7): " . StringUtils::substring($text, 7) . "\n";

$chineseText = "这是一段中文文本";
echo "substring('$chineseText', 2, 4): " . StringUtils::substring($chineseText, 2, 4) . "\n\n";

// 3. 截断字符串
echo "【3. 截断字符串】\n";
$longText = "这是一个很长的文本，需要被截断显示";
echo "truncate('$longText', 10): " . StringUtils::truncate($longText, 10) . "\n";
echo "truncate('$longText', 10, '>>'): " . StringUtils::truncate($longText, 10, '>>') . "\n\n";

// 4. 命名风格转换
echo "【4. 命名风格转换】\n";
echo "camelToSnake('camelCaseString'): " . StringUtils::camelToSnake('camelCaseString') . "\n";
echo "camelToSnake('getUserName'): " . StringUtils::camelToSnake('getUserName') . "\n";
echo "snakeToCamel('snake_case_string'): " . StringUtils::snakeToCamel('snake_case_string') . "\n";
echo "snakeToCamel('user_name', true): " . StringUtils::snakeToCamel('user_name', true) . "\n\n";

// 5. 随机字符串
echo "【5. 随机字符串】\n";
echo "random(8): " . StringUtils::random(8) . "\n";
echo "random(10, '0123456789'): " . StringUtils::random(10, '0123456789') . "\n";
echo "random(6, 'ABCDEF'): " . StringUtils::random(6, 'ABCDEF') . "\n\n";

// 6. 前缀后缀检查
echo "【6. 前缀后缀检查】\n";
$url = "https://example.com/path";
echo "startsWith('$url', 'https'): " . (StringUtils::startsWith($url, 'https') ? 'true' : 'false') . "\n";
echo "startsWith('$url', 'HTTPS', true): " . (StringUtils::startsWith($url, 'HTTPS', true) ? 'true' : 'false') . "\n";
echo "endsWith('$url', '.com'): " . (StringUtils::endsWith($url, '.com') ? 'true' : 'false') . "\n";
echo "endsWith('$url', '.COM', true): " . (StringUtils::endsWith($url, '.COM', true) ? 'true' : 'false') . "\n\n";

// 7. 移除前缀后缀
echo "【7. 移除前缀后缀】\n";
$fileName = "document.pdf";
echo "removePrefix('prefix_text', 'prefix_'): " . StringUtils::removePrefix('prefix_text', 'prefix_') . "\n";
echo "removeSuffix('$fileName', '.pdf'): " . StringUtils::removeSuffix($fileName, '.pdf') . "\n";
echo "removeSuffix('no_suffix', '.txt'): " . StringUtils::removeSuffix('no_suffix', '.txt') . "\n\n";

// 8. 按行分割
echo "【8. 按行分割】\n";
$multiLine = "第一行\n\n第二行\r\n第三行\n\n";
$lines = StringUtils::lines($multiLine);
echo "lines count: " . count($lines) . "\n";
foreach ($lines as $i => $line) {
    echo "  Line $i: '$line'\n";
}
echo "\n";

// 9. 重复和填充
echo "【9. 重复和填充】\n";
echo "repeat('*', 10): " . StringUtils::repeat('*', 10) . "\n";
echo "repeat('ab', 5): " . StringUtils::repeat('ab', 5) . "\n";
echo "pad('test', 10): '" . StringUtils::pad('test', 10) . "'\n";
echo "pad('test', 10, '0', STR_PAD_LEFT): '" . StringUtils::pad('test', 10, '0', STR_PAD_LEFT) . "'\n";
echo "pad('test', 10, '*', STR_PAD_BOTH): '" . StringUtils::pad('test', 10, '*', STR_PAD_BOTH) . "'\n\n";

// 10. 字符串反转
echo "【10. 字符串反转】\n";
echo "reverse('Hello'): " . StringUtils::reverse('Hello') . "\n";
echo "reverse('中文测试'): " . StringUtils::reverse('中文测试') . "\n\n";

// 11. 显示宽度计算
echo "【11. 显示宽度计算】\n";
echo "displayWidth('Hello'): " . StringUtils::displayWidth('Hello') . "\n";
echo "displayWidth('中文'): " . StringUtils::displayWidth('中文') . "\n";
echo "displayWidth('Hello中文'): " . StringUtils::displayWidth('Hello中文') . "\n\n";

// 12. 首字母大小写转换
echo "【12. 首字母大小写转换】\n";
echo "capitalize('hello world'): " . StringUtils::capitalize('hello world') . "\n";
echo "capitalize('中文开头'): " . StringUtils::capitalize('中文开头') . "\n";
echo "uncapitalize('Hello World'): " . StringUtils::uncapitalize('Hello World') . "\n\n";

// 13. 子串计数
echo "【13. 子串计数】\n";
$countText = "banana";
echo "count('$countText', 'a'): " . StringUtils::count($countText, 'a') . "\n";
echo "count('$countText', 'na'): " . StringUtils::count($countText, 'na') . "\n";
echo "count('Hello World', 'o', true): " . StringUtils::count('Hello World', 'O', true) . "\n\n";

// 14. 字符串比较
echo "【14. 字符串比较】\n";
echo "equals('abc', 'abc'): " . (StringUtils::equals('abc', 'abc') ? 'true' : 'false') . "\n";
echo "equals('abc', 'ABC'): " . (StringUtils::equals('abc', 'ABC') ? 'true' : 'false') . "\n";
echo "equals('abc', 'ABC', true): " . (StringUtils::equals('abc', 'ABC', true) ? 'true' : 'false') . "\n";
echo "equals(null, null): " . (StringUtils::equals(null, null) ? 'true' : 'false') . "\n\n";

// 15. URL Slug生成
echo "【15. URL Slug生成】\n";
echo "slug('Hello World'): " . StringUtils::slug('Hello World') . "\n";
echo "slug('PHP is Great!'): " . StringUtils::slug('PHP is Great!') . "\n";
echo "slug('Hello World', '_'): " . StringUtils::slug('Hello World', '_') . "\n";

echo "\n=== 示例运行完毕 ===\n";
