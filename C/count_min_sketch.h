#ifndef COUNT_MIN_SKETCH_H
#define COUNT_MIN_SKETCH_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct cms_sketch {
    uint64_t** table;
    size_t depth;
    size_t width;
    uint64_t seed;
    uint64_t total_count;
} cms_sketch_t;

cms_sketch_t* cms_new(size_t depth, size_t width);
cms_sketch_t* cms_new_default(void);
void cms_free(cms_sketch_t* sketch);

void cms_update(cms_sketch_t* sketch, const char* item, size_t item_len, uint64_t delta);
void cms_increment(cms_sketch_t* sketch, const char* item, size_t item_len);
uint64_t cms_estimate(const cms_sketch_t* sketch, const char* item, size_t item_len);
uint64_t cms_total_count(const cms_sketch_t* sketch);

int cms_merge(cms_sketch_t* dest, const cms_sketch_t* src);

uint8_t* cms_to_bytes(const cms_sketch_t* sketch, size_t* out_len);
cms_sketch_t* cms_from_bytes(const uint8_t* bytes, size_t len);

void cms_clear(cms_sketch_t* sketch);

typedef struct { size_t depth; size_t width; uint64_t seed; } cms_config_t;
cms_config_t cms_optimal(double epsilon, double delta);
cms_sketch_t* cms_with_rate(double epsilon, double delta);

void cms_dimensions(const cms_sketch_t* sketch, size_t* depth, size_t* width);

#define CMS_OK 0
#define CMS_ERR_DIM_MISMATCH -1
#define CMS_ERR_TOO_SHORT -2
#define CMS_ERR_INVALID_LEN -3

#ifdef __cplusplus
}
#endif

#endif