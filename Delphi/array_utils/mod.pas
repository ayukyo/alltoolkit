{*******************************************************************************
  AllToolkit - Delphi Array Utilities
  
  一个零依赖的数组处理工具库，适用于 Delphi 7+ 和 Free Pascal
  
  功能包括：
  - 动态数组操作（添加、插入、删除、合并）
  - 查找与搜索（线性搜索、二分搜索）
  - 排序算法（冒泡、快速、归并排序）
  - 统计函数（求和、平均、最大、最小）
  - 数组转换（反转、去重、填充）
  - 集合操作（交集、并集、差集）
  - 分区与分块
  - 数组验证与比较
  
  作者：AllToolkit Contributors
  许可证：MIT
********************************************************************************}

unit mod;

interface

uses
  SysUtils, Classes, Math;

type
  TIntArray = array of Integer;
  TInt64Array = array of Int64;
  TDoubleArray = array of Double;
  TStringArray = array of string;
  TBooleanArray = array of Boolean;
  
  TCompareFunction = function(const A, B: Integer): Integer;
  TCompareFunction64 = function(const A, B: Int64): Integer;
  TCompareFunctionDbl = function(const A, B: Double): Integer;
  TCompareFunctionStr = function(const A, B: string): Integer;

{===============================================================================
  动态数组基础操作 - Integer
===============================================================================}
function IntArrayCreate(const Values: array of Integer): TIntArray;
function IntArrayLength(const Arr: TIntArray): Integer;
function IntArrayGet(const Arr: TIntArray; Index: Integer): Integer;
procedure IntArraySet(var Arr: TIntArray; Index: Integer; Value: Integer);
function IntArrayAdd(var Arr: TIntArray; Value: Integer): Integer;
function IntArrayInsert(var Arr: TIntArray; Index: Integer; Value: Integer): Boolean;
function IntArrayDelete(var Arr: TIntArray; Index: Integer): Boolean;
function IntArrayClear(var Arr: TIntArray): Boolean;
function IntArrayCopy(const Arr: TIntArray): TIntArray;
function IntArraySlice(const Arr: TIntArray; Start, Count: Integer): TIntArray;

{===============================================================================
  动态数组基础操作 - String
===============================================================================}
function StrArrayCreate(const Values: array of string): TStringArray;
function StrArrayLength(const Arr: TStringArray): Integer;
function StrArrayGet(const Arr: TStringArray; Index: Integer): string;
procedure StrArraySet(var Arr: TStringArray; Index: Integer; const Value: string);
function StrArrayAdd(var Arr: TStringArray; const Value: string): Integer;
function StrArrayInsert(var Arr: TStringArray; Index: Integer; const Value: string): Boolean;
function StrArrayDelete(var Arr: TStringArray; Index: Integer): Boolean;
function StrArrayClear(var Arr: TStringArray): Boolean;
function StrArrayCopy(const Arr: TStringArray): TStringArray;
function StrArraySlice(const Arr: TStringArray; Start, Count: Integer): TStringArray;

{===============================================================================
  动态数组基础操作 - Double
===============================================================================}
function DblArrayCreate(const Values: array of Double): TDoubleArray;
function DblArrayLength(const Arr: TDoubleArray): Integer;
function DblArrayGet(const Arr: TDoubleArray; Index: Integer): Double;
procedure DblArraySet(var Arr: TDoubleArray; Index: Integer; Value: Double);
function DblArrayAdd(var Arr: TDoubleArray; Value: Double): Integer;
function DblArrayInsert(var Arr: TDoubleArray; Index: Integer; Value: Double): Boolean;
function DblArrayDelete(var Arr: TDoubleArray; Index: Integer): Boolean;
function DblArrayClear(var Arr: TDoubleArray): Boolean;
function DblArrayCopy(const Arr: TDoubleArray): TDoubleArray;
function DblArraySlice(const Arr: TDoubleArray; Start, Count: Integer): TDoubleArray;

{===============================================================================
  查找与搜索 - Integer
===============================================================================}
function IntArrayIndexOf(const Arr: TIntArray; Value: Integer): Integer;
function IntArrayLastIndexOf(const Arr: TIntArray; Value: Integer): Integer;
function IntArrayContains(const Arr: TIntArray; Value: Integer): Boolean;
function IntArrayCount(const Arr: TIntArray; Value: Integer): Integer;
function IntArrayFindAll(const Arr: TIntArray; Value: Integer): TIntArray;
function IntArrayBinarySearch(const Arr: TIntArray; Value: Integer): Integer;

{===============================================================================
  查找与搜索 - String
===============================================================================}
function StrArrayIndexOf(const Arr: TStringArray; const Value: string; IgnoreCase: Boolean = False): Integer;
function StrArrayLastIndexOf(const Arr: TStringArray; const Value: string; IgnoreCase: Boolean = False): Integer;
function StrArrayContains(const Arr: TStringArray; const Value: string; IgnoreCase: Boolean = False): Boolean;
function StrArrayCount(const Arr: TStringArray; const Value: string; IgnoreCase: Boolean = False): Integer;
function StrArrayFindAll(const Arr: TStringArray; const Value: string; IgnoreCase: Boolean = False): TStringArray;

{===============================================================================
  排序算法 - Integer
===============================================================================}
function IntArraySortBubble(const Arr: TIntArray): TIntArray;
function IntArraySortQuick(const Arr: TIntArray): TIntArray;
function IntArraySortMerge(const Arr: TIntArray): TIntArray;
function IntArraySortSelection(const Arr: TIntArray): TIntArray;
function IntArraySortInsertion(const Arr: TIntArray): TIntArray;
procedure IntArraySortInPlace(var Arr: TIntArray);

{===============================================================================
  排序算法 - String
===============================================================================}
function StrArraySort(const Arr: TStringArray; IgnoreCase: Boolean = False): TStringArray;
procedure StrArraySortInPlace(var Arr: TStringArray; IgnoreCase: Boolean = False);

{===============================================================================
  统计函数 - Integer
===============================================================================}
function IntArraySum(const Arr: TIntArray): Int64;
function IntArrayProduct(const Arr: TIntArray): Int64;
function IntArrayAverage(const Arr: TIntArray): Double;
function IntArrayMin(const Arr: TIntArray): Integer;
function IntArrayMax(const Arr: TIntArray): Integer;
function IntArrayMinMax(const Arr: TIntArray; out MinVal, MaxVal: Integer): Boolean;
function IntArrayRange(const Arr: TIntArray): Integer;
function IntArrayMedian(const Arr: TIntArray): Double;
function IntArrayMode(const Arr: TIntArray): Integer;

{===============================================================================
  统计函数 - Double
===============================================================================}
function DblArraySum(const Arr: TDoubleArray): Double;
function DblArrayProduct(const Arr: TDoubleArray): Double;
function DblArrayAverage(const Arr: TDoubleArray): Double;
function DblArrayMin(const Arr: TDoubleArray): Double;
function DblArrayMax(const Arr: TDoubleArray): Double;
function DblArrayMinMax(const Arr: TDoubleArray; out MinVal, MaxVal: Double): Boolean;
function DblArrayRange(const Arr: TDoubleArray): Double;
function DblArrayMedian(const Arr: TDoubleArray): Double;
function DblArrayStdDev(const Arr: TDoubleArray): Double;
function DblArrayVariance(const Arr: TDoubleArray): Double;

