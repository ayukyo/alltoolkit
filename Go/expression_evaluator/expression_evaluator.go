// Package expression_evaluator provides a mathematical expression parser and evaluator.
// Supports basic arithmetic, parentheses, functions, and variables with zero external dependencies.
package expression_evaluator

import (
	"errors"
	"fmt"
	"math"
	"strconv"
	"strings"
	"unicode"
)

// ExpressionEvaluator parses and evaluates mathematical expressions
type ExpressionEvaluator struct {
	variables map[string]float64
	functions map[string]func([]float64) (float64, error)
}

// New creates a new ExpressionEvaluator with default operators and functions
func New() *ExpressionEvaluator {
	e := &ExpressionEvaluator{
		variables: make(map[string]float64),
		functions: make(map[string]func([]float64) (float64, error)),
	}

	// Register default functions
	e.RegisterFunction1("sin", math.Sin)
	e.RegisterFunction1("cos", math.Cos)
	e.RegisterFunction1("tan", math.Tan)
	e.RegisterFunction1("asin", math.Asin)
	e.RegisterFunction1("acos", math.Acos)
	e.RegisterFunction1("atan", math.Atan)
	e.RegisterFunction1("sinh", math.Sinh)
	e.RegisterFunction1("cosh", math.Cosh)
	e.RegisterFunction1("tanh", math.Tanh)
	e.RegisterFunction1("sqrt", math.Sqrt)
	e.RegisterFunction1("cbrt", math.Cbrt)
	e.RegisterFunction1("abs", math.Abs)
	e.RegisterFunction1("ceil", math.Ceil)
	e.RegisterFunction1("floor", math.Floor)
	e.RegisterFunction1("round", math.Round)
	e.RegisterFunction1("log", math.Log)
	e.RegisterFunction1("log10", math.Log10)
	e.RegisterFunction1("log2", math.Log2)
	e.RegisterFunction1("exp", math.Exp)
	e.RegisterFunction1("ln", math.Log)

	// Multi-argument functions
	e.RegisterFunctionN("min", func(args []float64) (float64, error) {
		if len(args) == 0 {
			return 0, errors.New("min requires at least one argument")
		}
		result := args[0]
		for _, v := range args[1:] {
			if v < result {
				result = v
			}
		}
		return result, nil
	})

	e.RegisterFunctionN("max", func(args []float64) (float64, error) {
		if len(args) == 0 {
			return 0, errors.New("max requires at least one argument")
		}
		result := args[0]
		for _, v := range args[1:] {
			if v > result {
				result = v
			}
		}
		return result, nil
	})

	e.RegisterFunctionN("avg", func(args []float64) (float64, error) {
		if len(args) == 0 {
			return 0, errors.New("avg requires at least one argument")
		}
		sum := 0.0
		for _, v := range args {
			sum += v
		}
		return sum / float64(len(args)), nil
	})

	e.RegisterFunctionN("sum", func(args []float64) (float64, error) {
		sum := 0.0
		for _, v := range args {
			sum += v
		}
		return sum, nil
	})

	// Register default variables (constants)
	e.SetVariable("pi", math.Pi)
	e.SetVariable("e", math.E)
	e.SetVariable("phi", math.Phi)

	return e
}

// RegisterFunction1 adds a single-argument function
func (e *ExpressionEvaluator) RegisterFunction1(name string, fn func(float64) float64) {
	e.functions[name] = func(args []float64) (float64, error) {
		if len(args) != 1 {
			return 0, fmt.Errorf("%s expects 1 argument, got %d", name, len(args))
		}
		return fn(args[0]), nil
	}
}

// RegisterFunctionN adds a function with variable arguments
func (e *ExpressionEvaluator) RegisterFunctionN(name string, fn func([]float64) (float64, error)) {
	e.functions[name] = fn
}

// SetVariable sets a variable value
func (e *ExpressionEvaluator) SetVariable(name string, value float64) {
	e.variables[name] = value
}

// GetVariable gets a variable value
func (e *ExpressionEvaluator) GetVariable(name string) (float64, bool) {
	v, ok := e.variables[name]
	return v, ok
}

