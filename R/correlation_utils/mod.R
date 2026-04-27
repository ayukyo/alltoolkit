#!/usr/bin/env Rscript
# correlation_utils/mod.R - Correlation Analysis Utilities Module for R
#
# A comprehensive correlation utility module providing various correlation
# coefficients, correlation matrices, significance testing, and related
# statistical functions with zero external dependencies.
#
# Author: AllToolkit
# Version: 1.0.0
# License: MIT

# ============================================================================
# Module Metadata
# ============================================================================

CORRELATION_UTILS_VERSION <- "1.0.0"
CORRELATION_UTILS_AUTHOR <- "AllToolkit"

# ============================================================================
# Basic Correlation Coefficients
# ============================================================================

#' Calculate Pearson Correlation Coefficient
#'
#' @param x A numeric vector
#' @param y A numeric vector
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The Pearson correlation coefficient (-1 to 1)
pearson_cor <- function(x, y, na.rm = TRUE) {
  if (!is.numeric(x) || !is.numeric(y)) {
    stop("Both inputs must be numeric")
  }
  if (length(x) != length(y)) {
    stop("Vectors must have equal length")
  }
  
  if (na.rm) {
    complete <- !is.na(x) & !is.na(y)
    x <- x[complete]
    y <- y[complete]
  }
  
  n <- length(x)
  if (n < 2) {
    return(NA_real_)
  }
  
  # Check for zero variance
  if (var(x) == 0 || var(y) == 0) {
    return(NA_real_)
  }
  
  mx <- mean(x)
  my <- mean(y)
  
  numerator <- sum((x - mx) * (y - my))
  denominator <- sqrt(sum((x - mx)^2) * sum((y - my)^2))
  
  if (denominator == 0) {
    return(NA_real_)
  }
  
  numerator / denominator
}

#' Calculate Spearman Rank Correlation Coefficient
#'
#' @param x A numeric vector
#' @param y A numeric vector
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The Spearman correlation coefficient (-1 to 1)
spearman_cor <- function(x, y, na.rm = TRUE) {
  if (!is.numeric(x) || !is.numeric(y)) {
    stop("Both inputs must be numeric")
  }
  if (length(x) != length(y)) {
    stop("Vectors must have equal length")
  }
  
  if (na.rm) {
    complete <- !is.na(x) & !is.na(y)
    x <- x[complete]
    y <- y[complete]
  }
  
  n <- length(x)
  if (n < 2) {
    return(NA_real_)
  }
  
  # Convert to ranks
  rx <- rank(x, ties.method = "average")
  ry <- rank(y, ties.method = "average")
  
  # Pearson correlation on ranks
  pearson_cor(rx, ry, na.rm = FALSE)
}

#' Calculate Kendall's Tau Correlation Coefficient
#'
#' @param x A numeric vector
#' @param y A numeric vector
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The Kendall's tau coefficient (-1 to 1)
kendall_tau <- function(x, y, na.rm = TRUE) {
  if (!is.numeric(x) || !is.numeric(y)) {
    stop("Both inputs must be numeric")
  }
  if (length(x) != length(y)) {
    stop("Vectors must have equal length")
  }
  
  if (na.rm) {
    complete <- !is.na(x) & !is.na(y)
    x <- x[complete]
    y <- y[complete]
  }
  
  n <- length(x)
  if (n < 2) {
    return(NA_real_)
  }
  
  concordant <- 0
  discordant <- 0
  
  for (i in 1:(n - 1)) {
    for (j in (i + 1):n) {
      dx <- x[i] - x[j]
      dy <- y[i] - y[j]
      product <- dx * dy
      
      if (product > 0) {
        concordant <- concordant + 1
      } else if (product < 0) {
        discordant <- discordant + 1
      }
    }
  }
  
  total_pairs <- concordant + discordant
  if (total_pairs == 0) {
    return(NA_real_)
  }
  
  (concordant - discordant) / total_pairs
}

