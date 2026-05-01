"""
Perceptron Utils - Usage Examples

This file demonstrates various use cases for the perceptron utilities:
1. Basic logic gates (AND, OR, NAND, NOR)
2. Training on custom data
3. Multi-class classification
4. Visualization helpers
5. Model persistence
"""

import sys
import os
import math

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from perceptron_utils.mod import (
    Perceptron,
    MultiClassPerceptron,
    train_and_gate,
    train_or_gate,
    train_nand_gate,
    train_nor_gate,
    generate_linear_data
)


def example_1_basic_logic_gates():
    """Example 1: Train perceptrons on basic logic gates."""
    print("\n" + "="*60)
    print("Example 1: Basic Logic Gates")
    print("="*60)
    
    # AND gate
    print("\n--- AND Gate ---")
    p_and = train_and_gate()
    print(f"Perceptron: {p_and}")
    print(f"Weights: {p_and.weights}")
    print(f"Bias: {p_and.bias}")
    print("\nTruth Table:")
    for x in [[0, 0], [0, 1], [1, 0], [1, 1]]:
        print(f"  AND{tuple(x)} = {p_and.predict(x)}")
    
    # OR gate
    print("\n--- OR Gate ---")
    p_or = train_or_gate()
    print(f"Weights: {p_or.weights}, Bias: {p_or.bias}")
    for x in [[0, 0], [0, 1], [1, 0], [1, 1]]:
        print(f"  OR{tuple(x)} = {p_or.predict(x)}")
    
    # NAND gate
    print("\n--- NAND Gate ---")
    p_nand = train_nand_gate()
    print(f"Weights: {p_nand.weights}, Bias: {p_nand.bias}")
    for x in [[0, 0], [0, 1], [1, 0], [1, 1]]:
        print(f"  NAND{tuple(x)} = {p_nand.predict(x)}")
    
    # NOR gate
    print("\n--- NOR Gate ---")
    p_nor = train_nor_gate()
    print(f"Weights: {p_nor.weights}, Bias: {p_nor.bias}")
    for x in [[0, 0], [0, 1], [1, 0], [1, 1]]:
        print(f"  NOR{tuple(x)} = {p_nor.predict(x)}")


def example_2_custom_dataset():
    """Example 2: Train on a custom dataset."""
    print("\n" + "="*60)
    print("Example 2: Custom Dataset")
    print("="*60)
    
    # Simple 2D dataset: points above the diagonal y=x are class 1
    X = [
        [0.1, 0.8],  # Above -> 1
        [0.2, 0.9],  # Above -> 1
        [0.8, 0.1],  # Below -> 0
        [0.9, 0.2],  # Below -> 0
        [0.3, 0.7],  # Above -> 1
        [0.7, 0.3],  # Below -> 0
        [0.4, 0.6],  # Above -> 1
        [0.6, 0.4],  # Below -> 0
    ]
    y = [1, 1, 0, 0, 1, 0, 1, 0]
    
    # Train perceptron
    p = Perceptron(input_size=2, learning_rate=0.1, random_seed=42)
    p.fit(X, y, epochs=100, verbose=False)
    
    print(f"\nTrained perceptron: {p}")
    print(f"Weights: {p.weights}")
    print(f"Bias: {p.bias}")
    
    # Get decision boundary
    slope, intercept = p.get_line_2d()
    print(f"Decision boundary: y = {slope:.4f}*x + {intercept:.4f}")
    
    # Test predictions
    print("\nPredictions:")
    test_points = [[0.2, 0.8], [0.8, 0.2], [0.5, 0.5]]
    for x in test_points:
        pred = p.predict(x)
        print(f"  {x} -> class {pred}")
    
    # Calculate accuracy
    accuracy = p.score(X, y)
    print(f"\nTraining accuracy: {accuracy:.2%}")


def example_3_generated_data():
    """Example 3: Train on generated linear data."""
    print("\n" + "="*60)
    print("Example 3: Generated Linear Data")
    print("="*60)
    
    # Generate training data
    X_train, y_train = generate_linear_data(
        num_samples=200,
        num_features=2,
        noise=0.05,
        random_seed=42
    )
    
    # Generate test data
    X_test, y_test = generate_linear_data(
        num_samples=50,
        num_features=2,
        noise=0.0,
        random_seed=123
    )
    
    # Train perceptron
    p = Perceptron(input_size=2, learning_rate=0.1, random_seed=42)
    p.fit(X_train, y_train, epochs=100, early_stopping=True, verbose=False)
    
    print(f"\nTraining samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Epochs trained: {len(p.training_history)}")
    
    # Evaluate
    train_acc = p.score(X_train, y_train)
    test_acc = p.score(X_test, y_test)
    print(f"\nTraining accuracy: {train_acc:.2%}")
    print(f"Test accuracy: {test_acc:.2%}")
    
    # Show decision boundary
    slope, intercept = p.get_line_2d()
    print(f"\nDecision boundary: y = {slope:.4f}*x + {intercept:.4f}")
    print("(Data was generated with true boundary: y = x)")


