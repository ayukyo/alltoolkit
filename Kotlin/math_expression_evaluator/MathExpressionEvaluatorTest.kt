/**
 * MathExpressionEvaluator 单元测试
 * 
 * @author AllToolkit
 * @date 2026-05-15
 */

package com.alltoolkit.math

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertTrue
import kotlin.math.*

class MathExpressionEvaluatorTest {
    
    private val evaluator = MathExpressionEvaluator()
    
    // ==================== 基础运算测试 ====================
    
    @Test
    fun `test basic addition`() {
        assertEquals(5.0, evaluator.eval("2 + 3"))
        assertEquals(0.0, evaluator.eval("0 + 0"))
        assertEquals(-1.0, evaluator.eval("-2 + 1"))
        assertEquals(100.0, evaluator.eval("50 + 50"))
    }
    
    @Test
    fun `test basic subtraction`() {
        assertEquals(2.0, evaluator.eval("5 - 3"))
        assertEquals(-5.0, evaluator.eval("0 - 5"))
        assertEquals(0.0, evaluator.eval("10 - 10"))
        assertEquals(15.0, evaluator.eval("20 - 5"))
    }
    
    @Test
    fun `test basic multiplication`() {
        assertEquals(6.0, evaluator.eval("2 * 3"))
        assertEquals(0.0, evaluator.eval("0 * 100"))
        assertEquals(-6.0, evaluator.eval("-2 * 3"))
        assertEquals(100.0, evaluator.eval("10 * 10"))
    }
    
    @Test
    fun `test basic division`() {
        assertEquals(2.0, evaluator.eval("6 / 3"))
        assertEquals(0.5, evaluator.eval("1 / 2"))
        assertEquals(-2.0, evaluator.eval("-6 / 3"))
        assertEquals(3.3333333333333335, evaluator.eval("10 / 3"))
    }
    
    @Test
    fun `test division by zero throws exception`() {
        assertFailsWith<IllegalArgumentException> {
            evaluator.eval("1 / 0")
        }
    }
    
    @Test
    fun `test modulo`() {
        assertEquals(1.0, evaluator.eval("7 % 3"))
        assertEquals(0.0, evaluator.eval("9 % 3"))
        assertEquals(2.0, evaluator.eval("5 % 3"))
        assertEquals(0.5, evaluator.eval("2.5 % 1"))
    }
    
    @Test
    fun `test power`() {
        assertEquals(8.0, evaluator.eval("2 ^ 3"))
        assertEquals(1.0, evaluator.eval("5 ^ 0"))
        assertEquals(0.25, evaluator.eval("2 ^ -2"))
        assertEquals(9.0, evaluator.eval("3 ^ 2"))
    }
    
    // ==================== 运算优先级测试 ====================
    
    @Test
    fun `test operator precedence`() {
        assertEquals(14.0, evaluator.eval("2 + 3 * 4"))
        assertEquals(20.0, evaluator.eval("(2 + 3) * 4"))
        assertEquals(8.0, evaluator.eval("2 ^ 3 ^ 1"))  // 右结合: 2^(3^1) = 8
        assertEquals(6.0, evaluator.eval("10 - 2 * 2"))
    }
    
    @Test
    fun `test parentheses`() {
        assertEquals(9.0, evaluator.eval("(2 + 1) * 3"))
        assertEquals(5.0, evaluator.eval("((2 + 3))"))
        assertEquals(21.0, evaluator.eval("(1 + 2) * (3 + 4)"))
        assertEquals(2.0, evaluator.eval("((2))"))
    }
    
    @Test
    fun `test nested parentheses`() {
        assertEquals(26.0, evaluator.eval("((1 + 2) * (3 + 4)) + 5"))
        assertEquals(14.0, evaluator.eval("2 * (3 + 4)"))
        assertEquals(50.0, evaluator.eval("2 * (3 + 4 * 5)"))
    }
    
    // ==================== 一元运算符测试 ====================
    
