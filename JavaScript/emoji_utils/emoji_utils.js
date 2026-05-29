/**
 * Emoji Utilities - A zero-dependency emoji processing toolkit
 * 
 * Features:
 * - Extract emojis from text
 * - Count emoji frequency
 * - Remove emojis from text
 * - Replace emojis with text descriptions
 * - Validate emoji characters
 * - Group emojis by category
 * - Detect emoji skin tones
 * - Handle emoji sequences (ZWJ, modifiers)
 */

// Comprehensive emoji Unicode ranges
const EMOJI_CODEPOINTS = [
  // Emoticons (Smileys)
  [0x1F600, 0x1F64F],
  // Supplemental Emoticons
  [0x1F900, 0x1F9FF],
  // People & Body
  [0x1F440, 0x1F4FC],
  [0x1F9B0, 0x1F9FF],
  // Animals
  [0x1F400, 0x1F43F],
  [0x1F980, 0x1F9AE],
  // Nature
  [0x1F330, 0x1F34F],
  [0x1F350, 0x1F37F],
  [0x1F38F, 0x1F39F],
  // Food & Drink
  [0x1F300, 0x1F32F],
  // Weather & Sky
  [0x1F30C, 0x1F30F],
  // Objects
  [0x1F4A0, 0x1F4FF],
  [0x1F500, 0x1F5FF],
  [0x1F680, 0x1F6FF],
  // Symbols
  [0x2600, 0x26FF],
  [0x2700, 0x27BF],
  [0x1F100, 0x1F1FF],
  // Flags
  [0x1F1E6, 0x1F1FF],
  
  // Clocks
  [0x1F550, 0x1F56F],
  // Celebration & Activities
  [0x1F382, 0x1F393],
  [0x1F3AE, 0x1F3B0],
  [0x1F3B2, 0x1F3C0],
  // Additional misc
  [0x231A, 0x231B],
  [0x23E9, 0x23F3],
  [0x23F8, 0x23FA],
  [0x25AA, 0x25AB],
  [0x25B6, 0x25B6],
  [0x25C0, 0x25C0],
  [0x25FB, 0x25FE],
  [0x2614, 0x2615],
  [0x2648, 0x2653],
  [0x267F, 0x267F],
  [0x2693, 0x2693],
  [0x26A1, 0x26A1],
  [0x26AA, 0x26AB],
  [0x26BD, 0x26BE],
  [0x26C4, 0x26C5],
  [0x26CE, 0x26CE],
  [0x26D4, 0x26D4],
  [0x26EA, 0x26EA],
  [0x26F2, 0x26F3],
  [0x26F5, 0x26F5],
  [0x26FA, 0x26FA],
  [0x26FD, 0x26FD],
  [0x2702, 0x2702],
  [0x2705, 0x2705],
  [0x2708, 0x270D],
  [0x270F, 0x270F],
  [0x2712, 0x2712],
  [0x2714, 0x2714],
  [0x2716, 0x2716],
  [0x271D, 0x271D],
  [0x2721, 0x2721],
  [0x2728, 0x2728],
  [0x2733, 0x2734],
  [0x2744, 0x2744],
  [0x2747, 0x2747],
  [0x274C, 0x274C],
  [0x274E, 0x274E],
  [0x2753, 0x2755],
  [0x2757, 0x2757],
  [0x2763, 0x2764],
  [0x2795, 0x2797],
  [0x27A1, 0x27A1],
  [0x27B0, 0x27B0],
  [0x27BF, 0x27BF],
  [0x2934, 0x2935],
  [0x2B05, 0x2B07],
  [0x2B1B, 0x2B1C],
  [0x2B50, 0x2B50],
  [0x2B55, 0x2B55],
  [0x3030, 0x3030],
  [0x3297, 0x3297],
  [0x3299, 0x3299],
  [0x1F004, 0x1F004],
  [0x1F0CF, 0x1F0CF],
  [0x1F170, 0x1F171],
  [0x1F17E, 0x1F17F],
  [0x1F18E, 0x1F18E],
  [0x1F191, 0x1F19A],
  [0x1F201, 0x1F202],
  [0x1F21A, 0x1F21A],
  [0x1F22F, 0x1F22F],
  [0x1F232, 0x1F23A],
  [0x1F250, 0x1F251],
  [0x203C, 0x203C],
  [0x2049, 0x2049],
  [0x2122, 0x2122],
  [0x2139, 0x2139],
  [0x2194, 0x2199],
  [0x21A9, 0x21AA],
  [0x231A, 0x231B],
  [0x2328, 0x2328],
  [0x23CF, 0x23CF],
  [0x24C2, 0x24C2],
  [0x25AA, 0x25AB],
  [0x25B6, 0x25B6],
  [0x25C0, 0x25C0],
  [0x25FB, 0x25FE],
  [0x2600, 0x2604],
  [0x260E, 0x260E],
  [0x2611, 0x2611],
  [0x2614, 0x2615],
  [0x2618, 0x2618],
  [0x261D, 0x261D],
  [0x2620, 0x2620],
  [0x2622, 0x2623],
  [0x2626, 0x2626],
  [0x262A, 0x262A],
  [0x262E, 0x262F],
  [0x2638, 0x263A],
  [0x2640, 0x2640],
  [0x2642, 0x2642],
  [0x2648, 0x2653],
  [0x265F, 0x265F],
  [0x2660, 0x2666],
  [0x2668, 0x2668],
  [0x267B, 0x267B],
  [0x267E, 0x267F],
  [0x2692, 0x2697],
  [0x2699, 0x2699],
  [0x269B, 0x269C],
  [0x26A0, 0x26A1],
  [0x26A7, 0x26A7],
  [0x26AA, 0x26AB],
  [0x26B0, 0x26B1],
  [0x26BD, 0x26BE],
  [0x26C4, 0x26C8],
  [0x26CE, 0x26CF],
  [0x26D1, 0x26D1],
  [0x26D3, 0x26D4],
  [0x26E9, 0x26EA],
  [0x26F0, 0x26F5],
  [0x26F7, 0x26FA],
  [0x26FD, 0x26FD],
  [0x2702, 0x2702],
  [0x2705, 0x2705],
  [0x2708, 0x2709],
  [0x270A, 0x270B],
  [0x270C, 0x270D],
  [0x270E, 0x270F],
  [0x2712, 0x2712],
  [0x2714, 0x2714],
  [0x2716, 0x2716],
  [0x271D, 0x271D],
  [0x2721, 0x2721],
  [0x2728, 0x2728],
  [0x2733, 0x2734],
  [0x2744, 0x2744],
  [0x2747, 0x2747],
  [0x274C, 0x274C],
  [0x274E, 0x274E],
  [0x2753, 0x2755],
  [0x2757, 0x2757],
  [0x2763, 0x2764],
  [0x2795, 0x2797],
  [0x27A1, 0x27A1],
  [0x27B0, 0x27B0],
  [0x27BF, 0x27BF],
  [0x2934, 0x2935],
  [0x2B05, 0x2B07],
  [0x2B1B, 0x2B1C],
  [0x2B50, 0x2B50],
  [0x2B55, 0x2B55],
  [0x3030, 0x3030],
  [0x3297, 0x3297],
  [0x3299, 0x3299],
];

