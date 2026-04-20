# String Utilities for VB.NET

Complete string manipulation library for VB.NET applications. Zero external dependencies.

## Features

### Case Transformations
- `ToCamelCase` - Convert to camelCase
- `ToPascalCase` - Convert to PascalCase
- `ToSnakeCase` - Convert to snake_case
- `ToKebabCase` - Convert to kebab-case
- `ToTitleCase` - Convert to Title Case
- `ToSentenceCase` - Convert to Sentence case

### String Validation
- `IsValidEmail` - Email validation
- `IsValidUrl` - URL validation (optional HTTPS requirement)
- `IsValidPhone` - Phone number validation (international format)
- `IsValidCreditCard` - Credit card validation (Luhn algorithm)
- `IsValidIPv4` - IPv4 address validation
- `IsValidHexColor` - Hex color code validation
- `IsAlphanumeric` - Check if alphanumeric only
- `IsValidDate` - Date validation

### String Manipulation
- `Truncate` - Truncate with suffix
- `TruncateWords` - Truncate at word boundary
- `Repeat` - Repeat string N times
- `Reverse` - Reverse string
- `PadCenter` - Center padding
- `RemoveAll` - Remove all occurrences
- `StripHtml` - Remove HTML tags
- `NormalizeWhitespace` - Collapse multiple spaces

### String Searching
- `CountOccurrences` - Count substring occurrences
- `FindAllPositions` - Find all positions of substring
- `StartsWithAny` - Check multiple prefixes
- `EndsWithAny` - Check multiple suffixes

### String Generation
- `RandomString` - Random string with custom charset
- `RandomHex` - Random hexadecimal string
- `RandomPassword` - Strong password generation
- `GenerateUuid` - UUID-like identifier
- `GenerateShortId` - Short unique ID

### String Encoding
- `Base64Encode` / `Base64Decode` - Base64 operations
- `UrlEncode` / `UrlDecode` - URL encoding/decoding

### String Similarity
- `LevenshteinDistance` - Calculate edit distance
- `SimilarityPercentage` - Calculate similarity percentage
- `HammingDistance` - Calculate Hamming distance

### String Formatting
- `FormatNumber` - Format with thousand separators
- `FormatCurrency` - Format as currency
- `FormatPercentage` - Format as percentage
- `FormatFileSize` - Format bytes as human-readable size

### String Parsing
- `ParseQueryString` - Parse URL query string
- `BuildQueryString` - Build URL query string

## Usage

```vb
Imports AllToolkit

' Case transformations
Dim camelCase = StringUtils.ToCamelCase("hello world")  ' "helloWorld"
Dim pascal = StringUtils.ToPascalCase("hello world")    ' "HelloWorld"
Dim snake = StringUtils.ToSnakeCase("HelloWorld")       ' "hello_world"

' Validation
If StringUtils.IsValidEmail("user@example.com") Then
    Console.WriteLine("Valid email")
End If

' String generation
Dim password = StringUtils.RandomPassword(16)
Dim uuid = StringUtils.GenerateUuid()
Dim shortId = StringUtils.GenerateShortId()

' Similarity
Dim distance = StringUtils.LevenshteinDistance("kitten", "sitting")
Dim similarity = StringUtils.SimilarityPercentage("abc", "abd")

' File size formatting
Dim size = StringUtils.FormatFileSize(1073741824)  ' "1.00 GB"
```

## Files

- `mod.vb` - Main module implementation
- `test.vb` - Unit tests (75+ tests)
- `examples.vb` - Usage examples

## Running Tests

Add test.vb to a test project and run:

```bash
dotnet test
```

## Running Examples

Add examples.vb to a console project and run:

```bash
dotnet run
```

## Zero Dependencies

Uses only .NET standard library:
- System
- System.Text
- System.Linq
- System.Globalization
- System.Text.RegularExpressions
- System.Collections.Generic