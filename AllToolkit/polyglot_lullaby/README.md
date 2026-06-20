# 🍼 polyglot_lullaby v1.0.0

A creative tool that composes a **lullaby** for a programming language — a soothing,
structured "bedtime story" pairing each language's anxieties with idiomatic remedies.

## Concept

Every language has its own bedtime worries. `polyglot_lullaby` reads a code snippet
(or a stress topic) and hums back a calm narrative: a verse list of stanzas
(anxieties), refrains (idiomatic relief), and a final benediction.

## What makes it different

- **8 distinct musical keys** — each language in the rotation gets a unique
  musical key, motif, and tempo (Rust = D minor "ownership cradle", Go = G major
  "goroutine lull", Swift = A major "optional cocoon", etc.).
- **Keyword-aware verse selection** — scans your snippet for telltale tokens
  (`async`, `chan`, `!`, `malloc`, etc.) and surfaces the most relevant stanzas.
- **Deterministic** — same language + same snippet always hums the same tune
  (SHA-1 digest drives refrain/benediction selection).
- **Rotation-aware** — reads `language_rotation.json` and rotates `current_index`
  after each invocation.

## Usage

```bash
# Compose a lullaby for the current language in the rotation
python -m polyglot_lullaby

# Compose for a specific language + a code snippet
python -m polyglot_lullaby Rust "let v: Vec<i32> = (0..n).collect(); let w = v; v.push(1);"

# Run self-tests
python -m polyglot_lullaby --test

# Advance the rotation and persist
python -m polyglot_lullaby --advance
```

## Tests

```bash
cd AllToolkit
python -m pytest polyglot_lullaby/tests/test_lullaby.py -v
```

17 tests cover module metadata, verse library coverage, anxiety detection across
all 8 languages, deterministic composition, and rotation advance/wrap behavior.
