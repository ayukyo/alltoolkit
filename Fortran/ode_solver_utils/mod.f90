!! AllToolkit - Fortran ODE Solver Utilities
!! Zero-dependency ordinary differential equation solvers for Fortran 90/95/2003+
!!
!! Features:
!! - Forward Euler method (1st order)
!! - Backward Euler method (implicit, 1st order)
!! - Heun's method (2nd order Runge-Kutta)
!! - Midpoint method (2nd order Runge-Kutta)
!! - Classic Runge-Kutta 4th order method (RK4)
!! - Runge-Kutta-Fehlberg method (RKF45, adaptive step)
!! - Dormand-Prince method (DOPRI5, adaptive step)
!!
!! Author: AllToolkit Contributors
!! License: MIT

module ode_solver_utils
    implicit none
    
    ! Module parameters
    real(8), parameter :: ODE_EPSILON = 1.0d-12
    real(8), parameter :: DEFAULT_RTOL = 1.0d-6
    real(8), parameter :: DEFAULT_ATOL = 1.0d-9
    integer, parameter :: MAX_ITERATIONS = 10000
    integer, parameter :: MAX_NEWTON_ITER = 50
    
    ! Result type for ODE solutions
    type ode_solution
        integer :: n_steps
        real(8), allocatable :: t(:)      ! Time points
        real(8), allocatable :: y(:,:)    ! Solution values (n_points, n_vars)
        integer :: n_evals                ! Number of function evaluations
        logical :: success                ! Whether integration succeeded
        character(len=256) :: message     ! Status message
    end type ode_solution
    
    ! Adaptive step result
    type adaptive_result
        real(8) :: y_new(100)             ! New solution (max 100 variables)
        real(8) :: h_new                  ! Suggested new step size
        real(8) :: error                  ! Estimated error
        logical :: accepted               ! Whether step was accepted
    end type adaptive_result
    
