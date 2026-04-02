!! AllToolkit - Fortran Math Utilities Module
!! Zero-dependency mathematical utility functions for Fortran 90/95/2003+
!!
!! Features:
!! - Vector and matrix operations
!! - Statistical functions
!! - Numerical utilities
!! - Trigonometric helpers
!! - Interpolation and approximation
!!
!! Author: AllToolkit Contributors
!! License: MIT

module math_utils
    implicit none
    
    ! Module constants
    real(8), parameter :: PI = 3.14159265358979323846d0
    real(8), parameter :: E = 2.71828182845904523536d0
    real(8), parameter :: EPSILON = 1.0d-10
    real(8), parameter :: DEG_TO_RAD = PI / 180.0d0
    real(8), parameter :: RAD_TO_DEG = 180.0d0 / PI
    
    ! Interface for generic functions
    interface mean
        module procedure mean_real, mean_int
    end interface
    
    interface std_dev
        module procedure std_dev_real, std_dev_int
    end interface
    
    interface variance
        module procedure variance_real, variance_int
    end interface
    
    interface clamp
        module procedure clamp_real, clamp_int
    end interface
    
    interface linspace
        module procedure linspace_real
    end interface
    
    interface interp_linear
        module procedure interp_linear_real
    end interface
    
contains

    !==========================================================================
    ! Vector Operations
    !==========================================================================
    
    !> Calculate the dot product of two vectors
    !! @param a First vector
    !! @param b Second vector
    !! @return Dot product of a and b
    function dot_product_real(a, b) result(res)
        real(8), intent(in) :: a(:), b(:)
        real(8) :: res
        integer :: n, i
        n = min(size(a), size(b))
        res = 0.0d0
        do i = 1, n
            res = res + a(i) * b(i)
        end do
    end function dot_product_real
    
    !> Calculate the magnitude (L2 norm) of a vector
    !! @param vec Input vector
    !! @return Magnitude of the vector
    function vector_magnitude(vec) result(res)
        real(8), intent(in) :: vec(:)
        real(8) :: res
        integer :: i
        res = 0.0d0
        do i = 1, size(vec)
            res = res + vec(i) * vec(i)
        end do
        res = sqrt(res)
    end function vector_magnitude
    
    !> Normalize a vector (unit vector)
    !! @param vec Input vector
    !! @return Normalized vector
    function normalize_vector(vec) result(res)
        real(8), intent(in) :: vec(:)
        real(8) :: res(size(vec))
        real(8) :: mag
        mag = vector_magnitude(vec)
        if (mag > EPSILON) then
            res = vec / mag
        else
            res = 0.0d0
        end if
    end function normalize_vector
    
    !> Calculate the cross product of two 3D vectors
    !! @param a First 3D vector
    !! @param b Second 3D vector
    !! @return Cross product a x b
    function cross_product(a, b) result(res)
        real(8), intent(in) :: a(3), b(3)
        real(8) :: res(3)
        res(1) = a(2) * b(3) - a(3) * b(2)
        res(2) = a(3) * b(1) - a(1) * b(3)
        res(3) = a(1) * b(2) - a(2) * b(1)
    end function cross_product
    
    !> Calculate the angle between two vectors (in radians)
    !! @param a First vector
    !! @param b Second vector
    !! @return Angle in radians
    function vector_angle(a, b) result(res)
        real(8), intent(in) :: a(:), b(:)
        real(8) :: res
        real(8) :: dot, mag_a, mag_b
        dot = dot_product_real(a, b)
        mag_a = vector_magnitude(a)
        mag_b = vector_magnitude(b)
        if (mag_a > EPSILON .and. mag_b > EPSILON) then
            res = acos(max(-1.0d0, min(1.0d0, dot / (mag_a * mag_b))))
        else
            res = 0.0d0
        end if
    end function vector_angle
    
    !> Calculate the distance between two points
    !! @param a First point
    !! @param b Second point
    !! @return Euclidean distance
    function euclidean_distance(a, b) result(res)
        real(8), intent(in) :: a(:), b(:)
        real(8) :: res
        integer :: n, i
        n = min(size(a), size(b))
        res = 0.0d0
        do i = 1, n
            res = res + (a(i) - b(i)) ** 2
        end do
        res = sqrt(res)
    end function euclidean_distance
    
    !==========================================================================
    ! Statistical Functions
    !==========================================================================
    
    !> Calculate the arithmetic mean of real array
    !! @param arr Input array
    !! @return Mean value
    function mean_real(arr) result(res)
        real(8), intent(in) :: arr(:)
        real(8) :: res
        integer :: n
        n = size(arr)
        if (n > 0) then
            res = sum(arr) / real(n, 8)
        else
            res = 0.0d0
        end if
    end function mean_real
    
    !> Calculate the arithmetic mean of integer array
    !! @param arr Input array
    !! @return Mean value
    function mean_int(arr) result(res)
        integer, intent(in) :: arr(:)
        real(8) :: res
        integer :: n
        n = size(arr)
        if (n > 0) then
            res = sum(real(arr, 8)) / real(n, 8)
        else
            res = 0.0d0
        end if
    end function mean_int
    
    !> Calculate the variance of real array
    !! @param arr Input array
    !! @param sample If true, calculate sample variance (N-1), else population (N)
    !! @return Variance
    function variance_real(arr, sample) result(res)
        real(8), intent(in) :: arr(:)
        logical, intent(in), optional :: sample
        real(8) :: res, m, diff
        integer :: n, i
        logical :: use_sample
        use_sample = .false.
        if (present(sample)) use_sample = sample
        n = size(arr)
        if (n <= 0) then
            res = 0.0d0
            return
        end if
        m = mean_real(arr)
        res = 0.0d0
        do i = 1, n
            diff = arr(i) - m
            res = res + diff * diff
        end do
        if (use_sample .and. n > 1) then
            res = res / real(n - 1, 8)
        else
            res = res / real(n, 8)
        end if
    end function variance_real
    
    !> Calculate the variance of integer array
    !! @param arr Input array
    !! @param sample If true, calculate sample variance (N-1), else population (N)
    !! @return Variance
    function variance_int(arr, sample) result(res)
        integer, intent(in) :: arr(:)
        logical, intent(in), optional :: sample
        real(8) :: res
        real(8) :: arr_real(size(arr))
        arr_real = real(arr, 8)
        res = variance_real(arr_real, sample)
    end function variance_int
    
    !> Calculate the standard deviation of real array
    !! @param arr Input array
    !! @param sample If true, calculate sample std dev (N-1), else population (N)
    !! @return Standard deviation
    function std_dev_real(arr, sample) result(res)
        real(8), intent(in) :: arr(:)
        logical, intent(in), optional :: sample
        real(8) :: res
        res = sqrt(variance_real(arr, sample))
    end function std_dev_real
    
    !> Calculate the standard deviation of integer array
    !! @param arr Input array
    !! @param sample If true, calculate sample std dev (N-1), else population (N)
    !! @return Standard deviation
    function std_dev_int(arr, sample) result(res)
        integer, intent(in) :: arr(:)
        logical, intent(in), optional :: sample
        real(8) :: res
        res = sqrt(variance_int(arr, sample))
    end function std_dev_int
    
    !> Calculate the median of an array
    !! @param arr Input array
    !! @return Median value
    function median_real(arr) result(res)
        real(8), intent(in) :: arr(:)
        real(8) :: res
        real(8), allocatable :: sorted(:)
        integer :: n
        n = size(arr)
        if (n <= 0) then
            res = 0.0d0
            return
        end if
        allocate(sorted(n))
        sorted = arr
        call quicksort(sorted, 1, n)
        if (mod(n, 2) == 1) then
            res = sorted(n/2 + 1)
        else
            res = (sorted(n/2) + sorted(n/2 + 1)) / 2.0d0
        end if
        deallocate(sorted)
    end function median_real
    
    !> Quick sort helper subroutine
    !! @param arr Array to sort
    !! @param low Lower bound
    !! @param high Upper bound
    recursive subroutine quicksort(arr, low, high)
        real(8), intent(inout) :: arr(:)
        integer, intent(in) :: low, high
        integer :: i, j
        real(8) :: pivot, temp
        if (low < high) then
            pivot = arr(high)
            i = low - 1
            do j = low, high - 1
                if (arr(j) <= pivot) then
                    i = i + 1
                    temp = arr(i)
                    arr(i) = arr(j)
                    arr(j) = temp
                end if
            end do
            temp = arr(i + 1)
            arr(i + 1) = arr(high)
            arr(high) = temp
            call quicksort(arr, low, i)
            call quicksort(arr, i + 2, high)
        end if
    end subroutine quicksort
    
    !> Find minimum value in array
    !! @param arr Input array
    !! @return Minimum value
    function min_value(arr) result(res)
        real(8), intent(in) :: arr(:)
        real(8) :: res
        integer :: n, i
        n = size(arr)
        if (n > 0) then
            res = arr(1)
            do i = 2, n
                if (arr(i) < res) res = arr(i)
            end do
        else
            res = 0.0d0
        end if
    end function min_value
    
    !> Find maximum value in array
    !! @param arr Input array
    !! @return Maximum value
    function max_value(arr) result(res)
        real(8), intent(in) :: arr(:)
        real(8) :: res
        integer :: n, i
        n = size(arr)
        if (n > 0) then
            res = arr(1)
            do i = 2, n
                if (arr(i) > res) res = arr(i)
            end do
        else
            res = 0.0d0
        end if
    end function max_value
    
    !> Calculate sum of array elements
    !! @param arr Input array
    !! @return Sum of elements
    function sum_values(arr) result(res)
        real(8), intent(in) :: arr(:)
        real(8) :: res
        res = sum(arr)
    end function sum_values
    
    !> Calculate product of array elements
    !! @param arr Input array
    !! @return Product of elements
    function product_values(arr) result(res)
        real(8), intent(in) :: arr(:)
        real(8) :: res
        integer :: n, i
        n = size(arr)
        if (n > 0) then
            res = 1.0d0
            do i = 1, n
                res = res * arr(i)
            end do
        else
            res = 0.0d0
        end if
    end function product_values
    
    !==========================================================================
    ! Numerical Utilities
    !==========================================================================
    
    !> Clamp a value between min and max
    !! @param value Input value
    !! @param min_val Minimum allowed value
    !! @param max_val Maximum allowed value
    !! @return Clamped value
    function clamp_real(value, min_val, max_val) result(res)
        real(8), intent(in) :: value, min_val, max_val
        real(8) :: res
        res = max(min_val, min(max_val, value))
    end function clamp_real
    
    !> Clamp an integer value between min and max
    !! @param value Input value
    !! @param min_val Minimum allowed value
    !! @param max_val Maximum allowed value
    !! @return Clamped value
    function clamp_int(value, min_val, max_val) result(res)
        integer, intent(in) :: value, min_val, max_val
        integer :: res
        res = max(min_val, min(max_val, value))
    end function clamp_int
    
    !> Linear interpolation between two values
    !! @param a Start value
    !! @param b End value
    !! @param t Interpolation factor (0.0 to 1.0)
    !! @return Interpolated value
    function lerp(a, b, t) result(res)
        real(8), intent(in) :: a, b, t
        real(8) :: res
        res = a + (b - a) * clamp_real(t, 0.0d0, 1.0d0)
    end function lerp
    
    !> Smooth step interpolation (Hermite)
    !! @param edge0 Lower edge
    !! @param edge1 Upper edge
    !! @param x Input value
    !! @return Smooth step value
    function smoothstep(edge0, edge1, x) result(res)
        real(8), intent(in) :: edge0, edge1, x
        real(8) :: res, t
        t = clamp_real((x - edge0) / (edge1 - edge0), 0.0d0, 1.0d0)
        res = t * t * (3.0d0 - 2.0d0 * t)
    end function smoothstep
    
    !> Check if two values are approximately equal
    !! @param a First value
    !! @param b Second value
    !! @param tolerance Tolerance for comparison
    !! @return True if approximately equal
    function approx_equal(a, b, tolerance) result(res)
        real(8), intent(in) :: a, b
        real(8), intent(in), optional :: tolerance
        real(8) :: tol
        logical :: res
        tol = EPSILON
        if (present(tolerance)) tol = tolerance
        res = abs(a - b) <= tol
    end function approx_equal
    
    !> Check if value is power of two
    !! @param n Integer value
    !! @return True if power of two
    function is_power_of_two(n) result(res)
        integer, intent(in) :: n
        logical :: res
        res = n > 0 .and. iand(n, n - 1) == 0
    end function is_power_of_two
    
    !> Get next power of two
    !! @param n Integer value
    !! @return Next power of two
    function next_power_of_two(n) result(res)
        integer, intent(in) :: n
        integer :: res
        res = n - 1
        res = ior(res, ishft(res, -1))
        res = ior(res, ishft(res, -2))
        res = ior(res, ishft(res, -4))
        res = ior(res, ishft(res, -8))
        res = ior(res, ishft(res, -16))
        res = res + 1
        if (n <= 0) res = 1
    end function next_power_of_two
    
    !> Generate linearly spaced array
    !! @param start Start value
    !! @param end_val End value
    !! @param n Number of points
    !! @return Array of n linearly spaced values
    function linspace_real(start, end_val, n) result(res)
        real(8), intent(in) :: start, end_val
        integer, intent(in) :: n
        real(8), allocatable :: res(:)
        real(8) :: step
        integer :: i
        allocate(res(n))
        if (n > 1) then
            step = (end_val - start) / real(n - 1, 8)
            do i = 1, n
                res(i) = start + step * real(i - 1, 8)
            end do
        else if (n == 1) then
            res(1) = start
        end if
    end function linspace_real
    
    !> Map value from one range to another
    !! @param value Input value
    !! @param in_min Input range minimum
    !! @param in_max Input range maximum
    !! @param out_min Output range minimum
    !! @param out_max Output range maximum
    !! @return Mapped value
    function map_range(value, in_min, in_max, out_min, out_max) result(res)
        real(8), intent(in) :: value, in_min, in_max, out_min, out_max
        real(8) :: res
        res = out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)
    end function map_range
    
    !==========================================================================
    ! Trigonometric Helpers
    !==========================================================================
    
    !> Convert degrees to radians
    !! @param degrees Angle in degrees
    !! @return Angle in radians
    function to_radians(degrees) result(res)
        real(8), intent(in) :: degrees
        real(8) :: res
        res = degrees * DEG_TO_RAD
    end function to_radians
    
    !> Convert radians to degrees
    !! @param radians Angle in radians
    !! @return Angle in degrees
    function to_degrees(radians) result(res)
        real(8), intent(in) :: radians
        real(8) :: res
        res = radians * RAD_TO_DEG
    end function to_degrees
    
    !> Wrap angle to [0, 2*PI) range
    !! @param angle Angle in radians
    !! @return Wrapped angle
    function wrap_angle(angle) result(res)
        real(8), intent(in) :: angle
        real(8) :: res
        res = angle - 2.0d0 * PI * floor(angle / (2.0d0 * PI))
    end function wrap_angle
    
    !> Wrap angle to [-PI, PI) range
    !! @param angle Angle in radians
    !! @return Wrapped angle
    function wrap_angle_signed(angle) result(res)
        real(8), intent(in) :: angle
        real(8) :: res
        res = wrap_angle(angle + PI) - PI
    end function wrap_angle_signed
    
    !==========================================================================
    ! Interpolation
    !==========================================================================
    
    !> Linear interpolation for 1D data
    !! @param x Known x values (must be sorted)
    !! @param y Known y values
    !! @param xi Interpolation point
    !! @return Interpolated value
    function interp_linear_real(x, y, xi) result(res)
        real(8), intent(in) :: x(:), y(:)
        real(8), intent(in) :: xi
        real(8) :: res
        integer :: n, i, idx
        real(8) :: t
        n = min(size(x), size(y))
        if (n == 0) then
            res = 0.0d0
            return
        end if
        if (xi <= x(1)) then
            res = y(1)
            return
        end if
        if (xi >= x(n)) then
            res = y(n)
            return
        end if
        idx = 1
        do i = 2, n
            if (x(i) > xi) then
                idx = i - 1
                exit
            end if
        end do
        t = (xi - x(idx)) / (x(idx + 1) - x(idx))
        res = y(idx) + t * (y(idx + 1) - y(idx))
    end function interp_linear_real
    
    !==========================================================================
    ! Matrix Operations (2D)
    !==========================================================================
    
    !> Multiply two matrices
    !! @param a First matrix (m x n)
    !! @param b Second matrix (n x p)
    !! @return Result matrix (m x p)
    function matrix_multiply(a, b) result(res)
        real(8), intent(in) :: a(:,:), b(:,:)
        real(8), allocatable :: res(:,:)
        integer :: m, n, p, i, j, k
        m = size(a, 1)
        n = size(a, 2)
        p = size(b, 2)
        allocate(res(m, p))
        res = 0.0d0
        if (size(b, 1) == n) then
            do i = 1, m
                do j = 1, p
                    do k = 1, n
                        res(i, j) = res(i, j) + a(i, k) * b(k, j)
                    end do
                end do
            end do
        end if
    end function matrix_multiply
    
    !> Transpose a matrix
    !! @param mat Input matrix
    !! @return Transposed matrix
    function matrix_transpose(mat) result(res)
        real(8), intent(in) :: mat(:,:)
        real(8), allocatable :: res(:,:)
        integer :: m, n, i, j
        m = size(mat, 1)
        n = size(mat, 2)
        allocate(res(n, m))
        do i = 1, m
            do j = 1, n
                res(j, i) = mat(i, j)
            end do
        end do
    end function matrix_transpose
    
    !> Calculate determinant of 2x2 or 3x3 matrix
    !! @param mat Square matrix (2x2 or 3x3)
    !! @return Determinant
    function matrix_determinant(mat) result(res)
        real(8), intent(in) :: mat(:,:)
        real(8) :: res
        integer :: n
        n = size(mat, 1)
        if (n == 2 .and. size(mat, 2) == 2) then
            res = mat(1,1) * mat(2,2) - mat(1,2) * mat(2,1)
        else if (n == 3 .and. size(mat, 2) == 3) then
            res = mat(1,1) * (mat(2,2) * mat(3,3) - mat(2,3) * mat(3,2)) &
                - mat(1,2) * (mat(2,1) * mat(3,3) - mat(2,3) * mat(3,1)) &
                + mat(1,3) * (mat(2,1) * mat(3,2) - mat(2,2) * mat(3,1))
        else
            res = 0.0d0
        end if
    end function matrix_determinant
    
    !> Create identity matrix
    !! @param n Matrix size
    !! @return Identity matrix
    function identity_matrix(n) result(res)
        integer, intent(in) :: n
        real(8), allocatable :: res(:,:)
        integer :: i
        allocate(res(n, n))
        res = 0.0d0
        do i = 1, n
            res(i, i) = 1.0d0
        end do
    end function identity_matrix

end module math_utils