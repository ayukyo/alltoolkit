/**
 * @file mod.c
 * @brief HTTP Client Utilities Implementation for C
 * @author AllToolkit
 * @version 1.0.0
 *
 * Implementation of HTTP client utilities using libcurl.
 */

#include "mod.h"
#include <curl/curl.h>
#include <ctype.h>

/* ============================================================================
 * Internal Structures
 * ============================================================================ */

typedef struct {
    char *data;
    size_t size;
    size_t capacity;
} MemoryBuffer;

typedef struct {
    HttpHeaders *headers;
    size_t count;
} HeaderCollector;

/* ============================================================================
 * Memory Management Helpers
 * ============================================================================ */

static char* strdup_safe(const char *str) {
    if (!str) return NULL;
    size_t len = strlen(str);
    char *copy = (char*)malloc(len + 1);
    if (copy) {
        memcpy(copy, str, len + 1);
    }
    return copy;
}

static void memory_buffer_init(MemoryBuffer *buf) {
    buf->data = NULL;
    buf->size = 0;
    buf->capacity = 0;
}

static void memory_buffer_free(MemoryBuffer *buf) {
    if (buf->data) {
        free(buf->data);
        buf->data = NULL;
    }
    buf->size = 0;
    buf->capacity = 0;
}

static int memory_buffer_append(MemoryBuffer *buf, const char *data, size_t len) {
    if (buf->size + len + 1 > buf->capacity) {
        size_t new_capacity = (buf->capacity == 0) ? 1024 : buf->capacity * 2;
        while (new_capacity < buf->size + len + 1) {
            new_capacity *= 2;
        }
        if (new_capacity > HTTP_UTILS_MAX_RESPONSE_SIZE) {
            return -1;  /* Response too large */
        }
        char *new_data = (char*)realloc(buf->data, new_capacity);
        if (!new_data) return -1;
        buf->data = new_data;
        buf->capacity = new_capacity;
    }
    memcpy(buf->data + buf->size, data, len);
    buf->size += len;
    buf->data[buf->size] = '\0';
    return 0;
}

/* ============================================================================
 * libcurl Callbacks
 * ============================================================================ */

static size_t write_callback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t total_size = size * nmemb;
    MemoryBuffer *buf = (MemoryBuffer*)userp;
    if (memory_buffer_append(buf, (const char*)contents, total_size) != 0) {
        return 0;  /* Signal error */
    }
    return total_size;
}

static size_t header_callback(char *buffer, size_t size, size_t nitems, void *userp) {
    size_t total_size = size * nitems;
    HeaderCollector *collector = (HeaderCollector*)userp;
    
    /* Skip HTTP status line and empty lines */
    if (total_size < 2) return total_size;
    
    /* Check if this is the status line (starts with HTTP/) */
    if (strncmp(buffer, "HTTP/", 5) == 0) {
        return total_size;
    }
    
    /* Parse header line */
    char *colon = strchr(buffer, ':');
    if (colon) {
        size_t key_len = colon - buffer;
        char *key = (char*)malloc(key_len + 1);
        if (!key) return total_size;
        
        memcpy(key, buffer, key_len);
        key[key_len] = '\0';
        
        /* Trim whitespace from key */
        while (key_len > 0 && isspace((unsigned char)key[key_len - 1])) {
            key[--key_len] = '\0';
        }
        
        /* Get value (after colon) */
        char *value = colon + 1;
        while (*value && isspace((unsigned char)*value)) value++;
        
        /* Trim trailing whitespace and newline from value */
        size_t value_len = strlen(value);
        while (value_len > 0 && (isspace((unsigned char)value[value_len - 1]) || 
                                  value[value_len - 1] == '\r' || 
                                  value[value_len - 1] == '\n')) {
            value[--value_len] = '\0';
        }
        
        /* Skip empty headers */
        if (key_len > 0 && value_len > 0) {
            http_headers_add(collector->headers, key, value);
        }
        
        free(key);
    }
    
    return total_size;
}

/* ============================================================================
 * HTTP Headers Implementation
 * ============================================================================ */

HttpHeaders* http_headers_new(void) {
    HttpHeaders *headers = (HttpHeaders*)calloc(1, sizeof(HttpHeaders));
    return headers;
}

