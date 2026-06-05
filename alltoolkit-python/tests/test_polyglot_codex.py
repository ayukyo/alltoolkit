"""
Polyglot Codex 测试套件
"""

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_codex import (
    rotate_and_get_codex,
    get_codex_preview,
    format_codex_markdown,
    format_codex_console,
    CODEX,
    DEFAULT_LANGUAGE_ROTATION_JSON,
)


# ── 测试数据 ─────────────────────────────────────────────────────────────────
EXPECTED_LANGUAGE_ORDER = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# current_index=3 → 当前语言 Kotlin
_INITIAL_YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
INITIAL_TEST_DATA = {
    "languages": [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ],
    "current_index": 3,
    "last_language": "Swift",
    "updated_at": f"{_INITIAL_YESTERDAY}T02:10:00+08:00",
}


def _make_temp_json():
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_codex_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 测试：CODEX 数据库完整性
# ─────────────────────────────────────────────────────────────────────────────
class TestCodexDatabase(unittest.TestCase):
    """确保每种语言都有完整的数据项"""

    def test_all_8_languages_have_codex(self):
        """CODEX 必须收录全部 8 种轮换语言"""
        for lang in EXPECTED_LANGUAGE_ORDER:
            self.assertIn(lang, CODEX, f"{lang} 缺少 CODEX 条目")

    def test_each_codex_has_required_fields(self):
        """每个 CODEX 条目必须包含所有必需字段"""
        required_fields = [
            "personality", "tagline", "superpowers", "blindspots",
            "famous_projects", "ecosystem", "quick_tip",
            "real_world_snippet", "trivia", "color",
        ]
        for lang in EXPECTED_LANGUAGE_ORDER:
            entry = CODEX[lang]
            for field in required_fields:
                self.assertIn(field, entry, f"{lang} 缺少字段: {field}")

    def test_each_codex_superpowers_is_list(self):
        for lang in EXPECTED_LANGUAGE_ORDER:
            self.assertIsInstance(CODEX[lang]["superpowers"], list)
            self.assertGreater(len(CODEX[lang]["superpowers"]), 0)

    def test_each_codex_famous_projects_format(self):
        for lang in EXPECTED_LANGUAGE_ORDER:
            projects = CODEX[lang]["famous_projects"]
            self.assertIsInstance(projects, list)
            for p in projects:
                self.assertIsInstance(p, tuple)
                self.assertEqual(len(p), 2)

    def test_each_codex_snippet_has_title_and_code(self):
        for lang in EXPECTED_LANGUAGE_ORDER:
            snippet = CODEX[lang]["real_world_snippet"]
            self.assertIn("title", snippet)
            self.assertIn("code", snippet)

    def test_each_codex_trivia_is_list(self):
        for lang in EXPECTED_LANGUAGE_ORDER:
            trivia = CODEX[lang]["trivia"]
            self.assertIsInstance(trivia, list)
            self.assertGreater(len(trivia), 0)


