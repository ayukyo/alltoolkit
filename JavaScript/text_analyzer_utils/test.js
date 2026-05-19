/**
 * Text Analyzer Utils - 测试文件
 */

const assert = require('assert');
const textAnalyzer = require('./mod.js');

// ============================================================
// 测试数据
// ============================================================

const sampleTextEnglish = `The quick brown fox jumps over the lazy dog. This is a sample text for testing the text analyzer utils. It contains multiple sentences, some punctuation marks, and various word lengths.

The second paragraph talks about technology and programming. JavaScript is a versatile language that can be used for both frontend and backend development. It's important to understand the fundamentals.`;

const sampleTextChinese = `自然语言处理是人工智能的重要分支。它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。

自然语言处理是一门融语言学、计算机科学、数学于一体的科学。因此，这一领域的研究将涉及自然语言，即人们日常使用的语言，所以它与语言学的研究有着密切的联系。`;

const sampleTextMixed = `Hello world! 你好世界。This is a mixed text example with both English and Chinese content.
自然语言处理 NLP 是一个令人兴奋的领域。The technology is evolving rapidly.`;

// ============================================================
// 测试函数
// ============================================================

function testCountCharacters() {
  console.log('测试 countCharacters...');
  
  // 基础测试
  assert.strictEqual(textAnalyzer.countCharacters('hello'), 5);
  assert.strictEqual(textAnalyzer.countCharacters('hello world'), 11);
  assert.strictEqual(textAnalyzer.countCharacters(''), 0);
  assert.strictEqual(textAnalyzer.countCharacters(null), 0);
  
  // 不包含空格
  assert.strictEqual(textAnalyzer.countCharacters('hello world', { includeSpaces: false }), 10);
  
  // 不包含标点（hello, world! 移除逗号和感叹号后剩下 hello world，11个字符）
  assert.strictEqual(textAnalyzer.countCharacters('hello, world!', { includePunctuation: false }), 11);
  
  // 中文
  assert.strictEqual(textAnalyzer.countCharacters('你好世界'), 4);
  
  console.log('✓ countCharacters 测试通过');
}

function testCountWords() {
  console.log('测试 countWords...');
  
  // 英文
  assert.strictEqual(textAnalyzer.countWords('hello world'), 2);
  assert.strictEqual(textAnalyzer.countWords('The quick brown fox'), 4);
  
  // 中文
  assert.strictEqual(textAnalyzer.countWords('你好世界'), 4);
  assert.strictEqual(textAnalyzer.countWords('自然语言处理'), 6);
  
  // 混合
  assert.strictEqual(textAnalyzer.countWords('Hello 世界'), 3);
  
  // 边界
  assert.strictEqual(textAnalyzer.countWords(''), 0);
  assert.strictEqual(textAnalyzer.countWords('   '), 0);
  assert.strictEqual(textAnalyzer.countWords(null), 0);
  
  console.log('✓ countWords 测试通过');
}

function testCountSentences() {
  console.log('测试 countSentences...');
  
  // 英文
  assert.strictEqual(textAnalyzer.countSentences('Hello world.'), 1);
  assert.strictEqual(textAnalyzer.countSentences('Hello. World.'), 2);
  assert.strictEqual(textAnalyzer.countSentences('Hello! How are you? I am fine.'), 3);
  
  // 中文
  assert.strictEqual(textAnalyzer.countSentences('你好世界。'), 1);
  assert.strictEqual(textAnalyzer.countSentences('你好。世界。'), 2);
  assert.strictEqual(textAnalyzer.countSentences('你好！怎么样？'), 2);
  
  // 边界
  assert.strictEqual(textAnalyzer.countSentences(''), 0);
  assert.strictEqual(textAnalyzer.countSentences(null), 0);
  
  console.log('✓ countSentences 测试通过');
}

function testCountParagraphs() {
  console.log('测试 countParagraphs...');
  
  assert.strictEqual(textAnalyzer.countParagraphs('Single paragraph'), 1);
  assert.strictEqual(textAnalyzer.countParagraphs('First\n\nSecond'), 2);
  assert.strictEqual(textAnalyzer.countParagraphs('First\n\nSecond\n\nThird'), 3);
  assert.strictEqual(textAnalyzer.countParagraphs(''), 0);
  
  console.log('✓ countParagraphs 测试通过');
}