#' Calculate Kendall's Tau-b (with tie correction)
#'
#' @param x A numeric vector
#' @param y A numeric vector
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The Kendall's tau-b coefficient (-1 to 1)
kendall_tau_b <- function(x, y, na.rm = TRUE) {
  if (!is.numeric(x) || !is.numeric(y)) {
    stop("Both inputs must be numeric")
  }
  if (length(x) != length(y)) {
    stop("Vectors must have equal length")
  }
  
  if (na.rm) {
    complete <- !is.na(x) & !is.na(y)
    x <- x[complete]
    y <- y[complete]
  }
  
  n <- length(x)
  if (n < 2) {
    return(NA_real_)
  }
  
  concordant <- 0
  discordant <- 0
  tie_x <- 0
  tie_y <- 0
  
  for (i in 1:(n - 1)) {
    for (j in (i + 1):n) {
      dx <- sign(x[i] - x[j])
      dy <- sign(y[i] - y[j])
      
      if (dx == 0 || dy == 0) {
        if (dx == 0 && dy != 0) tie_x <- tie_x + 1
        if (dy == 0 && dx != 0) tie_y <- tie_y + 1
        if (dx == 0 && dy == 0) {
          tie_x <- tie_x + 1
          tie_y <- tie_y + 1
        }
      } else if (dx == dy) {
        concordant <- concordant + 1
      } else {
        discordant <- discordant + 1
      }
    }
  }
  
  total_pairs <- n * (n - 1) / 2
  n_con_dis <- concordant + discordant
  
  denominator <- sqrt((n_con_dis + tie_x) * (n_con_dis + tie_y))
  
  if (denominator == 0) {
    return(NA_real_)
  }
  
  (concordant - discordant) / denominator
}

# ============================================================================
# Correlation Matrix Functions
# ============================================================================

#' Calculate Correlation Matrix (Pearson)
#'
#' @param data A data frame or matrix with numeric columns
#' @param method Character, correlation method: "pearson", "spearman", or "kendall"
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return A correlation matrix
cor_matrix <- function(data, method = "pearson", na.rm = TRUE) {
  if (is.data.frame(data)) {
    data <- as.matrix(data)
  }
  
  if (!is.matrix(data) && !is.numeric(data)) {
    stop("Input must be a data frame or numeric matrix")
  }
  
  if (is.vector(data)) {
    stop("Input must have at least 2 columns")
  }
  
  cols <- ncol(data)
  if (cols < 2) {
    stop("Input must have at least 2 columns")
  }
  
  result <- matrix(1, nrow = cols, ncol = cols)
  colnames(result) <- colnames(data)
  rownames(result) <- colnames(data)
  
  for (i in 1:(cols - 1)) {
    for (j in (i + 1):cols) {
      x <- data[, i]
      y <- data[, j]
      
      cor_val <- switch(method,
        "pearson" = pearson_cor(x, y, na.rm = na.rm),
        "spearman" = spearman_cor(x, y, na.rm = na.rm),
        "kendall" = kendall_tau(x, y, na.rm = na.rm),
        pearson_cor(x, y, na.rm = na.rm)
      )
      
      result[i, j] <- cor_val
      result[j, i] <- cor_val
    }
  }
  
  result
}

#' Calculate Covariance Matrix
#'
#' @param data A data frame or matrix with numeric columns
#' @param sample Logical, use sample covariance? Default: TRUE
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return A covariance matrix
cov_matrix <- function(data, sample = TRUE, na.rm = TRUE) {
  if (is.data.frame(data)) {
    data <- as.matrix(data)
  }
  
  if (!is.matrix(data) && !is.numeric(data)) {
    stop("Input must be a data frame or numeric matrix")
  }
  
  cols <- ncol(data)
  if (cols < 2) {
    stop("Input must have at least 2 columns")
  }
  
  result <- matrix(0, nrow = cols, ncol = cols)
  colnames(result) <- colnames(data)
  rownames(result) <- colnames(data)
  
  for (i in 1:cols) {
    for (j in 1:cols) {
      result[i, j] <- covariance(data[, i], data[, j], sample = sample, na.rm = na.rm)
    }
  }
  
  result
}

