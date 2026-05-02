/**
 * AllToolkit - Swift CSV Utilities Tests
 *
 * 测试 CSV 解析和生成功能
 */

import Foundation

// 测试辅助函数
func assertEquals<T: Equatable>(_ actual: T, _ expected: T, _ message: String = "") -> Bool {
    if actual == expected {
        return true
    } else {
        print("❌ 断言失败: \(message.isEmpty ? "" : message + " - ")期望 \(expected)，实际 \(actual)")
        return false
    }
}

func assertTrue(_ condition: Bool, _ message: String = "") -> Bool {
    if condition {
        return true
    } else {
        print("❌ 断言失败: \(message)")
        return false
    }
}

var testsPassed = 0
var testsFailed = 0

func runTest(_ name: String, _ test: () -> Bool) {
    print("\n📋 测试: \(name)")
    if test() {
        print("✅ 通过")
        testsPassed += 1
    } else {
        print("❌ 失败")
        testsFailed += 1
    }
}

// MARK: - CSVField Tests

func testCSVFieldString() -> Bool {
    let field = CSVField.string("hello")
    return assertEquals(field.stringValue, "hello") &&
           assertEquals(field.description, "hello") &&
           assertTrue(!field.isEmpty) &&
           assertTrue(!field.isNull)
}

func testCSVFieldInteger() -> Bool {
    let field = CSVField.integer(42)
    return assertEquals(field.intValue, 42) &&
           assertEquals(field.doubleValue, 42.0) &&
           assertEquals(field.stringValue, "42") &&
           assertTrue(field.boolValue == true)
}

func testCSVFieldDouble() -> Bool {
    let field = CSVField.double(3.14)
    return assertEquals(field.doubleValue!, 3.14, accuracy: 0.001) &&
           assertEquals(field.intValue, 3) &&
           assertEquals(field.stringValue, "3.14")
}

func testCSVFieldBoolean() -> Bool {
    let trueField = CSVField.boolean(true)
    let falseField = CSVField.boolean(false)
    return assertEquals(trueField.boolValue, true) &&
           assertEquals(falseField.boolValue, false) &&
           assertEquals(trueField.stringValue, "true")
}

func testCSVFieldEmpty() -> Bool {
    let field = CSVField.empty
    return assertTrue(field.isEmpty) &&
           assertTrue(!field.isNull) &&
           assertEquals(field.stringValue, "")
}

func testCSVFieldNull() -> Bool {
    let field = CSVField.null
    return assertTrue(field.isNull) &&
           assertTrue(!field.isEmpty) &&
           assertEquals(field.stringValue, "")
}

func testCSVFieldInfer() -> Bool {
    return assertEquals(CSVField.infer(from: "123"), .integer(123)) &&
           assertEquals(CSVField.infer(from: "3.14"), .double(3.14)) &&
           assertEquals(CSVField.infer(from: "true"), .boolean(true)) &&
           assertEquals(CSVField.infer(from: "false"), .boolean(false)) &&
           assertEquals(CSVField.infer(from: "null"), .null) &&
           assertEquals(CSVField.infer(from: "hello"), .string("hello")) &&
           assertEquals(CSVField.infer(from: ""), .empty)
}

// MARK: - CSVRow Tests

func testCSVRowBasic() -> Bool {
    let row = CSVRow(strings: ["a", "b", "c"])
    return assertEquals(row.count, 3) &&
           assertEquals(row[0].stringValue, "a") &&
           assertEquals(row[1].stringValue, "b") &&
           assertEquals(row[2].stringValue, "c")
}

func testCSVRowWithHeader() -> Bool {
    var row = CSVRow(strings: ["Alice", "30", "true"])
    row.header = ["name", "age", "active"]
    return assertEquals(row["name"]?.stringValue, "Alice") &&
           assertEquals(row["age"]?.intValue, 30) &&
           assertEquals(row["active"]?.boolValue, true)
}

