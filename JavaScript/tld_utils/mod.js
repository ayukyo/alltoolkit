/**
 * TLD (Top-Level Domain) Utilities
 * 顶级域名工具模块
 * 
 * 功能：
 * - 从域名/URL提取TLD
 * - 验证TLD有效性
 * - TLD分类（ccTLD国家代码、gTLD通用、sTLD赞助等）
 * - 域名拆分（子域名、二级域名、TLD）
 * - 常用TLD列表查询
 * - IDN国际化域名支持
 * 
 * 零外部依赖，纯JavaScript实现
 */

// 常用 gTLD (Generic Top-Level Domains) 通用顶级域名
const COMMON_GTLD = new Set([
  // 原始 gTLD
  'com', 'org', 'net', 'edu', 'gov', 'mil', 'int', 'arpa',
  // 2000年后新增
  'info', 'biz', 'name', 'pro', 'aero', 'coop', 'museum',
  // 2012年后大量新增
  'app', 'blog', 'cloud', 'dev', 'email', 'game', 'health',
  'live', 'news', 'online', 'shop', 'site', 'store', 'tech',
  'video', 'world', 'xyz', 'club', 'io', 'co', 'ai', 'tv',
  'me', 'cc', 'ly', 'im', 'sh', 'fm', 'am', 'ws', 'us', 'uk',
  'cloud', 'dev', 'page', 'google', 'youtube', 'apple', 'amazon',
]);

// 常用 ccTLD (Country Code Top-Level Domains) 国家代码顶级域名
const COMMON_CCTLD = new Set([
  'cn', 'jp', 'kr', 'tw', 'hk', 'sg', 'my', 'th', 'vn', 'id', 'ph',
  'in', 'pk', 'bd', 'ir', 'sa', 'ae', 'il', 'tr', 'ru', 'ua', 'pl',
  'de', 'fr', 'uk', 'it', 'es', 'nl', 'be', 'ch', 'at', 'se', 'no',
  'dk', 'fi', 'pt', 'gr', 'cz', 'ro', 'hu', 'bg', 'sk', 'hr', 'rs',
  'us', 'ca', 'mx', 'br', 'ar', 'cl', 'co', 'pe', 've', 'ec',
  'au', 'nz', 'za', 'eg', 'ng', 'ke', 'ma', 'ng',
]);

// 赞助 TLD (sponsored TLD)
const SPONSORED_TLD = new Set([
  'aero', 'asia', 'cat', 'coop', 'edu', 'gov', 'int', 'jobs', 
  'mil', 'museum', 'post', 'tel', 'travel', 'xxx',
]);

// 基础设施 TLD
const INFRASTRUCTURE_TLD = new Set([
  'arpa', 'root',
]);

// 保留/测试用 TLD
const RESERVED_TLD = new Set([
  'example', 'invalid', 'localhost', 'test', 'onion',
]);

// 常见的多级 TLD (如 .co.uk, .com.cn 等)
const MULTI_LEVEL_TLD = [
  'co.uk', 'com.uk', 'org.uk', 'net.uk', 'me.uk', 'ltd.uk', 'plc.uk',
  'com.cn', 'net.cn', 'org.cn', 'edu.cn', 'gov.cn', 'ac.cn',
  'co.jp', 'ne.jp', 'or.jp', 'ac.jp', 'go.jp', 'ad.jp', 'gr.jp',
  'co.kr', 'ne.kr', 'or.kr', 'ac.kr', 'go.kr', 're.kr', 'pe.kr',
  'com.au', 'net.au', 'org.au', 'edu.au', 'gov.au',
  'co.nz', 'net.nz', 'org.nz', 'edu.nz', 'gov.nz', 'ac.nz',
  'com.br', 'net.br', 'org.br', 'edu.br', 'gov.br',
  'com.hk', 'net.hk', 'org.hk', 'edu.hk', 'gov.hk',
  'com.tw', 'net.tw', 'org.tw', 'edu.tw', 'gov.tw',
  'com.sg', 'net.sg', 'org.sg', 'edu.sg', 'gov.sg',
  'ac.uk', 'gov.uk', 'nhs.uk', 'police.uk', 'mod.uk',
  'edu.au', 'csiro.au', 'asn.au', 'id.au',
];

