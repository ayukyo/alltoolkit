' =============================================================================
' AllToolkit - String Utilities Examples for VB.NET
' =============================================================================
' Complete examples demonstrating all StringUtils features.
' Run with: dotnet run (after adding to console project)
' =============================================================================

Imports System
Imports System.Collections.Generic
Imports AllToolkit

Module StringUtilsExamples

    Sub Main()
        Console.WriteLine("="c, 60)
        Console.WriteLine("AllToolkit - StringUtils Examples for VB.NET")
        Console.WriteLine("="c, 60)
        Console.WriteLine()
        
        CaseTransformationExamples()
        ValidationExamples()
        ManipulationExamples()
        SearchingExamples()
        GenerationExamples()
        EncodingExamples()
        SimilarityExamples()
        FormattingExamples()
        ParsingExamples()
        
        Console.WriteLine()
        Console.WriteLine("All examples completed!")
    End Sub

    ' =========================================================================
    ' Case Transformation Examples
    ' =========================================================================

    Sub CaseTransformationExamples()
        Console.WriteLine("--- Case Transformations ---")
        
        Dim input As String = "hello world example"
        
        Console.WriteLine($"Original: {input}")
        Console.WriteLine($"camelCase: {StringUtils.ToCamelCase(input)}")
        Console.WriteLine($"PascalCase: {StringUtils.ToPascalCase(input)}")
        Console.WriteLine($"snake_case: {StringUtils.ToSnakeCase("helloWorldExample")}")
        Console.WriteLine($"kebab-case: {StringUtils.ToKebabCase("HelloWorldExample")}")
        Console.WriteLine($"Title Case: {StringUtils.ToTitleCase(input)}")
        Console.WriteLine($"Sentence case: {StringUtils.ToSentenceCase(input.ToUpper())}")
        
        ' Converting between formats
        Dim cssClass As String = "my-component-wrapper"
        Console.WriteLine($"{vbCrLf}CSS class '{cssClass}' to PascalCase: {StringUtils.ToPascalCase(cssClass)}")
        
        Dim dbName As String = "user_account_table"
        Console.WriteLine($"Database table '{dbName}' to PascalCase: {StringUtils.ToPascalCase(dbName)}")
        
        Console.WriteLine()
    End Sub

    ' =========================================================================
    ' Validation Examples
    ' =========================================================================

    Sub ValidationExamples()
        Console.WriteLine("--- Validation ---")
        
        ' Email validation
        Dim emails As String() = {"user@example.com", "invalid-email", "name.surname@company.co.uk"}
        For Each email As String In emails
            Console.WriteLine($"Email '{email}' valid: {StringUtils.IsValidEmail(email)}")
        Next
        
        ' URL validation
        Console.WriteLine($"{vbCrLf}URL validation:")
        Console.WriteLine($"https://example.com valid: {StringUtils.IsValidUrl("https://example.com")}")
        Console.WriteLine($"http://example.com (require HTTPS): {StringUtils.IsValidUrl("http://example.com", True)}")
        Console.WriteLine($"ftp://example.com valid: {StringUtils.IsValidUrl("ftp://example.com")}")
        
        ' Phone validation
        Console.WriteLine($"{vbCrLf}Phone validation:")
        Dim phones As String() = {"+1 (555) 123-4567", "+86 138 1234 5678", "invalid"}
        For Each phone As String In phones
            Console.WriteLine($"Phone '{phone}' valid: {StringUtils.IsValidPhone(phone)}")
        Next
        
        ' Credit card validation (test cards that pass Luhn check)
        Console.WriteLine($"{vbCrLf}Credit card validation:")
        Console.WriteLine($"Visa 4532015112830366 valid: {StringUtils.IsValidCreditCard("4532015112830366")}")
        Console.WriteLine($"Invalid card 1234567890123456 valid: {StringUtils.IsValidCreditCard("1234567890123456")}")
        
        ' IPv4 validation
        Console.WriteLine($"{vbCrLf}IPv4 validation:")
        Console.WriteLine($"192.168.1.1 valid: {StringUtils.IsValidIPv4("192.168.1.1")}")
        Console.WriteLine($"256.1.1.1 valid: {StringUtils.IsValidIPv4("256.1.1.1")}")
        
        ' Hex color validation
        Console.WriteLine($"{vbCrLf}Hex color validation:")
        Console.WriteLine($"#ffffff valid: {StringUtils.IsValidHexColor("#ffffff")}")
        Console.WriteLine($"#gggggg valid: {StringUtils.IsValidHexColor("#gggggg")}")
        
        Console.WriteLine()
    End Sub

    ' =========================================================================
    ' Manipulation Examples
    ' =========================================================================

    Sub ManipulationExamples()
        Console.WriteLine("--- Manipulation ---")
        
        ' Truncate
        Dim longText As String = "The quick brown fox jumps over the lazy dog"
        Console.WriteLine($"Original: {longText}")
        Console.WriteLine($"Truncated (20): {StringUtils.Truncate(longText, 20)}")
        Console.WriteLine($"Truncated words (20): {StringUtils.TruncateWords(longText, 20)}")
        
        ' Repeat
        Console.WriteLine($"{vbCrLf}Repeat 'abc' 3 times: {StringUtils.Repeat("abc", 3)}")
        Console.WriteLine($"Repeat '-' 10 times: {StringUtils.Repeat("-", 10)}")
        
        ' Reverse
        Console.WriteLine($"{vbCrLf}Reverse 'hello': {StringUtils.Reverse("hello")}")
        
        ' Pad center
        Console.WriteLine($"{vbCrLf}Pad center 'hi' to 10: '{StringUtils.PadCenter("hi", 10)}'")
        Console.WriteLine($"Pad center 'test' to 10 with '-': '{StringUtils.PadCenter("test", 10, "-"c)}'")
        
        ' Remove all
        Console.WriteLine($"{vbCrLf}Remove all 'l' from 'Hello': {StringUtils.RemoveAll("Hello World", "l")}")
        
        ' Strip HTML
        Dim html As String = "<div><b>Bold</b> and <i>italic</i> text &amp; more</div>"
        Console.WriteLine($"{vbCrLf}Strip HTML: {StringUtils.StripHtml(html)}")
        
        ' Normalize whitespace
        Console.WriteLine($"Normalize 'Hello    World  Test': '{StringUtils.NormalizeWhitespace("Hello    World  Test")}'")
        
        Console.WriteLine()
    End Sub

    ' =========================================================================
    ' Searching Examples
    ' =========================================================================

    Sub SearchingExamples()
        Console.WriteLine("--- Searching ---")
        
        ' Count occurrences
        Dim text As String = "The quick brown fox jumps over the lazy dog"
        Console.WriteLine($"Text: {text}")
        Console.WriteLine($"Count 'o': {StringUtils.CountOccurrences(text, "o")}")
        Console.WriteLine($"Count 'the': {StringUtils.CountOccurrences(text, "the", StringComparison.OrdinalIgnoreCase)}")
        
        ' Find all positions
        Console.WriteLine($"{vbCrLf}Positions of 'o' in 'hello world':")
        Dim positions As List(Of Integer) = StringUtils.FindAllPositions("hello world", "o")
        Console.WriteLine($"Positions: {String.Join(", ", positions)}")
        
        ' StartsWithAny / EndsWithAny
        Console.WriteLine($"{vbCrLf}Starts with any (hi/he/ho): {StringUtils.StartsWithAny("hello world", "hi", "he", "ho")}")
        Console.WriteLine($"Ends with any (.txt/.csv/.json): {StringUtils.EndsWithAny("data.txt", ".txt", ".csv", ".json")}")
        
        Console.WriteLine()
    End Sub

    ' =========================================================================
    ' Generation Examples
    ' =========================================================================

    Sub GenerationExamples()
        Console.WriteLine("--- Generation ---")
        
        ' Random strings
        Console.WriteLine($"Random string (16): {StringUtils.RandomString(16)}")
        Console.WriteLine($"Random hex (16): {StringUtils.RandomHex(16)}")
        Console.WriteLine($"Random alphanumeric (10): {StringUtils.RandomString(10, StringUtils.Alphanumeric)}")
        
        ' Passwords
        Console.WriteLine($"{vbCrLf}Random password (16 chars, with special):")
        Console.WriteLine($"  {StringUtils.RandomPassword(16)}")
        Console.WriteLine($"Random password (12 chars, no special):")
        Console.WriteLine($"  {StringUtils.RandomPassword(12, False)}")
        
        ' UUID and short ID
        Console.WriteLine($"{vbCrLf}UUID: {StringUtils.GenerateUuid()}")
        Console.WriteLine($"Short ID: {StringUtils.GenerateShortId()}")
        
        ' Generate multiple
        Console.WriteLine($"{vbCrLf}Generate 5 unique IDs:")
        For i As Integer = 1 To 5
            Console.WriteLine($"  {i}. {StringUtils.GenerateShortId()}")
        Next
        
        Console.WriteLine()
    End Sub

    ' =========================================================================
    ' Encoding Examples
    ' =========================================================================

    Sub EncodingExamples()
        Console.WriteLine("--- Encoding ---")
        
        ' Base64
        Dim original As String = "Hello, World! This is a test string."
        Dim encoded As String = StringUtils.Base64Encode(original)
        Dim decoded As String = StringUtils.Base64Decode(encoded)
        
        Console.WriteLine($"Original: {original}")
        Console.WriteLine($"Base64 encoded: {encoded}")
        Console.WriteLine($"Base64 decoded: {decoded}")
        
        ' URL encoding
        Dim urlData As String = "name=John Doe&city=New York&age=30"
        Dim urlEncoded As String = StringUtils.UrlEncode(urlData)
        Dim urlDecoded As String = StringUtils.UrlDecode(urlEncoded)
        
        Console.WriteLine($"{vbCrLf}URL encoding:")
        Console.WriteLine($"Original: {urlData}")
        Console.WriteLine($"URL encoded: {urlEncoded}")
        Console.WriteLine($"URL decoded: {urlDecoded}")
        
        Console.WriteLine()
    End Sub

    ' =========================================================================
    ' Similarity Examples
    ' =========================================================================

    Sub SimilarityExamples()
        Console.WriteLine("--- Similarity ---")
        
        ' Levenshtein distance
        Dim pairs As String(,) = {
            {"kitten", "sitting"},
            {"book", "back"},
            {"algorithm", "logarithm"},
            {"saturday", "sunday"}
        }
        
        Console.WriteLine("Levenshtein distances:")
        For i As Integer = 0 To pairs.GetLength(0) - 1
            Dim s1 As String = pairs(i, 0)
            Dim s2 As String = pairs(i, 1)
            Dim distance As Integer = StringUtils.LevenshteinDistance(s1, s2)
            Dim similarity As Double = StringUtils.SimilarityPercentage(s1, s2)
            Console.WriteLine($"  '{s1}' vs '{s2}': distance={distance}, similarity={similarity:F1}%")
        Next
        
        ' Hamming distance (same length strings)
        Console.WriteLine($"{vbCrLf}Hamming distance (same length strings):")
        Console.WriteLine($"  'karolin' vs 'kathrin': {StringUtils.HammingDistance("karolin", "kathrin")}")
        Console.WriteLine($"  '1011101' vs '1001001': {StringUtils.HammingDistance("1011101", "1001001")}")
        
        Console.WriteLine()
    End Sub

    ' =========================================================================
    ' Formatting Examples
    ' =========================================================================

    Sub FormattingExamples()
        Console.WriteLine("--- Formatting ---")
        
        ' Numbers
        Console.WriteLine($"Format number 1234567.89: {StringUtils.FormatNumber(1234567.89, 2)}")
        Console.WriteLine($"Format number 1234567: {StringUtils.FormatNumber(1234567, 0)}")
        
        ' Currency
        Console.WriteLine($"{vbCrLf}Currency:")
        Console.WriteLine($"USD: {StringUtils.FormatCurrency(1234.56, "$")}")
        Console.WriteLine($"EUR: {StringUtils.FormatCurrency(1234.56, "€")}")
        Console.WriteLine($"CNY: {StringUtils.FormatCurrency(1234.56, "¥")}")
        
        ' Percentage
        Console.WriteLine($"{vbCrLf}Percentage:")
        Console.WriteLine($"75.5%: {StringUtils.FormatPercentage(75.5, 1)}")
        Console.WriteLine($"100%: {StringUtils.FormatPercentage(100, 0)}")
        
        ' File sizes
        Console.WriteLine($"{vbCrLf}File sizes:")
        Console.WriteLine($"0 bytes: {StringUtils.FormatFileSize(0)}")
        Console.WriteLine($"500 bytes: {StringUtils.FormatFileSize(500)}")
        Console.WriteLine($"1 KB: {StringUtils.FormatFileSize(1024)}")
        Console.WriteLine($"1.5 MB: {StringUtils.FormatFileSize(1572864)}")
        Console.WriteLine($"1 GB: {StringUtils.FormatFileSize(1073741824)}")
        Console.WriteLine($"1 TB: {StringUtils.FormatFileSize(1099511627776)}")
        
        Console.WriteLine()
    End Sub

    ' =========================================================================
    ' Parsing Examples
    ' =========================================================================

    Sub ParsingExamples()
        Console.WriteLine("--- Parsing ---")
        
        ' Parse query string
        Dim queryString As String = "?name=John%20Doe&age=30&city=New%20York"
        Console.WriteLine($"Query string: {queryString}")
        
        Dim parsed As Dictionary(Of String, String) = StringUtils.ParseQueryString(queryString)
        Console.WriteLine("Parsed parameters:")
        For Each kvp As KeyValuePair(Of String, String) In parsed
            Console.WriteLine($"  {kvp.Key} = {kvp.Value}")
        Next
        
        ' Build query string
        Dim params As New Dictionary(Of String, String) From {
            {"search", "vb.net tutorial"},
            {"page", "1"},
            {"limit", "10"}
        }
        Dim built As String = StringUtils.BuildQueryString(params)
        Console.WriteLine($"{vbCrLf}Built query string: {built}")
        
        Console.WriteLine()
    End Sub

End Module