func testCSVRowDescription() -> Bool {
    let row = CSVRow(strings: ["apple", "banana", "cherry"])
    return assertEquals(row.description, "apple,banana,cherry")
}

// MARK: - CSVParser Tests

func testParseSimpleCSV() -> Bool {
    let csv = "name,age,city\nAlice,30,Beijing\nBob,25,Shanghai"
    let parser = CSVParser(configuration: .standard)
    
    do {
        let doc = try parser.parse(csv)
        return assertEquals(doc.header?.count, 3) &&
               assertEquals(doc.header?[0], "name") &&
               assertEquals(doc.rowCount, 2) &&
               assertEquals(doc[0, "name"]?.stringValue, "Alice") &&
               assertEquals(doc[0, "age"]?.intValue, 30) &&
               assertEquals(doc[1, "city"]?.stringValue, "Shanghai")
    } catch {
        print("解析错误: \(error)")
        return false
    }
}

func testParseCSVWithQuotes() -> Bool {
    let csv = "name,description\n\"Alice\",\"Loves, coding\"\n\"Bob\",\"Says \"\"hello\"\"\""
    let parser = CSVParser()
    
    do {
        let doc = try parser.parse(csv)
        return assertEquals(doc[0, "description"]?.stringValue, "Loves, coding") &&
               assertEquals(doc[1, "description"]?.stringValue, "Says \"hello\"")
    } catch {
        print("解析错误: \(error)")
        return false
    }
}

func testParseCSVNoHeader() -> Bool {
    let csv = "Alice,30\nBob,25"
    let parser = CSVParser(configuration: .noHeader)
    
    do {
        let doc = try parser.parse(csv)
        return assertEquals(doc.header, nil as [String]?) &&
               assertEquals(doc.rowCount, 2) &&
               assertEquals(doc[0, 0].stringValue, "Alice") &&
               assertEquals(doc[1, 1].stringValue, "25")
    } catch {
        print("解析错误: \(error)")
        return false
    }
}

func testParseTSV() -> Bool {
    let tsv = "name\tage\nAlice\t30\nBob\t25"
    let parser = CSVParser(configuration: .tsv)
    
    do {
        let doc = try parser.parse(tsv)
        return assertEquals(doc.header?.count, 2) &&
               assertEquals(doc[0, "name"]?.stringValue, "Alice") &&
               assertEquals(doc[0, "age"]?.stringValue, "30")
    } catch {
        print("解析错误: \(error)")
        return false
    }
}

func testParseCSVWithNewlines() -> Bool {
    let csv = "name,address\n\"Alice\",\"Line1\nLine2\"\n\"Bob\",\"Single Line\""
    let parser = CSVParser()
    
    do {
        let doc = try parser.parse(csv)
        return assertEquals(doc.rowCount, 2) &&
               assertEquals(doc[0, "address"]?.stringValue, "Line1\nLine2") &&
               assertEquals(doc[1, "address"]?.stringValue, "Single Line")
    } catch {
        print("解析错误: \(error)")
        return false
    }
}

func testParseCSVWithEmptyFields() -> Bool {
    let csv = "a,b,c\n1,,3\n,2,"
    let parser = CSVParser()
    
    do {
        let doc = try parser.parse(csv)
        return assertEquals(doc[0, 1].isEmpty, true) &&
               assertEquals(doc[1, 0].isEmpty, true) &&
               assertEquals(doc[1, 2].isEmpty, true) &&
               assertEquals(doc[0, 0].stringValue, "1") &&
               assertEquals(doc[0, 2].stringValue, "3")
    } catch {
        print("解析错误: \(error)")
        return false
    }
}

func testParseCSVWithCRLF() -> Bool {
    let csv = "name,age\r\nAlice,30\r\nBob,25"
    let parser = CSVParser()
    
    do {
        let doc = try parser.parse(csv)
        return assertEquals(doc.rowCount, 2) &&
               assertEquals(doc[0, "name"]?.stringValue, "Alice")
    } catch {
        print("解析错误: \(error)")
        return false
    }
}

