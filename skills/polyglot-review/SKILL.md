---
name: polyglot-review
description: Language-Aware Code Review Generator. Rotates through Rust→Go→Swift→Kotlin→TypeScript→JavaScript→Java→C/C++ delivering idiomatic code review feedback. Reads from language_rotation.json, advances the rotation, generates review topics/questions/checklists for the current language, then updates state. Use when user asks for a code review, wants feedback on their code, or requests language-specific review criteria.
---

# Polyglot Review

Generate idiomatic code review feedback that rotates through languages automatically.

## Rotation Order

**Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → (repeat)**

## Workflow

1. **Run the review engine**: `python3 ~/.openclaw/workspace/skills/polyglot-review/scripts/polyglot_review.py`
2. **Present**: Read the output — review topics, probing questions, and checklist for the current language
3. **Engage**: Apply the review criteria to the user's code; ask clarifying questions
4. **State**: The script auto-advances `current_index` and `last_language` in `language_rotation.json`

## Example Output

```
=== Polyglot Review (Rust) ===
📋 Code Review — Rust

### 🔍 Ownership & Borrowing
- Is every value owned by exactly one variable?
- Are borrows (&, &mut) used correctly?
...

### ✅ General Checklist
- [ ] No raw unwrap() on Result/Option in production paths
- [ ] Clippy warnings addressed (cargo clippy)
...
```

## Review Topics Per Language

Each language includes three themed topic sections (e.g., **Ownership & Borrowing** for Rust, **Error Handling** for Go, **Memory Safety** for Swift) plus a general checklist.

| Language | Topic 1 | Topic 2 | Topic 3 |
|----------|---------|---------|---------|
| Rust | Ownership & Borrowing | Error Handling | Performance |
| Go | Error Handling | Concurrency | Code Style |
| Swift | Memory Safety | API Design | Error Handling |
| Kotlin | Null Safety | Coroutines & Async | Pragmatic Style |
| TypeScript | Type Safety | Async Patterns | Module Quality |
| JavaScript | Async Discipline | Variable Practices | Modern Syntax |
| Java | Streams & Lambdas | Generics | OO & Design |
| C/C++ | Memory Safety | RAII & Resources | Templates & Generics |

## Running with Code Input

```bash
# Pass code via command line
python3 ~/.openclaw/workspace/skills/polyglot-review/scripts/polyglot_review.py "let x: string | null = null"

# Or pipe code in
echo "const x: string | null = null" | python3 ~/.openclaw/workspace/skills/polyglot-review/scripts/polyglot_review.py
```

## Design Philosophy

- Review criteria are **idiomatic** — specific to each language's paradigms and pitfalls
- Questions are **probing** — guide the reviewer to think critically, not just syntax-check
- The checklist is **actionable** — concrete items a reviewer can tick off
- Language rotation is **automatic** — every invocation advances the state

## Standalone Use

```bash
python3 ~/.openclaw/workspace/skills/polyglot-review/scripts/polyglot_review.py
```

The script reads `language_rotation.json`, advances to the next language, generates review criteria, and writes the updated state back.