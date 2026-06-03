"""
AllToolkit 测试套件 - dev_metrics 模块
"""

import unittest
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.dev_metrics import (
    measure_cyclomatic_complexity,
    measure_cognitive_complexity,
    analyze_structure,
    calculate_quality_score,
    suggest_improvements,
    analyze_code,
    analyze_file,
    analyze_directory,
    _remove_strings_and_comments,
    _detect_language,
    _detect_language_by_extension,
    _generate_summary,
)


class TestCyclomaticComplexity(unittest.TestCase):
    """圈复杂度测试"""

    def test_simple_linear_code(self):
        """线性代码复杂度为1"""
        code = "x = 1\ny = 2\nz = x + y"
        result = measure_cyclomatic_complexity(code)
        self.assertEqual(result, 1)

    def test_if_branch(self):
        """if 分支 +1"""
        code = "if x > 0:\n    y = 1"
        result = measure_cyclomatic_complexity(code)
        self.assertEqual(result, 2)

    def test_for_loop(self):
        """for 循环 +1"""
        code = "for i in range(10):\n    print(i)"
        result = measure_cyclomatic_complexity(code)
        self.assertEqual(result, 2)

    def test_if_elif_else(self):
        """if/elif/else 链 +3"""
        code = "if x > 0:\n    a\nelif x == 0:\n    b\nelse:\n    c"
        result = measure_cyclomatic_complexity(code)
        self.assertEqual(result, 3)  # base(1) + if + elif + else

    def test_and_or_condition(self):
        """and/or 条件 +1 each"""
        code = "if a and b:\n    x = 1"
        result = measure_cyclomatic_complexity(code)
        self.assertEqual(result, 3)  # 1 base + 1 if + 1 and

    def test_try_except(self):
        """try/except +1"""
        code = "try:\n    x = 1\nexcept:\n    x = 0"
        result = measure_cyclomatic_complexity(code)
        self.assertEqual(result, 2)

    def test_nested_loops(self):
        """嵌套循环"""
        code = "for i in range(10):\n    for j in range(10):\n        if i == j:\n            print(i)"
        result = measure_cyclomatic_complexity(code)
        self.assertGreater(result, 3)

    def test_string_not_counted(self):
        """字符串内容中的关键字不应计入"""
        code = 'msg = "if (x > 0) and (y < 10)"\nif True:\n    pass'
        result = measure_cyclomatic_complexity(code)
        self.assertEqual(result, 2)  # base + if，不含字符串中的


class TestCognitiveComplexity(unittest.TestCase):
    """认知复杂度测试"""

    def test_simple_code_low(self):
        """简单代码认知复杂度低"""
        code = "x = 1\ny = 2"
        result = measure_cognitive_complexity(code)
        self.assertGreaterEqual(result, 1)

    def test_function_increases_score(self):
        """函数定义增加认知复杂度"""
        code = "def foo():\n    pass"
        result = measure_cognitive_complexity(code)
        self.assertGreaterEqual(result, 1)


class TestStructureAnalysis(unittest.TestCase):
    """结构分析测试"""

    def test_detect_python(self):
        """检测 Python"""
        code = "def hello():\n    pass"
        structure = analyze_structure(code)
        self.assertEqual(structure["language"], "Python")

    def test_detect_rust(self):
        """检测 Rust"""
        code = "fn main() {\n    println!(\"Hello\");\n}"
        structure = analyze_structure(code)
        self.assertEqual(structure["language"], "Rust")

    def test_detect_go(self):
        """检测 Go"""
        code = "func main() {\n    fmt.Println(\"Hello\")\n}"
        structure = analyze_structure(code)
        self.assertEqual(structure["language"], "Go")

    def test_python_functions(self):
        """Python 函数提取"""
        code = """
def foo(a, b):
    return a + b

def bar(x):
    return x * 2
"""
        structure = analyze_structure(code)
        self.assertEqual(structure["function_count"], 2)
        func_names = [f["name"] for f in structure["functions"]]
        self.assertIn("foo", func_names)
        self.assertIn("bar", func_names)

    def test_python_classes(self):
        """Python 类提取"""
        code = """
class Foo:
    def method(self):
        pass

class Bar(Base):
    pass
"""
        structure = analyze_structure(code)
        self.assertEqual(structure["class_count"], 2)

    def test_python_imports(self):
        """Python import 提取"""
        code = """
import os
import sys
from pathlib import Path
"""
        structure = analyze_structure(code)
        self.assertEqual(structure["import_count"], 3)

    def test_comments_extraction(self):
        """注释提取"""
        code = "# This is a comment\nx = 1  # inline\n/* block */"
        structure = analyze_structure(code)
        self.assertGreaterEqual(structure["comment_count"], 2)


