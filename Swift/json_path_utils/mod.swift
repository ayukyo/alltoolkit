// json_path_utils.swift
// JSON Path 查询工具 - 零外部依赖
// 支持路径表达式查询 JSON 数据

import Foundation

// MARK: - JSON Path Error

public enum JSONPathError: Error, CustomStringConvertible {
    case invalidPath(String)
    case invalidIndex(Int)
    case keyNotFound(String)
    case typeMismatch(expected: String, actual: String)
    case invalidJSON(String)
    
    public var description: String {
        switch self {
        case .invalidPath(let path):
            return "Invalid path expression: \(path)"
        case .invalidIndex(let index):
            return "Invalid array index: \(index)"
        case .keyNotFound(let key):
            return "Key not found: \(key)"
        case .typeMismatch(let expected, let actual):
            return "Type mismatch: expected \(expected), got \(actual)"
        case .invalidJSON(let message):
            return "Invalid JSON: \(message)"
        }
    }
}

// MARK: - JSON Value Type

public enum JSONValue: Equatable, CustomStringConvertible {
    case null
    case bool(Bool)
    case number(Double)
    case string(String)
    case array([JSONValue])
    case object([String: JSONValue])
    
    public var description: String {
        switch self {
        case .null:
            return "null"
        case .bool(let value):
            return value ? "true" : "false"
        case .number(let value):
            return value.truncatingRemainder(dividingBy: 1) == 0 ? String(Int(value)) : String(value)
        case .string(let value):
            return "\"\(value)\""
        case .array(let values):
            let items = values.map { $0.description }.joined(separator: ", ")
            return "[\(items)]"
        case .object(let dict):
            let items = dict.map { "\"\($0.key)\": \($0.value.description)" }.sorted().joined(separator: ", ")
            return "{\(items)}"
        }
    }
    
    // 类型检查
    public var isArray: Bool {
        if case .array = self { return true }
        return false
    }
    
    public var isObject: Bool {
        if case .object = self { return true }
        return false
    }
    
    public var isString: Bool {
        if case .string = self { return true }
        return false
    }
    
    public var isNumber: Bool {
        if case .number = self { return true }
        return false
    }
    
    public var isBool: Bool {
        if case .bool = self { return true }
        return false
    }
    
    public var isNull: Bool {
        if case .null = self { return true }
        return false
    }
    
    // 获取值
    public var asString: String? {
        if case .string(let value) = self { return value }
        return nil
    }
    
    public var asNumber: Double? {
        if case .number(let value) = self { return value }
        return nil
    }
    
    public var asBool: Bool? {
        if case .bool(let value) = self { return value }
        return nil
    }
    
    public var asArray: [JSONValue]? {
        if case .array(let value) = self { return value }
        return nil
    }
    
    public var asObject: [String: JSONValue]? {
        if case .object(let value) = self { return value }
        return nil
    }
    
    public var asInt: Int? {
        if case .number(let value) = self { return Int(value) }
        return nil
    }
}

// MARK: - JSON Path Parser

public struct JSONPath {
    private let tokens: [PathToken]
    
    public enum PathToken: Equatable {
        case root
        case key(String)
        case index(Int)
        case allChildren
        case recursive(String)
        case slice(start: Int?, end: Int?, step: Int?)
        case filter(String)
    }
    
    public init(_ path: String) throws {
        self.tokens = try JSONPathParser.parse(path)
    }
    
