// usage_examples.swift
// JSON Path Utils 使用示例

import Foundation

// ============ 示例数据 ============

let apiResponse = """
{
    "status": "success",
    "data": {
        "users": [
            {
                "id": 1,
                "name": "张三",
                "email": "zhangsan@example.com",
                "age": 28,
                "active": true,
                "roles": ["admin", "editor"],
                "profile": {
                    "avatar": "https://example.com/avatar1.jpg",
                    "bio": "全栈开发者",
                    "skills": ["Swift", "Python", "JavaScript"]
                }
            },
            {
                "id": 2,
                "name": "李四",
                "email": "lisi@example.com",
                "age": 32,
                "active": true,
                "roles": ["viewer"],
                "profile": {
                    "avatar": "https://example.com/avatar2.jpg",
                    "bio": "产品经理",
                    "skills": ["产品设计", "数据分析"]
                }
            },
            {
                "id": 3,
                "name": "王五",
                "email": "wangwu@example.com",
                "age": 25,
                "active": false,
                "roles": ["editor"],
                "profile": {
                    "avatar": "https://example.com/avatar3.jpg",
                    "bio": "前端工程师",
                    "skills": ["Vue", "React", "TypeScript"]
                }
            }
        ],
        "pagination": {
            "page": 1,
            "perPage": 10,
            "total": 3,
            "totalPages": 1
        }
    },
    "meta": {
        "version": "1.0",
        "timestamp": "2026-05-02T17:00:00Z"
    }
}
"""

let productCatalog = """
{
    "products": [
        {
            "id": "P001",
            "name": "无线蓝牙耳机",
            "category": "电子产品",
            "price": 299.99,
            "stock": 150,
            "attributes": {
                "color": "黑色",
                "weight": "50g",
                "battery": "20小时"
            },
            "reviews": [
                {"user": "user1", "rating": 5, "comment": "非常好用"},
                {"user": "user2", "rating": 4, "comment": "性价比高"}
            ]
        },
        {
            "id": "P002",
            "name": "智能手表",
            "category": "电子产品",
            "price": 899.99,
            "stock": 80,
            "attributes": {
                "color": "银色",
                "weight": "35g",
                "battery": "7天"
            },
            "reviews": [
                {"user": "user3", "rating": 5, "comment": "功能齐全"}
            ]
        },
        {
            "id": "P003",
            "name": "机械键盘",
            "category": "电脑配件",
            "price": 459.99,
            "stock": 200,
            "attributes": {
                "color": "白色",
                "weight": "800g",
                "switch": "红轴"
            },
            "reviews": [
                {"user": "user4", "rating": 4, "comment": "手感很好"}
            ]
        }
    ]
}
"""

print("""
╔════════════════════════════════════════════════════════════╗
║          JSON Path Utils 使用示例                           ║
╚════════════════════════════════════════════════════════════╝
""")

// ============ 示例 1: 基础解析与查询 ============

print("\n📖 示例 1: 基础解析与查询")
print(String(repeating: "-", count: 50))

do {
    // 解析 JSON
    let json = try JSONPathUtils.parse(apiResponse)
    
    // 获取状态
    let status = try JSONPathUtils.getString(json, path: "$.status")
    print("  API 状态: \(status ?? "未知")")
    
    // 获取用户列表
    let users = try JSONPathUtils.getArray(json, path: "$.data.users")
    print("  用户数量: \(users?.count ?? 0)")
    
    // 获取第一个用户的名字
    let firstName = try JSONPathUtils.getString(json, path: "$.data.users[0].name")
    print("  第一个用户: \(firstName ?? "未知")")
    
} catch {
    print("  错误: \(error)")
}

// ============ 示例 2: 数组操作 ============

print("\n📖 示例 2: 数组操作")
print(String(repeating: "-", count: 50))

