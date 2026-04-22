/**
 * @file iterator_demo.c
 * @brief Trie iterator demonstration
 */

#include <stdio.h>
#include <string.h>
#include "trie.h"

int main(void) {
    printf("=== Trie Iterator Example ===\n\n");
    
    Trie *trie = trie_create();
    
    /* Insert words in random order */
    const char *words[] = {
        "zebra", "apple", "mango", "banana", "cherry",
        "orange", "grape", "kiwi", "peach", "lemon",
        NULL
    };
    
    printf("Inserting words:\n");
    for (int i = 0; words[i] != NULL; i++) {
        printf("  %s\n", words[i]);
        trie_insert(trie, words[i]);
    }
    printf("\nTotal words: %zu\n\n", trie_size(trie));
    
    /* Use iterator to traverse all words */
    printf("--- Iterating all words (alphabetical order) ---\n");
    
    TrieIterator iter;
    trie_iterator_init(trie, &iter);
    
    char buffer[256];
    int count = 0;
    
    while (trie_iterator_next(&iter, buffer, sizeof(buffer))) {
        printf("  %d. %s\n", ++count, buffer);
    }
    
    printf("\nIterated %d words.\n\n", count);
    
    /* Demonstrate early termination */
    printf("--- First 5 words only ---\n");
    
    trie_iterator_init(trie, &iter);
    count = 0;
    
    while (trie_iterator_next(&iter, buffer, sizeof(buffer)) && count < 5) {
        printf("  %s\n", buffer);
        count++;
    }
    
    printf("\n");
    
    trie_destroy(trie);
    printf("Trie destroyed.\n");
    
    return 0;
}