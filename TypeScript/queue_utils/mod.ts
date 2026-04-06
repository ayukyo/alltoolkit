/**
 * Queue Utilities - TypeScript
 * 
 * A comprehensive queue data structure utility module providing FIFO (First In First Out)
 * queue, LIFO (Last In First Out) stack, priority queue, and double-ended queue (deque)
 * implementations with zero dependencies.
 * 
 * @module queue_utils
 * @version 1.0.0
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
 * FIFO Queue implementation
 * 
 * A standard First In First Out queue with O(1) enqueue and dequeue operations.
 * 
 * @example
 * ```typescript
 * const queue = new Queue<number>();
 * queue.enqueue(1);
 * queue.enqueue(2);
 * queue.enqueue(3);
 * console.log(queue.dequeue()); // 1
 * console.log(queue.peek()); // 2
 * ```
 */
export class Queue<T> {
    private head: QueueNode<T> | null = null;
    private tail: QueueNode<T> | null = null;
    private _size: number = 0;

    /**
     * Add an element to the back of the queue
     * @param value - The value to enqueue
     * @returns The queue instance for chaining
     * @timeComplexity O(1)
     */
    enqueue(value: T): Queue<T> {
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
     * Remove and return the front element from the queue
     * @returns The front element, or undefined if queue is empty
     * @timeComplexity O(1)
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
     * @returns The front element, or undefined if queue is empty
     * @timeComplexity O(1)
     */
    peek(): T | undefined {
        return this.head?.value;
    }

    /**
     * Check if the queue is empty
     * @returns true if queue is empty
     * @timeComplexity O(1)
     */
    isEmpty(): boolean {
        return this._size === 0;
    }

    /**
     * Get the number of elements in the queue
     * @returns The queue size
     * @timeComplexity O(1)
     */
    size(): number {
        return this._size;
    }

    /**
     * Remove all elements from the queue
     * @returns The queue instance for chaining
     * @timeComplexity O(1)
     */
    clear(): Queue<T> {
        this.head = this.tail = null;
        this._size = 0;
        return this;
    }

    /**
     * Convert the queue to an array (front to back)
     * @returns Array representation of the queue
     * @timeComplexity O(n)
     */
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
     * Check if the queue contains a specific value
     * @param value - The value to search for
     * @returns true if value is found
     * @timeComplexity O(n)
     */
    contains(value: T): boolean {
        let current = this.head;
        while (current) {
            if (current.value === value) return true;
            current = current.next;
        }
        return false;
    }

    /**
     * Iterate over the queue elements
     */
    *[Symbol.iterator](): Iterator<T> {
        let current = this.head;
        while (current) {
            yield current.value;
            current = current.next;
        }
    }
}

/**
 * Stack implementation (LIFO)
 * 
 * A Last In First Out stack with O(1) push and pop operations.
 * 
 * @example
 * ```typescript
 * const stack = new Stack<number>();
 * stack.push(1);
 * stack.push(2);
 * stack.push(3);
 * console.log(stack.pop()); // 3
 * console.log(stack.peek()); // 2
 * ```
 */
export class Stack<T> {
    private top: QueueNode<T> | null = null;
    private _size: number = 0;

    /**
     * Add an element to the top of the stack
     * @param value - The value to push
     * @returns The stack instance for chaining
     * @timeComplexity O(1)
     */
    push(value: T): Stack<T> {
        const node = new QueueNode(value);
        node.next = this.top;
        this.top = node;
        this._size++;
        return this;
    }

    /**
     * Remove and return the top element from the stack
     * @returns The top element, or undefined if stack is empty
     * @timeComplexity O(1)
     */
    pop(): T | undefined {
        if (!this.top) return undefined;
        const value = this.top.value;
        this.top = this.top.next;
        this._size--;
        return value;
    }

    /**
     * Get the top element without removing it
     * @returns The top element, or undefined if stack is empty
     * @timeComplexity O(1)
     */
    peek(): T | undefined {
        return this.top?.value;
    }

    /**
     * Check if the stack is empty
     * @returns true if stack is empty
     * @timeComplexity O(1)
     */
    isEmpty(): boolean {
        return this._size === 0;
    }

