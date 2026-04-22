/**
 * @file spell_checker.c
 * @brief Spell checker example using Trie
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "trie.h"

/* Check if a word is spelled correctly */
bool is_spelled_correctly(Trie *dictionary, const char *word) {
    return trie_search(dictionary, word);
}

/* Find similar words (words with same prefix) */
void suggest_corrections(Trie *dictionary, const char *word, size_t max_suggestions) {
    printf("Suggestions for '%s':\n", word);
    
    /* Try words with the same first few characters */
    size_t word_len = strlen(word);
    size_t prefix_len = word_len > 3 ? 3 : word_len;
    char prefix[4] = {0};
    memcpy(prefix, word, prefix_len);
    
    TrieWordsResult result = trie_get_words_with_prefix(dictionary, prefix, max_suggestions);
    
    if (result.count == 0) {
        printf("  No suggestions found.\n");
    } else {
        for (size_t i = 0; i < result.count; i++) {
            printf("  - %s\n", result.words[i]);
        }
    }
    
    trie_free_words_result(&result);
}

int main(void) {
    printf("=== Trie Spell Checker Example ===\n\n");
    
    Trie *dictionary = trie_create();
    
    /* Load a simple dictionary */
    const char *words[] = {
        "apple", "application", "apartment", "appreciate", "approach",
        "banana", "balance", "battle", "beauty", "begin",
        "computer", "compare", "complete", "condition", "create",
        "develop", "different", "document", "double", "during",
        "example", "exercise", "experience", "explain", "express",
        "function", "future", "general", "garden", "gather",
        "hello", "helpful", "history", "hospital", "however",
        "important", "include", "information", "instead", "interest",
        "javascript", "javascripts", "journey", "justify",
        "knowledge", "kitchen",
        "language", "latest", "letter", "library", "limited",
        "machine", "management", "material", "method", "middle",
        "number", "object", "offer", "operation", "option",
        "people", "personal", "picture", "possible", "problem",
        "quality", "question", "quick", "quiet",
        "result", "return", "review", "running",
        "special", "standard", "station", "strong", "student",
        "table", "technology", "template", "together", "total",
        "understand", "university", "update", "useful",
        "variable", "version", "video", "virtual", "visible",
        "window", "without", "working", "writing",
        NULL
    };
    
    printf("Loading dictionary...\n");
    size_t count = trie_insert_batch(dictionary, words, 100);
    printf("Loaded %zu words.\n\n", count);
    
    /* Check spelling of various words */
    const char *test_words[] = {
        "apple", "appel",      /* correct / misspelled */
        "hello", "helo",        /* correct / misspelled */
        "javascript", "javascipt",  /* correct / misspelled */
        "question", "queston",  /* correct / misspelled */
        NULL
    };
    
    printf("--- Spell Checking ---\n\n");
    
    for (int i = 0; test_words[i] != NULL; i++) {
        const char *word = test_words[i];
        printf("Checking: '%s'\n", word);
        
        if (is_spelled_correctly(dictionary, word)) {
            printf("  ✓ Correct spelling\n\n");
        } else {
            printf("  ✗ Misspelled\n");
            suggest_corrections(dictionary, word, 5);
            printf("\n");
        }
    }
    
    /* Pattern matching for fuzzy search */
    printf("--- Pattern Matching ---\n\n");
    
    char *matches[20];
    size_t match_count;
    
    /* Match words like "he?lo" (hello, etc.) */
    printf("Pattern 'he?lo' (any character at ?):\n");
    match_count = trie_pattern_match(dictionary, "he?lo", matches, 20);
    for (size_t i = 0; i < match_count; i++) {
        printf("  - %s\n", matches[i]);
        free(matches[i]);
    }
    printf("\n");
    
    /* Match words starting with "comp" */
    printf("Pattern 'comp*':\n");
    match_count = trie_pattern_match(dictionary, "comp*", matches, 20);
    for (size_t i = 0; i < match_count; i++) {
        printf("  - %s\n", matches[i]);
        free(matches[i]);
    }
    printf("\n");
    
    trie_destroy(dictionary);
    printf("Dictionary destroyed.\n");
    
    return 0;
}