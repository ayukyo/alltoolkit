/**
 * @file csv_utils.hpp
 * @brief CSV file reading and writing utilities for C++
 * @author AllToolkit
 * @date 2026-04-17
 * 
 * Zero external dependencies - uses only C++17 standard library
 */

#ifndef CSV_UTILS_HPP
#define CSV_UTILS_HPP

#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <functional>
#include <optional>
#include <variant>
#include <map>
#include <algorithm>
#include <cctype>

namespace csv_utils {

// ============================================================================
// Configuration
// ============================================================================

struct CsvConfig {
    char delimiter = ',';
    char quote = '"';
    char escape = '"';
    bool has_header = true;
    bool skip_empty_lines = true;
    bool trim_whitespace = false;
    std::string line_ending = "\n";
};

// ============================================================================
// CSV Cell Value Type
// ============================================================================

using CsvValue = std::variant<std::string, int64_t, double, bool>;

// ============================================================================
// CSV Row
// ============================================================================

class CsvRow {
public:
    CsvRow() = default;
    explicit CsvRow(std::vector<std::string> values) : values_(std::move(values)) {}
    
    // Access by index
    const std::string& operator[](size_t index) const {
        if (index >= values_.size()) {
            throw std::out_of_range("Column index out of range: " + std::to_string(index));
        }
        return values_[index];
    }
    
    std::string& operator[](size_t index) {
        if (index >= values_.size()) {
            values_.resize(index + 1);
        }
        return values_[index];
    }
    
    // Access by column name (requires header mapping)
    const std::string& at(const std::string& column) const {
        if (!header_map_) {
            throw std::runtime_error("No header mapping available");
        }
        auto it = header_map_->find(column);
        if (it == header_map_->end()) {
            throw std::out_of_range("Column not found: " + column);
        }
        return (*this)[it->second];
    }
    
    // Size
    size_t size() const { return values_.size(); }
    bool empty() const { return values_.empty(); }
    
    // Iterators
    auto begin() const { return values_.begin(); }
    auto end() const { return values_.end(); }
    auto begin() { return values_.begin(); }
    auto end() { return values_.end(); }
    
    // Get typed values
    int64_t as_int(size_t index, int64_t default_val = 0) const {
        try {
            return std::stoll((*this)[index]);
        } catch (...) {
            return default_val;
        }
    }
    
    double as_double(size_t index, double default_val = 0.0) const {
        try {
            return std::stod((*this)[index]);
        } catch (...) {
            return default_val;
        }
    }
    
    bool as_bool(size_t index, bool default_val = false) const {
        const std::string& val = (*this)[index];
        std::string lower;
        for (char c : val) {
            lower += std::tolower(c);
        }
        if (lower == "true" || lower == "1" || lower == "yes" || lower == "on") {
            return true;
        }
        if (lower == "false" || lower == "0" || lower == "no" || lower == "off") {
            return false;
        }
        return default_val;
    }
    
    // Set header mapping (called by reader)
    void set_header_map(const std::map<std::string, size_t>* header_map) {
        header_map_ = header_map;
    }
    
private:
    std::vector<std::string> values_;
    const std::map<std::string, size_t>* header_map_ = nullptr;
};

// ============================================================================
// CSV Writer
// ============================================================================

class CsvWriter {
public:
    explicit CsvWriter(const CsvConfig& config = CsvConfig{}) : config_(config) {}
    
    // Write to string
    std::string write_to_string(const std::vector<CsvRow>& rows,
                                const std::vector<std::string>& header = {}) {
        std::ostringstream oss;
        write_to_stream(oss, rows, header);
        return oss.str();
    }
    
    // Write to file
    void write_to_file(const std::string& filename,
                       const std::vector<CsvRow>& rows,
                       const std::vector<std::string>& header = {}) {
        std::ofstream file(filename);
        if (!file) {
            throw std::runtime_error("Cannot open file for writing: " + filename);
        }
        write_to_stream(file, rows, header);
    }
    
    // Write to ostream
    void write_to_stream(std::ostream& os,
                         const std::vector<CsvRow>& rows,
                         const std::vector<std::string>& header = {}) {
        // Write header if provided
        if (!header.empty() && config_.has_header) {
            write_row(os, header);
        }
        
        // Write data rows
        for (const auto& row : rows) {
            std::vector<std::string> values;
            for (const auto& val : row) {
                values.push_back(val);
            }
            write_row(os, values);
        }
    }
    
