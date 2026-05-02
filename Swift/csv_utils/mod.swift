/**
 * AllToolkit - Swift CSV Utilities
 *
 * CSV 解析和生成工具类，提供完整的 CSV 读写功能。
 * 零依赖，仅使用 Swift 标准库。
 * 支持 iOS 13.0+, macOS 10.15+, watchOS 6.0+, tvOS 13.0+
 *
 * 特性：
 * - 标准 RFC 4180 CSV 格式支持
 * - 自定义分隔符支持
 * - 引号字段处理
 * - 换行符自动检测
 * - 流式解析支持
 * - 类型推断和转换
 * - 大文件处理优化
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// MARK: - CSV Configuration

/// CSV 配置选项
public struct CSVConfiguration {
    /// 字段分隔符（默认为逗号）
    public var delimiter: Character
    
    /// 引号字符（默认为双引号）
    public var quoteCharacter: Character
    
    /// 行分隔符（默认自动检测，可手动指定）
    public var rowSeparator: String?
    
    /// 是否将第一行作为标题行
    public var hasHeader: Bool
    
    /// 是否修剪字段空白
    public var trimWhitespace: Bool
    
    /// 是否允许空字段
    public var allowEmptyFields: Bool
    
    /// 编码格式
    public var encoding: String.Encoding
    
    /// 默认配置
    public init(
        delimiter: Character = ",",
        quoteCharacter: Character = "\"",
        rowSeparator: String? = nil,
        hasHeader: Bool = true,
        trimWhitespace: Bool = false,
        allowEmptyFields: Bool = true,
        encoding: String.Encoding = .utf8
    ) {
        self.delimiter = delimiter
        self.quoteCharacter = quoteCharacter
        self.rowSeparator = rowSeparator
        self.hasHeader = hasHeader
        self.trimWhitespace = trimWhitespace
        self.allowEmptyFields = allowEmptyFields
        self.encoding = encoding
    }
    
    /// 标准 CSV 配置
    public static let standard = CSVConfiguration()
    
    /// TSV（制表符分隔）配置
    public static let tsv = CSVConfiguration(delimiter: "\t")
    
    /// 无标题行的 CSV 配置
    public static let noHeader = CSVConfiguration(hasHeader: false)
    
    /// 分号分隔的 CSV 配置（欧洲常用）
    public static let semicolon = CSVConfiguration(delimiter: ";")
}

// MARK: - CSV Field

/// CSV 字段值
public enum CSVField: Equatable, CustomStringConvertible {
    case string(String)
    case integer(Int)
    case double(Double)
    case boolean(Bool)
    case null
    case empty
    
    public var description: String {
        switch self {
        case .string(let s): return s
        case .integer(let i): return String(i)
        case .double(let d): return String(d)
        case .boolean(let b): return String(b)
        case .null: return "null"
        case .empty: return ""
        }
    }
    
    /// 获取字符串值
    public var stringValue: String {
        switch self {
        case .string(let s): return s
        case .integer(let i): return String(i)
        case .double(let d): return String(d)
        case .boolean(let b): return String(b)
        case .null, .empty: return ""
        }
    }
    
    /// 获取整数值
    public var intValue: Int? {
        switch self {
        case .integer(let i): return i
        case .string(let s): return Int(s.trimmingCharacters(in: .whitespaces))
        case .double(let d): return Int(d)
        default: return nil
        }
    }
    
    /// 获取双精度值
    public var doubleValue: Double? {
        switch self {
        case .double(let d): return d
        case .integer(let i): return Double(i)
        case .string(let s): return Double(s.trimmingCharacters(in: .whitespaces))
        default: return nil
        }
    }
    
    /// 获取布尔值
    public var boolValue: Bool? {
        switch self {
        case .boolean(let b): return b
        case .string(let s):
            let lower = s.lowercased().trimmingCharacters(in: .whitespaces)
            if ["true", "yes", "1", "on"].contains(lower) { return true }
            if ["false", "no", "0", "off"].contains(lower) { return false }
            return nil
        case .integer(let i): return i != 0
        default: return nil
        }
    }
    
    /// 是否为空
    public var isEmpty: Bool {
        switch self {
        case .empty: return true
        case .string(let s): return s.isEmpty
        default: return false
        }
    }
    
    /// 是否为 null
    public var isNull: Bool {
        if case .null = self { return true }
        return false
    }
    
    /// 自动推断类型
    public static func infer(from string: String) -> CSVField {
        let trimmed = string.trimmingCharacters(in: .whitespaces)
        
        if trimmed.isEmpty {
            return .empty
        }
        
        // 检查 null 值
        let lower = trimmed.lowercased()
        if ["null", "nil", "none", "n/a", "na", "-"].contains(lower) {
            return .null
        }
        
        // 检查布尔值
        if ["true", "yes", "on"].contains(lower) {
            return .boolean(true)
        }
        if ["false", "no", "off"].contains(lower) {
            return .boolean(false)
        }
        
        // 检查整数
        if let int = Int(trimmed) {
            return .integer(int)
        }
        
        // 检查双精度
        if let double = Double(trimmed) {
            return .double(double)
        }
        
        return .string(string)
    }
}

// MARK: - CSV Row

/// CSV 行数据
public struct CSVRow: Equatable, CustomStringConvertible, RandomAccessCollection {
    public typealias Element = CSVField
    public typealias Index = Int
    
    private var fields: [CSVField]
    public var header: [String]?
    
    public var startIndex: Int { fields.startIndex }
    public var endIndex: Int { fields.endIndex }
    
    public init(fields: [CSVField], header: [String]? = nil) {
        self.fields = fields
        self.header = header
    }
    
    public init(strings: [String], inferTypes: Bool = true) {
        if inferTypes {
            self.fields = strings.map { CSVField.infer(from: $0) }
        } else {
            self.fields = strings.map { .string($0) }
        }
        self.header = nil
    }
    
    public var description: String {
        let values = fields.map { $0.description }
        return values.joined(separator: ",")
    }
    
    /// 字段数量
    public var count: Int { fields.count }
    
    /// 按索引访问字段
    public subscript(index: Int) -> CSVField {
        get { fields[index] }
        set { fields[index] = newValue }
    }
    
    /// 按列名访问字段
    public subscript(column: String) -> CSVField? {
        guard let header = header,
              let index = header.firstIndex(of: column),
              index < fields.count else {
            return nil
        }
        return fields[index]
    }
    
    /// 获取字符串数组
    public var stringValues: [String] {
        fields.map { $0.stringValue }
    }
    
    /// 获取字段类型
    public func fieldType(at index: Int) -> String {
        let field = fields[index]
        switch field {
        case .string: return "String"
        case .integer: return "Int"
        case .double: return "Double"
        case .boolean: return "Bool"
        case .null: return "Null"
        case .empty: return "Empty"
        }
    }
}

// MARK: - CSV Document

/// CSV 文档
public struct CSVDocument: Equatable, CustomStringConvertible {
    public var rows: [CSVRow]
    public var header: [String]?
    public var configuration: CSVConfiguration
    
    public init(rows: [CSVRow], header: [String]? = nil, configuration: CSVConfiguration = .standard) {
        self.rows = rows
        self.header = header
        self.configuration = configuration
    }
    
    public init(header: [String]? = nil, configuration: CSVConfiguration = .standard) {
        self.rows = []
        self.header = header
        self.configuration = configuration
    }
    
    public var description: String {
        var lines: [String] = []
        if let header = header {
            lines.append(header.joined(separator: String(configuration.delimiter)))
        }
        lines.append(contentsOf: rows.map { $0.description })
        return lines.joined(separator: "\n")
    }
    
    /// 行数
    public var rowCount: Int { rows.count }
    
    /// 列数
    public var columnCount: Int {
        max(header?.count ?? 0, rows.first?.count ?? 0)
    }
    
    /// 添加行
    public mutating func addRow(_ row: CSVRow) {
        rows.append(row)
    }
    
    /// 添加字符串行
    public mutating func addRow(strings: [String]) {
        var row = CSVRow(strings: strings)
        row.header = header
        rows.append(row)
    }
    
    /// 按行索引访问
    public subscript(rowIndex: Int) -> CSVRow {
        get { rows[rowIndex] }
        set { rows[rowIndex] = newValue }
    }
    
    /// 按行列索引访问
    public subscript(rowIndex: Int, columnIndex: Int) -> CSVField {
        get { rows[rowIndex][columnIndex] }
        set { rows[rowIndex][columnIndex] = newValue }
    }
    
    /// 按行列名访问
    public subscript(rowIndex: Int, column: String) -> CSVField? {
        get { rows[rowIndex][column] }
        set {
            guard let header = header,
                  let columnIndex = header.firstIndex(of: column),
                  columnIndex < rows[rowIndex].count else { return }
            rows[rowIndex][columnIndex] = newValue ?? .empty
        }
    }
    
    /// 获取列
    public func column(at index: Int) -> [CSVField] {
        rows.compactMap { $0.count > index ? $0[index] : nil }
    }
    
    /// 按列名获取列数据
    public func column(named name: String) -> [CSVField] {
        guard let header = header,
              let index = header.firstIndex(of: name) else {
            return []
        }
        return column(at: index)
    }
    
    /// 获取所有行作为字典数组
    public var asDictionaries: [[String: CSVField]] {
        guard let header = header else { return [] }
        return rows.map { row in
            var dict: [String: CSVField] = [:]
            for (index, field) in row.fields.enumerated() {
                if index < header.count {
                    dict[header[index]] = field
                }
            }
            return dict
        }
    }
    
    /// 过滤行
    public func filter(_ isIncluded: (CSVRow) -> Bool) -> CSVDocument {
        var doc = CSVDocument(header: header, configuration: configuration)
        doc.rows = rows.filter(isIncluded)
        return doc
    }
    
    /// 排序行
    public func sorted(by areInIncreasingOrder: (CSVRow, CSVRow) -> Bool) -> CSVDocument {
        var doc = CSVDocument(header: header, configuration: configuration)
        doc.rows = rows.sorted(by: areInIncreasingOrder)
        return doc
    }
    
    /// 按列名排序
    public func sorted(by column: String, ascending: Bool = true) -> CSVDocument {
        guard let header = header,
              let columnIndex = header.firstIndex(of: column) else {
            return self
        }
        return sorted { row1, row2 in
            let field1 = row1.count > columnIndex ? row1[columnIndex] : .empty
            let field2 = row2.count > columnIndex ? row2[columnIndex] : .empty
            return ascending ? field1.stringValue < field2.stringValue : field1.stringValue > field2.stringValue
        }
    }
}

// MARK: - CSV Parser

/// CSV 解析器
public class CSVParser {
    private let configuration: CSVConfiguration
    
    public init(configuration: CSVConfiguration = .standard) {
        self.configuration = configuration
    }
    
    /// 解析 CSV 字符串
    public func parse(_ string: String) throws -> CSVDocument {
        let rows = try parseRows(string)
        
        if configuration.hasHeader && !rows.isEmpty {
            let headerStrings = rows[0].stringValues
            var doc = CSVDocument(header: headerStrings, configuration: configuration)
            for i in 1..<rows.count {
                var row = rows[i]
                row.header = headerStrings
                doc.addRow(row)
            }
            return doc
        } else {
            var doc = CSVDocument(configuration: configuration)
            for row in rows {
                doc.addRow(row)
            }
            return doc
        }
    }
    
    /// 解析为行数组
    private func parseRows(_ string: String) throws -> [CSVRow] {
        var rows: [CSVRow] = []
        var currentRow: [String] = []
        var currentField = ""
        var inQuotes = false
        var i = string.startIndex
        
        let delimiter = configuration.delimiter
        let quote = configuration.quoteCharacter
        
        // 确定行分隔符
        let rowSeparator: String
        if let rs = configuration.rowSeparator {
            rowSeparator = rs
        } else {
            rowSeparator = string.contains("\r\n") ? "\r\n" : "\n"
        }
        
        while i < string.endIndex {
            let char = string[i]
            
            if inQuotes {
                if char == quote {
                    // 检查是否是转义引号
                    let nextIndex = string.index(after: i)
                    if nextIndex < string.endIndex && string[nextIndex] == quote {
                        currentField.append(quote)
                        i = string.index(after: nextIndex)
                        continue
                    } else {
                        inQuotes = false
                        i = string.index(after: i)
                        continue
                    }
                } else {
                    currentField.append(char)
                }
            } else {
                if char == quote {
                    inQuotes = true
                } else if char == delimiter {
                    currentRow.append(finalizeField(currentField))
                    currentField = ""
                } else if rowSeparator.contains(char) {
                    // 处理行分隔符
                    currentRow.append(finalizeField(currentField))
                    currentField = ""
                    if !currentRow.isEmpty || !rows.isEmpty {
                        rows.append(CSVRow(strings: currentRow))
                        currentRow = []
                    }
                    // 跳过剩余的行分隔符字符
                    if rowSeparator == "\r\n" && char == "\r" {
                        let nextIndex = string.index(after: i)
                        if nextIndex < string.endIndex && string[nextIndex] == "\n" {
                            i = nextIndex
                        }
                    }
                } else {
                    currentField.append(char)
                }
            }
            
            i = string.index(after: i)
        }
        
        // 处理最后一个字段和行
        currentRow.append(finalizeField(currentField))
        if !currentRow.isEmpty {
            rows.append(CSVRow(strings: currentRow))
        }
        
        return rows
    }
    
    /// 完成字段处理
    private func finalizeField(_ field: String) -> String {
        var result = field
        if configuration.trimWhitespace {
            result = result.trimmingCharacters(in: .whitespaces)
        }
        return result
    }
    
    /// 从文件解析
    public func parseFile(at path: String) throws -> CSVDocument {
        let data = try Data(contentsOf: URL(fileURLWithPath: path))
        guard let string = String(data: data, encoding: configuration.encoding) else {
            throw CSVError.encodingError
        }
        return try parse(string)
    }
    
    /// 从 Data 解析
    public func parse(data: Data) throws -> CSVDocument {
        guard let string = String(data: data, encoding: configuration.encoding) else {
            throw CSVError.encodingError
        }
        return try parse(string)
    }
}

// MARK: - CSV Writer

/// CSV 写入器
public class CSVWriter {
    private let configuration: CSVConfiguration
    
    public init(configuration: CSVConfiguration = .standard) {
        self.configuration = configuration
    }
    
    /// 将 CSV 文档转换为字符串
    public func stringify(_ document: CSVDocument) -> String {
        var lines: [String] = []
        
        // 写入标题行
        if let header = document.header {
            lines.append(encodeRow(header))
        }
        
        // 写入数据行
        for row in document.rows {
            lines.append(encodeRow(row.stringValues))
        }
        
        return lines.joined(separator: configuration.rowSeparator ?? "\n")
    }
    
    /// 将行数据编码为 CSV 字符串
    private func encodeRow(_ values: [String]) -> String {
        values.map { encodeField($0) }.joined(separator: String(configuration.delimiter))
    }
    
    /// 编码单个字段
    private func encodeField(_ field: String) -> String {
        let delimiter = configuration.delimiter
        let quote = configuration.quoteCharacter
        
        // 检查是否需要引号
        let needsQuoting = field.contains(delimiter) ||
                          field.contains(quote) ||
                          field.contains("\n") ||
                          field.contains("\r")
        
        if needsQuoting {
            // 转义引号并包装
            let escaped = field.replacingOccurrences(of: String(quote), with: String(quote) + String(quote))
            return String(quote) + escaped + String(quote)
        }
        
        return field
    }
    
    /// 写入到文件
    public func write(_ document: CSVDocument, to path: String) throws {
        let string = stringify(document)
        guard let data = string.data(using: configuration.encoding) else {
            throw CSVError.encodingError
        }
        try data.write(to: URL(fileURLWithPath: path))
    }
    
    /// 转换为 Data
    public func data(_ document: CSVDocument) throws -> Data {
        let string = stringify(document)
        guard let data = string.data(using: configuration.encoding) else {
            throw CSVError.encodingError
        }
        return data
    }
}

// MARK: - CSV Stream Parser

/// CSV 流式解析器（用于大文件）
public class CSVStreamParser {
    private let configuration: CSVConfiguration
    private var buffer: String = ""
    private var currentRow: [String] = []
    private var currentField: String = ""
    private var inQuotes: Bool = false
    private var header: [String]?
    private var firstRowParsed: Bool = false
    
    public init(configuration: CSVConfiguration = .standard) {
        self.configuration = configuration
    }
    
    /// 重置解析器状态
    public func reset() {
        buffer = ""
        currentRow = []
        currentField = ""
        inQuotes = false
        header = nil
        firstRowParsed = false
    }
    
    /// 输入数据块，返回完成的行
    public func parse(chunk: String) throws -> [CSVRow] {
        buffer += chunk
        var completedRows: [CSVRow] = []
        
        let delimiter = configuration.delimiter
        let quote = configuration.quoteCharacter
        
        var i = buffer.startIndex
        
        while i < buffer.endIndex {
            let char = buffer[i]
            
            if inQuotes {
                if char == quote {
                    let nextIndex = buffer.index(after: i)
                    if nextIndex < buffer.endIndex && buffer[nextIndex] == quote {
                        currentField.append(quote)
                        i = buffer.index(after: nextIndex)
                        continue
                    } else {
                        inQuotes = false
                        i = buffer.index(after: i)
                        continue
                    }
                } else {
                    currentField.append(char)
                }
            } else {
                if char == quote {
                    inQuotes = true
                } else if char == delimiter {
                    currentRow.append(finalizeField(currentField))
                    currentField = ""
                } else if char == "\n" || char == "\r" {
                    currentRow.append(finalizeField(currentField))
                    currentField = ""
                    
                    if !currentRow.isEmpty {
                        let row = CSVRow(strings: currentRow)
                        
                        if configuration.hasHeader && !firstRowParsed {
                            header = currentRow
                            firstRowParsed = true
                        } else {
                            var rowWithHeader = row
                            rowWithHeader.header = header
                            completedRows.append(rowWithHeader)
                        }
                        currentRow = []
                    }
                    
                    // 跳过 \r\n
                    if char == "\r" {
                        let nextIndex = buffer.index(after: i)
                        if nextIndex < buffer.endIndex && buffer[nextIndex] == "\n" {
                            i = nextIndex
                        }
                    }
                } else {
                    currentField.append(char)
                }
            }
            
            i = buffer.index(after: i)
        }
        
        // 保留未处理的数据
        buffer = String(buffer[i...])
        
        return completedRows
    }
    
    /// 完成解析，处理剩余缓冲区
    public func finish() throws -> [CSVRow] {
        var completedRows: [CSVRow] = []
        
        // 处理剩余的缓冲区
        if !currentField.isEmpty || !currentRow.isEmpty {
            currentRow.append(finalizeField(currentField))
            
            if configuration.hasHeader && !firstRowParsed {
                header = currentRow
            } else {
                var row = CSVRow(strings: currentRow)
                row.header = header
                completedRows.append(row)
            }
        }
        
        return completedRows
    }
    
    private func finalizeField(_ field: String) -> String {
        var result = field
        if configuration.trimWhitespace {
            result = result.trimmingCharacters(in: .whitespaces)
        }
        return result
    }
}

// MARK: - CSV Builder

/// CSV 文档构建器（流式 API）
public class CSVBuilder {
    private var document: CSVDocument
    
    public init(header: [String]? = nil, configuration: CSVConfiguration = .standard) {
        self.document = CSVDocument(header: header, configuration: configuration)
    }
    
    /// 添加行
    @discardableResult
    public func row(_ fields: String...) -> CSVBuilder {
        document.addRow(strings: fields)
        return self
    }
    
    /// 添加行
    @discardableResult
    public func row(_ fields: [String]) -> CSVBuilder {
        document.addRow(strings: fields)
        return self
    }
    
    /// 添加整数行
    @discardableResult
    public func row(ints: Int...) -> CSVBuilder {
        document.addRow(strings: ints.map { String($0) })
        return self
    }
    
    /// 添加双精度行
    @discardableResult
    public func row(doubles: Double...) -> CSVBuilder {
        document.addRow(strings: doubles.map { String($0) })
        return self
    }
    
    /// 添加字典行
    @discardableResult
    public func row(dict: [String: Any]) -> CSVBuilder {
        guard let header = document.header else { return self }
        let values = header.map { key in
            if let value = dict[key] {
                return String(describing: value)
            }
            return ""
        }
        document.addRow(strings: values)
        return self
    }
    
    /// 构建 CSV 文档
    public func build() -> CSVDocument {
        return document
    }
    
    /// 构建为字符串
    public func buildString() -> String {
        let writer = CSVWriter(configuration: document.configuration)
        return writer.stringify(document)
    }
}

// MARK: - CSV Errors

/// CSV 错误类型
public enum CSVError: Error, LocalizedError {
    case encodingError
    case invalidFormat(String)
    case unexpectedEndOfFile
    case unescapedQuote
    case rowLengthMismatch(expected: Int, actual: Int)
    case columnNotFound(String)
    case indexOutOfBounds(Int)
    
    public var errorDescription: String? {
        switch self {
        case .encodingError:
            return "CSV encoding error: Unable to encode/decode with specified encoding"
        case .invalidFormat(let message):
            return "CSV invalid format: \(message)"
        case .unexpectedEndOfFile:
            return "CSV parse error: Unexpected end of file"
        case .unescapedQuote:
            return "CSV parse error: Unescaped quote character"
        case .rowLengthMismatch(let expected, let actual):
            return "CSV row length mismatch: expected \(expected) columns, got \(actual)"
        case .columnNotFound(let column):
            return "CSV column not found: \(column)"
        case .indexOutOfBounds(let index):
            return "CSV index out of bounds: \(index)"
        }
    }
}

// MARK: - Convenience Functions

/// 快速解析 CSV 字符串
public func parseCSV(_ string: String, hasHeader: Bool = true) throws -> CSVDocument {
    let config = CSVConfiguration(hasHeader: hasHeader)
    let parser = CSVParser(configuration: config)
    return try parser.parse(string)
}

/// 快速解析 CSV 文件
public func parseCSVFile(at path: String, hasHeader: Bool = true) throws -> CSVDocument {
    let config = CSVConfiguration(hasHeader: hasHeader)
    let parser = CSVParser(configuration: config)
    return try parser.parseFile(at: path)
}

/// 快速创建 CSV 文档
public func createCSV(header: [String]? = nil, rows: [[String]]? = nil) -> CSVDocument {
    var doc = CSVDocument(header: header)
    rows?.forEach { doc.addRow(strings: $0) }
    return doc
}

/// 快速将 CSV 文档转换为字符串
public func stringifyCSV(_ document: CSVDocument) -> String {
    let writer = CSVWriter(configuration: document.configuration)
    return writer.stringify(document)
}

// MARK: - Extensions for Codable Support (Optional)

extension CSVDocument {
    /// 从字典数组创建 CSV 文档
    public init?(from dictionaries: [[String: Any]], configuration: CSVConfiguration = .standard) {
        guard let first = dictionaries.first else {
            self.init(configuration: configuration)
            return
        }
        
        let header = Array(first.keys)
        self.init(header: header, configuration: configuration)
        
        for dict in dictionaries {
            let values = header.map { key in
                if let value = dict[key] {
                    return String(describing: value)
                }
                return ""
            }
            addRow(strings: values)
        }
    }
}

// MARK: - Statistics Utilities

extension CSVDocument {
    /// 获取数值列的统计信息
    public func statistics(forColumn column: String) -> CSVColumnStatistics? {
        let values = column(named: column).compactMap { $0.doubleValue }
        guard !values.isEmpty else { return nil }
        
        let sum = values.reduce(0, +)
        let mean = sum / Double(values.count)
        let sorted = values.sorted()
        let median = sorted.count % 2 == 0
            ? (sorted[sorted.count/2 - 1] + sorted[sorted.count/2]) / 2
            : sorted[sorted.count/2]
        let variance = values.reduce(0) { $0 + ($1 - mean) * ($1 - mean) } / Double(values.count)
        
        return CSVColumnStatistics(
            count: values.count,
            sum: sum,
            mean: mean,
            median: median,
            min: sorted.first!,
            max: sorted.last!,
            variance: variance,
            standardDeviation: sqrt(variance)
        )
    }
    
    /// 获取列的唯一值
    public func uniqueValues(forColumn column: String) -> [String] {
        let values = column(named: column).map { $0.stringValue }
        return Array(Set(values)).sorted()
    }
    
    /// 按列分组
    public func groupBy(column: String) -> [String: [CSVRow]] {
        guard let header = header,
              let columnIndex = header.firstIndex(of: column) else {
            return [:]
        }
        
        var groups: [String: [CSVRow]] = [:]
        for row in rows {
            let key = row.count > columnIndex ? row[columnIndex].stringValue : ""
            groups[key, default: []].append(row)
        }
        return groups
    }
}

/// 列统计信息
public struct CSVColumnStatistics {
    public let count: Int
    public let sum: Double
    public let mean: Double
    public let median: Double
    public let min: Double
    public let max: Double
    public let variance: Double
    public let standardDeviation: Double
    
    public var range: Double { max - min }
}