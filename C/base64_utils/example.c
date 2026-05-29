/**
 * @file example.c
 * @brief Base64 工具库使用示例
 * @author AllToolkit
 * @date 2026-05-30
 * 
 * 本文件展示 Base64 工具库的各种用法
 * 编译命令：gcc -o example example.c base64_utils.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "base64_utils.h"

void print_separator(const char* title) {
    printf("\n========================================\n");
    printf("  %s\n", title);
    printf("========================================\n");
}

void print_hex(const unsigned char* data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%02x ", data[i]);
        if ((i + 1) % 16 == 0) printf("\n");
    }
    if (len % 16 != 0) printf("\n");
}

/* 基础编码示例 */
void example_basic_encode(void) {
    print_separator("基础编码示例");
    
    const char* message = "Hello, World!";
    char encoded[256];
    
    printf("原始数据: %s\n", message);
    
    size_t len = base64_encode((const unsigned char*)message, strlen(message), 
                                 encoded, sizeof(encoded));
    
    printf("编码结果: %s\n", encoded);
    printf("编码长度: %zu 字符\n", len);
}

/* 基础解码示例 */
void example_basic_decode(void) {
    print_separator("基础解码示例");
    
    const char* encoded = "SGVsbG8sIFdvcmxkIQ==";
    unsigned char decoded[256];
    
    printf("编码数据: %s\n", encoded);
    
    size_t len = base64_decode(encoded, strlen(encoded), decoded, sizeof(decoded));
    
    if (len != (size_t)-1) {
        decoded[len] = '\0';  /* 添加空终止符 */
        printf("解码结果: %s\n", (char*)decoded);
        printf("解码长度: %zu 字节\n", len);
    } else {
        printf("解码失败: %s\n", base64_get_error());
    }
}

/* 二进制数据编码示例 */
void example_binary_data(void) {
    print_separator("二进制数据编码示例");
    
    unsigned char binary_data[] = {0x00, 0x01, 0x02, 0x03, 0xFF, 0xFE, 0xFD, 0xFC};
    char encoded[256];
    
    printf("原始二进制数据:\n");
    print_hex(binary_data, sizeof(binary_data));
    
    size_t len = base64_encode(binary_data, sizeof(binary_data), encoded, sizeof(encoded));
    
    printf("编码结果: %s\n", encoded);
    printf("编码长度: %zu 字符\n", len);
    
    /* 解码验证 */
    unsigned char decoded[256];
    size_t dec_len = base64_decode(encoded, len, decoded, sizeof(decoded));
    
    printf("解码验证: %s\n", 
           (dec_len == sizeof(binary_data) && memcmp(decoded, binary_data, dec_len) == 0)
           ? "成功" : "失败");
}

/* Base64URL 示例 */
void example_base64url(void) {
    print_separator("Base64URL 示例（URL 安全编码）");
    
    const char* data = "\xFB\xFF\xBF";  /* 会产生 +/ 字符的数据 */
    char encoded[256];
    
    /* 标准 Base64 */
    size_t std_len = base64_encode((const unsigned char*)data, 3, encoded, sizeof(encoded));
    printf("标准 Base64: %s\n", encoded);
    
    /* Base64URL（无填充） */
    size_t url_len = base64url_encode((const unsigned char*)data, 3, encoded, sizeof(encoded));
    printf("Base64URL:   %s\n", encoded);
    
    /* Base64URL（带填充） */
    url_len = base64url_encode_with_padding((const unsigned char*)data, 3, encoded, sizeof(encoded));
    printf("Base64URL (填充): %s\n", encoded);
    
    printf("\n注意: 标准 Base64 中的 + 和 / 被替换为 - 和 _\n");
}

/* 字符串便捷函数示例 */
void example_string_functions(void) {
    print_separator("字符串便捷函数示例");
    
    /* 编码字符串 */
    char* encoded = base64_encode_string("OpenClaw AllToolkit");
    if (encoded != NULL) {
        printf("编码字符串: %s\n", encoded);
        free(encoded);
    }
    
    /* 解码字符串 */
    size_t out_len;
    unsigned char* decoded = base64_decode_string("T3BlbkNsYXcgQWxsVG9vbGtpdA==", &out_len);
    if (decoded != NULL) {
        decoded[out_len] = '\0';
        printf("解码字符串: %s\n", (char*)decoded);
        free(decoded);
    }
    
    /* 十六进制转 Base64 */
    encoded = base64_encode_hex("48656c6c6f");
    if (encoded != NULL) {
        printf("十六进制 '48656c6c6f' -> Base64: %s\n", encoded);
        free(encoded);
    }
}

/* PEM 格式编码示例 */
void example_pem_style(void) {
    print_separator("PEM 格式编码示例（带换行）");
    
    /* 模拟一些二进制数据 */
    unsigned char data[64];
    for (int i = 0; i < 64; i++) {
        data[i] = (unsigned char)(i * 4);
    }
    
    char encoded[512];
    size_t len = base64_encode_with_lines(data, sizeof(data), encoded, sizeof(encoded), 64);
    
    printf("-----BEGIN DATA-----\n");
    printf("%s\n", encoded);
    printf("-----END DATA-----\n");
}

