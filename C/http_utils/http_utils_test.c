/**
 * @file http_utils_test.c
 * @brief Unit tests for HTTP Client Utilities
 * @author AllToolkit
 * @version 1.0.0
 */

#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "mod.h"

/* Test statistics */
static int tests_run = 0;
static int tests_passed = 0;
static int tests_failed = 0;

/* Test macros */
#define TEST(name) void test_##name(void)
#define RUN_TEST(name) do { \
    printf("  Running %s... ", #name); \
    test_##name(); \
    tests_run++; \
    printf("PASSED\n"); \
    tests_passed++; \
} while(0)

#define ASSERT_TRUE(expr) do { \
    if (!(expr)) { \
        printf("FAILED\n  Assertion failed: %s at line %d\n", #expr, __LINE__); \
        tests_failed++; \
        return; \
    } \
} while(0)

#define ASSERT_FALSE(expr) ASSERT_TRUE(!(expr))
#define ASSERT_NULL(ptr) ASSERT_TRUE((ptr) == NULL)
#define ASSERT_NOT_NULL(ptr) ASSERT_TRUE((ptr) != NULL)
#define ASSERT_EQ(a, b) ASSERT_TRUE((a) == (b))
#define ASSERT_STR_EQ(a, b) ASSERT_TRUE(strcmp((a), (b)) == 0)
#define ASSERT_INT_EQ(a, b) ASSERT_EQ((a), (b))

/* ============================================================================
 * URL Parsing Tests
 * ============================================================================ */

TEST(url_parse_simple) {
    UrlComponents *comp = url_parse("https://example.com/path");
    ASSERT_NOT_NULL(comp);
    ASSERT_STR_EQ(comp->scheme, "https");
    ASSERT_STR_EQ(comp->host, "example.com");
    ASSERT_STR_EQ(comp->path, "/path");
    ASSERT_INT_EQ(comp->port, 443);
    url_components_free(comp);
}

TEST(url_parse_with_port) {
    UrlComponents *comp = url_parse("http://localhost:8080/api");
    ASSERT_NOT_NULL(comp);
    ASSERT_STR_EQ(comp->scheme, "http");
    ASSERT_STR_EQ(comp->host, "localhost");
    ASSERT_INT_EQ(comp->port, 8080);
    ASSERT_STR_EQ(comp->path, "/api");
    url_components_free(comp);
}

TEST(url_parse_with_query) {
    UrlComponents *comp = url_parse("https://api.example.com/search?q=test&page=1");
    ASSERT_NOT_NULL(comp);
    ASSERT_STR_EQ(comp->scheme, "https");
    ASSERT_STR_EQ(comp->host, "api.example.com");
    ASSERT_STR_EQ(comp->path, "/search");
    ASSERT_STR_EQ(comp->query, "q=test&page=1");
    url_components_free(comp);
}

TEST(url_parse_with_fragment) {
    UrlComponents *comp = url_parse("https://example.com/page#section");
    ASSERT_NOT_NULL(comp);
    ASSERT_STR_EQ(comp->scheme, "https");
    ASSERT_STR_EQ(comp->host, "example.com");
    ASSERT_STR_EQ(comp->path, "/page");
    ASSERT_STR_EQ(comp->fragment, "section");
    url_components_free(comp);
}

TEST(url_parse_with_userinfo) {
    UrlComponents *comp = url_parse("https://user:pass@example.com/");
    ASSERT_NOT_NULL(comp);
    ASSERT_STR_EQ(comp->scheme, "https");
    ASSERT_STR_EQ(comp->userinfo, "user:pass");
    ASSERT_STR_EQ(comp->host, "example.com");
    url_components_free(comp);
}

TEST(url_parse_null) {
    UrlComponents *comp = url_parse(NULL);
    ASSERT_NULL(comp);
}

TEST(url_parse_empty) {
    UrlComponents *comp = url_parse("");
    ASSERT_NULL(comp);
}

/* ============================================================================
 * URL Building Tests
 * ============================================================================ */

TEST(url_build_simple) {
    UrlComponents comp = {0};
    comp.scheme = strdup_safe("https");
    comp.host = strdup_safe("example.com");
    comp.path = strdup_safe("/path");
    
    char *url = url_build(&comp);
    ASSERT_NOT_NULL(url);
    ASSERT_STR_EQ(url, "https://example.com/path");
    
    free(url);
    free(comp.scheme);
    free(comp.host);
    free(comp.path);
}

TEST(url_build_with_port) {
    UrlComponents comp = {0};
    comp.scheme = strdup_safe("http");
    comp.host = strdup_safe("localhost");
    comp.port = 8080;
    comp.path = strdup_safe("/api");
    
    char *url = url_build(&comp);
    ASSERT_NOT_NULL(url);
    ASSERT_STR_EQ(url, "http://localhost:8080/api");
    
    free(url);
    free(comp.scheme);
    free(comp.host);
    free(comp.path);
}

