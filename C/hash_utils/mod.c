/**
 * @file mod.c
 * @brief Hash Utilities Implementation - MD5, SHA1, SHA256, SHA512, HMAC
 *
 * Zero-dependency implementations of standard cryptographic hash functions.
 * All algorithms implemented from specifications:
 * - MD5: RFC 1321
 * - SHA1: FIPS PUB 180-1
 * - SHA256: FIPS PUB 180-2
 * - SHA512: FIPS PUB 180-2
 * - HMAC: RFC 2104
 *
 * @author AllToolkit
 * @version 1.0.0
 * @license MIT
 */

#include "mod.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

/* ============================================================================
 * MD5 Implementation (RFC 1321)
 * ============================================================================ */

#define MD5_F(x, y, z) (((x) & (y)) | (~(x) & (z)))
#define MD5_G(x, y, z) (((x) & (z)) | ((y) & ~(z)))
#define MD5_H(x, y, z) ((x) ^ (y) ^ (z))
#define MD5_I(x, y, z) ((y) ^ ((x) | ~(z)))

#define MD5_ROTATE_LEFT(x, n) (((x) << (n)) | ((x) >> (32 - (n))))

static const uint32_t md5_k[64] = {
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a,
    0xa8304613, 0xfd469501, 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340,
    0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8,
    0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 0x289b7ec6, 0xeaa127fa,
    0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92,
    0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
};

static const uint32_t md5_s[64] = {
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
};

static void md5_transform(hash_md5_ctx_t *ctx, const uint8_t block[64]) {
    uint32_t a = ctx->state[0], b = ctx->state[1], c = ctx->state[2], d = ctx->state[3];
    uint32_t x[16], f, g, temp;
    int i;

    for (i = 0; i < 16; i++) {
        x[i] = ((uint32_t)block[i * 4]) | (((uint32_t)block[i * 4 + 1]) << 8) |
               (((uint32_t)block[i * 4 + 2]) << 16) | (((uint32_t)block[i * 4 + 3]) << 24);
    }

    for (i = 0; i < 64; i++) {
        if (i < 16) {
            f = MD5_F(b, c, d);
            g = i;
        } else if (i < 32) {
            f = MD5_G(b, c, d);
            g = (5 * i + 1) % 16;
        } else if (i < 48) {
            f = MD5_H(b, c, d);
            g = (3 * i + 5) % 16;
        } else {
            f = MD5_I(b, c, d);
            g = (7 * i) % 16;
        }
        temp = d;
        d = c;
        c = b;
        b = b + MD5_ROTATE_LEFT((a + f + md5_k[i] + x[g]), md5_s[i]);
        a = temp;
    }

    ctx->state[0] += a;
    ctx->state[1] += b;
    ctx->state[2] += c;
    ctx->state[3] += d;
}

void hash_md5_init(hash_md5_ctx_t *ctx) {
    ctx->state[0] = 0x67452301;
    ctx->state[1] = 0xefcdab89;
    ctx->state[2] = 0x98badcfe;
    ctx->state[3] = 0x10325476;
    ctx->count[0] = ctx->count[1] = 0;
}

void hash_md5_update(hash_md5_ctx_t *ctx, const uint8_t *data, size_t len) {
    size_t i, index, part_len;

    index = (size_t)((ctx->count[0] >> 3) & 0x3f);
    ctx->count[0] += (uint32_t)(len << 3);
    if (ctx->count[0] < (uint32_t)(len << 3)) ctx->count[1]++;
    ctx->count[1] += (uint32_t)(len >> 29);

    part_len = 64 - index;

    if (len >= part_len) {
        memcpy(&ctx->buffer[index], data, part_len);
        md5_transform(ctx, ctx->buffer);
        for (i = part_len; i + 63 < len; i += 64) {
            md5_transform(ctx, &data[i]);
        }
        index = 0;
    } else {
        i = 0;
    }

    memcpy(&ctx->buffer[index], &data[i], len - i);
}

