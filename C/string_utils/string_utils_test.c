/**
 * @file string_utils_test.c
 * @brief C语言字符串工具库单元测试
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-04
 *
 * 覆盖场景:
 * - 正常操作
 * - 边界值处理
 * - 异常情况（NULL指针、空字符串）
 */

#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "string_utils.h"

// 测试计数器
static int tests_passed = 0;
static int tests_failed = 0;

#define TEST(name) void test_##name()
#define RUN_TEST(name) do { \
    printf("  Testing %s... ", #name); \
    test_##name(); \
    printf("PASSED\n"); \
    tests_passed++; \
} while(0)

#define ASSERT_EQ(expected, actual) do { \
    if ((expected) != (actual)) { \
        printf("FAILED: Expected %d, got %d\n", (expected), (actual)); \
        tests_failed++; \
        return; \
    } \
} while(0)

#define ASSERT_STR_EQ(expected, actual) do { \
    if (strcmp((expected), (actual)) != 0) { \
        printf("FAILED: Expected \"%s\", got \"%s\"\n", (expected), (actual)); \
        tests_failed++; \
        return; \
    } \
} while(0)

#define ASSERT_TRUE(expr) do { \
    if (!(expr)) { \
        printf("FAILED: Assertion failed: %s\n", #expr); \
        tests_failed++; \
        return; \
    } \
} while(0)

#define ASSERT_FALSE(expr) ASSERT_TRUE(!(expr))

// =============================================================================
// 空白字符检测测试
// =============================================================================

TEST(is_whitespace_basic) {
    ASSERT_TRUE(is_whitespace(' '));
    ASSERT_TRUE(is_whitespace('\t'));
    ASSERT_TRUE(is_whitespace('\n'));
    ASSERT_TRUE(is_whitespace('\r'));
    ASSERT_FALSE(is_whitespace('a'));
    ASSERT_FALSE(is_whitespace('1'));
    ASSERT_FALSE(is_whitespace('\0'));
}

// =============================================================================
// 字符串修剪测试
// =============================================================================

TEST(trim_left_basic) {
    char str[] = "  hello";
    str_trim_left(str);
    ASSERT_STR_EQ("hello", str);
}

TEST(trim_left_no_whitespace) {
    char str[] = "hello";
    str_trim_left(str);
    ASSERT_STR_EQ("hello", str);
}

TEST(trim_left_all_whitespace) {
    char str[] = "   ";
    str_trim_left(str);
    ASSERT_STR_EQ("", str);
}

TEST(trim_left_empty) {
    char str[] = "";
    str_trim_left(str);
    ASSERT_STR_EQ("", str);
}

TEST(trim_left_null) {
    char *result = str_trim_left(NULL);
    ASSERT_TRUE(result == NULL);
}

TEST(trim_right_basic) {
    char str[] = "hello  ";
    str_trim_right(str);
    ASSERT_STR_EQ("hello", str);
}

TEST(trim_right_no_whitespace) {
    char str[] = "hello";
    str_trim_right(str);
    ASSERT_STR_EQ("hello", str);
}

TEST(trim_right_all_whitespace) {
    char str[] = "   ";
    str_trim_right(str);
    ASSERT_STR_EQ("", str);
}

TEST(trim_right_empty) {
    char str[] = "";
    str_trim_right(str);
    ASSERT_STR_EQ("", str);
}

TEST(trim_right_null) {
    char *result = str_trim_right(NULL);
    ASSERT_TRUE(result == NULL);
}

TEST(trim_both_sides) {
    char str[] = "  hello world  ";
    str_trim(str);
    ASSERT_STR_EQ("hello world", str);
}

TEST(trim_tabs_and_newlines) {
    char str[] = "\t\nhello\r\n";
    str_trim(str);
    ASSERT_STR_EQ("hello", str);
}

// =============================================================================
// 大小写转换测试
// =============================================================================

TEST(to_lower_basic) {
    char str[] = "HELLO WORLD";
    str_to_lower(str);
    ASSERT_STR_EQ("hello world", str);
}

TEST(to_lower_mixed) {
    char str[] = "Hello World 123";
    str_to_lower(str);
    ASSERT_STR_EQ("hello world 123", str);
}

TEST(to_lower_already_lower) {
    char str[] = "hello";
    str_to_lower(str);
    ASSERT_STR_EQ("hello", str);
}

TEST(to_lower_empty) {
    char str[] = "";
    str_to_lower(str);
    ASSERT_STR_EQ("", str);
}

TEST(to_lower_null) {
    char *result = str_to_lower(NULL);
    ASSERT_TRUE(result == NULL);
}

TEST(to_upper_basic) {
    char str[] = "hello world";
    str_to_upper(str);
    ASSERT_STR_EQ("HELLO WORLD", str);
}

