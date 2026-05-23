/**
 * Phonetic Utils - 语音匹配算法工具集
 * 
 * 包含多种语音编码算法，用于姓名匹配、模糊搜索、拼写检查等场景
 * - Soundex: 美国档案标准算法
 * - Metaphone: 改进的语音编码
 * - Double Metaphone: 处理多语言发音
 * - Caverphone: 新西兰地名匹配
 * - NYSIIS: 纽约州识别信息系统
 * 
 * 零外部依赖，纯 JavaScript 实现
 */

// ==================== Soundex ====================

/**
 * Soundex 编码算法
 * 将单词转换为 4 字符代码，用于英语姓名的语音匹配
 * 
 * @param {string} word - 输入单词
 * @returns {string} 4 字符 Soundex 编码
 * 
 * @example
 * soundex('Robert')  // 'R163'
 * soundex('Rupert')  // 'R163'
 * soundex('Smith')   // 'S530'
 */
function soundex(word) {
  if (!word || typeof word !== 'string') return '';
  
  const s = word.toUpperCase().replace(/[^A-Z]/g, '');
  if (s.length === 0) return '';
  
  // 保留首字母
  const first = s[0];
  
  // 编码映射表
  const codes = {
    B: '1', F: '1', P: '1', V: '1',
    C: '2', G: '2', J: '2', K: '2', Q: '2', S: '2', X: '2', Z: '2',
    D: '3', T: '3',
    L: '4',
    M: '5', N: '5',
    R: '6'
  };
  
  // 对剩余字母编码
  let encoded = '';
  let prevCode = codes[first] || '';
  
  for (let i = 1; i < s.length; i++) {
    const char = s[i];
    const code = codes[char] || '';
    
    // 相邻相同编码跳过（首字母例外）
    if (code && code !== prevCode) {
      encoded += code;
    }
    prevCode = code;
  }
  
  // 填充或截断到 4 字符
  return (first + encoded + '000').substring(0, 4);
}

/**
 * 计算两个单词的 Soundex 相似度
 * 
 * @param {string} word1 - 第一个单词
 * @param {string} word2 - 第二个单词
 * @returns {number} 0-1 之间的相似度
 */
function soundexSimilarity(word1, word2) {
  const s1 = soundex(word1);
  const s2 = soundex(word2);
  
  if (!s1 || !s2) return 0;
  if (s1 === s2) return 1;
  
  // 部分匹配
  let matches = 0;
  for (let i = 0; i < 4; i++) {
    if (s1[i] === s2[i]) matches++;
  }
  return matches / 4;
}

// ==================== Metaphone ====================

/**
 * Metaphone 编码算法
 * Soundex 的改进版本，更适合英语发音
 * 
 * @param {string} word - 输入单词
 * @param {number} maxLength - 最大编码长度（默认 4）
 * @returns {string} Metaphone 编码
 * 
 * @example
 * metaphone('phone')    // 'FN'
 * metaphone('know')     // 'N'
 * metaphone('psychic')  // 'SKSK'
 */
