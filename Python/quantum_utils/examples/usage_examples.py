#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Quantum Computing Utilities Examples
===================================================
Practical examples demonstrating quantum computing concepts.

Examples include:
    1. Basic qubit operations
    2. Quantum gates and circuits
    3. Bell states and entanglement
    4. Quantum teleportation simulation
    5. Simple quantum algorithms
    6. Bloch sphere visualization

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
from mod import (
    Qubit, QuantumRegister, QuantumCircuit,
    create_bell_state, create_ghz_state, create_w_state,
    is_entangled, entangle,
    quantum_fourier_transform, grover_oracle, grover_diffusion,
    teleportation_circuit,
    H_GATE, X_GATE, Z_GATE
)


def example_1_basic_qubit():
    """Example 1: Basic qubit operations."""
    print("=" * 60)
    print("Example 1: Basic Qubit Operations")
    print("=" * 60)
    
    # Create qubits in different states
    q0 = Qubit.ket_zero()
    q1 = Qubit.ket_one()
    qp = Qubit.ket_plus()
    qm = Qubit.ket_minus()
    
    print("\nStandard basis states:")
    print(f"|0⟩ = {q0}")
    print(f"|1⟩ = {q1}")
    
    print("\nSuperposition states:")
    print(f"|+⟩ = {qp}")
    print(f"|−⟩ = {qm}")
    
    print("\nProbabilities:")
    print(f"P(|0⟩): 0={q0.probabilities[0]:.2f}, 1={q0.probabilities[1]:.2f}")
    print(f"P(|+⟩): 0={qp.probabilities[0]:.2f}, 1={qp.probabilities[1]:.2f}")
    
    # Bloch sphere coordinates
    print("\nBloch sphere coordinates:")
    bloch = qp.get_bloch_coordinates()
    print(f"|+⟩: θ={bloch.theta:.4f}, φ={bloch.phi:.4f}")
    print(f"     x={bloch.x:.4f}, y={bloch.y:.4f}, z={bloch.z:.4f}")
    
    # Measurements
    print("\nMeasurements (10 trials each):")
    print("|+⟩ outcomes:", [qp.measure(seed=i).outcome for i in range(10)])
    print("|−⟩ outcomes:", [qm.measure(seed=i).outcome for i in range(10)])


def example_2_quantum_gates():
    """Example 2: Quantum gates."""
    print("\n" + "=" * 60)
    print("Example 2: Quantum Gates")
    print("=" * 60)
    
    print("\nHadamard gate transforms:")
    print(f"H|0⟩ = {Qubit.ket_zero().h()}")
    print(f"H|1⟩ = {Qubit.ket_one().h()}")
    print(f"H|+⟩ = {Qubit.ket_plus().h()}")
    print(f"H|−⟩ = {Qubit.ket_minus().h()}")
    
    print("\nPauli gates:")
    print(f"X|0⟩ = {Qubit.ket_zero().x()}  (NOT gate)")
    print(f"X|1⟩ = {Qubit.ket_one().x()}")
    print(f"Y|0⟩ = {Qubit.ket_zero().y()}")
    print(f"Z|1⟩ = {Qubit.ket_one().z()}")
    
    print("\nPhase gates:")
    print(f"S|1⟩ = {Qubit.ket_one().s()}")
    print(f"T|1⟩ = {Qubit.ket_one().t()}")
    
    print("\nRotation gates:")
    print(f"RY(π/2)|0⟩ = {Qubit.ket_zero().ry(math.pi/2)}")
    print(f"RX(π)|0⟩ = {Qubit.ket_zero().rx(math.pi)}")


def example_3_quantum_circuit():
    """Example 3: Quantum circuit building."""
    print("\n" + "=" * 60)
    print("Example 3: Quantum Circuit Building")
    print("=" * 60)
    
    # Create a circuit
    circuit = QuantumCircuit(2)
    circuit.h(0)        # Hadamard on qubit 0
    circuit.cnot(0, 1)  # CNOT with control=0, target=1
    circuit.measure_all()
    
    print("\nCircuit diagram:")
    print(circuit)
    
    print("\nState vector after gates:")
    statevector_circuit = QuantumCircuit(2)
    statevector_circuit.h(0).cnot(0, 1)
    state = statevector_circuit.get_statevector()
    print(f"State: {state}")
    
    print("\nRunning circuit (1000 shots):")
    results = circuit.run(shots=1000)
    print(f"Results: {results}")
    
    # Probability analysis
    total = sum(results.values())
    print(f"\nProbability analysis:")
    for outcome, count in sorted(results.items()):
        print(f"  |{outcome}⟩: {count/total:.2%}")


