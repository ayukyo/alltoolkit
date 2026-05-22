' =============================================================================
' AllToolkit - CSV Utilities for VB.NET
' =============================================================================
' A comprehensive CSV (Comma-Separated Values) utility library for VB.NET.
' Zero dependencies - uses only .NET standard library.
'
' Features:
' - CSV parsing (parse lines, parse files)
' - CSV generation (generate lines, generate files)
' - CSV escaping and unescaping (RFC 4180 compliant)
' - CSV validation (check format, check structure)
' - CSV transformation (convert to/from arrays, dictionaries)
' - CSV filtering and sorting
' - CSV column operations (add, remove, rename)
' - CSV row operations (filter, sort, group)
' =============================================================================

Imports System
Imports System.IO
Imports System.Text
Imports System.Collections.Generic
Imports System.Linq

Namespace AllToolkit

    ''' <summary>
    ''' Options for CSV parsing and generation.
    ''' </summary>
    Public Class CsvOptions
        ''' <summary>Field delimiter character (default: comma).</summary>
        Public Property Delimiter As Char = ","c
        
        ''' <summary>Quote character for fields (default: double-quote).</summary>
        Public Property QuoteChar As Char = """"
        
        ''' <summary>Character to escape quotes within quoted fields (default: double-quote).</summary>
        Public Property EscapeChar As Char = """"
        
        ''' <summary>Whether the CSV has a header row (default: True).</summary>
        Public Property HasHeader As Boolean = True
        
        ''' <summary>Newline character sequence (default: Environment.NewLine).</summary>
        Public Property NewLine As String = Environment.NewLine
        
        ''' <summary>Whether to trim whitespace from fields (default: False).</summary>
        Public Property TrimFields As Boolean = False
        
        ''' <summary>Whether to skip empty lines (default: True).</summary>
        Public Property SkipEmptyLines As Boolean = True
        
        ''' <summary>Encoding for file operations (default: UTF-8).</summary>
        Public Property Encoding As Encoding = Encoding.UTF8
        
        ''' <summary>Creates default CSV options.</summary>
        Public Shared Function Default() As CsvOptions
            Return New CsvOptions()
        End Function
        
        ''' <summary>Creates CSV options for tab-separated values.</summary>
        Public Shared Function TSV() As CsvOptions
            Return New CsvOptions With { .Delimiter = ControlChars.Tab }
        End Function
        
        ''' <summary>Creates CSV options for pipe-separated values.</summary>
        Public Shared Function PSV() As CsvOptions
            Return New CsvOptions With { .Delimiter = "|"c }
        End Function
    End Class

    ''' <summary>
    ''' Represents a CSV document with headers and rows.
    ''' </summary>
    Public Class CsvDocument
        ''' <summary>Header row (column names).</summary>
        Public Property Headers As List(Of String)
        
        ''' <summary>Data rows (each row is a dictionary mapping header to value).</summary>
        Public Property Rows As List(Of Dictionary(Of String, String))
        
        ''' <summary>Options used to parse/generate this CSV.</summary>
        Public Property Options As CsvOptions
        
        ''' <summary>Number of columns.</summary>
        Public ReadOnly Property ColumnCount As Integer
            Get
                Return If(Headers, New List(Of String)).Count
            End Get
        End Property
        
        ''' <summary>Number of data rows (excluding header).</summary>
        Public ReadOnly Property RowCount As Integer
            Get
                Return If(Rows, New List(Of Dictionary(Of String, String))).Count
            End Get
        End Property
        
        ''' <summary>Creates an empty CSV document.</summary>
        Public Sub New(Optional options As CsvOptions = Nothing)
            Me.Headers = New List(Of String)()
            Me.Rows = New List(Of Dictionary(Of String, String))()
            Me.Options = If(options, CsvOptions.Default())
        End Sub
        
        ''' <summary>Creates a CSV document with headers.</summary>
        Public Sub New(headers As IEnumerable(Of String), Optional options As CsvOptions = Nothing)
            Me.Headers = New List(Of String)(headers)
            Me.Rows = New List(Of Dictionary(Of String, String))()
            Me.Options = If(options, CsvOptions.Default())
        End Sub
        
        ''' <summary>Gets a column value by header name and row index.</summary>
        Public Function GetValue(rowIndex As Integer, headerName As String) As String
            If rowIndex < 0 OrElse rowIndex >= Rows.Count Then Return Nothing
            If Not Headers.Contains(headerName) Then Return Nothing
            
            If Rows(rowIndex).ContainsKey(headerName) Then
                Return Rows(rowIndex)(headerName)
            End If
            
            Return Nothing
        End Function
        
        ''' <summary>Sets a column value by header name and row index.</summary>
        Public Sub SetValue(rowIndex As Integer, headerName As String, value As String)
            If rowIndex < 0 OrElse rowIndex >= Rows.Count Then Return
            If Not Headers.Contains(headerName) Then Return
            
            Rows(rowIndex)(headerName) = value
        End Function
        
        ''' <summary>Adds a new row with values.</summary>
        Public Sub AddRow(values As IEnumerable(Of String))
            If values Is Nothing Then Return
            
            Dim row As New Dictionary(Of String, String)()
            Dim valueList As List(Of String) = values.ToList()
            
            For i As Integer = 0 To Math.Min(Headers.Count - 1, valueList.Count - 1)
                row(Headers(i)) = valueList(i)
            Next
            
            ' Fill remaining headers with empty values
            For i As Integer = valueList.Count To Headers.Count - 1
                row(Headers(i)) = String.Empty
            Next
            
            Rows.Add(row)
        End Sub
        
        ''' <summary>Adds a new row as a dictionary.</summary>
        Public Sub AddRow(row As Dictionary(Of String, String))
            If row Is Nothing Then Return
            Rows.Add(row)
        End Sub
    End Class

    ''' <summary>
    ''' Comprehensive CSV utilities for VB.NET.
    ''' </summary>
    Public Module CsvUtils

        ' =========================================================================
        ' CSV Parsing
        ' =========================================================================

        ''' <summary>
        ''' Parses a CSV string into a CsvDocument.
        ''' </summary>
        ''' <param name="csvContent">CSV string content.</param>
        ''' <param name="options">CSV parsing options.</param>
        ''' <returns>CsvDocument with headers and rows.</returns>
        Public Function ParseCsv(csvContent As String, Optional options As CsvOptions = Nothing) As CsvDocument
            If String.IsNullOrEmpty(csvContent) Then Return New CsvDocument(options)
            
            Dim opts As CsvOptions = If(options, CsvOptions.Default())
            Dim lines As String() = SplitLines(csvContent, opts)
            
            If lines.Length = 0 Then Return New CsvDocument(options)
            
            Dim doc As New CsvDocument(options)
            
            ' Parse header row if enabled
            Dim startIndex As Integer = 0
            If opts.HasHeader AndAlso lines.Length > 0 Then
                doc.Headers = ParseLine(lines(0), opts)
                startIndex = 1
            Else
                ' Generate default headers based on first row
                Dim firstRowFields As List(Of String) = ParseLine(lines(0), opts)
                For i As Integer = 0 To firstRowFields.Count - 1
                    doc.Headers.Add("Column" & (i + 1))
                Next
            End If
            
            ' Parse data rows
            For i As Integer = startIndex To lines.Length - 1
                Dim fields As List(Of String) = ParseLine(lines(i), opts)
                Dim row As New Dictionary(Of String, String)()
                
                For j As Integer = 0 To doc.Headers.Count - 1
                    If j < fields.Count Then
                        row(doc.Headers(j)) = fields(j)
                    Else
                        row(doc.Headers(j)) = String.Empty
                    End If
                Next
                
                doc.Rows.Add(row)
            Next
            
            Return doc
        End Function

        ''' <summary>
        ''' Parses a single CSV line into fields.
        ''' </summary>
        ''' <param name="line">CSV line to parse.</param>
        ''' <param name="options">CSV parsing options.</param>
        ''' <returns>List of field values.</returns>
        Public Function ParseLine(line As String, Optional options As CsvOptions = Nothing) As List(Of String)
            Dim fields As New List(Of String)()
            
            If String.IsNullOrEmpty(line) Then Return fields
            
            Dim opts As CsvOptions = If(options, CsvOptions.Default())
            Dim currentField As New StringBuilder()
            Dim inQuotes As Boolean = False
            Dim i As Integer = 0
            
            While i < line.Length
                Dim c As Char = line(i)
                
                If inQuotes Then
                    ' Inside quoted field
                    If c = opts.EscapeChar AndAlso i + 1 < line.Length AndAlso line(i + 1) = opts.EscapeChar Then
                        ' Escaped quote (double-quote)
                        currentField.Append(opts.EscapeChar)
                        i += 2
                        Continue While
                    ElseIf c = opts.EscapeChar Then
                        ' End of quoted field
                        inQuotes = False
                        i += 1
                        Continue While
                    Else
                        currentField.Append(c)
                        i += 1
                    End If
                Else
                    ' Outside quoted field
                    If c = opts.EscapeChar Then
                        ' Start of quoted field
                        inQuotes = True
                        i += 1
                    ElseIf c = opts.Delimiter Then
                        ' Field separator
                        Dim fieldValue As String = currentField.ToString()
                        If opts.TrimFields Then fieldValue = fieldValue.Trim()
                        fields.Add(fieldValue)
                        currentField.Clear()
                        i += 1
                    Else
                        currentField.Append(c)
                        i += 1
                    End If
                End If
            End While
            
            ' Add last field
            Dim lastField As String = currentField.ToString()
            If opts.TrimFields Then lastField = lastField.Trim()
            fields.Add(lastField)
            
            Return fields
        End Function

        ''' <summary>
        ''' Parses a CSV file into a CsvDocument.
        ''' </summary>
        ''' <param name="filePath">Path to CSV file.</param>
        ''' <param name="options">CSV parsing options.</param>
        ''' <returns>CsvDocument with headers and rows.</returns>
        Public Function ParseCsvFile(filePath As String, Optional options As CsvOptions = Nothing) As CsvDocument
            If String.IsNullOrEmpty(filePath) OrElse Not File.Exists(filePath) Then
                Return New CsvDocument(options)
            End If
            
            Dim opts As CsvOptions = If(options, CsvOptions.Default())
            Dim content As String = File.ReadAllText(filePath, opts.Encoding)
            Return ParseCsv(content, opts)
        End Function

        ''' <summary>
        ''' Parses CSV into a 2D array (without headers).
        ''' </summary>
        ''' <param name="csvContent">CSV string content.</param>
        ''' <param name="options">CSV parsing options.</param>
        ''' <returns>2D array of string values.</returns>
        Public Function ParseToArray(csvContent As String, Optional options As CsvOptions = Nothing) As String()()
            If String.IsNullOrEmpty(csvContent) Then Return New String()(){}
            
            Dim opts As CsvOptions = If(options, CsvOptions.Default())
            opts.HasHeader = False ' No headers for array output
            
            Dim lines As String() = SplitLines(csvContent, opts)
            Dim result As New List(Of String())()
            
            For Each line As String In lines
                result.Add(ParseLine(line, opts).ToArray())
            Next
            
            Return result.ToArray()
        End Function

        ' =========================================================================
        ' CSV Generation
        ' =========================================================================

        ''' <summary>
        ''' Generates a CSV string from a CsvDocument.
        ''' </summary>
        ''' <param name="doc">CsvDocument to convert.</param>
        ''' <returns>CSV string.</returns>
        Public Function GenerateCsv(doc As CsvDocument) As String
            If doc Is Nothing Then Return String.Empty
            
            Dim sb As New StringBuilder()
            
            ' Write header row
            If doc.Options.HasHeader AndAlso doc.Headers.Count > 0 Then
                sb.Append(GenerateLine(doc.Headers, doc.Options))
                sb.Append(doc.Options.NewLine)
            End If
            
            ' Write data rows
            For Each row As Dictionary(Of String, String) In doc.Rows
                Dim values As New List(Of String)()
                For Each header As String In doc.Headers
                    If row.ContainsKey(header) Then
                        values.Add(row(header))
                    Else
                        values.Add(String.Empty)
                    End If
                Next
                
                sb.Append(GenerateLine(values, doc.Options))
                sb.Append(doc.Options.NewLine)
            Next
            
            Return sb.ToString()
        End Function

        ''' <summary>
        ''' Generates a single CSV line from field values.
        ''' </summary>
        ''' <param name="fields">Field values.</param>
        ''' <param name="options">CSV generation options.</param>
        ''' <returns>CSV line string.</returns>
        Public Function GenerateLine(fields As IEnumerable(Of String), Optional options As CsvOptions = Nothing) As String
            If fields Is Nothing Then Return String.Empty
            
            Dim opts As CsvOptions = If(options, CsvOptions.Default())
            Dim fieldList As List(Of String) = fields.ToList()
            Dim sb As New StringBuilder()
            
            For i As Integer = 0 To fieldList.Count - 1
                If i > 0 Then sb.Append(opts.Delimiter)
                sb.Append(EscapeField(fieldList(i), opts))
            Next
            
            Return sb.ToString()
        End Function

        ''' <summary>
        ''' Generates CSV from a 2D array.
        ''' </summary>
        ''' <param name="data">2D array of values.</param>
        ''' <param name="headers">Optional header row.</param>
        ''' <param name="options">CSV generation options.</param>
        ''' <returns>CSV string.</returns>
        Public Function GenerateFromArray(data As String()(), Optional headers As String() = Nothing, Optional options As CsvOptions = Nothing) As String
            If data Is Nothing OrElse data.Length = 0 Then Return String.Empty
            
            Dim opts As CsvOptions = If(options, CsvOptions.Default())
            Dim sb As New StringBuilder()
            
            ' Write header row if provided
            If headers IsNot Nothing AndAlso headers.Length > 0 AndAlso opts.HasHeader Then
                sb.Append(GenerateLine(headers, opts))
                sb.Append(opts.NewLine)
            End If
            
            ' Write data rows
            For Each row As String() In data
                sb.Append(GenerateLine(row, opts))
                sb.Append(opts.NewLine)
            Next
            
            Return sb.ToString()
        End Function

        ''' <summary>
        ''' Saves a CsvDocument to a file.
        ''' </summary>
        ''' <param name="doc">CsvDocument to save.</param>
        ''' <param name="filePath">Destination file path.</param>
        Public Sub SaveCsvFile(doc As CsvDocument, filePath As String)
            If doc Is Nothing OrElse String.IsNullOrEmpty(filePath) Then Return
            
            Dim content As String = GenerateCsv(doc)
            File.WriteAllText(filePath, content, doc.Options.Encoding)
        End Sub

        ' =========================================================================
        ' CSV Escaping/Unescaping (RFC 4180 Compliant)
        ' =========================================================================

        ''' <summary>
        ''' Escapes a field value according to RFC 4180.
        ''' </summary>
        ''' <param name="field">Field value to escape.</param>
        ''' <param name="options">CSV options.</param>
        ''' <returns>Escaped field string.</returns>
        Public Function EscapeField(field As String, Optional options As CsvOptions = Nothing) As String
            If String.IsNullOrEmpty(field) Then Return String.Empty
            
            Dim opts As CsvOptions = If(options, CsvOptions.Default())
            
            ' Check if field needs quoting
            Dim needsQuoting As Boolean = _
                field.Contains(opts.Delimiter.ToString()) OrElse
                field.Contains(opts.EscapeChar.ToString()) OrElse
                field.Contains(ControlChars.Lf) OrElse
                field.Contains(ControlChars.Cr) OrElse
                field.Contains(opts.NewLine)
            
            If Not needsQuoting Then Return field
            
            ' Escape quotes by doubling them
            Dim escaped As String = field.Replace(opts.EscapeChar.ToString(), opts.EscapeChar.ToString() & opts.EscapeChar.ToString())
            
            ' Wrap in quotes
            Return opts.EscapeChar.ToString() & escaped & opts.EscapeChar.ToString()
        End Function

        ''' <summary>
        ''' Unescapes a quoted field value.
        ''' </summary>
        ''' <param name="field">Quoted field value.</param>
        ''' <param name="options">CSV options.</param>
        ''' <returns>Unescaped field string.</returns>
        Public Function UnescapeField(field As String, Optional options As CsvOptions = Nothing) As String
            If String.IsNullOrEmpty(field) Then Return String.Empty
            
            Dim opts As CsvOptions = If(options, CsvOptions.Default())
            
            ' Check if field is quoted
            If field.StartsWith(opts.EscapeChar.ToString()) AndAlso field.EndsWith(opts.EscapeChar.ToString()) Then
                ' Remove outer quotes
                Dim inner As String = field.Substring(1, field.Length - 2)
                
                ' Unescape doubled quotes
                Return inner.Replace(opts.EscapeChar.ToString() & opts.EscapeChar.ToString(), opts.EscapeChar.ToString())
            End If
            
            Return field
        End Function

        ' =========================================================================
        ' CSV Validation
        ' =========================================================================

        ''' <summary>
        ''' Validates CSV structure (consistent column count).
        ''' </summary>
        ''' <param name="csvContent">CSV string to validate.</param>
        ''' <param name="options">CSV options.</param>
        ''' <returns>True if CSV has consistent column count.</returns>
        Public Function ValidateCsvStructure(csvContent As String, Optional options As CsvOptions = Nothing) As Boolean
            If String.IsNullOrEmpty(csvContent) Then Return True
            
            Dim opts As CsvOptions = If(options, CsvOptions.Default())
            Dim lines As String() = SplitLines(csvContent, opts)
            
            If lines.Length = 0 Then Return True
            
            ' Get expected column count from first row
            Dim expectedColumns As Integer = ParseLine(lines(0), opts).Count
            Dim startIndex As Integer = If(opts.HasHeader, 1, 0)
            
            ' Check all rows have same column count
            For i As Integer = startIndex To lines.Length - 1
                Dim rowColumns As Integer = ParseLine(lines(i), opts).Count
                If rowColumns <> expectedColumns Then Return False
            Next
            
            Return True
        End Function

        ''' <summary>
        ''' Gets validation errors for CSV.
        ''' </summary>
        ''' <param name="csvContent">CSV string to validate.</param>
        ''' <param name="options">CSV options.</param>
        ''' <returns>List of validation error messages.</returns>
        Public Function GetValidationErrors(csvContent As String, Optional options As CsvOptions = Nothing) As List(Of String)
            Dim errors As New List(Of String)()
            
            If String.IsNullOrEmpty(csvContent) Then Return errors
            
            Dim opts As CsvOptions = If(options, CsvOptions.Default())
            Dim lines As String() = SplitLines(csvContent, opts)
            
            If lines.Length = 0 Then Return errors
            
            ' Get expected column count
            Dim expectedColumns As Integer = ParseLine(lines(0), opts).Count
            Dim startIndex As Integer = If(opts.HasHeader, 1, 0)
            
            ' Check each row
            For i As Integer = startIndex To lines.Length - 1
                Dim rowColumns As Integer = ParseLine(lines(i), opts).Count
                
                If rowColumns <> expectedColumns Then
                    errors.Add(String.Format("Row {0}: Expected {1} columns, found {2}", i + 1, expectedColumns, rowColumns))
                End If
                
                ' Check for unclosed quotes
                Dim quoteCount As Integer = lines(i).Count(Function(c) c = opts.EscapeChar)
                If quoteCount Mod 2 <> 0 Then
                    errors.Add(String.Format("Row {0}: Unclosed quote detected", i + 1))
                End If
            Next
            
            Return errors
        End Function

        ' =========================================================================
        ' CSV Transformation
        ' =========================================================================

        ''' <summary>
        ''' Converts CsvDocument to list of dictionaries.
        ''' </summary>
        ''' <param name="doc">CsvDocument to convert.</param>
        ''' <returns>List of dictionaries (header -> value).</returns>
        Public Function ToDictionaryList(doc As CsvDocument) As List(Of Dictionary(Of String, String))
            If doc Is Nothing Then Return New List(Of Dictionary(Of String, String))()
            Return doc.Rows
        End Function

        ''' <summary>
        ''' Converts CsvDocument to list of arrays.
        ''' </summary>
        ''' <param name="doc">CsvDocument to convert.</param>
        ''' <param name="includeHeader">Include header row as first array.</param>
        ''' <returns>List of string arrays.</returns>
        Public Function ToArrayList(doc As CsvDocument, Optional includeHeader As Boolean = False) As List(Of String())
            Dim result As New List(Of String())()
            
            If doc Is Nothing Then Return result
            
            If includeHeader AndAlso doc.Headers.Count > 0 Then
                result.Add(doc.Headers.ToArray())
            End If
            
            For Each row As Dictionary(Of String, String) In doc.Rows
                Dim values As New List(Of String)()
                For Each header As String In doc.Headers
                    If row.ContainsKey(header) Then
                        values.Add(row(header))
                    Else
                        values.Add(String.Empty)
                    End If
                Next
                result.Add(values.ToArray())
            Next
            
            Return result
        End Function

        ''' <summary>
        ''' Converts list of dictionaries to CsvDocument.
        ''' </summary>
        ''' <param name="data">List of dictionaries.</param>
        ''' <param name="headers">Optional explicit headers (default: infer from data).</param>
        ''' <returns>CsvDocument.</returns>
        Public Function FromDictionaryList(data As List(Of Dictionary(Of String, String)), Optional headers As IEnumerable(Of String) = Nothing) As CsvDocument
            If data Is Nothing OrElse data.Count = 0 Then Return New CsvDocument()
            
            ' Infer headers from first row if not provided
            Dim headerList As List(Of String) = If(headers, data(0).Keys.ToList()).ToList()
            
            Dim doc As New CsvDocument(headerList)
            
            For Each row As Dictionary(Of String, String) In data
                doc.AddRow(row)
            Next
            
            Return doc
        End Function

        ' =========================================================================
        ' CSV Row Operations
        ' =========================================================================

        ''' <summary>
        ''' Filters rows by a predicate.
        ''' </summary>
        ''' <param name="doc">CsvDocument to filter.</param>
        ''' <param name="predicate">Filter predicate function.</param>
        ''' <returns>New CsvDocument with filtered rows.</returns>
        Public Function FilterRows(doc As CsvDocument, predicate As Func(Of Dictionary(Of String, String), Boolean)) As CsvDocument
            If doc Is Nothing OrElse predicate Is Nothing Then Return New CsvDocument()
            
            Dim result As New CsvDocument(doc.Headers, doc.Options)
            
            For Each row As Dictionary(Of String, String) In doc.Rows
                If predicate(row) Then
                    result.AddRow(row)
                End If
            Next
            
            Return result
        End Function

        ''' <summary>
        ''' Sorts rows by a column value.
        ''' </summary>
        ''' <param name="doc">CsvDocument to sort.</param>
        ''' <param name="columnName">Column to sort by.</param>
        ''' <param name="ascending">Sort direction (default: True).</param>
        ''' <returns>New CsvDocument with sorted rows.</returns>
        Public Function SortRows(doc As CsvDocument, columnName As String, Optional ascending As Boolean = True) As CsvDocument
            If doc Is Nothing OrElse Not doc.Headers.Contains(columnName) Then Return doc
            
            Dim result As New CsvDocument(doc.Headers, doc.Options)
            
            Dim sortedRows As IEnumerable(Of Dictionary(Of String, String)) = doc.Rows
            If ascending Then
                sortedRows = sortedRows.OrderBy(Function(r) If(r.ContainsKey(columnName), r(columnName), String.Empty))
            Else
                sortedRows = sortedRows.OrderByDescending(Function(r) If(r.ContainsKey(columnName), r(columnName), String.Empty))
            End If
            
            For Each row As Dictionary(Of String, String) In sortedRows
                result.AddRow(row)
            Next
            
            Return result
        End Function

        ''' <summary>
        ''' Groups rows by a column value.
        ''' </summary>
        ''' <param name="doc">CsvDocument to group.</param>
        ''' <param name="columnName">Column to group by.</param>
        ''' <returns>Dictionary mapping group values to CsvDocuments.</returns>
        Public Function GroupRows(doc As CsvDocument, columnName As String) As Dictionary(Of String, CsvDocument)
            If doc Is Nothing OrElse Not doc.Headers.Contains(columnName) Then
                Return New Dictionary(Of String, CsvDocument)()
            End If
            
            Dim groups As New Dictionary(Of String, CsvDocument)()
            
            For Each row As Dictionary(Of String, String) In doc.Rows
                Dim groupKey As String = If(row.ContainsKey(columnName), row(columnName), String.Empty)
                
                If Not groups.ContainsKey(groupKey) Then
                    groups(groupKey) = New CsvDocument(doc.Headers, doc.Options)
                End If
                
                groups(groupKey).AddRow(row)
            Next
            
            Return groups
        End Function

        ''' <summary>
        ''' Removes rows matching a predicate.
        ''' </summary>
        ''' <param name="doc">CsvDocument to modify.</param>
        ''' <param name="predicate">Predicate for rows to remove.</param>
        ''' <returns>New CsvDocument without removed rows.</returns>
        Public Function RemoveRows(doc As CsvDocument, predicate As Func(Of Dictionary(Of String, String), Boolean)) As CsvDocument
            If doc Is Nothing OrElse predicate Is Nothing Then Return New CsvDocument()
            
            Return FilterRows(doc, Function(row) Not predicate(row))
        End Function

        ' =========================================================================
        ' CSV Column Operations
        ' =========================================================================

        ''' <summary>
        ''' Adds a new column with default value.
        ''' </summary>
        ''' <param name="doc">CsvDocument to modify.</param>
        ''' <param name="columnName">New column name.</param>
        ''' <param name="defaultValue">Default value for existing rows.</param>
        ''' <returns>New CsvDocument with added column.</returns>
        Public Function AddColumn(doc As CsvDocument, columnName As String, Optional defaultValue As String = "") As CsvDocument
            If doc Is Nothing OrElse String.IsNullOrEmpty(columnName) Then Return doc
            If doc.Headers.Contains(columnName) Then Return doc
            
            Dim result As New CsvDocument(doc.Headers.ToList(), doc.Options)
            result.Headers.Add(columnName)
            
            For Each row As Dictionary(Of String, String) In doc.Rows
                Dim newRow As New Dictionary(Of String, String)(row)
                newRow(columnName) = defaultValue
                result.AddRow(newRow)
            Next
            
            Return result
        End Function

        ''' <summary>
        ''' Removes a column.
        ''' </summary>
        ''' <param name="doc">CsvDocument to modify.</param>
        ''' <param name="columnName">Column name to remove.</param>
        ''' <returns>New CsvDocument without the column.</returns>
        Public Function RemoveColumn(doc As CsvDocument, columnName As String) As CsvDocument
            If doc Is Nothing OrElse Not doc.Headers.Contains(columnName) Then Return doc
            
            Dim newHeaders As List(Of String) = doc.Headers.Where(Function(h) h <> columnName).ToList()
            Dim result As New CsvDocument(newHeaders, doc.Options)
            
            For Each row As Dictionary(Of String, String) In doc.Rows
                Dim newRow As New Dictionary(Of String, String)()
                For Each header As String In newHeaders
                    If row.ContainsKey(header) Then
                        newRow(header) = row(header)
                    Else
                        newRow(header) = String.Empty
                    End If
                Next
                result.AddRow(newRow)
            Next
            
            Return result
        End Function

        ''' <summary>
        ''' Renames a column.
        ''' </summary>
        ''' <param name="doc">CsvDocument to modify.</param>
        ''' <param name="oldName">Current column name.</param>
        ''' <param name="newName">New column name.</param>
        ''' <returns>New CsvDocument with renamed column.</returns>
        Public Function RenameColumn(doc As CsvDocument, oldName As String, newName As String) As CsvDocument
            If doc Is Nothing OrElse String.IsNullOrEmpty(oldName) OrElse String.IsNullOrEmpty(newName) Then Return doc
            If Not doc.Headers.Contains(oldName) Then Return doc
            
            Dim newHeaders As List(Of String) = doc.Headers.Select(Function(h) If(h = oldName, newName, h)).ToList()
            Dim result As New CsvDocument(newHeaders, doc.Options)
            
            For Each row As Dictionary(Of String, String) In doc.Rows
                Dim newRow As New Dictionary(Of String, String)()
                For Each header As String In newHeaders
                    Dim sourceHeader As String = If(header = newName, oldName, header)
                    If row.ContainsKey(sourceHeader) Then
                        newRow(header) = row(sourceHeader)
                    Else
                        newRow(header) = String.Empty
                    End If
                Next
                result.AddRow(newRow)
            Next
            
            Return result
        End Function

        ''' <summary>
        ''' Gets unique values from a column.
        ''' </summary>
        ''' <param name="doc">CsvDocument.</param>
        ''' <param name="columnName">Column name.</param>
        ''' <returns>List of unique values.</returns>
        Public Function GetUniqueValues(doc As CsvDocument, columnName As String) As List(Of String)
            If doc Is Nothing OrElse Not doc.Headers.Contains(columnName) Then
                Return New List(Of String)()
            End If
            
            Return doc.Rows _
                .Where(Function(r) r.ContainsKey(columnName)) _
                .Select(Function(r) r(columnName)) _
                .Distinct() _
                .ToList()
        End Function

        ''' <summary>
        ''' Gets column values as a list.
        ''' </summary>
        ''' <param name="doc">CsvDocument.</param>
        ''' <param name="columnName">Column name.</param>
        ''' <returns>List of column values.</returns>
        Public Function GetColumnValues(doc As CsvDocument, columnName As String) As List(Of String)
            If doc Is Nothing OrElse Not doc.Headers.Contains(columnName) Then
                Return New List(Of String)()
            End If
            
            Return doc.Rows _
                .Select(Function(r) If(r.ContainsKey(columnName), r(columnName), String.Empty)) _
                .ToList()
        End Function

        ' =========================================================================
        ' CSV Statistics
        ' =========================================================================

        ''' <summary>
        ''' Counts total rows (excluding header).
        ''' </summary>
        ''' <param name="csvContent">CSV string.</param>
        ''' <param name="options">CSV options.</param>
        ''' <returns>Number of data rows.</returns>
        Public Function CountRows(csvContent As String, Optional options As CsvOptions = Nothing) As Integer
            If String.IsNullOrEmpty(csvContent) Then Return 0
            
            Dim opts As CsvOptions = If(options, CsvOptions.Default())
            Dim lines As String() = SplitLines(csvContent, opts)
            
            Return If(opts.HasHeader, lines.Length - 1, lines.Length)
        End Function

        ''' <summary>
        ''' Counts columns in CSV.
        ''' </summary>
        ''' <param name="csvContent">CSV string.</param>
        ''' <param name="options">CSV options.</param>
        ''' <returns>Number of columns.</returns>
        Public Function CountColumns(csvContent As String, Optional options As CsvOptions = Nothing) As Integer
            If String.IsNullOrEmpty(csvContent) Then Return 0
            
            Dim opts As CsvOptions = If(options, CsvOptions.Default())
            Dim lines As String() = SplitLines(csvContent, opts)
            
            If lines.Length = 0 Then Return 0
            
            Return ParseLine(lines(0), opts).Count
        End Function

        ''' <summary>
        ''' Gets CSV summary statistics.
        ''' </summary>
        ''' <param name="csvContent">CSV string.</param>
        ''' <param name="options">CSV options.</param>
        ''' <returns>Dictionary with statistics.</returns>
        Public Function GetCsvStatistics(csvContent As String, Optional options As CsvOptions = Nothing) As Dictionary(Of String, Object)
            Dim stats As New Dictionary(Of String, Object)()
            
            If String.IsNullOrEmpty(csvContent) Then
                stats("rows") = 0
                stats("columns") = 0
                stats("valid") = True
                stats("errors") = New List(Of String)()
                Return stats
            End If
            
            Dim opts As CsvOptions = If(options, CsvOptions.Default())
            
            stats("rows") = CountRows(csvContent, opts)
            stats("columns") = CountColumns(csvContent, opts)
            stats("valid") = ValidateCsvStructure(csvContent, opts)
            stats("errors") = GetValidationErrors(csvContent, opts)
            stats("headers") = If(opts.HasHeader, ParseLine(SplitLines(csvContent, opts)(0), opts), New List(Of String)())
            
            Return stats
        End Function

        ' =========================================================================
        ' Helper Methods
        ' =========================================================================

        ''' <summary>
        ''' Splits CSV content into lines, handling different newline formats.
        ''' </summary>
        Private Function SplitLines(content As String, options As CsvOptions) As String()
            If String.IsNullOrEmpty(content) Then Return New String(){}
            
            ' Normalize newlines
            Dim normalized As String = content.Replace(ControlChars.CrLf, ControlChars.Lf)
            normalized = normalized.Replace(ControlChars.Cr, ControlChars.Lf)
            
            Dim lines As String() = normalized.Split(ControlChars.Lf)
            Dim result As New List(Of String)()
            
            For Each line As String In lines
                If options.SkipEmptyLines AndAlso String.IsNullOrWhiteSpace(line) Then
                    Continue For
                End If
                
                result.Add(line)
            Next
            
            Return result.ToArray()
        End Function

    End Module

End Namespace