void hash_md5_final(hash_md5_ctx_t *ctx, uint8_t digest[HASH_MD5_SIZE]) {
    uint8_t bits[8];
    size_t index, pad_len;
    static const uint8_t padding[64] = {0x80};

    for (int i = 0; i < 8; i++) {
        bits[i] = (uint8_t)((ctx->count[i >> 2] >> ((i & 3) << 3)) & 0xff);
    }

    index = (size_t)((ctx->count[0] >> 3) & 0x3f);
    pad_len = (index < 56) ? (56 - index) : (120 - index);
    hash_md5_update(ctx, padding, pad_len);
    hash_md5_update(ctx, bits, 8);

    for (int i = 0; i < 4; i++) {
        digest[i] = (uint8_t)(ctx->state[0] >> (i * 8));
        digest[i + 4] = (uint8_t)(ctx->state[1] >> (i * 8));
        digest[i + 8] = (uint8_t)(ctx->state[2] >> (i * 8));
        digest[i + 12] = (uint8_t)(ctx->state[3] >> (i * 8));
    }
}

void hash_md5(const uint8_t *data, size_t len, uint8_t digest[HASH_MD5_SIZE]) {
    hash_md5_ctx_t ctx;
    hash_md5_init(&ctx);
    hash_md5_update(&ctx, data, len);
    hash_md5_final(&ctx, digest);
}

void hash_md5_string(const char *str, uint8_t digest[HASH_MD5_SIZE]) {
    hash_md5((const uint8_t *)str, strlen(str), digest);
}

char *hash_md5_hex(const uint8_t *data, size_t len, char *hex) {
    uint8_t digest[HASH_MD5_SIZE];
    hash_md5(data, len, digest);
    return hash_bytes_to_hex(digest, HASH_MD5_SIZE, hex);
}

char *hash_md5_string_hex(const char *str, char *hex) {
    return hash_md5_hex((const uint8_t *)str, strlen(str), hex);
}

/* ============================================================================
 * SHA1 Implementation (FIPS PUB 180-1)
 * ============================================================================ */

#define SHA1_ROTL(x, n) (((x) << (n)) | ((x) >> (32 - (n))))

static void sha1_transform(hash_sha1_ctx_t *ctx, const uint8_t block[64]) {
    uint32_t w[80], a, b, c, d, e, temp;
    int i;

    for (i = 0; i < 16; i++) {
        w[i] = ((uint32_t)block[i * 4] << 24) | ((uint32_t)block[i * 4 + 1] << 16) |
               ((uint32_t)block[i * 4 + 2] << 8) | (uint32_t)block[i * 4 + 3];
    }

    for (i = 16; i < 80; i++) {
        w[i] = SHA1_ROTL(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1);
    }

    a = ctx->state[0];
    b = ctx->state[1];
    c = ctx->state[2];
    d = ctx->state[3];
    e = ctx->state[4];

    for (i = 0; i < 80; i++) {
        if (i < 20) {
            temp = (b & c) | (~b & d);
            temp += 0x5a827999;
        } else if (i < 40) {
            temp = b ^ c ^ d;
            temp += 0x6ed9eba1;
        } else if (i < 60) {
            temp = (b & c) | (b & d) | (c & d);
            temp += 0x8f1bbcdc;
        } else {
            temp = b ^ c ^ d;
            temp += 0xca62c1d6;
        }
        temp += SHA1_ROTL(a, 5) + e + w[i];
        e = d;
        d = c;
        c = SHA1_ROTL(b, 30);
        b = a;
        a = temp;
    }

    ctx->state[0] += a;
    ctx->state[1] += b;
    ctx->state[2] += c;
    ctx->state[3] += d;
    ctx->state[4] += e;
}

void hash_sha1_init(hash_sha1_ctx_t *ctx) {
    ctx->state[0] = 0x67452301;
    ctx->state[1] = 0xefcdab89;
    ctx->state[2] = 0x98badcfe;
    ctx->state[3] = 0x10325476;
    ctx->state[4] = 0xc3d2e1f0;
    ctx->count[0] = ctx->count[1] = 0;
}

