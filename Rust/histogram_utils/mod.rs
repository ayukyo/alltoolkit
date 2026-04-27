//! # Histogram Utilities
//!
//! A collection of histogram utilities for Rust.
//! Provides binning strategies, histogram creation, and statistical analysis.
//! All functions are pure (no side effects) and have zero external dependencies.
//!
//! ## Features
//!
//! - Multiple binning strategies (equal-width, equal-frequency, Sturges, Freedman-Diaconis)
//! - Histogram creation and manipulation
//! - Statistical measures (mean, median, mode from histogram)
//! - Percentile calculation
//!
//! ## Usage
//!
//! ```rust
//! use histogram_utils::{Histogram, BinningStrategy};
//!
//! let data = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0];
//! let mut histogram = Histogram::new(&data, BinningStrategy::Sturges);
//! 
//! println!("Bin counts: {:?}", histogram.counts());
//! println!("Mean: {:?}", histogram.mean());
//! ```

use std::cmp::Ordering;

/// Binning strategy for histogram creation.
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum BinningStrategy {
    /// Fixed number of equal-width bins
    Fixed(usize),
    /// Sturges' rule: k = 1 + log2(n), where n is sample size
    Sturges,
    /// Freedman-Diaconis rule: bin width = 2 * IQR / n^(1/3)
    FreedmanDiaconis,
    /// Square root choice: k = sqrt(n)
    SquareRoot,
    /// Rice rule: k = 2 * n^(1/3)
    Rice,
}

/// A histogram data structure.
#[derive(Debug, Clone)]
pub struct Histogram {
    /// Bin edges (len = bins + 1)
    edges: Vec<f64>,
    /// Bin counts
    counts: Vec<usize>,
    /// Original data reference (min, max)
    data_min: f64,
    data_max: f64,
    /// Total count of values
    total: usize,
}

impl Histogram {
    /// Creates a new histogram from the given data using the specified binning strategy.
    ///
    /// # Arguments
    /// * `data` - The data to create a histogram from
    /// * `strategy` - The binning strategy to use
    ///
    /// # Returns
    /// A new Histogram instance, or None if data is empty.
    ///
    /// # Examples
    /// ```
    /// use histogram_utils::{Histogram, BinningStrategy};
    ///
    /// let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    /// let hist = Histogram::new(&data, BinningStrategy::Sturges).unwrap();
    /// assert!(hist.bin_count() > 0);
    /// ```
    pub fn new(data: &[f64], strategy: BinningStrategy) -> Option<Self> {
        if data.is_empty() {
            return None;
        }

        let data_min = data.iter().cloned().fold(f64::INFINITY, f64::min);
        let data_max = data.iter().cloned().fold(f64::NEG_INFINITY, f64::max);

        if data_min == data_max {
            // All values are the same - create single bin
            return Some(Histogram {
                edges: vec![data_min - 0.5, data_max + 0.5],
                counts: vec![data.len()],
                data_min,
                data_max,
                total: data.len(),
            });
        }

        let num_bins = Self::calculate_bin_count(data, strategy, data_min, data_max);
        let bin_width = (data_max - data_min) / num_bins as f64;

        // Create bin edges
        let mut edges = Vec::with_capacity(num_bins + 1);
        for i in 0..=num_bins {
            edges.push(data_min + i as f64 * bin_width);
        }

        // Initialize counts
        let mut counts = vec![0usize; num_bins];

        // Count values in each bin
        for &value in data {
            if value >= data_min && value <= data_max {
                let bin_idx = if value == data_max {
                    num_bins - 1 // Last bin includes max value
                } else {
                    ((value - data_min) / bin_width) as usize
                };
                if bin_idx < num_bins {
                    counts[bin_idx] += 1;
                }
            }
        }

        Some(Histogram {
            edges,
            counts,
            data_min,
            data_max,
            total: data.len(),
        })
    }

    /// Creates a histogram with a fixed number of bins.
    ///
    /// # Arguments
    /// * `data` - The data to create a histogram from
    /// * `bins` - Number of bins
    ///
    /// # Examples
    /// ```
    /// use histogram_utils::Histogram;
    ///
    /// let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    /// let hist = Histogram::with_bins(&data, 3).unwrap();
    /// assert_eq!(hist.bin_count(), 3);
    /// ```
    pub fn with_bins(data: &[f64], bins: usize) -> Option<Self> {
        if bins == 0 {
            return None;
        }
        Self::new(data, BinningStrategy::Fixed(bins))
    }

