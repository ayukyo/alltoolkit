#!/usr/bin/env Rscript
# stats_utils/mod.R - Statistical Utilities Module for R
#
# A comprehensive statistical utility module providing common statistical
# calculations, distributions, and data analysis functions with zero dependencies.
#
# Author: AllToolkit
# Version: 1.0.0
# License: MIT

# ============================================================================
# Module Metadata
# ============================================================================

STATS_UTILS_VERSION <- "1.0.0"
STATS_UTILS_AUTHOR <- "AllToolkit"

# ============================================================================
# Descriptive Statistics
# ============================================================================

#' Calculate Mean
#'
#' @param x A numeric vector
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The arithmetic mean
mean_value <- function(x, na.rm = TRUE) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (na.rm) {
    x <- x[!is.na(x)]
  }
  if (length(x) == 0) {
    return(NA_real_)
  }
  sum(x) / length(x)
}

#' Calculate Median
#'
#' @param x A numeric vector
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The median value
median_value <- function(x, na.rm = TRUE) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (na.rm) {
    x <- x[!is.na(x)]
  }
  n <- length(x)
  if (n == 0) {
    return(NA_real_)
  }
  sorted <- sort(x)
  if (n %% 2 == 1) {
    sorted[(n + 1) / 2]
  } else {
    (sorted[n / 2] + sorted[n / 2 + 1]) / 2
  }
}

#' Calculate Mode
#'
#' @param x A vector of any type
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The most frequent value(s)
mode_value <- function(x, na.rm = TRUE) {
  if (na.rm) {
    x <- x[!is.na(x)]
  }
  if (length(x) == 0) {
    return(NA)
  }
  ux <- unique(x)
  freq <- tabulate(match(x, ux))
  max_freq <- max(freq)
  ux[freq == max_freq]
}

#' Calculate Variance
#'
#' @param x A numeric vector
#' @param sample Logical, use sample variance (n-1)? Default: TRUE
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The variance
variance <- function(x, sample = TRUE, na.rm = TRUE) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (na.rm) {
    x <- x[!is.na(x)]
  }
  n <- length(x)
  if (n < 2) {
    return(NA_real_)
  }
  m <- mean_value(x, na.rm = FALSE)
  ss <- sum((x - m)^2)
  if (sample) {
    ss / (n - 1)
  } else {
    ss / n
  }
}

#' Calculate Standard Deviation
#'
#' @param x A numeric vector
#' @param sample Logical, use sample std dev (n-1)? Default: TRUE
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The standard deviation
std_dev <- function(x, sample = TRUE, na.rm = TRUE) {
  sqrt(variance(x, sample = sample, na.rm = na.rm))
}

#' Calculate Range
#'
#' @param x A numeric vector
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The range (max - min)
range_value <- function(x, na.rm = TRUE) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (na.rm) {
    x <- x[!is.na(x)]
  }
  if (length(x) == 0) {
    return(NA_real_)
  }
  max(x) - min(x)
}

#' Calculate Interquartile Range (IQR)
#'
#' @param x A numeric vector
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The IQR (Q3 - Q1)
iqr <- function(x, na.rm = TRUE) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (na.rm) {
    x <- x[!is.na(x)]
  }
  if (length(x) < 4) {
    return(NA_real_)
  }
  quantile_value(x, 0.75) - quantile_value(x, 0.25)
}

#' Calculate Quantile
#'
#' @param x A numeric vector
#' @param prob Probability level (0 to 1)
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The quantile value
quantile_value <- function(x, prob, na.rm = TRUE) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (prob < 0 || prob > 1) {
    stop("Probability must be between 0 and 1")
  }
  if (na.rm) {
    x <- x[!is.na(x)]
  }
  n <- length(x)
  if (n == 0) {
    return(NA_real_)
  }
  sorted <- sort(x)
  index <- prob * (n - 1) + 1
  lower <- floor(index)
  upper <- ceiling(index)
  if (lower == upper) {
    sorted[lower]
  } else {
    sorted[lower] + (index - lower) * (sorted[upper] - sorted[lower])
  }
}

