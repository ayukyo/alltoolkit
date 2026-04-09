/**
 * String Utils - Validation Examples
 * 
 * Demonstrates input validation and similarity checking.
 */

import {
  isAlpha,
  isAlphanumeric,
  isNumeric,
  isInteger,
  isFloat,
  isEmpty,
  isNotEmpty,
  startsWith,
  endsWith,
  contains,
  levenshtein,
  similarity,
  longestCommonSubstring,
  equals,
  slugify,
  randomString,
} from '../mod.ts';

console.log('📝 String Utils - Validation Examples\n');
console.log('=' .repeat(50));

// Basic Validation
console.log('\n1️⃣  Basic Validation:');
console.log('-' .repeat(30));

const testValues = ['Hello', 'Hello123', '123', '12.34', '', '   ', 'Hello!'];

console.log('Value         | Alpha | AlNum | Numeric | Int  | Float | Empty');
console.log('-'.repeat(65));
testValues.forEach(val => {
  const display = val || '(empty)';
  console.log(
    `${display.padEnd(13)} | ${String(isAlpha(val)).padEnd(5)} | ` +
    `${String(isAlphanumeric(val)).padEnd(5)} | ${String(isNumeric(val)).padEnd(7)} | ` +
    `${String(isInteger(val)).padEnd(4)} | ${String(isFloat(val)).padEnd(5)} | ` +
    `${isEmpty(val)}`
  );
});

// String Comparison
console.log('\n2️⃣  String Comparison:');
console.log('-' .repeat(30));

const str1 = 'Hello';
const str2 = 'hello';
const str3 = 'Hello World';

console.log(`"${str1}" vs "${str2}":`);
console.log(`  equals (case-insensitive): ${equals(str1, str2)}`);
console.log(`  equals (case-sensitive):   ${equals(str1, str2, true)}`);

console.log(`\n"${str3}":`);
console.log(`  startsWith "Hello":  ${startsWith(str3, 'Hello')}`);
console.log(`  endsWith "World":    ${endsWith(str3, 'World')}`);
console.log(`  contains "lo Wo":    ${contains(str3, 'lo Wo')}`);

// Similarity Checking
console.log('\n3️⃣  Similarity Checking:');
console.log('-' .repeat(30));

interface SimilarityTest {
  str1: string;
  str2: string;
  description: string;
}

const similarityTests: SimilarityTest[] = [
  { str1: 'kitten', str2: 'sitting', description: 'Classic example' },
  { str1: 'typescript', str2: 'javascript', description: 'Programming languages' },
  { str1: 'hello', str2: 'hello', description: 'Identical' },
  { str1: 'abc', str2: 'xyz', description: 'Completely different' },
  { str1: 'test', str2: 'testing', description: 'Prefix match' },
];

console.log('String 1      | String 2     | Distance | Similarity | Description');
console.log('-'.repeat(80));
similarityTests.forEach(({ str1, str2, description }) => {
  const distance = levenshtein(str1, str2);
  const sim = similarity(str1, str2);
  console.log(
    `${str1.padEnd(13)} | ${str2.padEnd(12)} | ${String(distance).padEnd(8)} | ` +
    `${sim.toFixed(2).padEnd(10)} | ${description}`
  );
});

// Longest Common Substring
console.log('\n4️⃣  Longest Common Substring:');
console.log('-' .repeat(30));

const pairs = [
  ['abcdef', 'zcdgh'],
  ['hello world', 'world peace'],
  ['typescript', 'javascript'],
];

pairs.forEach(([str1, str2]) => {
  const common = longestCommonSubstring(str1, str2);
  console.log(`"${str1}" & "${str2}" → "${common}"`);
});

// Form Validation Example
console.log('\n5️⃣  Form Validation Example:');
console.log('-' .repeat(30));

interface FormData {
  username: string;
  password: string;
  age: string;
  email: string;
}

interface ValidationResult {
  field: string;
  valid: boolean;
  error?: string;
}

