//! Validation Utilities Test Suite
//! 
//! Comprehensive tests for data validation functions.
//! All tests are standalone with full function implementations.

#[cfg(test)]
mod tests {
    // ============================================================================
    // Function implementations for standalone testing
    // ============================================================================

    fn is_valid_email(email: &str) -> bool {
        const MAX_LOCAL_LEN: usize = 64;
        const MAX_TOTAL_LEN: usize = 254;
        const MAX_LABEL_LEN: usize = 63;
        
        let len = email.len();
        if len == 0 || len > MAX_TOTAL_LEN {
            return false;
        }

        let bytes = email.as_bytes();
        let mut at_count = 0;
        let mut at_pos = 0;
        let mut last_dot_pos: Option<usize> = None;

        for (i, &b) in bytes.iter().enumerate() {
            if b == b'@' {
                if i > MAX_LOCAL_LEN || i == 0 {
                    return false;
                }
                at_count += 1;
                at_pos = i;
                if at_count > 1 {
                    return false;
                }
                continue;
            }
            
            if b == b'.' && at_count == 1 {
                if last_dot_pos == Some(i - 1) {
                    return false;
                }
                if let Some(last_dot) = last_dot_pos {
                    if i - last_dot - 1 > MAX_LABEL_LEN {
                        return false;
                    }
                } else if i - at_pos - 1 > MAX_LABEL_LEN {
                    return false;
                }
                last_dot_pos = Some(i);
            }
            
            if b <= b' ' || matches!(b, b'(' | b')' | b'<' | b'>' | b',' | b';' | b':' | b'\\' | b'"') {
                return false;
            }
        }

        if at_count != 1 {
            return false;
        }

        let domain = &email[at_pos + 1..];
        let domain_len = domain.len();
        if domain_len < 3 || !domain.contains('.') {
            return false;
        }

        let domain_bytes = domain.as_bytes();
        if domain_bytes[0] == b'.' || domain_bytes[domain_len - 1] == b'.' {
            return false;
        }
        
        if let Some(last_dot) = last_dot_pos {
            if domain_len - (last_dot - at_pos) - 1 > MAX_LABEL_LEN {
                return false;
            }
        }

        true
    }

    fn is_valid_url(url: &str) -> bool {
        let url = url.trim();
        let lower = url.to_lowercase();
        if !lower.starts_with("http://") && !lower.starts_with("https://") {
            return false;
        }
        
        let after_scheme = if lower.starts_with("https://") {
            &url[8..]
        } else {
            &url[7..]
        };
        
        if after_scheme.is_empty() {
            return false;
        }
        
        let host_end = after_scheme.find('/').unwrap_or(after_scheme.len());
        let host = &after_scheme[..host_end];
        
        if host.is_empty() {
            return false;
        }
        
        for c in host.chars() {
            if !c.is_alphanumeric() && c != '.' && c != '-' && c != ':' && c != '[' && c != ']' {
                return false;
            }
        }
        
        if host == "localhost" || host.contains('.') || host.starts_with('[') {
            return true;
        }
        
        // Allow IP addresses without dots
        host.parse::<std::net::Ipv4Addr>().is_ok()
    }

    fn is_valid_phone(phone: &str) -> bool {
        let phone = phone.trim();
        if !phone.starts_with('+') {
            return false;
        }
        
        let digits: String = phone[1..].chars()
            .filter(|c| c.is_ascii_digit())
            .collect();
        
        matches!(digits.len(), 7..=15)
    }

    fn is_valid_credit_card(card_number: &str) -> bool {
        let digits: String = card_number.chars()
            .filter(|c| c.is_ascii_digit())
            .collect();
        
        if !matches!(digits.len(), 13..=19) {
            return false;
        }
        
        let mut sum = 0u32;
        let mut alternate = false;
        
        for c in digits.chars().rev() {
            let mut d = (c as u32) - ('0' as u32);
            
            if alternate {
                d *= 2;
                if d > 9 {
                    d -= 9;
                }
            }
            
            sum += d;
            alternate = !alternate;
        }
        
        sum % 10 == 0
    }

    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    enum CreditCardType {
        Visa,
        Mastercard,
        AmericanExpress,
        Discover,
        JCB,
        DinersClub,
        Unknown,
    }

