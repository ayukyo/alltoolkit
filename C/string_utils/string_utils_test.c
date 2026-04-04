/**
 * @file string_utils_test.c
 * @brief C 语言字符串工具库测试
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "string_utils.h"

static int tests_passed = 0;
static int tests_failed = 0;

#define TEST(name) void test_##name()
#define RUN_TEST(name) do { \
    printf("  Running " #name "... "); \
    test_##name(); \
    printf("OK\n"); \
    tests_passed++; \
} while(0)

#define ASSERT(expr) do { \
    if (!(expr)) { \
        printf("\n    FAILED: %s at line %d\n", #expr, __LINE__); \
        tests_failed++; \
        return; \
    } \
} while(0)

#define ASSERT_STR_EQ(a, b) ASSERT(strcmp((a), (b)) == 0)

/* ==================== Trim Tests ==================== */

TEST(trim_left) {
    char s1[] = "  hello";
    ASSERT_STR_EQ(str_trim_left(s1), "hello");
    
    char s2[] = "hello";
    ASSERT_STR_EQ(str_trim_left(s2), "hello");
    
    char s3[] = "   ";
    ASSERT_STR_EQ(str_trim_left(s3), "");
}

TEST(trim_right) {
    char s1[] = "hello  ";
    str_trim_right(s1);
    ASSERT_STR_EQ(s1, "hello");
    
    char s2[] = "hello";
    str_trim_right(s2);
    ASSERT_STR_EQ(s2, "hello");
}

TEST(trim) {
    char s1[] = "  hello  ";
    ASSERT_STR_EQ(str_trim(s1), "hello");
    
    char s2[] = "\t\nhello\r\n";
    ASSERT_STR_EQ(str_trim(s2), "hello");
}

TEST(trim_chars) {
    char s1[] = "xxhelloxx";
    str_trim_chars(s1, "x");
    ASSERT_STR_EQ(s1, "hello");
    
    char s2[] = "xyhelloyx";
    str_trim_chars(s2, "xy");
    ASSERT_STR_EQ(s2, "hello");
}

/* ==================== Split Tests ==================== */

TEST(split) {
    StringSplitResult r = str_split("a,b,c", ",", 0);
    ASSERT(r.count == 3);
    ASSERT_STR_EQ(r.tokens[0], "a");
    ASSERT_STR_EQ(r.tokens[1], "b");
    ASSERT_STR_EQ(r.tokens[2], "c");
    str_split_free(&r);
}

TEST(split_char) {
    StringSplitResult r = str_split_char("a:b:c", ':', 0);
    ASSERT(r.count == 3);
    ASSERT_STR_EQ(r.tokens[0], "a");
    str_split_free(&r);
}

TEST(split_max) {
    StringSplitResult r = str_split("a,b,c,d", ",", 2);
    ASSERT(r.count == 3);
    ASSERT_STR_EQ(r.tokens[0], "a");
    ASSERT_STR_EQ(r.tokens[1], "b");
    ASSERT_STR_EQ(r.tokens[2], "c,d");
    str_split_free(&r);
}

/* ==================== Replace Tests ==================== */

TEST(replace) {
    char* r = str_replace("hello world", "world", "C");
    ASSERT_STR_EQ(r, "hello C");
    free(r);
}

TEST(replace_all) {
    char* r = str_replace("foo bar foo", "foo", "baz");
    ASSERT_STR_EQ(r, "baz bar baz");
    free(r);
}

TEST(replace_first) {
    char* r = str_replace_first("foo bar foo", "foo", "baz");
    ASSERT_STR_EQ(r, "baz bar foo");
    free(r);
}

TEST(replace_n) {
    char* r = str_replace_n("foo bar foo baz foo", "foo", "X", 2);
    ASSERT_STR_EQ(r, "X bar X baz foo");
    free(r);
}

/* ==================== Search Tests ==================== */

TEST(count) {
    ASSERT(str_count("hello hello hello", "hello") == 3);
    ASSERT(str_count("hello", "xyz") == 0);
    ASSERT(str_count("", "hello") == 0);
}

TEST(starts_with) {
    ASSERT(str_starts_with("hello world", "hello") == true);
    ASSERT(str_starts_with("hello world", "world") == false);
    ASSERT(str_starts_with("", "hello") == false);
}

TEST(ends_with) {
    ASSERT(str_ends_with("hello world", "world") == true);
    ASSERT(str_ends_with("hello world", "hello") == false);
    ASSERT(str_ends_with("", "hello") == false);
}

/* ==================== Case Tests ==================== */

TEST(to_upper) {
    char s[] = "hello";
    str_to_upper(s);
    ASSERT_STR_EQ(s, "HELLO");
}

TEST(to_lower) {
    char s[] = "HELLO";
    str_to_lower(s);
    ASSERT_STR_EQ(s, "hello");
}

TEST(to_upper_copy) {
    char* s = str_to_upper_copy("hello");
    ASSERT_STR_EQ(s, "HELLO");
    free(s);
}

/* ==================== Copy/Concat Tests ==================== */

TEST(copy_safe) {
    char buf[10];
    size_t n = str_copy_safe(buf, "hello world", sizeof(buf));
    ASSERT(n == 9);
    ASSERT_STR_EQ(buf, "hello wor");
}

TEST(concat_safe) {
    char buf[20] = "hello";
    size_t n = str_concat_safe(buf, " world", sizeof(buf));
    ASSERT_STR_EQ(buf, "hello world");
}