    public func query(_ json: JSONValue) -> [JSONValue] {
        var results: [JSONValue] = [json]
        
        for token in tokens {
            var newResults: [JSONValue] = []
            
            for current in results {
                switch token {
                case .root:
                    newResults.append(current)
                case .key(let key):
                    if let obj = current.asObject, let value = obj[key] {
                        newResults.append(value)
                    }
                case .index(let index):
                    if let arr = current.asArray, index >= 0 && index < arr.count {
                        newResults.append(arr[index])
                    }
                case .allChildren:
                    if let obj = current.asObject {
                        newResults.append(contentsOf: obj.values)
                    } else if let arr = current.asArray {
                        newResults.append(contentsOf: arr)
                    }
                case .recursive(let key):
                    newResults.append(contentsOf: recursiveSearch(current, for: key))
                case .slice(let start, let end, let step):
                    if let arr = current.asArray {
                        let sliceResult = sliceArray(arr, start: start, end: end, step: step)
                        newResults.append(contentsOf: sliceResult)
                    }
                case .filter(let expr):
                    if let arr = current.asArray {
                        let filtered = filterArray(arr, expression: expr)
                        newResults.append(contentsOf: filtered)
                    }
                }
            }
            
            results = newResults
        }
        
        return results
    }
    
    private func recursiveSearch(_ json: JSONValue, for key: String) -> [JSONValue] {
        var results: [JSONValue] = []
        
        if let obj = json.asObject {
            if let value = obj[key] {
                results.append(value)
            }
            for (_, value) in obj {
                results.append(contentsOf: recursiveSearch(value, for: key))
            }
        } else if let arr = json.asArray {
            for item in arr {
                results.append(contentsOf: recursiveSearch(item, for: key))
            }
        }
        
        return results
    }
    
    private func sliceArray(_ arr: [JSONValue], start: Int?, end: Int?, step: Int?) -> [JSONValue] {
        let count = arr.count
        let step = step ?? 1
        let start = start ?? (step > 0 ? 0 : count - 1)
        let end = end ?? (step > 0 ? count : -1)
        
        var result: [JSONValue] = []
        var i = start < 0 ? count + start : start
        
        if step > 0 {
            while i < (end < 0 ? count + end : end) && i < count {
                if i >= 0 {
                    result.append(arr[i])
                }
                i += step
            }
        } else if step < 0 {
            while i > (end < 0 ? count + end : end) && i >= 0 {
                if i < count {
                    result.append(arr[i])
                }
                i += step
            }
        }
        
        return result
    }
    
    private func filterArray(_ arr: [JSONValue], expression: String) -> [JSONValue] {
        return arr.filter { item in
            return evaluateFilter(item, expression: expression)
        }
    }
    
    private func evaluateFilter(_ item: JSONValue, expression: String) -> Bool {
        // 简单的过滤器实现，支持基本的比较操作
        // 例如: ".price > 100" 或 ".name == 'test'"
        let trimmed = expression.trimmingCharacters(in: .whitespaces)
        
        // 解析比较表达式
        if let match = trimmed.range(of: #"(^|\s)(@\.?[\w]+)\s*(==|!=|>=|<=|>|<)\s*(['"].*?['"]|\d+\.?\d*)"#, options: .regularExpression) {
            let expr = String(trimmed[match])
            return evaluateComparison(item, expression: expr)
        }
        
        return true
    }
    
    private func evaluateComparison(_ item: JSONValue, expression: String) -> Bool {
        let parts = expression.trimmingCharacters(in: .whitespaces)
            .split(separator: " ", omittingEmptySubsequences: true)
        
        guard parts.count >= 3 else { return true }
        
        let keyPath = String(parts[0]).replacingOccurrences(of: "@.", with: "")
        let operator = String(parts[1])
        let valueStr = String(parts[2]).replacingOccurrences(of: "'", with: "").replacingOccurrences(of: "\"", with: "")
        
        // 获取比较值
        guard let obj = item.asObject, let value = obj[keyPath] else { return false }
        
        // 比较操作
        switch operator {
        case "==":
            if let strVal = value.asString {
                return strVal == valueStr
            }
            if let numVal = value.asNumber, let compareNum = Double(valueStr) {
                return numVal == compareNum
            }
        case "!=":
            if let strVal = value.asString {
                return strVal != valueStr
            }
            if let numVal = value.asNumber, let compareNum = Double(valueStr) {
                return numVal != compareNum
            }
        case ">":
            if let numVal = value.asNumber, let compareNum = Double(valueStr) {
                return numVal > compareNum
            }
        case ">=":
            if let numVal = value.asNumber, let compareNum = Double(valueStr) {
                return numVal >= compareNum
            }
        case "<":
            if let numVal = value.asNumber, let compareNum = Double(valueStr) {
                return numVal < compareNum
            }
        case "<=":
            if let numVal = value.asNumber, let compareNum = Double(valueStr) {
                return numVal <= compareNum
            }
        default:
            return true
        }
        
        return false
    }
}

