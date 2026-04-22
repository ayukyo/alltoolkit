/**
 * @file trie.h
 * @brief Trie (Prefix Tree) Implementation in C
 * 
 * A memory-efficient trie data structure for string storage and prefix-based
 * operations. Supports Unicode UTF-8 strings.
 * 
 * Features:
 * - Insert, search, delete operations
 * - Prefix-based queries (autocomplete)
 * - Memory-efficient node structure
 * - Thread-safe operations (user must provide locks)
 * - Iterator support for traversal
 * 
 * @author AllToolkit
 * @date 2026-04-22
 */

#ifndef TRIE_H
#define TRIE_H

#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Configuration */
#define TRIE_ALPHABET_SIZE 128      /* ASCII range for simplicity */
#define TRIE_MAX_WORD_LENGTH 4096   /* Maximum word length */
#define TRIE_AUTOCOMPLETE_LIMIT 100 /* Default autocomplete limit */

/* Trie node structure */
typedef struct TrieNode {
    struct TrieNode *children[TRIE_ALPHABET_SIZE];  /* Child nodes */
    bool is_end_of_word;                              /* Word terminator flag */
    size_t word_count;                                /* Number of words below this node */
} TrieNode;

/* Trie structure */
typedef struct Trie {
    TrieNode *root;         /* Root node */
    size_t size;            /* Total number of words */
    size_t node_count;      /* Total number of nodes */
} Trie;

/* Iterator for word traversal */
typedef struct TrieIterator {
    TrieNode *stack[TRIE_MAX_WORD_LENGTH];   /* Node stack */
    int indices[TRIE_MAX_WORD_LENGTH];       /* Current child indices */
    int depth;                                 /* Current depth */
    char buffer[TRIE_MAX_WORD_LENGTH];        /* Current word buffer */
} TrieIterator;

/* 
 * ================================
 * Creation and Destruction
 * ================================
 */

/**
 * @brief Create a new empty trie
 * @return Pointer to new trie, or NULL on allocation failure
 */
Trie *trie_create(void);

/**
 * @brief Free all memory associated with a trie
 * @param trie Trie to destroy
 */
void trie_destroy(Trie *trie);

/**
 * @brief Clear all words from a trie (keeps structure)
 * @param trie Trie to clear
 */
void trie_clear(Trie *trie);

/*
 * ================================
 * Basic Operations
 * ================================
 */

/**
 * @brief Insert a word into the trie
 * @param trie Target trie
 * @param word Word to insert (null-terminated string)
 * @return true on success, false on failure
 */
bool trie_insert(Trie *trie, const char *word);

/**
 * @brief Check if a word exists in the trie
 * @param trie Target trie
 * @param word Word to search for
 * @return true if word exists, false otherwise
 */
bool trie_search(const Trie *trie, const char *word);

/**
 * @brief Remove a word from the trie
 * @param trie Target trie
 * @param word Word to remove
 * @return true if word was found and removed, false otherwise
 */
bool trie_delete(Trie *trie, const char *word);

/**
 * @brief Insert multiple words at once
 * @param trie Target trie
 * @param words Array of word strings
 * @param count Number of words
 * @return Number of words successfully inserted
 */
size_t trie_insert_batch(Trie *trie, const char **words, size_t count);

/*
 * ================================
 * Prefix Operations
 * ================================
 */

/**
 * @brief Check if any word starts with the given prefix
 * @param trie Target trie
 * @param prefix Prefix to check
 * @return true if prefix exists, false otherwise
 */
bool trie_starts_with(const Trie *trie, const char *prefix);

/**
 * @brief Get the node for a given prefix
 * @param trie Target trie
 * @param prefix Prefix to find
 * @return Pointer to prefix node, or NULL if not found
 */
TrieNode *trie_get_prefix_node(const Trie *trie, const char *prefix);

/**
 * @brief Count words with a given prefix
 * @param trie Target trie
 * @param prefix Prefix to match
 * @return Number of words starting with prefix
 */
size_t trie_count_prefix(const Trie *trie, const char *prefix);

/**
 * @brief Find longest common prefix of all words
 * @param trie Target trie
 * @param buffer Output buffer for prefix
 * @param buffer_size Size of output buffer
 * @return Length of longest common prefix
 */
size_t trie_longest_common_prefix(const Trie *trie, char *buffer, size_t buffer_size);

/*
 * ================================
 * Autocomplete and Suggestions
 * ================================
 */

/**
 * @brief Result structure for autocomplete
 */
typedef struct {
    char **words;       /* Array of word pointers */
    size_t count;       /* Number of words */
    size_t capacity;    /* Array capacity */
} TrieWordsResult;

/**
 * @brief Get all words with a given prefix
 * @param trie Target trie
 * @param prefix Prefix to match
 * @param limit Maximum number of results (0 for no limit)
 * @return Structure containing words array (caller must free with trie_free_words_result)
 */
TrieWordsResult trie_get_words_with_prefix(const Trie *trie, const char *prefix, size_t limit);

/**
 * @brief Get all words in the trie
 * @param trie Target trie
 * @return Structure containing all words (caller must free)
 */
TrieWordsResult trie_get_all_words(const Trie *trie);

/**
 * @brief Free a TrieWordsResult structure
 * @param result Result to free
 */
void trie_free_words_result(TrieWordsResult *result);

/*
 * ================================
 * Utility Functions
 * ================================
 */

/**
 * @brief Get total number of words in trie
 * @param trie Target trie
 * @return Word count
 */
size_t trie_size(const Trie *trie);

/**
 * @brief Get total number of nodes in trie
 * @param trie Target trie
 * @return Node count
 */
size_t trie_node_count(const Trie *trie);

/**
 * @brief Check if trie is empty
 * @param trie Target trie
 * @return true if empty, false otherwise
 */
bool trie_is_empty(const Trie *trie);

/**
 * @brief Check if a word matches a pattern (supports ? and *)
 * @param trie Target trie
 * @param pattern Pattern with ? (single char) and * (any chars)
 * @param matches Output array for matching words
 * @param match_count Maximum matches to return
 * @return Number of matches found
 */
size_t trie_pattern_match(const Trie *trie, const char *pattern, 
                          char **matches, size_t match_count);

/*
 * ================================
 * Iterator Support
 * ================================
 */

/**
 * @brief Initialize an iterator for traversal
 * @param trie Target trie
 * @param iter Iterator to initialize
 */
void trie_iterator_init(const Trie *trie, TrieIterator *iter);

/**
 * @brief Get next word from iterator
 * @param iter Iterator to advance
 * @param buffer Output buffer for word
 * @param buffer_size Size of output buffer
 * @return true if word found, false if iteration complete
 */
bool trie_iterator_next(TrieIterator *iter, char *buffer, size_t buffer_size);

/**
 * @brief Check if iterator has more words
 * @param iter Iterator to check
 * @return true if more words available
 */
bool trie_iterator_has_next(const TrieIterator *iter);

/*
 * ================================
 * Debug and Statistics
 * ================================
 */

/**
 * @brief Print trie structure (for debugging)
 * @param trie Trie to print
 * @param show_counts Show word counts at each node
 */
void trie_print(const Trie *trie, bool show_counts);

/**
 * @brief Calculate memory usage of trie
 * @param trie Target trie
 * @return Memory usage in bytes
 */
size_t trie_memory_usage(const Trie *trie);

#ifdef __cplusplus
}
#endif

#endif /* TRIE_H */