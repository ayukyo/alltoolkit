// CsvUtils Examples - Demonstrates all major features

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

/**
 * Example usage of CsvUtils for reading, writing, and manipulating CSV data.
 */
public class CsvUtilsExamples {

    public static void main(String[] args) throws IOException {
        System.out.println("=== CsvUtils Examples ===\n");
        
        // Create temp directory for examples
        Path tempDir = Files.createTempDirectory("csv_examples");
        
        // Run examples
        exampleBasicReading(tempDir);
        exampleBasicWriting(tempDir);
        exampleQuotedFields(tempDir);
        exampleCustomDelimiter(tempDir);
        exampleStreaming(tempDir);
        exampleTypeConversion(tempDir);
        exampleBuilderPattern(tempDir);
        exampleQuickMethods(tempDir);
        exampleDetectDelimiter(tempDir);
        
        System.out.println("\n=== All examples completed ===");
    }

    /**
     * Example 1: Basic CSV reading
     */
    static void exampleBasicReading(Path tempDir) throws IOException {
        System.out.println("\n--- Example 1: Basic CSV Reading ---");
        
        // Create a sample CSV file
        String csvContent = "name,age,city,occupation\n" +
                           "Alice,28,Beijing,Engineer\n" +
                           "Bob,35,Shanghai,Designer\n" +
                           "Charlie,42,Guangzhou,Manager\n";
        
        Path file = tempDir.resolve("sample.csv");
        Files.write(file, csvContent.getBytes());
        
        // Read using CsvUtils
        CsvUtils csv = new CsvUtils();
        List<Map<String, String>> rows = csv.readAsMaps(file.toFile());
        
        // Display data
        System.out.println("Read " + rows.size() + " records:");
        for (Map<String, String> row : rows) {
            System.out.println("  " + row.get("name") + " (" + row.get("age") + ") - " + 
                              row.get("city") + " - " + row.get("occupation"));
        }
        
        // Read as arrays
        List<String[]> arrays = csv.readAsArrays(file.toFile());
        System.out.println("\nAs arrays:");
        for (String[] arr : arrays) {
            System.out.println("  " + Arrays.toString(arr));
        }
    }

    /**
     * Example 2: Basic CSV writing
     */
    static void exampleBasicWriting(Path tempDir) throws IOException {
        System.out.println("\n--- Example 2: Basic CSV Writing ---");
        
        // Create data to write
        List<Map<String, String>> data = new ArrayList<>();
        
        Map<String, String> row1 = new LinkedHashMap<>();
        row1.put("id", "1");
        row1.put("product", "Laptop");
        row1.put("price", "999.99");
        row1.put("quantity", "10");
        data.add(row1);
        
        Map<String, String> row2 = new LinkedHashMap<>();
        row2.put("id", "2");
        row2.put("product", "Mouse");
        row2.put("price", "25.50");
        row2.put("quantity", "50");
        data.add(row2);
        
        Map<String, String> row3 = new LinkedHashMap<>();
        row3.put("id", "3");
        row3.put("product", "Keyboard");
        row3.put("price", "75.00");
        row3.put("quantity", "30");
        data.add(row3);
        
        // Write to file
        CsvUtils csv = new CsvUtils();
        Path outputFile = tempDir.resolve("products.csv");
        csv.write(outputFile, data);
        
        System.out.println("Written to: " + outputFile);
        System.out.println("Content:\n" + csv.writeToString(data));
    }

    /**
     * Example 3: Handling quoted fields
     */
    static void exampleQuotedFields(Path tempDir) throws IOException {
        System.out.println("\n--- Example 3: Quoted Fields ---");
        
        // CSV with special characters in fields
        String csvContent = "name,description,notes\n" +
                           "\"Smith, John\",\"A \"famous\" person\",\"Has comma, and quotes\"\n" +
                           "\"Jane Doe\",\"Line1\nLine2\",\"Multi-line field\"\n";
        
        Path file = tempDir.resolve("quoted.csv");
        Files.write(file, csvContent.getBytes());
        
        CsvUtils csv = new CsvUtils();
        List<Map<String, String>> rows = csv.readAsMaps(file.toFile());
        
        System.out.println("Parsed quoted fields:");
        for (Map<String, String> row : rows) {
            System.out.println("  Name: " + row.get("name"));
            System.out.println("  Description: " + row.get("description"));
            System.out.println("  Notes: " + row.get("notes"));
            System.out.println();
        }
        
        // Writing fields that need quotes
        List<Map<String, String>> data = new ArrayList<>();
        Map<String, String> specialRow = new LinkedHashMap<>();
        specialRow.put("text", "Contains, commas");
        specialRow.put("quote", "Has \"quotes\" inside");
        specialRow.put("newline", "Line1\nLine2");
        data.add(specialRow);
        
        System.out.println("Output with proper escaping:");
        System.out.println(csv.writeToString(data));
    }

