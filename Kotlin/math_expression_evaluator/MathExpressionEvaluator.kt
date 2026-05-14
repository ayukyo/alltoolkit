/**
 * MathExpressionEvaluator - 数学表达式计算器
 * 
 * 支持功能：
 * - 四则运算：+、-、*、/
 * - 幂运算：^
 * - 取模：%
 * - 括号：()
 * - 数学函数：sin、cos、tan、sqrt、abs、log、ln、exp、floor、ceil、round
 * - 常量：pi、e
 * - 变量绑定
 * - 一元运算符：+、-
 * 
 * 零外部依赖，纯 Kotlin 标准库实现
 * 
 * @author AllToolkit
 * @date 2026-05-15
 */

package com.alltoolkit.math

import kotlin.math.*

/**
 * 数学表达式计算器
 */
class MathExpressionEvaluator {
    
    private var expression: String = ""
    private var pos: Int = 0
    private var variables: Map<String, Double> = emptyMap()
    
    /**
     * 计算表达式结果
     * @param expr 数学表达式字符串
     * @param vars 变量映射表，可选
     * @return 计算结果
     * @throws IllegalArgumentException 如果表达式无效
     */
    fun evaluate(expr: String, vars: Map<String, Double> = emptyMap()): Double {
        this.expression = expr.replace("\\s+".toRegex(), "")
        this.pos = 0
        this.variables = vars
        
        if (this.expression.isEmpty()) {
            throw IllegalArgumentException("表达式不能为空")
        }
        
        val result = parseExpression()
        
        if (pos < expression.length) {
            throw IllegalArgumentException("表达式解析未完成，位置: $pos, 剩余: ${expression.substring(pos)}")
        }
        
        return result
    }
    
    /**
     * 计算表达式结果（简化版）
     */
    fun eval(expr: String): Double = evaluate(expr)
    
    // 解析表达式（处理加减法）
    private fun parseExpression(): Double {
        var result = parseTerm()
        
        while (pos < expression.length) {
            when (currentChar()) {
                '+' -> {
                    advance()
                    result += parseTerm()
                }
                '-' -> {
                    advance()
                    result -= parseTerm()
                }
                else -> break
            }
        }
        
        return result
    }
    
    // 解析项（处理乘除取模）
    private fun parseTerm(): Double {
        var result = parsePower()
        
        while (pos < expression.length) {
            when (currentChar()) {
                '*' -> {
                    advance()
                    result *= parsePower()
                }
                '/' -> {
                    advance()
                    val divisor = parsePower()
                    if (divisor == 0.0) {
                        throw IllegalArgumentException("除零错误")
                    }
                    result /= divisor
                }
                '%' -> {
                    advance()
                    val divisor = parsePower()
                    if (divisor == 0.0) {
                        throw IllegalArgumentException("取模除零错误")
                    }
                    result %= divisor
                }
                else -> break
            }
        }
        
        return result
    }
    
    // 解析幂运算
    private fun parsePower(): Double {
        var result = parseUnary()
        
        if (pos < expression.length && currentChar() == '^') {
            advance()
            val exponent = parsePower() // 右结合
            result = result.pow(exponent)
        }
        
        return result
    }
    
    // 解析一元运算符
    private fun parseUnary(): Double {
        return when (currentChar()) {
            '+' -> {
                advance()
                parseFactor()
            }
            '-' -> {
                advance()
                -parseFactor()
            }
            else -> parseFactor()
        }
    }
    
    // 解析因子（数字、括号、函数、变量）
    private fun parseFactor(): Double {
        // 处理括号
        if (currentChar() == '(') {
            advance()
            val result = parseExpression()
            if (currentChar() != ')') {
                throw IllegalArgumentException("缺少右括号")
            }
            advance()
            return result
        }
        
        // 处理数字
        if (currentChar().isDigit() || currentChar() == '.') {
            return parseNumber()
        }
        
        // 处理函数和变量
        if (currentChar().isLetter() || currentChar() == '_') {
            return parseFunctionOrVariable()
        }
        
        throw IllegalArgumentException("无效字符: ${currentChar()} at position $pos")
    }
    
