<?php
/**
 * TextSimilarityUtils - PHP 文本相似度计算工具类
 * 
 * 提供多种文本相似度计算方法，无外部依赖，可直接复用
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

class TextSimilarityUtils
{
    /**
     * 计算 Levenshtein 距离（编辑距离）
     * 
     * 返回将 str1 转换为 str2 所需的最少编辑操作次数
     * 编辑操作包括：插入、删除、替换
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return int Levenshtein 距离
     */
    public static function levenshteinDistance(string $str1, string $str2): int
    {
        $len1 = strlen($str1);
        $len2 = strlen($str2);
        
        // 边界情况
        if ($len1 === 0) return $len2;
        if ($len2 === 0) return $len1;
        
        // 使用一维数组优化空间复杂度
        $prev = range(0, $len2);
        $curr = array_fill(0, $len2 + 1, 0);
        
        for ($i = 1; $i <= $len1; $i++) {
            $curr[0] = $i;
            for ($j = 1; $j <= $len2; $j++) {
                $cost = ($str1[$i - 1] === $str2[$j - 1]) ? 0 : 1;
                $curr[$j] = min(
                    $prev[$j] + 1,        // 删除
                    $curr[$j - 1] + 1,    // 插入
                    $prev[$j - 1] + $cost // 替换
                );
            }
            $prev = $curr;
        }
        
        return $curr[$len2];
    }

    /**
     * 计算 Levenshtein 相似度（归一化到 0-1 范围）
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return float 相似度，范围 0-1
     */
    public static function levenshteinSimilarity(string $str1, string $str2): float
    {
        $maxLen = max(strlen($str1), strlen($str2));
        if ($maxLen === 0) return 1.0;
        
        $distance = self::levenshteinDistance($str1, $str2);
        return 1.0 - ($distance / $maxLen);
    }

    /**
     * 计算 Damerau-Levenshtein 距离
     * 
     * 与 Levenshtein 相比，额外支持相邻字符交换操作
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return int Damerau-Levenshtein 距离
     */
    public static function damerauLevenshteinDistance(string $str1, string $str2): int
    {
        $len1 = strlen($str1);
        $len2 = strlen($str2);
        
        if ($len1 === 0) return $len2;
        if ($len2 === 0) return $len1;
        
        // 创建距离矩阵
        $matrix = [];
        for ($i = 0; $i <= $len1; $i++) {
            $matrix[$i] = [];
            for ($j = 0; $j <= $len2; $j++) {
                $matrix[$i][$j] = 0;
            }
        }
        
        // 初始化第一行和第一列
        for ($i = 0; $i <= $len1; $i++) $matrix[$i][0] = $i;
        for ($j = 0; $j <= $len2; $j++) $matrix[0][$j] = $j;
        
        // 填充矩阵
        for ($i = 1; $i <= $len1; $i++) {
            for ($j = 1; $j <= $len2; $j++) {
                $cost = ($str1[$i - 1] === $str2[$j - 1]) ? 0 : 1;
                
                $matrix[$i][$j] = min(
                    $matrix[$i - 1][$j] + 1,      // 删除
                    $matrix[$i][$j - 1] + 1,      // 插入
                    $matrix[$i - 1][$j - 1] + $cost // 替换
                );
                
                // 检查相邻字符交换
                if ($i > 1 && $j > 1 && 
                    $str1[$i - 1] === $str2[$j - 2] && 
                    $str1[$i - 2] === $str2[$j - 1]) {
                    $matrix[$i][$j] = min(
                        $matrix[$i][$j],
                        $matrix[$i - 2][$j - 2] + $cost // 交换
                    );
                }
            }
        }
        
        return $matrix[$len1][$len2];
    }

    /**
     * 计算 Hamming 距离
     * 
     * 仅适用于等长字符串，返回不同位置的数量
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return int Hamming 距离
     * @throws InvalidArgumentException 当字符串长度不等时
     */
    public static function hammingDistance(string $str1, string $str2): int
    {
        $len1 = strlen($str1);
        $len2 = strlen($str2);
        
        if ($len1 !== $len2) {
            throw new InvalidArgumentException("Hamming 距离要求两个字符串长度相等，得到长度 $len1 和 $len2");
        }
        
        $distance = 0;
        for ($i = 0; $i < $len1; $i++) {
            if ($str1[$i] !== $str2[$i]) {
                $distance++;
            }
        }
        
        return $distance;
    }

    /**
     * 计算 Hamming 相似度
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return float 相似度，范围 0-1
     * @throws InvalidArgumentException 当字符串长度不等时
     */
    public static function hammingSimilarity(string $str1, string $str2): float
    {
        $len = strlen($str1);
        if ($len === 0) return 1.0;
        
        $distance = self::hammingDistance($str1, $str2);
        return 1.0 - ($distance / $len);
    }

    /**
     * 计算 Jaccard 相似度
     * 
     * 基于字符集合的交集与并集比率
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return float 相似度，范围 0-1
     */
    public static function jaccardSimilarity(string $str1, string $str2): float
    {
        $set1 = array_unique(str_split($str1));
        $set2 = array_unique(str_split($str2));
        
        $intersection = array_intersect($set1, $set2);
        $union = array_unique(array_merge($set1, $set2));
        
        $unionCount = count($union);
        if ($unionCount === 0) return 1.0;
        
        return count($intersection) / $unionCount;
    }

    /**
     * 计算 N-gram Jaccard 相似度
     * 
     * 基于 N-gram 集合的 Jaccard 相似度
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @param int $n N-gram 大小，默认 2
     * @return float 相似度，范围 0-1
     */
    public static function ngramJaccardSimilarity(string $str1, string $str2, int $n = 2): float
    {
        $ngrams1 = self::getNgrams($str1, $n);
        $ngrams2 = self::getNgrams($str2, $n);
        
        $intersection = array_intersect($ngrams1, $ngrams2);
        $union = array_unique(array_merge($ngrams1, $ngrams2));
        
        $unionCount = count($union);
        if ($unionCount === 0) return 1.0;
        
        return count($intersection) / $unionCount;
    }

    /**
     * 生成 N-gram 列表
     *
     * @param string $str 输入字符串
     * @param int $n N-gram 大小
     * @return array N-gram 列表
     */
    private static function getNgrams(string $str, int $n): array
    {
        $len = strlen($str);
        if ($len < $n || $n < 1) return [];
        
        $ngrams = [];
        for ($i = 0; $i <= $len - $n; $i++) {
            $ngrams[] = substr($str, $i, $n);
        }
        
        return $ngrams;
    }

    /**
     * 计算余弦相似度（基于字符向量）
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return float 相似度，范围 0-1
     */
    public static function cosineSimilarity(string $str1, string $str2): float
    {
        $chars1 = count_chars($str1, 1);
        $chars2 = count_chars($str2, 1);
        
        // 获取所有字符的并集
        $allChars = array_unique(array_merge(array_keys($chars1), array_keys($chars2)));
        
        $dotProduct = 0;
        $norm1 = 0;
        $norm2 = 0;
        
        foreach ($allChars as $char) {
            $v1 = $chars1[$char] ?? 0;
            $v2 = $chars2[$char] ?? 0;
            
            $dotProduct += $v1 * $v2;
            $norm1 += $v1 * $v1;
            $norm2 += $v2 * $v2;
        }
        
        $norm = sqrt($norm1) * sqrt($norm2);
        if ($norm === 0.0) return 1.0;
        
        return $dotProduct / $norm;
    }

    /**
     * 计算词频余弦相似度
     * 
     * 基于词频向量的余弦相似度，适用于句子/文档比较
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @param string $delimiter 分词分隔符，默认空格
     * @return float 相似度，范围 0-1
     */
    public static function wordCosineSimilarity(string $str1, string $str2, string $delimiter = ' '): float
    {
        $words1 = array_filter(explode($delimiter, strtolower($str1)));
        $words2 = array_filter(explode($delimiter, strtolower($str2)));
        
        $freq1 = array_count_values($words1);
        $freq2 = array_count_values($words2);
        
        $allWords = array_unique(array_merge(array_keys($freq1), array_keys($freq2)));
        
        $dotProduct = 0;
        $norm1 = 0;
        $norm2 = 0;
        
        foreach ($allWords as $word) {
            $v1 = $freq1[$word] ?? 0;
            $v2 = $freq2[$word] ?? 0;
            
            $dotProduct += $v1 * $v2;
            $norm1 += $v1 * $v1;
            $norm2 += $v2 * $v2;
        }
        
        $norm = sqrt($norm1) * sqrt($norm2);
        if ($norm === 0.0) return 1.0;
        
        return $dotProduct / $norm;
    }

    /**
     * 计算最长公共子序列长度
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return int LCS 长度
     */
    public static function lcsLength(string $str1, string $str2): int
    {
        $len1 = strlen($str1);
        $len2 = strlen($str2);
        
        // 使用滚动数组优化空间
        $prev = array_fill(0, $len2 + 1, 0);
        $curr = array_fill(0, $len2 + 1, 0);
        
        for ($i = 1; $i <= $len1; $i++) {
            for ($j = 1; $j <= $len2; $j++) {
                if ($str1[$i - 1] === $str2[$j - 1]) {
                    $curr[$j] = $prev[$j - 1] + 1;
                } else {
                    $curr[$j] = max($prev[$j], $curr[$j - 1]);
                }
            }
            $prev = $curr;
            $curr = array_fill(0, $len2 + 1, 0);
        }
        
        return $prev[$len2];
    }

    /**
     * 获取最长公共子序列
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return string 最长公共子序列
     */
    public static function lcs(string $str1, string $str2): string
    {
        $len1 = strlen($str1);
        $len2 = strlen($str2);
        
        // 构建 DP 表
        $dp = [];
        for ($i = 0; $i <= $len1; $i++) {
            $dp[$i] = array_fill(0, $len2 + 1, 0);
        }
        
        for ($i = 1; $i <= $len1; $i++) {
            for ($j = 1; $j <= $len2; $j++) {
                if ($str1[$i - 1] === $str2[$j - 1]) {
                    $dp[$i][$j] = $dp[$i - 1][$j - 1] + 1;
                } else {
                    $dp[$i][$j] = max($dp[$i - 1][$j], $dp[$i][$j - 1]);
                }
            }
        }
        
        // 回溯构建 LCS
        $result = '';
        $i = $len1;
        $j = $len2;
        
        while ($i > 0 && $j > 0) {
            if ($str1[$i - 1] === $str2[$j - 1]) {
                $result = $str1[$i - 1] . $result;
                $i--;
                $j--;
            } elseif ($dp[$i - 1][$j] > $dp[$i][$j - 1]) {
                $i--;
            } else {
                $j--;
            }
        }
        
        return $result;
    }

    /**
     * 计算 LCS 相似度
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return float 相似度，范围 0-1
     */
    public static function lcsSimilarity(string $str1, string $str2): float
    {
        $maxLen = max(strlen($str1), strlen($str2));
        if ($maxLen === 0) return 1.0;
        
        $lcsLen = self::lcsLength($str1, $str2);
        return $lcsLen / $maxLen;
    }

    /**
     * 计算 Dice 系数
     * 
     * 基于 Bigram 的 Dice 系数
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return float Dice 系数，范围 0-1
     */
    public static function diceCoefficient(string $str1, string $str2): float
    {
        $bigrams1 = self::getNgrams($str1, 2);
        $bigrams2 = self::getNgrams($str2, 2);
        
        if (empty($bigrams1) && empty($bigrams2)) return 1.0;
        if (empty($bigrams1) || empty($bigrams2)) return 0.0;
        
        $intersection = count(array_intersect($bigrams1, $bigrams2));
        
        return (2.0 * $intersection) / (count($bigrams1) + count($bigrams2));
    }

    /**
     * 计算 Jaro 相似度
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return float Jaro 相似度，范围 0-1
     */
    public static function jaroSimilarity(string $str1, string $str2): float
    {
        $len1 = strlen($str1);
        $len2 = strlen($str2);
        
        if ($len1 === 0 && $len2 === 0) return 1.0;
        if ($len1 === 0 || $len2 === 0) return 0.0;
        
        $matchDistance = (int) floor(max($len1, $len2) / 2) - 1;
        if ($matchDistance < 0) $matchDistance = 0;
        
        $str1Matches = array_fill(0, $len1, false);
        $str2Matches = array_fill(0, $len2, false);
        
        $matches = 0;
        $transpositions = 0;
        
        // 查找匹配字符
        for ($i = 0; $i < $len1; $i++) {
            $start = max(0, $i - $matchDistance);
            $end = min($i + $matchDistance + 1, $len2);
            
            for ($j = $start; $j < $end; $j++) {
                if ($str2Matches[$j] || $str1[$i] !== $str2[$j]) continue;
                
                $str1Matches[$i] = true;
                $str2Matches[$j] = true;
                $matches++;
                break;
            }
        }
        
        if ($matches === 0) return 0.0;
        
        // 计算转置
        $k = 0;
        for ($i = 0; $i < $len1; $i++) {
            if (!$str1Matches[$i]) continue;
            
            while (!$str2Matches[$k]) $k++;
            
            if ($str1[$i] !== $str2[$k]) $transpositions++;
            $k++;
        }
        
        $jaro = ($matches / $len1 + $matches / $len2 + ($matches - $transpositions / 2) / $matches) / 3;
        
        return $jaro;
    }

    /**
     * 计算 Jaro-Winkler 相似度
     * 
     * Jaro 的改进版，对前缀匹配给予更高权重
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @param float $prefixScale 前缀缩放因子，默认 0.1
     * @return float Jaro-Winkler 相似度，范围 0-1
     */
    public static function jaroWinklerSimilarity(string $str1, string $str2, float $prefixScale = 0.1): float
    {
        $jaro = self::jaroSimilarity($str1, $str2);
        
        // 计算公共前缀长度（最多4个字符）
        $prefixLen = 0;
        $minLen = min(strlen($str1), strlen($str2), 4);
        
        for ($i = 0; $i < $minLen; $i++) {
            if ($str1[$i] === $str2[$i]) {
                $prefixLen++;
            } else {
                break;
            }
        }
        
        return $jaro + $prefixLen * $prefixScale * (1 - $jaro);
    }

    /**
     * 计算 Sørensen-Dice 系数
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return float Sørensen-Dice 系数，范围 0-1
     */
    public static function sorensenDiceCoefficient(string $str1, string $str2): float
    {
        return self::diceCoefficient($str1, $str2);
    }

    /**
     * 计算 Overlap 系数
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return float Overlap 系数，范围 0-1
     */
    public static function overlapCoefficient(string $str1, string $str2): float
    {
        $set1 = array_unique(str_split($str1));
        $set2 = array_unique(str_split($str2));
        
        $intersection = count(array_intersect($set1, $set2));
        $minSize = min(count($set1), count($set2));
        
        if ($minSize === 0) return 1.0;
        
        return $intersection / $minSize;
    }

    /**
     * 计算 N-gram 相似度
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @param int $n N-gram 大小，默认 2
     * @return float 相似度，范围 0-1
     */
    public static function ngramSimilarity(string $str1, string $str2, int $n = 2): float
    {
        $ngrams1 = self::getNgrams($str1, $n);
        $ngrams2 = self::getNgrams($str2, $n);
        
        $count1 = count($ngrams1);
        $count2 = count($ngrams2);
        
        if ($count1 === 0 && $count2 === 0) return 1.0;
        if ($count1 === 0 || $count2 === 0) return 0.0;
        
        $intersection = count(array_intersect($ngrams1, $ngrams2));
        $maxLen = max($count1, $count2);
        
        return $intersection / $maxLen;
    }

    /**
     * 计算综合相似度
     * 
     * 综合多种算法计算平均相似度
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return array 包含各种相似度指标的关联数组
     */
    public static function comprehensiveSimilarity(string $str1, string $str2): array
    {
        $result = [
            'levenshtein_similarity' => self::levenshteinSimilarity($str1, $str2),
            'jaccard_similarity' => self::jaccardSimilarity($str1, $str2),
            'cosine_similarity' => self::cosineSimilarity($str1, $str2),
            'dice_coefficient' => self::diceCoefficient($str1, $str2),
            'jaro_similarity' => self::jaroSimilarity($str1, $str2),
            'jaro_winkler_similarity' => self::jaroWinklerSimilarity($str1, $str2),
            'lcs_similarity' => self::lcsSimilarity($str1, $str2),
            'ngram_similarity' => self::ngramSimilarity($str1, $str2),
        ];
        
        $result['average'] = array_sum($result) / count($result);
        
        return $result;
    }

    /**
     * 查找最相似的字符串
     * 
     * 从候选列表中找出与目标字符串最相似的
     *
     * @param string $target 目标字符串
     * @param array $candidates 候选字符串数组
     * @param string $method 相似度计算方法，默认 'jaro_winkler'
     * @return array 包含 'string' 和 'similarity' 的关联数组
     */
    public static function findMostSimilar(string $target, array $candidates, string $method = 'jaro_winkler'): array
    {
        $methodMap = [
            'levenshtein' => 'levenshteinSimilarity',
            'jaccard' => 'jaccardSimilarity',
            'cosine' => 'cosineSimilarity',
            'dice' => 'diceCoefficient',
            'jaro' => 'jaroSimilarity',
            'jaro_winkler' => 'jaroWinklerSimilarity',
            'lcs' => 'lcsSimilarity',
            'ngram' => 'ngramSimilarity',
        ];
        
        if (!isset($methodMap[$method])) {
            throw new InvalidArgumentException("未知的相似度方法: $method");
        }
        
        $func = $methodMap[$method];
        $bestSimilarity = -1;
        $bestMatch = '';
        
        foreach ($candidates as $candidate) {
            $similarity = self::$func($target, $candidate);
            if ($similarity > $bestSimilarity) {
                $bestSimilarity = $similarity;
                $bestMatch = $candidate;
            }
        }
        
        return [
            'string' => $bestMatch,
            'similarity' => $bestSimilarity,
        ];
    }

    /**
     * 批量计算相似度
     * 
     * 计算目标字符串与所有候选字符串的相似度
     *
     * @param string $target 目标字符串
     * @param array $candidates 候选字符串数组
     * @param string $method 相似度计算方法，默认 'jaro_winkler'
     * @return array 按相似度降序排列的结果数组
     */
    public static function rankBySimilarity(string $target, array $candidates, string $method = 'jaro_winkler'): array
    {
        $methodMap = [
            'levenshtein' => 'levenshteinSimilarity',
            'jaccard' => 'jaccardSimilarity',
            'cosine' => 'cosineSimilarity',
            'dice' => 'diceCoefficient',
            'jaro' => 'jaroSimilarity',
            'jaro_winkler' => 'jaroWinklerSimilarity',
            'lcs' => 'lcsSimilarity',
            'ngram' => 'ngramSimilarity',
        ];
        
        if (!isset($methodMap[$method])) {
            throw new InvalidArgumentException("未知的相似度方法: $method");
        }
        
        $func = $methodMap[$method];
        $results = [];
        
        foreach ($candidates as $candidate) {
            $results[] = [
                'string' => $candidate,
                'similarity' => self::$func($target, $candidate),
            ];
        }
        
        // 按相似度降序排序
        usort($results, function ($a, $b) {
            return $b['similarity'] <=> $a['similarity'];
        });
        
        return $results;
    }

    /**
     * 模糊匹配
     * 
     * 返回相似度超过阈值的所有候选
     *
     * @param string $target 目标字符串
     * @param array $candidates 候选字符串数组
     * @param float $threshold 相似度阈值，默认 0.7
     * @param string $method 相似度计算方法，默认 'jaro_winkler'
     * @return array 匹配的候选及其相似度
     */
    public static function fuzzyMatch(string $target, array $candidates, float $threshold = 0.7, string $method = 'jaro_winkler'): array
    {
        $ranked = self::rankBySimilarity($target, $candidates, $method);
        
        return array_values(array_filter($ranked, function ($item) use ($threshold) {
            return $item['similarity'] >= $threshold;
        }));
    }

    /**
     * 计算编辑距离比例
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @return float 编辑距离比例，范围 0-1
     */
    public static function editDistanceRatio(string $str1, string $str2): float
    {
        return self::levenshteinSimilarity($str1, $str2);
    }

    /**
     * 判断两个字符串是否相似
     *
     * @param string $str1 第一个字符串
     * @param string $str2 第二个字符串
     * @param float $threshold 相似度阈值，默认 0.8
     * @param string $method 相似度计算方法，默认 'jaro_winkler'
     * @return bool 是否相似
     */
    public static function isSimilar(string $str1, string $str2, float $threshold = 0.8, string $method = 'jaro_winkler'): bool
    {
        $methodMap = [
            'levenshtein' => 'levenshteinSimilarity',
            'jaccard' => 'jaccardSimilarity',
            'cosine' => 'cosineSimilarity',
            'dice' => 'diceCoefficient',
            'jaro' => 'jaroSimilarity',
            'jaro_winkler' => 'jaroWinklerSimilarity',
            'lcs' => 'lcsSimilarity',
            'ngram' => 'ngramSimilarity',
        ];
        
        if (!isset($methodMap[$method])) {
            throw new InvalidArgumentException("未知的相似度方法: $method");
        }
        
        $func = $methodMap[$method];
        return self::$func($str1, $str2) >= $threshold;
    }
}