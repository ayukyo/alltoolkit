"""
Perceptron Utils - A zero-dependency implementation of the perceptron algorithm.

The perceptron is the simplest neural network - a single-layer binary classifier.
It learns to separate two classes by finding a hyperplane decision boundary.

Features:
- Single-layer perceptron for binary classification
- Configurable learning rate and epochs
- Multiple activation functions (step, sigmoid, ReLU, tanh)
- Support for batch and online learning
- Weight and bias management
- Model serialization (to_dict/from_dict)

Author: AllToolkit
"""

import math
import random
from typing import List, Optional, Tuple, Callable, Dict, Any


class Perceptron:
    """
    A single-layer perceptron for binary classification.
    
    The perceptron learns a linear decision boundary by adjusting weights
    based on classification errors during training.
    
    Example:
        >>> p = Perceptron(input_size=2)
        >>> X = [[0, 0], [0, 1], [1, 0], [1, 1]]
        >>> y = [0, 0, 0, 1]  # AND gate
        >>> p.fit(X, y, epochs=100)
        >>> p.predict([1, 1])
        1
    """
    
    def __init__(
        self,
        input_size: int,
        learning_rate: float = 0.1,
        activation: str = 'step',
        random_seed: Optional[int] = None
    ):
        """
        Initialize the perceptron.
        
        Args:
            input_size: Number of input features
            learning_rate: Step size for weight updates (default: 0.1)
            activation: Activation function ('step', 'sigmoid', 'relu', 'tanh')
            random_seed: Optional seed for reproducibility
        """
        if input_size <= 0:
            raise ValueError("input_size must be positive")
        if learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
            
        self.input_size = input_size
        self.learning_rate = learning_rate
        self.activation_name = activation
        
        if random_seed is not None:
            random.seed(random_seed)
            
        # Initialize weights with small random values
        self.weights = [random.uniform(-0.5, 0.5) for _ in range(input_size)]
        self.bias = random.uniform(-0.5, 0.5)
        
        # Training history
        self.training_history: List[Dict[str, Any]] = []
        self._fitted = False
        
    def _get_activation(self) -> Callable[[float], float]:
        """Get the activation function by name."""
        activations = {
            'step': self._step,
            'sigmoid': self._sigmoid,
            'relu': self._relu,
            'tanh': self._tanh,
        }
        if self.activation_name not in activations:
            raise ValueError(f"Unknown activation: {self.activation_name}")
        return activations[self.activation_name]
    
    @staticmethod
    def _step(x: float) -> float:
        """Step activation function (Heaviside)."""
        return 1.0 if x >= 0 else 0.0
    
    @staticmethod
    def _sigmoid(x: float) -> float:
        """Sigmoid activation function."""
        if x < -700:  # Prevent overflow
            return 0.0
        if x > 700:
            return 1.0
        return 1.0 / (1.0 + math.exp(-x))
    
    @staticmethod
    def _relu(x: float) -> float:
        """ReLU activation function."""
        return max(0.0, x)
    
    @staticmethod
    def _tanh(x: float) -> float:
        """Tanh activation function."""
        return math.tanh(x)
    
    def net_input(self, x: List[float]) -> float:
        """
        Calculate the net input (weighted sum plus bias).
        
        Args:
            x: Input feature vector
            
        Returns:
            Net input value
        """
        if len(x) != self.input_size:
            raise ValueError(f"Expected {self.input_size} features, got {len(x)}")
        return sum(w * xi for w, xi in zip(self.weights, x)) + self.bias
    
    def predict(self, x: List[float]) -> int:
        """
        Predict the class label for a single sample.
        
        Args:
            x: Input feature vector
            
        Returns:
            Predicted class (0 or 1)
        """
        net = self.net_input(x)
        activation = self._get_activation()
        output = activation(net)
        
        # For step activation, output is already 0 or 1
        # For other activations, threshold at 0.5
        if self.activation_name == 'step':
            return int(output)
        return 1 if output >= 0.5 else 0
    
    def predict_proba(self, x: List[float]) -> float:
        """
        Predict the probability for class 1.
        
        Only meaningful for sigmoid activation. For other activations,
        returns the raw activation value.
        
        Args:
            x: Input feature vector
            
        Returns:
            Probability or activation value
        """
        net = self.net_input(x)
        activation = self._get_activation()
        return activation(net)
    
    def predict_batch(self, X: List[List[float]]) -> List[int]:
        """
        Predict class labels for multiple samples.
        
        Args:
            X: List of input feature vectors
            
        Returns:
            List of predicted classes
        """
        return [self.predict(x) for x in X]
    
    def fit(
        self,
        X: List[List[float]],
        y: List[int],
        epochs: int = 100,
        early_stopping: bool = True,
        verbose: bool = False
    ) -> 'Perceptron':
        """
        Train the perceptron on the given dataset.
        
        Uses the perceptron learning rule: weights are updated only
        when a misclassification occurs.
        
        Args:
            X: Training features
            y: Target labels (0 or 1)
            epochs: Maximum number of training epochs
            early_stopping: Stop if no errors in an epoch
            verbose: Print training progress
            
        Returns:
            self (for method chaining)
        """
        if len(X) != len(y):
            raise ValueError("X and y must have the same length")
        if not X:
            raise ValueError("Training data cannot be empty")
            
        self.training_history = []
        
        for epoch in range(epochs):
            errors = 0
            
            for xi, target in zip(X, y):
                # Calculate prediction
                prediction = self.predict(xi)
                
                # Update weights if misclassified
                if prediction != target:
                    errors += 1
                    # Perceptron learning rule
                    error = target - prediction
                    for j in range(self.input_size):
                        self.weights[j] += self.learning_rate * error * xi[j]
                    self.bias += self.learning_rate * error
            
            # Calculate accuracy for this epoch
            accuracy = self.score(X, y)
            self.training_history.append({
                'epoch': epoch + 1,
                'errors': errors,
                'accuracy': accuracy
            })
            
            if verbose:
                print(f"Epoch {epoch + 1}/{epochs}: errors={errors}, accuracy={accuracy:.4f}")
            
            # Early stopping if no errors
            if early_stopping and errors == 0:
                if verbose:
                    print(f"Converged at epoch {epoch + 1}")
                break
                
        self._fitted = True
        return self
    
    def fit_online(
        self,
        X: List[List[float]],
        y: List[int],
        epochs: int = 100,
        shuffle: bool = True,
        verbose: bool = False
    ) -> 'Perceptron':
        """
        Train using online (stochastic) learning.
        
        Updates weights after each sample, which can be faster
        for large datasets.
        
        Args:
            X: Training features
            y: Target labels (0 or 1)
            epochs: Maximum number of training epochs
            shuffle: Shuffle data each epoch
            verbose: Print training progress
            
        Returns:
            self (for method chaining)
        """
        if len(X) != len(y):
            raise ValueError("X and y must have the same length")
            
        indices = list(range(len(X)))
        self.training_history = []
        
        for epoch in range(epochs):
            if shuffle:
                random.shuffle(indices)
                
            errors = 0
            for i in indices:
                xi = X[i]
                target = y[i]
                
                net = self.net_input(xi)
                activation = self._get_activation()
                output = activation(net)
                
                if self.activation_name == 'step':
                    prediction = int(output)
                else:
                    prediction = 1 if output >= 0.5 else 0
                
                if prediction != target:
                    errors += 1
                    # Update using gradient-like rule for non-step activations
                    if self.activation_name == 'sigmoid':
                        # Sigmoid derivative
                        delta = (target - output) * output * (1 - output)
                    elif self.activation_name == 'tanh':
                        # Tanh derivative
                        delta = (target - output) * (1 - output * output)
                    elif self.activation_name == 'relu':
                        # ReLU derivative
                        delta = (target - output) * (1.0 if net > 0 else 0.0)
                    else:
                        delta = target - prediction
                    
                    for j in range(self.input_size):
                        self.weights[j] += self.learning_rate * delta * xi[j]
                    self.bias += self.learning_rate * delta
            
            accuracy = self.score(X, y)
            self.training_history.append({
                'epoch': epoch + 1,
                'errors': errors,
                'accuracy': accuracy
            })
            
            if verbose:
                print(f"Epoch {epoch + 1}: errors={errors}, accuracy={accuracy:.4f}")
        
        self._fitted = True
        return self
    
    def score(self, X: List[List[float]], y: List[int]) -> float:
        """
        Calculate accuracy on the given dataset.
        
        Args:
            X: Test features
            y: True labels
            
        Returns:
            Accuracy (0.0 to 1.0)
        """
        if len(X) != len(y):
            raise ValueError("X and y must have the same length")
        if not X:
            return 0.0
            
        correct = sum(1 for xi, yi in zip(X, y) if self.predict(xi) == yi)
        return correct / len(X)
    
    def decision_boundary(self) -> Tuple[List[float], float]:
        """
        Get the decision boundary parameters.
        
        The decision boundary is the hyperplane where:
        w[0]*x[0] + w[1]*x[1] + ... + bias = 0
        
        Returns:
            Tuple of (weights, bias)
        """
        return self.weights.copy(), self.bias
    
    def get_line_2d(self) -> Tuple[float, float]:
        """
        Get line parameters for 2D visualization.
        
        For a 2D perceptron, returns (slope, intercept) of the decision boundary.
        
        Returns:
            Tuple of (slope, intercept)
            
        Raises:
            ValueError: If input_size is not 2
        """
        if self.input_size != 2:
            raise ValueError("get_line_2d only works for 2D perceptrons")
            
        # w[0]*x + w[1]*y + bias = 0
        # y = -(w[0]*x + bias) / w[1]
        # y = (-w[0]/w[1])*x - bias/w[1]
        
        if abs(self.weights[1]) < 1e-10:
            # Vertical line
            return float('inf'), -self.bias / self.weights[0]
            
        slope = -self.weights[0] / self.weights[1]
        intercept = -self.bias / self.weights[1]
        return slope, intercept
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the perceptron to a dictionary.
        
        Returns:
            Dictionary containing perceptron state
        """
        return {
            'input_size': self.input_size,
            'learning_rate': self.learning_rate,
            'activation': self.activation_name,
            'weights': self.weights,
            'bias': self.bias,
            'fitted': self._fitted
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Perceptron':
        """
        Deserialize a perceptron from a dictionary.
        
        Args:
            data: Dictionary from to_dict()
            
        Returns:
            Perceptron instance
        """
        p = cls(
            input_size=data['input_size'],
            learning_rate=data['learning_rate'],
            activation=data['activation']
        )
        p.weights = data['weights'].copy()  # Copy to avoid reference sharing
        p.bias = data['bias']
        p._fitted = data.get('fitted', True)
        return p
    
    def copy(self) -> 'Perceptron':
        """
        Create a copy of this perceptron.
        
        Returns:
            New Perceptron with same parameters
        """
        return self.from_dict(self.to_dict())
    
    def reset(self, random_seed: Optional[int] = None) -> None:
        """
        Reset weights to random values.
        
        Args:
            random_seed: Optional seed for reproducibility
        """
        if random_seed is not None:
            random.seed(random_seed)
        self.weights = [random.uniform(-0.5, 0.5) for _ in range(self.input_size)]
        self.bias = random.uniform(-0.5, 0.5)
        self.training_history = []
        self._fitted = False
    
    def __repr__(self) -> str:
        status = "fitted" if self._fitted else "not fitted"
        return f"Perceptron(input_size={self.input_size}, activation='{self.activation_name}', {status})"


class MultiClassPerceptron:
    """
    Multi-class perceptron using one-vs-all strategy.
    
    Trains one perceptron per class, each distinguishing
    that class from all others.
    
    Example:
        >>> mcp = MultiClassPerceptron(num_classes=3, input_size=2)
        >>> X = [[0, 0], [0, 1], [1, 0], [1, 1]]
        >>> y = [0, 1, 2, 0]  # 3 classes
        >>> mcp.fit(X, y, epochs=100)
        >>> mcp.predict([0.5, 0.5])
        0
    """
    
    def __init__(
        self,
        num_classes: int,
        input_size: int,
        learning_rate: float = 0.1,
        activation: str = 'step',
        random_seed: Optional[int] = None
    ):
        """
        Initialize multi-class perceptron.
        
        Args:
            num_classes: Number of classes
            input_size: Number of input features
            learning_rate: Learning rate for all perceptrons
            activation: Activation function for all perceptrons
            random_seed: Optional seed for reproducibility
        """
        if num_classes < 2:
            raise ValueError("num_classes must be at least 2")
            
        self.num_classes = num_classes
        self.input_size = input_size
        self.learning_rate = learning_rate
        
        # Create one perceptron per class
        self.perceptrons: List[Perceptron] = []
        for i in range(num_classes):
            seed = random_seed + i if random_seed is not None else None
            p = Perceptron(
                input_size=input_size,
                learning_rate=learning_rate,
                activation=activation,
                random_seed=seed
            )
            self.perceptrons.append(p)
        
        self._fitted = False
        
    def fit(
        self,
        X: List[List[float]],
        y: List[int],
        epochs: int = 100,
        verbose: bool = False
    ) -> 'MultiClassPerceptron':
        """
        Train all perceptrons using one-vs-all strategy.
        
        Args:
            X: Training features
            y: Target labels (0 to num_classes-1)
            epochs: Training epochs per perceptron
            verbose: Print training progress
            
        Returns:
            self (for method chaining)
        """
        for class_idx, p in enumerate(self.perceptrons):
            # Create binary labels: 1 for current class, 0 for others
            y_binary = [1 if yi == class_idx else 0 for yi in y]
            
            if verbose:
                print(f"Training perceptron for class {class_idx}")
            
            p.fit(X, y_binary, epochs=epochs, verbose=verbose)
        
        self._fitted = True
        return self
    
    def predict(self, x: List[float]) -> int:
        """
        Predict class using winner-takes-all strategy.
        
        Args:
            x: Input feature vector
            
        Returns:
            Predicted class (0 to num_classes-1)
        """
        # Get scores from all perceptrons
        scores = [p.predict_proba(x) for p in self.perceptrons]
        # Return class with highest score
        return scores.index(max(scores))
    
    def predict_batch(self, X: List[List[float]]) -> List[int]:
        """
        Predict classes for multiple samples.
        
        Args:
            X: List of input feature vectors
            
        Returns:
            List of predicted classes
        """
        return [self.predict(x) for x in X]
    
    def score(self, X: List[List[float]], y: List[int]) -> float:
        """
        Calculate accuracy.
        
        Args:
            X: Test features
            y: True labels
            
        Returns:
            Accuracy (0.0 to 1.0)
        """
        predictions = self.predict_batch(X)
        correct = sum(1 for pred, true in zip(predictions, y) if pred == true)
        return correct / len(y) if y else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            'num_classes': self.num_classes,
            'input_size': self.input_size,
            'learning_rate': self.learning_rate,
            'perceptrons': [p.to_dict() for p in self.perceptrons],
            'fitted': self._fitted
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MultiClassPerceptron':
        """Deserialize from dictionary."""
        mcp = cls(
            num_classes=data['num_classes'],
            input_size=data['input_size'],
            learning_rate=data['learning_rate']
        )
        mcp.perceptrons = [Perceptron.from_dict(p) for p in data['perceptrons']]
        mcp._fitted = data.get('fitted', True)
        return mcp
    
    def __repr__(self) -> str:
        status = "fitted" if self._fitted else "not fitted"
        return f"MultiClassPerceptron(num_classes={self.num_classes}, input_size={self.input_size}, {status})"


# Convenience functions

def train_and_gate(learning_rate: float = 0.1, epochs: int = 100) -> Perceptron:
    """Train a perceptron on the AND gate."""
    p = Perceptron(input_size=2, learning_rate=learning_rate, random_seed=42)
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 0, 0, 1]
    p.fit(X, y, epochs=epochs)
    return p


def train_or_gate(learning_rate: float = 0.1, epochs: int = 100) -> Perceptron:
    """Train a perceptron on the OR gate."""
    p = Perceptron(input_size=2, learning_rate=learning_rate, random_seed=42)
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 1, 1, 1]
    p.fit(X, y, epochs=epochs)
    return p


def train_nand_gate(learning_rate: float = 0.1, epochs: int = 100) -> Perceptron:
    """Train a perceptron on the NAND gate."""
    p = Perceptron(input_size=2, learning_rate=learning_rate, random_seed=42)
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [1, 1, 1, 0]
    p.fit(X, y, epochs=epochs)
    return p


def train_nor_gate(learning_rate: float = 0.1, epochs: int = 100) -> Perceptron:
    """Train a perceptron on the NOR gate."""
    p = Perceptron(input_size=2, learning_rate=learning_rate, random_seed=42)
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [1, 0, 0, 0]
    p.fit(X, y, epochs=epochs)
    return p


def generate_linear_data(
    num_samples: int = 100,
    num_features: int = 2,
    noise: float = 0.1,
    random_seed: Optional[int] = None
) -> Tuple[List[List[float]], List[int]]:
    """
    Generate linearly separable data for testing.
    
    Creates data where points above y=x are class 1,
    and points below are class 0.
    
    Args:
        num_samples: Number of samples to generate
        num_features: Number of features (must be at least 2)
        noise: Noise level for labels
        random_seed: Optional seed for reproducibility
        
    Returns:
        Tuple of (X, y)
    """
    if random_seed is not None:
        random.seed(random_seed)
    
    X = []
    y = []
    
    for _ in range(num_samples):
        # Generate random point
        features = [random.uniform(-1, 1) for _ in range(num_features)]
        
        # Class 1 if above the diagonal, 0 otherwise
        # For 2D: y > x -> class 1
        if num_features >= 2:
            label = 1 if features[1] > features[0] else 0
        else:
            label = 1 if features[0] > 0 else 0
        
        # Add noise
        if random.random() < noise:
            label = 1 - label
        
        X.append(features)
        y.append(label)
    
    return X, y


if __name__ == '__main__':
    # Quick demo
    print("=== Perceptron Utils Demo ===\n")
    
    # Train AND gate
    print("Training AND gate:")
    p_and = train_and_gate()
    print(f"  {p_and}")
    print(f"  Weights: {p_and.weights}")
    print(f"  Bias: {p_and.bias}")
    print(f"  Predictions:")
    for x in [[0, 0], [0, 1], [1, 0], [1, 1]]:
        print(f"    {x} -> {p_and.predict(x)}")
    
    print("\nTraining OR gate:")
    p_or = train_or_gate()
    print(f"  {p_or}")
    for x in [[0, 0], [0, 1], [1, 0], [1, 1]]:
        print(f"    {x} -> {p_or.predict(x)}")
    
    print("\nGenerating and training on linear data:")
    X, y = generate_linear_data(num_samples=200, random_seed=42)
    p = Perceptron(input_size=2, random_seed=42)
    p.fit(X, y, epochs=100, verbose=False)
    print(f"  Accuracy: {p.score(X, y):.4f}")
    print(f"  Decision boundary: {p.get_line_2d()}")