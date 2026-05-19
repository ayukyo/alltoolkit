# Root Finding Utilities (Fortran)

Zero-dependency numerical root-finding algorithms for Fortran 90/95/2003+.

## Features

- **Bisection Method**: Guaranteed convergence for continuous functions with bracketing interval
- **Newton-Raphson Method**: Fast convergence for well-behaved functions (requires derivative)
- **Secant Method**: Newton-like convergence without derivative requirement
- **False Position (Regula Falsi)**: Hybrid method combining bisection safety with secant speed
- **Brent's Method**: Robust hybrid algorithm (recommended for most cases)
- **Ridder's Method**: Efficient method using exponential interpolation
- **Fixed-Point Iteration**: For solving x = g(x)
- **Newton-Raphson with Numerical Derivative**: When analytical derivative unavailable
- **Multiple Root Finder**: Scans interval to find all roots

## Usage

```fortran
use root_finding_utils

! Define your function
function my_function(x) result(y)
    real(8), intent(in) :: x
    real(8) :: y
    y = x**3 - x - 2.0d0
end function my_function

! Find root using Brent's method (recommended)
type(root_result) :: res
res = brent(my_function, 1.0d0, 2.0d0)

! Check result
if (res%converged) then
    print *, "Root found:", res%root
    print *, "Iterations:", res%iterations
end if
```

## Method Selection Guide

| Method | Requirements | Pros | Cons |
|--------|-------------|------|------|
| Bisection | Bracketed interval | Guaranteed convergence | Slow |
| Newton-Raphson | Initial guess + derivative | Very fast | May diverge |
| Secant | Two initial points | Fast, no derivative | May diverge |
| False Position | Bracketed interval | Better than bisection | Still slow for some functions |
| Brent | Bracketed interval | Fast + robust | More complex |
| Ridder | Bracketed interval | Fast | May fail occasionally |

**Recommendation**: Use Brent's method for most cases. It combines the reliability of bisection with the speed of secant/inverse quadratic interpolation.

## API Reference

### Types

```fortran
type :: root_result
    real(8) :: root          ! Found root
    real(8) :: residual      ! f(root)
    integer :: iterations    ! Number of iterations
    logical :: converged     ! Did it converge?
    character(64) :: method  ! Method name
    character(256) :: message ! Status message
end type
```

### Functions

#### `bisection(f, a, b, tolerance, max_iter)`
- `f`: Function to find root of
- `a, b`: Bracketing interval (f(a) and f(b) must have opposite signs)
- Returns: `root_result`

#### `newton_raphson(f, df, x0, tolerance, max_iter)`
- `f`: Function to find root of
- `df`: Derivative function
- `x0`: Initial guess
- Returns: `root_result`

#### `secant(f, x0, x1, tolerance, max_iter)`
- `f`: Function to find root of
- `x0, x1`: Two initial guesses
- Returns: `root_result`

#### `false_position(f, a, b, tolerance, max_iter)`
- `f`: Function to find root of
- `a, b`: Bracketing interval
- Returns: `root_result`

#### `brent(f, a, b, tolerance, max_iter)`
- `f`: Function to find root of
- `a, b`: Bracketing interval
- Returns: `root_result`

#### `ridder(f, a, b, tolerance, max_iter)`
- `f`: Function to find root of
- `a, b`: Bracketing interval
- Returns: `root_result`

#### `fixed_point(g, x0, tolerance, max_iter, relaxation)`
- `g`: Fixed-point function g(x) where we solve x = g(x)
- `x0`: Initial guess
- `relaxation`: Optional relaxation factor (default 1.0)
- Returns: `root_result`

#### `find_multiple_roots(f, a, b, n_intervals, tolerance)`
- `f`: Function to find roots of
- `a, b`: Interval to search
- `n_intervals`: Number of subintervals for searching
- Returns: Array of roots found

## Compilation

```bash
# Compile module
gfortran -c mod.f90

# Compile and run tests
gfortran -c mod.f90
gfortran mod.o test_root_finding.f90 -o test_root_finding
./test_root_finding

# Compile and run examples
gfortran -c mod.f90
gfortran mod.o examples/usage_examples.f90 -o usage_examples
./usage_examples
```

## Examples

### Computing Square Root
```fortran
! To find sqrt(N), solve x^2 - N = 0
function sqrt_func(x) result(y)
    real(8), intent(in) :: x
    real(8) :: y
    y = x * x - 25.0d0  ! Finding sqrt(25)
end function

res = brent(sqrt_func, 0.0d0, 26.0d0)
print *, "sqrt(25) = ", res%root  ! Output: 5.0
```

### Solving Transcendental Equation
```fortran
! Solve: x = 2*sin(x) + 1
function trans_func(x) result(y)
    real(8), intent(in) :: x
    real(8) :: y
    y = x - 2.0d0 * sin(x) - 1.0d0
end function

res = brent(trans_func, -5.0d0, 5.0d0)
```

### Newton-Raphson with Analytical Derivative
```fortran
! f(x) = x^3 - 2, f'(x) = 3x^2
function cubic(x) result(y)
    real(8), intent(in) :: x
    real(8) :: y
    y = x**3 - 2.0d0
end function

function cubic_deriv(x) result(y)
    real(8), intent(in) :: x
    real(8) :: y
    y = 3.0d0 * x**2
end function

res = newton_raphson(cubic, cubic_deriv, 1.5d0)
print *, "Cube root of 2 = ", res%root
```

## Default Parameters

- Default tolerance: `1.0e-10`
- Default maximum iterations: `100`
- Epsilon for zero checks: `1.0e-15`

## License

MIT License - Part of AllToolkit project