{===============================================================================
  数组转换 - Integer
===============================================================================}
function IntArrayReverse(const Arr: TIntArray): TIntArray;
procedure IntArrayReverseInPlace(var Arr: TIntArray);
function IntArrayUnique(const Arr: TIntArray): TIntArray;
function IntArrayFill(Count: Integer; Value: Integer): TIntArray;
function IntArrayFillRange(StartVal, EndVal: Integer): TIntArray;
function IntArrayFillRandom(Count: Integer; MinVal, MaxVal: Integer): TIntArray;
function IntArrayMap(const Arr: TIntArray; Multiplier: Integer; Offset: Integer = 0): TIntArray;
function IntArrayFilter(const Arr: TIntArray; MinVal, MaxVal: Integer): TIntArray;

{===============================================================================
  数组转换 - String
===============================================================================}
function StrArrayReverse(const Arr: TStringArray): TStringArray;
procedure StrArrayReverseInPlace(var Arr: TStringArray);
function StrArrayUnique(const Arr: TStringArray; IgnoreCase: Boolean = False): TStringArray;
function StrArrayFill(Count: Integer; const Value: string): TStringArray;

{===============================================================================
  集合操作 - Integer
===============================================================================}
function IntArrayUnion(const Arr1, Arr2: TIntArray): TIntArray;
function IntArrayIntersect(const Arr1, Arr2: TIntArray): TIntArray;
function IntArrayDifference(const Arr1, Arr2: TIntArray): TIntArray;
function IntArraySymmetricDifference(const Arr1, Arr2: TIntArray): TIntArray;
function IntArrayIsSubset(const SubArr, MainArr: TIntArray): Boolean;
function IntArrayIsDisjoint(const Arr1, Arr2: TIntArray): Boolean;

{===============================================================================
  集合操作 - String
===============================================================================}
function StrArrayUnion(const Arr1, Arr2: TStringArray; IgnoreCase: Boolean = False): TStringArray;
function StrArrayIntersect(const Arr1, Arr2: TStringArray; IgnoreCase: Boolean = False): TStringArray;
function StrArrayDifference(const Arr1, Arr2: TStringArray; IgnoreCase: Boolean = False): TStringArray;
function StrArraySymmetricDifference(const Arr1, Arr2: TStringArray; IgnoreCase: Boolean = False): TStringArray;
function StrArrayIsSubset(const SubArr, MainArr: TStringArray; IgnoreCase: Boolean = False): Boolean;

{===============================================================================
  分区与分块
===============================================================================}
function IntArrayChunk(const Arr: TIntArray; ChunkSize: Integer): array of TIntArray;
function StrArrayChunk(const Arr: TStringArray; ChunkSize: Integer): array of TStringArray;
function IntArrayPartition(const Arr: TIntArray; Pivot: Integer): array of TIntArray;
function StrArrayPartitionByLength(const Arr: TStringArray; MaxLength: Integer): TStringArray;

{===============================================================================
  数组验证与比较
===============================================================================}
function IntArrayEquals(const Arr1, Arr2: TIntArray): Boolean;
function StrArrayEquals(const Arr1, Arr2: TStringArray; IgnoreCase: Boolean = False): Boolean;
function IntArrayIsEmpty(const Arr: TIntArray): Boolean;
function StrArrayIsEmpty(const Arr: TStringArray): Boolean;
function IntArrayAllSame(const Arr: TIntArray): Boolean;
function StrArrayAllSame(const Arr: TStringArray; IgnoreCase: Boolean = False): Boolean;
function IntArrayIsSorted(const Arr: TIntArray): Boolean;
function StrArrayIsSorted(const Arr: TStringArray; IgnoreCase: Boolean = False): Boolean;

{===============================================================================
  字符串与数组互转
===============================================================================}
function IntArrayToString(const Arr: TIntArray; const Delimiter: string = ','): string;
function IntArrayFromString(const S: string; const Delimiter: string = ','): TIntArray;
function StrArrayToString(const Arr: TStringArray; const Delimiter: string = ','): string;
function StrArrayFromString(const S: string; const Delimiter: string = ','): TStringArray;

{===============================================================================
  特殊操作
===============================================================================}
function IntArrayRotateLeft(const Arr: TIntArray; Positions: Integer): TIntArray;
function IntArrayRotateRight(const Arr: TIntArray; Positions: Integer): TIntArray;
function IntArrayShuffle(const Arr: TIntArray): TIntArray;
function StrArrayShuffle(const Arr: TStringArray): TStringArray;
function IntArraySample(const Arr: TIntArray; Count: Integer): TIntArray;
function StrArraySample(const Arr: TStringArray; Count: Integer): TStringArray;

implementation

{===============================================================================
  内部辅助函数
===============================================================================}

procedure QuickSortInt(var Arr: TIntArray; Low, High: Integer);
var
  I, J, Pivot, Temp: Integer;
begin
  if Low < High then
  begin
    Pivot := Arr[(Low + High) div 2];
    I := Low;
    J := High;
    while I <= J do
    begin
      while Arr[I] < Pivot do Inc(I);
      while Arr[J] > Pivot do Dec(J);
      if I <= J then
      begin
        Temp := Arr[I];
        Arr[I] := Arr[J];
        Arr[J] := Temp;
        Inc(I);
        Dec(J);
      end;
    end;
    if Low < J then QuickSortInt(Arr, Low, J);
    if I < High then QuickSortInt(Arr, I, High);
  end;
end;

procedure QuickSortStr(var Arr: TStringArray; IgnoreCase: Boolean);
var
  I, J: Integer;
  Pivot, Temp: string;
  
  function Compare(const S1, S2: string): Integer;
  begin
    if IgnoreCase then
      Result := CompareText(S1, S2)
    else
      Result := CompareStr(S1, S2);
  end;
  
  procedure QSort(Low, High: Integer);
  begin
    if Low < High then
    begin
      Pivot := Arr[(Low + High) div 2];
      I := Low;
      J := High;
      while I <= J do
      begin
        while Compare(Arr[I], Pivot) < 0 do Inc(I);
        while Compare(Arr[J], Pivot) > 0 do Dec(J);
        if I <= J then
        begin
          Temp := Arr[I];
          Arr[I] := Arr[J];
          Arr[J] := Temp;
          Inc(I);
          Dec(J);
        end;
      end;
      if Low < J then QSort(Low, J);
      if I < High then QSort(I, High);
    end;
  end;
  
begin
  if Length(Arr) > 1 then
    QSort(0, Length(Arr) - 1);
end;

{===============================================================================
  动态数组基础操作 - Integer
===============================================================================}

function IntArrayCreate(const Values: array of Integer): TIntArray;
var
  I: Integer;
begin
  SetLength(Result, Length(Values));
  for I := 0 to High(Values) do
    Result[I] := Values[I];
end;

function IntArrayLength(const Arr: TIntArray): Integer;
begin
  Result := Length(Arr);
end;

function IntArrayGet(const Arr: TIntArray; Index: Integer): Integer;
begin
  if (Index >= 0) and (Index < Length(Arr)) then
    Result := Arr[Index]
  else
    Result := 0;