// 构建 TLD 查找树
function buildTldTree(tldList) {
  const tree = {};
  for (const tld of tldList) {
    const parts = tld.split('.').reverse();
    let current = tree;
    for (const part of parts) {
      if (!current[part]) {
        current[part] = {};
      }
      current = current[part];
    }
    current.$ = true; // 标记结束
  }
  return tree;
}

const multiLevelTldTree = buildTldTree(MULTI_LEVEL_TLD);

/**
 * TLD 类型枚举
 */
const TLDType = {
  GTLD: 'gTLD',           // 通用顶级域名
  CCTLD: 'ccTLD',         // 国家代码顶级域名
  STLD: 'sTLD',           // 赞助顶级域名
  INFRASTRUCTURE: 'infrastructure', // 基础设施 TLD
  RESERVED: 'reserved',   // 保留/测试用
  NEW_GTLD: 'new gTLD',   // 新通用顶级域名
  UNKNOWN: 'unknown',     // 未知类型
};

/**
 * 从域名或URL提取TLD
 * @param {string} input - 域名或URL
 * @returns {string|null} TLD (不含点号) 或 null
 */
function extractTld(input) {
  const domain = extractDomain(input);
  if (!domain) return null;
  
  const parts = domain.toLowerCase().split('.');
  if (parts.length < 2) return null;
  
  // 检查是否为多级TLD
  const twoLevelTld = parts.slice(-2).join('.');
  if (isMultiLevelTld(twoLevelTld)) {
    return twoLevelTld;
  }
  
  return parts[parts.length - 1];
}

/**
 * 从URL或域名提取完整域名
 * @param {string} input - URL或域名
 * @returns {string|null} 域名
 */
