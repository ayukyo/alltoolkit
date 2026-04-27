{*******************************************************************************
  AllToolkit - Delphi Array Utilities Example
  
  演示数组工具库的使用方法
********************************************************************************}

program array_utils_example;

{$APPTYPE CONSOLE}

uses
  SysUtils, Classes, mod;

var
  IntArr, ResultArr: TIntArray;
  StrArr, ResultStrArr: TStringArray;
  DblArr: TDoubleArray;
  MinVal, MaxVal: Integer;
  MinDbl, MaxDbl: Double;
  Chunks: array of TIntArray;
  I: Integer;

begin
  WriteLn('');
  WriteLn('========================================');
  WriteLn('AllToolkit - Delphi Array Utilities');
  WriteLn('========================================');
  WriteLn('');
  
  // ============================================
  // 1. Integer Array Basic Operations
  // ============================================
  WriteLn('--- 1. Integer Array Basic Operations ---');
  WriteLn('');
  
  // Create array
  IntArr := IntArrayCreate([10, 20, 30, 40, 50]);
  WriteLn('Create array: [', IntArrayToString(IntArr), ']');
  WriteLn('Length: ', IntArrayLength(IntArr));
  
  // Add and insert
  IntArrayAdd(IntArr, 60);
  WriteLn('After Add(60): [', IntArrayToString(IntArr), ']');
  
  IntArrayInsert(IntArr, 0, 5);
  WriteLn('After Insert(0, 5): [', IntArrayToString(IntArr), ']');
  
  // Delete
  IntArrayDelete(IntArr, 0);
  WriteLn('After Delete(0): [', IntArrayToString(IntArr), ']');
  
  // Get and Set
  WriteLn('Get(2): ', IntArrayGet(IntArr, 2));
  IntArraySet(IntArr, 2, 35);
  WriteLn('After Set(2, 35): Get(2) = ', IntArrayGet(IntArr, 2));
  
  WriteLn('');
  
  // ============================================
  // 2. Search Operations
  // ============================================
  WriteLn('--- 2. Search Operations ---');
  WriteLn('');
  
  IntArr := IntArrayCreate([10, 20, 30, 20, 40, 20, 50]);
  WriteLn('Array: [', IntArrayToString(IntArr), ']');
  
  WriteLn('IndexOf(20): ', IntArrayIndexOf(IntArr, 20));
  WriteLn('LastIndexOf(20): ', IntArrayLastIndexOf(IntArr, 20));
  WriteLn('Contains(30): ', IntArrayContains(IntArr, 30));
  WriteLn('Contains(99): ', IntArrayContains(IntArr, 99));
  WriteLn('Count(20): ', IntArrayCount(IntArr, 20));
  
  WriteLn('');
  
  // ============================================
  // 3. Sorting Algorithms
  // ============================================
  WriteLn('--- 3. Sorting Algorithms ---');
  WriteLn('');
  
  IntArr := IntArrayCreate([5, 3, 8, 1, 9, 2, 7, 4, 6]);
  WriteLn('Original: [', IntArrayToString(IntArr), ']');
  
  WriteLn('Bubble Sort:  [', IntArrayToString(IntArraySortBubble(IntArr)), ']');
  WriteLn('Quick Sort:   [', IntArrayToString(IntArraySortQuick(IntArr)), ']');
  WriteLn('Merge Sort:   [', IntArrayToString(IntArraySortMerge(IntArr)), ']');
  WriteLn('Selection:    [', IntArrayToString(IntArraySortSelection(IntArr)), ']');
  WriteLn('Insertion:    [', IntArrayToString(IntArraySortInsertion(IntArr)), ']');
  
  WriteLn('');
  
  // ============================================
  // 4. Statistics
  // ============================================
  WriteLn('--- 4. Statistics ---');
  WriteLn('');
  
  IntArr := IntArrayCreate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
  WriteLn('Array: [', IntArrayToString(IntArr), ']');
  
  WriteLn('Sum:      ', IntArraySum(IntArr));
  WriteLn('Average:  ', IntArrayAverage(IntArr):0:2);
  WriteLn('Min:      ', IntArrayMin(IntArr));
  WriteLn('Max:      ', IntArrayMax(IntArr));
  WriteLn('Range:    ', IntArrayRange(IntArr));
  WriteLn('Median:   ', IntArrayMedian(IntArr):0:2);
  
  IntArr := IntArrayCreate([1, 2, 2, 3, 3, 3, 4]);
  WriteLn('Array for Mode: [', IntArrayToString(IntArr), ']');
  WriteLn('Mode:     ', IntArrayMode(IntArr));
  
  WriteLn('');
  
  // ============================================
  // 5. Double Array Statistics
  // ============================================
  WriteLn('--- 5. Double Array Statistics ---');
  WriteLn('');
  
  DblArr := DblArrayCreate([1.5, 2.5, 3.5, 4.5, 5.5]);
  WriteLn('Double array created');
  
  WriteLn('Sum:      ', DblArraySum(DblArr):0:2);
  WriteLn('Average:  ', DblArrayAverage(DblArr):0:2);
  WriteLn('Min:      ', DblArrayMin(DblArr):0:2);
  WriteLn('Max:      ', DblArrayMax(DblArr):0:2);
  WriteLn('StdDev:   ', DblArrayStdDev(DblArr):0:4);
  WriteLn('Variance: ', DblArrayVariance(DblArr):0:4);
  
  WriteLn('');
  
  // ============================================
  // 6. Transformations
  // ============================================
  WriteLn('--- 6. Transformations ---');
  WriteLn('');
  
  IntArr := IntArrayCreate([1, 2, 3, 4, 5]);
  WriteLn('Original: [', IntArrayToString(IntArr), ']');
  WriteLn('Reverse:  [', IntArrayToString(IntArrayReverse(IntArr)), ']');
  WriteLn('Map(x*2): [', IntArrayToString(IntArrayMap(IntArr, 2)), ']');
  WriteLn('Map(x*3+1): [', IntArrayToString(IntArrayMap(IntArr, 3, 1)), ']');
  WriteLn('Filter(2-4): [', IntArrayToString(IntArrayFilter(IntArr, 2, 4)), ']');
  
  IntArr := IntArrayCreate([1, 2, 2, 3, 3, 3, 4]);
  WriteLn('With duplicates: [', IntArrayToString(IntArr), ']');
  WriteLn('Unique: [', IntArrayToString(IntArrayUnique(IntArr)), ']');
  
  WriteLn('Fill(5, 7): [', IntArrayToString(IntArrayFill(5, 7)), ']');
  WriteLn('FillRange(1, 5): [', IntArrayToString(IntArrayFillRange(1, 5)), ']');
  WriteLn('FillRange(10, 5): [', IntArrayToString(IntArrayFillRange(10, 5)), ']');
  
  WriteLn('');
  
  // ============================================
  // 7. Set Operations
  // ============================================
  WriteLn('--- 7. Set Operations ---');
  WriteLn('');
  
  IntArr := IntArrayCreate([1, 2, 3, 4]);
  ResultArr := IntArrayCreate([3, 4, 5, 6]);
  WriteLn('Set A: [', IntArrayToString(IntArr), ']');
  WriteLn('Set B: [', IntArrayToString(ResultArr), ']');
  
  WriteLn('Union:      [', IntArrayToString(IntArrayUnion(IntArr, ResultArr)), ']');
  WriteLn('Intersect:  [', IntArrayToString(IntArrayIntersect(IntArr, ResultArr)), ']');
  WriteLn('Diff A-B:   [', IntArrayToString(IntArrayDifference(IntArr, ResultArr)), ']');
  WriteLn('Diff B-A:   [', IntArrayToString(IntArrayDifference(ResultArr, IntArr)), ']');
  WriteLn('SymDiff:    [', IntArrayToString(IntArraySymmetricDifference(IntArr, ResultArr)), ']');
  
  WriteLn('IsSubset([1,2], A): ', IntArrayIsSubset(IntArrayCreate([1, 2]), IntArr));
  WriteLn('IsDisjoint([1,2], [5,6]): ', IntArrayIsDisjoint(IntArrayCreate([1, 2]), IntArrayCreate([5, 6])));
  
  WriteLn('');
  
  // ============================================
  // 8. Chunking and Partitioning
  // ============================================
  WriteLn('--- 8. Chunking and Partitioning ---');
  WriteLn('');
  
  IntArr := IntArrayCreate([1, 2, 3, 4, 5, 6, 7, 8, 9]);
  WriteLn('Array: [', IntArrayToString(IntArr), ']');
  
  Chunks := IntArrayChunk(IntArr, 3);
  WriteLn('Chunk(size=3):');
  for I := 0 to High(Chunks) do
    WriteLn('  Chunk ', I, ': [', IntArrayToString(Chunks[I]), ']');
  
  IntArr := IntArrayCreate([1, 5, 10, 15, 20, 25]);
  Chunks := IntArrayPartition(IntArr, 10);
  WriteLn('Partition(pivot=10):');
  WriteLn('  Less than 10: [', IntArrayToString(Chunks[0]), ']');
  WriteLn('  >= 10: [', IntArrayToString(Chunks[1]), ']');
  
  WriteLn('');
  
  // ============================================
  // 9. String Arrays
  // ============================================
  WriteLn('--- 9. String Arrays ---');
  WriteLn('');
  
  StrArr := StrArrayCreate(['apple', 'banana', 'cherry', 'date']);
  WriteLn('String array: [', StrArrayToString(StrArr), ']');
  
  WriteLn('Contains(banana): ', StrArrayContains(StrArr, 'banana'));
  WriteLn('Contains(BANANA, IgnoreCase): ', StrArrayContains(StrArr, 'BANANA', True));
  WriteLn('IndexOf(cherry): ', StrArrayIndexOf(StrArr, 'cherry'));
  
  StrArrayAdd(StrArr, 'elderberry');
  WriteLn('After Add: [', StrArrayToString(StrArr), ']');
  
  WriteLn('Sorted: [', StrArrayToString(StrArraySort(StrArr)), ']');
  
  StrArr := StrArrayCreate(['apple', 'apple', 'banana', 'cherry', 'cherry']);
  WriteLn('With duplicates: [', StrArrayToString(StrArr), ']');
  WriteLn('Unique: [', StrArrayToString(StrArrayUnique(StrArr)), ']');
  
  WriteLn('');
  
  // ============================================
  // 10. Special Operations
  // ============================================
  WriteLn('--- 10. Special Operations ---');
  WriteLn('');
  
  IntArr := IntArrayCreate([1, 2, 3, 4, 5]);
  WriteLn('Original: [', IntArrayToString(IntArr), ']');
  WriteLn('RotateLeft(2): [', IntArrayToString(IntArrayRotateLeft(IntArr, 2)), ']');
  WriteLn('RotateRight(2): [', IntArrayToString(IntArrayRotateRight(IntArr, 2)), ']');
  WriteLn('Shuffle: [', IntArrayToString(IntArrayShuffle(IntArr)), ']');
  WriteLn('Sample(3): [', IntArrayToString(IntArraySample(IntArr, 3)), ']');
  
  WriteLn('');
  
  // ============================================
  // 11. Random Array Generation
  // ============================================
  WriteLn('--- 11. Random Array Generation ---');
  WriteLn('');
  
  WriteLn('Random(10, 1-100): [', IntArrayToString(IntArrayFillRandom(10, 1, 100)), ']');
  
  WriteLn('');
  WriteLn('========================================');
  WriteLn('All examples completed successfully!');
  WriteLn('========================================');
  WriteLn('');
end.