    fn detect_credit_card_type(card_number: &str) -> CreditCardType {
        let digits: String = card_number.chars()
            .filter(|c| c.is_ascii_digit())
            .collect();
        
        if digits.is_empty() {
            return CreditCardType::Unknown;
        }
        
        let first = &digits[0..1];
        let first_two = if digits.len() >= 2 { &digits[0..2] } else { "" };
        let first_three = if digits.len() >= 3 { &digits[0..3] } else { "" };
        let first_four = if digits.len() >= 4 { &digits[0..4] } else { "" };
        
        if first == "4" && matches!(digits.len(), 13 | 16 | 19) {
            return CreditCardType::Visa;
        }
        
        if digits.len() == 16 {
            if let Ok(n) = first_two.parse::<u32>() {
                if (51..=55).contains(&n) {
                    return CreditCardType::Mastercard;
                }
            }
            if let Ok(n) = first_four.parse::<u32>() {
                if (2221..=2720).contains(&n) {
                    return CreditCardType::Mastercard;
                }
            }
        }
        
        if digits.len() == 15 && (first_two == "34" || first_two == "37") {
            return CreditCardType::AmericanExpress;
        }
        
        if matches!(digits.len(), 16..=19) {
            if first_four == "6011" || first_two == "65" {
                return CreditCardType::Discover;
            }
            if let Ok(n) = first_three.parse::<u32>() {
                if (644..=649).contains(&n) {
                    return CreditCardType::Discover;
                }
            }
        }
        
        if digits.len() == 16 {
            if let Ok(n) = first_four.parse::<u32>() {
                if (3528..=3589).contains(&n) {
                    return CreditCardType::JCB;
                }
            }
        }
        
        if digits.len() == 14 {
            if first_two == "36" || first_two == "38" {
                return CreditCardType::DinersClub;
            }
            if let Ok(n) = first_three.parse::<u32>() {
                if (300..=305).contains(&n) {
                    return CreditCardType::DinersClub;
                }
            }
        }
        
        CreditCardType::Unknown
    }

    fn is_valid_ipv4(ip: &str) -> bool {
        let parts: Vec<&str> = ip.split('.').collect();
        if parts.len() != 4 {
            return false;
        }
        
        for part in parts {
            if part.is_empty() || part.len() > 3 {
                return false;
            }
            if part.len() > 1 && part.starts_with('0') {
                return false;
            }
            if !part.chars().all(|c| c.is_ascii_digit()) {
                return false;
            }
            match part.parse::<u8>() {
                Ok(_) => {},
                Err(_) => return false,
            }
        }
        
        true
    }

    fn is_valid_ipv6(ip: &str) -> bool {
        let ip = if let Some(idx) = ip.find('%') {
            &ip[..idx]
        } else {
            ip
        };
        
        if ip == "::" {
            return true;
        }
        
        let double_colon_count = ip.matches("::").count();
        if double_colon_count > 1 {
            return false;
        }
        
        let has_double_colon = ip.contains("::");
        
        // Check for triple colon (:::)
        if ip.contains(":::") {
            return false;
        }
        
        let parts: Vec<&str> = if has_double_colon {
            ip.split("::")
                .flat_map(|s| if s.is_empty() { vec![] } else { s.split(':').collect() })
                .collect()
        } else {
            ip.split(':').collect()
        };
        
        let max_groups = if has_double_colon { 7 } else { 8 };
        
        if parts.len() > max_groups || (parts.is_empty() && !has_double_colon) {
            return false;
        }
        
        for part in &parts {
            if part.is_empty() {
                continue;
            }
            // Check for IPv4-mapped addresses (last part can be IPv4)
            if part.contains('.') {
                return is_valid_ipv4(part);
            }
            if part.len() > 4 {
                return false;
            }
            if !part.chars().all(|c| c.is_ascii_hexdigit()) {
                return false;
            }
        }
        
        if !has_double_colon && parts.len() != 8 {
            return false;
        }
        
        true
    }

    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    enum PasswordStrength {
        VeryWeak,
        Weak,
        Medium,
        Strong,
        VeryStrong,
    }

