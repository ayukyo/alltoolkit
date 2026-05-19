{*******************************************************************************
  AllToolkit - Delphi Prime Number Utilities
  
  一个零依赖的质数工具库，适用于 Delphi 7+ 和 Free Pascal
  
  功能包括：
  - 质数检测（确定性 Miller-Rabin）
  - 质数生成
  - 质因数分解
  - 最大公约数 / 最小公倍数
  - 欧拉函数
  - 质数计数函数（π函数）
  - 筛法（埃拉托斯特尼筛法）
  - 孪生质数检测
  - 回文质数检测
  - 安全质数检测
  
  作者：AllToolkit Contributors
  许可证：MIT
********************************************************************************}

unit mod;

interface

{===============================================================================
  基本质数检测
===============================================================================}
function IsPrime(N: Int64): Boolean;
function IsPrimeTrial(N: Int64): Boolean;

{===============================================================================
  Miller-Rabin 质数检测（确定性版本）
===============================================================================}
function IsPrimeMillerRabin(N: Int64): Boolean;

{===============================================================================
  质数生成
===============================================================================}
function NextPrime(N: Int64): Int64;
function PrevPrime(N: Int64): Int64;
function NthPrime(N: Integer): Int64;
function GeneratePrimes(Start, Count: Integer): TStringList;

{===============================================================================
  质因数分解
===============================================================================}
function PrimeFactors(N: Int64): TStringList;
function PrimeFactorization(N: Int64): TStringList;
function DistinctPrimeFactors(N: Int64): TStringList;

{===============================================================================
  最大公约数 / 最小公倍数
===============================================================================}
function GCD(A, B: Int64): Int64;
function LCM(A, B: Int64): Int64;
function GCDArray(const Values: array of Int64): Int64;
function LCMArray(const Values: array of Int64): Int64;

{===============================================================================
  欧拉函数
===============================================================================}
function EulerPhi(N: Int64): Int64;

{===============================================================================
  质数计数
===============================================================================}
function PrimeCount(N: Int64): Int64;
function CountPrimesInRange(Start, Finish: Int64): Int64;

{===============================================================================
  筛法
===============================================================================}
function SieveOfEratosthenes(Limit: Integer): TStringList;
function SieveRange(Start, Finish: Integer): TStringList;

{===============================================================================
  特殊质数类型
===============================================================================}
function IsTwinPrime(N: Int64): Boolean;
function GetTwinPrimePair(N: Int64): TStringList;
function IsPalindromePrime(N: Int64): Boolean;
function IsSafePrime(N: Int64): Boolean;
function IsSophieGermainPrime(N: Int64): Boolean;
function IsEmirp(N: Int64): Boolean;

{===============================================================================
  其他工具
===============================================================================}
function ModExp(Base, Exponent, Modulus: Int64): Int64;
function IsPerfectSquare(N: Int64): Boolean;
function LegendreSymbol(A, P: Int64): Integer;

implementation

uses
  SysUtils, Classes;

const
  // Deterministic Miller-Rabin witnesses for n < 2^64
  MR_WITNESSES: array[0..11] of Int64 = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37);

{===============================================================================
  辅助函数
===============================================================================}

function IntToStr64(N: Int64): string;
begin
  Result := IntToStr(N);
end;

function IsPerfectSquare(N: Int64): Boolean;
var
  Root: Int64;
begin
  if N < 0 then
  begin
    Result := False;
    Exit;
  end;
  Root := Trunc(Sqrt(N * 1.0));
  Result := (Root * Root = N) or ((Root + 1) * (Root + 1) = N);
end;

function ModExp(Base, Exponent, Modulus: Int64): Int64;
var
  Result64: Int64;
  Base64: Int64;
begin
  if Modulus = 1 then
  begin
    Result := 0;
    Exit;
  end;
  Result64 := 1;
  Base64 := Base mod Modulus;
  while Exponent > 0 do
  begin
    if Exponent and 1 = 1 then
      Result64 := (Result64 * Base64) mod Modulus;
    Exponent := Exponent shr 1;
    Base64 := (Base64 * Base64) mod Modulus;
  end;
  Result := Result64;
end;

{===============================================================================
  基本质数检测
===============================================================================}

function IsPrimeTrial(N: Int64): Boolean;
var
  I: Int64;
