"""
AllToolkit - Python ML Utils Test Suite

Comprehensive tests for machine learning utilities covering:
- Data preprocessing (normalize, standardize, train_test_split)
- Classification metrics (accuracy, precision, recall, F1, confusion matrix)
- Regression metrics (MSE, RMSE, MAE, R², MAPE)
- Learning rate schedulers
- Distance metrics
- Activation functions
- Utility functions

Run: python ml_utils_test.py -v
"""

import unittest
import math
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Preprocessing
    normalize, normalize_matrix, standardize, standardize_matrix,
    train_test_split, k_fold_split,
    
    # Classification Metrics
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix_binary, confusion_matrix_multiclass,
    classification_report, ClassificationReport,
    
    # Regression Metrics
    mean_squared_error, root_mean_squared_error, mean_absolute_error,
    r2_score, mean_absolute_percentage_error,
    
    # Learning Rate Schedulers
    StepLR, ExponentialLR, CosineAnnealingLR, ReduceLROnPlateau,
    
    # Distance Metrics
    euclidean_distance, manhattan_distance, cosine_similarity, cosine_distance,
    
    # Activation Functions
    softmax, sigmoid, relu,
    
    # Utilities
    one_hot_encode, argmax, cross_entropy_loss, memoize,
)


# =============================================================================
# Preprocessing Tests
# =============================================================================

class TestNormalize(unittest.TestCase):
    """Tests for normalize function."""
    
    def test_normalize_basic(self):
        """Test basic normalization."""
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        normalized, min_v, max_v = normalize(data)
        
        self.assertAlmostEqual(normalized[0], 0.0)
        self.assertAlmostEqual(normalized[-1], 1.0)
        self.assertEqual(min_v, 1.0)
        self.assertEqual(max_v, 5.0)
    
    def test_normalize_with_known_bounds(self):
        """Test normalization with known min/max."""
        data = [2.0, 3.0, 4.0]
        normalized, min_v, max_v = normalize(data, min_val=0.0, max_val=10.0)
        
        self.assertAlmostEqual(normalized[0], 0.2)
        self.assertAlmostEqual(normalized[-1], 0.4)
        self.assertEqual(min_v, 0.0)
        self.assertEqual(max_v, 10.0)
    
    def test_normalize_empty_raises(self):
        """Test that empty vector raises ValueError."""
        with self.assertRaises(ValueError):
            normalize([])
    
    def test_normalize_identical_values_raises(self):
        """Test that identical values raise ValueError."""
        with self.assertRaises(ValueError):
            normalize([5.0, 5.0, 5.0])
    
    def test_normalize_negative_values(self):
        """Test normalization with negative values."""
        data = [-10.0, 0.0, 10.0]
        normalized, _, _ = normalize(data)
        
        self.assertAlmostEqual(normalized[0], 0.0)
        self.assertAlmostEqual(normalized[1], 0.5)
        self.assertAlmostEqual(normalized[2], 1.0)


class TestNormalizeMatrix(unittest.TestCase):
    """Tests for normalize_matrix function."""
    
    def test_normalize_matrix_columns(self):
        """Test column-wise normalization."""
        matrix = [[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]]
        normalized, min_vals, max_vals = normalize_matrix(matrix, axis=0)
        
        self.assertEqual(len(min_vals), 2)
        self.assertEqual(len(max_vals), 2)
        self.assertAlmostEqual(normalized[0][0], 0.0)
        self.assertAlmostEqual(normalized[-1][0], 1.0)
    
    def test_normalize_matrix_rows(self):
        """Test row-wise normalization."""
        matrix = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        normalized, min_vals, max_vals = normalize_matrix(matrix, axis=1)
        
        self.assertEqual(len(min_vals), 2)
        self.assertAlmostEqual(normalized[0][0], 0.0)
        self.assertAlmostEqual(normalized[0][-1], 1.0)
    
    def test_normalize_matrix_invalid_axis(self):
        """Test invalid axis raises ValueError."""
        with self.assertRaises(ValueError):
            normalize_matrix([[1.0, 2.0]], axis=2)


