/**
 * Validator Utils - 使用示例
 * 
 * 本文件展示 validator_utils 模块的各种使用场景
 */

import {
  validateEmail,
  validatePhone,
  validateUrl,
  validateIPv4,
  validateChineseIdCard,
  validateCreditCard,
  validateDate,
  validateString,
  validateFields,
  allValid,
  getFirstError,
} from '../validator_utils.ts';

// =============================================================================
// 示例 1: 用户注册表单验证
// =============================================================================

console.log('=== 示例 1: 用户注册表单验证 ===\n');

interface RegistrationForm {
  email: string;
  phone: string;
  password: string;
}

function validateRegistrationForm(form: RegistrationForm): { valid: boolean; errors: Record<string, string> } {
  const results = validateFields({
    email: () => validateEmail(form.email),
    phone: () => validatePhone(form.phone, { countryCode: 'CN', allowInternational: true }),
    password: () => validateString(form.password, { minLength: 8, maxLength: 32 }),
  });

  const errors: Record<string, string> = {};
  
  if (!results.email.valid && results.email.error) {
    errors.email = results.email.error;
  }
  
  if (!results.phone.valid && results.phone.error) {
    errors.phone = results.phone.error;
  }
  
  if (!results.password.valid && results.password.error) {
    errors.password = results.password.error;
  }

  return {
    valid: allValid(Object.values(results)),
    errors,
  };
}

// 测试有效表单
const validForm: RegistrationForm = {
  email: 'user@example.com',
  phone: '13800138000',
  password: 'SecurePass123',
};

const validResult = validateRegistrationForm(validForm);
console.log('有效表单验证:', validResult);

// 测试无效表单
const invalidForm: RegistrationForm = {
  email: 'invalid-email',
  phone: '12345',
  password: '123',
};

const invalidResult = validateRegistrationForm(invalidForm);
console.log('无效表单验证:', invalidResult);

// =============================================================================
// 示例 2: 联系方式验证
// =============================================================================

console.log('\n=== 示例 2: 联系方式验证 ===\n');

function validateContactInfo(email: string, phone: string, website?: string): void {
  console.log(`验证联系方式: ${email}, ${phone}${website ? ', ' + website : ''}`);
  
  // 邮箱验证
  const emailResult = validateEmail(email);
  if (emailResult.valid) {
    console.log(`  ✓ 邮箱有效 (本地部分：${emailResult.data?.local}, 域名：${emailResult.data?.domain})`);
  } else {
    console.log(`  ✗ 邮箱无效：${emailResult.error}`);
  }
  
  // 电话验证
  const phoneResult = validatePhone(phone, { 
    countryCode: 'CN', 
    allowInternational: true 
  });
  if (phoneResult.valid) {
    console.log(`  ✓ 电话有效`);
  } else {
    console.log(`  ✗ 电话无效：${phoneResult.error}`);
  }
  
  // 网站验证（可选）
  if (website) {
    const urlResult = validateUrl(website);
    if (urlResult.valid) {
      console.log(`  ✓ 网站有效 (协议：${urlResult.data?.protocol}, 主机：${urlResult.data?.host})`);
    } else {
      console.log(`  ✗ 网站无效：${urlResult.error}`);
    }
  }
}

validateContactInfo('john.doe@company.com', '+86-138-0013-8000', 'https://company.com');
validateContactInfo('invalid', '123', 'not-a-url');

// =============================================================================
// 示例 3: 身份证和支付信息验证
// =============================================================================

console.log('\n=== 示例 3: 身份证和支付信息验证 ===\n');

