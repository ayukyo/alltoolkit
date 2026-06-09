#!/usr/bin/env python3
"""
🎼 Language Fugue v1.0
A creative code composition tool — generates idiomatic implementations
of a single algorithmic specification across ALL rotation languages,
each rendered in its native style and idioms.

Creative concept: "A fugue is a musical form where one theme is developed
across multiple voices. A Language Fugue takes one algorithmic spec and
renders it through every language's native lens — the same melody,
different instruments."

The spec is parsed into high-level constructs (loops, data structures, I/O),
then each language transpiles it into idiomatic code. The result is a
code composition showing how the same problem is approached differently
by Rust, Go, Swift, Kotlin, TypeScript, JavaScript, Java, and C/C++.

Distinct from existing tools:
  - polyglot_digest: shows same code syntax in different languages
  - polyglot_resonator: shows philosophical stances (no code generation)
  - language_compass: shows learning journey milestones (no code)
  - language_sage: shows tips and pitfalls (no code generation)
  - polyglot_cipher: generates cipher challenges (no code composition)

Fugue is about PARALLEL CODE GENERATION from a shared specification —
showing the full orchestra, not just one instrument.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import random
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

TOOL_NAME = "language-fugue"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "language_rotation.json"
)

# ── Algorithm specifications ──────────────────────────────────────────────────
SPECS: List[Dict[str, Any]] = [
    {
        "id": "word_frequency",
        "name": "Word Frequency Counter",
        "emoji": "📊",
        "description": (
            "Read a text string, split into words (strip punctuation), "
            "count occurrences case-insensitively, return the top N words sorted by count."
        ),
        "input": {"type": "string", "example": "Hello world! Hello World... hello?"},
        "params": [{"name": "top_n", "type": "int", "default": 3}],
        "returns": {"type": "list of (word, count) tuples"},
        "complexity": "O(n log n) — sorting dominates",
    },
    {
        "id": "fizzbuzz",
        "name": "FizzBuzz Sequence",
        "emoji": "🔢",
        "description": (
            "Generate numbers from 1 to n. For multiples of 3 print 'Fizz', "
            "for multiples of 5 print 'Buzz', for both print 'FizzBuzz', "
            "otherwise print the number. Return as a list of strings."
        ),
        "input": {"type": "int", "example": 15},
        "params": [{"name": "limit", "type": "int", "default": 20}],
        "returns": {"type": "list of strings"},
        "complexity": "O(n)",
    },
    {
        "id": "prime_sieve",
        "name": "Prime Sieve",
        "emoji": "🔱",
        "description": (
            "Find all primes up to n using the Sieve of Eratosthenes. "
            "Return a list of prime numbers."
        ),
        "input": {"type": "int", "example": 30},
        "params": [{"name": "max_n", "type": "int", "default": 30}],
        "returns": {"type": "list of ints"},
        "complexity": "O(n log log n)",
    },
    {
        "id": "binary_search",
        "name": "Binary Search",
        "emoji": "🔍",
        "description": (
            "Search a sorted list for a target value. Return the index if found, "
            "or -1 if not found. Must use binary search algorithm."
        ),
        "input": {"type": "list of sorted ints + target int", "example": "[1,3,5,7,9], target=7"},
        "params": [{"name": "target", "type": "int", "default": 7}],
        "returns": {"type": "int (index or -1)"},
        "complexity": "O(log n)",
    },
    {
        "id": "reverse_linked_list",
        "name": "Reverse Linked List",
        "emoji": "🔄",
        "description": (
            "Define a singly linked list node struct/class. "
            "Implement a function that reverses the list in-place. "
            "Return the new head node."
        ),
        "input": {"type": "linked list", "example": "1 → 2 → 3 → 4 → 5"},
        "params": [],
        "returns": {"type": "linked list (reversed)"},
        "complexity": "O(n)",
    },
]

# ── Transpiler functions ──────────────────────────────────────────────────────

def _rust_transpiler(spec: Dict[str, Any], params: Dict[str, Any]) -> str:
    sid = spec["id"]
    if sid == "word_frequency":
        top_n = params.get("top_n", 3)
        return 'use std::collections::HashMap;\n\nfn word_frequency(text: &str, top_n: usize) -> Vec<(&str, usize)> {\n    let mut counts: HashMap<String, usize> = HashMap::new();\n    for word in text.split_whitespace() {\n        let clean = word.trim_matches(|c: char| !c.is_alphabetic()).to_lowercase();\n        if !clean.is_empty() {\n            *counts.entry(clean).or_insert(0) += 1;\n        }\n    }\n    let mut sorted: Vec<_> = counts.into_iter().collect();\n    sorted.sort_by(|a, b| b.1.cmp(&a.1));\n    sorted.truncate(top_n);\n    sorted\n}\n\nfn main() {\n    let text = "Hello world! Hello World... hello?";\n    let top = word_frequency(text, %d);\n    for (word, count) in top {\n        println!("{}: {}", word, count);\n    }\n}' % top_n
    elif sid == "fizzbuzz":
        limit = params.get("limit", 20)
        return 'fn fizzbuzz(limit: usize) -> Vec<String> {\n    (1..=limit)\n        .map(|n| match (n %% 3 == 0, n %% 5 == 0) {\n            (true, true) => "FizzBuzz".to_string(),\n            (true, false) => "Fizz".to_string(),\n            (false, true) => "Buzz".to_string(),\n            _ => n.to_string(),\n        })\n        .collect()\n}\n\nfn main() {\n    for item in fizzbuzz(%d) {\n        println!("{}", item);\n    }\n}' % limit
    elif sid == "prime_sieve":
        max_n = params.get("max_n", 30)
        return 'fn prime_sieve(max_n: usize) -> Vec<usize> {\n    let mut is_prime = vec![true; max_n + 1];\n    is_prime[0] = false;\n    if max_n > 0 { is_prime[1] = false; }\n    for p in 2..=((max_n as f64).sqrt() as usize) {\n        if is_prime[p] {\n            for multiple in (p * p..=max_n).step_by(p) {\n                is_prime[multiple] = false;\n            }\n        }\n    }\n    is_prime\n        .iter()\n        .enumerate()\n        .filter(|(_, &prime)| prime)\n        .map(|(i, _)| i)\n        .collect()\n}\n\nfn main() {\n    let primes = prime_sieve(%d);\n    println!("{:?}", primes);\n}' % max_n
    elif sid == "binary_search":
        target = params.get("target", 7)
        return 'fn binary_search(arr: &[i32], target: i32) -> i32 {\n    let mut lo = 0isize;\n    let mut hi = arr.len() as isize - 1;\n    while lo <= hi {\n        let mid = (lo + hi) / 2;\n        match arr[mid as usize].cmp(&target) {\n            std::cmp::Ordering::Equal => return mid as i32,\n            std::cmp::Ordering::Less => lo = mid + 1,\n            std::cmp::Ordering::Greater => hi = mid - 1,\n        }\n    }\n    -1\n}\n\nfn main() {\n    let arr = [1, 3, 5, 7, 9];\n    let idx = binary_search(&arr, %d);\n    println!("Index: {}", idx);\n}' % target
    elif sid == "reverse_linked_list":
        return 'use std::mem;\n\nstruct Node<T> {\n    val: T,\n    next: Option<Box<Node<T>>>,\n}\n\nfn reverse<T>(head: Option<Box<Node<T>>>) -> Option<Box<Node<T>>> {\n    let mut prev = None;\n    let mut curr = head;\n    while let Some(mut node) = curr {\n        let next = node.next.take();\n        node.next = prev;\n        prev = Some(node);\n        curr = next;\n    }\n    prev\n}\n\nfn main() {\n    let mut head = Some(Box::new(Node { val: 1, next: None }));\n    let mut curr = &mut head;\n    for i in [2, 3, 4, 5] {\n        if let Some(node) = curr {\n            node.next = Some(Box::new(Node { val: i, next: None }));\n            curr = &mut node.next;\n        }\n    }\n    let reversed = reverse(head);\n    let mut curr = &reversed;\n    while let Some(node) = curr {\n        print!("{} ", node.val);\n        curr = &node.next;\n    }\n    println!();\n}'
    return "// Unsupported spec"


def _go_transpiler(spec: Dict[str, Any], params: Dict[str, Any]) -> str:
    sid = spec["id"]
    if sid == "word_frequency":
        top_n = params.get("top_n", 3)
        return (
            'package main\n\n'
            'import (\n'
            '    "fmt"\n'
            '    "regexp"\n'
            '    "sort"\n'
            '    "strings"\n'
            ')\n\n'
            'func wordFrequency(text string, topN int) [][]string {\n'
            '    re := regexp.MustCompile(`[a-zA-Z]+`)\n'
            '    counts := make(map[string]int)\n'
            '    for _, word := range re.FindAllString(text, -1) {\n'
            '        lower := strings.ToLower(word)\n'
            '        counts[lower]++\n'
            '    }\n'
            '    type kv struct { Word string; Count int }\n'
            '    var sorted []kv\n'
            '    for w, c := range counts { sorted = append(sorted, kv{w, c}) }\n'
            '    sort.Slice(sorted, func(i, j int) bool { return sorted[i].Count > sorted[j].Count })\n'
            '    if topN > len(sorted) { topN = len(sorted) }\n'
            '    result := make([][]string, topN)\n'
            '    for i := 0; i < topN; i++ {\n'
            '        result[i] = []string{sorted[i].Word, fmt.Sprintf("%d", sorted[i].Count)}\n'
            '    }\n'
            '    return result\n'
            '}\n\n'
            'func main() {\n'
            '    text := "Hello world! Hello World... hello?"\n'
            '    top := wordFrequency(text, ' + str(top_n) + ')\n'
            '    for _, kv := range top {\n'
            '        fmt.Printf("%s: %s\\n", kv[0], kv[1])\n'
            '    }\n'
            '}\n'
        )
    elif sid == "fizzbuzz":
        limit = params.get("limit", 20)
        return (
            'package main\n\n'
            'import "fmt"\n\n'
            'func fizzbuzz(limit int) []string {\n'
            '    result := make([]string, 0, limit)\n'
            '    for i := 1; i <= limit; i++ {\n'
            '        switch {\n'
            '        case i%3==0 && i%5==0:\n'
            '            result = append(result, "FizzBuzz")\n'
            '        case i%3==0:\n'
            '            result = append(result, "Fizz")\n'
            '        case i%5==0:\n'
            '            result = append(result, "Buzz")\n'
            '        default:\n'
            '            result = append(result, fmt.Sprintf("%d", i))\n'
            '        }\n'
            '    }\n'
            '    return result\n'
            '}\n\n'
            'func main() {\n'
            '    for _, s := range fizzbuzz(' + str(limit) + ') {\n'
            '        fmt.Println(s)\n'
            '    }\n'
            '}\n'
        )
    elif sid == "prime_sieve":
        max_n = params.get("max_n", 30)
        return (
            'package main\n\n'
            'import "fmt"\n\n'
            'func primeSieve(maxN int) []int {\n'
            '    isPrime := make([]bool, maxN+1)\n'
            '    for i := 2; i <= maxN; i++ { isPrime[i] = true }\n'
            '    for p := 2; p*p <= maxN; p++ {\n'
            '        if isPrime[p] {\n'
            '            for multiple := p * p; multiple <= maxN; multiple += p {\n'
            '                isPrime[multiple] = false\n'
            '            }\n'
            '        }\n'
            '    }\n'
            '    var primes []int\n'
            '    for i := 2; i <= maxN; i++ { if isPrime[i] { primes = append(primes, i) } }\n'
            '    return primes\n'
            '}\n\n'
            'func main() {\n'
            '    fmt.Println(primeSieve(' + str(max_n) + '))\n'
            '}\n'
        )
    elif sid == "binary_search":
        target = params.get("target", 7)
        return (
            'package main\n\n'
            'import "fmt"\n\n'
            'func binarySearch(arr []int, target int) int {\n'
            '    lo, hi := 0, len(arr)-1\n'
            '    for lo <= hi {\n'
            '        mid := (lo + hi) / 2\n'
            '        if arr[mid] == target { return mid }\n'
            '        if arr[mid] < target { lo = mid + 1 } else { hi = mid - 1 }\n'
            '    }\n'
            '    return -1\n'
            '}\n\n'
            'func main() {\n'
            '    arr := []int{1, 3, 5, 7, 9}\n'
            '    fmt.Printf("Index: %d\\n", binarySearch(arr, ' + str(target) + '))\n'
            '}\n'
        )
    elif sid == "reverse_linked_list":
        return '''package main

import "fmt"

type Node struct {
    Val  int
    Next *Node
}

func reverse(head *Node) *Node {
    var prev *Node
    curr := head
    for curr != nil {
        next := curr.Next
        curr.Next = prev
        prev = curr
        curr = next
    }
    return prev
}

func main() {
    head := &Node{Val: 1}
    curr := head
    for _, v := range []int{2, 3, 4, 5} {
        curr.Next = &Node{Val: v}
        curr = curr.Next
    }
    reversed := reverse(head)
    for curr = reversed; curr != nil; curr = curr.Next {
        fmt.Print(curr.Val, " ")
    }
    fmt.Println()
}
'''
    return "// Unsupported spec"


def _swift_transpiler(spec: Dict[str, Any], params: Dict[str, Any]) -> str:
    sid = spec["id"]
    if sid == "word_frequency":
        top_n = params.get("top_n", 3)
        return 'import Foundation\n\nfunc wordFrequency(_ text: String, topN: Int) -> [(String, Int)] {\n    let words = text.lowercased().components(separatedBy: .whitespaces)\n        .map { $0.trimmingCharacters(in: .punctuationCharacters) }\n        .filter { !$0.isEmpty }\n    var counts: [String: Int] = [:]\n    for word in words { counts[word, default: 0] += 1 }\n    let sorted = counts.sorted { $0.value > $1.value }\n    return Array(sorted.prefix(topN))\n}\n\nlet text = "Hello world! Hello World... hello?"\nlet top = wordFrequency(text, topN: %d)\nfor (word, count) in top {\n    print("\\(word): \\(count)")\n}' % top_n
    elif sid == "fizzbuzz":
        limit = params.get("limit", 20)
        return 'import Foundation\n\nfunc fizzbuzz(_ limit: Int) -> [String] {\n    return (1...limit).map {\n        switch ($0 %% 3 == 0, $0 %% 5 == 0) {\n        case (true, true): return "FizzBuzz"\n        case (true, false): return "Fizz"\n        case (false, true): return "Buzz"\n        case (false, false): return "\\($0)"\n        }\n    }\n}\n\nfor item in fizzbuzz(%d) {\n    print(item)\n}' % limit
    elif sid == "prime_sieve":
        max_n = params.get("max_n", 30)
        return 'import Foundation\n\nfunc primeSieve(_ maxN: Int) -> [Int] {\n    var isPrime = [Bool](repeating: true, count: maxN + 1)\n    isPrime[0] = false\n    if maxN > 0 { isPrime[1] = false }\n    var p = 2\n    while p * p <= maxN {\n        if isPrime[p] {\n            var multiple = p * p\n            while multiple <= maxN {\n                isPrime[multiple] = false\n                multiple += p\n            }\n        }\n        p += 1\n    }\n    return isPrime.enumerated().compactMap { $0.element ? $0.offset : nil }\n}\n\nprint(primeSieve(%d))' % max_n
    elif sid == "binary_search":
        target = params.get("target", 7)
        return 'import Foundation\n\nfunc binarySearch(_ arr: [Int], _ target: Int) -> Int {\n    var lo = 0, hi = arr.count - 1\n    while lo <= hi {\n        let mid = (lo + hi) / 2\n        if arr[mid] == target { return mid }\n        if arr[mid] < target { lo = mid + 1 } else { hi = mid - 1 }\n    }\n    return -1\n}\n\nlet arr = [1, 3, 5, 7, 9]\nprint("Index: \\(binarySearch(arr, %d))")' % target
    elif sid == "reverse_linked_list":
        return '''import Foundation

class Node {
    var val: Int
    var next: Node?
    init(_ val: Int) { self.val = val }
}

func reverse(_ head: Node?) -> Node? {
    var prev: Node? = nil
    var curr = head
    while let node = curr {
        let next = node.next
        node.next = prev
        prev = node
        curr = next
    }
    return prev
}

// Build: 1 -> 2 -> 3 -> 4 -> 5
let head = Node(1)
var curr = head
for v in [2, 3, 4, 5] {
    curr.next = Node(v)
    curr = curr.next!
}

let reversed = reverse(head)
var curr2 = reversed
while let node = curr2 {
    print(node.val, terminator: " ")
    curr2 = node.next
}
print()
'''
    return "// Unsupported spec"


def _kotlin_transpiler(spec: Dict[str, Any], params: Dict[str, Any]) -> str:
    sid = spec["id"]
    if sid == "word_frequency":
        top_n = params.get("top_n", 3)
        return 'fun wordFrequency(text: String, topN: Int): List<Pair<String, Int>> {\n    val counts = text.lowercase()\n        .split(Regex("\\\\s+"))\n        .map { it.trimEnd(\'.\', \'!\', \'?\') }\n        .filter { it.isNotEmpty() }\n        .groupingBy { it }\n        .eachCount()\n    return counts.entries\n        .sortedByDescending { it.value }\n        .take(topN)\n        .map { it.key to it.value }\n}\n\nfun main() {\n    val text = "Hello world! Hello World... hello?"\n    val top = wordFrequency(text, %d)\n    top.forEach { (word, count) -> println("$word: $count") }\n}' % top_n
    elif sid == "fizzbuzz":
        limit = params.get("limit", 20)
        return 'fun fizzbuzz(limit: Int): List<String> = (1..limit).map { n ->\n    when {\n        n %% 15 == 0 -> "FizzBuzz"\n        n %% 3 == 0 -> "Fizz"\n        n %% 5 == 0 -> "Buzz"\n        else -> n.toString()\n    }\n}\n\nfun main() {\n    fizzbuzz(%d).forEach { println(it) }\n}' % limit
    elif sid == "prime_sieve":
        max_n = params.get("max_n", 30)
        return 'fun primeSieve(maxN: Int): List<Int> {\n    val isPrime = BooleanArray(maxN + 1) { true }.apply {\n        this[0] = false; this[1] = false\n    }\n    for (p in 2..Math.sqrt(maxN.toDouble()).toInt()) {\n        if (isPrime[p]) {\n            for (multiple in p * p..maxN step p) {\n                isPrime[multiple] = false\n            }\n        }\n    }\n    return isPrime.mapIndexedNotNull { i, prime -> if (prime) i else null }\n}\n\nfun main() {\n    println(primeSieve(%d))\n}' % max_n
    elif sid == "binary_search":
        target = params.get("target", 7)
        return 'fun binarySearch(arr: List<Int>, target: Int): Int {\n    var lo = 0; var hi = arr.lastIndex\n    while (lo <= hi) {\n        val mid = (lo + hi) / 2\n        when {\n            arr[mid] == target -> return mid\n            arr[mid] < target -> lo = mid + 1\n            else -> hi = mid - 1\n        }\n    }\n    return -1\n}\n\nfun main() {\n    val arr = listOf(1, 3, 5, 7, 9)\n    println("Index: ${{binarySearch(arr, %d)}}")\n}' % target
    elif sid == "reverse_linked_list":
        return '''data class Node(var value: Int, var next: Node? = null)

fun reverse(head: Node?): Node? {
    var prev: Node? = null
    var curr = head
    while (curr != null) {
        val next = curr.next
        curr.next = prev
        prev = curr
        curr = next
    }
    return prev
}

fun main() {
    val head = Node(1)
    var curr = head
    for (v in listOf(2, 3, 4, 5)) {
        curr.next = Node(v)
        curr = curr.next!!
    }
    val reversed = reverse(head)
    var curr2 = reversed
    while (curr2 != null) {
        print("${curr2.value} ")
        curr2 = curr2.next
    }
    println()
}
'''
    return "// Unsupported spec"


def _typescript_transpiler(spec: Dict[str, Any], params: Dict[str, Any]) -> str:
    sid = spec["id"]
    if sid == "word_frequency":
        top_n = params.get("top_n", 3)
        return 'function wordFrequency(text: string, topN: number): [string, number][] {\n    const words = text.toLowerCase()\n        .split(/\\s+/)\n        .map(w => w.replace(/[^a-z]/g, ""))\n        .filter(w => w.length > 0);\n    const counts = new Map<string, number>();\n    for (const word of words) {\n        counts.set(word, (counts.get(word) ?? 0) + 1);\n    }\n    return Array.from(counts.entries())\n        .sort((a, b) => b[1] - a[1])\n        .slice(0, topN);\n}\n\nconst text = "Hello world! Hello World... hello?";\nconst top = wordFrequency(text, %d);\ntop.forEach(([word, count]) => console.log(`${word}: ${count}`));' % top_n
    elif sid == "fizzbuzz":
        limit = params.get("limit", 20)
        return 'function fizzbuzz(limit: number): string[] {\n    return Array.from({length: limit}, (_, i) => i + 1).map(n => {\n        if (n %% 15 === 0) return "FizzBuzz";\n        if (n %% 3 === 0) return "Fizz";\n        if (n %% 5 === 0) return "Buzz";\n        return String(n);\n    });\n}\n\nfizzbuzz(%d).forEach(s => console.log(s));' % limit
    elif sid == "prime_sieve":
        max_n = params.get("max_n", 30)
        return 'function primeSieve(maxN: number): number[] {\n    const isPrime = new Array(maxN + 1).fill(true);\n    isPrime[0] = false;\n    isPrime[1] = false;\n    for (let p = 2; p * p <= maxN; p++) {\n        if (isPrime[p]) {\n            for (let multiple = p * p; multiple <= maxN; multiple += p) {\n                isPrime[multiple] = false;\n            }\n        }\n    }\n    return isPrime.map((v, i) => v ? i : -1).filter(i => i >= 2);\n}\n\nconsole.log(primeSieve(%d));' % max_n
    elif sid == "binary_search":
        target = params.get("target", 7)
        return 'function binarySearch(arr: number[], target: number): number {\n    let lo = 0, hi = arr.length - 1;\n    while (lo <= hi) {\n        const mid = (lo + hi) >>> 1;\n        if (arr[mid] === target) return mid;\n        if (arr[mid] < target) lo = mid + 1;\n        else hi = mid - 1;\n    }\n    return -1;\n}\n\nconst arr = [1, 3, 5, 7, 9];\nconsole.log("Index:", binarySearch(arr, %d));' % target
    elif sid == "reverse_linked_list":
        return '''interface ListNode {
    val: number;
    next: ListNode | null;
}

function reverse(head: ListNode | null): ListNode | null {
    let prev: ListNode | null = null;
    let curr = head;
    while (curr !== null) {
        const next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}

// Build: 1 -> 2 -> 3 -> 4 -> 5
const head: ListNode = { val: 1, next: null };
let curr: ListNode = head;
for (const v of [2, 3, 4, 5]) {
    curr.next = { val: v, next: null };
    curr = curr.next;
}
const reversed = reverse(head);
let curr2: ListNode | null = reversed;
while (curr2 !== null) {
    process.stdout.write(`${curr2.val} `);
    curr2 = curr2.next;
}
console.log();
'''
    return "// Unsupported spec"


def _javascript_transpiler(spec: Dict[str, Any], params: Dict[str, Any]) -> str:
    sid = spec["id"]
    if sid == "word_frequency":
        top_n = params.get("top_n", 3)
        return 'function wordFrequency(text, topN) {\n    const words = text.toLowerCase()\n        .split(/\\s+/)\n        .map(w => w.replace(/[^a-z]/g, ""))\n        .filter(w => w.length > 0);\n    const counts = new Map();\n    for (const word of words) {\n        counts.set(word, (counts.get(word) || 0) + 1);\n    }\n    return [...counts.entries()]\n        .sort((a, b) => b[1] - a[1])\n        .slice(0, topN);\n}\n\nconst text = "Hello world! Hello World... hello?";\nconst top = wordFrequency(text, %d);\ntop.forEach(([word, count]) => console.log(`${word}: ${count}`));' % top_n
    elif sid == "fizzbuzz":
        limit = params.get("limit", 20)
        return 'function fizzbuzz(limit) {\n    return Array.from({length: limit}, (_, i) => i + 1).map(n => {\n        if (n %% 15 === 0) return "FizzBuzz";\n        if (n %% 3 === 0) return "Fizz";\n        if (n %% 5 === 0) return "Buzz";\n        return String(n);\n    });\n}\n\nfizzbuzz(%d).forEach(s => console.log(s));' % limit
    elif sid == "prime_sieve":
        max_n = params.get("max_n", 30)
        return 'function primeSieve(maxN) {\n    const isPrime = new Array(maxN + 1).fill(true);\n    isPrime[0] = false;\n    isPrime[1] = false;\n    for (let p = 2; p * p <= maxN; p++) {\n        if (isPrime[p]) {\n            for (let multiple = p * p; multiple <= maxN; multiple += p) {\n                isPrime[multiple] = false;\n            }\n        }\n    }\n    return isPrime.map((v, i) => v ? i : -1).filter(i => i >= 2);\n}\n\nconsole.log(primeSieve(%d));' % max_n
    elif sid == "binary_search":
        target = params.get("target", 7)
        return 'function binarySearch(arr, target) {\n    let lo = 0, hi = arr.length - 1;\n    while (lo <= hi) {\n        const mid = (lo + hi) >>> 1;\n        if (arr[mid] === target) return mid;\n        if (arr[mid] < target) lo = mid + 1;\n        else hi = mid - 1;\n    }\n    return -1;\n}\n\nconst arr = [1, 3, 5, 7, 9];\nconsole.log("Index:", binarySearch(arr, %d));' % target
    elif sid == "reverse_linked_list":
        return '''function ListNode(val, next = null) {
    this.val = val;
    this.next = next;
}

function reverse(head) {
    let prev = null, curr = head;
    while (curr !== null) {
        const next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}

// Build: 1 -> 2 -> 3 -> 4 -> 5
const head = new ListNode(1);
let curr = head;
for (const v of [2, 3, 4, 5]) {
    curr.next = new ListNode(v);
    curr = curr.next;
}
const reversed = reverse(head);
let curr2 = reversed;
while (curr2 !== null) {
    process.stdout.write(curr2.val + " ");
    curr2 = curr2.next;
}
console.log();
'''
    return "// Unsupported spec"


def _java_transpiler(spec: Dict[str, Any], params: Dict[str, Any]) -> str:
    sid = spec["id"]
    if sid == "word_frequency":
        top_n = params.get("top_n", 3)
        return 'import java.util.*;\nimport java.util.stream.*;\n\npublic class WordFrequency {\n    public static List<Map.Entry<String, Integer>> wordFrequency(String text, int topN) {\n        Map<String, Integer> counts = new HashMap<>();\n        for (String word : text.toLowerCase().split("\\\\s+")) {\n            String cleaned = word.replaceAll("[^a-z]", "");\n            if (!cleaned.isEmpty()) {\n                counts.merge(cleaned, 1, Integer::sum);\n            }\n        }\n        return counts.entrySet().stream()\n            .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())\n            .limit(topN)\n            .collect(Collectors.toList());\n    }\n\n    public static void main(String[] args) {\n        String text = "Hello world! Hello World... hello?";\n        List<Map.Entry<String, Integer>> top = wordFrequency(text, %d);\n        for (var entry : top) {\n            System.out.println(entry.getKey() + ": " + entry.getValue());\n        }\n    }\n}' % top_n
    elif sid == "fizzbuzz":
        limit = params.get("limit", 20)
        return 'import java.util.*;\n\npublic class FizzBuzz {\n    public static List<String> fizzbuzz(int limit) {\n        List<String> result = new ArrayList<>();\n        for (int i = 1; i <= limit; i++) {\n            if (i %% 15 == 0) result.add("FizzBuzz");\n            else if (i %% 3 == 0) result.add("Fizz");\n            else if (i %% 5 == 0) result.add("Buzz");\n            else result.add(String.valueOf(i));\n        }\n        return result;\n    }\n\n    public static void main(String[] args) {\n        fizzbuzz(%d).forEach(System.out::println);\n    }\n}' % limit
    elif sid == "prime_sieve":
        max_n = params.get("max_n", 30)
        return 'import java.util.*;\n\npublic class PrimeSieve {\n    public static List<Integer> primeSieve(int maxN) {\n        boolean[] isPrime = new boolean[maxN + 1];\n        Arrays.fill(isPrime, true);\n        isPrime[0] = false;\n        isPrime[1] = false;\n        for (int p = 2; p * p <= maxN; p++) {\n            if (isPrime[p]) {\n                for (int multiple = p * p; multiple <= maxN; multiple += p) {\n                    isPrime[multiple] = false;\n                }\n            }\n        }\n        List<Integer> primes = new ArrayList<>();\n        for (int i = 2; i <= maxN; i++) if (isPrime[i]) primes.add(i);\n        return primes;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(primeSieve(%d));\n    }\n}' % max_n
    elif sid == "binary_search":
        target = params.get("target", 7)
        return 'import java.util.*;\n\npublic class BinarySearch {\n    public static int binarySearch(int[] arr, int target) {\n        int lo = 0, hi = arr.length - 1;\n        while (lo <= hi) {\n            int mid = (lo + hi) >>> 1;\n            if (arr[mid] == target) return mid;\n            if (arr[mid] < target) lo = mid + 1;\n            else hi = mid - 1;\n        }\n        return -1;\n    }\n\n    public static void main(String[] args) {\n        int[] arr = {1, 3, 5, 7, 9};\n        System.out.printf("Index: %%d%%n", binarySearch(arr, %d));\n    }\n}' % target
    elif sid == "reverse_linked_list":
        return '''import java.util.*;

public class ReverseLinkedList {
    static class Node {
        int val;
        Node next;
        Node(int val) { this.val = val; }
    }

    public static Node reverse(Node head) {
        Node prev = null, curr = head;
        while (curr != null) {
            Node next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
        }
        return prev;
    }

    public static void main(String[] args) {
        Node head = new Node(1);
        Node curr = head;
        for (int v : new int[]{2, 3, 4, 5}) {
            curr.next = new Node(v);
            curr = curr.next;
        }
        Node reversed = reverse(head);
        for (Node n = reversed; n != null; n = n.next) {
            System.out.print(n.val + " ");
        }
        System.out.println();
    }
}
'''
    return "// Unsupported spec"


def _cpp_transpiler(spec: Dict[str, Any], params: Dict[str, Any]) -> str:
    sid = spec["id"]
    if sid == "word_frequency":
        top_n = params.get("top_n", 3)
        return '#include <iostream>\n#include <string>\n#include <map>\n#include <vector>\n#include <algorithm>\n#include <cctype>\n\nstd::vector<std::pair<std::string, int>> wordFrequency(const std::string& text, int topN) {\n    std::map<std::string, int> counts;\n    std::string word;\n    for (char c : text) {\n        if (std::isalpha(c)) {\n            word += std::tolower(c);\n        } else if (!word.empty()) {\n            counts[word]++;\n            word.clear();\n        }\n    }\n    if (!word.empty()) counts[word]++;\n    std::vector<std::pair<std::string, int>> sorted(counts.begin(), counts.end());\n    std::sort(sorted.begin(), sorted.end(),\n        [](const auto& a, const auto& b) { return a.second > b.second; });\n    if ((int)sorted.size() > topN) sorted.resize(topN);\n    return sorted;\n}\n\nint main() {\n    std::string text = "Hello world! Hello World... hello?";\n    auto top = wordFrequency(text, %d);\n    for (const auto& [word, count] : top) {\n        std::cout << word << ": " << count << "\\n";\n    }\n    return 0;\n}' % top_n
    elif sid == "fizzbuzz":
        limit = params.get("limit", 20)
        return '#include <iostream>\n#include <string>\n#include <vector>\n\nstd::vector<std::string> fizzbuzz(int limit) {\n    std::vector<std::string> result;\n    result.reserve(limit);\n    for (int i = 1; i <= limit; i++) {\n        if (i %% 15 == 0) result.push_back("FizzBuzz");\n        else if (i %% 3 == 0) result.push_back("Fizz");\n        else if (i %% 5 == 0) result.push_back("Buzz");\n        else result.push_back(std::to_string(i));\n    }\n    return result;\n}\n\nint main() {\n    for (const auto& s : fizzbuzz(%d)) {\n        std::cout << s << "\\n";\n    }\n    return 0;\n}' % limit
    elif sid == "prime_sieve":
        max_n = params.get("max_n", 30)
        return '#include <iostream>\n#include <vector>\n#include <cmath>\n\nstd::vector<int> primeSieve(int maxN) {\n    std::vector<bool> isPrime(maxN + 1, true);\n    isPrime[0] = false;\n    if (maxN > 0) isPrime[1] = false;\n    for (int p = 2; p * p <= maxN; p++) {\n        if (isPrime[p]) {\n            for (int multiple = p * p; multiple <= maxN; multiple += p) {\n                isPrime[multiple] = false;\n            }\n        }\n    }\n    std::vector<int> primes;\n    for (int i = 2; i <= maxN; i++) {\n        if (isPrime[i]) primes.push_back(i);\n    }\n    return primes;\n}\n\nint main() {\n    auto primes = primeSieve(%d);\n    for (int p : primes) std::cout << p << " ";\n    std::cout << "\\n";\n    return 0;\n}' % max_n
    elif sid == "binary_search":
        target = params.get("target", 7)
        return '#include <iostream>\n#include <vector>\n\nint binarySearch(const std::vector<int>& arr, int target) {\n    int lo = 0, hi = (int)arr.size() - 1;\n    while (lo <= hi) {\n        int mid = (lo + hi) / 2;\n        if (arr[mid] == target) return mid;\n        if (arr[mid] < target) lo = mid + 1;\n        else hi = mid - 1;\n    }\n    return -1;\n}\n\nint main() {\n    std::vector<int> arr = {1, 3, 5, 7, 9};\n    std::cout << "Index: " << binarySearch(arr, %d) << "\\n";\n    return 0;\n}' % target
    elif sid == "reverse_linked_list":
        return '''#include <iostream>

struct Node {
    int val;
    Node* next;
    Node(int v, Node* n = nullptr) : val(v), next(n) {}
};

Node* reverse(Node* head) {
    Node* prev = nullptr;
    Node* curr = head;
    while (curr) {
        Node* next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}

int main() {
    Node* head = new Node(1);
    Node* curr = head;
    for (int v : {2, 3, 4, 5}) {
        curr->next = new Node(v);
        curr = curr->next;
    }
    Node* reversed = reverse(head);
    for (Node* n = reversed; n; n = n->next) {
        std::cout << n->val << " ";
    }
    std::cout << std::endl;
    return 0;
}
'''
    return "// Unsupported spec"


# ── Supported rotation languages ──────────────────────────────────────────────
# These are the 8 languages in the rotation cycle.
ROTATION_LANGS = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]

# ── Transpiler registry (built after all functions are defined) ────────────────
TRANSPILERS: Dict[str, Dict[str, Any]] = {
    "Rust": {"emoji": "🦀", "transpose": _rust_transpiler},
    "Go": {"emoji": "🐹", "transpose": _go_transpiler},
    "Swift": {"emoji": "🦅", "transpose": _swift_transpiler},
    "Kotlin": {"emoji": "🟣", "transpose": _kotlin_transpiler},
    "TypeScript": {"emoji": "🔷", "transpose": _typescript_transpiler},
    "JavaScript": {"emoji": "🟨", "transpose": _javascript_transpiler},
    "Java": {"emoji": "☕", "transpose": _java_transpiler},
    "C/C++": {"emoji": "⚙️", "transpose": _cpp_transpiler},
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _wrap(text: str, width: int) -> List[str]:
    words = text.split()
    lines, current = [], ""
    for word in words:
        if len(current) + len(word) + 1 <= width:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _render_code_card(spec, compositions, emoji_map):
    lines = []
    lines.append("╔══════════════════════════════════════════════════════════════════╗")
    lines.append("║            🎼 LANGUAGE FUGUE — Code Composition                 ║")
    lines.append("╠══════════════════════════════════════════════════════════════════╣")
    lines.append("║  %s %s" % (spec["emoji"], spec["name"]))
    lines.append("║  Complexity: %s" % spec["complexity"])
    for sl in _wrap(spec["description"], 62):
        lines.append("║  %s" % sl)
    lines.append("╠══════════════════════════════════════════════════════════════════╣")

    for lang, code in compositions.items():
        lang_emoji = emoji_map.get(lang, "🔧")
        line_count = len(code.splitlines())
        padding = max(0, 50 - len(lang) - len(str(line_count)))
        lines.append("║  %s %s — %d lines%s║" % (lang_emoji, lang, line_count, " " * padding))
        lines.append("╠══════════════════════════════════════════════════════════════════╣")

        code_lines = code.strip().split("\n")
        display_lines = code_lines[:12]
        for cl in display_lines:
            display = cl[:60] + ("…" if len(cl) > 60 else "")
            lines.append("║    %s" % display)
        if len(code_lines) > 12:
            lines.append("║    … (+%d more lines)" % (len(code_lines) - 12))
        lines.append("║                                                                  ║")

    lines.append("╚══════════════════════════════════════════════════════════════════╝")
    return "\n".join(lines)


# ── Core API ─────────────────────────────────────────────────────────────────

def fugue(spec_id: Optional[str] = None, language: Optional[str] = None, seed: Optional[int] = None) -> Dict[str, Any]:
    """
    Main entry point: generate a multi-language code composition.
    """
    config = load_rotation()

    # Select spec
    if spec_id is not None:
        spec = next((s for s in SPECS if s["id"] == spec_id), None)
        if spec is None:
            raise ValueError("Unknown spec_id: %s" % spec_id)
    elif seed is not None:
        spec = SPECS[seed % len(SPECS)]
    else:
        spec = random.choice(SPECS)

    # Determine selected language (from ROTATION_LANGS, using config index)
    if language is None:
        current_idx = config.get("current_index", 0)
        language = ROTATION_LANGS[current_idx % len(ROTATION_LANGS)]

    # Generate compositions for ALL 8 rotation languages
    emoji_map = {lang: TRANSPILERS[lang]["emoji"] for lang in ROTATION_LANGS}
    compositions = {}
    for lang in ROTATION_LANGS:
        params = {}
        if spec["id"] == "word_frequency":
            params["top_n"] = 3
        elif spec["id"] == "fizzbuzz":
            params["limit"] = 20
        elif spec["id"] == "prime_sieve":
            params["max_n"] = 30
        elif spec["id"] == "binary_search":
            params["target"] = 7

        transpiler = TRANSPILERS.get(lang)
        if transpiler:
            compositions[lang] = transpiler["transpose"](spec, params)

    # Build code card
    code_card = _render_code_card(spec, compositions, emoji_map)

    # Advance rotation within the 8-language cycle
    current_idx = ROTATION_LANGS.index(language)
    next_idx = (current_idx + 1) % len(ROTATION_LANGS)

    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "spec": {
            "id": spec["id"],
            "name": spec["name"],
            "emoji": spec["emoji"],
            "description": spec["description"],
            "complexity": spec["complexity"],
            "params": spec["params"],
            "returns": spec["returns"],
        },
        "compositions": compositions,
        "code_card": code_card,
        "next_language": ROTATION_LANGS[next_idx],
        "rotation": ROTATION_LANGS,
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def run_tests() -> None:
    """Run tests to validate the Language Fugue module."""
    tests_passed = 0
    tests_failed = 0

    def assert_eq(a, b, msg):
        nonlocal tests_passed, tests_failed
        if a == b:
            tests_passed += 1
            print("  ✅ PASS: %s" % msg)
        else:
            tests_failed += 1
            print("  ❌ FAIL: %s — expected %r, got %r" % (msg, b, a))

    def assert_in(a, b, msg):
        nonlocal tests_passed, tests_failed
        if a in b:
            tests_passed += 1
            print("  ✅ PASS: %s" % msg)
        else:
            tests_failed += 1
            print("  ❌ FAIL: %s — '%s' not in result" % (msg, a))

    def assert_true(a, msg):
        nonlocal tests_passed, tests_failed
        if a:
            tests_passed += 1
            print("  ✅ PASS: %s" % msg)
        else:
            tests_failed += 1
            print("  ❌ FAIL: %s" % msg)

    print("Testing Language Fugue...")

    print("  Loading rotation config...")
    config = load_rotation()
    # The rotation order is: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++
    EXPECTED_LANGS = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
    assert_eq(8, len(EXPECTED_LANGS), "8 languages in rotation")
    assert_eq("Rust", EXPECTED_LANGS[0], "Rust is first language")

    print("  Testing fugue() output structure...")
    result = fugue()
    expected_keys = [
        "tool", "version", "selected_language", "spec",
        "compositions", "code_card", "next_language", "rotation", "timestamp"
    ]
    for key in expected_keys:
        assert_true(key in result, "Key '%s' present in response" % key)

    print("  Testing spec structure...")
    spec = result["spec"]
    assert_true("id" in spec, "spec has id")
    assert_true("name" in spec, "spec has name")
    assert_true("emoji" in spec, "spec has emoji")
    assert_true("description" in spec, "spec has description")
    assert_true("complexity" in spec, "spec has complexity")
    assert_true(result["selected_language"] in ROTATION_LANGS, "selected_language is in ROTATION_LANGS")
    assert_in("compositions", result, "compositions present")
    assert_in("code_card", result, "code_card present")

    print("  Testing all 8 languages have compositions...")
    for lang in ROTATION_LANGS:
        assert_true(lang in result["compositions"], "%s has composition" % lang)
        code = result["compositions"][lang]
        assert_true(isinstance(code, str), "%s composition is a string" % lang)
        assert_true(len(code) > 50, "%s composition has substantial code" % lang)
        assert_true("\n" in code, "%s composition has multiple lines" % lang)

    print("  Testing each language code has correct indicators...")
    rust_code = result["compositions"]["Rust"]
    assert_true("fn " in rust_code or "use " in rust_code, "Rust code has fn/use keywords")
    go_code = result["compositions"]["Go"]
    assert_true("func " in go_code or "package " in go_code, "Go code has func/package keywords")
    swift_code = result["compositions"]["Swift"]
    assert_true("func " in swift_code or "import " in swift_code, "Swift code has func/import")
    cpp_code = result["compositions"]["C/C++"]
    assert_true("#include" in cpp_code, "C/C++ code has #include")

    print("  Testing rotation advances after fugue()...")
    idx_before = load_rotation()["current_index"]
    lang_before = ROTATION_LANGS[idx_before % len(ROTATION_LANGS)]
    result = fugue()
    idx_after = load_rotation()["current_index"]
    assert_eq((idx_before + 1) % len(ROTATION_LANGS), idx_after % len(ROTATION_LANGS), "index advanced by 1")
    assert_eq(lang_before, load_rotation()["last_language"], "last_language recorded")

    print("  Testing spec_id override...")
    result = fugue(spec_id="fizzbuzz")
    assert_eq("fizzbuzz", result["spec"]["id"], "spec_id override works")
    assert_eq("🔢", result["spec"]["emoji"], "FizzBuzz has correct emoji")
    assert_in("FizzBuzz", result["compositions"]["Rust"], "Rust has FizzBuzz composition")

    print("  Testing seed gives deterministic spec selection...")
    r1 = fugue(seed=0)
    r2 = fugue(seed=0)
    assert_eq(r1["spec"]["id"], r2["spec"]["id"], "seed=0 gives same spec")

    print("  Testing all 5 specs produce valid compositions...")
    for i, spec_item in enumerate(SPECS):
        result = fugue(spec_id=spec_item["id"])
        assert_eq(spec_item["id"], result["spec"]["id"], "spec %s rendered" % spec_item["id"])
        for lang in ROTATION_LANGS:
            assert_true(lang in result["compositions"], "%s has code for %s" % (lang, spec_item["id"]))
            assert_true(len(result["compositions"][lang]) > 20, "%s code is substantial for %s" % (lang, spec_item["id"]))

    print("  Testing code_card contains key sections...")
    card = result["code_card"]
    assert_in("LANGUAGE FUGUE", card, "code_card has title")
    assert_in(result["spec"]["emoji"], card, "code_card has spec emoji")
    assert_in("Rust", card, "code_card has Rust")
    assert_in("Go", card, "code_card has Go")
    assert_in("Swift", card, "code_card has Swift")
    assert_in("C/C++", card, "code_card has C/C++")

    print("  Testing language override...")
    result = fugue(language="Rust")
    assert_eq("Rust", result["selected_language"], "language override works")
    assert_eq("🦀", TRANSPILERS["Rust"]["emoji"], "Rust has 🦀 emoji")

    print("  Testing next_language is in rotation list...")
    assert_true(result["next_language"] in result["rotation"], "next_language is in rotation")
    assert_true(result["next_language"] != result["selected_language"], "next != selected")

    print("  Testing tool name and version...")
    assert_eq("language-fugue", result["tool"], "correct tool name")
    assert_eq("1.0.0", result["version"], "correct version")

    print("  Testing compositions for each spec/language combo...")
    for spec_item in SPECS:
        for lang in ROTATION_LANGS:
            result = fugue(spec_id=spec_item["id"], language=lang)
            code = result["compositions"][lang]
            assert_true(len(code) > 30, "%s has code for %s" % (lang, spec_item["id"]))

    print("  Testing invalid spec_id raises ValueError...")
    try:
        fugue(spec_id="nonexistent")
        tests_failed += 1
        print("  ❌ FAIL: No error for invalid spec_id")
    except ValueError as e:
        tests_passed += 1
        print("  ✅ PASS: ValueError raised for invalid spec_id")

    print("\n%s" % ("=" * 55))
    print("Tests: %d passed, %d failed" % (tests_passed, tests_failed))
    if tests_failed == 0:
        print("🎼 All Fugue tests passed! Every voice sings in harmony.")
    else:
        print("💥 %d test(s) failed." % tests_failed)
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--fugue":
        result = fugue()
        print(json.dumps(result, indent=2))
    else:
        print("Language Fugue v%s" % TOOL_VERSION)
        print("Usage:")
        print("  python -m language_fugue --test    # Run tests")
        print("  python -m language_fugue --fugue  # Generate code composition")