#' Calculate Summary Statistics
#'
#' @param x A numeric vector
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return A list with summary statistics
summary_stats <- function(x, na.rm = TRUE) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (na.rm) {
    x <- x[!is.na(x)]
  }
  n <- length(x)
  if (n == 0) {
    return(list(
      n = 0,
      mean = NA_real_,
      median = NA_real_,
      sd = NA_real_,
      min = NA_real_,
      max = NA_real_,
      q1 = NA_real_,
      q3 = NA_real_
    ))
  }
  list(
    n = n,
    mean = mean_value(x, na.rm = FALSE),
    median = median_value(x, na.rm = FALSE),
    sd = std_dev(x, na.rm = FALSE),
    min = min(x),
    max = max(x),
    q1 = quantile_value(x, 0.25, na.rm = FALSE),
    q3 = quantile_value(x, 0.75, na.rm = FALSE)
  )
}

# ============================================================================
# Distribution Functions
# ============================================================================

#' Calculate Z-Score
#'
#' @param x A numeric vector or single value
#' @param mean The mean of the distribution
#' @param sd The standard deviation of the distribution
#' @return The z-score(s)
z_score <- function(x, mean = NULL, sd = NULL) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (is.null(mean)) {
    mean <- mean_value(x)
  }
  if (is.null(sd)) {
    sd <- std_dev(x)
  }
  if (sd == 0) {
    return(rep(Inf, length(x)))
  }
  (x - mean) / sd
}

#' Normal Probability Density Function
#'
#' @param x The value(s) to evaluate
#' @param mean The mean of the distribution (default: 0)
#' @param sd The standard deviation (default: 1)
#' @return The PDF value(s)
dnorm_approx <- function(x, mean = 0, sd = 1) {
  (1 / (sd * sqrt(2 * pi))) * exp(-0.5 * ((x - mean) / sd)^2)
}

#' Normal Cumulative Distribution Function (Approximation)
#'
#' @param x The value(s) to evaluate
#' @param mean The mean of the distribution (default: 0)
#' @param sd The standard deviation (default: 1)
#' @return The CDF value(s)
pnorm_approx <- function(x, mean = 0, sd = 1) {
  z <- (x - mean) / sd
  # Abramowitz and Stegun approximation
  b1 <- 0.319381530
  b2 <- -0.356563782
  b3 <- 1.781477937
  b4 <- -1.821255978
  b5 <- 1.330274429
  p <- 0.2316419
  c <- 0.39894228
  
  t <- 1 / (1 + p * abs(z))
  phi <- c * exp(-(z^2) / 2)
  y <- 1 - phi * t * (b1 + t * (b2 + t * (b3 + t * (b4 + t * b5))))
  
  result <- ifelse(z < 0, 1 - y, y)
  result
}

#' Generate Normal Random Numbers (Box-Muller Transform)
#'
#' @param n Number of random values to generate
#' @param mean The mean of the distribution (default: 0)
#' @param sd The standard deviation (default: 1)
#' @return A vector of random normal values
random_normal <- function(n, mean = 0, sd = 1) {
  if (n <= 0) {
    return(numeric(0))
  }
  n_pairs <- ceiling(n / 2)
  u1 <- runif(n_pairs)
  u2 <- runif(n_pairs)
  
  # Box-Muller transform
  z1 <- sqrt(-2 * log(u1)) * cos(2 * pi * u2)
  z2 <- sqrt(-2 * log(u1)) * sin(2 * pi * u2)
  
  result <- c(z1, z2)[1:n]
  mean + sd * result
}

#' Generate Uniform Random Numbers
#'
#' @param n Number of random values to generate
#' @param min Minimum value (default: 0)
#' @param max Maximum value (default: 1)
#' @return A vector of random uniform values
random_uniform <- function(n, min = 0, max = 1) {
  if (n <= 0) {
    return(numeric(0))
  }
  min + (max - min) * runif(n)
}

#' Generate Exponential Random Numbers
#'
#' @param n Number of random values to generate
#' @param rate The rate parameter (lambda)
#' @return A vector of random exponential values
random_exponential <- function(n, rate = 1) {
  if (n <= 0) {
    return(numeric(0))
  }
  if (rate <= 0) {
    stop("Rate must be positive")
  }
  -log(runif(n)) / rate
}

# ============================================================================
# Correlation and Regression
# ============================================================================

