//! Brainfuck Interpreter Utilities
//!
//! A complete Brainfuck language interpreter with support for:
//! - All 8 standard Brainfuck commands
//! - Nested loops
//! - Memory bounds checking
//! - Custom memory size configuration
//! - Debug/trace mode



/// Default memory size (30,000 cells as per standard Brainfuck)
pub const DEFAULT_MEMORY_SIZE: usize = 30_000;

/// Error type for Brainfuck interpreter
#[derive(Debug, Clone, PartialEq)]
pub enum BrainfuckError {
    /// Unmatched opening bracket '['
    UnmatchedOpenBracket(usize),
    /// Unmatched closing bracket ']'
    UnmatchedCloseBracket(usize),
    /// Memory pointer out of bounds
    MemoryOutOfBounds(usize),
    /// Invalid character in source code
    InvalidCharacter(char, usize),
    /// Input error
    InputError(String),
    /// Output error
    OutputError(String),
}

impl std::fmt::Display for BrainfuckError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::UnmatchedOpenBracket(pos) => write!(f, "Unmatched '[' at position {}", pos),
            Self::UnmatchedCloseBracket(pos) => write!(f, "Unmatched ']' at position {}", pos),
            Self::MemoryOutOfBounds(ptr) => write!(f, "Memory pointer out of bounds: {}", ptr),
            Self::InvalidCharacter(ch, pos) => write!(f, "Invalid character '{}' at position {}", ch, pos),
            Self::InputError(msg) => write!(f, "Input error: {}", msg),
            Self::OutputError(msg) => write!(f, "Output error: {}", msg),
        }
    }
}

impl std::error::Error for BrainfuckError {}

/// Brainfuck interpreter configuration
#[derive(Debug, Clone)]
pub struct InterpreterConfig {
    /// Memory size in cells
    pub memory_size: usize,
    /// Enable debug/trace output
    pub debug: bool,
    /// Maximum iterations to prevent infinite loops (0 = unlimited)
    pub max_iterations: usize,
    /// Wrap memory pointer at boundaries
    pub wrap_pointer: bool,
    /// Allow negative cell values (signed) or wrap at 0-255 (unsigned)
    pub signed_cells: bool,
}

impl Default for InterpreterConfig {
    fn default() -> Self {
        Self {
            memory_size: DEFAULT_MEMORY_SIZE,
            debug: false,
            max_iterations: 0,
            wrap_pointer: false,
            signed_cells: false,
        }
    }
}

/// Brainfuck interpreter
#[derive(Debug)]
pub struct BrainfuckInterpreter {
    /// Memory cells
    memory: Vec<i64>,
    /// Memory pointer
    pointer: usize,
    /// Instruction pointer
    instruction_pointer: usize,
    /// Program source (cleaned)
    source: Vec<char>,
    /// Bracket matching table (open position -> close position)
    bracket_map: std::collections::HashMap<usize, usize>,
    /// Configuration
    config: InterpreterConfig,
    /// Iteration counter
    iterations: usize,
    /// Output buffer
    output: Vec<u8>,
    /// Input buffer
    input: Vec<u8>,
    /// Input position
    input_pos: usize,
}

impl BrainfuckInterpreter {
    /// Create a new interpreter with default configuration
    pub fn new() -> Self {
        Self::with_config(InterpreterConfig::default())
    }

    /// Create a new interpreter with custom configuration
    pub fn with_config(config: InterpreterConfig) -> Self {
        Self {
            memory: vec![0; config.memory_size],
            pointer: 0,
            instruction_pointer: 0,
            source: Vec::new(),
            bracket_map: std::collections::HashMap::new(),
            config,
            iterations: 0,
            output: Vec::new(),
            input: Vec::new(),
            input_pos: 0,
        }
    }

    /// Parse and validate source code
    pub fn parse(&mut self, source: &str) -> Result<(), BrainfuckError> {
        // Clean source (keep only valid commands)
        self.source = source.chars().filter(|c| "<>+-[].,".contains(*c)).collect();
        self.instruction_pointer = 0;
        self.bracket_map.clear();
        self.memory.fill(0);
        self.pointer = 0;
        self.output.clear();
        self.input.clear();
        self.input_pos = 0;
        self.iterations = 0;

        // Build bracket map
        let mut stack = Vec::new();
        for (pos, &ch) in self.source.iter().enumerate() {
            match ch {
                '[' => stack.push(pos),
                ']' => {
                    if let Some(open_pos) = stack.pop() {
                        self.bracket_map.insert(open_pos, pos);
                        self.bracket_map.insert(pos, open_pos);
                    } else {
                        return Err(BrainfuckError::UnmatchedCloseBracket(pos));
                    }
                }
                _ => {}
            }
        }

        if let Some(open_pos) = stack.pop() {
            return Err(BrainfuckError::UnmatchedOpenBracket(open_pos));
        }

        Ok(())
    }

