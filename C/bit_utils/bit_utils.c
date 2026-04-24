/**
 * @file bit_utils.c
 * @brief 位操作工具库实现
 */

#include "bit_utils.h"
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/* ============================================================
 * 基本位操作
 * ============================================================ */

uint64_t bit_set(uint64_t value, uint8_t bit) {
    if (bit >= 64) return value;
    return value | ((uint64_t)1 << bit);
}

uint64_t bit_clear(uint64_t value, uint8_t bit) {
    if (bit >= 64) return value;
    return value & ~((uint64_t)1 << bit);
}

uint64_t bit_toggle(uint64_t value, uint8_t bit) {
    if (bit >= 64) return value;
    return value ^ ((uint64_t)1 << bit);
}

bool bit_test(uint64_t value, uint8_t bit) {
    if (bit >= 64) return false;
    return (value & ((uint64_t)1 << bit)) != 0;
}

uint64_t bit_set_value(uint64_t value, uint8_t bit, bool set_value) {
    if (bit >= 64) return value;
    uint64_t mask = (uint64_t)1 << bit;
    return set_value ? (value | mask) : (value & ~mask);
}

/* ============================================================
 * 位计数
 * ============================================================ */

uint8_t bit_count(uint64_t value) {
    /* Brian Kernighan 算法 - 高效计算置位数量 */
    uint8_t count = 0;
    while (value) {
        value &= value - 1;
        count++;
    }
    return count;
}

uint8_t bit_count_zero(uint64_t value) {
    return 64 - bit_count(value);
}

bool bit_parity(uint64_t value) {
    /* 使用 XOR 折叠计算奇偶校验 */
    value ^= value >> 32;
    value ^= value >> 16;
    value ^= value >> 8;
    value ^= value >> 4;
    value ^= value >> 2;
    value ^= value >> 1;
    return (value & 1) != 0;
}

/* ============================================================
 * 位查找
 * ============================================================ */

int8_t bit_find_first_set(uint64_t value) {
    if (value == 0) return -1;
    
    /* 使用二分查找定位最低有效位 */
    int8_t pos = 0;
    uint64_t mask = 0xFFFFFFFF;
    
    if ((value & mask) == 0) {
        value >>= 32;
        pos += 32;
    }
    mask = 0xFFFF;
    if ((value & mask) == 0) {
        value >>= 16;
        pos += 16;
    }
    mask = 0xFF;
    if ((value & mask) == 0) {
        value >>= 8;
        pos += 8;
    }
    mask = 0xF;
    if ((value & mask) == 0) {
        value >>= 4;
        pos += 4;
    }
    mask = 0x3;
    if ((value & mask) == 0) {
        value >>= 2;
        pos += 2;
    }
    mask = 0x1;
    if ((value & mask) == 0) {
        pos += 1;
    }
    
    return pos;
}

int8_t bit_find_last_set(uint64_t value) {
    if (value == 0) return -1;
    
    /* 使用二分查找定位最高有效位 */
    int8_t pos = 63;
    uint64_t mask = 0xFFFFFFFF00000000ULL;
    
    if ((value & mask) == 0) {
        value <<= 32;
        pos -= 32;
    }
    mask = 0xFFFF000000000000ULL;
    if ((value & mask) == 0) {
        value <<= 16;
        pos -= 16;
    }
    mask = 0xFF00000000000000ULL;
    if ((value & mask) == 0) {
        value <<= 8;
        pos -= 8;
    }
    mask = 0xF000000000000000ULL;
    if ((value & mask) == 0) {
        value <<= 4;
        pos -= 4;
    }
    mask = 0xC000000000000000ULL;
    if ((value & mask) == 0) {
        value <<= 2;
        pos -= 2;
    }
    mask = 0x8000000000000000ULL;
    if ((value & mask) == 0) {
        pos -= 1;
    }
    
    return pos;
}

int8_t bit_find_first_zero(uint64_t value) {
    return bit_find_first_set(~value);
}

int8_t bit_find_last_zero(uint64_t value) {
    return bit_find_last_set(~value);
}

/* ============================================================
 * 位反转和旋转
 * ============================================================ */

uint64_t bit_reverse(uint64_t value) {
    /* 使用分治法反转位 */
    value = ((value & 0x5555555555555555ULL) << 1) | 
            ((value & 0xAAAAAAAAAAAAAAAAULL) >> 1);
    value = ((value & 0x3333333333333333ULL) << 2) | 
            ((value & 0xCCCCCCCCCCCCCCCCULL) >> 2);
    value = ((value & 0x0F0F0F0F0F0F0F0FULL) << 4) | 
            ((value & 0xF0F0F0F0F0F0F0F0ULL) >> 4);
    value = ((value & 0x00FF00FF00FF00FFULL) << 8) | 
            ((value & 0xFF00FF00FF00FF00ULL) >> 8);
    value = ((value & 0x0000FFFF0000FFFFULL) << 16) | 
            ((value & 0xFFFF0000FFFF0000ULL) >> 16);
    value = (value << 32) | (value >> 32);
    return value;
}