end;

procedure IntArraySet(var Arr: TIntArray; Index: Integer; Value: Integer);
begin
  if (Index >= 0) and (Index < Length(Arr)) then
    Arr[Index] := Value;
end;

function IntArrayAdd(var Arr: TIntArray; Value: Integer): Integer;
begin
  Result := Length(Arr);
  SetLength(Arr, Result + 1);
  Arr[Result] := Value;
end;

function IntArrayInsert(var Arr: TIntArray; Index: Integer; Value: Integer): Boolean;
var
  I, Len: Integer;
begin
  Len := Length(Arr);
  if (Index < 0) or (Index > Len) then
  begin
    Result := False;
    Exit;
  end;
  SetLength(Arr, Len + 1);
  for I := Len downto Index + 1 do
    Arr[I] := Arr[I - 1];
  Arr[Index] := Value;
  Result := True;
end;

function IntArrayDelete(var Arr: TIntArray; Index: Integer): Boolean;
var
  I, Len: Integer;
begin
  Len := Length(Arr);
  if (Index < 0) or (Index >= Len) then
  begin
    Result := False;
    Exit;
  end;
  for I := Index to Len - 2 do
    Arr[I] := Arr[I + 1];
  SetLength(Arr, Len - 1);
  Result := True;
end;

function IntArrayClear(var Arr: TIntArray): Boolean;
begin
  SetLength(Arr, 0);
  Result := True;
end;

function IntArrayCopy(const Arr: TIntArray): TIntArray;
var
  I: Integer;
begin
  SetLength(Result, Length(Arr));
  for I := 0 to High(Arr) do
    Result[I] := Arr[I];
end;

function IntArraySlice(const Arr: TIntArray; Start, Count: Integer): TIntArray;
var
  I, Len: Integer;
begin
  Len := Length(Arr);
  if Start < 0 then Start := 0;
  if Start >= Len then
  begin
    SetLength(Result, 0);
    Exit;
  end;
  if Count < 0 then Count := Len - Start;
  if Start + Count > Len then Count := Len - Start;
  SetLength(Result, Count);
  for I := 0 to Count - 1 do
    Result[I] := Arr[Start + I];
end;

{===============================================================================
  动态数组基础操作 - String
===============================================================================}

function StrArrayCreate(const Values: array of string): TStringArray;
var
  I: Integer;
begin
  SetLength(Result, Length(Values));
  for I := 0 to High(Values) do
    Result[I] := Values[I];
end;

function StrArrayLength(const Arr: TStringArray): Integer;
begin
  Result := Length(Arr);
end;

function StrArrayGet(const Arr: TStringArray; Index: Integer): string;
begin
  if (Index >= 0) and (Index < Length(Arr)) then
    Result := Arr[Index]
  else
    Result := '';
end;

procedure StrArraySet(var Arr: TStringArray; Index: Integer; const Value: string);
begin
  if (Index >= 0) and (Index < Length(Arr)) then
    Arr[Index] := Value;
end;

function StrArrayAdd(var Arr: TStringArray; const Value: string): Integer;
begin
  Result := Length(Arr);
  SetLength(Arr, Result + 1);
  Arr[Result] := Value;
end;

function StrArrayInsert(var Arr: TStringArray; Index: Integer; const Value: string): Boolean;
var
  I, Len: Integer;
begin
  Len := Length(Arr);
  if (Index < 0) or (Index > Len) then
  begin
    Result := False;
    Exit;
  end;
  SetLength(Arr, Len + 1);
  for I := Len downto Index + 1 do
    Arr[I] := Arr[I - 1];
  Arr[Index] := Value;
  Result := True;
end;

function StrArrayDelete(var Arr: TStringArray; Index: Integer): Boolean;
var
  I, Len: Integer;
begin
  Len := Length(Arr);
  if (Index < 0) or (Index >= Len) then
  begin
    Result := False;
    Exit;
  end;
  for I := Index to Len - 2 do
    Arr[I] := Arr[I + 1];
  SetLength(Arr, Len - 1);
  Result := True;
end;

function StrArrayClear(var Arr: TStringArray): Boolean;
begin
  SetLength(Arr, 0);
  Result := True;
end;

function StrArrayCopy(const Arr: TStringArray): TStringArray;
var
  I: Integer;
begin
  SetLength(Result, Length(Arr));
  for I := 0 to High(Arr) do
    Result[I] := Arr[I];
end;

function StrArraySlice(const Arr: TStringArray; Start, Count: Integer): TStringArray;
var
  I, Len: Integer;
begin
  Len := Length(Arr);
  if Start < 0 then Start := 0;
  if Start >= Len then
  begin
    SetLength(Result, 0);
    Exit;
  end;
  if Count < 0 then Count := Len - Start;
  if Start + Count > Len then Count := Len - Start;
  SetLength(Result, Count);
  for I := 0 to Count - 1 do
    Result[I] := Arr[Start + I];
end;

{===============================================================================
  动态数组基础操作 - Double
===============================================================================}

function DblArrayCreate(const Values: array of Double): TDoubleArray;
var
  I: Integer;
begin
  SetLength(Result, Length(Values));
  for I := 0 to High(Values) do
    Result[I] := Values[I];
end;

function DblArrayLength(const Arr: TDoubleArray): Integer;
begin
  Result := Length(Arr);
end;

function DblArrayGet(const Arr: TDoubleArray; Index: Integer): Double;
begin
  if (Index >= 0) and (Index < Length(Arr)) then
    Result := Arr[Index]
  else
    Result := 0.0;
end;

procedure DblArraySet(var Arr: TDoubleArray; Index: Integer; Value: Double);
begin
  if (Index >= 0) and (Index < Length(Arr)) then
    Arr[Index] := Value;
end;

function DblArrayAdd(var Arr: TDoubleArray; Value: Double): Integer;
begin
  Result := Length(Arr);
  SetLength(Arr, Result + 1);
  Arr[Result] := Value;
end;

function DblArrayInsert(var Arr: TDoubleArray; Index: Integer; Value: Double): Boolean;
var
  I, Len: Integer;
begin
  Len := Length(Arr);
  if (Index < 0) or (Index > Len) then
  begin
    Result := False;
    Exit;
  end;
  SetLength(Arr, Len + 1);
  for I := Len downto Index + 1 do
    Arr[I] := Arr[I - 1];
  Arr[Index] := Value;
  Result := True;
end;

function DblArrayDelete(var Arr: TDoubleArray; Index: Integer): Boolean;
var
  I, Len: Integer;
begin
  Len := Length(Arr);
  if (Index < 0) or (Index >= Len) then
  begin
    Result := False;
    Exit;
  end;
  for I := Index to Len - 2 do
    Arr[I] := Arr[I + 1];
  SetLength(Arr, Len - 1);
  Result := True;
end;

function DblArrayClear(var Arr: TDoubleArray): Boolean;
begin
  SetLength(Arr, 0);
  Result := True;
end;

function DblArrayCopy(const Arr: TDoubleArray): TDoubleArray;
var
  I: Integer;
begin
  SetLength(Result, Length(Arr));
  for I := 0 to High(Arr) do
    Result[I] := Arr[I];
end;

