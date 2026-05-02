/**
 * AllToolkit - Swift CSV Utilities Examples
 *
 * 演示 CSV 工具库的各种用法
 */

import Foundation

// 注意：实际使用时需要将 mod.swift 文件添加到项目中
// 这里演示独立运行的方法

// 从文件读取示例代码并展示
print("""
╔══════════════════════════════════════════════════════════════╗
║           AllToolkit Swift CSV Utilities - 示例代码           ║
╚══════════════════════════════════════════════════════════════╝

本模块提供了完整的 CSV 解析和生成功能，零外部依赖。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 基本解析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// 解析简单 CSV
let csvString = \"\"\"
name,age,city
Alice,30,Beijing
Bob,25,Shanghai
Charlie,35,Guangzhou
\"\"\"

let parser = CSVParser()
let document = try parser.parse(csvString)

print("行数: \\(document.rowCount)")        // 3
print("列数: \\(document.columnCount)")    // 3
print("标题: \\(document.header ?? [])")   // ["name", "age", "city"]

// 访问数据
print(document[0, "name"]?.stringValue)    // "Alice"
print(document[0, "age"]?.intValue)        // 30
print(document[1, "city"]?.stringValue)    // "Shanghai"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. CSV 写入/生成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// 创建 CSV 文档
var doc = CSVDocument(header: ["id", "product", "price", "quantity"])
doc.addRow(strings: ["1", "Apple", "3.50", "100"])
doc.addRow(strings: ["2", "Banana", "2.80", "150"])
doc.addRow(strings: ["3", "Orange", "4.20", "80"])

// 转换为字符串
let writer = CSVWriter()
let csvOutput = writer.stringify(doc)
print(csvOutput)

// 写入文件
try writer.write(doc, to: "/path/to/output.csv")

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. 使用 Builder 模式
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// 流式构建 CSV
let csv = CSVBuilder(header: ["name", "email", "role"])
    .row("Alice", "alice@example.com", "Admin")
    .row("Bob", "bob@example.com", "User")
    .row("Charlie", "charlie@example.com", "Editor")
    .buildString()

print(csv)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. 类型推断
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// CSVField 自动推断类型
let field1 = CSVField.infer(from: "123")       // .integer(123)
let field2 = CSVField.infer(from: "3.14")      // .double(3.14)
let field3 = CSVField.infer(from: "true")      // .boolean(true)
let field4 = CSVField.infer(from: "null")      // .null
let field5 = CSVField.infer(from: "hello")     // .string("hello")

// 访问不同类型的值
print(field1.intValue)    // 123
print(field2.doubleValue) // 3.14
print(field3.boolValue)   // true

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. 引号和特殊字符处理
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// 包含逗号、引号、换行的 CSV
let complexCSV = \"\"\"
name,description
"Smith, John","Loves ""quotes"""
"Alice","Line1
Line2"
\"\"\"

let doc = try parser.parse(complexCSV)
print(doc[0, "name"]?.stringValue)         // "Smith, John"
print(doc[0, "description"]?.stringValue) // "Loves \"quotes\""
print(doc[1, "description"]?.stringValue) // "Line1\nLine2"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. 不同分隔符 (TSV, 分号等)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// TSV (制表符分隔)
let tsvParser = CSVParser(configuration: .tsv)
let tsvDoc = try tsvParser.parse("name\\tage\\nAlice\\t30")

// 分号分隔 (欧洲常用)
let semiParser = CSVParser(configuration: .semicolon)
let semiDoc = try semiParser.parse("name;age\\nAlice;30")

// 自定义配置
let customConfig = CSVConfiguration(
    delimiter: "|",
    quoteCharacter: "'",
    hasHeader: true,
    trimWhitespace: true
)
let customParser = CSVParser(configuration: customConfig)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. 数据操作
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// 过滤
let youngUsers = document.filter { row in
    guard let age = row["age"]?.intValue else { return false }
    return age < 30
}

// 排序
let sortedDoc = document.sorted(by: "age", ascending: false)

// 获取列数据
let names = document.column(named: "name")
let ages = document.column(named: "age")

// 转换为字典数组
let dicts = document.asDictionaries
// [["name": "Alice", "age": "30", ...], ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. 统计功能
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// 数值列统计
if let stats = document.statistics(forColumn: "age") {
    print("数量: \\(stats.count)")
    print("总和: \\(stats.sum)")
    print("平均: \\(stats.mean)")
    print("中位数: \\(stats.median)")
    print("最小: \\(stats.min)")
    print("最大: \\(stats.max)")
    print("方差: \\(stats.variance)")
    print("标准差: \\(stats.standardDeviation)")
    print("范围: \\(stats.range)")
}

// 唯一值
let uniqueCities = document.uniqueValues(forColumn: "city")

// 分组
let groups = document.groupBy(column: "city")
for (city, rows) in groups {
    print("\\(city): \\(rows.count) 人")
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. 流式解析 (大文件)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// 对于大文件，使用流式解析器
let streamParser = CSVStreamParser()

// 分块处理
let chunk1 = "name,age\\nAli"
let chunk2 = "ce,30\\nBob"
let chunk3 = ",25\\n"

let rows1 = try streamParser.parse(chunk: chunk1)
let rows2 = try streamParser.parse(chunk: chunk2)
let rows3 = try streamParser.parse(chunk: chunk3)
let finalRows = try streamParser.finish()

// 适合读取大文件
let fileHandle = FileHandle(forReadingAtPath: "/path/to/large.csv")
while let data = fileHandle?.readData(ofLength: 4096),
      !data.isEmpty {
    let chunk = String(data: data, encoding: .utf8) ?? ""
    let rows = try streamParser.parse(chunk: chunk)
    // 处理每批行
    for row in rows {
        processRow(row)
    }
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10. 便捷函数
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// 快速解析
let doc = try parseCSV("a,b\\n1,2", hasHeader: true)

// 从文件解析
let fileDoc = try parseCSVFile(at: "/path/to/file.csv")

// 快速创建
let newDoc = createCSV(header: ["x", "y"], rows: [["1", "2"], ["3", "4"]])

// 快速转换
let csvStr = stringifyCSV(newDoc)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
11. 完整示例：处理真实数据
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

""")

print("""
// 真实示例：员工数据
let employeeData = \"\"\"
id,name,email,department,salary,hire_date,active
1,Alice Smith,alice@company.com,Engineering,85000.00,2020-01-15,true
2,Bob Johnson,bob@company.com,Marketing,65000.00,2019-06-20,true
3,Charlie Brown,charlie@company.com,Engineering,92000.00,2018-03-10,true
4,Diana Williams,diana@company.com,Sales,78000.00,2021-02-28,false
5,Eve Davis,eve@company.com,Engineering,105000.00,2017-08-05,true
\"\"\"

let empParser = CSVParser()
let empDoc = try empParser.parse(employeeData)

// 1. 统计薪资
if let salaryStats = empDoc.statistics(forColumn: "salary") {
    print("📊 薪资统计:")
    print("   平均薪资: \\(String(format: "%.2f", salaryStats.mean))")
    print("   最高薪资: \\(String(format: "%.2f", salaryStats.max))")
    print("   最低薪资: \\(String(format: "%.2f", salaryStats.min))")
    print("   薪资范围: \\(String(format: "%.2f", salaryStats.range))")
}

// 2. 按部门分组
let byDept = empDoc.groupBy(column: "department")
print("\\n📁 部门人数:")
for (dept, rows) in byDept.sorted(by: { $0.key < $1.key }) {
    print("   \\(dept): \\(rows.count) 人")
}

// 3. 筛选活跃员工
let activeEmps = empDoc.filter { $0["active"]?.boolValue == true }
print("\\n✅ 活跃员工: \\(activeEmps.rowCount) 人")

// 4. 按薪资排序
let topEarners = empDoc.sorted(by: "salary", ascending: false)
print("\\n💰 薪资排名:")
for i in 0..<min(3, topEarners.rowCount) {
    if let name = topEarners[i, "name"]?.stringValue,
       let salary = topEarners[i, "salary"]?.doubleValue {
        print("   \\(i+1). \\(name): \\(String(format: "%.2f", salary))")
    }
}

// 5. 导出为 JSON 格式
let jsonDicts = empDoc.asDictionaries.map { row -> [String: Any] in
    var dict: [String: Any] = [:]
    for (key, field) in row {
        if let intVal = field.intValue {
            dict[key] = intVal
        } else if let doubleVal = field.doubleValue {
            dict[key] = doubleVal
        } else if let boolVal = field.boolValue {
            dict[key] = boolVal
        } else if field.isNull {
            dict[key] = NSNull()
        } else {
            dict[key] = field.stringValue
        }
    }
    return dict
}

if let jsonData = try? JSONSerialization.data(withJSONObject: jsonDicts, options: .prettyPrinted),
   let jsonString = String(data: jsonData, encoding: .utf8) {
    print("\\n📄 JSON 输出 (前 500 字符):")
    print(String(jsonString.prefix(500)))
}

""")

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
支持的特性
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 标准 RFC 4180 CSV 格式
✅ 自定义分隔符 (逗号, 制表符, 分号, 管道符等)
✅ 引号字段处理 (包含逗号、引号、换行)
✅ 多种换行符 (LF, CRLF, CR)
✅ 类型推断 (整数、浮点、布尔、空值)
✅ 流式解析 (大文件支持)
✅ Builder 模式 (流式 API)
✅ 数据操作 (过滤、排序、分组)
✅ 统计计算 (均值、中位数、方差等)
✅ 零外部依赖
✅ 完整的测试覆盖

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 详细文档请参考 mod.swift 源代码
🧪 测试代码见 csv_utils_test.swift
💡 示例代码见 examples/ 目录

""")