void http_headers_add(HttpHeaders *headers, const char *key, const char *value) {
    if (!headers || !key || !value) return;
    
    HttpHeader *header = (HttpHeader*)malloc(sizeof(HttpHeader));
    if (!header) return;
    
    header->key = strdup_safe(key);
    header->value = strdup_safe(value);
    header->next = NULL;
    
    if (headers->last) {
        headers->last->next = header;
    } else {
        headers->first = header;
    }
    headers->last = header;
    headers->count++;
}

const char* http_headers_get(const HttpHeaders *headers, const char *key) {
    if (!headers || !key) return NULL;
    
    HttpHeader *current = headers->first;
    while (current) {
        if (strcasecmp(current->key, key) == 0) {
            return current->value;
        }
        current = current->next;
    }
    return NULL;
}

void http_headers_free(HttpHeaders *headers) {
    if (!headers) return;
    
    HttpHeader *current = headers->first;
    while (current) {
        HttpHeader *next = current->next;
        free(current->key);
        free(current->value);
        free(current);
        current = next;
    }
    free(headers);
}

/* ============================================================================
 * Request Options Implementation
 * ============================================================================ */

HttpRequestOptions* http_options_new(void) {
    HttpRequestOptions *options = (HttpRequestOptions*)calloc(1, sizeof(HttpRequestOptions));
    if (options) {
        options->timeout = HTTP_UTILS_DEFAULT_TIMEOUT;
        options->follow_redirects = true;
        options->max_redirects = 10;
        options->verify_ssl = true;
    }
    return options;
}

void http_options_free(HttpRequestOptions *options) {
    if (!options) return;
    
    if (options->headers) {
        http_headers_free(options->headers);
    }
    free(options->proxy);
    free(options->user_agent);
    free(options->auth_username);
    free(options->auth_password);
    free(options);
}

/* ============================================================================
 * Response Implementation
 * ============================================================================ */

void http_response_free(HttpResponse *response) {
    if (!response) return;
    
    free(response->status_text);
    if (response->headers) {
        http_headers_free(response->headers);
    }
    free(response->body);
    free(response->url);
    free(response);
}

const char* http_response_get_header(const HttpResponse *response, const char *key) {
    if (!response || !response->headers) return NULL;
    return http_headers_get(response->headers, key);
}

bool http_response_is_json(const HttpResponse *response) {
    if (!response || !response->body) return false;
    
    const char *content_type = http_response_get_header(response, "Content-Type");
    if (content_type) {
        if (strstr(content_type, "application/json") != NULL) {
            return true;
        }
    }
    
    /* Check if body starts with { or [ */
    const char *p = response->body;
    while (*p && isspace((unsigned char)*p)) p++;
    return (*p == '{' || *p == '[');
}

/* ============================================================================
 * Core HTTP Request Function
 * ============================================================================ */

