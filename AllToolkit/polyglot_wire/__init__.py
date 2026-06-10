#!/usr/bin/env python3
"""
🔌 Polyglot Wire v1.0
A cross-language interoperability explorer — maps how data and functions
travel between languages via FFI, bindings, serialization, and IPC.

Creative concept: "Languages are islands; wire protocols are the bridges.
This tool maps what's possible to send across, what's lost in transit,
and what each language uses to connect to the outside world."

For the selected rotation language, this tool:
  1. Identifies the language's primary FFI/binding mechanism (C ABI, cgo, JNI, Python FFI…)
  2. Shows serialization formats supported (JSON, Protobuf, FlatBuffers, Cap'n Proto, msgpack…)
  3. Documents cross-language communication patterns (gRPC, ZeroMQ, nanomsg, shared memory…)
  4. Provides a "wire compatibility matrix" showing which languages can talk to each other natively
  5. Generates a practical FFI call example — calling a C library from the language

Distinct from existing tools:
  - polyglot_digest:      syntax-parallel snippets (same problem, same code, different syntax)
  - polyglot_resonator:   mental model frames (how each language THINKS)
  - polyglot_dna:         genetic trait mapping (what each language IS)
  - polyglot_chronicle:   daily history + challenge (temporal today)
  - polyglot_bridges:     semantic problem→solution maps (conceptual translation)
  - language_archaeology: historical lineage (temporal depth)
  - language_compass:      learning journey maps (milestones, stages)
  - language_ethos:       philosophical manifesto (belief/identity)
  - language_sage:        idioms, tips, pitfalls (practical wisdom)
  - language_ecohub:      package ecosystem (tooling landscape)
  - polyglot_chronicle:   daily diary entry (today's events/history/challenge)

Wire is about INTEROPERABILITY — how languages connect to each other and to foreign code.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import random
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-wire"
TOOL_VERSION = "1.0.0"

# The 8 languages this tool manages — matches the rotation order
TOOL_LANGUAGES = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]

ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
    "language_rotation.json"
)


def load_rotation():
    """Load language rotation config."""
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data):
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── FFI & Interoperability Profiles ──────────────────────────────────────────
# For each language: FFI mechanism, serialization formats, IPC options, example
INTEROP_PROFILES: Dict[str, Any] = {
    "Rust": {
        "ffi_name": "Rust → C via `#[no_mangle]` + C ABI",
        "ffi_mechanism": "Unsafe Rust, extern \"C\" blocks, #[no_mangle] for C symbol export",
        "inbound_ffi": "cbindgen generates C headers from Rust; rust-bindgen parses them",
        "serialization": ["serde_json", "rmp_serde (msgpack)", "prost (Protobuf)", "flatbuffers", "capnproto-rust", "Postcard (compact binary)"],
        "serialization_note": "serde is the de-facto standard — handles JSON, Bincode, MessagePack, etc.",
        "ipc_schemes": ["Unix domain sockets", "TCP/UDP", "gRPC via tonic", "共享内存 via libc", "nanomsg / nanomsg"],
        "foreign_interface": ["Python via PyO3 (Python 3.7+, matures rapidly)", "Node.js via neon (native Node.js addons)", "wasm-bindgen (WebAssembly)", "JNI via diplomat (experimental)"],
        "calling_c_example": '''// Rust exports a C-compatible function
#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}

// Python calls it via ctypes
import ctypes
lib = ctypes.CDLL('./librustlib.so')
result = lib.add(40, 2)  // → 42''',
        "calling_c_explained": "Rust's extern \"C\" blocks emit standard C ABI symbols. cbindgen auto-generates C headers, then ctypes/callable C code consumes them.",
        "key_insight": "Rust's safety guarantees don't extend past its FFI boundary — the 'unsafe' boundary is explicit and small.",
        "wire_score": 8,  # How easy it is to wire Rust to other languages (1-10)
    },
    "Go": {
        "ffi_name": "Go → C via cgo",
        "ffi_mechanism": "cgo for C integration, SWIG for wrapping C++ libraries, cshared for building shared libraries",
        "inbound_ffi": "cgo handles inbound C calls; can build .so/.dylib via -buildmode=c-shared",
        "serialization": ["encoding/json", "gob (Go-specific binary)", "protobuf (google.golang.org/protobuf)", "go-protobuf (v1)", "msgp (MessagePack code-gen)", "flatbuffers via github.com/google/flatbuffers/go"],
        "serialization_note": "gob is fast & compact but Go-only; json is slow but universal",
        "ipc_schemes": ["Unix pipes", "Unix domain sockets", "TCP/HTTP", "gRPC (first-class)", "共享内存 via golang.org/x/sys/windows", "nanomsg via github.com/go-nanomsg"],
        "foreign_interface": ["Python via cgo + ctypes bridge", "Node.js via addons (cgo + V8)", "WebAssembly via TinyGo or standard Go (wasm)"],
        "calling_c_example": '''// Go exports via c-shared build mode
package main

// #include <stdint.h>
// extern int32_t add(int32_t a, int32_t b);
import "C"

func main() {
    println(C.add(40, 2))  // → 42 (calling C lib)
}

// Build: go build -buildmode=c-shared -o libgo.so''',
        "calling_c_explained": "cgo is Go's FFI — it compiles C code inline and links it. Building with -buildmode=c-shared exports Go functions as a .so callable from anywhere.",
        "key_insight": "Go's goroutines are FIRST-CLASS and cheap — they beat threads for I/O-bound concurrency. gRPC makes them network-native.",
        "wire_score": 7,
    },
    "Swift": {
        "ffi_name": "Swift → C / Objective-C via ClangImporter",
        "ffi_mechanism": "Swift has a first-class C and Objective-C importer (ClangImporter). Swift Package Manager handles FFI via packages.",
        "inbound_ffi": "Swift can import C headers directly. Objective-C code is bridging-header free for most cases. Swift 6 eliminates unsafe code.",
        "serialization": ["Codable (JSON/PropertyList)", "NSCoding (legacy)", "Protocol Buffers via swift-protobuf", "FlatBuffers via flatbuffers-swift", "MessagePack via msgpack-swift"],
        "serialization_note": "Codable (Encodable/Decodable) is built-in — no external library needed for JSON",
        "ipc_schemes": ["XPC (macOS/iOS inter-process communication)", "Darwin notifications", "Unix domain sockets", "gRPC via swift-nio-grpc", "REST/HTTP"],
        "foreign_interface": ["Python via PythonKit (Swift-for-Python)", "JavaScript via JavaScriptCore", "WebAssembly via WasmKit"],
        "calling_c_example": '''// Swift calls a C function directly — ClangImporter handles it
import Darwin  // Swift's name for libc

let result = Darwin.add(40, 2)  // calling libc add

// Swift wrapping a C library:
// mylib.h → added to bridging header or imported via modulemap
// Then: let val = mylib_calculate(40, 2)''',
        "calling_c_explained": "Swift's ClangImporter reads C headers and exposes them as Swift — zero wrapper needed for most C libraries. Darwin module exposes libc.",
        "key_insight": "Swift's value types (structs) and copy-on-write arrays mean less memory churn. ARC handles reference types automatically.",
        "wire_score": 7,
    },
    "Kotlin": {
        "ffi_name": "Kotlin → C/C++ via JNI or Kotlin Native",
        "ffi_mechanism": "JNI (Java Native Interface) for C/C++, Kotlin/Native for WebAssembly and iOS",
        "inbound_ffi": "JNI is mature but verbose; Kotlin/Native enables direct C interop without JVM",
        "serialization": ["kotlinx.serialization (JSON/ProtoBuf/CBOR)", "Kotlinx-io (byte buffers)", "FlatBuffers via flatbuffers/kotlin", "Protocol Buffers via protoc-gen-kotlin", "msgpack-kotlin"],
        "serialization_note": "kotlinx.serialization is the standard — handles JSON, ProtoBuf, CBOR, HOCON",
        "ipc_schemes": ["gRPC (kotlin-grpc)", "Unix domain sockets via java.nio", "Aeron (high-performance IPC)", "ZeroMQ via jzmq", "REST/gRPC"],
        "foreign_interface": ["Python via chaquopy (Python-on-JVM)", "JavaScript via Kotlin/JS", "WebAssembly via Kotlin/Native wasm"],
        "calling_c_example": '''// Kotlin/Native calling C via cinterop
// mylib.h:
// int add(int a, int b);

// build.gradle.kts:
// nativeLibraryPaths += file("libmylib.so")

// Kotlin code:
import kotlinx.cinterop.*
import mylib.*

fun main() {
    println(add(40, 2))  // → 42
}

// Or on JVM with JNI:
// class NativeLib {
    // native fun add(a: Int, b: Int): Int
    // companion object { System.loadLibrary("mylib") }
}''',
        "calling_c_explained": "Kotlin/Native's cinterop tool reads C headers and generates Kotlin FFI bindings automatically. On JVM, JNI is the path.",
        "key_insight": "Kotlin's coroutines are the best async story on the JVM — lightweight, cancelable, and composable.",
        "wire_score": 6,
    },
    "TypeScript": {
        "ffi_name": "TypeScript → WebAssembly / Native via wasm-bindgen / ts2x",
        "ffi_mechanism": "No native FFI — communicates via WebAssembly, Node.js addons (N-API), or service boundaries",
        "inbound_ffi": "Node.js N-API (stable C API for native addons), WebAssembly is the primary native bridge",
        "serialization": ["JSON (universal)", "MessagePack via msgpack5", "Protocol Buffers via protobufjs", "FlatBuffers via flatbuffers TS", "BSON via bson-npm"],
        "serialization_note": "JSON dominates because JS is the web's lingua franca — but TypeScript adds type safety on top",
        "ipc_schemes": ["WebSocket", "HTTP/REST", "gRPC-web", "SharedArrayBuffer + Atomics (WASM workers)", "postMessage (browser tabs)", "Node.js IPC (child_process)"],
        "foreign_interface": ["Rust via wasm-bindgen + wasm-pack", "C/C++ via Emscripten (asm.js → WebAssembly)", "Go via TinyGo wasm", "Python via Pyodide (Python-in-Browser)"],
        "calling_c_example": '''// TypeScript → Rust via WebAssembly (wasm-bindgen)
// Rust: wasm-pack build --target web
// wasm-pack generates JS/TS wrappers automatically

import init, { add } from './pkg/my_wasm_lib.js';
await init();  // initialize WASM module
console.log(add(40, 2));  // → 42

// Or Node.js N-API (C addon):
// addon.node — built with node-gyp
const addon = require('./build/Release/addon.node');
console.log(addon.add(40, 2));''',
        "calling_c_explained": "TypeScript can't call C directly — WebAssembly is the safe, fast path to native code. N-API provides C addons via Node.js.",
        "key_insight": "TypeScript's type system is a compile-time tool — it disappears at runtime (or becomes runtime checks with ts-node). Design for that.",
        "wire_score": 9,  # Highest because JSON/JS is universal, and WASM bridges to native
    },
    "JavaScript": {
        "ffi_name": "JavaScript → Native via WebAssembly / Node.js N-API",
        "ffi_mechanism": "No native FFI in browsers; Node.js N-API for C/C++. WebAssembly for universal native bridge",
        "inbound_ffi": "WebAssembly is the universal bridge. In Node: require('bindings') + N-API.",
        "serialization": ["JSON (universal king)", "BSON (MongoDB-native binary JSON)", "MessagePack", "Protocol Buffers via protobufjs", "cbor.js", "thrift (Apache Thrift)"],
        "serialization_note": "JSON is so dominant in JS that every other format is an afterthought. The web IS JSON.",
        "ipc_schemes": ["WebSocket", "postMessage / BroadcastChannel", "SharedArrayBuffer + Atomics", "Service Worker communication", "WebRTC (P2P)", "HTTP/2, HTTP/3"],
        "foreign_interface": ["Rust via wasm-bindgen", "C++ via Emscripten", "Go via TinyGo", "Python via Pyodide"],
        "calling_c_example": '''// JavaScript → C via WebAssembly (Emscripten)
// Emscripten: emcc add.c -o add.js
// Generates add.wasm + JS glue code

var Module = require('./add.js');
Module.onRuntimeInitialized = () => {
    console.log(Module._add(40, 2));  // → 42 (C function, exported as _add)
};

// Or Node.js N-API:
// node-gyp build → addon.node
const addon = require('./build/Release/addon');
console.log(addon.add(40, 2));''',
        "calling_c_explained": "Emscripten compiles C/C++ to WebAssembly + JS glue. In Node, N-API addons are the standard way to expose C code.",
        "key_insight": "JavaScript runs EVERYWHERE — browsers, servers, edge (Cloudflare Workers), embedded (Espruino), AI (TensorFlow.js). Wire once, run anywhere.",
        "wire_score": 9,
    },
    "Java": {
        "ffi_name": "Java → C/C++ via JNI (Java Native Interface)",
        "ffi_mechanism": "JNI since Java 1.1 — mature, verbose, dangerous (leaks, crashes). Panama (Java 22+) modernizes this.",
        "inbound_ffi": "JNI is the standard path. Java 22+ Panama API replaces JNI with cleaner foreign function & memory API.",
        "serialization": ["Java Object Serialization (built-in)", "JSON via Jackson / Gson", "Protocol Buffers via protobuf-javalite", "Kryo (high-performance binary)", "Avro (Hadoop schema-evolution)", "FlatBuffers via flatbuffers/java"],
        "serialization_note": "Java has more serialization formats than any other language — enterprise needs fuel variety",
        "ipc_schemes": ["RMI (legacy, avoid)", "gRPC (modern choice)", "JMS (enterprise messaging)", "Unix sockets via Java NIO", "Aeron (high-performance)", "WebSocket"],
        "foreign_interface": ["Python via Jython", "R via rJava", "Native code via JNI/Panama", "WebAssembly via GraalVM TruffleWASM"],
        "calling_c_example": '''// Java → C via JNI
// NativeLib.c:
// JNIEXPORT jint JNICALL Java_NativeLib_add(JNIEnv* env, jclass cls, jint a, jint b) {
    // return a + b;
// }

// Java code:
public class NativeLib {
    static { System.loadLibrary("mylib"); }
    public native int add(int a, int b);
}

// Usage:
NativeLib lib = new NativeLib();
System.out.println(lib.add(40, 2));  // → 42

// Java 22+ Panama API (cleaner):
// try (Arena arena = Arena.ofConfined()) {
    // FunctionDescriptor.of(INTEGER, INTEGER, INTEGER);
    // MemorySegment add = Linker.nativeLinker().defaultLookup()
        // .find("add").orThrow();
// }''',
        "calling_c_explained": "JNI is verbose but battle-tested — every JVM release maintains it. Panama (Java 22+) finally replaces it with a modern, safe API.",
        "key_insight": "Java's 'write once, run anywhere' only works WITHIN the JVM. For native code, you're back to JNI. GraalVM is the future — native images, polyglot.",
        "wire_score": 5,
    },
    "C/C++": {
        "ffi_name": "C/C++ → Everything (the universal FFI language)",
        "ffi_mechanism": "C ABI is the wire standard. C++ uses name mangling + vtable + Itanium/MS ABI. Every language can call C.",
        "inbound_ffi": "C is the interoperability layer. C++ requires explicit extern \"C\" to suppress name mangling.",
        "serialization": ["C struct packing + manual read/write", "Protocol Buffers via libprotobuf-c (protobuf-c)", "MessagePack via msgpack-c", "FlatBuffers (flatbuffers_c)", "cJSON (lightweight JSON)", "CBOR via libcbor"],
        "serialization_note": "C has no standard serialization — you roll your own or use mature C libraries. Protocol Buffers (protobuf-c) is the most portable.",
        "ipc_schemes": ["Shared memory (shmget/shm_open)", "Unix domain sockets", "Message queues (POSIX mq)", "Pipes (anonymous + named)", "TCP/UDP", "gRPC via grpc (C++ core)", "Nanomsg via nanomsg/c"],
        "foreign_interface": ["Python via ctypes / cffi / cppyy", "R via Rcpp", "Julia via ccall / cglobal", "MATLAB via MEX files", "Rust via FFI (cbindgen)", "Any language with C ABI support"],
        "calling_c_example": '''/* C can call any language with a C ABI */
/* Example: calling a Rust .so from C */
#include <stdint.h>
#include <stdio.h>

// Rust .so declares: extern "C" int32_t add(int32_t a, int32_t b);
extern int32_t add(int32_t a, int32_t b);

int main() {
    printf("%d\\n", add(40, 2));  // → 42
    return 0;
}

/* Compile & link: gcc main.c -L./target/release -l rustlib -o main */
/* LD_LIBRARY_PATH=./target/release ./main */

/* Python via ctypes: */
import ctypes
lib = ctypes.CDLL('./libmylib.so')
print(lib.add(40, 2))  # → 42''',
        "calling_c_explained": "C is the wire language of the world. Every serious language provides a C FFI. C++ adds complexity via name mangling — use extern \"C\" to opt out.",
        "key_insight": "C's strength AND weakness: you own EVERYTHING. Memory, pointers, allocation. No safety net — but also no overhead.",
        "wire_score": 10,  # C IS the wire
    },
}


# ── Wire Compatibility Matrix ────────────────────────────────────────────────────
# Shows which languages can directly communicate with which others
# 10 = native C ABI / first-class support
#  7 = well-supported FFI / WASM
#  5 = supported but verbose/fragile
#  3 = experimental / painful
#  0 = not practical
WIRE_MATRIX: Dict[str, Dict[str, int]] = {
    "Rust": {
        "Rust": 10, "Go": 5, "Swift": 7, "Kotlin": 5, "TypeScript": 7, "JavaScript": 7, "Java": 4, "C/C++": 9,
    },
    "Go": {
        "Rust": 5, "Go": 10, "Swift": 3, "Kotlin": 5, "TypeScript": 5, "JavaScript": 5, "Java": 5, "C/C++": 7,
    },
    "Swift": {
        "Rust": 7, "Go": 3, "Swift": 10, "Kotlin": 6, "TypeScript": 7, "JavaScript": 7, "Java": 5, "C/C++": 8,
    },
    "Kotlin": {
        "Rust": 5, "Go": 5, "Swift": 6, "Kotlin": 10, "TypeScript": 5, "JavaScript": 5, "Java": 8, "C/C++": 5,
    },
    "TypeScript": {
        "Rust": 7, "Go": 5, "Swift": 7, "Kotlin": 5, "TypeScript": 10, "JavaScript": 10, "Java": 3, "C/C++": 6,
    },
    "JavaScript": {
        "Rust": 7, "Go": 5, "Swift": 7, "Kotlin": 5, "TypeScript": 10, "JavaScript": 10, "Java": 3, "C/C++": 6,
    },
    "Java": {
        "Rust": 4, "Go": 5, "Swift": 5, "Kotlin": 8, "TypeScript": 3, "JavaScript": 3, "Java": 10, "C/C++": 7,
    },
    "C/C++": {
        "Rust": 9, "Go": 7, "Swift": 8, "Kotlin": 5, "TypeScript": 6, "JavaScript": 6, "Java": 7, "C/C++": 10,
    },
}


def get_compatibility_bar(score: int) -> str:
    """Render a score as a visual bar."""
    filled = "█" * (score // 2)
    half = "▌" if score % 2 else ""
    empty = "░" * (5 - len(filled) - (1 if half else 0))
    return f"[{filled}{half}{empty}] {score}/10"


def get_serial_format_badge(fmt: str) -> str:
    """Return emoji badge for serialization format."""
    badges = {
        "JSON": "📋", "gob": "🔴", "Protobuf": "⚡", "MessagePack": "📦",
        "FlatBuffers": "🚀", "Cap'n Proto": "⚡", "Codable": "🍎", "NSCoding": "🍎",
        "Kryo": "💎", "Avro": "📡", "BSON": "🗃️", "CBOR": "📊",
    }
    return badges.get(fmt, "📄")


def wire() -> Dict[str, Any]:
    """
    Generate a wire interoperability report for the current rotation language.

    1. Load current index from language_rotation.json
    2. Pick the language at that index
    3. Advance the index (wrap around if past the end)
    4. Build a comprehensive interop profile for the language
    5. Save the updated rotation
    """
    # Step 1: load
    rotation = load_rotation()
    languages = TOOL_LANGUAGES
    current_index = rotation.get("current_index", 1)
    if current_index >= len(languages):
        current_index = 0

    # Step 2: select
    language = languages[current_index]
    profile = INTEROP_PROFILES.get(language, {})

    # Step 3: advance index
    next_index = (current_index + 1) % len(languages)
    rotation["current_index"] = next_index
    rotation["last_language"] = language
    rotation["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()

    # Step 4: build report
    compat = WIRE_MATRIX.get(language, {})

    # Sort other languages by compatibility score
    compat_sorted = sorted(
        [(lang, score) for lang, score in compat.items() if lang != language],
        key=lambda x: x[1],
        reverse=True
    )

    # Wire compatibility matrix display
    matrix_rows = []
    for other_lang, score in compat_sorted:
        bar = get_compatibility_bar(score)
        matrix_rows.append({
            "language": other_lang,
            "score": score,
            "bar": bar,
            "quality": (
                "native C ABI" if score >= 9
                else "first-class" if score >= 8
                else "well-supported" if score >= 7
                else "supported" if score >= 5
                else "experimental" if score >= 3
                else "not practical"
            ),
        })

    # Serialization formats with badges
    serial_formats = profile.get("serialization", [])
    serial_display = [
        {"format": fmt, "badge": get_serial_format_badge(fmt)}
        for fmt in serial_formats
    ]

    # FFI mechanisms
    ffi_sections = [
        {"role": "Exporting (outbound)", "text": profile.get("ffi_name", "N/A"), "detail": profile.get("calling_c_explained", "")},
        {"role": "Importing (inbound)", "text": profile.get("inbound_ffi", "N/A"), "detail": ""},
    ]

    # IPC schemes
    ipc_schemes = profile.get("ipc_schemes", [])

    # Foreign interfaces
    foreign_iface = profile.get("foreign_interface", [])

    # Wire score
    wire_score = profile.get("wire_score", 5)
    wire_bar = get_compatibility_bar(wire_score)

    report = {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "language": language,
        "rotation_index": current_index,
        "wire_score": wire_score,
        "wire_bar": wire_bar,
        "ffi_profiles": ffi_sections,
        "serialization": serial_display,
        "serialization_note": profile.get("serialization_note", ""),
        "ipc_schemes": ipc_schemes,
        "foreign_interfaces": foreign_iface,
        "calling_c_example": {
            "code": profile.get("calling_c_example", ""),
            "explained": profile.get("calling_c_explained", ""),
        },
        "key_insight": profile.get("key_insight", ""),
        "compatibility_matrix": matrix_rows,
    }

    # Step 5: save updated rotation
    save_rotation(rotation)

    return report


def format_wire_text(report: Dict[str, Any]) -> str:
    """Format the wire report as readable text."""
    lines = []
    lang = report["language"]

    lines.append(f"🔌 Polyglot Wire — {lang}")
    lines.append(f"   Generated: {report['generated_at']}")
    lines.append(f"   Rotation index: {report['rotation_index']}")
    lines.append("")

    # Wire score
    lines.append(f"📡 Wire Score: {report['wire_bar']}")
    lines.append("")

    # FFI profiles
    lines.append("─── FFI Profiles ───")
    for ffi in report["ffi_profiles"]:
        lines.append(f"  [{ffi['role']}]")
        lines.append(f"    → {ffi['text']}")
        if ffi.get("detail"):
            lines.append(f"    → {ffi['detail']}")
    lines.append("")

    # Serialization
    lines.append("─── Serialization Formats ───")
    fmt_list = ", ".join([f"{s['badge']} {s['format']}" for s in report["serialization"]])
    lines.append(f"  {fmt_list}")
    if report.get("serialization_note"):
        lines.append(f"  Note: {report['serialization_note']}")
    lines.append("")

    # IPC
    lines.append("─── IPC Schemes ───")
    for ipc in report["ipc_schemes"]:
        lines.append(f"  • {ipc}")
    lines.append("")

    # Foreign interfaces
    if report.get("foreign_interfaces"):
        lines.append("─── Foreign Interfaces ───")
        for fi in report["foreign_interfaces"]:
            lines.append(f"  • {fi}")
        lines.append("")

    # Calling C example
    lines.append("─── Calling C / Foreign Code Example ───")
    lines.append(f"  ```c")
    for line in report["calling_c_example"]["code"].split("\n"):
        lines.append(f"  {line}")
    lines.append(f"  ```")
    if report["calling_c_example"].get("explained"):
        lines.append(f"  💡 {report['calling_c_example']['explained']}")
    lines.append("")

    # Key insight
    if report.get("key_insight"):
        lines.append(f"─── Key Insight ───")
        lines.append(f"  💡 {report['key_insight']}")
        lines.append("")

    # Compatibility matrix
    lines.append("─── Compatibility Matrix (how well can {lang} wire to…) ───".format(lang=lang))
    for row in report["compatibility_matrix"]:
        lines.append(
            f"  {row['language']:<12} {row['bar']}  {row['quality']}"
        )
    lines.append("")
    lines.append(f"  ↻ Next: {TOOL_LANGUAGES[(report['rotation_index'] + 1) % len(TOOL_LANGUAGES)]}")

    return "\n".join(lines)


def run_tests() -> None:
    """Run unit tests."""
    import traceback

    errors = []

    # ── Test 1: rotation file exists ──────────────────────────────────────────
    try:
        assert os.path.exists(ROTATION_FILE), f"rotation file not found: {ROTATION_FILE}"
        print("✅ Test 1: rotation file exists")
    except Exception as e:
        errors.append(f"❌ Test 1: {e}")

    # ── Test 2: wire() returns expected shape ──────────────────────────────────
    try:
        result = wire()
        assert isinstance(result, dict), "wire() must return dict"
        assert "language" in result, "result must have 'language'"
        assert "wire_score" in result, "result must have 'wire_score'"
        assert "compatibility_matrix" in result, "result must have 'compatibility_matrix'"
        assert "ffi_profiles" in result, "result must have 'ffi_profiles'"
        assert "serialization" in result, "result must have 'serialization'"
        assert "calling_c_example" in result, "result must have 'calling_c_example'"
        print("✅ Test 2: wire() returns expected shape")
    except Exception as e:
        errors.append(f"❌ Test 2: {e}")
        traceback.print_exc()

    # ── Test 3: rotation index advances correctly ───────────────────────────────
    try:
        with open(ROTATION_FILE, "r") as f:
            before = json.load(f)
        idx_before = before["current_index"]

        result = wire()  # advances index
        idx_after = result["rotation_index"]

        # idx_after should be (idx_before + 1) % 8
        expected = idx_before % len(TOOL_LANGUAGES)
        assert idx_after == expected, f"index should advance from {idx_before} → {expected}, got {idx_after}"
        print(f"✅ Test 3: index advances correctly ({idx_before} → {expected})")
    except Exception as e:
        errors.append(f"❌ Test 3: {e}")
        traceback.print_exc()

    # ── Test 4: all languages in TOOL_LANGUAGES have profiles ─────────────────
    try:
        for lang in TOOL_LANGUAGES:
            assert lang in INTEROP_PROFILES, f"language {lang} missing from INTEROP_PROFILES"
        print("✅ Test 4: all languages have interop profiles")
    except Exception as e:
        errors.append(f"❌ Test 4: {e}")

    # ── Test 5: format_wire_text produces output ────────────────────────────────
    try:
        result = wire()
        text = format_wire_text(result)
        assert len(text) > 100, "formatted text too short"
        assert lang in text, f"language name missing from output"
        assert "Wire Score" in text or "wire_score" in result, "wire score missing"
        print(f"✅ Test 5: format_wire_text produces output ({len(text)} chars)")
    except Exception as e:
        errors.append(f"❌ Test 5: {e}")
        traceback.print_exc()

    # ── Test 6: compatibility matrix has entries for all other languages ─────────
    try:
        result = wire()
        matrix = result["compatibility_matrix"]
        assert len(matrix) == len(TOOL_LANGUAGES) - 1, \
            f"matrix should have {len(TOOL_LANGUAGES) - 1} entries, got {len(matrix)}"
        for row in matrix:
            assert "language" in row
            assert "score" in row
            assert "bar" in row
            assert "quality" in row
        print("✅ Test 6: compatibility matrix is complete")
    except Exception as e:
        errors.append(f"❌ Test 6: {e}")
        traceback.print_exc()

    # ── Test 7: serialization formats are listed ────────────────────────────────
    try:
        result = wire()
        assert len(result["serialization"]) > 0, "serialization list should not be empty"
        for s in result["serialization"]:
            assert "format" in s
            assert "badge" in s
        print(f"✅ Test 7: serialization formats listed ({len(result['serialization'])} formats)")
    except Exception as e:
        errors.append(f"❌ Test 7: {e}")

    # ── Summary ────────────────────────────────────────────────────────────────
    print("")
    if errors:
        print("FAILURES:")
        for e in errors:
            print(f"  {e}")
        raise SystemExit(1)
    else:
        print(f"🎉 All 7 tests passed!")