void hash_sha1_update(hash_sha1_ctx_t *ctx, const uint8_t *data, size_t len) {
    size_t i, index, part_len;

    index = (size_t)((ctx->count[0] >> 3) & 0x3f);
    ctx->count[0] += (uint32_t)(len << 3);
    if (ctx->count[0] < (uint32_t)(len << 3)) ctx->count[1]++;
    ctx->count[1] += (uint32_t)(len >> 29);

    part_len = 64 - index;

    if (len >= part_len) {
        memcpy(&ctx->buffer[index], data, part_len);
        sha1_transform(ctx, ctx->buffer);
        for (i = part_len; i + 63 < len; i += 64) {
            sha1_transform(ctx, &data[i]);
        }
        index = 0;
    } else {
        i = 0;
    }

    memcpy(&ctx->buffer[index], &data[i], len - i);
}

void hash_sha1_final(hash_sha1_ctx_t *ctx, uint8_t digest[HASH_SHA1_SIZE]) {
    uint8_t bits[8];
    size_t index, pad_len;
    static const uint8_t padding[64] = {0x80};

    for (int i = 0; i < 8; i++) {
        bits[i] = (uint8_t)((ctx->count[(i >> 2)] >> ((3 - (i & 3)) << 3)) & 0xff);
    }

    index = (size_t)((ctx->count[0] >> 3) & 0x3f);
    pad_len = (index < 56) ? (56 - index) : (120 - index);
    hash_sha1_update(ctx, padding, pad_len);
    hash_sha1_update(ctx, bits, 8);

    for (int i = 0; i < 5; i++) {
        digest[i * 4] = (uint8_t)((ctx->state[i] >> 24) & 0xff);
        digest[i * 4 + 1] = (uint8_t)((ctx->state[i] >> 16) & 0xff);
        digest[i * 4 + 2] = (uint8_t)((ctx->state[i] >> 8) & 0xff);
        digest[i * 4 + 3] = (uint8_t)(ctx->state[i] & 0xff);
    }
}

void hash_sha1(const uint8_t *data, size_t len, uint8_t digest[HASH_SHA1_SIZE]) {
    hash_sha1_ctx_t ctx;
    hash_sha1_init(&ctx);
    hash_sha1_update(&ctx, data, len);
    hash_sha1_final(&ctx, digest);
}

void hash_sha1_string(const char *str, uint8_t digest[HASH_SHA1_SIZE]) {
    hash_sha1((const uint8_t *)str, strlen(str), digest);
}

char *hash_sha1_hex(const uint8_t *data, size_t len, char *hex) {
    uint8_t digest[HASH_SHA1_SIZE];
    hash_sha1(data, len, digest);
    return hash_bytes_to_hex(digest, HASH_SHA1_SIZE, hex);
}

char *hash_sha1_string_hex(const char *str, char *hex) {
    return hash_sha1_hex((const uint8_t *)str, strlen(str), hex);
}

/* ============================================================================
 * SHA256 Implementation (FIPS PUB 180-2)
 * ============================================================================ */

static const uint32_t sha256_k[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
    0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
    0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
    0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
    0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
    0x5b9cca4f, 0x7763e373, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814,
    0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};

#define SHA256_ROTR(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
#define SHA256_CH(x, y, z) (((x) & (y)) ^ (~(x) & (z)))
#define SHA256_MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define SHA256_EP0(x) (SHA256_ROTR(x, 2) ^ SHA256_ROTR(x, 13) ^ SHA256_ROTR(x, 22))
#define SHA256_EP1(x) (SHA256_ROTR(x, 6) ^ SHA256_ROTR(x, 11) ^ SHA256_ROTR(x, 25))
#define SHA256_SIG0(x) (SHA256_ROTR(x, 7) ^ SHA256_ROTR(x, 18) ^ ((x) >> 3))
#define SHA256_SIG1(x) (SHA256_ROTR(x, 17) ^ SHA256_ROTR(x, 19) ^ ((x) >> 10))

