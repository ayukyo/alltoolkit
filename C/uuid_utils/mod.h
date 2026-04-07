/**
 * @file mod.h
 * @brief UUID Generation Utilities for C
 * 
 * A comprehensive UUID (Universally Unique Identifier) generation utility module
 * for C providing RFC 4122 compliant UUID v4 generation, validation, and format
 * conversion with zero external dependencies.
 * 
 * Features:
 * - UUID v4 generation (random-based) per RFC 4122
 * - UUID validation and format checking
 * - Format conversion (standard, compact, uppercase)
 * - UUID parsing from strings
 * - UUID comparison and copying
 * - Secure random generation using system entropy sources
 * 
 * @author AllToolkit
 * @version 1.0.0
 * @license MIT
 */

#ifndef UUID_UTILS_MOD_H
#define UUID_UTILS_MOD_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief UUID structure representing a 128-bit UUID
 * 
 * Stores UUID in network byte order (big-endian) as 16 bytes.
 * Layout follows RFC 4122:
 * - time_low (4 bytes)
 * - time_mid (2 bytes)
 * - time_hi_and_version (2 bytes)
 * - clock_seq_hi_and_res (1 byte)
 * - clock_seq_low (1 byte)
 * - node (6 bytes)
 */
typedef struct {
    uint8_t bytes[16];  /**< 16-byte UUID storage */
} uuid_t;

/**
 * @brief UUID version enumeration
 */
typedef enum {
    UUID_VERSION_1 = 1,  /**< Time-based UUID */
    UUID_VERSION_3 = 3,  /**< Name-based MD5 UUID */
    UUID_VERSION_4 = 4,  /**< Random UUID (supported) */
    UUID_VERSION_5 = 5,  /**< Name-based SHA1 UUID */
    UUID_VERSION_UNKNOWN = 0
} uuid_version_t;

/**
 * @brief UUID format enumeration
 */
typedef enum {
    UUID_FORMAT_STANDARD,   /**< xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx */
    UUID_FORMAT_COMPACT,    /**< xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx */
    UUID_FORMAT_UPPERCASE   /**< XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX */
} uuid_format_t;

/**
 * @brief Error codes for UUID operations
 */
typedef enum {
    UUID_OK = 0,                    /**< Success */
    UUID_ERROR_INVALID_FORMAT = -1, /**< Invalid UUID format */
    UUID_ERROR_NULL_POINTER = -2,   /**< Null pointer provided */
    UUID_ERROR_BUFFER_TOO_SMALL = -3, /**< Buffer too small */
    UUID_ERROR_RANDOM_SOURCE = -4,  /**< Failed to get random data */
    UUID_ERROR_INVALID_LENGTH = -5  /**< Invalid string length */
} uuid_error_t;

/* ============================================================================
 * UUID Generation
 * ============================================================================ */

/**
 * @brief Generate a new UUID v4 (random-based)
 * 
 * Generates a cryptographically secure random UUID version 4.
 * Uses system entropy sources (/dev/urandom on Unix, CryptGenRandom on Windows).
 * 
 * @param[out] uuid Pointer to uuid_t to store the generated UUID
 * @return UUID_OK on success, error code on failure
 * 
 * @code
 * uuid_t uuid;
 * if (uuid_generate_v4(&uuid) == UUID_OK) {
 *     // Use UUID
 * }
 * @endcode
 */
int uuid_generate_v4(uuid_t *uuid);

/**
 * @brief Generate multiple UUIDs v4 in batch
 * 
 * Efficiently generates multiple UUIDs. Uses a single entropy read when possible.
 * 
 * @param[out] uuids Array of uuid_t to store generated UUIDs
 * @param count Number of UUIDs to generate
 * @return UUID_OK on success, error code on failure
 */
int uuid_generate_v4_batch(uuid_t *uuids, size_t count);

/* ============================================================================
 * UUID to String Conversion
 * ============================================================================ */