// MARK: - JSON Path Parser

private struct JSONPathParser {
    static func parse(_ path: String) throws -> [JSONPath.PathToken] {
        var tokens: [JSONPath.PathToken] = []
        var index = path.startIndex
        
        // 跳过空白
        func skipWhitespace() {
            while index < path.endIndex && path[index].isWhitespace {
                index = path.index(after: index)
            }
        }
        
        // 解析标识符
        func parseIdentifier() -> String {
            var result = ""
            while index < path.endIndex {
                let char = path[index]
                if char.isLetter || char.isNumber || char == "_" || char == "-" {
                    result.append(char)
                    index = path.index(after: index)
                } else {
                    break
                }
            }
            return result
        }
        
        // 解析数字
        func parseNumber() -> Int? {
            var numStr = ""
            while index < path.endIndex && path[index].isNumber {
                numStr.append(path[index])
                index = path.index(after: index)
            }
            return Int(numStr)
        }
        
        // 解析引号字符串
        func parseQuotedString() -> String? {
            guard index < path.endIndex && (path[index] == "'" || path[index] == "\"") else { return nil }
            let quote = path[index]
            index = path.index(after: index)
            
            var result = ""
            while index < path.endIndex && path[index] != quote {
                result.append(path[index])
                index = path.index(after: index)
            }
            
            if index < path.endIndex {
                index = path.index(after: index) // 跳过结束引号
            }
            
            return result
        }
        
        skipWhitespace()
        
        // 根节点 $
        if index < path.endIndex && path[index] == "$" {
            tokens.append(.root)
            index = path.index(after: index)
        }
        
        while index < path.endIndex {
            skipWhitespace()
            
            guard index < path.endIndex else { break }
            
            let char = path[index]
            
            // 点号访问 .key
            if char == "." {
                index = path.index(after: index)
                
                if index < path.endIndex && path[index] == "." {
                    // 递归下降 ..key
                    index = path.index(after: index)
                    skipWhitespace()
                    let key = parseIdentifier()
                    tokens.append(.recursive(key))
                } else if index < path.endIndex && path[index] == "*" {
                    // 通配符 .*
                    index = path.index(after: index)
                    tokens.append(.allChildren)
                } else {
                    // 普通键访问
                    let key = parseIdentifier()
                    if key.isEmpty {
                        throw JSONPathError.invalidPath(path)
                    }
                    tokens.append(.key(key))
                }
            }
            // 方括号访问 [index] 或 [key] 或 [slice] 或 [?filter]
            else if char == "[" {
                index = path.index(after: index)
                skipWhitespace()
                
                guard index < path.endIndex else { throw JSONPathError.invalidPath(path) }
                
                let innerChar = path[index]
                
                // 通配符 [*]
                if innerChar == "*" {
                    index = path.index(after: index)
                    tokens.append(.allChildren)
                }
                // 过滤器 [?(@.price < 10)]
                else if innerChar == "?" {
                    index = path.index(after: index)
                    skipWhitespace()
                    
                    // 解析过滤表达式
                    var filterExpr = ""
                    var depth = 0
                    while index < path.endIndex {
                        let c = path[index]
                        if c == "[" { depth += 1 }
                        else if c == "]" {
                            if depth == 0 { break }
                            depth -= 1
                        }
                        filterExpr.append(c)
                        index = path.index(after: index)
                    }
                    tokens.append(.filter(filterExpr))
                }
                // 字符串键 ['key'] 或 ["key"]
                else if innerChar == "'" || innerChar == "\"" {
                    if let key = parseQuotedString() {
                        tokens.append(.key(key))
                    }
                }
                // 切片 [start:end:step]
                else if innerChar == ":" || innerChar.isNumber || innerChar == "-" {
                    var start: Int? = nil
                    var end: Int? = nil
                    var step: Int? = nil
                    
                    // 解析 start
                    if innerChar == ":" {
                        index = path.index(after: index)
                    } else {
                        if let num = parseNumber() {
                            start = num
                        }
                        skipWhitespace()
                        if index < path.endIndex && path[index] == ":" {
                            index = path.index(after: index)
                        }
                    }
                    
                    // 解析 end
                    skipWhitespace()
                    if index < path.endIndex && path[index] != ":" && path[index] != "]" {
                        if let num = parseNumber() {
                            end = num
                        }
                    }
                    
                    // 解析 step
                    skipWhitespace()
                    if index < path.endIndex && path[index] == ":" {
                        index = path.index(after: index)
                        skipWhitespace()
                        if let num = parseNumber() {
                            step = num
                        }
                    }
                    
                    tokens.append(.slice(start: start, end: end, step: step))
                }
                // 数字索引
                else if innerChar.isNumber {
                    if let num = parseNumber() {
                        tokens.append(.index(num))
                    }
                }
                
                skipWhitespace()
                if index < path.endIndex && path[index] == "]" {
                    index = path.index(after: index)
                }
            }
            else {
                // 未知字符，跳过
                index = path.index(after: index)
            }
        }
        
        return tokens.isEmpty ? [.root] : tokens
    }
}

