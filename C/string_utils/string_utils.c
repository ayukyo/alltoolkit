/**
 * @file string_utils.c
 * @brief C 语言字符串工具库实现
 */

#include "string_utils.h"
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

bool str_is_whitespace(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\f' || c == '\v';
}

static char* str_duplicate(const char* str) {
    if (!str) return NULL;
    size_t len = strlen(str);
    char* copy = (char*)malloc(len + 1);
    if (copy) memcpy(copy, str, len + 1);
    return copy;
}

char* str_trim_left(char* str) {
    if (!str) return NULL;
    while (*str && str_is_whitespace(*str)) str++;
    return str;
}

char* str_trim_right(char* str) {
    if (!str) return NULL;
    size_t len = strlen(str);
    while (len > 0 && str_is_whitespace(str[len - 1])) str[--len] = '\0';
    return str;
}

char* str_trim(char* str) {
    if (!str) return NULL;
    str = str_trim_left(str);
    str_trim_right(str);
    return str;
}

char* str_trim_chars(char* str, const char* chars) {
    if (!str || !chars) return str;
    char* start = str;
    while (*start && strchr(chars, *start)) start++;
    size_t len = strlen(start);
    while (len > 0 && strchr(chars, start[len - 1])) start[--len] = '\0';
    if (start != str) memmove(str, start, len + 1);
    return str;
}

StringSplitResult str_split(const char* str, const char* delimiter, size_t max_splits) {
    StringSplitResult result = {NULL, 0, 0};
    if (!str || !delimiter || *delimiter == '\0') return result;
    size_t delim_len = strlen(delimiter), token_count = 1;
    const char* pos = str;
    while ((pos = strstr(pos, delimiter)) != NULL) {
        if (max_splits > 0 && token_count >= max_splits + 1) break;
        token_count++;
        pos += delim_len;
    }
    result.tokens = (char**)malloc(token_count * sizeof(char*));
    if (!result.tokens) return result;
    result.capacity = token_count;
    const char* start = str;
    size_t i = 0;
    const char* end;
    while ((end = strstr(start, delimiter)) != NULL && i < token_count - 1) {
        size_t token_len = end - start;
        result.tokens[i] = (char*)malloc(token_len + 1);
        if (result.tokens[i]) { memcpy(result.tokens[i], start, token_len); result.tokens[i][token_len] = '\0'; }
        i++;
        start = end + delim_len;
    }
    result.tokens[i] = str_duplicate(start);
    result.count = i + 1;
    return result;
}

StringSplitResult str_split_char(const char* str, char delimiter, size_t max_splits) {
    char delim_str[2] = {delimiter, '\0'};
    return str_split(str, delim_str, max_splits);
}

void str_split_free(StringSplitResult* result) {
    if (!result) return;
    if (result->tokens) {
        for (size_t i = 0; i < result->count; i++) free(result->tokens[i]);
        free(result->tokens);
        result->tokens = NULL;
    }
    result->count = 0;
    result->capacity = 0;
}

char* str_replace(const char* str, const char* old_sub, const char* new_sub) {
    return str_replace_n(str, old_sub, new_sub, 0);
}

char* str_replace_first(const char* str, const char* old_sub, const char* new_sub) {
    return str_replace_n(str, old_sub, new_sub, 1);
}

char* str_replace_n(const char* str, const char* old_sub, const char* new_sub, size_t n) {
    if (!str || !old_sub || !new_sub) return NULL;
    if (*old_sub == '\0') return str_duplicate(str);
    size_t old_len = strlen(old_sub), new_len = strlen(new_sub), str_len = strlen(str);
    size_t count = 0;
    const char* tmp = str;
    while ((tmp = strstr(tmp, old_sub)) != NULL) { if (n > 0 && count >= n) break; count++; tmp += old_len; }
    if (count == 0) return str_duplicate(str);
    size_t result_len = str_len + count * (new_len - old_len);
    char* result = (char*)malloc(result_len + 1);
    if (!result) return NULL;
    char* dst = result;
    const char* src = str;
    size_t replaced = 0;
    while (*src && (n == 0 || replaced < n)) {
        const char* pos = strstr(src, old_sub);
        if (!pos) break;
        size_t prefix_len = pos - src;
        memcpy(dst, src, prefix_len); dst += prefix_len;
        memcpy(dst, new_sub, new_len); dst += new_len;
        src = pos + old_len;
        replaced++;
    }
    strcpy(dst, src);
    return result;
}

size_t str_count(const char* str, const char* sub) {
    if (!str || !sub || *sub == '\0') return 0;
    size_t count = 0, sub_len = strlen(sub);
    const char* pos = str;
    while ((pos = strstr(pos, sub)) != NULL) { count++; pos += sub_len; }
    return count;
}

bool str_starts_with(const char* str, const char* prefix) {
    if (!str || !prefix) return false;
    return strncmp(str, prefix, strlen(prefix)) == 0;
}

bool str_ends_with(const char* str, const char* suffix) {
    if (!str || !suffix) return false;
    size_t str_len = strlen(str), suffix_len = strlen(suffix);
    if (suffix_len > str_len) return false;
    return strcmp(str + str_len - suffix_len, suffix) == 0;
}

char* str_to_upper(char* str) {
    if (!str) return NULL;
    for (char* p = str; *p; p++) *p = (char)toupper((unsigned char)*p);
    return str;
}

char* str_to_lower(char* str) {
    if (!str) return NULL;
    for (char* p = str; *p; p++) *p = (char)tolower((unsigned char)*p);
    return str;
}

