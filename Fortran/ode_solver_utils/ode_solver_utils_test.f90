!! AllToolkit - ODE Solver Utilities Test Suite
!! Comprehensive tests for all ODE solver methods
!!
!! Author: AllToolkit Contributors
!! License: MIT

program ode_solver_utils_test
    use ode_solver_utils
    implicit none
    
    logical :: all_tests_passed
    integer :: test_count, pass_count
    
    all_tests_passed = .true.
    test_count = 0
    pass_count = 0
    
    write(*,*) '=========================================='
    write(*,*) '  ODE Solver Utilities - Test Suite'
    write(*,*) '=========================================='
    write(*,*) ''
    
    ! Run all tests
    call test_forward_euler(pass_count, test_count, all_tests_passed)
    call test_backward_euler(pass_count, test_count, all_tests_passed)
    call test_heun_method(pass_count, test_count, all_tests_passed)
    call test_midpoint_method(pass_count, test_count, all_tests_passed)
    call test_rk4(pass_count, test_count, all_tests_passed)
    call test_rkf45(pass_count, test_count, all_tests_passed)
    call test_stiff_ode(pass_count, test_count, all_tests_passed)
    call test_lotka_volterra(pass_count, test_count, all_tests_passed)
    call test_pendulum(pass_count, test_count, all_tests_passed)
    
    ! Summary
    write(*,*) ''
    write(*,*) '=========================================='
    write(*,'(A, I0, A, I0, A)') ' Tests: ', pass_count, ' passed / ', test_count, ' total'
    
    if (all_tests_passed) then
        write(*,*) ' Status: ALL TESTS PASSED'
        write(*,*) '=========================================='
    else
        write(*,*) ' Status: SOME TESTS FAILED'
        write(*,*) '=========================================='
        stop 1
    end if
    
