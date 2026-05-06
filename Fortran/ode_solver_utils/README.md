# ODE Solver Utilities

AllToolkit - Fortran ODE (Ordinary Differential Equation) Solver Utilities

Zero-dependency ordinary differential equation solvers for Fortran 90/95/2003+. Perfect for scientific computing, physics simulations, and engineering applications.

Author: AllToolkit Contributors
License: MIT

## Features

### Methods

1. **Forward Euler** (1st order, explicit)
   - Simple and fast
   - Suitable for non-stiff problems
   - O(h) accuracy

2. **Backward Euler** (1st order, implicit)
   - Stable for stiff problems
   - Uses Newton-Raphson iteration
   - O(h) accuracy

3. **Heun's Method** (2nd order Runge-Kutta)
   - Improved Euler
   - Predictor-corrector approach
   - O(h²) accuracy

4. **Midpoint Method** (2nd order Runge-Kutta)
   - Symmetric method
   - Good for oscillatory problems
   - O(h²) accuracy

5. **Classic RK4** (4th order Runge-Kutta)
   - Most widely used method
   - Excellent balance of accuracy and speed
   - O(h⁴) accuracy

6. **RKF45** (Runge-Kutta-Fehlberg, adaptive)
   - Adaptive step size control
   - Uses embedded 4th/5th order methods
   - Excellent for general-purpose use

7. **DOPRI5** (Dormand-Prince, adaptive)
   - Modern adaptive method
   - FSAL (First Same As Last) optimization
   - Used in many scientific libraries

### Key Characteristics

- **Zero external dependencies** - Pure Fortran 90/95/2003+
- **System of ODEs support** - Solve multiple coupled equations
- **Adaptive step size** - Automatic error control
- **Stiff problem handling** - Backward Euler for stability
- **Type safety** - Strong Fortran typing
- **Well documented** - Comprehensive comments and examples

## Usage

### Basic Example: Exponential Decay

```fortran
program example_decay
    use ode_solver_utils
    implicit none
    
    real(8) :: t0, h
    real(8) :: y0(1)
    real(8), allocatable :: t_out(:), y_out(:,:)
    integer :: n_steps, n_vars, i
    
    n_vars = 1
    n_steps = 100
    allocate(t_out(n_steps+1), y_out(n_steps+1, n_vars))
    
    ! Problem: dy/dt = -y, y(0) = 1
    ! Exact solution: y(t) = exp(-t)
    t0 = 0.0d0
    h = 0.01d0
    y0(1) = 1.0d0
    
    ! Solve using RK4
    call rk4(exponential_decay, t0, y0, h, n_steps, t_out, y_out, n_vars)
    
    ! Print results
    do i = 1, n_steps+1, 10
        write(*,'(F5.2, 2F12.6)') t_out(i), y_out(i,1), exp(-t_out(i))
    end do
    
    deallocate(t_out, y_out)
    
contains
    
    subroutine exponential_decay(t, y, dydt)
        real(8), intent(in) :: t
        real(8), intent(in) :: y(:)
        real(8), intent(out) :: dydt(:)
        dydt(1) = -y(1)
    end subroutine exponential_decay
    
end program example_decay
```

### System of ODEs: Harmonic Oscillator

```fortran
program example_harmonic
    use ode_solver_utils
    implicit none
    
    real(8) :: t0, h
    real(8) :: y0(2)
    real(8), allocatable :: t_out(:), y_out(:,:)
    integer :: n_steps, n_vars
    
    n_vars = 2  ! Two variables: position and velocity
    n_steps = 500
    allocate(t_out(n_steps+1), y_out(n_steps+1, n_vars))
    
    ! Harmonic oscillator: d²x/dt² = -x
    ! Convert to system:
    !   y1 = x (position)
    !   y2 = dx/dt (velocity)
    !   dy1/dt = y2
    !   dy2/dt = -y1
    
    t0 = 0.0d0
    h = 0.02d0
    y0(1) = 1.0d0  ! Initial position
    y0(2) = 0.0d0  ! Initial velocity
    
    call rk4(harmonic_oscillator, t0, y0, h, n_steps, t_out, y_out, n_vars)
    
    deallocate(t_out, y_out)
    
contains
    
    subroutine harmonic_oscillator(t, y, dydt)
        real(8), intent(in) :: t
        real(8), intent(in) :: y(:)
        real(8), intent(out) :: dydt(:)
        dydt(1) = y(2)
        dydt(2) = -y(1)
    end subroutine harmonic_oscillator
    
end program example_harmonic
```

### Adaptive Step Size: RKF45

```fortran
program example_adaptive
    use ode_solver_utils
    implicit none
    
    real(8) :: t0, t_end, h_init, rtol, atol
    real(8) :: y0(1)
    real(8), allocatable :: t_out(:), y_out(:,:)
    integer :: n_steps, n_vars, max_steps, n_evals
    
    n_vars = 1
    max_steps = 1000
    allocate(t_out(max_steps), y_out(max_steps, n_vars))
    
    t0 = 0.0d0
    t_end = 5.0d0
    h_init = 0.1d0
    rtol = 1.0d-6   ! Relative tolerance
    atol = 1.0d-9   ! Absolute tolerance
    y0(1) = 1.0d0
    
    ! Adaptive step size solver
    call rkf45(my_function, t0, t_end, y0, h_init, rtol, atol, &
               t_out, y_out, n_steps, n_vars, max_steps, n_evals)
    
    write(*,'(A, I0)') 'Steps taken: ', n_steps
    write(*,'(A, I0)') 'Function evaluations: ', n_evals
    
    deallocate(t_out, y_out)
    
contains
    
    subroutine my_function(t, y, dydt)
        real(8), intent(in) :: t
        real(8), intent(in) :: y(:)
        real(8), intent(out) :: dydt(:)
        dydt(1) = -y(1)
    end subroutine my_function
    
end program example_adaptive
```