do {
    let json = try JSONPathUtils.parse(apiResponse)
    
    // 获取所有用户名
    let names = try json.query("$..name")
    print("  所有用户名:")
    for name in names {
        if let n = name.asString {
            print("    - \(n)")
        }
    }
    
    // 获取所有邮箱
    let emails = try json.query("$..email")
    print("  所有邮箱:")
    for email in emails {
        if let e = email.asString {
            print("    - \(e)")
        }
    }
    
} catch {
    print("  错误: \(error)")
}

// ============ 示例 3: 嵌套对象访问 ============

print("\n📖 示例 3: 嵌套对象访问")
print(String(repeating: "-", count: 50))

do {
    let json = try JSONPathUtils.parse(apiResponse)
    
    // 访问深层嵌套
    let avatar = try JSONPathUtils.getString(json, path: "$.data.users[0].profile.avatar")
    print("  用户头像: \(avatar ?? "无")")
    
    let bio = try JSONPathUtils.getString(json, path: "$.data.users[1].profile.bio")
    print("  用户简介: \(bio ?? "无")")
    
    // 获取技能列表
    let skills = try JSONPathUtils.getArray(json, path: "$.data.users[0].profile.skills")
    print("  技能列表:")
    for skill in skills ?? [] {
        if let s = skill.asString {
            print("    • \(s)")
        }
    }
    
} catch {
    print("  错误: \(error)")
}

// ============ 示例 4: 递归查询 ============

print("\n📖 示例 4: 递归查询")
print(String(repeating: "-", count: 50))

do {
    let json = try JSONPathUtils.parse(productCatalog)
    
    // 查找所有价格
    let prices = try json.query("$..price")
    print("  所有产品价格:")
    for price in prices {
        if let p = price.asNumber {
            print("    - ¥\(String(format: "%.2f", p))")
        }
    }
    
    // 查找所有评分
    let ratings = try json.query("$..rating")
    print("  所有评分:")
    for rating in ratings {
        if let r = rating.asNumber {
            print("    - ⭐\(Int(r))")
        }
    }
    
    // 查找所有产品 ID
    let productIds = try json.query("$..id")
    print("  所有 ID (产品+评论用户):")
    for id in productIds {
        if let i = id.asString {
            print("    - \(i)")
        } else if let i = id.asNumber {
            print("    - \(Int(i))")
        }
    }
    
} catch {
    print("  错误: \(error)")
}

// ============ 示例 5: 数组切片 ============

print("\n📖 示例 5: 数组切片")
print(String(repeating: "-", count: 50))

do {
    let json = try JSONPathUtils.parse(productCatalog)
    
    // 获取前两个产品
    let firstTwo = try json.query("$.products[0:2]")
    print("  前两个产品:")
    for product in firstTwo {
        if let name = product.asObject?["name"]?.asString {
            print("    - \(name)")
        }
    }
    
    // 获取每第二个元素
    let everySecond = try json.query("$.products[::2]")
    print("  每隔一个产品:")
    for product in everySecond {
        if let name = product.asObject?["name"]?.asString {
            print("    - \(name)")
        }
    }
    
} catch {
    print("  错误: \(error)")
}

// ============ 示例 6: JSON 构建 ============

print("\n📖 示例 6: JSON 构建")
print(String(repeating: "-", count: 50))

do {
    // 从字典构建
    let userDict: [String: Any] = [
        "name": "赵六",
        "age": 30,
        "active": true,
        "tags": ["swift", "ios", "developer"]
    ]
    let userJson = JSONPathUtils.fromDictionary(userDict)
    
    // 紧凑输出
    print("  紧凑 JSON:")
    print("  \(userJson.stringify())")
    
    // 美化输出
    print("\n  美化 JSON:")
    print(userJson.stringify(pretty: true).split(separator: "\n").map { "  \($0)" }.joined(separator: "\n"))
    
} catch {
    print("  错误: \(error)")
}

// ============ 示例 7: JSON 合并 ============

