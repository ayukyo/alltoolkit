#! /usr/bin/env python3
"""
⚔️ Polyglot Gauntlet — Core Implementation v1.0
"""

import json
import os
import random
import re
import sys
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-gauntlet"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent          # polyglot_gauntlet/
_WORKSPACE_ROOT = _MODULE_DIR.parent.parent        # AllToolkit/ -> workspace/
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ── Gauntlet challenges per language ─────────────────────────────────────────
# Each gauntlet is the canonical "rite of passage" for that language.
# NOT algorithmic puzzles — language-specific demonstrations of mastery.

GAUNTLET_DATA: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "name": "The Ownership Marathon",
        "challenge": (
            "Implement a simple arena allocator (bump allocator) in safe Rust. "
            "The arena owns a pre-allocated buffer and hands out borrows to objects "
            "stored within it. All borrows must outlive the arena — prove it through "
            "the type system. Then implement Drop to free the arena."
        ),
        "difficulty": "★★★★☆",
        "time_estimate": "45–90 min",
        "skills_tested": [
            "Lifetime annotations",
            "Zero-cost abstractions",
            "Unsafe (optional for performance)",
            "RAII and Drop",
            "Slice and buffer unsizing",
        ],
        "success_criteria": [
            "Arena struct holds a Vec<u8> and a cursor",
            "arena.alloc<T>(&mut self, value: T) -> &mut T borrows from the arena",
            "All returned references are tied to the arena's lifetime",
            "Drop impl releases the buffer",
            "Code compiles with zero warnings under cargo clippy",
        ],
        "failure_modes": [
            "Leaking memory by cloning instead of borrowing into the arena",
            "Returning references to temporary values",
            "Missing lifetime annotations that the compiler would catch",
            "Unnecessary use of unsafe when safe code suffices",
        ],
        "mastery_quote": (
            "You don't fight the borrow checker. You restructure your API until "
            "the borrow checker agrees that your design is sound."
        ),
        "hints": [
            "Start with a simple bump index. The arena owns a Vec<u8> and a position cursor.",
            "Use a trait object or enum to store heterogeneous values in the arena.",
            "The key insight: arena.alloc() borrows self mutably and returns &mut T — lifetime elided.",
            "The Drop trait is your friend. The arena cleans up when it goes out of scope.",
        ],
        "starter_template": '''use std::mem;

/// A bump allocator — pre-allocates a buffer and hands out references.
pub struct Arena {
    /// The underlying memory buffer.
    buffer: Vec<u8>,
    /// Current write position (bytes used).
    cursor: usize,
}

impl Arena {
    pub fn new(capacity: usize) -> Self {
        Arena {
            buffer: vec![0u8; capacity],
            cursor: 0,
        }
    }

    /// Allocate a value of type T inside the arena.
    /// Returns a mutable reference to the allocated value.
    /// The lifetime 'a ties the returned reference to the arena itself.
    pub fn alloc<T>(&mut self, value: T) -> &mut T {
        let align = mem::align_of::<T>();
        let size = mem::size_of::<T>();

        // Round cursor up to the next alignment boundary
        self.cursor = (self.cursor + align - 1) & !(align - 1);

        // ... your code here: write value into buffer, advance cursor, return reference
        unimplemented!("bump the cursor, write value into buffer, return &mut T")
    }
}

// ── tests ────────────────────────────────────────────────────────────────────
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_compiles() {
        let mut arena = Arena::new(1024);
        let x = arena.alloc(42i32);
        assert_eq!(*x, 42);
    }

    #[test]
    fn references_outlive_arena() {
        let mut arena = Arena::new(1024);
        let reference: &mut i32;
        {
            reference = arena.alloc(100i32);
        }
        // 'reference' is still valid here — tied to arena's lifetime
        assert_eq!(*reference, 100);
    }

    #[test]
    fn multiple_allocations() {
        let mut arena = Arena::new(1024);
        let a = arena.alloc(1.0f64);
        let b = arena.alloc(2.0f64);
        let c = arena.alloc(3u64);
        assert_eq!(*a, 1.0);
        assert_eq!(*b, 2.0);
        assert_eq!(*c, 3u64);
    }
}''',
    },
    "Go": {
        "name": "The Goroutine Symphony",
        "challenge": (
            "Build a worker pool from scratch in Go. N workers pull jobs from a "
            "channel, process them concurrently, and send results to a results channel. "
            "Include graceful shutdown: send a stop signal, wait for all workers to "
            "finish their current job, then exit. No goroutine leaks allowed."
        ),
        "difficulty": "★★★☆☆",
        "time_estimate": "30–60 min",
        "skills_tested": [
            "Goroutines and channels",
            "select statements and non-blocking receives",
            "context.Context for cancellation",
            "sync.WaitGroup for graceful shutdown",
            "Buffered vs unbuffered channels",
        ],
        "success_criteria": [
            "Pool creates exactly N goroutines on startup",
            "Jobs are distributed across workers (load balanced)",
            "Calling stop() blocks until all workers have finished",
            "runtime.NumGoroutine() returns to baseline after shutdown",
            "context.Context cancel propagates to all workers",
        ],
        "failure_modes": [
            "Goroutines blocked on channel send/receive after shutdown (leak)",
            "Not handling slow jobs that outlive the shutdown signal",
            "Race conditions between job channel and stop signal",
            "Silent swallowing of context cancellation",
        ],
        "mastery_quote": (
            "Goroutines are cheap. Goroutine leaks are expensive. "
            "The WaitGroup is not optional — it's the difference between "
            "a clean shutdown and a haunted process."
        ),
        "hints": [
            "Use sync.WaitGroup.Add(N) before launching goroutines.",
            "A 'done' channel closed by the pool signals workers to exit.",
            "Use a select with a default case to implement non-blocking shutdown checking.",
            "context.WithCancel gives each worker a cancel function they defer-cancel in.",
        ],
        "starter_template": '''package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

type Job struct {
    ID   int
    Data string
}

type Result struct {
    JobID  int
    Output string
    Err   error
}

type WorkerPool struct {
    jobs    chan Job
    results chan Result
    done    chan struct{}
    wg      sync.WaitGroup
}

// NewWorkerPool creates a pool with n workers.
func NewWorkerPool(n int, buffer int) *WorkerPool {
    wp := &WorkerPool{
        jobs:    make(chan Job, buffer),
        results: make(chan Result, buffer),
        done:    make(chan struct{}),
    }
    // TODO: start n workers here
    // wp.wg.Add(n)
    // for i := 0; i < n; i++ {
    //     go wp.worker(i)
    // }
    return wp
}

// Submit adds a job to the queue. Returns false if the pool is stopped.
func (wp *WorkerPool) Submit(ctx context.Context, job Job) bool {
    select {
    case wp.jobs <- job:
        return true
    case <-ctx.Done():
        return false
    case <-wp.done:
        return false
    }
}

// Stop gracefully shuts down the pool.
// It waits for all in-progress jobs to complete.
func (wp *WorkerPool) Stop() {
    // TODO: signal workers to stop, wait for them
    close(wp.done)
    wp.wg.Wait()
}

func (wp *WorkerPool) worker(id int) {
    defer wp.wg.Done()
    for {
        select {
        case job := <-wp.jobs:
            // process job
            result := Result{JobID: job.ID, Output: fmt.Sprintf("worker-%d: processed %s", id, job.Data)}
            wp.results <- result
        case <-wp.done:
            fmt.Printf("worker-%d: exiting\\n", id)
            return
        }
    }
}

func main() {
    pool := NewWorkerPool(3, 10)
    ctx := context.Background()

    for i := 0; i < 5; i++ {
        pool.Submit(ctx, Job{ID: i, Data: fmt.Sprintf("task-%d", i)})
    }

    time.Sleep(100 * time.Millisecond)
    pool.Stop()
    fmt.Println("Pool stopped cleanly")
}''',
    },
    "Swift": {
        "name": "The Actor Isolation",
        "challenge": (
            "Model a bank account as a Swift actor. Multiple actors (ATMs, "
            "bank tellers, mobile apps) transfer money between accounts concurrently. "
            "Implement transfer(amount:to:) as a composable operation and prove that "
            "the balance is always consistent — no race conditions, no overdrafts."
        ),
        "difficulty": "★★★★☆",
        "time_estimate": "45–75 min",
        "skills_tested": [
            "Swift 6 actor isolation",
            "async/await",
            "Sendable conformance",
            "Data race safety at compile time",
        ],
        "success_criteria": [
            "BankAccount is an actor with a balance property",
            "transfer(to:amount:) uses isolatd(self) and isolated(to:) to atomically move money",
            "Code compiles in Swift 6 mode with zero isolation warnings",
            "Concurrent transfers never produce negative balances",
            "Actor is marked Sendable, Balance is Sendable",
        ],
        "failure_modes": [
            "Sharing mutable state across actors without Sendable",
            "Transfer operation not being atomic (interleaving with another transfer)",
            "Using class instead of actor for the account",
            "Forgetting to make Balance Sendable",
        ],
        "mastery_quote": (
            "If it compiles in Swift 6, it's data-race free. "
            "If it doesn't compile, the compiler is saving you from yourself."
        ),
        "hints": [
            "Use isolated(to:) on the destination account to ensure two accounts "
            "are locked in a deterministic order to prevent deadlocks.",
            "Make sure the transfer checks 'from.balance >= amount' atomically.",
            "Balance should be a simple struct (Int or Decimal) marked Sendable.",
            "In Swift 6, non-Sendable types can't cross actor boundaries.",
        ],
        "starter_template": '''import Foundation

// A simple Sendable struct representing a monetary amount
struct Money: Sendable {
    let amount: Int  // in cents
    static let zero = Money(amount: 0)
}

// A bank account — actor ensures exclusive access to balance
actor BankAccount: Sendable {
    let id: String
    var balance: Money

    init(id: String, initialBalance: Money) {
        self.id = id
        self.balance = initialBalance
    }

    /// Transfer money from this account to another account.
    /// The transfer is atomic — no race conditions possible.
    func transfer(to destination: isolated BankAccount, amount: Money) async -> Bool {
        // TODO: check balance, debit self, credit destination, return true/false
        // Hint: use 'isolated(destination)' on destination
        // The order of isolation matters for deadlock prevention
        // Hint: always debit before credit, and check balance atomically
        return false
    }

    func deposit(amount: Money) {
        balance = Money(amount: balance.amount + amount.amount)
    }

    func withdraw(amount: Money) -> Bool {
        if balance.amount >= amount.amount {
            balance = Money(amount: balance.amount - amount.amount)
            return true
        }
        return false
    }
}

// MARK: - Tests
func testTransfer() async {
    let accountA = BankAccount(id: "A", initialBalance: Money(amount: 1000))
    let accountB = BankAccount(id: "B", initialBalance: Money(amount: 500))

    let success = await accountA.transfer(to: accountB, amount: Money(amount: 300))

    print("Transfer success: \\(success)")
    // Expected: balance A = 700, balance B = 800
}

Task {
    await testTransfer()
}''',
    },
    "Kotlin": {
        "name": "The Coroutine Flow Battle",
        "challenge": (
            "Build a real-time event stream in Kotlin using Flow. "
            "A flow emits stock price updates. Build a pipeline that: "
            "(1) throttles updates to max 1 per second, "
            "(2) emits only when price changes by >1%, "
            "(3) combines with a 'news sentiment' flow, "
            "(4) emits alerts when both price and sentiment agree on a trend."
        ),
        "difficulty": "★★★★☆",
        "time_estimate": "40–70 min",
        "skills_tested": [
            "Kotlin coroutines and Flow",
            "StateIn / SharedFlow",
            "Flow operators: map, filter, debounce, combine, zip",
            "Backpressure",
            "Cold vs hot flows",
        ],
        "success_criteria": [
            "Price flow emits at most once per second (debounce/throttleFirst)",
            "Price flow only emits when |delta| > 1%",
            "Combined flow merges price and sentiment in real-time",
            "Alert is emitted only when both signals agree",
            "Flow cancels cleanly when the coroutine scope is cancelled",
        ],
        "failure_modes": [
            "Using a blocking Thread.sleep() inside a flow builder",
            "Forgetting backpressure handling (buffer overflow)",
            "Not making the flows hot (StateIn) when shared",
            "Combining flows that have different collection scopes",
        ],
        "mastery_quote": (
            "Flow is not a collection. It's a recipe for producing values "
            "over time. The collector decides when to start cooking."
        ),
        "hints": [
            "Use flow { emit(...) } for the price emitter and flowOf() or callbackFlow for news.",
            "debounce(1_000L) to throttle to once per second.",
            "filter { old, new -> abs(new - old) / old > 0.01 } for the 1% change filter.",
            "combine(flowA, flowB) { price, sentiment -> ... } to merge two flows.",
        ],
        "starter_template": '''import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

data class StockPrice(val symbol: String, val price: Double, val timestamp: Long)
enum class Sentiment { BULLISH, BEARISH, NEUTRAL }
data class Alert(val message: String, val price: StockPrice, val sentiment: Sentiment)

fun main() = runBlocking<Unit> {
    // Simulated stock price stream
    val priceFlow = flow {
        val prices = listOf(100.0, 101.5, 102.3, 98.7, 97.5, 103.0, 104.2, 105.0)
        for (price in prices) {
            emit(StockPrice("AAPL", price, System.currentTimeMillis()))
            delay(300) // emit every 300ms
        }
    }

    // Simulated news sentiment stream
    val sentimentFlow = flowOf(
        Sentiment.BULLISH, Sentiment.BEARISH, Sentiment.NEUTRAL, Sentiment.BULLISH,
        Sentiment.BULLISH, Sentiment.NEUTRAL, Sentiment.BULLISH, Sentiment.BEARISH
    ).onEach { delay(400) }

    // TODO: Build the pipeline
    // 1. Throttle to 1 update per second (debounce or throttleFirst)
    // 2. Filter for >1% price change
    // 3. Combine with sentiment
    // 4. Emit alerts when both signals agree

    val alerts = priceFlow
        // .debounce(1000L)
        // .filter { ... }  // >1% change
        // .combine(sentimentFlow) { price, sentiment -> ... }
        // .filter { (price, sentiment) -> ... }  // signals agree

    alerts.collect { alert ->
        println("🚨 ALERT: ${alert.message}")
    }
}''',
    },
    "TypeScript": {
        "name": "The Type-Safe State Machine",
        "challenge": (
            "Model a TCP connection state machine in TypeScript using discriminated "
            "unions. The states are: Closed, Opening, Open(sendQueue), Closing, "
            "Error(reason). Transitions are only valid from specific states. "
            "Use the type system to make illegal state transitions impossible at "
            "compile time, not just at runtime."
        ),
        "difficulty": "★★★★☆",
        "time_estimate": "35–60 min",
        "skills_tested": [
            "Discriminated unions / algebraic data types in TypeScript",
            "Exhaustive switch narrowing",
            "TypeScript's never type for exhaustiveness",
            "State machine pattern with type-level enforcement",
        ],
        "success_criteria": [
            "All 5 states are represented as distinct types in a discriminated union",
            "Invalid transitions produce compile errors (type errors, not runtime)",
            "Exhaustive switch statement covers all states with no default case",
            "The sendQueue in Open state is typed correctly",
            "TypeScript's strict mode passes with zero errors",
        ],
        "failure_modes": [
            "Using string literals for states instead of distinct types",
            "Allowing transitions from any state to any state",
            "Missing a state in the switch (no exhaustiveness check)",
            "Using any or unknown without proper narrowing",
        ],
        "mastery_quote": (
            "If it compiles, the state machine is correct. "
            "The type system is the spec. If it compiles, your invariants hold."
        ),
        "hints": [
            "Use an interface with a 'kind' discriminant: type Connection = Closed | Opening | ...",
            "Define validTransitions as a mapping of State -> Array<valid next states>.",
            "Use a type-safe transition function that narrows states explicitly.",
            "The 'never' type in the default case of a switch makes missing cases a compile error.",
        ],
        "starter_template": '''// ── TCP Connection State Machine ─────────────────────────────────────────────

type ConnectionState =
  | { kind: 'closed' }
  | { kind: 'opening' }
  | { kind: 'open'; sendQueue: string[] }
  | { kind: 'closing' }
  | { kind: 'error'; reason: string };

// ── Transition function ──────────────────────────────────────────────────────
// TODO: implement a type-safe transition function
// Valid transitions:
//   Closed → Opening (connect)
//   Opening → Open (connection established)
//   Opening → Error (connection refused)
//   Open → Closing (initiate close)
//   Open → Error (network failure)
//   Closing → Closed (clean disconnect)
//   Error → Closed (reset)

type TransitionResult =
  | { success: true; state: ConnectionState }
  | { success: false; reason: string };

function transition(state: ConnectionState, event: string): TransitionResult {
  switch (state.kind) {
    case 'closed':
      if (event === 'connect') return { success: true, state: { kind: 'opening' } };
      break;
    // TODO: implement all valid transitions
    default:
      // This should NOT compile if we missed a state
      const _exhaustive: never = state;
  }
  return { success: false, reason: `Invalid transition: ${state.kind} + ${event}` };
}

// ── Tests ───────────────────────────────────────────────────────────────────
const closed: ConnectionState = { kind: 'closed' };
const opening: ConnectionState = { kind: 'opening' };
const open: ConnectionState = { kind: 'open', sendQueue: [] };
const closing: ConnectionState = { kind: 'closing' };
const errorState: ConnectionState = { kind: 'error', reason: 'ETIMEDOUT' };

// These should compile (valid transitions)
const r1 = transition(closed, 'connect');    // → Opening
const r2 = transition(opening, 'established'); // → Open
const r3 = transition(open, 'close');         // → Closing
const r4 = transition(closing, 'closed');     // → Closed
const r5 = transition(opening, 'refused');    // → Error

// This should NOT compile (invalid transition)
// const bad = transition(closed, 'established'); // Error: Type '{ kind: "closed" }' has no property...

// ── Exhaustive handler ──────────────────────────────────────────────────────
function describe(state: ConnectionState): string {
  switch (state.kind) {
    case 'closed':    return 'Connection is closed';
    case 'opening':   return 'Connection is opening...';
    case 'open':      return `Open (${state.sendQueue.length} queued)`;
    case 'closing':   return 'Connection is closing...';
    case 'error':     return `Error: ${state.reason}`;
    default:
      const _never: never = state;
      return _never;
  }
}

console.log(describe(open));''',
    },
    "JavaScript": {
        "name": "The Prototype Chain Oracle",
        "challenge": (
            "Implement a mini OOP system using raw JavaScript prototypes — "
            "no class keyword, no ES6 classes. Build a Vehicle base class, "
            "a Car subclass that adds wheels and drive(), and a Tesla subclass "
            "that overrides drive() to add autopilot. Then implement a "
            "mixin system for Flyable and Chargeable that works with any "
            "prototype chain."
        ),
        "difficulty": "★★★☆☆",
        "time_estimate": "30–50 min",
        "skills_tested": [
            "JavaScript prototype chain",
            "Object.create() for inheritance",
            "hasOwnProperty and property enumeration",
            "Mixins without class syntax",
            "The difference between __proto__ and prototype",
        ],
        "success_criteria": [
            "Vehicle, Car, and Tesla use only Object.create() and manual property assignment",
            "No class keyword anywhere in the solution",
            "Flyable and Chargeable mixins are composable with any class",
            "instanceof-like checks work correctly across the chain",
            "Constructor property is correctly set on all objects",
        ],
        "failure_modes": [
            "Using class syntax (class Car extends Vehicle {})",
            "Mixins not properly copying properties (using reference sharing instead)",
            "Not properly setting the constructor property on the subclass prototype",
            "Confusing __proto__ (instance) with .prototype (class)",
        ],
        "mastery_quote": (
            "The prototype chain is not a polyfill for classes. "
            "It's a fundamentally different inheritance mechanism — "
            "one where objects delegate to other objects directly."
        ),
        "hints": [
            "Use Vehicle.prototype and Object.create(Car.prototype) for subclassing.",
            "The mixin function should iterate over own properties and copy them.",
            "Set SubClass.prototype.constructor = SubClass after Object.create.",
            "Use Vehicle.call(this, ...) in the Car constructor for proper initialization.",
        ],
        "starter_template": '''// ── Vehicle (base class) — using prototypes only ─────────────────────────────
function Vehicle(make, model) {
  this.make = make;
  this.model = model;
  this.speed = 0;
}

Vehicle.prototype.drive = function(speed) {
  this.speed = speed;
  return `${this.make} ${this.model} driving at ${speed}mph`;
};

Vehicle.prototype.stop = function() {
  this.speed = 0;
  return `${this.make} ${this.model} stopped`;
};

// ── Car (subclass) — prototype chain ───────────────────────────────────────
function Car(make, model, doors) {
  // TODO: call Vehicle constructor
}

Car.prototype = Object.create(Vehicle.prototype);
// TODO: fix the constructor property
Car.prototype.constructor = Car;

Car.prototype.drive = function(speed) {
  return Vehicle.prototype.drive.call(this, speed) + ` (${this.doors}-door)`;
};

// ── Mixins ──────────────────────────────────────────────────────────────────
const Flyable = {
  fly: function(altitude) {
    return `${this.make} ${this.model} flying at ${altitude}ft`;
  }
};

const Chargeable = {
  charge: function() {
    return `${this.make} ${this.model} charging...`;
  }
};

// ── Tesla (subclass with mixins) ────────────────────────────────────────────
function Tesla(model, doors) {
  Car.call(this, 'Tesla', model, doors);
  this.battery = 100;
}

Tesla.prototype = Object.create(Car.prototype);
Tesla.prototype.constructor = Tesla;

Tesla.prototype.drive = function(speed) {
  return Car.prototype.drive.call(this, speed) + ' [autopilot]';
};

// Apply mixins
Object.assign(Tesla.prototype, Flyable, Chargeable);

// ── Tests ───────────────────────────────────────────────────────────────────
const v = new Vehicle('Generic', 'Car');
const c = new Car('Toyota', 'Camry', 4);
const t = new Tesla('Model S', 4);

console.log(v.drive(60));      // Generic Car driving at 60mph
console.log(c.drive(60));      // Toyota Camry driving at 60mph (4-door)
console.log(t.drive(70));      // Tesla Model S driving at 70mph (4-door) [autopilot]
console.log(t.fly(10000));     // Tesla Model S flying at 10000ft
console.log(t.charge());      // Tesla Model S charging...
console.log(t instanceof Car);     // true
console.log(t instanceof Vehicle); // true''',
    },
    "Java": {
        "name": "The Generic Type Safety Trial",
        "challenge": (
            "Implement a type-safe Event Bus in pure Java using generics. "
            "Subscribers declare what event type they handle: bus.subscribe(MyEvent.class, handler). "
            "The bus stores handlers in a Map<EventType, List<Consumer<? super EventType>>>. "
            "Then implement a generic type hierarchy: Event → DomainEvent → UserEvent/OrderEvent. "
            "Prove that contravariant handlers (Consumer<? super T>) correctly allow a "
            "Consumer<UserEvent> to receive UserEvent and its subclasses."
        ),
        "difficulty": "★★★★★",
        "time_estimate": "60–90 min",
        "skills_tested": [
            "Java generics: wildcards, bounds, variance",
            "Consumer<? super T> for contravariance",
            "Type erasure and how to work with it",
            "Thread safety and concurrent event dispatch",
            "Checked exceptions in generic lambdas",
        ],
        "success_criteria": [
            "subscribe() correctly registers handlers with Class<T> as key",
            "publish() uses Class<? super T> to find all applicable handlers",
            "A Consumer<? super UserEvent> can receive UserCreatedEvent (subclass)",
            "Type erasure doesn't cause ClassCastExceptions at runtime",
            "Concurrent publish calls are handled safely (CopyOnWriteArrayList)",
        ],
        "failure_modes": [
            "Using Class<T> with Consumer<T> instead of Consumer<? super T> (too restrictive)",
            "Not handling type erasure for Class objects at runtime",
            "Subscribing the same handler twice",
            "Publishing from multiple threads without synchronization",
        ],
        "mastery_quote": (
            "PECS: Producer Extends, Consumer Super. "
            "The event bus is a consumer of events — it writes to handlers. "
            "So use ? super T, not ? extends T."
        ),
        "hints": [
            "Store handlers as Map<Class<?>, List<Consumer<?>>>.",
            "On subscribe: use type.getGenericSuperclass() or pass Class<T> directly.",
            "On publish: find all handlers where handlerClass.isAssignableFrom(event.getClass()).",
            "Use CopyOnWriteArrayList for thread-safe handler storage.",
        ],
        "starter_template": '''import java.lang.reflect.ParameterizedType;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.*;

class Event {}
class DomainEvent extends Event {}
class UserEvent extends DomainEvent { public final String userId; UserEvent(String userId) { this.userId = userId; } }
class OrderEvent extends DomainEvent { public final String orderId; OrderEvent(String orderId) { this.orderId = orderId; } }
class UserCreatedEvent extends UserEvent { UserCreatedEvent(String userId) { super(userId); } }

interface Consumer<T> { void accept(T t); }

// ── Type-Safe Event Bus ─────────────────────────────────────────────────────
class EventBus {
    // TODO: Map<Class<?>, List<Consumer<?>>> — handlers keyed by event type
    private final Map<Class<?>, List<Consumer<?>>> handlers = new ConcurrentHashMap<>();

    // Subscribe a handler for a specific event type
    // Consumer<? super T> allows handling T and any supertype of T
    public <T extends Event> void subscribe(Class<T> type, Consumer<? super T> handler) {
        // TODO: register handler in the map
        // Hint: Consumer<? super T> is contravariant — a Consumer<UserEvent>
        // can accept UserCreatedEvent
    }

    // Publish an event — find all handlers where handlerType is a supertype of eventType
    public <T extends Event> void publish(T event) {
        // TODO: find all applicable handlers and call them
        // Hint: use Class.isAssignableFrom() to check handler applicability
        // Call each handler by casting to Consumer<? super T>
    }

    public int handlerCount() {
        return handlers.values().stream().mapToInt(List::size).sum();
    }
}

// ── Tests ───────────────────────────────────────────────────────────────────
public class Gauntlet {
    public static void main(String[] args) {
        EventBus bus = new EventBus();

        // A consumer that accepts any UserEvent or its supertype
        Consumer<UserEvent> userHandler = evt ->
            System.out.println("UserEvent received: " + evt.userId);

        bus.subscribe(UserEvent.class, userHandler);

        // UserCreatedEvent is a subclass of UserEvent — should work with ? super T
        bus.publish(new UserCreatedEvent("alice"));

        // OrderEvent should NOT trigger the UserEvent handler
        bus.publish(new OrderEvent("order-42"));

        System.out.println("Total handlers: " + bus.handlerCount());
        // Expected output: "UserEvent received: alice" and "Total handlers: 1"
    }
}''',
    },
    "C/C++": {
        "name": "The Manual Memory Odyssey",
        "challenge": (
            "Implement a singly-linked list in pure C (not C++) with manual "
            "malloc/free, a custom slab allocator for list nodes to avoid "
            "fragmentation, and a double-free detection system using a poison "
            "value written to freed memory. Include proper ownership semantics "
            "documentation and valgrind-clean execution."
        ),
        "difficulty": "★★★★★",
        "time_estimate": "60–120 min",
        "skills_tested": [
            "Manual memory management (malloc/calloc/free)",
            "Memory allocators (slab allocator)",
            "Poison values and double-free detection",
            "Valgrind and memory debugging",
            "Ownership semantics and API contracts",
        ],
        "success_criteria": [
            "Linked list operations (push, pop, destroy) use no more than O(1) mallocs per push",
            "Slab allocator pre-allocates a pool and hands out nodes from it",
            "Double-free of the same node is detected and reported (not segfault)",
            "Valgrind reports zero definitely lost, probably lost, and still reachable",
            "All API functions have clear ownership documentation in comments",
        ],
        "failure_modes": [
            "Memory leak (forgetting to free nodes on destroy)",
            "Double-free (freeing the same node twice — your detector should catch this)",
            "Use-after-free (accessing a node after it's been freed)",
            "Slab allocator not recycling freed nodes (always calling malloc)",
        ],
        "mastery_quote": (
            "In C, every malloc is a promise. Every free is a fulfillment. "
            "The compiler won't tell you when you break a promise — "
            "but valgrind will, if you listen."
        ),
        "hints": [
            "Define POISON_VALUE as a sentinel uint32_t written to freed memory.",
            "Check for POISON_VALUE before freeing to detect double-free.",
            "The slab allocator holds a pre-allocated block and a free list of available nodes.",
            "Store metadata (next pointer, poison check) in the node itself.",
        ],
        "starter_template": '''#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

// ── Poison value for double-free detection ──────────────────────────────────
#define POISON_VALUE 0xDEADBEEF

// ── Node structure ──────────────────────────────────────────────────────────
typedef struct Node {
    int value;
    struct Node *next;
    // TODO: add poison marker for double-free detection
} Node;

// ── Slab Allocator ───────────────────────────────────────────────────────────
typedef struct SlabAllocator {
    // TODO: pre-allocated buffer of nodes
    // TODO: free list (stack of available node indices or pointers)
    size_t capacity;
    size_t free_count;
} SlabAllocator;

SlabAllocator *slab_new(size_t capacity) {
    SlabAllocator *slab = calloc(1, sizeof(SlabAllocator));
    slab->capacity = capacity;
    slab->free_count = capacity;
    // TODO: pre-allocate the buffer and populate the free list
    return slab;
}

Node *slab_alloc(SlabAllocator *slab) {
    // TODO: pop a node from the free list and return it
    return NULL; // placeholder
}

void slab_free(SlabAllocator *slab, Node *node) {
    // TODO: push node back onto the free list
    // TODO: write poison value to detect use-after-free
}

void slab_destroy(SlabAllocator *slab) {
    // TODO: free pre-allocated buffer and the allocator itself
}

// ── Linked List with Ownership Semantics ─────────────────────────────────────
//
// list_push(slab, list, value) — takes ownership of the value's storage
// list_pop(slab, list)         — returns value; caller owns returned memory
// list_destroy(slab, list)    — frees all nodes; invalidates list
//
// Caller must NOT free nodes directly. Use list_destroy().

typedef struct List {
    Node *head;
    size_t length;
} List;

List list_new(void) {
    List list = { .head = NULL, .length = 0 };
    return list;
}

void list_push(SlabAllocator *slab, List *list, int value) {
    // TODO: allocate from slab, push to front
}

int list_pop(SlabAllocator *slab, List *list) {
    // TODO: pop from front, poison and return to slab
    return -1; // placeholder
}

void list_destroy(SlabAllocator *slab, List *list) {
    // TODO: walk list, slab_free each node
    list->head = NULL;
    list->length = 0;
}

// ── Tests ───────────────────────────────────────────────────────────────────
int main(void) {
    printf("C/C++ Gauntlet: Manual Memory Odyssey\\n");
    printf("=====================================\\n");

    SlabAllocator *slab = slab_new(10);
    List list = list_new();

    list_push(slab, &list, 10);
    list_push(slab, &list, 20);
    list_push(slab, &list, 30);

    printf("Pop: %d\\n", list_pop(slab, &list));
    printf("Pop: %d\\n", list_pop(slab, &list));
    printf("Pop: %d\\n", list_pop(slab, &list));

    // Double-free test (should be detected)
    Node *test_node = slab_alloc(slab);
    slab_free(slab, test_node);
    // slab_free(slab, test_node); // TODO: uncomment — should detect double-free

    list_destroy(slab, &list);
    slab_destroy(slab);

    printf("Run with: valgrind --leak-check=full ./%s\\n", "gauntlet");
    return 0;
}''',
    },
}