TEST(to_upper_mixed) {
    char str[] = "Hello World 123";
    str_to_upper(str);
    ASSERT_STR_EQ("HELLO WORLD 123", str);
}

TEST(to_upper_already_upper) {
    char str[] = "HELLO";
    str_to_upper(str);
    ASSERT_STR_EQ("HELLO", str);
}

TEST(to_upper_empty) {
    char str[] = "";
    str_to_upper(str);
    ASSERT_STR_EQ("", str);
}

TEST(to_upper_null) {
    char *result = str_to_upper(NULL);
    ASSERT_TRUE(result == NULL);
}

// =============================================================================
// 字符串反转测试
// =============================================================================

TEST(reverse_basic) {
    char str[] = "hello";
    str_reverse(str);
    ASSERT_STR_EQ("olleh", str);
}

TEST(reverse_even_length) {
    char str[] = "abcd";
    str_reverse(str);
    ASSERT_STR_EQ("dcba", str);
}

TEST(reverse_single_char) {
    char str[] = "x";
    str_reverse(str);
    ASSERT_STR_EQ("x", str);
}

TEST(reverse_empty) {
    char str[] = "";
    str_reverse(str);
    ASSERT_STR_EQ("", str);
}

TEST(reverse_null) {
    char *result = str_reverse(NULL);
    ASSERT_TRUE(result == NULL);
}

// =============================================================================
// 前缀后缀检查测试
// =============================================================================

TEST(starts_with_basic) {
    ASSERT_TRUE(str_starts_with("hello world", "hello"));
    ASSERT_FALSE(str_starts_with("hello world", "world"));
}

TEST(starts_with_exact_match) {
    ASSERT_TRUE(str_starts_with("hello", "hello"));
}

TEST(starts_with_longer_prefix) {
    ASSERT_FALSE(str_starts_with("hi", "hello"));
}

TEST(starts_with_empty_prefix) {
    ASSERT_TRUE(str_starts_with("hello", ""));
}

TEST(starts_with_empty_string) {
    ASSERT_FALSE(str_starts_with("", "hello"));
}

TEST(starts_with_both_empty) {
    ASSERT_TRUE(str_starts_with("", ""));
}

TEST(starts_with_null_str) {
    ASSERT_FALSE(str_starts_with(NULL, "hello"));
}

TEST(starts_with_null_prefix) {
    ASSERT_FALSE(str_starts_with("hello", NULL));
}

TEST(ends_with_basic) {
    ASSERT_TRUE(str_ends_with("hello world", "world"));
    ASSERT_FALSE(str_ends_with("hello world", "hello"));
}

TEST(ends_with_exact_match) {
    ASSERT_TRUE(str_ends_with("hello", "hello"));
}

TEST(ends_with_longer_suffix) {
    ASSERT_FALSE(str_ends_with("hi", "hello"));
}

TEST(ends_with_empty_suffix) {
    ASSERT_TRUE(str_ends_with("hello", ""));
}

TEST(ends_with_empty_string) {
    ASSERT_FALSE(str_ends_with("", "hello"));
}

TEST(ends_with_both_empty) {
    ASSERT_TRUE(str_ends_with("", ""));
}

TEST(ends_with_null_str) {
    ASSERT_FALSE(str_ends_with(NULL, "hello"));
}

TEST(ends_with_null_suffix) {
    ASSERT_FALSE(str_ends_with("hello", NULL));
}

// =============================================================================
// 子串计数测试
// =============================================================================

TEST(count_basic) {
    ASSERT_EQ(2, str_count("hello hello", "hello"));
}

TEST(count_overlapping) {
    ASSERT_EQ(2, str_count("aaa", "aa"));  // Non-overlapping: "aa" at positions 0 and 1
}

TEST(count_not_found) {
    ASSERT_EQ(0, str_count("hello", "world"));
}

TEST(count_empty_substr) {
    ASSERT_EQ(0, str_count("hello", ""));
}

TEST(count_empty_string) {
    ASSERT_EQ(0, str_count("", "hello"));
}

TEST(count_single_char) {
    ASSERT_EQ(3, str_count("hello", "l"));
}

TEST(count_null_str) {
    ASSERT_EQ(0, str_count(NULL, "hello"));
}

TEST(count_null_substr) {
    ASSERT_EQ(0, str_count("hello", NULL));
}

// =============================================================================
// 安全复制测试
// =============================================================================

TEST(copy_safe_basic) {
    char dest[20];
    size_t copied = str_copy_safe(dest, "hello", 20);
    ASSERT_STR_EQ("hello", dest);
    ASSERT_EQ(5, copied);
}

TEST(copy_safe_exact_size) {
    char dest[6];
    size_t copied = str_copy_safe(dest, "hello", 6);
    ASSERT_STR_EQ("hello", dest);
    ASSERT_EQ(5, copied);
}

