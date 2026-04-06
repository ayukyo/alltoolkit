/**
 * CSV Utilities - TypeScript
 * 
 * A comprehensive CSV (Comma-Separated Values) manipulation utility module
 * providing parsing, generation, transformation, and validation functions
 * with zero dependencies.
 * 
 * @module CsvUtils
 * @version 1.0.0
 */

export interface CsvParseOptions {
  delimiter?: string;
  quote?: string;
  escape?: string;
  header?: boolean;
  trim?: boolean;
  skipEmptyLines?: boolean;
  newline?: string;
}

export interface CsvWriteOptions {
  delimiter?: string;
  quote?: string;
  escape?: string;
  header?: boolean;
  newline?: string;
  alwaysQuote?: boolean;
}

export interface CsvRow {
  [key: string]: string | number | boolean | null;
}

export interface CsvData {
  headers: string[];
  rows: CsvRow[];
  data: string[][];
}

export interface CsvStats {
  rowCount: number;
  columnCount: number;
  emptyCells: number;
  avgRowLength: number;
}

const DEFAULT_PARSE_OPTIONS: CsvParseOptions = {
  delimiter: ',',
  quote: '"',
  escape: '"',
  header: true,
  trim: true,
  skipEmptyLines: true,
};

const DEFAULT_WRITE_OPTIONS: CsvWriteOptions = {
  delimiter: ',',
  quote: '"',
  escape: '"',
  header: true,
  newline: '\n',
  alwaysQuote: false,
};

/**
 * Parse a CSV string into structured data
 * 
 * @param csvString - The CSV string to parse
 * @param options - Parse options
 * @returns Parsed CSV data
 */
export function parse(csvString: string, options: CsvParseOptions = {}): CsvData {
  const opts = { ...DEFAULT_PARSE_OPTIONS, ...options };
  const { delimiter, quote, escape, header, trim, skipEmptyLines } = opts;

  const newline = opts.newline || detectNewline(csvString);
  const lines = csvString.split(newline);
  
  const data: string[][] = [];
  let headers: string[] = [];
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    if (skipEmptyLines && line.trim() === '') {
      continue;
    }
    
    const row = parseLine(line, delimiter!, quote!, escape!);
    
    if (trim) {
      for (let j = 0; j < row.length; j++) {
        row[j] = row[j].trim();
      }
    }
    
    if (i === 0 && header) {
      headers = row;
    } else {
      data.push(row);
    }
  }
  
  if (!header || headers.length === 0) {
    const maxCols = data.reduce((max, row) => Math.max(max, row.length), 0);
    headers = Array.from({ length: maxCols }, (_, i) => `col${i + 1}`);
  }
  
  const rows: CsvRow[] = data.map(row => {
    const obj: CsvRow = {};
    for (let i = 0; i < headers.length; i++) {
      obj[headers[i]] = row[i] !== undefined ? row[i] : '';
    }
    return obj;
  });
  
  return { headers, rows, data };
}

function parseLine(line: string, delimiter: string, quote: string, escape: string): string[] {
  const fields: string[] = [];
  let current = '';
  let inQuotes = false;
  
  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    const nextChar = line[i + 1];
    
    if (char === quote) {
      if (inQuotes && nextChar === quote) {
        current += quote;
        i++;
      } else if (inQuotes) {
        inQuotes = false;
      } else if (current === '') {
        inQuotes = true;
      } else {
        current += char;
      }
    } else if (char === delimiter && !inQuotes) {
      fields.push(current);
      current = '';
    } else {
      current += char;
    }
  }
  
  fields.push(current);
  return fields;
}

function detectNewline(str: string): string {
  if (str.includes('\r\n')) return '\r\n';
  if (str.includes('\r')) return '\r';
  return '\n';
}

/**
 * Convert data to CSV string
 * 
 * @param data - Data to convert
 * @param options - Write options
 * @returns CSV string
 */
export function stringify(data: CsvRow[] | string[][], options: CsvWriteOptions = {}): string {
  const opts = { ...DEFAULT_WRITE_OPTIONS, ...options };
  const { delimiter, quote, escape, header, newline, alwaysQuote } = opts;
  
  if (data.length === 0) return '';
  
  let headers: string[] = [];
  let rows: string[][] = [];
  
  if (isArrayOfObjects(data)) {
    headers = Object.keys(data[0] as CsvRow);
    rows = (data as CsvRow[]).map(row => 
      headers.map(h => formatValue(row[h], quote!, delimiter!, alwaysQuote!))
    );
  } else {
    rows = data as string[][];
    headers = rows[0] || [];
    if (header) rows = rows.slice(1);
  }
  
  const lines: string[] = [];
  
  if (header && headers.length > 0) {
    lines.push(headers.map(h => formatValue(h, quote!, delimiter!, alwaysQuote!)).join(delimiter));
  }
  
  for (const row of rows) {
    lines.push(row.join(delimiter));
  }
  
  return lines.join(newline);
}

