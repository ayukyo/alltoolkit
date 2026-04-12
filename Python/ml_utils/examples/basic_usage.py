"""
AllToolkit - ML Utils Basic Usage Examples

This file demonstrates basic usage of the ml_utils module.
Run: python basic_usage.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # Preprocessing
    normalize, standardize, train_test_split, k_fold_split,
    
    # Classification Metrics
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix_binary, classification_report,
    
    # Regression Metrics
    mean_squared_error, root_mean_squared_error, mean_absolute_error, r2_score,
    
    # Distance Metrics
    euclidean_distance, cosine_similarity,
    
    # Activation Functions
    softmax, sigmoid, relu, argmax,
)


def demo_classification_metrics():
    """Demonstrate classification metrics."""
    print("=" * 60)
    print("Classification Metrics Demo")
    print("=" * 60)
    
    # Sample predictions
    y_true = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
    y_pred = [1, 0, 1, 0, 0, 1, 1, 0, 1, 0]
    
    print(f"\nTrue labels:  {y_true}")
    print(f"Pred labels:  {y_pred}")
    print(f"\nMatches:      {sum(t == p for t, p in zip(y_true, y_pred))}/{len(y_true)}")
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    
    print(f"\n{'Metric':<15} {'Value':>10}")
    print("-" * 25)
    print(f"{'Accuracy':<15} {accuracy:>10.4f}")
    print(f"{'Precision':<15} {precision:>10.4f}")
    print(f"{'Recall':<15} {recall:>10.4f}")
    print(f"{'F1 Score':<15} {f1:>10.4f}")
    
    # Confusion matrix
    cm = confusion_matrix_binary(y_true, y_pred)
    print(f"\nConfusion Matrix:")
    print(f"  TN={cm.matrix[0][0]:>3}  FP={cm.matrix[0][1]:>3}")
    print(f"  FN={cm.matrix[1][0]:>3}  TP={cm.matrix[1][1]:>3}")
    
    # Classification report
    print(f"\nClassification Report:")
    report = classification_report(y_true, y_pred)
    for label, metrics in report.items():
        print(f"  Class {label}: P={metrics.precision:.3f}, R={metrics.recall:.3f}, F1={metrics.f1_score:.3f}, Support={metrics.support}")


def demo_regression_metrics():
    """Demonstrate regression metrics."""
    print("\n" + "=" * 60)
    print("Regression Metrics Demo")
    print("=" * 60)
    
    # Sample predictions
    y_true = [10.0, 20.0, 30.0, 40.0, 50.0]
    y_pred = [11.0, 19.0, 31.0, 38.0, 52.0]
    
    print(f"\nTrue values:  {y_true}")
    print(f"Pred values:  {y_pred}")
    print(f"Errors:       {[f'{t-p:+.1f}' for t, p in zip(y_true, y_pred)]}")
    
    # Calculate metrics
    mse = mean_squared_error(y_true, y_pred)
    rmse = root_mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    print(f"\n{'Metric':<15} {'Value':>10}")
    print("-" * 25)
    print(f"{'MSE':<15} {mse:>10.4f}")
    print(f"{'RMSE':<15} {rmse:>10.4f}")
    print(f"{'MAE':<15} {mae:>10.4f}")
    print(f"{'R² Score':<15} {r2:>10.4f}")


def demo_preprocessing():
    """Demonstrate data preprocessing."""
    print("\n" + "=" * 60)
    print("Data Preprocessing Demo")
    print("=" * 60)
    
    # Sample data
    data = [10.0, 20.0, 30.0, 40.0, 50.0]
    
    print(f"\nOriginal data: {data}")
    
    # Normalize
    normalized, min_v, max_v = normalize(data)
    print(f"\nNormalized (min={min_v}, max={max_v}):")
    print(f"  {[f'{x:.3f}' for x in normalized]}")
    
    # Standardize
    standardized, mean, std = standardize(data)
    print(f"\nStandardized (mean={mean:.2f}, std={std:.2f}):")
    print(f"  {[f'{x:.3f}' for x in standardized]}")
    
    # Verify standardized data properties
    std_mean = sum(standardized) / len(standardized)
    std_var = sum((x - std_mean) ** 2 for x in standardized) / len(standardized)
    print(f"\nVerification:")
    print(f"  Standardized mean: {std_mean:.10f} (should be ~0)")
    print(f"  Standardized var:  {std_var:.10f} (should be ~1)")


def demo_train_test_split():
    """Demonstrate train/test split."""
    print("\n" + "=" * 60)
    print("Train/Test Split Demo")
    print("=" * 60)
    
    # Sample data
    X = [[i, i*2] for i in range(20)]
    y = [i % 2 for i in range(20)]
    
    print(f"\nTotal samples: {len(X)}")
    print(f"Test size: 20%")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set:     {len(X_test)} samples")
    
    # Show first few samples
    print(f"\nFirst 3 training samples:")
    for i in range(3):
        print(f"  X={X_train[i]}, y={y_train[i]}")
    
    print(f"\nFirst 3 test samples:")
    for i in range(3):
        print(f"  X={X_test[i]}, y={y_test[i]}")


def demo_k_fold():
    """Demonstrate k-fold cross-validation."""
    print("\n" + "=" * 60)
    print("K-Fold Cross-Validation Demo")
    print("=" * 60)
    
    n_samples = 10
    k = 5
    
    print(f"\nTotal samples: {n_samples}")
    print(f"Number of folds: {k}")
    
    folds = k_fold_split(n_samples, k, random_state=42)
    
    for fold_idx, (train_idx, test_idx) in enumerate(folds):
        print(f"\nFold {fold_idx + 1}:")
        print(f"  Train indices: {train_idx}")
        print(f"  Test indices:  {test_idx}")


def demo_distance_metrics():
    """Demonstrate distance metrics."""
    print("\n" + "=" * 60)
    print("Distance Metrics Demo")
    print("=" * 60)
    
    # Sample vectors
    a = [1.0, 2.0, 3.0]
    b = [4.0, 5.0, 6.0]
    c = [1.0, 2.0, 3.0]  # Same as a
    
    print(f"\nVector a: {a}")
    print(f"Vector b: {b}")
    print(f"Vector c: {c} (same as a)")
    
    # Euclidean distance
    dist_ab = euclidean_distance(a, b)
    dist_ac = euclidean_distance(a, c)
    print(f"\nEuclidean Distance:")
    print(f"  d(a, b) = {dist_ab:.4f}")
    print(f"  d(a, c) = {dist_ac:.4f} (should be 0)")
    
    # Cosine similarity
    sim_ab = cosine_similarity(a, b)
    sim_ac = cosine_similarity(a, c)
    print(f"\nCosine Similarity:")
    print(f"  sim(a, b) = {sim_ab:.4f}")
    print(f"  sim(a, c) = {sim_ac:.4f} (should be 1)")


def demo_activation_functions():
    """Demonstrate activation functions."""
    print("\n" + "=" * 60)
    print("Activation Functions Demo")
    print("=" * 60)
    
    # Sample inputs
    logits = [2.0, 1.0, 0.1]
    scalar = 3.0
    hidden = [-2.0, -1.0, 0.0, 1.0, 2.0]
    
    print(f"\nLogits: {logits}")
    
    # Softmax
    probs = softmax(logits)
    print(f"\nSoftmax output:")
    print(f"  Probabilities: {[f'{p:.4f}' for p in probs]}")
    print(f"  Sum: {sum(probs):.4f} (should be 1)")
    print(f"  Predicted class: {argmax(probs)}")
    
    # Sigmoid
    sig = sigmoid(scalar)
    print(f"\nSigmoid({scalar}) = {sig:.4f}")
    
    # ReLU
    relu_out = relu(hidden)
    print(f"\nReLU input:  {hidden}")
    print(f"ReLU output: {relu_out}")


def main():
    """Run all demos."""
    print("\n" + "#" * 60)
    print("# AllToolkit - ML Utils Basic Usage Examples")
    print("#" * 60)
    
    demo_classification_metrics()
    demo_regression_metrics()
    demo_preprocessing()
    demo_train_test_split()
    demo_k_fold()
    demo_distance_metrics()
    demo_activation_functions()
    
    print("\n" + "=" * 60)
    print("All demos completed!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
