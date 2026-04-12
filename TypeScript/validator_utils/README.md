# Validator Utils - TypeScript

数据验证工具函数库，提供全面的输入验证功能。

## 功能特性

- 📧 **邮箱验证** - RFC 5322 兼容，支持 IP 域名
- 📱 **电话号码验证** - 支持多国格式（中国、美国、英国等）
- 🔗 **URL 验证** - 支持协议过滤、IP 地址检测
- 🌐 **IP 地址验证** - IPv4/IPv6，私有地址检测
- 🆔 **身份证验证** - 中国身份证、美国 SSN
- 💳 **信用卡验证** - Luhn 算法，支持多家发卡行
- 📅 **日期时间验证** - 多种格式，闰年检测
- 📝 **字符串验证** - 长度、模式匹配

## 零依赖

仅使用 TypeScript/JavaScript 标准库，无需额外安装。

## 安装

无需安装，直接复制 `validator_utils.ts` 到你的项目即可使用。

```typescript
import {
  validateEmail,
  validatePhone,
  validateUrl,
  validateIP,
  validateChineseIdCard,
  validateCreditCard,
  validateDate,
  validateTime,
  validateString,
  validatePattern,
} from './validator_utils.ts';
```

## 使用示例

### 邮箱验证

```typescript
// 基本验证
const result = validateEmail('user@example.com');
// { valid: true, data: { local: 'user', domain: 'example.com' } }

// 带选项验证
const result2 = validateEmail('user@[192.168.1.1]', { 
  allowIpDomain: true,
  requireTld: false 
});

// 检查验证结果
if (result.valid) {
  console.log('邮箱有效');
} else {
  console.log('邮箱无效:', result.error);
}
```

### 电话号码验证

```typescript
// 中国手机号
const cn = validatePhone('13800138000', { countryCode: 'CN' });
// { valid: true }

// 国际格式
const intl = validatePhone('+1-555-123-4567', { 
  allowInternational: true 
});

// 带分隔号的号码
const formatted = validatePhone('138-0013-8000', { countryCode: 'CN' });
// 自动移除 -、空格、括号等分隔符
```

### URL 验证

```typescript
// 基本验证
const url = validateUrl('https://example.com/path?query=1');
// { valid: true, data: { protocol: 'https', host: 'example.com', ... } }

// 限制协议
const httpOnly = validateUrl('ftp://files.example.com', {
  protocols: ['http', 'https']
});
// { valid: false, error: "Protocol 'ftp' not allowed..." }

// 禁止 IP 地址
const noIp = validateUrl('http://192.168.1.1', { allowIp: false });
```

### IP 地址验证

```typescript
// IPv4
const ipv4 = validateIPv4('192.168.1.1');
// { valid: true, data: { version: 4, isPrivate: true, ... } }

// IPv6
const ipv6 = validateIPv6('2001:db8::1');
// { valid: true, data: { version: 6, compressed: true } }

// 自动检测
const ip = validateIP('192.168.1.1');
// 自动识别为 IPv4

const ip6 = validateIP('::1', 6);
// 强制要求 IPv6
```

### 身份证验证

```typescript
// 中国身份证
const cnId = validateChineseIdCard('110101199001011234');
// { valid: true, data: { birthdate: '1990-01-01', gender: 'male', ... } }

// 美国 SSN
const ssn = validateUSSSN('123-45-6789');
// { valid: true, data: { area: '123', group: '45', serial: '6789' } }
```

### 信用卡验证

```typescript
// Luhn 算法验证
const card = validateCreditCard('4532015112830366');
// { valid: true, data: { issuer: 'visa', lastFour: '0366', ... } }

// 指定发卡行
const visa = validateCreditCard('4532015112830366', 'visa');
// { valid: true }

const mc = validateCreditCard('4532015112830366', 'mastercard');
// { valid: false, error: "Card number does not match mastercard pattern" }
```

### 日期时间验证

```typescript
// 日期验证
const date = validateDate('2024-01-15', { format: 'YYYY-MM-DD' });
// { valid: true, data: { year: 2024, month: 1, day: 15, ... } }

// 闰年检测
const leap = validateDate('2024-02-29', { format: 'YYYY-MM-DD' });
// { valid: true } (2024 是闰年)

const nonLeap = validateDate('2023-02-29', { format: 'YYYY-MM-DD' });
// { valid: false, error: 'Invalid day for month 2' }

// 日期范围
const range = validateDate('2024-06-15', {
  format: 'YYYY-MM-DD',
  min: new Date(2024, 0, 1),
  max: new Date(2024, 11, 31)
});

// 时间验证
const time = validateTime('14:30:45', 'HH:mm:ss');
const time12h = validateTime('2:30 PM', '12h');
```

