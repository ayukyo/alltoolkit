# Ring Buffer Utility (C)

A thread-safe circular buffer implementation for C, useful for embedded systems, audio processing, and data streaming applications.

## Features

- **Fixed-size buffer** with O(1) read/write operations
- **Thread-safe** operations (can be used with external mutex)
- **Full/empty state detection**
- **Peek and skip** operations
- **Zero-copy access** for performance-critical applications
- **Typed data support** for structures and arrays
- **Byte search** functionality
- **Dynamic or static allocation** options

## Files

| File | Description |
|------|-------------|
| `ring_buffer.h` | Header file with API declarations |
| `ring_buffer.c` | Implementation |
| `test_ring_buffer.c` | Unit test suite |
| `example.c` | Usage examples |

## Building

### Compile tests
```bash
gcc -Wall -Wextra -o test_ring_buffer test_ring_buffer.c ring_buffer.c
./test_ring_buffer
```

### Compile examples
```bash
gcc -Wall -Wextra -o ring_buffer_example example.c ring_buffer.c
./ring_buffer_example
```

## API Reference

### Initialization

```c
// Static allocation (use existing buffer)
ring_buffer_error_t ring_buffer_init(ring_buffer_t *rb, uint8_t *buffer, size_t capacity);

// Dynamic allocation (malloc internally)
ring_buffer_error_t ring_buffer_create(ring_buffer_t *rb, size_t capacity);

// Free dynamically allocated buffer
void ring_buffer_destroy(ring_buffer_t *rb);

// Reset to empty state
ring_buffer_error_t ring_buffer_reset(ring_buffer_t *rb);
```

### Read/Write Operations

```c
// Write bytes
int ring_buffer_write(ring_buffer_t *rb, const uint8_t *data, size_t len);
ring_buffer_error_t ring_buffer_write_byte(ring_buffer_t *rb, uint8_t byte);

// Read bytes
int ring_buffer_read(ring_buffer_t *rb, uint8_t *data, size_t len);
ring_buffer_error_t ring_buffer_read_byte(ring_buffer_t *rb, uint8_t *byte);

// Peek without removing
int ring_buffer_peek(ring_buffer_t *rb, uint8_t *data, size_t len);
ring_buffer_error_t ring_buffer_peek_byte(ring_buffer_t *rb, uint8_t *byte);

// Skip (discard) bytes
int ring_buffer_skip(ring_buffer_t *rb, size_t len);
```

### Status Queries

```c
size_t ring_buffer_available(const ring_buffer_t *rb);
size_t ring_buffer_free_space(const ring_buffer_t *rb);
size_t ring_buffer_capacity(const ring_buffer_t *rb);
bool ring_buffer_is_empty(const ring_buffer_t *rb);
bool ring_buffer_is_full(const ring_buffer_t *rb);
```

### Zero-Copy Operations

```c
// Get pointers for direct access
size_t ring_buffer_get_read_ptr(const ring_buffer_t *rb, const uint8_t **data);
size_t ring_buffer_get_write_ptr(const ring_buffer_t *rb, uint8_t **data);

// Commit after direct access
ring_buffer_error_t ring_buffer_commit_write(ring_buffer_t *rb, size_t len);
ring_buffer_error_t ring_buffer_commit_read(ring_buffer_t *rb, size_t len);
```

### Utility Functions

```c
// Find byte position in buffer
int ring_buffer_find_byte(const ring_buffer_t *rb, uint8_t byte);

// Typed data operations
int ring_buffer_write_items(ring_buffer_t *rb, const void *data, size_t size, size_t count);
int ring_buffer_read_items(ring_buffer_t *rb, void *data, size_t size, size_t count);

// Error descriptions
const char *ring_buffer_error_string(ring_buffer_error_t error);
```

## Quick Example

```c
#include "ring_buffer.h"

int main(void) {
    // Create a 256-byte buffer
    ring_buffer_t rb;
    uint8_t buffer[256];
    ring_buffer_init(&rb, buffer, sizeof(buffer));
    
    // Write data
    const char *msg = "Hello, World!";
    ring_buffer_write(&rb, (const uint8_t *)msg, strlen(msg));
    
    // Read data
    uint8_t read_buf[256];
    int len = ring_buffer_read(&rb, read_buf, sizeof(read_buf));
    read_buf[len] = '\0';
    printf("Read: %s\n", read_buf);
    
    return 0;
}
```

## Error Codes

| Code | Description |
|------|-------------|
| `RING_BUFFER_OK` | Success |
| `RING_BUFFER_ERROR_NULL` | Null pointer argument |
| `RING_BUFFER_ERROR_FULL` | Buffer is full |
| `RING_BUFFER_ERROR_EMPTY` | Buffer is empty |
| `RING_BUFFER_ERROR_NO_MEMORY` | Memory allocation failed |
| `RING_BUFFER_ERROR_INVALID_SIZE` | Invalid size argument |
| `RING_BUFFER_ERROR_INVALID_ARGUMENT` | Invalid argument |

## Use Cases

1. **Embedded Systems**: UART/SPI data buffering
2. **Audio Processing**: Real-time audio sample buffering
3. **Network Protocols**: Packet buffering and reassembly
4. **Producer-Consumer**: Thread-safe data passing (with external mutex)
5. **DMA Transfers**: Zero-copy buffer management

## License

MIT License