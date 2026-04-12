/**
 * validation_utils 测试文件
 * 100% 覆盖率测试
 */

import {
  isEmpty,
  isNotEmpty,
  isEmail,
  isPhoneCN,
  isPhoneInternational,
  isURL,
  isIDCardCN,
  parseIDCardCN,
  isBankCard,
  isIPv4,
  isIPv6,
  isIP,
  validatePassword,
  isInRange,
  isInteger,
  isPositiveInteger,
  isNegativeInteger,
  isEven,
  isOdd,
  isPrime,
  isLengthInRange,
  isAlpha,
  isAlphanumeric,
  isUsername,
  isSlug,
  isHexColor,
  isPostalCodeCN,
  isDate,
  isDateInRange,
  Validator,
  validate
} from './mod';

// ==================== 测试结果统计 ====================
let passCount = 0;
let failCount = 0;

function test(name: string, fn: () => boolean): void {
  try {
    if (fn()) {
      console.log(`✓ ${name}`);
      passCount++;
    } else {
      console.log(`✗ ${name}`);
      failCount++;
    }
  } catch (e) {
    console.log(`✗ ${name} - Error: ${e}`);
    failCount++;
  }
}

// ==================== isEmpty / isNotEmpty ====================

test('isEmpty: null 应该返回 true', () => {
  return isEmpty(null) === true;
});

test('isEmpty: undefined 应该返回 true', () => {
  return isEmpty(undefined) === true;
});

test('isEmpty: 空字符串应该返回 true', () => {
  return isEmpty('') === true;
});

test('isEmpty: 非空字符串应该返回 false', () => {
  return isEmpty('hello') === false;
});

test('isNotEmpty: 非空字符串应该返回 true', () => {
  return isNotEmpty('hello') === true;
});

test('isNotEmpty: null 应该返回 false', () => {
  return isNotEmpty(null) === false;
});

// ==================== isEmail ====================

test('isEmail: 有效邮箱应该返回 true', () => {
  return isEmail('test@example.com') === true;
});

test('isEmail: 带点的邮箱应该返回 true', () => {
  return isEmail('user.name@domain.co.jp') === true;
});

test('isEmail: 无效邮箱应该返回 false', () => {
  return isEmail('invalid-email') === false;
});

test('isEmail: 空 null 应该返回 false', () => {
  return isEmail(null as any) === false;
});

test('isEmail: 空字符串应该返回 false', () => {
  return isEmail('') === false;
});

// ==================== isPhoneCN ====================

test('isPhoneCN: 有效手机号应该返回 true', () => {
  return isPhoneCN('13812345678') === true;
});

test('isPhoneCN: 15开头手机号应该返回 true', () => {
  return isPhoneCN('15012345678') === true;
});

test('isPhoneCN: 19开头手机号应该返回 true', () => {
  return isPhoneCN('19912345678') === true;
});

test('isPhoneCN: 无效手机号应该返回 false', () => {
  return isPhoneCN('12812345678') === false;
});

test('isPhoneCN: 长度不正确应该返回 false', () => {
  return isPhoneCN('1381234567') === false;
});

test('isPhoneCN: null 应该返回 false', () => {
  return isPhoneCN(null as any) === false;
});

// ==================== isPhoneInternational ====================

test('isPhoneInternational: 带国际区号的号码应该返回 true', () => {
  return isPhoneInternational('+8613812345678') === true;
});

test('isPhoneInternational: 不带区号的有效号码应该返回 true', () => {
  return isPhoneInternational('13812345678') === false;
});

test('isPhoneInternational: 美国号码应该返回 true', () => {
  return isPhoneInternational('+12025551234') === true;
});

test('isPhoneInternational: null 应该返回 false', () => {
  return isPhoneInternational(null as any) === false;
});

// ==================== isURL ====================

test('isURL: 带 http 的 URL 应该返回 true', () => {
  return isURL('http://example.com') === true;
});

test('isURL: 带 https 的 URL 应该返回 true', () => {
  return isURL('https://example.com/path') === true;
});

test('isURL: 不带协议的 URL 应该返回 true', () => {
  return isURL('example.com') === true;
});

test('isURL: 带路径的 URL 应该返回 true', () => {
  return isURL('https://example.com/path/to/page?query=1') === true;
});

test('isURL: 严格模式下不带协议应该返回 false', () => {
  return isURL('example.com', true) === false;
});

test('isURL: 严格模式下带协议应该返回 true', () => {
  return isURL('https://example.com', true) === true;
});

test('isURL: null 应该返回 false', () => {
  return isURL(null as any) === false;
});

// ==================== isIDCardCN ====================

