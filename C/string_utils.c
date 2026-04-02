/**
 * @file string_utils.c
 * @brief C语言通用字符串处理工具库实现
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-02
 */

#include "string_utils.h"
#include <string.h>
#include <ctype.h>

bool is_whitespace(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\v' || c == '\f';
}

char* str_trim_left(char* str) {
    if (str == NULL || *str == '\0') {
        return str;
    }
    
    char* start = str;
    while (is_whitespace(*start)) {
        start++;
    }
    
    if (start != str) {
        memmove(str, start, strlen(start) + 1);
    }
    
    return str;
}

char* str_trim_right(char* str) {
    if (str == NULL || *str == '\0') {
        return str;
    }
    
    size_t len = strlen(str);
    while (len > 0 && is_whitespace(str[len - 1])) {
        len--;
    }
    str[len] = '\0';
    
    return str;
}

char* str_trim(char* str) {
    str_trim_left(str);
    str_trim_right(str);
    return str;
}

char* str_to_lower(char* str) {
    if (str == NULL) {
        return NULL;
    }
    
    for (char* p = str; *p != '\0'; p++) {
        *p = (char)tolower((unsigned char)*p);
    }
    
    return str;
}

char* str_to_upper(char* str) {
    if (str == NULL) {
        return NULL;
    }
    
    for (char* p = str; *p != '\0'; p++) {
        *p = (char)toupper((unsigned char)*p);
    }
    
    return str;
}

char* str_reverse(char* str) {
    if (str == NULL || *str == '\0') {
        return str;
    }
    
    size_t len = strlen(str);
    size_t i = 0;
    size_t j = len - 1;
    
    while (i < j) {
        char temp = str[i];
        str[i] = str[j];
        str[j] = temp;
        i++;
        j--;
    }
    
    return str;
}

bool str_starts_with(const char* str, const char* prefix) {
    if (str == NULL || prefix == NULL) {
        return false;
    }
    
    size_t str_len = strlen(str);
    size_t prefix_len = strlen(prefix);
    
    if (prefix_len > str_len) {
        return false;
    }
    
    return strncmp(str, prefix, prefix_len) == 0;
}

bool str_ends_with(const char* str, const char* suffix) {
    if (str == NULL || suffix == NULL) {
        return false;
    }
    
    size_t str_len = strlen(str);
    size_t suffix_len = strlen(suffix);
    
    if (suffix_len > str_len) {
        return false;
    }
    
    return strcmp(str + str_len - suffix_len, suffix) == 0;
}

size_t str_count(const char* str, const char* substr) {
    if (str == NULL || substr == NULL || *substr == '\0') {
        return 0;
    }
    
    size_t count = 0;
    size_t substr_len = strlen(substr);
    const char* pos = str;
    
    while ((pos = strstr(pos, substr)) != NULL) {
        count++;
        pos += substr_len;
    }
    
    return count;
}

size_t str_copy_safe(char* dest, const char* src, size_t max_len) {
    if (dest == NULL || src == NULL || max_len == 0) {
        return 0;
    }
    
    size_t i;
    for (i = 0; i < max_len - 1 && src[i] != '\0'; i++) {
        dest[i] = src[i];
    }
    dest[i] = '\0';
    
    return i;
}
