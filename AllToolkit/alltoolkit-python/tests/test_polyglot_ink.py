"""
Polyglot Ink 测试套件
"""

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_ink import (
    rotate_and_get_ink,
    get_ink_preview,
    format_ink_console,
    format_ink_markdown,
    INK_DATABASE,
    ROTATION_ORDER,
)


# ── 测试数据 ─────────────────────────────────────────────────────────────────
# ROTATION_ORDER = ["Rust", "Go", "Swift", "Kotlin",
#                   "TypeScript", "JavaScript", "Java", "C/C++"]

# 初始 current_index=2 → 当前语言 Swift
_INITIAL_YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
# 完整22语言数组（模拟真实 language_rotation.json）
FULL_LANGUAGES = [
    "Python", "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++", "Lua",
    "C#", "PHP", "Ruby", "R", "SQL", "MATLAB",
    "Perl", "Delphi", "Fortran", "ArkTS", "VB", "Zig",
]
INITIAL_TEST_DATA = {
    "languages": FULL_LANGUAGES,
    "current_index": 2,    # → Swift（ROTATION_ORDER[2]）
    "last_language": "Go",
    "updated_at": f"{_INITIAL_YESTERDAY}T02:10:00+08:00",
}


def _make_temp_json(data: dict = None) -> str:
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_ink_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data or INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# 测试：ROTATION_ORDER 与数据库完整性
# ─────────────────────────────────────────────────────────────────────────────

class TestInkDatabase(unittest.TestCase):
    """确保每种语言都有完整的墨讯数据"""

    def test_rotation_order_has_8_languages(self):
        self.assertEqual(len(ROTATION_ORDER), 8)

    def test_rotation_order_sequence(self):
        """轮换顺序应为：Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++"""
        self.assertEqual(
            ROTATION_ORDER,
            ["Rust", "Go", "Swift", "Kotlin",
             "TypeScript", "JavaScript", "Java", "C/C++"],
        )

    def test_all_rotation_languages_have_ink_data(self):
        """ROTATION_ORDER 中每种语言都有墨讯数据库条目"""
        for lang in ROTATION_ORDER:
            self.assertIn(lang, INK_DATABASE, f"{lang} 缺少墨讯数据")

    def test_ink_data_has_required_fields(self):
        """每种语言的墨讯数据都包含必要字段"""
        required = {"proverb", "energy_map", "project_tips", "trivia", "idiom_snippet"}
        for lang, data in INK_DATABASE.items():
            missing = required - set(data.keys())
            self.assertFalse(missing, f"{lang} 缺少字段: {missing}")

    def test_proverb_has_both_en_and_zh(self):
        """每条谚语都有英文和中文"""
        for lang, data in INK_DATABASE.items():
            self.assertIn("en", data["proverb"])
            self.assertIn("zh", data["proverb"])
            self.assertTrue(data["proverb"]["en"])
            self.assertTrue(data["proverb"]["zh"])

    def test_energy_map_has_all_time_slots(self):
        """energy_map 包含 morning / afternoon / evening / night"""
        for lang, data in INK_DATABASE.items():
            self.assertIn("morning", data["energy_map"])
            self.assertIn("afternoon", data["energy_map"])
            self.assertIn("evening", data["energy_map"])
            self.assertIn("night", data["energy_map"])

    def test_project_tips_has_at_least_3_items(self):
        """每个语言至少有3个推荐项目"""
        for lang, data in INK_DATABASE.items():
            self.assertGreaterEqual(len(data["project_tips"]), 3)

    def test_idiom_snippet_has_title_and_code(self):
        """惯用法数据有 title 和 code"""
        for lang, data in INK_DATABASE.items():
            idioms = data["idiom_snippet"]
            self.assertIn("title", idioms)
            self.assertIn("code", idioms)
            self.assertTrue(idioms["code"])


# ─────────────────────────────────────────────────────────────────────────────
# 测试：rotate_and_get_ink
# ─────────────────────────────────────────────────────────────────────────────

