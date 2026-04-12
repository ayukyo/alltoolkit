/**
 * crypto_utils.js - 加密工具集
 * 
 * 提供常用的加密、解密、哈希、签名等功能
 * 零外部依赖，仅使用 Node.js 内置 crypto 模块
 * 
 * @author AllToolkit Auto-Generator
 * @version 1.0.0
 */

const crypto = require('crypto');

// ============================================
// 常量定义
// ============================================

const ALGORITHMS = {
  AES_256_GCM: 'aes-256-gcm',
  AES_256_CBC: 'aes-256-cbc',
  AES_128_GCM: 'aes-128-gcm',
  CHACHA20_POLY1305: 'chacha20-poly1305',
};

const HASH_ALGORITHMS = {
  SHA256: 'sha256',
  SHA512: 'sha512',
  SHA1: 'sha1',
  MD5: 'md5',
  RIPEMD160: 'ripemd160',
};

const KEY_LENGTHS = {
  AES_128: 16,
  AES_256: 32,
  CHACHA20: 32,
};

// ============================================
// 辅助函数
// ============================================

/**
 * 生成随机字节
 * @param {number} length - 字节长度
 * @returns {Buffer} 随机字节
 */
function randomBytes(length) {
  return crypto.randomBytes(length);
}

/**
 * 生成随机十六进制字符串
 * @param {number} length - 字节长度
 * @returns {string} 十六进制字符串
 */
function randomHex(length) {
  return crypto.randomBytes(length).toString('hex');
}

/**
 * 生成随机 Base64 字符串
 * @param {number} length - 字节长度
 * @returns {string} Base64 字符串
 */
function randomBase64(length) {
  return crypto.randomBytes(length).toString('base64');
}

/**
 * 生成 UUID v4
 * @returns {string} UUID 字符串
 */
function uuidv4() {
  return crypto.randomUUID();
}

/**
 * 十六进制字符串转 Buffer
 * @param {string} hex - 十六进制字符串
 * @returns {Buffer} Buffer 对象
 */
function hexToBuffer(hex) {
  return Buffer.from(hex, 'hex');
}

/**
 * Buffer 转十六进制字符串
 * @param {Buffer} buffer - Buffer 对象
 * @returns {string} 十六进制字符串
 */
function bufferToHex(buffer) {
  return buffer.toString('hex');
}

// ============================================
// 哈希函数
// ============================================

/**
 * 计算字符串的哈希值
 * @param {string|Buffer} data - 输入数据
 * @param {string} algorithm - 哈希算法 (sha256, sha512, sha1, md5, ripemd160)
 * @param {string} encoding - 输出编码 (hex, base64, base64url)
 * @returns {string} 哈希值
 */
function hash(data, algorithm = HASH_ALGORITHMS.SHA256, encoding = 'hex') {
  return crypto.createHash(algorithm).update(data).digest(encoding);
}

/**
 * 计算 SHA256 哈希
 * @param {string|Buffer} data - 输入数据
 * @returns {string} 十六进制哈希值
 */
function sha256(data) {
  return hash(data, HASH_ALGORITHMS.SHA256);
}

/**
 * 计算 SHA512 哈希
 * @param {string|Buffer} data - 输入数据
 * @returns {string} 十六进制哈希值
 */
function sha512(data) {
  return hash(data, HASH_ALGORITHMS.SHA512);
}

/**
 * 计算 MD5 哈希（仅用于非安全场景）
 * @param {string|Buffer} data - 输入数据
 * @returns {string} 十六进制哈希值
 */
function md5(data) {
  return hash(data, HASH_ALGORITHMS.MD5);
}

/**
 * 计算文件哈希值
 * @param {string} filePath - 文件路径
 * @param {string} algorithm - 哈希算法
 * @returns {Promise<string>} 哈希值
 */
async function hashFile(filePath, algorithm = HASH_ALGORITHMS.SHA256) {
  const fs = require('fs');
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash(algorithm);
    const stream = fs.createReadStream(filePath);
    stream.on('data', (chunk) => hash.update(chunk));
    stream.on('end', () => resolve(hash.digest('hex')));
    stream.on('error', reject);
  });
}

// ============================================
// HMAC 函数
// ============================================

/**
 * 计算 HMAC
 * @param {string|Buffer} data - 输入数据
 * @param {string|Buffer} key - 密钥
 * @param {string} algorithm - 哈希算法
 * @param {string} encoding - 输出编码
 * @returns {string} HMAC 值
 */
