/**
 * validation_utils 使用示例
 * 展示各种验证功能的使用方法
 */

import {
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
  isPrime,
  isAlpha,
  isAlphanumeric,
  isUsername,
  isHexColor,
  isPostalCodeCN,
  isDate,
  isDateInRange,
  Validator,
  validate
} from '../validation_utils/mod';

// ==================== 基础验证示例 ====================

console.log('========== 基础验证示例 ==========\n');

// 邮箱验证
const emails = ['user@example.com', 'invalid-email', 'user.name@domain.co.jp'];
emails.forEach(email => {
  console.log(`邮箱 "${email}" 验证结果: ${isEmail(email)}`);
});

// 手机号验证
console.log('\n--- 手机号验证 ---');
const phones = ['13812345678', '19912345678', '12812345678', '+8613812345678'];
phones.forEach(phone => {
  console.log(`手机号 "${phone}":`);
  console.log(`  中国大陆: ${isPhoneCN(phone)}`);
  console.log(`  国际格式: ${isPhoneInternational(phone)}`);
});

// URL 验证
console.log('\n--- URL 验证 ---');
const urls = [
  'https://example.com',
  'http://test.com/path?query=1',
  'example.com',
  'ftp://files.example.com'
];
urls.forEach(url => {
  console.log(`URL "${url}" 验证结果: ${isURL(url)}`);
});

// ==================== 身份证验证示例 ====================

console.log('\n========== 身份证验证示例 ==========\n');

const idCards = ['11010519900307803X', '44030419900101442X', 'invalid'];
idCards.forEach(idCard => {
  const valid = isIDCardCN(idCard);
  console.log(`身份证 "${idCard}" 验证结果: ${valid}`);
  
  if (valid) {
    const info = parseIDCardCN(idCard);
    console.log(`  生日: ${info.birthday}`);
    console.log(`  性别: ${info.gender}`);
    console.log(`  省份: ${info.province}`);
  }
});

// ==================== 银行卡验证示例 ====================

console.log('\n========== 银行卡验证示例 ==========\n');

const cards = ['6222021234567890123', '6222 0212 3456 7890 123', '1234567890'];
cards.forEach(card => {
  console.log(`银行卡 "${card}" 验证结果: ${isBankCard(card)}`);
});

// ==================== IP 地址验证示例 ====================

console.log('\n========== IP 地址验证示例 ==========\n');

const ips = ['192.168.1.1', '255.255.255.255', '256.1.1.1', '2001:0db8:85a3:0000:0000:8a2e:0370:7334'];
ips.forEach(ip => {
  console.log(`IP "${ip}":`);
  console.log(`  IPv4: ${isIPv4(ip)}`);
  console.log(`  IPv6: ${isIPv6(ip)}`);
  console.log(`  任意: ${isIP(ip)}`);
});

// ==================== 密码强度验证示例 ====================

console.log('\n========== 密码强度验证示例 ==========\n');

const passwords = ['123456', 'abc12345', 'Abc12345', 'Abc123!@#'];
passwords.forEach(pwd => {
  const result = validatePassword(pwd);
  console.log(`密码 "${pwd}":`);
  console.log(`  强度: ${result.level}`);
  console.log(`  有效: ${result.isValid}`);
  if (result.suggestions.length > 0) {
    console.log(`  建议: ${result.suggestions.join(', ')}`);
  }
});

// ==================== 数值验证示例 ====================

console.log('\n========== 数值验证示例 ==========\n');

const numbers = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23];
console.log('质数检测:');
numbers.forEach(n => {
  if (isPrime(n)) {
    console.log(`  ${n} 是质数`);
  }
});

console.log('\n范围检测:');
console.log(`5 在 1-10 范围内: ${isInRange(5, 1, 10)}`);
console.log(`15 在 1-10 范围内: ${isInRange(15, 1, 10)}`);

console.log('\n奇偶检测:');
[1, 2, 3, 4, 5].forEach(n => {
  console.log(`  ${n}: ${isEven(n) ? '偶数' : '奇数'}`);
});

// ==================== 字符串验证示例 ====================

console.log('\n========== 字符串验证示例 ==========\n');

// 用户名验证
const usernames = ['John123', 'john_doe', '123John', 'j'];
usernames.forEach(username => {
  console.log(`用户名 "${username}" 验证结果: ${isUsername(username)}`);
});

// 颜色验证
console.log('\n--- 颜色验证 ---');
const colors = ['#FF5733', '#F53', '#1234567', 'FF5733'];
colors.forEach(color => {
  console.log(`颜色 "${color}" 验证结果: ${isHexColor(color)}`);
});