class TestStandardize(unittest.TestCase):
    """Tests for standardize function."""
    
    def test_standardize_basic(self):
        """Test basic standardization."""
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        standardized, mean, std = standardize(data)
        
        self.assertAlmostEqual(mean, 3.0)
        self.assertGreater(std, 0)
        # Standardized data should have mean ≈ 0
        std_mean = sum(standardized) / len(standardized)
        self.assertAlmostEqual(std_mean, 0.0, places=10)
    
    def test_standardize_empty_raises(self):
        """Test that empty vector raises ValueError."""
        with self.assertRaises(ValueError):
            standardize([])
    
    def test_standardize_zero_variance_raises(self):
        """Test that zero variance raises ValueError."""
        with self.assertRaises(ValueError):
            standardize([5.0, 5.0, 5.0])


class TestTrainTestSplit(unittest.TestCase):
    """Tests for train_test_split function."""
    
    def test_train_test_split_basic(self):
        """Test basic train/test split."""
        X = [[i] for i in range(100)]
        y = list(range(100))
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.assertEqual(len(X_train), 80)
        self.assertEqual(len(X_test), 20)
        self.assertEqual(len(y_train), 80)
        self.assertEqual(len(y_test), 20)
    
    def test_train_test_split_reproducibility(self):
        """Test split is reproducible with same seed."""
        X = list(range(100))
        
        result1 = train_test_split(X, test_size=0.2, random_state=42)
        result2 = train_test_split(X, test_size=0.2, random_state=42)
        
        self.assertEqual(result1, result2)
    
    def test_train_test_split_invalid_size(self):
        """Test invalid test_size raises ValueError."""
        with self.assertRaises(ValueError):
            train_test_split([1, 2, 3], test_size=1.5)
    
    def test_train_test_split_mismatched_lengths(self):
        """Test mismatched array lengths raise ValueError."""
        with self.assertRaises(ValueError):
            train_test_split([1, 2, 3], [1, 2], test_size=0.2)


class TestKFoldSplit(unittest.TestCase):
    """Tests for k_fold_split function."""
    
    def test_k_fold_split_basic(self):
        """Test basic k-fold split."""
        folds = k_fold_split(n_samples=10, k=5, random_state=42)
        
        self.assertEqual(len(folds), 5)
        
        # Check that each sample appears in test set exactly once
        all_test_indices = []
        for train_idx, test_idx in folds:
            all_test_indices.extend(test_idx)
        
        self.assertEqual(sorted(all_test_indices), list(range(10)))
    
    def test_k_fold_split_invalid_k(self):
        """Test invalid k raises ValueError."""
        with self.assertRaises(ValueError):
            k_fold_split(n_samples=10, k=1)


# =============================================================================
# Classification Metrics Tests
# =============================================================================

class TestAccuracyScore(unittest.TestCase):
    """Tests for accuracy_score function."""
    
    def test_accuracy_perfect(self):
        """Test perfect accuracy."""
        y_true = [1, 0, 1, 1, 0]
        y_pred = [1, 0, 1, 1, 0]
        
        self.assertEqual(accuracy_score(y_true, y_pred), 1.0)
    
    def test_accuracy_zero(self):
        """Test zero accuracy."""
        y_true = [1, 1, 1]
        y_pred = [0, 0, 0]
        
        self.assertEqual(accuracy_score(y_true, y_pred), 0.0)
    
    def test_accuracy_partial(self):
        """Test partial accuracy."""
        y_true = [1, 0, 1, 0]
        y_pred = [1, 0, 0, 1]
        
        self.assertEqual(accuracy_score(y_true, y_pred), 0.5)
    
    def test_accuracy_empty_raises(self):
        """Test empty lists raise ValueError."""
        with self.assertRaises(ValueError):
            accuracy_score([], [])