static HttpResponse* perform_request(const char *url, const char *method,
                                     const char *body, const char *content_type,
                                     const HttpRequestOptions *options) {
    if (!url || !method) return NULL;
    
    HttpResponse *response = (HttpResponse*)calloc(1, sizeof(HttpResponse));
    if (!response) return NULL;
    
    response->headers = http_headers_new();
    if (!response->headers) {
        free(response);
        return NULL;
    }
    
    CURL *curl = curl_easy_init();
    if (!curl) {
        http_response_free(response);
        return NULL;
    }
    
    /* Set URL */
    curl_easy_setopt(curl, CURLOPT_URL, url);
    
    /* Set method */
    if (strcmp(method, "GET") == 0) {
        curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L);
    } else if (strcmp(method, "POST") == 0) {
        curl_easy_setopt(curl, CURLOPT_POST, 1L);
    } else if (strcmp(method, "PUT") == 0) {
        curl_easy_setopt(curl, CURLOPT_UPLOAD, 0L);
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "PUT");
    } else if (strcmp(method, "DELETE") == 0) {
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "DELETE");
    } else if (strcmp(method, "PATCH") == 0) {
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "PATCH");
    } else if (strcmp(method, "HEAD") == 0) {
        curl_easy_setopt(curl, CURLOPT_NOBODY, 1L);
    }
    
    /* Set request body */
    struct curl_slist *header_list = NULL;
    if (body && strlen(body) > 0) {
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, body);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, (long)strlen(body));
    }
    
    /* Set content type */
    if (content_type) {
        char content_type_header[HTTP_UTILS_MAX_HEADER_LENGTH];
        snprintf(content_type_header, sizeof(content_type_header),
                 "Content-Type: %s", content_type);
        header_list = curl_slist_append(header_list, content_type_header);
    }
    
    /* Set custom headers */
    if (options && options->headers) {
        HttpHeader *current = options->headers->first;
        while (current) {
            char header_line[HTTP_UTILS_MAX_HEADER_LENGTH];
            snprintf(header_line, sizeof(header_line), "%s: %s",
                     current->key, current->value);
            header_list = curl_slist_append(header_list, header_line);
            current = current->next;
        }
    }
    
    /* Set User-Agent */
    if (options && options->user_agent) {
        curl_easy_setopt(curl, CURLOPT_USERAGENT, options->user_agent);
    } else {
        curl_easy_setopt(curl, CURLOPT_USERAGENT, "AllToolkit-HTTP-Utils/" HTTP_UTILS_VERSION);
    }
    
    /* Set timeout */
    int timeout = (options && options->timeout > 0) ? options->timeout : HTTP_UTILS_DEFAULT_TIMEOUT;
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, (long)timeout);
    curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT, (long)timeout);
    
    /* Set redirect options */
    bool follow_redirects = (options) ? options->follow_redirects : true;
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, follow_redirects ? 1L : 0L);
    int max_redirects = (options && options->max_redirects > 0) ? options->max_redirects : 10;
    curl_easy_setopt(curl, CURLOPT_MAXREDIRS, (long)max_redirects);
    
    /* Set SSL verification */
    bool verify_ssl = (options) ? options->verify_ssl : true;
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, verify_ssl ? 1L : 0L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, verify_ssl ? 2L : 0L);
    
    /* Set proxy */
    if (options && options->proxy) {
        curl_easy_setopt(curl, CURLOPT_PROXY, options->proxy);
    }
    
    /* Set basic authentication */
    if (options && options->auth_username && options->auth_password) {
        char auth[512];
        snprintf(auth, sizeof(auth), "%s:%s", options->auth_username, options->auth_password);
        curl_easy_setopt(curl, CURLOPT_USERPWD, auth);
    }
    
    /* Set callbacks */
    MemoryBuffer response_buffer;
    memory_buffer_init(&response_buffer);
    
    HeaderCollector header_collector;
    header_collector.headers = response->headers;
    header_collector.count = 0;
    
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_buffer);
    curl_easy_setopt(curl, CURLOPT_HEADERFUNCTION, header_callback);
    curl_easy_setopt(curl, CURLOPT_HEADERDATA, &header_collector);
    
    /* Apply headers */
    if (header_list) {
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, header_list);
    }
    
    /* Perform request */
    clock_t start_time = clock();
    CURLcode res = curl_easy_perform(curl);
    clock_t end_time = clock();
    
    /* Calculate response time */
    response->response_time = ((double)(end_time - start_time)) / CLOCKS_PER_SEC;
    
    if (res == CURLE_OK) {
        /* Get response info */
        long status_code;
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &status_code);
        response->status_code = (int)status_code;
        response->success = (status_code >= 200 && status_code < 300);
        
        char *effective_url = NULL;
        curl_easy_getinfo(curl, CURLINFO_EFFECTIVE_URL, &effective_url);
        if (effective_url) {
            response->url = strdup_safe(effective_url);
        }
        
        /* Set status text */
        response->status_text = strdup_safe(http_status_text(response->status_code));
        
        /* Set response body */
        if (response_buffer.size > 0) {
            response->body = response_buffer.data;
            response->body_length = response_buffer.size;
            response_buffer.data = NULL;  /* Transfer ownership */
        }
    } else {
        /* Request failed */
        response->status_code = 0;
        response->success = false;
        response->status_text = strdup_safe(curl_easy_strerror(res));
    }
    
    /* Cleanup */
    if (header_list) {
        curl_slist_free_all(header_list);
    }
    curl_easy_cleanup(curl);
    memory_buffer_free(&response_buffer);
    
    return response;
}

/* ============================================================================
 * HTTP Method Implementations
 * ============================================================================ */

HttpResponse* http_get(const char *url, const HttpRequestOptions *options) {
    return perform_request(url, "GET", NULL, NULL, options);
}

HttpResponse* http_post(const char *url, const char *body, const char *content_type,
                        const HttpRequestOptions *options) {
    return perform_request(url, "POST", body, content_type, options);
}

