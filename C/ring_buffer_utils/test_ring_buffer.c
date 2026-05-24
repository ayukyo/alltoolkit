/**
 * Ring Buffer Test Suite
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "ring_buffer.h"

#define TEST_BUFFER_SIZE 64

static int tests_passed = 0;
static int tests_failed = 0;

#define TEST(name) static void test_##name(void)
#define RUN_TEST(name) do { \
    printf("  Testing: %s... ", #name); \
    test_##name(); \
    printf("PASSED\n"); \
    tests_passed++; \
} while(0)

#define ASSERT(cond) do { \
    if (!(cond)) { \
        printf("FAILED at line %d: %s\n", __LINE__, #cond); \
        tests_failed++; \
        return; \
    } \
} while(0)

#define ASSERT_EQ(a, b) ASSERT((a) == (b))
#define ASSERT_NE(a, b) ASSERT((a) != (b))
#define ASSERT_OK(err) ASSERT_EQ(err, RING_BUFFER_OK)

/* Test: Basic initialization with static buffer */
TEST(init_static_buffer) {
    ring_buffer_t rb;
    uint8_t buffer[TEST_BUFFER_SIZE];
    
    ring_buffer_error_t err = ring_buffer_init(&rb, buffer, TEST_BUFFER_SIZE);
    ASSERT_OK(err);
    ASSERT_EQ(ring_buffer_capacity(&rb), TEST_BUFFER_SIZE);
    ASSERT_EQ(ring_buffer_available(&rb), 0);
    ASSERT(ring_buffer_is_empty(&rb));
    ASSERT(!ring_buffer_is_full(&rb));
    ASSERT(!rb.is_dynamic);
}

/* Test: Dynamic allocation */
TEST(create_dynamic_buffer) {
    ring_buffer_t rb;
    
    ring_buffer_error_t err = ring_buffer_create(&rb, TEST_BUFFER_SIZE);
    ASSERT_OK(err);
    ASSERT_EQ(ring_buffer_capacity(&rb), TEST_BUFFER_SIZE);
    ASSERT_EQ(ring_buffer_available(&rb), 0);
    ASSERT(rb.is_dynamic);
    
    ring_buffer_destroy(&rb);
    ASSERT_EQ(rb.capacity, 0);
    ASSERT_EQ(rb.buffer, NULL);
}

/* Test: Write and read single bytes */
TEST(write_read_single_byte) {
    ring_buffer_t rb;
    uint8_t buffer[TEST_BUFFER_SIZE];
    ring_buffer_init(&rb, buffer, TEST_BUFFER_SIZE);
    
    uint8_t byte = 0xAB;
    ring_buffer_error_t err = ring_buffer_write_byte(&rb, byte);
    ASSERT_OK(err);
    ASSERT_EQ(ring_buffer_available(&rb), 1);
    
    uint8_t read_byte;
    err = ring_buffer_read_byte(&rb, &read_byte);
    ASSERT_OK(err);
    ASSERT_EQ(read_byte, byte);
    ASSERT(ring_buffer_is_empty(&rb));
}

/* Test: Write and read multiple bytes */
TEST(write_read_multiple_bytes) {
    ring_buffer_t rb;
    uint8_t buffer[TEST_BUFFER_SIZE];
    ring_buffer_init(&rb, buffer, TEST_BUFFER_SIZE);
    
    uint8_t data[] = {1, 2, 3, 4, 5};
    int written = ring_buffer_write(&rb, data, sizeof(data));
    ASSERT_EQ(written, sizeof(data));
    ASSERT_EQ(ring_buffer_available(&rb), sizeof(data));
    
    uint8_t read_data[sizeof(data)];
    int read = ring_buffer_read(&rb, read_data, sizeof(read_data));
    ASSERT_EQ(read, sizeof(data));
    ASSERT(memcmp(data, read_data, sizeof(data)) == 0);
}

