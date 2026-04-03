/**
 * @file mod.h
 * @brief HTTP Client Utilities for C
 * @author AllToolkit
 * @version 1.0.0
 *
 * A zero-dependency HTTP client library using only standard C library.
 * Supports HTTP/HTTPS GET, POST, PUT, DELETE, HEAD methods.
 * Requires libcurl for actual network operations.
 */

#ifndef ALLTOOLKIT_HTTP_UTILS_H
#define ALLTOOLKIT_HTTP_UTILS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ============================================================================
 * Constants
 * ============================================================================ */

#define HTTP_UTILS_VERSION "1.0.0"
#define HTTP_UTILS_MAX_URL_LENGTH 2048
#define HTTP_UTILS_MAX_HEADER_LENGTH 4096
#define HTTP_UTILS_DEFAULT_TIMEOUT 30
#define HTTP_UTILS_MAX_RESPONSE_SIZE (10 * 1024 * 1024)  /* 10MB max response */

/* HTTP Status Codes */
#define HTTP_STATUS_OK 200
#define HTTP_STATUS_CREATED 201
#define HTTP_STATUS_NO_CONTENT 204
#define HTTP_STATUS_BAD_REQUEST 400
#define HTTP_STATUS_UNAUTHORIZED 401
#define HTTP_STATUS_FORBIDDEN 403
#define HTTP_STATUS_NOT_FOUND 404
#define HTTP_STATUS_INTERNAL_ERROR 500
#define HTTP_STATUS_SERVICE_UNAVAILABLE 503

/* ============================================================================
 * Data Structures
 * ============================================================================ */

/**
 * @struct HttpHeader
 * @brief Single HTTP header key-value pair
 */
typedef struct HttpHeader {
    char *key;
    char *value;
    struct HttpHeader *next;
} HttpHeader;

/**
 * @struct HttpHeaders
 * @brief Collection of HTTP headers
 */
typedef struct HttpHeaders {
    HttpHeader *first;
    HttpHeader *last;
    size_t count;
} HttpHeaders;

/**
 * @struct HttpResponse
 * @brief HTTP response data structure
 */
typedef struct HttpResponse {
    int status_code;           /**< HTTP status code (e.g., 200, 404) */
    char *status_text;         /**< HTTP status text (e.g., "OK", "Not Found") */
    HttpHeaders *headers;      /**< Response headers */
    char *body;                /**< Response body (may be NULL if no body) */
    size_t body_length;        /**< Length of response body in bytes */
    double response_time;      /**< Response time in seconds */
    char *url;                 /**< Final URL after redirects */
    bool success;              /**< true if status_code is 200-299 */
} HttpResponse;

/**
 * @struct HttpRequestOptions
 * @brief Options for HTTP requests
 */
typedef struct HttpRequestOptions {
    HttpHeaders *headers;      /**< Custom request headers */
    int timeout;               /**< Request timeout in seconds (default: 30) */
    bool follow_redirects;     /**< Follow redirects (default: true) */
    int max_redirects;         /**< Maximum redirect hops (default: 10) */
    bool verify_ssl;           /**< Verify SSL certificates (default: true) */
    char *proxy;               /**< Proxy URL (e.g., "http://proxy:8080") */
    char *user_agent;          /**< Custom User-Agent string */
    char *auth_username;       /**< Username for basic authentication */
    char *auth_password;       /**< Password for basic authentication */
} HttpRequestOptions;

/**
 * @struct UrlComponents
 * @brief Parsed URL components
 */
typedef struct UrlComponents {
    char *scheme;              /**< Protocol scheme (http/https) */
    char *host;                /**< Hostname or IP address */
    int port;                  /**< Port number (0 for default) */
    char *path;                /**< URL path */
    char *query;               /**< Query string */
    char *fragment;            /**< Fragment identifier */
    char *userinfo;            /**< User info (username:password) */
} UrlComponents;

/* ============================================================================
 * HTTP Methods
 * ============================================================================ */

/**
 * @brief Send HTTP GET request
 * @param url The URL to request
 * @param options Request options (can be NULL for defaults)
 * @return HttpResponse* Response object (must be freed with http_response_free)
 */
HttpResponse* http_get(const char *url, const HttpRequestOptions *options);

/**
 * @brief Send HTTP POST request
 * @param url The URL to request
 * @param body Request body (can be NULL)
 * @param content_type Content-Type header (e.g., "application/json")
 * @param options Request options (can be NULL for defaults)
 * @return HttpResponse* Response object
 */
HttpResponse* http_post(const char *url, const char *body, const char *content_type,
                        const HttpRequestOptions *options);

/**
 * @brief Send HTTP POST request with JSON data
 * @param url The URL to request
 * @param json_data JSON string to send
 * @param options Request options (can be NULL for defaults)
 * @return HttpResponse* Response object
 */
HttpResponse* http_post_json(const char *url, const char *json_data,
                             const HttpRequestOptions *options);

/**
 * @brief Send HTTP POST request with form data
 * @param url The URL to request
 * @param form_data Form data string (e.g., "key1=value1&key2=value2")
 * @param options Request options (can be NULL for defaults)
 * @return HttpResponse* Response object
 */
HttpResponse* http_post_form(const char *url, const char *form_data,
                             const HttpRequestOptions *options);

/**
 * @brief Send HTTP PUT request
 * @param url The URL to request
 * @param body Request body (can be NULL)
 * @param content_type Content-Type header
 * @param options Request options (can be NULL for defaults)
 * @return HttpResponse* Response object
 */
