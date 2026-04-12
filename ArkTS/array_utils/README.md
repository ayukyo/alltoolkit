# Array Utilities for ArkTS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive array/collection manipulation utility module for ArkTS/HarmonyOS providing 100+ array operations with **zero dependencies**.

## Features

- ✅ **Empty/Blank Checks** - isEmpty, isNotEmpty, size
- ✅ **Safe Element Access** - first, last, get, getOrThrow, firstOrNull, lastOrNull
- ✅ **Filtering and Searching** - find, findIndex, contains, filter, filterNull
- ✅ **Transformation** - map, mapNotNull, flatMap, flatten, flattenDeep
- ✅ **Sorting and Ordering** - sort, sortBy, sortByDesc, reverse, shuffle
- ✅ **Set Operations** - unique, union, intersection, difference, duplicates
- ✅ **Grouping and Partitioning** - groupBy, partition, chunk, splitAt
- ✅ **Slicing and Taking** - take, takeLast, takeWhile, drop, dropWhile, slice
- ✅ **Aggregation** - sum, average, min, max, count, countBy
- ✅ **Random Operations** - randomElement, randomElements, sample
- ✅ **Immutable Modification** - insert, removeAt, append, prepend, concat
- ✅ **Comparison** - equals, equalsIgnoreOrder, startsWith, endsWith
- ✅ **Range and Fill** - range, fill, fillFn
- ✅ **Utility Functions** - forEach, reduce, every, some, join, zip, unzip

## Installation

```bash
# Copy the module to your HarmonyOS project
cp array_utils/mod.ets your-project/utils/array_utils/
```

## Usage

### Import

```typescript
import { 
  isEmpty, first, last, unique, groupBy, chunk, sum, 
  ArrayUtils 
} from './array_utils/mod';
```

### Empty/Blank Checks

```typescript
isEmpty(null)              // true
isEmpty([])                // true
isEmpty([1, 2, 3])         // false

isNotEmpty([1])            // true
size([1, 2, 3])            // 3
```

### Safe Element Access

```typescript
first([1, 2, 3])           // 1
last([1, 2, 3])            // 3

// Safe access with default
get([1, 2, 3], 10, 'default')  // 'default'
get([1, 2, 3], -1)             // 3 (negative index)

// Get or throw
getOrThrow([1, 2, 3], 0)       // 1
getOrThrow([1, 2, 3], 10)      // throws Error
```

### Filtering and Searching

```typescript
find([1, 2, 3, 4], x => x > 2)     // 3
findIndex([1, 2, 3], x => x === 2) // 1

contains([1, 2, 3], 2)             // true
containsAll([1, 2, 3], [1, 2])     // true

filter([1, 2, 3, 4], x => x > 2)   // [3, 4]
filterNot([1, 2, 3, 4], x => x > 2) // [1, 2]

// Filter out null/undefined
filterNull([1, null, 2, undefined, 3]) // [1, 2, 3]
```

### Transformation

```typescript
map([1, 2, 3], x => x * 2)           // [2, 4, 6]
mapNotNull([1, 2, 3], x => x > 1 ? x : null) // [2, 3]

flatMap([1, 2], x => [x, x * 2])     // [1, 2, 2, 4]
flatten([[1, 2], [3, 4]])            // [1, 2, 3, 4]
flattenDeep([1, [2, [3, [4]]]])      // [1, 2, 3, 4]
```

### Sorting

```typescript
sort([3, 1, 2])                      // [1, 2, 3]

// Sort by key
sortBy([{val: 3}, {val: 1}, {val: 2}], x => x.val)
// [{val: 1}, {val: 2}, {val: 3}]

sortByDesc([{val: 1}, {val: 3}], x => x.val) // [{val: 3}, {val: 1}]

reverse([1, 2, 3])                   // [3, 2, 1]
shuffle([1, 2, 3, 4, 5])             // randomized order

isSorted([1, 2, 3])                  // true
isSortedBy([{v: 1}, {v: 2}], x => x.v) // true
```

### Set Operations

```typescript
unique([1, 2, 2, 3, 3])              // [1, 2, 3]

uniqueBy([{id: 1}, {id: 2}, {id: 1}], x => x.id)
// [{id: 1}, {id: 2}]

union([1, 2], [2, 3])                // [1, 2, 3]
intersection([1, 2, 3], [2, 3, 4])    // [2, 3]
difference([1, 2, 3], [2, 3])        // [1]
symmetricDifference([1, 2], [2, 3])  // [1, 3]

duplicates([1, 2, 2, 3, 3])          // [2, 3]
hasDuplicates([1, 2, 2])             // true
```

