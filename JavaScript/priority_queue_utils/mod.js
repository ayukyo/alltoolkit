/**
 * Priority Queue Utils - A zero-dependency priority queue implementation
 * 
 * Features:
 * - Min-heap based priority queue
 * - Support for custom comparators
 * - Efficient O(log n) insert and extract operations
 * - Peek, update, and remove operations
 * - Bulk operations for building from array
 * 
 * @module priority_queue_utils
 */

/**
 * Default comparator for min-heap behavior (lower values have higher priority)
 * @param {*} a - First value
 * @param {*} b - Second value
 * @returns {number} Negative if a has higher priority, positive if b has higher priority
 */
function defaultComparator(a, b) {
  if (a < b) return -1;
  if (a > b) return 1;
  return 0;
}

/**
 * Priority Queue implementation using binary heap
 */
class PriorityQueue {
  /**
   * Create a new priority queue
   * @param {Function} [comparator=defaultComparator] - Comparison function
   * @param {Array} [items=[]] - Initial items to add
   */
  constructor(comparator = defaultComparator, items = []) {
    this._heap = [];
    this._comparator = comparator || defaultComparator;
    this._size = 0;
    
    if (items.length > 0) {
      this._heap = items.slice();
      this._size = items.length;
      this._heapify();
    }
  }

  /**
   * Get the number of items in the queue
   * @returns {number} Size of the queue
   */
  get size() {
    return this._size;
  }

  /**
   * Check if the queue is empty
   * @returns {boolean} True if empty
   */
  isEmpty() {
    return this._size === 0;
  }

  /**
   * Insert an item into the queue
   * @param {*} item - Item to insert
   * @returns {PriorityQueue} This queue for chaining
   */
  enqueue(item) {
    this._heap.push(item);
    this._size++;
    this._siftUp(this._size - 1);
    return this;
  }

  /**
   * Alias for enqueue
   * @param {*} item - Item to insert
   * @returns {PriorityQueue} This queue for chaining
   */
  push(item) {
    return this.enqueue(item);
  }

  /**
   * Extract and return the highest priority item
   * @returns {*} The highest priority item, or undefined if empty
   */
  dequeue() {
    if (this.isEmpty()) {
      return undefined;
    }

    const result = this._heap[0];
    const last = this._heap.pop();
    this._size--;

    if (this._size > 0) {
      this._heap[0] = last;
      this._siftDown(0);
    }

    return result;
  }

  /**
   * Alias for dequeue
   * @returns {*} The highest priority item, or undefined if empty
   */
  pop() {
    return this.dequeue();
  }

  /**
   * Peek at the highest priority item without removing it
   * @returns {*} The highest priority item, or undefined if empty
   */
  peek() {
    return this.isEmpty() ? undefined : this._heap[0];
  }

  /**
   * Alias for peek
   * @returns {*} The highest priority item, or undefined if empty
   */
  front() {
    return this.peek();
  }

  /**
   * Clear all items from the queue
   */
  clear() {
    this._heap = [];
    this._size = 0;
  }

  /**
   * Convert the queue to an array (not sorted)
   * @returns {Array} Array of items
   */
  toArray() {
    return this._heap.slice();
  }

  /**
   * Get all items in priority order (creates a copy)
   * @returns {Array} Sorted array of items
   */
  toSortedArray() {
    const result = [];
    const temp = new PriorityQueue(this._comparator, this._heap);
    while (!temp.isEmpty()) {
      result.push(temp.dequeue());
    }
    return result;
  }

  /**
   * Find an item matching a predicate
   * @param {Function} predicate - Function to test each item
   * @returns {*} The found item, or undefined
   */
  find(predicate) {
    for (const item of this._heap) {
      if (predicate(item)) {
        return item;
      }
    }
    return undefined;
  }

  /**
   * Find all items matching a predicate
   * @param {Function} predicate - Function to test each item
   * @returns {Array} Array of matching items
   */
  filter(predicate) {
    return this._heap.filter(predicate);
  }

  /**
   * Check if any item matches a predicate
   * @param {Function} predicate - Function to test each item
   * @returns {boolean} True if any item matches
   */
  some(predicate) {
    return this._heap.some(predicate);
  }

  /**
   * Check if all items match a predicate
   * @param {Function} predicate - Function to test each item
   * @returns {boolean} True if all items match
   */
  every(predicate) {
    return this._heap.every(predicate);
  }

  /**
   * Remove all items matching a predicate
   * @param {Function} predicate - Function to test each item
   * @returns {number} Number of items removed
   */
  remove(predicate) {
    const originalSize = this._size;
    this._heap = this._heap.filter(item => !predicate(item));
    this._size = this._heap.length;
    this._heapify();
    return originalSize - this._size;
  }

  /**
   * Update an item and restore heap property
   * @param {Function} predicate - Function to find the item
   * @param {Function} updater - Function to update the item
   * @returns {boolean} True if item was found and updated
   */
  update(predicate, updater) {
    for (let i = 0; i < this._size; i++) {
      if (predicate(this._heap[i])) {
        this._heap[i] = updater(this._heap[i]);
        // Re-heapify from this position
        this._siftUp(i);
        this._siftDown(i);
        return true;
      }
    }
    return false;
  }

  /**
   * Merge another priority queue into this one
   * @param {PriorityQueue} other - Another priority queue
   * @returns {PriorityQueue} This queue for chaining
   */
  merge(other) {
    if (!(other instanceof PriorityQueue)) {
      throw new TypeError('Can only merge with another PriorityQueue');
    }
    
    for (const item of other._heap) {
      this.enqueue(item);
    }
    return this;
  }