// Special emoji modifiers and joiners
const ZWJ = 0x200D; // Zero-width joiner
const VARIATION_SELECTOR_16 = 0xFE0F; // Text presentation
const VARIATION_SELECTOR_15 = 0xFE0E; // Emoji presentation

// Skin tone modifiers (Fitzpatrick scale)
const SKIN_TONES = {
  'light': '\u{1F3FB}',
  'medium_light': '\u{1F3FC}',
  'medium': '\u{1F3FD}',
  'medium_dark': '\u{1F3FE}',
  'dark': '\u{1F3FF}',
  'none': null,
};

// Common emoji categories with ranges
const EMOJI_RANGES = {
  smileys: [[0x1F600, 0x1F64F], [0x1F900, 0x1F9FF]],
  people: [[0x1F442, 0x1F4FC], [0x1F9B0, 0x1F9FF]],
  animals: [[0x1F400, 0x1F43F], [0x1F980, 0x1F9AE]],
  food: [[0x1F34F, 0x1F37F], [0x1F95D, 0x1F95F]],
  travel: [[0x1F30D, 0x1F39F], [0x1F3D4, 0x1F3EF]],
  activities: [[0x1F382, 0x1F393], [0x1F3AE, 0x1F3C0]],
  objects: [[0x1F4A0, 0x1F4FF], [0x1F50D, 0x1F5FF]],
  symbols: [[0x1F300, 0x1F30C], [0x2600, 0x27BF], [0x1F100, 0x1F1FF]],
  flags: [[0x1F1E6, 0x1F1FF], [0x1F3F4, 0x1F3F4]],
};

/**
 * Check if a code point is in emoji ranges
 * @param {number} codePoint - Unicode code point to check
 * @returns {boolean} True if code point is an emoji
 */
function isEmojiCodePoint(codePoint) {
  for (const [start, end] of EMOJI_CODEPOINTS) {
    if (codePoint >= start && codePoint <= end) {
      return true;
    }
  }
  return false;
}

/**
 * Check if a character is an emoji
 * @param {string} char - Character to check
 * @returns {boolean} True if the character is an emoji
 */
