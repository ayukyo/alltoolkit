/**
 * @file test_priority_queue.c
 * @brief Unit tests for Priority Queue (Min-Heap) Implementation
 * 
 * @author AllToolkit
 * @date 2026-04-23
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "priority_queue.h"

/* Test counters */
static int tests_run = 0;
static int tests_passed = 0;

#define TEST(name) do { \
    printf("  Testing: %s... ", #name); \
    tests_run++; \
    if (test_##name()) { \
        printf("PASSED\n"); \
        tests_passed++; \
    } else { \
        printf("FAILED\n"); \
    } \
} while(0)

/* Comparison function for integers */
static int cmp_int(const void *a, const void *b) {
    return *(const int *)a - *(const int *)b;
}

/* ========== Test Functions ========== */

int test_create_free(void) {
    PriorityQueue *pq = pq_create(sizeof(int), 0);
    if (pq == NULL) return 0;
    
    int result = (pq_size(pq) == 0) && 
                 (pq_is_empty(pq)) && 
                 (pq_capacity(pq) > 0);
    
    pq_free(&pq);
    return result && (pq == NULL);
}

int test_create_with_capacity(void) {
    PriorityQueue *pq = pq_create(sizeof(int), 100);
    if (pq == NULL) return 0;
    
    int result = (pq_capacity(pq) == 100) && (pq_size(pq) == 0);
    
    pq_free(&pq);
    return result;
}

int test_insert_extract_int(void) {
    PriorityQueue *pq = pq_create_int();
    if (pq == NULL) return 0;
    
    /* Insert in random order */
    pq_insert_int(pq, 30, 3.0);
    pq_insert_int(pq, 10, 1.0);
    pq_insert_int(pq, 20, 2.0);
    pq_insert_int(pq, 5, 0.5);
    
    if (pq_size(pq) != 4) {
        pq_free(&pq);
        return 0;
    }
    
    /* Extract in priority order */
    int val;
    double pri;
    
    pq_extract_int(pq, &val, &pri);
    if (val != 5 || pri != 0.5) {
        pq_free(&pq);
        return 0;
    }
    
    pq_extract_int(pq, &val, &pri);
    if (val != 10 || pri != 1.0) {
        pq_free(&pq);
        return 0;
    }
    
    pq_extract_int(pq, &val, &pri);
    if (val != 20 || pri != 2.0) {
        pq_free(&pq);
        return 0;
    }
    
    pq_extract_int(pq, &val, &pri);
    if (val != 30 || pri != 3.0) {
        pq_free(&pq);
        return 0;
    }
    
    int result = pq_is_empty(pq);
    pq_free(&pq);
    return result;
}

int test_peek(void) {
    PriorityQueue *pq = pq_create_int();
    if (pq == NULL) return 0;
    
    pq_insert_int(pq, 42, 2.0);
    pq_insert_int(pq, 99, 1.0);  /* Lower priority, should be at front */
    
    int val;
    double pri;
    if (!pq_peek_int(pq, &val, &pri) || val != 99 || pri != 1.0) {
        pq_free(&pq);
        return 0;
    }
    
    /* Peek should not remove element */
    if (pq_size(pq) != 2) {
        pq_free(&pq);
        return 0;
    }
    
    pq_free(&pq);
    return 1;
}

int test_same_priority(void) {
    PriorityQueue *pq = pq_create_int();
    if (pq == NULL) return 0;
    
    /* Insert elements with same priority */
    pq_insert_int(pq, 10, 1.0);
    pq_insert_int(pq, 20, 1.0);
    pq_insert_int(pq, 30, 1.0);
    
    /* All should be extractable */
    int val;
    int count = 0;
    while (!pq_is_empty(pq)) {
        pq_extract_int(pq, &val, NULL);
        count++;
    }
    
    pq_free(&pq);
    return count == 3;
}

int test_is_empty(void) {
    PriorityQueue *pq = pq_create_int();
    if (pq == NULL) return 0;
    
    if (!pq_is_empty(pq)) {
        pq_free(&pq);
        return 0;
    }
    
    pq_insert_int(pq, 1, 1.0);
    if (pq_is_empty(pq)) {
        pq_free(&pq);
        return 0;
    }
    
    int val;
    pq_extract_int(pq, &val, NULL);
    if (!pq_is_empty(pq)) {
        pq_free(&pq);
        return 0;
    }
    
    pq_free(&pq);
    return 1;
}

