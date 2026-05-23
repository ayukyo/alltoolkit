/**
 * diff_utils - 文本差异对比工具
 * 零外部依赖，纯 JavaScript 实现
 * 
 * 功能：
 * 1. 计算两段文本的差异
 * 2. 支持 LCS（最长公共子序列）算法
 * 3. 生成统一格式 diff（unified diff）
 * 4. 支持行级和字符级对比
 * 5. diff 应用与回滚
 */

/**
 * 差异类型枚举
 */
const DiffType = {
  EQUAL: 'equal',    // 相同
  ADD: 'add',        // 新增
  DELETE: 'delete'   // 删除
};

/**
 * 计算最长公共子序列（LCS）
 * @param {string[]} arr1 - 第一个数组
 * @param {string[]} arr2 - 第二个数组
 * @returns {number[][]} LCS 长度矩阵
 */
function computeLCSMatrix(arr1, arr2) {
  const m = arr1.length;
  const n = arr2.length;
  const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (arr1[i - 1] === arr2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  return dp;
}

/**
 * 从 LCS 矩阵回溯获取差异
 * @param {string[]} arr1 - 第一个数组
 * @param {string[]} arr2 - 第二个数组
 * @param {number[][]} dp - LCS 矩阵
 * @returns {Array<{type: string, value: string}>} 差异结果
 */
function backtrackDiff(arr1, arr2, dp) {
  const result = [];
  let i = arr1.length;
  let j = arr2.length;

  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && arr1[i - 1] === arr2[j - 1]) {
      result.unshift({ type: DiffType.EQUAL, value: arr1[i - 1] });
      i--;
      j--;
    } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
      result.unshift({ type: DiffType.ADD, value: arr2[j - 1] });
      j--;
    } else if (i > 0) {
      result.unshift({ type: DiffType.DELETE, value: arr1[i - 1] });
      i--;
    }
  }

  return result;
}

/**
 * 比较两段文本（行级）
 * @param {string} text1 - 原始文本
 * @param {string} text2 - 新文本
 * @returns {Array<{type: string, value: string}>} 差异结果
 */
function diffLines(text1, text2) {
  const lines1 = text1.split('\n');
  const lines2 = text2.split('\n');
  const dp = computeLCSMatrix(lines1, lines2);
  return backtrackDiff(lines1, lines2, dp);
}

/**
 * 比较两段文本（字符级）
 * @param {string} text1 - 原始文本
 * @param {string} text2 - 新文本
 * @returns {Array<{type: string, value: string}>} 差异结果
 */
function diffChars(text1, text2) {
  const chars1 = text1.split('');
  const chars2 = text2.split('');
  const dp = computeLCSMatrix(chars1, chars2);
  return backtrackDiff(chars1, chars2, dp);
}

/**
 * 比较两段文本（单词级）
 * @param {string} text1 - 原始文本
 * @param {string} text2 - 新文本
 * @returns {Array<{type: string, value: string}>} 差异结果
 */
function diffWords(text1, text2) {
  const words1 = text1.split(/(\s+)/);
  const words2 = text2.split(/(\s+)/);
  const dp = computeLCSMatrix(words1, words2);
  return backtrackDiff(words1, words2, dp);
}

/**
 * 合并相邻的相同类型差异
 * @param {Array<{type: string, value: string}>} diff - 差异结果
 * @returns {Array<{type: string, value: string}>} 合并后的差异
 */
function mergeDiff(diff) {
  if (diff.length === 0) return [];

  const result = [];
  let current = { ...diff[0] };

  for (let i = 1; i < diff.length; i++) {
    if (diff[i].type === current.type) {
      current.value += diff[i].value;
    } else {
      result.push(current);
      current = { ...diff[i] };
    }
  }
  result.push(current);

  return result;
}

/**
 * 生成统一格式 diff（Unified Diff）
 * @param {string} text1 - 原始文本
 * @param {string} text2 - 新文本
 * @param {Object} options - 选项
 * @param {string} options.filename1 - 原始文件名
 * @param {string} options.filename2 - 新文件名
 * @param {number} options.context - 上下文行数
 * @returns {string} Unified diff 格式字符串
 */
