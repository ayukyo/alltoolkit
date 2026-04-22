/**
 * @file priority_queue.c
 * @brief Generic Priority Queue (Min-Heap) Implementation
 * 
 * @author AllToolkit
 * @date 2026-04-23
 * @version 1.0.0
 */

#include "priority_queue.h"
#include <stdlib.h>
#include <string.h>

#define DEFAULT_CAPACITY 8
#define GROWTH_FACTOR 2

/* ========== Internal Helper Functions ========== */

/**
 * @brief Swap two elements in the heap
 */
static void swap_elements(PQElement *a, PQElement *b) {
    PQElement temp = *a;
    *a = *b;
    *b = temp;
}

/**
 * @brief Heapify up from given index
 */
static void heapify_up(PriorityQueue *pq, size_t index) {
    while (index > 0) {
        size_t parent = (index - 1) / 2;
        if (pq->elements[index].priority >= pq->elements[parent].priority) {
            break;
        }
        swap_elements(&pq->elements[index], &pq->elements[parent]);
        index = parent;
    }
}

/**
 * @brief Heapify down from given index
 */
static void heapify_down(PriorityQueue *pq, size_t index) {
    while (true) {
        size_t left = 2 * index + 1;
        size_t right = 2 * index + 2;
        size_t smallest = index;

        if (left < pq->size && 
            pq->elements[left].priority < pq->elements[smallest].priority) {
            smallest = left;
        }

        if (right < pq->size && 
            pq->elements[right].priority < pq->elements[smallest].priority) {
            smallest = right;
        }

        if (smallest == index) {
            break;
        }

        swap_elements(&pq->elements[index], &pq->elements[smallest]);
        index = smallest;
    }
}

/* ========== Public API Implementation ========== */

PriorityQueue *pq_create(size_t elem_size, size_t initial_capacity) {
    if (elem_size == 0) {
        return NULL;
    }

    PriorityQueue *pq = (PriorityQueue *)malloc(sizeof(PriorityQueue));
    if (pq == NULL) {
        return NULL;
    }

    pq->elem_size = elem_size;
    pq->size = 0;
    pq->capacity = (initial_capacity > 0) ? initial_capacity : DEFAULT_CAPACITY;

    pq->elements = (PQElement *)malloc(pq->capacity * sizeof(PQElement));
    if (pq->elements == NULL) {
        free(pq);
        return NULL;
    }

    /* Pre-allocate data buffers for each element */
    for (size_t i = 0; i < pq->capacity; i++) {
        pq->elements[i].data = malloc(pq->elem_size);
        if (pq->elements[i].data == NULL) {
            /* Clean up on failure */
            for (size_t j = 0; j < i; j++) {
                free(pq->elements[j].data);
            }
            free(pq->elements);
            free(pq);
            return NULL;
        }
        pq->elements[i].priority = 0.0;
    }

    return pq;
}

void pq_free(PriorityQueue **pq) {
    if (pq == NULL || *pq == NULL) {
        return;
    }

    /* Free all data buffers */
    for (size_t i = 0; i < (*pq)->capacity; i++) {
        free((*pq)->elements[i].data);
    }

    free((*pq)->elements);
    free(*pq);
    *pq = NULL;
}

bool pq_insert(PriorityQueue *pq, const void *data, double priority) {
    if (pq == NULL || data == NULL) {
        return false;
    }

    /* Check if we need to grow */
    if (pq->size >= pq->capacity) {
        size_t new_capacity = pq->capacity * GROWTH_FACTOR;
        
        /* Reallocate elements array */
        PQElement *new_elements = (PQElement *)realloc(pq->elements, 
                                                        new_capacity * sizeof(PQElement));
        if (new_elements == NULL) {
            return false;
        }
        
        pq->elements = new_elements;
        
        /* Allocate data buffers for new slots */
        for (size_t i = pq->capacity; i < new_capacity; i++) {
            pq->elements[i].data = malloc(pq->elem_size);
            if (pq->elements[i].data == NULL) {
                /* Rollback on failure */
                for (size_t j = pq->capacity; j < i; j++) {
                    free(pq->elements[j].data);
                }
                pq->elements = (PQElement *)realloc(pq->elements, 
                                                     pq->capacity * sizeof(PQElement));
                return false;
            }
        }
        
        pq->capacity = new_capacity;
    }

    /* Insert at the end */
    memcpy(pq->elements[pq->size].data, data, pq->elem_size);
    pq->elements[pq->size].priority = priority;
    pq->size++;

    /* Restore heap property */
    heapify_up(pq, pq->size - 1);

    return true;
}

bool pq_extract_min(PriorityQueue *pq, void *out, double *out_priority) {
    if (pq == NULL || pq->size == 0) {
        return false;
    }

    /* Copy the minimum element */
    if (out != NULL) {
        memcpy(out, pq->elements[0].data, pq->elem_size);
    }

    if (out_priority != NULL) {
        *out_priority = pq->elements[0].priority;
    }

    /* Move last element to root */
    pq->size--;

    if (pq->size > 0) {
        /* Swap data pointers for efficiency */
        void *temp_data = pq->elements[0].data;
        pq->elements[0].data = pq->elements[pq->size].data;
        pq->elements[pq->size].data = temp_data;
        pq->elements[0].priority = pq->elements[pq->size].priority;

        /* Restore heap property */
        heapify_down(pq, 0);
    }

    return true;
}

