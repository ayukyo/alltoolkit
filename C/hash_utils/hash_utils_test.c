/**
 * @file hash_utils_test.c
 * @brief Hash Utilities Test Suite
 *
 * Comprehensive test suite for hash functions including MD5, SHA1, SHA256,
 * SHA512, and HMAC-SHA256.
 */

#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "mod.h"

static int tests_passed = 0;
static int tests_failed = 0;

#define TEST(name) void test_##name(void)
#define RUN_TEST(name) do { \
    printf("  Testing " #name "... "); \
    test_##name(); \
} while(0)

#define ASSERT_STR_EQ(a, b) do { \
    if (strcmp((a), (b)) != 0) { \
        printf("FAILED: \"%s\" != \"%s\" at line %d\n", a, b, __LINE__); \
        tests_failed++; \
        return; \
    } \
} while(0)

#define ASSERT_TRUE(expr) do { \
    if (!(expr)) { \
        printf("FAILED: !\"%s\" at line %d\n", #expr, __LINE__); \
        tests_failed++; \
        return; \
    } \
} while(0)

#define ASSERT_FALSE(expr) do { \
    if (expr) { \
        printf("FAILED: \"%s\" at line %d\n", #expr, __LINE__); \
        tests_failed++; \
        return; \
    } \
} while(0)

#define PASS() do { \
    printf("PASSED\n"); \
    tests_passed++; \
} while(0)

/* MD5 Tests */
TEST(md5_empty_string) {
    char hex[HASH_MD5_HEX_LEN];
    hash_md5_string_hex("", hex);
    ASSERT_STR_EQ(hex, "d41d8cd98f00b204e9800998ecf8427e");
    PASS();
}

TEST(md5_hello) {
    char hex[HASH_MD5_HEX_LEN];
    hash_md5_string_hex("hello", hex);
    ASSERT_STR_EQ(hex, "5d41402abc4b2a76b9719d911017c592");
    PASS();
}

TEST(md5_hello_world) {
    char hex[HASH_MD5_HEX_LEN];
    hash_md5_string_hex("hello world", hex);
    ASSERT_STR_EQ(hex, "5eb63bbbe01eeed093cb22bb8f5acdc3");
    PASS();
}

TEST(md5_long_string) {
    char hex[HASH_MD5_HEX_LEN];
    hash_md5_string_hex("The quick brown fox jumps over the lazy dog", hex);
    ASSERT_STR_EQ(hex, "9e107d9d372bb6826bd81d3542a419d6");
    PASS();
}

TEST(md5_validation) {
    ASSERT_TRUE(hash_is_valid_md5("d41d8cd98f00b204e9800998ecf8427e"));
    ASSERT_TRUE(hash_is_valid_md5("D41D8CD98F00B204E9800998ECF8427E"));
    ASSERT_FALSE(hash_is_valid_md5("invalid"));
    ASSERT_FALSE(hash_is_valid_md5("d41d8cd98f00b204e9800998ecf8427"));
    ASSERT_FALSE(hash_is_valid_md5("d41d8cd98f00b204e9800998ecf8427ee"));
    PASS();
}

/* SHA1 Tests */
TEST(sha1_empty_string) {
    char hex[HASH_SHA1_HEX_LEN];
    hash_sha1_string_hex("", hex);
    ASSERT_STR_EQ(hex, "da39a3ee5e6b4b0d3255bfef95601890afd80709");
    PASS();
}

TEST(sha1_hello) {
    char hex[HASH_SHA1_HEX_LEN];
    hash_sha1_string_hex("hello", hex);
    ASSERT_STR_EQ(hex, "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d");
    PASS();
}

TEST(sha1_hello_world) {
    char hex[HASH_SHA1_HEX_LEN];
    hash_sha1_string_hex("hello world", hex);
    ASSERT_STR_EQ(hex, "2aae6c35c94fcfb415dbe95f408b9ce91ee846ed");
    PASS();
}

TEST(sha1_long_string) {
    char hex[HASH_SHA1_HEX_LEN];
    hash_sha1_string_hex("The quick brown fox jumps over the lazy dog", hex);
    ASSERT_STR_EQ(hex, "2fd4e1c67a2d28fced849ee1bb76e7391b93eb12");
    PASS();
}

TEST(sha1_validation) {
    ASSERT_TRUE(hash_is_valid_sha1("da39a3ee5e6b4b0d3255bfef95601890afd80709"));
    ASSERT_FALSE(hash_is_valid_sha1("invalid"));
    ASSERT_FALSE(hash_is_valid_sha1("da39a3ee5e6b4b0d3255bfef95601890afd8070"));
    PASS();
}

