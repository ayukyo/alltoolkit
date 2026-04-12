/**
 * Array Utilities Usage Examples for ArkTS
 * 
 * Demonstrates practical use cases for the array_utils module
 * in HarmonyOS application development.
 */

import {
  isEmpty, isNotEmpty, size,
  first, last, get,
  find, findIndex, contains, containsAll,
  filter, filterNot, filterNull,
  map, mapNotNull, flatMap, flatten,
  sort, sortBy, sortByDesc, reverse, shuffle,
  unique, uniqueBy, union, intersection, difference,
  groupBy, partition, chunk, splitAt,
  take, takeLast, drop, slice,
  sum, sumBy, average, averageBy, min, max, minBy, maxBy, count, countBy,
  randomElement, randomElements,
  insert, removeAt, removeFirst, removeAll, append, prepend, concat,
  updateAt, updateWhere,
  equals, equalsIgnoreOrder,
  range, fill, fillFn,
  forEach, forEachRight, reduce, every, some, none,
  join, joinWith, zip, zipWith, unzip, rotate, interleave,
  ArrayUtils
} from '../array_utils/mod';

// ============================================
// Example 1: User List Management
// ============================================

interface User {
  id: number;
  name: string;
  age: number;
  role: 'admin' | 'user' | 'guest';
  active: boolean;
}

const users: User[] = [
  { id: 1, name: 'Alice', age: 28, role: 'admin', active: true },
  { id: 2, name: 'Bob', age: 35, role: 'user', active: true },
  { id: 3, name: 'Charlie', age: 22, role: 'user', active: false },
  { id: 4, name: 'Diana', age: 30, role: 'admin', active: true },
  { id: 5, name: 'Eve', age: 25, role: 'guest', active: false },
];

// Find active admins
const activeAdmins = filter(users, u => u.active && u.role === 'admin');
console.log('Active admins:', activeAdmins.map(u => u.name).join(', '));

// Find user by ID
const userById = find(users, u => u.id === 3);
console.log('User with ID 3:', userById?.name);

// Get oldest user
const oldest = maxBy(users, u => u.age);
console.log('Oldest user:', oldest?.name, 'age:', oldest?.age);

// Group users by role
const byRole = groupBy(users, u => u.role);
console.log('Admins:', byRole['admin'].map(u => u.name).join(', '));

// Partition active vs inactive
const [active, inactive] = partition(users, u => u.active);
console.log('Active users:', active.length);
console.log('Inactive users:', inactive.length);

// ============================================
// Example 2: Data Processing Pipeline
// ============================================

interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  inStock: boolean;
}

const products: Product[] = [
  { id: 1, name: 'Laptop', category: 'electronics', price: 999, inStock: true },
  { id: 2, name: 'Phone', category: 'electronics', price: 699, inStock: true },
  { id: 3, name: 'Book', category: 'books', price: 29, inStock: false },
  { id: 4, name: 'Desk', category: 'furniture', price: 199, inStock: true },
  { id: 5, name: 'Chair', category: 'furniture', price: 149, inStock: true },
  { id: 6, name: 'Tablet', category: 'electronics', price: 499, inStock: false },
];

// Filter available products
const available = filter(products, p => p.inStock);

// Get products under $200
const affordable = filter(products, p => p.price < 200);

// Sort by price descending
const sortedByPrice = sortByDesc(products, p => p.price);
console.log('Most expensive:', first(sortedByPrice)?.name);

// Calculate total inventory value
const totalValue = sumBy(filter(products, p => p.inStock), p => p.price);
console.log('Total inventory value:', totalValue);

// Average price by category
const electronics = filter(products, p => p.category === 'electronics');
const avgElectronicsPrice = averageBy(electronics, p => p.price);
console.log('Avg electronics price:', avgElectronicsPrice);

// Group by category with stats
const byCategory = groupBy(products, p => p.category);
forEach(Object.keys(byCategory), cat => {
  const catProducts = byCategory[cat];
  const avg = averageBy(catProducts, p => p.price);
  console.log(`${cat}: ${catProducts.length} products, avg price: ${avg}`);
});

// ============================================
// Example 3: Form Validation
// ============================================

interface FormField {
  name: string;
  value: string;
  required: boolean;
  valid: boolean;
}

const formFields: FormField[] = [
  { name: 'username', value: 'john_doe', required: true, valid: true },
  { name: 'email', value: 'john@example.com', required: true, valid: true },
  { name: 'phone', value: '', required: false, valid: true },
  { name: 'address', value: '', required: true, valid: false },
];

