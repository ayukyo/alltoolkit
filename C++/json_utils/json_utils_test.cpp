/**
 * @file json_utils_test.cpp
 * @brief Unit tests for C++ JSON Utilities
 */

#include <iostream>
#include <cassert>
#include <cmath>
#include "mod.hpp"

using namespace AllToolkit;

void testNull() {
    Json j;
    assert(j.isNull());
    assert(j.toString() == "null");
    std::cout << "✓ Null test passed\n";
}

void testBoolean() {
    Json j1(true);
    assert(j1.isBoolean());
    assert(j1.asBool() == true);
    assert(j1.toString() == "true");
    
    Json j2(false);
    assert(j2.asBool() == false);
    assert(j2.toString() == "false");
    std::cout << "✓ Boolean test passed\n";
}

void testNumber() {
    Json j1(42);
    assert(j1.isNumber());
    assert(j1.asInt() == 42);
    
    Json j2(3.14);
    assert(j2.asDouble() > 3.13 && j2.asDouble() < 3.15);
    
    Json j3(-123);
    assert(j3.asInt() == -123);
    std::cout << "✓ Number test passed\n";
}

void testString() {
    Json j("Hello, World!");
    assert(j.isString());
    assert(j.asString() == "Hello, World!");
    assert(j.toString() == "\"Hello, World!\"");
    std::cout << "✓ String test passed\n";
}

void testArray() {
    Json arr = Json::Array({1, 2, 3});
    assert(arr.isArray());
    assert(arr.size() == 3);
    assert(arr[0].asInt() == 1);
    assert(arr[1].asInt() == 2);
    assert(arr[2].asInt() == 3);
    std::cout << "✓ Array test passed\n";
}

void testObject() {
    Json obj = Json::Object({
        {"name", "John"},
        {"age", 30}
    });
    assert(obj.isObject());
    assert(obj["name"].asString() == "John");
    assert(obj["age"].asInt() == 30);
    assert(obj.has("name"));
    assert(!obj.has("missing"));
    std::cout << "✓ Object test passed\n";
}

void testParse() {
    std::string json = R"({"name": "Alice", "age": 25, "active": true})";
    Json obj = Json::parse(json);
    assert(obj.isObject());
    assert(obj["name"].asString() == "Alice");
    assert(obj["age"].asInt() == 25);
    assert(obj["active"].asBool() == true);
    std::cout << "✓ Parse test passed\n";
}

void testParseArray() {
    std::string json = "[1, 2, 3, \"hello\", true, null]";
    Json arr = Json::parse(json);
    assert(arr.isArray());
    assert(arr.size() == 6);
    assert(arr[0].asInt() == 1);
    assert(arr[3].asString() == "hello");
    assert(arr[4].asBool() == true);
    assert(arr[5].isNull());
    std::cout << "✓ Parse array test passed\n";
}

void testNested() {
    std::string json = R"({"user": {"name": "Bob", "scores": [85, 90, 95]}})";
    Json obj = Json::parse(json);
    assert(obj["user"]["name"].asString() == "Bob");
    assert(obj["user"]["scores"][1].asInt() == 90);
    std::cout << "✓ Nested test passed\n";
}

void testEscape() {
    std::string json = R"({"text": "Hello\nWorld\tTab\"Quote"})";
    Json obj = Json::parse(json);
    assert(obj["text"].asString() == "Hello\nWorld\tTab\"Quote");
    std::cout << "✓ Escape test passed\n";
}

void testPrettyPrint() {
    Json obj = Json::Object({{"a", 1}, {"b", 2}});
    std::string pretty = obj.toPrettyString();
    assert(pretty.find("\n") != std::string::npos);
    assert(pretty.find("  \"a\"") != std::string::npos);
    std::cout << "✓ Pretty print test passed\n";
}

void testGetters() {
    Json obj = Json::Object({
        {"name", "Test"},
        {"count", 42},
        {"price", 19.99},
        {"active", true}
    });
    assert(obj.getString("name") == "Test");
    assert(obj.getInt("count") == 42);
    assert(obj.getDouble("price") > 19.9);
    assert(obj.getBool("active") == true);
    assert(obj.getString("missing", "default") == "default");
    std::cout << "✓ Getters test passed\n";
}

void testValidation() {
    assert(Json::isValid("{}"));
    assert(Json::isValid("[]"));
    assert(Json::isValid("null"));
    assert(Json::isValid("true"));
    assert(Json::isValid("123"));
    assert(Json::isValid("\"hello\""));
    assert(!Json::isValid("{invalid}"));
    assert(!Json::isValid(""));
    std::cout << "✓ Validation test passed\n";
}

void testRoundTrip() {
    Json original = Json::Object({
        {"name", "Test"},
        {"values", Json::Array({1, 2, 3})},
        {"nested", Json::Object({{"key", "value"}})}
    });
    std::string json = original.toString();
    Json parsed = Json::parse(json);
    assert(parsed["name"].asString() == "Test");
    assert(parsed["values"].size() == 3);
    assert(parsed["nested"]["key"].asString() == "value");
    std::cout << "✓ Round trip test passed\n";
}

int main() {
    std::cout << "Running JSON Utils Tests...\n\n";
    
    testNull();
    testBoolean();
    testNumber();
    testString();
    testArray();
    testObject();
    testParse();
    testParseArray();
    testNested();
    testEscape();
    testPrettyPrint();
    testGetters();
    testValidation();
    testRoundTrip();
    
    std::cout << "\n✅ All tests passed!\n";
    return 0;
}