function unifiedDiff(text1, text2, options = {}) {
  const {
    filename1 = 'a/original',
    filename2 = 'b/new',
    context = 3
  } = options;

  const diff = diffLines(text1, text2);
  const lines1 = text1.split('\n');
  const lines2 = text2.split('\n');

  let result = `--- ${filename1}\n+++ ${filename2}\n`;

  // 找出所有变化的区块
  const hunks = [];
  let currentHunk = null;

  for (let i = 0; i < diff.length; i++) {
    const item = diff[i];
    if (item.type !== DiffType.EQUAL) {
      if (!currentHunk) {
        // 找到变化的起始位置
        let startLine = 1;
        let count = 0;
        for (let j = 0; j < i; j++) {
          if (diff[j].type === DiffType.EQUAL) count++;
        }
        startLine = Math.max(1, count - context + 1);
        currentHunk = {
          startLine,
          oldStart: startLine,
          oldCount: 0,
          newStart: startLine,
          newCount: 0,
          lines: []
        };
        // 添加前置上下文
        const contextStart = Math.max(0, count - context);
        for (let j = contextStart; j < count; j++) {
          currentHunk.lines.push(' ' + lines1[j]);
          currentHunk.oldCount++;
          currentHunk.newCount++;
        }
      }
    }

    if (currentHunk) {
      if (item.type === DiffType.EQUAL) {
        currentHunk.lines.push(' ' + item.value);
        currentHunk.oldCount++;
        currentHunk.newCount++;
      } else if (item.type === DiffType.DELETE) {
        currentHunk.lines.push('-' + item.value);
        currentHunk.oldCount++;
      } else if (item.type === DiffType.ADD) {
        currentHunk.lines.push('+' + item.value);
        currentHunk.newCount++;
      }

      // 检查是否结束
      const nextItem = diff[i + 1];
      if (!nextItem || (nextItem.type === DiffType.EQUAL && 
          (i + context >= diff.length - 1 || 
           diff.slice(i + 1, i + context + 1).every(d => d.type === DiffType.EQUAL)))) {
        // 添加后置上下文
        let added = 0;
        for (let j = 1; j <= context && i + j < diff.length; j++) {
          if (diff[i + j].type === DiffType.EQUAL && added < context) {
            currentHunk.lines.push(' ' + diff[i + j].value);
            currentHunk.oldCount++;
            currentHunk.newCount++;
            added++;
          }
        }
        hunks.push(currentHunk);
        currentHunk = null;
      }
    }
  }

  // 生成 hunk header 并添加到结果
  for (const hunk of hunks) {
    result += `@@ -${hunk.oldStart},${hunk.oldCount} +${hunk.newStart},${hunk.newCount} @@\n`;
    for (const line of hunk.lines) {
      result += line + '\n';
    }
  }

  return result;
}

/**
 * 生成带 ANSI 颜色的 diff 输出
 * @param {Array<{type: string, value: string}>} diff - 差异结果
 * @returns {string} 带颜色的字符串
 */
function colorDiff(diff) {
  const GREEN = '\x1b[32m';
  const RED = '\x1b[31m';
  const RESET = '\x1b[0m';

  return diff.map(item => {
    switch (item.type) {
      case DiffType.ADD:
        return `${GREEN}+${item.value}${RESET}`;
      case DiffType.DELETE:
        return `${RED}-${item.value}${RESET}`;
      default:
        return ` ${item.value}`;
    }
  }).join('\n');
}

/**
 * 统计差异信息
 * @param {Array<{type: string, value: string}>} diff - 差异结果
 * @returns {Object} 统计信息
 */
function diffStats(diff) {
  const stats = {
    added: 0,
    deleted: 0,
    equal: 0,
    addedLines: 0,
    deletedLines: 0,
    addedChars: 0,
    deletedChars: 0
  };

  for (const item of diff) {
    switch (item.type) {
      case DiffType.ADD:
        stats.added++;
        stats.addedLines++;
        stats.addedChars += item.value.length;
        break;
      case DiffType.DELETE:
        stats.deleted++;
        stats.deletedLines++;
        stats.deletedChars += item.value.length;
        break;
      default:
        stats.equal++;
    }
  }

  return stats;
}

/**
 * 将差异应用到原始文本
 * @param {string} text - 原始文本
 * @param {Array<{type: string, value: string}>} diff - 差异结果
 * @returns {string} 应用差异后的文本
 */
function applyDiff(text, diff) {
  const result = [];
  for (const item of diff) {
    if (item.type === DiffType.EQUAL || item.type === DiffType.ADD) {
      result.push(item.value);
    }
  }
  return result.join('\n');
}

/**
 * 反转差异（用于回滚）
 * @param {Array<{type: string, value: string}>} diff - 差异结果
 * @returns {Array<{type: string, value: string}>} 反转后的差异
 */
function reverseDiff(diff) {
  return diff.map(item => {
    if (item.type === DiffType.ADD) {
      return { type: DiffType.DELETE, value: item.value };
    } else if (item.type === DiffType.DELETE) {
      return { type: DiffType.ADD, value: item.value };
    }
    return item;
  });
}

/**
 * 计算两个文本的相似度（0-1）
 * @param {string} text1 - 第一个文本
 * @param {string} text2 - 第二个文本
 * @returns {number} 相似度
 */
function similarity(text1, text2) {
  if (text1 === text2) return 1;
  if (text1.length === 0 || text2.length === 0) return 0;

  const chars1 = text1.split('');
  const chars2 = text2.split('');
  const dp = computeLCSMatrix(chars1, chars2);
  const lcsLength = dp[chars1.length][chars2.length];
  const maxLength = Math.max(chars1.length, chars2.length);

  return lcsLength / maxLength;
}

