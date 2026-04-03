package json_utils

/**
 * JSON Utilities Test Suite
 * Tests all JSON parsing and generation functionality
 */

fun main() {
    println("Running JSON Utils Tests...")
    println("=" * 50)

    var passed = 0
    var failed = 0

    // Test 1: Parse null
    try {
        val result = JsonUtils.parse("null")
        assert(result.isNull()) { "Expected null" }
        println("✓ Test 1: Parse null")
        passed++
    } catch (e: Exception) {
        println("✗ Test 1: Parse null - ${e.message}")
        failed++
    }

    // Test 2: Parse boolean true
    try {
        val result = JsonUtils.parse("true")
        assert(result.isBoolean() && result.asBoolean()) { "Expected true" }
        println("✓ Test 2: Parse boolean true")
        passed++
    } catch (e: Exception) {
        println("✗ Test 2: Parse boolean true - ${e.message}")
        failed++
    }

    // Test 3: Parse boolean false
    try {
        val result = JsonUtils.parse("false")
        assert(result.isBoolean() && !result.asBoolean()) { "Expected false" }
        println("✓ Test 3: Parse boolean false")
        passed++
    } catch (e: Exception) {
        println("✗ Test 3: Parse boolean false - ${e.message}")
        failed++
    }

    // Test 4: Parse integer
    try {
        val result = JsonUtils.parse("42")
        assert(result.isNumber() && result.asInt() == 42) { "Expected 42" }
        println("✓ Test 4: Parse integer")
        passed++
    } catch (e: Exception) {
        println("✗ Test 4: Parse integer - ${e.message}")
        failed++
    }

    // Test 5: Parse negative number
    try {
        val result = JsonUtils.parse("-123")
        assert(result.isNumber() && result.asInt() == -123) { "Expected -123" }
        println("✓ Test 5: Parse negative number")
        passed++
    } catch (e: Exception) {
        println("✗ Test 5: Parse negative number - ${e.message}")
        failed++
    }

    // Test 6: Parse float
    try {
        val result = JsonUtils.parse("3.14")
        assert(result.isNumber() && kotlin.math.abs(result.asDouble() - 3.14) < 0.001) { "Expected 3.14" }
        println("✓ Test 6: Parse float")
        passed++
    } catch (e: Exception) {
        println("✗ Test 6: Parse float - ${e.message}")
        failed++
    }

    // Test 7: Parse scientific notation
    try {
        val result = JsonUtils.parse("1.5e10")
        assert(result.isNumber() && result.asDouble() == 1.5e10) { "Expected 1.5e10" }
        println("✓ Test 7: Parse scientific notation")
        passed++
    } catch (e: Exception) {
        println("✗ Test 7: Parse scientific notation - ${e.message}")
        failed++
    }

    // Test 8: Parse simple string
    try {
        val result = JsonUtils.parse("\"hello\"")
        assert(result.isString() && result.asString() == "hello") { "Expected hello" }
        println("✓ Test 8: Parse simple string")
        passed++
    } catch (e: Exception) {
        println("✗ Test 8: Parse simple string - ${e.message}")
        failed++
    }

    // Test 9: Parse string with escape sequences
    try {
        val result = JsonUtils.parse("\"hello\\nworld\"")
        assert(result.isString() && result.asString() == "hello\nworld") { "Expected hello\\nworld" }
        println("✓ Test 9: Parse string with escape sequences")
        passed++
    } catch (e: Exception) {
        println("✗ Test 9: Parse string with escape sequences - ${e.message}")
        failed++
    }

    // Test 10: Parse empty array
    try {
        val result = JsonUtils.parse("[]")
        assert(result.isArray() && result.size() == 0) { "Expected empty array" }
        println("✓ Test 10: Parse empty array")
        passed++
    } catch (e: Exception) {
        println("✗ Test 10: Parse empty array - ${e.message}")
        failed++
    }

    // Test 11: Parse array with values
    try {
        val result = JsonUtils.parse("[1, 2, 3]")
        assert(result.isArray() && result.size() == 3) { "Expected array with 3 elements" }
        val arr = result.asArray()
        assert(arr.getInt(0) == 1 && arr.getInt(1) == 2 && arr.getInt(2) == 3)
        println("✓ Test 11: Parse array with values")
        passed++
    } catch (e: Exception) {
        println("✗ Test 11: Parse array with values - ${e.message}")
        failed++
    }

    // Test 12: Parse nested array
    try {
        val result = JsonUtils.parse("[[1, 2], [3, 4]]")
        assert(result.isArray() && result.size() == 2) { "Expected nested array" }
        val arr = result.asArray()
        assert(arr.getArray(0).size() == 2 && arr.getArray(1).size() == 2)
        println("✓ Test 12: Parse nested array")
        passed++
    } catch (e: Exception) {
        println("✗ Test 12: Parse nested array - ${e.message}")
        failed++
    }

    // Test 13: Parse empty object
    try {
        val result = JsonUtils.parse("{}")
        assert(result.isObject() && result.size() == 0) { "Expected empty object" }
        println("✓ Test 13: Parse empty object")
        passed++
    } catch (e: Exception) {
        println("✗ Test 13: Parse empty object - ${e.message}")
        failed++
    }

    // Test 14: Parse simple object
    try {
        val result = JsonUtils.parse("""{"name": "John", "age": 30}""")
        assert(result.isObject() && result.size() == 2) { "Expected object with 2 properties" }
        val obj = result.asObject()
        assert(obj.getString("name") == "John" && obj.getInt("age") == 30)
        println("✓ Test 14: Parse simple object")
        passed++
    } catch (e: Exception) {
        println("✗ Test 14: Parse simple object - ${e.message}")
        failed++
    }

    // Test 15: Parse nested object
    try {
        val result = JsonUtils.parse("""{"user": {"name": "John", "id": 1}}""")
        assert(result.isObject()) { "Expected object" }
        val obj = result.asObject()
        assert(obj.has("user"))
        val user = obj.getObject("user")
        assert(user.getString("name") == "John" && user.getInt("id") == 1)
        println("✓ Test 15: Parse nested object")
        passed++
    } catch (e: Exception) {
        println("✗ Test 15: Parse nested object - ${e.message}")
        failed++
    }

    // Test 16: Test object get with default
    try {
        val result = JsonUtils.parse("""{"name": "John"}""")
        val obj = result.asObject()
        assert(obj.getString("missing", "default") == "default")
        assert(obj.getInt("missing", 42) == 42)
        assert(obj.getBoolean("missing", true))
        println("✓ Test 16: Object get with default")
        passed++
    } catch (e: Exception) {
        println("✗ Test 16: Object get with default - ${e.message}")
        failed++
    }

    // Test 17: Test array get with default
    try {
        val result = JsonUtils.parse("[1, 2]")
        val arr = result.asArray()
        assert(arr.getInt(10, 99) == 99)
        assert(arr.getString(10, "default") == "default")
        println("✓ Test 17: Array get with default")
        passed++
    } catch (e: Exception) {
        println("✗ Test 17: Array get with default - ${e.message}")
        failed++
    }

    // Test 18: Generate JSON from object
    try {
        val obj = JsonUtils.obj(
            "name" to "John",
            "age" to 30,
            "active" to true
        )
        val json = obj.toJsonString()
        assert(json.contains("\"name\":\"John\""))
        assert(json.contains("\"age\":30"))
        assert(json.contains("\"active\":true"))
        println("✓ Test 18: Generate JSON from object")
        passed++
    } catch (e: Exception) {
        println("✗ Test 18: Generate JSON from object - ${e.message}")
        failed++
    }

    // Test 19: Generate JSON from array
    try {
        val arr = JsonUtils.arr(1, 2, 3, "hello")
        val json = arr.toJsonString()
        assert(json == "[1,2,3,\"hello\"]")
        println("✓ Test 19: Generate JSON from array")
        passed++
    } catch (e: Exception) {
        println("✗ Test 19: Generate JSON from array - ${e.message}")
        failed++
    }

    // Test 20: Pretty print JSON
    try {
        val json = """{"name":"John","age":30}"""
        val pretty = JsonUtils.prettyPrint(json)
        assert(pretty.contains("{\n"))
        assert(pretty.contains("  \"name\":"))
        println("✓ Test 20: Pretty print JSON")
        passed++
    } catch (e: Exception) {
        println("✗ Test 20: Pretty print JSON - ${e.message}")
        failed++
    }

    // Test 21: Minify JSON
    try {
        val json = """{
            "name": "John",
            "age": 30
        }"""
        val minified = JsonUtils.minify(json)
        assert(!minified.contains("\n"))
        assert(!minified.contains("  "))
        println("✓ Test 21: Minify JSON")
        passed++
    } catch (e: Exception) {
        println("✗ Test 21: Minify JSON - ${e.message}")
        failed++
    }

    // Test 22: Merge objects
    try {
        val obj1 = JsonUtils.obj("a" to 1, "b" to 2)
        val obj2 = JsonUtils.obj("b" to 3, "c" to 4)
        val merged = JsonUtils.merge(obj1, obj2)
        assert(merged.getInt("a") == 1)
        assert(merged.getInt("b") == 3) // obj2 overrides
        assert(merged.getInt("c") == 4)
        println("✓ Test 22: Merge objects")
        passed++
    } catch (e: Exception) {
        println("✗ Test 22: Merge objects - ${e.message}")
        failed++
    }

    // Test 23: Validate JSON
    try {
        assert(JsonUtils.isValid("{}"))
        assert(JsonUtils.isValid("[]"))
        assert(JsonUtils.isValid("\"hello\""))
        assert(JsonUtils.isValid("123"))
        assert(JsonUtils.isValid("true"))
        assert(!JsonUtils.isValid("{invalid}"))
        assert(!JsonUtils.isValid(""))
        println("✓ Test 23: Validate JSON")
        passed++
    } catch (e: Exception) {
        println("✗ Test 23: Validate JSON - ${e.message}")
        failed++
    }

    // Test 24: Parse or null
    try {
        assert(JsonUtils.parseOrNull("{}") != null)
        assert(JsonUtils.parseOrNull("invalid") == null)
        println("✓ Test 24: Parse or null")
        passed++
    } catch (e: Exception) {
        println("✗ Test 24: Parse or null - ${e.message}")
        failed++
    }

    // Test 25: Complex nested structure
    try {
        val json = """{
            "users": [
                {"id": 1, "name": "Alice", "roles": ["admin", "user"]},
                {"id": 2, "name": "Bob", "roles": ["user"]}
            ],
            "meta": {
                "total": 2,
                "page": 1
            }
        }"""
        val result = JsonUtils.parse(json)
        assert(result.isObject())
        val users = result.asObject().getArray("users")
        assert(users.size() == 2)
        assert(users.getObject(0).getString("name") == "Alice")
        assert(users.getObject(0).getArray("roles").size() == 2)
        assert(users.getObject(1).getString("name") == "Bob")
        assert(result.asObject().getObject("meta").getInt("total") == 2)
        println("✓ Test 25: Complex nested structure")
        passed++
    } catch (e: Exception) {
        println("✗ Test 25: Complex nested structure - ${e.message}")
        failed++
    }

    // Test 26: Unicode escape sequences
    try {
        val result = JsonUtils.parse("\"\\u0048\\u0065\\u006c\\u006c\\u006f\"")
        assert(result.asString() == "Hello")
        println("✓ Test 26: Unicode escape sequences")
        passed++
    } catch (e: Exception) {
        println("✗ Test 26: Unicode escape sequences - ${e.message}")
        failed++
    }

    // Test 27: Special characters in strings
    try {
        val result = JsonUtils.parse("\"hello\\tworld\\nnew line\"")
        assert(result.asString() == "hello\tworld\nnew line")
        println("✓ Test 27: Special characters in strings")
        passed++
    } catch (e: Exception) {
        println("✗ Test 27: Special characters in strings - ${e.message}")
        failed++
    }

    // Test 28: Null values in object
    try {
        val result = JsonUtils.parse("""{"name": null, "value": 42}""")
        assert(result.asObject().get("name").isNull())
        assert(result.asObject().getInt("value") == 42)
        println("✓ Test 28: Null values in object")
        passed++
    } catch (e: Exception) {
        println("✗ Test 28: Null values in object - ${e.message}")
        failed++
    }

    // Test 29: Mixed types in array
    try {
        val result = JsonUtils.parse("[1, \"two\", true, null, {\"a\": 1}]")
        val arr = result.asArray()
        assert(arr.getInt(0) == 1)
        assert(arr.getString(1) == "two")
        assert(arr.getBoolean(2))
        assert(arr[3].isNull())
        assert(arr.getObject(4).getInt("a") == 1)
        println("✓ Test 29: Mixed types in array")
        passed++
    } catch (e: Exception) {
        println("✗ Test 29: Mixed types in array - ${e.message}")
        failed++
    }

    // Test 30: Round-trip parsing
    try {
        val original = """{"name":"John","items":[1,2,3],"active":true}"""
        val parsed = JsonUtils.parse(original)
        val generated = parsed.toJsonString()
        val reparsed = JsonUtils.parse(generated)
        assert(reparsed.asObject().getString("name") == "John")
        assert(reparsed.asObject().getArray("items").size() == 3)
        assert(reparsed.asObject().getBoolean("active"))
        println("✓ Test 30: Round-trip parsing")
        passed++
    } catch (e: Exception) {
        println("✗ Test 30: Round-trip parsing - ${e.message}")
        failed++
    }

    println("=" * 50)
    println("Results: $passed passed, $failed failed")
    if (failed == 0) {
        println("All tests passed! ✓")
    } else {
        println("Some tests failed! ✗")
        kotlin.system.exitProcess(1)
    }
}
