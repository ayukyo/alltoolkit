"""
AllToolkit - Python Machine Learning Utilities

A zero-dependency, production-ready machine learning utility module.
Provides data preprocessing, model evaluation metrics, and common ML operations.
All implemented using only Python standard library.

Author: AllToolkit
License: MIT
"""

import math
from typing import List, Tuple, Dict, Any, Optional, Union, Callable
from dataclasses import dataclass
from functools import wraps
import random
import copy


# =============================================================================
# Type Aliases
# =============================================================================

Vector = List[float]
Matrix = List[List[float]]
Label = Union[int, str]
Labels = List[Label]


# =============================================================================
# Data Preprocessing
# =============================================================================

def normalize(vector: Vector, min_val: Optional[float] = None, max_val: Optional[float] = None) -> Tuple[Vector, float, float]:
    """
    Normalize a vector to [0, 1] range using min-max scaling.
    
    Args:
        vector: Input vector to normalize
        min_val: Known minimum value (optional, computed if not provided)
        max_val: Known maximum value (optional, computed if not provided)
    
    Returns:
        Tuple of (normalized_vector, min_val, max_val)
    
    Raises:
        ValueError: If vector is empty or all values are identical
    """
    if not vector:
        raise ValueError("Cannot normalize empty vector")
    
    if min_val is None:
        min_val = min(vector)
    if max_val is None:
        max_val = max(vector)
    
    range_val = max_val - min_val
    if range_val == 0:
        raise ValueError("Cannot normalize: all values are identical")
    
    normalized = [(x - min_val) / range_val for x in vector]
    return normalized, min_val, max_val


def normalize_matrix(matrix: Matrix, axis: int = 0) -> Tuple[Matrix, List[float], List[float]]:
    """
    Normalize a matrix along specified axis.
    
    Args:
        matrix: Input matrix (list of lists)
        axis: 0 to normalize columns (features), 1 to normalize rows (samples)
    
    Returns:
        Tuple of (normalized_matrix, min_vals, max_vals)
    """
    if not matrix or not matrix[0]:
        raise ValueError("Cannot normalize empty matrix")
    
    if axis == 0:  # Normalize columns (features)
        n_features = len(matrix[0])
        min_vals = []
        max_vals = []
        
        for j in range(n_features):
            col = [matrix[i][j] for i in range(len(matrix))]
            _, min_v, max_v = normalize(col)
            min_vals.append(min_v)
            max_vals.append(max_v)
        
        normalized = []
        for row in matrix:
            norm_row = [(row[j] - min_vals[j]) / (max_vals[j] - min_vals[j]) for j in range(n_features)]
            normalized.append(norm_row)
        
        return normalized, min_vals, max_vals
    
    elif axis == 1:  # Normalize rows (samples)
        normalized = []
        min_vals = []
        max_vals = []
        
        for row in matrix:
            norm_row, min_v, max_v = normalize(row)
            normalized.append(norm_row)
            min_vals.append(min_v)
            max_vals.append(max_v)
        
        return normalized, min_vals, max_vals
    
    else:
        raise ValueError(f"Invalid axis: {axis}. Must be 0 or 1.")


def standardize(vector: Vector, mean: Optional[float] = None, std: Optional[float] = None) -> Tuple[Vector, float, float]:
    """
    Standardize a vector to have zero mean and unit variance (z-score normalization).
    
    Args:
        vector: Input vector to standardize
        mean: Known mean (optional, computed if not provided)
        std: Known standard deviation (optional, computed if not provided)
    
    Returns:
        Tuple of (standardized_vector, mean, std)
    
    Raises:
        ValueError: If vector is empty or has zero variance
    """
    if not vector:
        raise ValueError("Cannot standardize empty vector")
    
    if mean is None:
        mean = sum(vector) / len(vector)
    if std is None:
        variance = sum((x - mean) ** 2 for x in vector) / len(vector)
        std = math.sqrt(variance)
    
    if std == 0:
        raise ValueError("Cannot standardize: zero variance")
    
    standardized = [(x - mean) / std for x in vector]
    return standardized, mean, std


