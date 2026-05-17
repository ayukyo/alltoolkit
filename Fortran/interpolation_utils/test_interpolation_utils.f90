! test_interpolation_utils.f90
! Unit tests for interpolation_utils module
!
! Author: AllToolkit
! Date: 2026-05-18

program test_interpolation_utils
    use interpolation_utils
    implicit none
    
    integer :: tests_passed, tests_failed
    real(8), parameter :: tolerance = 1.0d-10
    
    tests_passed = 0
    tests_failed = 0
    
    print *, "========================================"
    print *, "Interpolation Utils Test Suite"
    print *, "========================================"
    print *, ""
    
    ! Run all tests
    call test_linear_interpolation()
    call test_linear_array_interpolation()
    call test_lagrange_interpolation()
    call test_newton_interpolation()
    call test_cubic_spline()
    call test_bilinear_interpolation()
    
    print *, ""
    print *, "========================================"
    print *, "Test Summary"
    print *, "========================================"
    print '(A, I0)', "Tests passed: ", tests_passed
    print '(A, I0)', "Tests failed: ", tests_failed
    
    if (tests_failed == 0) then
        print *, ""
        print *, "All tests PASSED!"
    else
        print *, ""
        print *, "Some tests FAILED!"
    end if

contains

    subroutine check_result(test_name, expected, actual, tol)
        character(len=*), intent(in) :: test_name
        real(8), intent(in) :: expected, actual
        real(8), intent(in) :: tol
        real(8) :: diff
        
        diff = abs(expected - actual)
        if (diff <= tol) then
            print '(A, A, A)', "  [PASS] ", test_name, ""
            tests_passed = tests_passed + 1
        else
            print '(A, A, A, ES12.4)', "  [FAIL] ", test_name, " - diff: ", diff
            tests_failed = tests_failed + 1
        end if
    end subroutine check_result
    
    subroutine test_linear_interpolation()
        real(8) :: result
        
        print *, "--- Linear Interpolation Tests ---"
        
        ! Test 1: Simple midpoint
        result = linear_interp(0.0d0, 0.0d0, 2.0d0, 2.0d0, 1.0d0)
        call check_result("Midpoint (0,0)-(2,2) at x=1 should be 1", 1.0d0, result, tolerance)
        
        ! Test 2: Quarter point
        result = linear_interp(0.0d0, 0.0d0, 4.0d0, 4.0d0, 1.0d0)
        call check_result("Quarter point at x=1 should be 1", 1.0d0, result, tolerance)
        
        ! Test 3: Non-zero baseline
        result = linear_interp(1.0d0, 2.0d0, 3.0d0, 6.0d0, 2.0d0)
        call check_result("Midpoint (1,2)-(3,6) at x=2 should be 4", 4.0d0, result, tolerance)
        
        ! Test 4: Extrapolation beyond
        result = linear_interp(0.0d0, 0.0d0, 1.0d0, 1.0d0, 2.0d0)
        call check_result("Extrapolation at x=2 should be 2", 2.0d0, result, tolerance)
        
        ! Test 5: Negative slope
        result = linear_interp(0.0d0, 10.0d0, 5.0d0, 0.0d0, 2.0d0)
        call check_result("Negative slope at x=2 should be 6", 6.0d0, result, tolerance)
        
        print *, ""
    end subroutine test_linear_interpolation
    
    subroutine test_linear_array_interpolation()
        real(8) :: x_data(5), y_data(5), x_vals(3), y_result(3)
        
        print *, "--- Linear Array Interpolation Tests ---"
        
        ! Setup data: y = x^2
        x_data = [1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0]
        y_data = [1.0d0, 4.0d0, 9.0d0, 16.0d0, 25.0d0]
        x_vals = [1.5d0, 2.5d0, 4.5d0]
        
        y_result = linear_interp_array(x_data, y_data, x_vals)
        
        call check_result("At x=1.5 should be 2.5", 2.5d0, y_result(1), tolerance)
        call check_result("At x=2.5 should be 6.5", 6.5d0, y_result(2), tolerance)
        call check_result("At x=4.5 should be 20.5", 20.5d0, y_result(3), tolerance)
        
        print *, ""
    end subroutine test_linear_array_interpolation
    
    subroutine test_lagrange_interpolation()
        real(8) :: x_data(4), y_data(4)
        real(8) :: result
        
        print *, "--- Lagrange Interpolation Tests ---"
        
        ! Test with y = x^2
        x_data = [0.0d0, 1.0d0, 2.0d0, 3.0d0]
        y_data = [0.0d0, 1.0d0, 4.0d0, 9.0d0]
        
        ! At x=1.5, exact should be 2.25
        result = lagrange_interp(x_data, y_data, 1.5d0)
        call check_result("y=x^2 at x=1.5 should be 2.25", 2.25d0, result, tolerance)
        
        ! At x=2.5, exact should be 6.25
        result = lagrange_interp(x_data, y_data, 2.5d0)
        call check_result("y=x^2 at x=2.5 should be 6.25", 6.25d0, result, tolerance)
        
        ! At known point x=2
        result = lagrange_interp(x_data, y_data, 2.0d0)
        call check_result("At known point x=2 should be 4", 4.0d0, result, tolerance)
        
        print *, ""
    end subroutine test_lagrange_interpolation
    
    subroutine test_newton_interpolation()
        real(8) :: x_data(4), y_data(4)
        real(8) :: result
        
        print *, "--- Newton Interpolation Tests ---"
        
        ! Test with y = x^3
        x_data = [0.0d0, 1.0d0, 2.0d0, 3.0d0]
        y_data = [0.0d0, 1.0d0, 8.0d0, 27.0d0]
        
        ! At x=1.5
        result = newton_interp(x_data, y_data, 1.5d0)
        call check_result("y=x^3 at x=1.5 should be 3.375", 3.375d0, result, tolerance)
        
        ! At x=2.5
        result = newton_interp(x_data, y_data, 2.5d0)
        call check_result("y=x^3 at x=2.5 should be 15.625", 15.625d0, result, tolerance)
        
        ! At known point
        result = newton_interp(x_data, y_data, 2.0d0)
        call check_result("At known point x=2 should be 8", 8.0d0, result, tolerance)
        
        print *, ""
    end subroutine test_newton_interpolation
    
    subroutine test_cubic_spline()
        real(8) :: x_data(5), y_data(5)
        type(cubic_spline) :: spline
        real(8) :: result
        integer :: i
        
        print *, "--- Cubic Spline Tests ---"
        
        ! Test with smooth function
        x_data = [0.0d0, 1.0d0, 2.0d0, 3.0d0, 4.0d0]
        y_data = [0.0d0, 1.0d0, 4.0d0, 9.0d0, 16.0d0]  ! y = x^2
        
        call spline%init(x_data, y_data)
        
        ! Check known points
        do i = 1, 5
            result = spline%interp(x_data(i))
            call check_result("Spline at known point", y_data(i), result, tolerance)
        end do
        
        ! Check interpolation at midpoints
        result = spline%interp(0.5d0)
        call check_result("Spline at x=0.5 near 0.25", 0.25d0, result, 0.5d0)  ! Slightly relaxed
        
        result = spline%interp(1.5d0)
        call check_result("Spline at x=1.5 near 2.25", 2.25d0, result, 0.5d0)
        
        call spline%free()
        
        print *, ""
    end subroutine test_cubic_spline
    
    subroutine test_bilinear_interpolation()
        real(8) :: result
        
        print *, "--- Bilinear Interpolation Tests ---"
        
        ! Test case: unit square with values at corners
        ! z(0,0)=0, z(1,0)=1, z(0,1)=1, z(1,1)=2
        ! Center should be 1
        
        result = bilinear_interp(0.0d0, 1.0d0, 0.0d0, 1.0d0, &
                                  0.0d0, 1.0d0, 1.0d0, 2.0d0, 0.5d0, 0.5d0)
        call check_result("Center of unit square should be 1", 1.0d0, result, tolerance)
        
        ! At (0.25, 0.25)
        result = bilinear_interp(0.0d0, 1.0d0, 0.0d0, 1.0d0, &
                                  0.0d0, 1.0d0, 1.0d0, 2.0d0, 0.25d0, 0.25d0)
        call check_result("At (0.25, 0.25) should be 0.5", 0.5d0, result, tolerance)
        
        ! At corner (0,0)
        result = bilinear_interp(0.0d0, 1.0d0, 0.0d0, 1.0d0, &
                                  0.0d0, 1.0d0, 1.0d0, 2.0d0, 0.0d0, 0.0d0)
        call check_result("At corner (0,0) should be 0", 0.0d0, result, tolerance)
        
        ! At corner (1,1)
        result = bilinear_interp(0.0d0, 1.0d0, 0.0d0, 1.0d0, &
                                  0.0d0, 1.0d0, 1.0d0, 2.0d0, 1.0d0, 1.0d0)
        call check_result("At corner (1,1) should be 2", 2.0d0, result, tolerance)
        
        print *, ""
    end subroutine test_bilinear_interpolation

end program test_interpolation_utils