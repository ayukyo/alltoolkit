"""
Tests for Perceptron Utils.
"""

import math
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from perceptron_utils.mod import (
    Perceptron,
    MultiClassPerceptron,
    train_and_gate,
    train_or_gate,
    train_nand_gate,
    train_nor_gate,
    generate_linear_data
)


def test_perceptron_init():
    """Test perceptron initialization."""
    p = Perceptron(input_size=3)
    assert p.input_size == 3
    assert len(p.weights) == 3
    assert p.learning_rate == 0.1
    assert p.activation_name == 'step'
    assert not p._fitted
    print("✓ test_perceptron_init passed")


def test_perceptron_init_custom():
    """Test perceptron with custom parameters."""
    p = Perceptron(
        input_size=5,
        learning_rate=0.01,
        activation='sigmoid',
        random_seed=42
    )
    assert p.input_size == 5
    assert p.learning_rate == 0.01
    assert p.activation_name == 'sigmoid'
    # Check reproducibility
    p2 = Perceptron(input_size=5, random_seed=42)
    assert p.weights == p2.weights
    print("✓ test_perceptron_init_custom passed")


def test_perceptron_init_errors():
    """Test perceptron initialization errors."""
    try:
        Perceptron(input_size=0)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    try:
        Perceptron(input_size=3, learning_rate=0)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    # Unknown activation raises error when used
    p = Perceptron(input_size=3, activation='unknown')
    try:
        p.predict([1, 2, 3])
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("✓ test_perceptron_init_errors passed")


def test_activation_functions():
    """Test all activation functions."""
    # Step
    p = Perceptron(input_size=1, activation='step', random_seed=42)
    assert p._step(0) == 1.0
    assert p._step(-0.001) == 0.0
    assert p._step(100) == 1.0
    
    # Sigmoid
    p = Perceptron(input_size=1, activation='sigmoid', random_seed=42)
    assert abs(p._sigmoid(0) - 0.5) < 0.001
    assert p._sigmoid(-100) < 0.001
    assert p._sigmoid(100) > 0.999
    
    # ReLU
    p = Perceptron(input_size=1, activation='relu', random_seed=42)
    assert p._relu(-5) == 0
    assert p._relu(0) == 0
    assert p._relu(5) == 5
    
    # Tanh
    p = Perceptron(input_size=1, activation='tanh', random_seed=42)
    assert abs(p._tanh(0)) < 0.001
    assert p._tanh(10) > 0.999
    assert p._tanh(-10) < -0.999
    
    print("✓ test_activation_functions passed")


def test_net_input():
    """Test net input calculation."""
    p = Perceptron(input_size=2, random_seed=42)
    p.weights = [0.5, 0.5]
    p.bias = -0.5
    
    # net = 0.5*1 + 0.5*1 - 0.5 = 0.5
    assert abs(p.net_input([1, 1]) - 0.5) < 0.001
    
    # net = 0.5*0 + 0.5*0 - 0.5 = -0.5
    assert abs(p.net_input([0, 0]) - (-0.5)) < 0.001
    
    print("✓ test_net_input passed")


def test_predict():
    """Test prediction."""
    p = Perceptron(input_size=2, random_seed=42)
    p.weights = [1, 1]
    p.bias = -1.5
    
    # 1 + 1 - 1.5 = 0.5 >= 0 -> 1
    assert p.predict([1, 1]) == 1
    
    # 0 + 1 - 1.5 = -0.5 < 0 -> 0
    assert p.predict([0, 1]) == 0
    
    print("✓ test_predict passed")


def test_and_gate():
    """Test AND gate training."""
    p = train_and_gate()
    
    assert p.predict([0, 0]) == 0
    assert p.predict([0, 1]) == 0
    assert p.predict([1, 0]) == 0
    assert p.predict([1, 1]) == 1
    
    # Check accuracy
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 0, 0, 1]
    assert p.score(X, y) == 1.0
    
    print("✓ test_and_gate passed")


def test_or_gate():
    """Test OR gate training."""
    p = train_or_gate()
    
    assert p.predict([0, 0]) == 0
    assert p.predict([0, 1]) == 1
    assert p.predict([1, 0]) == 1
    assert p.predict([1, 1]) == 1
    
    print("✓ test_or_gate passed")


