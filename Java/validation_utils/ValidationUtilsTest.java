package validation_utils;

import java.util.List;
import java.util.Map;
import java.util.HashMap;

/**
 * ValidationUtils 单元测试
 * 
 * 运行方式：
 * cd Java/validation_utils
 * javac *.java && java validation_utils.ValidationUtilsTest
 */
public class ValidationUtilsTest {
    
    private static int passed = 0;
    private static int failed = 0;
    
    public static void main(String[] args) {
        System.out.println("=== ValidationUtils Test Suite ===\n");
        
        testBasicValidation();
        testEmailValidation();
        testPhoneValidation();
        testIpValidation();
        testUrlValidation();
        testFormatValidation();
        testRangeValidation();
        testUtilityMethods();
        
        System.out.println("\n=== Test Summary ===");
        System.out.println("Passed: " + passed);
        System.out.println("Failed: " + failed);
        System.out.println("Total:  " + (passed + failed));
        
        if (failed > 0) {
            System.exit(1);
        }
    }
    
    private static void testBasicValidation() {
        System.out.println("Testing Basic Validation...");
        
        assertTrue("isEmpty(null)", ValidationUtils.isEmpty(null));
        assertTrue("isEmpty('')", ValidationUtils.isEmpty(""));
        assertFalse("isEmpty('a')", ValidationUtils.isEmpty("a"));
        
        assertTrue("isBlank(null)", ValidationUtils.isBlank(null));
        assertTrue("isBlank('')", ValidationUtils.isBlank(""));
        assertTrue("isBlank('  ')", ValidationUtils.isBlank("  "));
        assertFalse("isBlank('a')", ValidationUtils.isBlank("a"));
        
        assertFalse("isNotEmpty(null)", ValidationUtils.isNotEmpty(null));
        assertTrue("isNotEmpty('a')", ValidationUtils.isNotEmpty("a"));
        
        assertFalse("isNotBlank('  ')", ValidationUtils.isNotBlank("  "));
        assertTrue("isNotBlank('a')", ValidationUtils.isNotBlank("a"));
        
        System.out.println("  Basic Validation: PASSED\n");
    }
    
    private static void testEmailValidation() {
        System.out.println("Testing Email Validation...");
        
        assertTrue("isEmail('test@example.com')", ValidationUtils.isEmail("test@example.com"));
        assertTrue("isEmail('user.name@domain.co.uk')", ValidationUtils.isEmail("user.name@domain.co.uk"));
        assertFalse("isEmail(null)", ValidationUtils.isEmail(null));
        assertFalse("isEmail('')", ValidationUtils.isEmail(""));
        assertFalse("isEmail('invalid')", ValidationUtils.isEmail("invalid"));
        assertFalse("isEmail('@example.com')", ValidationUtils.isEmail("@example.com"));
        
        System.out.println("  Email Validation: PASSED\n");
    }
    
    private static void testPhoneValidation() {
        System.out.println("Testing Phone Validation...");
        
        assertTrue("isChinaMobile('13800138000')", ValidationUtils.isChinaMobile("13800138000"));
        assertTrue("isChinaMobile('19912345678')", ValidationUtils.isChinaMobile("19912345678"));
        assertFalse("isChinaMobile(null)", ValidationUtils.isChinaMobile(null));
        assertFalse("isChinaMobile('12345678901')", ValidationUtils.isChinaMobile("12345678901"));
        assertFalse("isChinaMobile('1380013800')", ValidationUtils.isChinaMobile("1380013800"));
        
        System.out.println("  Phone Validation: PASSED\n");
    }
    
    private static void testIpValidation() {
        System.out.println("Testing IP Validation...");
        
        assertTrue("isIpv4('192.168.1.1')", ValidationUtils.isIpv4("192.168.1.1"));
        assertTrue("isIpv4('255.255.255.255')", ValidationUtils.isIpv4("255.255.255.255"));
        assertFalse("isIpv4(null)", ValidationUtils.isIpv4(null));
        assertFalse("isIpv4('256.1.1.1')", ValidationUtils.isIpv4("256.1.1.1"));
        assertFalse("isIpv4('192.168.1')", ValidationUtils.isIpv4("192.168.1"));
        
        assertTrue("isIpv6('::1')", ValidationUtils.isIpv6("::1"));
        assertFalse("isIpv6('192.168.1.1')", ValidationUtils.isIpv6("192.168.1.1"));
        
        System.out.println("  IP Validation: PASSED\n");
    }
    