    /**
     * Example 4: Custom delimiter (tab, semicolon, pipe)
     */
    static void exampleCustomDelimiter(Path tempDir) throws IOException {
        System.out.println("\n--- Example 4: Custom Delimiter ---");
        
        // Tab-delimited file
        String tabContent = "name\tage\tcity\n" +
                           "Alice\t28\tBeijing\n" +
                           "Bob\t35\tShanghai\n";
        
        Path tabFile = tempDir.resolve("tab_delimited.csv");
        Files.write(tabFile, tabContent.getBytes());
        
        CsvUtils tabCsv = CsvUtils.tabDelimited();
        List<Map<String, String>> tabRows = tabCsv.readAsMaps(tabFile.toFile());
        
        System.out.println("Tab-delimited:");
        System.out.println("  " + tabRows.get(0).get("name") + " - " + tabRows.get(0).get("city"));
        
        // Semicolon-delimited file (common in European CSV)
        String semicolonContent = "name;age;city\n" +
                                  "Alice;28;Beijing\n" +
                                  "Bob;35;Shanghai\n";
        
        Path semiFile = tempDir.resolve("semicolon.csv");
        Files.write(semiFile, semicolonContent.getBytes());
        
        CsvUtils semiCsv = CsvUtils.semicolonDelimited();
        List<Map<String, String>> semiRows = semiCsv.readAsMaps(semiFile.toFile());
        
        System.out.println("Semicolon-delimited:");
        System.out.println("  " + semiRows.get(0).get("name") + " - " + semiRows.get(0).get("city"));
        
        // Pipe-delimited file
        String pipeContent = "name|age|city\n" +
                            "Alice|28|Beijing\n" +
                            "Bob|35|Shanghai\n";
        
        Path pipeFile = tempDir.resolve("pipe.csv");
        Files.write(pipeFile, pipeContent.getBytes());
        
        CsvUtils pipeCsv = CsvUtils.pipeDelimited();
        List<Map<String, String>> pipeRows = pipeCsv.readAsMaps(pipeFile.toFile());
        
        System.out.println("Pipe-delimited:");
        System.out.println("  " + pipeRows.get(0).get("name") + " - " + pipeRows.get(0).get("city"));
    }

    /**
     * Example 5: Streaming for large files
     */
    static void exampleStreaming(Path tempDir) throws IOException {
        System.out.println("\n--- Example 5: Streaming Large Files ---");
        
        // Create a "large" file (1000 rows)
        StringBuilder sb = new StringBuilder();
        sb.append("id,value,category\n");
        for (int i = 0; i < 1000; i++) {
            sb.append(i).append(",value").append(i).append(",cat").append(i % 10).append("\n");
        }
        
        Path largeFile = tempDir.resolve("large.csv");
        Files.write(largeFile, sb.toString().getBytes());
        
        // Count records using streaming
        CsvUtils csv = new CsvUtils();
        int[] count = {0, 0, 0}; // [total, cat0, cat1]
        
        csv.stream(largeFile.toFile(), row -> {
            count[0]++;
            if (row.length > 2) {
                if (row[2].equals("cat0")) count[1]++;
                if (row[2].equals("cat1")) count[2]++;
            }
        });
        
        System.out.println("Streamed through " + count[0] + " rows");
        System.out.println("  Category 0: " + count[1] + " rows");
        System.out.println("  Category 1: " + count[2] + " rows");
        
        // Using countRecords method
        int recordCount = csv.countRecords(largeFile.toFile());
        System.out.println("Data records (excluding header): " + recordCount);
    }

    /**
     * Example 6: Type conversion helpers
     */
    static void exampleTypeConversion(Path tempDir) throws IOException {
        System.out.println("\n--- Example 6: Type Conversion ---");
        
        // CSV with numeric and boolean data
        String csvContent = "id,amount,active,score\n" +
                           "1,99.99,true,4.5\n" +
                           "2,25.50,false,3.8\n" +
                           "3,,yes,4.2\n";
        
        Path file = tempDir.resolve("types.csv");
        Files.write(file, csvContent.getBytes());
        
        CsvUtils csv = new CsvUtils();
        List<Map<String, String>> rows = csv.readAsMaps(file.toFile());
        
        System.out.println("Converted values:");
        for (Map<String, String> row : rows) {
            int id = CsvUtils.toInt(row.get("id"), 0);
            double amount = CsvUtils.toDouble(row.get("amount"), 0.0);
            boolean active = CsvUtils.toBoolean(row.get("active"));
            double score = CsvUtils.toDouble(row.get("score"), 0.0);
            
            System.out.printf("  ID: %d, Amount: %.2f, Active: %s, Score: %.1f%n",
                             id, amount, active, score);
        }
        
        // Sum all amounts
        double total = 0;
        for (Map<String, String> row : rows) {
            total += CsvUtils.toDouble(row.get("amount"), 0.0);
        }
        System.out.printf("  Total amount: %.2f%n", total);
    }

