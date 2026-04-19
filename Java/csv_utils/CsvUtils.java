// CsvUtils - CSV File Reader/Writer with Zero External Dependencies
// Pure Java implementation supporting streaming, headers, and type conversion

import java.io.*;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.function.Consumer;
import java.util.function.Function;

/**
 * A lightweight CSV utility for reading and writing CSV files.
 * Zero external dependencies - uses only Java standard library.
 * 
 * Features:
 * - Read CSV files to List of Maps or List of Arrays
 * - Write data to CSV files or strings
 * - Support for headers (first row as column names)
 * - Support for quoted fields containing delimiters and newlines
 * - Configurable delimiter, quote character, and line separator
 * - Streaming mode for large files
 * - Type conversion helpers
 * - RFC 4180 compliant
 * 
 * @author AllToolkit
 * @version 1.0.0
 */
public class CsvUtils {

    // Default configuration
    private static final char DEFAULT_DELIMITER = ',';
    private static final char DEFAULT_QUOTE = '"';
    private static final String DEFAULT_LINE_SEPARATOR = "\r\n";
    private static final Charset DEFAULT_CHARSET = StandardCharsets.UTF_8;

    // Instance configuration
    private final char delimiter;
    private final char quote;
    private final String lineSeparator;
    private final Charset charset;
    private final boolean hasHeader;
    private final boolean trimWhitespace;

    /**
     * Builder for creating CsvUtils instances with custom configuration.
     */
    public static class Builder {
        private char delimiter = DEFAULT_DELIMITER;
        private char quote = DEFAULT_QUOTE;
        private String lineSeparator = DEFAULT_LINE_SEPARATOR;
        private Charset charset = DEFAULT_CHARSET;
        private boolean hasHeader = true;
        private boolean trimWhitespace = false;

        /**
         * Set the field delimiter character.
         * @param delimiter delimiter character (default: ',')
         * @return this builder
         */
        public Builder delimiter(char delimiter) {
            this.delimiter = delimiter;
            return this;
        }

        /**
         * Set the quote character for escaping fields.
         * @param quote quote character (default: '"')
         * @return this builder
         */
        public Builder quote(char quote) {
            this.quote = quote;
            return this;
        }

        /**
         * Set the line separator.
         * @param lineSeparator line separator string (default: "\r\n")
         * @return this builder
         */
        public Builder lineSeparator(String lineSeparator) {
            this.lineSeparator = lineSeparator;
            return this;
        }

        /**
         * Set the file charset.
         * @param charset charset for encoding/decoding (default: UTF-8)
         * @return this builder
         */
        public Builder charset(Charset charset) {
            this.charset = charset;
            return this;
        }

        /**
         * Set whether the first row is a header.
         * @param hasHeader true if first row is header (default: true)
         * @return this builder
         */
        public Builder hasHeader(boolean hasHeader) {
            this.hasHeader = hasHeader;
            return this;
        }

        /**
         * Set whether to trim whitespace from fields.
         * @param trimWhitespace true to trim (default: false)
         * @return this builder
         */
        public Builder trimWhitespace(boolean trimWhitespace) {
            this.trimWhitespace = trimWhitespace;
            return this;
        }

        /**
         * Build the CsvUtils instance.
         * @return new CsvUtils instance
         */
        public CsvUtils build() {
            return new CsvUtils(this);
        }
    }

    /**
     * Create a new builder for CsvUtils.
     * @return new Builder instance
     */
    public static Builder builder() {
        return new Builder();
    }

    /**
     * Create CsvUtils with default settings.
     */
    public CsvUtils() {
        this(builder());
    }

    private CsvUtils(Builder builder) {
        this.delimiter = builder.delimiter;
        this.quote = builder.quote;
        this.lineSeparator = builder.lineSeparator;
        this.charset = builder.charset;
        this.hasHeader = builder.hasHeader;
        this.trimWhitespace = builder.trimWhitespace;
    }

    // ==================== READING ====================

    /**
     * Read CSV file and return list of maps (using first row as headers).
     * @param filePath path to the CSV file
     * @return list of maps where keys are column headers
     * @throws IOException if file cannot be read
     */
    public List<Map<String, String>> readAsMaps(Path filePath) throws IOException {
        return readAsMaps(filePath.toFile());
    }