function isEmoji(char) {
  if (!char || typeof char !== 'string') return false;
  const codePoint = char.codePointAt(0);
  return isEmojiCodePoint(codePoint);
}

/**
 * Extract all emojis from text
 * @param {string} text - Text to extract emojis from
 * @returns {string[]} Array of emojis found
 */
function extractEmojis(text) {
  if (!text || typeof text !== 'string') return [];
  
  const emojis = [];
  let i = 0;
  
  while (i < text.length) {
    const codePoint = text.codePointAt(i);
    
    // Check if this is an emoji start
    if (isEmojiCodePoint(codePoint)) {
      let emoji = String.fromCodePoint(codePoint);
      let nextIdx = i + (codePoint > 0xFFFF ? 2 : 1);
      
      // Handle emoji sequences
      while (nextIdx < text.length) {
        const nextCodePoint = text.codePointAt(nextIdx);
        
        // Zero-width joiner - emoji sequence continues
        if (nextCodePoint === ZWJ) {
          emoji += String.fromCodePoint(ZWJ);
          nextIdx++;
          if (nextIdx < text.length) {
            const joinedCodePoint = text.codePointAt(nextIdx);
            if (isEmojiCodePoint(joinedCodePoint)) {
              emoji += String.fromCodePoint(joinedCodePoint);
              nextIdx += joinedCodePoint > 0xFFFF ? 2 : 1;
            }
          }
          continue;
        }
        
        // Skin tone modifiers (Fitzpatrick scale: 1F3FB-1F3FF)
        if (nextCodePoint >= 0x1F3FB && nextCodePoint <= 0x1F3FF) {
          emoji += String.fromCodePoint(nextCodePoint);
          nextIdx++;
          continue;
        }
        
        // Variation selectors
        if (nextCodePoint === VARIATION_SELECTOR_16 || nextCodePoint === VARIATION_SELECTOR_15) {
          emoji += String.fromCodePoint(nextCodePoint);
          nextIdx++;
          continue;
        }
        
        // Regional indicator symbols for flags (A-Z: 1F1E6-1F1FF)
        if (nextCodePoint >= 0x1F1E6 && nextCodePoint <= 0x1F1FF) {
          emoji += String.fromCodePoint(nextCodePoint);
          nextIdx++;
          continue;
        }
        
        break;
      }
      
      emojis.push(emoji);
      i = nextIdx;
    } else {
      i++;
    }
  }
  
  return emojis;
}

/**
 * Count emoji frequency in text
 * @param {string} text - Text to analyze
 * @returns {Object} Object with emoji as key and count as value
 */
function countEmojis(text) {
  const emojis = extractEmojis(text);
  const counts = {};
  for (const emoji of emojis) {
    counts[emoji] = (counts[emoji] || 0) + 1;
  }
  return counts;
}

/**
 * Get emoji frequency sorted by count
 * @param {string} text - Text to analyze
 * @returns {Array} Array of [emoji, count] pairs sorted by count descending
 */
function getEmojiFrequency(text) {
  const counts = countEmojis(text);
  return Object.entries(counts).sort((a, b) => b[1] - a[1]);
}

/**
 * Remove all emojis from text
 * @param {string} text - Text to process
 * @returns {string} Text with emojis removed
 */
function removeEmojis(text) {
  if (!text || typeof text !== 'string') return '';
  
  let result = '';
  let i = 0;
  
  while (i < text.length) {
    const codePoint = text.codePointAt(i);
    
    if (isEmojiCodePoint(codePoint)) {
      // Skip emoji and its modifiers
      let nextIdx = i + (codePoint > 0xFFFF ? 2 : 1);
      
      while (nextIdx < text.length) {
        const nextCodePoint = text.codePointAt(nextIdx);
        
        if (nextCodePoint === ZWJ) {
          nextIdx++;
          if (nextIdx < text.length) {
            const joinedCP = text.codePointAt(nextIdx);
            nextIdx += joinedCP > 0xFFFF ? 2 : 1;
          }
          continue;
        }
        
        if ((nextCodePoint >= 0x1F3FB && nextCodePoint <= 0x1F3FF) ||
            nextCodePoint === VARIATION_SELECTOR_16 ||
            nextCodePoint === VARIATION_SELECTOR_15 ||
            (nextCodePoint >= 0x1F1E6 && nextCodePoint <= 0x1F1FF)) {
          nextIdx++;
          continue;
        }
        
        break;
      }
      
      i = nextIdx;
    } else {
      result += String.fromCodePoint(codePoint);
      i += codePoint > 0xFFFF ? 2 : 1;
    }
  }
  
  return result;
}

/**
 * Replace emojis with their text descriptions
 * @param {string} text - Text to process
 * @param {string} [wrapper=''] - Wrapper for description (e.g., ':')
 * @returns {string} Text with emojis replaced by descriptions
 */
