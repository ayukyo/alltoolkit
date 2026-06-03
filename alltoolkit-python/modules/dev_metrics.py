"""
代码指标分析模块 (Code Metrics Analyzer)
测量代码复杂度、质量和结构指标
"""

import re
import ast
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path


# ─────────────────────────────────────────────
# 复杂度分析
# ─────────────────────────────────────────────

def measure_cyclomatic_complexity(code: str) -> int:
    """
    测量圈复杂度（McCabe Complexity）
    
    基于控制流分支：if/elif/else, for, while, except, and, or, ?:
    
    Returns:
        复杂度数值（1 = 最低，线性代码）
    """
    # 移除字符串和注释中的关键字（避免误判）
    cleaned = _remove_strings_and_comments(code)
    
    complexity = 1  # 基础复杂度
    
    # 控制流关键词
    patterns = [
        r'\bif\b',           # if
        r'\belif\b',         # elif
        r'\bwhile\b',        # while
        r'\bfor\b',          # for
        r'\band\b',          # and
        r'\bor\b',           # or
        r'\bexcept\b',       # except
        r'\bcase\b',         # case (switch)
        r'\?\s*[^:]+:',     # 三元运算符
    ]
    
    for p in patterns:
        complexity += len(re.findall(p, cleaned))
    
    return max(1, complexity)


def measure_cognitive_complexity(code: str) -> int:
    """
    测量认知复杂度（SonarQube 风格）
    
    比圈复杂度更注重代码的"思维跳转成本"
    - 递增：嵌套结构、递归、交叉跳转
    - 嵌套越深，分数越高
    """
    cleaned = _remove_strings_and_comments(code)
    lines = cleaned.split('\n')
    
    score = 0
    nesting_level = 0
    
    # 递归结构关键词（增加复杂度）
    for line in lines:
        stripped = line.strip()
        
        # 嵌套结构
        if re.match(r'\b(if|elif|else|while|for|except)\b.*:', stripped):
            nesting_level += 1
            score += nesting_level
        elif re.match(r'\bdef\b', stripped):
            # 函数定义本身 +1，之后的嵌套继续累加
            nesting_level += 1
            score += nesting_level
        elif stripped and not stripped.startswith('#'):
            # 缩进减少 → 嵌套结束
            indent = len(line) - len(line.lstrip())
            # 简单估算嵌套层级变化
            if indent == 0 and nesting_level > 0:
                nesting_level = max(0, nesting_level - 1)
    
    return max(1, score)


# ─────────────────────────────────────────────
# 结构分析
# ─────────────────────────────────────────────

def analyze_structure(code: str) -> Dict:
    """
    分析代码结构（函数、类、方法、模块级变量等）
    
    Returns:
        包含各类结构统计的字典
    """
    language = _detect_language(code)
    
    functions = _extract_functions(code, language)
    classes = _extract_classes(code, language)
    imports = _extract_imports(code, language)
    comments = _extract_comments(code)
    
    # 计算继承深度
    inheritances = _extract_inheritance(classes)
    max_inheritance_depth = _compute_inheritance_depth(inheritances)
    
    return {
        "language": language,
        "functions": functions,
        "function_count": len(functions),
        "classes": classes,
        "class_count": len(classes),
        "imports": imports,
        "import_count": len(imports),
        "comments": comments,
        "comment_count": len(comments),
        "inheritance": inheritances,
        "max_inheritance_depth": max_inheritance_depth,
    }


