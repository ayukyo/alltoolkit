"""Polyglot Metamorphosis - AST-aware code transformation across languages."""

import json
import re
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    from rich.console import Console
    from rich.syntax import Syntax
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    Console = None


# Language metadata
LANGUAGE_TRAITS = {
    "Rust": {
        "paradigm": "systems/functional",
        "syntax": "fn name() { ... }",
        "entry": "fn main() { ... }",
        "fmt": "rustfmt",
        "paradigm_keywords": ["ownership", "borrowing", "lifetimes", "traits", "match", "Option<T>", "Result<T>"],
    },
    "Go": {
        "paradigm": "concurrent/imperative",
        "syntax": "func name() { ... }",
        "entry": "func main() { ... }",
        "fmt": "gofmt",
        "paradigm_keywords": ["goroutine", "channel", "defer", "interface{}", "go func()"],
    },
    "Swift": {
        "paradigm": "protocol-oriented/functional",
        "syntax": "func name() { ... }",
        "entry": "@main struct App { ... }",
        "fmt": "swiftformat",
        "paradigm_keywords": ["optional", "guard", "protocol", "extension", "struct", "enum", "nil_coalescing", "force_unwrap"],
    },
    "Kotlin": {
        "paradigm": "object-oriented/functional",
        "syntax": "fun name() { ... }",
        "entry": "fun main() { ... }",
        "fmt": "ktlint",
        "paradigm_keywords": ["data class", "sealed class", "coroutine", "extension", "safe_call", "elvis", "when"],
    },
    "TypeScript": {
        "paradigm": "typed/functional",
        "syntax": "function name(): Type { ... }",
        "entry": "// run: npx ts-node main.ts",
        "fmt": "prettier",
        "paradigm_keywords": ["interface", "type", "generic", "async_await", "unknown", "Partial<T>"],
    },
    "JavaScript": {
        "paradigm": "prototype-based/functional",
        "syntax": "function name() { ... }",
        "entry": "// run: node main.js",
        "fmt": "prettier",
        "paradigm_keywords": ["prototype", "closure", "callback", "Promise", "async_await", "destructuring"],
    },
    "Java": {
        "paradigm": "object-oriented",
        "syntax": "public void name() { ... }",
        "entry": "public class Main { public static void main(String[] args) { ... } }",
        "fmt": "google-java-format",
        "paradigm_keywords": ["class", "interface", "extends", "implements", "generic", "Stream<T>"],
    },
    "C/C++": {
        "paradigm": "procedural/systems",
        "syntax": "void name() { ... }",
        "entry": "int main(int argc, char* argv[]) { ... }",
        "fmt": "clang-format",
        "paradigm_keywords": ["pointer", "reference", "template", "STL", "const", "struct", "#include"],
    },
}

LANGUAGE_CYCLE = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]


# Rotation engine
def load_rotation_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation_config(config_path, data):
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def advance_rotation(config_path):
    """Read config, advance to next language, save, return result."""
    data = load_rotation_config(config_path)
    languages = data.get("languages", LANGUAGE_CYCLE)
    current = data.get("current_index", 0)
    prev_lang = languages[current]
    new_index = (current + 1) % len(languages)
    new_lang = languages[new_index]

    data["current_index"] = new_index
    data["last_language"] = new_lang
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation_config(config_path, data)

    return {
        "previous_language": prev_lang,
        "current_language": new_lang,
        "current_index": new_index,
    }


def get_current_language(config_path):
    """Return the language at current_index without advancing."""
    data = load_rotation_config(config_path)
    languages = data.get("languages", LANGUAGE_CYCLE)
    idx = data.get("current_index", 0)
    return languages[idx]