function isArrayOfObjects(data: CsvRow[] | string[][]): boolean {
  return data.length > 0 && typeof data[0] === 'object' && !Array.isArray(data[0]);
}

function formatValue(value: unknown, quote: string, delimiter: string, alwaysQuote: boolean): string {
  const str = value === null || value === undefined ? '' : String(value);
  const needsQuote = alwaysQuote || str.includes(quote) || str.includes(delimiter) || str.includes('\n') || str.includes('\r');
  
  if (!needsQuote) return str;
  
  const escaped = str.replace(new RegExp(quote, 'g'), quote + quote);
  return quote + escaped + quote;
}

/**
 * Validate if a string is valid CSV format
 * 
 * @param csvString - String to validate
 * @param options - Parse options
 * @returns True if valid CSV
 */
export function isValidCsv(csvString: string, options: CsvParseOptions = {}): boolean {
  try {
    parse(csvString, options);
    return true;
  } catch {
    return false;
  }
}

/**
 * Get statistics about CSV data
 * 
 * @param csvData - Parsed CSV data
 * @returns Statistics object
 */
export function getStats(csvData: CsvData): CsvStats {
  const rowCount = csvData.rows.length;
  const columnCount = csvData.headers.length;
  
  let emptyCells = 0;
  let totalLength = 0;
  
  for (const row of csvData.data) {
    for (const cell of row) {
      if (cell === '' || cell === null || cell === undefined) {
        emptyCells++;
      }
      totalLength += String(cell).length;
    }
  }
  
  const avgRowLength = rowCount > 0 ? totalLength / rowCount : 0;
  
  return { rowCount, columnCount, emptyCells, avgRowLength };
}

/**
 * Filter rows based on a predicate function
 * 
 * @param csvData - CSV data to filter
 * @param predicate - Filter function
 * @returns Filtered CSV data
 */
export function filterRows(csvData: CsvData, predicate: (row: CsvRow, index: number) => boolean): CsvData {
  const filteredRows = csvData.rows.filter(predicate);
  const filteredData = filteredRows.map(row => csvData.headers.map(h => String(row[h] ?? '')));
  
  return {
    headers: [...csvData.headers],
    rows: filteredRows,
    data: filteredData,
  };
}

/**
 * Select specific columns from CSV data
 * 
 * @param csvData - CSV data
 * @param columns - Columns to select
 * @returns CSV data with selected columns
 */
export function selectColumns(csvData: CsvData, columns: string[]): CsvData {
  const validColumns = columns.filter(c => csvData.headers.includes(c));
  
  const newRows = csvData.rows.map(row => {
    const newRow: CsvRow = {};
    for (const col of validColumns) {
      newRow[col] = row[col];
    }
    return newRow;
  });
  
  const newData = newRows.map(row => validColumns.map(c => String(row[c] ?? '')));
  
  return {
    headers: validColumns,
    rows: newRows,
    data: newData,
  };
}

/**
 * Sort CSV data by a column
 * 
 * @param csvData - CSV data to sort
 * @param column - Column to sort by
 * @param ascending - Sort ascending (default: true)
 * @returns Sorted CSV data
 */
export function sortBy(csvData: CsvData, column: string, ascending: boolean = true): CsvData {
  if (!csvData.headers.includes(column)) {
    return { ...csvData };
  }
  
  const sortedRows = [...csvData.rows].sort((a, b) => {
    const aVal = String(a[column] ?? '');
    const bVal = String(b[column] ?? '');
    
    const aNum = parseFloat(aVal);
    const bNum = parseFloat(bVal);
    
    if (!isNaN(aNum) && !isNaN(bNum)) {
      return ascending ? aNum - bNum : bNum - aNum;
    }
    
    return ascending ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
  });
  
  const sortedData = sortedRows.map(row => csvData.headers.map(h => String(row[h] ?? '')));
  
  return {
    headers: [...csvData.headers],
    rows: sortedRows,
    data: sortedData,
  };
}

/**
 * Add a new column to CSV data
 * 
 * @param csvData - CSV data
 * @param name - New column name
 * @param values - Values for the new column
 * @returns CSV data with new column
 */
