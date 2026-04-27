# Expression Evaluator Utils (Go)

A mathematical expression parser and evaluator for Go with zero external dependencies.

## Features

- **Basic Arithmetic**: `+`, `-`, `*`, `/`, `%` operators
- **Exponentiation**: `^` operator (right-associative)
- **Parentheses**: Full support for deeply nested parentheses
- **Unary Operators**: Support for unary plus (`+`) and minus (`-`)
- **Built-in Functions**: 25+ mathematical functions
- **Variables**: Define and use variables in expressions
- **Constants**: Built-in `pi`, `e`, `phi`
- **Extensible**: Add custom functions
- **Zero Dependencies**: Pure Go implementation

## Installation

```go
import "github.com/ayukyo/alltoolkit/Go/expression_evaluator"
```

## Quick Start

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/expression_evaluator"
)

func main() {
    e := expression_evaluator.New()
    
    // Basic arithmetic
    result, _ := e.Evaluate("2 + 3 * 4")
    fmt.Println(result) // 14
    
    // With parentheses
    result, _ = e.Evaluate("(2 + 3) * 4")
    fmt.Println(result) // 20
    
    // Using functions
    result, _ = e.Evaluate("sqrt(16) + abs(-5)")
    fmt.Println(result) // 9
    
    // Using variables
    e.SetVariable("x", 10)
    result, _ = e.Evaluate("x * 2 + 5")
    fmt.Println(result) // 25
    
    // Using constants
    result, _ = e.Evaluate("sin(pi / 2)")
    fmt.Println(result) // 1
    
    // Unary operators
    result, _ = e.Evaluate("-5 + 10")
    fmt.Println(result) // 5
}
```

## Supported Operators

| Operator | Description | Precedence | Associativity |
|----------|-------------|------------|---------------|
| `^` | Exponentiation | 4 | Right |
| `*`, `/`, `%` | Multiplication, Division, Modulo | 3 | Left |
| `+`, `-` | Addition, Subtraction | 2 | Left |
| `-` (unary) | Negation | 1 | Right |
| `+` (unary) | Identity | 1 | Right |

## Built-in Functions

### Single Argument Functions

| Function | Description |
|----------|-------------|
| `sin(x)` | Sine |
| `cos(x)` | Cosine |
| `tan(x)` | Tangent |
| `asin(x)` | Arc sine |
| `acos(x)` | Arc cosine |
| `atan(x)` | Arc tangent |
| `sinh(x)` | Hyperbolic sine |
| `cosh(x)` | Hyperbolic cosine |
| `tanh(x)` | Hyperbolic tangent |
| `sqrt(x)` | Square root |
| `cbrt(x)` | Cube root |
| `abs(x)` | Absolute value |
| `ceil(x)` | Ceiling |
| `floor(x)` | Floor |
| `round(x)` | Round to nearest integer |
| `log(x)` | Natural logarithm |
| `log10(x)` | Base-10 logarithm |
| `log2(x)` | Base-2 logarithm |
| `ln(x)` | Natural logarithm (alias) |
| `exp(x)` | Exponential (e^x) |

### Multi-Argument Functions

| Function | Description |
|----------|-------------|
| `min(a, b, ...)` | Minimum of arguments |
| `max(a, b, ...)` | Maximum of arguments |
| `avg(a, b, ...)` | Average of arguments |
| `sum(a, b, ...)` | Sum of arguments |

## Variables

```go
e := expression_evaluator.New()

// Set variables
e.SetVariable("x", 10)
e.SetVariable("y", 20)

// Use in expressions
result, _ := e.Evaluate("x + y")  // 30

// Get variable value
val, ok := e.GetVariable("x")  // val = 10, ok = true

// Clear user variables (keeps constants)
e.ClearVariables()
```

## Built-in Constants

| Constant | Value |
|----------|-------|
| `pi` | π ≈ 3.141592653589793 |
| `e` | e ≈ 2.718281828459045 |
| `phi` | Golden ratio ≈ 1.618033988749895 |

## Custom Functions

```go
e := expression_evaluator.New()