# Transformation engine
def detect_language(code):
    """Guess language from code patterns."""
    if re.search(r"\bfn\s+\w+\s*\(", code) and ("->" in code or "let mut" in code):
        return "Rust"
    if re.search(r"\bfunc\s+\w+\s*\(", code) and "package " in code:
        return "Go"
    if re.search(r"\bfunc\s+\w+\s*\(", code) and ("guard " in code or "struct " in code):
        return "Swift"
    if re.search(r"\bfun\s+\w+\s*\(", code) and ("val " in code or "var " in code):
        return "Kotlin"
    if re.search(r":\s*\w+\[\]|\binterface\s+\w+", code) or "export " in code:
        return "TypeScript"
    if re.search(r"\bfunction\s+\w+\s*\(", code) and ("console." in code or "module.exports" in code):
        return "JavaScript"
    if re.search(r"\bpublic\s+(static\s+)?void\s+main", code) or "System.out." in code:
        return "Java"
    if re.search(r"#include\s*<", code) or re.search(r"\bstd::", code):
        return "C/C++"
    return None


def extract_code_concepts(code, language):
    """Extract structural concepts from code."""
    concepts = {
        "functions": re.findall(
            r"(?:fn|func|fun|function|def|public\s+\w+\s+\w+)\s+(\w+)",
            code
        ),
        "variables": re.findall(
            r"(?:let\s+|var\s+|val\s+|const\s+|int\s+|string\s+|auto\s+)(\w+)",
            code
        ),
        "loops": bool(re.search(r"\b(for|while|loop)\s*\(", code)),
        "conditionals": bool(re.search(r"\b(if|when|switch|match)\s*\(", code)),
        "classes": re.findall(r"\b(struct|class|enum|interface|type)\s+(\w+)", code),
        "async": "async" in code or "await" in code or "go func" in code,
        "error_handling": bool(re.search(r"\b(try|catch|unwrap|panic|Result|Option|throws)\b", code)),
    }
    return concepts


def generate_metamorphic_mapping(source_lang, target_lang, concepts):
    """Generate concept-level mapping from source to target language."""
    fn_map = {
        "Rust": "fn {name}() { ... }",
        "Go": "func {name}() { ... }",
        "Swift": "func {name}() { ... }",
        "Kotlin": "fun {name}() { ... }",
        "TypeScript": "function {name}(): void { ... }",
        "JavaScript": "function {name}() { ... }",
        "Java": "public void {name}() { ... }",
        "C/C++": "void {name}() { ... }",
    }

    paradigm_shifts = []
    if source_lang in ("JavaScript", "TypeScript", "Java") and target_lang == "Rust":
        paradigm_shifts.append("Introduce ownership and borrowing model")
        paradigm_shifts.append("Replace classes with traits and impl blocks")
    if source_lang == "Rust" and target_lang in ("JavaScript", "Python"):
        paradigm_shifts.append("Drop explicit lifetimes - garbage collected")
        paradigm_shifts.append("Replace Result<T,E> with try/catch or .catch()")
    if source_lang in ("Java", "C/C++") and target_lang == "Go":
        paradigm_shifts.append("Replace inheritance with composition plus interfaces")
        paradigm_shifts.append("Simplify error handling - no exceptions")
    if source_lang == "Go" and target_lang == "Swift":
        paradigm_shifts.append("Convert goroutines to async/await with Task")
        paradigm_shifts.append("Replace channels with Combine or async sequences")

    mapping = {
        "source_language": source_lang,
        "target_language": target_lang,
        "source_traits": LANGUAGE_TRAITS.get(source_lang, {}),
        "target_traits": LANGUAGE_TRAITS.get(target_lang, {}),
        "function_skeleton": fn_map.get(target_lang, ""),
        "paradigm_shifts": paradigm_shifts,
        "extracted_concepts": concepts,
        "keywords_to_learn": [
            kw for kw in LANGUAGE_TRAITS.get(target_lang, {}).get("paradigm_keywords", [])
            if kw not in LANGUAGE_TRAITS.get(source_lang, {}).get("paradigm_keywords", [])
        ],
    }
    return mapping


