/**
 * Tests for Emoji Utilities
 * Run with: node emoji_utils.test.js
 */

const {
  isEmoji,
  extractEmojis,
  countEmojis,
  countTotalEmojis,
  hasEmoji,
  getUniqueEmojis,
  getEmojiFrequency,
  getEmojiStats,
  removeEmojis,
  replaceEmojisWithText,
  replaceEmoji,
  getEmojiDescription,
  getEmojiCategory,
  groupEmojisByCategory,
  detectSkinTone,
  addSkinTone,
  removeSkinTone,
  isSkinToneModifier,
  getSupportedSkinTones,
  SKIN_TONES,
} = require('./emoji_utils.js');

// Test result tracking
let passed = 0;
let failed = 0;

function assert(condition, testName) {
  if (condition) {
    console.log(`✅ ${testName}`);
    passed++;
  } else {
    console.log(`❌ ${testName}`);
    failed++;
  }
}

function assertEqual(actual, expected, testName) {
  const condition = JSON.stringify(actual) === JSON.stringify(expected);
  if (condition) {
    console.log(`✅ ${testName}`);
    passed++;
  } else {
    console.log(`❌ ${testName}`);
    console.log(`   Expected: ${JSON.stringify(expected)}`);
    console.log(`   Actual: ${JSON.stringify(actual)}`);
    failed++;
  }
}

console.log('=== Emoji Utilities Tests ===\n');

// Test isEmoji
console.log('--- isEmoji ---');
assert(isEmoji('😀'), 'Detects simple emoji');
assert(isEmoji('❤️'), 'Detects heart emoji');
assert(isEmoji('👍'), 'Detects thumbs up emoji');
assert(!isEmoji('a'), 'Rejects regular letter');
assert(!isEmoji('1'), 'Rejects number');
assert(!isEmoji(''), 'Rejects empty string');
assert(!isEmoji(' '), 'Rejects space');

// Test extractEmojis
console.log('\n--- extractEmojis ---');
assertEqual(extractEmojis('Hello 😀 World 🌍'), ['😀', '🌍'], 'Extracts emojis from text');
assertEqual(extractEmojis('No emojis here'), [], 'Returns empty array for no emojis');
assertEqual(extractEmojis('😀😀😀'), ['😀', '😀', '😀'], 'Extracts duplicate emojis');
assertEqual(extractEmojis('🎉🎊🎈'), ['🎉', '🎊', '🎈'], 'Extracts multiple different emojis');
assertEqual(extractEmojis(''), [], 'Handles empty string');
assertEqual(extractEmojis('🔥'), ['🔥'], 'Extracts single emoji');

// Test countEmojis
console.log('\n--- countEmojis ---');
assertEqual(countEmojis('😀 🌍 😀'), { '😀': 2, '🌍': 1 }, 'Counts emoji frequency');
assertEqual(countEmojis('No emojis'), {}, 'Returns empty object for no emojis');
assertEqual(countEmojis('🎉🎉🎉'), { '🎉': 3 }, 'Counts single repeated emoji');

// Test countTotalEmojis
console.log('\n--- countTotalEmojis ---');
assertEqual(countTotalEmojis('Hello 😀 World 🌍 🎉'), 3, 'Counts total emojis');
assertEqual(countTotalEmojis('No emojis here'), 0, 'Returns 0 for no emojis');
assertEqual(countTotalEmojis(''), 0, 'Handles empty string');

// Test hasEmoji
console.log('\n--- hasEmoji ---');
assert(hasEmoji('Hello 😀'), 'Detects emoji in text');
assert(!hasEmoji('No emojis here'), 'Returns false for no emojis');
assert(!hasEmoji(''), 'Returns false for empty string');

// Test getUniqueEmojis
console.log('\n--- getUniqueEmojis ---');
assertEqual(getUniqueEmojis('😀 🌍 😀 🎉'), ['😀', '🌍', '🎉'], 'Gets unique emojis');
assertEqual(getUniqueEmojis('No emojis'), [], 'Returns empty for no emojis');

// Test getEmojiFrequency
console.log('\n--- getEmojiFrequency ---');
const freq = getEmojiFrequency('😀 🌍 😀 🎉 🎉 🎉');
assertEqual(freq.length, 3, 'Returns correct number of unique emojis');
assertEqual(freq[0], ['🎉', 3], 'Most frequent emoji first');
assertEqual(freq[1], ['😀', 2], 'Second most frequent');
assertEqual(freq[2], ['🌍', 1], 'Least frequent last');

// Test removeEmojis
console.log('\n--- removeEmojis ---');
assertEqual(removeEmojis('Hello 😀 World 🌍'), 'Hello  World ', 'Removes emojis from text');
assertEqual(removeEmojis('No emojis'), 'No emojis', 'Keeps text without emojis');
assertEqual(removeEmojis('😀😀😀'), '', 'Removes all emojis');
assertEqual(removeEmojis(''), '', 'Handles empty string');

// Test getEmojiDescription
console.log('\n--- getEmojiDescription ---');
assertEqual(getEmojiDescription('😀'), 'grinning face', 'Gets description for grinning face');
assertEqual(getEmojiDescription('❤️'), 'red heart', 'Gets description for heart');
assertEqual(getEmojiDescription('👍'), 'thumbs up', 'Gets description for thumbs up');
assert(typeof getEmojiDescription('🆕') === 'string', 'Returns string for unknown emoji');

// Test replaceEmojisWithText
console.log('\n--- replaceEmojisWithText ---');
assertEqual(replaceEmojisWithText('Hello 😀!'), 'Hello grinning face!', 'Replaces emoji with description');
assertEqual(replaceEmojisWithText('I ❤️ coding'), 'I red heart coding', 'Replaces heart emoji');
assertEqual(replaceEmojisWithText('No emojis'), 'No emojis', 'Keeps text without emojis');
assertEqual(replaceEmojisWithText('👍', ':'), ':thumbs up:', 'Uses wrapper for descriptions');