    @Test
    fun `test unary plus`() {
        assertEquals(5.0, evaluator.eval("+5"))
        assertEquals(3.0, evaluator.eval("+(2 + 1)"))
    }
    
    @Test
    fun `test unary minus`() {
        assertEquals(-5.0, evaluator.eval("-5"))
        assertEquals(5.0, evaluator.eval("--5"))
        assertEquals(-3.0, evaluator.eval("-(2 + 1)"))
        assertEquals(-8.0, evaluator.eval("-2 * 4"))
        assertEquals(-6.0, evaluator.eval("2 * -3"))
    }
    
    // ==================== 三角函数测试 ====================
    
    @Test
    fun `test sin function`() {
        assertEquals(0.0, evaluator.eval("sin(0)"), 1e-10)
        assertEquals(1.0, evaluator.eval("sin(pi/2)"), 1e-10)
        assertEquals(0.0, evaluator.eval("sin(pi)"), 1e-10)
    }
    
    @Test
    fun `test cos function`() {
        assertEquals(1.0, evaluator.eval("cos(0)"), 1e-10)
        assertEquals(0.0, evaluator.eval("cos(pi/2)"), 1e-10)
        assertEquals(-1.0, evaluator.eval("cos(pi)"), 1e-10)
    }
    
    @Test
    fun `test tan function`() {
        assertEquals(0.0, evaluator.eval("tan(0)"), 1e-10)
        assertEquals(1.0, evaluator.eval("tan(pi/4)"), 1e-10)
    }
    
    // ==================== 数学函数测试 ====================
    
    @Test
    fun `test sqrt function`() {
        assertEquals(2.0, evaluator.eval("sqrt(4)"))
        assertEquals(3.0, evaluator.eval("sqrt(9)"))
        assertEquals(1.4142135623730951, evaluator.eval("sqrt(2)"), 1e-10)
    }
    
    @Test
    fun `test sqrt negative throws exception`() {
        assertFailsWith<IllegalArgumentException> {
            evaluator.eval("sqrt(-1)")
        }
    }
    
    @Test
    fun `test abs function`() {
        assertEquals(5.0, evaluator.eval("abs(5)"))
        assertEquals(5.0, evaluator.eval("abs(-5)"))
        assertEquals(0.0, evaluator.eval("abs(0)"))
    }
    
    @Test
    fun `test log functions`() {
        assertEquals(1.0, evaluator.eval("log(10)"))
        assertEquals(2.0, evaluator.eval("log(100)"))
        assertEquals(ln(E), evaluator.eval("ln(e)"), 1e-10)
    }
    
    @Test
    fun `test exp function`() {
        assertEquals(1.0, evaluator.eval("exp(0)"))
        assertEquals(E, evaluator.eval("exp(1)"), 1e-10)
    }
    
    @Test
    fun `test floor and ceil`() {
        assertEquals(2.0, evaluator.eval("floor(2.9)"))
        assertEquals(-3.0, evaluator.eval("floor(-2.1)"))
        assertEquals(3.0, evaluator.eval("ceil(2.1)"))
        assertEquals(-2.0, evaluator.eval("ceil(-2.9)"))
    }
    
    @Test
    fun `test round function`() {
        assertEquals(3.0, evaluator.eval("round(2.5)"))
        assertEquals(2.0, evaluator.eval("round(2.4)"))
        assertEquals(-3.0, evaluator.eval("round(-2.5)"))
    }
    
    // ==================== 多参数函数测试 ====================
    
    @Test
    fun `test pow function`() {
        assertEquals(8.0, evaluator.eval("pow(2, 3)"))
        assertEquals(4.0, evaluator.eval("pow(16, 0.5)"))
        assertEquals(1.0, evaluator.eval("pow(5, 0)"))
    }
    
    @Test
    fun `test max function`() {
        assertEquals(5.0, evaluator.eval("max(1, 5)"))
        assertEquals(3.0, evaluator.eval("max(1, 2, 3)"))
        assertEquals(-1.0, evaluator.eval("max(-5, -1, -3)"))
    }
    
