"""
AllToolkit Polyglot Quiz 测试套件
"""

import unittest
import json
import os
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_quiz import (
    generate_quiz,
    check_answer,
    get_quiz_stats,
    record_attempt,
    rotate_and_get_quiz,
    format_quiz_console,
    format_quiz_markdown,
    format_stats_console,
    QUIZ_DB,
    LANGUAGE_METADATA,
    CORE_LANGUAGES,
)


EXPECTED_LANGUAGE_ORDER = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# 初始测试数据：current_index=2 → 当前语言 Swift
_INITIAL_YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
INITIAL_TEST_DATA = {
    "languages": [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ],
    "current_index": 2,
    "last_language": "Rust",
    "updated_at": f"{_INITIAL_YESTERDAY}T02:10:00+08:00",
}


def _make_temp_json():
    """每个测试用例使用独立的临时文件，避免状态污染"""
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_quiz_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)
    return path


def _make_temp_history():
    """Quiz 历史临时文件"""
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_quiz_hist_")
    os.close(fd)
    return path


class TestQuizUnit(unittest.TestCase):
    """Quiz 模块单元测试"""

    def test_quiz_db_has_all_languages(self):
        """题库应包含所有 8 种核心语言"""
        for lang in EXPECTED_LANGUAGE_ORDER:
            self.assertIn(lang, QUIZ_DB, f"{lang} 不在题库中")

    def test_quiz_db_has_enough_questions(self):
        """每种语言至少应有 3 道题"""
        for lang, questions in QUIZ_DB.items():
            self.assertGreaterEqual(
                len(questions), 3,
                f"{lang} 只有 {len(questions)} 道题，需要至少 3 道"
            )

    def test_all_questions_have_required_fields(self):
        """每道题应包含 code, hint, distractors"""
        required = {"code", "hint", "distractors"}
        for lang, questions in QUIZ_DB.items():
            for q in questions:
                self.assertTrue(
                    required.issubset(q.keys()),
                    f"{lang} 的题目缺少必要字段: {q}"
                )

    def test_generate_quiz_returns_required_fields(self):
        """generate_quiz 返回应包含所有必要字段"""
        quiz = generate_quiz(language="Rust")
        required = {
            "question_id", "language", "emoji", "code",
            "hint", "options", "correct_answer", "explanation", "topic",
        }
        self.assertTrue(
            required.issubset(quiz.keys()),
            f"generate_quiz 返回缺少字段: {required - quiz.keys()}"
        )

    def test_generate_quiz_correct_language(self):
        """generate_quiz 指定语言时应返回该语言的题"""
        quiz = generate_quiz(language="Swift")
        self.assertEqual(quiz["language"], "Swift")

    def test_generate_quiz_unknown_language_raises(self):
        """未知语言应抛出 ValueError"""
        with self.assertRaises(ValueError):
            generate_quiz(language="Forth")

    def test_generate_quiz_options_count(self):
        """generate_quiz 应返回 4 个选项"""
        quiz = generate_quiz(language="Go")
        self.assertEqual(len(quiz["options"]), 4)

    def test_generate_quiz_options_contains_correct(self):
        """4 个选项中应包含正确答案"""
        quiz = generate_quiz(language="Kotlin")
        values = [opt["value"] for opt in quiz["options"]]
        self.assertIn("Kotlin", values)

    def test_generate_quiz_options_all_distinct(self):
        """4 个选项应互不相同"""
        quiz = generate_quiz(language="JavaScript")
        values = [opt["value"] for opt in quiz["options"]]
        self.assertEqual(len(values), len(set(values)), "选项存在重复")

    def test_generate_quiz_correct_answer_in_options(self):
        """correct_answer 字段值应出现在 options 中"""
        for lang in EXPECTED_LANGUAGE_ORDER:
            quiz = generate_quiz(language=lang)
            values = [opt["value"] for opt in quiz["options"]]
            self.assertIn(
                quiz["correct_answer"], values,
                f"{lang}: correct_answer 不在 options 中"
            )

    def test_check_answer_correct(self):
        """正确答案应返回 correct=True"""
        result = check_answer("q_rust_1", "Rust", "Rust")
        self.assertTrue(result["correct"])

    def test_check_answer_incorrect(self):
        """错误答案应返回 correct=False"""
        result = check_answer("q_rust_1", "Go", "Rust")
        self.assertFalse(result["correct"])

    def test_check_answer_case_insensitive(self):
        """答案应大小写不敏感"""
        result = check_answer("q_rust_1", "rust", "Rust")
        self.assertTrue(result["correct"])

    def test_record_and_get_stats(self):
        """记录答题后统计应反映正确数据"""
        hist_path = _make_temp_history()
        try:
            record_attempt("q_rust_1", "Rust", "Rust", True, history_path=hist_path)
            record_attempt("q_go_1", "Go", "Go", True, history_path=hist_path)
            record_attempt("q_swift_1", "Swift", "Go", False, history_path=hist_path)

            stats = get_quiz_stats(history_path=hist_path)
            self.assertEqual(stats["total_attempts"], 3)
            self.assertEqual(stats["correct_count"], 2)
            self.assertEqual(stats["accuracy"], round(2 / 3 * 100, 1))
            self.assertIn("Rust", stats["by_language"])
            self.assertIn("Go", stats["by_language"])
            self.assertIn("Swift", stats["by_language"])
            self.assertEqual(stats["by_language"]["Rust"]["correct"], 1)
            self.assertEqual(stats["by_language"]["Swift"]["correct"], 0)
        finally:
            if os.path.exists(hist_path):
                os.remove(hist_path)

    def test_get_stats_empty_history(self):
        """空历史应返回零值统计"""
        hist_path = _make_temp_history()
        try:
            stats = get_quiz_stats(history_path=hist_path)
            self.assertEqual(stats["total_attempts"], 0)
            self.assertEqual(stats["accuracy"], 0.0)
        finally:
            if os.path.exists(hist_path):
                os.remove(hist_path)

    def test_format_quiz_console_contains_code(self):
        """控制台格式输出应包含代码片段"""
        quiz = generate_quiz(language="Rust")
        output = format_quiz_console(quiz)
        self.assertIn("Rust", output)
        self.assertIn("╔", output)

    def test_format_quiz_markdown_contains_code(self):
        """Markdown 格式输出应包含代码片段"""
        quiz = generate_quiz(language="Go")
        output = format_quiz_markdown(quiz)
        self.assertIn("Go", output)
        self.assertIn("```", output)

    def test_format_stats_console_contains_headers(self):
        """统计控制台输出应包含头部"""
        hist_path = _make_temp_history()
        try:
            stats = get_quiz_stats(history_path=hist_path)
            output = format_stats_console(stats)
            self.assertIn("📊", output)
            self.assertIn("总答题次数", output)
        finally:
            if os.path.exists(hist_path):
                os.remove(hist_path)