def standardize_matrix(matrix: Matrix, axis: int = 0) -> Tuple[Matrix, List[float], List[float]]:
    """
    Standardize a matrix along specified axis.
    
    Args:
        matrix: Input matrix (list of lists)
        axis: 0 to standardize columns (features), 1 to standardize rows (samples)
    
    Returns:
        Tuple of (standardized_matrix, means, stds)
    """
    if not matrix or not matrix[0]:
        raise ValueError("Cannot standardize empty matrix")
    
    if axis == 0:  # Standardize columns (features)
        n_features = len(matrix[0])
        means = []
        stds = []
        
        for j in range(n_features):
            col = [matrix[i][j] for i in range(len(matrix))]
            _, mean, std = standardize(col)
            means.append(mean)
            stds.append(std)
        
        standardized = []
        for row in matrix:
            std_row = [(row[j] - means[j]) / stds[j] for j in range(n_features)]
            standardized.append(std_row)
        
        return standardized, means, stds
    
    elif axis == 1:  # Standardize rows (samples)
        standardized = []
        means = []
        stds = []
        
        for row in matrix:
            std_row, mean, std = standardize(row)
            standardized.append(std_row)
            means.append(mean)
            stds.append(std)
        
        return standardized, means, stds
    
    else:
        raise ValueError(f"Invalid axis: {axis}. Must be 0 or 1.")


def train_test_split(
    *arrays: Union[Matrix, Vector, Labels],
    test_size: float = 0.2,
    random_state: Optional[int] = None
) -> List:
    """
    Split arrays into random train and test subsets.
    
    Args:
        *arrays: One or more arrays to split (X, y, etc.)
        test_size: Proportion of data for testing (0.0 to 1.0)
        random_state: Random seed for reproducibility
    
    Returns:
        List of split arrays: [X_train, X_test, y_train, y_test, ...]
    """
    if not arrays:
        raise ValueError("At least one array must be provided")
    
    n_samples = len(arrays[0])
    if not all(len(arr) == n_samples for arr in arrays):
        raise ValueError("All arrays must have the same length")
    
    if not 0.0 < test_size < 1.0:
        raise ValueError("test_size must be between 0 and 1")
    
    if random_state is not None:
        random.seed(random_state)
    
    indices = list(range(n_samples))
    random.shuffle(indices)
    
    split_idx = int(n_samples * (1 - test_size))
    train_indices = indices[:split_idx]
    test_indices = indices[split_idx:]
    
    result = []
    for arr in arrays:
        train = [arr[i] for i in train_indices]
        test = [arr[i] for i in test_indices]
        result.extend([train, test])
    
    return result


def k_fold_split(n_samples: int, k: int = 5, random_state: Optional[int] = None) -> List[Tuple[List[int], List[int]]]:
    """
    Generate k-fold cross-validation indices.
    
    Args:
        n_samples: Total number of samples
        k: Number of folds
        random_state: Random seed for reproducibility
    
    Returns:
        List of (train_indices, test_indices) tuples for each fold
    """
    if k <= 1:
        raise ValueError("k must be greater than 1")
    if k > n_samples:
        raise ValueError("k cannot be greater than n_samples")
    
    indices = list(range(n_samples))
    if random_state is not None:
        random.seed(random_state)
        random.shuffle(indices)
    
    fold_size = n_samples // k
    folds = []
    
    for i in range(k):
        start = i * fold_size
        end = start + fold_size if i < k - 1 else n_samples
        test_indices = indices[start:end]
        train_indices = indices[:start] + indices[end:]
        folds.append((train_indices, test_indices))
    
    return folds


# =============================================================================
# Classification Metrics
# =============================================================================

@dataclass
class ClassificationReport:
    """Classification report with precision, recall, and F1 score."""
    precision: float
    recall: float
    f1_score: float
    support: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'precision': self.precision,
            'recall': self.recall,
            'f1_score': self.f1_score,
            'support': self.support,
        }


@dataclass
class ConfusionMatrix:
    """Confusion matrix for binary or multi-class classification."""
    matrix: Matrix
    labels: List[Label]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'matrix': self.matrix,
            'labels': self.labels,
        }