class TestPrecisionRecallF1(unittest.TestCase):
    """Tests for precision, recall, and F1 score."""
    
    def setUp(self):
        self.y_true = [1, 0, 1, 1, 0, 1, 0, 0]
        self.y_pred = [1, 0, 1, 0, 0, 1, 1, 0]
    
    def test_precision_binary(self):
        """Test binary precision."""
        precision = precision_score(self.y_true, self.y_pred)
        # TP=3, FP=1, precision = 3/4 = 0.75
        self.assertAlmostEqual(precision, 0.75)
    
    def test_recall_binary(self):
        """Test binary recall."""
        recall = recall_score(self.y_true, self.y_pred)
        # TP=3, FN=1, recall = 3/4 = 0.75
        self.assertAlmostEqual(recall, 0.75)
    
    def test_f1_binary(self):
        """Test binary F1 score."""
        f1 = f1_score(self.y_true, self.y_pred)
        # F1 = 2 * 0.75 * 0.75 / (0.75 + 0.75) = 0.75
        self.assertAlmostEqual(f1, 0.75)
    
    def test_precision_macro(self):
        """Test macro-averaged precision."""
        precision = precision_score(self.y_true, self.y_pred, average='macro')
        self.assertGreater(precision, 0)
        self.assertLessEqual(precision, 1)
    
    def test_recall_weighted(self):
        """Test weighted recall."""
        recall = recall_score(self.y_true, self.y_pred, average='weighted')
        self.assertGreater(recall, 0)
        self.assertLessEqual(recall, 1)


class TestConfusionMatrix(unittest.TestCase):
    """Tests for confusion matrix functions."""
    
    def test_confusion_matrix_binary(self):
        """Test binary confusion matrix."""
        y_true = [1, 0, 1, 1, 0, 0]
        y_pred = [1, 0, 1, 0, 0, 1]
        
        cm = confusion_matrix_binary(y_true, y_pred)
        
        # TN=2, FP=1, FN=1, TP=2
        self.assertEqual(cm.matrix[0][0], 2)  # TN
        self.assertEqual(cm.matrix[0][1], 1)  # FP
        self.assertEqual(cm.matrix[1][0], 1)  # FN
        self.assertEqual(cm.matrix[1][1], 2)  # TP
    
    def test_confusion_matrix_multiclass(self):
        """Test multi-class confusion matrix."""
        y_true = [0, 1, 2, 0, 1, 2]
        y_pred = [0, 1, 1, 0, 2, 2]
        
        cm = confusion_matrix_multiclass(y_true, y_pred)
        
        self.assertEqual(len(cm.matrix), 3)
        self.assertEqual(len(cm.labels), 3)
    
    def test_confusion_matrix_mismatched_raises(self):
        """Test mismatched lengths raise ValueError."""
        with self.assertRaises(ValueError):
            confusion_matrix_binary([1, 0, 1], [1, 0])


class TestClassificationReport(unittest.TestCase):
    """Tests for classification_report function."""
    
    def test_classification_report(self):
        """Test classification report generation."""
        y_true = [0, 1, 2, 0, 1, 2, 0, 1]
        y_pred = [0, 1, 1, 0, 2, 2, 0, 0]
        
        report = classification_report(y_true, y_pred)
        
        self.assertEqual(len(report), 3)  # 3 classes
        for label, metrics in report.items():
            self.assertIsInstance(metrics, ClassificationReport)
            self.assertGreaterEqual(metrics.precision, 0)
            self.assertGreaterEqual(metrics.recall, 0)
            self.assertGreaterEqual(metrics.f1_score, 0)
            self.assertGreater(metrics.support, 0)


# =============================================================================
# Regression Metrics Tests
# =============================================================================