def example_4_bell_states():
    """Example 4: Bell states and entanglement."""
    print("\n" + "=" * 60)
    print("Example 4: Bell States and Entanglement")
    print("=" * 60)
    
    print("\nCreating Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2:")
    bell = create_bell_state()
    print(f"State: {bell}")
    print(f"Entangled: {is_entangled(bell)}")
    
    print("\nProbability distribution:")
    probs = bell.get_probabilities()
    print(f"P(|00⟩) = {probs[0]:.4f}")
    print(f"P(|01⟩) = {probs[1]:.4f}")
    print(f"P(|10⟩) = {probs[2]:.4f}")
    print(f"P(|11⟩) = {probs[3]:.4f}")
    
    print("\nGHZ state |GHZ⟩ = (|000⟩ + |111⟩)/√2:")
    ghz = create_ghz_state(3)
    print(f"State: {ghz}")
    
    print("\nW state |W⟩ = (|001⟩ + |010⟩ + |100⟩)/√3:")
    w = create_w_state(3)
    print(f"State: {w}")
    
    print("\nMeasuring Bell state 100 times:")
    results = {}
    for i in range(100):
        reg = create_bell_state()
        outcome = reg.measure_all(seed=i).outcome
        key = bin(outcome)[2:].zfill(2)
        results[key] = results.get(key, 0) + 1
    print(f"Results: {results}")
    print("(Notice: only 00 and 11 outcomes - perfect correlation!")


def example_5_quantum_teleportation():
    """Example 5: Quantum teleportation."""
    print("\n" + "=" * 60)
    print("Example 5: Quantum Teleportation Simulation")
    print("=" * 60)
    
    print("\nQuantum teleportation circuit:")
    circuit = teleportation_circuit()
    print(circuit)
    
    print("\nTeleportation steps:")
    print("1. Alice and Bob share a Bell pair (qubits 1 and 2)")
    print("2. Alice entangles her message qubit (qubit 0) with her half")
    print("3. Alice measures qubits 0 and 1")
    print("4. Bob applies corrections based on measurement results")
    
    print("\nSimulating teleportation:")
    
    # Create a message qubit with some state
    message = Qubit.from_angle(math.pi/4, math.pi/6)
    print(f"Message state: {message}")
    
    # Set up teleportation
    reg = QuantumRegister(3)
    reg.apply_single_qubit_gate(H_GATE, 1)
    reg.apply_cnot(1, 2)
    
    # Entangle message with Alice's half
    reg.apply_cnot(0, 1)
    reg.apply_single_qubit_gate(H_GATE, 0)
    
    # Alice measures
    m0 = reg.measure_qubit(0)
    m1 = reg.measure_qubit(1)
    
    print(f"Alice's measurements: {m0.outcome}, {m1.outcome}")
    
    # Bob's corrections (simplified)
    print("Bob applies corrections based on Alice's classical message")


def example_6_superdense_coding():
    """Example 6: Superdense coding."""
    print("\n" + "=" * 60)
    print("Example 6: Superdense Coding")
    print("=" * 60)
    
    print("\nSuperdense coding: send 2 bits using 1 qubit")
    print("Alice and Bob share a Bell pair.")
    print("Alice encodes 2 bits by applying gates to her qubit.")
    
    # Message to send: '01'
    message = '01'
    
    print(f"\nEncoding message: {message}")
    
    # Start with Bell state
    reg = QuantumRegister(2)
    reg.apply_single_qubit_gate(H_GATE, 0)
    reg.apply_cnot(0, 1)
    
    # Alice applies gates based on message
    if message[0] == '1':
        reg.apply_single_qubit_gate(Z_GATE, 0)
    if message[1] == '1':
        reg.apply_single_qubit_gate(X_GATE, 0)
    
    # Bob decodes by reversing Bell state creation
    reg.apply_cnot(0, 1)
    reg.apply_single_qubit_gate(H_GATE, 0)
    
    print(f"State after encoding: {reg}")
    
    # Measure both qubits
    result = reg.measure_all(seed=42)
    decoded = bin(result.outcome)[2:].zfill(2)
    
    print(f"Decoded message: {decoded}")
    print(f"Original message: {message}")
    print(f"Match: {decoded == message}")


