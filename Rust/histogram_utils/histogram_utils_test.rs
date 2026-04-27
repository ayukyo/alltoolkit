//! # Histogram Utilities Tests
//!
//! Comprehensive tests for the histogram utilities module.

use histogram_utils::{Histogram, BinningStrategy, describe, histogram, histogram_with_bins, Stats};

mod basic_tests {
    use super::*;

    #[test]
    fn test_histogram_creation_basic() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Sturges).unwrap();
        
        assert!(hist.bin_count() > 0);
        assert_eq!(hist.total(), 5);
        assert!((hist.min() - 1.0).abs() < 1e-10);
        assert!((hist.max() - 5.0).abs() < 1e-10);
    }

    #[test]
    fn test_histogram_empty_data() {
        let data: Vec<f64> = vec![];
        assert!(Histogram::new(&data, BinningStrategy::Sturges).is_none());
    }

    #[test]
    fn test_histogram_single_value() {
        let data = vec![42.0; 10];
        let hist = Histogram::new(&data, BinningStrategy::Sturges).unwrap();
        
        assert_eq!(hist.total(), 10);
        assert!((hist.min() - 42.0).abs() < 1e-10);
        assert!((hist.max() - 42.0).abs() < 1e-10);
    }

    #[test]
    fn test_histogram_two_values() {
        let data = vec![1.0, 2.0];
        let hist = Histogram::new(&data, BinningStrategy::Sturges).unwrap();
        
        assert_eq!(hist.total(), 2);
        assert!(hist.bin_count() > 0);
    }

    #[test]
    fn test_histogram_with_bins() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0];
        let hist = Histogram::with_bins(&data, 5).unwrap();
        
        assert_eq!(hist.bin_count(), 5);
    }

    #[test]
    fn test_histogram_with_zero_bins() {
        let data = vec![1.0, 2.0, 3.0];
        assert!(Histogram::with_bins(&data, 0).is_none());
    }

    #[test]
    fn test_histogram_with_edges() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0];
        let edges = vec![0.0, 2.0, 4.0, 6.0, 8.0];
        let hist = Histogram::with_edges(&data, &edges).unwrap();
        
        assert_eq!(hist.bin_count(), 4);
    }

    #[test]
    fn test_histogram_with_invalid_edges() {
        let data = vec![1.0, 2.0, 3.0];
        
        // Empty edges
        assert!(Histogram::with_edges(&data, &[]).is_none());
        
        // Single edge
        assert!(Histogram::with_edges(&data, &[1.0]).is_none());
        
        // Unsorted edges
        assert!(Histogram::with_edges(&data, &[3.0, 1.0, 2.0]).is_none());
        
        // Duplicate edges
        assert!(Histogram::with_edges(&data, &[1.0, 2.0, 2.0, 3.0]).is_none());
    }
}

mod binning_strategy_tests {
    use super::*;

    #[test]
    fn test_sturges_rule() {
        // Sturges: k = 1 + log2(n)
        let data: Vec<f64> = (1..=100).map(|x| x as f64).collect();
        let hist = Histogram::new(&data, BinningStrategy::Sturges).unwrap();
        
        // For n=100, Sturges gives k = 1 + log2(100) ≈ 7.64 → 8 bins
        assert!(hist.bin_count() >= 7 && hist.bin_count() <= 9);
    }

    #[test]
    fn test_sqrt_rule() {
        // Square root: k = sqrt(n)
        let data: Vec<f64> = (1..=100).map(|x| x as f64).collect();
        let hist = Histogram::new(&data, BinningStrategy::SquareRoot).unwrap();
        
        // For n=100, sqrt(100) = 10 bins
        assert_eq!(hist.bin_count(), 10);
    }

    #[test]
    fn test_rice_rule() {
        // Rice: k = 2 * n^(1/3)
        let data: Vec<f64> = (1..=100).map(|x| x as f64).collect();
        let hist = Histogram::new(&data, BinningStrategy::Rice).unwrap();
        
        // For n=100, 2 * 100^(1/3) ≈ 9.28 → 10 bins
        assert!(hist.bin_count() >= 9 && hist.bin_count() <= 11);
    }

    #[test]
    fn test_freedman_diaconis_rule() {
        let data: Vec<f64> = (1..=100).map(|x| x as f64).collect();
        let hist = Histogram::new(&data, BinningStrategy::FreedmanDiaconis).unwrap();
        
        assert!(hist.bin_count() > 0);
    }