func testParseSemicolonCSV() -> Bool {
    let csv = "name;age\nAlice;30\nBob;25"
    let parser = CSVParser(configuration: .semicolon)
    
    do {
        let doc = try parser.parse(csv)
        return assertEquals(doc.rowCount, 2) &&
               assertEquals(doc[0, "name"]?.stringValue, "Alice")
    } catch {
        print("解析错误: \(error)")
        return false
    }
}

// MARK: - CSVWriter Tests

func testWriteSimpleCSV() -> Bool {
    var doc = CSVDocument(header: ["name", "age", "city"])
    doc.addRow(strings: ["Alice", "30", "Beijing"])
    doc.addRow(strings: ["Bob", "25", "Shanghai"])
    
    let writer = CSVWriter()
    let result = writer.stringify(doc)
    
    return assertTrue(result.contains("name,age,city")) &&
           assertTrue(result.contains("Alice,30,Beijing")) &&
           assertTrue(result.contains("Bob,25,Shanghai"))
}

func testWriteCSVWithQuotes() -> Bool {
    var doc = CSVDocument(header: ["name", "description"])
    doc.addRow(strings: ["Alice", "Loves, coding"])
    doc.addRow(strings: ["Bob", "Says \"hello\""])
    
    let writer = CSVWriter()
    let result = writer.stringify(doc)
    
    return assertTrue(result.contains("\"Loves, coding\"")) &&
           assertTrue(result.contains("\"Says \"\"hello\"\"\""))
}

func testWriteTSV() -> Bool {
    var doc = CSVDocument(header: ["name", "age"], configuration: .tsv)
    doc.addRow(strings: ["Alice", "30"])
    
    let writer = CSVWriter(configuration: .tsv)
    let result = writer.stringify(doc)
    
    return assertTrue(result.contains("name\tage")) &&
           assertTrue(result.contains("Alice\t30"))
}

func testRoundTrip() -> Bool {
    var original = CSVDocument(header: ["name", "age", "city"])
    original.addRow(strings: ["Alice", "30", "Beijing"])
    original.addRow(strings: ["Bob", "25", "Shanghai"])
    
    let writer = CSVWriter()
    let parser = CSVParser()
    
    do {
        let csvString = writer.stringify(original)
        let parsed = try parser.parse(csvString)
        
        return assertEquals(parsed.rowCount, original.rowCount) &&
               assertEquals(parsed.header, original.header) &&
               assertEquals(parsed[0, "name"]?.stringValue, original[0, "name"]?.stringValue) &&
               assertEquals(parsed[1, "city"]?.stringValue, original[1, "city"]?.stringValue)
    } catch {
        print("Round trip 错误: \(error)")
        return false
    }
}

// MARK: - CSVBuilder Tests

func testBuilderBasic() -> Bool {
    let csv = CSVBuilder(header: ["name", "age", "city"])
        .row("Alice", "30", "Beijing")
        .row("Bob", "25", "Shanghai")
        .build()
    
    return assertEquals(csv.rowCount, 2) &&
           assertEquals(csv.header, ["name", "age", "city"]) &&
           assertEquals(csv[0, "name"]?.stringValue, "Alice")
}

func testBuilderWithTypes() -> Bool {
    let csv = CSVBuilder(header: ["name", "score", "rating"])
        .row(ints: 1, 2, 3)
        .row(doubles: 1.5, 2.5, 3.5)
        .build()
    
    return assertEquals(csv.rowCount, 2) &&
           assertEquals(csv[0, 0].stringValue, "1") &&
           assertEquals(csv[1, 1].stringValue, "2.5")
}

func testBuilderWithStringify() -> Bool {
    let csvString = CSVBuilder(header: ["a", "b"])
        .row("1", "2")
        .buildString()
    
    return assertTrue(csvString.contains("a,b")) &&
           assertTrue(csvString.contains("1,2"))
}

// MARK: - CSVDocument Operations Tests