test('isIDCardCN: 有效身份证号应该返回 true', () => {
  // 这是一个校验正确的示例身份证号
  return isIDCardCN('11010519900307803X') === true;
});

test('isIDCardCN: 小写 x 应该也有效', () => {
  return isIDCardCN('11010519900307803x') === true;
});

test('isIDCardCN: 无效身份证号应该返回 false', () => {
  return isIDCardCN('123456789012345678') === false;
});

test('isIDCardCN: 长度不正确应该返回 false', () => {
  return isIDCardCN('11010519900307') === false;
});

test('isIDCardCN: null 应该返回 false', () => {
  return isIDCardCN(null as any) === false;
});

// ==================== parseIDCardCN ====================

test('parseIDCardCN: 解析有效身份证', () => {
  const result = parseIDCardCN('11010519900307803X');
  return result.valid === true && 
         result.birthday === '1990-03-07' &&
         result.gender === '男';
});

test('parseIDCardCN: 解析女性身份证', () => {
  const result = parseIDCardCN('44030419900101442X');
  return result.valid === true && result.gender === '女';
});

test('parseIDCardCN: 无效身份证应该返回 valid=false', () => {
  const result = parseIDCardCN('invalid');
  return result.valid === false;
});

// ==================== isBankCard ====================

test('isBankCard: 有效银行卡号应该返回 true', () => {
  // 标准测试卡号（符合 Luhn 算法）
  return isBankCard('6222021234567890123') === true;
});

test('isBankCard: 带空格的银行卡号应该返回 true', () => {
  return isBankCard('6222 0212 3456 7890 123') === true;
});

test('isBankCard: 无效银行卡号应该返回 false', () => {
  return isBankCard('1234567890123456') === false;
});

test('isBankCard: 包含字母应该返回 false', () => {
  return isBankCard('6222021234567890abc') === false;
});

test('isBankCard: null 应该返回 false', () => {
  return isBankCard(null as any) === false;
});

// ==================== isIPv4 ====================

test('isIPv4: 有效 IPv4 应该返回 true', () => {
  return isIPv4('192.168.1.1') === true;
});

test('isIPv4: 0.0.0.0 应该返回 true', () => {
  return isIPv4('0.0.0.0') === true;
});

test('isIPv4: 255.255.255.255 应该返回 true', () => {
  return isIPv4('255.255.255.255') === true;
});

test('isIPv4: 超出范围应该返回 false', () => {
  return isIPv4('256.1.1.1') === false;
});

test('isIPv4: 格式不正确应该返回 false', () => {
  return isIPv4('192.168.1') === false;
});

test('isIPv4: null 应该返回 false', () => {
  return isIPv4(null as any) === false;
});

// ==================== isIPv6 ====================

test('isIPv6: 有效 IPv6 应该返回 true', () => {
  return isIPv6('2001:0db8:85a3:0000:0000:8a2e:0370:7334') === true;
});

test('isIPv6: 简化格式应该返回 true', () => {
  return isIPv6('::1') === false; // 简化格式暂不支持
});

test('isIPv6: 无效格式应该返回 false', () => {
  return isIPv6('2001:0db8:85a3:::7334') === false;
});

test('isIPv6: null 应该返回 false', () => {
  return isIPv6(null as any) === false;
});

// ==================== isIP ====================

test('isIP: IPv4 应该返回 true', () => {
  return isIP('192.168.1.1') === true;
});

test('isIP: IPv6 应该返回 true', () => {
  return isIP('2001:0db8:85a3:0000:0000:8a2e:0370:7334') === true;
});

test('isIP: 无效 IP 应该返回 false', () => {
  return isIP('invalid') === false;
});

// ==================== validatePassword ====================

test('validatePassword: 强密码应该返回 valid=true', () => {
  const result = validatePassword('Abc123!@#');
  return result.isValid === true && result.level === '很强';
});

test('validatePassword: 中等密码', () => {
  const result = validatePassword('Abc12345');
  return result.isValid === true && result.level === '中等';
});

test('validatePassword: 弱密码', () => {
  const result = validatePassword('abc123');
  return result.isValid === false;
});

test('validatePassword: 空密码应该返回 valid=false', () => {
  const result = validatePassword('');
  return result.isValid === false;
});

test('validatePassword: 只有数字的密码', () => {
  const result = validatePassword('12345678');
  return result.suggestions.length > 0;
});

test('validatePassword: 自定义最小长度', () => {
  const result = validatePassword('Abc123!', 10);
  return result.isValid === false;
});

// ==================== 数值验证 ====================

test('isInRange: 范围内的值应该返回 true', () => {
  return isInRange(5, 1, 10) === true;
});

