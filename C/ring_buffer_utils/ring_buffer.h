/**
 * Ring Buffer (Circular Buffer) Utility
 * 
 * A thread-safe circular buffer implementation for C.
 * Useful for embedded systems, audio processing, and data streaming.
 * 
 * Features:
 * - Fixed-size buffer with O(1) read/write operations
 * - Thread-safe operations with optional mutex support
 * - Full/empty state detection
 * - Peek and skip operations
 * - Zero-copy access where possible
 * 
 * License: MIT
 */

#ifndef RING_BUFFER_H
#define RING_BUFFER_H

#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Ring buffer structure
 */
typedef struct {
    uint8_t *buffer;        /* Pointer to the data buffer */
    size_t capacity;        /* Total capacity of the buffer */
    size_t head;            /* Write position */
    size_t tail;            /* Read position */
    size_t count;           /* Number of elements currently in buffer */
    bool is_dynamic;        /* Whether buffer was dynamically allocated */
} ring_buffer_t;

/**
 * Error codes
 */
typedef enum {
    RING_BUFFER_OK = 0,
    RING_BUFFER_ERROR_NULL = -1,
    RING_BUFFER_ERROR_FULL = -2,
    RING_BUFFER_ERROR_EMPTY = -3,
    RING_BUFFER_ERROR_NO_MEMORY = -4,
    RING_BUFFER_ERROR_INVALID_SIZE = -5,
    RING_BUFFER_ERROR_INVALID_ARGUMENT = -6
} ring_buffer_error_t;

/**
 * Initialize a ring buffer with a pre-allocated buffer
 * 
 * @param rb        Pointer to ring buffer structure
 * @param buffer    Pre-allocated buffer memory
 * @param capacity  Size of the buffer in bytes
 * @return          RING_BUFFER_OK on success, error code otherwise
 */
ring_buffer_error_t ring_buffer_init(ring_buffer_t *rb, uint8_t *buffer, size_t capacity);

/**
 * Create a ring buffer with dynamic memory allocation
 * 
 * @param rb        Pointer to ring buffer structure
 * @param capacity  Desired capacity in bytes
 * @return          RING_BUFFER_OK on success, error code otherwise
 */
ring_buffer_error_t ring_buffer_create(ring_buffer_t *rb, size_t capacity);

/**
 * Free dynamically allocated buffer memory
 * 
 * @param rb        Pointer to ring buffer structure
 */
void ring_buffer_destroy(ring_buffer_t *rb);

/**
 * Reset the buffer to empty state
 * 
 * @param rb        Pointer to ring buffer structure
 * @return          RING_BUFFER_OK on success, error code otherwise
 */
ring_buffer_error_t ring_buffer_reset(ring_buffer_t *rb);

/**
 * Write data to the buffer
 * 
 * @param rb        Pointer to ring buffer structure
 * @param data      Pointer to data to write
 * @param len       Number of bytes to write
 * @return          Number of bytes written, or negative error code
 */
int ring_buffer_write(ring_buffer_t *rb, const uint8_t *data, size_t len);

/**
 * Write a single byte to the buffer
 * 
 * @param rb        Pointer to ring buffer structure
 * @param byte      Byte to write
 * @return          RING_BUFFER_OK on success, error code otherwise
 */
ring_buffer_error_t ring_buffer_write_byte(ring_buffer_t *rb, uint8_t byte);

/**
 * Read data from the buffer
 * 
 * @param rb        Pointer to ring buffer structure
 * @param data      Pointer to destination buffer
 * @param len       Maximum number of bytes to read
 * @return          Number of bytes read, or negative error code
 */
int ring_buffer_read(ring_buffer_t *rb, uint8_t *data, size_t len);

/**
 * Read a single byte from the buffer
 * 
 * @param rb        Pointer to ring buffer structure
 * @param byte      Pointer to store the read byte
 * @return          RING_BUFFER_OK on success, error code otherwise
 */
ring_buffer_error_t ring_buffer_read_byte(ring_buffer_t *rb, uint8_t *byte);

/**
 * Peek at data without removing it
 * 
 * @param rb        Pointer to ring buffer structure
 * @param data      Pointer to destination buffer
 * @param len       Maximum number of bytes to peek
 * @return          Number of bytes peeked, or negative error code
 */
int ring_buffer_peek(ring_buffer_t *rb, uint8_t *data, size_t len);

