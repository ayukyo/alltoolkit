# language_probe

**Parallel Multi-Language Runtime Environment Probe**

Probes all language runtimes in the rotation simultaneously, builds a capability matrix (availability, version, arch, concurrency model, memory model, package manager), and advances `language_rotation.json`.

## What it Does

1. Loads `language_rotation.json` (AllToolkit root) — reads current language
2. Probes all 8 language runtimes simultaneously:
   - **Rust** · `rustc --version`
   - **Go** · `go version`
   - **Swift** · `swift --version`
   - **Kotlin** · `kotlin -version`
   - **TypeScript** · `npx tsc --version`
   - **JavaScript** · `node --version`
   - **Java** · `java -version`
   - **C/C++** · `gcc --version`
3. For each probe, captures: version, arch (via `uname -m`), concurrency model, memory model, package manager
4. Displays a **capability matrix table** showing availability and scores
5. Advances `current_index` → 1 (next run selects **Go**), saves back to `language_rotation.json`

## Capability Matrix

Each language gets a **capability score 0–100** based on:
- Availability (20 pts)
- Version detected (15 pts)
- Architecture info (10 pts)
- Concurrency model (20 pts)
- Memory model (15 pts)
- Package manager (20 pts)

## Language Rotation Order

```
Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → (loop)
```

## Run

```bash
cargo run --release
# or
./target/release/language_probe
```

## Test Results

```
running 10 tests
test tests::test_advance_index              ... ok
test tests::test_availability_badge         ... ok
test tests::test_capability_score_available  ... ok
test tests::test_capability_score_unavailable ... ok
test tests::test_current_language           ... ok
test tests::test_load_rotation_state        ... ok
test tests::test_probe_summary_display      ... ok
test tests::test_rotation_state_roundtrip   ... ok
test tests::test_unknown_language_probe     ... ok
test tests::test_all_probe_commands_defined  ... ok

test result: ok. 10 passed; 0 failed
```

## Output Example

```
🌐 Language Runtime Probe — Capability Matrix
══════════════════════════════════════════════════════════════════════════════════════
│ Rust        │ ✅ Available │ x86_64  │ ✅ Threads + Send/Sync     │ Manual       │ cargo             │   100/100 │
│ Go          │ ✅ Available │ x86_64  │ ✅ Goroutines + Channels    │ GC           │ go mod            │   100/100 │
│ Swift       │ ❌ Unavailable │ -      │ -                          │ -            │ -                 │     0/100 │
│ Kotlin      │ ✅ Available │ x86_64  │ ✅ Coroutines + Flow        │ GC           │ Gradle / Maven    │   100/100 │
│ TypeScript  │ ✅ Available │ x86_64  │ ✅ async/await + Web Workers│ GC           │ npm / yarn / pnpm │   100/100 │
│ JavaScript  │ ✅ Available │ x86_64  │ ✅ async/await + Web Workers│ GC          │ npm / yarn / pnpm │   100/100 │
│ Java        │ ✅ Available │ x86_64  │ ✅ Threads + Virtual Threads│ GC           │ Maven / Gradle    │   100/100 │
│ C/C++       │ ✅ Available │ x86_64  │ ✅ Threads + C++20 Coroutines│ Manual      │ CMake / vcpkg     │   100/100 │
══════════════════════════════════════════════════════════════════════════════════════
  8 languages probed · 7 available · 1 unavailable · 523 ms elapsed
```

## Rotation State

Reads and writes `/home/admin/.openclaw/workspace/AllToolkit/language_rotation.json`:

```json
{
  "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
  "current_index": 1,    // ← next run selects Go (index 1)
  "last_language": "Rust",
  "updated_at": "..."
}
```

After each run, `current_index` is advanced (modulo 8). Next cron invocation will pick **Go**.