class TestRegressionMetrics(unittest.TestCase):
    """Tests for regression metrics."""
    
    def setUp(self):
        self.y_true = [3.0, -0.5, 2.0, 7.0]
        self.y_pred = [2.5, 0.0, 2.0, 8.0]
    
    def test_mse(self):
        """Test mean squared error."""
        mse = mean_squared_error(self.y_true, self.y_pred)
        # ((0.5)^2 + (0.5)^2 + 0 + (-1)^2) / 4 = (0.25 + 0.25 + 0 + 1) / 4 = 0.375
        self.assertAlmostEqual(mse, 0.375)
    
    def test_rmse(self):
        """Test root mean squared error."""
        rmse = root_mean_squared_error(self.y_true, self.y_pred)
        self.assertAlmostEqual(rmse, math.sqrt(0.375))
    
    def test_mae(self):
        """Test mean absolute error."""
        mae = mean_absolute_error(self.y_true, self.y_pred)
        # (0.5 + 0.5 + 0 + 1) / 4 = 0.5
        self.assertAlmostEqual(mae, 0.5)
    
    def test_r2_perfect(self):
        """Test R² for perfect predictions."""
        y_true = [1.0, 2.0, 3.0]
        y_pred = [1.0, 2.0, 3.0]
        
        self.assertEqual(r2_score(y_true, y_pred), 1.0)
    
    def test_r2_actual(self):
        """Test R² for actual predictions."""
        r2 = r2_score(self.y_true, self.y_pred)
        self.assertLessEqual(r2, 1.0)
    
    def test_mape(self):
        """Test mean absolute percentage error."""
        y_true = [100.0, 200.0, 300.0]
        y_pred = [110.0, 190.0, 300.0]
        
        mape = mean_absolute_percentage_error(y_true, y_pred)
        # (10% + 5% + 0%) / 3 = 5%
        self.assertAlmostEqual(mape, 5.0, places=5)


# =============================================================================
# Learning Rate Scheduler Tests
# =============================================================================

class TestStepLR(unittest.TestCase):
    """Tests for StepLR scheduler."""
    
    def test_step_lr_decay(self):
        """Test StepLR decay pattern."""
        scheduler = StepLR(initial_lr=0.1, step_size=10, gamma=0.5)
        
        self.assertAlmostEqual(scheduler.step(0), 0.1)
        self.assertAlmostEqual(scheduler.step(9), 0.1)
        self.assertAlmostEqual(scheduler.step(10), 0.05)
        self.assertAlmostEqual(scheduler.step(20), 0.025)


class TestExponentialLR(unittest.TestCase):
    """Tests for ExponentialLR scheduler."""
    
    def test_exponential_lr_decay(self):
        """Test ExponentialLR decay pattern."""
        scheduler = ExponentialLR(initial_lr=0.1, gamma=0.9)
        
        self.assertAlmostEqual(scheduler.step(0), 0.1)
        self.assertAlmostEqual(scheduler.step(1), 0.09)
        self.assertAlmostEqual(scheduler.step(2), 0.081)


class TestCosineAnnealingLR(unittest.TestCase):
    """Tests for CosineAnnealingLR scheduler."""
    
    def test_cosine_annealing(self):
        """Test cosine annealing pattern."""
        scheduler = CosineAnnealingLR(initial_lr=0.1, min_lr=0.0, max_epochs=100)
        
        # Start at initial LR
        lr0 = scheduler.step(0)
        self.assertAlmostEqual(lr0, 0.1)
        
        # End near min LR
        lr_end = scheduler.step(100)
        self.assertAlmostEqual(lr_end, 0.0, places=10)


