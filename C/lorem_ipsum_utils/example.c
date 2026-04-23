/**
 * @file example.c
 * @brief Lorem Ipsum 工具库使用示例
 * @author AllToolkit
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lorem_ipsum_utils.h"

/* 动态分配足够大的缓冲区 */
static char* create_buffer(size_t size) {
    char* buffer = (char*)malloc(size);
    if (buffer) buffer[0] = '\0';
    return buffer;
}

int main(void) {
    printf("====================================\n");
    printf("  Lorem Ipsum 工具库示例\n");
    printf("====================================\n\n");
    
    /* 示例 1：生成单个单词 */
    printf("【示例 1】生成单个随机单词\n");
    printf("------------------------------------\n");
    char word[50];
    lorem_single_word(word, sizeof(word));
    printf("随机单词: %s\n\n", word);
    
    /* 示例 2：生成指定数量的单词 */
    printf("【示例 2】生成 15 个单词\n");
    printf("------------------------------------\n");
    char* words = create_buffer(200);
    lorem_words(15, words, 200);
    printf("%s\n\n", words);
    free(words);
    
    /* 示例 3：生成句子 */
    printf("【示例 3】生成 3 个句子\n");
    printf("------------------------------------\n");
    char* sentences = create_buffer(500);
    lorem_sentences(3, sentences, 500);
    printf("%s\n\n", sentences);
    free(sentences);
    
    /* 示例 4：生成自定义句子（控制单词数量）*/
    printf("【示例 4】生成 2 个句子，每句 4-6 个单词\n");
    printf("------------------------------------\n");
    char* custom_sentences = create_buffer(300);
    lorem_sentences_custom(2, 4, 6, custom_sentences, 300);
    printf("%s\n\n", custom_sentences);
    free(custom_sentences);
    
    /* 示例 5：生成段落 */
    printf("【示例 5】生成 2 个段落\n");
    printf("------------------------------------\n");
    char* paragraphs = create_buffer(2000);
    lorem_paragraphs(2, paragraphs, 2000);
    printf("%s\n\n", paragraphs);
    free(paragraphs);
    
    /* 示例 6：生成自定义段落 */
    printf("【示例 6】生成 1 个段落，2-3 句，每句 8-12 词\n");
    printf("------------------------------------\n");
    char* custom_para = create_buffer(1000);
    lorem_paragraphs_custom(1, 2, 3, 8, 12, custom_para, 1000);
    printf("%s\n\n", custom_para);
    free(custom_para);
    
    /* 示例 7：经典开头段落 */
    printf("【示例 7】经典 Lorem Ipsum 开头段落\n");
    printf("------------------------------------\n");
    char* classic = create_buffer(1000);
    lorem_classic_start(classic, 1000);
    printf("%s\n\n", classic);
    free(classic);
    
    /* 示例 8：可重复生成（使用固定种子）*/
    printf("【示例 8】可重复生成（固定种子 42）\n");
    printf("------------------------------------\n");
    lorem_set_seed(42);
    char* reproducible1 = create_buffer(200);
    lorem_words(10, reproducible1, 200);
    printf("第一次: %s\n", reproducible1);
    
    lorem_set_seed(42);
    char* reproducible2 = create_buffer(200);
    lorem_words(10, reproducible2, 200);
    printf("第二次: %s\n", reproducible2);
    
    if (strcmp(reproducible1, reproducible2) == 0) {
        printf("✓ 两次生成结果完全相同！\n");
    }
    printf("\n");
    
    free(reproducible1);
    free(reproducible2);
    
    /* 示例 9：估算缓冲区大小 */
    printf("【示例 9】缓冲区大小估算\n");
    printf("------------------------------------\n");
    printf("50 个单词建议缓冲区: %zu 字节\n", lorem_estimate_buffer('w', 50));
    printf("5 个句子建议缓冲区: %zu 字节\n", lorem_estimate_buffer('s', 5));
    printf("3 个段落建议缓冲区: %zu 字节\n", lorem_estimate_buffer('p', 3));
    printf("\n");
    
    /* 示例 10：生成占位文本 */
    printf("【示例 10】生成文章占位文本\n");
    printf("------------------------------------\n");
    printf("标题: 示例文章标题\n\n");
    
    lorem_reset_seed();  /* 重置为随机状态 */
    
    char* intro = create_buffer(500);
    lorem_sentences(2, intro, 500);
    printf("【引言】\n%s\n\n", intro);
    free(intro);
    
    char* body = create_buffer(2000);
    lorem_paragraphs_custom(2, 3, 5, 10, 15, body, 2000);
    printf("【正文】\n%s\n\n", body);
    free(body);
    
    char* conclusion = create_buffer(500);
    lorem_sentences(2, conclusion, 500);
    printf("【结语】\n%s\n", conclusion);
    free(conclusion);
    
    printf("\n====================================\n");
    printf("  示例运行完成\n");
    printf("====================================\n");
    
    return 0;
}