class TestLanguageDetection(unittest.TestCase):
    """语言检测测试"""

    def test_detect_python_keyword(self):
        self.assertEqual(_detect_language("def foo():\n    pass"), "Python")

    def test_detect_rust_keyword(self):
        self.assertEqual(_detect_language("fn main() {\n}"), "Rust")

    def test_detect_go_keyword(self):
        self.assertEqual(_detect_language("func main() {\n}"), "Go")

    def test_detect_swift_keyword(self):
        self.assertEqual(_detect_language("func foo() -> Int {\n}"), "Swift")

    def test_detect_kotlin_keyword(self):
        self.assertEqual(_detect_language("fun foo() {\n}"), "Kotlin")

    def test_detect_java_keyword(self):
        self.assertEqual(_detect_language("class Foo {\n}"), "Java")

    def test_detect_typescript(self):
        self.assertEqual(_detect_language("const f = (x: number): void => {}"), "TypeScript")

    def test_detect_c(self):
        self.assertEqual(_detect_language("#include <stdio.h>"), "C/C++")

    def test_extension_python(self):
        self.assertEqual(_detect_language_by_extension("foo.py"), "Python")

    def test_extension_rust(self):
        self.assertEqual(_detect_language_by_extension("main.rs"), "Rust")

    def test_extension_go(self):
        self.assertEqual(_detect_language_by_extension("main.go"), "Go")

    def test_extension_swift(self):
        self.assertEqual(_detect_language_by_extension("foo.swift"), "Swift")

    def test_extension_kotlin(self):
        self.assertEqual(_detect_language_by_extension("Main.kt"), "Kotlin")

    def test_extension_java(self):
        self.assertEqual(_detect_language_by_extension("Main.java"), "Java")

    def test_extension_typescript(self):
        self.assertEqual(_detect_language_by_extension("app.ts"), "TypeScript")

    def test_extension_javascript(self):
        self.assertEqual(_detect_language_by_extension("app.js"), "JavaScript")

    def test_extension_cpp(self):
        self.assertEqual(_detect_language_by_extension("main.cpp"), "C++")

    def test_extension_c(self):
        self.assertEqual(_detect_language_by_extension("main.c"), "C")


class TestQualityScore(unittest.TestCase):
    """质量评分测试"""

    def test_simple_code_high_score(self):
        """简单代码得高分"""
        code = "#!/usr/bin/env python3\nx = 1\ny = 2\nprint(x + y)"
        structure = analyze_structure(code)
        quality = calculate_quality_score(code, structure)
        self.assertGreaterEqual(quality["overall"], 0)
        self.assertLessEqual(quality["overall"], 100)

    def test_quality_scores_in_range(self):
        """各项评分在 0-100"""
        code = "x = 1"
        structure = analyze_structure(code)
        quality = calculate_quality_score(code, structure)
        
        for key in ["overall", "complexity_score", "struct_score", "comment_score", "inherit_score"]:
            self.assertGreaterEqual(quality[key], 0)
            self.assertLessEqual(quality[key], 100)

    def test_cyclomatic_complexity_included(self):
        """质量报告中包含圈复杂度"""
        code = "if True:\n    pass"
        structure = analyze_structure(code)
        quality = calculate_quality_score(code, structure)
        self.assertIn("cyclomatic_complexity", quality)
        self.assertGreater(quality["cyclomatic_complexity"], 1)

    def test_lines_of_code(self):
        """行数统计"""
        code = "line1\nline2\nline3\n"
        structure = analyze_structure(code)
        quality = calculate_quality_score(code, structure)
        self.assertEqual(quality["lines_of_code"], 4)