int test_clear(void) {
    PriorityQueue *pq = pq_create_int();
    if (pq == NULL) return 0;
    
    for (int i = 0; i < 100; i++) {
        pq_insert_int(pq, i, (double)i);
    }
    
    if (pq_size(pq) != 100) {
        pq_free(&pq);
        return 0;
    }
    
    pq_clear(pq);
    
    int result = (pq_size(pq) == 0) && pq_is_empty(pq);
    pq_free(&pq);
    return result;
}

int test_reserve(void) {
    PriorityQueue *pq = pq_create_int();
    if (pq == NULL) return 0;
    
    if (!pq_reserve(pq, 1000)) {
        pq_free(&pq);
        return 0;
    }
    
    if (pq_capacity(pq) != 1000) {
        pq_free(&pq);
        return 0;
    }
    
    /* Reserve smaller should not shrink */
    pq_reserve(pq, 500);
    if (pq_capacity(pq) != 1000) {
        pq_free(&pq);
        return 0;
    }
    
    pq_free(&pq);
    return 1;
}

int test_shrink_to_fit(void) {
    PriorityQueue *pq = pq_create_int();
    if (pq == NULL) return 0;
    
    pq_reserve(pq, 100);
    for (int i = 0; i < 10; i++) {
        pq_insert_int(pq, i, (double)i);
    }
    
    if (!pq_shrink_to_fit(pq)) {
        pq_free(&pq);
        return 0;
    }
    
    int result = (pq_capacity(pq) == 10) && (pq_size(pq) == 10);
    pq_free(&pq);
    return result;
}

int test_contains_priority(void) {
    PriorityQueue *pq = pq_create_int();
    if (pq == NULL) return 0;
    
    pq_insert_int(pq, 10, 1.0);
    pq_insert_int(pq, 20, 2.0);
    pq_insert_int(pq, 30, 3.0);
    
    if (!pq_contains_priority(pq, 1.0)) {
        pq_free(&pq);
        return 0;
    }
    
    if (!pq_contains_priority(pq, 2.0)) {
        pq_free(&pq);
        return 0;
    }
    
    if (pq_contains_priority(pq, 99.0)) {
        pq_free(&pq);
        return 0;
    }
    
    pq_free(&pq);
    return 1;
}

int test_update_priority(void) {
    PriorityQueue *pq = pq_create_int();
    if (pq == NULL) return 0;
    
    pq_insert_int(pq, 10, 3.0);
    pq_insert_int(pq, 20, 2.0);
    pq_insert_int(pq, 30, 1.0);
    
    /* Update priority of element 20 from 2.0 to 0.5 (should become min) */
    int target = 20;
    if (!pq_update_priority(pq, &target, 0.5, cmp_int)) {
        pq_free(&pq);
        return 0;
    }
    
    /* Verify 20 is now at front */
    int val;
    double pri;
    pq_peek_int(pq, &val, &pri);
    if (val != 20 || pri != 0.5) {
        pq_free(&pq);
        return 0;
    }
    
    pq_free(&pq);
    return 1;
}

int test_merge(void) {
    PriorityQueue *pq1 = pq_create_int();
    PriorityQueue *pq2 = pq_create_int();
    if (pq1 == NULL || pq2 == NULL) {
        if (pq1) pq_free(&pq1);
        if (pq2) pq_free(&pq2);
        return 0;
    }
    
    pq_insert_int(pq1, 10, 1.0);
    pq_insert_int(pq1, 30, 3.0);
    
    pq_insert_int(pq2, 20, 2.0);
    pq_insert_int(pq2, 40, 4.0);
    
    if (!pq_merge(pq1, pq2)) {
        pq_free(&pq1);
        pq_free(&pq2);
        return 0;
    }
    
    if (pq_size(pq1) != 4) {
        pq_free(&pq1);
        pq_free(&pq2);
        return 0;
    }
    
    /* Extract should be in sorted order */
    int val;
    double pri;
    pq_extract_int(pq1, &val, &pri);
    if (val != 10 || pri != 1.0) {
        pq_free(&pq1);
        pq_free(&pq2);
        return 0;
    }
    
    pq_extract_int(pq1, &val, &pri);
    if (val != 20 || pri != 2.0) {
        pq_free(&pq1);
        pq_free(&pq2);
        return 0;
    }
    
    pq_free(&pq1);
    pq_free(&pq2);
    return 1;
}