def test_nand_gate():
    """Test NAND gate training."""
    p = train_nand_gate()
    
    assert p.predict([0, 0]) == 1
    assert p.predict([0, 1]) == 1
    assert p.predict([1, 0]) == 1
    assert p.predict([1, 1]) == 0
    
    print("✓ test_nand_gate passed")


def test_nor_gate():
    """Test NOR gate training."""
    p = train_nor_gate()
    
    assert p.predict([0, 0]) == 1
    assert p.predict([0, 1]) == 0
    assert p.predict([1, 0]) == 0
    assert p.predict([1, 1]) == 0
    
    print("✓ test_nor_gate passed")


def test_fit_early_stopping():
    """Test training with early stopping."""
    p = Perceptron(input_size=2, random_seed=42)
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 0, 0, 1]  # AND gate
    
    p.fit(X, y, epochs=1000, early_stopping=True)
    
    assert len(p.training_history) < 1000  # Should stop early
    assert p._fitted
    assert p.score(X, y) == 1.0
    
    print("✓ test_fit_early_stopping passed")


def test_fit_online():
    """Test online training."""
    p = Perceptron(input_size=2, activation='sigmoid', random_seed=42)
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 0, 0, 1]  # AND gate
    
    p.fit_online(X, y, epochs=100, shuffle=True)
    
    assert p._fitted
    assert p.score(X, y) >= 0.75  # Should learn reasonably well
    
    print("✓ test_fit_online passed")


def test_predict_batch():
    """Test batch prediction."""
    p = train_and_gate()
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    
    predictions = p.predict_batch(X)
    assert predictions == [0, 0, 0, 1]
    
    print("✓ test_predict_batch passed")


def test_predict_proba():
    """Test probability prediction."""
    p = Perceptron(input_size=1, activation='sigmoid', random_seed=42)
    p.weights = [1]
    p.bias = 0
    
    # Sigmoid(0) = 0.5
    prob = p.predict_proba([0])
    assert abs(prob - 0.5) < 0.001
    
    # Large positive -> close to 1
    prob = p.predict_proba([10])
    assert prob > 0.99
    
    # Large negative -> close to 0
    prob = p.predict_proba([-10])
    assert prob < 0.01
    
    print("✓ test_predict_proba passed")


def test_decision_boundary():
    """Test decision boundary extraction."""
    p = Perceptron(input_size=3, random_seed=42)
    p.weights = [1, 2, 3]
    p.bias = -4
    
    weights, bias = p.decision_boundary()
    assert weights == [1, 2, 3]
    assert bias == -4
    
    print("✓ test_decision_boundary passed")


def test_get_line_2d():
    """Test 2D line extraction."""
    p = Perceptron(input_size=2, random_seed=42)
    p.weights = [1, 1]
    p.bias = -0.5
    
    slope, intercept = p.get_line_2d()
    # w[0]*x + w[1]*y + bias = 0
    # 1*x + 1*y - 0.5 = 0
    # y = -x + 0.5
    assert abs(slope - (-1)) < 0.001
    assert abs(intercept - 0.5) < 0.001
    
    print("✓ test_get_line_2d passed")


def test_get_line_2d_vertical():
    """Test 2D line extraction for vertical line."""
    p = Perceptron(input_size=2, random_seed=42)
    p.weights = [1, 0]  # No y dependence
    p.bias = -2
    
    slope, intercept = p.get_line_2d()
    assert slope == float('inf')
    assert abs(intercept - 2) < 0.001  # x = 2
    
    print("✓ test_get_line_2d_vertical passed")


def test_get_line_2d_error():
    """Test error for non-2D perceptron."""
    p = Perceptron(input_size=3)
    
    try:
        p.get_line_2d()
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("✓ test_get_line_2d_error passed")


def test_serialization():
    """Test to_dict and from_dict."""
    p1 = train_and_gate()
    
    # Serialize
    data = p1.to_dict()
    assert data['input_size'] == 2
    assert data['learning_rate'] == 0.1
    assert data['activation'] == 'step'
    assert 'weights' in data
    assert 'bias' in data
    assert data['fitted'] == True
    
    # Deserialize
    p2 = Perceptron.from_dict(data)
    assert p2.input_size == p1.input_size
    assert p2.weights == p1.weights
    assert p2.bias == p1.bias
    assert p2.predict([1, 1]) == 1
    assert p2.predict([0, 0]) == 0
    
    print("✓ test_serialization passed")