    /**
     * Get the number of elements in the stack
     * @returns The stack size
     * @timeComplexity O(1)
     */
    size(): number {
        return this._size;
    }

    /**
     * Remove all elements from the stack
     * @returns The stack instance for chaining
     * @timeComplexity O(1)
     */
    clear(): Stack<T> {
        this.top = null;
        this._size = 0;
        return this;
    }

    /**
     * Convert the stack to an array (top to bottom)
     * @returns Array representation of the stack
     * @timeComplexity O(n)
     */
    toArray(): T[] {
        const result: T[] = [];
        let current = this.top;
        while (current) {
            result.push(current.value);
            current = current.next;
        }
        return result;
    }

    /**
     * Check if the stack contains a specific value
     * @param value - The value to search for
     * @returns true if value is found
     * @timeComplexity O(n)
     */
    contains(value: T): boolean {
        let current = this.top;
        while (current) {
            if (current.value === value) return true;
            current = current.next;
        }
        return false;
    }

    /**
     * Iterate over the stack elements
     */
    *[Symbol.iterator](): Iterator<T> {
        let current = this.top;
        while (current) {
            yield current.value;
            current = current.next;
        }
    }
}

/**
 * Priority Queue implementation
 * 
 * A queue where elements are ordered by priority (higher priority first).
 * Elements with the same priority are handled in FIFO order.
 * 
 * @example
 * ```typescript
 * const pq = new PriorityQueue<string>();
 * pq.enqueue("low", 1);
 * pq.enqueue("high", 10);
 * pq.enqueue("medium", 5);
 * console.log(pq.dequeue()); // "high"
 * ```
 */
export class PriorityQueue<T> {
    private items: Array<{ value: T; priority: number }> = [];

    /**
     * Add an element with a priority to the queue
     * @param value - The value to enqueue
     * @param priority - The priority (higher = more important)
     * @returns The priority queue instance for chaining
     * @timeComplexity O(n) - insertion sort by priority
     */
    enqueue(value: T, priority: number = 0): PriorityQueue<T> {
        const item = { value, priority };
        let inserted = false;
        
        // Insert in priority order (higher priority first)
        for (let i = 0; i < this.items.length; i++) {
            if (this.items[i].priority < priority) {
                this.items.splice(i, 0, item);
                inserted = true;
                break;
            }
        }
        
        if (!inserted) {
            this.items.push(item);
        }
        
        return this;
    }

    /**
     * Remove and return the highest priority element
     * @returns The highest priority element, or undefined if empty
     * @timeComplexity O(1)
     */
    dequeue(): T | undefined {
        return this.items.shift()?.value;
    }

    /**
     * Get the highest priority element without removing it
     * @returns The highest priority element, or undefined if empty
     * @timeComplexity O(1)
     */
    peek(): T | undefined {
        return this.items[0]?.value;
    }

    /**
     * Get the priority of the highest priority element
     * @returns The priority, or undefined if empty
     * @timeComplexity O(1)
     */
    peekPriority(): number | undefined {
        return this.items[0]?.priority;
    }

    /**
     * Check if the priority queue is empty
     * @returns true if empty
     * @timeComplexity O(1)
     */
    isEmpty(): boolean {
        return this.items.length === 0;
    }

    /**
     * Get the number of elements in the priority queue
     * @returns The size
     * @timeComplexity O(1)
     */
    size(): number {
        return this.items.length;
    }

    /**
     * Remove all elements from the priority queue
     * @returns The priority queue instance for chaining
     * @timeComplexity O(1)
     */
    clear(): PriorityQueue<T> {
        this.items = [];
        return this;
    }

    /**
     * Convert the priority queue to an array (highest to lowest priority)
     * @returns Array representation
     * @timeComplexity O(n)
     */
    toArray(): T[] {
        return this.items.map(item => item.value);
    }

    /**
     * Get all items with their priorities
     * @returns Array of {value, priority} objects
     * @timeComplexity O(n)
     */
    toArrayWithPriority(): Array<{ value: T; priority: number }> {
        return [...this.items];
    }

