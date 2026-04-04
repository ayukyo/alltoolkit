package examples;

import validation_utils.ValidationUtils;

/**
 * ValidationUtils 使用示例
 * 
 * 运行方式：
 * cd Java
 * javac -cp . examples/validation_utils_example.java validation_utils/*.java
 * java -cp . examples.validation_utils_example
 */
public class validation_utils_example {
    
    public static void main(String[] args) {
        System.out.println("=== ValidationUtils Examples ===\n");
        
        exampleBasicValidation();
        exampleEmailValidation();
        examplePhoneValidation();
        exampleIpValidation();
        exampleUrlValidation();
        exampleFormatValidation();
        exampleRangeValidation();
        exampleRegexValidation();
        exampleUtilityMethods();
        
        System.out.println("\n=== All Examples Completed ===");
    }
    
    private static void exampleBasicValidation() {
        System.out.println("1. Basic Validation");
        System.out.println("-------------------");
        
        String input1 = null;
        String input2 = "";
        String input3 = "   ";
        String input4 = "hello";
        
        System.out.println("isEmpty(null): " + ValidationUtils.isEmpty(input1));
        System.out.println("isEmpty(''): " + ValidationUtils.isEmpty(input2));
        System.out.println("isBlank('   '): " + ValidationUtils.isBlank(input3));
        System.out.println("isNotBlank('hello'): " + ValidationUtils.isNotBlank(input4));
        System.out.println();
    }
    
    private static void exampleEmailValidation() {
        System.out.println("2. Email Validation");
        System.out.println("-------------------");
        
        String[] emails = {
            "user@example.com",
            "invalid.email",
            "test@domain.co.uk",
            "@example.com",
            "user+tag@example.com"
        };
        
        for (String email : emails) {
            System.out.println("isEmail('" + email + "'): " + ValidationUtils.isEmail(email));
        }
        System.out.println();
    }
    
    private static void examplePhoneValidation() {
        System.out.println("3. Phone Validation (China Mobile)");
        System.out.println("-----------------------------------");
        
        String[] phones = {
            "13800138000",
            "19912345678",
            "12345678901",
            "1380013800",
            "138001380001"
        };
        
        for (String phone : phones) {
            System.out.println("isChinaMobile('" + phone + "'): " + ValidationUtils.isChinaMobile(phone));
        }
        System.out.println();
    }
    
    private static void exampleIpValidation() {
        System.out.println("4. IP Address Validation");
        System.out.println("------------------------");
        
        String[] ips = {
            "192.168.1.1",
            "256.1.1.1",
            "::1",
            "2001:0db8:85a3::8a2e:0370:7334"
        };
        
        for (String ip : ips) {
            System.out.println("isIpv4('" + ip + "'): " + ValidationUtils.isIpv4(ip) + 
                ", isIpv6('" + ip + "'): " + ValidationUtils.isIpv6(ip));
        }
        System.out.println();
    }
    
    private static void exampleUrlValidation() {
        System.out.println("5. URL Validation");
        System.out.println("-----------------");
        
        String[] urls = {
            "https://example.com",
            "http://localhost:8080",
            "ftp://files.example.com",
            "example.com",
            "not a url"
        };
        
        for (String url : urls) {
            System.out.println("isUrl('" + url + "'): " + ValidationUtils.isUrl(url));
        }
        System.out.println();
    }
    
    private static void exampleFormatValidation() {
        System.out.println("6. Format Validation");
        System.out.println("--------------------");
        
        // UUID
        String uuid = "550e8400-e29b-41d4-a716-446655440000";
        System.out.println("isUuid('" + uuid + "'): " + ValidationUtils.isUuid(uuid));
        
        // Hex Color
        System.out.println("isHexColor('#FF5733'): " + ValidationUtils.isHexColor("#FF5733"));
        System.out.println("isHexColor('#F53'): " + ValidationUtils.isHexColor("#F53"));
        
        // Numeric and Alpha
        System.out.println("isNumeric('12345'): " + ValidationUtils.isNumeric("12345"));
        System.out.println("isAlpha('hello'): " + ValidationUtils.isAlpha("hello"));
        System.out.println("isAlphanumeric('abc123'): " + ValidationUtils.isAlphanumeric("abc123"));
        
        // Username
        System.out.println("isUsername('user123'): " + ValidationUtils.isUsername("user123"));
        System.out.println("isUsername('123user'): " + ValidationUtils.isUsername("123user"));
        
        // MAC Address
        System.out.println("isMacAddress('00:1A:2B:3C:4D:5E'): " + 
            ValidationUtils.isMacAddress("00:1A:2B:3C:4D:5E"));
        
        // Chinese
        System.out.println("isChinese('中文'): " + ValidationUtils.isChinese("中文"));
        System.out.println();
    }
    
    private static void exampleRangeValidation() {
        System.out.println("7. Range Validation");
        System.out.println("-------------------");
        
        String str = "hello";
        System.out.println("lengthBetween('hello', 3, 10): " + ValidationUtils.lengthBetween(str, 3, 10));
        System.out.println("lengthBetween('hello', 1, 3): " + ValidationUtils.lengthBetween(str, 1, 3));
        
        int num = 5;
        System.out.println("between(5, 1, 10): " + ValidationUtils.between(num, 1, 10));
        System.out.println("between(5, 10, 20): " + ValidationUtils.between(num, 10, 20));
        System.out.println();
    }
    
    private static void exampleRegexValidation() {
        System.out.println("8. Regex Validation");
        System.out.println("-------------------");
        
        String text = "The quick brown fox jumps over 13 lazy dogs.";
        String pattern = "\\d+";
        
        System.out.println("Text: '" + text + "'");
        System.out.println("Pattern: '" + pattern + "'");
        System.out.println("matches: " + ValidationUtils.matches(text, pattern));
        System.out.println("findFirst: " + ValidationUtils.findFirst(text, pattern));
        System.out.println("findAll: " + ValidationUtils.findAll(text, pattern));
        System.out.println();
    }
    
    private static void exampleUtilityMethods() {
        System.out.println("9. Utility Methods");
        System.out.println("------------------");
        
        // Leap year
        System.out.println("isLeapYear(2020): " + ValidationUtils.isLeapYear(2020));
        System.out.println("isLeapYear(2021): " + ValidationUtils.isLeapYear(2021));
        
        // String utilities
        System.out.println("equals('test', 'test'): " + ValidationUtils.equals("test", "test"));
        System.out.println("equalsIgnoreCase('Test', 'test'): " + ValidationUtils.equalsIgnoreCase("Test", "test"));
        System.out.println("contains('hello world', 'world'): " + ValidationUtils.contains("hello world", "world"));
        System.out.println("startsWith('hello', 'he'): " + ValidationUtils.startsWith("hello", "he"));
        System.out.println("endsWith('hello', 'lo'): " + ValidationUtils.endsWith("hello", "lo"));
        System.out.println();
    }
}
