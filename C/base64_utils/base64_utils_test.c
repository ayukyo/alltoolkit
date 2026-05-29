/**
 * @file base64_utils_test.c
 * @brief Base64 工具库单元测试
 * @author AllToolkit
 * @date 2026-05-30
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "base64_utils.h"

/* 测试计数器 */
static int tests_run = 0;
static int tests_passed = 0;
static int tests_failed = 0;

/* 测试宏 */
#define TEST(name) do { \
    printf("  [TEST] %s... ", name); \
    tests_run++; \
} while(0)

#define PASS() do { \
    printf("PASS\n"); \
    tests_passed++; \
} while(0)

#define FAIL(msg) do { \
    printf("FAIL: %s\n", msg); \
    tests_failed++; \
} while(0)

#define ASSERT_TRUE(cond) do { \
    if (!(cond)) { \
        FAIL("Assertion failed: " #cond); \
        return; \
    } \
} while(0)

#define ASSERT_FALSE(cond) ASSERT_TRUE(!(cond))

#define ASSERT_EQ(a, b) do { \
    if ((a) != (b)) { \
        FAIL("Not equal"); \
        return; \
    } \
} while(0)

#define ASSERT_STR_EQ(a, b) do { \
    if (strcmp((a), (b)) != 0) { \
        char _msg[256]; \
        snprintf(_msg, sizeof(_msg), "Expected '%s', got '%s'", (b), (a)); \
        FAIL(_msg); \
        return; \
    } \
} while(0)

#define ASSERT_MEM_EQ(a, b, len) do { \
    if (memcmp((a), (b), (len)) != 0) { \
        FAIL("Memory not equal"); \
        return; \
    } \
} while(0)

/* ==================== 测试函数 ==================== */

void test_encode_length(void) {
    TEST("base64_encode_length - empty input");
    ASSERT_EQ(base64_encode_length(0), 1);
    PASS();
    
    TEST("base64_encode_length - 1 byte");
    ASSERT_EQ(base64_encode_length(1), 5);
    PASS();
    
    TEST("base64_encode_length - 2 bytes");
    ASSERT_EQ(base64_encode_length(2), 5);
    PASS();
    
    TEST("base64_encode_length - 3 bytes");
    ASSERT_EQ(base64_encode_length(3), 5);
    PASS();
    
    TEST("base64_encode_length - 4 bytes");
    ASSERT_EQ(base64_encode_length(4), 9);
    PASS();
}

void test_basic_encode(void) {
    char output[256];
    
    TEST("base64_encode - empty input");
    size_t len = base64_encode((unsigned char*)"", 0, output, sizeof(output));
    ASSERT_EQ(len, 0);
    PASS();
    
    TEST("base64_encode - 'Hello'");
    len = base64_encode((unsigned char*)"Hello", 5, output, sizeof(output));
    ASSERT_STR_EQ(output, "SGVsbG8=");
    ASSERT_EQ(len, 8);
    PASS();
    
    TEST("base64_encode - 'Hello World'");
    len = base64_encode((unsigned char*)"Hello World", 11, output, sizeof(output));
    ASSERT_STR_EQ(output, "SGVsbG8gV29ybGQ=");
    ASSERT_EQ(len, 16);
    PASS();
    
    TEST("base64_encode - 'Man'");
    len = base64_encode((unsigned char*)"Man", 3, output, sizeof(output));
    ASSERT_STR_EQ(output, "TWFu");
    ASSERT_EQ(len, 4);
    PASS();
    
    TEST("base64_encode - 'Ma'");
    len = base64_encode((unsigned char*)"Ma", 2, output, sizeof(output));
    ASSERT_STR_EQ(output, "TWE=");
    ASSERT_EQ(len, 4);
    PASS();
    
    TEST("base64_encode - 'M'");
    len = base64_encode((unsigned char*)"M", 1, output, sizeof(output));
    ASSERT_STR_EQ(output, "TQ==");
    ASSERT_EQ(len, 4);
    PASS();
    
    TEST("base64_encode - 'any carnal pleasure.'");
    len = base64_encode((unsigned char*)"any carnal pleasure.", 20, output, sizeof(output));
    ASSERT_STR_EQ(output, "YW55IGNhcm5hbCBwbGVhc3VyZS4=");
    ASSERT_EQ(len, 28);
    PASS();
    
    TEST("base64_encode - binary data");
    unsigned char binary[] = {0x00, 0x01, 0x02, 0x03, 0xFF, 0xFE, 0xFD};
    len = base64_encode(binary, 7, output, sizeof(output));
    ASSERT_STR_EQ(output, "AAECA//+/Q==");
    ASSERT_EQ(len, 12);
    PASS();
}

