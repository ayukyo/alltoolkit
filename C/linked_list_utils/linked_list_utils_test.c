/**
 * @file linked_list_utils_test.c
 * @brief 双向链表工具库测试
 * @author AllToolkit
 * @date 2026-04-20
 */

#include "linked_list_utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

/* 测试计数 */
static int tests_passed = 0;
static int tests_failed = 0;

#define TEST(name) printf("  Testing: %s... ", name)
#define PASS() do { printf("✓\n"); tests_passed++; } while(0)
#define FAIL(msg) do { printf("✗ (%s)\n", msg); tests_failed++; } while(0)
#define ASSERT(cond, msg) do { if (cond) { PASS(); } else { FAIL(msg); } } while(0)

/* ==================== 整数链表测试 ==================== */

void test_int_list_create_destroy(void) {
    printf("\n=== Integer List: Create & Destroy ===\n");
    
    LinkedList* list = list_create_int();
    TEST("Create integer list");
    ASSERT(list != NULL, "list should not be NULL");
    
    TEST("List is empty");
    ASSERT(list_is_empty(list), "list should be empty");
    
    TEST("List size is 0");
    ASSERT(list_size(list) == 0, "size should be 0");
    
    TEST("List type is INT");
    ASSERT(list_get_type(list) == LIST_TYPE_INT, "type should be LIST_TYPE_INT");
    
    list_destroy(list);
    PASS();
}

void test_int_list_push_pop(void) {
    printf("\n=== Integer List: Push & Pop ===\n");
    
    LinkedList* list = list_create_int();
    
    TEST("Push front 10");
    ASSERT(list_push_front(list, 10), "push_front should succeed");
    
    TEST("Push front 20");
    ASSERT(list_push_front(list, 20), "push_front should succeed");
    
    TEST("Push back 30");
    ASSERT(list_push_back(list, 30), "push_back should succeed");
    
    TEST("List size is 3");
    ASSERT(list_size(list) == 3, "size should be 3");
    
    /* Should be: 20, 10, 30 */
    int val;
    TEST("Get element at index 0 is 20");
    list_get_int(list, 0, &val);
    ASSERT(val == 20, "index 0 should be 20");
    
    TEST("Get element at index 1 is 10");
    list_get_int(list, 1, &val);
    ASSERT(val == 10, "index 1 should be 10");
    
    TEST("Get element at index 2 is 30");
    list_get_int(list, 2, &val);
    ASSERT(val == 30, "index 2 should be 30");
    
    TEST("Pop front");
    ASSERT(list_pop_front(list), "pop_front should succeed");
    
    TEST("List size is 2 after pop");
    ASSERT(list_size(list) == 2, "size should be 2");
    
    list_get_int(list, 0, &val);
    TEST("First element is now 10");
    ASSERT(val == 10, "first element should be 10");
    
    TEST("Pop back");
    ASSERT(list_pop_back(list), "pop_back should succeed");
    
    TEST("List size is 1 after pop back");
    ASSERT(list_size(list) == 1, "size should be 1");
    
    list_destroy(list);
}

void test_int_list_find(void) {
    printf("\n=== Integer List: Find ===\n");
    
    LinkedList* list = list_create_int();
    list_push_back(list, 10);
    list_push_back(list, 20);
    list_push_back(list, 30);
    list_push_back(list, 20);
    
    TEST("Find 20 returns index 1");
    ASSERT(list_find_int(list, 20) == 1, "should find at index 1");
    
    TEST("Find 10 returns index 0");
    ASSERT(list_find_int(list, 10) == 0, "should find at index 0");
    
    TEST("Find 99 returns -1");
    ASSERT(list_find_int(list, 99) == -1, "should not find 99");
    
    TEST("Contains 30 is true");
    ASSERT(list_contains_int(list, 30), "should contain 30");
    
    TEST("Contains 99 is false");
    ASSERT(!list_contains_int(list, 99), "should not contain 99");
    
    list_destroy(list);
}