function DblArraySlice(const Arr: TDoubleArray; Start, Count: Integer): TDoubleArray;
var
  I, Len: Integer;
begin
  Len := Length(Arr);
  if Start < 0 then Start := 0;
  if Start >= Len then
  begin
    SetLength(Result, 0);
    Exit;
  end;
  if Count < 0 then Count := Len - Start;
  if Start + Count > Len then Count := Len - Start;
  SetLength(Result, Count);
  for I := 0 to Count - 1 do
    Result[I] := Arr[Start + I];
end;

{===============================================================================
  查找与搜索 - Integer
===============================================================================}

function IntArrayIndexOf(const Arr: TIntArray; Value: Integer): Integer;
var
  I: Integer;
begin
  for I := 0 to High(Arr) do
    if Arr[I] = Value then
    begin
      Result := I;
      Exit;
    end;
  Result := -1;
end;

function IntArrayLastIndexOf(const Arr: TIntArray; Value: Integer): Integer;
var
  I: Integer;
begin
  for I := High(Arr) downto 0 do
    if Arr[I] = Value then
    begin
      Result := I;
      Exit;
    end;
  Result := -1;
end;

function IntArrayContains(const Arr: TIntArray; Value: Integer): Boolean;
begin
  Result := IntArrayIndexOf(Arr, Value) >= 0;
end;

function IntArrayCount(const Arr: TIntArray; Value: Integer): Integer;
var
  I: Integer;
begin
  Result := 0;
  for I := 0 to High(Arr) do
    if Arr[I] = Value then
      Inc(Result);
end;

function IntArrayFindAll(const Arr: TIntArray; Value: Integer): TIntArray;
var
  I: Integer;
begin
  SetLength(Result, 0);
  for I := 0 to High(Arr) do
    if Arr[I] = Value then
      IntArrayAdd(Result, I);
end;

function IntArrayBinarySearch(const Arr: TIntArray; Value: Integer): Integer;
var
  Low, High, Mid: Integer;
begin
  Result := -1;
  Low := 0;
  High := Length(Arr) - 1;
  while Low <= High do
  begin
    Mid := (Low + High) div 2;
    if Arr[Mid] = Value then
    begin
      Result := Mid;
      Exit;
    end
    else if Arr[Mid] < Value then
      Low := Mid + 1
    else
      High := Mid - 1;
  end;
end;

{===============================================================================
  查找与搜索 - String
===============================================================================}

function StrArrayIndexOf(const Arr: TStringArray; const Value: string; IgnoreCase: Boolean = False): Integer;
var
  I: Integer;
begin
  for I := 0 to High(Arr) do
  begin
    if IgnoreCase then
    begin
      if SameText(Arr[I], Value) then
      begin
        Result := I;
        Exit;
      end;
    end
    else
    begin
      if Arr[I] = Value then
      begin
        Result := I;
        Exit;
      end;
    end;
  end;
  Result := -1;
end;

function StrArrayLastIndexOf(const Arr: TStringArray; const Value: string; IgnoreCase: Boolean = False): Integer;
var
  I: Integer;
begin
  for I := High(Arr) downto 0 do
  begin
    if IgnoreCase then
    begin
      if SameText(Arr[I], Value) then
      begin
        Result := I;
        Exit;
      end;
    end
    else
    begin
      if Arr[I] = Value then
      begin
        Result := I;
        Exit;
      end;
    end;
  end;
  Result := -1;
end;

function StrArrayContains(const Arr: TStringArray; const Value: string; IgnoreCase: Boolean = False): Boolean;
begin
  Result := StrArrayIndexOf(Arr, Value, IgnoreCase) >= 0;
end;

function StrArrayCount(const Arr: TStringArray; const Value: string; IgnoreCase: Boolean = False): Integer;
var
  I: Integer;
begin
  Result := 0;
  for I := 0 to High(Arr) do
  begin
    if IgnoreCase then
    begin
      if SameText(Arr[I], Value) then
        Inc(Result);
    end
    else
    begin
      if Arr[I] = Value then
        Inc(Result);
    end;
  end;
end;

function StrArrayFindAll(const Arr: TStringArray; const Value: string; IgnoreCase: Boolean = False): TStringArray;
var
  I: Integer;
begin
  SetLength(Result, 0);
  for I := 0 to High(Arr) do
  begin
    if IgnoreCase then
    begin
      if SameText(Arr[I], Value) then
        StrArrayAdd(Result, Arr[I]);
    end
    else
    begin
      if Arr[I] = Value then
        StrArrayAdd(Result, Arr[I]);
    end;
  end;
end;

{===============================================================================
  排序算法 - Integer
===============================================================================}

function IntArraySortBubble(const Arr: TIntArray): TIntArray;
var
  I, J, Temp: Integer;
  Swapped: Boolean;
begin
  Result := IntArrayCopy(Arr);
  if Length(Result) <= 1 then Exit;
  for I := 0 to Length(Result) - 2 do
  begin
    Swapped := False;
    for J := 0 to Length(Result) - I - 2 do
    begin
      if Result[J] > Result[J + 1] then
      begin
        Temp := Result[J];
        Result[J] := Result[J + 1];
        Result[J + 1] := Temp;
        Swapped := True;
      end;
    end;
    if not Swapped then Break;
  end;
end;

function IntArraySortQuick(const Arr: TIntArray): TIntArray;
begin
  Result := IntArrayCopy(Arr);
  if Length(Result) > 1 then
    QuickSortInt(Result, 0, Length(Result) - 1);
end;

function IntArraySortMerge(const Arr: TIntArray): TIntArray;
  
  procedure Merge(var A: TIntArray; Left, Mid, Right: Integer);
  var
    I, J, K: Integer;
    Temp: TIntArray;
  begin
    SetLength(Temp, Right - Left + 1);
    I := Left;
    J := Mid + 1;
    K := 0;
    while (I <= Mid) and (J <= Right) do
    begin
      if A[I] <= A[J] then
      begin
        Temp[K] := A[I];
        Inc(I);
      end
      else
      begin
        Temp[K] := A[J];
        Inc(J);
      end;
      Inc(K);
    end;
    while I <= Mid do
    begin
      Temp[K] := A[I];
      Inc(I);
      Inc(K);
    end;
    while J <= Right do
    begin
      Temp[K] := A[J];
      Inc(J);
      Inc(K);
    end;
    for I := 0 to K - 1 do
      A[Left + I] := Temp[I];
  end;
  
  procedure MergeSort(var A: TIntArray; Left, Right: Integer);
  var
    Mid: Integer;
  begin
    if Left < Right then
    begin
      Mid := (Left + Right) div 2;
      MergeSort(A, Left, Mid);
      MergeSort(A, Mid + 1, Right);
      Merge(A, Left, Mid, Right);
    end;
  end;
  
begin
  Result := IntArrayCopy(Arr);
  if Length(Result) > 1 then
    MergeSort(Result, 0, Length(Result) - 1);
end;

function IntArraySortSelection(const Arr: TIntArray): TIntArray;
var
  I, J, MinIdx, Temp: Integer;