def transform_example(source_lang, target_lang):
    """Generate a simple idiomatic example in target language."""
    templates = {
        ("JavaScript", "Rust"): """// JavaScript to Rust metamorphosis
// Source patterns: closure, callback, async/await

// JS: asynchronous with callbacks
async function fetchData(url) {
    const response = await fetch(url);
    return response.json();
}

// Rust equivalent (ownership-aware)
async fn fetch_data(url: &str) -> Result<serde_json::Value, reqwest::Error> {
    let response = reqwest::get(url).await?;
    let json: serde_json::Value = response.json().await?;
    Ok(json)
}
""",
        ("Rust", "JavaScript"): """// Rust to JavaScript metamorphosis
// Source patterns: ownership, Result<T,E>, Option<T>

// Rust: explicit error handling
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 { Err("Division by zero".to_string()) }
    else { Ok(a / b) }
}

// JS equivalent (exceptions plus optional chaining)
async function divide(a, b) {
    if (b === 0) throw new Error("Division by zero");
    return a / b;
}
""",
        ("Go", "Kotlin"): """// Go to Kotlin metamorphosis
// Source patterns: goroutine, channel, defer

// Go: concurrent with channels
func worker(jobs <-chan int, results chan<- int) {
    for j := range jobs {
        results <- j * 2
    }
}

// Kotlin equivalent (coroutines)
fun worker(jobs: ReceiveChannel<Int>, results: SendChannel<Int>) = GlobalScope.launch {
    for (j in jobs) {
        results.send(j * 2)
    }
}
""",
    }

    key = (source_lang, target_lang)
    if key in templates:
        return templates[key]

    tgt_trait = LANGUAGE_TRAITS.get(target_lang, {})
    return """// {src} to {tgt} metamorphosis
//
// Paradigm: {paradigm}
//
// Entry point:
// {entry}

// {syntax}
// See paradigm keywords: {keywords}
""".format(
        src=source_lang,
        tgt=target_lang,
        paradigm=tgt_trait.get("paradigm", "mixed"),
        entry=tgt_trait.get("entry", "// No standard entry"),
        syntax=tgt_trait.get("syntax", "// syntax varies"),
        keywords=", ".join(tgt_trait.get("paradigm_keywords", [])[:5]),
    )


# CLI
def cli():
    import argparse
    parser = argparse.ArgumentParser(description="Polyglot Metamorphosis")
    parser.add_argument("--config", default="language_rotation.json", help="Path to rotation config")
    parser.add_argument("--source", help="Source language (auto-detected if omitted)")
    parser.add_argument("--target", help="Target language (defaults to current rotated language)")
    parser.add_argument("--code", help="Source code to analyze")
    parser.add_argument("--example", action="store_true", help="Show metamorphic example")
    parser.add_argument("--traits", action="store_true", help="Show language traits for current rotation")
    args = parser.parse_args()

    config_path = Path(__file__).parent.parent.parent / args.config
    if not config_path.exists():
        config_path = Path("language_rotation.json")

    rotation = advance_rotation(str(config_path))
    current_lang = rotation["current_language"]

    console = Console() if HAS_RICH else None

    if args.traits:
        traits = LANGUAGE_TRAITS.get(current_lang, {})
        print("Language: {}".format(current_lang))
        print("Paradigm: {}".format(traits.get("paradigm", "unknown")))
        print("Syntax:   {}".format(traits.get("syntax", "unknown")))
        print("Formatter: {}".format(traits.get("fmt", "unknown")))
        print("Keywords: {}".format(", ".join(traits.get("paradigm_keywords", []))))
        return

    if args.example:
        source = args.source or detect_language(args.code or "") or "JavaScript"
        target = args.target or current_lang
        example = transform_example(source, target)
        print(example)
        return

    print("Previous: {}".format(rotation["previous_language"]))
    print("Current:  {}  [index={}]".format(current_lang, rotation["current_index"]))
    print("Updated:  {}".format(rotation.get("updated_at", "n/a")))

    if args.code:
        source = args.source or detect_language(args.code) or "Unknown"
        concepts = extract_code_concepts(args.code, source)
        mapping = generate_metamorphic_mapping(source, current_lang, concepts)
        print("\nSource: {}".format(source))
        print("Concepts: {}".format(concepts))
        print("Paradigm shifts: {}".format(mapping["paradigm_shifts"]))
        print("Target keywords to learn: {}".format(mapping["keywords_to_learn"]))


if __name__ == "__main__":
    cli()
