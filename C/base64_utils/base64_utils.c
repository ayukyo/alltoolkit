/**
 * @file base64_utils.c
 * @brief Base64 编码/解码工具库实现
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-05-30
 */

#include "base64_utils.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ==================== 常量定义 ==================== */

/* 标准 Base64 字符集 */
const char* BASE64_STANDARD_CHARS = 
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

/* Base64URL 字符集 (URL 安全) */
const char* BASE64_URL_CHARS = 
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";

/* 解码查找表 */
static const int base64_decode_table[256] = {
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63,
    52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1,
    -1,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14,
    15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1,
    -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
    41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
};

/* URL 安全解码查找表 */
static int url_decode_table[256] = { -1 };
static int url_decode_table_initialized = 0;

/* 错误信息 */
static const char* last_error = NULL;

/* ==================== 内部辅助函数 ==================== */

static void init_url_decode_table(void) {
    if (url_decode_table_initialized) return;
    
    /* 复制标准表 */
    for (int i = 0; i < 256; i++) {
        url_decode_table[i] = base64_decode_table[i];
    }
    /* URL 安全字符替换 */
    url_decode_table['-'] = 62;  /* '+' -> '-' */
    url_decode_table['_'] = 63;  /* '/' -> '_' */
    /* 在 URL 安全模式下，+ 和 / 不是有效字符 */
    url_decode_table['+'] = -1;  /* '+' 无效 */
    url_decode_table['/'] = -1;  /* '/' 无效 */
    
    url_decode_table_initialized = 1;
}

static size_t min_size(size_t a, size_t b) {
    return (a < b) ? a : b;
}

/* ==================== 编码函数实现 ==================== */

size_t base64_encode_length(size_t input_len) {
    /* Base64 编码后长度 = ((input_len + 2) / 3) * 4 + 1 (null terminator) */
    return ((input_len + 2) / 3) * 4 + 1;
}

size_t base64_encode(const unsigned char* input, size_t input_len,
                     char* output, size_t output_size) {
    return base64_encode_custom(input, input_len, output, output_size,
                                BASE64_STANDARD_CHARS, '=');
}

size_t base64_encode_with_lines(const unsigned char* input, size_t input_len,
                                 char* output, size_t output_size,
                                 size_t line_width) {
    if (input == NULL || input_len == 0) {
        last_error = "Invalid input";
        return 0;
    }
    
    /* 计算需要的缓冲区大小 */
    size_t encoded_len = base64_encode_length(input_len) - 1;
    size_t num_lines = encoded_len / line_width;
    size_t total_len = encoded_len + num_lines; /* +1 for each newline */
    
    if (output == NULL) {
        return total_len + 1;
    }
    
    if (output_size < total_len + 1) {
        last_error = "Output buffer too small";
        return 0;
    }
    
    /* 先编码 */
    size_t actual_len = base64_encode(input, input_len, output, output_size);
    if (actual_len == 0) {
        return 0;
    }
    
    /* 添加换行符 */
    if (line_width > 0 && actual_len > line_width) {
        /* 需要移动数据来插入换行符 */
        char* temp = (char*)malloc(total_len + 1);
        if (temp == NULL) {
            last_error = "Memory allocation failed";
            return 0;
        }
        
        size_t src_idx = 0;
        size_t dst_idx = 0;
        
        while (src_idx < actual_len) {
            size_t copy_len = min_size(line_width, actual_len - src_idx);
            memcpy(temp + dst_idx, output + src_idx, copy_len);
            src_idx += copy_len;
            dst_idx += copy_len;
            
            if (src_idx < actual_len) {
                temp[dst_idx++] = '\n';
            }
        }
        
        temp[dst_idx] = '\0';
        memcpy(output, temp, dst_idx + 1);
        free(temp);
        
        return dst_idx;
    }
    
    return actual_len;
}

size_t base64url_encode(const unsigned char* input, size_t input_len,
                         char* output, size_t output_size) {
    return base64_encode_custom(input, input_len, output, output_size,
                                BASE64_URL_CHARS, '\0'); /* 无填充 */
}

size_t base64url_encode_with_padding(const unsigned char* input, size_t input_len,
                                      char* output, size_t output_size) {
    return base64_encode_custom(input, input_len, output, output_size,
                                BASE64_URL_CHARS, '=');
}