#' Calculate Covariance
#'
#' @param x First numeric vector
#' @param y Second numeric vector
#' @param sample Logical, use sample covariance (n-1)? Default: TRUE
#' @return The covariance
#'
covariance <- function(x, y, sample = TRUE) {
  if (!is.numeric(x) || !is.numeric(y)) {
    stop("Both inputs must be numeric")
  }
  if (length(x) != length(y)) {
    stop("Vectors must have the same length")
  }
  n <- length(x)
  if (n < 2) {
    return(NA_real_)
  }
  mx <- mean_value(x, na.rm = FALSE)
  my <- mean_value(y, na.rm = FALSE)
  ss <- sum((x - mx) * (y - my))
  if (sample) {
    ss / (n - 1)
  } else {
    ss / n
  }
}

#' Calculate Pearson Correlation Coefficient
#'
#' @param x First numeric vector
#' @param y Second numeric vector
#' @return The correlation coefficient (-1 to 1)
correlation <- function(x, y) {
  if (!is.numeric(x) || !is.numeric(y)) {
    stop("Both inputs must be numeric")
  }
  if (length(x) != length(y)) {
    stop("Vectors must have the same length")
  }
  n <- length(x)
  if (n < 2) {
    return(NA_real_)
  }
  sd_x <- std_dev(x, na.rm = FALSE)
  sd_y <- std_dev(y, na.rm = FALSE)
  if (sd_x == 0 || sd_y == 0) {
    return(NA_real_)
  }
  covariance(x, y, sample = TRUE) / (sd_x * sd_y)
}

#' Simple Linear Regression
#'
#' @param x Independent variable (numeric vector)
#' @param y Dependent variable (numeric vector)
#' @return A list with regression results
linear_regression <- function(x, y) {
  if (!is.numeric(x) || !is.numeric(y)) {
    stop("Both inputs must be numeric")
  }
  if (length(x) != length(y)) {
    stop("Vectors must have the same length")
  }
  n <- length(x)
  if (n < 2) {
    stop("Need at least 2 data points")
  }
  
  mx <- mean_value(x, na.rm = FALSE)
  my <- mean_value(y, na.rm = FALSE)
  
  ss_xy <- sum((x - mx) * (y - my))
  ss_xx <- sum((x - mx)^2)
  
  if (ss_xx == 0) {
    stop("x values must have some variation")
  }
  
  slope <- ss_xy / ss_xx
  intercept <- my - slope * mx
  
  # Calculate R-squared
  y_pred <- intercept + slope * x
  ss_tot <- sum((y - my)^2)
  ss_res <- sum((y - y_pred)^2)
  r_squared <- 1 - (ss_res / ss_tot)
  
  list(
    intercept = intercept,
    slope = slope,
    r_squared = r_squared,
    formula = paste0("y = ", round(intercept, 4), " + ", round(slope, 4), " * x"),
    predict = function(new_x) {
      intercept + slope * new_x
    }
  )
}

# ============================================================================
# Outlier Detection
# ============================================================================

#' Detect Outliers using IQR Method
#'
#' @param x A numeric vector
#' @param multiplier IQR multiplier (default: 1.5)
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return A logical vector indicating outliers
detect_outliers_iqr <- function(x, multiplier = 1.5, na.rm = TRUE) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (na.rm) {
    x <- x[!is.na(x)]
  }
  q1 <- quantile_value(x, 0.25, na.rm = FALSE)
  q3 <- quantile_value(x, 0.75, na.rm = FALSE)
  iqr_val <- q3 - q1
  lower_bound <- q1 - multiplier * iqr_val
  upper_bound <- q3 + multiplier * iqr_val
  x < lower_bound | x > upper_bound
}

#' Detect Outliers using Z-Score Method
#'
#' @param x A numeric vector
#' @param threshold Z-score threshold (default: 3)
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return A logical vector indicating outliers
detect_outliers_zscore <- function(x, threshold = 3, na.rm = TRUE) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (na.rm) {
    x <- x[!is.na(x)]
  }
  z <- z_score(x)
  abs(z) > threshold
}

#' Remove Outliers
#'
#' @param x A numeric vector
#' @param method Detection method ("iqr" or "zscore")
#' @param ... Additional arguments passed to detection function
#' @return Vector with outliers removed
remove_outliers <- function(x, method = "iqr", ...) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (method == "iqr") {
    outliers <- detect_outliers_iqr(x, ...)
  } else if (method == "zscore") {
    outliers <- detect_outliers_zscore(x, ...)
  } else {
    stop("Method must be 'iqr' or 'zscore'")
  }
  x[!outliers]
}

# ============================================================================
# Data Transformation
# ============================================================================

