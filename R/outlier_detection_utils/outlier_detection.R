# Outlier Detection Utils
# A comprehensive toolkit for detecting outliers in data
# Zero external dependencies - uses only base R functions

# ============================================================================
# IQR Method (Interquartile Range)
# ============================================================================

#' Detect outliers using the IQR method
#' 
#' @param x Numeric vector
#' @param multiplier IQR multiplier (default 1.5, use 3 for extreme outliers)
#' @return List containing outliers, indices, and bounds
detect_outliers_iqr <- function(x, multiplier = 1.5) {
  if (!is.numeric(x)) {
    stop("Input must be a numeric vector")
  }
  
  x <- x[!is.na(x)]
  
  q1 <- quantile(x, 0.25)
  q3 <- quantile(x, 0.75)
  iqr <- q3 - q1
  
  lower_bound <- q1 - multiplier * iqr
  upper_bound <- q3 + multiplier * iqr
  
  outlier_indices <- which(x < lower_bound | x > upper_bound)
  outliers <- x[outlier_indices]
  
  list(
    method = "IQR",
    outliers = outliers,
    indices = outlier_indices,
    lower_bound = lower_bound,
    upper_bound = upper_bound,
    iqr = iqr,
    q1 = q1,
    q3 = q3,
    multiplier = multiplier,
    total_detected = length(outliers)
  )
}

# ============================================================================
# Z-Score Method
# ============================================================================

#' Detect outliers using the Z-score method
#' 
#' @param x Numeric vector
#' @param threshold Z-score threshold (default 3)
#' @return List containing outliers, indices, and statistics
detect_outliers_zscore <- function(x, threshold = 3) {
  if (!is.numeric(x)) {
    stop("Input must be a numeric vector")
  }
  
  x <- x[!is.na(x)]
  
  mean_val <- mean(x)
  sd_val <- sd(x)
  
  if (sd_val == 0) {
    warning("Standard deviation is zero, no outliers detected")
    return(list(
      method = "Z-Score",
      outliers = numeric(0),
      indices = integer(0),
      z_scores = rep(0, length(x)),
      threshold = threshold,
      mean = mean_val,
      sd = sd_val,
      total_detected = 0
    ))
  }
  
  z_scores <- (x - mean_val) / sd_val
  outlier_indices <- which(abs(z_scores) > threshold)
  outliers <- x[outlier_indices]
  
  list(
    method = "Z-Score",
    outliers = outliers,
    indices = outlier_indices,
    z_scores = z_scores,
    threshold = threshold,
    mean = mean_val,
    sd = sd_val,
    total_detected = length(outliers)
  )
}

# ============================================================================
# Modified Z-Score Method (Median Absolute Deviation)
# ============================================================================

#' Detect outliers using the Modified Z-score (MAD) method
#' More robust than standard Z-score for non-normal distributions
#' 
#' @param x Numeric vector
#' @param threshold Modified Z-score threshold (default 3.5)
#' @return List containing outliers, indices, and statistics
detect_outliers_mad <- function(x, threshold = 3.5) {
  if (!is.numeric(x)) {
    stop("Input must be a numeric vector")
  }
  
  x <- x[!is.na(x)]
  
  median_val <- median(x)
  mad_val <- median(abs(x - median_val))
  
  # Use constant for normal distribution consistency
  constant <- 1.4826
  
  if (mad_val == 0) {
    # Fall back to standard deviation-based approach if MAD is zero
    mad_val <- sd(x) / constant
    if (mad_val == 0) {
      warning("Both MAD and SD are zero, no outliers detected")
      return(list(
        method = "Modified Z-Score (MAD)",
        outliers = numeric(0),
        indices = integer(0),
        modified_z_scores = rep(0, length(x)),
        threshold = threshold,
        median = median_val,
        mad = 0,
        total_detected = 0
      ))
    }
  }
  
  modified_z_scores <- constant * (x - median_val) / mad_val
  outlier_indices <- which(abs(modified_z_scores) > threshold)
  outliers <- x[outlier_indices]
  
  list(
    method = "Modified Z-Score (MAD)",
    outliers = outliers,
    indices = outlier_indices,
    modified_z_scores = modified_z_scores,
    threshold = threshold,
    median = median_val,
    mad = mad_val,
    total_detected = length(outliers)
  )
}

# ============================================================================
# Percentile Method
# ============================================================================

