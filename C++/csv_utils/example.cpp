/**
 * @file example.cpp
 * @brief Usage examples for csv_utils
 * 
 * Compile: g++ -std=c++17 -o example example.cpp csv_utils_test.cpp
 * Run: ./example
 */

#include "csv_utils.hpp"
#include <iostream>
#include <fstream>

using namespace csv_utils;

void print_separator(const std::string& title) {
    std::cout << "\n=== " << title << " ===" << std::endl;
}

void example_basic_read() {
    print_separator("Basic CSV Reading");
    
    // Create a sample CSV
    std::string csv = R"(name,age,city
Alice,30,Beijing
Bob,25,Shanghai
Charlie,35,Guangzhou
)";
    
    // Parse with header
    auto rows = parse_csv(csv, true);
    
    std::cout << "Read " << rows.size() << " rows:" << std::endl;
    for (const auto& row : rows) {
        std::cout << "  Name: " << row[0] 
                  << ", Age: " << row[1] 
                  << ", City: " << row[2] << std::endl;
    }
}

void example_basic_write() {
    print_separator("Basic CSV Writing");
    
    // Create rows
    std::vector<CsvRow> rows;
    rows.push_back(CsvRow({"Apple", "10", "Red"}));
    rows.push_back(CsvRow({"Banana", "20", "Yellow"}));
    rows.push_back(CsvRow({"Grape", "15", "Purple"}));
    
    // Write to string
    std::vector<std::string> header = {"fruit", "quantity", "color"};
    std::string csv = to_csv(rows, header);
    
    std::cout << "Generated CSV:" << std::endl;
    std::cout << csv << std::endl;
}

void example_file_operations() {
    print_separator("File Operations");
    
    // Create a temporary CSV file
    std::string filename = "/tmp/example_data.csv";
    
    // Write data
    std::vector<std::string> header = {"id", "product", "price"};
    std::vector<CsvRow> rows;
    rows.push_back(CsvRow({"1", "Laptop", "999.99"}));
    rows.push_back(CsvRow({"2", "Mouse", "29.99"}));
    rows.push_back(CsvRow({"3", "Keyboard", "79.99"}));
    
    write_csv(filename, rows, header);
    std::cout << "Written to: " << filename << std::endl;
    
    // Read back
    auto read_rows = read_csv(filename);
    std::cout << "Read " << read_rows.size() << " rows from file:" << std::endl;
    
    for (const auto& row : read_rows) {
        std::cout << "  ID: " << row.as_int(0)
                  << ", Product: " << row[1]
                  << ", Price: $" << row.as_double(2) << std::endl;
    }
    
    // Clean up
    std::remove(filename.c_str());
}

void example_streaming_large_file() {
    print_separator("Streaming Large File");
    
    // Generate a large CSV in memory
    std::ostringstream oss;
    oss << "id,value,score\n";
    for (int i = 0; i < 1000; ++i) {
        oss << i << ",item" << i << "," << (i * 10 % 100) << "\n";
    }
    
    // Stream process without loading all into memory
    int count = 0;
    double total_score = 0;
    
    CsvReader reader;
    reader.stream_from_string(oss.str(), [&count, &total_score](const CsvRow& row) {
        total_score += row.as_double(2);
        ++count;
    });
    
    std::cout << "Processed " << count << " rows" << std::endl;
    std::cout << "Average score: " << (total_score / count) << std::endl;
}

void example_custom_delimiter() {
    print_separator("Custom Delimiter (TSV)");
    
    // Tab-separated values
    std::string tsv = "name\tscore\tgrade\nAlice\t95\tA\nBob\t87\tB\n";
    
    CsvConfig config;
    config.has_header = true;
    config.delimiter = '\t';
    
    CsvReader reader(config);
    auto rows = reader.read_from_string(tsv);
    
    std::cout << "TSV data:" << std::endl;
    for (const auto& row : rows) {
        std::cout << "  " << row[0] << ": " << row[1] << " (" << row[2] << ")" << std::endl;
    }
}

void example_quoted_fields() {
    print_separator("Quoted Fields with Special Characters");
    
    // Note: Multi-line fields within quotes are not supported by getline-based readers
    std::string csv = R"(name,description,value
"Smith, John","Contains ""quotes"" and commas",100
"Jane Doe","Simple description",200
)";
    
    auto rows = parse_csv(csv);
    
    for (const auto& row : rows) {
        std::cout << "Name: " << row[0] << std::endl;
        std::cout << "Description: " << row[1] << std::endl;
        std::cout << "Value: " << row[2] << std::endl;
        std::cout << "---" << std::endl;
    }
}

void example_filter_and_transform() {
    print_separator("Filter and Transform");
    
    std::string csv = R"(product,price,stock
Apple,1.50,100
Banana,0.80,200
Orange,2.00,50
Grape,3.00,30
Mango,1.20,80
)";
    
    auto rows = parse_csv(csv);
    
    // Filter: products with stock > 50
    auto high_stock = filter_rows(rows, [](const CsvRow& row) {
        return row.as_int(2) > 50;
    });
    
    std::cout << "Products with stock > 50:" << std::endl;
    for (const auto& row : high_stock) {
        std::cout << "  " << row[0] << ": " << row.as_int(2) << " units @ $" 
                  << row.as_double(1) << std::endl;
    }
    
    // Calculate total value
    double total_value = 0;
    for (const auto& row : rows) {
        total_value += row.as_double(1) * row.as_int(2);
    }
    std::cout << "\nTotal inventory value: $" << total_value << std::endl;
}

void example_header_access() {
    print_separator("Column Access by Name");
    
    std::string csv = R"(employee_id,first_name,last_name,department,salary
E001,John,Smith,Engineering,85000
E002,Jane,Doe,Marketing,72000
E003,Bob,Johnson,Engineering,92000
)";
    
    CsvReader reader;
    auto rows = reader.read_from_string(csv);
    
    std::cout << "Employees in Engineering:" << std::endl;
    for (const auto& row : rows) {
        if (row.at("department") == "Engineering") {
            std::cout << "  " << row.at("first_name") << " " << row.at("last_name")
                      << ": $" << row.as_double(4) << std::endl;
        }
    }
}

void example_roundtrip() {
    print_separator("Roundtrip (Write then Read)");
    
    // Create data
    std::vector<std::string> header = {"timestamp", "user", "action", "details"};
    std::vector<CsvRow> original;
    original.push_back(CsvRow({"2024-01-15 10:30:00", "admin", "login", "Success from 192.168.1.1"}));
    original.push_back(CsvRow({"2024-01-15 10:35:00", "admin", "update", "Modified config.ini"}));
    original.push_back(CsvRow({"2024-01-15 10:40:00", "admin", "logout", "Session ended"}));
    
    // Write to string
    std::string csv = to_csv(original, header);
    std::cout << "Written CSV:" << std::endl;
    std::cout << csv << std::endl;
    
    // Read back
    auto restored = parse_csv(csv);
    std::cout << "Restored " << restored.size() << " rows:" << std::endl;
    for (const auto& row : restored) {
        std::cout << "  [" << row[0] << "] " << row[1] << ": " << row[2] << std::endl;
    }
}

int main() {
    std::cout << "CSV Utils Examples" << std::endl;
    std::cout << "==================" << std::endl;
    
    example_basic_read();
    example_basic_write();
    example_file_operations();
    example_streaming_large_file();
    example_custom_delimiter();
    example_quoted_fields();
    example_filter_and_transform();
    example_header_access();
    example_roundtrip();
    
    std::cout << "\n=== All examples completed ===" << std::endl;
    
    return 0;
}