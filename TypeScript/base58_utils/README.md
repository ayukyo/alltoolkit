# Base58 Utils

Base58 编码/解码工具模块，零外部依赖，纯 TypeScript 实现。

## 功能特性

- ✅ Base58 编码/解码（字节数组、字符串、十六进制）
- ✅ 多种字母表支持（Bitcoin、Flickr、Ripple）
- ✅ 自定义字母表
- ✅ BigInt 支持
- ✅ 带校验和的编解码
- ✅ 随机 Base58 字符串生成
- ✅ 有效性验证
- ✅ 完整类型支持

## 安装

```typescript
import { encodeBase58, decodeBase58 } from './base58_utils/mod';
```

## 快速开始

### 基础编解码

```typescript
import { encodeBase58, decodeBase58 } from './base58_utils/mod';

// 编码字节数组
const data = new TextEncoder().encode('Hello!');
const encoded = encodeBase58(data);
console.log(encoded); // "9Ajdvzr"

// 解码
const decoded = decodeBase58(encoded);
console.log(new TextDecoder().decode(decoded)); // "Hello!"
```

### 字符串快捷方法

```typescript
import { encodeBase58String, decodeBase58String } from './base58_utils/mod';

const encoded = encodeBase58String('测试中文 🚀');
const decoded = decodeBase58String(encoded);
console.log(decoded); // "测试中文 🚀"
```

### 十六进制编解码

```typescript
import { encodeBase58Hex, decodeBase58ToHex } from './base58_utils/mod';

const encoded = encodeBase58Hex('deadbeef');
const decoded = decodeBase58ToHex(encoded);
console.log(decoded); // "deadbeef"
```

### 随机生成

```typescript
import { randomBase58 } from './base58_utils/mod';

const id = randomBase58(16);
console.log(id); // 例如: "2gBuM5PmDqF3QkLw"
```

### BigInt 支持

```typescript
import { bigIntToBase58, base58ToBigInt } from './base58_utils/mod';

const bigNumber = 123456789012345678901234567890n;
const encoded = bigIntToBase58(bigNumber);
const decoded = base58ToBigInt(encoded);
console.log(decoded === bigNumber); // true
```

### 带校验和编解码

```typescript
import { encodeWithChecksum, decodeWithChecksum } from './base58_utils/mod';

const data = new TextEncoder().encode('important data');
const encoded = encodeWithChecksum(data);

// 解码并验证校验和
const decoded = decodeWithChecksum(encoded);
if (decoded !== null) {
    console.log('校验成功');
}

// 篡改数据会返回 null
const tamperedResult = decodeWithChecksum(encoded + 'x');
console.log(tamperedResult); // null
```

### 不同字母表

```typescript
import { base58, base58Flickr, base58Ripple } from './base58_utils/mod';

const data = new Uint8Array([0xde, 0xad, 0xbe, 0xef]);

console.log(base58.encode(data));      // Bitcoin 字母表
console.log(base58Flickr.encode(data)); // Flickr 字母表
console.log(base58Ripple.encode(data)); // Ripple 字母表
```

### 自定义字母表

```typescript
import { Base58Encoder } from './base58_utils/mod';

const customAlphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz123456789';
const encoder = new Base58Encoder(customAlphabet);
const encoded = encoder.encode(data);
```

## API 参考

### 函数

| 函数 | 说明 |
|------|------|
| `encodeBase58(bytes)` | 编码字节数组 |
| `decodeBase58(str)` | 解码为字节数组 |
| `encodeBase58String(str)` | 编码 UTF-8 字符串 |
| `decodeBase58String(str)` | 解码为 UTF-8 字符串 |
| `encodeBase58Hex(hex)` | 编码十六进制字符串 |
| `decodeBase58ToHex(str)` | 解码为十六进制字符串 |
| `isValidBase58(str)` | 验证是否为有效 Base58 |
| `randomBase58(length)` | 生成随机 Base58 字符串 |
| `bigIntToBase58(value)` | BigInt 转 Base58 |
| `base58ToBigInt(str)` | Base58 转 BigInt |
| `encodeWithChecksum(data)` | 带校验和编码 |
| `decodeWithChecksum(str)` | 带校验和解码 |

### 类

| 类 | 说明 |
|----|------|
| `Base58Encoder` | 编码器类，支持自定义字母表 |

### 预定义实例

| 实例 | 字母表 |
|------|--------|
| `base58` | Bitcoin（最常用）|
| `base58Flickr` | Flickr |
| `base58Ripple` | Ripple |

## 使用场景

- 🔑 Bitcoin 地址编码
- 📁 IPFS 内容标识符
- 🔗 短链接 ID 生成
- 🎫 邀请码/优惠券生成
- 🔐 安全令牌生成
- 📦 订单号生成

## 运行测试

```bash
npx ts-node base58_utils/base58_utils_test.ts
```

## 运行示例

```bash
npx ts-node base58_utils/examples/usage_examples.ts
```

## License

MIT