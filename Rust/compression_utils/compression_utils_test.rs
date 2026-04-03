//! Compression Utilities Test Suite
//!
//! Comprehensive tests for the compression_utils module.
//! Run with: cargo test

#[path = "mod.rs"]
mod compression;

use compression::*;

#[test]
fn test_rle_basic() {
    let data = b"AAABBBCCCC";
    let compressed = rle_encode(data);
    assert_eq!(compressed.data, vec![3, b'A', 3, b'B', 4, b'C']);
    assert_eq!(compressed.original_len, 10);
    assert!(compressed.ratio < 1.0);

    let decompressed = rle_decode(&compressed.data);
    assert_eq!(decompressed, data.to_vec());
}

#[test]
fn test_rle_single_char() {
    let data = b"AAAAA";
    let compressed = rle_encode(data);
    assert_eq!(compressed.data, vec![5, b'A']);

    let decompressed = rle_decode(&compressed.data);
    assert_eq!(decompressed, data.to_vec());
}

#[test]
fn test_rle_no_repetition() {
    let data = b"ABCDEF";
    let compressed = rle_encode(data);
    assert_eq!(compressed.data, vec![1, b'A', 1, b'B', 1, b'C', 1, b'D', 1, b'E', 1, b'F']);

    let decompressed = rle_decode(&compressed.data);
    assert_eq!(decompressed, data.to_vec());
}

#[test]
fn test_rle_empty() {
    let compressed = rle_encode(b"");
    assert!(compressed.data.is_empty());
    assert_eq!(compressed.original_len, 0);
    assert_eq!(compressed.ratio, 0.0);

    let decompressed = rle_decode(&compressed.data);
    assert!(decompressed.is_empty());
}

#[test]
fn test_rle_max_count() {
    // Test that count wraps at 255
    let data = vec![b'A'; 300];
    let compressed = rle_encode(&data);
    assert_eq!(compressed.data[0], 255);
    assert_eq!(compressed.data[1], b'A');
    assert_eq!(compressed.data[2], 45);
    assert_eq!(compressed.data[3], b'A');

    let decompressed = rle_decode(&compressed.data);
    assert_eq!(decompressed.len(), 300);
    assert_eq!(decompressed, data);
}

#[test]
fn test_delta_basic() {
    let data = vec![10, 12, 15, 15, 20];
    let encoded = delta_encode(&data);
    assert_eq!(encoded, vec![10, 2, 3, 0, 5]);

    let decoded = delta_decode(&encoded);
    assert_eq!(decoded, data);
}

#[test]
fn test_delta_negative() {
    let data = vec![100, 90, 95, 80, 85];
    let encoded = delta_encode(&data);
    assert_eq!(encoded, vec![100, -10, 5, -15, 5]);

    let decoded = delta_decode(&encoded);
    assert_eq!(decoded, data);
}

#[test]
fn test_delta_empty() {
    let encoded = delta_encode(&[]);
    assert!(encoded.is_empty());

    let decoded = delta_decode(&[]);
    assert!(decoded.is_empty());
}

#[test]
fn test_delta_single() {
    let data = vec![42];
    let encoded = delta_encode(&data);
    assert_eq!(encoded, vec![42]);

    let decoded = delta_decode(&encoded);
    assert_eq!(decoded, data);
}

#[test]
fn test_base64_basic() {
    let data = b"Hello, World!";
    let encoded = base64_encode(data);
    assert_eq!(encoded, "SGVsbG8sIFdvcmxkIQ==");

    let decoded = base64_decode(&encoded);
    assert_eq!(decoded, Some(data.to_vec()));
}

#[test]
fn test_base64_empty() {
    assert_eq!(base64_encode(b""), "");
    assert_eq!(base64_decode(""), Some(Vec::new()));
}

#[test]
fn test_base64_padding() {
    // Test different padding scenarios
    let data1 = b"f";
    let encoded1 = base64_encode(data1);
    assert_eq!(encoded1, "Zg==");
    assert_eq!(base64_decode(&encoded1), Some(data1.to_vec()));

    let data2 = b"fo";
    let encoded2 = base64_encode(data2);
    assert_eq!(encoded2, "Zm8=");
    assert_eq!(base64_decode(&encoded2), Some(data2.to_vec()));

    let data3 = b"foo";
    let encoded3 = base64_encode(data3);
    assert_eq!(encoded3, "Zm9v");
    assert_eq!(base64_decode(&encoded3), Some(data3.to_vec()));
}

