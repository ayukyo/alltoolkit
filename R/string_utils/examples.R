# examples.R - R 字符串工具库使用示例
# @author AllToolkit
# @version 1.0.0
# @date 2026-04-16

# 加载模块
source("string_utils.R")

cat("========================================\n")
cat("  R string_utils 模块使用示例\n")
cat("========================================\n\n")

# ============================================================================
# 1. 字符串修剪
# ============================================================================
cat("【1. 字符串修剪】\n")
text <- "  hello world  "
cat("原始字符串: '", text, "'\n", sep = "")
cat("trim(): '", trim(text), "'\n", sep = "")
cat("trim_left(): '", trim_left(text), "'\n", sep = "")
cat("trim_right(): '", trim_right(text), "'\n", sep = "")
cat("trim_chars('**hello**', '*'): '", trim_chars("**hello**", "*"), "'\n\n", sep = "")

# ============================================================================
# 2. 字符串分割
# ============================================================================
cat("【2. 字符串分割】\n")
csv <- "apple,banana,cherry"
cat("CSV字符串: ", csv, "\n")
cat("split(): ", paste(split(csv, ","), collapse = " | "), "\n")
lines <- "line1\nline2\nline3"
cat("split_lines(): ", paste(split_lines(lines), collapse = " | "), "\n\n")

# ============================================================================
# 3. 字符串替换
# ============================================================================
cat("【3. 字符串替换】\n")
text <- "hello world, hello R"
cat("原始: ", text, "\n")
cat("replace_all('o', '0'): ", replace_all(text, "o", "0"), "\n")
cat("replace_first('o', '0'): ", replace_first(text, "o", "0"), "\n\n")

# ============================================================================
# 4. 大小写转换
# ============================================================================
cat("【4. 大小写转换】\n")
text <- "hello world"
cat("原始: ", text, "\n")
cat("to_upper(): ", to_upper(text), "\n")
cat("to_title(): ", to_title(text), "\n")
cat("to_sentence(): ", to_sentence(text), "\n")
cat("to_camel(): ", to_camel(text), "\n")
cat("to_snake('HelloWorld'): ", to_snake("HelloWorld"), "\n")
cat("to_kebab('HelloWorld'): ", to_kebab("HelloWorld"), "\n\n")

# ============================================================================
# 5. 字符串验证
# ============================================================================
cat("【5. 字符串验证】\n")
cat("is_empty(''): ", is_empty(""), "\n")
cat("is_blank('   '): ", is_blank("   "), "\n")
cat("is_numeric('123.45'): ", is_numeric("123.45"), "\n")
cat("is_alpha('hello'): ", is_alpha("hello"), "\n")
cat("is_alphanumeric('abc123'): ", is_alphanumeric("abc123"), "\n")
cat("starts_with('hello', 'hel'): ", starts_with("hello", "hel"), "\n")
cat("ends_with('hello', 'llo'): ", ends_with("hello", "llo"), "\n\n")

# ============================================================================
# 6. 字符串查找
# ============================================================================
cat("【6. 字符串查找】\n")
text <- "hello world, hello R"
cat("原始: ", text, "\n")
cat("contains('world'): ", contains(text, "world"), "\n")
cat("count('hello'): ", count(text, "hello"), "\n")
cat("find_first('l'): ", find_first(text, "l"), "\n")
cat("find_last('l'): ", find_last(text, "l"), "\n")
cat("find_all('l'): ", paste(find_all(text, "l"), collapse = ", "), "\n\n")

# ============================================================================
# 7. 字符串填充
# ============================================================================
cat("【7. 字符串填充】\n")
cat("pad_left('42', 5, '0'): '", pad_left("42", 5, "0"), "'\n", sep = "")
cat("pad_right('hello', 10): '", pad_right("hello", 10), "'\n", sep = "")
cat("center('hi', 10): '", center("hi", 10), "'\n\n", sep = "")

# ============================================================================
# 8. 字符串重复与连接
# ============================================================================
cat("【8. 字符串重复与连接】\n")
cat("repeat_str('ab', 3): ", repeat_str("ab", 3), "\n")
cat("join(c('a','b','c'), '-'): ", join(c("a", "b", "c"), "-"), "\n\n")

# ============================================================================
# 9. 字符串截取
# ============================================================================
cat("【9. 字符串截取】\n")
cat("truncate('hello world', 8): ", truncate("hello world", 8), "\n")
cat("substring_before('user@domain.com', '@'): ", substring_before("user@domain.com", "@"), "\n")
cat("substring_after('user@domain.com', '@'): ", substring_after("user@domain.com", "@"), "\n\n")

# ============================================================================
# 10. 空白处理
# ============================================================================
cat("【10. 空白处理】\n")
text <- "hello    world"
cat("原始: '", text, "'\n", sep = "")
cat("normalize_space(): '", normalize_space(text), "'\n", sep = "")
cat("remove_whitespace(): '", remove_whitespace("a b c"), "'\n\n", sep = "")

# ============================================================================
# 11. 其他实用函数
# ============================================================================
cat("【11. 其他实用函数】\n")
cat("reverse('hello'): ", reverse("hello"), "\n")
cat("capitalize('hello'): ", capitalize("hello"), "\n")
cat("random_string(8): ", random_string(8), "\n")
cat("is_palindrome('A man a plan a canal Panama'): ", 
    is_palindrome("A man a plan a canal Panama"), "\n")
cat("char_frequency('hello'): l=", char_frequency("hello")["l"], ", h=", 
    char_frequency("hello")["h"], "\n")
cat("substring_safe('hello', -3, -1): ", substring_safe("hello", -3, -1), "\n\n")

# ============================================================================
# 12. 实际应用场景
# ============================================================================
cat("【12. 实际应用场景】\n\n")

# 数据清洗
cat("--- 数据清洗示例 ---\n")
raw_data <- c("  Alice  ", "BOB", "  charlie")
clean_names <- trim(raw_data)
clean_names <- to_title(clean_names)
cat("原始数据: ", paste(raw_data, collapse = ", "), "\n")
cat("清洗后: ", paste(clean_names, collapse = ", "), "\n\n")

# CSV 处理
cat("--- CSV 处理示例 ---\n")
csv_line <- "apple, banana , cherry ,date"
items <- split(csv_line, ",")
items <- trim(items)
cat("原始CSV: ", csv_line, "\n")
cat("处理后: ", paste(items, collapse = " | "), "\n\n")

# URL 友好转换
cat("--- URL 友好转换 ---\n")
titles <- c("Hello World", "My Blog Post", "R is Awesome!")
slugs <- sapply(titles, function(t) {
  to_lower(to_kebab(t))
})
cat("标题: ", paste(titles, collapse = ", "), "\n")
cat("URL: ", paste(slugs, collapse = ", "), "\n\n")

# 密码/ID 生成
cat("--- 随机ID生成 ---\n")
for (i in 1:3) {
  cat("ID", i, ": ", random_string(12), "\n", sep = "")
}

cat("\n========================================\n")
cat("  版本: ", get_version(), "\n", sep = "")
cat("========================================\n")