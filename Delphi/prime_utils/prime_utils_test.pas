{*******************************************************************************
  AllToolkit - Delphi Prime Number Utilities Tests
  
  测试套件：验证所有质数工具函数的正确性
  
  运行方式：
  - Delphi: 在IDE中打开并运行
  - Free Pascal: fpc prime_utils_test.pas && ./prime_utils_test
********************************************************************************}

program prime_utils_test;

{$IFDEF FPC}
  {$MODE DELPHI}
{$ENDIF}

uses
  SysUtils, Classes, mod;

var
  Passed, Failed: Integer;

procedure Test(const Name: string; Condition: Boolean);
begin
  if Condition then
  begin
    WriteLn('  [PASS] ', Name);
    Inc(Passed);
  end
  else
  begin
    WriteLn('  [FAIL] ', Name);
    Inc(Failed);
  end;
end;

procedure Test_IsPrime;
begin
  WriteLn('Testing IsPrime...');
  Test('IsPrime(2) = True', IsPrime(2) = True);
  Test('IsPrime(3) = True', IsPrime(3) = True);
  Test('IsPrime(5) = True', IsPrime(5) = True);
  Test('IsPrime(7) = True', IsPrime(7) = True);
  Test('IsPrime(11) = True', IsPrime(11) = True);
  Test('IsPrime(13) = True', IsPrime(13) = True);
  Test('IsPrime(17) = True', IsPrime(17) = True);
  Test('IsPrime(19) = True', IsPrime(19) = True);
  Test('IsPrime(23) = True', IsPrime(23) = True);
  Test('IsPrime(97) = True', IsPrime(97) = True);
  Test('IsPrime(1) = False', IsPrime(1) = False);
  Test('IsPrime(0) = False', IsPrime(0) = False);
  Test('IsPrime(-7) = False', IsPrime(-7) = False);
  Test('IsPrime(4) = False', IsPrime(4) = False);
  Test('IsPrime(6) = False', IsPrime(6) = False);
  Test('IsPrime(9) = False', IsPrime(9) = False);
  Test('IsPrime(15) = False', IsPrime(15) = False);
  Test('IsPrime(25) = False', IsPrime(25) = False);
  Test('IsPrime(100) = False', IsPrime(100) = False);
  Test('IsPrime(7919) = True', IsPrime(7919) = True);  // 1000th prime
  Test('IsPrime(104729) = True', IsPrime(104729) = True);  // 10000th prime
end;

procedure Test_IsPrimeTrial;
begin
  WriteLn('Testing IsPrimeTrial...');
  Test('IsPrimeTrial(2) = True', IsPrimeTrial(2) = True);
  Test('IsPrimeTrial(17) = True', IsPrimeTrial(17) = True);
  Test('IsPrimeTrial(97) = True', IsPrimeTrial(97) = True);
  Test('IsPrimeTrial(1) = False', IsPrimeTrial(1) = False);
  Test('IsPrimeTrial(15) = False', IsPrimeTrial(15) = False);
end;

procedure Test_NextPrime;
begin
  WriteLn('Testing NextPrime...');
  Test('NextPrime(0) = 2', NextPrime(0) = 2);
  Test('NextPrime(1) = 2', NextPrime(1) = 2);
  Test('NextPrime(2) = 3', NextPrime(2) = 3);
  Test('NextPrime(3) = 5', NextPrime(3) = 5);
  Test('NextPrime(10) = 11', NextPrime(10) = 11);
  Test('NextPrime(13) = 17', NextPrime(13) = 17);
  Test('NextPrime(100) = 101', NextPrime(100) = 101);
end;

procedure Test_PrevPrime;
begin
  WriteLn('Testing PrevPrime...');
  Test('PrevPrime(2) = -1', PrevPrime(2) = -1);
  Test('PrevPrime(3) = 2', PrevPrime(3) = 2);
  Test('PrevPrime(5) = 3', PrevPrime(5) = 3);
  Test('PrevPrime(10) = 7', PrevPrime(10) = 7);
  Test('PrevPrime(13) = 11', PrevPrime(13) = 11);
  Test('PrevPrime(100) = 97', PrevPrime(100) = 97);