contains
    
    ! =========================================================================
    ! Test Routines
    ! =========================================================================
    
    subroutine test_forward_euler(pass_count, test_count, all_passed)
        integer, intent(inout) :: pass_count, test_count
        logical, intent(inout) :: all_passed
        
        real(8) :: t0, h, tolerance
        real(8) :: y0(1)
        real(8), allocatable :: t_out(:), y_out(:,:)
        integer :: n_steps, n_vars, i
        real(8) :: max_error
        logical :: passed
        
        write(*,*) 'Test 1: Forward Euler - Exponential Decay'
        write(*,*) '  dy/dt = -y, y(0) = 1'
        write(*,*) '  Exact solution: y(t) = exp(-t)'
        
        n_vars = 1
        n_steps = 100
        allocate(t_out(n_steps+1), y_out(n_steps+1, n_vars))
        
        t0 = 0.0d0
        h = 0.01d0
        y0(1) = 1.0d0
        tolerance = 0.05d0  ! Forward Euler has O(h) error
        
        call forward_euler(test_exp_decay, t0, y0, h, n_steps, t_out, y_out, n_vars)
        
        max_error = 0.0d0
        do i = 1, n_steps+1
            max_error = max(max_error, abs(y_out(i,1) - exp(-t_out(i))))
        end do
        
        passed = (max_error < tolerance)
        test_count = test_count + 1
        if (passed) then
            pass_count = pass_count + 1
            write(*,'(A, F10.6)') '  PASS - Max error: ', max_error
        else
            write(*,'(A, F10.6)') '  FAIL - Max error: ', max_error
            all_passed = .false.
        end if
        write(*,*) ''
        
        deallocate(t_out, y_out)
    end subroutine test_forward_euler
    
    subroutine test_backward_euler(pass_count, test_count, all_passed)
        integer, intent(inout) :: pass_count, test_count
        logical, intent(inout) :: all_passed
        
        real(8) :: t0, h, tolerance
        real(8) :: y0(1)
        real(8), allocatable :: t_out(:), y_out(:,:)
        integer :: n_steps, n_vars, i
        real(8) :: max_error
        logical :: passed
        
        write(*,*) 'Test 2: Backward Euler - Exponential Decay'
        write(*,*) '  dy/dt = -y, y(0) = 1'
        write(*,*) '  Exact solution: y(t) = exp(-t)'
        
        n_vars = 1
        n_steps = 50
        allocate(t_out(n_steps+1), y_out(n_steps+1, n_vars))
        
        t0 = 0.0d0
        h = 0.02d0
        y0(1) = 1.0d0
        tolerance = 0.05d0
        
        call backward_euler(test_exp_decay, t0, y0, h, n_steps, t_out, y_out, n_vars)
        
        max_error = 0.0d0
        do i = 1, n_steps+1
            max_error = max(max_error, abs(y_out(i,1) - exp(-t_out(i))))
        end do
        
        passed = (max_error < tolerance)
        test_count = test_count + 1
        if (passed) then
            pass_count = pass_count + 1
            write(*,'(A, F10.6)') '  PASS - Max error: ', max_error
        else
            write(*,'(A, F10.6)') '  FAIL - Max error: ', max_error
            all_passed = .false.
        end if
        write(*,*) ''
        
        deallocate(t_out, y_out)
    end subroutine test_backward_euler
    
    subroutine test_heun_method(pass_count, test_count, all_passed)
        integer, intent(inout) :: pass_count, test_count
        logical, intent(inout) :: all_passed
        
        real(8) :: t0, h, tolerance
        real(8) :: y0(1)
        real(8), allocatable :: t_out(:), y_out(:,:)
        integer :: n_steps, n_vars, i
        real(8) :: max_error
        logical :: passed
        
        write(*,*) 'Test 3: Heun Method - Exponential Decay'
        write(*,*) '  dy/dt = -y, y(0) = 1'
        write(*,*) '  Expected: O(h^2) accuracy'
        
        n_vars = 1
        n_steps = 50
        allocate(t_out(n_steps+1), y_out(n_steps+1, n_vars))
        
        t0 = 0.0d0
        h = 0.02d0
        y0(1) = 1.0d0
        tolerance = 0.01d0  ! Heun is 2nd order
        
        call heun_method(test_exp_decay, t0, y0, h, n_steps, t_out, y_out, n_vars)
        
        max_error = 0.0d0
        do i = 1, n_steps+1
            max_error = max(max_error, abs(y_out(i,1) - exp(-t_out(i))))
        end do
        
        passed = (max_error < tolerance)
        test_count = test_count + 1
        if (passed) then
            pass_count = pass_count + 1
            write(*,'(A, F10.6)') '  PASS - Max error: ', max_error
        else
            write(*,'(A, F10.6)') '  FAIL - Max error: ', max_error
            all_passed = .false.
        end if
        write(*,*) ''
        
        deallocate(t_out, y_out)
    end subroutine test_heun_method
    
    subroutine test_midpoint_method(pass_count, test_count, all_passed)
        integer, intent(inout) :: pass_count, test_count
        logical, intent(inout) :: all_passed
        
        real(8) :: t0, h, tolerance
        real(8) :: y0(1)
        real(8), allocatable :: t_out(:), y_out(:,:)
        integer :: n_steps, n_vars, i
        real(8) :: max_error
        logical :: passed
        
        write(*,*) 'Test 4: Midpoint Method - Exponential Decay'
        write(*,*) '  dy/dt = -y, y(0) = 1'
        write(*,*) '  Expected: O(h^2) accuracy'
        
        n_vars = 1
        n_steps = 50
        allocate(t_out(n_steps+1), y_out(n_steps+1, n_vars))
        
        t0 = 0.0d0
        h = 0.02d0
        y0(1) = 1.0d0
        tolerance = 0.01d0
        
        call midpoint_method(test_exp_decay, t0, y0, h, n_steps, t_out, y_out, n_vars)
        
        max_error = 0.0d0
        do i = 1, n_steps+1
            max_error = max(max_error, abs(y_out(i,1) - exp(-t_out(i))))
        end do
        
        passed = (max_error < tolerance)
        test_count = test_count + 1
        if (passed) then
            pass_count = pass_count + 1
            write(*,'(A, F10.6)') '  PASS - Max error: ', max_error
        else
            write(*,'(A, F10.6)') '  FAIL - Max error: ', max_error
            all_passed = .false.
        end if
        write(*,*) ''
        
        deallocate(t_out, y_out)
    end subroutine test_midpoint_method
    
    subroutine test_rk4(pass_count, test_count, all_passed)
        integer, intent(inout) :: pass_count, test_count
        logical, intent(inout) :: all_passed
        
        real(8) :: t0, h, tolerance
        real(8) :: y0(1)
        real(8), allocatable :: t_out(:), y_out(:,:)
        integer :: n_steps, n_vars, i
        real(8) :: max_error
        logical :: passed
        
        write(*,*) 'Test 5: RK4 Method - Exponential Decay'
        write(*,*) '  dy/dt = -y, y(0) = 1'
        write(*,*) '  Expected: O(h^4) accuracy'
        
        n_vars = 1
        n_steps = 50
        allocate(t_out(n_steps+1), y_out(n_steps+1, n_vars))
        
        t0 = 0.0d0
        h = 0.02d0
        y0(1) = 1.0d0
        tolerance = 0.001d0  ! RK4 is 4th order, much more accurate
        
        call rk4(test_exp_decay, t0, y0, h, n_steps, t_out, y_out, n_vars)
        
        max_error = 0.0d0
        do i = 1, n_steps+1
            max_error = max(max_error, abs(y_out(i,1) - exp(-t_out(i))))
        end do
        
        passed = (max_error < tolerance)
        test_count = test_count + 1
        if (passed) then
            pass_count = pass_count + 1
            write(*,'(A, F10.6)') '  PASS - Max error: ', max_error
        else
            write(*,'(A, F10.6)') '  FAIL - Max error: ', max_error
            all_passed = .false.
        end if
        write(*,*) ''
        
        deallocate(t_out, y_out)
    end subroutine test_rk4
    
    subroutine test_rkf45(pass_count, test_count, all_passed)
        integer, intent(inout) :: pass_count, test_count
        logical, intent(inout) :: all_passed
        
        real(8) :: t0, t_end, h_init, rtol, atol
        real(8) :: y0(1)
        real(8), allocatable :: t_out(:), y_out(:,:)
        integer :: n_steps, n_vars, max_steps, n_evals, i
        real(8) :: max_error
        logical :: passed
        
        write(*,*) 'Test 6: RKF45 Adaptive Method - Exponential Decay'
        write(*,*) '  dy/dt = -y, y(0) = 1'
        write(*,*) '  Adaptive step size control'
        
        n_vars = 1
        max_steps = 1000
        allocate(t_out(max_steps), y_out(max_steps, n_vars))
        
        t0 = 0.0d0
        t_end = 5.0d0
        h_init = 0.1d0
        rtol = 1.0d-6
        atol = 1.0d-9
        y0(1) = 1.0d0
        
        call rkf45(test_exp_decay, t0, t_end, y0, h_init, rtol, atol, &
                   t_out, y_out, n_steps, n_vars, max_steps, n_evals)
        
        max_error = 0.0d0
        do i = 1, n_steps
            max_error = max(max_error, abs(y_out(i,1) - exp(-t_out(i))))
        end do
        
        passed = (max_error < rtol)
        test_count = test_count + 1
        if (passed) then
            pass_count = pass_count + 1
            write(*,'(A, F10.6)') '  PASS - Max error: ', max_error
            write(*,'(A, I0)') '  Steps taken: ', n_steps
            write(*,'(A, I0)') '  Function evaluations: ', n_evals
        else
            write(*,'(A, F10.6)') '  FAIL - Max error: ', max_error
            all_passed = .false.
        end if
        write(*,*) ''
        
        deallocate(t_out, y_out)
    end subroutine test_rkf45
    
    subroutine test_stiff_ode(pass_count, test_count, all_passed)
        integer, intent(inout) :: pass_count, test_count
        logical, intent(inout) :: all_passed
        
        real(8) :: t0, h
        real(8) :: y0(1)
        real(8), allocatable :: t_out(:), y_out(:,:)
        integer :: n_steps, n_vars
        logical :: passed
        
        write(*,*) 'Test 7: Backward Euler - Stiff ODE'
        write(*,*) '  dy/dt = -1000*y, y(0) = 1'
        write(*,*) '  Testing stability on stiff problem'
        
        n_vars = 1
        n_steps = 50
        allocate(t_out(n_steps+1), y_out(n_steps+1, n_vars))
        
        t0 = 0.0d0
        h = 0.001d0  ! Small step for stiff problem
        y0(1) = 1.0d0
        
        call backward_euler(test_stiff_decay, t0, y0, h, n_steps, t_out, y_out, n_vars)
        
        ! For stiff problems, main goal is stability (no oscillation/instability)
        ! Check that solution remains positive and decreasing (stable)
        passed = .true.
        if (minval(y_out(:,1)) < 0.0d0) then
            passed = .false.  ! Instability detected
        end if
        
        ! Also check that it doesn't grow unbounded
        if (maxval(abs(y_out(:,1))) > 2.0d0) then
            passed = .false.
        end if
        
        test_count = test_count + 1
        if (passed) then
            pass_count = pass_count + 1
            write(*,'(A)') '  PASS - Solution is stable (no oscillations)'
            write(*,'(A, F10.6)') '  Initial value: ', y0(1)
            write(*,'(A, F10.6)') '  Final value: ', y_out(n_steps+1, 1)
        else
            write(*,'(A)') '  FAIL - Instability detected'
            all_passed = .false.
        end if
        write(*,*) ''
        
        deallocate(t_out, y_out)
    end subroutine test_stiff_ode
    
    subroutine test_lotka_volterra(pass_count, test_count, all_passed)
        integer, intent(inout) :: pass_count, test_count
        logical, intent(inout) :: all_passed
        
        real(8) :: t0, h
        real(8) :: y0(2)
        real(8), allocatable :: t_out(:), y_out(:,:)
        integer :: n_steps, n_vars
        logical :: passed
        
        write(*,*) 'Test 8: RK4 - Lotka-Volterra (Predator-Prey)'
        write(*,*) '  dx/dt = alpha*x - beta*x*y'
        write(*,*) '  dy/dt = delta*x*y - gamma*y'
        write(*,*) '  Testing system of ODEs'
        
        n_vars = 2
        n_steps = 1000
        allocate(t_out(n_steps+1), y_out(n_steps+1, n_vars))
        
        t0 = 0.0d0
        h = 0.01d0
        y0(1) = 10.0d0  ! Initial prey
        y0(2) = 5.0d0   ! Initial predators
        
        call rk4(test_lotka_volterra_ode, t0, y0, h, n_steps, t_out, y_out, n_vars)
        
        ! Check populations stay positive (basic sanity check)
        passed = .true.
        if (minval(y_out(:,1)) < 0.0d0 .or. minval(y_out(:,2)) < 0.0d0) then
            passed = .false.
        end if
        
        test_count = test_count + 1
        if (passed) then
            pass_count = pass_count + 1
            write(*,'(A)') '  PASS - Populations remain positive'
            write(*,'(A, F10.4)') '  Final prey: ', y_out(n_steps+1, 1)
            write(*,'(A, F10.4)') '  Final predator: ', y_out(n_steps+1, 2)
        else
            write(*,'(A)') '  FAIL - Negative population detected'
            all_passed = .false.
        end if
        write(*,*) ''
        
        deallocate(t_out, y_out)
    end subroutine test_lotka_volterra
    
    subroutine test_pendulum(pass_count, test_count, all_passed)
        integer, intent(inout) :: pass_count, test_count
        logical, intent(inout) :: all_passed
        
        real(8) :: t0, h, tolerance
        real(8) :: y0(2)
        real(8), allocatable :: t_out(:), y_out(:,:)
        integer :: n_steps, n_vars, i
        real(8) :: total_energy, initial_energy
        logical :: passed
        
        write(*,*) 'Test 9: RK4 - Simple Pendulum'
        write(*,*) '  d^2(theta)/dt^2 = -g/L * sin(theta)'
        write(*,*) '  Testing energy conservation'
        
        n_vars = 2
        n_steps = 1000
        allocate(t_out(n_steps+1), y_out(n_steps+1, n_vars))
        
        t0 = 0.0d0
        h = 0.01d0
        y0(1) = 0.5d0   ! Initial angle (radians)
        y0(2) = 0.0d0   ! Initial angular velocity
        
        call rk4(test_pendulum_ode, t0, y0, h, n_steps, t_out, y_out, n_vars)
        
        ! Check energy conservation (E = 0.5*L^2*omega^2 - g*L*cos(theta))
        ! For simplicity, check that energy is approximately conserved
        initial_energy = 0.5d0 * y0(2)**2 - 9.81d0 * cos(y0(1))
        
        ! Check final energy
        total_energy = 0.5d0 * y_out(n_steps+1, 2)**2 - 9.81d0 * cos(y_out(n_steps+1, 1))
        
        tolerance = 0.01d0  ! Allow 1% energy drift
        passed = (abs(total_energy - initial_energy) < tolerance)
        
        test_count = test_count + 1
        if (passed) then
            pass_count = pass_count + 1
            write(*,'(A)') '  PASS - Energy well conserved'
            write(*,'(A, F10.6)') '  Initial energy: ', initial_energy
            write(*,'(A, F10.6)') '  Final energy: ', total_energy
            write(*,'(A, F10.6)') '  Energy drift: ', abs(total_energy - initial_energy)
        else
            write(*,'(A)') '  FAIL - Energy conservation violated'
            all_passed = .false.
        end if
        write(*,*) ''
        
        deallocate(t_out, y_out)
    end subroutine test_pendulum
    
    ! =========================================================================
    ! ODE Functions for Testing
    ! =========================================================================
    
    subroutine test_exp_decay(t, y, dydt)
        !! dy/dt = -y
        real(8), intent(in) :: t
        real(8), intent(in) :: y(:)
        real(8), intent(out) :: dydt(:)
        
        dydt(1) = -y(1)
    end subroutine test_exp_decay
    
    subroutine test_stiff_decay(t, y, dydt)
        !! dy/dt = -1000*y (stiff problem)
        real(8), intent(in) :: t
        real(8), intent(in) :: y(:)
        real(8), intent(out) :: dydt(:)
        
        dydt(1) = -1000.0d0 * y(1)
    end subroutine test_stiff_decay
    
    subroutine test_lotka_volterra_ode(t, y, dydt)
        !! Lotka-Volterra predator-prey model
        !! dx/dt = alpha*x - beta*x*y  (prey)
        !! dy/dt = delta*x*y - gamma*y  (predator)
        real(8), intent(in) :: t
        real(8), intent(in) :: y(:)
        real(8), intent(out) :: dydt(:)
        
        real(8) :: alpha, beta, delta, gamma
        
        alpha = 1.0d0    ! Prey growth rate
        beta = 0.1d0     ! Predation rate
        delta = 0.075d0  ! Predator growth rate per prey
        gamma = 1.5d0    ! Predator death rate
        
        dydt(1) = alpha * y(1) - beta * y(1) * y(2)
        dydt(2) = delta * y(1) * y(2) - gamma * y(2)
    end subroutine test_lotka_volterra_ode
    
    subroutine test_pendulum_ode(t, y, dydt)
        !! Simple pendulum
        !! y(1) = theta (angle)
        !! y(2) = omega (angular velocity)
        !! d(theta)/dt = omega
        !! d(omega)/dt = -g/L * sin(theta)
        real(8), intent(in) :: t
        real(8), intent(in) :: y(:)
        real(8), intent(out) :: dydt(:)
        
        real(8) :: g, L
        
        g = 9.81d0   ! gravity
        L = 1.0d0    ! pendulum length
        
        dydt(1) = y(2)
        dydt(2) = -(g / L) * sin(y(1))
    end subroutine test_pendulum_ode

end program ode_solver_utils_test