# ── Rotation helpers ──────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_current_language(config: Dict[str, Any]) -> str:
    languages = config["languages"]
    idx = config.get("current_index", 0)
    return languages[idx % len(languages)]


def advance_rotation(config: Dict[str, Any]) -> None:
    languages = config["languages"]
    config["current_index"] = (config.get("current_index", 0) + 1) % len(languages)


# ── Core gauntlet function ───────────────────────────────────────────────────

def get_gauntlet(language: Optional[str] = None) -> Dict[str, Any]:
    """
    Issue the gauntlet challenge for the current (or specified) language.

    Args:
        language: override the current rotation language (for testing)

    Returns:
        dict with the gauntlet challenge, rubric, and metadata
    """
    config = load_rotation()

    if language is None:
        language = get_current_language(config)
        advance_rotation(config)

    gauntlet = GAUNTLET_DATA[language]
    lang_idx = config["languages"].index(language)
    rng_seed = lang_idx

    # Deterministic selection from hints
    rng = random.Random(rng_seed)
    num_hints = min(2, len(gauntlet["hints"]))
    selected_hints = rng.sample(gauntlet["hints"], num_hints)

    # Update rotation
    config["last_language"] = language
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)

    emoji_map = {
        "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
        "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "C/C++": "⚙️"
    }

    # next_language is always the one AFTER 'language' in the rotation cycle
    lang_pos = config["languages"].index(language)
    next_lang = config["languages"][(lang_pos + 1) % len(config["languages"])]
    next_emoji = emoji_map.get(next_lang, "🔧")

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": language,
        "emoji": emoji_map.get(language, "🔧"),
        "name": gauntlet["name"],
        "challenge": gauntlet["challenge"],
        "difficulty": gauntlet["difficulty"],
        "time_estimate": gauntlet["time_estimate"],
        "skills_tested": gauntlet["skills_tested"],
        "success_criteria": gauntlet["success_criteria"],
        "failure_modes": gauntlet["failure_modes"],
        "mastery_quote": gauntlet["mastery_quote"],
        "hints": selected_hints,
        "starter_template": gauntlet.get("starter_template", ""),
        "rotation": config["languages"],
        "next_language": next_lang,
        "next_emoji": next_emoji,
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def format_gauntlet(result: Dict[str, Any]) -> str:
    """Format a gauntlet as readable text."""
    lines = [
        f"{result['emoji']} Polyglot Gauntlet — {result['language']}",
        f"{'═' * 55}",
        f"⚔️  {result['name']}",
        f"Difficulty: {result['difficulty']}  |  Est: {result['time_estimate']}",
        f"",
        f"📜 THE CHALLENGE:",
        f"{result['challenge']}",
        f"",
        f"✅ SUCCESS CRITERIA:",
    ]
    for criterion in result["success_criteria"]:
        lines.append(f"  • {criterion}")

    lines.extend([
        f"",
        f"❌ FAILURE MODES:",
    ])
    for mode in result["failure_modes"]:
        lines.append(f"  • {mode}")

    lines.extend([
        f"",
        f"🎯 SKILLS TESTED:",
    ])
    for skill in result["skills_tested"]:
        lines.append(f"  • {skill}")

    lines.extend([
        f"",
        f"💡 HINTS ({len(result['hints'])} selected):",
    ])
    for i, hint in enumerate(result["hints"], 1):
        lines.append(f"  {i}. {hint}")

    lines.extend([
        f"",
        f"🏆 MASTERY QUOTE:",
        f"  \"{result['mastery_quote']}\"",
        f"",
        f"{'─' * 55}",
        f"Next up: {result['next_emoji']} {result['next_language']}",
    ])
    return "\n".join(lines)


# ── Tests ─────────────────────────────────────────────────────────────────────

def run_tests() -> None:
    """Run all internal tests."""
    import subprocess
    result = subprocess.run(
        [sys.executable, "-m", "pytest",
         str(Path(__file__).parent.parent / "tests" / "test_gauntlet.py"), "-v"],
        capture_output=False,
    )
    raise SystemExit(result.returncode)


# ── __main__ CLI ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        from gauntlet import run_tests
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--gauntlet":
        result = get_gauntlet()
        print(format_gauntlet(result))
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        result = get_gauntlet()
        print(json.dumps(result, indent=2))
    else:
        print(f"⚔️ Polyglot Gauntlet v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_gauntlet --gauntlet  # Issue gauntlet")
        print("  python -m polyglot_gauntlet --test       # Run tests")
        print("  python -m polyglot_gauntlet --json       # JSON output")
