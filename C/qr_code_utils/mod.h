/**
 * @file mod.h
 * @brief QR Code Generator for C - Zero-dependency QR code generation
 * @version 1.0.0
 *
 * A lightweight, zero-dependency QR code generator for C.
 * Supports all QR code versions (1-40) and error correction levels.
 *
 * Features:
 * - Generate QR codes from text strings
 * - Support for numeric, alphanumeric, and byte encoding modes
 * - Four error correction levels: L, M, Q, H
 * - Output as ASCII art or binary matrix
 * - Zero external dependencies
 *
 * @example
 * @code
 * #include "mod.h"
 *
 * // Create QR code
 * QRCode qr;
 * qr_code_init(&qr);
 *
 * // Generate QR code from text
 * if (qr_code_encode_text(&qr, "Hello, World!", QR_ECC_M)) {
 *     // Print as ASCII art
 *     qr_code_print_ascii(&qr);
 * }
 *
 * // Cleanup
 * qr_code_free(&qr);
 * @endcode
 */

#ifndef QR_CODE_UTILS_H
#define QR_CODE_UTILS_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Maximum QR code version (1-40)
 */
#define QR_CODE_MAX_VERSION 40

/**
 * @brief Maximum QR code size in modules (version 40)
 */
#define QR_CODE_MAX_SIZE 177

/**
 * @brief Maximum data capacity in bytes
 */
#define QR_CODE_MAX_DATA 2953

/**
 * @brief Error correction levels
 */
typedef enum {
    QR_ECC_L = 0,  /**< Low - ~7% correction */
    QR_ECC_M = 1,  /**< Medium - ~15% correction */
    QR_ECC_Q = 2,  /**< Quartile - ~25% correction */
    QR_ECC_H = 3   /**< High - ~30% correction */
} QRCodeEcc;

/**
 * @brief Encoding modes
 */
typedef enum {
    QR_MODE_NUMERIC = 0,      /**< Numeric only (0-9) */
    QR_MODE_ALPHANUMERIC = 1, /**< Alphanumeric (0-9, A-Z, space, $%*+-./:) */
    QR_MODE_BYTE = 2          /**< Binary/byte mode (any data) */
} QRCodeMode;

/**
 * @brief QR code structure
 */
typedef struct {
    uint8_t modules[QR_CODE_MAX_SIZE][QR_CODE_MAX_SIZE]; /**< Module data (0=white, 1=black, 2=unset) */
    int size;                                             /**< QR code size in modules (21-177) */
    int version;                                          /**< QR code version (1-40) */
    QRCodeEcc ecc;                                        /**< Error correction level */
    QRCodeMode mode;                                      /**< Encoding mode used */
    int mask_pattern;                                     /**< Mask pattern used (0-7) */
    bool initialized;                                     /**< Whether structure is initialized */
} QRCode;

/**
 * @brief Result codes
 */
typedef enum {
    QR_OK = 0,                    /**< Success */
    QR_ERROR_INVALID_INPUT = -1,  /**< Invalid input parameters */
    QR_ERROR_DATA_TOO_LONG = -2,  /**< Data exceeds capacity */
    QR_ERROR_VERSION = -3,        /**< Invalid version */
    QR_ERROR_ECC = -4,            /**< Invalid error correction level */
    QR_ERROR_MEMORY = -5,         /**< Memory allocation failed */
    QR_ERROR_NOT_INITIALIZED = -6 /**< QR code not initialized */
} QRCodeResult;

/**
 * @brief Initialize a QR code structure
 * @param qr Pointer to QRCode structure to initialize
 * @return QR_OK on success, error code on failure
 */
int qr_code_init(QRCode *qr);

/**
 * @brief Free QR code resources
 * @param qr Pointer to QRCode structure
 */
void qr_code_free(QRCode *qr);

/**
 * @brief Encode text as QR code (auto-detects best mode)
 * @param qr Pointer to initialized QRCode structure
 * @param text Null-terminated text string to encode
 * @param ecc Error correction level (QR_ECC_L/M/Q/H)
 * @return QR_OK on success, error code on failure
 */
int qr_code_encode_text(QRCode *qr, const char *text, QRCodeEcc ecc);

/**
 * @brief Encode binary data as QR code
 * @param qr Pointer to initialized QRCode structure
 * @param data Binary data to encode
 * @param length Length of data in bytes
 * @param ecc Error correction level
 * @return QR_OK on success, error code on failure
 */
int qr_code_encode_binary(QRCode *qr, const uint8_t *data, size_t length, QRCodeEcc ecc);

/**
 * @brief Encode with specific mode and version
 * @param qr Pointer to initialized QRCode structure
 * @param text Text to encode
 * @param version QR version (1-40, or 0 for auto)
 * @param ecc Error correction level
 * @param mode Encoding mode (or -1 for auto)
 * @return QR_OK on success, error code on failure
 */
int qr_code_encode_advanced(QRCode *qr, const char *text, int version, QRCodeEcc ecc, QRCodeMode mode);

/**
 * @brief Get module value at coordinates
 * @param qr Pointer to QRCode structure
 * @param x X coordinate (0 to size-1)
 * @param y Y coordinate (0 to size-1)
 * @return 1 for black module, 0 for white, -1 for error
 */
int qr_code_get_module(const QRCode *qr, int x, int y);

/**
 * @brief Print QR code as ASCII art to stdout (Unicode)
 * @param qr Pointer to QRCode structure
 */
void qr_code_print_ascii(const QRCode *qr);

/**
 * @brief Print QR code as simple ASCII
 * @param qr Pointer to QRCode structure
 */
void qr_code_print_simple(const QRCode *qr);

/**
 * @brief Get QR code version from size
 * @param size Size in modules
 * @return Version (1-40), or 0 if invalid
 */
int qr_code_version_from_size(int size);

/**
 * @brief Get QR code size from version
 * @param version Version (1-40)
 * @return Size in modules, or 0 if invalid
 */
int qr_code_size_from_version(int version);

/**
 * @brief Get maximum data capacity for version and ECC
 * @param version QR version (1-40)
 * @param ecc Error correction level
 * @param mode Encoding mode
 * @return Maximum data bytes, or 0 if invalid
 */
int qr_code_get_capacity(int version, QRCodeEcc ecc, QRCodeMode mode);

/**
 * @brief Check if text can be encoded in numeric mode
 * @param text Text to check
 * @return true if numeric only, false otherwise
 */
bool qr_code_is_numeric(const char *text);

/**
 * @brief Check if text can be encoded in alphanumeric mode
 * @param text Text to check
 * @return true if alphanumeric compatible, false otherwise
 */
bool qr_code_is_alphanumeric(const char *text);

/**
 * @brief Get optimal encoding mode for text
 * @param text Text to analyze
 * @return Recommended encoding mode
 */
QRCodeMode qr_code_get_best_mode(const char *text);

/**
 * @brief Get error correction level as string
 * @param ecc Error correction level
 * @return String representation ("L", "M", "Q", "H", or "?")
 */
const char* qr_code_ecc_to_string(QRCodeEcc ecc);

/**
 * @brief Get encoding mode as string
 * @param mode Encoding mode
 * @return String representation ("Numeric", "Alphanumeric", "Byte", or "?")
 */
const char* qr_code_mode_to_string(QRCodeMode mode);

/**
 * @brief Get result code as string
 * @param result Result code
 * @return String description
 */
const char* qr_code_result_to_string(int result);

#ifdef __cplusplus
}
#endif

#endif /* QR_CODE_UTILS_H */
