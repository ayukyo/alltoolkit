/**
 * @file linked_list_utils.h
 * @brief C 语言双向链表工具库
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-20
 */

#ifndef LINKED_LIST_UTILS_H
#define LINKED_LIST_UTILS_H

#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ==================== 类型定义 ==================== */

/**
 * @brief 链表节点类型枚举
 */
typedef enum {
    LIST_TYPE_INT,       /* int 类型 */
    LIST_TYPE_DOUBLE,    /* double 类型 */
    LIST_TYPE_STRING,    /* char* 类型 (会深拷贝) */
    LIST_TYPE_POINTER,   /* void* 类型 (不管理内存) */
    LIST_TYPE_GENERIC    /* 通用类型 (用户自定义) */
} ListType;

/**
 * @brief 链表节点
 */
typedef struct ListNode {
    union {
        int int_val;
        double double_val;
        char* string_val;
        void* pointer_val;
        unsigned char generic_data[32]; /* 小对象直接存储 */
    } data;
    struct ListNode* prev;
    struct ListNode* next;
} ListNode;

/**
 * @brief 双向链表结构
 */
typedef struct {
    ListNode* head;
    ListNode* tail;
    size_t size;
    ListType type;
    size_t generic_size;        /* 通用类型的数据大小 */
    void (*free_func)(void*);    /* 自定义释放函数 */
} LinkedList;

/**
 * @brief 链表迭代器
 */
typedef struct {
    ListNode* current;
    ListType type;
    bool forward;  /* true = 正向, false = 反向 */
} ListIterator;

/* ==================== 创建和销毁 ==================== */

/**
 * @brief 创建整数类型链表
 */
LinkedList* list_create_int(void);

/**
 * @brief 创建浮点类型链表
 */
LinkedList* list_create_double(void);

/**
 * @brief 创建字符串类型链表
 */
LinkedList* list_create_string(void);

/**
 * @brief 创建指针类型链表
 */
LinkedList* list_create_pointer(void);

/**
 * @brief 创建通用类型链表
 * @param data_size 单个元素大小
 * @param free_func 自定义释放函数 (可为 NULL)
 */
LinkedList* list_create_generic(size_t data_size, void (*free_func)(void*));

/**
 * @brief 销毁链表并释放所有内存
 */
void list_destroy(LinkedList* list);

/**
 * @brief 清空链表 (保留链表结构)
 */
void list_clear(LinkedList* list);

/* ==================== 头部操作 ==================== */

/**
 * @brief 在头部插入元素
 */
bool list_push_front(LinkedList* list, ...);

/**
 * @brief 移除头部元素并返回
 */
bool list_pop_front(LinkedList* list);

/**
 * @brief 获取头部元素
 */
ListNode* list_front(LinkedList* list);

/* ==================== 尾部操作 ==================== */

/**
 * @brief 在尾部插入元素
 */
bool list_push_back(LinkedList* list, ...);

/**
 * @brief 移除尾部元素
 */
bool list_pop_back(LinkedList* list);

/**
 * @brief 获取尾部元素
 */
ListNode* list_back(LinkedList* list);

/* ==================== 索引操作 ==================== */

/**
 * @brief 在指定位置插入元素
 * @param index 插入位置 (0 = 头部, size = 尾部)
 */
bool list_insert_at(LinkedList* list, size_t index, ...);

/**
 * @brief 移除指定位置的元素
 */
bool list_remove_at(LinkedList* list, size_t index);

/**
 * @brief 获取指定位置的节点
 */
ListNode* list_get_node(LinkedList* list, size_t index);

/**
 * @brief 获取指定位置的整数值
 */
bool list_get_int(LinkedList* list, size_t index, int* out);

/**
 * @brief 获取指定位置的浮点值
 */
bool list_get_double(LinkedList* list, size_t index, double* out);

/**
 * @brief 获取指定位置的字符串值
 */
bool list_get_string(LinkedList* list, size_t index, const char** out);

/**
 * @brief 获取指定位置的指针值
 */
bool list_get_pointer(LinkedList* list, size_t index, void** out);

/* ==================== 查找操作 ==================== */

/**
 * @brief 查找整数值的位置 (-1 表示未找到)
 */
long list_find_int(LinkedList* list, int value);