### 字符串验证

```typescript
// 长度验证
const str = validateString('hello', {
  minLength: 3,
  maxLength: 10
});

// 精确长度
const exact = validateString('hello', { exactLength: 5 });

// 允许空字符串
const empty = validateString('', { allowEmpty: true });

// 模式匹配
const pattern = validatePattern('hello123', /^[a-z]+\d+$/i);
```

### 批量验证

```typescript
// 验证多个字段
const results = validateFields({
  email: () => validateEmail('user@example.com'),
  phone: () => validatePhone('13800138000', { countryCode: 'CN' }),
  url: () => validateUrl('https://example.com')
});

// 检查是否全部通过
const allPassed = allValid(Object.values(results));

// 获取第一个错误
const firstError = getFirstError(Object.values(results));
```

## API 参考

### 类型定义

```typescript
interface ValidationResult {
  valid: boolean;
  error?: string;
  data?: Record<string, unknown>;
}

interface EmailOptions {
  allowIpDomain?: boolean;
  requireTld?: boolean;
  maxLength?: number;
}

interface PhoneOptions {
  countryCode?: string;  // 'CN', 'US', 'UK', 'JP', 'DE', 'FR', 'AU', 'IN', 'BR', 'RU'
  allowInternational?: boolean;
  strict?: boolean;
}

interface UrlOptions {
  protocols?: string[];  // 默认 ['http', 'https']
  requireProtocol?: boolean;
  allowIp?: boolean;
  requireTld?: boolean;
}

interface DateOptions {
  format?: string;  // 'YYYY-MM-DD', 'DD/MM/YYYY', 'MM/DD/YYYY', 'YYYYMMDD'
  min?: Date;
  max?: Date;
}

interface StringOptions {
  minLength?: number;
  maxLength?: number;
  exactLength?: number;
  allowEmpty?: boolean;
  trim?: boolean;
}
```

### 函数列表

| 函数 | 描述 |
|------|------|
| `validateEmail(email, options?)` | 验证邮箱地址 |
| `validatePhone(phone, options?)` | 验证电话号码 |
| `validateUrl(url, options?)` | 验证 URL |
| `validateIP(ip, version?)` | 验证 IP 地址（v4/v6） |
| `validateIPv4(ip)` | 验证 IPv4 地址 |
| `validateIPv6(ip)` | 验证 IPv6 地址 |
| `validateChineseIdCard(idCard)` | 验证中国身份证 |
| `validateUSSSN(ssn)` | 验证美国 SSN |
| `validateCreditCard(cardNumber, issuer?)` | 验证信用卡号 |
| `validateDate(dateStr, options?)` | 验证日期 |
| `validateTime(timeStr, format?)` | 验证时间 |
| `validateString(str, options?)` | 验证字符串 |
| `validatePattern(str, pattern, flags?)` | 验证字符串模式 |
| `validateFields(fields)` | 批量验证多个字段 |
| `allValid(results)` | 检查是否全部验证通过 |
| `getFirstError(results)` | 获取第一个错误信息 |

## 运行测试

```bash
# 使用 Deno
deno test validator_utils_test.ts

# 使用 Bun
bun test validator_utils_test.ts

# 使用 Node.js 20+
node --test validator_utils_test.ts
```

## 支持的国家/地区代码

| 代码 | 国家/地区 | 格式示例 |
|------|-----------|----------|
| CN | 中国 | 13800138000 |
| US | 美国/加拿大 | +1-555-123-4567 |
| UK | 英国 | +44-7911-123456 |
| JP | 日本 | +81-90-1234-5678 |
| DE | 德国 | +49-151-12345678 |
| FR | 法国 | +33-6-12-34-56-78 |
| AU | 澳大利亚 | +61-4-1234-5678 |
| IN | 印度 | +91-98765-43210 |
| BR | 巴西 | +55-11-91234-5678 |
| RU | 俄罗斯 | +7-912-345-67-89 |

## 支持的信用卡发卡行

| 发卡行 | 卡号前缀 | 长度 |
|--------|----------|------|
| Visa | 4 | 13, 16, 19 |
| Mastercard | 51-55, 22-27 | 16 |
| American Express | 34, 37 | 15 |
| Discover | 6011, 65 | 16 |
| JCB | 35 | 16 |
| Diners Club | 300-305, 36, 38 | 14 |

## 许可证

MIT License

## 版本

1.0.0