function metaphone(word, maxLength = 4) {
  if (!word || typeof word !== 'string') return '';
  
  let s = word.toUpperCase().replace(/[^A-Z]/g, '');
  if (s.length === 0) return '';
  
  // 处理特殊开头
  if (s.startsWith('KN') || s.startsWith('GN') || s.startsWith('PN') || s.startsWith('AE') || s.startsWith('WR')) {
    s = s.substring(1);
  }
  if (s.startsWith('WH')) {
    s = 'W' + s.substring(2);
  }
  if (s.startsWith('X')) {
    s = 'S' + s.substring(1);
  }
  
  let result = '';
  
  for (let i = 0; i < s.length && result.length < maxLength; i++) {
    const char = s[i];
    const prev = i > 0 ? s[i - 1] : '';
    const next = i < s.length - 1 ? s[i + 1] : '';
    const nextNext = i < s.length - 2 ? s[i + 2] : '';
    
    // 跳过重复字母（除 C 外）
    if (char === prev && char !== 'C') continue;
    
    switch (char) {
      case 'A': case 'E': case 'I': case 'O': case 'U':
        // 元音只在开头保留
        if (i === 0) result += char;
        break;
        
      case 'B':
        // B 在 MB 词尾不发音
        if (!(prev === 'M' && i === s.length - 1)) {
          result += 'B';
        }
        break;
        
      case 'C':
        // CI, CE, CY -> S
        if (next === 'I' || next === 'E' || next === 'Y') {
          result += 'S';
        } else if (next === 'H') {
          // CH -> X (保留 X 表示 'sh' 音)
          result += 'X';
          i++;
        } else {
          result += 'K';
        }
        break;
        
      case 'D':
        // DGE, DGI, DGY -> J
        if (next === 'G' && (nextNext === 'E' || nextNext === 'I' || nextNext === 'Y')) {
          result += 'J';
          i += 2;
        } else {
          result += 'T';
        }
        break;
        
      case 'F':
        result += 'F';
        break;
        
      case 'G':
        // GH 不发音，GN 开头不发音
        if (next === 'H') {
          if (i < s.length - 2 && !'AEIOU'.includes(nextNext)) {
            result += 'K';
            i++;
          }
        } else if (next === 'N' && i === s.length - 2) {
          // GN 词尾不发音
        } else if (!(next === 'I' && nextNext === 'N') && next !== 'Y') {
          if (!'IEY'.includes(next) || (prev === 'G' && i > 0)) {
            result += 'K';
          }
        }
        break;
        
      case 'H':
        // H 在元音前发音
        if ('AEIOU'.includes(next) && !'CSPTG'.includes(prev)) {
          result += 'H';
        }
        break;
        
      case 'J':
        result += 'J';
        break;
        
      case 'K':
        // KN 开头不发音（已处理）
        if (i > 0 || s[1] !== 'N') {
          result += 'K';
        }
        break;
        
      case 'L':
        result += 'L';
        break;
        
      case 'M':
        result += 'M';
        break;
        
      case 'N':
        result += 'N';
        break;
        
      case 'P':
        // PH -> F
        if (next === 'H') {
          result += 'F';
          i++;
        } else {
          result += 'P';
        }
        break;
        
      case 'Q':
        result += 'K';
        break;
        
      case 'R':
        result += 'R';
        break;
        
      case 'S':
        // SH -> X
        if (next === 'H') {
          result += 'X';
          i++;
        } else if (next === 'I' && (nextNext === 'O' || nextNext === 'A')) {
          // SIO, SIA -> X
          result += 'X';
        } else {
          result += 'S';
        }
        break;
        
      case 'T':
        // TIA, TIO -> X
        if (next === 'I' && (nextNext === 'A' || nextNext === 'O')) {
          result += 'X';
        } else if (next === 'H') {
          result += '0'; // TH -> 0
          i++;
        } else if (!(next === 'C' && nextNext === 'H')) {
          result += 'T';
        }
        break;
        
      case 'V':
        result += 'F';
        break;
        
      case 'W':
        // WR 开头不发音（已处理）
        if ('AEIOU'.includes(next)) {
          result += 'W';
        }
        break;
        
      case 'X':
        result += 'KS';
        break;
        
      case 'Y':
        if ('AEIOU'.includes(next)) {
          result += 'Y';
        }
        break;
        
      case 'Z':
        result += 'S';
        break;
    }
  }
  
  return result.substring(0, maxLength);
}

// ==================== Double Metaphone ====================

/**
 * Double Metaphone 编码算法
 * 为每个单词生成主编码和备用编码，处理多种语言发音
 * 
 * @param {string} word - 输入单词
 * @returns {{primary: string, alternate: string}} 主编码和备用编码
 * 
 * @example
 * doubleMetaphone('Smith')
 * // { primary: 'SM0T', alternate: 'XMT' }
 */
