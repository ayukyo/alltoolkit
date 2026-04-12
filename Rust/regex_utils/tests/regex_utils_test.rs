//! # Regex Utilities - Comprehensive Test Suite
//!
//! This file contains extensive tests for the regex_utils module.
//! Run with: cargo test --test regex_utils_test
//!
//! All tests are designed to verify correctness, edge cases, and performance.

use regex_utils::{
    // Validation
    is_email, is_ipv4, is_ipv6, is_url, is_phone, is_china_phone,
    is_date, is_time, is_uuid, is_hex_color, is_username,
    is_strong_password, is_china_id, is_china_postcode, is_china_license,
    matches_pattern,
    
    // Extraction
    extract_all, extract_numbers, extract_emails, extract_urls,
    extract_phones, extract_china_phones, extract_first_capture,
    extract_captures, extract_named_captures,
    
    // Replacement
    replace_all, replace_first, remove_all, strip_html,
    normalize_whitespace, sanitize_filename,
    
    // Utility
    count_matches, contains_pattern, split_by, escape_regex,
    is_valid_regex,
    
    // Patterns
    patterns,
};

// ============================================================================
// Validation Function Tests
// ============================================================================

mod validation {
    use super::*;

    #[test]
    fn test_is_email_valid() {
        let valid_emails = vec![
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user_name@example.co.uk",
            "test123@sub.domain.org",
            "a@b.co",
            "user@domain.io",
        ];
        
        for email in valid_emails {
            assert!(is_email(email), "Expected {} to be valid", email);
        }
    }

    #[test]
    fn test_is_email_invalid() {
        let invalid_emails = vec![
            "invalid",
            "@example.com",
            "user@",
            "user@.com",
            "user@domain",
            "@",
            "",
            "user name@example.com",
        ];
        
        for email in invalid_emails {
            assert!(!is_email(email), "Expected {} to be invalid", email);
        }
    }

    #[test]
    fn test_is_ipv4_valid() {
        let valid_ips = vec![
            "192.168.1.1",
            "0.0.0.0",
            "255.255.255.255",
            "10.0.0.1",
            "172.16.0.1",
            "127.0.0.1",
        ];
        
        for ip in valid_ips {
            assert!(is_ipv4(ip), "Expected {} to be valid IPv4", ip);
        }
    }

    #[test]
    fn test_is_ipv4_invalid() {
        let invalid_ips = vec![
            "256.1.1.1",
            "192.168.1",
            "192.168.1.1.1",
            "192.168.-1.1",
            "abc.def.ghi.jkl",
            "",
            "192.168.1.1:8080",
        ];
        
        for ip in invalid_ips {
            assert!(!is_ipv4(ip), "Expected {} to be invalid IPv4", ip);
        }
    }

    #[test]
    fn test_is_url_valid() {
        let valid_urls = vec![
            "https://example.com",
            "http://localhost:8080",
            "https://sub.domain.com/path",
            "http://example.com?query=1&value=2",
            "https://example.com/path/to/resource",
            "http://127.0.0.1:3000",
        ];
        
        for url in valid_urls {
            assert!(is_url(url), "Expected {} to be valid URL", url);
        }
    }

    #[test]
    fn test_is_url_invalid() {
        let invalid_urls = vec![
            "ftp://example.com",
            "not-a-url",
            "example.com",
            "www.example.com",
            "",
            "http://",
            "https://",
        ];
        
        for url in invalid_urls {
            assert!(!is_url(url), "Expected {} to be invalid URL", url);
        }
    }

    #[test]
    fn test_is_phone_valid() {
        let valid_phones = vec![
            "+1234567890",
            "1234567890",
            "+8613812345678",
            "+442071234567",
            "19876543210",
        ];
        
        for phone in valid_phones {
            assert!(is_phone(phone), "Expected {} to be valid phone", phone);
        }
    }