HttpResponse* http_post_json(const char *url, const char *json_data,
                             const HttpRequestOptions *options) {
    return perform_request(url, "POST", json_data, "application/json", options);
}

HttpResponse* http_post_form(const char *url, const char *form_data,
                             const HttpRequestOptions *options) {
    return perform_request(url, "POST", form_data, "application/x-www-form-urlencoded", options);
}

HttpResponse* http_put(const char *url, const char *body, const char *content_type,
                       const HttpRequestOptions *options) {
    return perform_request(url, "PUT", body, content_type, options);
}

HttpResponse* http_put_json(const char *url, const char *json_data,
                            const HttpRequestOptions *options) {
    return perform_request(url, "PUT", json_data, "application/json", options);
}

HttpResponse* http_delete(const char *url, const HttpRequestOptions *options) {
    return perform_request(url, "DELETE", NULL, NULL, options);
}

HttpResponse* http_patch(const char *url, const char *body, const char *content_type,
                         const HttpRequestOptions *options) {
    return perform_request(url, "PATCH", body, content_type, options);
}

HttpResponse* http_head(const char *url, const HttpRequestOptions *options) {
    return perform_request(url, "HEAD", NULL, NULL, options);
}

/* ============================================================================
 * URL Utilities Implementation
 * ============================================================================ */

UrlComponents* url_parse(const char *url) {
    if (!url || !*url) return NULL;
    
    UrlComponents *components = (UrlComponents*)calloc(1, sizeof(UrlComponents));
    if (!components) return NULL;
    
    const char *ptr = url;
    const char *end = url + strlen(url);
    
    /* Parse scheme */
    const char *scheme_end = strstr(ptr, "://");
    if (scheme_end) {
        size_t scheme_len = scheme_end - ptr;
        components->scheme = (char*)malloc(scheme_len + 1);
        if (components->scheme) {
            memcpy(components->scheme, ptr, scheme_len);
            components->scheme[scheme_len] = '\0';
            /* Convert to lowercase */
            for (size_t i = 0; i < scheme_len; i++) {
                components->scheme[i] = tolower((unsigned char)components->scheme[i]);
            }
        }
        ptr = scheme_end + 3;
    }
    
    /* Parse userinfo */
    const char *at = strchr(ptr, '@');
    const char *slash = strchr(ptr, '/');
    if (at && (!slash || at < slash)) {
        size_t userinfo_len = at - ptr;
        components->userinfo = (char*)malloc(userinfo_len + 1);
        if (components->userinfo) {
            memcpy(components->userinfo, ptr, userinfo_len);
            components->userinfo[userinfo_len] = '\0';
        }
        ptr = at + 1;
    }
    
    /* Parse host and port */
    const char *host_end = slash ? slash : end;
    const char *colon = strchr(ptr, ':');
    if (colon && colon < host_end) {
        /* Port specified */
        size_t host_len = colon - ptr;
        components->host = (char*)malloc(host_len + 1);
        if (components->host) {
            memcpy(components->host, ptr, host_len);
            components->host[host_len] = '\0';
        }
        components->port = atoi(colon + 1);
    } else {
        size_t host_len = host_end - ptr;
        components->host = (char*)malloc(host_len + 1);
        if (components->host) {
            memcpy(components->host, ptr, host_len);
            components->host[host_len] = '\0';
        }
        /* Set default port */
        if (components->scheme) {
            if (strcmp(components->scheme, "http") == 0) {
                components->port = 80;
            } else if (strcmp(components->scheme, "https") == 0) {
                components->port = 443;
            }
        }
    }
    ptr = host_end;
    
    /* Parse path */
    if (ptr < end && *ptr == '/') {
        const char *query_start = strchr(ptr, '?');
        const char *fragment_start = strchr(ptr, '#');
        const char *path_end = end;
        
        if (query_start) path_end = query_start;
        if (fragment_start && fragment_start < path_end) path_end = fragment_start;
        
        size_t path_len = path_end - ptr;
        components->path = (char*)malloc(path_len + 1);
        if (components->path) {
            memcpy(components->path, ptr, path_len);
            components->path[path_len] = '\0';
        }
        ptr = path_end;
    } else {
        components->path = strdup_safe("/");
    }
    
    /* Parse query */
    if (ptr < end && *ptr == '?') {
        ptr++;
        const char *fragment_start = strchr(ptr, '#');
        const char *query_end = fragment_start ? fragment_start : end;
        
        size_t query_len = query_end - ptr;
        components->query = (char*)malloc(query_len + 1);
        if (components->query) {
            memcpy(components->query, ptr, query_len);
            components->query[query_len] = '\0';
        }
        ptr = query_end;
    }
    
    /* Parse fragment */
    if (ptr < end && *ptr == '#') {
        ptr++;
        size_t fragment_len = end - ptr;
        components->fragment = (char*)malloc(fragment_len + 1);
        if (components->fragment) {
            memcpy(components->fragment, ptr, fragment_len);
            components->fragment[fragment_len] = '\0';
        }
    }
    
    return components;
}