/**
 * @brief 查找浮点值的位置 (使用 epsilon 比较)
 */
long list_find_double(LinkedList* list, double value, double epsilon);

/**
 * @brief 查找字符串值的位置
 */
long list_find_string(LinkedList* list, const char* value);

/**
 * @brief 查找指针值的位置
 */
long list_find_pointer(LinkedList* list, void* value);

/**
 * @brief 检查链表是否包含指定整数值
 */
bool list_contains_int(LinkedList* list, int value);

/**
 * @brief 检查链表是否包含指定字符串
 */
bool list_contains_string(LinkedList* list, const char* value);

/* ==================== 删除操作 ==================== */

/**
 * @brief 删除第一个匹配的整数值
 */
bool list_remove_int(LinkedList* list, int value);

/**
 * @brief 删除第一个匹配的字符串值
 */
bool list_remove_string(LinkedList* list, const char* value);

/**
 * @brief 删除所有匹配的整数值
 */
size_t list_remove_all_int(LinkedList* list, int value);

/* ==================== 信息查询 ==================== */

/**
 * @brief 获取链表大小
 */
size_t list_size(LinkedList* list);

/**
 * @brief 检查链表是否为空
 */
bool list_is_empty(LinkedList* list);

/**
 * @brief 获取链表类型
 */
ListType list_get_type(LinkedList* list);

/* ==================== 链表操作 ==================== */

/**
 * @brief 反转链表
 */
void list_reverse(LinkedList* list);

/**
 * @brief 连接两个链表 (目标链表会被清空并追加到源链表末尾)
 */
void list_concat(LinkedList* list, LinkedList* other);

/**
 * @brief 复制链表
 */
LinkedList* list_clone(LinkedList* list);

/**
 * @brief 对链表排序 (升序)
 */
void list_sort(LinkedList* list);

/**
 * @brief 对链表排序 (可指定比较函数)
 */
void list_sort_with(LinkedList* list, int (*compare)(ListNode*, ListNode*));

/**
 * @brief 去重 (需要已排序)
 */
void list_unique(LinkedList* list);

/* ==================== 迭代器 ==================== */

/**
 * @brief 创建正向迭代器
 */
ListIterator list_iterator(LinkedList* list);

/**
 * @brief 创建反向迭代器
 */
ListIterator list_iterator_reverse(LinkedList* list);

/**
 * @brief 移动到下一个元素
 */
bool list_iterator_next(ListIterator* it);

/**
 * @brief 获取当前节点
 */
ListNode* list_iterator_get(ListIterator* it);

/**
 * @brief 获取当前整数值
 */
int list_iterator_get_int(ListIterator* it);

/**
 * @brief 获取当前字符串值
 */
const char* list_iterator_get_string(ListIterator* it);

/* ==================== 工具函数 ==================== */

/**
 * @brief 创建整数链表并填充数组
 */
LinkedList* list_from_int_array(int* arr, size_t size);

/**
 * @brief 创建字符串链表并填充数组
 */
LinkedList* list_from_string_array(const char** arr, size_t size);

/**
 * @brief 将整数链表转换为数组
 */
int* list_to_int_array(LinkedList* list, size_t* out_size);

/**
 * @brief 遍历链表并执行回调函数
 */
void list_foreach(LinkedList* list, void (*callback)(ListNode*, void*), void* user_data);

/**
 * @brief 过滤链表元素
 */
LinkedList* list_filter(LinkedList* list, bool (*predicate)(ListNode*, void*), void* user_data);

/**
 * @brief 映射链表元素
 */
LinkedList* list_map(LinkedList* list, void (*mapper)(ListNode*, ListNode*, void*), void* user_data);

/**
 * @brief 折叠/归约链表
 */
bool list_fold_int(LinkedList* list, int initial, int (*func)(int, int, void*), void* user_data, int* result);

/* ==================== 打印调试 ==================== */

/**
 * @brief 打印链表内容
 */
void list_print(LinkedList* list);

/**
 * @brief 打印整数链表
 */
void list_print_int(LinkedList* list);

/**
 * @brief 打印字符串链表
 */
void list_print_string(LinkedList* list);

#ifdef __cplusplus
}
#endif

#endif /* LINKED_LIST_UTILS_H */