end;

procedure Test_NthPrime;
begin
  WriteLn('Testing NthPrime...');
  Test('NthPrime(1) = 2', NthPrime(1) = 2);
  Test('NthPrime(2) = 3', NthPrime(2) = 3);
  Test('NthPrime(3) = 5', NthPrime(3) = 5);
  Test('NthPrime(4) = 7', NthPrime(4) = 7);
  Test('NthPrime(5) = 11', NthPrime(5) = 11);
  Test('NthPrime(10) = 29', NthPrime(10) = 29);
  Test('NthPrime(25) = 97', NthPrime(25) = 97);
  Test('NthPrime(100) = 541', NthPrime(100) = 541);
  Test('NthPrime(0) = -1', NthPrime(0) = -1);
end;

procedure Test_GCD;
begin
  WriteLn('Testing GCD...');
  Test('GCD(12, 8) = 4', GCD(12, 8) = 4);
  Test('GCD(54, 24) = 6', GCD(54, 24) = 6);
  Test('GCD(17, 13) = 1', GCD(17, 13) = 1);
  Test('GCD(100, 25) = 25', GCD(100, 25) = 25);
  Test('GCD(0, 5) = 5', GCD(0, 5) = 5);
  Test('GCD(5, 0) = 5', GCD(5, 0) = 5);
  Test('GCD(-12, 8) = 4', GCD(-12, 8) = 4);
end;

procedure Test_LCM;
begin
  WriteLn('Testing LCM...');
  Test('LCM(4, 6) = 12', LCM(4, 6) = 12);
  Test('LCM(3, 5) = 15', LCM(3, 5) = 15);
  Test('LCM(12, 8) = 24', LCM(12, 8) = 24);
  Test('LCM(7, 11) = 77', LCM(7, 11) = 77);
  Test('LCM(1, 5) = 5', LCM(1, 5) = 5);
end;

procedure Test_GCDArray;
begin
  WriteLn('Testing GCDArray...');
  Test('GCDArray([12, 8, 4]) = 4', GCDArray([12, 8, 4]) = 4);
  Test('GCDArray([15, 25, 35]) = 5', GCDArray([15, 25, 35]) = 5);
  Test('GCDArray([17, 13, 11]) = 1', GCDArray([17, 13, 11]) = 1);
end;

procedure Test_LCMArray;
begin
  WriteLn('Testing LCMArray...');
  Test('LCMArray([2, 3, 4]) = 12', LCMArray([2, 3, 4]) = 12);
  Test('LCMArray([4, 6, 8]) = 24', LCMArray([4, 6, 8]) = 24);
  Test('LCMArray([3, 5, 7]) = 105', LCMArray([3, 5, 7]) = 105);
end;

procedure Test_PrimeFactors;
var
  Factors: TStringList;
begin
  WriteLn('Testing PrimeFactors...');
  
  Factors := PrimeFactors(12);
  try
    Test('PrimeFactors(12) count = 3', Factors.Count = 3);
    Test('PrimeFactors(12) = [2,2,3]', 
      (Factors.Count = 3) and (Factors[0] = '2') and (Factors[1] = '2') and (Factors[2] = '3'));
  finally
    Factors.Free;
  end;
  
  Factors := PrimeFactors(100);
  try
    Test('PrimeFactors(100) = [2,2,5,5]', 
      (Factors.Count = 4) and (Factors[0] = '2') and (Factors[1] = '2') and 
      (Factors[2] = '5') and (Factors[3] = '5'));
  finally
    Factors.Free;
  end;
  
  Factors := PrimeFactors(17);
  try
    Test('PrimeFactors(17) = [17]', (Factors.Count = 1) and (Factors[0] = '17'));
  finally
    Factors.Free;
  end;