begin
  if N < 2 then
  begin
    Result := False;
    Exit;
  end;
  if N = 2 then
  begin
    Result := True;
    Exit;
  end;
  if (N mod 2 = 0) or (N = 1) then
  begin
    Result := False;
    Exit;
  end;
  I := 3;
  while I * I <= N do
  begin
    if N mod I = 0 then
    begin
      Result := False;
      Exit;
    end;
    I := I + 2;
  end;
  Result := True;
end;

function IsPrimeMillerRabin(N: Int64): Boolean;
var
  D, S, X, A: Int64;
  I, J: Integer;
begin
  // Handle small cases
  if N < 2 then
  begin
    Result := False;
    Exit;
  end;
  if N = 2 then
  begin
    Result := True;
    Exit;
  end;
  if (N mod 2 = 0) then
  begin
    Result := False;
    Exit;
  end;
  if N < 9 then
  begin
    Result := True;  // 3, 5, 7 are prime
    Exit;
  end;
  if N mod 3 = 0 then
  begin
    Result := False;
    Exit;
  end;

  // Write n-1 as 2^s * d
  D := N - 1;
  S := 0;
  while D mod 2 = 0 do
  begin
    D := D div 2;
    Inc(S);
  end;

  // Test with deterministic witnesses for n < 2^64
  for I := 0 to High(MR_WITNESSES) do
  begin
    A := MR_WITNESSES[I];
    if A >= N then
      Continue;
    
    X := ModExp(A, D, N);
    
    if (X = 1) or (X = N - 1) then
      Continue;
    
    for J := 0 to S - 2 do
    begin
      X := ModExp(X, 2, N);
      if X = N - 1 then
        Break;
    end;
    
    if X <> N - 1 then
    begin
      Result := False;
      Exit;
    end;
  end;
  
  Result := True;
end;

function IsPrime(N: Int64): Boolean;
begin
  Result := IsPrimeMillerRabin(N);
end;

{===============================================================================
  质数生成
===============================================================================}

function NextPrime(N: Int64): Int64;
begin
  if N < 2 then
  begin
    Result := 2;
    Exit;
  end;
  Result := N + 1;
  if Result mod 2 = 0 then
    Inc(Result);
  while not IsPrime(Result) do
    Inc(Result, 2);
end;

function PrevPrime(N: Int64): Int64;
begin
  if N <= 2 then
  begin
    Result := -1;  // No prime less than 2
    Exit;
  end;
  if N = 3 then
  begin
    Result := 2;
    Exit;
  end;
  Result := N - 1;
  if Result mod 2 = 0 then
    Dec(Result);
  while (Result >= 2) and not IsPrime(Result) do
    Dec(Result, 2);
  if Result < 2 then
    Result := -1;
end;

function NthPrime(N: Integer): Int64;
var
  Count: Integer;
  Candidate: Int64;
begin
  if N < 1 then
  begin
    Result := -1;
    Exit;
  end;
  if N = 1 then
  begin
    Result := 2;
    Exit;
  end;
  Count := 1;
  Candidate := 1;
  while Count < N do
  begin
    Candidate := Candidate + 2;
    if IsPrime(Candidate) then
      Inc(Count);
  end;
  Result := Candidate;
end;

function GeneratePrimes(Start, Count: Integer): TStringList;
var
  List: TStringList;
  Generated: Integer;
  Candidate: Int64;
begin
  List := TStringList.Create;
  Generated := 0;
  Candidate := Start;
  
  // Find first prime >= Start
  if Candidate < 2 then
    Candidate := 2;
  if (Candidate > 2) and (Candidate mod 2 = 0) then
    Inc(Candidate);
  while not IsPrime(Candidate) do
    Inc(Candidate, 2);
  
  while Generated < Count do
  begin
    List.Add(IntToStr64(Candidate));
    Inc(Generated);
    Candidate := NextPrime(Candidate);
  end;
  
  Result := List;
end;

{===============================================================================
  质因数分解
===============================================================================}

function PrimeFactors(N: Int64): TStringList;
var
  List: TStringList;
  I: Int64;
begin
  List := TStringList.Create;
  if N < 2 then
  begin
    Result := List;
    Exit;
  end;
  
  // Handle factor 2
  while N mod 2 = 0 do
  begin
    List.Add('2');
    N := N div 2;
  end;
  
  // Handle odd factors
  I := 3;
  while I * I <= N do
  begin
    while N mod I = 0 do
    begin
      List.Add(IntToStr64(I));
      N := N div I;
    end;
    I := I + 2;
  end;
  
  // If N is still > 1, it's a prime factor
  if N > 1 then
    List.Add(IntToStr64(N));
  
  Result := List;
end;