    /**
     * Example 7: Builder pattern for custom configuration
     */
    static void exampleBuilderPattern(Path tempDir) throws IOException {
        System.out.println("\n--- Example 7: Builder Pattern ---");
        
        // Custom CsvUtils with specific settings
        CsvUtils custom = CsvUtils.builder()
            .delimiter('|')
            .quote('\'')
            .hasHeader(true)
            .trimWhitespace(true)
            .build();
        
        String content = "name|age|city\n" +
                        "  Alice  |  28  |  Beijing  \n" +
                        "  Bob  |  35  |  Shanghai  \n";
        
        Path file = tempDir.resolve("custom.csv");
        Files.write(file, content.getBytes());
        
        List<Map<String, String>> rows = custom.readAsMaps(file.toFile());
        
        System.out.println("Custom delimiter '|' with trim:");
        System.out.println("  Name: " + rows.get(0).get("name")); // "Alice" (trimmed)
        System.out.println("  Age: " + rows.get(0).get("age"));   // "28" (trimmed)
        
        // No header mode
        CsvUtils noHeader = CsvUtils.builder()
            .hasHeader(false)
            .build();
        
        String noHeaderContent = "Alice,28,Beijing\n" +
                                 "Bob,35,Shanghai\n";
        
        Path noHeaderFile = tempDir.resolve("no_header.csv");
        Files.write(noHeaderFile, noHeaderContent.getBytes());
        
        List<String[]> arrayRows = noHeader.readAsArrays(noHeaderFile.toFile());
        
        System.out.println("No header mode:");
        System.out.println("  First row: " + Arrays.toString(arrayRows.get(0)));
    }

    /**
     * Example 8: Quick static methods
     */
    static void exampleQuickMethods(Path tempDir) throws IOException {
        System.out.println("\n--- Example 8: Quick Static Methods ---");
        
        // Quick read - one line!
        String content = "name,age\nAlice,28\nBob,35\n";
        Path file = tempDir.resolve("quick.csv");
        Files.write(file, content.getBytes());
        
        List<Map<String, String>> rows = CsvUtils.quickRead(file.toFile());
        System.out.println("Quick read: " + rows.size() + " records");
        
        // Quick write - one line!
        List<Map<String, String>> data = new ArrayList<>();
        data.add(new LinkedHashMap<String, String>() {{
            put("name", "Charlie");
            put("age", "42");
        }});
        
        Path outFile = tempDir.resolve("quickwrite.csv");
        CsvUtils.quickWrite(outFile.toFile(), data);
        System.out.println("Quick write completed");
        
        // Quick read arrays
        List<String[]> arrays = CsvUtils.quickReadArrays(file.toFile());
        System.out.println("Quick read arrays: " + arrays.size() + " rows");
    }

    /**
     * Example 9: Detect delimiter from file
     */
    static void exampleDetectDelimiter(Path tempDir) throws IOException {
        System.out.println("\n--- Example 9: Auto-Detect Delimiter ---");
        
        // Create files with different delimiters
        Path commaFile = tempDir.resolve("detect_comma.csv");
        Files.write(commaFile, "a,b,c\n1,2,3\n".getBytes());
        
        Path tabFile = tempDir.resolve("detect_tab.csv");
        Files.write(tabFile, "a\tb\tc\n1\t2\t3\n".getBytes());
        
        Path semiFile = tempDir.resolve("detect_semi.csv");
        Files.write(semiFile, "a;b;c\n1;2;3\n".getBytes());
        
        // Detect delimiters
        char comma = CsvUtils.detectDelimiter(commaFile.toFile());
        char tab = CsvUtils.detectDelimiter(tabFile.toFile());
        char semi = CsvUtils.detectDelimiter(semiFile.toFile());
        
        System.out.println("Detected delimiters:");
        System.out.println("  comma.csv: '" + comma + "'");
        System.out.println("  tab.csv: '\\t'");
        System.out.println("  semi.csv: '" + semi + "'");
        
        // Use detected delimiter
        CsvUtils autoCsv = CsvUtils.builder()
            .delimiter(tab)
            .build();
        
        List<String[]> rows = autoCsv.readAsArrays(tabFile.toFile());
        System.out.println("  Using detected delimiter: " + Arrays.toString(rows.get(0)));
    }
}