char* str_to_upper_copy(const char* str) {
    if (!str) return NULL;
    char* copy = str_duplicate(str);
    if (copy) str_to_upper(copy);
    return copy;
}

char* str_to_lower_copy(const char* str) {
    if (!str) return NULL;
    char* copy = str_duplicate(str);
    if (copy) str_to_lower(copy);
    return copy;
}

size_t str_copy_safe(char* dest, const char* src, size_t dest_size) {
    if (!dest || !src || dest_size == 0) return 0;
    size_t i;
    for (i = 0; i < dest_size - 1 && src[i]; i++) dest[i] = src[i];
    dest[i] = '\0';
    return i;
}

size_t str_concat_safe(char* dest, const char* src, size_t dest_size) {
    if (!dest || !src || dest_size == 0) return 0;
    size_t dest_len = strlen(dest);
    if (dest_len >= dest_size - 1) return dest_len;
    size_t i;
    for (i = 0; dest_len + i < dest_size - 1 && src[i]; i++) dest[dest_len + i] = src[i];
    dest[dest_len + i] = '\0';
    return dest_len + i;
}

char* str_repeat(const char* str, size_t n) {
    if (!str) return NULL;
    if (n == 0) return str_duplicate("");
    size_t str_len = strlen(str), result_len = str_len * n;
    char* result = (char*)malloc(result_len + 1);
    if (!result) return NULL;
    for (size_t i = 0; i < n; i++) memcpy(result + i * str_len, str, str_len);
    result[result_len] = '\0';
    return result;
}

char* str_join_array(const char** strings, size_t count, const char* separator) {
    if (!strings || count == 0) return str_duplicate("");
    size_t sep_len = separator ? strlen(separator) : 0, total_len = 0;
    for (size_t i = 0; i < count; i++) total_len += strings[i] ? strlen(strings[i]) : 0;
    total_len += sep_len * (count - 1);
    char* result = (char*)malloc(total_len + 1);
    if (!result) return NULL;
    result[0] = '\0';
    for (size_t i = 0; i < count; i++) {
        if (i > 0 && separator) strcat(result, separator);
        if (strings[i]) strcat(result, strings[i]);
    }
    return result;
}

bool str_is_blank(const char* str) {
    if (!str) return true;
    while (*str) { if (!str_is_whitespace(*str)) return false; str++; }
    return true;
}

bool str_is_numeric(const char* str) {
    if (!str || *str == '\0') return false;
    while (*str) { if (!isdigit((unsigned char)*str)) return false; str++; }
    return true;
}

bool str_is_integer(const char* str) {
    if (!str || *str == '\0') return false;
    if (*str == '-' || *str == '+') str++;
    if (*str == '\0') return false;
    return str_is_numeric(str);
}

bool str_is_float(const char* str) {
    if (!str || *str == '\0') return false;
    if (*str == '-' || *str == '+') str++;
    int dot_count = 0;
    int digit_count = 0;
    while (*str) {
        if (*str == '.') {
            dot_count++;
            if (dot_count > 1) return false;
        } else if (isdigit((unsigned char)*str)) {
            digit_count++;
        } else {
            return false;
        }
        str++;
    }
    return digit_count > 0;
}

bool str_is_alpha(const char* str) {
    if (!str || *str == '\0') return false;
    while (*str) { if (!isalpha((unsigned char)*str)) return false; str++; }
    return true;
}

bool str_is_alphanumeric(const char* str) {
    if (!str || *str == '\0') return false;
    while (*str) { if (!isalnum((unsigned char)*str)) return false; str++; }
    return true;
}

char* str_substring(const char* str, size_t start, size_t length) {
    if (!str) return NULL;
    size_t str_len = strlen(str);
    if (start >= str_len) return str_duplicate("");
    if (start + length > str_len) length = str_len - start;
    char* result = (char*)malloc(length + 1);
    if (!result) return NULL;
    memcpy(result, str + start, length);
    result[length] = '\0';
    return result;
}

char* str_left(const char* str, size_t n) {
    return str_substring(str, 0, n);
}

char* str_right(const char* str, size_t n) {
    if (!str) return NULL;
    size_t str_len = strlen(str);
    if (n > str_len) n = str_len;
    return str_substring(str, str_len - n, n);
}

char* str_drop_left(const char* str, size_t n) {
    if (!str) return NULL;
    size_t str_len = strlen(str);
    if (n >= str_len) return str_duplicate("");
    return str_substring(str, n, str_len - n);
}

char* str_drop_right(const char* str, size_t n) {
    if (!str) return NULL;
    size_t str_len = strlen(str);
    if (n >= str_len) return str_duplicate("");
    return str_substring(str, 0, str_len - n);
}

char* str_remove_whitespace(char* str) {
    if (!str) return NULL;
    char* src = str;
    char* dst = str;
    while (*src) {
        if (!str_is_whitespace(*src)) *dst++ = *src;
        src++;
    }
    *dst = '\0';
    return str;
}

char* str_remove_chars(char* str, const char* chars) {
    if (!str || !chars) return str;
    char* src = str;
    char* dst = str;
    while (*src) {
        if (!strchr(chars, *src)) *dst++ = *src;
        src++;
    }
    *dst = '\0';
    return str;
}

char* str_normalize_whitespace(char* str) {
    if (!str) return NULL;
    char* src = str;
    char* dst = str;
    int last_was_space = 0;
    while (*src) {
        if (str_is_whitespace(*src)) {
            if (!last_was_space) {
                *dst++ = ' ';
                last_was_space = 1;
            }
        } else {
            *dst++ = *src;
            last_was_space = 0;
        }
        src++;
    }
    *dst = '\0';
    str_trim_right(str);
    return str;
}