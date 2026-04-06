/**
 * CSV Utilities Example
 * 
 * This file demonstrates the usage of the CSV Utilities module.
 * 
 * To run this example:
 *   cd TypeScript/examples
 *   npx ts-node csv_utils_example.ts
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
} from '../csv_utils/mod';

console.log('=== CSV Utilities Examples ===\n');

// Example 1: Parse CSV string
console.log('1. Parse CSV string:');
const csvString = `
name,age,city
John Doe,30,New York
Jane Smith,25,Los Angeles
Bob Johnson,35,Chicago
Alice Brown,28,San Francisco
`;

const parsed = parse(csvString);
console.log('Headers:', parsed.headers);
console.log('First row:', parsed.rows[0]);
console.log('');

// Example 2: Parse CSV with quotes and special characters
console.log('2. Parse CSV with quotes:');
const csvWithQuotes = `
name,description,price
"Doe, John","A software developer, who loves coding",50000
Jane Smith,"Senior Developer",75000
`;

const parsedQuotes = parse(csvWithQuotes);
console.log('Parsed with quotes:', parsedQuotes.rows);
console.log('');

// Example 3: Convert data to CSV
console.log('3. Convert data to CSV:');
const data = [
  { product: 'Laptop', price: 999.99, stock: 50 },
  { product: 'Mouse', price: 29.99, stock: 200 },
  { product: 'Keyboard', price: 79.99, stock: 100 },
];

const csvOutput = stringify(data);
console.log('Generated CSV:');
console.log(csvOutput);

// Example 4: CSV with custom delimiter
console.log('4. CSV with semicolon delimiter:');
const semicolonData = stringify(data, { delimiter: ';' });
console.log(semicolonData);

// Example 5: Validate CSV
console.log('5. Validate CSV:');
const validCsv = 'name,age\nJohn,30';
const invalidCsv = 'name,age\nJohn,30\n"unclosed quote';
console.log('Is valid CSV:', isValidCsv(validCsv));
console.log('Is valid CSV (unclosed quote):', isValidCsv(invalidCsv));
console.log('');

// Example 6: Get statistics
console.log('6. Get CSV statistics:');
const stats = getStats(parsed);
console.log('Statistics:', stats);
console.log('');

// Example 7: Filter rows
console.log('7. Filter rows (age > 25):');
const filtered = filterRows(parsed, (row) => parseInt(row.age as string) > 25);
console.log('Filtered rows:', filtered.rows);
console.log('');

// Example 8: Select specific columns
console.log('8. Select specific columns:');
const selected = selectColumns(parsed, ['name', 'city']);
console.log('Selected columns:', selected.headers);
console.log('Selected data:', selected.rows);
console.log('');

// Example 9: Sort by column
console.log('9. Sort by age (ascending):');
const sortedAsc = sortBy(parsed, 'age');
console.log('Sorted ascending:', sortedAsc.rows.map(r => `${r.name}: ${r.age}`));

console.log('Sort by age (descending):');
const sortedDesc = sortBy(parsed, 'age', false);
console.log('Sorted descending:', sortedDesc.rows.map(r => `${r.name}: ${r.age}`));
console.log('');

// Example 10: Add a new column
console.log('10. Add a new column:');
const withCountry = addColumn(parsed, 'country', ['USA', 'USA', 'USA', 'USA']);
console.log('New headers:', withCountry.headers);
console.log('First row with country:', withCountry.rows[0]);
console.log('');

// Example 11: Remove a column
console.log('11. Remove a column:');
const withoutCity = removeColumn(parsed, 'city');
console.log('Headers after removal:', withoutCity.headers);
console.log('');

// Example 12: Rename a column
console.log('12. Rename a column:');
const renamed = renameColumn(parsed, 'age', 'years');
console.log('Headers after rename:', renamed.headers);
console.log('First row:', renamed.rows[0]);
console.log('');

// Example 13: Merge two CSV datasets
console.log('13. Merge two CSV datasets:');
const csv1 = `
name,score
Alice,95
Bob,87
`;
const csv2 = `
name,score
Charlie,92
Diana,88
`;

const data1 = parse(csv1);
const data2 = parse(csv2);
const merged = mergeVertical(data1, data2);
console.log('Merged rows:', merged.rows);
console.log('');

// Example 14: Detect delimiter
console.log('14. Detect delimiter:');
const semicolonCsv = 'name;age;city\nJohn;30;NYC';
const tabCsv = 'name\tage\tcity\nJohn\t30\tNYC';
console.log('Detected delimiter (semicolon):', detectDelimiter(semicolonCsv));
console.log('Detected delimiter (tab):', detectDelimiter(tabCsv));
console.log('');

// Example 15: Convert to JSON
console.log('15. Convert CSV to JSON:');
const jsonData = toJson(parsed);
console.log('JSON output:', JSON.stringify(jsonData, null, 2));
console.log('');

// Example 16: Convert from JSON
console.log('16. Convert JSON to CSV:');
const jsonInput = [
  { id: 1, title: 'Task 1', completed: true },
  { id: 2, title: 'Task 2', completed: false },
  { id: 3, title: 'Task 3', completed: true },
];

const fromJsonData = fromJson(jsonInput);
console.log('Headers:', fromJsonData.headers);
console.log('CSV output:');
console.log(stringify(fromJsonData.rows));
console.log('');

// Example 17: Parse CSV without headers
console.log('17. Parse CSV without headers:');
const noHeaderCsv = 'John,30,NYC\nJane,25,LA';
const noHeaderParsed = parse(noHeaderCsv, { header: false });
console.log('Generated headers:', noHeaderParsed.headers);
console.log('Rows:', noHeaderParsed.rows);
console.log('');

// Example 18: Always quote fields
console.log('18. Always quote fields:');
const quoted = stringify(data, { alwaysQuote: true });
console.log(quoted);

console.log('=== All examples completed ===');