uint64_t bit_reverse_n(uint64_t value, uint8_t width) {
    if (width == 0 || width > 64) return value;
    
    /* 反转后保持低width位 */
    uint64_t result = bit_reverse(value);
    return result >> (64 - width);
}

uint64_t bit_rotate_left(uint64_t value, uint8_t shift, uint8_t width) {
    if (width == 0 || width > 64) return value;
    shift %= width;
    if (shift == 0) return value;
    
    uint64_t mask = (width == 64) ? ~0ULL : ((1ULL << width) - 1);
    value &= mask;
    return ((value << shift) | (value >> (width - shift))) & mask;
}

uint64_t bit_rotate_right(uint64_t value, uint8_t shift, uint8_t width) {
    if (width == 0 || width > 64) return value;
    shift %= width;
    if (shift == 0) return value;
    
    uint64_t mask = (width == 64) ? ~0ULL : ((1ULL << width) - 1);
    value &= mask;
    return ((value >> shift) | (value << (width - shift))) & mask;
}

/* ============================================================
 * 位掩码
 * ============================================================ */

uint64_t bit_mask_low(uint8_t n) {
    if (n >= 64) return ~0ULL;
    if (n == 0) return 0;
    return (1ULL << n) - 1;
}

uint64_t bit_mask_high(uint8_t n) {
    if (n >= 64) return ~0ULL;
    if (n == 0) return 0;
    return ~((1ULL << (64 - n)) - 1);
}

uint64_t bit_mask_range(uint8_t start, uint8_t end) {
    if (start > end || start >= 64) return 0;
    if (end >= 63) return ~0ULL << start;
    return ((1ULL << (end - start + 1)) - 1) << start;
}

uint64_t bit_extract(uint64_t value, uint8_t start, uint8_t end) {
    if (start > end || start >= 64) return 0;
    return (value >> start) & bit_mask_low(end - start + 1);
}

uint64_t bit_insert(uint64_t value, uint64_t insert, uint8_t start, uint8_t end) {
    if (start > end || start >= 64) return value;
    
    uint64_t mask = bit_mask_range(start, end);
    uint64_t width = end - start + 1;
    uint64_t insert_mask = bit_mask_low(width);
    
    return (value & ~mask) | ((insert & insert_mask) << start);
}

/* ============================================================
 * 字节序转换
 * ============================================================ */

uint16_t bit_swap16(uint16_t value) {
    return (value >> 8) | (value << 8);
}

uint32_t bit_swap32(uint32_t value) {
    value = ((value & 0xFF00FF00) >> 8) | ((value & 0x00FF00FF) << 8);
    value = (value >> 16) | (value << 16);
    return value;
}

uint64_t bit_swap64(uint64_t value) {
    value = ((value & 0xFF00FF00FF00FF00ULL) >> 8) | 
            ((value & 0x00FF00FF00FF00FFULL) << 8);
    value = ((value & 0xFFFF0000FFFF0000ULL) >> 16) | 
            ((value & 0x0000FFFF0000FFFFULL) << 16);
    value = (value >> 32) | (value << 32);
    return value;
}

uint16_t bit_le_to_be16(uint16_t value) {
    return bit_swap16(value);
}

uint32_t bit_le_to_be32(uint32_t value) {
    return bit_swap32(value);
}

uint64_t bit_le_to_be64(uint64_t value) {
    return bit_swap64(value);
}

uint16_t bit_be_to_le16(uint16_t value) {
    return bit_swap16(value);
}

uint32_t bit_be_to_le32(uint32_t value) {
    return bit_swap32(value);
}

uint64_t bit_be_to_le64(uint64_t value) {
    return bit_swap64(value);
}

/* ============================================================
 * 位字段操作
 * ============================================================ */

uint64_t bit_field_read(uint64_t value, uint8_t offset, uint8_t width) {
    if (width == 0 || width > 64 || offset >= 64) return 0;
    return (value >> offset) & bit_mask_low(width);
}

uint64_t bit_field_write(uint64_t value, uint64_t field_val, uint8_t offset, uint8_t width) {
    if (width == 0 || width > 64 || offset >= 64) return value;
    
    uint64_t mask = bit_mask_low(width) << offset;
    return (value & ~mask) | ((field_val << offset) & mask);
}

/* ============================================================
 * 位向量操作
 * ============================================================ */

BitVector* bit_vector_create(size_t size) {
    BitVector *bv = (BitVector*)malloc(sizeof(BitVector));
    if (!bv) return NULL;
    
    size_t bytes = (size + 7) / 8;
    bv->data = (uint8_t*)calloc(bytes, 1);
    if (!bv->data) {
        free(bv);
        return NULL;
    }
    
    bv->size = size;
    bv->capacity = bytes;
    return bv;
}