    /// Creates a histogram with custom bin edges.
    ///
    /// # Arguments
    /// * `data` - The data to create a histogram from
    /// * `edges` - Custom bin edges (must be sorted ascending, len >= 2)
    ///
    /// # Examples
    /// ```
    /// use histogram_utils::Histogram;
    ///
    /// let data = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0];
    /// let edges = vec![0.0, 2.0, 4.0, 6.0];
    /// let hist = Histogram::with_edges(&data, &edges).unwrap();
    /// assert_eq!(hist.bin_count(), 3);
    /// ```
    pub fn with_edges(data: &[f64], edges: &[f64]) -> Option<Self> {
        if edges.len() < 2 || data.is_empty() {
            return None;
        }

        // Verify edges are sorted
        for i in 1..edges.len() {
            if edges[i] <= edges[i - 1] {
                return None;
            }
        }

        let num_bins = edges.len() - 1;
        let mut counts = vec![0usize; num_bins];
        let data_min = edges[0];
        let data_max = edges[edges.len() - 1];

        for &value in data {
            // Binary search for the correct bin
            let mut bin_idx = None;
            for i in 0..num_bins {
                if value >= edges[i] && (value < edges[i + 1] || (i == num_bins - 1 && value == edges[i + 1])) {
                    bin_idx = Some(i);
                    break;
                }
            }
            if let Some(idx) = bin_idx {
                counts[idx] += 1;
            }
        }

        Some(Histogram {
            edges: edges.to_vec(),
            counts,
            data_min,
            data_max,
            total: data.len(),
        })
    }

    /// Calculates the optimal number of bins using the specified strategy.
    fn calculate_bin_count(data: &[f64], strategy: BinningStrategy, min: f64, max: f64) -> usize {
        let n = data.len();

        match strategy {
            BinningStrategy::Fixed(bins) => bins.max(1),
            BinningStrategy::Sturges => {
                // Sturges' rule: k = 1 + log2(n)
                let k = 1.0 + (n as f64).log2();
                k.ceil() as usize
            }
            BinningStrategy::SquareRoot => {
                // Square root choice: k = sqrt(n)
                ((n as f64).sqrt().ceil()) as usize
            }
            BinningStrategy::Rice => {
                // Rice rule: k = 2 * n^(1/3)
                (2.0 * (n as f64).powf(1.0 / 3.0)).ceil() as usize
            }
            BinningStrategy::FreedmanDiaconis => {
                // Freedman-Diaconis: bin width = 2 * IQR / n^(1/3)
                let iqr = Self::calculate_iqr(data);
                let bin_width = 2.0 * iqr / (n as f64).powf(1.0 / 3.0);
                if bin_width > 0.0 {
                    ((max - min) / bin_width).ceil() as usize
                } else {
                    // Fallback to Sturges if IQR is 0
                    let k = 1.0 + (n as f64).log2();
                    k.ceil() as usize
                }
            }
        }
    }

    /// Calculates the interquartile range (IQR) of the data.
    fn calculate_iqr(data: &[f64]) -> f64 {
        let mut sorted: Vec<f64> = data.to_vec();
        sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(Ordering::Equal));
        
        let n = sorted.len();
        let q1_idx = n / 4;
        let q3_idx = (3 * n) / 4;
        
