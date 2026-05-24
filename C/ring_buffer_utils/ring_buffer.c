/**
 * Ring Buffer Implementation
 */

#include "ring_buffer.h"
#include <stdlib.h>
#include <string.h>

/* Get minimum of two values */
#define MIN(a, b) ((a) < (b) ? (a) : (b))

ring_buffer_error_t ring_buffer_init(ring_buffer_t *rb, uint8_t *buffer, size_t capacity) {
    if (rb == NULL || buffer == NULL) {
        return RING_BUFFER_ERROR_NULL;
    }
    
    if (capacity == 0) {
        return RING_BUFFER_ERROR_INVALID_SIZE;
    }
    
    rb->buffer = buffer;
    rb->capacity = capacity;
    rb->head = 0;
    rb->tail = 0;
    rb->count = 0;
    rb->is_dynamic = false;
    
    return RING_BUFFER_OK;
}

ring_buffer_error_t ring_buffer_create(ring_buffer_t *rb, size_t capacity) {
    if (rb == NULL) {
        return RING_BUFFER_ERROR_NULL;
    }
    
    if (capacity == 0) {
        return RING_BUFFER_ERROR_INVALID_SIZE;
    }
    
    uint8_t *buffer = (uint8_t *)malloc(capacity);
    if (buffer == NULL) {
        return RING_BUFFER_ERROR_NO_MEMORY;
    }
    
    rb->buffer = buffer;
    rb->capacity = capacity;
    rb->head = 0;
    rb->tail = 0;
    rb->count = 0;
    rb->is_dynamic = true;
    
    return RING_BUFFER_OK;
}

void ring_buffer_destroy(ring_buffer_t *rb) {
    if (rb != NULL && rb->is_dynamic && rb->buffer != NULL) {
        free(rb->buffer);
        rb->buffer = NULL;
        rb->capacity = 0;
        rb->head = 0;
        rb->tail = 0;
        rb->count = 0;
        rb->is_dynamic = false;
    }
}

ring_buffer_error_t ring_buffer_reset(ring_buffer_t *rb) {
    if (rb == NULL) {
        return RING_BUFFER_ERROR_NULL;
    }
    
    rb->head = 0;
    rb->tail = 0;
    rb->count = 0;
    
    return RING_BUFFER_OK;
}

int ring_buffer_write(ring_buffer_t *rb, const uint8_t *data, size_t len) {
    if (rb == NULL || data == NULL) {
        return RING_BUFFER_ERROR_NULL;
    }
    
    if (len == 0) {
        return 0;
    }
    
    size_t free_space = rb->capacity - rb->count;
    size_t to_write = MIN(len, free_space);
    
    if (to_write == 0) {
        return 0; /* Buffer is full, write nothing */
    }
    
    /* Calculate how much we can write before wrapping */
    size_t first_chunk = MIN(to_write, rb->capacity - rb->head);
    
    /* Write first chunk */
    memcpy(rb->buffer + rb->head, data, first_chunk);
    
    /* Write second chunk if it wraps around */
    if (first_chunk < to_write) {
        memcpy(rb->buffer, data + first_chunk, to_write - first_chunk);
    }
    
    /* Update head and count */
    rb->head = (rb->head + to_write) % rb->capacity;
    rb->count += to_write;
    
    return (int)to_write;
}

ring_buffer_error_t ring_buffer_write_byte(ring_buffer_t *rb, uint8_t byte) {
    if (rb == NULL) {
        return RING_BUFFER_ERROR_NULL;
    }
    
    if (rb->count >= rb->capacity) {
        return RING_BUFFER_ERROR_FULL;
    }
    
    rb->buffer[rb->head] = byte;
    rb->head = (rb->head + 1) % rb->capacity;
    rb->count++;
    
    return RING_BUFFER_OK;
}