void test_basic_decode(void) {
    unsigned char output[256];
    size_t len;
    
    TEST("base64_decode - 'SGVsbG8='");
    len = base64_decode("SGVsbG8=", 8, output, sizeof(output));
    ASSERT_EQ(len, 5);
    ASSERT_MEM_EQ(output, "Hello", 5);
    PASS();
    
    TEST("base64_decode - 'TWFu'");
    len = base64_decode("TWFu", 4, output, sizeof(output));
    ASSERT_EQ(len, 3);
    ASSERT_MEM_EQ(output, "Man", 3);
    PASS();
    
    TEST("base64_decode - 'TWE='");
    len = base64_decode("TWE=", 4, output, sizeof(output));
    ASSERT_EQ(len, 2);
    ASSERT_MEM_EQ(output, "Ma", 2);
    PASS();
    
    TEST("base64_decode - 'TQ=='");
    len = base64_decode("TQ==", 4, output, sizeof(output));
    ASSERT_EQ(len, 1);
    ASSERT_EQ(output[0], 'M');
    PASS();
    
    TEST("base64_decode - with whitespace");
    len = base64_decode("SGVs bG8=", 9, output, sizeof(output));
    ASSERT_EQ(len, 5);
    ASSERT_MEM_EQ(output, "Hello", 5);
    PASS();
    
    TEST("base64_decode - 'AAEC/wb+'");
    len = base64_decode("AAEC/wb+", 8, output, sizeof(output));
    ASSERT_EQ(len, 6);
    unsigned char expected[] = {0x00, 0x01, 0x02, 0xFF, 0x06, 0xFE};
    ASSERT_MEM_EQ(output, expected, 6);
    PASS();
}

void test_roundtrip(void) {
    char encoded[256];
    unsigned char decoded[256];
    size_t enc_len, dec_len;
    
    TEST("Roundtrip - 'The quick brown fox'");
    const char* input1 = "The quick brown fox jumps over the lazy dog";
    enc_len = base64_encode((const unsigned char*)input1, strlen(input1), encoded, sizeof(encoded));
    dec_len = base64_decode(encoded, enc_len, decoded, sizeof(decoded));
    ASSERT_EQ(dec_len, strlen(input1));
    ASSERT_MEM_EQ(decoded, input1, dec_len);
    PASS();
    
    TEST("Roundtrip - all printable ASCII");
    char ascii[95];
    for (int i = 0; i < 94; i++) {
        ascii[i] = (char)(32 + i);
    }
    ascii[94] = '\0';
    enc_len = base64_encode((unsigned char*)ascii, 94, encoded, sizeof(encoded));
    dec_len = base64_decode(encoded, enc_len, decoded, sizeof(decoded));
    ASSERT_EQ(dec_len, 94);
    ASSERT_MEM_EQ(decoded, ascii, 94);
    PASS();
    
    TEST("Roundtrip - binary zeros");
    unsigned char zeros[100];
    memset(zeros, 0, 100);
    enc_len = base64_encode(zeros, 100, encoded, sizeof(encoded));
    dec_len = base64_decode(encoded, enc_len, decoded, sizeof(decoded));
    ASSERT_EQ(dec_len, 100);
    for (int i = 0; i < 100; i++) {
        if (decoded[i] != 0) {
            FAIL("Binary zeros roundtrip failed");
            return;
        }
    }
    PASS();
}