// ClearVariables removes all user-defined variables (keeps constants)
func (e *ExpressionEvaluator) ClearVariables() {
	pi := e.variables["pi"]
	eVar := e.variables["e"]
	phi := e.variables["phi"]
	
	e.variables = make(map[string]float64)
	e.variables["pi"] = pi
	e.variables["e"] = eVar
	e.variables["phi"] = phi
}

// Parser state
type parser struct {
	expr string
	pos  int
	eval *ExpressionEvaluator
}

// Evaluate parses and evaluates a mathematical expression
func (e *ExpressionEvaluator) Evaluate(expr string) (float64, error) {
	p := &parser{
		expr: strings.TrimSpace(expr),
		pos:  0,
		eval: e,
	}
	
	result, err := p.parseExpression()
	if err != nil {
		return 0, err
	}
	
	p.skipWhitespace()
	if p.pos < len(p.expr) {
		return 0, fmt.Errorf("unexpected character at position %d: %c", p.pos, p.expr[p.pos])
	}
	
	return result, nil
}

// parseExpression parses addition and subtraction (lowest precedence)
func (p *parser) parseExpression() (float64, error) {
	left, err := p.parseTerm()
	if err != nil {
		return 0, err
	}
	
	for {
		p.skipWhitespace()
		if p.pos >= len(p.expr) {
			break
		}
		
		op := p.expr[p.pos]
		if op != '+' && op != '-' {
			break
		}
		p.pos++
		
		right, err := p.parseTerm()
		if err != nil {
			return 0, err
		}
		
		if op == '+' {
			left = left + right
		} else {
			left = left - right
		}
	}
	
	return left, nil
}

// parseTerm parses multiplication, division, and modulo
func (p *parser) parseTerm() (float64, error) {
	left, err := p.parseFactor()
	if err != nil {
		return 0, err
	}
	
	for {
		p.skipWhitespace()
		if p.pos >= len(p.expr) {
			break
		}
		
		op := p.expr[p.pos]
		if op != '*' && op != '/' && op != '%' {
			break
		}
		p.pos++
		
		right, err := p.parseFactor()
		if err != nil {
			return 0, err
		}
		
		switch op {
		case '*':
			left = left * right
		case '/':
			if right == 0 {
				return 0, errors.New("division by zero")
			}
			left = left / right
		case '%':
			left = math.Mod(left, right)
		}
	}
	
	return left, nil
}

// parseFactor parses exponentiation (highest precedence for binary ops)
func (p *parser) parseFactor() (float64, error) {
	left, err := p.parseUnary()
	if err != nil {
		return 0, err
	}
	
	p.skipWhitespace()
	if p.pos < len(p.expr) && p.expr[p.pos] == '^' {
		p.pos++
		right, err := p.parseFactor() // Right associative
		if err != nil {
			return 0, err
		}
		left = math.Pow(left, right)
	}
	
	return left, nil
}

// parseUnary handles unary plus and minus
func (p *parser) parseUnary() (float64, error) {
	p.skipWhitespace()
	
	if p.pos >= len(p.expr) {
		return 0, errors.New("unexpected end of expression")
	}
	
	if p.expr[p.pos] == '+' {
		p.pos++
		return p.parseUnary()
	}
	
	if p.expr[p.pos] == '-' {
		p.pos++
		val, err := p.parseUnary()
		if err != nil {
			return 0, err
		}
		return -val, nil
	}
	
	return p.parsePrimary()
}

// parsePrimary handles numbers, identifiers, and parenthesized expressions
func (p *parser) parsePrimary() (float64, error) {
	p.skipWhitespace()
	
	if p.pos >= len(p.expr) {
		return 0, errors.New("unexpected end of expression")
	}
	
	// Parenthesized expression
	if p.expr[p.pos] == '(' {
		p.pos++
		result, err := p.parseExpression()
		if err != nil {
			return 0, err
		}
		p.skipWhitespace()
		if p.pos >= len(p.expr) || p.expr[p.pos] != ')' {
			return 0, errors.New("missing closing parenthesis")
		}
		p.pos++
		return result, nil
	}
	
	// Number
	if unicode.IsDigit(rune(p.expr[p.pos])) || p.expr[p.pos] == '.' {
		return p.parseNumber()
	}
	
	// Identifier (variable or function)
	if unicode.IsLetter(rune(p.expr[p.pos])) || p.expr[p.pos] == '_' {
		return p.parseIdentifier()
	}
	
	return 0, fmt.Errorf("unexpected character: %c", p.expr[p.pos])
}

