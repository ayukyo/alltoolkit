/**
 * 01_basic_usage.js - 基础用法示例
 * 
 * 演示 crypto_utils 的基本功能
 * 
 * 运行: node 01_basic_usage.js
 */

const {
  uuidv4,
  randomHex,
  randomBase64,
  sha256,
  sha512,
  md5,
  hmacSha256,
} = require('./crypto_utils');

console.log('========================================');
console.log('crypto_utils 基础用法示例');
console.log('========================================\n');

// ============================================
// 1. 随机数生成
// ============================================
console.log('--- 随机数生成 ---\n');

const uuid = uuidv4();
console.log('UUID v4:', uuid);

const hex = randomHex(16);
console.log('随机十六进制 (16字节):', hex);

const b64 = randomBase64(24);
console.log('随机 Base64 (24字节):', b64);

// ============================================
// 2. 哈希函数
// ============================================
console.log('\n--- 哈希函数 ---\n');

const data = 'Hello, World!';

console.log('输入数据:', data);
console.log('SHA-256:', sha256(data));
console.log('SHA-512:', sha512(data));
console.log('MD5 (不推荐用于安全场景):', md5(data));

// ============================================
// 3. HMAC
// ============================================
console.log('\n--- HMAC ---\n');

const message = '重要消息';
const secret = 'my-secret-key';

console.log('消息:', message);
console.log('密钥:', secret);
console.log('HMAC-SHA256:', hmacSha256(message, secret));

// ============================================
// 4. 数据指纹
// ============================================
console.log('\n--- 数据指纹 ---\n');

const users = [
  { id: 1, name: 'Alice', email: 'alice@example.com' },
  { id: 2, name: 'Bob', email: 'bob@example.com' },
];

users.forEach(user => {
  const fingerprint = sha256(JSON.stringify(user));
  console.log(`用户 ${user.name} 指纹: ${fingerprint.substring(0, 16)}...`);
});

console.log('\n========================================');
console.log('示例完成！');
console.log('========================================');