// Check if all required fields are valid
const requiredValid = every(
  filter(formFields, f => f.required),
  f => f.valid
);
console.log('Form valid:', requiredValid);

// Find invalid fields
const invalidFields = filter(formFields, f => !f.valid);
console.log('Invalid fields:', join(invalidFields.map(f => f.name), ', '));

// Get first invalid required field
const firstInvalid = find(formFields, f => f.required && !f.valid);
console.log('First invalid required:', firstInvalid?.name);

// ============================================
// Example 4: List UI Component
// ============================================

// Paginated list display
const allItems = range(1, 100); // Items 1-99
const pageSize = 10;
const currentPage = 2;

const pageItems = chunk(allItems, pageSize);
const currentPageItems = get(pageItems, currentPage - 1);
console.log('Page 2 items:', currentPageItems);

// Display with filtering
const filteredItems = filter(allItems, i => i % 3 === 0);
const filteredPageItems = take(filteredItems, pageSize);
console.log('Filtered items (divisible by 3):', filteredPageItems);

// Sort options
const sortOptions = ['price-asc', 'price-desc', 'name-asc', 'name-desc'];
const selectedSort = first(sortOptions);
console.log('Default sort:', selectedSort);

// ============================================
// Example 5: Shopping Cart
// ============================================

interface CartItem {
  productId: number;
  name: string;
  price: number;
  quantity: number;
}

let cart: CartItem[] = [
  { productId: 1, name: 'Laptop', price: 999, quantity: 1 },
  { productId: 2, name: 'Phone', price: 699, quantity: 2 },
];

// Add item (immutable)
cart = append(cart, { productId: 4, name: 'Desk', price: 199, quantity: 1 });
console.log('Cart items:', cart.length);

// Update quantity
cart = updateWhere(cart, i => i.productId === 2, i => ({
  ...i,
  quantity: i.quantity + 1
}));
const phoneItem = find(cart, i => i.productId === 2);
console.log('Phone quantity:', phoneItem?.quantity);

// Remove item
cart = removeFirst(cart, find(cart, i => i.productId === 4) as CartItem);
console.log('Cart after removal:', cart.length);

// Calculate total
const total = sumBy(cart, i => i.price * i.quantity);
console.log('Cart total:', total);

// ============================================
// Example 6: Search and Filter UI
// ============================================

const searchItems = ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry', 'Fig', 'Grape'];

// Search with contains
const searchResults = filter(searchItems, item => 
  contains(item.toLowerCase(), 'a')
);
console.log('Items containing "a":', searchResults);

// Autocomplete suggestions
const query = 'ap';
const suggestions = filter(searchItems, item =>
  startsWith(item.toLowerCase() as unknown as string[], query.toLowerCase().split(''))
);
// Note: For string prefix, use string_utils.startsWith instead

// ============================================
// Example 7: Analytics Dashboard
// ============================================

interface Metric {
  name: string;
  value: number;
  timestamp: number;
}

const metrics: Metric[] = [
  { name: 'views', value: 1000, timestamp: 1 },
  { name: 'clicks', value: 150, timestamp: 2 },
  { name: 'views', value: 1200, timestamp: 3 },
  { name: 'clicks', value: 200, timestamp: 4 },
  { name: 'views', value: 800, timestamp: 5 },
];

// Total views
const views = filter(metrics, m => m.name === 'views');
const totalViews = sumBy(views, m => m.value);
console.log('Total views:', totalViews);

// Average clicks
const clicks = filter(metrics, m => m.name === 'clicks');
const avgClicks = averageBy(clicks, m => m.value);
console.log('Average clicks:', avgClicks);

// Min/Max views
const minViews = minBy(views, m => m.value);
const maxViews = maxBy(views, m => m.value);
console.log('Views range:', minViews?.value, '-', maxViews?.value);

// Metric count by name
const metricCounts = countBy(metrics, m => m.name);
console.log('Metric counts:', metricCounts);

// ============================================
// Example 8: Tag Management
// ============================================

const articleTags = ['tech', 'programming', 'javascript', 'web', 'tech', 'tutorial'];

// Get unique tags
const uniqueTags = unique(articleTags);
console.log('Unique tags:', uniqueTags);

// Merge tags from another article
const otherTags = ['design', 'css', 'web', 'frontend'];
const allTags = union(uniqueTags, otherTags);
console.log('All unique tags:', allTags);

// Common tags
const commonTags = intersection(uniqueTags, otherTags);
console.log('Common tags:', commonTags);

// Check for duplicates
if (hasDuplicates(articleTags)) {
  console.log('Duplicates found:', duplicates(articleTags));
}

