/**
 * @file test_bit_utils.c
 * @brief 位操作工具库测试
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "bit_utils.h"

/* 测试计数器 */
static int tests_passed = 0;
static int tests_failed = 0;

#define TEST(name) static void test_##name(void)
#define RUN_TEST(name) do { \
    printf("  Running %s... ", #name); \
    test_##name(); \
    printf("PASSED\n"); \
    tests_passed++; \
} while(0)

#define ASSERT_EQ(expected, actual) do { \
    if ((expected) != (actual)) { \
        printf("FAILED at line %d: expected %llu, got %llu\n", \
               __LINE__, (unsigned long long)(expected), (unsigned long long)(actual)); \
        tests_failed++; \
        return; \
    } \
} while(0)

#define ASSERT_TRUE(condition) do { \
    if (!(condition)) { \
        printf("FAILED at line %d: expected true\n", __LINE__); \
        tests_failed++; \
        return; \
    } \
} while(0)

#define ASSERT_FALSE(condition) do { \
    if (condition) { \
        printf("FAILED at line %d: expected false\n", __LINE__); \
        tests_failed++; \
        return; \
    } \
} while(0)

/* ============================================================
 * 基本位操作测试
 * ============================================================ */

TEST(bit_set_basic) {
    ASSERT_EQ(1ULL, bit_set(0, 0));
    ASSERT_EQ(2ULL, bit_set(0, 1));
    ASSERT_EQ(4ULL, bit_set(0, 2));
    ASSERT_EQ(0x8000000000000000ULL, bit_set(0, 63));
    ASSERT_EQ(0xFULL, bit_set(0xE, 0));  /* 1110 | 0001 = 1111 */
    ASSERT_EQ(0xFULL, bit_set(0xF, 0));  /* 已设置的位不变 */
}

TEST(bit_clear_basic) {
    ASSERT_EQ(0ULL, bit_clear(1, 0));
    ASSERT_EQ(0ULL, bit_clear(2, 1));
    ASSERT_EQ(0xBULL, bit_clear(0xF, 2));  /* 1111 & ~0100 = 1011 = 0xB */
    ASSERT_EQ(0x7FFFFFFFFFFFFFFFULL, bit_clear(~0ULL, 63));
    ASSERT_EQ(0xFULL, bit_clear(0xF, 4));  /* 超出范围不变 */
}

TEST(bit_toggle_basic) {
    ASSERT_EQ(1ULL, bit_toggle(0, 0));
    ASSERT_EQ(0ULL, bit_toggle(1, 0));
    ASSERT_EQ(0x9ULL, bit_toggle(0xD, 2));  /* 1101 ^ 0100 = 1001 = 0x9 */
    ASSERT_EQ(0x1ULL, bit_toggle(0x5, 2));  /* 0101 ^ 0100 = 0001 = 0x1 */
    ASSERT_EQ(0ULL, bit_toggle(0x8000000000000000ULL, 63));
}

TEST(bit_test_basic) {
    ASSERT_TRUE(bit_test(1, 0));
    ASSERT_TRUE(bit_test(2, 1));
    ASSERT_TRUE(bit_test(0x8000000000000000ULL, 63));
    ASSERT_FALSE(bit_test(0, 0));
    ASSERT_FALSE(bit_test(0xFE, 0));  /* 11111110, bit 0 is 0 */
    ASSERT_FALSE(bit_test(1, 1));
}

TEST(bit_set_value_basic) {
    ASSERT_EQ(1ULL, bit_set_value(0, 0, true));
    ASSERT_EQ(0ULL, bit_set_value(1, 0, false));
    ASSERT_EQ(0x8000000000000000ULL, bit_set_value(0, 63, true));
    ASSERT_EQ(0x7FFFFFFFFFFFFFFFULL, bit_set_value(~0ULL, 63, false));
}

/* ============================================================
 * 位计数测试
 * ============================================================ */