    #[test]
    fn test_is_phone_invalid() {
        let invalid_phones = vec![
            "123",
            "+0123456789",
            "abcdefghij",
            "",
            "+123456789012345678",
            "12-345-6789",
        ];
        
        for phone in invalid_phones {
            assert!(!is_phone(phone), "Expected {} to be invalid phone", phone);
        }
    }

    #[test]
    fn test_is_china_phone_valid() {
        let valid_phones = vec![
            "13812345678",
            "19912345678",
            "13012345678",
            "15912345678",
            "18612345678",
        ];
        
        for phone in valid_phones {
            assert!(is_china_phone(phone), "Expected {} to be valid China phone", phone);
        }
    }

    #[test]
    fn test_is_china_phone_invalid() {
        let invalid_phones = vec![
            "12345678",
            "23812345678",
            "12345678901",
            "",
            "+8613812345678",
            "138-1234-5678",
        ];
        
        for phone in invalid_phones {
            assert!(!is_china_phone(phone), "Expected {} to be invalid China phone", phone);
        }
    }

    #[test]
    fn test_is_date_valid() {
        let valid_dates = vec![
            "2024-06-15",
            "2000-01-01",
            "2024-12-31",
            "1999-06-30",
            "2024-02-29",
        ];
        
        for date in valid_dates {
            assert!(is_date(date), "Expected {} to be valid date", date);
        }
    }

    #[test]
    fn test_is_date_invalid() {
        let invalid_dates = vec![
            "2024-13-01",
            "2024/06/15",
            "06-15-2024",
            "2024-6-15",
            "2024-06-32",
            "",
            "20240615",
        ];
        
        for date in invalid_dates {
            assert!(!is_date(date), "Expected {} to be invalid date", date);
        }
    }

    #[test]
    fn test_is_time_valid() {
        let valid_times = vec![
            "14:30:00",
            "00:00:00",
            "23:59:59",
            "12:00:00",
            "01:01:01",
        ];
        
        for time in valid_times {
            assert!(is_time(time), "Expected {} to be valid time", time);
        }
    }

    #[test]
    fn test_is_time_invalid() {
        let invalid_times = vec![
            "25:00:00",
            "14:60:00",
            "14:30",
            "14:30:60",
            "1:30:00",
            "",
            "14-30-00",
        ];
        
        for time in invalid_times {
            assert!(!is_time(time), "Expected {} to be invalid time", time);
        }
    }

    #[test]
    fn test_is_uuid_valid() {
        let valid_uuids = vec![
            "550e8400-e29b-41d4-a716-446655440000",
            "123e4567-e89b-12d3-a456-426614174000",
            "00000000-0000-0000-0000-000000000000",
            "ffffffff-ffff-ffff-ffff-ffffffffffff",
            "ABCDEF12-3456-7890-ABCD-EF1234567890",
        ];
        
        for uuid in valid_uuids {
            assert!(is_uuid(uuid), "Expected {} to be valid UUID", uuid);
        }
    }

    #[test]
    fn test_is_uuid_invalid() {
        let invalid_uuids = vec![
            "not-a-uuid",
            "550e8400e29b41d4a716446655440000",
            "550e8400-e29b-41d4-a716",
            "",
            "550e8400-e29b-41d4-a716-44665544000g",
        ];
        
        for uuid in invalid_uuids {
            assert!(!is_uuid(uuid), "Expected {} to be invalid UUID", uuid);
        }
    }

    #[test]
    fn test_is_hex_color_valid() {
        let valid_colors = vec![
            "#FFF",
            "#fff",
            "#FF5733",
            "#ff5733",
            "#FF5733AA",
            "#ABC",
            "#123456",
            "#12345678",
        ];
        
        for color in valid_colors {
            assert!(is_hex_color(color), "Expected {} to be valid hex color", color);
        }
    }

    #[test]
    fn test_is_hex_color_invalid() {
        let invalid_colors = vec![
            "FF5733",
            "#GGG",
            "#FF",
            "#FFFFF",
            "#FFFFFFF",
            "",
            "#FF573",
        ];
        
        for color in invalid_colors {
            assert!(!is_hex_color(color), "Expected {} to be invalid hex color", color);
        }
    }

