! polynomial_utils.f90
! A comprehensive polynomial manipulation library with zero external dependencies
! Supports: evaluation, differentiation, integration, root finding, arithmetic operations

module polynomial_utils
    implicit none
    private
    
    ! Constants
    real(8), parameter, public :: POLY_PI = 3.14159265358979323846d0
    real(8), parameter, public :: POLY_EPS = 1.0d-12
    integer, parameter, public :: MAX_ITERATIONS = 100
    
    ! Public procedures
    public :: poly_eval
    public :: poly_eval_horner
    public :: poly_derivative
    public :: poly_integral
    public :: poly_add
    public :: poly_subtract
    public :: poly_multiply
    public :: poly_scale
    public :: poly_degree
    public :: poly_normalize
    public :: poly_print
    public :: poly_roots_bisection
    public :: poly_roots_newton
    public :: poly_roots_durand_kerner
    public :: poly_deflate
    public :: poly_lagrange_interpolate
    public :: poly_from_roots
    public :: poly_compose
    public :: poly_gcd
    public :: poly_value_at_derivative
    
contains

    ! Get the degree of a polynomial (highest non-zero coefficient index)
    function poly_degree(coeffs) result(deg)
        real(8), intent(in) :: coeffs(:)
        integer :: deg
        integer :: i
        
        deg = 0
        do i = size(coeffs), 1, -1
            if (abs(coeffs(i)) > POLY_EPS) then
                deg = i - 1
                exit
            end if
        end do
    end function poly_degree
    
    ! Evaluate polynomial at point x (direct method)
    function poly_eval(coeffs, x) result(y)
        real(8), intent(in) :: coeffs(:)
        real(8), intent(in) :: x
        real(8) :: y
        integer :: i, n
        
        n = size(coeffs)
        y = coeffs(n)
        do i = n - 1, 1, -1
            y = y * x + coeffs(i)
        end do
    end function poly_eval
    
    ! Evaluate polynomial using Horner's method (numerically stable)
    function poly_eval_horner(coeffs, x) result(y)
        real(8), intent(in) :: coeffs(:)
        real(8), intent(in) :: x
        real(8) :: y
        integer :: i, n
        
        n = size(coeffs)
        y = 0.0d0
        do i = n, 1, -1
            y = y * x + coeffs(i)
        end do
    end function poly_eval_horner
    
    ! Compute derivative of polynomial
    function poly_derivative(coeffs) result(dcoeffs)
        real(8), intent(in) :: coeffs(:)
        real(8), allocatable :: dcoeffs(:)
        integer :: n, deg, i
        
        deg = poly_degree(coeffs)
        
        if (deg == 0) then
            allocate(dcoeffs(1))
            dcoeffs(1) = 0.0d0
            return
        end if
        
        n = deg
        allocate(dcoeffs(n))
        
        do i = 1, n
            dcoeffs(i) = coeffs(i+1) * real(i, 8)
        end do
    end function poly_derivative
    
    ! Compute indefinite integral of polynomial
    function poly_integral(coeffs, c) result(icoeffs)
        real(8), intent(in) :: coeffs(:)
        real(8), intent(in), optional :: c  ! Integration constant
        real(8), allocatable :: icoeffs(:)
        integer :: n, deg, i
        real(8) :: const
        
        const = 0.0d0
        if (present(c)) const = c
        
        deg = poly_degree(coeffs)
        n = deg + 2
        
        allocate(icoeffs(n))
        icoeffs(1) = const
        
        do i = 2, n
            icoeffs(i) = coeffs(i-1) / real(i-1, 8)
        end do
    end function poly_integral
    
    ! Add two polynomials
    function poly_add(coeffs1, coeffs2) result(result_coeffs)
        real(8), intent(in) :: coeffs1(:), coeffs2(:)
        real(8), allocatable :: result_coeffs(:)
        integer :: n1, n2, nmax
        integer :: i
        
        n1 = size(coeffs1)
        n2 = size(coeffs2)
        nmax = max(n1, n2)
        
        allocate(result_coeffs(nmax))
        result_coeffs = 0.0d0
        
        do i = 1, n1
            result_coeffs(i) = result_coeffs(i) + coeffs1(i)
        end do
        
        do i = 1, n2
            result_coeffs(i) = result_coeffs(i) + coeffs2(i)
        end do
    end function poly_add
    
    ! Subtract two polynomials (coeffs1 - coeffs2)
    function poly_subtract(coeffs1, coeffs2) result(result_coeffs)
        real(8), intent(in) :: coeffs1(:), coeffs2(:)
        real(8), allocatable :: result_coeffs(:)
        integer :: n1, n2, nmax
        integer :: i
        
        n1 = size(coeffs1)
        n2 = size(coeffs2)
        nmax = max(n1, n2)
        
        allocate(result_coeffs(nmax))
        result_coeffs = 0.0d0
        
        do i = 1, n1
            result_coeffs(i) = result_coeffs(i) + coeffs1(i)
        end do
        
        do i = 1, n2
            result_coeffs(i) = result_coeffs(i) - coeffs2(i)
        end do
    end function poly_subtract
    
    ! Multiply two polynomials
    function poly_multiply(coeffs1, coeffs2) result(result_coeffs)
        real(8), intent(in) :: coeffs1(:), coeffs2(:)
        real(8), allocatable :: result_coeffs(:)
        integer :: n1, n2, n
        integer :: i, j
        
        n1 = size(coeffs1)
        n2 = size(coeffs2)
        n = n1 + n2 - 1
        
        allocate(result_coeffs(n))
        result_coeffs = 0.0d0
        
        do i = 1, n1
            do j = 1, n2
                result_coeffs(i + j - 1) = result_coeffs(i + j - 1) + coeffs1(i) * coeffs2(j)
            end do
        end do
    end function poly_multiply
    
    ! Scale polynomial by a constant
    function poly_scale(coeffs, scalar) result(result_coeffs)
        real(8), intent(in) :: coeffs(:)
        real(8), intent(in) :: scalar
        real(8), allocatable :: result_coeffs(:)
        
        allocate(result_coeffs(size(coeffs)))
        result_coeffs = coeffs * scalar
    end function poly_scale
    
    ! Normalize polynomial (remove trailing zeros)
    function poly_normalize(coeffs) result(norm_coeffs)
        real(8), intent(in) :: coeffs(:)
        real(8), allocatable :: norm_coeffs(:)
        integer :: deg
        
        deg = poly_degree(coeffs)
        allocate(norm_coeffs(deg + 1))
        norm_coeffs = coeffs(1:deg+1)
    end function poly_normalize
    
    ! Print polynomial in human-readable form
    subroutine poly_print(coeffs, var_name)
        real(8), intent(in) :: coeffs(:)
        character(len=*), intent(in), optional :: var_name
        character(len=1) :: var
        integer :: i, n, first
        real(8) :: c
        
        var = 'x'
        if (present(var_name)) var = trim(var_name(1:1))
        
        n = size(coeffs)
        first = 1
        
        do i = n, 1, -1
            c = coeffs(i)
            if (abs(c) < POLY_EPS) cycle
            
            if (first == 0) then
                if (c > 0) then
                    write(*,'(A)', advance='no') ' + '
                else
                    write(*,'(A)', advance='no') ' - '
                    c = abs(c)
                end if
            else
                first = 0
                if (c < 0) then
                    write(*,'(A)', advance='no') '-'
                    c = abs(c)
                end if
            end if
            
            if (i == 1) then
                write(*,'(F12.6)', advance='no') c
            else if (i == 2) then
                if (abs(c - 1.0d0) < POLY_EPS) then
                    write(*,'(A)', advance='no') var
                else
                    write(*,'(F12.6,A)', advance='no') c, var
                end if
            else
                if (abs(c - 1.0d0) < POLY_EPS) then
                    write(*,'(A,A,I0)', advance='no') var, '^', i-1
                else
                    write(*,'(F12.6,A,A,I0)', advance='no') c, var, '^', i-1
                end if
            end if
        end do
        
        if (first == 1) then
            write(*,'(F12.6)', advance='no') 0.0d0
        end if
        
        write(*,*)
    end subroutine poly_print
    
    ! Find root using bisection method
    function poly_roots_bisection(coeffs, a, b, tol) result(root)
        real(8), intent(in) :: coeffs(:)
        real(8), intent(in) :: a, b
        real(8), intent(in), optional :: tol
        real(8) :: root
        real(8) :: fa, fb, fc, c, left, right
        real(8) :: tolerance
        integer :: i
        
        tolerance = POLY_EPS
        if (present(tol)) tolerance = tol
        
        left = a
        right = b
        
        fa = poly_eval(coeffs, left)
        fb = poly_eval(coeffs, right)
        
        if (fa * fb > 0) then
            root = huge(1.0d0)  ! No root in interval
            return
        end if
        
        root = right
        do i = 1, MAX_ITERATIONS
            c = (left + right) / 2.0d0
            fc = poly_eval(coeffs, c)
            
            if (abs(fc) < tolerance .or. abs(right - left) < tolerance) then
                root = c
                return
            end if
            
            if (fa * fc < 0) then
                right = c
                fb = fc
            else
                left = c
                fa = fc
            end if
        end do
        
        root = c
    end function poly_roots_bisection
    
    ! Find root using Newton-Raphson method
    function poly_roots_newton(coeffs, x0, tol) result(root)
        real(8), intent(in) :: coeffs(:)
        real(8), intent(in) :: x0
        real(8), intent(in), optional :: tol
        real(8) :: root
        real(8) :: tolerance
        real(8) :: x, fx, dfx
        real(8), allocatable :: dcoeffs(:)
        integer :: i
        
        tolerance = POLY_EPS
        if (present(tol)) tolerance = tol
        
        dcoeffs = poly_derivative(coeffs)
        x = x0
        
        do i = 1, MAX_ITERATIONS
            fx = poly_eval(coeffs, x)
            dfx = poly_eval(dcoeffs, x)
            
            if (abs(dfx) < POLY_EPS) exit
            
            root = x - fx / dfx
            
            if (abs(root - x) < tolerance) return
            
            x = root
        end do
        
        root = x
    end function poly_roots_newton
    
    ! Find all roots using Durand-Kerner method
    function poly_roots_durand_kerner(coeffs, tol) result(roots)
        real(8), intent(in) :: coeffs(:)
        real(8), intent(in), optional :: tol
        complex(8), allocatable :: roots(:)
        integer :: n, i, j, iter
        real(8) :: tolerance
        real(8), allocatable :: norm_coeffs(:)
        complex(8) :: q, delta, max_delta
        
        tolerance = POLY_EPS
        if (present(tol)) tolerance = tol
        
        norm_coeffs = poly_normalize(coeffs)
        n = poly_degree(norm_coeffs)
        
        if (n == 0) then
            allocate(roots(0))
            return
        end if
        
        allocate(roots(n))
        
        ! Normalize polynomial (leading coefficient = 1)
        norm_coeffs = norm_coeffs / norm_coeffs(n+1)
        
        ! Initial guesses distributed on a circle
        do i = 1, n
            roots(i) = cmplx(cos(2.0d0 * POLY_PI * i / n), sin(2.0d0 * POLY_PI * i / n), 8)
        end do
        
        ! Iterate
        do iter = 1, MAX_ITERATIONS
            max_delta = (0.0d0, 0.0d0)
            
            do i = 1, n
                q = poly_eval_complex(norm_coeffs, roots(i))
                
                do j = 1, n
                    if (j /= i) then
                        q = q / (roots(i) - roots(j))
                    end if
                end do
                
                delta = roots(i) - q
                roots(i) = roots(i) - q
                
                if (abs(delta) > abs(max_delta)) max_delta = delta
            end do
            
            if (abs(max_delta) < tolerance) exit
        end do
    end function poly_roots_durand_kerner
    
    ! Evaluate polynomial at complex point (helper function)
    function poly_eval_complex(coeffs, z) result(y)
        real(8), intent(in) :: coeffs(:)
        complex(8), intent(in) :: z
        complex(8) :: y
        integer :: i, n
        
        n = size(coeffs)
        y = coeffs(n)
        do i = n - 1, 1, -1
            y = y * z + coeffs(i)
        end do
    end function poly_eval_complex
    
    ! Deflate polynomial by removing a root
    function poly_deflate(coeffs, root) result(quotient)
        real(8), intent(in) :: coeffs(:)
        real(8), intent(in) :: root
        real(8), allocatable :: quotient(:)
        integer :: n, i
        real(8), allocatable :: temp(:)
        
        n = poly_degree(coeffs)
        allocate(quotient(n))
        allocate(temp(n+1))
        
        temp = coeffs
        
        do i = n, 2, -1
            quotient(i-1) = temp(i)
            temp(i-1) = temp(i-1) + quotient(i-1) * root
        end do
    end function poly_deflate
    
    ! Lagrange interpolation
    function poly_lagrange_interpolate(x_points, y_points) result(coeffs)
        real(8), intent(in) :: x_points(:), y_points(:)
        real(8), allocatable :: coeffs(:)
        integer :: n, i, j
        real(8), allocatable :: temp(:), basis(:)
        real(8) :: denom
        
        n = size(x_points)
        
        if (n /= size(y_points)) then
            allocate(coeffs(1))
            coeffs(1) = 0.0d0
            return
        end if
        
        allocate(coeffs(n))
        allocate(temp(n))
        allocate(basis(n))
        
        coeffs = 0.0d0
        
        do i = 1, n
            basis = 0.0d0
            basis(1) = 1.0d0
            denom = 1.0d0
            
            do j = 1, n
                if (j /= i) then
                    denom = denom * (x_points(i) - x_points(j))
                    
                    ! Multiply basis by (x - x_points(j))
                    temp = 0.0d0
                    temp(2:n) = basis(1:n-1)
                    temp = temp - x_points(j) * basis
                    basis = temp
                end if
            end do
            
            basis = basis * y_points(i) / denom
            coeffs = coeffs + basis
        end do
    end function poly_lagrange_interpolate
    
    ! Create polynomial from roots
    function poly_from_roots(roots) result(coeffs)
        real(8), intent(in) :: roots(:)
        real(8), allocatable :: coeffs(:)
        integer :: n, i
        real(8), allocatable :: temp(:)
        
        n = size(roots)
        allocate(coeffs(n+1))
        allocate(temp(n+1))
        
        coeffs = 0.0d0
        coeffs(1) = 1.0d0  ! Start with p(x) = 1
        
        do i = 1, n
            ! Multiply by (x - roots(i))
            temp = 0.0d0
            temp(2:i+1) = coeffs(1:i)  ! Shift for x term
            temp = temp - roots(i) * coeffs
            coeffs = temp
        end do
    end function poly_from_roots
    
    ! Compose two polynomials: p(q(x))
    function poly_compose(p, q) result(result_coeffs)
        real(8), intent(in) :: p(:), q(:)
        real(8), allocatable :: result_coeffs(:)
        integer :: np, i
        real(8), allocatable :: power(:)
        
        np = size(p)
        
        allocate(power(1))
        power(1) = 1.0d0
        
        result_coeffs = poly_scale(power, p(1))
        
        do i = 2, np
            ! power = power * q
            power = poly_multiply(power, q)
            
            ! result_coeffs += p(i) * power
            result_coeffs = poly_add(result_coeffs, poly_scale(power, p(i)))
        end do
        
        ! Normalize to remove trailing zeros
        result_coeffs = poly_normalize(result_coeffs)
    end function poly_compose
    
    ! GCD of two polynomials (Euclidean algorithm)
    function poly_gcd(p, q) result(gcd_coeffs)
        real(8), intent(in) :: p(:), q(:)
        real(8), allocatable :: gcd_coeffs(:)
        real(8), allocatable :: a(:), b(:), r(:)
        real(8) :: leading
        
        a = poly_normalize(p)
        b = poly_normalize(q)
        
        do while (poly_degree(b) > 0 .or. abs(b(1)) > POLY_EPS)
            r = poly_remainder(a, b)
            a = b
            b = r
        end do
        
        ! Normalize so leading coefficient is 1
        if (size(a) > 0) then
            leading = a(size(a))
            if (abs(leading) > POLY_EPS) then
                a = a / leading
            end if
        end if
        
        gcd_coeffs = a
    end function poly_gcd
    
    ! Compute remainder of polynomial division
    function poly_remainder(dividend, divisor) result(rem)
        real(8), intent(in) :: dividend(:), divisor(:)
        real(8), allocatable :: rem(:), temp(:)
        integer :: n, m, i
        real(8) :: factor
        
        n = poly_degree(dividend)
        m = poly_degree(divisor)
        
        if (m == 0 .and. abs(divisor(1)) < POLY_EPS) then
            allocate(rem(1))
            rem(1) = huge(1.0d0)
            return
        end if
        
        allocate(temp(n+1))
        temp = dividend(1:n+1)
        
        do i = n, m, -1
            factor = temp(i+1) / divisor(m+1)
            temp(i-m+1:i+1) = temp(i-m+1:i+1) - factor * divisor(1:m+1)
        end do
        
        rem = poly_normalize(temp)
    end function poly_remainder
    
    ! Evaluate polynomial and its derivative at a point
    subroutine poly_value_at_derivative(coeffs, x, value, deriv_value)
        real(8), intent(in) :: coeffs(:)
        real(8), intent(in) :: x
        real(8), intent(out) :: value, deriv_value
        real(8), allocatable :: dcoeffs(:)
        
        value = poly_eval(coeffs, x)
        dcoeffs = poly_derivative(coeffs)
        deriv_value = poly_eval(dcoeffs, x)
    end subroutine poly_value_at_derivative

end module polynomial_utils