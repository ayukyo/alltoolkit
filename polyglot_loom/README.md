# 🪡 polyglot_loom v1.0.0

A **weaving/textile arts** engine for programming languages — every language
is treated as a hand-loom with warp, weft, threads, heddles, shuttles, bobbins,
dye-pots, and pattern books.

## Concept

> "Every program is a tapestry, and every language is a loom. Some looms
> are sturdy oaken floor-looms (C/C++), some are sleek modern rigid-heddle
> (TypeScript), some are circular knitting rings (Kotlin), some are Jacquard
> punched-card marvels (Rust's ownership checker)."

Each language gets a **loom archetype**, a **fabric** it weaves, and the
complete toolkit: warp threads (static syntax), weft threads (dynamic runtime),
heddles (type system), shuttles (control flow), bobbins (primitives), dye
palette (syntax highlighting), pattern book (idioms), and an ASCII weave
preview.

## Features

1. **Loom Catalogue** — every language mapped to a loom archetype
2. **Warp & Weft** — static (syntax/keywords) vs dynamic (runtime) thread inventories
3. **Thread Library** — package/library ecosystem as dyed threads
4. **Heddle Map** — type system rules that comb the warp threads
5. **Shuttle Patterns** — control-flow motifs (looping, branching, async)
6. **Bobbin Inventory** — primitives & value types in the loom's bin
7. **Dye-Pot Palette** — color mapping for syntax highlighting
8. **Cloth Density** — composite density (precision × complexity × weight)
9. **Pattern Book** — idiomatic weave patterns for each language
10. **ASCII Tapestry Preview** — deterministic woven cloth rendered in monospace
11. **Snippet-aware Weave Detection** — detect which pattern book pattern applies
12. **Dye Comparison** — palette similarity between two looms
13. **Loom Tour** — visit all 8 looms in sequence
14. **Rotation Advance** — reads/updates `language_rotation.json`

## Loom archetypes at a glance

| Language    | Loom                                    | Fabric                              |
|-------------|-----------------------------------------|-------------------------------------|
| Rust        | Jacquard Loom (punched-card)            | Borrowed Ownership Cloth            |
| Go          | Sturdy Floor Loom (rigid-heddle)        | Goroutine Plain-Weave               |
| Swift       | Tartan Loom (patterned, decorative)     | Optional-Value Tartan               |
| Kotlin      | Circular Knitting Loom                  | Null-Safe Knit                      |
| TypeScript  | Rigid-Heddle Modern Loom                | Typed Huck-a-Back                   |
| JavaScript  | Backstrap Loom (portable)               | Async Huck                          |
| Java        | Heavy Industrial Loom                   | Enterprise Twill                    |
| C/C++       | Handloom of Antiquity                   | Foundational Linen                  |

## Usage

```bash
# Generate a loom report for the current rotation language
python -m polyglot_loom

# Loom report for a specific language
python -m polyglot_loom Java

# Feed a code snippet for weave-pattern detection
python -m polyglot_loom Rust --snippet "let v: Vec<i32> = xs.iter().map(|x| x*2).collect();"

# Compare dye palettes between two languages
python -m polyglot_loom --dye Rust Go

# Tour all 8 looms
python -m polyglot_loom --tour

# Show the current rotation language (no advance)
python -m polyglot_loom --current

# Run self-tests
python -m polyglot_loom --test
```

## What makes it different

- **polyglot_bloom** — gardening / phenology (organic growth lens)
- **polyglot_lullaby** — bedtime narrative (calming lens)
- **polyglot_mood** — emotional profiling (psychological lens)
- **polyglot_flavor** — sensory sommelier (taste lens)
- **polyglot_vessel** — essence distillation (alembic lens)
- **polyglot_pulse** — vital signs (medical lens)
- **polyglot_wire** — cross-language FFI (electrical lens)
- **polyglot_reef** — marine ecosystem (oceanic lens)
- **polyglot_forge** — metalworking / smithing lens
- **polyglot_orbit** — celestial mechanics (spatial lens)
- **polyglot_rorschach** — inkblot projection (psychoanalytic lens)
- **polyglot_metamorphosis** — AST transformation (transmutation lens)

**Loom is about WEAVING / TEXTILE ARTS** — threads, heddles, shuttles,
warps, wefts, bobbins, dye-pots, patterns, and cloth. No other tool does that.

## Tests

```bash
cd AllToolkit
python -m polyglot_loom --test                 # built-in runner
python -m pytest polyglot_loom/tests/test_loom.py -v   # pytest wrapper
```

The self-test suite covers:

- Rotation file shape (8 languages, current_index, last_language, updated_at)
- Loom catalogue completeness (every language has all required fields)
- Cloth density math (within [0,10])
- Thread library health (foundation / runtime / utility classification)
- Weave pattern detection (with and without snippets)
- Dye recipe generation (5 dyes per loom, gradient suggestion)
- ASCII weave preview (deterministic, framed)
- Loom report structure (all expected keys)
- Loom tour coverage (8 looms)
- Dye comparison symmetry
- Rotation advance / wrap behavior
- Deterministic digest
- Vitality score range

Rotation: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust