//! JSON Utilities Test Suite
//!
//! Comprehensive tests for the JSON parsing and generation module.

use std::collections::HashMap;

// Include the module for testing
#[path = "mod.rs"]
mod json_utils;

use json_utils::*;

fn main() {
    println!("Running JSON Utilities Test Suite...\n");

    let mut passed = 0;
    let mut failed = 0;

    // Test 1: Parse null
    print!("Test 1: Parse null... ");
    match parse_json("null") {
        Ok(v) if v.is_null() => { println!("PASSED"); passed += 1; }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 2: Parse true
    print!("Test 2: Parse true... ");
    match parse_json("true") {
        Ok(v) if v.as_bool() == true => { println!("PASSED"); passed += 1; }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 3: Parse false
    print!("Test 3: Parse false... ");
    match parse_json("false") {
        Ok(v) if v.as_bool() == false => { println!("PASSED"); passed += 1; }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 4: Parse integer
    print!("Test 4: Parse integer... ");
    match parse_json("42") {
        Ok(v) if v.as_i64() == 42 => { println!("PASSED"); passed += 1; }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 5: Parse negative integer
    print!("Test 5: Parse negative integer... ");
    match parse_json("-42") {
        Ok(v) if v.as_i64() == -42 => { println!("PASSED"); passed += 1; }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 6: Parse float
    print!("Test 6: Parse float... ");
    match parse_json("3.14") {
        Ok(v) => {
            let n = v.as_f64();
            if (n - 3.14).abs() < 0.001 { println!("PASSED"); passed += 1; }
            else { println!("FAILED"); failed += 1; }
        }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 7: Parse scientific notation
    print!("Test 7: Parse scientific notation... ");
    match parse_json("1e10") {
        Ok(v) if v.as_f64() == 1e10 => { println!("PASSED"); passed += 1; }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 8: Parse simple string
    print!("Test 8: Parse simple string... ");
    match parse_json("\"hello\"") {
        Ok(v) if v.as_string() == "hello" => { println!("PASSED"); passed += 1; }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 9: Parse string with newline escape
    print!("Test 9: Parse string with newline escape... ");
    match parse_json("\"hello\\nworld\"") {
        Ok(v) if v.as_string() == "hello\nworld" => { println!("PASSED"); passed += 1; }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 10: Parse string with tab escape
    print!("Test 10: Parse string with tab escape... ");
    match parse_json("\"hello\\tworld\"") {
        Ok(v) if v.as_string() == "hello\tworld" => { println!("PASSED"); passed += 1; }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 11: Parse string with quote escape
    print!("Test 11: Parse string with quote escape... ");
    match parse_json("\"hello\\\"world\"") {
        Ok(v) if v.as_string() == "hello\"world" => { println!("PASSED"); passed += 1; }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 12: Parse string with unicode escape
    print!("Test 12: Parse string with unicode escape... ");
    match parse_json("\"\\u0041\\u0042\\u0043\"") {
        Ok(v) if v.as_string() == "ABC" => { println!("PASSED"); passed += 1; }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 13: Parse empty array
    print!("Test 13: Parse empty array... ");
    match parse_json("[]") {
        Ok(v) if v.is_array() && v.is_empty() => { println!("PASSED"); passed += 1; }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 14: Parse array with numbers
    print!("Test 14: Parse array with numbers... ");
    match parse_json("[1, 2, 3]") {
        Ok(v) => {
            if v.len() == 3 &&
               v.get_index(0).as_i64() == 1 &&
               v.get_index(1).as_i64() == 2 &&
               v.get_index(2).as_i64() == 3 {
                println!("PASSED"); passed += 1;
            } else {
                println!("FAILED"); failed += 1;
            }
        }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 15: Parse array with mixed types
    print!("Test 15: Parse array with mixed types... ");
    match parse_json("[1, \"two\", true, null]") {
        Ok(v) => {
            if v.len() == 4 &&
               v.get_index(0).as_i64() == 1 &&
               v.get_index(1).as_string() == "two" &&
               v.get_index(2).as_bool() == true &&
               v.get_index(3).is_null() {
                println!("PASSED"); passed += 1;
            } else {
                println!("FAILED"); failed += 1;
            }
        }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 16: Parse empty object
    print!("Test 16: Parse empty object... ");
    match parse_json("{}") {
        Ok(v) if v.is_object() && v.is_empty() => { println!("PASSED"); passed += 1; }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 17: Parse simple object
    print!("Test 17: Parse simple object... ");
    match parse_json(r#"{"name": "John", "age": 30}"#) {
        Ok(v) => {
            if v.get("name").as_string() == "John" &&
               v.get("age").as_i64() == 30 {
                println!("PASSED"); passed += 1;
            } else {
                println!("FAILED"); failed += 1;
            }
        }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 18: Parse nested object
    print!("Test 18: Parse nested object... ");
    match parse_json(r#"{"user": {"name": "John", "age": 30}}"#) {
        Ok(v) => {
            if v.get("user").get("name").as_string() == "John" &&
               v.get("user").get("age").as_i64() == 30 {
                println!("PASSED"); passed += 1;
            } else {
                println!("FAILED"); failed += 1;
            }
        }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 19: Parse array of objects
    print!("Test 19: Parse array of objects... ");
    match parse_json(r#"[{"id": 1}, {"id": 2}]"#) {
        Ok(v) => {
            if v.len() == 2 &&
               v.get_index(0).get("id").as_i64() == 1 &&
               v.get_index(1).get("id").as_i64() == 2 {
                println!("PASSED"); passed += 1;
            } else {
                println!("FAILED"); failed += 1;
            }
        }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 20: Test has() method
    print!("Test 20: Test has() method... ");
    match parse_json(r#"{"a": 1}"#) {
        Ok(v) => {
            if v.has("a") && !v.has("b") {
                println!("PASSED"); passed += 1;
            } else {
                println!("FAILED"); failed += 1;
            }
        }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 21: Test keys() method
    print!("Test 21: Test keys() method... ");
    match parse_json(r#"{"a": 1, "b": 2}"#) {
        Ok(v) => {
            let keys = v.keys();
            if keys.len() == 2 && keys.contains(&"a".to_string()) && keys.contains(&"b".to_string()) {
                println!("PASSED"); passed += 1;
            } else {
                println!("FAILED"); failed += 1;
            }
        }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 22: Test is_valid_json()
    print!("Test 22: Test is_valid_json()... ");
    if is_valid_json("{}") && is_valid_json("[]") && is_valid_json("null") &&
       is_valid_json("true") && is_valid_json("123") && is_valid_json("\"test\"") &&
       !is_valid_json("") && !is_valid_json("{invalid}") && !is_valid_json("undefined") {
        println!("PASSED"); passed += 1;
    } else {
        println!("FAILED"); failed += 1;
    }

    // Test 23: Test to_json() serialization
    print!("Test 23: Test to_json() serialization... ");
    let obj = json_utils::JsonValue::object({
        let mut m = HashMap::new();
        m.insert("name".to_string(), json_utils::JsonValue::string("John"));
        m.insert("age".to_string(), json_utils::JsonValue::number(30.0));
        m
    });
    let json_str = obj.to_json();
    if json_str.contains("name") && json_str.contains("John") &&
       json_str.contains("age") && json_str.contains("30") {
        println!("PASSED"); passed += 1;
    } else {
        println!("FAILED"); failed += 1;
    }

    // Test 24: Test round-trip parsing
    print!("Test 24: Test round-trip parsing... ");
    let original = r#"{"name": "John", "age": 30, "active": true}"#;
    match parse_json(original) {
        Ok(parsed) => {
            let output = parsed.to_json();
            match parse_json(&output) {
                Ok(reparsed) => {
                    if parsed == reparsed {
                        println!("PASSED"); passed += 1;
                    } else {
                        println!("FAILED"); failed += 1;
                    }
                }
                _ => { println!("FAILED"); failed += 1; }
            }
        }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 25: Test type checking methods
    print!("Test 25: Test type checking methods... ");
    if json_utils::JsonValue::Null.is_null() &&
       json_utils::JsonValue::Bool(true).is_bool() &&
       json_utils::JsonValue::Number(42.0).is_number() &&
       json_utils::JsonValue::String("test".to_string()).is_string() &&
       json_utils::JsonValue::Array(vec![]).is_array() &&
       json_utils::JsonValue::Object(HashMap::new()).is_object() {
        println!("PASSED"); passed += 1;
    } else {
        println!("FAILED"); failed += 1;
    }

    // Test 26: Test default value methods
    print!("Test 26: Test default value methods... ");
    let null_val = json_utils::JsonValue::Null;
    if null_val.as_bool_or(true) == true &&
       null_val.as_i64_or(42) == 42 &&
       null_val.as_f64_or(3.14) == 3.14 &&
       null_val.as_string_or("default") == "default" {
        println!("PASSED"); passed += 1;
    } else {
        println!("FAILED"); failed += 1;
    }

    // Test 27: Test merge
    print!("Test 27: Test merge... ");
    let mut obj1 = match parse_json(r#"{"a": 1}"#) {
        Ok(v) => v,
        _ => { println!("FAILED"); failed += 1; return; }
    };
    let obj2 = match parse_json(r#"{"b": 2}"#) {
        Ok(v) => v,
        _ => { println!("FAILED"); failed += 1; return; }
    };
    obj1.merge(&obj2);
    if obj1.get("a").as_i64() == 1 && obj1.get("b").as_i64() == 2 {
        println!("PASSED"); passed += 1;
    } else {
        println!("FAILED"); failed += 1;
    }

    // Test 28: Test pretty print
    print!("Test 28: Test pretty print... ");
    match parse_json(r#"{"a":1}"#) {
        Ok(v) => {
            let pretty = v.to_pretty_json();
            if pretty.contains("\n") && pretty.contains("  ") {
                println!("PASSED"); passed += 1;
            } else {
                println!("FAILED"); failed += 1;
            }
        }
        _ => { println!("FAILED"); failed += 1; }
    }

    // Test 29: Test From conversions
    print!("Test 29: Test From conversions... ");
    let _: json_utils::JsonValue = ().into();
    let _: json_utils::JsonValue = true.into();
    let _: json_utils::JsonValue = 42i32.into();
    let _: json_utils::JsonValue = 3.14f64.into();
    let _: json_utils::JsonValue = "test".into();
    let _: json_utils::JsonValue = vec![1i32, 2, 3].into();
    println!("PASSED"); passed += 1;

    // Test 30: Test parse_json_or_null
    print!("Test 30: Test parse_json_or_null... ");
    let result = parse_json_or_null("invalid json");
    if result.is_null() {
        println!("PASSED"); passed += 1;
    } else {
        println!("FAILED"); failed += 1;
    }

    // Summary
    println!("\n========================================");
    println!("Test Results: {} passed, {} failed", passed, failed);
    println!("========================================");

    if failed > 0 {
        std::process::exit(1);
    }
}
