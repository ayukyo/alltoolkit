/**
 * AllToolkit - C++ UUID Utilities Examples
 * 
 * Practical examples demonstrating uuid_utils usage.
 * Compile with: g++ -std=c++17 -o uuid_example uuid_example.cpp
 * 
 * Author: AllToolkit
 * License: MIT
 */

#include "../uuid_utils.hpp"
#include <iostream>
#include <iomanip>
#include <set>

using namespace alltoolkit;

void print_separator(const std::string& title) {
    std::cout << "\n" << std::string(50, '=') << "\n";
    std::cout << title << "\n";
    std::cout << std::string(50, '=') << "\n";
}

void example_basic_generation() {
    print_separator("Basic UUID Generation");
    
    // Generate a random UUID v4
    UUID uuid = UUID::generate_v4();
    
    std::cout << "Generated UUID v4:\n";
    std::cout << "  Standard: " << uuid.to_string() << "\n";
    std::cout << "  Uppercase: " << uuid.to_string(true) << "\n";
    std::cout << "  No dashes: " << uuid.to_string_no_dashes() << "\n";
    std::cout << "  URN:       " << uuid.to_urn() << "\n";
    std::cout << "  Version:   " << uuid.version() << "\n";
    std::cout << "  Variant:   " << uuid.variant() << "\n";
    std::cout << "  Is nil:    " << (uuid.is_nil() ? "yes" : "no") << "\n";
}

void example_parsing() {
    print_separator("UUID Parsing");
    
    // Parse from standard format
    std::string uuid_str = "550e8400-e29b-41d4-a716-446655440000";
    UUID uuid = UUID::from_string(uuid_str);
    
    std::cout << "Parsed: " << uuid.to_string() << "\n";
    
    // Parse from format without dashes
    UUID uuid2 = UUID::from_string("550e8400e29b41d4a716446655440000");
    std::cout << "Parsed (no dashes): " << uuid2.to_string() << "\n";
    
    // Validate before parsing
    std::string input = "not-a-valid-uuid";
    if (UUID::is_valid(input)) {
        UUID valid_uuid = UUID::from_string(input);
        std::cout << "Valid: " << valid_uuid.to_string() << "\n";
    } else {
        std::cout << "'" << input << "' is not a valid UUID\n";
    }
    
    // Safe parsing with try_parse
    UUID try_uuid;
    if (UUID::try_from_string("550e8400-e29b-41d4-a716-446655440000", try_uuid)) {
        std::cout << "Try-parse succeeded: " << try_uuid.to_string() << "\n";
    }
}

void example_bulk_generation() {
    print_separator("Bulk UUID Generation");
    
    // Generate 10 UUIDs efficiently
    std::vector<UUID> uuids = UUID::generate_v4_bulk(10);
    
    std::cout << "Generated " << uuids.size() << " UUIDs:\n";
    for (size_t i = 0; i < uuids.size(); ++i) {
        std::cout << std::setw(2) << (i + 1) << ". " << uuids[i].to_string() << "\n";
    }
}

void example_comparison() {
    print_separator("UUID Comparison");
    
    UUID uuid1 = UUID::from_string("00000000-0000-0000-0000-000000000000");
    UUID uuid2 = UUID::from_string("550e8400-e29b-41d4-a716-446655440000");
    UUID uuid3 = UUID::from_string("ffffffff-ffff-ffff-ffff-ffffffffffff");
    
    std::cout << "UUID 1: " << uuid1.to_string() << "\n";
    std::cout << "UUID 2: " << uuid2.to_string() << "\n";
    std::cout << "UUID 3: " << uuid3.to_string() << "\n\n";
    
    std::cout << "uuid1 < uuid2: " << (uuid1 < uuid2 ? "yes" : "no") << "\n";
    std::cout << "uuid2 < uuid3: " << (uuid2 < uuid3 ? "yes" : "no") << "\n";
    std::cout << "uuid1 == uuid1: " << (uuid1 == uuid1 ? "yes" : "no") << "\n";
    std::cout << "uuid1 == uuid2: " << (uuid1 == uuid2 ? "yes" : "no") << "\n";
    
    // Using in sorted containers
    std::set<UUID> uuid_set;
    uuid_set.insert(uuid3);
    uuid_set.insert(uuid1);
    uuid_set.insert(uuid2);
    
    std::cout << "\nSorted in set:\n";
    for (const auto& u : uuid_set) {
        std::cout << "  " << u.to_string() << "\n";
    }
}

void example_nil_uuid() {
    print_separator("Nil UUID");
    
    UUID nil_uuid = UUID::nil();
    UUID random_uuid = UUID::generate_v4();
    
    std::cout << "Nil UUID: " << nil_uuid.to_string() << "\n";
    std::cout << "Is nil: " << (nil_uuid.is_nil() ? "yes" : "no") << "\n\n";
    
    std::cout << "Random UUID: " << random_uuid.to_string() << "\n";
    std::cout << "Is nil: " << (random_uuid.is_nil() ? "yes" : "no") << "\n";
    
    // Useful for default values or checking if a UUID has been set
    UUID some_uuid;
    std::cout << "\nDefault-constructed UUID is nil: " 
              << (some_uuid.is_nil() ? "yes" : "no") << "\n";
}