begin
  Result := IntArrayCopy(Arr);
  if Length(Result) <= 1 then Exit;
  for I := 0 to Length(Result) - 2 do
  begin
    MinIdx := I;
    for J := I + 1 to Length(Result) - 1 do
      if Result[J] < Result[MinIdx] then
        MinIdx := J;
    if MinIdx <> I then
    begin
      Temp := Result[I];
      Result[I] := Result[MinIdx];
      Result[MinIdx] := Temp;
    end;
  end;
end;

function IntArraySortInsertion(const Arr: TIntArray): TIntArray;
var
  I, J, Temp: Integer;
begin
  Result := IntArrayCopy(Arr);
  if Length(Result) <= 1 then Exit;
  for I := 1 to Length(Result) - 1 do
  begin
    Temp := Result[I];
    J := I - 1;
    while (J >= 0) and (Result[J] > Temp) do
    begin
      Result[J + 1] := Result[J];
      Dec(J);
    end;
    Result[J + 1] := Temp;
  end;
end;

procedure IntArraySortInPlace(var Arr: TIntArray);
begin
  if Length(Arr) > 1 then
    QuickSortInt(Arr, 0, Length(Arr) - 1);
end;

{===============================================================================
  排序算法 - String
===============================================================================}

function StrArraySort(const Arr: TStringArray; IgnoreCase: Boolean = False): TStringArray;
begin
  Result := StrArrayCopy(Arr);
  if Length(Result) > 1 then
    QuickSortStr(Result, IgnoreCase);
end;

procedure StrArraySortInPlace(var Arr: TStringArray; IgnoreCase: Boolean = False);
begin
  if Length(Arr) > 1 then
    QuickSortStr(Arr, IgnoreCase);
end;

{===============================================================================
  统计函数 - Integer
===============================================================================}

function IntArraySum(const Arr: TIntArray): Int64;
var
  I: Integer;
begin
  Result := 0;
  for I := 0 to High(Arr) do
    Result := Result + Arr[I];
end;

function IntArrayProduct(const Arr: TIntArray): Int64;
var
  I: Integer;
begin
  if Length(Arr) = 0 then
  begin
    Result := 0;
    Exit;
  end;
  Result := 1;
  for I := 0 to High(Arr) do
    Result := Result * Arr[I];
end;

function IntArrayAverage(const Arr: TIntArray): Double;
var
  Sum: Int64;
begin
  if Length(Arr) = 0 then
  begin
    Result := 0.0;
    Exit;
  end;
  Sum := 0;
  for Sum := 0 to High(Arr) do
    Sum := Sum + Arr[Sum];
  Result := Sum / Length(Arr);
end;

function IntArrayMin(const Arr: TIntArray): Integer;
var
  I: Integer;
begin
  if Length(Arr) = 0 then
  begin
    Result := 0;
    Exit;
  end;
  Result := Arr[0];
  for I := 1 to High(Arr) do
    if Arr[I] < Result then
      Result := Arr[I];
end;

function IntArrayMax(const Arr: TIntArray): Integer;
var
  I: Integer;
begin
  if Length(Arr) = 0 then
  begin
    Result := 0;
    Exit;
  end;
  Result := Arr[0];
  for I := 1 to High(Arr) do
    if Arr[I] > Result then
      Result := Arr[I];
end;

function IntArrayMinMax(const Arr: TIntArray; out MinVal, MaxVal: Integer): Boolean;
var
  I: Integer;
begin
  if Length(Arr) = 0 then
  begin
    MinVal := 0;
    MaxVal := 0;
    Result := False;
    Exit;
  end;
  MinVal := Arr[0];
  MaxVal := Arr[0];
  for I := 1 to High(Arr) do
  begin
    if Arr[I] < MinVal then MinVal := Arr[I];
    if Arr[I] > MaxVal then MaxVal := Arr[I];
  end;
  Result := True;
end;

function IntArrayRange(const Arr: TIntArray): Integer;
var
  MinVal, MaxVal: Integer;
begin
  if IntArrayMinMax(Arr, MinVal, MaxVal) then
    Result := MaxVal - MinVal
  else
    Result := 0;
end;

function IntArrayMedian(const Arr: TIntArray): Double;
var
  Sorted: TIntArray;
  Len: Integer;
begin
  if Length(Arr) = 0 then
  begin
    Result := 0.0;
    Exit;
  end;
  Sorted := IntArraySortQuick(Arr);
  Len := Length(Sorted);
  if Len mod 2 = 1 then
    Result := Sorted[Len div 2]
  else
    Result := (Sorted[Len div 2 - 1] + Sorted[Len div 2]) / 2.0;
end;

function IntArrayMode(const Arr: TIntArray): Integer;
var
  I, MaxCount, CurrentCount, CurrentVal: Integer;
  Sorted: TIntArray;
begin
  if Length(Arr) = 0 then
  begin
    Result := 0;
    Exit;
  end;
  Sorted := IntArraySortQuick(Arr);
  Result := Sorted[0];
  MaxCount := 1;
  CurrentCount := 1;
  CurrentVal := Sorted[0];
  for I := 1 to High(Sorted) do
  begin
    if Sorted[I] = CurrentVal then
      Inc(CurrentCount)
    else
    begin
      if CurrentCount > MaxCount then
      begin
        MaxCount := CurrentCount;
        Result := CurrentVal;
      end;
      CurrentVal := Sorted[I];
      CurrentCount := 1;
    end;
  end;
  if CurrentCount > MaxCount then
    Result := CurrentVal;
end;

{===============================================================================
  统计函数 - Double
===============================================================================}

function DblArraySum(const Arr: TDoubleArray): Double;
var
  I: Integer;
begin
  Result := 0.0;
  for I := 0 to High(Arr) do
    Result := Result + Arr[I];
end;

function DblArrayProduct(const Arr: TDoubleArray): Double;
var
  I: Integer;
begin
  if Length(Arr) = 0 then
  begin
    Result := 0.0;
    Exit;
  end;
  Result := 1.0;
  for I := 0 to High(Arr) do
    Result := Result * Arr[I];
end;

function DblArrayAverage(const Arr: TDoubleArray): Double;
var
  I: Integer;
  Sum: Double;
begin
  if Length(Arr) = 0 then
  begin
    Result := 0.0;
    Exit;
  end;
  Sum := 0.0;
  for I := 0 to High(Arr) do
    Sum := Sum + Arr[I];
  Result := Sum / Length(Arr);
end;

function DblArrayMin(const Arr: TDoubleArray): Double;
var
  I: Integer;
begin
  if Length(Arr) = 0 then
  begin
    Result := 0.0;
    Exit;
  end;
  Result := Arr[0];
  for I := 1 to High(Arr) do
    if Arr[I] < Result then
      Result := Arr[I];
end;

function DblArrayMax(const Arr: TDoubleArray): Double;
var
  I: Integer;
begin
  if Length(Arr) = 0 then
  begin
    Result := 0.0;
    Exit;
  end;
  Result := Arr[0];
  for I := 1 to High(Arr) do
    if Arr[I] > Result then
      Result := Arr[I];
end;

function DblArrayMinMax(const Arr: TDoubleArray; out MinVal, MaxVal: Double): Boolean;
var
  I: Integer;