void url_components_free(UrlComponents *components) {
    if (!components) return;
    
    free(components->scheme);
    free(components->host);
    free(components->path);
    free(components->query);
    free(components->fragment);
    free(components->userinfo);
    free(components);
}

char* url_build(const UrlComponents *components) {
    if (!components) return NULL;
    
    size_t url_len = 0;
    if (components->scheme) url_len += strlen(components->scheme) + 3;  /* :// */
    if (components->userinfo) url_len += strlen(components->userinfo) + 1;  /* @ */
    if (components->host) url_len += strlen(components->host);
    if (components->port > 0 && components->port != 80 && components->port != 443) {
        url_len += 6;  /* :port */
    }
    if (components->path) url_len += strlen(components->path);
    if (components->query) url_len += strlen(components->query) + 1;  /* ? */
    if (components->fragment) url_len += strlen(components->fragment) + 1;  /* # */
    url_len += 1;  /* null terminator */
    
    char *url = (char*)malloc(url_len);
    if (!url) return NULL;
    
    url[0] = '\0';
    
    if (components->scheme) {
        strcat(url, components->scheme);
        strcat(url, "://");
    }
    if (components->userinfo) {
        strcat(url, components->userinfo);
        strcat(url, "@");
    }
    if (components->host) {
        strcat(url, components->host);
    }
    if (components->port > 0 && components->port != 80 && components->port != 443) {
        char port_str[8];
        snprintf(port_str, sizeof(port_str), ":%d", components->port);
        strcat(url, port_str);
    }
    if (components->path) {
        strcat(url, components->path);
    }
    if (components->query) {
        strcat(url, "?");
        strcat(url, components->query);
    }
    if (components->fragment) {
        strcat(url, "#");
        strcat(url, components->fragment);
    }
    
    return url;
}

static int is_url_safe_char(unsigned char c) {
    return isalnum(c) || c == '-' || c == '_' || c == '.' || c == '~';
}

char* url_encode(const char *str) {
    if (!str) return NULL;
    
    size_t len = strlen(str);
    size_t encoded_len = len * 3 + 1;
    char *encoded = (char*)malloc(encoded_len);
    if (!encoded) return NULL;
    
    size_t j = 0;
    for (size_t i = 0; i < len; i++) {
        unsigned char c = (unsigned char)str[i];
        if (is_url_safe_char(c)) {
            encoded[j++] = c;
        } else if (c == ' ') {
            encoded[j++] = '+';
        } else {
            snprintf(&encoded[j], 4, "%%%02X", c);
            j += 3;
        }
    }
    encoded[j] = '\0';
    
    return encoded;
}

char* url_decode(const char *str) {
    if (!str) return NULL;
    
    size_t len = strlen(str);
    char *decoded = (char*)malloc(len + 1);
    if (!decoded) return NULL;
    
    size_t j = 0;
    for (size_t i = 0; i < len; i++) {
        if (str[i] == '+' && (i == 0 || str[i-1] != '%')) {
            decoded[j++] = ' ';
        } else if (str[i] == '%' && i + 2 < len && 
                   isxdigit((unsigned char)str[i+1]) && 
                   isxdigit((unsigned char)str[i+2])) {
            char hex[3] = {str[i+1], str[i+2], '\0'};
            decoded[j++] = (char)strtol(hex, NULL, 16);
            i += 2;
        } else {
            decoded[j++] = str[i];
        }
    }
    decoded[j] = '\0';
    
    return decoded;
}