/**
 * @brief Convert UUID to string representation
 * 
 * Converts a UUID structure to its string representation.
 * Output buffer must be at least 37 bytes for standard format (36 chars + null).
 * For compact format, buffer must be at least 33 bytes.
 * 
 * @param[in] uuid Pointer to uuid_t to convert
 * @param[out] buffer Output buffer for string representation
 * @param[in] buffer_size Size of output buffer
 * @param[in] format Output format (STANDARD, COMPACT, or UPPERCASE)
 * @return UUID_OK on success, error code on failure
 * 
 * @code
 * uuid_t uuid;
 * char str[37];
 * uuid_generate_v4(&uuid);
 * uuid_to_string(&uuid, str, sizeof(str), UUID_FORMAT_STANDARD);
 * // str now contains "550e8400-e29b-41d4-a716-446655440000"
 * @endcode
 */
int uuid_to_string(const uuid_t *uuid, char *buffer, size_t buffer_size, 
                   uuid_format_t format);

/**
 * @brief Convert UUID to standard format string (convenience function)
 * 
 * @param[in] uuid Pointer to uuid_t to convert
 * @param[out] buffer Output buffer (must be at least 37 bytes)
 * @param[in] buffer_size Size of output buffer
 * @return UUID_OK on success, error code on failure
 */
int uuid_to_string_standard(const uuid_t *uuid, char *buffer, size_t buffer_size);

/**
 * @brief Convert UUID to compact format string (no hyphens)
 * 
 * @param[in] uuid Pointer to uuid_t to convert
 * @param[out] buffer Output buffer (must be at least 33 bytes)
 * @param[in] buffer_size Size of output buffer
 * @return UUID_OK on success, error code on failure
 */
int uuid_to_string_compact(const uuid_t *uuid, char *buffer, size_t buffer_size);

/* ============================================================================
 * String to UUID Parsing
 * ============================================================================ */

/**
 * @brief Parse UUID from string
 * 
 * Parses a UUID string in standard or compact format.
 * Accepts both lowercase and uppercase hex characters.
 * 
 * @param[in] str String representation of UUID
 * @param[out] uuid Pointer to uuid_t to store parsed UUID
 * @return UUID_OK on success, error code on failure
 * 
 * @code
 * uuid_t uuid;
 * if (uuid_from_string("550e8400-e29b-41d4-a716-446655440000", &uuid) == UUID_OK) {
 *     // Use parsed UUID
 * }
 * @endcode
 */
int uuid_from_string(const char *str, uuid_t *uuid);

/**
 * @brief Parse UUID from string with length
 * 
 * Same as uuid_from_string but accepts string with explicit length.
 * Useful for parsing UUIDs embedded in larger strings.
 * 
 * @param[in] str String representation of UUID
 * @param[in] len Length of string (should be 36 for standard, 32 for compact)
 * @param[out] uuid Pointer to uuid_t to store parsed UUID
 * @return UUID_OK on success, error code on failure
 */
int uuid_from_string_n(const char *str, size_t len, uuid_t *uuid);

/* ============================================================================
 * UUID Validation
 * ============================================================================ */

/**
 * @brief Check if string is a valid UUID format
 * 
 * Validates that the string matches UUID format without parsing.
 * Accepts both standard (with hyphens) and compact (without hyphens) formats.
 * 
 * @param[in] str String to validate
 * @return true if valid UUID format, false otherwise
 * 
 * @code
 * if (uuid_is_valid_string("550e8400-e29b-41d4-a716-446655440000")) {
 *     // Valid UUID format
 * }
 * @endcode
 */
bool uuid_is_valid_string(const char *str);

/**
 * @brief Check if string is a valid UUID format with length
 * 
 * @param[in] str String to validate
 * @param[in] len Length of string
 * @return true if valid UUID format, false otherwise
 */
bool uuid_is_valid_string_n(const char *str, size_t len);

/**
 * @brief Validate UUID and get version
 * 
 * Checks if UUID is valid and returns its version.
 * For UUID v4, checks that version field is 4 and variant is RFC 4122.
 * 
 * @param[in] uuid Pointer to uuid_t to validate
 * @return Version number (1-5) if valid, 0 if invalid
 */
int uuid_get_version(const uuid_t *uuid);

/**
 * @brief Check if UUID is nil (all zeros)
 * 
 * @param[in] uuid Pointer to uuid_t to check
 * @return true if UUID is nil, false otherwise
 */
bool uuid_is_nil(const uuid_t *uuid);

/*