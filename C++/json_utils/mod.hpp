/**
 * @file mod.hpp
 * @brief C++ JSON Utilities - Header-only JSON parser and builder
 * @author AllToolkit
 * @version 1.0.0
 *
 * A lightweight, header-only JSON library for C++ with no external dependencies.
 * Supports parsing, building, and manipulating JSON data.
 */

#ifndef ALLTOOLKIT_JSON_UTILS_HPP
#define ALLTOOLKIT_JSON_UTILS_HPP

#include <string>
#include <vector>
#include <map>
#include <stdexcept>
#include <sstream>
#include <iomanip>
#include <cctype>
#include <cmath>

namespace AllToolkit {

/**
 * @class Json
 * @brief Main JSON value class representing any JSON type
 */
class Json {
public:
    enum class Type { Null, Boolean, Number, String, Array, Object };

    Json() : type_(Type::Null) {}
    Json(std::nullptr_t) : type_(Type::Null) {}
    Json(bool value) : type_(Type::Boolean), boolValue_(value) {}
    Json(int value) : type_(Type::Number), numberValue_(static_cast<double>(value)) {}
    Json(long value) : type_(Type::Number), numberValue_(static_cast<double>(value)) {}
    Json(long long value) : type_(Type::Number), numberValue_(static_cast<double>(value)) {}
    Json(double value) : type_(Type::Number), numberValue_(value) {}
    Json(const char* value) : type_(Type::String), stringValue_(value) {}
    Json(const std::string& value) : type_(Type::String), stringValue_(value) {}

    static Json Array(std::initializer_list<Json> values) {
        Json j; j.type_ = Type::Array; j.arrayValue_ = std::vector<Json>(values); return j;
    }
    static Json Array(const std::vector<Json>& values) {
        Json j; j.type_ = Type::Array; j.arrayValue_ = values; return j;
    }
    static Json Object(std::initializer_list<std::pair<const std::string, Json>> pairs) {
        Json j; j.type_ = Type::Object; j.objectValue_ = std::map<std::string, Json>(pairs); return j;
    }

    bool isNull() const { return type_ == Type::Null; }
    bool isBoolean() const { return type_ == Type::Boolean; }
    bool isNumber() const { return type_ == Type::Number; }
    bool isString() const { return type_ == Type::String; }
    bool isArray() const { return type_ == Type::Array; }
    bool isObject() const { return type_ == Type::Object; }
    Type type() const { return type_; }

    bool asBool() const { if (!isBoolean()) throw std::runtime_error("Not a boolean"); return boolValue_; }
    double asDouble() const { if (!isNumber()) throw std::runtime_error("Not a number"); return numberValue_; }
    int asInt() const { if (!isNumber()) throw std::runtime_error("Not a number"); return static_cast<int>(numberValue_); }
    const std::string& asString() const { if (!isString()) throw std::runtime_error("Not a string"); return stringValue_; }
    const std::vector<Json>& asArray() const { if (!isArray()) throw std::runtime_error("Not an array"); return arrayValue_; }
    const std::map<std::string, Json>& asObject() const { if (!isObject()) throw std::runtime_error("Not an object"); return objectValue_; }

    size_t size() const {
        if (isArray()) return arrayValue_.size();
        if (isObject()) return objectValue_.size();
        throw std::runtime_error("Not an array or object");
    }
    bool empty() const {
        if (isArray()) return arrayValue_.empty();
        if (isObject()) return objectValue_.empty();
        return true;
    }

    Json& operator[](size_t index) {
        if (!isArray()) throw std::runtime_error("Not an array");
        if (index >= arrayValue_.size()) throw std::out_of_range("Array index out of range");
        return arrayValue_[index];
    }
    const Json& operator[](size_t index) const {
        if (!isArray()) throw std::runtime_error("Not an array");
        if (index >= arrayValue_.size()) throw std::out_of_range("Array index out of range");
        return arrayValue_[index];
    }
    Json& operator[](const std::string& key) {
        if (isNull()) { type_ = Type::Object; objectValue_ = std::map<std::string, Json>(); }
        if (!isObject()) throw std::runtime_error("Not an object");
        return objectValue_[key];
    }
    const Json& operator[](const std::string& key) const {
        if (!isObject()) throw std::runtime_error("Not an object");
        auto it = objectValue_.find(key);
        if (it == objectValue_.end()) throw std::out_of_range("Key not found: " + key);
        return it->second;
    }

    bool has(const std::string& key) const {
        if (!isObject()) return false;
        return objectValue_.find(key) != objectValue_.end();
    }

