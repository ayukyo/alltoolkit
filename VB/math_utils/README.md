# MathUtils - Mathematical Utilities for VB.NET

A comprehensive mathematical utility library for VB.NET applications with zero external dependencies.

## Features

### Constants
- Pi, E, Golden Ratio, Square Roots
- Conversion factors for degrees/radians

### Number Theory
- **GCD** - Greatest Common Divisor (Euclidean algorithm)
- **LCM** - Least Common Multiple
- **IsPrime** - Prime number checking with optimizations
- **GeneratePrimes** - Sieve of Eratosthenes
- **NextPrime/PreviousPrime** - Find adjacent primes
- **GetPrimeFactors** - Prime factorization

### Factorial & Fibonacci
- **Factorial** - Standard factorial calculation
- **FactorialBig** - Large factorial support (string output)
- **Fibonacci** - nth Fibonacci number
- **FibonacciSequence** - Generate Fibonacci sequence

### Statistics
- **Mean** - Arithmetic mean (average)
- **Median** - Median value
- **Mode** - Most frequent value(s)
- **Variance** - Population variance
- **StandardDeviation** - Standard deviation
- **Range** - Max - Min
- **Sum/Product** - Aggregation

### Number Validation
- **IsEven/IsOdd** - Parity check
- **IsPerfectSquare/IsPerfectCube** - Power validation
- **IsPerfectNumber** - Perfect number check
- **IsArmstrongNumber** - Narcissistic number check
- **IsPalindromeNumber** - Numeric palindrome
- **IsDivisible** - Divisibility test

### Number Conversion
- **ToBinary/FromBinary** - Base-2 conversion
- **ToOctal/FromOctal** - Base-8 conversion
- **ToHex/FromHex** - Base-16 conversion
- **ToRoman/FromRoman** - Roman numeral conversion

### Geometry
- **Distance2D/Distance3D** - Euclidean distance
- **CircleArea/CircleCircumference** - Circle calculations
- **RectangleArea/RectanglePerimeter** - Rectangle calculations
- **TriangleArea/TriangleAreaHeron** - Triangle calculations
- **SphereArea/SphereVolume** - Sphere calculations
- **CylinderVolume/ConeVolume** - 3D shape volumes

### Financial Math
- **SimpleInterest** - Simple interest calculation
- **CompoundInterest** - Compound interest calculation
- **MonthlyPayment** - Loan payment calculation
- **PresentValue/FutureValue** - Time value of money

### Combinatorics
- **Permutations** - nPr calculation
- **Combinations** - nCr calculation
- **Derangements** - Permutations with no fixed points

### Random Generation
- **RandomInt** - Random integer in range
- **RandomDouble** - Random double in range
- **RandomBool** - Random boolean
- **RandomLong** - Random long integer
- **RandomUniqueInts** - Unique random integers
- **Shuffle** - Fisher-Yates shuffle
- **RandomChoice/RandomChoices** - Random selection from collection

### Rounding
- **RoundToNearest** - Round to integer
- **RoundToDecimals** - Round to decimal places
- **RoundUp/RoundDown** - Ceiling/Floor
- **RoundToMultiple** - Round to nearest multiple
- **RoundToSigFigs** - Significant figures rounding
- **TruncateToDecimals** - Truncate without rounding

### Angle Conversions
- **DegreesToRadiansConvert** - Convert degrees to radians
- **RadiansToDegreesConvert** - Convert radians to degrees
- **NormalizeAngleDegrees/Radians** - Normalize angles

### Clamp & Wrap
- **Clamp** - Clamp value to range
- **Wrap** - Wrap value in range (modulo)
- **Lerp** - Linear interpolation
- **InverseLerp** - Inverse interpolation
- **MapRange** - Map value between ranges

### Power & Root
- **NthRoot** - nth root calculation
- **Power** - Integer exponentiation
- **PowerMod** - Modular exponentiation
- **IsPowerOfTwo** - Power of two check
- **NextPowerOfTwo** - Find next power of two
- **IntegerSqrt** - Integer square root

## Usage

```vb
Imports AllToolkit

' Number theory
Dim gcd As Long = MathUtils.GCD(12, 18)  ' Returns 6
Dim isPrime As Boolean = MathUtils.IsPrime(17)  ' Returns True

' Statistics
Dim data As Double() = {1, 2, 3, 4, 5}
Dim avg As Double = MathUtils.Mean(data)  ' Returns 3.0

' Geometry
Dim dist As Double = MathUtils.Distance2D(0, 0, 3, 4)  ' Returns 5.0
Dim area As Double = MathUtils.CircleArea(5)  ' Returns ~78.54

' Financial
Dim ci As Double = MathUtils.CompoundInterest(1000, 0.05, 10)  ' Compound interest
Dim payment As Double = MathUtils.MonthlyPayment(100000, 0.05, 360)  ' Monthly loan payment

' Random generation
Dim randInt As Integer = MathUtils.RandomInt(1, 100)
Dim shuffled As New List(Of Integer) From {1, 2, 3, 4, 5}
MathUtils.Shuffle(shuffled)
```

## Running Tests

```bash
vbc test.vb mod.vb && test.exe
```

## Running Examples

```bash
vbc examples.vb mod.vb && examples.exe
```

## Requirements

- VB.NET compiler (vbc)
- .NET Framework or .NET Core/5+

## License

Part of the AllToolkit project.