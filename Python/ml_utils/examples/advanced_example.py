"""
AllToolkit - ML Utils Advanced Example

This file demonstrates an end-to-end machine learning pipeline using ml_utils.
We'll build a simple K-Nearest Neighbors classifier from scratch.

Run: python advanced_example.py
"""

import sys
import os
from collections import Counter

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # Preprocessing
    train_test_split, normalize_matrix, standardize_matrix,
    
    # Classification Metrics
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix_multiclass, classification_report,
    
    # Distance Metrics
    euclidean_distance,
    
    # Cross-validation
    k_fold_split,
    
    # Learning Rate Schedulers
    StepLR, CosineAnnealingLR,
)


class KNNClassifier:
    """
    Simple K-Nearest Neighbors classifier implemented from scratch.
    Uses ml_utils for distance calculation and metrics.
    """
    
    def __init__(self, k: int = 3, distance_fn=euclidean_distance):
        self.k = k
        self.distance_fn = distance_fn
        self.X_train = None
        self.y_train = None
    
    def fit(self, X: list, y: list) -> 'KNNClassifier':
        """Store training data."""
        self.X_train = X
        self.y_train = y
        return self
    
    def _predict_single(self, x: list) -> any:
        """Predict class for a single sample."""
        # Calculate distances to all training points
        distances = []
        for i, x_train in enumerate(self.X_train):
            dist = self.distance_fn(x, x_train)
            distances.append((dist, self.y_train[i]))
        
        # Sort by distance and get k nearest neighbors
        distances.sort(key=lambda x: x[0])
        k_nearest = distances[:self.k]
        
        # Majority vote
        votes = Counter(label for _, label in k_nearest)
        return votes.most_common(1)[0][0]
    
    def predict(self, X: list) -> list:
        """Predict classes for multiple samples."""
        return [self._predict_single(x) for x in X]


def generate_synthetic_data(n_samples: int = 200, n_features: int = 4, n_classes: int = 3):
    """
    Generate synthetic classification data.
    Each class is centered around a different point in feature space.
    """
    import random
    random.seed(42)
    
    # Class centers
    centers = [
        [random.uniform(0, 10) for _ in range(n_features)]
        for _ in range(n_classes)
    ]
    
    X = []
    y = []
    
    samples_per_class = n_samples // n_classes
    
    for class_idx in range(n_classes):
        for _ in range(samples_per_class):
            # Generate point around class center with some noise
            point = [
                centers[class_idx][j] + random.gauss(0, 1.5)
                for j in range(n_features)
            ]
            X.append(point)
            y.append(class_idx)
    
    return X, y


def evaluate_model(y_true: list, y_pred: list, model_name: str = "Model"):
    """Print comprehensive evaluation metrics."""
    print(f"\n{'=' * 60}")
    print(f"{model_name} Evaluation")
    print(f"{'=' * 60}")
    
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='macro')
    recall = recall_score(y_true, y_pred, average='macro')
    f1 = f1_score(y_true, y_pred, average='macro')
    
    print(f"\nOverall Metrics (macro average):")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1 Score:  {f1:.4f}")
    
    # Per-class metrics
    print(f"\nPer-Class Metrics:")
    report = classification_report(y_true, y_pred)
    for label in sorted(report.keys()):
        metrics = report[label]
        print(f"  Class {label}: P={metrics.precision:.3f}, R={metrics.recall:.3f}, "
              f"F1={metrics.f1_score:.3f}, Support={metrics.support}")
    
    # Confusion matrix
    cm = confusion_matrix_multiclass(y_true, y_pred)
    print(f"\nConfusion Matrix:")
    print(f"  Labels: {cm.labels}")
    for i, row in enumerate(cm.matrix):
        print(f"  Class {i}: {row}")
    
    return accuracy


