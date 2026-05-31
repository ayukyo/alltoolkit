"""Usage examples for outlier_detection_utils module."""

from mod import (
    z_score_outliers,
    iqr_outliers,
    modified_z_score_outliers,
    esd_test,
    isolation_forest_score,
    density_dbscan_outliers,
    mahalanobis_outliers,
    all_methods_summary,
)


def example_basic():
    """Basic usage with simple numeric data."""
    print("=" * 60)
    print("Example 1: Basic Z-Score Detection")
    print("=" * 60)
    
    sensor_data = [20.5, 21.2, 20.8, 21.0, 20.3, 19.9, 20.7, 21.1, 20.6, 20.4, 85.0, 20.9, 20.2, 21.3, 20.8]
    
    print(f"Data: {sensor_data}")
    print()
    
    outliers = z_score_outliers(sensor_data, threshold=3.0)
    print("Z-Score outliers (threshold=3.0):")
    for idx, val, z in outliers:
        print(f"  Index {idx}: value={val}, z-score={z:.2f}")
    
    iqr_result = iqr_outliers(sensor_data)
    print("\nIQR outliers (multiplier=1.5):")
    for idx, val, lower, upper in iqr_result:
        print(f"  Index {idx}: value={val}, bounds=[{lower:.2f}, {upper:.2f}]")
    
    print()


def example_time_series():
    """Detect outliers in time series data."""
    print("=" * 60)
    print("Example 2: Time Series Anomaly Detection")
    print("=" * 60)
    
    response_times = [45, 48, 52, 47, 50, 120, 51, 49, 46, 48, 53, 350, 47, 50, 52, 49]
    
    print(f"Response times: {response_times}")
    print()
    
    mad_outliers = modified_z_score_outliers(response_times, threshold=3.5)
    print("Modified Z-Score (MAD-based) outliers:")
    for idx, val, mz in mad_outliers:
        print(f"  Index {idx}: value={val}ms, modified_z={mz:.2f}")
    
    summary = all_methods_summary(response_times)
    print(f"\nData statistics:")
    print(f"  Mean: {summary['data_stats']['mean']:.2f}ms")
    print(f"  Median: {summary['data_stats']['median']:.2f}ms")
    print(f"  Std: {summary['data_stats']['std']:.2f}ms")
    print()


def example_multiple_outliers():
    """Detect multiple outliers with ESD test."""
    print("=" * 60)
    print("Example 3: Multiple Outliers with ESD Test")
    print("=" * 60)
    
    sales_data = [100, 105, 98, 102, 110, 95, 500, 103, 99, 101, 104, 800, 100, 105, 97, 102, 1200, 98, 103, 96, 101]
    
    print(f"Sales data: {sales_data}")
    print()
    
    outliers = esd_test(sales_data, max_outliers=5, significance=0.05)
    print(f"ESD detected {len(outliers)} outliers:")
    for idx, val, g in outliers:
        print(f"  Index {idx}: value={val}, Grubbs G={g:.2f}")
    
    print()


def example_isolation_forest():
    """Use isolation forest for scoring anomalies."""
    print("=" * 60)
    print("Example 4: Isolation Forest Anomaly Scoring")
    print("=" * 60)
    
    session_durations = [2, 3, 4, 5, 6, 7, 8, 45, 60, 90, 5, 6, 7, 4, 3, 5, 120, 180, 300, 6, 5, 4, 7, 3]
    
    print(f"Session durations: {session_durations}")
    print()
    
    result = isolation_forest_score(session_durations, n_trees=100, contamination=0.2)
    
    print("Top 5 anomalous sessions:")
    for idx, val, score in result[:5]:
        print(f"  Index {idx}: {val}min (anomaly score={score:.3f})")
    
    print()


def example_density_based():
    """Detect outliers using density-based clustering."""
    print("=" * 60)
    print("Example 5: Density-Based Outlier Detection")
    print("=" * 60)
    
    purchase_amounts = [25, 30, 35, 28, 32, 150, 160, 155, 45, 38, 42, 50, 35, 500, 600, 550, 800, 33, 29, 41, 36]
    
    print(f"Purchase amounts: {purchase_amounts}")
    print()
    
    result = density_dbscan_outliers(purchase_amounts, min_points=3, epsilon_factor=0.5)
    
    outliers = [r for r in result if r[2] == -1]
    print(f"Found {len(outliers)} outliers (cluster_id=-1):")
    for idx, val, cluster in outliers:
        print(f"  Index {idx}: ${val}")
    
    print()


def example_multivariate():
    """Detect outliers in multivariate data."""
    print("=" * 60)
    print("Example 6: Multivariate Outlier Detection")
    print("=" * 60)
    
    customer_data = [
        [25, 40000], [30, 55000], [35, 65000], [28, 48000], [45, 75000],
        [32, 62000], [29, 51000], [50, 90000], [55, 120000], [27, 45000], [38, 70000],
    ]
    
    print("Customer data [age, income]:")
    for i, c in enumerate(customer_data):
        print(f"  {i}: {c}")
    print()
    
    outliers = mahalanobis_outliers(customer_data, threshold=2.5)
    print(f"Mahalanobis distance detected {len(outliers)} outliers:")
    for idx, point, dist in outliers:
        print(f"  Index {idx}: {point}, distance={dist:.2f}")
    
    print()


def example_comprehensive():
    """Run all methods and compare results."""
    print("=" * 60)
    print("Example 7: Comprehensive Analysis")
    print("=" * 60)
    
    data = [10, 12, 11, 13, 12, 14, 11, 10, 13, 12, 100, 150]
    print(f"Data: {data}")
    print()
    
    summary = all_methods_summary(data)
    
    print("Detection results by method:")
    print(f"  Z-Score:       {len(summary['z_score'])} outliers")
    print(f"  IQR:           {len(summary['iqr'])} outliers")
    print(f"  Modified Z:    {len(summary['modified_z_score'])} outliers")
    print(f"  ESD:           {len(summary['esd'])} outliers")
    print(f"  Density DBSCAN: {len(summary['density_dbscan'])} outliers")
    
    all_indices = set()
    for method in ['z_score', 'iqr', 'modified_z_score', 'esd']:
        for item in summary[method]:
            all_indices.add(item[0])
    
    print(f"\nIndices flagged by at least one method: {sorted(all_indices)}")
    print()


def run_all_examples():
    """Run all examples."""
    example_basic()
    example_time_series()
    example_multiple_outliers()
    example_isolation_forest()
    example_density_based()
    example_multivariate()
    example_comprehensive()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()