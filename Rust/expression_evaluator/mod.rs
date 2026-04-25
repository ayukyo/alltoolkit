//! # Expression Evaluator
//!
//! A lightweight mathematical expression parser and evaluator with zero external dependencies.
//! Supports variables, functions, and proper operator precedence.
//!
//! ## Features
//!
//! - Parse and evaluate mathematical expressions
//! - Support for variables with custom values
//! - Built-in functions: `sin`, `cos`, `tan`, `sqrt`, `abs`, `ln`, `log10`, `exp`, `floor`, `ceil`, `round`
//! - Constants: `pi`, `e`
//! - Proper operator precedence (PEMDAS)
//! - Parentheses for grouping
//! - Error handling for invalid expressions
//!
//! ## Usage
//!
//! ```rust
//! use expression_evaluator::Evaluator;
//!
//! // Simple expression
//! let result = Evaluator::new().eval("2 + 3 * 4").unwrap();
//! assert_eq!(result, 14.0);
//!
//! // With variables
//! let mut eval = Evaluator::new();
//! eval.set_var("x", 5.0);
//! eval.set_var("y", 3.0);
//! let result = eval.eval("x * y + 2").unwrap();
//! assert_eq!(result, 17.0);
//!
//! // Using functions
//! let result = Evaluator::new().eval("sqrt(16) + sin(pi/2)").unwrap();
//! ```

use std::collections::HashMap;
use std::f64::consts::{E, PI};

/// Expression parsing and evaluation errors
#[derive(Debug, Clone, PartialEq)]
pub enum EvalError {
    /// Unexpected character encountered
    UnexpectedChar(char, usize),
    /// Unexpected end of expression
    UnexpectedEnd,
    /// Missing closing parenthesis
    MissingClosingParen,
    /// Unknown function name
    UnknownFunction(String),
    /// Unknown variable name
    UnknownVariable(String),
    /// Invalid number format
    InvalidNumber(String),
    /// Division by zero
    DivisionByZero,
    /// Invalid argument count for function
    InvalidArgCount { func: String, expected: usize, got: usize },
    /// Function domain error (e.g., sqrt of negative)
    DomainError(String),
}

impl std::fmt::Display for EvalError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            EvalError::UnexpectedChar(c, pos) => write!(f, "Unexpected character '{}' at position {}", c, pos),
            EvalError::UnexpectedEnd => write!(f, "Unexpected end of expression"),
            EvalError::MissingClosingParen => write!(f, "Missing closing parenthesis"),
            EvalError::UnknownFunction(name) => write!(f, "Unknown function: {}", name),
            EvalError::UnknownVariable(name) => write!(f, "Unknown variable: {}", name),
            EvalError::InvalidNumber(s) => write!(f, "Invalid number: {}", s),
            EvalError::DivisionByZero => write!(f, "Division by zero"),
            EvalError::InvalidArgCount { func, expected, got } => {
                write!(f, "Function {} expects {} arguments, got {}", func, expected, got)
            }
            EvalError::DomainError(msg) => write!(f, "Domain error: {}", msg),
        }
    }
}

impl std::error::Error for EvalError {}

/// Token types for lexical analysis
#[derive(Debug, Clone, PartialEq)]
enum Token {
    Number(f64),
    Operator(char),
    Function(String),
    Variable(String),
    LeftParen,
    RightParen,
    Comma,
}

/// Mathematical expression evaluator
#[derive(Debug)]
pub struct Evaluator {
    /// User-defined variables
    variables: HashMap<String, f64>,
    /// Built-in functions
    functions: HashMap<String, fn(&[f64]) -> Result<f64, EvalError>>,
}

impl Default for Evaluator {
    fn default() -> Self {
        Self::new()
    }
}

impl Evaluator {
    /// Create a new evaluator with built-in functions and constants
    pub fn new() -> Self {
        let mut eval = Evaluator {
            variables: HashMap::new(),
            functions: HashMap::new(),
        };
        
        // Register built-in functions
        eval.register_builtin_functions();
        
        // Register constants
        eval.variables.insert("pi".to_string(), PI);
        eval.variables.insert("e".to_string(), E);
        
        eval
    }
    
