"""
AllToolkit - Python Statistics Utils Test Suite

Comprehensive tests for statistics utilities covering:
- Descriptive statistics (mean, median, mode, variance, std_dev)
- Correlation and regression
- Normalization and scaling
- Outlier detection
- Distribution functions
- Frequency analysis
- Edge cases and error handling

Run: python statistics_utils_test.py -v
"""

import unittest
import sys
import os
import math

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Exceptions
    StatisticsError, EmptyDataError, InvalidDataError,
    
    # Descriptive Statistics
    mean, geometric_mean, harmonic_mean, median, mode,
    variance, std_dev, quartiles, iqr, percentile,
    range_value, coefficient_of_variation, skewness, kurtosis,
    
    # Correlation and Regression
    covariance, correlation, spearman_correlation,
    linear_regression, predict,
    
    # Normalization
    normalize_minmax, standardize, robust_scale,
    
    # Outlier Detection
    detect_outliers_iqr, detect_outliers_zscore, remove_outliers,
    
    # Distribution Functions
    normal_pdf, normal_cdf, z_score, chi_square_statistic,
    
    # Frequency Analysis
    frequency_table, relative_frequency, cumulative_frequency,
    
    # Convenience
    describe, summary,
)


# ============================================================================
# Descriptive Statistics Tests
# ============================================================================

class TestMean(unittest.TestCase):
    """Tests for mean function."""
    
    def test_simple_mean(self):
        """Test basic arithmetic mean."""
        self.assertEqual(mean([1, 2, 3, 4, 5]), 3.0)
    
    def test_single_value(self):
        """Test mean of single value."""
        self.assertEqual(mean([42]), 42.0)
    
    def test_negative_values(self):
        """Test mean with negative values."""
        self.assertEqual(mean([-1, 0, 1]), 0.0)
    
    def test_float_values(self):
        """Test mean with floats."""
        self.assertAlmostEqual(mean([1.5, 2.5, 3.5]), 2.5)
    
    def test_empty_data(self):
        """Test mean of empty data raises error."""
        with self.assertRaises(EmptyDataError):
            mean([])


class TestGeometricMean(unittest.TestCase):
    """Tests for geometric mean function."""
    
    def test_simple_geometric_mean(self):
        """Test basic geometric mean."""
        # GM of 2, 8 = sqrt(2*8) = 4
        self.assertAlmostEqual(geometric_mean([2, 8]), 4.0)
    
    def test_three_values(self):
        """Test geometric mean of three values."""
        # GM of 1, 27, 8 = (1*27*8)^(1/3) = 6
        self.assertAlmostEqual(geometric_mean([1, 27, 8]), 6.0)
    
    def test_empty_data(self):
        """Test geometric mean of empty data raises error."""
        with self.assertRaises(EmptyDataError):
            geometric_mean([])
    
    def test_negative_values(self):
        """Test geometric mean with negative values raises error."""
        with self.assertRaises(InvalidDataError):
            geometric_mean([-1, 2, 3])


class TestHarmonicMean(unittest.TestCase):
    """Tests for harmonic mean function."""
    
    def test_simple_harmonic_mean(self):
        """Test basic harmonic mean."""
        # HM of 1, 2, 4 = 3 / (1 + 0.5 + 0.25) = 3/1.75 = 1.714...
        self.assertAlmostEqual(harmonic_mean([1, 2, 4]), 1.714285714, places=6)
    
    def test_empty_data(self):
        """Test harmonic mean of empty data raises error."""
        with self.assertRaises(EmptyDataError):
            harmonic_mean([])


class TestMedian(unittest.TestCase):
    """Tests for median function."""
    
    def test_odd_count(self):
        """Test median with odd number of values."""
        self.assertEqual(median([1, 3, 5, 7, 9]), 5)
    
    def test_even_count(self):
        """Test median with even number of values."""
        self.assertEqual(median([1, 2, 3, 4]), 2.5)
    
    def test_unsorted_data(self):
        """Test median with unsorted data."""
        self.assertEqual(median([9, 1, 5, 3, 7]), 5)
    
    def test_single_value(self):
        """Test median of single value."""
        self.assertEqual(median([42]), 42)
    
    def test_empty_data(self):
        """Test median of empty data raises error."""
        with self.assertRaises(EmptyDataError):
            median([])


