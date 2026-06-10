---
name: polyglot-companion
description: Polyglot Programming Wisdom & Code Snippet Generator. Rotates through programming languages (Rust→Go→Swift→Kotlin→TypeScript→JavaScript→Java→C/C++) delivering philosophy and representative code for each. Triggers when user asks for language wisdom, code examples across languages, or a rotating programming challenge.
---

# Polyglot Companion

Deliver programming wisdom and idiomatic code snippets across the language rotation: **Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → (repeat)**

## Rotation Workflow

1. **Read state**: Load `~/.openclaw/workspace/language_rotation.json`
2. **Advance**: Move to next language in rotation order (not alphabetical), update `last_language` and `current_index`
3. **Deliver**: Output the language's philosophy + a representative code snippet
4. **Persist**: Write updated state back to `language_rotation.json`

## Run the Wisdom Engine

```bash
python3 ~/.openclaw/workspace/skills/polyglot-companion/scripts/polyglot_wisdom.py
```

## Language Wisdom Reference

| Language | Philosophy |
|----------|------------|
| Rust | Memory safety without GC; zero-cost abstractions |
| Go | Simplicity; concurrency built in via goroutines |
| Swift | Safe, fast, expressive; optionals for nil |
| Kotlin | Pragmatic elegance; coroutines for async |
| TypeScript | JS that scales; types catch bugs |
| JavaScript | Language of the web; async/await |
| Java | Write once, run anywhere; streams & generics |
| C/C++ | Maximum control; RAII and templates |

## Tips for Creative Use

- After delivering wisdom, suggest a small coding challenge in that language
- Connect the new language to the previous one ("Unlike Rust's borrow checker, Go uses...")  
- Each invocation automatically advances the rotation — don't hardcode languages
- The script handles the cycling; just call and deliver