    // 解析数字
    private fun parseNumber(): Double {
        val start = pos
        
        // 整数部分
        while (pos < expression.length && currentChar().isDigit()) {
            advance()
        }
        
        // 小数部分
        if (pos < expression.length && currentChar() == '.') {
            advance()
            while (pos < expression.length && currentChar().isDigit()) {
                advance()
            }
        }
        
        // 科学计数法
        if (pos < expression.length && (currentChar() == 'e' || currentChar() == 'E')) {
            advance()
            if (pos < expression.length && (currentChar() == '+' || currentChar() == '-')) {
                advance()
            }
            while (pos < expression.length && currentChar().isDigit()) {
                advance()
            }
        }
        
        return expression.substring(start, pos).toDouble()
    }
    
    // 解析函数或变量
    private fun parseFunctionOrVariable(): Double {
        val start = pos
        while (pos < expression.length && (currentChar().isLetterOrDigit() || currentChar() == '_')) {
            advance()
        }
        val name = expression.substring(start, pos)
        
        // 检查是否是函数（后面跟括号）
        if (currentChar() == '(') {
            return callFunction(name)
        }
        
        // 检查常量
        return when (name.lowercase()) {
            "pi" -> PI
            "e" -> E
            else -> {
                // 检查变量
                variables[name] ?: throw IllegalArgumentException("未知变量: $name")
            }
        }
    }
    
    // 调用函数
    private fun callFunction(name: String): Double {
        advance() // 跳过 '('
        
        val args = mutableListOf<Double>()
        
        // 解析参数
        if (currentChar() != ')') {
            args.add(parseExpression())
            while (currentChar() == ',') {
                advance()
                args.add(parseExpression())
            }
        }
        
        if (currentChar() != ')') {
            throw IllegalArgumentException("函数调用缺少右括号: $name")
        }
        advance()
        
        return evaluateFunction(name, args)
    }
    
    // 计算函数值
    private fun evaluateFunction(name: String, args: List<Double>): Double {
        return when (name.lowercase()) {
            // 三角函数
            "sin" -> {
                requireArgs(name, args, 1)
                sin(args[0])
            }
            "cos" -> {
                requireArgs(name, args, 1)
                cos(args[0])
            }
            "tan" -> {
                requireArgs(name, args, 1)
                tan(args[0])
            }
            "asin" -> {
                requireArgs(name, args, 1)
                asin(args[0])
            }
            "acos" -> {
                requireArgs(name, args, 1)
                acos(args[0])
            }
            "atan" -> {
                requireArgs(name, args, 1)
                atan(args[0])
            }
            "sinh" -> {
                requireArgs(name, args, 1)
                sinh(args[0])
            }
            "cosh" -> {
                requireArgs(name, args, 1)
                cosh(args[0])
            }
            "tanh" -> {
                requireArgs(name, args, 1)
                tanh(args[0])
            }
            
            // 数学函数
            "sqrt" -> {
                requireArgs(name, args, 1)
                if (args[0] < 0) throw IllegalArgumentException("sqrt 参数不能为负数")
                sqrt(args[0])
            }
            "abs" -> {
                requireArgs(name, args, 1)
                abs(args[0])
            }
            "log", "log10" -> {
                requireArgs(name, args, 1)
                log10(args[0])
            }
            "ln", "log2" -> {
                requireArgs(name, args, 1)
                log(args[0], 2.0)
            }
            "exp" -> {
                requireArgs(name, args, 1)
                exp(args[0])
            }
            "floor" -> {
                requireArgs(name, args, 1)
                floor(args[0])
            }
            "ceil" -> {
                requireArgs(name, args, 1)
                ceil(args[0])
            }
            "round" -> {
                requireArgs(name, args, 1)
                round(args[0])
            }
            "sign" -> {
                requireArgs(name, args, 1)
                sign(args[0])
            }
            
            // 幂函数
            "pow" -> {
                requireArgs(name, args, 2)
                args[0].pow(args[1])
            }
            
            // 最大最小值
            "max" -> {
                if (args.isEmpty()) throw IllegalArgumentException("$name 需要至少一个参数")
                args.maxOrNull()!!
            }
            "min" -> {
                if (args.isEmpty()) throw IllegalArgumentException("$name 需要至少一个参数")
                args.minOrNull()!!
            }
            
            // 平均值
            "avg", "mean" -> {
                if (args.isEmpty()) throw IllegalArgumentException("$name 需要至少一个参数")
                args.average()
            }
            
            // 求和
            "sum" -> {
                if (args.isEmpty()) throw IllegalArgumentException("$name 需要至少一个参数")
                args.sum()
            }
            
            // 弧度角度转换
            "deg" -> {
                requireArgs(name, args, 1)
                Math.toDegrees(args[0])
            }
            "rad" -> {
                requireArgs(name, args, 1)
                Math.toRadians(args[0])
            }
            
            // 其他
            "random" -> {
                if (args.isEmpty()) random()
                else random(args[0].toLong())
            }
            
            else -> throw IllegalArgumentException("未知函数: $name")
        }
    }
    
