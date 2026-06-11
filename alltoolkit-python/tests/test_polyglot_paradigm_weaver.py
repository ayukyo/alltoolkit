"""
AllToolkit Polyglot Paradigm Weaver 测试套件
"""

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_paradigm_weaver import (
    rotate_and_weave,
    get_weave_preview,
    format_weave_console,
    format_weave_markdown,
    CORE_LANGUAGES,
    LANGUAGE_EMOJI,
    LANGUAGE_EXT,
    PARADIGM_KEYS,
    PARADIGM_DATABASE,
    DEFAULT_LANGUAGE_ROTATION_JSON,
)


# 初始测试数据：current_index=1 → 当前语言 Go
_INITIAL_YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
INITIAL_TEST_DATA = {
    "languages": [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ],
    "current_index": 1,
    "last_language": "Rust",
    "updated_at": f"{_INITIAL_YESTERDAY}T02:10:00+08:00",
}


def _make_temp_json():
    """每个测试用例使用独立的临时文件，避免状态污染"""
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_weave_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)
    return path


class TestParadigmWeaver(unittest.TestCase):
    """Paradigm Weaver 单元测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    # ── rotate_and_weave ─────────────────────────

    def test_weave_returns_current_language(self):
        """轮换应返回 current_index 所指的语言（index=1 → Go）"""
        result = rotate_and_weave(json_path=self.test_path)
        self.assertEqual(result["current_language"], "Go")

    def test_weave_returns_all_required_fields(self):
        """返回字典应包含所有必要字段"""
        result = rotate_and_weave(json_path=self.test_path)
        self.assertIn("current_language", result)
        self.assertIn("next_language", result)
        self.assertIn("paradigm", result)
        self.assertIn("language_examples", result)
        self.assertIn("rotation_index", result)
        self.assertIn("paradigm_index", result)
        self.assertIn("rotated_at", result)

    def test_weave_paradigm_has_required_fields(self):
        """paradigm 字段应包含 title、title_en、description"""
        result = rotate_and_weave(json_path=self.test_path)
        p = result["paradigm"]
        self.assertIn("title", p)
        self.assertIn("title_en", p)
        self.assertIn("description", p)
        self.assertIn("key", p)

    def test_weave_language_examples_has_all_8_languages(self):
        """language_examples 应包含全部 8 种语言"""
        result = rotate_and_weave(json_path=self.test_path)
        examples = result["language_examples"]
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, examples)

    def test_weave_language_examples_have_code_and_explanation(self):
        """每个语言的示例应包含 code 和 explanation"""
        result = rotate_and_weave(json_path=self.test_path)
        examples = result["language_examples"]
        for lang in CORE_LANGUAGES:
            ex = examples[lang]
            self.assertIn("code", ex)
            self.assertIn("explanation", ex)
            self.assertIn("emoji", ex)
            self.assertTrue(len(ex["code"]) > 10, f"{lang} code is too short")

    def test_weave_language_advances_index(self):
        """每次 weave 后 current_index 应前进一位"""
        expected = ["Go", "Swift", "Kotlin", "TypeScript",
                    "JavaScript", "Java", "C/C++", "Rust", "Go"]
        for expected_lang in expected:
            result = rotate_and_weave(json_path=self.test_path)
            self.assertEqual(result["current_language"], expected_lang,
                             f"轮换到 {expected_lang} 失败")

    def test_weave_index_wraps_around(self):
        """索引到达末尾后应循环回 0"""
        # 初始 index=1 → Go; 8次轮换后 index 回到 1
        for _ in range(8):
            rotate_and_weave(json_path=self.test_path)
        # 第 9 次轮换 → Go（索引已回到 1）
        result = rotate_and_weave(json_path=self.test_path)
        self.assertEqual(result["current_language"], "Go")

    def test_weave_updates_json(self):
        """weave 后 JSON 的 current_index 应更新"""
        rotate_and_weave(json_path=self.test_path)  # Go(1) → Swift(2)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 2)
        self.assertEqual(data["last_language"], "Go")

    def test_weave_updates_timestamp(self):
        """weave 后 updated_at 应更新为当前时间"""
        rotate_and_weave(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertNotEqual(data["updated_at"], INITIAL_TEST_DATA["updated_at"])

    def test_weave_paradigm_key_valid(self):
        """paradigm key 必须在 PARADIGM_KEYS 中"""
        result = rotate_and_weave(json_path=self.test_path)
        self.assertIn(result["paradigm"]["key"], PARADIGM_KEYS)

    def test_weave_paradigm_in_database(self):
        """paradigm 内容必须在 PARADIGM_DATABASE 中"""
        result = rotate_and_weave(json_path=self.test_path)
        key = result["paradigm"]["key"]
        self.assertIn(key, PARADIGM_DATABASE)
        self.assertEqual(result["paradigm"]["title"], PARADIGM_DATABASE[key]["title"])

    def test_weave_next_language_correct(self):
        """next_language 应该是 languages 数组中当前索引的下一位"""
        result = rotate_and_weave(json_path=self.test_path)
        # index=1 → Go, next 应该是 Swift
        self.assertEqual(result["next_language"], "Swift")

    # ── get_weave_preview ───────────────────────

    def test_preview_no_language_uses_current(self):
        """不指定语言时使用当前轮换语言（Go）"""
        result = get_weave_preview(json_path=self.test_path)
        self.assertEqual(result["language"], "Go")

    def test_preview_specified_language(self):
        """指定语言时返回该语言的示例"""
        result = get_weave_preview("Rust", json_path=self.test_path)
        self.assertEqual(result["language"], "Rust")

    def test_preview_does_not_advance_index(self):
        """preview 不应改变 current_index"""
        with open(self.test_path, "r", encoding="utf-8") as f:
            before = json.load(f)["current_index"]
        get_weave_preview(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            after = json.load(f)["current_index"]
        self.assertEqual(before, after)

    def test_preview_returns_example(self):
        """preview 应返回 example 字段包含 code 和 explanation"""
        result = get_weave_preview("Rust", json_path=self.test_path)
        self.assertIn("example", result)
        self.assertIn("code", result["example"])
        self.assertIn("explanation", result["example"])

    # ── format_weave_console ────────────────────

    def test_console_output_contains_language(self):
        """控制台输出应包含当前语言名称"""
        result = rotate_and_weave(json_path=self.test_path)
        output = format_weave_console(result)
        self.assertIn(result["current_language"], output)

    def test_console_output_contains_paradigm_title(self):
        """控制台输出应包含范式标题"""
        result = rotate_and_weave(json_path=self.test_path)
        output = format_weave_console(result)
        self.assertIn(result["paradigm"]["title"], output)

    def test_console_output_contains_code(self):
        """控制台输出应包含代码示例"""
        result = rotate_and_weave(json_path=self.test_path)
        output = format_weave_console(result)
        # 应包含至少一种语言的代码
        self.assertIn("fn main", output)  # Rust/Go/Swift 特征代码

    # ── format_weave_markdown ───────────────────

    def test_markdown_output_contains_language(self):
        """Markdown 输出应包含语言名称"""
        result = rotate_and_weave(json_path=self.test_path)
        output = format_weave_markdown(result)
        self.assertIn(result["current_language"], output)

    def test_markdown_output_contains_code_fences(self):
        """Markdown 输出应包含代码高亮标记（```）"""
        result = rotate_and_weave(json_path=self.test_path)
        output = format_weave_markdown(result)
        self.assertIn("```", output)

    # ── CORE_LANGUAGES ───────────────────────────

    def test_core_languages_has_8_items(self):
        """CORE_LANGUAGES 应包含 8 种语言"""
        self.assertEqual(len(CORE_LANGUAGES), 8)

    def test_core_languages_order(self):
        """CORE_LANGUAGES 应按正确顺序排列"""
        expected = ["Rust", "Go", "Swift", "Kotlin",
                    "TypeScript", "JavaScript", "Java", "C/C++"]
        self.assertEqual(CORE_LANGUAGES, expected)

    def test_language_emoji_has_all_languages(self):
        """LANGUAGE_EMOJI 应包含所有 8 种语言"""
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, LANGUAGE_EMOJI)

    def test_language_ext_has_all_languages(self):
        """LANGUAGE_EXT 应包含所有 8 种语言"""
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, LANGUAGE_EXT)

    def test_paradigm_database_has_all_8_themes(self):
        """PARADIGM_DATABASE 应包含 8 个主题"""
        self.assertEqual(len(PARADIGM_DATABASE), 8)

    def test_paradigm_keys_matches_database(self):
        """PARADIGM_KEYS 应与 PARADIGM_DATABASE 的 key 一致"""
        self.assertEqual(set(PARADIGM_KEYS), set(PARADIGM_DATABASE.keys()))

    def test_all_paradigms_have_all_8_languages(self):
        """每个范式主题的 concepts 应包含全部 8 种语言"""
        for key, paradigm in PARADIGM_DATABASE.items():
            concepts = paradigm["concepts"]
            for lang in CORE_LANGUAGES:
                self.assertIn(lang, concepts,
                              f"Paradigm '{key}' missing language '{lang}'")
                code = concepts[lang].get("code", "")
                self.assertTrue(len(code) > 10,
                                f"Paradigm '{key}', language '{lang}' has short code")