func testDocumentFilter() -> Bool {
    var doc = CSVDocument(header: ["name", "age"])
    doc.addRow(strings: ["Alice", "30"])
    doc.addRow(strings: ["Bob", "25"])
    doc.addRow(strings: ["Charlie", "35"])
    
    let filtered = doc.filter { row in
        guard let age = row["age"]?.intValue else { return false }
        return age >= 30
    }
    
    return assertEquals(filtered.rowCount, 2) &&
           assertEquals(filtered[0, "name"]?.stringValue, "Alice") &&
           assertEquals(filtered[1, "name"]?.stringValue, "Charlie")
}

func testDocumentSort() -> Bool {
    var doc = CSVDocument(header: ["name", "age"])
    doc.addRow(strings: ["Charlie", "35"])
    doc.addRow(strings: ["Alice", "30"])
    doc.addRow(strings: ["Bob", "25"])
    
    let sorted = doc.sorted(by: "age")
    
    return assertEquals(sorted[0, "name"]?.stringValue, "Bob") &&
           assertEquals(sorted[1, "name"]?.stringValue, "Alice") &&
           assertEquals(sorted[2, "name"]?.stringValue, "Charlie")
}

func testDocumentColumnAccess() -> Bool {
    var doc = CSVDocument(header: ["name", "age"])
    doc.addRow(strings: ["Alice", "30"])
    doc.addRow(strings: ["Bob", "25"])
    doc.addRow(strings: ["Charlie", "30"])
    
    let names = doc.column(named: "name")
    let ages = doc.column(named: "age")
    
    return assertEquals(names.count, 3) &&
           assertEquals(names[0].stringValue, "Alice") &&
           assertEquals(ages.count, 3)
}

func testDocumentAsDictionaries() -> Bool {
    var doc = CSVDocument(header: ["name", "age"])
    doc.addRow(strings: ["Alice", "30"])
    doc.addRow(strings: ["Bob", "25"])
    
    let dicts = doc.asDictionaries
    
    return assertEquals(dicts.count, 2) &&
           assertEquals(dicts[0]["name"]?.stringValue, "Alice") &&
           assertEquals(dicts[0]["age"]?.stringValue, "30") &&
           assertEquals(dicts[1]["name"]?.stringValue, "Bob")
}

// MARK: - Statistics Tests

func testStatistics() -> Bool {
    var doc = CSVDocument(header: ["name", "score"])
    doc.addRow(strings: ["A", "10"])
    doc.addRow(strings: ["B", "20"])
    doc.addRow(strings: ["C", "30"])
    doc.addRow(strings: ["D", "40"])
    doc.addRow(strings: ["E", "50"])
    
    let stats = doc.statistics(forColumn: "score")
    
    return stats != nil &&
           assertEquals(stats!.count, 5) &&
           assertEquals(stats!.sum, 150.0, accuracy: 0.001) &&
           assertEquals(stats!.mean, 30.0, accuracy: 0.001) &&
           assertEquals(stats!.median, 30.0, accuracy: 0.001) &&
           assertEquals(stats!.min, 10.0, accuracy: 0.001) &&
           assertEquals(stats!.max, 50.0, accuracy: 0.001)
}

func testUniqueValues() -> Bool {
    var doc = CSVDocument(header: ["category"])
    doc.addRow(strings: ["A"])
    doc.addRow(strings: ["B"])
    doc.addRow(strings: ["A"])
    doc.addRow(strings: ["C"])
    doc.addRow(strings: ["B"])
    
    let unique = doc.uniqueValues(forColumn: "category")
    
    return assertEquals(unique.count, 3) &&
           assertTrue(unique.contains("A")) &&
           assertTrue(unique.contains("B")) &&
           assertTrue(unique.contains("C"))
}

