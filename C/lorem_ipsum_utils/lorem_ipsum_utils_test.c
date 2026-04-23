/**
 * @file lorem_ipsum_utils_test.c
 * @brief Lorem Ipsum 工具库测试
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "lorem_ipsum_utils.h"

/* 测试计数器 */
static int tests_passed = 0;
static int tests_failed = 0;

#define TEST(name) static void test_##name(void)
#define RUN_TEST(name) do { \
    printf("  Running test: %s... ", #name); \
    test_##name(); \
    printf("PASSED\n"); \
    tests_passed++; \
} while(0)

#define ASSERT_TRUE(expr) do { \
    if (!(expr)) { \
        printf("FAILED at line %d: %s\n", __LINE__, #expr); \
        tests_failed++; \
        return; \
    } \
} while(0)

#define ASSERT_FALSE(expr) ASSERT_TRUE(!(expr))
#define ASSERT_EQ(a, b) ASSERT_TRUE((a) == (b))
#define ASSERT_NE(a, b) ASSERT_TRUE((a) != (b))
#define ASSERT_STREQ(a, b) ASSERT_TRUE(strcmp((a), (b)) == 0)
#define ASSERT_GT(a, b) ASSERT_TRUE((a) > (b))
#define ASSERT_GTE(a, b) ASSERT_TRUE((a) >= (b))
#define ASSERT_LT(a, b) ASSERT_TRUE((a) < (b))
#define ASSERT_LTE(a, b) ASSERT_TRUE((a) <= (b))

/* ==================== 测试用例 ==================== */

TEST(single_word) {
    char buffer[100];
    size_t len = lorem_single_word(buffer, sizeof(buffer));
    
    ASSERT_TRUE(len > 0);
    ASSERT_TRUE(strlen(buffer) == len);
    ASSERT_TRUE(buffer[len] == '\0');
    
    /* 验证单词都是小写字母 */
    for (size_t i = 0; i < len; i++) {
        ASSERT_TRUE(buffer[i] >= 'a' && buffer[i] <= 'z');
    }
}

TEST(single_word_small_buffer) {
    char buffer[5];
    size_t len = lorem_single_word(buffer, sizeof(buffer));
    
    /* 即使缓冲区小，也应该正确处理 */
    ASSERT_TRUE(len < sizeof(buffer));
    ASSERT_TRUE(buffer[len] == '\0');
}

TEST(words_basic) {
    char buffer[1000];
    size_t len = lorem_words(10, buffer, sizeof(buffer));
    
    ASSERT_TRUE(len > 0);
    ASSERT_TRUE(strlen(buffer) == len);
    
    /* 计算单词数（空格分隔）*/
    int word_count = 1;
    for (size_t i = 0; i < len; i++) {
        if (buffer[i] == ' ') word_count++;
    }
    ASSERT_EQ(word_count, 10);
}

TEST(words_zero_count) {
    char buffer[100];
    size_t len = lorem_words(0, buffer, sizeof(buffer));
    ASSERT_EQ(len, 0);
}

TEST(words_null_buffer) {
    size_t len = lorem_words(10, NULL, 100);
    ASSERT_EQ(len, 0);
}

TEST(words_small_buffer) {
    char buffer[20];
    size_t len = lorem_words(100, buffer, sizeof(buffer));
    
    /* 应该被截断，但不会溢出 */
    ASSERT_TRUE(len < sizeof(buffer));
    ASSERT_TRUE(buffer[len] == '\0');
}

TEST(sentences_basic) {
    char buffer[2000];
    size_t len = lorem_sentences(5, buffer, sizeof(buffer));
    
    ASSERT_TRUE(len > 0);
    ASSERT_TRUE(strlen(buffer) == len);
    
    /* 统计句号数量 */
    int period_count = 0;
    for (size_t i = 0; i < len; i++) {
        if (buffer[i] == '.') period_count++;
    }
    ASSERT_EQ(period_count, 5);
    
    /* 首字母应该大写 */
    ASSERT_TRUE(buffer[0] >= 'A' && buffer[0] <= 'Z');
}

TEST(sentences_custom_word_count) {
    char buffer[2000];
    size_t len = lorem_sentences_custom(3, 8, 12, buffer, sizeof(buffer));
    
    ASSERT_TRUE(len > 0);
    
    /* 验证句子结构 */
    int period_count = 0;
    for (size_t i = 0; i < len; i++) {
        if (buffer[i] == '.') period_count++;
    }
    ASSERT_EQ(period_count, 3);
}

TEST(paragraphs_basic) {
    char buffer[5000];
    size_t len = lorem_paragraphs(3, buffer, sizeof(buffer));
    
    ASSERT_TRUE(len > 0);
    ASSERT_TRUE(strlen(buffer) == len);
    
    /* 统计双换行数量（段落分隔）*/
    int para_sep_count = 0;
    for (size_t i = 0; i < len - 1; i++) {
        if (buffer[i] == '\n' && buffer[i+1] == '\n') {
            para_sep_count++;
        }
    }
    /* 3个段落有2个分隔 */
    ASSERT_EQ(para_sep_count, 2);
}