def demo_knn_pipeline():
    """Demonstrate complete KNN classification pipeline."""
    print("\n" + "#" * 60)
    print("# KNN Classification Pipeline Demo")
    print("#" * 60)
    
    # Generate data
    print("\n[1] Generating synthetic data...")
    X, y = generate_synthetic_data(n_samples=300, n_features=4, n_classes=3)
    print(f"    Generated {len(X)} samples with {len(set(y))} classes")
    
    # Split data
    print("\n[2] Splitting data (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"    Training: {len(X_train)} samples")
    print(f"    Test:     {len(X_test)} samples")
    
    # Standardize features
    print("\n[3] Standardizing features...")
    X_train_std, means, stds = standardize_matrix(X_train, axis=0)
    
    # Apply same transformation to test set
    X_test_std = []
    for row in X_test:
        std_row = [(row[j] - means[j]) / stds[j] for j in range(len(row))]
        X_test_std.append(std_row)
    print(f"    Feature means: {[f'{m:.2f}' for m in means]}")
    print(f"    Feature stds:  {[f'{s:.2f}' for s in stds]}")
    
    # Train and evaluate with different k values
    print("\n[4] Evaluating different k values...")
    best_k = 1
    best_accuracy = 0
    
    for k in [1, 3, 5, 7, 9, 11]:
        knn = KNNClassifier(k=k)
        knn.fit(X_train_std, y_train)
        y_pred = knn.predict(X_test_std)
        accuracy = evaluate_model(y_test, y_pred, f"KNN (k={k})")
        
        if accuracy > best_accuracy:
            best_k = k
            best_accuracy = accuracy
    
    print(f"\n[5] Best k value: {best_k} (accuracy: {best_accuracy:.4f})")
    
    return best_k


def demo_cross_validation():
    """Demonstrate k-fold cross-validation for hyperparameter tuning."""
    print("\n" + "#" * 60)
    print("# K-Fold Cross-Validation Demo")
    print("#" * 60)
    
    # Generate data
    print("\n[1] Generating data for cross-validation...")
    X, y = generate_synthetic_data(n_samples=200, n_features=4, n_classes=3)
    
    # K-fold split
    print("\n[2] Creating 5-fold cross-validation...")
    folds = k_fold_split(n_samples=len(X), k=5, random_state=42)
    
    # Test different k values
    k_values = [1, 3, 5, 7, 9]
    cv_results = {k: [] for k in k_values}
    
    print("\n[3] Running cross-validation...")
    for fold_idx, (train_idx, test_idx) in enumerate(folds):
        # Split data for this fold
        X_train = [X[i] for i in train_idx]
        X_test = [X[i] for i in test_idx]
        y_train = [y[i] for i in train_idx]
        y_test = [y[i] for i in test_idx]
        
        # Standardize
        X_train_std, means, stds = standardize_matrix(X_train, axis=0)
        X_test_std = []
        for row in X_test:
            std_row = [(row[j] - means[j]) / stds[j] for j in range(len(row))]
            X_test_std.append(std_row)
        
        # Evaluate each k
        for k in k_values:
            knn = KNNClassifier(k=k)
            knn.fit(X_train_std, y_train)
            y_pred = knn.predict(X_test_std)
            accuracy = accuracy_score(y_test, y_pred)
            cv_results[k].append(accuracy)
            
            print(f"    Fold {fold_idx + 1}, k={k}: accuracy={accuracy:.4f}")
    
    # Summarize results
    print("\n[4] Cross-Validation Results Summary:")
    print(f"    {'k':<5} {'Mean Acc':>10} {'Std Acc':>10}")
    print(f"    {'-' * 5} {'-' * 10} {'-' * 10}")
    
    best_k = 1
    best_mean = 0
    for k in k_values:
        mean_acc = sum(cv_results[k]) / len(cv_results[k])
        std_acc = (sum((x - mean_acc) ** 2 for x in cv_results[k]) / len(cv_results[k])) ** 0.5
        print(f"    {k:<5} {mean_acc:>10.4f} {std_acc:>10.4f}")
        
        if mean_acc > best_mean:
            best_k = k
            best_mean = mean_acc
    
    print(f"\n[5] Best k from CV: {best_k} (mean accuracy: {best_mean:.4f})")
    
    return best_k


def demo_learning_rate_schedulers():
    """Demonstrate learning rate schedulers (for reference in training loops)."""
    print("\n" + "#" * 60)
    print("# Learning Rate Scheduler Demo")
    print("#" * 60)
    
    # StepLR
    print("\n[1] StepLR Scheduler:")
    print(f"    Initial LR: 0.1, Step size: 10, Gamma: 0.5")
    scheduler = StepLR(initial_lr=0.1, step_size=10, gamma=0.5)
    
    print(f"    {'Epoch':<8} {'LR':>10}")
    print(f"    {'-' * 8} {'-' * 10}")
    for epoch in [0, 5, 10, 15, 20, 25, 30]:
        lr = scheduler.step(epoch)
        print(f"    {epoch:<8} {lr:>10.6f}")
    
    # CosineAnnealingLR
    print("\n[2] Cosine Annealing Scheduler:")
    print(f"    Initial LR: 0.1, Min LR: 0.001, Max epochs: 50")
    scheduler = CosineAnnealingLR(initial_lr=0.1, min_lr=0.001, max_epochs=50)
    
    print(f"    {'Epoch':<8} {'LR':>10}")
    print(f"    {'-' * 8} {'-' * 10}")
    for epoch in [0, 10, 20, 30, 40, 50]:
        lr = scheduler.step(epoch)
        print(f"    {epoch:<8} {lr:>10.6f}")


def demo_feature_importance():
    """Demonstrate feature importance analysis using permutation."""
    print("\n" + "#" * 60)
    print("# Feature Importance Demo (Permutation-based)")
    print("#" * 60)
    
    import random
    random.seed(42)
    
    # Generate data
    X, y = generate_synthetic_data(n_samples=200, n_features=4, n_classes=3)
    
    # Split and standardize
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train_std, means, stds = standardize_matrix(X_train, axis=0)
    X_test_std = []
    for row in X_test:
        std_row = [(row[j] - means[j]) / stds[j] for j in range(len(row))]
        X_test_std.append(std_row)
    
    # Train baseline model
    knn = KNNClassifier(k=5)
    knn.fit(X_train_std, y_train)
    y_pred = knn.predict(X_test_std)
    baseline_accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n[1] Baseline accuracy: {baseline_accuracy:.4f}")
    
    # Permute each feature and measure accuracy drop
    print("\n[2] Feature importance (accuracy drop after permutation):")
    n_features = len(X_train_std[0])
    importance = []
    
    for feature_idx in range(n_features):
        # Create permuted test set
        X_test_permuted = [row.copy() for row in X_test_std]
        feature_values = [row[feature_idx] for row in X_test_permuted]
        random.shuffle(feature_values)
        for i, row in enumerate(X_test_permuted):
            row[feature_idx] = feature_values[i]
        
        # Evaluate
        y_pred_permuted = knn.predict(X_test_permuted)
        permuted_accuracy = accuracy_score(y_test, y_pred_permuted)
        importance_drop = baseline_accuracy - permuted_accuracy
        
        importance.append((feature_idx, importance_drop))
        print(f"    Feature {feature_idx}: {importance_drop:+.4f} "
              f"({'important' if importance_drop > 0.05 else 'less important'})")
    
    # Rank features
    importance.sort(key=lambda x: x[1], reverse=True)
    print(f"\n[3] Feature ranking (most to least important):")
    for rank, (feat_idx, imp) in enumerate(importance, 1):
        print(f"    {rank}. Feature {feat_idx} (importance: {imp:.4f})")


def main():
    """Run all advanced demos."""
    print("\n" + "=" * 60)
    print("AllToolkit - ML Utils Advanced Examples")
    print("End-to-End Machine Learning Pipeline")
    print("=" * 60)
    
    demo_knn_pipeline()
    demo_cross_validation()
    demo_learning_rate_schedulers()
    demo_feature_importance()
    
    print("\n" + "=" * 60)
    print("All advanced demos completed!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