// Single-argument function
e.RegisterFunction1("double", func(x float64) float64 {
    return x * 2
})

result, _ := e.Evaluate("double(5)")  // 10

// Multi-argument function
e.RegisterFunctionN("sum3", func(args []float64) (float64, error) {
    if len(args) != 3 {
        return 0, fmt.Errorf("sum3 requires exactly 3 arguments")
    }
    return args[0] + args[1] + args[2], nil
})
```

## Examples

### Simple Calculator

```go
e := expression_evaluator.New()

expressions := []string{
    "2 + 3",
    "10 * 5 - 3",
    "(2 + 3) * (4 - 1)",
    "sqrt(144)",
    "sin(pi / 6)",
}

for _, expr := range expressions {
    result, err := e.Evaluate(expr)
    if err != nil {
        fmt.Printf("%s = Error: %v\n", expr, err)
    } else {
        fmt.Printf("%s = %v\n", expr, result)
    }
}
```

### Formula Calculator

```go
e := expression_evaluator.New()

// Set up variables for a physics formula
e.SetVariable("m", 10)  // mass in kg
e.SetVariable("v", 5)   // velocity in m/s

// Calculate kinetic energy: KE = 0.5 * m * v^2
ke, _ := e.Evaluate("0.5 * m * v ^ 2")
fmt.Printf("Kinetic Energy: %v J\n", ke)  // 125 J
```

### Temperature Converter

```go
e := expression_evaluator.New()
e.SetVariable("celsius", 25)

// Convert to Fahrenheit: F = C * 9/5 + 32
e.RegisterFunction1("toFahrenheit", func(c float64) float64 {
    return c*9/5 + 32
})

f, _ := e.Evaluate("toFahrenheit(celsius)")
fmt.Printf("25°C = %v°F\n", f)  // 77°F
```

## Error Handling

```go
e := expression_evaluator.New()

// Undefined variable
_, err := e.Evaluate("x + 1")
// Error: undefined variable: x

// Mismatched parentheses
_, err = e.Evaluate("(2 + 3")
// Error: missing closing parenthesis

// Division by zero
_, err = e.Evaluate("10 / 0")
// Error: division by zero

// Unknown function
_, err = e.Evaluate("foo(5)")
// Error: unknown function: foo
```

## API Reference

### Constructor

```go
e := expression_evaluator.New()
```

### Methods

| Method | Description |
|--------|-------------|
| `Evaluate(expr string) (float64, error)` | Evaluate an expression |
| `EvaluateAsString(expr string) (string, error)` | Evaluate and return as string |
| `SetVariable(name string, value float64)` | Set a variable |
| `GetVariable(name string) (float64, bool)` | Get a variable value |
| `ClearVariables()` | Clear all user variables |
| `RegisterFunction1(name string, fn func(float64) float64)` | Add single-arg function |
| `RegisterFunctionN(name string, fn func([]float64) (float64, error))` | Add multi-arg function |
| `GetSupportedFunctions() []string` | List all functions |
| `GetVariables() map[string]float64` | Get all variables |
| `IsExpressionValid(expr string) bool` | Check if expression is valid |
| `ParseAndExplain(expr string) (string, error)` | Get detailed explanation |

## Implementation Details

This implementation uses a **recursive descent parser** (also known as a Pratt parser) that naturally handles operator precedence:

- `parseExpression()` handles `+` and `-` (lowest precedence)
- `parseTerm()` handles `*`, `/`, `%`
- `parseFactor()` handles `^` (right-associative)
- `parseUnary()` handles unary `+` and `-`
- `parsePrimary()` handles numbers, identifiers, and parentheses

This approach is simpler than Shunting-yard algorithm and more maintainable.

## Test Results

All 21 test cases pass including:
- Basic arithmetic operations
- Operator precedence
- Parentheses (including deeply nested)
- Built-in functions (25+)
- Multi-argument functions
- Variables and constants
- Unary operators
- Decimal numbers
- Whitespace handling
- Error handling
- Custom functions
- Nested functions

## License

MIT License