    #[test]
    fn test_fixed_bins() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(3)).unwrap();
        
        assert_eq!(hist.bin_count(), 3);
    }

    #[test]
    fn test_bin_width_calculation() {
        let data = vec![0.0, 1.0, 2.0, 3.0, 4.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(4)).unwrap();
        
        // Range is 4, with 4 bins, each bin should be width 1.0
        assert!((hist.bin_width() - 1.0).abs() < 1e-10);
    }
}

mod statistical_tests {
    use super::*;

    #[test]
    fn test_histogram_mean() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let mean = hist.mean().unwrap();
        // Mean should be approximately 3.0
        assert!((mean - 3.0).abs() < 0.5);
    }

    #[test]
    fn test_histogram_mean_uniform() {
        let data: Vec<f64> = (1..=100).map(|x| x as f64).collect();
        let hist = Histogram::new(&data, BinningStrategy::Fixed(10)).unwrap();
        
        let mean = hist.mean().unwrap();
        // Mean of 1-100 is 50.5
        assert!((mean - 50.5).abs() < 5.0);
    }

    #[test]
    fn test_histogram_variance() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let variance = hist.variance().unwrap();
        assert!(variance >= 0.0);
    }

    #[test]
    fn test_histogram_std_dev() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let std_dev = hist.std_dev().unwrap();
        let variance = hist.variance().unwrap();
        
        assert!((std_dev - variance.sqrt()).abs() < 1e-10);
    }

    #[test]
    fn test_histogram_median() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let median = hist.median().unwrap();
        // Median of 1-5 is 3
        assert!((median - 3.0).abs() < 0.5);
    }

    #[test]
    fn test_histogram_mode() {
        // Create data with clear mode
        let data = vec![1.0, 1.0, 1.0, 1.0, 5.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let mode = hist.mode().unwrap();
        // Mode should be around 1.0
        assert!(mode < 2.0);
    }

    #[test]
    fn test_histogram_percentile() {
        let data: Vec<f64> = (1..=100).map(|x| x as f64).collect();
        let hist = Histogram::new(&data, BinningStrategy::Fixed(20)).unwrap();
        
        let p25 = hist.percentile(25.0).unwrap();
        let p50 = hist.percentile(50.0).unwrap();
        let p75 = hist.percentile(75.0).unwrap();
        
        // Approximate percentiles
        assert!(p25 > 15.0 && p25 < 35.0);
        assert!(p50 > 40.0 && p50 < 60.0);
        assert!(p75 > 65.0 && p75 < 85.0);
    }

    #[test]
    fn test_histogram_percentile_invalid() {
        let data = vec![1.0, 2.0, 3.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(3)).unwrap();
        
        assert!(hist.percentile(-1.0).is_none());
        assert!(hist.percentile(101.0).is_none());
    }

    #[test]
    fn test_histogram_cdf() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let cdf = hist.cdf();
        
        // CDF should be non-decreasing
        for i in 1..cdf.len() {
            assert!(cdf[i] >= cdf[i - 1]);
        }
        
        // Last value should be 1.0
        assert!((cdf[cdf.len() - 1] - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_histogram_frequencies() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let freqs = hist.frequencies();
        let sum: f64 = freqs.iter().sum();
        
        assert!((sum - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_histogram_density() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let density = hist.density();
        
        // All density values should be non-negative
        for &d in &density {
            assert!(d >= 0.0);
        }
    }
}

mod describe_tests {
    use super::*;

    #[test]
    fn test_describe_basic() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let stats = describe(&data).unwrap();
        
        assert_eq!(stats.count, 5);
        assert!((stats.sum - 15.0).abs() < 1e-10);
        assert!((stats.mean - 3.0).abs() < 1e-10);
        assert!((stats.min - 1.0).abs() < 1e-10);
        assert!((stats.max - 5.0).abs() < 1e-10);
        assert!((stats.range - 4.0).abs() < 1e-10);
        assert!((stats.median - 3.0).abs() < 1e-10);
    }

    #[test]
    fn test_describe_variance() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let stats = describe(&data).unwrap();
        
        // Population variance of [1,2,3,4,5] is 2.0
        assert!((stats.variance - 2.0).abs() < 1e-10);
        assert!((stats.std_dev - 2.0_f64.sqrt()).abs() < 1e-10);
    }

    #[test]
    fn test_describe_even_count() {
        let data = vec![1.0, 2.0, 3.0, 4.0];
        let stats = describe(&data).unwrap();
        
        assert_eq!(stats.count, 4);
        assert!((stats.median - 2.5).abs() < 1e-10);
    }

    #[test]
    fn test_describe_empty() {
        let data: Vec<f64> = vec![];
        assert!(describe(&data).is_none());
    }

    #[test]
    fn test_describe_single_value() {
        let data = vec![5.0];
        let stats = describe(&data).unwrap();
        
        assert_eq!(stats.count, 1);
        assert!((stats.mean - 5.0).abs() < 1e-10);
        assert!((stats.variance - 0.0).abs() < 1e-10);
    }

    #[test]
    fn test_describe_large_dataset() {
        let data: Vec<f64> = (1..=1000).map(|x| x as f64).collect();
        let stats = describe(&data).unwrap();
        
        assert_eq!(stats.count, 1000);
        assert!((stats.min - 1.0).abs() < 1e-10);
        assert!((stats.max - 1000.0).abs() < 1e-10);
        assert!((stats.range - 999.0).abs() < 1e-10);
    }
}

mod utility_tests {
    use super::*;

    #[test]
    fn test_histogram_function() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = histogram(&data).unwrap();
        
        assert!(hist.bin_count() > 0);
    }

    #[test]
    fn test_histogram_with_bins_function() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = histogram_with_bins(&data, 3).unwrap();
        
        assert_eq!(hist.bin_count(), 3);
    }

    #[test]
    fn test_bin_for_value() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        // Test values within range
        assert!(hist.bin_for_value(1.0).is_some());
        assert!(hist.bin_for_value(3.0).is_some());
        assert!(hist.bin_for_value(5.0).is_some());
        
        // Test values outside range
        assert!(hist.bin_for_value(0.0).is_none());
        assert!(hist.bin_for_value(10.0).is_none());
    }

    #[test]
    fn test_count_for_bin() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let total: usize = (0..hist.bin_count())
            .filter_map(|i| hist.count_for_bin(i))
            .sum();
        
        assert_eq!(total, 5);
    }

    #[test]
    fn test_bin_range() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let range = hist.bin_range(0).unwrap();
        assert!(range.0 < range.1);
        
        // Invalid bin index
        assert!(hist.bin_range(100).is_none());
    }

    #[test]
    fn test_bin_midpoint() {
        let data = vec![0.0, 10.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(2)).unwrap();
        
        let midpoint = hist.bin_midpoint(0).unwrap();
        assert!(midpoint >= 0.0 && midpoint <= 10.0);
    }

    #[test]
    fn test_max_bin() {
        let data = vec![1.0, 1.0, 1.0, 5.0, 5.0, 5.0, 5.0, 5.0]; // More 5s
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let max_bin = hist.max_bin().unwrap();
        assert!(max_bin < hist.bin_count());
    }

    #[test]
    fn test_min_bin() {
        let data = vec![1.0, 1.0, 1.0, 2.0, 3.0]; // More 1s
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let min_bin_exclude_empty = hist.min_bin(true).unwrap();
        assert!(min_bin_exclude_empty < hist.bin_count());
    }

    #[test]
    fn test_bins_above_threshold() {
        let data = vec![1.0, 1.0, 1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let bins = hist.bins_above_threshold(0);
        assert!(bins.len() > 0);
    }
}

