# ✉️ polyglot_correspondent v1.0.0

An **epistolary engine** for programming languages — every language is
a *pen pal* with a distinct letter-writing tradition, stationery, and
sense of formality.

## Concept

> "Every program is a letter. Every language signs its letters differently.
> Rust is a Swiss watchmaker — precision engraved on heavy parchment,
> signed with a wax seal of types. Go is a 1950s civil servant — typed
> on onionskin, signed in block letters, copied in triplicate. Swift
> is a Victorian gentleman-scholar — embossed on cream laid paper,
> signed with an italic nib, sealed in crimson wax. Java is a
> Victorian-era law firm — foolscap, three-carbon copy, embossed
> company seal, registered post. JavaScript is a Telegram —
> brief, dashed-off, no envelope. C is a chisel-stone inscription —
> no envelope at all, the wall is the letter."

Each language is examined as a correspondence tradition:

- ✉️ **Letterhead** — the file/module/namespace structure (the printed header)
- 📮 **Addressing** — imports, packages, modules, the addressing of the recipient
- 👋 **Salutation** — the opening (entry point, `main`, `init`)
- ✍️ **Quill** — the language's primary unit of expression (struct, class, function)
- 🕯️ **Wax Seal** — the type system (the embossed seal of authenticity)
- 💬 **Margin Notes** — comment culture and grammar (footnotes, marginalia)
- 📨 **Postscript** — `defer`, `finally`, `afterAll` (the P.S. after the letter body)
- 🖋️ **Valediction** — return / exit / close (the closing salutation)
- 👤 **Signature** — author identity, version, package metadata
- 📜 **Stationery** — file extension, encoding, source layout
- 🚚 **Postal Route** — package manager / module resolution / module system
- 🎭 **Epistolary Tone** — formal, terse, friendly, official

The tool reads `language_rotation.json`, picks the current rotation
language, and produces a **letter from that language to the developer** —
in that language's own voice, addressing the developer as that language
would.

Distinct from existing tools:

- **polyglot_oracle / polyglot_tarot** — mystical / divinatory reading
- **polyglot_echoes** — community quotes / battle cries
- **polyglot_horology** — watchmaking (time)
- **polyglot_architect** — architecture (buildings)
- **polyglot_signal** — error/absence/warning semantics
- **polyglot_loom** — weaving (textile arts)
- **polyglot_resonator** — mental models / frequency

`polyglot_correspondent` is uniquely about the *epistolary voice* — the
conventions of address, salutation, signature, postscript, stationery,
and the postal route. No other tool maps the letter-writing tradition
of programming languages.

## Features

- ✉️ **Letterhead Catalogue** — every language mapped to a letterhead style
- 📮 **Postal Route Mapping** — module system / package manager / resolution
- 👋 **Salutation Generator** — opens the letter in the language's voice
- 🕯️ **Wax Seal Identification** — type system as embossed seal
- 📨 **Postscript Detection** — finds defer/finally/afterAll patterns
- 🎭 **Tone Classification** — formal / terse / friendly / official
- ✍️ **Cross-Language Comparison** — how the same letter is signed differently
- 🔁 **Rotation Support** — automatically selects next language via `language_rotation.json`

## Installation

```bash
cd AllToolkit/polyglot_correspondent
python -m polyglot_correspondent --test     # run all tests
python -m polyglot_correspondent --report   # generate a letter from current language
```

## Rotation Order

`Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust`