// MARK: - JSON Parser

public struct JSONParser {
    public static func parse(_ data: Data) throws -> JSONValue {
        guard let json = try? JSONSerialization.jsonObject(with: data, options: [.allowFragments]) else {
            throw JSONPathError.invalidJSON("Failed to parse JSON data")
        }
        return convert(json)
    }
    
    public static func parse(_ string: String) throws -> JSONValue {
        guard let data = string.data(using: .utf8) else {
            throw JSONPathError.invalidJSON("Invalid UTF-8 string")
        }
        return try parse(data)
    }
    
    private static func convert(_ json: Any) -> JSONValue {
        if json is NSNull {
            return .null
        } else if let bool = json as? Bool {
            return .bool(bool)
        } else if let number = json as? NSNumber {
            return .number(number.doubleValue)
        } else if let string = json as? String {
            return .string(string)
        } else if let array = json as? [Any] {
            return .array(array.map { convert($0) })
        } else if let dict = json as? [String: Any] {
            return .object(dict.mapValues { convert($0) })
        }
        return .null
    }
}

// MARK: - JSON Builder

public struct JSONBuilder {
    public static func build(_ value: JSONValue, pretty: Bool = false) -> String {
        if pretty {
            return buildPretty(value, indent: 0)
        }
        return buildCompact(value)
    }
    
    private static func buildCompact(_ value: JSONValue) -> String {
        switch value {
        case .null:
            return "null"
        case .bool(let b):
            return b ? "true" : "false"
        case .number(let n):
            if n.truncatingRemainder(dividingBy: 1) == 0 {
                return String(Int(n))
            }
            return String(n)
        case .string(let s):
            return "\"\(escapeString(s))\""
        case .array(let arr):
            let items = arr.map { buildCompact($0) }.joined(separator: ",")
            return "[\(items)]"
        case .object(let dict):
            let items = dict.map { "\"\(escapeString($0.key))\":\(buildCompact($0.value))" }
                .sorted()
                .joined(separator: ",")
            return "{\(items)}"
        }
    }
    
