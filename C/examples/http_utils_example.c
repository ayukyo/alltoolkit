/**
 * @file http_utils_example.c
 * @brief HTTP Client Utilities Usage Examples
 * @author AllToolkit
 * @version 1.0.0
 *
 * This file demonstrates how to use the HTTP Utils library
 * for making HTTP requests and manipulating URLs.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../http_utils/mod.h"

/* Helper function to print response */
static void print_response(HttpResponse *response) {
    if (!response) {
        printf("Error: No response received\n");
        return;
    }
    
    printf("Status: %d %s\n", response->status_code, 
           response->status_text ? response->status_text : "Unknown");
    printf("Success: %s\n", response->success ? "true" : "false");
    printf("Response Time: %.3f seconds\n", response->response_time);
    printf("URL: %s\n", response->url ? response->url : "N/A");
    
    if (response->body) {
        printf("Body Length: %zu bytes\n", response->body_length);
        printf("Body (first 500 chars):\n%.500s%s\n\n", 
               response->body,
               response->body_length > 500 ? "..." : "");
    } else {
        printf("No body\n\n");
    }
}

/* Helper function to print URL components */
static void print_url_components(UrlComponents *comp) {
    if (!comp) {
        printf("Invalid URL\n");
        return;
    }
    
    printf("  Scheme: %s\n", comp->scheme ? comp->scheme : "(none)");
    printf("  Host: %s\n", comp->host ? comp->host : "(none)");
    printf("  Port: %d\n", comp->port);
    printf("  Path: %s\n", comp->path ? comp->path : "(none)");
    printf("  Query: %s\n", comp->query ? comp->query : "(none)");
    printf("  Fragment: %s\n", comp->fragment ? comp->fragment : "(none)");
    printf("  Userinfo: %s\n", comp->userinfo ? comp->userinfo : "(none)");
}

/* ============================================================================
 * Example 1: URL Parsing
 * ============================================================================ */
static void example_url_parsing(void) {
    printf("\n========================================\n");
    printf("Example 1: URL Parsing\n");
    printf("========================================\n\n");
    
    const char *urls[] = {
        "https://api.example.com/v1/users?page=1&limit=10",
        "http://localhost:8080/api/health",
        "https://user:pass@example.com:8443/path#section",
        NULL
    };
    
    for (int i = 0; urls[i]; i++) {
        printf("Parsing: %s\n", urls[i]);
        UrlComponents *comp = url_parse(urls[i]);
        print_url_components(comp);
        url_components_free(comp);
        printf("\n");
    }
}

/* ============================================================================
 * Example 2: URL Building
 * ============================================================================ */
static void example_url_building(void) {
    printf("\n========================================\n");
    printf("Example 2: URL Building\n");
    printf("========================================\n\n");
    
    UrlComponents comp = {0};
    comp.scheme = "https";
    comp.host = "api.example.com";
    comp.path = "/v1/search";
    comp.query = "q=hello+world&page=1";
    
    char *url = url_build(&comp);
    printf("Built URL: %s\n\n", url);
    free(url);
    
    /* Build with port */
    comp.port = 8443;
    url = url_build(&comp);
    printf("URL with port: %s\n\n", url);
    free(url);
}

/* ============================================================================
 * Example 3: URL Encoding/Decoding
 * ============================================================================ */
static void example_url_encoding(void) {
    printf("\n========================================\n");
    printf("Example 3: URL Encoding/Decoding\n");
    printf("========================================\n\n");
    
    const char *strings[] = {
        "hello world",
        "test@example.com",
        "special chars: &=?#",
        "Unicode: 你好世界",
        NULL
    };
    
    for (int i = 0; strings[i]; i++) {
        char *encoded = url_encode(strings[i]);
        char *decoded = url_decode(encoded);
        
        printf("Original: %s\n", strings[i]);
        printf("Encoded:  %s\n", encoded);
        printf("Decoded:  %s\n", decoded);
        printf("Match: %s\n\n", strcmp(strings[i], decoded) == 0 ? "YES" : "NO");
        
        free(encoded);
        free(decoded);
    }
}

/* ============================================================================
 * Example 4: Query String Building
 * ============================================================================ */
static void example_query_string(void) {
    printf("\n========================================\n");
    printf("Example 4: Query String Building\n");
    printf("========================================\n\n");
    
    const char *keys[] = {"name", "email", "age"};
    const char *values[] = {"John Doe", "john@example.com", "30"};
    
    char *query = url_build_query_string(keys, values, 3);
    printf("Query string: %s\n\n", query);
    free(query);
    
    /* Add params to URL */
    char *url = url_add_params("https://api.example.com/users", keys, values, 3);
    printf("Full URL: %s\n\n", url);
    free(url);
}

/* ============================================================================
 * Example 5: HTTP GET Request
 * ============================================================================ */