TEST(bit_count_basic) {
    ASSERT_EQ(0, bit_count(0));
    ASSERT_EQ(1, bit_count(1));
    ASSERT_EQ(1, bit_count(2));
    ASSERT_EQ(2, bit_count(3));
    ASSERT_EQ(8, bit_count(0xFF));
    ASSERT_EQ(16, bit_count(0xFFFF));
    ASSERT_EQ(32, bit_count(0xFFFFFFFF));
    ASSERT_EQ(64, bit_count(~0ULL));
    ASSERT_EQ(1, bit_count(0x8000000000000000ULL));
    ASSERT_EQ(4, bit_count(0xF));
    ASSERT_EQ(4, bit_count(0xF0));
}

TEST(bit_count_zero_basic) {
    ASSERT_EQ(64, bit_count_zero(0));
    ASSERT_EQ(63, bit_count_zero(1));
    ASSERT_EQ(0, bit_count_zero(~0ULL));
    ASSERT_EQ(60, bit_count_zero(0xF));
}

TEST(bit_parity_basic) {
    ASSERT_FALSE(bit_parity(0));      /* 偶数个1（0个） */
    ASSERT_TRUE(bit_parity(1));       /* 奇数个1（1个） */
    ASSERT_FALSE(bit_parity(3));      /* 偶数个1（2个） */
    ASSERT_TRUE(bit_parity(7));       /* 奇数个1（3个） */
    ASSERT_FALSE(bit_parity(0xFF));   /* 偶数个1（8个） */
    ASSERT_TRUE(bit_parity(0x7F));    /* 奇数个1（7个） */
}

/* ============================================================
 * 位查找测试
 * ============================================================ */

TEST(bit_find_first_set_basic) {
    ASSERT_EQ(-1, bit_find_first_set(0));
    ASSERT_EQ(0, bit_find_first_set(1));
    ASSERT_EQ(1, bit_find_first_set(2));
    ASSERT_EQ(0, bit_find_first_set(3));
    ASSERT_EQ(2, bit_find_first_set(4));
    ASSERT_EQ(63, bit_find_first_set(0x8000000000000000ULL));
    ASSERT_EQ(0, bit_find_first_set(0x8000000000000001ULL));
}

TEST(bit_find_last_set_basic) {
    ASSERT_EQ(-1, bit_find_last_set(0));
    ASSERT_EQ(0, bit_find_last_set(1));
    ASSERT_EQ(1, bit_find_last_set(2));
    ASSERT_EQ(1, bit_find_last_set(3));
    ASSERT_EQ(2, bit_find_last_set(4));
    ASSERT_EQ(63, bit_find_last_set(0x8000000000000000ULL));
    ASSERT_EQ(63, bit_find_last_set(0x8000000000000001ULL));
    ASSERT_EQ(3, bit_find_last_set(0xF));
}

TEST(bit_find_first_zero_basic) {
    ASSERT_EQ(0, bit_find_first_zero(0));
    ASSERT_EQ(1, bit_find_first_zero(1));
    ASSERT_EQ(2, bit_find_first_zero(3));
    ASSERT_EQ(0, bit_find_first_zero(2));
    ASSERT_EQ(-1, bit_find_first_zero(~0ULL));
}

TEST(bit_find_last_zero_basic) {
    ASSERT_EQ(63, bit_find_last_zero(0));
    ASSERT_EQ(63, bit_find_last_zero(1));
    ASSERT_EQ(0, bit_find_last_zero(0xFFFFFFFFFFFFFFFEULL));
    ASSERT_EQ(-1, bit_find_last_zero(~0ULL));
}

/* ============================================================
 * 位反转和旋转测试
 * ============================================================ */

