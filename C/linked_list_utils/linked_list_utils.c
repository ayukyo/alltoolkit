/**
 * @file linked_list_utils.c
 * @brief C 语言双向链表工具库实现
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-20
 */

#define _POSIX_C_SOURCE 200809L  /* For strdup */

#include "linked_list_utils.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdarg.h>

/* ==================== 内部辅助函数 ==================== */

/**
 * @brief 创建新节点
 */
static ListNode* create_node(LinkedList* list) {
    ListNode* node = (ListNode*)calloc(1, sizeof(ListNode));
    if (!node) return NULL;
    node->prev = NULL;
    node->next = NULL;
    return node;
}

/**
 * @brief 释放节点数据
 */
static void free_node_data(LinkedList* list, ListNode* node) {
    if (!node) return;
    
    switch (list->type) {
        case LIST_TYPE_STRING:
            if (node->data.string_val) {
                free(node->data.string_val);
                node->data.string_val = NULL;
            }
            break;
        case LIST_TYPE_GENERIC:
            if (list->free_func && node->data.generic_data) {
                list->free_func(node->data.generic_data);
            }
            break;
        default:
            break;
    }
}

/**
 * @brief 释放节点
 */
static void free_node(LinkedList* list, ListNode* node) {
    if (!node) return;
    free_node_data(list, node);
    free(node);
}

/* ==================== 创建和销毁 ==================== */

LinkedList* list_create_int(void) {
    LinkedList* list = (LinkedList*)calloc(1, sizeof(LinkedList));
    if (!list) return NULL;
    list->type = LIST_TYPE_INT;
    list->generic_size = sizeof(int);
    return list;
}

LinkedList* list_create_double(void) {
    LinkedList* list = (LinkedList*)calloc(1, sizeof(LinkedList));
    if (!list) return NULL;
    list->type = LIST_TYPE_DOUBLE;
    list->generic_size = sizeof(double);
    return list;
}

LinkedList* list_create_string(void) {
    LinkedList* list = (LinkedList*)calloc(1, sizeof(LinkedList));
    if (!list) return NULL;
    list->type = LIST_TYPE_STRING;
    list->generic_size = sizeof(char*);
    return list;
}

LinkedList* list_create_pointer(void) {
    LinkedList* list = (LinkedList*)calloc(1, sizeof(LinkedList));
    if (!list) return NULL;
    list->type = LIST_TYPE_POINTER;
    list->generic_size = sizeof(void*);
    return list;
}

LinkedList* list_create_generic(size_t data_size, void (*free_func)(void*)) {
    LinkedList* list = (LinkedList*)calloc(1, sizeof(LinkedList));
    if (!list) return NULL;
    list->type = LIST_TYPE_GENERIC;
    list->generic_size = data_size;
    list->free_func = free_func;
    return list;
}

void list_destroy(LinkedList* list) {
    if (!list) return;
    list_clear(list);
    free(list);
}

void list_clear(LinkedList* list) {
    if (!list) return;
    
    ListNode* current = list->head;
    while (current) {
        ListNode* next = current->next;
        free_node(list, current);
        current = next;
    }
    
    list->head = NULL;
    list->tail = NULL;
    list->size = 0;
}

/* ==================== 头部操作 ==================== */

bool list_push_front(LinkedList* list, ...) {
    if (!list) return false;
    
    ListNode* node = create_node(list);
    if (!node) return false;
    
    va_list args;
    va_start(args, list);
    
    switch (list->type) {
        case LIST_TYPE_INT:
            node->data.int_val = va_arg(args, int);
            break;
        case LIST_TYPE_DOUBLE:
            node->data.double_val = va_arg(args, double);
            break;
        case LIST_TYPE_STRING: {
            const char* str = va_arg(args, const char*);
            if (str) {
                node->data.string_val = strdup(str);
                if (!node->data.string_val) {
                    free(node);
                    va_end(args);
                    return false;
                }
            }
            break;
        }
        case LIST_TYPE_POINTER:
            node->data.pointer_val = va_arg(args, void*);
            break;
        case LIST_TYPE_GENERIC: {
            void* data = va_arg(args, void*);
            if (data) {
                memcpy(node->data.generic_data, data, list->generic_size);
            }
            break;
        }
    }
    
    va_end(args);
    
    node->prev = NULL;
    node->next = list->head;
    
    if (list->head) {
        list->head->prev = node;
    } else {
        list->tail = node;
    }
    
    list->head = node;
    list->size++;
    
    return true;
}