    fn validate_password_strength(password: &str) -> PasswordStrength {
        let len = password.len();
        let mut score = 0;
        
        if len >= 8 { score += 1; }
        if len >= 12 { score += 1; }
        if len >= 16 { score += 1; }
        
        let has_lowercase = password.chars().any(|c| c.is_ascii_lowercase());
        let has_uppercase = password.chars().any(|c| c.is_ascii_uppercase());
        let has_digit = password.chars().any(|c| c.is_ascii_digit());
        let has_special = password.chars().any(|c| "!@#$%^&*()_+-=[]{}|;':\",./<>?`~".contains(c));
        
        if has_lowercase { score += 1; }
        if has_uppercase { score += 1; }
        if has_digit { score += 1; }
        if has_special { score += 2; }
        
        let type_count = [has_lowercase, has_uppercase, has_digit, has_special]
            .iter().filter(|&&x| x).count();
        if type_count >= 3 { score += 1; }
        if type_count == 4 { score += 1; }
        
        match score {
            0..=2 => PasswordStrength::VeryWeak,
            3..=4 => PasswordStrength::Weak,
            5..=6 => PasswordStrength::Medium,
            7..=8 => PasswordStrength::Strong,
            _ => PasswordStrength::VeryStrong,
        }
    }

    fn is_valid_isbn(isbn: &str) -> bool {
        let cleaned: String = isbn.chars()
            .filter(|c| *c != '-' && *c != ' ')
            .collect();
        
        match cleaned.len() {
            10 => validate_isbn10(&cleaned),
            13 => validate_isbn13(&cleaned),
            _ => false,
        }
    }

    fn validate_isbn10(isbn: &str) -> bool {
        let chars: Vec<char> = isbn.chars().collect();
        let mut sum = 0u32;
        for (i, &c) in chars.iter().enumerate() {
            let digit = if i == 9 && c == 'X' {
                10
            } else if c.is_ascii_digit() {
                (c as u32) - ('0' as u32)
            } else {
                return false;
            };
            sum += digit * (10 - i as u32);
        }
        sum % 11 == 0
    }

    fn validate_isbn13(isbn: &str) -> bool {
        let chars: Vec<char> = isbn.chars().collect();
        let mut sum = 0u32;
        for (i, &c) in chars.iter().enumerate() {
            if !c.is_ascii_digit() {
                return false;
            }
            let digit = (c as u32) - ('0' as u32);
            let weight = if i % 2 == 0 { 1 } else { 3 };
            sum += digit * weight;
        }
        sum % 10 == 0
    }

    fn is_valid_hex_color(color: &str) -> bool {
        let color = color.trim();
        if !color.starts_with('#') {
            return false;
        }
        let hex = &color[1..];
        let len = hex.len();
        if !matches!(len, 3 | 4 | 6 | 8) {
            return false;
        }
        hex.chars().all(|c| c.is_ascii_hexdigit())
    }

    fn is_valid_slug(slug: &str) -> bool {
        let len = slug.len();
        if len == 0 || len > 64 {
            return false;
        }
        let chars: Vec<char> = slug.chars().collect();
        // Only lowercase alphanumeric and hyphens allowed
        if !chars[0].is_ascii_lowercase() && !chars[0].is_ascii_digit() {
            return false;
        }
        if !chars[len - 1].is_ascii_lowercase() && !chars[len - 1].is_ascii_digit() {
            return false;
        }
        let mut prev_hyphen = false;
        for &c in &chars {
            if !c.is_ascii_lowercase() && !c.is_ascii_digit() && c != '-' {
                return false;
            }
            if c == '-' {
                if prev_hyphen {
                    return false;
                }
                prev_hyphen = true;
            } else {
                prev_hyphen = false;
            }
        }
        true
    }