TEST(copy_safe_truncated) {
    char dest[4];
    size_t copied = str_copy_safe(dest, "hello", 4);
    ASSERT_STR_EQ("hel", dest);
    ASSERT_EQ(3, copied);
}

TEST(copy_safe_empty) {
    char dest[10];
    size_t copied = str_copy_safe(dest, "", 10);
    ASSERT_STR_EQ("", dest);
    ASSERT_EQ(0, copied);
}

TEST(copy_safe_size_one) {
    char dest[1];
    size_t copied = str_copy_safe(dest, "hello", 1);
    ASSERT_STR_EQ("", dest);
    ASSERT_EQ(0, copied);
}

TEST(copy_safe_null_dest) {
    size_t copied = str_copy_safe(NULL, "hello", 10);
    ASSERT_EQ(0, copied);
}

TEST(copy_safe_null_src) {
    char dest[10];
    size_t copied = str_copy_safe(dest, NULL, 10);
    ASSERT_EQ(0, copied);
}

TEST(copy_safe_zero_size) {
    char dest[10];
    size_t copied = str_copy_safe(dest, "hello", 0);
    ASSERT_EQ(0, copied);
}

// =============================================================================
// 主函数
// =============================================================================

int main(void) {
    printf("========================================\n");
    printf("C String Utils Test Suite\n");
    printf("========================================\n\n");

    printf("Whitespace Tests:\n");
    RUN_TEST(is_whitespace_basic);

    printf("\nTrim Tests:\n");
    RUN_TEST(trim_left_basic);
    RUN_TEST(trim_left_no_whitespace);
    RUN_TEST(trim_left_all_whitespace);
    RUN_TEST(trim_left_empty);
    RUN_TEST(trim_left_null);
    RUN_TEST(trim_right_basic);
    RUN_TEST(trim_right_no_whitespace);
    RUN_TEST(trim_right_all_whitespace);
    RUN_TEST(trim_right_empty);
    RUN_TEST(trim_right_null);
    RUN_TEST(trim_both_sides);
    RUN_TEST(trim_tabs_and_newlines);

    printf("\nCase Conversion Tests:\n");
    RUN_TEST(to_lower_basic);
    RUN_TEST(to_lower_mixed);
    RUN_TEST(to_lower_already_lower);
    RUN_TEST(to_lower_empty);
    RUN_TEST(to_lower_null);
    RUN_TEST(to_upper_basic);
    RUN_TEST(to_upper_mixed);
    RUN_TEST(to_upper_already_upper);
    RUN_TEST(to_upper_empty);
    RUN_TEST(to_upper_null);

    printf("\nReverse Tests:\n");
    RUN_TEST(reverse_basic);
    RUN_TEST(reverse_even_length);
    RUN_TEST(reverse_single_char);
    RUN_TEST(reverse_empty);
    RUN_TEST(reverse_null);

    printf("\nStartsWith Tests:\n");
    RUN_TEST(starts_with_basic);
    RUN_TEST(starts_with_exact_match);
    RUN_TEST(starts_with_longer_prefix);
    RUN_TEST(starts_with_empty_prefix);
    RUN_TEST(starts_with_empty_string);
    RUN_TEST(starts_with_both_empty);
    RUN_TEST(starts_with_null_str);
    RUN_TEST(starts_with_null_prefix);

    printf("\nEndsWith Tests:\n");
    RUN_TEST(ends_with_basic);
    RUN_TEST(ends_with_exact_match);
    RUN_TEST(ends_with_longer_suffix);
    RUN_TEST(ends_with_empty_suffix);
    RUN_TEST(ends_with_empty_string);
    RUN_TEST(ends_with_both_empty);
    RUN_TEST(ends_with_null_str);
    RUN_TEST(ends_with_null_suffix);

    printf("\nCount Tests:\n");
    RUN_TEST(count_basic);
    RUN_TEST(count_overlapping);
    RUN_TEST(count_not_found);
    RUN_TEST(count_empty_substr);
    RUN_TEST(count_empty_string);
    RUN_TEST(count_single_char);
    RUN_TEST(count_null_str);
    RUN_TEST(count_null_substr);

    printf("\nCopy Safe Tests:\n");
    RUN_TEST(copy_safe_basic);
    RUN_TEST(copy_safe_exact_size);
    RUN_TEST(copy_safe_truncated);
    RUN_TEST(copy_safe_empty);
    RUN_TEST(copy_safe_size_one);
    RUN_TEST(copy_safe_null_dest);
    RUN_TEST(copy_safe_null_src);
    RUN_TEST(copy_safe_zero_size);

    printf("\n========================================\n");
    printf("Results: %d passed, %d failed\n", tests_passed, tests_failed);
    printf("========================================\n");

    return tests_failed > 0 ? 1 : 0;
}