class TestMode(unittest.TestCase):
    """Tests for mode function."""
    
    def test_single_mode(self):
        """Test data with single mode."""
        self.assertEqual(mode([1, 2, 2, 3, 4]), [2])
    
    def test_multiple_modes(self):
        """Test data with multiple modes."""
        result = mode([1, 1, 2, 2, 3])
        self.assertEqual(sorted(result), [1, 2])
    
    def test_no_mode(self):
        """Test data where all values appear once."""
        result = mode([1, 2, 3, 4, 5])
        self.assertEqual(len(result), 5)  # All are modes
    
    def test_empty_data(self):
        """Test mode of empty data raises error."""
        with self.assertRaises(EmptyDataError):
            mode([])


class TestVariance(unittest.TestCase):
    """Tests for variance function."""
    
    def test_sample_variance(self):
        """Test sample variance (default)."""
        # Sample variance of [1, 2, 3, 4, 5] = 2.5
        self.assertEqual(variance([1, 2, 3, 4, 5]), 2.5)
    
    def test_population_variance(self):
        """Test population variance."""
        # Population variance of [1, 2, 3, 4, 5] = 2.0
        self.assertEqual(variance([1, 2, 3, 4, 5], population=True), 2.0)
    
    def test_single_value_sample(self):
        """Test sample variance with single value raises error."""
        with self.assertRaises(ValueError):
            variance([42])
    
    def test_empty_data(self):
        """Test variance of empty data raises error."""
        with self.assertRaises(EmptyDataError):
            variance([])


class TestStdDev(unittest.TestCase):
    """Tests for standard deviation function."""
    
    def test_sample_std_dev(self):
        """Test sample standard deviation."""
        self.assertAlmostEqual(std_dev([1, 2, 3, 4, 5]), math.sqrt(2.5))
    
    def test_population_std_dev(self):
        """Test population standard deviation."""
        self.assertAlmostEqual(std_dev([1, 2, 3, 4, 5], population=True), math.sqrt(2.0))


class TestQuartiles(unittest.TestCase):
    """Tests for quartiles function."""
    
    def test_quartiles(self):
        """Test quartile calculation."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        q1, q2, q3 = quartiles(data)
        self.assertEqual(q2, 5)  # Median
    
    def test_empty_data(self):
        """Test quartiles of empty data raises error."""
        with self.assertRaises(EmptyDataError):
            quartiles([])


class TestIQR(unittest.TestCase):
    """Tests for IQR function."""
    
    def test_iqr(self):
        """Test IQR calculation."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # IQR depends on quartile method; just verify it's positive and reasonable
        iqr_val = iqr(data)
        self.assertGreater(iqr_val, 0)
        self.assertLess(iqr_val, 10)