int test_get_sorted(void) {
    PriorityQueue *pq = pq_create_int();
    if (pq == NULL) return 0;
    
    pq_insert_int(pq, 30, 3.0);
    pq_insert_int(pq, 10, 1.0);
    pq_insert_int(pq, 20, 2.0);
    pq_insert_int(pq, 5, 0.5);
    
    int sorted[4];
    double priorities[4];
    
    if (!pq_get_sorted(pq, sorted, priorities)) {
        pq_free(&pq);
        return 0;
    }
    
    /* Verify sorted order */
    if (sorted[0] != 5 || priorities[0] != 0.5) {
        pq_free(&pq);
        return 0;
    }
    if (sorted[1] != 10 || priorities[1] != 1.0) {
        pq_free(&pq);
        return 0;
    }
    if (sorted[2] != 20 || priorities[2] != 2.0) {
        pq_free(&pq);
        return 0;
    }
    if (sorted[3] != 30 || priorities[3] != 3.0) {
        pq_free(&pq);
        return 0;
    }
    
    /* Original queue should be unchanged */
    if (pq_size(pq) != 4) {
        pq_free(&pq);
        return 0;
    }
    
    pq_free(&pq);
    return 1;
}

int test_double_type(void) {
    PriorityQueue *pq = pq_create_double();
    if (pq == NULL) return 0;
    
    pq_insert_double(pq, 3.14, 3.0);
    pq_insert_double(pq, 1.41, 1.0);
    pq_insert_double(pq, 2.71, 2.0);
    
    double val;
    double pri;
    
    pq_extract_double(pq, &val, &pri);
    if (val < 1.40 || val > 1.42 || pri != 1.0) {
        pq_free(&pq);
        return 0;
    }
    
    pq_extract_double(pq, &val, &pri);
    if (val < 2.70 || val > 2.72 || pri != 2.0) {
        pq_free(&pq);
        return 0;
    }
    
    pq_free(&pq);
    return 1;
}

int test_char_type(void) {
    PriorityQueue *pq = pq_create_char();
    if (pq == NULL) return 0;
    
    /* Insert characters with priorities */
    pq_insert_char(pq, 'c', 3.0);
    pq_insert_char(pq, 'a', 1.0);
    pq_insert_char(pq, 'b', 2.0);
    
    char val;
    pq_extract_char(pq, &val, NULL);
    if (val != 'a') {
        pq_free(&pq);
        return 0;
    }
    
    pq_extract_char(pq, &val, NULL);
    if (val != 'b') {
        pq_free(&pq);
        return 0;
    }
    
    pq_extract_char(pq, &val, NULL);
    if (val != 'c') {
        pq_free(&pq);
        return 0;
    }
    
    pq_free(&pq);
    return 1;
}

int test_large_queue(void) {
    PriorityQueue *pq = pq_create_int();
    if (pq == NULL) return 0;
    
    /* Insert 10000 elements in reverse priority order */
    for (int i = 9999; i >= 0; i--) {
        pq_insert_int(pq, i, (double)i);
    }
    
    if (pq_size(pq) != 10000) {
        pq_free(&pq);
        return 0;
    }
    
    /* Extract should be in ascending priority order */
    for (int i = 0; i < 10000; i++) {
        int val;
        double pri;
        if (!pq_extract_int(pq, &val, &pri) || val != i || pri != (double)i) {
            pq_free(&pq);
            return 0;
        }
    }
    
    int result = pq_is_empty(pq);
    pq_free(&pq);
    return result;
}

int test_null_handling(void) {
    /* These should not crash */
    pq_free(NULL);
    
    PriorityQueue *pq = NULL;
    pq_free(&pq);
    
    int val;
    double pri;
    if (pq_extract_min(NULL, &val, &pri)) return 0;
    if (pq_insert(NULL, &val, 1.0)) return 0;
    if (pq_peek_min(NULL, &val, &pri)) return 0;
    if (pq_size(NULL) != 0) return 0;
    if (!pq_is_empty(NULL)) return 0;
    
    pq = pq_create(sizeof(int), 0);
    if (pq == NULL) return 0;
    
    /* Insert with NULL data should fail */
    if (pq_insert(pq, NULL, 1.0)) {
        pq_free(&pq);
        return 0;
    }
    
    pq_free(&pq);
    return 1;
}