def accuracy_score(y_true: Labels, y_pred: Labels) -> float:
    """
    Calculate accuracy score.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
    
    Returns:
        Accuracy as a float between 0 and 1
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    if not y_true:
        raise ValueError("Cannot calculate accuracy for empty lists")
    
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    return correct / len(y_true)


def confusion_matrix_binary(y_true: Labels, y_pred: Labels, pos_label: Label = 1) -> ConfusionMatrix:
    """
    Calculate confusion matrix for binary classification.
    
    Returns matrix in format:
        [[TN, FP],
         [FN, TP]]
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        pos_label: Positive class label
    
    Returns:
        ConfusionMatrix object
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    
    tn = fp = fn = tp = 0
    for t, p in zip(y_true, y_pred):
        if t == pos_label and p == pos_label:
            tp += 1
        elif t == pos_label and p != pos_label:
            fn += 1
        elif t != pos_label and p == pos_label:
            fp += 1
        else:
            tn += 1
    
    return ConfusionMatrix(
        matrix=[[tn, fp], [fn, tp]],
        labels=[0, pos_label]
    )


def confusion_matrix_multiclass(y_true: Labels, y_pred: Labels, labels: Optional[List[Label]] = None) -> ConfusionMatrix:
    """
    Calculate confusion matrix for multi-class classification.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        labels: List of labels (inferred if not provided)
    
    Returns:
        ConfusionMatrix object
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    
    if labels is None:
        labels = sorted(set(y_true) | set(y_pred))
    
    label_to_idx = {label: idx for idx, label in enumerate(labels)}
    n_classes = len(labels)
    
    matrix = [[0] * n_classes for _ in range(n_classes)]
    for t, p in zip(y_true, y_pred):
        if t in label_to_idx and p in label_to_idx:
            matrix[label_to_idx[t]][label_to_idx[p]] += 1
    
    return ConfusionMatrix(matrix=matrix, labels=labels)


def precision_score(y_true: Labels, y_pred: Labels, pos_label: Label = 1, average: str = 'binary') -> float:
    """
    Calculate precision score.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        pos_label: Positive class label
        average: 'binary', 'macro', 'micro', or 'weighted'
    
    Returns:
        Precision score
    """
    if average == 'binary':
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == pos_label and p == pos_label)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != pos_label and p == pos_label)
        
        if tp + fp == 0:
            return 0.0
        return tp / (tp + fp)
    
    elif average in ('macro', 'micro', 'weighted'):
        labels = list(set(y_true) | set(y_pred))
        precisions = []
        supports = []
        
        for label in labels:
            tp = sum(1 for t, p in zip(y_true, y_pred) if t == label and p == label)
            fp = sum(1 for t, p in zip(y_true, y_pred) if t != label and p == label)
            
            if tp + fp > 0:
                precisions.append(tp / (tp + fp))
            else:
                precisions.append(0.0)
            supports.append(sum(1 for t in y_true if t == label))
        
        if average == 'macro':
            return sum(precisions) / len(precisions)
        elif average == 'micro':
            total_tp = sum(1 for t, p in zip(y_true, y_pred) if t == p)
            total_fp = sum(1 for t, p in zip(y_true, y_pred) if t != p)
            return total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
        else:  # weighted
            total_support = sum(supports)
            if total_support == 0:
                return 0.0
            return sum(p * s for p, s in zip(precisions, supports)) / total_support
    
    else:
        raise ValueError(f"Invalid average: {average}")


def recall_score(y_true: Labels, y_pred: Labels, pos_label: Label = 1, average: str = 'binary') -> float:
    """
    Calculate recall score.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        pos_label: Positive class label
        average: 'binary', 'macro', 'micro', or 'weighted'
    
    Returns:
        Recall score
    """
    if average == 'binary':
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == pos_label and p == pos_label)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == pos_label and p != pos_label)
        
        if tp + fn == 0:
            return 0.0
        return tp / (tp + fn)
    
    elif average in ('macro', 'micro', 'weighted'):
        labels = list(set(y_true) | set(y_pred))
        recalls = []
        supports = []
        
        for label in labels:
            tp = sum(1 for t, p in zip(y_true, y_pred) if t == label and p == label)
            fn = sum(1 for t, p in zip(y_true, y_pred) if t == label and p != label)
            
            if tp + fn > 0:
                recalls.append(tp / (tp + fn))
            else:
                recalls.append(0.0)
            supports.append(sum(1 for t in y_true if t == label))
        
        if average == 'macro':
            return sum(recalls) / len(recalls)
        elif average == 'micro':
            total_tp = sum(1 for t, p in zip(y_true, y_pred) if t == p)
            total_fn = sum(1 for t, p in zip(y_true, y_pred) if t != p)
            return total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
        else:  # weighted
            total_support = sum(supports)
            if total_support == 0:
                return 0.0
            return sum(r * s for r, s in zip(recalls, supports)) / total_support
    
    else:
        raise ValueError(f"Invalid average: {average}")


def f1_score(y_true: Labels, y_pred: Labels, pos_label: Label = 1, average: str = 'binary') -> float:
    """
    Calculate F1 score (harmonic mean of precision and recall).
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        pos_label: Positive class label
        average: 'binary', 'macro', 'micro', or 'weighted'
    
    Returns:
        F1 score
    """
    precision = precision_score(y_true, y_pred, pos_label, average)
    recall = recall_score(y_true, y_pred, pos_label, average)
    
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def classification_report(y_true: Labels, y_pred: Labels, average: str = 'weighted') -> Dict[Label, ClassificationReport]:
    """
    Generate classification report with precision, recall, and F1 for each class.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        average: Not used for per-class report, included for API consistency
    
    Returns:
        Dictionary mapping labels to ClassificationReport objects
    """
    labels = sorted(set(y_true) | set(y_pred))
    report = {}
    
    for label in labels:
        precision = precision_score(y_true, y_pred, pos_label=label, average='binary')
        recall = recall_score(y_true, y_pred, pos_label=label, average='binary')
        f1 = f1_score(y_true, y_pred, pos_label=label, average='binary')
        support = sum(1 for t in y_true if t == label)
        
        report[label] = ClassificationReport(
            precision=precision,
            recall=recall,
            f1_score=f1,
            support=support
        )
    
    return report


# =============================================================================
# Regression Metrics
# =============================================================================

def mean_squared_error(y_true: Vector, y_pred: Vector) -> float:
    """
    Calculate Mean Squared Error (MSE).
    
    Args:
        y_true: Ground truth values
        y_pred: Predicted values
    
    Returns:
        MSE value
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    if not y_true:
        raise ValueError("Cannot calculate MSE for empty lists")
    
    return sum((t - p) ** 2 for t, p in zip(y_true, y_pred)) / len(y_true)