func testGroupBy() -> Bool {
    var doc = CSVDocument(header: ["name", "category"])
    doc.addRow(strings: ["Apple", "Fruit"])
    doc.addRow(strings: ["Carrot", "Vegetable"])
    doc.addRow(strings: ["Banana", "Fruit"])
    doc.addRow(strings: ["Broccoli", "Vegetable"])
    
    let groups = doc.groupBy(column: "category")
    
    return assertEquals(groups.count, 2) &&
           assertEquals(groups["Fruit"]?.count, 2) &&
           assertEquals(groups["Vegetable"]?.count, 2)
}

// MARK: - Stream Parser Tests

func testStreamParser() -> Bool {
    let config = CSVConfiguration(hasHeader: true)
    let streamParser = CSVStreamParser(configuration: config)
    
    let chunk1 = "name,age\nAli"
    let chunk2 = "ce,30\nBob"
    let chunk3 = ",25\n"
    
    do {
        let rows1 = try streamParser.parse(chunk: chunk1)
        let rows2 = try streamParser.parse(chunk: chunk2)
        let rows3 = try streamParser.parse(chunk: chunk3)
        let final = try streamParser.finish()
        
        return assertEquals(rows1.count, 0) && // 第一行是 header，不作为数据返回
               assertEquals(rows2.count, 1) &&
               assertEquals(rows2[0]["name"]?.stringValue, "Alice") &&
               assertEquals(rows3.count, 1) &&
               assertEquals(rows3[0]["name"]?.stringValue, "Bob") &&
               assertEquals(final.count, 0)
    } catch {
        print("Stream parser 错误: \(error)")
        return false
    }
}

// MARK: - Convenience Functions Tests

func testConvenienceFunctions() -> Bool {
    do {
        // 测试 parseCSV
        let doc = try parseCSV("a,b\n1,2", hasHeader: true)
        if doc.rowCount != 1 { return false }
        
        // 测试 createCSV
        let doc2 = createCSV(header: ["x", "y"], rows: [["1", "2"], ["3", "4"]])
        if doc2.rowCount != 2 { return false }
        
        // 测试 stringifyCSV
        let str = stringifyCSV(doc2)
        if !str.contains("x,y") { return false }
        
        return true
    } catch {
        print("Convenience function 错误: \(error)")
        return false
    }
}

// MARK: - Error Tests

func testErrors() -> Bool {
    do {
        let doc = CSVDocument(header: ["a", "b"])
        doc.addRow(strings: ["1"])
        
        // 访问不存在的列应该返回 nil
        let value = doc[0, "nonexistent"]
        if value != nil {
            return false
        }
        
        return true
    }
}

// MARK: - Complex Real-World Test

func testRealWorldCSV() -> Bool {
    let csvData = """
    id,name,email,age,active,salary
    1,Alice Smith,alice@example.com,30,true,50000.50
    2,Bob Johnson,bob@example.com,25,false,45000.00
    3,Charlie Brown,charlie@example.com,35,true,60000.75
    "4","Diana ""Di"" Williams","diana@example.com",28,true,"75,000.00"
    """
    
    let parser = CSVParser()
    
    do {
        let doc = try parser.parse(csvData)
        
        // 验证解析结果
        if doc.rowCount != 4 { return false }
        
        // 测试类型推断
        if doc[0, "age"]?.intValue != 30 { return false }
        if doc[0, "active"]?.boolValue != true { return false }
        if doc[0, "salary"]?.doubleValue != 50000.50 { return false }
        
        // 测试引号转义
        if doc[3, "name"]?.stringValue != "Diana \"Di\" Williams" { return false }
        
        // 测试包含逗号的字段
        if doc[3, "salary"]?.stringValue != "75,000.00" { return false }
        
        // 测试统计
        let stats = doc.statistics(forColumn: "age")
        if stats?.mean != 29.5 { return false }
        
        // 测试过滤和排序
        let activeUsers = doc.filter { $0["active"]?.boolValue == true }
        if activeUsers.rowCount != 3 { return false }
        
        return true
    } catch {
        print("Real-world test 错误: \(error)")
        return false
    }
}

