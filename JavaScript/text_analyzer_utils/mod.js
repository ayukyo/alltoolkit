/**
 * Text Analyzer Utils - 文本分析工具集
 * 零外部依赖，纯 JavaScript 实现
 * 
 * 功能：
 * - 文本统计（字数、词数、句数、段落数）
 * - 阅读时间估算
 * - 词汇频率分析
 * - 可读性指标（Flesch-Kincaid 等）
 * - 关键词提取
 * - 句子复杂度分析
 */

// ============================================================
// 基础统计功能
// ============================================================

/**
 * 统计文本中的字符数
 * @param {string} text - 输入文本
 * @param {Object} options - 选项
 * @param {boolean} options.includeSpaces - 是否包含空格（默认 true）
 * @param {boolean} options.includePunctuation - 是否包含标点（默认 true）
 * @returns {number} 字符数
 */
function countCharacters(text, options = {}) {
  const { includeSpaces = true, includePunctuation = true } = options;
  
  if (!text || typeof text !== 'string') return 0;
  
  let result = text;
  
  if (!includeSpaces) {
    result = result.replace(/\s/g, '');
  }
  
  if (!includePunctuation) {
    result = result.replace(/[.,!?;:'"()（）。，！？；：""''、]/g, '');
  }
  
  return result.length;
}

/**
 * 统计文本中的单词数（支持中英文混合）
 * @param {string} text - 输入文本
 * @returns {number} 单词数
 */
function countWords(text) {
  if (!text || typeof text !== 'string') return 0;
  
  // 移除多余空格
  const trimmed = text.trim();
  if (!trimmed) return 0;
  
  // 英文单词匹配
  const englishWords = trimmed.match(/[a-zA-Z]+/g) || [];
  
  // 中文汉字匹配（每个汉字算一个词）
  const chineseChars = trimmed.match(/[\u4e00-\u9fff]/g) || [];
  
  // 其他语言文字（日文假名、韩文等）
  const otherChars = trimmed.match(/[\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]/g) || [];
  
  return englishWords.length + chineseChars.length + otherChars.length;
}

/**
 * 统计文本中的句子数
 * @param {string} text - 输入文本
 * @returns {number} 句子数
 */
function countSentences(text) {
  if (!text || typeof text !== 'string') return 0;
  
  // 中英文句子分隔符
  const sentences = text.split(/[.!?。！？…]+/).filter(s => s.trim().length > 0);
  
  return sentences.length || 1;
}

/**
 * 统计文本中的段落数
 * @param {string} text - 输入文本
 * @returns {number} 段落数
 */
function countParagraphs(text) {
  if (!text || typeof text !== 'string') return 0;
  
  const paragraphs = text.split(/\n\s*\n|\r\n\s*\r\n/).filter(p => p.trim().length > 0);
  
  return paragraphs.length || 1;
}

/**
 * 获取文本完整统计信息
 * @param {string} text - 输入文本
 * @returns {Object} 统计信息对象
 */
function getTextStatistics(text) {
  const chars = countCharacters(text);
  const charsNoSpaces = countCharacters(text, { includeSpaces: false });
  const words = countWords(text);
  const sentences = countSentences(text);
  const paragraphs = countParagraphs(text);
  
  return {
    characters: chars,
    charactersNoSpaces: charsNoSpaces,
    words: words,
    sentences: sentences,
    paragraphs: paragraphs,
    avgWordsPerSentence: sentences > 0 ? (words / sentences).toFixed(2) : 0,
    avgCharsPerWord: words > 0 ? (charsNoSpaces / words).toFixed(2) : 0,
  };
}

// ============================================================
// 阅读时间估算
// ============================================================

/**
 * 估算阅读时间
 * @param {string} text - 输入文本
 * @param {Object} options - 选项
 * @param {number} options.wordsPerMinute - 阅读速度（词/分钟，默认 200）
 * @param {number} options.chineseCharsPerMinute - 中文阅读速度（字/分钟，默认 300）
 * @returns {Object} 阅读时间信息
 */
function estimateReadingTime(text, options = {}) {
  const { wordsPerMinute = 200, chineseCharsPerMinute = 300 } = options;
  
  if (!text || typeof text !== 'string') {
    return { minutes: 0, seconds: 0, formatted: '0秒' };
  }
  
  // 英文单词数
  const englishWords = (text.match(/[a-zA-Z]+/g) || []).length;
  
  // 中文字符数
  const chineseChars = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  
  // 分别计算时间（分钟）
  const englishTime = englishWords / wordsPerMinute;
  const chineseTime = chineseChars / chineseCharsPerMinute;
  
  const totalMinutes = englishTime + chineseTime;
  const totalSeconds = Math.ceil(totalMinutes * 60);
  
  return {
    minutes: Math.floor(totalMinutes),
    seconds: totalSeconds % 60,
    totalSeconds: totalSeconds,
    formatted: formatTime(totalSeconds),
    details: {
      englishWords: englishWords,
      chineseChars: chineseChars,
      englishTime: englishTime,
      chineseTime: chineseTime,
    },
  };
}

/**
 * 格式化时间为可读字符串
 * @param {number} seconds - 秒数
 * @returns {string} 格式化的时间字符串
 */
function formatTime(seconds) {
  if (seconds < 60) {
    return `${seconds}秒`;
  }
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return secs > 0 ? `${minutes}分${secs}秒` : `${minutes}分钟`;
}

// ============================================================
// 词汇频率分析
// ============================================================

/**
 * 停用词列表（英文）
 */
const STOP_WORDS_EN = new Set([
  'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
  'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
  'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
  'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought',
  'used', 'it', 'its', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
  'she', 'we', 'they', 'what', 'which', 'who', 'whom', 'whose', 'where',
  'when', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
  'most', 'other', 'some', 'such', 'no', 'not', 'only', 'own', 'same',
  'so', 'than', 'too', 'very', 'just', 'also', 'now', 'here', 'there',
]);

/**
 * 停用词列表（中文）
 */
const STOP_WORDS_ZH = new Set([
  '的', '了', '和', '是', '在', '有', '我', '他', '这', '为', '之',
  '以', '及', '与', '或', '不', '也', '就', '都', '而', '及', '着',
  '或', '一个', '没有', '我们', '你们', '他们', '她们', '它们',
  '这个', '那个', '什么', '怎么', '如何', '为什么', '哪里', '那里',
  '这里', '如果', '因为', '所以', '但是', '然后', '可以', '可能',
]);

/**
 * 分析词汇频率
 * @param {string} text - 输入文本
 * @param {Object} options - 选项
 * @param {boolean} options.removeStopWords - 是否移除停用词（默认 true）
 * @param {number} options.topN - 返回前 N 个高频词（默认 20）
 * @param {boolean} options.caseSensitive - 是否区分大小写（默认 false）
 * @returns {Object} 频率分析结果
 */
function analyzeWordFrequency(text, options = {}) {
  const { removeStopWords = true, topN = 20, caseSensitive = false } = options;
  
  if (!text || typeof text !== 'string') {
    return { words: [], total: 0, unique: 0 };
  }
  
  // 提取英文单词
  let englishWords = text.match(/[a-zA-Z]+/g) || [];
  
  // 提取中文词汇（简单分词：每 2-4 字组合）
  const chineseText = text.match(/[\u4e00-\u9fff]+/g) || [];
  const chineseWords = [];
  chineseText.forEach(segment => {
    // 单字
    for (let i = 0; i < segment.length; i++) {
      chineseWords.push(segment[i]);
    }
    // 双字词
    for (let i = 0; i < segment.length - 1; i++) {
      chineseWords.push(segment.substring(i, i + 2));
    }
  });
  
  // 合并所有词
  let allWords = [...englishWords, ...chineseWords];
  
  // 大小写处理
  if (!caseSensitive) {
    allWords = allWords.map(w => w.toLowerCase());
  }
  
  // 移除停用词
  if (removeStopWords) {
    allWords = allWords.filter(w => 
      !STOP_WORDS_EN.has(w.toLowerCase()) && 
      !STOP_WORDS_ZH.has(w)
    );
  }
  
  // 统计频率
  const frequency = {};
  allWords.forEach(word => {
    frequency[word] = (frequency[word] || 0) + 1;
  });
  
  // 排序并取前 N 个
  const sorted = Object.entries(frequency)
    .sort((a, b) => b[1] - a[1])
    .slice(0, topN)
    .map(([word, count]) => ({ word, count, percentage: (count / allWords.length * 100).toFixed(2) }));
  
  return {
    words: sorted,
    total: allWords.length,
    unique: Object.keys(frequency).length,
    averageFrequency: allWords.length > 0 ? (allWords.length / Object.keys(frequency).length).toFixed(2) : 0,
  };
}

// ============================================================
// 可读性指标
// ============================================================

/**
 * 计算 Flesch-Kincaid 阅读难度等级（适用于英文）
 * @param {string} text - 输入文本
 * @returns {Object} 可读性指标
 */
function calculateFleschKincaid(text) {
  if (!text || typeof text !== 'string') {
    return { score: 0, grade: 'N/A', description: '无文本' };
  }
  
  const words = text.match(/[a-zA-Z]+/g) || [];
  const sentences = countSentences(text);
  const syllables = words.reduce((sum, word) => sum + countSyllables(word), 0);
  
  if (words.length === 0 || sentences === 0) {
    return { score: 0, grade: 'N/A', description: '无有效文本' };
  }
  
  // Flesch Reading Ease
  const readingEase = 206.835 - 1.015 * (words.length / sentences) - 84.6 * (syllables / words.length);
  
  // Flesch-Kincaid Grade Level
  const gradeLevel = 0.39 * (words.length / sentences) + 11.8 * (syllables / words.length) - 15.59;
  
  return {
    score: Math.max(0, Math.min(100, readingEase)).toFixed(2),
    gradeLevel: Math.max(0, gradeLevel).toFixed(2),
    grade: getGradeFromScore(readingEase),
    description: getDescriptionFromScore(readingEase),
    details: {
      words: words.length,
      sentences: sentences,
      syllables: syllables,
      avgWordsPerSentence: (words.length / sentences).toFixed(2),
      avgSyllablesPerWord: (syllables / words.length).toFixed(2),
    },
  };
}

/**
 * 计算单词音节数（英文）
 * @param {string} word - 单词
 * @returns {number} 音节数
 */
function countSyllables(word) {
  if (!word) return 0;
  
  word = word.toLowerCase();
  if (word.length <= 3) return 1;
  
  // 移除尾部不发音的 e
  word = word.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/, '');
  word = word.replace(/^y/, '');
  
  // 计算元音组
  const matches = word.match(/[aeiouy]{1,2}/g);
  return matches ? matches.length : 1;
}

/**
 * 根据分数获取等级
 * @param {number} score - Flesch 分数
 * @returns {string} 等级
 */
function getGradeFromScore(score) {
  if (score >= 90) return '小学';
  if (score >= 80) return '初中';
  if (score >= 70) return '高中';
  if (score >= 60) return '大学';
  if (score >= 50) return '本科';
  if (score >= 30) return '研究生';
  return '专业';
}

/**
 * 根据分数获取描述
 * @param {number} score - Flesch 分数
 * @returns {string} 描述
 */
function getDescriptionFromScore(score) {
  if (score >= 90) return '非常容易阅读';
  if (score >= 80) return '容易阅读';
  if (score >= 70) return '较易阅读';
  if (score >= 60) return '标准难度';
  if (score >= 50) return '较难阅读';
  if (score >= 30) return '困难阅读';
  return '非常困难';
}

/**
 * 计算中文文本可读性（简化版）
 * @param {string} text - 输入文本
 * @returns {Object} 可读性指标
 */
function calculateChineseReadability(text) {
  if (!text || typeof text !== 'string') {
    return { score: 0, level: 'N/A', description: '无文本' };
  }
  
  const chineseChars = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const sentences = countSentences(text);
  const paragraphs = countParagraphs(text);
  const punctuation = (text.match(/[，。、；：""''！？……（）]/g) || []).length;
  
  if (chineseChars === 0) {
    return { score: 0, level: 'N/A', description: '无中文文本' };
  }
  
  // 平均句长（越短越易读）
  const avgSentenceLength = sentences > 0 ? chineseChars / sentences : 0;
  
  // 标点密度（适当的标点提高可读性）
  const punctuationDensity = punctuation / chineseChars;
  
  // 段落数
  const avgParagraphLength = paragraphs > 0 ? chineseChars / paragraphs : 0;
  
  // 简单可读性评分（0-100，越高越易读）
  let score = 100;
  
  // 句长影响（每超过 20 字扣分）
  if (avgSentenceLength > 20) {
    score -= (avgSentenceLength - 20) * 2;
  }
  
  // 标点密度影响（理想范围 0.05-0.15）
  if (punctuationDensity < 0.05) {
    score -= 10;
  } else if (punctuationDensity > 0.20) {
    score -= 5;
  }
  
  // 段落长度影响（每超过 200 字扣分）
  if (avgParagraphLength > 200) {
    score -= (avgParagraphLength - 200) / 20;
  }
  
  score = Math.max(0, Math.min(100, score));
  
  return {
    score: score.toFixed(2),
    level: getChineseLevel(score),
    description: getChineseDescription(score),
    details: {
      chineseChars,
      sentences,
      paragraphs,
      punctuation,
      avgSentenceLength: avgSentenceLength.toFixed(2),
      punctuationDensity: (punctuationDensity * 100).toFixed(2) + '%',
      avgParagraphLength: avgParagraphLength.toFixed(2),
    },
  };
}

/**
 * 根据分数获取中文等级
 * @param {number} score - 分数
 * @returns {string} 等级
 */
function getChineseLevel(score) {
  if (score >= 80) return '通俗易懂';
  if (score >= 60) return '中等难度';
  if (score >= 40) return '较难理解';
  return '晦涩难懂';
}

/**
 * 根据分数获取中文描述
 * @param {number} score - 分数
 * @returns {string} 描述
 */
function getChineseDescription(score) {
  if (score >= 80) return '适合大众阅读，语言流畅';
  if (score >= 60) return '需要一定阅读能力';
  if (score >= 40) return '需要专业知识背景';
  return '专业性强，难以理解';
}

// ============================================================
// 关键词提取
// ============================================================

/**
 * 简单关键词提取（基于词频和位置）
 * @param {string} text - 输入文本
 * @param {Object} options - 选项
 * @param {number} options.topN - 返回前 N 个关键词（默认 10）
 * @param {number} options.minLength - 最小词长（默认 2）
 * @returns {Object} 关键词提取结果
 */
function extractKeywords(text, options = {}) {
  const { topN = 10, minLength = 2 } = options;
  
  if (!text || typeof text !== 'string') {
    return { keywords: [], totalCandidates: 0 };
  }
  
  // 获取词频
  const freqResult = analyzeWordFrequency(text, { 
    removeStopWords: true, 
    topN: 50,
    caseSensitive: false,
  });
  
  // 过滤短词
  const candidates = freqResult.words.filter(w => w.word.length >= minLength);
  
  // 位置权重（标题和首段权重更高）
  const paragraphs = text.split(/\n\s*\n/);
  const firstParagraph = paragraphs[0] || '';
  
  const keywords = candidates.slice(0, topN).map(item => {
    const positionWeight = firstParagraph.includes(item.word) ? 1.2 : 1.0;
    const lengthWeight = Math.min(item.word.length / 4, 1.5);
    const score = item.count * positionWeight * lengthWeight;
    
    return {
      word: item.word,
      count: item.count,
      score: score.toFixed(2),
      inFirstParagraph: firstParagraph.includes(item.word),
    };
  });
  
  // 按分数重新排序
  keywords.sort((a, b) => parseFloat(b.score) - parseFloat(a.score));
  
  return {
    keywords: keywords.slice(0, topN),
    totalCandidates: candidates.length,
  };
}

// ============================================================
// 句子复杂度分析
// ============================================================

/**
 * 分析句子复杂度
 * @param {string} text - 输入文本
 * @returns {Object} 复杂度分析结果
 */
function analyzeSentenceComplexity(text) {
  if (!text || typeof text !== 'string') {
    return { 
      overallScore: 0, 
      level: 'N/A',
      sentences: [],
    };
  }
  
  const sentences = text.split(/[.!?。！？…]+/).filter(s => s.trim().length > 0);
  
  const analysis = sentences.map(sentence => {
    const trimmed = sentence.trim();
    const words = countWords(trimmed);
    const chars = trimmed.length;
    const commas = (trimmed.match(/[,，、;；]/g) || []).length;
    const conjunctions = countConjunctions(trimmed);
    const clauses = commas + conjunctions + 1;
    
    // 复杂度评分（0-100，越高越复杂）
    let complexity = 0;
    
    // 句子长度影响
    if (words > 30) complexity += 30;
    else if (words > 20) complexity += 20;
    else if (words > 10) complexity += 10;
    
    // 从句数影响
    if (clauses > 4) complexity += 30;
    else if (clauses > 2) complexity += 20;
    else if (clauses > 1) complexity += 10;
    
    // 连词影响
    complexity += Math.min(conjunctions * 5, 20);
    
    return {
      sentence: trimmed.substring(0, 50) + (trimmed.length > 50 ? '...' : ''),
      length: chars,
      words: words,
      commas: commas,
      conjunctions: conjunctions,
      clauses: clauses,
      complexity: Math.min(complexity, 100),
      level: getComplexityLevel(complexity),
    };
  });
  
  const avgComplexity = analysis.length > 0
    ? analysis.reduce((sum, s) => sum + s.complexity, 0) / analysis.length
    : 0;
  
  return {
    overallScore: avgComplexity.toFixed(2),
    level: getComplexityLevel(avgComplexity),
    totalSentences: analysis.length,
    sentences: analysis,
    summary: {
      simple: analysis.filter(s => s.complexity < 30).length,
      moderate: analysis.filter(s => s.complexity >= 30 && s.complexity < 60).length,
      complex: analysis.filter(s => s.complexity >= 60).length,
    },
  };
}

/**
 * 计算连词数量
 * @param {string} sentence - 句子
 * @returns {number} 连词数
 */
function countConjunctions(sentence) {
  const englishConjunctions = [
    'and', 'but', 'or', 'nor', 'for', 'yet', 'so', 'although', 'because',
    'since', 'unless', 'while', 'where', 'when', 'if', 'that', 'which', 'who',
  ];
  
  const chineseConjunctions = [
    '虽然', '但是', '因为', '所以', '如果', '那么', '只要', '就', '而且',
    '并且', '或者', '可是', '然而', '因此', '不但', '而且', '既然', '即使',
  ];
  
  let count = 0;
  const lowerSentence = sentence.toLowerCase();
  
  englishConjunctions.forEach(conj => {
    const regex = new RegExp('\\b' + conj + '\\b', 'gi');
    const matches = lowerSentence.match(regex);
    if (matches) count += matches.length;
  });
  
  chineseConjunctions.forEach(conj => {
    const regex = new RegExp(conj, 'g');
    const matches = sentence.match(regex);
    if (matches) count += matches.length;
  });
  
  return count;
}

/**
 * 根据分数获取复杂度等级
 * @param {number} score - 复杂度分数
 * @returns {string} 等级
 */
function getComplexityLevel(score) {
  if (score >= 70) return '复杂';
  if (score >= 40) return '中等';
  return '简单';
}

// ============================================================
// 综合分析
// ============================================================

/**
 * 获取文本完整分析报告
 * @param {string} text - 输入文本
 * @returns {Object} 完整分析报告
 */
function getFullAnalysis(text) {
  if (!text || typeof text !== 'string') {
    return { error: '请提供有效文本' };
  }
  
  return {
    statistics: getTextStatistics(text),
    readingTime: estimateReadingTime(text),
    wordFrequency: analyzeWordFrequency(text, { topN: 10 }),
    readability: {
      english: calculateFleschKincaid(text),
      chinese: calculateChineseReadability(text),
    },
    keywords: extractKeywords(text, { topN: 10 }),
    sentenceComplexity: analyzeSentenceComplexity(text),
  };
}

// ============================================================
// 导出模块
// ============================================================

module.exports = {
  // 基础统计
  countCharacters,
  countWords,
  countSentences,
  countParagraphs,
  getTextStatistics,
  
  // 阅读时间
  estimateReadingTime,
  
  // 词汇频率
  analyzeWordFrequency,
  STOP_WORDS_EN,
  STOP_WORDS_ZH,
  
  // 可读性
  calculateFleschKincaid,
  calculateChineseReadability,
  countSyllables,
  
  // 关键词
  extractKeywords,
  
  // 句子复杂度
  analyzeSentenceComplexity,
  
  // 综合分析
  getFullAnalysis,
};