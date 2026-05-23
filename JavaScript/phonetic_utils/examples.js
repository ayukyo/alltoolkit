/**
 * Phonetic Utils 使用示例
 * 
 * 运行方式: node examples.js
 */

const {
  soundex,
  metaphone,
  doubleMetaphone,
  nysiis,
  caverphone,
  phoneticSimilarity,
  findPhoneticMatches
} = require('./index');

console.log('='.repeat(50));
console.log('🔊 Phonetic Utils - 语音匹配工具示例');
console.log('='.repeat(50));

// ========== Soundex 示例 ==========
console.log('\n📋 Soundex 编码示例');
console.log('-'.repeat(40));

const soundexExamples = [
  ['Robert', 'Rupert'],
  ['Smith', 'Smythe'],
  ['Ashcraft', 'Ashcroft'],
  ['Schmidt', 'Schmitt'],
  ['Johnson', 'Johnsen']
];

for (const [name1, name2] of soundexExamples) {
  const code1 = soundex(name1);
  const code2 = soundex(name2);
  const match = code1 === code2 ? '✅ 匹配' : '❌ 不匹配';
  console.log(`  ${name1.padEnd(12)} -> ${code1} | ${name2.padEnd(12)} -> ${code2} | ${match}`);
}

// ========== Metaphone 示例 ==========
console.log('\n📋 Metaphone 编码示例');
console.log('-'.repeat(40));

const metaphoneExamples = [
  'phone', 'know', 'psychic', 'school', 'bright',
  'write', 'through', 'knight', 'gnome', 'wright'
];

for (const word of metaphoneExamples) {
  const code = metaphone(word);
  console.log(`  ${word.padEnd(12)} -> ${code}`);
}

// ========== Double Metaphone 示例 ==========
console.log('\n📋 Double Metaphone 编码示例');
console.log('-'.repeat(40));

const dmExamples = ['Smith', 'Schmidt', 'phone', 'through', 'Catherine', 'Katherine'];

for (const word of dmExamples) {
  const { primary, alternate } = doubleMetaphone(word);
  console.log(`  ${word.padEnd(12)} -> 主编码: ${primary.padEnd(6)} 备用: ${alternate}`);
}

// ========== NYSIIS 示例 ==========
console.log('\n📋 NYSIIS 编码示例');
console.log('-'.repeat(40));

const nysiisExamples = [
  'Smith', 'Schmidt', 'Washington', 'MacDonald',
  'O\'Brien', 'Johnson', 'Williams', 'Brown'
];

for (const word of nysiisExamples) {
  const code = nysiis(word);
  console.log(`  ${word.padEnd(12)} -> ${code}`);
}

// ========== Caverphone 示例 ==========
console.log('\n📋 Caverphone 编码示例');
console.log('-'.repeat(40));

const caverphoneExamples = ['Thompson', 'Katherine', 'Stevenson', 'O\'Connor'];

for (const word of caverphoneExamples) {
  const code = caverphone(word);
  console.log(`  ${word.padEnd(12)} -> ${code}`);
}

// ========== 相似度计算示例 ==========
console.log('\n📊 语音相似度计算示例');
console.log('-'.repeat(40));

const similarityPairs = [
  ['Smith', 'Smythe'],
  ['Robert', 'Rupert'],
  ['Catherine', 'Katherine'],
  ['Johnson', 'Johnsen'],
  ['apple', 'orange']
];

const algorithms = ['soundex', 'metaphone', 'doubleMetaphone', 'nysiis', 'caverphone'];

for (const [word1, word2] of similarityPairs) {
  console.log(`\n  "${word1}" vs "${word2}":`);
  for (const algo of algorithms) {
    const sim = phoneticSimilarity(word1, word2, algo);
    const bar = '█'.repeat(Math.round(sim * 10));
    console.log(`    ${algo.padEnd(16)} ${bar.padEnd(10)} ${(sim * 100).toFixed(1)}%`);
  }
}

// ========== 实用场景示例 ==========
console.log('\n\n🎯 实用场景示例');
console.log('='.repeat(50));