void example_byte_access() {
    print_separator("Byte Access");
    
    UUID uuid = UUID::from_string("550e8400-e29b-41d4-a716-446655440000");
    
    std::cout << "UUID: " << uuid.to_string() << "\n\n";
    
    std::cout << "Individual bytes:\n";
    for (size_t i = 0; i < UUID::BYTE_SIZE; ++i) {
        std::cout << "  Byte " << std::setw(2) << i << ": 0x" 
                  << std::hex << std::setw(2) << std::setfill('0')
                  << static_cast<int>(uuid[i]) << std::dec << "\n";
    }
    
    std::cout << "\nFull byte array:\n  ";
    const auto& bytes = uuid.bytes();
    for (size_t i = 0; i < bytes.size(); ++i) {
        std::cout << std::hex << std::setw(2) << std::setfill('0')
                  << static_cast<int>(bytes[i]);
        if (i < bytes.size() - 1) std::cout << " ";
    }
    std::cout << std::dec << "\n";
}

void example_uuid_utils() {
    print_separator("UUIDUtils Helper Class");
    
    // Generation
    UUID uuid = UUIDUtils::generate();
    std::cout << "Generated: " << uuid.to_string() << "\n";
    
    // Parse
    UUID parsed = UUIDUtils::parse("550e8400-e29b-41d4-a716-446655440000");
    std::cout << "Parsed: " << parsed.to_string() << "\n";
    
    // Validate
    std::cout << "Is valid: " << (UUIDUtils::is_valid("550e8400-e29b-41d4-a716-446655440000") ? "yes" : "no") << "\n";
    
    // Compare
    UUID uuid1 = UUIDUtils::generate();
    UUID uuid2 = UUIDUtils::generate();
    std::cout << "\nCompare result: " << UUIDUtils::compare(uuid1, uuid2) << " (-1: less, 0: equal, 1: greater)\n";
    
    // Vector operations
    std::vector<UUID> uuids = UUIDUtils::generate_bulk(5);
    std::cout << "\nGenerated " << uuids.size() << " UUIDs\n";
    
    std::cout << "Contains first UUID: " << (UUIDUtils::contains(uuids, uuids[0]) ? "yes" : "no") << "\n";
    
    UUIDUtils::sort(uuids);
    std::cout << "Sorted UUIDs\n";
    
    auto strings = UUIDUtils::to_strings(uuids);
    std::cout << "Converted to strings: " << strings.size() << " strings\n";
    
    auto back = UUIDUtils::from_strings(strings);
    std::cout << "Parsed back: " << back.size() << " UUIDs\n";
}

void example_database_ids() {
    print_separator("Using as Database IDs");
    
    // Simulate generating IDs for records
    struct Record {
        UUID id;
        std::string name;
        int value;
    };
    
    std::vector<Record> records;
    
    // Create some records with UUID primary keys
    records.push_back({UUID::generate_v4(), "Alice", 100});
    records.push_back({UUID::generate_v4(), "Bob", 200});
    records.push_back({UUID::generate_v4(), "Charlie", 300});
    
    std::cout << "Records with UUID primary keys:\n";
    std::cout << std::left;
    for (const auto& record : records) {
        std::cout << "  " << std::setw(36) << record.id.to_string() 
                  << " | " << std::setw(10) << record.name 
                  << " | " << record.value << "\n";
    }
    
    // Find a record by UUID
    UUID search_id = records[1].id;
    auto it = std::find_if(records.begin(), records.end(), [&search_id](const Record& r) {
        return r.id == search_id;
    });
    
    if (it != records.end()) {
        std::cout << "\nFound record: " << it->name << " (value: " << it->value << ")\n";
    }
}

void example_session_tokens() {
    print_separator("Session Token Generation");
    
    // Generate session tokens for web applications
    struct Session {
        UUID token;
        std::string user_id;
        std::string created_at;
    };
    
    std::vector<Session> sessions;
    
    sessions.push_back({UUID::generate_v4(), "user_001", "2026-04-16T10:00:00Z"});
    sessions.push_back({UUID::generate_v4(), "user_002", "2026-04-16T10:05:00Z"});
    
    std::cout << "Active sessions:\n";
    for (const auto& session : sessions) {
        std::cout << "  Token: " << session.token.to_string() << "\n";
        std::cout << "  User:  " << session.user_id << "\n";
        std::cout << "  Since: " << session.created_at << "\n\n";
    }
    
    // Use no-dash format for URLs/cookies
    std::cout << "URL-safe token format:\n";
    std::cout << "  " << sessions[0].token.to_string_no_dashes() << "\n";
}

int main() {
    std::cout << "====================================\n";
    std::cout << "AllToolkit UUID Utilities Examples\n";
    std::cout << "====================================";
    
    example_basic_generation();
    example_parsing();
    example_bulk_generation();
    example_comparison();
    example_nil_uuid();
    example_byte_access();
    example_uuid_utils();
    example_database_ids();
    example_session_tokens();
    
    std::cout << "\n" << std::string(50, '=') << "\n";
    std::cout << "Examples completed!\n";
    std::cout << std::string(50, '=') << "\n";
    
    return 0;
}