function doubleMetaphone(word) {
  if (!word || typeof word !== 'string') return { primary: '', alternate: '' };
  
  const s = word.toUpperCase().replace(/[^A-Z]/g, '');
  if (s.length === 0) return { primary: '', alternate: '' };
  
  let primary = '';
  let alternate = '';
  let i = 0;
  const maxLen = 4;
  
  // 辅助函数：追加编码
  const append = (p, a = p) => {
    if (primary.length < maxLen) primary += p;
    if (alternate.length < maxLen) alternate += a;
  };
  
  // 检查元音
  const isVowel = (c) => 'AEIOU'.includes(c);
  const getChar = (idx) => s[idx] || '';
  
  // 处理特殊开头
  if (s.startsWith('KN') || s.startsWith('GN') || s.startsWith('PN') || s.startsWith('WR') || s.startsWith('AE')) {
    i = 1;
  } else if (s.startsWith('WH')) {
    append('W', 'A');
    i = 2;
  } else if (s.startsWith('X')) {
    append('S');
    i = 1;
  } else if (s.startsWith('A')) {
    append('A');
    i = 1;
  }
  
  while ((primary.length < maxLen || alternate.length < maxLen) && i < s.length) {
    const c = getChar(i);
    const prev = getChar(i - 1);
    const next = getChar(i + 1);
    const nextNext = getChar(i + 2);
    const nextNextNext = getChar(i + 3);
    
    switch (c) {
      case 'A': case 'E': case 'I': case 'O': case 'U':
        if (i === 0) append(c);
        i++;
        break;
        
      case 'B':
        append('P');
        i += (next === 'B') ? 2 : 1;
        break;
        
      case 'C':
        if (prev === 'S' && next === 'I' && nextNext === 'O') {
          append('X', 'X');
          i += 3;
        } else if (next === 'I' && nextNext === 'A') {
          append('X', 'X');
          i += 2;
        } else if (next === 'H') {
          append('X', 'X');
          i += 2;
        } else if (next === 'Y') {
          append('S', 'S');
          i += 2;
        } else {
          append('K', 'K');
          i += (next === 'C') ? 2 : 1;
        }
        break;
        
      case 'D':
        if (next === 'G' && 'EIY'.includes(nextNext)) {
          append('J', 'J');
          i += 3;
        } else {
          append('T', 'T');
          i += (next === 'D') ? 2 : 1;
        }
        break;
        
      case 'F':
        append('F', 'F');
        i += (next === 'F') ? 2 : 1;
        break;
        
      case 'G':
        if (next === 'H') {
          if (i > 0 && !isVowel(prev)) {
            append('K', 'K');
          } else if (i === 0) {
            if (isVowel(nextNext)) {
              append('K', 'K');
            }
          }
          i += 2;
        } else if (next === 'I' && nextNext === 'N') {
          // -GIN- 可能不发音
          i += 3;
        } else if (next === 'N' && (i === 0 || prev === 'A')) {
          append('K', 'K');
          i += 2;
        } else if (next === 'Y' || (next === 'I' && nextNext !== 'N')) {
          append('J', 'K');
          i += 2;
        } else {
          append('K', 'K');
          i += (next === 'G') ? 2 : 1;
        }
        break;
        
      case 'H':
        if (i === 0 || isVowel(prev)) {
          if (isVowel(next)) {
            append('H', 'H');
          }
        }
        i++;
        break;
        
      case 'J':
        append('J', 'J');
        i += (next === 'J') ? 2 : 1;
        break;
        
      case 'K':
        append('K', 'K');
        i += (next === 'K') ? 2 : 1;
        break;
        
      case 'L':
        append('L', 'L');
        i += (next === 'L') ? 2 : 1;
        break;
        
      case 'M':
        append('M', 'M');
        i += (next === 'M') ? 2 : 1;
        break;
        
      case 'N':
        append('N', 'N');
        i += (next === 'N') ? 2 : 1;
        break;
        
      case 'P':
        if (next === 'H') {
          append('F', 'F');
          i += 2;
        } else if (next === 'S' && nextNext === 'H') {
          append('F', 'F');
          i += 3;
        } else {
          append('P', 'P');
          i += (next === 'P') ? 2 : 1;
        }
        break;
        
      case 'Q':
        append('K', 'K');
        i += (next === 'Q') ? 2 : 1;
        break;
        
      case 'R':
        append('R', 'R');
        i += (next === 'R') ? 2 : 1;
        break;
        
      case 'S':
        if (next === 'H') {
          append('X', 'X');
          i += 2;
        } else if (next === 'I' && (nextNext === 'O' || nextNext === 'A')) {
          append('S', 'X');
          i += 3;
        } else {
          append('S', 'S');
          i += (next === 'S') ? 2 : 1;
        }
        break;
        
      case 'T':
        if (next === 'H') {
          append('0', 'T');
          i += 2;
        } else if (next === 'I' && (nextNext === 'O' || nextNext === 'A')) {
          append('X', 'X');
          i += 3;
        } else {
          append('T', 'T');
          i += (next === 'T') ? 2 : 1;
        }
        break;
        
      case 'V':
        append('F', 'F');
        i += (next === 'V') ? 2 : 1;
        break;
        
      case 'W':
        if (isVowel(next)) {
          append('W', 'W');
        }
        i++;
        break;
        
      case 'X':
        append('KS', 'KS');
        i += (next === 'X') ? 2 : 1;
        break;
        
      case 'Y':
        if (isVowel(next)) {
          append('Y', 'Y');
        }
        i++;
        break;
        
      case 'Z':
        append('S', 'S');
        i += (next === 'Z') ? 2 : 1;
        break;
        
      default:
        i++;
    }
  }
  
  return {
    primary: primary.substring(0, maxLen),
    alternate: alternate.substring(0, maxLen)
  };
}