    #[test]
    fn test_is_username_valid() {
        let valid_usernames = vec![
            "john_doe",
            "user123",
            "Test_User",
            "abc",
            "user_name_123",
            "a__________________b",
        ];
        
        for username in valid_usernames {
            assert!(is_username(username), "Expected {} to be valid username", username);
        }
    }

    #[test]
    fn test_is_username_invalid() {
        let invalid_usernames = vec![
            "ab",
            "123start",
            "user-name",
            "user name",
            "",
            "user@name",
            "a________________________________b",
        ];
        
        for username in invalid_usernames {
            assert!(!is_username(username), "Expected {} to be invalid username", username);
        }
    }

    #[test]
    fn test_is_strong_password_valid() {
        let valid_passwords = vec![
            "SecureP@ss1!",
            "MyP@ssw0rd!",
            "Str0ng!Pass",
            "C0mplex#Pass",
        ];
        
        for password in valid_passwords {
            assert!(is_strong_password(password), "Expected {} to be strong password", password);
        }
    }

    #[test]
    fn test_is_strong_password_invalid() {
        let invalid_passwords = vec![
            "weak",
            "NoSpecial1",
            "nouppercase1!",
            "NOLOWERCASE1!",
            "NoDigit@!",
            "Short1!",
            "",
        ];
        
        for password in invalid_passwords {
            assert!(!is_strong_password(password), "Expected {} to be weak password", password);
        }
    }

    #[test]
    fn test_is_china_id_valid() {
        let valid_ids = vec![
            "11010519491231002X",
            "110105199001011234",
            "310101200001011234",
        ];
        
        for id in valid_ids {
            assert!(is_china_id(id), "Expected {} to be valid China ID", id);
        }
    }

    #[test]
    fn test_is_china_id_invalid() {
        let invalid_ids = vec![
            "123456",
            "11010519491231002",
            "",
            "11010519491231002A",
        ];
        
        for id in invalid_ids {
            assert!(!is_china_id(id), "Expected {} to be invalid China ID", id);
        }
    }

    #[test]
    fn test_is_china_postcode_valid() {
        let valid_postcodes = vec![
            "100000",
            "200000",
            "518000",
            "430000",
        ];
        
        for postcode in valid_postcodes {
            assert!(is_china_postcode(postcode), "Expected {} to be valid postcode", postcode);
        }
    }

    #[test]
    fn test_is_china_postcode_invalid() {
        let invalid_postcodes = vec![
            "12345",
            "012345",
            "",
            "1234567",
            "abcdef",
        ];
        
        for postcode in invalid_postcodes {
            assert!(!is_china_postcode(postcode), "Expected {} to be invalid postcode", postcode);
        }
    }

    #[test]
    fn test_is_china_license_valid() {
        let valid_plates = vec![
            "京A12345",
            "沪B12345",
            "粤A12345",
            "浙B12345",
            "苏A12345",
        ];
        
        for plate in valid_plates {
            assert!(is_china_license(plate), "Expected {} to be valid license", plate);
        }
    }

    #[test]
    fn test_is_china_license_invalid() {
        let invalid_plates = vec![
            "AB12345",
            "A12345",
            "",
            "京12345",
            "京AB1234",  // 6 chars after province, should be 4-5
        ];
        
        for plate in invalid_plates {
            assert!(!is_china_license(plate), "Expected {} to be invalid license", plate);
        }
    }

    #[test]
    fn test_matches_pattern_basic() {
        assert!(matches_pattern(r"^\d{3}-\d{4}$", "123-4567"));
        assert!(!matches_pattern(r"^\d{3}-\d{4}$", "1234567"));
        assert!(!matches_pattern(r"[invalid", "test"));
    }
}

// ============================================================================
// Extraction Function Tests
// ============================================================================

mod extraction {
    use super::*;

