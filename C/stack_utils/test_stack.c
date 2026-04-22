/**
 * @file test_stack.c
 * @brief Unit tests for Stack Data Structure
 * 
 * @author AllToolkit
 * @date 2026-04-22
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "stack.h"

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

/* ========== Test Functions ========== */

int test_create_free(void) {
    Stack *stack = stack_create(sizeof(int), 0);
    if (stack == NULL) return 0;
    
    int result = (stack_size(stack) == 0) && 
                 (stack_is_empty(stack)) && 
                 (stack_capacity(stack) > 0);
    
    stack_free(&stack);
    return result && (stack == NULL);
}

int test_create_with_capacity(void) {
    Stack *stack = stack_create(sizeof(int), 100);
    if (stack == NULL) return 0;
    
    int result = (stack_capacity(stack) == 100) && (stack_size(stack) == 0);
    
    stack_free(&stack);
    return result;
}

int test_push_pop_int(void) {
    Stack *stack = stack_create_int();
    if (stack == NULL) return 0;
    
    stack_push_int(stack, 10);
    stack_push_int(stack, 20);
    stack_push_int(stack, 30);
    
    if (stack_size(stack) != 3) {
        stack_free(&stack);
        return 0;
    }
    
    int val;
    stack_pop_int(stack, &val);
    if (val != 30) {
        stack_free(&stack);
        return 0;
    }
    
    stack_pop_int(stack, &val);
    if (val != 20) {
        stack_free(&stack);
        return 0;
    }
    
    stack_pop_int(stack, &val);
    if (val != 10) {
        stack_free(&stack);
        return 0;
    }
    
    int result = stack_is_empty(stack);
    stack_free(&stack);
    return result;
}

int test_peek(void) {
    Stack *stack = stack_create_int();
    if (stack == NULL) return 0;
    
    stack_push_int(stack, 42);
    stack_push_int(stack, 99);
    
    int val;
    if (!stack_peek_int(stack, &val) || val != 99) {
        stack_free(&stack);
        return 0;
    }
    
    /* Peek should not remove element */
    if (stack_size(stack) != 2) {
        stack_free(&stack);
        return 0;
    }
    
    stack_free(&stack);
    return 1;
}

int test_is_empty(void) {
    Stack *stack = stack_create_int();
    if (stack == NULL) return 0;
    
    if (!stack_is_empty(stack)) {
        stack_free(&stack);
        return 0;
    }
    
    stack_push_int(stack, 1);
    if (stack_is_empty(stack)) {
        stack_free(&stack);
        return 0;
    }
    
    int val;
    stack_pop_int(stack, &val);
    if (!stack_is_empty(stack)) {
        stack_free(&stack);
        return 0;
    }
    
    stack_free(&stack);
    return 1;
}

int test_clear(void) {
    Stack *stack = stack_create_int();
    if (stack == NULL) return 0;
    
    for (int i = 0; i < 100; i++) {
        stack_push_int(stack, i);
    }
    
    if (stack_size(stack) != 100) {
        stack_free(&stack);
        return 0;
    }
    
    stack_clear(stack);
    
    int result = (stack_size(stack) == 0) && stack_is_empty(stack);
    stack_free(&stack);
    return result;
}

int test_reserve(void) {
    Stack *stack = stack_create_int();
    if (stack == NULL) return 0;
    
    if (!stack_reserve(stack, 1000)) {
        stack_free(&stack);
        return 0;
    }
    
    if (stack_capacity(stack) != 1000) {
        stack_free(&stack);
        return 0;
    }
    
    /* Reserve smaller should not shrink */
    stack_reserve(stack, 500);
    if (stack_capacity(stack) != 1000) {
        stack_free(&stack);
        return 0;
    }
    
    stack_free(&stack);
    return 1;
}

