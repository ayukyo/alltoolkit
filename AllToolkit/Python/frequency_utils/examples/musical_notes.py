#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Frequency Utilities - Musical Notes Examples
=============================================

Examples demonstrating musical note frequency calculations.
"""

import sys
sys.path.insert(0, '..')

from mod import (
    note_to_frequency,
    frequency_to_note,
    get_midi_frequency,
    calculate_cents,
    cents_to_frequency,
    get_note_harmonics,
    generate_major_scale,
    generate_chromatic_scale,
    format_frequency,
)


def main():
    print("=" * 60)
    print("Frequency Utilities - Musical Notes Examples")
    print("=" * 60)
    
    # 1. Note names to frequencies
    print("\n--- Note to Frequency ---")
    print(f"A4 (standard): {note_to_frequency('A', 4):.2f} Hz")
    print(f"C4 (Middle C): {note_to_frequency('C', 4):.2f} Hz")
    print(f"E4: {note_to_frequency('E', 4):.2f} Hz")
    print(f"G4: {note_to_frequency('G', 4):.2f} Hz")
    print(f"A#4 / Bb4: {note_to_frequency('A#', 4):.2f} Hz")
    
    # Using different A4 reference
    print(f"\n--- Using A4 = 442 Hz (some orchestras) ---")
    print(f"A4: {note_to_frequency('A', 4, a4_hz=442):.2f} Hz")
    print(f"C4: {note_to_frequency('C', 4, a4_hz=442):.2f} Hz")
    
    # 2. Frequency to note
    print("\n--- Frequency to Note ---")
    test_freqs = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]
    for freq in test_freqs:
        note = frequency_to_note(freq)
        print(f"{freq:.2f} Hz → {note.full_name} (MIDI: {note.midi_note})")
    
    # 3. MIDI note numbers
    print("\n--- MIDI Note Frequencies ---")
    print(f"MIDI 60 (C4): {get_midi_frequency(60):.2f} Hz")
    print(f"MIDI 69 (A4): {get_midi_frequency(69):.2f} Hz")
    print(f"MIDI 21 (A0): {get_midi_frequency(21):.2f} Hz (lowest piano A)")
    print(f"MIDI 108 (C8): {get_midi_frequency(108):.2f} Hz (highest piano C)")
    
    # 4. Cent calculations
    print("\n--- Cent (Pitch) Calculations ---")
    
    # Octave
    cents = calculate_cents(440, 880)
    print(f"440 → 880 Hz: {cents:.0f} cents (one octave)")
    
    # Semitone
    cents = calculate_cents(440, 466.16)
    print(f"440 → 466.16 Hz: {cents:.0f} cents (one semitone)")
    
    # Perfect fifth
    cents = calculate_cents(440, 660)
    print(f"440 → 660 Hz: {cents:.0f} cents (perfect fifth ~702 cents)")
    
    # From cents to frequency
    print("\n--- Cents to Frequency ---")
    freq = cents_to_frequency(440, 100)
    print(f"440 Hz + 100 cents = {freq:.2f} Hz (A#4)")
    freq = cents_to_frequency(440, -100)
    print(f"440 Hz - 100 cents = {freq:.2f} Hz (G#4)")
    
    # 5. Harmonics series
    print("\n--- Harmonic Series (A4) ---")
    harmonics = get_note_harmonics(440, 8)
    print(f"Fundamental: {harmonics.fundamental_hz:.2f} Hz (A4)")
    for n, freq, note_name in harmonics.harmonics:
        print(f"  {n}×: {freq:.2f} Hz ({note_name})")
    
    # 6. Major scale
    print("\n--- C Major Scale ---")
    scale = generate_major_scale('C', 4)
    for note_name, octave, freq in scale:
        print(f"  {note_name}{octave}: {format_frequency(freq)}")
    
    # 7. Chromatic scale
    print("\n--- Chromatic Scale (C4-C5) ---")
    scale = generate_chromatic_scale('C', 4, 13)
    for note_name, octave, freq in scale:
        print(f"  {note_name}{octave}: {format_frequency(freq)}")


if __name__ == '__main__':
    main()