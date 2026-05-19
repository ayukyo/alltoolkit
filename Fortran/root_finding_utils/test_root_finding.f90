!! Test program for root_finding_utils module
!! Tests all root-finding algorithms with various test functions

program test_root_finding
    use root_finding_utils
    implicit none
    
    integer :: total_tests, passed_tests
    
    total_tests = 0
    passed_tests = 0
    
    print *, "========================================"
    print *, "  Root Finding Utilities Test Suite"
    print *, "========================================"
    print *, ""
    
    ! Test 1: Polynomial - x^2 - 2 = 0 (root: sqrt(2))
    call test_polynomial_sqrt2()
    
    ! Test 2: Polynomial - x^3 - x - 2 = 0
    call test_polynomial_cubic()
    
    ! Test 3: Trigonometric - cos(x) - x = 0
    call test_trigonometric()
    
    ! Test 4: Exponential - e^x - 3 = 0
    call test_exponential()
    
    ! Test 5: Fixed-point iteration
    call test_fixed_point()
    
    ! Test 6: Multiple roots
    call test_multiple_roots()
    
    ! Test 7: Numerical derivative Newton
    call test_newton_numerical()
    
    ! Test 8: Edge cases
    call test_edge_cases()
    
    print *, ""
    print *, "========================================"
    print '(A,I0,A,I0)', "  Results: ", passed_tests, "/", total_tests, " tests passed"
    print *, "========================================"
    
    if (passed_tests == total_tests) then
        print *, "  ALL TESTS PASSED!"
    else
        print *, "  SOME TESTS FAILED!"
    end if

