# mask_utils - 数据脱敏/格式化工具

JavaScript 数据脱敏和格式化工具库，提供敏感信息的脱敏、格式化和验证功能。

## 安装

```bash
# 将 mask_utils.js 复制到项目中使用
```

## 功能特性

### 脱敏功能
- 📱 手机号脱敏
- ☎️ 固定电话脱敏
- 🪪 身份证号脱敏
- 💳 银行卡号脱敏
- 📧 邮箱脱敏
- 👤 姓名脱敏
- 🏠 地址脱敏
- 🌐 IP地址脱敏
- 💳 信用卡号脱敏
- 🛂 护照号脱敏
- 🚗 驾驶证号脱敏
- 🏢 统一社会信用代码脱敏
- 🚙 车牌号脱敏
- ✏️ 自定义脱敏

### 格式化功能
- 银行卡号格式化
- 手机号格式化
- 金额格式化（千分位）

### 验证功能
- 手机号验证
- 邮箱验证
- 身份证号验证（含校验位）
- 银行卡号验证（Luhn算法）
- IP地址验证
- 信用卡号验证（含卡类型识别）

### 文本脱敏
- 从文本中提取并脱敏手机号
- 从文本中提取并脱敏邮箱
- 从文本中提取并脱敏身份证号

## API 文档

### 脱敏函数

#### maskPhone(phone, options?)
手机号脱敏

```javascript
const { maskPhone } = require('./mask_utils');

maskPhone('13812345678');  // '138****5678'
maskPhone('13812345678', { maskChar: 'x' });  // '138xxxx5678'
maskPhone('13812345678', { showFirst: 2, showLast: 3 });  // '13******678'
```

#### maskIdCard(idCard, options?)
身份证号脱敏

```javascript
maskIdCard('110101199001011234');  // '110101********1234'
```

#### maskBankCard(bankCard, options?)
银行卡号脱敏

```javascript
maskBankCard('6222021234567890123');  // '6222 **** **** 0123'
```

#### maskEmail(email, options?)
邮箱脱敏

```javascript
maskEmail('example@domain.com');  // 'e*****@domain.com'
```

#### maskName(name, options?)
姓名脱敏

```javascript
maskName('张三');      // '张*'
maskName('张小明');    // '张**'
```

#### maskAddress(address, options?)
地址脱敏（保留省市区信息）

```javascript
maskAddress('北京市朝阳区望京街道');  // '北京市朝阳区****'
```

#### maskIP(ip, options?)
IP地址脱敏

```javascript
maskIP('192.168.1.100');  // '192.168.*.*'
```

#### maskCustom(str, showFirst, showLast, options?)
自定义脱敏

```javascript
maskCustom('abcdefghij', 2, 2);  // 'ab******ij'
```

### 格式化函数

#### formatBankCard(cardNumber, separator?)
银行卡号格式化

```javascript
formatBankCard('6222021234567890');  // '6222 0212 3456 7890'
formatBankCard('6222021234567890', '-');  // '6222-0212-3456-7890'
```

#### formatPhone(phone, separator?)
手机号格式化

```javascript
formatPhone('13812345678');  // '138 1234 5678'
```

#### formatAmount(amount, decimals?, separator?)
金额格式化（千分位）

```javascript
formatAmount(1234567.89);  // '1,234,567.89'
formatAmount(1234567.89, 4);  // '1,234,567.8900'
```

### 验证函数

#### validatePhone(phone)
验证手机号

```javascript
validatePhone('13812345678');  // true
validatePhone('12812345678');  // false (无效号段)
```

#### validateEmail(email)
验证邮箱

```javascript
validateEmail('test@example.com');  // true
validateEmail('invalid');  // false
```

#### validateIdCard(idCard)
验证身份证号（含校验位验证）

```javascript
validateIdCard('11010519491231002X');  // true
validateIdCard('110105194912310021');  // false (校验位错误)
```

#### validateBankCard(cardNumber)
验证银行卡号（Luhn算法）

```javascript
validateBankCard('4532015112830366');  // true
validateBankCard('1234567890123456');  // false
```

#### validateCreditCard(cardNumber)
验证信用卡号并识别卡类型

```javascript
validateCreditCard('4532015112830366');
// { valid: true, type: 'Visa' }

validateCreditCard('5500000000000004');
// { valid: true, type: 'MasterCard' }
```

#### validateIP(ip)
验证IP地址

```javascript
validateIP('192.168.1.1');  // true
validateIP('256.1.1.1');  // false
```

### 文本脱敏

#### maskPhoneInText(text, options?)
从文本中提取并脱敏手机号

```javascript
maskPhoneInText('联系13812345678或13987654321');
// '联系138****5678或139****4321'
```

#### maskEmailInText(text, options?)
从文本中提取并脱敏邮箱

#### maskIdCardInText(text, options?)
从文本中提取并脱敏身份证号

### 批量脱敏

#### maskBatch(data, rules)
批量脱敏数据对象

```javascript
const data = {
    phone: '13812345678',
    email: 'test@example.com',
    name: '张三'
};
const rules = {
    phone: 'phone',
    email: 'email',
    name: 'name'
};
const result = maskBatch(data, rules);
// {
//   phone: '138****5678',
//   email: 't***@example.com',
//   name: '张*'
// }
```

## 使用示例

```javascript
const maskUtils = require('./mask_utils');

// 用户信息脱敏
const userInfo = {
    name: '张小明',
    phone: '13812345678',
    idCard: '110101199001011234',
    email: 'zhangxiaoming@example.com',
    bankCard: '6222021234567890123',
    address: '北京市朝阳区望京街道'
};

console.log('姓名:', maskUtils.maskName(userInfo.name));
// 姓名: 张**

console.log('手机:', maskUtils.maskPhone(userInfo.phone));
// 手机: 138****5678

console.log('身份证:', maskUtils.maskIdCard(userInfo.idCard));
// 身份证: 110101********1234

console.log('邮箱:', maskUtils.maskEmail(userInfo.email));
// 邮箱: z***********@example.com

console.log('银行卡:', maskUtils.maskBankCard(userInfo.bankCard));
// 银行卡: 6222 **** **** 0123

console.log('地址:', maskUtils.maskAddress(userInfo.address));
// 地址: 北京市朝阳区********

// 批量脱敏
const maskedData = maskUtils.maskBatch(userInfo, {
    name: 'name',
    phone: 'phone',
    idCard: 'idCard',
    email: 'email',
    bankCard: 'bankCard',
    address: 'address'
});

// 验证
console.log(maskUtils.validatePhone('13812345678'));  // true
console.log(maskUtils.validateEmail('test@example.com'));  // true
console.log(maskUtils.validateIdCard('11010519491231002X'));  // true

// 信用卡验证
const ccResult = maskUtils.validateCreditCard('4532015112830366');
console.log(ccResult);  // { valid: true, type: 'Visa' }

// 格式化
console.log(maskUtils.formatBankCard('6222021234567890123'));
// 6222 0212 3456 7890 123

console.log(maskUtils.formatAmount(1234567.89));
// 1,234,567.89
```

## 选项参数

```javascript
{
    maskChar: '*',    // 脱敏字符，默认 '*'
    showFirst: 3,     // 显示前几位
    showLast: 4,      // 显示后几位
    separator: ' '    // 分隔符（格式化函数）
}
```

## 测试

```bash
node mask_utils.test.js
```

## 许可证

MIT License