    fn register_builtin_functions(&mut self) {
        // Single-argument functions
        self.functions.insert("sin".to_string(), |args| {
            check_args("sin", 1, args)?;
            Ok(args[0].sin())
        });
        
        self.functions.insert("cos".to_string(), |args| {
            check_args("cos", 1, args)?;
            Ok(args[0].cos())
        });
        
        self.functions.insert("tan".to_string(), |args| {
            check_args("tan", 1, args)?;
            Ok(args[0].tan())
        });
        
        self.functions.insert("asin".to_string(), |args| {
            check_args("asin", 1, args)?;
            if args[0].abs() > 1.0 {
                return Err(EvalError::DomainError("asin argument must be in [-1, 1]".to_string()));
            }
            Ok(args[0].asin())
        });
        
        self.functions.insert("acos".to_string(), |args| {
            check_args("acos", 1, args)?;
            if args[0].abs() > 1.0 {
                return Err(EvalError::DomainError("acos argument must be in [-1, 1]".to_string()));
            }
            Ok(args[0].acos())
        });
        
        self.functions.insert("atan".to_string(), |args| {
            check_args("atan", 1, args)?;
            Ok(args[0].atan())
        });
        
        self.functions.insert("sqrt".to_string(), |args| {
            check_args("sqrt", 1, args)?;
            if args[0] < 0.0 {
                return Err(EvalError::DomainError("sqrt of negative number".to_string()));
            }
            Ok(args[0].sqrt())
        });
        
        self.functions.insert("abs".to_string(), |args| {
            check_args("abs", 1, args)?;
            Ok(args[0].abs())
        });
        
        self.functions.insert("ln".to_string(), |args| {
            check_args("ln", 1, args)?;
            if args[0] <= 0.0 {
                return Err(EvalError::DomainError("ln of non-positive number".to_string()));
            }
            Ok(args[0].ln())
        });
        
        self.functions.insert("log10".to_string(), |args| {
            check_args("log10", 1, args)?;
            if args[0] <= 0.0 {
                return Err(EvalError::DomainError("log10 of non-positive number".to_string()));
            }
            Ok(args[0].log10())
        });
        
        self.functions.insert("log2".to_string(), |args| {
            check_args("log2", 1, args)?;
            if args[0] <= 0.0 {
                return Err(EvalError::DomainError("log2 of non-positive number".to_string()));
            }
            Ok(args[0].log2())
        });
        
        self.functions.insert("exp".to_string(), |args| {
            check_args("exp", 1, args)?;
            Ok(args[0].exp())
        });
        
        self.functions.insert("floor".to_string(), |args| {
            check_args("floor", 1, args)?;
            Ok(args[0].floor())
        });
        
        self.functions.insert("ceil".to_string(), |args| {
            check_args("ceil", 1, args)?;
            Ok(args[0].ceil())
        });
        
        self.functions.insert("round".to_string(), |args| {
            check_args("round", 1, args)?;
            Ok(args[0].round())
        });
        
        self.functions.insert("sign".to_string(), |args| {
            check_args("sign", 1, args)?;
            Ok(args[0].signum())
        });
        
        // Two-argument functions
        self.functions.insert("pow".to_string(), |args| {
            check_args("pow", 2, args)?;
            Ok(args[0].powf(args[1]))
        });
        
        self.functions.insert("log".to_string(), |args| {
            check_args("log", 2, args)?;
            if args[0] <= 0.0 || args[1] <= 0.0 || args[1] == 1.0 {
                return Err(EvalError::DomainError("invalid log arguments".to_string()));
            }
            Ok(args[0].log(args[1]))
        });
        
        self.functions.insert("min".to_string(), |args| {
            check_args("min", 2, args)?;
            Ok(args[0].min(args[1]))
        });
        
        self.functions.insert("max".to_string(), |args| {
            check_args("max", 2, args)?;
            Ok(args[0].max(args[1]))
        });
        
        // Multi-argument functions
        self.functions.insert("sum".to_string(), |args| {
            if args.is_empty() {
                return Err(EvalError::InvalidArgCount { 
                    func: "sum".to_string(), 
                    expected: 1, 
                    got: 0 
                });
            }
            Ok(args.iter().sum())
        });
        
        self.functions.insert("avg".to_string(), |args| {
            if args.is_empty() {
                return Err(EvalError::InvalidArgCount { 
                    func: "avg".to_string(), 
                    expected: 1, 
                    got: 0 
                });
            }
            Ok(args.iter().sum::<f64>() / args.len() as f64)
        });
    }
    
