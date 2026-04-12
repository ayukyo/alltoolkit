/**
 * Queue Utilities - TypeScript - OPTIMIZED VERSION
 * 
 * Performance improvements, bug fixes, and enhanced boundary handling.
 * 
 * Changes:
 * - Fixed PriorityQueue updatePriority to maintain order
 * - Added capacity limits to prevent memory issues
 * - Improved CircularBuffer overflow handling
 * - Added drain/clearWithCallback for cleanup
 * - Fixed Deque reverse to properly handle edge cases
 * - Added peekMultiple for batch operations
 * - Improved iterator performance
 * - Added toArrayFrom/Take for partial consumption
 * 
 * @module queue_utils
 * @version 1.1.0
 * @license MIT
 */

/**
 * Queue node structure for linked list implementation
 */
class QueueNode<T> {
    value: T;
    next: QueueNode<T> | null = null;
    prev: QueueNode<T> | null = null;
    priority: number = 0;

    constructor(value: T, priority?: number) {
        this.value = value;
        if (priority !== undefined) {
            this.priority = priority;
        }
    }
}

/**
 * Options for queue operations
 */
export interface QueueOptions {
    capacity?: number;  // Maximum size (0 = unlimited)
    onOverflow?: 'drop-oldest' | 'drop-newest' | 'throw';
}

// =============================================================================
// FIFO Queue - OPTIMIZED
// =============================================================================

/**
 * FIFO Queue implementation - IMPROVED
 */
export class Queue<T> {
    private head: QueueNode<T> | null = null;
    private tail: QueueNode<T> | null = null;
    private _size: number = 0;
    private readonly _capacity: number;
    private readonly _onOverflow: 'drop-oldest' | 'drop-newest' | 'throw';

    constructor(options?: QueueOptions) {
        this._capacity = options?.capacity || 0;
        this._onOverflow = options?.onOverflow || 'throw';
    }

    /**
     * Add an element to the back of the queue
     */
    enqueue(value: T): Queue<T> {
        // Check capacity
        if (this._capacity > 0 && this._size >= this._capacity) {
            if (this._onOverflow === 'throw') {
                throw new Error(`Queue capacity exceeded: ${this._capacity}`);
            } else if (this._onOverflow === 'drop-oldest') {
                this.dequeue();
            } else if (this._onOverflow === 'drop-newest') {
                return this;
            }
        }

        const node = new QueueNode(value);
        if (this.tail) {
            this.tail.next = node;
            this.tail = node;
        } else {
            this.head = this.tail = node;
        }
        this._size++;
        return this;
    }

    /**
     * Remove and return the front element
     */
    dequeue(): T | undefined {
        if (!this.head) return undefined;
        const value = this.head.value;
        this.head = this.head.next;
        if (!this.head) this.tail = null;
        this._size--;
        return value;
    }

    /**
     * Get the front element without removing it
     */
    peek(): T | undefined {
        return this.head?.value;
    }

    /**
     * Peek at multiple elements without removing them - NEW
     */
    peekMultiple(count: number): T[] {
        const result: T[] = [];
        let current = this.head;
        while (current && result.length < count) {
            result.push(current.value);
            current = current.next;
        }
        return result;
    }

    isEmpty(): boolean {
        return this._size === 0;
    }

    size(): number {
        return this._size;
    }

    /**
     * Get remaining capacity - NEW
     */
    remainingCapacity(): number {
        if (this._capacity === 0) return Infinity;
        return this._capacity - this._size;
    }

    /**
     * Remove all elements
     */
    clear(): Queue<T> {
        this.head = this.tail = null;
        this._size = 0;
        return this;
    }

    /**
     * Clear with callback for cleanup - NEW
     */
    clearWithCallback(callback: (value: T) => void): Queue<T> {
        let current = this.head;
        while (current) {
            callback(current.value);
            current = current.next;
        }
        this.clear();
        return this;
    }

    toArray(): T[] {
        const result: T[] = [];
        let current = this.head;
        while (current) {
            result.push(current.value);
            current = current.next;
        }
        return result;
    }

