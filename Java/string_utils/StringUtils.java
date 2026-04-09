package string_utils;

import java.util.*;
import java.util.regex.*;
import java.text.Normalizer;

/**
 * StringUtils - Java 字符串工具类
 * 
 * 提供全面的字符串操作功能，包括：
 * - 大小写转换（camelCase、PascalCase、snake_case、kebab-case 等）
 * - 字符串修剪和填充
 * - 截断处理
 * - 模板插值
 * - HTML/XML/JSON/SQL 转义
 * - 模式提取（URL、邮箱、电话、标签等）
 * - 字符统计分析
 * - 字符串操作（反转、替换、插入、删除）
 * - Base64 编码解码
 * - 相似度计算（Levenshtein 距离）
 * - 实用工具（slugify、随机字符串等）
 * 
 * 零依赖，仅使用 Java 标准库
 * 
 * @author AllToolkit
 * @version 1.0.0
 */
public class StringUtils {
    
    // ==================== 常用字符集 ====================
    
    private static final String UPPER_CASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    private static final String LOWER_CASE = "abcdefghijklmnopqrstuvwxyz";
    private static final String DIGITS = "0123456789";
    private static final String ALPHANUMERIC = UPPER_CASE + LOWER_CASE + DIGITS;
    private static final String HEX_DIGITS = "0123456789ABCDEF";
    
    // ==================== 大小写转换 ====================
    
    /**
     * 转换为驼峰命名（camelCase）
     * 
     * @param input 输入字符串
     * @return 驼峰命名格式
     */
    public static String toCamelCase(String input) {
        if (input == null || input.isEmpty()) {
            return input;
        }
        
        // 先分割单词
        List<String> words = splitWords(input);
        if (words.isEmpty()) {
            return "";
        }
        
        StringBuilder result = new StringBuilder();
        result.append(words.get(0).toLowerCase());
        
        for (int i = 1; i < words.size(); i++) {
            String word = words.get(i).toLowerCase();
            if (!word.isEmpty()) {
                result.append(Character.toUpperCase(word.charAt(0)));
                if (word.length() > 1) {
                    result.append(word.substring(1));
                }
            }
        }
        
        return result.toString();
    }
    
    /**
     * 转换为大驼峰命名（PascalCase）
     * 
     * @param input 输入字符串
     * @return 大驼峰命名格式
     */
    public static String toPascalCase(String input) {
        if (input == null || input.isEmpty()) {
            return input;
        }
        
        List<String> words = splitWords(input);
        StringBuilder result = new StringBuilder();
        
        for (String word : words) {
            if (!word.isEmpty()) {
                String lower = word.toLowerCase();
                result.append(Character.toUpperCase(lower.charAt(0)));
                if (lower.length() > 1) {
                    result.append(lower.substring(1));
                }
            }
        }
        
        return result.toString();
    }
    
    /**
     * 转换为蛇形命名（snake_case）
     * 
     * @param input 输入字符串
     * @return 蛇形命名格式
     */
    public static String toSnakeCase(String input) {
        if (input == null || input.isEmpty()) {
            return input;
        }
        
        List<String> words = splitWords(input);
        return String.join("_", words).toLowerCase();
    }
    
    /**
     * 转换为短横线命名（kebab-case）
     * 
     * @param input 输入字符串
     * @return 短横线命名格式
     */
    public static String toKebabCase(String input) {
        if (input == null || input.isEmpty()) {
            return input;
        }
        
        List<String> words = splitWords(input);
        return String.join("-", words).toLowerCase();
    }
    
    /**
     * 转换为常量命名（SCREAMING_SNAKE_CASE）
     * 
     * @param input 输入字符串
     * @return 常量命名格式
     */
    public static String toConstantCase(String input) {
        if (input == null || input.isEmpty()) {
            return input;
        }
        
        List<String> words = splitWords(input);
        return String.join("_", words).toUpperCase();
    }
    
    /**
     * 转换为点分隔命名（dot.case）
     * 
     * @param input 输入字符串
     * @return 点分隔命名格式
     */
    public static String toDotCase(String input) {
        if (input == null || input.isEmpty()) {
            return input;
        }
        
        List<String> words = splitWords(input);
        return String.join(".", words).toLowerCase();
    }
    
