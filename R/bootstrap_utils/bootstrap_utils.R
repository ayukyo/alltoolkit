# Bootstrap Utilities for R
# Statistical bootstrap methods for resampling and inference
# Zero external dependencies - pure R implementation

#' Generate bootstrap samples
#' 
#' @param data Numeric vector to bootstrap
#' @param n_samples Number of bootstrap samples to generate
#' @param seed Optional random seed for reproducibility
#' @return Matrix where each column is a bootstrap sample
generate_bootstrap_samples <- function(data, n_samples = 1000, seed = NULL) {
  if (!is.numeric(data)) {
    stop("Data must be numeric")
  }
  if (length(data) == 0) {
    stop("Data cannot be empty")
  }
  if (!is.numeric(n_samples) || n_samples < 1) {
    stop("n_samples must be a positive integer")
  }
  
  if (!is.null(seed)) {
    set.seed(seed)
  }
  
  n <- length(data)
  samples <- matrix(nrow = n, ncol = n_samples)
  
  for (i in 1:n_samples) {
    samples[, i] <- sample(data, size = n, replace = TRUE)
  }
  
  samples
}

#' Bootstrap confidence interval
#' 
#' @param data Numeric vector
#' @param statistic Function to compute statistic (default: mean)
#' @param n_samples Number of bootstrap samples
#' @param confidence Confidence level (default: 0.95)
#' @param method CI method: "percentile", "basic", "bca", "normal"
#' @param seed Optional random seed
#' @return List with estimate, lower, upper, and se
bootstrap_ci <- function(data, 
                         statistic = mean,
                         n_samples = 1000,
                         confidence = 0.95,
                         method = "percentile",
                         seed = NULL) {
  if (!is.numeric(data) || length(data) == 0) {
    stop("Data must be a non-empty numeric vector")
  }
  if (confidence <= 0 || confidence >= 1) {
    stop("Confidence must be between 0 and 1")
  }
  
  if (!is.null(seed)) {
    set.seed(seed)
  }
  
  # Generate bootstrap statistics
  n <- length(data)
  boot_stats <- numeric(n_samples)
  jackknife_stats <- numeric(n)
  
  for (i in 1:n_samples) {
    sample_i <- sample(data, size = n, replace = TRUE)
    boot_stats[i] <- statistic(sample_i)
  }
  
  # Original statistic
  original_stat <- statistic(data)
  
  # Standard error
  se <- sd(boot_stats)
  
  # Compute CI based on method
  alpha <- 1 - confidence
  
  if (method == "percentile") {
    lower <- quantile(boot_stats, alpha / 2)
    upper <- quantile(boot_stats, 1 - alpha / 2)
  } else if (method == "basic") {
    lower <- 2 * original_stat - quantile(boot_stats, 1 - alpha / 2)
    upper <- 2 * original_stat - quantile(boot_stats, alpha / 2)
  } else if (method == "normal") {
    z <- qnorm(1 - alpha / 2)
    lower <- original_stat - z * se
    upper <- original_stat + z * se
  } else if (method == "bca") {
    # BCa (Bias-Corrected and Accelerated) method
    # Compute bias correction factor
    prop_less <- mean(boot_stats < original_stat)
    z0 <- qnorm(prop_less)
    
    # Compute acceleration factor using jackknife
    for (j in 1:n) {
      jackknife_stats[j] <- statistic(data[-j])
    }
    jack_mean <- mean(jackknife_stats)
    num <- sum((jack_mean - jackknife_stats)^3)
    denom <- 6 * (sum((jack_mean - jackknife_stats)^2))^1.5
    a <- if (denom != 0) num / denom else 0
    
    # Adjusted percentiles
    z_alpha <- qnorm(c(alpha / 2, 1 - alpha / 2))
    
    adjusted <- pnorm(z0 + (z0 + z_alpha) / (1 - a * (z0 + z_alpha)))
    
    lower <- quantile(boot_stats, adjusted[1])
    upper <- quantile(boot_stats, adjusted[2])
  } else {
    stop("Method must be 'percentile', 'basic', 'bca', or 'normal'")
  }
  
  list(
    estimate = original_stat,
    lower = as.numeric(lower),
    upper = as.numeric(upper),
    se = se,
    method = method,
    confidence = confidence,
    n_samples = n_samples
  )
}

