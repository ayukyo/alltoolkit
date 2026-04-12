/**
 * 02_encryption.js - 加密解密示例
 * 
 * 演示对称加密和非对称加密的用法
 * 
 * 运行: node 02_encryption.js
 */

const {
  randomBytes,
  aesGcmEncrypt,
  aesGcmDecrypt,
  aesCbcEncrypt,
  aesCbcDecrypt,
  chaCha20Encrypt,
  chaCha20Decrypt,
  generateRsaKeyPair,
  rsaEncrypt,
  rsaDecrypt,
  encrypt,
  decrypt,
} = require('./crypto_utils');

async function main() {
  console.log('========================================');
  console.log('crypto_utils 加密解密示例');
  console.log('========================================\n');

  // ============================================
  // 1. AES-GCM 加密（推荐）
  // ============================================
  console.log('--- AES-GCM 加密 ---\n');

  const aesKey = randomBytes(32); // 256 位密钥
  const plaintext = '这是需要加密的敏感信息 🔐';

  console.log('原始数据:', plaintext);

  const aesEncrypted = aesGcmEncrypt(plaintext, aesKey);
  console.log('加密结果:');
  console.log('  密文:', aesEncrypted.ciphertext.substring(0, 32) + '...');
  console.log('  IV:', aesEncrypted.iv);
  console.log('  认证标签:', aesEncrypted.authTag);

  const aesDecrypted = aesGcmDecrypt(
    aesEncrypted.ciphertext,
    aesKey,
    aesEncrypted.iv,
    aesEncrypted.authTag
  );
  console.log('解密结果:', aesDecrypted);

  // ============================================
  // 2. AES-CBC 加密
  // ============================================
  console.log('\n--- AES-CBC 加密 ---\n');

  const cbcEncrypted = aesCbcEncrypt(plaintext, aesKey);
  console.log('加密结果:');
  console.log('  密文:', cbcEncrypted.ciphertext.substring(0, 32) + '...');
  console.log('  IV:', cbcEncrypted.iv);

  const cbcDecrypted = aesCbcDecrypt(
    cbcEncrypted.ciphertext,
    aesKey,
    cbcEncrypted.iv
  );
  console.log('解密结果:', cbcDecrypted);

  // ============================================
  // 3. ChaCha20-Poly1305 加密
  // ============================================
  console.log('\n--- ChaCha20-Poly1305 加密 ---\n');

  const chachaKey = randomBytes(32);
  const chachaEncrypted = chaCha20Encrypt(plaintext, chachaKey);
  console.log('加密结果:');
  console.log('  密文:', chachaEncrypted.ciphertext.substring(0, 32) + '...');
  console.log('  Nonce:', chachaEncrypted.nonce);
  console.log('  认证标签:', chachaEncrypted.authTag);

  const chachaDecrypted = chaCha20Decrypt(
    chachaEncrypted.ciphertext,
    chachaKey,
    chachaEncrypted.nonce,
    chachaEncrypted.authTag
  );
  console.log('解密结果:', chachaDecrypted);

  // ============================================
  // 4. RSA 非对称加密
  // ============================================
  console.log('\n--- RSA 非对称加密 ---\n');

  console.log('生成 RSA 密钥对...');
  const { publicKey, privateKey } = await generateRsaKeyPair(2048);
  console.log('密钥对已生成');

  const rsaMessage = 'RSA 加密的消息';
  const rsaEncrypted = rsaEncrypt(rsaMessage, publicKey);
  console.log('加密结果:', rsaEncrypted.substring(0, 32) + '...');

  const rsaDecrypted = rsaDecrypt(rsaEncrypted, privateKey);
  console.log('解密结果:', rsaDecrypted);

  // ============================================
  // 5. 高级便捷 API
  // ============================================
  console.log('\n--- 高级便捷 API ---\n');

  // 自动生成密钥
  const autoEncrypted = await encrypt('自动加密的秘密消息');
  console.log('自动加密:');
  console.log('  密文:', autoEncrypted.ciphertext.substring(0, 32) + '...');
  console.log('  自动生成的密钥:', autoEncrypted.key);

  const autoDecrypted = await decrypt(
    autoEncrypted.ciphertext,
    autoEncrypted.iv,
    autoEncrypted.authTag,
    autoEncrypted.salt,
    autoEncrypted.key
  );
  console.log('解密结果:', autoDecrypted);

  // 使用密码加密
  const passwordEncrypted = await encrypt('密码加密的消息', 'my-password-123');
  console.log('\n使用密码加密:');
  console.log('  密文:', passwordEncrypted.ciphertext.substring(0, 32) + '...');

  const passwordDecrypted = await decrypt(
    passwordEncrypted.ciphertext,
    passwordEncrypted.iv,
    passwordEncrypted.authTag,
    passwordEncrypted.salt,
    'my-password-123'
  );
  console.log('解密结果:', passwordDecrypted);

  // ============================================
  // 6. 附加认证数据 (AAD)
  // ============================================
  console.log('\n--- 附加认证数据 (AAD) ---\n');

  const aad = Buffer.from('user_id:12345');
  const aadEncrypted = aesGcmEncrypt('敏感数据', aesKey, null, aad);
  console.log('使用 AAD 加密完成');
  console.log('AAD:', aad.toString());

  // 解密时必须提供相同的 AAD
  const aadDecrypted = aesGcmDecrypt(
    aadEncrypted.ciphertext,
    aesKey,
    aadEncrypted.iv,
    aadEncrypted.authTag,
    aad
  );
  console.log('解密结果:', aadDecrypted);

  console.log('\n========================================');
  console.log('示例完成！');
  console.log('========================================');
}

main().catch(console.error);