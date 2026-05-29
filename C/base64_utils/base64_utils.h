/**
 * @file base64_utils.h
 * @brief Base64 编码/解码工具库
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-05-30
 * 
 * 提供 Base64 和 Base64URL 编码/解码功能
 * 支持：标准 Base64、Base64URL、自定义字符表
 * 零外部依赖
 */

#ifndef BASE64_UTILS_H
#define BASE64_UTILS_H

#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ==================== 常量定义 ==================== */

/* 标准 Base64 字符集 */
extern const char* BASE64_STANDARD_CHARS;
/* Base64URL 字符集 (URL 安全) */
extern const char* BASE64_URL_CHARS;

/* ==================== 编码函数 ==================== */

/**
 * @brief 计算编码后的缓冲区大小
 * @param input_len 输入数据长度
 * @return 编码后所需的缓冲区大小（包含空终止符）
 */
size_t base64_encode_length(size_t input_len);

/**
 * @brief 标准 Base64 编码
 * @param input 输入数据
 * @param input_len 输入数据长度
 * @param output 输出缓冲区（可以为 NULL，只计算长度）
 * @param output_size 输出缓冲区大小
 * @return 编码后的字符串长度（不含空终止符），失败返回 0
 */
size_t base64_encode(const unsigned char* input, size_t input_len,
                     char* output, size_t output_size);

/**
 * @brief 标准 Base64 编码（带换行，适合 PEM 格式）
 * @param input 输入数据
 * @param input_len 输入数据长度
 * @param output 输出缓冲区
 * @param output_size 输出缓冲区大小
 * @param line_width 每行宽度（通常为 64 或 76）
 * @return 编码后的字符串长度
 */
size_t base64_encode_with_lines(const unsigned char* input, size_t input_len,
                                 char* output, size_t output_size,
                                 size_t line_width);

/**
 * @brief Base64URL 编码（URL 安全，无填充）
 * @param input 输入数据
 * @param input_len 输入数据长度
 * @param output 输出缓冲区
 * @param output_size 输出缓冲区大小
 * @return 编码后的字符串长度
 */
size_t base64url_encode(const unsigned char* input, size_t input_len,
                         char* output, size_t output_size);

/**
 * @brief Base64URL 编码（带填充）
 * @param input 输入数据
 * @param input_len 输入数据长度
 * @param output 输出缓冲区
 * @param output_size 输出缓冲区大小
 * @return 编码后的字符串长度
 */
size_t base64url_encode_with_padding(const unsigned char* input, size_t input_len,
                                      char* output, size_t output_size);

/**
 * @brief 自定义字符集 Base64 编码
 * @param input 输入数据
 * @param input_len 输入数据长度
 * @param output 输出缓冲区
 * @param output_size 输出缓冲区大小
 * @param chars 自定义字符集（64 个字符 + 填充字符）
 * @param pad_char 填充字符（通常为 '='，传入 '\0' 表示无填充）
 * @return 编码后的字符串长度
 */
size_t base64_encode_custom(const unsigned char* input, size_t input_len,
                             char* output, size_t output_size,
                             const char* chars, char pad_char);

/* ==================== 解码函数 ==================== */

/**
 * @brief 计算解码后的缓冲区大小
 * @param input 输入字符串
 * @param input_len 输入字符串长度
 * @return 解码后所需的最大缓冲区大小
 */
size_t base64_decode_length(const char* input, size_t input_len);

/**
 * @brief 标准 Base64 解码
 * @param input 输入字符串
 * @param input_len 输入字符串长度
 * @param output 输出缓冲区（可以为 NULL，只计算长度）
 * @param output_size 输出缓冲区大小
 * @return 解码后的数据长度，失败返回 (size_t)-1
 */
size_t base64_decode(const char* input, size_t input_len,
                     unsigned char* output, size_t output_size);

/**
 * @brief Base64URL 解码
 * @param input 输入字符串
 * @param input_len 输入字符串长度
 * @param output 输出缓冲区
 * @param output_size 输出缓冲区大小
 * @return 解码后的数据长度
 */
size_t base64url_decode(const char* input, size_t input_len,
                        unsigned char* output, size_t output_size);

/**
 * @brief 自定义字符集 Base64 解码
 * @param input 输入字符串
 * @param input_len 输入字符串长度
 * @param output 输出缓冲区
 * @param output_size 输出缓冲区大小
 * @param chars 自定义字符集
 * @param pad_char 填充字符
 * @return 解码后的数据长度
 */
size_t base64_decode_custom(const char* input, size_t input_len,
                             unsigned char* output, size_t output_size,
                             const char* chars, char pad_char);

/* ==================== 验证函数 ==================== */

/**
 * @brief 验证 Base64 字符串是否有效
 * @param input 输入字符串
 * @param input_len 输入字符串长度
 * @return true 如果有效，false 如果无效
 */
bool base64_is_valid(const char* input, size_t input_len);

/**
 * @brief 验证 Base64URL 字符串是否有效
 * @param input 输入字符串
 * @param input_len 输入字符串长度
 * @return true 如果有效
 */
bool base64url_is_valid(const char* input, size_t input_len);

/* ==================== 字符串便捷函数 ==================== */

/**
 * @brief 编码字符串到 Base64
 * @param str 输入字符串（以空终止）
 * @return 新分配的编码字符串，需调用者释放。失败返回 NULL。
 */
char* base64_encode_string(const char* str);

/**
 * @brief 解码 Base64 字符串
 * @param input Base64 编码的字符串
 * @param output_len 输出参数，解码后的长度
 * @return 新分配的解码数据缓冲区，需调用者释放。失败返回 NULL。
 */
unsigned char* base64_decode_string(const char* input, size_t* output_len);

/**
 * @brief 编码十六进制字符串到 Base64
 * @param hex 十六进制字符串
 * @return 新分配的 Base64 字符串。失败返回 NULL。
 */
char* base64_encode_hex(const char* hex);

/* ==================== 文件操作函数 ==================== */

/**
 * @brief 编码文件内容到 Base64
 * @param filepath 文件路径
 * @param output 输出缓冲区
 * @param output_size 输出缓冲区大小
 * @return 编码后的长度，失败返回 (size_t)-1
 */
size_t base64_encode_file(const char* filepath, char* output, size_t output_size);

/**
 * @brief 解码 Base64 到文件
 * @param input Base64 字符串
 * @param input_len 输入长度
 * @param filepath 输出文件路径
 * @return 成功返回 true
 */
bool base64_decode_to_file(const char* input, size_t input_len, const char* filepath);

/* ==================== 辅助函数 ==================== */

/**
 * @brief 计算 Base64 字符串去除空白后的长度
 * @param input 输入字符串
 * @param input_len 输入长度
 * @return 去除空白后的长度
 */
size_t base64_strip_whitespace_length(const char* input, size_t input_len);

/**
 * @brief 去除 Base64 字符串中的空白字符
 * @param input 输入字符串
 * @param input_len 输入长度
 * @param output 输出缓冲区
 * @param output_size 输出缓冲区大小
 * @return 输出长度
 */
size_t base64_strip_whitespace(const char* input, size_t input_len,
                                char* output, size_t output_size);

/**
 * @brief 获取 Base64 编码的错误描述
 * @return 错误描述字符串
 */
const char* base64_get_error(void);

#ifdef __cplusplus
}
#endif

#endif /* BASE64_UTILS_H */