#' Bootstrap hypothesis test
#' 
#' @param data Numeric vector
#' @param null_value Null hypothesis value
#' @param statistic Function to compute statistic (default: mean)
#' @param n_samples Number of bootstrap samples
#' @param alternative "two.sided", "less", or "greater"
#' @param seed Optional random seed
#' @return List with statistic, p_value, and decision
bootstrap_test <- function(data,
                            null_value = 0,
                            statistic = mean,
                            n_samples = 1000,
                            alternative = "two.sided",
                            seed = NULL) {
  if (!is.numeric(data) || length(data) == 0) {
    stop("Data must be a non-empty numeric vector")
  }
  if (!alternative %in% c("two.sided", "less", "greater")) {
    stop("Alternative must be 'two.sided', 'less', or 'greater'")
  }
  
  if (!is.null(seed)) {
    set.seed(seed)
  }
  
  # Center data under null hypothesis
  centered_data <- data - statistic(data) + null_value
  
  # Bootstrap from centered data
  n <- length(data)
  boot_stats <- numeric(n_samples)
  
  for (i in 1:n_samples) {
    sample_i <- sample(centered_data, size = n, replace = TRUE)
    boot_stats[i] <- statistic(sample_i)
  }
  
  # Original statistic
  observed_stat <- statistic(data)
  
  # Compute p-value
  if (alternative == "two.sided") {
    p_value <- mean(abs(boot_stats - null_value) >= abs(observed_stat - null_value))
  } else if (alternative == "less") {
    p_value <- mean(boot_stats <= observed_stat)
  } else {
    p_value <- mean(boot_stats >= observed_stat)
  }
  
  # Ensure p-value is not 0 (minimum 1/n_samples)
  p_value <- max(p_value, 1 / n_samples)
  
  list(
    statistic = observed_stat,
    null_value = null_value,
    p_value = p_value,
    alternative = alternative,
    n_samples = n_samples,
    reject_h0 = p_value < 0.05
  )
}

#' Two-sample bootstrap test
#' 
#' @param x First sample
#' @param y Second sample
#' @param statistic Function comparing two samples (default: difference of means)
#' @param n_samples Number of bootstrap samples
#' @param seed Optional random seed
#' @return List with statistic, p_value, and ci
bootstrap_two_sample <- function(x, 
                                  y,
                                  statistic = function(a, b) mean(a) - mean(b),
                                  n_samples = 1000,
                                  seed = NULL) {
  if (!is.numeric(x) || !is.numeric(y) || length(x) == 0 || length(y) == 0) {
    stop("Both samples must be non-empty numeric vectors")
  }
  
  if (!is.null(seed)) {
    set.seed(seed)
  }
  
  n_x <- length(x)
  n_y <- length(y)
  
  # Observed statistic
  observed_stat <- statistic(x, y)
  
  # Combined sample for permutation-style bootstrap
  combined <- c(x, y)
  
  boot_stats <- numeric(n_samples)
  
  for (i in 1:n_samples) {
    # Resample with replacement from combined
    sample_x <- sample(combined, size = n_x, replace = TRUE)
    sample_y <- sample(combined, size = n_y, replace = TRUE)
    boot_stats[i] <- statistic(sample_x, sample_y)
  }
  
  # P-value (two-sided)
  p_value <- mean(abs(boot_stats) >= abs(observed_stat))
  p_value <- max(p_value, 1 / n_samples)
  
  # CI
  ci <- quantile(boot_stats, c(0.025, 0.975))
  
  list(
    statistic = observed_stat,
    p_value = p_value,
    ci_lower = as.numeric(ci[1]),
    ci_upper = as.numeric(ci[2]),
    n_samples = n_samples
  )
}

#' Bootstrap estimate of standard error
#' 
#' @param data Numeric vector
#' @param statistic Function to compute statistic
#' @param n_samples Number of bootstrap samples
#' @param seed Optional random seed
#' @return Bootstrap standard error
bootstrap_se <- function(data, statistic = mean, n_samples = 1000, seed = NULL) {
  if (!is.null(seed)) {
    set.seed(seed)
  }
  
  n <- length(data)
  boot_stats <- numeric(n_samples)
  
  for (i in 1:n_samples) {
    sample_i <- sample(data, size = n, replace = TRUE)
    boot_stats[i] <- statistic(sample_i)
  }
  
  sd(boot_stats)
}

#' Bootstrap estimate of bias
#' 
#' @param data Numeric vector
#' @param statistic Function to compute statistic
#' @param n_samples Number of bootstrap samples
#' @param seed Optional random seed
#' @return Bootstrap bias estimate
bootstrap_bias <- function(data, statistic = mean, n_samples = 1000, seed = NULL) {
  if (!is.null(seed)) {
    set.seed(seed)
  }
  
  n <- length(data)
  original_stat <- statistic(data)
  boot_stats <- numeric(n_samples)
  
  for (i in 1:n_samples) {
    sample_i <- sample(data, size = n, replace = TRUE)
    boot_stats[i] <- statistic(sample_i)
  }
  
  mean(boot_stats) - original_stat
}

