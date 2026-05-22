# CSV Utilities for VB.NET

Complete CSV (Comma-Separated Values) utility library for VB.NET applications. Zero external dependencies - RFC 4180 compliant.

## Features

### CSV Parsing
- `ParseCsv` - Parse CSV string into CsvDocument
- `ParseLine` - Parse single CSV line into fields
- `ParseCsvFile` - Parse CSV file into CsvDocument
- `ParseToArray` - Parse CSV into 2D array (no headers)

### CSV Generation
- `GenerateCsv` - Generate CSV string from CsvDocument
- `GenerateLine` - Generate single CSV line from fields
- `GenerateFromArray` - Generate CSV from 2D array
- `SaveCsvFile` - Save CsvDocument to file

### CSV Escaping (RFC 4180 Compliant)
- `EscapeField` - Escape field with quoting if needed
- `UnescapeField` - Unescape quoted field

### CSV Validation
- `ValidateCsvStructure` - Check consistent column count
- `GetValidationErrors` - Get detailed validation errors

### Row Operations
- `FilterRows` - Filter rows by predicate
- `SortRows` - Sort rows by column (ascending/descending)
- `GroupRows` - Group rows by column value
- `RemoveRows` - Remove rows matching predicate

### Column Operations
- `AddColumn` - Add new column with default value
- `RemoveColumn` - Remove column
- `RenameColumn` - Rename column
- `GetUniqueValues` - Get unique values from column
- `GetColumnValues` - Get all values from column

### Transformation
- `ToDictionaryList` - Convert to list of dictionaries
- `ToArrayList` - Convert to list of arrays
- `FromDictionaryList` - Convert from list of dictionaries

### Statistics
- `CountRows` - Count data rows
- `CountColumns` - Count columns
- `GetCsvStatistics` - Get comprehensive statistics

## Usage

```vb
Imports AllToolkit

' Parse CSV string
Dim csv As String = "name,age,city" & vbCrLf & _
                   "John,30,New York" & vbCrLf & _
                   "Jane,25,Los Angeles"

Dim doc As CsvDocument = CsvUtils.ParseCsv(csv)

' Access data
Console.WriteLine("Headers: " & String.Join(", ", doc.Headers))
Console.WriteLine("First row name: " & doc.GetValue(0, "name"))

' Create CSV document
Dim newDoc As New CsvDocument({"product", "price", "quantity"})
newDoc.AddRow({"Apple", "1.50", "100"})
newDoc.AddRow({"Orange", "2.00", "50"})

' Generate CSV
Dim csvOutput As String = CsvUtils.GenerateCsv(newDoc)

' Row operations
Dim filtered As CsvDocument = CsvUtils.FilterRows(doc, _
    Function(row) Integer.Parse(row("age")) >= 30)

Dim sorted As CsvDocument = CsvUtils.SortRows(doc, "age", False)

' Column operations
Dim withColumn As CsvDocument = CsvUtils.AddColumn(doc, "country", "USA")

' Different delimiters (TSV, PSV)
Dim tsvDoc As CsvDocument = CsvUtils.ParseCsv(tsvContent, CsvOptions.TSV())
Dim psvDoc As CsvDocument = CsvUtils.ParseCsv(psvContent, CsvOptions.PSV())

' File operations
CsvUtils.SaveCsvFile(doc, "output.csv")
Dim loaded As CsvDocument = CsvUtils.ParseCsvFile("input.csv")
```

## CsvDocument Class

```vb
' Create with headers
Dim doc As New CsvDocument({"name", "age", "city"})

' Add rows
doc.AddRow({"John", "30", "New York"})
doc.AddRow(New Dictionary(Of String, String) From { _
    {"name", "Jane"}, {"age", "25"}, {"city", "LA"} })

' Properties
Console.WriteLine("Rows: " & doc.RowCount)
Console.WriteLine("Columns: " & doc.ColumnCount)

' Get/Set values
Dim name As String = doc.GetValue(0, "name")
doc.SetValue(0, "age", "31")
```

## CsvOptions Class

```vb
' Default CSV options (comma delimiter)
Dim opts As CsvOptions = CsvOptions.Default()

' TSV (Tab-Separated Values)
Dim tsvOpts As CsvOptions = CsvOptions.TSV()

' PSV (Pipe-Separated Values)
Dim psvOpts As CsvOptions = CsvOptions.PSV()

' Custom options
Dim customOpts As New CsvOptions With {
    .Delimiter = ";"c,
    .HasHeader = True,
    .TrimFields = True,
    .SkipEmptyLines = True
}
```

## RFC 4180 Compliance

Handles:
- Quoted fields with commas: `"value,with,commas"`
- Escaped quotes: `"value with ""quote"""`
- Newlines in fields: `"line1\nline2"`
- Empty fields: `a,,c`

## Files

- `mod.vb` - Main module implementation
- `test.vb` - Unit tests (70+ tests)
- `examples.vb` - Usage examples (10 examples)
- `README.md` - This documentation

## Running Tests

```bash
dotnet test
```

## Running Examples

```bash
dotnet run
```

## Zero Dependencies

Uses only .NET standard library:
- System
- System.IO
- System.Text
- System.Collections.Generic
- System.Linq