class TestReduceLROnPlateau(unittest.TestCase):
    """Tests for ReduceLROnPlateau scheduler."""
    
    def test_reduce_on_plateau_min(self):
        """Test ReduceLROnPlateau with min mode."""
        scheduler = ReduceLROnPlateau(initial_lr=0.1, factor=0.5, patience=3, mode='min')
        
        # Improving
        scheduler.step(1.0)
        scheduler.step(0.8)
        scheduler.step(0.6)
        
        self.assertAlmostEqual(scheduler.get_lr(), 0.1)  # No reduction yet
        
        # Not improving (need patience+1 steps without improvement)
        scheduler.step(0.6)  # cooldown: 2
        scheduler.step(0.6)  # cooldown: 1
        scheduler.step(0.6)  # cooldown: 0
        scheduler.step(0.6)  # cooldown: -1, LR reduced
        scheduler.step(0.6)  # cooldown: 3 (reset after reduction)
        
        self.assertLess(scheduler.get_lr(), 0.1)  # Should have reduced


# =============================================================================
# Distance Metrics Tests
# =============================================================================

class TestDistanceMetrics(unittest.TestCase):
    """Tests for distance metric functions."""
    
    def test_euclidean_distance(self):
        """Test Euclidean distance."""
        a = [0.0, 0.0]
        b = [3.0, 4.0]
        
        self.assertEqual(euclidean_distance(a, b), 5.0)
    
    def test_manhattan_distance(self):
        """Test Manhattan distance."""
        a = [0.0, 0.0]
        b = [3.0, 4.0]
        
        self.assertEqual(manhattan_distance(a, b), 7.0)
    
    def test_cosine_similarity_identical(self):
        """Test cosine similarity for identical vectors."""
        a = [1.0, 2.0, 3.0]
        b = [1.0, 2.0, 3.0]
        
        self.assertAlmostEqual(cosine_similarity(a, b), 1.0)
    
    def test_cosine_similarity_orthogonal(self):
        """Test cosine similarity for orthogonal vectors."""
        a = [1.0, 0.0]
        b = [0.0, 1.0]
        
        self.assertAlmostEqual(cosine_similarity(a, b), 0.0)
    
    def test_cosine_distance(self):
        """Test cosine distance."""
        a = [1.0, 0.0]
        b = [1.0, 0.0]
        
        self.assertAlmostEqual(cosine_distance(a, b), 0.0)


# =============================================================================
# Activation Function Tests
# =============================================================================

class TestActivationFunctions(unittest.TestCase):
    """Tests for activation functions."""
    
    def test_softmax(self):
        """Test softmax function."""
        logits = [1.0, 2.0, 3.0]
        probs = softmax(logits)
        
        # Sum should be 1
        self.assertAlmostEqual(sum(probs), 1.0)
        
        # Probabilities should be in (0, 1)
        for p in probs:
            self.assertGreater(p, 0)
            self.assertLess(p, 1)
        
        # Higher logit should have higher probability
        self.assertLess(probs[0], probs[1])
        self.assertLess(probs[1], probs[2])
    
    def test_sigmoid_scalar(self):
        """Test sigmoid with scalar input."""
        self.assertAlmostEqual(sigmoid(0), 0.5)
        self.assertGreater(sigmoid(10), 0.99)
        self.assertLess(sigmoid(-10), 0.01)
    
    def test_sigmoid_vector(self):
        """Test sigmoid with vector input."""
        result = sigmoid([-1.0, 0.0, 1.0])
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[1], 0.5)
    
    def test_relu(self):
        """Test ReLU function."""
        self.assertEqual(relu(-5.0), 0)
        self.assertEqual(relu(0), 0)
        self.assertEqual(relu(5.0), 5.0)
        
        result = relu([-1.0, 0.0, 1.0])
        self.assertEqual(result, [0, 0, 1.0])


# =============================================================================
# Utility Function Tests
# =============================================================================