// Test replaceEmoji
console.log('\n--- replaceEmoji ---');
assertEqual(replaceEmoji('Hello 😀!', '😀', 'World'), 'Hello World!', 'Replaces specific emoji');
assertEqual(replaceEmoji('🎉🎉🎉', '🎉', '🎊'), '🎊🎊🎊', 'Replaces all occurrences');
assertEqual(replaceEmoji('Hello World', '😀', '👍'), 'Hello World', 'No change if emoji not found');

// Test getEmojiCategory
console.log('\n--- getEmojiCategory ---');
assertEqual(getEmojiCategory('😀'), 'smileys', 'Categorizes grinning face as smileys');
assertEqual(getEmojiCategory('🐶'), 'animals', 'Categorizes dog as animals');
assertEqual(getEmojiCategory('🍕'), 'food', 'Categorizes pizza as food');
assert(typeof getEmojiCategory('🆕') === 'string', 'Returns string for any emoji');

// Test groupEmojisByCategory
console.log('\n--- groupEmojisByCategory ---');
const groups = groupEmojisByCategory('😀 🐶 🍕 ⚽');
assert(typeof groups === 'object', 'Returns an object');
assert(Array.isArray(groups.smileys), 'Has smileys category');
assert(Array.isArray(groups.animals), 'Has animals category');

// Test detectSkinTone
console.log('\n--- detectSkinTone ---');
assert(detectSkinTone('👍🏻') === 'light', 'Detects light skin tone');
assert(detectSkinTone('👍🏿') === 'dark', 'Detects dark skin tone');
assert(detectSkinTone('👍') === null, 'Returns null for no skin tone');

// Test addSkinTone
console.log('\n--- addSkinTone ---');
assert(addSkinTone('👍', 'light').includes(SKIN_TONES.light), 'Adds light skin tone');
assert(addSkinTone('👍', 'dark').includes(SKIN_TONES.dark), 'Adds dark skin tone');
assertEqual(addSkinTone('👍', 'none'), '👍', 'Returns original for none skin tone');

// Test removeSkinTone
console.log('\n--- removeSkinTone ---');
assertEqual(removeSkinTone('👍🏻'), '👍', 'Removes skin tone modifier');
assertEqual(removeSkinTone('👍'), '👍', 'Returns original if no skin tone');

// Test isSkinToneModifier
console.log('\n--- isSkinToneModifier ---');
assert(isSkinToneModifier(SKIN_TONES.light), 'Detects light skin tone modifier');
assert(isSkinToneModifier(SKIN_TONES.dark), 'Detects dark skin tone modifier');
assert(!isSkinToneModifier('a'), 'Rejects regular character');
assert(!isSkinToneModifier('😀'), 'Rejects emoji');

// Test getSupportedSkinTones
console.log('\n--- getSupportedSkinTones ---');
const skinTones = getSupportedSkinTones();
assertEqual(typeof skinTones, 'object', 'Returns an object');
assertEqual(Object.keys(skinTones).length, 6, 'Has 6 skin tone options');
assertEqual(skinTones.light, SKIN_TONES.light, 'Includes light skin tone');
assertEqual(skinTones.dark, SKIN_TONES.dark, 'Includes dark skin tone');

// Test getEmojiStats
console.log('\n--- getEmojiStats ---');
const stats = getEmojiStats('Hello 😀 World 🌍 😀 🎉');
assertEqual(stats.total, 4, 'Stats has correct total');
assertEqual(stats.unique, 3, 'Stats has correct unique count');
assert(typeof stats.frequency === 'object', 'Stats has frequency object');
assert(Array.isArray(stats.sortedFrequency), 'Stats has sorted frequency array');
assert(typeof stats.categories === 'object', 'Stats has categories object');

// Complex test cases
console.log('\n--- Complex Test Cases ---');

// Test with skin tone emojis
const skinToneText = '👍🏻 👍🏼 👍🏽 👍🏾 👍🏿';
const skinToneEmojis = extractEmojis(skinToneText);
assertEqual(skinToneEmojis.length, 5, 'Extracts 5 skin tone variants');

// Test with text containing no emojis
assertEqual(extractEmojis('This is plain text 123 !@#'), [], 'Handles plain text with numbers and symbols');

// Test with mixed content
const mixedText = 'Hello 😀 World 🌍! This is a test 🎉 with emojis 👍';
assertEqual(countTotalEmojis(mixedText), 4, 'Counts emojis in mixed content');
assertEqual(removeEmojis(mixedText), 'Hello  World ! This is a test  with emojis ', 'Removes emojis from mixed content');

// Test emoji replacement with wrapper
const replaced = replaceEmojisWithText('I love ❤️ coding', ':');
assert(replaced.includes(':red heart:'), 'Wraps description correctly');

// Test frequency sorting
const freqTest = getEmojiFrequency('a b c 😀 😀 🌍 🎉 🎉 🎉');
assertEqual(freqTest[0][0], '🎉', 'Most frequent emoji is first');
assertEqual(freqTest[0][1], 3, 'Most frequent has correct count');
assertEqual(freqTest[1][0], '😀', 'Second most frequent is correct');
assertEqual(freqTest[1][1], 2, 'Second most frequent has correct count');

// Summary
console.log('\n=== Test Summary ===');
console.log(`✅ Passed: ${passed}`);
console.log(`❌ Failed: ${failed}`);
console.log(`📊 Total: ${passed + failed}`);
console.log(`\n${failed === 0 ? '🎉 All tests passed!' : '⚠️ Some tests failed.'}`);

process.exit(failed === 0 ? 0 : 1);