/**
 * @file trie.c
 * @brief Trie (Prefix Tree) Implementation
 */

#include "trie.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/*
 * ================================
 * Internal Helper Functions
 * ================================
 */

/* Create a new trie node */
static TrieNode *trie_node_create(void) {
    TrieNode *node = (TrieNode *)calloc(1, sizeof(TrieNode));
    if (node == NULL) {
        return NULL;
    }
    node->is_end_of_word = false;
    node->word_count = 0;
    /* children are initialized to NULL by calloc */
    return node;
}

/* Free a trie node and all its children */
static void trie_node_free(TrieNode *node) {
    if (node == NULL) {
        return;
    }
    for (int i = 0; i < TRIE_ALPHABET_SIZE; i++) {
        if (node->children[i] != NULL) {
            trie_node_free(node->children[i]);
        }
    }
    free(node);
}

/* Check if a node has any children */
static bool trie_node_has_children(const TrieNode *node) {
    if (node == NULL) {
        return false;
    }
    for (int i = 0; i < TRIE_ALPHABET_SIZE; i++) {
        if (node->children[i] != NULL) {
            return true;
        }
    }
    return false;
}



/* Recursive helper for collecting words with prefix */
static void trie_collect_words(TrieNode *node, char *prefix, size_t prefix_len,
                               TrieWordsResult *result, size_t limit) {
    if (node == NULL || (limit > 0 && result->count >= limit)) {
        return;
    }
    
    if (node->is_end_of_word) {
        if (result->count >= result->capacity) {
            /* Grow the array */
            size_t new_capacity = result->capacity == 0 ? 16 : result->capacity * 2;
            char **new_words = (char **)realloc(result->words, new_capacity * sizeof(char *));
            if (new_words == NULL) {
                return;
            }
            result->words = new_words;
            result->capacity = new_capacity;
        }
        
        /* Copy the word */
        result->words[result->count] = (char *)malloc(prefix_len + 1);
        if (result->words[result->count] != NULL) {
            memcpy(result->words[result->count], prefix, prefix_len + 1);
            result->count++;
        }
    }
    
    /* Recursively collect from children */
    for (int i = 0; i < TRIE_ALPHABET_SIZE; i++) {
        if (node->children[i] != NULL) {
            if (prefix_len < TRIE_MAX_WORD_LENGTH - 1) {
                prefix[prefix_len] = (char)i;
                prefix[prefix_len + 1] = '\0';
                trie_collect_words(node->children[i], prefix, prefix_len + 1, result, limit);
            }
        }
    }
    
    /* Restore prefix for backtracking */
    prefix[prefix_len] = '\0';
}

/* Recursive delete helper */
static bool trie_delete_helper(Trie *trie, TrieNode *node, const char *word, size_t depth) {
    if (node == NULL) {
        return false;
    }
    
    size_t len = strlen(word);
    if (depth == len) {
        /* End of word */
        if (!node->is_end_of_word) {
            return false;  /* Word not found */
        }
        node->is_end_of_word = false;
        trie->size--;
        
        /* Update word count for this node */
        node->word_count--;
        
        /* Delete node if it has no children */
        if (!trie_node_has_children(node)) {
            return true;  /* Signal to delete this node */
        }
        return false;
    }
    
    /* Recurse to child */
    unsigned char index = (unsigned char)word[depth];
    TrieNode *child = node->children[index];
    
    if (child == NULL) {
        return false;  /* Word not found */
    }
    
    bool should_delete_child = trie_delete_helper(trie, child, word, depth + 1);
    
    /* Update word count if word was found */
    node->word_count--;
    
    if (should_delete_child) {
        /* Child should be deleted */
        trie_node_free(node->children[index]);
        node->children[index] = NULL;
        trie->node_count--;
        
        /* Delete current node if not end of word and has no children */
        if (!node->is_end_of_word && !trie_node_has_children(node)) {
            return true;
        }
    }
    
    return false;
}