static void sha256_transform(hash_sha256_ctx_t *ctx, const uint8_t block[64]) {
    uint32_t a, b, c, d, e, f, g, h, t1, t2, m[64];
    int i;

    for (i = 0; i < 16; i++) {
        m[i] = ((uint32_t)block[i * 4] << 24) | ((uint32_t)block[i * 4 + 1] << 16) |
               ((uint32_t)block[i * 4 + 2] << 8) | (uint32_t)block[i * 4 + 3];
    }

    for (i = 16; i < 64; i++) {
        m[i] = SHA256_SIG1(m[i - 2]) + m[i - 7] + SHA256_SIG0(m[i - 15]) + m[i - 16];
    }

    a = ctx->state[0];
    b = ctx->state[1];
    c = ctx->state[2];
    d = ctx->state[3];
    e = ctx->state[4];
    f = ctx->state[5];
    g = ctx->state[6];
    h = ctx->state[7];

    for (i = 0; i < 64; i++) {
        t1 = h + SHA256_EP1(e) + SHA256_CH(e, f, g) + sha256_k[i] + m[i];
        t2 = SHA256_EP0(a) + SHA256_MAJ(a, b, c);
        h = g;
        g = f;
        f = e;
        e = d + t1;
        d = c;
        c = b;
        b = a;
        a = t1 + t2;
    }

    ctx->state[0] += a;
    ctx->state[1] += b;
    ctx->state[2] += c;
    ctx->state[3] += d;
    ctx->state[4] += e;
    ctx->state[5] += f;
    ctx->state[6] += g;
    ctx->state[7] += h;
}

void hash_sha256_init(hash_sha256_ctx_t *ctx) {
    ctx->state[0] = 0x6a09e667;
    ctx->state[1] = 0xbb67ae85;
    ctx->state[2] = 0x3c6ef372;
    ctx->state[3] = 0xa54ff53a;
    ctx->state[4] = 0x510e527f;
    ctx->state[5] = 0x9b05688c;
    ctx->state[6] = 0x1f83d9ab;
    ctx->state[7] = 0x5be0cd19;
    ctx->count[0] = ctx->count[1] = 0;
}

void hash_sha256_update(hash_sha256_ctx_t *ctx, const uint8_t *data, size_t len) {
    size_t i, index, part_len;

    index = (size_t)((ctx->count[0] >> 3) & 0x3f);
    ctx->count[0] += (uint32_t)(len << 3);
    if (ctx->count[0] < (uint32_t)(len << 3)) ctx->count[1]++;
    ctx->count[1] += (uint32_t)(len >> 29);

    part_len = 64 - index;

    if (len >= part_len) {
        memcpy(&ctx->buffer[index], data, part_len);
        sha256_transform(ctx, ctx->buffer);
        for (i = part_len; i + 63 < len; i += 64) {
            sha256_transform(ctx, &data[i]);
        }
        index = 0;
    } else {
        i = 0;
    }

    memcpy(&ctx->buffer[index], &data[i], len - i);
}

void hash_sha256_final(hash_sha256_ctx_t *ctx, uint8_t digest[HASH_SHA256_SIZE]) {
    uint8_t bits[8];
    size_t index, pad_len;
    static const uint8_t padding[64] = {0x80};

    for (int i = 0; i < 8; i++) {
        bits[i] = (uint8_t)((ctx->count[(i >> 2)] >> ((3 - (i & 3)) << 3)) & 0xff);
    }

    index = (size_t)((ctx->count[0] >> 3) & 0x3f);
    pad_len = (index < 56) ? (56 - index) : (120 - index);
    hash_sha256_update(ctx, padding, pad_len);
    hash_sha256_update(ctx, bits, 8);

    for (int i = 0; i < 8; i++) {
        digest[i * 4] = (uint8_t)((ctx->state[i] >> 24) & 0xff);
        digest[i * 4 + 1] = (uint8_t)((ctx->state[i] >> 16) & 0xff);
        digest[i * 4 + 2] = (uint8_t)((ctx->state[i] >> 8) & 0xff);
        digest[i * 4 + 3] = (uint8_t)(ctx->state[i] & 0xff);
    }
}