TEST(repeat) {
    char* r = str_repeat("ab", 3);
    ASSERT_STR_EQ(r, "ababab");
    free(r);
}

TEST(join_array) {
    const char* arr[] = {"a", "b", "c"};
    char* r = str_join_array(arr, 3, ",");
    ASSERT_STR_EQ(r, "a,b,c");
    free(r);
}

/* ==================== Validation Tests ==================== */

TEST(is_blank) {
    ASSERT(str_is_blank("") == true);
    ASSERT(str_is_blank("   ") == true);
    ASSERT(str_is_blank("\t\n") == true);
    ASSERT(str_is_blank("hello") == false);
    ASSERT(str_is_blank("  hello  ") == false);
}

TEST(is_numeric) {
    ASSERT(str_is_numeric("123") == true);
    ASSERT(str_is_numeric("12.3") == false);
    ASSERT(str_is_numeric("abc") == false);
    ASSERT(str_is_numeric("") == false);
}

TEST(is_integer) {
    ASSERT(str_is_integer("123") == true);
    ASSERT(str_is_integer("-123") == true);
    ASSERT(str_is_integer("+123") == true);
    ASSERT(str_is_integer("12.3") == false);
    ASSERT(str_is_integer("-") == false);
}

TEST(is_float) {
    ASSERT(str_is_float("123.45") == true);
    ASSERT(str_is_float("-123.45") == true);
    ASSERT(str_is_float("123") == true);
    ASSERT(str_is_float("123.45.67") == false);
    ASSERT(str_is_float("abc") == false);
}

TEST(is_alpha) {
    ASSERT(str_is_alpha("hello") == true);
    ASSERT(str_is_alpha("Hello") == true);
    ASSERT(str_is_alpha("hello123") == false);
    ASSERT(str_is_alpha("") == false);
}

TEST(is_alphanumeric) {
    ASSERT(str_is_alphanumeric("hello123") == true);
    ASSERT(str_is_alpha("hello") == true);
    ASSERT(str_is_alphanumeric("hello_123") == false);
}

/* ==================== Substring Tests ==================== */

TEST(substring) {
    char* r = str_substring("hello", 1, 3);
    ASSERT_STR_EQ(r, "ell");
    free(r);
}

TEST(left) {
    char* r = str_left("hello", 3);
    ASSERT_STR_EQ(r, "hel");
    free(r);
}

TEST(right) {
    char* r = str_right("hello", 3);
    ASSERT_STR_EQ(r, "llo");
    free(r);
}

TEST(drop_left) {
    char* r = str_drop_left("hello", 2);
    ASSERT_STR_EQ(r, "llo");
    free(r);
}

TEST(drop_right) {
    char* r = str_drop_right("hello", 2);
    ASSERT_STR_EQ(r, "hel");
    free(r);
}

/* ==================== Cleanup Tests ==================== */

TEST(remove_whitespace) {
    char s[] = "h e l l o";
    str_remove_whitespace(s);
    ASSERT_STR_EQ(s, "hello");
}

TEST(remove_chars) {
    char s[] = "hello123world456";
    str_remove_chars(s, "0123456789");
    ASSERT_STR_EQ(s, "helloworld");
}

TEST(normalize_whitespace) {
    char s[] = "hello    world\t\t\ttest";
    str_normalize_whitespace(s);
    ASSERT_STR_EQ(s, "hello world test");
}

/* ==================== Main ==================== */

int main() {
    printf("Running string_utils tests...\n\n");
    
    printf("Trim Tests:\n");
    RUN_TEST(trim_left);
    RUN_TEST(trim_right);
    RUN_TEST(trim);
    RUN_TEST(trim_chars);
    
    printf("\nSplit Tests:\n");
    RUN_TEST(split);
    RUN_TEST(split_char);
    RUN_TEST(split_max);
    
    printf("\nReplace Tests:\n");
    RUN_TEST(replace);
    RUN_TEST(replace_all);
    RUN_TEST(replace_first);
    RUN_TEST(replace_n);
    
    printf("\nSearch Tests:\n");
    RUN_TEST(count);
    RUN_TEST(starts_with);
    RUN_TEST(ends_with);
    
    printf("\nCase Tests:\n");
    RUN_TEST(to_upper);
    RUN_TEST(to_lower);
    RUN_TEST(to_upper_copy);
    
    printf("\nCopy/Concat Tests:\n");
    RUN_TEST(copy_safe);
    RUN_TEST(concat_safe);
    RUN_TEST(repeat);
    RUN_TEST(join_array);
    
    printf("\nValidation Tests:\n");
    RUN_TEST(is_blank);
    RUN_TEST(is_numeric);
    RUN_TEST(is_integer);
    RUN_TEST(is_float);
    RUN_TEST(is_alpha);
    RUN_TEST(is_alphanumeric);
    
    printf("\nSubstring Tests:\n");
    RUN_TEST(substring);
    RUN_TEST(left);
    RUN_TEST(right);
    RUN_TEST(drop_left);
    RUN_TEST(drop_right);
    
    printf("\nCleanup Tests:\n");
    RUN_TEST(remove_whitespace);
    RUN_TEST(remove_chars);
    RUN_TEST(normalize_whitespace);
    
    printf("\n========================================\n");
    printf("Results: %d passed, %d failed\n", tests_passed, tests_failed);
    
    return tests_failed > 0 ? 1 : 0;
}