begin
  if Length(Arr) = 0 then
  begin
    MinVal := 0.0;
    MaxVal := 0.0;
    Result := False;
    Exit;
  end;
  MinVal := Arr[0];
  MaxVal := Arr[0];
  for I := 1 to High(Arr) do
  begin
    if Arr[I] < MinVal then MinVal := Arr[I];
    if Arr[I] > MaxVal then MaxVal := Arr[I];
  end;
  Result := True;
end;

function DblArrayRange(const Arr: TDoubleArray): Double;
var
  MinVal, MaxVal: Double;
begin
  if DblArrayMinMax(Arr, MinVal, MaxVal) then
    Result := MaxVal - MinVal
  else
    Result := 0.0;
end;

function DblArrayMedian(const Arr: TDoubleArray): Double;
var
  Sorted: TDoubleArray;
  Len, I, J: Integer;
  Temp: Double;
begin
  if Length(Arr) = 0 then
  begin
    Result := 0.0;
    Exit;
  end;
  // Sort copy using bubble sort for simplicity
  Sorted := DblArrayCopy(Arr);
  for I := 0 to Length(Sorted) - 2 do
    for J := 0 to Length(Sorted) - I - 2 do
      if Sorted[J] > Sorted[J + 1] then
      begin
        Temp := Sorted[J];
        Sorted[J] := Sorted[J + 1];
        Sorted[J + 1] := Temp;
      end;
  Len := Length(Sorted);
  if Len mod 2 = 1 then
    Result := Sorted[Len div 2]
  else
    Result := (Sorted[Len div 2 - 1] + Sorted[Len div 2]) / 2.0;
end;

function DblArrayStdDev(const Arr: TDoubleArray): Double;
var
  Mean, SumSquares: Double;
  I: Integer;
begin
  if Length(Arr) <= 1 then
  begin
    Result := 0.0;
    Exit;
  end;
  Mean := DblArrayAverage(Arr);
  SumSquares := 0.0;
  for I := 0 to High(Arr) do
    SumSquares := SumSquares + Sqr(Arr[I] - Mean);
  Result := Sqrt(SumSquares / Length(Arr));
end;

function DblArrayVariance(const Arr: TDoubleArray): Double;
var
  Mean, SumSquares: Double;
  I: Integer;
begin
  if Length(Arr) <= 1 then
  begin
    Result := 0.0;
    Exit;
  end;
  Mean := DblArrayAverage(Arr);
  SumSquares := 0.0;
  for I := 0 to High(Arr) do
    SumSquares := SumSquares + Sqr(Arr[I] - Mean);
  Result := SumSquares / Length(Arr);
end;

{===============================================================================
  数组转换 - Integer
===============================================================================}

function IntArrayReverse(const Arr: TIntArray): TIntArray;
var
  I, Len: Integer;
begin
  Len := Length(Arr);
  SetLength(Result, Len);
  for I := 0 to Len - 1 do
    Result[I] := Arr[Len - I - 1];
end;

procedure IntArrayReverseInPlace(var Arr: TIntArray);
var
  I, J, Temp: Integer;
begin
  I := 0;
  J := Length(Arr) - 1;
  while I < J do
  begin
    Temp := Arr[I];
    Arr[I] := Arr[J];
    Arr[J] := Temp;
    Inc(I);
    Dec(J);
  end;
end;

function IntArrayUnique(const Arr: TIntArray): TIntArray;
var
  I: Integer;
  Sorted, Temp: TIntArray;
begin
  if Length(Arr) = 0 then
  begin
    SetLength(Result, 0);
    Exit;
  end;
  Sorted := IntArraySortQuick(Arr);
  SetLength(Temp, 1);
  Temp[0] := Sorted[0];
  for I := 1 to High(Sorted) do
    if Sorted[I] <> Sorted[I - 1] then
      IntArrayAdd(Temp, Sorted[I]);
  Result := Temp;
end;

function IntArrayFill(Count: Integer; Value: Integer): TIntArray;
var
  I: Integer;
begin
  SetLength(Result, Count);
  for I := 0 to Count - 1 do
    Result[I] := Value;
end;

function IntArrayFillRange(StartVal, EndVal: Integer): TIntArray;
var
  I, Count: Integer;
begin
  if StartVal <= EndVal then
  begin
    Count := EndVal - StartVal + 1;
    SetLength(Result, Count);
    for I := 0 to Count - 1 do
      Result[I] := StartVal + I;
  end
  else
  begin
    Count := StartVal - EndVal + 1;
    SetLength(Result, Count);
    for I := 0 to Count - 1 do
      Result[I] := StartVal - I;
  end;
end;

function IntArrayFillRandom(Count: Integer; MinVal, MaxVal: Integer): TIntArray;
var
  I: Integer;
begin
  Randomize;
  SetLength(Result, Count);
  for I := 0 to Count - 1 do
    Result[I] := MinVal + Random(MaxVal - MinVal + 1);
end;

function IntArrayMap(const Arr: TIntArray; Multiplier: Integer; Offset: Integer = 0): TIntArray;
var
  I: Integer;
begin
  SetLength(Result, Length(Arr));
  for I := 0 to High(Arr) do
    Result[I] := Arr[I] * Multiplier + Offset;
end;

function IntArrayFilter(const Arr: TIntArray; MinVal, MaxVal: Integer): TIntArray;
var
  I: Integer;
begin
  SetLength(Result, 0);
  for I := 0 to High(Arr) do
    if (Arr[I] >= MinVal) and (Arr[I] <= MaxVal) then
      IntArrayAdd(Result, Arr[I]);
end;

{===============================================================================
  数组转换 - String
===============================================================================}

function StrArrayReverse(const Arr: TStringArray): TStringArray;
var
  I, Len: Integer;
begin
  Len := Length(Arr);
  SetLength(Result, Len);
  for I := 0 to Len - 1 do
    Result[I] := Arr[Len - I - 1];
end;

procedure StrArrayReverseInPlace(var Arr: TStringArray);
var
  I, J: Integer;
  Temp: string;
begin
  I := 0;
  J := Length(Arr) - 1;
  while I < J do
  begin
    Temp := Arr[I];
    Arr[I] := Arr[J];
    Arr[J] := Temp;
    Inc(I);
    Dec(J);
  end;
end;

function StrArrayUnique(const Arr: TStringArray; IgnoreCase: Boolean = False): TStringArray;
var
  I: Integer;
  Sorted, Temp: TStringArray;
begin
  if Length(Arr) = 0 then
  begin
    SetLength(Result, 0);
    Exit;
  end;
  Sorted := StrArraySort(Arr, IgnoreCase);
  SetLength(Temp, 1);
  Temp[0] := Sorted[0];
  for I := 1 to High(Sorted) do
  begin
    if IgnoreCase then
    begin
      if not SameText(Sorted[I], Sorted[I - 1]) then
        StrArrayAdd(Temp, Sorted[I]);
    end
    else
    begin
      if Sorted[I] <> Sorted[I - 1] then
        StrArrayAdd(Temp, Sorted[I]);
    end;
  end;
  Result := Temp;
end;

function StrArrayFill(Count: Integer; const Value: string): TStringArray;
var
  I: Integer;
begin
  SetLength(Result, Count);
  for I := 0 to Count - 1 do
    Result[I] := Value;
end;

{===============================================================================
  集合操作 - Integer
===============================================================================}