void hash_sha256(const uint8_t *data, size_t len, uint8_t digest[HASH_SHA256_SIZE]) {
    hash_sha256_ctx_t ctx;
    hash_sha256_init(&ctx);
    hash_sha256_update(&ctx, data, len);
    hash_sha256_final(&ctx, digest);
}

void hash_sha256_string(const char *str, uint8_t digest[HASH_SHA256_SIZE]) {
    hash_sha256((const uint8_t *)str, strlen(str), digest);
}

char *hash_sha256_hex(const uint8_t *data, size_t len, char *hex) {
    uint8_t digest[HASH_SHA256_SIZE];
    hash_sha256(data, len, digest);
    return hash_bytes_to_hex(digest, HASH_SHA256_SIZE, hex);
}

char *hash_sha256_string_hex(const char *str, char *hex) {
    return hash_sha256_hex((const uint8_t *)str, strlen(str), hex);
}

/* ============================================================================
 * SHA512 Implementation (FIPS PUB 180-2)
 * ============================================================================ */

static const uint64_t sha512_k[80] = {
    0x428a2f98d728ae22ULL, 0x7137449123ef65cdULL, 0xb5c0fbcfec4d3b2fULL,
    0xe9b5dba58189dbbcULL, 0x3956c25bf348b538ULL, 0x59f111f1b605d019ULL,
    0x923f82a4af194f9bULL, 0xab1c5ed5da6d8118ULL, 0xd807aa98a3030242ULL,
    0x12835b0145706fbeULL, 0x243185be4ee4b28cULL, 0x550c7dc3d5ffb4e2ULL,
    0x72be5d74f27b896fULL, 0x80deb1fe3b1696b1ULL, 0x9bdc06a725c71235ULL,
    0xc19bf174cf692694ULL, 0xe49b69c19ef14ad2ULL, 0xefbe4786384f25e3ULL,
    0x0fc19dc68b8cd5b5ULL, 0x240ca1cc77ac9c65ULL, 0x2de92c6f592b0275ULL,
    0x4a7484aa6ea6e483ULL, 0x5cb0a9dcbd41fbd4ULL, 0x76f988da831153b5ULL,
    0x983e5152ee66dfabULL, 0xa831c66d2db43210ULL, 0xb00327c898fb213fULL,
    0xbf597fc7beef0ee4ULL, 0xc6e00bf33da88fc2ULL, 0xd5a79147930aa725ULL,
    0x06ca6351e003826fULL, 0x142929670a0e6e70ULL, 0x27b70a8546d22ffcULL,
    0x2e1b21385c26c926ULL, 0x4d2c6dfc5ac42aedULL, 0x53380d139d95b3dfULL,
    0x650a73548baf63deULL, 0x766a0abb3c77b2a8ULL, 0x81c2c92e47edaee6ULL,
    0x92722c851482353bULL, 0xa2bfe8a14cf10364ULL, 0xa81a664bbc423001ULL,
    0xc24b8b70d0f89791ULL, 0xc76c51a30654be30ULL, 0xd192e819d6ef5218ULL,
    0xd69906245565a910ULL, 0xf40e35855771202aULL, 0x106aa07032bbd1b8ULL,
    0x19a4c116b8d2d0c8ULL, 0x1e376c085141ab53ULL, 0x2748774cdf8eeb99ULL,
    0x34b0bcb5e19b48a8ULL, 0x391c0cb3c5c95a63ULL, 0x4ed8aa4ae3418acbULL,
    0x5b9cca4f7763e373ULL, 0x682e6ff3d6b2b8a3ULL, 0x748f82ee5defb2fcULL,
    0x78a5636f43172f60ULL, 0x84c87814a1f0ab72ULL, 0x8cc702081a6439ecULL,
    0x90befffa23631e28ULL, 0xa4506cebde82bde9ULL, 0xbef9a3f7b2c67915ULL,
    0xc67178f2e372532bULL, 0xca273eceea26619cULL, 0xd186b8c721c0c207ULL,
    0xeada7dd6cde0eb1eULL, 0xf57d4f7fee6ed178ULL, 0x06f067aa72176fbaULL,
    0x0a637dc5a2c898a6ULL, 0x113f9804bef90daeULL, 0x1b710b35131c471bULL,
    0x28db77f523047d84ULL, 0x32caab7b40c72493ULL, 0x3c9ebe0a15c9bebcULL,
    0x431d67c49c100d4cULL, 0x4cc5d4becb3e42b6ULL, 0x597f299cfc657e2aULL,
    0x5fcb6fab3ad6faecULL, 0x6c44198c4a475817ULL
};