print("\n📖 示例 7: JSON 合并")
print(String(repeating: "-", count: 50))

do {
    let baseJson = try JSONPathUtils.parse("""
    {
        "name": "产品",
        "version": "1.0",
        "features": ["A", "B"]
    }
    """)
    
    let overlayJson = try JSONPathUtils.parse("""
    {
        "version": "2.0",
        "author": "开发者",
        "features": ["C", "D"]
    }
    """)
    
    let merged = JSONPathUtils.merge(baseJson, overlayJson)
    
    print("  合并结果:")
    print(merged.stringify(pretty: true).split(separator: "\n").map { "  \($0)" }.joined(separator: "\n"))
    
} catch {
    print("  错误: \(error)")
}

// ============ 示例 8: 键和叶子值提取 ============

print("\n📖 示例 8: 键和叶子值提取")
print(String(repeating: "-", count: 50))

do {
    let json = try JSONPathUtils.parse("""
    {
        "user": {
            "name": "测试",
            "settings": {
                "theme": "dark",
                "language": "zh-CN"
            }
        },
        "app": "demo"
    }
    """)
    
    // 获取所有键
    let keys = JSONPathUtils.getAllKeys(json)
    print("  所有键: \(keys)")
    
    // 获取所有叶子值
    let leaves = JSONPathUtils.getLeafValues(json)
    print("  所有叶子值:")
    for leaf in leaves {
        print("    - \(leaf)")
    }
    
} catch {
    print("  错误: \(error)")
}

// ============ 示例 9: 类型检查 ============

print("\n📖 示例 9: 类型检查")
print(String(repeating: "-", count: 50))

do {
    let json = try JSONPathUtils.parse("""
    {
        "text": "hello",
        "number": 42,
        "float": 3.14,
        "bool": true,
        "null": null,
        "array": [1, 2, 3],
        "object": {"key": "value"}
    }
    """)
    
    let obj = json.asObject
    
    print("  类型检查结果:")
    if let text = obj?["text"] {
        print("    text isString: \(text.isString), value: \(text.asString ?? "")")
    }
    if let number = obj?["number"] {
        print("    number isNumber: \(number.isNumber), value: \(number.asNumber ?? 0)")
    }
    if let bool = obj?["bool"] {
        print("    bool isBool: \(bool.isBool), value: \(bool.asBool ?? false)")
    }
    if let null = obj?["null"] {
        print("    null isNull: \(null.isNull)")
    }
    if let array = obj?["array"] {
        print("    array isArray: \(array.isArray), count: \(array.asArray?.count ?? 0)")
    }
    if let object = obj?["object"] {
        print("    object isObject: \(object.isObject), keys: \(object.asObject?.keys ?? [])")
    }
    
} catch {
    print("  错误: \(error)")
}

// ============ 示例 10: 验证与深拷贝 ============

print("\n📖 示例 10: 验证与深拷贝")
print(String(repeating: "-", count: 50))

// 验证 JSON
let validJson = "{\"name\": \"test\", \"value\": 123}"
let invalidJson = "{name: test, value: 123}"

print("  验证有效 JSON: \(validJson.isValidJSON)")
print("  验证无效 JSON: \(invalidJson.isValidJSON)")

// 详细验证结果
let (isValid, error) = JSONPathUtils.validate(invalidJson)
print("  详细验证: valid=\(isValid), error=\(error ?? "无")")

// 深拷贝
do {
    let original = try JSONPathUtils.parse("{\"items\": [1, 2, {\"nested\": true}]}")
    let copy = JSONPathUtils.deepCopy(original)
    
    print("  原始 JSON: \(original.stringify())")
    print("  深拷贝 JSON: \(copy.stringify())")
    print("  是不同的实例: \(original !== copy)")
    
} catch {
    print("  错误: \(error)")
}

print("\n" + String(repeating: "=", count: 60))
print("✨ 示例演示完成!")
print(String(repeating: "=", count: 60) + "\n")