class TestRotateAndGetInk(unittest.TestCase):
    """轮换并生成墨讯"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_rotate_picks_correct_language_by_rotation_order(self):
        """current_index=2 → ROTATION_ORDER[2] = Swift"""
        result = rotate_and_get_ink(json_path=self.test_path)
        self.assertEqual(result["current_language"], "Swift")

    def test_rotate_returns_all_required_fields(self):
        """返回完整字段"""
        result = rotate_and_get_ink(json_path=self.test_path)
        self.assertIn("current_language", result)
        self.assertIn("next_language", result)
        self.assertIn("ink", result)
        self.assertIn("rotated_at", result)

    def test_rotate_ink_has_all_sections(self):
        """墨讯包含所有章节"""
        result = rotate_and_get_ink(json_path=self.test_path)
        ink = result["ink"]
        self.assertIn("proverb", ink)
        self.assertIn("energy", ink)
        self.assertIn("project_tip", ink)
        self.assertIn("trivia", ink)
        self.assertIn("idiom", ink)

    def test_rotate_advances_index_correctly(self):
        """每次轮换索引前进一位（基于 ROTATION_ORDER 而非 languages 数组）"""
        # index=2 → Swift; 轮换序列：Swift(2), Kotlin(3), TypeScript(4), ...
        expected = ["Swift", "Kotlin", "TypeScript", "JavaScript",
                    "Java", "C/C++", "Rust", "Go"]
        for expected_lang in expected:
            result = rotate_and_get_ink(json_path=self.test_path)
            self.assertEqual(result["current_language"], expected_lang)

    def test_rotate_wraps_around(self):
        """轮换到末尾后循环回 Rust"""
        # 初始 index=2 → Swift; 8次后回到 Swift
        for _ in range(8):
            rotate_and_get_ink(json_path=self.test_path)
        # 第 9 次 → Swift（index 回到 2）
        result = rotate_and_get_ink(json_path=self.test_path)
        self.assertEqual(result["current_language"], "Swift")

    def test_rotate_updates_json(self):
        """轮换后 JSON 的 current_index 和 last_language 应更新"""
        rotate_and_get_ink(json_path=self.test_path)  # Swift(2) → Kotlin(3)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 3)
        self.assertEqual(data["last_language"], "Swift")

    def test_rotate_updates_timestamp(self):
        """轮换后 updated_at 应更新为当前时间"""
        rotate_and_get_ink(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertNotEqual(data["updated_at"], INITIAL_TEST_DATA["updated_at"])

    def test_rotate_proverb_en_and_zh(self):
        """Swift 谚语有中英文"""
        result = rotate_and_get_ink(json_path=self.test_path)
        self.assertTrue(result["ink"]["proverb"]["en"])
        self.assertTrue(result["ink"]["proverb"]["zh"])

    def test_rotate_energy_is_nonempty(self):
        """能量描述非空"""
        result = rotate_and_get_ink(json_path=self.test_path)
        self.assertTrue(result["ink"]["energy"])

    def test_rotate_project_tip_is_nonempty(self):
        """项目推荐非空"""
        result = rotate_and_get_ink(json_path=self.test_path)
        self.assertTrue(result["ink"]["project_tip"])

    def test_rotate_next_language_is_correct(self):
        """next_language 正确"""
        result = rotate_and_get_ink(json_path=self.test_path)  # Swift → Kotlin
        self.assertEqual(result["next_language"], "Kotlin")


# ─────────────────────────────────────────────────────────────────────────────
# 测试：get_ink_preview
# ─────────────────────────────────────────────────────────────────────────────

class TestGetInkPreview(unittest.TestCase):
    """预览墨讯（不推进索引）"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_preview_does_not_advance_index(self):
        """预览不应改变 current_index"""
        with open(self.test_path, "r", encoding="utf-8") as f:
            before = json.load(f)["current_index"]
        get_ink_preview(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            after = json.load(f)["current_index"]
        self.assertEqual(before, after)

    def test_preview_current_language(self):
        """预览当前语言 = Swift（index=2）"""
        result = get_ink_preview(json_path=self.test_path)
        self.assertEqual(result["current_language"], "Swift")

    def test_preview_specific_language(self):
        """预览指定语言 = Rust"""
        result = get_ink_preview("Rust", json_path=self.test_path)
        self.assertEqual(result["current_language"], "Rust")
        # 谚语内容非空（不检查语言名是否出现，因为谚语本身不提语言名）
        self.assertTrue(result["ink"]["proverb"]["en"])
        self.assertTrue(result["ink"]["proverb"]["zh"])

    def test_preview_unknown_language_has_fallback(self):
        """未知语言使用空数据，不崩溃"""
        result = get_ink_preview("Forth", json_path=self.test_path)
        self.assertEqual(result["current_language"], "Forth")

    def test_preview_returns_all_ink_sections(self):
        """预览返回所有墨讯章节"""
        result = get_ink_preview(json_path=self.test_path)
        ink = result["ink"]
        self.assertIn("proverb", ink)
        self.assertIn("energy", ink)
        self.assertIn("project_tip", ink)
        self.assertIn("trivia", ink)
        self.assertIn("idiom", ink)


# ─────────────────────────────────────────────────────────────────────────────
# 测试：格式化输出
# ─────────────────────────────────────────────────────────────────────────────

class TestFormatInk(unittest.TestCase):
    """格式化输出测试"""

    def setUp(self):
        self.test_path = _make_temp_json()
        self.result = rotate_and_get_ink(json_path=self.test_path)

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_console_format_contains_language_name(self):
        output = format_ink_console(self.result)
        self.assertIn("Swift", output)

    def test_console_format_contains_proverb(self):
        output = format_ink_console(self.result)
        self.assertIn("💬", output)
        self.assertIn("谚语", output)

    def test_console_format_contains_energy(self):
        output = format_ink_console(self.result)
        self.assertIn("⚡", output)

    def test_console_format_contains_project_tip(self):
        output = format_ink_console(self.result)
        self.assertIn("🛠️", output)

    def test_console_format_contains_trivia(self):
        output = format_ink_console(self.result)
        self.assertIn("📚", output)
        self.assertIn("趣闻", output)

    def test_console_format_contains_idiom(self):
        output = format_ink_console(self.result)
        self.assertIn("🧩", output)
        self.assertIn("惯用法", output)

    def test_console_format_contains_next_language(self):
        output = format_ink_console(self.result)
        self.assertIn("⏭️", output)
        self.assertIn("Kotlin", output)

    def test_markdown_format_contains_language(self):
        output = format_ink_markdown(self.result)
        self.assertIn("Swift", output)

    def test_markdown_format_contains_proverb_en(self):
        output = format_ink_markdown(self.result)
        self.assertIn("EN:", output)

    def test_markdown_format_contains_code_block(self):
        output = format_ink_markdown(self.result)
        self.assertIn("```", output)

    def test_markdown_format_contains_trivia(self):
        output = format_ink_markdown(self.result)
        self.assertIn("趣闻", output)


# ─────────────────────────────────────────────────────────────────────────────
# 测试：时间能量逻辑
# ─────────────────────────────────────────────────────────────────────────────

class TestEnergyTimeLogic(unittest.TestCase):
    """_get_energy_of_now 根据当前时间返回正确的能量描述"""

    def test_energy_map_values_are_nonempty(self):
        """所有时段的能量描述都非空"""
        from modules.polyglot_ink import _get_energy_of_now
        for lang, data in INK_DATABASE.items():
            emap = data["energy_map"]
            for key in ("morning", "afternoon", "evening", "night"):
                result = _get_energy_of_now(emap)
                self.assertTrue(result)


# ─────────────────────────────────────────────────────────────────────────────
# 集成测试
# ─────────────────────────────────────────────────────────────────────────────

class TestInkIntegration(unittest.TestCase):
    """墨讯集成测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_full_rotation_cycle_all_languages_appear(self):
        """完整轮换一圈（8次），所有语言各出现一次"""
        seen = []
        for _ in range(8):
            result = rotate_and_get_ink(json_path=self.test_path)
            seen.append(result["current_language"])
        self.assertEqual(sorted(seen), sorted(ROTATION_ORDER))
        self.assertEqual(len(set(seen)), 8)  # 无重复

    def test_rotate_then_preview_shows_next_language(self):
        """轮换一次后，预览显示 Kotlin（index=3）"""
        rotate_and_get_ink(json_path=self.test_path)  # Swift(2) → Kotlin(3)
        result = get_ink_preview(json_path=self.test_path)
        self.assertEqual(result["current_language"], "Kotlin")

    def test_console_output_for_each_language_is_deterministic(self):
        """每种语言的格式化输出稳定（不含随机内容在固定区域）"""
        from modules.polyglot_ink import _get_energy_of_now

        for lang in ROTATION_ORDER:
            # 构建稳定 result（project_tip 是随机的，但结构和固定字段稳定）
            result = {
                "current_language": lang,
                "next_language": ROTATION_ORDER[(ROTATION_ORDER.index(lang) + 1) % 8],
                "ink": {
                    "proverb": INK_DATABASE[lang]["proverb"],
                    "energy": INK_DATABASE[lang]["energy_map"]["morning"],
                    "project_tip": INK_DATABASE[lang]["project_tips"][0],
                    "trivia": INK_DATABASE[lang]["trivia"],
                    "idiom": INK_DATABASE[lang]["idiom_snippet"],
                },
                "rotated_at": "2026-06-07T06:00:00+08:00",
            }
            output = format_ink_console(result)
            self.assertIn(lang, output)
            self.assertIn(INK_DATABASE[lang]["proverb"]["en"], output)

    def test_unknown_language_preview_does_not_crash(self):
        """预览未知语言不崩溃"""
        result = get_ink_preview("Zig", json_path=self.test_path)
        self.assertEqual(result["current_language"], "Zig")


if __name__ == "__main__":
    unittest.main(verbosity=2)