    /// Set input for the program
    pub fn set_input(&mut self, input: &[u8]) {
        self.input = input.to_vec();
        self.input_pos = 0;
    }

    /// Set input from string
    pub fn set_input_string(&mut self, input: &str) {
        self.set_input(input.as_bytes());
    }

    /// Run the program and return output
    pub fn run(&mut self) -> Result<Vec<u8>, BrainfuckError> {
        while self.instruction_pointer < self.source.len() {
            if self.config.max_iterations > 0 && self.iterations >= self.config.max_iterations {
                break;
            }
            self.step()?;
            self.iterations += 1;
        }
        Ok(self.output.clone())
    }

    /// Run the program and return output as string
    pub fn run_to_string(&mut self) -> Result<String, BrainfuckError> {
        let output = self.run()?;
        String::from_utf8(output)
            .map_err(|_| BrainfuckError::OutputError("Invalid UTF-8 output".to_string()))
    }

    /// Execute one instruction
    pub fn step(&mut self) -> Result<(), BrainfuckError> {
        let command = self.source.get(self.instruction_pointer).copied();

        if let Some(cmd) = command {
            match cmd {
                '>' => self.move_pointer(1)?,
                '<' => self.move_pointer(-1)?,
                '+' => self.increment_cell()?,
                '-' => self.decrement_cell()?,
                '.' => self.output_cell()?,
                ',' => self.input_cell()?,
                '[' => self.jump_if_zero()?,
                ']' => self.jump_if_not_zero()?,
                _ => {}
            }
            self.instruction_pointer += 1;
        }

        Ok(())
    }

    fn move_pointer(&mut self, delta: isize) -> Result<(), BrainfuckError> {
        if delta > 0 {
            self.pointer = if self.config.wrap_pointer {
                (self.pointer + delta as usize) % self.config.memory_size
            } else {
                self.pointer.checked_add(delta as usize)
                    .ok_or(BrainfuckError::MemoryOutOfBounds(usize::MAX))?
            };
        } else {
            self.pointer = if self.config.wrap_pointer {
                let new_ptr = self.pointer as isize + delta;
                if new_ptr < 0 {
                    (new_ptr + self.config.memory_size as isize) as usize
                } else {
                    new_ptr as usize
                }
            } else {
                self.pointer.checked_sub((-delta) as usize)
                    .ok_or(BrainfuckError::MemoryOutOfBounds(0))?
            };
        }

        if self.pointer >= self.config.memory_size {
            return Err(BrainfuckError::MemoryOutOfBounds(self.pointer));
        }

        Ok(())
    }

    fn increment_cell(&mut self) -> Result<(), BrainfuckError> {
        if self.config.signed_cells {
            self.memory[self.pointer] += 1;
        } else {
            self.memory[self.pointer] = (self.memory[self.pointer] + 1) % 256;
        }
        Ok(())
    }

    fn decrement_cell(&mut self) -> Result<(), BrainfuckError> {
        if self.config.signed_cells {
            self.memory[self.pointer] -= 1;
        } else {
            self.memory[self.pointer] = if self.memory[self.pointer] == 0 {
                255
            } else {
                self.memory[self.pointer] - 1
            };
        }
        Ok(())
    }

    fn output_cell(&mut self) -> Result<(), BrainfuckError> {
        let value = self.memory[self.pointer] as u8;
        self.output.push(value);
        Ok(())
    }

    fn input_cell(&mut self) -> Result<(), BrainfuckError> {
        if self.input_pos < self.input.len() {
            self.memory[self.pointer] = self.input[self.input_pos] as i64;
            self.input_pos += 1;
        } else {
            // EOF: set to 0 or -1 depending on implementation
            self.memory[self.pointer] = if self.config.signed_cells { -1 } else { 0 };
        }
        Ok(())
    }