// 场景1: 姓名去重
console.log('\n📌 场景1: 姓名去重');
console.log('-'.repeat(40));

const names = [
  'Smith', 'Smythe', 'Schmidt', 'Johnson', 'Johnsen',
  'Williams', 'Williamson', 'Brown', 'Browne', 'Jones'
];

console.log('  输入姓名列表:', names.join(', '));
console.log('\n  按语音编码分组:');

const groups = {};
for (const name of names) {
  const code = soundex(name);
  if (!groups[code]) groups[code] = [];
  groups[code].push(name);
}

for (const [code, members] of Object.entries(groups)) {
  console.log(`    ${code}: ${members.join(', ')}`);
}

// 场景2: 模糊搜索
console.log('\n📌 场景2: 模糊搜索');
console.log('-'.repeat(40));

const database = [
  'Robert Johnson', 'Rupert Johnsen', 'William Smith',
  'Willem Smythe', 'Catherine Brown', 'Katherine Browne',
  'James Williams', 'Jim Williamson', 'Elizabeth Davis'
];

const searchQuery = 'Katherine Brown';
console.log(`  搜索: "${searchQuery}"`);
console.log(`  数据库: [${database.slice(0, 4).join(', ')}...]\n`);

const results = database.map(name => ({
  name,
  similarity: Math.max(
    phoneticSimilarity(searchQuery.split(' ')[0], name.split(' ')[0], 'metaphone'),
    phoneticSimilarity(searchQuery.split(' ')[0], name.split(' ')[1] || '', 'metaphone')
  )
})).sort((a, b) => b.similarity - a.similarity);

console.log('  搜索结果:');
for (const { name, similarity } of results.slice(0, 5)) {
  const bar = '█'.repeat(Math.round(similarity * 10));
  console.log(`    ${name.padEnd(20)} ${bar} ${(similarity * 100).toFixed(0)}%`);
}

// 场景3: 拼写检查建议
console.log('\n📌 场景3: 拼写检查建议');
console.log('-'.repeat(40));

const dictionary = [
  'through', 'though', 'thought', 'thorough',
  'their', 'there', 'they\'re',
  'write', 'right', 'wright',
  'phone', 'known', 'gnome', 'knight', 'night'
];

const misspelled = 'nite'; // 常见拼写错误
console.log(`  输入: "${misspelled}"`);
console.log('  建议:');

const suggestions = findPhoneticMatches(misspelled, dictionary, {
  algorithm: 'metaphone',
  threshold: 0.5,
  limit: 5
});

for (const { word, similarity } of suggestions) {
  console.log(`    ${word.padEnd(12)} (${(similarity * 100).toFixed(0)}%)`);
}

// 场景4: 多算法对比
console.log('\n📌 场景4: 多算法对比分析');
console.log('-'.repeat(40));

const testPairs = [
  ['Smith', 'Schmidt'],
  ['phone', 'known'],
  ['write', 'right'],
  ['Catherine', 'Katherine']
];

for (const [w1, w2] of testPairs) {
  console.log(`\n  "${w1}" vs "${w2}":`);
  for (const algo of ['soundex', 'metaphone', 'doubleMetaphone', 'nysiis', 'caverphone']) {
    let enc1, enc2;
    switch (algo) {
      case 'soundex': enc1 = soundex(w1); enc2 = soundex(w2); break;
      case 'metaphone': enc1 = metaphone(w1); enc2 = metaphone(w2); break;
      case 'doubleMetaphone': 
        enc1 = doubleMetaphone(w1).primary; 
        enc2 = doubleMetaphone(w2).primary; 
        break;
      case 'nysiis': enc1 = nysiis(w1); enc2 = nysiis(w2); break;
      case 'caverphone': enc1 = caverphone(w1); enc2 = caverphone(w2); break;
    }
    const sim = phoneticSimilarity(w1, w2, algo);
    console.log(`    ${algo.padEnd(16)}: ${enc1} vs ${enc2} -> ${(sim * 100).toFixed(0)}%`);
  }
}

console.log('\n' + '='.repeat(50));
console.log('✅ 示例演示完成');
console.log('='.repeat(50) + '\n');