end;

procedure Test_PrimeFactorization;
var
  Factors: TStringList;
begin
  WriteLn('Testing PrimeFactorization...');
  
  Factors := PrimeFactorization(12);
  try
    Test('PrimeFactorization(12) = [2^2, 3]', Factors.Count = 2);
  finally
    Factors.Free;
  end;
  
  Factors := PrimeFactorization(360);
  try
    Test('PrimeFactorization(360) count = 3', Factors.Count = 3);
  finally
    Factors.Free;
  end;
  
  Factors := PrimeFactorization(1000);
  try
    Test('PrimeFactorization(1000) = [2^3, 5^3]', Factors.Count = 2);
  finally
    Factors.Free;
  end;
end;

procedure Test_DistinctPrimeFactors;
var
  Factors: TStringList;
begin
  WriteLn('Testing DistinctPrimeFactors...');
  
  Factors := DistinctPrimeFactors(12);
  try
    Test('DistinctPrimeFactors(12) = [2, 3]', 
      (Factors.Count = 2) and (Factors[0] = '2') and (Factors[1] = '3'));
  finally
    Factors.Free;
  end;
  
  Factors := DistinctPrimeFactors(100);
  try
    Test('DistinctPrimeFactors(100) = [2, 5]', 
      (Factors.Count = 2) and (Factors[0] = '2') and (Factors[1] = '5'));
  finally
    Factors.Free;
  end;
end;

procedure Test_EulerPhi;
begin
  WriteLn('Testing EulerPhi...');
  Test('EulerPhi(1) = 1', EulerPhi(1) = 1);
  Test('EulerPhi(2) = 1', EulerPhi(2) = 1);
  Test('EulerPhi(3) = 2', EulerPhi(3) = 2);
  Test('EulerPhi(4) = 2', EulerPhi(4) = 2);
  Test('EulerPhi(5) = 4', EulerPhi(5) = 4);
  Test('EulerPhi(6) = 2', EulerPhi(6) = 2);
  Test('EulerPhi(7) = 6', EulerPhi(7) = 6);
  Test('EulerPhi(9) = 6', EulerPhi(9) = 6);
  Test('EulerPhi(10) = 4', EulerPhi(10) = 4);
  Test('EulerPhi(12) = 4', EulerPhi(12) = 4);
  Test('EulerPhi(30) = 8', EulerPhi(30) = 8);
end;

procedure Test_PrimeCount;
begin
  WriteLn('Testing PrimeCount...');
  Test('PrimeCount(0) = 0', PrimeCount(0) = 0);
  Test('PrimeCount(1) = 0', PrimeCount(1) = 0);
  Test('PrimeCount(2) = 1', PrimeCount(2) = 1);
  Test('PrimeCount(10) = 4', PrimeCount(10) = 4);  // 2,3,5,7
  Test('PrimeCount(100) = 25', PrimeCount(100) = 25);
end;

procedure Test_CountPrimesInRange;
begin
  WriteLn('Testing CountPrimesInRange...');
  Test('CountPrimesInRange(1, 10) = 4', CountPrimesInRange(1, 10) = 4);
  Test('CountPrimesInRange(10, 20) = 4', CountPrimesInRange(10, 20) = 4);  // 11,13,17,19
  Test('CountPrimesInRange(50, 100) = 10', CountPrimesInRange(50, 100) = 10);
end;

procedure Test_SieveOfEratosthenes;
var
  Primes: TStringList;
begin
  WriteLn('Testing SieveOfEratosthenes...');
  
  Primes := SieveOfEratosthenes(10);
  try
    Test('Sieve(10) count = 4', Primes.Count = 4);
    Test('Sieve(10) = [2,3,5,7]', 
      (Primes.Count >= 4) and (Primes[0] = '2') and (Primes[1] = '3') and 
      (Primes[2] = '5') and (Primes[3] = '7'));
  finally
    Primes.Free;
  end;
  
  Primes := SieveOfEratosthenes(30);
  try
    Test('Sieve(30) count = 10', Primes.Count = 10);
  finally
    Primes.Free;
  end;