def test_copy():
    """Test perceptron copy."""
    p1 = train_and_gate()
    p2 = p1.copy()
    
    assert p1.weights == p2.weights
    assert p1.bias == p2.bias
    
    # Both should predict the same
    assert p1.predict([1, 1]) == p2.predict([1, 1])
    
    # Verify they are independent objects
    assert p1 is not p2
    assert p1.weights is not p2.weights
    
    print("✓ test_copy passed")


def test_reset():
    """Test perceptron reset."""
    p = train_and_gate()
    old_weights = p.weights.copy()
    
    p.reset(random_seed=42)
    
    assert p._fitted == False
    assert len(p.training_history) == 0
    # Weights should be different (random)
    assert p.weights != old_weights
    
    print("✓ test_reset passed")


def test_repr():
    """Test string representation."""
    p = Perceptron(input_size=3)
    assert "input_size=3" in repr(p)
    assert "not fitted" in repr(p)
    
    p.fit([[1, 1, 1]], [1], epochs=1)
    assert "fitted" in repr(p)
    
    print("✓ test_repr passed")


def test_generate_linear_data():
    """Test linear data generation."""
    X, y = generate_linear_data(num_samples=100, random_seed=42)
    
    assert len(X) == 100
    assert len(y) == 100
    assert all(len(x) == 2 for x in X)
    assert all(yi in [0, 1] for yi in y)
    
    # Check reproducibility
    X2, y2 = generate_linear_data(num_samples=100, random_seed=42)
    assert X == X2
    assert y == y2
    
    print("✓ test_generate_linear_data passed")


def test_generate_linear_data_noise():
    """Test linear data generation with noise."""
    X, y = generate_linear_data(num_samples=100, noise=0.5, random_seed=42)
    
    # With 50% noise, should have some "wrong" labels
    # Most points should still be correct
    # Just verify it runs without error
    assert len(X) == 100
    assert len(y) == 100
    
    print("✓ test_generate_linear_data_noise passed")


def test_generate_linear_data_multidim():
    """Test linear data generation with more features."""
    X, y = generate_linear_data(num_samples=50, num_features=5, random_seed=42)
    
    assert all(len(x) == 5 for x in X)
    
    print("✓ test_generate_linear_data_multidim passed")


def test_train_on_linear_data():
    """Test training on generated linear data."""
    X, y = generate_linear_data(num_samples=200, random_seed=42)
    
    p = Perceptron(input_size=2, learning_rate=0.1, random_seed=42)
    p.fit(X, y, epochs=100)
    
    accuracy = p.score(X, y)
    assert accuracy > 0.80  # Should achieve good accuracy
    
    print(f"✓ test_train_on_linear_data passed (accuracy={accuracy:.4f})")


# MultiClassPerceptron tests

def test_multiclass_init():
    """Test multi-class perceptron initialization."""
    mcp = MultiClassPerceptron(num_classes=3, input_size=2)
    
    assert mcp.num_classes == 3
    assert mcp.input_size == 2
    assert len(mcp.perceptrons) == 3
    
    print("✓ test_multiclass_init passed")


def test_multiclass_init_error():
    """Test multi-class perceptron initialization error."""
    try:
        MultiClassPerceptron(num_classes=1, input_size=2)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("✓ test_multiclass_init_error passed")


def test_multiclass_fit_predict():
    """Test multi-class training and prediction."""
    # Simple 3-class problem
    X = [
        [0, 0], [0.1, 0.1],  # Class 0
        [1, 0], [0.9, 0.1],  # Class 1
        [0, 1], [0.1, 0.9],  # Class 2
    ]
    y = [0, 0, 1, 1, 2, 2]
    
    mcp = MultiClassPerceptron(num_classes=3, input_size=2, random_seed=42)
    mcp.fit(X, y, epochs=100)
    
    # Should predict correctly for training data
    predictions = mcp.predict_batch(X)
    assert predictions == y
    
    print("✓ test_multiclass_fit_predict passed")


def test_multiclass_score():
    """Test multi-class accuracy."""
    X = [
        [0, 0], [0, 1], [1, 0], [1, 1],
        [0.5, 0.5], [0.2, 0.8], [0.8, 0.2]
    ]
    y = [0, 1, 2, 3, 0, 1, 2]
    
    mcp = MultiClassPerceptron(num_classes=4, input_size=2, random_seed=42)
    mcp.fit(X, y, epochs=200)
    
    accuracy = mcp.score(X, y)
    assert accuracy >= 0.7  # Should learn reasonably well
    
    print(f"✓ test_multiclass_score passed (accuracy={accuracy:.4f})")


