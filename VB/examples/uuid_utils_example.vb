' =============================================================================
' AllToolkit - UUID Utilities Examples for VB.NET
' =============================================================================
' Usage examples for UUID utilities module.
' =============================================================================

Imports System
Imports System.Collections.Generic
Imports AllToolkit

Namespace AllToolkit.Examples

    ''' <summary>
    ''' Example class demonstrating UUID utilities usage.
    ''' </summary>
    Public Class UuidUtilsExample

        Public Shared Sub Main()
            Console.WriteLine("=== UUID Utilities Examples ===")
            Console.WriteLine()
            
            BasicGeneration()
            FormattingOptions()
            ValidationAndParsing()
            NameBasedUuids()
            VersionDetection()
            ShortIds()
            SequentialUuids()
            PracticalApplications()
            
            Console.WriteLine()
            Console.WriteLine("Examples complete!")
        End Sub

        ' =========================================================================
        ' Basic Generation
        ' =========================================================================

        Private Shared Sub BasicGeneration()
            Console.WriteLine("--- 1. Basic UUID Generation ---")
            
            ' Generate a random UUID (version 4)
            Dim uuid As Guid = UuidUtils.NewUuid()
            Console.WriteLine($"  Random UUID (v4): {UuidUtils.Format(uuid)}")
            
            ' Generate multiple UUIDs
            Dim uuids As Guid() = UuidUtils.NewUuids(5)
            Console.WriteLine("  5 UUIDs generated:")
            For Each u As Guid In uuids
                Console.WriteLine($"    {UuidUtils.Format(u)}")
            Next
            
            ' Generate cryptographically secure UUID
            Dim secureUuid As Guid = UuidUtils.NewSecureUuid()
            Console.WriteLine($"  Secure UUID: {UuidUtils.Format(secureUuid)}")
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Formatting Options
        ' =========================================================================

        Private Shared Sub FormattingOptions()
            Console.WriteLine("--- 2. Formatting Options ---")
            
            Dim uuid As Guid = UuidUtils.NewUuid()
            
            Console.WriteLine($"  Standard (default):     {UuidUtils.Format(uuid)}")
            Console.WriteLine($"  Uppercase:              {UuidUtils.FormatUpper(uuid)}")
            Console.WriteLine($"  Compact (no dashes):    {UuidUtils.FormatCompact(uuid)}")
            Console.WriteLine($"  Compact Upper:          {UuidUtils.FormatCompactUpper(uuid)}")
            Console.WriteLine($"  Base64 (22 chars):      {UuidUtils.FormatBase64(uuid)}")
            Console.WriteLine($"  With braces:            {UuidUtils.FormatBraced(uuid)}")
            Console.WriteLine($"  URN format:             {UuidUtils.FormatUrn(uuid)}")
            
            ' Base64 roundtrip
            Dim base64 As String = UuidUtils.FormatBase64(uuid)
            Dim parsed As Guid = UuidUtils.ParseBase64Uuid(base64)
            Console.WriteLine($"  Base64 roundtrip:       {UuidUtils.AreEqual(uuid, parsed)}")
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Validation and Parsing
        ' =========================================================================

        Private Shared Sub ValidationAndParsing()
            Console.WriteLine("--- 3. Validation and Parsing ---")
            
            ' Validate different formats
            Dim formats As String() = {
                "550e8400-e29b-41d4-a716-446655440000",
                "550E8400-E29B-41D4-A716-446655440000",
                "550e8400e29b41d4a716446655440000",
                "{550e8400-e29b-41d4-a716-446655440000}",
                "not-a-valid-uuid"
            }
            
            Console.WriteLine("  Validation results:")
            For Each fmt As String In formats
                Dim valid As Boolean = UuidUtils.IsValidUuid(fmt)
                Console.WriteLine($"    '{fmt}' -> {valid}")
            Next
            
            ' Detailed validation
            Dim result As UuidValidationResult = UuidUtils.ValidateUuid("550e8400-e29b-41d4-a716-446655440000")
            Console.WriteLine($"  Detailed validation:")
            Console.WriteLine($"    IsValid: {result.IsValid}")
            Console.WriteLine($"    Value: {UuidUtils.Format(result.Value)}")
            
            ' Parsing compact UUID
            Dim compactUuid As Guid = UuidUtils.ParseCompactUuid("550e8400e29b41d4a716446655440000")
            Console.WriteLine($"  Compact parsed: {UuidUtils.Format(compactUuid)}")
            
            ' Check nil UUID
            Console.WriteLine($"  Is Guid.Empty nil: {UuidUtils.IsNilUuid(Guid.Empty)}")
            Console.WriteLine($"  Is new UUID nil: {UuidUtils.IsNilUuid(UuidUtils.NewUuid())}")
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Name-Based UUIDs
        ' =========================================================================

        Private Shared Sub NameBasedUuids()
            Console.WriteLine("--- 4. Name-Based UUIDs (v3 and v5) ---")
            
            ' V3 (MD5) - deterministic based on name
            Dim dnsV3 As Guid = UuidUtils.NewV3(UuidNamespaces.DNS, "example.com")
            Console.WriteLine($"  V3 (DNS, 'example.com'): {UuidUtils.Format(dnsV3)}")
            
            ' Same name = same UUID
            Dim dnsV3Again As Guid = UuidUtils.NewV3(UuidNamespaces.DNS, "example.com")
            Console.WriteLine($"  V3 again: {UuidUtils.Format(dnsV3Again)}")
            Console.WriteLine($"  Are equal: {UuidUtils.AreEqual(dnsV3, dnsV3Again)}")
            
            ' V5 (SHA-1) - deterministic based on name
            Dim urlV5 As Guid = UuidUtils.NewV5(UuidNamespaces.URL, "https://api.example.com/users/123")
            Console.WriteLine($"  V5 (URL, 'https://api.example.com/users/123'): {UuidUtils.Format(urlV5)}")
            
            ' Use OID namespace
            Dim oidV5 As Guid = UuidUtils.NewV5(UuidNamespaces.OID, "1.2.3.4.5.6")
            Console.WriteLine($"  V5 (OID, '1.2.3.4.5.6'): {UuidUtils.Format(oidV5)}")
            
            ' Use X500 namespace
            Dim x500V5 As Guid = UuidUtils.NewV5(UuidNamespaces.X500, "cn=John Doe,ou=Users,o=Example")
            Console.WriteLine($"  V5 (X500, 'cn=John Doe...'): {UuidUtils.Format(x500V5)}")
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Version Detection
        ' =========================================================================

        Private Shared Sub VersionDetection()
            Console.WriteLine("--- 5. Version Detection ---")
            
            ' Generate different versions
            Dim v1 As Guid = UuidUtils.NewV1()
            Dim v4 As Guid = UuidUtils.NewV4()
            Dim v5 As Guid = UuidUtils.NewV5(UuidNamespaces.URL, "test")
            
            Console.WriteLine($"  V1 UUID: {UuidUtils.Format(v1)}")
            Console.WriteLine($"    Version: {UuidUtils.GetVersion(v1)}")
            Console.WriteLine($"    Variant: {UuidUtils.GetVariant(v1)}")
            Console.WriteLine($"    Timestamp: {UuidUtils.GetTimestamp(v1):yyyy-MM-dd HH:mm:ss}")
            Console.WriteLine($"    Node ID: {UuidUtils.GetNodeId(v1)}")
            
            Console.WriteLine($"  V4 UUID: {UuidUtils.Format(v4)}")
            Console.WriteLine($"    Version: {UuidUtils.GetVersion(v4)}")
            Console.WriteLine($"    Variant: {UuidUtils.GetVariant(v4)}")
            
            Console.WriteLine($"  V5 UUID: {UuidUtils.Format(v5)}")
            Console.WriteLine($"    Version: {UuidUtils.GetVersion(v5)}")
            Console.WriteLine($"    Variant: {UuidUtils.GetVariant(v5)}")
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Short IDs
        ' =========================================================================

        Private Shared Sub ShortIds()
            Console.WriteLine("--- 6. Short IDs ---")
            
            ' 8-character IDs
            For i As Integer = 1 To 5
                Console.WriteLine($"  Short ID ({i}): {UuidUtils.NewShortId()}")
            Next
            
            ' 12-character IDs
            For i As Integer = 1 To 5
                Console.WriteLine($"  Medium ID ({i}): {UuidUtils.NewMediumId()}")
            Next
            
            ' Base64 (22 chars) - good for URLs
            Dim uuid As Guid = UuidUtils.NewUuid()
            Dim base64 As String = UuidUtils.FormatBase64(uuid)
            Console.WriteLine($"  Base64 ID: {base64}")
            Console.WriteLine($"  Length: {base64.Length} characters (URL-safe)")
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Sequential UUIDs
        ' =========================================================================

        Private Shared Sub SequentialUuids()
            Console.WriteLine("--- 7. Sequential UUIDs ---")
            
            ' Sequential UUIDs are good for database indexing
            Dim seqUuids As New List(Of Guid)()
            For i As Integer = 1 To 5
                seqUuids.Add(UuidUtils.NewSequentialUuid())
                ' Small delay to show sequence
                System.Threading.Thread.Sleep(10)
            Next
            
            Console.WriteLine("  Sequential UUIDs (good for DB indexing):")
            For Each seq As Guid In seqUuids
                Console.WriteLine($"    {UuidUtils.Format(seq)}")
            Next
            
            Console.WriteLine()
        End Sub

        ' =========================================================================
        ' Practical Applications
        ' =========================================================================

        Private Shared Sub PracticalApplications()
            Console.WriteLine("--- 8. Practical Applications ---")
            
            ' Generate user ID
            Dim userId As Guid = UuidUtils.NewUuid()
            Console.WriteLine($"  User ID: {UuidUtils.FormatCompact(userId)}")
            
            ' Generate session ID (short)
            Dim sessionId As String = UuidUtils.NewMediumId()
            Console.WriteLine($"  Session ID: {sessionId}")
            
            ' Generate order number (short + date prefix)
            Dim orderNum As String = DateTime.Now.ToString("yyyyMMdd") & "-" & UuidUtils.NewShortId()
            Console.WriteLine($"  Order Number: {orderNum}")
            
            ' Generate API key (base64)
            Dim apiKey As String = UuidUtils.FormatBase64(UuidUtils.NewSecureUuid())
            Console.WriteLine($"  API Key: {apiKey}")
            
            ' Generate transaction ID
            Dim txId As Guid = UuidUtils.NewV1()  ' Time-based for traceability
            Console.WriteLine($"  Transaction ID (v1): {UuidUtils.FormatCompactUpper(txId)}")
            
            ' Generate deterministic resource ID (v5)
            Dim resourceId As Guid = UuidUtils.NewV5(UuidNamespaces.URL, "https://myapp.com/resources/avatar-user-123")
            Console.WriteLine($"  Deterministic Resource ID (v5): {UuidUtils.FormatCompact(resourceId)}")
            
            ' Generate traceable request ID
            Dim requestId As String = UuidUtils.FormatBase64(UuidUtils.NewV1())
            Console.WriteLine($"  Traceable Request ID: {requestId}")
            
            Console.WriteLine()
        End Sub

    End Class

End Namespace