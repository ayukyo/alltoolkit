' =============================================================================
' AllToolkit - Math Utilities Tests for VB.NET
' =============================================================================
' Unit tests for the MathUtils module.
' Run with: vbc test.vb mod.vb && test.exe
' =============================================================================

Imports System
Imports System.Collections.Generic
Imports AllToolkit

Module MathUtilsTests

    Private testCount As Integer = 0
    Private passCount As Integer = 0
    Private failCount As Integer = 0

    Sub Main()
        Console.WriteLine("=" & New String("="c, 60))
        Console.WriteLine("AllToolkit MathUtils Tests")
        Console.WriteLine("=" & New String("="c, 60))
        Console.WriteLine()

        ' Run all tests
        TestConstants()
        TestNumberTheory()
        TestFactorialAndFibonacci()
        TestStatistics()
        TestNumberValidation()
        TestNumberConversion()
        TestGeometry()
        TestFinancialMath()
        TestCombinatorics()
        TestRandomGeneration()
        TestRounding()
        TestAngleConversions()
        TestClampAndWrap()
        TestPowerAndRoot()

        ' Summary
        Console.WriteLine()
        Console.WriteLine("=" & New String("="c, 60))
        Console.WriteLine($"Test Results: {passCount}/{testCount} passed")
        Console.WriteLine($"  Passed: {passCount}")
        Console.WriteLine($"  Failed: {failCount}")
        Console.WriteLine("=" & New String("="c, 60))

        If failCount > 0 Then
            Console.WriteLine("Some tests failed!")
            Environment.Exit(1)
        Else
            Console.WriteLine("All tests passed!")
            Environment.Exit(0)
        End If
    End Sub

    Private Sub Assert(condition As Boolean, testName As String)
        testCount += 1
        If condition Then
            passCount += 1
            Console.WriteLine($"  [PASS] {testName}")
        Else
            failCount += 1
            Console.WriteLine($"  [FAIL] {testName}")
        End If
    End Sub

    Private Sub AssertEquals(expected As Object, actual As Object, testName As String)
        testCount += 1
        If expected.Equals(actual) Then
            passCount += 1
            Console.WriteLine($"  [PASS] {testName}")
        Else
            failCount += 1
            Console.WriteLine($"  [FAIL] {testName} - Expected: {expected}, Actual: {actual}")
        End If
    End Sub

    Private Sub AssertApproxEquals(expected As Double, actual As Double, tolerance As Double, testName As String)
        testCount += 1
        If Math.Abs(expected - actual) <= tolerance Then
            passCount += 1
            Console.WriteLine($"  [PASS] {testName}")
        Else
            failCount += 1
            Console.WriteLine($"  [FAIL] {testName} - Expected: {expected}, Actual: {actual}")
        End If
    End Sub

    ' ==========================================================================
    ' Test Constants
    ' ==========================================================================

    Sub TestConstants()
        Console.WriteLine("Testing Constants...")

        AssertApproxEquals(3.14159265358979, MathUtils.Pi, 0.0000001, "Pi constant")
        AssertApproxEquals(2.71828182845905, MathUtils.E, 0.0000001, "E constant")
        AssertApproxEquals(1.61803398874989, MathUtils.GoldenRatio, 0.0000001, "Golden ratio")
        AssertApproxEquals(1.41421356237309, MathUtils.Sqrt2, 0.0000001, "Square root of 2")
        AssertApproxEquals(1.73205080756887, MathUtils.Sqrt3, 0.0000001, "Square root of 3")
        AssertApproxEquals(0.69314718055994, MathUtils.Ln2, 0.0000001, "Ln2")
        Assert(MathUtils.DegreesToRadians < 1, "DegreesToRadians conversion factor")
        Assert(MathUtils.RadiansToDegrees > 1, "RadiansToDegrees conversion factor")
    End Sub

    ' ==========================================================================
    ' Test Number Theory
    ' ==========================================================================

    Sub TestNumberTheory()
        Console.WriteLine("Testing Number Theory...")

        AssertEquals(6, MathUtils.GCD(12, 18), "GCD(12, 18) = 6")
        AssertEquals(1, MathUtils.GCD(7, 11), "GCD(7, 11) = 1")
        AssertEquals(12, MathUtils.GCD(12, 0), "GCD(12, 0) = 12")
        AssertEquals(6, MathUtils.GCD(12, 18, 24), "GCD(12, 18, 24) = 6")

        AssertEquals(36, MathUtils.LCM(12, 18), "LCM(12, 18) = 36")
        AssertEquals(77, MathUtils.LCM(7, 11), "LCM(7, 11) = 77")
        AssertEquals(0, MathUtils.LCM(12, 0), "LCM(12, 0) = 0")
        AssertEquals(72, MathUtils.LCM(12, 18, 8), "LCM(12, 18, 8) = 72")

        Assert(MathUtils.IsPrime(2), "IsPrime(2) = true")
        Assert(MathUtils.IsPrime(3), "IsPrime(3) = true")
        Assert(MathUtils.IsPrime(17), "IsPrime(17) = true")
        Assert(Not MathUtils.IsPrime(1), "IsPrime(1) = false")
        Assert(Not MathUtils.IsPrime(4), "IsPrime(4) = false")
        Assert(Not MathUtils.IsPrime(15), "IsPrime(15) = false")

        Dim primes As List(Of Long) = MathUtils.GeneratePrimes(20)
        AssertEquals(8, primes.Count, "GeneratePrimes(20) count = 8")
        AssertEquals(2, primes(0), "First prime = 2")
        AssertEquals(19, primes(primes.Count - 1), "Last prime = 19")

        AssertEquals(7, MathUtils.NextPrime(5), "NextPrime(5) = 7")
        AssertEquals(11, MathUtils.NextPrime(10), "NextPrime(10) = 11")
        AssertEquals(2, MathUtils.NextPrime(0), "NextPrime(0) = 2")

        AssertEquals(3, MathUtils.PreviousPrime(5), "PreviousPrime(5) = 3")
        AssertEquals(7, MathUtils.PreviousPrime(11), "PreviousPrime(11) = 7")
        AssertEquals(-1, MathUtils.PreviousPrime(2), "PreviousPrime(2) = -1")

        AssertEquals(3, MathUtils.CountPrimeFactors(12), "CountPrimeFactors(12) = 3")
        AssertEquals(1, MathUtils.CountPrimeFactors(7), "CountPrimeFactors(7) = 1")

        Dim factors As List(Of Long) = MathUtils.GetPrimeFactors(12)
        AssertEquals(3, factors.Count, "GetPrimeFactors(12) count = 3")
    End Sub

    ' ==========================================================================
    ' Test Factorial and Fibonacci
    ' ==========================================================================

    Sub TestFactorialAndFibonacci()
        Console.WriteLine("Testing Factorial and Fibonacci...")

        AssertEquals(1, MathUtils.Factorial(0), "Factorial(0) = 1")
        AssertEquals(1, MathUtils.Factorial(1), "Factorial(1) = 1")
        AssertEquals(2, MathUtils.Factorial(2), "Factorial(2) = 2")
        AssertEquals(6, MathUtils.Factorial(3), "Factorial(3) = 6")
        AssertEquals(24, MathUtils.Factorial(4), "Factorial(4) = 24")
        AssertEquals(120, MathUtils.Factorial(5), "Factorial(5) = 120")
        AssertEquals(3628800, MathUtils.Factorial(10), "Factorial(10) = 3628800")

        AssertEquals("1", MathUtils.FactorialBig(0), "FactorialBig(0) = 1")
        AssertEquals("3628800", MathUtils.FactorialBig(10), "FactorialBig(10) = 3628800")
        Assert(MathUtils.FactorialBig(50).Length > 10, "FactorialBig(50) produces large number")

        AssertEquals(0, MathUtils.Fibonacci(0), "Fibonacci(0) = 0")
        AssertEquals(1, MathUtils.Fibonacci(1), "Fibonacci(1) = 1")
        AssertEquals(1, MathUtils.Fibonacci(2), "Fibonacci(2) = 1")
        AssertEquals(2, MathUtils.Fibonacci(3), "Fibonacci(3) = 2")
        AssertEquals(3, MathUtils.Fibonacci(4), "Fibonacci(4) = 3")
        AssertEquals(5, MathUtils.Fibonacci(5), "Fibonacci(5) = 5")
        AssertEquals(55, MathUtils.Fibonacci(10), "Fibonacci(10) = 55")

        Dim fibSeq As List(Of Long) = MathUtils.FibonacciSequence(10)
        AssertEquals(10, fibSeq.Count, "FibonacciSequence(10) count = 10")
        AssertEquals(55, fibSeq(fibSeq.Count - 1), "Last Fibonacci = 55")
    End Sub

    ' ==========================================================================
    ' Test Statistics
    ' ==========================================================================

    Sub TestStatistics()
        Console.WriteLine("Testing Statistics...")

        Dim numbers As Double() = {1, 2, 3, 4, 5}

        AssertApproxEquals(3.0, MathUtils.Mean(numbers), 0.0001, "Mean of 1-5 = 3")
        AssertApproxEquals(3.0, MathUtils.Median(numbers), 0.0001, "Median of 1-5 = 3")

        Dim numbers2 As Double() = {1, 2, 2, 3, 4}
        AssertApproxEquals(2.0, MathUtils.Median(numbers2), 0.0001, "Median of 1,2,2,3,4 = 2")

        Dim numbers3 As Double() = {1, 1, 2, 2, 2, 3}
        Dim modeResult As List(Of Double) = MathUtils.Mode(numbers3)
        AssertEquals(1, modeResult.Count, "Mode count = 1")
        AssertEquals(2.0, modeResult(0), "Mode = 2")

        AssertApproxEquals(2.0, MathUtils.Variance(numbers), 0.0001, "Variance of 1-5 = 2")
        AssertApproxEquals(Math.Sqrt(2.0), MathUtils.StandardDeviation(numbers), 0.0001, "StdDev of 1-5")

        AssertApproxEquals(4.0, MathUtils.Range(numbers), 0.0001, "Range of 1-5 = 4")
        AssertApproxEquals(15.0, MathUtils.Sum(numbers), 0.0001, "Sum of 1-5 = 15")
        AssertApproxEquals(120.0, MathUtils.Product(numbers), 0.0001, "Product of 1-5 = 120")
    End Sub

    ' ==========================================================================
    ' Test Number Validation
    ' ==========================================================================

    Sub TestNumberValidation()
        Console.WriteLine("Testing Number Validation...")

        Assert(MathUtils.IsEven(2), "IsEven(2) = true")
        Assert(MathUtils.IsEven(0), "IsEven(0) = true")
        Assert(Not MathUtils.IsEven(3), "IsEven(3) = false")

        Assert(MathUtils.IsOdd(3), "IsOdd(3) = true")
        Assert(Not MathUtils.IsOdd(2), "IsOdd(2) = false")
        Assert(Not MathUtils.IsOdd(0), "IsOdd(0) = false")

        Assert(MathUtils.IsPerfectSquare(4), "IsPerfectSquare(4) = true")
        Assert(MathUtils.IsPerfectSquare(9), "IsPerfectSquare(9) = true")
        Assert(MathUtils.IsPerfectSquare(16), "IsPerfectSquare(16) = true")
        Assert(Not MathUtils.IsPerfectSquare(5), "IsPerfectSquare(5) = false")
        Assert(Not MathUtils.IsPerfectSquare(-1), "IsPerfectSquare(-1) = false")

        Assert(MathUtils.IsPerfectCube(8), "IsPerfectCube(8) = true")
        Assert(MathUtils.IsPerfectCube(27), "IsPerfectCube(27) = true")
        Assert(Not MathUtils.IsPerfectCube(9), "IsPerfectCube(9) = false")

        Assert(MathUtils.IsPerfectNumber(6), "IsPerfectNumber(6) = true")  ' 1+2+3 = 6
        Assert(MathUtils.IsPerfectNumber(28), "IsPerfectNumber(28) = true") ' 1+2+4+7+14 = 28
        Assert(Not MathUtils.IsPerfectNumber(12), "IsPerfectNumber(12) = false")

        Assert(MathUtils.IsArmstrongNumber(153), "IsArmstrongNumber(153) = true") ' 1^3+5^3+3^3 = 153
        Assert(MathUtils.IsArmstrongNumber(370), "IsArmstrongNumber(370) = true") ' 3^3+7^3+0^3 = 370
        Assert(Not MathUtils.IsArmstrongNumber(100), "IsArmstrongNumber(100) = false")

        Assert(MathUtils.IsPalindromeNumber(121), "IsPalindromeNumber(121) = true")
        Assert(MathUtils.IsPalindromeNumber(1221), "IsPalindromeNumber(1221) = true")
        Assert(Not MathUtils.IsPalindromeNumber(123), "IsPalindromeNumber(123) = false")

        Assert(MathUtils.IsDivisible(12, 3), "IsDivisible(12, 3) = true")
        Assert(MathUtils.IsDivisible(12, 4), "IsDivisible(12, 4) = true")
        Assert(Not MathUtils.IsDivisible(12, 5), "IsDivisible(12, 5) = false")
    End Sub

    ' ==========================================================================
    ' Test Number Conversion
    ' ==========================================================================

    Sub TestNumberConversion()
        Console.WriteLine("Testing Number Conversion...")

        AssertEquals("0", MathUtils.ToBinary(0), "ToBinary(0) = 0")
        AssertEquals("10", MathUtils.ToBinary(2), "ToBinary(2) = 10")
        AssertEquals("11111111", MathUtils.ToBinary(255), "ToBinary(255) = 11111111")

        AssertEquals("0", MathUtils.ToOctal(0), "ToOctal(0) = 0")
        AssertEquals("10", MathUtils.ToOctal(8), "ToOctal(8) = 10")
        AssertEquals("377", MathUtils.ToOctal(255), "ToOctal(255) = 377")

        AssertEquals("0", MathUtils.ToHex(0), "ToHex(0) = 0")
        AssertEquals("A", MathUtils.ToHex(10), "ToHex(10) = A")
        AssertEquals("FF", MathUtils.ToHex(255), "ToHex(255) = FF")

        AssertEquals(255, MathUtils.FromBinary("11111111"), "FromBinary(11111111) = 255")
        AssertEquals(255, MathUtils.FromOctal("377"), "FromOctal(377) = 255")
        AssertEquals(255, MathUtils.FromHex("FF"), "FromHex(FF) = 255")
        AssertEquals(255, MathUtils.FromHex("0xFF"), "FromHex(0xFF) = 255")

        AssertEquals("I", MathUtils.ToRoman(1), "ToRoman(1) = I")
        AssertEquals("IV", MathUtils.ToRoman(4), "ToRoman(4) = IV")
        AssertEquals("V", MathUtils.ToRoman(5), "ToRoman(5) = V")
        AssertEquals("X", MathUtils.ToRoman(10), "ToRoman(10) = X")
        AssertEquals("XL", MathUtils.ToRoman(40), "ToRoman(40) = XL")
        AssertEquals("L", MathUtils.ToRoman(50), "ToRoman(50) = L")
        AssertEquals("XC", MathUtils.ToRoman(90), "ToRoman(90) = XC")
        AssertEquals("C", MathUtils.ToRoman(100), "ToRoman(100) = C")
        AssertEquals("M", MathUtils.ToRoman(1000), "ToRoman(1000) = M")
        AssertEquals("MMMCMXCIX", MathUtils.ToRoman(3999), "ToRoman(3999) = MMMCMXCIX")

        AssertEquals(1, MathUtils.FromRoman("I"), "FromRoman(I) = 1")
        AssertEquals(4, MathUtils.FromRoman("IV"), "FromRoman(IV) = 4")
        AssertEquals(10, MathUtils.FromRoman("X"), "FromRoman(X) = 10")
        AssertEquals(3999, MathUtils.FromRoman("MMMCMXCIX"), "FromRoman(MMMCMXCIX) = 3999")
    End Sub

    ' ==========================================================================
    ' Test Geometry
    ' ==========================================================================

    Sub TestGeometry()
        Console.WriteLine("Testing Geometry...")

        AssertApproxEquals(5.0, MathUtils.Distance2D(0, 0, 3, 4), 0.0001, "Distance2D (3,4,5 triangle)")
        AssertApproxEquals(13.0, MathUtils.Distance3D(0, 0, 0, 3, 4, 12), 0.0001, "Distance3D")

        AssertApproxEquals(Math.PI, MathUtils.CircleArea(1), 0.0001, "CircleArea(1) = Pi")
        AssertApproxEquals(4 * Math.PI, MathUtils.CircleArea(2), 0.0001, "CircleArea(2)")
        AssertApproxEquals(2 * Math.PI, MathUtils.CircleCircumference(1), 0.0001, "CircleCircumference(1)")

        AssertApproxEquals(50.0, MathUtils.RectangleArea(10, 5), 0.0001, "RectangleArea(10,5) = 50")
        AssertApproxEquals(30.0, MathUtils.RectanglePerimeter(10, 5), 0.0001, "RectanglePerimeter(10,5) = 30")

        AssertApproxEquals(10.0, MathUtils.TriangleArea(5, 4), 0.0001, "TriangleArea(5,4) = 10")
        AssertApproxEquals(6.0, MathUtils.TriangleAreaHeron(3, 4, 5), 0.0001, "TriangleAreaHeron(3,4,5) = 6")

        AssertApproxEquals(4 * Math.PI, MathUtils.SphereArea(1), 0.0001, "SphereArea(1)")
        AssertApproxEquals(4.0 / 3.0 * Math.PI, MathUtils.SphereVolume(1), 0.0001, "SphereVolume(1)")

        AssertApproxEquals(Math.PI * 4, MathUtils.CylinderVolume(1, 4), 0.0001, "CylinderVolume(1,4)")
        AssertApproxEquals(Math.PI / 3.0, MathUtils.ConeVolume(1, 1), 0.0001, "ConeVolume(1,1)")
    End Sub

    ' ==========================================================================
    ' Test Financial Math
    ' ==========================================================================

    Sub TestFinancialMath()
        Console.WriteLine("Testing Financial Math...")

        ' Compound interest: P(1 + r/n)^nt
        ' $1000 at 5% for 1 year compounded monthly
        Dim ci As Double = MathUtils.CompoundInterest(1000, 0.05, 1, 12)
        Assert(ci > 1050 AndAlso ci < 1052, "CompoundInterest basic")

        AssertApproxEquals(50.0, MathUtils.SimpleInterest(1000, 0.05, 1), 0.0001, "SimpleInterest(1000, 5%, 1yr) = 50")

        ' Monthly payment calculation
        Dim payment As Double = MathUtils.MonthlyPayment(1000, 0.12, 12)
        Assert(payment > 80 AndAlso payment < 90, "MonthlyPayment basic")

        Assert(MathUtils.PresentValue(110, 0.1, 1) < 110, "PresentValue basic")
        Assert(MathUtils.FutureValue(100, 0.1, 1) > 100, "FutureValue basic")
    End Sub

    ' ==========================================================================
    ' Test Combinatorics
    ' ==========================================================================

    Sub TestCombinatorics()
        Console.WriteLine("Testing Combinatorics...")

        AssertEquals(720, MathUtils.Permutations(6, 3), "Permutations(6,3) = 720") ' 6*5*4
        AssertEquals(6, MathUtils.Permutations(3, 2), "Permutations(3,2) = 6") ' 3*2
        AssertEquals(1, MathUtils.Permutations(5, 0), "Permutations(5,0) = 1")

        AssertEquals(20, MathUtils.Combinations(6, 3), "Combinations(6,3) = 20")
        AssertEquals(3, MathUtils.Combinations(3, 2), "Combinations(3,2) = 3")
        AssertEquals(1, MathUtils.Combinations(5, 0), "Combinations(5,0) = 1")
        AssertEquals(1, MathUtils.Combinations(5, 5), "Combinations(5,5) = 1")
        AssertEquals(252, MathUtils.Combinations(10, 5), "Combinations(10,5) = 252")

        AssertEquals(1, MathUtils.Derangements(0), "Derangements(0) = 1")
        AssertEquals(0, MathUtils.Derangements(1), "Derangements(1) = 0")
        AssertEquals(1, MathUtils.Derangements(2), "Derangements(2) = 1")
        AssertEquals(2, MathUtils.Derangements(3), "Derangements(3) = 2")
        AssertEquals(9, MathUtils.Derangements(4), "Derangements(4) = 9")
    End Sub

    ' ==========================================================================
    ' Test Random Generation
    ' ==========================================================================

    Sub TestRandomGeneration()
        Console.WriteLine("Testing Random Generation...")

        ' Test random range
        For i As Integer = 1 To 100
            Dim r As Integer = MathUtils.RandomInt(5, 10)
            Assert(r >= 5 AndAlso r <= 10, $"RandomInt in range 5-10 (test {i})")
        Next

        ' Test random double
        For i As Integer = 1 To 100
            Dim r As Double = MathUtils.RandomDouble(0, 1)
            Assert(r >= 0 AndAlso r < 1, $"RandomDouble in range 0-1 (test {i})")
        Next

        ' Test random bool
        Dim trueCount As Integer = 0
        For i As Integer = 1 To 1000
            If MathUtils.RandomBool() Then trueCount += 1
        Next
        Assert(trueCount > 400 AndAlso trueCount < 600, "RandomBool distribution")

        ' Test unique random
        Dim uniqueInts As List(Of Integer) = MathUtils.RandomUniqueInts(5, 1, 10)
        AssertEquals(5, uniqueInts.Count, "RandomUniqueInts count = 5")
        Dim seen As New HashSet(Of Integer)()
        For Each n As Integer In uniqueInts
            Assert(Not seen.Contains(n), "RandomUniqueInts no duplicates")
            seen.Add(n)
        Next

        ' Test shuffle
        Dim list As New List(Of Integer) From {1, 2, 3, 4, 5}
        MathUtils.Shuffle(list)
        AssertEquals(5, list.Count, "Shuffle preserves count")

        ' Test random choice
        Dim choiceList As New List(Of String) From {"A", "B", "C"}
        Dim choice As String = MathUtils.RandomChoice(choiceList)
        Assert(choiceList.Contains(choice), "RandomChoice returns valid element")

        ' Test random choices
        Dim choices As List(Of String) = MathUtils.RandomChoices(choiceList, 5)
        AssertEquals(5, choices.Count, "RandomChoices count = 5")
    End Sub

    ' ==========================================================================
    ' Test Rounding
    ' ==========================================================================

    Sub TestRounding()
        Console.WriteLine("Testing Rounding...")

        AssertEquals(3, MathUtils.RoundToNearest(3.4), "RoundToNearest(3.4)")
        AssertEquals(4, MathUtils.RoundToNearest(3.6), "RoundToNearest(3.6)")

        AssertApproxEquals(3.14, MathUtils.RoundToDecimals(3.14159, 2), 0.001, "RoundToDecimals(3.14159, 2)")
        AssertApproxEquals(3.142, MathUtils.RoundToDecimals(3.14159, 3), 0.0001, "RoundToDecimals(3.14159, 3)")

        AssertEquals(4, MathUtils.RoundUp(3.1), "RoundUp(3.1) = 4")
        AssertEquals(4, MathUtils.RoundUp(3.9), "RoundUp(3.9) = 4")
        AssertEquals(-3, MathUtils.RoundUp(-3.9), "RoundUp(-3.9) = -3")

        AssertEquals(3, MathUtils.RoundDown(3.9), "RoundDown(3.9) = 3")
        AssertEquals(3, MathUtils.RoundDown(3.1), "RoundDown(3.1) = 3")
        AssertEquals(-4, MathUtils.RoundDown(-3.1), "RoundDown(-3.1) = -4")

        AssertApproxEquals(25, MathUtils.RoundToMultiple(23, 5), 0.1, "RoundToMultiple(23, 5)")
        AssertApproxEquals(20, MathUtils.RoundToMultiple(22, 5), 0.1, "RoundToMultiple(22, 5)")

        Assert(MathUtils.RoundToSigFigs(1234, 2) >= 1200 AndAlso MathUtils.RoundToSigFigs(1234, 2) <= 1300, "RoundToSigFigs(1234, 2)")

        AssertApproxEquals(3.14, MathUtils.TruncateToDecimals(3.14999, 2), 0.001, "TruncateToDecimals(3.14999, 2)")
    End Sub

    ' ==========================================================================
    ' Test Angle Conversions
    ' ==========================================================================

    Sub TestAngleConversions()
        Console.WriteLine("Testing Angle Conversions...")

        AssertApproxEquals(Math.PI, MathUtils.DegreesToRadiansConvert(180), 0.0001, "180 degrees to radians")
        AssertApproxEquals(180, MathUtils.RadiansToDegreesConvert(Math.PI), 0.0001, "Pi radians to degrees")

        AssertApproxEquals(90, MathUtils.NormalizeAngleDegrees(90), 0.1, "NormalizeAngleDegrees(90)")
        AssertApproxEquals(180, MathUtils.NormalizeAngleDegrees(540), 0.1, "NormalizeAngleDegrees(540)")
        AssertApproxEquals(90, MathUtils.NormalizeAngleDegrees(-270), 0.1, "NormalizeAngleDegrees(-270)")

        Assert(MathUtils.NormalizeAngleRadians(Math.PI) >= 0 AndAlso MathUtils.NormalizeAngleRadians(Math.PI) < 2 * Math.PI, "NormalizeAngleRadians")
    End Sub

    ' ==========================================================================
    ' Test Clamp and Wrap
    ' ==========================================================================

    Sub TestClampAndWrap()
        Console.WriteLine("Testing Clamp and Wrap...")

        AssertEquals(10, MathUtils.Clamp(15, 5, 10), "Clamp(15, 5, 10) = 10")
        AssertEquals(5, MathUtils.Clamp(3, 5, 10), "Clamp(3, 5, 10) = 5")
        AssertEquals(7, MathUtils.Clamp(7, 5, 10), "Clamp(7, 5, 10) = 7")

        AssertApproxEquals(5, MathUtils.Wrap(25, 0, 10), 0.1, "Wrap(25, 0, 10) = 5")
        AssertApproxEquals(5, MathUtils.Wrap(-5, 0, 10), 0.1, "Wrap(-5, 0, 10) = 5")

        AssertApproxEquals(50, MathUtils.Lerp(0, 100, 0.5), 0.1, "Lerp(0, 100, 0.5) = 50")
        AssertApproxEquals(25, MathUtils.Lerp(0, 100, 0.25), 0.1, "Lerp(0, 100, 0.25) = 25")

        AssertApproxEquals(0.5, MathUtils.InverseLerp(0, 100, 50), 0.1, "InverseLerp(0, 100, 50) = 0.5")

        AssertApproxEquals(150, MathUtils.MapRange(50, 0, 100, 100, 200), 0.1, "MapRange")
    End Sub

    ' ==========================================================================
    ' Test Power and Root
    ' ==========================================================================

    Sub TestPowerAndRoot()
        Console.WriteLine("Testing Power and Root...")

        AssertApproxEquals(2.0, MathUtils.NthRoot(8, 3), 0.0001, "NthRoot(8, 3) = 2")
        AssertApproxEquals(3.0, MathUtils.NthRoot(81, 4), 0.0001, "NthRoot(81, 4) = 3")

        AssertEquals(8, MathUtils.Power(2, 3), "Power(2, 3) = 8")
        AssertEquals(16, MathUtils.Power(2, 4), "Power(2, 4) = 16")
        AssertEquals(1, MathUtils.Power(5, 0), "Power(5, 0) = 1")

        AssertEquals(1, MathUtils.PowerMod(2, 10, 7), "PowerMod(2, 10, 7) = 1") ' 1024 mod 7 = 1

        Assert(MathUtils.IsPowerOfTwo(1), "IsPowerOfTwo(1) = true")
        Assert(MathUtils.IsPowerOfTwo(2), "IsPowerOfTwo(2) = true")
        Assert(MathUtils.IsPowerOfTwo(4), "IsPowerOfTwo(4) = true")
        Assert(MathUtils.IsPowerOfTwo(16), "IsPowerOfTwo(16) = true")
        Assert(Not MathUtils.IsPowerOfTwo(3), "IsPowerOfTwo(3) = false")
        Assert(Not MathUtils.IsPowerOfTwo(5), "IsPowerOfTwo(5) = false")

        AssertEquals(1, MathUtils.NextPowerOfTwo(1), "NextPowerOfTwo(1) = 1")
        AssertEquals(4, MathUtils.NextPowerOfTwo(3), "NextPowerOfTwo(3) = 4")
        AssertEquals(8, MathUtils.NextPowerOfTwo(5), "NextPowerOfTwo(5) = 8")
        AssertEquals(16, MathUtils.NextPowerOfTwo(16), "NextPowerOfTwo(16) = 16")

        AssertEquals(3, MathUtils.IntegerSqrt(9), "IntegerSqrt(9) = 3")
        AssertEquals(3, MathUtils.IntegerSqrt(10), "IntegerSqrt(10) = 3")
        AssertEquals(4, MathUtils.IntegerSqrt(16), "IntegerSqrt(16) = 4")
        AssertEquals(0, MathUtils.IntegerSqrt(0), "IntegerSqrt(0) = 0")
    End Sub

End Module