contains
    
    ! =========================================================================
    ! Forward Euler Method (1st order, explicit)
    ! =========================================================================
    
    subroutine forward_euler(f, t0, y0, h, n_steps, t_out, y_out, n_vars)
        !! Forward Euler method for solving ODEs
        !! dy/dt = f(t, y)
        !!
        !! Arguments:
        !!   f       - Derivative function f(t, y)
        !!   t0      - Initial time
        !!   y0      - Initial values (array of n_vars)
        !!   h       - Step size
        !!   n_steps - Number of steps
        !!   t_out   - Output time array
        !!   y_out   - Output solution array (n_steps+1, n_vars)
        !!   n_vars  - Number of variables
        
        implicit none
        
        interface
            subroutine f(t, y, dydt)
                real(8), intent(in) :: t
                real(8), intent(in) :: y(:)
                real(8), intent(out) :: dydt(:)
            end subroutine f
        end interface
        
        real(8), intent(in) :: t0, h
        real(8), intent(in) :: y0(:)
        integer, intent(in) :: n_steps, n_vars
        real(8), intent(out) :: t_out(:)
        real(8), intent(out) :: y_out(:,:)
        
        real(8), allocatable :: dydt(:), y(:)
        integer :: i
        
        allocate(dydt(n_vars), y(n_vars))
        
        ! Initialize
        t_out(1) = t0
        y_out(1,:) = y0
        y = y0
        
        ! Time stepping
        do i = 1, n_steps
            call f(t_out(i), y, dydt)
            y = y + h * dydt
            t_out(i+1) = t_out(i) + h
            y_out(i+1,:) = y
        end do
        
        deallocate(dydt, y)
    end subroutine forward_euler
    
    ! =========================================================================
    ! Backward Euler Method (1st order, implicit)
    ! =========================================================================
    
    subroutine backward_euler(f, t0, y0, h, n_steps, t_out, y_out, n_vars, tol)
        !! Backward Euler method (implicit) for stiff ODEs
        !! Uses Newton-Raphson iteration to solve implicit equation
        !!
        !! Arguments:
        !!   f       - Derivative function f(t, y)
        !!   t0      - Initial time
        !!   y0      - Initial values
        !!   h       - Step size
        !!   n_steps - Number of steps
        !!   t_out   - Output time array
        !!   y_out   - Output solution array
        !!   n_vars  - Number of variables
        !!   tol     - Newton iteration tolerance (optional)
        
        implicit none
        
        interface
            subroutine f(t, y, dydt)
                real(8), intent(in) :: t
                real(8), intent(in) :: y(:)
                real(8), intent(out) :: dydt(:)
            end subroutine f
        end interface
        
        real(8), intent(in) :: t0, h
        real(8), intent(in) :: y0(:)
        integer, intent(in) :: n_steps, n_vars
        real(8), intent(out) :: t_out(:)
        real(8), intent(out) :: y_out(:,:)
        real(8), intent(in), optional :: tol
        
        real(8) :: tolerance, t_current
        real(8), allocatable :: y(:), y_new(:), dydt(:), y_old(:)
        integer :: i, iter
        
        tolerance = ODE_EPSILON
        if (present(tol)) tolerance = tol
        
        allocate(y(n_vars), y_new(n_vars), dydt(n_vars), y_old(n_vars))
        
        ! Initialize
        t_out(1) = t0
        y_out(1,:) = y0
        y = y0
        t_current = t0
        
        ! Time stepping
        do i = 1, n_steps
            ! Initial guess using forward Euler
            call f(t_current, y, dydt)
            y_new = y + h * dydt
            t_current = t_current + h
            
            ! Newton-Raphson iteration: y_{n+1} = y_n + h * f(t_{n+1}, y_{n+1})
            do iter = 1, MAX_NEWTON_ITER
                y_old = y_new
                call f(t_current, y_new, dydt)
                y_new = y + h * dydt
                
                ! Check convergence
                if (maxval(abs(y_new - y_old)) < tolerance) exit
            end do
            
            y = y_new
            t_out(i+1) = t_current
            y_out(i+1,:) = y
        end do
        
        deallocate(y, y_new, dydt, y_old)
    end subroutine backward_euler
    
    ! =========================================================================
    ! Heun's Method (2nd order Runge-Kutta, improved Euler)
    ! =========================================================================
    
    subroutine heun_method(f, t0, y0, h, n_steps, t_out, y_out, n_vars)
        !! Heun's method (2nd order Runge-Kutta)
        !! Also known as improved Euler or modified Euler
        !!
        !! k1 = f(t_n, y_n)
        !! k2 = f(t_n + h, y_n + h*k1)
        !! y_{n+1} = y_n + h/2 * (k1 + k2)
        
        implicit none
        
        interface
            subroutine f(t, y, dydt)
                real(8), intent(in) :: t
                real(8), intent(in) :: y(:)
                real(8), intent(out) :: dydt(:)
            end subroutine f
        end interface
        
        real(8), intent(in) :: t0, h
        real(8), intent(in) :: y0(:)
        integer, intent(in) :: n_steps, n_vars
        real(8), intent(out) :: t_out(:)
        real(8), intent(out) :: y_out(:,:)
        
        real(8), allocatable :: y(:), k1(:), k2(:)
        real(8) :: t_current
        integer :: i
        
        allocate(y(n_vars), k1(n_vars), k2(n_vars))
        
        ! Initialize
        t_out(1) = t0
        y_out(1,:) = y0
        y = y0
        t_current = t0
        
        ! Time stepping
        do i = 1, n_steps
            call f(t_current, y, k1)
            call f(t_current + h, y + h*k1, k2)
            y = y + h * 0.5d0 * (k1 + k2)
            t_current = t_current + h
            t_out(i+1) = t_current
            y_out(i+1,:) = y
        end do
        
        deallocate(y, k1, k2)
    end subroutine heun_method
    
    ! =========================================================================
    ! Midpoint Method (2nd order Runge-Kutta)
    ! =========================================================================
    
    subroutine midpoint_method(f, t0, y0, h, n_steps, t_out, y_out, n_vars)
        !! Midpoint method (2nd order Runge-Kutta)
        !!
        !! k1 = f(t_n, y_n)
        !! k2 = f(t_n + h/2, y_n + h/2 * k1)
        !! y_{n+1} = y_n + h * k2
        
        implicit none
        
        interface
            subroutine f(t, y, dydt)
                real(8), intent(in) :: t
                real(8), intent(in) :: y(:)
                real(8), intent(out) :: dydt(:)
            end subroutine f
        end interface
        
        real(8), intent(in) :: t0, h
        real(8), intent(in) :: y0(:)
        integer, intent(in) :: n_steps, n_vars
        real(8), intent(out) :: t_out(:)
        real(8), intent(out) :: y_out(:,:)
        
        real(8), allocatable :: y(:), k1(:), k2(:)
        real(8) :: t_current
        integer :: i
        
        allocate(y(n_vars), k1(n_vars), k2(n_vars))
        
        ! Initialize
        t_out(1) = t0
        y_out(1,:) = y0
        y = y0
        t_current = t0
        
        ! Time stepping
        do i = 1, n_steps
            call f(t_current, y, k1)
            call f(t_current + 0.5d0*h, y + 0.5d0*h*k1, k2)
            y = y + h * k2
            t_current = t_current + h
            t_out(i+1) = t_current
            y_out(i+1,:) = y
        end do
        
        deallocate(y, k1, k2)
    end subroutine midpoint_method
    
    ! =========================================================================
    ! Classic Runge-Kutta 4th Order Method (RK4)
    ! =========================================================================
    
    subroutine rk4(f, t0, y0, h, n_steps, t_out, y_out, n_vars)
        !! Classic 4th order Runge-Kutta method
        !!
        !! k1 = f(t_n, y_n)
        !! k2 = f(t_n + h/2, y_n + h/2 * k1)
        !! k3 = f(t_n + h/2, y_n + h/2 * k2)
        !! k4 = f(t_n + h, y_n + h * k3)
        !! y_{n+1} = y_n + h/6 * (k1 + 2*k2 + 2*k3 + k4)
        
        implicit none
        
        interface
            subroutine f(t, y, dydt)
                real(8), intent(in) :: t
                real(8), intent(in) :: y(:)
                real(8), intent(out) :: dydt(:)
            end subroutine f
        end interface
        
        real(8), intent(in) :: t0, h
        real(8), intent(in) :: y0(:)
        integer, intent(in) :: n_steps, n_vars
        real(8), intent(out) :: t_out(:)
        real(8), intent(out) :: y_out(:,:)
        
        real(8), allocatable :: y(:), k1(:), k2(:), k3(:), k4(:)
        real(8) :: t_current
        integer :: i
        
        allocate(y(n_vars), k1(n_vars), k2(n_vars), k3(n_vars), k4(n_vars))
        
        ! Initialize
        t_out(1) = t0
        y_out(1,:) = y0
        y = y0
        t_current = t0
        
        ! Time stepping
        do i = 1, n_steps
            call f(t_current, y, k1)
            call f(t_current + 0.5d0*h, y + 0.5d0*h*k1, k2)
            call f(t_current + 0.5d0*h, y + 0.5d0*h*k2, k3)
            call f(t_current + h, y + h*k3, k4)
            
            y = y + h * (k1 + 2.0d0*k2 + 2.0d0*k3 + k4) / 6.0d0
            t_current = t_current + h
            t_out(i+1) = t_current
            y_out(i+1,:) = y
        end do
        
        deallocate(y, k1, k2, k3, k4)
    end subroutine rk4
    
    ! =========================================================================
    ! Runge-Kutta-Fehlberg Method (RKF45, Adaptive Step Size)
    ! =========================================================================
    
    subroutine rkf45(f, t0, t_end, y0, h_init, rtol, atol, t_out, y_out, &
                      n_steps, n_vars, max_steps, n_evals)
        !! Runge-Kutta-Fehlberg method with adaptive step size
        !! Uses 4th and 5th order methods to estimate error
        !!
        !! Arguments:
        !!   f         - Derivative function
        !!   t0        - Initial time
        !!   t_end     - Final time
        !!   y0        - Initial values
        !!   h_init    - Initial step size
        !!   rtol      - Relative tolerance
        !!   atol      - Absolute tolerance
        !!   t_out     - Output time array
        !!   y_out     - Output solution array
        !!   n_steps   - Number of steps actually taken (output)
        !!   n_vars    - Number of variables
        !!   max_steps - Maximum number of steps allowed
        !!   n_evals   - Number of function evaluations (output)
        
        implicit none
        
        interface
            subroutine f(t, y, dydt)
                real(8), intent(in) :: t
                real(8), intent(in) :: y(:)
                real(8), intent(out) :: dydt(:)
            end subroutine f
        end interface
        
        real(8), intent(in) :: t0, t_end, h_init, rtol, atol
        real(8), intent(in) :: y0(:)
        real(8), intent(out) :: t_out(:)
        real(8), intent(out) :: y_out(:,:)
        integer, intent(out) :: n_steps
        integer, intent(in) :: n_vars, max_steps
        integer, intent(out) :: n_evals
        
        ! RKF45 coefficients
        real(8), parameter :: a2 = 1.0d0/4.0d0
        real(8), parameter :: a3 = 3.0d0/8.0d0
        real(8), parameter :: a4 = 12.0d0/13.0d0
        real(8), parameter :: a5 = 1.0d0
        real(8), parameter :: a6 = 1.0d0/2.0d0
        
        real(8), parameter :: b21 = 1.0d0/4.0d0
        real(8), parameter :: b31 = 3.0d0/32.0d0
        real(8), parameter :: b32 = 9.0d0/32.0d0
        real(8), parameter :: b41 = 1932.0d0/2197.0d0
        real(8), parameter :: b42 = -7200.0d0/2197.0d0
        real(8), parameter :: b43 = 7296.0d0/2197.0d0
        real(8), parameter :: b51 = 439.0d0/216.0d0
        real(8), parameter :: b52 = -8.0d0
        real(8), parameter :: b53 = 3680.0d0/513.0d0
        real(8), parameter :: b54 = -845.0d0/4104.0d0
        real(8), parameter :: b61 = -8.0d0/27.0d0
        real(8), parameter :: b62 = 2.0d0
        real(8), parameter :: b63 = -3544.0d0/2565.0d0
        real(8), parameter :: b64 = 1859.0d0/4104.0d0
        real(8), parameter :: b65 = -11.0d0/40.0d0
        
        ! 4th order coefficients
        real(8), parameter :: c1 = 25.0d0/216.0d0
        real(8), parameter :: c3 = 1408.0d0/2565.0d0
        real(8), parameter :: c4 = 2197.0d0/4104.0d0
        real(8), parameter :: c5 = -1.0d0/5.0d0
        
        ! 5th order coefficients
        real(8), parameter :: d1 = 16.0d0/135.0d0
        real(8), parameter :: d3 = 6656.0d0/12825.0d0
        real(8), parameter :: d4 = 28561.0d0/56430.0d0
        real(8), parameter :: d5 = -9.0d0/50.0d0
        real(8), parameter :: d6 = 2.0d0/55.0d0
        
        real(8), allocatable :: y(:), k1(:), k2(:), k3(:), k4(:), k5(:), k6(:)
        real(8), allocatable :: y4(:), y5(:), err_vec(:), scale(:)
        real(8) :: t_current, h, err, h_new
        integer :: i
        
        allocate(y(n_vars), k1(n_vars), k2(n_vars), k3(n_vars), k4(n_vars), &
                 k5(n_vars), k6(n_vars), y4(n_vars), y5(n_vars), err_vec(n_vars), scale(n_vars))
        
        ! Initialize
        t_out(1) = t0
        y_out(1,:) = y0
        y = y0
        t_current = t0
        h = h_init
        n_steps = 1
        n_evals = 0
        
        ! Adaptive stepping
        do while (t_current < t_end .and. n_steps < max_steps)
            ! Ensure last step reaches t_end
            if (t_current + h > t_end) h = t_end - t_current
            
            ! Compute RKF45 stages
            call f(t_current, y, k1)
            call f(t_current + a2*h, y + b21*h*k1, k2)
            call f(t_current + a3*h, y + b31*h*k1 + b32*h*k2, k3)
            call f(t_current + a4*h, y + b41*h*k1 + b42*h*k2 + b43*h*k3, k4)
            call f(t_current + a5*h, y + b51*h*k1 + b52*h*k2 + b53*h*k3 + b54*h*k4, k5)
            call f(t_current + a6*h, y + b61*h*k1 + b62*h*k2 + b63*h*k3 + b64*h*k4 + b65*h*k5, k6)
            
            n_evals = n_evals + 6
            
            ! 4th order solution
            y4 = y + h * (c1*k1 + c3*k3 + c4*k4 + c5*k5)
            
            ! 5th order solution
            y5 = y + h * (d1*k1 + d3*k3 + d4*k4 + d5*k5 + d6*k6)
            
            ! Error estimation
            err_vec = abs(y5 - y4)
            scale = atol + rtol * max(abs(y), abs(y5))
            err = maxval(err_vec / scale)
            
            if (err <= 1.0d0) then
                ! Accept step
                y = y5
                t_current = t_current + h
                n_steps = n_steps + 1
                t_out(n_steps) = t_current
                y_out(n_steps,:) = y
            end if
            
            ! Adjust step size
            if (err > 1.0d-15) then
                h_new = 0.9d0 * h * (1.0d0 / err) ** 0.2d0
            else
                h_new = 2.0d0 * h
            end if
            
            h = min(max(h_new, 0.1d0*h), 5.0d0*h)  ! Limit step size change
        end do
        
        deallocate(y, k1, k2, k3, k4, k5, k6, y4, y5, err_vec, scale)
    end subroutine rkf45
    
    ! =========================================================================
    ! Dormand-Prince Method (DOPRI5, Adaptive Step Size)
    ! =========================================================================
    
    subroutine dopri5_step(f, t, y, h, y_new, err, n_vars, n_evals)
        !! Single step of Dormand-Prince method (DOPRI5)
        !! Returns new y and error estimate
        
        implicit none
        
        interface
            subroutine f(t, y, dydt)
                real(8), intent(in) :: t
                real(8), intent(in) :: y(:)
                real(8), intent(out) :: dydt(:)
            end subroutine f
        end interface
        
        real(8), intent(in) :: t, h
        real(8), intent(in) :: y(:)
        real(8), intent(out) :: y_new(:), err(:)
        integer, intent(in) :: n_vars
        integer, intent(out) :: n_evals
        
        real(8), allocatable :: k1(:), k2(:), k3(:), k4(:), k5(:), k6(:), k7(:)
        real(8), allocatable :: y5(:)
        
        ! DOPRI5 coefficients (Butcher tableau)
        real(8), parameter :: c2 = 1.0d0/5.0d0
        real(8), parameter :: c3 = 3.0d0/10.0d0
        real(8), parameter :: c4 = 4.0d0/5.0d0
        real(8), parameter :: c5 = 8.0d0/9.0d0
        
        real(8), parameter :: a21 = 1.0d0/5.0d0
        real(8), parameter :: a31 = 3.0d0/40.0d0
        real(8), parameter :: a32 = 9.0d0/40.0d0
        real(8), parameter :: a41 = 44.0d0/45.0d0
        real(8), parameter :: a42 = -56.0d0/15.0d0
        real(8), parameter :: a43 = 32.0d0/9.0d0
        real(8), parameter :: a51 = 19372.0d0/6561.0d0
        real(8), parameter :: a52 = -25360.0d0/2187.0d0
        real(8), parameter :: a53 = 64448.0d0/6561.0d0
        real(8), parameter :: a54 = -212.0d0/729.0d0
        real(8), parameter :: a61 = 9017.0d0/3168.0d0
        real(8), parameter :: a62 = -355.0d0/33.0d0
        real(8), parameter :: a63 = 46732.0d0/5247.0d0
        real(8), parameter :: a64 = 49.0d0/176.0d0
        real(8), parameter :: a65 = -5103.0d0/18656.0d0
        real(8), parameter :: a71 = 35.0d0/384.0d0
        real(8), parameter :: a73 = 500.0d0/1113.0d0
        real(8), parameter :: a74 = 125.0d0/192.0d0
        real(8), parameter :: a75 = -2187.0d0/6784.0d0
        real(8), parameter :: a76 = 11.0d0/84.0d0
        
        ! 5th order coefficients
        real(8), parameter :: b1 = 35.0d0/384.0d0
        real(8), parameter :: b3 = 500.0d0/1113.0d0
        real(8), parameter :: b4 = 125.0d0/192.0d0
        real(8), parameter :: b5 = -2187.0d0/6784.0d0
        real(8), parameter :: b6 = 11.0d0/84.0d0
        
        ! Error coefficients (difference between 5th and 4th order)
        real(8), parameter :: e1 = 71.0d0/57600.0d0
        real(8), parameter :: e3 = -71.0d0/16695.0d0
        real(8), parameter :: e4 = 71.0d0/1920.0d0
        real(8), parameter :: e5 = -17253.0d0/339200.0d0
        real(8), parameter :: e6 = 22.0d0/525.0d0
        real(8), parameter :: e7 = -1.0d0/40.0d0
        
        allocate(k1(n_vars), k2(n_vars), k3(n_vars), k4(n_vars), k5(n_vars), &
                 k6(n_vars), k7(n_vars), y5(n_vars))
        
        call f(t, y, k1)
        call f(t + c2*h, y + a21*h*k1, k2)
        call f(t + c3*h, y + a31*h*k1 + a32*h*k2, k3)
        call f(t + c4*h, y + a41*h*k1 + a42*h*k2 + a43*h*k3, k4)
        call f(t + c5*h, y + a51*h*k1 + a52*h*k2 + a53*h*k3 + a54*h*k4, k5)
        call f(t + h, y + a61*h*k1 + a62*h*k2 + a63*h*k3 + a64*h*k4 + a65*h*k5, k6)
        
        y5 = y + h * (b1*k1 + b3*k3 + b4*k4 + b5*k5 + b6*k6)
        
        call f(t + h, y5, k7)
        
        n_evals = 7
        
        ! 5th order solution
        y_new = y5
        
        ! Error estimate
        err = h * (e1*k1 + e3*k3 + e4*k4 + e5*k5 + e6*k6 + e7*k7)
        
        deallocate(k1, k2, k3, k4, k5, k6, k7, y5)
    end subroutine dopri5_step
    
    ! =========================================================================
    ! Utility Functions
    ! =========================================================================
    
    subroutine simple_ode_test()
        !! Test function to verify module works
        !! Solves dy/dt = -y with y(0) = 1, solution is y(t) = exp(-t)
        
        implicit none
        
        real(8) :: t0, t_end, h
        real(8) :: y0(1)
        real(8), allocatable :: t_out(:), y_out(:,:)
        integer :: n_steps, n_vars, i
        
        n_vars = 1
        n_steps = 10
        allocate(t_out(n_steps+1), y_out(n_steps+1, n_vars))
        
        t0 = 0.0d0
        t_end = 1.0d0
        h = (t_end - t0) / dble(n_steps)
        y0(1) = 1.0d0
        
        call forward_euler(exponential_decay, t0, y0, h, n_steps, t_out, y_out, n_vars)
        
        ! Print results
        write(*,*) 'Forward Euler test: dy/dt = -y, y(0) = 1'
        write(*,*) 't      y_num      y_exact    error'
        do i = 1, n_steps+1
            write(*,'(F5.2, 3F12.6)') t_out(i), y_out(i,1), exp(-t_out(i)), &
                                       abs(y_out(i,1) - exp(-t_out(i)))
        end do
        
        deallocate(t_out, y_out)
    end subroutine simple_ode_test
    
    subroutine exponential_decay(t, y, dydt)
        !! Example ODE: dy/dt = -y
        real(8), intent(in) :: t
        real(8), intent(in) :: y(:)
        real(8), intent(out) :: dydt(:)
        
        dydt(1) = -y(1)
    end subroutine exponential_decay
    
    ! =========================================================================
    ! Harmonic Oscillator Test
    ! =========================================================================
    
    subroutine harmonic_oscillator(t, y, dydt)
        !! Harmonic oscillator: d^2x/dt^2 = -x
        !! Converted to first order system:
        !!   y(1) = x (position)
        !!   y(2) = dx/dt (velocity)
        !!   dy(1)/dt = y(2)
        !!   dy(2)/dt = -y(1)
        real(8), intent(in) :: t
        real(8), intent(in) :: y(:)
        real(8), intent(out) :: dydt(:)
        
        dydt(1) = y(2)
        dydt(2) = -y(1)
    end subroutine harmonic_oscillator
    
    subroutine harmonic_oscillator_test()
        !! Test harmonic oscillator with different methods
        
        implicit none
        
        real(8) :: t0, t_end, h
        real(8) :: y0(2)
        real(8), allocatable :: t_out(:), y_out(:,:)
        integer :: n_steps, n_vars, i
        real(8) :: amplitude, omega
        
        n_vars = 2
        n_steps = 100
        allocate(t_out(n_steps+1), y_out(n_steps+1, n_vars))
        
        t0 = 0.0d0
        t_end = 10.0d0
        h = (t_end - t0) / dble(n_steps)
        amplitude = 1.0d0
        omega = 1.0d0
        y0(1) = amplitude  ! Initial position
        y0(2) = 0.0d0      ! Initial velocity
        
        call rk4(harmonic_oscillator, t0, y0, h, n_steps, t_out, y_out, n_vars)
        
        ! Print results
        write(*,*) ''
        write(*,*) 'Harmonic Oscillator Test: d^2x/dt^2 = -x'
        write(*,*) 'Using RK4 method'
        write(*,*) 't      x_num      x_exact    v_num      v_exact'
        do i = 1, n_steps+1, 10  ! Print every 10th point
            write(*,'(F5.2, 4F12.6)') t_out(i), y_out(i,1), &
                amplitude*cos(omega*t_out(i)), y_out(i,2), &
                -amplitude*omega*sin(omega*t_out(i))
        end do
        
        deallocate(t_out, y_out)
    end subroutine harmonic_oscillator_test
    
end module ode_solver_utils