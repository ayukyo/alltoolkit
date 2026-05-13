# Brainfuck Interpreter Utils

A complete Brainfuck language interpreter implemented in Rust with zero external dependencies.

## Features

- **Complete BF Commands**: Supports all 8 standard Brainfuck commands (`>`, `<`, `+`, `-`, `.`, `,`, `[`, `]`)
- **Nested Loops**: Full support for nested loop structures
- **Memory Bounds Checking**: Configurable memory size with optional pointer wrapping
- **Input/Output Support**: Handle both input and output operations
- **Code Optimization**: Merge consecutive operations for better performance
- **Syntax Validation**: Validate Brainfuck code before execution
- **Zero Dependencies**: Uses only Rust standard library

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
brainfuck_interpreter_utils = "0.1.0"
```

## Usage

### Basic Usage

```rust
use brainfuck_interpreter_utils::run_brainfuck;

// Hello World
let source = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.";
let output = run_brainfuck(source).unwrap();
println!("{}", output); // Hello World!
```

### With Input

```rust
use brainfuck_interpreter_utils::run_brainfuck_with_input;

let source = ",."; // Echo
let output = run_brainfuck_with_input(source, "A").unwrap();
println!("{}", output); // A
```

### Custom Configuration

```rust
use brainfuck_interpreter_utils::{BrainfuckInterpreter, InterpreterConfig};

let mut config = InterpreterConfig {
    memory_size: 1000,
    debug: false,
    max_iterations: 10000,
    wrap_pointer: true,
    signed_cells: false,
};

let mut interpreter = BrainfuckInterpreter::with_config(config);
interpreter.parse("+++[>+++<-]>.").unwrap();
let output = interpreter.run_to_string().unwrap();
```

### Code Optimization

```rust
use brainfuck_interpreter_utils::optimize;

let unoptimized = "++++++++++----------+++++-----";
let optimized = optimize(unoptimized);
// Result: "" (operations cancel out)
```

### Code Validation

```rust
use brainfuck_interpreter_utils::validate;

match validate("+++[>+++<-]") {
    Ok(()) => println!("Valid code"),
    Err(e) => println!("Error: {}", e),
}
```

## API Reference

### Functions

- `run_brainfuck(source: &str) -> Result<String, BrainfuckError>` - Execute BF code and return output
- `run_brainfuck_with_input(source: &str, input: &str) -> Result<String, BrainfuckError>` - Execute with input
- `optimize(source: &str) -> String` - Optimize BF code by merging operations
- `validate(source: &str) -> Result<(), BrainfuckError>` - Validate BF syntax

### Structs

- `BrainfuckInterpreter` - Main interpreter with step-by-step execution
- `InterpreterConfig` - Configuration options
- `BrainfuckError` - Error types

### Interpreter Methods

- `new()` - Create interpreter with default config
- `with_config(config)` - Create with custom config
- `parse(source)` - Parse and validate code
- `set_input(input)` - Set input buffer
- `run()` - Execute program, returns output bytes
- `run_to_string()` - Execute and return string
- `step()` - Execute single instruction
- `reset()` - Reset state (keep code)
- `memory_dump(start, len)` - Get memory contents
- `current_cell()` - Get current cell value
- `pointer()` - Get memory pointer position
- `iterations()` - Get execution count

## Examples

Run the examples:

```bash
cargo run --example basic
```

## License

MIT