TEST(url_build_with_query) {
    UrlComponents comp = {0};
    comp.scheme = strdup_safe("https");
    comp.host = strdup_safe("api.example.com");
    comp.path = strdup_safe("/search");
    comp.query = strdup_safe("q=test");
    
    char *url = url_build(&comp);
    ASSERT_NOT_NULL(url);
    ASSERT_STR_EQ(url, "https://api.example.com/search?q=test");
    
    free(url);
    free(comp.scheme);
    free(comp.host);
    free(comp.path);
    free(comp.query);
}

/* ============================================================================
 * URL Encoding Tests
 * ============================================================================ */

TEST(url_encode_simple) {
    char *encoded = url_encode("hello world");
    ASSERT_NOT_NULL(encoded);
    ASSERT_STR_EQ(encoded, "hello+world");
    free(encoded);
}

TEST(url_encode_special) {
    char *encoded = url_encode("test@example.com");
    ASSERT_NOT_NULL(encoded);
    ASSERT_STR_EQ(encoded, "test%40example.com");
    free(encoded);
}

TEST(url_encode_empty) {
    char *encoded = url_encode("");
    ASSERT_NOT_NULL(encoded);
    ASSERT_STR_EQ(encoded, "");
    free(encoded);
}

TEST(url_encode_null) {
    char *encoded = url_encode(NULL);
    ASSERT_NULL(encoded);
}

TEST(url_decode_simple) {
    char *decoded = url_decode("hello+world");
    ASSERT_NOT_NULL(decoded);
    ASSERT_STR_EQ(decoded, "hello world");
    free(decoded);
}

TEST(url_decode_percent) {
    char *decoded = url_decode("test%40example.com");
    ASSERT_NOT_NULL(decoded);
    ASSERT_STR_EQ(decoded, "test@example.com");
    free(decoded);
}

TEST(url_decode_empty) {
    char *decoded = url_decode("");
    ASSERT_NOT_NULL(decoded);
    ASSERT_STR_EQ(decoded, "");
    free(decoded);
}

TEST(url_decode_null) {
    char *decoded = url_decode(NULL);
    ASSERT_NULL(decoded);
}

/* ============================================================================
 * URL Validation Tests
 * ============================================================================ */

TEST(url_is_valid_valid) {
    ASSERT_TRUE(url_is_valid("https://example.com"));
    ASSERT_TRUE(url_is_valid("http://localhost:8080"));
    ASSERT_TRUE(url_is_valid("https://api.example.com/v1/users"));
}

TEST(url_is_valid_invalid) {
    ASSERT_FALSE(url_is_valid(NULL));
    ASSERT_FALSE(url_is_valid(""));
    ASSERT_FALSE(url_is_valid("not a url"));
    ASSERT_FALSE(url_is_valid("example.com"));  /* Missing scheme */
}

/* ============================================================================
 * URL Component Extraction Tests
 * ============================================================================ */

TEST(url_get_domain) {
    char *domain = url_get_domain("https://api.example.com/path");
    ASSERT_NOT_NULL(domain);
    ASSERT_STR_EQ(domain, "api.example.com");
    free(domain);
}

TEST(url_get_path) {
    char *path = url_get_path("https://example.com/api/v1/users");
    ASSERT_NOT_NULL(path);
    ASSERT_STR_EQ(path, "/api/v1/users");
    free(path);
}

/* ============================================================================
 * Query String Tests
 * ============================================================================ */

TEST(url_build_query_string) {
    const char *keys[] = {"name", "age"};
    const char *values[] = {"John", "30"};
    
    char *query = url_build_query_string(keys, values, 2);
    ASSERT_NOT_NULL(query);
    ASSERT_TRUE(strstr(query, "name=John") != NULL);
    ASSERT_TRUE(strstr(query, "age=30") != NULL);
    free(query);
}

TEST(url_build_query_string_empty) {
    char *query = url_build_query_string(NULL, NULL, 0);
    ASSERT_NOT_NULL(query);
    ASSERT_STR_EQ(query, "");
    free(query);
}

TEST(url_add_params) {
    const char *keys[] = {"q", "page"};
    const char *values[] = {"hello world", "1"};
    
    char *url = url_add_params("https://api.example.com/search", keys, values, 2);
    ASSERT_NOT_NULL(url);
    ASSERT_TRUE(strstr(url, "https://api.example.com/search") != NULL);
    ASSERT_TRUE(strstr(url, "q=hello+world") != NULL);
    ASSERT_TRUE(strstr(url, "page=1") != NULL);
    free(url);
}

/* ============================================================================
 * Header Tests
 * ============================================================================ */