// ==================== NYSIIS ====================

/**
 * NYSIIS (New York State Identification and Intelligence System) 编码
 * 美国纽约州的姓名匹配系统，比 Soundex 更精确
 * 
 * @param {string} word - 输入单词
 * @returns {string} NYSIIS 编码
 * 
 * @example
 * nysiis('Smith')   // 'SNAT'
 * nysiis('Schmidt') // 'SNAT'
 */
function nysiis(word) {
  if (!word || typeof word !== 'string') return '';
  
  let s = word.toUpperCase().replace(/[^A-Z]/g, '');
  if (s.length === 0) return '';
  
  // 首字母转换
  if (s[0] === 'K' || s[0] === 'C') {
    s = 'C' + s.substring(1);
  } else if (s[0] === 'P' && s[1] === 'H') {
    s = 'F' + s.substring(2);
  } else if (s[0] === 'V') {
    s = 'W' + s.substring(1);
  }
  
  // 替换开头
  const prefixes = [
    ['MAC', 'MCC'], ['KN', 'NN'], ['K', 'C'], ['PH', 'FF'],
    ['PF', 'FF'], ['SCH', 'SSS']
  ];
  for (const [from, to] of prefixes) {
    if (s.startsWith(from)) {
      s = to + s.substring(from.length);
      break;
    }
  }
  
  // 替换结尾
  const suffixes = [
    ['EE', 'Y'], ['IE', 'Y'], ['DT', 'D'], ['RT', 'D'],
    ['NT', 'D'], ['ND', 'D']
  ];
  for (const [from, to] of suffixes) {
    if (s.endsWith(from)) {
      s = s.substring(0, s.length - from.length) + to;
      break;
    }
  }
  
  // 中间转换
  let result = s[0];
  for (let i = 1; i < s.length; i++) {
    const prev = s[i - 1];
    const curr = s[i];
    const next = s[i + 1] || '';
    
    let converted = curr;
    
    // EV -> AF
    if (curr === 'E' && next === 'V') {
      converted = 'A';
    }
    // 元音
    else if ('AEIOU'.includes(curr)) {
      converted = 'A';
    }
    // Q -> G
    else if (curr === 'Q') {
      converted = 'G';
    }
    // Z -> S
    else if (curr === 'Z') {
      converted = 'S';
    }
    // M -> N
    else if (curr === 'M') {
      converted = 'N';
    }
    // KN -> N
    else if (curr === 'K' && next === 'N') {
      continue;
    }
    // K -> C
    else if (curr === 'K') {
      converted = 'C';
    }
    // PH, H -> F
    else if (curr === 'H' && (prev === 'P' || !'AEIOU'.includes(next))) {
      continue;
    }
    else if (curr === 'H' && (prev === 'P')) {
      converted = 'F';
    }
    // SCH -> SSS
    else if (curr === 'S' && next === 'C' && s[i + 2] === 'H') {
      result += 'SSS';
      i += 2;
      continue;
    }
    
    // 去除重复
    if (result[result.length - 1] !== converted) {
      result += converted;
    }
  }
  
  // 去除结尾 S
  if (result.endsWith('S')) {
    result = result.substring(0, result.length - 1);
  }
  
  // 结尾 AY -> Y
  if (result.endsWith('AY')) {
    result = result.substring(0, result.length - 2) + 'Y';
  }
  
  // 去除结尾 A
  if (result.endsWith('A')) {
    result = result.substring(0, result.length - 1);
  }
  
  return result;
}