function validateUserIdentity(idCard: string, cardNumber?: string): void {
  console.log(`验证身份信息：${idCard}${cardNumber ? ', ' + cardNumber : ''}`);
  
  // 身份证验证
  const idResult = validateChineseIdCard(idCard);
  if (idResult.valid && idResult.data) {
    console.log(`  ✓ 身份证有效`);
    console.log(`    - 出生日期：${idResult.data.birthdate}`);
    console.log(`    - 地区代码：${idResult.data.regionCode}`);
    console.log(`    - 性别：${idResult.data.gender}`);
  } else {
    console.log(`  ✗ 身份证无效：${idResult.error}`);
  }
  
  // 信用卡验证（可选）
  if (cardNumber) {
    const cardResult = validateCreditCard(cardNumber);
    if (cardResult.valid && cardResult.data) {
      console.log(`  ✓ 信用卡有效`);
      console.log(`    - 发卡行：${cardResult.data.issuer}`);
      console.log(`    - 卡号后四位：${cardResult.data.lastFour}`);
    } else {
      console.log(`  ✗ 信用卡无效：${cardResult.error}`);
    }
  }
}

// 注意：以下使用测试数据，实际应用中请使用真实数据
validateUserIdentity('110101199001011234');
validateUserIdentity('110101199001011234', '4532015112830366');

// =============================================================================
// 示例 4: 日期范围验证
// =============================================================================

console.log('\n=== 示例 4: 日期范围验证 ===\n');

function validateBookingDates(checkIn: string, checkOut: string): void {
  console.log(`验证预订日期：入住 ${checkIn}, 退房 ${checkOut}`);
  
  const today = new Date();
  const nextMonth = new Date(today.getFullYear(), today.getMonth() + 1, today.getDate());
  
  // 验证入住日期
  const checkInResult = validateDate(checkIn, {
    format: 'YYYY-MM-DD',
    min: today,
    max: nextMonth,
  });
  
  if (checkInResult.valid && checkInResult.data) {
    console.log(`  ✓ 入住日期有效 (${checkInResult.data.dayOfWeek})`);
  } else {
    console.log(`  ✗ 入住日期无效：${checkInResult.error}`);
  }
  
  // 验证退房日期
  const checkOutResult = validateDate(checkOut, {
    format: 'YYYY-MM-DD',
    min: today,
    max: nextMonth,
  });
  
  if (checkOutResult.valid) {
    console.log(`  ✓ 退房日期有效`);
  } else {
    console.log(`  ✗ 退房日期无效：${checkOutResult.error}`);
  }
}

validateBookingDates('2024-06-15', '2024-06-20');
validateBookingDates('2020-01-01', '2020-01-05'); // 过去日期

// =============================================================================
// 示例 5: IP 地址和网络验证
// =============================================================================

console.log('\n=== 示例 5: IP 地址和网络验证 ===\n');

function validateNetworkConfig(ip: string, gateway?: string, dns?: string): void {
  console.log(`验证网络配置：IP ${ip}${gateway ? ', 网关 ' + gateway : ''}${dns ? ', DNS ' + dns : ''}`);
  
  // 验证 IP 地址
  const ipResult = validateIPv4(ip);
  if (ipResult.valid && ipResult.data) {
    console.log(`  ✓ IP 地址有效`);
    console.log(`    - 版本：IPv${ipResult.data.version}`);
    console.log(`    - 类型：${ipResult.data.isPrivate ? '私有地址' : '公有地址'}`);
  } else {
    console.log(`  ✗ IP 地址无效：${ipResult.error}`);
  }
  
  // 验证网关（如果提供）
  if (gateway) {
    const gatewayResult = validateIPv4(gateway);
    if (gatewayResult.valid) {
      console.log(`  ✓ 网关地址有效`);
    } else {
      console.log(`  ✗ 网关地址无效：${gatewayResult.error}`);
    }
  }
  
  // 验证 DNS（如果提供）
  if (dns) {
    const dnsResult = validateIPv4(dns);
    if (dnsResult.valid) {
      console.log(`  ✓ DNS 地址有效`);
    } else {
      console.log(`  ✗ DNS 地址无效：${dnsResult.error}`);
    }
  }
}

validateNetworkConfig('192.168.1.100', '192.168.1.1', '8.8.8.8');
validateNetworkConfig('10.0.0.50');
validateNetworkConfig('256.1.1.1'); // 无效 IP

// =============================================================================
// 示例 6: 密码强度验证（使用模式匹配）
// =============================================================================