    /**
     * Read CSV file and return list of maps (using first row as headers).
     * @param file the CSV file
     * @return list of maps where keys are column headers
     * @throws IOException if file cannot be read
     */
    public List<Map<String, String>> readAsMaps(File file) throws IOException {
        if (!hasHeader) {
            throw new IllegalStateException("hasHeader must be true for readAsMaps");
        }
        
        List<String[]> rows = readAsArrays(file);
        if (rows.isEmpty()) {
            return Collections.emptyList();
        }
        
        String[] headers = rows.get(0);
        List<Map<String, String>> result = new ArrayList<>();
        
        for (int i = 1; i < rows.size(); i++) {
            String[] values = rows.get(i);
            Map<String, String> map = new LinkedHashMap<>();
            for (int j = 0; j < headers.length && j < values.length; j++) {
                map.put(headers[j], values[j]);
            }
            result.add(map);
        }
        
        return result;
    }

    /**
     * Read CSV file and return list of string arrays.
     * @param filePath path to the CSV file
     * @return list of string arrays (each array is a row)
     * @throws IOException if file cannot be read
     */
    public List<String[]> readAsArrays(Path filePath) throws IOException {
        return readAsArrays(filePath.toFile());
    }

    /**
     * Read CSV file and return list of string arrays.
     * @param file the CSV file
     * @return list of string arrays (each array is a row)
     * @throws IOException if file cannot be read
     */
    public List<String[]> readAsArrays(File file) throws IOException {
        List<String[]> result = new ArrayList<>();
        try (BufferedReader reader = Files.newBufferedReader(file.toPath(), charset)) {
            String line;
            StringBuilder buffer = new StringBuilder();
            boolean inQuotes = false;
            
            while ((line = reader.readLine()) != null) {
                if (buffer.length() > 0) {
                    buffer.append('\n');
                }
                buffer.append(line);
                
                // Count quotes to determine if we're in a quoted field
                int quoteCount = countQuotes(buffer.toString());
                inQuotes = (quoteCount % 2) != 0;
                
                if (!inQuotes) {
                    result.add(parseLine(buffer.toString()));
                    buffer.setLength(0);
                }
            }
            
            // Handle remaining buffer
            if (buffer.length() > 0) {
                result.add(parseLine(buffer.toString()));
            }
        }
        
        return result;
    }

    /**
     * Read CSV string and return list of maps.
     * @param csvContent CSV content as string
     * @return list of maps where keys are column headers
     */
    public List<Map<String, String>> readAsMapsFromString(String csvContent) {
        if (!hasHeader) {
            throw new IllegalStateException("hasHeader must be true for readAsMapsFromString");
        }
        
        List<String[]> rows = parse(csvContent);
        if (rows.isEmpty()) {
            return Collections.emptyList();
        }
        
        String[] headers = rows.get(0);
        List<Map<String, String>> result = new ArrayList<>();
        
        for (int i = 1; i < rows.size(); i++) {
            String[] values = rows.get(i);
            Map<String, String> map = new LinkedHashMap<>();
            for (int j = 0; j < headers.length && j < values.length; j++) {
                map.put(headers[j], values[j]);
            }
            result.add(map);
        }
        
        return result;
    }

    /**
     * Parse CSV string into list of string arrays.
     * @param csvContent CSV content as string
     * @return list of string arrays
     */
    public List<String[]> parse(String csvContent) {
        List<String[]> result = new ArrayList<>();
        String[] lines = splitLines(csvContent);
        
        StringBuilder buffer = new StringBuilder();
        boolean inQuotes = false;
        
        for (String line : lines) {
            if (buffer.length() > 0) {
                buffer.append('\n');
            }
            buffer.append(line);
            
            int quoteCount = countQuotes(buffer.toString());
            inQuotes = (quoteCount % 2) != 0;
            
            if (!inQuotes) {
                result.add(parseLine(buffer.toString()));
                buffer.setLength(0);
            }
        }
        
        if (buffer.length() > 0) {
            result.add(parseLine(buffer.toString()));
        }
        
        return result;
    }

    /**
     * Stream CSV rows to a consumer (memory efficient for large files).
     * @param filePath path to the CSV file
     * @param consumer consumer for each row as string array
     * @throws IOException if file cannot be read
     */
    public void stream(Path filePath, Consumer<String[]> consumer) throws IOException {
        stream(filePath.toFile(), consumer);
    }