    #[test]
    fn test_extract_all_basic() {
        let matches = extract_all(r"\d+", "abc123def456");
        assert_eq!(matches, vec!["123", "456"]);
    }

    #[test]
    fn test_extract_all_no_matches() {
        let matches = extract_all(r"\d+", "abcdef");
        assert!(matches.is_empty());
    }

    #[test]
    fn test_extract_all_invalid_pattern() {
        let matches = extract_all(r"[invalid", "abc123");
        assert!(matches.is_empty());
    }

    #[test]
    fn test_extract_numbers_basic() {
        let numbers = extract_numbers("Price: $100, discount: $20.50");
        assert_eq!(numbers, vec!["100", "20", "50"]);
    }

    #[test]
    fn test_extract_numbers_mixed() {
        let numbers = extract_numbers("Room 101, floor 2, building 3");
        assert_eq!(numbers, vec!["101", "2", "3"]);
    }

    #[test]
    fn test_extract_emails_basic() {
        let emails = extract_emails("Contact: user@example.com or admin@test.org");
        assert_eq!(emails, vec!["user@example.com", "admin@test.org"]);
    }

    #[test]
    fn test_extract_emails_none() {
        let emails = extract_emails("No emails here");
        assert!(emails.is_empty());
    }

    #[test]
    fn test_extract_urls_basic() {
        let urls = extract_urls("Visit https://example.com or http://test.org/path");
        assert_eq!(urls, vec!["https://example.com", "http://test.org/path"]);
    }

    #[test]
    fn test_extract_phones_basic() {
        let phones = extract_phones("Call +1234567890 or 9876543210");
        assert_eq!(phones, vec!["+1234567890", "9876543210"]);
    }

    #[test]
    fn test_extract_china_phones_basic() {
        let phones = extract_china_phones("联系 13812345678 或 19987654321");
        // Pattern matches 1[3-9]\d{9} - 11 digits starting with 1
        assert!(phones.contains(&"13812345678".to_string()));
        assert!(phones.contains(&"19987654321".to_string()));
    }

    #[test]
    fn test_extract_first_capture_found() {
        let name = extract_first_capture(r"name=(\w+)", "user=name=John&age=30");
        assert_eq!(name, Some("John".to_string()));
    }

    #[test]
    fn test_extract_first_capture_not_found() {
        let result = extract_first_capture(r"notfound=(\w+)", "name=John");
        assert_eq!(result, None);
    }

    #[test]
    fn test_extract_captures_basic() {
        let matches = extract_captures(r"(\w+)=(\d+)", "a=1 b=2 c=3");
        assert_eq!(matches.len(), 3);
        assert_eq!(matches[0], vec!["a", "1"]);
        assert_eq!(matches[1], vec!["b", "2"]);
        assert_eq!(matches[2], vec!["c", "3"]);
    }

    #[test]
    fn test_extract_named_captures_basic() {
        let data = extract_named_captures(
            r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})",
            "2024-06-15"
        );
        assert_eq!(data.get("year"), Some(&"2024".to_string()));
        assert_eq!(data.get("month"), Some(&"06".to_string()));
        assert_eq!(data.get("day"), Some(&"15".to_string()));
    }

    #[test]
    fn test_extract_named_captures_empty() {
        // Test with a pattern that won't match the input
        let data = extract_named_captures(r"(?P<code>\d{4})", "no match here");
        assert!(data.is_empty());
    }
}

// ============================================================================
// Replacement Function Tests
// ============================================================================

mod replacement {
    use super::*;

    #[test]
    fn test_replace_all_basic() {
        let result = replace_all(r"\d+", "abc123def456", "NUM");
        assert_eq!(result, "abcNUMdefNUM");
    }

    #[test]
    fn test_replace_all_with_capture_groups() {
        let result = replace_all(r"(\w+) (\w+)", "John Doe", "$2, $1");
        assert_eq!(result, "Doe, John");
    }

    #[test]
    fn test_replace_all_no_matches() {
        let result = replace_all(r"\d+", "abcdef", "NUM");
        assert_eq!(result, "abcdef");
    }

