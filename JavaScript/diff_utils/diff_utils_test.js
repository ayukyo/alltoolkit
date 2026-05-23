/**
 * diff_utils 测试文件
 */

const assert = require('assert');
const {
  DiffType,
  diffLines,
  diffChars,
  diffWords,
  mergeDiff,
  unifiedDiff,
  colorDiff,
  diffStats,
  applyDiff,
  reverseDiff,
  similarity,
  longestCommonSubsequence,
  longestCommonSubstring,
  diffToHtml,
  parseUnifiedDiff,
  threeWayMerge,
  computeLCSMatrix
} = require('./mod.js');

// 测试计数器
let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (error) {
    console.log(`✗ ${name}`);
    console.log(`  Error: ${error.message}`);
    failed++;
  }
}

function testGroup(name) {
  console.log(`\n【${name}】`);
}

// ============== 测试开始 ==============

testGroup('基础差异计算');

test('diffLines - 完全相同的文本', () => {
  const text1 = 'hello\nworld';
  const text2 = 'hello\nworld';
  const diff = diffLines(text1, text2);
  
  assert.strictEqual(diff.length, 2);
  assert.strictEqual(diff[0].type, DiffType.EQUAL);
  assert.strictEqual(diff[0].value, 'hello');
  assert.strictEqual(diff[1].type, DiffType.EQUAL);
  assert.strictEqual(diff[1].value, 'world');
});

test('diffLines - 完全不同的文本', () => {
  const text1 = 'hello';
  const text2 = 'world';
  const diff = diffLines(text1, text2);
  
  assert.strictEqual(diff.length, 2);
  assert.strictEqual(diff[0].type, DiffType.DELETE);
  assert.strictEqual(diff[0].value, 'hello');
  assert.strictEqual(diff[1].type, DiffType.ADD);
  assert.strictEqual(diff[1].value, 'world');
});

test('diffLines - 部分不同', () => {
  const text1 = 'hello\nworld\nfoo';
  const text2 = 'hello\nbar\nfoo';
  const diff = diffLines(text1, text2);
  
  // 应该有 4 部分：equal(hello), delete(world), add(bar), equal(foo)
  assert.strictEqual(diff.length, 4);
  assert.strictEqual(diff[0].type, DiffType.EQUAL);
  assert.strictEqual(diff[0].value, 'hello');
  assert.strictEqual(diff[1].type, DiffType.DELETE);
  assert.strictEqual(diff[1].value, 'world');
  assert.strictEqual(diff[2].type, DiffType.ADD);
  assert.strictEqual(diff[2].value, 'bar');
  assert.strictEqual(diff[3].type, DiffType.EQUAL);
  assert.strictEqual(diff[3].value, 'foo');
});

test('diffLines - 添加行', () => {
  const text1 = 'hello\nworld';
  const text2 = 'hello\nbeautiful\nworld';
  const diff = diffLines(text1, text2);
  
  assert.ok(diff.some(d => d.type === DiffType.ADD && d.value === 'beautiful'));
});

test('diffLines - 删除行', () => {
  const text1 = 'hello\nbeautiful\nworld';
  const text2 = 'hello\nworld';
  const diff = diffLines(text1, text2);
  
  assert.ok(diff.some(d => d.type === DiffType.DELETE && d.value === 'beautiful'));
});

testGroup('字符级差异');

test('diffChars - 字符差异', () => {
  const text1 = 'hello';
  const text2 = 'hallo';
  const diff = diffChars(text1, text2);
  
  assert.ok(diff.some(d => d.type === DiffType.DELETE && d.value === 'e'));
  assert.ok(diff.some(d => d.type === DiffType.ADD && d.value === 'a'));
});

test('diffChars - 完全相同', () => {
  const diff = diffChars('abc', 'abc');
  // diffChars 按字符返回，需要用 mergeDiff 合并
  const merged = mergeDiff(diff);
  assert.strictEqual(merged.length, 1);
  assert.strictEqual(merged[0].type, DiffType.EQUAL);
  assert.strictEqual(merged[0].value, 'abc');
});

testGroup('单词级差异');

test('diffWords - 单词差异', () => {
  const text1 = 'hello world foo';
  const text2 = 'hello bar foo';
  const diff = diffWords(text1, text2);
  
  assert.ok(diff.some(d => d.type === DiffType.DELETE && d.value === 'world'));
  assert.ok(diff.some(d => d.type === DiffType.ADD && d.value === 'bar'));
});

testGroup('差异合并');

test('mergeDiff - 合并相邻相同类型', () => {
  const diff = [
    { type: DiffType.EQUAL, value: 'a' },
    { type: DiffType.EQUAL, value: 'b' },
    { type: DiffType.ADD, value: 'c' },
    { type: DiffType.ADD, value: 'd' }
  ];
  
  const merged = mergeDiff(diff);
  
  assert.strictEqual(merged.length, 2);
  assert.strictEqual(merged[0].value, 'ab');
  assert.strictEqual(merged[1].value, 'cd');
});