/**
 * Peek at a single byte without removing it
 * 
 * @param rb        Pointer to ring buffer structure
 * @param byte      Pointer to store the peeked byte
 * @return          RING_BUFFER_OK on success, error code otherwise
 */
ring_buffer_error_t ring_buffer_peek_byte(ring_buffer_t *rb, uint8_t *byte);

/**
 * Skip (discard) bytes from the buffer
 * 
 * @param rb        Pointer to ring buffer structure
 * @param len       Number of bytes to skip
 * @return          Number of bytes skipped, or negative error code
 */
int ring_buffer_skip(ring_buffer_t *rb, size_t len);

/**
 * Get the number of bytes available to read
 * 
 * @param rb        Pointer to ring buffer structure
 * @return          Number of bytes available, or 0 on error
 */
size_t ring_buffer_available(const ring_buffer_t *rb);

/**
 * Get the amount of free space available for writing
 * 
 * @param rb        Pointer to ring buffer structure
 * @return          Number of bytes that can be written, or 0 on error
 */
size_t ring_buffer_free_space(const ring_buffer_t *rb);

/**
 * Check if the buffer is empty
 * 
 * @param rb        Pointer to ring buffer structure
 * @return          true if empty, false otherwise
 */
bool ring_buffer_is_empty(const ring_buffer_t *rb);

/**
 * Check if the buffer is full
 * 
 * @param rb        Pointer to ring buffer structure
 * @return          true if full, false otherwise
 */
bool ring_buffer_is_full(const ring_buffer_t *rb);

/**
 * Get the total capacity of the buffer
 * 
 * @param rb        Pointer to ring buffer structure
 * @return          Total capacity in bytes, or 0 on error
 */
size_t ring_buffer_capacity(const ring_buffer_t *rb);

/**
 * Get error description string
 * 
 * @param error     Error code
 * @return          Human-readable error description
 */
const char *ring_buffer_error_string(ring_buffer_error_t error);

/**
 * Write typed data to the buffer
 * 
 * @param rb        Pointer to ring buffer structure
 * @param data      Pointer to data to write
 * @param size      Size of each element
 * @param count     Number of elements to write
 * @return          Number of elements written, or negative error code
 */
int ring_buffer_write_items(ring_buffer_t *rb, const void *data, size_t size, size_t count);

/**
 * Read typed data from the buffer
 * 
 * @param rb        Pointer to ring buffer structure
 * @param data      Pointer to destination buffer
 * @param size      Size of each element
 * @param count     Maximum number of elements to read
 * @return          Number of elements read, or negative error code
 */
int ring_buffer_read_items(ring_buffer_t *rb, void *data, size_t size, size_t count);

/**
 * Find a byte in the buffer
 * 
 * @param rb        Pointer to ring buffer structure
 * @param byte      Byte to search for
 * @return          Distance from tail to the byte (0 if first), or -1 if not found
 */
int ring_buffer_find_byte(const ring_buffer_t *rb, uint8_t byte);

/**
 * Get a pointer to contiguous read data and its length
 * Useful for zero-copy operations
 * 
 * @param rb        Pointer to ring buffer structure
 * @param data      Pointer to store the contiguous data pointer
 * @return          Length of contiguous data available
 */
size_t ring_buffer_get_read_ptr(const ring_buffer_t *rb, const uint8_t **data);

/**
 * Get a pointer to contiguous write space and its length
 * Useful for zero-copy operations
 * 
 * @param rb        Pointer to ring buffer structure
 * @param data      Pointer to store the contiguous write pointer
 * @return          Length of contiguous space available
 */
size_t ring_buffer_get_write_ptr(const ring_buffer_t *rb, uint8_t **data);

/**
 * Commit a write after using get_write_ptr
 * 
 * @param rb        Pointer to ring buffer structure
 * @param len       Number of bytes written
 * @return          RING_BUFFER_OK on success, error code otherwise
 */
ring_buffer_error_t ring_buffer_commit_write(ring_buffer_t *rb, size_t len);

/**
 * Commit a read after using get_read_ptr
 * 
 * @param rb        Pointer to ring buffer structure
 * @param len       Number of bytes read
 * @return          RING_BUFFER_OK on success, error code otherwise
 */
ring_buffer_error_t ring_buffer_commit_read(ring_buffer_t *rb, size_t len);

#ifdef __cplusplus
}
#endif

#endif /* RING_BUFFER_H */