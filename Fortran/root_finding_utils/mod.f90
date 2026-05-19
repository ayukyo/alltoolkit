!! AllToolkit - Fortran Root Finding Utilities Module
!! Zero-dependency numerical root-finding algorithms for Fortran 90/95/2003+
!!
!! Features:
!! - Bisection method (guaranteed convergence for continuous functions)
!! - Newton-Raphson method (fast convergence for well-behaved functions)
!! - Secant method (Newton-like without derivative)
!! - False Position (Regula Falsi) method
!! - Brent's method (hybrid, robust and efficient)
!! - Fixed-point iteration
!! - Ridder's method
!!
!! Author: AllToolkit Contributors
!! License: MIT

module root_finding_utils
    implicit none
    
    ! Module constants
    real(8), parameter :: DEFAULT_TOLERANCE = 1.0d-10
    integer, parameter :: DEFAULT_MAX_ITER = 100
    real(8), parameter :: EPSILON = 1.0d-15
    
    ! Result type for root finding
    type :: root_result
        real(8) :: root              ! Found root
        real(8) :: residual           ! Function value at root
        integer :: iterations         ! Number of iterations used
        logical :: converged          ! Did it converge?
        character(len=64) :: method   ! Method used
        character(len=256) :: message ! Status message
    end type root_result
    
    ! Abstract interface for function f(x)
    abstract interface
        function func_interface(x) result(y)
            real(8), intent(in) :: x
            real(8) :: y
        end function func_interface
        
        function func_interface_params(x, params) result(y)
            real(8), intent(in) :: x
            real(8), intent(in) :: params(:)
            real(8) :: y
        end function func_interface_params
        
        function deriv_interface(x) result(y)
            real(8), intent(in) :: x
            real(8) :: y
        end function deriv_interface
    end interface