function PrimeFactorization(N: Int64): TStringList;
var
  List: TStringList;
  Factors: TStringList;
  I: Integer;
  CurrentFactor: string;
  Count: Integer;
begin
  List := TStringList.Create;
  if N < 2 then
  begin
    Result := List;
    Exit;
  end;
  
  Factors := PrimeFactors(N);
  try
    if Factors.Count = 0 then
    begin
      Result := List;
      Exit;
    end;
    
    CurrentFactor := Factors[0];
    Count := 1;
    
    for I := 1 to Factors.Count - 1 do
    begin
      if Factors[I] = CurrentFactor then
        Inc(Count)
      else
      begin
        if Count = 1 then
          List.Add(CurrentFactor)
        else
          List.Add(CurrentFactor + '^' + IntToStr(Count));
        CurrentFactor := Factors[I];
        Count := 1;
      end;
    end;
    
    // Add the last factor
    if Count = 1 then
      List.Add(CurrentFactor)
    else
      List.Add(CurrentFactor + '^' + IntToStr(Count));
  finally
    Factors.Free;
  end;
  
  Result := List;
end;

function DistinctPrimeFactors(N: Int64): TStringList;
var
  List: TStringList;
  Factors: TStringList;
  I: Integer;
  LastFactor: string;
begin
  List := TStringList.Create;
  if N < 2 then
  begin
    Result := List;
    Exit;
  end;
  
  Factors := PrimeFactors(N);
  try
    LastFactor := '';
    for I := 0 to Factors.Count - 1 do
    begin
      if Factors[I] <> LastFactor then
      begin
        List.Add(Factors[I]);
        LastFactor := Factors[I];
      end;
    end;
  finally
    Factors.Free;
  end;
  
  Result := List;
end;

{===============================================================================
  最大公约数 / 最小公倍数
===============================================================================}

function GCD(A, B: Int64): Int64;
var
  Temp: Int64;
begin
  if A < 0 then A := -A;
  if B < 0 then B := -B;
  
  while B <> 0 do
  begin
    Temp := B;
    B := A mod B;
    A := Temp;
  end;
  Result := A;
end;

function LCM(A, B: Int64): Int64;
var
  G: Int64;
begin
  if A = 0 then A := 1;
  if B = 0 then B := 1;
  if A < 0 then A := -A;
  if B < 0 then B := -B;
  
  G := GCD(A, B);
  Result := (A div G) * B;
end;

function GCDArray(const Values: array of Int64): Int64;
var
  I: Integer;
begin
  if Length(Values) = 0 then
  begin
    Result := 0;
    Exit;
  end;
  
  Result := Values[0];
  for I := 1 to High(Values) do
    Result := GCD(Result, Values[I]);
end;

function LCMArray(const Values: array of Int64): Int64;
var
  I: Integer;
begin
  if Length(Values) = 0 then
  begin
    Result := 0;
    Exit;
  end;
  
  Result := Values[0];
  for I := 1 to High(Values) do
    Result := LCM(Result, Values[I]);
end;

{===============================================================================
  欧拉函数
===============================================================================}

function EulerPhi(N: Int64): Int64;
var
  Factors: TStringList;
  I: Integer;
  P: Int64;
  LastFactor: string;
begin
  if N < 1 then
  begin
    Result := 0;
    Exit;
  end;
  if N = 1 then
  begin
    Result := 1;
    Exit;
  end;
  
  Result := N;
  Factors := DistinctPrimeFactors(N);
  try
    for I := 0 to Factors.Count - 1 do
    begin
      P := StrToInt64(Factors[I]);
      Result := Result div P * (P - 1);
    end;
  finally
    Factors.Free;
  end;
end;

{===============================================================================
  质数计数
===============================================================================}

function PrimeCount(N: Int64): Int64;
var
  I: Int64;
begin
  Result := 0;
  if N < 2 then
    Exit;
  
  // Count 2
  if N >= 2 then
    Inc(Result);
  
  // Count odd primes
  I := 3;
  while I <= N do
  begin
    if IsPrime(I) then
      Inc(Result);
    I := I + 2;
  end;
end;

function CountPrimesInRange(Start, Finish: Int64): Int64;
var
  I: Int64;
begin
  Result := 0;
  I := Start;
  
  if I < 2 then
    I := 2;
  
  if (I = 2) and (Finish >= 2) then
  begin
    Inc(Result);
    I := 3;
  end;
  
  if I mod 2 = 0 then
    Inc(I);
  
  while I <= Finish do
  begin
    if IsPrime(I) then
      Inc(Result);
    I := I + 2;
  end;