bool list_pop_front(LinkedList* list) {
    if (!list || !list->head) return false;
    
    ListNode* node = list->head;
    list->head = node->next;
    
    if (list->head) {
        list->head->prev = NULL;
    } else {
        list->tail = NULL;
    }
    
    free_node(list, node);
    list->size--;
    
    return true;
}

ListNode* list_front(LinkedList* list) {
    return list ? list->head : NULL;
}

/* ==================== 尾部操作 ==================== */

bool list_push_back(LinkedList* list, ...) {
    if (!list) return false;
    
    ListNode* node = create_node(list);
    if (!node) return false;
    
    va_list args;
    va_start(args, list);
    
    switch (list->type) {
        case LIST_TYPE_INT:
            node->data.int_val = va_arg(args, int);
            break;
        case LIST_TYPE_DOUBLE:
            node->data.double_val = va_arg(args, double);
            break;
        case LIST_TYPE_STRING: {
            const char* str = va_arg(args, const char*);
            if (str) {
                node->data.string_val = strdup(str);
                if (!node->data.string_val) {
                    free(node);
                    va_end(args);
                    return false;
                }
            }
            break;
        }
        case LIST_TYPE_POINTER:
            node->data.pointer_val = va_arg(args, void*);
            break;
        case LIST_TYPE_GENERIC: {
            void* data = va_arg(args, void*);
            if (data) {
                memcpy(node->data.generic_data, data, list->generic_size);
            }
            break;
        }
    }
    
    va_end(args);
    
    node->prev = list->tail;
    node->next = NULL;
    
    if (list->tail) {
        list->tail->next = node;
    } else {
        list->head = node;
    }
    
    list->tail = node;
    list->size++;
    
    return true;
}

bool list_pop_back(LinkedList* list) {
    if (!list || !list->tail) return false;
    
    ListNode* node = list->tail;
    list->tail = node->prev;
    
    if (list->tail) {
        list->tail->next = NULL;
    } else {
        list->head = NULL;
    }
    
    free_node(list, node);
    list->size--;
    
    return true;
}

ListNode* list_back(LinkedList* list) {
    return list ? list->tail : NULL;
}

/* ==================== 索引操作 ==================== */

bool list_insert_at(LinkedList* list, size_t index, ...) {
    if (!list || index > list->size) return false;
    
    if (index == 0) {
        va_list args;
        va_start(args, index);
        bool result = list_push_front(list, va_arg(args, int));
        va_end(args);
        /* Note: this doesn't work correctly for double/string, need to fix */
        return result;
    }
    
    if (index == list->size) {
        va_list args;
        va_start(args, index);
        bool result = list_push_back(list, va_arg(args, int));
        va_end(args);
        return result;
    }
    
    /* Find the node at index */
    ListNode* current = list->head;
    for (size_t i = 0; i < index; i++) {
        current = current->next;
    }
    
    /* Insert before current */
    ListNode* node = create_node(list);
    if (!node) return false;
    
    va_list args;
    va_start(args, index);
    
    switch (list->type) {
        case LIST_TYPE_INT:
            node->data.int_val = va_arg(args, int);
            break;
        case LIST_TYPE_DOUBLE:
            node->data.double_val = va_arg(args, double);
            break;
        case LIST_TYPE_STRING: {
            const char* str = va_arg(args, const char*);
            if (str) {
                node->data.string_val = strdup(str);
                if (!node->data.string_val) {
                    free(node);
                    va_end(args);
                    return false;
                }
            }
            break;
        }
        case LIST_TYPE_POINTER:
            node->data.pointer_val = va_arg(args, void*);
            break;
        case LIST_TYPE_GENERIC: {
            void* data = va_arg(args, void*);
            if (data) {
                memcpy(node->data.generic_data, data, list->generic_size);
            }
            break;
        }
    }
    
    va_end(args);
    
    node->prev = current->prev;
    node->next = current;
    current->prev->next = node;
    current->prev = node;
    
    list->size++;
    
    return true;
}