/* Test: Buffer wrap-around */
TEST(buffer_wrap_around) {
    ring_buffer_t rb;
    uint8_t buffer[8];
    ring_buffer_init(&rb, buffer, 8);
    
    /* Fill the buffer */
    uint8_t data1[] = {1, 2, 3, 4, 5, 6, 7, 8};
    int written = ring_buffer_write(&rb, data1, 8);
    ASSERT_EQ(written, 8);
    ASSERT(ring_buffer_is_full(&rb));
    
    /* Read half */
    uint8_t read1[4];
    int read = ring_buffer_read(&rb, read1, 4);
    ASSERT_EQ(read, 4);
    
    /* Write more (should wrap around) */
    uint8_t data2[] = {10, 11, 12, 13};
    written = ring_buffer_write(&rb, data2, 4);
    ASSERT_EQ(written, 4);
    ASSERT(ring_buffer_is_full(&rb));
    
    /* Read all */
    uint8_t read2[8];
    read = ring_buffer_read(&rb, read2, 8);
    ASSERT_EQ(read, 8);
    
    uint8_t expected[] = {5, 6, 7, 8, 10, 11, 12, 13};
    ASSERT(memcmp(read2, expected, 8) == 0);
}

/* Test: Full buffer rejection */
TEST(full_buffer_rejection) {
    ring_buffer_t rb;
    uint8_t buffer[4];
    ring_buffer_init(&rb, buffer, 4);
    
    uint8_t data[] = {1, 2, 3, 4};
    int written = ring_buffer_write(&rb, data, 4);
    ASSERT_EQ(written, 4);
    ASSERT(ring_buffer_is_full(&rb));
    
    /* Try to write more */
    uint8_t extra[] = {5, 6};
    written = ring_buffer_write(&rb, extra, 2);
    ASSERT_EQ(written, 0); /* Should write nothing */
    ASSERT_EQ(ring_buffer_available(&rb), 4);
}

/* Test: Partial write when nearly full */
TEST(partial_write) {
    ring_buffer_t rb;
    uint8_t buffer[4];
    ring_buffer_init(&rb, buffer, 4);
    
    uint8_t data[] = {1, 2};
    int written = ring_buffer_write(&rb, data, 2);
    ASSERT_EQ(written, 2);
    
    /* Try to write more than available space */
    uint8_t extra[] = {3, 4, 5, 6};
    written = ring_buffer_write(&rb, extra, 4);
    ASSERT_EQ(written, 2); /* Should only write 2 bytes */
    ASSERT(ring_buffer_is_full(&rb));
}

/* Test: Empty buffer read */
TEST(empty_buffer_read) {
    ring_buffer_t rb;
    uint8_t buffer[TEST_BUFFER_SIZE];
    ring_buffer_init(&rb, buffer, TEST_BUFFER_SIZE);
    
    uint8_t byte;
    ring_buffer_error_t err = ring_buffer_read_byte(&rb, &byte);
    ASSERT_EQ(err, RING_BUFFER_ERROR_EMPTY);
    
    uint8_t data[10];
    int read = ring_buffer_read(&rb, data, 10);
    ASSERT_EQ(read, 0);
}

/* Test: Peek operations */
TEST(peek_operations) {
    ring_buffer_t rb;
    uint8_t buffer[TEST_BUFFER_SIZE];
    ring_buffer_init(&rb, buffer, TEST_BUFFER_SIZE);
    
    uint8_t data[] = {1, 2, 3, 4, 5};
    ring_buffer_write(&rb, data, sizeof(data));
    
    /* Peek single byte */
    uint8_t peeked_byte;
    ring_buffer_error_t err = ring_buffer_peek_byte(&rb, &peeked_byte);
    ASSERT_OK(err);
    ASSERT_EQ(peeked_byte, 1);
    ASSERT_EQ(ring_buffer_available(&rb), 5); /* Data still there */
    
    /* Peek multiple bytes */
    uint8_t peeked_data[3];
    int peeked = ring_buffer_peek(&rb, peeked_data, 3);
    ASSERT_EQ(peeked, 3);
    ASSERT(memcmp(peeked_data, data, 3) == 0);
    ASSERT_EQ(ring_buffer_available(&rb), 5); /* Data still there */
    
    /* Read should still work */
    uint8_t read_data[5];
    int read = ring_buffer_read(&rb, read_data, 5);
    ASSERT_EQ(read, 5);
}