TEST(bit_reverse_basic) {
    ASSERT_EQ(0ULL, bit_reverse(0));
    ASSERT_EQ(0x8000000000000000ULL, bit_reverse(1));
    ASSERT_EQ(1ULL, bit_reverse(0x8000000000000000ULL));
    ASSERT_EQ(0xC000000000000000ULL, bit_reverse(3));
    ASSERT_EQ(0xAAAAAAAAAAAAAAAAULL, bit_reverse(0x5555555555555555ULL));
    ASSERT_EQ(0x5555555555555555ULL, bit_reverse(0xAAAAAAAAAAAAAAAAULL));
}

TEST(bit_reverse_n_basic) {
    ASSERT_EQ(0ULL, bit_reverse_n(0, 8));
    ASSERT_EQ(0xF0ULL, bit_reverse_n(0xF, 8));
    ASSERT_EQ(0xF0ULL, bit_reverse_n(0x0F, 8));
    ASSERT_EQ(0xAAULL, bit_reverse_n(0x55, 8));
    ASSERT_EQ(0xFULL, bit_reverse_n(0xF, 4));
    ASSERT_EQ(0x1ULL, bit_reverse_n(0x8, 4));
}

TEST(bit_rotate_left_basic) {
    ASSERT_EQ(2ULL, bit_rotate_left(1, 1, 8));
    ASSERT_EQ(4ULL, bit_rotate_left(1, 2, 8));
    ASSERT_EQ(1ULL, bit_rotate_left(1, 8, 8));  /* 循环回原位 */
    ASSERT_EQ(0x80ULL, bit_rotate_left(0x40, 1, 8));
    ASSERT_EQ(0x01ULL, bit_rotate_left(0x80, 1, 8));  /* 循环 */
}

TEST(bit_rotate_right_basic) {
    ASSERT_EQ(0x80ULL, bit_rotate_right(1, 1, 8));
    ASSERT_EQ(0x40ULL, bit_rotate_right(1, 2, 8));
    ASSERT_EQ(1ULL, bit_rotate_right(1, 8, 8));
    ASSERT_EQ(0x40ULL, bit_rotate_right(0x80, 1, 8));
    ASSERT_EQ(1ULL, bit_rotate_right(2, 1, 8));
}

/* ============================================================
 * 位掩码测试
 * ============================================================ */

TEST(bit_mask_low_basic) {
    ASSERT_EQ(0ULL, bit_mask_low(0));
    ASSERT_EQ(1ULL, bit_mask_low(1));
    ASSERT_EQ(3ULL, bit_mask_low(2));
    ASSERT_EQ(0xFULL, bit_mask_low(4));
    ASSERT_EQ(0xFFULL, bit_mask_low(8));
    ASSERT_EQ(~0ULL, bit_mask_low(64));
}

TEST(bit_mask_high_basic) {
    ASSERT_EQ(0ULL, bit_mask_high(0));
    ASSERT_EQ(0x8000000000000000ULL, bit_mask_high(1));
    ASSERT_EQ(0xC000000000000000ULL, bit_mask_high(2));
    ASSERT_EQ(0xF000000000000000ULL, bit_mask_high(4));
    ASSERT_EQ(~0ULL, bit_mask_high(64));
}

TEST(bit_mask_range_basic) {
    ASSERT_EQ(1ULL, bit_mask_range(0, 0));
    ASSERT_EQ(3ULL, bit_mask_range(0, 1));
    ASSERT_EQ(0xCULL, bit_mask_range(2, 3));
    ASSERT_EQ(0xFF00ULL, bit_mask_range(8, 15));
    ASSERT_EQ(0xFFFFULL, bit_mask_range(0, 15));
}

TEST(bit_extract_basic) {
    ASSERT_EQ(1ULL, bit_extract(1, 0, 0));
    ASSERT_EQ(3ULL, bit_extract(7, 0, 1));
    ASSERT_EQ(3ULL, bit_extract(0xF, 1, 2));
    ASSERT_EQ(0xFULL, bit_extract(0xFF00, 8, 11));
    ASSERT_EQ(0xFFULL, bit_extract(0xFFFF, 0, 7));
}