### Predator-Prey Model (Lotka-Volterra)

```fortran
program example_lotka_volterra
    use ode_solver_utils
    implicit none
    
    real(8) :: t0, h
    real(8) :: y0(2)
    real(8), allocatable :: t_out(:), y_out(:,:)
    integer :: n_steps, n_vars
    
    n_vars = 2
    n_steps = 2000
    allocate(t_out(n_steps+1), y_out(n_steps+1, n_vars))
    
    ! Initial populations
    y0(1) = 10.0d0  ! Prey (x)
    y0(2) = 5.0d0   ! Predators (y)
    
    t0 = 0.0d0
    h = 0.02d0
    
    call rk4(lotka_volterra, t0, y0, h, n_steps, t_out, y_out, n_vars)
    
    deallocate(t_out, y_out)
    
contains
    
    subroutine lotka_volterra(t, y, dydt)
        real(8), intent(in) :: t
        real(8), intent(in) :: y(:)
        real(8), intent(out) :: dydt(:)
        
        real(8) :: alpha, beta, delta, gamma
        
        alpha = 1.0d0    ! Prey birth rate
        beta = 0.1d0     ! Predation rate
        delta = 0.075d0  ! Predator birth rate per prey eaten
        gamma = 1.5d0    ! Predator death rate
        
        ! dx/dt = alpha*x - beta*x*y
        dydt(1) = alpha * y(1) - beta * y(1) * y(2)
        
        ! dy/dt = delta*x*y - gamma*y
        dydt(2) = delta * y(1) * y(2) - gamma * y(2)
    end subroutine lotka_volterra
    
end program example_lotka_volterra
```

## API Reference

### forward_euler

```fortran
call forward_euler(f, t0, y0, h, n_steps, t_out, y_out, n_vars)
```

Explicit forward Euler method (1st order).

### backward_euler

```fortran
call backward_euler(f, t0, y0, h, n_steps, t_out, y_out, n_vars, tol)
```

Implicit backward Euler method for stiff problems.

### heun_method

```fortran
call heun_method(f, t0, y0, h, n_steps, t_out, y_out, n_vars)
```

Heun's method (improved Euler, 2nd order).

### midpoint_method

```fortran
call midpoint_method(f, t0, y0, h, n_steps, t_out, y_out, n_vars)
```

Midpoint method (2nd order Runge-Kutta).

### rk4

```fortran
call rk4(f, t0, y0, h, n_steps, t_out, y_out, n_vars)
```

Classic 4th order Runge-Kutta method.

### rkf45

```fortran
call rkf45(f, t0, t_end, y0, h_init, rtol, atol, t_out, y_out, &
           n_steps, n_vars, max_steps, n_evals)
```

Runge-Kutta-Fehlberg adaptive step size method.

### dopri5_step

```fortran
call dopri5_step(f, t, y, h, y_new, err, n_vars, n_evals)
```

Single step of Dormand-Prince method.

## Testing

Compile and run the test suite:

```bash
gfortran -O2 mod.f90 ode_solver_utils_test.f90 -o test_ode
./test_ode
```

Expected output:

```
==========================================
  ODE Solver Utilities - Test Suite
==========================================

Test 1: Forward Euler - Exponential Decay
  PASS - Max error: ...

Test 2: Backward Euler - Exponential Decay
  PASS - Max error: ...

...

Tests: 9 passed / 9 total
 Status: ALL TESTS PASSED
==========================================
```

## Performance Tips

1. **Choose the right method:**
   - Non-stiff, low accuracy needed → Forward Euler
   - Stiff problems → Backward Euler
   - General purpose → RK4
   - Automatic control needed → RKF45

2. **Step size selection:**
   - Fixed step: Choose h based on problem timescales
   - Adaptive: Let the algorithm adjust automatically

3. **Stiffness detection:**
   - If Forward Euler gives erratic results → Use Backward Euler
   - If adaptive methods take many steps → Consider stiff solver

4. **Memory allocation:**
   - Preallocate output arrays for efficiency
   - Use appropriate array sizes

## Applications

- Physics simulations (pendulum, orbital mechanics)
- Chemical kinetics (reaction rates)
- Population dynamics (Lotka-Volterra)
- Control systems (PID controllers)
- Signal processing (filters)
- Finance (Black-Scholes equation)
- Engineering (heat transfer, structural dynamics)

## File Structure

```
ode_solver_utils/
├── mod.f90                  # Main module with all methods
├── ode_solver_utils_test.f90 # Comprehensive test suite
├── README.md                # This documentation
└── examples/                # Usage examples
    ├── decay.f90            # Simple exponential decay
    ├── harmonic.f90         # Harmonic oscillator
    ├── lotka_volterra.f90   # Predator-prey model
    └── pendulum.f90         # Simple pendulum
```

## Compilation

Using gfortran:

```bash
# Single file
gfortran -O2 -c mod.f90

# With test
gfortran -O2 mod.f90 ode_solver_utils_test.f90 -o test_ode

# With example
gfortran -O2 mod.f90 examples/decay.f90 -o decay_example
```

Using Intel Fortran (ifort):

```bash
ifort -O3 mod.f90 ode_solver_utils_test.f90 -o test_ode
```

---

**Last updated**: 2026-05-06