package validation_utils;

import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

/**
 * ValidationUtils - 通用验证工具类
 * 
 * 提供常见的数据验证功能，包括：
 * - 邮箱、手机号、身份证等格式验证
 * - 字符串长度、范围验证
 * - 正则表达式验证
 * - 信用卡、IP地址等特殊格式验证
 * 
 * 零依赖，仅使用 Java 标准库
 * 
 * @author AllToolkit
 * @version 1.0.0
 */
public class ValidationUtils {
    
    // ==================== 正则表达式常量 ====================
    
    /** 邮箱验证正则（RFC 5322 简化版） */
    private static final Pattern EMAIL_PATTERN = Pattern.compile(
        "^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,}$"
    );
    
    /** 中国大陆手机号验证 */
    private static final Pattern CHINA_MOBILE_PATTERN = Pattern.compile(
        "^1[3-9]\\d{9}$"
    );
    
    /** IPv4 地址验证 */
    private static final Pattern IPV4_PATTERN = Pattern.compile(
        "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    );
    
    /** IPv6 地址验证（简化版） */
    private static final Pattern IPV6_PATTERN = Pattern.compile(
        "^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::1$|^::$"
    );
    
    /** URL 验证 */
    private static final Pattern URL_PATTERN = Pattern.compile(
        "^(https?|ftp)://[^\\s/$.?#].[^\\s]*$", Pattern.CASE_INSENSITIVE
    );
    
    /** 中国大陆身份证号验证（18位） */
    private static final Pattern CHINA_ID_CARD_PATTERN = Pattern.compile(
        "^[1-9]\\d{5}(?:18|19|20)\\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\\d|3[01])\\d{3}[\\dXx]$"
    );
    
    /** 信用卡号验证（Luhn算法预处理） */
    private static final Pattern CREDIT_CARD_PATTERN = Pattern.compile(
        "^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\\d{3})\\d{11})$"
    );
    
    /** 邮政编码验证（中国大陆） */
    private static final Pattern CHINA_ZIP_CODE_PATTERN = Pattern.compile(
        "^[1-9]\\d{5}$"
    );
    
    /** 日期格式验证（YYYY-MM-DD） */
    private static final Pattern DATE_PATTERN = Pattern.compile(
        "^(\\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12]\\d|3[01])$"
    );
    
    /** 时间格式验证（HH:MM:SS） */
    private static final Pattern TIME_PATTERN = Pattern.compile(
        "^([01]\\d|2[0-3]):([0-5]\\d):([0-5]\\d)$"
    );
    
    /** UUID 验证 */
    private static final Pattern UUID_PATTERN = Pattern.compile(
        "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
    );
    
    /** 十六进制颜色验证 */
    private static final Pattern HEX_COLOR_PATTERN = Pattern.compile(
        "^#(?:[0-9a-fA-F]{3}){1,2}$"
    );
    
    /** 纯数字验证 */
    private static final Pattern NUMERIC_PATTERN = Pattern.compile(
        "^-?\\d+$"
    );
    
    /** 纯字母验证 */
    private static final Pattern ALPHA_PATTERN = Pattern.compile(
        "^[a-zA-Z]+$"
    );
    
    /** 字母数字验证 */
    private static final Pattern ALPHANUMERIC_PATTERN = Pattern.compile(
        "^[a-zA-Z0-9]+$"
    );
    
    /** 用户名验证（字母开头，允许字母数字下划线） */
    private static final Pattern USERNAME_PATTERN = Pattern.compile(
        "^[a-zA-Z][a-zA-Z0-9_]{2,19}$"
    );
    
    /** 强密码验证（至少8位，包含大小写字母、数字、特殊字符） */
    private static final Pattern STRONG_PASSWORD_PATTERN = Pattern.compile(
        "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$"
    );
    
    /** MAC 地址验证 */
    private static final Pattern MAC_ADDRESS_PATTERN = Pattern.compile(
        "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    );
    
    /** 中文验证 */
    private static final Pattern CHINESE_PATTERN = Pattern.compile(
        "^[\\u4e00-\\u9fa5]+$"
    );
    
    // ==================== 基础验证方法 ====================
    
    /**
     * 检查字符串是否为空（null 或长度为0）
     * 
     * @param str 待检查字符串
     * @return 是否为空
     */
    public static boolean isEmpty(String str) {
        return str == null || str.isEmpty();
    }
    
    /**
     * 检查字符串是否为空白（null、空或仅包含空白字符）
     * 
     * @param str 待检查字符串
     * @return 是否为空白
     */
    public static boolean isBlank(String str) {
        return str == null || str.trim().isEmpty();
    }
    
    /**
     * 检查字符串是否不为空
     * 
     * @param str 待检查字符串
     * @return 是否不为空
     */
    public static boolean isNotEmpty(String str) {
        return !isEmpty(str);
    }
    
    /**
     * 检查字符串是否不为空白
     * 
     * @param str 待检查字符串
     * @return 是否不为空白
     */
    public static boolean isNotBlank(String str) {
        return !isBlank(str);
    }
    
    // ==================== 格式验证方法 ====================
    
    /**
     * 验证邮箱格式
     * 
     * @param email 邮箱地址
     * @return 是否有效
     */
    public static boolean isEmail(String email) {
        if (isBlank(email)) return false;
        return EMAIL_PATTERN.matcher(email).matches();
    }
    
    /**
     * 验证中国大陆手机号
     * 
     * @param phone 手机号
     * @return 是否有效
     */
    public static boolean isChinaMobile(String phone) {
        if (isBlank(phone)) return false;
        return CHINA_MOBILE_PATTERN.matcher(phone).matches();
    }
    
    /**
     * 验证 IPv4 地址
     * 
     * @param ip IP地址
     * @return 是否有效
     */
    public static boolean isIpv4(String ip) {
        if (isBlank(ip)) return false;
        if (!IPV4_PATTERN.matcher(ip).matches()) return false;
        
        // 额外验证每个段是否在 0-255 范围内
        String[] parts = ip.split("\\.");
        for (String part : parts) {
            int num = Integer.parseInt(part);
            if (num < 0 || num > 255) return false;
        }
        return true;
    }
    
    /**
     * 验证 IPv6 地址
     * 
     * @param ip IP地址
     * @return 是否有效
     */
    public static boolean isIpv6(String ip) {
        if (isBlank(ip)) return false;
        return IPV6_PATTERN.matcher(ip).matches();
    }
    
    /**
     * 验证 URL 格式
     * 
     * @param url URL地址
     * @return 是否有效
     */
    public static boolean isUrl(String url) {
        if (isBlank(url)) return false;
        return URL_PATTERN.matcher(url).matches();
    }
    
    /**
     * 验证中国大陆身份证号（18位）
     * 包含校验码验证
     * 
     * @param idCard 身份证号
     * @return 是否有效
     */
    public static boolean isChinaIdCard(String idCard) {
        if (isBlank(idCard)) return false;
        if (!CHINA_ID_CARD_PATTERN.matcher(idCard).matches()) return false;
        
        // 校验码验证
        return validateIdCardCheckCode(idCard);
    }
    
    /**
     * 验证身份证号校验码
     * 
     * @param idCard 身份证号
     * @return 校验码是否正确
     */
    private static boolean validateIdCardCheckCode(String idCard) {
        String[] weights = {"7", "9", "10", "5", "8", "4", "2", "1", "6", "3", "7", "9", "10", "5", "8", "4", "2"};
        String[] checkCodes = {"1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"};
        
        int sum = 0;
        for (int i = 0; i < 17; i++) {
            sum += Integer.parseInt(String.valueOf(idCard.charAt(i))) * Integer.parseInt(weights[i]);
        }
        
        int mod = sum % 11;
        String expectedCheckCode = checkCodes[mod];
        String actualCheckCode = idCard.substring(17).toUpperCase();
        
        return expectedCheckCode.equals(actualCheckCode);
    }
    
    /**
     * 验证信用卡号（使用 Luhn 算法）
     * 
     * @param cardNumber 信用卡号
     * @return 是否有效
     */
    public static boolean isCreditCard(String cardNumber) {
        if (isBlank(cardNumber)) return false;
        
        // 移除空格和横线
        String cleaned = cardNumber.replaceAll("[\\s-]", "");
        
        if (!CREDIT_CARD_PATTERN.matcher(cleaned).matches()) return false;
        
        // Luhn 算法验证
        return luhnCheck(cleaned);
    }
    
    /**
     * Luhn 算法验证
     * 
     * @param cardNumber 清理后的卡号
     * @return 是否通过验证
     */
    private static boolean luhnCheck(String cardNumber) {
        int sum = 0;
        boolean alternate = false;
        
        for (int i = cardNumber.length() - 1; i >= 0; i--) {
            int n = Integer.parseInt(cardNumber.substring(i, i + 1));
            if (alternate) {
                n *= 2;
                if (n > 9) n -= 9;
            }
            sum += n;
            alternate = !alternate;
        }
        
        return (sum % 10) == 0;
    }
    
    /**
     * 验证邮政编码（中国大陆）
     * 
     * @param zipCode 邮政编码
     * @return 是否有效
     */
    public static boolean isChinaZipCode(String zipCode) {
        if (isBlank(zipCode)) return false;
        return CHINA_ZIP_CODE_PATTERN.matcher(zipCode).matches();
    }
    
    /**
     * 验证日期格式（YYYY-MM-DD）
     * 
     * @param date 日期字符串
     * @return 是否有效
     */
    public static boolean isDate(String date) {
        if (isBlank(date)) return false;
        if (!DATE_PATTERN.matcher(date).matches()) return false;
        
        // 进一步验证日期有效性
        try {
            String[] parts = date.split("-");
            int year = Integer.parseInt(parts[0]);
            int month = Integer.parseInt(parts[1]);
            int day = Integer.parseInt(parts[2]);
            
            return isValidDate(year, month, day);
        } catch (Exception e) {
            return false;
        }
    }
    
    /**
     * 验证时间格式（HH:MM:SS）
     * 
     * @param time 时间字符串
     * @return 是否有效
     */
    public static boolean isTime(String time) {
        if (isBlank(time)) return false;
        return TIME_PATTERN.matcher(time).matches();
    }
    
    /**
     * 验证 UUID 格式
     * 
     * @param uuid UUID字符串
     * @return 是否有效
     */
    public static boolean isUuid(String uuid) {
        if (isBlank(uuid)) return false;
        return UUID_PATTERN.matcher(uuid).matches();
    }
    
    /**
     * 验证十六进制颜色格式
     * 
     * @param color 颜色字符串（如 #FF5733 或 #F53）
     * @return 是否有效
     */
    public static boolean isHexColor(String color) {
        if (isBlank(color)) return false;
        return HEX_COLOR_PATTERN.matcher(color).matches();
    }
    
    /**
     * 验证是否为纯数字
     * 
     * @param str 待验证字符串
     * @return 是否有效
     */
    public static boolean isNumeric(String str) {
        if (isBlank(str)) return false;
        return NUMERIC_PATTERN.matcher(str).matches();
    }
    
    /**
     * 验证是否为纯字母
     * 
     * @param str 待验证字符串
     * @return 是否有效
     */
    public static boolean isAlpha(String str) {
        if (isBlank(str)) return false;
        return ALPHA_PATTERN.matcher(str).matches();
    }
    
    /**
     * 验证是否为字母数字组合
     * 
     * @param str 待验证字符串
     * @return 是否有效
     */
    public static boolean isAlphanumeric(String str) {
        if (isBlank(str)) return false;
        return ALPHANUMERIC_PATTERN.matcher(str).matches();
    }
    
    /**
     * 验证用户名格式
     * 字母开头，3-20位，允许字母数字下划线
     * 
     * @param username 用户名
     * @return 是否有效
     */
    public static boolean isUsername(String username) {
        if (isBlank(username)) return false;
        return USERNAME_PATTERN.matcher(username).matches();
    }
    
    /**
     * 验证强密码
     * 至少8位，包含大小写字母、数字、特殊字符
     * 
     * @param password 密码
     * @return 是否有效
     */
    public static boolean isStrongPassword(String password) {
        if (isBlank(password)) return false;
        return STRONG_PASSWORD_PATTERN.matcher(password).matches();
    }
    
    /**
     * 验证 MAC 地址格式
     * 
     * @param macAddress MAC地址
     * @return 是否有效
     */
    public static boolean isMacAddress(String macAddress) {
        if (isBlank(macAddress)) return false;
        return MAC_ADDRESS_PATTERN.matcher(macAddress).matches();
    }
    
    /**
     * 验证是否为纯中文
     * 
     * @param str 待验证字符串
     * @return 是否有效
     */
    public static boolean isChinese(String str) {
        if (isBlank(str)) return false;
        return CHINESE_PATTERN.matcher(str).matches();
    }
    
    // ==================== 范围验证方法 ====================
    
    /**
     * 验证字符串长度是否在指定范围内
     * 
     * @param str 待验证字符串
     * @param min 最小长度（包含）
     * @param max 最大长度（包含）
     * @return 是否在范围内
     */
    public static boolean lengthBetween(String str, int min, int max) {
        if (str == null) return false;
        int len = str.length();
        return len >= min && len <= max;
    }
    
    /**
     * 验证数值是否在指定范围内
     * 
     * @param value 数值
     * @param min 最小值（包含）
     * @param max 最大值（包含）
     * @return 是否在范围内
     */
    public static boolean between(int value, int min, int max) {
        return value >= min && value <= max;
    }
    
    /**
     * 验证数值是否在指定范围内（长整型）
     * 
     * @param value 数值
     * @param min 最小值（包含）
     * @param max 最大值（包含）
     * @return 是否在范围内
     */
    public static boolean between(long value, long min, long max) {
        return value >= min && value <= max;
    }
    
    /**
     * 验证数值是否在指定范围内（双精度浮点）
     * 
     * @param value 数值
     * @param min 最小值（包含）
     * @param max 最大值（包含）
     * @return 是否在范围内
     */
    public static boolean between(double value, double min, double max) {
        return value >= min && value <= max;
    }
    
    // ==================== 正则表达式验证方法 ====================
    
    /**
     * 使用正则表达式验证字符串
     * 
     * @param str 待验证字符串
     * @param pattern 正则表达式
     * @return 是否匹配
     */
    public static boolean matches(String str, String pattern) {
        if (isBlank(str) || isBlank(pattern)) return false;
        return Pattern.compile(pattern).matcher(str).matches();
    }
    
    /**
     * 使用正则表达式验证字符串（使用预编译 Pattern）
     * 
     * @param str 待验证字符串
     * @param pattern 预编译的正则表达式
     * @return 是否匹配
     */
    public static boolean matches(String str, Pattern pattern) {
        if (isBlank(str) || pattern == null) return false;
        return pattern.matcher(str).matches();
    }
    
    /**
     * 查找字符串中所有匹配正则表达式的子串
     * 
     * @param str 待搜索字符串
     * @param pattern 正则表达式
     * @return 匹配的子串列表
     */
    public static List<String> findAll(String str, String pattern) {
        List<String> matches = new ArrayList<>();
        if (isBlank(str) || isBlank(pattern)) return matches;
        
        Matcher matcher = Pattern.compile(pattern).matcher(str);
        while (matcher.find()) {
            matches.add(matcher.group());
        }
        return matches;
    }
    
    /**
     * 查找字符串中第一个匹配正则表达式的子串
     * 
     * @param str 待搜索字符串
     * @param pattern 正则表达式
     * @return 匹配的子串，未找到返回 null
     */
    public static String findFirst(String str, String pattern) {
        if (isBlank(str) || isBlank(pattern)) return null;
        
        Matcher matcher = Pattern.compile(pattern).matcher(str);
        if (matcher.find()) {
            return matcher.group();
        }
        return null;
    }
    
    // ==================== 批量验证方法 ====================
    
    /**
     * 验证结果类
     */
    public static class ValidationResult {
        private final boolean valid;
        private final String field;
        private final String message;
        
        public ValidationResult(boolean valid, String field, String message) {
            this.valid = valid;
            this.field = field;
            this.message = message;
        }
        
        public boolean isValid() { return valid; }
        public String getField() { return field; }
        public String getMessage() { return message; }
        
        @Override
        public String toString() {
            return String.format("ValidationResult{valid=%s, field='%s', message='%s'}", 
                valid, field, message);
        }
    }
    
    /**
     * 批量验证多个字段
     * 
     * @param validations 验证规则映射（字段名 -> 待验证值）
     * @return 验证结果列表
     */
    public static List<ValidationResult> validateAll(Map<String, String> validations) {
        List<ValidationResult> results = new ArrayList<>();
        
        for (Map.Entry<String, String> entry : validations.entrySet()) {
            String field = entry.getKey();
            String value = entry.getValue();
            
            if (isBlank(value)) {
                results.add(new ValidationResult(false, field, field + " cannot be empty"));
            } else {
                results.add(new ValidationResult(true, field, "OK"));
            }
        }
        
        return results;
    }
    
    // ==================== 辅助方法 ====================
    
    /**
     * 验证日期是否有效（考虑闰年等因素）
     * 
     * @param year 年份
     * @param month 月份（1-12）
     * @param day 日期（1-31）
     * @return 是否有效
     */
    private static boolean isValidDate(int year, int month, int day) {
        if (year < 1 || month < 1 || month > 12 || day < 1) return false;
        
        int[] daysInMonth = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        
        // 闰年判断
        if (isLeapYear(year)) {
            daysInMonth[1] = 29;
        }
        
        return day <= daysInMonth[month - 1];
    }
    
    /**
     * 判断是否为闰年
     * 
     * @param year 年份
     * @return 是否为闰年
     */
    public static boolean isLeapYear(int year) {
        return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
    }
    
    /**
     * 获取字符串长度（null 安全）
     * 
     * @param str 字符串
     * @return 长度，null 返回 0
     */
    public static int length(String str) {
        return str == null ? 0 : str.length();
    }
    
    /**
     * 检查字符串是否包含指定子串（null 安全）
     * 
     * @param str 待检查字符串
     * @param substr 子串
     * @return 是否包含
     */
    public static boolean contains(String str, String substr) {
        if (str == null || substr == null) return false;
        return str.contains(substr);
    }
    
    /**
     * 检查字符串是否以指定前缀开头（null 安全）
     * 
     * @param str 待检查字符串
     * @param prefix 前缀
     * @return 是否以此前缀开头
     */
    public static boolean startsWith(String str, String prefix) {
        if (str == null || prefix == null) return false;
        return str.startsWith(prefix);
    }
    
    /**
     * 检查字符串是否以指定后缀结尾（null 安全）
     * 
     * @param str 待检查字符串
     * @param suffix 后缀
     * @return 是否以此后缀结尾
     */
    public static boolean endsWith(String str, String suffix) {
        if (str == null || suffix == null) return false;
        return str.endsWith(suffix);
    }
    
    /**
     * 验证字符串是否等于指定值（null 安全）
     * 
     * @param str1 字符串1
     * @param str2 字符串2
     * @return 是否相等
     */
    public static boolean equals(String str1, String str2) {
        if (str1 == null && str2 == null) return true;
        if (str1 == null || str2 == null) return false;
        return str1.equals(str2);
    }
    
    /**
     * 验证字符串是否等于指定值（忽略大小写，null 安全）
     * 
     * @param str1 字符串1
     * @param str2 字符串2
     * @return 是否相等（忽略大小写）
     */
    public static boolean equalsIgnoreCase(String str1, String str2) {
        if (str1 == null && str2 == null) return true;
        if (str1 == null || str2 == null) return false;
        return str1.equalsIgnoreCase(str2);
    }
}
