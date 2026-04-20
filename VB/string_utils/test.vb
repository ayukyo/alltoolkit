' =============================================================================
' AllToolkit - String Utilities Tests for VB.NET
' =============================================================================
' Comprehensive unit tests for StringUtils module.
' Run with: dotnet test (after adding to test project)
' =============================================================================

Imports System
Imports System.Collections.Generic
Imports Microsoft.VisualStudio.TestTools.UnitTesting
Imports AllToolkit

<TestClass>
Public Class StringUtilsTests

    ' =========================================================================
    ' Case Transformation Tests
    ' =========================================================================

    <TestMethod>
    Public Sub ToCamelCase_EmptyString_ReturnsEmpty()
        Assert.AreEqual(String.Empty, StringUtils.ToCamelCase(""))
        Assert.AreEqual(Nothing, StringUtils.ToCamelCase(Nothing))
    End Sub

    <TestMethod>
    Public Sub ToCamelCase_SingleWord_ReturnsLowercase()
        Assert.AreEqual("hello", StringUtils.ToCamelCase("Hello"))
        Assert.AreEqual("world", StringUtils.ToCamelCase("WORLD"))
    End Sub

    <TestMethod>
    Public Sub ToCamelCase_MultipleWords_ConvertsCorrectly()
        Assert.AreEqual("helloWorld", StringUtils.ToCamelCase("hello world"))
        Assert.AreEqual("fooBarBaz", StringUtils.ToCamelCase("FOO BAR BAZ"))
        Assert.AreEqual("myVariableName", StringUtils.ToCamelCase("my_variable_name"))
        Assert.AreEqual("cssClassName", StringUtils.ToCamelCase("css-class-name"))
    End Sub

    <TestMethod>
    Public Sub ToPascalCase_EmptyString_ReturnsEmpty()
        Assert.AreEqual(String.Empty, StringUtils.ToPascalCase(""))
        Assert.AreEqual(Nothing, StringUtils.ToPascalCase(Nothing))
    End Sub

    <TestMethod>
    Public Sub ToPascalCase_MultipleWords_ConvertsCorrectly()
        Assert.AreEqual("HelloWorld", StringUtils.ToPascalCase("hello world"))
        Assert.AreEqual("FooBarBaz", StringUtils.ToPascalCase("foo_bar_baz"))
        Assert.AreEqual("MyClassName", StringUtils.ToPascalCase("my-class-name"))
    End Sub

    <TestMethod>
    Public Sub ToSnakeCase_ConvertsCorrectly()
        Assert.AreEqual("hello", StringUtils.ToSnakeCase("hello"))
        Assert.AreEqual("hello_world", StringUtils.ToSnakeCase("helloWorld"))
        Assert.AreEqual("foo_bar_baz", StringUtils.ToSnakeCase("FooBarBaz"))
    End Sub

    <TestMethod>
    Public Sub ToKebabCase_ConvertsCorrectly()
        Assert.AreEqual("hello", StringUtils.ToKebabCase("hello"))
        Assert.AreEqual("hello-world", StringUtils.ToKebabCase("helloWorld"))
        Assert.AreEqual("foo-bar-baz", StringUtils.ToKebabCase("FooBarBaz"))
        Assert.AreEqual("my-class-name", StringUtils.ToKebabCase("my_class_name"))
    End Sub

    <TestMethod>
    Public Sub ToTitleCase_ConvertsCorrectly()
        Assert.AreEqual("Hello World", StringUtils.ToTitleCase("hello world"))
        Assert.AreEqual("The Quick Brown Fox", StringUtils.ToTitleCase("THE QUICK BROWN FOX"))
    End Sub

    <TestMethod>
    Public Sub ToSentenceCase_ConvertsCorrectly()
        Assert.AreEqual("Hello world", StringUtils.ToSentenceCase("HELLO WORLD"))
        Assert.AreEqual("The quick brown fox", StringUtils.ToSentenceCase("the quick brown fox"))
    End Sub

    ' =========================================================================
    ' Validation Tests
    ' =========================================================================

    <TestMethod>
    Public Sub IsValidEmail_ValidEmails_ReturnsTrue()
        Assert.IsTrue(StringUtils.IsValidEmail("test@example.com"))
        Assert.IsTrue(StringUtils.IsValidEmail("user.name@domain.co.uk"))
        Assert.IsTrue(StringUtils.IsValidEmail("user+tag@example.org"))
    End Sub

    <TestMethod>
    Public Sub IsValidEmail_InvalidEmails_ReturnsFalse()
        Assert.IsFalse(StringUtils.IsValidEmail(""))
        Assert.IsFalse(StringUtils.IsValidEmail("notanemail"))
        Assert.IsFalse(StringUtils.IsValidEmail("@example.com"))
        Assert.IsFalse(StringUtils.IsValidEmail("user@"))
        Assert.IsFalse(StringUtils.IsValidEmail("user @example.com"))
    End Sub

    <TestMethod>
    Public Sub IsValidUrl_ValidUrls_ReturnsTrue()
        Assert.IsTrue(StringUtils.IsValidUrl("http://example.com"))
        Assert.IsTrue(StringUtils.IsValidUrl("https://example.com/path"))
        Assert.IsTrue(StringUtils.IsValidUrl("https://example.com/path?query=1"))
    End Sub

    <TestMethod>
    Public Sub IsValidUrl_RequireHttps_WorksCorrectly()
        Assert.IsTrue(StringUtils.IsValidUrl("https://example.com", True))
        Assert.IsFalse(StringUtils.IsValidUrl("http://example.com", True))
    End Sub

    <TestMethod>
    Public Sub IsValidUrl_InvalidUrls_ReturnsFalse()
        Assert.IsFalse(StringUtils.IsValidUrl(""))
        Assert.IsFalse(StringUtils.IsValidUrl("not a url"))
        Assert.IsFalse(StringUtils.IsValidUrl("ftp://example.com"))
    End Sub

    <TestMethod>
    Public Sub IsValidPhone_ValidPhones_ReturnsTrue()
        Assert.IsTrue(StringUtils.IsValidPhone("+1234567890"))
        Assert.IsTrue(StringUtils.IsValidPhone("+1 (234) 567-8901"))
        Assert.IsTrue(StringUtils.IsValidPhone("+86 138 1234 5678"))
    End Sub

    <TestMethod>
    Public Sub IsValidPhone_InvalidPhones_ReturnsFalse()
        Assert.IsFalse(StringUtils.IsValidPhone(""))
        Assert.IsFalse(StringUtils.IsValidPhone("123"))
        Assert.IsFalse(StringUtils.IsValidPhone("+0123456789")) ' Starts with 0 after +
    End Sub

    <TestMethod>
    Public Sub IsValidCreditCard_ValidCards_ReturnsTrue()
        ' These are test card numbers that pass Luhn check
        Assert.IsTrue(StringUtils.IsValidCreditCard("4532015112830366")) ' Visa
        Assert.IsTrue(StringUtils.IsValidCreditCard("5555555555554444")) ' MasterCard
        Assert.IsTrue(StringUtils.IsValidCreditCard("378282246310005")) ' Amex
    End Sub

    <TestMethod>
    Public Sub IsValidCreditCard_InvalidCards_ReturnsFalse()
        Assert.IsFalse(StringUtils.IsValidCreditCard(""))
        Assert.IsFalse(StringUtils.IsValidCreditCard("1234567890123456"))
        Assert.IsFalse(StringUtils.IsValidCreditCard("0000000000000000"))
    End Sub

    <TestMethod>
    Public Sub IsValidIPv4_ValidAddresses_ReturnsTrue()
        Assert.IsTrue(StringUtils.IsValidIPv4("192.168.1.1"))
        Assert.IsTrue(StringUtils.IsValidIPv4("0.0.0.0"))
        Assert.IsTrue(StringUtils.IsValidIPv4("255.255.255.255"))
    End Sub

    <TestMethod>
    Public Sub IsValidIPv4_InvalidAddresses_ReturnsFalse()
        Assert.IsFalse(StringUtils.IsValidIPv4(""))
        Assert.IsFalse(StringUtils.IsValidIPv4("256.1.1.1"))
        Assert.IsFalse(StringUtils.IsValidIPv4("192.168.1"))
        Assert.IsFalse(StringUtils.IsValidIPv4("192.168.1.1.1"))
        Assert.IsFalse(StringUtils.IsValidIPv4("192.168.01.1")) ' Leading zero
    End Sub

    <TestMethod>
    Public Sub IsValidHexColor_ValidColors_ReturnsTrue()
        Assert.IsTrue(StringUtils.IsValidHexColor("#fff"))
        Assert.IsTrue(StringUtils.IsValidHexColor("#ffffff"))
        Assert.IsTrue(StringUtils.IsValidHexColor("#ABCDEF"))
        Assert.IsTrue(StringUtils.IsValidHexColor("#123456"))
    End Sub

    <TestMethod>
    Public Sub IsValidHexColor_InvalidColors_ReturnsFalse()
        Assert.IsFalse(StringUtils.IsValidHexColor(""))
        Assert.IsFalse(StringUtils.IsValidHexColor("ffffff"))
        Assert.IsFalse(StringUtils.IsValidHexColor("#ff"))
        Assert.IsFalse(StringUtils.IsValidHexColor("#fffff"))
        Assert.IsFalse(StringUtils.IsValidHexColor("#gggggg"))
    End Sub

    <TestMethod>
    Public Sub IsAlphanumeric_WorksCorrectly()
        Assert.IsTrue(StringUtils.IsAlphanumeric("abc123"))
        Assert.IsTrue(StringUtils.IsAlphanumeric("ABC"))
        Assert.IsTrue(StringUtils.IsAlphanumeric("123"))
        Assert.IsFalse(StringUtils.IsAlphanumeric("abc 123"))
        Assert.IsFalse(StringUtils.IsAlphanumeric("abc-123"))
        Assert.IsFalse(StringUtils.IsAlphanumeric(""))
    End Sub

    ' =========================================================================
    ' Manipulation Tests
    ' =========================================================================

    <TestMethod>
    Public Sub Truncate_LongString_TruncatesCorrectly()
        Assert.AreEqual("Hello…", StringUtils.Truncate("Hello World", 6))
        Assert.AreEqual("Hello World", StringUtils.Truncate("Hello World", 20))
        Assert.AreEqual("Hello...", StringUtils.Truncate("Hello World", 8, "..."))
    End Sub

    <TestMethod>
    Public Sub TruncateWords_TruncatesAtWordBoundary()
        Assert.AreEqual("Hello…", StringUtils.TruncateWords("Hello World", 8))
        Assert.AreEqual("Hello…", StringUtils.TruncateWords("Hello World Foo Bar", 10))
    End Sub

    <TestMethod>
    Public Sub Repeat_RepeatsString()
        Assert.AreEqual("abcabcabc", StringUtils.Repeat("abc", 3))
        Assert.AreEqual("---", StringUtils.Repeat("-", 3))
        Assert.AreEqual("", StringUtils.Repeat("abc", 0))
        Assert.AreEqual("", StringUtils.Repeat("", 5))
    End Sub

    <TestMethod>
    Public Sub Reverse_ReversesString()
        Assert.AreEqual("cba", StringUtils.Reverse("abc"))
        Assert.AreEqual("12345", StringUtils.Reverse("54321"))
        Assert.AreEqual("", StringUtils.Reverse(""))
    End Sub

    <TestMethod>
    Public Sub PadCenter_PadsEqually()
        Assert.AreEqual("  hi  ", StringUtils.PadCenter("hi", 6))
        Assert.AreEqual("---test---", StringUtils.PadCenter("test", 10, "-"c))
    End Sub

    <TestMethod>
    Public Sub RemoveAll_RemovesAllOccurrences()
        Assert.AreEqual("Heo Word", StringUtils.RemoveAll("Hello World", "l"))
        Assert.AreEqual("H W", StringUtils.RemoveAll("Hello World", "ello"))
    End Sub

    <TestMethod>
    Public Sub StripHtml_RemovesTags()
        Assert.AreEqual("Hello World", StringUtils.StripHtml("<p>Hello World</p>"))
        Assert.AreEqual("Hello World", StringUtils.StripHtml("<div><b>Hello</b> <i>World</i></div>"))
        Assert.AreEqual("Tom & Jerry", StringUtils.StripHtml("Tom &amp; Jerry"))
    End Sub

    <TestMethod>
    Public Sub NormalizeWhitespace_CollapsesSpaces()
        Assert.AreEqual("Hello World", StringUtils.NormalizeWhitespace("Hello    World"))
        Assert.AreEqual("Test", StringUtils.NormalizeWhitespace("   Test   "))
        Assert.AreEqual("A B C", StringUtils.NormalizeWhitespace("A  B   C"))
    End Sub

    ' =========================================================================
    ' Searching Tests
    ' =========================================================================

    <TestMethod>
    Public Sub CountOccurrences_CountsCorrectly()
        Assert.AreEqual(2, StringUtils.CountOccurrences("Hello", "l"))
        Assert.AreEqual(3, StringUtils.CountOccurrences("aaa", "a"))
        Assert.AreEqual(0, StringUtils.CountOccurrences("abc", "z"))
        Assert.AreEqual(2, StringUtils.CountOccurrences("Hello Hello", "Hello"))
    End Sub

    <TestMethod>
    Public Sub FindAllPositions_FindsAllPositions()
        Dim positions As List(Of Integer) = StringUtils.FindAllPositions("ababab", "ab")
        Assert.AreEqual(3, positions.Count)
        CollectionAssert.AreEqual({0, 2, 4}, positions.ToArray())
    End Sub

    <TestMethod>
    Public Sub StartsWithAny_WorksCorrectly()
        Assert.IsTrue(StringUtils.StartsWithAny("hello world", "hi", "he", "ho"))
        Assert.IsFalse(StringUtils.StartsWithAny("hello world", "a", "b", "c"))
    End Sub

    <TestMethod>
    Public Sub EndsWithAny_WorksCorrectly()
        Assert.IsTrue(StringUtils.EndsWithAny("hello.txt", ".txt", ".csv", ".json"))
        Assert.IsFalse(StringUtils.EndsWithAny("hello.doc", ".txt", ".csv", ".json"))
    End Sub

    ' =========================================================================
    ' Generation Tests
    ' =========================================================================

    <TestMethod>
    Public Sub RandomString_GeneratesCorrectLength()
        Dim str1 As String = StringUtils.RandomString(10)
        Assert.AreEqual(10, str1.Length)
        
        Dim str2 As String = StringUtils.RandomString(20)
        Assert.AreEqual(20, str2.Length)
    End Sub

    <TestMethod>
    Public Sub RandomString_UsesCustomCharset()
        Dim str As String = StringUtils.RandomString(10, "a")
        Assert.AreEqual("aaaaaaaaaa", str)
    End Sub

    <TestMethod>
    Public Sub RandomString_GeneratesDifferentStrings()
        Dim str1 As String = StringUtils.RandomString(20)
        Dim str2 As String = StringUtils.RandomString(20)
        Assert.AreNotEqual(str1, str2)
    End Sub

    <TestMethod>
    Public Sub RandomHex_GeneratesValidHex()
        Dim hex As String = StringUtils.RandomHex(16)
        Assert.AreEqual(16, hex.Length)
        
        For Each c As Char In hex
            Assert.IsTrue("0123456789abcdef".Contains(c))
        Next
    End Sub

    <TestMethod>
    Public Sub RandomPassword_GeneratesValidPassword()
        Dim password As String = StringUtils.RandomPassword(16)
        Assert.AreEqual(16, password.Length)
        
        ' Should have uppercase, lowercase, digit, special
        Assert.IsTrue(password.Any(Function(c) Char.IsLower(c)))
        Assert.IsTrue(password.Any(Function(c) Char.IsUpper(c)))
        Assert.IsTrue(password.Any(Function(c) Char.IsDigit(c)))
    End Sub

    <TestMethod>
    Public Sub RandomPassword_NoSpecial_NoSpecialChars()
        Dim password As String = StringUtils.RandomPassword(16, False)
        Assert.AreEqual(16, password.Length)
        
        For Each c As Char In password
            Assert.IsTrue(Char.IsLetterOrDigit(c))
        Next
    End Sub

    <TestMethod>
    Public Sub GenerateUuid_GeneratesValidFormat()
        Dim uuid As String = StringUtils.GenerateUuid()
        Assert.AreEqual(36, uuid.Length)
        Assert.AreEqual("-", uuid(8))
        Assert.AreEqual("-", uuid(13))
        Assert.AreEqual("-", uuid(18))
        Assert.AreEqual("-", uuid(23))
    End Sub

    <TestMethod>
    Public Sub GenerateShortId_GeneratesCorrectLength()
        Dim id As String = StringUtils.GenerateShortId()
        Assert.AreEqual(8, id.Length)
    End Sub

    ' =========================================================================
    ' Encoding Tests
    ' =========================================================================

    <TestMethod>
    Public Sub Base64Encode_EncodesCorrectly()
        Assert.AreEqual("SGVsbG8gV29ybGQ=", StringUtils.Base64Encode("Hello World"))
        Assert.AreEqual("YWJjMTIz", StringUtils.Base64Encode("abc123"))
    End Sub

    <TestMethod>
    Public Sub Base64Decode_DecodesCorrectly()
        Assert.AreEqual("Hello World", StringUtils.Base64Decode("SGVsbG8gV29ybGQ="))
        Assert.AreEqual("abc123", StringUtils.Base64Decode("YWJjMTIz"))
    End Sub

    <TestMethod>
    Public Sub Base64_RoundTrip_WorksCorrectly()
        Dim original As String = "The quick brown fox jumps over the lazy dog"
        Dim encoded As String = StringUtils.Base64Encode(original)
        Dim decoded As String = StringUtils.Base64Decode(encoded)
        Assert.AreEqual(original, decoded)
    End Sub

    <TestMethod>
    Public Sub UrlEncode_EncodesCorrectly()
        Assert.AreEqual("hello%20world", StringUtils.UrlEncode("hello world"))
        Assert.AreEqual("a%2Bb%3Dc", StringUtils.UrlEncode("a+b=c"))
    End Sub

    <TestMethod>
    Public Sub UrlDecode_DecodesCorrectly()
        Assert.AreEqual("hello world", StringUtils.UrlDecode("hello%20world"))
        Assert.AreEqual("a+b=c", StringUtils.UrlDecode("a%2Bb%3Dc"))
    End Sub

    <TestMethod>
    Public Sub Url_RoundTrip_WorksCorrectly()
        Dim original As String = "name=John Doe&age=30"
        Dim encoded As String = StringUtils.UrlEncode(original)
        Dim decoded As String = StringUtils.UrlDecode(encoded)
        Assert.AreEqual(original, decoded)
    End Sub

    ' =========================================================================
    ' Similarity Tests
    ' =========================================================================

    <TestMethod>
    Public Sub LevenshteinDistance_CalculatesCorrectly()
        Assert.AreEqual(0, StringUtils.LevenshteinDistance("abc", "abc"))
        Assert.AreEqual(1, StringUtils.LevenshteinDistance("abc", "abd"))
        Assert.AreEqual(3, StringUtils.LevenshteinDistance("kitten", "sitting"))
        Assert.AreEqual(2, StringUtils.LevenshteinDistance("book", "back"))
    End Sub

    <TestMethod>
    Public Sub LevenshteinDistance_HandlesEmptyStrings()
        Assert.AreEqual(3, StringUtils.LevenshteinDistance("", "abc"))
        Assert.AreEqual(3, StringUtils.LevenshteinDistance("abc", ""))
        Assert.AreEqual(0, StringUtils.LevenshteinDistance("", ""))
    End Sub

    <TestMethod>
    Public Sub SimilarityPercentage_CalculatesCorrectly()
        Assert.AreEqual(100.0, StringUtils.SimilarityPercentage("abc", "abc"))
        Assert.IsTrue(StringUtils.SimilarityPercentage("abc", "abd") > 50)
        Assert.IsTrue(StringUtils.SimilarityPercentage("abc", "xyz") < 50)
    End Sub

    <TestMethod>
    Public Sub HammingDistance_CalculatesCorrectly()
        Assert.AreEqual(0, StringUtils.HammingDistance("abc", "abc"))
        Assert.AreEqual(1, StringUtils.HammingDistance("abc", "abd"))
        Assert.AreEqual(3, StringUtils.HammingDistance("abc", "xyz"))
    End Sub

    <TestMethod>
    <ExpectedException(GetType(ArgumentException))>
    Public Sub HammingDistance_DifferentLengths_ThrowsException()
        StringUtils.HammingDistance("abc", "abcd")
    End Sub

    ' =========================================================================
    ' Formatting Tests
    ' =========================================================================

    <TestMethod>
    Public Sub FormatNumber_FormatsCorrectly()
        Dim result As String = StringUtils.FormatNumber(1234567.89, 2)
        Assert.IsTrue(result.Contains("1") AndAlso result.Contains("234") AndAlso result.Contains("567"))
    End Sub

    <TestMethod>
    Public Sub FormatCurrency_FormatsCorrectly()
        Dim result As String = StringUtils.FormatCurrency(1234.56, "$")
        Assert.IsTrue(result.StartsWith("$"))
        Assert.IsTrue(result.Contains("1234"))
    End Sub

    <TestMethod>
    Public Sub FormatPercentage_FormatsCorrectly()
        Dim result As String = StringUtils.FormatPercentage(75.5, 1)
        Assert.IsTrue(result.Contains("75"))
        Assert.IsTrue(result.EndsWith("%"))
    End Sub

    <TestMethod>
    Public Sub FormatFileSize_FormatsCorrectly()
        Assert.AreEqual("0 B", StringUtils.FormatFileSize(0))
        Assert.IsTrue(StringUtils.FormatFileSize(1023).EndsWith(" B"))
        Assert.IsTrue(StringUtils.FormatFileSize(1024).EndsWith(" KB"))
        Assert.IsTrue(StringUtils.FormatFileSize(1048576).EndsWith(" MB"))
        Assert.IsTrue(StringUtils.FormatFileSize(1073741824).EndsWith(" GB"))
    End Sub

    ' =========================================================================
    ' Parsing Tests
    ' =========================================================================

    <TestMethod>
    Public Sub ParseQueryString_ParsesCorrectly()
        Dim result As Dictionary(Of String, String) = StringUtils.ParseQueryString("?name=John&age=30")
        Assert.AreEqual(2, result.Count)
        Assert.AreEqual("John", result("name"))
        Assert.AreEqual("30", result("age"))
    End Sub

    <TestMethod>
    Public Sub ParseQueryString_HandlesEmptyValues()
        Dim result As Dictionary(Of String, String) = StringUtils.ParseQueryString("flag&name=test")
        Assert.AreEqual(2, result.Count)
        Assert.AreEqual("", result("flag"))
        Assert.AreEqual("test", result("name"))
    End Sub

    <TestMethod>
    Public Sub ParseQueryString_EmptyString_ReturnsEmptyDictionary()
        Dim result As Dictionary(Of String, String) = StringUtils.ParseQueryString("")
        Assert.AreEqual(0, result.Count)
    End Sub

    <TestMethod>
    Public Sub BuildQueryString_BuildsCorrectly()
        Dim params As New Dictionary(Of String, String) From {
            {"name", "John Doe"},
            {"age", "30"}
        }
        Dim result As String = StringUtils.BuildQueryString(params)
        Assert.IsTrue(result.Contains("name=John%20Doe"))
        Assert.IsTrue(result.Contains("age=30"))
    End Sub

    <TestMethod>
    Public Sub QueryString_RoundTrip_WorksCorrectly()
        Dim original As New Dictionary(Of String, String) From {
            {"name", "John Doe"},
            {"city", "New York"},
            {"page", "1"}
        }
        Dim queryString As String = StringUtils.BuildQueryString(original)
        Dim parsed As Dictionary(Of String, String) = StringUtils.ParseQueryString(queryString)
        
        Assert.AreEqual(3, parsed.Count)
        Assert.AreEqual("John Doe", parsed("name"))
        Assert.AreEqual("New York", parsed("city"))
        Assert.AreEqual("1", parsed("page"))
    End Sub

End Class