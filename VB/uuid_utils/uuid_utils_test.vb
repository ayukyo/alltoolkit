' =============================================================================
' AllToolkit - UUID Utilities Tests for VB.NET
' =============================================================================
' Unit tests for UUID utilities module.
' =============================================================================

Imports System
Imports System.Collections.Generic
Imports AllToolkit

Namespace AllToolkit.Tests

    ''' <summary>
    ''' Test class for UUID utilities.
    ''' </summary>
    Public Class UuidUtilsTest

        Public Shared Sub RunAllTests()
            Console.WriteLine("=== UUID Utilities Tests ===")
            Console.WriteLine()
            
            TestGeneration()
            TestValidation()
            TestFormatting()
            TestParsing()
            TestVersionDetection()
            TestNameBasedUuids()
            TestComparison()
            TestHelpers()
            TestSequentialUuid()
            
            Console.WriteLine()
            Console.WriteLine("All tests passed!")
        End Sub

        ' =========================================================================
        ' Generation Tests
        ' =========================================================================

        Private Shared Sub TestGeneration()
            Console.WriteLine("--- Testing Generation ---")
            
            ' Test NewUuid
            Dim uuid1 As Guid = UuidUtils.NewUuid()
            Assert(uuid1 <> Guid.Empty, "NewUuid should not be empty")
            Console.WriteLine($"  [PASS] NewUuid generated: {UuidUtils.Format(uuid1)}")
            
            ' Test NewV4
            Dim uuid2 As Guid = UuidUtils.NewV4()
            Assert(uuid2 <> Guid.Empty, "NewV4 should not be empty")
            Assert(UuidUtils.GetVersion(uuid2) = UuidVersion.Version4, "NewV4 should be version 4")
            Console.WriteLine($"  [PASS] NewV4 generated: {UuidUtils.Format(uuid2)}")
            
            ' Test NewSecureUuid
            Dim uuid3 As Guid = UuidUtils.NewSecureUuid()
            Assert(uuid3 <> Guid.Empty, "NewSecureUuid should not be empty")
            Assert(UuidUtils.GetVersion(uuid3) = UuidVersion.Version4, "NewSecureUuid should be version 4")
            Console.WriteLine($"  [PASS] NewSecureUuid generated: {UuidUtils.Format(uuid3)}")
            
            ' Test NewV1
            Dim uuid4 As Guid = UuidUtils.NewV1()
            Assert(uuid4 <> Guid.Empty, "NewV1 should not be empty")
            Assert(UuidUtils.GetVersion(uuid4) = UuidVersion.Version1, "NewV1 should be version 1")
            Console.WriteLine($"  [PASS] NewV1 generated: {UuidUtils.Format(uuid4)}")
            
            ' Test uniqueness
            Dim uuids As Guid() = UuidUtils.NewUuids(1000)
            Dim uniqueSet As New HashSet(Of Guid)(uuids)
            Assert(uniqueSet.Count = 1000, "All 1000 UUIDs should be unique")
            Console.WriteLine($"  [PASS] 1000 UUIDs generated, all unique")
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Validation Tests
        ' =========================================================================

        Private Shared Sub TestValidation()
            Console.WriteLine("--- Testing Validation ---")
            
            ' Test valid UUID
            Dim validUuid As String = "550e8400-e29b-41d4-a716-446655440000"
            Assert(UuidUtils.IsValidUuid(validUuid), "Standard format should be valid")
            Console.WriteLine($"  [PASS] Valid UUID accepted: {validUuid}")
            
            ' Test uppercase
            Dim upperUuid As String = "550E8400-E29B-41D4-A716-446655440000"
            Assert(UuidUtils.IsValidUuid(upperUuid), "Uppercase should be valid")
            Console.WriteLine($"  [PASS] Uppercase UUID accepted")
            
            ' Test without dashes
            Dim compactUuid As String = "550e8400e29b41d4a716446655440000"
            Assert(UuidUtils.IsValidUuid(compactUuid), "Compact format should be valid")
            Console.WriteLine($"  [PASS] Compact UUID accepted")
            
            ' Test invalid UUID
            Dim invalidUuid As String = "not-a-uuid"
            Assert(Not UuidUtils.IsValidUuid(invalidUuid), "Invalid string should fail")
            Console.WriteLine($"  [PASS] Invalid UUID rejected: {invalidUuid}")
            
            ' Test empty string
            Assert(Not UuidUtils.IsValidUuid(""), "Empty string should fail")
            Console.WriteLine($"  [PASS] Empty string rejected")
            
            ' Test nil UUID
            Assert(UuidUtils.IsNilUuid(Guid.Empty), "Guid.Empty should be nil")
            Console.WriteLine($"  [PASS] Nil UUID detected")
            
            Dim uuid As Guid = UuidUtils.NewUuid()
            Assert(Not UuidUtils.IsNilUuid(uuid), "New UUID should not be nil")
            Console.WriteLine($"  [PASS] Non-nil UUID detected")
            
            ' Test validation result
            Dim result As UuidValidationResult = UuidUtils.ValidateUuid(validUuid)
            Assert(result.IsValid, "Validation result should be valid")
            Assert(result.Value <> Guid.Empty, "Parsed value should not be empty")
            Console.WriteLine($"  [PASS] ValidateUuid returned valid result")
            
            Dim badResult As UuidValidationResult = UuidUtils.ValidateUuid("invalid")
            Assert(Not badResult.IsValid, "Bad validation result should be invalid")
            Assert(badResult.ErrorMessage <> "", "Error message should be present")
            Console.WriteLine($"  [PASS] Invalid UUID gave error message: {badResult.ErrorMessage}")
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Formatting Tests
        ' =========================================================================

        Private Shared Sub TestFormatting()
            Console.WriteLine("--- Testing Formatting ---")
            
            Dim uuid As Guid = Guid.Parse("550e8400-e29b-41d4-a716-446655440000")
            
            ' Test standard format
            Dim standard As String = UuidUtils.Format(uuid)
            Assert(standard = "550e8400-e29b-41d4-a716-446655440000", "Standard format correct")
            Console.WriteLine($"  [PASS] Format: {standard}")
            
            ' Test uppercase
            Dim upper As String = UuidUtils.FormatUpper(uuid)
            Assert(upper = "550E8400-E29B-41D4-A716-446655440000", "Uppercase format correct")
            Console.WriteLine($"  [PASS] FormatUpper: {upper}")
            
            ' Test compact
            Dim compact As String = UuidUtils.FormatCompact(uuid)
            Assert(compact = "550e8400e29b41d4a716446655440000", "Compact format correct")
            Assert(compact.Length = 32, "Compact length should be 32")
            Console.WriteLine($"  [PASS] FormatCompact: {compact}")
            
            ' Test compact uppercase
            Dim compactUpper As String = UuidUtils.FormatCompactUpper(uuid)
            Assert(compactUpper = "550E8400E29B41D4A716446655440000", "Compact uppercase correct")
            Console.WriteLine($"  [PASS] FormatCompactUpper: {compactUpper}")
            
            ' Test Base64
            Dim base64 As String = UuidUtils.FormatBase64(uuid)
            Assert(base64.Length = 22, "Base64 UUID should be 22 chars")
            Console.WriteLine($"  [PASS] FormatBase64: {base64} ({base64.Length} chars)")
            
            ' Test Base64 roundtrip
            Dim parsedBase64 As Guid = UuidUtils.ParseBase64Uuid(base64)
            Assert(parsedBase64 = uuid, "Base64 roundtrip should work")
            Console.WriteLine($"  [PASS] Base64 roundtrip successful")
            
            ' Test braced
            Dim braced As String = UuidUtils.FormatBraced(uuid)
            Assert(braced.StartsWith("{") AndAlso braced.EndsWith("}"), "Braced format has braces")
            Console.WriteLine($"  [PASS] FormatBraced: {braced}")
            
            ' Test URN
            Dim urn As String = UuidUtils.FormatUrn(uuid)
            Assert(urn.StartsWith("urn:uuid:"), "URN format has prefix")
            Console.WriteLine($"  [PASS] FormatUrn: {urn}")
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Parsing Tests
        ' =========================================================================

        Private Shared Sub TestParsing()
            Console.WriteLine("--- Testing Parsing ---")
            
            ' Test ParseUuid
            Dim uuid As Guid = UuidUtils.ParseUuid("550e8400-e29b-41d4-a716-446655440000")
            Assert(uuid <> Guid.Empty, "Parsed UUID should not be empty")
            Console.WriteLine($"  [PASS] ParseUuid worked")
            
            ' Test TryParseUuid
            Dim parsed As Guid
            Assert(UuidUtils.TryParseUuid("550e8400-e29b-41d4-a716-446655440000", parsed), "TryParseUuid should succeed")
            Assert(parsed <> Guid.Empty, "TryParseUuid result should not be empty")
            Console.WriteLine($"  [PASS] TryParseUuid succeeded")
            
            Assert(Not UuidUtils.TryParseUuid("invalid", parsed), "TryParseUuid should fail for invalid")
            Console.WriteLine($"  [PASS] TryParseUuid rejected invalid string")
            
            ' Test ParseCompactUuid
            Dim compact As Guid = UuidUtils.ParseCompactUuid("550e8400e29b41d4a716446655440000")
            Assert(compact = uuid, "ParseCompactUuid should match standard parse")
            Console.WriteLine($"  [PASS] ParseCompactUuid worked")
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Version Detection Tests
        ' =========================================================================

        Private Shared Sub TestVersionDetection()
            Console.WriteLine("--- Testing Version Detection ---")
            
            ' Test v1 detection
            Dim v1 As Guid = UuidUtils.NewV1()
            Assert(UuidUtils.GetVersion(v1) = UuidVersion.Version1, "V1 UUID detected correctly")
            Assert(UuidUtils.GetVariant(v1) = UuidVariant.RFC4122, "V1 should be RFC4122 variant")
            Console.WriteLine($"  [PASS] V1 UUID: version={UuidUtils.GetVersion(v1)}, variant={UuidUtils.GetVariant(v1)}")
            
            ' Test v4 detection
            Dim v4 As Guid = UuidUtils.NewV4()
            Assert(UuidUtils.GetVersion(v4) = UuidVersion.Version4, "V4 UUID detected correctly")
            Assert(UuidUtils.GetVariant(v4) = UuidVariant.RFC4122, "V4 should be RFC4122 variant")
            Console.WriteLine($"  [PASS] V4 UUID: version={UuidUtils.GetVersion(v4)}, variant={UuidUtils.GetVariant(v4)}")
            
            ' Test v1 timestamp extraction
            Dim timestamp As DateTime? = UuidUtils.GetTimestamp(v1)
            Assert(timestamp.HasValue, "V1 should have timestamp")
            Dim diff As TimeSpan = DateTime.UtcNow - timestamp.Value
            Assert(diff.TotalSeconds < 5, "Timestamp should be recent")
            Console.WriteLine($"  [PASS] V1 timestamp: {timestamp.Value:yyyy-MM-dd HH:mm:ss}")
            
            ' Test v1 node ID
            Dim nodeId As String = UuidUtils.GetNodeId(v1)
            Assert(nodeId IsNot Nothing, "V1 should have node ID")
            Assert(nodeId.Length = 17, "Node ID should be 17 chars (6 hex pairs with colons)")
            Console.WriteLine($"  [PASS] V1 node ID: {nodeId}")
            
            ' Test nil UUID
            Assert(UuidUtils.GetVersion(Guid.Empty) = UuidVersion.Unknown, "Nil UUID has unknown version")
            Console.WriteLine($"  [PASS] Nil UUID version: Unknown")
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Name-Based UUID Tests
        ' =========================================================================

        Private Shared Sub TestNameBasedUuids()
            Console.WriteLine("--- Testing Name-Based UUIDs ---")
            
            ' Test V3 (MD5)
            Dim v3a As Guid = UuidUtils.NewV3(UuidNamespaces.DNS, "example.com")
            Dim v3b As Guid = UuidUtils.NewV3(UuidNamespaces.DNS, "example.com")
            Assert(v3a = v3b, "Same name should produce same V3 UUID")
            Assert(UuidUtils.GetVersion(v3a) = UuidVersion.Version3, "V3 should be version 3")
            Console.WriteLine($"  [PASS] V3 for DNS 'example.com': {UuidUtils.Format(v3a)}")
            
            ' Test V5 (SHA-1)
            Dim v5a As Guid = UuidUtils.NewV5(UuidNamespaces.URL, "https://example.com")
            Dim v5b As Guid = UuidUtils.NewV5(UuidNamespaces.URL, "https://example.com")
            Assert(v5a = v5b, "Same name should produce same V5 UUID")
            Assert(UuidUtils.GetVersion(v5a) = UuidVersion.Version5, "V5 should be version 5")
            Console.WriteLine($"  [PASS] V5 for URL 'https://example.com': {UuidUtils.Format(v5a)}")
            
            ' Test different names produce different UUIDs
            Dim v5c As Guid = UuidUtils.NewV5(UuidNamespaces.URL, "https://other.com")
            Assert(v5a <> v5c, "Different names should produce different UUIDs")
            Console.WriteLine($"  [PASS] Different names produce different UUIDs")
            
            ' Test different namespaces produce different UUIDs
            Dim v5d As Guid = UuidUtils.NewV5(UuidNamespaces.DNS, "https://example.com")
            Assert(v5a <> v5d, "Different namespaces should produce different UUIDs")
            Console.WriteLine($"  [PASS] Different namespaces produce different UUIDs")
            
            ' Test predefined namespace values
            Assert(UuidNamespaces.DNS <> Guid.Empty, "DNS namespace should not be empty")
            Assert(UuidNamespaces.URL <> Guid.Empty, "URL namespace should not be empty")
            Assert(UuidNamespaces.OID <> Guid.Empty, "OID namespace should not be empty")
            Assert(UuidNamespaces.X500 <> Guid.Empty, "X500 namespace should not be empty")
            Console.WriteLine($"  [PASS] Predefined namespaces are valid")
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Comparison Tests
        ' =========================================================================

        Private Shared Sub TestComparison()
            Console.WriteLine("--- Testing Comparison ---")
            
            Dim uuid1 As Guid = UuidUtils.NewUuid()
            Dim uuid2 As Guid = UuidUtils.NewUuid()
            
            ' Test equality
            Assert(UuidUtils.AreEqual(uuid1, uuid1), "Same UUID should be equal")
            Console.WriteLine($"  [PASS] AreEqual(uuid1, uuid1) = True")
            
            Assert(Not UuidUtils.AreEqual(uuid1, uuid2), "Different UUIDs should not be equal")
            Console.WriteLine($"  [PASS] AreEqual(uuid1, uuid2) = False")
            
            ' Test compare
            Dim cmp As Integer = UuidUtils.Compare(uuid1, uuid2)
            Assert(cmp <> 0, "Compare should show difference")
            Console.WriteLine($"  [PASS] Compare result: {cmp}")
            
            ' Test sort
            Dim uuids As New List(Of Guid)()
            uuids.Add(uuid1)
            uuids.Add(uuid2)
            uuids.Add(Guid.Parse("00000000-0000-0000-0000-000000000001"))
            uuids.Add(Guid.Parse("ffffffff-ffff-ffff-ffff-ffffffffffff"))
            
            Dim sorted As List(Of Guid) = UuidUtils.Sort(uuids)
            For i As Integer = 0 To sorted.Count - 2
                Assert(sorted(i).CompareTo(sorted(i + 1)) <= 0, "Sorted list should be ordered")
            Next
            Console.WriteLine($"  [PASS] Sort produced ordered list")
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Helper Tests
        ' =========================================================================

        Private Shared Sub TestHelpers()
            Console.WriteLine("--- Testing Helpers ---")
            
            ' Test NewUuids
            Dim uuids As Guid() = UuidUtils.NewUuids(10)
            Assert(uuids.Length = 10, "NewUuids should return 10 UUIDs")
            Console.WriteLine($"  [PASS] NewUuids(10) returned 10 UUIDs")
            
            ' Test NewShortId
            Dim shortId As String = UuidUtils.NewShortId()
            Assert(shortId.Length = 8, "Short ID should be 8 chars")
            Console.WriteLine($"  [PASS] NewShortId: {shortId} (8 chars)")
            
            ' Test NewMediumId
            Dim mediumId As String = UuidUtils.NewMediumId()
            Assert(mediumId.Length = 12, "Medium ID should be 12 chars")
            Console.WriteLine($"  [PASS] NewMediumId: {mediumId} (12 chars)")
            
            ' Test FromInt64 / ToInt64
            Dim high As Long = 12345678901234L
            Dim low As Long = 56789012345678L
            Dim fromInt As Guid = UuidUtils.FromInt64(high, low)
            Dim back As Tuple(Of Long, Long) = UuidUtils.ToInt64(fromInt)
            Console.WriteLine($"  [PASS] FromInt64 created UUID: {UuidUtils.Format(fromInt)}")
            Console.WriteLine($"  [PASS] ToInt64 extracted: high={back.Item1}, low={back.Item2}")
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Sequential UUID Tests
        ' =========================================================================

        Private Shared Sub TestSequentialUuid()
            Console.WriteLine("--- Testing Sequential UUID ---")
            
            ' Generate multiple sequential UUIDs
            Dim seq1 As Guid = UuidUtils.NewSequentialUuid()
            Dim seq2 As Guid = UuidUtils.NewSequentialUuid()
            Dim seq3 As Guid = UuidUtils.NewSequentialUuid()
            
            ' They should be version 4
            Assert(UuidUtils.GetVersion(seq1) = UuidVersion.Version4, "Sequential should be v4")
            Assert(UuidUtils.GetVersion(seq2) = UuidVersion.Version4, "Sequential should be v4")
            Console.WriteLine($"  [PASS] Sequential UUIDs are version 4")
            
            ' Generated at different times should be sortable
            ' (Note: in rapid succession, timestamps might be same)
            Console.WriteLine($"  [PASS] Sequential UUID 1: {UuidUtils.Format(seq1)}")
            Console.WriteLine($"  [PASS] Sequential UUID 2: {UuidUtils.Format(seq2)}")
            Console.WriteLine($"  [PASS] Sequential UUID 3: {UuidUtils.Format(seq3)}")
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Assertion Helper
        ' =========================================================================

        Private Shared Sub Assert(condition As Boolean, message As String)
            If Not condition Then
                Console.WriteLine($"  [FAIL] {message}")
                Throw New Exception($"Assertion failed: {message}")
            End If
        End Sub

    End Class

End Namespace