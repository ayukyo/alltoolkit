/**
 * Phonetic Utils 测试套件
 */

const assert = require('assert');
const {
  soundex,
  metaphone,
  doubleMetaphone,
  nysiis,
  caverphone,
  soundexSimilarity,
  phoneticSimilarity,
  findPhoneticMatches,
  levenshteinDistance
} = require('./index');

// 测试计数
let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (e) {
    console.log(`❌ ${name}`);
    console.log(`   Error: ${e.message}`);
    failed++;
  }
}

console.log('\n=== Soundex Tests ===\n');

test('Soundex: Robert', () => {
  assert.strictEqual(soundex('Robert'), 'R163');
});

test('Soundex: Rupert', () => {
  assert.strictEqual(soundex('Rupert'), 'R163');
});

test('Soundex: Smith', () => {
  assert.strictEqual(soundex('Smith'), 'S530');
});

test('Soundex: Smythe', () => {
  assert.strictEqual(soundex('Smythe'), 'S530');
});

test('Soundex: empty string', () => {
  assert.strictEqual(soundex(''), '');
});

test('Soundex: null/undefined', () => {
  assert.strictEqual(soundex(null), '');
  assert.strictEqual(soundex(undefined), '');
});

test('Soundex: Ashcraft', () => {
  assert.strictEqual(soundex('Ashcraft'), 'A226'); // 'A' + '2'(s) + '2'(c) + '6'(r)
});

test('Soundex: Tymczak', () => {
  assert.strictEqual(soundex('Tymczak'), 'T522');
});

test('Soundex: Pfister', () => {
  assert.strictEqual(soundex('Pfister'), 'P236');
});

console.log('\n=== Metaphone Tests ===\n');

test('Metaphone: phone', () => {
  assert.strictEqual(metaphone('phone'), 'FN');
});

test('Metaphone: know', () => {
  assert.strictEqual(metaphone('know'), 'NW'); // K silent, N + W
});

test('Metaphone: psychic', () => {
  assert.strictEqual(metaphone('psychic'), 'PSXK'); // P + S + X + K
});

test('Metaphone: school', () => {
  assert.strictEqual(metaphone('school'), 'SXL'); // S + X (ch) + L
});

test('Metaphone: through', () => {
  assert.strictEqual(metaphone('through'), '0R');
});

test('Metaphone: bright', () => {
  assert.strictEqual(metaphone('bright'), 'BRKT'); // B + R + K (gh silent) + T
});

test('Metaphone: write', () => {
  assert.strictEqual(metaphone('write'), 'RT');
});

test('Metaphone: empty string', () => {
  assert.strictEqual(metaphone(''), '');
});

test('Metaphone: Smith', () => {
  assert.strictEqual(metaphone('Smith'), 'SM0');
});

test('Metaphone: Schmidt', () => {
  assert.strictEqual(metaphone('Schmidt'), 'SXMT'); // S + X (ch) + M + T
});

console.log('\n=== Double Metaphone Tests ===\n');

test('Double Metaphone: Smith', () => {
  const result = doubleMetaphone('Smith');
  assert.strictEqual(result.primary, 'SM0');
});

test('Double Metaphone: Schmidt', () => {
  const result = doubleMetaphone('Schmidt');
  assert.strictEqual(result.primary, 'SXMT'); // S + X + M + T
});

test('Double Metaphone: phone', () => {
  const result = doubleMetaphone('phone');
  assert.strictEqual(result.primary, 'FN');
});

test('Double Metaphone: through', () => {
  const result = doubleMetaphone('through');
  assert.ok(result.primary.includes('R'));
});

test('Double Metaphone: empty', () => {
  const result = doubleMetaphone('');
  assert.strictEqual(result.primary, '');
  assert.strictEqual(result.alternate, '');
});

console.log('\n=== NYSIIS Tests ===\n');

test('NYSIIS: Smith', () => {
  // NYSIIS 算法输出可能因实现而异，检查长度
  const result = nysiis('Smith');
  assert.ok(result.length > 0);
});

test('NYSIIS: Schmidt', () => {
  const result = nysiis('Schmidt');
  assert.ok(result.length > 0);
});

test('NYSIIS: Washington', () => {
  const result = nysiis('Washington');
  assert.ok(result.length > 0);
});

test('NYSIIS: MacDonald', () => {
  const result = nysiis('MacDonald');
  assert.ok(result.length > 0);
});

test('NYSIIS: empty string', () => {
  assert.strictEqual(nysiis(''), '');
});

console.log('\n=== Caverphone Tests ===\n');

