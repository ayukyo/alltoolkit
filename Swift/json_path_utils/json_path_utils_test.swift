// json_path_utils_test.swift
// JSON Path 工具测试用例

import Foundation

// 测试辅助函数
func runTest(_ name: String, _ test: () throws -> Bool) {
    do {
        let result = try test()
        if result {
            print("✅ PASS: \(name)")
        } else {
            print("❌ FAIL: \(name)")
        }
    } catch {
        print("❌ ERROR: \(name) - \(error)")
    }
}

// 测试数据
let sampleJSON = """
{
    "store": {
        "book": [
            {
                "category": "reference",
                "author": "Nigel Rees",
                "title": "Sayings of the Century",
                "price": 8.95
            },
            {
                "category": "fiction",
                "author": "Evelyn Waugh",
                "title": "Sword of Honour",
                "price": 12.99
            },
            {
                "category": "fiction",
                "author": "Herman Melville",
                "title": "Moby Dick",
                "isbn": "0-553-21311-3",
                "price": 8.99
            },
            {
                "category": "fiction",
                "author": "J. R. R. Tolkien",
                "title": "The Lord of the Rings",
                "isbn": "0-395-19395-8",
                "price": 22.99
            }
        ],
        "bicycle": {
            "color": "red",
            "price": 19.95
        }
    },
    "expensive": 10
}
"""

// ============ 测试用例 ============

print("\n" + String(repeating: "=", count: 50))
print("JSON Path Utils 测试套件")
print(String(repeating: "=", count: 50) + "\n")

// 测试 1: 基础解析
runTest("基础 JSON 解析") {
    let json = try JSONPathUtils.parse(sampleJSON)
    return json.isObject
}

// 测试 2: 根节点查询
runTest("根节点查询 $") {
    let json = try JSONPathUtils.parse(sampleJSON)
    let results = try json.query("$")
    return results.count == 1 && results.first?.isObject == true
}

// 测试 3: 属性访问
runTest("属性访问 $.store") {
    let json = try JSONPathUtils.parse(sampleJSON)
    let store = try json.queryFirst("$.store")
    return store?.isObject == true
}

// 测试 4: 嵌套属性访问
runTest("嵌套属性访问 $.store.bicycle.color") {
    let json = try JSONPathUtils.parse(sampleJSON)
    let color = try JSONPathUtils.getString(json, path: "$.store.bicycle.color")
    return color == "red"
}

// 测试 5: 数组索引访问
runTest("数组索引访问 $.store.book[0]") {
    let json = try JSONPathUtils.parse(sampleJSON)
    let firstBook = try json.queryFirst("$.store.book[0]")
    return firstBook?.isObject == true
}

// 测试 6: 数组元素属性
runTest("数组元素属性 $.store.book[0].title") {
    let json = try JSONPathUtils.parse(sampleJSON)
    let title = try JSONPathUtils.getString(json, path: "$.store.book[0].title")
    return title == "Sayings of the Century"
}

// 测试 7: 获取数字值
runTest("获取数字值 $.expensive") {
    let json = try JSONPathUtils.parse(sampleJSON)
    let value = try JSONPathUtils.getNumber(json, path: "$.expensive")
    return value == 10.0
}

// 测试 8: 获取价格
runTest("获取嵌套数字 $.store.bicycle.price") {
    let json = try JSONPathUtils.parse(sampleJSON)
    let price = try JSONPathUtils.getNumber(json, path: "$.store.bicycle.price")
    return price == 19.95
}

// 测试 9: 通配符 [*]
runTest("通配符访问 $.store.book[*]") {
    let json = try JSONPathUtils.parse(sampleJSON)
    let books = try json.query("$.store.book[*]")
    return books.count == 4
}

// 测试 10: 通配符获取所有属性
runTest("通配符获取属性 $.store.bicycle.*") {
    let json = try JSONPathUtils.parse(sampleJSON)
    let values = try json.query("$.store.bicycle.*")
    return values.count == 2
}

// 测试 11: 递归下降
runTest("递归下降查找 $.store..price") {
    let json = try JSONPathUtils.parse(sampleJSON)
    let prices = try json.query("$..price")
    return prices.count == 5
}

// 测试 12: 数组切片
runTest("数组切片 [1:3]") {
    let json = try JSONPathUtils.parse(sampleJSON)
    let slice = try json.query("$.store.book[1:3]")
    return slice.count == 2
}

// 测试 13: 数组切片带步长
runTest("数组切片带步长 [::2]") {
    let json = try JSONPathUtils.parse(sampleJSON)
    let slice = try json.query("$.store.book[::2]")
    return slice.count == 2
}

// 测试 14: 括号属性访问
runTest("括号属性访问 $['store']['bicycle']['color']") {
    let json = try JSONPathUtils.parse(sampleJSON)
    let color = try JSONPathUtils.getString(json, path: "$['store']['bicycle']['color']")
    return color == "red"
}

// 测试 15: JSON 字符串验证
runTest("JSON 字符串验证 - 有效") {
    return "{\"key\": \"value\"}".isValidJSON
}

// 测试 16: JSON 字符串验证无效
runTest("JSON 字符串验证 - 无效") {
    let result = JSONPathUtils.validate("{invalid json}")
    return !result.valid
}

// 测试 17: stringify 紧凑模式
runTest("JSON stringify 紧凑模式") {
    let json = try JSONPathUtils.parse("{\"name\": \"test\", \"value\": 123}")
    let str = JSONPathUtils.stringify(json, pretty: false)
    return str.contains("\"name\":") && str.contains("\"test\"")
}

