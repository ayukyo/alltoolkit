package string_utils;

import java.util.*;

/**
 * StringUtils 单元测试
 * 
 * 运行方式：
 * cd Java/string_utils
 * javac *.java && java string_utils.StringUtilsTest
 */
public class StringUtilsTest {
    
    private static int passed = 0;
    private static int failed = 0;
    
    public static void main(String[] args) {
        System.out.println("=== StringUtils Test Suite ===\n");
        
        testCaseConversion();
        testTrimAndPad();
        testTruncate();
        testInterpolation();
        testEscaping();
        testExtraction();
        testCharStats();
        testStringOperations();
        testBase64();
        testSimilarity();
        testUtilities();
        
        System.out.println("\n=== Test Summary ===");
        System.out.println("Passed: " + passed);
        System.out.println("Failed: " + failed);
        System.out.println("Total:  " + (passed + failed));
        
        if (failed > 0) {
            System.exit(1);
        }
    }
    
    private static void assertTrue(String message, boolean condition) {
        if (condition) {
            passed++;
        } else {
            failed++;
            System.out.println("  FAILED: " + message);
        }
    }
    
    private static void assertEquals(String message, String expected, String actual) {
        if (Objects.equals(expected, actual)) {
            passed++;
        } else {
            failed++;
            System.out.println("  FAILED: " + message);
            System.out.println("    Expected: " + expected);
            System.out.println("    Actual:   " + actual);
        }
    }
    
    private static void assertEquals(String message, int expected, int actual) {
        if (expected == actual) {
            passed++;
        } else {
            failed++;
            System.out.println("  FAILED: " + message);
            System.out.println("    Expected: " + expected);
            System.out.println("    Actual:   " + actual);
        }
    }
    
    private static void assertEquals(String message, double expected, double actual, double delta) {
        if (Math.abs(expected - actual) <= delta) {
            passed++;
        } else {
            failed++;
            System.out.println("  FAILED: " + message);
            System.out.println("    Expected: " + expected);
            System.out.println("    Actual:   " + actual);
        }
    }
    
    private static void testCaseConversion() {
        System.out.println("Testing Case Conversion...");
        
        // camelCase
        assertEquals("toCamelCase('hello_world')", "helloWorld", StringUtils.toCamelCase("hello_world"));
        assertEquals("toCamelCase('Hello-World-Test')", "helloWorldTest", StringUtils.toCamelCase("Hello-World-Test"));
        assertEquals("toCamelCase('alreadyCamelCase')", "alreadyCamelCase", StringUtils.toCamelCase("alreadyCamelCase"));
        
        // PascalCase
        assertEquals("toPascalCase('hello_world')", "HelloWorld", StringUtils.toPascalCase("hello_world"));
        assertEquals("toPascalCase('hello-world')", "HelloWorld", StringUtils.toPascalCase("hello-world"));
        
        // snake_case
        assertEquals("toSnakeCase('helloWorld')", "hello_world", StringUtils.toSnakeCase("helloWorld"));
        assertEquals("toSnakeCase('HelloWorldTest')", "hello_world_test", StringUtils.toSnakeCase("HelloWorldTest"));
        
        // kebab-case
        assertEquals("toKebabCase('helloWorld')", "hello-world", StringUtils.toKebabCase("helloWorld"));
        assertEquals("toKebabCase('Hello World')", "hello-world", StringUtils.toKebabCase("Hello World"));
        
        // CONSTANT_CASE
        assertEquals("toConstantCase('helloWorld')", "HELLO_WORLD", StringUtils.toConstantCase("helloWorld"));
        
        // dot.case
        assertEquals("toDotCase('helloWorld')", "hello.world", StringUtils.toDotCase("helloWorld"));
        
        // path/case
        assertEquals("toPathCase('helloWorld')", "hello/world", StringUtils.toPathCase("helloWorld"));
        
        // space case
        assertEquals("toSpaceCase('helloWorld')", "hello world", StringUtils.toSpaceCase("helloWorld"));
        
        // Sentence case
        assertEquals("toSentenceCase('hello WORLD')", "Hello world", StringUtils.toSentenceCase("hello WORLD"));
        
        // Edge cases
        assertEquals("toCamelCase(null)", null, StringUtils.toCamelCase(null));
        assertEquals("toCamelCase('')", "", StringUtils.toCamelCase(""));
        assertEquals("toCamelCase('a')", "a", StringUtils.toCamelCase("a"));
        
        System.out.println("  Case Conversion: PASSED\n");
    }
    