function testGetTextStatistics() {
  console.log('测试 getTextStatistics...');
  
  const stats = textAnalyzer.getTextStatistics(sampleTextEnglish);
  
  assert.strictEqual(typeof stats.characters, 'number');
  assert.strictEqual(typeof stats.words, 'number');
  assert.strictEqual(typeof stats.sentences, 'number');
  assert.strictEqual(typeof stats.paragraphs, 'number');
  assert.ok(stats.characters > 0);
  assert.ok(stats.words > 0);
  assert.ok(stats.sentences > 0);
  assert.ok(stats.paragraphs >= 1);
  
  console.log('文本统计结果:', stats);
  console.log('✓ getTextStatistics 测试通过');
}

function testEstimateReadingTime() {
  console.log('测试 estimateReadingTime...');
  
  // 短文本
  const shortTime = textAnalyzer.estimateReadingTime('Hello world');
  assert.strictEqual(typeof shortTime.minutes, 'number');
  assert.strictEqual(typeof shortTime.seconds, 'number');
  assert.ok(shortTime.totalSeconds >= 0);
  
  // 长文本
  const longText = 'word '.repeat(400);
  const longTime = textAnalyzer.estimateReadingTime(longText);
  assert.ok(longTime.minutes >= 1 || longTime.seconds > 0);
  
  // 中文
  const chineseText = '这是一个测试文本。'.repeat(100);
  const chineseTime = textAnalyzer.estimateReadingTime(chineseText);
  assert.ok(chineseTime.totalSeconds > 0);
  
  // 混合
  const mixedTime = textAnalyzer.estimateReadingTime(sampleTextMixed);
  assert.ok(mixedTime.totalSeconds > 0);
  
  console.log('英文阅读时间:', textAnalyzer.estimateReadingTime(sampleTextEnglish).formatted);
  console.log('中文阅读时间:', textAnalyzer.estimateReadingTime(sampleTextChinese).formatted);
  console.log('✓ estimateReadingTime 测试通过');
}

function testAnalyzeWordFrequency() {
  console.log('测试 analyzeWordFrequency...');
  
  const result = textAnalyzer.analyzeWordFrequency(sampleTextEnglish, { topN: 5 });
  
  assert.ok(Array.isArray(result.words));
  assert.strictEqual(typeof result.total, 'number');
  assert.strictEqual(typeof result.unique, 'number');
  assert.ok(result.words.length <= 5);
  
  // 验证词频格式
  if (result.words.length > 0) {
    const first = result.words[0];
    assert.ok(first.word);
    assert.ok(first.count > 0);
    assert.ok(first.percentage);
  }
  
  // 测试不移除停用词
  const withStopWords = textAnalyzer.analyzeWordFrequency('the the the test', { removeStopWords: false });
  assert.ok(withStopWords.total > 0);
  
  // 中文
  const chineseResult = textAnalyzer.analyzeWordFrequency(sampleTextChinese, { topN: 5 });
  assert.ok(chineseResult.words.length > 0);
  
  console.log('词频分析结果:', result);
  console.log('✓ analyzeWordFrequency 测试通过');
}

function testCalculateFleschKincaid() {
  console.log('测试 calculateFleschKincaid...');
  
  const result = textAnalyzer.calculateFleschKincaid(sampleTextEnglish);
  
  assert.ok(result.score >= 0 && result.score <= 100);
  assert.ok(result.gradeLevel);
  assert.ok(result.grade);
  assert.ok(result.description);
  assert.ok(result.details);
  
  console.log('Flesch-Kincaid 结果:', result);
  console.log('✓ calculateFleschKincaid 测试通过');
}

function testCalculateChineseReadability() {
  console.log('测试 calculateChineseReadability...');
  
  const result = textAnalyzer.calculateChineseReadability(sampleTextChinese);
  
  assert.ok(result.score >= 0 && result.score <= 100);
  assert.ok(result.level);
  assert.ok(result.description);
  assert.ok(result.details);
  
  console.log('中文可读性结果:', result);
  console.log('✓ calculateChineseReadability 测试通过');
}