// MARK: - Run All Tests

print("=" + String(repeating: "=", count: 59))
print("AllToolkit Swift CSV Utilities Tests")
print(String(repeating: "=", count: 60))

runTest("CSVField String", testCSVFieldString)
runTest("CSVField Integer", testCSVFieldInteger)
runTest("CSVField Double", testCSVFieldDouble)
runTest("CSVField Boolean", testCSVFieldBoolean)
runTest("CSVField Empty", testCSVFieldEmpty)
runTest("CSVField Null", testCSVFieldNull)
runTest("CSVField Type Inference", testCSVFieldInfer)

runTest("CSVRow Basic", testCSVRowBasic)
runTest("CSVRow With Header", testCSVRowWithHeader)
runTest("CSVRow Description", testCSVRowDescription)

runTest("Parse Simple CSV", testParseSimpleCSV)
runTest("Parse CSV With Quotes", testParseCSVWithQuotes)
runTest("Parse CSV No Header", testParseCSVNoHeader)
runTest("Parse TSV", testParseTSV)
runTest("Parse CSV With Newlines", testParseCSVWithNewlines)
runTest("Parse CSV With Empty Fields", testParseCSVWithEmptyFields)
runTest("Parse CSV With CRLF", testParseCSVWithCRLF)
runTest("Parse Semicolon CSV", testParseSemicolonCSV)

runTest("Write Simple CSV", testWriteSimpleCSV)
runTest("Write CSV With Quotes", testWriteCSVWithQuotes)
runTest("Write TSV", testWriteTSV)
runTest("Round Trip", testRoundTrip)

runTest("Builder Basic", testBuilderBasic)
runTest("Builder With Types", testBuilderWithTypes)
runTest("Builder With Stringify", testBuilderWithStringify)

runTest("Document Filter", testDocumentFilter)
runTest("Document Sort", testDocumentSort)
runTest("Document Column Access", testDocumentColumnAccess)
runTest("Document As Dictionaries", testDocumentAsDictionaries)

runTest("Statistics", testStatistics)
runTest("Unique Values", testUniqueValues)
runTest("Group By", testGroupBy)

runTest("Stream Parser", testStreamParser)

runTest("Convenience Functions", testConvenienceFunctions)
runTest("Error Handling", testErrors)
runTest("Real-World CSV", testRealWorldCSV)

print("\n" + String(repeating: "=", count: 60))
print("测试结果: ✅ \(testsPassed) 通过, ❌ \(testsFailed) 失败")
print(String(repeating: "=", count: 60))

if testsFailed == 0 {
    print("\n🎉 所有测试通过!")
}

// 辅助扩展用于 Double 比较精度
extension XCTAssertEqual where T == Double? {
    static func assertEquals(_ actual: Double?, _ expected: Double, accuracy: Double) -> Bool {
        guard let actual = actual else { return false }
        return abs(actual - expected) < accuracy
    }
}

extension CSVField: Equatable {
    public static func == (lhs: CSVField, rhs: CSVField) -> Bool {
        switch (lhs, rhs) {
        case (.string(let a), .string(let b)): return a == b
        case (.integer(let a), .integer(let b)): return a == b
        case (.double(let a), .double(let b)): return a == b
        case (.boolean(let a), .boolean(let b)): return a == b
        case (.null, .null): return true
        case (.empty, .empty): return true
        default: return false
        }
    }
}

// 辅助函数用于带精度的 Double 比较
func assertEquals(_ actual: Double?, _ expected: Double, accuracy: Double = 0.0001, _ message: String = "") -> Bool {
    guard let actual = actual else {
        print("❌ 断言失败: \(message.isEmpty ? "" : message + " - ")期望 \(expected)，实际 nil")
        return false
    }
    if abs(actual - expected) < accuracy {
        return true
    } else {
        print("❌ 断言失败: \(message.isEmpty ? "" : message + " - ")期望 \(expected) (±\(accuracy))，实际 \(actual)")
        return false
    }
}