// 邮政编码验证
console.log('\n--- 邮政编码验证 ---');
const postalCodes = ['100000', '200001', '12345'];
postalCodes.forEach(code => {
  console.log(`邮政编码 "${code}" 验证结果: ${isPostalCodeCN(code)}`);
});

// ==================== 日期验证示例 ====================

console.log('\n========== 日期验证示例 ==========\n');

const dates = ['2024-03-15', '2024/03/15', '20240315', '2024-13-01', '2024-02-30'];
dates.forEach(date => {
  console.log(`日期 "${date}" 验证结果: ${isDate(date)}`);
});

// 日期范围验证
console.log('\n--- 日期范围验证 ---');
const startDate = '2024-03-01';
const endDate = '2024-03-31';
const testDates = ['2024-03-15', '2024-04-01', '2024-03-01'];
testDates.forEach(date => {
  console.log(`"${date}" 在范围内: ${isDateInRange(date, startDate, endDate)}`);
});

// ==================== 链式验证器示例 ====================

console.log('\n========== 链式验证器示例 ==========\n');

// 用户注册表单验证
const formData = {
  email: 'user@example.com',
  password: 'Abc123!@#',
  age: '25'
};

const emailResult = Validator.of(formData.email)
  .required('请输入邮箱')
  .email('邮箱格式不正确')
  .result();

const passwordResult = Validator.of(formData.password)
  .required('请输入密码')
  .minLength(8, '密码至少8位')
  .result();

const ageResult = Validator.of(formData.age)
  .required('请输入年龄')
  .range(1, 120, '年龄必须在1-120之间')
  .result();

console.log('邮箱验证:', emailResult.valid ? '通过' : emailResult.errors);
console.log('密码验证:', passwordResult.valid ? '通过' : passwordResult.errors);
console.log('年龄验证:', ageResult.valid ? '通过' : ageResult.errors);

// ==================== Schema 批量验证示例 ====================

console.log('\n========== Schema 批量验证示例 ==========\n');

// 注册表单验证
const registerSchema = {
  username: { 
    required: true, 
    minLength: 3, 
    maxLength: 16, 
    message: '用户名' 
  },
  email: { 
    required: true, 
    email: true, 
    message: '邮箱' 
  },
  phone: { 
    phoneCN: true, 
    message: '手机号' 
  },
  age: { 
    min: 1, 
    max: 120, 
    message: '年龄' 
  },
  idCard: { 
    idCardCN: true, 
    message: '身份证' 
  }
};

const validUser = {
  username: 'zhangsan',
  email: 'zhangsan@example.com',
  phone: '13812345678',
  age: 25,
  idCard: '11010519900307803X'
};

const invalidUser = {
  username: 'ab',
  email: 'invalid-email',
  phone: '12345',
  age: 200,
  idCard: 'invalid'
};

console.log('有效用户数据验证:');
const validResult = validate(validUser, registerSchema);
console.log('结果:', validResult.valid ? '通过' : validResult.errors);

console.log('\n无效用户数据验证:');
const invalidResult = validate(invalidUser, registerSchema);
console.log('结果:', invalidResult.valid ? '通过' : invalidResult.errors);

// ==================== 实际应用示例 ====================

console.log('\n========== 实际应用示例 ==========\n');

// 登录表单验证
function validateLoginForm(email: string, password: string): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  
  if (!isEmail(email)) {
    errors.push('请输入有效的邮箱地址');
  }
  
  const pwdResult = validatePassword(password);
  if (!pwdResult.isValid) {
    errors.push(`密码强度不足: ${pwdResult.suggestions.join(', ')}`);
  }
  
  return { valid: errors.length === 0, errors };
}

console.log('登录表单验证:');
const loginResult = validateLoginForm('user@example.com', 'weak');
console.log('结果:', loginResult.valid ? '通过' : loginResult.errors);

// 实名认证验证
function validateRealNameAuth(name: string, idCard: string): { valid: boolean; errors: string[]; info?: any } {
  const errors: string[] = [];
  
  if (name.length < 2 || name.length > 20) {
    errors.push('姓名长度应在2-20个字符之间');
  }
  
  if (!isIDCardCN(idCard)) {
    errors.push('身份证号格式不正确');
  } else {
    const info = parseIDCardCN(idCard);
    console.log(`实名认证信息: 生日=${info.birthday}, 性别=${info.gender}, 省份=${info.province}`);
    return { valid: true, errors: [], info };
  }
  
  return { valid: false, errors };
}

console.log('\n实名认证验证:');
const authResult = validateRealNameAuth('张三', '11010519900307803X');
console.log('结果:', authResult.valid ? '通过' : authResult.errors);

console.log('\n========== 示例结束 ==========');