### Grouping and Partitioning

```typescript
groupBy([{type: 'a', v: 1}, {type: 'b', v: 2}, {type: 'a', v: 3}], x => x.type)
// { a: [{type: 'a', v: 1}, {type: 'a', v: 3}], b: [{type: 'b', v: 2}] }

partition([1, 2, 3, 4], x => x > 2)  // [[3, 4], [1, 2]]

chunk([1, 2, 3, 4, 5], 2)            // [[1, 2], [3, 4], [5]]
splitAt([1, 2, 3, 4], 2)             // [[1, 2], [3, 4]]
```

### Slicing and Taking

```typescript
take([1, 2, 3, 4, 5], 2)             // [1, 2]
takeLast([1, 2, 3, 4, 5], 2)         // [4, 5]
takeWhile([1, 2, 3, 4, 5], x => x < 3) // [1, 2]

drop([1, 2, 3, 4, 5], 2)             // [3, 4, 5]
dropLast([1, 2, 3, 4, 5], 2)         // [1, 2, 3]
dropWhile([1, 2, 3, 4, 5], x => x < 3) // [3, 4, 5]

slice([1, 2, 3, 4], 1, 3)            // [2, 3]
```

### Aggregation

```typescript
sum([1, 2, 3])                       // 6
sumBy([{v: 1}, {v: 2}], x => x.v)    // 3

average([1, 2, 3])                   // 2
averageBy([{v: 1}, {v: 3}], x => x.v) // 2

min([3, 1, 2])                       // 1
max([1, 3, 2])                       // 3
minBy([{v: 3}, {v: 1}], x => x.v)    // {v: 1}
maxBy([{v: 1}, {v: 3}], x => x.v)    // {v: 3}

count([1, 2, 3, 4], x => x > 2)      // 2
countBy(['a', 'b', 'a', 'c'], x => x) // { a: 2, b: 1, c: 1 }
```

### Random Operations

```typescript
randomElement([1, 2, 3, 4, 5])       // random single element
randomElements([1, 2, 3, 4, 5], 3)   // 3 random elements
sample([1, 2, 3, 4, 5], 2)           // alias for randomElements
```

### Immutable Modification

```typescript
insert([1, 2, 3], 1, 5)              // [1, 5, 2, 3]
insertAll([1, 4], 1, [2, 3])         // [1, 2, 3, 4]

removeAt([1, 2, 3], 1)               // [1, 3]
removeFirst([1, 2, 3, 2], 2)         // [1, 3, 2]
removeAll([1, 2, 2, 3], 2)           // [1, 3]

updateAt([1, 2, 3], 1, 5)            // [1, 5, 3]
updateWhere([1, 2, 3], x => x > 1, x => x * 2) // [1, 4, 6]

append([1, 2], 3)                    // [1, 2, 3]
prepend([1, 2], 0)                   // [0, 1, 2]
concat([1, 2], [3, 4])               // [1, 2, 3, 4]
```

### Comparison

```typescript
equals([1, 2, 3], [1, 2, 3])         // true
equalsIgnoreOrder([1, 2, 3], [3, 2, 1]) // true

startsWith([1, 2, 3, 4], [1, 2])     // true
endsWith([1, 2, 3, 4], [3, 4])       // true
```

### Range and Fill

```typescript
range(5)                             // [0, 1, 2, 3, 4]
range(0, 5)                          // [0, 1, 2, 3, 4]
range(0, 10, 2)                      // [0, 2, 4, 6, 8]
range(5, 0, -1)                      // [5, 4, 3, 2, 1]

fill(3, 0)                           // [0, 0, 0]
fillFn(3, i => i)                    // [0, 1, 2]
fillFn(3, i => i * 2)                // [0, 2, 4]
```

### Utility Functions

```typescript
forEach([1, 2, 3], x => console.log(x))
forEachRight([1, 2, 3], x => console.log(x)) // reverse order

reduce([1, 2, 3], (a, b) => a + b, 0) // 6
every([1, 2, 3], x => x > 0)         // true
some([1, 2, 3], x => x > 2)          // true
none([1, 2, 3], x => x > 5)          // true

join([1, 2, 3], '-')                 // '1-2-3'
joinWith([1, 2, 3], '-', '[', ']')   // '[1-2-3]'

zip([1, 2], ['a', 'b'])              // [[1, 'a'], [2, 'b']]
zipWith([1, 2], [3, 4], (a, b) => a + b) // [4, 6]
unzip([[1, 'a'], [2, 'b']])          // [[1, 2], ['a', 'b']]

rotate([1, 2, 3, 4], 1)              // [2, 3, 4, 1]
interleave([1, 2, 3], ['a', 'b', 'c']) // [1, 'a', 2, 'b', 3, 'c']
```