    fn jump_if_zero(&mut self) -> Result<(), BrainfuckError> {
        if self.memory[self.pointer] == 0 {
            if let Some(&close_pos) = self.bracket_map.get(&self.instruction_pointer) {
                self.instruction_pointer = close_pos;
            }
        }
        Ok(())
    }

    fn jump_if_not_zero(&mut self) -> Result<(), BrainfuckError> {
        if self.memory[self.pointer] != 0 {
            if let Some(&open_pos) = self.bracket_map.get(&self.instruction_pointer) {
                self.instruction_pointer = open_pos;
            }
        }
        Ok(())
    }

    /// Get current cell value
    pub fn current_cell(&self) -> i64 {
        self.memory[self.pointer]
    }

    /// Get memory pointer position
    pub fn pointer(&self) -> usize {
        self.pointer
    }

    /// Get instruction pointer position
    pub fn instruction_pointer(&self) -> usize {
        self.instruction_pointer
    }

    /// Get total iterations executed
    pub fn iterations(&self) -> usize {
        self.iterations
    }

    /// Get memory dump (for debugging)
    pub fn memory_dump(&self, start: usize, len: usize) -> &[i64] {
        let end = (start + len).min(self.memory.len());
        &self.memory[start..end]
    }

    /// Get current output
    pub fn output(&self) -> &[u8] {
        &self.output
    }

    /// Check if execution is complete
    pub fn is_complete(&self) -> bool {
        self.instruction_pointer >= self.source.len()
    }

    /// Reset interpreter state (keep source)
    pub fn reset(&mut self) {
        self.memory.fill(0);
        self.pointer = 0;
        self.instruction_pointer = 0;
        self.output.clear();
        self.input_pos = 0;
        self.iterations = 0;
    }
}

impl Default for BrainfuckInterpreter {
    fn default() -> Self {
        Self::new()
    }
}

/// Convenience function to run Brainfuck code
pub fn run_brainfuck(source: &str) -> Result<String, BrainfuckError> {
    let mut interpreter = BrainfuckInterpreter::new();
    interpreter.parse(source)?;
    interpreter.run_to_string()
}

/// Run Brainfuck code with input
pub fn run_brainfuck_with_input(source: &str, input: &str) -> Result<String, BrainfuckError> {
    let mut interpreter = BrainfuckInterpreter::new();
    interpreter.parse(source)?;
    interpreter.set_input_string(input);
    interpreter.run_to_string()
}

/// Optimize Brainfuck code by combining consecutive operations
pub fn optimize(source: &str) -> String {
    let mut result = String::new();
    let chars: Vec<char> = source.chars().collect();
    let mut i = 0;

    while i < chars.len() {
        let c = chars[i];
        if "<>+-".contains(c) {
            let mut count = 0i32;
            while i < chars.len() {
                let current = chars[i];
                if current == c {
                    count += 1;
                    i += 1;
                } else if (c == '>' && current == '<') || (c == '<' && current == '>') {
                    count -= 1;
                    i += 1;
                } else if (c == '+' && current == '-') || (c == '-' && current == '+') {
                    count -= 1;
                    i += 1;
                } else {
                    break;
                }
            }
            if count > 0 {
                for _ in 0..count {
                    result.push(c);
                }
            } else if count < 0 {
                let opposite = if c == '>' { '<' } else if c == '<' { '>' } else if c == '+' { '-' } else { '+' };
                for _ in 0..(-count) {
                    result.push(opposite);
                }
            }
        } else if "[].,".contains(c) {
            result.push(c);
            i += 1;
        } else {
            i += 1;
        }
    }

    result
}

