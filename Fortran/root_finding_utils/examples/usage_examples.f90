!! Example program demonstrating root_finding_utils module usage
!! Shows practical applications of various root-finding algorithms

program usage_examples
    use root_finding_utils
    implicit none
    
    print *, "========================================"
    print *, "  Root Finding Utilities - Examples"
    print *, "========================================"
    print *, ""
    
    ! Example 1: Finding square root using root finding
    call example_sqrt()
    
    ! Example 2: Solving transcendental equations
    call example_transcendental()
    
    ! Example 3: Physics application - projectile motion
    call example_physics()
    
    ! Example 4: Engineering application - heat transfer
    call example_heat()
    
    ! Example 5: Economics application - break-even analysis
    call example_economics()
    
    ! Example 6: Finding all roots in an interval
    call example_multiple_roots()
    
    print *, ""
    print *, "All examples completed!"

contains

    ! Example 1 functions
    function sqrt25_func(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = x * x - 25.0d0
    end function sqrt25_func
    
    subroutine example_sqrt()
        type(root_result) :: res
        
        print *, "Example 1: Computing Square Root"
        print *, "---------------------------------------"
        print *, "To find sqrt(N), we solve f(x) = x^2 - N = 0"
        print *, ""
        
        print '(A)', "Finding sqrt(25)..."
        res = brent(sqrt25_func, 0.0d0, 26.0d0)
        print '(A,F12.8)', "Result: ", res%root
        print '(A,F12.8)', "Actual: ", sqrt(25.0d0)
        print '(A,I0)', "Iterations: ", res%iterations
        print *, ""
    end subroutine example_sqrt
    
    ! Example 2 functions
    function trans_func(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = x - 2.0d0 * sin(x) - 1.0d0
    end function trans_func
    
    subroutine example_transcendental()
        type(root_result) :: res
        
        print *, "Example 2: Transcendental Equations"
        print *, "---------------------------------------"
        
        print *, "Solving: x = 2*sin(x) + 1"
        print *, ""
        
        res = brent(trans_func, -5.0d0, 5.0d0)
        print '(A,F12.8)', "Root: ", res%root
        print '(A,F12.8)', "Verification f(root): ", res%residual
        print '(A,I0)', "Iterations: ", res%iterations
        print *, ""
    end subroutine example_transcendental
    
    ! Example 3 functions
    function projectile_func(theta) result(y)
        real(8), intent(in) :: theta
        real(8) :: y
        real(8) :: v0, g, y_target
        v0 = 50.0d0
        g = 9.81d0
        y_target = 20.0d0
        y = sin(2.0d0 * theta) - y_target * g / (v0 * v0)
    end function projectile_func
    
    subroutine example_physics()
        type(root_result) :: res
        real(8) :: theta_deg
        
        print *, "Example 3: Projectile Motion"
        print *, "---------------------------------------"
        print *, "Finding launch angle for projectile"
        print *, ""
        
        print '(A)', "Initial velocity: 50 m/s"
        print '(A)', "Target height: 20 m"
        print *, ""
        
        res = brent(projectile_func, 0.1d0, 1.4d0)
        
        theta_deg = res%root * 180.0d0 / 3.141592653589793d0
        
        print '(A,F8.2,A)', "Launch angle: ", theta_deg, " degrees"
        print '(A,I0)', "Iterations: ", res%iterations
        print *, ""
    end subroutine example_physics
    
    ! Example 4 functions
    function heat_func(L) result(y)
        real(8), intent(in) :: L
        real(8) :: y
        real(8) :: T_surface, T_ambient, h, k, q_target
        T_surface = 100.0d0
        T_ambient = 20.0d0
        h = 10.0d0
        k = 0.5d0
        q_target = 500.0d0
        y = h * (T_surface - T_ambient) * L / (L + k/h) - q_target
    end function heat_func
    
    subroutine example_heat()
        type(root_result) :: res
        
        print *, "Example 4: Heat Transfer Analysis"
        print *, "---------------------------------------"
        print *, "Finding wall thickness for desired heat flux"
        print *, ""
        
        print '(A)', "Surface temp: 100 C"
        print '(A)', "Ambient temp: 20 C"
        print '(A)', "Target heat flux: 500 W/m^2"
        print *, ""
        
        res = brent(heat_func, 0.01d0, 1.0d0)
        
        print '(A,F8.4,A)', "Required wall thickness: ", res%root, " m"
        print '(A,I0)', "Iterations: ", res%iterations
        print *, ""
    end subroutine example_heat
    
    ! Example 5 functions
    function profit_func(q) result(y)
        real(8), intent(in) :: q
        real(8) :: y
        real(8) :: fixed_cost, variable_cost, price
        fixed_cost = 50000.0d0
        variable_cost = 15.0d0
        price = 25.0d0
        y = (price - variable_cost) * q - fixed_cost
    end function profit_func
    
    subroutine example_economics()
        type(root_result) :: res
        
        print *, "Example 5: Break-Even Analysis"
        print *, "---------------------------------------"
        print *, "Finding break-even quantity"
        print *, ""
        
        print '(A)', "Fixed costs: $50000"
        print '(A)', "Variable cost per unit: $15"
        print '(A)', "Selling price per unit: $25"
        print *, ""
        
        res = brent(profit_func, 0.0d0, 10000.0d0)
        
        print '(A,F10.0,A)', "Break-even quantity: ", res%root, " units"
        print '(A,I0)', "Iterations: ", res%iterations
        print *, ""
    end subroutine example_economics
    
    ! Example 6 functions
    function sine_half(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = sin(x) - 0.5d0
    end function sine_half
    
    subroutine example_multiple_roots()
        real(8), allocatable :: roots(:)
        integer :: i
        
        print *, "Example 6: Finding Multiple Roots"
        print *, "---------------------------------------"
        print *, "Finding all roots of sin(x) - 0.5 = 0 in [0, 4*pi]"
        print *, ""
        
        roots = find_multiple_roots(sine_half, 0.0d0, 4.0d0 * 3.14159265d0, 100)
        
        print '(A,I0,A)', "Found ", size(roots), " roots:"
        do i = 1, size(roots)
            print '(A,I2,A,F12.6)', "  Root ", i, ": x = ", roots(i)
        end do
        print *, ""
    end subroutine example_multiple_roots

end program usage_examples