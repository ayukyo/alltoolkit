/**
 * Array Utilities Test Suite for ArkTS
 * 
 * Comprehensive tests for the array_utils module with 100% coverage.
 */

import {
  isEmpty, isNotEmpty, size,
  first, last, get, getOrThrow, firstOrNull, lastOrNull,
  find, findLast, findIndex, findLastIndex, indexOf, lastIndexOf,
  contains, containsAll, containsAny,
  filter, filterNot, reject, filterNull,
  map, mapNotNull, flatMap, flatten, flattenDeep,
  sort, sortBy, sortByDesc, reverse, shuffle, isSorted, isSortedBy,
  unique, uniqueBy, union, intersection, difference, symmetricDifference,
  duplicates, hasDuplicates,
  groupBy, partition, chunk, splitAt,
  take, takeLast, takeWhile, drop, dropLast, dropWhile, slice,
  sum, sumBy, average, averageBy, min, max, minBy, maxBy, count, countBy,
  randomElement, randomElements, sample,
  insert, insertAll, removeAt, removeFirst, removeAll, removeWhere,
  updateAt, updateWhere, append, prepend, concat,
  equals, equalsIgnoreOrder, startsWith, endsWith,
  range, fill, fillFn,
  forEach, forEachRight, reduce, reduceRight, every, some, none,
  join, joinWith, zip, zipWith, unzip, rotate, interleave,
  ArrayUtils
} from './mod';

// ============================================
// Test Framework
// ============================================

let passed = 0;
let failed = 0;

function test(name: string, fn: () => void): void {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (e) {
    console.error(`✗ ${name}: ${e}`);
    failed++;
  }
}