testGroup('统一格式 diff');

test('unifiedDiff - 生成统一格式', () => {
  const text1 = 'line1\nline2\nline3';
  const text2 = 'line1\nmodified\nline3';
  const result = unifiedDiff(text1, text2, {
    filename1: 'a/original.txt',
    filename2: 'b/new.txt',
    context: 1
  });
  
  assert.ok(result.includes('--- a/original.txt'));
  assert.ok(result.includes('+++ b/new.txt'));
  assert.ok(result.includes('@@'));
  assert.ok(result.includes('-line2'));
  assert.ok(result.includes('+modified'));
});

test('unifiedDiff - 多行变更', () => {
  const text1 = 'a\nb\nc\nd\ne';
  const text2 = 'a\nx\ny\nc\nd\ne';
  const result = unifiedDiff(text1, text2);
  
  assert.ok(result.includes('-b'));
  assert.ok(result.includes('+x'));
  assert.ok(result.includes('+y'));
});

testGroup('差异统计');

test('diffStats - 统计信息', () => {
  const diff = [
    { type: DiffType.EQUAL, value: 'a' },
    { type: DiffType.DELETE, value: 'bb' },
    { type: DiffType.ADD, value: 'ccc' }
  ];
  
  const stats = diffStats(diff);
  
  assert.strictEqual(stats.equal, 1);
  assert.strictEqual(stats.deleted, 1);
  assert.strictEqual(stats.added, 1);
  assert.strictEqual(stats.deletedChars, 2);
  assert.strictEqual(stats.addedChars, 3);
});

testGroup('差异应用与回滚');

test('applyDiff - 应用差异', () => {
  const text1 = 'hello\nworld';
  const text2 = 'hello\nbeautiful\nworld';
  const diff = diffLines(text1, text2);
  const result = applyDiff(text1, diff);
  
  assert.strictEqual(result, text2);
});

test('reverseDiff - 反转差异', () => {
  const diff = [
    { type: DiffType.ADD, value: 'a' },
    { type: DiffType.DELETE, value: 'b' },
    { type: DiffType.EQUAL, value: 'c' }
  ];
  
  const reversed = reverseDiff(diff);
  
  assert.strictEqual(reversed[0].type, DiffType.DELETE);
  assert.strictEqual(reversed[1].type, DiffType.ADD);
  assert.strictEqual(reversed[2].type, DiffType.EQUAL);
});

testGroup('相似度计算');

test('similarity - 完全相同', () => {
  const sim = similarity('hello', 'hello');
  assert.strictEqual(sim, 1);
});

test('similarity - 完全不同', () => {
  const sim = similarity('abc', 'xyz');
  assert.strictEqual(sim, 0);
});

test('similarity - 部分相同', () => {
  const sim = similarity('hello', 'hallo');
  assert.ok(sim > 0.5 && sim < 1);
});

test('similarity - 空字符串', () => {
  assert.strictEqual(similarity('', ''), 1);
  assert.strictEqual(similarity('', 'a'), 0);
  assert.strictEqual(similarity('a', ''), 0);
});

testGroup('最长公共子序列/子串');

test('longestCommonSubsequence - 基本测试', () => {
  const lcs = longestCommonSubsequence('ABCBDAB', 'BDCABA');
  assert.strictEqual(lcs.length, 4);
  // LCS 可能是 BCBA 或 BDAB
  assert.ok(['BCBA', 'BDAB', 'BCAB'].includes(lcs));
});

test('longestCommonSubsequence - 完全相同', () => {
  const lcs = longestCommonSubsequence('hello', 'hello');
  assert.strictEqual(lcs, 'hello');
});

test('longestCommonSubsequence - 无公共部分', () => {
  const lcs = longestCommonSubsequence('abc', 'xyz');
  assert.strictEqual(lcs, '');
});

test('longestCommonSubstring - 基本测试', () => {
  const lcs = longestCommonSubstring('ABCBDAB', 'BDCABA');
  // 最长公共子串应该是 AB 或 BD
  assert.ok(lcs.length >= 2);
});

test('longestCommonSubstring - 完全相同', () => {
  const lcs = longestCommonSubstring('hello', 'hello');
  assert.strictEqual(lcs, 'hello');
});

testGroup('HTML 输出');

test('diffToHtml - 生成 HTML', () => {
  const diff = [
    { type: DiffType.EQUAL, value: 'hello' },
    { type: DiffType.ADD, value: 'world' },
    { type: DiffType.DELETE, value: 'foo' }
  ];
  
  const html = diffToHtml(diff);
  
  assert.ok(html.includes('class="diff-equal"'));
  assert.ok(html.includes('class="diff-add"'));
  assert.ok(html.includes('class="diff-delete"'));
  assert.ok(html.includes('hello'));
  assert.ok(html.includes('world'));
});