function IntArrayUnion(const Arr1, Arr2: TIntArray): TIntArray;
var
  I: Integer;
  Temp: TIntArray;
begin
  Temp := IntArrayCopy(Arr1);
  for I := 0 to High(Arr2) do
    if not IntArrayContains(Temp, Arr2[I]) then
      IntArrayAdd(Temp, Arr2[I]);
  Result := Temp;
end;

function IntArrayIntersect(const Arr1, Arr2: TIntArray): TIntArray;
var
  I: Integer;
begin
  SetLength(Result, 0);
  for I := 0 to High(Arr1) do
    if IntArrayContains(Arr2, Arr1[I]) and not IntArrayContains(Result, Arr1[I]) then
      IntArrayAdd(Result, Arr1[I]);
end;

function IntArrayDifference(const Arr1, Arr2: TIntArray): TIntArray;
var
  I: Integer;
begin
  SetLength(Result, 0);
  for I := 0 to High(Arr1) do
    if not IntArrayContains(Arr2, Arr1[I]) then
      IntArrayAdd(Result, Arr1[I]);
end;

function IntArraySymmetricDifference(const Arr1, Arr2: TIntArray): TIntArray;
var
  Diff1, Diff2: TIntArray;
begin
  Diff1 := IntArrayDifference(Arr1, Arr2);
  Diff2 := IntArrayDifference(Arr2, Arr1);
  Result := IntArrayUnion(Diff1, Diff2);
end;

function IntArrayIsSubset(const SubArr, MainArr: TIntArray): Boolean;
var
  I: Integer;
begin
  for I := 0 to High(SubArr) do
    if not IntArrayContains(MainArr, SubArr[I]) then
    begin
      Result := False;
      Exit;
    end;
  Result := True;
end;

function IntArrayIsDisjoint(const Arr1, Arr2: TIntArray): Boolean;
var
  I: Integer;
begin
  for I := 0 to High(Arr1) do
    if IntArrayContains(Arr2, Arr1[I]) then
    begin
      Result := False;
      Exit;
    end;
  Result := True;
end;

{===============================================================================
  集合操作 - String
===============================================================================}

function StrArrayUnion(const Arr1, Arr2: TStringArray; IgnoreCase: Boolean = False): TStringArray;
var
  I: Integer;
  Temp: TStringArray;
begin
  Temp := StrArrayCopy(Arr1);
  for I := 0 to High(Arr2) do
    if not StrArrayContains(Temp, Arr2[I], IgnoreCase) then
      StrArrayAdd(Temp, Arr2[I]);
  Result := Temp;
end;

function StrArrayIntersect(const Arr1, Arr2: TStringArray; IgnoreCase: Boolean = False): TStringArray;
var
  I: Integer;
begin
  SetLength(Result, 0);
  for I := 0 to High(Arr1) do
    if StrArrayContains(Arr2, Arr1[I], IgnoreCase) and not StrArrayContains(Result, Arr1[I], IgnoreCase) then
      StrArrayAdd(Result, Arr1[I]);
end;

function StrArrayDifference(const Arr1, Arr2: TStringArray; IgnoreCase: Boolean = False): TStringArray;
var
  I: Integer;
begin
  SetLength(Result, 0);
  for I := 0 to High(Arr1) do
    if not StrArrayContains(Arr2, Arr1[I], IgnoreCase) then
      StrArrayAdd(Result, Arr1[I]);
end;

function StrArraySymmetricDifference(const Arr1, Arr2: TStringArray; IgnoreCase: Boolean = False): TStringArray;
var
  Diff1, Diff2: TStringArray;
begin
  Diff1 := StrArrayDifference(Arr1, Arr2, IgnoreCase);
  Diff2 := StrArrayDifference(Arr2, Arr1, IgnoreCase);
  Result := StrArrayUnion(Diff1, Diff2, IgnoreCase);
end;

function StrArrayIsSubset(const SubArr, MainArr: TStringArray; IgnoreCase: Boolean = False): Boolean;
var
  I: Integer;
begin
  for I := 0 to High(SubArr) do
    if not StrArrayContains(MainArr, SubArr[I], IgnoreCase) then
    begin
      Result := False;
      Exit;
    end;
  Result := True;
end;

{===============================================================================
  分区与分块
===============================================================================}

function IntArrayChunk(const Arr: TIntArray; ChunkSize: Integer): array of TIntArray;
var
  I, ChunkCount, Remainder: Integer;
begin
  if (ChunkSize <= 0) or (Length(Arr) = 0) then
  begin
    SetLength(Result, 0);
    Exit;
  end;
  ChunkCount := Length(Arr) div ChunkSize;
  Remainder := Length(Arr) mod ChunkSize;
  if Remainder > 0 then
    Inc(ChunkCount);
  SetLength(Result, ChunkCount);
  for I := 0 to ChunkCount - 1 do
    Result[I] := IntArraySlice(Arr, I * ChunkSize, ChunkSize);
end;

function StrArrayChunk(const Arr: TStringArray; ChunkSize: Integer): array of TStringArray;
var
  I, ChunkCount, Remainder: Integer;
begin
  if (ChunkSize <= 0) or (Length(Arr) = 0) then
  begin
    SetLength(Result, 0);
    Exit;
  end;
  ChunkCount := Length(Arr) div ChunkSize;
  Remainder := Length(Arr) mod ChunkSize;
  if Remainder > 0 then
    Inc(ChunkCount);
  SetLength(Result, ChunkCount);
  for I := 0 to ChunkCount - 1 do
    Result[I] := StrArraySlice(Arr, I * ChunkSize, ChunkSize);
end;

function IntArrayPartition(const Arr: TIntArray; Pivot: Integer): array of TIntArray;
var
  I: Integer;
begin
  SetLength(Result, 2);
  SetLength(Result[0], 0);
  SetLength(Result[1], 0);
  for I := 0 to High(Arr) do
  begin
    if Arr[I] < Pivot then
      IntArrayAdd(Result[0], Arr[I])
    else
      IntArrayAdd(Result[1], Arr[I]);
  end;
end;

function StrArrayPartitionByLength(const Arr: TStringArray; MaxLength: Integer): TStringArray;
var
  I: Integer;
  CurrentStr: string;
begin
  SetLength(Result, 0);
  if Length(Arr) = 0 then Exit;
  CurrentStr := Arr[0];
  for I := 1 to High(Arr) do
  begin
    if Length(CurrentStr) + Length(Arr[I]) + 1 <= MaxLength then
      CurrentStr := CurrentStr + ',' + Arr[I]
    else
    begin
      StrArrayAdd(Result, CurrentStr);
      CurrentStr := Arr[I];
    end;
  end;
  if CurrentStr <> '' then
    StrArrayAdd(Result, CurrentStr);
end;

{===============================================================================
  数组验证与比较
===============================================================================}

function IntArrayEquals(const Arr1, Arr2: TIntArray): Boolean;
var
  I: Integer;
begin
  if Length(Arr1) <> Length(Arr2) then
  begin
    Result := False;
    Exit;
  end;
  for I := 0 to High(Arr1) do
    if Arr1[I] <> Arr2[I] then
    begin
      Result := False;
      Exit;
    end;
  Result := True;
end;

