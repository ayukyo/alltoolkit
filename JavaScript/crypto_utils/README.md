# crypto_utils - JavaScript 加密工具集

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D14.0.0-green.svg)](https://nodejs.org/)

一个零外部依赖的 JavaScript 加密工具库，仅使用 Node.js 内置 `crypto` 模块。

## ✨ 特性

- 🔐 **对称加密**: AES-GCM, AES-CBC, ChaCha20-Poly1305
- 🔑 **非对称加密**: RSA 加密/解密
- ✍️ **数字签名**: ECDSA, Ed25519
- 📝 **哈希函数**: SHA256, SHA512, MD5, RIPEMD160
- 🔏 **HMAC**: 消息认证码
- 🔧 **密钥派生**: PBKDF2, HKDF
- 🔒 **密码哈希**: 安全的密码存储和验证
- 🎲 **随机数生成**: 安全的随机字节、十六进制、Base64、UUID
- ⏱️ **时序安全**: 防止时序攻击的比较函数

## 📦 安装

无需安装任何依赖！只需将 `crypto_utils.js` 文件复制到您的项目中。

```bash
# 克隆或下载后
cp crypto_utils.js your-project/utils/
```

## 🚀 快速开始

```javascript
const {
  sha256,
  aesGcmEncrypt,
  aesGcmDecrypt,
  hashPassword,
  verifyPassword,
  uuidv4,
} = require('./crypto_utils');

// 生成 UUID
const id = uuidv4();
console.log('UUID:', id);

// 计算哈希
const hash = sha256('hello world');
console.log('SHA256:', hash);

// AES-GCM 加密
const key = Buffer.from('0123456789abcdef0123456789abcdef'.slice(0, 32)); // 32 字节密钥
const encrypted = aesGcmEncrypt('敏感数据', key);
console.log('加密结果:', encrypted);

// AES-GCM 解密
const decrypted = aesGcmDecrypt(
  encrypted.ciphertext,
  key,
  encrypted.iv,
  encrypted.authTag
);
console.log('解密结果:', decrypted);

// 密码哈希
const { hash: pwdHash, salt } = await hashPassword('user_password');
const isValid = await verifyPassword('user_password', pwdHash, salt);
console.log('密码验证:', isValid);
```

## 📖 API 文档

### 随机数生成

```javascript
const { randomBytes, randomHex, randomBase64, uuidv4 } = require('./crypto_utils');

// 生成 32 字节随机数
const bytes = randomBytes(32);

// 生成 16 字节的十六进制字符串 (32 个字符)
const hex = randomHex(16);

// 生成 Base64 字符串
const b64 = randomBase64(32);

// 生成 UUID v4
const id = uuidv4();
```

### 哈希函数

```javascript
const { hash, sha256, sha512, md5, hashFile } = require('./crypto_utils');

// 通用哈希
const h1 = hash('data', 'sha256');           // hex 输出
const h2 = hash('data', 'sha512', 'base64'); // base64 输出

// 便捷函数
const h3 = sha256('data');
const h4 = sha512('data');
const h5 = md5('data'); // 仅用于非安全场景

// 文件哈希
const fileHash = await hashFile('/path/to/file', 'sha256');
```

### HMAC

```javascript
const { hmac, hmacSha256 } = require('./crypto_utils');

const mac = hmac('message', 'secret_key', 'sha256');
const mac2 = hmacSha256('message', 'secret_key');
```

### 密钥派生

```javascript
const { pbkdf2, pbkdf2Sync, hkdf } = require('./crypto_utils');

// PBKDF2 (异步)
const key = await pbkdf2('password', 'salt', 100000, 32);

// PBKDF2 (同步)
const key2 = pbkdf2Sync('password', 'salt', 100000, 32);

// HKDF
const derivedKey = hkdf('input_key_material', 'salt', 'context_info', 32);
```

### 对称加密

#### AES-GCM (推荐)

```javascript
const { aesGcmEncrypt, aesGcmDecrypt } = require('./crypto_utils');

const key = Buffer.from('32字节密钥...'); // 32 字节用于 AES-256

// 加密
const encrypted = aesGcmEncrypt('敏感数据', key);
// 返回: { ciphertext, iv, authTag }

// 可选: 使用自定义 IV
const encrypted2 = aesGcmEncrypt('数据', key, customIv);

// 可选: 使用附加认证数据 (AAD)
const encrypted3 = aesGcmEncrypt('数据', key, null, aadBuffer);

// 解密
const decrypted = aesGcmDecrypt(
  encrypted.ciphertext,
  key,
  encrypted.iv,
  encrypted.authTag
);

// 解密时也提供 AAD
const decrypted2 = aesGcmDecrypt(
  encrypted.ciphertext,
  key,
  encrypted.iv,
  encrypted.authTag,
  aadBuffer
);
```

#### AES-CBC

```javascript
const { aesCbcEncrypt, aesCbcDecrypt } = require('./crypto_utils');

const key = Buffer.from('32字节密钥...');

// 加密
const encrypted = aesCbcEncrypt('数据', key);
// 返回: { ciphertext, iv }

// 解密
const decrypted = aesCbcDecrypt(encrypted.ciphertext, key, encrypted.iv);
```

#### ChaCha20-Poly1305

```javascript
const { chaCha20Encrypt, chaCha20Decrypt } = require('./crypto_utils');

const key = Buffer.from('32字节密钥...');

// 加密
const encrypted = chaCha20Encrypt('数据', key);
// 返回: { ciphertext, nonce, authTag }

// 解密
const decrypted = chaCha20Decrypt(
  encrypted.ciphertext,
  key,
  encrypted.nonce,
  encrypted.authTag
);
```

### 非对称加密 (RSA)

```javascript
const { generateRsaKeyPair, rsaEncrypt, rsaDecrypt } = require('./crypto_utils');

// 生成密钥对 (默认 2048 位)
const { publicKey, privateKey } = await generateRsaKeyPair();

// 生成 4096 位密钥对
const keys = await generateRsaKeyPair(4096);

// 加密
const encrypted = rsaEncrypt('敏感数据', publicKey);

// 解密
const decrypted = rsaDecrypt(encrypted, privateKey);
```

### 数字签名

#### Ed25519 (推荐)

```javascript
const { generateEd25519KeyPair, ed25519Sign, ed25519Verify } = require('./crypto_utils');

// 生成密钥对
const { publicKey, privateKey } = await generateEd25519KeyPair();

// 签名
const signature = ed25519Sign('数据', privateKey);

// 验证
const isValid = ed25519Verify('数据', signature, publicKey);
```

#### ECDSA

```javascript
const { generateEcdsaKeyPair, ecdsaSign, ecdsaVerify } = require('./crypto_utils');

// 生成密钥对 (默认 P-256)
const { publicKey, privateKey } = await generateEcdsaKeyPair();

// 使用 P-384 曲线
const keys = await generateEcdsaKeyPair('P-384');

// 签名
const signature = ecdsaSign('数据', privateKey);

// 验证
const isValid = ecdsaVerify('数据', signature, publicKey);
```

### 密码哈希

```javascript
const { hashPassword, verifyPassword } = require('./crypto_utils');

// 哈希密码 (自动生成盐值)
const { hash, salt } = await hashPassword('user_password');

// 使用自定义盐值
const result = await hashPassword('password', 'custom_salt');

// 验证密码
const isValid = await verifyPassword('password', hash, salt);
```

### 时序安全比较

```javascript
const { timingSafeEqual } = require('./crypto_utils');

// 防止时序攻击的字符串比较
const isMatch = timingSafeEqual(userToken, expectedToken);
```

### 高级 API (便捷加密)

```javascript
const { encrypt, decrypt } = require('./crypto_utils');

// 自动生成密钥加密
const encrypted = await encrypt('敏感数据');
console.log('密钥:', encrypted.key); // 保存此密钥！

// 使用自定义密码加密
const encrypted2 = await encrypt('数据', 'mypassword');

// 解密
const decrypted = await decrypt(
  encrypted.ciphertext,
  encrypted.iv,
  encrypted.authTag,
  encrypted.salt,
  encrypted.key // 或 'mypassword'
);
```

## 🧪 运行测试

```bash
node crypto_utils.test.js
```

测试覆盖所有公开 API 和边界情况：

```
========================================
测试结果
========================================
总计: 85 个测试
通过: 85 个
失败: 0 个
覆盖率: 100%
========================================
```

## 🔒 安全建议

1. **密钥管理**: 永远不要硬编码密钥，使用环境变量或安全的密钥管理系统
2. **AES-GCM 推荐**: AES-GCM 比 AES-CBC 更安全，优先使用
3. **密码存储**: 使用 `hashPassword` 函数，它会自动处理盐值
4. **签名算法**: Ed25519 比 ECDSA 更快更安全，优先使用
5. **密钥长度**: RSA 推荐 2048 位以上，AES 推荐 256 位

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**Created by AllToolkit Auto-Generator**