HttpResponse* http_put(const char *url, const char *body, const char *content_type,
                       const HttpRequestOptions *options);

/**
 * @brief Send HTTP PUT request with JSON data
 * @param url The URL to request
 * @param json_data JSON string to send
 * @param options Request options (can be NULL for defaults)
 * @return HttpResponse* Response object
 */
HttpResponse* http_put_json(const char *url, const char *json_data,
                            const HttpRequestOptions *options);

/**
 * @brief Send HTTP DELETE request
 * @param url The URL to request
 * @param options Request options (can be NULL for defaults)
 * @return HttpResponse* Response object
 */
HttpResponse* http_delete(const char *url, const HttpRequestOptions *options);

/**
 * @brief Send HTTP PATCH request
 * @param url The URL to request
 * @param body Request body (can be NULL)
 * @param content_type Content-Type header
 * @param options Request options (can be NULL for defaults)
 * @return HttpResponse* Response object
 */
HttpResponse* http_patch(const char *url, const char *body, const char *content_type,
                         const HttpRequestOptions *options);

/**
 * @brief Send HTTP HEAD request
 * @param url The URL to request
 * @param options Request options (can be NULL for defaults)
 * @return HttpResponse* Response object (body will be empty)
 */
HttpResponse* http_head(const char *url, const HttpRequestOptions *options);

/* ============================================================================
 * URL Utilities
 * ============================================================================ */

/**
 * @brief Parse URL into components
 * @param url The URL to parse
 * @return UrlComponents* Parsed components (must be freed with url_components_free)
 */
UrlComponents* url_parse(const char *url);

/**
 * @brief Free URL components
 * @param components Components to free
 */
void url_components_free(UrlComponents *components);

/**
 * @brief Build URL from components
 * @param components URL components
 * @return char* Complete URL string (must be freed)
 */
char* url_build(const UrlComponents *components);

/**
 * @brief URL encode a string
 * @param str String to encode
 * @return char* URL-encoded string (must be freed)
 */
char* url_encode(const char *str);

/**
 * @brief URL decode a string
 * @param str URL-encoded string
 * @return char* Decoded string (must be freed)
 */
char* url_decode(const char *str);

/**
 * @brief Build query string from key-value pairs
 * @param keys Array of keys
 * @param values Array of values
 * @param count Number of key-value pairs
 * @return char* Query string (must be freed)
 */
char* url_build_query_string(const char **keys, const char **values, size_t count);

/**
 * @brief Add query parameters to URL
 * @param base_url Base URL
 * @param keys Array of parameter keys
 * @param values Array of parameter values
 * @param count Number of parameters
 * @return char* URL with query parameters (must be freed)
 */
char* url_add_params(const char *base_url, const char **keys, const char **values, size_t count);

/**
 * @brief Validate URL format
 * @param url URL to validate
 * @return bool true if valid URL
 */
bool url_is_valid(const char *url);

/**
 * @brief Extract domain from URL
 * @param url URL string
 * @return char* Domain (must be freed) or NULL on error
 */
char* url_get_domain(const char *url);

/**
 * @brief Extract path from URL
 * @param url URL string
 * @return char* Path (must be freed) or NULL on error
 */
char* url_get_path(const char *url);

/* ============================================================================
 * Header Utilities
 * ============================================================================ */

/**
 * @brief Create new headers collection
 * @return HttpHeaders* New headers object
 */
HttpHeaders* http_headers_new(void);

/**
 * @brief Add header to collection
 * @param headers Headers collection
 * @param key Header name
 * @param value Header value
 */
void http_headers_add(HttpHeaders *headers, const char *key, const char *value);

/**
 * @brief Get header value by key
 * @param headers Headers collection
 * @param key Header name
 * @return const char* Header value or NULL if not found
 */
const char* http_headers_get(const HttpHeaders *headers, const char *key);

/**
 * @brief Free headers collection
 * @param headers Headers to free
 */
void http_headers_free(HttpHeaders *headers);

/* ============================================================================
 * Request Options
 * ============================================================================ */

/**
 * @brief Create default request options
 * @return HttpRequestOptions* Options with default values
 */
HttpRequestOptions* http_options_new(void);

/**
 * @brief Free request options
 * @param options Options to free
 */
void http_options_free(HttpRequestOptions *options);

/* ============================================================================
 * Response Utilities
 * ============================================================================ */

/**
 * @brief Free HTTP response
 * @param response Response to free
 */
void http_response_free(HttpResponse *response);

/**
 * @brief Get response header value
 * @param response HTTP response
 * @param key Header name
 * @return const char* Header value or NULL if not found
 */
const char* http_response_get_header(const HttpResponse *response, const char *key);

/**
 * @brief Check if response body is valid JSON
 * @param response HTTP response
 * @return bool true if body appears to be JSON
 */
bool http_response_is_json(const HttpResponse *response);

/* ============================================================================
 * Utility Functions
 * ============================================================================ */

/**
 * @brief Get library version
 * @return const char* Version string
 */
const char* http_utils_version(void);

/**
 * @brief Get HTTP status text from status code
 * @param status_code HTTP status code
 * @return const char* Status text (e.g., "OK", "Not Found")
 */
const char* http_status_text(int status_code);

#ifdef __cplusplus
}
#endif

#endif /* ALLTOOLKIT_HTTP_UTILS_H */