mod merge_tests {
    use super::*;

    #[test]
    fn test_histogram_merge_same_edges() {
        let data1 = vec![1.0, 2.0, 3.0];
        let data2 = vec![2.0, 3.0, 4.0];
        
        let mut hist1 = Histogram::new(&data1, BinningStrategy::Fixed(5)).unwrap();
        let hist2 = Histogram::new(&data1, BinningStrategy::Fixed(5)).unwrap();
        
        let result = hist1.merge(&hist2);
        assert!(result.is_ok());
        assert_eq!(hist1.total(), 6);
    }

    #[test]
    fn test_histogram_merge_different_edges() {
        let data1 = vec![1.0, 2.0, 3.0];
        let data2 = vec![1.0, 2.0, 3.0, 4.0, 5.0]; // Different range
        
        let hist1 = Histogram::new(&data1, BinningStrategy::Fixed(5)).unwrap();
        let hist2 = Histogram::new(&data2, BinningStrategy::Fixed(5)).unwrap();
        
        // Different edges should fail
        let mut hist1_clone = hist1.clone();
        assert!(hist1_clone.merge(&hist2).is_err());
    }
}

mod ascii_test {
    use super::*;

    #[test]
    fn test_to_ascii() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let ascii = hist.to_ascii(10);
        
        assert!(!ascii.is_empty());
        assert!(ascii.contains("█")); // Contains bar characters
    }

    #[test]
    fn test_to_ascii_empty() {
        let hist = Histogram::new(&[], BinningStrategy::Fixed(5));
        assert!(hist.is_none());
    }

    #[test]
    fn test_to_ascii_zero_width() {
        let data = vec![1.0, 2.0, 3.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(3)).unwrap();
        
        let ascii = hist.to_ascii(0);
        assert!(ascii.is_empty());
    }
}