class TestSuggestions(unittest.TestCase):
    """改进建议测试"""

    def test_suggestions_return_list(self):
        """建议返回列表"""
        code = "x = 1"
        structure = analyze_structure(code)
        quality = calculate_quality_score(code, structure)
        suggestions = suggest_improvements(code, structure, quality)
        self.assertIsInstance(suggestions, list)

    def test_high_complexity_gets_suggestion(self):
        """高复杂度代码有建议"""
        code = "\n".join(["if x == 1:\n    pass"] * 30)
        structure = analyze_structure(code)
        quality = calculate_quality_score(code, structure)
        suggestions = suggest_improvements(code, structure, quality)
        self.assertTrue(any("复杂度" in s for s in suggestions))


class TestAnalyzeCode(unittest.TestCase):
    """完整分析测试"""

    def test_analyze_code_returns_all_fields(self):
        """分析结果包含所有字段"""
        code = "def foo():\n    pass"
        result = analyze_code(code)
        
        self.assertIn("language", result)
        self.assertIn("structure", result)
        self.assertIn("quality", result)
        self.assertIn("suggestions", result)
        self.assertIn("summary", result)

    def test_analyze_code_with_path(self):
        """带路径分析"""
        code = "x = 1"
        result = analyze_code(code, "foo.py")
        self.assertEqual(result["language"], "Python")

    def test_summary_format(self):
        """摘要格式正确"""
        code = "def foo():\n    pass"
        result = analyze_code(code)
        summary = result["summary"]
        
        self.assertIn("[Python]", summary)
        self.assertIn("行代码", summary)
        self.assertIn("质量评分", summary)


class TestAnalyzeFile(unittest.TestCase):
    """文件分析测试"""

    def test_analyze_current_file(self):
        """分析当前测试文件"""
        result = analyze_file(__file__)
        
        self.assertIn("language", result)
        self.assertIn("structure", result)
        self.assertEqual(result["language"], "Python")

    def test_nonexistent_file_raises(self):
        """不存在文件抛出异常"""
        with self.assertRaises(FileNotFoundError):
            analyze_file("/nonexistent/file/xyz.py")


class TestAnalyzeDirectory(unittest.TestCase):
    """目录分析测试"""

    def test_analyze_modules_directory(self):
        """分析 modules 目录"""
        modules_dir = Path(__file__).parent.parent / "modules"
        if not modules_dir.exists():
            self.skipTest("modules 目录不存在")
        
        results = analyze_directory(str(modules_dir), extensions=[".py"])
        
        self.assertIsInstance(results, list)
        for r in results:
            self.assertIn("file_path", r)
            self.assertIn("summary", r)
            self.assertIn("language", r)


class TestRemoveStringsAndComments(unittest.TestCase):
    """字符串/注释移除测试"""

    def test_removes_single_quoted_strings(self):
        code = 'x = "hello world"\ny = 1'
        result = _remove_strings_and_comments(code)
        self.assertNotIn("hello world", result)
        self.assertIn("y = 1", result)

    def test_removes_double_quoted_strings(self):
        code = 'x = "hello world"\ny = 1'
        result = _remove_strings_and_comments(code)
        self.assertNotIn("hello world", result)

    def test_removes_python_comments(self):
        code = "# comment\nx = 1\n# another"
        result = _remove_strings_and_comments(code)
        self.assertNotIn("comment", result)
        self.assertIn("x = 1", result)

    def test_removes_cpp_comments(self):
        code = "// comment\nx = 1"
        result = _remove_strings_and_comments(code)
        self.assertNotIn("comment", result)


class TestGenerateSummary(unittest.TestCase):
    """摘要生成测试"""

    def test_summary_contains_language(self):
        structure = {
            "function_count": 2,
            "class_count": 1,
            "max_inheritance_depth": 0,
        }
        quality = {
            "overall": 75.0,
            "lines_of_code": 50,
        }
        summary = _generate_summary("Python", structure, quality)
        self.assertIn("[Python]", summary)
        self.assertIn("50行代码", summary)


if __name__ == "__main__":
    unittest.main(verbosity=2)
