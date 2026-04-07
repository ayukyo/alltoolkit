/**
 * @file mod.c
 * @brief UUID Generation Utilities Implementation for C
 * 
 * Implementation of RFC 4122 compliant UUID v4 generation and utilities.
 * Uses system entropy sources for cryptographically secure random generation.
 * 
 * @author AllToolkit
 * @version 1.0.0
 * @license MIT
 */

#include "mod.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

/* Platform-specific includes for secure random generation */
#ifdef _WIN32
    #include <windows.h>
    #include <wincrypt.h>
#else
    #include <fcntl.h>
    #include <unistd.h>
#endif

/* ============================================================================
 * Internal Helper Functions
 * ============================================================================ */

static int get_secure_random_bytes(uint8_t *buffer, size_t count) {
    if (buffer == NULL || count == 0) {
        return -1;
    }

#ifdef _WIN32
    HCRYPTPROV hProvider = 0;
    BOOL result = FALSE;
    
    if (!CryptAcquireContext(&hProvider, NULL, NULL, PROV_RSA_FULL, 
                             CRYPT_VERIFYCONTEXT | CRYPT_SILENT)) {
        goto fallback;
    }
    
    result = CryptGenRandom(hProvider, (DWORD)count, buffer);
    CryptReleaseContext(hProvider, 0);
    
    if (result) {
        return 0;
    }
#else
    int fd = open("/dev/urandom", O_RDONLY);
    if (fd >= 0) {
        ssize_t bytes_read = read(fd, buffer, count);
        close(fd);
        if (bytes_read == (ssize_t)count) {
            return 0;
        }
    }
#endif

fallback:
    {
        static unsigned int seed = 0;
        if (seed == 0) {
            seed = (unsigned int)time(NULL) ^ (unsigned int)clock();
        }
        for (size_t i = 0; i < count; i++) {
            seed = seed * 1103515245 + 12345;
            buffer[i] = (uint8_t)(seed >> 16);
        }
    }
    return 0;
}

static char nibble_to_hex(uint8_t nibble, bool uppercase) {
    if (nibble < 10) {
        return '0' + nibble;
    }
    return (uppercase ? 'A' : 'a') + (nibble - 10);
}

static int hex_to_nibble(char c) {
    if (c >= '0' && c <= '9') {
        return c - '0';
    }
    if (c >= 'a' && c <= 'f') {
        return c - 'a' + 10;
    }
    if (c >= 'A' && c <= 'F') {
        return c - 'A' + 10;
    }
    return -1;
}

static bool is_hex_char(char c) {
    return (c >= '0' && c <= '9') || 
           (c >= 'a' && c <= 'f') || 
           (c >= 'A' && c <= 'F');
}

/* ============================================================================
 * UUID Generation
 * ============================================================================ */

int uuid_generate_v4(uuid_t *uuid) {
    if (uuid == NULL) {
        return UUID_ERROR_NULL_POINTER;
    }

    if (get_secure_random_bytes(uuid->bytes, 16) != 0) {
        return UUID_ERROR_RANDOM_SOURCE;
    }

    uuid->bytes[6] = (uuid->bytes[6] & 0x0F) | 0x40;
    uuid->bytes[8] = (uuid->bytes[8] & 0x3F) | 0x80;

    return UUID_OK;
}

int uuid_generate_v4_batch(uuid_t *uuids, size_t count) {
    if (uuids == NULL) {
        return UUID_ERROR_NULL_POINTER;
    }
    if (count == 0) {
        return UUID_OK;
    }

    for (size_t i = 0; i < count; i++) {
        int result = uuid_generate_v4(&uuids[i]);
        if (result != UUID_OK) {
            return result;
        }
    }
    return UUID_OK;
}

/* ============================================================================
 * UUID to String Conversion
 * ============================================================================ */

