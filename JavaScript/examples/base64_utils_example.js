/**
 * Base64 Utilities - 使用示例
 * 
 * 本文件演示如何使用 base64_utils 模块的各种功能。
 * 
 * 运行方式:
 * - Node.js: node base64_utils_example.js
 * - 浏览器: 在 HTML 中引入 <script src="../base64_utils/mod.js"></script>
 *           然后在控制台运行示例代码
 */

// 加载模块（Node.js 环境）
const Base64Utils = (typeof require !== 'undefined') 
  ? require('../base64_utils/mod.js') 
  : window;

const { encode, decode, toUrlSafe, fromUrlSafe, isValid, toUint8Array, fromUint8Array, encodedLength } = Base64Utils;

console.log('========================================');
console.log('Base64 Utilities - Usage Examples');
console.log('========================================\n');

// ========================================
// 1. 基本编码和解码
// ========================================
console.log('--- 1. Basic Encoding and Decoding ---\n');

const originalText = 'Hello, World! 你好，世界！';
console.log('Original:', originalText);

// 编码为 Base64
const encoded = encode(originalText);
console.log('Encoded:', encoded);

// 解码回原始文本
const decoded = decode(encoded);
console.log('Decoded:', decoded);
console.log('Match:', originalText === decoded ? '✓' : '✗');

// ========================================
// 2. URL 安全 Base64
// ========================================
console.log('\n--- 2. URL-Safe Base64 ---\n');

// 标准 Base64 包含 + 和 /，在 URL 中需要编码
const standardBase64 = encode('>>>???');
console.log('Standard Base64:', standardBase64);

// 转换为 URL 安全格式（+ -> -, / -> _, 移除 =）
const urlSafe = toUrlSafe(standardBase64);
console.log('URL-Safe:', urlSafe);

// 从 URL 安全格式转回标准格式
const backToStandard = fromUrlSafe(urlSafe);
console.log('Back to Standard:', backToStandard);

// 直接编码为 URL 安全格式
const directUrlSafe = encode('Hello World', { urlSafe: true, pad: false });
console.log('Direct URL-Safe:', directUrlSafe);

// ========================================
// 3. 验证 Base64 字符串
// ========================================
console.log('\n--- 3. Validation ---\n');

const validString = 'SGVsbG8gV29ybGQ=';
const invalidString = 'Invalid!!!';

console.log(`isValid('${validString}'):`, isValid(validString) ? '✓ Valid' : '✗ Invalid');
console.log(`isValid('${invalidString}'):`, isValid(invalidString) ? '✓ Valid' : '✗ Invalid');

// 验证 URL 安全格式
const urlSafeString = 'SGVsbG8gV29ybGQ';
console.log(`isValid('${urlSafeString}', { urlSafe: true }):`, 
  isValid(urlSafeString, { urlSafe: true }) ? '✓ Valid' : '✗ Invalid');

// ========================================
// 4. 处理二进制数据
// ========================================
console.log('\n--- 4. Binary Data Handling ---\n');

// 将 Base64 转换为 Uint8Array
const base64Data = 'SGVsbG8gV29ybGQ=';
const uint8Array = toUint8Array(base64Data);
console.log('Base64 to Uint8Array:', base64Data);
console.log('Uint8Array:', Array.from(uint8Array));

// 将 Uint8Array 编码回 Base64
const backToBase64 = fromUint8Array(uint8Array);
console.log('Back to Base64:', backToBase64);

// 创建自定义二进制数据
const customBytes = new Uint8Array([0x48, 0x65, 0x6C, 0x6C, 0x6F]); // "Hello"
const customBase64 = fromUint8Array(customBytes);
console.log('Custom bytes to Base64:', customBase64);

// ========================================
// 5. 计算编码后长度
// ========================================
console.log('\n--- 5. Calculate Encoded Length ---\n');

const testStrings = ['A', 'AB', 'ABC', 'Hello', 'Hello World'];
for (const str of testStrings) {
  const withPad = encodedLength(str);
  const withoutPad = encodedLength(str, { pad: false });
  console.log(`'${str}' -> With padding: ${withPad}, Without padding: ${withoutPad}`);
}

// ========================================
// 6. 实际应用场景
// ========================================
console.log('\n--- 6. Practical Use Cases ---\n');

// 场景 1: 在 URL 中传递数据
console.log('Use Case 1: Passing data in URL');
const userData = { name: 'John', age: 30 };
const jsonString = JSON.stringify(userData);
const urlSafeData = encode(jsonString, { urlSafe: true, pad: false });
const url = `https://example.com/data?payload=${urlSafeData}`;
console.log('URL:', url.substring(0, 70) + '...');

// 场景 2: 处理 Unicode 字符（如 Emoji）
console.log('\nUse Case 2: Encoding Unicode/Emoji');
const emoji = '🎉🎊🎁';
const emojiEncoded = encode(emoji);
const emojiDecoded = decode(emojiEncoded);
console.log('Original:', emoji);
console.log('Encoded:', emojiEncoded);
console.log('Decoded:', emojiDecoded);

// 场景 3: 处理多语言文本
console.log('\nUse Case 3: Multi-language Text');
const multiLang = 'Hello 你好 こんにちは 안녕하세요';
const multiEncoded = encode(multiLang);
const multiDecoded = decode(multiEncoded);
console.log('Original:', multiLang);
console.log('Encoded:', multiEncoded);
console.log('Decoded:', multiDecoded);
console.log('Match:', multiLang === multiDecoded ? '✓' : '✗');

// ========================================
// 7. 无填充编码
// ========================================
console.log('\n--- 7. Encoding Without Padding ---\n');

const text = 'Hello';
const withPadding = encode(text);
const withoutPadding = encode(text, { pad: false });

console.log('Original:', text);
console.log('With padding:', withPadding);
console.log('Without padding:', withoutPadding);

// 解码时两种格式都可以正确解码
console.log('Decode with padding:', decode(withPadding));
console.log('Decode without padding:', decode(withoutPadding));

// ========================================
// 8. 错误处理示例
// ========================================
console.log('\n--- 8. Error Handling ---\n');

// 尝试解码无效的 Base64
try {
  decode('This is not valid!!!');
} catch (e) {
  console.log('Caught error for invalid Base64:', e.message);
}

// 尝试对非字符串进行编码
try {
  encode(12345);
} catch (e) {
  console.log('Caught error for non-string input:', e.message);
}

// 使用 isValid 进行安全验证
const userInput = 'UserInput123';
if (isValid(userInput)) {
  console.log('Valid Base64, decoding:', decode(userInput));
} else {
  console.log('Invalid Base64, skipping decode');
}

console.log('\n========================================');
console.log('Examples completed!');
console.log('========================================');
