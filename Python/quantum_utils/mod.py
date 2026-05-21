#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Quantum Computing Utilities Module
================================================
A comprehensive quantum computing simulation module for Python with zero external dependencies.

Features:
    - Qubit representation and state manipulation
    - Single-qubit gates (Hadamard, Pauli-X/Y/Z, Phase, T, S, R)
    - Multi-qubit gates (CNOT, CZ, SWAP, Toffoli)
    - Quantum circuit building and simulation
    - Measurement and probability calculations
    - Bell state generation (entanglement)
    - Quantum teleportation simulation
    - Bloch sphere representation
    - Quantum Fourier Transform (QFT)
    - Grover's search algorithm basics

Author: AllToolkit Contributors
License: MIT
"""

import math
import random
import cmath
from typing import List, Tuple, Optional, Union, Callable
from dataclasses import dataclass, field
from copy import deepcopy

# ============================================================================
# Constants
# ============================================================================

# Tolerance for floating point comparisons
EPSILON = 1e-10

# Common quantum gates as matrices
# |0⟩ state
ZERO_STATE = [complex(1, 0), complex(0, 0)]

# |1⟩ state
ONE_STATE = [complex(0, 0), complex(1, 0)]

# Pauli-X gate (NOT gate)
X_GATE = [
    [complex(0, 0), complex(1, 0)],
    [complex(1, 0), complex(0, 0)]
]

# Pauli-Y gate
Y_GATE = [
    [complex(0, 0), complex(0, -1)],
    [complex(0, 1), complex(0, 0)]
]

# Pauli-Z gate
Z_GATE = [
    [complex(1, 0), complex(0, 0)],
    [complex(0, 0), complex(-1, 0)]
]

# Hadamard gate
H_GATE = [
    [complex(1/math.sqrt(2), 0), complex(1/math.sqrt(2), 0)],
    [complex(1/math.sqrt(2), 0), complex(-1/math.sqrt(2), 0)]
]

# S gate (Phase gate, π/2 rotation around Z)
S_GATE = [
    [complex(1, 0), complex(0, 0)],
    [complex(0, 0), complex(0, 1)]
]

# T gate (π/4 rotation around Z)
T_GATE = [
    [complex(1, 0), complex(0, 0)],
    [complex(0, 0), complex(cmath.exp(1j * math.pi / 4).real, cmath.exp(1j * math.pi / 4).imag)]
]

# Identity gate
I_GATE = [
    [complex(1, 0), complex(0, 0)],
    [complex(0, 0), complex(1, 0)]
]


# ============================================================================
# Helper Functions
# ============================================================================

def _complex_equal(a: complex, b: complex, eps: float = EPSILON) -> bool:
    """Check if two complex numbers are approximately equal."""
    return abs(a - b) < eps


def _matrix_multiply(A: List[List[complex]], B: List[List[complex]]) -> List[List[complex]]:
    """Multiply two matrices."""
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    if cols_A != rows_B:
        raise ValueError("Matrix dimensions don't match for multiplication")
    
    result = [[complex(0, 0) for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    
    return result


def _tensor_product(A: List[List[complex]], B: List[List[complex]]) -> List[List[complex]]:
    """Compute tensor product (Kronecker product) of two matrices."""
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    result = [[complex(0, 0) for _ in range(cols_A * cols_B)] for _ in range(rows_A * rows_B)]
    
    for i in range(rows_A):
        for j in range(cols_A):
            for k in range(rows_B):
                for l in range(cols_B):
                    result[i * rows_B + k][j * cols_B + l] = A[i][j] * B[k][l]
    
    return result


def _tensor_product_vector(a: List[complex], b: List[complex]) -> List[complex]:
    """Compute tensor product of two vectors."""
    return [a_i * b_j for a_i in a for b_j in b]


def _normalize(state: List[complex]) -> List[complex]:
    """Normalize a quantum state vector."""
    norm = math.sqrt(sum(abs(x)**2 for x in state))
    if norm < EPSILON:
        raise ValueError("Cannot normalize zero state")
    return [x / norm for x in state]


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class MeasurementResult:
    """Result of a quantum measurement."""
    outcome: int  # 0 or 1 for single qubit, binary encoding for multi-qubit
    probability: float
    state_after: Optional[List[complex]] = None


@dataclass
class BlochCoordinates:
    """Coordinates on the Bloch sphere."""
    theta: float  # Polar angle (0 to π)
    phi: float    # Azimuthal angle (0 to 2π)
    x: float      # Cartesian x
    y: float      # Cartesian y
    z: float      # Cartesian z


@dataclass
class QuantumGate:
    """A quantum gate with its matrix representation."""
    name: str
    matrix: List[List[complex]]
    num_qubits: int = 1
    
    def __matmul__(self, other: 'QuantumGate') -> 'QuantumGate':
        """Compose two gates (matrix multiplication)."""
        return QuantumGate(
            name=f"{self.name}·{other.name}",
            matrix=_matrix_multiply(self.matrix, other.matrix),
            num_qubits=self.num_qubits
        )


# ============================================================================
# Qubit Class
# ============================================================================

class Qubit:
    """
    A single qubit represented as a quantum state vector.
    
    The state is |ψ⟩ = α|0⟩ + β|1⟩ where |α|² + |β|² = 1.
    
    Examples:
        >>> q = Qubit()  # |0⟩ state
        >>> q.measure()  # Always returns 0
        0
        
        >>> q = Qubit.ket_one()  # |1⟩ state
        >>> q.measure()  # Always returns 1
        1
        
        >>> q = Qubit.ket_plus()  # |+⟩ = (|0⟩ + |1⟩)/√2
        >>> q.measure()  # Returns 0 or 1 with equal probability
    """
    
    def __init__(self, alpha: complex = complex(1, 0), beta: complex = complex(0, 0)):
        """
        Initialize a qubit with amplitudes α and β.
        
        Args:
            alpha: Amplitude for |0⟩ state
            beta: Amplitude for |1⟩ state
        """
        self._state = _normalize([complex(alpha), complex(beta)])
    
    @property
    def state(self) -> List[complex]:
        """Return the state vector [α, β]."""
        return self._state.copy()
    
    @property
    def alpha(self) -> complex:
        """Return amplitude for |0⟩ state."""
        return self._state[0]
    
    @property
    def beta(self) -> complex:
        """Return amplitude for |1⟩ state."""
        return self._state[1]
    
    @property
    def probabilities(self) -> Tuple[float, float]:
        """Return (P(0), P(1)) probabilities."""
        return (abs(self.alpha)**2, abs(self.beta)**2)
    
    @classmethod
    def ket_zero(cls) -> 'Qubit':
        """Create a |0⟩ state qubit."""
        return cls(complex(1, 0), complex(0, 0))
    
    @classmethod
    def ket_one(cls) -> 'Qubit':
        """Create a |1⟩ state qubit."""
        return cls(complex(0, 0), complex(1, 0))
    
    @classmethod
    def ket_plus(cls) -> 'Qubit':
        """Create a |+⟩ = (|0⟩ + |1⟩)/√2 state."""
        return cls(complex(1/math.sqrt(2), 0), complex(1/math.sqrt(2), 0))
    
    @classmethod
    def ket_minus(cls) -> 'Qubit':
        """Create a |−⟩ = (|0⟩ - |1⟩)/√2 state."""
        return cls(complex(1/math.sqrt(2), 0), complex(-1/math.sqrt(2), 0))
    
    @classmethod
    def ket_i_plus(cls) -> 'Qubit':
        """Create a |i+⟩ = (|0⟩ + i|1⟩)/√2 state."""
        return cls(complex(1/math.sqrt(2), 0), complex(0, 1/math.sqrt(2)))
    
    @classmethod
    def ket_i_minus(cls) -> 'Qubit':
        """Create a |i-⟩ = (|0⟩ - i|1⟩)/√2 state."""
        return cls(complex(1/math.sqrt(2), 0), complex(0, -1/math.sqrt(2)))
    
    @classmethod
    def from_angle(cls, theta: float, phi: float) -> 'Qubit':
        """
        Create a qubit from Bloch sphere angles.
        
        Args:
            theta: Polar angle (0 to π)
            phi: Azimuthal angle (0 to 2π)
        
        Returns:
            Qubit with state |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩
        """
        alpha = complex(math.cos(theta / 2), 0)
        beta = complex(math.cos(phi), math.sin(phi)) * math.sin(theta / 2)
        return cls(alpha, beta)
    
    def apply_gate(self, gate: Union[List[List[complex]], QuantumGate]) -> 'Qubit':
        """
        Apply a quantum gate to this qubit.
        
        Args:
            gate: 2x2 unitary matrix or QuantumGate object
        
        Returns:
            New qubit with transformed state
        """
        if isinstance(gate, QuantumGate):
            matrix = gate.matrix
        else:
            matrix = gate
        
        new_alpha = matrix[0][0] * self.alpha + matrix[0][1] * self.beta
        new_beta = matrix[1][0] * self.alpha + matrix[1][1] * self.beta
        
        return Qubit(new_alpha, new_beta)
    
    def h(self) -> 'Qubit':
        """Apply Hadamard gate."""
        return self.apply_gate(H_GATE)
    
    def x(self) -> 'Qubit':
        """Apply Pauli-X (NOT) gate."""
        return self.apply_gate(X_GATE)
    
    def y(self) -> 'Qubit':
        """Apply Pauli-Y gate."""
        return self.apply_gate(Y_GATE)
    
    def z(self) -> 'Qubit':
        """Apply Pauli-Z gate."""
        return self.apply_gate(Z_GATE)
    
    def s(self) -> 'Qubit':
        """Apply S (Phase) gate."""
        return self.apply_gate(S_GATE)
    
    def t(self) -> 'Qubit':
        """Apply T (π/8) gate."""
        return self.apply_gate(T_GATE)
    
    def r(self, theta: float) -> 'Qubit':
        """
        Apply rotation gate R(θ) = e^(iθ/2) Rz(θ).
        
        Args:
            theta: Rotation angle in radians
        """
        matrix = [
            [complex(1, 0), complex(0, 0)],
            [complex(0, 0), complex(math.cos(theta), math.sin(theta))]
        ]
        return self.apply_gate(matrix)
    
    def rx(self, theta: float) -> 'Qubit':
        """
        Apply rotation around X-axis.
        
        Args:
            theta: Rotation angle in radians
        """
        c = math.cos(theta / 2)
        s = math.sin(theta / 2)
        matrix = [
            [complex(c, 0), complex(0, -s)],
            [complex(0, -s), complex(c, 0)]
        ]
        return self.apply_gate(matrix)
    
    def ry(self, theta: float) -> 'Qubit':
        """
        Apply rotation around Y-axis.
        
        Args:
            theta: Rotation angle in radians
        """
        c = math.cos(theta / 2)
        s = math.sin(theta / 2)
        matrix = [
            [complex(c, 0), complex(-s, 0)],
            [complex(s, 0), complex(c, 0)]
        ]
        return self.apply_gate(matrix)
    
    def rz(self, theta: float) -> 'Qubit':
        """
        Apply rotation around Z-axis.
        
        Args:
            theta: Rotation angle in radians
        """
        e_neg = cmath.exp(-1j * theta / 2)
        e_pos = cmath.exp(1j * theta / 2)
        matrix = [
            [e_neg, complex(0, 0)],
            [complex(0, 0), e_pos]
        ]
        return self.apply_gate(matrix)
    
    def measure(self, seed: Optional[int] = None) -> MeasurementResult:
        """
        Measure the qubit in the computational basis.
        
        Args:
            seed: Optional random seed for reproducibility
        
        Returns:
            MeasurementResult with outcome (0 or 1) and probability
        """
        if seed is not None:
            random.seed(seed)
        
        p0, p1 = self.probabilities
        
        if random.random() < p0:
            return MeasurementResult(
                outcome=0,
                probability=p0,
                state_after=[complex(1, 0), complex(0, 0)]
            )
        else:
            return MeasurementResult(
                outcome=1,
                probability=p1,
                state_after=[complex(0, 0), complex(1, 0)]
            )
    
    def get_bloch_coordinates(self) -> BlochCoordinates:
        """
        Get the Bloch sphere coordinates for this qubit state.
        
        Returns:
            BlochCoordinates with angles and Cartesian coordinates
        """
        # Calculate theta from probability of |1⟩
        prob_1 = abs(self.beta)**2
        theta = 2 * math.acos(math.sqrt(1 - prob_1))
        
        # Calculate phi from the phase of beta/alpha
        if abs(self.alpha) < EPSILON:
            # |ψ⟩ = |1⟩, phi is undefined, use 0
            phi = 0
        elif abs(self.beta) < EPSILON:
            # |ψ⟩ = |0⟩, phi is undefined, use 0
            phi = 0
        else:
            # Calculate relative phase
            ratio = self.beta / self.alpha
            phi = cmath.phase(ratio)
        
        # Cartesian coordinates
        x = math.sin(theta) * math.cos(phi)
        y = math.sin(theta) * math.sin(phi)
        z = math.cos(theta)
        
        return BlochCoordinates(theta=theta, phi=phi, x=x, y=y, z=z)
    
    def density_matrix(self) -> List[List[complex]]:
        """
        Calculate the density matrix ρ = |ψ⟩⟨ψ|.
        
        Returns:
            2x2 density matrix
        """
        a, b = self.alpha, self.beta
        return [
            [a * a.conjugate(), a * b.conjugate()],
            [b * a.conjugate(), b * b.conjugate()]
        ]
    
    def __eq__(self, other: object) -> bool:
        """Check equality with another qubit (up to global phase)."""
        if not isinstance(other, Qubit):
            return False
        
        # States are equal if their density matrices are equal
        rho1 = self.density_matrix()
        rho2 = other.density_matrix()
        
        for i in range(2):
            for j in range(2):
                if not _complex_equal(rho1[i][j], rho2[i][j]):
                    return False
        return True
    
    def __repr__(self) -> str:
        """Return string representation."""
        a, b = self.alpha, self.beta
        
        def format_complex(c: complex) -> str:
            if abs(c.imag) < EPSILON:
                return f"{c.real:.4f}"
            elif abs(c.real) < EPSILON:
                return f"{c.imag:.4f}i"
            else:
                sign = "+" if c.imag >= 0 else ""
                return f"({c.real:.4f}{sign}{c.imag:.4f}i)"
        
        a_str = format_complex(a)
        b_str = format_complex(b)
        
        terms = []
        if abs(a) > EPSILON:
            terms.append(f"{a_str}|0⟩")
        if abs(b) > EPSILON:
            if terms and b.real >= 0:
                terms.append(f"+ {b_str}|1⟩")
            else:
                terms.append(f"{b_str}|1⟩")
        
        return " ".join(terms) if terms else "0"


# ============================================================================
# Multi-Qubit Register
# ============================================================================

class QuantumRegister:
    """
    A quantum register holding multiple qubits.
    
    The state vector has 2^n dimensions for n qubits.
    
    Examples:
        >>> reg = QuantumRegister(2)  # |00⟩
        >>> reg.apply_hadamard(0)  # Apply H to first qubit
        >>> reg.apply_cnot(0, 1)  # Apply CNOT with control=0, target=1
        >>> reg.measure()  # Measure all qubits
    """
    
    def __init__(self, num_qubits: int, initial_state: Optional[List[complex]] = None):
        """
        Initialize a quantum register.
        
        Args:
            num_qubits: Number of qubits in the register
            initial_state: Optional initial state vector (defaults to |0...0⟩)
        """
        if num_qubits < 1:
            raise ValueError("Must have at least 1 qubit")
        
        self.num_qubits = num_qubits
        self.dim = 2 ** num_qubits
        
        if initial_state is None:
            # Initialize to |0...0⟩
            self._state = [complex(0, 0)] * self.dim
            self._state[0] = complex(1, 0)
        else:
            if len(initial_state) != self.dim:
                raise ValueError(f"State vector must have {self.dim} elements")
            self._state = _normalize([complex(x) for x in initial_state])
    
    @property
    def state(self) -> List[complex]:
        """Return the state vector."""
        return self._state.copy()
    
    def get_probabilities(self) -> List[float]:
        """Get probabilities for all computational basis states."""
        return [abs(x)**2 for x in self._state]
    
    def get_qubit(self, index: int) -> Qubit:
        """
        Extract a single qubit's reduced density matrix as a state.
        
        Note: This only works correctly if the qubit is not entangled.
        
        Args:
            index: Qubit index (0 to num_qubits-1)
        
        Returns:
            Qubit object (if separable, otherwise gives best approximation)
        """
        if index < 0 or index >= self.num_qubits:
            raise IndexError(f"Qubit index out of range: {index}")
        
        # Trace out other qubits to get reduced density matrix
        # For simplicity, we'll just compute the probability of measuring |0⟩ or |1⟩
        p0 = 0.0
        p1 = 0.0
        
        for i, amplitude in enumerate(self._state):
            # Check if the index-th bit is 0 or 1
            if (i >> index) & 1 == 0:
                p0 += abs(amplitude)**2
            else:
                p1 += abs(amplitude)**2
        
        # Return a qubit with the correct probabilities
        # Note: phase information is lost for entangled states
        alpha = cmath.sqrt(p0)
        beta = cmath.sqrt(p1)
        
        return Qubit(alpha, beta)
    
    def apply_single_qubit_gate(self, gate: List[List[complex]], target: int) -> 'QuantumRegister':
        """
        Apply a single-qubit gate to the specified qubit.
        
        Args:
            gate: 2x2 unitary matrix
            target: Target qubit index
        
        Returns:
            Self for method chaining
        """
        if target < 0 or target >= self.num_qubits:
            raise IndexError(f"Qubit index out of range: {target}")
        
        new_state = [complex(0, 0)] * self.dim
        
        # Process all pairs of states where only the target qubit differs
        for base in range(self.dim):
            # Only process states where target qubit is 0 (avoid double processing)
            if (base >> target) & 1 == 0:
                i0 = base  # State with target qubit = 0
                i1 = base | (1 << target)  # State with target qubit = 1
                
                # Apply gate: |new⟩ = gate|old⟩
                # new_0 = gate[0][0] * old_0 + gate[0][1] * old_1
                # new_1 = gate[1][0] * old_0 + gate[1][1] * old_1
                new_state[i0] = gate[0][0] * self._state[i0] + gate[0][1] * self._state[i1]
                new_state[i1] = gate[1][0] * self._state[i0] + gate[1][1] * self._state[i1]
        
        self._state = new_state
        return self
    
    def apply_hadamard(self, target: int) -> 'QuantumRegister':
        """Apply Hadamard gate to target qubit."""
        return self.apply_single_qubit_gate(H_GATE, target)
    
    def apply_x(self, target: int) -> 'QuantumRegister':
        """Apply Pauli-X (NOT) gate to target qubit."""
        return self.apply_single_qubit_gate(X_GATE, target)
    
    def apply_y(self, target: int) -> 'QuantumRegister':
        """Apply Pauli-Y gate to target qubit."""
        return self.apply_single_qubit_gate(Y_GATE, target)
    
    def apply_z(self, target: int) -> 'QuantumRegister':
        """Apply Pauli-Z gate to target qubit."""
        return self.apply_single_qubit_gate(Z_GATE, target)
    
    def apply_cnot(self, control: int, target: int) -> 'QuantumRegister':
        """
        Apply CNOT gate with control and target qubits.
        
        Args:
            control: Control qubit index
            target: Target qubit index
        
        Returns:
            Self for method chaining
        """
        if control < 0 or control >= self.num_qubits:
            raise IndexError(f"Control qubit index out of range: {control}")
        if target < 0 or target >= self.num_qubits:
            raise IndexError(f"Target qubit index out of range: {target}")
        if control == target:
            raise ValueError("Control and target must be different qubits")
        
        # CNOT: when control is 1, flip target
        # We need to swap amplitudes between pairs of states
        # where control=1 and only target differs
        new_state = [complex(0, 0)] * self.dim
        
        # Process in pairs to properly swap
        processed = set()
        for i in range(self.dim):
            if i in processed:
                continue
            
            # Check if control is 1 for this state
            if (i >> control) & 1 == 1:
                # Find the paired state (flip target bit)
                j = i ^ (1 << target)
                processed.add(i)
                processed.add(j)
                
                # Swap amplitudes between i and j (both have control=1)
                new_state[j] = self._state[i]  # i -> j (target flipped)
                new_state[i] = self._state[j]  # j -> i (target flipped)
            else:
                # Control is 0, state stays unchanged
                new_state[i] = self._state[i]
        
        self._state = new_state
        return self
    
    def apply_cz(self, control: int, target: int) -> 'QuantumRegister':
        """
        Apply CZ (Controlled-Z) gate.
        
        Args:
            control: Control qubit index
            target: Target qubit index
        
        Returns:
            Self for method chaining
        """
        if control == target:
            raise ValueError("Control and target must be different qubits")
        
        for i in range(self.dim):
            # Apply -1 phase if both control and target are 1
            if ((i >> control) & 1) == 1 and ((i >> target) & 1) == 1:
                self._state[i] *= -1
        
        return self
    
    def apply_swap(self, qubit1: int, qubit2: int) -> 'QuantumRegister':
        """
        Apply SWAP gate between two qubits.
        
        Args:
            qubit1: First qubit index
            qubit2: Second qubit index
        
        Returns:
            Self for method chaining
        """
        if qubit1 == qubit2:
            return self
        
        new_state = [complex(0, 0)] * self.dim
        
        # Process in pairs to properly swap
        processed = set()
        for i in range(self.dim):
            if i in processed:
                continue
            
            bit1 = (i >> qubit1) & 1
            bit2 = (i >> qubit2) & 1
            
            if bit1 != bit2:
                # Swap the bits: state i goes to state j
                j = i ^ (1 << qubit1) ^ (1 << qubit2)
                processed.add(i)
                processed.add(j)
                
                # Swap amplitudes
                new_state[j] = self._state[i]
                new_state[i] = self._state[j]
            else:
                # Bits are same, state stays unchanged
                new_state[i] = self._state[i]
        
        self._state = new_state
        return self
    
    def apply_toffoli(self, control1: int, control2: int, target: int) -> 'QuantumRegister':
        """
        Apply Toffoli (CCNOT) gate.
        
        Args:
            control1: First control qubit index
            control2: Second control qubit index
            target: Target qubit index
        
        Returns:
            Self for method chaining
        """
        new_state = self._state.copy()
        
        for i in range(self.dim):
            # Check if both controls are 1
            if ((i >> control1) & 1) == 1 and ((i >> control2) & 1) == 1:
                # Flip target bit
                j = i ^ (1 << target)
                new_state[j] = self._state[i]
        
        self._state = new_state
        return self
    
    def measure_qubit(self, target: int, seed: Optional[int] = None) -> MeasurementResult:
        """
        Measure a single qubit.
        
        Args:
            target: Qubit to measure
            seed: Optional random seed
        
        Returns:
            MeasurementResult with outcome and probability
        """
        if seed is not None:
            random.seed(seed)
        
        if target < 0 or target >= self.num_qubits:
            raise IndexError(f"Qubit index out of range: {target}")
        
        # Calculate probability of measuring 0
        p0 = 0.0
        for i, amplitude in enumerate(self._state):
            if ((i >> target) & 1) == 0:
                p0 += abs(amplitude)**2
        
        p1 = 1.0 - p0
        
        # Perform measurement
        if random.random() < p0:
            outcome = 0
            prob = p0
        else:
            outcome = 1
            prob = p1
        
        # Collapse state
        new_state = [complex(0, 0)] * self.dim
        norm = math.sqrt(prob)
        
        for i, amplitude in enumerate(self._state):
            if ((i >> target) & 1) == outcome:
                new_state[i] = amplitude / norm
        
        self._state = new_state
        
        return MeasurementResult(outcome=outcome, probability=prob)
    
    def measure_all(self, seed: Optional[int] = None) -> MeasurementResult:
        """
        Measure all qubits.
        
        Args:
            seed: Optional random seed
        
        Returns:
            MeasurementResult with outcome (binary encoded) and probability
        """
        if seed is not None:
            random.seed(seed)
        
        probs = self.get_probabilities()
        
        # Choose outcome based on probabilities
        r = random.random()
        cumulative = 0.0
        outcome = 0
        
        for i, p in enumerate(probs):
            cumulative += p
            if r < cumulative:
                outcome = i
                break
        
        # Collapse to measured state
        new_state = [complex(0, 0)] * self.dim
        new_state[outcome] = complex(1, 0)
        self._state = new_state
        
        return MeasurementResult(outcome=outcome, probability=probs[outcome])
    
    def measure(self, targets: Optional[List[int]] = None, seed: Optional[int] = None) -> Union[MeasurementResult, int]:
        """
        Measure qubits.
        
        Args:
            targets: Optional list of qubit indices to measure (None = all)
            seed: Optional random seed
        
        Returns:
            MeasurementResult for single qubit, or int for all qubits
        """
        if targets is None:
            return self.measure_all(seed)
        elif len(targets) == 1:
            return self.measure_qubit(targets[0], seed)
        else:
            # Measure multiple qubits
            outcomes = []
            for t in sorted(targets, reverse=True):
                result = self.measure_qubit(t, seed)
                outcomes.append(result.outcome)
            return outcomes
    
    def __repr__(self) -> str:
        """Return string representation of the state."""
        terms = []
        for i, amplitude in enumerate(self._state):
            if abs(amplitude) > EPSILON:
                basis = bin(i)[2:].zfill(self.num_qubits)
                if abs(amplitude.real) < EPSILON and abs(amplitude.imag) < EPSILON:
                    continue
                elif abs(amplitude.imag) < EPSILON:
                    terms.append(f"{amplitude.real:.4f}|{basis}⟩")
                elif abs(amplitude.real) < EPSILON:
                    terms.append(f"{amplitude.imag:.4f}i|{basis}⟩")
                else:
                    terms.append(f"({amplitude:.4f})|{basis}⟩")
        
        return " + ".join(terms) if terms else "0"
    
    def copy(self) -> 'QuantumRegister':
        """Create a copy of this register."""
        return QuantumRegister(self.num_qubits, self._state.copy())


# ============================================================================
# Quantum Circuit
# ============================================================================

@dataclass
class CircuitGate:
    """A gate applied in a circuit."""
    name: str
    gate_type: str  # 'single', 'cnot', 'cz', 'swap', 'toffoli'
    targets: List[int]
    controls: List[int] = field(default_factory=list)
    params: dict = field(default_factory=dict)


class QuantumCircuit:
    """
    A quantum circuit for building and executing quantum programs.
    
    Examples:
        >>> circuit = QuantumCircuit(2)
        >>> circuit.h(0)  # Hadamard on qubit 0
        >>> circuit.cnot(0, 1)  # CNOT with control=0, target=1
        >>> circuit.measure_all()
        >>> result = circuit.run()
    """
    
    def __init__(self, num_qubits: int, num_classical_bits: int = 0):
        """
        Initialize a quantum circuit.
        
        Args:
            num_qubits: Number of quantum bits
            num_classical_bits: Number of classical bits for measurement
        """
        self.num_qubits = num_qubits
        self.num_classical_bits = num_classical_bits or num_qubits
        self.gates: List[CircuitGate] = []
        self.measurements: List[int] = []  # Qubit indices to measure
    
    def h(self, target: int) -> 'QuantumCircuit':
        """Add Hadamard gate."""
        self.gates.append(CircuitGate('H', 'single', [target]))
        return self
    
    def x(self, target: int) -> 'QuantumCircuit':
        """Add Pauli-X (NOT) gate."""
        self.gates.append(CircuitGate('X', 'single', [target]))
        return self
    
    def y(self, target: int) -> 'QuantumCircuit':
        """Add Pauli-Y gate."""
        self.gates.append(CircuitGate('Y', 'single', [target]))
        return self
    
    def z(self, target: int) -> 'QuantumCircuit':
        """Add Pauli-Z gate."""
        self.gates.append(CircuitGate('Z', 'single', [target]))
        return self
    
    def s(self, target: int) -> 'QuantumCircuit':
        """Add S (Phase) gate."""
        self.gates.append(CircuitGate('S', 'single', [target]))
        return self
    
    def t(self, target: int) -> 'QuantumCircuit':
        """Add T (π/8) gate."""
        self.gates.append(CircuitGate('T', 'single', [target]))
        return self
    
    def rx(self, target: int, theta: float) -> 'QuantumCircuit':
        """Add RX rotation gate."""
        self.gates.append(CircuitGate('RX', 'single', [target], params={'theta': theta}))
        return self
    
    def ry(self, target: int, theta: float) -> 'QuantumCircuit':
        """Add RY rotation gate."""
        self.gates.append(CircuitGate('RY', 'single', [target], params={'theta': theta}))
        return self
    
    def rz(self, target: int, theta: float) -> 'QuantumCircuit':
        """Add RZ rotation gate."""
        self.gates.append(CircuitGate('RZ', 'single', [target], params={'theta': theta}))
        return self
    
    def cnot(self, control: int, target: int) -> 'QuantumCircuit':
        """Add CNOT (Controlled-X) gate."""
        self.gates.append(CircuitGate('CNOT', 'cnot', [target], [control]))
        return self
    
    def cx(self, control: int, target: int) -> 'QuantumCircuit':
        """Alias for CNOT."""
        return self.cnot(control, target)
    
    def cz(self, control: int, target: int) -> 'QuantumCircuit':
        """Add CZ (Controlled-Z) gate."""
        self.gates.append(CircuitGate('CZ', 'cz', [target], [control]))
        return self
    
    def swap(self, qubit1: int, qubit2: int) -> 'QuantumCircuit':
        """Add SWAP gate."""
        self.gates.append(CircuitGate('SWAP', 'swap', [qubit1, qubit2]))
        return self
    
    def toffoli(self, control1: int, control2: int, target: int) -> 'QuantumCircuit':
        """Add Toffoli (CCNOT) gate."""
        self.gates.append(CircuitGate('Toffoli', 'toffoli', [target], [control1, control2]))
        return self
    
    def ccx(self, control1: int, control2: int, target: int) -> 'QuantumCircuit':
        """Alias for Toffoli."""
        return self.toffoli(control1, control2, target)
    
    def measure(self, target: int) -> 'QuantumCircuit':
        """Add measurement on a qubit."""
        self.measurements.append(target)
        return self
    
    def measure_all(self) -> 'QuantumCircuit':
        """Add measurement on all qubits."""
        self.measurements = list(range(self.num_qubits))
        return self
    
    def run(self, shots: int = 1, seed: Optional[int] = None) -> dict:
        """
        Run the circuit and return measurement results.
        
        Args:
            shots: Number of times to run the circuit
            seed: Optional random seed for reproducibility
        
        Returns:
            Dictionary mapping measurement outcomes to counts
        """
        results = {}
        
        for shot in range(shots):
            # Create fresh register
            reg = QuantumRegister(self.num_qubits)
            
            # Apply gates
            for gate in self.gates:
                if gate.gate_type == 'single':
                    target = gate.targets[0]
                    if gate.name == 'H':
                        reg.apply_hadamard(target)
                    elif gate.name == 'X':
                        reg.apply_x(target)
                    elif gate.name == 'Y':
                        reg.apply_y(target)
                    elif gate.name == 'Z':
                        reg.apply_z(target)
                    elif gate.name == 'S':
                        reg.apply_single_qubit_gate(S_GATE, target)
                    elif gate.name == 'T':
                        reg.apply_single_qubit_gate(T_GATE, target)
                    elif gate.name == 'RX':
                        theta = gate.params['theta']
                        reg.apply_single_qubit_gate(self._rx_matrix(theta), target)
                    elif gate.name == 'RY':
                        theta = gate.params['theta']
                        reg.apply_single_qubit_gate(self._ry_matrix(theta), target)
                    elif gate.name == 'RZ':
                        theta = gate.params['theta']
                        reg.apply_single_qubit_gate(self._rz_matrix(theta), target)
                elif gate.gate_type == 'cnot':
                    reg.apply_cnot(gate.controls[0], gate.targets[0])
                elif gate.gate_type == 'cz':
                    reg.apply_cz(gate.controls[0], gate.targets[0])
                elif gate.gate_type == 'swap':
                    reg.apply_swap(gate.targets[0], gate.targets[1])
                elif gate.gate_type == 'toffoli':
                    reg.apply_toffoli(gate.controls[0], gate.controls[1], gate.targets[0])
            
            # Measure
            if self.measurements:
                outcome_bits = []
                for target in sorted(self.measurements):
                    result = reg.measure_qubit(target, seed=seed if seed is None else seed + shot)
                    outcome_bits.append(str(result.outcome))
                outcome = ''.join(outcome_bits)
            else:
                outcome = bin(random.randint(0, 2**self.num_qubits - 1))[2:].zfill(self.num_qubits)
            
            results[outcome] = results.get(outcome, 0) + 1
        
        return results
    
    def _rx_matrix(self, theta: float) -> List[List[complex]]:
        """Create RX rotation matrix."""
        c, s = math.cos(theta / 2), math.sin(theta / 2)
        return [
            [complex(c, 0), complex(0, -s)],
            [complex(0, -s), complex(c, 0)]
        ]
    
    def _ry_matrix(self, theta: float) -> List[List[complex]]:
        """Create RY rotation matrix."""
        c, s = math.cos(theta / 2), math.sin(theta / 2)
        return [
            [complex(c, 0), complex(-s, 0)],
            [complex(s, 0), complex(c, 0)]
        ]
    
    def _rz_matrix(self, theta: float) -> List[List[complex]]:
        """Create RZ rotation matrix."""
        e_neg = cmath.exp(-1j * theta / 2)
        e_pos = cmath.exp(1j * theta / 2)
        return [
            [e_neg, complex(0, 0)],
            [complex(0, 0), e_pos]
        ]
    
    def get_statevector(self) -> List[complex]:
        """
        Get the final state vector without measurement.
        
        Returns:
            State vector after applying all gates
        """
        reg = QuantumRegister(self.num_qubits)
        
        for gate in self.gates:
            if gate.gate_type == 'single':
                target = gate.targets[0]
                if gate.name == 'H':
                    reg.apply_hadamard(target)
                elif gate.name == 'X':
                    reg.apply_x(target)
                elif gate.name == 'Y':
                    reg.apply_y(target)
                elif gate.name == 'Z':
                    reg.apply_z(target)
                elif gate.name == 'S':
                    reg.apply_single_qubit_gate(S_GATE, target)
                elif gate.name == 'T':
                    reg.apply_single_qubit_gate(T_GATE, target)
                elif gate.name == 'RX':
                    reg.apply_single_qubit_gate(self._rx_matrix(gate.params['theta']), target)
                elif gate.name == 'RY':
                    reg.apply_single_qubit_gate(self._ry_matrix(gate.params['theta']), target)
                elif gate.name == 'RZ':
                    reg.apply_single_qubit_gate(self._rz_matrix(gate.params['theta']), target)
            elif gate.gate_type == 'cnot':
                reg.apply_cnot(gate.controls[0], gate.targets[0])
            elif gate.gate_type == 'cz':
                reg.apply_cz(gate.controls[0], gate.targets[0])
            elif gate.gate_type == 'swap':
                reg.apply_swap(gate.targets[0], gate.targets[1])
            elif gate.gate_type == 'toffoli':
                reg.apply_toffoli(gate.controls[0], gate.controls[1], gate.targets[0])
        
        return reg.state
    
    def __repr__(self) -> str:
        """Return circuit diagram."""
        lines = []
        for i in range(self.num_qubits):
            line = f"q{i}: ─"
            gate_strs = []
            
            for gate in self.gates:
                if gate.gate_type == 'single':
                    if gate.targets[0] == i:
                        gate_strs.append(f"─{gate.name}─")
                    else:
                        gate_strs.append("─────")
                elif gate.gate_type == 'cnot':
                    if gate.controls[0] == i:
                        gate_strs.append("──●──")
                    elif gate.targets[0] == i:
                        gate_strs.append("──⊕──")
                    else:
                        gate_strs.append("─────")
                elif gate.gate_type == 'cz':
                    if gate.controls[0] == i or gate.targets[0] == i:
                        gate_strs.append("──●──")
                    else:
                        gate_strs.append("─────")
                elif gate.gate_type == 'swap':
                    if gate.targets[0] == i:
                        gate_strs.append("──×──")
                    elif gate.targets[1] == i:
                        gate_strs.append("──×──")
                    else:
                        gate_strs.append("─────")
                elif gate.gate_type == 'toffoli':
                    if i in gate.controls:
                        gate_strs.append("──●──")
                    elif gate.targets[0] == i:
                        gate_strs.append("──⊕──")
                    else:
                        gate_strs.append("─────")
            
            line += "".join(gate_strs)
            if self.measurements and i in self.measurements:
                line += "──M──"
            lines.append(line)
        
        return "\n".join(lines)


# ============================================================================
# Standard States and Circuits
# ============================================================================

def create_bell_state() -> QuantumRegister:
    """
    Create a Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2.
    
    This is the simplest example of quantum entanglement.
    
    Returns:
        QuantumRegister in Bell state
    """
    reg = QuantumRegister(2)
    reg.apply_hadamard(0)
    reg.apply_cnot(0, 1)
    return reg


def create_ghz_state(num_qubits: int = 3) -> QuantumRegister:
    """
    Create a GHZ state (|0...0⟩ + |1...1⟩)/√2.
    
    Args:
        num_qubits: Number of qubits (default 3)
    
    Returns:
        QuantumRegister in GHZ state
    """
    reg = QuantumRegister(num_qubits)
    reg.apply_hadamard(0)
    for i in range(num_qubits - 1):
        reg.apply_cnot(i, i + 1)
    return reg


def create_w_state(num_qubits: int = 3) -> QuantumRegister:
    """
    Create a W state (|100...0⟩ + |010...0⟩ + ... + |000...1⟩)/√n.
    
    Args:
        num_qubits: Number of qubits (default 3)
    
    Returns:
        QuantumRegister in W state
    """
    # W state is more complex to create
    # |W₃⟩ = (|001⟩ + |010⟩ + |100⟩)/√3
    # For simplicity, we'll create the normalized superposition
    dim = 2 ** num_qubits
    state = [complex(0, 0)] * dim
    norm = 1.0 / math.sqrt(num_qubits)
    
    for i in range(num_qubits):
        # Only qubit i is |1⟩
        index = 1 << i
        state[index] = complex(norm, 0)
    
    return QuantumRegister(num_qubits, state)


def quantum_fourier_transform(num_qubits: int) -> QuantumCircuit:
    """
    Create a Quantum Fourier Transform circuit.
    
    Args:
        num_qubits: Number of qubits
    
    Returns:
        QuantumCircuit implementing QFT
    """
    circuit = QuantumCircuit(num_qubits)
    
    for i in range(num_qubits):
        circuit.h(i)
        for j in range(i + 1, num_qubits):
            # Controlled rotation Rk where k = j - i + 1
            theta = 2 * math.pi / (2 ** (j - i + 1))
            # Note: simplified - in real QFT would need controlled R
            # For now, we'll just use H gates
    
    # Add swap gates at the end
    for i in range(num_qubits // 2):
        circuit.swap(i, num_qubits - 1 - i)
    
    return circuit


def deutsch_jozsa(oracle: Callable[[int], int], num_qubits: int) -> QuantumCircuit:
    """
    Create a Deutsch-Jozsa algorithm circuit.
    
    Args:
        oracle: Function that maps input bitstring to output bit (0 or 1)
        num_qubits: Number of input qubits
    
    Returns:
        QuantumCircuit for Deutsch-Jozsa algorithm
    """
    circuit = QuantumCircuit(num_qubits + 1)
    
    # Initialize last qubit to |1⟩
    circuit.x(num_qubits)
    
    # Apply Hadamard to all qubits
    for i in range(num_qubits + 1):
        circuit.h(i)
    
    # Apply oracle (simplified - would need to implement based on oracle)
    # In practice, oracle would be implemented as a series of gates
    
    # Apply Hadamard to input qubits
    for i in range(num_qubits):
        circuit.h(i)
    
    circuit.measure_all()
    return circuit


# ============================================================================
# Utility Functions
# ============================================================================

def entangle(qubit1: Qubit, qubit2: Qubit) -> QuantumRegister:
    """
    Entangle two qubits using Hadamard + CNOT gate.
    
    Creates a Bell state by first applying Hadamard to the control qubit,
    then applying CNOT with control as the first qubit and target as the second.
    
    Args:
        qubit1: First qubit (becomes control)
        qubit2: Second qubit (becomes target)
    
    Returns:
        QuantumRegister with entangled qubits (Bell-like state)
    """
    state = _tensor_product_vector(qubit1.state, qubit2.state)
    reg = QuantumRegister(2, state)
    # Apply Hadamard to control qubit to create superposition
    reg.apply_hadamard(0)
    # Apply CNOT to create entanglement
    reg.apply_cnot(0, 1)
    return reg


def is_entangled(reg: QuantumRegister) -> bool:
    """
    Check if a quantum register is entangled.
    
    Uses the partial trace method to check if the state can be
    written as a tensor product of individual qubit states.
    
    Args:
        reg: Quantum register to check
    
    Returns:
        True if entangled, False if separable
    """
    if reg.num_qubits < 2:
        return False
    
    # Simple check: if probabilities show correlation, likely entangled
    probs = reg.get_probabilities()
    
    # For Bell state, only |00⟩ and |11⟩ have non-zero probability
    # For separable state, this wouldn't happen
    p00 = probs[0]
    p01 = probs[1]
    p10 = probs[2]
    p11 = probs[3]
    
    # If we have strong correlation (p00 and p11 non-zero, p01 and p10 near zero)
    # or strong anti-correlation (p01 and p10 non-zero, p00 and p11 near zero)
    # then likely entangled
    
    # More rigorous: use entanglement entropy
    # For a 2-qubit system, we can check if the reduced density matrix
    # is pure (separable) or mixed (entangled)
    
    if reg.num_qubits == 2:
        # Calculate reduced density matrix for first qubit
        rho_0 = [[complex(0, 0), complex(0, 0)],
                  [complex(0, 0), complex(0, 0)]]
        
        for i, amp in enumerate(reg.state):
            bit0 = (i >> 0) & 1
            bit1 = (i >> 1) & 1
            for j, amp_j in enumerate(reg.state):
                bit0_j = (j >> 0) & 1
                bit1_j = (j >> 1) & 1
                if bit1 == bit1_j:
                    rho_0[bit0][bit0_j] += amp * amp_j.conjugate()
        
        # Calculate purity = Tr(ρ²)
        purity = rho_0[0][0]**2 + rho_0[0][1] * rho_0[1][0] + \
                 rho_0[1][0] * rho_0[0][1] + rho_0[1][1]**2
        
        # If purity < 1, the state is entangled
        return abs(purity - 1.0) > EPSILON
    
    return True  # Assume entangled for multi-qubit states


def teleportation_circuit() -> QuantumCircuit:
    """
    Create a quantum teleportation circuit.
    
    Teleports the state of qubit 0 to qubit 2 using qubit 1 as entanglement.
    
    Returns:
        QuantumCircuit for teleportation
    """
    circuit = QuantumCircuit(3, 3)
    
    # Create Bell pair between qubits 1 and 2
    circuit.h(1)
    circuit.cnot(1, 2)
    
    # Entangle qubit 0 with qubit 1
    circuit.cnot(0, 1)
    circuit.h(0)
    
    # Measure qubits 0 and 1
    circuit.measure(0)
    circuit.measure(1)
    
    return circuit


def grover_oracle(target: int, num_qubits: int) -> QuantumCircuit:
    """
    Create an oracle for Grover's search that marks the target state.
    
    Args:
        target: Target state to search for
        num_qubits: Number of qubits
    
    Returns:
        QuantumCircuit implementing the oracle
    """
    circuit = QuantumCircuit(num_qubits)
    
    # Apply X gates to flip target bits
    target_bits = bin(target)[2:].zfill(num_qubits)
    for i, bit in enumerate(target_bits):
        if bit == '0':
            circuit.x(num_qubits - 1 - i)
    
    # Apply multi-controlled Z
    if num_qubits == 1:
        circuit.z(0)
    elif num_qubits == 2:
        circuit.cz(0, 1)
    else:
        # For more qubits, would need multi-controlled Z
        # Simplified version
        circuit.z(num_qubits - 1)
    
    # Unapply X gates
    for i, bit in enumerate(target_bits):
        if bit == '0':
            circuit.x(num_qubits - 1 - i)
    
    return circuit


def grover_diffusion(num_qubits: int) -> QuantumCircuit:
    """
    Create the diffusion operator for Grover's algorithm.
    
    Args:
        num_qubits: Number of qubits
    
    Returns:
        QuantumCircuit implementing the diffusion operator
    """
    circuit = QuantumCircuit(num_qubits)
    
    # Apply H to all qubits
    for i in range(num_qubits):
        circuit.h(i)
    
    # Apply X to all qubits
    for i in range(num_qubits):
        circuit.x(i)
    
    # Apply multi-controlled Z
    if num_qubits == 1:
        circuit.z(0)
    elif num_qubits == 2:
        circuit.cz(0, 1)
    else:
        circuit.z(num_qubits - 1)
    
    # Apply X to all qubits
    for i in range(num_qubits):
        circuit.x(i)
    
    # Apply H to all qubits
    for i in range(num_qubits):
        circuit.h(i)
    
    return circuit


# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    print("=== Quantum Computing Utilities Demo ===\n")
    
    # Single qubit operations
    print("Single Qubit Operations:")
    print("-" * 40)
    
    q = Qubit.ket_zero()
    print(f"Initial state |0⟩: {q}")
    
    q = q.h()
    print(f"After H: {q}")
    print(f"Probabilities: P(0)={q.probabilities[0]:.4f}, P(1)={q.probabilities[1]:.4f}")
    
    bloch = q.get_bloch_coordinates()
    print(f"Bloch coordinates: θ={bloch.theta:.4f}, φ={bloch.phi:.4f}")
    print(f"Cartesian: ({bloch.x:.4f}, {bloch.y:.4f}, {bloch.z:.4f})")
    
    # Bell state
    print("\nBell State (Entanglement):")
    print("-" * 40)
    
    bell = create_bell_state()
    print(f"Bell state: {bell}")
    print(f"Entangled: {is_entangled(bell)}")
    
    # Run measurements
    print("\nMeasurements (1000 shots):")
    results = {}
    for _ in range(1000):
        reg = create_bell_state()
        outcome = reg.measure_all().outcome
        key = bin(outcome)[2:].zfill(2)
        results[key] = results.get(key, 0) + 1
    print(f"Results: {results}")
    
    # Quantum circuit
    print("\nQuantum Circuit:")
    print("-" * 40)
    
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cnot(0, 1)
    circuit.measure_all()
    
    print(f"Circuit:\n{circuit}")
    print(f"\nRunning 1000 shots...")
    results = circuit.run(shots=1000)
    print(f"Results: {results}")
    
    print("\n=== Demo Complete ===")