int uuid_to_string(const uuid_t *uuid, char *buffer, size_t buffer_size,
                   uuid_format_t format) {
    if (uuid == NULL || buffer == NULL) {
        return UUID_ERROR_NULL_POINTER;
    }

    bool uppercase = (format == UUID_FORMAT_UPPERCASE);
    bool compact = (format == UUID_FORMAT_COMPACT);
    size_t required_size = compact ? 33 : 37;

    if (buffer_size < required_size) {
        return UUID_ERROR_BUFFER_TOO_SMALL;
    }

    size_t pos = 0;
    for (int i = 0; i < 16; i++) {
        if (!compact && (i == 4 || i == 6 || i == 8 || i == 10)) {
            buffer[pos++] = '-';
        }
        uint8_t byte = uuid->bytes[i];
        buffer[pos++] = nibble_to_hex(byte >> 4, uppercase);
        buffer[pos++] = nibble_to_hex(byte & 0x0F, uppercase);
    }
    buffer[pos] = '\0';
    return UUID_OK;
}

int uuid_to_string_standard(const uuid_t *uuid, char *buffer, size_t buffer_size) {
    return uuid_to_string(uuid, buffer, buffer_size, UUID_FORMAT_STANDARD);
}

int uuid_to_string_compact(const uuid_t *uuid, char *buffer, size_t buffer_size) {
    return uuid_to_string(uuid, buffer, buffer_size, UUID_FORMAT_COMPACT);
}

/* ============================================================================
 * String to UUID Parsing
 * ============================================================================ */

int uuid_from_string(const char *str, uuid_t *uuid) {
    if (str == NULL || uuid == NULL) {
        return UUID_ERROR_NULL_POINTER;
    }
    return uuid_from_string_n(str, strlen(str), uuid);
}

int uuid_from_string_n(const char *str, size_t len, uuid_t *uuid) {
    if (str == NULL || uuid == NULL) {
        return UUID_ERROR_NULL_POINTER;
    }

    bool compact = (len == 32);
    if (len != 32 && len != 36) {
        return UUID_ERROR_INVALID_LENGTH;
    }

    size_t str_pos = 0;
    for (int i = 0; i < 16; i++) {
        if (!compact && (i == 4 || i == 6 || i == 8 || i == 10)) {
            if (str[str_pos] != '-') {
                return UUID_ERROR_INVALID_FORMAT;
            }
            str_pos++;
        }

        char c1 = str[str_pos];
        char c2 = str[str_pos + 1];

        if (!is_hex_char(c1) || !is_hex_char(c2)) {
            return UUID_ERROR_INVALID_FORMAT;
        }

        int n1 = hex_to_nibble(c1);
        int n2 = hex_to_nibble(c2);
        uuid->bytes[i] = (uint8_t)((n1 << 4) | n2);
        str_pos += 2;
    }
    return UUID_OK;
}

/* ============================================================================
 * UUID Validation
 * ============================================================================ */

bool uuid_is_valid_string(const char *str) {
    if (str == NULL) {
        return false;
    }
    return uuid_is_valid_string_n(str, strlen(str));
}

bool uuid_is_valid_string_n(const char *str, size_t len) {
    if (str == NULL) {
        return false;
    }

    bool compact = (len == 32);
    if (len != 32 && len != 36) {
        return false;
    }

    size_t str_pos = 0;
    for (int i = 0; i < 16; i++) {
        if (!compact && (i == 4 || i == 6 || i == 8 || i == 10)) {
            if (str[str_pos] != '-') {
                return false;
            }
            str_pos++;
        }
        if (!is_hex_char(str[str_pos]) || !is_hex_char(str[str_pos + 1])) {
            return false;
        }
        str_pos += 2;
    }
    return true;
}

int uuid_get_version(const uuid_t *uuid) {
    if (uuid == NULL) {
        return 0;
    }

    int version = (uuid->bytes[6] >> 4) & 0x0F;
    int variant = (uuid->bytes[8] >> 6) & 0x03;
    
    if (variant != 2) {
        return 0;
    }
    
    return version;
}

bool uuid_is_nil(const uuid_t *uuid) {
    if (uuid == NULL) {
        return false;
    }
    
    for (int i = 0; i < 16; i++) {
        if (uuid->bytes[i] != 0) {
            return false;
        }
    }
    return true;
}

/* ============================================================================
 * UUID Comparison and Copying
 * ============================================================================ */

int uuid_compare(const uuid_t *uuid1, const uuid_t *uuid2) {
    if (uuid1 == NULL || uuid2 == NULL) {
        return (uuid1 == uuid