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

}

JsonObjectIter json_object_iter(const JsonValue* o) {
    JsonObjectIter i = {o, 0, 0};
    if (o && o->type == JSON_OBJECT) i.count = o->data.object_val.size;
    return i;
}

JsonKeyValue json_object_iter_next(JsonObjectIter* i) {
    JsonKeyValue kv = {NULL, NULL};
    if (!i || !i->object || i->object->type != JSON_OBJECT) return kv;
    const JsonObjectData* obj = &i->object->data.object_val;
    size_t found = 0;
    for (size_t b = 0; b < obj->bucket_count && found <= i->index; b++) {
        JsonObjectEntry* e = obj->buckets[b];
        while (e && found <= i->index) {
            if (found == i->index) { kv.key = e->key; kv.value = e->value; i->index++; return kv; }
            found++; e = e->next;
        }
    }
    return kv;
}

static void parser_skip_ws(JsonParser* p) {
    while (p->pos < p->len && isspace((unsigned char)p->json[p->pos])) p->pos++;
}

static bool parser_match(JsonParser* p, const char* s) {
    size_t l = strlen(s);
    if (p->pos + l > p->len) return false;
    if (strncmp(p->json + p->pos, s, l) == 0) { p->pos += l; return true; }
    return false;
}

static JsonValue* parser_parse_null(JsonParser* p) {
    if (parser_match(p, "null")) return json_null_new();
    return NULL;
}

static JsonValue* parser_parse_bool(JsonParser* p) {
    if (parser_match(p, "true")) return json_bool_new(true);
    if (parser_match(p, "false")) return json_bool_new(false);
    return NULL;
}

static JsonValue* parser_parse_num(JsonParser* p) {
    size_t start = p->pos;
    bool has = false;
    if (p->pos < p->len && (p->json[p->pos] == '-' || p->json[p->pos] == '+')) p->pos++;
    while (p->pos < p->len && isdigit((unsigned char)p->json[p->pos])) { p->pos++; has = true; }
    if (p->pos < p->len && p->json[p->pos] == '.') {
        p->pos++;
        while (p->pos < p->len && isdigit((unsigned char)p->json[p->pos])) { p->pos++; has = true; }
    }
    if (has && p->pos < p->len && (p->json[p->pos] == 'e' || p->json[p->pos] == 'E')) {
        size_t ep = p->pos; p->pos++;
        if (p->pos < p->len && (p->json[p->pos] == '-' || p->json[p->pos] == '+')) p->pos++;
        bool hd = false;
        while (p->pos < p->len && isdigit((unsigned char)p->json[p->pos])) { p->pos++; hd = true; }
        if (!hd) p->pos = ep;
    }
    if (!has) { p->pos = start; return NULL; }
    char* ns = (char*)json_malloc(p->pos - start + 1);
    if (!ns) return NULL;
    memcpy(ns, p->json + start, p->pos - start);
    ns[p->pos - start] = 0;
    double val = strtod(ns, NULL);
    json_free(ns);
    return json_number_new(val);
}

static char* parser_parse_str_raw(JsonParser* p) {
    if (p->pos >= p->len || p->json[p->pos] != '"') return NULL;
    p->pos++;
    size_t start = p->pos, len = 0;
    while (p->pos < p->len && p->json[p->pos] != '"') {
        if (p->json[p->pos] == '\\' && p->pos + 1 < p->len) { p->pos += 2; }
        else { p->pos++; }
        len++;
    }
    if (p->pos >= p->len) return NULL;
    char* r = (char*)json_malloc(len + 1);
    if (!r) return NULL;
    size_t j = 0; p->pos = start;
    while (p->pos < p->len && p->json[p->pos] != '"') {
        if (p->json[p->pos] == '\\' && p->pos + 1 < p->len) {
            p->pos++;
            switch (p->json[p->pos]) {
                case '"': r[j++] = '"'; break; case '\\': r[j++] = '\\'; break;
                case '/': r[j++] = '/'; break; case 'b': r[j++] = '\b'; break;
                case 'f': r[j++] = '\f'; break; case 'n': r[j++] = '\n'; break;
                case 'r': r[j++] = '\r'; break; case 't': r[j++] = '\t'; break;
                default: r[j++] = p->json[p->pos]; break;
            }
            p->pos++;
        } else { r[j++] = p->json[p->pos++]; }
    }
    r[j] = 0;
    if (p->pos < p->len && p->json[p->pos] == '"') p->pos++;
    return r;
}