function hmac(data, key, algorithm = HASH_ALGORITHMS.SHA256, encoding = 'hex') {
  return crypto.createHmac(algorithm, key).update(data).digest(encoding);
}

/**
 * 计算 HMAC-SHA256
 * @param {string|Buffer} data - 输入数据
 * @param {string|Buffer} key - 密钥
 * @returns {string} HMAC 值
 */
function hmacSha256(data, key) {
  return hmac(data, key, HASH_ALGORITHMS.SHA256);
}

// ============================================
// PBKDF2 密钥派生
// ============================================

/**
 * 使用 PBKDF2 派生密钥
 * @param {string|Buffer} password - 密码
 * @param {string|Buffer} salt - 盐值
 * @param {number} iterations - 迭代次数
 * @param {number} keyLength - 密钥长度（字节）
 * @param {string} algorithm - 哈希算法
 * @returns {Promise<string>} 派生的密钥（十六进制）
 */
async function pbkdf2(password, salt, iterations = 100000, keyLength = 32, algorithm = HASH_ALGORITHMS.SHA256) {
  return new Promise((resolve, reject) => {
    crypto.pbkdf2(password, salt, iterations, keyLength, algorithm, (err, derivedKey) => {
      if (err) reject(err);
      else resolve(derivedKey.toString('hex'));
    });
  });
}

/**
 * 同步版本的 PBKDF2
 * @param {string|Buffer} password - 密码
 * @param {string|Buffer} salt - 盐值
 * @param {number} iterations - 迭代次数
 * @param {number} keyLength - 密钥长度（字节）
 * @param {string} algorithm - 哈希算法
 * @returns {string} 派生的密钥（十六进制）
 */
function pbkdf2Sync(password, salt, iterations = 100000, keyLength = 32, algorithm = HASH_ALGORITHMS.SHA256) {
  return crypto.pbkdf2Sync(password, salt, iterations, keyLength, algorithm).toString('hex');
}

// ============================================
// HKDF 密钥派生
// ============================================

/**
 * 使用 HKDF 派生密钥
 * @param {string|Buffer} ikm - 输入密钥材料
 * @param {string|Buffer} salt - 盐值
 * @param {string|Buffer} info - 上下文信息
 * @param {number} keyLength - 输出密钥长度
 * @param {string} algorithm - 哈希算法
 * @returns {Buffer} 派生的密钥
 */
function hkdf(ikm, salt, info, keyLength = 32, algorithm = HASH_ALGORITHMS.SHA256) {
  const result = crypto.hkdfSync(algorithm, ikm, salt, info, keyLength);
  // Node.js hkdfSync 返回 Buffer 或字符串（取决于版本）
  return Buffer.isBuffer(result) ? result : Buffer.from(result, 'hex');
}

// ============================================
// 对称加密 (AES-GCM 推荐)
// ============================================

/**
 * AES-GCM 加密
 * @param {string|Buffer} plaintext - 明文
 * @param {string|Buffer} key - 密钥（32字节用于 AES-256）
 * @param {string|Buffer} [iv] - 初始化向量（可选，默认自动生成）
 * @param {string|Buffer} [aad] - 附加认证数据（可选）
 * @returns {Object} 包含密文、IV、认证标签的对象
 */
function aesGcmEncrypt(plaintext, key, iv = null, aad = null) {
  const actualIv = iv || crypto.randomBytes(12);
  const cipher = crypto.createCipheriv(ALGORITHMS.AES_256_GCM, key, actualIv, { authTagLength: 16 });
  
  if (aad) {
    cipher.setAAD(aad);
  }
  
  const encrypted = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const authTag = cipher.getAuthTag();
  
  return {
    ciphertext: encrypted.toString('base64'),
    iv: actualIv.toString('base64'),
    authTag: authTag.toString('base64'),
  };
}

/**
 * AES-GCM 解密
 * @param {string|Buffer} ciphertext - 密文（Base64 或 Buffer）
 * @param {string|Buffer} key - 密钥
 * @param {string|Buffer} iv - 初始化向量（Base64 或 Buffer）
 * @param {string|Buffer} authTag - 认证标签（Base64 或 Buffer）
 * @param {string|Buffer} [aad] - 附加认证数据（可选）
 * @returns {string} 明文
 */
