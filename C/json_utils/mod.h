/**
 * @file mod.h
 * @brief Lightweight JSON Parser for C
 * @author AllToolkit
 * @version 1.0.0
 *
 * A zero-dependency, lightweight JSON parser and builder for C.
 * Supports parsing JSON strings, building JSON objects, and
 * type-safe value access.
 *
 * Features:
 * - Parse JSON strings into structured data
 * - Build JSON objects programmatically
 * - Type-safe value access with defaults
 * - Memory management with reference counting
 * - UTF-8 string support
 * - No external dependencies (ANSI C compatible)
 */

#ifndef ALLTOOLKIT_JSON_UTILS_H
#define ALLTOOLKIT_JSON_UTILS_H

#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ============================================================================
 * Type Definitions
 * ============================================================================ */

/**
 * @brief JSON value types
 */
typedef enum {
    JSON_NULL = 0,
    JSON_BOOL,
    JSON_NUMBER,
    JSON_STRING,
    JSON_ARRAY,
    JSON_OBJECT
} JsonType;

/**
 * @brief JSON value structure (opaque)
 */
typedef struct JsonValue JsonValue;

/**
 * @brief JSON array iterator
 */
typedef struct {
    const JsonValue* array;
    size_t index;
    size_t count;
} JsonArrayIter;

/**
 * @brief JSON object iterator
 */
typedef struct {
    const JsonValue* object;
    size_t index;
    size_t count;
} JsonObjectIter;

/**
 * @brief Key-value pair for object iteration
 */
typedef struct {
    const char* key;
    const JsonValue* value;
} JsonKeyValue;

/* ============================================================================
 * Parsing Functions
 * ============================================================================ */

JsonValue* json_parse(const char* json, char* error_msg, size_t error_size);
JsonValue* json_parse_file(const char* filepath, char* error_msg, size_t error_size);
bool json_is_valid(const char* json);

/* ============================================================================
 * Type Checking Functions
 * ============================================================================ */

JsonType json_type(const JsonValue* value);
bool json_is_null(const JsonValue* value);
bool json_is_bool(const JsonValue* value);
bool json_is_number(const JsonValue* value);
bool json_is_string(const JsonValue* value);
bool json_is_array(const JsonValue* value);
bool json_is_object(const JsonValue* value);

/* ============================================================================
 * Value Access Functions
 * ============================================================================ */

bool json_as_bool(const JsonValue* value, bool default_val);
double json_as_number(const JsonValue* value, double default_val);
int json_as_int(const JsonValue* value, int default_val);
const char* json_as_string(const JsonValue* value, const char* default_val);

/* ============================================================================
 * Array Functions
 * ============================================================================ */

size_t json_array_length(const JsonValue* array);
const JsonValue* json_array_get(const JsonValue* array, size_t index);
JsonArrayIter json_array_iter(const JsonValue* array);
const JsonValue* json_array_iter_next(JsonArrayIter* iter);

/* ============================================================================
 * Object Functions
 * ============================================================================ */

size_t json_object_count(const JsonValue* object);
const JsonValue* json_object_get(const JsonValue* object, const char* key);
bool json_object_has(const JsonValue* object, const char* key);
bool json_object_get_bool(const JsonValue* object, const char* key, bool default_val);
double json_object_get_number(const JsonValue* object, const char* key, double default_val);
int json_object_get_int(const JsonValue* object, const char* key, int default_val);
const char* json_object_get_string(const JsonValue* object, const char* key, const char* default_val);
JsonObjectIter json_object_iter(const JsonValue* object);
JsonKeyValue json_object_iter_next(JsonObjectIter* iter);

/* ============================================================================
 * JSON Building Functions
 * ============================================================================ */

JsonValue* json_null_new(void);
JsonValue* json_bool_new(bool val);
JsonValue* json_number_new(double val);
JsonValue* json_string_new(const char* val);
JsonValue* json_array_new(void);
JsonValue* json_object_new(void);

/* ============================================================================
 * Array/Object Manipulation
 * ============================================================================ */

void json_array_append(JsonValue* array, JsonValue* value);
void json_object_set(JsonValue* object, const char* key, JsonValue* value);

/* ============================================================================
 * Serialization Functions
 * ============================================================================ */

/**
 * @brief Serialize JSON value to string
 * @param value The JSON value to serialize
 * @return char* Newly allocated string (caller must free), or NULL on error
 */
char* json_serialize(const JsonValue* value);

/**
 * @brief Serialize JSON value to pretty-printed string
 * @param value The JSON value to serialize
 * @param indent Number of spaces per indentation level
 * @return char* Newly allocated string (caller must free), or NULL on error
 */
char* json_serialize_pretty(const JsonValue* value, int indent);

/* ============================================================================
 * Memory Management
 * ============================================================================ */

/**
 * @brief Increment reference count
 * @param value The JSON value
 * @return JsonValue* The same value (for chaining)
 */
JsonValue* json_retain(JsonValue* value);

/**
 * @brief Decrement reference count, free if zero
 * @param value The JSON value
 */
void json_release(JsonValue* value);

/**
 * @brief Get reference count (for debugging)
 * @param value The JSON value
 * @return int Reference count
 */
int json_refcount(const JsonValue* value);

#ifdef __cplusplus
}
#endif

#endif /* ALLTOOLKIT_JSON_UTILS_H */