function validateForm(data: FormData): ValidationResult[] {
  const results: ValidationResult[] = [];
  
  // Username: alphanumeric, 3-20 chars
  if (isEmpty(data.username)) {
    results.push({ field: 'username', valid: false, error: 'Username is required' });
  } else if (!isAlphanumeric(data.username)) {
    results.push({ field: 'username', valid: false, error: 'Username must be alphanumeric' });
  } else if (data.username.length < 3 || data.username.length > 20) {
    results.push({ field: 'username', valid: false, error: 'Username must be 3-20 characters' });
  } else {
    results.push({ field: 'username', valid: true });
  }
  
  // Password: not empty, at least 8 chars
  if (isEmpty(data.password)) {
    results.push({ field: 'password', valid: false, error: 'Password is required' });
  } else if (data.password.length < 8) {
    results.push({ field: 'password', valid: false, error: 'Password must be at least 8 characters' });
  } else {
    results.push({ field: 'password', valid: true });
  }
  
  // Age: integer between 1 and 150
  if (isEmpty(data.age)) {
    results.push({ field: 'age', valid: false, error: 'Age is required' });
  } else if (!isInteger(data.age)) {
    results.push({ field: 'age', valid: false, error: 'Age must be a whole number' });
  } else {
    const ageNum = parseInt(data.age, 10);
    if (ageNum < 1 || ageNum > 150) {
      results.push({ field: 'age', valid: false, error: 'Age must be between 1 and 150' });
    } else {
      results.push({ field: 'age', valid: true });
    }
  }
  
  // Email: basic format check (contains @ and .)
  if (isEmpty(data.email)) {
    results.push({ field: 'email', valid: false, error: 'Email is required' });
  } else if (!contains(data.email, '@') || !contains(data.email, '.')) {
    results.push({ field: 'email', valid: false, error: 'Invalid email format' });
  } else {
    results.push({ field: 'email', valid: true });
  }
  
  return results;
}

const testForms: FormData[] = [
  { username: 'john123', password: 'securepass123', age: '25', email: 'john@example.com' },
  { username: 'ab', password: 'short', age: '200', email: 'invalid' },
  { username: 'valid_user!', password: 'goodpass123', age: 'abc', email: 'test@test.com' },
];

testForms.forEach((form, index) => {
  console.log(`\nForm ${index + 1}:`);
  const results = validateForm(form);
  results.forEach(({ field, valid, error }) => {
    console.log(`  ${field}: ${valid ? '✅' : '❌'} ${error || ''}`);
  });
});

// Search Suggestion Example (Fuzzy Matching)
console.log('\n6️⃣  Search Suggestion Example (Fuzzy Matching):');
console.log('-' .repeat(30));

const products = [
  'iPhone 15 Pro',
  'iPhone 15',
  'iPad Pro',
  'MacBook Pro',
  'Apple Watch',
  'AirPods Pro',
];

const searchQuery = 'iphone pro';

console.log(`Search: "${searchQuery}"\n`);

const suggestions = products
  .map(product => ({
    product,
    similarity: similarity(searchQuery.toLowerCase(), product.toLowerCase()),
  }))
  .filter(({ similarity }) => similarity > 0.3)
  .sort((a, b) => b.similarity - a.similarity);

console.log('Suggestions:');
suggestions.forEach(({ product, similarity }) => {
  console.log(`  ${product} (${(similarity * 100).toFixed(0)}% match)`);
});

// Random ID Generation
console.log('\n7️⃣  Random ID Generation:');
console.log('-' .repeat(30));

console.log('Session IDs:');
for (let i = 0; i < 3; i++) {
  console.log(`  ${randomString(16)}`);
}

console.log('\nNumeric PINs:');
for (let i = 0; i < 3; i++) {
  console.log(`  ${randomString(6, '0123456789')}`);
}

console.log('\nURL-safe Tokens:');
for (let i = 0; i < 3; i++) {
  const token = slugify(randomString(20));
  console.log(`  ${token}`);
});

console.log('\n' + '=' .repeat(50));
console.log('✅ Examples completed!\n');
