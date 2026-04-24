/**
 * @file array_utils.c
 * @brief C 语言数组工具库实现
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-25
 */

#include "array_utils.h"
#include <stdlib.h>
#include <string.h>

/* ==================== 辅助函数 ==================== */

void array_swap(void* a, void* b, size_t element_size) {
    if (a == NULL || b == NULL || element_size == 0) return;
    
    unsigned char* pa = (unsigned char*)a;
    unsigned char* pb = (unsigned char*)b;
    unsigned char temp;
    
    for (size_t i = 0; i < element_size; i++) {
        temp = pa[i];
        pa[i] = pb[i];
        pb[i] = temp;
    }
}

/* ==================== 排序算法 ==================== */

void array_bubble_sort(void* arr, size_t count, size_t element_size, CompareFunc cmp) {
    if (arr == NULL || cmp == NULL || element_size == 0) return;
    
    unsigned char* base = (unsigned char*)arr;
    bool swapped;
    
    for (size_t i = 0; i < count - 1; i++) {
        swapped = false;
        for (size_t j = 0; j < count - i - 1; j++) {
            void* a = base + j * element_size;
            void* b = base + (j + 1) * element_size;
            if (cmp(a, b) > 0) {
                array_swap(a, b, element_size);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

void array_selection_sort(void* arr, size_t count, size_t element_size, CompareFunc cmp) {
    if (arr == NULL || cmp == NULL || element_size == 0) return;
    
    unsigned char* base = (unsigned char*)arr;
    
    for (size_t i = 0; i < count - 1; i++) {
        size_t min_idx = i;
        for (size_t j = i + 1; j < count; j++) {
            void* a = base + min_idx * element_size;
            void* b = base + j * element_size;
            if (cmp(a, b) > 0) {
                min_idx = j;
            }
        }
        if (min_idx != i) {
            array_swap(base + i * element_size, base + min_idx * element_size, element_size);
        }
    }
}

void array_insertion_sort(void* arr, size_t count, size_t element_size, CompareFunc cmp) {
    if (arr == NULL || cmp == NULL || element_size == 0) return;
    
    unsigned char* base = (unsigned char*)arr;
    unsigned char* key = (unsigned char*)malloc(element_size);
    
    if (key == NULL) return;
    
    for (size_t i = 1; i < count; i++) {
        memcpy(key, base + i * element_size, element_size);
        size_t j = i;
        
        while (j > 0 && cmp(key, base + (j - 1) * element_size) < 0) {
            memcpy(base + j * element_size, base + (j - 1) * element_size, element_size);
            j--;
        }
        memcpy(base + j * element_size, key, element_size);
    }
    
    free(key);
}

/* 快速排序内部实现 */
static size_t partition(unsigned char* base, size_t count, size_t element_size, CompareFunc cmp) {
    size_t pivot_idx = count / 2;
    array_swap(base + pivot_idx * element_size, base + (count - 1) * element_size, element_size);
    
    void* pivot = base + (count - 1) * element_size;
    size_t store_idx = 0;
    
    for (size_t i = 0; i < count - 1; i++) {
        if (cmp(base + i * element_size, pivot) <= 0) {
            array_swap(base + i * element_size, base + store_idx * element_size, element_size);
            store_idx++;
        }
    }
    
    array_swap(base + store_idx * element_size, base + (count - 1) * element_size, element_size);
    return store_idx;
}

void array_quick_sort(void* arr, size_t count, size_t element_size, CompareFunc cmp) {
    if (arr == NULL || cmp == NULL || element_size == 0 || count <= 1) return;
    
    unsigned char* base = (unsigned char*)arr;
    
    /* 使用显式栈避免递归深度问题 */
    typedef struct {
        size_t start;
        size_t count;
    } StackItem;
    
    StackItem* stack = (StackItem*)malloc(count * sizeof(StackItem));
    if (stack == NULL) return;
    
    int stack_top = 0;
    stack[stack_top].start = 0;
    stack[stack_top].count = count;
    
    while (stack_top >= 0) {
        StackItem current = stack[stack_top--];
        
        if (current.count <= 1) continue;
        
        size_t pivot_idx = partition(base + current.start * element_size, 
                                      current.count, element_size, cmp);
        
        /* 左半部分 */
        if (pivot_idx > 0) {
            stack[++stack_top].start = current.start;
            stack[stack_top].count = pivot_idx;
        }
        
        /* 右半部分 */
        if (pivot_idx + 1 < current.count) {
            stack[++stack_top].start = current.start + pivot_idx + 1;
            stack[stack_top].count = current.count - pivot_idx - 1;
        }
    }
    
    free(stack);
}

bool array_merge_sort(void* arr, size_t count, size_t element_size, CompareFunc cmp, void* temp_buffer) {
    if (arr == NULL || cmp == NULL || element_size == 0 || count <= 1) return true;
    
    unsigned char* base = (unsigned char*)arr;
    bool need_free = false;
    
    if (temp_buffer == NULL) {
        temp_buffer = malloc(count * element_size);
        if (temp_buffer == NULL) return false;
        need_free = true;
    }
    
    unsigned char* temp = (unsigned char*)temp_buffer;
    
    /* 自底向上归并 */
    for (size_t width = 1; width < count; width *= 2) {
        for (size_t i = 0; i < count; i += 2 * width) {
            size_t left = i;
            size_t mid = (i + width < count) ? i + width : count;
            size_t right = (i + 2 * width < count) ? i + 2 * width : count;
            
            /* 归并 */
            size_t l = left, r = mid, k = left;
            while (l < mid && r < right) {
                if (cmp(base + l * element_size, base + r * element_size) <= 0) {
                    memcpy(temp + k * element_size, base + l * element_size, element_size);
                    l++;
                } else {
                    memcpy(temp + k * element_size, base + r * element_size, element_size);
                    r++;
                }
                k++;
            }
            
            while (l < mid) {
                memcpy(temp + k * element_size, base + l * element_size, element_size);
                l++;
                k++;
            }
            
            while (r < right) {
                memcpy(temp + k * element_size, base + r * element_size, element_size);
                r++;
                k++;
            }
        }
        
        /* 交换 base 和 temp */
        unsigned char* swap_temp = base;
        base = temp;
        temp = swap_temp;
    }
    
    /* 确保结果在原数组中 */
    if (base != arr) {
        memcpy(arr, base, count * element_size);
    }
    
    if (need_free) {
        free(temp_buffer);
    }
    
    return true;
}

/* ==================== 搜索算法 ==================== */

size_t array_linear_search(const void* arr, size_t count, size_t element_size,
                           const void* target, CompareFunc cmp) {
    if (arr == NULL || target == NULL || cmp == NULL || element_size == 0) {
        return (size_t)-1;
    }
    
    const unsigned char* base = (const unsigned char*)arr;
    
    for (size_t i = 0; i < count; i++) {
        if (cmp(base + i * element_size, target) == 0) {
            return i;
        }
    }
    
    return (size_t)-1;
}

size_t array_binary_search(const void* arr, size_t count, size_t element_size,
                           const void* target, CompareFunc cmp) {
    if (arr == NULL || target == NULL || cmp == NULL || element_size == 0) {
        return (size_t)-1;
    }
    
    const unsigned char* base = (const unsigned char*)arr;
    size_t left = 0;
    size_t right = count;
    
    while (left < right) {
        size_t mid = left + (right - left) / 2;
        int result = cmp(base + mid * element_size, target);
        
        if (result == 0) {
            return mid;
        } else if (result < 0) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    
    return (size_t)-1;
}

/* ==================== 数组操作 ==================== */

void array_reverse(void* arr, size_t count, size_t element_size) {
    if (arr == NULL || element_size == 0 || count <= 1) return;
    
    unsigned char* base = (unsigned char*)arr;
    size_t left = 0;
    size_t right = count - 1;
    
    while (left < right) {
        array_swap(base + left * element_size, base + right * element_size, element_size);
        left++;
        right--;
    }
}

void* array_slice(const void* src, size_t src_count, size_t element_size,
                  size_t start, size_t length, void* dest) {
    if (src == NULL || element_size == 0) return NULL;
    if (start >= src_count) return NULL;
    
    /* 调整长度避免越界 */
    if (start + length > src_count) {
        length = src_count - start;
    }
    
    if (dest == NULL) {
        dest = malloc(length * element_size);
        if (dest == NULL) return NULL;
    }
    
    memcpy(dest, (const unsigned char*)src + start * element_size, length * element_size);
    
    return dest;
}

void* array_merge(const void* arr1, size_t count1, const void* arr2, size_t count2,
                  size_t element_size, void* dest) {
    if (element_size == 0) return NULL;
    
    size_t total = count1 + count2;
    
    if (dest == NULL) {
        dest = malloc(total * element_size);
        if (dest == NULL) return NULL;
    }
    
    if (arr1 != NULL && count1 > 0) {
        memcpy(dest, arr1, count1 * element_size);
    }
    
    if (arr2 != NULL && count2 > 0) {
        memcpy((unsigned char*)dest + count1 * element_size, arr2, count2 * element_size);
    }
    
    return dest;
}

size_t array_unique_sorted(void* arr, size_t* count, size_t element_size, CompareFunc cmp) {
    if (arr == NULL || count == NULL || cmp == NULL || element_size == 0) {
        if (count) *count = 0;
        return 0;
    }
    
    unsigned char* base = (unsigned char*)arr;
    size_t new_count = 0;
    
    for (size_t i = 0; i < *count; i++) {
        if (i == 0 || cmp(base + i * element_size, base + (new_count - 1) * element_size) != 0) {
            if (i != new_count) {
                memcpy(base + new_count * element_size, base + i * element_size, element_size);
            }
            new_count++;
        }
    }
    
    *count = new_count;
    return new_count;
}

void array_fill(void* arr, size_t count, size_t element_size, const void* value) {
    if (arr == NULL || element_size == 0) return;
    
    unsigned char* base = (unsigned char*)arr;
    
    for (size_t i = 0; i < count; i++) {
        memcpy(base + i * element_size, value, element_size);
    }
}

void array_copy(void* dest, const void* src, size_t count, size_t element_size) {
    if (dest == NULL || src == NULL || element_size == 0) return;
    
    memcpy(dest, src, count * element_size);
}

/* ==================== 统计函数（整型数组） ==================== */

int array_int_min(const int* arr, size_t count) {
    if (arr == NULL || count == 0) return 0;
    
    int min = arr[0];
    for (size_t i = 1; i < count; i++) {
        if (arr[i] < min) {
            min = arr[i];
        }
    }
    return min;
}

int array_int_max(const int* arr, size_t count) {
    if (arr == NULL || count == 0) return 0;
    
    int max = arr[0];
    for (size_t i = 1; i < count; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}

long long array_int_sum(const int* arr, size_t count) {
    if (arr == NULL || count == 0) return 0;
    
    long long sum = 0;
    for (size_t i = 0; i < count; i++) {
        sum += arr[i];
    }
    return sum;
}

double array_int_avg(const int* arr, size_t count) {
    if (arr == NULL || count == 0) return 0.0;
    
    return (double)array_int_sum(arr, count) / (double)count;
}

/* ==================== 统计函数（浮点型数组） ==================== */

double array_double_min(const double* arr, size_t count) {
    if (arr == NULL || count == 0) return 0.0;
    
    double min = arr[0];
    for (size_t i = 1; i < count; i++) {
        if (arr[i] < min) {
            min = arr[i];
        }
    }
    return min;
}

double array_double_max(const double* arr, size_t count) {
    if (arr == NULL || count == 0) return 0.0;
    
    double max = arr[0];
    for (size_t i = 1; i < count; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}

double array_double_sum(const double* arr, size_t count) {
    if (arr == NULL || count == 0) return 0.0;
    
    double sum = 0.0;
    for (size_t i = 0; i < count; i++) {
        sum += arr[i];
    }
    return sum;
}

double array_double_avg(const double* arr, size_t count) {
    if (arr == NULL || count == 0) return 0.0;
    
    return array_double_sum(arr, count) / (double)count;
}

/* ==================== 数组判断 ==================== */

bool array_is_sorted(const void* arr, size_t count, size_t element_size, CompareFunc cmp) {
    if (arr == NULL || cmp == NULL || element_size == 0 || count <= 1) {
        return true;
    }
    
    const unsigned char* base = (const unsigned char*)arr;
    
    for (size_t i = 0; i < count - 1; i++) {
        if (cmp(base + i * element_size, base + (i + 1) * element_size) > 0) {
            return false;
        }
    }
    
    return true;
}

bool array_contains(const void* arr, size_t count, size_t element_size,
                    const void* target, CompareFunc cmp) {
    return array_linear_search(arr, count, element_size, target, cmp) != (size_t)-1;
}

size_t array_count_element(const void* arr, size_t count, size_t element_size,
                           const void* target, CompareFunc cmp) {
    if (arr == NULL || target == NULL || cmp == NULL || element_size == 0) {
        return 0;
    }
    
    size_t result = 0;
    const unsigned char* base = (const unsigned char*)arr;
    
    for (size_t i = 0; i < count; i++) {
        if (cmp(base + i * element_size, target) == 0) {
            result++;
        }
    }
    
    return result;
}

/* ==================== 预定义比较函数 ==================== */

int compare_int(const void* a, const void* b) {
    int ia = *(const int*)a;
    int ib = *(const int*)b;
    return (ia > ib) - (ia < ib);
}

int compare_int_desc(const void* a, const void* b) {
    return -compare_int(a, b);
}

int compare_double(const void* a, const void* b) {
    double da = *(const double*)a;
    double db = *(const double*)b;
    if (da < db) return -1;
    if (da > db) return 1;
    return 0;
}

int compare_double_desc(const void* a, const void* b) {
    return -compare_double(a, b);
}

int compare_char(const void* a, const void* b) {
    char ca = *(const char*)a;
    char cb = *(const char*)b;
    return (int)((unsigned char)ca - (unsigned char)cb);
}

int compare_char_desc(const void* a, const void* b) {
    return -compare_char(a, b);
}

int compare_string(const void* a, const void* b) {
    const char* sa = *(const char* const*)a;
    const char* sb = *(const char* const*)b;
    return strcmp(sa, sb);
}