    private static void testTrimAndPad() {
        System.out.println("Testing Trim and Pad...");
        
        // trim
        assertEquals("trim('  hello  ')", "hello", StringUtils.trim("  hello  "));
        assertEquals("trim(null)", null, StringUtils.trim(null));
        
        // trimLeft
        assertEquals("trimLeft('  hello  ')", "hello  ", StringUtils.trimLeft("  hello  "));
        
        // trimRight
        assertEquals("trimRight('  hello  ')", "  hello", StringUtils.trimRight("  hello  "));
        
        // padLeft
        assertEquals("padLeft('123', 5, '0')", "00123", StringUtils.padLeft("123", 5, '0'));
        assertEquals("padLeft('12345', 3, '0')", "12345", StringUtils.padLeft("12345", 3, '0'));
        
        // padRight
        assertEquals("padRight('123', 5, ' ')", "123  ", StringUtils.padRight("123", 5, ' '));
        
        // zeroPad
        assertEquals("zeroPad('42', 4)", "0042", StringUtils.zeroPad("42", 4));
        
        // center
        assertEquals("center('hi', 5, '*')", "*hi**", StringUtils.center("hi", 5, '*'));
        assertEquals("center('hi', 4, '*')", "*hi*", StringUtils.center("hi", 4, '*'));
        
        System.out.println("  Trim and Pad: PASSED\n");
    }
    
    private static void testTruncate() {
        System.out.println("Testing Truncate...");
        
        // truncate with suffix
        assertEquals("truncate('Hello World', 8, '...')", "Hello...", StringUtils.truncate("Hello World", 8, "..."));
        assertEquals("truncate('Hi', 10, '...')", "Hi", StringUtils.truncate("Hi", 10, "..."));
        
        // truncate default
        assertEquals("truncate('Hello World', 8)", "Hello...", StringUtils.truncate("Hello World", 8));
        
        // truncateWords
        assertEquals("truncateWords('Hello World Test', 2, '...')", "Hello World...", StringUtils.truncateWords("Hello World Test", 2, "..."));
        assertEquals("truncateWords('Hello World', 5, '...')", "Hello World", StringUtils.truncateWords("Hello World", 5, "..."));
        
        System.out.println("  Truncate: PASSED\n");
    }
    
    private static void testInterpolation() {
        System.out.println("Testing Interpolation...");
        
        // interpolate
        Map<String, String> vars = new HashMap<>();
        vars.put("name", "World");
        vars.put("greeting", "Hello");
        assertEquals("interpolate", "Hello World!", StringUtils.interpolate("${greeting} ${name}!", vars));
        assertEquals("interpolate missing", "${missing}", StringUtils.interpolate("${missing}", vars));
        
        // format
        assertEquals("format", "Hello World", StringUtils.format("{0} {1}", "Hello", "World"));
        assertEquals("format numbers", "Value: 42", StringUtils.format("Value: {0}", 42));
        
        System.out.println("  Interpolation: PASSED\n");
    }
    
