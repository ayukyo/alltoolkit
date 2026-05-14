program test_polynomial_utils
    use polynomial_utils
    implicit none
    
    integer :: tests_passed, tests_failed
    
    tests_passed = 0
    tests_failed = 0
    
    print *, "========================================"
    print *, "  Polynomial Utils Test Suite"
    print *, "========================================"
    print *
    
    ! Run all tests
    call test_poly_eval()
    call test_poly_derivative()
    call test_poly_integral()
    call test_poly_add()
    call test_poly_multiply()
    call test_poly_degree()
    call test_poly_roots_bisection()
    call test_poly_roots_newton()
    call test_poly_lagrange_interpolate()
    call test_poly_from_roots()
    call test_poly_compose()
    call test_poly_gcd()
    
    ! Summary
    print *
    print *, "========================================"
    print *, "  Test Summary"
    print *, "========================================"
    print '(A,I0)', "  Tests Passed: ", tests_passed
    print '(A,I0)', "  Tests Failed: ", tests_failed
    print *
    
    if (tests_failed == 0) then
        print *, "  All tests passed!"
    else
        print *, "  Some tests failed."
    end if

contains

    subroutine test_poly_eval()
        real(8) :: coeffs(4)
        real(8) :: result
        
        print *, "Test: poly_eval"
        
        ! Test polynomial: 1 + 2x + 3x^2 + 4x^3
        coeffs = [1.0d0, 2.0d0, 3.0d0, 4.0d0]
        
        result = poly_eval(coeffs, 0.0d0)
        call assert_approx(result, 1.0d0, "Evaluate at x=0")
        
        result = poly_eval(coeffs, 1.0d0)
        call assert_approx(result, 10.0d0, "Evaluate at x=1")
        
        result = poly_eval(coeffs, 2.0d0)
        call assert_approx(result, 49.0d0, "Evaluate at x=2")
        
        result = poly_eval(coeffs, -1.0d0)
        call assert_approx(result, -2.0d0, "Evaluate at x=-1")
        
        print *
    end subroutine test_poly_eval
    
    subroutine test_poly_derivative()
        real(8) :: coeffs(4)
        real(8), allocatable :: dcoeffs(:)
        
        print *, "Test: poly_derivative"
        
        ! Test polynomial: 1 + 2x + 3x^2 + 4x^3
        coeffs = [1.0d0, 2.0d0, 3.0d0, 4.0d0]
        dcoeffs = poly_derivative(coeffs)
        
        call assert_approx(dcoeffs(1), 2.0d0, "Derivative constant")
        call assert_approx(dcoeffs(2), 6.0d0, "Derivative linear")
        call assert_approx(dcoeffs(3), 12.0d0, "Derivative quadratic")
        
        print *
    end subroutine test_poly_derivative
    
    subroutine test_poly_integral()
        real(8) :: coeffs(3)
        real(8), allocatable :: icoeffs(:)
        
        print *, "Test: poly_integral"
        
        ! Test polynomial: 1 + 2x + 3x^2
        coeffs = [1.0d0, 2.0d0, 3.0d0]
        icoeffs = poly_integral(coeffs)
        
        call assert_approx(icoeffs(1), 0.0d0, "Integral constant")
        call assert_approx(icoeffs(2), 1.0d0, "Integral linear")
        call assert_approx(icoeffs(3), 1.0d0, "Integral quadratic")
        call assert_approx(icoeffs(4), 1.0d0, "Integral cubic")
        
        print *
    end subroutine test_poly_integral
    
    subroutine test_poly_add()
        real(8) :: p1(3), p2(4)
        real(8), allocatable :: result(:)
        
        print *, "Test: poly_add"
        
        ! p1 = 1 + 2x + 3x^2, p2 = 1 + 0x + 0x^2 + 4x^3
        p1 = [1.0d0, 2.0d0, 3.0d0]
        p2 = [1.0d0, 0.0d0, 0.0d0, 4.0d0]
        
        result = poly_add(p1, p2)
        
        call assert_approx(result(1), 2.0d0, "Add constant")
        call assert_approx(result(2), 2.0d0, "Add linear")
        call assert_approx(result(3), 3.0d0, "Add quadratic")
        call assert_approx(result(4), 4.0d0, "Add cubic")
        
        print *
    end subroutine test_poly_add
    
    subroutine test_poly_multiply()
        real(8) :: p1(2), p2(2)
        real(8), allocatable :: result(:)
        
        print *, "Test: poly_multiply"
        
        ! (1 + x) * (1 + x) = 1 + 2x + x^2
        p1 = [1.0d0, 1.0d0]
        p2 = [1.0d0, 1.0d0]
        
        result = poly_multiply(p1, p2)
        
        call assert_approx(result(1), 1.0d0, "Multiply constant")
        call assert_approx(result(2), 2.0d0, "Multiply linear")
        call assert_approx(result(3), 1.0d0, "Multiply quadratic")
        
        print *
    end subroutine test_poly_multiply
    
    subroutine test_poly_degree()
        real(8) :: coeffs(5), coeffs2(3)
        integer :: deg
        
        print *, "Test: poly_degree"
        
        coeffs = [0.0d0, 0.0d0, 3.0d0, 0.0d0, 5.0d0]
        deg = poly_degree(coeffs)
        call assert_equal(deg, 4, "Degree with trailing zeros")
        
        coeffs2 = [5.0d0, 0.0d0, 0.0d0]
        deg = poly_degree(coeffs2)
        call assert_equal(deg, 0, "Degree of constant")
        
        print *
    end subroutine test_poly_degree
    
    subroutine test_poly_roots_bisection()
        real(8) :: coeffs(3)
        real(8) :: root
        
        print *, "Test: poly_roots_bisection"
        
        ! x^2 - 4 = 0, roots at x = ±2
        coeffs = [-4.0d0, 0.0d0, 1.0d0]
        
        root = poly_roots_bisection(coeffs, 0.0d0, 3.0d0)
        call assert_approx(root, 2.0d0, "Bisection root at 2")
        
        root = poly_roots_bisection(coeffs, -3.0d0, 0.0d0)
        call assert_approx(root, -2.0d0, "Bisection root at -2")
        
        print *
    end subroutine test_poly_roots_bisection
    
    subroutine test_poly_roots_newton()
        real(8) :: coeffs(3)
        real(8) :: root
        
        print *, "Test: poly_roots_newton"
        
        ! x^2 - 4 = 0
        coeffs = [-4.0d0, 0.0d0, 1.0d0]
        
        root = poly_roots_newton(coeffs, 3.0d0)
        call assert_approx(root, 2.0d0, "Newton root at 2")
        
        root = poly_roots_newton(coeffs, -3.0d0)
        call assert_approx(root, -2.0d0, "Newton root at -2")
        
        print *
    end subroutine test_poly_roots_newton
    
    subroutine test_poly_lagrange_interpolate()
        real(8) :: x_points(3), y_points(3)
        real(8), allocatable :: coeffs(:)
        real(8) :: val
        
        print *, "Test: poly_lagrange_interpolate"
        
        ! Points: (0, 1), (1, 2), (2, 5)
        ! Should give: 1 + x^2
        x_points = [0.0d0, 1.0d0, 2.0d0]
        y_points = [1.0d0, 2.0d0, 5.0d0]
        
        coeffs = poly_lagrange_interpolate(x_points, y_points)
        
        val = poly_eval(coeffs, 0.0d0)
        call assert_approx(val, 1.0d0, "Lagrange at x=0")
        
        val = poly_eval(coeffs, 1.0d0)
        call assert_approx(val, 2.0d0, "Lagrange at x=1")
        
        val = poly_eval(coeffs, 2.0d0)
        call assert_approx(val, 5.0d0, "Lagrange at x=2")
        
        print *
    end subroutine test_poly_lagrange_interpolate
    
    subroutine test_poly_from_roots()
        real(8) :: roots(3)
        real(8), allocatable :: coeffs(:)
        real(8) :: val
        
        print *, "Test: poly_from_roots"
        
        ! Roots: -1, 0, 1 -> polynomial: x^3 - x = x(x-1)(x+1)
        roots = [-1.0d0, 0.0d0, 1.0d0]
        
        coeffs = poly_from_roots(roots)
        
        val = poly_eval(coeffs, -1.0d0)
        call assert_approx(val, 0.0d0, "From roots at x=-1")
        
        val = poly_eval(coeffs, 0.0d0)
        call assert_approx(val, 0.0d0, "From roots at x=0")
        
        val = poly_eval(coeffs, 1.0d0)
        call assert_approx(val, 0.0d0, "From roots at x=1")
        
        print *
    end subroutine test_poly_from_roots
    
    subroutine test_poly_compose()
        real(8) :: p(2), q(2)
        real(8), allocatable :: result(:)
        real(8) :: val
        
        print *, "Test: poly_compose"
        
        ! p(x) = 1 + 2x, q(x) = 1 + x
        ! p(q(x)) = 1 + 2(1+x) = 3 + 2x
        p = [1.0d0, 2.0d0]
        q = [1.0d0, 1.0d0]
        
        result = poly_compose(p, q)
        
        val = poly_eval(result, 0.0d0)
        call assert_approx(val, 3.0d0, "Compose at x=0")
        
        val = poly_eval(result, 1.0d0)
        call assert_approx(val, 5.0d0, "Compose at x=1")
        
        print *
    end subroutine test_poly_compose
    
    subroutine test_poly_gcd()
        real(8) :: p(5), q(3)
        real(8), allocatable :: gcd_coeffs(:)
        real(8) :: val
        
        print *, "Test: poly_gcd"
        
        ! p(x) = (x-1)(x-2)(x^2+1) = x^4 - 3x^3 + 3x^2 - 3x + 2
        ! q(x) = (x-1)(x-2) = x^2 - 3x + 2
        ! GCD should be (x-1)(x-2) = x^2 - 3x + 2
        
        p = [2.0d0, -3.0d0, 3.0d0, -3.0d0, 1.0d0]
        q = [2.0d0, -3.0d0, 1.0d0]
        
        gcd_coeffs = poly_gcd(p, q)
        
        val = poly_eval(gcd_coeffs, 1.0d0)
        call assert_approx(val, 0.0d0, "GCD root at x=1")
        
        val = poly_eval(gcd_coeffs, 2.0d0)
        call assert_approx(val, 0.0d0, "GCD root at x=2")
        
        print *
    end subroutine test_poly_gcd
    
    subroutine assert_approx(actual, expected, test_name)
        real(8), intent(in) :: actual, expected
        character(len=*), intent(in) :: test_name
        
        if (abs(actual - expected) < 1.0d-9) then
            tests_passed = tests_passed + 1
            print '(A,A,A,F12.6,A,F12.6)', "  [PASS] ", test_name, ": ", actual, " == ", expected
        else
            tests_failed = tests_failed + 1
            print '(A,A,A,F12.6,A,F12.6)', "  [FAIL] ", test_name, ": ", actual, " != ", expected
        end if
    end subroutine assert_approx
    
    subroutine assert_equal(actual, expected, test_name)
        integer, intent(in) :: actual, expected
        character(len=*), intent(in) :: test_name
        
        if (actual == expected) then
            tests_passed = tests_passed + 1
            print '(A,A,A,I0,A,I0)', "  [PASS] ", test_name, ": ", actual, " == ", expected
        else
            tests_failed = tests_failed + 1
            print '(A,A,A,I0,A,I0)', "  [FAIL] ", test_name, ": ", actual, " != ", expected
        end if
    end subroutine assert_equal

end program test_polynomial_utils