{*******************************************************************************
  AllToolkit - Delphi Array Utilities Test
  
  测试数组工具库的所有功能
********************************************************************************}

unit array_utils_test;

interface

uses
  SysUtils, Classes, mod;

procedure RunAllTests;

implementation

procedure TestIntArrayBasic;
var
  Arr, Arr2: TIntArray;
  I: Integer;
begin
  WriteLn('=== Testing IntArray Basic Operations ===');
  
  // Test creation
  Arr := IntArrayCreate([1, 2, 3, 4, 5]);
  WriteLn('Create: Length = ', IntArrayLength(Arr), ' (expected 5)');
  Assert(IntArrayLength(Arr) = 5, 'Create failed');
  
  // Test get/set
  WriteLn('Get(2) = ', IntArrayGet(Arr, 2), ' (expected 3)');
  Assert(IntArrayGet(Arr, 2) = 3, 'Get failed');
  IntArraySet(Arr, 2, 10);
  WriteLn('Set(2, 10) -> Get(2) = ', IntArrayGet(Arr, 2), ' (expected 10)');
  Assert(IntArrayGet(Arr, 2) = 10, 'Set failed');
  
  // Test add
  I := IntArrayAdd(Arr, 100);
  WriteLn('Add(100): Index = ', I, ' Length = ', IntArrayLength(Arr), ' (expected 6)');
  Assert(I = 5, 'Add index failed');
  Assert(IntArrayLength(Arr) = 6, 'Add length failed');
  
  // Test insert
  IntArrayInsert(Arr, 0, 0);
  WriteLn('Insert(0, 0): First element = ', IntArrayGet(Arr, 0), ' (expected 0)');
  Assert(IntArrayGet(Arr, 0) = 0, 'Insert failed');
  
  // Test delete
  IntArrayDelete(Arr, 0);
  WriteLn('Delete(0): First element = ', IntArrayGet(Arr, 0), ' (expected 1)');
  Assert(IntArrayGet(Arr, 0) = 1, 'Delete failed');
  
  // Test copy
  Arr2 := IntArrayCopy(Arr);
  WriteLn('Copy: Length = ', IntArrayLength(Arr2), ' (expected ', IntArrayLength(Arr), ')');
  Assert(IntArrayEquals(Arr, Arr2), 'Copy failed');
  
  // Test slice
  Arr2 := IntArraySlice(Arr, 1, 3);
  WriteLn('Slice(1, 3): Length = ', IntArrayLength(Arr2), ' (expected 3)');
  Assert(IntArrayLength(Arr2) = 3, 'Slice length failed');
  
  // Test clear
  IntArrayClear(Arr);
  WriteLn('Clear: Length = ', IntArrayLength(Arr), ' (expected 0)');
  Assert(IntArrayLength(Arr) = 0, 'Clear failed');
  
  WriteLn('IntArray Basic Tests PASSED');
  WriteLn('');
end;

procedure TestStrArrayBasic;
var
  Arr, Arr2: TStringArray;
  I: Integer;
begin
  WriteLn('=== Testing StrArray Basic Operations ===');
  
  // Test creation
  Arr := StrArrayCreate(['apple', 'banana', 'cherry']);
  WriteLn('Create: Length = ', StrArrayLength(Arr), ' (expected 3)');
  Assert(StrArrayLength(Arr) = 3, 'Create failed');
  
  // Test get/set
  WriteLn('Get(1) = ', StrArrayGet(Arr, 1), ' (expected banana)');
  Assert(StrArrayGet(Arr, 1) = 'banana', 'Get failed');
  StrArraySet(Arr, 1, 'blueberry');
  WriteLn('Set(1, blueberry) -> Get(1) = ', StrArrayGet(Arr, 1));
  Assert(StrArrayGet(Arr, 1) = 'blueberry', 'Set failed');
  
  // Test add
  I := StrArrayAdd(Arr, 'date');
  WriteLn('Add(date): Index = ', I, ' Length = ', StrArrayLength(Arr));
  Assert(I = 3, 'Add index failed');
  Assert(StrArrayLength(Arr) = 4, 'Add length failed');
  
  // Test copy
  Arr2 := StrArrayCopy(Arr);
  Assert(StrArrayEquals(Arr, Arr2), 'Copy failed');
  
  WriteLn('StrArray Basic Tests PASSED');
  WriteLn('');
end;

procedure TestIntArraySearch;
var
  Arr: TIntArray;
