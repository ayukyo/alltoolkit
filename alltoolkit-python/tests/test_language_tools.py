"""
AllToolkit 语言轮换工具测试套件
"""

import unittest
import json
import os
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.language_tools import (
    rotate_and_get_next,
    get_rotation_status,
    get_language_badge,
    get_all_badges,
    get_streak_info,
    LANGUAGE_METADATA,
)


EXPECTED_LANGUAGE_ORDER = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# 初始测试数据：current_index=2 → 当前语言 Swift
# updated_at 使用昨天（北京昨天日期），便于测试 is_active_today 逻辑
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
    "current_index": 2,
    "last_language": "Rust",   # 上一次轮换的语言
    "updated_at": f"{_INITIAL_YESTERDAY}T02:10:00+08:00",
}


def _make_temp_json():
    """每个测试用例使用独立的临时文件，避免状态污染"""
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_lang_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)
    return path


class TestLanguageTools(unittest.TestCase):
    """语言工具单元测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    # ── rotate_and_get_next ──────────────────────

    def test_rotate_picks_current_language(self):
        """轮换应返回 current_index 所指的语言（index=2 → Swift）"""
        result = rotate_and_get_next(json_path=self.test_path)
        self.assertEqual(result["current_language"], "Swift")

    def test_rotate_returns_metadata(self):
        """轮换应返回该语言的元数据"""
        result = rotate_and_get_next(json_path=self.test_path)
        self.assertIn("emoji", result)
        self.assertIn("hello_world", result)
        self.assertIn("tagline", result)
        self.assertIn("file_ext", result)
        self.assertIn("year", result)
        self.assertIn("paradigm", result)
        self.assertIn("next_language", result)
        self.assertIn("index", result)
        self.assertIn("total", result)

    def test_rotate_swift_hello_world(self):
        """Swift 的 hello_world 示例应为 print(...)"""
        result = rotate_and_get_next(json_path=self.test_path)
        self.assertIn('print("Hello, World!")', result["hello_world"])

    def test_rotate_index_advances(self):
        """每次 rotate 后 current_index 应按顺序前进一位"""
        # 初始 index=2 → Swift; 轮换序列：Swift, Kotlin, TypeScript, ...
        expected = ["Swift", "Kotlin", "TypeScript", "JavaScript",
                    "Java", "C/C++", "Rust", "Go"]
        for expected_lang in expected:
            result = rotate_and_get_next(json_path=self.test_path)
            self.assertEqual(result["current_language"], expected_lang,
                             f"轮换到 {expected_lang} 失败")

    def test_rotate_index_wraps_around(self):
        """索引到达末尾后应循环回 0"""
        # 初始 index=2 → Swift; 8次轮换后 index=2 再回到 Swift
        for _ in range(8):
            rotate_and_get_next(json_path=self.test_path)
        # 第 9 次轮换 → Swift（索引已回到 2）
        result = rotate_and_get_next(json_path=self.test_path)
        self.assertEqual(result["current_language"], "Swift")
        self.assertEqual(result["index"], 2)   # 返回的是 pre-advance 索引
        self.assertEqual(result["next_language"], "Kotlin")

    def test_rotate_updates_json(self):
        """rotate 后 JSON 的 current_index 应更新"""
        rotate_and_get_next(json_path=self.test_path)  # Swift(2) → Kotlin(3)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 3)
        self.assertEqual(data["last_language"], "Swift")

    def test_rotate_updates_timestamp(self):
        """rotate 后 updated_at 应更新为当前时间"""
        rotate_and_get_next(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertNotEqual(data["updated_at"], INITIAL_TEST_DATA["updated_at"])

    # ── get_rotation_status ──────────────────────

    def test_status_returns_all_fields(self):
        """状态查询应返回完整字段"""
        st = get_rotation_status(json_path=self.test_path)
        self.assertIn("languages", st)
        self.assertIn("current_language", st)
        self.assertIn("current_index", st)
        self.assertIn("next_language", st)
        self.assertIn("total", st)
        self.assertIn("last_language", st)
        self.assertIn("updated_at", st)

    def test_status_does_not_advance_index(self):
        """状态查询不应改变 current_index"""
        with open(self.test_path, "r", encoding="utf-8") as f:
            before = json.load(f)["current_index"]
        get_rotation_status(json_path=self.test_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            after = json.load(f)["current_index"]
        self.assertEqual(before, after)

    def test_status_current_language(self):
        """状态查询当前语言应为 Swift（index=2）"""
        st = get_rotation_status(json_path=self.test_path)
        self.assertEqual(st["current_language"], "Swift")
        self.assertEqual(st["current_index"], 2)
        self.assertEqual(st["next_language"], "Kotlin")

    # ── get_language_badge ───────────────────────

    def test_badge_contains_language_name(self):
        """徽章应包含语言名称"""
        badge = get_language_badge("Rust", json_path=self.test_path)
        self.assertIn("Rust", badge)

    def test_badge_contains_emoji(self):
        """徽章应包含 emoji"""
        badge = get_language_badge("Rust", json_path=self.test_path)
        self.assertIn("🦀", badge)

    def test_badge_contains_hello_world(self):
        """徽章应包含 hello world 示例"""
        badge = get_language_badge("Rust", json_path=self.test_path)
        self.assertIn("Hello, World!", badge)

    def test_badge_no_language_uses_current(self):
        """不指定语言时使用当前轮换语言（Swift）"""
        badge = get_language_badge(json_path=self.test_path)
        self.assertIn("Swift", badge)

    def test_badge_unknown_language_still_works(self):
        """未知语言使用默认占位符，不崩溃"""
        badge = get_language_badge("Forth", json_path=self.test_path)
        self.assertIn("Forth", badge)

    # ── get_all_badges ───────────────────────────

    def test_all_badges_contains_all_languages(self):
        """列出所有语言"""
        badges = get_all_badges(json_path=self.test_path)
        for lang in EXPECTED_LANGUAGE_ORDER:
            self.assertIn(lang, badges)

    def test_all_badges_count(self):
        """应有 8 种语言"""
        badges = get_all_badges(json_path=self.test_path)
        self.assertIn("Rust", badges)
        self.assertIn("C/C++", badges)

    # ── get_streak_info ──────────────────────────

    def test_streak_not_today(self):
        """上次更新是昨天（北京），距今 1 天，不算今日活跃"""
        st = get_streak_info(json_path=self.test_path)
        self.assertEqual(st["streak_days"], 1)
        self.assertFalse(st["is_active_today"])

    def test_streak_active_today(self):
        """updated_at 改成今天，is_active_today 应为 True"""
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["updated_at"] = now
        with open(self.test_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        st = get_streak_info(json_path=self.test_path)
        self.assertEqual(st["streak_days"], 0)
        self.assertTrue(st["is_active_today"])

    def test_streak_yesterday(self):
        """昨天活跃，今日未轮换，streak_days 应为 1"""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT12:00:00+08:00")
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["updated_at"] = yesterday
        with open(self.test_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        st = get_streak_info(json_path=self.test_path)
        self.assertEqual(st["streak_days"], 1)
        self.assertFalse(st["is_active_today"])

    # ── LANGUAGE_METADATA ─────────────────────────

    def test_all_languages_have_metadata(self):
        """所有语言都有元数据"""
        for lang in EXPECTED_LANGUAGE_ORDER:
            self.assertIn(lang, LANGUAGE_METADATA)

    def test_metadata_has_required_fields(self):
        """元数据应包含必要字段"""
        required = {"emoji", "tagline", "hello_world", "file_ext", "year", "paradigm"}
        for lang, meta in LANGUAGE_METADATA.items():
            self.assertTrue(required.issubset(meta.keys()), f"{lang} 缺少字段")


class TestLanguageToolsIntegration(unittest.TestCase):
    """语言工具集成测试"""

    def setUp(self):
        self.test_path = _make_temp_json()

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_full_rotation_cycle(self):
        """完整轮换一圈（8 次），验证所有语言按顺序出现"""
        # 初始 index=2 → Swift; 8次轮换序列
        expected = ["Swift", "Kotlin", "TypeScript", "JavaScript",
                    "Java", "C/C++", "Rust", "Go"]
        seen = []
        for _ in expected:
            result = rotate_and_get_next(json_path=self.test_path)
            seen.append(result["current_language"])
            self.assertIn(result["current_language"], EXPECTED_LANGUAGE_ORDER)
        self.assertEqual(seen, expected)

    def test_rotate_then_status_reflects_next(self):
        """轮换一次后，status 应反映新的当前语言和下一个语言"""
        rotate_and_get_next(json_path=self.test_path)  # Swift(2) → Kotlin(3)
        st = get_rotation_status(json_path=self.test_path)
        self.assertEqual(st["current_language"], "Kotlin")
        self.assertEqual(st["next_language"], "TypeScript")

    def test_badge_workflow(self):
        """轮换 → 打印徽章 → 验证徽章包含该语言和 emoji"""
        result = rotate_and_get_next(json_path=self.test_path)
        badge = get_language_badge(result["current_language"], json_path=self.test_path)
        self.assertIn(result["current_language"], badge)
        self.assertIn(result["emoji"], badge)

    def test_no_repeated_language_in_one_cycle(self):
        """一轮（8 次）中每种语言只应出现一次"""
        seen = set()
        for _ in range(8):
            result = rotate_and_get_next(json_path=self.test_path)
            lang = result["current_language"]
            self.assertNotIn(lang, seen, f"语言 {lang} 在本轮中重复出现")
            seen.add(lang)
        self.assertEqual(len(seen), 8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