static void example_http_get(void) {
    printf("\n========================================\n");
    printf("Example 5: HTTP GET Request\n");
    printf("========================================\n\n");
    
    printf("Fetching data from httpbin.org...\n\n");
    
    HttpResponse *response = http_get("https://httpbin.org/get", NULL);
    print_response(response);
    http_response_free(response);
}

/* ============================================================================
 * Example 6: HTTP POST with JSON
 * ============================================================================ */
static void example_http_post_json(void) {
    printf("\n========================================\n");
    printf("Example 6: HTTP POST with JSON\n");
    printf("========================================\n\n");
    
    const char *json_data = "{\"name\":\"John\",\"age\":30,\"city\":\"New York\"}";
    
    printf("Sending JSON: %s\n\n", json_data);
    
    HttpResponse *response = http_post_json("https://httpbin.org/post", json_data, NULL);
    print_response(response);
    http_response_free(response);
}

/* ============================================================================
 * Example 7: HTTP POST with Form Data
 * ============================================================================ */
static void example_http_post_form(void) {
    printf("\n========================================\n");
    printf("Example 7: HTTP POST with Form Data\n");
    printf("========================================\n\n");
    
    const char *form_data = "username=admin&password=secret123";
    
    printf("Sending form data: %s\n\n", form_data);
    
    HttpResponse *response = http_post_form("https://httpbin.org/post", form_data, NULL);
    print_response(response);
    http_response_free(response);
}

/* ============================================================================
 * Example 8: Custom Headers
 * ============================================================================ */
static void example_custom_headers(void) {
    printf("\n========================================\n");
    printf("Example 8: Custom Headers\n");
    printf("========================================\n\n");
    
    HttpRequestOptions *options = http_options_new();
    options->headers = http_headers_new();
    http_headers_add(options->headers, "Authorization", "Bearer token123");
    http_headers_add(options->headers, "X-Custom-Header", "CustomValue");
    http_headers_add(options->headers, "Accept", "application/json");
    
    printf("Sending request with custom headers...\n\n");
    
    HttpResponse *response = http_get("https://httpbin.org/headers", options);
    print_response(response);
    
    http_response_free(response);
    http_options_free(options);
}

/* ============================================================================
 * Example 9: HTTP DELETE Request
 * ============================================================================ */
static void example_http_delete(void) {
    printf("\n========================================\n");
    printf("Example 9: HTTP DELETE Request\n");
    printf("========================================\n\n");
    
    printf("Sending DELETE request...\n\n");
    
    HttpResponse *response = http_delete("https://httpbin.org/delete", NULL);
    print_response(response);
    http_response_free(response);
}

/* ============================================================================
 * Example 10: URL Validation
 * ============================================================================ */
static void example_url_validation(void) {
    printf("\n========================================\n");
    printf("Example 10: URL Validation\n");
    printf("========================================\n\n");
    
    const char *urls[] = {
        "https://example.com",
        "http://localhost:8080/api",
        "not a url",
        "example.com",
        "https://user:pass@example.com/path?query=1#frag",
        NULL
    };
    
    for (int i = 0; urls[i]; i++) {
        bool valid = url_is_valid(urls[i]);
        printf("URL: %-40s -> %s\n", urls[i], valid ? "VALID" : "INVALID");
    }
    printf("\n");
}

/* ============================================================================
 * Example 11: Extract URL Components
 * ============================================================================ */
static void example_extract_components(void) {
    printf("\n========================================\n");
    printf("Example 11: Extract URL Components\n");
    printf("========================================\n\n");
    
    const char *url = "https://api.example.com/v1/users?page=1";
    
    char *domain = url_get_domain(url);
    char *path = url_get_path(url);
    
    printf("URL: %s\n", url);
    printf("Domain: %s\n", domain ? domain : "(null)");
    printf("Path: %s\n\n", path ? path : "(null)");
    
    free(domain);
    free(path);
}

/* ============================================================================
 * Main Function
 * ============================================================================ */
int main(void) {
    printf("\n");
    printf("╔══════════════════════════════════════════════════════════╗\n");
    printf("║     AllToolkit - HTTP Utils Example Program              ║\n");
    printf("║     Version: %s                                         ║\n", http_utils_version());
    printf("╚══════════════════════════════════════════════════════════╝\n");
    
    /* URL manipulation examples */
    example_url_parsing();
    example_url_building();
    example_url_encoding();
    example_query_string();
    example_url_validation();
    example_extract_components();
    
    /* HTTP request examples (require network) */
    printf("\n========================================\n");
    printf("HTTP Request Examples (Network Required)\n");
    printf("========================================\n");
    printf("Note: These examples require internet connectivity\n");
    printf("and use httpbin.org for testing.\n\n");
    
    example_http_get();
    example_http_post_json();
    example_http_post_form();
    example_custom_headers();
    example_http_delete();
    
    printf("\n========================================\n");
    printf("All examples completed!\n");
    printf("========================================\n\n");
    
    return 0;
}