    #[test]
    fn test_replace_first_basic() {
        let result = replace_first(r"\d+", "abc123def456", "NUM");
        assert_eq!(result, "abcNUMdef456");
    }

    #[test]
    fn test_replace_first_only_first() {
        let result = replace_first(r"o", "hello world", "X");
        assert_eq!(result, "hellX world");
    }

    #[test]
    fn test_remove_all_basic() {
        let result = remove_all(r"\s+", "hello   world");
        assert_eq!(result, "helloworld");
    }

    #[test]
    fn test_remove_all_vowels() {
        let result = remove_all(r"[aeiou]", "hello world");
        assert_eq!(result, "hll wrld");
    }

    #[test]
    fn test_strip_html_basic() {
        let result = strip_html("<p>Hello <b>World</b></p>");
        assert_eq!(result, "Hello World");
    }

    #[test]
    fn test_strip_html_with_attributes() {
        let result = strip_html("<div class='test'><span>Content</span></div>");
        assert_eq!(result, "Content");
    }

    #[test]
    fn test_strip_html_empty() {
        let result = strip_html("No HTML here");
        assert_eq!(result, "No HTML here");
    }

    #[test]
    fn test_normalize_whitespace_basic() {
        let result = normalize_whitespace("  hello   world  \n\t test  ");
        assert_eq!(result, "hello world test");
    }

    #[test]
    fn test_normalize_whitespace_single_space() {
        let result = normalize_whitespace("hello");
        assert_eq!(result, "hello");
    }

    #[test]
    fn test_sanitize_filename_basic() {
        let result = sanitize_filename("my file: name?.txt");
        assert_eq!(result, "my_file_name.txt");
    }

    #[test]
    fn test_sanitize_filename_special_chars() {
        let result = sanitize_filename("test<>file.txt");
        assert_eq!(result, "testfile.txt");
    }

    #[test]
    fn test_sanitize_filename_preserves_extension() {
        let result = sanitize_filename("my_document_final.pdf");
        assert_eq!(result, "my_document_final.pdf");
    }
}

// ============================================================================
// Utility Function Tests
// ============================================================================

mod utility {
    use super::*;

    #[test]
    fn test_count_matches_basic() {
        let count = count_matches(r"\d+", "abc123def456ghi789");
        assert_eq!(count, 3);
    }

    #[test]
    fn test_count_matches_zero() {
        let count = count_matches(r"\d+", "abcdef");
        assert_eq!(count, 0);
    }

    #[test]
    fn test_count_matches_invalid_pattern() {
        let count = count_matches(r"[invalid", "abc123");
        assert_eq!(count, 0);
    }

    #[test]
    fn test_contains_pattern_found() {
        assert!(contains_pattern(r"\d+", "abc123"));
    }

    #[test]
    fn test_contains_pattern_not_found() {
        assert!(!contains_pattern(r"\d+", "abcdef"));
    }

    #[test]
    fn test_split_by_whitespace() {
        let parts = split_by(r"\s+", "hello world  test");
        assert_eq!(parts, vec!["hello", "world", "test"]);
    }

    #[test]
    fn test_split_by_comma() {
        let parts = split_by(r",", "a,b,c");
        assert_eq!(parts, vec!["a", "b", "c"]);
    }

    #[test]
    fn test_split_by_no_match() {
        let parts = split_by(r",", "abc");
        assert_eq!(parts, vec!["abc"]);
    }

    #[test]
    fn test_escape_regex_special_chars() {
        let escaped = escape_regex("price: $100 (50% off)");
        assert_eq!(escaped, r"price: \$100 \(50% off\)");
    }

    #[test]
    fn test_escape_regex_backslash() {
        let escaped = escape_regex(r"\d+");
        assert_eq!(escaped, r"\\d\+");
    }

    #[test]
    fn test_escape_regex_no_special() {
        let escaped = escape_regex("hello");
        assert_eq!(escaped, "hello");
    }

