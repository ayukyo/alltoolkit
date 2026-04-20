/**
 * Test suite for Priority Queue Utils
 */

const assert = require('assert');
const { PriorityQueue, IndexedPriorityQueue, defaultComparator } = require('./mod.js');

// Test counters
let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (e) {
    console.log(`✗ ${name}`);
    console.log(`  Error: ${e.message}`);
    failed++;
  }
}

// ============== PriorityQueue Tests ==============

console.log('\n=== PriorityQueue Tests ===\n');

test('should create empty queue', () => {
  const pq = new PriorityQueue();
  assert.strictEqual(pq.size, 0);
  assert.strictEqual(pq.isEmpty(), true);
});

test('should create queue with initial items', () => {
  const pq = new PriorityQueue(null, [3, 1, 4, 1, 5]);
  assert.strictEqual(pq.size, 5);
  assert.strictEqual(pq.isEmpty(), false);
});

test('should enqueue and dequeue in priority order (min-heap)', () => {
  const pq = new PriorityQueue();
  pq.enqueue(5).enqueue(3).enqueue(1).enqueue(4).enqueue(2);
  
  assert.strictEqual(pq.dequeue(), 1);
  assert.strictEqual(pq.dequeue(), 2);
  assert.strictEqual(pq.dequeue(), 3);
  assert.strictEqual(pq.dequeue(), 4);
  assert.strictEqual(pq.dequeue(), 5);
  assert.strictEqual(pq.dequeue(), undefined);
});

test('should support push/pop aliases', () => {
  const pq = new PriorityQueue();
  pq.push(10).push(5).push(20);
  
  assert.strictEqual(pq.pop(), 5);
  assert.strictEqual(pq.pop(), 10);
  assert.strictEqual(pq.pop(), 20);
});

test('should peek without removing', () => {
  const pq = new PriorityQueue();
  pq.enqueue(42);
  
  assert.strictEqual(pq.peek(), 42);
  assert.strictEqual(pq.size, 1);
  assert.strictEqual(pq.peek(), 42);
});

test('should support max-heap via comparator', () => {
  const pq = PriorityQueue.maxHeap([3, 1, 4, 1, 5]);
  
  assert.strictEqual(pq.dequeue(), 5);
  assert.strictEqual(pq.dequeue(), 4);
  assert.strictEqual(pq.dequeue(), 3);
  assert.strictEqual(pq.dequeue(), 1);
  assert.strictEqual(pq.dequeue(), 1);
});

test('should support min-heap static method', () => {
  const pq = PriorityQueue.minHeap([5, 3, 1, 4, 2]);
  
  assert.strictEqual(pq.dequeue(), 1);
  assert.strictEqual(pq.dequeue(), 2);
  assert.strictEqual(pq.dequeue(), 3);
});

test('should handle custom comparator for objects', () => {
  const pq = new PriorityQueue((a, b) => a.priority - b.priority);
  pq.enqueue({ name: 'C', priority: 3 });
  pq.enqueue({ name: 'A', priority: 1 });
  pq.enqueue({ name: 'B', priority: 2 });
  
  assert.strictEqual(pq.dequeue().name, 'A');
  assert.strictEqual(pq.dequeue().name, 'B');
  assert.strictEqual(pq.dequeue().name, 'C');
});

test('should clear the queue', () => {
  const pq = new PriorityQueue(null, [1, 2, 3, 4, 5]);
  pq.clear();
  
  assert.strictEqual(pq.size, 0);
  assert.strictEqual(pq.isEmpty(), true);
});

test('should convert to array', () => {
  const pq = new PriorityQueue(null, [1, 2, 3]);
  const arr = pq.toArray();
  
  assert.strictEqual(arr.length, 3);
  assert.strictEqual(pq.size, 3); // Original unchanged
});

test('should convert to sorted array', () => {
  const pq = new PriorityQueue(null, [5, 2, 8, 1, 9]);
  const sorted = pq.toSortedArray();
  
  assert.deepStrictEqual(sorted, [1, 2, 5, 8, 9]);
});

test('should find items with predicate', () => {
  const pq = new PriorityQueue(null, [10, 20, 30, 40, 50]);
  
  assert.strictEqual(pq.find(x => x > 25), 30);
  assert.strictEqual(pq.find(x => x > 100), undefined);
});

test('should filter items', () => {
  const pq = new PriorityQueue(null, [1, 2, 3, 4, 5, 6]);
  const evens = pq.filter(x => x % 2 === 0);
  
  assert.deepStrictEqual(evens.sort(), [2, 4, 6]);
});

