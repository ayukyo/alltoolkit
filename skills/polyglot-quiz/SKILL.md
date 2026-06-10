---
name: polyglot-quiz
description: Interactive Programming Language Quiz Generator. Rotates through languages (Rust→Go→Swift→Kotlin→TypeScript→JavaScript→Java→C/C++) presenting quiz questions to test knowledge. Reads from language_rotation.json, advances the rotation, and updates state after each quiz. Use when user wants a programming challenge, language trivia, or to test their knowledge across the language rotation.
---

# Polyglot Quiz

Deliver interactive programming language quizzes that rotate through the language order automatically.

## Quiz Rotation Order

**Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → (repeat)**

## Workflow

1. **Run the quiz engine**: `python3 ~/.openclaw/workspace/skills/polyglot-quiz/scripts/polyglot_quiz.py`
2. **Present**: Read the output — language, question, hint, answer
3. **Engage**: Ask the user to answer, then reveal. Optionally offer a follow-up challenge in that language
4. **State**: The script auto-advances `current_index` and `last_language` in `language_rotation.json`

## Example Output

```
=== Polyglot Quiz (Rust) ===
Q: Rust's ownership system eliminates entire classes of bugs. What Rust feature ensures memory safety without a garbage collector?
Think: It involves `&` references and rules about who owns the data.
Answer: Ownership & Borrowing (or 'ownership' or 'borrow checker')
```

## Design Philosophy

- Each quiz question is a *conceptual* challenge, not a "write Hello World" task
- Questions test understanding of the language's unique design philosophy
- Hints guide without giving away the answer
- Questions cycle with the language — new language, new challenge

## Running Standalone

```bash
python3 ~/.openclaw/workspace/skills/polyglot-quiz/scripts/polyglot_quiz.py
```

The script reads `language_rotation.json`, advances to the next language in the rotation, generates a quiz, and writes the updated state back.