' =============================================================================
' JSON Utilities Test Suite for VB.NET
' =============================================================================
' Comprehensive test suite for the JSON Utilities module.
' Run with: vbc json_utils_test.vb mod.vb /out:json_test.exe && json_test.exe
' =============================================================================

Imports System
Imports System.Collections.Generic
Imports System.IO
Imports AllToolkit

Module JsonUtilsTest

    Private _passed As Integer = 0
    Private _failed As Integer = 0

    Sub Main()
        Console.WriteLine("========================================")
        Console.WriteLine("JSON Utilities Test Suite")
        Console.WriteLine("========================================")
        Console.WriteLine()

        TestParsing()
        TestSerialization()
        TestTypeChecking()
        TestTypeConversion()
        TestObjectAccess()
        TestArrayAccess()
        TestPrettyPrint()
        TestFileOperations()
        TestEdgeCases()
        TestComplexStructures()

        Console.WriteLine()
        Console.WriteLine("========================================")
        Console.WriteLine($"Tests Passed: {_passed}")
        Console.WriteLine($"Tests Failed: {_failed}")
        Console.WriteLine($"Total Tests: {_passed + _failed}")
        Console.WriteLine("========================================")

        If _failed > 0 Then
            Environment.Exit(1)
        End If
    End Sub

    Sub TestParsing()
        Console.WriteLine("--- Test: Parsing ---")
        AssertEquals("Parse null", JsonValueType.Null, JsonUtils.Parse("null").Type)
        AssertEquals("Parse true", JsonValueType.Boolean, JsonUtils.Parse("true").Type)
        AssertEquals("Parse true value", True, JsonUtils.Parse("true").AsBoolean())
        AssertEquals("Parse false value", False, JsonUtils.Parse("false").AsBoolean())
        AssertEquals("Parse integer", JsonValueType.Number, JsonUtils.Parse("42").Type)
        AssertEquals("Parse integer value", 42.0, JsonUtils.Parse("42").AsNumber())
        AssertEquals("Parse negative", -123.0, JsonUtils.Parse("-123").AsNumber())
        AssertEquals("Parse float", 3.14, JsonUtils.Parse("3.14").AsNumber())
        AssertEquals("Parse string", JsonValueType.String, JsonUtils.Parse("""hello""").Type)
        AssertEquals("Parse string value", "hello", JsonUtils.Parse("""hello""").AsString())
        AssertEquals("Parse empty array", JsonValueType.Array, JsonUtils.Parse("[]").Type)
        AssertEquals("Parse array count", 3, JsonUtils.Parse("[1, 2, 3]").GetCount())
        AssertEquals("Parse empty object", JsonValueType.Object, JsonUtils.Parse("{}").Type)
        AssertEquals("Parse object has key", True, JsonUtils.Parse("{""a"": 1}").HasKey("a"))
        AssertEquals("Parse invalid returns null type", JsonValueType.Null, JsonUtils.Parse("invalid").Type)
        AssertEquals("IsValid true", True, JsonUtils.IsValid("{}"))
        AssertEquals("IsValid false", False, JsonUtils.IsValid("invalid"))
        Console.WriteLine()
    End Sub

    Sub TestSerialization()
        Console.WriteLine("--- Test: Serialization ---")
        AssertEquals("Serialize null", "null", JsonUtils.Serialize(New JsonValue()))
        AssertEquals("Serialize true", "true", JsonUtils.Serialize(JsonValue.CreateBoolean(True)))
        AssertEquals("Serialize false", "false", JsonUtils.Serialize(JsonValue.CreateBoolean(False)))
        AssertEquals("Serialize integer", "42", JsonUtils.Serialize(JsonValue.CreateNumber(42)))
        AssertEquals("Serialize float", "3.14", JsonUtils.Serialize(JsonValue.CreateNumber(3.14)))
        AssertEquals("Serialize string", """hello""", JsonUtils.Serialize(JsonValue.CreateString("hello")))
        Dim arr As JsonValue = JsonUtils.Parse("[1,2]")
        AssertEquals("Serialize array", "[1,2]", JsonUtils.Serialize(arr))
        Dim obj As JsonValue = JsonUtils.Parse("{""name"":""test""}")
        AssertEquals("Serialize object", "{""name"":""test""}", JsonUtils.Serialize(obj))
        Console.WriteLine()
    End Sub

    Sub TestTypeChecking()
        Console.WriteLine("--- Test: Type Checking ---")
        Dim nullVal As New JsonValue()
        AssertEquals("IsNull", True, nullVal.IsNull())
        AssertEquals("IsBoolean false", False, nullVal.IsBoolean())
        Dim boolVal = JsonValue.CreateBoolean(True)
        AssertEquals("IsBoolean", True, boolVal.IsBoolean())
        AssertEquals("IsNull false", False, boolVal.IsNull())
        Dim numVal = JsonValue.CreateNumber(42)
        AssertEquals("IsNumber", True, numVal.IsNumber())
        Dim strVal = JsonValue.CreateString("test")
        AssertEquals("IsString", True, strVal.IsString())
        Dim arrVal = JsonValue.CreateArray()
        AssertEquals("IsArray", True, arrVal.IsArray())
        Dim objVal = JsonValue.CreateObject()
        AssertEquals("IsObject", True, objVal.IsObject())
        Console.WriteLine()
    End Sub

    Sub TestTypeConversion()
        Console.WriteLine("--- Test: Type Conversion ---")
        Dim nullVal As New JsonValue()
        AssertEquals("Null AsBoolean default", False, nullVal.AsBoolean())
        AssertEquals("Null AsNumber default", 0.0, nullVal.AsNumber())
        AssertEquals("Null AsString default", "", nullVal.AsString())
        Dim boolVal = JsonValue.CreateBoolean(True)
        AssertEquals("Boolean AsBoolean", True, boolVal.AsBoolean())
        Dim numVal = JsonValue.CreateNumber(42.5)
        AssertEquals("Number AsNumber", 42.5, numVal.AsNumber())
        Dim strVal = JsonValue.CreateString("hello")
        AssertEquals("String AsString", "hello", strVal.AsString())
        Console.WriteLine()
    End Sub

    Sub TestObjectAccess()
        Console.WriteLine("--- Test: Object Access ---")
        Dim json As String = "{""name"":""John"",""age"":30,""active"":true}"
        Dim obj = JsonUtils.Parse(json)
        AssertEquals("Object HasKey existing", True, obj.HasKey("name"))
        AssertEquals("Object HasKey missing", False, obj.HasKey("missing"))
        AssertEquals("GetString existing", "John", obj.GetString("name"))
        AssertEquals("GetString default", "default", obj.GetString("missing", "default"))
        AssertEquals("GetNumber existing", 30.0, obj.GetNumber("age"))
        AssertEquals("GetBoolean existing", True, obj.GetBoolean("active"))
        Dim keys = obj.GetKeys()
        AssertEquals("GetKeys count", 3, keys.Count)
        Console.WriteLine()
    End Sub

    Sub TestArrayAccess()
        Console.WriteLine("--- Test: Array Access ---")
        Dim json As String = "[1, 2, 3, 4, 5]"
        Dim arr = JsonUtils.Parse(json)
        AssertEquals("Array GetCount", 5, arr.GetCount())
        AssertEquals("Array GetItem 0", 1.0, arr.GetItem(0).AsNumber())
        AssertEquals("Array GetItem 4", 5.0, arr.GetItem(4).AsNumber())
        Dim outOfBounds = arr.GetItem(10)
        AssertEquals("Array out of bounds type", JsonValueType.Null, outOfBounds.Type)
        Console.WriteLine()
    End Sub

    Sub TestPrettyPrint()
        Console.WriteLine("--- Test: Pretty Print ---")
        Dim obj As JsonValue = JsonUtils.Parse("{""a"":1,""b"":2}")
        Dim pretty = JsonUtils.SerializePretty(obj)
        AssertContains("Pretty print contains newline", vbCrLf, pretty)
        AssertContains("Pretty print contains indent", "  ", pretty)
        Dim minified = JsonUtils.Minify("{ ""a"" : 1 , ""b"" : 2 }")
        AssertEquals("Minify", "{""a"":1,""b"":2}", minified)
        Console.WriteLine()
    End Sub

    Sub TestFileOperations()
        Console.WriteLine("--- Test: File Operations ---")
        Dim testFile As String = "test_json.json"
        If File.Exists(testFile) Then File.Delete(testFile)
        Dim obj As JsonValue = JsonUtils.Parse("{""test"":""value"",""number"":42}")
        JsonUtils.WriteFile(testFile, obj)
        AssertEquals("WriteFile creates file", True, File.Exists(testFile))
        Dim parsed = JsonUtils.ParseFile(testFile)
        AssertEquals("ParseFile type", JsonValueType.Object, parsed.Type)
        AssertEquals("ParseFile value", "value", parsed.GetString("test"))
        If File.Exists(testFile) Then File.Delete(testFile)
        Console.WriteLine()
    End Sub

    Sub TestEdgeCases()
        Console.WriteLine("--- Test: Edge Cases ---")
        AssertEquals("Whitespace before value", JsonValueType.Number, JsonUtils.Parse("   42").Type)
        AssertEquals("Whitespace after value", JsonValueType.Number, JsonUtils.Parse("42   ").Type)
        Dim nested = JsonUtils.Parse("{""a"":{""b"":{""c"":1}}}")
        AssertEquals("Nested object", 1.0, nested.GetValue("a").GetValue("b").GetNumber("c"))
        Dim emptyObj = JsonUtils.Parse("{}")
        AssertEquals("Empty object keys count", 0, emptyObj.GetKeys().Count)
        Dim emptyArr = JsonUtils.Parse("[]")
        AssertEquals("Empty array count", 0, emptyArr.GetCount())
        Console.WriteLine()
    End Sub

    Sub TestComplexStructures()
        Console.WriteLine("--- Test: Complex Structures ---")
        Dim json As String = "{""users"":[{""id"":1,""name"":""Alice""},{""id"":2,""name"":""Bob""}],""count"":2}"
        Dim data = JsonUtils.Parse(json)
        AssertEquals("Complex object type", JsonValueType.Object, data.Type)
        AssertEquals("Users array count", 2, data.GetValue("users").GetCount())
        AssertEquals("First user name", "Alice", data.GetValue("users").GetItem(0).GetString("name"))
        AssertEquals("Second user id", 2.0, data.GetValue("users").GetItem(1).GetNumber("id"))
        AssertEquals("Count value", 2.0, data.GetNumber("count"))
        Console.WriteLine()
    End Sub

    ' =========================================================================
    ' Assertion Helpers
    ' =========================================================================
    Sub AssertEquals(name As String, expected As Object, actual As Object)
        If expected.Equals(actual) Then
            _passed += 1
            Console.WriteLine($"  [PASS] {name}")
        Else
            _failed += 1
            Console.WriteLine($"  [FAIL] {name}")
            Console.WriteLine($"         Expected: {expected}")
            Console.WriteLine($"         Actual: {actual}")
        End If
    End Sub

    Sub AssertContains(name As String, expected As String, actual As String)
        If actual.Contains(expected) Then
            _passed += 1
            Console.WriteLine($"  [PASS] {name}")
        Else
            _failed += 1
            Console.WriteLine($"  [FAIL] {name}")
            Console.WriteLine($"         Expected to contain: {expected}")
            Console.WriteLine($"         Actual: {actual}")
        End If
    End Sub

End Module