#' Detect outliers using percentile method
#' 
#' @param x Numeric vector
#' @param lower_percentile Lower percentile threshold (default 1)
#' @param upper_percentile Upper percentile threshold (default 99)
#' @return List containing outliers, indices, and bounds
detect_outliers_percentile <- function(x, lower_percentile = 1, upper_percentile = 99) {
  if (!is.numeric(x)) {
    stop("Input must be a numeric vector")
  }
  
  x <- x[!is.na(x)]
  
  lower_bound <- quantile(x, lower_percentile / 100)
  upper_bound <- quantile(x, upper_percentile / 100)
  
  outlier_indices <- which(x < lower_bound | x > upper_bound)
  outliers <- x[outlier_indices]
  
  list(
    method = "Percentile",
    outliers = outliers,
    indices = outlier_indices,
    lower_bound = lower_bound,
    upper_bound = upper_bound,
    lower_percentile = lower_percentile,
    upper_percentile = upper_percentile,
    total_detected = length(outliers)
  )
}

# ============================================================================
# Tukey's Fences Method
# ============================================================================

#' Detect outliers using Tukey's fences (inner and outer)
#' 
#' @param x Numeric vector
#' @param fences Type of fences: "inner" (1.5*IQR) or "outer" (3*IQR)
#' @return List containing outliers, indices, and bounds
detect_outliers_tukey <- function(x, fences = c("inner", "outer")) {
  fences <- match.arg(fences)
  multiplier <- if (fences == "inner") 1.5 else 3
  
  result <- detect_outliers_iqr(x, multiplier)
  result$method <- paste("Tukey's", fences, "fences")
  result$fences_type <- fences
  
  result
}

# ============================================================================
# Grubbs' Test for Single Outlier
# ============================================================================

#' Perform Grubbs' test for a single outlier
#' 
#' @param x Numeric vector
#' @param alpha Significance level (default 0.05)
#' @return List containing test results
detect_outlier_grubbs <- function(x, alpha = 0.05) {
  if (!is.numeric(x)) {
    stop("Input must be a numeric vector")
  }
  
  x <- x[!is.na(x)]
  n <- length(x)
  
  if (n < 3) {
    stop("Grubbs' test requires at least 3 observations")
  }
  
  mean_val <- mean(x)
  sd_val <- sd(x)
  
  if (sd_val == 0) {
    warning("Standard deviation is zero, no outlier detected")
    return(list(
      method = "Grubbs' Test",
      is_outlier = FALSE,
      outlier_value = NA,
      outlier_index = NA,
      g_statistic = NA,
      critical_value = NA,
      p_value = NA,
      alpha = alpha
    ))
  }
  
  # Find the most extreme value
  deviations <- abs(x - mean_val)
  max_dev_index <- which.max(deviations)
  max_deviation <- deviations[max_dev_index]
  
  # Grubbs' statistic
  g_statistic <- max_deviation / sd_val
  
  # Critical value for Grubbs' test (two-sided)
  t_critical <- qt(1 - alpha / (2 * n), df = n - 2)
  critical_value <- ((n - 1) / sqrt(n)) * sqrt(t_critical^2 / (n - 2 + t_critical^2))
  
  is_outlier <- g_statistic > critical_value
  
  list(
    method = "Grubbs' Test",
    is_outlier = is_outlier,
    outlier_value = x[max_dev_index],
    outlier_index = max_dev_index,
    g_statistic = g_statistic,
    critical_value = critical_value,
    alpha = alpha,
    mean = mean_val,
    sd = sd_val
  )
}

# ============================================================================
# Dixon's Q Test for Small Samples
# ============================================================================

