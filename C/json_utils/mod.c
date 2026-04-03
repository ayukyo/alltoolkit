/**
 * @file mod.c
 * @brief Lightweight JSON Parser Implementation for C
 */

#include "mod.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

typedef struct { JsonValue** items; size_t size; size_t capacity; } JsonArrayData;
typedef struct JsonObjectEntry { char* key; JsonValue* value; struct JsonObjectEntry* next; } JsonObjectEntry;
typedef struct { JsonObjectEntry** buckets; size_t bucket_count; size_t size; } JsonObjectData;

struct JsonValue {
    JsonType type;
    int refcount;
    union { bool bool_val; double number_val; char* string_val; JsonArrayData array_val; JsonObjectData object_val; } data;
};

typedef struct { const char* json; size_t pos; size_t len; } JsonParser;

static void* json_malloc(size_t s) { return malloc(s); }
static void* json_realloc(void* p, size_t s) { return realloc(p, s); }
static void json_free(void* p) { free(p); }

static char* json_strdup(const char* str) {
    if (!str) return NULL;
    size_t len = strlen(str);
    char* copy = (char*)json_malloc(len + 1);
    if (copy) memcpy(copy, str, len + 1);
    return copy;
}

JsonValue* json_retain(JsonValue* v) { if (v) v->refcount++; return v; }

void json_release(JsonValue* v) {
    if (!v) return;
    v->refcount--;
    if (v->refcount > 0) return;
    switch (v->type) {
        case JSON_STRING: json_free(v->data.string_val); break;
        case JSON_ARRAY: {
            JsonArrayData* a = &v->data.array_val;
            for (size_t i = 0; i < a->size; i++) json_release(a->items[i]);
            json_free(a->items); break;
        }
        case JSON_OBJECT: {
            JsonObjectData* o = &v->data.object_val;
            for (size_t i = 0; i < o->bucket_count; i++) {
                JsonObjectEntry* e = o->buckets[i];
                while (e) { JsonObjectEntry* n = e->next; json_free(e->key); json_release(e->value); json_free(e); e = n; }
            }
            json_free(o->buckets); break;
        }
        default: break;
    }
    json_free(v);
}

int json_refcount(const JsonValue* v) { return v ? v->refcount : 0; }

static JsonValue* json_value_new(JsonType t) {
    JsonValue* v = (JsonValue*)json_malloc(sizeof(JsonValue));
    if (!v) return NULL;
    memset(v, 0, sizeof(JsonValue));
    v->type = t; v->refcount = 1;
    return v;
}

JsonValue* json_null_new(void) { return json_value_new(JSON_NULL); }
JsonValue* json_bool_new(bool val) { JsonValue* v = json_value_new(JSON_BOOL); if (v) v->data.bool_val = val; return v; }
JsonValue* json_number_new(double val) { JsonValue* v = json_value_new(JSON_NUMBER); if (v) v->data.number_val = val; return v; }

JsonValue* json_string_new(const char* val) {
    if (!val) return NULL;
    JsonValue* v = json_value_new(JSON_STRING);
    if (!v) return NULL;
    v->data.string_val = json_strdup(val);
    if (!v->data.string_val) { json_free(v); return NULL; }
    return v;
}

JsonValue* json_array_new(void) {
    JsonValue* v = json_value_new(JSON_ARRAY);
    if (!v) return NULL;
    v->data.array_val.items = NULL; v->data.array_val.size = 0; v->data.array_val.capacity = 0;
    return v;
}

JsonValue* json_object_new(void) {
    JsonValue* v = json_value_new(JSON_OBJECT);
    if (!v) return NULL;
    v->data.object_val.buckets = NULL; v->data.object_val.bucket_count = 0; v->data.object_val.size = 0;
    return v;
}

JsonType json_type(const JsonValue* v) { return v ? v->type : JSON_NULL; }
bool json_is_null(const JsonValue* v) { return v && v->type == JSON_NULL; }
bool json_is_bool(const JsonValue* v) { return v && v->type == JSON_BOOL; }
bool json_is_number(const JsonValue* v) { return v && v->type == JSON_NUMBER; }
bool json_is_string(const JsonValue* v) { return v && v->type == JSON_STRING; }
bool json_is_array(const JsonValue* v) { return v && v->type == JSON_ARRAY; }
bool json_is_object(const JsonValue* v) { return v && v->type == JSON_OBJECT; }

