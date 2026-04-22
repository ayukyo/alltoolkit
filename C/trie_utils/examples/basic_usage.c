/**
 * @file basic_usage.c
 * @brief Basic usage examples for the Trie library
 */

#include <stdio.h>
#include <string.h>
#include "trie.h"

int main(void) {
    printf("=== Trie Basic Usage Example ===\n\n");
    
    /* Create a new trie */
    Trie *trie = trie_create();
    if (trie == NULL) {
        printf("Failed to create trie!\n");
        return 1;
    }
    
    /* Insert words */
    printf("--- Inserting words ---\n");
    trie_insert(trie, "apple");
    trie_insert(trie, "appetite");
    trie_insert(trie, "application");
    trie_insert(trie, "apply");
    trie_insert(trie, "banana");
    trie_insert(trie, "band");
    trie_insert(trie, "bandana");
    printf("Inserted: apple, appetite, application, apply, banana, band, bandana\n\n");
    
    /* Print statistics */
    printf("--- Statistics ---\n");
    printf("Total words: %zu\n", trie_size(trie));
    printf("Total nodes: %zu\n", trie_node_count(trie));
    printf("Memory usage: %zu bytes\n\n", trie_memory_usage(trie));
    
    /* Search for words */
    printf("--- Searching ---\n");
    printf("Search 'apple': %s\n", trie_search(trie, "apple") ? "found" : "not found");
    printf("Search 'app': %s\n", trie_search(trie, "app") ? "found" : "not found");
    printf("Search 'banana': %s\n", trie_search(trie, "banana") ? "found" : "not found");
    printf("Search 'band': %s\n", trie_search(trie, "band") ? "found" : "not found");
    printf("Search 'bandana': %s\n", trie_search(trie, "bandana") ? "found" : "not found");
    printf("Search 'orange': %s\n\n", trie_search(trie, "orange") ? "found" : "not found");
    
    /* Prefix operations */
    printf("--- Prefix operations ---\n");
    printf("Starts with 'app': %s\n", trie_starts_with(trie, "app") ? "yes" : "no");
    printf("Starts with 'ban': %s\n", trie_starts_with(trie, "ban") ? "yes" : "no");
    printf("Starts with 'ora': %s\n\n", trie_starts_with(trie, "ora") ? "yes" : "no");
    
    /* Count words with prefix */
    printf("Words with prefix 'app': %zu\n", trie_count_prefix(trie, "app"));
    printf("Words with prefix 'ban': %zu\n", trie_count_prefix(trie, "ban"));
    printf("Words with prefix 'xyz': %zu\n\n", trie_count_prefix(trie, "xyz"));
    
    /* Longest common prefix */
    char lcp[256];
    size_t lcp_len = trie_longest_common_prefix(trie, lcp, sizeof(lcp));
    printf("Longest common prefix: '%s' (length: %zu)\n\n", lcp, lcp_len);
    
    /* Delete a word */
    printf("--- Deleting 'apply' ---\n");
    trie_delete(trie, "apply");
    printf("Search 'apply' after delete: %s\n", trie_search(trie, "apply") ? "found" : "not found");
    printf("Total words: %zu\n\n", trie_size(trie));
    
    /* Print all words */
    printf("--- All words in trie ---\n");
    trie_print(trie, false);
    
    /* Clean up */
    trie_destroy(trie);
    printf("\nTrie destroyed successfully.\n");
    
    return 0;
}