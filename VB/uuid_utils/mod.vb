' =============================================================================
' AllToolkit - UUID Utilities for VB.NET
' =============================================================================
' A comprehensive UUID (Universally Unique Identifier) utility library.
' Zero dependencies - uses only .NET standard library.
'
' Features:
' - UUID Generation (v1 time-based, v3 name-based MD5, v4 random, v5 name-based SHA-1)
' - UUID Validation and Parsing
' - UUID Formatting (standard, compact, base64, etc.)
' - UUID Comparison and Sorting
' - UUID Component Extraction (timestamp, version, variant)
' - UUID Namespace Support (DNS, URL, OID, X500)
' =============================================================================

Imports System
Imports System.Text
Imports System.Security.Cryptography
Imports System.Collections.Generic

Namespace AllToolkit

    ''' <summary>
    ''' UUID version numbers.
    ''' </summary>
    Public Enum UuidVersion
        ''' <summary>Unknown or invalid version.</summary>
        Unknown = 0
        ''' <summary>Time-based UUID.</summary>
        Version1 = 1
        ''' <summary>DCE Security UUID.</summary>
        Version2 = 2
        ''' <summary>Name-based MD5 UUID.</summary>
        Version3 = 3
        ''' <summary>Random UUID.</summary>
        Version4 = 4
        ''' <summary>Name-based SHA-1 UUID.</summary>
        Version5 = 5
    End Enum

    ''' <summary>
    ''' UUID variant types.
    ''' </summary>
    Public Enum UuidVariant
        ''' <summary>Invalid variant.</summary>
        Invalid = 0
        ''' <summary>NCS backward compatibility variant.</summary>
        NCS = 1
        ''' <summary>RFC 4122 variant (standard).</summary>
        RFC4122 = 2
        ''' <summary>Microsoft Corporation variant.</summary>
        Microsoft = 3
        ''' <summary>Reserved for future use.</summary>
        Reserved = 4
    End Enum

    ''' <summary>
    ''' Predefined UUID namespaces for v3 and v5 UUIDs.
    ''' </summary>
    Public Module UuidNamespaces
        ''' <summary>DNS namespace.</summary>
        Public ReadOnly DNS As Guid = New Guid("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
        
        ''' <summary>URL namespace.</summary>
        Public ReadOnly URL As Guid = New Guid("6ba7b811-9dad-11d1-80b4-00c04fd430c8")
        
        ''' <summary>OID namespace.</summary>
        Public ReadOnly OID As Guid = New Guid("6ba7b812-9dad-11d1-80b4-00c04fd430c8")
        
        ''' <summary>X.500 DN namespace.</summary>
        Public ReadOnly X500 As Guid = New Guid("6ba7b814-9dad-11d1-80b4-00c04fd430c8")
        
        ''' <summary>Null/empty namespace.</summary>
        Public ReadOnly [Nil] As Guid = Guid.Empty
    End Module

    ''' <summary>
    ''' Result of UUID validation.
    ''' </summary>
    Public Class UuidValidationResult
        ''' <summary>Whether the UUID is valid.</summary>
        Public ReadOnly Property IsValid As Boolean
        
        ''' <summary>Error message if invalid.</summary>
        Public ReadOnly Property ErrorMessage As String
        
        ''' <summary>Parsed Guid if valid.</summary>
        Public ReadOnly Property Value As Guid

        Public Sub New(isValid As Boolean, Optional value As Guid = Nothing, Optional errorMessage As String = "")
            Me.IsValid = isValid
            Me.Value = value
            Me.ErrorMessage = errorMessage
        End Sub
    End Class

    ''' <summary>
    ''' Comprehensive UUID utilities for VB.NET.
    ''' </summary>
    Public Module UuidUtils

        ' =========================================================================
        ' Constants
        ' =========================================================================
        
        Private Const HexChars As String = "0123456789abcdef"
        Private Shared ReadOnly RandomGenerator As New Random()
        Private Shared ReadOnly RandomLock As New Object()

        ' =========================================================================
        ' UUID Generation
        ' =========================================================================

        ''' <summary>
        ''' Generates a random UUID (version 4).
        ''' This is the most commonly used UUID generation method.
        ''' </summary>
        ''' <returns>A random UUID.</returns>
        Public Function NewUuid() As Guid
            Return Guid.NewGuid()
        End Function

        ''' <summary>
        ''' Generates a random UUID (version 4) - alias for NewUuid.
        ''' </summary>
        ''' <returns>A random UUID.</returns>
        Public Function NewV4() As Guid
            Return Guid.NewGuid()
        End Function

        ''' <summary>
        ''' Generates a custom random UUID with more control.
        ''' Uses cryptographic random for better security.
        ''' </summary>
        ''' <returns>A cryptographically random UUID.</returns>
        Public Function NewSecureUuid() As Guid
            Dim bytes(15) As Byte
            Using rng As RandomNumberGenerator = RandomNumberGenerator.Create()
                rng.GetBytes(bytes)
            End Using
            
            ' Set version (4) and variant bits
            bytes(6) = CByte((bytes(6) And &HF) Or &H40)  ' Version 4
            bytes(8) = CByte((bytes(8) And &H3F) Or &H80) ' Variant 1
            
            Return New Guid(bytes)
        End Function

        ''' <summary>
        ''' Generates a time-based UUID (version 1).
        ''' Note: This is a simplified implementation without MAC address.
        ''' Uses random node ID instead of actual MAC for privacy.
        ''' </summary>
        ''' <returns>A time-based UUID.</returns>
        Public Function NewV1() As Guid
            ' Get current timestamp (100-nanosecond intervals since Oct 15, 1582)
            Dim timestamp As Long = GetGregorianTimestamp()
            
            ' Add UUID epoch offset (Oct 15, 1582 to Jan 1, 1970)
            ' This is handled in GetGregorianTimestamp
            
            Dim bytes(15) As Byte
            
            ' Time low (4 bytes, little-endian for Guid)
            bytes(0) = CByte(timestamp And &HFF)
            bytes(1) = CByte((timestamp >> 8) And &HFF)
            bytes(2) = CByte((timestamp >> 16) And &HFF)
            bytes(3) = CByte((timestamp >> 24) And &HFF)
            
            ' Time mid (2 bytes)
            bytes(4) = CByte((timestamp >> 32) And &HFF)
            bytes(5) = CByte((timestamp >> 40) And &HFF)
            
            ' Time hi and version (2 bytes, version 1)
            Dim timeHi As UShort = CUShort((timestamp >> 48) And &H0FFF)
            bytes(6) = CByte((timeHi >> 8) And &HFF)
            bytes(7) = CByte(timeHi And &HFF)
            
            ' Set version to 1
            bytes(6) = CByte(bytes(6) Or &H10)
            
            ' Clock sequence (random, with variant)
            SyncLock RandomLock
                bytes(8) = CByte(RandomGenerator.Next(256) And &H3F Or &H80)
                bytes(9) = CByte(RandomGenerator.Next(256))
            End SyncLock
            
            ' Node ID (random for privacy)
            SyncLock RandomLock
                RandomGenerator.NextBytes(New Byte(5) {})
                bytes(10) = CByte(RandomGenerator.Next(256) Or &H01) ' Set multicast bit
                bytes(11) = CByte(RandomGenerator.Next(256))
                bytes(12) = CByte(RandomGenerator.Next(256))
                bytes(13) = CByte(RandomGenerator.Next(256))
                bytes(14) = CByte(RandomGenerator.Next(256))
                bytes(15) = CByte(RandomGenerator.Next(256))
            End SyncLock
            
            Return New Guid(bytes)
        End Function

        ''' <summary>
        ''' Generates a name-based UUID using MD5 hash (version 3).
        ''' </summary>
        ''' <param name="namespace">The namespace UUID.</param>
        ''' <param name="name">The name string.</param>
        ''' <returns>A name-based UUID v3.</returns>
        Public Function NewV3([namespace] As Guid, name As String) As Guid
            Return NewNameBasedUuid([namespace], name, useSha1:=False)
        End Function

        ''' <summary>
        ''' Generates a name-based UUID using SHA-1 hash (version 5).
        ''' </summary>
        ''' <param name="namespace">The namespace UUID.</param>
        ''' <param name="name">The name string.</param>
        ''' <returns>A name-based UUID v5.</returns>
        Public Function NewV5([namespace] As Guid, name As String) As Guid
            Return NewNameBasedUuid([namespace], name, useSha1:=True)
        End Function

        ''' <summary>
        ''' Internal method for generating name-based UUIDs.
        ''' </summary>
        Private Function NewNameBasedUuid([namespace] As Guid, name As String, useSha1 As Boolean) As Guid
            If String.IsNullOrEmpty(name) Then
                Throw New ArgumentException("Name cannot be null or empty", NameOf(name))
            End If
            
            ' Convert namespace to bytes (big-endian for hashing)
            Dim namespaceBytes As Byte() = [namespace].ToByteArray()
            SwapByteOrder(namespaceBytes)
            
            ' Convert name to bytes
            Dim nameBytes As Byte() = Encoding.UTF8.GetBytes(name)
            
            ' Combine namespace + name
            Dim combinedBytes As Byte() = New Byte(namespaceBytes.Length + nameBytes.Length - 1) {}
            Buffer.BlockCopy(namespaceBytes, 0, combinedBytes, 0, namespaceBytes.Length)
            Buffer.BlockCopy(nameBytes, 0, combinedBytes, namespaceBytes.Length, nameBytes.Length)
            
            ' Hash
            Dim hash As Byte()
            If useSha1 Then
                Using sha1 As SHA1 = SHA1.Create()
                    hash = sha1.ComputeHash(combinedBytes)
                End Using
            Else
                Using md5 As MD5 = MD5.Create()
                    hash = md5.ComputeHash(combinedBytes)
                End Using
            End If
            
            ' Create UUID from first 16 bytes of hash
            Dim uuidBytes(15) As Byte
            Buffer.BlockCopy(hash, 0, uuidBytes, 0, 16)
            
            ' Set version (3 for MD5, 5 for SHA-1)
            uuidBytes(6) = CByte((uuidBytes(6) And &H0F) Or (If(useSha1, &H50, &H30)))
            
            ' Set variant to RFC 4122
            uuidBytes(8) = CByte((uuidBytes(8) And &H3F) Or &H80)
            
            Return New Guid(uuidBytes)
        End Function

        ''' <summary>
        ''' Swaps byte order for Guid conversion (little-endian to big-endian for certain parts).
        ''' </summary>
        Private Sub SwapByteOrder(bytes As Byte())
            ' Swap first 4 bytes (int32)
            Dim temp As Byte = bytes(0)
            bytes(0) = bytes(3)
            bytes(3) = temp
            temp = bytes(1)
            bytes(1) = bytes(2)
            bytes(2) = temp
            
            ' Swap next 2 bytes (int16)
            temp = bytes(4)
            bytes(4) = bytes(5)
            bytes(5) = temp
            
            ' Swap next 2 bytes (int16)
            temp = bytes(6)
            bytes(6) = bytes(7)
            bytes(7) = temp
        End Sub

        ''' <summary>
        ''' Gets current timestamp in Gregorian format (100-ns intervals since Oct 15, 1582).
        ''' </summary>
        Private Function GetGregorianTimestamp() As Long
            ' UUID epoch: October 15, 1582
            Dim uuidEpoch As New DateTime(1582, 10, 15, 0, 0, 0, DateTimeKind.Utc)
            Dim now As DateTime = DateTime.UtcNow
            Dim ticks As Long = now.Ticks - uuidEpoch.Ticks
            Return ticks
        End Function

        ' =========================================================================
        ' UUID Validation
        ' =========================================================================

        ''' <summary>
        ''' Validates if a string is a valid UUID.
        ''' </summary>
        ''' <param name="uuidString">String to validate.</param>
        ''' <returns>True if valid UUID format.</returns>
        Public Function IsValidUuid(uuidString As String) As Boolean
            Return Guid.TryParse(uuidString, Nothing)
        End Function

        ''' <summary>
        ''' Validates a UUID string with detailed result.
        ''' </summary>
        ''' <param name="uuidString">String to validate.</param>
        ''' <returns>Validation result with details.</returns>
        Public Function ValidateUuid(uuidString As String) As UuidValidationResult
            If String.IsNullOrWhiteSpace(uuidString) Then
                Return New UuidValidationResult(False, Guid.Empty, "UUID string is null or empty")
            End If
            
            Dim parsed As Guid
            If Guid.TryParse(uuidString, parsed) Then
                Return New UuidValidationResult(True, parsed, "")
            Else
                Return New UuidValidationResult(False, Guid.Empty, "Invalid UUID format")
            End If
        End Function

        ''' <summary>
        ''' Checks if a UUID is the nil/empty UUID.
        ''' </summary>
        ''' <param name="uuid">UUID to check.</param>
        ''' <returns>True if nil UUID.</returns>
        Public Function IsNilUuid(uuid As Guid) As Boolean
            Return uuid = Guid.Empty
        End Function

        ' =========================================================================
        ' UUID Parsing
        ' =========================================================================

        ''' <summary>
        ''' Parses a UUID string to Guid.
        ''' </summary>
        ''' <param name="uuidString">UUID string to parse.</param>
        ''' <returns>Parsed Guid.</returns>
        ''' <exception cref="FormatException">Thrown if string is not valid UUID.</exception>
        Public Function ParseUuid(uuidString As String) As Guid
            If String.IsNullOrWhiteSpace(uuidString) Then
                Throw New ArgumentException("UUID string cannot be null or empty", NameOf(uuidString))
            End If
            
            Return Guid.Parse(uuidString)
        End Function

        ''' <summary>
        ''' Tries to parse a UUID string to Guid.
        ''' </summary>
        ''' <param name="uuidString">UUID string to parse.</param>
        ''' <param name="result">Parsed Guid if successful.</param>
        ''' <returns>True if parsing succeeded.</returns>
        Public Function TryParseUuid(uuidString As String, ByRef result As Guid) As Boolean
            Return Guid.TryParse(uuidString, result)
        End Function

        ''' <summary>
        ''' Parses a compact UUID (without dashes) to Guid.
        ''' </summary>
        ''' <param name="compactUuid">Compact UUID string (32 hex chars).</param>
        ''' <returns>Parsed Guid.</returns>
        Public Function ParseCompactUuid(compactUuid As String) As Guid
            If String.IsNullOrWhiteSpace(compactUuid) Then
                Throw New ArgumentException("Compact UUID cannot be null or empty", NameOf(compactUuid))
            End If
            
            If compactUuid.Length <> 32 Then
                Throw New FormatException("Compact UUID must be 32 hex characters")
            End If
            
            ' Insert dashes at correct positions
            Dim formatted As String = String.Format("{0}-{1}-{2}-{3}-{4}",
                compactUuid.Substring(0, 8),
                compactUuid.Substring(8, 4),
                compactUuid.Substring(12, 4),
                compactUuid.Substring(16, 4),
                compactUuid.Substring(20, 12))
            
            Return Guid.Parse(formatted)
        End Function

        ' =========================================================================
        ' UUID Formatting
        ' =========================================================================

        ''' <summary>
        ''' Formats UUID as standard string (lowercase, with dashes).
        ''' </summary>
        ''' <param name="uuid">UUID to format.</param>
        ''' <returns>Standard UUID string (e.g., "550e8400-e29b-41d4-a716-446655440000").</returns>
        Public Function Format(uuid As Guid) As String
            Return uuid.ToString("D").ToLowerInvariant()
        End Function

        ''' <summary>
        ''' Formats UUID as uppercase string with dashes.
        ''' </summary>
        ''' <param name="uuid">UUID to format.</param>
        ''' <returns>Uppercase UUID string.</returns>
        Public Function FormatUpper(uuid As Guid) As String
            Return uuid.ToString("D").ToUpperInvariant()
        End Function

        ''' <summary>
        ''' Formats UUID as compact string (no dashes, lowercase).
        ''' </summary>
        ''' <param name="uuid">UUID to format.</param>
        ''' <returns>Compact UUID string (32 hex chars).</returns>
        Public Function FormatCompact(uuid As Guid) As String
            Return uuid.ToString("N").ToLowerInvariant()
        End Function

        ''' <summary>
        ''' Formats UUID as compact uppercase string (no dashes).
        ''' </summary>
        ''' <param name="uuid">UUID to format.</param>
        ''' <returns>Compact uppercase UUID string.</returns>
        Public Function FormatCompactUpper(uuid As Guid) As String
            Return uuid.ToString("N").ToUpperInvariant()
        End Function

        ''' <summary>
        ''' Formats UUID as Base64 string (22 characters, no padding).
        ''' </summary>
        ''' <param name="uuid">UUID to format.</param>
        ''' <returns>Base64-encoded UUID (22 chars).</returns>
        Public Function FormatBase64(uuid As Guid) As String
            Dim bytes As Byte() = uuid.ToByteArray()
            Return Convert.ToBase64String(bytes).TrimEnd("="c).Replace("+", "-").Replace("/", "_")
        End Function

        ''' <summary>
        ''' Parses a Base64-encoded UUID back to Guid.
        ''' </summary>
        ''' <param name="base64Uuid">Base64-encoded UUID string.</param>
        ''' <returns>Parsed Guid.</returns>
        Public Function ParseBase64Uuid(base64Uuid As String) As Guid
            If String.IsNullOrWhiteSpace(base64Uuid) Then
                Throw New ArgumentException("Base64 UUID cannot be null or empty", NameOf(base64Uuid))
            End If
            
            ' Restore URL-safe chars and padding
            Dim standardBase64 As String = base64Uuid.Replace("-", "+").Replace("_", "/")
            Select Case standardBase64.Length Mod 4
                Case 2 : standardBase64 &= "=="
                Case 3 : standardBase64 &= "="
            End Select
            
            Dim bytes As Byte() = Convert.FromBase64String(standardBase64)
            Return New Guid(bytes)
        End Function

        ''' <summary>
        ''' Formats UUID with braces.
        ''' </summary>
        ''' <param name="uuid">UUID to format.</param>
        ''' <returns>UUID string with braces (e.g., "{550e8400-e29b-41d4-a716-446655440000}").</returns>
        Public Function FormatBraced(uuid As Guid) As String
            Return "{" & uuid.ToString("D").ToLowerInvariant() & "}"
        End Function

        ''' <summary>
        ''' Formats UUID with URN prefix.
        ''' </summary>
        ''' <param name="uuid">UUID to format.</param>
        ''' <returns>URN-formatted UUID (e.g., "urn:uuid:550e8400-e29b-41d4-a716-446655440000").</returns>
        Public Function FormatUrn(uuid As Guid) As String
            Return "urn:uuid:" & uuid.ToString("D").ToLowerInvariant()
        End Function

        ' =========================================================================
        ' UUID Component Extraction
        ' =========================================================================

        ''' <summary>
        ''' Gets the version of a UUID.
        ''' </summary>
        ''' <param name="uuid">UUID to inspect.</param>
        ''' <returns>UUID version.</returns>
        Public Function GetVersion(uuid As Guid) As UuidVersion
            Dim bytes As Byte() = uuid.ToByteArray()
            Dim versionBits As Byte = CByte((bytes(7) >> 4) And &HF)
            
            Select Case versionBits
                Case 1 : Return UuidVersion.Version1
                Case 2 : Return UuidVersion.Version2
                Case 3 : Return UuidVersion.Version3
                Case 4 : Return UuidVersion.Version4
                Case 5 : Return UuidVersion.Version5
                Case Else : Return UuidVersion.Unknown
            End Select
        End Function

        ''' <summary>
        ''' Gets the variant of a UUID.
        ''' </summary>
        ''' <param name="uuid">UUID to inspect.</param>
        ''' <returns>UUID variant.</returns>
        Public Function GetVariant(uuid As Guid) As UuidVariant
            Dim bytes As Byte() = uuid.ToByteArray()
            Dim variantBits As Byte = CByte((bytes(8) >> 6) And &H3)
            
            Select Case variantBits
                Case 0 : Return UuidVariant.NCS
                Case 1 : Return UuidVariant.RFC4122
                Case 2 : Return UuidVariant.Microsoft
                Case 3 : Return UuidVariant.Reserved
                Case Else : Return UuidVariant.Invalid
            End Select
        End Function

        ''' <summary>
        ''' Extracts timestamp from a v1 UUID.
        ''' </summary>
        ''' <param name="uuid">V1 UUID.</param>
        ''' <returns>Timestamp as DateTime (UTC), or Nothing if not v1.</returns>
        Public Function GetTimestamp(uuid As Guid) As DateTime?
            If GetVersion(uuid) <> UuidVersion.Version1 Then
                Return Nothing
            End If
            
            Dim bytes As Byte() = uuid.ToByteArray()
            
            ' Extract timestamp (100-ns intervals since Oct 15, 1582)
            ' Note: Guid stores bytes in a specific order
            Dim timestamp As Long = 0L
            
            ' Time low (bytes 0-3, reversed for little-endian int32)
            timestamp = (CType(bytes(3), Long) << 24) Or (CType(bytes(2), Long) << 16) Or (CType(bytes(1), Long) << 8) Or CType(bytes(0), Long)
            
            ' Time mid (bytes 4-5, reversed)
            timestamp = (timestamp << 16) Or (CType(bytes(5), Long) << 8) Or CType(bytes(4), Long)
            
            ' Time hi (bytes 6-7, reversed, minus version)
            timestamp = (timestamp << 12) Or ((CType(bytes(7), Long) << 8) Or CType(bytes(6), Long)) And &H0FFF
            
            ' Convert to DateTime
            ' UUID epoch: October 15, 1582
            Dim uuidEpoch As New DateTime(1582, 10, 15, 0, 0, 0, DateTimeKind.Utc)
            Return uuidEpoch.AddTicks(timestamp)
        End Function

        ''' <summary>
        ''' Extracts node ID from a v1 UUID.
        ''' </summary>
        ''' <param name="uuid">V1 UUID.</param>
        ''' <returns>Node ID as MAC address-like string, or Nothing if not v1.</returns>
        Public Function GetNodeId(uuid As Guid) As String
            If GetVersion(uuid) <> UuidVersion.Version1 Then
                Return Nothing
            End If
            
            Dim bytes As Byte() = uuid.ToByteArray()
            
            ' Node ID is in bytes 10-15
            Return String.Format("{0:X2}:{1:X2}:{2:X2}:{3:X2}:{4:X2}:{5:X2}",
                bytes(10), bytes(11), bytes(12), bytes(13), bytes(14), bytes(15))
        End Function

        ' =========================================================================
        ' UUID Comparison
        ' =========================================================================

        ''' <summary>
        ''' Compares two UUIDs.
        ''' </summary>
        ''' <param name="uuid1">First UUID.</param>
        ''' <param name="uuid2">Second UUID.</param>
        ''' <returns>-1, 0, or 1.</returns>
        Public Function Compare(uuid1 As Guid, uuid2 As Guid) As Integer
            Return uuid1.CompareTo(uuid2)
        End Function

        ''' <summary>
        ''' Checks if two UUIDs are equal.
        ''' </summary>
        ''' <param name="uuid1">First UUID.</param>
        ''' <param name="uuid2">Second UUID.</param>
        ''' <returns>True if equal.</returns>
        Public Function AreEqual(uuid1 As Guid, uuid2 As Guid) As Boolean
            Return uuid1 = uuid2
        End Function

        ''' <summary>
        ''' Sorts a list of UUIDs.
        ''' </summary>
        ''' <param name="uuids">List of UUIDs to sort.</param>
        ''' <returns>Sorted list.</returns>
        Public Function Sort(uuids As IEnumerable(Of Guid)) As List(Of Guid)
            Dim list As New List(Of Guid)(uuids)
            list.Sort()
            Return list
        End Function

        ' =========================================================================
        ' UUID Generation Helpers
        ' =========================================================================

        ''' <summary>
        ''' Generates multiple UUIDs at once.
        ''' </summary>
        ''' <param name="count">Number of UUIDs to generate.</param>
        ''' <returns>Array of UUIDs.</returns>
        Public Function NewUuids(count As Integer) As Guid()
            If count < 0 Then
                Throw New ArgumentException("Count cannot be negative", NameOf(count))
            End If
            
            Dim result(count - 1) As Guid
            For i As Integer = 0 To count - 1
                result(i) = Guid.NewGuid()
            Next
            
            Return result
        End Function

        ''' <summary>
        ''' Generates a sequential UUID prefix (for database indexing).
        ''' Creates a UUID that is sortable by timestamp.
        ''' </summary>
        ''' <returns>A timestamp-prefixed UUID.</returns>
        Public Function NewSequentialUuid() As Guid
            Dim timestamp As Long = GetGregorianTimestamp()
            Dim bytes(15) As Byte
            
            ' Use timestamp in first 8 bytes for sortability
            bytes(0) = CByte((timestamp >> 56) And &HFF)
            bytes(1) = CByte((timestamp >> 48) And &HFF)
            bytes(2) = CByte((timestamp >> 40) And &HFF)
            bytes(3) = CByte((timestamp >> 32) And &HFF)
            bytes(4) = CByte((timestamp >> 24) And &HFF)
            bytes(5) = CByte((timestamp >> 16) And &HFF)
            bytes(6) = CByte((timestamp >> 8) And &HFF)
            bytes(7) = CByte(timestamp And &HFF)
            
            ' Random bytes for uniqueness
            SyncLock RandomLock
                RandomGenerator.NextBytes(New Byte(7) {})
                bytes(8) = CByte(RandomGenerator.Next(256))
                bytes(9) = CByte(RandomGenerator.Next(256))
                bytes(10) = CByte(RandomGenerator.Next(256))
                bytes(11) = CByte(RandomGenerator.Next(256))
                bytes(12) = CByte(RandomGenerator.Next(256))
                bytes(13) = CByte(RandomGenerator.Next(256))
                bytes(14) = CByte(RandomGenerator.Next(256))
                bytes(15) = CByte(RandomGenerator.Next(256))
            End SyncLock
            
            ' Set version 4 and variant
            bytes(6) = CByte((bytes(6) And &H0F) Or &H40)
            bytes(8) = CByte((bytes(8) And &H3F) Or &H80)
            
            Return New Guid(bytes)
        End Function

        ''' <summary>
        ''' Creates a UUID from two 64-bit integers.
        ''' </summary>
        ''' <param name="high">High 64 bits.</param>
        ''' <param name="low">Low 64 bits.</param>
        ''' <returns>Combined UUID.</returns>
        Public Function FromInt64(high As Long, low As Long) As Guid
            Dim bytes(15) As Byte
            
            ' Copy high (big-endian)
            For i As Integer = 0 To 7
                bytes(i) = CByte((high >> (56 - i * 8)) And &HFF)
            Next
            
            ' Copy low (big-endian)
            For i As Integer = 0 To 7
                bytes(i + 8) = CByte((low >> (56 - i * 8)) And &HFF)
            Next
            
            Return New Guid(bytes)
        End Function

        ''' <summary>
        ''' Splits a UUID into two 64-bit integers.
        ''' </summary>
        ''' <param name="uuid">UUID to split.</param>
        ''' <returns>Tuple of (high, low) 64-bit integers.</returns>
        Public Function ToInt64(uuid As Guid) As Tuple(Of Long, Long)
            Dim bytes As Byte() = uuid.ToByteArray()
            
            Dim high As Long = 0L
            Dim low As Long = 0L
            
            For i As Integer = 0 To 7
                high = (high << 8) Or bytes(i)
                low = (low << 8) Or bytes(i + 8)
            Next
            
            Return Tuple.Create(high, low)
        End Function

        ''' <summary>
        ''' Generates a short ID (first 8 chars of UUID).
        ''' </summary>
        ''' <returns>8-character ID.</returns>
        Public Function NewShortId() As String
            Return Guid.NewGuid().ToString("N").Substring(0, 8)
        End Function

        ''' <summary>
        ''' Generates a medium ID (first 12 chars of UUID).
        ''' </summary>
        ''' <returns>12-character ID.</returns>
        Public Function NewMediumId() As String
            Return Guid.NewGuid().ToString("N").Substring(0, 12)
        End Function

    End Module

End Namespace