    private static func buildPretty(_ value: JSONValue, indent: Int) -> String {
        let indentStr = String(repeating: "  ", count: indent)
        let nextIndent = String(repeating: "  ", count: indent + 1)
        
        switch value {
        case .null:
            return "null"
        case .bool(let b):
            return b ? "true" : "false"
        case .number(let n):
            if n.truncatingRemainder(dividingBy: 1) == 0 {
                return String(Int(n))
            }
            return String(n)
        case .string(let s):
            return "\"\(escapeString(s))\""
        case .array(let arr):
            if arr.isEmpty {
                return "[]"
            }
            let items = arr.map { "\(nextIndent)\(buildPretty($0, indent: indent + 1))" }
                .joined(separator: ",\n")
            return "[\n\(items)\n\(indentStr)]"
        case .object(let dict):
            if dict.isEmpty {
                return "{}"
            }
            let items = dict.map { "\(nextIndent)\"\(escapeString($0.key))\": \(buildPretty($0.value, indent: indent + 1))" }
                .sorted()
                .joined(separator: ",\n")
            return "{\n\(items)\n\(indentStr)}"
        }
    }
    
    private static func escapeString(_ s: String) -> String {
        return s
            .replacingOccurrences(of: "\\", with: "\\\\")
            .replacingOccurrences(of: "\"", with: "\\\"")
            .replacingOccurrences(of: "\n", with: "\\n")
            .replacingOccurrences(of: "\r", with: "\\r")
            .replacingOccurrences(of: "\t", with: "\\t")
    }
}

// MARK: - JSON Path Utils Main Class

public class JSONPathUtils {
    
    /// 从字符串解析 JSON
    public static func parse(_ jsonString: String) throws -> JSONValue {
        return try JSONParser.parse(jsonString)
    }
    
    /// 从 Data 解析 JSON
    public static func parse(_ data: Data) throws -> JSONValue {
        return try JSONParser.parse(data)
    }
    
    /// 查询 JSON 值
    public static func query(_ json: JSONValue, path: String) throws -> [JSONValue] {
        let jsonPath = try JSONPath(path)
        return jsonPath.query(json)
    }
    
    /// 查询并返回第一个结果
    public static func queryFirst(_ json: JSONValue, path: String) throws -> JSONValue? {
        let results = try query(json, path: path)
        return results.first
    }
    
    /// 查询并返回单个值
    public static func queryValue<T>(_ json: JSONValue, path: String, transform: (JSONValue) throws -> T) throws -> T? {
        guard let value = try queryFirst(json, path: path) else { return nil }
        return try transform(value)
    }
    
    /// 获取字符串值
    public static func getString(_ json: JSONValue, path: String) throws -> String? {
        return try queryValue(json, path: path) { $0.asString }
    }
    
    /// 获取数字值
    public static func getNumber(_ json: JSONValue, path: String) throws -> Double? {
        return try queryValue(json, path: path) { $0.asNumber }
    }
    
    /// 获取整数值
    public static func getInt(_ json: JSONValue, path: String) throws -> Int? {
        return try queryValue(json, path: path) { $0.asInt }
    }
    
    /// 获取布尔值
    public static func getBool(_ json: JSONValue, path: String) throws -> Bool? {
        return try queryValue(json, path: path) { $0.asBool }
    }
    
    /// 获取数组
    public static func getArray(_ json: JSONValue, path: String) throws -> [JSONValue]? {
        return try queryValue(json, path: path) { $0.asArray }
    }
    
    /// 获取对象
    public static func getObject(_ json: JSONValue, path: String) throws -> [String: JSONValue]? {
        return try queryValue(json, path: path) { $0.asObject }
    }
    
    /// 将 JSON 值转为字符串
    public static func stringify(_ value: JSONValue, pretty: Bool = false) -> String {
        return JSONBuilder.build(value, pretty: pretty)
    }
    
    /// 从字典创建 JSON 值
    public static func fromDictionary(_ dict: [String: Any]) -> JSONValue {
        return convertToJSONValue(dict)
    }
    
    /// 从数组创建 JSON 值
    public static func fromArray(_ arr: [Any]) -> JSONValue {
        return .array(arr.map { convertToJSONValue($0) })
    }
    
