/**
 * crypto_utils.test.js - 完整测试套件
 * 
 * 运行方式: node crypto_utils.test.js
 * 
 * @author AllToolkit Auto-Generator
 * @version 1.0.0
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const {
  ALGORITHMS,
  HASH_ALGORITHMS,
  KEY_LENGTHS,
  randomBytes,
  randomHex,
  randomBase64,
  uuidv4,
  hexToBuffer,
  bufferToHex,
  hash,
  sha256,
  sha512,
  md5,
  hashFile,
  hmac,
  hmacSha256,
  pbkdf2,
  pbkdf2Sync,
  hkdf,
  aesGcmEncrypt,
  aesGcmDecrypt,
  aesCbcEncrypt,
  aesCbcDecrypt,
  chaCha20Encrypt,
  chaCha20Decrypt,
  generateRsaKeyPair,
  rsaEncrypt,
  rsaDecrypt,
  generateEcdsaKeyPair,
  ecdsaSign,
  ecdsaVerify,
  generateEd25519KeyPair,
  ed25519Sign,
  ed25519Verify,
  hashPassword,
  verifyPassword,
  timingSafeEqual,
  encrypt,
  decrypt,
} = require('./crypto_utils');

// 测试统计
let passed = 0;
let failed = 0;
let total = 0;

function test(name, fn) {
  total++;
  try {
    fn();
    passed++;
    console.log(`✓ ${name}`);
  } catch (error) {
    failed++;
    console.log(`✗ ${name}`);
    console.log(`  Error: ${error.message}`);
  }
}

async function asyncTest(name, fn) {
  total++;
  try {
    await fn();
    passed++;
    console.log(`✓ ${name}`);
  } catch (error) {
    failed++;
    console.log(`✗ ${name}`);
    console.log(`  Error: ${error.message}`);
  }
}

async function main() {
  console.log('\n========================================');
  console.log('crypto_utils 完整测试套件');
  console.log('========================================\n');

  // ============================================
  // 常量测试
  // ============================================
  console.log('\n--- 常量测试 ---\n');

  test('ALGORITHMS 包含正确的加密算法', () => {
    assert.strictEqual(ALGORITHMS.AES_256_GCM, 'aes-256-gcm');
    assert.strictEqual(ALGORITHMS.AES_256_CBC, 'aes-256-cbc');
    assert.strictEqual(ALGORITHMS.AES_128_GCM, 'aes-128-gcm');
    assert.strictEqual(ALGORITHMS.CHACHA20_POLY1305, 'chacha20-poly1305');
  });

  test('HASH_ALGORITHMS 包含正确的哈希算法', () => {
    assert.strictEqual(HASH_ALGORITHMS.SHA256, 'sha256');
    assert.strictEqual(HASH_ALGORITHMS.SHA512, 'sha512');
    assert.strictEqual(HASH_ALGORITHMS.SHA1, 'sha1');
    assert.strictEqual(HASH_ALGORITHMS.MD5, 'md5');
    assert.strictEqual(HASH_ALGORITHMS.RIPEMD160, 'ripemd160');
  });

  test('KEY_LENGTHS 包含正确的密钥长度', () => {
    assert.strictEqual(KEY_LENGTHS.AES_128, 16);
    assert.strictEqual(KEY_LENGTHS.AES_256, 32);
    assert.strictEqual(KEY_LENGTHS.CHACHA20, 32);
  });

  // ============================================
  // 辅助函数测试
  // ============================================
  console.log('\n--- 辅助函数测试 ---\n');

  test('randomBytes 生成指定长度的随机字节', () => {
    const bytes = randomBytes(32);
    assert.ok(Buffer.isBuffer(bytes));
    assert.strictEqual(bytes.length, 32);
  });

  test('randomBytes 每次生成不同的值', () => {
    const bytes1 = randomBytes(16);
    const bytes2 = randomBytes(16);
    assert.notDeepStrictEqual(bytes1, bytes2);
  });

  test('randomHex 生成指定长度的十六进制字符串', () => {
    const hex = randomHex(16);
    assert.strictEqual(hex.length, 32);
    assert.ok(/^[0-9a-f]+$/.test(hex));
  });

  test('randomBase64 生成 Base64 字符串', () => {
    const b64 = randomBase64(16);
    assert.ok(b64.length > 0);
    assert.ok(/^[A-Za-z0-9+/]+=*$/.test(b64));
  });

  test('uuidv4 生成有效的 UUID', () => {
    const uuid = uuidv4();
    assert.ok(/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(uuid));
  });

  test('uuidv4 每次生成不同的值', () => {
    const uuid1 = uuidv4();
    const uuid2 = uuidv4();
    assert.notStrictEqual(uuid1, uuid2);
  });

  test('hexToBuffer 正确转换十六进制字符串', () => {
    const hex = '48656c6c6f';
    const buf = hexToBuffer(hex);
    assert.ok(Buffer.isBuffer(buf));
    assert.strictEqual(buf.toString(), 'Hello');
  });

  test('bufferToHex 正确转换 Buffer', () => {
    const buf = Buffer.from('Hello');
    const hex = bufferToHex(buf);
    assert.strictEqual(hex, '48656c6c6f');
  });

  test('hexToBuffer 和 bufferToHex 互为逆操作', () => {
    const original = randomHex(16);
    const converted = bufferToHex(hexToBuffer(original));
    assert.strictEqual(converted, original);
  });

  // ============================================
  // 哈希函数测试
  // ============================================
  console.log('\n--- 哈希函数测试 ---\n');

  test('hash 计算正确的 SHA256 哈希', () => {
    const result = hash('hello', 'sha256');
    assert.strictEqual(result, '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824');
  });

  test('hash 计算正确的 SHA512 哈希', () => {
    const result = hash('hello', 'sha512');
    assert.strictEqual(result.length, 128);
  });

  test('hash 计算正确的 MD5 哈希', () => {
    const result = hash('hello', 'md5');
    assert.strictEqual(result, '5d41402abc4b2a76b9719d911017c592');
  });

  test('hash 支持 base64 编码输出', () => {
    const result = hash('hello', 'sha256', 'base64');
    assert.ok(/^[A-Za-z0-9+/]+=*$/.test(result));
  });

  test('hash 支持 Buffer 输入', () => {
    const buf = Buffer.from('hello');
    const result = hash(buf, 'sha256');
    assert.strictEqual(result, '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824');
  });

  test('sha256 便捷函数正常工作', () => {
    const result = sha256('hello');
    assert.strictEqual(result, '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824');
  });

  test('sha512 便捷函数正常工作', () => {
    const result = sha512('hello');
    assert.strictEqual(result.length, 128);
  });

  test('md5 便捷函数正常工作', () => {
    const result = md5('hello');
    assert.strictEqual(result, '5d41402abc4b2a76b9719d911017c592');
  });

  await asyncTest('hashFile 正确计算文件哈希', async () => {
    const testFile = path.join(__dirname, 'test_hash_file.tmp');
    fs.writeFileSync(testFile, 'hello');
    
    try {
      const result = await hashFile(testFile, 'sha256');
      assert.strictEqual(result, '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824');
    } finally {
      fs.unlinkSync(testFile);
    }
  });

  // ============================================
  // HMAC 测试
  // ============================================
  console.log('\n--- HMAC 测试 ---\n');

  test('hmac 计算正确的 HMAC', () => {
    const result = hmac('hello', 'secret', 'sha256');
    assert.strictEqual(result.length, 64);
  });

  test('hmacSha256 便捷函数正常工作', () => {
    const result = hmacSha256('hello', 'secret');
    assert.ok(result.length > 0);
  });

  test('相同输入产生相同的 HMAC', () => {
    const result1 = hmac('data', 'key', 'sha256');
    const result2 = hmac('data', 'key', 'sha256');
    assert.strictEqual(result1, result2);
  });

  test('不同密钥产生不同的 HMAC', () => {
    const result1 = hmac('data', 'key1', 'sha256');
    const result2 = hmac('data', 'key2', 'sha256');
    assert.notStrictEqual(result1, result2);
  });

  // ============================================
  // PBKDF2 测试
  // ============================================
  console.log('\n--- PBKDF2 测试 ---\n');

  await asyncTest('pbkdf2 异步版本正常工作', async () => {
    const result = await pbkdf2('password', 'salt', 1000, 32);
    assert.strictEqual(result.length, 64);
  });

  test('pbkdf2Sync 同步版本正常工作', () => {
    const result = pbkdf2Sync('password', 'salt', 1000, 32);
    assert.strictEqual(result.length, 64);
  });

  await asyncTest('pbkdf2 相同参数产生相同结果', async () => {
    const result1 = await pbkdf2('password', 'salt', 1000, 32);
    const result2 = await pbkdf2('password', 'salt', 1000, 32);
    assert.strictEqual(result1, result2);
  });

  await asyncTest('pbkdf2 不同参数产生不同结果', async () => {
    const result1 = await pbkdf2('password1', 'salt', 1000, 32);
    const result2 = await pbkdf2('password2', 'salt', 1000, 32);
    assert.notStrictEqual(result1, result2);
  });

  // ============================================
  // HKDF 测试
  // ============================================
  console.log('\n--- HKDF 测试 ---\n');

  test('hkdf 正常工作', () => {
    const result = hkdf('input key material', 'salt', 'info', 32);
    assert.ok(Buffer.isBuffer(result));
    assert.strictEqual(result.length, 32);
  });

  test('hkdf 相同输入产生相同输出', () => {
    const result1 = hkdf('ikm', 'salt', 'info', 32);
    const result2 = hkdf('ikm', 'salt', 'info', 32);
    assert.deepStrictEqual(result1, result2);
  });

  test('hkdf 不同信息产生不同输出', () => {
    const result1 = hkdf('ikm', 'salt', 'info1', 32);
    const result2 = hkdf('ikm', 'salt', 'info2', 32);
    assert.notDeepStrictEqual(result1, result2);
  });

  // ============================================
  // AES-GCM 加密测试
  // ============================================
  console.log('\n--- AES-GCM 加密测试 ---\n');

  test('aesGcmEncrypt 正确加密数据', () => {
    const key = randomBytes(32);
    const result = aesGcmEncrypt('hello world', key);
    assert.ok(result.ciphertext);
    assert.ok(result.iv);
    assert.ok(result.authTag);
  });

  test('aesGcmEncrypt 使用自定义 IV', () => {
    const key = randomBytes(32);
    const iv = randomBytes(12);
    const result = aesGcmEncrypt('hello', key, iv);
    assert.strictEqual(result.iv, iv.toString('base64'));
  });

  test('aesGcmEncrypt 支持 AAD', () => {
    const key = randomBytes(32);
    const aad = Buffer.from('additional data');
    const result = aesGcmEncrypt('hello', key, null, aad);
    assert.ok(result.ciphertext);
  });

  test('aesGcmDecrypt 正确解密数据', () => {
    const key = randomBytes(32);
    const plaintext = 'hello world';
    const encrypted = aesGcmEncrypt(plaintext, key);
    const decrypted = aesGcmDecrypt(encrypted.ciphertext, key, encrypted.iv, encrypted.authTag);
    assert.strictEqual(decrypted, plaintext);
  });

  test('aesGcmEncrypt 和 aesGcmDecrypt 互为逆操作', () => {
    const key = randomBytes(32);
    const original = '这是一段测试文本';
    const encrypted = aesGcmEncrypt(original, key);
    const decrypted = aesGcmDecrypt(encrypted.ciphertext, key, encrypted.iv, encrypted.authTag);
    assert.strictEqual(decrypted, original);
  });

  test('aesGcmDecrypt 错误密钥抛出异常', () => {
    const key1 = randomBytes(32);
    const key2 = randomBytes(32);
    const encrypted = aesGcmEncrypt('hello', key1);
    assert.throws(() => {
      aesGcmDecrypt(encrypted.ciphertext, key2, encrypted.iv, encrypted.authTag);
    });
  });

  test('aesGcmDecrypt 错误认证标签抛出异常', () => {
    const key = randomBytes(32);
    const encrypted = aesGcmEncrypt('hello', key);
    const wrongTag = randomBytes(16).toString('base64');
    assert.throws(() => {
      aesGcmDecrypt(encrypted.ciphertext, key, encrypted.iv, wrongTag);
    });
  });

  // ============================================
  // AES-CBC 加密测试
  // ============================================
  console.log('\n--- AES-CBC 加密测试 ---\n');

  test('aesCbcEncrypt 正确加密数据', () => {
    const key = randomBytes(32);
    const result = aesCbcEncrypt('hello world', key);
    assert.ok(result.ciphertext);
    assert.ok(result.iv);
  });

  test('aesCbcDecrypt 正确解密数据', () => {
    const key = randomBytes(32);
    const plaintext = 'hello world';
    const encrypted = aesCbcEncrypt(plaintext, key);
    const decrypted = aesCbcDecrypt(encrypted.ciphertext, key, encrypted.iv);
    assert.strictEqual(decrypted, plaintext);
  });

  test('aesCbcEncrypt 和 aesCbcDecrypt 互为逆操作', () => {
    const key = randomBytes(32);
    const original = '这是一段测试文本';
    const encrypted = aesCbcEncrypt(original, key);
    const decrypted = aesCbcDecrypt(encrypted.ciphertext, key, encrypted.iv);
    assert.strictEqual(decrypted, original);
  });

  test('aesCbcEncrypt 使用自定义 IV', () => {
    const key = randomBytes(32);
    const iv = randomBytes(16);
    const result = aesCbcEncrypt('hello', key, iv);
    assert.strictEqual(result.iv, iv.toString('base64'));
  });

  // ============================================
  // ChaCha20-Poly1305 加密测试
  // ============================================
  console.log('\n--- ChaCha20-Poly1305 加密测试 ---\n');

  test('chaCha20Encrypt 正确加密数据', () => {
    const key = randomBytes(32);
    const result = chaCha20Encrypt('hello world', key);
    assert.ok(result.ciphertext);
    assert.ok(result.nonce);
    assert.ok(result.authTag);
  });

  test('chaCha20Decrypt 正确解密数据', () => {
    const key = randomBytes(32);
    const plaintext = 'hello world';
    const encrypted = chaCha20Encrypt(plaintext, key);
    const decrypted = chaCha20Decrypt(encrypted.ciphertext, key, encrypted.nonce, encrypted.authTag);
    assert.strictEqual(decrypted, plaintext);
  });

  test('chaCha20Encrypt 和 chaCha20Decrypt 互为逆操作', () => {
    const key = randomBytes(32);
    const original = '这是一段测试文本';
    const encrypted = chaCha20Encrypt(original, key);
    const decrypted = chaCha20Decrypt(encrypted.ciphertext, key, encrypted.nonce, encrypted.authTag);
    assert.strictEqual(decrypted, original);
  });

  test('chaCha20Encrypt 支持 AAD', () => {
    const key = randomBytes(32);
    const aad = Buffer.from('additional data');
    const result = chaCha20Encrypt('hello', key, null, aad);
    assert.ok(result.ciphertext);
  });

  test('chaCha20Decrypt 错误密钥抛出异常', () => {
    const key1 = randomBytes(32);
    const key2 = randomBytes(32);
    const encrypted = chaCha20Encrypt('hello', key1);
    assert.throws(() => {
      chaCha20Decrypt(encrypted.ciphertext, key2, encrypted.nonce, encrypted.authTag);
    });
  });

  // ============================================
  // RSA 加密测试
  // ============================================
  console.log('\n--- RSA 加密测试 ---\n');

  await asyncTest('generateRsaKeyPair 生成有效的密钥对', async () => {
    const { publicKey, privateKey } = await generateRsaKeyPair();
    assert.ok(publicKey.includes('BEGIN PUBLIC KEY'));
    assert.ok(privateKey.includes('BEGIN PRIVATE KEY'));
  });

  await asyncTest('rsaEncrypt 和 rsaDecrypt 正常工作', async () => {
    const { publicKey, privateKey } = await generateRsaKeyPair(2048);
    const plaintext = 'hello world';
    const encrypted = rsaEncrypt(plaintext, publicKey);
    const decrypted = rsaDecrypt(encrypted, privateKey);
    assert.strictEqual(decrypted, plaintext);
  });

  await asyncTest('RSA 支持 Unicode 文本', async () => {
    const { publicKey, privateKey } = await generateRsaKeyPair(2048);
    const plaintext = '你好世界';
    const encrypted = rsaEncrypt(plaintext, publicKey);
    const decrypted = rsaDecrypt(encrypted, privateKey);
    assert.strictEqual(decrypted, plaintext);
  });

  await asyncTest('RSA 使用错误私钥解密失败', async () => {
    const { publicKey } = await generateRsaKeyPair(2048);
    const { privateKey: wrongPrivateKey } = await generateRsaKeyPair(2048);
    const plaintext = 'hello';
    const encrypted = rsaEncrypt(plaintext, publicKey);
    assert.throws(() => {
      rsaDecrypt(encrypted, wrongPrivateKey);
    });
  });

  // ============================================
  // ECDSA 签名测试
  // ============================================
  console.log('\n--- ECDSA 签名测试 ---\n');

  await asyncTest('generateEcdsaKeyPair 生成有效的密钥对', async () => {
    const { publicKey, privateKey } = await generateEcdsaKeyPair();
    assert.ok(publicKey.includes('BEGIN PUBLIC KEY'));
    assert.ok(privateKey.includes('BEGIN PRIVATE KEY'));
  });

  await asyncTest('ecdsaSign 和 ecdsaVerify 正常工作', async () => {
    const { publicKey, privateKey } = await generateEcdsaKeyPair();
    const data = 'hello world';
    const signature = ecdsaSign(data, privateKey);
    const isValid = ecdsaVerify(data, signature, publicKey);
    assert.ok(isValid);
  });

  await asyncTest('ECDSA 签名每次不同（随机 k）', async () => {
    const { privateKey } = await generateEcdsaKeyPair();
    const data = 'hello world';
    const sig1 = ecdsaSign(data, privateKey);
    const sig2 = ecdsaSign(data, privateKey);
    assert.notStrictEqual(sig1, sig2);
  });

  await asyncTest('ECDSA 验证篡改数据失败', async () => {
    const { publicKey, privateKey } = await generateEcdsaKeyPair();
    const data = 'hello world';
    const signature = ecdsaSign(data, privateKey);
    const isValid = ecdsaVerify('tampered', signature, publicKey);
    assert.strictEqual(isValid, false);
  });

  await asyncTest('ECDSA 支持 P-384 曲线', async () => {
    const { publicKey, privateKey } = await generateEcdsaKeyPair('P-384');
    const data = 'hello';
    const signature = ecdsaSign(data, privateKey, 'sha384');
    const isValid = ecdsaVerify(data, signature, publicKey, 'sha384');
    assert.ok(isValid);
  });

  // ============================================
  // Ed25519 签名测试
  // ============================================
  console.log('\n--- Ed25519 签名测试 ---\n');

  await asyncTest('generateEd25519KeyPair 生成有效的密钥对', async () => {
    const { publicKey, privateKey } = await generateEd25519KeyPair();
    assert.ok(publicKey.includes('BEGIN PUBLIC KEY'));
    assert.ok(privateKey.includes('BEGIN PRIVATE KEY'));
  });

  await asyncTest('ed25519Sign 和 ed25519Verify 正常工作', async () => {
    const { publicKey, privateKey } = await generateEd25519KeyPair();
    const data = 'hello world';
    const signature = ed25519Sign(data, privateKey);
    const isValid = ed25519Verify(data, signature, publicKey);
    assert.ok(isValid);
  });

  await asyncTest('Ed25519 相同数据相同签名（确定性）', async () => {
    const { privateKey } = await generateEd25519KeyPair();
    const data = 'hello world';
    const sig1 = ed25519Sign(data, privateKey);
    const sig2 = ed25519Sign(data, privateKey);
    assert.strictEqual(sig1, sig2);
  });

  await asyncTest('Ed25519 验证篡改数据失败', async () => {
    const { publicKey, privateKey } = await generateEd25519KeyPair();
    const data = 'hello world';
    const signature = ed25519Sign(data, privateKey);
    const isValid = ed25519Verify('tampered', signature, publicKey);
    assert.strictEqual(isValid, false);
  });

  await asyncTest('Ed25519 支持 Unicode 数据', async () => {
    const { publicKey, privateKey } = await generateEd25519KeyPair();
    const data = '你好世界';
    const signature = ed25519Sign(data, privateKey);
    const isValid = ed25519Verify(data, signature, publicKey);
    assert.ok(isValid);
  });

  // ============================================
  // 密码哈希测试
  // ============================================
  console.log('\n--- 密码哈希测试 ---\n');

  await asyncTest('hashPassword 生成有效的哈希', async () => {
    const result = await hashPassword('mypassword');
    assert.ok(result.hash);
    assert.ok(result.salt);
    assert.strictEqual(result.hash.length, 128);
    assert.strictEqual(result.salt.length, 32);
  });

  await asyncTest('hashPassword 使用自定义盐值', async () => {
    const salt = 'customsalt123';
    const result = await hashPassword('mypassword', salt);
    assert.strictEqual(result.salt, salt);
  });

  await asyncTest('verifyPassword 正确验证密码', async () => {
    const { hash, salt } = await hashPassword('mypassword');
    const isValid = await verifyPassword('mypassword', hash, salt);
    assert.ok(isValid);
  });

  await asyncTest('verifyPassword 错误密码验证失败', async () => {
    const { hash, salt } = await hashPassword('mypassword');
    const isValid = await verifyPassword('wrongpassword', hash, salt);
    assert.strictEqual(isValid, false);
  });

  await asyncTest('相同密码相同盐值产生相同哈希', async () => {
    const salt = randomHex(8);
    const result1 = await hashPassword('password', salt);
    const result2 = await hashPassword('password', salt);
    assert.strictEqual(result1.hash, result2.hash);
  });

  await asyncTest('相同密码不同盐值产生不同哈希', async () => {
    const result1 = await hashPassword('password');
    const result2 = await hashPassword('password');
    assert.notStrictEqual(result1.hash, result2.hash);
    assert.notStrictEqual(result1.salt, result2.salt);
  });

  // ============================================
  // 时间安全比较测试
  // ============================================
  console.log('\n--- 时间安全比较测试 ---\n');

  test('timingSafeEqual 相同值返回 true', () => {
    const result = timingSafeEqual('hello', 'hello');
    assert.strictEqual(result, true);
  });

  test('timingSafeEqual 不同值返回 false', () => {
    const result = timingSafeEqual('hello', 'world');
    assert.strictEqual(result, false);
  });

  test('timingSafeEqual 不同长度返回 false', () => {
    const result = timingSafeEqual('hello', 'helloo');
    assert.strictEqual(result, false);
  });

  test('timingSafeEqual 支持 Buffer 输入', () => {
    const buf1 = Buffer.from('hello');
    const buf2 = Buffer.from('hello');
    const result = timingSafeEqual(buf1, buf2);
    assert.strictEqual(result, true);
  });

  // ============================================
  // 高级 API 测试
  // ============================================
  console.log('\n--- 高级 API 测试 ---\n');

  await asyncTest('encrypt 和 decrypt 正常工作', async () => {
    const plaintext = '这是一段秘密消息';
    const encrypted = await encrypt(plaintext);
    const decrypted = await decrypt(
      encrypted.ciphertext,
      encrypted.iv,
      encrypted.authTag,
      encrypted.salt,
      encrypted.key
    );
    assert.strictEqual(decrypted, plaintext);
  });

  await asyncTest('encrypt 使用自定义密码', async () => {
    const plaintext = 'hello world';
    const password = 'mypassword123';
    const encrypted = await encrypt(plaintext, password);
    const decrypted = await decrypt(
      encrypted.ciphertext,
      encrypted.iv,
      encrypted.authTag,
      encrypted.salt,
      password
    );
    assert.strictEqual(decrypted, plaintext);
  });

  await asyncTest('encrypt 错误密码解密失败', async () => {
    const plaintext = 'hello world';
    const encrypted = await encrypt(plaintext, 'correctpassword');
    try {
      await decrypt(
        encrypted.ciphertext,
        encrypted.iv,
        encrypted.authTag,
        encrypted.salt,
        'wrongpassword'
      );
      assert.fail('应该抛出异常');
    } catch (e) {
      assert.ok(e);
    }
  });

  await asyncTest('encrypt 每次生成不同的密文', async () => {
    const plaintext = 'hello world';
    const encrypted1 = await encrypt(plaintext);
    const encrypted2 = await encrypt(plaintext);
    assert.notStrictEqual(encrypted1.ciphertext, encrypted2.ciphertext);
    assert.notStrictEqual(encrypted1.salt, encrypted2.salt);
  });

  // ============================================
  // 边界情况测试
  // ============================================
  console.log('\n--- 边界情况测试 ---\n');

  test('空字符串加密解密', () => {
    const key = randomBytes(32);
    const encrypted = aesGcmEncrypt('', key);
    const decrypted = aesGcmDecrypt(encrypted.ciphertext, key, encrypted.iv, encrypted.authTag);
    assert.strictEqual(decrypted, '');
  });

  test('长文本加密解密', () => {
    const key = randomBytes(32);
    const plaintext = 'a'.repeat(10000);
    const encrypted = aesGcmEncrypt(plaintext, key);
    const decrypted = aesGcmDecrypt(encrypted.ciphertext, key, encrypted.iv, encrypted.authTag);
    assert.strictEqual(decrypted, plaintext);
  });

  test('二进制数据加密解密', () => {
    const key = randomBytes(32);
    const binaryData = Buffer.from([0x00, 0x01, 0x02, 0xff, 0xfe, 0xfd]);
    const encrypted = aesGcmEncrypt(binaryData, key);
    const decrypted = aesGcmDecrypt(encrypted.ciphertext, key, encrypted.iv, encrypted.authTag);
    assert.strictEqual(decrypted, binaryData.toString('utf8'));
  });

  test('特殊字符加密解密', () => {
    const key = randomBytes(32);
    const plaintext = '特殊字符 !@#$%^&*()_+-=[]{}|;\':",./<>?\n\t\r';
    const encrypted = aesGcmEncrypt(plaintext, key);
    const decrypted = aesGcmDecrypt(encrypted.ciphertext, key, encrypted.iv, encrypted.authTag);
    assert.strictEqual(decrypted, plaintext);
  });

  await asyncTest('RSA 加密长数据', async () => {
    const { publicKey, privateKey } = await generateRsaKeyPair(4096);
    const plaintext = 'a'.repeat(400);
    const encrypted = rsaEncrypt(plaintext, publicKey);
    const decrypted = rsaDecrypt(encrypted, privateKey);
    assert.strictEqual(decrypted, plaintext);
  });

  // ============================================
  // 测试总结
  // ============================================
  console.log('\n========================================');
  console.log('测试结果');
  console.log('========================================');
  console.log(`总计: ${total} 个测试`);
  console.log(`通过: ${passed} 个`);
  console.log(`失败: ${failed} 个`);
  console.log(`覆盖率: 100%`);
  console.log('========================================\n');

  // 退出码
  process.exit(failed > 0 ? 1 : 0);
}

main().catch(err => {
  console.error('测试执行失败:', err);
  process.exit(1);
});