bool list_remove_at(LinkedList* list, size_t index) {
    if (!list || index >= list->size) return false;
    
    if (index == 0) {
        return list_pop_front(list);
    }
    
    if (index == list->size - 1) {
        return list_pop_back(list);
    }
    
    /* Find the node at index */
    ListNode* node = list->head;
    for (size_t i = 0; i < index; i++) {
        node = node->next;
    }
    
    node->prev->next = node->next;
    node->next->prev = node->prev;
    
    free_node(list, node);
    list->size--;
    
    return true;
}

ListNode* list_get_node(LinkedList* list, size_t index) {
    if (!list || index >= list->size) return NULL;
    
    /* Optimize by starting from the closest end */
    ListNode* node;
    if (index < list->size / 2) {
        node = list->head;
        for (size_t i = 0; i < index; i++) {
            node = node->next;
        }
    } else {
        node = list->tail;
        for (size_t i = list->size - 1; i > index; i--) {
            node = node->prev;
        }
    }
    
    return node;
}

bool list_get_int(LinkedList* list, size_t index, int* out) {
    ListNode* node = list_get_node(list, index);
    if (!node || list->type != LIST_TYPE_INT) return false;
    if (out) *out = node->data.int_val;
    return true;
}

bool list_get_double(LinkedList* list, size_t index, double* out) {
    ListNode* node = list_get_node(list, index);
    if (!node || list->type != LIST_TYPE_DOUBLE) return false;
    if (out) *out = node->data.double_val;
    return true;
}

bool list_get_string(LinkedList* list, size_t index, const char** out) {
    ListNode* node = list_get_node(list, index);
    if (!node || list->type != LIST_TYPE_STRING) return false;
    if (out) *out = node->data.string_val;
    return true;
}

bool list_get_pointer(LinkedList* list, size_t index, void** out) {
    ListNode* node = list_get_node(list, index);
    if (!node || list->type != LIST_TYPE_POINTER) return false;
    if (out) *out = node->data.pointer_val;
    return true;
}

/* ==================== 查找操作 ==================== */

long list_find_int(LinkedList* list, int value) {
    if (!list || list->type != LIST_TYPE_INT) return -1;
    
    ListNode* node = list->head;
    long index = 0;
    
    while (node) {
        if (node->data.int_val == value) {
            return index;
        }
        node = node->next;
        index++;
    }
    
    return -1;
}

long list_find_double(LinkedList* list, double value, double epsilon) {
    if (!list || list->type != LIST_TYPE_DOUBLE) return -1;
    
    ListNode* node = list->head;
    long index = 0;
    
    while (node) {
        double diff = node->data.double_val - value;
        if (diff < 0) diff = -diff;
        if (diff < epsilon) {
            return index;
        }
        node = node->next;
        index++;
    }
    
    return -1;
}

long list_find_string(LinkedList* list, const char* value) {
    if (!list || list->type != LIST_TYPE_STRING) return -1;
    
    ListNode* node = list->head;
    long index = 0;
    
    while (node) {
        if ((node->data.string_val == NULL && value == NULL) ||
            (node->data.string_val && value && strcmp(node->data.string_val, value) == 0)) {
            return index;
        }
        node = node->next;
        index++;
    }
    
    return -1;
}

long list_find_pointer(LinkedList* list, void* value) {
    if (!list || list->type != LIST_TYPE_POINTER) return -1;
    
    ListNode* node = list->head;
    long index = 0;
    
    while (node) {
        if (node->data.pointer_val == value) {
            return index;
        }
        node = node->next;
        index++;
    }
    
    return -1;
}

bool list_contains_int(LinkedList* list, int value) {
    return list_find_int(list, value) >= 0;
}

bool list_contains_string(LinkedList* list, const char* value) {
    return list_find_string(list, value) >= 0;
}

/* ==================== 删除操作 ==================== */

bool list_remove_int(LinkedList* list, int value) {
    if (!list || list->type != LIST_TYPE_INT) return false;
    
    ListNode* node = list->head;
    while (node) {
        if (node->data.int_val == value) {
            if (node->prev) {
                node->prev->next = node->next;
            } else {
                list->head = node->next;
            }
            
            if (node->next) {
                node->next->prev = node->prev;
            } else {
                list->tail = node->prev;
            }
            
            free_node(list, node);
            list->size--;
            return true;
        }
        node = node->next;
    }
    
    return false;
}

