/**
 * Array Utilities for ArkTS
 * 
 * A comprehensive array/collection manipulation utility module for ArkTS/HarmonyOS
 * providing common array operations with zero dependencies.
 * 
 * Features:
 * - Empty/blank checks and safety operations
 * - Element access (first, last, nth, safe access)
 * - Filtering and searching (find, filter, reject, contains)
 * - Transformation (map, flatMap, flatten)
 * - Sorting and ordering
 * - Set operations (unique, union, intersection, difference)
 * - Grouping and partitioning
 * - Aggregation (sum, average, min, max, count)
 * - Chunking and slicing
 * - Shuffling and sampling
 * - Immutable operations
 * 
 * @module array_utils
 * @version 1.0.0
 */

// ============================================
// Empty/Blank Checks
// ============================================

export function isEmpty<T>(arr: T[] | null | undefined): boolean {
  return arr === null || arr === undefined || arr.length === 0;
}

export function isNotEmpty<T>(arr: T[] | null | undefined): boolean {
  return !isEmpty(arr);
}

export function size<T>(arr: T[] | null | undefined): number {
  return arr?.length ?? 0;
}

// ============================================
// Safe Element Access
// ============================================

export function first<T>(arr: T[] | null | undefined): T | undefined {
  return arr && arr.length > 0 ? arr[0] : undefined;
}

export function last<T>(arr: T[] | null | undefined): T | undefined {
  return arr && arr.length > 0 ? arr[arr.length - 1] : undefined;
}

export function get<T>(arr: T[] | null | undefined, index: number, defaultValue?: T): T | undefined {
  if (arr === null || arr === undefined) {
    return defaultValue;
  }
  if (index < 0) {
    index = arr.length + index;
  }
  if (index < 0 || index >= arr.length) {
    return defaultValue;
  }
  return arr[index];
}

export function getOrThrow<T>(arr: T[], index: number): T {
  if (index < 0) {
    index = arr.length + index;
  }
  if (index < 0 || index >= arr.length) {
    throw new Error(`Index ${index} out of bounds for array of length ${arr.length}`);
  }
  return arr[index];
}

export function firstOrNull<T>(arr: T[] | null | undefined): T | null {
  return arr && arr.length > 0 ? arr[0] : null;
}

export function lastOrNull<T>(arr: T[] | null | undefined): T | null {
  return arr && arr.length > 0 ? arr[arr.length - 1] : null;
}

// ============================================
// Filtering and Searching
// ============================================

export function find<T>(arr: T[] | null | undefined, predicate: (item: T, index: number) => boolean): T | undefined {
  if (isEmpty(arr)) return undefined;
  for (let i = 0; i < arr!.length; i++) {
    if (predicate(arr![i], i)) {
      return arr![i];
    }
  }
  return undefined;
}

export function findLast<T>(arr: T[] | null | undefined, predicate: (item: T, index: number) => boolean): T | undefined {
  if (isEmpty(arr)) return undefined;
  for (let i = arr!.length - 1; i >= 0; i--) {
    if (predicate(arr![i], i)) {
      return arr![i];
    }
  }
  return undefined;
}

export function findIndex<T>(arr: T[] | null | undefined, predicate: (item: T, index: number) => boolean): number {
  if (isEmpty(arr)) return -1;
  for (let i = 0; i < arr!.length; i++) {
    if (predicate(arr![i], i)) {
      return i;
    }
  }
  return -1;
}

export function findLastIndex<T>(arr: T[] | null | undefined, predicate: (item: T, index: number) => boolean): number {
  if (isEmpty(arr)) return -1;
  for (let i = arr!.length - 1; i >= 0; i--) {
    if (predicate(arr![i], i)) {
      return i;
    }
  }
  return -1;
}

export function indexOf<T>(arr: T[] | null | undefined, item: T): number {
  if (isEmpty(arr)) return -1;
  return arr!.indexOf(item);
}

export function lastIndexOf<T>(arr: T[] | null | undefined, item: T): number {
  if (isEmpty(arr)) return -1;
  return arr!.lastIndexOf(item);
}

export function contains<T>(arr: T[] | null | undefined, item: T): boolean {
  if (isEmpty(arr)) return false;
  return arr!.includes(item);
}