function replaceEmojisWithText(text, wrapper = '') {
  if (!text || typeof text !== 'string') return '';
  
  let result = '';
  let i = 0;
  
  while (i < text.length) {
    const codePoint = text.codePointAt(i);
    
    if (isEmojiCodePoint(codePoint)) {
      let emoji = String.fromCodePoint(codePoint);
      let nextIdx = i + (codePoint > 0xFFFF ? 2 : 1);
      
      while (nextIdx < text.length) {
        const nextCP = text.codePointAt(nextIdx);
        
        if (nextCP === ZWJ) {
          emoji += String.fromCodePoint(ZWJ);
          nextIdx++;
          if (nextIdx < text.length) {
            const joinedCP = text.codePointAt(nextIdx);
            emoji += String.fromCodePoint(joinedCP);
            nextIdx += joinedCP > 0xFFFF ? 2 : 1;
          }
          continue;
        }
        
        if ((nextCP >= 0x1F3FB && nextCP <= 0x1F3FF) ||
            nextCP === VARIATION_SELECTOR_16 ||
            nextCP === VARIATION_SELECTOR_15 ||
            (nextCP >= 0x1F1E6 && nextCP <= 0x1F1FF)) {
          emoji += String.fromCodePoint(nextCP);
          nextIdx++;
          continue;
        }
        
        break;
      }
      
      const desc = getEmojiDescription(emoji);
      result += wrapper + desc + wrapper;
      i = nextIdx;
    } else {
      result += String.fromCodePoint(codePoint);
      i += codePoint > 0xFFFF ? 2 : 1;
    }
  }
  
  return result;
}