bool pq_peek_min(const PriorityQueue *pq, void *out, double *out_priority) {
    if (pq == NULL || pq->size == 0 || out == NULL) {
        return false;
    }

    memcpy(out, pq->elements[0].data, pq->elem_size);

    if (out_priority != NULL) {
        *out_priority = pq->elements[0].priority;
    }

    return true;
}

bool pq_is_empty(const PriorityQueue *pq) {
    return (pq == NULL || pq->size == 0);
}

size_t pq_size(const PriorityQueue *pq) {
    return (pq == NULL) ? 0 : pq->size;
}

size_t pq_capacity(const PriorityQueue *pq) {
    return (pq == NULL) ? 0 : pq->capacity;
}

void pq_clear(PriorityQueue *pq) {
    if (pq != NULL) {
        pq->size = 0;
    }
}

bool pq_reserve(PriorityQueue *pq, size_t capacity) {
    if (pq == NULL) {
        return false;
    }

    if (capacity <= pq->capacity) {
        return true;  /* Already have enough capacity */
    }

    PQElement *new_elements = (PQElement *)realloc(pq->elements, 
                                                    capacity * sizeof(PQElement));
    if (new_elements == NULL) {
        return false;
    }

    pq->elements = new_elements;

    /* Allocate data buffers for new slots */
    for (size_t i = pq->capacity; i < capacity; i++) {
        pq->elements[i].data = malloc(pq->elem_size);
        if (pq->elements[i].data == NULL) {
            /* Rollback on failure */
            for (size_t j = pq->capacity; j < i; j++) {
                free(pq->elements[j].data);
            }
            return false;
        }
    }

    pq->capacity = capacity;
    return true;
}

bool pq_shrink_to_fit(PriorityQueue *pq) {
    if (pq == NULL) {
        return false;
    }

    if (pq->size == 0) {
        /* Shrink to default capacity */
        for (size_t i = DEFAULT_CAPACITY; i < pq->capacity; i++) {
            free(pq->elements[i].data);
        }
        
        PQElement *new_elements = (PQElement *)realloc(pq->elements, 
                                                        DEFAULT_CAPACITY * sizeof(PQElement));
        if (new_elements == NULL) {
            return false;
        }
        
        pq->elements = new_elements;
        pq->capacity = DEFAULT_CAPACITY;
        return true;
    }

    if (pq->size == pq->capacity) {
        return true;  /* Already at minimum */
    }

    /* Free unused data buffers */
    for (size_t i = pq->size; i < pq->capacity; i++) {
        free(pq->elements[i].data);
    }

    PQElement *new_elements = (PQElement *)realloc(pq->elements, 
                                                    pq->size * sizeof(PQElement));
    if (new_elements == NULL) {
        return false;
    }

    pq->elements = new_elements;
    pq->capacity = pq->size;
    return true;
}

bool pq_contains_priority(const PriorityQueue *pq, double priority) {
    if (pq == NULL || pq->size == 0) {
        return false;
    }

    for (size_t i = 0; i < pq->size; i++) {
        if (pq->elements[i].priority == priority) {
            return true;
        }
    }

    return false;
}

bool pq_update_priority(PriorityQueue *pq, const void *data, double new_priority,
                        int (*cmp)(const void *, const void *)) {
    if (pq == NULL || data == NULL || cmp == NULL) {
        return false;
    }

    /* Find the element */
    for (size_t i = 0; i < pq->size; i++) {
        if (cmp(pq->elements[i].data, data) == 0) {
            double old_priority = pq->elements[i].priority;
            pq->elements[i].priority = new_priority;

            /* Restore heap property */
            if (new_priority < old_priority) {
                /* Priority decreased, heapify up */
                heapify_up(pq, i);
            } else if (new_priority > old_priority) {
                /* Priority increased, heapify down */
                heapify_down(pq, i);
            }

            return true;
        }
    }

    return false;
}

bool pq_merge(PriorityQueue *pq, const PriorityQueue *other) {
    if (pq == NULL || other == NULL) {
        return false;
    }

    if (pq->elem_size != other->elem_size) {
        return false;  /* Cannot merge different element sizes */
    }

    /* Reserve capacity if needed */
    size_t new_size = pq->size + other->size;
    if (new_size > pq->capacity) {
        if (!pq_reserve(pq, new_size)) {
            return false;
        }
    }

    /* Insert all elements from other */
    for (size_t i = 0; i < other->size; i++) {
        if (!pq_insert(pq, other->elements[i].data, other->elements[i].priority)) {
            return false;
        }
    }

    return true;
}

bool pq_get_sorted(const PriorityQueue *pq, void *out_data, double *out_priorities) {
    if (pq == NULL || out_data == NULL) {
        return false;
    }

    if (pq->size == 0) {
        return true;
    }

    /* Create a copy of the heap to extract in sorted order */
    PriorityQueue *copy = pq_create(pq->elem_size, pq->size);
    if (copy == NULL) {
        return false;
    }

    /* Copy elements */
    for (size_t i = 0; i < pq->size; i++) {
        memcpy(copy->elements[i].data, pq->elements[i].data, pq->elem_size);
        copy->elements[i].priority = pq->elements[i].priority;
    }
    copy->size = pq->size;

    /* Extract in sorted order */
    char *data_ptr = (char *)out_data;
    for (size_t i = 0; i < pq->size; i++) {
        double priority;
        if (!pq_extract_min(copy, data_ptr + i * pq->elem_size, &priority)) {
            pq_free(&copy);
            return false;
        }
        if (out_priorities != NULL) {
            out_priorities[i] = priority;
        }
    }

    pq_free(&copy);
    return true;
}