/* Recursive pattern match helper */
static void trie_pattern_match_helper(TrieNode *node, const char *pattern, size_t pattern_idx,
                                      char *buffer, size_t buffer_len,
                                      char **matches, size_t *match_count, size_t max_matches) {
    if (node == NULL || *match_count >= max_matches) {
        return;
    }
    
    /* If we've reached the end of the pattern */
    if (pattern[pattern_idx] == '\0') {
        if (node->is_end_of_word) {
            matches[*match_count] = (char *)malloc(buffer_len + 1);
            if (matches[*match_count] != NULL) {
                memcpy(matches[*match_count], buffer, buffer_len + 1);
                (*match_count)++;
            }
        }
        return;
    }
    
    char p = pattern[pattern_idx];
    
    if (p == '?') {
        /* Match any single character */
        for (int i = 0; i < TRIE_ALPHABET_SIZE; i++) {
            if (node->children[i] != NULL && buffer_len < TRIE_MAX_WORD_LENGTH - 1) {
                buffer[buffer_len] = (char)i;
                buffer[buffer_len + 1] = '\0';
                trie_pattern_match_helper(node->children[i], pattern, pattern_idx + 1,
                                         buffer, buffer_len + 1, matches, match_count, max_matches);
            }
        }
    } else if (p == '*') {
        /* Match zero or more characters */
        /* Case 1: Skip the * (match zero chars) */
        trie_pattern_match_helper(node, pattern, pattern_idx + 1, buffer, buffer_len,
                                  matches, match_count, max_matches);
        
        /* Case 2: Match one more character and stay on * */
        for (int i = 0; i < TRIE_ALPHABET_SIZE; i++) {
            if (node->children[i] != NULL && buffer_len < TRIE_MAX_WORD_LENGTH - 1) {
                buffer[buffer_len] = (char)i;
                buffer[buffer_len + 1] = '\0';
                trie_pattern_match_helper(node->children[i], pattern, pattern_idx,
                                         buffer, buffer_len + 1, matches, match_count, max_matches);
            }
        }
    } else {
        /* Exact match */
        unsigned char idx = (unsigned char)p;
        if (node->children[idx] != NULL && buffer_len < TRIE_MAX_WORD_LENGTH - 1) {
            buffer[buffer_len] = p;
            buffer[buffer_len + 1] = '\0';
            trie_pattern_match_helper(node->children[idx], pattern, pattern_idx + 1,
                                      buffer, buffer_len + 1, matches, match_count, max_matches);
        }
    }
}

/* Recursive print helper */
static void trie_print_helper(const TrieNode *node, char *buffer, size_t depth, bool show_counts) {
    if (node == NULL) {
        return;
    }
    
    if (node->is_end_of_word) {
        buffer[depth] = '\0';
        if (show_counts) {
            printf("'%s' (count: %zu)\n", buffer, node->word_count);
        } else {
            printf("'%s'\n", buffer);
        }
    }
    
    for (int i = 0; i < TRIE_ALPHABET_SIZE; i++) {
        if (node->children[i] != NULL) {
            buffer[depth] = (char)i;
            trie_print_helper(node->children[i], buffer, depth + 1, show_counts);
        }
    }
}

/*
 * ================================
 * Creation and Destruction
 * ================================
 */

Trie *trie_create(void) {
    Trie *trie = (Trie *)malloc(sizeof(Trie));
    if (trie == NULL) {
        return NULL;
    }
    
    trie->root = trie_node_create();
    if (trie->root == NULL) {
        free(trie);
        return NULL;
    }
    
    trie->size = 0;
    trie->node_count = 1;
    
    return trie;
}

void trie_destroy(Trie *trie) {
    if (trie == NULL) {
        return;
    }
    trie_node_free(trie->root);
    free(trie);
}

void trie_clear(Trie *trie) {
    if (trie == NULL) {
        return;
    }
    
    /* Free all children of root but keep root */
    for (int i = 0; i < TRIE_ALPHABET_SIZE; i++) {
        if (trie->root->children[i] != NULL) {
            trie_node_free(trie->root->children[i]);
            trie->root->children[i] = NULL;
        }
    }
    
    trie->root->is_end_of_word = false;
    trie->root->word_count = 0;
    trie->size = 0;
    trie->node_count = 1;
}

/*
 * ================================
 * Basic Operations
 * ================================
 */

bool trie_insert(Trie *trie, const char *word) {
    if (trie == NULL || word == NULL) {
        return false;
    }
    
    size_t len = strlen(word);
    if (len == 0 || len >= TRIE_MAX_WORD_LENGTH) {
        return false;
    }
    
    TrieNode *current = trie->root;
    
    for (size_t i = 0; i < len; i++) {
        unsigned char index = (unsigned char)word[i];
        
        if (current->children[index] == NULL) {
            current->children[index] = trie_node_create();
            if (current->children[index] == NULL) {
                return false;  /* Allocation failure */
            }
            trie->node_count++;
        }
        
        current->word_count++;
        current = current->children[index];
    }
    
    /* Check if word already exists */
    if (current->is_end_of_word) {
        return true;  /* Word already in trie */
    }
    
    current->is_end_of_word = true;
    current->word_count++;
    trie->size++;
    
    return true;
}

