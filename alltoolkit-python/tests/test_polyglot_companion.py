"""
test_polyglot_companion.py — Polyglot Companion 单元测试
"""

import unittest
import json
import os
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.polyglot_companion import (
    generate_adventure,
    get_adventure_report,
    get_companion_stats,
    LANGUAGE_ADVENTURES,
    POMODORO_STEPS,
)


# 初始测试数据：current_index=2 → Swift
_INITIAL_YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
INITIAL_TEST_DATA = {
    "languages": ["Rust", "Go", "Swift", "Kotlin",
                 "TypeScript", "JavaScript", "Java", "C/C++"],
    "current_index": 2,
    "last_language": "Go",
    "updated_at": f"{_INITIAL_YESTERDAY}T02:10:00+08:00",
}


def _make_temp_json():
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_companion_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(INITIAL_TEST_DATA, f, ensure_ascii=False, indent=2)
    return path


def _make_temp_history():
    fd, path = tempfile.mkstemp(suffix=".json", prefix="test_history_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"sessions": [], "total_sessions": 0}, f)
    return path


class TestPolyglotCompanion(unittest.TestCase):

    def setUp(self):
        self.test_path = _make_temp_json()
        self.hist_path = _make_temp_history()

    def tearDown(self):
        for p in (self.test_path, self.hist_path):
            if os.path.exists(p):
                os.remove(p)

    # ── generate_adventure ──────────────────────

    def test_adventure_returns_all_fields(self):
        """探险报告应包含所有必要字段"""
        result = generate_adventure(self.test_path, self.hist_path)
        required = [
            "language", "emoji", "feature_name", "feature_blurb",
            "code_example", "fun_fact", "mini_exercise",
            "study_tips", "pomodoro_steps", "session_id", "generated_at",
        ]
        for f in required:
            self.assertIn(f, result, f"缺少字段：{f}")

    def test_adventure_picks_current_language(self):
        """探险应取 current_index=2 对应的语言 Swift"""
        result = generate_adventure(self.test_path, self.hist_path)
        self.assertEqual(result["language"], "Swift")
        self.assertEqual(result["feature_name"], "Optional 类型与空安全")

    def test_adventure_swift_metadata(self):
        """Swift 探险应包含 Swift 的元数据"""
        result = generate_adventure(self.test_path, self.hist_path)
        self.assertIn("Optional", result["feature_name"])
        self.assertIn("Swift", result["language"])
        self.assertIn("🦅", result["emoji"])
        self.assertIn("print", result["code_example"])
        self.assertTrue(len(result["study_tips"]) > 0)
        self.assertTrue(len(result["mini_exercise"]) > 0)

    def test_adventure_index_advances(self):
        """每次探险后索引应前移一位（Swift→Kotlin→TypeScript...）"""
        expected = ["Swift", "Kotlin", "TypeScript", "JavaScript",
                    "Java", "C/C++", "Rust", "Go"]
        for lang in expected:
            result = generate_adventure(self.test_path, self.hist_path)
            self.assertEqual(result["language"], lang,
                             f"期望 {lang}，实际 {result['language']}")

    def test_adventure_index_wraps_around(self):
        """索引到达末尾后应循环回 0"""
        for _ in range(8):
            generate_adventure(self.test_path, self.hist_path)
        # 第 9 次 → Swift（index 回到 2）
        result = generate_adventure(self.test_path, self.hist_path)
        self.assertEqual(result["language"], "Swift")

    def test_adventure_updates_json(self):
        """探险后 JSON 的 current_index 应更新"""
        generate_adventure(self.test_path, self.hist_path)  # Swift(2)→Kotlin(3)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 3)
        self.assertEqual(data["last_language"], "Swift")

    def test_adventure_saves_history(self):
        """探险后应保存历史记录"""
        generate_adventure(self.test_path, self.hist_path)
        with open(self.hist_path, "r", encoding="utf-8") as f:
            hist = json.load(f)
        self.assertEqual(hist["total_sessions"], 1)
        self.assertEqual(hist["sessions"][0]["language"], "Swift")

    def test_adventure_session_id_unique(self):
        """每次探险的 session_id 应唯一"""
        ids = set()
        for _ in range(5):
            result = generate_adventure(self.test_path, self.hist_path)
            self.assertNotIn(result["session_id"], ids)
            ids.add(result["session_id"])

    def test_adventure_timestamp_updated(self):
        """探险后 updated_at 应更新为当前时间"""
        generate_adventure(self.test_path, self.hist_path)
        with open(self.test_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertNotEqual(data["updated_at"], INITIAL_TEST_DATA["updated_at"])

    # ── get_adventure_report ─────────────────────

    def test_report_contains_language(self):
        """报告应包含语言名称"""
        report = get_adventure_report("Rust", self.test_path)
        self.assertIn("Rust", report)

    def test_report_contains_feature(self):
        """报告应包含特性名称"""
        report = get_adventure_report("Rust", self.test_path)
        self.assertIn("所有权", report)

    def test_report_contains_code(self):
        """报告应包含代码示例"""
        report = get_adventure_report("Rust", self.test_path)
        self.assertIn("fn main()", report)

    def test_report_contains_fun_fact(self):
        """报告应包含趣味知识"""
        report = get_adventure_report("Rust", self.test_path)
        self.assertIn("编译时内存管理", report)

    def test_report_contains_exercise(self):
        """报告应包含迷你练习"""
        report = get_adventure_report("Rust", self.test_path)
        self.assertIn("修复借用错误", report)

    def test_report_no_language_uses_current(self):
        """不指定语言时使用当前轮换语言（Swift）"""
        report = get_adventure_report(json_path=self.test_path)
        self.assertIn("Swift", report)

    def test_report_unknown_language(self):
        """未知语言使用默认占位符，不崩溃"""
        report = get_adventure_report("Forth", self.test_path)
        self.assertIn("Forth", report)

    def test_report_markdown_format(self):
        """报告应为 Markdown 格式"""
        report = get_adventure_report("Go", self.test_path)
        self.assertIn("# 🌐 语言探险报告", report)
        self.assertIn("## 💻 代码示例", report)
        self.assertIn("## 🧪 迷你练习", report)
        self.assertIn("## 🍅 Pomodoro", report)

    # ── get_companion_stats ─────────────────────

    def test_stats_empty_history(self):
        """空历史返回正确的初始状态"""
        st = get_companion_stats(self.hist_path)
        self.assertEqual(st["total_sessions"], 0)
        self.assertEqual(st["session_count"], 0)
        self.assertEqual(st["language_counts"], {})

    def test_stats_accumulates(self):
        """统计应累积所有探险记录"""
        generate_adventure(self.test_path, self.hist_path)
        generate_adventure(self.test_path, self.hist_path)
        generate_adventure(self.test_path, self.hist_path)
        st = get_companion_stats(self.hist_path)
        self.assertEqual(st["total_sessions"], 3)
        self.assertEqual(st["session_count"], 3)

    def test_stats_language_counts(self):
        """语言计数应正确"""
        generate_adventure(self.test_path, self.hist_path)  # Swift
        generate_adventure(self.test_path, self.hist_path)  # Kotlin
        generate_adventure(self.test_path, self.hist_path)  # TypeScript
        st = get_companion_stats(self.hist_path)
        counts = st["language_counts"]
        self.assertEqual(counts.get("Swift", 0), 1)
        self.assertEqual(counts.get("Kotlin", 0), 1)
        self.assertEqual(counts.get("TypeScript", 0), 1)

    def test_stats_recent_sessions(self):
        """recent_sessions 最多返回 5 条"""
        for i in range(7):
            generate_adventure(self.test_path, self.hist_path)
        st = get_companion_stats(self.hist_path)
        self.assertLessEqual(len(st["recent_sessions"]), 5)

    # ── LANGUAGE_ADVENTURES ─────────────────────

    def test_all_languages_have_adventures(self):
        """所有 8 种语言都有探险数据"""
        EXPECTED = ["Rust", "Go", "Swift", "Kotlin",
                    "TypeScript", "JavaScript", "Java", "C/C++"]
        for lang in EXPECTED:
            self.assertIn(lang, LANGUAGE_ADVENTURES, f"缺少 {lang}")

    def test_adventure_has_required_fields(self):
        """每种语言的探险数据包含必要字段"""
        required = ["emoji", "file_ext", "feature_name", "feature_blurb",
                    "code_example", "fun_fact", "mini_exercise", "study_tips"]
        for lang, adv in LANGUAGE_ADVENTURES.items():
            missing = [f for f in required if f not in adv]
            self.assertEqual(missing, [], f"{lang} 缺少字段：{missing}")

    def test_exercise_has_required_fields(self):
        """迷你练习包含必要字段"""
        required = ["title", "description", "broken_code", "hint"]
        for lang, adv in LANGUAGE_ADVENTURES.items():
            ex = adv.get("mini_exercise", {})
            missing = [f for f in required if f not in ex]
            self.assertEqual(missing, [], f"{lang} 练习缺少字段：{missing}")

    # ── POMODORO_STEPS ──────────────────────────

    def test_pomodoro_has_4_steps(self):
        """Pomodoro 节奏应有 4 步"""
        self.assertEqual(len(POMODORO_STEPS), 4)

    def test_pomodoro_total_80_minutes(self):
        """Pomodoro 总时长应为 80 分钟（25×3 专注 + 5min 复盘）"""
        total = sum(s["minutes"] for s in POMODORO_STEPS)
        self.assertEqual(total, 80)


class TestPolyglotCompanionIntegration(unittest.TestCase):

    def setUp(self):
        self.test_path = _make_temp_json()
        self.hist_path = _make_temp_history()

    def tearDown(self):
        for p in (self.test_path, self.hist_path):
            if os.path.exists(p):
                os.remove(p)

    def test_full_rotation_cycle(self):
        """完整轮换一圈（8 次），验证所有语言出现且历史完整"""
        seen = set()
        for _ in range(8):
            result = generate_adventure(self.test_path, self.hist_path)
            self.assertNotIn(result["language"], seen)
            seen.add(result["language"])
        self.assertEqual(len(seen), 8)

    def test_adventure_then_report(self):
        """探险后查询报告应反映新的当前语言"""
        generate_adventure(self.test_path, self.hist_path)  # Swift → Kotlin
        report = get_adventure_report(json_path=self.test_path)
        self.assertIn("Kotlin", report)

    def test_stats_after_full_cycle(self):
        """完整一轮后每种语言出现 1 次"""
        for _ in range(8):
            generate_adventure(self.test_path, self.hist_path)
        st = get_companion_stats(self.hist_path)
        counts = st["language_counts"]
        for lang in ["Rust", "Go", "Swift", "Kotlin",
                     "TypeScript", "JavaScript", "Java", "C/C++"]:
            self.assertEqual(counts.get(lang, 0), 1,
                             f"{lang} 应出现 1 次，实际 {counts.get(lang, 0)} 次")


if __name__ == "__main__":
    unittest.main(verbosity=2)
