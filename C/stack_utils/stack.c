/**
 * @file stack.c
 * @brief Generic Stack Data Structure Implementation
 * 
 * @author AllToolkit
 * @date 2026-04-22
 * @version 1.0.0
 */

#include "stack.h"
#include <stdlib.h>
#include <string.h>

#define DEFAULT_CAPACITY 8
#define GROWTH_FACTOR 2

Stack *stack_create(size_t elem_size, size_t initial_capacity) {
    if (elem_size == 0) {
        return NULL;
    }

    Stack *stack = (Stack *)malloc(sizeof(Stack));
    if (stack == NULL) {
        return NULL;
    }

    stack->elem_size = elem_size;
    stack->size = 0;
    stack->capacity = (initial_capacity > 0) ? initial_capacity : DEFAULT_CAPACITY;

    stack->data = malloc(stack->capacity * elem_size);
    if (stack->data == NULL) {
        free(stack);
        return NULL;
    }

    return stack;
}

void stack_free(Stack **stack) {
    if (stack == NULL || *stack == NULL) {
        return;
    }

    free((*stack)->data);
    free(*stack);
    *stack = NULL;
}

bool stack_push(Stack *stack, const void *elem) {
    if (stack == NULL || elem == NULL) {
        return false;
    }

    /* Check if we need to grow */
    if (stack->size >= stack->capacity) {
        size_t new_capacity = stack->capacity * GROWTH_FACTOR;
        void *new_data = realloc(stack->data, new_capacity * stack->elem_size);
        if (new_data == NULL) {
            return false;
        }
        stack->data = new_data;
        stack->capacity = new_capacity;
    }

    /* Copy element to the top of the stack */
    memcpy((char *)stack->data + (stack->size * stack->elem_size), elem, stack->elem_size);
    stack->size++;

    return true;
}

bool stack_pop(Stack *stack, void *out) {
    if (stack == NULL || stack->size == 0) {
        return false;
    }

    stack->size--;

    if (out != NULL) {
        memcpy(out, (char *)stack->data + (stack->size * stack->elem_size), stack->elem_size);
    }

    return true;
}

bool stack_peek(const Stack *stack, void *out) {
    if (stack == NULL || stack->size == 0 || out == NULL) {
        return false;
    }

    memcpy(out, (char *)stack->data + ((stack->size - 1) * stack->elem_size), stack->elem_size);
    return true;
}

bool stack_is_empty(const Stack *stack) {
    return (stack == NULL || stack->size == 0);
}

size_t stack_size(const Stack *stack) {
    return (stack == NULL) ? 0 : stack->size;
}

size_t stack_capacity(const Stack *stack) {
    return (stack == NULL) ? 0 : stack->capacity;
}

void stack_clear(Stack *stack) {
    if (stack != NULL) {
        stack->size = 0;
    }
}

bool stack_reserve(Stack *stack, size_t capacity) {
    if (stack == NULL) {
        return false;
    }

    if (capacity <= stack->capacity) {
        return true;  /* Already have enough capacity */
    }

    void *new_data = realloc(stack->data, capacity * stack->elem_size);
    if (new_data == NULL) {
        return false;
    }

    stack->data = new_data;
    stack->capacity = capacity;
    return true;
}

bool stack_shrink_to_fit(Stack *stack) {
    if (stack == NULL) {
        return false;
    }

    if (stack->size == 0) {
        /* Shrink to default capacity */
        void *new_data = realloc(stack->data, DEFAULT_CAPACITY * stack->elem_size);
        if (new_data == NULL) {
            return false;
        }
        stack->data = new_data;
        stack->capacity = DEFAULT_CAPACITY;
        return true;
    }

    if (stack->size == stack->capacity) {
        return true;  /* Already at minimum */
    }

    void *new_data = realloc(stack->data, stack->size * stack->elem_size);
    if (new_data == NULL) {
        return false;
    }

    stack->data = new_data;
    stack->capacity = stack->size;
    return true;
}

Stack *stack_copy(const Stack *stack) {
    if (stack == NULL) {
        return NULL;
    }

    Stack *new_stack = stack_create(stack->elem_size, stack->size);
    if (new_stack == NULL) {
        return NULL;
    }

    memcpy(new_stack->data, stack->data, stack->size * stack->elem_size);
    new_stack->size = stack->size;

    return new_stack;
}

void stack_reverse(Stack *stack) {
    if (stack == NULL || stack->size <= 1) {
        return;
    }

    void *temp = malloc(stack->elem_size);
    if (temp == NULL) {
        return;
    }

    size_t left = 0;
    size_t right = stack->size - 1;

    while (left < right) {
        void *left_ptr = (char *)stack->data + (left * stack->elem_size);
        void *right_ptr = (char *)stack->data + (right * stack->elem_size);

        /* Swap elements */
        memcpy(temp, left_ptr, stack->elem_size);
        memcpy(left_ptr, right_ptr, stack->elem_size);
        memcpy(right_ptr, temp, stack->elem_size);

        left++;
        right--;
    }

    free(temp);
}

bool stack_at(const Stack *stack, size_t index, void *out) {
    if (stack == NULL || out == NULL || index >= stack->size) {
        return false;
    }

    /* Index from top: 0 = top element */
    size_t actual_index = stack->size - 1 - index;
    memcpy(out, (char *)stack->data + (actual_index * stack->elem_size), stack->elem_size);
    return true;
}