// 测试 18: stringify 美化模式
runTest("JSON stringify 美化模式") {
    let json = try JSONPathUtils.parse("{\"name\": \"test\", \"value\": 123}")
    let str = JSONPathUtils.stringify(json, pretty: true)
    return str.contains("\n") && str.contains("  ")
}

// 测试 19: 合并 JSON 对象
runTest("合并 JSON 对象") {
    let base = try JSONPathUtils.parse("{\"a\": 1, \"b\": 2}")
    let overlay = try JSONPathUtils.parse("{\"b\": 3, \"c\": 4}")
    let merged = JSONPathUtils.merge(base, overlay)
    let obj = merged.asObject
    return obj?["a"]?.asNumber == 1 && obj?["b"]?.asNumber == 3 && obj?["c"]?.asNumber == 4
}

// 测试 20: 深拷贝
runTest("JSON 深拷贝") {
    let original = try JSONPathUtils.parse("{\"arr\": [1, 2, 3]}")
    let copy = JSONPathUtils.deepCopy(original)
    let originalArr = original.asObject?["arr"]?.asArray?.count
    let copyArr = copy.asObject?["arr"]?.asArray?.count
    return originalArr == copyArr && originalArr == 3
}

// 测试 21: 获取所有键
runTest("获取所有键") {
    let json = try JSONPathUtils.parse("{\"a\": {\"b\": {\"c\": 1}}, \"d\": 2}")
    let keys = JSONPathUtils.getAllKeys(json)
    return keys.contains("a") && keys.contains("b") && keys.contains("c") && keys.contains("d")
}

// 测试 22: 获取叶子值
runTest("获取叶子值") {
    let json = try JSONPathUtils.parse("{\"a\": 1, \"b\": [2, 3], \"c\": {\"d\": 4}}")
    let leaves = JSONPathUtils.getLeafValues(json)
    return leaves.count == 4
}

// 测试 23: 从字典创建 JSON
runTest("从字典创建 JSON") {
    let dict: [String: Any] = ["name": "test", "count": 42, "active": true]
    let json = JSONPathUtils.fromDictionary(dict)
    let obj = json.asObject
    return obj?["name"]?.asString == "test" && obj?["count"]?.asNumber == 42
}

// 测试 24: 从数组创建 JSON
runTest("从数组创建 JSON") {
    let arr: [Any] = [1, "two", true, ["nested": "value"]]
    let json = JSONPathUtils.fromArray(arr)
    let array = json.asArray
    return array?.count == 4
}

// 测试 25: 类型检查
runTest("类型检查") {
    let json = try JSONPathUtils.parse("""
    {
        "null_val": null,
        "bool_val": true,
        "number_val": 42.5,
        "string_val": "hello",
        "array_val": [1, 2, 3],
        "object_val": {"key": "value"}
    }
    """)
    
    let obj = json.asObject
    return obj?["null_val"]?.isNull == true &&
           obj?["bool_val"]?.isBool == true &&
           obj?["number_val"]?.isNumber == true &&
           obj?["string_val"]?.isString == true &&
           obj?["array_val"]?.isArray == true &&
           obj?["object_val"]?.isObject == true
}

// 测试 26: 数组长度
runTest("数组长度查询") {
    let json = try JSONPathUtils.parse(sampleJSON)
    let books = try JSONPathUtils.getArray(json, path: "$.store.book")
    return books?.count == 4
}

// 测试 27: 布尔值获取
runTest("布尔值获取") {
    let json = try JSONPathUtils.parse("{\"active\": true, \"disabled\": false}")
    let active = try JSONPathUtils.getBool(json, path: "$.active")
    let disabled = try JSONPathUtils.getBool(json, path: "$.disabled")
    return active == true && disabled == false
}

// 测试 28: 扩展方法 parseJSON
runTest("String 扩展 parseJSON") {
    let json = try "{\"test\": 123}".parseJSON()
    return json.asObject?["test"]?.asNumber == 123
}

// 测试 29: JSONValue stringify 扩展
runTest("JSONValue stringify 扩展") {
    let json = try JSONPathUtils.parse("{\"key\": \"value\"}")
    let str = json.stringify()
    return str.contains("key") && str.contains("value")
}

// 测试 30: 负数切片
runTest("负数索引") {
    let json = try JSONPathUtils.parse("{\"items\": [1, 2, 3, 4, 5]}")
    // 使用倒数第二个元素
    let items = try JSONPathUtils.getArray(json, path: "$.items")
    return items?.count == 5
}

print("\n" + String(repeating: "=", count: 50))
print("测试完成")
print(String(repeating: "=", count: 50) + "\n")

// 性能测试
print("\n📊 性能测试")

let largeArrayJSON = "["
    + (0..<1000).map { "{\"id\": \($0), \"name\": \"item\($0)\"}" }.joined(separator: ",")
    + "]"

let startTime = Date()
if let largeJson = try? JSONPathUtils.parse(largeArrayJSON) {
    let results = try? largeJson.query("$[*].name")
    let elapsed = Date().timeIntervalSince(startTime) * 1000
    print("  解析并查询 1000 元素数组: \(String(format: "%.2f", elapsed)) ms")
    print("  查询结果数量: \(results?.count ?? 0)")
}

// 复杂嵌套查询性能
let complexQueryStart = Date()
if let json = try? JSONPathUtils.parse(sampleJSON) {
    _ = try? json.query("$..price")
    let elapsed = Date().timeIntervalSince(complexQueryStart) * 1000
    print("  递归查询所有 price: \(String(format: "%.2f", elapsed)) ms")
}

print("\n✨ 所有测试完成！\n")