  /**
   * Create a new priority queue from merging two queues
   * @param {PriorityQueue} a - First queue
   * @param {PriorityQueue} b - Second queue
   * @returns {PriorityQueue} New merged queue
   */
  static merge(a, b) {
    const result = new PriorityQueue(a._comparator);
    result.merge(a);
    result.merge(b);
    return result;
  }

  /**
   * Create a priority queue from an array
   * @param {Array} items - Array of items
   * @param {Function} [comparator] - Optional comparator
   * @returns {PriorityQueue} New priority queue
   */
  static from(items, comparator) {
    return new PriorityQueue(comparator, items);
  }

  /**
   * Create a min-heap priority queue
   * @param {Array} [items] - Initial items
   * @returns {PriorityQueue} Min-heap priority queue
   */
  static minHeap(items = []) {
    return new PriorityQueue((a, b) => a - b, items);
  }

  /**
   * Create a max-heap priority queue
   * @param {Array} [items] - Initial items
   * @returns {PriorityQueue} Max-heap priority queue
   */
  static maxHeap(items = []) {
    return new PriorityQueue((a, b) => b - a, items);
  }

  /**
   * Heapify the internal heap array
   * @private
   */
  _heapify() {
    // Start from the last non-leaf node and sift down each
    for (let i = Math.floor(this._size / 2) - 1; i >= 0; i--) {
      this._siftDown(i);
    }
  }

  /**
   * Sift up from a given index
   * @param {number} index - Starting index
   * @private
   */
  _siftUp(index) {
    while (index > 0) {
      const parentIndex = Math.floor((index - 1) / 2);
      if (this._comparator(this._heap[index], this._heap[parentIndex]) >= 0) {
        break;
      }
      this._swap(index, parentIndex);
      index = parentIndex;
    }
  }

  /**
   * Sift down from a given index
   * @param {number} index - Starting index
   * @private
   */
  _siftDown(index) {
    while (true) {
      const leftChild = 2 * index + 1;
      const rightChild = 2 * index + 2;
      let smallest = index;

      if (leftChild < this._size && 
          this._comparator(this._heap[leftChild], this._heap[smallest]) < 0) {
        smallest = leftChild;
      }

      if (rightChild < this._size && 
          this._comparator(this._heap[rightChild], this._heap[smallest]) < 0) {
        smallest = rightChild;
      }

      if (smallest === index) {
        break;
      }

      this._swap(index, smallest);
      index = smallest;
    }
  }

  /**
   * Swap two elements in the heap
   * @param {number} i - First index
   * @param {number} j - Second index
   * @private
   */
  _swap(i, j) {
    [this._heap[i], this._heap[j]] = [this._heap[j], this._heap[i]];
  }

  /**
   * Make the queue iterable
   * Yields items in heap order (not priority order)
   */
  *[Symbol.iterator]() {
    yield* this._heap;
  }
}

/**
 * Indexed Priority Queue - allows updating priorities by key
 */
class IndexedPriorityQueue {
  /**
   * Create an indexed priority queue
   * @param {Function} [comparator=defaultComparator] - Comparison function
   */
  constructor(comparator = defaultComparator) {
    this._pq = new PriorityQueue(
      (a, b) => comparator(a.priority, b.priority),
      []
    );
    this._index = new Map();
  }

  /**
   * Get the number of items
   * @returns {number} Size
   */
  get size() {
    return this._pq.size;
  }

  /**
   * Check if empty
   * @returns {boolean} True if empty
   */
  isEmpty() {
    return this._pq.isEmpty();
  }

  /**
   * Set or update a key with a priority
   * @param {string} key - Unique key
   * @param {number} priority - Priority value
   * @param {*} [value] - Optional associated value
   * @returns {boolean} True if key was updated (false if new)
   */
  set(key, priority, value = null) {
    const exists = this._index.has(key);
    if (exists) {
      this._pq.update(
        item => item.key === key,
        () => ({ key, priority, value })
      );
    } else {
      this._pq.enqueue({ key, priority, value });
    }
    this._index.set(key, { priority, value });
    return exists;
  }

  /**
   * Check if a key exists
   * @param {string} key - Key to check
   * @returns {boolean} True if exists
   */
  has(key) {
    return this._index.has(key);
  }

  /**
   * Get the priority of a key
   * @param {string} key - Key to look up
   * @returns {number|undefined} Priority or undefined
   */
  getPriority(key) {
    return this._index.get(key)?.priority;
  }

  /**
   * Get the value associated with a key
   * @param {string} key - Key to look up
   * @returns {*|undefined} Value or undefined
   */
  get(key) {
    return this._index.get(key)?.value;
  }

  /**
   * Remove and return the highest priority item
   * @returns {Object|undefined} { key, priority, value } or undefined
   */
  dequeue() {
    const item = this._pq.dequeue();
    if (item) {
      this._index.delete(item.key);
    }
    return item;
  }

  /**
   * Alias for dequeue
   * @returns {Object|undefined} { key, priority, value } or undefined
   */
  pop() {
    return this.dequeue();
  }

  /**
   * Peek at the highest priority item
   * @returns {Object|undefined} { key, priority, value } or undefined
   */
  peek() {
    return this._pq.peek();
  }

  /**
   * Remove a key from the queue
   * @param {string} key - Key to remove
   * @returns {boolean} True if key was found and removed
   */
  delete(key) {
    if (!this._index.has(key)) {
      return false;
    }
    this._pq.remove(item => item.key === key);
    this._index.delete(key);
    return true;
  }

  /**
   * Clear all items
   */
  clear() {
    this._pq.clear();
    this._index.clear();
  }

  /**
   * Get all keys
   * @returns {Array} Array of keys
   */
  keys() {
    return Array.from(this._index.keys());
  }
}

// Export classes and utilities
module.exports = {
  PriorityQueue,
  IndexedPriorityQueue,
  defaultComparator
};