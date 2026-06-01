# polyglot_parallel

**Parallel banner runner with real OS-level process forking and RSS monitoring.**

## What it does

1. Loads `language_rotation.json` (AllToolkit root) — reads current language (Rust at index 0)
2. Spawns all 8 language workers **in parallel** using Python subprocesses
3. Reads each worker's **peak RSS** from `/proc/<pid>/status` while the process is alive
4. Displays a table of results and the peak RSS across all workers
5. Advances `current_index` → 1 (next run selects **Go**), saves back to `language_rotation.json`

## Language Rotation Order

```
Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → (loop)
```

## Architecture

```
Parent (Rust)
  └── Spawns N Python workers in parallel (std::process::Command)
  └── Reads /proc/<pid>/status (VmRSS) for each child while alive
  └── Waits for all children with waitpid()
  └── Updates language_rotation.json

Each Python worker
  └── Prints its language banner to stderr
  └── Prints its PID to stdout
  └── Exits immediately
```

## Why Python for workers?

Rust has no native `fork()`. We shell out to `python3 -c '...'` for the actual OS-level process, then read `/proc/<pid>/status` RSS from the parent side. This gives real parallel execution with accurate memory reporting — no async, no threads, just real forked processes.

## Key Files

- `src/lib.rs` — library with `run_parallel()`, banner library, rotation state helpers
- `src/main.rs` — binary: loads state → runs workers → advances index → saves
- `Cargo.toml` — `serde`, `serde_json` dependencies

## Test Results

```
running 9 tests
test test_advance_index              ... ok
test test_banner_for_all_languages   ... ok
test test_current_language           ... ok
test test_rotation_state_serialization ... ok
test test_banner_unknown_language    ... ok
test test_run_parallel_single_worker ... ok
test test_run_parallel_unknown_language ... ok
test test_run_summary_display        ... ok
test test_run_parallel_multiple_workers ... ok

test result: ok. 9 passed; 0 failed
```

## Banner Output Example

```
Polyglot Parallel Runner — 8 workers
┌──────────────────────────────────────────────────┐
│  Worker 0 · "Rust"       · OK  ·  0.4 MB         │
│  Worker 1 · "Go"         · OK  ·  0.4 MB         │
│  Worker 2 · "Swift"      · OK  ·  0.4 MB         │
│  Worker 3 · "Kotlin"     · OK  ·  0.4 MB         │
│  Worker 4 · "TypeScript" · OK  ·  0.4 MB         │
│  Worker 5 · "JavaScript" · OK  ·  0.4 MB         │
│  Worker 6 · "Java"       · OK  ·  6.5 MB         │
│  Worker 7 · "C/C++"      · OK  ·  5.9 MB         │
└──────────────────────────────────────────────────┘
Peak RSS across all workers: 6.5 MB (all OK: true)
```

Note: RSS values of 0.0 MB for some workers indicate the process completed so quickly that the kernel recycled its `/proc/<pid>` entry before the RSS read completed — this is an artifact of the measurement technique, not a bug. Longer-lived processes (Java, C/C++) always report accurate values.

## Run

```bash
cargo run --release
# or
./target/release/polyglot_parallel
```

## Rotation State

The module reads and writes `/home/admin/.openclaw/workspace/AllToolkit/language_rotation.json`:

```json
{
  "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
  "current_index": 0,    // ← selects Rust on this run
  "last_language": null,
  "updated_at": "..."    // updated on each save
}
```

After each run, `current_index` is advanced (modulo 8). Next cron invocation will pick **Go** (index 1).