int ring_buffer_read(ring_buffer_t *rb, uint8_t *data, size_t len) {
    if (rb == NULL || data == NULL) {
        return RING_BUFFER_ERROR_NULL;
    }
    
    if (len == 0) {
        return 0;
    }
    
    size_t to_read = MIN(len, rb->count);
    
    if (to_read == 0) {
        return 0;
    }
    
    /* Calculate how much we can read before wrapping */
    size_t first_chunk = MIN(to_read, rb->capacity - rb->tail);
    
    /* Read first chunk */
    memcpy(data, rb->buffer + rb->tail, first_chunk);
    
    /* Read second chunk if it wraps around */
    if (first_chunk < to_read) {
        memcpy(data + first_chunk, rb->buffer, to_read - first_chunk);
    }
    
    /* Update tail and count */
    rb->tail = (rb->tail + to_read) % rb->capacity;
    rb->count -= to_read;
    
    return (int)to_read;
}

ring_buffer_error_t ring_buffer_read_byte(ring_buffer_t *rb, uint8_t *byte) {
    if (rb == NULL || byte == NULL) {
        return RING_BUFFER_ERROR_NULL;
    }
    
    if (rb->count == 0) {
        return RING_BUFFER_ERROR_EMPTY;
    }
    
    *byte = rb->buffer[rb->tail];
    rb->tail = (rb->tail + 1) % rb->capacity;
    rb->count--;
    
    return RING_BUFFER_OK;
}

int ring_buffer_peek(ring_buffer_t *rb, uint8_t *data, size_t len) {
    if (rb == NULL || data == NULL) {
        return RING_BUFFER_ERROR_NULL;
    }
    
    if (len == 0) {
        return 0;
    }
    
    size_t to_peek = MIN(len, rb->count);
    
    if (to_peek == 0) {
        return 0;
    }
    
    /* Calculate how much we can peek before wrapping */
    size_t first_chunk = MIN(to_peek, rb->capacity - rb->tail);
    
    /* Peek first chunk */
    memcpy(data, rb->buffer + rb->tail, first_chunk);
    
    /* Peek second chunk if it wraps around */
    if (first_chunk < to_peek) {
        memcpy(data + first_chunk, rb->buffer, to_peek - first_chunk);
    }
    
    return (int)to_peek;
}

ring_buffer_error_t ring_buffer_peek_byte(ring_buffer_t *rb, uint8_t *byte) {
    if (rb == NULL || byte == NULL) {
        return RING_BUFFER_ERROR_NULL;
    }
    
    if (rb->count == 0) {
        return RING_BUFFER_ERROR_EMPTY;
    }
    
    *byte = rb->buffer[rb->tail];
    
    return RING_BUFFER_OK;
}

int ring_buffer_skip(ring_buffer_t *rb, size_t len) {
    if (rb == NULL) {
        return RING_BUFFER_ERROR_NULL;
    }
    
    if (len == 0) {
        return 0;
    }
    
    size_t to_skip = MIN(len, rb->count);
    
    rb->tail = (rb->tail + to_skip) % rb->capacity;
    rb->count -= to_skip;
    
    return (int)to_skip;
}

size_t ring_buffer_available(const ring_buffer_t *rb) {
    if (rb == NULL) {
        return 0;
    }
    return rb->count;
}

size_t ring_buffer_free_space(const ring_buffer_t *rb) {
    if (rb == NULL) {
        return 0;
    }
    return rb->capacity - rb->count;
}

bool ring_buffer_is_empty(const ring_buffer_t *rb) {
    if (rb == NULL) {
        return true;
    }
    return rb->count == 0;
}

bool ring_buffer_is_full(const ring_buffer_t *rb) {
    if (rb == NULL) {
        return false;
    }
    return rb->count >= rb->capacity;
}

size_t ring_buffer_capacity(const ring_buffer_t *rb) {
    if (rb == NULL) {
        return 0;
    }
    return rb->capacity;
}