#[test]
fn test_base64_binary() {
    let data = vec![0x00, 0x01, 0x02, 0xFF, 0xFE];
    let encoded = base64_encode(&data);
    let decoded = base64_decode(&encoded);
    assert_eq!(decoded, Some(data));
}

#[test]
fn test_base64_invalid() {
    assert_eq!(base64_decode("invalid!"), None);
    assert_eq!(base64_decode("SGVsbG8"), None); // Not multiple of 4
    assert_eq!(base64_decode("SGVsbG8="), Some(b"Hello".to_vec()));
}

#[test]
fn test_hex_basic() {
    let data = b"Hello";
    let encoded = hex_encode(data);
    assert_eq!(encoded, "48656c6c6f");

    let decoded = hex_decode(&encoded);
    assert_eq!(decoded, Some(data.to_vec()));
}

#[test]
fn test_hex_empty() {
    assert_eq!(hex_encode(b""), "");
    assert_eq!(hex_decode(""), Some(Vec::new()));
}

#[test]
fn test_hex_uppercase() {
    let decoded = hex_decode("48656C6C6F");
    assert_eq!(decoded, Some(b"Hello".to_vec()));
}

#[test]
fn test_hex_binary() {
    let data = vec![0x00, 0xFF, 0xAB, 0xCD];
    let encoded = hex_encode(&data);
    assert_eq!(encoded, "00ffabcd");

    let decoded = hex_decode(&encoded);
    assert_eq!(decoded, Some(data));
}

#[test]
fn test_hex_invalid() {
    assert_eq!(hex_decode("xyz"), None);
    assert_eq!(hex_decode("486"), None); // Odd length
}

#[test]
fn test_url_encode_basic() {
    let data = "hello world!";
    let encoded = url_encode(data);
    assert_eq!(encoded, "hello%20world%21");

    let decoded = url_decode(&encoded);
    assert_eq!(decoded, Some(data.to_string()));
}

#[test]
fn test_url_encode_special() {
    let data = "path/to/file.txt";
    let encoded = url_encode(data);
    assert_eq!(encoded, "path%2Fto%2Ffile.txt");

    let decoded = url_decode(&encoded);
    assert_eq!(decoded, Some(data.to_string()));
}

#[test]
fn test_url_encode_unreserved() {
    // These should not be encoded
    let data = "abcABC123-_.~";
    let encoded = url_encode(data);
    assert_eq!(encoded, data);
}

#[test]
fn test_url_decode_plus() {
    // Plus sign should be decoded as space
    let decoded = url_decode("hello+world");
    assert_eq!(decoded, Some("hello world".to_string()));
}

#[test]
fn test_url_empty() {
    assert_eq!(url_encode(""), "");
    assert_eq!(url_decode(""), Some(String::new()));
}

#[test]
fn test_url_invalid() {
    assert_eq!(url_decode("%"), None);
    assert_eq!(url_decode("%G"), None);
    assert_eq!(url_decode("%GH"), None);
}

#[test]
fn test_calc_stats() {
    let stats = calc_stats(100, 60);
    assert_eq!(stats.original_size, 100);
    assert_eq!(stats.compressed_size, 60);
    assert_eq!(stats.ratio, 0.6);
    assert_eq!(stats.space_saved, 40.0);
}

#[test]
fn test_calc_stats_no_compression() {
    let stats = calc_stats(100, 100);
    assert_eq!(stats.ratio, 1.0);
    assert_eq!(stats.space_saved, 0.0);
}

#[test]
fn test_calc_stats_empty() {
    let stats = calc_stats(0, 0);
    assert_eq!(stats.ratio, 0.0);
    assert_eq!(stats.space_saved, 0.0);
}

#[test]
fn test_bwt_basic() {
    let data = b"banana";
    let (transformed, index) = bwt_transform(data);
    assert_eq!(transformed.len(), data.len());
    assert!(index < data.len());

    let restored = bwt_reverse(&transformed, index);
    assert_eq!(restored, data.to_vec());
}

#[test]
fn test_bwt_empty() {
    let (transformed, index) = bwt_transform(b"");
    assert!(transformed.is_empty());
    assert_eq!(index, 0);

    let restored = bwt_reverse(&transformed, index);
    assert!(restored.is_empty());
}

