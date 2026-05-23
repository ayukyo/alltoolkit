/**
 * TLD Utils 测试
 */

const assert = require('assert');
const tldUtils = require('./mod.js');

const {
  extractTld,
  extractDomain,
  parseDomain,
  isValidDomain,
  isValidTld,
  isMultiLevelTld,
  getTldType,
  getTldInfo,
  getDomainName,
  getFullDomain,
  getSubdomain,
  normalizeDomain,
  isIdn,
  isPunycode,
  isSameDomain,
  isTechTld,
  searchTld,
  getAllGtld,
  getAllCctld,
  getAllSponsoredTld,
  getAllReservedTld,
  getAllMultiLevelTld,
  TLDType,
} = tldUtils;

console.log('=== TLD Utils 测试开始 ===\n');

let passCount = 0;
let failCount = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passCount++;
  } catch (e) {
    console.log(`❌ ${name}`);
    console.log(`   Error: ${e.message}`);
    failCount++;
  }
}

// ========== extractDomain 测试 ==========
console.log('--- extractDomain 测试 ---');

test('extractDomain: 标准URL', () => {
  assert.strictEqual(extractDomain('https://www.example.com/path'), 'www.example.com');
  assert.strictEqual(extractDomain('https://example.com'), 'example.com');
});

test('extractDomain: 带端口', () => {
  assert.strictEqual(extractDomain('http://example.com:8080'), 'example.com');
  assert.strictEqual(extractDomain('example.com:3000'), 'example.com');
});

test('extractDomain: 带认证信息', () => {
  assert.strictEqual(extractDomain('https://user:pass@example.com'), 'example.com');
});

test('extractDomain: 带子域名', () => {
  assert.strictEqual(extractDomain('blog.example.com'), 'blog.example.com');
  assert.strictEqual(extractDomain('api.v1.example.com'), 'api.v1.example.com');
});

test('extractDomain: 处理无效输入', () => {
  assert.strictEqual(extractDomain(''), null);
  assert.strictEqual(extractDomain(null), null);
  assert.strictEqual(extractDomain(undefined), null);
});

test('extractDomain: 带查询参数', () => {
  assert.strictEqual(extractDomain('example.com/path?query=value'), 'example.com');
  assert.strictEqual(extractDomain('example.com#hash'), 'example.com');
});

// ========== extractTld 测试 ==========
console.log('\n--- extractTld 测试 ---');

test('extractTld: 标准域名', () => {
  assert.strictEqual(extractTld('example.com'), 'com');
  assert.strictEqual(extractTld('example.org'), 'org');
  assert.strictEqual(extractTld('example.net'), 'net');
});

test('extractTld: ccTLD', () => {
  assert.strictEqual(extractTld('example.cn'), 'cn');
  assert.strictEqual(extractTld('example.jp'), 'jp');
  assert.strictEqual(extractTld('example.uk'), 'uk');
});

test('extractTld: 多级TLD', () => {
  assert.strictEqual(extractTld('example.co.uk'), 'co.uk');
  assert.strictEqual(extractTld('example.com.cn'), 'com.cn');
  assert.strictEqual(extractTld('example.co.jp'), 'co.jp');
});

test('extractTld: URL输入', () => {
  assert.strictEqual(extractTld('https://www.example.com'), 'com');
  assert.strictEqual(extractTld('https://blog.example.co.uk'), 'co.uk');
});

// ========== parseDomain 测试 ==========
console.log('\n--- parseDomain 测试 ---');

test('parseDomain: 标准域名', () => {
  const result = parseDomain('www.example.com');
  assert.strictEqual(result.subdomain, 'www');
  assert.strictEqual(result.domain, 'example');
  assert.strictEqual(result.tld, 'com');
});

test('parseDomain: 无子域名', () => {
  const result = parseDomain('example.com');
  assert.strictEqual(result.subdomain, null);
  assert.strictEqual(result.domain, 'example');
  assert.strictEqual(result.tld, 'com');
});

test('parseDomain: 多级子域名', () => {
  const result = parseDomain('api.v1.example.com');
  assert.strictEqual(result.subdomain, 'api.v1');
  assert.strictEqual(result.domain, 'example');
  assert.strictEqual(result.tld, 'com');
});

test('parseDomain: 多级TLD', () => {
  const result = parseDomain('www.example.co.uk');
  assert.strictEqual(result.subdomain, 'www');
  assert.strictEqual(result.domain, 'example');
  assert.strictEqual(result.tld, 'co.uk');
});

test('parseDomain: URL输入', () => {
  const result = parseDomain('https://blog.example.co.jp');
  assert.strictEqual(result.subdomain, 'blog');
  assert.strictEqual(result.domain, 'example');
  assert.strictEqual(result.tld, 'co.jp');
});