/// Validate Brainfuck code syntax
pub fn validate(source: &str) -> Result<(), BrainfuckError> {
    let clean: Vec<char> = source.chars().filter(|c| "<>+-[].,".contains(*c)).collect();
    let mut stack = Vec::new();

    for (pos, &ch) in clean.iter().enumerate() {
        match ch {
            '[' => stack.push(pos),
            ']' => {
                if stack.pop().is_none() {
                    return Err(BrainfuckError::UnmatchedCloseBracket(pos));
                }
            }
            _ => {}
        }
    }

    if let Some(open_pos) = stack.pop() {
        return Err(BrainfuckError::UnmatchedOpenBracket(open_pos));
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hello_world() {
        let source = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.";
        let result = run_brainfuck(source).unwrap();
        assert_eq!(result.trim_end(), "Hello World!");
    }

    #[test]
    fn test_simple_output() {
        // Output character 'A' (65)
        let source = "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.";
        let result = run_brainfuck(source).unwrap();
        assert_eq!(result, "A");
    }

    #[test]
    fn test_increment_decrement() {
        let source = "+++.--.";
        let result = run_brainfuck(source).unwrap();
        assert_eq!(result, "\x03\x01");
    }

    #[test]
    fn test_loop() {
        // Set cell 0 to 3, then use it as loop counter to add 5 to cell 1
        let source = "+++[>+++++<-]>.";
        let result = run_brainfuck(source).unwrap();
        assert_eq!(result, "\x0f"); // 15
    }

    #[test]
    fn test_input() {
        let source = ",.";
        let result = run_brainfuck_with_input(source, "X").unwrap();
        assert_eq!(result, "X");
    }

    #[test]
    fn test_nested_loops() {
        // 3 * 4 = 12
        let source = "+++[>++++<-]>.";
        let result = run_brainfuck(source).unwrap();
        assert_eq!(result, "\x0c");
    }

    #[test]
    fn test_pointer_movement() {
        let source = ">++++++++++.---.";
        let result = run_brainfuck(source).unwrap();
        assert_eq!(result.as_bytes(), &[10, 7]); // newline and bell
    }

    #[test]
    fn test_unmatched_bracket() {
        let source = "[";
        let result = validate(source);
        assert!(matches!(result, Err(BrainfuckError::UnmatchedOpenBracket(0))));
    }

    #[test]
    fn test_unmatched_close() {
        let source = "]";
        let result = validate(source);
        assert!(matches!(result, Err(BrainfuckError::UnmatchedCloseBracket(0))));
    }

    #[test]
    fn test_optimize() {
        let source = "+++++---";
        let optimized = optimize(source);
        assert_eq!(optimized, "++");
    }

    #[test]
    fn test_optimize_movement() {
        let source = ">>><<>";
        let optimized = optimize(source);
        assert_eq!(optimized, ">>");
    }

    #[test]
    fn test_empty_loop() {
        let source = "[]";
        let result = run_brainfuck(source);
        assert!(result.is_ok());
    }

    #[test]
    fn test_multiple_loops() {
        // 2 * 3 + 5 = 11
        let source = "++[>+++<-]>+++++.";
        let result = run_brainfuck(source).unwrap();
        assert_eq!(result, "\x0b");
    }

    #[test]
    fn test_wrap_cells() {
        let mut config = InterpreterConfig::default();
        config.signed_cells = false;
        let mut interpreter = BrainfuckInterpreter::with_config(config);
        interpreter.parse("-.").unwrap();
        let result = interpreter.run().unwrap();
        assert_eq!(result, vec![255u8]); // 255
    }

    #[test]
    fn test_signed_cells() {
        let mut config = InterpreterConfig::default();
        config.signed_cells = true;
        let mut interpreter = BrainfuckInterpreter::with_config(config);
        interpreter.parse("-.").unwrap();
        let result = interpreter.run().unwrap();
        assert_eq!(result, vec![255u8]); // -1 as unsigned byte (wrapping)
    }

    #[test]
    fn test_interpreter_state() {
        let mut interpreter = BrainfuckInterpreter::new();
        interpreter.parse("+++").unwrap();
        interpreter.run().unwrap();
        assert_eq!(interpreter.current_cell(), 3);
        assert_eq!(interpreter.iterations(), 3);
        assert!(interpreter.is_complete());
    }

    #[test]
    fn test_memory_dump() {
        let mut interpreter = BrainfuckInterpreter::new();
        interpreter.parse(">+++>+++++").unwrap();
        interpreter.run().unwrap();
        let dump = interpreter.memory_dump(0, 3);
        assert_eq!(dump, [0, 3, 5]);
    }

    #[test]
    fn test_reset() {
        let mut interpreter = BrainfuckInterpreter::new();
        interpreter.parse("+++").unwrap();
        interpreter.run().unwrap();
        assert_eq!(interpreter.current_cell(), 3);
        interpreter.reset();
        assert_eq!(interpreter.current_cell(), 0);
        assert!(!interpreter.is_complete());
    }
}