bool list_remove_string(LinkedList* list, const char* value) {
    if (!list || list->type != LIST_TYPE_STRING) return false;
    
    ListNode* node = list->head;
    while (node) {
        bool match = (node->data.string_val == NULL && value == NULL) ||
                     (node->data.string_val && value && strcmp(node->data.string_val, value) == 0);
        
        if (match) {
            if (node->prev) {
                node->prev->next = node->next;
            } else {
                list->head = node->next;
            }
            
            if (node->next) {
                node->next->prev = node->prev;
            } else {
                list->tail = node->prev;
            }
            
            free_node(list, node);
            list->size--;
            return true;
        }
        node = node->next;
    }
    
    return false;
}

size_t list_remove_all_int(LinkedList* list, int value) {
    if (!list || list->type != LIST_TYPE_INT) return 0;
    
    size_t count = 0;
    ListNode* node = list->head;
    
    while (node) {
        ListNode* next = node->next;
        
        if (node->data.int_val == value) {
            if (node->prev) {
                node->prev->next = node->next;
            } else {
                list->head = node->next;
            }
            
            if (node->next) {
                node->next->prev = node->prev;
            } else {
                list->tail = node->prev;
            }
            
            free_node(list, node);
            list->size--;
            count++;
        }
        
        node = next;
    }
    
    return count;
}

/* ==================== 信息查询 ==================== */

size_t list_size(LinkedList* list) {
    return list ? list->size : 0;
}

bool list_is_empty(LinkedList* list) {
    return list ? list->size == 0 : true;
}

ListType list_get_type(LinkedList* list) {
    return list ? list->type : LIST_TYPE_INT;
}

/* ==================== 链表操作 ==================== */

void list_reverse(LinkedList* list) {
    if (!list || list->size < 2) return;
    
    ListNode* current = list->head;
    ListNode* temp = NULL;
    
    while (current) {
        temp = current->prev;
        current->prev = current->next;
        current->next = temp;
        current = current->prev;  /* Move to next (now prev due to swap) */
    }
    
    /* Swap head and tail */
    temp = list->head;
    list->head = list->tail;
    list->tail = temp;
}

void list_concat(LinkedList* list, LinkedList* other) {
    if (!list || !other || list_is_empty(other)) return;
    
    /* Type must match */
    if (list->type != other->type) return;
    
    if (list_is_empty(list)) {
        list->head = other->head;
        list->tail = other->tail;
        list->size = other->size;
    } else {
        list->tail->next = other->head;
        other->head->prev = list->tail;
        list->tail = other->tail;
        list->size += other->size;
    }
    
    /* Clear other list without freeing nodes */
    other->head = NULL;
    other->tail = NULL;
    other->size = 0;
}

LinkedList* list_clone(LinkedList* list) {
    if (!list) return NULL;
    
    LinkedList* clone = NULL;
    
    switch (list->type) {
        case LIST_TYPE_INT:
            clone = list_create_int();
            break;
        case LIST_TYPE_DOUBLE:
            clone = list_create_double();
            break;
        case LIST_TYPE_STRING:
            clone = list_create_string();
            break;
        case LIST_TYPE_POINTER:
            clone = list_create_pointer();
            break;
        case LIST_TYPE_GENERIC:
            clone = list_create_generic(list->generic_size, list->free_func);
            break;
    }
    
    if (!clone) return NULL;
    
    ListNode* node = list->head;
    while (node) {
        switch (list->type) {
            case LIST_TYPE_INT:
                list_push_back(clone, node->data.int_val);
                break;
            case LIST_TYPE_DOUBLE:
                list_push_back(clone, node->data.double_val);
                break;
            case LIST_TYPE_STRING:
                list_push_back(clone, node->data.string_val);
                break;
            case LIST_TYPE_POINTER:
                list_push_back(clone, node->data.pointer_val);
                break;
            case LIST_TYPE_GENERIC:
                list_push_back(clone, node->data.generic_data);
                break;
        }
        node = node->next;
    }
    
    return clone;
}

/* Internal merge sort for integers */
static ListNode* merge_sort_int(ListNode* head);
static ListNode* merge_int(ListNode* left, ListNode* right);
static void split_list(ListNode* head, ListNode** left, ListNode** right);