    private fun requireArgs(name: String, args: List<Double>, expected: Int) {
        if (args.size != expected) {
            throw IllegalArgumentException("$name 需要 $expected 个参数，但收到 ${args.size} 个")
        }
    }
    
    private fun currentChar(): Char = if (pos < expression.length) expression[pos] else '\u0000'
    private fun advance() { pos++ }
    
    // 简单的随机数生成器（用于 random 函数的可重复性）
    private var seed = System.currentTimeMillis()
    private fun random(): Double {
        seed = (seed * 1103515245 + 12345) and 0x7FFFFFFF
        return seed.toDouble() / 0x7FFFFFFF
    }
    private fun random(seed: Long): Double {
        this.seed = seed
        return random()
    }
}

/**
 * 表达式验证器
 */
object ExpressionValidator {
    
    /**
     * 验证表达式是否有效
     */
    fun isValid(expr: String): Boolean {
        return try {
            MathExpressionEvaluator().evaluate(expr)
            true
        } catch (e: Exception) {
            false
        }
    }
    
    /**
     * 获取表达式中的变量名列表
     */
    fun extractVariables(expr: String): Set<String> {
        val vars = mutableSetOf<String>()
        val cleaned = expr.replace("\\s+".toRegex(), "")
        val regex = "[a-zA-Z_][a-zA-Z0-9_]*".toRegex()
        
        regex.findAll(cleaned).forEach { match ->
            val name = match.value
            // 排除函数名和常量
            if (name.lowercase() !in setOf(
                "sin", "cos", "tan", "asin", "acos", "atan",
                "sinh", "cosh", "tanh", "sqrt", "abs", "log",
                "log10", "ln", "log2", "exp", "floor", "ceil",
                "round", "sign", "pow", "max", "min", "avg",
                "mean", "sum", "deg", "rad", "random", "pi", "e"
            )) {
                // 检查后面是否跟括号（函数调用）
                val endIndex = match.range.last + 1
                if (endIndex >= cleaned.length || cleaned[endIndex] != '(') {
                    vars.add(name)
                }
            }
        }
        
        return vars
    }
    
    /**
     * 检查括号是否匹配
     */
    fun hasBalancedParentheses(expr: String): Boolean {
        var count = 0
        for (c in expr) {
            when (c) {
                '(' -> count++
                ')' -> {
                    count--
                    if (count < 0) return false
                }
            }
        }
        return count == 0
    }
}

/**
 * 表达式简化器
 */
object ExpressionSimplifier {
    
    /**
     * 简化表达式（移除多余空格、规范化）
     */
    fun simplify(expr: String): String {
        return expr.replace("\\s+".toRegex(), "")
            .replace("\\+\\+".toRegex(), "+")
            .replace("--".toRegex(), "+")
            .replace("\\+-".toRegex(), "-")
            .replace("-\\+".toRegex(), "-")
    }
}

/**
 * 扩展函数 - 方便使用
 */
fun String.evalMath(vars: Map<String, Double> = emptyMap()): Double {
    return MathExpressionEvaluator().evaluate(this, vars)
}

fun String.evalMath(vararg pairs: Pair<String, Number>): Double {
    val vars = pairs.associate { it.first to it.second.toDouble() }
    return MathExpressionEvaluator().evaluate(this, vars)
}