TEST(bit_insert_basic) {
    ASSERT_EQ(1ULL, bit_insert(0, 1, 0, 0));
    ASSERT_EQ(7ULL, bit_insert(0, 7, 0, 2));
    ASSERT_EQ(0xFF00ULL, bit_insert(0, 0xFF, 8, 15));
    ASSERT_EQ(0xF0FULL, bit_insert(0xF, 0xF, 8, 11));
    ASSERT_EQ(0xABULL, bit_insert(0xA0, 0xB, 0, 3));
}

/* ============================================================
 * 字节序转换测试
 * ============================================================ */

TEST(bit_swap16_basic) {
    ASSERT_EQ(0x0100, bit_swap16(0x0001));
    ASSERT_EQ(0xF0DE, bit_swap16(0xDEF0));
    ASSERT_EQ(0xFF00, bit_swap16(0x00FF));
}

TEST(bit_swap32_basic) {
    ASSERT_EQ(0x04030201, bit_swap32(0x01020304));
    ASSERT_EQ(0xBEBAFECA, bit_swap32(0xCAFEBABE));
}

TEST(bit_swap64_basic) {
    ASSERT_EQ(0x0807060504030201ULL, bit_swap64(0x0102030405060708ULL));
    ASSERT_EQ(0xEFBEADDEEFBEADDEULL, bit_swap64(0xDEADBEEFDEADBEEFULL));
}

TEST(bit_endian_conversion) {
    /* 小端到大端再转回应该保持不变 */
    ASSERT_EQ(0x1234, bit_be_to_le16(bit_le_to_be16(0x1234)));
    ASSERT_EQ(0x12345678, bit_be_to_le32(bit_le_to_be32(0x12345678)));
    ASSERT_EQ(0x123456789ABCDEF0ULL, bit_be_to_le64(bit_le_to_be64(0x123456789ABCDEF0ULL)));
}

/* ============================================================
 * 位字段操作测试
 * ============================================================ */

TEST(bit_field_read_basic) {
    ASSERT_EQ(1ULL, bit_field_read(1, 0, 1));
    ASSERT_EQ(3ULL, bit_field_read(7, 0, 2));
    ASSERT_EQ(0xFULL, bit_field_read(0xFF, 0, 4));
    ASSERT_EQ(0xFULL, bit_field_read(0xFF0, 4, 4));
}

TEST(bit_field_write_basic) {
    ASSERT_EQ(1ULL, bit_field_write(0, 1, 0, 1));
    ASSERT_EQ(7ULL, bit_field_write(0, 7, 0, 3));
    ASSERT_EQ(0xF0ULL, bit_field_write(0, 0xF, 4, 7));
    ASSERT_EQ(0xF7ULL, bit_field_write(0xF0, 0xF, 0, 3));  /* bits 0-2 = 3 bits, mask=7 */
}

/* ============================================================
 * 位向量测试
 * ============================================================ */

TEST(bit_vector_create_destroy) {
    BitVector *bv = bit_vector_create(100);
    ASSERT_TRUE(bv != NULL);
    ASSERT_TRUE(bv->data != NULL);
    ASSERT_EQ(100, bv->size);
    ASSERT_TRUE(bv->capacity >= 13);  /* ceil(100/8) = 13 */
    bit_vector_destroy(bv);
}