end;

{===============================================================================
  筛法
===============================================================================}

function SieveOfEratosthenes(Limit: Integer): TStringList;
var
  List: TStringList;
  Sieve: array of Boolean;
  I, J: Integer;
begin
  List := TStringList.Create;
  
  if Limit < 2 then
  begin
    Result := List;
    Exit;
  end;
  
  SetLength(Sieve, Limit + 1);
  for I := 0 to Limit do
    Sieve[I] := True;
  
  Sieve[0] := False;
  Sieve[1] := False;
  
  I := 2;
  while I * I <= Limit do
  begin
    if Sieve[I] then
    begin
      J := I * I;
      while J <= Limit do
      begin
        Sieve[J] := False;
        J := J + I;
      end;
    end;
    Inc(I);
  end;
  
  for I := 2 to Limit do
    if Sieve[I] then
      List.Add(IntToStr(I));
  
  Result := List;
end;

function SieveRange(Start, Finish: Integer): TStringList;
var
  List: TStringList;
  I: Int64;
begin
  List := TStringList.Create;
  
  if Finish < Start then
  begin
    Result := List;
    Exit;
  end;
  
  if Start < 2 then
    Start := 2;
  
  I := Start;
  
  // Handle 2 specially
  if (I <= 2) and (Finish >= 2) then
  begin
    List.Add('2');
    I := 3;
  end;
  
  if I mod 2 = 0 then
    Inc(I);
  
  while I <= Finish do
  begin
    if IsPrime(I) then
      List.Add(IntToStr64(I));
    I := I + 2;
  end;
  
  Result := List;
end;

{===============================================================================
  特殊质数类型
===============================================================================}

function IsTwinPrime(N: Int64): Boolean;
begin
  if not IsPrime(N) then
  begin
    Result := False;
    Exit;
  end;
  Result := IsPrime(N - 2) or IsPrime(N + 2);
end;

function GetTwinPrimePair(N: Int64): TStringList;
var
  List: TStringList;
begin
  List := TStringList.Create;
  
  if not IsPrime(N) then
  begin
    Result := List;
    Exit;
  end;
  
  if IsPrime(N - 2) then
  begin
    List.Add(IntToStr64(N - 2));
    List.Add(IntToStr64(N));
  end
  else if IsPrime(N + 2) then
  begin
    List.Add(IntToStr64(N));
    List.Add(IntToStr64(N + 2));
  end;
  
  Result := List;
end;

function ReverseNumber(N: Int64): Int64;
var
  Temp: Int64;
begin
  Temp := 0;
  while N > 0 do
  begin
    Temp := Temp * 10 + (N mod 10);
    N := N div 10;
  end;
  Result := Temp;
end;

function IsPalindromePrime(N: Int64): Boolean;
begin
  if not IsPrime(N) then
  begin
    Result := False;
    Exit;
  end;
  Result := N = ReverseNumber(N);
end;

function IsSafePrime(N: Int64): Boolean;
begin
  if not IsPrime(N) then
  begin
    Result := False;
    Exit;
  end;
  Result := IsPrime((N - 1) div 2);
end;

function IsSophieGermainPrime(N: Int64): Boolean;
begin
  if not IsPrime(N) then
  begin
    Result := False;
    Exit;
  end;
  Result := IsPrime(2 * N + 1);
end;

function IsEmirp(N: Int64): Boolean;
var
  Reversed: Int64;
begin
  if not IsPrime(N) then
  begin
    Result := False;
    Exit;
  end;
  Reversed := ReverseNumber(N);
  // An emirp is a prime that gives a different prime when reversed
  Result := (Reversed <> N) and IsPrime(Reversed);
end;

{===============================================================================
  其他工具
===============================================================================}

function LegendreSymbol(A, P: Int64): Integer;
var
  Result64: Int64;
begin
  if P <= 0 then
  begin
    Result := 0;
    Exit;
  end;
  
  // P must be an odd prime
  if not IsPrime(P) or (P = 2) then
  begin
    Result := 0;
    Exit;
  end;
  
  A := A mod P;
  if A < 0 then
    A := A + P;
  
  if A = 0 then
  begin
    Result := 0;
    Exit;
  end;
  
  Result64 := ModExp(A, (P - 1) div 2, P);
  
  if Result64 = 1 then
    Result := 1
  else if Result64 = P - 1 then
    Result := -1
  else
    Result := 0;
end;

end.