#define SHA512_ROTR(x, n) (((x) >> (n)) | ((x) << (64 - (n))))
#define SHA512_CH(x, y, z) (((x) & (y)) ^ (~(x) & (z)))
#define SHA512_MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define SHA512_EP0(x) (SHA512_ROTR(x, 28) ^ SHA512_ROTR(x, 34) ^ SHA512_ROTR(x, 39))
#define SHA512_EP1(x) (SHA512_ROTR(x, 14) ^ SHA512_ROTR(x, 18) ^ SHA512_ROTR(x, 41))
#define SHA512_SIG0(x) (SHA512_ROTR(x, 1) ^ SHA512_ROTR(x, 8) ^ ((x) >> 7))
#define SHA512_SIG1(x) (SHA512_ROTR(x, 19) ^ SHA512_ROTR(x, 61) ^ ((x) >> 6))

static void sha512_transform(hash_sha512_ctx_t *ctx, const uint8_t block[128]) {
    uint64_t a, b, c, d, e, f, g, h, t1, t2, m[80];
    int i;

    for (i = 0; i < 16; i++) {
        m[i] = ((uint64_t)block[i * 8] << 56) | ((uint64_t)block[i * 8 + 1] << 48) |
               ((uint64_t)block[i * 8 + 2] << 40) | ((uint64_t)block[i * 8 + 3] << 32) |
               ((uint64_t)block[i * 8 + 4] << 24) | ((uint64_t)block[i * 8 + 5] << 16) |
               ((uint64_t)block[i * 8 + 6] << 8) | (uint64_t)block[i * 8 + 7];
    }

    for (i = 16; i < 80; i++) {
        m[i] = SHA512_SIG1(m[i - 2]) + m[i - 7] + SHA512_SIG0(m[i - 15]) + m[i - 16];
    }

    a = ctx->state[0];
    b = ctx->state[1];
    c = ctx->state[2];
    d = ctx->state[3];
    e = ctx->state[4];
    f = ctx->state[5];
    g = ctx->state[6];
    h = ctx->state[7];

    for (i = 0; i < 80; i++) {
        t1 = h + SHA512_EP1(e) + SHA512_CH(e, f, g) + sha512_k[i] + m[i];
        t2 = SHA512_EP0(a) + SHA512_MAJ(a, b, c);
        h = g;
        g = f;
        f = e;
        e = d + t1;
        d = c;
        c = b;
        b = a;
        a = t1 + t2;
    }

    ctx->state[0] += a;
    ctx->state[1] += b;
    ctx->state[2] += c;
    ctx->state[3] += d;
    ctx->state[4] += e;
    ctx->state[5] += f;
    ctx->state[6] += g;
    ctx->state[7] += h;
}

void hash_sha512_init(hash_sha512_ctx_t *ctx) {
    ctx->state[0] = 0x6a09e667f3bcc908ULL;
    ctx->state[1] = 0xbb67ae8584caa73bULL;
    ctx->state[2] = 0x3c6ef372fe94f82bULL;
    ctx->state[3] = 0xa54ff53a5f1d36f1ULL;
    ctx->state[4] = 0x510e527fade682d1ULL;
    ctx->state[5] = 0x9b05688c2b3e6c1fULL;
    ctx->state[6] = 0x1f83d9abfb41bd6bULL;
    ctx->state[7] = 0x5be0cd19137e2179ULL;
    ctx->count[0] = ctx->count[1] = 0;
}