def _extract_functions(code: str, language: str) -> List[Dict]:
    """提取函数列表"""
    functions = []
    
    if language == "Python":
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    args = [a.arg for a in node.args.args]
                    functions.append({
                        "name": node.name,
                        "args": args,
                        "arg_count": len(args),
                        "line": node.lineno,
                        "is_async": isinstance(node, ast.AsyncFunctionDef),
                    })
        except SyntaxError:
            pass
    
    elif language in ("Rust", "Go", "Swift", "Kotlin", "Java", "C", "C++", "TypeScript", "JavaScript"):
        # 函数声明模式（简化）
        patterns = {
            "Rust":   r'(?:pub\s+)?fn\s+(\w+)\s*\(',
            "Go":     r'func\s+(\w+)\s*\(',
            "Swift":  r'func\s+(\w+)\s*\(',
            "Kotlin": r'fun\s+(\w+)\s*\(',
            "Java":   r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\(',
            "C":      r'(?:\w+\s+)+(\w+)\s*\([^)]*\)\s*\{',
            "C++":    r'(?:\w+\s+)+(\w+)\s*\([^)]*\)\s*\{',
            "TypeScript": r'function\s+(\w+)\s*\(',
            "JavaScript": r'function\s+(\w+)\s*\(',
        }
        pattern = patterns.get(language, r'function\s+(\w+)\s*\(')
        for m in re.finditer(pattern, code):
            functions.append({
                "name": m.group(1),
                "line": code[:m.start()].count('\n') + 1,
            })
    
    return functions


def _extract_classes(code: str, language: str) -> List[Dict]:
    """提取类列表"""
    classes = []
    
    if language == "Python":
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    bases = [b.attr if isinstance(b, ast.Attribute) else 
                             (b.id if isinstance(b, ast.Name) else str(b))
                             for b in node.bases]
                    classes.append({
                        "name": node.name,
                        "bases": bases,
                        "line": node.lineno,
                        "method_count": sum(1 for n in node.body 
                                          if isinstance(n, ast.FunctionDef)),
                    })
        except SyntaxError:
            pass
    
    elif language in ("Rust", "Go", "Swift", "Kotlin", "Java", "C++", "TypeScript", "JavaScript"):
        patterns = {
            "Rust":       r'struct\s+(\w+)',
            "Go":         r'type\s+(\w+)\s+struct',
            "Swift":      r'class\s+(\w+)',
            "Kotlin":    r'class\s+(\w+)',
            "Java":       r'class\s+(\w+)',
            "C++":        r'class\s+(\w+)',
            "TypeScript": r'class\s+(\w+)',
            "JavaScript": r'class\s+(\w+)',
        }
        pattern = patterns.get(language, r'class\s+(\w+)')
        for m in re.finditer(pattern, code):
            classes.append({
                "name": m.group(1),
                "line": code[:m.start()].count('\n') + 1,
            })
    
    return classes


def _extract_imports(code: str, language: str) -> List[str]:
    """提取 import 语句"""
    imports = []
    
    if language == "Python":
        for m in re.finditer(r'^(?:from\s+[\w.]+\s+)?import\s+.+$', code, re.MULTILINE):
            imports.append(m.group().strip())
    elif language in ("Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript"):
        for m in re.finditer(r'^\s*(?:use|import|require)\s+[^;]+;?\s*$', code, re.MULTILINE):
            imports.append(m.group().strip())
    elif language in ("Java", "C", "C++"):
        for m in re.finditer(r'^\s*#\s*include\s*.+$', code, re.MULTILINE):
            imports.append(m.group().strip())
    
    return imports


def _extract_comments(code: str) -> List[str]:
    """提取所有注释"""
    comments = []
    
    # 单行注释
    for m in re.finditer(r'//.*$', code, re.MULTILINE):
        comments.append(m.group().strip())
    
    # 多行注释（先处理字符串避免干扰）
    for m in re.finditer(r'/\*[\s\S]*?\*/', code):
        comments.append(m.group().strip())
    
    # Python 注释
    for m in re.finditer(r'^#.*$', code, re.MULTILINE):
        comments.append(m.group().strip())
    
    return comments


def _extract_inheritance(classes: List[Dict]) -> Dict[str, List[str]]:
    """提取继承关系"""
    result = {}
    for cls in classes:
        if cls.get("bases"):
            result[cls["name"]] = cls["bases"]
    return result


def _compute_inheritance_depth(inheritances: Dict[str, List[str]]) -> int:
    """计算最大继承深度"""
    if not inheritances:
        return 0
    
    depths = {}
    
    def get_depth(cls: str) -> int:
        if cls in depths:
            return depths[cls]
        if cls not in inheritances or not inheritances[cls]:
            depths[cls] = 0
            return 0
        max_base = max((get_depth(b) for b in inheritances[cls]), default=0)
        depths[cls] = max_base + 1
        return depths[cls]
    
    return max((get_depth(c) for c in inheritances), default=0)


# ─────────────────────────────────────────────
# 代码质量评分
# ─────────────────────────────────────────────

def calculate_quality_score(code: str, structure: Dict) -> Dict:
    """
    综合代码质量评分（0-100）
    
    维度：
    - 复杂度得分（圈复杂度）
    - 结构得分（函数/类规模、继承深度）
    - 可读性得分（注释覆盖率）
    - 模块化得分（import 合理性）
    """
    complexity = measure_cyclomatic_complexity(code)
    lines = len(code.split('\n'))
    
    # 复杂度评分（越低越好）
    if complexity <= 5:
        complexity_score = 100
    elif complexity <= 10:
        complexity_score = 80
    elif complexity <= 20:
        complexity_score = 60
    elif complexity <= 50:
        complexity_score = 40
    else:
        complexity_score = 20
    
    # 结构评分（函数数量/行数比例合理则高）
    func_count = structure["function_count"]
    class_count = structure["class_count"]
    
    if lines == 0:
        struct_score = 0
    else:
        ratio = (func_count + class_count * 2) / lines
        if ratio > 0.05:
            struct_score = 70  # 可能过度分割
        elif ratio >= 0.01:
            struct_score = 90  # 合理
        else:
            struct_score = 60  # 可能缺乏结构
    
    # 注释覆盖率
    comment_ratio = structure["comment_count"] / max(lines, 1)
    if comment_ratio >= 0.15:
        comment_score = 100
    elif comment_ratio >= 0.10:
        comment_score = 80
    elif comment_ratio >= 0.05:
        comment_score = 60
    else:
        comment_score = 40
    
    # 继承深度评分
    inherit_depth = structure["max_inheritance_depth"]
    if inherit_depth <= 2:
        inherit_score = 100
    elif inherit_depth <= 4:
        inherit_score = 70
    else:
        inherit_score = 50
    
    # 综合评分（加权平均）
    overall = (
        complexity_score * 0.35 +
        struct_score * 0.20 +
        comment_score * 0.20 +
        inherit_score * 0.25
    )
    
    return {
        "overall": round(overall, 1),
        "complexity_score": complexity_score,
        "struct_score": round(struct_score, 1),
        "comment_score": comment_score,
        "inherit_score": inherit_score,
        "cyclomatic_complexity": complexity,
        "lines_of_code": lines,
    }


def suggest_improvements(code: str, structure: Dict, quality: Dict) -> List[str]:
    """
    基于分析结果给出改进建议
    """
    suggestions = []
    
    complexity = quality["cyclomatic_complexity"]
    if complexity > 20:
        suggestions.append(f"圈复杂度 {complexity} 过高，建议拆分为更小的函数（目标 < 10）")
    elif complexity > 10:
        suggestions.append(f"圈复杂度 {complexity} 偏高，考虑简化条件逻辑")
    
    if quality["struct_score"] < 70:
        suggestions.append("代码结构分散，建议增加内聚性或拆分文件")
    
    if quality["comment_score"] < 60:
        suggestions.append("注释不足，建议添加文档字符串和关键注释")
    
    if structure["max_inheritance_depth"] > 3:
        suggestions.append("继承层次过深（建议 ≤ 3），考虑使用组合替代继承")
    
    # 过长函数检测
    if structure["function_count"] > 0:
        code_lines = len(code.split('\n'))
        avg_func_length = code_lines / structure["function_count"]
        if avg_func_length > 50:
            suggestions.append(f"平均函数长度 {avg_func_length:.0f} 行偏长，建议每个函数 ≤ 50 行")
    
    if not suggestions:
        suggestions.append("代码质量良好，继续保持！")
    
    return suggestions


# ─────────────────────────────────────────────
# 综合分析入口
# ─────────────────────────────────────────────

def analyze_code(code: str, file_path: Optional[str] = None) -> Dict:
    """
    完整代码分析
    
    Args:
        code: 源代码文本
        file_path: 可选，文件路径（用于推断语言）
    
    Returns:
        完整的分析报告
    """
    language = _detect_language(code)
    if file_path:
        ext_lang = _detect_language_by_extension(file_path)
        if ext_lang:
            language = ext_lang
    
    structure = analyze_structure(code)
    quality = calculate_quality_score(code, structure)
    improvements = suggest_improvements(code, structure, quality)
    
    return {
        "language": language,
        "structure": structure,
        "quality": quality,
        "suggestions": improvements,
        "summary": _generate_summary(language, structure, quality),
    }


def analyze_file(file_path: str) -> Dict:
    """
    分析文件
    
    Args:
        file_path: 源代码文件路径
    
    Returns:
        完整分析报告
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    code = path.read_text(encoding="utf-8", errors="ignore")
    return analyze_code(code, str(path))


def analyze_directory(directory: str, extensions: Optional[List[str]] = None) -> List[Dict]:
    """
    分析目录下所有代码文件
    
    Args:
        directory: 目录路径
        extensions: 要分析的文件扩展名（如 [".py", ".rs"]）
    
    Returns:
        每个文件的分析报告列表
    """
    if extensions is None:
        extensions = [".py", ".rs", ".go", ".swift", ".kt", ".java",
                      ".ts", ".js", ".c", ".cpp", ".h", ".hpp"]
    
    dir_path = Path(directory)
    results = []
    
    for ext in extensions:
        for file_path in dir_path.rglob(f"*{ext}"):
            # 跳过 node_modules、__pycache__ 等
            if any(part.startswith('.') or part in ('node_modules', '__pycache__', 'target', 'dist')
                    for part in file_path.parts):
                continue
            try:
                result = analyze_file(str(file_path))
                result["file_path"] = str(file_path)
                results.append(result)
            except Exception:
                pass
    
    return results


# ─────────────────────────────────────────────
# 辅助函数
# ─────────────────────────────────────────────

def _remove_strings_and_comments(code: str) -> str:
    """移除字符串和注释，避免在统计复杂度时误判"""
    result = []
    i = 0
    n = len(code)
    
    while i < n:
        c = code[i]
        
        # 字符串
        if c in '"\'':
            quote = c
            if i + 2 < n and code[i+1] == quote and code[i+2] == quote:
                # 三引号字符串
                quote3 = code[i:i+3]
                end = code.find(quote3, i+3)
                i = end + 3 if end != -1 else n
            else:
                i += 1
                while i < n and code[i] != quote:
                    if code[i] == '\\' and i+1 < n:
                        i += 2
                    else:
                        i += 1
                i += 1
        # 单行注释
        elif c == '#' and i + 1 < n:
            end = code.find('\n', i)
            i = end if end != -1 else n
        elif c == '/' and i + 1 < n and code[i+1] == '/':
            end = code.find('\n', i)
            i = end if end != -1 else n
        elif c == '/' and i + 1 < n and code[i+1] == '*':
            end = code.find('*/', i+2)
            i = end + 2 if end != -1 else n
        else:
            result.append(c)
            i += 1
    
    return ''.join(result)


def _detect_language(code: str) -> str:
    """通过代码特征检测语言"""
    patterns = [
        (r'\bfn\s+\w+', "Rust"),
        (r'\bfunc\s+\w+\s*\([^)]*\)\s*->', "Swift"),
        (r'\bfunc\s+\w+\s*\(.*?\)\s*\{', "Go"),
        (r'\bfunc\s+\w+', "Go"),
        (r'\bfunc\s+\w+\s*\(', "Swift"),
        (r'\bfun\s+\w+', "Kotlin"),
        (r'\bclass\s+\w+', "Java"),
        (r'\bdef\s+\w+', "Python"),
        (r'\bfunction\s+\w+', "JavaScript"),
        (r':\s*\w+\s*=>', "TypeScript"),
        (r'#include\s*<', "C/C++"),
        (r'^\s*import\s+', "Python"),
    ]
    
    for pattern, lang in patterns:
        if re.search(pattern, code):
            return lang
    
    return "Unknown"


def _detect_language_by_extension(file_path: str) -> Optional[str]:
    """通过文件扩展名推断语言"""
    ext_map = {
        ".py": "Python",
        ".rs": "Rust",
        ".go": "Go",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".java": "Java",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".c": "C",
        ".cpp": "C++",
        ".cc": "C++",
        ".h": "C/C++",
        ".hpp": "C++",
    }
    
    ext = Path(file_path).suffix
    return ext_map.get(ext.lower())


def _generate_summary(language: str, structure: Dict, quality: Dict) -> str:
    """生成一句话总结"""
    score = quality["overall"]
    lines = quality["lines_of_code"]
    funcs = structure["function_count"]
    classes = structure["class_count"]
    
    if score >= 85:
        rating = "优秀"
    elif score >= 70:
        rating = "良好"
    elif score >= 50:
        rating = "一般"
    else:
        rating = "需改进"
    
    return (f"[{language}] {lines}行代码 | "
            f"{funcs}函数 {classes}类 | "
            f"质量评分{score:.0f}分（{rating}）")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("用法: python dev_metrics.py <file|directory>")
        sys.exit(1)
    
    target = sys.argv[1]
    path = Path(target)
    
    if path.is_file():
        result = analyze_file(target)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif path.is_dir():
        results = analyze_directory(target)
        for r in results:
            print(f"{r['file_path']}: {r['summary']}")
        print(f"\n共分析 {len(results)} 个文件")
    else:
        print(f"无效路径: {target}")
        sys.exit(1)