/* Test: Skip operations */
TEST(skip_operations) {
    ring_buffer_t rb;
    uint8_t buffer[TEST_BUFFER_SIZE];
    ring_buffer_init(&rb, buffer, TEST_BUFFER_SIZE);
    
    uint8_t data[] = {1, 2, 3, 4, 5};
    ring_buffer_write(&rb, data, sizeof(data));
    
    /* Skip 2 bytes */
    int skipped = ring_buffer_skip(&rb, 2);
    ASSERT_EQ(skipped, 2);
    ASSERT_EQ(ring_buffer_available(&rb), 3);
    
    /* Read remaining */
    uint8_t read_data[3];
    int read = ring_buffer_read(&rb, read_data, 3);
    ASSERT_EQ(read, 3);
    uint8_t expected[] = {3, 4, 5};
    ASSERT(memcmp(read_data, expected, 3) == 0);
}

/* Test: Reset buffer */
TEST(reset_buffer) {
    ring_buffer_t rb;
    uint8_t buffer[TEST_BUFFER_SIZE];
    ring_buffer_init(&rb, buffer, TEST_BUFFER_SIZE);
    
    uint8_t data[] = {1, 2, 3, 4, 5};
    ring_buffer_write(&rb, data, sizeof(data));
    
    ring_buffer_error_t err = ring_buffer_reset(&rb);
    ASSERT_OK(err);
    ASSERT(ring_buffer_is_empty(&rb));
    ASSERT_EQ(ring_buffer_available(&rb), 0);
    ASSERT_EQ(ring_buffer_free_space(&rb), TEST_BUFFER_SIZE);
}

/* Test: Find byte */
TEST(find_byte) {
    ring_buffer_t rb;
    uint8_t buffer[TEST_BUFFER_SIZE];
    ring_buffer_init(&rb, buffer, TEST_BUFFER_SIZE);
    
    uint8_t data[] = {1, 2, 3, 4, 5};
    ring_buffer_write(&rb, data, sizeof(data));
    
    int pos = ring_buffer_find_byte(&rb, 3);
    ASSERT_EQ(pos, 2);
    
    pos = ring_buffer_find_byte(&rb, 5);
    ASSERT_EQ(pos, 4);
    
    pos = ring_buffer_find_byte(&rb, 99);
    ASSERT_EQ(pos, -1);
}

/* Test: Typed item operations */
TEST(typed_item_operations) {
    ring_buffer_t rb;
    uint8_t buffer[TEST_BUFFER_SIZE];
    ring_buffer_init(&rb, buffer, TEST_BUFFER_SIZE);
    
    typedef struct {
        int id;
        float value;
    } item_t;
    
    item_t items[] = {
        {1, 1.5f},
        {2, 2.5f},
        {3, 3.5f}
    };
    
    int written = ring_buffer_write_items(&rb, items, sizeof(item_t), 3);
    ASSERT_EQ(written, 3);
    
    item_t read_items[3];
    int read = ring_buffer_read_items(&rb, read_items, sizeof(item_t), 3);
    ASSERT_EQ(read, 3);
    
    for (int i = 0; i < 3; i++) {
        ASSERT_EQ(read_items[i].id, items[i].id);
        ASSERT_EQ(read_items[i].value, items[i].value);
    }
}

/* Test: Zero-copy operations */
TEST(zero_copy_operations) {
    ring_buffer_t rb;
    uint8_t buffer[TEST_BUFFER_SIZE];
    ring_buffer_init(&rb, buffer, TEST_BUFFER_SIZE);
    
    /* Get write pointer */
    uint8_t *write_ptr;
    size_t write_space = ring_buffer_get_write_ptr(&rb, &write_ptr);
    ASSERT(write_space > 0);
    ASSERT(write_ptr != NULL);
    
    /* Write directly */
    for (size_t i = 0; i < 10; i++) {
        write_ptr[i] = (uint8_t)(i * 10);
    }
    
    ring_buffer_error_t err = ring_buffer_commit_write(&rb, 10);
    ASSERT_OK(err);
    ASSERT_EQ(ring_buffer_available(&rb), 10);
    
    /* Get read pointer */
    const uint8_t *read_ptr;
    size_t read_avail = ring_buffer_get_read_ptr(&rb, &read_ptr);
    ASSERT_EQ(read_avail, 10);
    ASSERT(read_ptr != NULL);
    
    /* Verify data */
    for (size_t i = 0; i < 10; i++) {
        ASSERT_EQ(read_ptr[i], (uint8_t)(i * 10));
    }
    
    /* Commit read */
    err = ring_buffer_commit_read(&rb, 5);
    ASSERT_OK(err);
    ASSERT_EQ(ring_buffer_available(&rb), 5);
}