void hash_sha512_update(hash_sha512_ctx_t *ctx, const uint8_t *data, size_t len) {
    size_t i, index, part_len;

    index = (size_t)((ctx->count[0] >> 3) & 0x7f);
    ctx->count[0] += (uint64_t)(len << 3);
    if (ctx->count[0] < (uint64_t)(len << 3)) ctx->count[1]++;
    ctx->count[1] += (uint64_t)(len >> 61);

    part_len = 128 - index;

    if (len >= part_len) {
        memcpy(&ctx->buffer[index], data, part_len);
        sha512_transform(ctx, ctx->buffer);
        for (i = part_len; i + 127 < len; i += 128) {
            sha512_transform(ctx, &data[i]);
        }
        index = 0;
    } else {
        i = 0;
    }

    memcpy(&ctx->buffer[index], &data[i], len - i);
}

void hash_sha512_final(hash_sha512_ctx_t *ctx, uint8_t digest[HASH_SHA512_SIZE]) {
    uint8_t bits[16];
    size_t index, pad_len;
    static const uint8_t padding[128] = {0x80};

    for (int i = 0; i < 16; i++) {
        bits[i] = (uint8_t)((ctx->count[(i >> 3)] >> ((7 - (i & 7)) << 3)) & 0xff);
    }

    index = (size_t)((ctx->count[0] >> 3) & 0x7f);
    pad_len = (index < 112) ? (112 - index) : (240 - index);
    hash_sha512_update(ctx, padding, pad_len);
    hash_sha512_update(ctx, bits, 16);

    for (int i = 0; i < 8; i++) {
        digest[i * 8] = (uint8_t)((ctx->state[i] >> 56) & 0xff);
        digest[i * 8 + 1] = (uint8_t)((ctx->state[i] >> 48) & 0xff);
        digest[i * 8 + 2] = (uint8_t)((ctx->state[i] >> 40) & 0xff);
        digest[i * 8 + 3] = (uint8_t)((ctx->state[i] >> 32) & 0xff);
        digest[i * 8 + 4] = (uint8_t)((ctx->state[i] >> 24) & 0xff);
        digest[i * 8 + 5] = (uint8_t)((ctx->state[i] >> 16) & 0xff);
        digest[i * 8 + 6] = (uint8_t)((ctx->state[i] >> 8) & 0xff);
        digest[i * 8 + 7] = (uint8_t)(ctx->state[i] & 0xff);
    }
}

void hash_sha512(const uint8_t *data, size_t len, uint8_t digest[HASH_SHA512_SIZE]) {
    hash_sha512_ctx_t ctx;
    hash_sha512_init(&ctx);
    hash_sha512_update(&ctx, data, len);
    hash_sha512_final(&ctx, digest);
}

void hash_sha512_string(const char *str, uint8_t digest[HASH_SHA512_SIZE]) {
    hash_sha512((const uint8_t *)str, strlen(str), digest);
}

char *hash_sha512_hex(const uint8_t *data, size_t len, char *hex) {
    uint8_t digest[HASH_SHA512_SIZE];
    hash_sha512(data, len, digest);
    return hash_bytes_to_hex(digest, HASH_SHA512_SIZE, hex);
}

char *hash_sha512_string_hex(const char *str, char *hex) {
    return hash_sha512_hex((const uint8_t *)str, strlen(str), hex);
}

/* ============================================================================
 * HMAC-SHA256 Implementation (RFC 2104)
 * ============================================================================ */