function StrArrayEquals(const Arr1, Arr2: TStringArray; IgnoreCase: Boolean = False): Boolean;
var
  I: Integer;
begin
  if Length(Arr1) <> Length(Arr2) then
  begin
    Result := False;
    Exit;
  end;
  for I := 0 to High(Arr1) do
  begin
    if IgnoreCase then
    begin
      if not SameText(Arr1[I], Arr2[I]) then
      begin
        Result := False;
        Exit;
      end;
    end
    else
    begin
      if Arr1[I] <> Arr2[I] then
      begin
        Result := False;
        Exit;
      end;
    end;
  end;
  Result := True;
end;

function IntArrayIsEmpty(const Arr: TIntArray): Boolean;
begin
  Result := Length(Arr) = 0;
end;

function StrArrayIsEmpty(const Arr: TStringArray): Boolean;
begin
  Result := Length(Arr) = 0;
end;

function IntArrayAllSame(const Arr: TIntArray): Boolean;
var
  I: Integer;
begin
  if Length(Arr) <= 1 then
  begin
    Result := True;
    Exit;
  end;
  for I := 1 to High(Arr) do
    if Arr[I] <> Arr[0] then
    begin
      Result := False;
      Exit;
    end;
  Result := True;
end;

function StrArrayAllSame(const Arr: TStringArray; IgnoreCase: Boolean = False): Boolean;
var
  I: Integer;
begin
  if Length(Arr) <= 1 then
  begin
    Result := True;
    Exit;
  end;
  for I := 1 to High(Arr) do
  begin
    if IgnoreCase then
    begin
      if not SameText(Arr[I], Arr[0]) then
      begin
        Result := False;
        Exit;
      end;
    end
    else
    begin
      if Arr[I] <> Arr[0] then
      begin
        Result := False;
        Exit;
      end;
    end;
  end;
  Result := True;
end;

function IntArrayIsSorted(const Arr: TIntArray): Boolean;
var
  I: Integer;
begin
  if Length(Arr) <= 1 then
  begin
    Result := True;
    Exit;
  end;
  for I := 0 to Length(Arr) - 2 do
    if Arr[I] > Arr[I + 1] then
    begin
      Result := False;
      Exit;
    end;
  Result := True;
end;

function StrArrayIsSorted(const Arr: TStringArray; IgnoreCase: Boolean = False): Boolean;
var
  I: Integer;
begin
  if Length(Arr) <= 1 then
  begin
    Result := True;
    Exit;
  end;
  for I := 0 to Length(Arr) - 2 do
  begin
    if IgnoreCase then
    begin
      if CompareText(Arr[I], Arr[I + 1]) > 0 then
      begin
        Result := False;
        Exit;
      end;
    end
    else
    begin
      if CompareStr(Arr[I], Arr[I + 1]) > 0 then
      begin
        Result := False;
        Exit;
      end;
    end;
  end;
  Result := True;
end;

{===============================================================================
  字符串与数组互转
===============================================================================}

function IntArrayToString(const Arr: TIntArray; const Delimiter: string = ','): string;
var
  I: Integer;
begin
  if Length(Arr) = 0 then
  begin
    Result := '';
    Exit;
  end;
  Result := IntToStr(Arr[0]);
  for I := 1 to High(Arr) do
    Result := Result + Delimiter + IntToStr(Arr[I]);
end;

function IntArrayFromString(const S: string; const Delimiter: string = ','): TIntArray;
var
  Parts: TStringList;
  I: Integer;
begin
  SetLength(Result, 0);
  if S = '' then Exit;
  Parts := TStringList.Create;
  try
    Parts.Delimiter := Delimiter[1];
    Parts.StrictDelimiter := True;
    Parts.DelimitedText := S;
    SetLength(Result, Parts.Count);
    for I := 0 to Parts.Count - 1 do
      Result[I] := StrToIntDef(Trim(Parts[I]), 0);
  finally
    Parts.Free;
  end;
end;

function StrArrayToString(const Arr: TStringArray; const Delimiter: string = ','): string;
var
  I: Integer;
begin
  if Length(Arr) = 0 then
  begin
    Result := '';
    Exit;
  end;
  Result := Arr[0];
  for I := 1 to High(Arr) do
    Result := Result + Delimiter + Arr[I];
end;

function StrArrayFromString(const S: string; const Delimiter: string = ','): TStringArray;
var
  Parts: TStringList;
  I: Integer;
begin
  SetLength(Result, 0);
  if S = '' then Exit;
  Parts := TStringList.Create;
  try
    Parts.Delimiter := Delimiter[1];
    Parts.StrictDelimiter := True;
    Parts.DelimitedText := S;
    SetLength(Result, Parts.Count);
    for I := 0 to Parts.Count - 1 do
      Result[I] := Parts[I];
  finally
    Parts.Free;
  end;
end;

{===============================================================================
  特殊操作
===============================================================================}

function IntArrayRotateLeft(const Arr: TIntArray; Positions: Integer): TIntArray;
var
  I, Len, Pos: Integer;
begin
  Len := Length(Arr);
  if Len <= 1 then
  begin
    Result := IntArrayCopy(Arr);
    Exit;
  end;
  Pos := Positions mod Len;
  if Pos < 0 then Pos := Pos + Len;
  SetLength(Result, Len);
  for I := 0 to Len - 1 do
    Result[I] := Arr[(I + Pos) mod Len];
end;

function IntArrayRotateRight(const Arr: TIntArray; Positions: Integer): TIntArray;
begin
  Result := IntArrayRotateLeft(Arr, -Positions);
end;

function IntArrayShuffle(const Arr: TIntArray): TIntArray;
var
  I, J, Temp: Integer;
begin
  Result := IntArrayCopy(Arr);
  Randomize;
  for I := Length(Result) - 1 downto 1 do
  begin
    J := Random(I + 1);
    Temp := Result[I];
    Result[I] := Result[J];
    Result[J] := Temp;
  end;
end;

function StrArrayShuffle(const Arr: TStringArray): TStringArray;
var
  I, J: Integer;
  Temp: string;
begin
  Result := StrArrayCopy(Arr);
  Randomize;
  for I := Length(Result) - 1 downto 1 do
  begin
    J := Random(I + 1);
    Temp := Result[I];
    Result[I] := Result[J];
    Result[J] := Temp;
  end;
end;

function IntArraySample(const Arr: TIntArray; Count: Integer): TIntArray;
var
  Shuffled: TIntArray;
  I: Integer;
begin
  if Count > Length(Arr) then
    Count := Length(Arr);
  if Count <= 0 then
  begin
    SetLength(Result, 0);
    Exit;
  end;
  Shuffled := IntArrayShuffle(Arr);
  SetLength(Result, Count);
  for I := 0 to Count - 1 do
    Result[I] := Shuffled[I];
end;

function StrArraySample(const Arr: TStringArray; Count: Integer): TStringArray;
var
  Shuffled: TStringArray;
  I: Integer;
begin
  if Count > Length(Arr) then
    Count := Length(Arr);
  if Count <= 0 then
  begin
    SetLength(Result, 0);
    Exit;
  end;
  Shuffled := StrArrayShuffle(Arr);
  SetLength(Result, Count);
  for I := 0 to Count - 1 do
    Result[I] := Shuffled[I];
end;

end.