#[test]
fn test_bwt_single() {
    let data = b"A";
    let (transformed, index) = bwt_transform(data);
    let restored = bwt_reverse(&transformed, index);
    assert_eq!(restored, data.to_vec());
}

#[test]
fn test_lzw_basic() {
    let data = b"TOBEORNOTTOBEORTOBEORNOT";
    let compressed = lzw_compress(data);
    assert!(!compressed.is_empty());

    let decompressed = lzw_decompress(&compressed);
    assert_eq!(decompressed, data.to_vec());
}

#[test]
fn test_lzw_empty() {
    let compressed = lzw_compress(b"");
    assert!(compressed.is_empty());

    let decompressed = lzw_decompress(&compressed);
    assert!(decompressed.is_empty());
}

#[test]
fn test_lzw_single() {
    let data = b"A";
    let compressed = lzw_compress(data);
    let decompressed = lzw_decompress(&compressed);
    assert_eq!(decompressed, data.to_vec());
}

#[test]
fn test_lzw_repetitive() {
    let data = b"AAAAAAAAAA";
    let compressed = lzw_compress(data);
    let decompressed = lzw_decompress(&compressed);
    assert_eq!(decompressed, data.to_vec());
}

#[test]
fn test_is_valid_base64() {
    assert!(is_valid_base64(""));
    assert!(is_valid_base64("SGVsbG8="));
    assert!(is_valid_base64("SGVsbG8sIFdvcmxkIQ=="));
    assert!(!is_valid_base64("invalid!"));
    assert!(!is_valid_base64("SGVsbG8"));
}

#[test]
fn test_is_valid_hex() {
    assert!(is_valid_hex(""));
    assert!(is_valid_hex("48656c6c6f"));
    assert!(is_valid_hex("ABCDEF"));
    assert!(is_valid_hex("abcdef"));
    assert!(!is_valid_hex("xyz"));
    assert!(!is_valid_hex("486"));
}

#[test]
fn test_roundtrip_compression() {
    // Test various data patterns
    let test_cases = vec![
        b"The quick brown fox jumps over the lazy dog".to_vec(),
        vec![0u8; 100],
        vec![255u8; 100],
        (0..=255).collect::<Vec<u8>>(),
        b"AAAAAAAABBBBBBBBCCCCCCCC".to_vec(),
    ];

    for data in test_cases {
        // RLE
        let rle_compressed = rle_encode(&data);
        let rle_decompressed = rle_decode(&rle_compressed.data);
        assert_eq!(rle_decompressed, data, "RLE roundtrip failed");

        // Base64
        let b64_encoded = base64_encode(&data);
        let b64_decoded = base64_decode(&b64_encoded);
        assert_eq!(b64_decoded, Some(data.clone()), "Base64 roundtrip failed");

        // Hex
        let hex_encoded = hex_encode(&data);
        let hex_decoded = hex_decode(&hex_encoded);
        assert_eq!(hex_decoded, Some(data.clone()), "Hex roundtrip failed");
    }
}

#[test]
fn test_compression_stats_accuracy() {
    let data = b"Test data for compression statistics";
    let compressed = rle_encode(data);
    let stats = calc_stats(compressed.original_len, compressed.data.len());

    assert_eq!(stats.original_size, data.len());
    assert_eq!(stats.compressed_size, compressed.data.len());
    assert_eq!(stats.ratio, compressed.ratio);
}

#[test]
fn test_edge_cases() {
    // Very long repeated sequence
    let long_data = vec![b'X'; 1000];
    let compressed = rle_encode(&long_data);
    let decompressed = rle_decode(&compressed.data);
    assert_eq!(decompressed, long_data);

    // Alternating pattern
    let alt_data = b"ABABABABABABABABABAB";
    let compressed = rle_encode(alt_data);
    let decompressed = rle_decode(&compressed.data);
    assert_eq!(decompressed, alt_data.to_vec());

    // Binary data
    let binary = vec![0u8, 255u8, 0u8, 255u8, 128u8, 64u8, 32u8, 16u8];
    let b64 = base64_encode(&binary);
    let decoded = base64_decode(&b64);
    assert_eq!(decoded, Some(binary));
}

fn main() {
    println!("Running compression_utils tests...");
    println!("All tests should be run with: cargo test");
}