def test_multiclass_serialization():
    """Test multi-class perceptron serialization."""
    X = [[0, 0], [1, 0], [0, 1], [1, 1]]
    y = [0, 1, 2, 0]
    
    mcp1 = MultiClassPerceptron(num_classes=3, input_size=2, random_seed=42)
    mcp1.fit(X, y, epochs=100)
    
    data = mcp1.to_dict()
    assert data['num_classes'] == 3
    assert len(data['perceptrons']) == 3
    
    mcp2 = MultiClassPerceptron.from_dict(data)
    assert mcp2.num_classes == mcp1.num_classes
    assert mcp2.predict([0, 0]) == mcp1.predict([0, 0])
    
    print("✓ test_multiclass_serialization passed")


def test_multiclass_repr():
    """Test multi-class perceptron string representation."""
    mcp = MultiClassPerceptron(num_classes=3, input_size=2)
    assert "num_classes=3" in repr(mcp)
    assert "not fitted" in repr(mcp)
    
    mcp.fit([[0, 0]], [0], epochs=1)
    assert "fitted" in repr(mcp)
    
    print("✓ test_multiclass_repr passed")


def test_xor_not_learnable():
    """Test that XOR is not learnable (as expected for single perceptron)."""
    p = Perceptron(input_size=2, random_seed=42)
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 1, 1, 0]  # XOR
    
    p.fit(X, y, epochs=1000, early_stopping=False)
    
    # XOR is not linearly separable, so accuracy should be < 1.0
    accuracy = p.score(X, y)
    assert accuracy < 1.0
    
    print(f"✓ test_xor_not_learnable passed (accuracy={accuracy:.4f}, as expected < 1.0)")


def test_sigmoid_activation_learning():
    """Test learning with sigmoid activation."""
    p = Perceptron(input_size=2, activation='sigmoid', learning_rate=0.5, random_seed=42)
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 0, 0, 1]  # AND gate
    
    p.fit_online(X, y, epochs=500)
    
    # Should learn AND gate reasonably well
    accuracy = p.score(X, y)
    assert accuracy >= 0.75
    
    print(f"✓ test_sigmoid_activation_learning passed (accuracy={accuracy:.4f})")


def test_tanh_activation_learning():
    """Test learning with tanh activation."""
    p = Perceptron(input_size=2, activation='tanh', learning_rate=0.5, random_seed=42)
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 1, 1, 1]  # OR gate
    
    p.fit_online(X, y, epochs=500)
    
    accuracy = p.score(X, y)
    assert accuracy >= 0.75
    
    print(f"✓ test_tanh_activation_learning passed (accuracy={accuracy:.4f})")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("Running Perceptron Utils Tests")
    print("="*60 + "\n")
    
    # Basic tests
    test_perceptron_init()
    test_perceptron_init_custom()
    test_perceptron_init_errors()
    test_activation_functions()
    test_net_input()
    test_predict()
    
    # Logic gate tests
    test_and_gate()
    test_or_gate()
    test_nand_gate()
    test_nor_gate()
    
    # Training tests
    test_fit_early_stopping()
    test_fit_online()
    
    # Prediction tests
    test_predict_batch()
    test_predict_proba()
    
    # Utility tests
    test_decision_boundary()
    test_get_line_2d()
    test_get_line_2d_vertical()
    test_get_line_2d_error()
    
    # Serialization tests
    test_serialization()
    test_copy()
    test_reset()
    test_repr()
    
    # Data generation tests
    test_generate_linear_data()
    test_generate_linear_data_noise()
    test_generate_linear_data_multidim()
    test_train_on_linear_data()
    
    # Multi-class tests
    test_multiclass_init()
    test_multiclass_init_error()
    test_multiclass_fit_predict()
    test_multiclass_score()
    test_multiclass_serialization()
    test_multiclass_repr()
    
    # Edge case tests
    test_xor_not_learnable()
    test_sigmoid_activation_learning()
    test_tanh_activation_learning()
    
    print("\n" + "="*60)
    print("All tests passed! ✓")
    print("="*60 + "\n")


if __name__ == '__main__':
    run_all_tests()