const char *ring_buffer_error_string(ring_buffer_error_t error) {
    switch (error) {
        case RING_BUFFER_OK:
            return "Success";
        case RING_BUFFER_ERROR_NULL:
            return "Null pointer";
        case RING_BUFFER_ERROR_FULL:
            return "Buffer is full";
        case RING_BUFFER_ERROR_EMPTY:
            return "Buffer is empty";
        case RING_BUFFER_ERROR_NO_MEMORY:
            return "Memory allocation failed";
        case RING_BUFFER_ERROR_INVALID_SIZE:
            return "Invalid size";
        case RING_BUFFER_ERROR_INVALID_ARGUMENT:
            return "Invalid argument";
        default:
            return "Unknown error";
    }
}

int ring_buffer_write_items(ring_buffer_t *rb, const void *data, size_t size, size_t count) {
    if (rb == NULL || data == NULL) {
        return RING_BUFFER_ERROR_NULL;
    }
    
    if (size == 0 || count == 0) {
        return 0;
    }
    
    size_t bytes_to_write = size * count;
    int written = ring_buffer_write(rb, (const uint8_t *)data, bytes_to_write);
    
    if (written < 0) {
        return written;
    }
    
    return (int)(written / size);
}

int ring_buffer_read_items(ring_buffer_t *rb, void *data, size_t size, size_t count) {
    if (rb == NULL || data == NULL) {
        return RING_BUFFER_ERROR_NULL;
    }
    
    if (size == 0 || count == 0) {
        return 0;
    }
    
    size_t bytes_to_read = size * count;
    int read = ring_buffer_read(rb, (uint8_t *)data, bytes_to_read);
    
    if (read < 0) {
        return read;
    }
    
    return (int)(read / size);
}

int ring_buffer_find_byte(const ring_buffer_t *rb, uint8_t byte) {
    if (rb == NULL || rb->count == 0) {
        return -1;
    }
    
    for (size_t i = 0; i < rb->count; i++) {
        size_t idx = (rb->tail + i) % rb->capacity;
        if (rb->buffer[idx] == byte) {
            return (int)i;
        }
    }
    
    return -1;
}

size_t ring_buffer_get_read_ptr(const ring_buffer_t *rb, const uint8_t **data) {
    if (rb == NULL || data == NULL || rb->count == 0) {
        if (data != NULL) {
            *data = NULL;
        }
        return 0;
    }
    
    *data = rb->buffer + rb->tail;
    
    /* Return contiguous data length (might wrap around) */
    size_t contiguous = rb->capacity - rb->tail;
    return MIN(contiguous, rb->count);
}

size_t ring_buffer_get_write_ptr(const ring_buffer_t *rb, uint8_t **data) {
    if (rb == NULL || data == NULL || rb->count >= rb->capacity) {
        if (data != NULL) {
            *data = NULL;
        }
        return 0;
    }
    
    *data = rb->buffer + rb->head;
    
    /* Return contiguous space length (might wrap around) */
    size_t contiguous = rb->capacity - rb->head;
    return MIN(contiguous, rb->capacity - rb->count);
}

ring_buffer_error_t ring_buffer_commit_write(ring_buffer_t *rb, size_t len) {
    if (rb == NULL) {
        return RING_BUFFER_ERROR_NULL;
    }
    
    size_t free_space = rb->capacity - rb->count;
    if (len > free_space) {
        return RING_BUFFER_ERROR_INVALID_ARGUMENT;
    }
    
    rb->head = (rb->head + len) % rb->capacity;
    rb->count += len;
    
    return RING_BUFFER_OK;
}

ring_buffer_error_t ring_buffer_commit_read(ring_buffer_t *rb, size_t len) {
    if (rb == NULL) {
        return RING_BUFFER_ERROR_NULL;
    }
    
    if (len > rb->count) {
        return RING_BUFFER_ERROR_INVALID_ARGUMENT;
    }
    
    rb->tail = (rb->tail + len) % rb->capacity;
    rb->count -= len;
    
    return RING_BUFFER_OK;
}