void bit_vector_destroy(BitVector *bv) {
    if (bv) {
        free(bv->data);
        free(bv);
    }
}

int bit_vector_get(const BitVector *bv, size_t index) {
    if (!bv || index >= bv->size) return -1;
    return (bv->data[index / 8] >> (index % 8)) & 1;
}

int bit_vector_set(BitVector *bv, size_t index, bool value) {
    if (!bv || index >= bv->size) return -1;
    
    size_t byte_idx = index / 8;
    uint8_t bit_idx = index % 8;
    
    if (value) {
        bv->data[byte_idx] |= (1 << bit_idx);
    } else {
        bv->data[byte_idx] &= ~(1 << bit_idx);
    }
    return 0;
}

int bit_vector_toggle(BitVector *bv, size_t index) {
    if (!bv || index >= bv->size) return -1;
    
    size_t byte_idx = index / 8;
    uint8_t bit_idx = index % 8;
    
    bv->data[byte_idx] ^= (1 << bit_idx);
    return (bv->data[byte_idx] >> bit_idx) & 1;
}

void bit_vector_fill(BitVector *bv, bool value) {
    if (!bv || !bv->data) return;
    
    /* 填充所有字节 */
    memset(bv->data, value ? 0xFF : 0x00, bv->capacity);
    
    /* 如果大小不是8的倍数，清除超出部分的位 */
    if (value && bv->size % 8 != 0) {
        uint8_t extra_bits = bv->capacity * 8 - bv->size;
        uint8_t mask = (1 << (8 - extra_bits)) - 1;
        bv->data[bv->capacity - 1] &= mask;
    }
}

size_t bit_vector_count(const BitVector *bv) {
    if (!bv || !bv->data) return 0;
    
    size_t count = 0;
    for (size_t i = 0; i < bv->capacity; i++) {
        count += bit_count(bv->data[i]);
    }
    return count;
}

int bit_vector_resize(BitVector *bv, size_t new_size) {
    if (!bv) return -1;
    
    size_t new_bytes = (new_size + 7) / 8;
    uint8_t *new_data = (uint8_t*)realloc(bv->data, new_bytes);
    if (!new_data) return -1;
    
    bv->data = new_data;
    bv->size = new_size;
    bv->capacity = new_bytes;
    
    return 0;
}

/* ============================================================
 * 实用函数
 * ============================================================ */

bool bit_is_power_of_two(uint64_t value) {
    return value != 0 && (value & (value - 1)) == 0;
}

uint64_t bit_next_power_of_two(uint64_t value) {
    if (value == 0) return 1;
    if (bit_is_power_of_two(value)) return value;
    
    /* 向上取整到最近的2的幂 */
    value--;
    value |= value >> 1;
    value |= value >> 2;
    value |= value >> 4;
    value |= value >> 8;
    value |= value >> 16;
    value |= value >> 32;
    value++;
    
    return value;
}

uint64_t bit_prev_power_of_two(uint64_t value) {
    if (value <= 1) return 1;
    if (bit_is_power_of_two(value)) return value;
    
    /* 找到最高有效位 */
    int8_t msb = bit_find_last_set(value);
    return 1ULL << msb;
}

uint8_t bit_width(uint64_t value) {
    if (value == 0) return 0;
    return (uint8_t)(bit_find_last_set(value) + 1);
}

uint64_t bit_binary_to_gray(uint64_t value) {
    return value ^ (value >> 1);
}

uint64_t bit_gray_to_binary(uint64_t gray) {
    uint64_t mask = gray >> 1;
    while (mask) {
        gray ^= mask;
        mask >>= 1;
    }
    return gray;
}

char* bit_to_string(uint64_t value, char *buffer, uint8_t width) {
    if (!buffer || width == 0 || width > 64) return NULL;
    
    for (int8_t i = width - 1; i >= 0; i--) {
        *buffer++ = (value & (1ULL << i)) ? '1' : '0';
    }
    *buffer = '\0';
    return buffer - width;
}

int bit_from_string(const char *str, uint64_t *value) {
    if (!str || !value) return -1;
    
    *value = 0;
    
    /* 跳过前导空格和 0b/0B 前缀 */
    while (*str && isspace((unsigned char)*str)) str++;
    if (str[0] == '0' && (str[1] == 'b' || str[1] == 'B')) {
        str += 2;
    }
    
    /* 解析二进制字符 */
    while (*str) {
        if (*str == '0') {
            *value <<= 1;
        } else if (*str == '1') {
            *value = (*value << 1) | 1;
        } else if (!isspace((unsigned char)*str)) {
            return -1;  /* 无效字符 */
        }
        str++;
    }
    
    return 0;
}