void test_base64url(void) {
    char output[256];
    unsigned char decoded[256];
    size_t len, dec_len;
    
    TEST("base64url_encode - basic");
    len = base64url_encode((unsigned char*)"Hello", 5, output, sizeof(output));
    ASSERT_STR_EQ(output, "SGVsbG8");
    ASSERT_EQ(len, 7);
    PASS();
    
    TEST("base64url_encode - with +/");
    /* "hello?" -> "aGVsbG8/" in standard, "aGVsbG8_" in url-safe */
    len = base64url_encode((unsigned char*)"\xFB\xFF\xBF", 3, output, sizeof(output));
    ASSERT_STR_EQ(output, "-_-_");
    PASS();
    
    TEST("base64url_encode_with_padding");
    len = base64url_encode_with_padding((unsigned char*)"Hello", 5, output, sizeof(output));
    ASSERT_STR_EQ(output, "SGVsbG8=");
    PASS();
    
    TEST("base64url_decode - basic");
    dec_len = base64url_decode("SGVsbG8", 7, decoded, sizeof(decoded));
    ASSERT_EQ(dec_len, 5);
    ASSERT_MEM_EQ(decoded, "Hello", 5);
    PASS();
    
    TEST("base64url_decode - URL safe chars");
    dec_len = base64url_decode("-_-_", 4, decoded, sizeof(decoded));
    ASSERT_EQ(dec_len, 3);
    ASSERT_EQ(decoded[0], 0xFB);
    ASSERT_EQ(decoded[1], 0xFF);
    ASSERT_EQ(decoded[2], 0xBF);
    PASS();
}

void test_validation(void) {
    TEST("base64_is_valid - valid string");
    ASSERT_TRUE(base64_is_valid("SGVsbG8=", 8));
    PASS();
    
    TEST("base64_is_valid - valid without padding");
    /* 8 chars without padding is valid */
    ASSERT_TRUE(base64_is_valid("SGVsbG8g", 8));
    PASS();
    
    TEST("base64_is_valid - with whitespace");
    ASSERT_TRUE(base64_is_valid("SGVs bG8=", 9));
    PASS();
    
    TEST("base64_is_valid - invalid character");
    ASSERT_FALSE(base64_is_valid("SGVs*bG8=", 9));
    PASS();
    
    TEST("base64_is_valid - NULL input");
    ASSERT_FALSE(base64_is_valid(NULL, 0));
    PASS();
    
    TEST("base64url_is_valid - valid");
    ASSERT_TRUE(base64url_is_valid("SGVsbG8-_abc123", 15));
    PASS();
    
    TEST("base64url_is_valid - invalid");
    ASSERT_FALSE(base64url_is_valid("SGVs+bG8/abc", 12));
    PASS();
}

void test_encode_with_lines(void) {
    char output[1024];
    size_t len;
    
    TEST("base64_encode_with_lines - line width 4");
    const char* long_input = "HelloWorld1234567890HelloWorld1234567890";
    len = base64_encode_with_lines((unsigned char*)long_input, strlen(long_input), 
                                    output, sizeof(output), 4);
    /* 应该每 4 个字符换行 */
    ASSERT_TRUE(len > strlen(long_input));
    PASS();
    
    TEST("base64_encode_with_lines - PEM style (64 chars)");
    /* 生成足够长的数据 */
    unsigned char data[100];
    for (int i = 0; i < 100; i++) data[i] = (unsigned char)i;
    len = base64_encode_with_lines(data, 100, output, sizeof(output), 64);
    ASSERT_TRUE(len > 0);
    PASS();
}

void test_string_functions(void) {
    TEST("base64_encode_string");
    char* encoded = base64_encode_string("Hello World");
    ASSERT_TRUE(encoded != NULL);
    ASSERT_STR_EQ(encoded, "SGVsbG8gV29ybGQ=");
    free(encoded);
    PASS();
    
    TEST("base64_decode_string");
    size_t out_len;
    unsigned char* decoded = base64_decode_string("SGVsbG8gV29ybGQ=", &out_len);
    ASSERT_TRUE(decoded != NULL);
    ASSERT_EQ(out_len, 11);
    ASSERT_MEM_EQ(decoded, "Hello World", 11);
    free(decoded);
    PASS();
    
    TEST("base64_encode_hex");
    char* hex_encoded = base64_encode_hex("48656c6c6f");
    ASSERT_TRUE(hex_encoded != NULL);
    ASSERT_STR_EQ(hex_encoded, "SGVsbG8=");
    free(hex_encoded);
    PASS();
}