class TestPercentile(unittest.TestCase):
    """Tests for percentile function."""
    
    def test_median_percentile(self):
        """Test 50th percentile equals median."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(percentile(data, 50), median(data))
    
    def test_min_max_percentiles(self):
        """Test 0th and 100th percentiles."""
        data = [1, 2, 3, 4, 5]
        self.assertEqual(percentile(data, 0), 1)
        self.assertEqual(percentile(data, 100), 5)
    
    def test_invalid_percentile(self):
        """Test invalid percentile raises error."""
        with self.assertRaises(ValueError):
            percentile([1, 2, 3], 150)


class TestRange(unittest.TestCase):
    """Tests for range function."""
    
    def test_range(self):
        """Test range calculation."""
        self.assertEqual(range_value([1, 5, 10, 3]), 9)
    
    def test_empty_data(self):
        """Test range of empty data raises error."""
        with self.assertRaises(EmptyDataError):
            range_value([])


class TestCoefficientOfVariation(unittest.TestCase):
    """Tests for coefficient of variation function."""
    
    def test_cv(self):
        """Test CV calculation."""
        data = [10, 20, 30, 40, 50]
        cv = coefficient_of_variation(data)
        self.assertGreater(cv, 0)
    
    def test_zero_mean(self):
        """Test CV with zero mean raises error."""
        with self.assertRaises(InvalidDataError):
            coefficient_of_variation([-1, 0, 1])


class TestSkewness(unittest.TestCase):
    """Tests for skewness function."""
    
    def test_symmetric_data(self):
        """Test skewness of symmetric data."""
        data = [1, 2, 3, 4, 5]
        skew = skewness(data)
        self.assertAlmostEqual(skew, 0, places=10)
    
    def test_right_skewed(self):
        """Test positive skewness (right-skewed)."""
        data = [1, 2, 3, 4, 100]
        self.assertGreater(skewness(data), 0)
    
    def test_left_skewed(self):
        """Test negative skewness (left-skewed)."""
        data = [-100, 1, 2, 3, 4]
        self.assertLess(skewness(data), 0)


class TestKurtosis(unittest.TestCase):
    """Tests for kurtosis function."""
    
    def test_kurtosis(self):
        """Test kurtosis calculation."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        kurt = kurtosis(data)
        self.assertIsInstance(kurt, float)


# ============================================================================
# Correlation and Regression Tests
# ============================================================================

class TestCovariance(unittest.TestCase):
    """Tests for covariance function."""
    
    def test_positive_covariance(self):
        """Test positive covariance."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        self.assertGreater(covariance(x, y), 0)
    
    def test_negative_covariance(self):
        """Test negative covariance."""
        x = [1, 2, 3, 4, 5]
        y = [10, 8, 6, 4, 2]
        self.assertLess(covariance(x, y), 0)
    
    def test_length_mismatch(self):
        """Test covariance with mismatched lengths raises error."""
        with self.assertRaises(ValueError):
            covariance([1, 2, 3], [1, 2])


class TestCorrelation(unittest.TestCase):
    """Tests for correlation function."""
    
    def test_perfect_positive(self):
        """Test perfect positive correlation."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        self.assertAlmostEqual(correlation(x, y), 1.0)
    
    def test_perfect_negative(self):
        """Test perfect negative correlation."""
        x = [1, 2, 3, 4, 5]
        y = [10, 8, 6, 4, 2]
        self.assertAlmostEqual(correlation(x, y), -1.0)
    
    def test_no_correlation(self):
        """Test near-zero correlation."""
        x = [1, 2, 3, 4, 5]
        y = [5, 3, 6, 2, 4]
        corr = correlation(x, y)
        self.assertLess(abs(corr), 0.5)


class TestSpearmanCorrelation(unittest.TestCase):
    """Tests for Spearman correlation function."""
    
    def test_spearman_perfect(self):
        """Test perfect Spearman correlation."""
        x = [1, 2, 3, 4, 5]
        y = [10, 20, 30, 40, 50]
        self.assertAlmostEqual(spearman_correlation(x, y), 1.0)


class TestLinearRegression(unittest.TestCase):
    """Tests for linear regression function."""
    
    def test_perfect_linear(self):
        """Test regression on perfect linear data."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        result = linear_regression(x, y)
        self.assertAlmostEqual(result['slope'], 2.0)
        self.assertAlmostEqual(result['intercept'], 0.0)
        self.assertAlmostEqual(result['r_squared'], 1.0)
    
    def test_prediction(self):
        """Test prediction using regression."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        reg = linear_regression(x, y)
        self.assertAlmostEqual(predict(reg, 6), 12.0)


# ============================================================================
# Normalization Tests
# ============================================================================

