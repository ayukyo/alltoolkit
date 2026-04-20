/**
 * Top-N Selection Utilities
 * Efficient algorithms for finding top N largest/smallest elements
 * Uses heap-based approach for O(n log k) time complexity
 */

/**
 * Min-heap implementation for finding largest elements
 */
class MinHeap<T> {
  private data: T[] = [];
  private comparator: (a: T, b: T) => number;

  constructor(comparator: (a: T, b: T) => number) {
    this.comparator = comparator;
  }

  get length(): number {
    return this.data.length;
  }

  peek(): T | undefined {
    return this.data[0];
  }

  push(value: T): void {
    this.data.push(value);
    this.bubbleUp(this.data.length - 1);
  }

  pop(): T | undefined {
    if (this.data.length === 0) return undefined;
    const top = this.data[0];
    const last = this.data.pop()!;
    if (this.data.length > 0) {
      this.data[0] = last;
      this.bubbleDown(0);
    }
    return top;
  }

  private bubbleUp(index: number): void {
    while (index > 0) {
      const parentIndex = Math.floor((index - 1) / 2);
      if (this.comparator(this.data[index], this.data[parentIndex]) >= 0) break;
      [this.data[index], this.data[parentIndex]] = [this.data[parentIndex], this.data[index]];
      index = parentIndex;
    }
  }

  private bubbleDown(index: number): void {
    const length = this.data.length;
    while (true) {
      const leftChild = 2 * index + 1;
      const rightChild = 2 * index + 2;
      let smallest = index;

      if (leftChild < length && this.comparator(this.data[leftChild], this.data[smallest]) < 0) {
        smallest = leftChild;
      }
      if (rightChild < length && this.comparator(this.data[rightChild], this.data[smallest]) < 0) {
        smallest = rightChild;
      }

      if (smallest === index) break;
      [this.data[index], this.data[smallest]] = [this.data[smallest], this.data[index]];
      index = smallest;
    }
  }

  toArray(): T[] {
    return [...this.data];
  }
}

/**
 * Max-heap implementation for finding smallest elements
 */
class MaxHeap<T> {
  private heap: MinHeap<T>;

  constructor(comparator: (a: T, b: T) => number) {
    // Invert comparator for max-heap behavior
    this.heap = new MinHeap<T>((a, b) => -comparator(a, b));
  }

  get length(): number {
    return this.heap.length;
  }

  peek(): T | undefined {
    return this.heap.peek();
  }

  push(value: T): void {
    this.heap.push(value);
  }

  pop(): T | undefined {
    return this.heap.pop();
  }

  toArray(): T[] {
    return this.heap.toArray();
  }
}

/**
 * Top-N Finder class for efficient selection of top elements
 */
export class TopNFinder {
  private n: number;

  constructor(n: number) {
    this.n = n > 0 ? n : 1;
  }

  /**
   * Find the top N largest numbers from an array
   * Returns sorted in descending order
   * Time: O(n log k), Space: O(k) where k is N
   */
  largest(data: number[]): number[] {
    if (data.length === 0 || this.n <= 0) return [];

    const k = Math.min(this.n, data.length);
    const heap = new MinHeap<number>((a, b) => a - b);

    for (const value of data) {
      if (heap.length < k) {
        heap.push(value);
      } else if (value > heap.peek()!) {
        heap.pop();
        heap.push(value);
      }
    }

    // Extract and sort in descending order
    const result: number[] = [];
    while (heap.length > 0) {
      result.unshift(heap.pop()!);
    }
    return result;
  }

  /**
   * Find the top N smallest numbers from an array
   * Returns sorted in ascending order
   */
  smallest(data: number[]): number[] {
    if (data.length === 0 || this.n <= 0) return [];

    const k = Math.min(this.n, data.length);
    const heap = new MaxHeap<number>((a, b) => a - b);

    for (const value of data) {
      if (heap.length < k) {
        heap.push(value);
      } else if (value < heap.peek()!) {
        heap.pop();
        heap.push(value);
      }
    }

    // Extract and sort in ascending order
    const result: number[] = [];
    while (heap.length > 0) {
      result.unshift(heap.pop()!);
    }
    return result;
  }
}

/**
 * Find the top N largest numbers (convenience function)
 */
export function topNLargest(data: number[], n: number): number[] {
  return new TopNFinder(n).largest(data);
}

/**
 * Find the top N smallest numbers (convenience function)
 */
export function topNSmallest(data: number[], n: number): number[] {
  return new TopNFinder(n).smallest(data);
}

/**
 * Find the top N largest strings (lexicographically)
 */
