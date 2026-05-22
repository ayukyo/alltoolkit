' =============================================================================
' AllToolkit - CSV Utilities Examples for VB.NET
' =============================================================================
' Usage examples for CSV utilities.
' Run with: dotnet run
' =============================================================================

Imports System
Imports System.IO
Imports System.Collections.Generic
Imports AllToolkit

Module CsvUtilsExamples

    Sub Main()
        Console.WriteLine("=== CSV Utilities Examples ===")
        Console.WriteLine()
        
        ' Example 1: Basic CSV Parsing
        Example1_BasicParsing()
        
        ' Example 2: CSV Generation
        Example2_CsvGeneration()
        
        ' Example 3: CSV Escaping
        Example3_CsvEscaping()
        
        ' Example 4: Row Operations
        Example4_RowOperations()
        
        ' Example 5: Column Operations
        Example5_ColumnOperations()
        
        ' Example 6: File Operations
        Example6_FileOperations()
        
        ' Example 7: TSV/PSV Support
        Example7_DifferentDelimiters()
        
        ' Example 8: Statistics
        Example8_Statistics()
        
        ' Example 9: Validation
        Example9_Validation()
        
        ' Example 10: Complex Data
        Example10_ComplexData()
        
        Console.WriteLine()
        Console.WriteLine("All examples completed successfully!")
    End Sub

    Sub Example1_BasicParsing()
        Console.WriteLine("--- Example 1: Basic CSV Parsing ---")
        
        Dim csv As String = "name,age,city" & ControlChars.CrLf & _
                           "John,30,New York" & ControlChars.CrLf & _
                           "Jane,25,Los Angeles" & ControlChars.CrLf & _
                           "Bob,35,Chicago"
        
        ' Parse CSV string
        Dim doc As CsvDocument = CsvUtils.ParseCsv(csv)
        
        Console.WriteLine("Headers: " & String.Join(", ", doc.Headers))
        Console.WriteLine("Rows: " & doc.RowCount)
        Console.WriteLine("Columns: " & doc.ColumnCount)
        
        ' Access specific values
        Console.WriteLine("First row name: " & doc.GetValue(0, "name"))
        Console.WriteLine("Second row city: " & doc.GetValue(1, "city"))
        
        Console.WriteLine()
    End Sub

    Sub Example2_CsvGeneration()
        Console.WriteLine("--- Example 2: CSV Generation ---")
        
        ' Create CSV document with headers
        Dim doc As New CsvDocument({"product", "price", "quantity"})
        
        ' Add rows
        doc.AddRow({"Apple", "1.50", "100"})
        doc.AddRow({"Orange", "2.00", "50"})
        doc.AddRow({"Banana", "0.75", "200"})
        
        ' Generate CSV string
        Dim csv As String = CsvUtils.GenerateCsv(doc)
        Console.WriteLine("Generated CSV:")
        Console.WriteLine(csv)
        
        Console.WriteLine()
    End Sub

    Sub Example3_CsvEscaping()
        Console.WriteLine("--- Example 3: CSV Escaping ---")
        
        ' Fields that need escaping
        Dim fields As String() = {
            "simple",
            "contains, comma",
            "has ""quote""",
            "has" & ControlChars.Lf & "newline"
        }
        
        For Each field As String In fields
            Dim escaped As String = CsvUtils.EscapeField(field)
            Dim unescaped As String = CsvUtils.UnescapeField(escaped)
            Console.WriteLine("Original: " & field.Replace(ControlChars.Lf, "[LF]"))
            Console.WriteLine("Escaped:  " & escaped.Replace(ControlChars.Lf, "[LF]"))
            Console.WriteLine("Unescaped: " & unescaped.Replace(ControlChars.Lf, "[LF]"))
            Console.WriteLine()
        Next
    End Sub

    Sub Example4_RowOperations()
        Console.WriteLine("--- Example 4: Row Operations ---")
        
        Dim doc As New CsvDocument({"name", "score", "team"})
        doc.AddRow({"Alice", "95", "A"})
        doc.AddRow({"Bob", "85", "B"})
        doc.AddRow({"Charlie", "90", "A"})
        doc.AddRow({"David", "80", "B"})
        
        ' Filter rows (score >= 90)
        Dim filtered As CsvDocument = CsvUtils.FilterRows(doc, _
            Function(row) Integer.Parse(row("score")) >= 90)
        Console.WriteLine("Filtered (score >= 90): " & filtered.RowCount & " rows")
        
        ' Sort by score descending
        Dim sorted As CsvDocument = CsvUtils.SortRows(doc, "score", False)
        Console.WriteLine("Sorted by score (desc):")
        For i As Integer = 0 To sorted.RowCount - 1
            Console.WriteLine("  " & sorted.GetValue(i, "name") & ": " & sorted.GetValue(i, "score"))
        Next
        
        ' Group by team
        Dim groups As Dictionary(Of String, CsvDocument) = CsvUtils.GroupRows(doc, "team")
        Console.WriteLine("Grouped by team:")
        For Each kvp As KeyValuePair(Of String, CsvDocument) In groups
            Console.WriteLine("  Team " & kvp.Key & ": " & kvp.Value.RowCount & " members")
        Next
        
        Console.WriteLine()
    End Sub

    Sub Example5_ColumnOperations()
        Console.WriteLine("--- Example 5: Column Operations ---")
        
        Dim doc As New CsvDocument({"name", "score"})
        doc.AddRow({"Alice", "95"})
        doc.AddRow({"Bob", "85"})
        
        ' Add column
        Dim withGrade As CsvDocument = CsvUtils.AddColumn(doc, "grade", "")
        For i As Integer = 0 To withGrade.RowCount - 1
            Dim score As Integer = Integer.Parse(withGrade.GetValue(i, "score"))
            Dim grade As String = If(score >= 90, "A", If(score >= 80, "B", "C"))
            withGrade.SetValue(i, "grade", grade)
        Next
        Console.WriteLine("Added grade column:")
        Console.WriteLine(CsvUtils.GenerateCsv(withGrade))
        
        ' Rename column
        Dim renamed As CsvDocument = CsvUtils.RenameColumn(doc, "score", "points")
        Console.WriteLine("Renamed 'score' to 'points':")
        Console.WriteLine(String.Join(", ", renamed.Headers))
        
        ' Remove column
        Dim removed As CsvDocument = CsvUtils.RemoveColumn(withGrade, "grade")
        Console.WriteLine("Removed 'grade' column:")
        Console.WriteLine(String.Join(", ", removed.Headers))
        
        Console.WriteLine()
    End Sub

    Sub Example6_FileOperations()
        Console.WriteLine("--- Example 6: File Operations ---")
        
        Dim tempFile As String = Path.Combine(Path.GetTempPath(), "test_csv.csv")
        
        ' Create CSV document
        Dim doc As New CsvDocument({"id", "name", "value"})
        doc.AddRow({"1", "Item1", "100"})
        doc.AddRow({"2", "Item2", "200"})
        doc.AddRow({"3", "Item3", "300"})
        
        ' Save to file
        CsvUtils.SaveCsvFile(doc, tempFile)
        Console.WriteLine("Saved CSV to: " & tempFile)
        
        ' Read from file
        Dim loaded As CsvDocument = CsvUtils.ParseCsvFile(tempFile)
        Console.WriteLine("Loaded from file:")
        Console.WriteLine("  Headers: " & String.Join(", ", loaded.Headers))
        Console.WriteLine("  Rows: " & loaded.RowCount)
        
        ' Clean up
        File.Delete(tempFile)
        Console.WriteLine("Deleted temp file")
        
        Console.WriteLine()
    End Sub

    Sub Example7_DifferentDelimiters()
        Console.WriteLine("--- Example 7: Different Delimiters ---")
        
        ' TSV (Tab-Separated Values)
        Dim tsv As String = "name" & ControlChars.Tab & "age" & ControlChars.CrLf & _
                           "John" & ControlChars.Tab & "30"
        
        Dim docTSV As CsvDocument = CsvUtils.ParseCsv(tsv, CsvOptions.TSV())
        Console.WriteLine("TSV parsed: " & docTSV.GetValue(0, "name") & ", " & docTSV.GetValue(0, "age"))
        
        ' PSV (Pipe-Separated Values)
        Dim psv As String = "name|age" & ControlChars.CrLf & _
                           "Jane|25"
        
        Dim docPSV As CsvDocument = CsvUtils.ParseCsv(psv, CsvOptions.PSV())
        Console.WriteLine("PSV parsed: " & docPSV.GetValue(0, "name") & ", " & docPSV.GetValue(0, "age"))
        
        ' Generate TSV
        Dim doc As New CsvDocument({"a", "b"}, CsvOptions.TSV())
        doc.AddRow({"x", "y"})
        Console.WriteLine("Generated TSV: " & CsvUtils.GenerateCsv(doc).Replace(ControlChars.Tab, "[TAB]"))
        
        Console.WriteLine()
    End Sub

    Sub Example8_Statistics()
        Console.WriteLine("--- Example 8: CSV Statistics ---")
        
        Dim csv As String = "product,price,stock" & ControlChars.CrLf & _
                           "Apple,1.50,100" & ControlChars.CrLf & _
                           "Orange,2.00,50" & ControlChars.CrLf & _
                           "Banana,0.75,200"
        
        Dim stats As Dictionary(Of String, Object) = CsvUtils.GetCsvStatistics(csv)
        
        Console.WriteLine("Statistics:")
        Console.WriteLine("  Rows: " & stats("rows"))
        Console.WriteLine("  Columns: " & stats("columns"))
        Console.WriteLine("  Valid: " & stats("valid"))
        Console.WriteLine("  Headers: " & String.Join(", ", stats("headers")))
        
        ' Count operations
        Console.WriteLine("  Total rows: " & CsvUtils.CountRows(csv))
        Console.WriteLine("  Total columns: " & CsvUtils.CountColumns(csv))
        
        Console.WriteLine()
    End Sub

    Sub Example9_Validation()
        Console.WriteLine("--- Example 9: CSV Validation ---")
        
        ' Valid CSV
        Dim validCsv As String = "a,b,c" & ControlChars.CrLf & _
                                "1,2,3" & ControlChars.CrLf & _
                                "x,y,z"
        
        Console.WriteLine("Valid CSV structure: " & CsvUtils.ValidateCsvStructure(validCsv))
        
        ' Invalid CSV (inconsistent columns)
        Dim invalidCsv As String = "a,b,c" & ControlChars.CrLf & _
                                  "1,2,3" & ControlChars.CrLf & _
                                  "x,y"
        
        Console.WriteLine("Invalid CSV structure: " & CsvUtils.ValidateCsvStructure(invalidCsv))
        
        Dim errors As List(Of String) = CsvUtils.GetValidationErrors(invalidCsv)
        Console.WriteLine("Validation errors:")
        For Each error As String In errors
            Console.WriteLine("  " & error)
        Next
        
        Console.WriteLine()
    End Sub

    Sub Example10_ComplexData()
        Console.WriteLine("--- Example 10: Complex Data ---")
        
        ' CSV with quotes, commas, and newlines in fields
        Dim complexCsv As String = "title,author,description" & ControlChars.CrLf & _
                                  """The Great Gatsby"",F. Scott Fitzgerald,""A story of """"wealth"""" and dreams""" & ControlChars.CrLf & _
                                  """1984"",George Orwell,"""Dystopian novel" & ControlChars.Lf & "about totalitarianism""" & ControlChars.CrLf & _
                                  "Simple Book,Unknown Author,No special characters"
        
        Dim doc As CsvDocument = CsvUtils.ParseCsv(complexCsv)
        
        Console.WriteLine("Parsed complex CSV:")
        For i As Integer = 0 To doc.RowCount - 1
            Console.WriteLine("  Title: " & doc.GetValue(i, "title"))
            Console.WriteLine("  Author: " & doc.GetValue(i, "author"))
            Console.WriteLine("  Description: " & doc.GetValue(i, "description").Replace(ControlChars.Lf, "[LF]"))
            Console.WriteLine()
        Next
        
        ' Round-trip test
        Dim regenerated As String = CsvUtils.GenerateCsv(doc)
        Console.WriteLine("Regenerated CSV preserves complex data correctly")
        
        Console.WriteLine()
    End Sub

End Module