def example_4_multiclass():
    """Example 4: Multi-class classification."""
    print("\n" + "="*60)
    print("Example 4: Multi-Class Classification")
    print("="*60)
    
    # Create a simple 3-class problem
    # Class 0: bottom-left quadrant
    # Class 1: bottom-right quadrant
    # Class 2: top half
    X = [
        [-1, -1], [-0.5, -0.8], [-0.8, -0.5],  # Class 0
        [1, -1], [0.5, -0.8], [0.8, -0.5],     # Class 1
        [0, 1], [0.5, 0.8], [-0.5, 0.8],       # Class 2
    ]
    y = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    
    # Train multi-class perceptron
    mcp = MultiClassPerceptron(
        num_classes=3,
        input_size=2,
        learning_rate=0.1,
        random_seed=42
    )
    mcp.fit(X, y, epochs=200, verbose=False)
    
    print(f"\n{mcp}")
    
    # Test predictions
    print("\nPredictions:")
    test_points = [
        (-0.5, -0.5),  # Should be class 0
        (0.5, -0.5),   # Should be class 1
        (0, 0.5),      # Should be class 2
    ]
    for x in test_points:
        pred = mcp.predict(list(x))
        print(f"  {x} -> class {pred}")
    
    # Accuracy
    accuracy = mcp.score(X, y)
    print(f"\nTraining accuracy: {accuracy:.2%}")


def example_5_different_activations():
    """Example 5: Compare different activation functions."""
    print("\n" + "="*60)
    print("Example 5: Different Activation Functions")
    print("="*60)
    
    activations = ['step', 'sigmoid', 'relu', 'tanh']
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 0, 0, 1]  # AND gate
    
    print("\nTraining AND gate with different activations:\n")
    
    for activation in activations:
        p = Perceptron(
            input_size=2,
            activation=activation,
            learning_rate=0.5,
            random_seed=42
        )
        
        if activation == 'step':
            p.fit(X, y, epochs=100)
        else:
            p.fit_online(X, y, epochs=500)
        
        predictions = [p.predict(x) for x in X]
        correct = sum(1 for pred, true in zip(predictions, y) if pred == true)
        
        print(f"  {activation:8} activation: {correct}/4 correct, "
              f"weights={p.weights}, bias={p.bias:.4f}")


def example_6_model_persistence():
    """Example 6: Save and load model."""
    print("\n" + "="*60)
    print("Example 6: Model Persistence")
    print("="*60)
    
    # Train a model
    X, y = generate_linear_data(num_samples=100, random_seed=42)
    p1 = Perceptron(input_size=2, learning_rate=0.1, random_seed=42)
    p1.fit(X, y, epochs=50)
    
    print(f"\nOriginal model: {p1}")
    print(f"Weights: {p1.weights}")
    print(f"Bias: {p1.bias}")
    print(f"Accuracy: {p1.score(X, y):.2%}")
    
    # Serialize to dict (can be saved as JSON)
    model_data = p1.to_dict()
    print("\nSerialized model data:")
    print(f"  {model_data}")
    
    # Load from dict
    p2 = Perceptron.from_dict(model_data)
    print(f"\nLoaded model: {p2}")
    print(f"Accuracy (same): {p2.score(X, y):.2%}")
    
    # Verify predictions match
    test_point = [0.5, -0.3]
    assert p1.predict(test_point) == p2.predict(test_point)
    print(f"\nPredictions for {test_point}:")
    print(f"  Original: {p1.predict(test_point)}")
    print(f"  Loaded:   {p2.predict(test_point)}")