size_t base64_encode_custom(const unsigned char* input, size_t input_len,
                             char* output, size_t output_size,
                             const char* chars, char pad_char) {
    if (input == NULL && input_len > 0) {
        last_error = "Invalid input";
        return 0;
    }
    
    if (chars == NULL) {
        last_error = "Invalid character set";
        return 0;
    }
    
    size_t encoded_len = ((input_len + 2) / 3) * 4;
    
    if (output == NULL) {
        return encoded_len + 1; /* 包含空终止符 */
    }
    
    if (output_size < encoded_len + 1) {
        last_error = "Output buffer too small";
        return 0;
    }
    
    size_t i, j;
    size_t remaining;
    
    for (i = 0, j = 0; i < input_len; i += 3) {
        remaining = input_len - i;
        
        unsigned int octet_a = input[i];
        unsigned int octet_b = (remaining >= 2) ? input[i + 1] : 0;
        unsigned int octet_c = (remaining >= 3) ? input[i + 2] : 0;
        
        unsigned int triple = (octet_a << 16) + (octet_b << 8) + octet_c;
        
        output[j++] = chars[(triple >> 18) & 0x3F];
        output[j++] = chars[(triple >> 12) & 0x3F];
        
        if (remaining >= 2) {
            output[j++] = chars[(triple >> 6) & 0x3F];
        } else if (pad_char != '\0') {
            output[j++] = pad_char;
        }
        
        if (remaining >= 3) {
            output[j++] = chars[triple & 0x3F];
        } else if (pad_char != '\0') {
            output[j++] = pad_char;
        }
    }
    
    output[j] = '\0';
    last_error = NULL;
    
    return j;
}

/* ==================== 解码函数实现 ==================== */

size_t base64_decode_length(const char* input, size_t input_len) {
    if (input == NULL || input_len == 0) {
        return 0;
    }
    
    /* 计算去除空白后的长度 */
    size_t stripped_len = base64_strip_whitespace_length(input, input_len);
    
    /* Base64 解码后长度 */
    size_t padding = 0;
    if (stripped_len > 0 && input[stripped_len - 1] == '=') padding++;
    if (stripped_len > 1 && input[stripped_len - 2] == '=') padding++;
    
    return (stripped_len / 4) * 3 - padding;
}

static size_t base64_decode_internal(const char* input, size_t input_len,
                                      unsigned char* output, size_t output_size,
                                      const int* decode_table, bool url_mode) {
    if (input == NULL || input_len == 0) {
        last_error = "Invalid input";
        return (size_t)-1;
    }
    
    /* 去除空白字符 */
    char* stripped = (char*)malloc(input_len + 1);
    if (stripped == NULL) {
        last_error = "Memory allocation failed";
        return (size_t)-1;
    }
    
    size_t stripped_len = base64_strip_whitespace(input, input_len, 
                                                    stripped, input_len + 1);
    
    if (stripped_len == 0) {
        free(stripped);
        last_error = "Empty input after stripping whitespace";
        return (size_t)-1;
    }
    
    /* 验证长度必须是 4 的倍数 */
    if (!url_mode && stripped_len % 4 != 0) {
        free(stripped);
        last_error = "Invalid Base64 length";
        return (size_t)-1;
    }
    
    /* 计算输出长度 */
    size_t padding = 0;
    if (stripped_len >= 1 && stripped[stripped_len - 1] == '=') padding++;
    if (stripped_len >= 2 && stripped[stripped_len - 2] == '=') padding++;
    
    size_t decoded_len = (stripped_len / 4) * 3 - padding;
    
    if (output == NULL) {
        free(stripped);
        return decoded_len;
    }
    
    if (output_size < decoded_len) {
        free(stripped);
        last_error = "Output buffer too small";
        return (size_t)-1;
    }
    
    /* 解码 */
    size_t i, j;
    for (i = 0, j = 0; i < stripped_len; ) {
        int sextet_a = (stripped[i] == '=') ? 0 : decode_table[(unsigned char)stripped[i]];
        i++;
        int sextet_b = (i < stripped_len && stripped[i] == '=') ? 0 : 
                       (i < stripped_len ? decode_table[(unsigned char)stripped[i]] : 0);
        i++;
        int sextet_c = (i < stripped_len && stripped[i] == '=') ? 0 : 
                       (i < stripped_len ? decode_table[(unsigned char)stripped[i]] : 0);
        i++;
        int sextet_d = (i < stripped_len && stripped[i] == '=') ? 0 : 
                       (i < stripped_len ? decode_table[(unsigned char)stripped[i]] : 0);
        i++;
        
        if (sextet_a == -1 || sextet_b == -1 || sextet_c == -1 || sextet_d == -1) {
            free(stripped);
            last_error = "Invalid Base64 character";
            return (size_t)-1;
        }
        
        unsigned int triple = (sextet_a << 18) + (sextet_b << 12) + 
                              (sextet_c << 6) + sextet_d;
        
        if (j < decoded_len) output[j++] = (triple >> 16) & 0xFF;
        if (j < decoded_len) output[j++] = (triple >> 8) & 0xFF;
        if (j < decoded_len) output[j++] = triple & 0xFF;
    }
    
    free(stripped);
    last_error = NULL;
    
    return decoded_len;
}

