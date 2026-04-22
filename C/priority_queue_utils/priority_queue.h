/**
 * @file priority_queue.h
 * @brief Generic Priority Queue (Min-Heap) Implementation
 * 
 * A dynamic, type-agnostic priority queue implementation using a binary min-heap.
 * Supports any data type with customizable element size and comparison function.
 * Lower priority values are dequeued first (min-heap property).
 * 
 * @author AllToolkit
 * @date 2026-04-23
 * @version 1.0.0
 */

#ifndef PRIORITY_QUEUE_H
#define PRIORITY_QUEUE_H

#include <stddef.h>
#include <stdbool.h>

/**
 * @brief Priority queue element structure
 * 
 * Each element stores its data and priority value.
 * Lower priority values are dequeued first.
 */
typedef struct {
    void *data;         /**< Pointer to the element data */
    double priority;    /**< Priority value (lower = higher precedence) */
} PQElement;

/**
 * @brief Priority queue structure
 */
typedef struct {
    PQElement *elements;    /**< Array of elements */
    size_t elem_size;        /**< Size of each data element in bytes */
    size_t size;             /**< Current number of elements */
    size_t capacity;         /**< Current capacity */
} PriorityQueue;

/**
 * @brief Create a new priority queue
 * @param elem_size Size of each data element in bytes
 * @param initial_capacity Initial capacity (0 for default of 8)
 * @return Pointer to new priority queue, or NULL on failure
 */
PriorityQueue *pq_create(size_t elem_size, size_t initial_capacity);

/**
 * @brief Free a priority queue and its data
 * @param pq Pointer to priority queue pointer (set to NULL after free)
 */
void pq_free(PriorityQueue **pq);

/**
 * @brief Insert an element with given priority
 * @param pq Pointer to priority queue
 * @param data Pointer to data to insert
 * @param priority Priority value (lower = higher precedence)
 * @return true on success, false on failure
 */
bool pq_insert(PriorityQueue *pq, const void *data, double priority);

/**
 * @brief Remove and return the minimum priority element
 * @param pq Pointer to priority queue
 * @param out Pointer to store the extracted data (can be NULL)
 * @param out_priority Pointer to store the priority (can be NULL)
 * @return true on success, false if queue is empty
 */
bool pq_extract_min(PriorityQueue *pq, void *out, double *out_priority);

/**
 * @brief Get the minimum priority element without removing it
 * @param pq Pointer to priority queue
 * @param out Pointer to store the peeked data
 * @param out_priority Pointer to store the priority (can be NULL)
 * @return true on success, false if queue is empty
 */
bool pq_peek_min(const PriorityQueue *pq, void *out, double *out_priority);

/**
 * @brief Check if priority queue is empty
 * @param pq Pointer to priority queue
 * @return true if empty, false otherwise
 */
bool pq_is_empty(const PriorityQueue *pq);

/**
 * @brief Get the number of elements in the priority queue
 * @param pq Pointer to priority queue
 * @return Number of elements
 */
size_t pq_size(const PriorityQueue *pq);

/**
 * @brief Get the current capacity of the priority queue
 * @param pq Pointer to priority queue
 * @return Current capacity
 */
size_t pq_capacity(const PriorityQueue *pq);

/**
 * @brief Clear all elements from the priority queue
 * @param pq Pointer to priority queue
 */
void pq_clear(PriorityQueue *pq);

/**
 * @brief Reserve capacity for the priority queue
 * @param pq Pointer to priority queue
 * @param capacity New capacity
 * @return true on success, false on failure
 */
bool pq_reserve(PriorityQueue *pq, size_t capacity);

/**
 * @brief Shrink capacity to fit current size
 * @param pq Pointer to priority queue
 * @return true on success, false on failure
 */
bool pq_shrink_to_fit(PriorityQueue *pq);

/**
 * @brief Check if an element with given priority exists
 * @param pq Pointer to priority queue
 * @param priority Priority value to search for
 * @return true if found, false otherwise
 */
bool pq_contains_priority(const PriorityQueue *pq, double priority);

/**
 * @brief Update the priority of an element (finds by data comparison)
 * @param pq Pointer to priority queue
 * @param data Pointer to data to find
 * @param new_priority New priority value
 * @param cmp Comparison function (returns 0 if equal)
 * @return true if found and updated, false otherwise
 */
bool pq_update_priority(PriorityQueue *pq, const void *data, double new_priority,
                        int (*cmp)(const void *, const void *));

/**
 * @brief Merge another priority queue into this one
 * @param pq Destination priority queue
 * @param other Source priority queue (not modified)
 * @return true on success, false on failure
 */
bool pq_merge(PriorityQueue *pq, const PriorityQueue *other);

/**
 * @brief Get all elements sorted by priority (does not modify queue)
 * @param pq Pointer to priority queue
 * @param out_data Array to store sorted data (must have space for pq_size elements)
 * @param out_priorities Array to store sorted priorities (can be NULL)
 * @return true on success, false on failure
 */
bool pq_get_sorted(const PriorityQueue *pq, void *out_data, double *out_priorities);

/* ========== Convenience Macros for Common Types ========== */

/**
 * @brief Create a priority queue for integers
 */
#define pq_create_int() pq_create(sizeof(int), 0)

/**
 * @brief Create a priority queue for doubles
 */
#define pq_create_double() pq_create(sizeof(double), 0)

/**
 * @brief Create a priority queue for characters
 */
#define pq_create_char() pq_create(sizeof(char), 0)

/**
 * @brief Create a priority queue for size_t
 */
#define pq_create_size() pq_create(sizeof(size_t), 0)

/**
 * @brief Insert an integer
 */
#define pq_insert_int(pq, val, pri) do { int _v = (val); pq_insert((pq), &_v, (pri)); } while(0)

/**
 * @brief Insert a double
 */
#define pq_insert_double(pq, val, pri) do { double _v = (val); pq_insert((pq), &_v, (pri)); } while(0)

/**
 * @brief Insert a character
 */
#define pq_insert_char(pq, val, pri) do { char _v = (val); pq_insert((pq), &_v, (pri)); } while(0)

/**
 * @brief Extract an integer
 */
#define pq_extract_int(pq, out, pri) pq_extract_min((pq), (out), (pri))

/**
 * @brief Extract a double
 */
#define pq_extract_double(pq, out, pri) pq_extract_min((pq), (out), (pri))

/**
 * @brief Extract a character
 */
#define pq_extract_char(pq, out, pri) pq_extract_min((pq), (out), (pri))

/**
 * @brief Peek integer
 */
#define pq_peek_int(pq, out, pri) pq_peek_min((pq), (out), (pri))

/**
 * @brief Peek double
 */
#define pq_peek_double(pq, out, pri) pq_peek_min((pq), (out), (pri))

/**
 * @brief Peek character
 */
#define pq_peek_char(pq, out, pri) pq_peek_min((pq), (out), (pri))

#endif /* PRIORITY_QUEUE_H */