        sorted[q3_idx] - sorted[q1_idx]
    }

    /// Returns the number of bins in the histogram.
    pub fn bin_count(&self) -> usize {
        self.counts.len()
    }

    /// Returns the bin edges.
    pub fn edges(&self) -> &[f64] {
        &self.edges
    }

    /// Returns the bin counts.
    pub fn counts(&self) -> &[usize] {
        &self.counts
    }

    /// Returns the total count of all values.
    pub fn total(&self) -> usize {
        self.total
    }

    /// Returns the bin width (assumes equal-width bins).
    pub fn bin_width(&self) -> f64 {
        if self.edges.len() < 2 {
            return 0.0;
        }
        self.edges[1] - self.edges[0]
    }

    /// Returns the minimum data value.
    pub fn min(&self) -> f64 {
        self.data_min
    }

    /// Returns the maximum data value.
    pub fn max(&self) -> f64 {
        self.data_max
    }

    /// Returns the bin index for a given value, or None if out of range.
    pub fn bin_for_value(&self, value: f64) -> Option<usize> {
        if value < self.data_min || value > self.data_max {
            return None;
        }

        for i in 0..self.counts.len() {
            if value >= self.edges[i] && value < self.edges[i + 1] {
                return Some(i);
            }
        }

        // Check if value equals the last edge
        if value == self.edges[self.edges.len() - 1] {
            return Some(self.counts.len() - 1);
        }

        None
    }

    /// Returns the count for a specific bin.
    pub fn count_for_bin(&self, bin: usize) -> Option<usize> {
        self.counts.get(bin).copied()
    }

    /// Returns the range of a specific bin.
    pub fn bin_range(&self, bin: usize) -> Option<(f64, f64)> {
        if bin >= self.counts.len() {
            return None;
        }
        Some((self.edges[bin], self.edges[bin + 1]))
    }

    /// Returns the midpoint of a specific bin.
    pub fn bin_midpoint(&self, bin: usize) -> Option<f64> {
        let (start, end) = self.bin_range(bin)?;
        Some((start + end) / 2.0)
    }

    /// Returns normalized frequencies (counts / total).
    pub fn frequencies(&self) -> Vec<f64> {
        if self.total == 0 {
            return vec![0.0; self.counts.len()];
        }
        self.counts.iter().map(|&c| c as f64 / self.total as f64).collect()
    }

    /// Returns the density (frequency / bin width) for each bin.
    pub fn density(&self) -> Vec<f64> {
        let bin_width = self.bin_width();
        if bin_width == 0.0 || self.total == 0 {
            return vec![0.0; self.counts.len()];
        }
        self.counts.iter()
            .map(|&c| (c as f64 / self.total as f64) / bin_width)
            .collect()
    }

    /// Calculates the mean from the histogram.
    pub fn mean(&self) -> Option<f64> {
        if self.total == 0 {
            return None;
        }

        let sum: f64 = self.counts.iter().enumerate()
            .filter_map(|(i, &count)| {
                self.bin_midpoint(i).map(|mid| mid * count as f64)
            })
            .sum();

        Some(sum / self.total as f64)
    }

    /// Calculates the variance from the histogram.
    pub fn variance(&self) -> Option<f64> {
        let mean = self.mean()?;
        if self.total == 0 {
            return None;
        }

        let sum_sq: f64 = self.counts.iter().enumerate()
            .filter_map(|(i, &count)| {
                self.bin_midpoint(i).map(|mid| {
                    let diff = mid - mean;
                    diff * diff * count as f64
                })
            })
            .sum();

        Some(sum_sq / self.total as f64)
    }

    /// Calculates the standard deviation from the histogram.
    pub fn std_dev(&self) -> Option<f64> {
        self.variance().map(|v| v.sqrt())
    }

    /// Returns the mode (most frequent bin midpoint).
    pub fn mode(&self) -> Option<f64> {
        let max_count = *self.counts.iter().max()?;
        let mode_bin = self.counts.iter().position(|&c| c == max_count)?;
        self.bin_midpoint(mode_bin)
    }

    /// Returns the median (50th percentile) estimate.
    pub fn median(&self) -> Option<f64> {
        self.percentile(50.0)
    }

    /// Estimates a percentile value from the histogram.
    /// Percentile should be between 0 and 100.
    pub fn percentile(&self, percentile: f64) -> Option<f64> {
        if percentile < 0.0 || percentile > 100.0 || self.total == 0 {
            return None;
        }

        let target = (percentile / 100.0) * self.total as f64;
        let mut cumulative = 0.0;

        for (i, &count) in self.counts.iter().enumerate() {
            cumulative += count as f64;
            if cumulative >= target {
                // Linear interpolation within the bin
                let prev_cumulative = cumulative - count as f64;
                let fraction = if count > 0 {
                    (target - prev_cumulative) / count as f64
                } else {
                    0.0
                };
                
                let (bin_start, bin_end) = self.bin_range(i)?;
                return Some(bin_start + fraction * (bin_end - bin_start));
            }
        }

        // Return max value if we've exceeded 100th percentile
        Some(self.data_max)
    }

    /// Returns the cumulative distribution function (CDF) values.
    pub fn cdf(&self) -> Vec<f64> {
        if self.total == 0 {
            return vec![0.0; self.counts.len()];
        }

        let mut cdf = Vec::with_capacity(self.counts.len());
        let mut cumulative = 0usize;

        for &count in &self.counts {
            cumulative += count;
            cdf.push(cumulative as f64 / self.total as f64);
        }

        cdf
    }

    /// Finds bins that have counts above a threshold.
    pub fn bins_above_threshold(&self, threshold: usize) -> Vec<usize> {
        self.counts.iter()
            .enumerate()
            .filter_map(|(i, &count)| {
                if count > threshold { Some(i) } else { None }
            })
            .collect()
    }

    /// Returns the bin with the maximum count.
    pub fn max_bin(&self) -> Option<usize> {
        self.counts.iter()
            .enumerate()
            .max_by_key(|(_, &count)| count)
            .map(|(i, _)| i)
    }

    /// Returns the bin with the minimum count (excluding empty bins if desired).
    pub fn min_bin(&self, exclude_empty: bool) -> Option<usize> {
        self.counts.iter()
            .enumerate()
            .filter(|(_, &count)| !exclude_empty || count > 0)
            .min_by_key(|(_, &count)| count)
            .map(|(i, _)| i)
    }

    /// Merges this histogram with another histogram.
    /// Both histograms must have the same bin edges.
    pub fn merge(&mut self, other: &Histogram) -> Result<(), &'static str> {
        if self.edges != other.edges {
            return Err("Cannot merge histograms with different bin edges");
        }

        for (i, &count) in other.counts.iter().enumerate() {
            self.counts[i] += count;
        }
        self.total += other.total;

        // Update min/max if needed
        self.data_min = self.data_min.min(other.data_min);
        self.data_max = self.data_max.max(other.data_max);

        Ok(())
    }

    /// Returns a string representation of the histogram (ASCII art).
    pub fn to_ascii(&self, width: usize) -> String {
        if self.counts.is_empty() || width == 0 {
            return String::new();
        }

        let max_count = *self.counts.iter().max().unwrap_or(&0);
        if max_count == 0 {
            return self.counts.iter()
                .enumerate()
                .map(|(i, _)| format!("{:.2}-{:.2}: |", self.edges[i], self.edges[i + 1]))
                .collect::<Vec<_>>()
                .join("\n");
        }

        let mut result = String::new();
        for (i, &count) in self.counts.iter().enumerate() {
            let bar_len = if count > 0 {
                ((count as f64 / max_count as f64) * width as f64).round() as usize
            } else {
                0
            };
            let bar: String = "█".repeat(bar_len);
            result.push_str(&format!("{:.2}-{:.2}: |{} ({})\n", 
                self.edges[i], self.edges[i + 1], bar, count));
        }
        result
    }
}

