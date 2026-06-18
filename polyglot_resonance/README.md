# 🎵 Polyglot Resonance

A creative tool that maps how programming concepts "resonate" differently across the language spectrum — as harmonic frequency shifts and phase distortions.

## Features

- **Resonance Themes**: Universal programming concepts mapped as frequencies
- **Waveform Visualization**: ASCII oscilloscope display of language "vibrations"
- **Harmonic Analysis**: Which languages are "in tune" vs. create dissonance
- **Cross-Language Mapping**: How the same concept sounds in each language
- **Rotation Support**: Automatically selects next language via `language_rotation.json`

## Installation

```bash
cd polyglot_resonance
python -m polyglot_resonance --help
```

## Usage

```bash
# Run tests
python -m polyglot_resonance --test

# Generate resonance analysis for current rotation language
python -m polyglot_resonance

# JSON output
python -m polyglot_resonance --json
```

## Example Output

```
🎵 Polyglot Resonance — Language Vibrations
═══════════════════════════════════════════════════════════════

  Language: Go 🐹
  Theme: State Mutation 🔄
  Fundamental: 440.0 Hz (A4)

  ─── Waveform ───────────────────────────────────────────
          ●●
      ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
      ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
  ────────────────────────────────────────────────────────

  Frequency: 438.0 Hz (triangle wave)
  Phase: +0.05 — slightly behind perfect resonance
  In Tune: ✓ (in_tune)
```

## Languages Covered

- Rust, Go, Swift, Kotlin, TypeScript, JavaScript, Java, C/C++

## Module Structure

```
polyglot_resonance/
├── src/
│   └── __init__.py     # Main module (TOOL_NAME, resonance functions)
├── tests/
│   └── test_resonance.py  # 15 test cases
└── README.md
```

## Tests

Run tests with:
```bash
python -m pytest tests/ -v
```

Test coverage includes:
- Tool name and version constants
- Rotation order and resonance themes
- Main resonance() function
- generate_resonance_analysis() for all languages
- format_resonance() output
- Rotation file operations