    private static void testEscaping() {
        System.out.println("Testing Escaping...");
        
        // escapeHtml
        assertEquals("escapeHtml", "&lt;script&gt;", StringUtils.escapeHtml("<script>"));
        assertEquals("escapeHtml quotes", "&quot;test&quot;", StringUtils.escapeHtml("\"test\""));
        
        // unescapeHtml
        assertEquals("unescapeHtml", "<script>", StringUtils.unescapeHtml("&lt;script&gt;"));
        
        // escapeXml
        assertEquals("escapeXml", "&apos;test&apos;", StringUtils.escapeXml("'test'"));
        
        // escapeJson
        assertEquals("escapeJson newline", "\\n", StringUtils.escapeJson("\n"));
        assertEquals("escapeJson quote", "\\\"test\\\"", StringUtils.escapeJson("\"test\""));
        
        // escapeSql
        assertEquals("escapeSql", "O''Brien", StringUtils.escapeSql("O'Brien"));
        
        // escapeRegex
        assertEquals("escapeRegex", "\\Q.test\\E", StringUtils.escapeRegex(".test"));
        
        // urlEncode/Decode
        assertEquals("urlEncode", "Hello+World", StringUtils.urlEncode("Hello World"));
        assertEquals("urlDecode", "Hello World", StringUtils.urlDecode("Hello+World"));
        
        System.out.println("  Escaping: PASSED\n");
    }
    
    private static void testExtraction() {
        System.out.println("Testing Extraction...");
        
        String text = "Contact us at test@example.com or support@domain.org. Visit https://example.com or call +1234567890. #trending @user";
        
        // extractEmails
        List<String> emails = StringUtils.extractEmails(text);
        assertEquals("extractEmails count", 2, emails.size());
        assertTrue("extractEmails contains", emails.contains("test@example.com"));
        
        // extractUrls
        List<String> urls = StringUtils.extractUrls(text);
        assertEquals("extractUrls count", 1, urls.size());
        assertTrue("extractUrls contains", urls.contains("https://example.com"));
        
        // extractPhoneNumbers
        List<String> phones = StringUtils.extractPhoneNumbers(text);
        assertEquals("extractPhoneNumbers count", 1, phones.size());
        
        // extractHashtags
        List<String> hashtags = StringUtils.extractHashtags(text);
        assertEquals("extractHashtags count", 1, hashtags.size());
        assertEquals("extractHashtags value", "trending", hashtags.get(0));
        
        // extractMentions
        List<String> mentions = StringUtils.extractMentions(text);
        assertEquals("extractMentions count", 1, mentions.size());
        assertEquals("extractMentions value", "user", mentions.get(0));
        
        // extractNumbers
        List<String> numbers = StringUtils.extractNumbers("Price: $100, discount 20%, final 80");
        assertEquals("extractNumbers count", 3, numbers.size());
        
        System.out.println("  Extraction: PASSED\n");
    }
    
    private static void testCharStats() {
        System.out.println("Testing Character Stats...");
        
        String str = "Hello 123!";
        
        assertEquals("countLetters", 5, StringUtils.countLetters(str));
        assertEquals("countDigits", 3, StringUtils.countDigits(str));
        assertEquals("countWhitespace", 1, StringUtils.countWhitespace(str));
        assertEquals("countSpecialChars", 1, StringUtils.countSpecialChars(str));
        
        Map<String, Integer> stats = StringUtils.getCharStats(str);
        assertEquals("stats total", 10, stats.get("total").intValue());
        assertEquals("stats letters", 5, stats.get("letters").intValue());
        
        System.out.println("  Character Stats: PASSED\n");
    }
    
    private static void testStringOperations() {
        System.out.println("Testing String Operations...");
        
        // reverse
        assertEquals("reverse", "olleH", StringUtils.reverse("Hello"));
        
        // replace
        assertEquals("replace", "Hi Hi Hi", StringUtils.replace("Hello Hello Hello", "Hello", "Hi", -1));
        assertEquals("replace limited", "Hi Hi Hello", StringUtils.replace("Hello Hello Hello", "Hello", "Hi", 2));
        
        // insert
        assertEquals("insert", "HelXlo", StringUtils.insert("Hello", "X", 3));
        
        // delete
        assertEquals("delete", "Helo", StringUtils.delete("Hello", 2, 3));
        
        // repeat
        assertEquals("repeat", "abcabcabc", StringUtils.repeat("abc", 3));
        
        // capitalize
        assertEquals("capitalize", "Hello", StringUtils.capitalize("hello"));
        
        // uncapitalize
        assertEquals("uncapitalize", "hello", StringUtils.uncapitalize("Hello"));
        
        // swapCase
        assertEquals("swapCase", "hELLO", StringUtils.swapCase("Hello"));
        
        // isPalindrome
        assertTrue("isPalindrome", StringUtils.isPalindrome("A man a plan a canal Panama"));
        assertTrue("isPalindrome number", StringUtils.isPalindrome("12321"));
        assertFalse("isPalindrome false", StringUtils.isPalindrome("hello"));
        
        // join
        assertEquals("join array", "a,b,c", StringUtils.join(",", "a", "b", "c"));
        assertEquals("join collection", "x y z", StringUtils.join(" ", Arrays.asList("x", "y", "z")));
        
        // split
        List<String> parts = StringUtils.split("a,b,c", ",");
        assertEquals("split count", 3, parts.size());
        
        System.out.println("  String Operations: PASSED\n");
    }
    