    /**
     * Check if the priority queue contains a specific value
     * @param value - The value to search for
     * @returns true if found
     * @timeComplexity O(n)
     */
    contains(value: T): boolean {
        return this.items.some(item => item.value === value);
    }

    /**
     * Update the priority of an existing element
     * @param value - The value to update
     * @param newPriority - The new priority
     * @returns true if element was found and updated
     * @timeComplexity O(n)
     */
    updatePriority(value: T, newPriority: number): boolean {
        const index = this.items.findIndex(item => item.value === value);
        if (index === -1) return false;
        
        // Remove and re-insert with new priority
        this.items.splice(index, 1);
        this.enqueue(value, newPriority);
        return true;
    }

    /**
     * Iterate over the priority queue elements
     */
    *[Symbol.iterator](): Iterator<T> {
        for (const item of this.items) {
            yield item.value;
        }
    }
}

/**
 * Double-ended Queue (Deque) implementation
 * 
 * A queue that supports adding and removing elements from both ends.
 * 
 * @example
 * ```typescript
 * const deque = new Deque<number>();
 * deque.pushBack(1);
 * deque.pushFront(2);
 * deque.pushBack(3);
 * console.log(deque.toArray()); // [2, 1, 3]
 * console.log(deque.popFront()); // 2
 * console.log(deque.popBack()); // 3
 * ```
 */
export class Deque<T> {
    private head: QueueNode<T> | null = null;
    private tail: QueueNode<T> | null = null;
    private _size: number = 0;