/* SHA256 Tests */
TEST(sha256_empty_string) {
    char hex[HASH_SHA256_HEX_LEN];
    hash_sha256_string_hex("", hex);
    ASSERT_STR_EQ(hex, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
    PASS();
}

TEST(sha256_hello) {
    char hex[HASH_SHA256_HEX_LEN];
    hash_sha256_string_hex("hello", hex);
    ASSERT_STR_EQ(hex, "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824");
    PASS();
}

TEST(sha256_hello_world) {
    char hex[HASH_SHA256_HEX_LEN];
    hash_sha256_string_hex("hello world", hex);
    ASSERT_STR_EQ(hex, "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9");
    PASS();
}

TEST(sha256_long_string) {
    char hex[HASH_SHA256_HEX_LEN];
    hash_sha256_string_hex("The quick brown fox jumps over the lazy dog", hex);
    ASSERT_STR_EQ(hex, "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592");
    PASS();
}

TEST(sha256_validation) {
    ASSERT_TRUE(hash_is_valid_sha256("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"));
    ASSERT_FALSE(hash_is_valid_sha256("invalid"));
    PASS();
}

/* SHA512 Tests */
TEST(sha512_empty_string) {
    char hex[HASH_SHA512_HEX_LEN];
    hash_sha512_string_hex("", hex);
    ASSERT_STR_EQ(hex, "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e");
    PASS();
}

TEST(sha512_hello) {
    char hex[HASH_SHA512_HEX_LEN];
    hash_sha512_string_hex("hello", hex);
    ASSERT_STR_EQ(hex, "9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043");
    PASS();
}

TEST(sha512_hello_world) {
    char hex[HASH_SHA512_HEX_LEN];
    hash_sha512_string_hex("hello world", hex);
    ASSERT_STR_EQ(hex, "309ecc489c12d6eb4cc40f50c902f2b4d0ed77ee511a7c7a9bcd3ca86d4cd86f989dd35bc5ff499670da34255b45b0cfd830e81f605dcf7dc5542e93ae9cd76f");
    PASS();
}

TEST(sha512_validation) {
    ASSERT_TRUE(hash_is_valid_sha512("cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e"));
    ASSERT_FALSE(hash_is_valid_sha512("invalid"));
    PASS();
}

/* HMAC-SHA256 Tests */
TEST(hmac_sha256_empty) {
    char hex[HASH_SHA256_HEX_LEN];
    hash_hmac_sha256_hex("", "", hex);
    ASSERT_TRUE(strlen(hex) == 64);
    PASS();
}

TEST(hmac_sha256_basic) {
    char hex[HASH_SHA256_HEX_LEN];
    hash_hmac_sha256_hex("key", "message", hex);
    ASSERT_TRUE(strlen(hex) == 64);
    PASS();
}

TEST(hmac_sha256_verify) {
    char hex[HASH_SHA256_HEX_LEN];
    hash_hmac_sha256_hex("secret", "message", hex);
    ASSERT_TRUE(hash_hmac_sha256_verify("secret", "message", hex));
    ASSERT_FALSE(hash_hmac_sha256_verify("secret", "message", "wronghash"));
    PASS();
}

/* Utility Tests */
TEST(bytes_to_hex) {
    uint8_t bytes[] = {0x00, 0x0f, 0xf0, 0xff};
    char hex[9];
    hash_bytes_to_hex(bytes, 4, hex);
    ASSERT_STR_EQ(hex, "000ff0ff");
    PASS();
}

TEST(hex_to_bytes) {
    const char *hex = "000ff0ff";
    uint8_t bytes[4];
    ASSERT_TRUE(hash_hex_to_bytes(hex, bytes, 4));
    ASSERT_TRUE(bytes[0] == 0x00 && bytes[1] == 0x0f && bytes[2] == 0xf0 && bytes[3] == 0xff);
    PASS();
}

/* Main */
int main(void) {
    printf("============================================\n");
    printf("Hash Utilities Test Suite\n");
    printf("============================================\n\n");

    printf("MD5 Tests:\n");
    RUN_TEST(md5_empty_string);
    RUN_TEST(md5_hello);
    RUN_TEST(md5_hello_world);
    RUN_TEST(md5_long_string);
    RUN_TEST(md5_validation);

    printf("\nSHA1 Tests:\n");
    RUN_TEST(sha1_empty_string);
    RUN_TEST(sha1_hello);
    RUN_TEST(sha1_hello_world);
    RUN_TEST(sha1_long_string);
    RUN_TEST(sha1_validation);

    printf("\nSHA256 Tests:\n");
    RUN_TEST(sha256_empty_string);
    RUN_TEST(sha256_hello);
    RUN_TEST(sha256_hello_world);
    RUN_TEST(sha256_long_string);
    RUN_TEST(sha256_validation);

    printf("\nSHA512 Tests:\n");
    RUN_TEST(sha512_empty_string);
    RUN_TEST(sha512_hello);
    RUN_TEST(sha512_hello_world);
    RUN_TEST(sha512_validation);

    printf("\nHMAC-SHA256 Tests:\n");
    RUN_TEST(hmac_sha256_empty);
    RUN_TEST(hmac_sha256_basic);
    RUN_TEST(hmac_sha256_verify);

    printf("\nUtility Tests:\n");
    RUN_TEST(bytes_to_hex);
    RUN_TEST(hex_to_bytes);

    printf("\n============================================\n");
    printf("Results: %d passed, %d failed\n", tests_passed, tests_failed);
    printf("============================================\n");

    return tests_failed > 0 ? 1 : 0;
}

