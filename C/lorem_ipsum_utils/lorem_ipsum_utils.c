/**
 * @file lorem_ipsum_utils.c
 * @brief C 语言 Lorem Ipsum 文本生成工具库实现
 */

#include "lorem_ipsum_utils.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>

/* Lorem Ipsum 单词库（经典拉丁词汇）*/
static const char* LOREM_WORDS[] = {
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
    "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
    "exercitation", "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
    "consequat", "duis", "aute", "irure", "in", "reprehenderit", "voluptate",
    "velit", "esse", "cillum", "fugiat", "nulla", "pariatur", "excepteur", "sint",
    "occaecat", "cupidatat", "non", "proident", "sunt", "culpa", "qui", "officia",
    "deserunt", "mollit", "anim", "id", "est", "laborum", "perspiciatis", "unde",
    "omnis", "iste", "natus", "error", "voluptatem", "accusantium", "doloremque",
    "laudantium", "totam", "rem", "aperiam", "eaque", "ipsa", "quae", "ab", "illo",
    "inventore", "veritatis", "quasi", "architecto", "beatae", "vitae", "dicta",
    "explicabo", "nemo", "ipsam", "quia", "voluptas", "aspernatur", "aut", "odit",
    "fugit", "consequuntur", "magni", "dolores", "eos", "ratione", "sequi",
    "nesciunt", "neque", "porro", "quisquam", "dolorem", "adipisci", "numquam",
    "eius", "modi", "tempora", "magnam", "quaerat", "adipisci", "velit", "dolorem",
    "adipisci", "velit", "esse", "quam", "nihil", "molestiae", "consequatur",
    "vel", "illum", "fugiat", "voluptas", "nulla", "pariatur", "at", "vero",
    "accusamus", "iusto", "dignissimos", "ducimus", "blanditiis", "praesentium",
    "voluptatum", "deleniti", "atque", "corrupti", "quos", "molestias", "excepturi",
    "sint", "obcaecati", "cupiditate", "provident", "similique", "mollitia",
    "animi", "laborum", "dolor", "fuga", "harum", "quid", "rerum", "facilis",
    "expedita", "distinctio", "nam", "libero", "tempore", "soluta", "nobis",
    "eligendi", "optio", "cumque", "nihil", "impedit", "quo", "minus", "maxime",
    "placeat", "facere", "possimus", "omnis", "voluptas", "assumenda", "omnis",
    "dolor", "repellendus", "temporibus", "autem", "quibusdam", "officiis",
    "debitis", "aut", "rerum", "necessitatibus", "saepe", "eveniet", "et",
    "voluptates", "repudiandae", "recusandae", "itaque", "earum", "rerum",
    "hic", "tenetur", "sapiente", "delectus", "reiciendis", "voluptatibus",
    "maiores", "alias", "consequatur", "aut", "perferendis", "doloribus", "asperiores",
    "repellat"
};

#define WORD_COUNT (sizeof(LOREM_WORDS) / sizeof(LOREM_WORDS[0]))

/* 经典开头段落 */
static const char* CLASSIC_START = 
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, "
    "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo "
    "consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse "
    "cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat "
    "non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";

/* 随机状态 */
static unsigned int g_seed = 0;
static bool g_seed_initialized = false;

/* 内部随机函数 */
static unsigned int lorem_rand(void) {
    if (!g_seed_initialized) {
        g_seed = (unsigned int)time(NULL);
        g_seed_initialized = true;
    }
    /* 简单的线性同余生成器 */
    g_seed = g_seed * 1103515245 + 12345;
    return (g_seed >> 16) & 0x7FFF;
}

/* 范围随机 */
static size_t lorem_rand_range(size_t min_val, size_t max_val) {
    if (min_val >= max_val) return min_val;
    return min_val + (lorem_rand() % (max_val - min_val + 1));
}

/* 首字母大写 */
static void capitalize_first(char* word) {
    if (word && *word) {
        if (*word >= 'a' && *word <= 'z') {
            *word = *word - 'a' + 'A';
        }
    }
}

/* ==================== 随机种子控制 ==================== */

void lorem_set_seed(unsigned int seed) {
    g_seed = seed;
    g_seed_initialized = true;
}

void lorem_reset_seed(void) {
    g_seed_initialized = false;
}

/* ==================== 基础生成函数 ==================== */

size_t lorem_single_word(char* buffer, size_t buffer_size) {
    if (!buffer || buffer_size == 0) return 0;
    
    const char* word = LOREM_WORDS[lorem_rand() % WORD_COUNT];
    size_t len = strlen(word);
    
    if (len >= buffer_size) {
        len = buffer_size - 1;
    }
    
    memcpy(buffer, word, len);
    buffer[len] = '\0';
    
    return len;
}