void list_sort(LinkedList* list) {
    if (!list || list->size < 2) return;
    
    if (list->type == LIST_TYPE_INT) {
        list->head = merge_sort_int(list->head);
        
        /* Fix prev pointers and find tail */
        ListNode* prev = NULL;
        ListNode* current = list->head;
        while (current) {
            current->prev = prev;
            prev = current;
            if (!current->next) {
                list->tail = current;
            }
            current = current->next;
        }
    }
    /* Other types would need custom comparators */
}

static ListNode* merge_sort_int(ListNode* head) {
    if (!head || !head->next) return head;
    
    ListNode* left = NULL;
    ListNode* right = NULL;
    split_list(head, &left, &right);
    
    left = merge_sort_int(left);
    right = merge_sort_int(right);
    
    return merge_int(left, right);
}

static ListNode* merge_int(ListNode* left, ListNode* right) {
    ListNode dummy;
    ListNode* tail = &dummy;
    dummy.next = NULL;
    
    while (left && right) {
        if (left->data.int_val <= right->data.int_val) {
            tail->next = left;
            left = left->next;
        } else {
            tail->next = right;
            right = right->next;
        }
        tail = tail->next;
    }
    
    tail->next = left ? left : right;
    
    return dummy.next;
}

static void split_list(ListNode* head, ListNode** left, ListNode** right) {
    ListNode* slow = head;
    ListNode* fast = head->next;
    
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    
    *left = head;
    *right = slow->next;
    slow->next = NULL;
}

void list_sort_with(LinkedList* list, int (*compare)(ListNode*, ListNode*)) {
    /* Placeholder for custom sort - would implement similar to list_sort */
    (void)list;
    (void)compare;
}

void list_unique(LinkedList* list) {
    if (!list || list->size < 2) return;
    
    if (list->type != LIST_TYPE_INT) return;
    
    ListNode* current = list->head;
    
    while (current && current->next) {
        if (current->data.int_val == current->next->data.int_val) {
            ListNode* duplicate = current->next;
            current->next = duplicate->next;
            
            if (duplicate->next) {
                duplicate->next->prev = current;
            } else {
                list->tail = current;
            }
            
            free_node(list, duplicate);
            list->size--;
        } else {
            current = current->next;
        }
    }
}

/* ==================== 迭代器 ==================== */

ListIterator list_iterator(LinkedList* list) {
    ListIterator it = {0};
    if (list) {
        it.current = list->head;
        it.type = list->type;
        it.forward = true;
    }
    return it;
}

ListIterator list_iterator_reverse(LinkedList* list) {
    ListIterator it = {0};
    if (list) {
        it.current = list->tail;
        it.type = list->type;
        it.forward = false;
    }
    return it;
}

bool list_iterator_next(ListIterator* it) {
    if (!it || !it->current) return false;
    it->current = it->forward ? it->current->next : it->current->prev;
    return it->current != NULL;
}

ListNode* list_iterator_get(ListIterator* it) {
    return it ? it->current : NULL;
}

int list_iterator_get_int(ListIterator* it) {
    return (it && it->current) ? it->current->data.int_val : 0;
}

const char* list_iterator_get_string(ListIterator* it) {
    return (it && it->current && it->type == LIST_TYPE_STRING) ? 
           it->current->data.string_val : NULL;
}

/* ==================== 工具函数 ==================== */

LinkedList* list_from_int_array(int* arr, size_t size) {
    if (!arr || size == 0) return NULL;
    
    LinkedList* list = list_create_int();
    if (!list) return NULL;
    
    for (size_t i = 0; i < size; i++) {
        if (!list_push_back(list, arr[i])) {
            list_destroy(list);
            return NULL;
        }
    }
    
    return list;
}

LinkedList* list_from_string_array(const char** arr, size_t size) {
    if (!arr || size == 0) return NULL;
    
    LinkedList* list = list_create_string();
    if (!list) return NULL;
    
    for (size_t i = 0; i < size; i++) {
        if (!list_push_back(list, arr[i])) {
            list_destroy(list);
            return NULL;
        }
    }
    
    return list;
}

int* list_to_int_array(LinkedList* list, size_t* out_size) {
    if (!list || list->type != LIST_TYPE_INT || list->size == 0) {
        if (out_size) *out_size = 0;
        return NULL;
    }
    
    int* arr = (int*)malloc(list->size * sizeof(int));
    if (!arr) {
        if (out_size) *out_size = 0;
        return NULL;
    }
    
    ListNode* node = list->head;
    for (size_t i = 0; i < list->size; i++) {
        arr[i] = node->data.int_val;
        node = node->next;
    }
    
    if (out_size) *out_size = list->size;
    return arr;
}