size_t base64_decode(const char* input, size_t input_len,
                     unsigned char* output, size_t output_size) {
    return base64_decode_internal(input, input_len, output, output_size,
                                  base64_decode_table, false);
}

size_t base64url_decode(const char* input, size_t input_len,
                        unsigned char* output, size_t output_size) {
    init_url_decode_table();
    
    /* URL 解码允许非 4 的倍数的输入 */
    /* 需要先补齐 */
    char* padded_input = NULL;
    size_t padded_len = input_len;
    
    /* 如果长度不是 4 的倍数，需要补齐 */
    size_t remainder = input_len % 4;
    if (remainder != 0) {
        padded_len = input_len + (4 - remainder);
        padded_input = (char*)malloc(padded_len + 1);
        if (padded_input == NULL) {
            last_error = "Memory allocation failed";
            return (size_t)-1;
        }
        memcpy(padded_input, input, input_len);
        for (size_t i = input_len; i < padded_len; i++) {
            padded_input[i] = '=';
        }
        padded_input[padded_len] = '\0';
        input = padded_input;
    }
    
    size_t result = base64_decode_internal(input, padded_len, output, output_size,
                                            url_decode_table, true);
    
    if (padded_input != NULL) {
        free(padded_input);
    }
    
    return result;
}

size_t base64_decode_custom(const char* input, size_t input_len,
                             unsigned char* output, size_t output_size,
                             const char* chars, char pad_char) {
    if (chars == NULL) {
        last_error = "Invalid character set";
        return (size_t)-1;
    }
    
    /* 构建解码表 */
    int custom_decode_table[256];
    memset(custom_decode_table, -1, sizeof(custom_decode_table));
    
    for (int i = 0; i < 64; i++) {
        custom_decode_table[(unsigned char)chars[i]] = i;
    }
    
    if (pad_char != '\0') {
        custom_decode_table[(unsigned char)pad_char] = -2; /* 标记为填充 */
    }
    
    /* 使用标准解码逻辑 */
    if (input == NULL || input_len == 0) {
        last_error = "Invalid input";
        return (size_t)-1;
    }
    
    char* stripped = (char*)malloc(input_len + 1);
    if (stripped == NULL) {
        last_error = "Memory allocation failed";
        return (size_t)-1;
    }
    
    size_t stripped_len = base64_strip_whitespace(input, input_len, 
                                                    stripped, input_len + 1);
    
    if (stripped_len % 4 != 0) {
        free(stripped);
        last_error = "Invalid Base64 length";
        return (size_t)-1;
    }
    
    size_t padding = 0;
    if (stripped_len >= 1 && stripped[stripped_len - 1] == pad_char) padding++;
    if (stripped_len >= 2 && stripped[stripped_len - 2] == pad_char) padding++;
    
    size_t decoded_len = (stripped_len / 4) * 3 - padding;
    
    if (output == NULL) {
        free(stripped);
        return decoded_len;
    }
    
    if (output_size < decoded_len) {
        free(stripped);
        last_error = "Output buffer too small";
        return (size_t)-1;
    }
    
    size_t i, j;
    for (i = 0, j = 0; i < stripped_len; ) {
        int sextet_a = custom_decode_table[(unsigned char)stripped[i]];
        int sextet_b = custom_decode_table[(unsigned char)stripped[i + 1]];
        int sextet_c = custom_decode_table[(unsigned char)stripped[i + 2]];
        int sextet_d = custom_decode_table[(unsigned char)stripped[i + 3]];
        
        if (sextet_a < 0 || sextet_b < 0) {
            free(stripped);
            last_error = "Invalid Base64 character";
            return (size_t)-1;
        }
        
        sextet_c = (sextet_c == -2) ? 0 : sextet_c;
        sextet_d = (sextet_d == -2) ? 0 : sextet_d;
        
        if (sextet_c == -1 || sextet_d == -1) {
            free(stripped);
            last_error = "Invalid Base64 character";
            return (size_t)-1;
        }
        
        i += 4;
        
        unsigned int triple = (sextet_a << 18) + (sextet_b << 12) + 
                              (sextet_c << 6) + sextet_d;
        
        if (j < decoded_len) output[j++] = (triple >> 16) & 0xFF;
        if (j < decoded_len) output[j++] = (triple >> 8) & 0xFF;
        if (j < decoded_len) output[j++] = triple & 0xFF;
    }
    
    free(stripped);
    last_error = NULL;
    
    return decoded_len;
}