// Common emoji descriptions (abbreviated for space)
const EMOJI_DESCRIPTIONS = {
  '😀': 'grinning face', '😃': 'grinning face big eyes', '😄': 'grinning face smiling eyes',
  '😁': 'beaming face', '😅': 'grinning face sweat', '😂': 'face tears joy',
  '🤣': 'rofl', '😊': 'smiling face eyes', '😇': 'smiling face halo',
  '🙂': 'slightly smiling', '🙃': 'upside-down face', '😉': 'winking face',
  '😌': 'relieved face', '😍': 'smiling face heart-eyes', '🥰': 'smiling face hearts',
  '😘': 'blowing kiss', '😗': 'kissing face', '😙': 'kissing face eyes',
  '😚': 'kissing face closed eyes', '😋': 'savoring food', '😛': 'face tongue',
  '😜': 'winking face tongue', '🤪': 'zany face', '😝': 'squinting face tongue',
  '🤑': 'money-mouth', '🤗': 'hugging face', '🤭': 'hand over mouth',
  '🤫': 'shushing face', '🤔': 'thinking face', '🤐': 'zipper-mouth',
  '🤨': 'raised eyebrow', '😐': 'neutral face', '😑': 'expressionless',
  '😶': 'no mouth', '😏': 'smirking', '😒': 'unamused', '🙄': 'rolling eyes',
  '😬': 'grimacing', '😮': 'open mouth', '🤯': 'exploding head',
  '😱': 'screaming fear', '😨': 'fearful', '😰': 'anxious sweat',
  '😥': 'sad relieved', '😢': 'crying', '😭': 'loudly crying',
  '😤': 'steam nose', '😠': 'angry', '😡': 'pouting', '🤬': 'symbols mouth',
  '😷': 'medical mask', '🤒': 'thermometer', '🤕': 'head-bandage',
  '👋': 'waving hand', '🤚': 'back of hand', '🖐': 'fingers splayed',
  '✋': 'raised hand', '🖖': 'vulcan salute', '👌': 'OK hand',
  '🤌': 'pinched fingers', '🤏': 'pinching', '✌': 'victory hand',
  '🤞': 'crossed fingers', '🤟': 'love-you', '🤘': 'horns', '🤙': 'call me',
  '👈': 'pointing left', '👉': 'pointing right', '👆': 'pointing up',
  '🖕': 'middle finger', '👇': 'pointing down', '☝': 'index up',
  '👍': 'thumbs up', '👎': 'thumbs down', '✊': 'raised fist',
  '👊': 'oncoming fist', '🤛': 'left fist', '🤜': 'right fist',
  '👏': 'clapping', '🙌': 'raising hands', '👐': 'open hands',
  '🤲': 'palms up', '🤝': 'handshake', '🙏': 'folded hands',
  '❤': 'red heart', '🧡': 'orange heart', '💛': 'yellow heart',
  '💚': 'green heart', '💙': 'blue heart', '💜': 'purple heart',
  '🖤': 'black heart', '🤍': 'white heart', '🤎': 'brown heart',
  '💔': 'broken heart', '❣': 'heart exclamation', '💕': 'two hearts',
  '💞': 'revolving hearts', '💓': 'beating heart', '💗': 'growing heart',
  '💖': 'sparkling heart', '💘': 'heart arrow', '💝': 'heart ribbon',
  '💟': 'heart decoration',
  '🐶': 'dog face', '🐱': 'cat face', '🐭': 'mouse face',
  '🐹': 'hamster', '🐰': 'rabbit face', '🦊': 'fox', '🐻': 'bear',
  '🐼': 'panda', '🐨': 'koala', '🐯': 'tiger face', '🦁': 'lion',
  '🐮': 'cow face', '🐷': 'pig face', '🐸': 'frog', '🐵': 'monkey face',
  '🙈': 'see-no-evil', '🙉': 'hear-no-evil', '🙊': 'speak-no-evil',
  '🐒': 'monkey', '🐔': 'chicken', '🐧': 'penguin', '🐦': 'bird',
  '🦆': 'duck', '🦅': 'eagle', '🦉': 'owl', '🦇': 'bat', '🐺': 'wolf',
  '🦄': 'unicorn', '🐝': 'honeybee', '🦋': 'butterfly', '🐌': 'snail',
  '🐞': 'lady beetle', '🐢': 'turtle', '🐍': 'snake', '🦎': 'lizard',
  '🦖': 'T-Rex', '🦕': 'sauropod', '🐙': 'octopus', '🦑': 'squid',
  '🦐': 'shrimp', '🦞': 'lobster', '🦀': 'crab', '🐡': 'blowfish',
  '🐠': 'tropical fish', '🐟': 'fish', '🐬': 'dolphin', '🐳': 'whale',
  '🦈': 'shark', '🐊': 'crocodile', '🦍': 'gorilla', '🦧': 'orangutan',
  '🐘': 'elephant', '🦛': 'hippo', '🦏': 'rhino', '🐪': 'camel',
  '🦒': 'giraffe', '🦘': 'kangaroo', '🐃': 'water buffalo', '🐂': 'ox',
  '🐄': 'cow', '🐎': 'horse', '🐖': 'pig', '🐏': 'ram', '🐑': 'ewe',
  '🦙': 'llama', '🐐': 'goat', '🦌': 'deer', '🐕': 'dog', '🐩': 'poodle',
  '🐈': 'cat', '🐇': 'rabbit', '🦝': 'raccoon', '🦡': 'badger',
  '🦫': 'beaver', '🦦': 'otter', '🦥': 'sloth', '🐁': 'mouse', '🐀': 'rat',
  '🌸': 'cherry blossom', '💮': 'white flower', '🌹': 'rose',
  '🥀': 'wilted flower', '🌺': 'hibiscus', '🌻': 'sunflower',
  '🌼': 'blossom', '🌷': 'tulip', '🌱': 'seedling', '🌲': 'evergreen tree',
  '🌳': 'deciduous tree', '🌴': 'palm tree', '🌵': 'cactus',
  '🌾': 'rice', '🌿': 'herb', '☘': 'shamrock', '🍀': 'clover',
  '🍁': 'maple leaf', '🍂': 'fallen leaf', '🍃': 'leaf fluttering',
  '🍇': 'grapes', '🍈': 'melon', '🍉': 'watermelon', '🍊': 'tangerine',
  '🍋': 'lemon', '🍌': 'banana', '🍍': 'pineapple', '🥭': 'mango',
  '🍎': 'red apple', '🍏': 'green apple', '🍐': 'pear', '🍑': 'peach',
  '🍒': 'cherries', '🍓': 'strawberry', '🥝': 'kiwi', '🍅': 'tomato',
  '🥥': 'coconut', '🥑': 'avocado', '🍆': 'eggplant', '🥔': 'potato',
  '🥕': 'carrot', '🌽': 'corn', '🌶': 'hot pepper', '🥒': 'cucumber',
  '🥬': 'leafy green', '🥦': 'broccoli', '🧄': 'garlic', '🧅': 'onion',
  '🍄': 'mushroom', '🥜': 'peanuts', '🌰': 'chestnut', '🍞': 'bread',
  '🥐': 'croissant', '🥖': 'baguette', '🥨': 'pretzel', '🥯': 'bagel',
  '🥞': 'pancakes', '🧇': 'waffle', '🧀': 'cheese', '🍖': 'meat on bone',
  '🍗': 'poultry leg', '🥩': 'steak', '🥓': 'bacon', '🍔': 'hamburger',
  ' fries': 'french fries', '🍕': 'pizza', '🌭': 'hot dog',
  '🥪': 'sandwich', '🌮': 'taco', '🌯': 'burrito', '🥙': 'stuffed flatbread',
  '🥚': 'egg', '🍳': 'cooking', '🥘': 'pan food', '🍲': 'pot food',
  '🥣': 'bowl spoon', '🥗': 'salad', '🍿': 'popcorn', '🧈': 'butter',
  '🧂': 'salt', '🥫': 'canned food', '🍱': 'bento', '🍘': 'rice cracker',
  '🍙': 'rice ball', '🍚': 'cooked rice', '🍛': 'curry', '🍜': 'noodles',
  '🍝': 'spaghetti', '🍠': 'sweet potato', '🍢': 'oden', '🍣': 'sushi',
  '🍤': 'fried shrimp', '🍥': 'fish cake', '🥮': 'moon cake', '🍡': 'dango',
  '🥟': 'dumpling', '🥠': 'fortune cookie', '🥡': 'takeout box',
  '🍦': 'ice cream', '🍧': 'shaved ice', '🍨': 'ice cream cup',
  '🍩': 'doughnut', '🍪': 'cookie', '🎂': 'birthday cake', '🍰': 'shortcake',
  '🧁': 'cupcake', '🥧': 'pie', '🍫': 'chocolate', '🍬': 'candy',
  '🍭': 'lollipop', '🍮': 'custard', '🍯': 'honey', '🍼': 'baby bottle',
  '🥛': 'milk', '☕': 'coffee', '🍵': 'tea', '🍶': 'sake',
  '🍾': 'champagne', '🍷': 'wine', '🍸': 'cocktail', '🍹': 'tropical drink',
  '🍺': 'beer', '🍻': 'beers', '🥂': 'champagne glasses', '🥃': 'whiskey',
  '🥤': 'cup straw', '🧋': 'bubble tea', '🧃': 'juice box', '🧉': 'mate',
  '🧊': 'ice cube',
  '☀': 'sun', '🌤': 'sun cloud', '⛅': 'cloud sun', '🌥': 'cloud sun',
  '☁': 'cloud', '🌦': 'sun rain', '🌧': 'rain', '⛈': 'storm',
  '🌩': 'lightning', '🌨': 'snow', '❄': 'snowflake', '☃': 'snowman',
  '⛄': 'snowman no snow', '🌬': 'wind face', '💨': 'wind', '🌪': 'tornado',
  '🌫': 'fog', '🌈': 'rainbow', '🌂': 'umbrella closed', '☂': 'umbrella',
  '☔': 'umbrella rain', '⚡': 'lightning bolt', '🌊': 'wave', '🔥': 'fire',
  '💧': 'droplet', '💦': 'sweat drops',
  '🎃': 'jack-o-lantern', '🎄': 'Christmas tree', '🎆': 'fireworks',
  '🎇': 'sparkler', '🧨': 'firecracker', '✨': 'sparkles', '🎈': 'balloon',
  '🎉': 'party popper', '🎊': 'confetti ball', '🎀': 'ribbon', '🎁': 'gift',
  '🏆': 'trophy', '🏅': 'medal', '🥇': 'gold medal', '🥈': 'silver medal',
  '🥉': 'bronze medal', '⚽': 'soccer', '⚾': 'baseball', '🏀': 'basketball',
  '🏐': 'volleyball', '🏈': 'football', '🎾': 'tennis', '🎳': 'bowling',
  '🎯': 'bullseye', '🎮': 'video game', '🕹': 'joystick', '🎲': 'dice',
  '🧩': 'puzzle piece', '🧸': 'teddy bear', '♠': 'spade', '♥': 'heart',
  '♦': 'diamond', '♣': 'club',
  '⭐': 'star', '🌟': 'glowing star', '💫': 'dizzy', '✡': 'star of David',
  '☯': 'yin yang', '✝': 'cross', '♈': 'Aries', '♉': 'Taurus',
  '♊': 'Gemini', '♋': 'Cancer', '♌': 'Leo', '♍': 'Virgo',
  '♎': 'Libra', '♏': 'Scorpio', '♐': 'Sagittarius', '♑': 'Capricorn',
  '♒': 'Aquarius', '♓': 'Pisces',
  '🕐': '1 oclock', '🕑': '2 oclock', '🕒': '3 oclock', '🕓': '4 oclock',
  '🕔': '5 oclock', '🕕': '6 oclock', '🕖': '7 oclock', '🕗': '8 oclock',
  '🕘': '9 oclock', '🕙': '10 oclock', '🕚': '11 oclock', '🕛': '12 oclock',
  '⏰': 'alarm clock', '⏱': 'stopwatch', '⏲': 'timer', '🕰': 'clock',
  '⌛': 'hourglass done', '⏳': 'hourglass',
  '💡': 'light bulb', '🔦': 'flashlight', '🕯': 'candle',
  '💰': 'money bag', '💴': 'yen', '💵': 'dollar', '💶': 'euro',
  '💷': 'pound', '💸': 'money wings', '💳': 'credit card', '💎': 'gem',
  '⚖': 'balance', '🔧': 'wrench', '🔨': 'hammer', '⚙': 'gear',
  '🔗': 'link', '⛓': 'chains', '🧰': 'toolbox', '🧲': 'magnet',
  '🔫': 'pistol', '💣': 'bomb', '🔪': 'knife', '⚔': 'crossed swords',
  '🛡': 'shield', '🚬': 'cigarette', '💊': 'pill', '💉': 'syringe',
  '🧬': 'dna', '🦠': 'microbe', '🧪': 'test tube', '🌡': 'thermometer',
  '🧹': 'broom', '🧺': 'basket', '🧻': 'paper roll', '🧼': 'soap',
  '🪥': 'toothbrush', '🧽': 'sponge', '🧴': 'lotion', '🛁': 'bathtub',
  '🚿': 'shower', '🚽': 'toilet', '🪠': 'plunger', '🔑': 'key',
  '🗝': 'old key', '🚪': 'door', '🪑': 'chair', '🛋': 'couch',
  '🛏': 'bed', '🛌': 'person bed', '🖼': 'picture', '🛍': 'shopping bags',
  '🛒': 'shopping cart',
  '🏁': 'finish flag', '🚩': 'flag', '🎌': 'crossed flags',
  '🏴': 'black flag', '🏳': 'white flag',
  '✅': 'check', '❌': 'cross mark', '❎': 'cross button',
  '➕': 'plus', '➖': 'minus', '➗': 'divide', '✖': 'multiply',
  '♾': 'infinity', '‼': 'double exclamation', '⁉': 'exclamation question',
  '❓': 'question', '❔': 'white question', '❕': 'white exclamation',
  '❗': 'exclamation', '©': 'copyright', '®': 'registered', '™': 'trademark',
  '🔴': 'red circle', '🟠': 'orange circle', '🟡': 'yellow circle',
  '🟢': 'green circle', '🔵': 'blue circle', '🟣': 'purple circle',
  '🟤': 'brown circle', '⚫': 'black circle', '⚪': 'white circle',
  '⬛': 'black square', '⬜': 'white square', '🔶': 'orange diamond',
  '🔷': 'blue diamond', '🔸': 'small orange diamond', '🔹': 'small blue diamond',
  '🔺': 'red triangle up', '🔻': 'red triangle down', '💠': 'diamond dot',
  '🔘': 'radio button', '🔳': 'white button', '🔲': 'black button',
};