    /**
     * 转换为路径命名（path/case）
     * 
     * @param input 输入字符串
     * @return 路径命名格式
     */
    public static String toPathCase(String input) {
        if (input == null || input.isEmpty()) {
            return input;
        }
        
        List<String> words = splitWords(input);
        return String.join("/", words).toLowerCase();
    }
    
    /**
     * 转换为空格分隔（Space Case）
     * 
     * @param input 输入字符串
     * @return 空格分隔格式
     */
    public static String toSpaceCase(String input) {
        if (input == null || input.isEmpty()) {
            return input;
        }
        
        List<String> words = splitWords(input);
        List<String> lowerWords = new ArrayList<>();
        for (String word : words) {
            lowerWords.add(word.toLowerCase());
        }
        return String.join(" ", lowerWords);
    }
    
    /**
     * 转换为句子大小写（Sentence case）
     * 
     * @param input 输入字符串
     * @return 句子大小写格式
     */
    public static String toSentenceCase(String input) {
        if (input == null || input.isEmpty()) {
            return input;
        }
        
        String trimmed = input.trim();
        if (trimmed.isEmpty()) {
            return trimmed;
        }
        
        return Character.toUpperCase(trimmed.charAt(0)) + 
               trimmed.substring(1).toLowerCase();
    }
    
    /**
     * 分割单词
     * 
     * @param input 输入字符串
     * @return 单词列表
     */
    private static List<String> splitWords(String input) {
        List<String> words = new ArrayList<>();
        
        if (input == null || input.isEmpty()) {
            return words;
        }
        
        // 处理各种分隔符和大小写变化
        StringBuilder current = new StringBuilder();
        
        for (int i = 0; i < input.length(); i++) {
            char c = input.charAt(i);
            
            if (c == '_' || c == '-' || c == '.' || c == '/' || c == ' ') {
                if (current.length() > 0) {
                    words.add(current.toString());
                    current = new StringBuilder();
                }
            } else if (Character.isUpperCase(c) && current.length() > 0) {
                // 大写字母表示新单词开始
                words.add(current.toString());
                current = new StringBuilder();
                current.append(c);
            } else if (Character.isDigit(c) && current.length() > 0 && 
                       !Character.isDigit(current.charAt(current.length() - 1))) {
                // 数字开始新单词
                words.add(current.toString());
                current = new StringBuilder();
                current.append(c);
            } else {
                current.append(c);
            }
        }
        
        if (current.length() > 0) {
            words.add(current.toString());
        }
        
        return words;
    }
    
    // ==================== 字符串修剪和填充 ====================
    
    /**
     * 修剪字符串两端空白
     * 
     * @param str 输入字符串
     * @return 修剪后的字符串
     */
    public static String trim(String str) {
        return str == null ? null : str.trim();
    }
    
    /**
     * 修剪字符串左端空白
     * 
     * @param str 输入字符串
     * @return 修剪后的字符串
     */
    public static String trimLeft(String str) {
        if (str == null) return null;
        
        int i = 0;
        while (i < str.length() && Character.isWhitespace(str.charAt(i))) {
            i++;
        }
        return str.substring(i);
    }
    
    /**
     * 修剪字符串右端空白
     * 
     * @param str 输入字符串
     * @return 修剪后的字符串
     */
    public static String trimRight(String str) {
        if (str == null) return null;
        
        int i = str.length() - 1;
        while (i >= 0 && Character.isWhitespace(str.charAt(i))) {
            i--;
        }
        return str.substring(0, i + 1);
    }
    
