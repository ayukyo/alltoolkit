/**
 * CSV Utilities Test Suite
 * 
 * Comprehensive tests for the CSV Utilities module.
 */

import {
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
} from './mod';

// Test utilities
let testsPassed = 0;
let testsFailed = 0;

function test(name: string, fn: () => void): void {
  try {
    fn();
    testsPassed++;
    console.log(`✓ ${name}`);
  } catch (e) {
    testsFailed++;
    console.error(`✗ ${name}: ${e}`);
  }
}

function assertEqual(actual: unknown, expected: unknown, msg?: string): void {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`${msg || 'Assertion failed'}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

function assertTrue(value: boolean, msg?: string): void {
  if (!value) {
    throw new Error(msg || 'Expected true');
  }
}

function assertFalse(value: boolean, msg?: string): void {
  if (value) {
    throw new Error(msg || 'Expected false');
  }
}

// Test cases
console.log('Running CSV Utilities Tests...\n');

// Parse tests
test('parse simple CSV', () => {
  const csv = 'name,age\nJohn,30\nJane,25';
  const result = parse(csv);
  assertEqual(result.headers, ['name', 'age']);
  assertEqual(result.rows.length, 2);
  assertEqual(result.rows[0].name, 'John');
  assertEqual(result.rows[0].age, '30');
});

test('parse CSV with quotes', () => {
  const csv = 'name,description\n"John Doe","A person, who codes"\nJane,Developer';
  const result = parse(csv);
  assertEqual(result.rows[0].name, 'John Doe');
  assertEqual(result.rows[0].description, 'A person, who codes');
});

test('parse CSV with escaped quotes', () => {
  const csv = 'name,quote\nJohn,"He said ""Hello"""\nJane,Hi';
  const result = parse(csv);
  assertEqual(result.rows[0].quote, 'He said "Hello"');
});

test('parse CSV without headers', () => {
  const csv = 'John,30\nJane,25';
  const result = parse(csv, { header: false });
  assertEqual(result.headers, ['col1', 'col2']);
  assertEqual(result.rows[0].col1, 'John');
});

test('parse CSV with custom delimiter', () => {
  const csv = 'name;age\nJohn;30\nJane;25';
  const result = parse(csv, { delimiter: ';' });
  assertEqual(result.headers, ['name', 'age']);
  assertEqual(result.rows[0].name, 'John');
});

test('parse CSV with CRLF line endings', () => {
  const csv = 'name,age\r\nJohn,30\r\nJane,25';
  const result = parse(csv);
  assertEqual(result.rows.length, 2);
});

test('parse CSV with empty lines', () => {
  const csv = 'name,age\n\nJohn,30\n\nJane,25\n';
  const result = parse(csv);
  assertEqual(result.rows.length, 2);
});

test('parse CSV with trim disabled', () => {
  const csv = 'name,age\n John , 30 \nJane,25';
  const result = parse(csv, { trim: false });
  assertEqual(result.rows[0].name, ' John ');
});

// Stringify tests
test('stringify simple data', () => {
  const data = [{ name: 'John', age: 30 }, { name: 'Jane', age: 25 }];
  const result = stringify(data);
  assertTrue(result.includes('name,age'));
  assertTrue(result.includes('John,30'));
});

test('stringify with quotes', () => {
  const data = [{ name: 'John, Jr.', age: 30 }];
  const result = stringify(data);
  assertTrue(result.includes('"John, Jr."'));
});

test('stringify 2D array', () => {
  const data = [['name', 'age'], ['John', '30'], ['Jane', '25']];
  const result = stringify(data);
  assertTrue(result.includes('name,age'));
});

test('stringify with custom delimiter', () => {
  const data = [{ name: 'John', age: 30 }];
  const result = stringify(data, { delimiter: ';' });
  assertTrue(result.includes('name;age'));
});

test('stringify without headers', () => {
  const data = [{ name: 'John', age: 30 }];
  const result = stringify(data, { header: false });
  assertFalse(result.includes('name,age'));
});

test('stringify with alwaysQuote', () => {
  const data = [{ name: 'John', age: 30 }];
  const result = stringify(data, { alwaysQuote: true });
  assertTrue(result.includes('"John"'));
  assertTrue(result.includes('"30"'));
});

// Validation tests
test('isValidCsv with valid CSV', () => {
  assertTrue(isValidCsv('name,age\nJohn,30'));
});

test('isValidCsv with empty string', () => {
  assertTrue(isValidCsv(''));
});

// Stats tests
test('getStats', () => {
  const csv = 'name,age\nJohn,30\nJane,25';
  const data = parse(csv);
  const stats = getStats(data);
  assertEqual(stats.rowCount, 2);
  assertEqual(stats.columnCount, 2);
  assertEqual(stats.emptyCells, 0);
  assertTrue(stats.avgRowLength > 0);
});

test('getStats with empty cells', () => {
  const csv = 'name,age\nJohn,\n,25';
  const data = parse(csv);
  const stats = getStats(data);
  assertEqual(stats.emptyCells, 2);
});

// Filter tests
test('filterRows', () => {
  const csv = 'name,age\nJohn,30\nJane,25\nBob,35';
  const data = parse(csv);
  const filtered = filterRows(data, (row) => parseInt(row.age as string) > 25);
  assertEqual(filtered.rows.length, 2);
});

// Select columns tests
test('selectColumns', () => {
  const csv = 'name,age,city\nJohn,30,NYC\nJane,25,LA';
  const data = parse(csv);
  const selected = selectColumns(data, ['name', 'city']);
  assertEqual(selected.headers, ['name', 'city']);
  assertEqual(selected.rows[0].name, 'John');
  assertEqual(selected.rows[0].city, 'NYC');
});

test('selectColumns with invalid column', () => {
  const csv = 'name,age\nJohn,30';
  const data = parse(csv);
  const selected = selectColumns(data, ['name', 'invalid']);
  assertEqual(selected.headers, ['name']);
});

// Sort tests
test('sortBy numeric ascending', () => {
  const csv = 'name,age\nBob,35\nJohn,30\nJane,25';
  const data = parse(csv);
  const sorted = sortBy(data, 'age');
  assertEqual(sorted.rows[0].name, 'Jane');
  assertEqual(sorted.rows[2].name, 'Bob');
});

test('sortBy numeric descending', () => {
  const csv = 'name,age\nBob,35\nJohn,30\nJane,25';
  const data = parse(csv);
  const sorted = sortBy(data, 'age', false);
  assertEqual(sorted.rows[0].name, 'Bob');
  assertEqual(sorted.rows[2].name, 'Jane');
});

test('sortBy string', () => {
  const csv = 'name,age\nBob,35\nAlice,30\nCharlie,25';
  const data = parse(csv);
  const sorted = sortBy(data, 'name');
  assertEqual(sorted.rows[0].name, 'Alice');
  assertEqual(sorted.rows[2].name, 'Charlie');
});

test('sortBy invalid column', () => {
  const csv = 'name,age\nJohn,30';
  const data = parse(csv);
  const sorted = sortBy(data, 'invalid');
  assertEqual(sorted.rows.length, 1);
});

// Add column tests
test('addColumn', () => {
  const csv = 'name,age\nJohn,30\nJane,25';
  const data = parse(csv);
  const updated = addColumn(data, 'city', ['NYC', 'LA']);
  assertEqual(updated.headers, ['name', 'age', 'city']);
  assertEqual(updated.rows[0].city, 'NYC');
  assertEqual(updated.rows[1].city, 'LA');
});

// Remove column tests
test('removeColumn', () => {
  const csv = 'name,age,city\nJohn,30,NYC';
  const data = parse(csv);
  const updated = removeColumn(data, 'age');
  assertEqual(updated.headers, ['name', 'city']);
  assertEqual(updated.rows[0].name, 'John');
});

test('removeColumn invalid', () => {
  const csv = 'name,age\nJohn,30';
  const data = parse(csv);
  const updated = removeColumn(data, 'invalid');
  assertEqual(updated.headers, ['name', 'age']);
});

// Rename column tests
test('renameColumn', () => {
  const csv = 'name,age\nJohn,30';
  const data = parse(csv);
  const updated = renameColumn(data, 'age', 'years');
  assertEqual(updated.headers, ['name', 'years']);
  assertEqual(updated.rows[0].years, '30');
});

// Merge tests
test('mergeVertical', () => {
  const csv1 = 'name,age\nJohn,30';
  const csv2 = 'name,age\nJane,25';
  const data1 = parse(csv1);
  const data2 = parse(csv2);
  const merged = mergeVertical(data1, data2);
  assertEqual(merged.rows.length, 2);
  assertEqual(merged.rows[0].name, 'John');
  assertEqual(merged.rows[1].name, 'Jane');
});

// Detect delimiter tests
test('detectDelimiter comma', () => {
  const csv = 'name,age,city\nJohn,30,NYC';
  assertEqual(detectDelimiter(csv), ',');
});

test('detectDelimiter semicolon', () => {
  const csv = 'name;age;city\nJohn;30;NYC';
  assertEqual(detectDelimiter(csv), ';');
});

test('detectDelimiter tab', () => {
  const csv = 'name\tage\tcity\nJohn\t30\tNYC';
  assertEqual(detectDelimiter(csv), '\t');
});

// JSON conversion tests
test('toJson', () => {
  const csv = 'name,age\nJohn,30\nJane,25';
  const data = parse(csv);
  const json = toJson(data);
  assertEqual(json.length, 2);
  assertEqual(json[0].name, 'John');
});

test('fromJson', () => {
  const json = [{ name: 'John', age: 30 }, { name: 'Jane', age: 25 }];
  const data = fromJson(json);
  assertEqual(data.headers, ['name', 'age']);
  assertEqual(data.rows.length, 2);
});

test('fromJson empty', () => {
  const json: Record<string, unknown>[] = [];
  const data = fromJson(json);
  assertEqual(data.headers, []);
  assertEqual(data.rows.length, 0);
});

// Run tests
console.log(`\n${'='.repeat(50)}`);
console.log(`Tests completed: ${testsPassed} passed, ${testsFailed} failed`);
console.log(`${'='.repeat(50)}`);

if (testsFailed > 0) {
  process.exit(1);
}