function extractDomain(input) {
  if (!input || typeof input !== 'string') return null;
  
  let str = input.trim();
  
  // 移除协议
  str = str.replace(/^[a-z][a-z0-9+.-]*:\/\//i, '');
  
  // 先移除用户认证信息（在 split 之前处理）
  if (str.includes('@')) {
    str = str.split('@').pop();
  }
  
  // 移除端口和路径
  str = str.split(/[\/:\?#]/)[0];
  
  // 转小写（IDN字符会被保留）
  str = str.toLowerCase();
  
  // 验证域名格式
  if (!isValidDomain(str)) {
    return null;
  }
  
  return str;
}

/**
 * 验证域名格式是否有效
 * @param {string} domain - 域名
 * @returns {boolean}
 */
function isValidDomain(domain) {
  if (!domain || typeof domain !== 'string') return false;
  
  // 基本长度检查
  if (domain.length > 253) return false;
  if (domain.length < 2) return false;
  
  // 检查是否为 IDN（国际化域名）
  const isIdnDomain = /[^\x00-\x7F]/.test(domain);
  
  // 检查每个标签
  const labels = domain.split('.');
  
  // 域名必须至少有两个标签（域名和TLD）
  if (labels.length < 2) return false;
  
  for (const label of labels) {
    if (!label || label.length > 63) return false;
    
    // 标签不能以连字符开始或结束
    if (label.startsWith('-') || label.endsWith('-')) return false;
    
    // 检查标签格式
    // 允许普通 ASCII、punycode（xn--）和 IDN 字符
    if (isIdnDomain) {
      // IDN 域名：允许 Unicode 字符、数字、连字符
      if (!/^[\w\u0080-\uFFFF]([\w\u0080-\uFFFF-]*[\w\u0080-\uFFFF])?$/u.test(label) &&
          !/^xn--[a-z0-9-]+$/i.test(label)) {
        return false;
      }
    } else {
      // 普通 ASCII 域名或 punycode
      if (!/^[a-z0-9]([a-z0-9-]*[a-z0-9])?$/i.test(label) &&
          !/^xn--[a-z0-9-]+$/i.test(label)) {
        return false;
      }
    }
  }
  
  return true;
}

/**
 * 验证TLD是否有效（在已知列表中）
 * @param {string} tld - TLD
 * @returns {boolean}
 */
function isValidTld(tld) {
  if (!tld || typeof tld !== 'string') return false;
  
  const normalized = tld.toLowerCase().trim();
  
  // 检查是否在已知TLD集合中
  if (COMMON_GTLD.has(normalized)) return true;
  if (COMMON_CCTLD.has(normalized)) return true;
  if (SPONSORED_TLD.has(normalized)) return true;
  if (INFRASTRUCTURE_TLD.has(normalized)) return true;
  if (RESERVED_TLD.has(normalized)) return true;
  
  // 检查多级TLD
  if (isMultiLevelTld(normalized)) return true;
  
  // 基本格式检查（允许未知的TLD）
  return /^[a-z]{2,}$/i.test(normalized) || /^xn--[a-z0-9-]+$/i.test(normalized);
}

/**
 * 判断是否为多级TLD
 * @param {string} tld - TLD
 * @returns {boolean}
 */
function isMultiLevelTld(tld) {
  const parts = tld.toLowerCase().split('.').reverse();
  let current = multiLevelTldTree;
  
  for (const part of parts) {
    if (!current[part]) return false;
    current = current[part];
  }
  
  return current.$ === true;
}

/**
 * 获取TLD类型
 * @param {string} tld - TLD
 * @returns {string} TLD类型
 */
function getTldType(tld) {
  if (!tld || typeof tld !== 'string') return TLDType.UNKNOWN;
  
  const normalized = tld.toLowerCase().trim();
  
  if (SPONSORED_TLD.has(normalized)) return TLDType.STLD;
  if (INFRASTRUCTURE_TLD.has(normalized)) return TLDType.INFRASTRUCTURE;
  if (RESERVED_TLD.has(normalized)) return TLDType.RESERVED;
  if (COMMON_CCTLD.has(normalized)) return TLDType.CCTLD;
  if (COMMON_GTLD.has(normalized)) return TLDType.GTLD;
  
  // 检查是否为有效的国家代码
  if (/^[a-z]{2}$/i.test(normalized)) {
    return TLDType.CCTLD;
  }
  
  // 检查是否为新的 gTLD
  if (/^[a-z]{3,}$/i.test(normalized)) {
    return TLDType.NEW_GTLD;
  }
  
  return TLDType.UNKNOWN;
}

/**
 * 获取TLD的详细类型描述
 * @param {string} tld - TLD
 * @returns {object} TLD详情
 */
function getTldInfo(tld) {
  if (!tld || typeof tld !== 'string') {
    return null;
  }
  
  const normalized = tld.toLowerCase().trim();
  const type = getTldType(normalized);
  
  const info = {
    tld: normalized,
    type: type,
    isValid: isValidTld(normalized),
    isMultiLevel: isMultiLevelTld(normalized),
    isReserved: RESERVED_TLD.has(normalized),
    isCountryCode: type === TLDType.CCTLD,
    isGeneric: type === TLDType.GTLD || type === TLDType.NEW_GTLD,
    isSponsored: type === TLDType.STLD,
  };
  
  // 添加国家代码信息
  if (info.isCountryCode) {
    info.countryCode = normalized.toUpperCase();
    info.countryName = getCountryName(normalized);
  }
  
  return info;
}

/**
 * 获取国家名称
 * @param {string} ccTLD - 国家代码TLD
 * @returns {string|null} 国家名称
 */
function getCountryName(ccTLD) {
  const countries = {
    'cn': '中国', 'jp': '日本', 'kr': '韩国', 'tw': '台湾', 'hk': '香港',
    'sg': '新加坡', 'my': '马来西亚', 'th': '泰国', 'vn': '越南', 'id': '印度尼西亚',
    'ph': '菲律宾', 'in': '印度', 'pk': '巴基斯坦', 'bd': '孟加拉国', 'ir': '伊朗',
    'sa': '沙特阿拉伯', 'ae': '阿联酋', 'il': '以色列', 'tr': '土耳其',
    'ru': '俄罗斯', 'ua': '乌克兰', 'pl': '波兰', 'de': '德国', 'fr': '法国',
    'uk': '英国', 'it': '意大利', 'es': '西班牙', 'nl': '荷兰', 'be': '比利时',
    'ch': '瑞士', 'at': '奥地利', 'se': '瑞典', 'no': '挪威', 'dk': '丹麦',
    'fi': '芬兰', 'pt': '葡萄牙', 'gr': '希腊', 'cz': '捷克', 'ro': '罗马尼亚',
    'hu': '匈牙利', 'bg': '保加利亚', 'sk': '斯洛伐克', 'hr': '克罗地亚',
    'rs': '塞尔维亚', 'us': '美国', 'ca': '加拿大', 'mx': '墨西哥',
    'br': '巴西', 'ar': '阿根廷', 'cl': '智利', 'co': '哥伦比亚',
    'pe': '秘鲁', 've': '委内瑞拉', 'ec': '厄瓜多尔', 'au': '澳大利亚',
    'nz': '新西兰', 'za': '南非', 'eg': '埃及', 'ng': '尼日利亚',
    'ke': '肯尼亚', 'ma': '摩洛哥',
  };
  return countries[ccTLD.toLowerCase()] || null;
}

/**
 * 拆分域名为子域名、二级域名和TLD
 * @param {string} input - URL或域名
 * @returns {object|null} { subdomain, domain, tld, fullDomain }
 */
function parseDomain(input) {
  const fullDomain = extractDomain(input);
  if (!fullDomain) return null;
  
  const parts = fullDomain.split('.');
  
  // 检查多级TLD
  let tld = null;
  let tldParts = 1;
  
  if (parts.length >= 2) {
    const twoLevelTld = parts.slice(-2).join('.');
    if (isMultiLevelTld(twoLevelTld)) {
      tld = twoLevelTld;
      tldParts = 2;
    }
  }
  
  if (!tld) {
    tld = parts[parts.length - 1];
    tldParts = 1;
  }
  
  // 提取剩余部分
  const remaining = parts.slice(0, parts.length - tldParts);
  
  if (remaining.length === 0) {
    return {
      subdomain: null,
      domain: null,
      tld: tld,
      fullDomain: fullDomain,
    };
  }
  
  const domain = remaining.pop();
  const subdomain = remaining.length > 0 ? remaining.join('.') : null;
  
  return {
    subdomain: subdomain,
    domain: domain,
    tld: tld,
    fullDomain: fullDomain,
  };
}

/**
 * 获取域名主体（不含子域名和TLD）
 * @param {string} input - URL或域名
 * @returns {string|null}
 */
function getDomainName(input) {
  const parsed = parseDomain(input);
  return parsed ? parsed.domain : null;
}

/**
 * 获取完整域名（不含路径）
 * @param {string} input - URL或域名
 * @returns {string|null}
 */
function getFullDomain(input) {
  return extractDomain(input);
}

/**
 * 获取子域名
 * @param {string} input - URL或域名
 * @returns {string|null}
 */
function getSubdomain(input) {
  const parsed = parseDomain(input);
  return parsed ? parsed.subdomain : null;
}

/**
 * 获取所有已知gTLD列表
 * @returns {string[]}
 */
function getAllGtld() {
  return [...COMMON_GTLD].sort();
}

/**
 * 获取所有已知ccTLD列表
 * @returns {string[]}
 */
function getAllCctld() {
  return [...COMMON_CCTLD].sort();
}

/**
 * 获取所有赞助TLD列表
 * @returns {string[]}
 */
function getAllSponsoredTld() {
  return [...SPONSORED_TLD].sort();
}

/**
 * 获取所有保留TLD列表
 * @returns {string[]}
 */
function getAllReservedTld() {
  return [...RESERVED_TLD].sort();
}

/**
 * 获取所有多级TLD列表
 * @returns {string[]}
 */
function getAllMultiLevelTld() {
  return [...MULTI_LEVEL_TLD].sort();
}

/**
 * 搜索匹配的TLD
 * @param {string} query - 搜索关键词
 * @param {object} options - 搜索选项
 * @returns {string[]}
 */
function searchTld(query, options = {}) {
  const {
    type = null,  // 筛选类型：'gTLD', 'ccTLD', 'sTLD', 'reserved'
    limit = 20,
  } = options;
  
  const normalizedQuery = query.toLowerCase().trim();
  let results = [];
  
  // 根据类型选择搜索集合
  if (!type || type === 'gTLD') {
    results.push(...COMMON_GTLD);
  }
  if (!type || type === 'ccTLD') {
    results.push(...COMMON_CCTLD);
  }
  if (!type || type === 'sTLD') {
    results.push(...SPONSORED_TLD);
  }
  if (!type || type === 'reserved') {
    results.push(...RESERVED_TLD);
  }
  
  // 过滤匹配项
  results = results.filter(tld => tld.includes(normalizedQuery));
  
  // 去重、排序、限制
  return [...new Set(results)]
    .sort()
    .slice(0, Math.max(1, limit));
}

/**
 * 判断两个域名是否为同一主域名
 * @param {string} domain1 - 第一个域名
 * @param {string} domain2 - 第二个域名
 * @returns {boolean}
 */
function isSameDomain(domain1, domain2) {
  const name1 = getDomainName(domain1);
  const tld1 = extractTld(domain1);
  const name2 = getDomainName(domain2);
  const tld2 = extractTld(domain2);
  
  return name1 && name2 && tld1 && tld2 &&
         name1.toLowerCase() === name2.toLowerCase() &&
         tld1.toLowerCase() === tld2.toLowerCase();
}

/**
 * 规范化域名（转小写，移除www前缀）
 * @param {string} input - URL或域名
 * @returns {string|null}
 */
function normalizeDomain(input) {
  const domain = extractDomain(input);
  if (!domain) return null;
  
  // 移除 www. 前缀
  if (domain.startsWith('www.')) {
    return domain.slice(4);
  }
  
  return domain;
}

/**
 * 检查域名是否为IDN（国际化域名）
 * @param {string} input - URL或域名
 * @returns {boolean}
 */
function isIdn(input) {
  const domain = extractDomain(input);
  if (!domain) return false;
  
  // 检查是否包含非ASCII字符或punycode
  return /[^\x00-\x7F]/.test(domain) || /xn--/i.test(domain);
}

/**
 * 检查域名是否为punycode格式
 * @param {string} input - URL或域名
 * @returns {boolean}
 */
function isPunycode(input) {
  const domain = extractDomain(input);
  if (!domain) return false;
  
  return /xn--/i.test(domain);
}

/**
 * 判断TLD是否常用于科技/创业公司
 * @param {string} tld - TLD
 * @returns {boolean}
 */
function isTechTld(tld) {
  const techTlds = new Set([
    'io', 'ai', 'dev', 'app', 'tech', 'cloud', 'code', 'dev', 'git', 'tech',
    'co', 'ly', 'fm', 'am', 'tv', 'me',
  ]);
  return techTlds.has(tld.toLowerCase());
}

// 导出
module.exports = {
  // 常量
  TLDType,
  COMMON_GTLD,
  COMMON_CCTLD,
  SPONSORED_TLD,
  RESERVED_TLD,
  MULTI_LEVEL_TLD,
  
  // 主要函数
  extractTld,
  extractDomain,
  parseDomain,
  
  // 验证函数
  isValidDomain,
  isValidTld,
  isMultiLevelTld,
  isIdn,
  isPunycode,
  
  // 类型判断
  getTldType,
  getTldInfo,
  
  // 域名操作
  getDomainName,
  getFullDomain,
  getSubdomain,
  normalizeDomain,
  isSameDomain,
  
  // 查询函数
  getAllGtld,
  getAllCctld,
  getAllSponsoredTld,
  getAllReservedTld,
  getAllMultiLevelTld,
  searchTld,
  
  // 辅助函数
  getCountryName,
  isTechTld,
};