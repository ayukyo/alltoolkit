/**
 * @file json_utils_test.c
 * @brief Unit tests for JSON Utilities
 * @author AllToolkit
 */

#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "mod.h"

static int tests_passed = 0;
static int tests_failed = 0;

#define TEST(name) void test_##name()
#define RUN_TEST(name) do { \
    printf("  Running " #name "... "); \
    test_##name(); \
    printf("PASSED\n"); \
    tests_passed++; \
} while(0)

#define ASSERT(expr) do { \
    if (!(expr)) { \
        printf("FAILED\n  Assertion failed: %s at line %d\n", #expr, __LINE__); \
        tests_failed++; \
        return; \
    } \
} while(0)

#define ASSERT_NULL(ptr) ASSERT((ptr) == NULL)
#define ASSERT_NOT_NULL(ptr) ASSERT((ptr) != NULL)
#define ASSERT_EQ(a, b) ASSERT((a) == (b))
#define ASSERT_STR_EQ(a, b) ASSERT(strcmp((a), (b)) == 0)
#define ASSERT_NEAR(a, b, eps) ASSERT(fabs((a) - (b)) < (eps))

/* ============================================================================
 * Parsing Tests
 * ============================================================================ */

TEST(parse_null) {
    char error[256];
    JsonValue* val = json_parse("null", error, sizeof(error));
    ASSERT_NOT_NULL(val);
    ASSERT(json_is_null(val));
    json_release(val);
}

