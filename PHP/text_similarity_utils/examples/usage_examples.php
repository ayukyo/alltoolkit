<?php
/**
 * TextSimilarityUtils 使用示例
 * 
 * 演示各种文本相似度计算方法的使用场景
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

require_once __DIR__ . '/../mod.php';

echo "=== TextSimilarityUtils 使用示例 ===\n\n";

// ============================================
// 1. 基础距离和相似度计算
// ============================================
echo "--- 1. 基础距离和相似度 ---\n";

$str1 = 'kitten';
$str2 = 'sitting';

echo "比较 '$str1' 和 '$str2':\n";
echo "  Levenshtein 距离: " . TextSimilarityUtils::levenshteinDistance($str1, $str2) . "\n";
echo "  Levenshtein 相似度: " . TextSimilarityUtils::levenshteinSimilarity($str1, $str2) . "\n";
echo "  Damerau-Levenshtein 距离: " . TextSimilarityUtils::damerauLevenshteinDistance($str1, $str2) . "\n";

// Hamming 距离（仅用于等长字符串）
$ham1 = 'hello';
$ham2 = 'hallo';
echo "\n比较 '$ham1' 和 '$ham2':\n";
echo "  Hamming 距离: " . TextSimilarityUtils::hammingDistance($ham1, $ham2) . "\n";
echo "  Hamming 相似度: " . TextSimilarityUtils::hammingSimilarity($ham1, $ham2) . "\n";

// ============================================
// 2. 集合类相似度
// ============================================
echo "\n--- 2. 集合类相似度 ---\n";

$str1 = 'hello';
$str2 = 'hallo';

echo "比较 '$str1' 和 '$str2':\n";
echo "  Jaccard 相似度: " . TextSimilarityUtils::jaccardSimilarity($str1, $str2) . "\n";
echo "  Dice 系数: " . TextSimilarityUtils::diceCoefficient($str1, $str2) . "\n";
echo "  Overlap 系数: " . TextSimilarityUtils::overlapCoefficient($str1, $str2) . "\n";

// N-gram Jaccard
echo "\nN-gram Jaccard 相似度（n=2,3,4）:\n";
for ($n = 2; $n <= 4; $n++) {
    echo "  n=$n: " . TextSimilarityUtils::ngramJaccardSimilarity($str1, $str2, $n) . "\n";
}

// ============================================
// 3. 向量类相似度
// ============================================
echo "\n--- 3. 向量类相似度 ---\n";

$str1 = 'hello world';
$str2 = 'hallo world';

echo "比较 '$str1' 和 '$str2':\n";
echo "  Cosine 相似度（字符向量）: " . TextSimilarityUtils::cosineSimilarity($str1, $str2) . "\n";
echo "  Cosine 相似度（词向量）: " . TextSimilarityUtils::wordCosineSimilarity($str1, $str2) . "\n";

// ============================================
// 4. 序列类相似度
// ============================================
echo "\n--- 4. 序列类相似度 ---\n";

$str1 = 'AGGTAB';
$str2 = 'GXTXAYB';

echo "比较 '$str1' 和 '$str2':\n";
echo "  LCS 长度: " . TextSimilarityUtils::lcsLength($str1, $str2) . "\n";
echo "  LCS 字符串: '" . TextSimilarityUtils::lcs($str1, $str2) . "'\n";
echo "  LCS 相似度: " . TextSimilarityUtils::lcsSimilarity($str1, $str2) . "\n";

// ============================================
// 5. 高级相似度算法
// ============================================
echo "\n--- 5. 高级相似度算法 ---\n";

$str1 = 'MARTHA';
$str2 = 'MARHTA';

echo "比较 '$str1' 和 '$str2':\n";
echo "  Jaro 相似度: " . TextSimilarityUtils::jaroSimilarity($str1, $str2) . "\n";
echo "  Jaro-Winkler 相似度: " . TextSimilarityUtils::jaroWinklerSimilarity($str1, $str2) . "\n";

// 前缀匹配优势
$str1 = 'duplicate';
$str2 = 'duplication';
echo "\n比较 '$str1' 和 '$str2':\n";
echo "  Jaro 相似度: " . TextSimilarityUtils::jaroSimilarity($str1, $str2) . "\n";
echo "  Jaro-Winkler 相似度: " . TextSimilarityUtils::jaroWinklerSimilarity($str1, $str2) . "\n";
echo "  （JW 对前缀匹配有加成）\n";

// ============================================
// 6. 综合相似度报告
// ============================================
echo "\n--- 6. 综合相似度报告 ---\n";

$result = TextSimilarityUtils::comprehensiveSimilarity('hello', 'hallo');
echo "比较 'hello' 和 'hallo' 的综合报告:\n";
foreach ($result as $key => $value) {
    printf("  %-25s: %.4f\n", $key, $value);
}

// ============================================
// 7. 实用场景：拼写纠错
// ============================================
echo "\n--- 7. 拼写纠错场景 ---\n";

$dictionary = ['apple', 'banana', 'orange', 'grape', 'kiwi', 'mango', 'pear'];
$misspelled = 'aple'; // 拼写错误

$result = TextSimilarityUtils::findMostSimilar($misspelled, $dictionary);
echo "输入: '$misspelled'（拼写错误）\n";
echo "最相似的正确单词: '$result['string']' (相似度: {$result['similarity']})\n";

// 获取多个候选
$candidates = TextSimilarityUtils::fuzzyMatch($misspelled, $dictionary, 0.6);
echo "所有可能的正确单词（阈值0.6）:\n";
foreach ($candidates as $c) {
    printf("  - %s (%.2f)\n", $c['string'], $c['similarity']);
}

// ============================================
// 8. 实用场景：搜索排序
// ============================================
echo "\n--- 8. 搜索排序场景 ---\n";

$products = [
    'iPhone 14 Pro',
    'iPhone 15 Pro',
    'iPhone 14',
    'iPhone 15',
    'iPhone 13',
    'iPad Pro',
    'iPad Air',
    'MacBook Pro',
    'MacBook Air',
];
$query = 'iphone pro';

$ranked = TextSimilarityUtils::rankBySimilarity($query, $products, 'jaro_winkler');
echo "搜索 '$query' 的结果:\n";
foreach ($ranked as $item) {
    printf("  %-20s (%.3f)\n", $item['string'], $item['similarity']);
}

// ============================================
// 9. 实用场景：文档去重
// ============================================
echo "\n--- 9. 文档去重场景 ---\n";

$docs = [
    'The quick brown fox jumps over the lazy dog.',
    'The quick brown fox jumped over the lazy dog.',
    'A quick brown fox jumps over the lazy dog.',
    'This is a completely different sentence.',
];

echo "检测文档相似度:\n";
$threshold = 0.85;
$duplicates = [];

for ($i = 0; $i < count($docs); $i++) {
    for ($j = $i + 1; $j < count($docs); $j++) {
        $sim = TextSimilarityUtils::wordCosineSimilarity($docs[$i], $docs[$j]);
        if ($sim >= $threshold) {
            $duplicates[] = [
                'doc1' => $i,
                'doc2' => $j,
                'similarity' => $sim,
            ];
        }
    }
}

if (empty($duplicates)) {
    echo "  无高度相似文档（阈值 $threshold）\n";
} else {
    foreach ($duplicates as $dup) {
        printf("  文档%d 和 文档%d 相似度: %.3f\n", 
            $dup['doc1'] + 1, $dup['doc2'] + 1, $dup['similarity']);
        echo "    '{$docs[$dup['doc1']]}'\n";
        echo "    '{$docs[$dup['doc2']]}'\n";
    }
}

// ============================================
// 10. 实用场景：地址匹配
// ============================================
echo "\n--- 10. 地址匹配场景 ---\n";

$addressDB = [
    '123 Main Street',
    '456 Oak Avenue',
    '789 Pine Road',
    '321 Elm Boulevard',
    '654 Maple Lane',
];
$inputAddress = '123 Main St'; // 简化写法

$result = TextSimilarityUtils::findMostSimilar($inputAddress, $addressDB);
echo "输入地址: '$inputAddress'\n";
echo "匹配到: '{$result['string']}' (相似度: {$result['similarity']})\n";

// ============================================
// 11. 实用场景：代码差异检测
// ============================================
echo "\n--- 11. 代码差异检测 ---\n";

$code1 = 'function add(a, b) { return a + b; }';
$code2 = 'function add(a, b) { return a - b; }';

$lcs = TextSimilarityUtils::lcs($code1, $code2);
echo "代码1: '$code1'\n";
echo "代码2: '$code2'\n";
echo "公共部分: '$lcs'\n";
echo "相似度: " . TextSimilarityUtils::lcsSimilarity($code1, $code2) . "\n";

// ============================================
// 12. 实用场景：用户名相似检测
// ============================================
echo "\n--- 12. 用户名相似检测 ---\n";

$existingUsers = ['john_doe', 'jane_doe', 'john_smith', 'jsmith', 'jdoe'];
$newUser = 'john_doe1';

$similarUsers = TextSimilarityUtils::fuzzyMatch($newUser, $existingUsers, 0.8);
echo "新用户名: '$newUser'\n";
if (empty($similarUsers)) {
    echo "  无相似用户名，可以使用\n";
} else {
    echo "  发现相似用户名:\n";
    foreach ($similarUsers as $u) {
        printf("    - %s (%.2f)\n", $u['string'], $u['similarity']);
    }
    echo "  建议: 选择不同的用户名以避免混淆\n";
}

// ============================================
// 13. 性能测试
// ============================================
echo "\n--- 13. 性能测试 ---\n";

$longStr1 = str_repeat('abcdefghij', 100);
$longStr2 = str_repeat('abcdefghik', 100);

echo "测试字符串长度: " . strlen($longStr1) . " 字符\n";

$methods = ['levenshtein', 'jaccard', 'cosine', 'dice', 'jaro', 'jaro_winkler', 'lcs'];
foreach ($methods as $method) {
    $start = microtime(true);
    $sim = TextSimilarityUtils::findMostSimilar($longStr1, [$longStr2], $method)['similarity'];
    $time = microtime(true) - $start;
    printf("  %-15s: %.4f (耗时: %.3f秒)\n", $method, $sim, $time);
}

echo "\n=== 示例完成 ===\n";