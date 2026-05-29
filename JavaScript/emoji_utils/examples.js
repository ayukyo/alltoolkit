/**
 * Emoji Utilities - Usage Examples
 * Run with: node examples.js
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
  getSupportedSkinTones,
} = require('./emoji_utils.js');

console.log('='.repeat(60));
console.log('Emoji Utilities - Usage Examples');
console.log('='.repeat(60));

// Example 1: Basic Emoji Detection
console.log('\n📌 Example 1: Basic Emoji Detection');
console.log('-'.repeat(40));

console.log(`isEmoji('😀'): ${isEmoji('😀')}`);
console.log(`isEmoji('a'): ${isEmoji('a')}`);
console.log(`isEmoji('❤️'): ${isEmoji('❤️')}`);
console.log(`isEmoji('👍'): ${isEmoji('👍')}`);

// Example 2: Extract Emojis from Text
console.log('\n📌 Example 2: Extract Emojis from Text');
console.log('-'.repeat(40));

const text1 = 'Hello 😀 World 🌍! This is awesome 🎉';
const emojis1 = extractEmojis(text1);
console.log(`Text: "${text1}"`);
console.log(`Emojis found: ${emojis1.join(' ')}`);

// Example 3: Count Emoji Frequency
console.log('\n📌 Example 3: Count Emoji Frequency');
console.log('-'.repeat(40));

const text2 = 'I love 🍕 and 🍕 and more 🍕! Also 🍔';
const counts = countEmojis(text2);
console.log(`Text: "${text2}"`);
console.log('Emoji counts:', counts);

// Example 4: Get Sorted Emoji Frequency
console.log('\n📌 Example 4: Get Sorted Emoji Frequency');
console.log('-'.repeat(40));

const text3 = '😀 🌍 😀 🎉 🎉 🎉 🐶 🐶';
const freq = getEmojiFrequency(text3);
console.log(`Text: "${text3}"`);
console.log('Sorted by frequency:');
freq.forEach(([emoji, count]) => {
  console.log(`  ${emoji}: ${count} time(s)`);
});

// Example 5: Remove Emojis from Text
console.log('\n📌 Example 5: Remove Emojis from Text');
console.log('-'.repeat(40));

const text4 = 'Hello 😀 World 🌍! How are you? 👍';
const cleaned = removeEmojis(text4);
console.log(`Original: "${text4}"`);
console.log(`Cleaned: "${cleaned}"`);

// Example 6: Replace Emojis with Descriptions
console.log('\n📌 Example 6: Replace Emojis with Descriptions');
console.log('-'.repeat(40));

const text5 = 'I am so 😀 today! 🌍 is beautiful!';
const described = replaceEmojisWithText(text5);
console.log(`Original: "${text5}"`);
console.log(`Described: "${described}"`);

// With wrapper
const wrapped = replaceEmojisWithText(text5, ':');
console.log(`Wrapped: "${wrapped}"`);

// Example 7: Get Emoji Descriptions
console.log('\n📌 Example 7: Get Emoji Descriptions');
console.log('-'.repeat(40));

const emojisToDescribe = ['😀', '❤️', '👍', '🎉', '🍕', '🚀'];
emojisToDescribe.forEach(emoji => {
  const desc = getEmojiDescription(emoji);
  console.log(`${emoji}: ${desc}`);
});

// Example 8: Emoji Categories
console.log('\n📌 Example 8: Emoji Categories');
console.log('-'.repeat(40));

const text6 = '😀 🐶 🍕 ⚽ 🚗 ❤️';
const categories = groupEmojisByCategory(text6);
console.log(`Text: "${text6}"`);
console.log('Grouped by category:');
Object.entries(categories).forEach(([category, emojis]) => {
  console.log(`  ${category}: ${emojis.join(' ')}`);
});

// Example 9: Individual Category Detection
console.log('\n📌 Example 9: Individual Category Detection');
console.log('-'.repeat(40));

const categoryTestEmojis = ['😀', '🐶', '🍕', '⚽', '🚗', '❤️'];
categoryTestEmojis.forEach(emoji => {
  const category = getEmojiCategory(emoji);
  console.log(`${emoji}: ${category}`);
});

// Example 10: Skin Tone Detection and Modification
console.log('\n📌 Example 10: Skin Tone Detection and Modification');
console.log('-'.repeat(40));

const skinToneEmojis = ['👍🏻', '👍🏼', '👍🏽', '👍🏾', '👍🏿', '👍'];
console.log('Detecting skin tones:');
skinToneEmojis.forEach(emoji => {
  const tone = detectSkinTone(emoji);
  console.log(`${emoji}: ${tone || 'no skin tone'}`);
});

// Adding skin tones
console.log('\nAdding skin tones:');
const baseEmoji = '👍';
const skinTones = getSupportedSkinTones();
Object.entries(skinTones).forEach(([name, char]) => {
  if (char) {
    const modified = addSkinTone(baseEmoji, name);
    console.log(`${name}: ${modified}`);
  }
});

// Removing skin tone
console.log('\nRemoving skin tone:');
const withTone = '👍🏽';
const withoutTone = removeSkinTone(withTone);
console.log(`${withTone} → ${withoutTone}`);

// Example 11: Check for Emoji Presence
console.log('\n📌 Example 11: Check for Emoji Presence');
console.log('-'.repeat(40));

const texts = [
  'Hello World!',
  'Hello 😀 World!',
  '12345',
  '🎉 Party time!',
];

texts.forEach(t => {
  console.log(`"${t}": has emoji = ${hasEmoji(t)}`);
});

// Example 12: Get Unique Emojis
console.log('\n📌 Example 12: Get Unique Emojis');
console.log('-'.repeat(40));

const text7 = '😀 🌍 😀 🎉 😀 🌍 🎉 🎉';
const unique = getUniqueEmojis(text7);
console.log(`Text: "${text7}"`);
console.log(`Unique emojis: ${unique.join(' ')}`);

// Example 13: Replace Specific Emoji
console.log('\n📌 Example 13: Replace Specific Emoji');
console.log('-'.repeat(40));

const text8 = 'I love 🍕 but my friend prefers 🍔';
const replaced = replaceEmoji(text8, '🍕', '🍝');
console.log(`Original: "${text8}"`);
console.log(`Replaced: "${replaced}"`);

// Example 14: Comprehensive Emoji Statistics
console.log('\n📌 Example 14: Comprehensive Emoji Statistics');
console.log('-'.repeat(40));

const text9 = 'Hello 😀! I love 🍕 and 🍔. 😀 is happy, 🌍 is beautiful! 👍👍👍';
const stats = getEmojiStats(text9);

console.log(`Text: "${text9}"`);
console.log(`Total emojis: ${stats.total}`);
console.log(`Unique emojis: ${stats.unique}`);
console.log('\nFrequency:');
stats.sortedFrequency.forEach(([emoji, count]) => {
  console.log(`  ${emoji}: ${count}`);
});
console.log('\nCategories:');
Object.entries(stats.categories).forEach(([cat, emojis]) => {
  console.log(`  ${cat}: ${emojis.join(' ')}`);
});

// Example 15: Process User Messages
console.log('\n📌 Example 15: Process User Messages (Practical Use Case)');
console.log('-'.repeat(40));

const messages = [
  'Great job! 👏👏👏',
  'I love this! ❤️❤️❤️',
  'Haha 😂😂😂 that is so funny!',
  '🙏 Prayers for everyone',
  'This is 🔥🔥🔥',
];

console.log('Analyzing messages:');
messages.forEach((msg, i) => {
  const emojiCount = countTotalEmojis(msg);
  const topEmoji = getEmojiFrequency(msg)[0];
  console.log(`\nMessage ${i + 1}: "${msg}"`);
  console.log(`  Emoji count: ${emojiCount}`);
  if (topEmoji) {
    console.log(`  Most used: ${topEmoji[0]} (${topEmoji[1]} times)`);
  }
});

// Example 16: Text Cleaning for Processing
console.log('\n📌 Example 16: Text Cleaning for Processing');
console.log('-'.repeat(40));

const userComment = 'This product is amazing! 🌟🌟🌟 I would give it 5 stars ⭐⭐⭐⭐⭐. Highly recommend! 👍';
const cleanComment = removeEmojis(userComment);
const emojiCount = countTotalEmojis(userComment);

console.log(`Original comment: "${userComment}"`);
console.log(`Cleaned for analysis: "${cleanComment}"`);
console.log(`Total emojis used: ${emojiCount}`);

// Example 17: Emoji-Aware Text Length
console.log('\n📌 Example 17: Emoji-Aware Text Length');
console.log('-'.repeat(40));

const tweet = 'Just launched our new product! 🚀🎉 Check it out! #startup #launch';
const visualLength = removeEmojis(tweet).length;
const emojiCount2 = countTotalEmojis(tweet);

console.log(`Tweet: "${tweet}"`);
console.log(`Character length (no emojis): ${visualLength}`);
console.log(`Emoji count: ${emojiCount2}`);
console.log(`Total "units": ${visualLength + emojiCount2}`);

// Example 18: Generate Emoji Report
console.log('\n📌 Example 18: Generate Emoji Report');
console.log('-'.repeat(40));

const socialPost = `
🎉 Exciting News! 🎉
We're thrilled to announce our new product! 🚀
Thank you to everyone who supported us! ❤️❤️❤️
Special thanks to our team! 👏👏
Let's celebrate! 🎂🎈🎊
`;

const report = getEmojiStats(socialPost);
console.log('Emoji Analysis Report:');
console.log(`  Total emojis: ${report.total}`);
console.log(`  Unique emojis: ${report.unique}`);
console.log(`  Has skin tone variants: ${report.hasSkinTone}`);
console.log('\n  Top emojis:');
report.sortedFrequency.slice(0, 5).forEach(([emoji, count], i) => {
  console.log(`    ${i + 1}. ${emoji} (${count}x)`);
});

console.log('\n' + '='.repeat(60));
console.log('Examples completed!');
console.log('='.repeat(60));