export function topNLargestStrings(data: string[], n: number): string[] {
  if (data.length === 0 || n <= 0) return [];

  const k = Math.min(n, data.length);
  const heap = new MinHeap<string>((a, b) => a.localeCompare(b));

  for (const value of data) {
    if (heap.length < k) {
      heap.push(value);
    } else if (value.localeCompare(heap.peek()!) > 0) {
      heap.pop();
      heap.push(value);
    }
  }

  const result: string[] = [];
  while (heap.length > 0) {
    result.unshift(heap.pop()!);
  }
  return result;
}

/**
 * Find the top N smallest strings (lexicographically)
 */
export function topNSmallestStrings(data: string[], n: number): string[] {
  if (data.length === 0 || n <= 0) return [];

  const k = Math.min(n, data.length);
  const heap = new MaxHeap<string>((a, b) => a.localeCompare(b));

  for (const value of data) {
    if (heap.length < k) {
      heap.push(value);
    } else if (value.localeCompare(heap.peek()!) < 0) {
      heap.pop();
      heap.push(value);
    }
  }

  const result: string[] = [];
  while (heap.length > 0) {
    result.unshift(heap.pop()!);
  }
  return result;
}

/**
 * Generic item interface for custom scored items
 */
export interface ScoredItem<T> {
  value: T;
  score: number;
}

/**
 * Find the top N items with highest scores
 */
export function topNLargestItems<T>(items: ScoredItem<T>[], n: number): ScoredItem<T>[] {
  if (items.length === 0 || n <= 0) return [];

  const k = Math.min(n, items.length);
  const heap = new MinHeap<ScoredItem<T>>((a, b) => a.score - b.score);

  for (const item of items) {
    if (heap.length < k) {
      heap.push(item);
    } else if (item.score > heap.peek()!.score) {
      heap.pop();
      heap.push(item);
    }
  }

  const result: ScoredItem<T>[] = [];
  while (heap.length > 0) {
    result.unshift(heap.pop()!);
  }
  return result;
}

/**
 * Find the top N items with lowest scores
 */
export function topNSmallestItems<T>(items: ScoredItem<T>[], n: number): ScoredItem<T>[] {
  if (items.length === 0 || n <= 0) return [];

  const k = Math.min(n, items.length);
  const heap = new MaxHeap<ScoredItem<T>>((a, b) => a.score - b.score);

  for (const item of items) {
    if (heap.length < k) {
      heap.push(item);
    } else if (item.score < heap.peek()!.score) {
      heap.pop();
      heap.push(item);
    }
  }

  const result: ScoredItem<T>[] = [];
  while (heap.length > 0) {
    result.unshift(heap.pop()!);
  }
  return result;
}

/**
 * QuickSelect algorithm to find k-th smallest element (0-indexed)
 * Average O(n), worst O(n²)
 */
export function quickSelect(data: number[], k: number): number {
  if (data.length === 0 || k < 0 || k >= data.length) {
    throw new Error('Invalid input or index');
  }

  const arr = [...data]; // Don't modify original
  return quickSelectHelper(arr, 0, arr.length - 1, k);
}

function quickSelectHelper(arr: number[], left: number, right: number, k: number): number {
  if (left === right) return arr[left];

  const pivotIndex = partition(arr, left, right);

  if (k === pivotIndex) {
    return arr[k];
  } else if (k < pivotIndex) {
    return quickSelectHelper(arr, left, pivotIndex - 1, k);
  }
  return quickSelectHelper(arr, pivotIndex + 1, right, k);
}

function partition(arr: number[], left: number, right: number): number {
  const pivot = arr[right];
  let i = left;

  for (let j = left; j < right; j++) {
    if (arr[j] <= pivot) {
      [arr[i], arr[j]] = [arr[j], arr[i]];
      i++;
    }
  }
  [arr[i], arr[right]] = [arr[right], arr[i]];
  return i;
}

/**
 * Find the k-th smallest element (1-indexed)
 */
export function kthSmallest(data: number[], k: number): number {
  if (k < 1 || k > data.length) {
    throw new Error('Invalid k value');
  }
  return quickSelect(data, k - 1);
}

/**
 * Find the k-th largest element (1-indexed)
 */
export function kthLargest(data: number[], k: number): number {
  if (k < 1 || k > data.length) {
    throw new Error('Invalid k value');
  }
  return quickSelect(data, data.length - k);
}

/**
 * Calculate the median of a number array
 */
export function median(data: number[]): number {
  if (data.length === 0) return 0;

  const sorted = [...data].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);

  if (sorted.length % 2 === 1) {
    return sorted[mid];
  }
  return (sorted[mid - 1] + sorted[mid]) / 2;
}

/**
 * Calculate the value at a given percentile (0-100)
 */
export function percentile(data: number[], p: number): number {
  if (data.length === 0 || p < 0 || p > 100) {
    throw new Error('Invalid input');
  }

  const sorted = [...data].sort((a, b) => a - b);
  const index = Math.floor((sorted.length - 1) * p / 100);
  return sorted[index];
}