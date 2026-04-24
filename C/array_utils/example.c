/**
 * @file example.c
 * @brief C 语言数组工具库使用示例
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-25
 */

#include <stdio.h>
#include <stdlib.h>
#include "array_utils.h"

/* 打印整型数组 */
void print_int_array(const char* label, const int* arr, size_t count) {
    printf("%s: [", label);
    for (size_t i = 0; i < count; i++) {
        printf("%d", arr[i]);
        if (i < count - 1) printf(", ");
    }
    printf("]\n");
}

/* 打印浮点数组 */
void print_double_array(const char* label, const double* arr, size_t count) {
    printf("%s: [", label);
    for (size_t i = 0; i < count; i++) {
        printf("%.1f", arr[i]);
        if (i < count - 1) printf(", ");
    }
    printf("]\n");
}

/* 示例1：排序算法 */
void example_sorting() {
    printf("\n========== 排序算法示例 ==========\n");
    
    int arr1[] = {64, 34, 25, 12, 22, 11, 90};
    size_t count = sizeof(arr1) / sizeof(arr1[0]);
    
    print_int_array("原始数组", arr1, count);
    
    /* 冒泡排序 */
    int arr2[] = {64, 34, 25, 12, 22, 11, 90};
    array_bubble_sort(arr2, count, sizeof(int), compare_int);
    print_int_array("冒泡排序", arr2, count);
    
    /* 选择排序 */
    int arr3[] = {64, 34, 25, 12, 22, 11, 90};
    array_selection_sort(arr3, count, sizeof(int), compare_int);
    print_int_array("选择排序", arr3, count);
    
    /* 插入排序 */
    int arr4[] = {64, 34, 25, 12, 22, 11, 90};
    array_insertion_sort(arr4, count, sizeof(int), compare_int);
    print_int_array("插入排序", arr4, count);
    
    /* 快速排序 */
    int arr5[] = {64, 34, 25, 12, 22, 11, 90};
    array_quick_sort(arr5, count, sizeof(int), compare_int);
    print_int_array("快速排序", arr5, count);
    
    /* 归并排序 */
    int arr6[] = {64, 34, 25, 12, 22, 11, 90};
    array_merge_sort(arr6, count, sizeof(int), compare_int, NULL);
    print_int_array("归并排序", arr6, count);
    
    /* 降序排序 */
    int arr7[] = {64, 34, 25, 12, 22, 11, 90};
    array_quick_sort(arr7, count, sizeof(int), compare_int_desc);
    print_int_array("降序排序", arr7, count);
}

/* 示例2：搜索算法 */
void example_search() {
    printf("\n========== 搜索算法示例 ==========\n");
    
    int arr[] = {11, 12, 22, 25, 34, 64, 90};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    print_int_array("已排序数组", arr, count);
    
    /* 线性搜索 */
    int target = 22;
    size_t idx = array_linear_search(arr, count, sizeof(int), &target, compare_int);
    printf("线性搜索 %d: 索引 %zu\n", target, idx);
    
    /* 二分搜索 */
    target = 64;
    idx = array_binary_search(arr, count, sizeof(int), &target, compare_int);
    printf("二分搜索 %d: 索引 %zu\n", target, idx);
    
    /* 搜索不存在的元素 */
    target = 100;
    idx = array_binary_search(arr, count, sizeof(int), &target, compare_int);
    printf("二分搜索 %d: 索引 %zu (未找到)\n", target, idx);
}

/* 示例3：数组操作 */
void example_operations() {
    printf("\n========== 数组操作示例 ==========\n");
    
    int arr[] = {1, 2, 3, 4, 5};
    size_t count = sizeof(arr) / sizeof(arr[0]);
    
    /* 反转 */
    int reversed[] = {1, 2, 3, 4, 5};
    array_reverse(reversed, count, sizeof(int));
    print_int_array("反转后", reversed, count);
    
    /* 切片 */
    int source[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int* slice = (int*)array_slice(source, 10, sizeof(int), 2, 4, NULL);
    print_int_array("切片 [2:6]", slice, 4);
    free(slice);
    
    /* 合并 */
    int arr1[] = {1, 2, 3};
    int arr2[] = {4, 5, 6};
    int* merged = (int*)array_merge(arr1, 3, arr2, 3, sizeof(int), NULL);
    print_int_array("合并后", merged, 6);
    free(merged);
    
    /* 去重 */
    int unique[] = {1, 1, 2, 2, 2, 3, 4, 4, 5};
    size_t unique_count = 9;
    print_int_array("去重前", unique, unique_count);
    size_t new_count = array_unique_sorted(unique, &unique_count, sizeof(int), compare_int);
    print_int_array("去重后", unique, new_count);
    
    /* 填充 */
    int filled[5];
    int value = 42;
    array_fill(filled, 5, sizeof(int), &value);
    print_int_array("填充后", filled, 5);
}

/* 示例4：统计函数 */
void example_statistics() {
    printf("\n========== 统计函数示例 ==========\n");
    
    /* 整型统计 */
    int int_arr[] = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3};
    size_t int_count = sizeof(int_arr) / sizeof(int_arr[0]);
    
    print_int_array("整型数组", int_arr, int_count);
    printf("最小值: %d\n", array_int_min(int_arr, int_count));
    printf("最大值: %d\n", array_int_max(int_arr, int_count));
    printf("总和: %lld\n", array_int_sum(int_arr, int_count));
    printf("平均值: %.2f\n", array_int_avg(int_arr, int_count));
    
    /* 浮点统计 */
    double dbl_arr[] = {1.5, 2.5, 3.5, 4.5, 5.5};
    size_t dbl_count = sizeof(dbl_arr) / sizeof(dbl_arr[0]);
    
    print_double_array("浮点数组", dbl_arr, dbl_count);
    printf("最小值: %.1f\n", array_double_min(dbl_arr, dbl_count));
    printf("最大值: %.1f\n", array_double_max(dbl_arr, dbl_count));
    printf("总和: %.1f\n", array_double_sum(dbl_arr, dbl_count));
    printf("平均值: %.2f\n", array_double_avg(dbl_arr, dbl_count));
}

