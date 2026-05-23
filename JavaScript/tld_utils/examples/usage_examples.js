/**
 * TLD Utils 使用示例
 * 
 * 展示顶级域名工具模块的各种用法
 */

const tldUtils = require('../mod.js');

const {
  extractTld,
  extractDomain,
  parseDomain,
  isValidDomain,
  isValidTld,
  getTldType,
  getTldInfo,
  getDomainName,
  getSubdomain,
  normalizeDomain,
  isSameDomain,
  isIdn,
  isPunycode,
  isTechTld,
  searchTld,
  getAllGtld,
  getAllCctld,
  TLDType,
} = tldUtils;

console.log('╔══════════════════════════════════════════════════════════╗');
console.log('║         TLD Utils - 顶级域名工具模块使用示例              ║');
console.log('╚══════════════════════════════════════════════════════════╝\n');

// ========== 1. 基础提取功能 ==========
console.log('📌 1. 基础提取功能');
console.log('─'.repeat(50));

// 从URL提取域名
const urls = [
  'https://www.example.com/path/to/page',
  'http://user:password@api.example.co.uk:8080/endpoint',
  'blog.github.io',
  'https://news.sina.com.cn/article/123',
];

console.log('\n从URL提取域名:');
urls.forEach(url => {
  console.log(`  ${url}`);
  console.log(`    → 域名: ${extractDomain(url)}`);
  console.log(`    → TLD: ${extractTld(url)}`);
});

// ========== 2. 域名解析 ==========
console.log('\n📌 2. 域名解析');
console.log('─'.repeat(50));

const domainsToParse = [
  'www.google.com',
  'mail.qq.com',
  'api.v1.example.co.uk',
  'openai.com',
  'docs.python.org',
];

console.log('\n解析域名结构:');
domainsToParse.forEach(domain => {
  const parsed = parseDomain(domain);
  console.log(`\n  ${domain}`);
  console.log(`    子域名: ${parsed.subdomain || '(无)'}`);
  console.log(`    主域名: ${parsed.domain}`);
  console.log(`    TLD: ${parsed.tld}`);
});

// ========== 3. TLD类型判断 ==========
console.log('\n📌 3. TLD类型判断');
console.log('─'.repeat(50));

const tlds = ['com', 'cn', 'edu', 'io', 'localhost', 'co.uk'];

console.log('\nTLD类型识别:');
tlds.forEach(tld => {
  const type = getTldType(tld);
  console.log(`  .${tld} → ${type}`);
});

// ========== 4. 获取TLD详细信息 ==========
console.log('\n📌 4. 获取TLD详细信息');
console.log('─'.repeat(50));

const infoTlds = ['com', 'cn', 'io', 'edu', 'test'];

console.log('\nTLD详细信息:');
infoTlds.forEach(tld => {
  const info = getTldInfo(tld);
  console.log(`\n  .${tld}:`);
  console.log(`    类型: ${info.type}`);
  console.log(`    有效: ${info.isValid}`);
  console.log(`    多级: ${info.isMultiLevel}`);
  if (info.countryName) {
    console.log(`    国家: ${info.countryName}`);
  }
  if (info.isReserved) {
    console.log(`    (保留/测试用)`);
  }
});

// ========== 5. 域名验证 ==========
console.log('\n📌 5. 域名验证');
console.log('─'.repeat(50));

const testDomains = [
  'example.com',
  'my-domain.org',
  'sub.domain.example.co.uk',
  '-invalid.com',
  'invalid-.com',
  'xn--fiqs8s.com',  // punycode
  '例子.中国',  // IDN
  'a'.repeat(64) + '.com',  // 标签过长
];

console.log('\n域名有效性验证:');
testDomains.forEach(domain => {
  const valid = isValidDomain(domain);
  console.log(`  ${domain.substring(0, 40).padEnd(40)} → ${valid ? '✅ 有效' : '❌ 无效'}`);
});

// ========== 6. 域名比较 ==========
console.log('\n📌 6. 域名比较');
console.log('─'.repeat(50));

const domainPairs = [
  ['www.example.com', 'example.com'],
  ['blog.example.com', 'shop.example.com'],
  ['example.com', 'example.org'],
  ['api.example.cn', 'www.example.cn'],
];

console.log('\n判断是否为同一主域名:');
domainPairs.forEach(([d1, d2]) => {
  const same = isSameDomain(d1, d2);
  console.log(`  ${d1} vs ${d2} → ${same ? '✅ 相同' : '❌ 不同'}`);
});