class TestQuizIntegration(unittest.TestCase):
    """Quiz 模块集成测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_rotate_and_get_quiz_changes_language(self):
        """rotate_and_get_quiz 应推进轮换索引并生成对应语言的题"""
        # 初始 index=2 → Swift
        quiz = rotate_and_get_quiz(json_path=self.test_path)
        self.assertIn(quiz["language"], EXPECTED_LANGUAGE_ORDER)
        # JSON 的 current_index 应前移一位
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 3)  # 从 2 → 3

    def test_rotate_and_get_quiz_full_cycle(self):
        """完整轮换一圈（8 次），所有语言各生成一道题"""
        seen = set()
        for _ in range(8):
            quiz = rotate_and_get_quiz()
            self.assertIn(quiz["language"], EXPECTED_LANGUAGE_ORDER)
            seen.add(quiz["language"])
        self.assertEqual(len(seen), 8)

    def test_full_quiz_workflow(self):
        """完整流程：轮换 → 生成题 → 答题 → 记录 → 统计"""
        hist_path = _make_temp_history()
        try:
            quiz = rotate_and_get_quiz()
            language = quiz["language"]
            correct = quiz["correct_answer"]

            # 答对
            result = check_answer(quiz["question_id"], correct, language)
            self.assertTrue(result["correct"])

            record_attempt(
                quiz["question_id"], language, correct, result["correct"],
                history_path=hist_path
            )

            # 答错
            wrong = "Go" if correct != "Go" else "Rust"
            result2 = check_answer(quiz["question_id"], wrong, language)
            self.assertFalse(result2["correct"])

            record_attempt(
                quiz["question_id"], language, wrong, result2["correct"],
                history_path=hist_path
            )

            stats = get_quiz_stats(history_path=hist_path)
            self.assertEqual(stats["total_attempts"], 2)
            self.assertEqual(stats["correct_count"], 1)
            self.assertEqual(stats["accuracy"], 50.0)
        finally:
            if os.path.exists(hist_path):
                os.remove(hist_path)

    def test_quiz_with_different_languages(self):
        """为每种语言生成题，所有语言都成功"""
        for lang in EXPECTED_LANGUAGE_ORDER:
            quiz = generate_quiz(language=lang)
            self.assertEqual(quiz["language"], lang)
            self.assertEqual(len(quiz["options"]), 4)

    def test_language_metadata_consistency(self):
        """LANGUAGE_METADATA 应与 language_tools.py 定义的元数据一致"""
        required_meta_keys = {"emoji", "tagline", "hello_world", "file_ext", "year", "paradigm"}
        for lang in EXPECTED_LANGUAGE_ORDER:
            self.assertIn(lang, LANGUAGE_METADATA)
            self.assertTrue(
                required_meta_keys.issubset(LANGUAGE_METADATA[lang].keys()),
                f"{lang} 元数据缺少字段"
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)