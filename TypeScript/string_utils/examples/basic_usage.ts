/**
 * String Utils - Basic Usage Examples
 * 
 * Demonstrates common string utility operations.
 */

import {
  toCamelCase,
  toSnakeCase,
  toKebabCase,
  toPascalCase,
  capitalize,
  slugify,
  truncate,
  padLeft,
  reverse,
} from '../mod.ts';

console.log('📝 String Utils - Basic Usage Examples\n');
console.log('=' .repeat(50));

// Case Conversion
console.log('\n1️⃣  Case Conversion:');
console.log('-' .repeat(30));

const input = 'hello_world_test';
console.log(`Input: "${input}"`);
console.log(`  → camelCase:      ${toCamelCase(input)}`);
console.log(`  → PascalCase:     ${toPascalCase(input)}`);
console.log(`  → snake_case:     ${toSnakeCase(input)}`);
console.log(`  → kebab-case:     ${toKebabCase(input)}`);

const camelInput = 'helloWorldTest';
console.log(`\nInput: "${camelInput}"`);
console.log(`  → snake_case:     ${toSnakeCase(camelInput)}`);
console.log(`  → kebab-case:     ${toKebabCase(camelInput)}`);
console.log(`  → PascalCase:     ${toPascalCase(camelInput)}`);

// String Formatting
console.log('\n2️⃣  String Formatting:');
console.log('-' .repeat(30));

const name = 'typescript';
console.log(`Input: "${name}"`);
console.log(`  → Capitalized:    ${capitalize(name)}`);
console.log(`  → Slug:           ${slugify(name + ' STRING UTILS!')}`);

const longText = 'This is a very long text that needs to be truncated';
console.log(`\nInput: "${longText}"`);
console.log(`  → Truncated:      ${truncate(longText, { length: 25 })}`);
console.log(`  → Preserve words: ${truncate(longText, { length: 25, preserveWords: true })}`);

// Padding
console.log('\n3️⃣  Padding:');
console.log('-' .repeat(30));

const numbers = [1, 23, 456, 7890];
console.log('ID formatting:');
numbers.forEach(num => {
  console.log(`  ${num} → ${padLeft(String(num), 4, '0')}`);
});

// String Manipulation
console.log('\n4️⃣  String Manipulation:');
console.log('-' .repeat(30));

const text = 'Hello, World!';
console.log(`Input: "${text}"`);
console.log(`  → Reversed:       ${reverse(text)}`);
console.log(`  → Capitalized:    ${capitalize(text)}`);

// Real-world Example: API Response Transformation
console.log('\n5️⃣  Real-world Example - API Response:');
console.log('-' .repeat(30));

interface ApiResponse {
  user_name: string;
  email_address: string;
  created_at: string;
}

const apiData: ApiResponse = {
  user_name: 'john_doe',
  email_address: 'john@example.com',
  created_at: '2024-01-15',
};

console.log('Original API response (snake_case):');
console.log(JSON.stringify(apiData, null, 2));

// Transform to camelCase for frontend
const frontendData = {
  userName: toCamelCase(apiData.user_name),
  emailAddress: toCamelCase(apiData.email_address),
  createdAt: toCamelCase(apiData.created_at),
};

console.log('\nTransformed for frontend (camelCase):');
console.log(JSON.stringify(frontendData, null, 2));

// Generate URL slug from username
const slug = slugify(apiData.user_name);
console.log(`\nProfile URL: /users/${slug}`);

console.log('\n' + '=' .repeat(50));
console.log('✅ Examples completed!\n');