void test_int_list_remove(void) {
    printf("\n=== Integer List: Remove ===\n");
    
    LinkedList* list = list_create_int();
    list_push_back(list, 10);
    list_push_back(list, 20);
    list_push_back(list, 30);
    list_push_back(list, 20);
    list_push_back(list, 40);
    
    /* [10, 20, 30, 20, 40] */
    
    TEST("Remove at index 2 (value 30)");
    ASSERT(list_remove_at(list, 2), "remove_at should succeed");
    
    int val;
    list_get_int(list, 2, &val);
    TEST("Element at index 2 is now 20");
    ASSERT(val == 20, "index 2 should be 20");
    
    /* Now: [10, 20, 20, 40] */
    
    TEST("Remove first occurrence of 20");
    ASSERT(list_remove_int(list, 20), "remove_int should succeed");
    
    /* Now: [10, 20, 40] - removed 20 at index 1 */
    
    list_get_int(list, 1, &val);
    TEST("Element at index 1 is now 20");
    ASSERT(val == 20, "index 1 should be 20");
    
    /* Add some 10s for testing remove_all */
    list_push_back(list, 10);
    list_push_back(list, 10);
    /* [10, 20, 40, 10, 10] */
    
    TEST("Remove all 10s");
    size_t count = list_remove_all_int(list, 10);
    ASSERT(count == 3, "should remove 3 occurrences");
    
    TEST("List size is 2");
    ASSERT(list_size(list) == 2, "size should be 2");
    
    /* Final: [20, 40] */
    list_get_int(list, 0, &val);
    TEST("First element is 20");
    ASSERT(val == 20, "first should be 20");
    
    list_destroy(list);
}

void test_int_list_insert(void) {
    printf("\n=== Integer List: Insert ===\n");
    
    LinkedList* list = list_create_int();
    list_push_back(list, 10);
    list_push_back(list, 30);
    /* [10, 30] */
    
    TEST("Insert 20 at index 1");
    ASSERT(list_insert_at(list, 1, 20), "insert_at should succeed");
    
    int val;
    list_get_int(list, 1, &val);
    TEST("Element at index 1 is 20");
    ASSERT(val == 20, "index 1 should be 20");
    
    list_get_int(list, 2, &val);
    TEST("Element at index 2 is 30");
    ASSERT(val == 30, "index 2 should be 30");
    
    list_destroy(list);
}

void test_int_list_reverse(void) {
    printf("\n=== Integer List: Reverse ===\n");
    
    LinkedList* list = list_create_int();
    list_push_back(list, 1);
    list_push_back(list, 2);
    list_push_back(list, 3);
    list_push_back(list, 4);
    /* [1, 2, 3, 4] */
    
    TEST("Reverse list");
    list_reverse(list);
    
    int val;
    list_get_int(list, 0, &val);
    TEST("First element is 4");
    ASSERT(val == 4, "first should be 4");
    
    list_get_int(list, 3, &val);
    TEST("Last element is 1");
    ASSERT(val == 1, "last should be 1");
    
    list_destroy(list);
}

void test_int_list_sort(void) {
    printf("\n=== Integer List: Sort ===\n");
    
    LinkedList* list = list_create_int();
    list_push_back(list, 30);
    list_push_back(list, 10);
    list_push_back(list, 40);
    list_push_back(list, 20);
    list_push_back(list, 50);
    /* [30, 10, 40, 20, 50] */
    
    TEST("Sort list");
    list_sort(list);
    
    int val;
    list_get_int(list, 0, &val);
    TEST("First element is 10");
    ASSERT(val == 10, "first should be 10");
    
    list_get_int(list, 4, &val);
    TEST("Last element is 50");
    ASSERT(val == 50, "last should be 50");
    
    list_destroy(list);
}

void test_int_list_unique(void) {
    printf("\n=== Integer List: Unique ===\n");
    
    LinkedList* list = list_create_int();
    list_push_back(list, 1);
    list_push_back(list, 1);
    list_push_back(list, 2);
    list_push_back(list, 3);
    list_push_back(list, 3);
    list_push_back(list, 3);
    list_push_back(list, 4);
    /* [1, 1, 2, 3, 3, 3, 4] */
    
    TEST("Remove duplicates");
    list_unique(list);
    
    TEST("List size is 4");
    ASSERT(list_size(list) == 4, "size should be 4");
    
    int val;
    list_get_int(list, 0, &val);
    TEST("First element is 1");
    ASSERT(val == 1, "first should be 1");
    
    list_get_int(list, 3, &val);
    TEST("Last element is 4");
    ASSERT(val == 4, "last should be 4");
    
    list_destroy(list);
}

