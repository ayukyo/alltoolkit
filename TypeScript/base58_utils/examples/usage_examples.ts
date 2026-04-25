/**
 * Base58 工具模块使用示例
 * 
 * Base58 是一种二进制到文本的编码方案，广泛用于：
 * - Bitcoin 地址
 * - IPFS 内容标识符
 * - URL 短链接
 * - 其他需要避免混淆字符的场景
 */

import {
    Base58Encoder,
    base58,
    base58Flickr,
    base58Ripple,
    encodeBase58,
    decodeBase58,
    encodeBase58String,
    decodeBase58String,
    encodeBase58Hex,
    decodeBase58ToHex,
    isValidBase58,
    randomBase58,
    bigIntToBase58,
    base58ToBigInt,
    encodeWithChecksum,
    decodeWithChecksum,
} from '../mod';

console.log('=== Base58 工具模块使用示例 ===\n');

// ========================================
// 1. 基础编码解码
// ========================================
console.log('【1. 基础编码解码】');

const data = new TextEncoder().encode('Hello, Base58!');
const encoded = encodeBase58(data);
const decoded = decodeBase58(encoded);

console.log(`原始数据: "${new TextDecoder().decode(data)}"`);
console.log(`Base58 编码: ${encoded}`);
console.log(`解码还原: "${new TextDecoder().decode(decoded)}"`);
console.log();

// ========================================
// 2. 字符串快捷编解码
// ========================================
console.log('【2. 字符串快捷编解码】');

const message = '这是一条测试消息 🚀';
const encodedStr = encodeBase58String(message);
const decodedStr = decodeBase58String(encodedStr);

console.log(`原始消息: ${message}`);
console.log(`Base58 编码: ${encodedStr}`);
console.log(`解码还原: ${decodedStr}`);
console.log();

// ========================================
// 3. 十六进制编解码
// ========================================
console.log('【3. 十六进制编解码】');

const hexData = 'deadbeef';
const encodedHex = encodeBase58Hex(hexData);
const decodedHex = decodeBase58ToHex(encodedHex);

console.log(`原始十六进制: ${hexData}`);
console.log(`Base58 编码: ${encodedHex}`);
console.log(`解码还原: ${decodedHex}`);
console.log();

// ========================================
// 4. 生成随机 Base58 字符串
// ========================================
console.log('【4. 生成随机 Base58 字符串】');

const randomId1 = randomBase58(8);
const randomId2 = randomBase58(16);
const randomId3 = randomBase58(32);

console.log(`8 字符 ID: ${randomId1}`);
console.log(`16 字符 ID: ${randomId2}`);
console.log(`32 字符 ID: ${randomId3}`);
console.log();

// ========================================
// 5. BigInt 转换
// ========================================
console.log('【5. BigInt 转换】');

const bigNumber = 123456789012345678901234567890n;
const encodedBigInt = bigIntToBase58(bigNumber);
const decodedBigInt = base58ToBigInt(encodedBigInt);

console.log(`原始 BigInt: ${bigNumber}`);
console.log(`Base58 编码: ${encodedBigInt}`);
console.log(`解码还原: ${decodedBigInt}`);
console.log();

// ========================================
// 6. 带校验和的编解码
// ========================================
console.log('【6. 带校验和的编解码】');

const importantData = new TextEncoder().encode('重要数据');
const encodedWithChecksum = encodeWithChecksum(importantData);
const decodedWithChecksum = decodeWithChecksum(encodedWithChecksum);

console.log(`原始数据: "${new TextDecoder().decode(importantData)}"`);
console.log(`带校验和编码: ${encodedWithChecksum}`);
if (decodedWithChecksum) {
    console.log(`解码成功: "${new TextDecoder().decode(decodedWithChecksum)}"`);
}

// 演示校验失败的情况
const tampered = encodedWithChecksum.slice(0, -2) + 'xx';
const tamperedResult = decodeWithChecksum(tampered);
console.log(`篡改后的解码结果: ${tamperedResult === null ? '校验失败' : '校验通过'}`);
console.log();

// ========================================
// 7. 验证 Base58 字符串
// ========================================
console.log('【7. 验证 Base58 字符串】');

const validBase58 = '2gBuM5PmDqF3QkLwA';
const invalidBase58 = '2gBuM5Pm0qF3QkLwA'; // 包含 '0' 和 'O'

console.log(`"${validBase58}" 是否有效: ${isValidBase58(validBase58)}`);
console.log(`"${invalidBase58}" 是否有效: ${isValidBase58(invalidBase58)}`);
console.log();

// ========================================
// 8. 使用不同字母表
// ========================================
console.log('【8. 使用不同字母表】');

const sampleBytes = new Uint8Array([0xde, 0xad, 0xbe, 0xef]);

console.log('相同数据使用不同字母表编码:');
console.log(`Bitcoin 字母表: ${base58.encode(sampleBytes)}`);
console.log(`Flickr 字母表: ${base58Flickr.encode(sampleBytes)}`);
console.log(`Ripple 字母表: ${base58Ripple.encode(sampleBytes)}`);
console.log();

// ========================================
// 9. 自定义字母表
// ========================================
console.log('【9. 自定义字母表】');

const customAlphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz123456789';
const customEncoder = new Base58Encoder(customAlphabet);
const customEncoded = customEncoder.encode(sampleBytes);

console.log(`自定义字母表编码: ${customEncoded}`);
console.log(`自定义字母表解码: ${bytesToHex(customEncoder.decode(customEncoded))}`);
console.log();

// ========================================
// 10. 实际应用场景
// ========================================
console.log('【10. 实际应用场景】');

// 10.1 生成短链接 ID
console.log('场景 1: 生成短链接 ID');
const shortLinkId = randomBase58(6);
console.log(`短链接 ID: https://example.com/s/${shortLinkId}`);

// 10.2 生成唯一订单号
console.log('\n场景 2: 生成唯一订单号');
const timestamp = Date.now();
const orderIdBase = BigInt(timestamp) * 1000n + BigInt(Math.floor(Math.random() * 1000));
const orderId = bigIntToBase58(orderIdBase);
console.log(`订单号: ${orderId}`);

// 10.3 编码 Bitcoin 风格地址
console.log('\n场景 3: 编码 Bitcoin 风格地址');
const publicKeyHash = '0010965e4a3a7c2c3e1d8f7a6b5c4d3e2f1a0b9c8d7';
const versionByte = '00';
const addressPayload = versionByte + publicKeyHash;
const bitcoinAddress = '1' + encodeBase58Hex(addressPayload); // 简化示例
console.log(`公钥哈希: ${publicKeyHash}`);
console.log(`地址 (简化): ${bitcoinAddress.slice(0, 20)}...`);

// 10.4 编码 IPFS CID（简化示例）
console.log('\n场景 4: 编码 IPFS CID');
const cidData = new TextEncoder().encode('QmPZ9gcCEpqKTo6aq61g2nXGUhM/CiZ3hZ9hZ5s');
const cid = encodeBase58(cidData);
console.log(`CID (简化): ${cid.slice(0, 20)}...`);

// 10.5 安全令牌生成
console.log('\n场景 5: 安全令牌生成');
const token = randomBase58(32);
console.log(`API Token: ${token}`);

// 10.6 邀请码生成
console.log('\n场景 6: 邀请码生成');
const inviteCode = randomBase58(8).toUpperCase();
console.log(`邀请码: ${inviteCode}`);

console.log('\n=== 示例完成 ===\n');

// 辅助函数
function bytesToHex(bytes: Uint8Array): string {
    return Array.from(bytes).map(b => b.toString(16).padStart(2, '0')).join('');
}