<?php
/**
 * TextSimilarityUtils 测试类
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

require_once __DIR__ . '/mod.php';

class TextSimilarityUtilsTest
{
    private int $passed = 0;
    private int $failed = 0;
    private array $errors = [];

    public function run(): void
    {
        echo "=== TextSimilarityUtils 测试开始 ===\n\n";
        
        // Levenshtein 测试
        $this->testLevenshteinDistance();
        $this->testLevenshteinSimilarity();
        
        // Damerau-Levenshtein 测试
        $this->testDamerauLevenshteinDistance();
        
        // Hamming 测试
        $this->testHammingDistance();
        $this->testHammingSimilarity();
        
        // Jaccard 测试
        $this->testJaccardSimilarity();
        $this->testNgramJaccardSimilarity();
        
        // Cosine 测试
        $this->testCosineSimilarity();
        $this->testWordCosineSimilarity();
        
        // LCS 测试
        $this->testLcsLength();
        $this->testLcs();
        $this->testLcsSimilarity();
        
        // Dice 测试
        $this->testDiceCoefficient();
        
        // Jaro 测试
        $this->testJaroSimilarity();
        $this->testJaroWinklerSimilarity();
        
        // Overlap 测试
        $this->testOverlapCoefficient();
        
        // N-gram 测试
        $this->testNgramSimilarity();
        
        // 综合测试
        $this->testComprehensiveSimilarity();
        
        // 查找测试
        $this->testFindMostSimilar();
        $this->testRankBySimilarity();
        $this->testFuzzyMatch();
        
        // 判断测试
        $this->testIsSimilar();
        
        $this->printSummary();
    }

    private function assert(bool $condition, string $message): void
    {
        if ($condition) {
            $this->passed++;
            echo "  ✓ $message\n";
        } else {
            $this->failed++;
            $this->errors[] = $message;
            echo "  ✗ $message\n";
        }
    }

    private function assertEquals($expected, $actual, string $message): void
    {
        $this->assert($expected === $actual, "$message (期望: " . json_encode($expected) . ", 实际: " . json_encode($actual) . ")");
    }

    private function assertEqualsFloat(float $expected, float $actual, float $delta, string $message): void
    {
        $this->assert(abs($expected - $actual) < $delta, "$message (期望: $expected, 实际: $actual)");
    }

    private function testLevenshteinDistance(): void
    {
        echo "\n--- Levenshtein 距离测试 ---\n";
        
        $this->assertEquals(0, TextSimilarityUtils::levenshteinDistance('', ''), '空字符串距离为0');
        $this->assertEquals(3, TextSimilarityUtils::levenshteinDistance('', 'abc'), '插入3个字符');
        $this->assertEquals(3, TextSimilarityUtils::levenshteinDistance('abc', ''), '删除3个字符');
        $this->assertEquals(0, TextSimilarityUtils::levenshteinDistance('hello', 'hello'), '相同字符串距离为0');
        $this->assertEquals(1, TextSimilarityUtils::levenshteinDistance('kitten', 'sitten'), '替换1个字符');
        $this->assertEquals(3, TextSimilarityUtils::levenshteinDistance('kitten', 'sitting'), 'kitten -> sitting');
        $this->assertEquals(1, TextSimilarityUtils::levenshteinDistance('abc', 'abcd'), '插入1个字符');
        $this->assertEquals(1, TextSimilarityUtils::levenshteinDistance('abcd', 'abc'), '删除1个字符');
    }

    private function testLevenshteinSimilarity(): void
    {
        echo "\n--- Levenshtein 相似度测试 ---\n";
        
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::levenshteinSimilarity('', ''), 0.001, '空字符串相似度为1');
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::levenshteinSimilarity('hello', 'hello'), 0.001, '相同字符串相似度为1');
        $this->assertEqualsFloat(0.0, TextSimilarityUtils::levenshteinSimilarity('', 'abc'), 0.001, '空与非空相似度为0');
        $this->assertEqualsFloat(0.833, TextSimilarityUtils::levenshteinSimilarity('kitten', 'sitting'), 0.01, 'kitten vs sitting');
    }

    private function testDamerauLevenshteinDistance(): void
    {
        echo "\n--- Damerau-Levenshtein 距离测试 ---\n";
        
        $this->assertEquals(0, TextSimilarityUtils::damerauLevenshteinDistance('', ''), '空字符串距离为0');
        $this->assertEquals(0, TextSimilarityUtils::damerauLevenshteinDistance('abc', 'abc'), '相同字符串距离为0');
        $this->assertEquals(1, TextSimilarityUtils::damerauLevenshteinDistance('ab', 'ba'), '交换相邻字符');
        $this->assertEquals(2, TextSimilarityUtils::damerauLevenshteinDistance('abc', 'acb'), '交换非相邻字符');
    }

    private function testHammingDistance(): void
    {
        echo "\n--- Hamming 距离测试 ---\n";
        
        $this->assertEquals(0, TextSimilarityUtils::hammingDistance('', ''), '空字符串距离为0');
        $this->assertEquals(0, TextSimilarityUtils::hammingDistance('hello', 'hello'), '相同字符串距离为0');
        $this->assertEquals(1, TextSimilarityUtils::hammingDistance('hello', 'hallo'), '1个字符不同');
        $this->assertEquals(3, TextSimilarityUtils::hammingDistance('karolin', 'kathrin'), 'karolin vs kathrin');
        
        // 测试不等长异常
        try {
            TextSimilarityUtils::hammingDistance('abc', 'ab');
            $this->assert(false, '不等长字符串应抛出异常');
        } catch (InvalidArgumentException $e) {
            $this->assert(true, '不等长字符串正确抛出异常');
        }
    }

    private function testHammingSimilarity(): void
    {
        echo "\n--- Hamming 相似度测试 ---\n";
        
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::hammingSimilarity('hello', 'hello'), 0.001, '相同字符串相似度为1');
        $this->assertEqualsFloat(0.8, TextSimilarityUtils::hammingSimilarity('hello', 'hallo'), 0.001, '1/5不同');
    }

    private function testJaccardSimilarity(): void
    {
        echo "\n--- Jaccard 相似度测试 ---\n";
        
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::jaccardSimilarity('', ''), 0.001, '空字符串相似度为1');
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::jaccardSimilarity('abc', 'abc'), 0.001, '相同字符串相似度为1');
        $this->assertEqualsFloat(0.0, TextSimilarityUtils::jaccardSimilarity('abc', 'xyz'), 0.001, '无交集');
        
        $sim = TextSimilarityUtils::jaccardSimilarity('hello', 'hallo');
        $this->assert($sim > 0 && $sim < 1, "Jaccard 相似度在0和1之间: $sim");
    }

    private function testNgramJaccardSimilarity(): void
    {
        echo "\n--- N-gram Jaccard 相似度测试 ---\n";
        
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::ngramJaccardSimilarity('abc', 'abc', 2), 0.001, '相同字符串N-gram Jaccard为1');
        $this->assert(TextSimilarityUtils::ngramJaccardSimilarity('hello', 'hallo', 2) > 0, '有交集');
    }

    private function testCosineSimilarity(): void
    {
        echo "\n--- Cosine 相似度测试 ---\n";
        
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::cosineSimilarity('', ''), 0.001, '空字符串相似度为1');
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::cosineSimilarity('abc', 'abc'), 0.001, '相同字符串相似度为1');
        $this->assertEqualsFloat(0.0, TextSimilarityUtils::cosineSimilarity('abc', 'xyz'), 0.001, '无交集');
        
        $sim = TextSimilarityUtils::cosineSimilarity('hello', 'hallo');
        $this->assert($sim > 0 && $sim <= 1, "Cosine 相似度在0和1之间: $sim");
    }

    private function testWordCosineSimilarity(): void
    {
        echo "\n--- 词频 Cosine 相似度测试 ---\n";
        
        $sim = TextSimilarityUtils::wordCosineSimilarity('hello world', 'hello world');
        $this->assertEqualsFloat(1.0, $sim, 0.001, '相同词序列相似度为1');
        
        $sim = TextSimilarityUtils::wordCosineSimilarity('hello world', 'world hello');
        $this->assertEqualsFloat(1.0, $sim, 0.001, '相同词不同顺序相似度为1');
        
        $sim = TextSimilarityUtils::wordCosineSimilarity('hello world', 'hello');
        $this->assert($sim > 0 && $sim < 1, "部分匹配相似度在0和1之间: $sim");
    }

    private function testLcsLength(): void
    {
        echo "\n--- LCS 长度测试 ---\n";
        
        $this->assertEquals(0, TextSimilarityUtils::lcsLength('', ''), '空字符串LCS为0');
        $this->assertEquals(3, TextSimilarityUtils::lcsLength('abc', 'abc'), '相同字符串LCS为长度');
        $this->assertEquals(4, TextSimilarityUtils::lcsLength('abcde', 'ace'), 'abcde vs ace LCS为3');
        $this->assertEquals(3, TextSimilarityUtils::lcsLength('AGGTAB', 'GXTXAYB'), 'AGGTAB vs GXTXAYB');
    }

    private function testLcs(): void
    {
        echo "\n--- LCS 字符串测试 ---\n";
        
        $this->assertEquals('', TextSimilarityUtils::lcs('', ''), '空字符串LCS为空');
        $this->assertEquals('abc', TextSimilarityUtils::lcs('abc', 'abc'), '相同字符串LCS为原串');
        $this->assertEquals('ace', TextSimilarityUtils::lcs('abcde', 'ace'), 'abcde vs ace');
        $this->assertEquals('GTAB', TextSimilarityUtils::lcs('AGGTAB', 'GXTXAYB'), 'AGGTAB vs GXTXAYB');
    }

    private function testLcsSimilarity(): void
    {
        echo "\n--- LCS 相似度测试 ---\n";
        
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::lcsSimilarity('', ''), 0.001, '空字符串相似度为1');
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::lcsSimilarity('abc', 'abc'), 0.001, '相同字符串相似度为1');
        $this->assert(TextSimilarityUtils::lcsSimilarity('abc', 'xyz') === 0.0, '无公共子序列相似度为0');
    }

    private function testDiceCoefficient(): void
    {
        echo "\n--- Dice 系数测试 ---\n";
        
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::diceCoefficient('', ''), 0.001, '空字符串Dice为1');
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::diceCoefficient('abc', 'abc'), 0.001, '相同字符串Dice为1');
        $this->assertEqualsFloat(0.0, TextSimilarityUtils::diceCoefficient('a', 'b'), 0.001, '单字符不同Dice为0');
        
        $sim = TextSimilarityUtils::diceCoefficient('hello', 'hallo');
        $this->assert($sim > 0 && $sim < 1, "Dice 系数在0和1之间: $sim");
    }

    private function testJaroSimilarity(): void
    {
        echo "\n--- Jaro 相似度测试 ---\n";
        
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::jaroSimilarity('', ''), 0.001, '空字符串Jaro为1');
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::jaroSimilarity('abc', 'abc'), 0.001, '相同字符串Jaro为1');
        $this->assertEqualsFloat(0.0, TextSimilarityUtils::jaroSimilarity('abc', 'xyz'), 0.001, '无匹配Jaro为0');
        
        $sim = TextSimilarityUtils::jaroSimilarity('MARTHA', 'MARHTA');
        $this->assert($sim > 0.9, "MARTHA vs MARHTA Jaro > 0.9: $sim");
    }

    private function testJaroWinklerSimilarity(): void
    {
        echo "\n--- Jaro-Winkler 相似度测试 ---\n";
        
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::jaroWinklerSimilarity('', ''), 0.001, '空字符串JW为1');
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::jaroWinklerSimilarity('abc', 'abc'), 0.001, '相同字符串JW为1');
        
        // Jaro-Winkler 应该比 Jaro 更高（有前缀匹配加成）
        $jw = TextSimilarityUtils::jaroWinklerSimilarity('hello', 'hallo');
        $jaro = TextSimilarityUtils::jaroSimilarity('hello', 'hallo');
        $this->assert($jw >= $jaro, "JW($jw) >= Jaro($jaro)");
        
        // 前缀匹配测试
        $sim = TextSimilarityUtils::jaroWinklerSimilarity('prefix-test', 'prefix-demo');
        $this->assert($sim > 0.8, "相同前缀JW > 0.8: $sim");
    }

    private function testOverlapCoefficient(): void
    {
        echo "\n--- Overlap 系数测试 ---\n";
        
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::overlapCoefficient('', ''), 0.001, '空字符串Overlap为1');
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::overlapCoefficient('abc', 'abc'), 0.001, '相同字符串Overlap为1');
        $this->assertEqualsFloat(0.0, TextSimilarityUtils::overlapCoefficient('abc', 'xyz'), 0.001, '无交集Overlap为0');
    }

    private function testNgramSimilarity(): void
    {
        echo "\n--- N-gram 相似度测试 ---\n";
        
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::ngramSimilarity('', '', 2), 0.001, '空字符串相似度为1');
        $this->assertEqualsFloat(1.0, TextSimilarityUtils::ngramSimilarity('abc', 'abc', 2), 0.001, '相同字符串相似度为1');
        $this->assertEqualsFloat(0.0, TextSimilarityUtils::ngramSimilarity('ab', 'cd', 2), 0.001, '无交集相似度为0');
    }

    private function testComprehensiveSimilarity(): void
    {
        echo "\n--- 综合相似度测试 ---\n";
        
        $result = TextSimilarityUtils::comprehensiveSimilarity('hello', 'hallo');
        
        $this->assert(isset($result['levenshtein_similarity']), '包含 Levenshtein 相似度');
        $this->assert(isset($result['jaccard_similarity']), '包含 Jaccard 相似度');
        $this->assert(isset($result['cosine_similarity']), '包含 Cosine 相似度');
        $this->assert(isset($result['dice_coefficient']), '包含 Dice 系数');
        $this->assert(isset($result['jaro_similarity']), '包含 Jaro 相似度');
        $this->assert(isset($result['jaro_winkler_similarity']), '包含 Jaro-Winkler 相似度');
        $this->assert(isset($result['lcs_similarity']), '包含 LCS 相似度');
        $this->assert(isset($result['ngram_similarity']), '包含 N-gram 相似度');
        $this->assert(isset($result['average']), '包含平均值');
        
        $this->assert($result['average'] > 0 && $result['average'] <= 1, "平均值在合理范围: {$result['average']}");
    }

    private function testFindMostSimilar(): void
    {
        echo "\n--- 查找最相似字符串测试 ---\n";
        
        $candidates = ['apple', 'banana', 'orange', 'grape'];
        
        $result = TextSimilarityUtils::findMostSimilar('aple', $candidates); // 故意拼写错误
        $this->assertEquals('apple', $result['string'], '找到 apple 作为最相似');
        $this->assert($result['similarity'] > 0.8, "相似度 > 0.8: {$result['similarity']}");
        
        // 测试不同方法
        $result = TextSimilarityUtils::findMostSimilar('banna', $candidates, 'levenshtein');
        $this->assertEquals('banana', $result['string'], '使用 Levenshtein 找到 banana');
    }

    private function testRankBySimilarity(): void
    {
        echo "\n--- 按相似度排序测试 ---\n";
        
        $candidates = ['hello', 'hallo', 'hola', 'world'];
        $ranked = TextSimilarityUtils::rankBySimilarity('hello', $candidates);
        
        $this->assertEquals(4, count($ranked), '返回4个结果');
        $this->assertEquals('hello', $ranked[0]['string'], '第一个是 hello');
        $this->assertEqualsFloat(1.0, $ranked[0]['similarity'], 0.001, 'hello 相似度为1');
        
        // 检查降序排列
        for ($i = 1; $i < count($ranked); $i++) {
            $this->assert(
                $ranked[$i - 1]['similarity'] >= $ranked[$i]['similarity'],
                "结果按相似度降序排列"
            );
        }
    }

    private function testFuzzyMatch(): void
    {
        echo "\n--- 模糊匹配测试 ---\n";
        
        $candidates = ['apple', 'application', 'banana', 'orange', 'applet'];
        $matches = TextSimilarityUtils::fuzzyMatch('aple', $candidates, 0.7);
        
        $this->assert(count($matches) >= 2, "至少有2个匹配");
        $matchedStrings = array_column($matches, 'string');
        $this->assert(in_array('apple', $matchedStrings), '包含 apple');
        $this->assert(in_array('applet', $matchedStrings), '包含 applet');
        
        // 测试高阈值
        $matches = TextSimilarityUtils::fuzzyMatch('aple', $candidates, 0.9);
        $this->assert(count($matches) <= 2, "高阈值匹配数较少");
    }

    private function testIsSimilar(): void
    {
        echo "\n--- 相似判断测试 ---\n";
        
        $this->assert(TextSimilarityUtils::isSimilar('hello', 'hello'), '相同字符串相似');
        $this->assert(TextSimilarityUtils::isSimilar('hello', 'hallo', 0.7), 'hello vs hallo 相似（阈值0.7）');
        $this->assert(!TextSimilarityUtils::isSimilar('hello', 'world', 0.7), 'hello vs world 不相似（阈值0.7）');
        $this->assert(TextSimilarityUtils::isSimilar('hello', 'world', 0.1), 'hello vs world 相似（极低阈值）');
        
        // 测试不同方法
        $this->assert(
            TextSimilarityUtils::isSimilar('hello', 'hallo', 0.8, 'levenshtein'),
            '使用 Levenshtein 方法判断相似'
        );
    }

    private function printSummary(): void
    {
        echo "\n=== 测试总结 ===\n";
        echo "通过: {$this->passed}\n";
        echo "失败: {$this->failed}\n";
        echo "总计: " . ($this->passed + $this->failed) . "\n";
        
        if ($this->failed > 0) {
            echo "\n失败的测试:\n";
            foreach ($this->errors as $error) {
                echo "  - $error\n";
            }
            exit(1);
        } else {
            echo "\n✓ 所有测试通过！\n";
            exit(0);
        }
    }
}

// 运行测试
$test = new TextSimilarityUtilsTest();
$test->run();