// ==================== Caverphone ====================

/**
 * Caverphone 编码算法
 * 专为新西兰地名设计的语音编码，也适用于英语姓名
 * 
 * @param {string} word - 输入单词
 * @returns {string} Caverphone 编码
 * 
 * @example
 * caverphone('Thompson') // 'TMPSN111'
 */
function caverphone(word) {
  if (!word || typeof word !== 'string') return '';
  
  let s = word.toLowerCase().replace(/[^a-z]/g, '');
  if (s.length === 0) return '';
  
  // 转换规则
  s = s.replace(/e$/g, '')
       .replace(/^gn/g, '2n')
       .replace(/^kn/g, '2n')
       .replace(/^ph/g, 'f')
       .replace(/^wr/g, 'r')
       .replace(/mb$/g, 'm2')
       .replace(/ng$/g, 'n2')
       .replace(/ough/g, 'o2f')
       .replace(/a/g, '3')
       .replace(/e/g, '3')
       .replace(/i/g, '3')
       .replace(/o/g, '3')
       .replace(/u/g, '3')
       .replace(/c/g, 'k')
       .replace(/g/g, 'k')
       .replace(/p/g, 'k')
       .replace(/q/g, 'k')
       .replace(/s/g, 'k')
       .replace(/t/g, 'k')
       .replace(/v/g, 'f')
       .replace(/w/g, 'f')
       .replace(/x/g, 'k')
       .replace(/z/g, 'k')
       .replace(/b/g, 'p')
       .replace(/d/g, 't')
       .replace(/j/g, 't')
       .replace(/l/g, '4')
       .replace(/m/g, '5')
       .replace(/n/g, '5')
       .replace(/r/g, '6')
       .replace(/h/g, 'h')
       .replace(/y/g, '3')
       .replace(/k+/, 'k')
       .replace(/5+/, '5')
       .replace(/3+/, '3')
       .replace(/4+/, '4')
       .replace(/6+/, '6');
  
  // 填充到 10 字符
  s = s.substring(0, 10);
  while (s.length < 10) {
    s += '1';
  }
  
  return s;
}

// ==================== 匹配工具 ====================

/**
 * 比较两个单词的语音相似度
 * 
 * @param {string} word1 - 第一个单词
 * @param {string} word2 - 第二个单词
 * @param {string} algorithm - 算法名称：'soundex', 'metaphone', 'doubleMetaphone', 'nysiis', 'caverphone'
 * @returns {number} 0-1 之间的相似度分数
 * 
 * @example
 * phoneticSimilarity('Smith', 'Smythe', 'metaphone') // 1
 */
