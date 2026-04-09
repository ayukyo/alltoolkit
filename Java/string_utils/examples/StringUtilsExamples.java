package string_utils.examples;

import string_utils.StringUtils;
import java.util.*;

/**
 * StringUtils 使用示例
 * 
 * 运行方式：
 * cd Java/string_utils/examples
 * javac -cp .. StringUtilsExamples.java && java -cp ..:./ string_utils.examples.StringUtilsExamples
 */
public class StringUtilsExamples {
    
    public static void main(String[] args) {
        System.out.println("=== StringUtils Examples ===\n");
        
        exampleCaseConversion();
        exampleTrimAndPad();
        exampleTruncate();
        exampleInterpolation();
        exampleEscaping();
        exampleExtraction();
        exampleBase64();
        exampleSimilarity();
        exampleUtilities();
        
        System.out.println("\n=== Examples Complete ===");
    }
    
    private static void exampleCaseConversion() {
        System.out.println("--- Case Conversion Examples ---\n");
        
        String input = "hello_world_test";
        
        System.out.println("Original: " + input);
        System.out.println("camelCase:     " + StringUtils.toCamelCase(input));
        System.out.println("PascalCase:    " + StringUtils.toPascalCase(input));
        System.out.println("snake_case:    " + StringUtils.toSnakeCase(input));
        System.out.println("kebab-case:    " + StringUtils.toKebabCase(input));
        System.out.println("CONSTANT_CASE: " + StringUtils.toConstantCase(input));
        System.out.println("dot.case:      " + StringUtils.toDotCase(input));
        System.out.println("path/case:     " + StringUtils.toPathCase(input));
        System.out.println("space case:    " + StringUtils.toSpaceCase(input));
        System.out.println();
        
        // Real-world example: converting API response fields
        String apiField = "user_first_name";
        System.out.println("API field '" + apiField + "' to Java variable: " + StringUtils.toCamelCase(apiField));
        
        // Converting Java variable to database column
        String javaVar = "userName";
        System.out.println("Java variable '" + javaVar + "' to DB column: " + StringUtils.toSnakeCase(javaVar));
        System.out.println();
    }
    
    private static void exampleTrimAndPad() {
        System.out.println("--- Trim and Pad Examples ---\n");
        
        // Formatting numbers for display
        System.out.println("Formatting numbers:");
        for (int i = 1; i <= 5; i++) {
            System.out.println("  " + StringUtils.zeroPad(String.valueOf(i), 3));
        }
        System.out.println();
        
        // Creating a formatted table
        System.out.println("Creating formatted output:");
        String[] names = {"Alice", "Bob", "Charlie"};
        int[] ages = {25, 30, 35};
        
        for (int i = 0; i < names.length; i++) {
            String name = StringUtils.padRight(names[i], 10, ' ');
            String age = StringUtils.padLeft(String.valueOf(ages[i]), 3, ' ');
            System.out.println("  | " + name + " | " + age + " |");
        }
        System.out.println();
        
        // Centering text
        String title = "Welcome";
        System.out.println(StringUtils.center(title, 30, '='));
        System.out.println();
    }
    
    private static void exampleTruncate() {
        System.out.println("--- Truncate Examples ---\n");
        
        String longText = "This is a very long description that needs to be truncated for display purposes.";
        
        System.out.println("Original: " + longText);
        System.out.println("Truncated (20 chars): " + StringUtils.truncate(longText, 20));
        System.out.println("Truncated (30 chars): " + StringUtils.truncate(longText, 30, " [more]"));
        System.out.println();
        
        // Truncating by words for summaries
        String article = "Java is a versatile programming language. " +
                        "It runs on billions of devices worldwide. " +
                        "From mobile apps to enterprise systems.";
        
        System.out.println("Article preview:");
        System.out.println(StringUtils.truncateWords(article, 5));
        System.out.println();
    }
    
    private static void exampleInterpolation() {
        System.out.println("--- Interpolation Examples ---\n");
        
        // Template with variables
        Map<String, String> user = new HashMap<>();
        user.put("name", "张三");
        user.put("email", "zhangsan@example.com");
        user.put("role", "管理员");
        
        String template = "欢迎 ${name}！您的邮箱是 ${email}，角色是 ${role}。";
        System.out.println("Template: " + template);
        System.out.println("Result:   " + StringUtils.interpolate(template, user));
        System.out.println();
        
        // Format method
        String greeting = StringUtils.format("你好，{0}！今天是 {1} 年 {2} 月 {3} 日。", 
                                              "李四", "2026", "4", "9");
        System.out.println("Formatted: " + greeting);
        System.out.println();
    }
    
    private static void exampleEscaping() {
        System.out.println("--- Escaping Examples ---\n");
        
        // HTML escaping for safe display
        String userInput = "<script>alert('XSS')</script>";
        System.out.println("User input:  " + userInput);
        System.out.println("HTML escaped: " + StringUtils.escapeHtml(userInput));
        System.out.println();
        
        // JSON escaping
        String jsonValue = "Line 1\nLine 2\tTabbed";
        System.out.println("Original:   " + jsonValue);
        System.out.println("JSON escaped: \"" + StringUtils.escapeJson(jsonValue) + "\"");
        System.out.println();
        
        // SQL escaping (though prepared statements are preferred)
        String name = "O'Brien";
        System.out.println("Name:       " + name);
        System.out.println("SQL escaped: " + StringUtils.escapeSql(name));
        System.out.println();
        
        // URL encoding
        String query = "hello world & 你好";
        System.out.println("Query:      " + query);
        System.out.println("URL encoded: " + StringUtils.urlEncode(query));
        System.out.println();
    }
    