    #[test]
    fn test_is_valid_regex_valid() {
        assert!(is_valid_regex(r"\d+"));
        assert!(is_valid_regex(r"[a-z]+"));
        // Note: lookahead assertions like (?=...) require regex crate with Unicode support
        // which may not be available in all configurations
    }

    #[test]
    fn test_is_valid_regex_invalid() {
        assert!(!is_valid_regex(r"[\d+"));
        assert!(!is_valid_regex(r"(unclosed"));
        assert!(!is_valid_regex(r"[z-a]"));
    }
}

// ============================================================================
// Pattern Constant Tests (skip - patterns module is internal)
// ============================================================================
// Note: Pattern constants are tested indirectly through validation functions

// ============================================================================
// Edge Case Tests
// ============================================================================

mod edge_cases {
    use super::*;

    #[test]
    fn test_empty_string_validation() {
        assert!(!is_email(""));
        assert!(!is_ipv4(""));
        assert!(!is_url(""));
        assert!(!is_phone(""));
        assert!(!is_date(""));
        assert!(!is_time(""));
        assert!(!is_uuid(""));
        assert!(!is_username(""));
        assert!(!is_strong_password(""));
    }

    #[test]
    fn test_empty_string_extraction() {
        assert!(extract_all(r"\d+", "").is_empty());
        assert!(extract_numbers("").is_empty());
        assert!(extract_emails("").is_empty());
        assert!(extract_urls("").is_empty());
    }

    #[test]
    fn test_empty_string_replacement() {
        assert_eq!(replace_all(r"\d+", "", "X"), "");
        assert_eq!(replace_first(r"\d+", "", "X"), "");
        assert_eq!(remove_all(r"\d+", ""), "");
    }

    #[test]
    fn test_unicode_handling() {
        // Unicode emails may not be supported by basic regex pattern
        let emails = extract_emails("联系 user@example.com 或 admin@test.cn");
        assert!(emails.contains(&"user@example.com".to_string()));
        assert!(emails.contains(&"admin@test.cn".to_string()));
    }

    #[test]
    fn test_very_long_string() {
        let long_text = "a".repeat(10000) + "123" + &"b".repeat(10000);
        let numbers = extract_numbers(&long_text);
        assert_eq!(numbers, vec!["123"]);
    }

    #[test]
    fn test_overlapping_patterns() {
        let text = "aaa";
        let matches = extract_all(r"aa", text);
        // Regex finds non-overlapping matches
        assert_eq!(matches, vec!["aa"]);
    }

    #[test]
    fn test_greedy_vs_non_greedy() {
        let html = "<div>content1</div><div>content2</div>";
        // Greedy match
        let greedy = extract_all(r"<div>.*</div>", html);
        assert_eq!(greedy.len(), 1);
        
        // Non-greedy match
        let non_greedy = extract_all(r"<div>.*?</div>", html);
        assert_eq!(non_greedy.len(), 2);
    }
}

// ============================================================================
// Performance Tests (not run by default)
// ============================================================================

#[cfg(test)]
mod performance {
    use super::*;
    use std::time::Instant;

    #[test]
    #[ignore] // Run with: cargo test --test regex_utils_test -- --ignored
    fn test_validation_performance() {
        let email = "user@example.com";
        let start = Instant::now();
        
        for _ in 0..10000 {
            let _ = is_email(email);
        }
        
        let duration = start.elapsed();
        println!("10000 email validations: {:?}", duration);
        assert!(duration.as_millis() < 1000, "Validation should be fast");
    }

    #[test]
    #[ignore]
    fn test_extraction_performance() {
        let text = "Contact: user1@example.com, user2@test.org, user3@domain.net";
        let start = Instant::now();
        
        for _ in 0..10000 {
            let _ = extract_emails(text);
        }
        
        let duration = start.elapsed();
        println!("10000 email extractions: {:?}", duration);
        assert!(duration.as_millis() < 5000, "Extraction should be reasonable");
    }
}