#' Stratified bootstrap
#' 
#' @param data Data frame with stratification column
#' @param strata_col Name of stratification column
#' @param statistic Function to compute statistic (receives data frame)
#' @param n_samples Number of bootstrap samples
#' @param seed Optional random seed
#' @return Vector of bootstrap statistics
stratified_bootstrap <- function(data,
                                  strata_col,
                                  statistic,
                                  n_samples = 1000,
                                  seed = NULL) {
  if (!is.data.frame(data)) {
    stop("Data must be a data frame")
  }
  if (!strata_col %in% names(data)) {
    stop("Strata column not found in data")
  }
  
  if (!is.null(seed)) {
    set.seed(seed)
  }
  
  strata <- data[[strata_col]]
  strata_levels <- unique(strata)
  
  boot_stats <- numeric(n_samples)
  
  for (i in 1:n_samples) {
    # Resample within each stratum
    boot_data <- do.call(rbind, lapply(strata_levels, function(level) {
      stratum_data <- data[strata == level, ]
      n_stratum <- nrow(stratum_data)
      stratum_data[sample(1:n_stratum, n_stratum, replace = TRUE), ]
    }))
    boot_stats[i] <- statistic(boot_data)
  }
  
  boot_stats
}

#' Block bootstrap for time series
#' 
#' @param data Time series data
#' @param block_size Size of blocks
#' @param statistic Function to compute statistic
#' @param n_samples Number of bootstrap samples
#' @param seed Optional random seed
#' @return Vector of bootstrap statistics
block_bootstrap <- function(data,
                             block_size,
                             statistic = mean,
                             n_samples = 1000,
                             seed = NULL) {
  if (!is.numeric(data) || length(data) == 0) {
    stop("Data must be a non-empty numeric vector")
  }
  if (block_size < 1 || block_size > length(data)) {
    stop("Block size must be between 1 and length of data")
  }
  
  if (!is.null(seed)) {
    set.seed(seed)
  }
  
  n <- length(data)
  n_blocks <- ceiling(n / block_size)
  
  boot_stats <- numeric(n_samples)
  
  for (i in 1:n_samples) {
    # Generate block indices
    block_starts <- sample(1:(n - block_size + 1), n_blocks, replace = TRUE)
    
    # Create bootstrap sample
    boot_sample <- numeric(n)
    for (j in 1:n_blocks) {
      start_idx <- (j - 1) * block_size + 1
      end_idx <- min(j * block_size, n)
      block_len <- end_idx - start_idx + 1
      boot_sample[start_idx:end_idx] <- data[block_starts[j]:(block_starts[j] + block_len - 1)]
    }
    
    boot_stats[i] <- statistic(boot_sample)
  }
  
  boot_stats
}

#' Bootstrap distribution summary
#' 
#' @param boot_stats Vector of bootstrap statistics
#' @param confidence Confidence level for CI
#' @return Summary statistics of bootstrap distribution
bootstrap_summary <- function(boot_stats, confidence = 0.95) {
  if (!is.numeric(boot_stats) || length(boot_stats) == 0) {
    stop("boot_stats must be a non-empty numeric vector")
  }
  
  alpha <- 1 - confidence
  
  list(
    mean = mean(boot_stats),
    median = median(boot_stats),
    sd = sd(boot_stats),
    se = sd(boot_stats) / sqrt(length(boot_stats)),
    ci_lower = as.numeric(quantile(boot_stats, alpha / 2)),
    ci_upper = as.numeric(quantile(boot_stats, 1 - alpha / 2)),
    skewness = sum((boot_stats - mean(boot_stats))^3) / 
               (length(boot_stats) * sd(boot_stats)^3),
    kurtosis = sum((boot_stats - mean(boot_stats))^4) / 
               (length(boot_stats) * sd(boot_stats)^4) - 3,
    n = length(boot_stats)
  )
}

#' Parametric bootstrap
#' 
#' @param data Numeric vector
#' @param statistic Function to compute statistic
#' @param fit_dist Function to fit distribution (returns parameters)
#' @param sample_dist Function to sample from fitted distribution
#' @param n_samples Number of bootstrap samples
#' @param seed Optional random seed
#' @return Vector of bootstrap statistics
parametric_bootstrap <- function(data,
                                  statistic = mean,
                                  fit_dist = function(d) list(mean = mean(d), sd = sd(d)),
                                  sample_dist = function(params, n) rnorm(n, params$mean, params$sd),
                                  n_samples = 1000,
                                  seed = NULL) {
  if (!is.numeric(data) || length(data) == 0) {
    stop("Data must be a non-empty numeric vector")
  }
  
  if (!is.null(seed)) {
    set.seed(seed)
  }
  
  n <- length(data)
  params <- fit_dist(data)
  
  boot_stats <- numeric(n_samples)
  
  for (i in 1:n_samples) {
    sample_i <- sample_dist(params, n)
    boot_stats[i] <- statistic(sample_i)
  }
  
  boot_stats
}