test('should check some and every', () => {
  const pq = new PriorityQueue(null, [2, 4, 6, 8]);
  
  assert.strictEqual(pq.some(x => x > 5), true);
  assert.strictEqual(pq.some(x => x > 10), false);
  assert.strictEqual(pq.every(x => x % 2 === 0), true);
  assert.strictEqual(pq.every(x => x < 5), false);
});

test('should remove items matching predicate', () => {
  const pq = new PriorityQueue(null, [1, 2, 3, 4, 5, 6]);
  const removed = pq.remove(x => x % 2 === 0);
  
  assert.strictEqual(removed, 3);
  assert.strictEqual(pq.size, 3);
  
  const remaining = pq.toSortedArray();
  assert.deepStrictEqual(remaining, [1, 3, 5]);
});

test('should update items', () => {
  const pq = new PriorityQueue(null, [1, 2, 3, 4, 5]);
  pq.update(x => x === 3, x => 10);
  
  const sorted = pq.toSortedArray();
  assert.deepStrictEqual(sorted, [1, 2, 4, 5, 10]);
});

test('should merge queues', () => {
  const pq1 = new PriorityQueue(null, [1, 3, 5]);
  const pq2 = new PriorityQueue(null, [2, 4, 6]);
  
  pq1.merge(pq2);
  
  assert.strictEqual(pq1.size, 6);
  assert.deepStrictEqual(pq1.toSortedArray(), [1, 2, 3, 4, 5, 6]);
});

test('should merge queues statically', () => {
  const pq1 = new PriorityQueue(null, [1, 3]);
  const pq2 = new PriorityQueue(null, [2, 4]);
  const merged = PriorityQueue.merge(pq1, pq2);
  
  assert.strictEqual(merged.size, 4);
  assert.deepStrictEqual(merged.toSortedArray(), [1, 2, 3, 4]);
  
  // Originals unchanged
  assert.strictEqual(pq1.size, 2);
  assert.strictEqual(pq2.size, 2);
});

test('should create from array', () => {
  const pq = PriorityQueue.from([5, 3, 1, 4, 2], (a, b) => a - b);
  
  assert.deepStrictEqual(pq.toSortedArray(), [1, 2, 3, 4, 5]);
});

test('should be iterable', () => {
  const pq = new PriorityQueue(null, [1, 2, 3]);
  const items = [...pq];
  
  assert.strictEqual(items.length, 3);
});

test('should handle duplicate values', () => {
  const pq = new PriorityQueue(null, [3, 1, 4, 1, 5, 9, 2, 6, 5]);
  
  assert.strictEqual(pq.dequeue(), 1);
  assert.strictEqual(pq.dequeue(), 1);
  assert.strictEqual(pq.dequeue(), 2);
});

test('should handle strings', () => {
  const pq = new PriorityQueue();
  pq.enqueue('cherry').enqueue('apple').enqueue('banana');
  
  assert.strictEqual(pq.dequeue(), 'apple');
  assert.strictEqual(pq.dequeue(), 'banana');
  assert.strictEqual(pq.dequeue(), 'cherry');
});

test('should handle negative numbers', () => {
  const pq = new PriorityQueue(null, [5, -3, 0, -10, 8]);
  
  assert.strictEqual(pq.dequeue(), -10);
  assert.strictEqual(pq.dequeue(), -3);
  assert.strictEqual(pq.dequeue(), 0);
});

test('should handle large datasets efficiently', () => {
  const size = 10000;
  const pq = new PriorityQueue();
  
  // Insert random values
  for (let i = 0; i < size; i++) {
    pq.enqueue(Math.random() * 10000);
  }
  
  assert.strictEqual(pq.size, size);
  
  // Extract all - should be in sorted order
  let prev = -Infinity;
  let count = 0;
  while (!pq.isEmpty()) {
    const curr = pq.dequeue();
    assert(curr >= prev, 'Items should be in ascending order');
    prev = curr;
    count++;
  }
  
  assert.strictEqual(count, size);
});

// ============== IndexedPriorityQueue Tests ==============

console.log('\n=== IndexedPriorityQueue Tests ===\n');

test('should create empty indexed queue', () => {
  const ipq = new IndexedPriorityQueue();
  assert.strictEqual(ipq.size, 0);
  assert.strictEqual(ipq.isEmpty(), true);
});

