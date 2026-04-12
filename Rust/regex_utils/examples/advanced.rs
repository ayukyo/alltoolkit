//! # Advanced Regex Utils Examples
//!
//! Demonstrates advanced usage patterns for data processing and validation.
//! Run with: cargo run --example advanced

use regex_utils::{
    is_email, is_china_phone, is_strong_password,
    extract_emails, extract_china_phones, extract_captures,
    extract_named_captures, strip_html, normalize_whitespace,
    count_matches, contains_pattern,
};

/// Example: Process user registration data
fn process_registration(name: &str, email: &str, phone: &str, password: &str) -> Result<(), String> {
    println!("Processing registration for: {}", name);
    
    // Validate email
    if !is_email(email) {
        return Err(format!("Invalid email: {}", email));
    }
    println!("  ✓ Email valid: {}", email);
    
    // Validate phone (China format)
    if !is_china_phone(phone) {
        return Err(format!("Invalid phone: {}", phone));
    }
    println!("  ✓ Phone valid: {}", phone);
    
    // Validate password strength
    if !is_strong_password(password) {
        return Err("Password too weak. Requirements: 8+ chars, uppercase, lowercase, digit, special char".to_string());
    }
    println!("  ✓ Password strength OK");
    
    Ok(())
}

/// Example: Extract contact info from HTML page
fn extract_contact_info(html: &str) -> ContactInfo {
    // Remove HTML tags
    let text = strip_html(html);
    let text = normalize_whitespace(&text);
    
    // Extract emails and phones
    let emails = extract_emails(&text);
    let phones = extract_china_phones(&text);
    
    ContactInfo {
        emails,
        phones,
        raw_text: text,
    }
}

struct ContactInfo {
    emails: Vec<String>,
    phones: Vec<String>,
    raw_text: String,
}

/// Example: Parse log entries
fn parse_log_entries(log_text: &str) -> Vec<LogEntry> {
    let pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(?P<level>\w+)\] (?P<message>.+)";
    
    extract_captures(pattern, log_text)
        .into_iter()
        .map(|captures| {
            LogEntry {
                timestamp: captures[0].clone(),
                level: captures[1].clone(),
                message: captures[2].clone(),
            }
        })
        .collect()
}

struct LogEntry {
    timestamp: String,
    level: String,
    message: String,
}

/// Example: Validate and clean user input batch
fn validate_input_batch(inputs: Vec<&str>) -> ValidationResult {
    let mut valid = Vec::new();
    let mut invalid = Vec::new();
    
    for input in inputs {
        if contains_pattern(r"^\w+@\w+\.\w+$", input) && is_email(input) {
            valid.push(input.to_string());
        } else {
            invalid.push(input.to_string());
        }
    }
    
    ValidationResult { valid, invalid }
}

struct ValidationResult {
    valid: Vec<String>,
    invalid: Vec<String>,
}

fn main() {
    println!("🔍 Advanced Regex Utils Examples\n");

    // Example 1: User Registration
    println!("📝 Example 1: User Registration Validation");
    println!("{}", "─".repeat(50));
    
    let registrations = vec![
        ("Alice", "alice@example.com", "13812345678", "SecureP@ss1"),
        ("Bob", "invalid-email", "13812345678", "weak"),
        ("Carol", "carol@test.org", "12345", "Str0ng!Pass"),
    ];
    
    for (name, email, phone, password) in registrations {
        match process_registration(name, email, phone, password) {
            Ok(_) => println!("  ✅ Registration successful for {}\n", name),
            Err(e) => println!("  ❌ Registration failed: {}\n", e),
        }
    }

    // Example 2: Extract Contact Info from HTML
    println!("\n📄 Example 2: Extract Contact Info from HTML");
    println!("{}", "─".repeat(50));
    
    let html = r#"
        <div class="contact">
            <h1>Contact Us</h1>
            <p>Email: support@example.com or sales@company.org</p>
            <p>Phone: 13812345678 or 19987654321</p>
            <p>Address: 北京市朝阳区</p>
        </div>
    "#;
    
    let contact = extract_contact_info(html);
    println!("  Extracted from HTML:");
    println!("  Emails: {:?}", contact.emails);
    println!("  Phones: {:?}", contact.phones);

    // Example 3: Parse Log Entries
    println!("\n📋 Example 3: Parse Log Entries");
    println!("{}", "─".repeat(50));
    
    let log_text = r#"
        2024-06-15 10:30:00 [INFO] Application started
        2024-06-15 10:30:05 [DEBUG] Loading configuration
        2024-06-15 10:30:10 [ERROR] Database connection failed
        2024-06-15 10:30:15 [WARN] Retrying connection
        2024-06-15 10:30:20 [INFO] Connection established
    "#;
    
    let entries = parse_log_entries(log_text);
    println!("  Parsed {} log entries:", entries.len());
    for entry in entries {
        println!("  [{}] {} - {}", entry.level, entry.timestamp, entry.message);
    }

    // Example 4: Batch Input Validation
    println!("\n📊 Example 4: Batch Input Validation");
    println!("{}", "─".repeat(50));
    
    let inputs = vec![
        "user@example.com",
        "invalid",
        "admin@test.org",
        "@bad.com",
        "test@domain.net",
    ];
    
    let result = validate_input_batch(inputs);
    println!("  Valid inputs ({}):", result.valid.len());
    for v in &result.valid {
        println!("    ✓ {}", v);
    }
    println!("  Invalid inputs ({}):", result.invalid.len());
    for i in &result.invalid {
        println!("    ✗ {}", i);
    }

    // Example 5: Count Pattern Occurrences
    println!("\n🔢 Example 5: Count Pattern Occurrences");
    println!("{}", "─".repeat(50));
    
    let text = "Error: Connection timeout. Error: Database unavailable. Error: Network issue.";
    let error_count = count_matches(r"Error:", text);
    println!("  Text: {}", text);
    println!("  Error count: {}", error_count);

    // Example 6: Named Capture Groups
    println!("\n🏷️ Example 6: Named Capture Groups");
    println!("{}", "─".repeat(50));
    
    let query = "name=John&age=30&city=Beijing";
    let data = extract_named_captures(r"(?P<key>\w+)=(?P<value>\w+)", query);
    
    println!("  Query string: {}", query);
    println!("  Parsed parameters:");
    for (key, value) in &data {
        println!("    {} = {}", key, value);
    }

    println!("\n✅ All advanced examples completed!");
}
