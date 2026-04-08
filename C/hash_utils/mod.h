/**
 * @file mod.h
 * @brief Hash Utilities - Zero-dependency cryptographic hash functions for C
 *
 * A comprehensive hash utility module providing MD5, SHA1, SHA256, SHA512
 * hash calculations and HMAC-SHA256 message authentication codes.
 * All implementations use only standard C library - no external dependencies.
 *
 * Features:
 * - MD5 hash (32-character hex string)
 * - SHA1 hash (40-character hex string)
 * - SHA256 hash (64-character hex string)
 * - SHA512 hash (128-character hex string)
 * - HMAC-SHA256 for message authentication
 * - Hex encoding/decoding utilities
 * - Hash validation functions
 *
 * @author AllToolkit
 * @version 1.0.0
 * @license MIT
 */

#ifndef HASH_UTILS_H
#define HASH_UTILS_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ============================================================================
 * Constants
 * ============================================================================ */

#define HASH_MD5_SIZE       16
#define HASH_SHA1_SIZE      20
#define HASH_SHA256_SIZE    32
#define HASH_SHA512_SIZE    64
#define HASH_MAX_SIZE       HASH_SHA512_SIZE

#define HASH_MD5_HEX_LEN    33
#define HASH_SHA1_HEX_LEN   41
#define HASH_SHA256_HEX_LEN 65
#define HASH_SHA512_HEX_LEN 129

/* ============================================================================
 * Hash Context Structures
 * ============================================================================ */

typedef struct {
    uint32_t state[4];
    uint32_t count[2];
    uint8_t buffer[64];
} hash_md5_ctx_t;

typedef struct {
    uint32_t state[5];
    uint32_t count[2];
    uint8_t buffer[64];
} hash_sha1_ctx_t;

typedef struct {
    uint32_t state[8];
    uint32_t count[2];
    uint8_t buffer[64];
} hash_sha256_ctx_t;

typedef struct {
    uint64_t state[8];
    uint64_t count[2];
    uint8_t buffer[128];
} hash_sha512_ctx_t;

/* ============================================================================
 * MD5 Functions
 * ============================================================================ */

void hash_md5_init(hash_md5_ctx_t *ctx);
void hash_md5_update(hash_md5_ctx_t *ctx, const uint8_t *data, size_t len);
void hash_md5_final(hash_md5_ctx_t *ctx, uint8_t digest[HASH_MD5_SIZE]);
void hash_md5(const uint8_t *data, size_t len, uint8_t digest[HASH_MD5_SIZE]);
void hash_md5_string(const char *str, uint8_t digest[HASH_MD5_SIZE]);
char *hash_md5_hex(const uint8_t *data, size_t len, char *hex);
char *hash_md5_string_hex(const char *str, char *hex);

/* ============================================================================
 * SHA1 Functions
 * ============================================================================ */

void hash_sha1_init(hash_sha1_ctx_t *ctx);
void hash_sha1_update(hash_sha1_ctx_t *ctx, const uint8_t *data, size_t len);
void hash_sha1_final(hash_sha1_ctx_t *ctx, uint8_t digest[HASH_SHA1_SIZE]);
void hash_sha1(const uint8_t *data, size_t len, uint8_t digest[HASH_SHA1_SIZE]);
void hash_sha1_string(const char *str, uint8_t digest[HASH_SHA1_SIZE]);
char *hash_sha1_hex(const uint8_t *data, size_t len, char *hex);
char *hash_sha1_string_hex(const char *str, char *hex);

/* ============================================================================
 * SHA256 Functions
 * ============================================================================ */

void hash_sha256_init(hash_sha256_ctx_t *ctx);
void hash_sha256_update(hash_sha256_ctx_t *ctx, const uint8_t *data, size_t len);
void hash_sha256_final(hash_sha256_ctx_t *ctx, uint8_t digest[HASH_SHA256_SIZE]);
void hash_sha256(const uint8_t *data, size_t len, uint8_t digest[HASH_SHA256_SIZE]);
void hash_sha256_string(const char *str, uint8_t digest[HASH_SHA256_SIZE]);
char *hash_sha256_hex(const uint8_t *data, size_t len, char *hex);
char *hash_sha256_string_hex(const char *str, char *hex);

/* ============================================================================
 * SHA512 Functions
 * ============================================================================ */

void hash_sha512_init(hash_sha512_ctx_t *ctx);
void hash_sha512_update(hash_sha512_ctx_t *ctx, const uint8_t *data, size_t len);
void hash_sha512_final(hash_sha512_ctx_t *ctx, uint8_t digest[HASH_SHA512_SIZE]);
void hash_sha512(const uint8_t *data, size_t len, uint8_t digest[HASH_SHA512_SIZE]);
void hash_sha512_string(const char *str, uint8_t digest[HASH_SHA512_SIZE]);
char *hash_sha512_hex(const uint8_t *data, size_t len, char *hex);
char *hash_sha512_string_hex(const char *str, char *hex);

/* ============================================================================
 * HMAC-SHA256 Functions
 * ============================================================================ */

void hash_hmac_sha256(const uint8_t *key, size_t key_len,
                      const uint8_t *data, size_t data_len,
                      uint8_t digest[HASH_SHA256_SIZE]);
char *hash_hmac_sha256_hex(const char *key, const char *data, char *hex);
bool hash_hmac_sha256_verify(const char *key, const char *data, const char *expected_hex);

/* ============================================================================
 * Utility Functions
 * ============================================================================ */

char *hash_bytes_to_hex(const uint8_t *bytes, size_t len, char *hex);
bool hash_hex_to_bytes(const char *hex, uint8_t *bytes, size_t max_len);
bool hash_is_valid_md5(const char *hex);
bool hash_is_valid_sha1(const char *hex);
bool hash_is_valid_sha256(const char *hex);
bool hash_is_valid_sha512(const char *hex);

#ifdef __cplusplus
}
#endif

#endif /* HASH_UTILS_H */