end;

procedure Test_SieveRange;
var
  Primes: TStringList;
begin
  WriteLn('Testing SieveRange...');
  
  Primes := SieveRange(10, 30);
  try
    Test('SieveRange(10, 30) count = 6', Primes.Count = 6);  // 11,13,17,19,23,29
  finally
    Primes.Free;
  end;
  
  Primes := SieveRange(100, 200);
  try
    Test('SieveRange(100, 200) count = 21', Primes.Count = 21);
  finally
    Primes.Free;
  end;
end;

procedure Test_IsTwinPrime;
begin
  WriteLn('Testing IsTwinPrime...');
  Test('IsTwinPrime(3) = True', IsTwinPrime(3) = True);     // (3,5)
  Test('IsTwinPrime(5) = True', IsTwinPrime(5) = True);     // (3,5) and (5,7)
  Test('IsTwinPrime(7) = True', IsTwinPrime(7) = True);     // (5,7)
  Test('IsTwinPrime(11) = True', IsTwinPrime(11) = True);   // (11,13)
  Test('IsTwinPrime(13) = True', IsTwinPrime(13) = True);   // (11,13)
  Test('IsTwinPrime(17) = True', IsTwinPrime(17) = True);   // (17,19)
  Test('IsTwinPrime(23) = False', IsTwinPrime(23) = False);  // Not part of twin prime pair
  Test('IsTwinPrime(4) = False', IsTwinPrime(4) = False);   // Not prime
end;

procedure Test_IsPalindromePrime;
begin
  WriteLn('Testing IsPalindromePrime...');
  Test('IsPalindromePrime(2) = True', IsPalindromePrime(2) = True);
  Test('IsPalindromePrime(3) = True', IsPalindromePrime(3) = True);
  Test('IsPalindromePrime(5) = True', IsPalindromePrime(5) = True);
  Test('IsPalindromePrime(7) = True', IsPalindromePrime(7) = True);
  Test('IsPalindromePrime(11) = True', IsPalindromePrime(11) = True);
  Test('IsPalindromePrime(101) = True', IsPalindromePrime(101) = True);
  Test('IsPalindromePrime(131) = True', IsPalindromePrime(131) = True);
  Test('IsPalindromePrime(13) = False', IsPalindromePrime(13) = False);   // Prime but not palindrome
  Test('IsPalindromePrime(22) = False', IsPalindromePrime(22) = False);  // Palindrome but not prime
end;

procedure Test_IsSafePrime;
begin
  WriteLn('Testing IsSafePrime...');
  Test('IsSafePrime(5) = True', IsSafePrime(5) = True);      // (5-1)/2 = 2 is prime
  Test('IsSafePrime(7) = True', IsSafePrime(7) = True);      // (7-1)/2 = 3 is prime
  Test('IsSafePrime(11) = True', IsSafePrime(11) = True);    // (11-1)/2 = 5 is prime
  Test('IsSafePrime(23) = True', IsSafePrime(23) = True);    // (23-1)/2 = 11 is prime
  Test('IsSafePrime(47) = True', IsSafePrime(47) = True);    // (47-1)/2 = 23 is prime
  Test('IsSafePrime(13) = False', IsSafePrime(13) = False);   // (13-1)/2 = 6 is not prime
  Test('IsSafePrime(4) = False', IsSafePrime(4) = False);    // Not prime
end;