static JsonValue* parser_parse_str(JsonParser* p) {
    size_t start = p->pos;
    char* s = parser_parse_str_raw(p);
    if (s) { JsonValue* v = json_string_new(s); json_free(s); return v; }
    p->pos = start; return NULL;
}

static JsonValue* parser_parse_arr(JsonParser* p);
static JsonValue* parser_parse_obj(JsonParser* p);

static JsonValue* parser_parse_val(JsonParser* p) {
    parser_skip_ws(p);
    JsonValue* v;
    if ((v = parser_parse_null(p))) return v;
    if ((v = parser_parse_bool(p))) return v;
    if ((v = parser_parse_num(p))) return v;
    if ((v = parser_parse_str(p))) return v;
    if ((v = parser_parse_arr(p))) return v;
    if ((v = parser_parse_obj(p))) return v;
    return NULL;
}

static JsonValue* parser_parse_arr(JsonParser* p) {
    if (p->pos >= p->len || p->json[p->pos] != '[') return NULL;
    p->pos++;
    JsonValue* arr = json_array_new();
    if (!arr) return NULL;
    parser_skip_ws(p);
    if (p->pos < p->len && p->json[p->pos] == ']') { p->pos++; return arr; }
    while (p->pos < p->len) {
        JsonValue* e = parser_parse_val(p);
        if (!e) { json_release(arr); return NULL; }
        json_array_append(arr, e); json_release(e);
        parser_skip_ws(p);
        if (p->pos < p->len && p->json[p->pos] == ',') { p->pos++; }
        else if (p->pos < p->len && p->json[p->pos] == ']') { p->pos++; return arr; }
        else { json_release(arr); return NULL; }
    }
    json_release(arr); return NULL;
}

static JsonValue* parser_parse_obj(JsonParser* p) {
    if (p->pos >= p->len || p->json[p->pos] != '{') return NULL;
    p->pos++;
    JsonValue* obj = json_object_new();
    if (!obj) return NULL;
    parser_skip_ws(p);
    if (p->pos < p->len && p->json[p->pos] == '}') { p->pos++; return obj; }
    while (p->pos < p->len) {
        parser_skip_ws(p);
        char* k = parser_parse_str_raw(p);
        if (!k) { json_release(obj); return NULL; }
        parser_skip_ws(p);
        if (p->pos >= p->len || p->json[p->pos] != ':') { json_free(k); json_release(obj); return NULL; }
        p->pos++;
        JsonValue* v = parser_parse_val(p);
        if (!v) { json_free(k); json_release(obj); return NULL; }
        json_object_set(obj, k, v); json_release(v); json_free(k);
        parser_skip_ws(p);
        if (p->pos < p->len && p->json[p->pos] == ',') { p->pos++; }
        else if (p->pos < p->len && p->json[p->pos] == '}') { p->pos++; return obj; }
        else { json_release(obj); return NULL; }
    }
    json_release(obj); return NULL;
}

JsonValue* json_parse(const char* json, char* err, size_t err_sz) {
    if (!json) {
        if (err && err_sz > 0) { strncpy(err, "Null input", err_sz - 1); err[err_sz - 1] = 0; }
        return NULL;
    }
    JsonParser p = {json, 0, strlen(json)};
    JsonValue* v = parser_parse_val(&p);
    if (!v) {
        if (err && err_sz > 0) snprintf(err, err_sz, "Parse error at %zu", p.pos);
        return NULL;
    }
    parser_skip_ws(&p);
    if (p.pos != p.len) {
        if (err && err_sz > 0) snprintf(err, err_sz, "Trailing data at %zu", p.pos);
        json_release(v); return NULL;
    }
    return v;
}

JsonValue* json_parse_file(const char* fp, char* err, size_t err_sz) {
    FILE* f = fopen(fp, "rb");
    if (!f) {
        if (err && err_sz > 0) snprintf(err, err_sz, "Cannot open: %s", fp);
        return NULL;
    }
    fseek(f, 0, SEEK_END); long sz = ftell(f); fseek(f, 0, SEEK_SET);
    if (sz < 0) { fclose(f); if (err && err_sz > 0) { strncpy(err, "Cannot get size", err_sz - 1); err[err_sz - 1] = 0; } return NULL; }
    char* buf = (char*)json_malloc(sz + 1);
    if (!buf) { fclose(f); if (err && err_sz > 0) { strncpy(err, "Alloc failed", err_sz - 1); err[err_sz - 1] = 0; } return NULL; }
    size_t r = fread(buf, 1, sz, f); fclose(f); buf[r] = 0;
    JsonValue* v = json_parse(buf, err, err_sz); json_free(buf); return v;
}

bool json_is_valid(const char* json) {
    if (!json) return false;