# ─────────────────────────────────────────────────────────────────────────────
# 测试：rotate_and_get_codex
# ─────────────────────────────────────────────────────────────────────────────
class TestRotateAndGetCodex(unittest.TestCase):
    """核心 API：轮换并获取 Codex"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_returns_current_language_kotlin(self):
        """index=3 → 当前语言 Kotlin"""
        result = rotate_and_get_codex(json_path=self.test_path)
        self.assertEqual(result["language"], "Kotlin")

    def test_returns_all_required_fields(self):
        result = rotate_and_get_codex(json_path=self.test_path)
        self.assertIn("language", result)
        self.assertIn("color", result)
        self.assertIn("personality", result)
        self.assertIn("tagline", result)
        self.assertIn("superpowers", result)
        self.assertIn("blindspots", result)
        self.assertIn("famous_projects", result)
        self.assertIn("ecosystem", result)
        self.assertIn("quick_tip", result)
        self.assertIn("real_world_snippet", result)
        self.assertIn("trivia", result)
        self.assertIn("index", result)
        self.assertIn("total", result)
        self.assertIn("next_language", result)

    def test_index_is_3(self):
        result = rotate_and_get_codex(json_path=self.test_path)
        self.assertEqual(result["index"], 3)

    def test_total_is_8(self):
        result = rotate_and_get_codex(json_path=self.test_path)
        self.assertEqual(result["total"], 8)

    def test_next_language_is_typescript(self):
        """Kotlin 之后 → TypeScript"""
        result = rotate_and_get_codex(json_path=self.test_path)
        self.assertEqual(result["next_language"], "TypeScript")

    def test_updates_current_index_to_4(self):
        """轮换后 index 应前进到 4"""
        rotate_and_get_codex(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 4)

    def test_updates_last_language_to_kotlin(self):
        """轮换后 last_language 应更新"""
        rotate_and_get_codex(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["last_language"], "Kotlin")

    def test_updates_updated_at(self):
        """轮换后 updated_at 应更新为非空字符串（Python 3.6兼容）"""
        rotate_and_get_codex(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertTrue(bool(data["updated_at"]))
        # 验证格式为 ISO 字符串
        self.assertIn("T", data["updated_at"])
        self.assertIn("+08:00", data["updated_at"])

    def test_full_rotation_cycle_wraps(self):
        """完整轮换循环：8次调用后回到 Rust"""
        # 设置为 Rust (index=0)
        test_data = {
            "languages": EXPECTED_LANGUAGE_ORDER,
            "current_index": 0,
            "last_language": "C/C++",
            "updated_at": f"{_INITIAL_YESTERDAY}T02:10:00+08:00",
        }
        fd, path = tempfile.mkstemp(suffix=".json", prefix="test_cycle_")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

        try:
            # 完整走一圈
            for i, expected_lang in enumerate(EXPECTED_LANGUAGE_ORDER):
                result = rotate_and_get_codex(json_path=path)
                self.assertEqual(
                    result["language"], expected_lang,
                    f"Cycle step {i}: expected {expected_lang}, got {result['language']}"
                )
        finally:
            os.remove(path)

    def test_unknown_language_raises(self):
        """用非 CODEX 语言会崩溃（但测试 JSON 不应出现这种情况）"""
        # 创建一个使用未知语言的 JSON
        test_data = {
            "languages": ["Rust", "Forth", "Swift"],
            "current_index": 1,
            "last_language": "Rust",
            "updated_at": f"{_INITIAL_YESTERDAY}T02:10:00+08:00",
        }
        fd, path = tempfile.mkstemp(suffix=".json", prefix="test_unknown_")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        try:
            with self.assertRaises(ValueError):
                rotate_and_get_codex(json_path=path)
        finally:
            os.remove(path)


# ─────────────────────────────────────────────────────────────────────────────
# 测试：get_codex_preview（不推进索引）
# ─────────────────────────────────────────────────────────────────────────────
class TestGetCodexPreview(unittest.TestCase):
    """预览 API 不应改变 current_index"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_preview_returns_kotlin(self):
        result = get_codex_preview(json_path=self.test_path)
        self.assertEqual(result["language"], "Kotlin")

    def test_preview_does_not_change_index(self):
        get_codex_preview(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 预览不应改变索引（仍然是 3）
        self.assertEqual(data["current_index"], 3)

    def test_preview_returns_next_language(self):
        result = get_codex_preview(json_path=self.test_path)
        self.assertEqual(result["next_language"], "TypeScript")


# ─────────────────────────────────────────────────────────────────────────────
# 测试：format_codex_markdown
# ─────────────────────────────────────────────────────────────────────────────
class TestFormatCodexMarkdown(unittest.TestCase):
    def test_format_contains_language(self):
        codex = rotate_and_get_codex()
        md = format_codex_markdown(codex)
        self.assertIn(codex["language"], md)

    def test_format_contains_personality(self):
        codex = rotate_and_get_codex()
        md = format_codex_markdown(codex)
        self.assertIn(codex["personality"], md)

    def test_format_contains_tagline(self):
        codex = rotate_and_get_codex()
        md = format_codex_markdown(codex)
        self.assertIn(codex["tagline"], md)

    def test_format_contains_superpowers(self):
        codex = rotate_and_get_codex()
        md = format_codex_markdown(codex)
        for sp in codex["superpowers"]:
            self.assertIn(sp, md)

    def test_format_contains_snippet_title(self):
        codex = rotate_and_get_codex()
        md = format_codex_markdown(codex)
        self.assertIn(codex["real_world_snippet"]["title"], md)

    def test_format_contains_next_language(self):
        codex = rotate_and_get_codex()
        md = format_codex_markdown(codex)
        self.assertIn(codex["next_language"], md)

    def test_format_is_markdown(self):
        codex = rotate_and_get_codex()
        md = format_codex_markdown(codex)
        self.assertTrue(md.startswith("## "))


# ─────────────────────────────────────────────────────────────────────────────
# 测试：format_codex_console
# ─────────────────────────────────────────────────────────────────────────────
class TestFormatCodexConsole(unittest.TestCase):
    def test_console_format_contains_language(self):
        codex = rotate_and_get_codex()
        out = format_codex_console(codex)
        self.assertIn(codex["language"], out)

    def test_console_format_contains_superpowers(self):
        codex = rotate_and_get_codex()
        out = format_codex_console(codex)
        self.assertIn("SUPERPOWERS", out)

    def test_console_format_contains_trivia(self):
        codex = rotate_and_get_codex()
        out = format_codex_console(codex)
        self.assertIn("TRIVIA", out)

    def test_console_format_uses_box_drawing_chars(self):
        codex = rotate_and_get_codex()
        out = format_codex_console(codex)
        self.assertIn("╔", out)
        self.assertIn("║", out)
        self.assertIn("╚", out)


# ─────────────────────────────────────────────────────────────────────────────
# 测试：默认 JSON 路径
# ─────────────────────────────────────────────────────────────────────────────
class TestDefaultPath(unittest.TestCase):
    def test_default_rotation_json_exists(self):
        """验证 DEFAULT_LANGUAGE_ROTATION_JSON 指向真实文件"""
        self.assertTrue(
            os.path.exists(DEFAULT_LANGUAGE_ROTATION_JSON),
            f"默认 JSON 不存在: {DEFAULT_LANGUAGE_ROTATION_JSON}"
        )

    def test_default_json_has_valid_structure(self):
        with open(DEFAULT_LANGUAGE_ROTATION_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("languages", data)
        self.assertIn("current_index", data)
        self.assertEqual(len(data["languages"]), 8)


if __name__ == "__main__":
    unittest.main()