def root_mean_squared_error(y_true: Vector, y_pred: Vector) -> float:
    """
    Calculate Root Mean Squared Error (RMSE).
    
    Args:
        y_true: Ground truth values
        y_pred: Predicted values
    
    Returns:
        RMSE value
    """
    return math.sqrt(mean_squared_error(y_true, y_pred))


def mean_absolute_error(y_true: Vector, y_pred: Vector) -> float:
    """
    Calculate Mean Absolute Error (MAE).
    
    Args:
        y_true: Ground truth values
        y_pred: Predicted values
    
    Returns:
        MAE value
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    if not y_true:
        raise ValueError("Cannot calculate MAE for empty lists")
    
    return sum(abs(t - p) for t, p in zip(y_true, y_pred)) / len(y_true)


def r2_score(y_true: Vector, y_pred: Vector) -> float:
    """
    Calculate R-squared (coefficient of determination).
    
    Args:
        y_true: Ground truth values
        y_pred: Predicted values
    
    Returns:
        R² value (can be negative for poor models)
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    if not y_true:
        raise ValueError("Cannot calculate R² for empty lists")
    
    mean_y = sum(y_true) / len(y_true)
    ss_tot = sum((t - mean_y) ** 2 for t in y_true)
    ss_res = sum((t - p) ** 2 for t, p in zip(y_true, y_pred))
    
    if ss_tot == 0:
        return 1.0 if ss_res == 0 else 0.0
    
    return 1 - (ss_res / ss_tot)