/* 示例5：数组判断 */
void example_checks() {
    printf("\n========== 数组判断示例 ==========\n");
    
    int sorted[] = {1, 2, 3, 4, 5};
    int unsorted[] = {1, 3, 2, 4, 5};
    
    printf("数组 [1,2,3,4,5] 已排序: %s\n", 
           array_is_sorted(sorted, 5, sizeof(int), compare_int) ? "是" : "否");
    printf("数组 [1,3,2,4,5] 已排序: %s\n", 
           array_is_sorted(unsorted, 5, sizeof(int), compare_int) ? "是" : "否");
    
    int arr[] = {10, 20, 30, 40, 50};
    int target = 30;
    printf("数组包含 30: %s\n", 
           array_contains(arr, 5, sizeof(int), &target, compare_int) ? "是" : "否");
    
    int dup_arr[] = {1, 2, 3, 2, 4, 2, 5, 2};
    target = 2;
    printf("数组中 2 出现次数: %zu\n", 
           array_count_element(dup_arr, 8, sizeof(int), &target, compare_int));
}

/* 示例6：字符串数组 */
void example_strings() {
    printf("\n========== 字符串数组示例 ==========\n");
    
    const char* fruits[] = {"banana", "apple", "cherry", "date", "elderberry"};
    size_t count = sizeof(fruits) / sizeof(fruits[0]);
    
    printf("排序前: [");
    for (size_t i = 0; i < count; i++) {
        printf("\"%s\"", fruits[i]);
        if (i < count - 1) printf(", ");
    }
    printf("]\n");
    
    /* 字符串排序 */
    array_quick_sort(fruits, count, sizeof(const char*), compare_string);
    
    printf("排序后: [");
    for (size_t i = 0; i < count; i++) {
        printf("\"%s\"", fruits[i]);
        if (i < count - 1) printf(", ");
    }
    printf("]\n");
}

/* 示例7：自定义比较函数 */
int compare_person_age(const void* a, const void* b) {
    /* 假设结构体第一个成员是 age (int) */
    int age_a = *(const int*)a;
    int age_b = *(const int*)b;
    return (age_a > age_b) - (age_a < age_b);
}

void example_custom_compare() {
    printf("\n========== 自定义比较函数示例 ==========\n");
    
    /* 简化的结构体：假设第一个字段是 age */
    typedef struct {
        int age;
        const char* name;
    } Person;
    
    Person people[] = {
        {25, "Alice"},
        {30, "Bob"},
        {20, "Charlie"},
        {35, "Diana"}
    };
    size_t count = sizeof(people) / sizeof(people[0]);
    
    printf("排序前:\n");
    for (size_t i = 0; i < count; i++) {
        printf("  %s: %d 岁\n", people[i].name, people[i].age);
    }
    
    /* 按年龄排序 */
    array_quick_sort(people, count, sizeof(Person), compare_person_age);
    
    printf("按年龄排序后:\n");
    for (size_t i = 0; i < count; i++) {
        printf("  %s: %d 岁\n", people[i].name, people[i].age);
    }
}

int main() {
    printf("========================================\n");
    printf("  C 语言数组工具库使用示例\n");
    printf("========================================\n");
    
    example_sorting();
    example_search();
    example_operations();
    example_statistics();
    example_checks();
    example_strings();
    example_custom_compare();
    
    printf("\n========================================\n");
    printf("  示例演示完成！\n");
    printf("========================================\n");
    
    return 0;
}