TEST(parse_true) {
    JsonValue* val = json_parse("true", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT(json_is_bool(val));
    ASSERT_EQ(json_as_bool(val, false), true);
    json_release(val);
}

TEST(parse_false) {
    JsonValue* val = json_parse("false", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT(json_is_bool(val));
    ASSERT_EQ(json_as_bool(val, true), false);
    json_release(val);
}

TEST(parse_number_integer) {
    JsonValue* val = json_parse("42", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT(json_is_number(val));
    ASSERT_EQ(json_as_int(val, 0), 42);
    json_release(val);
}

TEST(parse_number_negative) {
    JsonValue* val = json_parse("-123", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT_EQ(json_as_int(val, 0), -123);
    json_release(val);
}

TEST(parse_number_float) {
    JsonValue* val = json_parse("3.14159", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT_NEAR(json_as_number(val, 0), 3.14159, 0.00001);
    json_release(val);
}

TEST(parse_number_scientific) {
    JsonValue* val = json_parse("1.5e10", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT_NEAR(json_as_number(val, 0), 1.5e10, 1e5);
    json_release(val);
}

TEST(parse_string_simple) {
    JsonValue* val = json_parse("\"hello\"", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT(json_is_string(val));
    ASSERT_STR_EQ(json_as_string(val, ""), "hello");
    json_release(val);
}

TEST(parse_string_escaped) {
    JsonValue* val = json_parse("\"hello\\nworld\"", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT_STR_EQ(json_as_string(val, ""), "hello\nworld");
    json_release(val);
}

TEST(parse_string_unicode_escape) {
    JsonValue* val = json_parse("\"hello\\tworld\"", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT_STR_EQ(json_as_string(val, ""), "hello\tworld");
    json_release(val);
}

TEST(parse_empty_array) {
    JsonValue* val = json_parse("[]", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT(json_is_array(val));
    ASSERT_EQ(json_array_length(val), 0);
    json_release(val);
}

TEST(parse_array_numbers) {
    JsonValue* val = json_parse("[1, 2, 3]", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT_EQ(json_array_length(val), 3);
    ASSERT_EQ(json_as_int(json_array_get(val, 0), 0), 1);
    ASSERT_EQ(json_as_int(json_array_get(val, 1), 0), 2);
    ASSERT_EQ(json_as_int(json_array_get(val, 2), 0), 3);
    json_release(val);
}

TEST(parse_array_mixed) {
    JsonValue* val = json_parse("[1, \"two\", true, null]", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT_EQ(json_array_length(val), 4);
    ASSERT(json_is_number(json_array_get(val, 0)));
    ASSERT(json_is_string(json_array_get(val, 1)));
    ASSERT(json_is_bool(json_array_get(val, 2)));
    ASSERT(json_is_null(json_array_get(val, 3)));
    json_release(val);
}

TEST(parse_nested_array) {
    JsonValue* val = json_parse("[[1, 2], [3, 4]]", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT_EQ(json_array_length(val), 2);
    const JsonValue* inner = json_array_get(val, 0);
    ASSERT(json_is_array(inner));
    ASSERT_EQ(json_array_length(inner), 2);
    json_release(val);
}

TEST(parse_empty_object) {
    JsonValue* val = json_parse("{}", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT(json_is_object(val));
    ASSERT_EQ(json_object_count(val), 0);
    json_release(val);
}

TEST(parse_simple_object) {
    JsonValue* val = json_parse("{\"name\":\"John\",\"age\":30}", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT(json_is_object(val));
    ASSERT_EQ(json_object_count(val), 2);
    ASSERT_STR_EQ(json_object_get_string(val, "name", ""), "John");
    ASSERT_EQ(json_object_get_int(val, "age", 0), 30);
    json_release(val);
}

TEST(parse_nested_object) {
    JsonValue* val = json_parse("{\"user\":{\"name\":\"John\"}}", NULL, 0);
    ASSERT_NOT_NULL(val);
    const JsonValue* user = json_object_get(val, "user");
    ASSERT_NOT_NULL(user);
    ASSERT(json_is_object(user));
    ASSERT_STR_EQ(json_object_get_string(user, "name", ""), "John");
    json_release(val);
}

TEST(parse_whitespace) {
    JsonValue* val = json_parse("  {  \"a\"  :  1  }  ", NULL, 0);
    ASSERT_NOT_NULL(val);
    ASSERT_EQ(json_object_get_int(val, "a", 0), 1);
    json_release(val);
}

TEST(parse_invalid_null) {
    char error[256];
    JsonValue* val = json_parse("nul", error, sizeof(error));
    ASSERT_NULL(val);
}

TEST(parse_invalid_trailing) {
    char error[256];
    JsonValue* val = json_parse("{}abc", error, sizeof(error));
    ASSERT_NULL(val);
}

TEST(parse_invalid_missing_bracket) {
    JsonValue* val = json_parse("[1, 2", NULL, 0);
    ASSERT_NULL(val);
}

TEST(parse_invalid_missing_brace) {
    JsonValue* val = json_parse("{\"a\":1", NULL, 0);
    ASSERT_NULL(val);
}

/* ============================================================================
 * Validation Tests
 * ============================================================================ */

TEST(validate_valid) {
    ASSERT_EQ(json_is_valid("{}"), true);
    ASSERT_EQ(json_is_valid("[]"), true);
    ASSERT_EQ(json_is_valid("\"hello\""), true);
    ASSERT_EQ(json_is_valid("123"), true);
    ASSERT_EQ(json_is_valid("true"), true);
    ASSERT_EQ(json_is_valid("false"), false);
}

TEST(validate_invalid) {
    ASSERT_EQ(json_is_valid(""), false);
    ASSERT_EQ(json_is_valid("{"), false);
    ASSERT_EQ(json_is_valid("undefined"), false);
}

/* ============================================================================
 * Building Tests
 * ============================================================================ */

TEST(build_null) {
    JsonValue* val = json_null_new();
    ASSERT_NOT_NULL(val);
    ASSERT(json_is_null(val));
    json_release(val);
}

TEST(build_bool) {
    JsonValue* val = json_bool_new(true);
    ASSERT_NOT_NULL(val);
    ASSERT(json_is_bool(val));
    ASSERT_EQ(json_as_bool(val, false), true);
    json_release(val);
}

TEST(build_number) {
    JsonValue* val = json_number_new(3.14);
    ASSERT_NOT_NULL(val);
    ASSERT(json_is_number(val));
    ASSERT_NEAR(json_as_number(val, 0), 3.14, 0.001);
    json_release(val);
}

TEST(build_string) {
    JsonValue* val = json_string_new("hello");
    ASSERT_NOT_NULL(val);

TEST(build_array) {
    JsonValue* arr = json_array_new();
    ASSERT_NOT_NULL(arr);
    ASSERT_EQ(json_array_length(arr), 0);
    
    JsonValue* n1 = json_number_new(1);
    JsonValue* n2 = json_number_new(2);
    json_array_append(arr, n1);
    json_array_append(arr, n2);
    
    ASSERT_EQ(json_array_length(arr), 2);
    ASSERT_EQ(json_as_int(json_array_get(arr, 0), 0), 1);
    ASSERT_EQ(json_as_int(json_array_get(arr, 1), 0), 2);
    
    json_release(n1);
    json_release(n2);
    json_release(arr);
}

TEST(build_object) {
    JsonValue* obj = json_object_new();
    ASSERT_NOT_NULL(obj);
    ASSERT_EQ(json_object_count(obj), 0);
    
    JsonValue* name = json_string_new("John");
    JsonValue* age = json_number_new(30);
    json_object_set(obj, "name", name);
    json_object_set(obj, "age", age);
    
    ASSERT_EQ(json_object_count(obj), 2);
    ASSERT_STR_EQ(json_object_get_string(obj, "name", ""), "John");
    ASSERT_EQ(json_object_get_int(obj, "age", 0), 30);
    
    json_release(name);
    json_release(age);
    json_release(obj);
}

TEST(build_complex) {
    JsonValue* root = json_object_new();
    JsonValue* items = json_array_new();
    
    for (int i = 1; i <= 3; i++) {
        JsonValue* item = json_object_new();
        JsonValue* id = json_number_new(i);
        JsonValue* name = json_string_new(i == 1 ? "first" : i == 2 ? "second" : "third");
        json_object_set(item, "id", id);
        json_object_set(item, "name", name);
        json_array_append(items, item);
        json_release(id);
        json_release(name);
        json_release(item);
    }
    
    JsonValue* count = json_number_new(3);
    json_object_set(root, "items", items);
    json_object_set(root, "count", count);
    
    ASSERT_EQ(json_object_get_int(root, "count", 0), 3);
    ASSERT_EQ(json_array_length(json_object_get(root, "items")), 3);
    
    json_release(count);
    json_release(items);
    json_release(root);
}

/* ============================================================================
 * Serialization Tests
 * ============================================================================ */

TEST(serialize_null) {
    JsonValue* val = json_null_new();
    char* str = json_serialize(val);
    ASSERT_STR_EQ(str, "null");
    json_free(str);
    json_release(val);
}

TEST(serialize_bool) {
    JsonValue* t = json_bool_new(true);
    JsonValue* f = json_bool_new(false);
    char* str_t = json_serialize(t);
    char* str_f = json_serialize(f);
    ASSERT_STR_EQ(str_t, "true");
    ASSERT_STR_EQ(str_f, "false");
    json_free(str_t);
    json_free(str_f);
    json_release(t);
    json_release(f);
}

TEST(serialize_number) {
    JsonValue* val = json_number_new(42);
    char* str = json_serialize(val);
    ASSERT_STR_EQ(str, "42");
    json_free(str);
    json_release(val);
}

TEST(serialize_string) {
    JsonValue* val = json_string_new("hello");
    char* str = json_serialize(val);
    ASSERT_STR_EQ(str, "\"hello\"");
    json_free(str);
    json_release(val);
}

TEST(serialize_string_escaped) {
    JsonValue* val = json_string_new("hello\nworld");
    char* str = json_serialize(val);
    ASSERT_STR_EQ(str, "\"hello\\nworld\"");
    json_free(str);
    json_release(val);
}

TEST(serialize_array) {
    JsonValue* arr = json_array_new();
    json_array_append(arr, json_number_new(1));
    json_array_append(arr, json_number_new(2));
    char* str = json_serialize(arr);
    ASSERT_STR_EQ(str, "[1,2]");
    json_free(str);
    json_release(arr);
}

TEST(serialize_object) {
    JsonValue* obj = json_object_new();
    json_object_set(obj, "a", json_number_new(1));
    json_object_set(obj, "b", json_string_new("test"));
    char* str = json_serialize(obj);
    ASSERT_NOT_NULL(str);
    ASSERT(strstr(str, "\"a\":1") != NULL);
    ASSERT(strstr(str, "\"b\":\"test\"") != NULL);
    json_free(str);
    json_release(obj);
}

TEST(serialize_pretty) {
    JsonValue* obj = json_object_new();
    json_object_set(obj, "name", json_string_new("test"));
    char* str = json_serialize_pretty(obj, 2);
    ASSERT_NOT_NULL(str);
    ASSERT(strstr(str, "\n") != NULL);
    json_free(str);
    json_release(obj);
}

/* ============================================================================
 * Iterator Tests
 * ============================================================================ */

TEST(iter_array) {
    JsonValue* arr = json_parse("[1, 2, 3]", NULL, 0);
    JsonArrayIter iter = json_array_iter(arr);
    int sum = 0;
    const JsonValue* v;
    while ((v = json_array_iter_next(&iter)) != NULL) {
        sum += json_as_int(v, 0);
    }
    ASSERT_EQ(sum, 6);
    json_release(arr);
}

TEST(iter_object) {
    JsonValue* obj = json_parse("{\"a\":1,\"b\":2}", NULL, 0);
    JsonObjectIter iter = json_object_iter(obj);
    int sum = 0;
    JsonKeyValue kv;
    while ((kv = json_object_iter_next(&iter)).key != NULL) {
        sum += json_as_int(kv.value, 0);
    }
    ASSERT_EQ(sum, 3);
    json_release(obj);
}

/* ============================================================================
 * Reference Counting Tests
 * ============================================================================ */

TEST(refcount_basic) {
    JsonValue* val = json_string_new("test");
    ASSERT_EQ(json_refcount(val), 1);
    json_retain(val);
    ASSERT_EQ(json_refcount(val), 2);
    json_release(val);
    ASSERT_EQ(json_refcount(val), 1);
    json_release(val);
}

/* ============================================================================
 * Main
 * ============================================================================ */

int main() {
    printf("Running JSON Utilities Tests...\n\n");
    
    printf("Parsing Tests:\n");
    RUN_TEST(parse_null);
    RUN_TEST(parse_true);
    RUN_TEST(parse_false);
    RUN_TEST(parse_number_integer);
    RUN_TEST(parse_number_negative);
    RUN_TEST(parse_number_float);
    RUN_TEST(parse_number_scientific);
    RUN_TEST(parse_string_simple);
    RUN_TEST(parse_string_escaped);
    RUN_TEST(parse_string_unicode_escape);
    RUN_TEST(parse_empty_array);
    RUN_TEST(parse_array_numbers);
    RUN_TEST(parse_array_mixed);
    RUN_TEST(parse_nested_array);
    RUN_TEST(parse_empty_object);
    RUN_TEST(parse_simple_object);
    RUN_TEST(parse_nested_object);
    RUN_TEST(parse_whitespace);
    RUN_TEST(parse_invalid_null);
    RUN_TEST(parse_invalid_trailing);
    RUN_TEST(parse_invalid_missing_bracket);
    RUN_TEST(parse_invalid_missing_brace);
    
    printf("\nValidation Tests:\n");
    RUN_TEST(validate_valid);
    RUN_TEST(validate_invalid);
    
    printf("\nBuilding Tests:\n");
    RUN_TEST(build_null);
    RUN_TEST(build_bool);
    RUN_TEST(build_number);
    RUN_TEST(build_string);
    RUN_TEST(build_array);
    RUN_TEST(build_object);
    RUN_TEST(build_complex);
    
    printf("\nSerialization Tests:\n");
    RUN_TEST(serialize_null);
    RUN_TEST(serialize_bool);
    RUN_TEST(serialize_number);
    RUN_TEST(serialize_string);
    RUN_TEST(serialize_string_escaped);
    RUN_TEST(serialize_array);
    RUN_TEST(serialize_object);
    RUN_TEST(serialize_pretty);
    
    printf("\nIterator Tests:\n");
    RUN_TEST(iter_array);
    RUN_TEST(iter_object);
    
    printf("\nReference Counting Tests:\n");
    RUN_TEST(refcount_basic);
    
    printf("\n========================================\n");
    printf("Tests passed: %d\n", tests_passed);
    printf("Tests failed: %d\n", tests_failed);
    printf("========================================\n");
    
    return tests_failed > 0 ? 1 : 0;
}
