/**
 * @file word_frequency.c
 * @brief Word frequency counter using Trie
 */

#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include "trie.h"

/* Structure to hold word frequency */
typedef struct {
    char word[256];
    size_t count;
} WordFreq;

/* Simple tokenizer - extract words from text */
void process_text(Trie *word_trie, const char *text) {
    (void)word_trie; /* Reserved for future frequency tracking */
    char word[256];
    size_t word_len = 0;
    
    for (size_t i = 0; text[i] != '\0'; i++) {
        if (isalpha(text[i]) || text[i] == '\'') {
            if (word_len < sizeof(word) - 1) {
                word[word_len++] = tolower(text[i]);
            }
        } else if (word_len > 0) {
            word[word_len] = '\0';
            
            /* Add to word set */
            trie_insert(word_trie, word);
            
            word_len = 0;
        }
    }
    
    /* Handle last word */
    if (word_len > 0) {
        word[word_len] = '\0';
        trie_insert(word_trie, word);
    }
}

int main(void) {
    printf("=== Trie Word Frequency Example ===\n\n");
    
    Trie *trie = trie_create();
    
    /* Sample text */
    const char *text = 
        "The quick brown fox jumps over the lazy dog. "
        "The dog was not lazy, but the fox was quick. "
        "Quick thinking and quick action saved the day. "
        "The lazy dog slept while the fox ran around.";
    
    printf("Sample text:\n%s\n\n", text);
    
    /* Extract and insert words */
    char word[256];
    size_t word_len = 0;
    
    for (size_t i = 0; text[i] != '\0'; i++) {
        char c = text[i];
        if (isalpha(c)) {
            if (word_len < sizeof(word) - 1) {
                word[word_len++] = tolower(c);
            }
        } else if (word_len > 0) {
            word[word_len] = '\0';
            trie_insert(trie, word);
            word_len = 0;
        }
    }
    
    if (word_len > 0) {
        word[word_len] = '\0';
        trie_insert(trie, word);
    }
    
    /* Get all unique words */
    printf("--- Word Analysis ---\n\n");
    printf("Unique words: %zu\n", trie_size(trie));
    printf("Memory used: %zu bytes\n\n", trie_memory_usage(trie));
    
    /* List all words */
    printf("All unique words:\n");
    TrieWordsResult result = trie_get_all_words(trie);
    for (size_t i = 0; i < result.count; i++) {
        printf("  %s\n", result.words[i]);
    }
    trie_free_words_result(&result);
    
    /* Check specific words */
    printf("\n--- Word Lookups ---\n\n");
    const char *check_words[] = {"the", "quick", "fox", "lazy", "dog", "cat"};
    
    for (int i = 0; i < 6; i++) {
        const char *w = check_words[i];
        bool found = trie_search(trie, w);
        printf("'%s': %s\n", w, found ? "present" : "absent");
    }
    
    /* Prefix analysis */
    printf("\n--- Prefix Analysis ---\n\n");
    
    const char *prefixes[] = {"qu", "la", "fo", "th"};
    for (int i = 0; i < 4; i++) {
        size_t count = trie_count_prefix(trie, prefixes[i]);
        printf("Words starting with '%s': %zu\n", prefixes[i], count);
        
        TrieWordsResult words = trie_get_words_with_prefix(trie, prefixes[i], 0);
        for (size_t j = 0; j < words.count; j++) {
            printf("  - %s\n", words.words[j]);
        }
        trie_free_words_result(&words);
        printf("\n");
    }
    
    trie_destroy(trie);
    printf("Trie destroyed.\n");
    
    return 0;
}