void test_buffer_sizing(void) {
    TEST("Encode with exact buffer size");
    char output[9]; /* "SGVsbG8=" + null */
    size_t len = base64_encode((unsigned char*)"Hello", 5, output, sizeof(output));
    ASSERT_EQ(len, 8);
    PASS();
    
    TEST("Encode with insufficient buffer");
    char small[5];
    len = base64_encode((unsigned char*)"Hello", 5, small, sizeof(small));
    ASSERT_EQ(len, 0);
    PASS();
    
    TEST("Decode with NULL output returns length");
    len = base64_decode("SGVsbG8=", 8, NULL, 0);
    ASSERT_EQ(len, 5);
    PASS();
}

void test_edge_cases(void) {
    TEST("NULL input encode");
    char output[32];
    size_t len = base64_encode(NULL, 0, output, sizeof(output));
    ASSERT_EQ(len, 0);
    PASS();
    
    TEST("NULL input decode");
    unsigned char decoded[32];
    len = base64_decode(NULL, 0, decoded, sizeof(decoded));
    ASSERT_EQ(len, (size_t)-1);
    PASS();
    
    TEST("Empty string encode");
    len = base64_encode((unsigned char*)"", 0, output, sizeof(output));
    ASSERT_EQ(len, 0);
    PASS();
}

void test_decode_length(void) {
    TEST("base64_decode_length - 'SGVsbG8='");
    size_t len = base64_decode_length("SGVsbG8=", 8);
    ASSERT_EQ(len, 5);
    PASS();
    
    TEST("base64_decode_length - 'TWFu'");
    len = base64_decode_length("TWFu", 4);
    ASSERT_EQ(len, 3);
    PASS();
    
    TEST("base64_decode_length - 'TQ=='");
    len = base64_decode_length("TQ==", 4);
    ASSERT_EQ(len, 1);
    PASS();
}

void test_custom_charset(void) {
    char output[64];
    unsigned char decoded[32];
    size_t len, dec_len;
    
    TEST("Custom charset - rot13 style");
    /* 使用 ROT13 变体 */
    const char* rot13_chars = "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm0123456789+/";
    
    len = base64_encode_custom((unsigned char*)"Man", 3, output, sizeof(output), 
                                rot13_chars, '=');
    ASSERT_TRUE(len > 0);
    
    dec_len = base64_decode_custom(output, len, decoded, sizeof(decoded),
                                   rot13_chars, '=');
    ASSERT_EQ(dec_len, 3);
    ASSERT_MEM_EQ(decoded, "Man", 3);
    PASS();
}

/* ==================== 测试运行器 ==================== */

int main(void) {
    printf("\n=== Base64 Utils Test Suite ===\n\n");
    
    /* 编码长度测试 */
    printf("--- Encode Length Tests ---\n");
    test_encode_length();
    
    /* 基础编码测试 */
    printf("\n--- Basic Encode Tests ---\n");
    test_basic_encode();
    
    /* 基础解码测试 */
    printf("\n--- Basic Decode Tests ---\n");
    test_basic_decode();
    
    /* 往返测试 */
    printf("\n--- Roundtrip Tests ---\n");
    test_roundtrip();
    
    /* Base64URL 测试 */
    printf("\n--- Base64URL Tests ---\n");
    test_base64url();
    
    /* 验证测试 */
    printf("\n--- Validation Tests ---\n");
    test_validation();
    
    /* 带换行编码测试 */
    printf("\n--- Encode with Lines Tests ---\n");
    test_encode_with_lines();
    
    /* 字符串函数测试 */
    printf("\n--- String Function Tests ---\n");
    test_string_functions();
    
    /* 缓冲区大小测试 */
    printf("\n--- Buffer Sizing Tests ---\n");
    test_buffer_sizing();
    
    /* 边界情况测试 */
    printf("\n--- Edge Case Tests ---\n");
    test_edge_cases();
    
    /* 解码长度测试 */
    printf("\n--- Decode Length Tests ---\n");
    test_decode_length();
    
    /* 自定义字符集测试 */
    printf("\n--- Custom Charset Tests ---\n");
    test_custom_charset();
    
    /* 测试总结 */
    printf("\n=== Test Summary ===\n");
    printf("  Total:  %d\n", tests_run);
    printf("  Passed: %d\n", tests_passed);
    printf("  Failed: %d\n", tests_failed);
    
    if (tests_failed == 0) {
        printf("\n✓ All tests passed!\n\n");
        return 0;
    } else {
        printf("\n✗ Some tests failed.\n\n");
        return 1;
    }
}