{*******************************************************************************
  AllToolkit - Delphi Prime Utilities Examples
  
  示例程序：展示质数工具库的主要功能
  
  运行方式：
  - Delphi: 在IDE中打开并运行
  - Free Pascal: fpc prime_examples.pas && ./prime_examples
********************************************************************************}

program prime_examples;

{$IFDEF FPC}
  {$MODE DELPHI}
{$ENDIF}

uses
  SysUtils, Classes, mod;

procedure PrintList(List: TStringList);
var
  I: Integer;
begin
  for I := 0 to List.Count - 1 do
    Write(List[I], ' ');
  WriteLn('');
end;

procedure Example_BasicPrimeDetection;
begin
  WriteLn('=== 基本质数检测 ===');
  WriteLn('IsPrime(17): ', IsPrime(17));
  WriteLn('IsPrime(25): ', IsPrime(25));
  WriteLn('IsPrime(7919): ', IsPrime(7919));  // 第1000个质数
  WriteLn('');
end;

procedure Example_PrimeGeneration;
var
  Primes: TStringList;
begin
  WriteLn('=== 质数生成 ===');
  WriteLn('NextPrime(100): ', NextPrime(100));
  WriteLn('PrevPrime(100): ', PrevPrime(100));
  WriteLn('NthPrime(25): ', NthPrime(25));
  WriteLn('NthPrime(100): ', NthPrime(100));
  WriteLn('');
  
  WriteLn('生成前10个质数:');
  Primes := GeneratePrimes(1, 10);
  PrintList(Primes);
  Primes.Free;
  WriteLn('');
end;

procedure Example_GCDAndLCM;
begin
  WriteLn('=== 最大公约数和最小公倍数 ===');
  WriteLn('GCD(48, 18): ', GCD(48, 18));
  WriteLn('LCM(4, 6): ', LCM(4, 6));
  WriteLn('GCDArray([24, 36, 48]): ', GCDArray([24, 36, 48]));
  WriteLn('LCMArray([2, 3, 4, 5]): ', LCMArray([2, 3, 4, 5]));
  WriteLn('');
end;

procedure Example_PrimeFactorization;
var
  Factors: TStringList;
begin
  WriteLn('=== 质因数分解 ===');
  WriteLn('分解 360:');
  Write('质因数: ');
  Factors := PrimeFactors(360);
  PrintList(Factors);
  Factors.Free;
  
  Write('分解形式: ');
  Factors := PrimeFactorization(360);
  PrintList(Factors);
  Factors.Free;
  
  Write('不同质因数: ');
  Factors := DistinctPrimeFactors(360);
  PrintList(Factors);
  Factors.Free;
  WriteLn('');
end;

procedure Example_EulerPhi;
begin
  WriteLn('=== 欧拉函数 ===');
  WriteLn('EulerPhi(1): ', EulerPhi(1));
  WriteLn('EulerPhi(10): ', EulerPhi(10));
  WriteLn('EulerPhi(30): ', EulerPhi(30));
  WriteLn('EulerPhi(100): ', EulerPhi(100));
  WriteLn('');
end;

procedure Example_Sieve;
var
  Primes: TStringList;
begin
  WriteLn('=== 埃拉托斯特尼筛法 ===');
  WriteLn('筛法生成100以内的质数:');
  Primes := SieveOfEratosthenes(100);
  PrintList(Primes);
  WriteLn('质数总数: ', Primes.Count);
  Primes.Free;
  WriteLn('');
  
  WriteLn('筛选50到100之间的质数:');
  Primes := SieveRange(50, 100);
  PrintList(Primes);
  Primes.Free;
  WriteLn('');
end;

procedure Example_PrimeCount;
begin
  WriteLn('=== 质数计数 ===');
  WriteLn('PrimeCount(10): ', PrimeCount(10));
  WriteLn('PrimeCount(100): ', PrimeCount(100));
  WriteLn('PrimeCount(1000): ', PrimeCount(1000));
  WriteLn('CountPrimesInRange(50, 100): ', CountPrimesInRange(50, 100));
  WriteLn('');
end;

procedure Example_SpecialPrimes;
begin
  WriteLn('=== 特殊质数类型 ===');
  WriteLn('--- 孪生质数 ---');
  WriteLn('IsTwinPrime(11): ', IsTwinPrime(11));
  WriteLn('IsTwinPrime(23): ', IsTwinPrime(23));
  WriteLn('');
  
  WriteLn('--- 回文质数 ---');
  WriteLn('IsPalindromePrime(101): ', IsPalindromePrime(101));
  WriteLn('IsPalindromePrime(131): ', IsPalindromePrime(131));
  WriteLn('');
  
  WriteLn('--- 安全质数 ---');
  WriteLn('IsSafePrime(5): ', IsSafePrime(5));
  WriteLn('IsSafePrime(7): ', IsSafePrime(7));
  WriteLn('');
  
  WriteLn('--- Sophie Germain质数 ---');
  WriteLn('IsSophieGermainPrime(2): ', IsSophieGermainPrime(2));
  WriteLn('IsSophieGermainPrime(11): ', IsSophieGermainPrime(11));
  WriteLn('');
  
  WriteLn('--- Emirp质数 ---');
  WriteLn('IsEmirp(13): ', IsEmirp(13));  // 13 -> 31
  WriteLn('IsEmirp(17): ', IsEmirp(17));  // 17 -> 71
  WriteLn('');
end;

procedure Example_ModExp;
begin
  WriteLn('=== 模幂运算 ===');
  WriteLn('ModExp(2, 10, 100): ', ModExp(2, 10, 100));
  WriteLn('ModExp(7, 256, 13): ', ModExp(7, 256, 13));
  WriteLn('');
end;

procedure Example_LegendreSymbol;
begin
  WriteLn('=== Legendre符号 ===');
  WriteLn('LegendreSymbol(2, 7): ', LegendreSymbol(2, 7));
  WriteLn('LegendreSymbol(3, 7): ', LegendreSymbol(3, 7));
  WriteLn('LegendreSymbol(5, 11): ', LegendreSymbol(5, 11));
  WriteLn('');
end;

begin
  WriteLn('');
  WriteLn('===========================================');
  WriteLn('  AllToolkit - Delphi Prime Utils Examples');
  WriteLn('===========================================');
  WriteLn('');
  
  Example_BasicPrimeDetection;
  Example_PrimeGeneration;
  Example_GCDAndLCM;
  Example_PrimeFactorization;
  Example_EulerPhi;
  Example_Sieve;
  Example_PrimeCount;
  Example_SpecialPrimes;
  Example_ModExp;
  Example_LegendreSymbol;
  
  WriteLn('===========================================');
  WriteLn('  Examples completed!');
  WriteLn('===========================================');
end.