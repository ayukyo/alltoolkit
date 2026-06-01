# json_patch_utils (Zig)

A zero-dependency, pure-Zig implementation of [RFC 6902 JSON Patch](https://datatracker.ietf.org/doc/html/rfc6902) — the standard format for describing changes to a JSON document — together with [RFC 6901 JSON Pointer](https://datatracker.ietf.org/doc/html/rfc6901) resolution.

## Features

- All 6 standard operations: `add`, `remove`, `replace`, `move`, `copy`, `test`
- `add` to arrays with `"/-"` (append), arbitrary index (insert), or to objects
- `test` op aborts the whole patch on mismatch
- `move` / `copy` support `from` and proper `from`-then-`path` evaluation order
- Full JSON Pointer escaping: `~1` → `/`, `~0` → `~`
- `apply()` convenience: parse doc + parse patch + apply + return JSON text in one call
- Low-level `parsePatch` / `applyPatch` for in-place mutation without re-stringifying
- `jsonEql` helper for structural JSON equality
- `deepCloneValue` helper for cloning arbitrary JSON values
- Zero external dependencies — uses only the Zig standard library

## Build

```bash
zig build test          # run all unit tests
zig build run           # run the basic example
zig build run-advanced  # run the advanced example
```

## Quick start

```zig
const std = @import("std");
const json_patch = @import("json_patch");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    const doc =
        \\{"name": "Alice", "age": 30, "tags": ["admin"]}
    ;
    const patch =
        \\[{"op": "replace", "path": "/name", "value": "Bob"},
        \\ {"op": "add",     "path": "/city", "value": "Paris"},
        \\ {"op": "add",     "path": "/tags/-", "value": "vip"}]
    ;

    const result = try json_patch.apply(allocator, doc, patch);
    defer allocator.free(result);
    std.debug.print("{s}\n", .{result});
}
```

## API

### `apply(allocator, doc_text, patch_text) ![]u8`
Convenience: parse, apply, return indented JSON text.

### `parsePatch(allocator, patch_text) !Patch`
Parse a JSON Patch document. Caller must `patch.deinit()`.

### `applyPatch(allocator, doc, patch) !void`
Apply a parsed patch to an already-parsed `json.Value` (mutates in place).

### `applyOp(allocator, doc, op) !void`
Apply a single operation.

### `deepCloneValue(allocator, value) !json.Value`
Deep-clone a `json.Value`.

### `jsonEql(a, b) bool`
Structural equality on `json.Value` (object key order–insensitive; integer/float cross-comparable).

### `Op` enum
`add`, `remove`, `replace`, `move`, `copy`, `test`.

### `PatchError` error set
`InvalidJson`, `InvalidPatch`, `InvalidPath`, `InvalidIndex`, `PathNotFound`, `NotAnArray`, `NotAnObject`, `OutOfMemory`, `TestFailed`.

## Path syntax (RFC 6901)

- `/foo` — object key `foo`
- `/foo/0` — first element of `foo` array
- `/a~1b` — object key `a/b` (`~1` → `/`)
- `/a~0b` — object key `a~b` (`~0` → `~`)
- `/-` — for `add` into an array: append at end

## License

MIT
