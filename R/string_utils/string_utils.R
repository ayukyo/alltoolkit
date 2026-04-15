# string_utils.R - R 字符串工具库
# 零依赖、纯 R 实现的字符串处理函数集
# @author AllToolkit
# @version 1.0.0
# @date 2026-04-16
#
# 提供以下功能：
# - 字符串修剪 (trim, trim_left, trim_right)
# - 字符串分割 (split, split_lines)
# - 字符串替换 (replace, replace_first, replace_all)
# - 大小写转换 (to_upper, to_lower, to_title, to_sentence, to_camel, to_snake, to_kebab)
# - 字符串验证 (is_empty, is_blank, is_numeric, is_alpha, is_alphanumeric, starts_with, ends_with)
# - 字符串查找 (contains, count, find_first, find_last, find_all)
# - 字符串填充 (pad_left, pad_right, center)
# - 字符串重复与连接 (repeat_str, join)
# - 字符串截取 (truncate, substring_before, substring_after)
# - 空白字符处理 (normalize_space, remove_whitespace)
# - 字符串反转 (reverse)

# ============================================================================
# 字符串修剪函数 (Trim)
# ============================================================================

#' 去除字符串两侧的空白字符
#' @param str 输入字符串（可以是字符向量）
#' @return 去除两侧空白后的字符串
#' @examples
#' trim("  hello  ")  # "hello"
#' trim(c("  a  ", "b  ", "  c"))  # c("a", "b", "c")
trim <- function(str) {
  gsub("^\\s+|\\s+$", "", str)
}

#' 去除字符串左侧的空白字符
#' @param str 输入字符串
#' @return 去除左侧空白后的字符串
#' @examples
#' trim_left("  hello  ")  # "hello  "
trim_left <- function(str) {
  gsub("^\\s+", "", str)
}

#' 去除字符串右侧的空白字符
#' @param str 输入字符串
#' @return 去除右侧空白后的字符串
#' @examples
#' trim_right("  hello  ")  # "  hello"
trim_right <- function(str) {
  gsub("\\s+$", "", str)
}

#' 去除字符串两侧的指定字符
#' @param str 输入字符串
#' @param chars 要去除的字符集合
#' @return 去除指定字符后的字符串
#' @examples
#' trim_chars("xxhelloxx", "x")  # "hello"
#' trim_chars("**hello**", "*")  # "hello"
trim_chars <- function(str, chars) {
  pattern <- paste0("^[", gsub("([\\[\\]\\(\\)\\{\\}\\^\\$\\.\\*\\+\\?\\|\\\\])", "\\\\\\1", chars), "]+|[", 
                    gsub("([\\[\\]\\(\\)\\{\\}\\^\\$\\.\\*\\+\\?\\|\\\\])", "\\\\\\1", chars), "]+$")
  gsub(pattern, "", str)
}

# ============================================================================
# 字符串分割函数 (Split)
# ============================================================================

#' 按分隔符分割字符串
#' @param str 输入字符串
#' @param delimiter 分隔符（默认为空白字符）
#' @param max_splits 最大分割次数（-1 表示无限制）
#' @return 分割后的字符向量
#' @examples
#' split("a,b,c", ",")  # c("a", "b", "c")
#' split("one two three")  # c("one", "two", "three")
split <- function(str, delimiter = "\\s+", max_splits = -1) {
  if (is_empty(str)) return(character(0))
  
  if (max_splits < 0) {
    return(strsplit(str, delimiter, fixed = FALSE)[[1]])
  }
  
  parts <- strsplit(str, delimiter, fixed = FALSE)[[1]]
  if (length(parts) <= max_splits + 1) {
    return(parts)
  }
  
  # 合并超出部分
  first_parts <- parts[1:max_splits]
  last_part <- paste(parts[(max_splits + 1):length(parts)], collapse = if (delimiter == "\\s+") " " else delimiter)
  c(first_parts, last_part)
}

#' 按行分割字符串
#' @param str 输入字符串
#' @return 行向量
#' @examples
#' split_lines("line1\nline2\nline3")  # c("line1", "line2", "line3")
split_lines <- function(str) {
  if (is_empty(str)) return(character(0))
  strsplit(str, "\n")[[1]]
}

# ============================================================================
# 字符串替换函数 (Replace)
# ============================================================================