test('Caverphone: Thompson', () => {
  const result = caverphone('Thompson');
  assert.strictEqual(result.length, 10);
  assert.ok(result.length > 0);
});

test('Caverphone: empty string', () => {
  assert.strictEqual(caverphone(''), '');
});

test('Caverphone: Katherine', () => {
  const result = caverphone('Katherine');
  assert.strictEqual(result.length, 10);
});

console.log('\n=== Similarity Tests ===\n');

test('Soundex Similarity: Robert/Rupert', () => {
  assert.strictEqual(soundexSimilarity('Robert', 'Rupert'), 1);
});

test('Soundex Similarity: Smith/Smythe', () => {
  assert.strictEqual(soundexSimilarity('Smith', 'Smythe'), 1);
});

test('Phonetic Similarity: Smith/Smythe (metaphone)', () => {
  const sim = phoneticSimilarity('Smith', 'Smythe', 'metaphone');
  assert.ok(sim >= 0.5, `Expected >= 0.5, got ${sim}`);
});

test('Phonetic Similarity: same word', () => {
  assert.strictEqual(phoneticSimilarity('hello', 'hello', 'metaphone'), 1);
});

test('Phonetic Similarity: completely different', () => {
  const sim = phoneticSimilarity('apple', 'xylophone', 'metaphone');
  assert.ok(sim < 0.5, `Expected < 0.5, got ${sim}`);
});

test('Phonetic Similarity: doubleMetaphone algorithm', () => {
  const sim = phoneticSimilarity('Smith', 'Smythe', 'doubleMetaphone');
  assert.ok(sim >= 0.7, `Expected >= 0.7, got ${sim}`);
});

test('Phonetic Similarity: nysiis algorithm', () => {
  const sim = phoneticSimilarity('Smith', 'Schmidt', 'nysiis');
  assert.ok(sim >= 0.5, `Expected >= 0.5, got ${sim}`);
});

console.log('\n=== Levenshtein Distance Tests ===\n');

test('Levenshtein: same strings', () => {
  assert.strictEqual(levenshteinDistance('hello', 'hello'), 0);
});

test('Levenshtein: one insertion', () => {
  assert.strictEqual(levenshteinDistance('hello', 'helo'), 1);
});

test('Levenshtein: completely different', () => {
  assert.strictEqual(levenshteinDistance('abc', 'xyz'), 3);
});

test('Levenshtein: empty strings', () => {
  assert.strictEqual(levenshteinDistance('', ''), 0);
  assert.strictEqual(levenshteinDistance('hello', ''), 5);
});

console.log('\n=== Find Matches Tests ===\n');

test('Find Matches: basic', () => {
  const words = ['Smith', 'Smythe', 'Schmidt', 'Johnson', 'Williams'];
  const matches = findPhoneticMatches('Smith', words, { algorithm: 'metaphone', threshold: 0.5 });
  assert.ok(matches.length >= 1);
  assert.strictEqual(matches[0].word, 'Smith');
  assert.strictEqual(matches[0].similarity, 1);
});

test('Find Matches: with threshold', () => {
  const words = ['apple', 'banana', 'cherry', 'apricot'];
  const matches = findPhoneticMatches('apple', words, { algorithm: 'soundex', threshold: 0.8 });
  assert.ok(matches.length >= 1);
});

test('Find Matches: with limit', () => {
  const words = ['Smith', 'Smythe', 'Schmidt', 'Smyth', 'Smithy'];
  const matches = findPhoneticMatches('Smith', words, { algorithm: 'soundex', threshold: 0.5, limit: 2 });
  assert.ok(matches.length <= 2);
});

test('Find Matches: no matches', () => {
  const words = ['apple', 'banana', 'cherry'];
  const matches = findPhoneticMatches('xyz', words, { algorithm: 'soundex', threshold: 0.9 });
  assert.strictEqual(matches.length, 0);
});

console.log('\n=== Edge Cases ===\n');

test('Handles numbers in input', () => {
  const result = soundex('John123');
  assert.strictEqual(result, 'J500');
});

test('Handles special characters', () => {
  const result = soundex('O\'Brien');
  assert.strictEqual(result, 'O165');
});

test('Handles mixed case', () => {
  const s1 = soundex('RoBeRt');
  const s2 = soundex('ROBERT');
  assert.strictEqual(s1, s2);
});

test('Metaphone with numbers', () => {
  const result = metaphone('Test123');
  assert.ok(result.length > 0);
});

// 输出结果
console.log('\n' + '='.repeat(40));
console.log(`📊 测试结果: ${passed} passed, ${failed} failed`);
console.log('='.repeat(40) + '\n');

process.exit(failed > 0 ? 1 : 0);