function aesGcmDecrypt(ciphertext, key, iv, authTag, aad = null) {
  const decipher = crypto.createDecipheriv(
    ALGORITHMS.AES_256_GCM,
    key,
    typeof iv === 'string' ? Buffer.from(iv, 'base64') : iv
  );
  
  decipher.setAuthTag(typeof authTag === 'string' ? Buffer.from(authTag, 'base64') : authTag);
  
  if (aad) {
    decipher.setAAD(typeof aad === 'string' ? Buffer.from(aad) : aad);
  }
  
  const decrypted = Buffer.concat([
    decipher.update(typeof ciphertext === 'string' ? Buffer.from(ciphertext, 'base64') : ciphertext),
    decipher.final(),
  ]);
  
  return decrypted.toString('utf8');
}

/**
 * AES-CBC 加密
 * @param {string|Buffer} plaintext - 明文
 * @param {string|Buffer} key - 密钥
 * @param {string|Buffer} [iv] - 初始化向量（可选）
 * @returns {Object} 包含密文和 IV 的对象
 */
function aesCbcEncrypt(plaintext, key, iv = null) {
  const actualIv = iv || crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHMS.AES_256_CBC, key, actualIv);
  
  // PKCS7 填充由 Node.js 自动处理
  const encrypted = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  
  return {
    ciphertext: encrypted.toString('base64'),
    iv: actualIv.toString('base64'),
  };
}

/**
 * AES-CBC 解密
 * @param {string|Buffer} ciphertext - 密文
 * @param {string|Buffer} key - 密钥
 * @param {string|Buffer} iv - 初始化向量
 * @returns {string} 明文
 */
function aesCbcDecrypt(ciphertext, key, iv) {
  const decipher = crypto.createDecipheriv(
    ALGORITHMS.AES_256_CBC,
    key,
    typeof iv === 'string' ? Buffer.from(iv, 'base64') : iv
  );
  
  const decrypted = Buffer.concat([
    decipher.update(typeof ciphertext === 'string' ? Buffer.from(ciphertext, 'base64') : ciphertext),
    decipher.final(),
  ]);
  
  return decrypted.toString('utf8');
}

// ============================================
// ChaCha20-Poly1305 加密
// ============================================

/**
 * ChaCha20-Poly1305 加密
 * @param {string|Buffer} plaintext - 明文
 * @param {string|Buffer} key - 密钥（32字节）
 * @param {string|Buffer} [nonce] - nonce（可选，默认自动生成）
 * @param {string|Buffer} [aad] - 附加认证数据
 * @returns {Object} 包含密文、nonce、认证标签的对象
 */
function chaCha20Encrypt(plaintext, key, nonce = null, aad = null) {
  const actualNonce = nonce || crypto.randomBytes(12);
  const cipher = crypto.createCipheriv(ALGORITHMS.CHACHA20_POLY1305, key, actualNonce);
  
  if (aad) {
    cipher.setAAD(aad);
  }
  
  const encrypted = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const authTag = cipher.getAuthTag();
  
  return {
    ciphertext: encrypted.toString('base64'),
    nonce: actualNonce.toString('base64'),
    authTag: authTag.toString('base64'),
  };
}

/**
 * ChaCha20-Poly1305 解密
 * @param {string|Buffer} ciphertext - 密文
 * @param {string|Buffer} key - 密钥
 * @param {string|Buffer} nonce - nonce
 * @param {string|Buffer} authTag - 认证标签
 * @param {string|Buffer} [aad] - 附加认证数据
 * @returns {string} 明文
 */
function chaCha20Decrypt(ciphertext, key, nonce, authTag, aad = null) {
  const decipher = crypto.createDecipheriv(
    ALGORITHMS.CHACHA20_POLY1305,
    key,
    typeof nonce === 'string' ? Buffer.from(nonce, 'base64') : nonce
  );
  
  decipher.setAuthTag(typeof authTag === 'string' ? Buffer.from(authTag, 'base64') : authTag);
  
  if (aad) {
    decipher.setAAD(typeof aad === 'string' ? Buffer.from(aad) : aad);
  }
  
  const decrypted = Buffer.concat([
    decipher.update(typeof ciphertext === 'string' ? Buffer.from(ciphertext, 'base64') : ciphertext),
    decipher.final(),
  ]);
  
  return decrypted.toString('utf8');
}

// ============================================
// 非对称加密 (RSA)
// ============================================

/**
 * 生成 RSA 密钥对
 * @param {number} modulusLength - 模数长度（默认 2048）
 * @returns {Promise<Object>} 包含公钥和私钥的对象
 */
async function generateRsaKeyPair(modulusLength = 2048) {
  return new Promise((resolve, reject) => {
    crypto.generateKeyPair('rsa', {
      modulusLength,
      publicKeyEncoding: {
        type: 'spki',
        format: 'pem',
      },
      privateKeyEncoding: {
        type: 'pkcs8',
        format: 'pem',
      },
    }, (err, publicKey, privateKey) => {
      if (err) reject(err);
      else resolve({ publicKey, privateKey });
    });
  });
}