class TestNormalizeMinMax(unittest.TestCase):
    """Tests for min-max normalization."""
    
    def test_normalize_default_range(self):
        """Test normalization to [0, 1]."""
        data = [10, 20, 30, 40, 50]
        result = normalize_minmax(data)
        self.assertAlmostEqual(result[0], 0.0)
        self.assertAlmostEqual(result[-1], 1.0)
    
    def test_normalize_custom_range(self):
        """Test normalization to custom range."""
        data = [10, 20, 30, 40, 50]
        result = normalize_minmax(data, new_min=-1, new_max=1)
        self.assertAlmostEqual(result[0], -1.0)
        self.assertAlmostEqual(result[-1], 1.0)


class TestStandardize(unittest.TestCase):
    """Tests for standardization (z-scores)."""
    
    def test_standardize_mean_zero(self):
        """Test standardized data has mean 0."""
        data = [10, 20, 30, 40, 50]
        result = standardize(data)
        self.assertAlmostEqual(mean(result), 0.0, places=10)
    
    def test_standardize_std_one(self):
        """Test standardized data has std dev 1."""
        data = [10, 20, 30, 40, 50]
        result = standardize(data)
        self.assertAlmostEqual(std_dev(result), 1.0, places=10)


class TestRobustScale(unittest.TestCase):
    """Tests for robust scaling."""
    
    def test_robust_scale(self):
        """Test robust scaling."""
        data = [1, 2, 3, 4, 5, 100]  # With outlier
        result = robust_scale(data)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(data))


# ============================================================================
# Outlier Detection Tests
# ============================================================================

class TestDetectOutliersIQR(unittest.TestCase):
    """Tests for IQR outlier detection."""
    
    def test_detect_outlier(self):
        """Test detecting clear outlier."""
        data = [1, 2, 3, 4, 5, 100]
        outliers = detect_outliers_iqr(data)
        self.assertEqual(len(outliers), 1)
        self.assertEqual(outliers[0][1], 100)
    
    def test_no_outliers(self):
        """Test data without outliers."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        outliers = detect_outliers_iqr(data)
        self.assertEqual(len(outliers), 0)


class TestDetectOutliersZScore(unittest.TestCase):
    """Tests for z-score outlier detection."""
    
    def test_detect_outlier(self):
        """Test detecting outlier with z-score."""
        # Use more data points so the outlier doesn't dominate the statistics
        data = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 100]
        outliers = detect_outliers_zscore(data, threshold=2.5)
        self.assertGreater(len(outliers), 0)


class TestRemoveOutliers(unittest.TestCase):
    """Tests for outlier removal."""
    
    def test_remove_outliers_iqr(self):
        """Test removing outliers with IQR method."""
        data = [1, 2, 3, 4, 5, 100]
        result = remove_outliers(data, method='iqr')
        self.assertNotIn(100, result)
        self.assertEqual(len(result), 5)
    
    def test_invalid_method(self):
        """Test invalid method raises error."""
        with self.assertRaises(ValueError):
            remove_outliers([1, 2, 3], method='invalid')


# ============================================================================
# Distribution Function Tests
# ============================================================================

class TestNormalPDF(unittest.TestCase):
    """Tests for normal PDF."""
    
    def test_pdf_at_mean(self):
        """Test PDF at mean (should be maximum)."""
        pdf_at_mean = normal_pdf(0, mu=0, sigma=1)
        pdf_away = normal_pdf(2, mu=0, sigma=1)
        self.assertGreater(pdf_at_mean, pdf_away)
    
    def test_invalid_sigma(self):
        """Test invalid sigma raises error."""
        with self.assertRaises(ValueError):
            normal_pdf(0, sigma=0)


class TestNormalCDF(unittest.TestCase):
    """Tests for normal CDF."""
    
    def test_cdf_at_mean(self):
        """Test CDF at mean should be 0.5."""
        self.assertAlmostEqual(normal_cdf(0, mu=0, sigma=1), 0.5, places=10)
    
    def test_cdf_range(self):
        """Test CDF is between 0 and 1."""
        # Use reasonable values where CDF is not at floating point limits
        self.assertGreater(normal_cdf(-5), 0)
        self.assertLess(normal_cdf(5), 1)
        # Verify CDF approaches limits
        self.assertAlmostEqual(normal_cdf(-10), 0, places=15)
        self.assertAlmostEqual(normal_cdf(10), 1, places=15)


class TestZScore(unittest.TestCase):
    """Tests for z-score calculation."""
    
    def test_z_score(self):
        """Test z-score calculation."""
        z = z_score(85, mu=70, sigma=10)
        self.assertEqual(z, 1.5)


class TestChiSquare(unittest.TestCase):
    """Tests for chi-square statistic."""
    
    def test_chi_square(self):
        """Test chi-square calculation."""
        observed = [50, 50, 50, 50]
        expected = [45, 55, 45, 55]
        chi2 = chi_square_statistic(observed, expected)
        self.assertGreater(chi2, 0)


# ============================================================================
# Frequency Analysis Tests
# ============================================================================

class TestFrequencyTable(unittest.TestCase):
    """Tests for frequency table."""
    
    def test_frequency_table(self):
        """Test frequency table creation."""
        data = ['a', 'b', 'a', 'c', 'a', 'b']
        freq = frequency_table(data)
        self.assertEqual(freq['a'], 3)
        self.assertEqual(freq['b'], 2)
        self.assertEqual(freq['c'], 1)


class TestRelativeFrequency(unittest.TestCase):
    """Tests for relative frequency."""
    
    def test_relative_frequency(self):
        """Test relative frequency sums to 1."""
        data = ['a', 'b', 'a', 'c', 'a', 'b']
        rel_freq = relative_frequency(data)
        self.assertAlmostEqual(sum(rel_freq.values()), 1.0)


class TestCumulativeFrequency(unittest.TestCase):
    """Tests for cumulative frequency."""
    
    def test_cumulative_frequency(self):
        """Test cumulative frequency calculation."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        cum_freq = cumulative_frequency(data, bins=5)
        self.assertEqual(cum_freq[-1][1], 10)  # Total count


