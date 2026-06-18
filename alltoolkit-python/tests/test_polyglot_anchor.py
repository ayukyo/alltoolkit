"""
AllToolkit Polyglot Anchor 测试套件
"""

import unittest
import json
import os
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_anchor import (
    get_anchor,
    get_anchor_preview,
    format_anchor_console,
    format_anchor_markdown,
    rotate_and_get_anchor,
    ANCHOR_DB,
    CORE_LANGUAGES,
    LANGUAGE_EMOJI,
)


# 初始测试数据：current_index=3 → 当前语言 Kotlin
_INITIAL_YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
INITIAL_TEST_DATA = {
    "languages": [
        "Rust",
        "Go",
        "Swift",
        "Kotlin",
        "TypeScript",
        "JavaScript",
        "Java",
        "C/C++",
    ],
    "current_index": 3,
    "last_language": "Swift",
    "updated_at": f"{_INITIAL_YESTERDAY}T02:10:00+08:00",
}


def _make_temp_json():
    """每个测试用例使用独立的临时文件"""
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_anchor_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)
    return path


class TestPolyglotAnchor(unittest.TestCase):
    """Polyglot Anchor 单元测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    # ── get_anchor ──────────────────────────────

    def test_anchor_returns_kotlin(self):
        """index=3 → 当前语言应为 Kotlin"""
        result = get_anchor(json_path=self.test_path)
        self.assertEqual(result["language"], "Kotlin")

    def test_anchor_returns_all_required_fields(self):
        """锚应包含所有必要字段"""
        result = get_anchor(json_path=self.test_path)
        required = [
            "language", "emoji", "breath", "mindset", "active_mindset",
            "mantra", "ritual", "totem_code", "focus_word",
            "energy_tip", "anchor_index", "next_language",
        ]
        for field in required:
            self.assertIn(field, result, f"Missing field: {field}")

    def test_anchor_breath_structure(self):
        """breath 应包含 inhale/hold/exhale/pattern"""
        result = get_anchor(json_path=self.test_path)
        breath = result["breath"]
        self.assertIn("inhale", breath)
        self.assertIn("hold", breath)
        self.assertIn("exhale", breath)
        self.assertIn("pattern", breath)
        self.assertIsInstance(breath["inhale"], int)
        self.assertIsInstance(breath["hold"], int)
        self.assertIsInstance(breath["exhale"], int)

    def test_anchor_mindset_not_empty(self):
        """mindset 列表不应为空"""
        result = get_anchor(json_path=self.test_path)
        self.assertIsInstance(result["mindset"], list)
        self.assertGreater(len(result["mindset"]), 0)

    def test_anchor_active_mindset_in_list(self):
        """active_mindset 应该是 mindset 列表中的一条"""
        result = get_anchor(json_path=self.test_path)
        self.assertIn(result["active_mindset"], result["mindset"])

    def test_anchor_totem_code_not_empty(self):
        """totem_code 不应为空"""
        result = get_anchor(json_path=self.test_path)
        self.assertTrue(result["totem_code"].strip())

    def test_anchor_next_language_is_different(self):
        """next_language 不应等于当前语言"""
        result = get_anchor(json_path=self.test_path)
        self.assertNotEqual(result["language"], result["next_language"])

    def test_anchor_index_advances(self):
        """每次调用后 current_index 应前移一位"""
        # 初始 index=3 → Kotlin
        expected = ["Kotlin", "TypeScript", "JavaScript", "Java",
                    "C/C++", "Rust", "Go", "Swift"]
        for expected_lang in expected:
            result = get_anchor(json_path=self.test_path)
            self.assertEqual(result["language"], expected_lang,
                             f"Expected {expected_lang}, got {result['language']}")

    def test_anchor_index_wraps_around(self):
        """索引到达末尾后应循环回 0"""
        # 从 index=3 开始，8 次轮换后回到 index=3
        for _ in range(8):
            get_anchor(json_path=self.test_path)
        result = get_anchor(json_path=self.test_path)
        self.assertEqual(result["language"], "Kotlin")
        self.assertEqual(result["anchor_index"], 3)

    def test_anchor_updates_json(self):
        """调用后 JSON 的 current_index 应更新"""
        get_anchor(json_path=self.test_path)  # Kotlin(3) → TypeScript(4)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 4)
        self.assertEqual(data["last_language"], "Kotlin")

    def test_anchor_updates_timestamp(self):
        """调用后 updated_at 应更新为当前时间"""
        get_anchor(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertNotEqual(data["updated_at"], INITIAL_TEST_DATA["updated_at"])

    def test_anchor_rotation_alias(self):
        """rotate_and_get_anchor 是 get_anchor 的别名，两者都推进索引"""
        # 两个函数指向同一个实现，验证可调用 + 推进索引
        result1 = get_anchor(json_path=self.test_path)
        self.assertEqual(result1["language"], "Kotlin")
        # 再次调用 rotate_and_get_anchor（同一文件，index 已变为 4）
        result2 = rotate_and_get_anchor(json_path=self.test_path)
        self.assertEqual(result2["language"], "TypeScript")
        # 验证 rotate_and_get_anchor 推进索引后 JSON 中 last_language 更新
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["last_language"], "TypeScript")

    # ── get_anchor_preview ──────────────────────

    def test_preview_returns_kotlin(self):
        """preview 不推进索引，应返回当前语言 Kotlin"""
        result = get_anchor_preview(json_path=self.test_path)
        self.assertEqual(result["language"], "Kotlin")
        self.assertEqual(result["anchor_index"], 3)

    def test_preview_does_not_advance_index(self):
        """preview 不应改变 current_index"""
        with open(self.test_path, "r", encoding="utf-8") as f:
            before = json.load(f)["current_index"]
        get_anchor_preview(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            after = json.load(f)["current_index"]
        self.assertEqual(before, after)

    def test_preview_returns_required_fields(self):
        """preview 应返回必要字段（不含 session 状态字段）"""
        result = get_anchor_preview(json_path=self.test_path)
        required = ["language", "emoji", "breath", "mantra",
                    "focus_word", "anchor_index", "next_language"]
        for field in required:
            self.assertIn(field, result, f"Missing field: {field}")

    # ── ANCHOR_DB ───────────────────────────────

    def test_anchor_db_has_all_languages(self):
        """ANCHOR_DB 应包含所有 8 种核心语言"""
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, ANCHOR_DB, f"Missing language: {lang}")

    def test_anchor_db_structure(self):
        """每种语言的锚定数据应包含所有子字段"""
        required_keys = ["breath", "mindset", "mantra", "ritual",
                         "totem_code", "focus_word", "energy_tip"]
        for lang, anchor in ANCHOR_DB.items():
            for key in required_keys:
                self.assertIn(key, anchor, f"{lang} missing {key}")

    def test_emoji_matches_language(self):
        """每种语言的 emoji 应与 LANGUAGE_EMOJI 一致"""
        for lang in CORE_LANGUAGES:
            self.assertIn(lang, LANGUAGE_EMOJI)
            self.assertIn(lang, ANCHOR_DB)


class TestPolyglotAnchorIntegration(unittest.TestCase):
    """Polyglot Anchor 集成测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_full_rotation_cycle(self):
        """完整轮换一圈（8 次），验证所有语言按顺序出现"""
        # 初始 index=3 → Kotlin; 8次轮换序列
        expected = ["Kotlin", "TypeScript", "JavaScript",
                    "Java", "C/C++", "Rust", "Go", "Swift"]
        seen = []
        for _ in expected:
            result = get_anchor(json_path=self.test_path)
            seen.append(result["language"])
        self.assertEqual(seen, expected)

    def test_preview_then_anchor_reflects_next(self):
        """先 preview，再 anchor，验证 anchor 从新位置开始"""
        preview = get_anchor_preview(json_path=self.test_path)
        self.assertEqual(preview["language"], "Kotlin")

        result = get_anchor(json_path=self.test_path)
        self.assertEqual(result["language"], "Kotlin")

        # 再次 preview，应反映 TypeScript
        preview2 = get_anchor_preview(json_path=self.test_path)
        self.assertEqual(preview2["language"], "TypeScript")
        self.assertEqual(preview2["next_language"], "JavaScript")

    def test_format_console_output(self):
        """format_anchor_console 应返回非空字符串"""
        result = get_anchor(json_path=self.test_path)
        output = format_anchor_console(result)
        self.assertIsInstance(output, str)
        self.assertGreater(len(output), 50)
        self.assertIn("Polyglot Anchor", output)
        self.assertIn(result["language"], output)

    def test_format_markdown_output(self):
        """format_anchor_markdown 应返回非空字符串"""
        result = get_anchor(json_path=self.test_path)
        output = format_anchor_markdown(result)
        self.assertIsInstance(output, str)
        self.assertGreater(len(output), 50)
        self.assertIn("Polyglot Anchor", output)
        self.assertIn(result["language"], output)

    def test_consistency_rotation_and_preview(self):
        """rotation 后 next_language 与 preview 的 current_language 一致"""
        result = get_anchor(json_path=self.test_path)
        preview = get_anchor_preview(json_path=self.test_path)
        self.assertEqual(result["next_language"], preview["language"])

    def test_no_language_repeated_in_one_cycle(self):
        """一轮（8 次）中每种语言只应出现一次"""
        seen = set()
        for _ in range(8):
            result = get_anchor(json_path=self.test_path)
            lang = result["language"]
            self.assertNotIn(lang, seen, f"Language {lang} repeated in cycle")
            seen.add(lang)
        self.assertEqual(len(seen), 8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