size_t lorem_words(size_t count, char* buffer, size_t buffer_size) {
    if (!buffer || buffer_size == 0 || count == 0) return 0;
    
    size_t pos = 0;
    
    for (size_t i = 0; i < count && pos < buffer_size - 1; i++) {
        const char* word = LOREM_WORDS[lorem_rand() % WORD_COUNT];
        size_t word_len = strlen(word);
        
        /* 添加空格（第一个单词除外）*/
        if (i > 0) {
            if (pos + 1 >= buffer_size) break;
            buffer[pos++] = ' ';
        }
        
        /* 检查缓冲区剩余空间 */
        if (pos + word_len >= buffer_size) {
            word_len = buffer_size - pos - 1;
            if (word_len == 0) break;
        }
        
        memcpy(buffer + pos, word, word_len);
        pos += word_len;
    }
    
    buffer[pos] = '\0';
    return pos;
}

size_t lorem_sentences(size_t count, char* buffer, size_t buffer_size) {
    return lorem_sentences_custom(count, 5, 15, buffer, buffer_size);
}

size_t lorem_sentences_custom(size_t count, size_t min_words, size_t max_words,
                              char* buffer, size_t buffer_size) {
    if (!buffer || buffer_size == 0 || count == 0) return 0;
    
    size_t pos = 0;
    
    for (size_t i = 0; i < count && pos < buffer_size - 1; i++) {
        /* 确定本句单词数 */
        size_t word_count = lorem_rand_range(min_words, max_words);
        
        for (size_t j = 0; j < word_count && pos < buffer_size - 2; j++) {
            const char* word = LOREM_WORDS[lorem_rand() % WORD_COUNT];
            size_t word_len = strlen(word);
            
            /* 添加空格 */
            if (j > 0) {
                if (pos + 1 >= buffer_size) break;
                buffer[pos++] = ' ';
            }
            
            /* 检查空间 */
            if (pos + word_len >= buffer_size - 1) {
                word_len = buffer_size - pos - 2;
                if (word_len == 0) break;
            }
            
            /* 复制单词 */
            memcpy(buffer + pos, word, word_len);
            
            /* 首句首字母大写 */
            if (j == 0) {
                capitalize_first(buffer + pos);
            }
            
            pos += word_len;
        }
        
        /* 添加句号 */
        if (pos < buffer_size - 1) {
            buffer[pos++] = '.';
        }
        
        /* 如果不是最后一句，添加空格 */
        if (i < count - 1 && pos < buffer_size - 1) {
            buffer[pos++] = ' ';
        }
    }
    
    buffer[pos] = '\0';
    return pos;
}

size_t lorem_paragraphs(size_t count, char* buffer, size_t buffer_size) {
    return lorem_paragraphs_custom(count, 3, 7, 5, 15, buffer, buffer_size);
}

size_t lorem_paragraphs_custom(size_t count,
                                size_t min_sentences, size_t max_sentences,
                                size_t min_words, size_t max_words,
                                char* buffer, size_t buffer_size) {
    if (!buffer || buffer_size == 0 || count == 0) return 0;
    
    size_t pos = 0;
    
    for (size_t i = 0; i < count && pos < buffer_size - 1; i++) {
        /* 确定本段句子数 */
        size_t sentence_count = lorem_rand_range(min_sentences, max_sentences);
        
        /* 生成句子 */
        size_t written = lorem_sentences_custom(sentence_count, min_words, max_words,
                                                 buffer + pos, buffer_size - pos);
        if (written == 0) break;
        pos += written;
        
        /* 如果不是最后一段，添加两个换行 */
        if (i < count - 1 && pos + 2 < buffer_size) {
            buffer[pos++] = '\n';
            buffer[pos++] = '\n';
        }
    }
    
    buffer[pos] = '\0';
    return pos;
}

size_t lorem_classic_start(char* buffer, size_t buffer_size) {
    if (!buffer || buffer_size == 0) return 0;
    
    size_t len = strlen(CLASSIC_START);
    if (len >= buffer_size) {
        len = buffer_size - 1;
    }
    
    memcpy(buffer, CLASSIC_START, len);
    buffer[len] = '\0';
    
    return len;
}

size_t lorem_estimate_buffer(char type, size_t count) {
    /* 平均单词长度：约8字符
       平均每句单词数：约10个
       平均每段句子数：约5句
       加上标点和空格的开销
    */
    switch (type) {
        case 'w':
        case 'W':
            return count * 10 + 1;  /* 单词 + 空格 + 终止符 */
        case 's':
        case 'S':
            return count * 110 + 1; /* 句子(10词×8+2) × count */
        case 'p':
        case 'P':
            return count * 600 + 1; /* 段落(5句×110+2) × count */
        default:
            return 0;
    }
}