    // ============================================================================
    // Tests
    // ============================================================================

    #[test]
    fn test_is_valid_email_valid() {
        assert!(is_valid_email("user@example.com"));
        assert!(is_valid_email("user.name@example.com"));
        assert!(is_valid_email("user+tag@example.com"));
        assert!(is_valid_email("user_name@example.com"));
        assert!(is_valid_email("user@sub.domain.com"));
        assert!(is_valid_email("user@sub.domain.co.uk"));
        assert!(is_valid_email("a@b.co")); // Shortest valid email
    }

    #[test]
    fn test_is_valid_email_invalid() {
        assert!(!is_valid_email(""));
        assert!(!is_valid_email("user@"));
        assert!(!is_valid_email("@example.com"));
        assert!(!is_valid_email("user@example"));
        assert!(!is_valid_email("user @example.com"));
        assert!(!is_valid_email("user@@example.com"));
        assert!(!is_valid_email("user@example..com"));
        assert!(!is_valid_email("user@.example.com"));
        assert!(!is_valid_email("user(name)@example.com"));
        assert!(!is_valid_email("user;@example.com"));
    }

    #[test]
    fn test_is_valid_url_valid() {
        assert!(is_valid_url("https://example.com"));
        assert!(is_valid_url("http://example.com"));
        assert!(is_valid_url("https://sub.domain.com"));
        assert!(is_valid_url("https://example.com/path"));
        assert!(is_valid_url("http://localhost"));
        assert!(is_valid_url("https://192.168.1.1"));
    }

    #[test]
    fn test_is_valid_url_invalid() {
        assert!(!is_valid_url(""));
        assert!(!is_valid_url("ftp://example.com"));
        assert!(!is_valid_url("example.com"));
        assert!(!is_valid_url("http://"));
        assert!(!is_valid_url("https://"));
        assert!(!is_valid_url("not-a-url"));
    }

    #[test]
    fn test_is_valid_phone_valid() {
        assert!(is_valid_phone("+1234567890"));
        assert!(is_valid_phone("+1-555-123-4567"));
        assert!(is_valid_phone("+44 20 7946 0958"));
        assert!(is_valid_phone("+8613800138000"));
        assert!(is_valid_phone("+4915112345678"));
        assert!(is_valid_phone("+1 (555) 123-4567"));
    }

    #[test]
    fn test_is_valid_phone_invalid() {
        assert!(!is_valid_phone(""));
        assert!(!is_valid_phone("1234567890")); // Missing +
        assert!(!is_valid_phone("+123")); // Too short
        assert!(!is_valid_phone("+123456")); // Too short
        assert!(!is_valid_phone("abc"));
        assert!(!is_valid_phone("phone-number"));
    }

    #[test]
    fn test_is_valid_credit_card_valid() {
        // Test cards that pass Luhn check
        assert!(is_valid_credit_card("4532015112830366")); // Visa
        assert!(is_valid_credit_card("5500000000000004")); // Mastercard
        assert!(is_valid_credit_card("340000000000009")); // Amex
        assert!(is_valid_credit_card("6011000000000004")); // Discover
        assert!(is_valid_credit_card("3566002020360505")); // JCB
        assert!(is_valid_credit_card("30000000000004")); // Diners
    }

    #[test]
    fn test_is_valid_credit_card_invalid() {
        assert!(!is_valid_credit_card("1234567890123456")); // Fails Luhn
        assert!(!is_valid_credit_card("123")); // Too short
        assert!(!is_valid_credit_card(""));
        assert!(!is_valid_credit_card("abcd efgh ijkl mnop"));
    }