int test_extract_without_output(void) {
    PriorityQueue *pq = pq_create_int();
    if (pq == NULL) return 0;
    
    pq_insert_int(pq, 1, 1.0);
    pq_insert_int(pq, 2, 2.0);
    pq_insert_int(pq, 3, 3.0);
    
    /* Extract without storing */
    if (!pq_extract_min(pq, NULL, NULL) || pq_size(pq) != 2) {
        pq_free(&pq);
        return 0;
    }
    
    /* Next should be priority 2.0 */
    int val;
    double pri;
    pq_extract_int(pq, &val, &pri);
    if (val != 2 || pri != 2.0) {
        pq_free(&pq);
        return 0;
    }
    
    pq_free(&pq);
    return 1;
}

int test_struct_type(void) {
    typedef struct {
        int x;
        int y;
    } Point;
    
    PriorityQueue *pq = pq_create(sizeof(Point), 0);
    if (pq == NULL) return 0;
    
    Point p1 = {10, 20};
    Point p2 = {30, 40};
    Point p3 = {50, 60};
    
    pq_insert(pq, &p1, 3.0);
    pq_insert(pq, &p2, 1.0);  /* Highest priority */
    pq_insert(pq, &p3, 2.0);
    
    Point out;
    pq_extract_min(pq, &out, NULL);
    if (out.x != 30 || out.y != 40) {
        pq_free(&pq);
        return 0;
    }
    
    pq_extract_min(pq, &out, NULL);
    if (out.x != 50 || out.y != 60) {
        pq_free(&pq);
        return 0;
    }
    
    pq_extract_min(pq, &out, NULL);
    if (out.x != 10 || out.y != 20) {
        pq_free(&pq);
        return 0;
    }
    
    pq_free(&pq);
    return 1;
}

int test_negative_priority(void) {
    PriorityQueue *pq = pq_create_int();
    if (pq == NULL) return 0;
    
    pq_insert_int(pq, 10, 1.0);
    pq_insert_int(pq, -10, -1.0);
    pq_insert_int(pq, 0, 0.0);
    
    int val;
    double pri;
    
    pq_extract_int(pq, &val, &pri);
    if (val != -10 || pri != -1.0) {
        pq_free(&pq);
        return 0;
    }
    
    pq_extract_int(pq, &val, &pri);
    if (val != 0 || pri != 0.0) {
        pq_free(&pq);
        return 0;
    }
    
    pq_extract_int(pq, &val, &pri);
    if (val != 10 || pri != 1.0) {
        pq_free(&pq);
        return 0;
    }
    
    pq_free(&pq);
    return 1;
}

int test_priority_stability(void) {
    /* Test that heap property is maintained after many operations */
    PriorityQueue *pq = pq_create_int();
    if (pq == NULL) return 0;
    
    /* Insert many elements */
    for (int i = 0; i < 100; i++) {
        pq_insert_int(pq, i, (double)(rand() % 1000));
    }
    
    /* Extract all and verify min-heap property */
    double last_priority = -1.0;
    while (!pq_is_empty(pq)) {
        int val;
        double pri;
        pq_extract_int(pq, &val, &pri);
        if (pri < last_priority) {
            pq_free(&pq);
            return 0;  /* Priority order violated */
        }
        last_priority = pri;
    }
    
    pq_free(&pq);
    return 1;
}

/* ========== Main ========== */

int main(void) {
    printf("\n========================================\n");
    printf("  Priority Queue Utils Test Suite\n");
    printf("========================================\n\n");
    
    /* Basic operations */
    TEST(create_free);
    TEST(create_with_capacity);
    TEST(insert_extract_int);
    TEST(peek);
    TEST(same_priority);
    TEST(is_empty);
    TEST(clear);
    
    /* Memory management */
    TEST(reserve);
    TEST(shrink_to_fit);
    
    /* Advanced operations */
    TEST(contains_priority);
    TEST(update_priority);
    TEST(merge);
    TEST(get_sorted);
    
    /* Different types */
    TEST(double_type);
    TEST(char_type);
    TEST(struct_type);
    
    /* Edge cases */
    TEST(negative_priority);
    TEST(priority_stability);
    TEST(null_handling);
    TEST(extract_without_output);
    
    /* Stress test */
    TEST(large_queue);
    
    printf("\n========================================\n");
    printf("  Results: %d/%d tests passed\n", tests_passed, tests_run);
    printf("========================================\n\n");
    
    return (tests_passed == tests_run) ? 0 : 1;
}