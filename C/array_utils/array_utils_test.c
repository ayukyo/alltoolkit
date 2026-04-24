/**
 * @file array_utils_test.c
 * @brief C 语言数组工具库测试
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-25
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "array_utils.h"

#define TEST_PASS(name) printf("  ✓ %s\n", name)

/* 辅助函数：比较数组是否相等 */
static bool int_array_equals(const int* a, const int* b, size_t count) {
    for (size_t i = 0; i < count; i++) {
        if (a[i] != b[i]) return false;
    }
    return true;
}

/* ==================== 排序算法测试 ==================== */

static void test_bubble_sort(void) {
    printf("\n[冒泡排序测试]\n");
    
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    array_bubble_sort(arr, count, sizeof(int), compare_int);
    
    int expected[] = {11, 12, 22, 25, 34, 64, 90};
    assert(int_array_equals(arr, expected, count));
    TEST_PASS("冒泡排序 - 基本测试");
    
    /* 单元素 */
    int single[] = {42};
    array_bubble_sort(single, 1, sizeof(int), compare_int);
    assert(single[0] == 42);
    TEST_PASS("冒泡排序 - 单元素");
}

static void test_selection_sort(void) {
    printf("\n[选择排序测试]\n");
    
    int arr[] = {29, 10, 14, 37, 13};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    array_selection_sort(arr, count, sizeof(int), compare_int);
    
    int expected[] = {10, 13, 14, 29, 37};
    assert(int_array_equals(arr, expected, count));
    TEST_PASS("选择排序 - 基本测试");
}

static void test_insertion_sort(void) {
    printf("\n[插入排序测试]\n");
    
    int arr[] = {12, 11, 13, 5, 6};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    array_insertion_sort(arr, count, sizeof(int), compare_int);
    
    int expected[] = {5, 6, 11, 12, 13};
    assert(int_array_equals(arr, expected, count));
    TEST_PASS("插入排序 - 基本测试");
}

static void test_quick_sort(void) {
    printf("\n[快速排序测试]\n");
    
    int arr[] = {10, 7, 8, 9, 1, 5};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    array_quick_sort(arr, count, sizeof(int), compare_int);
    
    assert(array_is_sorted(arr, count, sizeof(int), compare_int));
    TEST_PASS("快速排序 - 基本测试");
    
    /* 大数组测试 */
    int* large = (int*)malloc(500 * sizeof(int));
    if (large) {
        for (int i = 0; i < 500; i++) {
            large[i] = rand() % 10000;
        }
        array_quick_sort(large, 500, sizeof(int), compare_int);
        assert(array_is_sorted(large, 500, sizeof(int), compare_int));
        free(large);
        TEST_PASS("快速排序 - 大数组");
    }
}

static void test_merge_sort(void) {
    printf("\n[归并排序测试]\n");
    
    int arr[] = {38, 27, 43, 3, 9, 82, 10};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    bool result = array_merge_sort(arr, count, sizeof(int), compare_int, NULL);
    assert(result == true);
    assert(array_is_sorted(arr, count, sizeof(int), compare_int));
    TEST_PASS("归并排序 - 基本测试");
}

/* ==================== 搜索算法测试 ==================== */

static void test_linear_search(void) {
    printf("\n[线性搜索测试]\n");
    
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    int target = 22;
    size_t idx = array_linear_search(arr, count, sizeof(int), &target, compare_int);
    assert(idx == 4);
    TEST_PASS("线性搜索 - 找到元素");
    
    target = 100;
    idx = array_linear_search(arr, count, sizeof(int), &target, compare_int);
    assert(idx == (size_t)-1);
    TEST_PASS("线性搜索 - 未找到元素");
}

static void test_binary_search(void) {
    printf("\n[二分搜索测试]\n");
    
    int arr[] = {11, 12, 22, 25, 34, 64, 90};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    int target = 22;
    size_t idx = array_binary_search(arr, count, sizeof(int), &target, compare_int);
    assert(idx == 2);
    TEST_PASS("二分搜索 - 找到元素");
    
    target = 100;
    idx = array_binary_search(arr, count, sizeof(int), &target, compare_int);
    assert(idx == (size_t)-1);
    TEST_PASS("二分搜索 - 未找到元素");
}

/* ==================== 数组操作测试 ==================== */

static void test_reverse(void) {
    printf("\n[数组反转测试]\n");
    
    int arr[] = {1, 2, 3, 4, 5};
    array_reverse(arr, 5, sizeof(int));
    
    int expected[] = {5, 4, 3, 2, 1};
    assert(int_array_equals(arr, expected, 5));
    TEST_PASS("数组反转 - 基本测试");
}