char* url_build_query_string(const char **keys, const char **values, size_t count) {
    if (!keys || !values || count == 0) return strdup_safe("");
    
    size_t total_len = 0;
    char **encoded_keys = (char**)malloc(count * sizeof(char*));
    char **encoded_values = (char**)malloc(count * sizeof(char*));
    if (!encoded_keys || !encoded_values) {
        free(encoded_keys);
        free(encoded_values);
        return NULL;
    }
    
    for (size_t i = 0; i < count; i++) {
        encoded_keys[i] = url_encode(keys[i]);
        encoded_values[i] = url_encode(values[i]);
        if (encoded_keys[i] && encoded_values[i]) {
            total_len += strlen(encoded_keys[i]) + strlen(encoded_values[i]) + 2;  /* = and & */
        }
    }
    
    char *query = (char*)malloc(total_len + 1);
    if (!query) {
        for (size_t i = 0; i < count; i++) {
            free(encoded_keys[i]);
            free(encoded_values[i]);
        }
        free(encoded_keys);
        free(encoded_values);
        return NULL;
    }
    
    query[0] = '\0';
    for (size_t i = 0; i < count; i++) {
        if (i > 0) strcat(query, "&");
        strcat(query, encoded_keys[i]);
        strcat(query, "=");
        strcat(query, encoded_values[i]);
    }
    
    for (size_t i = 0; i < count; i++) {
        free(encoded_keys[i]);
        free(encoded_values[i]);
    }
    free(encoded_keys);
    free(encoded_values);
    
    return query;
}

char* url_add_params(const char *base_url, const char **keys, const char **values, size_t count) {
    if (!base_url) return NULL;
    if (!keys || !values || count == 0) return strdup_safe(base_url);
    
    char *query = url_build_query_string(keys, values, count);
    if (!query) return NULL;
    
    size_t base_len = strlen(base_url);
    size_t query_len = strlen(query);
    size_t sep_len = (strchr(base_url, '?') != NULL) ? 1 : 1;  /* & or ? */
    
    char *url = (char*)malloc(base_len + sep_len + query_len + 1);
    if (!url) {
        free(query);
        return NULL;
    }
    
    strcpy(url, base_url);
    strcat(url, (strchr(base_url, '?') != NULL) ? "&" : "?");
    strcat(url, query);
    free(query);
    
    return url;
}

bool url_is_valid(const char *url) {
    if (!url || !*url) return false;
    
    /* Check for scheme */
    if (strstr(url, "://") == NULL) return false;
    
    /* Check for valid characters */
    const char *valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;=";
    for (size_t i = 0; url[i]; i++) {
        if (!strchr(valid_chars, url[i]) && (unsigned char)url[i] > 127) {
            return false;
        }
    }
    
    /* Try to parse */
    UrlComponents *components = url_parse(url);
    if (!components) return false;
    
    bool valid = (components->scheme != NULL && components->host != NULL);
    url_components_free(components);
    
    return valid;
}

char* url_get_domain(const char *url) {
    if (!url) return NULL;
    
    UrlComponents *components = url_parse(url);
    if (!components) return NULL;
    
    char *domain = strdup_safe(components->host);
    url_components_free(components);
    
    return domain;
}

char* url_get_path(const char *url) {
    if (!url) return NULL;
    
    UrlComponents *components = url_parse(url);
    if (!components) return NULL;
    
    char *path = strdup_safe(components->path);
    url_components_free(components);
    
    return path;
}

/* ============================================================================
 * Utility Functions
 * ============================================================================ */

const char* http_utils_version(void) {
    return HTTP_UTILS_VERSION;
}

const char* http_status_text(int status_code) {
    switch (status_code) {
        case 100: return "Continue";
        case 101: return "Switching Protocols";
        case 200: return "OK";
        case 201: return "Created";
        case 202: return "Accepted";
        case 204: return "No Content";
        case 301: return "Moved Permanently";
        case 302: return "Found";
        case 304: return "Not Modified";
        case 400: return "Bad Request";
        case 401: return "Unauthorized";
        case 403: return "Forbidden";
        case 404: return "Not Found";
        case 405: return "Method Not Allowed";
        case 500: return "Internal Server Error";
        case 502: return "Bad Gateway";
        case 503: return "Service Unavailable";
        default:
            if (status_code >= 200 && status_code < 300) return "Success";
            if (status_code >= 400 && status_code < 500) return "Client Error";
            if (status_code >= 500) return "Server Error";
            return "Unknown";
    }
}