def mean_absolute_percentage_error(y_true: Vector, y_pred: Vector) -> float:
    """
    Calculate Mean Absolute Percentage Error (MAPE).
    
    Args:
        y_true: Ground truth values
        y_pred: Predicted values
    
    Returns:
        MAPE as a percentage (0-100)
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    if not y_true:
        raise ValueError("Cannot calculate MAPE for empty lists")
    
    errors = []
    for t, p in zip(y_true, y_pred):
        if t == 0:
            continue  # Skip zero values to avoid division by zero
        errors.append(abs((t - p) / t) * 100)
    
    if not errors:
        return 0.0
    return sum(errors) / len(errors)


# =============================================================================
# Learning Rate Schedulers
# =============================================================================

class LearningRateScheduler:
    """Learning rate schedulers for training loops."""
    
    def __init__(self, initial_lr: float = 0.001):
        self.initial_lr = initial_lr
        self.current_lr = initial_lr
    
    def step(self, epoch: int) -> float:
        """Update and return learning rate for given epoch."""
        raise NotImplementedError
    
    def get_lr(self) -> float:
        """Get current learning rate."""
        return self.current_lr
    
    def reset(self) -> None:
        """Reset to initial learning rate."""
        self.current_lr = self.initial_lr


class StepLR(LearningRateScheduler):
    """Step learning rate scheduler - decay by gamma every step_size epochs."""
    
    def __init__(self, initial_lr: float = 0.001, step_size: int = 30, gamma: float = 0.1):
        super().__init__(initial_lr)
        self.step_size = step_size
        self.gamma = gamma
    
    def step(self, epoch: int) -> float:
        self.current_lr = self.initial_lr * (self.gamma ** (epoch // self.step_size))
        return self.current_lr


class ExponentialLR(LearningRateScheduler):
    """Exponential learning rate scheduler - decay by gamma every epoch."""
    
    def __init__(self, initial_lr: float = 0.001, gamma: float = 0.95):
        super().__init__(initial_lr)
        self.gamma = gamma
    
    def step(self, epoch: int) -> float:
        self.current_lr = self.initial_lr * (self.gamma ** epoch)
        return self.current_lr


class CosineAnnealingLR(LearningRateScheduler):
    """Cosine annealing learning rate scheduler."""
    
    def __init__(self, initial_lr: float = 0.001, min_lr: float = 0.0, max_epochs: int = 100):
        super().__init__(initial_lr)
        self.min_lr = min_lr
        self.max_epochs = max_epochs
    
    def step(self, epoch: int) -> float:
        epoch = min(epoch, self.max_epochs)
        self.current_lr = self.min_lr + 0.5 * (self.initial_lr - self.min_lr) * (
            1 + math.cos(math.pi * epoch / self.max_epochs)
        )
        return self.current_lr


class ReduceLROnPlateau(LearningRateScheduler):
    """Reduce learning rate when a metric has stopped improving."""
    
    def __init__(
        self,
        initial_lr: float = 0.001,
        factor: float = 0.1,
        patience: int = 10,
        min_lr: float = 1e-6,
        mode: str = 'min'
    ):
        super().__init__(initial_lr)
        self.factor = factor
        self.patience = patience
        self.min_lr = min_lr
        self.mode = mode
        self.best_value = float('inf') if mode == 'min' else float('-inf')
        self.cooldown_counter = 0
        self._best_lr = initial_lr
    
    def step(self, metric: float) -> float:
        """
        Update learning rate based on metric value.
        
        Args:
            metric: Current metric value (loss, accuracy, etc.)
        
        Returns:
            Updated learning rate
        """
        is_improved = (self.mode == 'min' and metric < self.best_value) or \
                      (self.mode == 'max' and metric > self.best_value)
        
        if is_improved:
            self.best_value = metric
            self._best_lr = self.current_lr
            self.cooldown_counter = self.patience
        else:
            if self.cooldown_counter > 0:
                self.cooldown_counter -= 1
            else:
                self.cooldown_counter -= 1
                if self.cooldown_counter < 0:
                    new_lr = max(self.current_lr * self.factor, self.min_lr)
                    if new_lr < self.current_lr:
                        self.current_lr = new_lr
                    self.cooldown_counter = self.patience
        
        return self.current_lr


# =============================================================================
# Distance Metrics
# =============================================================================

def euclidean_distance(a: Vector, b: Vector) -> float:
    """Calculate Euclidean distance between two vectors."""
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def manhattan_distance(a: Vector, b: Vector) -> float:
    """Calculate Manhattan (L1) distance between two vectors."""
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    return sum(abs(x - y) for x, y in zip(a, b))


def cosine_similarity(a: Vector, b: Vector) -> float:
    """Calculate cosine similarity between two vectors."""
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x ** 2 for x in a))
    norm_b = math.sqrt(sum(x ** 2 for x in b))
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)


def cosine_distance(a: Vector, b: Vector) -> float:
    """Calculate cosine distance (1 - cosine_similarity) between two vectors."""
    return 1 - cosine_similarity(a, b)


# =============================================================================
# Utility Functions
# =============================================================================

def softmax(logits: Vector) -> Vector:
    """
    Apply softmax function to convert logits to probabilities.
    
    Args:
        logits: Input logits (raw scores)
    
    Returns:
        Probability distribution (sums to 1)
    """
    if not logits:
        return []
    
    # Subtract max for numerical stability
    max_logit = max(logits)
    exp_logits = [math.exp(x - max_logit) for x in logits]
    sum_exp = sum(exp_logits)
    
    return [x / sum_exp for x in exp_logits]


def sigmoid(x: Union[float, Vector]) -> Union[float, Vector]:
    """
    Apply sigmoid function.
    
    Args:
        x: Input value or vector
    
    Returns:
        Sigmoid output(s) in range (0, 1)
    """
    if isinstance(x, (int, float)):
        return 1 / (1 + math.exp(-x))
    else:
        return [1 / (1 + math.exp(-xi)) for xi in x]


def relu(x: Union[float, Vector]) -> Union[float, Vector]:
    """
    Apply ReLU (Rectified Linear Unit) activation.
    
    Args:
        x: Input value or vector
    
    Returns:
        ReLU output(s)
    """
    if isinstance(x, (int, float)):
        return max(0, x)
    else:
        return [max(0, xi) for xi in x]


def one_hot_encode(labels: Labels, num_classes: Optional[int] = None) -> Matrix:
    """
    Encode labels as one-hot vectors.
    
    Args:
        labels: List of labels (integers)
        num_classes: Total number of classes (inferred if not provided)
    
    Returns:
        Matrix of one-hot encoded vectors
    """
    if not labels:
        return []
    
    if num_classes is None:
        num_classes = max(labels) + 1
    
    encoded = []
    for label in labels:
        vector = [0] * num_classes
        vector[label] = 1
        encoded.append(vector)
    
    return encoded


def argmax(vector: Vector) -> int:
    """Return index of maximum value in vector."""
    if not vector:
        raise ValueError("Cannot find argmax of empty vector")
    return max(range(len(vector)), key=lambda i: vector[i])


def cross_entropy_loss(predictions: Matrix, targets: Vector) -> float:
    """
    Calculate cross-entropy loss.
    
    Args:
        predictions: Predicted probabilities (matrix of probability distributions)
        targets: True class indices
    
    Returns:
        Cross-entropy loss value
    """
    if len(predictions) != len(targets):
        raise ValueError("Predictions and targets must have the same length")
    if not predictions:
        raise ValueError("Cannot calculate loss for empty predictions")
    
    epsilon = 1e-15  # For numerical stability
    loss = 0.0
    
    for pred, target in zip(predictions, targets):
        prob = max(pred[int(target)], epsilon)
        loss -= math.log(prob)
    
    return loss / len(predictions)


# =============================================================================
# Convenience Functions
# =============================================================================

def _get_global_cache() -> Dict[str, Any]:
    """Get global cache for memoization."""
    if not hasattr(_get_global_cache, 'cache'):
        _get_global_cache.cache = {}
    return _get_global_cache.cache


def memoize(func: Callable) -> Callable:
    """
    Simple memoization decorator for pure functions.
    
    Args:
        func: Function to memoize
    
    Returns:
        Memoized function
    """
    cache = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    wrapper.cache = cache
    wrapper.cache_clear = lambda: cache.clear()
    return wrapper


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Preprocessing
    'normalize', 'normalize_matrix',
    'standardize', 'standardize_matrix',
    'train_test_split', 'k_fold_split',
    
    # Classification Metrics
    'accuracy_score', 'precision_score', 'recall_score', 'f1_score',
    'confusion_matrix_binary', 'confusion_matrix_multiclass',
    'classification_report', 'ClassificationReport', 'ConfusionMatrix',
    
    # Regression Metrics
    'mean_squared_error', 'root_mean_squared_error',
    'mean_absolute_error', 'r2_score', 'mean_absolute_percentage_error',
    
    # Learning Rate Schedulers
    'LearningRateScheduler', 'StepLR', 'ExponentialLR',
    'CosineAnnealingLR', 'ReduceLROnPlateau',
    
    # Distance Metrics
    'euclidean_distance', 'manhattan_distance',
    'cosine_similarity', 'cosine_distance',
    
    # Activation Functions
    'softmax', 'sigmoid', 'relu',
    
    # Utilities
    'one_hot_encode', 'argmax', 'cross_entropy_loss',
    'memoize',
]


if __name__ == '__main__':
    # Quick demo
    print("AllToolkit - ML Utils Demo")
    print("=" * 50)
    
    # Demo: Classification Metrics
    y_true = [1, 0, 1, 1, 0, 1, 0, 0]
    y_pred = [1, 0, 1, 0, 0, 1, 1, 0]
    
    print(f"\nClassification Demo:")
    print(f"True labels:  {y_true}")
    print(f"Pred labels:  {y_pred}")
    print(f"Accuracy:     {accuracy_score(y_true, y_pred):.4f}")
    print(f"Precision:    {precision_score(y_true, y_pred):.4f}")
    print(f"Recall:       {recall_score(y_true, y_pred):.4f}")
    print(f"F1 Score:     {f1_score(y_true, y_pred):.4f}")
    
    cm = confusion_matrix_binary(y_true, y_pred)
    print(f"\nConfusion Matrix:")
    print(f"  {cm.matrix[0]}")
    print(f"  {cm.matrix[1]}")
    
    # Demo: Regression Metrics
    y_true_reg = [3.0, -0.5, 2.0, 7.0]
    y_pred_reg = [2.5, 0.0, 2.0, 8.0]
    
    print(f"\nRegression Demo:")
    print(f"True values:  {y_true_reg}")
    print(f"Pred values:  {y_pred_reg}")
    print(f"MSE:          {mean_squared_error(y_true_reg, y_pred_reg):.4f}")
    print(f"RMSE:         {root_mean_squared_error(y_true_reg, y_pred_reg):.4f}")
    print(f"MAE:          {mean_absolute_error(y_true_reg, y_pred_reg):.4f}")
    print(f"R² Score:     {r2_score(y_true_reg, y_pred_reg):.4f}")
    
    # Demo: Preprocessing
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    normalized, min_v, max_v = normalize(data)
    standardized, mean, std = standardize(data)
    
    print(f"\nPreprocessing Demo:")
    print(f"Original:     {data}")
    print(f"Normalized:   {[f'{x:.3f}' for x in normalized]}")
    print(f"Standardized: {[f'{x:.3f}' for x in standardized]}")
    
    # Demo: Learning Rate Scheduler
    print(f"\nLearning Rate Scheduler Demo (StepLR):")
    scheduler = StepLR(initial_lr=0.1, step_size=10, gamma=0.5)
    for epoch in [0, 10, 20, 30]:
        lr = scheduler.step(epoch)
        print(f"  Epoch {epoch:2d}: LR = {lr:.6f}")
    
    print("\n" + "=" * 50)
    print("Demo complete!")
