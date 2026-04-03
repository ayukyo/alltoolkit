/**
 * @file json_utils_example.c
 * @brief JSON Utilities Usage Examples
 * @author AllToolkit
 *
 * Demonstrates parsing, building, and manipulating JSON data
 * using the AllToolkit JSON utilities for C.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../json_utils/mod.h"

/* Example 1: Parse a simple JSON string */
void example_parse_simple() {
    printf("\n=== Example 1: Parse Simple JSON ===\n");
    
    const char* json = "{\"name\":\"John Doe\",\"age\":30,\"active\":true}";
    char error[256];
    
    JsonValue* root = json_parse(json, error, sizeof(error));
    if (!root) {
        printf("Parse error: %s\n", error);
        return;
    }
    
    printf("Parsed JSON:\n");
    printf("  Name: %s\n", json_object_get_string(root, "name", "N/A"));
    printf("  Age: %d\n", json_object_get_int(root, "age", 0));
    printf("  Active: %s\n", json_object_get_bool(root, "active", false) ? "true" : "false");
    
    json_release(root);
}

/* Example 2: Parse an array */
void example_parse_array() {
    printf("\n=== Example 2: Parse Array ===\n");
    
    const char* json = "[\"apple\", \"banana\", \"cherry\"]";
    JsonValue* arr = json_parse(json, NULL, 0);
    
    if (arr && json_is_array(arr)) {
        printf("Fruits:\n");
        for (size_t i = 0; i < json_array_length(arr); i++) {
            const JsonValue* item = json_array_get(arr, i);
            printf("  [%zu]: %s\n", i, json_as_string(item, "unknown"));
        }
    }
    
    json_release(arr);
}

/* Example 3: Parse nested objects */
void example_parse_nested() {
    printf("\n=== Example 3: Parse Nested Objects ===\n");
    
    const char* json = "{"
        "\"user\":{"
            "\"id\":12345,"
            "\"profile\":{"
                "\"email\":\"john@example.com\","
                "\"phone\":\"+1-555-0123\""
            "}"
        "}"
    "}";
    
    JsonValue* root = json_parse(json, NULL, 0);
    if (!root) return;
    
    const JsonValue* user = json_object_get(root, "user");
    const JsonValue* profile = json_object_get(user, "profile");
    
    printf("User ID: %d\n", json_object_get_int(user, "id", 0));
    printf("Email: %s\n", json_object_get_string(profile, "email", "N/A"));
    printf("Phone: %s\n", json_object_get_string(profile, "phone", "N/A"));
    
    json_release(root);
}

/* Example 4: Build JSON programmatically */
void example_build_json() {
    printf("\n=== Example 4: Build JSON Programmatically ===\n");
    
    JsonValue* root = json_object_new();
    JsonValue* items = json_array_new();
    
    /* Add items to array */
    for (int i = 1; i <= 3; i++) {
        JsonValue* item = json_object_new();
        JsonValue* id = json_number_new(i);
        JsonValue* name = json_string_new(i == 1 ? "First" : i == 2 ? "Second" : "Third");
        JsonValue* price = json_number_new(10.99 * i);
        
        json_object_set(item, "id", id);
        json_object_set(item, "name", name);
        json_object_set(item, "price", price);
        
        json_array_append(items, item);
        
        json_release(id);
        json_release(name);
        json_release(price);
        json_release(item);
    }
    
    JsonValue* count = json_number_new(3);
    JsonValue* total = json_number_new(65.97);
    
    json_object_set(root, "items", items);
    json_object_set(root, "count", count);
    json_object_set(root, "total", total);
    
    /* Serialize to string */
    char* compact = json_serialize(root);
    char* pretty = json_serialize_pretty(root, 2);
    
    printf("Compact:\n%s\n\n", compact);
    printf("Pretty:\n%s\n", pretty);
    
    json_free(compact);
    json_free(pretty);
    json_release(count);
    json_release(total);
    json_release(items);
    json_release(root);
}

/* Example 5: Iterate over array */
void example_iterate_array() {
    printf("\n=== Example 5: Iterate Over Array ===\n");
    
    const char* json = "[{\"name\":\"Alice\",\"score\":95},{\"name\":\"Bob\",\"score\":87}]";
    JsonValue* arr = json_parse(json, NULL, 0);
    
    if (!arr) return;
    
    printf("Students:\n");
    JsonArrayIter iter = json_array_iter(arr);
    const JsonValue* item;
    
    while ((item = json_array_iter_next(&iter)) != NULL) {
        const char* name = json_object_get_string(item, "name", "Unknown");
        int score = json_object_get_int(item, "score", 0);
        printf("  %s: %d\n", name, score);
    }
    
    json_release(arr);
}

/* Example 6: Iterate over object */
void example_iterate_object() {
    printf("\n=== Example 6: Iterate Over Object ===\n");
    
    const char* json = "{\"red\":\"#FF0000\",\"green\":\"#00FF00\",\"blue\":\"#0000FF\"}";
    JsonValue* obj = json_parse(json, NULL, 0);
    
    if (!obj) return;
    
    printf("Colors:\n");
    JsonObjectIter iter = json_object_iter(obj);
    JsonKeyValue kv;
    
    while ((kv = json_object_iter_next(&iter)).key != NULL) {
        printf("  %s: %s\n", kv.key, json_as_string(kv.value, ""));
    }
    
    json_release(obj);
}