    // Write single row
    void write_row(std::ostream& os, const std::vector<std::string>& values) {
        for (size_t i = 0; i < values.size(); ++i) {
            if (i > 0) {
                os << config_.delimiter;
            }
            os << escape_field(values[i]);
        }
        os << config_.line_ending;
    }
    
private:
    CsvConfig config_;
    
    std::string escape_field(const std::string& field) {
        bool needs_quoting = false;
        
        // Check if quoting is needed
        for (char c : field) {
            if (c == config_.delimiter || c == config_.quote || 
                c == '\n' || c == '\r') {
                needs_quoting = true;
                break;
            }
        }
        
        if (!needs_quoting && !config_.trim_whitespace) {
            needs_quoting = (field.find_first_of(" \t") != std::string::npos);
        }
        
        if (!needs_quoting) {
            return field;
        }
        
        // Quote and escape
        std::string result;
        result += config_.quote;
        
        for (char c : field) {
            if (c == config_.quote) {
                result += config_.escape;
                result += config_.quote;
            } else {
                result += c;
            }
        }
        
        result += config_.quote;
        return result;
    }
};

// ============================================================================
// CSV Reader
// ============================================================================

class CsvReader {
public:
    explicit CsvReader(const CsvConfig& config = CsvConfig{}) 
        : config_(config), line_number_(0) {}
    
    // Read from string
    std::vector<CsvRow> read_from_string(const std::string& content) {
        std::istringstream iss(content);
        return read_from_stream(iss);
    }
    
    // Read from file
    std::vector<CsvRow> read_from_file(const std::string& filename) {
        std::ifstream file(filename);
        if (!file) {
            throw std::runtime_error("Cannot open file for reading: " + filename);
        }
        return read_from_stream(file);
    }
    
    // Read from stream
    std::vector<CsvRow> read_from_stream(std::istream& is) {
        std::vector<CsvRow> rows;
        std::string line;
        line_number_ = 0;
        
        // Read header
        if (config_.has_header) {
            if (std::getline(is, line)) {
                ++line_number_;
                header_ = parse_line(line);
                for (size_t i = 0; i < header_.size(); ++i) {
                    header_map_[header_[i]] = i;
                }
            }
        }
        
        // Read data rows
        while (std::getline(is, line)) {
            ++line_number_;
            
            if (config_.skip_empty_lines) {
                if (line.empty() || is_whitespace_only(line)) {
                    continue;
                }
            }
            
            CsvRow row(parse_line(line));
            row.set_header_map(&header_map_);
            rows.push_back(std::move(row));
        }
        
        return rows;
    }
    
    // Get header
    const std::vector<std::string>& get_header() const { return header_; }
    
    // Get line number (for error reporting)
    size_t line_number() const { return line_number_; }
    
    // Streaming interface (for large files)
    template<typename Callback>
    void stream_from_file(const std::string& filename, Callback callback) {
        std::ifstream file(filename);
        if (!file) {
            throw std::runtime_error("Cannot open file for reading: " + filename);
        }
        stream_from_stream(file, callback);
    }
    
    template<typename Callback>
    void stream_from_stream(std::istream& is, Callback callback) {
        std::string line;
        line_number_ = 0;
        
        // Read header
        if (config_.has_header) {
            if (std::getline(is, line)) {
                ++line_number_;
                header_ = parse_line(line);
                for (size_t i = 0; i < header_.size(); ++i) {
                    header_map_[header_[i]] = i;
                }
            }
        }
        
        // Stream data rows
        while (std::getline(is, line)) {
            ++line_number_;
            
            if (config_.skip_empty_lines) {
                if (line.empty() || is_whitespace_only(line)) {
                    continue;
                }
            }
            
            CsvRow row(parse_line(line));
            row.set_header_map(&header_map_);
            callback(row);
        }
    }
    
    // Stream from string (for in-memory CSV data)
    template<typename Callback>
    void stream_from_string(const std::string& content, Callback callback) {
        std::istringstream iss(content);
        stream_from_stream(iss, callback);
    }
    
private:
    CsvConfig config_;
    std::vector<std::string> header_;
    std::map<std::string, size_t> header_map_;
    size_t line_number_;
    
