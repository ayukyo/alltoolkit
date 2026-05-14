program examples_polynomial_utils
    use polynomial_utils
    implicit none
    
    real(8), allocatable :: coeffs(:), coeffs2(:), coeffs3(:)
    real(8), allocatable :: deriv(:), integ(:), sum_poly(:), prod(:)
    real(8), allocatable :: interp(:), from_roots(:), gcd_result(:)
    real(8) :: x, val
    real(8) :: roots(3)
    complex(8), allocatable :: all_roots(:)
    integer :: i
    
    print *, "========================================"
    print *, "  Polynomial Utils Examples"
    print *, "========================================"
    print *
    
    ! Example 1: Polynomial Evaluation
    print *, "Example 1: Polynomial Evaluation"
    print *, "---------------------------------"
    coeffs = [1.0d0, -5.0d0, 6.0d0, 1.0d0]  ! 1 - 5x + 6x^2 + x^3
    print *, "Polynomial: "
    call poly_print(coeffs, 'x')
    print *
    
    do i = -2, 3
        x = real(i, 8)
        val = poly_eval(coeffs, x)
        print '(A,F5.1,A,F10.4)', "  p(", x, ") = ", val
    end do
    print *
    
    ! Example 2: Derivatives and Integrals
    print *, "Example 2: Derivatives and Integrals"
    print *, "------------------------------------"
    coeffs = [1.0d0, 2.0d0, 3.0d0]  ! 1 + 2x + 3x^2
    
    print *, "Original polynomial: "
    call poly_print(coeffs, 'x')
    
    deriv = poly_derivative(coeffs)
    print *, "Derivative: "
    call poly_print(deriv, 'x')
    
    integ = poly_integral(coeffs, 0.0d0)
    print *, "Indefinite integral (c=0): "
    call poly_print(integ, 'x')
    print *
    
    ! Example 3: Arithmetic Operations
    print *, "Example 3: Arithmetic Operations"
    print *, "-------------------------------"
    coeffs = [1.0d0, 1.0d0]    ! 1 + x
    coeffs2 = [2.0d0, 1.0d0]   ! 2 + x
    
    print *, "p(x) = "
    call poly_print(coeffs, 'x')
    print *, "q(x) = "
    call poly_print(coeffs2, 'x')
    
    sum_poly = poly_add(coeffs, coeffs2)
    print *, "p(x) + q(x) = "
    call poly_print(sum_poly, 'x')
    
    prod = poly_multiply(coeffs, coeffs2)
    print *, "p(x) * q(x) = "
    call poly_print(prod, 'x')
    print *
    
    ! Example 4: Root Finding
    print *, "Example 4: Root Finding"
    print *, "----------------------"
    coeffs = [-4.0d0, 0.0d0, 1.0d0]  ! x^2 - 4
    
    print *, "Finding roots of: "
    call poly_print(coeffs, 'x')
    
    val = poly_roots_bisection(coeffs, 0.0d0, 3.0d0, 1.0d-10)
    print '(A,F12.6)', "  Bisection method (interval [0,3]): ", val
    
    val = poly_roots_newton(coeffs, 2.5d0, 1.0d-10)
    print '(A,F12.6)', "  Newton-Raphson method (initial guess 2.5): ", val
    print *
    
    ! Example 5: Find All Roots (Durand-Kerner)
    print *, "Example 5: Find All Roots (Durand-Kerner)"
    print *, "-----------------------------------------"
    coeffs = [6.0d0, -5.0d0, -2.0d0, 1.0d0]  ! 6 - 5x - 2x^2 + x^3 = (x-1)(x-2)(x+3)
    
    print *, "Polynomial: "
    call poly_print(coeffs, 'x')
    
    all_roots = poly_roots_durand_kerner(coeffs, 1.0d-10)
    print *, "Roots found:"
    do i = 1, size(all_roots)
        if (abs(aimag(all_roots(i))) < 1.0d-6) then
            print '(A,F12.6)', "  x = ", real(all_roots(i))
        else
            print '(A,F12.6,A,F12.6,A)', "  x = ", real(all_roots(i)), " + ", aimag(all_roots(i)), "i"
        end if
    end do
    print *
    
    ! Example 6: Lagrange Interpolation
    print *, "Example 6: Lagrange Interpolation"
    print *, "--------------------------------"
    print *, "Interpolating through points: (0,1), (1,2), (2,5)"
    
    interp = poly_lagrange_interpolate([0.0d0, 1.0d0, 2.0d0], [1.0d0, 2.0d0, 5.0d0])
    print *, "Interpolating polynomial: "
    call poly_print(interp, 'x')
    
    do i = 0, 2
        x = real(i, 8)
        val = poly_eval(interp, x)
        print '(A,F5.1,A,F10.4)', "  p(", x, ") = ", val
    end do
    print *
    
    ! Example 7: Polynomial from Roots
    print *, "Example 7: Polynomial from Roots"
    print *, "--------------------------------"
    roots = [1.0d0, 2.0d0, 3.0d0]
    print *, "Creating polynomial with roots: 1, 2, 3"
    
    from_roots = poly_from_roots(roots)
    print *, "Result: "
    call poly_print(from_roots, 'x')
    
    print *, "Verification:"
    do i = 1, 3
        val = poly_eval(from_roots, roots(i))
        print '(A,I0,A,F12.6)', "  p(", int(roots(i)), ") = ", val
    end do
    print *
    
    ! Example 8: Polynomial Composition
    print *, "Example 8: Polynomial Composition"
    print *, "---------------------------------"
    coeffs = [1.0d0, 0.0d0, 1.0d0]    ! 1 + x^2
    coeffs2 = [1.0d0, 1.0d0]          ! 1 + x
    
    print *, "p(x) = "
    call poly_print(coeffs, 'x')
    print *, "q(x) = "
    call poly_print(coeffs2, 'x')
    
    prod = poly_compose(coeffs, coeffs2)
    print *, "p(q(x)) = "
    call poly_print(prod, 'x')
    print *
    
    ! Example 9: GCD of Polynomials
    print *, "Example 9: GCD of Polynomials"
    print *, "----------------------------"
    
    ! p(x) = (x-1)(x-2)(x+1) = x^3 - 2x^2 - x + 2
    ! q(x) = (x-1)(x+1) = x^2 - 1
    coeffs = [2.0d0, -1.0d0, -2.0d0, 1.0d0]
    coeffs2 = [-1.0d0, 0.0d0, 1.0d0]
    
    print *, "p(x) = "
    call poly_print(coeffs, 'x')
    print *, "q(x) = "
    call poly_print(coeffs2, 'x')
    
    gcd_result = poly_gcd(coeffs, coeffs2)
    print *, "GCD = "
    call poly_print(gcd_result, 'x')
    
    print *
    print *, "========================================"
    print *, "  Examples Complete!"
    print *, "========================================"

end program examples_polynomial_utils