int test_shrink_to_fit(void) {
    Stack *stack = stack_create_int();
    if (stack == NULL) return 0;
    
    stack_reserve(stack, 100);
    for (int i = 0; i < 10; i++) {
        stack_push_int(stack, i);
    }
    
    if (!stack_shrink_to_fit(stack)) {
        stack_free(&stack);
        return 0;
    }
    
    int result = (stack_capacity(stack) == 10) && (stack_size(stack) == 10);
    stack_free(&stack);
    return result;
}

int test_copy(void) {
    Stack *stack = stack_create_int();
    if (stack == NULL) return 0;
    
    for (int i = 0; i < 10; i++) {
        stack_push_int(stack, i);
    }
    
    Stack *copy = stack_copy(stack);
    if (copy == NULL) {
        stack_free(&stack);
        return 0;
    }
    
    if (stack_size(copy) != 10) {
        stack_free(&stack);
        stack_free(&copy);
        return 0;
    }
    
    /* Verify contents */
    for (int i = 9; i >= 0; i--) {
        int val1, val2;
        stack_pop_int(stack, &val1);
        stack_pop_int(copy, &val2);
        if (val1 != val2 || val1 != i) {
            stack_free(&stack);
            stack_free(&copy);
            return 0;
        }
    }
    
    stack_free(&stack);
    stack_free(&copy);
    return 1;
}

int test_reverse(void) {
    Stack *stack = stack_create_int();
    if (stack == NULL) return 0;
    
    /* Push 1, 2, 3 -> stack is [1, 2, 3] with 3 on top */
    stack_push_int(stack, 1);
    stack_push_int(stack, 2);
    stack_push_int(stack, 3);
    
    stack_reverse(stack);
    
    /* After reverse: [3, 2, 1] with 1 on top */
    int val;
    stack_pop_int(stack, &val);
    if (val != 1) {
        stack_free(&stack);
        return 0;
    }
    
    stack_pop_int(stack, &val);
    if (val != 2) {
        stack_free(&stack);
        return 0;
    }
    
    stack_pop_int(stack, &val);
    if (val != 3) {
        stack_free(&stack);
        return 0;
    }
    
    stack_free(&stack);
    return 1;
}

int test_at(void) {
    Stack *stack = stack_create_int();
    if (stack == NULL) return 0;
    
    stack_push_int(stack, 10);
    stack_push_int(stack, 20);
    stack_push_int(stack, 30);
    /* Stack: [10, 20, 30], top is 30 */
    
    int val;
    if (!stack_at(stack, 0, &val) || val != 30) {
        stack_free(&stack);
        return 0;
    }
    
    if (!stack_at(stack, 1, &val) || val != 20) {
        stack_free(&stack);
        return 0;
    }
    
    if (!stack_at(stack, 2, &val) || val != 10) {
        stack_free(&stack);
        return 0;
    }
    
    /* Out of bounds should fail */
    if (stack_at(stack, 3, &val)) {
        stack_free(&stack);
        return 0;
    }
    
    stack_free(&stack);
    return 1;
}

int test_double_type(void) {
    Stack *stack = stack_create_double();
    if (stack == NULL) return 0;
    
    stack_push_double(stack, 3.14);
    stack_push_double(stack, 2.71);
    stack_push_double(stack, 1.41);
    
    double val;
    stack_pop_double(stack, &val);
    if (val < 1.40 || val > 1.42) {
        stack_free(&stack);
        return 0;
    }
    
    stack_pop_double(stack, &val);
    if (val < 2.70 || val > 2.72) {
        stack_free(&stack);
        return 0;
    }
    
    stack_pop_double(stack, &val);
    if (val < 3.13 || val > 3.15) {
        stack_free(&stack);
        return 0;
    }
    
    stack_free(&stack);
    return 1;
}

int test_char_type(void) {
    Stack *stack = stack_create_char();
    if (stack == NULL) return 0;
    
    const char *str = "hello";
    for (int i = 0; str[i] != '\0'; i++) {
        stack_push_char(stack, str[i]);
    }
    
    char val;
    char reversed[6];
    int idx = 0;
    while (!stack_is_empty(stack)) {
        stack_pop_char(stack, &val);
        reversed[idx++] = val;
    }
    reversed[idx] = '\0';
    
    int result = strcmp(reversed, "olleh") == 0;
    stack_free(&stack);
    return result;
}

