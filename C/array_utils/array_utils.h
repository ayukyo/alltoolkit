/**
 * @file array_utils.h
 * @brief C 语言数组工具库
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-25
 */

#ifndef ARRAY_UTILS_H
#define ARRAY_UTILS_H

#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ==================== 比较函数类型 ==================== */

/**
 * @brief 比较函数指针类型
 * @param a 第一个元素指针
 * @param b 第二个元素指针
 * @return <0: a<b, 0: a==b, >0: a>b
 */
typedef int (*CompareFunc)(const void* a, const void* b);

/* ==================== 排序算法 ==================== */

/**
 * @brief 冒泡排序
 * @param arr 数组指针
 * @param count 元素数量
 * @param element_size 元素大小（字节）
 * @param cmp 比较函数
 */
void array_bubble_sort(void* arr, size_t count, size_t element_size, CompareFunc cmp);

/**
 * @brief 选择排序
 * @param arr 数组指针
 * @param count 元素数量
 * @param element_size 元素大小（字节）
 * @param cmp 比较函数
 */
void array_selection_sort(void* arr, size_t count, size_t element_size, CompareFunc cmp);

/**
 * @brief 插入排序
 * @param arr 数组指针
 * @param count 元素数量
 * @param element_size 元素大小（字节）
 * @param cmp 比较函数
 */
void array_insertion_sort(void* arr, size_t count, size_t element_size, CompareFunc cmp);

/**
 * @brief 快速排序
 * @param arr 数组指针
 * @param count 元素数量
 * @param element_size 元素大小（字节）
 * @param cmp 比较函数
 */
void array_quick_sort(void* arr, size_t count, size_t element_size, CompareFunc cmp);

/**
 * @brief 归并排序
 * @param arr 数组指针
 * @param count 元素数量
 * @param element_size 元素大小（字节）
 * @param cmp 比较函数
 * @param temp_buffer 临时缓冲区（可选，NULL则自动分配）
 * @return 成功返回true，失败返回false
 */
bool array_merge_sort(void* arr, size_t count, size_t element_size, CompareFunc cmp, void* temp_buffer);

/* ==================== 搜索算法 ==================== */

/**
 * @brief 线性搜索
 * @param arr 数组指针
 * @param count 元素数量
 * @param element_size 元素大小（字节）
 * @param target 目标元素指针
 * @param cmp 比较函数
 * @return 找到返回索引，未找到返回 -1（size_t 最大值）
 */
size_t array_linear_search(const void* arr, size_t count, size_t element_size, 
                           const void* target, CompareFunc cmp);

/**
 * @brief 二分搜索（数组必须已排序）
 * @param arr 数组指针
 * @param count 元素数量
 * @param element_size 元素大小（字节）
 * @param target 目标元素指针
 * @param cmp 比较函数
 * @return 找到返回索引，未找到返回 -1（size_t 最大值）
 */
size_t array_binary_search(const void* arr, size_t count, size_t element_size,
                           const void* target, CompareFunc cmp);

/* ==================== 数组操作 ==================== */

/**
 * @brief 反转数组
 * @param arr 数组指针
 * @param count 元素数量
 * @param element_size 元素大小（字节）
 */
void array_reverse(void* arr, size_t count, size_t element_size);

/**
 * @brief 数组切片复制
 * @param src 源数组
 * @param src_count 源数组元素数量
 * @param element_size 元素大小（字节）
 * @param start 起始索引
 * @param length 切片长度
 * @param dest 目标缓冲区（NULL则自动分配）
 * @return 成功返回目标缓冲区指针，失败返回NULL
 */
void* array_slice(const void* src, size_t src_count, size_t element_size,
                  size_t start, size_t length, void* dest);

/**
 * @brief 合并两个数组
 * @param arr1 第一个数组
 * @param count1 第一个数组元素数量
 * @param arr2 第二个数组
 * @param count2 第二个数组元素数量
 * @param element_size 元素大小（字节）
 * @param dest 目标缓冲区（NULL则自动分配）
 * @return 成功返回目标缓冲区指针，失败返回NULL
 */
void* array_merge(const void* arr1, size_t count1, const void* arr2, size_t count2,
                  size_t element_size, void* dest);