TEST(bit_vector_get_set) {
    BitVector *bv = bit_vector_create(64);
    ASSERT_TRUE(bv != NULL);
    
    /* 初始全0 */
    for (size_t i = 0; i < 64; i++) {
        ASSERT_EQ(0, bit_vector_get(bv, i));
    }
    
    /* 设置位 */
    ASSERT_EQ(0, bit_vector_set(bv, 0, true));
    ASSERT_EQ(1, bit_vector_get(bv, 0));
    
    ASSERT_EQ(0, bit_vector_set(bv, 63, true));
    ASSERT_EQ(1, bit_vector_get(bv, 63));
    
    ASSERT_EQ(0, bit_vector_set(bv, 32, true));
    ASSERT_EQ(1, bit_vector_get(bv, 32));
    
    /* 清除位 */
    ASSERT_EQ(0, bit_vector_set(bv, 0, false));
    ASSERT_EQ(0, bit_vector_get(bv, 0));
    
    bit_vector_destroy(bv);
}

TEST(bit_vector_toggle) {
    BitVector *bv = bit_vector_create(32);
    ASSERT_TRUE(bv != NULL);
    
    ASSERT_EQ(1, bit_vector_toggle(bv, 0));  /* 0 -> 1 */
    ASSERT_EQ(0, bit_vector_toggle(bv, 0));  /* 1 -> 0 */
    ASSERT_EQ(1, bit_vector_toggle(bv, 0));  /* 0 -> 1 */
    ASSERT_EQ(1, bit_vector_get(bv, 0));
    
    bit_vector_destroy(bv);
}

TEST(bit_vector_fill_count) {
    BitVector *bv = bit_vector_create(100);
    ASSERT_TRUE(bv != NULL);
    
    ASSERT_EQ(0, bit_vector_count(bv));
    
    bit_vector_fill(bv, true);
    ASSERT_EQ(100, bit_vector_count(bv));
    
    bit_vector_fill(bv, false);
    ASSERT_EQ(0, bit_vector_count(bv));
    
    bit_vector_set(bv, 0, true);
    bit_vector_set(bv, 50, true);
    bit_vector_set(bv, 99, true);
    ASSERT_EQ(3, bit_vector_count(bv));
    
    bit_vector_destroy(bv);
}

TEST(bit_vector_resize) {
    BitVector *bv = bit_vector_create(32);
    ASSERT_TRUE(bv != NULL);
    
    bit_vector_set(bv, 0, true);
    bit_vector_set(bv, 31, true);
    
    ASSERT_EQ(0, bit_vector_resize(bv, 64));
    ASSERT_EQ(64, bv->size);
    ASSERT_EQ(1, bit_vector_get(bv, 0));
    ASSERT_EQ(1, bit_vector_get(bv, 31));
    ASSERT_EQ(0, bit_vector_get(bv, 32));
    ASSERT_EQ(0, bit_vector_get(bv, 63));
    
    bit_vector_destroy(bv);
}

/* ============================================================
 * 实用函数测试
 * ============================================================ */

TEST(bit_is_power_of_two_basic) {
    ASSERT_FALSE(bit_is_power_of_two(0));
    ASSERT_TRUE(bit_is_power_of_two(1));
    ASSERT_TRUE(bit_is_power_of_two(2));
    ASSERT_FALSE(bit_is_power_of_two(3));
    ASSERT_TRUE(bit_is_power_of_two(4));
    ASSERT_FALSE(bit_is_power_of_two(5));
    ASSERT_TRUE(bit_is_power_of_two(1024));
    ASSERT_TRUE(bit_is_power_of_two(0x80000000ULL));
    ASSERT_FALSE(bit_is_power_of_two(1023));
}

TEST(bit_next_power_of_two_basic) {
    ASSERT_EQ(1, bit_next_power_of_two(0));
    ASSERT_EQ(1, bit_next_power_of_two(1));
    ASSERT_EQ(2, bit_next_power_of_two(2));
    ASSERT_EQ(4, bit_next_power_of_two(3));
    ASSERT_EQ(4, bit_next_power_of_two(4));
    ASSERT_EQ(8, bit_next_power_of_two(5));
    ASSERT_EQ(1024, bit_next_power_of_two(1000));
    ASSERT_EQ(0x10000ULL, bit_next_power_of_two(0xFFFF));
}