int test_large_stack(void) {
    Stack *stack = stack_create_int();
    if (stack == NULL) return 0;
    
    /* Push 10000 elements */
    for (int i = 0; i < 10000; i++) {
        stack_push_int(stack, i);
    }
    
    if (stack_size(stack) != 10000) {
        stack_free(&stack);
        return 0;
    }
    
    /* Pop and verify */
    for (int i = 9999; i >= 0; i--) {
        int val;
        if (!stack_pop_int(stack, &val) || val != i) {
            stack_free(&stack);
            return 0;
        }
    }
    
    int result = stack_is_empty(stack);
    stack_free(&stack);
    return result;
}

int test_null_handling(void) {
    /* These should not crash */
    stack_free(NULL);
    
    Stack *stack = NULL;
    stack_free(&stack);
    
    int val;
    if (stack_pop(NULL, &val)) return 0;
    if (stack_push(NULL, &val)) return 0;
    if (stack_peek(NULL, &val)) return 0;
    if (stack_size(NULL) != 0) return 0;
    if (!stack_is_empty(NULL)) return 0;
    
    stack = stack_create(sizeof(int), 0);
    if (stack == NULL) return 0;
    
    /* Push with NULL element should fail */
    if (stack_push(stack, NULL)) {
        stack_free(&stack);
        return 0;
    }
    
    stack_free(&stack);
    return 1;
}

int test_pop_without_output(void) {
    Stack *stack = stack_create_int();
    if (stack == NULL) return 0;
    
    stack_push_int(stack, 1);
    stack_push_int(stack, 2);
    stack_push_int(stack, 3);
    
    /* Pop without storing */
    if (!stack_pop(stack, NULL) || stack_size(stack) != 2) {
        stack_free(&stack);
        return 0;
    }
    
    int val;
    stack_pop_int(stack, &val);
    if (val != 2) {
        stack_free(&stack);
        return 0;
    }
    
    stack_free(&stack);
    return 1;
}

int test_struct_type(void) {
    typedef struct {
        int x;
        int y;
    } Point;
    
    Stack *stack = stack_create(sizeof(Point), 0);
    if (stack == NULL) return 0;
    
    Point p1 = {10, 20};
    Point p2 = {30, 40};
    Point p3 = {50, 60};
    
    stack_push(stack, &p1);
    stack_push(stack, &p2);
    stack_push(stack, &p3);
    
    Point out;
    stack_pop(stack, &out);
    if (out.x != 50 || out.y != 60) {
        stack_free(&stack);
        return 0;
    }
    
    stack_pop(stack, &out);
    if (out.x != 30 || out.y != 40) {
        stack_free(&stack);
        return 0;
    }
    
    stack_pop(stack, &out);
    if (out.x != 10 || out.y != 20) {
        stack_free(&stack);
        return 0;
    }
    
    stack_free(&stack);
    return 1;
}

/* ========== Main ========== */

int main(void) {
    printf("\n========================================\n");
    printf("  Stack Utils Test Suite\n");
    printf("========================================\n\n");
    
    /* Basic operations */
    TEST(create_free);
    TEST(create_with_capacity);
    TEST(push_pop_int);
    TEST(peek);
    TEST(is_empty);
    TEST(clear);
    
    /* Memory management */
    TEST(reserve);
    TEST(shrink_to_fit);
    TEST(copy);
    
    /* Advanced operations */
    TEST(reverse);
    TEST(at);
    
    /* Different types */
    TEST(double_type);
    TEST(char_type);
    TEST(struct_type);
    
    /* Stress test */
    TEST(large_stack);
    
    /* Edge cases */
    TEST(null_handling);
    TEST(pop_without_output);
    
    printf("\n========================================\n");
    printf("  Results: %d/%d tests passed\n", tests_passed, tests_run);
    printf("========================================\n\n");
    
    return (tests_passed == tests_run) ? 0 : 1;
}