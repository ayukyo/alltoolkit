' =============================================================================
' AllToolkit - String Utilities for VB.NET
' =============================================================================
' A comprehensive string manipulation utility library for VB.NET applications.
' Zero dependencies - uses only .NET standard library.
'
' Features:
' - Case transformations (camelCase, PascalCase, snake_case, kebab-case)
' - String validation (email, URL, phone, credit card, etc.)
' - String manipulation (truncate, pad, reverse, repeat)
' - String searching (contains, count, find all positions)
' - String cleaning (trim, remove, strip HTML, normalize whitespace)
' - String generation (random, password, UUID-like)
' - String encoding (base64, URL encode/decode)
' - String similarity (Levenshtein distance, Hamming distance)
' - String formatting (number format, currency, percentage)
' =============================================================================

Imports System
Imports System.Text
Imports System.Linq
Imports System.Globalization
Imports System.Text.RegularExpressions
Imports System.Collections.Generic

Namespace AllToolkit

    ''' <summary>
    ''' Result of a string validation operation.
    ''' </summary>
    Public Class ValidationResult
        ''' <summary>Indicates whether the string is valid.</summary>
        Public ReadOnly Property IsValid As Boolean
        
        ''' <summary>Error message if validation failed.</summary>
        Public ReadOnly Property ErrorMessage As String
        
        ''' <summary>Validated and optionally normalized value.</summary>
        Public ReadOnly Property Value As String

        Public Sub New(isValid As Boolean, Optional value As String = "", Optional errorMessage As String = "")
            Me.IsValid = isValid
            Me.Value = value
            Me.ErrorMessage = errorMessage
        End Sub
    End Class

    ''' <summary>
    ''' Comprehensive string utilities for VB.NET.
    ''' </summary>
    Public Module StringUtils

        ' =========================================================================
        ' Constants
        ' =========================================================================
        
        ''' <summary>Letters a-z (lowercase).</summary>
        Public ReadOnly LowercaseLetters As String = "abcdefghijklmnopqrstuvwxyz"
        
        ''' <summary>Letters A-Z (uppercase).</summary>
        Public ReadOnly UppercaseLetters As String = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        ''' <summary>All letters (a-z, A-Z).</summary>
        Public ReadOnly AllLetters As String = LowercaseLetters & UppercaseLetters
        
        ''' <summary>Digits 0-9.</summary>
        Public ReadOnly Digits As String = "0123456789"
        
        ''' <summary>Alphanumeric characters.</summary>
        Public ReadOnly Alphanumeric As String = AllLetters & Digits
        
        ''' <summary>Hexadecimal characters.</summary>
        Public ReadOnly HexChars As String = "0123456789abcdefABCDEF"
        
        ''' <summary>Special characters for passwords.</summary>
        Public ReadOnly SpecialChars As String = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        ''' <summary>Random number generator (thread-safe via SyncLock).</summary>
        Private ReadOnly RandomGenerator As New Random()
        Private ReadOnly RandomLock As New Object()

        ' =========================================================================
        ' Case Transformations
        ' =========================================================================

        ''' <summary>
        ''' Converts a string to camelCase.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <param name="separator">Word separator (default: space, underscore, hyphen).</param>
        ''' <returns>camelCase string.</returns>
        Public Function ToCamelCase(input As String, Optional separator As Char() = Nothing) As String
            If String.IsNullOrEmpty(input) Then Return input
            
            Dim separators As Char() = If(separator, {" "c, "_"c, "-"c})
            Dim words As String() = input.Split(separators, StringSplitOptions.RemoveEmptyEntries)
            
            If words.Length = 0 Then Return String.Empty
            
            Dim sb As New StringBuilder()
            sb.Append(words(0).ToLower())
            
            For i As Integer = 1 To words.Length - 1
                If words(i).Length > 0 Then
                    sb.Append(Char.ToUpper(words(i)(0)))
                    sb.Append(words(i).Substring(1).ToLower())
                End If
            Next
            
            Return sb.ToString()
        End Function

        ''' <summary>
        ''' Converts a string to PascalCase.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <param name="separator">Word separator (default: space, underscore, hyphen).</param>
        ''' <returns>PascalCase string.</returns>
        Public Function ToPascalCase(input As String, Optional separator As Char() = Nothing) As String
            If String.IsNullOrEmpty(input) Then Return input
            
            Dim separators As Char() = If(separator, {" "c, "_"c, "-"c})
            Dim words As String() = input.Split(separators, StringSplitOptions.RemoveEmptyEntries)
            
            If words.Length = 0 Then Return String.Empty
            
            Dim sb As New StringBuilder()
            
            For Each word As String In words
                If word.Length > 0 Then
                    sb.Append(Char.ToUpper(word(0)))
                    sb.Append(word.Substring(1).ToLower())
                End If
            Next
            
            Return sb.ToString()
        End Function

        ''' <summary>
        ''' Converts a string to snake_case.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <returns>snake_case string.</returns>
        Public Function ToSnakeCase(input As String) As String
            If String.IsNullOrEmpty(input) Then Return input
            
            Dim sb As New StringBuilder()
            
            For i As Integer = 0 To input.Length - 1
                Dim c As Char = input(i)
                
                If Char.IsUpper(c) Then
                    If i > 0 Then sb.Append("_"c)
                    sb.Append(Char.ToLower(c))
                Else
                    sb.Append(c)
                End If
            Next
            
            Return sb.ToString()
        End Function

        ''' <summary>
        ''' Converts a string to kebab-case.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <returns>kebab-case string.</returns>
        Public Function ToKebabCase(input As String) As String
            If String.IsNullOrEmpty(input) Then Return input
            
            Dim sb As New StringBuilder()
            
            For i As Integer = 0 To input.Length - 1
                Dim c As Char = input(i)
                
                If Char.IsUpper(c) Then
                    If i > 0 Then sb.Append("-"c)
                    sb.Append(Char.ToLower(c))
                Else If c = "_"c Then
                    sb.Append("-"c)
                Else
                    sb.Append(c)
                End If
            Next
            
            Return sb.ToString()
        End Function

        ''' <summary>
        ''' Converts a string to Title Case.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <returns>Title Case string.</returns>
        Public Function ToTitleCase(input As String) As String
            If String.IsNullOrEmpty(input) Then Return input
            
            Dim ti As TextInfo = CultureInfo.CurrentCulture.TextInfo
            Return ti.ToTitleCase(input.ToLower())
        End Function

        ''' <summary>
        ''' Converts a string to Sentence case.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <returns>Sentence case string.</returns>
        Public Function ToSentenceCase(input As String) As String
            If String.IsNullOrEmpty(input) Then Return input
            
            Dim trimmed As String = input.Trim()
            If trimmed.Length = 0 Then Return String.Empty
            
            Return Char.ToUpper(trimmed(0)) & trimmed.Substring(1).ToLower()
        End Function

        ' =========================================================================
        ' String Validation
        ' =========================================================================

        ''' <summary>
        ''' Validates if string is a valid email address.
        ''' </summary>
        ''' <param name="email">Email string to validate.</param>
        ''' <returns>True if valid email.</returns>
        Public Function IsValidEmail(email As String) As Boolean
            If String.IsNullOrWhiteSpace(email) Then Return False
            
            Try
                Dim pattern As String = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                Return Regex.IsMatch(email, pattern)
            Catch
                Return False
            End Try
        End Function

        ''' <summary>
        ''' Validates if string is a valid URL.
        ''' </summary>
        ''' <param name="url">URL string to validate.</param>
        ''' <param name="requireHttps">Require HTTPS protocol.</param>
        ''' <returns>True if valid URL.</returns>
        Public Function IsValidUrl(url As String, Optional requireHttps As Boolean = False) As Boolean
            If String.IsNullOrWhiteSpace(url) Then Return False
            
            Try
                Dim uri As New Uri(url)
                If requireHttps Then Return uri.Scheme = Uri.UriSchemeHttps
                Return uri.Scheme = Uri.UriSchemeHttp OrElse uri.Scheme = Uri.UriSchemeHttps
            Catch
                Return False
            End Try
        End Function

        ''' <summary>
        ''' Validates if string is a valid phone number (international format).
        ''' </summary>
        ''' <param name="phone">Phone string to validate.</param>
        ''' <returns>True if valid phone number.</returns>
        Public Function IsValidPhone(phone As String) As Boolean
            If String.IsNullOrWhiteSpace(phone) Then Return False
            
            ' Remove common separators
            Dim cleaned As String = Regex.Replace(phone, "[\s\-\.\(\)]", "")
            
            ' International format: + followed by 7-15 digits
            Dim pattern As String = "^\+?[1-9]\d{6,14}$"
            Return Regex.IsMatch(cleaned, pattern)
        End Function

        ''' <summary>
        ''' Validates if string is a valid credit card number (Luhn algorithm).
        ''' </summary>
        ''' <param name="cardNumber">Card number string to validate.</param>
        ''' <returns>True if valid credit card number.</returns>
        Public Function IsValidCreditCard(cardNumber As String) As Boolean
            If String.IsNullOrWhiteSpace(cardNumber) Then Return False
            
            ' Remove spaces and dashes
            Dim cleaned As String = Regex.Replace(cardNumber, "[\s\-]", "")
            
            ' Must be 13-19 digits
            If Not Regex.IsMatch(cleaned, "^\d{13,19}$") Then Return False
            
            ' Luhn algorithm
            Dim sum As Integer = 0
            Dim alternate As Boolean = False
            
            For i As Integer = cleaned.Length - 1 To 0 Step -1
                Dim digit As Integer = Convert.ToInt32(cleaned(i).ToString())
                
                If alternate Then
                    digit *= 2
                    If digit > 9 Then digit -= 9
                End If
                
                sum += digit
                alternate = Not alternate
            Next
            
            Return sum Mod 10 = 0
        End Function

        ''' <summary>
        ''' Validates if string is a valid IPv4 address.
        ''' </summary>
        ''' <param name="ip">IP string to validate.</param>
        ''' <returns>True if valid IPv4.</returns>
        Public Function IsValidIPv4(ip As String) As Boolean
            If String.IsNullOrWhiteSpace(ip) Then Return False
            
            Dim parts As String() = ip.Split("."c)
            If parts.Length <> 4 Then Return False
            
            For Each part As String In parts
                Dim num As Integer
                If Not Integer.TryParse(part, num) Then Return False
                If num < 0 OrElse num > 255 Then Return False
                If part.Length > 1 AndAlso part.StartsWith("0") Then Return False
            Next
            
            Return True
        End Function

        ''' <summary>
        ''' Validates if string is a valid hex color code.
        ''' </summary>
        ''' <param name="color">Color string to validate.</param>
        ''' <returns>True if valid hex color.</returns>
        Public Function IsValidHexColor(color As String) As Boolean
            If String.IsNullOrWhiteSpace(color) Then Return False
            
            Dim pattern As String = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
            Return Regex.IsMatch(color, pattern)
        End Function

        ''' <summary>
        ''' Validates if string contains only alphanumeric characters.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <returns>True if alphanumeric only.</returns>
        Public Function IsAlphanumeric(input As String) As Boolean
            If String.IsNullOrEmpty(input) Then Return False
            Return input.All(Function(c) Char.IsLetterOrDigit(c))
        End Function

        ''' <summary>
        ''' Validates if string is a valid date.
        ''' </summary>
        ''' <param name="dateStr">Date string to validate.</param>
        ''' <param name="format">Expected date format (optional).</param>
        ''' <returns>True if valid date.</returns>
        Public Function IsValidDate(dateStr As String, Optional format As String = Nothing) As Boolean
            If String.IsNullOrWhiteSpace(dateStr) Then Return False
            
            If String.IsNullOrEmpty(format) Then
                Return DateTime.TryParse(dateStr, Nothing, DateTimeStyles.None, Nothing)
            Else
                Return DateTime.TryParseExact(dateStr, format, Nothing, DateTimeStyles.None, Nothing)
            End If
        End Function

        ' =========================================================================
        ' String Manipulation
        ' =========================================================================

        ''' <summary>
        ''' Truncates a string to specified length with optional suffix.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <param name="maxLength">Maximum length.</param>
        ''' <param name="suffix">Suffix to append if truncated (default: "…").</param>
        ''' <returns>Truncated string.</returns>
        Public Function Truncate(input As String, maxLength As Integer, Optional suffix As String = "…") As String
            If String.IsNullOrEmpty(input) OrElse input.Length <= maxLength Then Return input
            
            Dim suffixLength As Integer = suffix.Length
            If maxLength <= suffixLength Then Return suffix.Substring(0, maxLength)
            
            Return input.Substring(0, maxLength - suffixLength) & suffix
        End Function

        ''' <summary>
        ''' Truncates string at word boundary.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <param name="maxLength">Maximum length.</param>
        ''' <param name="suffix">Suffix to append if truncated.</param>
        ''' <returns>Truncated string at word boundary.</returns>
        Public Function TruncateWords(input As String, maxLength As Integer, Optional suffix As String = "…") As String
            If String.IsNullOrEmpty(input) OrElse input.Length <= maxLength Then Return input
            
            Dim truncated As String = input.Substring(0, maxLength)
            Dim lastSpace As Integer = truncated.LastIndexOf(" "c)
            
            If lastSpace > 0 Then
                truncated = truncated.Substring(0, lastSpace)
            End If
            
            Return truncated.Trim() & suffix
        End Function

        ''' <summary>
        ''' Repeats a string specified number of times.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <param name="count">Number of times to repeat.</param>
        ''' <returns>Repeated string.</returns>
        Public Function Repeat(input As String, count As Integer) As String
            If String.IsNullOrEmpty(input) OrElse count <= 0 Then Return String.Empty
            
            Dim sb As New StringBuilder(input.Length * count)
            For i As Integer = 1 To count
                sb.Append(input)
            Next
            
            Return sb.ToString()
        End Function

        ''' <summary>
        ''' Reverses a string.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <returns>Reversed string.</returns>
        Public Function Reverse(input As String) As String
            If String.IsNullOrEmpty(input) Then Return input
            
            Dim chars As Char() = input.ToCharArray()
            Array.Reverse(chars)
            Return New String(chars)
        End Function

        ''' <summary>
        ''' Pads both sides of string equally.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <param name="totalLength">Total length after padding.</param>
        ''' <param name="padChar">Padding character (default: space).</param>
        ''' <returns>Center-padded string.</returns>
        Public Function PadCenter(input As String, totalLength As Integer, Optional padChar As Char = " "c) As String
            If String.IsNullOrEmpty(input) Then Return Repeat(padChar.ToString(), totalLength)
            If input.Length >= totalLength Then Return input
            
            Dim padLength As Integer = totalLength - input.Length
            Dim padLeft As Integer = padLength \ 2
            Dim padRight As Integer = padLength - padLeft
            
            Return Repeat(padChar.ToString(), padLeft) & input & Repeat(padChar.ToString(), padRight)
        End Function

        ''' <summary>
        ''' Removes all occurrences of a substring.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <param name="remove">Substring to remove.</param>
        ''' <param name="comparison">String comparison type.</param>
        ''' <returns>String with all occurrences removed.</returns>
        Public Function RemoveAll(input As String, remove As String, Optional comparison As StringComparison = StringComparison.Ordinal) As String
            If String.IsNullOrEmpty(input) OrElse String.IsNullOrEmpty(remove) Then Return input
            
            Dim sb As New StringBuilder()
            Dim currentIndex As Integer = 0
            
            While currentIndex < input.Length
                Dim foundIndex As Integer = input.IndexOf(remove, currentIndex, comparison)
                
                If foundIndex < 0 Then
                    sb.Append(input.Substring(currentIndex))
                    Exit While
                End If
                
                sb.Append(input.Substring(currentIndex, foundIndex - currentIndex))
                currentIndex = foundIndex + remove.Length
            End While
            
            Return sb.ToString()
        End Function

        ''' <summary>
        ''' Strips HTML tags from string.
        ''' </summary>
        ''' <param name="html">HTML string.</param>
        ''' <returns>Plain text without HTML tags.</returns>
        Public Function StripHtml(html As String) As String
            If String.IsNullOrEmpty(html) Then Return html
            
            ' Remove HTML tags
            Dim result As String = Regex.Replace(html, "<[^>]*>", String.Empty)
            
            ' Decode common HTML entities
            result = result.Replace("&amp;", "&")
            result = result.Replace("&lt;", "<")
            result = result.Replace("&gt;", ">")
            result = result.Replace("&nbsp;", " ")
            result = result.Replace("&quot;", """")
            result = result.Replace("&#39;", "'")
            
            Return result
        End Function

        ''' <summary>
        ''' Normalizes whitespace (collapses multiple spaces, trims).
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <returns>Whitespace-normalized string.</returns>
        Public Function NormalizeWhitespace(input As String) As String
            If String.IsNullOrEmpty(input) Then Return input
            
            ' Replace all whitespace sequences with single space
            Dim result As String = Regex.Replace(input, "\s+", " ")
            Return result.Trim()
        End Function

        ' =========================================================================
        ' String Searching
        ' =========================================================================

        ''' <summary>
        ''' Counts occurrences of a substring.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <param name="search">Substring to count.</param>
        ''' <param name="comparison">String comparison type.</param>
        ''' <returns>Number of occurrences.</returns>
        Public Function CountOccurrences(input As String, search As String, Optional comparison As StringComparison = StringComparison.Ordinal) As Integer
            If String.IsNullOrEmpty(input) OrElse String.IsNullOrEmpty(search) Then Return 0
            
            Dim count As Integer = 0
            Dim index As Integer = 0
            
            While index < input.Length
                Dim foundIndex As Integer = input.IndexOf(search, index, comparison)
                If foundIndex < 0 Then Exit While
                
                count += 1
                index = foundIndex + search.Length
            End While
            
            Return count
        End Function

        ''' <summary>
        ''' Finds all positions of a substring.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <param name="search">Substring to find.</param>
        ''' <param name="comparison">String comparison type.</param>
        ''' <returns>List of all positions.</returns>
        Public Function FindAllPositions(input As String, search As String, Optional comparison As StringComparison = StringComparison.Ordinal) As List(Of Integer)
            Dim positions As New List(Of Integer)()
            
            If String.IsNullOrEmpty(input) OrElse String.IsNullOrEmpty(search) Then Return positions
            
            Dim index As Integer = 0
            
            While index < input.Length
                Dim foundIndex As Integer = input.IndexOf(search, index, comparison)
                If foundIndex < 0 Then Exit While
                
                positions.Add(foundIndex)
                index = foundIndex + 1
            End While
            
            Return positions
        End Function

        ''' <summary>
        ''' Checks if string starts with any of the prefixes.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <param name="prefixes">Prefixes to check.</param>
        ''' <returns>True if starts with any prefix.</returns>
        Public Function StartsWithAny(input As String, ParamArray prefixes As String()) As Boolean
            If String.IsNullOrEmpty(input) Then Return False
            
            For Each prefix As String In prefixes
                If Not String.IsNullOrEmpty(prefix) AndAlso input.StartsWith(prefix) Then
                    Return True
                End If
            Next
            
            Return False
        End Function

        ''' <summary>
        ''' Checks if string ends with any of the suffixes.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <param name="suffixes">Suffixes to check.</param>
        ''' <returns>True if ends with any suffix.</returns>
        Public Function EndsWithAny(input As String, ParamArray suffixes As String()) As Boolean
            If String.IsNullOrEmpty(input) Then Return False
            
            For Each suffix As String In suffixes
                If Not String.IsNullOrEmpty(suffix) AndAlso input.EndsWith(suffix) Then
                    Return True
                End If
            Next
            
            Return False
        End Function

        ' =========================================================================
        ' String Generation
        ' =========================================================================

        ''' <summary>
        ''' Generates a random string of specified length.
        ''' </summary>
        ''' <param name="length">Length of string to generate.</param>
        ''' <param name="chars">Characters to use (default: alphanumeric).</param>
        ''' <returns>Random string.</returns>
        Public Function RandomString(length As Integer, Optional chars As String = Nothing) As String
            If length <= 0 Then Return String.Empty
            
            Dim charSet As String = If(chars, Alphanumeric)
            
            SyncLock RandomLock
                Dim sb As New StringBuilder(length)
                For i As Integer = 1 To length
                    sb.Append(charSet(RandomGenerator.Next(charSet.Length)))
                Next
                Return sb.ToString()
            End SyncLock
        End Function

        ''' <summary>
        ''' Generates a random hexadecimal string.
        ''' </summary>
        ''' <param name="length">Length of string to generate.</param>
        ''' <returns>Random hex string (lowercase).</returns>
        Public Function RandomHex(length As Integer) As String
            Return RandomString(length, "0123456789abcdef")
        End Function

        ''' <summary>
        ''' Generates a strong random password.
        ''' </summary>
        ''' <param name="length">Password length (default: 16, min: 8).</param>
        ''' <param name="includeSpecial">Include special characters.</param>
        ''' <returns>Strong random password.</returns>
        Public Function RandomPassword(Optional length As Integer = 16, Optional includeSpecial As Boolean = True) As String
            If length < 8 Then length = 8
            
            Dim allChars As String = AllLetters & Digits
            If includeSpecial Then allChars &= SpecialChars
            
            Dim passwordChars As Char() = New Char(length - 1) {}
            
            SyncLock RandomLock
                ' Ensure at least one of each required type
                passwordChars(0) = LowercaseLetters(RandomGenerator.Next(LowercaseLetters.Length))
                passwordChars(1) = UppercaseLetters(RandomGenerator.Next(UppercaseLetters.Length))
                passwordChars(2) = Digits(RandomGenerator.Next(Digits.Length))
                
                If includeSpecial Then
                    passwordChars(3) = SpecialChars(RandomGenerator.Next(SpecialChars.Length))
                    
                    ' Fill remaining
                    For i As Integer = 4 To length - 1
                        passwordChars(i) = allChars(RandomGenerator.Next(allChars.Length))
                    Next
                Else
                    ' Fill remaining
                    For i As Integer = 3 To length - 1
                        passwordChars(i) = allChars(RandomGenerator.Next(allChars.Length))
                    Next
                End If
                
                ' Shuffle the password
                For i As Integer = 0 To passwordChars.Length - 2
                    Dim j As Integer = RandomGenerator.Next(i, passwordChars.Length)
                    Dim temp As Char = passwordChars(i)
                    passwordChars(i) = passwordChars(j)
                    passwordChars(j) = temp
                Next
            End SyncLock
            
            Return New String(passwordChars)
        End Function

        ''' <summary>
        ''' Generates a UUID-like identifier (without external dependencies).
        ''' </summary>
        ''' <returns>UUID-like string (format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx).</returns>
        Public Function GenerateUuid() As String
            SyncLock RandomLock
                Dim bytes As Byte() = New Byte(15) {}
                RandomGenerator.NextBytes(bytes)
                
                ' Set version (4) and variant bits
                bytes(6) = CByte((bytes(6) And &HF) Or &H40)  ' Version 4
                bytes(8) = CByte((bytes(8) And &H3F) Or &H80) ' Variant 1
                
                Return String.Format("{0:x2}{1:x2}{2:x2}{3:x2}-{4:x2}{5:x2}-{6:x2}{7:x2}-{8:x2}{9:x2}-{10:x2}{11:x2}{12:x2}{13:x2}{14:x2}{15:x2}",
                    bytes(0), bytes(1), bytes(2), bytes(3),
                    bytes(4), bytes(5),
                    bytes(6), bytes(7),
                    bytes(8), bytes(9),
                    bytes(10), bytes(11), bytes(12), bytes(13), bytes(14), bytes(15))
            End SyncLock
        End Function

        ''' <summary>
        ''' Generates a short unique ID (8 characters).
        ''' </summary>
        ''' <returns>Short unique ID.</returns>
        Public Function GenerateShortId() As String
            Return RandomString(8, "abcdefghijklmnopqrstuvwxyz0123456789")
        End Function

        ' =========================================================================
        ' String Encoding
        ' =========================================================================

        ''' <summary>
        ''' Encodes string to Base64.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <param name="encoding">Text encoding (default: UTF-8).</param>
        ''' <returns>Base64 encoded string.</returns>
        Public Function Base64Encode(input As String, Optional encoding As Encoding = Nothing) As String
            If String.IsNullOrEmpty(input) Then Return String.Empty
            
            Dim enc As Encoding = If(encoding, Encoding.UTF8)
            Dim bytes As Byte() = enc.GetBytes(input)
            Return Convert.ToBase64String(bytes)
        End Function

        ''' <summary>
        ''' Decodes Base64 string.
        ''' </summary>
        ''' <param name="base64">Base64 string to decode.</param>
        ''' <param name="encoding">Text encoding (default: UTF-8).</param>
        ''' <returns>Decoded string.</returns>
        Public Function Base64Decode(base64 As String, Optional encoding As Encoding = Nothing) As String
            If String.IsNullOrEmpty(base64) Then Return String.Empty
            
            Try
                Dim bytes As Byte() = Convert.FromBase64String(base64)
                Dim enc As Encoding = If(encoding, Encoding.UTF8)
                Return enc.GetString(bytes)
            Catch
                Return String.Empty
            End Try
        End Function

        ''' <summary>
        ''' URL encodes a string.
        ''' </summary>
        ''' <param name="input">Input string.</param>
        ''' <returns>URL encoded string.</returns>
        Public Function UrlEncode(input As String) As String
            If String.IsNullOrEmpty(input) Then Return String.Empty
            Return Uri.EscapeDataString(input)
        End Function

        ''' <summary>
        ''' URL decodes a string.
        ''' </summary>
        ''' <param name="encoded">URL encoded string.</param>
        ''' <returns>Decoded string.</returns>
        Public Function UrlDecode(encoded As String) As String
            If String.IsNullOrEmpty(encoded) Then Return String.Empty
            Return Uri.UnescapeDataString(encoded)
        End Function

        ' =========================================================================
        ' String Similarity
        ' =========================================================================

        ''' <summary>
        ''' Calculates Levenshtein distance between two strings.
        ''' </summary>
        ''' <param name="s1">First string.</param>
        ''' <param name="s2">Second string.</param>
        ''' <returns>Number of edits needed to transform s1 into s2.</returns>
        Public Function LevenshteinDistance(s1 As String, s2 As String) As Integer
            If String.IsNullOrEmpty(s1) Then Return If(s2, "").Length
            If String.IsNullOrEmpty(s2) Then Return s1.Length
            
            Dim len1 As Integer = s1.Length
            Dim len2 As Integer = s2.Length
            
            Dim matrix As Integer(,) = New Integer(len1, len2) {}
            
            ' Initialize first row and column
            For i As Integer = 0 To len1
                matrix(i, 0) = i
            Next
            
            For j As Integer = 0 To len2
                matrix(0, j) = j
            Next
            
            ' Fill the matrix
            For i As Integer = 1 To len1
                For j As Integer = 1 To len2
                    Dim cost As Integer = If(s1(i - 1) = s2(j - 1), 0, 1)
                    matrix(i, j) = Math.Min(
                        Math.Min(matrix(i - 1, j) + 1, matrix(i, j - 1) + 1),
                        matrix(i - 1, j - 1) + cost
                    )
                Next
            Next
            
            Return matrix(len1, len2)
        End Function

        ''' <summary>
        ''' Calculates similarity percentage between two strings.
        ''' </summary>
        ''' <param name="s1">First string.</param>
        ''' <param name="s2">Second string.</param>
        ''' <returns>Similarity percentage (0-100).</returns>
        Public Function SimilarityPercentage(s1 As String, s2 As String) As Double
            If String.IsNullOrEmpty(s1) AndAlso String.IsNullOrEmpty(s2) Then Return 100.0
            If String.IsNullOrEmpty(s1) OrElse String.IsNullOrEmpty(s2) Then Return 0.0
            
            Dim maxLen As Integer = Math.Max(s1.Length, s2.Length)
            Dim distance As Integer = LevenshteinDistance(s1, s2)
            
            Return (1.0 - CDbl(distance) / CDbl(maxLen)) * 100.0
        End Function

        ''' <summary>
        ''' Calculates Hamming distance between two strings.
        ''' </summary>
        ''' <param name="s1">First string.</param>
        ''' <param name="s2">Second string.</param>
        ''' <returns>Number of differing positions.</returns>
        ''' <exception cref="ArgumentException">Thrown if strings have different lengths.</exception>
        Public Function HammingDistance(s1 As String, s2 As String) As Integer
            If String.IsNullOrEmpty(s1) AndAlso String.IsNullOrEmpty(s2) Then Return 0
            If s1?.Length <> s2?.Length Then
                Throw New ArgumentException("Strings must have equal length")
            End If
            
            Dim distance As Integer = 0
            For i As Integer = 0 To s1.Length - 1
                If s1(i) <> s2(i) Then distance += 1
            Next
            
            Return distance
        End Function

        ' =========================================================================
        ' String Formatting
        ' =========================================================================

        ''' <summary>
        ''' Formats a number with thousand separators.
        ''' </summary>
        ''' <param name="number">Number to format.</param>
        ''' <param name="decimalPlaces">Number of decimal places.</param>
        ''' <returns>Formatted number string.</returns>
        Public Function FormatNumber(number As Double, Optional decimalPlaces As Integer = 0) As String
            Return number.ToString("N" & decimalPlaces, CultureInfo.CurrentCulture)
        End Function

        ''' <summary>
        ''' Formats a number as currency.
        ''' </summary>
        ''' <param name="amount">Amount to format.</param>
        ''' <param name="currencySymbol">Currency symbol (default: $).</param>
        ''' <returns>Formatted currency string.</returns>
        Public Function FormatCurrency(amount As Double, Optional currencySymbol As String = "$") As String
            Return currencySymbol & amount.ToString("N2", CultureInfo.CurrentCulture)
        End Function

        ''' <summary>
        ''' Formats a number as percentage.
        ''' </summary>
        ''' <param name="value">Value to format (0-100).</param>
        ''' <param name="decimalPlaces">Number of decimal places.</param>
        ''' <returns>Formatted percentage string.</returns>
        Public Function FormatPercentage(value As Double, Optional decimalPlaces As Integer = 0) As String
            Return value.ToString("F" & decimalPlaces, CultureInfo.CurrentCulture) & "%"
        End Function

        ''' <summary>
        ''' Formats bytes as human-readable file size.
        ''' </summary>
        ''' <param name="bytes">Size in bytes.</param>
        ''' <param name="decimalPlaces">Number of decimal places.</param>
        ''' <returns>Human-readable file size.</returns>
        Public Function FormatFileSize(bytes As Long, Optional decimalPlaces As Integer = 2) As String
            Dim units As String() = {"B", "KB", "MB", "GB", "TB", "PB"}
            Dim size As Double = bytes
            Dim unitIndex As Integer = 0
            
            While size >= 1024 AndAlso unitIndex < units.Length - 1
                size /= 1024
                unitIndex += 1
            End While
            
            Return size.ToString("F" & decimalPlaces, CultureInfo.InvariantCulture) & " " & units(unitIndex)
        End Function

        ' =========================================================================
        ' String Parsing
        ' =========================================================================

        ''' <summary>
        ''' Parses a query string into a dictionary.
        ''' </summary>
        ''' <param name="queryString">Query string (with or without leading ?).</param>
        ''' <returns>Dictionary of key-value pairs.</returns>
        Public Function ParseQueryString(queryString As String) As Dictionary(Of String, String)
            Dim result As New Dictionary(Of String, String)(StringComparer.OrdinalIgnoreCase)
            
            If String.IsNullOrWhiteSpace(queryString) Then Return result
            
            ' Remove leading ?
            If queryString.StartsWith("?"c) Then
                queryString = queryString.Substring(1)
            End If
            
            Dim pairs As String() = queryString.Split("&"c)
            
            For Each pair As String In pairs
                Dim keyValue As String() = pair.Split({"="c}, 2)
                
                If keyValue.Length = 2 Then
                    Dim key As String = UrlDecode(keyValue(0))
                    Dim value As String = UrlDecode(keyValue(1))
                    result(key) = value
                ElseIf keyValue.Length = 1 AndAlso keyValue(0).Length > 0 Then
                    result(UrlDecode(keyValue(0))) = String.Empty
                End If
            Next
            
            Return result
        End Function

        ''' <summary>
        ''' Builds a query string from a dictionary.
        ''' </summary>
        ''' <param name="parameters">Key-value pairs.</param>
        ''' <returns>Query string (without leading ?).</returns>
        Public Function BuildQueryString(parameters As Dictionary(Of String, String)) As String
            If parameters Is Nothing OrElse parameters.Count = 0 Then Return String.Empty
            
            Dim pairs As New List(Of String)()
            
            For Each kvp As KeyValuePair(Of String, String) In parameters
                If Not String.IsNullOrEmpty(kvp.Key) Then
                    pairs.Add(UrlEncode(kvp.Key) & "=" & UrlEncode(If(kvp.Value, "")))
                End If
            Next
            
            Return String.Join("&", pairs)
        End Function

    End Module

End Namespace