TEST(bit_prev_power_of_two_basic) {
    ASSERT_EQ(1, bit_prev_power_of_two(0));
    ASSERT_EQ(1, bit_prev_power_of_two(1));
    ASSERT_EQ(2, bit_prev_power_of_two(2));
    ASSERT_EQ(2, bit_prev_power_of_two(3));
    ASSERT_EQ(4, bit_prev_power_of_two(4));
    ASSERT_EQ(4, bit_prev_power_of_two(5));
    ASSERT_EQ(512, bit_prev_power_of_two(1000));
}

TEST(bit_width_basic) {
    ASSERT_EQ(0, bit_width(0));
    ASSERT_EQ(1, bit_width(1));
    ASSERT_EQ(2, bit_width(2));
    ASSERT_EQ(2, bit_width(3));
    ASSERT_EQ(3, bit_width(4));
    ASSERT_EQ(8, bit_width(0xFF));
    ASSERT_EQ(16, bit_width(0xFFFF));
    ASSERT_EQ(64, bit_width(0x8000000000000000ULL));
}

TEST(bit_gray_conversion) {
    /* 二进制 -> Gray码 */
    ASSERT_EQ(0ULL, bit_binary_to_gray(0));
    ASSERT_EQ(1ULL, bit_binary_to_gray(1));
    ASSERT_EQ(3ULL, bit_binary_to_gray(2));
    ASSERT_EQ(2ULL, bit_binary_to_gray(3));
    ASSERT_EQ(6ULL, bit_binary_to_gray(4));
    ASSERT_EQ(7ULL, bit_binary_to_gray(5));
    ASSERT_EQ(5ULL, bit_binary_to_gray(6));
    ASSERT_EQ(4ULL, bit_binary_to_gray(7));
    
    /* Gray码 -> 二进制 */
    ASSERT_EQ(0ULL, bit_gray_to_binary(0));
    ASSERT_EQ(1ULL, bit_gray_to_binary(1));
    ASSERT_EQ(2ULL, bit_gray_to_binary(3));
    ASSERT_EQ(3ULL, bit_gray_to_binary(2));
    ASSERT_EQ(4ULL, bit_gray_to_binary(6));
    ASSERT_EQ(5ULL, bit_gray_to_binary(7));
    ASSERT_EQ(6ULL, bit_gray_to_binary(5));
    ASSERT_EQ(7ULL, bit_gray_to_binary(4));
    
    /* 往返转换 */
    for (int i = 0; i < 256; i++) {
        uint64_t gray = bit_binary_to_gray(i);
        ASSERT_EQ((uint64_t)i, bit_gray_to_binary(gray));
    }
}

TEST(bit_to_string_basic) {
    char buffer[65];
    
    ASSERT_TRUE(strcmp(bit_to_string(0, buffer, 8), "00000000") == 0);
    ASSERT_TRUE(strcmp(bit_to_string(1, buffer, 8), "00000001") == 0);
    ASSERT_TRUE(strcmp(bit_to_string(0xFF, buffer, 8), "11111111") == 0);
    ASSERT_TRUE(strcmp(bit_to_string(0xAA, buffer, 8), "10101010") == 0);
    ASSERT_TRUE(strcmp(bit_to_string(0xF0, buffer, 8), "11110000") == 0);
    ASSERT_TRUE(strcmp(bit_to_string(0xDEADBEEF, buffer, 32), "11011110101011011011111011101111") == 0);
}

