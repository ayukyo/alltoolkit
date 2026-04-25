! =============================================================================
! Statistics Utilities - Complete Statistics Module for Fortran
! =============================================================================
! A comprehensive statistics library with zero external dependencies.
! Supports descriptive statistics, distributions, and regression analysis.
!
! Features:
!   - Descriptive statistics (mean, median, mode, variance, std, etc.)
!   - Percentiles and quartiles
!   - Correlation coefficients (Pearson, Spearman)
!   - Linear regression
!   - Moving statistics (moving average, moving std)
!   - Histogram generation
!   - Normalization utilities
!
! Version: 1.0.0
! License: MIT
! =============================================================================

module statistics_utils
    implicit none
    private
    
    ! Public procedures
    public :: mean, median, mode, variance, variance_pop, std_dev, std_dev_pop
    public :: percentile, quartiles, iqr
    public :: skewness, kurtosis
    public :: covariance, pearson_correlation, spearman_correlation
    public :: linear_regression
    public :: moving_mean, moving_std
    public :: histogram
    public :: z_score, normalize
    public :: geometric_mean, harmonic_mean
    public :: range_val, coefficient_of_variation
    public :: standard_error, confidence_interval
    public :: normal_pdf, normal_cdf
    
    ! Constants
    real(8), parameter :: PI = 3.14159265358979323846d0
    