    std::string getString(const std::string& key, const std::string& defaultValue = "") const {
        if (!has(key)) return defaultValue;
        const Json& val = objectValue_.at(key);
        return val.isString() ? val.asString() : defaultValue;
    }
    int getInt(const std::string& key, int defaultValue = 0) const {
        if (!has(key)) return defaultValue;
        const Json& val = objectValue_.at(key);
        return val.isNumber() ? val.asInt() : defaultValue;
    }
    double getDouble(const std::string& key, double defaultValue = 0.0) const {
        if (!has(key)) return defaultValue;
        const Json& val = objectValue_.at(key);
        return val.isNumber() ? val.asDouble() : defaultValue;
    }
    bool getBool(const std::string& key, bool defaultValue = false) const {
        if (!has(key)) return defaultValue;
        const Json& val = objectValue_.at(key);
        return val.isBoolean() ? val.asBool() : defaultValue;
    }

    std::string toString() const {
        std::ostringstream oss;
        serialize(oss, false, 0);
        return oss.str();
    }
    std::string toPrettyString(int indent = 2) const {
        std::ostringstream oss;
        serialize(oss, true, 0, indent);
        return oss.str();
    }

    static Json parse(const std::string& json) {
        Parser parser(json);
        return parser.parse();
    }
    static Json parse(const std::string& json, std::string& error) {
        try {
            Parser parser(json);
            return parser.parse();
        } catch (const std::exception& e) {
            error = e.what();
            return Json();
        }
    }
    static bool isValid(const std::string& json) {
        std::string error;
        parse(json, error);
        return error.empty();
    }

private:
    Type type_;
    bool boolValue_ = false;
    double numberValue_ = 0.0;
    std::string stringValue_;
    std::vector<Json> arrayValue_;
    std::map<std::string, Json> objectValue_;

    void serialize(std::ostringstream& oss, bool pretty, int depth, int indent = 2) const {
        switch (type_) {
            case Type::Null: oss << "null"; break;
            case Type::Boolean: oss << (boolValue_ ? "true" : "false"); break;
            case Type::Number:
                if (std::isnan(numberValue_) || std::isinf(numberValue_)) oss << "null";
                else oss << std::setprecision(15) << numberValue_;
                break;
            case Type::String: oss << '"' << escapeString(stringValue_) << '"'; break;
            case Type::Array:
                oss << '[';
                if (pretty && !arrayValue_.empty()) {
                    oss << '\n';
                    for (size_t i = 0; i < arrayValue_.size(); ++i) {
                        oss << std::string((depth + 1) * indent, ' ');
                        arrayValue_[i].serialize(oss, pretty, depth + 1, indent);
                        if (i < arrayValue_.size() - 1) oss << ",";
                        oss << '\n';
                    }
                    oss << std::string(depth * indent, ' ');
                } else {
                    for (size_t i = 0; i < arrayValue_.size(); ++i) {
                        if (i > 0) oss << ",";
                        arrayValue_[i].serialize(oss, pretty, depth, indent);
                    }
                }
                oss << ']';
                break;
            case Type::Object:
                oss << '{';
                if (pretty && !objectValue_.empty()) {
                    oss << '\n';
                    size_t i = 0;
                    for (const auto& pair : objectValue_) {
                        oss << std::string((depth + 1) * indent, ' ');
                        oss << '"' << escapeString(pair.first) << "\": ";
                        pair.second.serialize(oss, pretty, depth + 1, indent);
                        if (++i < objectValue_.size()) oss << ",";
                        oss << '\n';
                    }
                    oss << std::string(depth * indent, ' ');
                } else {
                    size_t i = 0;
                    for (const auto& pair : objectValue_) {
                        if (i++ > 0) oss << ",";
                        oss << '"' << escapeString(pair.first) << "\":";
                        pair.second.serialize(oss, pretty, depth, indent);
                    }
                }
                oss << '}';
                break;
        }
    }

    static std::string escapeString(const std::string& s) {
        std::ostringstream oss;
        for (char c : s) {
            switch (c) {
                case '"': oss << "\\\""; break;
                case '\\': oss << "\\\\"; break;
                case '\b': oss << "\\b"; break;
                case '\f': oss << "\\f"; break;
                case '\n': oss << "\\n"; break;
                case '\r': oss << "\\r"; break;
                case '\t': oss << "\\t"; break;
                default:
                    if (static_cast<unsigned char>(c) < 0x20) {
                        oss << "\\u" << std::hex << std::setw(4) << std::setfill('0') << (static_cast<int>(c) & 0xFF);
                    } else {
                        oss << c;
                    }
            }
        }
        return oss.str();
    }