/**
 * 找出最长公共子序列文本
 * @param {string} text1 - 第一个文本
 * @param {string} text2 - 第二个文本
 * @returns {string} LCS 文本
 */
function longestCommonSubsequence(text1, text2) {
  const chars1 = text1.split('');
  const chars2 = text2.split('');
  const dp = computeLCSMatrix(chars1, chars2);

  // 回溯获取 LCS
  const result = [];
  let i = chars1.length;
  let j = chars2.length;

  while (i > 0 && j > 0) {
    if (chars1[i - 1] === chars2[j - 1]) {
      result.unshift(chars1[i - 1]);
      i--;
      j--;
    } else if (dp[i - 1][j] > dp[i][j - 1]) {
      i--;
    } else {
      j--;
    }
  }

  return result.join('');
}

/**
 * 找出最长公共子串（连续）
 * @param {string} text1 - 第一个文本
 * @param {string} text2 - 第二个文本
 * @returns {string} 最长公共子串
 */
function longestCommonSubstring(text1, text2) {
  if (text1.length === 0 || text2.length === 0) return '';

  const m = text1.length;
  const n = text2.length;
  const dp = Array(m + 1).fill(0).map(() => Array(n + 1).fill(0));
  let maxLength = 0;
  let endIndex = 0;

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (text1[i - 1] === text2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
        if (dp[i][j] > maxLength) {
          maxLength = dp[i][j];
          endIndex = i;
        }
      }
    }
  }

  return text1.slice(endIndex - maxLength, endIndex);
}

/**
 * 生成差异的 HTML 输出
 * @param {Array<{type: string, value: string}>} diff - 差异结果
 * @returns {string} HTML 格式的差异
 */
function diffToHtml(diff) {
  const escapeHtml = (str) => {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  };

  const lines = diff.map(item => {
    const escaped = escapeHtml(item.value);
    switch (item.type) {
      case DiffType.ADD:
        return `<div class="diff-add">+${escaped}</div>`;
      case DiffType.DELETE:
        return `<div class="diff-delete">-${escaped}</div>`;
      default:
        return `<div class="diff-equal"> ${escaped}</div>`;
    }
  });

  return `<div class="diff-container">${lines.join('')}</div>`;
}

/**
 * 解析统一格式 diff
 * @param {string} unifiedDiff - Unified diff 格式字符串
 * @returns {Array<{type: string, value: string}>} 差异结果
 */
function parseUnifiedDiff(unifiedDiff) {
  const lines = unifiedDiff.split('\n');
  const result = [];

  for (const line of lines) {
    if (line.startsWith('@@') || line.startsWith('---') || line.startsWith('+++') || line === '') {
      continue;
    }
    if (line.startsWith('+')) {
      result.push({ type: DiffType.ADD, value: line.slice(1) });
    } else if (line.startsWith('-')) {
      result.push({ type: DiffType.DELETE, value: line.slice(1) });
    } else if (line.startsWith(' ')) {
      result.push({ type: DiffType.EQUAL, value: line.slice(1) });
    }
  }

  return result;
}

/**
 * 三方合并
 * @param {string} base - 基础文本
 * @param {string} ours - 我们的修改
 * @param {string} theirs - 他们的修改
 * @returns {Object} 合并结果
 */
function threeWayMerge(base, ours, theirs) {
  const diffOurs = diffLines(base, ours);
  const diffTheirs = diffLines(base, theirs);

  const conflicts = [];
  const result = [];

  // 简化版三方合并：分别应用两个 diff
  // 真实的三方合并需要更复杂的冲突检测
  let oursChanges = {};
  let theirsChanges = {};

  let lineNum = 0;
  for (const item of diffOurs) {
    if (item.type === DiffType.ADD) {
      oursChanges[lineNum] = { type: 'add', value: item.value };
    } else if (item.type === DiffType.DELETE) {
      oursChanges[lineNum] = { type: 'delete', value: item.value };
    } else {
      lineNum++;
    }
  }

  lineNum = 0;
  for (const item of diffTheirs) {
    if (item.type === DiffType.ADD) {
      theirsChanges[lineNum] = { type: 'add', value: item.value };
    } else if (item.type === DiffType.DELETE) {
      theirsChanges[lineNum] = { type: 'delete', value: item.value };
    } else {
      lineNum++;
    }
  }

  // 检测冲突
  for (const key of Object.keys(oursChanges)) {
    if (theirsChanges[key] && oursChanges[key].value !== theirsChanges[key].value) {
      conflicts.push({
        line: parseInt(key),
        ours: oursChanges[key].value,
        theirs: theirsChanges[key].value
      });
    }
  }

  return {
    success: conflicts.length === 0,
    conflicts,
    diffOurs,
    diffTheirs
  };
}

module.exports = {
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
};