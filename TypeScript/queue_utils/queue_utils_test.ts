/**
 * Queue Utilities Test Suite
 */

import { Queue, Stack, PriorityQueue, Deque, CircularBuffer, QueueUtils } from './mod';

let passed = 0;
let failed = 0;

function test(name: string, fn: () => void): void {
    try {
        fn();
        console.log(`✓ ${name}`);
        passed++;
    } catch (error) {
        console.error(`✗ ${name}: ${error}`);
        failed++;
    }
}

function assertEqual(actual: any, expected: any): void {
    if (actual !== expected) {
        throw new Error(`expected ${expected}, got ${actual}`);
    }
}

function assertTrue(value: boolean): void {
    if (!value) throw new Error('expected true');
}

function assertFalse(value: boolean): void {
    if (value) throw new Error('expected false');
}

function assertArrayEqual(actual: any[], expected: any[]): void {
    if (actual.length !== expected.length) {
        throw new Error(`length mismatch: expected ${expected.length}, got ${actual.length}`);
    }
    for (let i = 0; i < actual.length; i++) {
        if (actual[i] !== expected[i]) {
            throw new Error(`element ${i}: expected ${expected[i]}, got ${actual[i]}`);
        }
    }
}

function assertUndefined(value: any): void {
    if (value !== undefined) throw new Error(`expected undefined, got ${value}`);
}

// Queue Tests
console.log('\n=== Queue Tests ===\n');

test('Queue: enqueue/dequeue single', () => {
    const q = new Queue<number>();
    q.enqueue(1);
    assertEqual(q.dequeue(), 1);
});

test('Queue: FIFO order', () => {
    const q = new Queue<number>();
    q.enqueue(1).enqueue(2).enqueue(3);
    assertEqual(q.dequeue(), 1);
    assertEqual(q.dequeue(), 2);
    assertEqual(q.dequeue(), 3);
});

test('Queue: peek', () => {
    const q = new Queue<number>();
    q.enqueue(1).enqueue(2);
    assertEqual(q.peek(), 1);
    assertEqual(q.size(), 2);
});

test('Queue: isEmpty', () => {
    const q = new Queue<number>();
    assertTrue(q.isEmpty());
    q.enqueue(1);
    assertFalse(q.isEmpty());
});

test('Queue: clear', () => {
    const q = new Queue<number>();
    q.enqueue(1).enqueue(2);
    q.clear();
    assertTrue(q.isEmpty());
});

test('Queue: contains', () => {
    const q = new Queue<number>();
    q.enqueue(1).enqueue(2);
    assertTrue(q.contains(2));
    assertFalse(q.contains(3));
});

test('Queue: toArray', () => {
    const q = new Queue<number>();
    q.enqueue(1).enqueue(2).enqueue(3);
    assertArrayEqual(q.toArray(), [1, 2, 3]);
});

// Stack Tests
console.log('\n=== Stack Tests ===\n');

test('Stack: push/pop single', () => {
    const s = new Stack<number>();
    s.push(1);
    assertEqual(s.pop(), 1);
});

test('Stack: LIFO order', () => {
    const s = new Stack<number>();
    s.push(1).push(2).push(3);
    assertEqual(s.pop(), 3);
    assertEqual(s.pop(), 2);
    assertEqual(s.pop(), 1);
});

test('Stack: peek', () => {
    const s = new Stack<number>();
    s.push(1).push(2);
    assertEqual(s.peek(), 2);
    assertEqual(s.size(), 2);
});

test('Stack: isEmpty', () => {
    const s = new Stack<number>();
    assertTrue(s.isEmpty());
});

// PriorityQueue Tests
console.log('\n=== PriorityQueue Tests ===\n');

test('PriorityQueue: priority order', () => {
    const pq = new PriorityQueue<string>();
    pq.enqueue('low', 1);
    pq.enqueue('high', 10);
    pq.enqueue('medium', 5);
    assertEqual(pq.dequeue(), 'high');
    assertEqual(pq.dequeue(), 'medium');
    assertEqual(pq.dequeue(), 'low');
});

test('PriorityQueue: same priority FIFO', () => {
    const pq = new PriorityQueue<string>();
    pq.enqueue('first', 5);
    pq.enqueue('second', 5);
    assertEqual(pq.dequeue(), 'first');
    assertEqual(pq.dequeue(), 'second');
});

test('PriorityQueue: peek', () => {
    const pq = new PriorityQueue<string>();
    pq.enqueue('task', 10);
    assertEqual(pq.peek(), 'task');
    assertEqual(pq.peekPriority(), 10);
});

// Deque Tests
console.log('\n=== Deque Tests ===\n');