bool json_as_bool(const JsonValue* v, bool d) { return (v && v->type == JSON_BOOL) ? v->data.bool_val : d; }
double json_as_number(const JsonValue* v, double d) { return (v && v->type == JSON_NUMBER) ? v->data.number_val : d; }
int json_as_int(const JsonValue* v, int d) { return (v && v->type == JSON_NUMBER) ? (int)v->data.number_val : d; }
const char* json_as_string(const JsonValue* v, const char* d) { return (v && v->type == JSON_STRING) ? v->data.string_val : d; }

size_t json_array_length(const JsonValue* a) { return (a && a->type == JSON_ARRAY) ? a->data.array_val.size : 0; }

const JsonValue* json_array_get(const JsonValue* a, size_t i) {
    if (!a || a->type != JSON_ARRAY) return NULL;
    const JsonArrayData* arr = &a->data.array_val;
    return (i < arr->size) ? arr->items[i] : NULL;
}

void json_array_append(JsonValue* a, JsonValue* val) {
    if (!a || a->type != JSON_ARRAY || !val) return;
    JsonArrayData* arr = &a->data.array_val;
    if (arr->size >= arr->capacity) {
        size_t nc = arr->capacity == 0 ? 8 : arr->capacity * 2;
        JsonValue** ni = (JsonValue**)json_realloc(arr->items, nc * sizeof(JsonValue*));
        if (!ni) return;
        arr->items = ni; arr->capacity = nc;
    }
    arr->items[arr->size++] = json_retain(val);
}

JsonArrayIter json_array_iter(const JsonValue* a) {
    JsonArrayIter i = {a, 0, 0};
    if (a && a->type == JSON_ARRAY) i.count = a->data.array_val.size;
    return i;
}

const JsonValue* json_array_iter_next(JsonArrayIter* i) {
    return (i && i->array && i->index < i->count) ? json_array_get(i->array, i->index++) : NULL;
}

static unsigned int json_hash(const char* k) {
    unsigned int h = 5381; int c;
    while ((c = *k++)) h = ((h << 5) + h) + c;
    return h;
}

static void json_object_ensure_buckets(JsonObjectData* o) {
    if (o->bucket_count > 0) return;
    o->bucket_count = 16;
    o->buckets = (JsonObjectEntry**)json_malloc(o->bucket_count * sizeof(JsonObjectEntry*));
    if (o->buckets) memset(o->buckets, 0, o->bucket_count * sizeof(JsonObjectEntry*));
}

size_t json_object_count(const JsonValue* o) { return (o && o->type == JSON_OBJECT) ? o->data.object_val.size : 0; }

const JsonValue* json_object_get(const JsonValue* o, const char* k) {
    if (!o || o->type != JSON_OBJECT || !k) return NULL;
    const JsonObjectData* obj = &o->data.object_val;
    if (obj->bucket_count == 0) return NULL;
    unsigned int h = json_hash(k) % obj->bucket_count;
    JsonObjectEntry* e = obj->buckets[h];
    while (e) { if (strcmp(e->key, k) == 0) return e->value; e = e->next; }
    return NULL;
}

bool json_object_has(const JsonValue* o, const char* k) { return json_object_get(o, k) != NULL; }
bool json_object_get_bool(const JsonValue* o, const char* k, bool d) { return json_as_bool(json_object_get(o, k), d); }
double json_object_get_number(const JsonValue* o, const char* k, double d) { return json_as_number(json_object_get(o, k), d); }
int json_object_get_int(const JsonValue* o, const char* k, int d) { return json_as_int(json_object_get(o, k), d); }
const char* json_object_get_string(const JsonValue* o, const char* k, const char* d) { return json_as_string(json_object_get(o, k), d); }

void json_object_set(JsonValue* o, const char* k, JsonValue* val) {
    if (!o || o->type != JSON_OBJECT || !k || !val) return;
    JsonObjectData* obj = &o->data.object_val;
    json_object_ensure_buckets(obj);
    if (!obj->buckets) return;
    unsigned int h = json_hash(k) % obj->bucket_count;
    JsonObjectEntry* e = obj->buckets[h];
    while (e) {
        if (strcmp(e->key, k) == 0) { json_release(e->value); e->value = json_retain(val); return; }
        e = e->next;
    }
    e = (JsonObjectEntry*)json_malloc(sizeof(JsonObjectEntry));
    if (!e) return;
    e->key = json_strdup(k); e->value = json_retain(val); e->next = obj->buckets[h];
    obj->buckets[h] = e; obj->size++;
}

JsonObjectIter json_object_iter(const Json