/* 验证示例 */
void example_validation(void) {
    print_separator("验证示例");
    
    const char* valid1 = "SGVsbG8gV29ybGQ=";
    const char* valid2 = "SGVsbG8gV29ybGQ";  /* 无填充 */
    const char* invalid = "SGVs*bG8=";
    
    printf("'%s' 有效: %s\n", valid1, base64_is_valid(valid1, strlen(valid1)) ? "是" : "否");
    printf("'%s' 有效: %s\n", valid2, base64_is_valid(valid2, strlen(valid2)) ? "是" : "否");
    printf("'%s' 有效: %s\n", invalid, base64_is_valid(invalid, strlen(invalid)) ? "是" : "否");
}

/* 长度计算示例 */
void example_length_calculation(void) {
    print_separator("长度计算示例");
    
    const char* inputs[] = {"", "M", "Ma", "Man", "Many"};
    
    printf("%-10s | %-15s | %-15s\n", "输入", "编码长度", "解码长度");
    printf("%-10s | %-15s | %-15s\n", "----------", "---------------", "---------------");
    
    for (int i = 0; i < 5; i++) {
        size_t in_len = strlen(inputs[i]);
        size_t enc_len = base64_encode_length(in_len);
        
        char encoded[256];
        base64_encode((const unsigned char*)inputs[i], in_len, encoded, sizeof(encoded));
        size_t dec_len = base64_decode_length(encoded, strlen(encoded));
        
        printf("%-10s | %-15zu | %-15zu\n", 
               inputs[i][0] ? inputs[i] : "(empty)", enc_len, dec_len);
    }
}

/* 文件编码示例 */
void example_file_encoding(void) {
    print_separator("文件编码示例");
    
    /* 创建测试文件 */
    const char* test_file = "/tmp/base64_test.txt";
    FILE* f = fopen(test_file, "wb");
    if (f) {
        fprintf(f, "This is test content for Base64 encoding.");
        fclose(f);
        
        /* 编码文件 */
        char encoded[256];
        size_t len = base64_encode_file(test_file, encoded, sizeof(encoded));
        
        if (len != (size_t)-1) {
            printf("文件编码成功: %s\n", encoded);
            
            /* 解码到新文件 */
            const char* output_file = "/tmp/base64_decoded.txt";
            if (base64_decode_to_file(encoded, len, output_file)) {
                printf("解码到文件成功: %s\n", output_file);
            }
        } else {
            printf("文件编码失败: %s\n", base64_get_error());
        }
        
        /* 清理测试文件 */
        remove(test_file);
        remove("/tmp/base64_decoded.txt");
    } else {
        printf("无法创建测试文件\n");
    }
}

/* 自定义字符集示例 */
void example_custom_charset(void) {
    print_separator("自定义字符集示例");
    
    /* 使用文件名安全字符集 */
    const char* filename_safe = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
    
    const char* data = "Custom!";
    char encoded[256];
    unsigned char decoded[256];
    
    /* 编码 */
    size_t enc_len = base64_encode_custom((const unsigned char*)data, strlen(data),
                                           encoded, sizeof(encoded), filename_safe, '\0');
    printf("自定义字符集编码: %s\n", encoded);
    
    /* 解码 */
    size_t dec_len = base64_decode_custom(encoded, enc_len, decoded, sizeof(decoded),
                                           filename_safe, '\0');
    if (dec_len != (size_t)-1) {
        decoded[dec_len] = '\0';
        printf("解码结果: %s\n", (char*)decoded);
    }
}

/* 性能提示示例 */
void example_performance_tips(void) {
    print_separator("性能提示");
    
    printf("1. 预分配缓冲区：使用 base64_encode_length() 和 base64_decode_length()\n");
    printf("   预先计算所需缓冲区大小，避免动态分配\n\n");
    
    printf("2. 批量处理：对于大量数据，一次性处理比多次小块处理更高效\n\n");
    
    printf("3. URL 安全编码：使用 base64url_encode() 避免后续的字符串替换\n\n");
    
    printf("4. 验证优先：在解码前使用 base64_is_valid() 验证输入\n");
}

int main(void) {
    printf("\n╔════════════════════════════════════════════╗\n");
    printf("║     Base64 Utils - 使用示例                ║\n");
    printf("║     AllToolkit C Library                   ║\n");
    printf("╚════════════════════════════════════════════╝\n");
    
    /* 运行所有示例 */
    example_basic_encode();
    example_basic_decode();
    example_binary_data();
    example_base64url();
    example_string_functions();
    example_pem_style();
    example_validation();
    example_length_calculation();
    example_custom_charset();
    example_file_encoding();
    example_performance_tips();
    
    printf("\n========================================\n");
    printf("  示例演示完成！\n");
    printf("========================================\n\n");
    
    return 0;
}