#' Min-Max Normalization
#'
#' @param x A numeric vector
#' @param new_min New minimum value (default: 0)
#' @param new_max New maximum value (default: 1)
#' @return Normalized vector
min_max_scale <- function(x, new_min = 0, new_max = 1) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  old_min <- min(x, na.rm = TRUE)
  old_max <- max(x, na.rm = TRUE)
  if (old_max == old_min) {
    return(rep(new_min, length(x)))
  }
  new_min + (x - old_min) * (new_max - new_min) / (old_max - old_min)
}

#' Z-Score Standardization
#'
#' @param x A numeric vector
#' @return Standardized vector
standardize <- function(x) {
  z_score(x)
}

#' Log Transform
#'
#' @param x A numeric vector
#' @param base Logarithm base (default: e)
#' @return Log-transformed vector
log_transform <- function(x, base = exp(1)) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (any(x <= 0, na.rm = TRUE)) {
    stop("All values must be positive for log transform")
  }
  log(x, base = base)
}

#' Box-Cox Transform (simplified)
#'
#' @param x A numeric vector
#' @param lambda Transformation parameter
#' @return Transformed vector
box_cox_transform <- function(x, lambda) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (any(x <= 0, na.rm = TRUE)) {
    stop("All values must be positive for Box-Cox transform")
  }
  if (abs(lambda) < 1e-10) {
    log(x)
  } else {
    (x^lambda - 1) / lambda
  }
}

# ============================================================================
# Statistical Tests
# ============================================================================

#' One-Sample T-Test
#'
#' @param x A numeric vector
#' @param mu Hypothesized mean (default: 0)
#' @return A list with test results
t_test_one_sample <- function(x, mu = 0) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  n <- length(x)
  if (n < 2) {
    stop("Need at least 2 observations")
  }
  x_mean <- mean_value(x, na.rm = FALSE)
  x_sd <- std_dev(x, na.rm = FALSE)
  se <- x_sd / sqrt(n)
  t_stat <- (x_mean - mu) / se
  df <- n - 1
  
  # Two-tailed p-value approximation
  p_value <- 2 * (1 - pnorm_approx(abs(t_stat)))
  
  list(
    statistic = t_stat,
    df = df,
    p_value = p_value,
    mean = x_mean,
    alternative = "two.sided",
    method = "One Sample t-test"
  )
}

#' Chi-Square Goodness of Fit Test
#'
#' @param observed Observed frequencies
#' @param expected Expected frequencies (default: equal)
#' @return A list with test results
chi_square_test <- function(observed, expected = NULL) {
  if (!is.numeric(observed)) {
    stop("Observed must be numeric")
  }
  if (any(observed < 0)) {
    stop("Frequencies must be non-negative")
  }
  
  if (is.null(expected)) {
    expected <- rep(sum(observed) / length(observed), length(observed))
  }
  
  if (length(observed) != length(expected)) {
    stop("Observed and expected must have same length")
  }
  
  chi_sq <- sum((observed - expected)^2 / expected)
  df <- length(observed) - 1
  
  list(
    statistic = chi_sq,
    df = df,
    p_value = NA,  # Would need more complex calculation
    method = "Chi-squared test"
  )
}

# ============================================================================
# Utility Functions
# ============================================================================

#' Calculate Percentile Rank
#'
#' @param x A numeric vector
#' @param value The value to find percentile for
#' @return The percentile rank (0 to 100)
percentile_rank <- function(x, value) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  x <- x[!is.na(x)]
  if (length(x) == 0) {
    return(NA_real_)
  }
  sum(x <= value) / length(x) * 100
}

#' Calculate Coefficient of Variation
#'
#' @param x A numeric vector
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The CV as a percentage
coefficient_of_variation <- function(x, na.rm = TRUE) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (na.rm) {
    x <- x[!is.na(x)]
  }
  m <- mean_value(x, na.rm = FALSE)
  if (m == 0) {
    return(Inf)
  }
  abs(std_dev(x, na.rm = FALSE) / m) * 100
}

#' Calculate Skewness
#'
#' @param x A numeric vector
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The skewness
skewness <- function(x, na.rm = TRUE) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (na.rm) {
    x <- x[!is.na(x)]
  }
  n <- length(x)
  if (n < 3) {
    return(NA_real_)
  }
  m <- mean_value(x, na.rm = FALSE)
  s <- std_dev(x, na.rm = FALSE)
  if (s == 0) {
    return(0)
  }
  n / ((n - 1) * (n - 2)) * sum(((x - m) / s)^3)
}

