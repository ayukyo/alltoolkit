# test_string_utils.R - R 字符串工具库测试
# @author AllToolkit
# @version 1.0.0
# @date 2026-04-16

# 加载模块
source("string_utils.R")

# 测试计数器
tests_passed <- 0
tests_failed <- 0

# 测试辅助函数
test_that <- function(description, expr) {
  result <- tryCatch({
    if (eval(expr)) {
      tests_passed <<- tests_passed + 1
      cat("✓ ", description, "\n")
      TRUE
    } else {
      tests_failed <<- tests_failed + 1
      cat("✗ ", description, " (FAILED)\n")
      FALSE
    }
  }, error = function(e) {
    tests_failed <<- tests_failed + 1
    cat("✗ ", description, " (ERROR: ", e$message, ")\n")
    FALSE
  })
  invisible(result)
}

cat("\n")
cat("========================================\n")
cat("  R string_utils 模块测试\n")
cat("========================================\n\n")

# ============================================================================
# 测试修剪函数
# ============================================================================
cat("【修剪函数测试】\n")

test_that("trim() 去除两侧空白", {
  trim("  hello  ") == "hello"
})

test_that("trim() 处理向量化", {
  all(trim(c("  a  ", "b  ", "  c")) == c("a", "b", "c"))
})

test_that("trim_left() 只去除左侧空白", {
  trim_left("  hello  ") == "hello  "
})

test_that("trim_right() 只去除右侧空白", {
  trim_right("  hello  ") == "  hello"
})

test_that("trim_chars() 去除指定字符", {
  trim_chars("xxhelloxx", "x") == "hello"
})

test_that("trim_chars() 去除星号", {
  trim_chars("**hello**", "*") == "hello"
})

# ============================================================================
# 测试分割函数
# ============================================================================
cat("\n【分割函数测试】\n")

test_that("split() 按分隔符分割", {
  identical(split("a,b,c", ","), c("a", "b", "c"))
})

test_that("split() 默认按空白分割", {
  identical(split("one two three"), c("one", "two", "three"))
})

test_that("split_lines() 按行分割", {
  identical(split_lines("line1\nline2\nline3"), c("line1", "line2", "line3"))
})

test_that("split() 空字符串返回空向量", {
  identical(split(""), character(0))
})

# ============================================================================
# 测试替换函数
# ============================================================================
cat("\n【替换函数测试】\n")

test_that("replace_all() 替换所有匹配", {
  replace_all("hello world", "o", "0") == "hell0 w0rld"
})

test_that("replace_first() 只替换第一次", {
  replace_first("hello world", "o", "0") == "hell0 world"
})

test_that("replace() 是 replace_all 的别名", {
  replace("hello", "l", "L") == "heLLo"
})

test_that("replace_all() 支持 fixed 模式", {
  replace_all("a.b.c", ".", "-", fixed = TRUE) == "a-b-c"
})

# ============================================================================
# 测试大小写转换函数
# ============================================================================
cat("\n【大小写转换测试】\n")

test_that("to_upper() 转换为大写", {
  to_upper("hello") == "HELLO"
})

test_that("to_lower() 转换为小写", {
  to_lower("HELLO") == "hello"
})

test_that("to_title() 标题大小写", {
  to_title("hello world") == "Hello World"
})

test_that("to_sentence() 句子大小写", {
  to_sentence("hello world") == "Hello world"
})

test_that("to_camel() 驼峰命名", {
  to_camel("hello_world") == "helloWorld"
})

test_that("to_pascal() 帕斯卡命名", {
  to_pascal("hello_world") == "HelloWorld"
})

test_that("to_snake() 蛇形命名", {
  to_snake("HelloWorld") == "hello_world"
})

test_that("to_kebab() 短横线命名", {
  to_kebab("HelloWorld") == "hello-world"
})

# ============================================================================
# 测试验证函数
# ============================================================================
cat("\n【验证函数测试】\n")

test_that("is_empty() 检测空字符串", {
  is_empty("")
})

test_that("is_empty() 检测 NULL", {
  is_empty(NULL)
})

test_that("is_empty() 非空返回 FALSE", {
  !is_empty("hello")
})

test_that("is_blank() 检测空白字符串", {
  is_blank("   ")
})

test_that("is_numeric() 检测数字字符串", {
  is_numeric("123")
})

test_that("is_numeric() 检测浮点数字符串", {
  is_numeric("12.34")
})

test_that("is_numeric() 非数字返回 FALSE", {
  !is_numeric("abc")
})

test_that("is_alpha() 检测纯字母", {
  is_alpha("hello")
})

