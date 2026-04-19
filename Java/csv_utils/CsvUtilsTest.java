// Test suite for CsvUtils

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

/**
 * Comprehensive test suite for CsvUtils.
 * Tests cover reading, writing, parsing, and edge cases.
 */
@DisplayName("CsvUtils Tests")
class CsvUtilsTest {

    private CsvUtils csv;
    private Path tempDir;

    @BeforeEach
    void setUp() throws IOException {
        csv = new CsvUtils();
        tempDir = Files.createTempDirectory("csv_test");
    }

    @AfterEach
    void tearDown() throws IOException {
        // Clean up temp files
        Files.walk(tempDir)
            .sorted(Comparator.reverseOrder())
            .forEach(path -> {
                try {
                    Files.deleteIfExists(path);
                } catch (IOException e) {
                    // ignore
                }
            });
    }

    // ==================== Basic Parsing Tests ====================

    @Test
    @DisplayName("Parse simple CSV line")
    void testParseSimpleLine() {
        String[] result = csv.parseLine("a,b,c");
        assertArrayEquals(new String[]{"a", "b", "c"}, result);
    }

    @Test
    @DisplayName("Parse CSV line with spaces")
    void testParseLineWithSpaces() {
        String[] result = csv.parseLine("a, b , c");
        assertArrayEquals(new String[]{"a", " b ", " c"}, result);
    }

    @Test
    @DisplayName("Parse CSV line with trailing spaces")
    void testParseLineWithTrailingSpaces() {
        String[] result = csv.parseLine("a,b,c  ");
        assertArrayEquals(new String[]{"a", "b", "c  "}, result);
    }

    @Test
    @DisplayName("Parse empty line")
    void testParseEmptyLine() {
        String[] result = csv.parseLine("");
        assertArrayEquals(new String[]{""}, result);
    }

    @Test
    @DisplayName("Parse single field")
    void testParseSingleField() {
        String[] result = csv.parseLine("hello");
        assertArrayEquals(new String[]{"hello"}, result);
    }

    @Test
    @DisplayName("Parse empty fields")
    void testParseEmptyFields() {
        String[] result = csv.parseLine("a,,c");
        assertArrayEquals(new String[]{"a", "", "c"}, result);
    }

    @Test
    @DisplayName("Parse line with multiple empty fields")
    void testParseMultipleEmptyFields() {
        String[] result = csv.parseLine(",,,");
        assertArrayEquals(new String[]{"", "", "", ""}, result);
    }

    // ==================== Quoted Field Tests ====================

    @Test
    @DisplayName("Parse quoted field")
    void testParseQuotedField() {
        String[] result = csv.parseLine("\"hello world\",b,c");
        assertArrayEquals(new String[]{"hello world", "b", "c"}, result);
    }

    @Test
    @DisplayName("Parse field with delimiter in quotes")
    void testParseDelimiterInQuotes() {
        String[] result = csv.parseLine("\"a,b\",c,d");
        assertArrayEquals(new String[]{"a,b", "c", "d"}, result);
    }

    @Test
    @DisplayName("Parse field with newline in quotes")
    void testParseNewlineInQuotes() {
        List<String[]> rows = csv.parse("\"a\nb\",c,d\ne,f,g");
        assertEquals(2, rows.size());
        assertEquals("a\nb", rows.get(0)[0]);
    }

    @Test
    @DisplayName("Parse escaped quotes")
    void testParseEscapedQuotes() {
        String[] result = csv.parseLine("\"he said \"\"hello\"\"\",b");
        assertArrayEquals(new String[]{"he said \"hello\"", "b"}, result);
    }

    @Test
    @DisplayName("Parse multiple quoted fields")
    void testParseMultipleQuotedFields() {
        String[] result = csv.parseLine("\"a\",\"b\",\"c\"");
        assertArrayEquals(new String[]{"a", "b", "c"}, result);
    }

    // ==================== Format Tests ====================

    @Test
    @DisplayName("Format simple row")
    void testFormatSimpleRow() {
        String result = csv.formatRow(new String[]{"a", "b", "c"});
        assertEquals("a,b,c\r\n", result);
    }

    @Test
    @DisplayName("Format row with quotes needed")
    void testFormatRowWithQuotes() {
        String result = csv.formatRow(new String[]{"a,b", "c"});
        assertEquals("\"a,b\",c\r\n", result);
    }

    @Test
    @DisplayName("Format row with newline in field")
    void testFormatRowWithNewline() {
        String result = csv.formatRow(new String[]{"a\nb", "c"});
        assertEquals("\"a\nb\",c\r\n", result);
    }