// ============================================
// Example 9: Queue-like Operations
// ============================================

const queue = [1, 2, 3, 4, 5];

// Dequeue (take first)
const dequeued = first(queue);
const remaining = drop(queue, 1);
console.log('Dequeued:', dequeued, 'Remaining:', remaining);

// Enqueue (append)
const enqueued = append(queue, 6);
console.log('After enqueue:', enqueued);

// Rotate (circular queue)
const rotated = rotate(queue, 1);
console.log('Rotated right:', rotated);

// ============================================
// Example 10: Matrix Operations
// ============================================

const matrix = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
];

// Flatten matrix
const flattened = flatten(matrix);
console.log('Flattened matrix:', flattened);

// Deep flatten (nested arrays)
const nested = [[1, [2, 3]], [[4, 5], 6]];
const deepFlattened = flattenDeep(nested);
console.log('Deep flattened:', deepFlattened);

// Transpose (transpose matrix)
const rows = matrix.length;
const cols = first(matrix)?.length ?? 0;
const transposed: number[][] = [];
for (let j = 0; j < cols; j++) {
  transposed.push(map(matrix, row => row[j]));
}
console.log('Transposed:', transposed);

// ============================================
// Example 11: Comparison and Equality
// ============================================

const list1 = [1, 2, 3];
const list2 = [1, 2, 3];
const list3 = [3, 2, 1];

// Check equality
console.log('list1 equals list2:', equals(list1, list2));
console.log('list1 equals list3:', equals(list1, list3));
console.log('list1 equalsIgnoreOrder list3:', equalsIgnoreOrder(list1, list3));

// Prefix/Suffix checks
const fullList = [1, 2, 3, 4, 5];
console.log('Starts with [1, 2]:', startsWith(fullList, [1, 2]));
console.log('Ends with [4, 5]:', endsWith(fullList, [4, 5]));

// ============================================
// Example 12: Random Selection
// ============================================

const participants = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'];

// Random winner
const winner = randomElement(participants);
console.log('Winner:', winner);

// Random sample for testing
const testers = randomElements(participants, 2);
console.log('Testers:', testers);

// Shuffle for random order
const shuffledParticipants = shuffle(participants);
console.log('Shuffled order:', shuffledParticipants);

// ============================================
// Example 13: String List Operations
// ============================================

const words = ['hello', 'world', 'arkts', 'harmonyos'];

// Join with separator
const sentence = join(words, ' ');
console.log('Sentence:', sentence);

// Join with prefix/suffix
const quoted = joinWith(words, ',', '[', ']');
console.log('Quoted:', quoted);

// Interleave with numbers
const numbered = interleave(range(1, words.length + 1), words);
console.log('Numbered:', numbered);

// ============================================
// Example 14: Array Generation
// ============================================

// Generate range
const indexes = range(10);
console.log('Indexes 0-9:', indexes);

// Generate with step
const evenNumbers = range(0, 20, 2);
console.log('Even numbers:', evenNumbers);

// Generate negative range
const countdown = range(10, 0, -1);
console.log('Countdown:', countdown);

// Fill with value
const zeros = fill(5, 0);
console.log('Five zeros:', zeros);

// Fill with function
const squares = fillFn(5, i => i * i);
console.log('Squares:', squares);

// ============================================
// Example 15: Reducing and Aggregating
// ============================================

const numbers = [1, 2, 3, 4, 5];

// Sum
console.log('Sum:', sum(numbers));

// Product (via reduce)
const product = reduce(numbers, (a, b) => a * b, 1);
console.log('Product:', product);

// Find longest string
const strings = ['a', 'abc', 'ab', 'abcd'];
const longest = maxBy(strings, s => s.length);
console.log('Longest:', longest);

// Count occurrences
const letters = ['a', 'b', 'a', 'c', 'a', 'b'];
const letterCounts = countBy(letters, l => l);
console.log('Letter counts:', letterCounts);

// ============================================
// Example 16: Class API Usage
// ============================================

// Using ArrayUtils class for cleaner imports
const data = [1, 2, 3, 4, 5];

console.log('First:', ArrayUtils.first(data));
console.log('Last:', ArrayUtils.last(data));
console.log('Sum:', ArrayUtils.sum(data));
console.log('Average:', ArrayUtils.average(data));
console.log('Unique:', ArrayUtils.unique([1, 2, 2, 3]));
console.log('Chunk:', ArrayUtils.chunk(data, 2));
console.log('Reverse:', ArrayUtils.reverse(data));

// ============================================
// Summary
// ============================================

console.log('\n========================================');
console.log('All examples completed successfully!');
console.log('========================================');