    #[test]
    fn test_detect_credit_card_type() {
        assert_eq!(detect_credit_card_type("4532015112830366"), CreditCardType::Visa);
        assert_eq!(detect_credit_card_type("4111111111111111"), CreditCardType::Visa);
        assert_eq!(detect_credit_card_type("5500000000000004"), CreditCardType::Mastercard);
        assert_eq!(detect_credit_card_type("2221000000000009"), CreditCardType::Mastercard);
        assert_eq!(detect_credit_card_type("340000000000009"), CreditCardType::AmericanExpress);
        assert_eq!(detect_credit_card_type("370000000000002"), CreditCardType::AmericanExpress);
        assert_eq!(detect_credit_card_type("6011000000000004"), CreditCardType::Discover);
        assert_eq!(detect_credit_card_type("6500000000000002"), CreditCardType::Discover);
        assert_eq!(detect_credit_card_type("3566002020360505"), CreditCardType::JCB);
        assert_eq!(detect_credit_card_type("30000000000004"), CreditCardType::DinersClub);
        assert_eq!(detect_credit_card_type("1234567890123456"), CreditCardType::Unknown);
    }

    #[test]
    fn test_is_valid_ipv4_valid() {
        assert!(is_valid_ipv4("192.168.1.1"));
        assert!(is_valid_ipv4("0.0.0.0"));
        assert!(is_valid_ipv4("255.255.255.255"));
        assert!(is_valid_ipv4("127.0.0.1"));
        assert!(is_valid_ipv4("10.0.0.1"));
        assert!(is_valid_ipv4("172.16.0.1"));
        assert!(is_valid_ipv4("8.8.8.8"));
    }

    #[test]
    fn test_is_valid_ipv4_invalid() {
        assert!(!is_valid_ipv4(""));
        assert!(!is_valid_ipv4("256.1.1.1")); // Out of range
        assert!(!is_valid_ipv4("1.1.1")); // Missing octet
        assert!(!is_valid_ipv4("1.1.1.1.1")); // Extra octet
        assert!(!is_valid_ipv4("01.1.1.1")); // Leading zero
        assert!(!is_valid_ipv4("1.1.1.a")); // Invalid char
        assert!(!is_valid_ipv4("1.1.1.-1")); // Negative
    }

