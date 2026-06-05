"""Outlier Detection Utils - Statistical methods for detecting anomalies in data."""
import random

import math
from typing import List, Tuple, Optional, Dict, Any
from collections import defaultdict


def _mean(data: List[float]) -> float:
    if not data:
        raise ValueError("Data cannot be empty")
    return sum(data) / len(data)


def _std(data: List[float], mean: Optional[float] = None) -> float:
    if not data:
        raise ValueError("Data cannot be empty")
    if mean is None:
        mean = _mean(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return math.sqrt(variance)


def _median(data: List[float]) -> float:
    if not data:
        raise ValueError("Data cannot be empty")
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    return sorted_data[mid] if n % 2 == 1 else (sorted_data[mid - 1] + sorted_data[mid]) / 2


def z_score_outliers(data: List[float], threshold: float = 3.0, method: str = "absolute") -> List[Tuple[int, float, float]]:
    """Detect outliers using Z-Score method."""
    if len(data) < 3:
        return []
    mu = _mean(data)
    sigma = _std(data, mu)
    if sigma == 0:
        return []
    outliers = []
    for i, x in enumerate(data):
        z = (x - mu) / sigma
        if method == "absolute":
            if abs(z) > threshold:
                outliers.append((i, x, z))
        else:
            if z > threshold:
                outliers.append((i, x, z))
    return outliers


def iqr_outliers(data: List[float], multiplier: float = 1.5) -> List[Tuple[int, float, float, float]]:
    """Detect outliers using IQR method."""
    if len(data) < 4:
        return []
    sorted_data = sorted(data)
    n = len(sorted_data)
    # Use median-based quartile indices (Excel-style)
    q1_idx = (n + 1) // 4
    q3_idx = (3 * n + 3) // 4
    q1 = sorted_data[q1_idx]
    q3 = sorted_data[q3_idx]
    iqr = q3 - q1
    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr
    outliers = []
    for i, x in enumerate(data):
        if x < lower_bound or x > upper_bound:
            outliers.append((i, x, lower_bound, upper_bound))
    return outliers


def modified_z_score_outliers(data: List[float], threshold: float = 3.5) -> List[Tuple[int, float, float]]:
    """Detect outliers using Modified Z-Score (MAD-based)."""
    if len(data) < 3:
        return []
    med = _median(data)
    deviations = [abs(x - med) for x in data]
    mad = _median(deviations)
    if mad == 0:
        return []
    outliers = []
    for i, x in enumerate(data):
        modified_z = 0.6745 * (x - med) / mad
        if abs(modified_z) > threshold:
            outliers.append((i, x, modified_z))
    return outliers


def esd_test(data: List[float], max_outliers: int = 10, significance: float = 0.05) -> List[Tuple[int, float, float]]:
    """Detect multiple outliers using ESD test."""
    if len(data) < 3:
        return []
    n = len(data)
    max_to_check = min(max_outliers, n // 2)
    if max_to_check == 0:
        return []
    values = list(data)
    outliers = []
    for _ in range(max_to_check):
        mu = _mean(values)
        sigma = _std(values, mu)
        if sigma == 0:
            break
        max_abs_z = -1
        max_idx = -1
        for i, x in enumerate(values):
            z = abs((x - mu) / sigma)
            if z > max_abs_z:
                max_abs_z = z
                max_idx = i
        n_current = len(values)
        critical_multiplier = 2.5 + 1.0 / math.sqrt(n_current)
        if max_abs_z > critical_multiplier:
            outliers.append((max_idx, values[max_idx], max_abs_z))
            values.pop(max_idx)
        else:
            break
    return outliers


def _sample_indices(n: int, size: int) -> List[int]:
    indices = list(range(n))
    for i in range(size):
        j = i + int(random.random() * (n - i))
        indices[i], indices[j] = indices[j], indices[i]
    return indices[:size]


def _c(n: int) -> float:
    if n <= 1:
        return 0
    if n == 2:
        return 1
    return 2.0 * (math.log(n - 1) + 0.5772156649) - (2.0 * (n - 1) / n)


def isolation_forest_score(data: List[float], n_trees: int = 100, sample_size: Optional[int] = None, contamination: float = 0.1) -> List[Tuple[int, float, float]]:
    """Simplified Isolation Forest for anomaly detection."""
    if len(data) < 4:
        return []
    n = len(data)
    sample_size = min(256, n) if sample_size is None else max(4, min(sample_size, n))
    scores = [0.0] * n
    for _ in range(n_trees):
        indices = _sample_indices(n, sample_size)
        sample = [data[i] for i in indices]
        for idx_in_sample, orig_idx in enumerate(indices):
            path_len = _isolation_tree_path(sample, idx_in_sample, 0)
            scores[orig_idx] += path_len
    avg_path_len = _c(sample_size)
    results = []
    for i, score in enumerate(scores):
        avg_score = score / n_trees
        anomaly_score = 2 ** (-avg_score / avg_path_len)
        results.append((i, data[i], anomaly_score))
    results.sort(key=lambda x: x[2], reverse=True)
    cutoff = max(1, int(n * contamination)) if contamination > 0 else len(results)
    return results[:cutoff]


def _isolation_tree_path(data: List[float], idx: int, depth: int, max_depth: int = 32) -> float:
    if len(data) <= 1 or depth >= max_depth:
        return depth + _c(len(data))
    min_val = min(data)
    max_val = max(data)
    if min_val == max_val:
        return depth + _c(len(data))
    split = min_val + random.random() * (max_val - min_val)
    below = [x for x in data if x < split]
    above = [x for x in data if x >= split]
    if idx < len(below):
        return _isolation_tree_path(below, idx, depth + 1, max_depth)
    else:
        return _isolation_tree_path(above, idx - len(below), depth + 1, max_depth)


def density_dbscan_outliers(data: List[float], min_points: int = 5, epsilon_factor: float = 0.5) -> List[Tuple[int, float, int]]:
    """Detect outliers using density-based approach (simplified DBSCAN)."""
    if len(data) < 3:
        return []
    n = len(data)
    mu = _mean(data)
    sigma = _std(data, mu)
    epsilon = sigma * epsilon_factor if sigma > 0 else 1.0
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if abs(data[i] - data[j]) <= epsilon:
                adj[i].append(j)
                adj[j].append(i)
    cluster_id = 0
    clusters = [-1] * n
    visited = [False] * n
    for i in range(n):
        if visited[i]:
            continue
        queue = [i]
        visited[i] = True
        while queue:
            curr = queue.pop(0)
            clusters[curr] = cluster_id
            for neighbor in adj[curr]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        cluster_id += 1
    cluster_sizes = defaultdict(int)
    for c in clusters:
        if c >= 0:
            cluster_sizes[c] += 1
    outliers = []
    for i, c in enumerate(clusters):
        if c >= 0 and cluster_sizes[c] < min_points:
            outliers.append((i, data[i], -1))
        elif c == -1:
            outliers.append((i, data[i], -1))
    return outliers


def mahalanobis_outliers(data: List[List[float]], threshold: float = 3.0) -> List[Tuple[int, List[float], float]]:
    """Detect outliers using Mahalanobis distance in multivariate data."""
    if len(data) < 3:
        return []
    n = len(data)
    dims = len(data[0])
    mean = [sum(data[i][j] for i in range(n)) / n for j in range(dims)]
    cov = [[0.0] * dims for _ in range(dims)]
    for i in range(dims):
        for j in range(i, dims):
            cov_ij = sum((data[k][i] - mean[i]) * (data[k][j] - mean[j]) for k in range(n)) / n
            cov[i][j] = cov_ij
            cov[j][i] = cov_ij
    try:
        cov_inv = _matrix_inverse(cov)
    except:
        return _mahalanobis_fallback(data, threshold)
    outliers = []
    for i, point in enumerate(data):
        diff = [point[j] - mean[j] for j in range(dims)]
        mahal_sq = 0.0
        for a in range(dims):
            for b in range(dims):
                mahal_sq += diff[a] * cov_inv[a][b] * diff[b]
        mahal_dist = math.sqrt(mahal_sq)
        if mahal_dist > threshold * math.sqrt(dims):
            outliers.append((i, point, mahal_dist))
    return outliers


def _matrix_inverse(m: List[List[float]]) -> List[List[float]]:
    n = len(m)
    if n == 2:
        det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
        if abs(det) < 1e-10:
            raise ValueError("Singular matrix")
        return [[m[1][1] / det, -m[0][1] / det], [-m[1][0] / det, m[0][0] / det]]
    aug = [row + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(m)]
    for col in range(n):
        max_row = col
        for row in range(col + 1, n):
            if abs(aug[row][col]) > abs(aug[max_row][col]):
                max_row = row
        aug[col], aug[max_row] = aug[max_row], aug[col]
        if abs(aug[col][col]) < 1e-10:
            raise ValueError("Singular matrix")
        pivot = aug[col][col]
        for j in range(2 * n):
            aug[col][j] /= pivot
        for row in range(n):
            if row != col:
                factor = aug[row][col]
                for j in range(2 * n):
                    aug[row][j] -= factor * aug[col][j]
    return [row[n:] for row in aug]


def _mahalanobis_fallback(data: List[List[float]], threshold: float) -> List[Tuple[int, List[float], float]]:
    if not data or not data[0]:
        return []
    n = len(data)
    dims = len(data[0])
    means = [_mean([data[i][j] for i in range(n)]) for j in range(dims)]
    stds = [_std([data[i][j] for i in range(n)], means[j]) for j in range(dims)]
    outliers = []
    for i, point in enumerate(data):
        max_z = 0.0
        for j in range(dims):
            if stds[j] > 0:
                z = abs((point[j] - means[j]) / stds[j])
                max_z = max(max_z, z)
        if max_z > threshold:
            outliers.append((i, point, max_z))
    return outliers


def all_methods_summary(data: List[float], threshold: float = 3.0) -> Dict[str, Any]:
    """Run all outlier detection methods and return summary."""
    return {
        "z_score": z_score_outliers(data, threshold),
        "iqr": iqr_outliers(data),
        "modified_z_score": modified_z_score_outliers(data, threshold),
        "esd": esd_test(data, max_outliers=5),
        "density_dbscan": density_dbscan_outliers(data),
        "data_stats": {
            "count": len(data),
            "mean": _mean(data),
            "std": _std(data),
            "median": _median(data),
            "min": min(data),
            "max": max(data)
        }
    }
