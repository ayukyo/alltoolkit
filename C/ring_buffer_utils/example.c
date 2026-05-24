/**
 * Ring Buffer Usage Examples
 * 
 * This file demonstrates various use cases for the ring buffer utility.
 */

#include <stdio.h>
#include <string.h>
#include "ring_buffer.h"

/* Example 1: Basic usage with static buffer */
void example_basic_static(void) {
    printf("=== Example 1: Basic Static Buffer ===\n");
    
    uint8_t buffer[32];
    ring_buffer_t rb;
    
    /* Initialize with static buffer */
    ring_buffer_init(&rb, buffer, sizeof(buffer));
    printf("Buffer capacity: %zu bytes\n", ring_buffer_capacity(&rb));
    
    /* Write some data */
    const char *message = "Hello, Ring Buffer!";
    size_t msg_len = strlen(message);
    int written = ring_buffer_write(&rb, (const uint8_t *)message, msg_len);
    printf("Wrote %d bytes\n", written);
    
    /* Read it back */
    uint8_t read_buf[32] = {0};
    int read = ring_buffer_read(&rb, read_buf, sizeof(read_buf) - 1);
    printf("Read %d bytes: %s\n\n", read, read_buf);
}

/* Example 2: Dynamic buffer allocation */
void example_dynamic_allocation(void) {
    printf("=== Example 2: Dynamic Buffer Allocation ===\n");
    
    ring_buffer_t rb;
    
    /* Create buffer dynamically */
    ring_buffer_error_t err = ring_buffer_create(&rb, 256);
    if (err != RING_BUFFER_OK) {
        printf("Failed to create buffer: %s\n", ring_buffer_error_string(err));
        return;
    }
    
    printf("Created buffer with capacity: %zu bytes\n", ring_buffer_capacity(&rb));
    
    /* Use the buffer... */
    uint8_t data[] = {0xDE, 0xAD, 0xBE, 0xEF};
    ring_buffer_write(&rb, data, sizeof(data));
    
    /* Clean up when done */
    ring_buffer_destroy(&rb);
    printf("Buffer destroyed\n\n");
}

/* Example 3: Byte-by-byte operations */
void example_byte_operations(void) {
    printf("=== Example 3: Byte-by-Byte Operations ===\n");
    
    uint8_t buffer[16];
    ring_buffer_t rb;
    ring_buffer_init(&rb, buffer, sizeof(buffer));
    
    /* Write bytes one at a time */
    for (uint8_t i = 0; i < 10; i++) {
        ring_buffer_write_byte(&rb, i * 10);
    }
    printf("Wrote 10 bytes, buffer now has %zu bytes\n", ring_buffer_available(&rb));
    
    /* Read bytes one at a time */
    printf("Reading bytes: ");
    while (!ring_buffer_is_empty(&rb)) {
        uint8_t byte;
        ring_buffer_read_byte(&rb, &byte);
        printf("%d ", byte);
    }
    printf("\n\n");
}

/* Example 4: Peek and skip operations */
void example_peek_skip(void) {
    printf("=== Example 4: Peek and Skip Operations ===\n");
    
    uint8_t buffer[32];
    ring_buffer_t rb;
    ring_buffer_init(&rb, buffer, sizeof(buffer));
    
    /* Write some data */
    const char *data = "ABCDEFGH";
    ring_buffer_write(&rb, (const uint8_t *)data, strlen(data));
    
    /* Peek at the first 3 bytes */
    uint8_t peek_buf[4] = {0};
    int peeked = ring_buffer_peek(&rb, peek_buf, 3);
    printf("Peeked %d bytes: %s (buffer still has %zu bytes)\n", 
           peeked, peek_buf, ring_buffer_available(&rb));
    
    /* Skip first 2 bytes */
    int skipped = ring_buffer_skip(&rb, 2);
    printf("Skipped %d bytes, buffer now has %zu bytes\n", 
           skipped, ring_buffer_available(&rb));
    
    /* Read the rest */
    uint8_t read_buf[10] = {0};
    int read = ring_buffer_read(&rb, read_buf, sizeof(read_buf) - 1);
    printf("Read remaining %d bytes: %s\n\n", read, read_buf);
}

/* Example 5: Finding bytes in buffer */
void example_find_byte(void) {
    printf("=== Example 5: Finding Bytes ===\n");
    
    uint8_t buffer[32];
    ring_buffer_t rb;
    ring_buffer_init(&rb, buffer, sizeof(buffer));
    
    /* Write data with a delimiter */
    const char *packet = "CMD:DATA|END";
    ring_buffer_write(&rb, (const uint8_t *)packet, strlen(packet));
    
    /* Find the delimiter */
    int pos = ring_buffer_find_byte(&rb, '|');
    if (pos >= 0) {
        printf("Found '|' at position %d\n", pos);
        
        /* Read everything before the delimiter */
        uint8_t cmd[16] = {0};
        ring_buffer_read(&rb, cmd, pos);
        printf("Command: %s\n", cmd);
        
        /* Skip the delimiter */
        ring_buffer_skip(&rb, 1);
        
        /* Read the rest */
        uint8_t rest[16] = {0};
        ring_buffer_read(&rb, rest, 7);
        printf("Rest: %s\n", rest);
    }
    printf("\n");
}