TEST(http_headers_new) {
    HttpHeaders *headers = http_headers_new();
    ASSERT_NOT_NULL(headers);
    ASSERT_INT_EQ(headers->count, 0);
    ASSERT_NULL(headers->first);
    http_headers_free(headers);
}

TEST(http_headers_add) {
    HttpHeaders *headers = http_headers_new();
    http_headers_add(headers, "Content-Type", "application/json");
    http_headers_add(headers, "Authorization", "Bearer token123");
    
    ASSERT_INT_EQ(headers->count, 2);
    ASSERT_NOT_NULL(http_headers_get(headers, "Content-Type"));
    ASSERT_STR_EQ(http_headers_get(headers, "Content-Type"), "application/json");
    ASSERT_STR_EQ(http_headers_get(headers, "Authorization"), "Bearer token123");
    
    http_headers_free(headers);
}

TEST(http_headers_get_case_insensitive) {
    HttpHeaders *headers = http_headers_new();
    http_headers_add(headers, "Content-Type", "application/json");
    
    ASSERT_STR_EQ(http_headers_get(headers, "content-type"), "application/json");
    ASSERT_STR_EQ(http_headers_get(headers, "CONTENT-TYPE"), "application/json");
    
    http_headers_free(headers);
}

TEST(http_headers_get_not_found) {
    HttpHeaders *headers = http_headers_new();
    ASSERT_NULL(http_headers_get(headers, "X-Custom-Header"));
    http_headers_free(headers);
}

/* ============================================================================
 * Request Options Tests
 * ============================================================================ */

TEST(http_options_new) {
    HttpRequestOptions *options = http_options_new();
    ASSERT_NOT_NULL(options);
    ASSERT_INT_EQ(options->timeout, HTTP_UTILS_DEFAULT_TIMEOUT);
    ASSERT_TRUE(options->follow_redirects);
    ASSERT_INT_EQ(options->max_redirects, 10);
    ASSERT_TRUE(options->verify_ssl);
    http_options_free(options);
}

/* ============================================================================
 * Utility Tests
 * ============================================================================ */

TEST(http_utils_version) {
    const char *version = http_utils_version();
    ASSERT_NOT_NULL(version);
    ASSERT_TRUE(strlen(version) > 0);
}

TEST(http_status_text) {
    ASSERT_STR_EQ(http_status_text(200), "OK");
    ASSERT_STR_EQ(http_status_text(404), "Not Found");
    ASSERT_STR_EQ(http_status_text(500), "Internal Server Error");
    ASSERT_STR_EQ(http_status_text(0), "Unknown");
}

/* ============================================================================
 * Main Test Runner
 * ============================================================================ */

int main(void) {
    printf("\n========================================\n");
    printf("HTTP Utils Test Suite\n");
    printf("========================================\n\n");
    
    printf("URL Parsing Tests:\n");
    RUN_TEST(url_parse_simple);
    RUN_TEST(url_parse_with_port);
    RUN_TEST(url_parse_with_query);
    RUN_TEST(url_parse_with_fragment);
    RUN_TEST(url_parse_with_userinfo);
    RUN_TEST(url_parse_null);
    RUN_TEST(url_parse_empty);
    
    printf("\nURL Building Tests:\n");
    RUN_TEST(url_build_simple);
    RUN_TEST(url_build_with_port);
    RUN_TEST(url_build_with_query);
    
    printf("\nURL Encoding Tests:\n");
    RUN_TEST(url_encode_simple);
    RUN_TEST(url_encode_special);
    RUN_TEST(url_encode_empty);
    RUN_TEST(url_encode_null);
    RUN_TEST(url_decode_simple);
    RUN_TEST(url_decode_percent);
    RUN_TEST(url_decode_empty);
    RUN_TEST(url_decode_null);
    
    printf("\nURL Validation Tests:\n");
    RUN_TEST(url_is_valid_valid);
    RUN_TEST(url_is_valid_invalid);
    
    printf("\nURL Component Tests:\n");
    RUN_TEST(url_get_domain);
    RUN_TEST(url_get_path);
    
    printf("\nQuery String Tests:\n");
    RUN_TEST(url_build_query_string);
    RUN_TEST(url_build_query_string_empty);
    RUN_TEST(url_add_params);
    
    printf("\nHeader Tests:\n");
    RUN_TEST(http_headers_new);
    RUN_TEST(http_headers_add);
    RUN_TEST(http_headers_get_case_insensitive);
    RUN_TEST(http_headers_get_not_found);
    
    printf("\nRequest Options Tests:\n");
    RUN_TEST(http_options_new);
    
    printf("\nUtility Tests:\n");
    RUN_TEST(http_utils_version);
    RUN_TEST(http_status_text);
    
    printf("\n========================================\n");
    printf("Test Results: %d run, %d passed, %d failed\n", 
           tests_run, tests_passed, tests_failed);
    printf("========================================\n\n");
    
    return tests_failed > 0 ? 1 : 0;
}