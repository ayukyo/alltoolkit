# 🕰️ polyglot_horology v1.0.0

A **watchmaking / clockwork** engine for programming languages — every
language is treated as a precision timepiece, with movements, mainsprings,
escapements, balance wheels, jewels, gear trains, bridges, plates,
complications, and chronometric profiles.

## Concept

> "Every program tells time. Some languages are skeleton tourbillons —
> every gear visible, every jewel polished, every millisecond accounted for
> (Rust). Some are quartz field watches — battery-powered, ubiquitous,
> near-perfect (Go). Some are Apple Watches with a digital crown and OLED
> dial (Swift). Some are grandfather clocks — slow, loud, accurate, and
> meant to outlast generations (Java). The horologist — the developer —
> winds the mainspring, oils the jewels, assembles the plates, fits the
> bridges, and produces a movement."

Each language gets a **movement archetype**, a **dial face**, a **caliber
reference**, and the complete toolkit: mainspring (runtime), escapement
(control flow), balance wheel (type system), jewels (primitives), bridges
(framework pieces), plates (build files), complications (extra features),
gear train (compile pipeline), and a chronometric profile (precision).

## Features

- 🕰️ **Movement Catalogue** — every language mapped to a watch archetype
- ⚙️ **Mainspring** — power source (the runtime / language spec)
- 🔄 **Escapement** — cadence (control flow / scheduler)
- ⚖️ **Balance Wheel** — regulator (type system / memory model)
- 💎 **Jewels** — anti-friction bearings (primitive types)
- 🛠️ **Gear Train** — operation pipeline (compile → link → run)
- 🌉 **Bridges & Plates** — internal architecture (frameworks, std lib)
- 🎯 **Complications** — extra features (async, generics, FFI, GC)
- ⏱️ **Chronograph** — stopwatch capability (profiling, tracing)
- 🎨 **Dial** — the public interface (syntax + idioms)
- 👑 **Crown** — the user input mechanism (REPL / build tool)
- 🕒 **Timekeeping Rate** — performance & precision profile
- 🔋 **Power Reserve** — runtime longevity (memory / startup)
- 🌐 **Movement Tour** — visit all 8 movements in sequence
- 🆚 **Chronometer Compare** — chronometric comparison between two languages
- 🔁 **Rotation Advance** — reads/updates `language_rotation.json`

## Languages Covered

Rust (skeleton tourbillon), Go (quartz field watch), Swift (Apple Watch),
Kotlin (perpetual calendar), TypeScript (sapphire-crystal field watch),
JavaScript (smartwatch with web apps), Java (grandfather clock),
C/C++ (marine chronometer).

## Usage

```bash
# Run the movement report for the rotation's current language (advances index)
python -m polyglot_horology

# Run for a specific language (does not advance rotation)
python -m polyglot_horology Rust

# Tour all 8 movements
python -m polyglot_horology --tour

# Chronometer comparison between two languages
python -m polyglot_horology --compare Rust Go

# Show current rotation language
python -m polyglot_horology --current

# Run all self-tests
python -m polyglot_horology --test

# Feed a code snippet for crown-signature detection
python -m polyglot_horology --snippet "async fn fetch() -> Result<...> { ... }"
```

## Rotation

Follows `Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust`
(loops). Reads and updates the workspace's `language_rotation.json`.

## Distinct From Other Tools

| Tool | Lens |
|------|------|
| `polyglot_loom` | Weaving / textile arts |
| `polyglot_tempo` | Musical rhythm |
| `polyglot_odyssey` | Time-travel journey |
| `polyglot_forge` | Metalworking |
| `polyglot_orbit` | Celestial mechanics |
| `polyglot_metamorphosis` | AST transformation |
| `polyglot_reef` | Marine ecosystem |
| `polyglot_pulse` | Vital signs |
| `polyglot_vessel` | Alembic / distillation |
| `polyglot_horology` | **Watchmaking / clockwork** ← *this tool* |

## Test

```bash
python -m polyglot_horology --test
# or
cd AllToolkit && python -m pytest polyglot_horology/tests/
```