/* Example 6: Zero-copy operations */
void example_zero_copy(void) {
    printf("=== Example 6: Zero-Copy Operations ===\n");
    
    uint8_t buffer[64];
    ring_buffer_t rb;
    ring_buffer_init(&rb, buffer, sizeof(buffer));
    
    /* Get write pointer and write directly */
    uint8_t *write_ptr;
    size_t write_space = ring_buffer_get_write_ptr(&rb, &write_ptr);
    printf("Available contiguous write space: %zu bytes\n", write_space);
    
    /* Write directly to buffer (simulating hardware DMA or file read) */
    const char *data = "Zero-copy data transfer!";
    size_t data_len = strlen(data);
    if (data_len <= write_space) {
        memcpy(write_ptr, data, data_len);
        ring_buffer_commit_write(&rb, data_len);
        printf("Wrote %zu bytes using zero-copy\n", data_len);
    }
    
    /* Get read pointer and read directly */
    const uint8_t *read_ptr;
    size_t read_avail = ring_buffer_get_read_ptr(&rb, &read_ptr);
    printf("Available contiguous read data: %zu bytes\n", read_avail);
    
    /* Process data without copying */
    printf("Data: %.*s\n", (int)read_avail, read_ptr);
    
    /* Commit read after processing */
    ring_buffer_commit_read(&rb, read_avail);
    printf("Buffer now empty: %s\n\n", ring_buffer_is_empty(&rb) ? "yes" : "no");
}

/* Example 7: Typed data structures */
void example_typed_data(void) {
    printf("=== Example 7: Typed Data Structures ===\n");
    
    typedef struct {
        uint16_t id;
        int16_t x;
        int16_t y;
        uint16_t temperature;
    } sensor_reading_t;
    
    uint8_t buffer[sizeof(sensor_reading_t) * 10];
    ring_buffer_t rb;
    ring_buffer_init(&rb, buffer, sizeof(buffer));
    
    /* Write sensor readings */
    sensor_reading_t readings[] = {
        {1, 100, 200, 2500},
        {2, 150, 180, 2600},
        {3, 200, 220, 2550}
    };
    
    int written = ring_buffer_write_items(&rb, readings, 
                                           sizeof(sensor_reading_t), 
                                           sizeof(readings)/sizeof(readings[0]));
    printf("Wrote %d sensor readings\n", written);
    
    /* Read them back */
    sensor_reading_t read_readings[3];
    int read = ring_buffer_read_items(&rb, read_readings, 
                                      sizeof(sensor_reading_t), 3);
    printf("Read %d sensor readings:\n", read);
    
    for (int i = 0; i < read; i++) {
        printf("  ID=%u, pos=(%d,%d), temp=%u\n",
               read_readings[i].id,
               read_readings[i].x,
               read_readings[i].y,
               read_readings[i].temperature);
    }
    printf("\n");
}

/* Example 8: Circular buffer for streaming */
void example_streaming(void) {
    printf("=== Example 8: Streaming Use Case ===\n");
    
    /* Simulate audio streaming with a small buffer */
    uint8_t buffer[256];
    ring_buffer_t rb;
    ring_buffer_init(&rb, buffer, sizeof(buffer));
    
    printf("Simulating audio stream (256 byte buffer)\n\n");
    
    /* Producer: Write data in chunks */
    const char *chunks[] = {
        "Audio chunk 1: silence",
        "Audio chunk 2: music",
        "Audio chunk 3: voice"
    };
    
    for (int i = 0; i < 3; i++) {
        size_t chunk_len = strlen(chunks[i]);
        
        /* Wait for space */
        if (ring_buffer_free_space(&rb) < chunk_len) {
            printf("Buffer full! Freeing space...\n");
            ring_buffer_skip(&rb, 50); /* Discard old data */
        }
        
        ring_buffer_write(&rb, (const uint8_t *)chunks[i], chunk_len);
        printf("Producer: Wrote '%s' (%zu bytes)\n", chunks[i], chunk_len);
        printf("  Buffer: %zu/%zu bytes used\n", 
               ring_buffer_available(&rb), ring_buffer_capacity(&rb));
    }
    
    /* Consumer: Read data */
    printf("\nConsumer: Processing buffered data...\n");
    uint8_t read_buf[257];
    while (!ring_buffer_is_empty(&rb)) {
        int read = ring_buffer_read(&rb, read_buf, 32);
        read_buf[read] = '\0';
        printf("  Processed: '%s'\n", read_buf);
    }
    printf("\n");
}

/* Example 9: Error handling */
void example_error_handling(void) {
    printf("=== Example 9: Error Handling ===\n");
    
    ring_buffer_t rb;
    uint8_t buffer[8];
    ring_buffer_init(&rb, buffer, sizeof(buffer));
    
    /* Fill the buffer */
    uint8_t data[] = {1, 2, 3, 4, 5, 6, 7, 8};
    ring_buffer_write(&rb, data, sizeof(data));
    
    /* Try to write to full buffer */
    ring_buffer_error_t err = ring_buffer_write_byte(&rb, 99);
    if (err == RING_BUFFER_ERROR_FULL) {
        printf("Correctly detected full buffer: %s\n", 
               ring_buffer_error_string(err));
    }
    
    /* Try to read from empty buffer after clearing */
    ring_buffer_reset(&rb);
    uint8_t byte;
    err = ring_buffer_read_byte(&rb, &byte);
    if (err == RING_BUFFER_ERROR_EMPTY) {
        printf("Correctly detected empty buffer: %s\n", 
               ring_buffer_error_string(err));
    }
    
    /* NULL pointer handling */
    err = ring_buffer_init(NULL, buffer, sizeof(buffer));
    printf("NULL buffer check: %s\n\n", ring_buffer_error_string(err));
}

int main(void) {
    printf("\n========================================\n");
    printf("   Ring Buffer Usage Examples\n");
    printf("========================================\n\n");
    
    example_basic_static();
    example_dynamic_allocation();
    example_byte_operations();
    example_peek_skip();
    example_find_byte();
    example_zero_copy();
    example_typed_data();
    example_streaming();
    example_error_handling();
    
    printf("All examples completed!\n");
    return 0;
}