export function containsAll<T>(arr: T[] | null | undefined, items: T[]): boolean {
  if (isEmpty(arr) || isEmpty(items)) return false;
  return items.every(item => arr!.includes(item));
}

export function containsAny<T>(arr: T[] | null | undefined, items: T[]): boolean {
  if (isEmpty(arr) || isEmpty(items)) return false;
  return items.some(item => arr!.includes(item));
}

export function filter<T>(arr: T[] | null | undefined, predicate: (item: T, index: number) => boolean): T[] {
  if (isEmpty(arr)) return [];
  return arr!.filter(predicate);
}

export function filterNot<T>(arr: T[] | null | undefined, predicate: (item: T, index: number) => boolean): T[] {
  if (isEmpty(arr)) return [];
  return arr!.filter((item, index) => !predicate(item, index));
}

export function reject<T>(arr: T[] | null | undefined, predicate: (item: T, index: number) => boolean): T[] {
  return filterNot(arr, predicate);
}

export function filterNull<T>(arr: (T | null | undefined)[] | null | undefined): T[] {
  if (isEmpty(arr)) return [];
  return arr!.filter((item): item is T => item !== null && item !== undefined);
}

// ============================================
// Transformation
// ============================================

export function map<T, R>(arr: T[] | null | undefined, mapper: (item: T, index: number) => R): R[] {
  if (isEmpty(arr)) return [];
  return arr!.map(mapper);
}

export function mapNotNull<T, R>(arr: T[] | null | undefined, mapper: (item: T, index: number) => R | null | undefined): R[] {
  if (isEmpty(arr)) return [];
  const result: R[] = [];
  for (let i = 0; i < arr!.length; i++) {
    const mapped = mapper(arr![i], i);
    if (mapped !== null && mapped !== undefined) {
      result.push(mapped);
    }
  }
  return result;
}

export function flatMap<T, R>(arr: T[] | null | undefined, mapper: (item: T, index: number) => R[]): R[] {
  if (isEmpty(arr)) return [];
  const result: R[] = [];
  for (let i = 0; i < arr!.length; i++) {
    result.push(...mapper(arr![i], i));
  }
  return result;
}

export function flatten<T>(arr: (T[])[] | null | undefined): T[] {
  if (isEmpty(arr)) return [];
  return arr!.flat();
}

export function flattenDeep<T>(arr: unknown[] | null | undefined): T[] {
  if (isEmpty(arr)) return [];
  const result: T[] = [];
  const flattenRecursive = (items: unknown[]): void => {
    for (const item of items) {
      if (Array.isArray(item)) {
        flattenRecursive(item);
      } else {
        result.push(item as T);
      }
    }
  };
  flattenRecursive(arr!);
  return result;
}

// ============================================
// Sorting and Ordering
// ============================================

export function sort<T>(arr: T[] | null | undefined): T[] {
  if (isEmpty(arr)) return [];
  return [...arr!].sort();
}

export function sortBy<T>(arr: T[] | null | undefined, keyFn: (item: T) => unknown): T[] {
  if (isEmpty(arr)) return [];
  return [...arr!].sort((a, b) => {
    const keyA = keyFn(a);
    const keyB = keyFn(b);
    if (keyA === keyB) return 0;
    if (keyA === null || keyA === undefined) return 1;
    if (keyB === null || keyB === undefined) return -1;
    return keyA < keyB ? -1 : 1;
  });
}

export function sortByDesc<T>(arr: T[] | null | undefined, keyFn: (item: T) => unknown): T[] {
  if (isEmpty(arr)) return [];
  return [...arr!].sort((a, b) => {
    const keyA = keyFn(a);
    const keyB = keyFn(b);
    if (keyA === keyB) return 0;
    if (keyA === null || keyA === undefined) return 1;
    if (keyB === null || keyB === undefined) return -1;
    return keyA > keyB ? -1 : 1;
  });
}

export function reverse<T>(arr: T[] | null | undefined): T[] {
  if (isEmpty(arr)) return [];
  return [...arr!].reverse();
}