contains

    !==========================================================================
    ! Bisection Method
    !==========================================================================
    
    !> Bisection method for finding root of f(x) in interval [a, b]
    !! Requires f(a) and f(b) to have opposite signs
    !! @param f Function to find root of
    !! @param a Left endpoint
    !! @param b Right endpoint
    !! @param tolerance Desired accuracy (optional)
    !! @param max_iter Maximum iterations (optional)
    !! @return root_result with found root and status
    function bisection(f, a, b, tolerance, max_iter) result(res)
        procedure(func_interface) :: f
        real(8), intent(in) :: a, b
        real(8), intent(in), optional :: tolerance
        integer, intent(in), optional :: max_iter
        type(root_result) :: res
        
        real(8) :: tol, fa, fb, fc, c
        real(8) :: xa, xb  ! Local copies for interval updates
        integer :: maxit, iter
        
        ! Set defaults
        tol = DEFAULT_TOLERANCE
        if (present(tolerance)) tol = tolerance
        maxit = DEFAULT_MAX_ITER
        if (present(max_iter)) maxit = max_iter
        
        ! Initialize result
        res%method = "Bisection"
        res%converged = .false.
        res%iterations = 0
        
        ! Initialize local interval
        xa = a
        xb = b
        
        ! Check endpoints
        fa = f(xa)
        fb = f(xb)
        
        ! Check if endpoint is already a root (using tolerance)
        if (abs(fa) < tol) then
            res%root = xa
            res%residual = fa
            res%converged = .true.
            res%message = "Root found at left endpoint"
            return
        end if
        
        if (abs(fb) < tol) then
            res%root = xb
            res%residual = fb
            res%converged = .true.
            res%message = "Root found at right endpoint"
            return
        end if
        
        ! Check for valid interval
        if (fa * fb > 0.0d0) then
            res%root = (xa + xb) / 2.0d0
            res%residual = f(res%root)
            res%message = "Error: f(a) and f(b) must have opposite signs"
            return
        end if
        
        ! Bisection loop
        do iter = 1, maxit
            c = (xa + xb) / 2.0d0
            fc = f(c)
            
            res%iterations = iter
            res%root = c
            res%residual = fc
            
            ! Check convergence
            if (abs(fc) < tol .or. abs(xb - xa) < tol) then
                res%converged = .true.
                write(res%message, '(A,I0,A)') "Converged in ", iter, " iterations"
                return
            end if
            
            ! Update interval
            if (fa * fc < 0.0d0) then
                xb = c
                fb = fc
            else
                xa = c
                fa = fc
            end if
        end do
        
        res%message = "Warning: Maximum iterations reached"
    end function bisection
    
    !==========================================================================
    ! Newton-Raphson Method
    !==========================================================================
    
    !> Newton-Raphson method for finding root of f(x)
    !! Requires derivative function df
    !! @param f Function to find root of
    !! @param df Derivative of f
    !! @param x0 Initial guess
    !! @param tolerance Desired accuracy (optional)
    !! @param max_iter Maximum iterations (optional)
    !! @return root_result with found root and status
    function newton_raphson(f, df, x0, tolerance, max_iter) result(res)
        procedure(func_interface) :: f, df
        real(8), intent(in) :: x0
        real(8), intent(in), optional :: tolerance
        integer, intent(in), optional :: max_iter
        type(root_result) :: res
        
        real(8) :: tol, x, fx, dfx, dx
        integer :: maxit, iter
        
        tol = DEFAULT_TOLERANCE
        if (present(tolerance)) tol = tolerance
        maxit = DEFAULT_MAX_ITER
        if (present(max_iter)) maxit = max_iter
        
        res%method = "Newton-Raphson"
        res%converged = .false.
        res%iterations = 0
        
        x = x0
        
        do iter = 1, maxit
            fx = f(x)
            dfx = df(x)
            
            res%iterations = iter
            res%root = x
            res%residual = fx
            
            ! Check convergence
            if (abs(fx) < tol) then
                res%converged = .true.
                write(res%message, '(A,I0,A)') "Converged in ", iter, " iterations"
                return
            end if
            
            ! Check for zero derivative
            if (abs(dfx) < EPSILON) then
                res%message = "Error: Zero derivative encountered"
                return
            end if
            
            ! Newton step
            dx = fx / dfx
            x = x - dx
            
            ! Check for convergence by step size
            if (abs(dx) < tol) then
                res%converged = .true.
                res%root = x
                res%residual = f(x)
                write(res%message, '(A,I0,A)') "Converged in ", iter, " iterations"
                return
            end if
        end do
        
        res%message = "Warning: Maximum iterations reached"
    end function newton_raphson
    
    !==========================================================================
    ! Secant Method
    !==========================================================================
    
    !> Secant method for finding root of f(x)
    !! Does not require derivative
    !! @param f Function to find root of
    !! @param x0 First initial guess
    !! @param x1 Second initial guess
    !! @param tolerance Desired accuracy (optional)
    !! @param max_iter Maximum iterations (optional)
    !! @return root_result with found root and status
    function secant(f, x0, x1, tolerance, max_iter) result(res)
        procedure(func_interface) :: f
        real(8), intent(in) :: x0, x1
        real(8), intent(in), optional :: tolerance
        integer, intent(in), optional :: max_iter
        type(root_result) :: res
        
        real(8) :: tol, xa, xb, fa, fb, xnew, dx
        integer :: maxit, iter
        
        tol = DEFAULT_TOLERANCE
        if (present(tolerance)) tol = tolerance
        maxit = DEFAULT_MAX_ITER
        if (present(max_iter)) maxit = max_iter
        
        res%method = "Secant"
        res%converged = .false.
        res%iterations = 0
        
        xa = x0
        xb = x1
        fa = f(xa)
        fb = f(xb)
        
        do iter = 1, maxit
            res%iterations = iter
            
            ! Check if we're close enough
            if (abs(fb) < tol) then
                res%root = xb
                res%residual = fb
                res%converged = .true.
                write(res%message, '(A,I0,A)') "Converged in ", iter, " iterations"
                return
            end if
            
            ! Check for division by zero
            if (abs(fb - fa) < EPSILON) then
                res%root = xb
                res%residual = fb
                res%message = "Error: Secant denominator too small"
                return
            end if
            
            ! Secant step
            xnew = xb - fb * (xb - xa) / (fb - fa)
            
            ! Update
            xa = xb
            fa = fb
            xb = xnew
            fb = f(xb)
            
            ! Check convergence by step size
            if (abs(xb - xa) < tol) then
                res%root = xb
                res%residual = fb
                res%converged = .true.
                write(res%message, '(A,I0,A)') "Converged in ", iter, " iterations"
                return
            end if
        end do
        
        res%root = xb
        res%residual = fb
        res%message = "Warning: Maximum iterations reached"
    end function secant
    
    !==========================================================================
    ! False Position (Regula Falsi) Method
    !==========================================================================
    
    !> False Position (Regula Falsi) method for finding root of f(x)
    !! Combines bisection guarantee with secant speed
    !! @param f Function to find root of
    !! @param a Left endpoint
    !! @param b Right endpoint
    !! @param tolerance Desired accuracy (optional)
    !! @param max_iter Maximum iterations (optional)
    !! @return root_result with found root and status
    function false_position(f, a, b, tolerance, max_iter) result(res)
        procedure(func_interface) :: f
        real(8), intent(in) :: a, b
        real(8), intent(in), optional :: tolerance
        integer, intent(in), optional :: max_iter
        type(root_result) :: res
        
        real(8) :: tol, xa, xb, fa, fb, c, fc
        integer :: maxit, iter
        
        tol = DEFAULT_TOLERANCE
        if (present(tolerance)) tol = tolerance
        maxit = DEFAULT_MAX_ITER
        if (present(max_iter)) maxit = max_iter
        
        res%method = "False Position"
        res%converged = .false.
        res%iterations = 0
        
        xa = a
        xb = b
        fa = f(xa)
        fb = f(xb)
        
        ! Check endpoints (using tolerance)
        if (abs(fa) < tol) then
            res%root = xa
            res%residual = fa
            res%converged = .true.
            res%message = "Root found at left endpoint"
            return
        end if
        
        if (abs(fb) < tol) then
            res%root = xb
            res%residual = fb
            res%converged = .true.
            res%message = "Root found at right endpoint"
            return
        end if
        
        ! Check for valid interval
        if (fa * fb > 0.0d0) then
            res%root = (xa + xb) / 2.0d0
            res%residual = f(res%root)
            res%message = "Error: f(a) and f(b) must have opposite signs"
            return
        end if
        
        do iter = 1, maxit
            res%iterations = iter
            
            ! False position step
            c = (xa * fb - xb * fa) / (fb - fa)
            fc = f(c)
            
            res%root = c
            res%residual = fc
            
            ! Check convergence
            if (abs(fc) < tol) then
                res%converged = .true.
                write(res%message, '(A,I0,A)') "Converged in ", iter, " iterations"
                return
            end if
            
            ! Update interval
            if (fa * fc < 0.0d0) then
                xb = c
                fb = fc
            else
                xa = c
                fa = fc
            end if
            
            ! Check interval size
            if (abs(xb - xa) < tol) then
                res%converged = .true.
                write(res%message, '(A,I0,A)') "Converged in ", iter, " iterations"
                return
            end if
        end do
        
        res%message = "Warning: Maximum iterations reached"
    end function false_position
    
    !==========================================================================
    ! Brent's Method
    !==========================================================================
    
    !> Brent's method for finding root of f(x)
    !! Robust hybrid method combining bisection, secant, and inverse quadratic interpolation
    !! Based on Brent's algorithm (1973)
    !! @param f Function to find root of
    !! @param a Left endpoint
    !! @param b Right endpoint
    !! @param tolerance Desired accuracy (optional)
    !! @param max_iter Maximum iterations (optional)
    !! @return root_result with found root and status
    function brent(f, a, b, tolerance, max_iter) result(res)
        procedure(func_interface) :: f
        real(8), intent(in) :: a, b
        real(8), intent(in), optional :: tolerance
        integer, intent(in), optional :: max_iter
        type(root_result) :: res
        
        real(8) :: tol
        integer :: maxit, iter
        real(8) :: xa, xb, xc, fa, fb, fc
        real(8) :: s, p, q, r, t, xm
        real(8) :: tol1, d, e
        
        tol = DEFAULT_TOLERANCE
        if (present(tolerance)) tol = tolerance
        maxit = DEFAULT_MAX_ITER
        if (present(max_iter)) maxit = max_iter
        
        res%method = "Brent"
        res%converged = .false.
        res%iterations = 0
        
        xa = a
        xb = b
        fa = f(xa)
        fb = f(xb)
        
        ! Check endpoints (using tolerance)
        if (abs(fa) < tol) then
            res%root = xa
            res%residual = fa
            res%converged = .true.
            res%message = "Root found at left endpoint"
            return
        end if
        
        if (abs(fb) < tol) then
            res%root = xb
            res%residual = fb
            res%converged = .true.
            res%message = "Root found at right endpoint"
            return
        end if
        
        ! Check for valid interval
        if (fa * fb > 0.0d0) then
            res%root = (xa + xb) / 2.0d0
            res%residual = f(res%root)
            res%message = "Error: f(a) and f(b) must have opposite signs"
            return
        end if
        
        ! Setup - ensure |fa| >= |fb| so b is the better estimate
        if (abs(fa) < abs(fb)) then
            t = xa; xa = xb; xb = t
            t = fa; fa = fb; fb = t
        end if
        
        xc = xa
        fc = fa
        e = 0.0d0
        d = 0.0d0
        
        do iter = 1, maxit
            res%iterations = iter
            tol1 = 2.0d0 * EPSILON * abs(xb) + 0.5d0 * tol
            
            xm = 0.5d0 * (xa - xb)
            
            ! Test for convergence
            if (abs(fb) <= tol .or. abs(xm) <= tol1) then
                res%root = xb
                res%residual = fb
                res%converged = .true.
                write(res%message, '(A,I0,A)') "Converged in ", iter, " iterations"
                return
            end if
            
            ! Test for bisection condition
            if (abs(e) >= tol1 .and. abs(fc) > abs(fb)) then
                ! Inverse quadratic or secant interpolation
                s = fb / fc
                if (abs(xa - xc) > EPSILON) then
                    ! Inverse quadratic interpolation
                    q = fb / fa
                    r = fb / fc
                    s = xb - (r * (xb - xc) * q - q * (xb - xa)) / (s - 1.0d0) * (q - r)
                    p = s - xb
                else
                    ! Secant interpolation
                    s = xb - (xb - xa) * fb / (fb - fa)
                    p = s - xb
                end if
                
                ! Check if interpolation is acceptable
                if (abs(p) < abs(0.5d0 * xm) .and. p > xm .and. p < 3.0d0 * tol1 - xm) then
                    ! Accept interpolation
                    d = p
                    e = d
                else
                    ! Use bisection
                    d = xm
                    e = d
                end if
            else
                ! Use bisection
                d = xm
                e = d
            end if
            
            xc = xb
            fc = fb
            
            if (abs(d) > tol1) then
                xb = xb + d
            else
                if (xm > 0.0d0) then
                    xb = xb + tol1
                else
                    xb = xb - tol1
                end if
            end if
            
            fb = f(xb)
            
            ! Maintain bracket on root
            if (fb * fa > 0.0d0) then
                xa = xc
                fa = fc
            else
                ! xa stays the same, fa stays the same
            end if
            
            ! Ensure b is the best estimate
            if (abs(fa) < abs(fb)) then
                t = xa; xa = xb; xb = t
                t = fa; fa = fb; fb = t
            end if
        end do
        
        res%root = xb
        res%residual = fb
        res%message = "Warning: Maximum iterations reached"
    end function brent
    
    !==========================================================================
    ! Fixed-Point Iteration
    !==========================================================================
    
    !> Fixed-point iteration for finding root
    !! Solves x = g(x) where f(x) = x - g(x)
    !! @param g Fixed-point function g(x)
    !! @param x0 Initial guess
    !! @param tolerance Desired accuracy (optional)
    !! @param max_iter Maximum iterations (optional)
    !! @param relaxation Relaxation factor (optional, default 1.0)
    !! @return root_result with found root and status
    function fixed_point(g, x0, tolerance, max_iter, relaxation) result(res)
        procedure(func_interface) :: g
        real(8), intent(in) :: x0
        real(8), intent(in), optional :: tolerance, relaxation
        integer, intent(in), optional :: max_iter
        type(root_result) :: res
        
        real(8) :: tol, w, x, xnew, diff
        integer :: maxit, iter
        
        tol = DEFAULT_TOLERANCE
        if (present(tolerance)) tol = tolerance
        maxit = DEFAULT_MAX_ITER
        if (present(max_iter)) maxit = max_iter
        w = 1.0d0
        if (present(relaxation)) w = relaxation
        
        res%method = "Fixed-Point Iteration"
        res%converged = .false.
        res%iterations = 0
        
        x = x0
        
        do iter = 1, maxit
            xnew = (1.0d0 - w) * x + w * g(x)
            diff = abs(xnew - x)
            
            res%iterations = iter
            res%root = xnew
            
            ! Check convergence
            if (diff < tol) then
                res%converged = .true.
                res%residual = xnew - g(xnew)
                write(res%message, '(A,I0,A)') "Converged in ", iter, " iterations"
                return
            end if
            
            x = xnew
        end do
        
        res%residual = x - g(x)
        res%message = "Warning: Maximum iterations reached"
    end function fixed_point
    
    !==========================================================================
    ! Ridder's Method
    !==========================================================================
    
    !> Ridder's method for finding root of f(x)
    !! Efficient method using exponential fit
    !! @param f Function to find root of
    !! @param a Left endpoint
    !! @param b Right endpoint
    !! @param tolerance Desired accuracy (optional)
    !! @param max_iter Maximum iterations (optional)
    !! @return root_result with found root and status
    function ridder(f, a, b, tolerance, max_iter) result(res)
        procedure(func_interface) :: f
        real(8), intent(in) :: a, b
        real(8), intent(in), optional :: tolerance
        integer, intent(in), optional :: max_iter
        type(root_result) :: res
        
        real(8) :: tol, xa, xb, xc, xd, fa, fb, fc, fd, s, xm
        integer :: maxit, iter
        
        tol = DEFAULT_TOLERANCE
        if (present(tolerance)) tol = tolerance
        maxit = DEFAULT_MAX_ITER
        if (present(max_iter)) maxit = max_iter
        
        res%method = "Ridder"
        res%converged = .false.
        res%iterations = 0
        
        xa = a
        xb = b
        fa = f(xa)
        fb = f(xb)
        
        ! Check endpoints (using tolerance)
        if (abs(fa) < tol) then
            res%root = xa
            res%residual = fa
            res%converged = .true.
            res%message = "Root found at left endpoint"
            return
        end if
        
        if (abs(fb) < tol) then
            res%root = xb
            res%residual = fb
            res%converged = .true.
            res%message = "Root found at right endpoint"
            return
        end if
        
        ! Check for valid interval
        if (fa * fb > 0.0d0) then
            res%root = (xa + xb) / 2.0d0
            res%residual = f(res%root)
            res%message = "Error: f(a) and f(b) must have opposite signs"
            return
        end if
        
        do iter = 1, maxit
            res%iterations = iter
            
            ! Midpoint
            xc = (xa + xb) / 2.0d0
            fc = f(xc)
            
            ! Check convergence
            if (abs(fc) < tol) then
                res%root = xc
                res%residual = fc
                res%converged = .true.
                write(res%message, '(A,I0,A)') "Converged in ", iter, " iterations"
                return
            end if
            
            ! Ridder's formula
            s = sqrt(fc * fc - fa * fb)
            if (s == 0.0d0) then
                res%root = xc
                res%residual = fc
                res%message = "Error: Ridder method failed (s=0)"
                return
            end if
            
            ! New estimate
            xd = xc + (xc - xa) * sign(1.0d0, fa - fb) * fc / s
            fd = f(xd)
            
            ! Check convergence
            if (abs(fd) < tol) then
                res%root = xd
                res%residual = fd
                res%converged = .true.
                write(res%message, '(A,I0,A)') "Converged in ", iter, " iterations"
                return
            end if
            
            ! Update bracket
            if (fc * fd < 0.0d0) then
                xa = xc
                fa = fc
                xb = xd
                fb = fd
            else if (fa * fd < 0.0d0) then
                xb = xd
                fb = fd
            else
                xa = xd
                fa = fd
            end if
            
            ! Check interval size
            if (abs(xb - xa) < tol) then
                res%root = (xa + xb) / 2.0d0
                res%residual = f(res%root)
                res%converged = .true.
                write(res%message, '(A,I0,A)') "Converged in ", iter, " iterations"
                return
            end if
        end do
        
        res%root = (xa + xb) / 2.0d0
        res%residual = f(res%root)
        res%message = "Warning: Maximum iterations reached"
    end function ridder
    
    !==========================================================================
    ! Numerical Derivative (for methods that don't have analytical derivatives)
    !==========================================================================
    
    !> Compute numerical derivative using central difference
    !! @param f Function to differentiate
    !! @param x Point to compute derivative at
    !! @param h Step size (optional, default 1e-8)
    !! @return Approximate derivative
    function numerical_derivative(f, x, h) result(df)
        procedure(func_interface) :: f
        real(8), intent(in) :: x
        real(8), intent(in), optional :: h
        real(8) :: df, step
        
        step = 1.0d-8
        if (present(h)) step = h
        
        df = (f(x + step) - f(x - step)) / (2.0d0 * step)
    end function numerical_derivative
    
    !==========================================================================
    ! Newton-Raphson with Numerical Derivative
    !==========================================================================
    
    !> Newton-Raphson method with numerical derivative
    !! @param f Function to find root of
    !! @param x0 Initial guess
    !! @param tolerance Desired accuracy (optional)
    !! @param max_iter Maximum iterations (optional)
    !! @return root_result with found root and status
    function newton_raphson_numerical(f, x0, tolerance, max_iter) result(res)
        procedure(func_interface) :: f
        real(8), intent(in) :: x0
        real(8), intent(in), optional :: tolerance
        integer, intent(in), optional :: max_iter
        type(root_result) :: res
        
        real(8) :: tol, x, fx, dfx, dx
        integer :: maxit, iter
        
        tol = DEFAULT_TOLERANCE
        if (present(tolerance)) tol = tolerance
        maxit = DEFAULT_MAX_ITER
        if (present(max_iter)) maxit = max_iter
        
        res%method = "Newton-Raphson (Numerical)"
        res%converged = .false.
        res%iterations = 0
        
        x = x0
        
        do iter = 1, maxit
            fx = f(x)
            dfx = numerical_derivative(f, x)
            
            res%iterations = iter
            res%root = x
            res%residual = fx
            
            if (abs(fx) < tol) then
                res%converged = .true.
                write(res%message, '(A,I0,A)') "Converged in ", iter, " iterations"
                return
            end if
            
            if (abs(dfx) < EPSILON) then
                res%message = "Error: Zero derivative encountered"
                return
            end if
            
            dx = fx / dfx
            x = x - dx
            
            if (abs(dx) < tol) then
                res%converged = .true.
                res%root = x
                res%residual = f(x)
                write(res%message, '(A,I0,A)') "Converged in ", iter, " iterations"
                return
            end if
        end do
        
        res%message = "Warning: Maximum iterations reached"
    end function newton_raphson_numerical
    
    !==========================================================================
    ! Multi-Root Finder (finds multiple roots in an interval)
    !==========================================================================
    
    !> Find multiple roots by dividing interval and applying Brent's method
    !! @param f Function to find roots of
    !! @param a Left endpoint
    !! @param b Right endpoint
    !! @param n_intervals Number of subintervals to search
    !! @param tolerance Desired accuracy (optional)
    !! @return Array of roots found (limited to reasonable size)
    function find_multiple_roots(f, a, b, n_intervals, tolerance) result(roots)
        procedure(func_interface) :: f
        real(8), intent(in) :: a, b
        integer, intent(in) :: n_intervals
        real(8), intent(in), optional :: tolerance
        real(8), allocatable :: roots(:)
        
        real(8) :: tol, step, xa, xb, fa, fb
        integer :: i, n_found, max_roots
        type(root_result) :: r
        real(8) :: temp_roots(100)
        
        tol = DEFAULT_TOLERANCE
        if (present(tolerance)) tol = tolerance
        
        max_roots = 100
        n_found = 0
        step = (b - a) / real(n_intervals, 8)
        
        do i = 1, n_intervals
            xa = a + (i - 1) * step
            xb = a + i * step
            fa = f(xa)
            fb = f(xb)
            
            ! Check for sign change (potential root)
            if (fa * fb <= 0.0d0) then
                r = brent(f, xa, xb, tol)
                if (r%converged) then
                    ! Check if this root is already found
                    if (.not. is_duplicate(temp_roots, n_found, r%root, tol * 100.0d0)) then
                        n_found = n_found + 1
                        temp_roots(n_found) = r%root
                    end if
                end if
            end if
        end do
        
        ! Allocate and return
        allocate(roots(n_found))
        if (n_found > 0) then
            roots = temp_roots(1:n_found)
        end if
    end function find_multiple_roots
    
    !> Helper to check for duplicate roots
    function is_duplicate(roots, n, candidate, tolerance) result(is_dup)
        real(8), intent(in) :: roots(:)
        integer, intent(in) :: n
        real(8), intent(in) :: candidate, tolerance
        logical :: is_dup
        integer :: i
        
        is_dup = .false.
        do i = 1, n
            if (abs(roots(i) - candidate) < tolerance) then
                is_dup = .true.
                return
            end if
        end do
    end function is_duplicate

end module root_finding_utils