def example_7_grover_search():
    """Example 7: Grover's search algorithm (simplified)."""
    print("\n" + "=" * 60)
    print("Example 7: Grover's Search Algorithm")
    print("=" * 60)
    
    print("\nGrover's algorithm searches unsorted database.")
    print("Classical: O(N), Quantum: O(√N)")
    
    # 2-qubit example, searching for |11⟩
    target = 3  # |11⟩ in decimal
    
    print(f"Searching for state |{bin(target)[2:].zfill(2)}⟩")
    
    # Create circuit
    circuit = QuantumCircuit(2)
    
    # Initial superposition
    circuit.h(0)
    circuit.h(1)
    
    # Grover iterations (for 2 qubits, optimal is 1 iteration)
    # Oracle marks |11⟩
    circuit.h(1)
    circuit.z(1)
    circuit.h(1)
    
    # Diffusion operator
    circuit.h(0).h(1)
    circuit.z(0).z(1)
    circuit.cnot(0, 1)
    circuit.z(1)
    circuit.cnot(0, 1)
    circuit.h(0).h(1)
    
    circuit.measure_all()
    
    print("\nCircuit:")
    print(circuit)
    
    print("\nRunning search (100 shots):")
    results = circuit.run(shots=100)
    print(f"Results: {results}")
    
    # Check if target is found
    target_str = bin(target)[2:].zfill(2)
    if target_str in results:
        print(f"\nTarget |{target_str}⟩ found {results[target_str]} times!")


def example_8_quantum_fourier_transform():
    """Example 8: Quantum Fourier Transform."""
    print("\n" + "=" * 60)
    print("Example 8: Quantum Fourier Transform")
    print("=" * 60)
    
    print("\nQFT transforms computational basis to Fourier basis.")
    print("Used in Shor's algorithm and phase estimation.")
    
    # Create QFT circuit
    circuit = quantum_fourier_transform(3)
    
    print("\nQFT(3) circuit:")
    print(circuit)
    
    print("\nQFT properties:")
    print("|0⟩ → (|0⟩ + |1⟩ + |2⟩ + |3⟩ + |4⟩ + |5⟩ + |6⟩ + |7⟩)/√8")


def example_9_quantum_random_number():
    """Example 9: Quantum random number generation."""
    print("\n" + "=" * 60)
    print("Example 9: Quantum Random Number Generation")
    print("=" * 60)
    
    print("\nTrue random numbers from quantum measurement:")
    
    # Create n-qubit register in superposition
    def quantum_random_bits(n_bits: int) -> str:
        reg = QuantumRegister(n_bits)
        for i in range(n_bits):
            reg.apply_hadamard(i)
        
        result = reg.measure_all()
        return bin(result.outcome)[2:].zfill(n_bits)
    
    print("\nGenerating 8 random bits:")
    random_numbers = [quantum_random_bits(8) for _ in range(10)]
    for i, num in enumerate(random_numbers):
        print(f"  {i+1}: {num} ({int(num, 2)})")
    
    print("\nGenerating random numbers in range [0, 100]:")
    for i in range(5):
        bits = quantum_random_bits(7)  # 7 bits can represent 0-127
        num = int(bits, 2)
        if num <= 100:
            print(f"  {i+1}: {num}")
        else:
            print(f"  {i+1}: {num} (out of range, retry)")


def example_10_quantum_coin_flips():
    """Example 10: Quantum coin flipping."""
    print("\n" + "=" * 60)
    print("Example 10: Quantum Coin Flipping")
    print("=" * 60)
    
    print("\nQuantum coin flip using |+⟩ state:")
    
    # Multiple coin flips
    outcomes = []
    for i in range(20):
        coin = Qubit.ket_plus()
        result = coin.measure(seed=i)
        outcomes.append(result.outcome)
    
    print(f"Outcomes: {outcomes}")
    print(f"Heads (0): {sum(1 for o in outcomes if o == 0)}")
    print(f"Tails (1): {sum(1 for o in outcomes if o == 1)}")
    
    # Biased coin
    print("\nBiased coin (75% heads):")
    biased = Qubit(math.sqrt(0.75), math.sqrt(0.25))
    print(f"State: {biased}")
    
    outcomes = [biased.measure(seed=i).outcome for i in range(100)]
    print(f"Heads: {sum(1 for o in outcomes if o == 0)}")
    print(f"Tails: {sum(1 for o in outcomes if o == 1)}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("QUANTUM COMPUTING UTILITIES - EXAMPLES")
    print("=" * 60)
    
    example_1_basic_qubit()
    example_2_quantum_gates()
    example_3_quantum_circuit()
    example_4_bell_states()
    example_5_quantum_teleportation()
    example_6_superdense_coding()
    example_7_grover_search()
    example_8_quantum_fourier_transform()
    example_9_quantum_random_number()
    example_10_quantum_coin_flips()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()