bool trie_search(const Trie *trie, const char *word) {
    if (trie == NULL || word == NULL) {
        return false;
    }
    
    size_t len = strlen(word);
    if (len == 0) {
        return false;
    }
    
    const TrieNode *current = trie->root;
    
    for (size_t i = 0; i < len; i++) {
        unsigned char index = (unsigned char)word[i];
        
        if (current->children[index] == NULL) {
            return false;
        }
        current = current->children[index];
    }
    
    return current->is_end_of_word;
}

bool trie_delete(Trie *trie, const char *word) {
    if (trie == NULL || word == NULL || trie->root == NULL) {
        return false;
    }
    
    size_t len = strlen(word);
    if (len == 0) {
        return false;
    }
    
    /* Check if word exists first */
    if (!trie_search(trie, word)) {
        return false;
    }
    
    /* Store original size to verify deletion */
    size_t original_size = trie->size;
    
    trie_delete_helper(trie, trie->root, word, 0);
    
    /* Return true if size decreased */
    return trie->size < original_size;
}

size_t trie_insert_batch(Trie *trie, const char **words, size_t count) {
    if (trie == NULL || words == NULL) {
        return 0;
    }
    
    size_t inserted = 0;
    for (size_t i = 0; i < count; i++) {
        if (words[i] != NULL && trie_insert(trie, words[i])) {
            inserted++;
        }
    }
    
    return inserted;
}

/*
 * ================================
 * Prefix Operations
 * ================================
 */

bool trie_starts_with(const Trie *trie, const char *prefix) {
    if (trie == NULL || prefix == NULL) {
        return false;
    }
    
    return trie_get_prefix_node(trie, prefix) != NULL;
}

TrieNode *trie_get_prefix_node(const Trie *trie, const char *prefix) {
    if (trie == NULL || prefix == NULL) {
        return NULL;
    }
    
    TrieNode *current = trie->root;
    size_t len = strlen(prefix);
    
    for (size_t i = 0; i < len; i++) {
        unsigned char index = (unsigned char)prefix[i];
        
        if (current == NULL || current->children[index] == NULL) {
            return NULL;
        }
        current = current->children[index];
    }
    
    return current;
}

size_t trie_count_prefix(const Trie *trie, const char *prefix) {
    if (trie == NULL || prefix == NULL) {
        return 0;
    }
    
    TrieNode *node = trie_get_prefix_node(trie, prefix);
    if (node == NULL) {
        return 0;
    }
    
    return node->word_count;
}

size_t trie_longest_common_prefix(const Trie *trie, char *buffer, size_t buffer_size) {
    if (trie == NULL || buffer == NULL || buffer_size == 0) {
        return 0;
    }
    
    buffer[0] = '\0';
    
    if (trie->size == 0) {
        return 0;
    }
    
    /* Single word has no common prefix (requires at least 2 words) */
    if (trie->size <= 1) {
        buffer[0] = '\0';
        return 0;
    }
    
    size_t len = 0;
    TrieNode *current = trie->root;
    
    while (current != NULL && len < buffer_size - 1) {
        int child_count = 0;
        int child_index = -1;
        
        /* Find the only child */
        for (int i = 0; i < TRIE_ALPHABET_SIZE; i++) {
            if (current->children[i] != NULL) {
                child_count++;
                child_index = i;
            }
        }
        
        /* Stop if multiple children or word ends here */
        if (child_count != 1 || current->is_end_of_word) {
            break;
        }
        
        buffer[len++] = (char)child_index;
        current = current->children[child_index];
    }
    
    buffer[len] = '\0';
    return len;
}

/*
 * ================================
 * Autocomplete and Suggestions
 * ================================
 */