#' Calculate Kurtosis
#'
#' @param x A numeric vector
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The excess kurtosis
kurtosis <- function(x, na.rm = TRUE) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (na.rm) {
    x <- x[!is.na(x)]
  }
  n <- length(x)
  if (n < 4) {
    return(NA_real_)
  }
  m <- mean_value(x, na.rm = FALSE)
  s <- std_dev(x, na.rm = FALSE)
  if (s == 0) {
    return(0)
  }
  n * (n + 1) / ((n - 1) * (n - 2) * (n - 3)) * sum(((x - m) / s)^4) -
    3 * (n - 1)^2 / ((n - 2) * (n - 3))
}

#' Moving Average
#'
#' @param x A numeric vector
#' @param window Window size
#' @return Vector of moving averages
moving_average <- function(x, window) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (window <= 0 || window > length(x)) {
    stop("Invalid window size")
  }
  n <- length(x)
  result <- rep(NA_real_, n)
  for (i in window:n) {
    result[i] <- mean_value(x[(i - window + 1):i], na.rm = TRUE)
  }
  result
}

#' Calculate Confidence Interval
#'
#' @param x A numeric vector
#' @param confidence Confidence level (default: 0.95)
#' @return A list with lower and upper bounds
confidence_interval <- function(x, confidence = 0.95) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  n <- length(x[!is.na(x)])
  if (n < 2) {
    return(list(lower = NA_real_, upper = NA_real_, mean = NA_real_))
  }
  x_mean <- mean_value(x, na.rm = TRUE)
  x_sd <- std_dev(x, na.rm = TRUE)
  se <- x_sd / sqrt(n)
  
  # Approximate z-score for confidence level
  z <- qnorm_approx(1 - (1 - confidence) / 2)
  
  list(
    lower = x_mean - z * se,
    upper = x_mean + z * se,
    mean = x_mean
  )
}

#' Quantile-Quantile Normal
#'
#' @param x A numeric vector
#' @return A list with theoretical and sample quantiles
qq_normal <- function(x) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  x <- sort(x[!is.na(x)])
  n <- length(x)
  if (n < 2) {
    return(list(theoretical = numeric(0), sample = x))
  }
  
  # Calculate theoretical quantiles
  probs <- (1:n - 0.5) / n
  theoretical <- qnorm_approx(probs)
  
  list(
    theoretical = theoretical,
    sample = x
  )
}

#' Inverse Normal CDF (Approximation)
#'
#' @param p Probability (0 to 1)
#' @return The z-score
qnorm_approx <- function(p) {
  if (any(p <= 0 | p >= 1)) {
    stop("Probability must be between 0 and 1 (exclusive)")
  }
  
  # Beasley-Springer-Moro approximation
  a0 <- 2.50662823884
  a1 <- -18.61500062529
  a2 <- 41.39119773534
  a3 <- -25.44106049637
  
  b0 <- -8.47351093090
  b1 <- 23.08336743743
  b2 <- -21.06224101826
  b3 <- 3.13082909833
  
  c0 <- 0.3374754822726147
  c1 <- 0.9761690190917186
  c2 <- 0.1607979714918209
  c3 <- 0.0276438810333863
  c4 <- 0.0038405729373609
  c5 <- 0.0003951896511919
  c6 <- 0.0000321767881768
  c7 <- 0.0000002888167364
  c8 <- 0.0000003960315187
  
  result <- numeric(length(p))
  
  for (i in seq_along(p)) {
    if (p[i] < 0.5) {
      y <- p[i]
      sign <- -1
    } else {
      y <- 1 - p[i]
      sign <- 1
    }
    
    if (y < 0.08) {
      x <- log(-log(y))
      result[i] <- sign * (c0 + x * (c1 + x * (c2 + x * (c3 + x * (c4 + x * (c5 + x * (c6 + x * (c7 + x * c8)))))))
    } else {
      z <- sqrt(-2 * log(y))
      result[i] <- sign * (z - (a0 + z * (a1 + z * (a2 + z * a3))) / (1 + z * (b0 + z * (b1 + z * (b2 + z * b3)))))
    }
  }
  
  result
}

# ============================================================================
# Module Export
# ============================================================================

# Return module info when sourced
cat("R Stats Utils Module v", STATS_UTILS_VERSION, " loaded\n", sep = "")
cat("Author: ", STATS_UTILS_AUTHOR, "\n", sep = "")