#' Calculate Covariance between two vectors
#'
#' @param x A numeric vector
#' @param y A numeric vector
#' @param sample Logical, use sample covariance? Default: TRUE
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The covariance
covariance <- function(x, y, sample = TRUE, na.rm = TRUE) {
  if (!is.numeric(x) || !is.numeric(y)) {
    stop("Both inputs must be numeric")
  }
  if (length(x) != length(y)) {
    stop("Vectors must have equal length")
  }
  
  if (na.rm) {
    complete <- !is.na(x) & !is.na(y)
    x <- x[complete]
    y <- y[complete]
  }
  
  n <- length(x)
  if (n < 2) {
    return(NA_real_)
  }
  
  mx <- mean(x)
  my <- mean(y)
  
  divisor <- if (sample) n - 1 else n
  
  sum((x - mx) * (y - my)) / divisor
}

# ============================================================================
# Significance Testing
# ============================================================================

#' Calculate p-value for Pearson correlation
#'
#' @param r The correlation coefficient
#' @param n The sample size
#' @return Two-tailed p-value
cor_p_value <- function(r, n) {
  if (abs(r) >= 1) {
    return(if (abs(r) >= 1) 0 else NA_real_)
  }
  
  if (n < 4) {
    return(NA_real_)
  }
  
  # t-statistic
  t_stat <- r * sqrt((n - 2) / (1 - r^2))
  
  # Two-tailed p-value using t-distribution
  df <- n - 2
  2 * pt(-abs(t_stat), df = df)
}

#' Test Correlation Significance
#'
#' @param x A numeric vector
#' @param y A numeric vector
#' @param method Character, correlation method: "pearson", "spearman", or "kendall"
#' @param alpha Significance level, default 0.05
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return A list with correlation, p-value, and significance result
cor_test <- function(x, y, method = "pearson", alpha = 0.05, na.rm = TRUE) {
  if (!is.numeric(x) || !is.numeric(y)) {
    stop("Both inputs must be numeric")
  }
  if (length(x) != length(y)) {
    stop("Vectors must have equal length")
  }
  
  if (na.rm) {
    complete <- !is.na(x) & !is.na(y)
    x <- x[complete]
    y <- y[complete]
  }
  
  n <- length(x)
  
  cor_val <- switch(method,
    "pearson" = pearson_cor(x, y, na.rm = FALSE),
    "spearman" = spearman_cor(x, y, na.rm = FALSE),
    "kendall" = kendall_tau(x, y, na.rm = FALSE),
    pearson_cor(x, y, na.rm = FALSE)
  )
  
  p_val <- cor_p_value(cor_val, n)
  
  list(
    correlation = cor_val,
    p_value = p_val,
    n = n,
    method = method,
    significant = p_val < alpha,
    alpha = alpha
  )
}

# ============================================================================
# Partial and Semi-partial Correlation
# ============================================================================

#' Calculate Partial Correlation
#'
#' Calculates the correlation between x and y while controlling for z
#'
#' @param x A numeric vector
#' @param y A numeric vector
#' @param z A numeric vector or matrix of control variables
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The partial correlation coefficient
partial_cor <- function(x, y, z, na.rm = TRUE) {
  if (!is.numeric(x) || !is.numeric(y)) {
    stop("x and y must be numeric vectors")
  }
  
  if (is.vector(z)) {
    z <- matrix(z, ncol = 1)
  }
  
  if (na.rm) {
    # Remove rows with any NA
    all_data <- cbind(x, y, z)
    complete <- complete.cases(all_data)
    x <- x[complete]
    y <- y[complete]
    z <- z[complete, , drop = FALSE]
  }
  
  n <- length(x)
  if (n < 3) {
    return(NA_real_)
  }
  
  # Simple case: single control variable
  if (ncol(z) == 1) {
    z_vec <- z[, 1]
    
    rxy <- pearson_cor(x, y, na.rm = FALSE)
    rxz <- pearson_cor(x, z_vec, na.rm = FALSE)
    ryz <- pearson_cor(y, z_vec, na.rm = FALSE)
    
    numerator <- rxy - rxz * ryz
    denominator <- sqrt((1 - rxz^2) * (1 - ryz^2))
    
    if (denominator == 0) {
      return(NA_real_)
    }
    
    return(numerator / denominator)
  }
  
  # Multiple control variables: use matrix approach
  # Get residuals from regressing x and y on z
  z_with_intercept <- cbind(1, z)
  
  # Residuals for x
  coef_x <- solve(t(z_with_intercept) %*% z_with_intercept) %*% t(z_with_intercept) %*% x
  resid_x <- x - z_with_intercept %*% coef_x
  
  # Residuals for y
  coef_y <- solve(t(z_with_intercept) %*% z_with_intercept) %*% t(z_with_intercept) %*% y
  resid_y <- y - z_with_intercept %*% coef_y
  
  pearson_cor(as.vector(resid_x), as.vector(resid_y), na.rm = FALSE)
}

