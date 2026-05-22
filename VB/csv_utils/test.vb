' =============================================================================
' AllToolkit - CSV Utilities Tests for VB.NET
' =============================================================================
' Comprehensive unit tests for CSV utilities.
' Run with: dotnet test
' =============================================================================

Imports System
Imports System.IO
Imports System.Collections.Generic
Imports Microsoft.VisualStudio.TestTools.UnitTesting
Imports AllToolkit

<TestClass>
Public Class CsvUtilsTests

    ' =========================================================================
    ' ParseLine Tests
    ' =========================================================================

    <TestMethod>
    Public Sub ParseLine_SimpleFields_ReturnsCorrectCount()
        Dim line As String = "a,b,c"
        Dim fields As List(Of String) = CsvUtils.ParseLine(line)
        
        Assert.AreEqual(3, fields.Count)
        Assert.AreEqual("a", fields(0))
        Assert.AreEqual("b", fields(1))
        Assert.AreEqual("c", fields(2))
    End Sub

    <TestMethod>
    Public Sub ParseLine_EmptyField_ReturnsEmptyString()
        Dim line As String = "a,,c"
        Dim fields As List(Of String) = CsvUtils.ParseLine(line)
        
        Assert.AreEqual(3, fields.Count)
        Assert.AreEqual(String.Empty, fields(1))
    End Sub

    <TestMethod>
    Public Sub ParseLine_QuotedField_ReturnsUnquoted()
        Dim line As String = "a,""quoted"",c"
        Dim fields As List(Of String) = CsvUtils.ParseLine(line)
        
        Assert.AreEqual("quoted", fields(1))
    End Sub

    <TestMethod>
    Public Sub ParseLine_EscapedQuote_ReturnsCorrectValue()
        Dim line As String = "a,""quote""""inside"",c"
        Dim fields As List(Of String) = CsvUtils.ParseLine(line)
        
        Assert.AreEqual("quote""inside", fields(1))
    End Sub

    <TestMethod>
    Public Sub ParseLine_CommaInQuotes_ReturnsAsField()
        Dim line As String = """a,b"",c"
        Dim fields As List(Of String) = CsvUtils.ParseLine(line)
        
        Assert.AreEqual(2, fields.Count)
        Assert.AreEqual("a,b", fields(0))
    End Sub

    <TestMethod>
    Public Sub ParseLine_NewlineInQuotes_ReturnsAsField()
        Dim line As String = """line1" & ControlChars.Lf & "line2"",c"
        Dim fields As List(Of String) = CsvUtils.ParseLine(line)
        
        Assert.AreEqual(2, fields.Count)
        Assert.IsTrue(fields(0).Contains(ControlChars.Lf))
    End Sub

    <TestMethod>
    Public Sub ParseLine_TSV_ReturnsCorrectFields()
        Dim line As String = "a" & ControlChars.Tab & "b" & ControlChars.Tab & "c"
        Dim fields As List(Of String) = CsvUtils.ParseLine(line, CsvOptions.TSV())
        
        Assert.AreEqual(3, fields.Count)
    End Sub

    <TestMethod>
    Public Sub ParseLine_EmptyString_ReturnsEmptyList()
        Dim fields As List(Of String) = CsvUtils.ParseLine(String.Empty)
        Assert.AreEqual(0, fields.Count)
    End Sub

    <TestMethod>
    Public Sub ParseLine_TrimsFieldsWhenEnabled()
        Dim line As String = " a , b , c "
        Dim opts As New CsvOptions With { .TrimFields = True }
        Dim fields As List(Of String) = CsvUtils.ParseLine(line, opts)
        
        Assert.AreEqual("a", fields(0))
        Assert.AreEqual("b", fields(1))
        Assert.AreEqual("c", fields(2))
    End Sub

    ' =========================================================================
    ' GenerateLine Tests
    ' =========================================================================

    <TestMethod>
    Public Sub GenerateLine_SimpleFields_ReturnsCorrectFormat()
        Dim fields As String() = {"a", "b", "c"}
        Dim line As String = CsvUtils.GenerateLine(fields)
        
        Assert.AreEqual("a,b,c", line)
    End Sub

    <TestMethod>
    Public Sub GenerateLine_EmptyField_ReturnsCorrectFormat()
        Dim fields As String() = {"a", "", "c"}
        Dim line As String = CsvUtils.GenerateLine(fields)
        
        Assert.AreEqual("a,,c", line)
    End Sub

    <TestMethod>
    Public Sub GenerateLine_CommaInField_ReturnsQuoted()
        Dim fields As String() = {"a,b", "c"}
        Dim line As String = CsvUtils.GenerateLine(fields)
        
        Assert.AreEqual("""a,b"",c", line)
    End Sub

    <TestMethod>
    Public Sub GenerateLine_QuoteInField_ReturnsEscaped()
        Dim fields As String() = {"quote""here", "c"}
        Dim line As String = CsvUtils.GenerateLine(fields)
        
        Assert.AreEqual("""quote""""here"",c", line)
    End Sub

    <TestMethod>
    Public Sub GenerateLine_NewlineInField_ReturnsQuoted()
        Dim fields As String() = {"line1" & ControlChars.Lf & "line2", "c"}
        Dim line As String = CsvUtils.GenerateLine(fields)
        
        Assert.IsTrue(line.StartsWith(""""))
    End Sub

    <TestMethod>
    Public Sub GenerateLine_TSV_ReturnsCorrectFormat()
        Dim fields As String() = {"a", "b", "c"}
        Dim line As String = CsvUtils.GenerateLine(fields, CsvOptions.TSV())
        
        Assert.AreEqual("a" & ControlChars.Tab & "b" & ControlChars.Tab & "c", line)
    End Sub

    ' =========================================================================
    ' ParseCsv Tests
    ' =========================================================================

    <TestMethod>
    Public Sub ParseCsv_WithHeaders_ReturnsDocument()
        Dim csv As String = "name,age,city" & ControlChars.CrLf & _
                           "John,30,New York" & ControlChars.CrLf & _
                           "Jane,25,Los Angeles"
        
        Dim doc As CsvDocument = CsvUtils.ParseCsv(csv)
        
        Assert.AreEqual(3, doc.Headers.Count)
        Assert.AreEqual("name", doc.Headers(0))
        Assert.AreEqual("age", doc.Headers(1))
        Assert.AreEqual("city", doc.Headers(2))
        
        Assert.AreEqual(2, doc.RowCount)
    End Sub

    <TestMethod>
    Public Sub ParseCsv_NoHeaders_ReturnsDocumentWithDefaultHeaders()
        Dim csv As String = "John,30,New York" & ControlChars.CrLf & _
                           "Jane,25,Los Angeles"
        
        Dim opts As New CsvOptions With { .HasHeader = False }
        Dim doc As CsvDocument = CsvUtils.ParseCsv(csv, opts)
        
        Assert.AreEqual(2, doc.RowCount)
        Assert.AreEqual("Column1", doc.Headers(0))
        Assert.AreEqual("Column2", doc.Headers(1))
        Assert.AreEqual("Column3", doc.Headers(2))
    End Sub

    <TestMethod>
    Public Sub ParseCsv_EmptyContent_ReturnsEmptyDocument()
        Dim doc As CsvDocument = CsvUtils.ParseCsv(String.Empty)
        
        Assert.AreEqual(0, doc.RowCount)
        Assert.AreEqual(0, doc.ColumnCount)
    End Sub

    <TestMethod>
    Public Sub ParseCsv_GetValue_ReturnsCorrectValue()
        Dim csv As String = "name,age" & ControlChars.CrLf & _
                           "John,30" & ControlChars.CrLf & _
                           "Jane,25"
        
        Dim doc As CsvDocument = CsvUtils.ParseCsv(csv)
        
        Assert.AreEqual("John", doc.GetValue(0, "name"))
        Assert.AreEqual("30", doc.GetValue(0, "age"))
        Assert.AreEqual("Jane", doc.GetValue(1, "name"))
        Assert.AreEqual("25", doc.GetValue(1, "age"))
    End Sub

    ' =========================================================================
    ' GenerateCsv Tests
    ' =========================================================================

    <TestMethod>
    Public Sub GenerateCsv_FromDocument_ReturnsCorrectFormat()
        Dim doc As New CsvDocument({"name", "age"})
        doc.AddRow({"John", "30"})
        doc.AddRow({"Jane", "25"})
        
        Dim csv As String = CsvUtils.GenerateCsv(doc)
        
        Assert.IsTrue(csv.StartsWith("name,age"))
        Assert.IsTrue(csv.Contains("John,30"))
        Assert.IsTrue(csv.Contains("Jane,25"))
    End Sub

    <TestMethod>
    Public Sub GenerateCsv_EmptyDocument_ReturnsEmptyString()
        Dim doc As New CsvDocument()
        Dim csv As String = CsvUtils.GenerateCsv(doc)
        
        Assert.AreEqual(String.Empty, csv)
    End Sub

    <TestMethod>
    Public Sub GenerateCsv_RoundTripPreservesData()
        Dim original As String = "name,age" & ControlChars.CrLf & _
                                 "John,30" & ControlChars.CrLf & _
                                 "Jane,25"
        
        Dim doc As CsvDocument = CsvUtils.ParseCsv(original)
        Dim generated As String = CsvUtils.GenerateCsv(doc)
        
        ' Parse again and compare
        Dim doc2 As CsvDocument = CsvUtils.ParseCsv(generated)
        
        Assert.AreEqual(doc.RowCount, doc2.RowCount)
        Assert.AreEqual(doc.ColumnCount, doc2.ColumnCount)
        Assert.AreEqual(doc.GetValue(0, "name"), doc2.GetValue(0, "name"))
    End Sub

    ' =========================================================================
    ' EscapeField/UnescapeField Tests
    ' =========================================================================

    <TestMethod>
    Public Sub EscapeField_SimpleValue_ReturnsUnquoted()
        Dim escaped As String = CsvUtils.EscapeField("simple")
        Assert.AreEqual("simple", escaped)
    End Sub

    <TestMethod>
    Public Sub EscapeField_CommaInValue_ReturnsQuoted()
        Dim escaped As String = CsvUtils.EscapeField("a,b")
        Assert.AreEqual("""a,b"", escaped)
    End Sub

    <TestMethod>
    Public Sub EscapeField_QuoteInValue_ReturnsEscaped()
        Dim escaped As String = CsvUtils.EscapeField("a""b")
        Assert.AreEqual("""a""""b"", escaped)
    End Sub

    <TestMethod>
    Public Sub UnescapeField_QuotedValue_ReturnsUnquoted()
        Dim unescaped As String = CsvUtils.UnescapeField("""value""")
        Assert.AreEqual("value", unescaped)
    End Sub

    <TestMethod>
    Public Sub UnescapeField_EscapedQuotes_ReturnsSingleQuote()
        Dim unescaped As String = CsvUtils.UnescapeField("""a""""b""")
        Assert.AreEqual("a""b", unescaped)
    End Sub

    ' =========================================================================
    ' Validation Tests
    ' =========================================================================

    <TestMethod>
    Public Sub ValidateCsvStructure_ConsistentColumns_ReturnsTrue()
        Dim csv As String = "a,b,c" & ControlChars.CrLf & _
                           "1,2,3" & ControlChars.CrLf & _
                           "x,y,z"
        
        Assert.IsTrue(CsvUtils.ValidateCsvStructure(csv))
    End Sub

    <TestMethod>
    Public Sub ValidateCsvStructure_InconsistentColumns_ReturnsFalse()
        Dim csv As String = "a,b,c" & ControlChars.CrLf & _
                           "1,2,3" & ControlChars.CrLf & _
                           "x,y"
        
        Assert.IsFalse(CsvUtils.ValidateCsvStructure(csv))
    End Sub

    <TestMethod>
    Public Sub GetValidationErrors_ValidCsv_ReturnsEmptyList()
        Dim csv As String = "a,b,c" & ControlChars.CrLf & _
                           "1,2,3" & ControlChars.CrLf & _
                           "x,y,z"
        
        Dim errors As List(Of String) = CsvUtils.GetValidationErrors(csv)
        Assert.AreEqual(0, errors.Count)
    End Sub

    <TestMethod>
    Public Sub GetValidationErrors_InvalidCsv_ReturnsErrors()
        Dim csv As String = "a,b,c" & ControlChars.CrLf & _
                           "1,2,3" & ControlChars.CrLf & _
                           "x,y"
        
        Dim errors As List(Of String) = CsvUtils.GetValidationErrors(csv)
        Assert.IsTrue(errors.Count > 0)
    End Sub

    ' =========================================================================
    ' Row Operations Tests
    ' =========================================================================

    <TestMethod>
    Public Sub FilterRows_MatchingPredicate_ReturnsFiltered()
        Dim doc As New CsvDocument({"name", "age"})
        doc.AddRow({"John", "30"})
        doc.AddRow({"Jane", "25"})
        doc.AddRow({"Bob", "35"})
        
        Dim filtered As CsvDocument = CsvUtils.FilterRows(doc, _
            Function(row) Integer.Parse(row("age")) >= 30)
        
        Assert.AreEqual(2, filtered.RowCount)
    End Sub

    <TestMethod>
    Public Sub SortRows_Ascending_ReturnsSorted()
        Dim doc As New CsvDocument({"name", "age"})
        doc.AddRow({"John", "30"})
        doc.AddRow({"Jane", "25"})
        doc.AddRow({"Bob", "35"})
        
        Dim sorted As CsvDocument = CsvUtils.SortRows(doc, "age", True)
        
        Assert.AreEqual("Jane", sorted.GetValue(0, "name"))
        Assert.AreEqual("John", sorted.GetValue(1, "name"))
        Assert.AreEqual("Bob", sorted.GetValue(2, "name"))
    End Sub

    <TestMethod>
    Public Sub SortRows_Descending_ReturnsSorted()
        Dim doc As New CsvDocument({"name", "age"})
        doc.AddRow({"John", "30"})
        doc.AddRow({"Jane", "25"})
        doc.AddRow({"Bob", "35"})
        
        Dim sorted As CsvDocument = CsvUtils.SortRows(doc, "age", False)
        
        Assert.AreEqual("Bob", sorted.GetValue(0, "name"))
        Assert.AreEqual("John", sorted.GetValue(1, "name"))
        Assert.AreEqual("Jane", sorted.GetValue(2, "name"))
    End Sub

    <TestMethod>
    Public Sub GroupRows_ReturnsCorrectGroups()
        Dim doc As New CsvDocument({"name", "city"})
        doc.AddRow({"John", "NYC"})
        doc.AddRow({"Jane", "LA"})
        doc.AddRow({"Bob", "NYC"})
        
        Dim groups As Dictionary(Of String, CsvDocument) = CsvUtils.GroupRows(doc, "city")
        
        Assert.AreEqual(2, groups.Count)
        Assert.AreEqual(2, groups("NYC").RowCount)
        Assert.AreEqual(1, groups("LA").RowCount)
    End Sub

    ' =========================================================================
    ' Column Operations Tests
    ' =========================================================================

    <TestMethod>
    Public Sub AddColumn_ReturnsDocumentWithNewColumn()
        Dim doc As New CsvDocument({"name", "age"})
        doc.AddRow({"John", "30"})
        
        Dim result As CsvDocument = CsvUtils.AddColumn(doc, "city", "Unknown")
        
        Assert.AreEqual(3, result.ColumnCount)
        Assert.AreEqual("Unknown", result.GetValue(0, "city"))
    End Sub

    <TestMethod>
    Public Sub RemoveColumn_ReturnsDocumentWithoutColumn()
        Dim doc As New CsvDocument({"name", "age", "city"})
        doc.AddRow({"John", "30", "NYC"})
        
        Dim result As CsvDocument = CsvUtils.RemoveColumn(doc, "age")
        
        Assert.AreEqual(2, result.ColumnCount)
        Assert.IsFalse(result.Headers.Contains("age"))
    End Sub

    <TestMethod>
    Public Sub RenameColumn_ReturnsDocumentWithRenamedColumn()
        Dim doc As New CsvDocument({"name", "age"})
        doc.AddRow({"John", "30"})
        
        Dim result As CsvDocument = CsvUtils.RenameColumn(doc, "age", "years")
        
        Assert.IsTrue(result.Headers.Contains("years"))
        Assert.IsFalse(result.Headers.Contains("age"))
        Assert.AreEqual("30", result.GetValue(0, "years"))
    End Sub

    <TestMethod>
    Public Sub GetUniqueValues_ReturnsDistinctValues()
        Dim doc As New CsvDocument({"name", "city"})
        doc.AddRow({"John", "NYC"})
        doc.AddRow({"Jane", "LA"})
        doc.AddRow({"Bob", "NYC"})
        
        Dim unique As List(Of String) = CsvUtils.GetUniqueValues(doc, "city")
        
        Assert.AreEqual(2, unique.Count)
        Assert.IsTrue(unique.Contains("NYC"))
        Assert.IsTrue(unique.Contains("LA"))
    End Sub

    <TestMethod>
    Public Sub GetColumnValues_ReturnsAllValues()
        Dim doc As New CsvDocument({"name", "city"})
        doc.AddRow({"John", "NYC"})
        doc.AddRow({"Jane", "LA"})
        doc.AddRow({"Bob", "NYC"})
        
        Dim values As List(Of String) = CsvUtils.GetColumnValues(doc, "name")
        
        Assert.AreEqual(3, values.Count)
        Assert.AreEqual("John", values(0))
        Assert.AreEqual("Jane", values(1))
        Assert.AreEqual("Bob", values(2))
    End Sub

    ' =========================================================================
    ' Statistics Tests
    ' =========================================================================

    <TestMethod>
    Public Sub CountRows_ReturnsCorrectCount()
        Dim csv As String = "name,age" & ControlChars.CrLf & _
                           "John,30" & ControlChars.CrLf & _
                           "Jane,25"
        
        Assert.AreEqual(2, CsvUtils.CountRows(csv))
    End Sub

    <TestMethod>
    Public Sub CountColumns_ReturnsCorrectCount()
        Dim csv As String = "name,age,city" & ControlChars.CrLf & _
                           "John,30,NYC"
        
        Assert.AreEqual(3, CsvUtils.CountColumns(csv))
    End Sub

    <TestMethod>
    Public Sub GetCsvStatistics_ReturnsCorrectStats()
        Dim csv As String = "name,age" & ControlChars.CrLf & _
                           "John,30" & ControlChars.CrLf & _
                           "Jane,25"
        
        Dim stats As Dictionary(Of String, Object) = CsvUtils.GetCsvStatistics(csv)
        
        Assert.AreEqual(2, stats("rows"))
        Assert.AreEqual(2, stats("columns"))
        Assert.IsTrue(stats("valid"))
    End Sub

    ' =========================================================================
    ' Transformation Tests
    ' =========================================================================

    <TestMethod>
    Public Sub ParseToArray_ReturnsCorrectArray()
        Dim csv As String = "a,b,c" & ControlChars.CrLf & _
                           "1,2,3" & ControlChars.CrLf & _
                           "x,y,z"
        
        Dim arr As String()() = CsvUtils.ParseToArray(csv)
        
        Assert.AreEqual(3, arr.Length)
        Assert.AreEqual(3, arr(0).Length)
    End Sub

    <TestMethod>
    Public Sub GenerateFromArray_ReturnsCorrectCsv()
        Dim data As String()() = {
            {"John", "30"},
            {"Jane", "25"}
        }
        
        Dim headers As String() = {"name", "age"}
        Dim csv As String = CsvUtils.GenerateFromArray(data, headers)
        
        Assert.IsTrue(csv.StartsWith("name,age"))
    End Sub

    <TestMethod>
    Public Sub ToArrayList_ReturnsCorrectList()
        Dim doc As New CsvDocument({"name", "age"})
        doc.AddRow({"John", "30"})
        doc.AddRow({"Jane", "25"})
        
        Dim list As List(Of String()) = CsvUtils.ToArrayList(doc, True)
        
        Assert.AreEqual(3, list.Count)  ' Header + 2 rows
    End Sub

    <TestMethod>
    Public Sub FromDictionaryList_ReturnsCorrectDocument()
        Dim data As New List(Of Dictionary(Of String, String))()
        data.Add(New Dictionary(Of String, String) From { {"name", "John"}, {"age", "30"} })
        data.Add(New Dictionary(Of String, String) From { {"name", "Jane"}, {"age", "25"} })
        
        Dim doc As CsvDocument = CsvUtils.FromDictionaryList(data)
        
        Assert.AreEqual(2, doc.RowCount)
        Assert.AreEqual(2, doc.ColumnCount)
    End Sub

    ' =========================================================================
    ' CsvDocument Tests
    ' =========================================================================

    <TestMethod>
    Public Sub CsvDocument_AddRow_IncreasesRowCount()
        Dim doc As New CsvDocument({"name", "age"})
        doc.AddRow({"John", "30"})
        doc.AddRow({"Jane", "25"})
        
        Assert.AreEqual(2, doc.RowCount)
    End Sub

    <TestMethod>
    Public Sub CsvDocument_SetValue_ChangesValue()
        Dim doc As New CsvDocument({"name", "age"})
        doc.AddRow({"John", "30"})
        
        doc.SetValue(0, "age", "35")
        
        Assert.AreEqual("35", doc.GetValue(0, "age"))
    End Sub

    ' =========================================================================
    ' CsvOptions Tests
    ' =========================================================================

    <TestMethod>
    Public Sub CsvOptions_Default_HasCorrectDefaults()
        Dim opts As CsvOptions = CsvOptions.Default()
        
        Assert.AreEqual(","c, opts.Delimiter)
        Assert.AreEqual("""", opts.EscapeChar.ToString())
        Assert.IsTrue(opts.HasHeader)
    End Sub

    <TestMethod>
    Public Sub CsvOptions_TSV_HasTabDelimiter()
        Dim opts As CsvOptions = CsvOptions.TSV()
        
        Assert.AreEqual(ControlChars.Tab, opts.Delimiter)
    End Sub

    <TestMethod>
    Public Sub CsvOptions_PSV_HasPipeDelimiter()
        Dim opts As CsvOptions = CsvOptions.PSV()
        
        Assert.AreEqual("|"c, opts.Delimiter)
    End Sub

End Class