#' Perform Dixon's Q test for outlier detection in small samples
#' 
#' @param x Numeric vector (size 3-30)
#' @param alpha Significance level (default 0.05)
#' @return List containing test results
detect_outlier_dixon <- function(x, alpha = 0.05) {
  if (!is.numeric(x)) {
    stop("Input must be a numeric vector")
  }
  
  x <- x[!is.na(x)]
  n <- length(x)
  
  if (n < 3 || n > 30) {
    stop("Dixon's Q test requires sample size between 3 and 30")
  }
  
  x_sorted <- sort(x)
  
  # Calculate range
  data_range <- x_sorted[n] - x_sorted[1]
  
  if (data_range == 0) {
    warning("All values are identical, no outlier detected")
    return(list(
      method = "Dixon's Q Test",
      is_outlier = FALSE,
      outlier_value = NA,
      outlier_position = NA,
      q_statistic = NA,
      critical_value = NA,
      alpha = alpha
    ))
  }
  
  # Calculate Q for potential outliers at both ends
  q_low <- (x_sorted[2] - x_sorted[1]) / data_range
  q_high <- (x_sorted[n] - x_sorted[n-1]) / data_range
  
  # Critical values table for Dixon's Q test (alpha = 0.05)
  q_critical_table <- c(
    0.970, 0.829, 0.710, 0.625, 0.568,
    0.526, 0.493, 0.466, 0.444, 0.426,
    0.410, 0.396, 0.384, 0.374, 0.365,
    0.356, 0.349, 0.342, 0.337, 0.331,
    0.326, 0.321, 0.317, 0.312, 0.308,
    0.305, 0.301, 0.290
  )
  
  critical_value <- q_critical_table[n - 2]
  
  # Check both ends
  is_low_outlier <- q_low > critical_value
  is_high_outlier <- q_high > critical_value
  
  if (is_low_outlier && !is_high_outlier) {
    list(
      method = "Dixon's Q Test",
      is_outlier = TRUE,
      outlier_value = x_sorted[1],
      outlier_position = "low",
      q_statistic = q_low,
      critical_value = critical_value,
      alpha = alpha,
      sorted_data = x_sorted
    )
  } else if (is_high_outlier && !is_low_outlier) {
    list(
      method = "Dixon's Q Test",
      is_outlier = TRUE,
      outlier_value = x_sorted[n],
      outlier_position = "high",
      q_statistic = q_high,
      critical_value = critical_value,
      alpha = alpha,
      sorted_data = x_sorted
    )
  } else if (is_low_outlier && is_high_outlier) {
    # Both are outliers, pick the one with higher Q
    if (q_low > q_high) {
      list(
        method = "Dixon's Q Test",
        is_outlier = TRUE,
        outlier_value = x_sorted[1],
        outlier_position = "low",
        q_statistic = q_low,
        critical_value = critical_value,
        alpha = alpha,
        note = "Both ends exceed threshold; reporting lower outlier",
        sorted_data = x_sorted
      )
    } else {
      list(
        method = "Dixon's Q Test",
        is_outlier = TRUE,
        outlier_value = x_sorted[n],
        outlier_position = "high",
        q_statistic = q_high,
        critical_value = critical_value,
        alpha = alpha,
        note = "Both ends exceed threshold; reporting upper outlier",
        sorted_data = x_sorted
      )
    }
  } else {
    list(
      method = "Dixon's Q Test",
      is_outlier = FALSE,
      outlier_value = NA,
      outlier_position = NA,
      q_statistic = max(q_low, q_high),
      critical_value = critical_value,
      alpha = alpha,
      sorted_data = x_sorted
    )
  }
}

# ============================================================================
# Comprehensive Outlier Detection
# ============================================================================

#' Run all outlier detection methods and combine results
#' 
#' @param x Numeric vector
#' @param include_tests Whether to include statistical tests (default TRUE)
#' @return List containing results from all methods
detect_outliers_all <- function(x, include_tests = TRUE) {
  if (!is.numeric(x)) {
    stop("Input must be a numeric vector")
  }
  
  x_clean <- x[!is.na(x)]
  
  results <- list(
    iqr = detect_outliers_iqr(x_clean),
    iqr_extreme = detect_outliers_iqr(x_clean, multiplier = 3),
    zscore = detect_outliers_zscore(x_clean),
    mad = detect_outliers_mad(x_clean),
    percentile = detect_outliers_percentile(x_clean),
    tukey_inner = detect_outliers_tukey(x_clean, "inner"),
    tukey_outer = detect_outliers_tukey(x_clean, "outer")
  )
  
  if (include_tests && length(x_clean) >= 3) {
    if (length(x_clean) <= 30) {
      results$dixon <- detect_outlier_dixon(x_clean)
    }
    results$grubbs <- detect_outlier_grubbs(x_clean)
  }
  
  # Count votes for each point being an outlier
  outlier_counts <- table(unlist(lapply(
    results[grep("^(iqr|zscore|mad|percentile|tukey)", names(results))],
    function(r) r$indices
  )))
  
  # Points detected by multiple methods
  consensus_outliers <- as.numeric(names(outlier_counts[outlier_counts >= 3]))
  
  results$consensus <- list(
    outlier_indices = consensus_outliers,
    outlier_values = x_clean[consensus_outliers],
    detection_counts = outlier_counts,
    total_detected = length(consensus_outliers),
    threshold_methods = 3  # Detected by at least this many methods
  )
  
  results$summary <- data.frame(
    method = c("IQR", "IQR (extreme)", "Z-Score", "MAD", "Percentile", 
               "Tukey Inner", "Tukey Outer"),
    outliers_found = c(
      results$iqr$total_detected,
      results$iqr_extreme$total_detected,
      results$zscore$total_detected,
      results$mad$total_detected,
      results$percentile$total_detected,
      results$tukey_inner$total_detected,
      results$tukey_outer$total_detected
    )
  )
  
  results$data <- x_clean
  results$n <- length(x_clean)
  
  results
}

