# 📡 Polyglot Anomaly Detector

A creative tool that catalogs the quirks, paradoxes, and delightful contradictions of programming languages — the moments where each language breaks from expectation and reveals something deeper about its design philosophy.

## Features

- **Anomaly Catalog**: Documented language quirks, edge cases, and counterintuitive behaviors
- **Severity Classification**: Each anomaly rated as critical/high/medium/low
- **Paradoxes**: Philosophical contradictions unique to each language
- **Workarounds**: Practical solutions for each documented anomaly
- **Rotation Support**: Automatically selects next language via `language_rotation.json`

## Installation

```bash
cd polyglot_anomaly
python -m polyglot_anomaly --help
```

## Usage

```bash
# Run tests
python -m polyglot_anomaly --test

# Generate anomaly report for current rotation language
python -m polyglot_anomaly

# Generate report for specific language
python -m polyglot_anomaly --detect Rust

# JSON output
python -m polyglot_anomaly --json
```

## Example Output

```
========================================================
  🦀 Rust -- Anomaly Report
========================================================
  Tool: polyglot-anomaly v1.0.0
  Anomalies documented: 5
  Severity: CRITICAL=0 HIGH=2 MEDIUM=2 LOW=1
  Next language: Go
========================================================

[1] Recursive Mutable Borrows Are Forbidden (HIGH)
    ID: rust-001
    Cannot have a data structure that contains a mutable reference to itself.
    Paradox: Safety enforcement creates constraints safe code cannot express.
    Workaround: Use Rc<RefCell<T>> or Box<T> for recursive types.
    Example: struct Node { child: &mut Node } // ERROR
```

## Languages Covered

- Rust, Go, Swift, Kotlin, TypeScript, JavaScript, Java, C/C++

## Module Structure

```
polyglot_anomaly/
├── __init__.py           # Package entry with imports
├── __main__.py           # CLI entry point
├── src/
│   └── anomaly.py        # Core implementation with ANOMALY_DATA
└── README.md
```