    /**
     * Stream CSV rows to a consumer (memory efficient for large files).
     * @param file the CSV file
     * @param consumer consumer for each row as string array
     * @throws IOException if file cannot be read
     */
    public void stream(File file, Consumer<String[]> consumer) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(file.toPath(), charset)) {
            String line;
            StringBuilder buffer = new StringBuilder();
            
            while ((line = reader.readLine()) != null) {
                if (buffer.length() > 0) {
                    buffer.append('\n');
                }
                buffer.append(line);
                
                int quoteCount = countQuotes(buffer.toString());
                boolean inQuotes = (quoteCount % 2) != 0;
                
                if (!inQuotes) {
                    consumer.accept(parseLine(buffer.toString()));
                    buffer.setLength(0);
                }
            }
            
            if (buffer.length() > 0) {
                consumer.accept(parseLine(buffer.toString()));
            }
        }
    }

    // ==================== WRITING ====================

    /**
     * Write list of maps to a CSV file.
     * @param filePath path to the output file
     * @param data list of maps to write
     * @throws IOException if file cannot be written
     */
    public void write(Path filePath, List<Map<String, String>> data) throws IOException {
        write(filePath, data, null);
    }

    /**
     * Write list of maps to a CSV file with specified headers.
     * @param filePath path to the output file
     * @param data list of maps to write
     * @param headers column headers (null to use keys from first map)
     * @throws IOException if file cannot be written
     */
    public void write(Path filePath, List<Map<String, String>> data, String[] headers) throws IOException {
        String content = writeToString(data, headers);
        Files.write(filePath, content.getBytes(charset));
    }

    /**
     * Write list of arrays to a CSV file.
     * @param filePath path to the output file
     * @param data list of string arrays to write
     * @param headers column headers (null for no header)
     * @throws IOException if file cannot be written
     */
    public void writeArrays(Path filePath, List<String[]> data, String[] headers) throws IOException {
        String content = writeArraysToString(data, headers);
        Files.write(filePath, content.getBytes(charset));
    }

    /**
     * Convert list of maps to CSV string.
     * @param data list of maps to convert
     * @return CSV string
     */
    public String writeToString(List<Map<String, String>> data) {
        return writeToString(data, null);
    }

    /**
     * Convert list of maps to CSV string with specified headers.
     * @param data list of maps to convert
     * @param headers column headers (null to use keys from first map)
     * @return CSV string
     */
    public String writeToString(List<Map<String, String>> data, String[] headers) {
        if (data.isEmpty()) {
            return "";
        }
        
        // Determine headers
        if (headers == null) {
            headers = data.get(0).keySet().toArray(new String[0]);
        }
        
        StringBuilder sb = new StringBuilder();
        
        // Write header
        if (hasHeader) {
            sb.append(formatRow(headers));
        }
        
        // Write data rows
        for (Map<String, String> map : data) {
            String[] values = new String[headers.length];
            for (int i = 0; i < headers.length; i++) {
                values[i] = map.getOrDefault(headers[i], "");
            }
            sb.append(formatRow(values));
        }
        
        return sb.toString();
    }

    /**
     * Convert list of arrays to CSV string.
     * @param data list of string arrays
     * @param headers column headers (null for no header)
     * @return CSV string
     */
    public String writeArraysToString(List<String[]> data, String[] headers) {
        StringBuilder sb = new StringBuilder();
        
        // Write header
        if (hasHeader && headers != null) {
            sb.append(formatRow(headers));
        }
        
        // Write data rows
        for (String[] row : data) {
            sb.append(formatRow(row));
        }
        
        return sb.toString();
    }

    /**
     * Write CSV to an output stream.
     * @param outputStream output stream to write to
     * @param data list of maps to write
     * @throws IOException if writing fails
     */
    public void write(OutputStream outputStream, List<Map<String, String>> data) throws IOException {
        String content = writeToString(data);
        outputStream.write(content.getBytes(charset));
    }

    /**
     * Append data to an existing CSV file.
     * @param filePath path to the CSV file
     * @param data list of maps to append
     * @throws IOException if file cannot be written
     */
    public void append(Path filePath, List<Map<String, String>> data) throws IOException {
        String content = writeToString(data, null);
        // Remove header when appending
        if (hasHeader && content.startsWith(lineSeparator) == false && content.contains(lineSeparator)) {
            content = content.substring(content.indexOf(lineSeparator) + lineSeparator.length());
        }
        Files.write(filePath, content.getBytes(charset), 
            java.nio.file.StandardOpenOption.CREATE, 
            java.nio.file.StandardOpenOption.APPEND);
    }

    // ==================== PARSING HELPERS ====================

    /**
     * Parse a single CSV line into string array.
     * @param line CSV line to parse
     * @return array of field values
     */
    public String[] parseLine(String line) {
        List<String> fields = new ArrayList<>();
        StringBuilder field = new StringBuilder();
        boolean inQuotes = false;
        
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            
            if (inQuotes) {
                if (c == quote) {
                    // Check for escaped quote
                    if (i + 1 < line.length() && line.charAt(i + 1) == quote) {
                        field.append(quote);
                        i++; // Skip next quote
                    } else {
                        inQuotes = false;
                    }
                } else {
                    field.append(c);
                }
            } else {
                if (c == quote) {
                    inQuotes = true;
                } else if (c == delimiter) {
                    fields.add(processField(field.toString()));
                    field.setLength(0);
                } else {
                    field.append(c);
                }
            }
        }
        
        // Add last field
        fields.add(processField(field.toString()));
        
        return fields.toArray(new String[0]);
    }

    /**
     * Format a row of values as a CSV line.
     * @param values field values
     * @return formatted CSV line with line separator
     */
    public String formatRow(String[] values) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < values.length; i++) {
            if (i > 0) {
                sb.append(delimiter);
            }
            sb.append(formatField(values[i]));
        }
        sb.append(lineSeparator);
        return sb.toString();
    }

    /**
     * Format a single field for CSV output.
     * @param value field value
     * @return formatted field value
     */
    public String formatField(String value) {
        if (value == null) {
            return "";
        }
        
        boolean needsQuote = value.indexOf(quote) >= 0 || 
                            value.indexOf(delimiter) >= 0 || 
                            value.indexOf('\n') >= 0 || 
                            value.indexOf('\r') >= 0;
        
        if (needsQuote) {
            return quote + value.replace(String.valueOf(quote), String.valueOf(quote) + quote) + quote;
        }
        
        return value;
    }

    // ==================== TYPE CONVERSION ====================

    /**
     * Convert string to integer.
     * @param value string value
     * @param defaultValue default value if parsing fails
     * @return integer value
     */
    public static int toInt(String value, int defaultValue) {
        if (value == null || value.trim().isEmpty()) {
            return defaultValue;
        }
        try {
            return Integer.parseInt(value.trim());
        } catch (NumberFormatException e) {
            return defaultValue;
        }
    }

    /**
     * Convert string to long.
     * @param value string value
     * @param defaultValue default value if parsing fails
     * @return long value
     */
    public static long toLong(String value, long defaultValue) {
        if (value == null || value.trim().isEmpty()) {
            return defaultValue;
        }
        try {
            return Long.parseLong(value.trim());
        } catch (NumberFormatException e) {
            return defaultValue;
        }
    }

    /**
     * Convert string to double.
     * @param value string value
     * @param defaultValue default value if parsing fails
     * @return double value
     */
    public static double toDouble(String value, double defaultValue) {
        if (value == null || value.trim().isEmpty()) {
            return defaultValue;
        }
        try {
            return Double.parseDouble(value.trim());
        } catch (NumberFormatException e) {
            return defaultValue;
        }
    }

    /**
     * Convert string to boolean.
     * @param value string value
     * @return true if value is "true", "1", "yes", "y" (case-insensitive)
     */
    public static boolean toBoolean(String value) {
        if (value == null || value.trim().isEmpty()) {
            return false;
        }
        String v = value.trim().toLowerCase();
        return v.equals("true") || v.equals("1") || v.equals("yes") || v.equals("y");
    }

    /**
     * Get string value from map with default.
     * @param map data map
     * @param key column key
     * @param defaultValue default value if key not found
     * @return string value
     */
    public static String getString(Map<String, String> map, String key, String defaultValue) {
        String value = map.get(key);
        return value != null ? value : defaultValue;
    }

    // ==================== UTILITY METHODS ====================

    /**
     * Get delimiter character.
     * @return delimiter character
     */
    public char getDelimiter() {
        return delimiter;
    }

    /**
     * Get quote character.
     * @return quote character
     */
    public char getQuote() {
        return quote;
    }

    /**
     * Check if has header.
     * @return true if first row is header
     */
    public boolean hasHeader() {
        return hasHeader;
    }

    /**
     * Count records in a CSV file (excluding header).
     * @param file CSV file
     * @return number of data rows
     * @throws IOException if file cannot be read
     */
    public int countRecords(File file) throws IOException {
        int[] count = {0};
        stream(file, row -> count[0]++);
        return hasHeader ? Math.max(0, count[0] - 1) : count[0];
    }

    /**
     * Detect delimiter from file content.
     * @param file CSV file
     * @return detected delimiter character
     * @throws IOException if file cannot be read
     */
    public static char detectDelimiter(File file) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(file.toPath(), StandardCharsets.UTF_8)) {
            String firstLine = reader.readLine();
            if (firstLine == null) {
                return DEFAULT_DELIMITER;
            }
            
            // Count potential delimiters
            int comma = countChar(firstLine, ',');
            int tab = countChar(firstLine, '\t');
            int semicolon = countChar(firstLine, ';');
            int pipe = countChar(firstLine, '|');
            
            int max = Math.max(Math.max(comma, tab), Math.max(semicolon, pipe));
            
            if (max == 0) return DEFAULT_DELIMITER;
            if (max == comma) return ',';
            if (max == tab) return '\t';
            if (max == semicolon) return ';';
            return '|';
        }
    }

    // ==================== PRIVATE HELPERS ====================

    private String processField(String field) {
        if (trimWhitespace) {
            return field.trim();
        }
        return field;
    }

    private int countQuotes(String text) {
        int count = 0;
        for (char c : text.toCharArray()) {
            if (c == quote) count++;
        }
        return count;
    }

    private String[] splitLines(String text) {
        List<String> lines = new ArrayList<>();
        StringBuilder sb = new StringBuilder();
        
        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            if (c == '\r') {
                lines.add(sb.toString());
                sb.setLength(0);
                // Skip following \n if exists
                if (i + 1 < text.length() && text.charAt(i + 1) == '\n') {
                    i++;
                }
            } else if (c == '\n') {
                lines.add(sb.toString());
                sb.setLength(0);
            } else {
                sb.append(c);
            }
        }
        
        if (sb.length() > 0) {
            lines.add(sb.toString());
        }
        
        return lines.toArray(new String[0]);
    }

    private static int countChar(String text, char c) {
        int count = 0;
        for (char ch : text.toCharArray()) {
            if (ch == c) count++;
        }
        return count;
    }

    // ==================== STATIC FACTORY METHODS ====================

    /**
     * Create CsvUtils with default settings.
     * @return new CsvUtils instance
     */
    public static CsvUtils create() {
        return new CsvUtils();
    }

    /**
     * Create CsvUtils with no header mode.
     * @return new CsvUtils instance
     */
    public static CsvUtils noHeader() {
        return builder().hasHeader(false).build();
    }

    /**
     * Create CsvUtils with tab delimiter.
     * @return new CsvUtils instance
     */
    public static CsvUtils tabDelimited() {
        return builder().delimiter('\t').build();
    }

    /**
     * Create CsvUtils with semicolon delimiter.
     * @return new CsvUtils instance
     */
    public static CsvUtils semicolonDelimited() {
        return builder().delimiter(';').build();
    }

    /**
     * Create CsvUtils with pipe delimiter.
     * @return new CsvUtils instance
     */
    public static CsvUtils pipeDelimited() {
        return builder().delimiter('|').build();
    }

    /**
     * Quick read CSV file as list of maps.
     * @param file CSV file
     * @return list of maps
     * @throws IOException if file cannot be read
     */
    public static List<Map<String, String>> quickRead(File file) throws IOException {
        return create().readAsMaps(file);
    }

    /**
     * Quick read CSV file as list of arrays.
     * @param file CSV file
     * @return list of string arrays
     * @throws IOException if file cannot be read
     */
    public static List<String[]> quickReadArrays(File file) throws IOException {
        return create().readAsArrays(file);
    }

    /**
     * Quick write data to CSV file.
     * @param file output file
     * @param data list of maps
     * @throws IOException if file cannot be written
     */
    public static void quickWrite(File file, List<Map<String, String>> data) throws IOException {
        create().write(file.toPath(), data);
    }
}