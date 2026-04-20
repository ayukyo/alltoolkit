/**
 * Top-N Utils Usage Examples
 */

import {
  TopNFinder,
  topNLargest,
  topNSmallest,
  topNLargestStrings,
  topNSmallestStrings,
  topNLargestItems,
  topNSmallestItems,
  kthSmallest,
  kthLargest,
  median,
  percentile,
  ScoredItem,
} from './topn';

console.log('=== Top-N Utils Examples ===\n');

// Example 1: Find top N largest numbers
console.log('1. Top N Largest Numbers');
const numbers = [45, 23, 67, 12, 89, 34, 78, 56, 90, 11, 33, 44];
const finder = new TopNFinder(5);
const largest = finder.largest(numbers);
console.log(`   Data: [${numbers.join(', ')}]`);
console.log(`   Top 5 Largest: [${largest.join(', ')}]\n`);

// Example 2: Find top N smallest numbers
console.log('2. Top N Smallest Numbers');
const smallest = finder.smallest(numbers);
console.log(`   Data: [${numbers.join(', ')}]`);
console.log(`   Top 5 Smallest: [${smallest.join(', ')}]\n`);

// Example 3: Convenience functions
console.log('3. Convenience Functions (Quick API)');
const quickData = [15, 3, 9, 8, 2, 6, 12, 1, 7];
const top3 = topNLargest(quickData, 3);
const bottom3 = topNSmallest(quickData, 3);
console.log(`   Data: [${quickData.join(', ')}]`);
console.log(`   Top 3 Largest: [${top3.join(', ')}]`);
console.log(`   Top 3 Smallest: [${bottom3.join(', ')}]\n`);

// Example 4: String operations
console.log('4. Top N Strings (Lexicographic)');
const words = ['zebra', 'apple', 'mango', 'banana', 'cherry', 'orange'];
const topWords = topNLargestStrings(words, 3);
const bottomWords = topNSmallestStrings(words, 3);
console.log(`   Data: [${words.join(', ')}]`);
console.log(`   Top 3 (Z-A): [${topWords.join(', ')}]`);
console.log(`   Top 3 (A-Z): [${bottomWords.join(', ')}]\n`);

// Example 5: Custom scored items
console.log('5. Custom Items with Scores (e.g., Product Ratings)');
interface Product {
  name: string;
  category?: string;
}

const products: ScoredItem<Product>[] = [
  { value: { name: 'Laptop' }, score: 4.8 },
  { value: { name: 'Phone' }, score: 4.5 },
  { value: { name: 'Tablet' }, score: 4.2 },
  { value: { name: 'Monitor' }, score: 4.7 },
  { value: { name: 'Keyboard' }, score: 4.1 },
  { value: { name: 'Mouse' }, score: 4.9 },
  { value: { name: 'Headphones' }, score: 4.6 },
];

const topProducts = topNLargestItems(products, 3);
console.log('   Top 3 Highest Rated Products:');
topProducts.forEach((item, i) => {
  console.log(`   ${i + 1}. ${item.value.name} (Score: ${item.score})`);
});
console.log();

// Example 6: K-th element selection
console.log('6. K-th Element Selection');
const testData = [7, 2, 5, 3, 9, 1, 6, 4, 8];
console.log(`   Data: [${testData.join(', ')}]`);
console.log(`   3rd Smallest: ${kthSmallest(testData, 3)}`);
console.log(`   2nd Largest: ${kthLargest(testData, 2)}\n`);

// Example 7: Statistical functions
console.log('7. Statistical Functions');
const scores = [85, 92, 78, 95, 88, 72, 90, 82, 79, 91];
console.log(`   Scores: [${scores.join(', ')}]`);
console.log(`   Median: ${median(scores)}`);
console.log(`   25th Percentile: ${percentile(scores, 25)}`);
console.log(`   75th Percentile: ${percentile(scores, 75)}\n`);

// Example 8: Real-world use case - API response times
console.log('8. Real-World: Finding Slowest API Endpoints');
interface Endpoint {
  path: string;
}

const responseTimes: ScoredItem<Endpoint>[] = [
  { value: { path: '/api/users' }, score: 45 },
  { value: { path: '/api/products' }, score: 120 },
  { value: { path: '/api/orders' }, score: 89 },
  { value: { path: '/api/search' }, score: 230 },
  { value: { path: '/api/auth' }, score: 35 },
  { value: { path: '/api/reports' }, score: 450 },
  { value: { path: '/api/export' }, score: 380 },
  { value: { path: '/api/import' }, score: 520 },
];

const slowest = topNLargestItems(responseTimes, 3);
console.log('   Top 3 Slowest API Endpoints:');
slowest.forEach((item, i) => {
  console.log(`   ${i + 1}. ${item.value.path} (${item.score}ms)`);
});
console.log();

// Example 9: Student grades analysis
console.log('9. Student Grades Analysis');
interface Student {
  name: string;
}

const grades: ScoredItem<Student>[] = [
  { value: { name: 'Alice' }, score: 95 },
  { value: { name: 'Bob' }, score: 87 },
  { value: { name: 'Charlie' }, score: 92 },
  { value: { name: 'Diana' }, score: 88 },
  { value: { name: 'Eve' }, score: 91 },
  { value: { name: 'Frank' }, score: 85 },
  { value: { name: 'Grace' }, score: 93 },
  { value: { name: 'Henry' }, score: 79 },
];

const topStudents = topNLargestItems(grades, 3);
const struggling = topNSmallestItems(grades, 3);

console.log('   Top 3 Students:');
topStudents.forEach((item, i) => {
  console.log(`   ${i + 1}. ${item.value.name} (${item.score})`);
});

console.log('   Bottom 3 Students (for extra help):');
struggling.forEach((item, i) => {
  console.log(`   ${i + 1}. ${item.value.name} (${item.score})`);
});

console.log(`   Class Median: ${median(grades.map(g => g.score))}\n`);

// Example 10: Large dataset simulation
console.log('10. Large Dataset Performance');
const largeData = Array.from({ length: 100000 }, () => Math.floor(Math.random() * 1000000));

const startLargest = Date.now();
const top100Largest = topNLargest(largeData, 100);
const elapsedLargest = Date.now() - startLargest;

const startSmallest = Date.now();
const top100Smallest = topNSmallest(largeData, 100);
const elapsedSmallest = Date.now() - startSmallest;

console.log(`   Found top 100 largest from 100,000 elements in ${elapsedLargest}ms`);
console.log(`   Found top 100 smallest from 100,000 elements in ${elapsedSmallest}ms`);
console.log(`   Largest result (first 5): [${top100Largest.slice(0, 5).join(', ')}]...`);
console.log(`   Smallest result (first 5): [${top100Smallest.slice(0, 5).join(', ')}]...\n`);

console.log('=== All Examples Complete ===');