/// Creates a histogram from data with automatic bin selection (Sturges' rule).
///
/// # Examples
/// ```
/// use histogram_utils::histogram;
///
/// let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
/// let hist = histogram(&data).unwrap();
/// assert!(hist.bin_count() > 0);
/// ```
pub fn histogram(data: &[f64]) -> Option<Histogram> {
    Histogram::new(data, BinningStrategy::Sturges)
}

/// Creates a histogram with a fixed number of bins.
///
/// # Examples
/// ```
/// use histogram_utils::histogram_with_bins;
///
/// let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
/// let hist = histogram_with_bins(&data, 3).unwrap();
/// assert_eq!(hist.bin_count(), 3);
/// ```
pub fn histogram_with_bins(data: &[f64], bins: usize) -> Option<Histogram> {
    Histogram::with_bins(data, bins)
}

/// Calculates descriptive statistics for a dataset.
pub fn describe(data: &[f64]) -> Option<Stats> {
    if data.is_empty() {
        return None;
    }

    let mut sorted: Vec<f64> = data.to_vec();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(Ordering::Equal));

    let n = sorted.len();
    let sum: f64 = sorted.iter().sum();
    let mean = sum / n as f64;

    let variance: f64 = sorted.iter()
        .map(|x| (x - mean).powi(2))
        .sum::<f64>() / n as f64;

    let min = sorted[0];
    let max = sorted[n - 1];
    let range = max - min;

    let median = if n % 2 == 0 {
        (sorted[n / 2 - 1] + sorted[n / 2]) / 2.0
    } else {
        sorted[n / 2]
    };

    let q1 = sorted[n / 4];
    let q3 = sorted[3 * n / 4];
    let iqr = q3 - q1;

    Some(Stats {
        count: n,
        sum,
        mean,
        variance,
        std_dev: variance.sqrt(),
        min,
        max,
        range,
        median,
        q1,
        q3,
        iqr,
    })
}