mod edge_cases {
    use super::*;

    #[test]
    fn test_negative_values() {
        let data = vec![-5.0, -3.0, -1.0, 0.0, 1.0, 3.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        assert_eq!(hist.total(), 7);
        assert!((hist.min() - (-5.0)).abs() < 1e-10);
        assert!((hist.max() - 5.0).abs() < 1e-10);
    }

    #[test]
    fn test_very_large_values() {
        let data = vec![1e10, 2e10, 3e10, 4e10, 5e10];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        assert_eq!(hist.total(), 5);
    }

    #[test]
    fn test_very_small_values() {
        let data = vec![1e-10, 2e-10, 3e-10, 4e-10, 5e-10];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        assert_eq!(hist.total(), 5);
    }

    #[test]
    fn test_many_bins() {
        let data: Vec<f64> = (1..=1000).map(|x| x as f64).collect();
        let hist = Histogram::new(&data, BinningStrategy::Fixed(100)).unwrap();
        
        assert_eq!(hist.bin_count(), 100);
    }

    #[test]
    fn test_duplicate_values() {
        let data = vec![5.0; 100]; // All same value
        let hist = Histogram::new(&data, BinningStrategy::Fixed(10)).unwrap();
        
        assert_eq!(hist.total(), 100);
    }

    #[test]
    fn test_outliers() {
        let mut data: Vec<f64> = (1..=100).map(|x| x as f64).collect();
        data.push(1e6); // Outlier
        data.push(-1e6); // Outlier
        
        let hist = Histogram::new(&data, BinningStrategy::Fixed(10)).unwrap();
        
        assert_eq!(hist.total(), 102);
    }
}

mod real_world_scenarios {
    use super::*;

    #[test]
    fn test_normal_distribution_approximation() {
        // Generate approximate normal distribution
        let mut data = Vec::new();
        for _ in 0..1000 {
            // Simple approximation of normal distribution
            let sum: f64 = (0..12).map(|_| rand_simple()).sum();
            data.push(sum - 6.0); // Mean 0, std 1
        }
        
        let hist = Histogram::new(&data, BinningStrategy::Sturges).unwrap();
        
        // Mode should be near 0
        let mode = hist.mode().unwrap();
        assert!(mode.abs() < 2.0);
        
        // Mean should be near 0
        let mean = hist.mean().unwrap();
        assert!(mean.abs() < 0.5);
    }

    #[test]
    fn test_bimodal_distribution() {
        // Create bimodal distribution
        let mut data = Vec::new();
        for _ in 0..50 {
            data.push(-5.0);
            data.push(5.0);
        }
        
        let hist = Histogram::new(&data, BinningStrategy::Fixed(10)).unwrap();
        
        assert_eq!(hist.total(), 100);
    }

    #[test]
    fn test_uniform_distribution() {
        // Uniform distribution from 0 to 10
        let data: Vec<f64> = (0..100).map(|x| (x % 11) as f64).collect();
        
        let hist = Histogram::new(&data, BinningStrategy::Fixed(10)).unwrap();
        
        // For uniform distribution, frequencies should be roughly equal
        let freqs = hist.frequencies();
        let max_freq = freqs.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let min_freq = freqs.iter().cloned().fold(f64::INFINITY, f64::min);
        
        // Not exactly equal due to discretization, but should be close
        assert!(max_freq - min_freq < 0.5);
    }
}

// Simple random number generator for tests
fn rand_simple() -> f64 {
    use std::time::{SystemTime, UNIX_EPOCH};
    let seed = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos() as u64;
    // Simple LCG
    let state = seed.wrapping_mul(6364136223846793005).wrapping_add(1);
    (state >> 33) as f64 / (1u64 << 31) as f64
}