void test_int_list_clone(void) {
    printf("\n=== Integer List: Clone ===\n");
    
    LinkedList* list = list_create_int();
    list_push_back(list, 10);
    list_push_back(list, 20);
    list_push_back(list, 30);
    
    TEST("Clone list");
    LinkedList* clone = list_clone(list);
    ASSERT(clone != NULL, "clone should not be NULL");
    
    TEST("Clone size matches");
    ASSERT(list_size(clone) == list_size(list), "sizes should match");
    
    int val1, val2;
    for (size_t i = 0; i < list_size(list); i++) {
        list_get_int(list, i, &val1);
        list_get_int(clone, i, &val2);
        if (val1 != val2) {
            FAIL("values should match");
            break;
        }
    }
    PASS();
    
    TEST("Modify original does not affect clone");
    list_pop_front(list);
    ASSERT(list_size(list) == 2 && list_size(clone) == 3, "sizes should differ");
    
    list_destroy(list);
    list_destroy(clone);
}

/* ==================== 字符串链表测试 ==================== */

void test_string_list(void) {
    printf("\n=== String List: Operations ===\n");
    
    LinkedList* list = list_create_string();
    
    TEST("Create string list");
    ASSERT(list != NULL && list_get_type(list) == LIST_TYPE_STRING, "should be string type");
    
    TEST("Push front 'hello'");
    ASSERT(list_push_front(list, "hello"), "push should succeed");
    
    TEST("Push back 'world'");
    ASSERT(list_push_back(list, "world"), "push should succeed");
    
    TEST("Push back NULL");
    ASSERT(list_push_back(list, NULL), "push NULL should succeed");
    
    TEST("List size is 3");
    ASSERT(list_size(list) == 3, "size should be 3");
    
    const char* str;
    TEST("Get first string 'hello'");
    list_get_string(list, 0, &str);
    ASSERT(strcmp(str, "hello") == 0, "should be 'hello'");
    
    TEST("Find 'world' at index 1");
    ASSERT(list_find_string(list, "world") == 1, "should find at index 1");
    
    TEST("Find NULL at index 2");
    ASSERT(list_find_string(list, NULL) == 2, "should find NULL at index 2");
    
    TEST("Contains 'hello'");
    ASSERT(list_contains_string(list, "hello"), "should contain 'hello'");
    
    TEST("Remove 'world'");
    ASSERT(list_remove_string(list, "world"), "remove should succeed");
    
    TEST("List size is 2");
    ASSERT(list_size(list) == 2, "size should be 2");
    
    list_destroy(list);
}

/* ==================== 双精度链表测试 ==================== */

void test_double_list(void) {
    printf("\n=== Double List: Operations ===\n");
    
    LinkedList* list = list_create_double();
    
    TEST("Create double list");
    ASSERT(list != NULL && list_get_type(list) == LIST_TYPE_DOUBLE, "should be double type");
    
    list_push_back(list, 1.5);
    list_push_back(list, 2.7);
    list_push_back(list, 3.14);
    
    TEST("List size is 3");
    ASSERT(list_size(list) == 3, "size should be 3");
    
    double val;
    TEST("Get first element 1.5");
    list_get_double(list, 0, &val);
    ASSERT(val == 1.5, "should be 1.5");
    
    TEST("Find 3.14");
    ASSERT(list_find_double(list, 3.14, 0.001) == 2, "should find 3.14");
    
    TEST("Find 3.15 (not found)");
    ASSERT(list_find_double(list, 3.15, 0.001) == -1, "should not find 3.15");
    
    list_destroy(list);
}

/* ==================== 迭代器测试 ==================== */

void test_iterator(void) {
    printf("\n=== Iterator: Forward & Reverse ===\n");
    
    LinkedList* list = list_create_int();
    for (int i = 1; i <= 5; i++) {
        list_push_back(list, i);
    }
    /* [1, 2, 3, 4, 5] */
    
    printf("  Forward iteration: ");
    ListIterator it = list_iterator(list);
    int expected = 1;
    bool correct = true;
    do {
        if (list_iterator_get_int(&it) != expected) {
            correct = false;
            break;
        }
        expected++;
    } while (list_iterator_next(&it));
    TEST("All elements in order");
    ASSERT(correct && expected == 6, "forward iteration should work");
    
    printf("  Reverse iteration: ");
    it = list_iterator_reverse(list);
    expected = 5;
    correct = true;
    do {
        if (list_iterator_get_int(&it) != expected) {
            correct = false;
            break;
        }
        expected--;
    } while (list_iterator_next(&it));
    TEST("All elements in reverse order");
    ASSERT(correct && expected == 0, "reverse iteration should work");
    
    list_destroy(list);
}

