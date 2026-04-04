/**
 * @file string_utils.hpp
 * @brief C++ 字符串工具库 - 零依赖、现代 C++17 实现
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-04
 *
 * 提供 30+ 个常用字符串处理函数，涵盖：
 * - 字符串修剪（Trim）
 * - 字符串分割（Split）
 * - 字符串替换（Replace）
 * - 字符串查找（Search）
 * - 大小写转换（Case Conversion）
 * - 字符串验证（Validation）
 * - 子字符串操作（Substring）
 * - 字符串连接与重复（Join & Repeat）
 * - 空白字符处理（Whitespace）
 */

#ifndef ALLTOOLKIT_STRING_UTILS_HPP
#define ALLTOOLKIT_STRING_UTILS_HPP

#include <algorithm>
#include <cctype>
#include <functional>
#include <optional>
#include <regex>
#include <sstream>
#include <string>
#include <string_view>
#include <vector>

namespace alltoolkit {

/**
 * @brief 字符串工具命名空间
 */
namespace string_utils {

// ============================================================================
// 类型定义
// ============================================================================

using StringList = std::vector<std::string>;
using StringView = std::string_view;

// ============================================================================
// 字符判断辅助函数
// ============================================================================

/**
 * @brief 判断字符是否为空白字符
 * @param ch 要判断的字符
 * @return true 如果是空白字符（空格、\t、\n、\r、\f、\v）
 */
[[nodiscard]] inline bool isWhitespace(char ch) noexcept {
    return std::isspace(static_cast<unsigned char>(ch));
}

/**
 * @brief 判断字符是否为字母
 * @param ch 要判断的字符
 * @return true 如果是字母（a-z, A-Z）
 */
[[nodiscard]] inline bool isAlpha(char ch) noexcept {
    return std::isalpha(static_cast<unsigned char>(ch));
}

/**
 * @brief 判断字符是否为数字
 * @param ch 要判断的字符
 * @return true 如果是数字（0-9）
 */
[[nodiscard]] inline bool isDigit(char ch) noexcept {
    return std::isdigit(static_cast<unsigned char>(ch));
}

/**
 * @brief 判断字符是否为字母或数字
 * @param ch 要判断的字符
 * @return true 如果是字母或数字
 */
[[nodiscard]] inline bool isAlphanumeric(char ch) noexcept {
    return std::isalnum(static_cast<unsigned char>(ch));
}

// ============================================================================
// 修剪函数 (Trim)
// ============================================================================

/**
 * @brief 去除字符串左侧的空白字符
 * @param str 输入字符串
 * @return 去除左侧空白后的新字符串
 * @example trimLeft("  hello  ") -> "hello  "
 */
[[nodiscard]] inline std::string trimLeft(StringView str) {
    auto start = std::find_if_not(str.begin(), str.end(), isWhitespace);
    return std::string(start, str.end());
}

/**
 * @brief 去除字符串右侧的空白字符
 * @param str 输入字符串
 * @return 去除右侧空白后的新字符串
 * @example trimRight("  hello  ") -> "  hello"
 */
[[nodiscard]] inline std::string trimRight(StringView str) {
    auto end = std::find_if_not(str.rbegin(), str.rend(), isWhitespace).base();
    return std::string(str.begin(), end);
}

/**
 * @brief 去除字符串两侧的空白字符
 * @param str 输入字符串
 * @return 去除两侧空白后的新字符串
 * @example trim("  hello  ") -> "hello"
 */
[[nodiscard]] inline std::string trim(StringView str) {
    return trimLeft(trimRight(str));
}

/**
 * @brief 去除字符串两侧的指定字符
 * @param str 输入字符串
 * @param chars 要去除的字符集合
 * @return 去除指定字符后的新字符串
 * @example trimChars("xxhelloxx", "x") -> "hello"
 */
[[nodiscard]] inline std::string trimChars(StringView str, StringView chars) {
    if (str.empty() || chars.empty()) return std::string(str);
    
    auto isInChars = [&chars](char c) {
        return chars.find(c) != StringView::npos;
    };
    
    auto start = std::find_if_not(str.begin(), str.end(), isInChars);
    auto end = std::find_if_not(str.rbegin(), str.rend(), isInChars).base();
    
    if (start >= end) return "";
    return std::string(start, end);
}

// ============================================================================
// 分割函数 (Split)
// ============================================================================

/**
 * @brief 按分隔符分割字符串
 * @param str 输入字符串
 * @param delimiter 分隔符
 * @param maxSplits 最大分割次数（-1 表示无限制）
 * @return 分割后的字符串列表
 * @example split("a,b,c", ",") -> {"a", "b", "c"}
 * @example split("a,b,c", ",", 1) -> {"a", "b,c"}
 */
[[nodiscard]] inline StringList split(StringView str, StringView delimiter, int maxSplits = -1) {
    StringList result;
    if (str.empty()) return result;
    if (delimiter.empty()) {
        result.emplace_back(str);
        return result;
    }
    
    size_t start = 0;
    size_t end = str.find(delimiter);
    int splits = 0;
    
    while (end != StringView::npos && (maxSplits < 0 || splits < maxSplits)) {
        result.emplace_back(str.substr(start, end - start));
        start = end + delimiter.length();
        end = str.find(delimiter, start);
        splits++;
    }
    
    result.emplace_back(str.substr(start));
    return result;
}

/**
 * @brief 按字符分割字符串
 * @param str 输入字符串
 * @param delimiter 分隔字符
 * @param maxSplits 最大分割次数（-1 表示无限制）
 * @return 分割后的字符串列表
 * @example splitChar("a,b,c", ',') -> {"a", "b", "c"}
 */
[[nodiscard]] inline StringList splitChar(StringView str, char delimiter, int maxSplits = -1) {
    StringList result;
    if (str.empty()) return result;
    
    size_t start = 0;
    size_t end = str.find(delimiter);
    int splits = 0;
    
    while (end != StringView::npos && (maxSplits < 0 || splits < maxSplits)) {
        result.emplace_back(str.substr(start, end - start));
        start = end + 1;
        end = str.find(delimiter, start);
        splits++;
    }
    
    result.emplace_back(str.substr(start));
    return result;
}

/**
 * @brief 按正则表达式分割字符串
 * @param str 输入字符串
 * @param pattern 正则表达式模式
 * @return 分割后的字符串列表
 * @example splitRegex("a1b2c3", R"(\d)") -> {"a", "b", "c", ""}
 */
[[nodiscard]] inline StringList splitRegex(StringView str, const std::string& pattern) {
    StringList result;
    if (str.empty()) return result;
    
    std::regex re(pattern);
    std::sregex_token_iterator iter(str.begin(), str.end(), re, -1);
    std::sregex_token_iterator end;
    
    for (; iter != end; ++iter) {
        result.emplace_back(*iter);
    }
    
    return result;
}

// ============================================================================
// 替换函数 (Replace)
// ============================================================================

/**
 * @brief 替换字符串中所有匹配的子串
 * @param str 输入字符串
 * @param oldStr 要被替换的子串
 * @param newStr 用于替换的新子串
 * @return 替换后的新字符串
 * @example replace("hello world", "o", "0") -> "hell0 w0rld"
 */
[[nodiscard]] inline std::string replace(StringView str, StringView oldStr, StringView newStr) {
    if (oldStr.empty() || str.find(oldStr) == StringView::npos) {
        return std::string(str);
    }
    
    std::string result;
    result.reserve(str.length());
    
    size_t start = 0;
    size_t pos = str.find(oldStr);
    
    while (pos != StringView::npos) {
        result.append(str.substr(start, pos - start));
        result.append(newStr);
        start = pos + oldStr.length();
        pos = str.find(oldStr, start);
    }
    
    result.append(str.substr(start));
    return result;
}

/**
 * @brief 只替换第一次匹配的子串
 * @param str 输入字符串
 * @param oldStr 要被替换的子串
 * @param newStr 用于替换的新子串
 * @return 替换后的新字符串
 * @example replaceFirst("hello world", "o", "0") -> "hell0 world"
 */
[[nodiscard]] inline std::string replaceFirst(StringView str, StringView oldStr, StringView newStr) {
    if (oldStr.empty()) return std::string(str);
    
    size_t pos = str.find(oldStr);
    if (pos == StringView::npos) return std::string(str);
    
    std::string result(str);
    result.replace(pos, oldStr.length(), newStr);
    return result;
}

/**
 * @brief 替换前 N 次匹配的子串
 * @param str 输入字符串
 * @param oldStr 要被替换的子串
 * @param newStr 用于替换的新子串
 * @param count 最大替换次数
 * @return 替换后的新字符串
 * @example replaceN("hello world", "o", "0", 1) -> "hell0 world"
 */
[[nodiscard]] inline std::string