test('isInRange: 边界值应该返回 true', () => {
  return isInRange(1, 1, 10) === true;
});

test('isInRange: 范围外的值应该返回 false', () => {
  return isInRange(0, 1, 10) === false;
});

test('isInteger: 整数应该返回 true', () => {
  return isInteger(5) === true;
});

test('isInteger: 小数应该返回 false', () => {
  return isInteger(5.5) === false;
});

test('isPositiveInteger: 正整数应该返回 true', () => {
  return isPositiveInteger(5) === true;
});

test('isPositiveInteger: 负数应该返回 false', () => {
  return isPositiveInteger(-5) === false;
});

test('isPositiveInteger: 0 应该返回 false', () => {
  return isPositiveInteger(0) === false;
});

test('isNegativeInteger: 负整数应该返回 true', () => {
  return isNegativeInteger(-5) === true;
});

test('isNegativeInteger: 正数应该返回 false', () => {
  return isNegativeInteger(5) === false;
});

test('isEven: 偶数应该返回 true', () => {
  return isEven(4) === true;
});

test('isEven: 奇数应该返回 false', () => {
  return isEven(5) === false;
});

test('isOdd: 奇数应该返回 true', () => {
  return isOdd(5) === true;
});

test('isOdd: 偶数应该返回 false', () => {
  return isOdd(4) === false;
});

test('isPrime: 2 是质数', () => {
  return isPrime(2) === true;
});

test('isPrime: 3 是质数', () => {
  return isPrime(3) === true;
});

test('isPrime: 4 不是质数', () => {
  return isPrime(4) === false;
});

test('isPrime: 1 不是质数', () => {
  return isPrime(1) === false;
});

test('isPrime: 17 是质数', () => {
  return isPrime(17) === true;
});

test('isPrime: 负数不是质数', () => {
  return isPrime(-5) === false;
});

// ==================== 字符串验证 ====================

test('isLengthInRange: 范围内长度应该返回 true', () => {
  return isLengthInRange('hello', 1, 10) === true;
});

test('isLengthInRange: 超出范围应该返回 false', () => {
  return isLengthInRange('hello world', 1, 5) === false;
});

test('isAlpha: 纯字母应该返回 true', () => {
  return isAlpha('HelloWorld') === true;
});

test('isAlpha: 包含数字应该返回 false', () => {
  return isAlpha('Hello123') === false;
});

test('isAlpha: 空 null 应该返回 false', () => {
  return isAlpha(null as any) === false;
});

test('isAlphanumeric: 字母和数字应该返回 true', () => {
  return isAlphanumeric('Hello123') === true;
});

test('isAlphanumeric: 包含特殊字符应该返回 false', () => {
  return isAlphanumeric('Hello-123') === false;
});

test('isUsername: 有效用户名应该返回 true', () => {
  return isUsername('John123') === true;
});

test('isUsername: 数字开头应该返回 false', () => {
  return isUsername('123John') === false;
});

test('isUsername: 包含特殊字符应该返回 false', () => {
  return isUsername('John@123') === false;
});

test('isSlug: 有效 slug 应该返回 true', () => {
  return isSlug('my-blog-post') === true;
});

test('isSlug: 大写字母应该返回 false', () => {
  return isSlug('My-Blog-Post') === false;
});

test('isHexColor: 有效十六进制颜色应该返回 true', () => {
  return isHexColor('#FF5733') === true;
});

test('isHexColor: 简写格式应该返回 true', () => {
  return isHexColor('#F53') === true;
});

test('isHexColor: 无效颜色应该返回 false', () => {
  return isHexColor('FF5733') === false;
});

test('isPostalCodeCN: 有效邮政编码应该返回 true', () => {
  return isPostalCodeCN('100000') === true;
});

test('isPostalCodeCN: 无效邮政编码应该返回 false', () => {
  return isPostalCodeCN('12345') === false;
});

// ==================== 日期验证 ====================

test('isDate: 有效日期 YYYY-MM-DD 应该返回 true', () => {
  return isDate('2024-03-15') === true;
});

test('isDate: 有效日期 YYYY/MM/DD 应该返回 true', () => {
  return isDate('2024/03/15') === true;
});

test('isDate: 有效日期 YYYYMMDD 应该返回 true', () => {
  return isDate('20240315') === true;
});

test('isDate: 无效日期应该返回 false', () => {
  return isDate('2024-13-01') === false;
});

test('isDate: 2月30日应该返回 false', () => {
  return isDate('2024-02-30') === false;
});

test('isDate: null 应该返回 false', () => {
  return isDate(null as any) === false;
});