#' Calculate Semi-partial (Part) Correlation
#'
#' Calculates the correlation between x and y after removing the effect of z from x only
#'
#' @param x A numeric vector
#' @param y A numeric vector
#' @param z A numeric vector of control variable
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The semi-partial correlation coefficient
semi_partial_cor <- function(x, y, z, na.rm = TRUE) {
  if (!is.numeric(x) || !is.numeric(y) || !is.numeric(z)) {
    stop("All inputs must be numeric")
  }
  if (length(x) != length(y) || length(x) != length(z)) {
    stop("Vectors must have equal length")
  }
  
  if (na.rm) {
    complete <- !is.na(x) & !is.na(y) & !is.na(z)
    x <- x[complete]
    y <- y[complete]
    z <- z[complete]
  }
  
  n <- length(x)
  if (n < 3) {
    return(NA_real_)
  }
  
  rxy <- pearson_cor(x, y, na.rm = FALSE)
  rxz <- pearson_cor(x, z, na.rm = FALSE)
  ryz <- pearson_cor(y, z, na.rm = FALSE)
  
  numerator <- rxy - rxz * ryz
  denominator <- sqrt(1 - rxz^2)
  
  if (denominator == 0) {
    return(NA_real_)
  }
  
  numerator / denominator
}

# ============================================================================
# Correlation Distance and Similarity
# ============================================================================

#' Calculate Correlation Distance
#'
#' @param x A numeric vector
#' @param y A numeric vector
#' @param method Character, correlation method
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The correlation distance (0 to 2)
cor_distance <- function(x, y, method = "pearson", na.rm = TRUE) {
  r <- switch(method,
    "pearson" = pearson_cor(x, y, na.rm = na.rm),
    "spearman" = spearman_cor(x, y, na.rm = na.rm),
    "kendall" = kendall_tau(x, y, na.rm = na.rm),
    pearson_cor(x, y, na.rm = na.rm)
  )
  
  1 - r
}

#' Calculate Distance Correlation (dCor)
#'
#' A measure of dependence that can detect non-linear relationships
#'
#' @param x A numeric vector
#' @param y A numeric vector
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The distance correlation (0 to 1)
distance_cor <- function(x, y, na.rm = TRUE) {
  if (!is.numeric(x) || !is.numeric(y)) {
    stop("Both inputs must be numeric")
  }
  if (length(x) != length(y)) {
    stop("Vectors must have equal length")
  }
  
  if (na.rm) {
    complete <- !is.na(x) & !is.na(y)
    x <- x[complete]
    y <- y[complete]
  }
  
  n <- length(x)
  if (n < 4) {
    return(NA_real_)
  }
  
  # Compute distance matrices
  a <- matrix(0, n, n)
  b <- matrix(0, n, n)
  
  for (i in 1:n) {
    for (j in 1:n) {
      a[i, j] <- abs(x[i] - x[j])
      b[i, j] <- abs(y[i] - y[j])
    }
  }
  
  # Double center
  row_means_a <- rowMeans(a)
  col_means_a <- colMeans(a)
  grand_mean_a <- mean(a)
  
  row_means_b <- rowMeans(b)
  col_means_b <- colMeans(b)
  grand_mean_b <- mean(b)
  
  a_centered <- a - outer(row_means_a, rep(1, n)) - outer(rep(1, n), col_means_a) + grand_mean_a
  b_centered <- b - outer(row_means_b, rep(1, n)) - outer(rep(1, n), col_means_b) + grand_mean_b
  
  # Compute squared distance covariances
  dcov2 <- sum(a_centered * b_centered) / (n^2)
  dvar_x2 <- sum(a_centered^2) / (n^2)
  dvar_y2 <- sum(b_centered^2) / (n^2)
  
  # Distance correlation
  if (dvar_x2 <= 0 || dvar_y2 <= 0) {
    return(0)
  }
  
  sqrt(abs(dcov2) / sqrt(dvar_x2 * dvar_y2))
}