/* Example 7: Type checking and safe access */
void example_type_checking() {
    printf("\n=== Example 7: Type Checking and Safe Access ===\n");
    
    const char* json = "{\"count\":42,\"ratio\":3.14,\"name\":\"test\",\"items\":[1,2,3],\"meta\":{}}";
    JsonValue* root = json_parse(json, NULL, 0);
    
    if (!root) return;
    
    const JsonValue* count = json_object_get(root, "count");
    const JsonValue* ratio = json_object_get(root, "ratio");
    const JsonValue* name = json_object_get(root, "name");
    const JsonValue* items = json_object_get(root, "items");
    const JsonValue* meta = json_object_get(root, "meta");
    
    printf("Type checking:\n");
    printf("  count is number: %s\n", json_is_number(count) ? "yes" : "no");
    printf("  ratio is number: %s\n", json_is_number(ratio) ? "yes" : "no");
    printf("  name is string: %s\n", json_is_string(name) ? "yes" : "no");
    printf("  items is array: %s\n", json_is_array(items) ? "yes" : "no");
    printf("  meta is object: %s\n", json_is_object(meta) ? "yes" : "no");
    
    /* Safe access with defaults */
    printf("\nSafe access with defaults:\n");
    printf("  count as int: %d\n", json_object_get_int(root, "count", 0));
    printf("  missing as int: %d\n", json_object_get_int(root, "missing", -1));
    printf("  name as string: %s\n", json_object_get_string(root, "name", "default"));
    printf("  missing as string: %s\n", json_object_get_string(root, "missing", "default"));
    
    json_release(root);
}

/* Example 8: Validate JSON */
void example_validate() {
    printf("\n=== Example 8: Validate JSON ===\n");
    
    const char* valid[] = {
        "{}",
        "[]",
        "\"hello\"",
        "123",
        "true",
        "null",
        "{\"a\":[1,2,3]}"
    };
    
    const char* invalid[] = {
        "",
        "{",
        "[1, 2,",
        "undefined",
        "{\"a\"}",
        "{a:1}"
    };
    
        printf("  \"%s\": %s\n", invalid[i], json_is_valid(invalid[i]) ? "valid" : "invalid");
    }
}

/* Example 9: Parse from file */
void example_parse_file() {
    printf("\n=== Example 9: Parse From File ===\n");
    
    /* Create a temporary JSON file */
    const char* filename = "/tmp/test_config.json";
    FILE* f = fopen(filename, "w");
    if (f) {
        fprintf(f, "{\"app\":\"MyApp\",\"version\":\"1.0.0\",\"debug\":true}");
        fclose(f);
        
        char error[256];
        JsonValue* root = json_parse_file(filename, error, sizeof(error));
        
        if (root) {
            printf("Config from file:\n");
            printf("  App: %s\n", json_object_get_string(root, "app", "N/A"));
            printf("  Version: %s\n", json_object_get_string(root, "version", "N/A"));
            printf("  Debug: %s\n", json_object_get_bool(root, "debug", false) ? "true" : "false");
            json_release(root);
        } else {
            printf("Failed to parse file: %s\n", error);
        }
        
        remove(filename);
    }
}

/* Example 10: Complex data structure */
void example_complex_structure() {
    printf("\n=== Example 10: Complex Data Structure ===\n");
    
    const char* json = "{"
        "\"company\":\"Acme Corp\","
        "\"employees\":["
            "{\"id\":1,\"name\":\"John Smith\",\"department\":\"Engineering\",\"salary\":85000},"
            "{\"id\":2,\"name\":\"Jane Doe\",\"department\":\"Marketing\",\"salary\":75000},"
            "{\"id\":3,\"name\":\"Bob Johnson\",\"department\":\"Engineering\",\"salary\":92000}"
        "],"
        "\"locations\":{"
            "\"hq\":\"New York\","
            "\"branch\":\"San Francisco\""
        "}"
    "}";
    
    JsonValue* root = json_parse(json, NULL, 0);
    if (!root) return;
    
    printf("Company: %s\n", json_object_get_string(root, "company", "N/A"));
    
    const JsonValue* employees = json_object_get(root, "employees");
    printf("\nEmployees (%zu total):\n", json_array_length(employees));
    
    double total_salary = 0;
    int eng_count = 0;
    
    for (size_t i = 0; i < json_array_length(employees); i++) {
        const JsonValue* emp = json_array_get(employees, i);
        const char* name = json_object_get_string(emp, "name", "Unknown");
        const char* dept = json_object_get_string(emp, "department", "Unknown");
        double salary = json_object_get_number(emp, "salary", 0);
        
        printf("  %s (%s): $%.0f\n", name, dept, salary);
        total_salary += salary;
        
        if (strcmp(dept, "Engineering") == 0) {
            eng_count++;
        }
    }
    
    printf("\nStatistics:\n");
    printf("  Average salary: $%.0f\n", total_salary / json_array_length(employees));
    printf("  Engineering employees: %d\n", eng_count);
    
    const JsonValue* locations = json_object_get(root, "locations");
    printf("\nLocations:\n");
    printf("  HQ: %s\n", json_object_get_string(locations, "hq", "N/A"));
    printf("  Branch: %s\n", json_object_get_string(locations, "branch", "N/A"));
    
    json_release(root);
}

/* ============================================================================
 * Main
 * ============================================================================ */

int main() {
    printf("JSON Utilities Examples\n");
    printf("=======================\n");
    
    example_parse_simple();
    example_parse_array();
    example_parse_nested();
    example_build_json();
    example_iterate_array();
    example_iterate_object();
    example_type_checking();
    example_validate();
    example_parse_file();
    example_complex_structure();
    
    printf("\n\nAll examples completed!\n");
    return 0;
}
