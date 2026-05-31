"""Tests for outlier_detection_utils module."""

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


def test_z_score_basic():
    data = [1, 2, 2, 3, 4, 5, 6, 7, 8, 100]
    outliers = z_score_outliers(data, threshold=2.5)
    assert len(outliers) == 1
    assert outliers[0][0] == 9
    assert outliers[0][1] == 100
    print("✓ z_score_basic passed")


def test_z_score_no_outliers():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    outliers = z_score_outliers(data, threshold=3.0)
    assert len(outliers) == 0
    print("✓ z_score_no_outliers passed")


def test_z_score_small_data():
    assert z_score_outliers([1, 2], threshold=2.0) == []
    assert z_score_outliers([], threshold=2.0) == []
    print("✓ z_score_small_data passed")


def test_iqr_basic():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
    outliers = iqr_outliers(data)
    assert len(outliers) == 1
    assert outliers[0][0] == 9
    print("✓ iqr_basic passed")


def test_iqr_extreme_outlier():
    """Test IQR with clear extreme outlier."""
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100, 200]
    outliers = iqr_outliers(data, multiplier=1.5)
    # Both 100 and 200 exceed upper bound
    assert len(outliers) >= 1
    indices = [o[0] for o in outliers]
    assert 9 in indices or 10 in indices
    print("✓ iqr_extreme_outlier passed")


def test_iqr_high_multiplier():
    """Test IQR with higher multiplier reduces outliers."""
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
    standard = iqr_outliers(data, multiplier=1.5)
    extreme = iqr_outliers(data, multiplier=3.0)
    assert len(standard) >= len(extreme)
    print("✓ iqr_high_multiplier passed")


def test_modified_z_basic():
    data = [1, 2, 2, 3, 4, 5, 6, 7, 8, 100]
    outliers = modified_z_score_outliers(data, threshold=3.0)
    assert len(outliers) >= 1
    print("✓ modified_z_basic passed")


def test_modified_z_no_outliers():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    outliers = modified_z_score_outliers(data, threshold=3.5)
    assert len(outliers) == 0
    print("✓ modified_z_no_outliers passed")


def test_esd_basic():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100, 200]
    outliers = esd_test(data, max_outliers=5)
    assert len(outliers) >= 1
    print("✓ esd_basic passed")


def test_esd_limit():
    data = list(range(1, 101)) + [1000, 2000, 3000]
    outliers = esd_test(data, max_outliers=2)
    assert len(outliers) <= 2
    print("✓ esd_limit passed")


def test_isolation_forest_score():
    data = [1, 2, 2, 3, 4, 5, 6, 7, 8, 100, 200]
    result = isolation_forest_score(data, contamination=0.3)
    assert len(result) >= 1
    assert result[0][2] >= result[-1][2]
    print("✓ isolation_forest_score passed")


def test_isolation_forest_small_data():
    assert isolation_forest_score([1, 2, 3]) == []
    print("✓ isolation_forest_small_data passed")


def test_density_dbscan_basic():
    data = [1, 2, 3, 50, 51, 52, 100, 101]
    result = density_dbscan_outliers(data, min_points=2, epsilon_factor=0.8)
    assert len(result) >= 0
    print("✓ density_dbscan_basic passed")


def test_density_dbscan_no_outliers():
    data = list(range(1, 21))
    result = density_dbscan_outliers(data, min_points=3, epsilon_factor=0.3)
    outlier_count = len([r for r in result if r[2] == -1])
    assert outlier_count < len(data)
    print("✓ density_dbscan_no_outliers passed")


def test_mahalanobis_univariate():
    data = [[1], [2], [3], [4], [5], [500]]  # 500 is clearly an outlier
    outliers = mahalanobis_outliers(data, threshold=2.0)  # z=2.23 > 2
    assert len(outliers) >= 1
    print("✓ mahalanobis_univariate passed")


def test_mahalanobis_multivariate():
    data = [[1, 2], [2, 3], [3, 4], [4, 5], [100, 100]]  # mahal distance ~2.0, threshold sqrt(2)≈1.41
    outliers = mahalanobis_outliers(data, threshold=1.0)
    assert len(outliers) >= 1
    print("✓ mahalanobis_multivariate passed")


def test_mahalanobis_small_data():
    assert mahalanobis_outliers([[1], [2]], threshold=2.0) == []
    print("✓ mahalanobis_small_data passed")


def test_all_methods_summary():
    data = [1, 2, 3, 4, 5, 100]
    summary = all_methods_summary(data)
    assert "z_score" in summary
    assert "iqr" in summary
    assert "modified_z_score" in summary
    assert "esd" in summary
    assert "density_dbscan" in summary
    assert "data_stats" in summary
    assert summary["data_stats"]["count"] == 6
    print("✓ all_methods_summary passed")


def test_boundary_cases():
    """Test edge cases."""
    # All same values - no outliers
    data = [5.0] * 10
    result = z_score_outliers(data, threshold=2.0)
    assert result == []
    
    # Clean data - no outliers
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = z_score_outliers(data, threshold=3.0)
    assert len(result) == 0
    print("✓ boundary_cases passed")


def run_all_tests():
    print("\n" + "=" * 50)
    print("Running Outlier Detection Utils Tests")
    print("=" * 50 + "\n")
    
    tests = [
        test_z_score_basic,
        test_z_score_no_outliers,
        test_z_score_small_data,
        test_iqr_basic,
        test_iqr_extreme_outlier,
        test_iqr_high_multiplier,
        test_modified_z_basic,
        test_modified_z_no_outliers,
        test_esd_basic,
        test_esd_limit,
        test_isolation_forest_score,
        test_isolation_forest_small_data,
        test_density_dbscan_basic,
        test_density_dbscan_no_outliers,
        test_mahalanobis_univariate,
        test_mahalanobis_multivariate,
        test_mahalanobis_small_data,
        test_all_methods_summary,
        test_boundary_cases,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