begin
  WriteLn('=== Testing IntArray Search Operations ===');
  
  Arr := IntArrayCreate([10, 20, 30, 20, 40, 20, 50]);
  
  // Test indexOf
  WriteLn('IndexOf(20) = ', IntArrayIndexOf(Arr, 20), ' (expected 1)');
  Assert(IntArrayIndexOf(Arr, 20) = 1, 'IndexOf failed');
  
  // Test lastIndexOf
  WriteLn('LastIndexOf(20) = ', IntArrayLastIndexOf(Arr, 20), ' (expected 5)');
  Assert(IntArrayLastIndexOf(Arr, 20) = 5, 'LastIndexOf failed');
  
  // Test contains
  WriteLn('Contains(30) = ', IntArrayContains(Arr, 30), ' (expected True)');
  Assert(IntArrayContains(Arr, 30), 'Contains failed');
  WriteLn('Contains(99) = ', IntArrayContains(Arr, 99), ' (expected False)');
  Assert(not IntArrayContains(Arr, 99), 'Contains negative failed');
  
  // Test count
  WriteLn('Count(20) = ', IntArrayCount(Arr, 20), ' (expected 3)');
  Assert(IntArrayCount(Arr, 20) = 3, 'Count failed');
  
  WriteLn('IntArray Search Tests PASSED');
  WriteLn('');
end;

procedure TestIntArraySorting;
var
  Arr, Sorted: TIntArray;
begin
  WriteLn('=== Testing IntArray Sorting Operations ===');
  
  Arr := IntArrayCreate([5, 3, 8, 1, 9, 2, 7, 4, 6]);
  
  // Test bubble sort
  Sorted := IntArraySortBubble(Arr);
  WriteLn('BubbleSort: IsSorted = ', IntArrayIsSorted(Sorted));
  Assert(IntArrayIsSorted(Sorted), 'BubbleSort failed');
  
  // Test quick sort
  Sorted := IntArraySortQuick(Arr);
  WriteLn('QuickSort: IsSorted = ', IntArrayIsSorted(Sorted));
  Assert(IntArrayIsSorted(Sorted), 'QuickSort failed');
  
  // Test merge sort
  Sorted := IntArraySortMerge(Arr);
  WriteLn('MergeSort: IsSorted = ', IntArrayIsSorted(Sorted));
  Assert(IntArrayIsSorted(Sorted), 'MergeSort failed');
  
  // Test selection sort
  Sorted := IntArraySortSelection(Arr);
  WriteLn('SelectionSort: IsSorted = ', IntArrayIsSorted(Sorted));
  Assert(IntArrayIsSorted(Sorted), 'SelectionSort failed');
  
  // Test insertion sort
  Sorted := IntArraySortInsertion(Arr);
  WriteLn('InsertionSort: IsSorted = ', IntArrayIsSorted(Sorted));
  Assert(IntArrayIsSorted(Sorted), 'InsertionSort failed');
  
  // Test binary search
  Sorted := IntArraySortQuick(Arr);
  WriteLn('BinarySearch(5) = ', IntArrayBinarySearch(Sorted, 5), ' (expected 4)');
  Assert(IntArrayBinarySearch(Sorted, 5) >= 0, 'BinarySearch failed');
  
  WriteLn('IntArray Sorting Tests PASSED');
  WriteLn('');
end;

procedure TestIntArrayStats;
var
  Arr: TIntArray;
  MinVal, MaxVal: Integer;
begin
  WriteLn('=== Testing IntArray Statistics ===');
  
  Arr := IntArrayCreate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
  
  // Test sum
  WriteLn('Sum = ', IntArraySum(Arr), ' (expected 55)');
  Assert(IntArraySum(Arr) = 55, 'Sum failed');
  
  // Test min/max
  WriteLn('Min = ', IntArrayMin(Arr), ' (expected 1)');
  Assert(IntArrayMin(Arr) = 1, 'Min failed');
  WriteLn('Max = ', IntArrayMax(Arr), ' (expected 10)');
  Assert(IntArrayMax(Arr) = 10, 'Max failed');
  
  // Test minmax
  IntArrayMinMax(Arr, MinVal, MaxVal);
  WriteLn('MinMax: Min=', MinVal, ' Max=', MaxVal);
  Assert((MinVal = 1) and (MaxVal = 10), 'MinMax failed');
  
  // Test range
  WriteLn('Range = ', IntArrayRange(Arr), ' (expected 9)');
  Assert(IntArrayRange(Arr) = 9, 'Range failed');
  
  // Test average
  WriteLn('Average = ', IntArrayAverage(Arr):0:1, ' (expected 5.5)');
  Assert(IntArrayAverage(Arr) = 5.5, 'Average failed');
  
  // Test median
  Arr := IntArrayCreate([1, 2, 3, 4, 5]);
  WriteLn('Median([1,2,3,4,5]) = ', IntArrayMedian(Arr):0:1, ' (expected 3)');
  Assert(IntArrayMedian(Arr) = 3, 'Median failed');
  
  Arr := IntArrayCreate([1, 2, 3, 4, 5, 6]);
  WriteLn('Median([1,2,3,4,5,6]) = ', IntArrayMedian(Arr):0:1, ' (expected 3.5)');
  Assert(IntArrayMedian(Arr) = 3.5, 'Median even failed');
  
  // Test mode
  Arr := IntArrayCreate([1, 2, 2, 3, 3, 3, 4]);
  WriteLn('Mode([1,2,2,3,3,3,4]) = ', IntArrayMode(Arr), ' (expected 3)');
  Assert(IntArrayMode(Arr) = 3, 'Mode failed');
  
  WriteLn('IntArray Statistics Tests PASSED');
  WriteLn('');
