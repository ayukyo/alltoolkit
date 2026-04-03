//! Compression Utilities Example
//!
//! Demonstrates usage of the compression_utils module.
//! Run with: cargo run --example compression_utils_example

#[path = "../compression_utils/mod.rs"]
mod compression;

use compression::*;

fn main() {
    println!("=== Compression Utilities Examples ===\n");

    // 1. Run-Length Encoding (RLE)
    println!("1. Run-Length Encoding (RLE)");
    println!("   RLE is efficient for data with many consecutive repeated values.");
    println!();

    let rle_data = b"AAABBBCCCCDDDD";
    println!("   Original: {:?}", std::str::from_utf8(rle_data).unwrap());
    println!("   Original size: {} bytes", rle_data.len());

    let rle_compressed = rle_encode(rle_data);
    println!("   Compressed: {:?}", rle_compressed.data);
    println!("   Compressed size: {} bytes", rle_compressed.data.len());
    println!("   Compression ratio: {:.2}", rle_compressed.ratio);

    let rle_decompressed = rle_decode(&rle_compressed.data);
    println!("   Decompressed: {:?}", std::str::from_utf8(&rle_decompressed).unwrap());
    println!("   Match: {}", rle_decompressed == rle_data);
    println!();

    // 2. Delta Encoding
    println!("2. Delta Encoding");
    println!("   Delta encoding stores differences between consecutive values.");
    println!("   Efficient for time-series data or sequences with small changes.");
    println!();

    let delta_data = vec![100, 102, 105, 105, 108, 110, 115];
    println!("   Original: {:?}", delta_data);

    let delta_encoded = delta_encode(&delta_data);
    println!("   Delta encoded: {:?}", delta_encoded);
    println!("   First value + differences");

    let delta_decoded = delta_decode(&delta_encoded);
    println!("   Decoded: {:?}", delta_decoded);
    println!("   Match: {}", delta_decoded == delta_data);
    println!();

    // 3. Base64 Encoding
    println!("3. Base64 Encoding");
    println!("   Base64 converts binary data to ASCII text.");
    println!("   Commonly used for data transmission and storage.");
    println!();

    let text = "Hello, World!";
    let b64_encoded = base64_encode(text.as_bytes());
    println!("   Original: {}", text);
    println!("   Base64 encoded: {}", b64_encoded);

    let b64_decoded = base64_decode(&b64_encoded);
    println!("   Decoded: {}", std::str::from_utf8(&b64_decoded.unwrap()).unwrap());
    println!();

    // Binary data example
    let binary = vec![0x00, 0x01, 0x02, 0xFF, 0xFE];
    let b64_binary = base64_encode(&binary);
    println!("   Binary data: {:?}", binary);
    println!("   Base64 encoded: {}", b64_binary);
    println!();

    // 4. Hex Encoding
    println!("4. Hex Encoding");
    println!("   Hex encoding converts binary to hexadecimal representation.");
    println!();

    let hex_data = b"Rust";
    let hex_encoded = hex_encode(hex_data);
    println!("   Original: {:?}", std::str::from_utf8(hex_data).unwrap());
    println!("   Hex encoded: {}", hex_encoded);

    let hex_decoded = hex_decode(&hex_encoded);
    println!("   Decoded: {:?}", std::str::from_utf8(&hex_decoded.unwrap()).unwrap());
    println!();

    // 5. URL Encoding
    println!("5. URL Encoding (Percent-Encoding)");
    println!("   URL encoding makes strings safe for use in URLs.");
    println!();

    let url_data = "hello world! how are you?";
    let url_encoded = url_encode(url_data);
    println!("   Original: {}", url_data);
    println!("   URL encoded: {}", url_encoded);

    let url_decoded = url_decode(&url_encoded);
    println!("   Decoded: {}", url_decoded.unwrap());
    println!();

    // 6. Burrows-Wheeler Transform
    println!("6. Burrows-Wheeler Transform (BWT)");
    println!("   BWT rearranges data to group similar characters together.");
    println!("   Often used as a preprocessing step for compression.");
    println!();

    let bwt_data = b"banana";
    println!("   Original: {:?}", std::str::from_utf8(bwt_data).unwrap());

    let (bwt_transformed, index) = bwt_transform(bwt_data);
    println!("   BWT transformed: {:?}", std::str::from_utf8(&bwt_transformed).unwrap());
    println!("   Original index: {}", index);

    let bwt_restored = bwt_reverse(&bwt_transformed, index);
    println!("   Restored: {:?}", std::str::from_utf8(&bwt_restored).unwrap());
    println!("   Match: {}", bwt_restored == bwt_data.to_vec());
    println!();

    // 7. LZW Compression
    println!("7. LZW Compression");
    println!("   LZW (Lempel-Ziv-Welch) is a dictionary-based compression.");
    println!("   Builds a dictionary of patterns and replaces them with codes.");
    println!();

    let lzw_data = b"TOBEORNOTTOBEORTOBEORNOT";
    println!("   Original: {:?}", std::str::from_utf8(lzw_data).unwrap());
    println!("   Original size: {} bytes", lzw_data.len());

    let lzw_compressed = lzw_compress(lzw_data);
    println!("   Compressed codes: {:?}", lzw_compressed);
    println!("   Compressed size: {} codes ({} bytes if stored as u16)",
             lzw_compressed.len(), lzw_compressed.len() * 2);

    let lzw_decompressed = lzw_decompress(&lzw_compressed);
    println!("   Decompressed: {:?}", std::str::from_utf8(&lzw_decompressed).unwrap());
    println!("   Match: {}", lzw_decompressed == lzw_data.to_vec());
    println!();

    // 8. Compression Statistics
    println!("8. Compression Statistics");
    println!("   Calculate compression effectiveness.");
    println!();

    let stats_data = b"AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDD";
    let stats_compressed = rle_encode(stats_data);
    let stats = calc_stats(stats_compressed.original_len, stats_compressed.data.len());

    println!("   Original size: {} bytes", stats.original_size);
    println!("   Compressed size: {} bytes", stats.compressed_size);
    println!("   Compression ratio: {:.2}", stats.ratio);
    println!("   Space saved: {:.1}%", stats.space_saved);
    println!();

    // 9. Validation Functions
    println!("9. Validation Functions");
    println!("   Check if strings are valid encoded data.");
    println!();

    let valid_b64 = "SGVsbG8gV29ybGQh";
    let invalid_b64 = "Not@Valid!";
    println!("   Is '{}' valid Base64? {}", valid_b64, is_valid_base64(valid_b64));
    println!("   Is '{}' valid Base64? {}", invalid_b64, is_valid_base64(invalid_b64));

    let valid_hex = "48656c6c6f";
    let invalid_hex = "xyz123";
    println!("   Is '{}' valid Hex? {}", valid_hex, is_valid_hex(valid_hex));
    println!("   Is '{}' valid Hex? {}", invalid_hex, is_valid_hex(invalid_hex));
    println!();

    // 10. Practical Example: Log Data Compression
    println!("10. Practical Example: Log Data Compression");
    println!("    Compressing repetitive log entries.");
    println!();

    let log_data = b"ERROR: Connection failed\nERROR: Connection failed\nERROR: Connection failed\nINFO: Retrying...\nINFO: Retrying...\nSUCCESS: Connected\n";
    println!("    Original log ({} bytes):", log_data.len());
    println!("    {}", std::str::from_utf8(log_data).unwrap());

    let log_compressed = rle_encode(log_data);
    let log_stats = calc_stats(log_data.len(), log_compressed.data.len());

    println!("    Compressed to {} bytes", log_compressed.data.len());
    println!("    Compression ratio: {:.2}", log_stats.ratio);
    println!("    Space saved: {:.1}%", log_stats.space_saved);
    println!();

    // 11. Practical Example: Sensor Data
    println!("11. Practical Example: Sensor Data (Delta Encoding)");
    println!("    Temperature readings over time.");
    println!();

    let temps = vec![200, 201, 203, 202, 205, 207, 210, 212, 211, 213]; // in tenths of degrees
    println!("    Temperature readings: {:?}", temps);
    println!("    Temperatures in Celsius: {:?}", temps.iter().map(|t| *t as f64 / 10.0).collect::<Vec<f64>>());

    let temps_encoded = delta_encode(&temps);
    println!("    Delta encoded: {:?}", temps_encoded);
    println!("    Small differences are more compressible!");
    println!();

    println!("=== All examples completed successfully! ===");
}