    @Test
    @DisplayName("Format row with quotes in field")
    void testFormatRowWithQuotesInField() {
        String result = csv.formatRow(new String[]{"say \"hi\"", "c"});
        assertEquals("\"say \"\"hi\"\"\",c\r\n", result);
    }

    @Test
    @DisplayName("Format null field")
    void testFormatNullField() {
        String result = csv.formatRow(new String[]{"a", null, "c"});
        assertEquals("a,,c\r\n", result);
    }

    @Test
    @DisplayName("Format empty fields")
    void testFormatEmptyFields() {
        String result = csv.formatRow(new String[]{"", "", ""});
        assertEquals(",,\r\n", result);
    }

    // ==================== Read/Write File Tests ====================

    @Test
    @DisplayName("Read CSV file as arrays")
    void testReadAsArrays() throws IOException {
        String content = "name,age,city\nAlice,25,Beijing\nBob,30,Shanghai\n";
        Path file = tempDir.resolve("test.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        List<String[]> rows = csv.readAsArrays(file.toFile());
        
        assertEquals(3, rows.size());
        assertArrayEquals(new String[]{"name", "age", "city"}, rows.get(0));
        assertArrayEquals(new String[]{"Alice", "25", "Beijing"}, rows.get(1));
        assertArrayEquals(new String[]{"Bob", "30", "Shanghai"}, rows.get(2));
    }

    @Test
    @DisplayName("Read CSV file as maps")
    void testReadAsMaps() throws IOException {
        String content = "name,age,city\nAlice,25,Beijing\nBob,30,Shanghai\n";
        Path file = tempDir.resolve("test.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        List<Map<String, String>> rows = csv.readAsMaps(file.toFile());
        
        assertEquals(2, rows.size());
        assertEquals("Alice", rows.get(0).get("name"));
        assertEquals("25", rows.get(0).get("age"));
        assertEquals("Beijing", rows.get(0).get("city"));
        assertEquals("Bob", rows.get(1).get("name"));
    }

    @Test
    @DisplayName("Write CSV file from maps")
    void testWriteFromMaps() throws IOException {
        List<Map<String, String>> data = new ArrayList<>();
        data.add(new LinkedHashMap<String, String>() {{
            put("name", "Alice");
            put("age", "25");
            put("city", "Beijing");
        }});
        data.add(new LinkedHashMap<String, String>() {{
            put("name", "Bob");
            put("age", "30");
            put("city", "Shanghai");
        }});
        
        Path file = tempDir.resolve("output.csv");
        csv.write(file, data);
        
        String content = new String(Files.readAllBytes(file), StandardCharsets.UTF_8);
        assertTrue(content.contains("name,age,city"));
        assertTrue(content.contains("Alice,25,Beijing"));
        assertTrue(content.contains("Bob,30,Shanghai"));
    }

    @Test
    @DisplayName("Write CSV file from arrays")
    void testWriteFromArrays() throws IOException {
        List<String[]> data = new ArrayList<>();
        data.add(new String[]{"Alice", "25", "Beijing"});
        data.add(new String[]{"Bob", "30", "Shanghai"});
        
        Path file = tempDir.resolve("output.csv");
        csv.writeArrays(file, data, new String[]{"name", "age", "city"});
        
        String content = new String(Files.readAllBytes(file), StandardCharsets.UTF_8);
        assertTrue(content.contains("name,age,city"));
        assertTrue(content.contains("Alice,25,Beijing"));
    }

    @Test
    @DisplayName("Round trip read and write")
    void testRoundTrip() throws IOException {
        // Create test data
        List<Map<String, String>> original = new ArrayList<>();
        original.add(new LinkedHashMap<String, String>() {{
            put("name", "Alice");
            put("age", "25");
            put("city", "Beijing");
        }});
        original.add(new LinkedHashMap<String, String>() {{
            put("name", "Bob");
            put("age", "30");
            put("city", "Shanghai");
        }});
        
        // Write
        Path file = tempDir.resolve("roundtrip.csv");
        csv.write(file, original);
        
        // Read
        List<Map<String, String>> read = csv.readAsMaps(file.toFile());
        
        // Compare
        assertEquals(original.size(), read.size());
        assertEquals(original.get(0).get("name"), read.get(0).get("name"));
        assertEquals(original.get(1).get("city"), read.get(1).get("city"));
    }

    // ==================== Parse String Tests ====================

    @Test
    @DisplayName("Parse CSV string")
    void testParseString() {
        String content = "a,b,c\n1,2,3\n4,5,6";
        List<String[]> rows = csv.parse(content);
        
        assertEquals(3, rows.size());
        assertArrayEquals(new String[]{"a", "b", "c"}, rows.get(0));
        assertArrayEquals(new String[]{"1", "2", "3"}, rows.get(1));
    }

    @Test
    @DisplayName("Parse CSV string as maps")
    void testParseStringAsMaps() {
        String content = "name,age\nAlice,25\nBob,30";
        List<Map<String, String>> rows = csv.readAsMapsFromString(content);
        
        assertEquals(2, rows.size());
        assertEquals("Alice", rows.get(0).get("name"));
        assertEquals("25", rows.get(0).get("age"));
        assertEquals("Bob", rows.get(1).get("name"));
        assertEquals("30", rows.get(1).get("age"));
    }

    // ==================== Streaming Tests ====================

    @Test
    @DisplayName("Stream CSV file")
    void testStream() throws IOException {
        String content = "a,b,c\n1,2,3\n4,5,6\n";
        Path file = tempDir.resolve("stream.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        List<String[]> rows = new ArrayList<>();
        csv.stream(file.toFile(), rows::add);
        
        assertEquals(3, rows.size());
        assertArrayEquals(new String[]{"a", "b", "c"}, rows.get(0));
    }

    @Test
    @DisplayName("Count records")
    void testCountRecords() throws IOException {
        String content = "a,b,c\n1,2,3\n4,5,6\n7,8,9\n";
        Path file = tempDir.resolve("count.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        int count = csv.countRecords(file.toFile());
        
        assertEquals(3, count); // 4 rows - 1 header
    }

    // ==================== Custom Delimiter Tests ====================

    @Test
    @DisplayName("Tab delimited file")
    void testTabDelimited() throws IOException {
        CsvUtils tabCsv = CsvUtils.tabDelimited();
        
        String content = "name\tage\nAlice\t25\nBob\t30\n";
        Path file = tempDir.resolve("tab.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        List<Map<String, String>> rows = tabCsv.readAsMaps(file.toFile());
        
        assertEquals(2, rows.size());
        assertEquals("Alice", rows.get(0).get("name"));
    }

    @Test
    @DisplayName("Semicolon delimited file")
    void testSemicolonDelimited() throws IOException {
        CsvUtils scsv = CsvUtils.semicolonDelimited();
        
        String content = "name;age\nAlice;25\nBob;30\n";
        Path file = tempDir.resolve("semicolon.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        List<Map<String, String>> rows = scsv.readAsMaps(file.toFile());
        
        assertEquals(2, rows.size());
        assertEquals("Alice", rows.get(0).get("name"));
    }

    @Test
    @DisplayName("Pipe delimited file")
    void testPipeDelimited() throws IOException {
        CsvUtils pipeCsv = CsvUtils.pipeDelimited();
        
        String content = "name|age\nAlice|25\nBob|30\n";
        Path file = tempDir.resolve("pipe.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        List<Map<String, String>> rows = pipeCsv.readAsMaps(file.toFile());
        
        assertEquals(2, rows.size());
        assertEquals("Alice", rows.get(0).get("name"));
    }

    // ==================== Builder Tests ====================

    @Test
    @DisplayName("Builder creates custom CsvUtils")
    void testBuilder() {
        CsvUtils custom = CsvUtils.builder()
            .delimiter(';')
            .quote('\'')
            .hasHeader(false)
            .trimWhitespace(true)
            .build();
        
        assertEquals(';', custom.getDelimiter());
        assertEquals('\'', custom.getQuote());
        assertFalse(custom.hasHeader());
    }

    @Test
    @DisplayName("No header mode")
    void testNoHeaderMode() throws IOException {
        CsvUtils noHeader = CsvUtils.noHeader();
        
        String content = "Alice,25,Beijing\nBob,30,Shanghai\n";
        Path file = tempDir.resolve("noheader.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        List<String[]> rows = noHeader.readAsArrays(file.toFile());
        
        assertEquals(2, rows.size());
        assertEquals("Alice", rows.get(0)[0]);
    }

    // ==================== Type Conversion Tests ====================

    @Test
    @DisplayName("Convert to int")
    void testToInt() {
        assertEquals(42, CsvUtils.toInt("42", 0));
        assertEquals(0, CsvUtils.toInt("abc", 0));
        assertEquals(-1, CsvUtils.toInt(null, -1));
        assertEquals(-1, CsvUtils.toInt("", -1));
        assertEquals(-1, CsvUtils.toInt("  ", -1));
    }

    @Test
    @DisplayName("Convert to long")
    void testToLong() {
        assertEquals(123456789L, CsvUtils.toLong("123456789", 0L));
        assertEquals(0L, CsvUtils.toLong("abc", 0L));
        assertEquals(-1L, CsvUtils.toLong(null, -1L));
    }

    @Test
    @DisplayName("Convert to double")
    void testToDouble() {
        assertEquals(3.14, CsvUtils.toDouble("3.14", 0.0), 0.001);
        assertEquals(0.0, CsvUtils.toDouble("abc", 0.0), 0.001);
        assertEquals(-1.0, CsvUtils.toDouble(null, -1.0), 0.001);
    }

    @Test
    @DisplayName("Convert to boolean")
    void testToBoolean() {
        assertTrue(CsvUtils.toBoolean("true"));
        assertTrue(CsvUtils.toBoolean("TRUE"));
        assertTrue(CsvUtils.toBoolean("1"));
        assertTrue(CsvUtils.toBoolean("yes"));
        assertTrue(CsvUtils.toBoolean("YES"));
        assertTrue(CsvUtils.toBoolean("y"));
        assertTrue(CsvUtils.toBoolean("Y"));
        assertFalse(CsvUtils.toBoolean("false"));
        assertFalse(CsvUtils.toBoolean("0"));
        assertFalse(CsvUtils.toBoolean("no"));
        assertFalse(CsvUtils.toBoolean(null));
        assertFalse(CsvUtils.toBoolean(""));
    }

    @Test
    @DisplayName("Get string with default")
    void testGetStringWithDefault() {
        Map<String, String> map = new HashMap<>();
        map.put("key", "value");
        
        assertEquals("value", CsvUtils.getString(map, "key", "default"));
        assertEquals("default", CsvUtils.getString(map, "missing", "default"));
    }

    // ==================== Static Factory Tests ====================

    @Test
    @DisplayName("Static create method")
    void testStaticCreate() {
        CsvUtils csv = CsvUtils.create();
        assertNotNull(csv);
        assertEquals(',', csv.getDelimiter());
    }

    @Test
    @DisplayName("Static quick read")
    void testStaticQuickRead() throws IOException {
        String content = "name,age\nAlice,25\n";
        Path file = tempDir.resolve("quick.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        List<Map<String, String>> rows = CsvUtils.quickRead(file.toFile());
        
        assertEquals(1, rows.size());
        assertEquals("Alice", rows.get(0).get("name"));
    }

    @Test
    @DisplayName("Static quick write")
    void testStaticQuickWrite() throws IOException {
        List<Map<String, String>> data = new ArrayList<>();
        data.add(new LinkedHashMap<String, String>() {{
            put("name", "Alice");
            put("age", "25");
        }});
        
        Path file = tempDir.resolve("quickwrite.csv");
        CsvUtils.quickWrite(file.toFile(), data);
        
        assertTrue(Files.exists(file));
        String content = new String(Files.readAllBytes(file), StandardCharsets.UTF_8);
        assertTrue(content.contains("name,age"));
        assertTrue(content.contains("Alice,25"));
    }

    // ==================== Edge Cases ====================

    @Test
    @DisplayName("Empty file")
    void testEmptyFile() throws IOException {
        Path file = tempDir.resolve("empty.csv");
        Files.write(file, "".getBytes(StandardCharsets.UTF_8));
        
        List<String[]> rows = csv.readAsArrays(file.toFile());
        
        assertTrue(rows.isEmpty());
    }

    @Test
    @DisplayName("File with only header")
    void testHeaderOnly() throws IOException {
        String content = "name,age,city\n";
        Path file = tempDir.resolve("header_only.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        List<Map<String, String>> rows = csv.readAsMaps(file.toFile());
        
        assertTrue(rows.isEmpty());
    }

    @Test
    @DisplayName("Unicode content")
    void testUnicodeContent() throws IOException {
        String content = "name,emoji\n张三,🎉\n李四,你好\n";
        Path file = tempDir.resolve("unicode.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        List<Map<String, String>> rows = csv.readAsMaps(file.toFile());
        
        assertEquals(2, rows.size());
        assertEquals("张三", rows.get(0).get("name"));
        assertEquals("🎉", rows.get(0).get("emoji"));
    }

    @Test
    @DisplayName("Large file")
    void testLargeFile() throws IOException {
        StringBuilder sb = new StringBuilder();
        sb.append("id,value\n");
        for (int i = 0; i < 1000; i++) {
            sb.append(i).append(",value").append(i).append("\n");
        }
        
        Path file = tempDir.resolve("large.csv");
        Files.write(file, sb.toString().getBytes(StandardCharsets.UTF_8));
        
        List<Map<String, String>> rows = csv.readAsMaps(file.toFile());
        
        assertEquals(1000, rows.size());
        assertEquals("0", rows.get(0).get("id"));
        assertEquals("999", rows.get(999).get("id"));
    }

    @Test
    @DisplayName("Very long field")
    void testVeryLongField() throws IOException {
        StringBuilder longField = new StringBuilder();
        for (int i = 0; i < 10000; i++) {
            longField.append("x");
        }
        
        String content = "name,value\n" + longField + ",test\n";
        Path file = tempDir.resolve("longfield.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        List<Map<String, String>> rows = csv.readAsMaps(file.toFile());
        
        assertEquals(1, rows.size());
        assertEquals(10000, rows.get(0).get("name").length());
    }

    @Test
    @DisplayName("Trim whitespace option")
    void testTrimWhitespace() throws IOException {
        CsvUtils trimCsv = CsvUtils.builder()
            .hasHeader(true)
            .trimWhitespace(true)
            .build();
        
        String content = "name,age\n  Alice  , 25 \n  Bob , 30 \n";
        Path file = tempDir.resolve("trim.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        List<Map<String, String>> rows = trimCsv.readAsMaps(file.toFile());
        
        assertEquals("Alice", rows.get(0).get("name"));
        assertEquals("25", rows.get(0).get("age"));
    }

    @Test
    @DisplayName("Detect delimiter - comma")
    void testDetectDelimiterComma() throws IOException {
        String content = "a,b,c\n1,2,3\n";
        Path file = tempDir.resolve("detect_comma.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        char detected = CsvUtils.detectDelimiter(file.toFile());
        
        assertEquals(',', detected);
    }

    @Test
    @DisplayName("Detect delimiter - tab")
    void testDetectDelimiterTab() throws IOException {
        String content = "a\tb\tc\n1\t2\t3\n";
        Path file = tempDir.resolve("detect_tab.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        char detected = CsvUtils.detectDelimiter(file.toFile());
        
        assertEquals('\t', detected);
    }

    @Test
    @DisplayName("Detect delimiter - semicolon")
    void testDetectDelimiterSemicolon() throws IOException {
        String content = "a;b;c\n1;2;3\n";
        Path file = tempDir.resolve("detect_semicolon.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        char detected = CsvUtils.detectDelimiter(file.toFile());
        
        assertEquals(';', detected);
    }

    @Test
    @DisplayName("Write to string")
    void testWriteToString() {
        List<Map<String, String>> data = new ArrayList<>();
        data.add(new LinkedHashMap<String, String>() {{
            put("name", "Alice");
            put("age", "25");
        }});
        
        String result = csv.writeToString(data);
        
        assertTrue(result.contains("name,age"));
        assertTrue(result.contains("Alice,25"));
    }

    @Test
    @DisplayName("Write with custom headers")
    void testWriteWithCustomHeaders() {
        List<Map<String, String>> data = new ArrayList<>();
        data.add(new LinkedHashMap<String, String>() {{
            put("name", "Alice");
            put("age", "25");
            put("extra", "ignored");
        }});
        
        String result = csv.writeToString(data, new String[]{"name", "age"});
        
        assertTrue(result.contains("name,age"));
        assertFalse(result.contains("extra"));
    }

    @Test
    @DisplayName("Append to existing file")
    void testAppend() throws IOException {
        // Create initial file
        List<Map<String, String>> data = new ArrayList<>();
        data.add(new LinkedHashMap<String, String>() {{
            put("name", "Alice");
            put("age", "25");
        }});
        
        Path file = tempDir.resolve("append.csv");
        csv.write(file, data);
        
        // Append more data
        List<Map<String, String>> moreData = new ArrayList<>();
        moreData.add(new LinkedHashMap<String, String>() {{
            put("name", "Bob");
            put("age", "30");
        }});
        csv.append(file, moreData);
        
        // Read and verify
        List<Map<String, String>> rows = csv.readAsMaps(file.toFile());
        assertEquals(2, rows.size());
        assertEquals("Alice", rows.get(0).get("name"));
        assertEquals("Bob", rows.get(1).get("name"));
    }

    @Test
    @DisplayName("ReadAsMaps without header throws exception")
    void testReadAsMapsWithoutHeader() throws IOException {
        CsvUtils noHeader = CsvUtils.noHeader();
        
        String content = "Alice,25\nBob,30\n";
        Path file = tempDir.resolve("noheader_test.csv");
        Files.write(file, content.getBytes(StandardCharsets.UTF_8));
        
        assertThrows(IllegalStateException.class, () -> noHeader.readAsMaps(file.toFile()));
    }
}