# ============================================================================
# Remove/Replace Outliers
# ============================================================================

#' Remove outliers from data
#' 
#' @param x Numeric vector
#' @param method Detection method: "iqr", "zscore", "mad", "percentile"
#' @param ... Additional arguments passed to detection function
#' @return List with cleaned data and removal info
remove_outliers <- function(x, method = c("iqr", "zscore", "mad", "percentile"), ...) {
  method <- match.arg(method)
  
  detect_fn <- switch(method,
    "iqr" = detect_outliers_iqr,
    "zscore" = detect_outliers_zscore,
    "mad" = detect_outliers_mad,
    "percentile" = detect_outliers_percentile
  )
  
  result <- detect_fn(x, ...)
  
  # Create logical vector for non-outliers (preserving NA positions)
  clean_x <- x
  if (length(result$indices) > 0) {
    clean_x[result$indices] <- NA
  }
  
  list(
    original = x,
    cleaned = clean_x,
    removed_indices = result$indices,
    removed_values = result$outliers,
    method = method,
    n_removed = length(result$indices)
  )
}

#' Replace outliers with specified value
#' 
#' @param x Numeric vector
#' @param method Detection method: "iqr", "zscore", "mad", "percentile"
#' @param replacement How to replace: "mean", "median", "trim", or a specific value
#' @param ... Additional arguments passed to detection function
#' @return List with replaced data and info
replace_outliers <- function(x, method = c("iqr", "zscore", "mad", "percentile"), 
                             replacement = "median", ...) {
  method <- match.arg(method)
  
  detect_fn <- switch(method,
    "iqr" = detect_outliers_iqr,
    "zscore" = detect_outliers_zscore,
    "mad" = detect_outliers_mad,
    "percentile" = detect_outliers_percentile
  )
  
  result <- detect_fn(x, ...)
  clean_x <- x
  
  if (length(result$indices) > 0) {
    # Get non-outlier values for calculating replacement
    non_outliers <- x[-result$indices]
    
    replace_value <- switch(replacement,
      "mean" = mean(non_outliers, na.rm = TRUE),
      "median" = median(non_outliers, na.rm = TRUE),
      "trim" = {
        # Winsorize to nearest non-outlier
        bounds <- switch(method,
          "iqr" = c(result$lower_bound, result$upper_bound),
          "zscore" = c(result$mean - result$threshold * result$sd, 
                       result$mean + result$threshold * result$sd),
          "mad" = c(result$median - result$threshold * result$mad / 1.4826,
                    result$median + result$threshold * result$mad / 1.4826),
          "percentile" = c(result$lower_bound, result$upper_bound)
        )
        clean_x[clean_x < bounds[1]] <- bounds[1]
        clean_x[clean_x > bounds[2]] <- bounds[2]
        return(list(
          original = x,
          replaced = clean_x,
          replaced_indices = result$indices,
          replaced_values = result$outliers,
          method = method,
          replacement = "winsorized",
          n_replaced = length(result$indices)
        ))
      },
      as.numeric(replacement)  # Use provided value
    )
    
    clean_x[result$indices] <- replace_value
  }
  
  list(
    original = x,
    replaced = clean_x,
    replaced_indices = result$indices,
    replaced_values = result$outliers,
    method = method,
    replacement = replacement,
    replacement_value = if (replacement != "trim") replace_value else NA,
    n_replaced = length(result$indices)
  )
}

# ============================================================================
# Visualization Helper (returns plot data)
# ============================================================================

#' Generate box plot statistics for outlier visualization
#' 
#' @param x Numeric vector
#' @return List with box plot statistics
boxplot_outlier_stats <- function(x) {
  if (!is.numeric(x)) {
    stop("Input must be a numeric vector")
  }
  
  x <- x[!is.na(x)]
  
  bp_stats <- boxplot.stats(x)
  
  list(
    lower_whisker = bp_stats$stats[1],
    q1 = bp_stats$stats[2],
    median = bp_stats$stats[3],
    q3 = bp_stats$stats[4],
    upper_whisker = bp_stats$stats[5],
    outliers = bp_stats$out,
    n = length(x),
    conf = bp_stats$conf
  )
}