def example_7_training_history():
    """Example 7: Analyze training history."""
    print("\n" + "="*60)
    print("Example 7: Training History")
    print("="*60)
    
    X, y = generate_linear_data(num_samples=100, noise=0.1, random_seed=42)
    
    p = Perceptron(input_size=2, learning_rate=0.1, random_seed=42)
    p.fit(X, y, epochs=100, early_stopping=True, verbose=False)
    
    history = p.training_history
    
    print(f"\nTotal epochs: {len(history)}")
    print(f"Final accuracy: {history[-1]['accuracy']:.4f}")
    print(f"Final errors: {history[-1]['errors']}")
    
    # Show progress
    print("\nTraining progress:")
    for i in range(0, len(history), max(1, len(history) // 5)):
        h = history[i]
        print(f"  Epoch {h['epoch']:3d}: errors={h['errors']:3d}, "
              f"accuracy={h['accuracy']:.4f}")
    
    # Final state
    print(f"  Epoch {history[-1]['epoch']:3d}: errors={history[-1]['errors']:3d}, "
          f"accuracy={history[-1]['accuracy']:.4f}")


def example_8_probability_predictions():
    """Example 8: Probability predictions with sigmoid."""
    print("\n" + "="*60)
    print("Example 8: Probability Predictions")
    print("="*60)
    
    # Train with sigmoid for probability output
    p = Perceptron(input_size=2, activation='sigmoid', random_seed=42)
    
    X, y = generate_linear_data(num_samples=100, random_seed=42)
    p.fit_online(X, y, epochs=200)
    
    print(f"\nTrained with sigmoid activation: {p}")
    
    # Test points near and far from boundary
    test_points = [
        ([1, -1], "far below diagonal"),
        ([0.5, -0.5], "below diagonal"),
        ([0, 0], "on diagonal"),
        ([-0.5, 0.5], "above diagonal"),
        ([-1, 1], "far above diagonal"),
    ]
    
    print("\nProbability predictions:")
    for point, desc in test_points:
        prob = p.predict_proba(point)
        pred = p.predict(point)
        print(f"  {point} ({desc:20}): P(class 1) = {prob:.4f}, "
              f"prediction = {pred}")


def example_9_higher_dimensions():
    """Example 9: Perceptron with more than 2 features."""
    print("\n" + "="*60)
    print("Example 9: Higher Dimensional Data")
    print("="*60)
    
    # Generate 5D data
    X, y = generate_linear_data(num_samples=200, num_features=5, random_seed=42)
    
    p = Perceptron(input_size=5, learning_rate=0.1, random_seed=42)
    p.fit(X, y, epochs=100)
    
    print(f"\nTrained on {len(X)} samples with 5 features")
    print(f"Weights: {p.weights}")
    print(f"Bias: {p.bias}")
    
    accuracy = p.score(X, y)
    print(f"Training accuracy: {accuracy:.2%}")
    
    # Test prediction on new data
    test_point = [0.5, 0.2, 0.3, 0.1, 0.4]
    pred = p.predict(test_point)
    print(f"\nPrediction for {test_point}: class {pred}")


def example_10_multiclass_iris_like():
    """Example 10: Multi-class classification (Iris-like)."""
    print("\n" + "="*60)
    print("Example 10: Multi-Class (Iris-like Problem)")
    print("="*60)
    
    # Create a simple Iris-like dataset
    # Features: sepal_length, sepal_width, petal_length, petal_width
    # 3 classes, linearly separable
    import random
    random.seed(42)
    
    # Simplified version - 3 clusters
    X = []
    y = []
    
    # Class 0: small flowers (sepal small, petal small)
    for _ in range(30):
        X.append([
            random.uniform(4.5, 5.5),   # sepal_length
            random.uniform(3.0, 4.0),   # sepal_width
            random.uniform(1.0, 2.0),   # petal_length
            random.uniform(0.1, 0.5),   # petal_width
        ])
        y.append(0)
    
    # Class 1: medium flowers
    for _ in range(30):
        X.append([
            random.uniform(5.5, 6.5),
            random.uniform(2.5, 3.5),
            random.uniform(3.5, 4.5),
            random.uniform(1.0, 1.5),
        ])
        y.append(1)
    
    # Class 2: large flowers
    for _ in range(30):
        X.append([
            random.uniform(6.5, 7.5),
            random.uniform(3.0, 4.0),
            random.uniform(5.5, 6.5),
            random.uniform(2.0, 2.5),
        ])
        y.append(2)
    
    # Train multi-class perceptron
    mcp = MultiClassPerceptron(
        num_classes=3,
        input_size=4,
        learning_rate=0.1,
        random_seed=42
    )
    mcp.fit(X, y, epochs=200)
    
    print(f"\n{mcp}")
    print(f"Training samples per class: 30")
    
    # Evaluate
    accuracy = mcp.score(X, y)
    print(f"Training accuracy: {accuracy:.2%}")
    
    # Test on typical examples
    print("\nSample predictions:")
    samples = [
        ([5.0, 3.5, 1.5, 0.3], "Iris setosa-like"),
        ([6.0, 3.0, 4.0, 1.2], "Iris versicolor-like"),
        ([7.0, 3.5, 6.0, 2.2], "Iris virginica-like"),
    ]
    for features, desc in samples:
        pred = mcp.predict(features)
        print(f"  {desc}: class {pred}")


def main():
    """Run all examples."""
    print("\n" + "#"*60)
    print("# Perceptron Utils - Usage Examples")
    print("#"*60)
    
    example_1_basic_logic_gates()
    example_2_custom_dataset()
    example_3_generated_data()
    example_4_multiclass()
    example_5_different_activations()
    example_6_model_persistence()
    example_7_training_history()
    example_8_probability_predictions()
    example_9_higher_dimensions()
    example_10_multiclass_iris_like()
    
    print("\n" + "#"*60)
    print("# All examples completed!")
    print("#"*60 + "\n")


if __name__ == '__main__':
    main()