#' 替换字符串中所有匹配的子串
#' @param str 输入字符串
#' @param pattern 要被替换的模式（可以是正则表达式）
#' @param replacement 用于替换的新字符串
#' @param fixed 是否禁用正则表达式（默认 FALSE）
#' @return 替换后的字符串
#' @examples
#' replace_all("hello world", "o", "0")  # "hell0 w0rld"
#' replace_all("a.b.c", ".", "-", fixed = TRUE)  # "a-b-c"
replace_all <- function(str, pattern, replacement, fixed = FALSE) {
  gsub(pattern, replacement, str, fixed = fixed)
}

#' 只替换第一次匹配的子串
#' @param str 输入字符串
#' @param pattern 要被替换的模式
#' @param replacement 用于替换的新字符串
#' @param fixed 是否禁用正则表达式（默认 FALSE）
#' @return 替换后的字符串
#' @examples
#' replace_first("hello world", "o", "0")  # "hell0 world"
replace_first <- function(str, pattern, replacement, fixed = FALSE) {
  sub(pattern, replacement, str, fixed = fixed)
}

#' 替换函数的别名（replace_all 的简写）
replace <- function(str, pattern, replacement, fixed = FALSE) {
  replace_all(str, pattern, replacement, fixed)
}

# ============================================================================
# 大小写转换函数 (Case Conversion)
# ============================================================================

#' 转换为大写
#' @param str 输入字符串
#' @return 大写字符串
to_upper <- function(str) {
  toupper(str)
}

#' 转换为小写
#' @param str 输入字符串
#' @return 小写字符串
to_lower <- function(str) {
  tolower(str)
}

#' 转换为标题大小写（每个单词首字母大写）
#' @param str 输入字符串
#' @return 标题大小写字符串
#' @examples
#' to_title("hello world")  # "Hello World"
to_title <- function(str) {
  sapply(str, function(s) {
    words <- strsplit(s, "\\s+")[[1]]
    paste(toupper(substring(words, 1, 1)), tolower(substring(words, 2)), sep = "", collapse = " ")
  }, USE.NAMES = FALSE)
}

#' 转换为句子大小写（首字母大写）
#' @param str 输入字符串
#' @return 句子大小写字符串
#' @examples
#' to_sentence("hello world")  # "Hello world"
to_sentence <- function(str) {
  paste0(toupper(substring(str, 1, 1)), substring(str, 2))
}

#' 转换为驼峰命名法
#' @param str 输入字符串（支持空格、下划线、短横线分隔）
#' @return 驼峰命名字符串
#' @examples
#' to_camel("hello_world")  # "helloWorld"
#' to_camel("hello-world")  # "helloWorld"
to_camel <- function(str) {
  # 先统一为空格分隔
  s <- gsub("[-_]", " ", str)
  words <- strsplit(s, "\\s+")[[1]]
  if (length(words) == 0) return("")
  paste0(tolower(words[1]), paste(toupper(substring(words[-1], 1, 1)), 
                                   tolower(substring(words[-1], 2)), sep = "", collapse = ""))
}

#' 转换为帕斯卡命名法（大驼峰）
#' @param str 输入字符串
#' @return 帕斯卡命名字符串
#' @examples
#' to_pascal("hello_world")  # "HelloWorld"
to_pascal <- function(str) {
  camel <- to_camel(str)
  paste0(toupper(substring(camel, 1, 1)), substring(camel, 2))
}

#' 转换为蛇形命名法
#' @param str 输入字符串
#' @return 蛇形命名字符串
#' @examples
#' to_snake("HelloWorld")  # "hello_world"
#' to_snake("hello-world")  # "hello_world"
to_snake <- function(str) {
  # 先处理短横线
  s <- gsub("-", "_", str)
  # 在大写字母前插入下划线
  s <- gsub("([a-z])([A-Z])", "\\1_\\2", s)
  tolower(s)
}

#' 转换为短横线命名法
#' @param str 输入字符串
#' @return 短横线命名字符串
#' @examples
#' to_kebab("HelloWorld")  # "hello-world"
to_kebab <- function(str) {
  # 先处理下划线
  s <- gsub("_", "-", str)
  # 在大写字母前插入短横线
  s <- gsub("([a-z])([A-Z])", "\\1-\\2", s)
  tolower(s)
}

# ============================================================================
# 字符串验证函数 (Validation)
# ============================================================================

