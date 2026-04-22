/**
 * @file autocomplete.c
 * @brief Autocomplete example using Trie
 */

#include <stdio.h>
#include <string.h>
#include "trie.h"

int main(void) {
    printf("=== Trie Autocomplete Example ===\n\n");
    
    Trie *trie = trie_create();
    
    /* Insert a dictionary of words */
    const char *dictionary[] = {
        "apple", "appetite", "application", "apply", "apprentice",
        "banana", "band", "bandana", "bank", "banner",
        "cat", "car", "card", "care", "carpet", "carrot",
        "dog", "door", "doorbell", "dormitory",
        NULL
    };
    
    printf("Loading dictionary...\n");
    for (int i = 0; dictionary[i] != NULL; i++) {
        trie_insert(trie, dictionary[i]);
    }
    printf("Loaded %zu words.\n\n", trie_size(trie));
    
    /* Simulate user typing */
    const char *prefixes[] = {"app", "ban", "car", "do", "xyz"};
    
    for (int i = 0; i < 5; i++) {
        printf("User types: '%s'\n", prefixes[i]);
        
        TrieWordsResult suggestions = trie_get_words_with_prefix(trie, prefixes[i], 5);
        
        if (suggestions.count == 0) {
            printf("  No suggestions found.\n");
        } else {
            printf("  Suggestions (%zu found):\n", suggestions.count);
            for (size_t j = 0; j < suggestions.count; j++) {
                printf("    %zu. %s\n", j + 1, suggestions.words[j]);
            }
        }
        
        trie_free_words_result(&suggestions);
        printf("\n");
    }
    
    /* Limited suggestions example */
    printf("--- Limited suggestions (max 3) ---\n");
    TrieWordsResult limited = trie_get_words_with_prefix(trie, "app", 3);
    printf("Prefix 'app' with limit 3:\n");
    for (size_t i = 0; i < limited.count; i++) {
        printf("  %s\n", limited.words[i]);
    }
    trie_free_words_result(&limited);
    
    /* Unlimited suggestions */
    printf("\n--- All words ---\n");
    TrieWordsResult all = trie_get_all_words(trie);
    printf("Total words in trie: %zu\n", all.count);
    trie_free_words_result(&all);
    
    trie_destroy(trie);
    return 0;
}