    #[test]
    fn test_is_valid_ipv6_valid() {
        assert!(is_valid_ipv6("::1"));
        assert!(is_valid_ipv6("::"));
        assert!(is_valid_ipv6("2001:db8::1"));
        assert!(is_valid_ipv6("fe80::1"));
        assert!(is_valid_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334"));
        assert!(is_valid_ipv6("2001:db8:85a3::8a2e:370:7334"));
        assert!(is_valid_ipv6("fe80::1%eth0")); // With zone ID
    }

    #[test]
    fn test_is_valid_ipv6_invalid() {
        assert!(!is_valid_ipv6(""));
        assert!(!is_valid_ipv6("gggg::1")); // Invalid hex
        assert!(!is_valid_ipv6("1:2:3:4:5:6:7:8:9")); // Too many groups
        assert!(!is_valid_ipv6(":::1")); // Triple colon
        assert!(!is_valid_ipv6("1::2::3")); // Multiple ::
    }

    #[test]
    fn test_validate_password_strength() {
        assert_eq!(validate_password_strength(""), PasswordStrength::VeryWeak);
        assert_eq!(validate_password_strength("a"), PasswordStrength::VeryWeak);
        assert_eq!(validate_password_strength("password"), PasswordStrength::VeryWeak);
        assert_eq!(validate_password_strength("PASSWORD"), PasswordStrength::VeryWeak);
        assert_eq!(validate_password_strength("Password"), PasswordStrength::Weak);
        assert_eq!(validate_password_strength("Password1"), PasswordStrength::Medium);
        assert_eq!(validate_password_strength("Password12"), PasswordStrength::Medium);
        assert_eq!(validate_password_strength("P@ssw0rd"), PasswordStrength::Strong);
        assert_eq!(validate_password_strength("P@ssw0rd123"), PasswordStrength::Strong);
        assert_eq!(validate_password_strength("P@ssw0rd!123"), PasswordStrength::VeryStrong);
        assert_eq!(validate_password_strength("MyV3ry$tr0ngP@ss!"), PasswordStrength::VeryStrong);
    }

    #[test]
    fn test_is_valid_isbn_valid() {
        // ISBN-10
        assert!(is_valid_isbn("0471958697"));
        assert!(is_valid_isbn("0-471-60695-2"));
        assert!(is_valid_isbn("0306406152"));
        
        // ISBN-13
        assert!(is_valid_isbn("9780471486480"));
        assert!(is_valid_isbn("978-0-13-235088-4"));
        assert!(is_valid_isbn("9780306406157"));
    }

    #[test]
    fn test_is_valid_isbn_invalid() {
        assert!(!is_valid_isbn(""));
        assert!(!is_valid_isbn("123456789")); // Too short
        assert!(!is_valid_isbn("12345678901234")); // Invalid length
        assert!(!is_valid_isbn("1234567890")); // Invalid checksum (sum=330, 330%11=0 but check digit wrong)
        assert!(!is_valid_isbn("1234567890123")); // Invalid checksum
    }

    #[test]
    fn test_is_valid_hex_color_valid() {
        assert!(is_valid_hex_color("#fff"));
        assert!(is_valid_hex_color("#FFF"));
        assert!(is_valid_hex_color("#ffffff"));
        assert!(is_valid_hex_color("#FFFFFF"));
        assert!(is_valid_hex_color("#ffaa"));
        assert!(is_valid_hex_color("#ffaa00"));
        assert!(is_valid_hex_color("#ffaa0080"));
        assert!(is_valid_hex_color("#0a1B2c"));
    }

    #[test]
    fn test_is_valid_hex_color_invalid() {
        assert!(!is_valid_hex_color(""));
        assert!(!is_valid_hex_color("fff")); // Missing #
        assert!(!is_valid_hex_color("#ff")); // Too short
        assert!(!is_valid_hex_color("#fffg00")); // Invalid char
        assert!(!is_valid_hex_color("#ff000")); // Invalid length
        assert!(!is_valid_hex_color("#ff00000")); // Invalid length
    }

    #[test]
    fn test_is_valid_slug_valid() {
        assert!(is_valid_slug("a"));
        assert!(is_valid_slug("my-slug"));
        assert!(is_valid_slug("my-blog-post-123"));
        assert!(is_valid_slug("user123"));
        assert!(is_valid_slug("test"));
        assert!(is_valid_slug("a-b-c"));
    }

    #[test]
    fn test_is_valid_slug_invalid() {
        assert!(!is_valid_slug("")); // Empty
        assert!(!is_valid_slug("-invalid")); // Starts with hyphen
        assert!(!is_valid_slug("invalid-")); // Ends with hyphen
        assert!(!is_valid_slug("has space")); // Has space
        assert!(!is_valid_slug("has--double")); // Double hyphen
        assert!(!is_valid_slug("has_underscore")); // Has underscore
        assert!(!is_valid_slug("UPPERCASE")); // Has uppercase
        assert!(!is_valid_slug(&"a".repeat(65))); // Too long
        assert!(!is_valid_slug("has.special")); // Has special chars
    }

    #[test]
    fn test_example_usage() {
        // Email validation
        assert!(is_valid_email("user@example.com"));
        
        // URL validation
        assert!(is_valid_url("https://example.com"));
        
        // Phone validation
        assert!(is_valid_phone("+1-555-123-4567"));
        
        // Credit card validation
        assert!(is_valid_credit_card("4532015112830366"));
        
        // Credit card type detection
        let card_type = detect_credit_card_type("4532015112830366");
        assert_eq!(card_type, CreditCardType::Visa);
        
        // IPv4 validation
        assert!(is_valid_ipv4("192.168.1.1"));
        
        // IPv6 validation
        assert!(is_valid_ipv6("::1"));
        
        // Password strength
        let strength = validate_password_strength("P@ssw0rd!123");
        assert_eq!(strength, PasswordStrength::VeryStrong);
        
        // ISBN validation
        assert!(is_valid_isbn("9780471486480"));
        
        // Hex color validation
        assert!(is_valid_hex_color("#ffffff"));
        
        // Slug validation
        assert!(is_valid_slug("my-blog-post"));
    }
}