#include "count_min_sketch.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

#define FNV_PRIME 0x100000001b3ULL

static uint64_t fnv_hash(const char* data, size_t len, uint64_t seed) {
    uint64_t hash = 0xcbf29ce484222325ULL ^ seed;
    for (size_t i = 0; i < len; i++) {
        hash = hash * FNV_PRIME + (uint8_t)data[i];
    }
    return hash;
}

static void get_hashes(const cms_sketch_t* sketch, const char* item, size_t len, uint64_t* out) {
    uint64_t h1 = fnv_hash(item, len, 0);
    uint64_t h2 = fnv_hash(item, len, sketch->seed);
    
    for (size_t i = 0; i < sketch->depth; i++) {
        out[i] = h1 + i * h2;
    }
}

cms_sketch_t* cms_new(size_t depth, size_t width) {
    if (depth < 1) depth = 1;
    if (width < 2) width = 2;
    
    cms_sketch_t* sketch = (cms_sketch_t*)malloc(sizeof(cms_sketch_t));
    if (!sketch) return NULL;
    
    sketch->depth = depth;
    sketch->width = width;
    sketch->seed = 0xDEADBEEF;
    sketch->total_count = 0;
    
    sketch->table = (uint64_t**)malloc(depth * sizeof(uint64_t*));
    if (!sketch->table) {
        free(sketch);
        return NULL;
    }
    
    for (size_t i = 0; i < depth; i++) {
        sketch->table[i] = (uint64_t*)calloc(width, sizeof(uint64_t));
        if (!sketch->table[i]) {
            for (size_t j = 0; j < i; j++) free(sketch->table[j]);
            free(sketch->table);
            free(sketch);
            return NULL;
        }
    }
    
    return sketch;
}

cms_sketch_t* cms_new_default(void) {
    return cms_new(10, 1000);
}

void cms_free(cms_sketch_t* sketch) {
    if (!sketch) return;
    for (size_t i = 0; i < sketch->depth; i++) {
        free(sketch->table[i]);
    }
    free(sketch->table);
    free(sketch);
}

void cms_update(cms_sketch_t* sketch, const char* item, size_t item_len, uint64_t delta) {
    uint64_t hashes[64];  // max depth
    get_hashes(sketch, item, item_len, hashes);
    
    for (size_t i = 0; i < sketch->depth; i++) {
        size_t idx = hashes[i] % sketch->width;
        sketch->table[i][idx] += delta;
    }
    sketch->total_count += delta;
}

void cms_increment(cms_sketch_t* sketch, const char* item, size_t item_len) {
    cms_update(sketch, item, item_len, 1);
}

uint64_t cms_estimate(const cms_sketch_t* sketch, const char* item, size_t item_len) {
    uint64_t hashes[64];
    get_hashes(sketch, item, item_len, hashes);
    
    uint64_t min_val = sketch->table[0][hashes[0] % sketch->width];
    for (size_t i = 1; i < sketch->depth; i++) {
        size_t idx = hashes[i] % sketch->width;
        uint64_t val = sketch->table[i][idx];
        if (val < min_val) min_val = val;
    }
    return min_val;
}

uint64_t cms_total_count(const cms_sketch_t* sketch) {
    return sketch->total_count;
}

int cms_merge(cms_sketch_t* dest, const cms_sketch_t* src) {
    if (dest->depth != src->depth || dest->width != src->width) {
        return CMS_ERR_DIM_MISMATCH;
    }
    
    for (size_t i = 0; i < dest->depth; i++) {
        for (size_t j = 0; j < dest->width; j++) {
            dest->table[i][j] += src->table[i][j];
        }
    }
    dest->total_count += src->total_count;
    return CMS_OK;
}

uint8_t* cms_to_bytes(const cms_sketch_t* sketch, size_t* out_len) {
    size_t size = 32 + sketch->depth * sketch->width * 8;
    uint8_t* bytes = (uint8_t*)malloc(size);
    if (!bytes) return NULL;
    
    memset(bytes, 0, size);
    
    size_t offset = 0;
    
    // depth (8 bytes)
    for (int i = 0; i < 8; i++) bytes[offset++] = (sketch->depth >> (i * 8)) & 0xFF;
    // width (8 bytes)
    for (int i = 0; i < 8; i++) bytes[offset++] = (sketch->width >> (i * 8)) & 0xFF;
    // seed (8 bytes)
    for (int i = 0; i < 8; i++) bytes[offset++] = (sketch->seed >> (i * 8)) & 0xFF;
    // total_count (8 bytes)
    for (int i = 0; i < 8; i++) bytes[offset++] = (sketch->total_count >> (i * 8)) & 0xFF;
    
    for (size_t i = 0; i < sketch->depth; i++) {
        for (size_t j = 0; j < sketch->width; j++) {
            uint64_t val = sketch->table[i][j];
            for (int k = 0; k < 8; k++) bytes[offset++] = (val >> (k * 8)) & 0xFF;
        }
    }
    
    *out_len = size;
    return bytes;
}

cms_sketch_t* cms_from_bytes(const uint8_t* bytes, size_t len) {
    if (len < 32) return NULL;
    
    size_t offset = 0;
    size_t depth = 0, width = 0;
    uint64_t seed = 0, total_count = 0;
    
    for (int i = 0; i < 8; i++) depth |= ((size_t)bytes[offset++]) << (i * 8);
    for (int i = 0; i < 8; i++) width |= ((size_t)bytes[offset++]) << (i * 8);
    for (int i = 0; i < 8; i++) seed |= ((uint64_t)bytes[offset++]) << (i * 8);
    for (int i = 0; i < 8; i++) total_count |= ((uint64_t)bytes[offset++]) << (i * 8);
    
    size_t expected = 32 + depth * width * 8;
    if (len < expected) return NULL;
    
    cms_sketch_t* sketch = cms_new(depth, width);
    if (!sketch) return NULL;
    
    sketch->seed = seed;
    sketch->total_count = total_count;
    
    for (size_t i = 0; i < depth; i++) {
        for (size_t j = 0; j < width; j++) {
            uint64_t val = 0;
            for (int k = 0; k < 8; k++) val |= ((uint64_t)bytes[offset++]) << (k * 8);
            sketch->table[i][j] = val;
        }
    }
    
    return sketch;
}

void cms_clear(cms_sketch_t* sketch) {
    for (size_t i = 0; i < sketch->depth; i++) {
        memset(sketch->table[i], 0, sketch->width * sizeof(uint64_t));
    }
    sketch->total_count = 0;
}

cms_config_t cms_optimal(double epsilon, double delta) {
    cms_config_t config;
    config.width = (size_t)ceil(exp(1.0) / epsilon);
    config.depth = (size_t)ceil(-log(delta));
    config.seed = 0xDEADBEEF;
    if (config.depth < 1) config.depth = 1;
    if (config.width < 2) config.width = 2;
    return config;
}

cms_sketch_t* cms_with_rate(double epsilon, double delta) {
    cms_config_t config = cms_optimal(epsilon, delta);
    return cms_new(config.depth, config.width);
}

void cms_dimensions(const cms_sketch_t* sketch, size_t* depth, size_t* width) {
    if (depth) *depth = sketch->depth;
    if (width) *width = sketch->width;
}