    /// Set a variable value
    pub fn set_var(&mut self, name: &str, value: f64) {
        self.variables.insert(name.to_lowercase(), value);
    }
    
    /// Get a variable value
    pub fn get_var(&self, name: &str) -> Option<f64> {
        self.variables.get(&name.to_lowercase()).copied()
    }
    
    /// Remove a variable
    pub fn remove_var(&mut self, name: &str) {
        self.variables.remove(&name.to_lowercase());
    }
    
    /// Clear all user-defined variables (keeps constants)
    pub fn clear_vars(&mut self) {
        self.variables.retain(|k, _| k == "pi" || k == "e");
    }
    
    /// Register a custom function
    pub fn register_function(&mut self, name: &str, func: fn(&[f64]) -> Result<f64, EvalError>) {
        self.functions.insert(name.to_lowercase(), func);
    }
    
    /// Evaluate an expression string
    pub fn eval(&self, expr: &str) -> Result<f64, EvalError> {
        let tokens = self.tokenize(expr)?;
        let mut pos = 0;
        self.parse_expression(&tokens, &mut pos)
    }
    
    /// Tokenize the input expression
    fn tokenize(&self, expr: &str) -> Result<Vec<Token>, EvalError> {
        let mut tokens = Vec::new();
        let chars: Vec<char> = expr.chars().collect();
        let mut i = 0;
        
        while i < chars.len() {
            let c = chars[i];
            
            // Skip whitespace
            if c.is_whitespace() {
                i += 1;
                continue;
            }
            
            // Number
            if c.is_ascii_digit() || (c == '.' && i + 1 < chars.len() && chars[i + 1].is_ascii_digit()) {
                let start = i;
                let mut has_dot = c == '.';
                
                while i < chars.len() {
                    if chars[i].is_ascii_digit() {
                        i += 1;
                    } else if chars[i] == '.' && !has_dot {
                        has_dot = true;
                        i += 1;
                    } else if chars[i] == 'e' || chars[i] == 'E' {
                        // Scientific notation
                        i += 1;
                        if i < chars.len() && (chars[i] == '+' || chars[i] == '-') {
                            i += 1;
                        }
                    } else {
                        break;
                    }
                }
                
                let num_str: String = chars[start..i].iter().collect();
                let num = num_str.parse::<f64>()
                    .map_err(|_| EvalError::InvalidNumber(num_str))?;
                tokens.push(Token::Number(num));
                continue;
            }
            
            // Identifier (variable or function)
            if c.is_alphabetic() || c == '_' {
                let start = i;
                while i < chars.len() && (chars[i].is_alphanumeric() || chars[i] == '_') {
                    i += 1;
                }
                let name: String = chars[start..i].iter().collect();
                
                // Check if it's a function (followed by '(')
                if i < chars.len() && chars[i] == '(' {
                    tokens.push(Token::Function(name.to_lowercase()));
                } else {
                    tokens.push(Token::Variable(name.to_lowercase()));
                }
                continue;
            }
            
            // Operators and punctuation
            match c {
                '+' | '-' | '*' | '/' | '%' | '^' => {
                    tokens.push(Token::Operator(c));
                }
                '(' => tokens.push(Token::LeftParen),
                ')' => tokens.push(Token::RightParen),
                ',' => tokens.push(Token::Comma),
                _ => return Err(EvalError::UnexpectedChar(c, i)),
            }
            
            i += 1;
        }
        
        Ok(tokens)
    }
    
    /// Parse expression with proper operator precedence
    fn parse_expression(&self, tokens: &[Token], pos: &mut usize) -> Result<f64, EvalError> {
        self.parse_additive(tokens, pos)
    }
    
