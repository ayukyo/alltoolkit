!! AllToolkit - Fortran Math Utilities Test Suite
!! Unit tests for math_utils module
!!
!! Run with: gfortran -o math_test mod.f90 math_utils_test.f90 && ./math_test

program math_utils_test
    use math_utils
    implicit none
    
    integer :: passed = 0
    integer :: failed = 0
    
    call test_vector_operations()
    call test_statistical_functions()
    call test_numerical_utilities()
    call test_trigonometric_helpers()
    call test_interpolation()
    call test_matrix_operations()
    
    print *, ""
    print *, "========================================"
    print *, "Test Results:"
    print *, "  Passed: ", passed
    print *, "  Failed: ", failed
    print *, "========================================"
    
    if (failed > 0) then
        stop 1
    end if
    
contains

    subroutine assert_true(condition, test_name)
        logical, intent(in) :: condition
        character(*), intent(in) :: test_name
        if (condition) then
            print *, "[PASS] ", test_name
            passed = passed + 1
        else
            print *, "[FAIL] ", test_name
            failed = failed + 1
        end if
    end subroutine assert_true
    
    subroutine assert_approx_equal(a, b, tolerance, test_name)
        real(8), intent(in) :: a, b, tolerance
        character(*), intent(in) :: test_name
        call assert_true(abs(a - b) <= tolerance, test_name)
    end subroutine assert_approx_equal
    
    subroutine test_vector_operations()
        real(8) :: a(3), b(3), c(3), result_vec(3)
        real(8) :: result_scalar
        
        print *, ""
        print *, "--- Vector Operations Tests ---"
        
        ! Test dot product
        a = [1.0d0, 2.0d0, 3.0d0]
        b = [4.0d0, 5.0d0, 6.0d0]
        result_scalar = dot_product_real(a, b)
        call assert_approx_equal(result_scalar, 32.0d0, EPSILON, "dot_product_real")
        
        ! Test vector magnitude
        a = [3.0d0, 4.0d0, 0.0d0]
        result_scalar = vector_magnitude(a)
        call assert_approx_equal(result_scalar, 5.0d0, EPSILON, "vector_magnitude")
        
        ! Test normalize vector
        a = [3.0d0, 0.0d0, 4.0d0]
        result_vec = normalize_vector(a)
        call assert_approx_equal(vector_magnitude(result_vec), 1.0d0, EPSILON, "normalize_vector")
        
        ! Test cross product
        a = [1.0d0, 0.0d0, 0.0d0]
        b = [0.0d0, 1.0d0, 0.0d0]
        c = cross_product(a, b)
        call assert_true(abs(c(1) - 0.0d0) < EPSILON .and. &
                        abs(c(2) - 0.0d0) < EPSILON .and. &
                        abs(c(3) - 1.0d0) < EPSILON, "cross_product")
        
        ! Test vector angle
        a = [1.0d0, 0.0d0, 0.0d0]
        b = [0.0d0, 1.0d0, 0.0d0]
        result_scalar = vector_angle(a, b)
        call assert_approx_equal(result_scalar, PI / 2.0d0, EPSILON, "vector_angle (90 degrees)")
        
        ! Test euclidean distance
        a = [0.0d0, 0.0d0, 0.0d0]
        b = [3.0d0, 4.0d0, 0.0d0]
        result_scalar = euclidean_distance(a, b)
        call assert_approx_equal(result_scalar, 5.0d0, EPSILON, "euclidean_distance")
    end subroutine test_vector_operations
    
    subroutine test_statistical_functions()
        real(8) :: arr_real(5)
        integer :: arr_int(5)
        real(8) :: result_scalar
        
        print *, ""
        print *, "--- Statistical Functions Tests ---"
        
        ! Test mean (real)
        arr_real = [1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0]
        result_scalar = mean_real(arr_real)
        call assert_approx_equal(result_scalar, 3.0d0, EPSILON, "mean_real")
        
        ! Test mean (integer)
        arr_int = [1, 2, 3, 4, 5]
        result_scalar = mean_int(arr_int)
        call assert_approx_equal(result_scalar, 3.0d0, EPSILON, "mean_int")
        
        ! Test variance (population)
        arr_real = [2.0d0, 4.0d0, 4.0d0, 4.0d0, 5.0d0, 5.0d0, 7.0d0, 9.0d0]
        result_scalar = variance_real(arr_real, .false.)
        call assert_approx_equal(result_scalar, 4.0d0, 0.01d0, "variance_real (population)")
        
        ! Test variance (sample)
        result_scalar = variance_real(arr_real, .true.)
        call assert_approx_equal(result_scalar, 4.571d0, 0.01d0, "variance_real (sample)")
        
        ! Test standard deviation
        result_scalar = std_dev_real(arr_real, .false.)
        call assert_approx_equal(result_scalar, 2.0d0, 0.01d0, "std_dev_real")
        
        ! Test median
        arr_real = [1.0d0, 3.0d0, 5.0d0]
        result_scalar = median_real(arr_real)
        call assert_approx_equal(result_scalar, 3.0d0, EPSILON, "median_real (odd)")
        
        arr_real = [1.0d0, 2.0d0, 3.0d0, 4.0d0]
        result_scalar = median_real(arr_real)
        call assert_approx_equal(result_scalar, 2.5d0, EPSILON, "median_real (even)")
        
        ! Test min/max
        arr_real = [5.0d0, 2.0d0, 8.0d0, 1.0d0, 9.0d0]
        call assert_approx_equal(min_value(arr_real), 1.0d0, EPSILON, "min_value")
        call assert_approx_equal(max_value(arr_real), 9.0d0, EPSILON, "max_value")
        
        ! Test sum and product
        arr_real = [1.0d0, 2.0d0, 3.0d0, 4.0d0]
        call assert_approx_equal(sum_values(arr_real), 10.0d0, EPSILON, "sum_values")
        call assert_approx_equal(product_values(arr_real), 24.0d0, EPSILON, "product_values")
    end subroutine test_statistical_functions
    
    subroutine test_numerical_utilities()
        real(8) :: result_scalar
        integer :: result_int
        real(8), allocatable :: arr(:)
        
        print *, ""
        print *, "--- Numerical Utilities Tests ---"
        
        ! Test clamp (real)
        result_scalar = clamp_real(5.0d0, 0.0d0, 10.0d0)
        call assert_approx_equal(result_scalar, 5.0d0, EPSILON, "clamp_real (within range)")
        
        result_scalar = clamp_real(-5.0d0, 0.0d0, 10.0d0)
        call assert_approx_equal(result_scalar, 0.0d0, EPSILON, "clamp_real (below min)")
        
        result_scalar = clamp_real(15.0d0, 0.0d0, 10.0d0)
        call assert_approx_equal(result_scalar, 10.0d0, EPSILON, "clamp_real (above max)")
        
        ! Test clamp (integer)
        result_int = clamp_int(5, 0, 10)
        call assert_true(result_int == 5, "clamp_int (within range)")
        
        ! Test lerp
        result_scalar = lerp(0.0d0, 10.0d0, 0.5d0)
        call assert_approx_equal(result_scalar, 5.0d0, EPSILON, "lerp")
        
        ! Test smoothstep
        result_scalar = smoothstep(0.0d0, 1.0d0, 0.5d0)
        call assert_approx_equal(result_scalar, 0.5d0, 0.01d0, "smoothstep")
        
        ! Test approx_equal
        call assert_true(approx_equal(1.0d0, 1.0000001d0), "approx_equal (close)")
        call assert_true(.not. approx_equal(1.0d0, 2.0d0), "approx_equal (different)")
        
        ! Test power of two
        call assert_true(is_power_of_two(1), "is_power_of_two (1)")
        call assert_true(is_power_of_two(2), "is_power_of_two (2)")
        call assert_true(is_power_of_two(8), "is_power_of_two (8)")
        call assert_true(.not. is_power_of_two(3), "is_power_of_two (3)")
        call assert_true(.not. is_power_of_two(0), "is_power_of_two (0)")
        
        ! Test next power of two
        result_int = next_power_of_two(5)
        call assert_true(result_int == 8, "next_power_of_two (5 -> 8)")
        result_int = next_power_of_two(16)
        call assert_true(result_int == 16, "next_power_of_two (16 -> 16)")
        
        ! Test linspace
        arr = linspace_real(0.0d0, 10.0d0, 5)
        call assert_true(size(arr) == 5, "linspace_real size")
        call assert_approx_equal(arr(1), 0.0d0, EPSILON, "linspace_real first")
        call assert_approx_equal(arr(5), 10.0d0, EPSILON, "linspace_real last")
        
        ! Test map_range
        result_scalar = map_range(5.0d0, 0.0d0, 10.0d0, 0.0d0, 100.0d0)
        call assert_approx_equal(result_scalar, 50.0d0, EPSILON, "map_range")
    end subroutine test_numerical_utilities
    
    subroutine test_trigonometric_helpers()
        real(8) :: result_scalar
        
        print *, ""
        print *, "--- Trigonometric Helpers Tests ---"
        
        ! Test to_radians
        result_scalar = to_radians(180.0d0)
        call assert_approx_equal(result_scalar, PI, EPSILON, "to_radians")
        
        ! Test to_degrees
        result_scalar = to_degrees(PI)
        call assert_approx_equal(result_scalar, 180.0d0, EPSILON, "to_degrees")
        
        ! Test wrap_angle
        result_scalar = wrap_angle(3.0d0 * PI)
        call assert_approx_equal(result_scalar, PI, EPSILON, "wrap_angle")
        
        ! Test wrap_angle_signed
        result_scalar = wrap_angle_signed(3.0d0 * PI / 2.0d0)
        call assert_approx_equal(result_scalar, -PI / 2.0d0, EPSILON, "wrap_angle_signed")
    end subroutine test_trigonometric_helpers
    
    subroutine test_interpolation()
        real(8) :: x(5), y(5)
        real(8) :: result_scalar
        
        print *, ""
        print *, "--- Interpolation Tests ---"
        
        ! Setup test data
        x = [0.0d0, 1.0d0, 2.0d0, 3.0d0, 4.0d0]
        y = [0.0d0, 2.0d0, 4.0d0, 6.0d0, 8.0d0]
        
        ! Test interpolation at known point
        result_scalar = interp_linear_real(x, y, 2.0d0)
        call assert_approx_equal(result_scalar, 4.0d0, EPSILON, "interp_linear (known point)")
        
        ! Test interpolation between points
        result_scalar = interp_linear_real(x, y, 1.5d0)
        call assert_approx_equal(result_scalar, 3.0d0, EPSILON, "interp_linear (between points)")
        
        ! Test extrapolation (below)
        result_scalar = interp_linear_real(x, y, -1.0d0)
        call assert_approx_equal(result_scalar, 0.0d0, EPSILON, "interp_linear (below range)")
        
        ! Test extrapolation (above)
        result_scalar = interp_linear_real(x, y, 5.0d0)
        call assert_approx_equal(result_scalar, 8.0d0, EPSILON, "interp_linear (above range)")
    end subroutine test_interpolation
    
    subroutine test_matrix_operations()
        real(8) :: a(2, 2), b(2, 2)
        real(8), allocatable :: result_mat(:,:)
        real(8) :: result_scalar
        
        print *, ""
        print *, "--- Matrix Operations Tests ---"
        
        ! Test matrix multiply
        a = reshape([1.0d0, 2.0d0, 3.0d0, 4.0d0], [2, 2])
        b = reshape([5.0d0, 6.0d0, 7.0d0, 8.0d0], [2, 2])
        result_mat = matrix_multiply(a, b)
        call assert_true(size(result_mat, 1) == 2 .and. size(result_mat, 2) == 2, &
                        "matrix_multiply dimensions")
        call assert_approx_equal(result_mat(1, 1), 19.0d0, EPSILON, "matrix_multiply (1,1)")
        call assert_approx_equal(result_mat(2, 2), 50.0d0, EPSILON, "matrix_multiply (2,2)")
        
        ! Test matrix transpose
        a = reshape([1.0d0, 2.0d0, 3.0d0, 4.0d0], [2, 2])
        result_mat = matrix_transpose(a)
        call assert_approx_equal(result_mat(1, 2), 2.0d0, EPSILON, "matrix_transpose")
        
        ! Test determinant (2x2)
        a = reshape([4.0d0, 3.0d0, 6.0d0, 8.0d0], [2, 2])
        result_scalar = matrix_determinant(a)
        call assert_approx_equal(result_scalar, 14.0d0, EPSILON, "matrix_determinant (2x2)")
        
        ! Test determinant (3x3)
        a = reshape([1.0d0, 2.0d0, 3.0d0, 0.0d0, 1.0d0, 4.0d0, 5.0d0, 6.0d0, 0.0d0], [3, 3])
        result_scalar = matrix_determinant(a)
        call assert_approx_equal(result_scalar, 1.0d0, EPSILON, "matrix_determinant (3x3)")
        
        ! Test identity matrix
        result_mat = identity_matrix(3)
        call assert_true(size(result_mat, 1) == 3 .and. size(result_mat, 2) == 3, &
                        "identity_matrix dimensions")
        call assert_approx_equal(result_mat(1, 1), 1.0d0, EPSILON, "identity_matrix diagonal")
        call assert_approx_equal(result_mat(1, 2), 0.0d0, EPSILON, "identity_matrix off-diagonal")
    end subroutine test_matrix_operations

end program math_utils_test