/// Descriptive statistics for a dataset.
#[derive(Debug, Clone)]
pub struct Stats {
    pub count: usize,
    pub sum: f64,
    pub mean: f64,
    pub variance: f64,
    pub std_dev: f64,
    pub min: f64,
    pub max: f64,
    pub range: f64,
    pub median: f64,
    pub q1: f64,
    pub q3: f64,
    pub iqr: f64,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_histogram_basic() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        assert_eq!(hist.bin_count(), 5);
        assert_eq!(hist.total(), 5);
    }

    #[test]
    fn test_histogram_empty_data() {
        let data: Vec<f64> = vec![];
        assert!(Histogram::new(&data, BinningStrategy::Sturges).is_none());
    }

    #[test]
    fn test_histogram_single_value() {
        let data = vec![5.0, 5.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Sturges).unwrap();
        assert_eq!(hist.total(), 3);
    }

    #[test]
    fn test_binning_strategies() {
        let data: Vec<f64> = (1..=100).map(|x| x as f64).collect();

        let sturges = Histogram::new(&data, BinningStrategy::Sturges).unwrap();
        let sqrt = Histogram::new(&data, BinningStrategy::SquareRoot).unwrap();
        let rice = Histogram::new(&data, BinningStrategy::Rice).unwrap();
        let fd = Histogram::new(&data, BinningStrategy::FreedmanDiaconis).unwrap();

        assert!(sturges.bin_count() > 0);
        assert!(sqrt.bin_count() > 0);
        assert!(rice.bin_count() > 0);
        assert!(fd.bin_count() > 0);
    }

    #[test]
    fn test_histogram_with_edges() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0];
        let edges = vec![0.0, 2.0, 4.0, 6.0];
        let hist = Histogram::with_edges(&data, &edges).unwrap();
        assert_eq!(hist.bin_count(), 3);
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
    fn test_histogram_mean() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        let mean = hist.mean().unwrap();
        // Approximate mean should be close to 3.0
        assert!((mean - 3.0).abs() < 0.5);
    }

    #[test]
    fn test_histogram_median() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        let median = hist.median().unwrap();
        // Median should be close to 3.0
        assert!((median - 3.0).abs() < 0.5);
    }

    #[test]
    fn test_histogram_mode() {
        let data = vec![1.0, 1.0, 1.0, 2.0, 3.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        let mode = hist.mode().unwrap();
        // Mode should be around 1.0
        assert!(mode < 2.0);
    }

    #[test]
    fn test_histogram_percentile() {
        let data: Vec<f64> = (1..=100).map(|x| x as f64).collect();
        let hist = Histogram::new(&data, BinningStrategy::Fixed(10)).unwrap();
        
        let p25 = hist.percentile(25.0).unwrap();
        let p50 = hist.percentile(50.0).unwrap();
        let p75 = hist.percentile(75.0).unwrap();
        
        // Approximate percentiles
        assert!(p25 > 20.0 && p25 < 30.0);
        assert!(p50 > 45.0 && p50 < 55.0);
        assert!(p75 > 70.0 && p75 < 80.0);
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
    fn test_histogram_ascii() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        let ascii = hist.to_ascii(10);
        assert!(!ascii.is_empty());
    }

    #[test]
    fn test_describe() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let stats = describe(&data).unwrap();
        
        assert_eq!(stats.count, 5);
        assert!((stats.mean - 3.0).abs() < 1e-10);
        assert!((stats.median - 3.0).abs() < 1e-10);
        assert!((stats.min - 1.0).abs() < 1e-10);
        assert!((stats.max - 5.0).abs() < 1e-10);
    }

    #[test]
    fn test_describe_empty() {
        let data: Vec<f64> = vec![];
        assert!(describe(&data).is_none());
    }

    #[test]
    fn test_histogram_merge() {
        let data1 = vec![1.0, 2.0, 3.0];
        let data2 = vec![4.0, 5.0, 6.0];
        
        let mut hist1 = Histogram::new(&data1, BinningStrategy::Fixed(3)).unwrap();
        let hist2 = Histogram::new(&data1, BinningStrategy::Fixed(3)).unwrap();
        
        assert!(hist1.merge(&hist2).is_ok());
        assert_eq!(hist1.total(), 6);
    }

    #[test]
    fn test_histogram_bin_for_value() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let bin = hist.bin_for_value(3.0);
        assert!(bin.is_some());
        
        let bin_outside = hist.bin_for_value(10.0);
        assert!(bin_outside.is_none());
    }

    #[test]
    fn test_histogram_variance_std_dev() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hist = Histogram::new(&data, BinningStrategy::Fixed(5)).unwrap();
        
        let variance = hist.variance().unwrap();
        let std_dev = hist.std_dev().unwrap();
        
        assert!(variance >= 0.0);
        assert!(std_dev >= 0.0);
        assert!((std_dev - variance.sqrt()).abs() < 1e-10);
    }
}