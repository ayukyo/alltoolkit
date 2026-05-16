' =============================================================================
' AllToolkit - Math Utilities for VB.NET
' =============================================================================
' A comprehensive mathematical utility library for VB.NET applications.
' Zero dependencies - uses only .NET standard library.
'
' Features:
' - Number theory (GCD, LCM, prime checking, prime generation)
' - Factorial and Fibonacci (with memoization)
' - Statistical functions (mean, median, mode, variance, std dev)
' - Number validation (even, odd, prime, perfect square, perfect number)
' - Number conversion (binary, octal, hex, roman numerals)
' - Geometric calculations (distance, area, perimeter)
' - Financial math (compound interest, amortization)
' - Combinatorics (permutations, combinations)
' - Random number generation (integers, decimals, from range)
' - Rounding utilities (round up, down, to nearest, significant figures)
' =============================================================================

Imports System
Imports System.Collections.Generic
Imports System.Linq

Namespace AllToolkit

    ''' <summary>
    ''' Comprehensive mathematical utilities for VB.NET.
    ''' </summary>
    Public Module MathUtils

        ' =========================================================================
        ' Constants
        ' =========================================================================

        ''' <summary>Mathematical constant Pi.</summary>
        Public ReadOnly Pi As Double = Math.PI

        ''' <summary>Mathematical constant E (Euler's number).</summary>
        Public ReadOnly E As Double = Math.E

        ''' <summary>Golden ratio (phi).</summary>
        Public ReadOnly GoldenRatio As Double = (1.0 + Math.Sqrt(5.0)) / 2.0

        ''' <summary>Square root of 2.</summary>
        Public ReadOnly Sqrt2 As Double = Math.Sqrt(2.0)

        ''' <summary>Square root of 3.</summary>
        Public ReadOnly Sqrt3 As Double = Math.Sqrt(3.0)

        ''' <summary>Natural log of 2.</summary>
        Public ReadOnly Ln2 As Double = Math.Log(2.0)

        ''' <summary>Degrees to radians conversion factor.</summary>
        Public ReadOnly DegreesToRadians As Double = Math.PI / 180.0

        ''' <summary>Radians to degrees conversion factor.</summary>
        Public ReadOnly RadiansToDegrees As Double = 180.0 / Math.PI

        ''' <summary>Random number generator (thread-safe).</summary>
        Private ReadOnly RandomGenerator As New Random()
        Private ReadOnly RandomLock As New Object()

        ' =========================================================================
        ' Number Theory
        ' =========================================================================

        ''' <summary>
        ''' Calculates the Greatest Common Divisor (GCD) of two integers.
        ''' Uses Euclidean algorithm.
        ''' </summary>
        ''' <param name="a">First integer.</param>
        ''' <param name="b">Second integer.</param>
        ''' <returns>GCD of a and b.</returns>
        Public Function GCD(a As Long, b As Long) As Long
            a = Math.Abs(a)
            b = Math.Abs(b)

            While b <> 0
                Dim temp As Long = b
                b = a Mod b
                a = temp
            End While

            Return a
        End Function

        ''' <summary>
        ''' Calculates the Greatest Common Divisor (GCD) of multiple integers.
        ''' </summary>
        ''' <param name="numbers">Array of integers.</param>
        ''' <returns>GCD of all numbers.</returns>
        Public Function GCD(ParamArray numbers As Long()) As Long
            If numbers Is Nothing OrElse numbers.Length = 0 Then Return 0
            If numbers.Length = 1 Then Return Math.Abs(numbers(0))

            Dim result As Long = numbers(0)
            For i As Integer = 1 To numbers.Length - 1
                result = GCD(result, numbers(i))
            Next

            Return result
        End Function

        ''' <summary>
        ''' Calculates the Least Common Multiple (LCM) of two integers.
        ''' </summary>
        ''' <param name="a">First integer.</param>
        ''' <param name="b">Second integer.</param>
        ''' <returns>LCM of a and b.</returns>
        Public Function LCM(a As Long, b As Long) As Long
            If a = 0 OrElse b = 0 Then Return 0
            Return Math.Abs(a \ GCD(a, b) * b)
        End Function

        ''' <summary>
        ''' Calculates the Least Common Multiple (LCM) of multiple integers.
        ''' </summary>
        ''' <param name="numbers">Array of integers.</param>
        ''' <returns>LCM of all numbers.</returns>
        Public Function LCM(ParamArray numbers As Long()) As Long
            If numbers Is Nothing OrElse numbers.Length = 0 Then Return 0
            If numbers.Length = 1 Then Return Math.Abs(numbers(0))

            Dim result As Long = numbers(0)
            For i As Integer = 1 To numbers.Length - 1
                result = LCM(result, numbers(i))
            Next

            Return result
        End Function

        ''' <summary>
        ''' Checks if a number is prime.
        ''' Uses trial division with optimizations.
        ''' </summary>
        ''' <param name="n">Number to check.</param>
        ''' <returns>True if the number is prime.</returns>
        Public Function IsPrime(n As Long) As Boolean
            If n < 2 Then Return False
            If n = 2 Then Return True
            If n Mod 2 = 0 Then Return False
            If n = 3 Then Return True
            If n Mod 3 = 0 Then Return False

            Dim i As Long = 5
            Dim w As Long = 2

            While i * i <= n
                If n Mod i = 0 Then Return False
                i += w
                w = 6 - w
            End While

            Return True
        End Function

        ''' <summary>
        ''' Generates all prime numbers up to a specified limit.
        ''' Uses Sieve of Eratosthenes.
        ''' </summary>
        ''' <param name="limit">Upper limit (inclusive).</param>
        ''' <returns>List of prime numbers up to limit.</returns>
        Public Function GeneratePrimes(limit As Long) As List(Of Long)
            Dim primes As New List(Of Long)()

            If limit < 2 Then Return primes

            ' Use Sieve of Eratosthenes
            Dim sieve As Boolean() = New Boolean(limit + 1) {}
            For i As Long = 2 To limit
                sieve(i) = True
            Next

            Dim p As Long = 2
            While p * p <= limit
                If sieve(p) Then
                    For i As Long = p * p To limit Step p
                        sieve(i) = False
                    Next
                End If
                p += 1
            End While

            For i As Long = 2 To limit
                If sieve(i) Then primes.Add(i)
            Next

            Return primes
        End Function

        ''' <summary>
        ''' Finds the next prime number after a given number.
        ''' </summary>
        ''' <param name="n">Starting number.</param>
        ''' <returns>Next prime number greater than n.</returns>
        Public Function NextPrime(n As Long) As Long
            If n < 2 Then Return 2

            Dim candidate As Long = n + 1
            If candidate Mod 2 = 0 Then candidate += 1

            While Not IsPrime(candidate)
                candidate += 2
            End While

            Return candidate
        End Function

        ''' <summary>
        ''' Finds the previous prime number before a given number.
        ''' </summary>
        ''' <param name="n">Starting number.</param>
        ''' <returns>Previous prime number less than n, or -1 if none exists.</returns>
        Public Function PreviousPrime(n As Long) As Long
            If n <= 2 Then Return -1
            If n = 3 Then Return 2

            Dim candidate As Long = n - 1
            If candidate Mod 2 = 0 Then candidate -= 1

            While candidate >= 2 AndAlso Not IsPrime(candidate)
                candidate -= 2
            End While

            Return If(candidate >= 2, candidate, -1)
        End Function

        ''' <summary>
        ''' Counts the number of prime factors of a number.
        ''' </summary>
        ''' <param name="n">Number to factorize.</param>
        ''' <returns>Number of prime factors (with multiplicity).</returns>
        Public Function CountPrimeFactors(n As Long) As Integer
            If n < 2 Then Return 0

            Dim count As Integer = 0

            ' Factor out 2s
            While n Mod 2 = 0
                count += 1
                n \= 2
            End While

            ' Factor out odd primes
            Dim factor As Long = 3
            While factor * factor <= n
                While n Mod factor = 0
                    count += 1
                    n \= factor
                End While
                factor += 2
            End While

            If n > 1 Then count += 1

            Return count
        End Function

        ''' <summary>
        ''' Gets all prime factors of a number.
        ''' </summary>
        ''' <param name="n">Number to factorize.</param>
        ''' <returns>List of prime factors (with multiplicity).</returns>
        Public Function GetPrimeFactors(n As Long) As List(Of Long)
            Dim factors As New List(Of Long)()

            If n < 2 Then Return factors

            ' Factor out 2s
            While n Mod 2 = 0
                factors.Add(2)
                n \= 2
            End While

            ' Factor out odd primes
            Dim factor As Long = 3
            While factor * factor <= n
                While n Mod factor = 0
                    factors.Add(factor)
                    n \= factor
                End While
                factor += 2
            End While

            If n > 1 Then factors.Add(n)

            Return factors
        End Function

        ' =========================================================================
        ' Factorial and Fibonacci
        ' =========================================================================

        ''' <summary>
        ''' Calculates factorial of a non-negative integer.
        ''' </summary>
        ''' <param name="n">Non-negative integer.</param>
        ''' <returns>n!</returns>
        Public Function Factorial(n As Integer) As Long
            If n < 0 Then Throw New ArgumentException("Factorial is not defined for negative numbers")
            If n = 0 OrElse n = 1 Then Return 1

            Dim result As Long = 1
            For i As Integer = 2 To n
                result *= i
            Next

            Return result
        End Function

        ''' <summary>
        ''' Calculates factorial using BigInteger for large numbers.
        ''' </summary>
        ''' <param name="n">Non-negative integer.</param>
        ''' <returns>n! as string (to handle large numbers).</returns>
        Public Function FactorialBig(n As Integer) As String
            If n < 0 Then Throw New ArgumentException("Factorial is not defined for negative numbers")
            If n <= 20 Then Return Factorial(n).ToString()

            ' Use BigInteger simulation via array multiplication
            Dim digits As New List(Of Integer) From {1}

            For i As Integer = 2 To n
                Dim carry As Integer = 0
                For j As Integer = 0 To digits.Count - 1
                    Dim product As Integer = digits(j) * i + carry
                    digits(j) = product Mod 10
                    carry = product \ 10
                Next

                While carry > 0
                    digits.Add(carry Mod 10)
                    carry \= 10
                End While
            Next

            ' Reverse and convert to string
            digits.Reverse()
            Return String.Join("", digits)
        End Function

        ''' <summary>
        ''' Calculates the nth Fibonacci number (iterative).
        ''' </summary>
        ''' <param name="n">Index (0-based).</param>
        ''' <returns>nth Fibonacci number.</returns>
        Public Function Fibonacci(n As Integer) As Long
            If n < 0 Then Throw New ArgumentException("Fibonacci is not defined for negative indices")
            If n = 0 Then Return 0
            If n = 1 Then Return 1

            Dim prev As Long = 0
            Dim curr As Long = 1

            For i As Integer = 2 To n
                Dim nextVal As Long = prev + curr
                prev = curr
                curr = nextVal
            Next

            Return curr
        End Function

        ''' <summary>
        ''' Generates Fibonacci sequence up to n terms.
        ''' </summary>
        ''' <param name="n">Number of terms.</param>
        ''' <returns>List of Fibonacci numbers.</returns>
        Public Function FibonacciSequence(n As Integer) As List(Of Long)
            Dim result As New List(Of Long)()

            If n <= 0 Then Return result

            For i As Integer = 0 To n - 1
                result.Add(Fibonacci(i))
            Next

            Return result
        End Function

        ' =========================================================================
        ' Statistical Functions
        ' =========================================================================

        ''' <summary>
        ''' Calculates the arithmetic mean (average) of a collection.
        ''' </summary>
        ''' <param name="numbers">Collection of numbers.</param>
        ''' <returns>Arithmetic mean.</returns>
        Public Function Mean(numbers As IEnumerable(Of Double)) As Double
            Dim list As List(Of Double) = numbers?.ToList()
            If list Is Nothing OrElse list.Count = 0 Then Return Double.NaN
            Return list.Sum() / list.Count
        End Function

        ''' <summary>
        ''' Calculates the median of a collection.
        ''' </summary>
        ''' <param name="numbers">Collection of numbers.</param>
        ''' <returns>Median value.</returns>
        Public Function Median(numbers As IEnumerable(Of Double)) As Double
            Dim list As List(Of Double) = numbers?.ToList()
            If list Is Nothing OrElse list.Count = 0 Then Return Double.NaN

            list.Sort()
            Dim count As Integer = list.Count
            Dim mid As Integer = count \ 2

            If count Mod 2 = 0 Then
                Return (list(mid - 1) + list(mid)) / 2.0
            Else
                Return list(mid)
            End If
        End Function

        ''' <summary>
        ''' Calculates the mode(s) of a collection.
        ''' </summary>
        ''' <param name="numbers">Collection of numbers.</param>
        ''' <returns>List of most frequent value(s).</returns>
        Public Function Mode(numbers As IEnumerable(Of Double)) As List(Of Double)
            Dim list As List(Of Double) = numbers?.ToList()
            Dim result As New List(Of Double)()

            If list Is Nothing OrElse list.Count = 0 Then Return result

            Dim freq As New Dictionary(Of Double, Integer)()
            For Each num As Double In list
                If freq.ContainsKey(num) Then
                    freq(num) += 1
                Else
                    freq(num) = 1
                End If
            Next

            Dim maxFreq As Integer = freq.Values.Max()
            For Each kvp As KeyValuePair(Of Double, Integer) In freq
                If kvp.Value = maxFreq Then
                    result.Add(kvp.Key)
                End If
            Next

            Return result
        End Function

        ''' <summary>
        ''' Calculates the variance of a collection (population variance).
        ''' </summary>
        ''' <param name="numbers">Collection of numbers.</param>
        ''' <returns>Population variance.</returns>
        Public Function Variance(numbers As IEnumerable(Of Double)) As Double
            Dim list As List(Of Double) = numbers?.ToList()
            If list Is Nothing OrElse list.Count = 0 Then Return Double.NaN

            Dim avg As Double = Mean(list)
            Dim sumSquaredDiff As Double = 0

            For Each num As Double In list
                sumSquaredDiff += Math.Pow(num - avg, 2)
            Next

            Return sumSquaredDiff / list.Count
        End Function

        ''' <summary>
        ''' Calculates the sample variance of a collection.
        ''' </summary>
        ''' <param name="numbers">Collection of numbers.</param>
        ''' <returns>Sample variance.</returns>
        Public Function SampleVariance(numbers As IEnumerable(Of Double)) As Double
            Dim list As List(Of Double) = numbers?.ToList()
            If list Is Nothing OrElse list.Count < 2 Then Return Double.NaN

            Dim avg As Double = Mean(list)
            Dim sumSquaredDiff As Double = 0

            For Each num As Double In list
                sumSquaredDiff += Math.Pow(num - avg, 2)
            Next

            Return sumSquaredDiff / (list.Count - 1)
        End Function

        ''' <summary>
        ''' Calculates the standard deviation of a collection (population).
        ''' </summary>
        ''' <param name="numbers">Collection of numbers.</param>
        ''' <returns>Population standard deviation.</returns>
        Public Function StandardDeviation(numbers As IEnumerable(Of Double)) As Double
            Dim variance As Double = Variance(numbers)
            Return Math.Sqrt(variance)
        End Function

        ''' <summary>
        ''' Calculates the sample standard deviation of a collection.
        ''' </summary>
        ''' <param name="numbers">Collection of numbers.</param>
        ''' <returns>Sample standard deviation.</returns>
        Public Function SampleStandardDeviation(numbers As IEnumerable(Of Double)) As Double
            Dim variance As Double = SampleVariance(numbers)
            Return Math.Sqrt(variance)
        End Function

        ''' <summary>
        ''' Calculates the range (max - min) of a collection.
        ''' </summary>
        ''' <param name="numbers">Collection of numbers.</param>
        ''' <returns>Range value.</returns>
        Public Function Range(numbers As IEnumerable(Of Double)) As Double
            Dim list As List(Of Double) = numbers?.ToList()
            If list Is Nothing OrElse list.Count = 0 Then Return Double.NaN
            Return list.Max() - list.Min()
        End Function

        ''' <summary>
        ''' Calculates the sum of a collection.
        ''' </summary>
        ''' <param name="numbers">Collection of numbers.</param>
        ''' <returns>Sum of all values.</returns>
        Public Function Sum(numbers As IEnumerable(Of Double)) As Double
            If numbers Is Nothing Then Return 0
            Return numbers.Sum()
        End Function

        ''' <summary>
        ''' Calculates the product of a collection.
        ''' </summary>
        ''' <param name="numbers">Collection of numbers.</param>
        ''' <returns>Product of all values.</returns>
        Public Function Product(numbers As IEnumerable(Of Double)) As Double
            Dim list As List(Of Double) = numbers?.ToList()
            If list Is Nothing OrElse list.Count = 0 Then Return 0

            Dim result As Double = 1
            For Each num As Double In list
                result *= num
            Next

            Return result
        End Function

        ' =========================================================================
        ' Number Validation
        ' =========================================================================

        ''' <summary>
        ''' Checks if a number is even.
        ''' </summary>
        Public Function IsEven(n As Long) As Boolean
            Return n Mod 2 = 0
        End Function

        ''' <summary>
        ''' Checks if a number is odd.
        ''' </summary>
        Public Function IsOdd(n As Long) As Boolean
            Return n Mod 2 <> 0
        End Function

        ''' <summary>
        ''' Checks if a number is a perfect square.
        ''' </summary>
        Public Function IsPerfectSquare(n As Long) As Boolean
            If n < 0 Then Return False
            Dim root As Long = CLng(Math.Sqrt(n))
            Return root * root = n
        End Function

        ''' <summary>
        ''' Checks if a number is a perfect cube.
        ''' </summary>
        Public Function IsPerfectCube(n As Long) As Boolean
            Dim absN As Long = Math.Abs(n)
            Dim root As Long = CLng(Math.Round(Math.Pow(absN, 1.0 / 3.0)))
            Return root * root * root = absN
        End Function

        ''' <summary>
        ''' Checks if a number is a perfect number (sum of proper divisors equals the number).
        ''' </summary>
        Public Function IsPerfectNumber(n As Long) As Boolean
            If n < 2 Then Return False

            Dim sum As Long = 1
            Dim sqrt As Long = CLng(Math.Sqrt(n))

            For i As Long = 2 To sqrt
                If n Mod i = 0 Then
                    sum += i
                    Dim other As Long = n \ i
                    If other <> i Then sum += other
                End If
            Next

            Return sum = n
        End Function

        ''' <summary>
        ''' Checks if a number is an Armstrong number (narcissistic number).
        ''' </summary>
        Public Function IsArmstrongNumber(n As Long) As Boolean
            If n < 0 Then Return False
            If n < 10 Then Return True

            Dim digits As String = n.ToString()
            Dim power As Integer = digits.Length
            Dim sum As Long = 0

            For Each c As Char In digits
                sum += CLng(Math.Pow(CLng(c.ToString()), power))
            Next

            Return sum = n
        End Function

        ''' <summary>
        ''' Checks if a number is a palindrome.
        ''' </summary>
        Public Function IsPalindromeNumber(n As Long) As Boolean
            If n < 0 Then n = -n
            Dim s As String = n.ToString()
            Dim chars As Char() = s.ToCharArray()
            Array.Reverse(chars)
            Return s = New String(chars)
        End Function

        ''' <summary>
        ''' Checks if a number is divisible by another.
        ''' </summary>
        Public Function IsDivisible(n As Long, divisor As Long) As Boolean
            If divisor = 0 Then Return False
            Return n Mod divisor = 0
        End Function

        ' =========================================================================
        ' Number Conversion
        ' =========================================================================

        ''' <summary>
        ''' Converts a decimal number to binary string.
        ''' </summary>
        Public Function ToBinary(n As Long) As String
            If n = 0 Then Return "0"
            Return Convert.ToString(n, 2)
        End Function

        ''' <summary>
        ''' Converts a decimal number to octal string.
        ''' </summary>
        Public Function ToOctal(n As Long) As String
            If n = 0 Then Return "0"
            Return Convert.ToString(n, 8)
        End Function

        ''' <summary>
        ''' Converts a decimal number to hexadecimal string.
        ''' </summary>
        Public Function ToHex(n As Long) As String
            If n = 0 Then Return "0"
            Return Convert.ToString(n, 16).ToUpper()
        End Function

        ''' <summary>
        ''' Converts a binary string to decimal.
        ''' </summary>
        Public Function FromBinary(binary As String) As Long
            If String.IsNullOrWhiteSpace(binary) Then Return 0
            Return Convert.ToInt64(binary.Trim(), 2)
        End Function

        ''' <summary>
        ''' Converts an octal string to decimal.
        ''' </summary>
        Public Function FromOctal(octal As String) As Long
            If String.IsNullOrWhiteSpace(octal) Then Return 0
            Return Convert.ToInt64(octal.Trim(), 8)
        End Function

        ''' <summary>
        ''' Converts a hexadecimal string to decimal.
        ''' </summary>
        Public Function FromHex(hex As String) As Long
            If String.IsNullOrWhiteSpace(hex) Then Return 0
            Dim cleanHex As String = hex.Trim()
            If cleanHex.StartsWith("0x", StringComparison.OrdinalIgnoreCase) Then
                cleanHex = cleanHex.Substring(2)
            End If
            Return Convert.ToInt64(cleanHex, 16)
        End Function

        ''' <summary>
        ''' Converts a decimal number to Roman numerals.
        ''' </summary>
        Public Function ToRoman(n As Integer) As String
            If n < 1 OrElse n > 3999 Then
                Throw New ArgumentException("Roman numerals support values 1-3999")
            End If

            Dim values As Integer() = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1}
            Dim numerals As String() = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"}

            Dim result As New Text.StringBuilder()

            For i As Integer = 0 To values.Length - 1
                While n >= values(i)
                    result.Append(numerals(i))
                    n -= values(i)
                End While
            Next

            Return result.ToString()
        End Function

        ''' <summary>
        ''' Converts Roman numerals to decimal.
        ''' </summary>
        Public Function FromRoman(roman As String) As Integer
            If String.IsNullOrWhiteSpace(roman) Then Return 0

            Dim values As New Dictionary(Of Char, Integer) From {
                {"I"c, 1}, {"V"c, 5}, {"X"c, 10}, {"L"c, 50},
                {"C"c, 100}, {"D"c, 500}, {"M"c, 1000}
            }

            roman = roman.ToUpper().Trim()
            Dim result As Integer = 0
            Dim prevValue As Integer = 0

            For i As Integer = roman.Length - 1 To 0 Step -1
                Dim c As Char = roman(i)
                If Not values.ContainsKey(c) Then
                    Throw New ArgumentException($"Invalid Roman numeral character: {c}")
                End If

                Dim currentValue As Integer = values(c)
                If currentValue < prevValue Then
                    result -= currentValue
                Else
                    result += currentValue
                End If
                prevValue = currentValue
            Next

            Return result
        End Function

        ' =========================================================================
        ' Geometric Calculations
        ' =========================================================================

        ''' <summary>
        ''' Calculates distance between two points in 2D.
        ''' </summary>
        Public Function Distance2D(x1 As Double, y1 As Double, x2 As Double, y2 As Double) As Double
            Return Math.Sqrt(Math.Pow(x2 - x1, 2) + Math.Pow(y2 - y1, 2))
        End Function

        ''' <summary>
        ''' Calculates distance between two points in 3D.
        ''' </summary>
        Public Function Distance3D(x1 As Double, y1 As Double, z1 As Double,
                                   x2 As Double, y2 As Double, z2 As Double) As Double
            Return Math.Sqrt(Math.Pow(x2 - x1, 2) + Math.Pow(y2 - y1, 2) + Math.Pow(z2 - z1, 2))
        End Function

        ''' <summary>
        ''' Calculates the area of a circle.
        ''' </summary>
        Public Function CircleArea(radius As Double) As Double
            Return Math.PI * radius * radius
        End Function

        ''' <summary>
        ''' Calculates the circumference of a circle.
        ''' </summary>
        Public Function CircleCircumference(radius As Double) As Double
            Return 2 * Math.PI * radius
        End Function

        ''' <summary>
        ''' Calculates the area of a rectangle.
        ''' </summary>
        Public Function RectangleArea(width As Double, height As Double) As Double
            Return width * height
        End Function

        ''' <summary>
        ''' Calculates the perimeter of a rectangle.
        ''' </summary>
        Public Function RectanglePerimeter(width As Double, height As Double) As Double
            Return 2 * (width + height)
        End Function

        ''' <summary>
        ''' Calculates the area of a triangle.
        ''' </summary>
        Public Function TriangleArea(baseLength As Double, height As Double) As Double
            Return 0.5 * baseLength * height
        End Function

        ''' <summary>
        ''' Calculates the area of a triangle using Heron's formula.
        ''' </summary>
        Public Function TriangleAreaHeron(a As Double, b As Double, c As Double) As Double
            If a + b <= c OrElse b + c <= a OrElse a + c <= b Then
                Throw New ArgumentException("Invalid triangle sides")
            End If

            Dim s As Double = (a + b + c) / 2
            Return Math.Sqrt(s * (s - a) * (s - b) * (s - c))
        End Function

        ''' <summary>
        ''' Calculates the area of a sphere.
        ''' </summary>
        Public Function SphereArea(radius As Double) As Double
            Return 4 * Math.PI * radius * radius
        End Function

        ''' <summary>
        ''' Calculates the volume of a sphere.
        ''' </summary>
        Public Function SphereVolume(radius As Double) As Double
            Return (4.0 / 3.0) * Math.PI * Math.Pow(radius, 3)
        End Function

        ''' <summary>
        ''' Calculates the volume of a cylinder.
        ''' </summary>
        Public Function CylinderVolume(radius As Double, height As Double) As Double
            Return Math.PI * radius * radius * height
        End Function

        ''' <summary>
        ''' Calculates the volume of a cone.
        ''' </summary>
        Public Function ConeVolume(radius As Double, height As Double) As Double
            Return (1.0 / 3.0) * Math.PI * radius * radius * height
        End Function

        ' =========================================================================
        ' Financial Math
        ' =========================================================================

        ''' <summary>
        ''' Calculates compound interest.
        ''' </summary>
        ''' <param name="principal">Initial amount.</param>
        ''' <param name="rate">Annual interest rate (as decimal, e.g., 0.05 for 5%).</param>
        ''' <param name="years">Number of years.</param>
        ''' <param name="compoundsPerYear">Compounding frequency per year (default: 12).</param>
        ''' <returns>Final amount after compound interest.</returns>
        Public Function CompoundInterest(principal As Double, rate As Double, years As Double,
                                         Optional compoundsPerYear As Integer = 12) As Double
            Return principal * Math.Pow(1 + rate / compoundsPerYear, compoundsPerYear * years)
        End Function

        ''' <summary>
        ''' Calculates simple interest.
        ''' </summary>
        ''' <param name="principal">Initial amount.</param>
        ''' <param name="rate">Annual interest rate (as decimal).</param>
        ''' <param name="years">Number of years.</param>
        ''' <returns>Interest earned.</returns>
        Public Function SimpleInterest(principal As Double, rate As Double, years As Double) As Double
            Return principal * rate * years
        End Function

        ''' <summary>
        ''' Calculates monthly payment for a loan.
        ''' </summary>
        ''' <param name="principal">Loan amount.</param>
        ''' <param name="annualRate">Annual interest rate (as decimal).</param>
        ''' <param name="months">Number of months.</param>
        ''' <returns>Monthly payment amount.</returns>
        Public Function MonthlyPayment(principal As Double, annualRate As Double, months As Integer) As Double
            If annualRate = 0 Then Return principal / months

            Dim monthlyRate As Double = annualRate / 12
            Return principal * monthlyRate * Math.Pow(1 + monthlyRate, months) /
                   (Math.Pow(1 + monthlyRate, months) - 1)
        End Function

        ''' <summary>
        ''' Calculates the present value of a future amount.
        ''' </summary>
        ''' <param name="futureValue">Future value.</param>
        ''' <param name="rate">Annual interest rate (as decimal).</param>
        ''' <param name="years">Number of years.</param>
        ''' <returns>Present value.</returns>
        Public Function PresentValue(futureValue As Double, rate As Double, years As Double) As Double
            Return futureValue / Math.Pow(1 + rate, years)
        End Function

        ''' <summary>
        ''' Calculates the future value of a present amount.
        ''' </summary>
        ''' <param name="presentValue">Present value.</param>
        ''' <param name="rate">Annual interest rate (as decimal).</param>
        ''' <param name="years">Number of years.</param>
        ''' <returns>Future value.</returns>
        Public Function FutureValue(presentValue As Double, rate As Double, years As Double) As Double
            Return presentValue * Math.Pow(1 + rate, years)
        End Function

        ' =========================================================================
        ' Combinatorics
        ' =========================================================================

        ''' <summary>
        ''' Calculates permutations nPr = n! / (n-r)!
        ''' </summary>
        Public Function Permutations(n As Integer, r As Integer) As Long
            If n < 0 OrElse r < 0 OrElse r > n Then Return 0
            If r = 0 Then Return 1

            Dim result As Long = 1
            For i As Integer = n To n - r + 1 Step -1
                result *= i
            Next

            Return result
        End Function

        ''' <summary>
        ''' Calculates combinations nCr = n! / (r! * (n-r)!)
        ''' </summary>
        Public Function Combinations(n As Integer, r As Integer) As Long
            If n < 0 OrElse r < 0 OrElse r > n Then Return 0
            If r = 0 OrElse r = n Then Return 1

            ' Optimize by using smaller r
            If r > n - r Then r = n - r

            Dim result As Long = 1
            For i As Integer = 0 To r - 1
                result = result * (n - i) \ (i + 1)
            Next

            Return result
        End Function

        ''' <summary>
        ''' Calculates the number of derangements (permutations where no element is in original position).
        ''' </summary>
        Public Function Derangements(n As Integer) As Long
            If n = 0 Then Return 1
            If n = 1 Then Return 0

            Dim prev2 As Long = 1
            Dim prev1 As Long = 0
            Dim result As Long = 0

            For i As Integer = 2 To n
                result = (i - 1) * (prev1 + prev2)
                prev2 = prev1
                prev1 = result
            Next

            Return result
        End Function

        ' =========================================================================
        ' Random Number Generation
        ' =========================================================================

        ''' <summary>
        ''' Generates a random integer in a range.
        ''' </summary>
        ''' <param name="min">Minimum value (inclusive).</param>
        ''' <param name="max">Maximum value (inclusive).</param>
        ''' <returns>Random integer in [min, max].</returns>
        Public Function RandomInt(min As Integer, max As Integer) As Integer
            SyncLock RandomLock
                Return RandomGenerator.Next(min, max + 1)
            End SyncLock
        End Function

        ''' <summary>
        ''' Generates a random double in a range.
        ''' </summary>
        ''' <param name="min">Minimum value.</param>
        ''' <param name="max">Maximum value.</param>
        ''' <returns>Random double in [min, max).</returns>
        Public Function RandomDouble(min As Double, max As Double) As Double
            SyncLock RandomLock
                Return min + RandomGenerator.NextDouble() * (max - min)
            End SyncLock
        End Function

        ''' <summary>
        ''' Generates a random boolean.
        ''' </summary>
        Public Function RandomBool() As Boolean
            SyncLock RandomLock
                Return RandomGenerator.Next(2) = 1
            End SyncLock
        End Function

        ''' <summary>
        ''' Generates a random long integer in a range.
        ''' </summary>
        ''' <param name="min">Minimum value.</param>
        ''' <param name="max">Maximum value.</param>
        ''' <returns>Random long in [min, max].</returns>
        Public Function RandomLong(min As Long, max As Long) As Long
            SyncLock RandomLock
                Dim bytes As Byte() = New Byte(7) {}
                RandomGenerator.NextBytes(bytes)
                Dim value As Long = Math.Abs(BitConverter.ToInt64(bytes, 0))
                Return min + value Mod (max - min + 1)
            End SyncLock
        End Function

        ''' <summary>
        ''' Generates random integers with no duplicates.
        ''' </summary>
        ''' <param name="count">Number of integers to generate.</param>
        ''' <param name="min">Minimum value (inclusive).</param>
        ''' <param name="max">Maximum value (inclusive).</param>
        ''' <returns>List of unique random integers.</returns>
        Public Function RandomUniqueInts(count As Integer, min As Integer, max As Integer) As List(Of Integer)
            If count > max - min + 1 Then
                Throw New ArgumentException("Cannot generate more unique numbers than the range allows")
            End If

            Dim result As New List(Of Integer)()
            Dim available As New HashSet(Of Integer)()

            For i As Integer = min To max
                available.Add(i)
            Next

            SyncLock RandomLock
                While result.Count < count
                    Dim value As Integer = RandomGenerator.Next(min, max + 1)
                    If available.Contains(value) Then
                        result.Add(value)
                        available.Remove(value)
                    End If
                End While
            End SyncLock

            Return result
        End Function

        ''' <summary>
        ''' Shuffles a list using Fisher-Yates algorithm.
        ''' </summary>
        Public Sub Shuffle(Of T)(list As IList(Of T))
            If list Is Nothing OrElse list.Count <= 1 Then Return

            SyncLock RandomLock
                For i As Integer = list.Count - 1 To 1 Step -1
                    Dim j As Integer = RandomGenerator.Next(i + 1)
                    Dim temp As T = list(i)
                    list(i) = list(j)
                    list(j) = temp
                Next
            End SyncLock
        End Sub

        ''' <summary>
        ''' Picks a random element from a list.
        ''' </summary>
        Public Function RandomChoice(Of T)(list As IList(Of T)) As T
            If list Is Nothing OrElse list.Count = 0 Then
                Return Nothing
            End If

            SyncLock RandomLock
                Return list(RandomGenerator.Next(list.Count))
            End SyncLock
        End Function

        ''' <summary>
        ''' Picks random elements from a list with replacement.
        ''' </summary>
        Public Function RandomChoices(Of T)(list As IList(Of T), count As Integer) As List(Of T)
            Dim result As New List(Of T)()

            If list Is Nothing OrElse list.Count = 0 OrElse count <= 0 Then
                Return result
            End If

            SyncLock RandomLock
                For i As Integer = 1 To count
                    result.Add(list(RandomGenerator.Next(list.Count)))
                Next
            End SyncLock

            Return result
        End Function

        ' =========================================================================
        ' Rounding Utilities
        ' =========================================================================

        ''' <summary>
        ''' Rounds to nearest integer (half rounds to even - banker's rounding).
        ''' </summary>
        Public Function RoundToNearest(value As Double) As Double
            Return Math.Round(value)
        End Function

        ''' <summary>
        ''' Rounds to specified decimal places.
        ''' </summary>
        Public Function RoundToDecimals(value As Double, decimals As Integer) As Double
            Return Math.Round(value, decimals)
        End Function

        ''' <summary>
        ''' Rounds up to nearest integer.
        ''' </summary>
        Public Function RoundUp(value As Double) As Double
            Return Math.Ceiling(value)
        End Function

        ''' <summary>
        ''' Rounds down to nearest integer.
        ''' </summary>
        Public Function RoundDown(value As Double) As Double
            Return Math.Floor(value)
        End Function

        ''' <summary>
        ''' Rounds to nearest multiple.
        ''' </summary>
        ''' <param name="value">Value to round.</param>
        ''' <param name="multiple">Multiple to round to.</param>
        ''' <returns>Rounded value.</returns>
        Public Function RoundToMultiple(value As Double, multiple As Double) As Double
            If multiple = 0 Then Return value
            Return Math.Round(value / multiple) * multiple
        End Function

        ''' <summary>
        ''' Rounds to specified number of significant figures.
        ''' </summary>
        Public Function RoundToSigFigs(value As Double, sigFigs As Integer) As Double
            If value = 0 Then Return 0
            If sigFigs < 1 Then sigFigs = 1

            Dim magnitude As Double = Math.Pow(10, CInt(Math.Floor(Math.Log10(Math.Abs(value)))) - sigFigs + 1)
            Return Math.Round(value / magnitude) * magnitude
        End Function

        ''' <summary>
        ''' Truncates to specified decimal places (no rounding).
        ''' </summary>
        Public Function TruncateToDecimals(value As Double, decimals As Integer) As Double
            Dim multiplier As Double = Math.Pow(10, decimals)
            Return Math.Truncate(value * multiplier) / multiplier
        End Function

        ' =========================================================================
        ' Angle Conversions
        ' =========================================================================

        ''' <summary>
        ''' Converts degrees to radians.
        ''' </summary>
        Public Function DegreesToRadiansConvert(degrees As Double) As Double
            Return degrees * DegreesToRadians
        End Function

        ''' <summary>
        ''' Converts radians to degrees.
        ''' </summary>
        Public Function RadiansToDegreesConvert(radians As Double) As Double
            Return radians * RadiansToDegrees
        End Function

        ''' <summary>
        ''' Normalizes an angle to [0, 360) degrees.
        ''' </summary>
        Public Function NormalizeAngleDegrees(angle As Double) As Double
            angle = angle Mod 360
            If angle < 0 Then angle += 360
            Return angle
        End Function

        ''' <summary>
        ''' Normalizes an angle to [0, 2π) radians.
        ''' </summary>
        Public Function NormalizeAngleRadians(angle As Double) As Double
            angle = angle Mod (2 * Math.PI)
            If angle < 0 Then angle += 2 * Math.PI
            Return angle
        End Function

        ' =========================================================================
        ' Clamp and Wrap
        ' =========================================================================

        ''' <summary>
        ''' Clamps a value to a range.
        ''' </summary>
        Public Function Clamp(value As Double, min As Double, max As Double) As Double
            Return Math.Max(min, Math.Min(max, value))
        End Function

        ''' <summary>
        ''' Wraps a value within a range (modulo for continuous values).
        ''' </summary>
        Public Function Wrap(value As Double, min As Double, max As Double) As Double
            Dim range As Double = max - min
            If range = 0 Then Return min

            Dim result As Double = ((value - min) Mod range)
            If result < 0 Then result += range

            Return min + result
        End Function

        ''' <summary>
        ''' Linear interpolation between two values.
        ''' </summary>
        ''' <param name="start">Start value.</param>
        ''' <param name="end">End value.</param>
        ''' <param name="t">Interpolation factor (0-1).</param>
        ''' <returns>Interpolated value.</returns>
        Public Function Lerp(start As Double, end As Double, t As Double) As Double
            Return start + (end - start) * t
        End Function

        ''' <summary>
        ''' Inverse linear interpolation - finds t given value.
        ''' </summary>
        Public Function InverseLerp(start As Double, end As Double, value As Double) As Double
            If end = start Then Return 0
            Return (value - start) / (end - start)
        End Function

        ''' <summary>
        ''' Maps a value from one range to another.
        ''' </summary>
        Public Function MapRange(value As Double,
                                  fromMin As Double, fromMax As Double,
                                  toMin As Double, toMax As Double) As Double
            Dim t As Double = InverseLerp(fromMin, fromMax, value)
            Return Lerp(toMin, toMax, t)
        End Function

        ' =========================================================================
        ' Power and Root Functions
        ' =========================================================================

        ''' <summary>
        ''' Calculates the nth root of a number.
        ''' </summary>
        Public Function NthRoot(value As Double, n As Integer) As Double
            If n <= 0 Then Throw New ArgumentException("n must be positive")
            If value < 0 AndAlso n Mod 2 = 0 Then
                Throw New ArgumentException("Even root of negative number is not real")
            End If

            Return Math.Pow(Math.Abs(value), 1.0 / n) * Math.Sign(value)
        End Function

        ''' <summary>
        ''' Calculates x^y for large integer exponents.
        ''' </summary>
        Public Function Power(x As Long, y As Integer) As Long
            If y < 0 Then Throw New ArgumentException("Exponent must be non-negative")
            If y = 0 Then Return 1

            Dim result As Long = 1
            Dim base As Long = x

            While y > 0
                If y Mod 2 = 1 Then result *= base
                base *= base
                y \= 2
            End While

            Return result
        End Function

        ''' <summary>
        ''' Calculates x^y mod m efficiently using modular exponentiation.
        ''' </summary>
        Public Function PowerMod(x As Long, y As Long, m As Long) As Long
            If m = 1 Then Return 0

            Dim result As Long = 1
            x = x Mod m
            If x < 0 Then x += m

            While y > 0
                If y Mod 2 = 1 Then
                    result = (result * x) Mod m
                End If
                y \= 2
                x = (x * x) Mod m
            End While

            Return result
        End Function

        ''' <summary>
        ''' Checks if a number is a power of 2.
        ''' </summary>
        Public Function IsPowerOfTwo(n As Long) As Boolean
            Return n > 0 AndAlso (n And (n - 1)) = 0
        End Function

        ''' <summary>
        ''' Finds the next power of 2 greater than or equal to n.
        ''' </summary>
        Public Function NextPowerOfTwo(n As Long) As Long
            If n <= 0 Then Return 1
            If IsPowerOfTwo(n) Then Return n

            Dim result As Long = 1
            While result < n
                result <<= 1
            End While

            Return result
        End Function

        ''' <summary>
        ''' Calculates the integer square root.
        ''' </summary>
        Public Function IntegerSqrt(n As Long) As Long
            If n < 0 Then Throw New ArgumentException("Cannot compute square root of negative number")
            If n = 0 Then Return 0

            Dim x As Long = n
            Dim y As Long = (x + 1) \ 2

            While y < x
                x = y
                y = (x + n \ x) \ 2
            End While

            Return x
        End Function

    End Module

End Namespace