/* Test: Error handling - NULL pointers */
TEST(null_pointer_handling) {
    ring_buffer_t rb;
    uint8_t buffer[TEST_BUFFER_SIZE];
    
    ASSERT_EQ(ring_buffer_init(NULL, buffer, TEST_BUFFER_SIZE), RING_BUFFER_ERROR_NULL);
    ASSERT_EQ(ring_buffer_init(&rb, NULL, TEST_BUFFER_SIZE), RING_BUFFER_ERROR_NULL);
    
    ASSERT_EQ(ring_buffer_create(NULL, TEST_BUFFER_SIZE), RING_BUFFER_ERROR_NULL);
    
    ASSERT_EQ(ring_buffer_write(NULL, (uint8_t*)"", 1), RING_BUFFER_ERROR_NULL);
    
    uint8_t data = 0;
    ASSERT_EQ(ring_buffer_read(NULL, &data, 1), RING_BUFFER_ERROR_NULL);
}

/* Test: Error strings */
TEST(error_strings) {
    ASSERT(strcmp(ring_buffer_error_string(RING_BUFFER_OK), "Success") == 0);
    ASSERT(strcmp(ring_buffer_error_string(RING_BUFFER_ERROR_NULL), "Null pointer") == 0);
    ASSERT(strcmp(ring_buffer_error_string(RING_BUFFER_ERROR_FULL), "Buffer is full") == 0);
    ASSERT(strcmp(ring_buffer_error_string(RING_BUFFER_ERROR_EMPTY), "Buffer is empty") == 0);
}

/* Test: Large buffer operations */
TEST(large_buffer) {
    const size_t large_size = 4096;
    ring_buffer_t rb;
    ring_buffer_error_t err = ring_buffer_create(&rb, large_size);
    ASSERT_OK(err);
    
    /* Fill the buffer */
    uint8_t *large_data = (uint8_t *)malloc(large_size);
    ASSERT(large_data != NULL);
    
    for (size_t i = 0; i < large_size; i++) {
        large_data[i] = (uint8_t)(i % 256);
    }
    
    int written = ring_buffer_write(&rb, large_data, large_size);
    ASSERT_EQ((size_t)written, large_size);
    ASSERT(ring_buffer_is_full(&rb));
    
    /* Read and verify */
    uint8_t *read_data = (uint8_t *)malloc(large_size);
    ASSERT(read_data != NULL);
    
    int read = ring_buffer_read(&rb, read_data, large_size);
    ASSERT_EQ((size_t)read, large_size);
    ASSERT(memcmp(large_data, read_data, large_size) == 0);
    
    free(large_data);
    free(read_data);
    ring_buffer_destroy(&rb);
}

int main(void) {
    printf("=== Ring Buffer Test Suite ===\n\n");
    
    /* Basic operations */
    RUN_TEST(init_static_buffer);
    RUN_TEST(create_dynamic_buffer);
    RUN_TEST(write_read_single_byte);
    RUN_TEST(write_read_multiple_bytes);
    
    /* Advanced operations */
    RUN_TEST(buffer_wrap_around);
    RUN_TEST(full_buffer_rejection);
    RUN_TEST(partial_write);
    RUN_TEST(empty_buffer_read);
    
    /* Peek and skip */
    RUN_TEST(peek_operations);
    RUN_TEST(skip_operations);
    
    /* Other features */
    RUN_TEST(reset_buffer);
    RUN_TEST(find_byte);
    RUN_TEST(typed_item_operations);
    RUN_TEST(zero_copy_operations);
    
    /* Error handling */
    RUN_TEST(null_pointer_handling);
    RUN_TEST(error_strings);
    
    /* Large buffer */
    RUN_TEST(large_buffer);
    
    printf("\n=== Test Results ===\n");
    printf("Passed: %d\n", tests_passed);
    printf("Failed: %d\n", tests_failed);
    
    return tests_failed > 0 ? 1 : 0;
}