# Emoji Utilities

A zero-dependency JavaScript library for comprehensive emoji processing and analysis.

## Features

- **Extract Emojis** - Find all emojis in text, including complex sequences (ZWJ, skin tones)
- **Count & Analyze** - Count total emojis, get frequency statistics, find unique emojis
- **Remove Emojis** - Clean text by removing all emoji characters
- **Replace Emojis** - Convert emojis to their text descriptions
- **Category Detection** - Group emojis by category (smileys, animals, food, etc.)
- **Skin Tone Support** - Detect, add, and remove skin tone modifiers
- **Comprehensive Stats** - Get detailed statistics about emoji usage in text

## Installation

No installation required! This library has zero external dependencies. Simply copy the `emoji_utils.js` file to your project.

```javascript
const {
  isEmoji,
  extractEmojis,
  removeEmojis,
  // ... other functions
} = require('./emoji_utils.js');
```

## Quick Start

```javascript
const { extractEmojis, removeEmojis, getEmojiDescription } = require('./emoji_utils.js');

// Extract emojis from text
const text = 'Hello 😀 World 🌍!';
const emojis = extractEmojis(text);
console.log(emojis); // ['😀', '🌍']

// Remove emojis from text
const clean = removeEmojis(text);
console.log(clean); // 'Hello  World !'

// Get emoji description
console.log(getEmojiDescription('😀')); // 'grinning face'
```

## API Reference

### Core Functions

#### `isEmoji(char)`
Check if a character is an emoji.

```javascript
isEmoji('😀'); // true
isEmoji('a');  // false
```

#### `extractEmojis(text)`
Extract all emojis from text (including ZWJ sequences and skin tones).

```javascript
extractEmojis('Hello 😀 World 🌍 🎉'); // ['😀', '🌍', '🎉']
```

#### `removeEmojis(text)`
Remove all emojis from text.

```javascript
removeEmojis('Hello 😀 World 🌍'); // 'Hello  World '
```

#### `hasEmoji(text)`
Check if text contains any emoji.

```javascript
hasEmoji('Hello 😀'); // true
hasEmoji('Hello World'); // false
```

### Counting Functions

#### `countEmojis(text)`
Count frequency of each emoji in text.

```javascript
countEmojis('😀 🌍 😀 🎉'); // { '😀': 2, '🌍': 1, '🎉': 1 }
```

#### `countTotalEmojis(text)`
Count total number of emojis in text.

```javascript
countTotalEmojis('😀 🌍 😀 🎉'); // 4
```

#### `getUniqueEmojis(text)`
Get array of unique emojis from text.

```javascript
getUniqueEmojis('😀 🌍 😀 🎉'); // ['😀', '🌍', '🎉']
```

#### `getEmojiFrequency(text)`
Get sorted array of [emoji, count] pairs by frequency.

```javascript
getEmojiFrequency('😀 🌍 😀 🎉 🎉 🎉');
// [['🎉', 3], ['😀', 2], ['🌍', 1]]
```

#### `getEmojiStats(text)`
Get comprehensive statistics about emoji usage.

```javascript
getEmojiStats('Hello 😀 World 🌍 😀 🎉');
// {
//   total: 3,
//   unique: 3,
//   frequency: { '😀': 2, '🌍': 1, '🎉': 1 },
//   sortedFrequency: [['😀', 2], ['🌍', 1], ['🎉', 1]],
//   categories: { smileys: ['😀'], travel: ['🌍'], activities: ['🎉'] },
//   hasSkinTone: false,
//   skinTones: []
// }
```

### Description Functions

#### `getEmojiDescription(emoji)`
Get text description for an emoji.

```javascript
getEmojiDescription('😀'); // 'grinning face'
getEmojiDescription('❤️'); // 'red heart'
getEmojiDescription('👍'); // 'thumbs up'
```

#### `replaceEmojisWithText(text, wrapper = '')`
Replace emojis with their descriptions.

```javascript
replaceEmojisWithText('I ❤️ coding');
// 'I red heart coding'

replaceEmojisWithText('I ❤️ coding', ':');
// 'I :red heart: coding'
```

#### `replaceEmoji(text, targetEmoji, replacement)`
Replace a specific emoji with text.

```javascript
replaceEmoji('Hello 😀!', '😀', 'World'); // 'Hello World!'
```

### Category Functions

#### `getEmojiCategory(emoji)`
Get category name for an emoji.

```javascript
getEmojiCategory('😀'); // 'smileys'
getEmojiCategory('🐶'); // 'animals'
getEmojiCategory('🍕'); // 'food'
```

#### `groupEmojisByCategory(text)`
Group all emojis in text by category.

```javascript
groupEmojisByCategory('😀 🐶 🍕 ⚽');
// {
//   smileys: ['😀'],
//   animals: ['🐶'],
//   food: ['🍕'],
//   activities: ['⚽']
// }
```

### Skin Tone Functions

#### `detectSkinTone(emoji)`
Detect skin tone modifier in emoji.

```javascript
detectSkinTone('👍🏻'); // 'light'
detectSkinTone('👍🏿'); // 'dark'
detectSkinTone('👍');  // null
```

#### `addSkinTone(emoji, tone)`
Add skin tone modifier to emoji.

```javascript
addSkinTone('👍', 'light'); // '👍🏻'
addSkinTone('👍', 'dark');  // '👍🏿'
```

#### `removeSkinTone(emoji)`
Remove skin tone modifier from emoji.

```javascript
removeSkinTone('👍🏻'); // '👍'
```

#### `getSupportedSkinTones()`
Get all supported skin tone options.

```javascript
getSupportedSkinTones();
// {
//   light: '\u{1F3FB}',
//   medium_light: '\u{1F3FC}',
//   medium: '\u{1F3FD}',
//   medium_dark: '\u{1F3FE}',
//   dark: '\u{1F3FF}',
//   none: null
// }
```

#### `isSkinToneModifier(char)`
Check if character is a skin tone modifier.

```javascript
isSkinToneModifier('\u{1F3FB}'); // true
isSkinToneModifier('a');         // false
```

## Emoji Categories

The library recognizes the following categories:

- **smileys** - Emoticons and smiley faces
- **people** - People and body parts
- **animals** - Animals and nature
- **food** - Food and drink
- **travel** - Travel and places
- **activities** - Sports and activities
- **objects** - Various objects
- **symbols** - Symbols and signs
- **flags** - Country flags

## Running Tests

```bash
node emoji_utils.test.js
```

## Running Examples

```bash
node examples.js
```

## License

MIT License - Free to use in any project.

## Emoji Descriptions

The library includes built-in descriptions for 300+ common emojis. Unknown emojis will return a generic description like `emoji_U+1F600`.

## Browser Support

This library uses ES6 features and works in modern browsers. For older browser support, use a transpiler like Babel.

## Node.js Support

Requires Node.js 6.0.0 or higher for full Unicode support.