export function addColumn(csvData: CsvData, name: string, values: (string | number | boolean | null)[]): CsvData {
  const newHeaders = [...csvData.headers, name];
  
  const newRows = csvData.rows.map((row, i) => ({
    ...row,
    [name]: values[i] ?? null,
  }));
  
  const newData = newRows.map(row => newHeaders.map(h => String(row[h] ?? '')));
  
  return {
    headers: newHeaders,
    rows: newRows,
    data: newData,
  };
}

/**
 * Remove a column from CSV data
 * 
 * @param csvData - CSV data
 * @param name - Column name to remove
 * @returns CSV data without the column
 */
export function removeColumn(csvData: CsvData, name: string): CsvData {
  if (!csvData.headers.includes(name)) {
    return { ...csvData };
  }
  
  const newHeaders = csvData.headers.filter(h => h !== name);
  
  const newRows = csvData.rows.map(row => {
    const newRow: CsvRow = {};
    for (const h of newHeaders) {
      newRow[h] = row[h];
    }
    return newRow;
  });
  
  const newData = newRows.map(row => newHeaders.map(h => String(row[h] ?? '')));
  
  return {
    headers: newHeaders,
    rows: newRows,
    data: newData,
  };
}

/**
 * Rename a column in CSV data
 * 
 * @param csvData - CSV data
 * @param oldName - Current column name
 * @param newName - New column name
 * @returns CSV data with renamed column
 */
export function renameColumn(csvData: CsvData, oldName: string, newName: string): CsvData {
  if (!csvData.headers.includes(oldName)) {
    return { ...csvData };
  }
  
  const newHeaders = csvData.headers.map(h => h === oldName ? newName : h);
  
  const newRows = csvData.rows.map(row => {
    const newRow: CsvRow = {};
    for (const h of newHeaders) {
      const oldKey = h === newName ? oldName : h;
      newRow[h] = row[oldKey];
    }
    return newRow;
  });
  
  return {
    headers: newHeaders,
    rows: newRows,
    data: csvData.data,
  };
}

/**
 * Merge two CSV datasets vertically (add rows)
 * 
 * @param csvData1 - First CSV data
 * @param csvData2 - Second CSV data
 * @returns Merged CSV data
 */
export function mergeVertical(csvData1: CsvData, csvData2: CsvData): CsvData {
  const allHeaders = Array.from(new Set([...csvData1.headers, ...csvData2.headers]));
  
  const mergeRows = (data: CsvData) => {
    return data.rows.map(row => {
      const newRow: CsvRow = {};
      for (const h of allHeaders) {
        newRow[h] = row[h] ?? '';
      }
      return newRow;
    });
  };
  
  const newRows = [...mergeRows(csvData1), ...mergeRows(csvData2)];
  const newData = newRows.map(row => allHeaders.map(h => String(row[h] ?? '')));
  
  return {
    headers: allHeaders,
    rows: newRows,
    data: newData,
  };
}

/**
 * Detect the delimiter used in a CSV string
 * 
 * @param csvString - CSV string to analyze
 * @returns Detected delimiter
 */
export function detectDelimiter(csvString: string): string {
  const firstLine = csvString.split(/\r?\n/)[0] || '';
  
  const delimiters = [',', ';', '\t', '|'];
  let bestDelimiter = ',';
  let maxCount = 0;
  
  for (const delim of delimiters) {
    const count = firstLine.split(delim).length - 1;
    if (count > maxCount) {
      maxCount = count;
      bestDelimiter = delim;
    }
  }
  
  return bestDelimiter;
}

/**
 * Convert CSV data to JSON array
 * 
 * @param csvData - CSV data
 * @returns Array of objects
 */
export function toJson(csvData: CsvData): CsvRow[] {
  return csvData.rows;
}

/**
 * Create CSV data from JSON array
 * 
 * @param json - Array of objects
 * @returns CSV data
 */
export function fromJson(json: CsvRow[]): CsvData {
  if (json.length === 0) {
    return { headers: [], rows: [], data: [] };
  }
  
  const headers = Object.keys(json[0]);
  const data = json.map(row => headers.map(h => String(row[h] ?? '')));
  
  return {
    headers,
    rows: json,
    data,
  };
}

// Default export
export default {
  parse,
  stringify,
  isValidCsv,
  getStats,
  filterRows,
  selectColumns,
  sortBy,
  addColumn,
  removeColumn,
  renameColumn,
  mergeVertical,
  detectDelimiter,
  toJson,
  fromJson,
};