test_that("is_alpha() 混合返回 FALSE", {
  !is_alpha("hello123")
})

test_that("is_alphanumeric() 检测字母数字", {
  is_alphanumeric("hello123")
})

test_that("starts_with() 检测前缀", {
  starts_with("hello world", "hello")
})

test_that("ends_with() 检测后缀", {
  ends_with("hello world", "world")
})

test_that("starts_with() 忽略大小写", {
  starts_with("Hello", "hel", ignore_case = TRUE)
})

# ============================================================================
# 测试查找函数
# ============================================================================
cat("\n【查找函数测试】\n")

test_that("contains() 检测包含子串", {
  contains("hello world", "world")
})

test_that("contains() 不包含返回 FALSE", {
  !contains("hello", "xyz")
})

test_that("count() 计算子串出现次数", {
  count("hello world", "o") == 2
})

test_that("find_first() 查找首次出现位置", {
  find_first("hello world", "o") == 5
})

test_that("find_last() 查找最后出现位置", {
  find_last("hello world", "o") == 8
})

test_that("find_all() 查找所有位置", {
  identical(find_all("hello world", "o"), c(5L, 8L))
})

test_that("find_first() 未找到返回 -1", {
  find_first("hello", "x") == -1
})

# ============================================================================
# 测试填充函数
# ============================================================================
cat("\n【填充函数测试】\n")

test_that("pad_left() 左填充空格", {
  pad_left("42", 5) == "   42"
})

test_that("pad_left() 左填充指定字符", {
  pad_left("42", 5, "0") == "00042"
})

test_that("pad_right() 右填充", {
  pad_right("hello", 10) == "hello     "
})

test_that("center() 居中填充", {
  center("hi", 6) == "  hi  "
})

# ============================================================================
# 测试重复与连接函数
# ============================================================================
cat("\n【重复与连接函数测试】\n")

test_that("repeat_str() 重复字符串", {
  repeat_str("ab", 3) == "ababab"
})

test_that("join() 连接字符串向量", {
  join(c("a", "b", "c"), ",") == "a,b,c"
})

test_that("join() 无分隔符连接", {
  join(c("a", "b", "c")) == "abc"
})

# ============================================================================
# 测试截取函数
# ============================================================================
cat("\n【截取函数测试】\n")

test_that("truncate() 截断字符串", {
  truncate("hello world", 8) == "hello..."
})

test_that("truncate() 短字符串不变", {
  truncate("hi", 10) == "hi"
})

test_that("substring_before() 获取分隔符前内容", {
  substring_before("hello@world.com", "@") == "hello"
})

test_that("substring_after() 获取分隔符后内容", {
  substring_after("hello@world.com", "@") == "world.com"
})

# ============================================================================
# 测试空白处理函数
# ============================================================================
cat("\n【空白处理函数测试】\n")

test_that("normalize_space() 合并多个空白", {
  normalize_space("hello    world") == "hello world"
})

test_that("remove_whitespace() 移除所有空白", {
  remove_whitespace("hello world") == "helloworld"
})

# ============================================================================
# 测试其他函数
# ============================================================================
cat("\n【其他函数测试】\n")

test_that("reverse() 反转字符串", {
  reverse("hello") == "olleh"
})

test_that("capitalize() 首字母大写", {
  capitalize("hello") == "Hello"
})

test_that("is_palindrome() 检测回文", {
  is_palindrome("A man a plan a canal Panama")
})

test_that("is_palindrome() 非回文返回 FALSE", {
  !is_palindrome("hello")
})

test_that("char_frequency() 统计字符频率", {
  freq <- char_frequency("hello")
  freq["l"] == 2 && freq["h"] == 1
})

test_that("substring_safe() 安全获取子串", {
  substring_safe("hello", 1, 3) == "hel"
})

test_that("substring_safe() 支持负索引", {
  substring_safe("hello", -3, -1) == "llo"
})

test_that("random_string() 生成长度正确", {
  nchar(random_string(10)) == 10
})

test_that("get_version() 返回版本信息", {
  grepl("string_utils v1.0.0", get_version())
})

# ============================================================================
# 测试总结
# ============================================================================
cat("\n========================================\n")
cat("  测试完成\n")
cat("========================================\n")
cat("通过: ", tests_passed, "\n")
cat("失败: ", tests_failed, "\n")
cat("总计: ", tests_passed + tests_failed, "\n")

if (tests_failed == 0) {
  cat("\n🎉 所有测试通过！\n")
} else {
  cat("\n❌ 存在失败的测试。\n")
}