class TestParadigmWeaverIntegration(unittest.TestCase):
    """Paradigm Weaver 集成测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_full_rotation_cycle_all_languages(self):
        """完整轮换一圈（8 次），验证所有语言按顺序出现"""
        seen = []
        for _ in range(8):
            result = rotate_and_weave(json_path=self.test_path)
            seen.append(result["current_language"])
        expected = ["Go", "Swift", "Kotlin", "TypeScript",
                    "JavaScript", "Java", "C/C++", "Rust"]
        self.assertEqual(seen, expected)

    def test_weave_then_preview_reflects_next(self):
        """轮换一次后，preview 应反映新的当前语言"""
        rotate_and_weave(json_path=self.test_path)  # Go(1) → Swift(2)
        result = get_weave_preview(json_path=self.test_path)
        self.assertEqual(result["language"], "Swift")

    def test_paradigm_changes_every_rotation(self):
        """每次轮换语言时，paradigm_index 应前进一位（8次轮换覆盖全部 8 个主题）"""
        paradigm_keys_seen = []
        for i in range(8):
            result = rotate_and_weave(json_path=self.test_path)
            paradigm_keys_seen.append(result["paradigm"]["key"])
        # 8 次轮换应看到 8 个不同的 paradigm key
        self.assertEqual(len(set(paradigm_keys_seen)), 8,
                         "8 次轮换应覆盖全部 8 个范式主题")

    def test_paradigm_wraps_after_8_rotations(self):
        """第 9 次轮换时，paradigm_index 已在 0-7 范围内循环"""
        # 先跑 8 次轮换
        for _ in range(8):
            rotate_and_weave(json_path=self.test_path)
        # current_index 此时应为 9，paradigm_idx = 9 % 8 = 1
        # 第 9 次轮换后 current_index 变为 10，next_idx = 2，paradigm_idx = 2
        result = rotate_and_weave(json_path=self.test_path)
        # paradigm_index 应该在 0-7 范围内（已循环）
        self.assertIn(result["paradigm_index"], range(8),
                         "paradigm_index 应在 0-7 范围内")

    def test_all_paradigm_keys_covered_in_8_rotations(self):
        """连续 8 次轮换应覆盖所有 8 个范式主题"""
        covered = set()
        for i in range(8):
            result = rotate_and_weave(json_path=self.test_path)
            covered.add(result["paradigm"]["key"])
        self.assertEqual(len(covered), 8, "应覆盖全部 8 个范式主题")

    def test_console_output_every_rotation(self):
        """每次轮换的 console 输出都应包含 8 种语言"""
        for _ in range(3):
            result = rotate_and_weave(json_path=self.test_path)
            output = format_weave_console(result)
            for lang in CORE_LANGUAGES:
                self.assertIn(lang, output, f"Output missing language {lang}")

    def test_markdown_output_every_rotation(self):
        """每次轮换的 markdown 输出都应包含 8 种语言"""
        for _ in range(3):
            result = rotate_and_weave(json_path=self.test_path)
            output = format_weave_markdown(result)
            for lang in CORE_LANGUAGES:
                self.assertIn(lang, output, f"Markdown missing language {lang}")

    def test_json_update_preserves_other_fields(self):
        """JSON 更新后除 current_index/last_language/updated_at 外其他字段应保持不变"""
        rotate_and_weave(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["languages"], INITIAL_TEST_DATA["languages"])
        self.assertEqual(data["last_language"], "Go")


if __name__ == "__main__":
    unittest.main(verbosity=2)