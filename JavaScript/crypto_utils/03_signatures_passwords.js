/**
 * 03_signatures_passwords.js - 数字签名与密码哈希示例
 * 
 * 演示数字签名和密码哈希的用法
 * 
 * 运行: node 03_signatures_passwords.js
 */

const {
  generateEcdsaKeyPair,
  ecdsaSign,
  ecdsaVerify,
  generateEd25519KeyPair,
  ed25519Sign,
  ed25519Verify,
  hashPassword,
  verifyPassword,
  timingSafeEqual,
  pbkdf2,
} = require('./crypto_utils');

async function main() {
  console.log('========================================');
  console.log('crypto_utils 数字签名与密码哈希示例');
  console.log('========================================\n');

  // ============================================
  // 1. Ed25519 签名（推荐）
  // ============================================
  console.log('--- Ed25519 数字签名 ---\n');

  console.log('生成 Ed25519 密钥对...');
  const edKeys = await generateEd25519KeyPair();
  console.log('密钥对已生成\n');

  const message = '需要签名的消息 📝';
  console.log('原始消息:', message);

  // 签名
  const edSignature = ed25519Sign(message, edKeys.privateKey);
  console.log('签名:', edSignature.substring(0, 32) + '...');

  // 验证
  const edValid = ed25519Verify(message, edSignature, edKeys.publicKey);
  console.log('签名验证:', edValid ? '✅ 有效' : '❌ 无效');

  // 篡改检测
  const tamperedValid = ed25519Verify('篡改的消息', edSignature, edKeys.publicKey);
  console.log('篡改消息验证:', tamperedValid ? '✅ 有效' : '❌ 无效');

  // ============================================
  // 2. ECDSA 签名
  // ============================================
  console.log('\n--- ECDSA 数字签名 ---\n');

  console.log('生成 ECDSA 密钥对 (P-256)...');
  const ecdsaKeys = await generateEcdsaKeyPair('P-256');
  console.log('密钥对已生成\n');

  const ecdsaMessage = 'ECDSA 签名的消息';
  console.log('原始消息:', ecdsaMessage);

  // 签名
  const ecdsaSignature = ecdsaSign(ecdsaMessage, ecdsaKeys.privateKey);
  console.log('签名:', ecdsaSignature.substring(0, 32) + '...');

  // 验证
  const ecdsaValid = ecdsaVerify(ecdsaMessage, ecdsaSignature, ecdsaKeys.publicKey);
  console.log('签名验证:', ecdsaValid ? '✅ 有效' : '❌ 无效');

  // ============================================
  // 3. 不同曲线的 ECDSA
  // ============================================
  console.log('\n--- 不同椭圆曲线 ---\n');

  const curves = ['P-256', 'P-384', 'P-521'];
  
  for (const curve of curves) {
    const keys = await generateEcdsaKeyPair(curve);
    const hashAlgo = curve === 'P-256' ? 'sha256' : curve === 'P-384' ? 'sha384' : 'sha512';
    const sig = ecdsaSign('测试消息', keys.privateKey, hashAlgo);
    const valid = ecdsaVerify('测试消息', sig, keys.publicKey, hashAlgo);
    console.log(`${curve}: 签名长度 ${sig.length}, 验证 ${valid ? '✅' : '❌'}`);
  }

  // ============================================
  // 4. 密码哈希
  // ============================================
  console.log('\n--- 密码哈希 ---\n');

  const password = 'user_password_123';
  console.log('原始密码:', password);

  // 哈希密码
  console.log('\n哈希密码中 (PBKDF2, 100000 迭代)...');
  const startTime = Date.now();
  const { hash, salt } = await hashPassword(password);
  const hashTime = Date.now() - startTime;
  
  console.log('哈希值:', hash.substring(0, 32) + '...');
  console.log('盐值:', salt);
  console.log('计算时间:', hashTime, 'ms');

  // 验证正确密码
  const validPassword = await verifyPassword(password, hash, salt);
  console.log('\n验证正确密码:', validPassword ? '✅ 通过' : '❌ 失败');

  // 验证错误密码
  const invalidPassword = await verifyPassword('wrong_password', hash, salt);
  console.log('验证错误密码:', invalidPassword ? '✅ 通过' : '❌ 失败');

  // ============================================
  // 5. 使用自定义盐值
  // ============================================
  console.log('\n--- 自定义盐值 ---\n');

  const customSalt = 'my-custom-salt-value';
  const { hash: hash1 } = await hashPassword(password, customSalt);
  const { hash: hash2 } = await hashPassword(password, customSalt);
  
  console.log('相同密码 + 相同盐值 = 相同哈希:');
  console.log('哈希1:', hash1.substring(0, 32) + '...');
  console.log('哈希2:', hash2.substring(0, 32) + '...');
  console.log('是否相同:', hash1 === hash2 ? '✅' : '❌');

  // ============================================
  // 6. 时序安全比较
  // ============================================
  console.log('\n--- 时序安全比较 ---\n');

  const token1 = 'abc123def456ghi789';
  const token2 = 'abc123def456ghi789';
  const token3 = 'xyz789uvw456rst123';

  console.log('token1:', token1);
  console.log('token2:', token2);
  console.log('token3:', token3);
  console.log('\ntoken1 === token2:', timingSafeEqual(token1, token2) ? '✅ 相等' : '❌ 不等');
  console.log('token1 === token3:', timingSafeEqual(token1, token3) ? '✅ 相等' : '❌ 不等');

  // ============================================
  // 7. 密钥派生
  // ============================================
  console.log('\n--- 密钥派生 ---\n');

  const masterPassword = 'master_secret_key';
  const applicationSalt = 'app_salt_2024';
  
  console.log('主密码:', masterPassword);
  console.log('应用盐值:', applicationSalt);
  
  const derivedKey = await pbkdf2(masterPassword, applicationSalt, 100000, 32);
  console.log('派生密钥:', derivedKey.substring(0, 32) + '...');
  console.log('密钥长度:', derivedKey.length / 2, '字节');

  // 派生多个密钥
  const key1 = await pbkdf2(masterPassword, applicationSalt + ':encryption', 100000, 32);
  const key2 = await pbkdf2(masterPassword, applicationSalt + ':signing', 100000, 32);
  console.log('\n派生多个密钥:');
  console.log('加密密钥:', key1.substring(0, 16) + '...');
  console.log('签名密钥:', key2.substring(0, 16) + '...');

  console.log('\n========================================');
  console.log('示例完成！');
  console.log('========================================');
}

main().catch(console.error);