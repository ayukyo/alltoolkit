/**
 * @file lorem_ipsum_utils.h
 * @brief C 语言 Lorem Ipsum 文本生成工具库
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-23
 */

#ifndef LOREM_IPSUM_UTILS_H
#define LOREM_IPSUM_UTILS_H

#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ==================== 基础生成函数 ==================== */

/**
 * @brief 生成指定数量的单词
 * @param count 单词数量
 * @param buffer 输出缓冲区
 * @param buffer_size 缓冲区大小
 * @return 实际写入的字符数（不含终止符），失败返回0
 */
size_t lorem_words(size_t count, char* buffer, size_t buffer_size);

/**
 * @brief 生成指定数量的句子
 * @param count 句子数量
 * @param buffer 输出缓冲区
 * @param buffer_size 缓冲区大小
 * @return 实际写入的字符数（不含终止符），失败返回0
 */
size_t lorem_sentences(size_t count, char* buffer, size_t buffer_size);

/**
 * @brief 生成指定数量的段落
 * @param count 段落数量
 * @param buffer 输出缓冲区
 * @param buffer_size 缓冲区大小
 * @return 实际写入的字符数（不含终止符），失败返回0
 */
size_t lorem_paragraphs(size_t count, char* buffer, size_t buffer_size);

/* ==================== 自定义生成函数 ==================== */

/**
 * @brief 生成自定义句子（指定每句单词数范围）
 * @param count 句子数量
 * @param min_words 每句最小单词数
 * @param max_words 每句最大单词数
 * @param buffer 输出缓冲区
 * @param buffer_size 缓冲区大小
 * @return 实际写入的字符数
 */
size_t lorem_sentences_custom(size_t count, size_t min_words, size_t max_words,
                              char* buffer, size_t buffer_size);

/**
 * @brief 生成自定义段落（指定每段句子数范围）
 * @param count 段落数量
 * @param min_sentences 每段最小句子数
 * @param max_sentences 每段最大句子数
 * @param min_words 每句最小单词数
 * @param max_words 每句最大单词数
 * @param buffer 输出缓冲区
 * @param buffer_size 缓冲区大小
 * @return 实际写入的字符数
 */
size_t lorem_paragraphs_custom(size_t count,
                                size_t min_sentences, size_t max_sentences,
                                size_t min_words, size_t max_words,
                                char* buffer, size_t buffer_size);

/* ==================== 随机种子控制 ==================== */

/**
 * @brief 设置随机种子（用于可重复生成）
 * @param seed 随机种子值
 */
void lorem_set_seed(unsigned int seed);

/**
 * @brief 重置为默认随机状态
 */
void lorem_reset_seed(void);

/* ==================== 工具函数 ==================== */

/**
 * @brief 获取单个随机单词
 * @param buffer 输出缓冲区
 * @param buffer_size 缓冲区大小
 * @return 实际写入的字符数
 */
size_t lorem_single_word(char* buffer, size_t buffer_size);

/**
 * @brief 获取 Lorem Ipsum 起始段落（经典开头）
 * @param buffer 输出缓冲区
 * @param buffer_size 缓冲区大小
 * @return 实际写入的字符数
 */
size_t lorem_classic_start(char* buffer, size_t buffer_size);

/**
 * @brief 计算生成指定内容所需的缓冲区大小
 * @param type 类型：'w'=单词, 's'=句子, 'p'=段落
 * @param count 数量
 * @return 建议的缓冲区大小
 */
size_t lorem_estimate_buffer(char type, size_t count);

#ifdef __cplusplus
}
#endif

#endif /* LOREM_IPSUM_UTILS_H */