    private static void testBase64() {
        System.out.println("Testing Base64...");
        
        String original = "Hello, World! 你好世界";
        
        // base64Encode/Decode
        String encoded = StringUtils.base64Encode(original);
        String decoded = StringUtils.base64Decode(encoded);
        assertEquals("base64 roundtrip", original, decoded);
        
        // base64UrlEncode/Decode
        String urlEncoded = StringUtils.base64UrlEncode(original);
        String urlDecoded = StringUtils.base64UrlDecode(urlEncoded);
        assertEquals("base64Url roundtrip", original, urlDecoded);
        
        // null handling
        assertEquals("base64Encode null", null, StringUtils.base64Encode(null));
        assertEquals("base64Decode null", null, StringUtils.base64Decode(null));
        
        System.out.println("  Base64: PASSED\n");
    }
    
    private static void testSimilarity() {
        System.out.println("Testing Similarity...");
        
        // levenshteinDistance
        assertEquals("levenshtein identical", 0, StringUtils.levenshteinDistance("hello", "hello"));
        assertEquals("levenshtein one diff", 1, StringUtils.levenshteinDistance("hello", "helo"));
        assertEquals("levenshtein different", 3, StringUtils.levenshteinDistance("kitten", "sitting"));
        assertEquals("levenshtein empty", 5, StringUtils.levenshteinDistance("", "hello"));
        
        // similarityRatio
        assertEquals("similarity identical", 1.0, StringUtils.similarityRatio("hello", "hello"), 0.001);
        assertTrue("similarity similar", StringUtils.similarityRatio("hello", "helo") > 0.7);
        assertTrue("similarity different", StringUtils.similarityRatio("hello", "world") < 0.5);
        
        System.out.println("  Similarity: PASSED\n");
    }
    
    private static void testUtilities() {
        System.out.println("Testing Utilities...");
        
        // slugify
        assertEquals("slugify", "hello-world", StringUtils.slugify("Hello World!"));
        assertEquals("slugify special", "cafe", StringUtils.slugify("Café"));
        
        // randomString
        String random = StringUtils.randomString(10, "abc");
        assertEquals("randomString length", 10, random.length());
        assertTrue("randomString chars", random.matches("[abc]+"));
        
        // randomAlphanumeric
        String randomAlnum = StringUtils.randomAlphanumeric(20);
        assertEquals("randomAlphanumeric length", 20, randomAlnum.length());
        
        // randomHex
        String randomHex = StringUtils.randomHex(16);
        assertEquals("randomHex length", 16, randomHex.length());
        assertTrue("randomHex chars", randomHex.matches("[0-9A-F]+"));
        
        // containsChinese
        assertTrue("containsChinese", StringUtils.containsChinese("你好 World"));
        assertFalse("containsChinese false", StringUtils.containsChinese("Hello World"));
        
        // extractChinese
        assertEquals("extractChinese", "你好", StringUtils.extractChinese("你好 World"));
        
        System.out.println("  Utilities: PASSED\n");
    }
    
    private static void assertFalse(String message, boolean condition) {
        if (!condition) {
            passed++;
        } else {
            failed++;
            System.out.println("  FAILED: " + message);
        }
    }
}