TEST(bit_from_string_basic) {
    uint64_t value;
    
    ASSERT_EQ(0, bit_from_string("0", &value));
    ASSERT_EQ(0ULL, value);
    
    ASSERT_EQ(0, bit_from_string("1", &value));
    ASSERT_EQ(1ULL, value);
    
    ASSERT_EQ(0, bit_from_string("10101010", &value));
    ASSERT_EQ(0xAAULL, value);
    
    ASSERT_EQ(0, bit_from_string("11111111", &value));
    ASSERT_EQ(0xFFULL, value);
    
    ASSERT_EQ(0, bit_from_string("0b1010", &value));
    ASSERT_EQ(0xAULL, value);
    
    ASSERT_EQ(0, bit_from_string("0B1111", &value));
    ASSERT_EQ(0xFULL, value);
    
    /* 带空格 */
    ASSERT_EQ(0, bit_from_string("  101  ", &value));
    ASSERT_EQ(5ULL, value);
    
    /* 无效字符 */
    ASSERT_EQ(-1, bit_from_string("102", &value));
    ASSERT_EQ(-1, bit_from_string("abc", &value));
}

/* ============================================================
 * 主函数
 * ============================================================ */

int main(void) {
    printf("\n========================================\n");
    printf("  Bit Utils Test Suite\n");
    printf("========================================\n\n");
    
    /* 基本位操作 */
    printf("--- Basic Operations ---\n");
    RUN_TEST(bit_set_basic);
    RUN_TEST(bit_clear_basic);
    RUN_TEST(bit_toggle_basic);
    RUN_TEST(bit_test_basic);
    RUN_TEST(bit_set_value_basic);
    
    /* 位计数 */
    printf("\n--- Bit Counting ---\n");
    RUN_TEST(bit_count_basic);
    RUN_TEST(bit_count_zero_basic);
    RUN_TEST(bit_parity_basic);
    
    /* 位查找 */
    printf("\n--- Bit Finding ---\n");
    RUN_TEST(bit_find_first_set_basic);
    RUN_TEST(bit_find_last_set_basic);
    RUN_TEST(bit_find_first_zero_basic);
    RUN_TEST(bit_find_last_zero_basic);
    
    /* 位反转和旋转 */
    printf("\n--- Bit Reverse and Rotate ---\n");
    RUN_TEST(bit_reverse_basic);
    RUN_TEST(bit_reverse_n_basic);
    RUN_TEST(bit_rotate_left_basic);
    RUN_TEST(bit_rotate_right_basic);
    
    /* 位掩码 */
    printf("\n--- Bit Masks ---\n");
    RUN_TEST(bit_mask_low_basic);
    RUN_TEST(bit_mask_high_basic);
    RUN_TEST(bit_mask_range_basic);
    RUN_TEST(bit_extract_basic);
    RUN_TEST(bit_insert_basic);
    
    /* 字节序转换 */
    printf("\n--- Byte Order ---\n");
    RUN_TEST(bit_swap16_basic);
    RUN_TEST(bit_swap32_basic);
    RUN_TEST(bit_swap64_basic);
    RUN_TEST(bit_endian_conversion);
    
    /* 位字段操作 */
    printf("\n--- Bit Fields ---\n");
    RUN_TEST(bit_field_read_basic);
    RUN_TEST(bit_field_write_basic);
    
    /* 位向量 */
    printf("\n--- Bit Vector ---\n");
    RUN_TEST(bit_vector_create_destroy);
    RUN_TEST(bit_vector_get_set);
    RUN_TEST(bit_vector_toggle);
    RUN_TEST(bit_vector_fill_count);
    RUN_TEST(bit_vector_resize);
    
    /* 实用函数 */
    printf("\n--- Utility Functions ---\n");
    RUN_TEST(bit_is_power_of_two_basic);
    RUN_TEST(bit_next_power_of_two_basic);
    RUN_TEST(bit_prev_power_of_two_basic);
    RUN_TEST(bit_width_basic);
    RUN_TEST(bit_gray_conversion);
    RUN_TEST(bit_to_string_basic);
    RUN_TEST(bit_from_string_basic);
    
    printf("\n========================================\n");
    printf("  Results: %d passed, %d failed\n", tests_passed, tests_failed);
    printf("========================================\n\n");
    
    return tests_failed > 0 ? 1 : 0;
}