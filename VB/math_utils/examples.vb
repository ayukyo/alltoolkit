' =============================================================================
' AllToolkit - Math Utilities Examples for VB.NET
' =============================================================================
' Practical examples demonstrating MathUtils functionality.
' Run with: vbc examples.vb mod.vb && examples.exe
' =============================================================================

Imports System
Imports System.Collections.Generic
Imports AllToolkit

Module MathUtilsExamples

    Sub Main()
        Console.WriteLine("=" & New String("="c, 60))
        Console.WriteLine("AllToolkit MathUtils - Usage Examples")
        Console.WriteLine("=" & New String("="c, 60))
        Console.WriteLine()

        ExampleConstants()
        ExampleNumberTheory()
        ExampleFactorialFibonacci()
        ExampleStatistics()
        ExampleNumberValidation()
        ExampleNumberConversion()
        ExampleGeometry()
        ExampleFinancialMath()
        ExampleCombinatorics()
        ExampleRandomGeneration()
        ExampleRounding()
        ExampleAngleConversions()
        ExampleClampAndWrap()
        ExamplePowerAndRoot()

        Console.WriteLine()
        Console.WriteLine("=" & New String("="c, 60))
        Console.WriteLine("All examples completed!")
        Console.WriteLine("=" & New String("="c, 60))
    End Sub

    Sub ExampleConstants()
        Console.WriteLine("--- Mathematical Constants ---")

        Console.WriteLine($"Pi = {MathUtils.Pi}")
        Console.WriteLine($"E = {MathUtils.E}")
        Console.WriteLine($"Golden Ratio = {MathUtils.GoldenRatio}")
        Console.WriteLine($"Square Root of 2 = {MathUtils.Sqrt2}")
        Console.WriteLine($"Square Root of 3 = {MathUtils.Sqrt3}")
        Console.WriteLine($"Ln(2) = {MathUtils.Ln2}")

        Console.WriteLine()
    End Sub

    Sub ExampleNumberTheory()
        Console.WriteLine("--- Number Theory ---")

        Console.WriteLine("GCD and LCM:")
        Console.WriteLine($"  GCD(12, 18) = {MathUtils.GCD(12, 18)}")
        Console.WriteLine($"  GCD(48, 18, 12) = {MathUtils.GCD(48, 18, 12)}")
        Console.WriteLine($"  LCM(12, 18) = {MathUtils.LCM(12, 18)}")
        Console.WriteLine($"  LCM(4, 6, 8) = {MathUtils.LCM(4, 6, 8)}")

        Console.WriteLine("Prime checking:")
        Console.WriteLine($"  IsPrime(17) = {MathUtils.IsPrime(17)}")
        Console.WriteLine($"  IsPrime(18) = {MathUtils.IsPrime(18)}")
        Console.WriteLine($"  IsPrime(997) = {MathUtils.IsPrime(997)}")

        Console.WriteLine("Prime generation:")
        Dim primes As List(Of Long) = MathUtils.GeneratePrimes(50)
        Console.WriteLine($"  Primes up to 50: {String.Join(", ", primes.Take(10))}... (total: {primes.Count})")

        Console.WriteLine("Prime factors:")
        Dim factors As List(Of Long) = MathUtils.GetPrimeFactors(84)
        Console.WriteLine($"  Prime factors of 84: {String.Join(" x ", factors)}")

        Console.WriteLine()
    End Sub

    Sub ExampleFactorialFibonacci()
        Console.WriteLine("--- Factorial and Fibonacci ---")

        Console.WriteLine("Factorial:")
        Console.WriteLine($"  5! = {MathUtils.Factorial(5)}")
        Console.WriteLine($"  10! = {MathUtils.Factorial(10)}")
        Console.WriteLine($"  20! = {MathUtils.Factorial(20)}")
        Console.WriteLine($"  50! (big) = {MathUtils.FactorialBig(50).Substring(0, 20)}... ({MathUtils.FactorialBig(50).Length} digits)")

        Console.WriteLine("Fibonacci:")
        Console.WriteLine($"  Fibonacci(10) = {MathUtils.Fibonacci(10)}")
        Console.WriteLine($"  Fibonacci(20) = {MathUtils.Fibonacci(20)}")
        Console.WriteLine($"  Fibonacci(50) = {MathUtils.Fibonacci(50)}")

        Dim fibSeq As List(Of Long) = MathUtils.FibonacciSequence(10)
        Console.WriteLine($"  First 10 Fibonacci: {String.Join(", ", fibSeq)}")

        Console.WriteLine()
    End Sub

    Sub ExampleStatistics()
        Console.WriteLine("--- Statistics ---")

        Dim data As Double() = {12, 15, 18, 22, 25, 28, 30, 33, 35, 40}

        Console.WriteLine($"Data: {String.Join(", ", data)}")
        Console.WriteLine($"  Mean = {MathUtils.Mean(data):F2}")
        Console.WriteLine($"  Median = {MathUtils.Median(data):F2}")
        Console.WriteLine($"  Mode count = {MathUtils.Mode(data).Count}")
        Console.WriteLine($"  Range = {MathUtils.Range(data):F2}")
        Console.WriteLine($"  Sum = {MathUtils.Sum(data):F2}")
        Console.WriteLine($"  Product = {MathUtils.Product(data):F2}")
        Console.WriteLine($"  Variance = {MathUtils.Variance(data):F2}")
        Console.WriteLine($"  Std Dev = {MathUtils.StandardDeviation(data):F2}")
        Console.WriteLine($"  Sample Std Dev = {MathUtils.SampleStandardDeviation(data):F2}")

        Console.WriteLine()
    End Sub

    Sub ExampleNumberValidation()
        Console.WriteLine("--- Number Validation ---")

        Console.WriteLine($"  IsEven(42) = {MathUtils.IsEven(42)}")
        Console.WriteLine($"  IsOdd(43) = {MathUtils.IsOdd(43)}")
        Console.WriteLine($"  IsPerfectSquare(144) = {MathUtils.IsPerfectSquare(144)}")
        Console.WriteLine($"  IsPerfectCube(27) = {MathUtils.IsPerfectCube(27)}")
        Console.WriteLine($"  IsPerfectNumber(28) = {MathUtils.IsPerfectNumber(28)}")
        Console.WriteLine($"  IsArmstrongNumber(153) = {MathUtils.IsArmstrongNumber(153)}")
        Console.WriteLine($"  IsPalindromeNumber(12321) = {MathUtils.IsPalindromeNumber(12321)}")
        Console.WriteLine($"  IsDivisible(100, 25) = {MathUtils.IsDivisible(100, 25)}")

        Console.WriteLine()
    End Sub

    Sub ExampleNumberConversion()
        Console.WriteLine("--- Number Conversion ---")

        Console.WriteLine("Binary:")
        Console.WriteLine($"  42 in binary = {MathUtils.ToBinary(42)}")
        Console.WriteLine($"  101010 to decimal = {MathUtils.FromBinary("101010")}")

        Console.WriteLine("Octal:")
        Console.WriteLine($"  255 in octal = {MathUtils.ToOctal(255)}")
        Console.WriteLine($"  377 to decimal = {MathUtils.FromOctal("377")}")

        Console.WriteLine("Hexadecimal:")
        Console.WriteLine($"  255 in hex = {MathUtils.ToHex(255)}")
        Console.WriteLine($"  0xFF to decimal = {MathUtils.FromHex("0xFF")}")

        Console.WriteLine("Roman Numerals:")
        Console.WriteLine($"  1994 in Roman = {MathUtils.ToRoman(1994)}")
        Console.WriteLine($"  MMXXIV to decimal = {MathUtils.FromRoman("MMXXIV")}")

        Console.WriteLine()
    End Sub

    Sub ExampleGeometry()
        Console.WriteLine("--- Geometry ---")

        Console.WriteLine("Distance:")
        Console.WriteLine($"  Distance from (0,0) to (3,4) = {MathUtils.Distance2D(0, 0, 3, 4):F2}")
        Console.WriteLine($"  Distance from (0,0,0) to (1,2,2) = {MathUtils.Distance3D(0, 0, 0, 1, 2, 2):F2}")

        Console.WriteLine("Circle:")
        Console.WriteLine($"  Area of circle (r=5) = {MathUtils.CircleArea(5):F2}")
        Console.WriteLine($"  Circumference (r=5) = {MathUtils.CircleCircumference(5):F2}")

        Console.WriteLine("Rectangle:")
        Console.WriteLine($"  Area of 10x5 rectangle = {MathUtils.RectangleArea(10, 5):F2}")
        Console.WriteLine($"  Perimeter of 10x5 rectangle = {MathUtils.RectanglePerimeter(10, 5):F2}")

        Console.WriteLine("Triangle:")
        Console.WriteLine($"  Area (base=10, height=5) = {MathUtils.TriangleArea(10, 5):F2}")
        Console.WriteLine($"  Area (sides 3,4,5) via Heron = {MathUtils.TriangleAreaHeron(3, 4, 5):F2}")

        Console.WriteLine("3D Shapes:")
        Console.WriteLine($"  Sphere area (r=3) = {MathUtils.SphereArea(3):F2}")
        Console.WriteLine($"  Sphere volume (r=3) = {MathUtils.SphereVolume(3):F2}")
        Console.WriteLine($"  Cylinder volume (r=2, h=5) = {MathUtils.CylinderVolume(2, 5):F2}")

        Console.WriteLine()
    End Sub

    Sub ExampleFinancialMath()
        Console.WriteLine("--- Financial Math ---")

        Console.WriteLine("Interest:")
        Console.WriteLine($"  Simple interest on $1000 at 5% for 2 years = ${MathUtils.SimpleInterest(1000, 0.05, 2):F2}")
        Console.WriteLine($"  Compound interest: $1000 at 5% for 10 years = ${MathUtils.CompoundInterest(1000, 0.05, 10):F2}")

        Console.WriteLine("Loan:")
        Dim monthlyPayment As Double = MathUtils.MonthlyPayment(100000, 0.05, 360)
        Console.WriteLine($"  Monthly payment on $100K loan at 5% for 30 years = ${monthlyPayment:F2}")
        Console.WriteLine($"  Total paid over 30 years = ${monthlyPayment * 360:F2}")

        Console.WriteLine("Present/Future Value:")
        Console.WriteLine($"  Present value of $1000 in 5 years at 5% = ${MathUtils.PresentValue(1000, 0.05, 5):F2}")
        Console.WriteLine($"  Future value of $1000 in 5 years at 5% = ${MathUtils.FutureValue(1000, 0.05, 5):F2}")

        Console.WriteLine()
    End Sub

    Sub ExampleCombinatorics()
        Console.WriteLine("--- Combinatorics ---")

        Console.WriteLine("Permutations and Combinations:")
        Console.WriteLine($"  P(10, 3) = {MathUtils.Permutations(10, 3)} (arrange 10 items in 3 positions)")
        Console.WriteLine($"  C(10, 3) = {MathUtils.Combinations(10, 3)} (choose 3 from 10)")
        Console.WriteLine($"  C(52, 5) = {MathUtils.Combinations(52, 5)} (5-card poker hands)")

        Console.WriteLine("Derangements:")
        Console.WriteLine($"  Derangements of 4 items = {MathUtils.Derangements(4)}")
        Console.WriteLine($"  Derangements of 5 items = {MathUtils.Derangements(5)}")

        Console.WriteLine()
    End Sub

    Sub ExampleRandomGeneration()
        Console.WriteLine("--- Random Generation ---")

        Console.WriteLine($"  Random int [1, 100]: {MathUtils.RandomInt(1, 100)}")
        Console.WriteLine($"  Random double [0, 1]: {MathUtils.RandomDouble(0, 1):F6}")
        Console.WriteLine($"  Random bool: {MathUtils.RandomBool()}")

        Console.WriteLine($"  5 unique random ints [1, 20]: {String.Join(", ", MathUtils.RandomUniqueInts(5, 1, 20))}")

        Dim deck As New List(Of String) From {"A", "K", "Q", "J", "10", "9", "8", "7"}
        Console.WriteLine($"  Original: {String.Join(", ", deck)}")
        MathUtils.Shuffle(deck)
        Console.WriteLine($"  Shuffled: {String.Join(", ", deck)}")

        Dim colors As New List(Of String) From {"Red", "Green", "Blue", "Yellow"}
        Console.WriteLine($"  Random choice: {MathUtils.RandomChoice(colors)}")
        Console.WriteLine($"  3 random choices: {String.Join(", ", MathUtils.RandomChoices(colors, 3))}")

        Console.WriteLine()
    End Sub

    Sub ExampleRounding()
        Console.WriteLine("--- Rounding ---")

        Console.WriteLine($"  Round 3.14159 to 2 decimals: {MathUtils.RoundToDecimals(3.14159, 2)}")
        Console.WriteLine($"  Round 3.14159 to 4 decimals: {MathUtils.RoundToDecimals(3.14159, 4)}")
        Console.WriteLine($"  Round up 3.1: {MathUtils.RoundUp(3.1)}")
        Console.WriteLine($"  Round down 3.9: {MathUtils.RoundDown(3.9)}")
        Console.WriteLine($"  Round 23 to nearest 5: {MathUtils.RoundToMultiple(23, 5)}")
        Console.WriteLine($"  Round 1234 to 2 sig figs: {MathUtils.RoundToSigFigs(1234, 2)}")
        Console.WriteLine($"  Truncate 3.14999 to 2 decimals: {MathUtils.TruncateToDecimals(3.14999, 2)}")

        Console.WriteLine()
    End Sub

    Sub ExampleAngleConversions()
        Console.WriteLine("--- Angle Conversions ---")

        Console.WriteLine($"  90 degrees = {MathUtils.DegreesToRadiansConvert(90):F4} radians")
        Console.WriteLine($"  Pi radians = {MathUtils.RadiansToDegreesConvert(Math.PI):F2} degrees")
        Console.WriteLine($"  Normalize 450 degrees = {MathUtils.NormalizeAngleDegrees(450):F2} degrees")
        Console.WriteLine($"  Normalize -90 degrees = {MathUtils.NormalizeAngleDegrees(-90):F2} degrees")

        Console.WriteLine()
    End Sub

    Sub ExampleClampAndWrap()
        Console.WriteLine("--- Clamp and Wrap ---")

        Console.WriteLine($"  Clamp(150, 0, 100) = {MathUtils.Clamp(150, 0, 100)}")
        Console.WriteLine($"  Clamp(-50, 0, 100) = {MathUtils.Clamp(-50, 0, 100)}")
        Console.WriteLine($"  Wrap(250, 0, 100) = {MathUtils.Wrap(250, 0, 100)}")
        Console.WriteLine($"  Wrap(-50, 0, 100) = {MathUtils.Wrap(-50, 0, 100)}")

        Console.WriteLine("Interpolation:")
        Console.WriteLine($"  Lerp(0, 100, 0.5) = {MathUtils.Lerp(0, 100, 0.5)}")
        Console.WriteLine($"  Lerp(0, 100, 0.25) = {MathUtils.Lerp(0, 100, 0.25)}")
        Console.WriteLine($"  InverseLerp(0, 100, 50) = {MathUtils.InverseLerp(0, 100, 50)}")

        Console.WriteLine("Range mapping:")
        Console.WriteLine($"  Map 50 from [0,100] to [0,1000] = {MathUtils.MapRange(50, 0, 100, 0, 1000)}")
        Console.WriteLine($"  Map 75 from [0,100] to [200,400] = {MathUtils.MapRange(75, 0, 100, 200, 400)}")

        Console.WriteLine()
    End Sub

    Sub ExamplePowerAndRoot()
        Console.WriteLine("--- Power and Root ---")

        Console.WriteLine($"  Cube root of 27 = {MathUtils.NthRoot(27, 3):F2}")
        Console.WriteLine($"  4th root of 81 = {MathUtils.NthRoot(81, 4):F2}")
        Console.WriteLine($"  Power(2, 10) = {MathUtils.Power(2, 10)}")

        Console.WriteLine("Power of two:")
        Console.WriteLine($"  IsPowerOfTwo(64) = {MathUtils.IsPowerOfTwo(64)}")
        Console.WriteLine($"  IsPowerOfTwo(65) = {MathUtils.IsPowerOfTwo(65)}")
        Console.WriteLine($"  NextPowerOfTwo(100) = {MathUtils.NextPowerOfTwo(100)}")

        Console.WriteLine($"  IntegerSqrt(100) = {MathUtils.IntegerSqrt(100)}")
        Console.WriteLine($"  IntegerSqrt(99) = {MathUtils.IntegerSqrt(99)}")

        Console.WriteLine("Modular exponentiation:")
        Console.WriteLine($"  3^100 mod 7 = {MathUtils.PowerMod(3, 100, 7)}")

        Console.WriteLine()
    End Sub

End Module