    @Test
    fun `test min function`() {
        assertEquals(1.0, evaluator.eval("min(1, 5)"))
        assertEquals(1.0, evaluator.eval("min(1, 2, 3)"))
        assertEquals(-5.0, evaluator.eval("min(-5, -1, -3)"))
    }
    
    @Test
    fun `test avg function`() {
        assertEquals(3.0, evaluator.eval("avg(1, 5)"))
        assertEquals(2.0, evaluator.eval("avg(1, 2, 3)"))
        assertEquals(0.0, evaluator.eval("avg(-1, 0, 1)"))
    }
    
    @Test
    fun `test sum function`() {
        assertEquals(6.0, evaluator.eval("sum(1, 2, 3)"))
        assertEquals(0.0, evaluator.eval("sum(-1, 0, 1)"))
        assertEquals(15.0, evaluator.eval("sum(1, 2, 3, 4, 5)"))
    }
    
    // ==================== 常量测试 ====================
    
    @Test
    fun `test pi constant`() {
        assertEquals(PI, evaluator.eval("pi"))
        assertEquals(2 * PI, evaluator.eval("2 * pi"))
    }
    
    @Test
    fun `test e constant`() {
        assertEquals(E, evaluator.eval("e"))
        assertEquals(E * E, evaluator.eval("e ^ 2"))
    }
    
    // ==================== 变量测试 ====================
    
    @Test
    fun `test single variable`() {
        assertEquals(10.0, evaluator.evaluate("x", mapOf("x" to 10.0)))
        assertEquals(25.0, evaluator.evaluate("x * x", mapOf("x" to 5.0)))
    }
    
    @Test
    fun `test multiple variables`() {
        assertEquals(11.0, evaluator.evaluate("x + y", mapOf("x" to 5.0, "y" to 6.0)))
        assertEquals(30.0, evaluator.evaluate("x * y", mapOf("x" to 5.0, "y" to 6.0)))
        assertEquals(14.0, evaluator.evaluate("2*x + 3*y", mapOf("x" to 4.0, "y" to 2.0)))
    }
    
    @Test
    fun `test variable with function`() {
        assertEquals(5.0, evaluator.evaluate("sqrt(x)", mapOf("x" to 25.0)))
        assertEquals(sin(0.5), evaluator.evaluate("sin(x)", mapOf("x" to 0.5)), 1e-10)
    }
    
    @Test
    fun `test unknown variable throws exception`() {
        assertFailsWith<IllegalArgumentException> {
            evaluator.eval("x + 1")
        }
    }
    
    // ==================== 复杂表达式测试 ====================
    
    @Test
    fun `test complex expressions`() {
        // 物理公式: v = sqrt(2*g*h)
        val result1 = evaluator.evaluate("sqrt(2 * g * h)", mapOf("g" to 9.8, "h" to 10.0))
        assertEquals(sqrt(2.0 * 9.8 * 10.0), result1, 1e-10)
        
        // 二次方程: (-b + sqrt(b^2 - 4*a*c)) / (2*a)
        val vars = mapOf("a" to 1.0, "b" to -5.0, "c" to 6.0)
        val result2 = evaluator.evaluate("(-b + sqrt(b^2 - 4*a*c)) / (2*a)", vars)
        assertEquals(3.0, result2, 1e-10)
        
        // 欧拉公式相关: e^(i*pi) + 1 = 0 (这里只测试实部)
        assertEquals(-1.0, evaluator.eval("cos(pi)"), 1e-10)
    }
    
    @Test
    fun `test expression with spaces`() {
        assertEquals(7.0, evaluator.eval(" 2 + 5 "))
        assertEquals(9.0, evaluator.eval("2 + 3 * 4 - 5"))
        assertEquals(7.0, evaluator.eval("( 1 + 2 ) * 3 - 2"))
    }
    
    @Test
    fun `test decimal numbers`() {
        assertEquals(0.3, evaluator.eval("0.1 + 0.2"), 1e-10)
        assertEquals(3.14159, evaluator.eval("3.14159"))
        assertEquals(2.5, evaluator.eval("5.0 / 2.0"))
    }
    