    /// Parse addition and subtraction (lowest precedence)
    fn parse_additive(&self, tokens: &[Token], pos: &mut usize) -> Result<f64, EvalError> {
        let mut left = self.parse_multiplicative(tokens, pos)?;
        
        while *pos < tokens.len() {
            match &tokens[*pos] {
                Token::Operator('+') => {
                    *pos += 1;
                    let right = self.parse_multiplicative(tokens, pos)?;
                    left += right;
                }
                Token::Operator('-') => {
                    *pos += 1;
                    let right = self.parse_multiplicative(tokens, pos)?;
                    left -= right;
                }
                _ => break,
            }
        }
        
        Ok(left)
    }
    
    /// Parse multiplication, division, and modulo
    fn parse_multiplicative(&self, tokens: &[Token], pos: &mut usize) -> Result<f64, EvalError> {
        let mut left = self.parse_power(tokens, pos)?;
        
        while *pos < tokens.len() {
            match &tokens[*pos] {
                Token::Operator('*') => {
                    *pos += 1;
                    let right = self.parse_power(tokens, pos)?;
                    left *= right;
                }
                Token::Operator('/') => {
                    *pos += 1;
                    let right = self.parse_power(tokens, pos)?;
                    if right == 0.0 {
                        return Err(EvalError::DivisionByZero);
                    }
                    left /= right;
                }
                Token::Operator('%') => {
                    *pos += 1;
                    let right = self.parse_power(tokens, pos)?;
                    if right == 0.0 {
                        return Err(EvalError::DivisionByZero);
                    }
                    left %= right;
                }
                _ => break,
            }
        }
        
        Ok(left)
    }
    
    /// Parse exponentiation (right-associative)
    fn parse_power(&self, tokens: &[Token], pos: &mut usize) -> Result<f64, EvalError> {
        let base = self.parse_unary(tokens, pos)?;
        
        if *pos < tokens.len() && tokens[*pos] == Token::Operator('^') {
            *pos += 1;
            let exp = self.parse_power(tokens, pos)?; // Right-associative
            return Ok(base.powf(exp));
        }
        
        Ok(base)
    }
    
    /// Parse unary operators and primary expressions
    fn parse_unary(&self, tokens: &[Token], pos: &mut usize) -> Result<f64, EvalError> {
        if *pos >= tokens.len() {
            return Err(EvalError::UnexpectedEnd);
        }
        
        match &tokens[*pos] {
            Token::Operator('+') => {
                *pos += 1;
                self.parse_unary(tokens, pos) // Handle consecutive unary operators
            }
            Token::Operator('-') => {
                *pos += 1;
                let val = self.parse_unary(tokens, pos)?; // Handle consecutive unary operators
                Ok(-val)
            }
            _ => self.parse_primary(tokens, pos),
        }
    }
    
    /// Parse primary expressions: numbers, variables, functions, parentheses
    fn parse_primary(&self, tokens: &[Token], pos: &mut usize) -> Result<f64, EvalError> {
        if *pos >= tokens.len() {
            return Err(EvalError::UnexpectedEnd);
        }
        
        match &tokens[*pos].clone() {
            Token::Number(n) => {
                *pos += 1;
                Ok(*n)
            }
            Token::Variable(name) => {
                *pos += 1;
                self.variables.get(name)
                    .copied()
                    .ok_or_else(|| EvalError::UnknownVariable(name.clone()))
            }
            Token::Function(name) => {
                *pos += 1;
                self.parse_function_call(name, tokens, pos)
            }
            Token::LeftParen => {
                *pos += 1;
                let val = self.parse_expression(tokens, pos)?;
                if *pos >= tokens.len() || tokens[*pos] != Token::RightParen {
                    return Err(EvalError::MissingClosingParen);
                }
                *pos += 1;
                Ok(val)
            }
            _ => Err(EvalError::UnexpectedEnd),
        }
    }
    
