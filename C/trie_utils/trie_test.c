/**
 * @file trie_test.c
 * @brief Unit tests for Trie implementation
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "trie.h"

/* Test counter */
static int tests_passed = 0;
static int tests_total = 0;

/* Test macros */
#define TEST_START(name) do { tests_total++; printf("Testing: %s... ", name); } while(0)
#define TEST_PASS() do { tests_passed++; printf("PASS\n"); } while(0)
#define TEST_FAIL(msg) do { printf("FAIL: %s\n", msg); } while(0)
#define ASSERT_TRUE(cond, msg) do { if (!(cond)) { TEST_FAIL(msg); return; } } while(0)
#define ASSERT_FALSE(cond, msg) do { if (cond) { TEST_FAIL(msg); return; } } while(0)
#define ASSERT_EQ(a, b, msg) do { if ((a) != (b)) { TEST_FAIL(msg); return; } } while(0)
#define ASSERT_STR_EQ(a, b, msg) do { if (strcmp((a), (b)) != 0) { TEST_FAIL(msg); return; } } while(0)

/* ==================== Basic Tests ==================== */

void test_create_destroy(void) {
    TEST_START("trie_create and trie_destroy");
    
    Trie *trie = trie_create();
    ASSERT_TRUE(trie != NULL, "trie should not be NULL");
    ASSERT_TRUE(trie->root != NULL, "root should not be NULL");
    ASSERT_EQ(trie->size, 0, "size should be 0");
    ASSERT_EQ(trie->node_count, 1, "node_count should be 1");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_is_empty(void) {
    TEST_START("trie_is_empty");
    
    Trie *trie = trie_create();
    ASSERT_TRUE(trie_is_empty(trie), "empty trie should return true");
    
    trie_insert(trie, "test");
    ASSERT_FALSE(trie_is_empty(trie), "non-empty trie should return false");
    
    trie_destroy(trie);
    TEST_PASS();
}

/* ==================== Insert Tests ==================== */

void test_insert_single(void) {
    TEST_START("trie_insert single word");
    
    Trie *trie = trie_create();
    ASSERT_TRUE(trie_insert(trie, "hello"), "insert should succeed");
    ASSERT_EQ(trie->size, 1, "size should be 1");
    ASSERT_TRUE(trie_search(trie, "hello"), "word should be found");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_insert_multiple(void) {
    TEST_START("trie_insert multiple words");
    
    Trie *trie = trie_create();
    
    ASSERT_TRUE(trie_insert(trie, "apple"), "insert apple should succeed");
    ASSERT_TRUE(trie_insert(trie, "app"), "insert app should succeed");
    ASSERT_TRUE(trie_insert(trie, "application"), "insert application should succeed");
    ASSERT_TRUE(trie_insert(trie, "banana"), "insert banana should succeed");
    
    ASSERT_EQ(trie->size, 4, "size should be 4");
    ASSERT_TRUE(trie_search(trie, "apple"), "apple should be found");
    ASSERT_TRUE(trie_search(trie, "app"), "app should be found");
    ASSERT_TRUE(trie_search(trie, "application"), "application should be found");
    ASSERT_TRUE(trie_search(trie, "banana"), "banana should be found");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_insert_duplicate(void) {
    TEST_START("trie_insert duplicate word");
    
    Trie *trie = trie_create();
    
    ASSERT_TRUE(trie_insert(trie, "test"), "first insert should succeed");
    ASSERT_EQ(trie->size, 1, "size should be 1");
    
    ASSERT_TRUE(trie_insert(trie, "test"), "duplicate insert should succeed");
    ASSERT_EQ(trie->size, 1, "size should still be 1");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_insert_batch(void) {
    TEST_START("trie_insert_batch");
    
    Trie *trie = trie_create();
    const char *words[] = {"one", "two", "three", "four", "five"};
    
    size_t inserted = trie_insert_batch(trie, words, 5);
    ASSERT_EQ(inserted, 5, "all words should be inserted");
    ASSERT_EQ(trie->size, 5, "size should be 5");
    
    for (int i = 0; i < 5; i++) {
        ASSERT_TRUE(trie_search(trie, words[i]), "word should be found");
    }
    
    trie_destroy(trie);
    TEST_PASS();
}

/* ==================== Search Tests ==================== */

void test_search_existing(void) {
    TEST_START("trie_search existing word");
    
    Trie *trie = trie_create();
    trie_insert(trie, "hello");
    trie_insert(trie, "world");
    
    ASSERT_TRUE(trie_search(trie, "hello"), "hello should be found");
    ASSERT_TRUE(trie_search(trie, "world"), "world should be found");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_search_nonexistent(void) {
    TEST_START("trie_search nonexistent word");
    
    Trie *trie = trie_create();
    trie_insert(trie, "hello");
    
    ASSERT_FALSE(trie_search(trie, "hell"), "hell should not be found");
    ASSERT_FALSE(trie_search(trie, "helloo"), "helloo should not be found");
    ASSERT_FALSE(trie_search(trie, "world"), "world should not be found");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_search_prefix(void) {
    TEST_START("trie_search prefix only");
    
    Trie *trie = trie_create();
    trie_insert(trie, "application");
    
    ASSERT_FALSE(trie_search(trie, "app"), "prefix alone should not be found");
    ASSERT_TRUE(trie_search(trie, "application"), "full word should be found");
    
    trie_destroy(trie);
    TEST_PASS();
}

/* ==================== Delete Tests ==================== */

void test_delete_leaf(void) {
    TEST_START("trie_delete leaf word");
    
    Trie *trie = trie_create();
    trie_insert(trie, "hello");
    
    ASSERT_TRUE(trie_delete(trie, "hello"), "delete should succeed");
    ASSERT_EQ(trie->size, 0, "size should be 0");
    ASSERT_FALSE(trie_search(trie, "hello"), "word should not be found");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_delete_shared_prefix(void) {
    TEST_START("trie_delete word with shared prefix");
    
    Trie *trie = trie_create();
    trie_insert(trie, "app");
    trie_insert(trie, "apple");
    trie_insert(trie, "application");
    
    ASSERT_TRUE(trie_delete(trie, "apple"), "delete should succeed");
    ASSERT_EQ(trie->size, 2, "size should be 2");
    ASSERT_FALSE(trie_search(trie, "apple"), "apple should not be found");
    ASSERT_TRUE(trie_search(trie, "app"), "app should still exist");
    ASSERT_TRUE(trie_search(trie, "application"), "application should still exist");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_delete_nonexistent(void) {
    TEST_START("trie_delete nonexistent word");
    
    Trie *trie = trie_create();
    trie_insert(trie, "hello");
    
    ASSERT_FALSE(trie_delete(trie, "world"), "delete should fail for nonexistent");
    ASSERT_EQ(trie->size, 1, "size should still be 1");
    
    trie_destroy(trie);
    TEST_PASS();
}

/* ==================== Prefix Tests ==================== */

void test_starts_with(void) {
    TEST_START("trie_starts_with");
    
    Trie *trie = trie_create();
    trie_insert(trie, "apple");
    trie_insert(trie, "application");
    trie_insert(trie, "banana");
    
    ASSERT_TRUE(trie_starts_with(trie, "app"), "should have words starting with app");
    ASSERT_TRUE(trie_starts_with(trie, "ban"), "should have words starting with ban");
    ASSERT_FALSE(trie_starts_with(trie, "cat"), "should not have words starting with cat");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_count_prefix(void) {
    TEST_START("trie_count_prefix");
    
    Trie *trie = trie_create();
    trie_insert(trie, "app");
    trie_insert(trie, "apple");
    trie_insert(trie, "application");
    trie_insert(trie, "applied");
    trie_insert(trie, "banana");
    
    ASSERT_EQ(trie_count_prefix(trie, "app"), 4, "should count 4 words with prefix app");
    ASSERT_EQ(trie_count_prefix(trie, "ban"), 1, "should count 1 word with prefix ban");
    ASSERT_EQ(trie_count_prefix(trie, "xyz"), 0, "should count 0 words with prefix xyz");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_longest_common_prefix(void) {
    TEST_START("trie_longest_common_prefix");
    
    Trie *trie = trie_create();
    char buffer[256];
    
    trie_insert(trie, "apple");
    trie_insert(trie, "appetite");
    trie_insert(trie, "application");
    
    size_t len = trie_longest_common_prefix(trie, buffer, sizeof(buffer));
    ASSERT_EQ(len, 3, "common prefix length should be 3");
    ASSERT_STR_EQ(buffer, "app", "common prefix should be 'app'");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_longest_common_prefix_single(void) {
    TEST_START("trie_longest_common_prefix single word");
    
    Trie *trie = trie_create();
    char buffer[256];
    
    trie_insert(trie, "hello");
    
    size_t len = trie_longest_common_prefix(trie, buffer, sizeof(buffer));
    ASSERT_EQ(len, 0, "single word should have empty common prefix");
    
    trie_destroy(trie);
    TEST_PASS();
}

/* ==================== Autocomplete Tests ==================== */

void test_get_words_with_prefix(void) {
    TEST_START("trie_get_words_with_prefix");
    
    Trie *trie = trie_create();
    trie_insert(trie, "apple");
    trie_insert(trie, "appetite");
    trie_insert(trie, "application");
    trie_insert(trie, "apply");
    trie_insert(trie, "banana");
    
    TrieWordsResult result = trie_get_words_with_prefix(trie, "app", 0);
    ASSERT_EQ(result.count, 4, "should find 4 words starting with app");
    
    trie_free_words_result(&result);
    trie_destroy(trie);
    TEST_PASS();
}

void test_get_words_with_limit(void) {
    TEST_START("trie_get_words_with_prefix with limit");
    
    Trie *trie = trie_create();
    trie_insert(trie, "apple");
    trie_insert(trie, "appetite");
    trie_insert(trie, "application");
    trie_insert(trie, "apply");
    
    TrieWordsResult result = trie_get_words_with_prefix(trie, "app", 2);
    ASSERT_EQ(result.count, 2, "should find only 2 words with limit");
    
    trie_free_words_result(&result);
    trie_destroy(trie);
    TEST_PASS();
}

void test_get_all_words(void) {
    TEST_START("trie_get_all_words");
    
    Trie *trie = trie_create();
    trie_insert(trie, "one");
    trie_insert(trie, "two");
    trie_insert(trie, "three");
    
    TrieWordsResult result = trie_get_all_words(trie);
    ASSERT_EQ(result.count, 3, "should find all 3 words");
    
    trie_free_words_result(&result);
    trie_destroy(trie);
    TEST_PASS();
}

/* ==================== Pattern Match Tests ==================== */

void test_pattern_match_question(void) {
    TEST_START("trie_pattern_match with ?");
    
    Trie *trie = trie_create();
    trie_insert(trie, "cat");
    trie_insert(trie, "bat");
    trie_insert(trie, "rat");
    trie_insert(trie, "car");
    
    char *matches[10];
    size_t count = trie_pattern_match(trie, "?at", matches, 10);
    
    ASSERT_EQ(count, 3, "should match 3 words with ?at pattern");
    
    for (size_t i = 0; i < count; i++) {
        free(matches[i]);
    }
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_pattern_match_star(void) {
    TEST_START("trie_pattern_match with *");
    
    Trie *trie = trie_create();
    trie_insert(trie, "cat");
    trie_insert(trie, "car");
    trie_insert(trie, "care");
    trie_insert(trie, "cart");
    
    char *matches[10];
    size_t count = trie_pattern_match(trie, "ca*", matches, 10);
    
    ASSERT_TRUE(count >= 4, "should match at least 4 words with ca* pattern");
    
    for (size_t i = 0; i < count; i++) {
        free(matches[i]);
    }
    
    trie_destroy(trie);
    TEST_PASS();
}

/* ==================== Iterator Tests ==================== */

void test_iterator(void) {
    TEST_START("trie_iterator");
    
    Trie *trie = trie_create();
    trie_insert(trie, "apple");
    trie_insert(trie, "banana");
    trie_insert(trie, "cherry");
    
    TrieIterator iter;
    trie_iterator_init(trie, &iter);
    
    char buffer[256];
    int count = 0;
    
    while (trie_iterator_next(&iter, buffer, sizeof(buffer))) {
        count++;
    }
    
    ASSERT_EQ(count, 3, "iterator should yield 3 words");
    
    trie_destroy(trie);
    TEST_PASS();
}

/* ==================== Utility Tests ==================== */

void test_size_and_node_count(void) {
    TEST_START("trie_size and trie_node_count");
    
    Trie *trie = trie_create();
    
    ASSERT_EQ(trie_size(trie), 0, "empty trie size should be 0");
    ASSERT_EQ(trie_node_count(trie), 1, "empty trie should have 1 node (root)");
    
    trie_insert(trie, "abc");
    ASSERT_EQ(trie_size(trie), 1, "size should be 1");
    ASSERT_EQ(trie_node_count(trie), 4, "should have 4 nodes (root + a + b + c)");
    
    trie_insert(trie, "abd");
    ASSERT_EQ(trie_size(trie), 2, "size should be 2");
    ASSERT_EQ(trie_node_count(trie), 5, "should have 5 nodes (shared prefix)");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_clear(void) {
    TEST_START("trie_clear");
    
    Trie *trie = trie_create();
    trie_insert(trie, "one");
    trie_insert(trie, "two");
    trie_insert(trie, "three");
    
    trie_clear(trie);
    
    ASSERT_EQ(trie->size, 0, "size should be 0 after clear");
    ASSERT_TRUE(trie_is_empty(trie), "trie should be empty after clear");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_memory_usage(void) {
    TEST_START("trie_memory_usage");
    
    Trie *trie = trie_create();
    trie_insert(trie, "hello");
    
    size_t usage = trie_memory_usage(trie);
    ASSERT_TRUE(usage > 0, "memory usage should be positive");
    
    printf("(usage: %zu bytes) ", usage);
    
    trie_destroy(trie);
    TEST_PASS();
}

/* ==================== Edge Case Tests ==================== */

void test_null_handling(void) {
    TEST_START("null parameter handling");
    
    ASSERT_TRUE(trie_create() != NULL, "create should return valid trie");
    ASSERT_FALSE(trie_insert(NULL, "test"), "insert with NULL trie should fail");
    ASSERT_FALSE(trie_insert(trie_create(), NULL), "insert with NULL word should fail");
    ASSERT_FALSE(trie_search(NULL, "test"), "search with NULL trie should fail");
    ASSERT_FALSE(trie_delete(NULL, "test"), "delete with NULL trie should fail");
    ASSERT_EQ(trie_size(NULL), 0, "size of NULL trie should be 0");
    ASSERT_TRUE(trie_is_empty(NULL), "NULL trie should be empty");
    
    /* Clean up */
    Trie *trie = trie_create();
    trie_destroy(trie);
    
    TEST_PASS();
}

void test_empty_string(void) {
    TEST_START("empty string handling");
    
    Trie *trie = trie_create();
    
    ASSERT_FALSE(trie_insert(trie, ""), "insert empty string should fail");
    ASSERT_FALSE(trie_search(trie, ""), "search empty string should fail");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_unicode_ascii(void) {
    TEST_START("ASCII character handling");
    
    Trie *trie = trie_create();
    
    /* Test various ASCII characters */
    ASSERT_TRUE(trie_insert(trie, "Hello123!"), "alphanumeric should work");
    ASSERT_TRUE(trie_search(trie, "Hello123!"), "should find alphanumeric");
    
    ASSERT_TRUE(trie_insert(trie, "test@email.com"), "email should work");
    ASSERT_TRUE(trie_search(trie, "test@email.com"), "should find email");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_long_word(void) {
    TEST_START("long word handling");
    
    Trie *trie = trie_create();
    
    /* Create a word at max length */
    char long_word[TRIE_MAX_WORD_LENGTH];
    memset(long_word, 'a', TRIE_MAX_WORD_LENGTH - 1);
    long_word[TRIE_MAX_WORD_LENGTH - 1] = '\0';
    
    ASSERT_TRUE(trie_insert(trie, long_word), "should insert long word");
    ASSERT_TRUE(trie_search(trie, long_word), "should find long word");
    
    trie_destroy(trie);
    TEST_PASS();
}

void test_many_words(void) {
    TEST_START("many words handling");
    
    Trie *trie = trie_create();
    char word[20];
    const int count = 1000;
    
    /* Insert many numbered words */
    for (int i = 0; i < count; i++) {
        snprintf(word, sizeof(word), "word%d", i);
        ASSERT_TRUE(trie_insert(trie, word), "insert should succeed");
    }
    
    ASSERT_EQ(trie->size, (size_t)count, "size should match count");
    
    /* Verify all words exist */
    for (int i = 0; i < count; i++) {
        snprintf(word, sizeof(word), "word%d", i);
        ASSERT_TRUE(trie_search(trie, word), "word should be found");
    }
    
    trie_destroy(trie);
    TEST_PASS();
}

/* ==================== Main ==================== */

int main(void) {
    printf("\n=== Trie Unit Tests ===\n\n");
    
    /* Basic Tests */
    test_create_destroy();
    test_is_empty();
    
    /* Insert Tests */
    test_insert_single();
    test_insert_multiple();
    test_insert_duplicate();
    test_insert_batch();
    
    /* Search Tests */
    test_search_existing();
    test_search_nonexistent();
    test_search_prefix();
    
    /* Delete Tests */
    test_delete_leaf();
    test_delete_shared_prefix();
    test_delete_nonexistent();
    
    /* Prefix Tests */
    test_starts_with();
    test_count_prefix();
    test_longest_common_prefix();
    test_longest_common_prefix_single();
    
    /* Autocomplete Tests */
    test_get_words_with_prefix();
    test_get_words_with_limit();
    test_get_all_words();
    
    /* Pattern Match Tests */
    test_pattern_match_question();
    test_pattern_match_star();
    
    /* Iterator Tests */
    test_iterator();
    
    /* Utility Tests */
    test_size_and_node_count();
    test_clear();
    test_memory_usage();
    
    /* Edge Case Tests */
    test_null_handling();
    test_empty_string();
    test_unicode_ascii();
    test_long_word();
    test_many_words();
    
    /* Summary */
    printf("\n=== Test Summary ===\n");
    printf("Passed: %d/%d tests\n", tests_passed, tests_total);
    
    if (tests_passed == tests_total) {
        printf("\n✓ All tests passed!\n\n");
        return 0;
    } else {
        printf("\n✗ %d test(s) failed!\n\n", tests_total - tests_passed);
        return 1;
    }
}