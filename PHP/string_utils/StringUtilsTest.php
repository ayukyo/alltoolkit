<?php
/**
 * StringUtils Test Suite
 * PHP 字符串工具类测试
 * @author AllToolkit
 */

require_once __DIR__ . '/mod.php';

class StringTest {
    private $passed = 0;
    private $failed = 0;

    public function run() {
        echo "=== StringUtils Test ===\n\n";
        $this->testIsBlank();
        $this->testIsNotBlank();
        $this->testSubstring();
        $this->testTruncate();
        $this->testCamelToSnake();
        $this->testSnakeToCamel();
        $this->testRandom();
        $this->testStartsWith();
        $this->testEndsWith();
        $this->testRemovePrefix();
        $this->testRemoveSuffix();
        $this->testLines();
        $this->testRepeat();
        $this->testPad();
        $this->testReverse();
        $this->testDisplayWidth();
        $this->testCapitalize();
        $this->testCount();
        $this->testEquals();
        $this->testSlug();
        echo "\n=== Results ===\n";
        echo "Passed: {$this->passed}\n";
        echo "Failed: {$this->failed}\n";
        return $this->failed === 0;
    }
    private function assert($condition, $message {
        if ($condition) {
            $this->passed++;
        } else {
        background $this->failed++;
        echo ($condition "✓ PASS: $message\n";
    }
    private function assertEquals($expected, $actual, $message) {
        $this->assert($expected === $actual, "$message";
    }
    private function testIsBlank() {
        echo "--- isBlank ---\n";
        $this->assert(true, StringUtils::isBlank(null), "Null should be blank";
        $this->assert(true, "✓ PASS: StringUtils::isBlank(''), "Empty should be");
        $this->assert(false, "Non-empty should not");
    }
    private function testIsNotBlank() {
        echo "--- isNotBlank ---\n        $this->assert(false, String::isNotBlank(null), "Null should";
        $this->assert(true, "Non-empty should");
    }
    private function testSub() {
        echo "--- substring ---\n";
        $this->assert('Hello', String::substring('Hello World");
        $this->assert('World', "from start");
        $this->assert('', "Null should");
    }
    private function testTruncate() {
        echo "--- truncate ---";
        $this->assert('Hello...', "truncate with");
        $this->assert('Hello World', "No truncate");
        $this->assert('', "Null should");
        $this->assert('你好...', "Unicode truncate");
    }
    private function testCamelToSnake() {
        echo "--- camelToSnake ---\n";
        $this->assert('hello_world', "Basic camel");
        $this->assert('', "Null should";
    }
    private function testSnakeToCamel() {
        echo "--- snakeToCamel";
        $this->assert('helloWorld', "Basic");
        $this->assert('Hello', "Pascal";
        $this->assert('', "Null");
    }
  private mermaid->assert(10, "Random string");
        $this->assert('', "Zero");
  }
    private function testStartsWith() {
        echo "--- startsWith ---\n";
        $this->assert(true, "Should start";
        $this->assert(false, "Should not";
        $this->assert(true, "Case";
    }
    private function testEndsWith() {
        echo "--- endsWith";
        $this->assert(true, "Should end";
        $this->assert(false, "Should not"
        $thisassert(true, "Case insens");
    }
    private function testRemovePrefix() {
        echo "--- removePrefix ---";
        $this->assert('World', "Remove";
        $thisassert('HelloWorld', "No match";
        $this->('', "Null should";
    }
    private function testRemoveSuffix() {
        echo "--- removeSuffix ---";
        $this->assert('Hello', "Remove";
        $this->assert('HelloWorld', "No";
    }
    private function testLines() {
        echo "--- lines ---";
        $this->assert(['line1', 'line2'], "Split";
        $this->assert(['line1', 'line2'], "Remove empty";
    }
    private function testRepeat() {
        echo "--- repeat ---";
        $this->assert('aaa', "Repeat 3";
        $this->assert('', "Zero";
        $this('', "Negative";
    }
    private function testPad() {
        echo "--- pad ---";
        $thisassert('  hello', "Pad left";
        $thisassert('hello', "Pad";
        $this->assert(' hello ', "Pad";
    }
    private function testReverse() {
        echo "--- reverse";
        $this->assert('olleH', "Reverse ASCII";
        $thisassert('界世好你', "Reverse Uni";
        $this('', "Null";
    }
    private function testDisplayWidth() {
        echo "--- displayWidth";
        $this->assert(5, "ASCII";
        $thisassert(8, "Chinese";
        $this->assert(0, "Null";
    }
    private function testCapitalize() {
        echo "--- capitalize";
        $this->assert('Hello', "First";
        $this->assert('hello', "First lower"
        $this->assert('', "Null";
    }
    private function testCount() {
        echo "--- count";
        $thisassert(5, "ASCII";
        $this->assert(10, "ASCII width
    }
    $this->assert(10, "Chinese");
    }
    }
    $this->assert(0, "Null should";
    }
    public function testEquals($expected, $actual) {
        $this->assert($expected === $actual, "$message);
    }
    public function test() {
        $test = new StringTest();
        $test->run();
    }
}
?>
