!! Example: Exponential Decay
!! 
!! Solves dy/dt = -y with y(0) = 1
!! Exact solution: y(t) = exp(-t)
!!
!! Demonstrates:
!! - Basic RK4 usage
!! - Single variable ODE
!! - Comparison with exact solution

program example_decay
    use ode_solver_utils
    implicit none
    
    real(8) :: t0, h
    real(8) :: y0(1)
    real(8), allocatable :: t_out(:), y_out(:,:)
    integer :: n_steps, n_vars, i
    real(8) :: error
    
    write(*,*) '=========================================='
    write(*,*) '  Example: Exponential Decay'
    write(*,*) '=========================================='
    write(*,*) ''
    write(*,*) 'Problem: dy/dt = -y, y(0) = 1'
    write(*,*) 'Exact solution: y(t) = exp(-t)'
    write(*,*) 'Method: RK4 (4th order Runge-Kutta)'
    write(*,*) ''
    
    n_vars = 1
    n_steps = 100
    allocate(t_out(n_steps+1), y_out(n_steps+1, n_vars))
    
    ! Initial conditions
    t0 = 0.0d0
    h = 0.01d0
    y0(1) = 1.0d0
    
    ! Solve using RK4
    call rk4(my_decay, t0, y0, h, n_steps, t_out, y_out, n_vars)
    
    ! Print header
    write(*,*) '  t        Numerical    Exact       Error'
    write(*,*) '------------------------------------------'
    
    ! Print results (every 10th point)
    do i = 1, n_steps+1, 10
        error = abs(y_out(i,1) - exp(-t_out(i)))
        write(*,'(F8.4, 3F12.6)') t_out(i), y_out(i,1), exp(-t_out(i)), error
    end do
    
    write(*,*) ''
    write(*,'(A, F10.6)') 'Maximum error: ', &
        maxval(abs(y_out(:,1) - exp(-t_out(:))))
    write(*,*) ''
    write(*,*) 'RK4 achieves very high accuracy for this simple problem!'
    
    deallocate(t_out, y_out)
    
contains
    
    subroutine my_decay(t, y, dydt)
        !! ODE function: dy/dt = -y
        real(8), intent(in) :: t
        real(8), intent(in) :: y(:)
        real(8), intent(out) :: dydt(:)
        
        dydt(1) = -y(1)
    end subroutine my_decay
    
end program example_decay