console.log('\n=== 示例 6: 密码强度验证 ===\n');

function validatePasswordStrength(password: string): { valid: boolean; strength: string; issues: string[] } {
  const issues: string[] = [];
  
  // 长度检查
  const lengthResult = validateString(password, { minLength: 8 });
  if (!lengthResult.valid) {
    issues.push('密码长度至少 8 位');
  }
  
  // 包含大写字母
  if (!/[A-Z]/.test(password)) {
    issues.push('密码需包含大写字母');
  }
  
  // 包含小写字母
  if (!/[a-z]/.test(password)) {
    issues.push('密码需包含小写字母');
  }
  
  // 包含数字
  if (!/\d/.test(password)) {
    issues.push('密码需包含数字');
  }
  
  // 包含特殊字符
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    issues.push('密码需包含特殊字符');
  }
  
  // 计算强度
  let strength = '弱';
  if (issues.length === 0) {
    strength = '强';
  } else if (issues.length <= 2) {
    strength = '中';
  }
  
  return {
    valid: issues.length === 0,
    strength,
    issues,
  };
}

const passwords = ['weak', 'Medium1', 'Str0ng@Pass'];
for (const pwd of passwords) {
  const result = validatePasswordStrength(pwd);
  console.log(`密码 "${pwd}": 强度=${result.strength}`);
  if (result.issues.length > 0) {
    console.log(`  改进建议：${result.issues.join(', ')}`);
  }
}

// =============================================================================
// 示例 7: 批量数据验证
// =============================================================================

console.log('\n=== 示例 7: 批量数据验证 ===\n');

interface UserData {
  id: number;
  name: string;
  email: string;
  phone: string;
}

const users: UserData[] = [
  { id: 1, name: '张三', email: 'zhangsan@example.com', phone: '13800138000' },
  { id: 2, name: '李四', email: 'invalid-email', phone: '12345' },
  { id: 3, name: '王五', email: 'wangwu@company.cn', phone: '13900139000' },
];

function validateUserBatch(users: UserData[]): void {
  console.log(`批量验证 ${users.length} 个用户数据:\n`);
  
  let validCount = 0;
  let invalidCount = 0;
  
  for (const user of users) {
    const results = validateFields({
      name: () => validateString(user.name, { minLength: 2, maxLength: 20 }),
      email: () => validateEmail(user.email),
      phone: () => validatePhone(user.phone, { countryCode: 'CN' }),
    });
    
    const allPassed = allValid(Object.values(results));
    
    if (allPassed) {
      console.log(`✓ 用户 ${user.id} (${user.name}): 验证通过`);
      validCount++;
    } else {
      const error = getFirstError(Object.values(results));
      console.log(`✗ 用户 ${user.id} (${user.name}): ${error}`);
      invalidCount++;
    }
  }
  
  console.log(`\n验证完成：${validCount} 通过，${invalidCount} 失败`);
}

validateUserBatch(users);

// =============================================================================
// 示例 8: 时间和时区验证
// =============================================================================

console.log('\n=== 示例 8: 时间验证 ===\n');

function validateMeetingTime(time: string, format: 'HH:mm:ss' | 'HH:mm' | '12h'): void {
  console.log(`验证会议时间：${time} (${format})`);
  
  const result = validateTime(time, format);
  
  if (result.valid && result.data) {
    console.log(`  ✓ 时间有效`);
    console.log(`    - 24 小时制：${result.data.hour.toString().padStart(2, '0')}:${result.data.minute.toString().padStart(2, '0')}`);
    console.log(`    - 12 小时制：${result.data.hour12}:${result.data.minute.toString().padStart(2, '0')} ${result.data.ampm}`);
    console.log(`    - 总秒数：${result.data.seconds}秒`);
  } else {
    console.log(`  ✗ 时间无效：${result.error}`);
  }
}

validateMeetingTime('09:30:00', 'HH:mm:ss');
validateMeetingTime('2:30 PM', '12h');
validateMeetingTime('25:00', 'HH:mm'); // 无效时间

console.log('\n=== 所有示例执行完成 ===\n');
