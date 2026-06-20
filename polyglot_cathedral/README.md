# ⛪ Polyglot Cathedral

> A gothic-architecture engine for programming languages.
> Every language is a cathedral with its own diocese, style, nave, buttresses, gargoyles, and architects.

## Concept

A programming language is a **cathedral**. The floor plan is its paradigm;
the nave is its main runtime; the flying buttresses are its type system
supports; the rose window is its central abstraction; the gargoyles are
its footguns; the bell tower is its concurrency rhythm; the stained
glass is its syntax-highlighting palette; and the architects are the
people who designed it over time.

## Features

- **Cathedral Catalogue** — every language mapped to a unique cathedral
- **Floor Plan** — paradigm blueprint (Latin cross, Greek cross, open plan…)
- **Nave** — main central runtime chamber
- **Transepts** — ecosystem chambers (libraries, tools, runtimes)
- **Flying Buttresses** — type-system supports
- **Stained Glass** — syntax highlighting palette
- **Gargoyles** — footguns / sharp edges the cathedral warns against
- **Bell Tower** — concurrency rhythm & cadence
- **Rose Window** — central abstraction (the "core idea")
- **Vaulted Ceiling** — control flow architecture
- **Foundation** — VM / runtime substrate
- **Architect Lineage** — creator / maintainer history
- **Construction Era** — age & construction milestones
- **Pilgrimage Count** — adoption / visitors per year
- **Cathedral Tour** — visit all 8 cathedrals in rotation order
- **Side-By-Side Naves** — pairwise comparison of two cathedrals
- **Blueprint Snippet** — for a code snippet, which cathedral fits

## Usage

```bash
python -m polyglot_cathedral                       # report for current rotation language
python -m polyglot_cathedral TypeScript           # report for an explicit language
python -m polyglot_cathedral --test                # run self-tests
python -m polyglot_cathedral --tour                # tour all 8 cathedrals
python -m polyglot_cathedral --compare Rust Go     # side-by-side comparison
python -m polyglot_cathedral --current             # show current rotation language (no advance)
python -m polyglot_cathedral --snippet "code..."   # feed a snippet for snippet-homing
```

## Rotation

`Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust`

The module reads `language_rotation.json` at the workspace root, advances
the index by one when called without `--test` / `--tour` / `--compare` /
`--current`, and writes back the new state.

## Tests

Self-tests ship in `__init__.py` and are also wrapped for `pytest`:

```bash
python -m polyglot_cathedral --test    # internal runner
pytest polyglot_cathedral/tests/        # pytest discovery
```

## Distinct from existing tools

| Tool                  | Lens                              |
|-----------------------|-----------------------------------|
| polyglot_bloom        | gardening / phenology             |
| polyglot_loom         | weaving / textile arts            |
| polyglot_lighthouse   | maritime / pharos                 |
| polyglot_horology     | watchmaking / clockwork           |
| polyglot_reef         | marine ecosystem (organisms)      |
| polyglot_orbit        | celestial mechanics               |
| polyglot_vessel       | alchemical distillation           |
| polyglot_wire         | electrical FFI                    |
| polyglot_forge        | metalworking / smithing           |
| polyglot_pulse        | vital signs (medical)             |
| polyglot_mood         | emotional profiling               |
| polyglot_flavor       | sensory sommelier                 |
| **polyglot_cathedral**| **gothic architecture**           |

## Version

`polyglot-cathedral v1.0.0`