    private static void testUrlValidation() {
        System.out.println("Testing URL Validation...");
        
        assertTrue("isUrl('http://example.com')", ValidationUtils.isUrl("http://example.com"));
        assertTrue("isUrl('https://example.com')", ValidationUtils.isUrl("https://example.com"));
        assertFalse("isUrl(null)", ValidationUtils.isUrl(null));
        assertFalse("isUrl('')", ValidationUtils.isUrl(""));
        assertFalse("isUrl('example.com')", ValidationUtils.isUrl("example.com"));
        
        System.out.println("  URL Validation: PASSED\n");
    }
    
    private static void testFormatValidation() {
        System.out.println("Testing Format Validation...");
        
        assertTrue("isUuid('550e8400-e29b-41d4-a716-446655440000')", 
            ValidationUtils.isUuid("550e8400-e29b-41d4-a716-446655440000"));
        assertFalse("isUuid('invalid')", ValidationUtils.isUuid("invalid"));
        
        assertTrue("isHexColor('#FF5733')", ValidationUtils.isHexColor("#FF5733"));
        assertTrue("isHexColor('#F53')", ValidationUtils.isHexColor("#F53"));
        assertFalse("isHexColor('FF5733')", ValidationUtils.isHexColor("FF5733"));
        
        assertTrue("isNumeric('123')", ValidationUtils.isNumeric("123"));
        assertTrue("isNumeric('-123')", ValidationUtils.isNumeric("-123"));
        assertFalse("isNumeric('12.3')", ValidationUtils.isNumeric("12.3"));
        
        assertTrue("isAlpha('abc')", ValidationUtils.isAlpha("abc"));
        assertFalse("isAlpha('abc123')", ValidationUtils.isAlpha("abc123"));
        
        assertTrue("isAlphanumeric('abc123')", ValidationUtils.isAlphanumeric("abc123"));
        assertFalse("isAlphanumeric('abc-123')", ValidationUtils.isAlphanumeric("abc-123"));
        
        assertTrue("isUsername('user123')", ValidationUtils.isUsername("user123"));
        assertFalse("isUsername('123user')", ValidationUtils.isUsername("123user"));
        
        assertTrue("isMacAddress('00:1A:2B:3C:4D:5E')", ValidationUtils.isMacAddress("00:1A:2B:3C:4D:5E"));
        assertFalse("isMacAddress('invalid')", ValidationUtils.isMacAddress("invalid"));
        
        assertTrue("isChinese('中文')", ValidationUtils.isChinese("中文"));
        assertFalse("isChinese('Chinese')", ValidationUtils.isChinese("Chinese"));
        
        System.out.println("  Format Validation: PASSED\n");
    }
    
    private static void testRangeValidation() {
        System.out.println("Testing Range Validation...");
        
        assertTrue("lengthBetween('hello', 3, 10)", ValidationUtils.lengthBetween("hello", 3, 10));
        assertFalse("lengthBetween('hi', 3, 10)", ValidationUtils.lengthBetween("hi", 3, 10));
        assertFalse("lengthBetween(null, 3, 10)", ValidationUtils.lengthBetween(null, 3, 10));
        
        assertTrue("between(5, 1, 10)", ValidationUtils.between(5, 1, 10));
        assertFalse("between(15, 1, 10)", ValidationUtils.between(15, 1, 10));
        
        System.out.println("  Range Validation: PASSED\n");
    }
    
    private static void testUtilityMethods() {
        System.out.println("Testing Utility Methods...");
        
        assertTrue("isLeapYear(2020)", ValidationUtils.isLeapYear(2020));
        assertFalse("isLeapYear(2021)", ValidationUtils.isLeapYear(2021));
        
        assertTrue("equals('test', 'test')", ValidationUtils.equals("test", "test"));
        assertTrue("equals(null, null)", ValidationUtils.equals(null, null));
        assertFalse("equals('test', 'other')", ValidationUtils.equals("test", "other"));
        assertFalse("equals('test', null)", ValidationUtils.equals("test", null));
        
        assertTrue("equalsIgnoreCase('Test', 'test')", ValidationUtils.equalsIgnoreCase("Test", "test"));
        assertTrue("contains('hello world', 'world')", ValidationUtils.contains("hello world", "world"));
        assertFalse("contains('hello', 'world')", ValidationUtils.contains("hello", "world"));
        assertTrue("startsWith('hello', 'he')", ValidationUtils.startsWith("hello", "he"));
        assertTrue("endsWith('hello', 'lo')", ValidationUtils.endsWith("hello", "lo"));
        
        System.out.println("  Utility Methods: PASSED\n");
    }
    
    private static void assertTrue(String message, boolean condition) {
        if (condition) {
            passed++;
        } else {
            failed++;
            System.out.println("    FAILED: " + message);
        }
    }
    
    private static void assertFalse(String message, boolean condition) {
        assertTrue(message, !condition);
    }
}