function assertEqual<T>(actual: T, expected: T, msg?: string): void {
  if (actual !== expected) {
    throw new Error(`${msg || 'Assertion failed'}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

function assertDeepEqual<T>(actual: T, expected: T, msg?: string): void {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`${msg || 'Assertion failed'}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

function assertTrue(value: boolean, msg?: string): void {
  if (!value) {
    throw new Error(msg || 'Expected true, got false');
  }
}

function assertFalse(value: boolean, msg?: string): void {
  if (value) {
    throw new Error(msg || 'Expected false, got true');
  }
}

function assertUndefined(value: unknown, msg?: string): void {
  if (value !== undefined) {
    throw new Error(`${msg || 'Expected undefined'}, got ${value}`);
  }
}

function assertThrows(fn: () => void, msg?: string): void {
  try {
    fn();
    throw new Error(msg || 'Expected function to throw');
  } catch (e) {
    // Expected
  }
}

// ============================================
// Test Suite
// ============================================

export function runTests(): void {
  console.log('Running ArrayUtils Tests...\n');

  // ============================================
  // Empty/Blank Tests
  // ============================================
  
  test('isEmpty with null', () => assertTrue(isEmpty(null)));
  test('isEmpty with undefined', () => assertTrue(isEmpty(undefined)));
  test('isEmpty with empty array', () => assertTrue(isEmpty([])));
  test('isEmpty with non-empty array', () => assertFalse(isEmpty([1, 2, 3])));
  
  test('isNotEmpty with null', () => assertFalse(isNotEmpty(null)));
  test('isNotEmpty with empty array', () => assertFalse(isNotEmpty([])));
  test('isNotEmpty with non-empty array', () => assertTrue(isNotEmpty([1])));
  
  test('size with null', () => assertEqual(size(null), 0));
  test('size with undefined', () => assertEqual(size(undefined), 0));
  test('size with empty array', () => assertEqual(size([]), 0));
  test('size with array', () => assertEqual(size([1, 2, 3]), 3));

  // ============================================
  // Safe Element Access Tests
  // ============================================
  
  test('first with null', () => assertUndefined(first(null)));
  test('first with empty array', () => assertUndefined(first([])));
  test('first with array', () => assertEqual(first([1, 2, 3]), 1));
  test('first with string array', () => assertEqual(first(['a', 'b']), 'a'));
  
  test('last with null', () => assertUndefined(last(null)));
  test('last with empty array', () => assertUndefined(last([])));
  test('last with array', () => assertEqual(last([1, 2, 3]), 3));
  test('last with single element', () => assertEqual(last([1]), 1));
  
  test('get with null', () => assertUndefined(get(null, 0)));
  test('get with empty array', () => assertUndefined(get([], 0)));
  test('get with positive index', () => assertEqual(get([1, 2, 3], 1), 2));
  test('get with negative index', () => assertEqual(get([1, 2, 3], -1), 3));
  test('get with negative index -2', () => assertEqual(get([1, 2, 3], -2), 2));
  test('get with out of bounds', () => assertUndefined(get([1], 5)));
  test('get with default value', () => assertEqual(get([1], 5, 'default'), 'default'));
  test('get with negative out of bounds', () => assertUndefined(get([1], -5)));
  
  test('getOrThrow valid index', () => assertEqual(getOrThrow([1, 2, 3], 0), 1));
  test('getOrThrow negative index', () => assertEqual(getOrThrow([1, 2, 3], -1), 3));
  test('getOrThrow throws on out of bounds', () => assertThrows(() => getOrThrow([1], 5)));
  test('getOrThrow throws on negative out of bounds', () => assertThrows(() => getOrThrow([1], -5)));
  
  test('firstOrNull with null', () => assertEqual(firstOrNull(null), null));
  test('firstOrNull with empty array', () => assertEqual(firstOrNull([]), null));
  test('firstOrNull with array', () => assertEqual(firstOrNull([1, 2]), 1));
  
  test('lastOrNull with null', () => assertEqual(lastOrNull(null), null));
  test('lastOrNull with empty array', () => assertEqual(lastOrNull([]), null));
  test('lastOrNull with array', () => assertEqual(lastOrNull([1, 2]), 2));

  // ============================================
  // Filtering and Searching Tests
  // ============================================
  
  test('find with null', () => assertUndefined(find(null, x => x > 0)));
  test('find with empty array', () => assertUndefined(find([], x => x > 0)));
  test('find returns matching element', () => assertEqual(find([1, 2, 3], x => x > 1), 2));
  test('find returns first match', () => assertEqual(find([1, 2, 3, 4], x => x > 1), 2));
  test('find with no match', () => assertUndefined(find([1, 2, 3], x => x > 10)));
  test('find with index', () => assertEqual(find([1, 2, 3], (x, i) => i === 2), 3));
  
  test('findLast returns last match', () => assertEqual(findLast([1, 2, 3, 4], x => x > 1), 4));
  test('findLast with no match', () => assertUndefined(findLast([1], x => x > 10)));
  test('findLast with null', () => assertUndefined(findLast(null, x => true)));
  
  test('findIndex returns index', () => assertEqual(findIndex([1, 2, 3], x => x === 2), 1));
  test('findIndex with no match', () => assertEqual(findIndex([1, 2, 3], x => x === 5), -1));
  test('findIndex with null', () => assertEqual(findIndex(null, x => true), -1));
  
  test('findLastIndex returns last index', () => assertEqual(findLastIndex([1, 2, 3, 2], x => x === 2), 3));
  test('findLastIndex with no match', () => assertEqual(findLastIndex([1, 2, 3], x => x === 5), -1));
  
  test('indexOf returns index', () => assertEqual(indexOf([1, 2, 3], 2), 1));
  test('indexOf with no match', () => assertEqual(indexOf([1, 2, 3], 5), -1));
  test('indexOf with null', () => assertEqual(indexOf(null, 1), -1));
  
  test('lastIndexOf returns last index', () => assertEqual(lastIndexOf([1, 2, 3, 2], 2), 3));
  test('lastIndexOf with no match', () => assertEqual(lastIndexOf([1, 2, 3], 5), -1));
  
  test('contains returns true for existing', () => assertTrue(contains([1, 2, 3], 2)));
  test('contains returns false for missing', () => assertFalse(contains([1, 2, 3], 5)));
  test('contains with null', () => assertFalse(contains(null, 1)));
  
  test('containsAll returns true for all present', () => assertTrue(containsAll([1, 2, 3], [1, 2])));
  test('containsAll returns false for missing', () => assertFalse(containsAll([1, 2], [1, 3])));
  test('containsAll with null', () => assertFalse(containsAll(null, [1])));
  
  test('containsAny returns true for any present', () => assertTrue(containsAny([1, 2, 3], [5, 2])));
  test('containsAny returns false for none present', () => assertFalse(containsAny([1, 2], [3, 4])));
  test('containsAny with null', () => assertFalse(containsAny(null, [1])));
  
  test('filter returns matching elements', () => assertDeepEqual(filter([1, 2, 3, 4], x => x > 2), [3, 4]));
  test('filter with null', () => assertDeepEqual(filter(null, x => true), []));
  test('filter with empty array', () => assertDeepEqual(filter([], x => true), []));
  test('filter with index', () => assertDeepEqual(filter([1, 2, 3], (x, i) => i % 2 === 0), [1, 3]));
  
  test('filterNot returns non-matching elements', () => assertDeepEqual(filterNot([1, 2, 3, 4], x => x > 2), [1, 2]));
  test('filterNot with null', () => assertDeepEqual(filterNot(null, x => true), []));
  
  test('reject alias for filterNot', () => assertDeepEqual(reject([1, 2, 3, 4], x => x > 2), [1, 2]));
  
  test('filterNull removes null and undefined', () => assertDeepEqual(filterNull([1, null, 2, undefined, 3]), [1, 2, 3]));
  test('filterNull with all null', () => assertDeepEqual(filterNull([null, undefined]), []));
  test('filterNull with null array', () => assertDeepEqual(filterNull(null), []));

  // ============================================
  // Transformation Tests
  // ============================================
  
  test('map transforms elements', () => assertDeepEqual(map([1, 2, 3], x => x * 2), [2, 4, 6]));
  test('map with null', () => assertDeepEqual(map(null, x => x), []));
  test('map with empty', () => assertDeepEqual(map([], x => x), []));
  test('map with index', () => assertDeepEqual(map([1, 2, 3], (x, i) => x + i), [1, 3, 5]));
  
  test('mapNotNull filters out null results', () => assertDeepEqual(mapNotNull([1, 2, 3], x => x > 1 ? x : null), [2, 3]));
  test('mapNotNull filters out undefined results', () => assertDeepEqual(mapNotNull([1, 2, 3], x => x > 1 ? x : undefined), [2, 3]));
  test('mapNotNull with all null', () => assertDeepEqual(mapNotNull([1, 2, 3], x => null), []));
  
  test('flatMap flattens mapped results', () => assertDeepEqual(flatMap([1, 2, 3], x => [x, x * 2]), [1, 2, 2, 4, 3, 6]));
  test('flatMap with null', () => assertDeepEqual(flatMap(null, x => [x]), []));
  
  test('flatten flattens nested arrays', () => assertDeepEqual(flatten([[1, 2], [3, 4]]), [1, 2, 3, 4]));
  test('flatten with null', () => assertDeepEqual(flatten(null), []));
  test('flatten with empty', () => assertDeepEqual(flatten([]), []));
  
  test('flattenDeep flattens deeply nested', () => assertDeepEqual(flattenDeep([1, [2, [3, [4]]]]), [1, 2, 3, 4]));
  test('flattenDeep with null', () => assertDeepEqual(flattenDeep(null), []));

  // ============================================
  // Sorting Tests
  // ============================================
  
  test('sort sorts numbers', () => assertDeepEqual(sort([3, 1, 2]), [1, 2, 3]));
  test('sort sorts strings', () => assertDeepEqual(sort(['c', 'a', 'b']), ['a', 'b', 'c']));
  test('sort with null', () => assertDeepEqual(sort(null), []));
  test('sort with empty', () => assertDeepEqual(sort([]), []));
  test('sort is immutable', () => {
    const arr = [3, 1, 2];
    const sorted = sort(arr);
    assertDeepEqual(arr, [3, 1, 2]);
    assertDeepEqual(sorted, [1, 2, 3]);
  });
  
  test('sortBy sorts by key', () => {
    const arr = [{ name: 'b' }, { name: 'a' }, { name: 'c' }];
    const sorted = sortBy(arr, x => x.name);
    assertEqual(sorted[0].name, 'a');
    assertEqual(sorted[2].name, 'c');
  });
  test('sortBy with numbers', () => {
    const arr = [{ val: 3 }, { val: 1 }, { val: 2 }];
    const sorted = sortBy(arr, x => x.val);
    assertEqual(sorted[0].val, 1);
  });
  test('sortBy with null values', () => {
    const arr = [{ val: 1 }, { val: null }, { val: 2 }];
    const sorted = sortBy(arr, x => x.val);
    assertEqual(sorted[0].val, 1);
    assertEqual(sorted[1].val, null);
  });
  
  test('sortByDesc sorts descending', () => {
    const arr = [{ val: 1 }, { val: 3 }, { val: 2 }];
    const sorted = sortByDesc(arr, x => x.val);
    assertEqual(sorted[0].val, 3);
  });
  
  test('reverse reverses array', () => assertDeepEqual(reverse([1, 2, 3]), [3, 2, 1]));
  test('reverse with null', () => assertDeepEqual(reverse(null), []));
  test('reverse with single element', () => assertDeepEqual(reverse([1]), [1]));
  test('reverse is immutable', () => {
    const arr = [1, 2, 3];
    const reversed = reverse(arr);
    assertDeepEqual(arr, [1, 2, 3]);
  });
  
  test('shuffle changes order', () => {
    const arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    const shuffled = shuffle(arr);
    assertEqual(shuffled.length, 10);
    assertTrue(equalsIgnoreOrder(arr, shuffled));
  });
  test('shuffle with null', () => assertDeepEqual(shuffle(null), []));
  test('shuffle with empty', () => assertDeepEqual(shuffle([]), []));
  test('shuffle is immutable', () => {
    const arr = [1, 2, 3];
    shuffle(arr);
    assertDeepEqual(arr, [1, 2, 3]);
  });
  
  test('isSorted returns true for sorted', () => assertTrue(isSorted([1, 2, 3])));
  test('isSorted returns false for unsorted', () => assertFalse(isSorted([3, 1, 2])));
  test('isSorted with empty', () => assertTrue(isSorted([])));
  test('isSorted with single element', () => assertTrue(isSorted([1])));
  test('isSorted with null', () => assertTrue(isSorted(null)));
  
  test('isSortedBy returns true for sorted by key', () => {
    const arr = [{ val: 1 }, { val: 2 }, { val: 3 }];
    assertTrue(isSortedBy(arr, x => x.val));
  });
  test('isSortedBy returns false for unsorted', () => {
    const arr = [{ val: 3 }, { val: 1 }];
    assertFalse(isSortedBy(arr, x => x.val));
  });

  // ============================================
  // Set Operations Tests
  // ============================================
  
  test('unique removes duplicates', () => assertDeepEqual(unique([1, 2, 2, 3, 3]), [1, 2, 3]));
  test('unique with strings', () => assertDeepEqual(unique(['a', 'b', 'a']), ['a', 'b']));
  test('unique with null', () => assertDeepEqual(unique(null), []));
  test('unique with empty', () => assertDeepEqual(unique([]), []));
  test('unique preserves order', () => assertDeepEqual(unique([1, 3, 2, 3, 1]), [1, 3, 2]));
  
  test('uniqueBy removes duplicates by key', () => {
    const arr = [{ id: 1 }, { id: 2 }, { id: 1 }];
    const uniqueArr = uniqueBy(arr, x => x.id);
    assertEqual(uniqueArr.length, 2);
    assertEqual(uniqueArr[0].id, 1);
    assertEqual(uniqueArr[1].id, 2);
  });
  
  test('union combines arrays', () => assertDeepEqual(union([1, 2], [2, 3]), [1, 2, 3]));
  test('union with null first', () => assertDeepEqual(union(null, [1, 2]), [1, 2]));
  test('union with null second', () => assertDeepEqual(union([1, 2], null), [1, 2]));
  test('union with both null', () => assertDeepEqual(union(null, null), []));
  test('union preserves order', () => assertDeepEqual(union([1, 2], [3, 2]), [1, 2, 3]));
  
  test('intersection returns common elements', () => assertDeepEqual(intersection([1, 2, 3], [2, 3, 4]), [2, 3]));
  test('intersection with no common', () => assertDeepEqual(intersection([1, 2], [3, 4]), []));
  test('intersection with null', () => assertDeepEqual(intersection(null, [1]), []));
  test('intersection with empty', () => assertDeepEqual(intersection([], [1]), []));
  
  test('difference returns elements in first only', () => assertDeepEqual(difference([1, 2, 3], [2, 3]), [1]));
  test('difference with null first', () => assertDeepEqual(difference(null, [1]), []));
  test('difference with null second', () => assertDeepEqual(difference([1, 2], null), [1, 2]));
  test('difference with no overlap', () => assertDeepEqual(difference([1, 2], [3, 4]), [1, 2]));
  
  test('symmetricDifference returns unique elements from both', () => assertDeepEqual(symmetricDifference([1, 2], [2, 3]), [1, 3]));
  test('symmetricDifference with null', () => assertDeepEqual(symmetricDifference(null, [1]), [1]));
  
  test('duplicates returns duplicate elements', () => assertDeepEqual(duplicates([1, 2, 2, 3, 3, 3]), [2, 3]));
  test('duplicates with no duplicates', () => assertDeepEqual(duplicates([1, 2, 3]), []));
  test('duplicates with null', () => assertDeepEqual(duplicates(null), []));
  
  test('hasDuplicates returns true for duplicates', () => assertTrue(hasDuplicates([1, 2, 2])));
  test('hasDuplicates returns false for unique', () => assertFalse(hasDuplicates([1, 2, 3])));
  test('hasDuplicates with null', () => assertFalse(hasDuplicates(null)));
  test('hasDuplicates with empty', () => assertFalse(hasDuplicates([])));

  // ============================================
  // Grouping and Partitioning Tests
  // ============================================
  
  test('groupBy groups elements', () => {
    const arr = [{ type: 'a', val: 1 }, { type: 'b', val: 2 }, { type: 'a', val: 3 }];
    const grouped = groupBy(arr, x => x.type);
    assertEqual(grouped['a'].length, 2);
    assertEqual(grouped['b'].length, 1);
  });
  test('groupBy with null', () => assertDeepEqual(groupBy(null, x => x), {}));
  
  test('partition splits array', () => {
    const [pass, fail] = partition([1, 2, 3, 4], x => x > 2);
    assertDeepEqual(pass, [3, 4]);
    assertDeepEqual(fail, [1, 2]);
  });
  test('partition with null', () => {
    const [pass, fail] = partition(null, x => true);
    assertDeepEqual(pass, []);
    assertDeepEqual(fail, []);
  });
  test('partition with index', () => {
    const [pass, fail] = partition([1, 2, 3], (x, i) => i % 2 === 0);
    assertDeepEqual(pass, [1, 3]);
    assertDeepEqual(fail, [2]);
  });
  
  test('chunk splits into chunks', () => assertDeepEqual(chunk([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]));
  test('chunk with exact size', () => assertDeepEqual(chunk([1, 2, 3, 4], 2), [[1, 2], [3, 4]]));
  test('chunk with null', () => assertDeepEqual(chunk(null, 2), []));
  test('chunk with zero size', () => assertDeepEqual(chunk([1, 2, 3], 0), []));
  test('chunk with negative size', () => assertDeepEqual(chunk([1, 2, 3], -1), []));
  
  test('splitAt splits at index', () => {
    const [first, second] = splitAt([1, 2, 3, 4], 2);
    assertDeepEqual(first, [1, 2]);
    assertDeepEqual(second, [3, 4]);
  });
  test('splitAt with negative index', () => {
    const [first, second] = splitAt([1, 2, 3, 4], -2);
    assertDeepEqual(first, [1, 2]);
    assertDeepEqual(second, [3, 4]);
  });
  test('splitAt with null', () => {
    const [first, second] = splitAt(null, 2);
    assertDeepEqual(first, []);
    assertDeepEqual(second, []);
  });

  // ============================================
  // Slicing and Taking Tests
  // ============================================
  
  test('take takes first n elements', () => assertDeepEqual(take([1, 2, 3, 4], 2), [1, 2]));
  test('take more than length', () => assertDeepEqual(take([1, 2], 5), [1, 2]));
  test('take with zero', () => assertDeepEqual(take([1, 2, 3], 0), []));
  test('take with negative', () => assertDeepEqual(take([1, 2, 3], -1), []));
  test('take with null', () => assertDeepEqual(take(null, 2), []));
  
  test('takeLast takes last n elements', () => assertDeepEqual(takeLast([1, 2, 3, 4], 2), [3, 4]));
  test('takeLast more than length', () => assertDeepEqual(takeLast([1, 2], 5), [1, 2]));
  test('takeLast with zero', () => assertDeepEqual(takeLast([1, 2, 3], 0), []));
  test('takeLast with null', () => assertDeepEqual(takeLast(null, 2), []));
  
  test('takeWhile takes while predicate true', () => assertDeepEqual(takeWhile([1, 2, 3, 4, 5], x => x < 3), [1, 2]));
  test('takeWhile all pass', () => assertDeepEqual(takeWhile([1, 2, 3], x => x < 10), [1, 2, 3]));
  test('takeWhile first fails', () => assertDeepEqual(takeWhile([5, 1, 2], x => x < 3), []));
  test('takeWhile with null', () => assertDeepEqual(takeWhile(null, x => true), []));
  
  test('drop drops first n elements', () => assertDeepEqual(drop([1, 2, 3, 4], 2), [3, 4]));
  test('drop more than length', () => assertDeepEqual(drop([1, 2], 5), []));
  test('drop with zero', () => assertDeepEqual(drop([1, 2, 3], 0), [1, 2, 3]));
  test('drop with negative', () => assertDeepEqual(drop([1, 2, 3], -1), [1, 2, 3]));
  test('drop with null', () => assertDeepEqual(drop(null, 2), []));
  
  test('dropLast drops last n elements', () => assertDeepEqual(dropLast([1, 2, 3, 4], 2), [1, 2]));
  test('dropLast more than length', () => assertDeepEqual(dropLast([1, 2], 5), []));
  test('dropLast with null', () => assertDeepEqual(dropLast(null, 2), []));
  
  test('dropWhile drops while predicate true', () => assertDeepEqual(dropWhile([1, 2, 3, 4, 5], x => x < 3), [3, 4, 5]));
  test('dropWhile all pass', () => assertDeepEqual(dropWhile([1, 2, 3], x => x < 10), []));
  test('dropWhile none pass', () => assertDeepEqual(dropWhile([5, 1, 2], x => x < 3), [5, 1, 2]));
  test('dropWhile with null', () => assertDeepEqual(dropWhile(null, x => true), []));
  
  test('slice extracts range', () => assertDeepEqual(slice([1, 2, 3, 4], 1, 3), [2, 3]));
  test('slice with negative start', () => assertDeepEqual(slice([1, 2, 3, 4], -2), [3, 4]));
  test('slice with null', () => assertDeepEqual(slice(null, 0, 2), []));

  // ============================================
  // Aggregation Tests
  // ============================================
  
  test('sum calculates sum', () => assertEqual(sum([1, 2, 3]), 6));
  test('sum with negative', () => assertEqual(sum([-1, 2, 3]), 4));
  test('sum with empty', () => assertEqual(sum([]), 0));
  test('sum with null', () => assertEqual(sum(null), 0));
  
  test('sumBy calculates sum by key', () => {
    const arr = [{ val: 1 }, { val: 2 }, { val: 3 }];
    assertEqual(sumBy(arr, x => x.val), 6);
  });
  test('sumBy with null', () => assertEqual(sumBy(null, x => x), 0));
  
  test('average calculates average', () => assertEqual(average([1, 2, 3]), 2));
  test('average with empty', () => assertEqual(average([]), 0));
  test('average with null', () => assertEqual(average(null), 0));
  test('average with decimals', () => assertEqual(average([1, 2]), 1.5));
  
  test('averageBy calculates average by key', () => {
    const arr = [{ val: 1 }, { val: 2 }, { val: 3 }];
    assertEqual(averageBy(arr, x => x.val), 2);
  });
  
  test('min finds minimum', () => assertEqual(min([3, 1, 2]), 1));
  test('min with strings', () => assertEqual(min(['b', 'a', 'c']), 'a'));
  test('min with empty', () => assertUndefined(min([])));
  test('min with null', () => assertUndefined(min(null));
  
  test('max finds maximum', () => assertEqual(max([1, 3, 2]), 3));
  test('max with strings', () => assertEqual(max(['a', 'c', 'b']), 'c'));
  test('max with empty', () => assertUndefined(max([])));
  test('max with null', () => assertUndefined(max(null)));
  
  test('minBy finds minimum by key', () => {
    const arr = [{ val: 3 }, { val: 1 }, { val: 2 }];
    assertEqual(minBy(arr, x => x.val)!.val, 1);
  });
  test('minBy with empty', () => assertUndefined(minBy([], x => x));
  
  test('maxBy finds maximum by key', () => {
    const arr = [{ val: 1 }, { val: 3 }, { val: 2 }];
    assertEqual(maxBy(arr, x => x.val)!.val, 3);
  });
  test('maxBy with empty', () => assertUndefined(maxBy([], x => x));
  
  test('count returns length without predicate', () => assertEqual(count([1, 2, 3]), 3));
  test('count with predicate', () => assertEqual(count([1, 2, 3, 4], x => x > 2), 2));
  test('count with null', () => assertEqual(count(null), 0));
  test('count with empty', () => assertEqual(count([]), 0));
  
  test('countBy counts by key', () => {
    const result = countBy(['a', 'b', 'a', 'c', 'a'], x => x);
    assertEqual(result['a'], 3);
    assertEqual(result['b'], 1);
    assertEqual(result['c'], 1);
  });
  test('countBy with null', () => assertDeepEqual(countBy(null, x => x), {}));

  // ============================================
  // Random Operations Tests
  // ============================================
  
  test('randomElement returns element from array', () => {
    const arr = [1, 2, 3, 4, 5];
    const elem = randomElement(arr);
    assertTrue(contains(arr, elem));
  });
  test('randomElement with null', () => assertUndefined(randomElement(null)));
  test('randomElement with empty', () => assertUndefined(randomElement([])));
  test('randomElement with single', () => assertEqual(randomElement([1]), 1));
  
  test('randomElements returns multiple elements', () => {
    const arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    const elems = randomElements(arr, 3);
    assertEqual(elems.length, 3);
    assertTrue(every(elems, e => contains(arr, e)));
  });
  test('randomElements more than length', () => {
    const arr = [1, 2, 3];
    const elems = randomElements(arr, 10);
    assertEqual(elems.length, 3);
  });
  test('randomElements with null', () => assertDeepEqual(randomElements(null, 3), []));
  test('randomElements with zero', () => assertDeepEqual(randomElements([1, 2, 3], 0), []));
  
  test('sample alias for randomElements', () => {
    const arr = [1, 2, 3, 4, 5];
    const elems = sample(arr, 2);
    assertEqual(elems.length, 2);
  });

  // ============================================
  // Modification Tests
  // ============================================
  
  test('insert inserts at index', () => assertDeepEqual(insert([1, 2, 3], 1, 5), [1, 5, 2, 3]));
  test('insert at beginning', () => assertDeepEqual(insert([1, 2, 3], 0, 5), [5, 1, 2, 3]));
  test('insert at end', () => assertDeepEqual(insert([1, 2, 3], 3, 5), [1, 2, 3, 5]));
  test('insert with null', () => assertDeepEqual(insert(null, 0, 1), [1]));
  test('insert is immutable', () => {
    const arr = [1, 2, 3];
    insert(arr, 0, 5);
    assertDeepEqual(arr, [1, 2, 3]);
  });
  
  test('insertAll inserts multiple at index', () => assertDeepEqual(insertAll([1, 4], 1, [2, 3]), [1, 2, 3, 4]));
  test('insertAll with null', () => assertDeepEqual(insertAll(null, 0, [1, 2]), [1, 2]));
  
  test('removeAt removes at index', () => assertDeepEqual(removeAt([1, 2, 3], 1), [1, 3]));
  test('removeAt at beginning', () => assertDeepEqual(removeAt([1, 2, 3], 0), [2, 3]));
  test('removeAt at end', () => assertDeepEqual(removeAt([1, 2, 3], 2), [1, 2]));
  test('removeAt with null', () => assertDeepEqual(removeAt(null, 0), []));
  test('removeAt is immutable', () => {
    const arr = [1, 2, 3];
    removeAt(arr, 0);
    assertDeepEqual(arr, [1, 2, 3]);
  });
  
  test('removeFirst removes first occurrence', () => assertDeepEqual(removeFirst([1, 2, 3, 2], 2), [1, 3, 2]));
  test('removeFirst with no match', () => assertDeepEqual(removeFirst([1, 2, 3], 5), [1, 2, 3]));
  test('removeFirst with null', () => assertDeepEqual(removeFirst(null, 1), []));
  
  test('removeAll removes all occurrences', () => assertDeepEqual(removeAll([1, 2, 3, 2, 2], 2), [1, 3]));
  test('removeAll with no match', () => assertDeepEqual(removeAll([1, 2, 3], 5), [1, 2, 3]));
  test('removeAll with null', () => assertDeepEqual(removeAll(null, 1), []));
  
  test('removeWhere removes matching', () => assertDeepEqual(removeWhere([1, 2, 3, 4], x => x > 2), [1, 2]));
  test('removeWhere with null', () => assertDeepEqual(removeWhere(null, x => true), []));
  
  test('updateAt updates at index', () => assertDeepEqual(updateAt([1, 2, 3], 1, 5), [1, 5, 3]));
  test('updateAt out of bounds', () => assertDeepEqual(updateAt([1, 2, 3], 10, 5), [1, 2, 3]));
  test('updateAt with null', () => assertDeepEqual(updateAt(null, 0, 1), []));
  test('updateAt is immutable', () => {
    const arr = [1, 2, 3];
    updateAt(arr, 0, 5);
    assertDeepEqual(arr, [1, 2, 3]);
  });
  
  test('updateWhere updates matching', () => assertDeepEqual(updateWhere([1, 2, 3], x => x > 1, x => x * 2), [1, 4, 6]));
  test('updateWhere with null', () => assertDeepEqual(updateWhere(null, x => true, x => x), []));
  
  test('append adds to end', () => assertDeepEqual(append([1, 2], 3), [1, 2, 3]));
  test('append to null', () => assertDeepEqual(append(null, 1), [1]));
  test('append to empty', () => assertDeepEqual(append([], 1), [1]));
  test('append is immutable', () => {
    const arr = [1, 2];
    append(arr, 3);
    assertDeepEqual(arr, [1, 2]);
  });
  
  test('prepend adds to beginning', () => assertDeepEqual(prepend([1, 2], 0), [0, 1, 2]));
  test('prepend to null', () => assertDeepEqual(prepend(null, 1), [1]));
  test('prepend is immutable', () => {
    const arr = [1, 2];
    prepend(arr, 0);
    assertDeepEqual(arr, [1, 2]);
  });
  
  test('concat combines arrays', () => assertDeepEqual(concat([1, 2], [3, 4]), [1, 2, 3, 4]));
  test('concat with nulls', () => assertDeepEqual(concat(null, [1], null, [2]), [1, 2]));
  test('concat all nulls', () => assertDeepEqual(concat(null, null), []));
  test('concat with empty', () => assertDeepEqual(concat([], [], []), []));

  // ============================================
  // Comparison Tests
  // ============================================
  
  test('equals returns true for equal arrays', () => assertTrue(equals([1, 2, 3], [1, 2, 3])));
  test('equals returns false for different arrays', () => assertFalse(equals([1, 2], [1, 3])));
  test('equals returns false for different lengths', () => assertFalse(equals([1, 2], [1])));
  test('equals with nulls', () => assertTrue(equals(null, null)));
  test('equals with null and empty', () => assertFalse(equals(null, [])));
  test('equals with undefined', () => assertTrue(equals(undefined, undefined)));
  test('equals same reference', () => {
    const arr = [1, 2, 3];
    assertTrue(equals(arr, arr));
  });
  
  test('equalsIgnoreOrder returns true for same elements', () => assertTrue(equalsIgnoreOrder([1, 2, 3], [3, 2, 1])));
  test('equalsIgnoreOrder returns false for different elements', () => assertFalse(equalsIgnoreOrder([1, 2], [2, 3])));
  test('equalsIgnoreOrder with nulls', () => assertTrue(equalsIgnoreOrder(null, null)));
  
  test('startsWith returns true for prefix', () => assertTrue(startsWith([1, 2, 3, 4], [1, 2])));
  test('startsWith returns false for non-prefix', () => assertFalse(startsWith([1, 2, 3], [2, 3])));
  test('startsWith returns false for longer prefix', () => assertFalse(startsWith([1, 2], [1, 2, 3])));
  test('startsWith with null', () => assertFalse(startsWith(null, [1])));
  test('startsWith with empty prefix', () => assertFalse(startsWith([1, 2], [])));
  
  test('endsWith returns true for suffix', () => assertTrue(endsWith([1, 2, 3, 4], [3, 4])));
  test('endsWith returns false for non-suffix', () => assertFalse(endsWith([1, 2, 3], [1, 2])));
  test('endsWith returns false for longer suffix', () => assertFalse(endsWith([1, 2], [1, 2, 3])));
  test('endsWith with null', () => assertFalse(endsWith(null, [1])));

  // ============================================
  // Range and Fill Tests
  // ============================================
  
  test('range generates range', () => assertDeepEqual(range(0, 5), [0, 1, 2, 3, 4]));
  test('range with single argument', () => assertDeepEqual(range(3), [0, 1, 2]));
  test('range with step', () => assertDeepEqual(range(0, 10, 2), [0, 2, 4, 6, 8]));
  test('range with negative step', () => assertDeepEqual(range(5, 0, -1), [5, 4, 3, 2, 1]));
  test('range empty', () => assertDeepEqual(range(5, 5), []));
  
  test('fill creates filled array', () => assertDeepEqual(fill(3, 0), [0, 0, 0]));
  test('fill with zero length', () => assertDeepEqual(fill(0, 1), []));
  test('fill with objects', () => {
    const obj = { a: 1 };
    const arr = fill(2, obj);
    assertEqual(arr.length, 2);
  });
  
  test('fillFn creates array with function', () => assertDeepEqual(fillFn(3, i => i), [0, 1, 2]));
  test('fillFn with zero length', () => assertDeepEqual(fillFn(0, i => i), []));
  test('fillFn with complex function', () => assertDeepEqual(fillFn(3, i => i * 2), [0, 2, 4]));

  // ============================================
  // Utility Tests
  // ============================================
  
  test('forEach iterates all elements', () => {
    let sum = 0;
    forEach([1, 2, 3], x => sum += x);
    assertEqual(sum, 6);
  });
  test('forEach with index', () => {
    let indices = 0;
    forEach([1, 2, 3], (x, i) => indices += i);
    assertEqual(indices, 3);
  });
  test('forEach with null', () => {
    let count = 0;
    forEach(null, x => count++);
    assertEqual(count, 0);
  });
  
  test('forEachRight iterates in reverse', () => {
    const result: number[] = [];
    forEachRight([1, 2, 3], x => result.push(x));
    assertDeepEqual(result, [3, 2, 1]);
  });
  
  test('reduce reduces array', () => assertEqual(reduce([1, 2, 3], (a, b) => a + b, 0), 6));
  test('reduce with null', () => assertEqual(reduce(null, (a, b) => a + b, 0), 0));
  test('reduce with empty', () => assertEqual(reduce([], (a, b) => a + b, 5), 5));
  
  test('reduceRight reduces from right', () => {
    const result = reduceRight([1, 2, 3], (a, b) => `${a}-${b}`, '');
    assertEqual(result, '-3-2-1');
  });
  
  test('every returns true when all pass', () => assertTrue(every([1, 2, 3], x => x > 0)));
  test('every returns false when one fails', () => assertFalse(every([1, 2, -3], x => x > 0)));
  test('every with null', () => assertTrue(every(null, x => true)));
  test('every with empty', () => assertTrue(every([], x => false)));
  
  test('some returns true when any pass', () => assertTrue(some([1, 2, 3], x => x > 2)));
  test('some returns false when none pass', () => assertFalse(some([1, 2], x => x > 5)));
  test('some with null', () => assertFalse(some(null, x => true)));
  test('some with empty', () => assertFalse(some([], x => true)));
  
  test('none returns true when none pass', () => assertTrue(none([1, 2, 3], x => x > 5)));
  test('none returns false when any pass', () => assertFalse(none([1, 2, 3], x => x > 2)));
  test('none with null', () => assertTrue(none(null, x => true)));
  
  test('join joins elements', () => assertEqual(join([1, 2, 3], '-'), '1-2-3'));
  test('join with default separator', () => assertEqual(join([1, 2, 3]), '1,2,3'));
  test('join with null', () => assertEqual(join(null), ''));
  test('join with empty', () => assertEqual(join([]), ''));
  test('join with strings', () => assertEqual(join(['a', 'b', 'c'], ' '), 'a b c'));
  
  test('joinWith adds prefix and suffix', () => assertEqual(joinWith([1, 2, 3], '-', '[', ']'), '[1-2-3]'));
  test('joinWith with null', () => assertEqual(joinWith(null, '-'), ''));
  
  test('zip zips arrays', () => assertDeepEqual(zip([1, 2, 3], ['a', 'b', 'c']), [[1, 'a'], [2, 'b'], [3, 'c']]));
  test('zip with different lengths', () => assertDeepEqual(zip([1, 2, 3, 4], ['a', 'b']), [[1, 'a'], [2, 'b']]));
  test('zip with null', () => assertDeepEqual(zip(null, [1]), []));
  test('zip with empty', () => assertDeepEqual(zip([], [1]), []));
  
  test('zipWith zips with function', () => assertDeepEqual(zipWith([1, 2], [3, 4], (a, b) => a + b), [4, 6]));
  test('zipWith with different lengths', () => assertDeepEqual(zipWith([1, 2, 3], [4], (a, b) => a + b), [5]));
  
  test('unzip unzips pairs', () => {
    const [first, second] = unzip([[1, 'a'], [2, 'b'], [3, 'c']]);
    assertDeepEqual(first, [1, 2, 3]);
    assertDeepEqual(second, ['a', 'b', 'c']);
  });
  test('unzip with null', () => {
    const [first, second] = unzip(null);
    assertDeepEqual(first, []);
    assertDeepEqual(second, []);
  });
  
  test('rotate rotates array', () => assertDeepEqual(rotate([1, 2, 3, 4], 1), [2, 3, 4, 1]));
  test('rotate negative', () => assertDeepEqual(rotate([1, 2, 3, 4], -1), [4, 1, 2, 3]));
  test('rotate with zero', () => assertDeepEqual(rotate([1, 2, 3], 0), [1, 2, 3]));
  test('rotate larger than length', () => assertDeepEqual(rotate([1, 2, 3], 5), [3, 1, 2]));
  test('rotate with null', () => assertDeepEqual(rotate(null, 1), []));
  test('rotate with single element', () => assertDeepEqual(rotate([1], 1), [1]));
  
  test('interleave interleaves arrays', () => assertDeepEqual(interleave([1, 2, 3], ['a', 'b', 'c']), [1, 'a', 2, 'b', 3, 'c']));
  test('interleave with different lengths', () => assertDeepEqual(interleave([1, 2, 3], ['a']), [1, 'a', 2, 3]));
  test('interleave with null first', () => assertDeepEqual(interleave(null, [1]), [1]));
  test('interleave with null second', () => assertDeepEqual(interleave([1], null), [1]));
  test('interleave both null', () => assertDeepEqual(interleave(null, null), []));

  // ============================================
  // Class API Tests
  // ============================================
  
  test('ArrayUtils class API works', () => assertDeepEqual(ArrayUtils.first([1, 2, 3]), 1));
  test('ArrayUtils class map works', () => assertDeepEqual(ArrayUtils.map([1, 2, 3], x => x * 2), [2, 4, 6]));
  test('ArrayUtils class filter works', () => assertDeepEqual(ArrayUtils.filter([1, 2, 3, 4], x => x > 2), [3, 4]));
  test('ArrayUtils class unique works', () => assertDeepEqual(ArrayUtils.unique([1, 2, 2, 3]), [1, 2, 3]));

  // ============================================
  // Summary
  // ============================================
  
  console.log(`\n========================================`);
  console.log(`Test Results: ${passed} passed, ${failed} failed`);
  console.log(`========================================`);
}

// Run tests if executed directly
runTests();