// parseNumber parses a numeric literal
func (p *parser) parseNumber() (float64, error) {
	start := p.pos
	hasDot := false
	
	for p.pos < len(p.expr) {
		c := rune(p.expr[p.pos])
		if unicode.IsDigit(c) {
			p.pos++
		} else if c == '.' && !hasDot {
			hasDot = true
			p.pos++
		} else {
			break
		}
	}
	
	str := p.expr[start:p.pos]
	val, err := strconv.ParseFloat(str, 64)
	if err != nil {
		return 0, fmt.Errorf("invalid number: %s", str)
	}
	
	return val, nil
}

// parseIdentifier parses a variable or function call
func (p *parser) parseIdentifier() (float64, error) {
	start := p.pos
	
	for p.pos < len(p.expr) {
		c := rune(p.expr[p.pos])
		if unicode.IsLetter(c) || unicode.IsDigit(c) || c == '_' {
			p.pos++
		} else {
			break
		}
	}
	
	name := p.expr[start:p.pos]
	
	p.skipWhitespace()
	
	// Check if it's a function call
	if p.pos < len(p.expr) && p.expr[p.pos] == '(' {
		p.pos++
		args, err := p.parseFunctionArgs()
		if err != nil {
			return 0, err
		}
		
		p.skipWhitespace()
		if p.pos >= len(p.expr) || p.expr[p.pos] != ')' {
			return 0, fmt.Errorf("missing closing parenthesis for function %s", name)
		}
		p.pos++
		
		fn, ok := p.eval.functions[name]
		if !ok {
			return 0, fmt.Errorf("unknown function: %s", name)
		}
		
		return fn(args)
	}
	
	// It's a variable
	val, ok := p.eval.variables[name]
	if !ok {
		return 0, fmt.Errorf("undefined variable: %s", name)
	}
	
	return val, nil
}

// parseFunctionArgs parses function arguments separated by commas
func (p *parser) parseFunctionArgs() ([]float64, error) {
	var args []float64
	
	p.skipWhitespace()
	
	// Empty argument list
	if p.pos < len(p.expr) && p.expr[p.pos] == ')' {
		return args, nil
	}
	
	for {
		arg, err := p.parseExpression()
		if err != nil {
			return nil, err
		}
		args = append(args, arg)
		
		p.skipWhitespace()
		if p.pos >= len(p.expr) || p.expr[p.pos] != ',' {
			break
		}
		p.pos++
	}
	
	return args, nil
}

// skipWhitespace skips whitespace characters
func (p *parser) skipWhitespace() {
	for p.pos < len(p.expr) && unicode.IsSpace(rune(p.expr[p.pos])) {
		p.pos++
	}
}

// EvaluateAsString evaluates and returns the result as a string
func (e *ExpressionEvaluator) EvaluateAsString(expr string) (string, error) {
	result, err := e.Evaluate(expr)
	if err != nil {
		return "", err
	}
	s := strconv.FormatFloat(result, 'f', -1, 64)
	return s, nil
}

// IsExpressionValid checks if an expression is syntactically valid
func (e *ExpressionEvaluator) IsExpressionValid(expr string) bool {
	_, err := e.Evaluate(expr)
	return err == nil
}

// GetSupportedFunctions returns a list of supported functions
func (e *ExpressionEvaluator) GetSupportedFunctions() []string {
	result := make([]string, 0, len(e.functions))
	for name := range e.functions {
		result = append(result, name)
	}
	return result
}

// GetVariables returns all defined variables
func (e *ExpressionEvaluator) GetVariables() map[string]float64 {
	result := make(map[string]float64)
	for k, v := range e.variables {
		result[k] = v
	}
	return result
}

// ParseAndExplain parses an expression and returns a detailed explanation
func (e *ExpressionEvaluator) ParseAndExplain(expr string) (string, error) {
	result, err := e.Evaluate(expr)
	if err != nil {
		return "", err
	}

	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("Expression: %s\n", expr))
	sb.WriteString(fmt.Sprintf("Result: %v\n", result))
	sb.WriteString("\nVariables used:\n")
	
	for k, v := range e.variables {
		sb.WriteString(fmt.Sprintf("  %s = %v\n", k, v))
	}

	return sb.String(), nil
}