### Class API (Alternative)

```typescript
import ArrayUtils from './array_utils/mod';

ArrayUtils.first([1, 2, 3])          // 1
ArrayUtils.unique([1, 2, 2, 3])      // [1, 2, 3]
ArrayUtils.groupBy([...], x => x.type)
```

## API Reference

| Function | Description |
|----------|-------------|
| `isEmpty(arr)` | Checks if array is null, undefined, or empty |
| `isNotEmpty(arr)` | Checks if array has elements |
| `size(arr)` | Returns array length |
| `first(arr)` | Returns first element or undefined |
| `last(arr)` | Returns last element or undefined |
| `get(arr, index, default?)` | Safe element access with negative index support |
| `getOrThrow(arr, index)` | Get element or throw if out of bounds |
| `find(arr, predicate)` | Find first matching element |
| `findIndex(arr, predicate)` | Find index of first match |
| `contains(arr, item)` | Check if item exists |
| `filter(arr, predicate)` | Filter elements |
| `filterNull(arr)` | Remove null/undefined elements |
| `map(arr, mapper)` | Transform elements |
| `mapNotNull(arr, mapper)` | Transform and filter null results |
| `flatMap(arr, mapper)` | Map and flatten |
| `flatten(arr)` | Flatten one level |
| `flattenDeep(arr)` | Flatten all levels |
| `sort(arr)` | Sort elements |
| `sortBy(arr, keyFn)` | Sort by key |
| `reverse(arr)` | Reverse array |
| `shuffle(arr)` | Randomize order |
| `unique(arr)` | Remove duplicates |
| `uniqueBy(arr, keyFn)` | Remove duplicates by key |
| `union(arr1, arr2)` | Combine arrays (unique) |
| `intersection(arr1, arr2)` | Common elements |
| `difference(arr1, arr2)` | Elements in first only |
| `groupBy(arr, keyFn)` | Group by key |
| `partition(arr, predicate)` | Split into two arrays |
| `chunk(arr, size)` | Split into chunks |
| `take(arr, n)` | Take first n elements |
| `takeWhile(arr, predicate)` | Take while predicate true |
| `drop(arr, n)` | Drop first n elements |
| `dropWhile(arr, predicate)` | Drop while predicate true |
| `sum(arr)` | Sum of numbers |
| `sumBy(arr, valueFn)` | Sum by key |
| `average(arr)` | Average of numbers |
| `min(arr)` | Minimum element |
| `max(arr)` | Maximum element |
| `minBy(arr, keyFn)` | Minimum by key |
| `maxBy(arr, keyFn)` | Maximum by key |
| `count(arr, predicate?)` | Count elements |
| `countBy(arr, keyFn)` | Count by key |
| `randomElement(arr)` | Get random element |
| `randomElements(arr, n)` | Get n random elements |
| `insert(arr, index, item)` | Insert at index |
| `removeAt(arr, index)` | Remove at index |
| `append(arr, item)` | Add to end |
| `prepend(arr, item)` | Add to beginning |
| `concat(...arrays)` | Combine arrays |
| `equals(arr1, arr2)` | Deep equality check |
| `equalsIgnoreOrder(arr1, arr2)` | Equality ignoring order |
| `range(start, end?, step?)` | Generate number range |
| `fill(length, value)` | Create filled array |
| `fillFn(length, fn)` | Create array with function |
| `zip(arr1, arr2)` | Combine arrays into pairs |
| `zipWith(arr1, arr2, fn)` | Combine with function |
| `unzip(arr)` | Split pairs into two arrays |
| `rotate(arr, positions)` | Rotate array |
| `interleave(arr1, arr2)` | Interleave elements |

## Testing

```bash
# Run tests
node --loader ts-node/esm array_utils_test.ets
```

## Test Coverage

- ✅ **130+ test cases**
- ✅ **100% function coverage**
- ✅ **Null/undefined handling**
- ✅ **Empty array handling**
- ✅ **Edge cases (negative indices, out of bounds)**
- ✅ **Immutability verification**

## License

MIT License - See [LICENSE](../../LICENSE)

## Contributing

Contributions are welcome! Please ensure:
- All functions are pure (no side effects)
- All operations are immutable
- 100% test coverage for new functions
- Zero external dependencies