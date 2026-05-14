# Polynomial Utils (Fortran)

A comprehensive polynomial manipulation library with zero external dependencies.

## Features

### Core Operations
- **Evaluation**: Horner's method and direct evaluation
- **Arithmetic**: Addition, subtraction, multiplication, scaling
- **Derivative**: Compute nth derivative
- **Integral**: Compute indefinite integral with optional constant

### Advanced Features
- **Root Finding**: 
  - Bisection method (single root in interval)
  - Newton-Raphson method (single root from initial guess)
  - Durand-Kerner method (all roots simultaneously)
- **Interpolation**: Lagrange interpolation through points
- **Polynomial Construction**: From roots
- **Composition**: p(q(x))
- **GCD**: Greatest common divisor of two polynomials
- **Deflation**: Divide out a root

## Usage

### Basic Evaluation

```fortran
use polynomial_utils

real(8) :: coeffs(4)
real(8) :: result

! Polynomial: 1 + 2x + 3x^2 + 4x^3
coeffs = [1.0d0, 2.0d0, 3.0d0, 4.0d0]

! Evaluate at x = 2
result = poly_eval(coeffs, 2.0d0)
```

### Derivative and Integral

```fortran
real(8), allocatable :: deriv(:), integ(:)

! Compute derivative
deriv = poly_derivative(coeffs)

! Compute integral (with integration constant = 0)
integ = poly_integral(coeffs, 0.0d0)
```

### Root Finding

```fortran
! Find root using bisection
root = poly_roots_bisection(coeffs, a, b, tolerance)

! Find root using Newton-Raphson
root = poly_roots_newton(coeffs, initial_guess, tolerance)

! Find all roots using Durand-Kerner
complex(8), allocatable :: roots(:)
roots = poly_roots_durand_kerner(coeffs, tolerance)
```

### Lagrange Interpolation

```fortran
real(8) :: x_points(3), y_points(3)
real(8), allocatable :: interp_poly(:)

x_points = [0.0d0, 1.0d0, 2.0d0]
y_points = [1.0d0, 2.0d0, 5.0d0]

interp_poly = poly_lagrange_interpolate(x_points, y_points)
```

### Polynomial from Roots

```fortran
real(8) :: roots(3)
real(8), allocatable :: poly(:)

roots = [1.0d0, 2.0d0, 3.0d0]  ! Roots at x=1, x=2, x=3
poly = poly_from_roots(roots)   ! Creates (x-1)(x-2)(x-3)
```

## Building

```bash
# Compile the module
gfortran -c polynomial_utils.f90

# Compile and run tests
gfortran polynomial_utils.f90 test_polynomial_utils.f90 -o test_polynomial
./test_polynomial

# Compile and run examples
gfortran polynomial_utils.f90 examples_polynomial_utils.f90 -o examples_polynomial
./examples_polynomial
```

## API Reference

| Function | Description |
|----------|-------------|
| `poly_eval(coeffs, x)` | Evaluate polynomial at x |
| `poly_eval_horner(coeffs, x)` | Evaluate using Horner's method |
| `poly_derivative(coeffs)` | Compute derivative |
| `poly_integral(coeffs, c)` | Compute integral with constant c |
| `poly_add(p, q)` | Add two polynomials |
| `poly_subtract(p, q)` | Subtract q from p |
| `poly_multiply(p, q)` | Multiply two polynomials |
| `poly_scale(coeffs, s)` | Scale by constant s |
| `poly_degree(coeffs)` | Get polynomial degree |
| `poly_normalize(coeffs)` | Remove trailing zeros |
| `poly_print(coeffs, var)` | Print polynomial |
| `poly_roots_bisection(coeffs, a, b, tol)` | Bisection root finding |
| `poly_roots_newton(coeffs, x0, tol)` | Newton-Raphson root finding |
| `poly_roots_durand_kerner(coeffs, tol)` | Find all roots |
| `poly_deflate(coeffs, root)` | Divide out a root |
| `poly_lagrange_interpolate(x, y)` | Lagrange interpolation |
| `poly_from_roots(roots)` | Create polynomial from roots |
| `poly_compose(p, q)` | Compose p(q(x)) |
| `poly_gcd(p, q)` | GCD of two polynomials |

## Test Results

All 27 tests pass:
- Polynomial evaluation tests
- Derivative and integral tests
- Arithmetic operation tests
- Degree calculation tests
- Root finding tests (bisection, Newton, Durand-Kerner)
- Interpolation tests
- Polynomial construction tests
- Composition and GCD tests

## Date

Created: 2026-05-14