TEST(paragraphs_custom) {
    char buffer[5000];
    size_t len = lorem_paragraphs_custom(2, 2, 4, 3, 6, buffer, sizeof(buffer));
    
    ASSERT_TRUE(len > 0);
    
    /* 统计段落分隔 */
    int para_sep_count = 0;
    for (size_t i = 0; i < len - 1; i++) {
        if (buffer[i] == '\n' && buffer[i+1] == '\n') {
            para_sep_count++;
        }
    }
    ASSERT_EQ(para_sep_count, 1);
}

TEST(seed_reproducibility) {
    char buffer1[1000];
    char buffer2[1000];
    
    /* 设置相同的种子 */
    lorem_set_seed(12345);
    size_t len1 = lorem_words(20, buffer1, sizeof(buffer1));
    
    lorem_set_seed(12345);
    size_t len2 = lorem_words(20, buffer2, sizeof(buffer2));
    
    /* 应该生成完全相同的文本 */
    ASSERT_EQ(len1, len2);
    ASSERT_STREQ(buffer1, buffer2);
}

TEST(seed_different) {
    char buffer1[1000];
    char buffer2[1000];
    
    /* 不同的种子 */
    lorem_set_seed(11111);
    size_t len1 = lorem_words(20, buffer1, sizeof(buffer1));
    
    lorem_set_seed(22222);
    size_t len2 = lorem_words(20, buffer2, sizeof(buffer2));
    
    /* 长度可能相同，但内容应该不同 */
    /* 注意：有极小概率相同，但20个词几乎不可能 */
    int differences = 0;
    size_t min_len = len1 < len2 ? len1 : len2;
    for (size_t i = 0; i < min_len; i++) {
        if (buffer1[i] != buffer2[i]) differences++;
    }
    ASSERT_TRUE(differences > 0);
}

TEST(classic_start) {
    char buffer[1000];
    size_t len = lorem_classic_start(buffer, sizeof(buffer));
    
    ASSERT_TRUE(len > 0);
    ASSERT_TRUE(strstr(buffer, "Lorem ipsum dolor sit amet") != NULL);
    ASSERT_TRUE(strstr(buffer, "consectetur adipiscing elit") != NULL);
    ASSERT_TRUE(strstr(buffer, "dolor") != NULL);
}

TEST(classic_start_small_buffer) {
    char buffer[50];
    size_t len = lorem_classic_start(buffer, sizeof(buffer));
    
    ASSERT_TRUE(len < sizeof(buffer));
    ASSERT_TRUE(buffer[len] == '\0');
}

TEST(estimate_buffer) {
    /* 验证缓冲区估算 */
    size_t words_est = lorem_estimate_buffer('w', 100);
    size_t sentences_est = lorem_estimate_buffer('s', 10);
    size_t paragraphs_est = lorem_estimate_buffer('p', 5);
    
    ASSERT_GT(words_est, 100);
    ASSERT_GT(sentences_est, 100);
    ASSERT_GT(paragraphs_est, 100);
    
    /* 验证合理比例 */
    ASSERT_GT(sentences_est, words_est / 2);
    ASSERT_GT(paragraphs_est, sentences_est / 2);
}

TEST(estimate_buffer_invalid_type) {
    size_t est = lorem_estimate_buffer('x', 10);
    ASSERT_EQ(est, 0);
}

TEST(reset_seed) {
    /* 重置种子 */
    lorem_reset_seed();
    
    char buffer[100];
    size_t len = lorem_words(5, buffer, sizeof(buffer));
    ASSERT_TRUE(len > 0);
}

/* ==================== 主测试入口 ==================== */

int main(void) {
    printf("====================================\n");
    printf("  Lorem Ipsum Utils Test Suite\n");
    printf("====================================\n\n");
    
    printf("Running tests...\n\n");
    
    /* 单词测试 */
    RUN_TEST(single_word);
    RUN_TEST(single_word_small_buffer);
    RUN_TEST(words_basic);
    RUN_TEST(words_zero_count);
    RUN_TEST(words_null_buffer);
    RUN_TEST(words_small_buffer);
    
    /* 句子测试 */
    RUN_TEST(sentences_basic);
    RUN_TEST(sentences_custom_word_count);
    
    /* 段落测试 */
    RUN_TEST(paragraphs_basic);
    RUN_TEST(paragraphs_custom);
    
    /* 种子测试 */
    RUN_TEST(seed_reproducibility);
    RUN_TEST(seed_different);
    RUN_TEST(reset_seed);
    
    /* 经典段落测试 */
    RUN_TEST(classic_start);
    RUN_TEST(classic_start_small_buffer);
    
    /* 缓冲区估算测试 */
    RUN_TEST(estimate_buffer);
    RUN_TEST(estimate_buffer_invalid_type);
    
    printf("\n====================================\n");
    printf("  Results: %d passed, %d failed\n", tests_passed, tests_failed);
    printf("====================================\n");
    
    return tests_failed > 0 ? 1 : 0;
}