procedure Test_IsSophieGermainPrime;
begin
  WriteLn('Testing IsSophieGermainPrime...');
  Test('IsSophieGermainPrime(2) = True', IsSophieGermainPrime(2) = True);    // 2*2+1 = 5 is prime
  Test('IsSophieGermainPrime(3) = True', IsSophieGermainPrime(3) = True);    // 2*3+1 = 7 is prime
  Test('IsSophieGermainPrime(5) = True', IsSophieGermainPrime(5) = True);    // 2*5+1 = 11 is prime
  Test('IsSophieGermainPrime(11) = True', IsSophieGermainPrime(11) = True);  // 2*11+1 = 23 is prime
  Test('IsSophieGermainPrime(23) = True', IsSophieGermainPrime(23) = True);  // 2*23+1 = 47 is prime
  Test('IsSophieGermainPrime(7) = False', IsSophieGermainPrime(7) = False);  // 2*7+1 = 15 is not prime
  Test('IsSophieGermainPrime(4) = False', IsSophieGermainPrime(4) = False);  // Not prime
end;

procedure Test_IsEmirp;
begin
  WriteLn('Testing IsEmirp...');
  Test('IsEmirp(13) = True', IsEmirp(13) = True);     // 13 -> 31, both prime
  Test('IsEmirp(17) = True', IsEmirp(17) = True);     // 17 -> 71, both prime
  Test('IsEmirp(31) = True', IsEmirp(31) = True);     // 31 -> 13, both prime
  Test('IsEmirp(37) = True', IsEmirp(37) = True);     // 37 -> 73, both prime
  Test('IsEmirp(71) = True', IsEmirp(71) = True);     // 71 -> 17, both prime
  Test('IsEmirp(73) = True', IsEmirp(73) = True);     // 73 -> 37, both prime
  Test('IsEmirp(11) = False', IsEmirp(11) = False);   // 11 -> 11, same number (palindrome)
  Test('IsEmirp(23) = False', IsEmirp(23) = False);  // 23 -> 32, not prime
  Test('IsEmirp(4) = False', IsEmirp(4) = False);     // Not prime
end;

procedure Test_ModExp;
begin
  WriteLn('Testing ModExp...');
  Test('ModExp(2, 10, 1000) = 24', ModExp(2, 10, 1000) = 24);
  Test('ModExp(3, 7, 13) = 3', ModExp(3, 7, 13) = 3);
  Test('ModExp(7, 256, 13) = 9', ModExp(7, 256, 13) = 9);
  Test('ModExp(2, 0, 5) = 1', ModExp(2, 0, 5) = 1);
  Test('ModExp(5, 3, 7) = 6', ModExp(5, 3, 7) = 6);
end;

procedure Test_LegendreSymbol;
begin
  WriteLn('Testing LegendreSymbol...');
  Test('LegendreSymbol(1, 5) = 1', LegendreSymbol(1, 5) = 1);
  Test('LegendreSymbol(2, 7) = 1', LegendreSymbol(2, 7) = 1);
  Test('LegendreSymbol(3, 7) = -1', LegendreSymbol(3, 7) = -1);
  Test('LegendreSymbol(5, 11) = 1', LegendreSymbol(5, 11) = 1);
  Test('LegendreSymbol(7, 11) = -1', LegendreSymbol(7, 11) = -1);
  Test('LegendreSymbol(0, 7) = 0', LegendreSymbol(0, 7) = 0);
end;

procedure Test_GeneratePrimes;
var
  Primes: TStringList;
begin
  WriteLn('Testing GeneratePrimes...');
  
  Primes := GeneratePrimes(1, 5);
  try
    Test('GeneratePrimes(1, 5) count = 5', Primes.Count = 5);
    Test('GeneratePrimes(1, 5) first = 2', Primes[0] = '2');
    Test('GeneratePrimes(1, 5) second = 3', Primes[1] = '3');
    Test('GeneratePrimes(1, 5) fifth = 11', Primes[4] = '11');
  finally
    Primes.Free;
  end;
  
  Primes := GeneratePrimes(100, 3);
  try
    Test('GeneratePrimes(100, 3) count = 3', Primes.Count = 3);
    Test('GeneratePrimes(100, 3) first = 101', Primes[0] = '101');
  finally
    Primes.Free;
  end;