#' 判断字符串是否为空（NULL 或长度为 0）
#' @param str 输入字符串
#' @return 逻辑值
#' @examples
#' is_empty("")  # TRUE
#' is_empty(NULL)  # TRUE
#' is_empty("hello")  # FALSE
is_empty <- function(str) {
  is.null(str) || length(str) == 0 || (length(str) == 1 && str == "")
}

#' 判断字符串是否为空白（空或仅含空白字符）
#' @param str 输入字符串
#' @return 逻辑值
#' @examples
#' is_blank("   ")  # TRUE
#' is_blank("")  # TRUE
#' is_blank("hello")  # FALSE
is_blank <- function(str) {
  if (is_empty(str)) return(TRUE)
  nchar(trim(str)) == 0
}

#' 判断字符串是否为纯数字
#' @param str 输入字符串
#' @return 逻辑值
#' @examples
#' is_numeric("123")  # TRUE
#' is_numeric("12.34")  # TRUE
#' is_numeric("abc")  # FALSE
is_numeric <- function(str) {
  if (is_empty(str)) return(FALSE)
  !is.na(suppressWarnings(as.numeric(str)))
}

#' 判断字符串是否为纯字母
#' @param str 输入字符串
#' @return 逻辑值
#' @examples
#' is_alpha("hello")  # TRUE
#' is_alpha("hello123")  # FALSE
is_alpha <- function(str) {
  if (is_empty(str)) return(FALSE)
  grepl("^[A-Za-z]+$", str)
}

#' 判断字符串是否为字母或数字
#' @param str 输入字符串
#' @return 逻辑值
#' @examples
#' is_alphanumeric("hello123")  # TRUE
#' is_alphanumeric("hello!")  # FALSE
is_alphanumeric <- function(str) {
  if (is_empty(str)) return(FALSE)
  grepl("^[A-Za-z0-9]+$", str)
}

#' 判断字符串是否以指定前缀开头
#' @param str 输入字符串
#' @param prefix 前缀
#' @param ignore_case 是否忽略大小写（默认 FALSE）
#' @return 逻辑值
#' @examples
#' starts_with("hello world", "hello")  # TRUE
starts_with <- function(str, prefix, ignore_case = FALSE) {
  if (is_empty(str) || is_empty(prefix)) return(FALSE)
  if (ignore_case) {
    grepl(paste0("^", tolower(prefix)), tolower(str))
  } else {
    grepl(paste0("^", prefix), str)
  }
}

#' 判断字符串是否以指定后缀结尾
#' @param str 输入字符串
#' @param suffix 后缀
#' @param ignore_case 是否忽略大小写（默认 FALSE）
#' @return 逻辑值
#' @examples
#' ends_with("hello world", "world")  # TRUE
ends_with <- function(str, suffix, ignore_case = FALSE) {
  if (is_empty(str) || is_empty(suffix)) return(FALSE)
  if (ignore_case) {
    grepl(paste0(tolower(suffix), "$"), tolower(str))
  } else {
    grepl(paste0(suffix, "$"), str)
  }
}

# ============================================================================
# 字符串查找函数 (Search)
# ============================================================================

#' 判断字符串是否包含子串
#' @param str 输入字符串
#' @param substr 子串
#' @param ignore_case 是否忽略大小写（默认 FALSE）
#' @return 逻辑值
#' @examples
#' contains("hello world", "world")  # TRUE
contains <- function(str, substr, ignore_case = FALSE) {
  if (is_empty(str) || is_empty(substr)) return(FALSE)
  if (ignore_case) {
    grepl(tolower(substr), tolower(str), fixed = TRUE)
  } else {
    grepl(substr, str, fixed = TRUE)
  }
}

#' 计算子串出现次数
#' @param str 输入字符串
#' @param substr 子串
#' @return 出现次数
#' @examples
#' count("hello world", "o")  # 2
count <- function(str, substr) {
  if (is_empty(str) || is_empty(substr)) return(0)
  length(gregexpr(substr, str, fixed = TRUE)[[1]])
}

#' 查找子串首次出现的位置
#' @param str 输入字符串
#' @param substr 子串
#' @return 位置（从 1 开始，未找到返回 -1）
#' @examples
#' find_first("hello world", "o")  # 5
find_first <- function(str, substr) {
  if (is_empty(str) || is_empty(substr)) return(-1)
  pos <- regexpr(substr, str, fixed = TRUE)
  if (pos == -1) return(-1)
  as.integer(pos)
}