class TestOneHotEncode(unittest.TestCase):
    """Tests for one_hot_encode function."""
    
    def test_one_hot_encode_basic(self):
        """Test basic one-hot encoding."""
        labels = [0, 1, 2]
        encoded = one_hot_encode(labels)
        
        self.assertEqual(encoded, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    
    def test_one_hot_encode_with_num_classes(self):
        """Test one-hot encoding with specified num_classes."""
        labels = [0, 1]
        encoded = one_hot_encode(labels, num_classes=4)
        
        self.assertEqual(len(encoded[0]), 4)
        self.assertEqual(encoded, [[1, 0, 0, 0], [0, 1, 0, 0]])


class TestArgmax(unittest.TestCase):
    """Tests for argmax function."""
    
    def test_argmax_basic(self):
        """Test basic argmax."""
        self.assertEqual(argmax([1.0, 3.0, 2.0]), 1)
    
    def test_argmax_first_occurrence(self):
        """Test argmax returns first occurrence."""
        self.assertEqual(argmax([1.0, 3.0, 3.0]), 1)
    
    def test_argmax_empty_raises(self):
        """Test empty vector raises ValueError."""
        with self.assertRaises(ValueError):
            argmax([])


class TestCrossEntropyLoss(unittest.TestCase):
    """Tests for cross_entropy_loss function."""
    
    def test_cross_entropy_perfect(self):
        """Test cross-entropy for perfect predictions."""
        predictions = [[1.0, 0.0], [0.0, 1.0]]
        targets = [0, 1]
        
        self.assertAlmostEqual(cross_entropy_loss(predictions, targets), 0.0)
    
    def test_cross_entropy_imperfect(self):
        """Test cross-entropy for imperfect predictions."""
        predictions = [[0.9, 0.1], [0.1, 0.9]]
        targets = [0, 1]
        
        loss = cross_entropy_loss(predictions, targets)
        self.assertGreater(loss, 0)


class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator."""
    
    def test_memoize_caches_results(self):
        """Test that memoize caches function results."""
        call_count = [0]
        
        @memoize
        def expensive_function(x):
            call_count[0] += 1
            return x * 2
        
        # First call
        result1 = expensive_function(5)
        self.assertEqual(result1, 10)
        self.assertEqual(call_count[0], 1)
        
        # Cached call
        result2 = expensive_function(5)
        self.assertEqual(result2, 10)
        self.assertEqual(call_count[0], 1)  # Should not increment
        
        # Different argument
        result3 = expensive_function(10)
        self.assertEqual(result3, 20)
        self.assertEqual(call_count[0], 2)
    
    def test_memoize_cache_clear(self):
        """Test memoize cache clearing."""
        @memoize
        def func(x):
            return x
        
        func(1)
        func(2)
        func.cache_clear()
        
        self.assertEqual(len(func.cache), 0)


# =============================================================================
# Integration Tests
# =============================================================================

class TestMLPipeline(unittest.TestCase):
    """Integration tests for complete ML pipeline."""
    
    def test_full_classification_pipeline(self):
        """Test complete classification pipeline."""
        # Generate sample data
        X = [[i, i*2] for i in range(100)]
        y = [0 if i < 50 else 1 for i in range(100)]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Normalize features
        X_train_norm, min_vals, max_vals = normalize_matrix(X_train, axis=0)
        
        # Simulate predictions (80% accuracy)
        y_pred = y_test.copy()
        for i in range(len(y_pred) // 5):
            y_pred[i] = 1 - y_pred[i]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        self.assertGreater(accuracy, 0.7)
        self.assertGreater(precision, 0.5)
        self.assertGreater(recall, 0.5)
        self.assertGreater(f1, 0.5)
    
    def test_full_regression_pipeline(self):
        """Test complete regression pipeline."""
        # Generate sample data
        y_true = [i * 2 + 1 for i in range(50)]
        y_pred = [y + (i % 3 - 1) for i, y in enumerate(y_true)]
        
        # Calculate metrics
        mse = mean_squared_error(y_true, y_pred)
        rmse = root_mean_squared_error(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        self.assertGreater(mse, 0)
        self.assertGreater(rmse, 0)
        self.assertGreater(mae, 0)
        self.assertGreater(r2, 0.9)  # Should be high for small perturbations


if __name__ == '__main__':
    unittest.main(verbosity=2)