#' Jackknife resampling
#' 
#' @param data Numeric vector
#' @param statistic Function to compute statistic
#' @return List with jackknife estimates and pseudo-values
jackknife <- function(data, statistic = mean) {
  if (!is.numeric(data) || length(data) == 0) {
    stop("Data must be a non-empty numeric vector")
  }
  
  n <- length(data)
  jack_stats <- numeric(n)
  
  for (i in 1:n) {
    jack_stats[i] <- statistic(data[-i])
  }
  
  original_stat <- statistic(data)
  
  # Pseudo-values
  pseudo_values <- n * original_stat - (n - 1) * jack_stats
  
  # Jackknife estimate
  jack_estimate <- mean(pseudo_values)
  
  # Standard error
  jack_se <- sd(pseudo_values) / sqrt(n)
  
  # Bias
  bias <- (n - 1) * (mean(jack_stats) - original_stat)
  
  list(
    original = original_stat,
    jackknife_estimate = jack_estimate,
    bias = bias,
    se = jack_se,
    jackknife_statistics = jack_stats,
    pseudo_values = pseudo_values
  )
}

#' Bootstrap for regression coefficients
#' 
#' @param formula Regression formula
#' @param data Data frame
#' @param n_samples Number of bootstrap samples
#' @param seed Optional random seed
#' @return Matrix of bootstrap coefficient estimates
bootstrap_regression <- function(formula, data, n_samples = 1000, seed = NULL) {
  if (!is.data.frame(data)) {
    stop("Data must be a data frame")
  }
  
  if (!is.null(seed)) {
    set.seed(seed)
  }
  
  n <- nrow(data)
  
  # Fit original model to get coefficient names
  original_model <- lm(formula, data = data)
  coef_names <- names(coef(original_model))
  n_coefs <- length(coef_names)
  
  boot_coefs <- matrix(nrow = n_samples, ncol = n_coefs)
  colnames(boot_coefs) <- coef_names
  
  for (i in 1:n_samples) {
    sample_idx <- sample(1:n, n, replace = TRUE)
    boot_data <- data[sample_idx, ]
    boot_model <- lm(formula, data = boot_data)
    boot_coefs[i, ] <- coef(boot_model)
  }
  
  # Summary for each coefficient
  summary_list <- lapply(1:n_coefs, function(j) {
    boot_vals <- boot_coefs[, j]
    list(
      name = coef_names[j],
      estimate = coef(original_model)[j],
      se = sd(boot_vals),
      ci_lower = quantile(boot_vals, 0.025),
      ci_upper = quantile(boot_vals, 0.975)
    )
  })
  names(summary_list) <- coef_names
  
  list(
    coefficients = boot_coefs,
    summary = summary_list,
    original_model = original_model
  )
}

#' Accelerated bootstrap (BCa) acceleration factor
#' 
#' @param data Numeric vector
#' @param statistic Function to compute statistic
#' @return Acceleration factor 'a'
compute_acceleration <- function(data, statistic = mean) {
  if (!is.numeric(data) || length(data) < 2) {
    stop("Data must be a numeric vector with at least 2 elements")
  }
  
  n <- length(data)
  jack_stats <- numeric(n)
  
  for (i in 1:n) {
    jack_stats[i] <- statistic(data[-i])
  }
  
  jack_mean <- mean(jack_stats)
  num <- sum((jack_mean - jack_stats)^3)
  denom <- 6 * (sum((jack_mean - jack_stats)^2))^1.5
  
  if (denom == 0) {
    return(0)
  }
  
  num / denom
}

#' Print bootstrap CI result
#' 
#' @param x Bootstrap CI result
#' @param ... Additional arguments (ignored)
print.bootstrap_ci <- function(x, ...) {
  cat("Bootstrap Confidence Interval\n")
  cat("-----------------------------\n")
  cat(sprintf("Method: %s\n", x$method))
  cat(sprintf("Confidence: %.1f%%\n", x$confidence * 100))
  cat(sprintf("Bootstrap samples: %d\n\n", x$n_samples))
  cat(sprintf("Estimate: %.6f\n", x$estimate))
  cat(sprintf("SE: %.6f\n", x$se))
  cat(sprintf("95%% CI: [%.6f, %.6f]\n", x$lower, x$upper))
  invisible(x)
}