    private static void exampleExtraction() {
        System.out.println("--- Extraction Examples ---\n");
        
        String content = """
            联系我们：
            邮箱：support@example.com, sales@company.org
            网站：https://www.example.com/products
            电话：+8613800138000
            社交媒体：#新品发布 @official_account
            价格：100 元，折扣 20%
            """;
        
        System.out.println("Content:\n" + content);
        
        System.out.println("Extracted emails: " + StringUtils.extractEmails(content));
        System.out.println("Extracted URLs:   " + StringUtils.extractUrls(content));
        System.out.println("Extracted phones: " + StringUtils.extractPhoneNumbers(content));
        System.out.println("Extracted tags:   " + StringUtils.extractHashtags(content));
        System.out.println("Extracted mentions: " + StringUtils.extractMentions(content));
        System.out.println("Extracted numbers:  " + StringUtils.extractNumbers(content));
        System.out.println();
    }
    
    private static void exampleBase64() {
        System.out.println("--- Base64 Examples ---\n");
        
        String secret = "密码：SecurePassword123";
        
        String encoded = StringUtils.base64Encode(secret);
        System.out.println("Original: " + secret);
        System.out.println("Encoded:  " + encoded);
        System.out.println("Decoded:  " + StringUtils.base64Decode(encoded));
        System.out.println();
        
        // URL-safe encoding
        String urlData = "data?param=value&other=test";
        String urlEncoded = StringUtils.base64UrlEncode(urlData);
        System.out.println("URL-safe encoded: " + urlEncoded);
        System.out.println("URL-safe decoded: " + StringUtils.base64UrlDecode(urlEncoded));
        System.out.println();
    }
    
    private static void exampleSimilarity() {
        System.out.println("--- Similarity Examples ---\n");
        
        // Spell checking
        String input = "helo";
        String[] candidates = {"hello", "help", "held", "hero"};
        
        System.out.println("Finding closest match for '" + input + "':");
        String bestMatch = null;
        double bestScore = 0;
        
        for (String candidate : candidates) {
            double score = StringUtils.similarityRatio(input, candidate);
            System.out.println("  " + candidate + ": " + String.format("%.2f", score));
            if (score > bestScore) {
                bestScore = score;
                bestMatch = candidate;
            }
        }
        System.out.println("Best match: " + bestMatch + " (" + String.format("%.2f", bestScore) + ")");
        System.out.println();
        
        // Duplicate detection
        String s1 = "Java 编程语言";
        String s2 = "Java 编程语言";
        String s3 = "Java 程序语言";
        
        System.out.println("Duplicate detection:");
        System.out.println("  '" + s1 + "' vs '" + s2 + "': " + 
                          String.format("%.2f", StringUtils.similarityRatio(s1, s2)));
        System.out.println("  '" + s1 + "' vs '" + s3 + "': " + 
                          String.format("%.2f", StringUtils.similarityRatio(s1, s3)));
        System.out.println();
    }
    
    private static void exampleUtilities() {
        System.out.println("--- Utility Examples ---\n");
        
        // Slugify for URLs
        String title = "Hello World! 这是标题";
        String slug = StringUtils.slugify(title);
        System.out.println("Title: " + title);
        System.out.println("Slug:  " + slug);
        System.out.println("URL:   https://example.com/posts/" + slug);
        System.out.println();
        
        // Generate random tokens
        System.out.println("Random tokens:");
        System.out.println("  API Key:     " + StringUtils.randomAlphanumeric(32));
        System.out.println("  Session ID:  " + StringUtils.randomHex(16));
        System.out.println("  Password:    " + StringUtils.randomString(12, "abcdefghABCDEFGH12345678!@#$"));
        System.out.println();
        
        // Chinese text processing
        String mixed = "Hello 世界！Java 编程 123";
        System.out.println("Mixed text: " + mixed);
        System.out.println("Contains Chinese: " + StringUtils.containsChinese(mixed));
        System.out.println("Chinese only:   " + StringUtils.extractChinese(mixed));
        System.out.println();
        
        // Character statistics
        System.out.println("Character stats for '" + mixed + "':");
        Map<String, Integer> stats = StringUtils.getCharStats(mixed);
        for (Map.Entry<String, Integer> entry : stats.entrySet()) {
            System.out.println("  " + entry.getKey() + ": " + entry.getValue());
        }
        System.out.println();
        
        // Palindrome check
        System.out.println("Palindrome checks:");
        System.out.println("  '上海自来水来自海上': " + StringUtils.isPalindrome("上海自来水来自海上"));
        System.out.println("  'A man a plan a canal Panama': " + StringUtils.isPalindrome("A man a plan a canal Panama"));
        System.out.println("  'hello': " + StringUtils.isPalindrome("hello"));
        System.out.println();
    }
}
