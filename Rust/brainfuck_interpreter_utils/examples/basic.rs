//! Brainfuck Interpreter Examples

use brainfuck_interpreter_utils::{
    run_brainfuck, run_brainfuck_with_input, optimize, validate,
    BrainfuckInterpreter, InterpreterConfig,
};

fn main() {
    println!("=== Brainfuck Interpreter Examples ===\n");

    // Example 1: Hello World
    println!("1. Classic Hello World:");
    let hello_world = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.";
    match run_brainfuck(hello_world) {
        Ok(output) => println!("   Output: {}", output.trim_end()),
        Err(e) => println!("   Error: {}", e),
    }

    // Example 2: Simple counting
    println!("\n2. Print numbers 0-9:");
    let numbers = "++++++++++++++++++++++++++++++++++++++++++++++++.>+++++++++++++++++++++++++++++++++++++++++++++++++.>++++++++++++++++++++++++++++++++++++++++++++++++++.>+++++++++++++++++++++++++++++++++++++++++++++++++++.>++++++++++++++++++++++++++++++++++++++++++++++++++++.>+++++++++++++++++++++++++++++++++++++++++++++++++++++.>++++++++++++++++++++++++++++++++++++++++++++++++++++++.>+++++++++++++++++++++++++++++++++++++++++++++++++++++++.>++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++.";
    match run_brainfuck(numbers) {
        Ok(output) => println!("   Output: {}", output.trim()),
        Err(e) => println!("   Error: {}", e),
    }

    // Example 3: Using input
    println!("\n3. Echo input:");
    let echo = ",.";
    match run_brainfuck_with_input(echo, "A") {
        Ok(output) => println!("   Input: A, Output: {}", output),
        Err(e) => println!("   Error: {}", e),
    }

    // Example 4: Multiplication (3 * 7 = 21)
    println!("\n4. Multiplication (3 × 7 = 21):");
    let multiply = "+++[>+++++++<-]>.";
    match run_brainfuck(multiply) {
        Ok(output) => println!("   Output: {} (byte value: {})", output.chars().next().unwrap_or('\0'), output.as_bytes()[0]),
        Err(e) => println!("   Error: {}", e),
    }

    // Example 5: Nested loops
    println!("\n5. Nested loops (2 × 3 × 4 = 24):");
    let nested = "++[>+++[>++++<-]<-]>.";
    match run_brainfuck(nested) {
        Ok(output) => println!("   Output: {} (byte value: {})", output.chars().next().unwrap_or('\0'), output.as_bytes()[0]),
        Err(e) => println!("   Error: {}", e),
    }

    // Example 6: Using interpreter with custom config
    println!("\n6. Custom configuration (with iteration limit):");
    let mut config = InterpreterConfig::default();
    config.memory_size = 100;
    config.max_iterations = 1000;
    config.debug = false;
    
    let mut interpreter = BrainfuckInterpreter::with_config(config);
    let program = "+++++[>+++++<-]>.";
    
    match interpreter.parse(program) {
        Ok(()) => {
            match interpreter.run() {
                Ok(output) => println!("   Output: {} (byte value: {})", output.iter().map(|&b| b as char).collect::<String>(), output[0]),
                Err(e) => println!("   Error: {}", e),
            }
            println!("   Iterations: {}", interpreter.iterations());
        }
        Err(e) => println!("   Parse error: {}", e),
    }

    // Example 7: Optimization
    println!("\n7. Code optimization:");
    let unoptimized = "++++++++++----------+++++-----";
    let optimized = optimize(unoptimized);
    println!("   Original: {}", unoptimized);
    println!("   Optimized: {}", optimized);
    
    // Example 8: Validation
    println!("\n8. Code validation:");
    let valid_code = "+++[>+++<-]>.";
    let invalid_code = "+++[>+++<-.";
    
    println!("   '{}': {}", valid_code, match validate(valid_code) {
        Ok(()) => "Valid ✓".to_string(),
        Err(e) => format!("Invalid - {}", e),
    });
    
    println!("   '{} {}", invalid_code, match validate(invalid_code) {
        Ok(()) => "Valid ✓".to_string(),
        Err(e) => format!("Invalid - {}", e),
    });

    // Example 9: Memory dump for debugging
    println!("\n9. Memory dump after execution:");
    let mut interp = BrainfuckInterpreter::new();
    interp.parse(">+++>+++++>++").unwrap();
    interp.run().unwrap();
    let dump = interp.memory_dump(0, 10);
    println!("   First 10 cells: {:?}", dump);

    // Example 10: Cat program (reads and outputs until EOF)
    println!("\n10. Simple cat (first 3 chars):");
    let cat = ",.,.,.";
    match run_brainfuck_with_input(cat, "Hi!") {
        Ok(output) => println!("   Input: 'Hi!', Output: '{}'", output),
        Err(e) => println!("   Error: {}", e),
    }

    // Example 11: Fibonacci-like sequence
    println!("\n11. Generate sequence:");
    let sequence = "++++++++++++[>++++++>+++++++>++++>+++++<<<<-]>+.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.";
    match run_brainfuck(sequence) {
        Ok(output) => println!("   Output: {}", output.trim_end()),
        Err(e) => println!("   Error: {}", e),
    }

    // Example 12: Clear cells
    println!("\n12. Clear memory region:");
    let clear = "+++++[>+++++<-]>[-]<.";
    match run_brainfuck(clear) {
        Ok(output) => println!("   Cell 0 value: {} (should be 0)", output.as_bytes()[0]),
        Err(e) => println!("   Error: {}", e),
    }

    // Example 13: Copy value
    println!("\n13. Copy value from cell 0 to cell 1:");
    let copy = "+++++[->+>+<<]>>.";  // Copy 5 to cell 2
    match run_brainfuck(copy) {
        Ok(output) => println!("   Copied value: {} (should be 5)", output.as_bytes()[0]),
        Err(e) => println!("   Error: {}", e),
    }

    println!("\n=== All examples completed! ===");
}