function testCountSyllables() {
  console.log('测试 countSyllables...');
  
  // 音节计算是近似算法，主要用于可读性计算
  // 验证基本功能和边界情况
  assert.strictEqual(textAnalyzer.countSyllables('hello'), 2);
  assert.strictEqual(textAnalyzer.countSyllables('world'), 1);
  assert.strictEqual(textAnalyzer.countSyllables('the'), 1);
  assert.strictEqual(textAnalyzer.countSyllables('a'), 1);
  assert.strictEqual(textAnalyzer.countSyllables('apple'), 2);
  assert.strictEqual(textAnalyzer.countSyllables('banana'), 3);
  assert.strictEqual(textAnalyzer.countSyllables('jumped'), 1);
  assert.strictEqual(textAnalyzer.countSyllables(''), 0);
  
  console.log('✓ countSyllables 测试通过');
}

function testExtractKeywords() {
  console.log('测试 extractKeywords...');
  
  const result = textAnalyzer.extractKeywords(sampleTextEnglish, { topN: 5 });
  
  assert.ok(Array.isArray(result.keywords));
  assert.ok(result.keywords.length <= 5);
  assert.strictEqual(typeof result.totalCandidates, 'number');
  
  if (result.keywords.length > 0) {
    const first = result.keywords[0];
    assert.ok(first.word);
    assert.ok(first.count > 0);
    assert.ok(first.score);
  }
  
  // 中文关键词
  const chineseResult = textAnalyzer.extractKeywords(sampleTextChinese, { topN: 5 });
  assert.ok(chineseResult.keywords.length > 0);
  
  console.log('关键词提取结果:', result);
  console.log('✓ extractKeywords 测试通过');
}

function testAnalyzeSentenceComplexity() {
  console.log('测试 analyzeSentenceComplexity...');
  
  const result = textAnalyzer.analyzeSentenceComplexity(sampleTextEnglish);
  
  assert.ok(result.overallScore >= 0);
  assert.ok(result.level);
  assert.ok(Array.isArray(result.sentences));
  assert.strictEqual(typeof result.totalSentences, 'number');
  assert.ok(result.summary);
  assert.ok(typeof result.summary.simple === 'number');
  assert.ok(typeof result.summary.moderate === 'number');
  assert.ok(typeof result.summary.complex === 'number');
  
  console.log('句子复杂度结果:', {
    overallScore: result.overallScore,
    level: result.level,
    summary: result.summary,
  });
  console.log('✓ analyzeSentenceComplexity 测试通过');
}

function testGetFullAnalysis() {
  console.log('测试 getFullAnalysis...');
  
  const result = textAnalyzer.getFullAnalysis(sampleTextMixed);
  
  assert.ok(result.statistics);
  assert.ok(result.readingTime);
  assert.ok(result.wordFrequency);
  assert.ok(result.readability);
  assert.ok(result.keywords);
  assert.ok(result.sentenceComplexity);
  
  console.log('完整分析报告:');
  console.log('- 字符数:', result.statistics.characters);
  console.log('- 词数:', result.statistics.words);
  console.log('- 句子数:', result.statistics.sentences);
  console.log('- 段落数:', result.statistics.paragraphs);
  console.log('- 阅读时间:', result.readingTime.formatted);
  console.log('- 英文可读性:', result.readability.english.description);
  console.log('- 中文可读性:', result.readability.chinese.description);
  console.log('- 前5关键词:', result.keywords.keywords.slice(0, 5).map(k => k.word));
  console.log('- 句子复杂度:', result.sentenceComplexity.level);
  
  console.log('✓ getFullAnalysis 测试通过');
}

// ============================================================
// 运行所有测试
// ============================================================

function runAllTests() {
  console.log('========================================');
  console.log('Text Analyzer Utils 测试');
  console.log('========================================\n');
  
  try {
    testCountCharacters();
    testCountWords();
    testCountSentences();
    testCountParagraphs();
    testGetTextStatistics();
    testEstimateReadingTime();
    testAnalyzeWordFrequency();
    testCalculateFleschKincaid();
    testCalculateChineseReadability();
    testCountSyllables();
    testExtractKeywords();
    testAnalyzeSentenceComplexity();
    testGetFullAnalysis();
    
    console.log('\n========================================');
    console.log('✅ 所有测试通过！');
    console.log('========================================');
  } catch (error) {
    console.error('\n❌ 测试失败:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

runAllTests();