/* ==================== 验证函数实现 ==================== */

bool base64_is_valid(const char* input, size_t input_len) {
    if (input == NULL || input_len == 0) {
        return false;
    }
    
    /* 去除空白 */
    char* stripped = (char*)malloc(input_len + 1);
    if (stripped == NULL) {
        return false;
    }
    
    size_t stripped_len = base64_strip_whitespace(input, input_len, 
                                                    stripped, input_len + 1);
    
    if (stripped_len == 0 || stripped_len % 4 != 0) {
        free(stripped);
        return false;
    }
    
    /* 验证字符 */
    for (size_t i = 0; i < stripped_len; i++) {
        char c = stripped[i];
        if (i >= stripped_len - 2) {
            /* 最后两个字符可以是填充字符 */
            if (c == '=') continue;
        }
        if (base64_decode_table[(unsigned char)c] == -1) {
            free(stripped);
            return false;
        }
    }
    
    /* 填充必须正确 */
    size_t eq_pos = stripped_len;
    for (size_t i = stripped_len; i > 0; i--) {
        if (stripped[i - 1] == '=') {
            eq_pos = i - 1;
        } else {
            break;
        }
    }
    
    if (eq_pos < stripped_len) {
        /* 必须是 1 或 2 个等号 */
        if (eq_pos != stripped_len - 1 && eq_pos != stripped_len - 2) {
            free(stripped);
            return false;
        }
    }
    
    free(stripped);
    return true;
}

bool base64url_is_valid(const char* input, size_t input_len) {
    if (input == NULL || input_len == 0) {
        return false;
    }
    
    init_url_decode_table();
    
    for (size_t i = 0; i < input_len; i++) {
        char c = input[i];
        if (c == ' ' || c == '\n' || c == '\r' || c == '\t') continue;
        if (url_decode_table[(unsigned char)c] == -1) {
            return false;
        }
    }
    
    return true;
}

/* ==================== 字符串便捷函数实现 ==================== */

char* base64_encode_string(const char* str) {
    if (str == NULL) {
        return NULL;
    }
    
    size_t len = strlen(str);
    size_t encoded_len = base64_encode_length(len);
    
    char* output = (char*)malloc(encoded_len);
    if (output == NULL) {
        last_error = "Memory allocation failed";
        return NULL;
    }
    
    if (base64_encode((const unsigned char*)str, len, output, encoded_len) == 0) {
        free(output);
        return NULL;
    }
    
    return output;
}

unsigned char* base64_decode_string(const char* input, size_t* output_len) {
    if (input == NULL || output_len == NULL) {
        return NULL;
    }
    
    size_t input_len = strlen(input);
    size_t decoded_len = base64_decode_length(input, input_len);
    
    unsigned char* output = (unsigned char*)malloc(decoded_len + 1);
    if (output == NULL) {
        last_error = "Memory allocation failed";
        return NULL;
    }
    
    size_t actual_len = base64_decode(input, input_len, output, decoded_len);
    if (actual_len == (size_t)-1) {
        free(output);
        return NULL;
    }
    
    output[actual_len] = '\0';
    *output_len = actual_len;
    
    return output;
}