/* Fold helper function */
static int fold_sum(int acc, int val, void* user_data) {
    (void)user_data;
    return acc + val;
}

/* ==================== 工具函数测试 ==================== */

void test_utilities(void) {
    printf("\n=== Utilities: Array & ForEach ===\n");
    
    /* From array */
    int arr[] = {10, 20, 30, 40, 50};
    LinkedList* list = list_from_int_array(arr, 5);
    
    TEST("Create from int array");
    ASSERT(list != NULL && list_size(list) == 5, "should create list from array");
    
    /* To array */
    size_t out_size;
    int* out_arr = list_to_int_array(list, &out_size);
    
    TEST("Convert to int array");
    ASSERT(out_arr != NULL && out_size == 5, "should convert to array");
    
    TEST("Array values match");
    bool match = true;
    for (size_t i = 0; i < 5; i++) {
        if (arr[i] != out_arr[i]) {
            match = false;
            break;
        }
    }
    ASSERT(match, "arrays should match");
    
    free(out_arr);
    
    /* Fold (sum) */
    int sum;
    TEST("Fold (sum)");
    list_fold_int(list, 0, fold_sum, NULL, &sum);
    ASSERT(sum == 150, "sum should be 150");
    
    list_destroy(list);
}

/* ==================== 边界条件测试 ==================== */

void test_edge_cases(void) {
    printf("\n=== Edge Cases ===\n");
    
    LinkedList* list = list_create_int();
    
    TEST("Pop from empty list returns false");
    ASSERT(!list_pop_front(list), "should return false");
    
    TEST("Pop back from empty list returns false");
    ASSERT(!list_pop_back(list), "should return false");
    
    TEST("Get from empty list returns false");
    int val;
    ASSERT(!list_get_int(list, 0, &val), "should return false");
    
    TEST("Remove from empty list returns false");
    ASSERT(!list_remove_at(list, 0), "should return false");
    
    TEST("Find in empty list returns -1");
    ASSERT(list_find_int(list, 10) == -1, "should return -1");
    
    /* Test with NULL list */
    TEST("Operations on NULL list");
    ASSERT(list_size(NULL) == 0, "size should be 0");
    ASSERT(list_is_empty(NULL), "should be empty");
    ASSERT(list_front(NULL) == NULL, "front should be NULL");
    
    list_destroy(list);
}

/* ==================== 大量数据测试 ==================== */

void test_large_list(void) {
    printf("\n=== Large List: 10000 elements ===\n");
    
    LinkedList* list = list_create_int();
    
    TEST("Push 10000 elements");
    bool success = true;
    for (int i = 0; i < 10000; i++) {
        if (!list_push_back(list, i)) {
            success = false;
            break;
        }
    }
    ASSERT(success && list_size(list) == 10000, "should push all elements");
    
    TEST("Access last element");
    int val;
    list_get_int(list, 9999, &val);
    ASSERT(val == 9999, "last element should be 9999");
    
    TEST("Reverse 10000 elements");
    list_reverse(list);
    list_get_int(list, 0, &val);
    ASSERT(val == 9999, "first should now be 9999");
    
    TEST("Clear list");
    list_clear(list);
    ASSERT(list_is_empty(list), "should be empty");
    
    list_destroy(list);
}

/* ==================== 主函数 ==================== */

int main(void) {
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║       Linked List Utils - Test Suite                  ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n");
    
    /* 整数链表测试 */
    test_int_list_create_destroy();
    test_int_list_push_pop();
    test_int_list_find();
    test_int_list_remove();
    test_int_list_insert();
    test_int_list_reverse();
    test_int_list_sort();
    test_int_list_unique();
    test_int_list_clone();
    
    /* 字符串链表测试 */
    test_string_list();
    
    /* 双精度链表测试 */
    test_double_list();
    
    /* 迭代器测试 */
    test_iterator();
    
    /* 工具函数测试 */
    test_utilities();
    
    /* 边界条件测试 */
    test_edge_cases();
    
    /* 大量数据测试 */
    test_large_list();
    
    /* 总结 */
    printf("\n════════════════════════════════════════════════════════\n");
    printf("  Tests: %d passed, %d failed\n", tests_passed, tests_failed);
    printf("════════════════════════════════════════════════════════\n");
    
    return tests_failed > 0 ? 1 : 0;
}