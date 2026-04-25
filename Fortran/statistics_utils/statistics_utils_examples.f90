! =============================================================================
! Statistics Utilities Examples
! =============================================================================
! Demonstrates usage of statistics_utils module

program statistics_utils_examples
    use statistics_utils
    implicit none
    
    real(8) :: data(10), data2(10)
    real(8) :: x(5), y(5)
    real(8), allocatable :: ma(:), ms(:), normed(:)
    integer, allocatable :: counts(:)
    real(8), allocatable :: edges(:)
    real(8) :: result, q1, q2, q3, slope, intercept, r_sq
    real(8) :: lower, upper
    integer :: i
    
    print *, "=============================================="
    print *, "Statistics Utilities Examples"
    print *, "=============================================="
    
    ! Example data
    data = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0, 6.0d0, 7.0d0, 8.0d0, 9.0d0, 10.0d0/)
    
    ! =========================================================================
    ! Example 1: Basic Statistics
    ! =========================================================================
    print *, ""
    print *, "--- Example 1: Basic Statistics ---"
    print '(A, F6.2)', "  Mean: ", mean(data)
    print '(A, F6.4)', "  Geometric Mean: ", geometric_mean(data)
    print '(A, F6.4)', "  Harmonic Mean: ", harmonic_mean(data)
    print '(A, F6.2)', "  Median: ", median(data)
    print '(A, F6.2)', "  Mode: ", mode(data)
    print '(A, F6.4)', "  Sample Variance: ", variance(data)
    print '(A, F6.4)', "  Population Variance: ", variance_pop(data)
    print '(A, F6.4)', "  Standard Deviation: ", std_dev(data)
    print '(A, F6.2)', "  Range: ", range_val(data)
    print '(A, F6.2)', "  Coefficient of Variation: ", coefficient_of_variation(data)
    
    ! =========================================================================
    ! Example 2: Percentiles and Quartiles
    ! =========================================================================
    print *, ""
    print *, "--- Example 2: Percentiles and Quartiles ---"
    print '(A, F6.2)', "  25th percentile (Q1): ", percentile(data, 25.0d0)
    print '(A, F6.2)', "  50th percentile (median): ", percentile(data, 50.0d0)
    print '(A, F6.2)', "  75th percentile (Q3): ", percentile(data, 75.0d0)
    
    call quartiles(data, q1, q2, q3)
    print '(A, F6.2, A, F6.2, A, F6.2)', "  Quartiles: Q1=", q1, ", Q2=", q2, ", Q3=", q3
    print '(A, F6.2)', "  IQR: ", iqr(data)
    
    ! =========================================================================
    ! Example 3: Shape Measures
    ! =========================================================================
    print *, ""
    print *, "--- Example 3: Shape Measures ---"
    
    ! Positive skew data
    data2 = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0, 6.0d0, 7.0d0, 8.0d0, 9.0d0, 100.0d0/)
    print '(A, F6.4)', "  Skewness (positive): ", skewness(data2)
    print '(A, F6.4)', "  Kurtosis: ", kurtosis(data)
    
    ! =========================================================================
    ! Example 4: Correlation Analysis
    ! =========================================================================
    print *, ""
    print *, "--- Example 4: Correlation Analysis ---"
    
    x = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0/)
    y = (/2.1d0, 4.0d0, 5.9d0, 8.1d0, 10.0d0/)
    
    print '(A, F6.4)', "  Covariance: ", covariance(x, y)
    print '(A, F6.4)', "  Pearson Correlation: ", pearson_correlation(x, y)
    print '(A, F6.4)', "  Spearman Correlation: ", spearman_correlation(x, y)
    
    ! =========================================================================
    ! Example 5: Linear Regression
    ! =========================================================================
    print *, ""
    print *, "--- Example 5: Linear Regression ---"
    
    call linear_regression(x, y, slope, intercept, r_sq)
    print '(A, F6.4)', "  Slope: ", slope
    print '(A, F6.4)', "  Intercept: ", intercept
    print '(A, F6.4)', "  R-squared: ", r_sq
    print '(A)', "  Equation: y = 2x + 0 (approximately)"
    
    ! =========================================================================
    ! Example 6: Moving Statistics
    ! =========================================================================
    print *, ""
    print *, "--- Example 6: Moving Statistics ---"
    
    data = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0, 6.0d0, 7.0d0, 8.0d0, 9.0d0, 10.0d0/)
    ma = moving_mean(data, 3)
    
    print '(A)', "  Moving Average (window=3):"
    do i = 1, 10
        print '(A, I3, A, F6.2)', "    position ", i, ": ", ma(i)
    end do
    
    deallocate(ma, ms)
    
    ! =========================================================================
    ! Example 7: Histogram
    ! =========================================================================
    print *, ""
    print *, "--- Example 7: Histogram ---"
    
    ! Generate random-ish data
    data = (/5.1d0, 5.3d0, 5.5d0, 10.2d0, 10.5d0, 15.1d0, 15.3d0, 20.0d0, 20.1d0, 25.0d0/)
    call histogram(data, 5, counts, edges)
    
    print '(A)', "  Histogram bins:"
    do i = 1, size(counts)
        print '(A, F6.2, A, F6.2, A, I3)', "    [", edges(i), " - ", edges(i+1), "]: ", counts(i)
    end do
    
    deallocate(counts, edges)
    
    ! =========================================================================
    ! Example 8: Normalization
    ! =========================================================================
    print *, ""
    print *, "--- Example 8: Normalization ---"
    
    data = (/10.0d0, 20.0d0, 30.0d0, 40.0d0, 50.0d0/)
    normed = normalize(data)
    
    print '(A)', "  Original data: 10, 20, 30, 40, 50"
    print '(A)', "  Normalized to [0, 1]:"
    do i = 1, 5
        print '(A, I3, A, F6.4)', "    ", i, ": ", normed(i)
    end do
    
    print '(A, F6.4)', "  Z-score of 30 (mean): ", z_score(30.0d0, data)
    print '(A, F6.4)', "  Z-score of 50 (max): ", z_score(50.0d0, data)
    
    deallocate(normed)
    
    ! =========================================================================
    ! Example 9: Confidence Interval
    ! =========================================================================
    print *, ""
    print *, "--- Example 9: Confidence Interval ---"
    
    data = (/100.0d0, 102.0d0, 98.0d0, 101.0d0, 99.0d0, 103.0d0, 97.0d0, 100.0d0, 99.0d0, 101.0d0/)
    call confidence_interval(data, 0.95d0, lower, upper)
    
    print '(A, F6.2)', "  Mean: ", mean(data)
    print '(A, F6.4)', "  Standard Error: ", standard_error(data)
    print '(A, F6.2, A, F6.2)', "  95% Confidence Interval: [", lower, ", ", upper, "]"
    
    ! =========================================================================
    ! Example 10: Probability Distributions
    ! =========================================================================
    print *, ""
    print *, "--- Example 10: Probability Distributions ---"
    
    print '(A)', "  Normal Distribution (mu=0, sigma=1):"
    print '(A, F6.6)', "    PDF at x=0: ", normal_pdf(0.0d0, 0.0d0, 1.0d0)
    print '(A, F6.4)', "    CDF at x=0: ", normal_cdf(0.0d0, 0.0d0, 1.0d0)
    print '(A, F6.4)', "    CDF at x=1.96: ", normal_cdf(1.96d0, 0.0d0, 1.0d0)
    
    print *, ""
    print *, "=============================================="
    print *, "Examples completed successfully!"
    print *, "=============================================="

end program statistics_utils_examples