#' 查找子串最后出现的位置
#' @param str 输入字符串
#' @param substr 子串
#' @return 位置（从 1 开始，未找到返回 -1）
#' @examples
#' find_last("hello world", "o")  # 8
find_last <- function(str, substr) {
  if (is_empty(str) || is_empty(substr)) return(-1)
  positions <- gregexpr(substr, str, fixed = TRUE)[[1]]
  if (positions[1] == -1) return(-1)
  as.integer(positions[length(positions)])
}

#' 查找子串所有出现的位置
#' @param str 输入字符串
#' @param substr 子串
#' @return 位置向量（从 1 开始）
#' @examples
#' find_all("hello world", "o")  # c(5, 8)
find_all <- function(str, substr) {
  if (is_empty(str) || is_empty(substr)) return(integer(0))
  positions <- gregexpr(substr, str, fixed = TRUE)[[1]]
  if (positions[1] == -1) return(integer(0))
  as.integer(positions)
}

# ============================================================================
# 字符串填充函数 (Padding)
# ============================================================================

#' 左填充字符串
#' @param str 输入字符串
#' @param width 目标宽度
#' @param pad_char 填充字符（默认为空格）
#' @return 填充后的字符串
#' @examples
#' pad_left("42", 5)  # "   42"
#' pad_left("42", 5, "0")  # "00042"
pad_left <- function(str, width, pad_char = " ") {
  if (is_empty(str)) return(str)
  padding <- width - nchar(str)
  if (padding <= 0) return(str)
  paste0(paste(rep(pad_char, padding), collapse = ""), str)
}

#' 右填充字符串
#' @param str 输入字符串
#' @param width 目标宽度
#' @param pad_char 填充字符（默认为空格）
#' @return 填充后的字符串
#' @examples
#' pad_right("hello", 10)  # "hello     "
pad_right <- function(str, width, pad_char = " ") {
  if (is_empty(str)) return(str)
  padding <- width - nchar(str)
  if (padding <= 0) return(str)
  paste0(str, paste(rep(pad_char, padding), collapse = ""))
}

#' 居中填充字符串
#' @param str 输入字符串
#' @param width 目标宽度
#' @param pad_char 填充字符（默认为空格）
#' @return 填充后的字符串
#' @examples
#' center("hi", 6)  # "  hi  "
center <- function(str, width, pad_char = " ") {
  if (is_empty(str)) return(str)
  padding <- width - nchar(str)
  if (padding <= 0) return(str)
  left_pad <- floor(padding / 2)
  right_pad <- padding - left_pad
  paste0(paste(rep(pad_char, left_pad), collapse = ""), str, 
         paste(rep(pad_char, right_pad), collapse = ""))
}

# ============================================================================
# 字符串重复与连接函数
# ============================================================================

#' 重复字符串
#' @param str 输入字符串
#' @param times 重复次数
#' @return 重复后的字符串
#' @examples
#' repeat_str("ab", 3)  # "ababab"
repeat_str <- function(str, times) {
  if (times <= 0) return("")
  paste(rep(str, times), collapse = "")
}

#' 连接字符串向量
#' @param strings 字符串向量
#' @param separator 分隔符（默认为空）
#' @return 连接后的字符串
#' @examples
#' join(c("a", "b", "c"), ",")  # "a,b,c"
join <- function(strings, separator = "") {
  paste(strings, collapse = separator)
}

# ============================================================================
# 字符串截取函数
# ============================================================================

#' 截断字符串并添加省略号
#' @param str 输入字符串
#' @param max_length 最大长度
#' @param ellipsis 省略号（默认 "..."）
#' @return 截断后的字符串
#' @examples
#' truncate("hello world", 8)  # "hello..."
truncate <- function(str, max_length, ellipsis = "...") {
  if (is_empty(str)) return(str)
  if (nchar(str) <= max_length) return(str)
  paste0(substring(str, 1, max_length - nchar(ellipsis)), ellipsis)
}

#' 获取子串之前的内容
#' @param str 输入字符串
#' @param delimiter 分隔符
#' @return 分隔符之前的字符串，未找到返回原字符串
#' @examples
#' substring_before("hello@world.com", "@")  # "hello"
substring_before <- function(str, delimiter) {
  if (is_empty(str) || is_empty(delimiter)) return(str)
  pos <- regexpr(delimiter, str, fixed = TRUE)
  if (pos == -1) return(str)
  substring(str, 1, pos - 1)
}