// ========== isValidDomain 测试 ==========
console.log('\n--- isValidDomain 测试 ---');

test('isValidDomain: 有效域名', () => {
  assert.strictEqual(isValidDomain('example.com'), true);
  assert.strictEqual(isValidDomain('www.example.com'), true);
  assert.strictEqual(isValidDomain('a.b.c.example.com'), true);
});

test('isValidDomain: 无效域名', () => {
  assert.strictEqual(isValidDomain(''), false);
  assert.strictEqual(isValidDomain('example'), false);
  assert.strictEqual(isValidDomain('-example.com'), false);
  assert.strictEqual(isValidDomain('example-.com'), false);
  assert.strictEqual(isValidDomain('exa mple.com'), false);
});

test('isValidDomain: punycode域名', () => {
  assert.strictEqual(isValidDomain('xn--example.com'), true);
  assert.strictEqual(isValidDomain('example.xn--fiqs8s'), true);
});

// ========== isValidTld 测试 ==========
console.log('\n--- isValidTld 测试 ---');

test('isValidTld: 已知TLD', () => {
  assert.strictEqual(isValidTld('com'), true);
  assert.strictEqual(isValidTld('cn'), true);
  assert.strictEqual(isValidTld('edu'), true);
  assert.strictEqual(isValidTld('example'), true); // reserved
});

test('isValidTld: 多级TLD', () => {
  assert.strictEqual(isValidTld('co.uk'), true);
  assert.strictEqual(isValidTld('com.cn'), true);
});

test('isValidTld: 无效TLD', () => {
  // 基本格式检查通过但不在已知列表
  assert.strictEqual(isValidTld('x'), false); // 太短
  assert.strictEqual(isValidTld(''), false);
  assert.strictEqual(isValidTld(null), false);
});

// ========== getTldType 测试 ==========
console.log('\n--- getTldType 测试 ---');

test('getTldType: gTLD', () => {
  assert.strictEqual(getTldType('com'), TLDType.GTLD);
  assert.strictEqual(getTldType('org'), TLDType.GTLD);
  assert.strictEqual(getTldType('net'), TLDType.GTLD);
});

test('getTldType: ccTLD', () => {
  assert.strictEqual(getTldType('cn'), TLDType.CCTLD);
  assert.strictEqual(getTldType('jp'), TLDType.CCTLD);
  assert.strictEqual(getTldType('uk'), TLDType.CCTLD);
});

test('getTldType: sTLD', () => {
  assert.strictEqual(getTldType('edu'), TLDType.STLD);
  assert.strictEqual(getTldType('gov'), TLDType.STLD);
  assert.strictEqual(getTldType('mil'), TLDType.STLD);
});

test('getTldType: reserved', () => {
  assert.strictEqual(getTldType('example'), TLDType.RESERVED);
  assert.strictEqual(getTldType('localhost'), TLDType.RESERVED);
  assert.strictEqual(getTldType('test'), TLDType.RESERVED);
});

// ========== getTldInfo 测试 ==========
console.log('\n--- getTldInfo 测试 ---');

test('getTldInfo: ccTLD详情', () => {
  const info = getTldInfo('cn');
  assert.strictEqual(info.tld, 'cn');
  assert.strictEqual(info.type, TLDType.CCTLD);
  assert.strictEqual(info.isCountryCode, true);
  assert.strictEqual(info.countryName, '中国');
});

test('getTldInfo: gTLD详情', () => {
  const info = getTldInfo('com');
  assert.strictEqual(info.tld, 'com');
  assert.strictEqual(info.type, TLDType.GTLD);
  assert.strictEqual(info.isGeneric, true);
});

test('getTldInfo: reserved详情', () => {
  const info = getTldInfo('localhost');
  assert.strictEqual(info.isReserved, true);
});

// ========== getDomainName 测试 ==========
console.log('\n--- getDomainName 测试 ---');

test('getDomainName: 提取域名主体', () => {
  assert.strictEqual(getDomainName('www.example.com'), 'example');
  assert.strictEqual(getDomainName('blog.example.co.uk'), 'example');
  assert.strictEqual(getDomainName('example.com'), 'example');
});

// ========== getSubdomain 测试 ==========
console.log('\n--- getSubdomain 测试 ---');

test('getSubdomain: 提取子域名', () => {
  assert.strictEqual(getSubdomain('www.example.com'), 'www');
  assert.strictEqual(getSubdomain('api.v1.example.com'), 'api.v1');
  assert.strictEqual(getSubdomain('example.com'), null);
});

// ========== normalizeDomain 测试 ==========
console.log('\n--- normalizeDomain 测试 ---');