    /// 验证 JSON 字符串
    public static func validate(_ jsonString: String) -> (valid: Bool, error: String?) {
        do {
            _ = try parse(jsonString)
            return (true, nil)
        } catch {
            return (false, error.localizedDescription)
        }
    }
    
    /// 合并两个 JSON 对象
    public static func merge(_ base: JSONValue, _ overlay: JSONValue) -> JSONValue {
        switch (base, overlay) {
        case (.object(var baseDict), .object(let overlayDict)):
            for (key, value) in overlayDict {
                if let baseValue = baseDict[key] {
                    baseDict[key] = merge(baseValue, value)
                } else {
                    baseDict[key] = value
                }
            }
            return .object(baseDict)
        case (.array(var baseArr), .array(let overlayArr)):
            baseArr.append(contentsOf: overlayArr)
            return .array(baseArr)
        default:
            return overlay
        }
    }
    
    /// 深拷贝
    public static func deepCopy(_ value: JSONValue) -> JSONValue {
        switch value {
        case .null:
            return .null
        case .bool(let b):
            return .bool(b)
        case .number(let n):
            return .number(n)
        case .string(let s):
            return .string(s)
        case .array(let arr):
            return .array(arr.map { deepCopy($0) })
        case .object(let dict):
            return .object(dict.mapValues { deepCopy($0) })
        }
    }
    
    /// 获取所有键
    public static func getAllKeys(_ json: JSONValue) -> [String] {
        var keys: [String] = []
        collectKeys(json, keys: &keys)
        return keys
    }
    
    private static func collectKeys(_ json: JSONValue, keys: inout [String]) {
        switch json {
        case .object(let dict):
            for (key, value) in dict {
                keys.append(key)
                collectKeys(value, keys: &keys)
            }
        case .array(let arr):
            for item in arr {
                collectKeys(item, keys: &keys)
            }
        default:
            break
        }
    }
    
    /// 获取所有叶子节点的值
    public static func getLeafValues(_ json: JSONValue) -> [JSONValue] {
        var leaves: [JSONValue] = []
        collectLeaves(json, leaves: &leaves)
        return leaves
    }
    
    private static func collectLeaves(_ json: JSONValue, leaves: inout [JSONValue]) {
        switch json {
        case .object(let dict):
            for (_, value) in dict {
                collectLeaves(value, leaves: &leaves)
            }
        case .array(let arr):
            for item in arr {
                collectLeaves(item, leaves: &leaves)
            }
        default:
            leaves.append(json)
        }
    }
    
    private static func convertToJSONValue(_ value: Any) -> JSONValue {
        if value is NSNull {
            return .null
        } else if let bool = value as? Bool {
            return .bool(bool)
        } else if let number = value as? NSNumber {
            return .number(number.doubleValue)
        } else if let string = value as? String {
            return .string(string)
        } else if let array = value as? [Any] {
            return .array(array.map { convertToJSONValue($0) })
        } else if let dict = value as? [String: Any] {
            return .object(dict.mapValues { convertToJSONValue($0) })
        }
        return .null
    }
}

// MARK: - Convenience Extensions

public extension JSONValue {
    /// 使用路径查询
    func query(_ path: String) throws -> [JSONValue] {
        return try JSONPathUtils.query(self, path: path)
    }
    
    /// 获取第一个匹配项
    func queryFirst(_ path: String) throws -> JSONValue? {
        return try JSONPathUtils.queryFirst(self, path: path)
    }
    
    /// 转为 JSON 字符串
    func stringify(pretty: Bool = false) -> String {
        return JSONPathUtils.stringify(self, pretty: pretty)
    }
}

public extension String {
    /// 解析为 JSON
    func parseJSON() throws -> JSONValue {
        return try JSONPathUtils.parse(self)
    }
    
    /// 验证是否为有效 JSON
    var isValidJSON: Bool {
        return JSONPathUtils.validate(self).valid
    }
}