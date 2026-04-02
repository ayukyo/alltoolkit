!! AllToolkit - Fortran Math Utilities Example
!! Demonstrates usage of math_utils module
!!
!! Compile and run:
!!   gfortran -o math_example ../math_utils/mod.f90 math_utils_example.f90 && ./math_example

program math_utils_example
    use math_utils
    implicit none
    
    print *, "========================================"
    print *, "Fortran Math Utilities - Examples"
    print *, "========================================"
    
    call demonstrate_vector_operations()
    call demonstrate_statistics()
    call demonstrate_numerical_utilities()
    call demonstrate_trigonometry()
    call demonstrate_interpolation()
    call demonstrate_matrices()
    
    print *, ""
    print *, "========================================"
    print *, "All examples completed successfully!"
    print *, "========================================"
    
contains

    subroutine demonstrate_vector_operations()
        real(8) :: v1(3), v2(3), v3(3), v_result(3)
        real(8) :: scalar_result
        
        print *, ""
        print *, "--- Vector Operations ---"
        
        ! Define vectors
        v1 = [1.0d0, 2.0d0, 3.0d0]
        v2 = [4.0d0, 5.0d0, 6.0d0]
        
        print *, "Vector v1: ", v1
        print *, "Vector v2: ", v2
        
        ! Dot product
        scalar_result = dot_product_real(v1, v2)
        print *, "Dot product: ", scalar_result
        
        ! Cross product
        v_result = cross_product(v1, v2)
        print *, "Cross product: ", v_result
        
        ! Magnitude
        scalar_result = vector_magnitude(v1)
        print *, "Magnitude of v1: ", scalar_result
        
        ! Normalize
        v_result = normalize_vector(v1)
        print *, "Normalized v1: ", v_result
        print *, "Magnitude of normalized: ", vector_magnitude(v_result)
        
        ! Angle between vectors
        scalar_result = vector_angle(v1, v2)
        print *, "Angle between v1 and v2 (radians): ", scalar_result
        print *, "Angle between v1 and v2 (degrees): ", to_degrees(scalar_result)
        
        ! Distance
        scalar_result = euclidean_distance(v1, v2)
        print *, "Euclidean distance: ", scalar_result
    end subroutine demonstrate_vector_operations
    
    subroutine demonstrate_statistics()
        real(8) :: data_real(8)
        integer :: data_int(5)
        real(8) :: result
        real(8), allocatable :: linspace_arr(:)
        
        print *, ""
        print *, "--- Statistical Functions ---"
        
        ! Real array statistics
        data_real = [2.0d0, 4.0d0, 4.0d0, 4.0d0, 5.0d0, 5.0d0, 7.0d0, 9.0d0]
        print *, "Data: ", data_real
        print *, "Count: ", size(data_real)
        
        result = mean_real(data_real)
        print *, "Mean: ", result
        
        result = median_real(data_real)
        print *, "Median: ", result
        
        result = variance_real(data_real, .false.)  ! Population variance
        print *, "Variance (population): ", result
        
        result = variance_real(data_real, .true.)   ! Sample variance
        print *, "Variance (sample): ", result
        
        result = std_dev_real(data_real, .false.)
        print *, "Std Dev (population): ", result
        
        result = min_value(data_real)
        print *, "Min: ", result
        
        result = max_value(data_real)
        print *, "Max: ", result
        
        ! Integer array
        data_int = [10, 20, 30, 40, 50]
        print *, ""
        print *, "Integer data: ", data_int
        result = mean_int(data_int)
        print *, "Mean of integers: ", result
        
        ! Generate linearly spaced array
        print *, ""
        print *, "Linspace from 0 to 100 (11 points):"
        linspace_arr = linspace_real(0.0d0, 100.0d0, 11)
        print *, linspace_arr
    end subroutine demonstrate_statistics
    
    subroutine demonstrate_numerical_utilities()
        real(8) :: value, result
        integer :: int_result
        real(8), allocatable :: spaced(:)
        
        print *, ""
        print *, "--- Numerical Utilities ---"
        
        ! Clamp examples
        value = 15.0d0
        result = clamp_real(value, 0.0d0, 10.0d0)
        print *, "Clamp 15 to [0, 10]: ", result
        
        value = -5.0d0
        result = clamp_real(value, 0.0d0, 10.0d0)
        print *, "Clamp -5 to [0, 10]: ", result
        
        ! Lerp examples
        print *, ""
        print *, "Linear interpolation (lerp):"
        result = lerp(0.0d0, 100.0d0, 0.0d0)
        print *, "lerp(0, 100, 0.0): ", result
        result = lerp(0.0d0, 100.0d0, 0.5d0)
        print *, "lerp(0, 100, 0.5): ", result
        result = lerp(0.0d0, 100.0d0, 1.0d0)
        print *, "lerp(0, 100, 1.0): ", result
        
        ! Smoothstep
        print *, ""
        print *, "Smoothstep interpolation:"
        result = smoothstep(0.0d0, 1.0d0, 0.0d0)
        print *, "smoothstep(0, 1, 0.0): ", result
        result = smoothstep(0.0d0, 1.0d0, 0.5d0)
        print *, "smoothstep(0, 1, 0.5): ", result
        result = smoothstep(0.0d0, 1.0d0, 1.0d0)
        print *, "smoothstep(0, 1, 1.0): ", result
        
        ! Approximate equality
        print *, ""
        print *, "Approximate equality:"
        print *, "approx_equal(1.0, 1.000001): ", approx_equal(1.0d0, 1.000001d0)
        print *, "approx_equal(1.0, 1.1): ", approx_equal(1.0d0, 1.1d0)
        
        ! Power of two
        print *, ""
        print *, "Power of two functions:"
        print *, "is_power_of_two(1): ", is_power_of_two(1)
        print *, "is_power_of_two(8): ", is_power_of_two(8)
        print *, "is_power_of_two(10): ", is_power_of_two(10)
        int_result = next_power_of_two(5)
        print *, "next_power_of_two(5): ", int_result
        int_result = next_power_of_two(16)
        print *, "next_power_of_two(16): ", int_result
        
        ! Map range
        print *, ""
        print *, "Map range:"
        result = map_range(50.0d0, 0.0d0, 100.0d0, 0.0d0, 1.0d0)
        print *, "map_range(50, 0-100, 0-1): ", result
        result = map_range(0.5d0, 0.0d0, 1.0d0, 0.0d0, 255.0d0)
        print *, "map_range(0.5, 0-1, 0-255): ", result
    end subroutine demonstrate_numerical_utilities
    
    subroutine demonstrate_trigonometry()
        real(8) :: angle_deg, angle_rad, result
        
        print *, ""
        print *, "--- Trigonometric Helpers ---"
        
        ! Degrees to radians
        angle_deg = 180.0d0
        angle_rad = to_radians(angle_deg)
        print *, angle_deg, " degrees = ", angle_rad, " radians"
        
        ! Radians to degrees
        angle_rad = PI / 4.0d0
        angle_deg = to_degrees(angle_rad)
        print *, angle_rad, " radians = ", angle_deg, " degrees"
        
        ! Wrap angle
        print *, ""
        print *, "Angle wrapping:"
        result = wrap_angle(3.0d0 * PI)
        print *, "wrap_angle(3*PI): ", result, " (should be PI)"
        result = wrap_angle_signed(3.0d0 * PI / 2.0d0)
        print *, "wrap_angle_signed(3*PI/2): ", result, " (should be -PI/2)"
    end subroutine demonstrate_trigonometry
    
    subroutine demonstrate_interpolation()
        real(8) :: x(5), y(5)
        real(8) :: xi, yi
        integer :: i
        
        print *, ""
        print *, "--- Linear Interpolation ---"
        
        ! Sample data points
        x = [0.0d0, 1.0d0, 2.0d0, 3.0d0, 4.0d0]
        y = [0.0d0, 1.0d0, 4.0d0, 9.0d0, 16.0d0]
        
        print *, "Data points (x, y):"
        do i = 1, 5
            print *, "  (", x(i), ", ", y(i), ")"
        end do
        
        !
        ! Interpolate at various points
        print *, ""
        print *, "Interpolated values:"
        xi = 0.5d0
        yi = interp_linear_real(x, y, xi)
        print *, "  At x = ", xi, ", y = ", yi
        
        xi = 1.5d0
        yi = interp_linear_real(x, y, xi)
        print *, "  At x = ", xi, ", y = ", yi
        
        xi = 2.5d0
        yi = interp_linear_real(x, y, xi)
        print *, "  At x = ", xi, ", y = ", yi
        
        xi = 3.5d0
        yi = interp_linear_real(x, y, xi)
        print *, "  At x = ", xi, ", y = ", yi
    end subroutine demonstrate_interpolation
    
    subroutine demonstrate_matrices()
        real(8) :: a(2, 2), b(2, 2), c(3, 3)
        real(8), allocatable :: result(:,:)
        real(8) :: det
        
        print *, ""
        print *, "--- Matrix Operations ---"
        
        ! Define matrices
        a = reshape([1.0d0, 2.0d0, 3.0d0, 4.0d0], [2, 2])
        b = reshape([5.0d0, 6.0d0, 7.0d0, 8.0d0], [2, 2])
        
        print *, "Matrix A:"
        call print_matrix(a)
        
        print *, "Matrix B:"
        call print_matrix(b)
        
        ! Matrix multiplication
        result = matrix_multiply(a, b)
        print *, "A * B:"
        call print_matrix(result)
        
        ! Transpose
        result = matrix_transpose(a)
        print *, "Transpose of A:"
        call print_matrix(result)
        
        ! Determinant (2x2)
        det = matrix_determinant(a)
        print *, "Determinant of A: ", det
        
        ! Determinant (3x3)
        c = reshape([1.0d0, 0.0d0, 0.0d0, &
                     0.0d0, 2.0d0, 0.0d0, &
                     0.0d0, 0.0d0, 3.0d0], [3, 3])
        print *, ""
        print *, "Matrix C (diagonal):"
        call print_matrix(c)
        det = matrix_determinant(c)
        print *, "Determinant of C: ", det, " (should be 6)"
        
        ! Identity matrix
        result = identity_matrix(4)
        print *, ""
        print *, "4x4 Identity matrix:"
        call print_matrix(result)
    end subroutine demonstrate_matrices
    
    subroutine print_matrix(mat)
        real(8), intent(in) :: mat(:,:)
        integer :: i, j
        do i = 1, size(mat, 1)
            write(*, '(A)', advance='no') "  ["
            do j = 1, size(mat, 2)
                write(*, '(F8.3, A)', advance='no') mat(i, j), " "
            end do
            print *, "]"
        end do
    end subroutine print_matrix

end program math_utils_example