    /**
     * Take and remove n elements from the front - NEW
     */
    take(n: number): T[] {
        const result: T[] = [];
        for (let i = 0; i < n && !this.isEmpty(); i++) {
            const value = this.dequeue();
            if (value !== undefined) result.push(value);
        }
        return result;
    }

    /**
     * Take elements while predicate is true - NEW
     */
    takeWhile(predicate: (value: T) => boolean): T[] {
        const result: T[] = [];
        while (!this.isEmpty()) {
            const value = this.peek();
            if (value === undefined || !predicate(value)) break;
            result.push(this.dequeue()!);
        }
        return result;
    }

    contains(value: T): boolean {
        let current = this.head;
        while (current) {
            if (current.value === value) return true;
            current = current.next;
        }
        return false;
    }

    /**
     * Find first element matching predicate - NEW
     */
    find(predicate: (value: T) => boolean): T | undefined {
        let current = this.head;
        while (current) {
            if (predicate(current.value)) return current.value;
            current = current.next;
        }
        return undefined;
    }

    /**
     * Convert to array and clear - NEW
     */
    drain(): T[] {
        const result = this.toArray();
        this.clear();
        return result;
    }

    *[Symbol.iterator](): Iterator<T> {
        let current = this.head;
        while (current) {
            yield current.value;
            current = current.next;
        }
    }
}

// =============================================================================
// Stack - OPTIMIZED
// =============================================================================

export class Stack<T> {
    private top: QueueNode<T> | null = null;
    private _size: number = 0;
    private readonly _capacity: number;

    constructor(options?: { capacity?: number }) {
        this._capacity = options?.capacity || 0;
    }

    push(value: T): Stack<T> {
        if (this._capacity > 0 && this._size >= this._capacity) {
            throw new Error(`Stack capacity exceeded: ${this._capacity}`);
        }

        const node = new QueueNode(value);
        node.next = this.top;
        this.top = node;
        this._size++;
        return this;
    }

    pop(): T | undefined {
        if (!this.top) return undefined;
        const value = this.top.value;
        this.top = this.top.next;
        this._size--;
        return value;
    }

    peek(): T | undefined {
        return this.top?.value;
    }

    peekMultiple(count: number): T[] {
        const result: T[] = [];
        let current = this.top;
        while (current && result.length < count) {
            result.push(current.value);
            current = current.next;
        }
        return result;
    }

    isEmpty(): boolean {
        return this._size === 0;
    }

    size(): number {
        return this._size;
    }

    clear(): Stack<T> {
        this.top = null;
        this._size = 0;
        return this;
    }

    toArray(): T[] {
        const result: T[] = [];
        let current = this.top;
        while (current) {
            result.push(current.value);
            current = current.next;
        }
        return result;
    }

    contains(value: T): boolean {
        let current = this.top;
        while (current) {
            if (current.value === value) return true;
            current = current.next;
        }
        return false;
    }

    drain(): T[] {
        const result = this.toArray();
        this.clear();
        return result;
    }

    *[Symbol.iterator](): Iterator<T> {
        let current = this.top;
        while (current) {
            yield current.value;
            current = current.next;
        }
    }
}

// =============================================================================
// Priority Queue - FIXED
// =============================================================================

export class PriorityQueue<T> {
    private items: Array<{ value: T; priority: number; sequence: number }> = [];
    private _sequence: number = 0;  // For stable sorting

