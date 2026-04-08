/**
 * @file hash_utils_example.c
 * @brief Hash Utilities Usage Examples
 *
 * Demonstrates various use cases for hash functions including:
 * - MD5, SHA1, SHA256, SHA512 hashing
 * - HMAC-SHA256 for message authentication
 * - Hash validation and verification
 * - Binary data hashing
 */

#include <stdio.h>
#include <string.h>
#include "../hash_utils/mod.h"

int main(void) {
    printf("============================================\n");
    printf("Hash Utilities Example\n");
    printf("============================================\n\n");

    /* Example 1: Basic String Hashing */
    printf("1. Basic String Hashing\n");
    printf("------------------------\n");
    
    const char *message = "Hello, World!";
    char md5_hex[HASH_MD5_HEX_LEN];
    char sha1_hex[HASH_SHA1_HEX_LEN];
    char sha256_hex[HASH_SHA256_HEX_LEN];
    char sha512_hex[HASH_SHA512_HEX_LEN];
    
    hash_md5_string_hex(message, md5_hex);
    hash_sha1_string_hex(message, sha1_hex);
    hash_sha256_string_hex(message, sha256_hex);
    hash_sha512_string_hex(message, sha512_hex);
    
    printf("Message: \"%s\"\n", message);
    printf("MD5:     %s\n", md5_hex);
    printf("SHA1:    %s\n", sha1_hex);
    printf("SHA256:  %s\n", sha256_hex);
    printf("SHA512:  %s\n", sha512_hex);

    /* Example 2: Empty String Hashing */
    printf("\n2. Empty String Hashing\n");
    printf("------------------------\n");
    
    hash_md5_string_hex("", md5_hex);
    hash_sha256_string_hex("", sha256_hex);
    
    printf("Empty string MD5:    %s\n", md5_hex);
    printf("Empty string SHA256: %s\n", sha256_hex);

    /* Example 3: Binary Data Hashing */
    printf("\n3. Binary Data Hashing\n");
    printf("------------------------\n");
    
    uint8_t binary_data[] = {0x00, 0x01, 0x02, 0x03, 0xFF, 0xFE, 0xFD, 0xFC};
    hash_sha256_hex(binary_data, sizeof(binary_data), sha256_hex);
    
    printf("Binary data SHA256: %s\n", sha256_hex);

    /* Example 4: HMAC-SHA256 for API Authentication */
    printf("\n4. HMAC-SHA256 Message Authentication\n");
    printf("--------------------------------------\n");
    
    const char *api_key = "my_secret_api_key";
    const char *payload = "{\"user\":\"john\",\"action\":\"login\"}";
    char hmac_hex[HASH_SHA256_HEX_LEN];
    
    hash_hmac_sha256_hex(api_key, payload, hmac_hex);
    
    printf("API Key:  %s\n", api_key);
    printf("Payload:  %s\n", payload);
    printf("HMAC:     %s\n", hmac_hex);
    
    /* Verify HMAC */
    if (hash_hmac_sha256_verify(api_key, payload, hmac_hex)) {
        printf("Status:   Valid signature\n");
    } else {
        printf("Status:   Invalid signature\n");
    }

    /* Example 5: Hash Validation */
    printf("\n5. Hash Format Validation\n");
    printf("--------------------------\n");
    
    const char *valid_md5 = "d41d8cd98f00b204e9800998ecf8427e";
    const char *invalid_md5 = "not_a_valid_hash";
    const char *valid_sha256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";
    
    printf("Valid MD5:    %s -> %s\n", valid_md5, 
           hash_is_valid_md5(valid_md5) ? "VALID" : "INVALID");
    printf("Invalid MD5:  %s -> %s\n", invalid_md5,
           hash_is_valid_md5(invalid_md5) ? "VALID" : "INVALID");
    printf("Valid SHA256: %s -> %s\n", valid_sha256,
           hash_is_valid_sha256(valid_sha256) ? "VALID" : "INVALID");

    /* Example 6: File Checksum Simulation */
    printf("\n6. File Checksum Simulation\n");
    printf("----------------------------\n");
    
    const char *file_content = "This is a simulated file content for checksum calculation.";
    char checksum[HASH_SHA256_HEX_LEN];
    
    hash_sha256_string_hex(file_content, checksum);
    
    printf("File content: \"%s\"\n", file_content);
    printf("SHA256 Checksum: %s\n", checksum);
    printf("Use this to verify file integrity.\n");

    /* Example 7: Password Hashing (Simple) */
    printf("\n7. Password Hashing Example\n");
    printf("----------------------------\n");
    
    const char *password = "MySecurePassword123!";
    const char *salt = "random_salt_value";
    char password_hash[HASH_SHA256_HEX_LEN];
    char salted_input[256];
    
    /* Combine password and salt */
    snprintf(salted_input, sizeof(salted_input), "%s%s", password, salt);
    hash_sha256_string_hex(salted_input, password_hash);
    
    printf("Password: %s\n", password);
    printf("Salt:     %s\n", salt);
    printf("Hash:     %s\n", password_hash);
    printf("Note: In production, use dedicated password hashing like bcrypt/argon2\n");

    /* Example 8: Incremental Hashing */
    printf("\n8. Incremental Hashing (Large Data)\n");
    printf("------------------------------------\n");
    
    hash_sha256_ctx_t ctx;
    hash_sha256_init(&ctx);
    
    /* Simulate processing data in chunks */
    const char *chunk1 = "First part of the data. ";
    const char *chunk2 = "Second part of the data. ";
    const char *chunk3 = "Final part of the data.";
    
    hash_sha256_update(&ctx, (const uint8_t *)chunk1, strlen(chunk1));
    hash_sha256_update(&ctx, (const uint8_t *)chunk2, strlen(chunk2));
    hash_sha256_update(&ctx, (const uint8_t *)chunk3, strlen(chunk3));
    
    uint8_t final_digest[HASH_SHA256_SIZE];
    hash_sha256_final(&ctx, final_digest);
    
    char final_hex[HASH_SHA256_HEX_LEN];
    hash_bytes_to_hex(final_digest, HASH_SHA256_SIZE, final_hex);
    
    printf("Chunk 1: \"%s\"\n", chunk1);
    printf("Chunk 2: \"%s\"\n", chunk2);
    printf("Chunk 3: \"%s\"\n", chunk3);
    printf("Final hash: %s\n", final_hex);

    /* Example 9: Hex Encoding/Decoding */
    printf("\n9. Hex Encoding and Decoding\n");
    printf("-----------------------------\n");
    
    uint8_t original[] = {0x48, 0x65, 0x6C, 0x6C, 0x6F}; /* "Hello" */
    char encoded[11];
    uint8_t decoded[5];
    
    hash_bytes_to_hex(original, 5, encoded);
    printf("Original bytes: {0x48, 0x65, 0x6C, 0x6C, 0x6F}\n");
    printf("Hex encoded:    %s\n", encoded);
    
    if (hash_hex_to_bytes(encoded, decoded, 5)) {
        printf("Decoded bytes:  {0x%02X, 0x%02X, 0x%02X, 0x%02X, 0x%02X}\n",
               decoded[0], decoded[1], decoded[2], decoded[3], decoded[4]);
        printf("Match: %s\n", (memcmp(original, decoded, 5) == 0) ? "YES" : "NO");
    }

    /* Example 10: Comparing Different Hash Algorithms */
    printf("\n10. Hash Algorithm Comparison\n");
    printf("------------------------------\n");
    
    const char *test_data = "AllToolkit Hash Utilities";
    printf("Data: \"%s\"\n\n", test_data);
    
    hash_md5_string_hex(test_data, md5_hex);
    hash_sha1_string_hex(test_data, sha1_hex);
    hash_sha256_string_hex(test_data, sha256_hex);
    hash_sha512_string_hex(test_data, sha512_hex);
    
    printf("Algorithm | Output Length | Hash\n");
    printf("----------|---------------|------\n");
    printf("MD5       | 128 bits      | %s\n", md5_hex);
    printf("SHA1      | 160 bits      | %s\n", sha1_hex);
    printf("SHA256    | 256 bits      | %s\n", sha256_hex);
    printf("SHA512    | 512 bits      | %s\n", sha512_hex);

    printf("\n============================================\n");
    printf("Examples completed successfully!\n");
    printf("============================================\n");

    return 0;
}