# ============================================================================
# Coefficient of Determination and Effect Sizes
# ============================================================================

#' Calculate R-squared (Coefficient of Determination)
#'
#' @param x A numeric vector
#' @param y A numeric vector
#' @param method Character, correlation method
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return The R-squared value (0 to 1)
r_squared <- function(x, y, method = "pearson", na.rm = TRUE) {
  r <- switch(method,
    "pearson" = pearson_cor(x, y, na.rm = na.rm),
    "spearman" = spearman_cor(x, y, na.rm = na.rm),
    "kendall" = kendall_tau(x, y, na.rm = na.rm),
    pearson_cor(x, y, na.rm = na.rm)
  )
  
  r^2
}

#' Calculate Adjusted R-squared
#'
#' @param r_sq The R-squared value
#' @param n Sample size
#' @param p Number of predictors
#' @return The adjusted R-squared
adjusted_r_squared <- function(r_sq, n, p = 1) {
  if (n <= p + 1) {
    return(NA_real_)
  }
  
  1 - (1 - r_sq) * (n - 1) / (n - p - 1)
}

#' Calculate Cohen's d (Effect Size)
#'
#' @param x A numeric vector
#' @param y A numeric vector
#' @param na.rm Logical, should NA values be removed? Default: TRUE
#' @return Cohen's d effect size
cohens_d <- function(x, y, na.rm = TRUE) {
  if (!is.numeric(x) || !is.numeric(y)) {
    stop("Both inputs must be numeric")
  }
  
  if (na.rm) {
    x <- x[!is.na(x)]
    y <- y[!is.na(y)]
  }
  
  n1 <- length(x)
  n2 <- length(y)
  
  if (n1 < 2 || n2 < 2) {
    return(NA_real_)
  }
  
  m1 <- mean(x)
  m2 <- mean(y)
  
  # Pooled standard deviation
  var1 <- var(x)
  var2 <- var(y)
  
  s_pooled <- sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
  
  if (s_pooled == 0) {
    return(NA_real_)
  }
  
  (m1 - m2) / s_pooled
}

# ============================================================================
# Confidence Intervals
# ============================================================================

#' Calculate Confidence Interval for Pearson Correlation
#'
#' Uses Fisher's z-transformation
#'
#' @param r The correlation coefficient
#' @param n Sample size
#' @param conf_level Confidence level, default 0.95
#' @return A list with lower and upper bounds
cor_ci <- function(r, n, conf_level = 0.95) {
  if (abs(r) >= 1) {
    return(list(lower = NA_real_, upper = NA_real_))
  }
  
  if (n < 4) {
    return(list(lower = NA_real_, upper = NA_real_))
  }
  
  # Fisher's z-transformation
  z <- 0.5 * log((1 + r) / (1 - r))
  
  # Standard error
  se <- 1 / sqrt(n - 3)
  
  # z critical value
  alpha <- 1 - conf_level
  z_crit <- qnorm(1 - alpha / 2)
  
  # CI for z
  z_lower <- z - z_crit * se
  z_upper <- z + z_crit * se
  
  # Transform back to r
  r_lower <- (exp(2 * z_lower) - 1) / (exp(2 * z_lower) + 1)
  r_upper <- (exp(2 * z_upper) - 1) / (exp(2 * z_upper) + 1)
  
  list(lower = r_lower, upper = r_upper, conf_level = conf_level)
}

# ============================================================================
# Utility Functions
# ============================================================================