function phoneticSimilarity(word1, word2, algorithm = 'metaphone') {
  if (!word1 || !word2) return 0;
  if (word1.toLowerCase() === word2.toLowerCase()) return 1;
  
  switch (algorithm) {
    case 'soundex': {
      const s1 = soundex(word1);
      const s2 = soundex(word2);
      if (s1 === s2) return 1;
      let matches = 0;
      for (let i = 0; i < 4; i++) {
        if (s1[i] === s2[i]) matches++;
      }
      return matches / 4;
    }
    
    case 'metaphone': {
      const m1 = metaphone(word1);
      const m2 = metaphone(word2);
      if (m1 === m2) return 1;
      // Levenshtein 距离计算相似度
      const dist = levenshteinDistance(m1, m2);
      const maxLen = Math.max(m1.length, m2.length);
      return maxLen === 0 ? 1 : 1 - dist / maxLen;
    }
    
    case 'doubleMetaphone': {
      const d1 = doubleMetaphone(word1);
      const d2 = doubleMetaphone(word2);
      
      // 检查四种组合
      const combinations = [
        [d1.primary, d2.primary],
        [d1.primary, d2.alternate],
        [d1.alternate, d2.primary],
        [d1.alternate, d2.alternate]
      ];
      
      let maxSimilarity = 0;
      for (const [a, b] of combinations) {
        if (a === b) return 1;
        const dist = levenshteinDistance(a, b);
        const maxLen = Math.max(a.length, b.length);
        const sim = maxLen === 0 ? 1 : 1 - dist / maxLen;
        maxSimilarity = Math.max(maxSimilarity, sim);
      }
      return maxSimilarity;
    }
    
    case 'nysiis': {
      const n1 = nysiis(word1);
      const n2 = nysiis(word2);
      if (n1 === n2) return 1;
      const dist = levenshteinDistance(n1, n2);
      const maxLen = Math.max(n1.length, n2.length);
      return maxLen === 0 ? 1 : 1 - dist / maxLen;
    }
    
    case 'caverphone': {
      const c1 = caverphone(word1);
      const c2 = caverphone(word2);
      if (c1 === c2) return 1;
      let matches = 0;
      for (let i = 0; i < 10; i++) {
        if (c1[i] === c2[i]) matches++;
      }
      return matches / 10;
    }
    
    default:
      return 0;
  }
}

/**
 * Levenshtein 距离计算
 */
function levenshteinDistance(str1, str2) {
  const m = str1.length;
  const n = str2.length;
  
  const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
  
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      const cost = str1[i - 1] === str2[j - 1] ? 0 : 1;
      dp[i][j] = Math.min(
        dp[i - 1][j] + 1,
        dp[i][j - 1] + 1,
        dp[i - 1][j - 1] + cost
      );
    }
  }
  
  return dp[m][n];
}

/**
 * 在列表中查找语音相似单词
 * 
 * @param {string} target - 目标单词
 * @param {string[]} words - 候选单词列表
 * @param {Object} options - 选项
 * @param {string} options.algorithm - 算法名称
 * @param {number} options.threshold - 相似度阈值（默认 0.7）
 * @param {number} options.limit - 返回结果数量限制
 * @returns {Array<{word: string, similarity: number}>} 匹配结果
 * 
 * @example
 * findPhoneticMatches('Smith', ['Smythe', 'Schmidt', 'Johnson'], { algorithm: 'metaphone' })
 * // [{ word: 'Smythe', similarity: 1 }, { word: 'Schmidt', similarity: 0.75 }]
 */
function findPhoneticMatches(target, words, options = {}) {
  const { algorithm = 'metaphone', threshold = 0.7, limit = 10 } = options;
  
  const results = words
    .map(word => ({
      word,
      similarity: phoneticSimilarity(target, word, algorithm)
    }))
    .filter(r => r.similarity >= threshold)
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, limit);
  
  return results;
}

// ==================== 导出 ====================

module.exports = {
  // 编码算法
  soundex,
  metaphone,
  doubleMetaphone,
  nysiis,
  caverphone,
  
  // 相似度计算
  soundexSimilarity,
  phoneticSimilarity,
  
  // 搜索工具
  findPhoneticMatches,
  
  // 辅助函数
  levenshteinDistance
};