export function shuffle<T>(arr: T[] | null | undefined): T[] {
  if (isEmpty(arr)) return [];
  const result = [...arr!];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

export function isSorted<T>(arr: T[] | null | undefined): boolean {
  if (isEmpty(arr) || arr!.length <= 1) return true;
  for (let i = 1; i < arr!.length; i++) {
    if (arr![i - 1] > arr![i]) return false;
  }
  return true;
}

export function isSortedBy<T>(arr: T[] | null | undefined, keyFn: (item: T) => unknown): boolean {
  if (isEmpty(arr) || arr!.length <= 1) return true;
  for (let i = 1; i < arr!.length; i++) {
    const keyA = keyFn(arr![i - 1]);
    const keyB = keyFn(arr![i]);
    if (keyA > keyB) return false;
  }
  return true;
}

// ============================================
// Set Operations
// ============================================

export function unique<T>(arr: T[] | null | undefined): T[] {
  if (isEmpty(arr)) return [];
  return [...new Set(arr!)];
}

export function uniqueBy<T>(arr: T[] | null | undefined, keyFn: (item: T) => unknown): T[] {
  if (isEmpty(arr)) return [];
  const seen = new Set<unknown>();
  const result: T[] = [];
  for (const item of arr!) {
    const key = keyFn(item);
    if (!seen.has(key)) {
      seen.add(key);
      result.push(item);
    }
  }
  return result;
}

export function union<T>(arr1: T[] | null | undefined, arr2: T[] | null | undefined): T[] {
  const result: T[] = [];
  const set = new Set<T>();
  for (const item of (arr1 ?? [])) {
    if (!set.has(item)) {
      set.add(item);
      result.push(item);
    }
  }
  for (const item of (arr2 ?? [])) {
    if (!set.has(item)) {
      set.add(item);
      result.push(item);
    }
  }
  return result;
}

export function intersection<T>(arr1: T[] | null | undefined, arr2: T[] | null | undefined): T[] {
  if (isEmpty(arr1) || isEmpty(arr2)) return [];
  const set2 = new Set(arr2);
  return arr1!.filter(item => set2.has(item));
}

export function difference<T>(arr1: T[] | null | undefined, arr2: T[] | null | undefined): T[] {
  if (isEmpty(arr1)) return [];
  if (isEmpty(arr2)) return [...arr1!];
  const set2 = new Set(arr2);
  return arr1!.filter(item => !set2.has(item));
}

export function symmetricDifference<T>(arr1: T[] | null | undefined, arr2: T[] | null | undefined): T[] {
  const diff1 = difference(arr1, arr2);
  const diff2 = difference(arr2, arr1);
  return [...diff1, ...diff2];
}

export function duplicates<T>(arr: T[] | null | undefined): T[] {
  if (isEmpty(arr)) return [];
  const seen = new Set<T>();
  const result: T[] = [];
  for (const item of arr!) {
    if (seen.has(item) && !result.includes(item)) {
      result.push(item);
    }
    seen.add(item);
  }
  return result;
}

export function hasDuplicates<T>(arr: T[] | null | undefined): boolean {
  if (isEmpty(arr)) return false;
  return new Set(arr!).size !== arr!.length;
}

// ============================================
// Grouping and Partitioning
// ============================================

export function groupBy<T, K extends string | number>(arr: T[] | null | undefined, keyFn: (item: T) => K): Record<K, T[]> {
  if (isEmpty(arr)) return {} as Record<K, T[]>;
  const result = {} as Record<K, T[]>;
  for (const item of arr!) {
    const key = keyFn(item);
    if (!result[key]) {
      result[key] = [];
    }
    result[key].push(item);
  }
  return result;
}

export function partition<T>(arr: T[] | null | undefined, predicate: (item: T, index: number) => boolean): [T[], T[]] {
  if (isEmpty(arr)) return [[], []];
  const pass: T[] = [];
  const fail: T[] = [];
  for (let i = 0; i < arr!.length; i++) {
    if (predicate(arr![i], i)) {
      pass.push(arr![i]);
    } else {
      fail.push(arr![i]);
    }
  }
  return [pass, fail];
}

export function chunk<T>(arr: T[] | null | undefined, size: number): T[][] {
  if (isEmpty(arr) || size <= 0) return [];
  const result: T[][] = [];
  for (let i = 0; i < arr!.length; i += size) {
    result.push(arr!.slice(i, i + size));
  }
  return result;
}

export function splitAt<T>(arr: T[] | null | undefined, index: number): [T[], T[]] {
  if (isEmpty(arr)) return [[], []];
  if (index < 0) {
    index = Math.max(0, arr!.length + index);
  }
  return [arr!.slice(0, index), arr!.slice(index)];
}

// ============================================
// Slicing and Taking
// ============================================

export function take<T>(arr: T[] | null | undefined, n: number): T[] {
  if (isEmpty(arr)) return [];
  if (n <= 0) return [];
  return arr!.slice(0, n);
}

export function takeLast<T>(arr: T[] | null | undefined, n: number): T[] {
  if (isEmpty(arr)) return [];
  if (n <= 0) return [];
  return arr!.slice(-n);
}

export function takeWhile<T>(arr: T[] | null | undefined, predicate: (item: T, index: number) => boolean): T[] {
  if (isEmpty(arr)) return [];
  const result: T[] = [];
  for (let i = 0; i < arr!.length; i++) {
    if (predicate(arr![i], i)) {
      result.push(arr![i]);
    } else {
      break;
    }
  }
  return result;
}

export function drop<T>(arr: T[] | null | undefined, n: number): T[] {
  if (isEmpty(arr)) return [];
  if (n <= 0) return [...arr!];
  return arr!.slice(n);
}

export function dropLast<T>(arr: T[] | null | undefined, n: number): T[] {
  if (isEmpty(arr)) return [];
  if (n <= 0) return [...arr!];
  return arr!.slice(0, -n);
}

export function dropWhile<T>(arr: T[] | null | undefined, predicate: (item: T, index: number) => boolean): T[] {
  if (isEmpty(arr)) return [];
  let dropCount = 0;
  for (let i = 0; i < arr!.length; i++) {
    if (predicate(arr![i], i)) {
      dropCount++;
    } else {
      break;
    }
  }
  return arr!.slice(dropCount);
}

export function slice<T>(arr: T[] | null | undefined, start: number, end?: number): T[] {
  if (isEmpty(arr)) return [];
  return arr!.slice(start, end);
}

// ============================================
// Aggregation
// ============================================

export function sum(arr: number[] | null | undefined): number {
  if (isEmpty(arr)) return 0;
  return arr!.reduce((acc, val) => acc + val, 0);
}

export function sumBy<T>(arr: T[] | null | undefined, valueFn: (item: T) => number): number {
  if (isEmpty(arr)) return 0;
  return arr!.reduce((acc, item) => acc + valueFn(item), 0);
}

export function average(arr: number[] | null | undefined): number {
  if (isEmpty(arr)) return 0;
  return sum(arr) / arr!.length;
}

export function averageBy<T>(arr: T[] | null | undefined, valueFn: (item: T) => number): number {
  if (isEmpty(arr)) return 0;
  return sumBy(arr, valueFn) / arr!.length;
}

export function min<T>(arr: T[] | null | undefined): T | undefined {
  if (isEmpty(arr)) return undefined;
  return arr!.reduce((min, val) => val < min ? val : min);
}

export function max<T>(arr: T[] | null | undefined): T | undefined {
  if (isEmpty(arr)) return undefined;
  return arr!.reduce((max, val) => val > max ? val : max);
}

export function minBy<T>(arr: T[] | null | undefined, keyFn: (item: T) => number): T | undefined {
  if (isEmpty(arr)) return undefined;
  let minItem = arr![0];
  let minVal = keyFn(minItem);
  for (let i = 1; i < arr!.length; i++) {
    const val = keyFn(arr![i]);
    if (val < minVal) {
      minVal = val;
      minItem = arr![i];
    }
  }
  return minItem;
}

export function maxBy<T>(arr: T[] | null | undefined, keyFn: (item: T) => number): T | undefined {
  if (isEmpty(arr)) return undefined;
  let maxItem = arr![0];
  let maxVal = keyFn(maxItem);
  for (let i = 1; i < arr!.length; i++) {
    const val = keyFn(arr![i]);
    if (val > maxVal) {
      maxVal = val;
      maxItem = arr![i];
    }
  }
  return maxItem;
}

export function count<T>(arr: T[] | null | undefined, predicate?: (item: T, index: number) => boolean): number {
  if (isEmpty(arr)) return 0;
  if (!predicate) return arr!.length;
  return arr!.filter(predicate).length;
}

export function countBy<T>(arr: T[] | null | undefined, keyFn: (item: T) => string | number): Record<string | number, number> {
  if (isEmpty(arr)) return {};
  const result: Record<string | number, number> = {};
  for (const item of arr!) {
    const key = keyFn(item);
    result[key] = (result[key] || 0) + 1;
  }
  return result;
}

// ============================================
// Random Operations
// ============================================

export function randomElement<T>(arr: T[] | null | undefined): T | undefined {
  if (isEmpty(arr)) return undefined;
  return arr![Math.floor(Math.random() * arr!.length)];
}

export function randomElements<T>(arr: T[] | null | undefined, count: number): T[] {
  if (isEmpty(arr)) return [];
  if (count <= 0) return [];
  const shuffled = shuffle(arr)!;
  return shuffled.slice(0, Math.min(count, shuffled.length));
}

export function sample<T>(arr: T[] | null | undefined, count: number): T[] {
  return randomElements(arr, count);
}

// ============================================
// Modification (Immutable)
// ============================================

export function insert<T>(arr: T[] | null | undefined, index: number, item: T): T[] {
  if (isEmpty(arr)) return [item];
  const result = [...arr!];
  result.splice(index, 0, item);
  return result;
}

export function insertAll<T>(arr: T[] | null | undefined, index: number, items: T[]): T[] {
  if (isEmpty(arr)) return [...items];
  const result = [...arr!];
  result.splice(index, 0, ...items);
  return result;
}

export function removeAt<T>(arr: T[] | null | undefined, index: number): T[] {
  if (isEmpty(arr)) return [];
  const result = [...arr!];
  result.splice(index, 1);
  return result;
}

export function removeFirst<T>(arr: T[] | null | undefined, item: T): T[] {
  if (isEmpty(arr)) return [];
  const index = arr!.indexOf(item);
  if (index === -1) return [...arr!];
  return removeAt(arr, index);
}

export function removeAll<T>(arr: T[] | null | undefined, item: T): T[] {
  if (isEmpty(arr)) return [];
  return arr!.filter(i => i !== item);
}

export function removeWhere<T>(arr: T[] | null | undefined, predicate: (item: T, index: number) => boolean): T[] {
  return filterNot(arr, predicate);
}

export function updateAt<T>(arr: T[] | null | undefined, index: number, item: T): T[] {
  if (isEmpty(arr)) return [];
  const result = [...arr!];
  if (index >= 0 && index < result.length) {
    result[index] = item;
  }
  return result;
}

export function updateWhere<T>(arr: T[] | null | undefined, predicate: (item: T, index: number) => boolean, updater: (item: T) => T): T[] {
  if (isEmpty(arr)) return [];
  return arr!.map((item, index) => predicate(item, index) ? updater(item) : item);
}

export function append<T>(arr: T[] | null | undefined, item: T): T[] {
  if (isEmpty(arr)) return [item];
  return [...arr!, item];
}

export function prepend<T>(arr: T[] | null | undefined, item: T): T[] {
  if (isEmpty(arr)) return [item];
  return [item, ...arr!];
}

export function concat<T>(...arrays: (T[] | null | undefined)[]): T[] {
  const result: T[] = [];
  for (const arr of arrays) {
    if (arr) {
      result.push(...arr);
    }
  }
  return result;
}

// ============================================
// Comparison
// ============================================

export function equals<T>(arr1: T[] | null | undefined, arr2: T[] | null | undefined): boolean {
  if (arr1 === arr2) return true;
  if (arr1 === null || arr1 === undefined) return arr2 === null || arr2 === undefined;
  if (arr2 === null || arr2 === undefined) return false;
  if (arr1.length !== arr2.length) return false;
  for (let i = 0; i < arr1.length; i++) {
    if (arr1[i] !== arr2[i]) return false;
  }
  return true;
}

export function equalsIgnoreOrder<T>(arr1: T[] | null | undefined, arr2: T[] | null | undefined): boolean {
  if (arr1 === arr2) return true;
  if (arr1 === null || arr1 === undefined) return arr2 === null || arr2 === undefined;
  if (arr2 === null || arr2 === undefined) return false;
  if (arr1.length !== arr2.length) return false;
  const sorted1 = [...arr1].sort();
  const sorted2 = [...arr2].sort();
  return equals(sorted1, sorted2);
}

export function startsWith<T>(arr: T[] | null | undefined, prefix: T[]): boolean {
  if (isEmpty(arr) || isEmpty(prefix)) return false;
  if (prefix.length > arr!.length) return false;
  for (let i = 0; i < prefix.length; i++) {
    if (arr![i] !== prefix[i]) return false;
  }
  return true;
}

export function endsWith<T>(arr: T[] | null | undefined, suffix: T[]): boolean {
  if (isEmpty(arr) || isEmpty(suffix)) return false;
  if (suffix.length > arr!.length) return false;
  const offset = arr!.length - suffix.length;
  for (let i = 0; i < suffix.length; i++) {
    if (arr![offset + i] !== suffix[i]) return false;
  }
  return true;
}

// ============================================
// Range and Fill
// ============================================

export function range(start: number, end?: number, step: number = 1): number[] {
  if (end === undefined) {
    end = start;
    start = 0;
  }
  const result: number[] = [];
  if (step > 0) {
    for (let i = start; i < end; i += step) {
      result.push(i);
    }
  } else if (step < 0) {
    for (let i = start; i > end; i += step) {
      result.push(i);
    }
  }
  return result;
}

export function fill<T>(length: number, value: T): T[] {
  return Array(length).fill(value);
}

export function fillFn<T>(length: number, fn: (index: number) => T): T[] {
  const result: T[] = [];
  for (let i = 0; i < length; i++) {
    result.push(fn(i));
  }
  return result;
}

// ============================================
// Utility Functions
// ============================================

export function forEach<T>(arr: T[] | null | undefined, action: (item: T, index: number) => void): void {
  if (isEmpty(arr)) return;
  for (let i = 0; i < arr!.length; i++) {
    action(arr![i], i);
  }
}

export function forEachRight<T>(arr: T[] | null | undefined, action: (item: T, index: number) => void): void {
  if (isEmpty(arr)) return;
  for (let i = arr!.length - 1; i >= 0; i--) {
    action(arr![i], i);
  }
}

export function reduce<T, R>(arr: T[] | null | undefined, reducer: (acc: R, item: T, index: number) => R, initial: R): R {
  if (isEmpty(arr)) return initial;
  return arr!.reduce(reducer, initial);
}

export function reduceRight<T, R>(arr: T[] | null | undefined, reducer: (acc: R, item: T, index: number) => R, initial: R): R {
  if (isEmpty(arr)) return initial;
  return arr!.reduceRight(reducer, initial);
}

export function every<T>(arr: T[] | null | undefined, predicate: (item: T, index: number) => boolean): boolean {
  if (isEmpty(arr)) return true;
  return arr!.every(predicate);
}

export function some<T>(arr: T[] | null | undefined, predicate: (item: T, index: number) => boolean): boolean {
  if (isEmpty(arr)) return false;
  return arr!.some(predicate);
}

export function none<T>(arr: T[] | null | undefined, predicate: (item: T, index: number) => boolean): boolean {
  return !some(arr, predicate);
}

export function join<T>(arr: T[] | null | undefined, separator: string = ','): string {
  if (isEmpty(arr)) return '';
  return arr!.join(separator);
}

export function joinWith<T>(arr: T[] | null | undefined, separator: string, prefix: string = '', suffix: string = ''): string {
  if (isEmpty(arr)) return '';
  return prefix + arr!.join(separator) + suffix;
}

export function zip<T, U>(arr1: T[] | null | undefined, arr2: U[] | null | undefined): [T, U][] {
  if (isEmpty(arr1) || isEmpty(arr2)) return [];
  const length = Math.min(arr1!.length, arr2!.length);
  const result: [T, U][] = [];
  for (let i = 0; i < length; i++) {
    result.push([arr1![i], arr2![i]]);
  }
  return result;
}

export function zipWith<T, U, R>(arr1: T[] | null | undefined, arr2: U[] | null | undefined, fn: (a: T, b: U) => R): R[] {
  if (isEmpty(arr1) || isEmpty(arr2)) return [];
  const length = Math.min(arr1!.length, arr2!.length);
  const result: R[] = [];
  for (let i = 0; i < length; i++) {
    result.push(fn(arr1![i], arr2![i]));
  }
  return result;
}

export function unzip<T, U>(arr: [T, U][] | null | undefined): [T[], U[]] {
  if (isEmpty(arr)) return [[], []];
  const first: T[] = [];
  const second: U[] = [];
  for (const [a, b] of arr!) {
    first.push(a);
    second.push(b);
  }
  return [first, second];
}

export function rotate<T>(arr: T[] | null | undefined, positions: number): T[] {
  if (isEmpty(arr) || arr!.length <= 1) return isEmpty(arr) ? [] : [...arr!];
  const len = arr!.length;
  const normalizedPos = ((positions % len) + len) % len;
  return [...arr!.slice(normalizedPos), ...arr!.slice(0, normalizedPos)];
}

export function interleave<T>(arr1: T[] | null | undefined, arr2: T[] | null | undefined): T[] {
  if (isEmpty(arr1)) return isEmpty(arr2) ? [] : [...arr2!];
  if (isEmpty(arr2)) return [...arr1!];
  const result: T[] = [];
  const maxLen = Math.max(arr1!.length, arr2!.length);
  for (let i = 0; i < maxLen; i++) {
    if (i < arr1!.length) result.push(arr1![i]);
    if (i < arr2!.length) result.push(arr2![i]);
  }
  return result;
}

// ============================================
// ArrayUtils Class (Alternative API)
// ============================================

export class ArrayUtils {
  static isEmpty = isEmpty;
  static isNotEmpty = isNotEmpty;
  static size = size;
  static first = first;
  static last = last;
  static get = get;
  static getOrThrow = getOrThrow;
  static firstOrNull = firstOrNull;
  static lastOrNull = lastOrNull;
  static find = find;
  static findLast = findLast;
  static findIndex = findIndex;
  static findLastIndex = findLastIndex;
  static indexOf = indexOf;
  static lastIndexOf = lastIndexOf;
  static contains = contains;
  static containsAll = containsAll;
  static containsAny = containsAny;
  static filter = filter;
  static filterNot = filterNot;
  static reject = reject;
  static filterNull = filterNull;
  static map = map;
  static mapNotNull = mapNotNull;
  static flatMap = flatMap;
  static flatten = flatten;
  static flattenDeep = flattenDeep;
  static sort = sort;
  static sortBy = sortBy;
  static sortByDesc = sortByDesc;
  static reverse = reverse;
  static shuffle = shuffle;
  static isSorted = isSorted;
  static isSortedBy = isSortedBy;
  static unique = unique;
  static uniqueBy = uniqueBy;
  static union = union;
  static intersection = intersection;
  static difference = difference;
  static symmetricDifference = symmetricDifference;
  static duplicates = duplicates;
  static hasDuplicates = hasDuplicates;
  static groupBy = groupBy;
  static partition = partition;
  static chunk = chunk;
  static splitAt = splitAt;
  static take = take;
  static takeLast = takeLast;
  static takeWhile = takeWhile;
  static drop = drop;
  static dropLast = dropLast;
  static dropWhile = dropWhile;
  static slice = slice;
  static sum = sum;
  static sumBy = sumBy;
  static average = average;
  static averageBy = averageBy;
  static min = min;
  static max = max;
  static minBy = minBy;
  static maxBy = maxBy;
  static count = count;
  static countBy = countBy;
  static randomElement = randomElement;
  static randomElements = randomElements;
  static sample = sample;
  static insert = insert;
  static insertAll = insertAll;
  static removeAt = removeAt;
  static removeFirst = removeFirst;
  static removeAll = removeAll;
  static removeWhere = removeWhere;
  static updateAt = updateAt;
  static updateWhere = updateWhere;
  static append = append;
  static prepend = prepend;
  static concat = concat;
  static equals = equals;
  static equalsIgnoreOrder = equalsIgnoreOrder;
  static startsWith = startsWith;
  static endsWith = endsWith;
  static range = range;
  static fill = fill;
  static fillFn = fillFn;
  static forEach = forEach;
  static forEachRight = forEachRight;
  static reduce = reduce;
  static reduceRight = reduceRight;
  static every = every;
  static some = some;
  static none = none;
  static join = join;
  static joinWith = joinWith;
  static zip = zip;
  static zipWith = zipWith;
  static unzip = unzip;
  static rotate = rotate;
  static interleave = interleave;
}

export default ArrayUtils;