char* base64_encode_hex(const char* hex) {
    if (hex == NULL) {
        return NULL;
    }
    
    size_t hex_len = strlen(hex);
    if (hex_len % 2 != 0) {
        last_error = "Invalid hex string length";
        return NULL;
    }
    
    /* 转换十六进制到字节 */
    size_t byte_len = hex_len / 2;
    unsigned char* bytes = (unsigned char*)malloc(byte_len);
    if (bytes == NULL) {
        last_error = "Memory allocation failed";
        return NULL;
    }
    
    for (size_t i = 0; i < byte_len; i++) {
        unsigned int byte;
        if (sscanf(hex + i * 2, "%2x", &byte) != 1) {
            free(bytes);
            last_error = "Invalid hex character";
            return NULL;
        }
        bytes[i] = (unsigned char)byte;
    }
    
    /* 编码 */
    size_t encoded_len = base64_encode_length(byte_len);
    char* output = (char*)malloc(encoded_len);
    if (output == NULL) {
        free(bytes);
        last_error = "Memory allocation failed";
        return NULL;
    }
    
    base64_encode(bytes, byte_len, output, encoded_len);
    free(bytes);
    
    return output;
}

/* ==================== 文件操作函数实现 ==================== */

size_t base64_encode_file(const char* filepath, char* output, size_t output_size) {
    if (filepath == NULL) {
        last_error = "Invalid filepath";
        return (size_t)-1;
    }
    
    FILE* file = fopen(filepath, "rb");
    if (file == NULL) {
        last_error = "Cannot open file";
        return (size_t)-1;
    }
    
    /* 获取文件大小 */
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);
    
    if (file_size < 0) {
        fclose(file);
        last_error = "Cannot get file size";
        return (size_t)-1;
    }
    
    /* 读取文件内容 */
    unsigned char* buffer = (unsigned char*)malloc(file_size);
    if (buffer == NULL) {
        fclose(file);
        last_error = "Memory allocation failed";
        return (size_t)-1;
    }
    
    size_t read_len = fread(buffer, 1, file_size, file);
    fclose(file);
    
    if (read_len != (size_t)file_size) {
        free(buffer);
        last_error = "Failed to read file";
        return (size_t)-1;
    }
    
    /* 编码 */
    size_t result = base64_encode(buffer, read_len, output, output_size);
    free(buffer);
    
    return result;
}

bool base64_decode_to_file(const char* input, size_t input_len, const char* filepath) {
    if (input == NULL || filepath == NULL) {
        last_error = "Invalid input";
        return false;
    }
    
    /* 解码 */
    size_t decoded_len = base64_decode_length(input, input_len);
    unsigned char* decoded = (unsigned char*)malloc(decoded_len);
    if (decoded == NULL) {
        last_error = "Memory allocation failed";
        return false;
    }
    
    size_t actual_len = base64_decode(input, input_len, decoded, decoded_len);
    if (actual_len == (size_t)-1) {
        free(decoded);
        return false;
    }
    
    /* 写入文件 */
    FILE* file = fopen(filepath, "wb");
    if (file == NULL) {
        free(decoded);
        last_error = "Cannot open file for writing";
        return false;
    }
    
    size_t written = fwrite(decoded, 1, actual_len, file);
    fclose(file);
    free(decoded);
    
    if (written != actual_len) {
        last_error = "Failed to write file";
        return false;
    }
    
    return true;
}

/* ==================== 辅助函数实现 ==================== */

size_t base64_strip_whitespace_length(const char* input, size_t input_len) {
    if (input == NULL || input_len == 0) {
        return 0;
    }
    
    size_t count = 0;
    for (size_t i = 0; i < input_len; i++) {
        char c = input[i];
        if (c != ' ' && c != '\n' && c != '\r' && c != '\t') {
            count++;
        }
    }
    
    return count;
}

size_t base64_strip_whitespace(const char* input, size_t input_len,
                                char* output, size_t output_size) {
    if (input == NULL || output == NULL || output_size == 0) {
        return 0;
    }
    
    size_t j = 0;
    for (size_t i = 0; i < input_len && j < output_size - 1; i++) {
        char c = input[i];
        if (c != ' ' && c != '\n' && c != '\r' && c != '\t') {
            output[j++] = c;
        }
    }
    
    output[j] = '\0';
    return j;
}

const char* base64_get_error(void) {
    return last_error;
}