TrieWordsResult trie_get_words_with_prefix(const Trie *trie, const char *prefix, size_t limit) {
    TrieWordsResult result = {NULL, 0, 0};
    
    if (trie == NULL || prefix == NULL) {
        return result;
    }
    
    TrieNode *start = trie_get_prefix_node(trie, prefix);
    if (start == NULL) {
        return result;
    }
    
    /* Initialize result with initial capacity */
    result.words = (char **)malloc(16 * sizeof(char *));
    if (result.words == NULL) {
        return result;
    }
    result.capacity = 16;
    result.count = 0;
    
    /* Prepare buffer with prefix */
    char buffer[TRIE_MAX_WORD_LENGTH];
    size_t prefix_len = strlen(prefix);
    if (prefix_len >= TRIE_MAX_WORD_LENGTH) {
        trie_free_words_result(&result);
        result.words = NULL;
        result.count = 0;
        result.capacity = 0;
        return result;
    }
    
    memcpy(buffer, prefix, prefix_len + 1);
    
    /* Collect words */
    trie_collect_words(start, buffer, prefix_len, &result, limit);
    
    return result;
}

TrieWordsResult trie_get_all_words(const Trie *trie) {
    return trie_get_words_with_prefix(trie, "", 0);
}

void trie_free_words_result(TrieWordsResult *result) {
    if (result == NULL || result->words == NULL) {
        return;
    }
    
    for (size_t i = 0; i < result->count; i++) {
        free(result->words[i]);
    }
    free(result->words);
    result->words = NULL;
    result->count = 0;
    result->capacity = 0;
}

/*
 * ================================
 * Utility Functions
 * ================================
 */

size_t trie_size(const Trie *trie) {
    return trie != NULL ? trie->size : 0;
}

size_t trie_node_count(const Trie *trie) {
    return trie != NULL ? trie->node_count : 0;
}

bool trie_is_empty(const Trie *trie) {
    return trie == NULL || trie->size == 0;
}

size_t trie_pattern_match(const Trie *trie, const char *pattern, 
                          char **matches, size_t max_matches) {
    if (trie == NULL || pattern == NULL || matches == NULL || max_matches == 0) {
        return 0;
    }
    
    char buffer[TRIE_MAX_WORD_LENGTH];
    buffer[0] = '\0';
    size_t match_count = 0;
    
    trie_pattern_match_helper(trie->root, pattern, 0, buffer, 0, matches, &match_count, max_matches);
    
    return match_count;
}

/*
 * ================================
 * Iterator Support
 * ================================
 */

void trie_iterator_init(const Trie *trie, TrieIterator *iter) {
    if (iter == NULL) {
        return;
    }
    
    memset(iter, 0, sizeof(TrieIterator));
    
    if (trie != NULL && trie->root != NULL) {
        iter->stack[0] = trie->root;
        iter->indices[0] = -1;
        iter->depth = 0;
    }
}

bool trie_iterator_next(TrieIterator *iter, char *buffer, size_t buffer_size) {
    if (iter == NULL || buffer == NULL || buffer_size == 0) {
        return false;
    }
    
    while (iter->depth >= 0) {
        TrieNode *current = iter->stack[iter->depth];
        
        /* Find next child */
        int start = iter->indices[iter->depth] + 1;
        bool found = false;
        
        for (int i = start; i < TRIE_ALPHABET_SIZE; i++) {
            if (current->children[i] != NULL) {
                iter->indices[iter->depth] = i;
                iter->buffer[iter->depth] = (char)i;
                
                if (iter->depth + 1 < (int)buffer_size - 1) {
                    iter->depth++;
                    iter->stack[iter->depth] = current->children[i];
                    iter->indices[iter->depth] = -1;
                }
                
                found = true;
                
                /* Check if current node is end of word */
                if (current->children[i]->is_end_of_word) {
                    memcpy(buffer, iter->buffer, iter->depth + 1);
                    buffer[iter->depth + 1] = '\0';
                    return true;
                }
                
                break;
            }
        }
        
        if (!found) {
            /* Backtrack */
            iter->depth--;
        }
    }
    
    return false;
}

bool trie_iterator_has_next(const TrieIterator *iter) {
    return iter != NULL && iter->depth >= 0;
}

/*
 * ================================
 * Debug and Statistics
 * ================================
 */

void trie_print(const Trie *trie, bool show_counts) {
    if (trie == NULL) {
        printf("Trie: (null)\n");
        return;
    }
    
    printf("Trie (size: %zu, nodes: %zu):\n", trie->size, trie->node_count);
    
    char buffer[TRIE_MAX_WORD_LENGTH];
    trie_print_helper(trie->root, buffer, 0, show_counts);
}

size_t trie_memory_usage(const Trie *trie) {
    if (trie == NULL) {
        return 0;
    }
    
    return sizeof(Trie) + trie->node_count * sizeof(TrieNode);
}