end;

procedure Test_IsPerfectSquare;
begin
  WriteLn('Testing IsPerfectSquare...');
  Test('IsPerfectSquare(0) = True', IsPerfectSquare(0) = True);
  Test('IsPerfectSquare(1) = True', IsPerfectSquare(1) = True);
  Test('IsPerfectSquare(4) = True', IsPerfectSquare(4) = True);
  Test('IsPerfectSquare(9) = True', IsPerfectSquare(9) = True);
  Test('IsPerfectSquare(16) = True', IsPerfectSquare(16) = True);
  Test('IsPerfectSquare(100) = True', IsPerfectSquare(100) = True);
  Test('IsPerfectSquare(2) = False', IsPerfectSquare(2) = False);
  Test('IsPerfectSquare(3) = False', IsPerfectSquare(3) = False);
  Test('IsPerfectSquare(5) = False', IsPerfectSquare(5) = False);
  Test('IsPerfectSquare(-1) = False', IsPerfectSquare(-1) = False);
end;

procedure Test_GetTwinPrimePair;
var
  Pair: TStringList;
begin
  WriteLn('Testing GetTwinPrimePair...');
  
  Pair := GetTwinPrimePair(5);
  try
    Test('GetTwinPrimePair(5) = [3, 5]', 
      (Pair.Count = 2) and (Pair[0] = '3') and (Pair[1] = '5'));
  finally
    Pair.Free;
  end;
  
  Pair := GetTwinPrimePair(11);
  try
    Test('GetTwinPrimePair(11) = [11, 13]', 
      (Pair.Count = 2) and (Pair[0] = '11') and (Pair[1] = '13'));
  finally
    Pair.Free;
  end;
  
  Pair := GetTwinPrimePair(23);
  try
    Test('GetTwinPrimePair(23) = []', Pair.Count = 0);  // 23 is not a twin prime
  finally
    Pair.Free;
  end;
end;

procedure PrintSummary;
begin
  WriteLn('');
  WriteLn('===========================================');
  WriteLn('  Test Summary');
  WriteLn('===========================================');
  WriteLn('  Passed: ', Passed);
  WriteLn('  Failed: ', Failed);
  WriteLn('  Total:  ', Passed + Failed);
  WriteLn('===========================================');
  
  if Failed = 0 then
    WriteLn('  All tests passed!')
  else
    WriteLn('  Some tests failed!');
end;

begin
  Passed := 0;
  Failed := 0;
  
  WriteLn('');
  WriteLn('===========================================');
  WriteLn('  AllToolkit - Delphi Prime Utils Tests');
  WriteLn('===========================================');
  WriteLn('');
  
  // Basic prime tests
  Test_IsPrime;
  Test_IsPrimeTrial;
  
  // Prime generation tests
  Test_NextPrime;
  Test_PrevPrime;
  Test_NthPrime;
  Test_GeneratePrimes;
  
  // GCD/LCM tests
  Test_GCD;
  Test_LCM;
  Test_GCDArray;
  Test_LCMArray;
  
  // Factorization tests
  Test_PrimeFactors;
  Test_PrimeFactorization;
  Test_DistinctPrimeFactors;
  
  // Euler's totient tests
  Test_EulerPhi;
  
  // Prime counting tests
  Test_PrimeCount;
  Test_CountPrimesInRange;
  
  // Sieve tests
  Test_SieveOfEratosthenes;
  Test_SieveRange;
  
  // Special prime tests
  Test_IsTwinPrime;
  Test_GetTwinPrimePair;
  Test_IsPalindromePrime;
  Test_IsSafePrime;
  Test_IsSophieGermainPrime;
  Test_IsEmirp;
  
  // Utility tests
  Test_ModExp;
  Test_LegendreSymbol;
  Test_IsPerfectSquare;
  
  PrintSummary;
end.