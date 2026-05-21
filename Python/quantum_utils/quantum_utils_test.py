#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Quantum Computing Utilities Test Suite
=====================================================
Comprehensive tests for quantum_utils module.

Tests cover:
    - Qubit state initialization and operations
    - Quantum gates (H, X, Y, Z, S, T, R, RX, RY, RZ)
    - Measurement and probability calculations
    - Bloch sphere coordinates
    - Quantum register operations
    - Multi-qubit gates (CNOT, CZ, SWAP, Toffoli)
    - Bell states and entanglement
    - Quantum circuit building and execution
    - QFT and Grover's algorithm basics

Author: AllToolkit Contributors
License: MIT
"""

import unittest
import math
import cmath
import random

from mod import (
    Qubit, QuantumRegister, QuantumCircuit,
    MeasurementResult, BlochCoordinates, QuantumGate,
    H_GATE, X_GATE, Y_GATE, Z_GATE, S_GATE, T_GATE, I_GATE,
    ZERO_STATE, ONE_STATE,
    create_bell_state, create_ghz_state, create_w_state,
    is_entangled, entangle,
    _complex_equal, _normalize, _tensor_product, _matrix_multiply, _tensor_product_vector
)


class TestHelperFunctions(unittest.TestCase):
    """Test helper functions."""
    
    def test_complex_equal(self):
        """Test complex number equality check."""
        self.assertTrue(_complex_equal(complex(1, 0), complex(1, 0)))
        self.assertTrue(_complex_equal(complex(1, 1e-11), complex(1, 0)))
        self.assertFalse(_complex_equal(complex(1, 0), complex(1.1, 0)))
    
    def test_normalize(self):
        """Test vector normalization."""
        state = [complex(2, 0), complex(0, 0)]
        normalized = _normalize(state)
        self.assertAlmostEqual(abs(normalized[0])**2 + abs(normalized[1])**2, 1.0)
        
        # Test zero state raises error
        with self.assertRaises(ValueError):
            _normalize([complex(0, 0), complex(0, 0)])
    
    def test_tensor_product(self):
        """Test tensor product of vectors."""
        a = [complex(1, 0), complex(0, 0)]  # |0⟩
        b = [complex(0, 0), complex(1, 0)]  # |1⟩
        result = _tensor_product_vector(a, b)
        expected = [complex(0, 0), complex(1, 0), complex(0, 0), complex(0, 0)]  # |01⟩
        self.assertEqual(len(result), 4)
        self.assertTrue(_complex_equal(result[1], complex(1, 0)))
    
    def test_matrix_multiply(self):
        """Test matrix multiplication."""
        # H * H = I
        result = _matrix_multiply(H_GATE, H_GATE)
        for i in range(2):
            for j in range(2):
                self.assertTrue(_complex_equal(result[i][j], I_GATE[i][j]))
        
        # X * X = I
        result = _matrix_multiply(X_GATE, X_GATE)
        for i in range(2):
            for j in range(2):
                self.assertTrue(_complex_equal(result[i][j], I_GATE[i][j]))


class TestQubit(unittest.TestCase):
    """Test single qubit operations."""
    
    def test_init(self):
        """Test qubit initialization."""
        q = Qubit()
        self.assertTrue(_complex_equal(q.alpha, complex(1, 0)))
        self.assertTrue(_complex_equal(q.beta, complex(0, 0)))
        
        q = Qubit(complex(0, 0), complex(1, 0))
        self.assertTrue(_complex_equal(q.alpha, complex(0, 0)))
        self.assertTrue(_complex_equal(q.beta, complex(1, 0)))
        
        # Test normalization
        q = Qubit(complex(2, 0), complex(2, 0))
        self.assertAlmostEqual(abs(q.alpha)**2 + abs(q.beta)**2, 1.0)
    
    def test_ket_states(self):
        """Test ket state creation."""
        q0 = Qubit.ket_zero()
        self.assertEqual(str(q0), "1.0000|0⟩")
        
        q1 = Qubit.ket_one()
        self.assertEqual(str(q1), "1.0000|1⟩")
        
        qp = Qubit.ket_plus()
        probs = qp.probabilities
        self.assertAlmostEqual(probs[0], 0.5)
        self.assertAlmostEqual(probs[1], 0.5)
        
        qm = Qubit.ket_minus()
        probs = qm.probabilities
        self.assertAlmostEqual(probs[0], 0.5)
        self.assertAlmostEqual(probs[1], 0.5)
    
    def test_from_angle(self):
        """Test qubit creation from Bloch angles."""
        # |0⟩ corresponds to θ=0
        q = Qubit.from_angle(0, 0)
        self.assertTrue(_complex_equal(q.alpha, complex(1, 0)))
        
        # |1⟩ corresponds to θ=π
        q = Qubit.from_angle(math.pi, 0)
        self.assertTrue(_complex_equal(q.beta, complex(1, 0)))
        
        # |+⟩ corresponds to θ=π/2, φ=0
        q = Qubit.from_angle(math.pi/2, 0)
        probs = q.probabilities
        self.assertAlmostEqual(probs[0], 0.5)
    
    def test_hadamard(self):
        """Test Hadamard gate."""
        q = Qubit.ket_zero().h()
        probs = q.probabilities
        self.assertAlmostEqual(probs[0], 0.5)
        self.assertAlmostEqual(probs[1], 0.5)
        
        # H|+⟩ = |0⟩
        q = Qubit.ket_plus().h()
        self.assertTrue(_complex_equal(q.alpha, complex(1, 0)))
        
        # H|−⟩ = |1⟩
        q = Qubit.ket_minus().h()
        self.assertTrue(_complex_equal(q.beta, complex(1, 0)))
    
    def test_pauli_x(self):
        """Test Pauli-X (NOT) gate."""
        q = Qubit.ket_zero().x()
        self.assertTrue(_complex_equal(q.beta, complex(1, 0)))
        
        q = Qubit.ket_one().x()
        self.assertTrue(_complex_equal(q.alpha, complex(1, 0)))
        
        # X*X = I
        q = Qubit.ket_zero().x().x()
        self.assertTrue(_complex_equal(q.alpha, complex(1, 0)))
    
    def test_pauli_y(self):
        """Test Pauli-Y gate."""
        # Y|0⟩ = i|1⟩
        q = Qubit.ket_zero().y()
        self.assertTrue(_complex_equal(q.beta, complex(0, 1)))
        
        # Y|1⟩ = -i|0⟩
        q = Qubit.ket_one().y()
        self.assertTrue(_complex_equal(q.alpha, complex(0, -1)))
        
        # Y*Y = I
        q = Qubit.ket_zero().y().y()
        self.assertTrue(_complex_equal(q.alpha, complex(1, 0)))
    
    def test_pauli_z(self):
        """Test Pauli-Z gate."""
        # Z|0⟩ = |0⟩
        q = Qubit.ket_zero().z()
        self.assertTrue(_complex_equal(q.alpha, complex(1, 0)))
        
        # Z|1⟩ = -|1⟩
        q = Qubit.ket_one().z()
        self.assertTrue(_complex_equal(q.beta, complex(-1, 0)))
        
        # Z*Z = I
        q = Qubit.ket_one().z().z()
        self.assertTrue(_complex_equal(q.beta, complex(1, 0)))
    
    def test_phase_gates(self):
        """Test S and T phase gates."""
        # S|1⟩ = i|1⟩
        q = Qubit.ket_one().s()
        self.assertTrue(_complex_equal(q.beta, complex(0, 1)))
        
        # S*S = Z
        q = Qubit.ket_one().s().s()
        self.assertTrue(_complex_equal(q.beta, complex(-1, 0)))
        
        # T*T = S
        q = Qubit.ket_one().t().t()
        self.assertTrue(_complex_equal(q.beta, complex(0, 1)))
    
    def test_rotation_gates(self):
        """Test rotation gates RX, RY, RZ."""
        # RX(π)|0⟩ = -i|1⟩ (approximately)
        q = Qubit.ket_zero().rx(math.pi)
        self.assertAlmostEqual(abs(q.beta), 1.0)
        
        # RY(π)|0⟩ = |1⟩
        q = Qubit.ket_zero().ry(math.pi)
        self.assertTrue(_complex_equal(q.beta, complex(1, 0)))
        
        # RZ(π)|1⟩ applies phase: e^(iπ/2) = i to |1⟩ component
        # So |1⟩ becomes i|1⟩
        q = Qubit.ket_one().rz(math.pi)
        self.assertAlmostEqual(abs(q.beta), 1.0)
        # The phase should be i (imaginary part = 1)
        self.assertAlmostEqual(q.beta.imag, 1.0)
        
        # RZ(2π)|1⟩ = -|1⟩ (phase wraps)
        q = Qubit.ket_one().rz(2 * math.pi)
        self.assertAlmostEqual(abs(q.beta), 1.0)
        self.assertAlmostEqual(q.beta.real, -1.0)
    
    def test_measurement(self):
        """Test qubit measurement."""
        # |0⟩ always measures 0
        q = Qubit.ket_zero()
        result = q.measure(seed=42)
        self.assertEqual(result.outcome, 0)
        self.assertAlmostEqual(result.probability, 1.0)
        
        # |1⟩ always measures 1
        q = Qubit.ket_one()
        result = q.measure(seed=42)
        self.assertEqual(result.outcome, 1)
        self.assertAlmostEqual(result.probability, 1.0)
        
        # |+⟩ measures 0 or 1 with equal probability
        q = Qubit.ket_plus()
        results = [q.measure(seed=i).outcome for i in range(100)]
        zeros = sum(1 for r in results if r == 0)
        ones = sum(1 for r in results if r == 1)
        self.assertTrue(abs(zeros - ones) < 30)  # Should be approximately equal
    
    def test_bloch_coordinates(self):
        """Test Bloch sphere coordinates."""
        # |0⟩ should be at north pole (z=1)
        q = Qubit.ket_zero()
        bloch = q.get_bloch_coordinates()
        self.assertAlmostEqual(bloch.z, 1.0)
        self.assertAlmostEqual(bloch.theta, 0)
        
        # |1⟩ should be at south pole (z=-1)
        q = Qubit.ket_one()
        bloch = q.get_bloch_coordinates()
        self.assertAlmostEqual(bloch.z, -1.0)
        self.assertAlmostEqual(bloch.theta, math.pi)
        
        # |+⟩ should be on equator (z=0, x=1)
        q = Qubit.ket_plus()
        bloch = q.get_bloch_coordinates()
        self.assertAlmostEqual(bloch.z, 0.0)
        self.assertAlmostEqual(bloch.x, 1.0)
    
    def test_equality(self):
        """Test qubit equality (up to global phase)."""
        q1 = Qubit.ket_zero()
        q2 = Qubit.ket_zero()
        self.assertEqual(q1, q2)
        
        # Global phase doesn't matter
        q3 = Qubit(complex(-1, 0), complex(0, 0))
        self.assertEqual(q1, q3)
        
        q4 = Qubit.ket_one()
        self.assertNotEqual(q1, q4)
    
    def test_repr(self):
        """Test string representation."""
        q = Qubit.ket_zero()
        self.assertIn("|0⟩", str(q))
        
        q = Qubit.ket_one()
        self.assertIn("|1⟩", str(q))
        
        q = Qubit.ket_plus()
        self.assertIn("|0⟩", str(q))
        self.assertIn("|1⟩", str(q))


class TestQuantumRegister(unittest.TestCase):
    """Test quantum register operations."""
    
    def test_init(self):
        """Test register initialization."""
        reg = QuantumRegister(2)
        self.assertEqual(reg.num_qubits, 2)
        self.assertEqual(len(reg.state), 4)
        self.assertTrue(_complex_equal(reg.state[0], complex(1, 0)))
        
        # Invalid state
        with self.assertRaises(ValueError):
            QuantumRegister(2, [complex(1, 0)])  # Wrong size
    
    def test_single_qubit_gates(self):
        """Test single qubit gates on register."""
        reg = QuantumRegister(2)
        reg.apply_hadamard(0)
        
        # After H on qubit 0: state should be (|00⟩ + |01⟩)/√2
        probs = reg.get_probabilities()
        self.assertAlmostEqual(probs[0], 0.5)  # P(00)
        self.assertAlmostEqual(probs[1], 0.5)  # P(01)
        self.assertAlmostEqual(probs[2], 0)   # P(10)
        self.assertAlmostEqual(probs[3], 0)   # P(11)
    
    def test_cnot(self):
        """Test CNOT gate."""
        reg = QuantumRegister(2)
        reg.apply_hadamard(0)
        reg.apply_cnot(0, 1)
        
        # After H+CNOT: Bell state (|00⟩ + |11⟩)/√2
        probs = reg.get_probabilities()
        self.assertAlmostEqual(probs[0], 0.5)  # P(00)
        self.assertAlmostEqual(probs[3], 0.5)  # P(11)
        self.assertAlmostEqual(probs[1], 0)   # P(01)
        self.assertAlmostEqual(probs[2], 0)   # P(10)
    
    def test_cz(self):
        """Test CZ gate."""
        # Note: State index convention:
        # index = qubit0 + 2*qubit1 (bit 0 = qubit 0, bit 1 = qubit 1)
        # index 0 = |00⟩, index 1 = |01⟩ (q0=1,q1=0), index 2 = |10⟩ (q0=0,q1=1), index 3 = |11⟩
        
        reg = QuantumRegister(2)
        reg.apply_x(1)  # Creates state index 2 (q0=0, q1=1)
        reg.apply_cz(0, 1)  # CZ with control=0, target=1. Control (q0) is 0, so no change
        
        probs = reg.get_probabilities()
        self.assertAlmostEqual(probs[2], 1.0)  # State index 2 (q0=0, q1=1)
        
        reg = QuantumRegister(2)
        reg.apply_x(0)
        reg.apply_x(1)  # Creates state index 3 (q0=1, q1=1)
        reg.apply_cz(0, 1)  # CZ|11⟩ = -|11⟩ (phase change only)
        
        probs = reg.get_probabilities()
        self.assertAlmostEqual(probs[3], 1.0)  # Probability unchanged
    
    def test_swap(self):
        """Test SWAP gate."""
        reg = QuantumRegister(2)
        reg.apply_x(0)  # |01⟩
        reg.apply_swap(0, 1)  # SWAP|01⟩ = |10⟩
        
        probs = reg.get_probabilities()
        self.assertAlmostEqual(probs[2], 1.0)  # P(10)
    
    def test_toffoli(self):
        """Test Toffoli gate."""
        reg = QuantumRegister(3)
        reg.apply_x(0)
        reg.apply_x(1)  # |011⟩
        reg.apply_toffoli(0, 1, 2)  # Toffoli|011⟩ = |111⟩
        
        probs = reg.get_probabilities()
        self.assertAlmostEqual(probs[7], 1.0)  # P(111)
        
        # If only one control is 1, target unchanged
        reg = QuantumRegister(3)
        reg.apply_x(0)  # |001⟩
        reg.apply_toffoli(0, 1, 2)  # Toffoli|001⟩ = |001⟩
        
        probs = reg.get_probabilities()
        self.assertAlmostEqual(probs[1], 1.0)  # P(001)
    
    def test_measure_qubit(self):
        """Test measuring a single qubit in register."""
        reg = QuantumRegister(2)
        reg.apply_hadamard(0)
        
        result = reg.measure_qubit(0, seed=42)
        self.assertIn(result.outcome, [0, 1])
        
        # After measurement, state should be collapsed
        probs = reg.get_probabilities()
        if result.outcome == 0:
            self.assertAlmostEqual(probs[0] + probs[2], 1.0)  # Either |00⟩ or |10⟩
        else:
            self.assertAlmostEqual(probs[1] + probs[3], 1.0)  # Either |01⟩ or |11⟩
    
    def test_measure_all(self):
        """Test measuring all qubits."""
        reg = QuantumRegister(2)
        reg.apply_hadamard(0)
        reg.apply_hadamard(1)
        
        result = reg.measure_all(seed=42)
        self.assertIn(result.outcome, [0, 1, 2, 3])
        
        probs = reg.get_probabilities()
        self.assertAlmostEqual(probs[result.outcome], 1.0)
    
    def test_copy(self):
        """Test register copy."""
        reg = QuantumRegister(2)
        reg.apply_hadamard(0)
        
        copy = reg.copy()
        self.assertEqual(copy.num_qubits, reg.num_qubits)
        
        # Original unchanged if copy is modified
        copy.apply_x(0)
        self.assertNotEqual(reg.state, copy.state)
    
    def test_get_qubit(self):
        """Test extracting single qubit."""
        reg = QuantumRegister(2)
        reg.apply_hadamard(0)
        
        q0 = reg.get_qubit(0)
        probs = q0.probabilities
        self.assertAlmostEqual(probs[0], 0.5)
        self.assertAlmostEqual(probs[1], 0.5)
        
        q1 = reg.get_qubit(1)
        probs = q1.probabilities
        self.assertAlmostEqual(probs[0], 1.0)


class TestQuantumCircuit(unittest.TestCase):
    """Test quantum circuit operations."""
    
    def test_init(self):
        """Test circuit initialization."""
        circuit = QuantumCircuit(2)
        self.assertEqual(circuit.num_qubits, 2)
        self.assertEqual(len(circuit.gates), 0)
    
    def test_add_gates(self):
        """Test adding gates to circuit."""
        circuit = QuantumCircuit(2)
        circuit.h(0).cnot(0, 1)
        
        self.assertEqual(len(circuit.gates), 2)
        self.assertEqual(circuit.gates[0].name, 'H')
        self.assertEqual(circuit.gates[1].name, 'CNOT')
    
    def test_run(self):
        """Test running circuit."""
        circuit = QuantumCircuit(2)
        circuit.h(0).cnot(0, 1).measure_all()
        
        results = circuit.run(shots=1000)
        
        # Bell state should give only 00 and 11
        total = sum(results.values())
        self.assertEqual(total, 1000)
        
        # Results should be mostly 00 and 11
        self.assertTrue('00' in results or '11' in results)
    
    def test_get_statevector(self):
        """Test getting state vector."""
        circuit = QuantumCircuit(2)
        circuit.h(0).cnot(0, 1)
        
        state = circuit.get_statevector()
        self.assertEqual(len(state), 4)
        
        # Check Bell state
        self.assertAlmostEqual(abs(state[0])**2, 0.5)
        self.assertAlmostEqual(abs(state[3])**2, 0.5)
    
    def test_repr(self):
        """Test circuit diagram."""
        circuit = QuantumCircuit(2)
        circuit.h(0).cnot(0, 1)
        
        diagram = str(circuit)
        self.assertIn('H', diagram)
        self.assertIn('●', diagram)
        self.assertIn('⊕', diagram)


class TestBellStates(unittest.TestCase):
    """Test Bell state creation."""
    
    def test_bell_state(self):
        """Test Bell state creation."""
        bell = create_bell_state()
        probs = bell.get_probabilities()
        
        self.assertAlmostEqual(probs[0], 0.5)  # |00⟩
        self.assertAlmostEqual(probs[3], 0.5)  # |11⟩
        self.assertAlmostEqual(probs[1], 0)   # |01⟩
        self.assertAlmostEqual(probs[2], 0)   # |10⟩
    
    def test_ghz_state(self):
        """Test GHZ state creation."""
        ghz = create_ghz_state(3)
        probs = ghz.get_probabilities()
        
        self.assertAlmostEqual(probs[0], 0.5)  # |000⟩
        self.assertAlmostEqual(probs[7], 0.5)  # |111⟩
        
        for i in range(1, 7):
            self.assertAlmostEqual(probs[i], 0)
    
    def test_w_state(self):
        """Test W state creation."""
        w = create_w_state(3)
        probs = w.get_probabilities()
        
        # W state: (|001⟩ + |010⟩ + |100⟩)/√3
        self.assertAlmostEqual(probs[1], 1/3)  # |001⟩
        self.assertAlmostEqual(probs[2], 1/3)  # |010⟩
        self.assertAlmostEqual(probs[4], 1/3)  # |100⟩
        
        self.assertAlmostEqual(probs[0], 0)   # |000⟩
        self.assertAlmostEqual(probs[7], 0)   # |111⟩


class TestEntanglement(unittest.TestCase):
    """Test entanglement functions."""
    
    def test_entangle(self):
        """Test entangling two qubits."""
        q1 = Qubit.ket_zero()
        q2 = Qubit.ket_zero()
        
        reg = entangle(q1, q2)
        probs = reg.get_probabilities()
        
        # Should be Bell state
        self.assertAlmostEqual(probs[0], 0.5)
        self.assertAlmostEqual(probs[3], 0.5)
    
    def test_is_entangled(self):
        """Test entanglement detection."""
        bell = create_bell_state()
        self.assertTrue(is_entangled(bell))
        
        # Separable state
        reg = QuantumRegister(2)
        reg.apply_hadamard(0)
        self.assertFalse(is_entangled(reg))


class TestQuantumGates(unittest.TestCase):
    """Test QuantumGate class."""
    
    def test_gate_composition(self):
        """Test gate composition."""
        H = QuantumGate('H', H_GATE)
        X = QuantumGate('X', X_GATE)
        
        # H@H should give identity (up to scaling)
        HH = H @ H
        # Check that HH acting on |0⟩ gives |0⟩
        q = Qubit.ket_zero()
        q_result = q.apply_gate(HH)
        self.assertTrue(_complex_equal(q_result.alpha, complex(1, 0)))


class TestRandom(unittest.TestCase):
    """Test random seed reproducibility."""
    
    def test_reproducible_measurement(self):
        """Test that measurements are reproducible with seed."""
        q = Qubit.ket_plus()
        
        results = [q.measure(seed=42).outcome for _ in range(10)]
        expected = results.copy()
        
        # Same seed should give same results
        results2 = [q.measure(seed=42).outcome for _ in range(10)]
        self.assertEqual(results, results2)


if __name__ == '__main__':
    unittest.main(verbosity=2)