// ========== 7. 域名规范化 ==========
console.log('\n📌 7. 域名规范化');
console.log('─'.repeat(50));

const domainsToNormalize = [
  'WWW.EXAMPLE.COM',
  'www.GitHub.com',
  'https://WWW.OPENAI.COM/chat',
];

console.log('\n规范化域名:');
domainsToNormalize.forEach(input => {
  const normalized = normalizeDomain(input);
  console.log(`  ${input} → ${normalized}`);
});

// ========== 8. IDN和Punycode检测 ==========
console.log('\n📌 8. IDN和Punycode检测');
console.log('─'.repeat(50));

const idnTests = [
  'example.com',
  '例子.com',
  'xn--fiqs8s.com',
  'https://日本.jp',
  'www.中国.cn',
];

console.log('\n国际化域名检测:');
idnTests.forEach(test => {
  const isIdnResult = isIdn(test);
  const isPunycodeResult = isPunycode(test);
  console.log(`  ${test}`);
  console.log(`    IDN: ${isIdnResult ? '是' : '否'}, Punycode: ${isPunycodeResult ? '是' : '否'}`);
});

// ========== 9. 科技公司TLD识别 ==========
console.log('\n📌 9. 科技公司常用TLD识别');
console.log('─'.repeat(50));

const techDomains = [
  'github.io',
  'openai.com',
  'cursor.sh',
  'vercel.app',
  'node.dev',
  'python.org',
];

console.log('\n科技公司TLD判断:');
techDomains.forEach(domain => {
  const tld = extractTld(domain);
  const isTech = isTechTld(tld);
  console.log(`  ${domain} → ${isTech ? '🚀 科技相关' : '📡 非科技'}`);
});

// ========== 10. TLD搜索 ==========
console.log('\n📌 10. TLD搜索');
console.log('─'.repeat(50));

console.log('\n搜索包含 "io" 的TLD:');
const ioResults = searchTld('io');
console.log(`  找到: ${ioResults.join(', ')}`);

console.log('\n搜索包含 "com" 的gTLD:');
const comResults = searchTld('com', { type: 'gTLD', limit: 5 });
console.log(`  找到: ${comResults.join(', ')}`);

console.log('\n搜索国家代码TLD (包含"a"):');
const ccResults = searchTld('a', { type: 'ccTLD', limit: 10 });
console.log(`  找到: ${ccResults.join(', ')}`);

// ========== 11. 获取TLD列表 ==========
console.log('\n📌 11. 获取TLD列表');
console.log('─'.repeat(50));

console.log('\n常用gTLD (前10个):');
const gtld = getAllGtld();
console.log(`  ${gtld.slice(0, 10).join(', ')}`);

console.log('\n常用ccTLD (前10个):');
const cctld = getAllCctld();
console.log(`  ${cctld.slice(0, 10).join(', ')}`);

// ========== 12. 实际应用场景 ==========
console.log('\n📌 12. 实际应用场景');
console.log('─'.repeat(50));

// 场景1：批量处理URL
console.log('\n场景1：批量提取域名主体');
const urlsToProcess = [
  'https://www.alibaba.com/products',
  'https://taobao.com/item/123',
  'https://jd.com/category/electronics',
  'https://shop.tmall.com/store',
];

console.log('  提取结果:');
const domainNames = urlsToProcess.map(url => {
  const domain = getDomainName(url);
  return { url, domain };
});
domainNames.forEach(item => {
  console.log(`    ${item.url}`);
  console.log(`    → ${item.domain}`);
});

// 场景2：统计TLD分布
console.log('\n场景2：统计域名TLD分布');
const stats = {};
urlsToProcess.forEach(url => {
  const tld = extractTld(url);
  stats[tld] = (stats[tld] || 0) + 1;
});
console.log('  分布:');
Object.entries(stats).forEach(([tld, count]) => {
  console.log(`    .${tld}: ${count}个`);
});

// 场景3：判断域名归属
console.log('\n场景3：判断域名是否属于同一公司');
const companyDomains = [
  'www.taobao.com',
  'shop.taobao.com',
  'tmall.com',
  'www.alibaba.com',
];

console.log('  淘宝系域名检测:');
const taobaoDomains = companyDomains.filter(domain => 
  isSameDomain(domain, 'taobao.com')
);
console.log(`    淘宝域名: ${taobaoDomains.join(', ') || '无'}`);

console.log('\n✅ 所有示例运行完成！');