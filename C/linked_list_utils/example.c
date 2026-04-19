/**
 * @file example.c
 * @brief 双向链表工具库使用示例
 * @author AllToolkit
 * @date 2026-04-20
 */

#include "linked_list_utils.h"
#include <stdio.h>
#include <stdlib.h>

/* Fold helper function for sum */
static int example_fold_sum(int acc, int val, void* user) {
    (void)user;
    return acc + val;
}

int main(void) {
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║       Linked List Utils - Usage Examples              ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n\n");
    
    /* ========== 示例 1: 整数链表基本操作 ========== */
    printf("=== Example 1: Integer List Basics ===\n\n");
    
    LinkedList* int_list = list_create_int();
    
    /* 添加元素 */
    printf("Adding elements:\n");
    list_push_back(int_list, 10);
    list_push_back(int_list, 20);
    list_push_front(int_list, 5);
    list_insert_at(int_list, 2, 15);
    
    printf("  List: ");
    list_print_int(int_list);
    printf("  Size: %zu\n\n", list_size(int_list));
    
    /* 查找和访问 */
    printf("Finding and accessing:\n");
    int val;
    list_get_int(int_list, 0, &val);
    printf("  First element: %d\n", val);
    
    list_get_int(int_list, 2, &val);
    printf("  Element at index 2: %d\n", val);
    
    long idx = list_find_int(int_list, 20);
    printf("  Index of 20: %ld\n", idx);
    
    printf("  Contains 15? %s\n\n", list_contains_int(int_list, 15) ? "Yes" : "No");
    
    /* 排序和反转 */
    printf("Sorting and reversing:\n");
    list_push_back(int_list, 3);
    list_push_back(int_list, 25);
    printf("  Before sort: ");
    list_print_int(int_list);
    
    list_sort(int_list);
    printf("  After sort:  ");
    list_print_int(int_list);
    
    list_reverse(int_list);
    printf("  After reverse: ");
    list_print_int(int_list);
    printf("\n");
    
    /* 删除 */
    printf("Removing elements:\n");
    printf("  Remove element at index 1\n");
    list_remove_at(int_list, 1);
    printf("  List: ");
    list_print_int(int_list);
    
    printf("  Remove all occurrences of 5\n");
    list_remove_all_int(int_list, 5);
    printf("  List: ");
    list_print_int(int_list);
    printf("\n");
    
    list_destroy(int_list);
    
    /* ========== 示例 2: 字符串链表 ========== */
    printf("=== Example 2: String List ===\n\n");
    
    LinkedList* str_list = list_create_string();
    
    /* 添加字符串 */
    printf("Adding strings:\n");
    list_push_back(str_list, "Hello");
    list_push_back(str_list, "World");
    list_push_front(str_list, "Start");
    list_push_back(str_list, "End");
    
    printf("  List: ");
    list_print_string(str_list);
    printf("  Size: %zu\n\n", list_size(str_list));
    
    /* 查找和删除 */
    printf("Finding and removing:\n");
    long str_idx = list_find_string(str_list, "World");
    printf("  Index of 'World': %ld\n", str_idx);
    
    printf("  Remove 'World'\n");
    list_remove_string(str_list, "World");
    printf("  List: ");
    list_print_string(str_list);
    printf("\n");
    
    list_destroy(str_list);
    
    /* ========== 示例 3: 双精度链表 ========== */
    printf("=== Example 3: Double List ===\n\n");
    
    LinkedList* double_list = list_create_double();
    
    list_push_back(double_list, 1.5);
    list_push_back(double_list, 2.7);
    list_push_back(double_list, 3.14159);
    list_push_back(double_list, 1.41421);
    
    printf("  List: ");
    list_print(double_list);
    
    double dval;
    list_get_double(double_list, 2, &dval);
    printf("  Element at index 2: %.5f\n\n", dval);
    
    list_destroy(double_list);
    
    /* ========== 示例 4: 迭代器 ========== */
    printf("=== Example 4: Iterator ===\n\n");
    
    LinkedList* iter_list = list_create_int();
    for (int i = 1; i <= 5; i++) {
        list_push_back(iter_list, i * 10);
    }
    
    printf("  Forward iteration:\n");
    ListIterator it = list_iterator(iter_list);
    printf("    ");
    do {
        printf("%d ", list_iterator_get_int(&it));
    } while (list_iterator_next(&it));
    printf("\n");
    
    printf("  Reverse iteration:\n");
    it = list_iterator_reverse(iter_list);
    printf("    ");
    do {
        printf("%d ", list_iterator_get_int(&it));
    } while (list_iterator_next(&it));
    printf("\n\n");
    
    list_destroy(iter_list);
    
    /* ========== 示例 5: 数组转换 ========== */
    printf("=== Example 5: Array Conversion ===\n\n");
    
    int arr[] = {100, 200, 300, 400, 500};
    LinkedList* arr_list = list_from_int_array(arr, 5);
    
    printf("  Created from array: ");
    list_print_int(arr_list);
    
    size_t out_size;
    int* out_arr = list_to_int_array(arr_list, &out_size);
    
    printf("  Converted back to array: ");
    for (size_t i = 0; i < out_size; i++) {
        printf("%d ", out_arr[i]);
    }
    printf("\n\n");
    
    free(out_arr);
    list_destroy(arr_list);
    
    /* ========== 示例 6: 求和 (Fold) ========== */
    printf("=== Example 6: Sum with Fold ===\n\n");
    
    LinkedList* fold_list = list_create_int();
    list_push_back(fold_list, 1);
    list_push_back(fold_list, 2);
    list_push_back(fold_list, 3);
    list_push_back(fold_list, 4);
    list_push_back(fold_list, 5);
    
    /* Sum using fold */
    int sum_result;
    list_fold_int(fold_list, 0, example_fold_sum, NULL, &sum_result);
    
    printf("  List: ");
    list_print_int(fold_list);
    printf("  Sum of all elements: %d\n\n", sum_result);
    
    list_destroy(fold_list);
    
    /* ========== 示例 7: 克隆链表 ========== */
    printf("=== Example 7: Clone List ===\n\n");
    
    LinkedList* original = list_create_int();
    list_push_back(original, 1);
    list_push_back(original, 2);
    list_push_back(original, 3);
    
    LinkedList* cloned = list_clone(original);
    
    printf("  Original: ");
    list_print_int(original);
    printf("  Cloned:   ");
    list_print_int(cloned);
    
    /* 修改原始链表不影响克隆 */
    list_pop_front(original);
    printf("  After modifying original:\n");
    printf("    Original: ");
    list_print_int(original);
    printf("    Cloned:   ");
    list_print_int(cloned);
    printf("\n");
    
    list_destroy(original);
    list_destroy(cloned);
    
    /* ========== 示例 8: 去重 ========== */
    printf("=== Example 8: Unique (Remove Duplicates) ===\n\n");
    
    LinkedList* dup_list = list_create_int();
    list_push_back(dup_list, 1);
    list_push_back(dup_list, 1);
    list_push_back(dup_list, 2);
    list_push_back(dup_list, 2);
    list_push_back(dup_list, 2);
    list_push_back(dup_list, 3);
    
    printf("  Before unique: ");
    list_print_int(dup_list);
    
    list_unique(dup_list);
    printf("  After unique:  ");
    list_print_int(dup_list);
    printf("  Size: %zu\n\n", list_size(dup_list));
    
    list_destroy(dup_list);
    
    printf("════════════════════════════════════════════════════════\n");
    printf("All examples completed successfully!\n");
    printf("════════════════════════════════════════════════════════\n");
    
    return 0;
}