/**
 * Get description for an emoji
 * @param {string} emoji - Emoji character
 * @returns {string} Description or generated fallback
 */
function getEmojiDescription(emoji) {
  // Strip skin tone and variation selector for base lookup
  const base = emoji.replace(/[\u{1F3FB}-\u{1F3FF}\uFE0F]/gu, '');
  
  if (EMOJI_DESCRIPTIONS[emoji]) return EMOJI_DESCRIPTIONS[emoji];
  if (EMOJI_DESCRIPTIONS[base]) return EMOJI_DESCRIPTIONS[base];
  
  const cp = emoji.codePointAt(0);
  return `emoji U+${cp.toString(16).toUpperCase().padStart(4, '0')}`;
}

/**
 * Get category for an emoji
 * @param {string} emoji - Emoji character
 * @returns {string} Category name or 'unknown'
 */
function getEmojiCategory(emoji) {
  const cp = emoji.codePointAt(0);
  for (const [cat, ranges] of Object.entries(EMOJI_RANGES)) {
    for (const [start, end] of ranges) {
      if (cp >= start && cp <= end) return cat;
    }
  }
  return 'unknown';
}

/**
 * Group emojis by category
 * @param {string} text - Text to analyze
 * @returns {Object} Object with category as key and array of emojis as value
 */