#' 获取子串之后的内容
#' @param str 输入字符串
#' @param delimiter 分隔符
#' @return 分隔符之后的字符串，未找到返回原字符串
#' @examples
#' substring_after("hello@world.com", "@")  # "world.com"
substring_after <- function(str, delimiter) {
  if (is_empty(str) || is_empty(delimiter)) return(str)
  pos <- regexpr(delimiter, str, fixed = TRUE)
  if (pos == -1) return(str)
  substring(str, pos + nchar(delimiter))
}

# ============================================================================
# 空白字符处理函数
# ============================================================================

#' 规范化空白字符（多个空白字符合并为单个空格）
#' @param str 输入字符串
#' @return 规范化后的字符串
#' @examples
#' normalize_space("hello    world")  # "hello world"
normalize_space <- function(str) {
  if (is_empty(str)) return(str)
  gsub("\\s+", " ", trim(str))
}

#' 移除所有空白字符
#' @param str 输入字符串
#' @return 移除空白后的字符串
#' @examples
#' remove_whitespace("hello world")  # "helloworld"
remove_whitespace <- function(str) {
  if (is_empty(str)) return(str)
  gsub("\\s+", "", str)
}

# ============================================================================
# 字符串反转函数
# ============================================================================

#' 反转字符串
#' @param str 输入字符串
#' @return 反转后的字符串
#' @examples
#' reverse("hello")  # "olleh"
reverse <- function(str) {
  if (is_empty(str)) return(str)
  sapply(str, function(s) {
    paste(rev(strsplit(s, "")[[1]]), collapse = "")
  }, USE.NAMES = FALSE)
}

# ============================================================================
# 其他实用函数
# ============================================================================

#' 首字母大写
#' @param str 输入字符串
#' @return 首字母大写的字符串
#' @examples
#' capitalize("hello")  # "Hello"
capitalize <- function(str) {
  if (is_empty(str)) return(str)
  paste0(toupper(substring(str, 1, 1)), substring(str, 2))
}

#' 生成随机字符串
#' @param length 字符串长度
#' @param charset 字符集（默认为字母数字）
#' @return 随机字符串
#' @examples
#' random_string(8)  # 随机 8 位字符串
random_string <- function(length = 8, charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") {
  chars <- strsplit(charset, "")[[1]]
  paste(sample(chars, length, replace = TRUE), collapse = "")
}

#' 判断字符串是否为回文
#' @param str 输入字符串
#' @param ignore_case 是否忽略大小写（默认 TRUE）
#' @param ignore_space 是否忽略空白字符（默认 TRUE）
#' @return 逻辑值
#' @examples
#' is_palindrome("A man a plan a canal Panama")  # TRUE
is_palindrome <- function(str, ignore_case = TRUE, ignore_space = TRUE) {
  if (is_empty(str)) return(TRUE)
  s <- str
  if (ignore_case) s <- tolower(s)
  if (ignore_space) s <- remove_whitespace(s)
  s == reverse(s)
}

#' 统计字符串字符频率
#' @param str 输入字符串
#' @return 命名向量，字符为名，频率为值
#' @examples
#' char_frequency("hello")  # c(h=1, e=1, l=2, o=1)
char_frequency <- function(str) {
  if (is_empty(str)) return(integer(0))
  chars <- strsplit(str, "")[[1]]
  table(chars)
}

#' 安全获取子串（支持负索引）
#' @param str 输入字符串
#' @param start 起始位置（从 1 开始，负数表示从末尾）
#' @param end 结束位置（从 1 开始，负数表示从末尾）
#' @return 子串
#' @examples
#' substring_safe("hello", 1, 3)  # "hel"
#' substring_safe("hello", -3, -1)  # "llo"
substring_safe <- function(str, start, end) {
  if (is_empty(str)) return(str)
  len <- nchar(str)
  if (start < 0) start <- len + start + 1
  if (end < 0) end <- len + end + 1
  start <- max(1, start)
  end <- min(len, end)
  if (start > end) return("")
  substring(str, start, end)
}

# 模块信息
.string_utils_version <- "1.0.0"
.string_utils_author <- "AllToolkit"
.string_utils_date <- "2026-04-16"

#' 获取模块版本信息
#' @return 版本信息字符串
get_version <- function() {
  paste0("string_utils v", .string_utils_version, " by ", .string_utils_author, " (", .string_utils_date, ")")
}