/**
 * RSA 公钥加密
 * @param {string|Buffer} data - 明文
 * @param {string|Buffer} publicKey - 公钥
 * @returns {string} Base64 编码的密文
 */
function rsaEncrypt(data, publicKey) {
  const encrypted = crypto.publicEncrypt(
    {
      key: publicKey,
      padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
      oaepHash: HASH_ALGORITHMS.SHA256,
    },
    typeof data === 'string' ? Buffer.from(data) : data
  );
  return encrypted.toString('base64');
}

/**
 * RSA 私钥解密
 * @param {string|Buffer} ciphertext - 密文（Base64）
 * @param {string|Buffer} privateKey - 私钥
 * @returns {string} 明文
 */
function rsaDecrypt(ciphertext, privateKey) {
  const decrypted = crypto.privateDecrypt(
    {
      key: privateKey,
      padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
      oaepHash: HASH_ALGORITHMS.SHA256,
    },
    typeof ciphertext === 'string' ? Buffer.from(ciphertext, 'base64') : ciphertext
  );
  return decrypted.toString('utf8');
}

// ============================================
// ECDSA 签名
// ============================================

/**
 * 生成 ECDSA 密钥对
 * @param {string} namedCurve - 曲线名称（默认 P-256）
 * @returns {Promise<Object>} 包含公钥和私钥的对象
 */
async function generateEcdsaKeyPair(namedCurve = 'P-256') {
  return new Promise((resolve, reject) => {
    crypto.generateKeyPair('ec', {
      namedCurve,
      publicKeyEncoding: {
        type: 'spki',
        format: 'pem',
      },
      privateKeyEncoding: {
        type: 'pkcs8',
        format: 'pem',
      },
    }, (err, publicKey, privateKey) => {
      if (err) reject(err);
      else resolve({ publicKey, privateKey });
    });
  });
}

/**
 * ECDSA 签名
 * @param {string|Buffer} data - 待签名数据
 * @param {string|Buffer} privateKey - 私钥
 * @param {string} hashAlgorithm - 哈希算法
 * @returns {string} Base64 编码的签名
 */
function ecdsaSign(data, privateKey, hashAlgorithm = HASH_ALGORITHMS.SHA256) {
  const sign = crypto.createSign(hashAlgorithm);
  sign.update(data);
  sign.end();
  return sign.sign(privateKey, 'base64');
}

/**
 * ECDSA 验证签名
 * @param {string|Buffer} data - 原始数据
 * @param {string|Buffer} signature - 签名（Base64）
 * @param {string|Buffer} publicKey - 公钥
 * @param {string} hashAlgorithm - 哈希算法
 * @returns {boolean} 验证结果
 */
function ecdsaVerify(data, signature, publicKey, hashAlgorithm = HASH_ALGORITHMS.SHA256) {
  const verify = crypto.createVerify(hashAlgorithm);
  verify.update(data);
  verify.end();
  return verify.verify(publicKey, signature, 'base64');
}

// ============================================
// Ed25519 签名（推荐）
// ============================================

/**
 * 生成 Ed25519 密钥对
 * @returns {Promise<Object>} 包含公钥和私钥的对象
 */
async function generateEd25519KeyPair() {
  return new Promise((resolve, reject) => {
    crypto.generateKeyPair('ed25519', {
      publicKeyEncoding: {
        type: 'spki',
        format: 'pem',
      },
      privateKeyEncoding: {
        type: 'pkcs8',
        format: 'pem',
      },
    }, (err, publicKey, privateKey) => {
      if (err) reject(err);
      else resolve({ publicKey, privateKey });
    });
  });
}

/**
 * Ed25519 签名
 * @param {string|Buffer} data - 待签名数据
 * @param {string|Buffer} privateKey - 私钥
 * @returns {string} Base64 编码的签名
 */
function ed25519Sign(data, privateKey) {
  // Node.js 15+ 使用 crypto.sign API
  return crypto.sign(null, Buffer.from(data), privateKey).toString('base64');
}

/**
 * Ed25519 验证签名
 * @param {string|Buffer} data - 原始数据
 * @param {string|Buffer} signature - 签名（Base64）
 * @param {string|Buffer} publicKey - 公钥
 * @returns {boolean} 验证结果
 */
function ed25519Verify(data, signature, publicKey) {
  return crypto.verify(
    null,
    Buffer.from(data),
    publicKey,
    Buffer.from(signature, 'base64')
  );
}