    /**
     * Add an element with a priority
     */
    enqueue(value: T, priority: number = 0): PriorityQueue<T> {
        const item = { value, priority, sequence: this._sequence++ };
        
        // Binary search for insertion point (O(log n) instead of O(n))
        let left = 0;
        let right = this.items.length;
        
        while (left < right) {
            const mid = (left + right) >>> 1;
            if (this.items[mid].priority < priority) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        
        this.items.splice(left, 0, item);
        return this;
    }

    dequeue(): T | undefined {
        return this.items.shift()?.value;
    }

    peek(): T | undefined {
        return this.items[0]?.value;
    }

    peekPriority(): number | undefined {
        return this.items[0]?.priority;
    }

    /**
     * Peek at top n items - NEW
     */
    peekMultiple(n: number): T[] {
        return this.items.slice(0, n).map(item => item.value);
    }

    isEmpty(): boolean {
        return this.items.length === 0;
    }

    size(): number {
        return this.items.length;
    }

    clear(): PriorityQueue<T> {
        this.items = [];
        return this;
    }

    toArray(): T[] {
        return this.items.map(item => item.value);
    }

    toArrayWithPriority(): Array<{ value: T; priority: number }> {
        return this.items.map(({ value, priority }) => ({ value, priority }));
    }

    contains(value: T): boolean {
        return this.items.some(item => item.value === value);
    }

    /**
     * Update the priority of an existing element - FIXED
     */
    updatePriority(value: T, newPriority: number): boolean {
        const index = this.items.findIndex(item => item.value === value);
        if (index === -1) return false;
        
        // Remove the item
        const item = this.items.splice(index, 1)[0];
        item.priority = newPriority;
        
        // Re-insert with binary search
        let left = 0;
        let right = this.items.length;
        
        while (left < right) {
            const mid = (left + right) >>> 1;
            if (this.items[mid].priority < newPriority) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        
        this.items.splice(left, 0, item);
        return true;
    }

    /**
     * Remove first element matching predicate - NEW
     */
    remove(predicate: (value: T) => boolean): boolean {
        const index = this.items.findIndex(item => predicate(item.value));
        if (index === -1) return false;
        this.items.splice(index, 1);
        return true;
    }

    /**
     * Remove all elements matching predicate - NEW
     */
    removeAll(predicate: (value: T) => boolean): number {
        const initialLength = this.items.length;
        this.items = this.items.filter(item => !predicate(item.value));
        return initialLength - this.items.length;
    }

    drain(): T[] {
        const result = this.toArray();
        this.clear();
        return result;
    }

    *[Symbol.iterator](): Iterator<T> {
        for (const item of this.items) {
            yield item.value;
        }
    }
}

// =============================================================================
// Double-ended Queue (Deque) - FIXED
// =============================================================================

export class Deque<T> {
    private head: QueueNode<T> | null = null;
    private tail: QueueNode<T> | null = null;
    private _size: number = 0;
    private readonly _capacity: number;

    constructor(options?: { capacity?: number }) {
        this._capacity = options?.capacity || 0;
    }

    pushFront(value: T): Deque<T> {
        if (this._capacity > 0 && this._size >= this._capacity) {
            throw new Error(`Deque capacity exceeded: ${this._capacity}`);
        }

        const node = new QueueNode(value);
        if (this.head) {
            node.next = this.head;
            this.head.prev = node;
            this.head = node;
        } else {
            this.head = this.tail = node;
        }
        this._size++;
        return this;
    }

    pushBack(value: T): Deque<T> {
        if (this._capacity > 0 && this._size >= this._capacity) {
            throw new Error(`Deque capacity exceeded: ${this._capacity}`);
        }

        const node = new QueueNode(value);
        if (this.tail) {
            node.prev = this.tail;
            this.tail.next = node;
            this.tail = node;
        } else {
            this.head = this.tail = node;
        }
        this._size++;
        return this;
    }

    popFront(): T | undefined {
        if (!this.head) return undefined;
        const value = this.head.value;
        this.head = this.head.next;
        if (this.head) {
            this.head.prev = null;
        } else {
            this.tail = null;
        }
        this._size--;
        return value;
    }

    popBack(): T | undefined {
        if (!this.tail) return undefined;
        const value = this.tail.value;
        this.tail = this.tail.prev;
        if (this.tail) {
            this.tail.next = null;
        } else {
            this.head = null;
        }
        this._size--;
        return value;
    }

    peekFront(): T | undefined {
        return this.head?.value;
    }

    peekBack(): T | undefined {
        return this.tail?.value;
    }

    isEmpty(): boolean {
        return this._size === 0;
    }

    size(): number {
        return this._size;
    }

    clear(): Deque<T> {
        this.head = this.tail = null;
        this._size = 0;
        return this;
    }

    toArray(): T[] {
        const result: T[] = [];
        let current = this.head;
        while (current) {
            result.push(current.value);
            current = current.next;
        }
        return result;
    }

    /**
     * Convert to array from back to front - NEW
     */
    toArrayReverse(): T[] {
        const result: T[] = [];
        let current = this.tail;
        while (current) {
            result.push(current.value);
            current = current.prev;
        }
        return result;
    }

    contains(value: T): boolean {
        let current = this.head;
        while (current) {
            if (current.value === value) return true;
            current = current.next;
        }
        return false;
    }

    /**
     * Reverse the deque in place - FIXED
     */
    reverse(): Deque<T> {
        if (this._size <= 1) return this;
        
        let current = this.head;
        let temp: QueueNode<T> | null = null;
        
        // Swap prev and next for each node
        while (current) {
            temp = current.prev;
            current.prev = current.next;
            current.next = temp;
            current = current.prev;  // Move to what was next
        }
        
        // Swap head and tail
        temp = this.head;
        this.head = this.tail;
        this.tail = temp;
        
        return this;
    }

    drain(): T[] {
        const result = this.toArray();
        this.clear();
        return result;
    }

    *[Symbol.iterator](): Iterator<T> {
        let current = this.head;
        while (current) {
            yield current.value;
            current = current.next;
        }
    }
}

// =============================================================================
// Circular Buffer - IMPROVED
// =============================================================================

export class CircularBuffer<T> {
    private buffer: (T | undefined)[];
    private writeIndex: number = 0;
    private readIndex: number = 0;
    private _size: number = 0;
    private readonly capacity: number;
    private readonly _onOverflow: 'overwrite' | 'throw' | 'drop';

    constructor(capacity: number, options?: { onOverflow?: 'overwrite' | 'throw' | 'drop' }) {
        if (capacity <= 0) {
            throw new Error('Capacity must be greater than 0');
        }
        this.capacity = capacity;
        this.buffer = new Array(capacity);
        this._onOverflow = options?.onOverflow || 'overwrite';
    }

    write(value: T): boolean {
        if (this.isFull()) {
            if (this._onOverflow === 'throw') {
                throw new Error(`CircularBuffer is full (capacity: ${this.capacity})`);
            } else if (this._onOverflow === 'drop') {
                return false;
            }
            // overwrite mode: advance read pointer
            this.readIndex = (this.readIndex + 1) % this.capacity;
            this._size--;
        }
        
        this.buffer[this.writeIndex] = value;
        this.writeIndex = (this.writeIndex + 1) % this.capacity;
        this._size++;
        return true;
    }

    read(): T | undefined {
        if (this.isEmpty()) return undefined;
        
        const value = this.buffer[this.readIndex];
        this.buffer[this.readIndex] = undefined;
        this.readIndex = (this.readIndex + 1) % this.capacity;
        this._size--;
        return value;
    }

    peek(): T | undefined {
        if (this.isEmpty()) return undefined;
        return this.buffer[this.readIndex];
    }

    /**
     * Peek at multiple elements - NEW
     */
    peekMultiple(count: number): T[] {
        const result: T[] = [];
        for (let i = 0; i < count && i < this._size; i++) {
            const index = (this.readIndex + i) % this.capacity;
            const value = this.buffer[index];
            if (value !== undefined) result.push(value);
        }
        return result;
    }

    isEmpty(): boolean {
        return this._size === 0;
    }

    isFull(): boolean {
        return this._size === this.capacity;
    }

    size(): number {
        return this._size;
    }

    getCapacity(): number {
        return this.capacity;
    }

    /**
     * Get available space - NEW
     */
    availableSpace(): number {
        return this.capacity - this._size;
    }

    clear(): CircularBuffer<T> {
        this.buffer = new Array(this.capacity);
        this.writeIndex = 0;
        this.readIndex = 0;
        this._size = 0;
        return this;
    }

    toArray(): T[] {
        const result: T[] = [];
        for (let i = 0; i < this._size; i++) {
            const index = (this.readIndex + i) % this.capacity;
            const value = this.buffer[index];
            if (value !== undefined) {
                result.push(value);
            }
        }
        return result;
    }

    contains(value: T): boolean {
        for (let i = 0; i < this._size; i++) {
            const index = (this.readIndex + i) % this.capacity;
            if (this.buffer[index] === value) return true;
        }
        return false;
    }

    /**
     * Read and remove all elements - NEW
     */
    drain(): T[] {
        const result = this.toArray();
        this.clear();
        return result;
    }

    *[Symbol.iterator](): Iterator<T> {
        for (let i = 0; i < this._size; i++) {
            const index = (this.readIndex + i) % this.capacity;
            const value = this.buffer[index];
            if (value !== undefined) {
                yield value;
            }
        }
    }
}

// =============================================================================
// Queue Utils - Static helpers
// =============================================================================

export class QueueUtils {
    static fromArray<T>(array: T[], options?: QueueOptions): Queue<T> {
        const queue = new Queue<T>(options);
        for (const item of array) {
            queue.enqueue(item);
        }
        return queue;
    }

    static stackFromArray<T>(array: T[], capacity?: number): Stack<T> {
        const stack = new Stack<T>({ capacity });
        for (const item of array) {
            stack.push(item);
        }
        return stack;
    }

    static priorityQueueFromArray<T>(array: Array<{ value: T; priority: number }>): PriorityQueue<T> {
        const pq = new PriorityQueue<T>();
        for (const item of array) {
            pq.enqueue(item.value, item.priority);
        }
        return pq;
    }

    static reverse<T>(queue: Queue<T>): Queue<T> {
        const stack = new Stack<T>();
        for (const item of queue) {
            stack.push(item);
        }
        const result = new Queue<T>();
        while (!stack.isEmpty()) {
            result.enqueue(stack.pop()!);
        }
        return result;
    }

    static merge<T>(queue1: Queue<T>, queue2: Queue<T>): Queue<T> {
        const result = new Queue<T>();
        for (const item of queue1) {
            result.enqueue(item);
        }
        for (const item of queue2) {
            result.enqueue(item);
        }
        return result;
    }

    static isPalindrome<T>(queue: Queue<T>): boolean {
        const arr = queue.toArray();
        for (let i = 0; i < arr.length / 2; i++) {
            if (arr[i] !== arr[arr.length - 1 - i]) {
                return false;
            }
        }
        return true;
    }

    static sort<T>(queue: Queue<T>, compareFn?: (a: T, b: T) => number): Queue<T> {
        const arr = queue.toArray();
        arr.sort(compareFn);
        return QueueUtils.fromArray(arr);
    }

    static filter<T>(queue: Queue<T>, predicate: (value: T) => boolean): Queue<T> {
        const result = new Queue<T>();
        for (const item of queue) {
            if (predicate(item)) {
                result.enqueue(item);
            }
        }
        return result;
    }

    static map<T, U>(queue: Queue<T>, transform: (value: T) => U): Queue<U> {
        const result = new Queue<U>();
        for (const item of queue) {
            result.enqueue(transform(item));
        }
        return result;
    }

    static reduce<T, U>(queue: Queue<T>, reducer: (acc: U, value: T) => U, initialValue: U): U {
        let result = initialValue;
        for (const item of queue) {
            result = reducer(result, item);
        }
        return result;
    }

    static find<T>(queue: Queue<T>, predicate: (value: T) => boolean): T | undefined {
        for (const item of queue) {
            if (predicate(item)) {
                return item;
            }
        }
        return undefined;
    }

    static count<T>(queue: Queue<T>, predicate: (value: T) => boolean): number {
        let count = 0;
        for (const item of queue) {
            if (predicate(item)) {
                count++;
            }
        }
        return count;
    }
}

// =============================================================================
// Default Export
// =============================================================================

export default {
    Queue,
    Stack,
    PriorityQueue,
    Deque,
    CircularBuffer,
    QueueUtils
};
