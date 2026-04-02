/**
 * @file json_utils_example.cpp
 * @brief Example usage of C++ JSON Utilities
 * 
 * This example demonstrates how to use the AllToolkit JSON library
 * for parsing, building, and manipulating JSON data.
 */

#include <iostream>
#include <string>
#include "../json_utils/mod.hpp"

using namespace AllToolkit;

void example1_buildingJson() {
    std::cout << "=== Example 1: Building JSON ===\n";
    
    // Create a simple object
    Json person;
    person["name"] = "John Doe";
    person["age"] = 30;
    person["active"] = true;
    person["balance"] = 1234.56;
    
    // Create an array
    person["hobbies"] = Json::Array({"reading", "coding", "gaming"});
    
    // Create nested object
    Json address;
    address["street"] = "123 Main St";
    address["city"] = "New York";
    address["zip"] = "10001";
    person["address"] = address;
    
    // Output compact JSON
    std::cout << "Compact JSON:\n" << person.toString() << "\n\n";
    
    // Output pretty-printed JSON
    std::cout << "Pretty JSON:\n" << person.toPrettyString() << "\n";
}

void example2_parsingJson() {
    std::cout << "\n=== Example 2: Parsing JSON ===\n";
    
    std::string jsonStr = R"({
        "product": "Laptop",
        "price": 999.99,
        "inStock": true,
        "tags": ["electronics", "computers", "portable"],
        "specs": {
            "cpu": "Intel i7",
            "ram": "16GB",
            "storage": "512GB SSD"
        }
    })";
    
    // Parse JSON string
    Json product = Json::parse(jsonStr);
    
    // Access values
    std::cout << "Product: " << product["product"].asString() << "\n";
    std::cout << "Price: $" << product["price"].asDouble() << "\n";
    std::cout << "In Stock: " << (product["inStock"].asBool() ? "Yes" : "No") << "\n";
    
    // Access array
    std::cout << "Tags: ";
    Json tags = product["tags"];
    for (size_t i = 0; i < tags.size(); ++i) {
        if (i > 0) std::cout << ", ";
        std::cout << tags[i].asString();
    }
    std::cout << "\n";
    
    // Access nested object
    std::cout << "CPU: " << product["specs"]["cpu"].asString() << "\n";
    std::cout << "RAM: " << product["specs"]["ram"].asString() << "\n";
}

void example3_safeAccess() {
    std::cout << "\n=== Example 3: Safe Access with Defaults ===\n";
    
    Json config = Json::parse(R"({
        "server": "localhost",
        "port": 8080,
        "debug": false
    })");
    
    // Safe getters with defaults
    std::string server = config.getString("server", "127.0.0.1");
    int port = config.getInt("port", 3000);
    bool debug = config.getBool("debug", true);
    int timeout = config.getInt("timeout", 30);  // Uses default
    
    std::cout << "Server: " << server << "\n";
    std::cout << "Port: " << port << "\n";
    std::cout << "Debug: " << (debug ? "true" : "false") << "\n";
    std::cout << "Timeout: " << timeout << " (default used)\n";
    
    // Check if key exists
    if (config.has("ssl")) {
        std::cout << "SSL config found\n";
    } else {
        std::cout << "SSL config not found\n";
    }
}

void example4_workingWithArrays() {
    std::cout << "\n=== Example 4: Working with Arrays ===\n";
    
    // Parse array
    Json numbers = Json::parse("[10, 20, 30, 40, 50]");
    
    std::cout << "Array size: " << numbers.size() << "\n";
    std::cout << "Elements: ";
    for (size_t i = 0; i < numbers.size(); ++i) {
        if (i > 0) std::cout << ", ";
        std::cout << numbers[i].asInt();
    }
    std::cout << "\n";
    
    // Build array programmatically
    Json items = Json::Array({"First"});
    // Note: For empty arrays, you need to rebuild or use push_back pattern
    // Here we create with initial element
    Json moreItems = Json::Array({"First", "Second", "Third"});
    
    std::cout << "Built array: " << moreItems.toString() << "\n";
}

void example5_errorHandling() {
    std::cout << "\n=== Example 5: Error Handling ===\n";
    
    // Validate JSON
    std::string invalidJson = "{invalid json}";
    std::string error;
    
    Json result = Json::parse(invalidJson, error);
    if (!error.empty()) {
        std::cout << "Parse error: " << error << "\n";
    }
    
    // Check if valid
    if (Json::isValid("{\"valid\": true}")) {
        std::cout << "Valid JSON detected\n";
    }
    
    if (!Json::isValid("not json")) {
        std::cout << "Invalid JSON detected\n";
    }
}

void example6_complexStructure() {
    std::cout << "\n=== Example 6: Complex Structure ===\n";
    
    // Build a complex nested structure
    Json users = Json::Array({
        Json::Object({
            {"id", 1},
            {"name", "Alice"},
            {"roles", Json::Array({"admin", "user"})}
        }),
        Json::Object({
            {"id", 2},
            {"name", "Bob"},
            {"roles", Json::Array({"user"})}
        }),
        Json::Object({
            {"id", 3},
            {"name", "Charlie"},
            {"roles", Json::Array({"user", "editor"})}
        })
    });
    
    std::cout << "Users:\n";
    for (size_t i = 0; i < users.size(); ++i) {
        Json user = users[i];
        std::cout << "  ID: " << user["id"].asInt();
        std::cout << ", Name: " << user["name"].asString();
        std::cout << ", Roles: ";
        
        Json roles = user["roles"];
        for (size_t j = 0; j < roles.size(); ++j) {
            if (j > 0) std::cout << ", ";
            std::cout << roles[j].asString();
        }
        std::cout << "\n";
    }
    
    std::cout << "\nFull JSON:\n" << users.toPrettyString() << "\n";
}

void example7_modifyingJson() {
    std::cout << "\n=== Example 7: Modifying JSON ===\n";
    
    // Start with existing JSON
    Json data = Json::parse(R"({"count": 5, "items": ["a", "b"]})");
    
    std::cout << "Original: " << data.toString() << "\n";
    
    // Modify values
    data["count"] = 10;
    data["status"] = "updated";
    // Replace entire array instead of indexing beyond bounds
    data["items"] = Json::Array({"a", "b", "c", "d"});
    
    std::cout << "Modified: " << data.toString() << "\n";
}

int main() {
    std::cout << "C++ JSON Utilities Examples\n";
    std::cout << "===========================\n\n";
    
    try {
        example1_buildingJson();
        example2_parsingJson();
        example3_safeAccess();
        example4_workingWithArrays();
        example5_errorHandling();
        example6_complexStructure();
        example7_modifyingJson();
        
        std::cout << "\n✅ All examples completed successfully!\n";
    } catch (const std::exception& e) {
        std::cerr << "\n❌ Error: " << e.what() << "\n";
        return 1;
    }
    
    return 0;
}