test('should set and get items', () => {
  const ipq = new IndexedPriorityQueue();
  
  assert.strictEqual(ipq.set('a', 1), false); // New key
  assert.strictEqual(ipq.set('a', 2), true);  // Update existing
  
  assert.strictEqual(ipq.getPriority('a'), 2);
  assert.strictEqual(ipq.has('a'), true);
  assert.strictEqual(ipq.has('b'), false);
});

test('should dequeue in priority order', () => {
  const ipq = new IndexedPriorityQueue();
  ipq.set('task1', 3);
  ipq.set('task2', 1);
  ipq.set('task3', 2);
  
  assert.strictEqual(ipq.dequeue().key, 'task2');
  assert.strictEqual(ipq.dequeue().key, 'task3');
  assert.strictEqual(ipq.dequeue().key, 'task1');
  assert.strictEqual(ipq.dequeue(), undefined);
});

test('should support associated values', () => {
  const ipq = new IndexedPriorityQueue();
  ipq.set('a', 1, { name: 'Task A' });
  ipq.set('b', 2, { name: 'Task B' });
  
  assert.deepStrictEqual(ipq.get('a'), { name: 'Task A' });
  
  const first = ipq.dequeue();
  assert.strictEqual(first.key, 'a');
  assert.strictEqual(first.priority, 1);
  assert.deepStrictEqual(first.value, { name: 'Task A' });
});

test('should delete keys', () => {
  const ipq = new IndexedPriorityQueue();
  ipq.set('a', 1);
  ipq.set('b', 2);
  ipq.set('c', 3);
  
  assert.strictEqual(ipq.delete('b'), true);
  assert.strictEqual(ipq.has('b'), false);
  assert.strictEqual(ipq.delete('nonexistent'), false);
  
  const keys = ipq.keys();
  assert.strictEqual(keys.length, 2);
});

test('should clear all items', () => {
  const ipq = new IndexedPriorityQueue();
  ipq.set('a', 1);
  ipq.set('b', 2);
  ipq.clear();
  
  assert.strictEqual(ipq.size, 0);
  assert.strictEqual(ipq.isEmpty(), true);
});

test('should update priority', () => {
  const ipq = new IndexedPriorityQueue();
  ipq.set('a', 10);
  ipq.set('b', 5);
  ipq.set('c', 15);
  
  // Update 'a' to highest priority
  ipq.set('a', 1);
  
  assert.strictEqual(ipq.dequeue().key, 'a');
  assert.strictEqual(ipq.dequeue().key, 'b');
  assert.strictEqual(ipq.dequeue().key, 'c');
});

test('should peek without removing', () => {
  const ipq = new IndexedPriorityQueue();
  ipq.set('a', 1, 'value-a');
  
  const peeked = ipq.peek();
  assert.strictEqual(peeked.key, 'a');
  assert.strictEqual(ipq.size, 1); // Not removed
});

test('should get all keys', () => {
  const ipq = new IndexedPriorityQueue();
  ipq.set('a', 1);
  ipq.set('b', 2);
  ipq.set('c', 3);
  
  const keys = ipq.keys().sort();
  assert.deepStrictEqual(keys, ['a', 'b', 'c']);
});

test('should work with max-heap comparator', () => {
  const ipq = new IndexedPriorityQueue((a, b) => b - a);
  ipq.set('a', 1);
  ipq.set('b', 5);
  ipq.set('c', 3);
  
  assert.strictEqual(ipq.dequeue().key, 'b'); // Priority 5
  assert.strictEqual(ipq.dequeue().key, 'c'); // Priority 3
  assert.strictEqual(ipq.dequeue().key, 'a'); // Priority 1
});

// ============== Performance Tests ==============

console.log('\n=== Performance Tests ===\n');

test('should handle 10000 enqueue/dequeue operations quickly', () => {
  const pq = new PriorityQueue();
  const start = Date.now();
  
  for (let i = 0; i < 10000; i++) {
    pq.enqueue(Math.random());
  }
  
  while (!pq.isEmpty()) {
    pq.dequeue();
  }
  
  const elapsed = Date.now() - start;
  assert(elapsed < 100, `Should complete in <100ms, took ${elapsed}ms`);
});

test('should build heap efficiently from array', () => {
  const items = Array.from({ length: 10000 }, () => Math.random());
  const start = Date.now();
  
  const pq = new PriorityQueue(null, items);
  
  const elapsed = Date.now() - start;
  assert(elapsed < 50, `Should build in <50ms, took ${elapsed}ms`);
  assert.strictEqual(pq.size, 10000);
});

// ============== Summary ==============

console.log('\n=== Test Summary ===\n');
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log(`Total: ${passed + failed}`);

if (failed > 0) {
  process.exit(1);
}