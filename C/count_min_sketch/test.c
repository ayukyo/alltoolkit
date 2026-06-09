#include <stdio.h>
#include <string.h>
#include "count_min_sketch.h"

void test_basic() {
    cms_sketch_t* sketch = cms_new(5, 100);
    
    cms_increment(sketch, "hello", 5);
    cms_increment(sketch, "hello", 5);
    cms_increment(sketch, "world", 5);
    
    uint64_t hello = cms_estimate(sketch, "hello", 5);
    uint64_t world = cms_estimate(sketch, "world", 5);
    uint64_t missing = cms_estimate(sketch, "missing", 7);
    
    printf("hello: %lu, world: %lu, missing: %lu\n", hello, world, missing);
    
    if (hello >= 2 && world >= 1 && missing == 0) {
        printf("✓ Test 1: Basic increment PASSED\n");
    } else {
        printf("✗ Test 1: FAILED\n");
    }
    
    cms_free(sketch);
}

void test_update() {
    cms_sketch_t* sketch = cms_new(5, 100);
    cms_update(sketch, "item", 4, 5);
    
    uint64_t est = cms_estimate(sketch, "item", 4);
    if (est >= 5) {
        printf("✓ Test 2: Update with delta PASSED\n");
    } else {
        printf("✗ Test 2: FAILED (got %lu)\n", est);
    }
    
    cms_free(sketch);
}

void test_total() {
    cms_sketch_t* sketch = cms_new(5, 100);
    cms_increment(sketch, "a", 1);
    cms_update(sketch, "b", 1, 3);
    cms_increment(sketch, "c", 1);
    
    if (cms_total_count(sketch) == 5) {
        printf("✓ Test 3: Total count PASSED\n");
    } else {
        printf("✗ Test 3: FAILED (got %lu)\n", cms_total_count(sketch));
    }
    
    cms_free(sketch);
}

void test_merge() {
    cms_sketch_t* a = cms_new(5, 100);
    cms_sketch_t* b = cms_new(5, 100);
    
    cms_increment(a, "hello", 5);
    cms_increment(b, "world", 5);
    cms_increment(b, "world", 5);
    
    int err = cms_merge(a, b);
    if (err == CMS_OK && cms_estimate(a, "hello", 5) >= 1 && cms_estimate(a, "world", 5) >= 2) {
        printf("✓ Test 4: Merge PASSED\n");
    } else {
        printf("✗ Test 4: FAILED (err=%d)\n", err);
    }
    
    cms_free(a);
    cms_free(b);
}

void test_clear() {
    cms_sketch_t* sketch = cms_new(5, 100);
    cms_increment(sketch, "test", 4);
    
    cms_clear(sketch);
    
    if (cms_estimate(sketch, "test", 4) == 0) {
        printf("✓ Test 5: Clear PASSED\n");
    } else {
        printf("✗ Test 5: FAILED\n");
    }
    
    cms_free(sketch);
}

void test_dimensions() {
    cms_sketch_t* sketch = cms_new(7, 200);
    size_t d, w;
    cms_dimensions(sketch, &d, &w);
    
    if (d == 7 && w == 200) {
        printf("✓ Test 6: Dimensions PASSED\n");
    } else {
        printf("✗ Test 6: FAILED (got %zu, %zu)\n", d, w);
    }
    
    cms_free(sketch);
}

int main() {
    printf("Running Count-Min Sketch C tests...\n\n");
    
    test_basic();
    test_update();
    test_total();
    test_merge();
    test_clear();
    test_dimensions();
    
    printf("\n✅ All tests completed!\n");
    return 0;
}