    class Parser {
    public:
        explicit Parser(const std::string& str) : str_(str), pos_(0) {}
        Json parse() {
            skipWhitespace();
            Json result = parseValue();
            skipWhitespace();
            if (pos_ != str_.length()) throw std::runtime_error("Unexpected trailing characters");
            return result;
        }
    private:
        const std::string& str_;
        size_t pos_;
        void skipWhitespace() {
            while (pos_ < str_.length() && std::isspace(static_cast<unsigned char>(str_[pos_]))) ++pos_;
        }
        Json parseValue() {
            skipWhitespace();
            if (pos_ >= str_.length()) throw std::runtime_error("Unexpected end of input");
            char c = str_[pos_];
            if (c == 'n') return parseNull();
            if (c == 't' || c == 'f') return parseBool();
            if (c == '"') return parseString();
            if (c == '[') return parseArray();
            if (c == '{') return parseObject();
            if (c == '-' || std::isdigit(static_cast<unsigned char>(c))) return parseNumber();
            throw std::runtime_error(std::string("Unexpected character: ") + c);
        }
        Json parseNull() { expect("null"); return Json(); }
        Json parseBool() {
            if (str_.substr(pos_, 4) == "true") { pos_ += 4; return Json(true); }
            if (str_.substr(pos_, 5) == "false") { pos_ += 5; return Json(false); }
            throw std::runtime_error("Expected true or false");
        }
        Json parseNumber() {
            size_t start = pos_;
            if (str_[pos_] == '-') ++pos_;
            while (pos_ < str_.length() && std::isdigit(static_cast<unsigned char>(str_[pos_]))) ++pos_;
            if (pos_ < str_.length() && str_[pos_] == '.') {
                ++pos_;
                while (pos_ < str_.length() && std::isdigit(static_cast<unsigned char>(str_[pos_]))) ++pos_;
            }
            if (pos_ < str_.length() && (str_[pos_] == 'e' || str_[pos_] == 'E')) {
                ++pos_;
                if (pos_ < str_.length() && (str_[pos_] == '+' || str_[pos_] == '-')) ++pos_;
                while (pos_ < str_.length() && std::isdigit(static_cast<unsigned char>(str_[pos_]))) ++pos_;
            }
            std::string numStr = str_.substr(start, pos_ - start);
            return Json(std::stod(numStr));
        }
        Json parseString() {
            expect("\"");
            std::string result;
            while (pos_ < str_.length() && str_[pos_] != '"') {
                if (str_[pos_] == '\\') {
                    ++pos_;
                    if (pos_ >= str_.length()) throw std::runtime_error("Unterminated string escape");
                    char c = str_[pos_++];
                    switch (c) {
                        case '"': result += '"'; break;
                        case '\\': result += '\\'; break;
                        case '/': result += '/'; break;
                        case 'b': result += '\b'; break;
                        case 'f': result += '\f'; break;
                        case 'n': result += '\n'; break;
                        case 'r': result += '\r'; break;
                        case 't': result += '\t'; break;
                        case 'u': {
                            if (pos_ + 4 > str_.length()) throw std::runtime_error("Invalid unicode escape");
                            std::string hex = str_.substr(pos_, 4);
                            pos_ += 4;
                            int code = std::stoi(hex, nullptr, 16);
                            if (code < 0x80) result += static_cast<char>(code);
                            else result += '?';
                            break;
                        }
                        default: result += c; break;
                    }
                } else {
                    result += str_[pos_++];
                }
            }
            expect("\"");
            return Json(result);
        }
        Json parseArray() {
            expect("[");
            std::vector<Json> elements;
            skipWhitespace();
            if (pos_ < str_.length() && str_[pos_] != ']') {
                while (true) {
                    elements.push_back(parseValue());
                    skipWhitespace();
                    if (pos_ >= str_.length() || str_[pos_] != ',') break;
                    ++pos_;
                    skipWhitespace();
                }
            }
            expect("]");
            return Json::Array(elements);
        }
        Json parseObject() {
            expect("{");
            std::map<std::string, Json> members;
            skipWhitespace();
            if (pos_ < str_.length() && str_[pos_] != '}') {
                while (true) {
                    skipWhitespace();
                    Json keyJson = parseString();
                    std::string key = keyJson.asString();
                    skipWhitespace();
                    expect(":");
                    members[key] = parseValue();
                    skipWhitespace();
                    if (pos_ >= str_.length() || str_[pos_] != ',') break;
                    ++pos_;
                    skipWhitespace();
                }
            }
            expect("}");
            Json j;
            j.type_ = Type::Object;
            j.objectValue_ = members;
            return j;
        }
        void expect(const std::string& s) {
            if (str_.substr(pos_, s.length()) != s) {
                throw std::runtime_error("Expected: " + s);
            }
            pos_ += s.length();
        }
    };
};

/**
 * @brief Parse JSON string and return Json object
 * @param json JSON string to parse
 * @return Parsed Json object
 */
inline Json parseJson(const std::string& json) {
    return Json::parse(json);
}

/**
 * @brief Convert Json object to string
 * @param json Json object
 * @return JSON string
 */
inline std::string toJsonString(const Json& json) {
    return json.toString();
}

/**
 * @brief Convert Json object to pretty-printed string
 * @param json Json object
 * @param indent Indentation spaces
 * @return Pretty-printed JSON string
 */
inline std::string toPrettyJsonString(const Json& json, int indent = 2) {
    return json.toPrettyString(indent);
}

/**
 * @brief Validate if string is valid JSON
 * @param json String to validate
 * @return true if valid JSON
 */
inline bool isValidJson(const std::string& json) {
    return Json::isValid(json);
}

} // namespace AllToolkit

#endif // ALLTOOLKIT_JSON_UTILS_HPP