test('normalizeDomain: 移除www前缀', () => {
  assert.strictEqual(normalizeDomain('www.example.com'), 'example.com');
  assert.strictEqual(normalizeDomain('example.com'), 'example.com');
  assert.strictEqual(normalizeDomain('WWW.EXAMPLE.COM'), 'example.com');
});

// ========== isSameDomain 测试 ==========
console.log('\n--- isSameDomain 测试 ---');

test('isSameDomain: 相同域名判断', () => {
  assert.strictEqual(isSameDomain('www.example.com', 'example.com'), true);
  assert.strictEqual(isSameDomain('blog.example.com', 'api.example.com'), true);
  assert.strictEqual(isSameDomain('example.com', 'example.org'), false);
  assert.strictEqual(isSameDomain('example.cn', 'example.com'), false);
});

// ========== isIdn & isPunycode 测试 ==========
console.log('\n--- isIdn & isPunycode 测试 ---');

test('isIdn: 检测国际化域名', () => {
  assert.strictEqual(isIdn('example.com'), false);
  assert.strictEqual(isIdn('例子.com'), true);
  assert.strictEqual(isIdn('xn--example.com'), true);
});

test('isPunycode: 检测punycode格式', () => {
  assert.strictEqual(isPunycode('example.com'), false);
  assert.strictEqual(isPunycode('xn--fiqs8s.com'), true);
  assert.strictEqual(isPunycode('example.xn--fiqs8s'), true);
});

// ========== isTechTld 测试 ==========
console.log('\n--- isTechTld 测试 ---');

test('isTechTld: 科技公司常用TLD', () => {
  assert.strictEqual(isTechTld('io'), true);
  assert.strictEqual(isTechTld('ai'), true);
  assert.strictEqual(isTechTld('dev'), true);
  assert.strictEqual(isTechTld('com'), false);
});

// ========== searchTld 测试 ==========
console.log('\n--- searchTld 测试 ---');

test('searchTld: 搜索TLD', () => {
  const results = searchTld('com');
  assert.ok(results.includes('com'));
  assert.ok(results.length > 0);
});

test('searchTld: 按类型搜索', () => {
  const ccResults = searchTld('a', { type: 'ccTLD', limit: 5 });
  assert.ok(ccResults.length > 0);
  assert.ok(ccResults.length <= 5);
});

// ========== 列表获取函数测试 ==========
console.log('\n--- 列表获取函数测试 ---');

test('getAllGtld: 获取gTLD列表', () => {
  const gtld = getAllGtld();
  assert.ok(Array.isArray(gtld));
  assert.ok(gtld.includes('com'));
  assert.ok(gtld.includes('org'));
});

test('getAllCctld: 获取ccTLD列表', () => {
  const cctld = getAllCctld();
  assert.ok(Array.isArray(cctld));
  assert.ok(cctld.includes('cn'));
  assert.ok(cctld.includes('jp'));
});

test('getAllMultiLevelTld: 获取多级TLD列表', () => {
  const multi = getAllMultiLevelTld();
  assert.ok(Array.isArray(multi));
  assert.ok(multi.includes('co.uk'));
  assert.ok(multi.includes('com.cn'));
});

// ========== 综合测试 ==========
console.log('\n--- 综合测试 ---');

test('综合: 真实域名解析', () => {
  const tests = [
    { input: 'https://www.google.com', tld: 'com', domain: 'google', subdomain: 'www' },
    { input: 'https://github.com', tld: 'com', domain: 'github', subdomain: null },
    { input: 'https://www.bbc.co.uk', tld: 'co.uk', domain: 'bbc', subdomain: 'www' },
    { input: 'https://news.sina.com.cn', tld: 'com.cn', domain: 'sina', subdomain: 'news' },
    { input: 'https://openai.com/blog', tld: 'com', domain: 'openai', subdomain: null },
    { input: 'https://docs.python.org/3/', tld: 'org', domain: 'python', subdomain: 'docs' },
  ];
  
  for (const test of tests) {
    const parsed = parseDomain(test.input);
    assert.strictEqual(parsed.tld, test.tld, `TLD mismatch for ${test.input}`);
    assert.strictEqual(parsed.domain, test.domain, `Domain mismatch for ${test.input}`);
    assert.strictEqual(parsed.subdomain, test.subdomain, `Subdomain mismatch for ${test.input}`);
  }
});

// 输出测试结果
console.log('\n========================================');
console.log(`测试完成: ✅ ${passCount} 通过, ❌ ${failCount} 失败`);
console.log('=== TLD Utils 测试结束 ===');

// 退出码
process.exit(failCount > 0 ? 1 : 0);