end;

procedure TestDblArrayStats;
var
  Arr: TDoubleArray;
begin
  WriteLn('=== Testing DblArray Statistics ===');
  
  Arr := DblArrayCreate([1.0, 2.0, 3.0, 4.0, 5.0]);
  
  WriteLn('Sum = ', DblArraySum(Arr):0:1, ' (expected 15)');
  Assert(DblArraySum(Arr) = 15, 'DblSum failed');
  
  WriteLn('Average = ', DblArrayAverage(Arr):0:1, ' (expected 3)');
  Assert(DblArrayAverage(Arr) = 3, 'DblAverage failed');
  
  WriteLn('StdDev = ', DblArrayStdDev(Arr):0:4);
  WriteLn('Variance = ', DblArrayVariance(Arr):0:4);
  
  WriteLn('DblArray Statistics Tests PASSED');
  WriteLn('');
end;

procedure TestIntArrayTransform;
var
  Arr, Result: TIntArray;
begin
  WriteLn('=== Testing IntArray Transformations ===');
  
  Arr := IntArrayCreate([1, 2, 3, 4, 5]);
  
  // Test reverse
  Result := IntArrayReverse(Arr);
  WriteLn('Reverse: [', IntArrayToString(Result), ']');
  Assert(Result[0] = 5, 'Reverse failed');
  
  // Test unique
  Arr := IntArrayCreate([1, 2, 2, 3, 3, 3, 4]);
  Result := IntArrayUnique(Arr);
  WriteLn('Unique: Length = ', IntArrayLength(Result), ' (expected 4)');
  Assert(IntArrayLength(Result) = 4, 'Unique failed');
  
  // Test fill
  Result := IntArrayFill(5, 42);
  WriteLn('Fill(5, 42): AllSame = ', IntArrayAllSame(Result));
  Assert(IntArrayAllSame(Result), 'Fill failed');
  
  // Test fillRange
  Result := IntArrayFillRange(1, 5);
  WriteLn('FillRange(1, 5): [', IntArrayToString(Result), ']');
  Assert(IntArrayEquals(Result, IntArrayCreate([1, 2, 3, 4, 5])), 'FillRange failed');
  
  // Test map
  Arr := IntArrayCreate([1, 2, 3, 4, 5]);
  Result := IntArrayMap(Arr, 2, 1);
  WriteLn('Map(x*2+1): [', IntArrayToString(Result), ']');
  Assert(Result[0] = 3, 'Map failed');
  
  // Test filter
  Result := IntArrayFilter(Arr, 2, 4);
  WriteLn('Filter(2-4): [', IntArrayToString(Result), ']');
  Assert(IntArrayLength(Result) = 3, 'Filter failed');
  
  WriteLn('IntArray Transform Tests PASSED');
  WriteLn('');
end;

procedure TestSetOperations;
var
  Arr1, Arr2, Result: TIntArray;
begin
  WriteLn('=== Testing Set Operations ===');
  
  Arr1 := IntArrayCreate([1, 2, 3, 4]);
  Arr2 := IntArrayCreate([3, 4, 5, 6]);
  
  // Test union
  Result := IntArrayUnion(Arr1, Arr2);
  WriteLn('Union: Length = ', IntArrayLength(Result), ' (expected 6)');
  Assert(IntArrayLength(Result) = 6, 'Union failed');
  
  // Test intersect
  Result := IntArrayIntersect(Arr1, Arr2);
  WriteLn('Intersect: [', IntArrayToString(Result), ']');
  Assert(IntArrayEquals(Result, IntArrayCreate([3, 4])), 'Intersect failed');
  
  // Test difference
  Result := IntArrayDifference(Arr1, Arr2);
  WriteLn('Difference(Arr1-Arr2): [', IntArrayToString(Result), ']');
  Assert(IntArrayLength(Result) = 2, 'Difference failed');
  
  // Test isSubset
  Arr1 := IntArrayCreate([1, 2]);
  Arr2 := IntArrayCreate([1, 2, 3, 4]);
  WriteLn('IsSubset([1,2], [1,2,3,4]) = ', IntArrayIsSubset(Arr1, Arr2));
  Assert(IntArrayIsSubset(Arr1, Arr2), 'IsSubset failed');
  
  // Test isDisjoint
  Arr1 := IntArrayCreate([1, 2]);
  Arr2 := IntArrayCreate([3, 4]);
  WriteLn('IsDisjoint([1,2], [3,4]) = ', IntArrayIsDisjoint(Arr1, Arr2));
  Assert(IntArrayIsDisjoint(Arr1, Arr2), 'IsDisjoint failed');
  
  WriteLn('Set Operations Tests PASSED');
  WriteLn('');
