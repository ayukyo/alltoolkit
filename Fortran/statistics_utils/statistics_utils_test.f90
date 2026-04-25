! =============================================================================
! Statistics Utilities Test Suite
! =============================================================================
! Comprehensive tests for statistics_utils module

program statistics_utils_test
    use statistics_utils
    implicit none
    
    integer :: tests_passed, tests_failed
    
    tests_passed = 0
    tests_failed = 0
    
    print *, "=============================================="
    print *, "Statistics Utilities Test Suite"
    print *, "=============================================="
    print *, ""
    
    ! Run all test suites
    call test_basic_statistics()
    call test_percentiles()
    call test_shape_measures()
    call test_correlation()
    call test_regression()
    call test_moving_statistics()
    call test_histogram()
    call test_normalization()
    call test_distributions()
    
    print *, ""
    print *, "=============================================="
    print '(A, I0, A, I0, A)', " Results: ", tests_passed, " passed, ", tests_failed, " failed"
    print *, "=============================================="
    
    if (tests_failed > 0) then
        print *, "SOME TESTS FAILED!"
        stop 1
    else
        print *, "ALL TESTS PASSED!"
    end if

contains

    subroutine assert_true(condition, test_name)
        logical, intent(in) :: condition
        character(*), intent(in) :: test_name
        
        if (condition) then
            tests_passed = tests_passed + 1
            print '(A, A)', "  PASS: ", test_name
        else
            tests_failed = tests_failed + 1
            print '(A, A)', "  FAIL: ", test_name
        end if
    end subroutine assert_true
    
    subroutine assert_near(a, b, tolerance, test_name)
        real(8), intent(in) :: a, b, tolerance
        character(*), intent(in) :: test_name
        
        call assert_true(abs(a - b) < tolerance, test_name)
    end subroutine assert_near

    subroutine test_basic_statistics()
        real(8) :: data1(10), data3(3), data4(4), data7(7), data8(8), data5(5)
        real(8) :: result
        
        print *, ""
        print *, "--- Basic Statistics ---"
        
        ! Mean test
        data1 = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0, 6.0d0, 7.0d0, 8.0d0, 9.0d0, 10.0d0/)
        result = mean(data1)
        call assert_near(result, 5.5d0, 1.0d-10, "mean() calculates correct average")
        
        ! Geometric mean test
        result = geometric_mean(data1)
        call assert_near(result, 4.5287d0, 1.0d-4, "geometric_mean() calculates correctly")
        
        ! Harmonic mean test
        result = harmonic_mean(data1)
        call assert_near(result, 3.414d0, 1.0d-3, "harmonic_mean() calculates correctly")
        
        ! Median test (odd count)
        data3 = (/1.0d0, 3.0d0, 5.0d0/)
        result = median(data3)
        call assert_near(result, 3.0d0, 1.0d-10, "median() handles odd count")
        
        ! Median test (even count)
        data4 = (/1.0d0, 2.0d0, 3.0d0, 4.0d0/)
        result = median(data4)
        call assert_near(result, 2.5d0, 1.0d-10, "median() handles even count")
        
        ! Mode test
        data7 = (/1.0d0, 2.0d0, 2.0d0, 3.0d0, 3.0d0, 3.0d0, 4.0d0/)
        result = mode(data7)
        call assert_near(result, 3.0d0, 1.0d-10, "mode() finds most frequent value")
        
        ! Variance test (sample)
        data8 = (/2.0d0, 4.0d0, 4.0d0, 4.0d0, 5.0d0, 5.0d0, 7.0d0, 9.0d0/)
        result = variance(data8)
        call assert_near(result, 4.5714d0, 1.0d-4, "variance() calculates sample variance")
        
        ! Variance test (population)
        result = variance_pop(data8)
        call assert_near(result, 4.0d0, 1.0d-10, "variance_pop() calculates population variance")
        
        ! Standard deviation test
        result = std_dev(data8)
        call assert_near(result, 2.138d0, 1.0d-3, "std_dev() calculates correctly")
        
        ! Range test
        data5 = (/3.0d0, 7.0d0, 2.0d0, 9.0d0, 5.0d0/)
        result = range_val(data5)
        call assert_near(result, 7.0d0, 1.0d-10, "range_val() calculates max - min")
        
        ! Coefficient of variation test
        data3 = (/10.0d0, 20.0d0, 30.0d0/)
        result = coefficient_of_variation(data3)
        call assert_near(result, 50.0d0, 1.0d-6, "coefficient_of_variation() calculates correctly")
    end subroutine test_basic_statistics

    subroutine test_percentiles()
        real(8) :: data20(20)
        real(8) :: result, q1, q2, q3
        
        print *, ""
        print *, "--- Percentiles ---"
        
        data20 = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0, 6.0d0, 7.0d0, 8.0d0, 9.0d0, 10.0d0, &
                 11.0d0, 12.0d0, 13.0d0, 14.0d0, 15.0d0, 16.0d0, 17.0d0, 18.0d0, 19.0d0, 20.0d0/)
        
        result = percentile(data20, 0.0d0)
        call assert_near(result, 1.0d0, 1.0d-10, "percentile(0) returns minimum")
        
        result = percentile(data20, 50.0d0)
        call assert_near(result, 10.5d0, 0.1d0, "percentile(50) returns median")
        
        result = percentile(data20, 100.0d0)
        call assert_near(result, 20.0d0, 1.0d-10, "percentile(100) returns maximum")
        
        call quartiles(data20, q1, q2, q3)
        call assert_near(q1, percentile(data20, 25.0d0), 0.1d0, "quartiles() Q1 matches percentile(25)")
        call assert_near(q2, percentile(data20, 50.0d0), 0.1d0, "quartiles() Q2 matches percentile(50)")
        
        result = iqr(data20)
        call assert_near(result, q3 - q1, 1.0d-10, "iqr() returns Q3 - Q1")
    end subroutine test_percentiles

    subroutine test_shape_measures()
        real(8) :: data7a(7), data7b(7), data10(10)
        real(8) :: result
        
        print *, ""
        print *, "--- Shape Measures ---"
        
        data7a = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0, 6.0d0, 20.0d0/)
        result = skewness(data7a)
        call assert_true(result > 1.0d0, "skewness() detects positive skew")
        
        data7b = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0, 6.0d0, 7.0d0/)
        result = skewness(data7b)
        call assert_true(abs(result) < 0.5d0, "skewness() detects symmetry")
        
        data10 = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0, 6.0d0, 7.0d0, 8.0d0, 9.0d0, 10.0d0/)
        result = kurtosis(data10)
        call assert_true(abs(result) < 1.5d0, "kurtosis() near zero for normal distribution")
    end subroutine test_shape_measures

    subroutine test_correlation()
        real(8) :: x10(10), y10(10), x5(5), y5(5)
        real(8) :: result
        
        print *, ""
        print *, "--- Correlation ---"
        
        x10 = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0, 6.0d0, 7.0d0, 8.0d0, 9.0d0, 10.0d0/)
        y10 = (/2.0d0, 4.0d0, 6.0d0, 8.0d0, 10.0d0, 12.0d0, 14.0d0, 16.0d0, 18.0d0, 20.0d0/)
        result = pearson_correlation(x10, y10)
        call assert_near(result, 1.0d0, 1.0d-6, "pearson_correlation() perfect positive")
        
        y10 = (/20.0d0, 18.0d0, 16.0d0, 14.0d0, 12.0d0, 10.0d0, 8.0d0, 6.0d0, 4.0d0, 2.0d0/)
        result = pearson_correlation(x10, y10)
        call assert_near(result, -1.0d0, 1.0d-6, "pearson_correlation() perfect negative")
        
        x5 = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0/)
        y5 = (/2.0d0, 4.0d0, 6.0d0, 8.0d0, 10.0d0/)
        result = covariance(x5, y5)
        call assert_true(result > 0.0d0, "covariance() positive for positive relationship")
        
        y5 = (/5.0d0, 4.0d0, 3.0d0, 2.0d0, 1.0d0/)
        result = spearman_correlation(x5, y5)
        call assert_near(result, -1.0d0, 1.0d-6, "spearman_correlation() perfect negative rank")
    end subroutine test_correlation

    subroutine test_regression()
        real(8) :: x5(5), y5(5)
        real(8) :: slope, intercept, r_sq
        
        print *, ""
        print *, "--- Linear Regression ---"
        
        x5 = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0/)
        y5 = (/3.0d0, 5.0d0, 7.0d0, 9.0d0, 11.0d0/)
        
        call linear_regression(x5, y5, slope, intercept, r_sq)
        call assert_near(slope, 2.0d0, 1.0d-6, "linear_regression() slope correct")
        call assert_near(intercept, 1.0d0, 1.0d-6, "linear_regression() intercept correct")
        call assert_near(r_sq, 1.0d0, 1.0d-6, "linear_regression() R-squared = 1 for perfect fit")
        
        y5 = (/2.1d0, 3.9d0, 6.2d0, 7.8d0, 10.1d0/)
        call linear_regression(x5, y5, slope, intercept, r_sq)
        call assert_true(slope > 1.5d0 .and. slope < 2.5d0, "linear_regression() handles noisy data")
        call assert_true(r_sq > 0.95d0, "linear_regression() high R-squared for near-linear data")
    end subroutine test_regression

    subroutine test_moving_statistics()
        real(8) :: data10(10)
        real(8), allocatable :: ma(:), ms(:)
        
        print *, ""
        print *, "--- Moving Statistics ---"
        
        data10 = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0, 6.0d0, 7.0d0, 8.0d0, 9.0d0, 10.0d0/)
        
        ma = moving_mean(data10, 3)
        call assert_near(ma(1), 1.0d0, 1.0d-6, "moving_mean() first value")
        call assert_near(ma(3), 2.0d0, 1.0d-6, "moving_mean() third value (first full window)")
        call assert_near(ma(10), 9.0d0, 1.0d-6, "moving_mean() last value")
        
        ms = moving_std(data10, 3)
        call assert_true(ms(3) > 0.0d0, "moving_std() calculates standard deviation")
        
        deallocate(ma, ms)
    end subroutine test_moving_statistics

    subroutine test_histogram()
        real(8) :: data20(20)
        integer, allocatable :: counts(:)
        real(8), allocatable :: edges(:)
        
        print *, ""
        print *, "--- Histogram ---"
        
        data20 = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0, 6.0d0, 7.0d0, 8.0d0, 9.0d0, 10.0d0, &
                 11.0d0, 12.0d0, 13.0d0, 14.0d0, 15.0d0, 16.0d0, 17.0d0, 18.0d0, 19.0d0, 20.0d0/)
        
        call histogram(data20, 4, counts, edges)
        call assert_true(size(counts) == 4, "histogram() correct number of bins")
        call assert_true(size(edges) == 5, "histogram() correct number of edges")
        call assert_true(sum(counts) == 20, "histogram() all points counted")
        call assert_true(edges(1) == 1.0d0, "histogram() first edge is min")
        call assert_true(edges(5) == 20.0d0, "histogram() last edge is max")
        
        deallocate(counts, edges)
    end subroutine test_histogram

    subroutine test_normalization()
        real(8) :: data5a(5), data5b(5)
        real(8) :: result
        real(8), allocatable :: normed(:)
        real(8) :: lower, upper
        
        print *, ""
        print *, "--- Normalization ---"
        
        data5a = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0/)
        result = z_score(3.0d0, data5a)
        call assert_near(result, 0.0d0, 1.0d-6, "z_score() of mean is zero")
        
        result = z_score(5.0d0, data5a)
        call assert_near(result, 1.26d0, 0.02d0, "z_score() correct for positive deviation")
        
        data5b = (/2.0d0, 4.0d0, 6.0d0, 8.0d0, 10.0d0/)
        normed = normalize(data5b)
        call assert_near(normed(1), 0.0d0, 1.0d-6, "normalize() min becomes 0")
        call assert_near(normed(5), 1.0d0, 1.0d-6, "normalize() max becomes 1")
        call assert_near(normed(3), 0.5d0, 1.0d-6, "normalize() middle becomes 0.5")
        
        deallocate(normed)
        
        result = standard_error(data5b)
        call assert_true(result > 0.0d0, "standard_error() positive")
        
        call confidence_interval(data5b, 0.95d0, lower, upper)
        call assert_true(lower < upper, "confidence_interval() lower < upper")
        call assert_true(lower < 6.0d0, "confidence_interval() lower below mean")
        call assert_true(upper > 6.0d0, "confidence_interval() upper above mean")
    end subroutine test_normalization

    subroutine test_distributions()
        real(8) :: result
        
        print *, ""
        print *, "--- Probability Distributions ---"
        
        result = normal_pdf(0.0d0, 0.0d0, 1.0d0)
        call assert_near(result, 0.3989d0, 1.0d-4, "normal_pdf(0, 0, 1) correct")
        
        result = normal_cdf(0.0d0, 0.0d0, 1.0d0)
        call assert_near(result, 0.5d0, 0.01d0, "normal_cdf(0, 0, 1) = 0.5")
        
        result = normal_cdf(1.96d0, 0.0d0, 1.0d0)
        call assert_near(result, 0.975d0, 0.02d0, "normal_cdf(1.96, 0, 1) approx 0.975")
    end subroutine test_distributions

end program statistics_utils_test