#' Interpret Correlation Coefficient
#'
#' @param r The correlation coefficient
#' @param method Character, interpretation method: "cohen" or "evans"
#' @return A character string describing the strength
interpret_cor <- function(r, method = "evans") {
  r_abs <- abs(r)
  
  if (method == "cohen") {
    strength <- if (r_abs < 0.1) {
      "negligible"
    } else if (r_abs < 0.3) {
      "small"
    } else if (r_abs < 0.5) {
      "medium"
    } else {
      "large"
    }
  } else if (method == "evans") {
    strength <- if (r_abs < 0.2) {
      "very weak"
    } else if (r_abs < 0.4) {
      "weak"
    } else if (r_abs < 0.6) {
      "moderate"
    } else if (r_abs < 0.8) {
      "strong"
    } else {
      "very strong"
    }
  } else {
    strength <- "unknown"
  }
  
  direction <- if (r >= 0) "positive" else "negative"
  
  paste(strength, direction, "correlation")
}

#' Check if correlation is significant
#'
#' @param r The correlation coefficient
#' @param n Sample size
#' @param alpha Significance level, default 0.05
#' @return Logical indicating significance
is_significant <- function(r, n, alpha = 0.05) {
  p_val <- cor_p_value(r, n)
  !is.na(p_val) && p_val < alpha
}

#' Find significant correlations in a matrix
#'
#' @param mat A correlation matrix
#' @param n Sample size
#' @param alpha Significance level, default 0.05
#' @return A data frame of significant correlations
significant_cors <- function(mat, n, alpha = 0.05) {
  if (!is.matrix(mat)) {
    stop("Input must be a correlation matrix")
  }
  
  rows <- nrow(mat)
  cols <- ncol(mat)
  
  result <- data.frame(
    var1 = character(),
    var2 = character(),
    r = numeric(),
    p_value = numeric(),
    stringsAsFactors = FALSE
  )
  
  for (i in 1:(rows - 1)) {
    for (j in (i + 1):cols) {
      r_val <- mat[i, j]
      if (!is.na(r_val) && r_val != 1) {
        p_val <- cor_p_value(r_val, n)
        if (!is.na(p_val) && p_val < alpha) {
          result <- rbind(result, data.frame(
            var1 = rownames(mat)[i],
            var2 = colnames(mat)[j],
            r = r_val,
            p_value = p_val,
            stringsAsFactors = FALSE
          ))
        }
      }
    }
  }
  
  result[order(result$p_value), ]
}

#' Print correlation matrix with significance stars
#'
#' @param mat A correlation matrix
#' @param n Sample size
#' @return Character matrix with significance stars
format_cor_matrix <- function(mat, n) {
  rows <- nrow(mat)
  cols <- ncol(mat)
  
  result <- matrix("", nrow = rows, ncol = cols)
  rownames(result) <- rownames(mat)
  colnames(result) <- colnames(mat)
  
  for (i in 1:rows) {
    for (j in 1:cols) {
      r_val <- mat[i, j]
      if (i == j) {
        result[i, j] <- "1.000"
      } else if (!is.na(r_val)) {
        p_val <- cor_p_value(r_val, n)
        stars <- if (is.na(p_val)) "" else if (p_val < 0.001) "***" else if (p_val < 0.01) "**" else if (p_val < 0.05) "*" else ""
        result[i, j] <- paste0(sprintf("%.3f", r_val), stars)
      } else {
        result[i, j] <- "NA"
      }
    }
  }
  
  result
}

# ============================================================================
# Module Info
# ============================================================================

correlation_info <- function() {
  cat("correlation_utils - Correlation Analysis Utilities for R\n")
  cat("Version:", CORRELATION_UTILS_VERSION, "\n")
  cat("Author:", CORRELATION_UTILS_AUTHOR, "\n")
  cat("\nAvailable functions:\n")
  cat("  Correlation coefficients: pearson_cor, spearman_cor, kendall_tau, kendall_tau_b\n")
  cat("  Matrix functions: cor_matrix, cov_matrix, covariance\n")
  cat("  Significance testing: cor_p_value, cor_test, is_significant, significant_cors\n")
  cat("  Partial correlation: partial_cor, semi_partial_cor\n")
  cat("  Distance-based: cor_distance, distance_cor\n")
  cat("  Effect sizes: r_squared, adjusted_r_squared, cohens_d\n")
  cat("  Confidence intervals: cor_ci\n")
  cat("  Utilities: interpret_cor, format_cor_matrix\n")
}