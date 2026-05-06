!! Example: Harmonic Oscillator
!!
!! Solves the harmonic oscillator equation: d²x/dt² = -ω²x
!! Converted to system of first-order ODEs:
!!   y1 = x (position)
!!   y2 = dx/dt (velocity)
!!
!! Demonstrates:
!! - System of ODEs (2 variables)
!! - RK4 for oscillatory problems
!! - Energy conservation check

program example_harmonic
    use ode_solver_utils
    implicit none
    
    real(8) :: t0, h, omega, amplitude
    real(8) :: y0(2)
    real(8), allocatable :: t_out(:), y_out(:,:)
    integer :: n_steps, n_vars, i
    real(8) :: exact_pos, exact_vel, energy
    
    write(*,*) '=========================================='
    write(*,*) '  Example: Harmonic Oscillator'
    write(*,*) '=========================================='
    write(*,*) ''
    write(*,*) 'Problem: d²x/dt² = -ω²x'
    write(*,*) 'Converted to system:'
    write(*,*) '  dy1/dt = y2 (velocity)'
    write(*,*) '  dy2/dt = -ω²y1 (acceleration)'
    write(*,*) ''
    
    n_vars = 2
    n_steps = 200
    allocate(t_out(n_steps+1), y_out(n_steps+1, n_vars))
    
    ! Parameters
    omega = 2.0d0      ! Angular frequency
    amplitude = 1.0d0  ! Initial amplitude
    
    ! Initial conditions
    t0 = 0.0d0
    h = 0.01d0
    y0(1) = amplitude  ! x(0) = A
    y0(2) = 0.0d0      ! v(0) = 0 (starting at rest)
    
    write(*,'(A, F6.3)') 'Angular frequency: ω = ', omega
    write(*,'(A, F6.3)') 'Initial position: x(0) = ', amplitude
    write(*,'(A, F6.3)') 'Initial velocity: v(0) = 0'
    write(*,*) ''
    
    ! Solve using RK4
    call rk4(my_harmonic, t0, y0, h, n_steps, t_out, y_out, n_vars)
    
    ! Print header
    write(*,*) '  t      Position    Exact Pos   Velocity    Exact Vel'
    write(*,*) '---------------------------------------------------------'
    
    ! Print results (every 20th point)
    do i = 1, n_steps+1, 20
        exact_pos = amplitude * cos(omega * t_out(i))
        exact_vel = -amplitude * omega * sin(omega * t_out(i))
        write(*,'(F8.4, 4F12.6)') t_out(i), y_out(i,1), exact_pos, &
                                  y_out(i,2), exact_vel
    end do
    
    write(*,*) ''
    
    ! Check energy conservation
    ! Energy = (1/2) * m * v² + (1/2) * m * ω² * x²
    ! For unit mass: E = v²/2 + ω²x²/2
    energy = 0.5d0 * y_out(n_steps+1,2)**2 + 0.5d0 * omega**2 * y_out(n_steps+1,1)**2
    write(*,'(A, F12.6)') 'Initial energy: ', 0.5d0 * omega**2 * amplitude**2
    write(*,'(A, F12.6)') 'Final energy: ', energy
    write(*,'(A, F12.6)') 'Energy drift: ', &
        abs(energy - 0.5d0 * omega**2 * amplitude**2)
    write(*,*) ''
    write(*,*) 'RK4 maintains excellent energy conservation!'
    
    deallocate(t_out, y_out)
    
contains
    
    subroutine my_harmonic(t, y, dydt)
        !! System of ODEs for harmonic oscillator
        !! dy1/dt = y2
        !! dy2/dt = -ω²y1
        real(8), intent(in) :: t
        real(8), intent(in) :: y(:)
        real(8), intent(out) :: dydt(:)
        
        dydt(1) = y(2)                    ! dx/dt = v
        dydt(2) = -omega**2 * y(1)        ! dv/dt = -ω²x
    end subroutine my_harmonic
    
end program example_harmonic