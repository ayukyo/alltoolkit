//! JSON Utilities Example
//!
//! Demonstrates various use cases for the JSON parsing and generation module.

use std::collections::HashMap;

// Include the module
#[path = "../json_utils/mod.rs"]
mod json_utils;

use json_utils::*;

fn main() {
    println!("========================================");
    println!("JSON Utilities Example");
    println!("========================================\n");

    // Example 1: Parse JSON string
    println!("1. Parse JSON string");
    println!("--------------------");
    let json_str = r#"
    {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com",
        "isActive": true,
        "balance": 1234.56
    }
    "#;

    match parse_json(json_str) {
        Ok(user) => {
            println!("Name: {}", user.get("name").as_string());
            println!("Age: {}", user.get("age").as_i64());
            println!("Email: {}", user.get("email").as_string());
            println!("Active: {}", user.get("isActive").as_bool());
            println!("Balance: ${:.2}", user.get("balance").as_f64());
        }
        Err(e) => println!("Parse error: {}", e),
    }
    println!();

    // Example 2: Parse JSON array
    println!("2. Parse JSON array");
    println!("-------------------");
    let json_array = r#"["apple", "banana", "cherry"]"#;

    match parse_json(json_array) {
        Ok(fruits) => {
            println!("Fruits:");
            for i in 0..fruits.len() {
                println!("  [{}] {}", i, fruits.get_index(i).as_string());
            }
        }
        Err(e) => println!("Parse error: {}", e),
    }
    println!();

    // Example 3: Parse nested objects
    println!("3. Parse nested objects");
    println!("-----------------------");
    let nested_json = r#"
    {
        "user": {
            "name": "Alice",
            "address": {
                "city": "New York",
                "zipcode": "10001"
            }
        }
    }
    "#;

    match parse_json(nested_json) {
        Ok(data) => {
            println!("User name: {}", data.get("user").get("name").as_string());
            println!("City: {}", data.get("user").get("address").get("city").as_string());
            println!("Zipcode: {}", data.get("user").get("address").get("zipcode").as_string());
        }
        Err(e) => println!("Parse error: {}", e),
    }
    println!();

    // Example 4: Create JSON programmatically
    println!("4. Create JSON programmatically");
    println!("--------------------------------");
    let mut user = HashMap::new();
    user.insert("id".to_string(), JsonValue::number(1.0));
    user.insert("username".to_string(), JsonValue::string("alice"));
    user.insert("email".to_string(), JsonValue::string("alice@example.com"));
    user.insert("verified".to_string(), JsonValue::bool(true));

    let mut user_obj = JsonValue::object(user);
    println!("Compact JSON:");
    println!("{}", user_obj.to_json());
    println!();

    // Example 5: Pretty print JSON
    println!("5. Pretty print JSON");
    println!("--------------------");
    println!("Pretty JSON:");
    println!("{}", user_obj.to_pretty_json());
    println!();

    // Example 6: Create JSON array
    println!("6. Create JSON array");
    println!("--------------------");
    let mut items = Vec::new();
    for i in 1..=3 {
        let mut item = HashMap::new();
        item.insert("id".to_string(), JsonValue::number(i as f64));
        item.insert("name".to_string(), JsonValue::string(format!("Item {}", i)));
        items.push(JsonValue::object(item));
    }
    let array = JsonValue::array(items);
    println!("{}", array.to_pretty_json());
    println!();

    // Example 7: Type checking and safe access
    println!("7. Type checking and safe access");
    println!("---------------------------------");
    let mixed = parse_json(r#"[1, "two", true, null, 3.14]"#).unwrap();

    for i in 0..mixed.len() {
        let item = mixed.get_index(i);
        print!("[{}] ", i);
        if item.is_null() {
            println!("null");
        } else if item.is_bool() {
            println!("boolean: {}", item.as_bool());
        } else if item.is_number() {
            println!("number: {}", item.as_f64());
        } else if item.is_string() {
            println!("string: {}", item.as_string());
        }
    }
    println!();

    // Example 8: Default values
    println!("8. Default values");
    println!("-----------------");
    let config = parse_json(r#"{"timeout": 30}"#).unwrap();

    let timeout = config.get("timeout").as_i64_or(60);
    let retries = config.get("retries").as_i64_or(3);
    let enabled = config.get("enabled").as_bool_or(true);
    let name = config.get("name").as_string_or("default");

    println!("timeout: {} (from JSON)", timeout);
    println!("retries: {} (default)", retries);
    println!("enabled: {} (default)", enabled);
    println!("name: {} (default)", name);
    println!();

    // Example 9: Check if key exists
    println!("9. Check if key exists");
    println!("----------------------");
    let data = parse_json(r#"{"a": 1, "b": 2}"#).unwrap();
    println!("Has 'a': {}", data.has("a"));
    println!("Has 'c': {}", data.has("c"));
    println!();

    // Example 10: Get all keys
    println!("10. Get all keys");
    println!("----------------");
    let keys = data.keys();
    println!("Keys: {:?}", keys);
    println!();

    // Example 11: Merge objects
    println!("11. Merge objects");
    println!("-----------------");
    let mut obj1 = parse_json(r#"{"name": "John", "age": 30}"#).unwrap();
    let obj2 = parse_json(r#"{"city": "New York", "country": "USA"}"#).unwrap();

    println!("Before merge:");
    println!("{}", obj1.to_pretty_json());

    obj1.merge(&obj2);

    println!("\nAfter merge:");
    println!("{}", obj1.to_pretty_json());
    println!();

    // Example 12: Validate JSON
    println!("12. Validate JSON");
    println!("-----------------");
    let valid = r#"{"valid": true}"#;
    let invalid = r#"{invalid json}"#;

    println!("'{}' is valid: {}", valid, is_valid_json(valid));
    println!("'{}' is valid: {}", invalid, is_valid_json(invalid));
    println!();

    // Example 13: Error handling
    println!("13. Error handling");
    println!("------------------");
    match parse_json("{invalid}") {
        Ok(_) => println!("Unexpected success"),
        Err(e) => println!("Expected error: {}", e),
    }

    // Using parse_json_or_null for safe parsing
    let result = parse_json_or_null("{invalid}");
    println!("Safe parse result is null: {}", result.is_null());
    println!();

    // Example 14: Working with Option types
    println!("14. Working with Option types");
    println!("-----------------------------");
    let some_value: Option<i32> = Some(42);
    let none_value: Option<i32> = None;

    let json_some: JsonValue = some_value.into();
    let json_none: JsonValue = none_value.into();

    println!("Some(42) as JSON: {}", json_some.to_json());
    println!("None as JSON: {}", json_none.to_json());
    println!();

    // Example 15: Complex data structure
    println!("15. Complex data structure");
    println!("--------------------------");
    let complex_json = r#"
    {
        "company": "TechCorp",
        "employees": [
            {"name": "Alice", "role": "Engineer", "salary": 80000},
            {"name": "Bob", "role": "Designer", "salary": 70000},
            {"name": "Charlie", "role": "Manager", "salary": 90000}
        ],
        "location": {
            "city": "San Francisco",
            "state": "CA"
        }
    }
    "#;

    match parse_json(complex_json) {
        Ok(data) => {
            println!("Company: {}", data.get("company").as_string());
            println!("Location: {}, {}",
                data.get("location").get("city").as_string(),
                data.get("location").get("state").as_string());
            println!("Employees:");
            let employees = data.get("employees");
            for i in 0..employees.len() {
                let emp = employees.get_index(i);
                println!("  - {} ({}): ${}",
                    emp.get("name").as_string(),
                    emp.get("role").as_string(),
                    emp.get("salary").as_i64());
            }
        }
        Err(e) => println!("Parse error: {}", e),
    }
    println!();

    println!("========================================");
    println!("All examples completed!");
    println!("========================================");
}