    @Test
    fun `test scientific notation`() {
        assertEquals(1000.0, evaluator.eval("1e3"))
        assertEquals(0.001, evaluator.eval("1e-3"))
        assertEquals(1200.0, evaluator.eval("1.2e3"))
    }
    
    // ==================== 错误处理测试 ====================
    
    @Test
    fun `test empty expression throws exception`() {
        assertFailsWith<IllegalArgumentException> {
            evaluator.eval("")
        }
    }
    
    @Test
    fun `test unmatched parenthesis throws exception`() {
        assertFailsWith<IllegalArgumentException> {
            evaluator.eval("(2 + 3")
        }
        assertFailsWith<IllegalArgumentException> {
            evaluator.eval("2 + 3)")
        }
    }
    
    @Test
    fun `test invalid character throws exception`() {
        assertFailsWith<IllegalArgumentException> {
            evaluator.eval("2 @ 3")
        }
    }
    
    @Test
    fun `test unknown function throws exception`() {
        assertFailsWith<IllegalArgumentException> {
            evaluator.eval("unknown(5)")
        }
    }
    
    @Test
    fun `test wrong number of arguments throws exception`() {
        assertFailsWith<IllegalArgumentException> {
            evaluator.eval("sqrt(4, 2)")
        }
    }
    
    // ==================== 扩展函数测试 ====================
    
    @Test
    fun `test extension function`() {
        assertEquals(5.0, "2 + 3".evalMath())
        assertEquals(10.0, "x + y".evalMath("x" to 5, "y" to 5))
        assertEquals(8.0, "2 ^ 3".evalMath())
    }
}

class ExpressionValidatorTest {
    
    @Test
    fun `test valid expressions`() {
        assertTrue(ExpressionValidator.isValid("2 + 3"))
        assertTrue(ExpressionValidator.isValid("sin(pi/2)"))
        assertTrue(ExpressionValidator.isValid("sqrt(4) + max(1,2,3)"))
    }
    
    @Test
    fun `test invalid expressions`() {
        assertTrue(!ExpressionValidator.isValid("2 + "))
        assertTrue(!ExpressionValidator.isValid("(2 + 3"))
        assertTrue(!ExpressionValidator.isValid("unknown_func(5)"))
    }
    
    @Test
    fun `test extract variables`() {
        val vars = ExpressionValidator.extractVariables("x + y * z")
        assertEquals(setOf("x", "y", "z"), vars)
        
        val vars2 = ExpressionValidator.extractVariables("sin(x) + cos(y)")
        assertEquals(setOf("x", "y"), vars2)
        
        val vars3 = ExpressionValidator.extractVariables("pi + e")
        assertTrue(vars3.isEmpty())
    }
    
    @Test
    fun `test balanced parentheses`() {
        assertTrue(ExpressionValidator.hasBalancedParentheses("(2 + 3)"))
        assertTrue(ExpressionValidator.hasBalancedParentheses("((1 + 2) * 3)"))
        assertTrue(!ExpressionValidator.hasBalancedParentheses("(2 + 3"))
        assertTrue(!ExpressionValidator.hasBalancedParentheses("2 + 3)"))
    }
}

class ExpressionSimplifierTest {
    
    @Test
    fun `test simplify removes spaces`() {
        assertEquals("2+3", ExpressionSimplifier.simplify("2 + 3"))
        assertEquals("2+3*4", ExpressionSimplifier.simplify(" 2 + 3 * 4 "))
    }
    
    @Test
    fun `test simplify double operators`() {
        assertEquals("2+3", ExpressionSimplifier.simplify("2++3"))
        assertEquals("2+3", ExpressionSimplifier.simplify("2--3"))
        assertEquals("2-3", ExpressionSimplifier.simplify("2+-3"))
        assertEquals("2-3", ExpressionSimplifier.simplify("2-+3"))
    }
}