    /**
     * Add an element to the front of the deque
     * @param value - The value to add
     * @returns The deque instance for chaining
     * @timeComplexity O(1)
     */
    pushFront(value: T): Deque<T> {
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

    /**
     * Add an element to the back of the deque
     * @param value - The value to add
     * @returns The deque instance for chaining
     * @timeComplexity O(1)
     */
    pushBack(value: T): Deque<T> {
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

    /**
     * Remove and return the front element
     * @returns The front element, or undefined if empty
     * @timeComplexity O(1)
     */
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

    /**
     * Remove and return the back element
     * @returns The back element, or undefined if empty
     * @timeComplexity O(1)
     */
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

    /**
     * Get the front element without removing it
     * @returns The front element, or undefined if empty
     * @timeComplexity O(1)
     */
    peekFront(): T | undefined {
        return this.head?.value;
    }

    /**
     * Get the back element without removing it
     * @returns The back element, or undefined if empty
     * @timeComplexity O(1)
     */
    peekBack(): T | undefined {
        return this.tail?.value;
    }

    /**
     * Check if the deque is empty
     * @returns true if empty
     * @timeComplexity O(1)
     */
    isEmpty(): boolean {
        return this._size === 0;
    }

    /**
     * Get the number of elements in the deque
     * @returns The size
     * @timeComplexity O(1)
     */
    size(): number {
        return this._size;
    }

    /**
     * Remove all elements from the deque
     * @returns The deque instance for chaining
     * @timeComplexity O(1)
     */
    clear(): Deque<T> {
        this.head = this.tail = null;
        this._size = 0;
        return this;
    }

    /**
     * Convert the deque to an array (front to back)
     * @returns Array representation
     * @timeComplexity O(n)
     */
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
     * Check if the deque contains a specific value
     * @param value - The value to search for
     * @returns true if found
     * @timeComplexity O(n)
     */
    contains(value: T): boolean {
        let current = this.head;
        while (current) {
            if (current.value === value) return true;
            current = current.next;
        }
        return false;
    }

    /**
     * Reverse the deque in place
     * @returns The deque instance for chaining
     * @timeComplexity O(n)
     */
    reverse(): Deque<T> {
        let current = this.head;
        let temp: QueueNode<T> | null = null;
        
        while (current) {
            temp = current.prev;
            current.prev = current.next;
            current.next = temp;
            current = current.prev;
        }
        
        temp = this.head;
        this.head = this.tail;
        this.tail = temp;
        
        return this;
    }

    /**
     * Iterate over the deque elements
     */
    *[Symbol.iterator](): Iterator<T> {
        let current = this.head;
        while (current) {
            yield current.value;
            current = current.next;
        }
    }
}

/**
 * Circular Buffer (Ring Buffer) implementation
 * 
 * A fixed-size buffer that overwrites old data when full.
 * Useful for implementing sliding windows and rate limiting.
 * 
 * @example
 * ```typescript
 * const buffer = new CircularBuffer<number>(3);
 * buffer.write(1);
 * buffer.write(2);
 * buffer.write(3);
 * buffer.write(4); // overwrites 1
 * console.log(buffer.toArray()); // [2, 3, 4]
 * ```
 */
export class CircularBuffer<T> {
    private buffer: (T | undefined)[];
    private writeIndex: number = 0;
    private readIndex: number = 0;
    private _size: number = 0;
    private capacity: number;

    constructor(capacity: number) {
        if (capacity <= 0) {
            throw new Error('Capacity must be greater than 0');
        }
        this.capacity = capacity;
        this.buffer = new Array(capacity);
    }

    /**
     * Write a value to the buffer
     * @param value - The value to write
     * @returns true if write succeeded, false if buffer is full (in overwrite mode)
 * @timeComplexity O(1)
     */
    write(value: T): boolean {
        if (this.isFull()) {
            // Overwrite mode: advance read pointer
            this.buffer[this.writeIndex] = value;
            this.writeIndex = (this.writeIndex + 1) % this.capacity;
            this.readIndex = this.writeIndex;
            return true;
        }
        
        this.buffer[this.writeIndex] = value;
        this.writeIndex = (this.writeIndex + 1) % this.capacity;
        this._size++;
        return true;
    }

    /**
     * Read and remove the oldest value from the buffer
     * @returns The oldest value, or undefined if empty
     * @timeComplexity O(1)
     */
    read(): T | undefined {
        if (this.isEmpty()) return undefined;
        
        const value = this.buffer[this.readIndex];
        this.buffer[this.readIndex] = undefined;
        this.readIndex = (this.readIndex + 1) % this.capacity;
        this._size--;
        return value;
    }

    /**
     * Peek at the oldest value without removing it
     * @returns The oldest value, or undefined if empty
     * @timeComplexity O(1)
     */
    peek(): T | undefined {
        if (this.isEmpty()) return undefined;
        return this.buffer[this.readIndex];
    }

    /**
     * Check if the buffer is empty
     * @returns true if empty
     * @timeComplexity O(1)
     */
    isEmpty(): boolean {
        return this._size === 0;
    }

    /**
     * Check if the buffer is full
     * @returns true if full
     * @timeComplexity O(1)
     */
    isFull(): boolean {
        return this._size === this.capacity;
    }

    /**
     * Get the number of elements in the buffer
     * @returns The current size
     * @timeComplexity O(1)
     */
    size(): number {
        return this._size;
    }

    /**
     * Get the buffer capacity
     * @returns The capacity
     * @timeComplexity O(1)
     */
    getCapacity(): number {
        return this.capacity;
    }

    /**
     * Clear all elements from the buffer
     * @returns The buffer instance for chaining
     * @timeComplexity O(1)
     */
    clear(): CircularBuffer<T> {
        this.buffer = new Array(this.capacity);
        this.writeIndex = 0;
        this.readIndex = 0;
        this._size = 0;
        return this;
    }

    /**
     * Convert the buffer to an array (oldest to newest)
     * @returns Array representation
     * @timeComplexity O(n)
     */
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

    /**
     * Check if the buffer contains a specific value
     * @param value - The value to search for
     * @returns true if found
     * @timeComplexity O(n)
     */
    contains(value: T): boolean {
        for (let i = 0; i < this._size; i++) {
            const index = (this.readIndex + i) % this.capacity;
            if (this.buffer[index] === value) return true;
        }
        return false;
    }

    /**
     * Iterate over the buffer elements
     */
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

/**
 * Queue Utilities - Static helper functions
 * 
 * Provides utility functions for working with queues and performing
 * common queue-related operations.
 */
export class QueueUtils {
    /**
     * Create a queue from an array
     * @param array - The source array
     * @returns A new Queue with elements from the array
     */
    static fromArray<T>(array: T[]): Queue<T> {
        const queue = new Queue<T>();
        for (const item of array) {
            queue.enqueue(item);
        }
        return queue;
    }

    /**
     * Create a stack from an array
     * @param array - The source array
     * @returns A new Stack with elements from the array
     */
    static stackFromArray<T>(array: T[]): Stack<T> {
        const stack = new Stack<T>();
        for (const item of array) {
            stack.push(item);
        }
        return stack;
    }

    /**
     * Create a priority queue from an array of {value, priority} objects
     * @param array - Array of objects with value and priority
     * @returns A new PriorityQueue
     */
    static priorityQueueFromArray<T>(array: Array<{ value: T; priority: number }>): PriorityQueue<T> {
        const pq = new PriorityQueue<T>();
        for (const item of array) {
            pq.enqueue(item.value, item.priority);
        }
        return pq;
    }

    /**
     * Reverse a queue (returns a new queue)
     * @param queue - The queue to reverse
     * @returns A new Queue with elements in reverse order
     */
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

    /**
     * Merge two queues (queue1 first, then queue2)
     * @param queue1 - First queue
     * @param queue2 - Second queue
     * @returns A new Queue with elements from both
     */
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

    /**
     * Check if a queue is a palindrome
     * @param queue - The queue to check
     * @returns true if the queue is a palindrome
     */
    static isPalindrome<T>(queue: Queue<T>): boolean {
        const arr = queue.toArray();
        for (let i = 0; i < arr.length / 2; i++) {
            if (arr[i] !== arr[arr.length - 1 - i]) {
                return false;
            }
        }
        return true;
    }

    /**
     * Sort a queue using a comparison function
     * @param queue - The queue to sort
     * @param compareFn - Optional comparison function
     * @returns A new sorted Queue
     */
    static sort<T>(queue: Queue<T>, compareFn?: (a: T, b: T) => number): Queue<T> {
        const arr = queue.toArray();
        arr.sort(compareFn);
        return QueueUtils.fromArray(arr);
    }

    /**
     * Filter a queue based on a predicate
     * @param queue - The queue to filter
     * @param predicate - The filter function
     * @returns A new Queue with filtered elements
     */
    static filter<T>(queue: Queue<T>, predicate: (value: T) => boolean): Queue<T> {
        const result = new Queue<T>();
        for (const item of queue) {
            if (predicate(item)) {
                result.enqueue(item);
            }
        }
        return result;
    }

    /**
     * Map a queue to a new queue with transformed values
     * @param queue - The queue to map
     * @param transform - The transform function
     * @returns A new Queue with transformed elements
     */
    static map<T, U>(queue: Queue<T>, transform: (value: T) => U): Queue<U> {
        const result = new Queue<U>();
        for (const item of queue) {
            result.enqueue(transform(item));
        }
        return result;
    }

    /**
     * Reduce a queue to a single value
     * @param queue - The queue to reduce
     * @param reducer - The reducer function
     * @param initialValue - The initial value
     * @returns The reduced value
     */
    static reduce<T, U>(queue: Queue<T>, reducer: (acc: U, value: T) => U, initialValue: U): U {
        let result = initialValue;
        for (const item of queue) {
            result = reducer(result, item);
        }
        return result;
    }

    /**
     * Find the first element matching a predicate
     * @param queue - The queue to search
     * @param predicate - The search function
     * @returns The first matching element, or undefined
     */
    static find<T>(queue: Queue<T>, predicate: (value: T) => boolean): T | undefined {
        for (const item of queue) {
            if (predicate(item)) {
                return item;
            }
        }
        return undefined;
    }

    /**
     * Count elements matching a predicate
     * @param queue - The queue to count
     * @param predicate - The counting function
     * @returns The count of matching elements
     */
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

// Default exports
export default {
    Queue,
    Stack,
    PriorityQueue,
    Deque,
    CircularBuffer,
    QueueUtils
};