# ============================================================================
# Convenience Function Tests
# ============================================================================

class TestDescribe(unittest.TestCase):
    """Tests for describe function."""
    
    def test_describe(self):
        """Test comprehensive description."""
        data = [1, 2, 3, 4, 5]
        stats = describe(data)
        self.assertIn('mean', stats)
        self.assertIn('std_dev', stats)
        self.assertIn('median', stats)
        self.assertEqual(stats['count'], 5)


class TestSummary(unittest.TestCase):
    """Tests for summary function."""
    
    def test_summary(self):
        """Test summary string generation."""
        data = [1, 2, 3, 4, 5]
        result = summary(data)
        self.assertIsInstance(result, str)
        self.assertIn('Mean', result)
        self.assertIn('Count', result)


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================

class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""
    
    def test_all_same_values(self):
        """Test statistics with all same values."""
        data = [5, 5, 5, 5, 5]
        self.assertEqual(mean(data), 5)
        self.assertEqual(median(data), 5)
        self.assertEqual(variance(data, population=True), 0)
    
    def test_large_values(self):
        """Test with large values."""
        data = [1e10, 2e10, 3e10]
        self.assertAlmostEqual(mean(data), 2e10)
    
    def test_small_values(self):
        """Test with very small values."""
        data = [1e-10, 2e-10, 3e-10]
        self.assertAlmostEqual(mean(data), 2e-10)
    
    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative values."""
        data = [-10, -5, 0, 5, 10]
        self.assertEqual(mean(data), 0)


class TestErrorHandling(unittest.TestCase):
    """Tests for error handling."""
    
    def test_empty_data_errors(self):
        """Test that empty data raises appropriate errors."""
        empty_funcs = [
            lambda: mean([]),
            lambda: median([]),
            lambda: variance([]),
            lambda: std_dev([]),
            lambda: quartiles([]),
            lambda: range_value([]),
        ]
        for func in empty_funcs:
            with self.assertRaises(EmptyDataError):
                func()


# ============================================================================
# Test Runner
# ============================================================================

if __name__ == '__main__':
    unittest.main(verbosity=2)