function groupEmojisByCategory(text) {
  const emojis = extractEmojis(text);
  const groups = {};
  for (const emoji of emojis) {
    const cat = getEmojiCategory(emoji);
    if (!groups[cat]) groups[cat] = [];
    if (!groups[cat].includes(emoji)) groups[cat].push(emoji);
  }
  return groups;
}

/**
 * Detect skin tone of an emoji
 * @param {string} emoji - Emoji character
 * @returns {string|null} Skin tone name or null
 */
function detectSkinTone(emoji) {
  for (const [tone, char] of Object.entries(SKIN_TONES)) {
    if (char && emoji.includes(char)) return tone;
  }
  return null;
}

/**
 * Add skin tone to an emoji
 * @param {string} emoji - Base emoji
 * @param {string} tone - Skin tone name
 * @returns {string} Emoji with skin tone
 */
function addSkinTone(emoji, tone) {
  if (!SKIN_TONES[tone] || tone === 'none') return emoji;
  const base = emoji.replace(/[\u{1F3FB}-\u{1F3FF}]/gu, '');
  return base + SKIN_TONES[tone];
}

/**
 * Remove skin tone from an emoji
 * @param {string} emoji - Emoji with skin tone
 * @returns {string} Emoji without skin tone
 */
function removeSkinTone(emoji) {
  return emoji.replace(/[\u{1F3FB}-\u{1F3FF}]/gu, '');
}