    /**
     * 左侧填充字符串到指定长度
     * 
     * @param str 输入字符串
     * @param size 目标长度
     * @param padChar 填充字符
     * @return 填充后的字符串
     */
    public static String padLeft(String str, int size, char padChar) {
        if (str == null) return null;
        if (str.length() >= size) return str;
        
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < size - str.length(); i++) {
            result.append(padChar);
        }
        result.append(str);
        return result.toString();
    }
    
    /**
     * 右侧填充字符串到指定长度
     * 
     * @param str 输入字符串
     * @param size 目标长度
     * @param padChar 填充字符
     * @return 填充后的字符串
     */
    public static String padRight(String str, int size, char padChar) {
        if (str == null) return null;
        if (str.length() >= size) return str;
        
        StringBuilder result = new StringBuilder(str);
        for (int i = 0; i < size - str.length(); i++) {
            result.append(padChar);
        }
        return result.toString();
    }
    
    /**
     * 左侧填充零到指定长度
     * 
     * @param str 输入字符串
     * @param size 目标长度
     * @return 填充后的字符串
     */
    public static String zeroPad(String str, int size) {
        return padLeft(str, size, '0');
    }
    
    /**
     * 居中字符串
     * 
     * @param str 输入字符串
     * @param size 目标长度
     * @param padChar 填充字符
     * @return 居中后的字符串
     */
    public static String center(String str, int size, char padChar) {
        if (str == null) return null;
        if (str.length() >= size) return str;
        
        int totalPadding = size - str.length();
        int leftPadding = totalPadding / 2;
        int rightPadding = totalPadding - leftPadding;
        
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < leftPadding; i++) {
            result.append(padChar);
        }
        result.append(str);
        for (int i = 0; i < rightPadding; i++) {
            result.append(padChar);
        }
        return result.toString();
    }
    
    /**
     * 居中字符串（右侧重）
     * 当总填充数为奇数时，右侧多一个字符
     * 
     * @param str 输入字符串
     * @param size 目标长度
     * @param padChar 填充字符
     * @return 居中后的字符串
     */
    public static String centerRight(String str, int size, char padChar) {
        if (str == null) return null;
        if (str.length() >= size) return str;
        
        int totalPadding = size - str.length();
        int leftPadding = totalPadding / 2;
        int rightPadding = totalPadding - leftPadding;
        
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < leftPadding; i++) {
            result.append(padChar);
        }
        result.append(str);
        for (int i = 0; i < rightPadding; i++) {
            result.append(padChar);
        }
        return result.toString();
    }
    
    // ==================== 截断处理 ====================
    
    /**
     * 按长度截断字符串
     * 
     * @param str 输入字符串
     * @param maxLength 最大长度
     * @param suffix 后缀（如 "..."）
     * @return 截断后的字符串
     */
    public static String truncate(String str, int maxLength, String suffix) {
        if (str == null) return null;
        if (str.length() <= maxLength) return str;
        
        String effectiveSuffix = suffix == null ? "" : suffix;
        int truncateLength = maxLength - effectiveSuffix.length();
        if (truncateLength < 0) {
            return effectiveSuffix.substring(0, maxLength);
        }
        
        return str.substring(0, truncateLength) + effectiveSuffix;
    }
    
    /**
     * 按长度截断字符串（默认后缀 "..."）
     * 
     * @param str 输入字符串
     * @param maxLength 最大长度
     * @return 截断后的字符串
     */
    public static String truncate(String str, int maxLength) {
        return truncate(str, maxLength, "...");
    }
    
    /**
     * 按单词数截断字符串
     * 
     * @param str 输入字符串
     * @param maxWords 最大单词数
     * @param suffix 后缀
     * @return 截断后的字符串
     */
    public static String truncateWords(String str, int maxWords, String suffix) {
        if (str == null) return null;
        
        String[] words = str.trim().split("\\s+");
        if (words.length <= maxWords) {
            return str;
        }
        
        String effectiveSuffix = suffix == null ? "" : suffix;
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < maxWords; i++) {
            if (i > 0) result.append(" ");
            result.append(words[i]);
        }
        result.append(effectiveSuffix);
        return result.toString();
    }
    
    /**
     * 按单词数截断字符串（默认后缀 "..."）
     * 
     * @param str 输入字符串
     * @param maxWords 最大单词数
     * @return 截断后的字符串
     */
    public static String truncateWords(String str, int maxWords) {
        return truncateWords(str, maxWords, "...");
    }
    
    // ==================== 模板插值 ====================
    
    /**
     * 模板变量替换（使用 ${var} 语法）
     * 
     * @param template 模板字符串
     * @param variables 变量映射
     * @return 替换后的字符串
     */
    public static String interpolate(String template, Map<String, String> variables) {
        if (template == null || variables == null) return template;
        
        Pattern pattern = Pattern.compile("\\$\\{([^}]+)\\}");
        Matcher matcher = pattern.matcher(template);
        
        StringBuilder result = new StringBuilder();
        while (matcher.find()) {
            String varName = matcher.group(1);
            String replacement = variables.getOrDefault(varName, matcher.group(0));
            matcher.appendReplacement(result, Matcher.quoteReplacement(replacement));
        }
        matcher.appendTail(result);
        
        return result.toString();
    }
    
    /**
     * 格式化字符串（使用 {0}, {1} 语法）
     * 
     * @param template 模板字符串
     * @param args 参数数组
     * @return 格式化后的字符串
     */
    public static String format(String template, Object... args) {
        if (template == null) return null;
        if (args == null || args.length == 0) return template;
        
        String result = template;
        for (int i = 0; i < args.length; i++) {
            String placeholder = "{" + i + "}";
            String value = args[i] == null ? "null" : args[i].toString();
            result = result.replace(placeholder, value);
        }
        return result;
    }
    
    // ==================== 转义处理 ====================
    
    /**
     * HTML 转义
     * 
     * @param str 输入字符串
     * @return 转义后的字符串
     */
    public static String escapeHtml(String str) {
        if (str == null) return null;
        
        return str.replace("&", "&amp;")
                  .replace("<", "&lt;")
                  .replace(">", "&gt;")
                  .replace("\"", "&quot;")
                  .replace("'", "&#39;");
    }
    
    /**
     * HTML 反转义
     * 
     * @param str 输入字符串
     * @return 反转义后的字符串
     */
    public static String unescapeHtml(String str) {
        if (str == null) return null;
        
        return str.replace("&lt;", "<")
                  .replace("&gt;", ">")
                  .replace("&quot;", "\"")
                  .replace("&#39;", "'")
                  .replace("&amp;", "&");
    }
    
    /**
     * XML 转义
     * 
     * @param str 输入字符串
     * @return 转义后的字符串
     */
    public static String escapeXml(String str) {
        if (str == null) return null;
        
        return str.replace("&", "&amp;")
                  .replace("<", "&lt;")
                  .replace(">", "&gt;")
                  .replace("\"", "&quot;")
                  .replace("'", "&apos;");
    }
    
    /**
     * JSON 转义
     * 
     * @param str 输入字符串
     * @return 转义后的字符串
     */
    public static String escapeJson(String str) {
        if (str == null) return null;
        
        StringBuilder result = new StringBuilder();
        for (char c : str.toCharArray()) {
            switch (c) {
                case '"': result.append("\\\""); break;
                case '\\': result.append("\\\\"); break;
                case '\b': result.append("\\b"); break;
                case '\f': result.append("\\f"); break;
                case '\n': result.append("\\n"); break;
                case '\r': result.append("\\r"); break;
                case '\t': result.append("\\t"); break;
                default:
                    if (c < ' ') {
                        result.append(String.format("\\u%04x", (int) c));
                    } else {
                        result.append(c);
                    }
            }
        }
        return result.toString();
    }
    
    /**
     * SQL 转义（防止 SQL 注入）
     * 
     * @param str 输入字符串
     * @return 转义后的字符串
     */
    public static String escapeSql(String str) {
        if (str == null) return null;
        
        return str.replace("'", "''")
                  .replace("\\", "\\\\")
                  .replace("%", "\\%")
                  .replace("_", "\\_");
    }
    
    /**
     * 正则表达式转义
     * 
     * @param str 输入字符串
     * @return 转义后的字符串
     */
    public static String escapeRegex(String str) {
        if (str == null) return null;
        
        return Pattern.quote(str);
    }
    
    /**
     * URL 编码
     * 
     * @param str 输入字符串
     * @return 编码后的字符串
     */
    public static String urlEncode(String str) {
        if (str == null) return null;
        
        try {
            return java.net.URLEncoder.encode(str, "UTF-8");
        } catch (Exception e) {
            return str;
        }
    }
    
    /**
     * URL 解码
     * 
     * @param str 输入字符串
     * @return 解码后的字符串
     */
    public static String urlDecode(String str) {
        if (str == null) return null;
        
        try {
            return java.net.URLDecoder.decode(str, "UTF-8");
        } catch (Exception e) {
            return str;
        }
    }
    
    // ==================== 模式提取 ====================
    
    /**
     * 提取所有邮箱地址
     * 
     * @param text 输入文本
     * @return 邮箱列表
     */
    public static List<String> extractEmails(String text) {
        List<String> emails = new ArrayList<>();
        if (text == null) return emails;
        
        Pattern pattern = Pattern.compile(
            "[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@" +
            "[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*"
        );
        Matcher matcher = pattern.matcher(text);
        
        while (matcher.find()) {
            emails.add(matcher.group());
        }
        
        return emails;
    }
    
    /**
     * 提取所有 URL
     * 
     * @param text 输入文本
     * @return URL 列表
     */
    public static List<String> extractUrls(String text) {
        List<String> urls = new ArrayList<>();
        if (text == null) return urls;
        
        Pattern pattern = Pattern.compile(
            "https?://(?:www\\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\\." +
            "[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)"
        );
        Matcher matcher = pattern.matcher(text);
        
        while (matcher.find()) {
            urls.add(matcher.group());
        }
        
        return urls;
    }
    
    /**
     * 提取所有电话号码（国际格式）
     * 
     * @param text 输入文本
     * @return 电话号码列表
     */
    public static List<String> extractPhoneNumbers(String text) {
        List<String> phones = new ArrayList<>();
        if (text == null) return phones;
        
        Pattern pattern = Pattern.compile("\\+[1-9]\\d{6,14}");
        Matcher matcher = pattern.matcher(text);
        
        while (matcher.find()) {
            phones.add(matcher.group());
        }
        
        return phones;
    }
    
    /**
     * 提取所有标签（#hashtag）
     * 
     * @param text 输入文本
     * @return 标签列表
     */
    public static List<String> extractHashtags(String text) {
        List<String> hashtags = new ArrayList<>();
        if (text == null) return hashtags;
        
        Pattern pattern = Pattern.compile("#(\\w+)");
        Matcher matcher = pattern.matcher(text);
        
        while (matcher.find()) {
            hashtags.add(matcher.group(1));
        }
        
        return hashtags;
    }
    
    /**
     * 提取所有提及（@mention）
     * 
     * @param text 输入文本
     * @return 提及列表
     */
    public static List<String> extractMentions(String text) {
        List<String> mentions = new ArrayList<>();
        if (text == null) return mentions;
        
        // 使用负向后顾排除邮箱地址中的 @
        Pattern pattern = Pattern.compile("(?<![\\w.])@(\\w+)");
        Matcher matcher = pattern.matcher(text);
        
        while (matcher.find()) {
            mentions.add(matcher.group(1));
        }
        
        return mentions;
    }
    
    /**
     * 提取所有数字
     * 
     * @param text 输入文本
     * @return 数字列表
     */
    public static List<String> extractNumbers(String text) {
        List<String> numbers = new ArrayList<>();
        if (text == null) return numbers;
        
        Pattern pattern = Pattern.compile("-?\\d+(?:\\.\\d+)?");
        Matcher matcher = pattern.matcher(text);
        
        while (matcher.find()) {
            numbers.add(matcher.group());
        }
        
        return numbers;
    }
    
    // ==================== 字符统计分析 ====================
    
    /**
     * 统计字母数量
     * 
     * @param str 输入字符串
     * @return 字母数量
     */
    public static int countLetters(String str) {
        if (str == null) return 0;
        
        int count = 0;
        for (char c : str.toCharArray()) {
            if (Character.isLetter(c)) count++;
        }
        return count;
    }
    
    /**
     * 统计数字数量
     * 
     * @param str 输入字符串
     * @return 数字数量
     */
    public static int countDigits(String str) {
        if (str == null) return 0;
        
        int count = 0;
        for (char c : str.toCharArray()) {
            if (Character.isDigit(c)) count++;
        }
        return count;
    }
    
    /**
     * 统计空白字符数量
     * 
     * @param str 输入字符串
     * @return 空白字符数量
     */
    public static int countWhitespace(String str) {
        if (str == null) return 0;
        
        int count = 0;
        for (char c : str.toCharArray()) {
            if (Character.isWhitespace(c)) count++;
        }
        return count;
    }
    
    /**
     * 统计特殊字符数量
     * 
     * @param str 输入字符串
     * @return 特殊字符数量
     */
    public static int countSpecialChars(String str) {
        if (str == null) return 0;
        
        int count = 0;
        for (char c : str.toCharArray()) {
            if (!Character.isLetterOrDigit(c) && !Character.isWhitespace(c)) {
                count++;
            }
        }
        return count;
    }
    
    /**
     * 获取字符统计信息
     * 
     * @param str 输入字符串
     * @return 统计信息 Map
     */
    public static Map<String, Integer> getCharStats(String str) {
        Map<String, Integer> stats = new HashMap<>();
        if (str == null) return stats;
        
        stats.put("total", str.length());
        stats.put("letters", countLetters(str));
        stats.put("digits", countDigits(str));
        stats.put("whitespace", countWhitespace(str));
        stats.put("special", countSpecialChars(str));
        stats.put("uppercase", countUppercase(str));
        stats.put("lowercase", countLowercase(str));
        
        return stats;
    }
    
    private static int countUppercase(String str) {
        int count = 0;
        for (char c : str.toCharArray()) {
            if (Character.isUpperCase(c)) count++;
        }
        return count;
    }
    
    private static int countLowercase(String str) {
        int count = 0;
        for (char c : str.toCharArray()) {
            if (Character.isLowerCase(c)) count++;
        }
        return count;
    }
    
    // ==================== 字符串操作 ====================
    
    /**
     * 反转字符串
     * 
     * @param str 输入字符串
     * @return 反转后的字符串
     */
    public static String reverse(String str) {
        if (str == null) return null;
        return new StringBuilder(str).reverse().toString();
    }
    
    /**
     * 替换所有匹配的子串
     * 
     * @param str 输入字符串
     * @param target 目标子串
     * @param replacement 替换内容
     * @param maxCount 最大替换次数（-1 表示全部替换）
     * @return 替换后的字符串
     */
    public static String replace(String str, String target, String replacement, int maxCount) {
        if (str == null || target == null || target.isEmpty()) return str;
        if (maxCount == 0) return str;
        
        StringBuilder result = new StringBuilder();
        int index = 0;
        int count = 0;
        int lastIndex = 0;
        
        while ((index = str.indexOf(target, lastIndex)) != -1) {
            if (maxCount >= 0 && count >= maxCount) {
                break;
            }
            result.append(str, lastIndex, index);
            result.append(replacement);
            lastIndex = index + target.length();
            count++;
        }
        
        result.append(str.substring(lastIndex));
        return result.toString();
    }
    
    /**
     * 插入字符串到指定位置
     * 
     * @param str 原字符串
     * @param insert 要插入的字符串
     * @param position 插入位置
     * @return 插入后的字符串
     */
    public static String insert(String str, String insert, int position) {
        if (str == null) return null;
        if (insert == null) insert = "";
        
        int pos = Math.max(0, Math.min(position, str.length()));
        return str.substring(0, pos) + insert + str.substring(pos);
    }
    
    /**
     * 删除指定位置的字符
     * 
     * @param str 原字符串
     * @param start 起始位置
     * @param end 结束位置（不包含）
     * @return 删除后的字符串
     */
    public static String delete(String str, int start, int end) {
        if (str == null) return null;
        
        int s = Math.max(0, start);
        int e = Math.min(str.length(), end);
        
        if (s >= e) return str;
        
        return str.substring(0, s) + str.substring(e);
    }
    
    /**
     * 重复字符串多次
     * 
     * @param str 输入字符串
     * @param count 重复次数
     * @return 重复后的字符串
     */
    public static String repeat(String str, int count) {
        if (str == null || count <= 0) return "";
        
        StringBuilder result = new StringBuilder(str.length() * count);
        for (int i = 0; i < count; i++) {
            result.append(str);
        }
        return result.toString();
    }
    
    /**
     * 首字母大写
     * 
     * @param str 输入字符串
     * @return 首字母大写后的字符串
     */
    public static String capitalize(String str) {
        if (str == null || str.isEmpty()) return str;
        return Character.toUpperCase(str.charAt(0)) + str.substring(1);
    }
    
    /**
     * 首字母小写
     * 
     * @param str 输入字符串
     * @return 首字母小写后的字符串
     */
    public static String uncapitalize(String str) {
        if (str == null || str.isEmpty()) return str;
        return Character.toLowerCase(str.charAt(0)) + str.substring(1);
    }
    
    /**
     * 交换大小写
     * 
     * @param str 输入字符串
     * @return 交换大小写后的字符串
     */
    public static String swapCase(String str) {
        if (str == null) return null;
        
        StringBuilder result = new StringBuilder();
        for (char c : str.toCharArray()) {
            if (Character.isUpperCase(c)) {
                result.append(Character.toLowerCase(c));
            } else if (Character.isLowerCase(c)) {
                result.append(Character.toUpperCase(c));
            } else {
                result.append(c);
            }
        }
        return result.toString();
    }
    
    // ==================== Base64 编码解码 ====================
    
    /**
     * Base64 编码
     * 
     * @param str 输入字符串
     * @return Base64 编码结果
     */
    public static String base64Encode(String str) {
        if (str == null) return null;
        
        try {
            return java.util.Base64.getEncoder().encodeToString(str.getBytes("UTF-8"));
        } catch (Exception e) {
            return null;
        }
    }
    
    /**
     * Base64 解码
     * 
     * @param base64 Base64 编码字符串
     * @return 解码后的字符串
     */
    public static String base64Decode(String base64) {
        if (base64 == null) return null;
        
        try {
            return new String(java.util.Base64.getDecoder().decode(base64), "UTF-8");
        } catch (Exception e) {
            return null;
        }
    }
    
    /**
     * Base64URL 编码（URL 安全）
     * 
     * @param str 输入字符串
     * @return Base64URL 编码结果
     */
    public static String base64UrlEncode(String str) {
        if (str == null) return null;
        
        try {
            return java.util.Base64.getUrlEncoder().encodeToString(str.getBytes("UTF-8"));
        } catch (Exception e) {
            return null;
        }
    }
    
    /**
     * Base64URL 解码
     * 
     * @param base64Url Base64URL 编码字符串
     * @return 解码后的字符串
     */
    public static String base64UrlDecode(String base64Url) {
        if (base64Url == null) return null;
        
        try {
            return new String(java.util.Base64.getUrlDecoder().decode(base64Url), "UTF-8");
        } catch (Exception e) {
            return null;
        }
    }
    
    // ==================== 相似度计算 ====================
    
    /**
     * 计算 Levenshtein 编辑距离
     * 
     * @param s1 字符串 1
     * @param s2 字符串 2
     * @return 编辑距离
     */
    public static int levenshteinDistance(String s1, String s2) {
        if (s1 == null || s2 == null) return -1;
        
        int len1 = s1.length();
        int len2 = s2.length();
        
        // 优化：处理空字符串
        if (len1 == 0) return len2;
        if (len2 == 0) return len1;
        
        // 创建矩阵
        int[][] matrix = new int[len1 + 1][len2 + 1];
        
        // 初始化边界
        for (int i = 0; i <= len1; i++) {
            matrix[i][0] = i;
        }
        for (int j = 0; j <= len2; j++) {
            matrix[0][j] = j;
        }
        
        // 填充矩阵
        for (int i = 1; i <= len1; i++) {
            for (int j = 1; j <= len2; j++) {
                int cost = (s1.charAt(i - 1) == s2.charAt(j - 1)) ? 0 : 1;
                matrix[i][j] = Math.min(
                    Math.min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1),
                    matrix[i - 1][j - 1] + cost
                );
            }
        }
        
        return matrix[len1][len2];
    }
    
    /**
     * 计算相似度比率（0-1）
     * 
     * @param s1 字符串 1
     * @param s2 字符串 2
     * @return 相似度比率
     */
    public static double similarityRatio(String s1, String s2) {
        if (s1 == null || s2 == null) return 0.0;
        if (s1.equals(s2)) return 1.0;
        
        int distance = levenshteinDistance(s1, s2);
        int maxLen = Math.max(s1.length(), s2.length());
        
        if (maxLen == 0) return 1.0;
        
        return 1.0 - ((double) distance / maxLen);
    }
    
    // ==================== 实用工具 ====================
    
    /**
     * 生成 Slug（URL 友好字符串）
     * 
     * @param str 输入字符串
     * @return Slug 字符串
     */
    public static String slugify(String str) {
        if (str == null) return null;
        
        // 转小写
        String result = str.toLowerCase();
        
        // 移除重音
        result = Normalizer.normalize(result, Normalizer.Form.NFD)
                          .replaceAll("\\p{InCombiningDiacriticalMarks}+", "");
        
        // 替换非字母数字字符为连字符
        result = result.replaceAll("[^a-z0-9\\s-]", "");
        
        // 多个空白替换为单个连字符
        result = result.trim().replaceAll("[\\s-]+", "-");
        
        return result;
    }
    
    /**
     * 生成随机字符串
     * 
     * @param length 长度
     * @param charset 字符集
     * @return 随机字符串
     */
    public static String randomString(int length, String charset) {
        if (length <= 0 || charset == null || charset.isEmpty()) return "";
        
        Random random = new Random();
        StringBuilder result = new StringBuilder(length);
        
        for (int i = 0; i < length; i++) {
            result.append(charset.charAt(random.nextInt(charset.length())));
        }
        
        return result.toString();
    }
    
    /**
     * 生成随机字母数字字符串
     * 
     * @param length 长度
     * @return 随机字符串
     */
    public static String randomAlphanumeric(int length) {
        return randomString(length, ALPHANUMERIC);
    }
    
    /**
     * 生成随机十六进制字符串
     * 
     * @param length 长度
     * @return 随机十六进制字符串
     */
    public static String randomHex(int length) {
        return randomString(length, HEX_DIGITS);
    }
    
    /**
     * 检查字符串是否包含中文字符
     * 
     * @param str 输入字符串
     * @return 是否包含中文
     */
    public static boolean containsChinese(String str) {
        if (str == null) return false;
        
        for (char c : str.toCharArray()) {
            if (c >= '\u4e00' && c <= '\u9fa5') {
                return true;
            }
        }
        return false;
    }
    
    /**
     * 提取中文字符
     * 
     * @param str 输入字符串
     * @return 中文字符串
     */
    public static String extractChinese(String str) {
        if (str == null) return null;
        
        StringBuilder result = new StringBuilder();
        for (char c : str.toCharArray()) {
            if (c >= '\u4e00' && c <= '\u9fa5') {
                result.append(c);
            }
        }
        return result.toString();
    }
    
    /**
     * 检查字符串是否为回文
     * 
     * @param str 输入字符串
     * @return 是否为回文
     */
    public static boolean isPalindrome(String str) {
        if (str == null) return false;
        
        String cleaned = str.toLowerCase().replaceAll("[^a-z0-9\u4e00-\u9fa5]", "");
        return cleaned.equals(new StringBuilder(cleaned).reverse().toString());
    }
    
    /**
     * 连接字符串数组
     * 
     * @param delimiter 分隔符
     * @param elements 元素数组
     * @return 连接后的字符串
     */
    public static String join(String delimiter, String... elements) {
        if (elements == null || elements.length == 0) return "";
        if (delimiter == null) delimiter = "";
        
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < elements.length; i++) {
            if (i > 0) result.append(delimiter);
            result.append(elements[i] == null ? "" : elements[i]);
        }
        return result.toString();
    }
    
    /**
     * 连接字符串集合
     * 
     * @param delimiter 分隔符
     * @param elements 元素集合
     * @return 连接后的字符串
     */
    public static String join(String delimiter, Collection<String> elements) {
        if (elements == null || elements.isEmpty()) return "";
        if (delimiter == null) delimiter = "";
        
        StringBuilder result = new StringBuilder();
        boolean first = true;
        for (String element : elements) {
            if (!first) result.append(delimiter);
            result.append(element == null ? "" : element);
            first = false;
        }
        return result.toString();
    }
    
    /**
     * 分割字符串为列表
     * 
     * @param str 输入字符串
     * @param delimiter 分隔符
     * @return 字符串列表
     */
    public static List<String> split(String str, String delimiter) {
        List<String> result = new ArrayList<>();
        if (str == null || delimiter == null || delimiter.isEmpty()) return result;
        
        String[] parts = str.split(Pattern.quote(delimiter));
        result.addAll(Arrays.asList(parts));
        return result;
    }
}