    /// Parse a function call
    fn parse_function_call(&self, name: &str, tokens: &[Token], pos: &mut usize) -> Result<f64, EvalError> {
        // Expect opening parenthesis
        if *pos >= tokens.len() || tokens[*pos] != Token::LeftParen {
            return Err(EvalError::MissingClosingParen);
        }
        *pos += 1;
        
        // Parse arguments
        let mut args = Vec::new();
        
        // Handle empty argument list
        if *pos < tokens.len() && tokens[*pos] != Token::RightParen {
            args.push(self.parse_expression(tokens, pos)?);
            
            while *pos < tokens.len() && tokens[*pos] == Token::Comma {
                *pos += 1;
                args.push(self.parse_expression(tokens, pos)?);
            }
        }
        
        // Expect closing parenthesis
        if *pos >= tokens.len() || tokens[*pos] != Token::RightParen {
            return Err(EvalError::MissingClosingParen);
        }
        *pos += 1;
        
        // Call the function
        let func = self.functions.get(name)
            .ok_or_else(|| EvalError::UnknownFunction(name.to_string()))?;
        
        func(&args)
    }
}

/// Helper function to check argument count
fn check_args(func: &str, expected: usize, args: &[f64]) -> Result<(), EvalError> {
    if args.len() != expected {
        Err(EvalError::InvalidArgCount {
            func: func.to_string(),
            expected,
            got: args.len(),
        })
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_basic_arithmetic() {
        let eval = Evaluator::new();
        assert_eq!(eval.eval("2 + 3").unwrap(), 5.0);
        assert_eq!(eval.eval("10 - 4").unwrap(), 6.0);
        assert_eq!(eval.eval("3 * 4").unwrap(), 12.0);
        assert_eq!(eval.eval("20 / 5").unwrap(), 4.0);
        assert_eq!(eval.eval("17 % 5").unwrap(), 2.0);
    }
    
    #[test]
    fn test_operator_precedence() {
        let eval = Evaluator::new();
        assert_eq!(eval.eval("2 + 3 * 4").unwrap(), 14.0);
        assert_eq!(eval.eval("10 - 2 * 3").unwrap(), 4.0);
        assert_eq!(eval.eval("2 ^ 3 ^ 2").unwrap(), 512.0); // Right-associative
        assert_eq!(eval.eval("6 / 2 * 3").unwrap(), 9.0);
    }
    
    #[test]
    fn test_parentheses() {
        let eval = Evaluator::new();
        assert_eq!(eval.eval("(2 + 3) * 4").unwrap(), 20.0);
        assert_eq!(eval.eval("((2 + 3) * 4)").unwrap(), 20.0);
        assert_eq!(eval.eval("-(2 + 3)").unwrap(), -5.0);
    }
    
    #[test]
    fn test_unary_operators() {
        let eval = Evaluator::new();
        assert_eq!(eval.eval("-5").unwrap(), -5.0);
        assert_eq!(eval.eval("+5").unwrap(), 5.0);
        assert_eq!(eval.eval("--5").unwrap(), 5.0);
        assert_eq!(eval.eval("-(-5)").unwrap(), 5.0);
    }
    
    #[test]
    fn test_constants() {
        let eval = Evaluator::new();
        assert!((eval.eval("pi").unwrap() - std::f64::consts::PI).abs() < 1e-10);
        assert!((eval.eval("e").unwrap() - std::f64::consts::E).abs() < 1e-10);
    }
    
    #[test]
    fn test_variables() {
        let mut eval = Evaluator::new();
        eval.set_var("x", 10.0);
        eval.set_var("y", 5.0);
        assert_eq!(eval.eval("x + y").unwrap(), 15.0);
        assert_eq!(eval.eval("x * y").unwrap(), 50.0);
        assert_eq!(eval.eval("x / y").unwrap(), 2.0);
    }
    
    #[test]
    fn test_functions() {
        let eval = Evaluator::new();
        assert_eq!(eval.eval("sqrt(16)").unwrap(), 4.0);
        assert_eq!(eval.eval("abs(-5)").unwrap(), 5.0);
        assert_eq!(eval.eval("pow(2, 10)").unwrap(), 1024.0);
        assert_eq!(eval.eval("floor(3.7)").unwrap(), 3.0);
        assert_eq!(eval.eval("ceil(3.2)").unwrap(), 4.0);
        assert_eq!(eval.eval("round(3.5)").unwrap(), 4.0);
    }
    
    #[test]
    fn test_trig_functions() {
        let eval = Evaluator::new();
        
        assert!((eval.eval("sin(0)").unwrap() - 0.0).abs() < 1e-10);
        assert!((eval.eval("cos(0)").unwrap() - 1.0).abs() < 1e-10);
        assert!((eval.eval("sin(pi/2)").unwrap() - 1.0).abs() < 1e-10);
        assert!((eval.eval("tan(pi/4)").unwrap() - 1.0).abs() < 1e-10);
    }
    
    #[test]
    fn test_log_functions() {
        let eval = Evaluator::new();
        
        assert!((eval.eval("ln(e)").unwrap() - 1.0).abs() < 1e-10);
        assert!((eval.eval("log10(100)").unwrap() - 2.0).abs() < 1e-10);
        assert!((eval.eval("log2(8)").unwrap() - 3.0).abs() < 1e-10);
        assert!((eval.eval("exp(0)").unwrap() - 1.0).abs() < 1e-10);
    }
    
    #[test]
    fn test_min_max() {
        let eval = Evaluator::new();
        assert_eq!(eval.eval("min(5, 3)").unwrap(), 3.0);
        assert_eq!(eval.eval("max(5, 3)").unwrap(), 5.0);
        assert_eq!(eval.eval("min(-10, 10)").unwrap(), -10.0);
    }
    
    #[test]
    fn test_sum_avg() {
        let eval = Evaluator::new();
        assert_eq!(eval.eval("sum(1, 2, 3, 4, 5)").unwrap(), 15.0);
        assert_eq!(eval.eval("avg(10, 20, 30)").unwrap(), 20.0);
    }
    
    #[test]
    fn test_complex_expressions() {
        let eval = Evaluator::new();
        assert_eq!(eval.eval("2 + 3 * 4 - 5").unwrap(), 9.0);
        assert_eq!(eval.eval("(1 + 2) * (3 + 4)").unwrap(), 21.0);
        assert_eq!(eval.eval("sqrt(16) + pow(2, 3)").unwrap(), 12.0);
        assert!((eval.eval("sin(pi/4) ^ 2 + cos(pi/4) ^ 2").unwrap() - 1.0).abs() < 1e-10);
    }
    
    #[test]
    fn test_scientific_notation() {
        let eval = Evaluator::new();
        assert_eq!(eval.eval("1e3").unwrap(), 1000.0);
        assert_eq!(eval.eval("2.5e-2").unwrap(), 0.025);
        assert_eq!(eval.eval("1E+2").unwrap(), 100.0);
    }
    
    #[test]
    fn test_whitespace() {
        let eval = Evaluator::new();
        assert_eq!(eval.eval("  2  +  3  ").unwrap(), 5.0);
        assert_eq!(eval.eval("\n2\n+\n3\n").unwrap(), 5.0);
        assert_eq!(eval.eval("\t2\t+\t3\t").unwrap(), 5.0);
    }
    
    #[test]
    fn test_errors() {
        let eval = Evaluator::new();
        
        assert!(matches!(eval.eval("1 / 0"), Err(EvalError::DivisionByZero)));
        assert!(matches!(eval.eval("unknown_var"), Err(EvalError::UnknownVariable(_))));
        assert!(matches!(eval.eval("unknown_func()"), Err(EvalError::UnknownFunction(_))));
        assert!(matches!(eval.eval("(1 + 2"), Err(EvalError::MissingClosingParen)));
        assert!(matches!(eval.eval("sqrt(-1)"), Err(EvalError::DomainError(_))));
    }
    
    #[test]
    fn test_custom_function() {
        let mut eval = Evaluator::new();
        eval.register_function("double", |args| {
            check_args("double", 1, args)?;
            Ok(args[0] * 2.0)
        });
        
        assert_eq!(eval.eval("double(5)").unwrap(), 10.0);
        assert_eq!(eval.eval("double(3) + double(4)").unwrap(), 14.0);
    }
    
    #[test]
    fn test_case_insensitivity() {
        let mut eval = Evaluator::new();
        eval.set_var("X", 5.0);
        
        assert_eq!(eval.eval("X + x").unwrap(), 10.0);
        assert_eq!(eval.eval("SQRT(16)").unwrap(), 4.0);
        assert_eq!(eval.eval("PI").unwrap(), std::f64::consts::PI);
    }
}