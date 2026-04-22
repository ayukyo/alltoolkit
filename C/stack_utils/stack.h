/**
 * @file stack.h
 * @brief Generic Stack Data Structure Implementation
 * 
 * A dynamic, type-agnostic stack implementation using void pointers.
 * Supports any data type with customizable element size.
 * 
 * @author AllToolkit
 * @date 2026-04-22
 * @version 1.0.0
 */

#ifndef STACK_H
#define STACK_H

#include <stddef.h>
#include <stdbool.h>

/**
 * @brief Stack structure
 */
typedef struct {
    void *data;         /**< Pointer to the data array */
    size_t elem_size;   /**< Size of each element in bytes */
    size_t size;        /**< Current number of elements */
    size_t capacity;    /**< Current capacity */
} Stack;

/**
 * @brief Create a new stack
 * @param elem_size Size of each element in bytes
 * @param initial_capacity Initial capacity (0 for default of 8)
 * @return Pointer to new stack, or NULL on failure
 */
Stack *stack_create(size_t elem_size, size_t initial_capacity);

/**
 * @brief Free a stack and its data
 * @param stack Pointer to stack pointer (set to NULL after free)
 */
void stack_free(Stack **stack);

/**
 * @brief Push an element onto the stack
 * @param stack Pointer to stack
 * @param elem Pointer to element to push
 * @return true on success, false on failure
 */
bool stack_push(Stack *stack, const void *elem);

/**
 * @brief Pop an element from the stack
 * @param stack Pointer to stack
 * @param out Pointer to store popped element (can be NULL)
 * @return true on success, false if stack is empty
 */
bool stack_pop(Stack *stack, void *out);

/**
 * @brief Get the top element without removing it
 * @param stack Pointer to stack
 * @param out Pointer to store top element
 * @return true on success, false if stack is empty
 */
bool stack_peek(const Stack *stack, void *out);

/**
 * @brief Check if stack is empty
 * @param stack Pointer to stack
 * @return true if empty, false otherwise
 */
bool stack_is_empty(const Stack *stack);

/**
 * @brief Get the number of elements in the stack
 * @param stack Pointer to stack
 * @return Number of elements
 */
size_t stack_size(const Stack *stack);

/**
 * @brief Get the current capacity of the stack
 * @param stack Pointer to stack
 * @return Current capacity
 */
size_t stack_capacity(const Stack *stack);

/**
 * @brief Clear all elements from the stack
 * @param stack Pointer to stack
 */
void stack_clear(Stack *stack);

/**
 * @brief Reserve capacity for the stack
 * @param stack Pointer to stack
 * @param capacity New capacity
 * @return true on success, false on failure
 */
bool stack_reserve(Stack *stack, size_t capacity);

/**
 * @brief Shrink capacity to fit current size
 * @param stack Pointer to stack
 * @return true on success, false on failure
 */
bool stack_shrink_to_fit(Stack *stack);

/**
 * @brief Copy the stack (deep copy)
 * @param stack Pointer to stack
 * @return Pointer to new stack, or NULL on failure
 */
Stack *stack_copy(const Stack *stack);

/**
 * @brief Reverse the stack order
 * @param stack Pointer to stack
 */
void stack_reverse(Stack *stack);

/**
 * @brief Get element at specific index from top (0 = top)
 * @param stack Pointer to stack
 * @param index Index from top (0 = top element)
 * @param out Pointer to store element
 * @return true on success, false if index out of bounds
 */
bool stack_at(const Stack *stack, size_t index, void *out);

/* ========== Convenience Macros for Common Types ========== */

/**
 * @brief Create a stack for integers
 */
#define stack_create_int() stack_create(sizeof(int), 0)

/**
 * @brief Create a stack for doubles
 */
#define stack_create_double() stack_create(sizeof(double), 0)

/**
 * @brief Create a stack for characters
 */
#define stack_create_char() stack_create(sizeof(char), 0)

/**
 * @brief Create a stack for size_t
 */
#define stack_create_size() stack_create(sizeof(size_t), 0)

/**
 * @brief Push an integer
 */
#define stack_push_int(s, v) do { int _v = (v); stack_push((s), &_v); } while(0)

/**
 * @brief Push a double
 */
#define stack_push_double(s, v) do { double _v = (v); stack_push((s), &_v); } while(0)

/**
 * @brief Push a character
 */
#define stack_push_char(s, v) do { char _v = (v); stack_push((s), &_v); } while(0)

/**
 * @brief Pop an integer
 */
#define stack_pop_int(s, out) stack_pop((s), (out))

/**
 * @brief Pop a double
 */
#define stack_pop_double(s, out) stack_pop((s), (out))

/**
 * @brief Pop a character
 */
#define stack_pop_char(s, out) stack_pop((s), (out))

/**
 * @brief Peek integer
 */
#define stack_peek_int(s, out) stack_peek((s), (out))

/**
 * @brief Peek double
 */
#define stack_peek_double(s, out) stack_peek((s), (out))

/**
 * @brief Peek character
 */
#define stack_peek_char(s, out) stack_peek((s), (out))

#endif /* STACK_H */