contains

    ! Test function: f(x) = x^2 - 2 (root at sqrt(2) ≈ 1.41421356)
    function f_sqrt2(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = x * x - 2.0d0
    end function f_sqrt2
    
    ! Derivative: f'(x) = 2x
    function df_sqrt2(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = 2.0d0 * x
    end function df_sqrt2
    
    subroutine test_polynomial_sqrt2()
        type(root_result) :: res
        real(8) :: expected, error
        
        expected = sqrt(2.0d0)
        
        print *, "Test 1: f(x) = x^2 - 2 = 0  (root: sqrt(2) ≈ 1.414214)"
        print *, "-------------------------------------------"
        
        ! Bisection
        res = bisection(f_sqrt2, 1.0d0, 2.0d0)
        error = abs(res%root - expected)
        call check_result("Bisection", res%converged, error < 1.0d-8, res%root, expected)
        
        ! Newton-Raphson
        res = newton_raphson(f_sqrt2, df_sqrt2, 1.5d0)
        error = abs(res%root - expected)
        call check_result("Newton-Raphson", res%converged, error < 1.0d-8, res%root, expected)
        
        ! Secant
        res = secant(f_sqrt2, 1.0d0, 2.0d0)
        error = abs(res%root - expected)
        call check_result("Secant", res%converged, error < 1.0d-8, res%root, expected)
        
        ! False Position
        res = false_position(f_sqrt2, 1.0d0, 2.0d0)
        error = abs(res%root - expected)
        call check_result("False Position", res%converged, error < 1.0d-8, res%root, expected)
        
        ! Brent
        res = brent(f_sqrt2, 1.0d0, 2.0d0)
        error = abs(res%root - expected)
        call check_result("Brent", res%converged, error < 1.0d-8, res%root, expected)
        
        ! Ridder
        res = ridder(f_sqrt2, 1.0d0, 2.0d0)
        error = abs(res%root - expected)
        call check_result("Ridder", res%converged, error < 1.0d-8, res%root, expected)
        
        print *, ""
    end subroutine test_polynomial_sqrt2
    
    ! Test function: f(x) = x^3 - x - 2
    function f_cubic(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = x**3 - x - 2.0d0
    end function f_cubic
    
    ! Derivative: f'(x) = 3x^2 - 1
    function df_cubic(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = 3.0d0 * x * x - 1.0d0
    end function df_cubic
    
    subroutine test_polynomial_cubic()
        type(root_result) :: res
        real(8) :: expected, error
        
        ! Root is approximately 1.5213797...
        expected = 1.521379706804567d0
        
        print *, "Test 2: f(x) = x^3 - x - 2 = 0  (root: ≈ 1.521380)"
        print *, "-------------------------------------------"
        
        ! Bisection
        res = bisection(f_cubic, 1.0d0, 2.0d0)
        error = abs(res%root - expected)
        call check_result("Bisection", res%converged, error < 1.0d-6, res%root, expected)
        
        ! Newton-Raphson
        res = newton_raphson(f_cubic, df_cubic, 1.5d0)
        error = abs(res%root - expected)
        call check_result("Newton-Raphson", res%converged, error < 1.0d-8, res%root, expected)
        
        ! Secant
        res = secant(f_cubic, 1.0d0, 2.0d0)
        error = abs(res%root - expected)
        call check_result("Secant", res%converged, error < 1.0d-8, res%root, expected)
        
        ! Brent
        res = brent(f_cubic, 1.0d0, 2.0d0)
        error = abs(res%root - expected)
        call check_result("Brent", res%converged, error < 1.0d-8, res%root, expected)
        
        print *, ""
    end subroutine test_polynomial_cubic
    
    ! Test function: f(x) = cos(x) - x (root: Dottie number ≈ 0.739085)
    function f_trig(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = cos(x) - x
    end function f_trig
    
    ! Derivative: f'(x) = -sin(x) - 1
    function df_trig(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = -sin(x) - 1.0d0
    end function df_trig
    
    subroutine test_trigonometric()
        type(root_result) :: res
        real(8) :: expected, error
        
        ! Dottie number
        expected = 0.739085133215161d0
        
        print *, "Test 3: f(x) = cos(x) - x = 0  (Dottie number ≈ 0.739085)"
        print *, "-------------------------------------------"
        
        ! Bisection
        res = bisection(f_trig, 0.0d0, 1.0d0)
        error = abs(res%root - expected)
        call check_result("Bisection", res%converged, error < 1.0d-8, res%root, expected)
        
        ! Newton-Raphson
        res = newton_raphson(f_trig, df_trig, 0.5d0)
        error = abs(res%root - expected)
        call check_result("Newton-Raphson", res%converged, error < 1.0d-8, res%root, expected)
        
        ! Secant
        res = secant(f_trig, 0.5d0, 0.8d0)
        error = abs(res%root - expected)
        call check_result("Secant", res%converged, error < 1.0d-8, res%root, expected)
        
        ! Brent
        res = brent(f_trig, 0.0d0, 1.0d0)
        error = abs(res%root - expected)
        call check_result("Brent", res%converged, error < 1.0d-8, res%root, expected)
        
        print *, ""
    end subroutine test_trigonometric
    
    ! Test function: f(x) = e^x - 3 (root: ln(3) ≈ 1.098612)
    function f_exp(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = exp(x) - 3.0d0
    end function f_exp
    
    ! Derivative: f'(x) = e^x
    function df_exp(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = exp(x)
    end function df_exp
    
    subroutine test_exponential()
        type(root_result) :: res
        real(8) :: expected, error
        
        expected = log(3.0d0)
        
        print *, "Test 4: f(x) = e^x - 3 = 0  (root: ln(3) ≈ 1.098612)"
        print *, "-------------------------------------------"
        
        ! Bisection
        res = bisection(f_exp, 0.0d0, 2.0d0)
        error = abs(res%root - expected)
        call check_result("Bisection", res%converged, error < 1.0d-8, res%root, expected)
        
        ! Newton-Raphson
        res = newton_raphson(f_exp, df_exp, 1.0d0)
        error = abs(res%root - expected)
        call check_result("Newton-Raphson", res%converged, error < 1.0d-8, res%root, expected)
        
        ! Brent
        res = brent(f_exp, 0.0d0, 2.0d0)
        error = abs(res%root - expected)
        call check_result("Brent", res%converged, error < 1.0d-8, res%root, expected)
        
        print *, ""
    end subroutine test_exponential
    
    ! Fixed-point function: g(x) = cos(x) (for solving x = cos(x))
    function g_fixed(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = cos(x)
    end function g_fixed
    
    subroutine test_fixed_point()
        type(root_result) :: res
        real(8) :: expected, error
        
        ! Same as Dottie number
        expected = 0.739085133215161d0
        
        print *, "Test 5: Fixed-point x = cos(x)  (Dottie number ≈ 0.739085)"
        print *, "-------------------------------------------"
        
        ! Fixed-point iteration
        res = fixed_point(g_fixed, 0.5d0)
        error = abs(res%root - expected)
        call check_result("Fixed-Point", res%converged, error < 1.0d-6, res%root, expected)
        
        print *, ""
    end subroutine test_fixed_point
    
    ! Test function with multiple roots: f(x) = x^2 - 1 = 0 (roots: ±1)
    function f_multi(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = x * x - 1.0d0
    end function f_multi
    
    ! Test function with multiple roots: f(x) = sin(x) = 0 (roots at n*pi)
    function f_sine(x) result(y)
        real(8), intent(in) :: x
        real(8) :: y
        y = sin(x)
    end function f_sine
    
    subroutine test_multiple_roots()
        real(8), allocatable :: roots(:)
        integer :: i
        
        print *, "Test 6: Multiple roots"
        print *, "-------------------------------------------"
        
        ! Find roots of x^2 - 1 in [-2, 2]
        roots = find_multiple_roots(f_multi, -2.0d0, 2.0d0, 20)
        
        print '(A,I0,A)', "  Found ", size(roots), " root(s) for x^2 - 1 = 0 in [-2, 2]:"
        do i = 1, size(roots)
            print '(A,F12.8)', "    Root: ", roots(i)
        end do
        
        total_tests = total_tests + 1
        if (size(roots) == 2) then
            passed_tests = passed_tests + 1
            print *, "  [PASS] Correct number of roots found"
        else
            print *, "  [FAIL] Expected 2 roots"
        end if
        
        ! Find roots of sin(x) in [0, 10]
        roots = find_multiple_roots(f_sine, 0.0d0, 10.0d0, 100)
        
        print '(A,I0,A)', "  Found ", size(roots), " root(s) for sin(x) = 0 in [0, 10]:"
        do i = 1, min(size(roots), 5)  ! Show first 5
            print '(A,F12.8)', "    Root: ", roots(i)
        end do
        if (size(roots) > 5) print '(A,I0,A)', "    ... and ", size(roots) - 5, " more"
        
        total_tests = total_tests + 1
        if (size(roots) >= 3) then  ! Should find roots at 0, pi, 2*pi, 3*pi
            passed_tests = passed_tests + 1
            print *, "  [PASS] Found multiple roots for sin(x)"
        else
            print *, "  [FAIL] Expected at least 3 roots"
        end if
        
        print *, ""
    end subroutine test_multiple_roots
    
    subroutine test_newton_numerical()
        type(root_result) :: res
        real(8) :: expected, error
        
        expected = sqrt(2.0d0)
        
        print *, "Test 7: Newton-Raphson with numerical derivative"
        print *, "-------------------------------------------"
        
        res = newton_raphson_numerical(f_sqrt2, 1.5d0)
        error = abs(res%root - expected)
        call check_result("Newton (numerical)", res%converged, error < 1.0d-6, res%root, expected)
        
        print *, ""
    end subroutine test_newton_numerical
    
    subroutine test_edge_cases()
        type(root_result) :: res
        
        print *, "Test 8: Edge cases"
        print *, "-------------------------------------------"
        
        ! Root at endpoint
        res = bisection(f_sqrt2, sqrt(2.0d0), 2.0d0)
        total_tests = total_tests + 1
        if (res%converged .and. abs(res%root - sqrt(2.0d0)) < 1.0d-8) then
            passed_tests = passed_tests + 1
            print *, "  [PASS] Root at endpoint detected"
        else
            print *, "  [FAIL] Root at endpoint not handled correctly"
        end if
        
        ! Invalid interval (same signs)
        res = bisection(f_sqrt2, 2.0d0, 3.0d0)  ! Both f(2)=2 and f(3)=7 are positive
        total_tests = total_tests + 1
        if (.not. res%converged) then
            passed_tests = passed_tests + 1
            print *, "  [PASS] Invalid interval detected"
        else
            print *, "  [FAIL] Invalid interval not detected"
        end if
        
        print *, ""
    end subroutine test_edge_cases
    
    subroutine check_result(method_name, converged, accurate, computed, expected)
        character(len=*), intent(in) :: method_name
        logical, intent(in) :: converged, accurate
        real(8), intent(in) :: computed, expected
        
        total_tests = total_tests + 1
        
        print '(A,A)', "  ", method_name
        
        if (converged) then
            print '(A)', "    Status: Converged"
        else
            print '(A)', "    Status: Did not converge"
        end if
        
        print '(A,F16.12)', "    Computed: ", computed
        print '(A,F16.12)', "    Expected: ", expected
        print '(A,ES10.2)', "    Error:    ", abs(computed - expected)
        
        if (converged .and. accurate) then
            passed_tests = passed_tests + 1
            print '(A)', "    [PASS]"
        else
            print '(A)', "    [FAIL]"
        end if
        
        print *, ""
    end subroutine check_result

end program test_root_finding