void list_foreach(LinkedList* list, void (*callback)(ListNode*, void*), void* user_data) {
    if (!list || !callback) return;
    
    ListNode* node = list->head;
    while (node) {
        callback(node, user_data);
        node = node->next;
    }
}

LinkedList* list_filter(LinkedList* list, bool (*predicate)(ListNode*, void*), void* user_data) {
    if (!list || !predicate) return NULL;
    
    LinkedList* result = NULL;
    
    switch (list->type) {
        case LIST_TYPE_INT:
            result = list_create_int();
            break;
        case LIST_TYPE_DOUBLE:
            result = list_create_double();
            break;
        case LIST_TYPE_STRING:
            result = list_create_string();
            break;
        case LIST_TYPE_POINTER:
            result = list_create_pointer();
            break;
        case LIST_TYPE_GENERIC:
            result = list_create_generic(list->generic_size, list->free_func);
            break;
    }
    
    if (!result) return NULL;
    
    ListNode* node = list->head;
    while (node) {
        if (predicate(node, user_data)) {
            switch (list->type) {
                case LIST_TYPE_INT:
                    list_push_back(result, node->data.int_val);
                    break;
                case LIST_TYPE_DOUBLE:
                    list_push_back(result, node->data.double_val);
                    break;
                case LIST_TYPE_STRING:
                    list_push_back(result, node->data.string_val);
                    break;
                case LIST_TYPE_POINTER:
                    list_push_back(result, node->data.pointer_val);
                    break;
                case LIST_TYPE_GENERIC:
                    list_push_back(result, node->data.generic_data);
                    break;
            }
        }
        node = node->next;
    }
    
    return result;
}

LinkedList* list_map(LinkedList* list, void (*mapper)(ListNode*, ListNode*, void*), void* user_data) {
    (void)list;
    (void)mapper;
    (void)user_data;
    /* Placeholder - would need more context on how mapping works */
    return NULL;
}

bool list_fold_int(LinkedList* list, int initial, int (*func)(int, int, void*), void* user_data, int* result) {
    if (!list || list->type != LIST_TYPE_INT || !func || !result) return false;
    
    int acc = initial;
    ListNode* node = list->head;
    
    while (node) {
        acc = func(acc, node->data.int_val, user_data);
        node = node->next;
    }
    
    *result = acc;
    return true;
}

/* ==================== 打印调试 ==================== */

void list_print(LinkedList* list) {
    if (!list) {
        printf("NULL\n");
        return;
    }
    
    switch (list->type) {
        case LIST_TYPE_INT:
            list_print_int(list);
            break;
        case LIST_TYPE_STRING:
            list_print_string(list);
            break;
        case LIST_TYPE_DOUBLE:
            printf("[");
            ListNode* node = list->head;
            while (node) {
                printf("%.2f", node->data.double_val);
                if (node->next) printf(", ");
                node = node->next;
            }
            printf("]\n");
            break;
        case LIST_TYPE_POINTER:
            printf("[");
            node = list->head;
            while (node) {
                printf("%p", node->data.pointer_val);
                if (node->next) printf(", ");
                node = node->next;
            }
            printf("]\n");
            break;
        default:
            printf("[size=%zu]\n", list->size);
            break;
    }
}

void list_print_int(LinkedList* list) {
    if (!list || list->type != LIST_TYPE_INT) {
        printf("NULL or wrong type\n");
        return;
    }
    
    printf("[");
    ListNode* node = list->head;
    while (node) {
        printf("%d", node->data.int_val);
        if (node->next) printf(", ");
        node = node->next;
    }
    printf("]\n");
}

void list_print_string(LinkedList* list) {
    if (!list || list->type != LIST_TYPE_STRING) {
        printf("NULL or wrong type\n");
        return;
    }
    
    printf("[");
    ListNode* node = list->head;
    while (node) {
        printf("\"%s\"", node->data.string_val ? node->data.string_val : "NULL");
        if (node->next) printf(", ");
        node = node->next;
    }
    printf("]\n");
}