test('Deque: pushFront/popFront', () => {
    const d = new Deque<number>();
    d.pushFront(1).pushFront(2);
    assertEqual(d.popFront(), 2);
    assertEqual(d.popFront(), 1);
});

test('Deque: pushBack/popBack', () => {
    const d = new Deque<number>();
    d.pushBack(1).pushBack(2);
    assertEqual(d.popBack(), 2);
    assertEqual(d.popBack(), 1);
});

test('Deque: mixed operations', () => {
    const d = new Deque<number>();
    d.pushBack(1);
    d.pushFront(2);
    d.pushBack(3);
    assertArrayEqual(d.toArray(), [2, 1, 3]);
});

test('Deque: peek', () => {
    const d = new Deque<number>();
    d.pushBack(1).pushBack(2);
    assertEqual(d.peekFront(), 1);
    assertEqual(d.peekBack(), 2);
});

test('Deque: reverse', () => {
    const d = new Deque<number>();
    d.pushBack(1).pushBack(2).pushBack(3);
    d.reverse();
    assertArrayEqual(d.toArray(), [3, 2, 1]);
});

// CircularBuffer Tests
console.log('\n=== CircularBuffer Tests ===\n');

test('CircularBuffer: basic read/write', () => {
    const cb = new CircularBuffer<number>(3);
    cb.write(1);
    cb.write(2);
    assertEqual(cb.read(), 1);
    assertEqual(cb.read(), 2);
});

test('CircularBuffer: overwrite', () => {
    const cb = new CircularBuffer<number>(2);
    cb.write(1);
    cb.write(2);
    cb.write(3); // overwrites 1
    assertEqual(cb.read(), 2);
    assertEqual(cb.read(), 3);
});

test('CircularBuffer: isFull/isEmpty', () => {
    const cb = new CircularBuffer<number>(2);
    assertTrue(cb.isEmpty());
    cb.write(1);
    cb.write(2);
    assertTrue(cb.isFull());
});

test('CircularBuffer: toArray', () => {
    const cb = new CircularBuffer<number>(3);
    cb.write(1);
    cb.write(2);
    cb.write(3);
    assertArrayEqual(cb.toArray(), [1, 2, 3]);
});

// QueueUtils Tests
console.log('\n=== QueueUtils Tests ===\n');

test('QueueUtils: fromArray', () => {
    const q = QueueUtils.fromArray([1, 2, 3]);
    assertArrayEqual(q.toArray(), [1, 2, 3]);
});

test('QueueUtils: reverse', () => {
    const q = new Queue<number>();
    q.enqueue(1).enqueue(2).enqueue(3);
    const reversed = QueueUtils.reverse(q);
    assertArrayEqual(reversed.toArray(), [3, 2, 1]);
});

test('QueueUtils: merge', () => {
    const q1 = QueueUtils.fromArray([1, 2]);
    const q2 = QueueUtils.fromArray([3, 4]);
    const merged = QueueUtils.merge(q1, q2);
    assertArrayEqual(merged.toArray(), [1, 2, 3, 4]);
});

test('QueueUtils: isPalindrome', () => {
    const q1 = QueueUtils.fromArray([1, 2, 1]);
    const q2 = QueueUtils.fromArray([1, 2, 3]);
    assertTrue(QueueUtils.isPalindrome(q1));
    assertFalse(QueueUtils.isPalindrome(q2));
});

test('QueueUtils: filter', () => {
    const q = QueueUtils.fromArray([1, 2, 3, 4, 5]);
    const filtered = QueueUtils.filter(q, x => x % 2 === 0);
    assertArrayEqual(filtered.toArray(), [2, 4]);
});

test('QueueUtils: map', () => {
    const q = QueueUtils.fromArray([1, 2, 3]);
    const mapped = QueueUtils.map(q, x => x * 2);
    assertArrayEqual(mapped.toArray(), [2, 4, 6]);
});

test('QueueUtils: reduce', () => {
    const q = QueueUtils.fromArray([1, 2, 3, 4]);
    const sum = QueueUtils.reduce(q, (acc, x) => acc + x, 0);
    assertEqual(sum, 10);
});

test('QueueUtils: find', () => {
    const q = QueueUtils.fromArray([1, 2, 3, 4, 5]);
    const found = QueueUtils.find(q, x => x > 3);
    assertEqual(found, 4);
});

test('QueueUtils: count', () => {
    const q = QueueUtils.fromArray([1, 2, 3, 4, 5]);
    const count = QueueUtils.count(q, x => x % 2 === 0);
    assertEqual(count, 2);
});

// Summary
console.log('\n=== Test Summary ===\n');
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log(`Total:  ${passed + failed}`);

process.exit(failed > 0 ? 1 : 0);