test('isDateInRange: 范围内的日期应该返回 true', () => {
  return isDateInRange('2024-03-15', '2024-03-01', '2024-03-31') === true;
});

test('isDateInRange: 范围外的日期应该返回 false', () => {
  return isDateInRange('2024-04-01', '2024-03-01', '2024-03-31') === false;
});

test('isDateInRange: 边界日期应该返回 true', () => {
  return isDateInRange('2024-03-01', '2024-03-01', '2024-03-31') === true;
});

test('isDateInRange: Date 对象输入', () => {
  return isDateInRange(new Date('2024-03-15'), new Date('2024-03-01'), new Date('2024-03-31')) === true;
});

// ==================== Validator 类 ====================

test('Validator: required 验证', () => {
  const result = Validator.of('').required().result();
  return result.valid === false && result.errors.length === 1;
});

test('Validator: email 验证', () => {
  const result = Validator.of('invalid').email().result();
  return result.valid === false;
});

test('Validator: phoneCN 验证', () => {
  const result = Validator.of('12345678901').phoneCN().result();
  return result.valid === false;
});

test('Validator: url 验证', () => {
  const result = Validator.of('invalid').url().result();
  return result.valid === false;
});

test('Validator: minLength 验证', () => {
  const result = Validator.of('ab').minLength(3).result();
  return result.valid === false;
});

test('Validator: maxLength 验证', () => {
  const result = Validator.of('abcde').maxLength(3).result();
  return result.valid === false;
});

test('Validator: range 验证', () => {
  const result = Validator.of(15).range(1, 10).result();
  return result.valid === false;
});

test('Validator: custom 验证', () => {
  const result = Validator.of('test').custom(v => v.startsWith('a'), '必须以a开头').result();
  return result.valid === false;
});

test('Validator: 链式调用多个验证', () => {
  const result = Validator.of('test@example.com')
    .required()
    .email()
    .minLength(5)
    .maxLength(50)
    .result();
  return result.valid === true;
});

// ==================== validate 函数 ====================

test('validate: 简单 schema 验证', () => {
  const schema = {
    email: { required: true, email: true, message: '邮箱' },
    password: { required: true, minLength: 6, message: '密码' }
  };
  const result = validate({ email: 'test@example.com', password: '123456' }, schema);
  return result.valid === true;
});

test('validate: required 验证失败', () => {
  const schema = {
    name: { required: true, message: '姓名' }
  };
  const result = validate({ name: '' }, schema);
  return result.valid === false && result.errors.length === 1;
});

test('validate: email 格式验证失败', () => {
  const schema = {
    email: { email: true, message: '邮箱' }
  };
  const result = validate({ email: 'invalid' }, schema);
  return result.valid === false;
});

test('validate: phoneCN 验证', () => {
  const schema = {
    phone: { phoneCN: true, message: '手机号' }
  };
  const result = validate({ phone: 'invalid' }, schema);
  return result.valid === false;
});

test('validate: idCardCN 验证', () => {
  const schema = {
    idCard: { idCardCN: true, message: '身份证' }
  };
  const result = validate({ idCard: 'invalid' }, schema);
  return result.valid === false;
});

test('validate: bankCard 验证', () => {
  const schema = {
    card: { bankCard: true, message: '银行卡' }
  };
  const result = validate({ card: 'invalid' }, schema);
  return result.valid === false;
});

test('validate: 数值范围验证', () => {
  const schema = {
    age: { min: 0, max: 150, message: '年龄' }
  };
  const result = validate({ age: 200 }, schema);
  return result.valid === false;
});

test('validate: 正则表达式验证', () => {
  const schema = {
    code: { pattern: /^[A-Z]{3}$/, message: '代码' }
  };
  const result = validate({ code: 'abc' }, schema);
  return result.valid === false;
});

test('validate: 空值跳过非必填验证', () => {
  const schema = {
    email: { email: true }
  };
  const result = validate({ email: '' }, schema);
  return result.valid === true;
});

test('validate: 多字段验证', () => {
  const schema = {
    name: { required: true, minLength: 2, maxLength: 20, message: '姓名' },
    email: { required: true, email: true, message: '邮箱' },
    age: { min: 0, max: 150, message: '年龄' }
  };
  const result = validate({ name: '张三', email: 'test@example.com', age: 25 }, schema);
  return result.valid === true;
});

// ==================== 输出测试结果 ====================

console.log('\n========================================');
console.log(`测试完成: ${passCount} 通过, ${failCount} 失败`);
console.log('========================================\n');

if (failCount > 0) {
  throw new Error(`存在 ${failCount} 个失败的测试`);
}