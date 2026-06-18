# 🗺️ Polyglot Topology

A tool that maps the topological structure of programming language design space — which languages are "neighbors", which are "isolated continents", and what the shape of each language's neighborhood looks like.

## Features

- **Design Space Mapping**: Visualizes languages as points in abstract design space
- **Neighborhood Graph**: Shows which languages are topologically "close"
- **Boundary Lines**: Paradigm boundaries between language groups
- **ASCII Topology Maps**: Bird's-eye view of the language landscape
- **Rotation Support**: Automatically selects next language via `language_rotation.json`

## Installation

```bash
cd polyglot_topology
python -m polyglot_topology --help
```

## Usage

```bash
# Run tests
python -m polyglot_topology --test

# Generate topology map for current rotation language
python -m polyglot_topology

# Generate for specific language
python -m polyglot_topology Rust

# JSON output
python -m polyglot_topology --json
```

## Example Output

```
🗺️ Polyglot Topology — Language Design Space
═══════════════════════════════════════════════════════════════

  Language: Rust 🦀
  Region: Memory Safety Island (Ownership)
  Continent: Systems Security Continent

  ─── Topology Map ────────────────────────────────────────
                    [C/C++]
                         ↑
      [Rust] ←→ [Swift] ←→ [Kotlin]
        ↑               ↕         ↑
        |    [Go]      [Java]     |
        |      ↑        ↑         |
    (isolated)   [TypeScript] ←[JavaScript]
  ────────────────────────────────────────────────────────

  Neighbors: C/C++, Swift, Kotlin
  Topological Signature: ∂(∅) — zero aliasing boundary
```

## Languages Covered

- Rust, Go, Swift, Kotlin, TypeScript, JavaScript, Java, C/C++

## Module Structure

```
polyglot_topology/
├── src/
│   └── __init__.py     # Main module (topology functions)
├── tests/
│   └── test_topology.py  # 21 test cases
└── README.md
```

## Tests

```bash
python -m pytest tests/ -v
```

Test coverage includes:
- Tool name and version constants
- Feature vectors and neighborhood graph
- `_render_topology_map()` for all languages
- `_compute_topological_metrics()` for all languages
- `topology()` and `compute_topology()` main functions
- Rotation file operations