contains

    ! =========================================================================
    ! Basic Descriptive Statistics
    ! =========================================================================
    
    function mean(data) result(m)
        real(8), intent(in) :: data(:)
        real(8) :: m, sum_val
        integer :: n, i
        
        n = size(data)
        if (n == 0) then
            m = 0.0d0
            return
        end if
        
        sum_val = 0.0d0
        do i = 1, n
            sum_val = sum_val + data(i)
        end do
        m = sum_val / real(n, 8)
    end function mean
    
    function geometric_mean(data) result(gm)
        real(8), intent(in) :: data(:)
        real(8) :: gm, product_log
        integer :: i, n
        
        n = size(data)
        if (n == 0) then
            gm = 0.0d0
            return
        end if
        
        do i = 1, n
            if (data(i) <= 0.0d0) then
                gm = -1.0d0
                return
            end if
        end do
        
        product_log = 0.0d0
        do i = 1, n
            product_log = product_log + log(data(i))
        end do
        gm = exp(product_log / real(n, 8))
    end function geometric_mean
    
    function harmonic_mean(data) result(hm)
        real(8), intent(in) :: data(:)
        real(8) :: hm, sum_reciprocal
        integer :: i, n
        
        n = size(data)
        if (n == 0) then
            hm = 0.0d0
            return
        end if
        
        sum_reciprocal = 0.0d0
        do i = 1, n
            if (data(i) <= 0.0d0) then
                hm = -1.0d0
                return
            end if
            sum_reciprocal = sum_reciprocal + 1.0d0 / data(i)
        end do
        hm = real(n, 8) / sum_reciprocal
    end function harmonic_mean
    
    function median(data) result(m)
        real(8), intent(in) :: data(:)
        real(8) :: m
        real(8), allocatable :: sorted(:)
        integer :: n, mid
        
        n = size(data)
        if (n == 0) then
            m = 0.0d0
            return
        end if
        
        allocate(sorted(n))
        sorted = data
        call quick_sort(sorted)
        
        mid = n / 2
        if (mod(n, 2) == 0) then
            m = (sorted(mid) + sorted(mid + 1)) / 2.0d0
        else
            m = sorted(mid + 1)
        end if
        deallocate(sorted)
    end function median
    
    function mode(data) result(m)
        real(8), intent(in) :: data(:)
        real(8) :: m
        real(8), allocatable :: sorted(:)
        real(8) :: current_val, best_val
        integer :: i, n, current_count, best_count
        
        n = size(data)
        if (n == 0) then
            m = 0.0d0
            return
        end if
        
        allocate(sorted(n))
        sorted = data
        call quick_sort(sorted)
        
        best_val = sorted(1)
        best_count = 1
        current_val = sorted(1)
        current_count = 1
        
        do i = 2, n
            if (abs(sorted(i) - current_val) < 1.0d-10) then
                current_count = current_count + 1
            else
                if (current_count > best_count) then
                    best_count = current_count
                    best_val = current_val
                end if
                current_val = sorted(i)
                current_count = 1
            end if
        end do
        
        if (current_count > best_count) then
            best_val = current_val
        end if
        
        m = best_val
        deallocate(sorted)
    end function mode
    
    ! Sample variance
    function variance(data) result(v)
        real(8), intent(in) :: data(:)
        real(8) :: v, m, sum_val, diff_val
        integer :: n, i
        
        n = size(data)
        if (n < 2) then
            v = 0.0d0
            return
        end if
        
        m = mean(data)
        sum_val = 0.0d0
        do i = 1, n
            diff_val = data(i) - m
            sum_val = sum_val + diff_val * diff_val
        end do
        v = sum_val / real(n - 1, 8)
    end function variance
    
    ! Population variance
    function variance_pop(data) result(v)
        real(8), intent(in) :: data(:)
        real(8) :: v, m, sum_val, diff_val
        integer :: n, i
        
        n = size(data)
        if (n < 1) then
            v = 0.0d0
            return
        end if
        
        m = mean(data)
        sum_val = 0.0d0
        do i = 1, n
            diff_val = data(i) - m
            sum_val = sum_val + diff_val * diff_val
        end do
        v = sum_val / real(n, 8)
    end function variance_pop
    
    ! Sample standard deviation
    function std_dev(data) result(s)
        real(8), intent(in) :: data(:)
        real(8) :: s
        s = sqrt(variance(data))
    end function std_dev
    
    ! Population standard deviation
    function std_dev_pop(data) result(s)
        real(8), intent(in) :: data(:)
        real(8) :: s
        s = sqrt(variance_pop(data))
    end function std_dev_pop
    
    function range_val(data) result(r)
        real(8), intent(in) :: data(:)
        real(8) :: r
        
        if (size(data) == 0) then
            r = 0.0d0
            return
        end if
        r = maxval(data) - minval(data)
    end function range_val
    
    function coefficient_of_variation(data) result(cv)
        real(8), intent(in) :: data(:)
        real(8) :: cv, m, s
        
        m = mean(data)
        if (abs(m) < 1.0d-10) then
            cv = 0.0d0
            return
        end if
        s = std_dev(data)
        cv = (s / m) * 100.0d0
    end function coefficient_of_variation
    
    ! =========================================================================
    ! Percentiles and Quartiles
    ! =========================================================================
    
    function percentile(data, p) result(val)
        real(8), intent(in) :: data(:)
        real(8), intent(in) :: p
        real(8) :: val
        real(8), allocatable :: sorted(:)
        real(8) :: rank, frac
        integer :: n, lower, upper
        
        n = size(data)
        if (n == 0) then
            val = 0.0d0
            return
        end if
        
        allocate(sorted(n))
        sorted = data
        call quick_sort(sorted)
        
        if (p <= 0.0d0) then
            val = sorted(1)
        else if (p >= 100.0d0) then
            val = sorted(n)
        else
            rank = (p / 100.0d0) * real(n - 1, 8) + 1.0d0
            lower = int(rank)
            upper = lower + 1
            frac = rank - real(lower, 8)
            if (upper > n) then
                val = sorted(n)
            else
                val = sorted(lower) * (1.0d0 - frac) + sorted(upper) * frac
            end if
        end if
        deallocate(sorted)
    end function percentile
    
    subroutine quartiles(data, q1, q2, q3)
        real(8), intent(in) :: data(:)
        real(8), intent(out) :: q1, q2, q3
        
        q1 = percentile(data, 25.0d0)
        q2 = percentile(data, 50.0d0)
        q3 = percentile(data, 75.0d0)
    end subroutine quartiles
    
    function iqr(data) result(r)
        real(8), intent(in) :: data(:)
        real(8) :: r, q1, q2, q3
        
        call quartiles(data, q1, q2, q3)
        r = q3 - q1
    end function iqr
    
    ! =========================================================================
    ! Shape Measures
    ! =========================================================================
    
    function skewness(data) result(sk)
        real(8), intent(in) :: data(:)
        real(8) :: sk, m, s, n_val
        real(8) :: sum_val, diff_val
        integer :: n, i
        
        n = size(data)
        if (n < 3) then
            sk = 0.0d0
            return
        end if
        
        m = mean(data)
        s = std_dev(data)
        if (abs(s) < 1.0d-10) then
            sk = 0.0d0
            return
        end if
        
        sum_val = 0.0d0
        do i = 1, n
            diff_val = (data(i) - m) / s
            sum_val = sum_val + diff_val * diff_val * diff_val
        end do
        
        n_val = real(n, 8)
        sk = (n_val / ((n_val - 1.0d0) * (n_val - 2.0d0))) * sum_val
    end function skewness
    
    function kurtosis(data) result(ku)
        real(8), intent(in) :: data(:)
        real(8) :: ku, m, s, n_val
        real(8) :: sum_val, diff_val
        integer :: n, i
        
        n = size(data)
        if (n < 4) then
            ku = 0.0d0
            return
        end if
        
        m = mean(data)
        s = std_dev(data)
        if (abs(s) < 1.0d-10) then
            ku = 0.0d0
            return
        end if
        
        sum_val = 0.0d0
        do i = 1, n
            diff_val = (data(i) - m) / s
            sum_val = sum_val + diff_val * diff_val * diff_val * diff_val
        end do
        
        n_val = real(n, 8)
        ku = ((n_val * (n_val + 1.0d0)) / ((n_val - 1.0d0) * (n_val - 2.0d0) * (n_val - 3.0d0))) * sum_val - &
             (3.0d0 * (n_val - 1.0d0)**2) / ((n_val - 2.0d0) * (n_val - 3.0d0))
    end function kurtosis
    
    ! =========================================================================
    ! Correlation
    ! =========================================================================
    
    function covariance(x, y) result(cov)
        real(8), intent(in) :: x(:), y(:)
        real(8) :: cov, mean_x, mean_y, sum_val
        integer :: n, i
        
        n = size(x)
        if (n /= size(y) .or. n < 2) then
            cov = 0.0d0
            return
        end if
        
        mean_x = mean(x)
        mean_y = mean(y)
        
        sum_val = 0.0d0
        do i = 1, n
            sum_val = sum_val + (x(i) - mean_x) * (y(i) - mean_y)
        end do
        cov = sum_val / real(n - 1, 8)
    end function covariance
    
    function pearson_correlation(x, y) result(r)
        real(8), intent(in) :: x(:), y(:)
        real(8) :: r, std_x, std_y
        
        std_x = std_dev(x)
        std_y = std_dev(y)
        
        if (abs(std_x) < 1.0d-10 .or. abs(std_y) < 1.0d-10) then
            r = 0.0d0
            return
        end if
        
        r = covariance(x, y) / (std_x * std_y)
        r = max(-1.0d0, min(1.0d0, r))
    end function pearson_correlation
    
    function spearman_correlation(x, y) result(r)
        real(8), intent(in) :: x(:), y(:)
        real(8) :: r
        real(8), allocatable :: rank_x(:), rank_y(:)
        integer :: n
        
        n = size(x)
        if (n /= size(y) .or. n < 2) then
            r = 0.0d0
            return
        end if
        
        allocate(rank_x(n), rank_y(n))
        call compute_ranks(x, rank_x)
        call compute_ranks(y, rank_y)
        r = pearson_correlation(rank_x, rank_y)
        deallocate(rank_x, rank_y)
    end function spearman_correlation
    
    ! =========================================================================
    ! Linear Regression
    ! =========================================================================
    
    subroutine linear_regression(x, y, slope, intercept, r_squared)
        real(8), intent(in) :: x(:), y(:)
        real(8), intent(out) :: slope, intercept, r_squared
        real(8) :: mean_x, mean_y, ss_xx, ss_xy, ss_yy, sst, sse
        real(8), allocatable :: y_pred(:)
        integer :: n, i
        
        n = size(x)
        if (n /= size(y) .or. n < 2) then
            slope = 0.0d0
            intercept = 0.0d0
            r_squared = 0.0d0
            return
        end if
        
        mean_x = mean(x)
        mean_y = mean(y)
        
        ss_xx = 0.0d0
        ss_xy = 0.0d0
        do i = 1, n
            ss_xx = ss_xx + (x(i) - mean_x)**2
            ss_xy = ss_xy + (x(i) - mean_x) * (y(i) - mean_y)
        end do
        
        if (abs(ss_xx) < 1.0d-10) then
            slope = 0.0d0
            intercept = mean_y
        else
            slope = ss_xy / ss_xx
            intercept = mean_y - slope * mean_x
        end if
        
        ! R-squared
        ss_yy = 0.0d0
        do i = 1, n
            ss_yy = ss_yy + (y(i) - mean_y)**2
        end do
        sst = ss_yy
        
        allocate(y_pred(n))
        do i = 1, n
            y_pred(i) = intercept + slope * x(i)
        end do
        
        sse = 0.0d0
        do i = 1, n
            sse = sse + (y(i) - y_pred(i))**2
        end do
        deallocate(y_pred)
        
        if (abs(sst) < 1.0d-10) then
            r_squared = 1.0d0
        else
            r_squared = 1.0d0 - sse / sst
        end if
    end subroutine linear_regression
    
    ! =========================================================================
    ! Moving Statistics
    ! =========================================================================
    
    function moving_mean(data, window) result(ma)
        real(8), intent(in) :: data(:)
        integer, intent(in) :: window
        real(8), allocatable :: ma(:)
        integer :: n, i, j, count
        real(8) :: sum_val
        
        n = size(data)
        if (window <= 0 .or. window > n) then
            allocate(ma(n))
            ma = data
            return
        end if
        
        allocate(ma(n))
        do i = 1, n
            sum_val = 0.0d0
            count = 0
            do j = max(1, i - window + 1), i
                sum_val = sum_val + data(j)
                count = count + 1
            end do
            ma(i) = sum_val / real(count, 8)
        end do
    end function moving_mean
    
    function moving_std(data, window) result(ms)
        real(8), intent(in) :: data(:)
        integer, intent(in) :: window
        real(8), allocatable :: ms(:)
        integer :: n, i, j, count
        real(8) :: m, sum_val, diff_val
        
        n = size(data)
        if (window <= 0 .or. window > n) then
            allocate(ms(n))
            ms = 0.0d0
            return
        end if
        
        allocate(ms(n))
        do i = 1, n
            ! Calculate mean for window
            sum_val = 0.0d0
            count = 0
            do j = max(1, i - window + 1), i
                sum_val = sum_val + data(j)
                count = count + 1
            end do
            m = sum_val / real(count, 8)
            
            ! Calculate variance for window
            sum_val = 0.0d0
            do j = max(1, i - window + 1), i
                diff_val = data(j) - m
                sum_val = sum_val + diff_val * diff_val
            end do
            
            if (count >= 2) then
                ms(i) = sqrt(sum_val / real(count - 1, 8))
            else
                ms(i) = 0.0d0
            end if
        end do
    end function moving_std
    
    ! =========================================================================
    ! Histogram
    ! =========================================================================
    
    subroutine histogram(data, num_bins, counts, edges)
        real(8), intent(in) :: data(:)
        integer, intent(in) :: num_bins
        integer, allocatable, intent(out) :: counts(:)
        real(8), allocatable, intent(out) :: edges(:)
        real(8) :: data_min, data_max, bin_width
        integer :: n, i, bin_idx
        
        n = size(data)
        if (n == 0 .or. num_bins < 1) then
            allocate(counts(0), edges(0))
            return
        end if
        
        allocate(counts(num_bins), edges(num_bins + 1))
        
        data_min = minval(data)
        data_max = maxval(data)
        
        if (abs(data_max - data_min) < 1.0d-10) then
            counts = 0
            counts(1) = n
            do i = 1, num_bins + 1
                edges(i) = data_min
            end do
            return
        end if
        
        bin_width = (data_max - data_min) / real(num_bins, 8)
        
        do i = 1, num_bins + 1
            edges(i) = data_min + real(i - 1, 8) * bin_width
        end do
        
        counts = 0
        do i = 1, n
            bin_idx = int((data(i) - data_min) / bin_width) + 1
            bin_idx = max(1, min(num_bins, bin_idx))
            counts(bin_idx) = counts(bin_idx) + 1
        end do
    end subroutine histogram
    
    ! =========================================================================
    ! Normalization
    ! =========================================================================
    
    function z_score(value, data) result(z)
        real(8), intent(in) :: value
        real(8), intent(in) :: data(:)
        real(8) :: z, m, s
        
        m = mean(data)
        s = std_dev(data)
        if (abs(s) < 1.0d-10) then
            z = 0.0d0
        else
            z = (value - m) / s
        end if
    end function z_score
    
    function normalize(data) result(normed)
        real(8), intent(in) :: data(:)
        real(8), allocatable :: normed(:)
        real(8) :: data_min, data_max
        integer :: n
        
        n = size(data)
        allocate(normed(n))
        if (n == 0) return
        
        data_min = minval(data)
        data_max = maxval(data)
        
        if (abs(data_max - data_min) < 1.0d-10) then
            normed = 0.5d0
        else
            do n = 1, size(data)
                normed(n) = (data(n) - data_min) / (data_max - data_min)
            end do
        end if
    end function normalize
    
    function standard_error(data) result(se)
        real(8), intent(in) :: data(:)
        real(8) :: se
        se = std_dev(data) / sqrt(real(size(data), 8))
    end function standard_error
    
    subroutine confidence_interval(data, confidence_level, lower, upper)
        real(8), intent(in) :: data(:)
        real(8), intent(in) :: confidence_level
        real(8), intent(out) :: lower, upper
        real(8) :: m, se, t_crit
        integer :: n
        
        n = size(data)
        if (n < 2) then
            lower = 0.0d0
            upper = 0.0d0
            return
        end if
        
        m = mean(data)
        se = standard_error(data)
        t_crit = t_critical_value(confidence_level, n - 1)
        lower = m - t_crit * se
        upper = m + t_crit * se
    end subroutine confidence_interval
    
    ! =========================================================================
    ! Probability Distributions
    ! =========================================================================
    
    function normal_pdf(x, mu, sigma) result(pdf)
        real(8), intent(in) :: x, mu, sigma
        real(8) :: pdf, z
        
        if (sigma <= 0.0d0) then
            pdf = 0.0d0
            return
        end if
        z = (x - mu) / sigma
        pdf = (1.0d0 / (sigma * sqrt(2.0d0 * PI))) * exp(-0.5d0 * z**2)
    end function normal_pdf
    
    function normal_cdf(x, mu, sigma) result(cdf)
        real(8), intent(in) :: x, mu, sigma
        real(8) :: cdf, z
        
        if (sigma <= 0.0d0) then
            cdf = 0.0d0
            return
        end if
        z = (x - mu) / sigma
        cdf = 0.5d0 * (1.0d0 + erf_approx(z / sqrt(2.0d0)))
    end function normal_cdf
    
    ! =========================================================================
    ! Helper Functions
    ! =========================================================================
    
    recursive subroutine quick_sort(arr)
        real(8), intent(inout) :: arr(:)
        real(8) :: pivot, temp
        integer :: i, j, n
        
        n = size(arr)
        if (n <= 1) return
        
        pivot = arr(n / 2 + 1)
        i = 1
        j = n
        
        do
            do while (arr(i) < pivot)
                i = i + 1
            end do
            do while (arr(j) > pivot)
                j = j - 1
            end do
            if (i >= j) exit
            temp = arr(i)
            arr(i) = arr(j)
            arr(j) = temp
            i = i + 1
            j = j - 1
        end do
        
        if (i > 1) call quick_sort(arr(1:i-1))
        if (j < n) call quick_sort(arr(j+1:n))
    end subroutine quick_sort
    
    subroutine compute_ranks(data, ranks)
        real(8), intent(in) :: data(:)
        real(8), intent(out) :: ranks(:)
        integer, allocatable :: order(:)
        real(8), allocatable :: sorted(:)
        integer :: n, i, j, start_idx
        real(8) :: avg_rank
        
        n = size(data)
        allocate(order(n), sorted(n))
        
        do i = 1, n
            order(i) = i
            sorted(i) = data(i)
        end do
        
        call sort_with_indices(sorted, order)
        
        i = 1
        do while (i <= n)
            start_idx = i
            j = i
            do while (j < n .and. abs(sorted(j+1) - sorted(i)) < 1.0d-10)
                j = j + 1
            end do
            
            avg_rank = real(start_idx + j, 8) / 2.0d0
            do while (start_idx <= j)
                ranks(order(start_idx)) = avg_rank
                start_idx = start_idx + 1
            end do
            i = j + 1
        end do
        
        deallocate(order, sorted)
    end subroutine compute_ranks
    
    subroutine sort_with_indices(arr, indices)
        real(8), intent(inout) :: arr(:)
        integer, intent(inout) :: indices(:)
        real(8) :: temp_val
        integer :: temp_idx, i, j, n
        logical :: swapped
        
        n = size(arr)
        do i = 1, n - 1
            swapped = .false.
            do j = 1, n - i
                if (arr(j) > arr(j+1)) then
                    temp_val = arr(j)
                    arr(j) = arr(j+1)
                    arr(j+1) = temp_val
                    temp_idx = indices(j)
                    indices(j) = indices(j+1)
                    indices(j+1) = temp_idx
                    swapped = .true.
                end if
            end do
            if (.not. swapped) exit
        end do
    end subroutine sort_with_indices
    
    function erf_approx(x) result(res)
        real(8), intent(in) :: x
        real(8) :: res, t, tau
        
        t = 1.0d0 / (1.0d0 + 0.5d0 * abs(x))
        tau = t * exp(-x*x - 1.26551223d0 + 1.00002368d0*t + &
                      0.37409196d0*t*t + 0.09678418d0*t*t*t - &
                      0.18628806d0*t*t*t*t + 0.27886807d0*t*t*t*t*t - &
                      1.13520398d0*t*t*t*t*t*t + 1.48851587d0*t*t*t*t*t*t*t - &
                      0.82215223d0*t*t*t*t*t*t*t*t + 0.17087277d0*t*t*t*t*t*t*t*t*t)
        res = sign(1.0d0, x) * (1.0d0 - tau)
    end function erf_approx
    
    function t_critical_value(confidence, df) result(t)
        real(8), intent(in) :: confidence
        integer, intent(in) :: df
        real(8) :: t
        
        if (df >= 100) then
            if (confidence > 0.95d0) then
                t = 2.576d0
            else if (confidence > 0.90d0) then
                t = 1.96d0
            else
                t = 1.645d0
            end if
        else
            t = 2.0d0 * (1.0d0 + 1.0d0 / real(df, 8))
        end if
    end function t_critical_value

end module statistics_utils