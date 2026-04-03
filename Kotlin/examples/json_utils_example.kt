import json_utils.*

/**
 * JSON Utilities Example
 * Demonstrates usage of the JSON parsing and generation library
 */
fun main() {
    println("JSON Utilities Examples")
    println("=" * 50)

    // Example 1: Parse simple JSON values
    println("\n1. Parse simple JSON values:")
    val nullValue = JsonUtils.parse("null")
    println("   null -> ${nullValue}")

    val boolValue = JsonUtils.parse("true")
    println("   true -> ${boolValue.asBoolean()}")

    val numValue = JsonUtils.parse("42")
    println("   42 -> ${numValue.asInt()}")

    val strValue = JsonUtils.parse("\"Hello, World!\"")
    println("   \"Hello, World!\" -> ${strValue.asString()}")

    // Example 2: Parse JSON objects
    println("\n2. Parse JSON objects:")
    val userJson = """{"name": "John Doe", "age": 30, "active": true}"""
    val user = JsonUtils.parse(userJson).asObject()
    println("   JSON: $userJson")
    println("   Name: ${user.getString("name")}")
    println("   Age: ${user.getInt("age")}")
    println("   Active: ${user.getBoolean("active")}")

    // Example 3: Parse JSON arrays
    println("\n3. Parse JSON arrays:")
    val arrJson = "[1, 2, 3, 4, 5]"
    val arr = JsonUtils.parse(arrJson).asArray()
    println("   JSON: $arrJson")
    println("   First element: ${arr.getInt(0)}")
    println("   Array size: ${arr.size()}")

    // Example 4: Parse nested structures
    println("\n4. Parse nested structures:")
    val complexJson = """{
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ],
        "count": 2
    }"""
    val complex = JsonUtils.parse(complexJson).asObject()
    val users = complex.getArray("users")
    println("   Number of users: ${complex.getInt("count")}")
    println("   First user: ${users.getObject(0).getString("name")}")
    println("   Second user: ${users.getObject(1).getString("name")}")

    // Example 5: Create JSON programmatically
    println("\n5. Create JSON programmatically:")
    val newObj = JsonUtils.obj(
        "product" to "Laptop",
        "price" to 999.99,
        "inStock" to true,
        "tags" to JsonUtils.arr("electronics", "computers", "sale")
    )
    println("   Generated JSON: ${newObj.toJsonString()}")

    // Example 6: Pretty print JSON
    println("\n6. Pretty print JSON:")
    val uglyJson = """{"name":"John","items":[{"id":1},{"id":2}],"active":true}"""
    println("   Input: $uglyJson")
    println("   Pretty:")
    println(JsonUtils.prettyPrint(uglyJson))

    // Example 7: Minify JSON
    println("\n7. Minify JSON:")
    val prettyJson = """{
        "name": "John",
        "age": 30
    }"""
    println("   Input (multiline):")
    println(prettyJson)
    println("   Minified: ${JsonUtils.minify(prettyJson)}")

    // Example 8: Validate JSON
    println("\n8. Validate JSON:")
    val validJson = """{"name": "John", "age": 30}"""
    val invalidJson = """{"name": "John", "age": }"""
    println("   Valid JSON: ${JsonUtils.isValid(validJson)}")
    println("   Invalid JSON: ${JsonUtils.isValid(invalidJson)}")

    // Example 9: Safe parsing
    println("\n9. Safe parsing:")
    val result1 = JsonUtils.parseOrNull("{}").let { if (it != null) "Parsed successfully" else "Parse failed" }
    val result2 = JsonUtils.parseOrNull("invalid").let { if (it != null) "Parsed successfully" else "Parse failed" }
    println("   Valid JSON: $result1")
    println("   Invalid JSON: $result2")

    // Example 10: Working with defaults
    println("\n10. Working with defaults:")
    val partialObj = JsonUtils.parse("""{"name": "John"}""").asObject()
    println("   Existing key: ${partialObj.getString("name")}")
    println("   Missing key (with default): ${partialObj.getString("missing", "default value")}")
    println("   Missing key (int default): ${partialObj.getInt("missing", 0)}")

    // Example 11: Merge objects
    println("\n11. Merge objects:")
    val obj1 = JsonUtils.obj("a" to 1, "b" to 2)
    val obj2 = JsonUtils.obj("b" to 3, "c" to 4)
    val merged = JsonUtils.merge(obj1, obj2)
    println("   Object 1: ${obj1.toJsonString()}")
    println("   Object 2: ${obj2.toJsonString()}")
    println("   Merged: ${merged.toJsonString()}")

    // Example 12: Convert from Kotlin collections
    println("\n12. Convert from Kotlin collections:")
    val map = mapOf("name" to "Alice", "age" to 25, "city" to "NYC")
    val list = listOf(1, 2, 3, "hello", true)
    println("   Map -> JSON: ${JsonUtils.toJson(map)}")
    println("   List -> JSON: ${JsonUtils.toJson(list)}")

    // Example 13: Check types
    println("\n13. Check types:")
    val mixedArray = JsonUtils.parse("[1, \"two\", true, null, {}]").asArray()
    println("   Element 0 is number: ${mixedArray[0].isNumber()}")
    println("   Element 1 is string: ${mixedArray[1].isString()}")
    println("   Element 2 is boolean: ${mixedArray[2].isBoolean()}")
    println("   Element 3 is null: ${mixedArray[3].isNull()}")
    println("   Element 4 is object: ${mixedArray[4].isObject()}")

    // Example 14: Working with entries
    println("\n14. Iterate over object entries:")
    val person = JsonUtils.parse("""{"name": "John", "age": 30, "city": "NYC"}""").asObject()
    println("   Object entries:")
    for ((key, value) in person.entries()) {
        println("     $key = ${value.asString()}")
    }

    // Example 15: Complex nested access
    println("\n15. Complex nested access:")
    val dataJson = """{
        "company": {
            "name": "TechCorp",
            "employees": [
                {"name": "Alice", "department": "Engineering"},
                {"name": "Bob", "department": "Sales"}
            ]
        }
    }"""
    val data = JsonUtils.parse(dataJson).asObject()
    val company = data.getObject("company")
    val employees = company.getArray("employees")
    println("   Company: ${company.getString("name")}")
    println("   First employee: ${employees.getObject(0).getString("name")} (${employees.getObject(0).getString("department")})")
    println("   Second employee: ${employees.getObject(1).getString("name")} (${employees.getObject(1).getString("department")})")

    println("\n" + "=" * 50)
    println("Examples completed!")
}