/**
 * @brief 原地去重（已排序数组）
 * @param arr 数组指针
 * @param count 元素数量指针（输入/输出）
 * @param element_size 元素大小（字节）
 * @param cmp 比较函数
 * @return 新的元素数量
 */
size_t array_unique_sorted(void* arr, size_t* count, size_t element_size, CompareFunc cmp);

/**
 * @brief 数组填充
 * @param arr 数组指针
 * @param count 元素数量
 * @param element_size 元素大小（字节）
 * @param value 填充值指针
 */
void array_fill(void* arr, size_t count, size_t element_size, const void* value);

/**
 * @brief 数组复制
 * @param dest 目标数组
 * @param src 源数组
 * @param count 元素数量
 * @param element_size 元素大小（字节）
 */
void array_copy(void* dest, const void* src, size_t count, size_t element_size);

/* ==================== 统计函数（整型数组） ==================== */

/**
 * @brief 查找整型数组最小值
 * @param arr 数组指针
 * @param count 元素数量
 * @return 最小值
 */
int array_int_min(const int* arr, size_t count);

/**
 * @brief 查找整型数组最大值
 * @param arr 数组指针
 * @param count 元素数量
 * @return 最大值
 */
int array_int_max(const int* arr, size_t count);

/**
 * @brief 计算整型数组总和
 * @param arr 数组指针
 * @param count 元素数量
 * @return 总和
 */
long long array_int_sum(const int* arr, size_t count);

/**
 * @brief 计算整型数组平均值
 * @param arr 数组指针
 * @param count 元素数量
 * @return 平均值
 */
double array_int_avg(const int* arr, size_t count);

/* ==================== 统计函数（浮点型数组） ==================== */

/**
 * @brief 查找浮点数组最小值
 * @param arr 数组指针
 * @param count 元素数量
 * @return 最小值
 */
double array_double_min(const double* arr, size_t count);

/**
 * @brief 查找浮点数组最大值
 * @param arr 数组指针
 * @param count 元素数量
 * @return 最大值
 */
double array_double_max(const double* arr, size_t count);

/**
 * @brief 计算浮点数组总和
 * @param arr 数组指针
 * @param count 元素数量
 * @return 总和
 */
double array_double_sum(const double* arr, size_t count);

/**
 * @brief 计算浮点数组平均值
 * @param arr 数组指针
 * @param count 元素数量
 * @return 平均值
 */
double array_double_avg(const double* arr, size_t count);

/* ==================== 数组判断 ==================== */

/**
 * @brief 检查数组是否已排序（升序）
 * @param arr 数组指针
 * @param count 元素数量
 * @param element_size 元素大小（字节）
 * @param cmp 比较函数
 * @return 已排序返回true，否则返回false
 */
bool array_is_sorted(const void* arr, size_t count, size_t element_size, CompareFunc cmp);

/**
 * @brief 检查数组是否包含指定元素
 * @param arr 数组指针
 * @param count 元素数量
 * @param element_size 元素大小（字节）
 * @param target 目标元素指针
 * @param cmp 比较函数
 * @return 包含返回true，否则返回false
 */
bool array_contains(const void* arr, size_t count, size_t element_size,
                    const void* target, CompareFunc cmp);

/**
 * @brief 统计数组中某元素出现次数
 * @param arr 数组指针
 * @param count 元素数量
 * @param element_size 元素大小（字节）
 * @param target 目标元素指针
 * @param cmp 比较函数
 * @return 出现次数
 */
size_t array_count_element(const void* arr, size_t count, size_t element_size,
                           const void* target, CompareFunc cmp);

/* ==================== 辅助函数 ==================== */

/**
 * @brief 交换两个元素
 * @param a 第一个元素指针
 * @param b 第二个元素指针
 * @param element_size 元素大小（字节）
 */
void array_swap(void* a, void* b, size_t element_size);

/* ==================== 预定义比较函数 ==================== */

int compare_int(const void* a, const void* b);
int compare_int_desc(const void* a, const void* b);
int compare_double(const void* a, const void* b);
int compare_double_desc(const void* a, const void* b);
int compare_char(const void* a, const void* b);
int compare_char_desc(const void* a, const void* b);
int compare_string(const void* a, const void* b);

#ifdef __cplusplus
}
#endif

#endif /* ARRAY_UTILS_H */