/**
 * Check if character is a skin tone modifier
 * @param {string} char - Character to check
 * @returns {boolean}
 */
function isSkinToneModifier(char) {
  const cp = char.codePointAt(0);
  return cp >= 0x1F3FB && cp <= 0x1F3FF;
}

/**
 * Get all supported skin tones
 * @returns {Object}
 */
function getSupportedSkinTones() {
  return { ...SKIN_TONES };
}

/**
 * Count total emojis in text
 * @param {string} text - Text to analyze
 * @returns {number}
 */
function countTotalEmojis(text) {
  return extractEmojis(text).length;
}

/**
 * Check if text contains any emoji
 * @param {string} text - Text to check
 * @returns {boolean}
 */
function hasEmoji(text) {
  if (!text || typeof text !== 'string') return false;
  for (let i = 0; i < text.length; i++) {
    const cp = text.codePointAt(i);
    if (isEmojiCodePoint(cp)) return true;
    if (cp > 0xFFFF) i++;
  }
  return false;
}

/**
 * Get unique emojis from text
 * @param {string} text - Text to analyze
 * @returns {string[]}
 */
function getUniqueEmojis(text) {
  return [...new Set(extractEmojis(text))];
}

/**
 * Replace specific emoji in text
 * @param {string} text - Text to process
 * @param {string} targetEmoji - Emoji to replace
 * @param {string} replacement - Replacement text
 * @returns {string}
 */
function replaceEmoji(text, targetEmoji, replacement) {
  if (!text || !targetEmoji) return text;
  
  let result = '';
  let i = 0;
  
  while (i < text.length) {
    const cp = text.codePointAt(i);
    
    if (isEmojiCodePoint(cp)) {
      let emoji = String.fromCodePoint(cp);
      let nextIdx = i + (cp > 0xFFFF ? 2 : 1);
      
      while (nextIdx < text.length) {
        const nextCP = text.codePointAt(nextIdx);
        
        if (nextCP === ZWJ) {
          emoji += String.fromCodePoint(ZWJ);
          nextIdx++;
          if (nextIdx < text.length) {
            const joinedCP = text.codePointAt(nextIdx);
            emoji += String.fromCodePoint(joinedCP);
            nextIdx += joinedCP > 0xFFFF ? 2 : 1;
          }
          continue;
        }
        
        if ((nextCP >= 0x1F3FB && nextCP <= 0x1F3FF) ||
            nextCP === VARIATION_SELECTOR_16 ||
            nextCP === VARIATION_SELECTOR_15 ||
            (nextCP >= 0x1F1E6 && nextCP <= 0x1F1FF)) {
          emoji += String.fromCodePoint(nextCP);
          nextIdx++;
          continue;
        }
        
        break;
      }
      
      result += (emoji === targetEmoji) ? replacement : emoji;
      i = nextIdx;
    } else {
      result += String.fromCodePoint(cp);
      i += cp > 0xFFFF ? 2 : 1;
    }
  }
  
  return result;
}

/**
 * Get emoji stats for text
 * @param {string} text - Text to analyze
 * @returns {Object}
 */
function getEmojiStats(text) {
  const emojis = extractEmojis(text);
  const unique = getUniqueEmojis(text);
  const categories = groupEmojisByCategory(text);
  
  return {
    total: emojis.length,
    unique: unique.length,
    frequency: countEmojis(text),
    sortedFrequency: getEmojiFrequency(text),
    categories,
    hasSkinTone: emojis.some(e => detectSkinTone(e) !== null),
    skinTones: emojis.map(e => detectSkinTone(e)).filter(Boolean),
  };
}

module.exports = {
  isEmoji,
  extractEmojis,
  removeEmojis,
  countEmojis,
  countTotalEmojis,
  hasEmoji,
  getUniqueEmojis,
  getEmojiFrequency,
  getEmojiStats,
  getEmojiDescription,
  replaceEmojisWithText,
  replaceEmoji,
  getEmojiCategory,
  groupEmojisByCategory,
  detectSkinTone,
  addSkinTone,
  removeSkinTone,
  isSkinToneModifier,
  getSupportedSkinTones,
  EMOJI_RANGES,
  SKIN_TONES,
  EMOJI_DESCRIPTIONS,
};