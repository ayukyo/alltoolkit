#!/usr/bin/env python3
"""
🔧 Polyglot Recovery v1.0

Resilience Cartography — maps how each programming language models
failure recovery, retry strategies, circuit breakers, and graceful
degradation when things go wrong.

Creative concept: "Every language has a philosophy of failure. Some
languages pretend bad things never happen (C/C++: undefined behavior).
Others build entire ecosystems around it (Rust: Result<T,E> + the ?
operator). Go: you check the error and move on. Java: checked exceptions
force you to acknowledge failure. This tool maps the RECOVERY TOPOLOGY
of each language — what happens after the error, how retries feel,
how graceful degradation works, and what 'healing' means in each paradigm."

Each run selects the current rotation language and maps its recovery
architecture across five dimensions:
  1. RECOVERY MODEL  — how errors are caught and handled
  2. RETRY MECHANISM — how failed operations are retried
  3. GRACEFUL DEGRADATION — how systems degrade under failure
  4. CIRCUIT BREAKER — how languages handle cascading failures
  5. RESURRECTION    — how state is rebuilt after failure

Each category shows how the current language compares to all other
languages in the rotation — a "recovery topology map."

Distinct from existing tools:
  - polyglot_signal:        signal semantics (how languages SIGNAL conditions)
  - polyglot_resonator:     mental models (how languages THINK)
  - polyglot_topology:      neighborhood graph of design space
  - polyglot_harmony:       compatibility between consecutive pairs
  - polyglot_mood:          emotional personality profiles
  - polyglot_lexicon:       dictionary-style entries
  - polyglot_craft:         practical skill cards
  - polyglot_tempo:         timing/performance characteristics
  - polyglot_chronology:    geological time depth
  - polyglot_digest:        syntax-parallel code (same logic)
  - polyglot_translation:   cultural idioms/proverbs
  - polyglot_forge:        transformation & conversion
  - polyglot_resonance:     frequency harmonics
  - polyglot_cartographer: feature matrix comparison
  - polyglot_ecosystem_map: package landscape

Polyglot Recovery is about RESILIENCE ENGINEERING — how languages and
their ecosystems model failure, recovery, and graceful degradation.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-recovery"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent.parent  # polyglot_recovery/
_WORKSPACE_ROOT = _MODULE_DIR.parent               # AllToolkit/ -> workspace/
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ─────────────────────────────────────────────────────────────────────────────
# Recovery Category Database
# ─────────────────────────────────────────────────────────────────────────────
# Each language has 5 recovery dimensions:
#   model       — how errors are caught and handled
#   retry       — how failed operations are retried
#   degrade     — how systems degrade gracefully under failure
#   circuit     — how cascading failures are halted
#   resurrect   — how state is rebuilt after failure

RECOVERY_DB: Dict[str, Dict[str, Dict[str, Any]]] = {

    "Rust": {
        "model": {
            "strategy": "Result<T, E> + match/if let",
            "mechanism": "Errors are values propagated via Result<T,E>. No exceptions. "
                        "The ? operator auto-propagates. Pattern matching is exhaustive.",
            "idiom": "let f = File::open(\"data\")?; // Err propagates, Ok unwraps",
            "key_traits": ["no hidden control flow", "exhaustive pattern matching",
                           "? operator for clean propagation", "no exception overhead"],
            "resilience_tag": "PROVEN",
            "emoji": "🛡️",
        },
        "retry": {
            "strategy": "Manual retry loops + backoff crates",
            "mechanism": "No built-in retry. Retry logic is explicit: loop { match op() { Ok(v) => break, Err(e) => { if retries == 0 { break } retries -= 1; } } }. "
                        "Crates like `retry` or `backoff` wrap this pattern.",
            "idiom": "loop { match fetch(url) { Ok(data) => break data, Err(e) => { if retry_count == 0 { return Err(e) } retry_count -= 1; } } }",
            "key_traits": ["explicit retry loop", "no hidden retry magic",
                           "compile-time safe (no unchecked retries)", "backoff configurable"],
            "resilience_tag": "PROVEN",
            "emoji": "🛡️",
        },
        "degrade": {
            "strategy": "Option<T> for partial availability",
            "mechanism": "Services that may be unavailable return Option<T>. "
                        "None means degraded mode. Code uses `or_else` to provide fallbacks.",
            "idiom": "let cache = get_cached_data().or_else(|| get_cheaper_data());",
            "key_traits": ["Option as degradation signal", "or_else for fallbacks",
                           "compile-time enforced graceful degradation", "no runtime null checks"],
            "resilience_tag": "PROVEN",
            "emoji": "🛡️",
        },
        "circuit": {
            "strategy": "No built-in circuit breaker; use `circuit_breaker` crate",
            "mechanism": "Rust has no language-level circuit breaker. "
                        "A `circuit_breaker` crate wraps operations: it tracks failures "
                        "and opens the circuit after N failures, fast-failing subsequent calls.",
            "idiom": "breaker.call(|| risky_op()).unwrap_or(fallback)",
            "key_traits": ["third-party crate (circuit_breaker)", "compile-time typed fallback",
                           "state machine pattern", "no magic in the language"],
            "resilience_tag": "BUILTIN",
            "emoji": "🛡️",
        },
        "resurrect": {
            "strategy": "Drop + explicit rebuild + RAII",
            "mechanism": "RAII: resources are freed via Drop when structs go out of scope. "
                        "For resurrection: recreate the connection in a new scope, "
                        "propagate the new handle. No automatic self-healing.",
            "idiom": "struct DBConn { pool: Pool } impl Drop for DBConn { fn drop(&mut self) { self.pool.release(); } }",
            "key_traits": ["RAII deterministic cleanup", "explicit rebuild pattern",
                           "no automatic self-healing", "no exception-based resurrection"],
            "resilience_tag": "PROVEN",
            "emoji": "🛡️",
        },
    },

    "Go": {
        "model": {
            "strategy": "error interface — returned, not thrown",
            "mechanism": "Errors are returned as values (last return argument). "
                        "The caller must check. No exception mechanism. "
                        "Multiple return values: `(T, error)`.",
            "idiom": "f, err := os.Open(\"data\"); if err != nil { return err } // explicit nil check",
            "key_traits": ["explicit error checking", "no hidden control flow",
                           "errors are just interfaces", "no exception cost"],
            "resilience_tag": "NOMINAL",
            "emoji": "⚡",
        },
        "retry": {
            "strategy": "Explicit retry with for loop + time.Sleep",
            "mechanism": "Standard pattern: `for attempts := 0; attempts < maxRetries; attempts++` "
                        "with `time.Sleep(backoff)`. No retry library needed for basic cases.",
            "idiom": "for attempt := 0; attempt < 3; attempt++ { _, err := rpc.Call(); if err == nil { break }; time.Sleep(time.Duration(attempt+1)*100*time.Millisecond) }",
            "key_traits": ["explicit for loop", "manual backoff", "no retry magic",
                           "context.WithTimeout for deadline", "easy to read"],
            "resilience_tag": "NOMINAL",
            "emoji": "⚡",
        },
        "degrade": {
            "strategy": "Caching layer + fallback return pattern",
            "mechanism": "Go services degrade by returning cached/stale data. "
                        "The cache is checked first; on miss, fallback data is returned.",
            "idiom": "func getUser(id string) (User, error) { if u, ok := cache.Get(id); ok { return u, nil }; return db.getUser(id) }",
            "key_traits": ["explicit cache check", "nil vs. error distinction",
                           "interface{} for generic caching", "no Option type"],
            "resilience_tag": "NOMINAL",
            "emoji": "⚡",
        },
        "circuit": {
            "strategy": "sony/gobreaker third-party library",
            "mechanism": "gobreaker: tracks success/failure counts, opens circuit after "
                        "N consecutive failures. While open, calls fast-fail with circuit-open error.",
            "idiom": "breaker := gobreaker.NewCircuitBreaker(gobreaker.Settings{Name: \"my-service\"}); _, err := breaker.Execute(func() (interface{}, error) { return call() })",
            "key_traits": ["third-party library (gobreaker)", "state machine: closed/open/half-open",
                           "configurable threshold", "counts are not language-level"],
            "resilience_tag": "BUILTIN",
            "emoji": "⚡",
        },
        "resurrect": {
            "strategy": "goroutine restart + connection pool reset",
            "mechanism": "A crashed goroutine cannot be restarted, but the supervisor "
                        "pattern (watchdog goroutine) spawns a new one. "
                        "DB connection pools are reset via pool.Close() + reconnect.",
            "idiom": "go func() { for { if err := worker(); err != nil { log.Println(err); continue }; } }()",
            "key_traits": ["goroutine restart pattern", "watchdog supervisor",
                           "connection pool reset", "no automatic resurrection"],
            "resilience_tag": "NOMINAL",
            "emoji": "⚡",
        },
    },

    "Swift": {
        "model": {
            "strategy": "throws + Error protocol + do/catch",
            "mechanism": "Functions marked `throws` produce errors conforming to Error. "
                        "`do/catch` handles them. try? returns Optional. "
                        "try? for silent propagation, try! for force-unwrap.",
            "idiom": "do { try save(data) } catch { print(\"Recovery: \\(error)\") }",
            "key_traits": ["typed throws", "exhaustive catch (if not using `default`)",
                           "try? for Optional propagation", "no runtime exception cost"],
            "resilience_tag": "PROVEN",
            "emoji": "🏔️",
        },
        "retry": {
            "strategy": "async/await with retry loops + Combine publishers",
            "mechanism": "Swift 5.5+: async/await with explicit retry loops. "
                        "Combine framework has retry operators for publishers.",
            "idiom": "func fetchWithRetry() async throws -> Data { for attempt in 0..<maxRetries { do { return try await fetch() } catch { if attempt == maxRetries-1 { throw error } } } }",
            "key_traits": ["async/await syntax", "Combine has .retry() operator",
                           "explicit attempt counting", "Task.sleep for backoff"],
            "resilience_tag": "PROVEN",
            "emoji": "🏔️",
        },
        "degrade": {
            "strategy": "Result<T, Error> + @unchecked Sendable for partial data",
            "mechanism": "Swift degrades by returning Result<T, Error> where T is partial data. "
                        "Optional values represent missing features.",
            "idiom": "let result: Result<CachedData, Error> = .success(CachedData(stale: true))",
            "key_traits": ["Result as degraded signal", "Optional for missing parts",
                           "Combine .replaceError() operator", "actor isolation for safe cache"],
            "resilience_tag": "PROVEN",
            "emoji": "🏔️",
        },
        "circuit": {
            "strategy": "No built-in; use Circuitbreaker pattern with actors",
            "mechanism": "Swift actors can implement circuit breaker state machine. "
                        "Swift 6 data-race safety makes concurrent circuit state safe by default.",
            "idiom": "actor Circuit { var state: CircuitState = .closed; func execute<T>(_ op: @escaping () async throws -> T) async throws -> T { switch state { case .closed: do { let r = try await op(); state = .closed; return r } catch { state = .open; throw error } case .open: throw CircuitOpenError() } } }",
            "key_traits": ["actor isolation for circuit state", "Swift 6 memory safety",
                           "manual state machine", "no stdlib circuit breaker"],
            "resilience_tag": "BUILTIN",
            "emoji": "🏔️",
        },
        "resurrect": {
            "strategy": "Actor recreation + supervised task groups",
            "mechanism": "Actors fail when their async body throws. "
                        "A supervising actor can recreate the failed actor. "
                        "Task groups (structured concurrency) can restart child tasks.",
            "idiom": "actor DBConnection { private var conn: Connection?; func reconnect() async { conn = try? await Connection.connect() } }",
            "key_traits": ["actor recreation pattern", "TaskGroup for supervised restarts",
                           "no automatic resurrection", "async/await for reconnect"],
            "resilience_tag": "PROVEN",
            "emoji": "🏔️",
        },
    },

    "Kotlin": {
        "model": {
            "strategy": "exceptions (unchecked) + Result<T> (runCatching)",
            "mechanism": "Kotlin has no checked exceptions. "
                        "`runCatching { }` returns Result<T>. "
                        "`onFailure` and `onSuccess` handle branches.",
            "idiom": "val result = runCatching { risky() }; result.onFailure { println(it) }",
            "key_traits": ["no checked exceptions", "Result<T> for typed errors",
                           "getOrNull for safe access", "no forced declaration"],
            "resilience_tag": "ADAPTED",
            "emoji": "🟣",
        },
        "retry": {
            "strategy": "retryWhen coroutine builder (kotlinx-coroutines)",
            "mechanism": "kotlinx-coroutines provides `retryWhen` for exponential backoff: "
                        "`retryWhen { cause, attempt -> attempt < maxRetries && cause is IOException }`",
            "idiom": "flow { emit(problematic()) }.retryWhen { cause, attempt -> attempt < 3 && cause is IOException }",
            "key_traits": ["exponential backoff built-in", "retryWhen is declarative",
                           "flow-based retry", "configurable predicate"],
            "resilience_tag": "ADAPTED",
            "emoji": "🟣",
        },
        "degrade": {
            "strategy": "Nullable types (T?) + Result for fallback data",
            "mechanism": "Degraded data is represented as nullable or Result with stale data. "
                        "Elvis operator `?:` provides inline fallback.",
            "idiom": "val data: StaleData? = cache.get(); val displayData = data ?: StaleData(age=Int.MAX_VALUE)",
            "key_traits": ["nullable as degradation signal", "elvis operator for inline fallback",
                           "Result.success with fallback value", "sealed class for partial state"],
            "resilience_tag": "ADAPTED",
            "emoji": "🟣",
        },
        "circuit": {
            "strategy": "Resilience4j circuit breaker (JVM ecosystem)",
            "mechanism": "Resilience4j is the standard JVM circuit breaker. "
                        "Kotlin-friendly: `CircuitBreakerRegistry.of { it.withFailureRateThreshold(50) }`",
            "idiom": "val breaker = CircuitBreaker.of(\"my-service\").build(); breaker.execute { call() }",
            "key_traits": ["JVM ecosystem (Resilience4j)", "state transitions: CLOSED/OPEN/HALF_OPEN",
                           "metrics integration", "Kotlin DSL for config"],
            "resilience_tag": "BUILTIN",
            "emoji": "🟣",
        },
        "resurrect": {
            "strategy": "Kotlin coroutine supervisor + supervisedJob",
            "mechanism": "`supervisorScope { }` keeps child failure from canceling siblings. "
                        "SupervisorJob lets children fail independently. "
                        "Coroutines can be restarted after cancellation.",
            "idiom": "val supervisor = SupervisorJob(); val scope = CoroutineScope(supervisor + Dispatchers.Default); scope.launch { reconnect() }",
            "key_traits": ["SupervisorJob for fault isolation", "children fail independently",
                           "explicit restart", "structured concurrency prevents leaks"],
            "resilience_tag": "ADAPTED",
            "emoji": "🟣",
        },
    },

    "TypeScript": {
        "model": {
            "strategy": "throw + try/catch (type-erased) + Result pattern (fp-ts)",
            "mechanism": "Native TS: throw can throw any value. No typed errors. "
                        "fp-ts library provides Either<E, A> for type-safe errors. "
                        "TypeScript types are erased at runtime.",
            "idiom": "import { pipe } from 'fp-ts/function'; import * as E from 'fp-ts/Either'; "
                    "const result = E.tryCatch(() => JSON.parse(input), () => new Error('parse failed'))",
            "key_traits": ["throw any type", "fp-ts Either for typed errors",
                           "unknown forces narrowing", "type erasure at runtime"],
            "resilience_tag": "ADAPTED",
            "emoji": "🔷",
        },
        "retry": {
            "strategy": "Promise + retry loops + axios-retry (HTTP)",
            "mechanism": "Explicit retry with Promise chain: "
                        "`attempt < maxRetries && try again`. "
                        "axios-retry intercepts HTTP calls.",
            "idiom": "async function fetchWithRetry(url: string, attempt = 0): Promise<Response> { "
                    "try { return await fetch(url) } catch { if (attempt >= 3) throw; "
                    "await new Promise(r => setTimeout(r, 100 * 2 ** attempt)); "
                    "return fetchWithRetry(url, attempt + 1) } }",
            "key_traits": ["recursive retry function", "exponential backoff", "no stdlib retry",
                           "axios-retry for HTTP", "Promise-based"],
            "resilience_tag": "ADAPTED",
            "emoji": "🔷",
        },
        "degrade": {
            "strategy": "null/undefined + Optional chaining for partial data",
            "mechanism": "Degraded responses use partial data structures with missing fields = undefined. "
                        "Optional chaining (?.) handles absent nested values.",
            "idiom": "const userDisplay = user?.profile?.avatar ?? '/fallback-avatar.png'",
            "key_traits": ["undefined as degradation signal", "optional chaining (?.)",
                           "nullish coalescing (??)", "no Result type in stdlib"],
            "resilience_tag": "ADAPTED",
            "emoji": "🔷",
        },
        "circuit": {
            "strategy": "opossum (npm) — circuit breaker library",
            "mechanism": "opossum: tracks latency and failure rate, opens circuit after threshold. "
                        "While open, fallback function is called.",
            "idiom": "const breaker = circuitBreaker(call, { timeout: 3000, errorThresholdPercentage: 50 }); "
                    "breaker.fallback(() => fallbackResult); breaker.fire(args)",
            "key_traits": ["npm ecosystem (opossum)", "fallback function while open",
                           "hystrix-compatible API", "metrics dashboard"],
            "resilience_tag": "BUILTIN",
            "emoji": "🔷",
        },
        "resurrect": {
            "strategy": "Promise + re-initialization pattern",
            "mechanism": "JS objects are re-created from scratch. "
                        "A crashed connection returns to initial state and reconnects via retry loop. "
                        "No persistent actor model.",
            "idiom": "class DBConnection { async connect() { this.conn = await driver.connect() } "
                    "async recover() { await this.conn.close(); await this.connect() } }",
            "key_traits": ["explicit re-initialization", "Promise-based reconnect",
                           "no automatic self-healing", "event emitter for restart events"],
            "resilience_tag": "ADAPTED",
            "emoji": "🔷",
        },
    },

    "JavaScript": {
        "model": {
            "strategy": "throw + try/catch (untyped runtime)",
            "mechanism": "throw can throw any value (Error objects recommended). "
                        "Unhandled Promise rejections are silent failures. "
                        "No compile-time checking.",
            "idiom": "try { risky() } catch (e) { if (e instanceof TypeError) handle(e) }",
            "key_traits": ["throw any type", "unhandled rejection risk",
                           "no compile-time enforcement", "finally for cleanup"],
            "resilience_tag": "RUNTIME",
            "emoji": "🟨",
        },
        "retry": {
            "strategy": "Promise loop + setTimeout backoff",
            "mechanism": "Basic retry: recursive async function with counter. "
                        "No stdlib retry; popular pattern uses recursive Promise.",
            "idiom": "async function retry(fn, maxRetries = 3) { "
                    "for (let i = 0; i < maxRetries; i++) { "
                    "try { return await fn() } catch (e) { if (i === maxRetries - 1) throw e; "
                    "await new Promise(r => setTimeout(r, 100 * 2 ** i)) } } }",
            "key_traits": ["recursive Promise retry", "exponential backoff via setTimeout",
                           "no retry stdlib", "Promise rejection for final failure"],
            "resilience_tag": "RUNTIME",
            "emoji": "🟨",
        },
        "degrade": {
            "strategy": "null + default values + event emitter for stale data",
            "mechanism": "JS degrades by returning null or a stale cached object. "
                        "No type-level degradation signal. "
                        "Event emitters announce degraded mode.",
            "idiom": "const staleData = cache.get() || { data: null, degraded: true }",
            "key_traits": ["null as degradation signal", "|| for default values",
                           "EventEmitter for degraded announcements", "no Option type"],
            "resilience_tag": "RUNTIME",
            "emoji": "🟨",
        },
        "circuit": {
            "strategy": "opossum / brake (npm packages)",
            "mechanism": "JavaScript's circuit breaker is entirely in the npm ecosystem. "
                        "opossum and brake are popular choices.",
            "idiom": "const brake = require('brake'); async function call() { "
                    "return brake(() => risky(), { threshold: 3, timeout: 5000 }); }",
            "key_traits": ["npm packages only", "opossum and brake available",
                           "runtime-only circuit tracking", "no language-level support"],
            "resilience_tag": "BUILTIN",
            "emoji": "🟨",
        },
        "resurrect": {
            "strategy": "Module reloading via require('refresh') or new instance",
            "mechanism": "Node.js module cache can be cleared: `delete require.cache[require.resolve('./mod')]`. "
                        "Or: design services as classes, instantiate fresh on error.",
            "idiom": "const key = require.resolve('./db'); delete require.cache[key]; const DB = require('./db')",
            "key_traits": ["module cache invalidation", "class instance recreation",
                           "no automatic restart", "process.on('uncaughtException')"],
            "resilience_tag": "RUNTIME",
            "emoji": "🟨",
        },
    },

    "Java": {
        "model": {
            "strategy": "checked + unchecked exceptions + throws clause",
            "mechanism": "Checked exceptions must be declared in method signature. "
                        "Compiler enforces handling (catch or declare). "
                        "Unchecked exceptions (RuntimeException) are not enforced.",
            "idiom": "public void read() throws IOException { ... } // caller MUST handle",
            "key_traits": ["compiler-enforced checked exceptions", "throws in signature",
                           "finally for cleanup", "try-with-resources for AutoCloseable"],
            "resilience_tag": "PROVEN",
            "emoji": "☕",
        },
        "retry": {
            "strategy": "for loop + Thread.sleep + Spring Retry (@Retryable)",
            "mechanism": "Manual: `for (int i=0; i<maxRetries; i++) { try { return call(); } catch { if (i==maxRetries-1) throw; Thread.sleep(backoff); } }`. "
                        "Spring Retry annotates methods: `@Retryable(maxAttempts=3)`.",
            "idiom": "@Retryable(value = IOException.class, maxAttempts = 3, backoff = @Backoff(delay = 1000))",
            "key_traits": ["Spring @Retryable annotation", "exponential backoff via @Backoff",
                           "manual loop for simple cases", "retry on specific exception types"],
            "resilience_tag": "PROVEN",
            "emoji": "☕",
        },
        "degrade": {
            "strategy": "null + Optional<T> + default object pattern",
            "mechanism": "Java degrades via null or Optional.ofNullable. "
                        "FalloffData pattern: a degraded response object with default values. "
                        "Optional: `data.orElse(StaleData.default())`.",
            "idiom": "Optional<Data> cached = Optional.ofNullable(cache.get(id)); "
                    "Data display = cached.orElse(Data.fallback());",
            "key_traits": ["Optional<T> for null safety", "null as degradation",
                           "orElse for default fallback", "empty object pattern"],
            "resilience_tag": "PROVEN",
            "emoji": "☕",
        },
        "circuit": {
            "strategy": "Resilience4j (standard JVM circuit breaker)",
            "mechanism": "Resilience4j is the JVM standard: "
                        "`CircuitBreaker.of('my-service', CircuitBreakerConfig.custom()..."
                        "failureRateThreshold(50).build())`. "
                        "Spring Cloud Circuit Breaker wraps it.",
            "idiom": "CircuitBreaker breaker = CircuitBreaker.of('svc', CircuitBreakerConfig.ofDefaults()); "
                    "Supplier<String> result = breaker.executeSupplier(() -> call());",
            "key_traits": ["Resilience4j (de facto JVM standard)", "state machine: CLOSED/OPEN/HALF_OPEN",
                           "Spring Cloud Circuit Breaker wrapper", "AOP integration"],
            "resilience_tag": "PROVEN",
            "emoji": "☕",
        },
        "resurrect": {
            "strategy": "Thread restart + ExecutorService supervision",
            "mechanism": "Java virtual threads (Java 21+): a crashed virtual thread "
                        "can be restarted by the executor. "
                        "ExecutorService.submit() re-creates the task on a fresh thread.",
            "idiom": "ExecutorService ex = Executors.newVirtualThreadPerTaskExecutor(); "
                    "Future<?> f = ex.submit(() -> { if (failed) throw new RuntimeException(); });",
            "key_traits": ["Virtual threads for cheap restart", "ExecutorService supervision",
                           "Thread.UncaughtExceptionHandler", "no automatic restart without supervisor"],
            "resilience_tag": "PROVEN",
            "emoji": "☕",
        },
    },

    "C/C++": {
        "model": {
            "strategy": "return codes (C) | exceptions (C++) | no enforcement",
            "mechanism": "C: return codes + errno. No enforcement. Programmer must check. "
                        "C++: exceptions available but discouraged in performance code. "
                        "No garbage collector, no safety net.",
            "idiom": "int fd = open(path, O_RDONLY); if (fd < 0) { perror(\"open\"); return errno; }",
            "key_traits": ["manual error checking", "errno is global state",
                           "no exception safety without RAII", "undefined behavior on misuse"],
            "resilience_tag": "RUNTIME",
            "emoji": "⚙️",
        },
        "retry": {
            "strategy": "Manual goto loop + nanosleep",
            "mechanism": "C retry pattern uses a `retry:` label with goto: "
                        "`retry: result = call(); if (result == -1 && errno == EINTR) goto retry;`. "
                        "C++ uses a for loop with exponential backoff.",
            "idiom": "for (int attempt = 0; attempt < MAX_RETRIES; attempt++) { "
                    "int r = connect(); if (r == 0) break; "
                    "struct timespec ts = { .tv_sec = 0, .tv_nsec = 100000000L * (1 << attempt) }; "
                    "nanosleep(&ts, NULL); }",
            "key_traits": ["goto retry pattern (C)", "nanosleep for backoff (C)",
                           "for loop retry (C++)", "no stdlib retry"],
            "resilience_tag": "RUNTIME",
            "emoji": "⚙️",
        },
        "degrade": {
            "strategy": "NULL return + errno + fallback function pointer",
            "mechanism": "C degrades by returning NULL (errno set) or by invoking "
                        "a user-supplied fallback function registered at startup.",
            "idiom": "void (*fallback_handler)(void) = NULL; "
                    "void set_fallback(void (*f)(void)) { fallback_handler = f; }",
            "key_traits": ["NULL as degradation signal", "errno for error category",
                           "function pointer fallback registration", "struct with status field"],
            "resilience_tag": "RUNTIME",
            "emoji": "⚙️",
        },
        "circuit": {
            "strategy": "Manual state machine — no stdlib circuit breaker",
            "mechanism": "C/C++ requires hand-rolled circuit breaker: "
                        "a struct with enum { CLOSED, OPEN, HALF_OPEN } tracking failure counts. "
                        "No standard library support. Libraries exist (e.g. libqb).",
            "idiom": "typedef enum { CB_CLOSED, CB_OPEN, CB_HALF_OPEN } cb_state_t; "
                    "typedef struct { cb_state_t state; int failures; time_t open_until; } cb_t; "
                    "int cb_call(cb_t *cb, int (*fn)(void)) { "
                    "  if (cb->state == CB_OPEN && time(NULL) < cb->open_until) return -1; "
                    "  int r = fn(); if (r != 0) { cb->failures++; if (cb->failures > 3) cb->state = CB_OPEN; } else { cb->state = CB_CLOSED; cb->failures = 0; } return r; }",
            "key_traits": ["manual state machine", "no stdlib support",
                           "struct-based circuit state", "timer-based half-open transition"],
            "resilience_tag": "MANUAL",
            "emoji": "⚙️",
        },
        "resurrect": {
            "strategy": "Resource re-acquisition via RAII + explicit cleanup",
            "mechanism": "C: re-call open()/connect() after failure. "
                        "C++: RAII destructors called on scope exit. "
                        "Smart pointers (std::unique_ptr) auto-release. "
                        "No self-healing — explicit restart code required.",
            "idiom": "std::unique_ptr<FILE, decltype(&fclose)> fp(fopen(\"data\", \"r\"), fclose); "
                    "if (!fp) { fp.reset(fopen(\"fallback\", \"r\")); }",
            "key_traits": ["unique_ptr for RAII cleanup", "explicit re-acquisition",
                           "no automatic restart", "destructor fires on scope exit"],
            "resilience_tag": "RUNTIME",
            "emoji": "⚙️",
        },
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Resilience strength classification
# ─────────────────────────────────────────────────────────────────────────────

def classify_resilience_tag(tag: str) -> str:
    """Classify the rigor of a recovery/resilience model."""
    mapping = {
        "PROVEN":  "compile-time proven — compiler enforces correct recovery",
        "NOMINAL": "compile-time enforced — checked return values",
        "ADAPTED": "runtime + library — standard patterns via ecosystem",
        "BUILTIN": "library-level — circuit breaker via ecosystem packages",
        "MANUAL":  "manual only — no language or stdlib support",
        "RUNTIME": "runtime only — no compile-time enforcement",
    }
    return mapping.get(tag, "unknown")


# ─────────────────────────────────────────────────────────────────────────────
# Core API
# ─────────────────────────────────────────────────────────────────────────────

def _load_rotation(config_path: Optional[str] = None) -> Dict[str, Any]:
    path = config_path if config_path is not None else ROTATION_FILE
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_rotation(data: Dict[str, Any], config_path: Optional[str] = None) -> None:
    path = config_path if config_path is not None else ROTATION_FILE
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def get_current_language(config_path: Optional[str] = None) -> str:
    """Return the language at current_index."""
    data = _load_rotation(config_path)
    idx = data.get("current_index", 0)
    return data["languages"][idx % len(data["languages"])]


def advance_rotation(config_path: Optional[str] = None) -> str:
    """Advance index, save, return the language we just finished with."""
    data = _load_rotation(config_path)
    langs = data["languages"]
    old_idx = data["current_index"]
    new_idx = (old_idx + 1) % len(langs)
    data["current_index"] = new_idx
    data["last_language"] = langs[old_idx]
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    _save_rotation(data, config_path)
    return langs[old_idx]


def get_recovery_map(language: str) -> Dict[str, Dict[str, Any]]:
    """Return the full recovery taxonomy for a language."""
    return RECOVERY_DB.get(language, {})


def get_recovery_comparison(language: str) -> Dict[str, Any]:
    """Build a cross-language comparison of recovery dimensions for a given language."""
    my_recovery = RECOVERY_DB.get(language, {})

    comparison = {}
    for dim in ("model", "retry", "degrade", "circuit", "resurrect"):
        my_dim = my_recovery.get(dim, {})
        row = {
            "source_language": language,
            "source_strategy": my_dim.get("strategy", "?"),
            "source_tag": my_dim.get("resilience_tag", "?"),
        }
        for other in ROTATION_ORDER:
            if other == language:
                continue
            other_dim = RECOVERY_DB.get(other, {}).get(dim, {})
            row[other] = {
                "strategy": other_dim.get("strategy", "?"),
                "tag": other_dim.get("resilience_tag", "?"),
                "rigor": classify_resilience_tag(other_dim.get("resilience_tag", "?")),
            }
        comparison[dim] = row
    return comparison


def generate_recovery_report(
    rotate: bool = True,
    config_path: Optional[str] = None,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Generate a recovery resilience report for the current rotation language.

    Args:
        rotate: advance rotation after generating
        config_path: optional path to language_rotation.json
        seed: optional seed (unused, for API compatibility)

    Returns:
        full recovery report dict
    """
    data = _load_rotation(config_path)
    langs = data["languages"]
    old_idx = data["current_index"]

    current_language = langs[old_idx]
    new_idx = (old_idx + 1) % len(langs)

    if rotate:
        data["current_index"] = new_idx
        data["last_language"] = current_language
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        _save_rotation(data, config_path)

    recovery = get_recovery_map(current_language)
    comparison = get_recovery_comparison(current_language)

    categories = []
    for dim, info in recovery.items():
        categories.append({
            "dimension": dim,
            "strategy": info.get("strategy", "?"),
            "mechanism": info.get("mechanism", ""),
            "idiom": info.get("idiom", ""),
            "key_traits": info.get("key_traits", []),
            "resilience_tag": info.get("resilience_tag", "?"),
            "emoji": info.get("emoji", "🔧"),
            "rigor": classify_resilience_tag(info.get("resilience_tag", "?")),
        })

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": current_language,
        "current_index": old_idx,
        "new_index": new_idx if rotate else None,
        "rotated": rotate,
        "recovery_dimensions": categories,
        "cross_language_comparison": comparison,
        "rotation_order": ROTATION_ORDER,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def format_recovery_report(m: Dict[str, Any]) -> str:
    """Format the recovery report as a human-readable string."""
    lang = m["language"]
    dims = m["recovery_dimensions"]

    tag_legend = {
        "PROVEN":  "🛡️ PROVEN  — compile-time enforced",
        "NOMINAL": "⚡ NOMINAL — compile-time checked",
        "ADAPTED": "🟣 ADAPTED — runtime + ecosystem libs",
        "BUILTIN": "📦 BUILTIN — ecosystem circuit breaker",
        "MANUAL":  "⚙️ MANUAL  — hand-rolled only",
        "RUNTIME": "⚙️ RUNTIME — runtime only",
    }

    dim_labels = {
        "model":    "RECOVERY MODEL",
        "retry":    "RETRY MECHANISM",
        "degrade":  "GRACEFUL DEGRADATION",
        "circuit":  "CIRCUIT BREAKER",
        "resurrect": "RESURRECTION",
    }

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  🔧 POLYGLOT RECOVERY — Resilience Cartography                   ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Language : {lang:<48}║",
        f"║  Index    : {m['current_index']:<48}║",
        f"║  Rotated  : {str(m['rotated']):<48}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  RECOVERY DIMENSIONS                                            ║",
    ]

    for dim in dims:
        emoji = dim["emoji"]
        label = dim_labels.get(dim["dimension"], dim["dimension"].upper())
        lines.append(
            f"║  {emoji} {label:<8}: {dim['strategy']:<38}║"
        )
        lines.append(
            f"║              [{dim['resilience_tag']}] {classify_resilience_tag(dim['resilience_tag']):<35}║"
        )
        if dim["idiom"]:
            idiom_short = dim["idiom"][:60].replace("\n", " ")
            lines.append(f"║              💬 {idiom_short:<44}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  TAG LEGEND                                                     ║",
    ]
    for tag, desc in tag_legend.items():
        lines.append(f"║  {desc:<58}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  CROSS-LANGUAGE COMPARISON                                      ║",
    ]

    for dim, row in m["cross_language_comparison"].items():
        label = dim_labels.get(dim, dim.upper())
        lines.append(f"║  ── {label:<57}║")
        lines.append(f"║    My strategy: {row['source_strategy']:<41}║")
        others = [k for k in row if k not in ("source_language", "source_strategy", "source_tag")]
        others_str = ", ".join(
            f"{k}({row[k]['strategy'][:12]})" for k in others
        )
        lines.append(f"║    Others    : {others_str:<46}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  KEY TRAITS                                                     ║",
    ]
    for dim in dims:
        label = dim_labels.get(dim["dimension"], dim["dimension"].upper())
        for trait in dim["key_traits"][:3]:
            lines.append(f"║  {dim['emoji']} {label:<8}: {trait:<42}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🔄 ROTATION ORDER                                               ║",
        f"║  {' → '.join(ROTATION_ORDER):<58}║",
        "╚══════════════════════════════════════════════════════════════════╝",
    ]
    return "\n".join(lines)


def run_tests() -> None:
    """Run all tests and exit."""
    import pytest
    import sys
    sys.exit(pytest.main([str(Path(__file__).parent.parent / "tests"), "-v"]))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        report = generate_recovery_report()
        print(format_recovery_report(report))
    else:
        print(f"Polyglot Recovery v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_recovery --test   # Run tests")
        print("  python -m polyglot_recovery --report # Generate recovery report")