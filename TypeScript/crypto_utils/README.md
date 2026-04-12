# Crypto Utils - TypeScript

加密工具模块，提供哈希、编码、加密和随机生成功能。

## 特性

- **零依赖** - 使用 Node.js crypto 模块或 Web Crypto API
- **跨平台** - 支持 Node.js 和浏览器环境
- **完整测试** - 86+ 测试用例覆盖所有功能
- **类型安全** - 完整的 TypeScript 类型定义

## 安装

```bash
npm install alltoolkit-crypto-utils
```

## 功能

### 哈希函数

```typescript
import { md5, sha1, sha256, sha384, sha512, hash } from 'crypto_utils';

// MD5 (仅用于校验，不推荐用于安全场景)
md5('hello');  // '5d41402abc4b2a76b9719d911017c592'

// SHA-1
sha1('hello');  // 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d'

// SHA-256
sha256('hello');  // '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'

// SHA-384
sha384('hello');  // 96字符十六进制字符串

// SHA-512
sha512('hello');  // 128字符十六进制字符串

// 通用哈希函数
hash('hello', 'SHA-256');
```

### HMAC 签名

```typescript
import { hmacSha256, hmacSha384, hmacSha512, verifyHmac } from 'crypto_utils';

// 生成 HMAC
const signature = hmacSha256('message', 'secret');

// 验证签名
verifyHmac('message', 'secret', signature);  // true
verifyHmac('message', 'wrong-secret', signature);  // false
```

### Base64 编码

```typescript
import { base64Encode, base64Decode, base64UrlEncode, base64UrlDecode, isValidBase64 } from 'crypto_utils';

// 标准 Base64
base64Encode('Hello World!');  // 'SGVsbG8gV29ybGQh'
base64Decode('SGVsbG8gV29ybGQh');  // 'Hello World!'

// URL-safe Base64 (RFC 4648)
base64UrlEncode('Hello+World');  // 无 + 和 / 字符
base64UrlDecode('SGVsbG8rV29ybGQ');

// 验证
isValidBase64('SGVsbG8=');  // true
```

### Hex 编码

```typescript
import { hexEncode, hexDecode, isValidHex } from 'crypto_utils';

hexEncode('Hello');  // '48656c6c6f'
hexDecode('48656c6c6f');  // 'Hello'

isValidHex('48656c6c6f');  // true
isValidHex('invalid!');  // false
```

### 随机生成

```typescript
import { randomString, randomHex, uuidv4 } from 'crypto_utils';

// 随机字符串
randomString(16);  // 16字符随机字母数字
randomString(10, '0123456789');  // 仅数字

// 随机十六进制
randomHex(32);  // 32字符十六进制

// UUID v4
uuidv4();  // 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
```

## API 参考

| 函数 | 描述 | 返回类型 |
|------|------|----------|
| `md5(input)` | MD5 哈希 | `string` (32字符) |
| `sha1(input)` | SHA-1 哈希 | `string` (40字符) |
| `sha256(input)` | SHA-256 哈希 | `string` (64字符) |
| `sha384(input)` | SHA-384 哈希 | `string` (96字符) |
| `sha512(input)` | SHA-512 哈希 | `string` (128字符) |
| `hash(input, algorithm)` | 通用哈希 | `string` |
| `hmacSha256(message, secret)` | HMAC-SHA256 | `string` |
| `hmacSha384(message, secret)` | HMAC-SHA384 | `string` |
| `hmacSha512(message, secret)` | HMAC-SHA512 | `string` |
| `verifyHmac(message, secret, signature, algorithm)` | 验证 HMAC | `boolean` |
| `base64Encode(input)` | Base64 编码 | `string` |
| `base64Decode(input)` | Base64 解码 | `string` |
| `base64UrlEncode(input, padding)` | URL-safe Base64 编码 | `string` |
| `base64UrlDecode(input)` | URL-safe Base64 解码 | `string` |
| `isValidBase64(input)` | 验证 Base64 | `boolean` |
| `hexEncode(input)` | Hex 编码 | `string` |
| `hexDecode(input)` | Hex 解码 | `string` |
| `isValidHex(input)` | 验证 Hex | `boolean` |
| `randomString(length, charset)` | 随机字符串 | `string` |
| `randomHex(length)` | 随机 Hex | `string` |
| `uuidv4()` | UUID v4 | `string` |

## 运行测试

```bash
# 使用 tsx
npx tsx crypto_utils_test.ts

# 使用 Deno
deno test crypto_utils_test.ts

# 使用 Bun
bun test crypto_utils_test.ts
```

## 安全说明

- **MD5 和 SHA-1** 不推荐用于安全敏感场景，仅用于校验和兼容
- **SHA-256/384/512** 适用于安全场景
- **HMAC 验证** 使用时序安全比较防止时序攻击
- **简单后备实现** 仅用于无 crypto 模块的环境，不推荐用于生产

## 许可证

MIT License