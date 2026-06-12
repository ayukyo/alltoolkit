"""
Polyglot Snippet Vault 测试套件
"""

import unittest
import json
import os
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_snippet_vault import (
    get_snippet,
    search_snippets,
    get_vault_stats,
    get_supported_categories,
    format_snippet_console,
    format_snippet_markdown,
    SNIPPET_DB,
    CORE_LANGUAGES,
    CATEGORY_LABELS,
    Category,
)


# 初始测试数据：current_index=2 → 当前语言 Swift
_INITIAL_YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
INITIAL_TEST_DATA = {
    "languages": [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ],
    "current_index": 2,
    "last_language": "Go",
    "updated_at": f"{_INITIAL_YESTERDAY}T02:10:00+08:00",
}


def _make_temp_json():
    """每个测试用例使用独立的临时文件，避免状态污染"""
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_vault_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)
    return path


def _make_temp_log():
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_vault_log_")
    os.close(fd)
    return path


class TestSnippetVault(unittest.TestCase):
    """Snippet Vault 单元测试"""

    def setUp(self):
        self.test_path = _make_temp_json()
        self.test_log = _make_temp_log()

    def tearDown(self):
        for p in (self.test_path, self.test_log):
            if os.path.exists(p):
                os.remove(p)

    # ── get_snippet ─────────────────────────────

    def test_snippet_picks_current_language(self):
        """轮换语言应为 Swift（index=2）"""
        result = get_snippet(json_path=self.test_path, log_path=self.test_log)
        self.assertEqual(result["language"], "Swift")

    def test_snippet_returns_all_required_fields(self):
        """片段返回完整字段"""
        result = get_snippet(json_path=self.test_path, log_path=self.test_log)
        for field in ("language", "category", "title", "scenario",
                      "code", "why", "tags", "difficulty",
                      "difficulty_stars", "category_label",
                      "vault_index", "next_language", "generated_at"):
            self.assertIn(field, result, f"缺少字段: {field}")

    def test_snippet_advances_index(self):
        """每次调用后 current_index 应前进一位"""
        expected = ["Swift", "Kotlin", "TypeScript", "JavaScript",
                    "Java", "C/C++", "Rust", "Go"]
        for expected_lang in expected:
            result = get_snippet(json_path=self.test_path, log_path=self.test_log)
            self.assertEqual(result["language"], expected_lang,
                             f"轮到 {expected_lang} 失败")

    def test_snippet_wraps_around(self):
        """索引到达末尾后应循环回 0"""
        for _ in range(8):
            get_snippet(json_path=self.test_path, log_path=self.test_log)
        result = get_snippet(json_path=self.test_path, log_path=self.test_log)
        self.assertEqual(result["language"], "Swift")

    def test_snippet_updates_json(self):
        """调用后 JSON 的 current_index 应更新"""
        get_snippet(json_path=self.test_path, log_path=self.test_log)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 3)
        self.assertEqual(data["last_language"], "Swift")

    def test_snippet_saves_to_log(self):
        """调用后应记录到 vault_log"""
        get_snippet(json_path=self.test_path, log_path=self.test_log)
        self.assertTrue(os.path.exists(self.test_log))
        with open(self.test_log, "r", encoding="utf-8") as f:
            log = json.load(f)
        self.assertEqual(log["total_snippets"], 1)
        self.assertEqual(log["entries"][0]["language"], "Swift")

    def test_snippet_specific_language_no_advance(self):
        """指定语言时不应推进索引"""
        with open(self.test_path, "r", encoding="utf-8") as f:
            before = json.load(f)["current_index"]
        result = get_snippet(language="Rust", json_path=self.test_path, log_path=self.test_log)
        with open(self.test_path, "r", encoding="utf-8") as f:
            after = json.load(f)["current_index"]
        self.assertEqual(before, after)
        self.assertEqual(result["language"], "Rust")

    def test_snippet_category_filter(self):
        """按类别过滤"""
        result = get_snippet(
            language="Rust",
            category=Category.ERROR,
            json_path=self.test_path,
            log_path=self.test_log,
        )
        self.assertEqual(result["language"], "Rust")
        self.assertEqual(result["category"], Category.ERROR)

    def test_snippet_difficulty_filter(self):
        """按难度过滤"""
        result = get_snippet(
            language="Rust",
            difficulty=1,
            json_path=self.test_path,
            log_path=self.test_log,
        )
        self.assertIn(result["difficulty"], [1])

    def test_snippet_next_language(self):
        """next_language 应正确指向下一个"""
        result = get_snippet(json_path=self.test_path, log_path=self.test_log)
        self.assertEqual(result["language"], "Swift")
        self.assertEqual(result["next_language"], "Kotlin")

    # ── format_snippet ─────────────────────────

    def test_console_format_contains_language(self):
        """控制台格式应包含语言名称"""
        result = get_snippet(json_path=self.test_path, log_path=self.test_log)
        fmt = format_snippet_console(result)
        self.assertIn("Swift", fmt)

    def test_console_format_contains_code(self):
        """控制台格式应包含代码"""
        result = get_snippet(json_path=self.test_path, log_path=self.test_log)
        fmt = format_snippet_console(result)
        # 控制台格式使用中文"代码"header
        self.assertIn("💻", fmt)

    def test_markdown_format_contains_language(self):
        """Markdown 格式应包含语言名称"""
        result = get_snippet(json_path=self.test_path, log_path=self.test_log)
        fmt = format_snippet_markdown(result)
        self.assertIn("Swift", fmt)

    # ── search_snippets ─────────────────────────

    def test_search_by_keyword_in_title(self):
        """标题关键词搜索"""
        results = search_snippets("Result", language="Rust")
        self.assertTrue(len(results) > 0)
        titles = [r["title"] for r in results]
        self.assertTrue(any("Result" in t for t in titles),
                        f"未找到 Result 相关标题: {titles}")

    def test_search_by_keyword_in_tags(self):
        """标签关键词搜索"""
        results = search_snippets("iterator", language="Rust")
        self.assertTrue(len(results) > 0)

    def test_search_all_languages(self):
        """不指定语言时搜索所有语言"""
        results = search_snippets("error")
        self.assertTrue(len(results) > 0)

    def test_search_returns_correct_fields(self):
        """搜索结果应包含必要字段"""
        results = search_snippets("channel", language="Go")
        self.assertTrue(len(results) > 0)
        r = results[0]
        for field in ("language", "title", "category", "difficulty", "tags"):
            self.assertIn(field, r)

    # ── get_vault_stats ─────────────────────────

    def test_vault_stats_empty(self):
        """空 vault 应返回零值"""
        st = get_vault_stats(log_path=self.test_log)
        self.assertEqual(st["total_snippets"], 0)

    def test_vault_stats_with_entries(self):
        """有记录时应正确统计"""
        for _ in range(3):
            get_snippet(json_path=self.test_path, log_path=self.test_log)
        st = get_vault_stats(log_path=self.test_log)
        self.assertEqual(st["total_snippets"], 3)
        self.assertIn("Swift", st["language_counts"])

    # ── get_supported_categories ─────────────────

    def test_categories_not_empty(self):
        """类别列表不应为空"""
        cats = get_supported_categories()
        self.assertTrue(len(cats) > 0)
        self.assertTrue(all("id" in c and "label" in c for c in cats))

    # ── SNIPPET_DB ─────────────────────────────

    def test_all_core_languages_have_snippets(self):
        """所有核心语言都有片段"""
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, SNIPPET_DB, f"{lang} 缺少片段库")
            self.assertTrue(len(SNIPPET_DB[lang]) > 0, f"{lang} 片段库为空")

    def test_all_snippets_have_required_fields(self):
        """所有片段都有必要字段"""
        required = {"title", "category", "difficulty", "scenario", "code", "why", "tags"}
        for lang, snippets in SNIPPET_DB.items():
            for s in snippets:
                missing = required - set(s.keys())
                self.assertFalse(missing, f"{lang} 的片段缺少: {missing}")