static void test_slice(void) {
    printf("\n[数组切片测试]\n");
    
    int arr[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    int* slice = (int*)array_slice(arr, 10, sizeof(int), 2, 3, NULL);
    assert(slice != NULL);
    assert(slice[0] == 3);
    assert(slice[1] == 4);
    assert(slice[2] == 5);
    free(slice);
    TEST_PASS("数组切片 - 基本测试");
}

static void test_merge(void) {
    printf("\n[数组合并测试]\n");
    
    int arr1[] = {1, 2, 3};
    int arr2[] = {4, 5, 6};
    
    int* merged = (int*)array_merge(arr1, 3, arr2, 3, sizeof(int), NULL);
    assert(merged != NULL);
    assert(merged[0] == 1);
    assert(merged[5] == 6);
    free(merged);
    TEST_PASS("数组合并 - 基本测试");
}

static void test_unique_sorted(void) {
    printf("\n[数组去重测试]\n");
    
    int arr[] = {1, 1, 2, 2, 2, 3, 4, 4, 5};
    size_t count = 9;
    
    size_t new_count = array_unique_sorted(arr, &count, sizeof(int), compare_int);
    assert(new_count == 5);
    assert(count == 5);
    TEST_PASS("数组去重 - 基本测试");
}

static void test_fill(void) {
    printf("\n[数组填充测试]\n");
    
    int arr[5];
    int value = 42;
    
    array_fill(arr, 5, sizeof(int), &value);
    
    for (int i = 0; i < 5; i++) {
        assert(arr[i] == 42);
    }
    TEST_PASS("数组填充 - 整型");
}

/* ==================== 统计函数测试 ==================== */

static void test_int_statistics(void) {
    printf("\n[整型统计测试]\n");
    
    int arr[] = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    assert(array_int_min(arr, count) == 1);
    TEST_PASS("整型最小值");
    
    assert(array_int_max(arr, count) == 9);
    TEST_PASS("整型最大值");
    
    assert(array_int_sum(arr, count) == 39);
    TEST_PASS("整型总和");
    
    double avg = array_int_avg(arr, count);
    assert(avg == 3.9);
    TEST_PASS("整型平均值");
}

static void test_double_statistics(void) {
    printf("\n[浮点统计测试]\n");
    
    double arr[] = {1.5, 2.5, 3.5, 4.5, 5.5};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    assert(array_double_min(arr, count) == 1.5);
    TEST_PASS("浮点最小值");
    
    assert(array_double_max(arr, count) == 5.5);
    TEST_PASS("浮点最大值");
    
    double sum = array_double_sum(arr, count);
    assert(sum == 17.5);
    TEST_PASS("浮点总和");
}

/* ==================== 数组判断测试 ==================== */

static void test_is_sorted(void) {
    printf("\n[排序判断测试]\n");
    
    int sorted[] = {1, 2, 3, 4, 5};
    assert(array_is_sorted(sorted, 5, sizeof(int), compare_int) == true);
    TEST_PASS("已排序数组");
    
    int unsorted[] = {1, 3, 2, 4, 5};
    assert(array_is_sorted(unsorted, 5, sizeof(int), compare_int) == false);
    TEST_PASS("未排序数组");
}

static void test_contains(void) {
    printf("\n[包含测试]\n");
    
    int arr[] = {10, 20, 30, 40, 50};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    int target = 30;
    assert(array_contains(arr, count, sizeof(int), &target, compare_int) == true);
    TEST_PASS("包含元素");
    
    target = 100;
    assert(array_contains(arr, count, sizeof(int), &target, compare_int) == false);
    TEST_PASS("不包含元素");
}

static void test_count_element(void) {
    printf("\n[计数测试]\n");
    
    int arr[] = {1, 2, 3, 2, 4, 2, 5, 2};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    int target = 2;
    assert(array_count_element(arr, count, sizeof(int), &target, compare_int) == 4);
    TEST_PASS("计数 - 多次出现");
}

/* ==================== 字符串数组测试 ==================== */

static void test_string_sort(void) {
    printf("\n[字符串排序测试]\n");
    
    const char* arr[] = {"banana", "apple", "cherry", "date", "elderberry"};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    array_quick_sort(arr, count, sizeof(const char*), compare_string);
    
    assert(strcmp(arr[0], "apple") == 0);
    assert(strcmp(arr[4], "elderberry") == 0);
    TEST_PASS("字符串排序");
}

/* ==================== 主函数 ==================== */

int main(void) {
    printf("========================================\n");
    printf("  数组工具库测试\n");
    printf("========================================\n");
    
    /* 排序测试 */
    test_bubble_sort();
    test_selection_sort();
    test_insertion_sort();
    test_quick_sort();
    test_merge_sort();
    
    /* 搜索测试 */
    test_linear_search();
    test_binary_search();
    
    /* 数组操作测试 */
    test_reverse();
    test_slice();
    test_merge();
    test_unique_sorted();
    test_fill();
    
    /* 统计测试 */
    test_int_statistics();
    test_double_statistics();
    
    /* 判断测试 */
    test_is_sorted();
    test_contains();
    test_count_element();
    
    /* 字符串测试 */
    test_string_sort();
    
    printf("\n========================================\n");
    printf("  所有测试通过！ ✓\n");
    printf("========================================\n");
    
    return 0;
}