// ============================================
// 密码哈希（安全存储）
// ============================================

/**
 * 安全地哈希密码
 * @param {string} password - 密码
 * @param {string|Buffer} [salt] - 盐值（可选，默认自动生成）
 * @returns {Promise<Object>} 包含哈希值和盐值的对象
 */
async function hashPassword(password, salt = null) {
  const actualSalt = salt || crypto.randomBytes(16).toString('hex');
  const hash = await pbkdf2(password, actualSalt, 100000, 64);
  return {
    hash,
    salt: typeof actualSalt === 'string' ? actualSalt : actualSalt.toString('hex'),
  };
}

/**
 * 验证密码
 * @param {string} password - 待验证密码
 * @param {string} hash - 存储的哈希值
 * @param {string} salt - 盐值
 * @returns {Promise<boolean>} 验证结果
 */
async function verifyPassword(password, hash, salt) {
  const newHash = await pbkdf2(password, salt, 100000, 64);
  return crypto.timingSafeEqual(Buffer.from(hash, 'hex'), Buffer.from(newHash, 'hex'));
}

// ============================================
// 时间安全比较
// ============================================

/**
 * 时间安全字符串比较（防止时序攻击）
 * @param {string|Buffer} a - 第一个值
 * @param {string|Buffer} b - 第二个值
 * @returns {boolean} 是否相等
 */
function timingSafeEqual(a, b) {
  try {
    const bufA = typeof a === 'string' ? Buffer.from(a) : a;
    const bufB = typeof b === 'string' ? Buffer.from(b) : b;
    
    if (bufA.length !== bufB.length) {
      return false;
    }
    
    return crypto.timingSafeEqual(bufA, bufB);
  } catch {
    return false;
  }
}

// ============================================
// 便捷加密/解密（高级 API）
// ============================================

/**
 * 便捷加密：自动生成密钥，返回可序列化的加密结果
 * @param {string|Buffer} plaintext - 明文
 * @param {string} [password] - 密码（可选，默认自动生成）
 * @returns {Promise<Object>} 包含加密数据和密钥的对象
 */
async function encrypt(plaintext, password = null) {
  const actualPassword = password || crypto.randomBytes(32).toString('hex');
  const salt = crypto.randomBytes(16).toString('hex');
  const key = await pbkdf2(actualPassword, salt, 100000, 32);
  
  const result = aesGcmEncrypt(plaintext, Buffer.from(key, 'hex'));
  
  return {
    ...result,
    salt,
    key: password ? undefined : actualPassword, // 仅当密码未提供时返回密钥
  };
}

/**
 * 便捷解密：使用密码解密
 * @param {string} ciphertext - 密文（Base64）
 * @param {string} iv - IV（Base64）
 * @param {string} authTag - 认证标签（Base64）
 * @param {string} salt - 盐值
 * @param {string} password - 密码
 * @returns {Promise<string>} 明文
 */
async function decrypt(ciphertext, iv, authTag, salt, password) {
  const key = await pbkdf2(password, salt, 100000, 32);
  return aesGcmDecrypt(ciphertext, Buffer.from(key, 'hex'), iv, authTag);
}

// ============================================
// 导出
// ============================================

module.exports = {
  // 常量
  ALGORITHMS,
  HASH_ALGORITHMS,
  KEY_LENGTHS,
  
  // 辅助函数
  randomBytes,
  randomHex,
  randomBase64,
  uuidv4,
  hexToBuffer,
  bufferToHex,
  
  // 哈希函数
  hash,
  sha256,
  sha512,
  md5,
  hashFile,
  
  // HMAC
  hmac,
  hmacSha256,
  
  // 密钥派生
  pbkdf2,
  pbkdf2Sync,
  hkdf,
  
  // AES 加密
  aesGcmEncrypt,
  aesGcmDecrypt,
  aesCbcEncrypt,
  aesCbcDecrypt,
  
  // ChaCha20 加密
  chaCha20Encrypt,
  chaCha20Decrypt,
  
  // RSA
  generateRsaKeyPair,
  rsaEncrypt,
  rsaDecrypt,
  
  // ECDSA
  generateEcdsaKeyPair,
  ecdsaSign,
  ecdsaVerify,
  
  // Ed25519
  generateEd25519KeyPair,
  ed25519Sign,
  ed25519Verify,
  
  // 密码处理
  hashPassword,
  verifyPassword,
  
  // 安全工具
  timingSafeEqual,
  
  // 高级 API
  encrypt,
  decrypt,
};