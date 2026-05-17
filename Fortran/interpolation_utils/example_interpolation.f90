! example_interpolation.f90
! Example usage of interpolation_utils module
!
! Compile with:
!   gfortran -o example_interpolation interpolation_utils.f90 example_interpolation.f90
!
! Run:
!   ./example_interpolation
!
! Author: AllToolkit
! Date: 2026-05-18

program example_interpolation
    use interpolation_utils
    implicit none
    
    print *, "========================================"
    print *, "Interpolation Utils Examples"
    print *, "========================================"
    print *, ""
    
    call example_linear_interp()
    call example_lagrange_interp()
    call example_newton_interp()
    call example_cubic_spline()
    call example_bilinear_interp()

contains

    subroutine example_linear_interp()
        real(8) :: result
        real(8) :: x_data(5), y_data(5), x_vals(4), y_results(4)
        integer :: i
        
        print *, "--- Linear Interpolation Example ---"
        print *, ""
        
        ! Single point interpolation
        print *, "Data points: (0, 0), (10, 100)"
        print *, "Target x = 5"
        result = linear_interp(0.0d0, 0.0d0, 10.0d0, 100.0d0, 5.0d0)
        print '(A, F8.2)', "Interpolated y = ", result
        print *, ""
        
        ! Array interpolation
        print *, "Array interpolation (y = x^2):"
        x_data = [0.0d0, 1.0d0, 2.0d0, 3.0d0, 4.0d0]
        y_data = [0.0d0, 1.0d0, 4.0d0, 9.0d0, 16.0d0]
        x_vals = [0.5d0, 1.5d0, 2.5d0, 3.5d0]
        
        y_results = linear_interp_array(x_data, y_data, x_vals)
        
        do i = 1, 4
            print '(A, F4.1, A, F8.4, A, F6.2)', "x=", x_vals(i), &
                " -> y=", y_results(i), " (exact: ", x_vals(i)**2, ")"
        end do
        print *, ""
    end subroutine example_linear_interp
    
    subroutine example_lagrange_interp()
        real(8) :: x_data(4), y_data(4)
        real(8) :: x, y_exact, y_interp
        integer :: i
        
        print *, "--- Lagrange Interpolation Example ---"
        print *, ""
        print *, "Interpolating sin(x) using 4 points:"
        
        ! Sample sin(x) at 4 points
        x_data = [0.0d0, 1.0d0, 2.0d0, 3.0d0]
        do i = 1, 4
            y_data(i) = sin(x_data(i))
        end do
        
        print *, "Data points:"
        do i = 1, 4
            print '(A, F4.1, A, F8.5)', "  (", x_data(i), ", ", y_data(i), ")"
        end do
        print *, ""
        
        ! Interpolate at several points
        print *, "Interpolation results:"
        do i = 1, 5
            x = 0.5d0 * i
            y_exact = sin(x)
            y_interp = lagrange_interp(x_data, y_data, x)
            print '(A, F4.2, A, F8.5, A, F8.5, A, F10.6)', &
                "x=", x, " exact=", y_exact, " interp=", y_interp, &
                " error=", abs(y_exact - y_interp)
        end do
        print *, ""
    end subroutine example_lagrange_interp
    
    subroutine example_newton_interp()
        real(8) :: x_data(5), y_data(5)
        real(8) :: coeffs(5)
        real(8) :: x, y_exact, y_interp
        integer :: i
        
        print *, "--- Newton Interpolation Example ---"
        print *, ""
        print *, "Interpolating exp(x) using 5 points:"
        
        ! Sample exp(x)
        x_data = [0.0d0, 0.5d0, 1.0d0, 1.5d0, 2.0d0]
        do i = 1, 5
            y_data(i) = exp(x_data(i))
        end do
        
        ! Compute divided difference coefficients
        coeffs = newton_coefficients(x_data, y_data)
        
        print *, "Newton divided difference coefficients:"
        do i = 1, 5
            print '(A, I1, A, ES14.6)', "  c", i-1, " = ", coeffs(i)
        end do
        print *, ""
        
        ! Interpolate
        print *, "Interpolation results:"
        do i = 1, 5
            x = 0.25d0 * i
            y_exact = exp(x)
            y_interp = newton_interp(x_data, y_data, x)
            print '(A, F4.2, A, F10.6, A, F10.6, A, ES10.3)', &
                "x=", x, " exact=", y_exact, " interp=", y_interp, &
                " error=", abs(y_exact - y_interp)
        end do
        print *, ""
    end subroutine example_newton_interp
    
    subroutine example_cubic_spline()
        type(cubic_spline) :: spline
        real(8) :: x_data(6), y_data(6)
        real(8) :: x, y_exact, y_interp
        integer :: i
        
        print *, "--- Cubic Spline Interpolation Example ---"
        print *, ""
        print *, "Interpolating y = x^3 - 2x + 1:"
        
        ! Sample the function
        x_data = [-2.0d0, -1.0d0, 0.0d0, 1.0d0, 2.0d0, 3.0d0]
        do i = 1, 6
            y_data(i) = x_data(i)**3 - 2.0d0 * x_data(i) + 1.0d0
        end do
        
        print *, "Data points:"
        do i = 1, 6
            print '(A, F5.1, A, F8.2)', "  (", x_data(i), ", ", y_data(i), ")"
        end do
        print *, ""
        
        ! Initialize spline
        call spline%init(x_data, y_data)
        
        ! Interpolate at midpoints
        print *, "Interpolation at midpoints:"
        do i = 1, 10
            x = -2.0d0 + 0.5d0 * i
            y_exact = x**3 - 2.0d0 * x + 1.0d0
            y_interp = spline%interp(x)
            print '(A, F5.2, A, F10.4, A, F10.4, A, ES10.3)', &
                "x=", x, " exact=", y_exact, " interp=", y_interp, &
                " error=", abs(y_exact - y_interp)
        end do
        
        call spline%free()
        print *, ""
    end subroutine example_cubic_spline
    
    subroutine example_bilinear_interp()
        real(8) :: result
        
        print *, "--- Bilinear Interpolation Example ---"
        print *, ""
        print *, "2D grid interpolation:"
        print *, ""
        print *, "Grid values f(x, y):"
        print *, "          y=0    y=1    y=2"
        print *, "  x=0:    0.0    2.0    4.0"
        print *, "  x=1:    1.0    3.0    5.0"
        print *, "  x=2:    2.0    4.0    6.0"
        print *, ""
        
        ! Interpolate at (0.5, 0.5)
        result = bilinear_interp(0.0d0, 1.0d0, 0.0d0, 1.0d0, &
                                  0.0d0, 2.0d0, 1.0d0, 3.0d0, 0.5d0, 0.5d0)
        print '(A, F8.4)', "f(0.5, 0.5) = ", result
        
        ! Interpolate at (0.5, 1.5)
        result = bilinear_interp(0.0d0, 1.0d0, 1.0d0, 2.0d0, &
                                  2.0d0, 4.0d0, 3.0d0, 5.0d0, 0.5d0, 1.5d0)
        print '(A, F8.4)', "f(0.5, 1.5) = ", result
        
        ! Interpolate at (1.5, 0.5)
        result = bilinear_interp(1.0d0, 2.0d0, 0.0d0, 1.0d0, &
                                  1.0d0, 3.0d0, 2.0d0, 4.0d0, 1.5d0, 0.5d0)
        print '(A, F8.4)', "f(1.5, 0.5) = ", result
        
        print *, ""
    end subroutine example_bilinear_interp

end program example_interpolation