    bool is_whitespace_only(const std::string& s) const {
        for (char c : s) {
            if (!std::isspace(static_cast<unsigned char>(c))) {
                return false;
            }
        }
        return true;
    }
    
    std::string trim(const std::string& s) const {
        size_t start = 0;
        while (start < s.size() && std::isspace(static_cast<unsigned char>(s[start]))) {
            ++start;
        }
        
        size_t end = s.size();
        while (end > start && std::isspace(static_cast<unsigned char>(s[end - 1]))) {
            --end;
        }
        
        return s.substr(start, end - start);
    }
    
    std::vector<std::string> parse_line(const std::string& line) {
        std::vector<std::string> fields;
        std::string field;
        bool in_quotes = false;
        
        for (size_t i = 0; i < line.size(); ++i) {
            char c = line[i];
            
            if (in_quotes) {
                if (c == config_.quote) {
                    // Check for escaped quote
                    if (i + 1 < line.size() && line[i + 1] == config_.quote) {
                        field += config_.quote;
                        ++i;
                    } else {
                        in_quotes = false;
                    }
                } else {
                    field += c;
                }
            } else {
                if (c == config_.quote) {
                    in_quotes = true;
                } else if (c == config_.delimiter) {
                    if (config_.trim_whitespace) {
                        fields.push_back(trim(field));
                    } else {
                        fields.push_back(field);
                    }
                    field.clear();
                } else {
                    field += c;
                }
            }
        }
        
        // Add last field
        if (config_.trim_whitespace) {
            fields.push_back(trim(field));
        } else {
            fields.push_back(field);
        }
        
        return fields;
    }
};

// ============================================================================
// Utility Functions
// ============================================================================

// Quick read CSV file
inline std::vector<CsvRow> read_csv(const std::string& filename, 
                                     bool has_header = true) {
    CsvConfig config;
    config.has_header = has_header;
    CsvReader reader(config);
    return reader.read_from_file(filename);
}

// Quick write CSV file
inline void write_csv(const std::string& filename,
                      const std::vector<CsvRow>& rows,
                      const std::vector<std::string>& header = {},
                      bool has_header = true) {
    CsvConfig config;
    config.has_header = has_header;
    CsvWriter writer(config);
    writer.write_to_file(filename, rows, header);
}

// Parse CSV string
inline std::vector<CsvRow> parse_csv(const std::string& content,
                                      bool has_header = true) {
    CsvConfig config;
    config.has_header = has_header;
    CsvReader reader(config);
    return reader.read_from_string(content);
}

// Convert to CSV string
inline std::string to_csv(const std::vector<CsvRow>& rows,
                          const std::vector<std::string>& header = {},
                          bool has_header = true) {
    CsvConfig config;
    config.has_header = has_header;
    CsvWriter writer(config);
    return writer.write_to_string(rows, header);
}

// Count rows in file (without loading all data)
inline size_t count_rows(const std::string& filename, bool has_header = true) {
    std::ifstream file(filename);
    if (!file) {
        throw std::runtime_error("Cannot open file: " + filename);
    }
    
    size_t count = 0;
    std::string line;
    
    while (std::getline(file, line)) {
        if (!line.empty()) {
            ++count;
        }
    }
    
    return has_header && count > 0 ? count - 1 : count;
}

// Filter rows
template<typename Predicate>
std::vector<CsvRow> filter_rows(const std::vector<CsvRow>& rows, Predicate pred) {
    std::vector<CsvRow> result;
    for (const auto& row : rows) {
        if (pred(row)) {
            result.push_back(row);
        }
    }
    return result;
}

// Select columns by index
inline std::vector<CsvRow> select_columns(const std::vector<CsvRow>& rows,
                                           const std::vector<size_t>& indices) {
    std::vector<CsvRow> result;
    for (const auto& row : rows) {
        CsvRow new_row;
        for (size_t idx : indices) {
            if (idx < row.size()) {
                new_row[new_row.size()] = row[idx];
            }
        }
        result.push_back(std::move(new_row));
    }
    return result;
}

} // namespace csv_utils

#endif // CSV_UTILS_HPP