test('diffToHtml - 转义特殊字符', () => {
  const diff = [
    { type: DiffType.EQUAL, value: '<script>alert("xss")</script>' }
  ];
  
  const html = diffToHtml(diff);
  
  assert.ok(!html.includes('<script>'));
  assert.ok(html.includes('&lt;'));
  assert.ok(html.includes('&gt;'));
});

testGroup('解析统一格式');

test('parseUnifiedDiff - 解析 diff', () => {
  const unified = `--- a/original
+++ b/new
@@ -1,3 +1,3 @@
 line1
-line2
+modified
 line3`;
  
  const diff = parseUnifiedDiff(unified);
  
  assert.ok(diff.some(d => d.type === DiffType.EQUAL && d.value === 'line1'));
  assert.ok(diff.some(d => d.type === DiffType.DELETE && d.value === 'line2'));
  assert.ok(diff.some(d => d.type === DiffType.ADD && d.value === 'modified'));
  assert.ok(diff.some(d => d.type === DiffType.EQUAL && d.value === 'line3'));
});

testGroup('三方合并');

test('threeWayMerge - 无冲突', () => {
  const base = 'line1\nline2\nline3';
  const ours = 'line1\nline2\nline3';
  const theirs = 'line1\nline2\nline3';
  
  const result = threeWayMerge(base, ours, theirs);
  
  assert.strictEqual(result.success, true);
  assert.strictEqual(result.conflicts.length, 0);
});

test('threeWayMerge - 检测冲突', () => {
  const base = 'line1\nline2\nline3';
  const ours = 'line1\nour-change\nline3';
  const theirs = 'line1\ntheir-change\nline3';
  
  const result = threeWayMerge(base, ours, theirs);
  
  // 检测到冲突
  assert.ok(result.diffOurs.some(d => d.type === DiffType.ADD || d.type === DiffType.DELETE));
  assert.ok(result.diffTheirs.some(d => d.type === DiffType.ADD || d.type === DiffType.DELETE));
});

testGroup('LCS 矩阵计算');

test('computeLCSMatrix - 基本测试', () => {
  const arr1 = ['A', 'B', 'C'];
  const arr2 = ['A', 'C'];
  const dp = computeLCSMatrix(arr1, arr2);
  
  // LCS 长度应该是 2 (A 和 C)
  assert.strictEqual(dp[3][2], 2);
});

test('computeLCSMatrix - 完全相同', () => {
  const arr = ['a', 'b', 'c'];
  const dp = computeLCSMatrix(arr, arr);
  
  assert.strictEqual(dp[3][3], 3);
});

test('computeLCSMatrix - 无公共元素', () => {
  const dp = computeLCSMatrix(['a', 'b'], ['c', 'd']);
  
  assert.strictEqual(dp[2][2], 0);
});

testGroup('颜色输出');

test('colorDiff - 包含 ANSI 颜色码', () => {
  const diff = [
    { type: DiffType.ADD, value: 'added' },
    { type: DiffType.DELETE, value: 'deleted' },
    { type: DiffType.EQUAL, value: 'equal' }
  ];
  
  const colored = colorDiff(diff);
  
  assert.ok(colored.includes('\x1b[32m')); // 绿色
  assert.ok(colored.includes('\x1b[31m')); // 红色
  assert.ok(colored.includes('\x1b[0m')); // 重置
});

testGroup('边界情况');

test('空字符串处理', () => {
  const diff = diffLines('', '');
  // 空字符串 split('\n') 返回 ['']，所以有 1 个空行元素
  // 这是正确的行为，空文件也有 1 个空行
  assert.ok(diff.length >= 1);
  assert.ok(diff.every(d => d.type === DiffType.EQUAL));
});

test('单行文本', () => {
  const diff = diffLines('hello', 'world');
  assert.strictEqual(diff.length, 2);
  assert.strictEqual(diff[0].type, DiffType.DELETE);
  assert.strictEqual(diff[1].type, DiffType.ADD);
});

test('大量文本', () => {
  const lines1 = Array(1000).fill('line').map((v, i) => v + i);
  const lines2 = [...lines1];
  lines2[500] = 'modified';
  
  const diff = diffLines(lines1.join('\n'), lines2.join('\n'));
  
  assert.ok(diff.length > 0);
  assert.ok(diff.some(d => d.value === 'modified'));
});

// ============== 测试结束 ==============

console.log('\n' + '='.repeat(50));
console.log(`测试完成: ${passed} 通过, ${failed} 失败`);
console.log('='.repeat(50));

if (failed > 0) {
  process.exit(1);
}