end;

procedure TestChunking;
var
  Arr: TIntArray;
  Chunks: array of TIntArray;
  I: Integer;
begin
  WriteLn('=== Testing Chunking ===');
  
  Arr := IntArrayCreate([1, 2, 3, 4, 5, 6, 7, 8, 9]);
  Chunks := IntArrayChunk(Arr, 3);
  
  WriteLn('Chunk([1..9], 3): ChunkCount = ', Length(Chunks), ' (expected 3)');
  Assert(Length(Chunks) = 3, 'Chunk count failed');
  
  for I := 0 to High(Chunks) do
    WriteLn('Chunk ', I, ': [', IntArrayToString(Chunks[I]), ']');
  
  // Test partition
  Arr := IntArrayCreate([1, 5, 10, 15, 20]);
  Chunks := IntArrayPartition(Arr, 10);
  WriteLn('Partition(Pivot=10): Less=[', IntArrayToString(Chunks[0]), '] Greater=[', IntArrayToString(Chunks[1]), ']');
  
  WriteLn('Chunking Tests PASSED');
  WriteLn('');
end;

procedure TestStringConversion;
var
  Arr: TIntArray;
  S: string;
  Arr2: TIntArray;
begin
  WriteLn('=== Testing String Conversion ===');
  
  Arr := IntArrayCreate([1, 2, 3, 4, 5]);
  S := IntArrayToString(Arr);
  WriteLn('ToString: "', S, '"');
  Assert(S = '1,2,3,4,5', 'ToString failed');
  
  Arr2 := IntArrayFromString(S);
  WriteLn('FromString: Length = ', IntArrayLength(Arr2));
  Assert(IntArrayEquals(Arr, Arr2), 'FromString failed');
  
  WriteLn('String Conversion Tests PASSED');
  WriteLn('');
end;

procedure TestSpecialOperations;
var
  Arr, Result: TIntArray;
begin
  WriteLn('=== Testing Special Operations ===');
  
  Arr := IntArrayCreate([1, 2, 3, 4, 5]);
  
  // Test rotate left
  Result := IntArrayRotateLeft(Arr, 2);
  WriteLn('RotateLeft(2): [', IntArrayToString(Result), ']');
  Assert(Result[0] = 3, 'RotateLeft failed');
  
  // Test rotate right
  Result := IntArrayRotateRight(Arr, 2);
  WriteLn('RotateRight(2): [', IntArrayToString(Result), ']');
  Assert(Result[0] = 4, 'RotateRight failed');
  
  // Test shuffle (just check length preserved)
  Result := IntArrayShuffle(Arr);
  WriteLn('Shuffle: Length = ', IntArrayLength(Result));
  Assert(IntArrayLength(Result) = 5, 'Shuffle failed');
  
  // Test sample
  Result := IntArraySample(Arr, 3);
  WriteLn('Sample(3): Length = ', IntArrayLength(Result));
  Assert(IntArrayLength(Result) = 3, 'Sample failed');
  
  WriteLn('Special Operations Tests PASSED');
  WriteLn('');
end;

procedure RunAllTests;
begin
  WriteLn('');
  WriteLn('========================================');
  WriteLn('AllToolkit - Delphi Array Utilities Test');
  WriteLn('========================================');
  WriteLn('');
  
  TestIntArrayBasic;
  TestStrArrayBasic;
  TestIntArraySearch;
  TestIntArraySorting;
  TestIntArrayStats;
  TestDblArrayStats;
  TestIntArrayTransform;
  TestSetOperations;
  TestChunking;
  TestStringConversion;
  TestSpecialOperations;
  
  WriteLn('========================================');
  WriteLn('ALL TESTS PASSED!');
  WriteLn('========================================');
  WriteLn('');
end;

end.