void hash_hmac_sha256(const uint8_t *key, size_t key_len,
                      const uint8_t *data, size_t data_len,
                      uint8_t digest[HASH_SHA256_SIZE]) {
    hash_sha256_ctx_t ctx;
    uint8_t k_ipad[64], k_opad[64];
    uint8_t tk[HASH_SHA256_SIZE];
    int i;

    if (key_len > 64) {
        hash_sha256(key, key_len, tk);
        key = tk;
        key_len = HASH_SHA256_SIZE;
    }

    memset(k_ipad, 0, sizeof(k_ipad));
    memset(k_opad, 0, sizeof(k_opad));
    memcpy(k_ipad, key, key_len);
    memcpy(k_opad, key, key_len);

    for (i = 0; i < 64; i++) {
        k_ipad[i] ^= 0x36;
        k_opad[i] ^= 0x5c;
    }

    hash_sha256_init(&ctx);
    hash_sha256_update(&ctx, k_ipad, 64);
    hash_sha256_update(&ctx, data, data_len);
    hash_sha256_final(&ctx, digest);

    hash_sha256_init(&ctx);
    hash_sha256_update(&ctx, k_opad, 64);
    hash_sha256_update(&ctx, digest, HASH_SHA256_SIZE);
    hash_sha256_final(&ctx, digest);
}

char *hash_hmac_sha256_hex(const char *key, const char *data, char *hex) {
    uint8_t digest[HASH_SHA256_SIZE];
    hash_hmac_sha256((const uint8_t *)key, strlen(key),
                     (const uint8_t *)data, strlen(data), digest);
    return hash_bytes_to_hex(digest, HASH_SHA256_SIZE, hex);
}

bool hash_hmac_sha256_verify(const char *key, const char *data, const char *expected_hex) {
    char computed[HASH_SHA256_HEX_LEN];
    hash_hmac_sha256_hex(key, data, computed);
    return strcmp(computed, expected_hex) == 0;
}

/* ============================================================================
 * Utility Functions
 * ============================================================================ */

static const char hex_chars[] = "0123456789abcdef";

char *hash_bytes_to_hex(const uint8_t *bytes, size_t len, char *hex) {
    for (size_t i = 0; i < len; i++) {
        hex[i * 2] = hex_chars[bytes[i] >> 4];
        hex[i * 2 + 1] = hex_chars[bytes[i] & 0xf];
    }
    hex[len * 2] = '\0';
    return hex;
}

bool hash_hex_to_bytes(const char *hex, uint8_t *bytes, size_t max_len) {
    size_t len = strlen(hex);
    if (len % 2 != 0 || len / 2 > max_len) return false;

    for (size_t i = 0; i < len / 2; i++) {
        int high, low;
        char c1 = hex[i * 2], c2 = hex[i * 2 + 1];

        if (c1 >= '0' && c1 <= '9') high = c1 - '0';
        else if (c1 >= 'a' && c1 <= 'f') high = c1 - 'a' + 10;
        else if (c1 >= 'A' && c1 <= 'F') high = c1 - 'A' + 10;
        else return false;

        if (c2 >= '0' && c2 <= '9') low = c2 - '0';
        else if (c2 >= 'a' && c2 <= 'f') low = c2 - 'a' + 10;
        else if (c2 >= 'A' && c2 <= 'F') low = c2 - 'A' + 10;
        else return false;

        bytes[i] = (uint8_t)((high << 4) | low);
    }
    return true;
}

static bool is_valid_hex_of_len(const char *hex, size_t expected_len) {
    if (hex == NULL) return false;
    size_t len = strlen(hex);
    if (len != expected_len) return false;

    for (size_t i = 0; i < len; i++) {
        char c = hex[i];
        if (!((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F'))) {
            return false;
        }
    }
    return true;
}

bool hash_is_valid_md5(const char *hex) {
    return is_valid_hex_of_len(hex, 32);
}

bool hash_is_valid_sha1(const char *hex) {
    return is_valid_hex_of_len(hex, 40);
}

bool hash_is_valid_sha256(const char *hex) {
    return is_valid_hex_of_len(hex, 64);
}

bool hash_is_valid_sha512(const char *hex) {
    return is_valid_hex_of_len(hex, 128);
}