class TestSnippetVaultIntegration(unittest.TestCase):
    """Snippet Vault 集成测试"""

    def setUp(self):
        self.test_path = _make_temp_json()
        self.test_log = _make_temp_log()

    def tearDown(self):
        for p in (self.test_path, self.test_log):
            if os.path.exists(p):
                os.remove(p)

    def test_full_rotation_cycle(self):
        """完整轮换一圈（8 次）"""
        expected = ["Swift", "Kotlin", "TypeScript", "JavaScript",
                    "Java", "C/C++", "Rust", "Go"]
        seen = []
        for lang in expected:
            result = get_snippet(json_path=self.test_path, log_path=self.test_log)
            seen.append(result["language"])
            self.assertIn(result["language"], CORE_LANGUAGES)
        self.assertEqual(seen, expected)

    def test_snippet_then_status_reflects_next(self):
        """轮换后状态应反映新语言"""
        get_snippet(json_path=self.test_path, log_path=self.test_log)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 3)
        self.assertEqual(data["last_language"], "Swift")

    def test_no_repeated_language_in_one_cycle(self):
        """一轮中每种语言只出现一次"""
        seen = set()
        for _ in range(8):
            result = get_snippet(json_path=self.test_path, log_path=self.test_log)
            lang = result["language"]
            self.assertNotIn(lang, seen, f"语言 {lang} 在本轮中重复出现")
            seen.add(lang)
        self.assertEqual(len(seen), 8)


if __name__ == "__main__":
    unittest.main(verbosity=2)